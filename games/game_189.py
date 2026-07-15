from .base import Game
import random

class ShortestPathPerturbationGame(Game):

    game_rule_zh = """\
我们来玩一个"最短路径扰动判定"游戏，规则如下：

游戏设定了一个未知的简单、连通、无向、无权图 G，顶点集合为 {{1, 2, ..., {n}}}。图中有四个特殊的已标注顶点：
- S = {s}
- T = {t}
- U = {u}
- V = {v}

这四个顶点互不相同。图的边集对你不可见，你只能通过查询来获取信息。

你的目标是判断：如果在原图 G 上添加一条新边 (U, V)，从 S 到 T 的最短距离是否会严格减小。

你可以进行距离查询，每次查询两个顶点之间在原图 G 上的最短距离。查询格式如下：

<query_dist>a,b</query_dist>

其中 a 和 b 是顶点编号（1 到 {n} 之间）。我会回复一个非负整数，表示原图 G 上 a 到 b 的最短距离。

注意：
1. 所有查询都是针对原图 G 的，不能查询添加边之后的距离。
2. 请尽可能少地使用查询次数。
3. 每次只能提交一个查询标签。

当你收集到足够信息后，请提交最终判定结果。格式如下：

<answer>是</answer>

或

<answer>否</answer>

其中"是"表示添加边 (U, V) 会使 S 到 T 的最短距离严格减小，"否"表示不会减小。

若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Shortest Path Perturbation" game. Here are the rules:

The game involves an unknown simple, connected, undirected, unweighted graph G with vertex set {{1, 2, ..., {n}}}. There are four special labeled vertices in the graph:
- S = {s}
- T = {t}
- U = {u}
- V = {v}

These four vertices are all distinct. The edge set is hidden from you, and you can only obtain information through queries.

Your goal is to determine: if we add a new edge (U, V) to the original graph G, will the shortest distance from S to T strictly decrease?

You can perform distance queries to ask for the shortest distance between two vertices in the original graph G. The query format is:

<query_dist>a,b</query_dist>

where a and b are vertex IDs (between 1 and {n}). I will respond with a non-negative integer representing the shortest distance from a to b in the original graph G.

Note:
1. All queries are about the original graph G; you cannot query distances after adding the edge.
2. Please use as few queries as possible.
3. Each turn can only contain one query tag.

When you have collected enough information, submit your final decision in the following format:

<answer>Yes</answer>

or

<answer>No</answer>

where "Yes" means adding edge (U, V) will strictly decrease the shortest distance from S to T, and "No" means it will not decrease.

If the answer is wrong or the format is invalid, the game fails.
"""

    contextualized_rule_zh_1 = """\
这是交通规划领域的"路网最短路径扰动判定"推演。
我们设定了一个未知的简单、连通的无向路网图 G，代表城市中各个路口，路口集合为 {{1, 2, ..., {n}}}。图中有四个特殊的已标注路口：
- 核心物流枢纽 S = {s}
- 目标分拨中心 T = {t}
- 拟建高架桥起点 U = {u}
- 拟建高架桥终点 V = {v}

这四个路口互不相同。路网的现有道路分布对你不可见，你只能通过路网探测查询来获取信息。

你的目标是判断：如果在现有路网 G 上新增一条直达高架桥通道 (U, V)，从物流枢纽 S 到分拨中心 T 的最短通行距离（经过的路段数）是否会严格减小。

你可以进行路径探测，每次查询两个路口之间在现有路网 G 上的最短通行距离。查询格式如下：

<query_dist>a,b</query_dist>

其中 a 和 b 是路口编号（1 到 {n} 之间）。我会回复一个非负整数，表示现有路网 G 上 a 到 b 的最短通行距离。

注意：
1. 所有查询都是针对原路网 G 的，不能查询添加高架桥之后的距离。
2. 请尽可能少地使用查询次数。
3. 每次只能提交一个查询标签。

当你收集到足够信息后，请提交最终规划判定。格式如下：

<answer>是</answer>

或

<answer>否</answer>

其中"是"表示新增高架通道 (U, V) 会使 S 到 T 的最短距离严格减小，"否"表示不会减小。

若答案错误或格式不符，推演失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Shortest Path Perturbation Evaluation" in the field of traffic planning.
The scenario involves an unknown simple, connected, undirected road network graph G, representing various intersections in a city, with the intersection set being {{1, 2, ..., {n}}}. There are four special labeled intersections in the network:
- Core Logistics Hub S = {s}
- Target Distribution Center T = {t}
- Proposed Viaduct Start U = {u}
- Proposed Viaduct End V = {v}

These four intersections are all distinct. The current road connections are hidden from you, and you can only obtain information through network probing queries.

Your goal is to determine: if we construct a new direct viaduct corridor (U, V) on the existing road network G, will the shortest travel distance (number of road segments) from the Logistics Hub S to the Distribution Center T strictly decrease?

You can perform route probing to ask for the shortest travel distance between two intersections in the existing road network G. The query format is:

<query_dist>a,b</query_dist>

where a and b are intersection IDs (between 1 and {n}). I will respond with a non-negative integer representing the shortest travel distance from a to b in the existing road network G.

Note:
1. All queries are about the existing road network G; you cannot query distances after the viaduct is constructed.
2. Please use as few queries as possible.
3. Each turn can only contain one query tag.

When you have collected enough information, submit your final planning decision in the following format:

<answer>Yes</answer>

or

<answer>No</answer>

where "Yes" means constructing the viaduct corridor (U, V) will strictly decrease the shortest travel distance from S to T, and "No" means it will not decrease.

If the answer is wrong or the format is invalid, the evaluation fails.
"""

    contextualized_rule_zh_2 = """\
这是医疗急救领域的"医院转运通道优化"推演。
我们设定了一个未知的简单、连通的无向通道网络 G，代表医院内各个科室节点，科室集合为 {{1, 2, ..., {n}}}。网络中有四个特殊的已标注科室：
- 急诊科 S = {s}
- 重症监护室(ICU) T = {t}
- 拟建快速通道起点 U = {u}
- 拟建快速通道终点 V = {v}

这四个科室互不相同。医院现有的转运通道对你不可见，你只能通过通道距离查询来获取信息。

你的目标是判断：如果在现有网络 G 上打通一条内部直连通道 (U, V)，从急诊科 S 转运病人到重症监护室 T 的最短转移距离（经过的通道段数）是否会严格减小。

你可以进行距离查询，每次查询两个科室之间在现有网络 G 上的最短转移距离。查询格式如下：

<query_dist>a,b</query_dist>

其中 a 和 b 是科室编号（1 到 {n} 之间）。我会回复一个非负整数，表示现有网络 G 上 a 到 b 的最短转移距离。

注意：
1. 所有查询都是针对原网络 G 的，不能查询打通通道之后的最短距离。
2. 请尽可能少地使用查询次数。
3. 每次只能提交一个查询标签。

当你收集到足够信息后，请提交最终优化判定。格式如下：

<answer>是</answer>

或

<answer>否</answer>

其中"是"表示打通快速通道 (U, V) 会使急诊科 S 到重症监护室 T 的最短转移距离严格减小，"否"表示不会减小。

若答案错误或格式不符，推演失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Hospital Transfer Corridor Optimization" evaluation in the medical emergency field.
The scenario involves an unknown simple, connected, undirected corridor network G, representing various department nodes in a hospital, with the department set being {{1, 2, ..., {n}}}. There are four special labeled departments in the network:
- Emergency Department S = {s}
- Intensive Care Unit (ICU) T = {t}
- Proposed Rapid Corridor Start U = {u}
- Proposed Rapid Corridor End V = {v}

These four departments are all distinct. The current hospital transfer connections are hidden from you, and you can only obtain information through corridor distance queries.

Your goal is to determine: if we open up a new internal direct corridor (U, V) in the existing network G, will the shortest transfer distance (number of corridor segments) for moving a patient from the Emergency Department S to the ICU T strictly decrease?

You can perform distance queries to ask for the shortest transfer distance between two departments in the existing network G. The query format is:

<query_dist>a,b</query_dist>

where a and b are department IDs (between 1 and {n}). I will respond with a non-negative integer representing the shortest transfer distance from a to b in the existing network G.

Note:
1. All queries are about the existing network G; you cannot query distances after the new corridor is opened.
2. Please use as few queries as possible.
3. Each turn can only contain one query tag.

When you have collected enough information, submit your final optimization decision in the following format:

<answer>Yes</answer>

or

<answer>No</answer>

where "Yes" means opening the rapid corridor (U, V) will strictly decrease the shortest transfer distance from S to T, and "No" means it will not decrease.

If the answer is wrong or the format is invalid, the evaluation fails.
"""

    contextualized_rule_zh_3 = """\
这是校园网络设施领域的"网络路由跳数优化"分析。
我们设定了一个未知的简单、连通的无向拓扑网络 G，代表校园内的各个网络节点（路由器/交换机），节点集合为 {{1, 2, ..., {n}}}。网络中有四个特殊的已标注节点：
- 核心服务器 S = {s}
- 主教学楼基站 T = {t}
- 拟铺设直连光缆的节点 U = {u}
- 拟铺设直连光缆的节点 V = {v}

这四个节点互不相同。现有的网络物理拓扑对你不可见，你只能通过路由跳数查询来获取信息。

你的目标是判断：如果在现有拓扑 G 上铺设一条新的直连光缆 (U, V)，数据包从核心服务器 S 到主教学楼基站 T 传输的最少网络跳数是否会严格减小。

你可以进行跳数查询，每次查询两个节点之间在现有网络 G 上的最少路由跳数。查询格式如下：

<query_dist>a,b</query_dist>

其中 a 和 b 是节点编号（1 到 {n} 之间）。我会回复一个非负整数，表示现有网络 G 上 a 到 b 的最少跳数。

注意：
1. 所有查询都是针对原网络 G 的，不能查询铺设光缆之后的跳数。
2. 请尽可能少地使用查询次数。
3. 每次只能提交一个查询标签。

当你收集到足够信息后，请提交最终优化判定。格式如下：

<answer>是</answer>

或

<answer>否</answer>

其中"是"表示铺设光缆 (U, V) 会使核心服务器 S 到教学楼基站 T 的网络跳数严格减小，"否"表示不会减小。

若答案错误或格式不符，分析失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Network Routing Hop Optimization" analysis in the field of campus network infrastructure.
The scenario involves an unknown simple, connected, undirected topological network G, representing various network nodes (routers/switches) on campus, with the node set being {{1, 2, ..., {n}}}. There are four special labeled nodes in the network:
- Core Server S = {s}
- Main Academic Building Base Station T = {t}
- Proposed Fiber Optic Direct Connection Node U = {u}
- Proposed Fiber Optic Direct Connection Node V = {v}

These four nodes are all distinct. The current physical network topology is hidden from you, and you can only obtain information through routing hop queries.

Your goal is to determine: if we lay a new direct fiber optic cable (U, V) on the existing topology G, will the minimum network routing hops for data packets from the Core Server S to the Base Station T strictly decrease?

You can perform hop queries to ask for the minimum routing hops between two nodes in the existing network G. The query format is:

<query_dist>a,b</query_dist>

where a and b are node IDs (between 1 and {n}). I will respond with a non-negative integer representing the minimum routing hops from a to b in the existing network G.

Note:
1. All queries are about the existing network G; you cannot query hops after the cable is laid.
2. Please use as few queries as possible.
3. Each turn can only contain one query tag.

When you have collected enough information, submit your final optimization decision in the following format:

<answer>Yes</answer>

or

<answer>No</answer>

where "Yes" means laying the fiber optic cable (U, V) will strictly decrease the network hops from S to T, and "No" means it will not decrease.

If the answer is wrong or the format is invalid, the analysis fails.
"""

    contextualized_rule_zh_4 = """\
这是自动化制造领域的"流水线物料传送优化"推演。
我们设定了一个未知的简单、连通的无向传送带网络 G，代表工厂内部各个工作站，工作站集合为 {{1, 2, ..., {n}}}。网络中有四个特殊的已标注工作站：
- 原料库 S = {s}
- 总装车间 T = {t}
- 拟新增传送带起点 U = {u}
- 拟新增传送带终点 V = {v}

这四个工作站互不相同。目前的物料传送链路拓扑对你不可见，你只能通过传送段数查询来获取信息。

你的目标是判断：如果在现有传送带网络 G 上加装一条直接相连的传送带 (U, V)，从原料库 S 输送物料到总装车间 T 所需经历的最少传送环节数是否会严格减小。

你可以进行环节数查询，每次查询两个工作站之间在现有网络 G 上的最少传送环节数。查询格式如下：

<query_dist>a,b</query_dist>

其中 a 和 b 是工作站编号（1 到 {n} 之间）。我会回复一个非负整数，表示现有网络 G 上 a 到 b 的最少传送环节数。

注意：
1. 所有查询都是针对原网络 G 的，不能查询加装传送带之后的环节数。
2. 请尽可能少地使用查询次数。
3. 每次只能提交一个查询标签。

当你收集到足够信息后，请提交最终改造判定。格式如下：

<answer>是</answer>

或

<answer>否</answer>

其中"是"表示加装传送带 (U, V) 会使原料库 S 到总装车间 T 的最少传送环节数严格减小，"否"表示不会减小。

若答案错误或格式不符，推演失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's conduct an "Assembly Line Material Conveyance Optimization" evaluation in automated manufacturing.
The scenario involves an unknown simple, connected, undirected conveyor belt network G, representing various workstations inside a factory, with the workstation set being {{1, 2, ..., {n}}}. There are four special labeled workstations in the network:
- Raw Material Depot S = {s}
- Final Assembly Workshop T = {t}
- Proposed New Conveyor Belt Start U = {u}
- Proposed New Conveyor Belt End V = {v}

These four workstations are all distinct. The current topology of material conveyance links is hidden from you, and you can only obtain information through conveyance segment queries.

Your goal is to determine: if we install a new directly connected conveyor belt (U, V) on the existing network G, will the minimum number of conveyance segments required to transport materials from the Raw Material Depot S to the Final Assembly Workshop T strictly decrease?

You can perform segment queries to ask for the minimum conveyance segments between two workstations in the existing network G. The query format is:

<query_dist>a,b</query_dist>

where a and b are workstation IDs (between 1 and {n}). I will respond with a non-negative integer representing the minimum conveyance segments from a to b in the existing network G.

Note:
1. All queries are about the existing network G; you cannot query the segment counts after the new belt is installed.
2. Please use as few queries as possible.
3. Each turn can only contain one query tag.

When you have collected enough information, submit your final renovation decision in the following format:

<answer>Yes</answer>

or

<answer>No</answer>

where "Yes" means installing the conveyor belt (U, V) will strictly decrease the minimum conveyance segments from S to T, and "No" means it will not decrease.

If the answer is wrong or the format is invalid, the evaluation fails.
"""

    contextualized_rule_zh_5 = """\
这是司法侦查领域的"证据链推导步数判定"分析。
我们设定了一个未知的简单、连通的无向证据关联图 G，代表卷宗中的各类证据节点，节点集合为 {{1, 2, ..., {n}}}。图中有四个特殊的已标注证据节点：
- 初始线索 S = {s}
- 核心犯罪事实 T = {t}
- 待核实的关联证据 U = {u}
- 待核实的关联证据 V = {v}

这四个节点互不相同。目前的证据链直接关联网络对你不可见，你只能通过推导步数查询来获取信息。

你的目标是判断：如果在现有卷宗证据网络 G 中确认证据 U 和证据 V 之间存在直接逻辑关联（即新增一条关联边），从初始线索 S 成功推导到核心犯罪事实 T 所需的最短推导步数是否会严格减小。

你可以进行证据关联查询，每次查询两个证据节点之间在现有网络 G 上的最短推导步数。查询格式如下：

<query_dist>a,b</query_dist>

其中 a 和 b 是节点编号（1 到 {n} 之间）。我会回复一个非负整数，表示现有证据网络 G 上 a 到 b 的最短推导步数。

注意：
1. 所有查询都是针对现有卷宗网络 G 的，不能查询确立新逻辑关联之后的推导步数。
2. 请尽可能少地使用查询次数。
3. 每次只能提交一个查询标签。

当你收集到足够信息后，请提交最终逻辑研判。格式如下：

<answer>是</answer>

或

<answer>否</answer>

其中"是"表示确认证据关联 (U, V) 会使初始线索 S 到核心犯罪事实 T 的最短推导步数严格减小，"否"表示不会减小。

若答案错误或格式不符，分析失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct an "Evidence Chain Derivation Steps Determination" analysis in judicial investigation.
The scenario involves an unknown simple, connected, undirected evidence association graph G, representing various evidence nodes in the case file, with the node set being {{1, 2, ..., {n}}}. There are four special labeled evidence nodes in the graph:
- Initial Clue S = {s}
- Core Criminal Fact T = {t}
- Pending Associated Evidence U = {u}
- Pending Associated Evidence V = {v}

These four nodes are all distinct. The current direct association network of the evidence chain is hidden from you, and you can only obtain information through derivation step queries.

Your goal is to determine: if we confirm a direct logical association between evidence U and evidence V in the existing evidence network G (i.e., adding a new association edge), will the shortest derivation steps required to successfully deduce from the Initial Clue S to the Core Criminal Fact T strictly decrease?

You can perform evidence association queries to ask for the shortest derivation steps between two evidence nodes in the existing network G. The query format is:

<query_dist>a,b</query_dist>

where a and b are node IDs (between 1 and {n}). I will respond with a non-negative integer representing the shortest derivation steps from a to b in the existing evidence network G.

Note:
1. All queries are about the existing evidence network G; you cannot query the derivation steps after the new logical association is established.
2. Please use as few queries as possible.
3. Each turn can only contain one query tag.

When you have collected enough information, submit your final logical deduction decision in the following format:

<answer>Yes</answer>

or

<answer>No</answer>

where "Yes" means confirming the evidence association (U, V) will strictly decrease the shortest derivation steps from S to T, and "No" means it will not decrease.

If the answer is wrong or the format is invalid, the analysis fails.
"""

    tags = ["answer", "query_dist"]
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "s": 1, "t": 5, "u": 2, "v": 4,
                "edges": [
                    (1, 2), (2, 3), (3, 4), (4, 5),
                    (1, 6), (6, 7), (7, 8), (8, 5)
                ],
                "answer": True
            },
            2: {
                "n": 10,
                "s": 1, "t": 8, "u": 4, "v": 9,
                "edges": [
                    (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
                    (6, 7), (7, 8), (8, 9), (9, 10)
                ],
                "answer": True
            },
            3: {
                "n": 12,
                "s": 1, "t": 6, "u": 8, "v": 10,
                "edges": [
                    (1, 2), (2, 3), (3, 6),
                    (1, 4), (4, 5), (5, 6),
                    (8, 9), (9, 10), (10, 11), (11, 12),
                    (6, 7), (7, 8)
                ],
                "answer": False
            },
            4: {
                "n": 15,
                "s": 1, "t": 12, "u": 5, "v": 10,
                "edges": [
                    (1, 2), (2, 3), (3, 4), (4, 15), (15, 12),
                    (1, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 12),
                    (2, 13), (13, 14), (14, 11), (11, 12)
                ],
                "answer": True
            },
            5: {
                "n": 20,
                "s": 1, "t": 15, "u": 8, "v": 18,
                "edges": [
                    (1, 2), (2, 3), (3, 4), (4, 15),
                    (1, 5), (5, 6), (6, 7), (7, 8),
                    (8, 9), (9, 10), (10, 11),
                    (15, 16), (16, 17), (17, 18),
                    (18, 19), (19, 20),
                    (11, 12), (12, 13), (13, 14), (14, 15)
                ],
                "answer": False
            },
        },
        "en": {
            1: {
                "n": 8,
                "s": 1, "t": 5, "u": 2, "v": 4,
                "edges": [
                    (1, 2), (2, 3), (3, 4), (4, 5),
                    (1, 6), (6, 7), (7, 8), (8, 5)
                ],
                "answer": True
            },
            2: {
                "n": 10,
                "s": 1, "t": 8, "u": 4, "v": 9,
                "edges": [
                    (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
                    (6, 7), (7, 8), (8, 9), (9, 10)
                ],
                "answer": True
            },
            3: {
                "n": 12,
                "s": 1, "t": 6, "u": 8, "v": 10,
                "edges": [
                    (1, 2), (2, 3), (3, 6),
                    (1, 4), (4, 5), (5, 6),
                    (8, 9), (9, 10), (10, 11), (11, 12),
                    (6, 7), (7, 8)
                ],
                "answer": False
            },
            4: {
                "n": 15,
                "s": 1, "t": 12, "u": 5, "v": 10,
                "edges": [
                    (1, 2), (2, 3), (3, 4), (4, 15), (15, 12),
                    (1, 5), (5, 6), (6, 7), (7, 8), (8, 9), (9, 10), (10, 12),
                    (2, 13), (13, 14), (14, 11), (11, 12)
                ],
                "answer": True
            },
            5: {
                "n": 20,
                "s": 1, "t": 15, "u": 8, "v": 18,
                "edges": [
                    (1, 2), (2, 3), (3, 4), (4, 15),
                    (1, 5), (5, 6), (6, 7), (7, 8),
                    (8, 9), (9, 10), (10, 11),
                    (15, 16), (16, 17), (17, 18),
                    (18, 19), (19, 20),
                    (11, 12), (12, 13), (13, 14), (14, 15)
                ],
                "answer": False
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["s"] = cfg["s"]
        self._game_info["t"] = cfg["t"]
        self._game_info["u"] = cfg["u"]
        self._game_info["v"] = cfg["v"]
        
        self.n = cfg["n"]
        self.s = cfg["s"]
        self.t = cfg["t"]
        self.u = cfg["u"]
        self.v = cfg["v"]
        
        self.graph = {i: [] for i in range(1, self.n + 1)}
        for a, b in cfg["edges"]:
            self.graph[a].append(b)
            self.graph[b].append(a)
        
        self.ground_truth_answer = cfg["answer"]
        
        self.query_count = 0

    def _bfs_distance(self, start, end):
        if start == end:
            return 0
        
        from collections import deque
        queue = deque([start])
        visited = {start}
        distance = {start: 0}
        
        while queue:
            node = queue.popleft()
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    distance[neighbor] = distance[node] + 1
                    queue.append(neighbor)
                    if neighbor == end:
                        return distance[neighbor]
        
        return float('inf')

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if self.config.language == "zh":
            player_answer = (raw_ans == "是")
        else:
            player_answer = (raw_ans.lower() == "yes")
        
        return player_answer == self.ground_truth_answer

    def _cf_core_produce(self, parsed_info):
        if "query_dist" in parsed_info:
            self.query_count += 1
            
            try:
                raw = parsed_info["query_dist"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Query must contain exactly two vertex IDs")
                
                a, b = int(parts[0]), int(parts[1])
                
                if a < 1 or a > self.n or b < 1 or b > self.n:
                    if self.config.language == "zh":
                        return f"错误：顶点编号必须在 1 到 {self.n} 之间。"
                    else:
                        return f"Error: Vertex ID must be between 1 and {self.n}."
                
                dist = self._bfs_distance(a, b)
                return str(dist)
                
            except ValueError as e:
                if self.config.language == "zh":
                    return f"错误：查询格式无效。请使用格式 <query_dist>a,b</query_dist>"
                else:
                    return f"Error: Invalid query format. Please use format <query_dist>a,b</query_dist>"
        
        raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        stripped = correct.strip()
        
        try:
            val = int(stripped)
            return str(val + 1)
        except ValueError:
            pass
        
        if stripped == "是":
            return "否"
        if stripped == "否":
            return "是"
        if stripped.lower() == "yes":
            if stripped.isupper(): return "NO"
            if stripped.istitle(): return "No"
            return "no"
        if stripped.lower() == "no":
            if stripped.isupper(): return "YES"
            if stripped.istitle(): return "Yes"
            return "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        results = []
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                query_content = f"{i},{j}"
                
                dist = self._bfs_distance(i, j)
                
                results.append({
                    "query": f"<query_dist>{query_content}</query_dist>",
                    "answer": str(dist)
                })
        return results