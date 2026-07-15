from .base import Game
import random

class DirectedGraphReachabilityGame(Game):

    game_rule_zh = """\
我们来玩一个"有向图可达性推断"游戏，规则如下：

游戏设定了一个整数 N = {n}，顶点集合为 {{0, 1, ..., N-1}}，所有运算按模 N 进行。

存在一个未知但固定的偏移集合 S，它是 {{1, 2, ..., N-1}} 的子集。对于任意顶点 u，当且仅当 (v - u) mod N 属于 S 时，存在有向边 u -> v。这个结构在所有顶点上完全一致，不存在其他边。

可达性定义：从起点到终点可以经由零条或多条有向边连通。零条边表示顶点可达自身。

你的目标是：判定是否存在某个顶点 w，使得从 w 出发可以到达所有顶点 {{0, 1, ..., N-1}}；若存在，给出任意一个这样的顶点编号。

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实设定如实回答：

1. Probe(u, v)：询问是否存在边 u -> v。回答"是"或"否"。
2. Route(u, [a1, a2, ..., ak])：从 u 按序尝试走到 a1、a2、...、ak。回答：
   - 若全部单跳存在："成功，终点 ak"
   - 否则："失败：第 i 步（从 x 到 ai）不存在"，并给出当前停留顶点 x 与失败步数 i
3. Outdeg(u)：询问顶点 u 的出度。回答一个整数。
4. Reach(u, L)：询问从 u 出发在至多 L 跳内可达的不同顶点数量。回答一个整数。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次只能包含一个标签。请使用以下 XML 格式：

- Probe 查询（例如询问边 0 -> 1）：
<query_probe>0,1</query_probe>

- Route 查询（例如从 0 经过 [1,2,3]）：
<query_route>0,[1,2,3]</query_route>

- Outdeg 查询（例如询问顶点 0）：
<query_outdeg>0</query_outdeg>

- Reach 查询（例如从顶点 0 出发最多 3 跳）：
<query_reach>0,3</query_reach>

提交最终答案时，必须说明是否存在可达全体的顶点，格式如下：

- 若存在，给出一个示例顶点（例如顶点 0）：
<answer>exists, vertex=0</answer>

- 若不存在：
<answer>not_exists</answer>
"""

    game_rule_en = """\
Let's play a "Directed Graph Reachability Inference" game. Here are the rules:

The game sets an integer N = {n}, with a vertex set {{0, 1, ..., N-1}}, and all operations are modulo N.

There exists an unknown but fixed offset set S, which is a subset of {{1, 2, ..., N-1}}. For any vertex u, there exists a directed edge u -> v if and only if (v - u) mod N belongs to S. This structure is completely consistent across all vertices, and no other edges exist.

Reachability definition: From a starting point to an endpoint, you can connect via zero or more directed edges. Zero edges means a vertex can reach itself.

Your goal is: Determine whether there exists a vertex w such that all vertices {{0, 1, ..., N-1}} are reachable from w; if so, provide any one such vertex number.

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully based on the actual setup:

1. Probe(u, v): Ask if there exists an edge u -> v. Answer "Yes" or "No".
2. Route(u, [a1, a2, ..., ak]): Try to walk from u sequentially to a1, a2, ..., ak. Answer:
   - If all single hops exist: "Success, endpoint ak"
   - Otherwise: "Failed: step i (from x to ai) does not exist", with current vertex x and failed step i
3. Outdeg(u): Ask for the out-degree of vertex u. Answer an integer.
4. Reach(u, L): Ask for the number of distinct vertices reachable from u within at most L hops. Answer an integer.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Probe query (e.g., asking about edge 0 -> 1):
<query_probe>0,1</query_probe>

- Route query (e.g., from 0 through [1,2,3]):
<query_route>0,[1,2,3]</query_route>

- Outdeg query (e.g., asking about vertex 0):
<query_outdeg>0</query_outdeg>

- Reach query (e.g., from vertex 0 within at most 3 hops):
<query_reach>0,3</query_reach>

When submitting the final answer, specify whether a vertex that reaches all exists:

- If exists, provide an example vertex (e.g., vertex 0):
<answer>exists, vertex=0</answer>

- If not exists:
<answer>not_exists</answer>
"""

    contextualized_rule_zh_1 = """\
【交通网络枢纽排查】
本地区包含 N = {n} 个物流中转站，编号为 {{0, 1, ..., N-1}}。目前正在规划一种标准化的单向直飞航线。

根据规划，存在一个未知但固定的航线偏移量集合 S。对于任意中转站 u，仅当 (v - u) mod N 属于集合 S 时，才存在一条从 u 直飞 v 的单向航线。这种环形网络的拓扑在所有站点上完全一致。

“可达性”意味着从一个中转站出发，可以通过零次或多次航班中转到达目标站点。

你的任务是：找出是否存在一个“核心枢纽站” w，使得从 w 出发能够将货物投递到所有的 {{0, 1, ..., N-1}} 个站点。如果存在，请给出一个符合条件的站点编号。

你可以通过以下指令向调度中心查询信息：
1. Probe(u, v)：查询是否存在从站点 u 直飞 v 的航线。
2. Route(u, [a1, a2, ..., ak])：尝试安排货物从 u 依次经停 a1, a2, ..., ak。
3. Outdeg(u)：查询站点 u 拥有的直飞出发航线总数。
4. Reach(u, L)：查询从站点 u 出发，在不超过 L 个航段（跳）内能够覆盖的站点总数。

收集到足够信息后，请提交结果。

每次仅包含一个 XML 标签：
- Probe 查询：<query_probe>0,1</query_probe>
- Route 查询：<query_route>0,[1,2,3]</query_route>
- Outdeg 查询：<query_outdeg>0</query_outdeg>
- Reach 查询：<query_reach>0,3</query_reach>

最终答案提交：
- 若存在核心枢纽，给出一个示例：<answer>exists, vertex=0</answer>
- 若不存在：<answer>not_exists</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Logistics Scenario]
This region contains N = {n} logistics transit stations, numbered {{0, 1, ..., N-1}}. A standardized one-way direct flight network is being planned.

According to the plan, there is an unknown but fixed set of route offsets S. For any station u, a direct one-way flight from u to v exists if and only if (v - u) mod N belongs to set S. This circular network topology is completely uniform across all stations.

"Reachability" means that cargo originating from a station can be delivered to a destination station via zero or multiple connecting flights.

Your task is to determine if there exists a "core hub" station w such that cargo can be delivered from w to all {{0, 1, ..., N-1}} stations. If so, provide the ID of any one such station.

You can query the dispatch center for information using the following commands:
1. Probe(u, v): Query if there is a direct flight from station u to v.
2. Route(u, [a1, a2, ..., ak]): Attempt to route cargo from u sequentially through a1, a2, ..., ak.
3. Outdeg(u): Query the total number of outbound direct flights from station u.
4. Reach(u, L): Query the number of distinct stations that can be reached from u within a maximum of L flight segments (hops).

Once you have gathered enough information, submit your final result.

Each query must contain exactly one XML tag:
- Probe query: <query_probe>0,1</query_probe>
- Route query: <query_route>0,[1,2,3]</query_route>
- Outdeg query: <query_outdeg>0</query_outdeg>
- Reach query: <query_reach>0,3</query_reach>

Final answer submission:
- If a core hub exists, provide an example: <answer>exists, vertex=0</answer>
- If not exists: <answer>not_exists</answer>
"""

    contextualized_rule_zh_2 = """\
【医疗感染源流调追踪】
在一座拥有 N = {n} 个科室（编号为 {{0, 1, ..., N-1}}）的大型隔离医院中，我们正在调查某种通过气流单向传播的病原体。

医院的单向通风系统遵循一个固定的偏移规律集合 S。对于任意科室 u，仅当 (v - u) mod N 属于集合 S 时，存在一条从 u 到 v 的单向气流通道。所有科室的通风设计均完全一致。

“可达性”意味着病原体可以通过零条或多条单向通风管道进行跨科室传播。

你的任务是：判断是否存在一个“总污染源”科室 w，一旦该科室被污染，病原体将通过气流系统传播到所有 {{0, 1, ..., N-1}} 个科室。如果存在，请提供任意一个可能的科室编号。

你可以向工程部提出以下流调排查：
1. Probe(u, v)：检测是否存在从科室 u 直达科室 v 的气流通道。
2. Route(u, [a1, a2, ..., ak])：追踪从 u 开始，依次流经 a1, a2, ..., ak 的气流路径是否连通。
3. Outdeg(u)：查询从科室 u 直接吹向其他科室的管道数量。
4. Reach(u, L)：查询从科室 u 的气流在最多跨越 L 个管道节点后能波及的不同科室总数。

收集信息后，请提交追踪结论。

每次仅限一个 XML 标签：
- Probe 查询：<query_probe>0,1</query_probe>
- Route 查询：<query_route>0,[1,2,3]</query_route>
- Outdeg 查询：<query_outdeg>0</query_outdeg>
- Reach 查询：<query_reach>0,3</query_reach>

最终答案提交：
- 若存在总污染源，给出一个示例科室：<answer>exists, vertex=0</answer>
- 若不存在：<answer>not_exists</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Infection Tracing Scenario]
In a large isolation hospital with N = {n} departments (numbered {{0, 1, ..., N-1}}), we are investigating a pathogen that spreads via one-way airflow.

The hospital's one-way ventilation system follows a fixed set of offset rules S. For any department u, a one-way airflow duct from u to v exists if and only if (v - u) mod N belongs to set S. This ventilation design is perfectly uniform across all departments.

"Reachability" implies that the pathogen can spread across departments via zero or multiple one-way ventilation ducts.

Your task is to determine whether there exists a "primary contamination source" department w such that if contaminated, the pathogen would spread to all {{0, 1, ..., N-1}} departments. If so, provide the ID of any such department.

You can request the following tracing checks from the engineering team:
1. Probe(u, v): Detect if there is a direct airflow duct from department u to v.
2. Route(u, [a1, a2, ..., ak]): Trace if the airflow path from u sequentially through a1, a2, ..., ak is connected.
3. Outdeg(u): Query the number of direct outward ducts blowing from department u.
4. Reach(u, L): Query the total number of distinct departments the airflow from u can affect within at most L duct nodes.

Once you have gathered sufficient information, submit your conclusion.

Each query must contain exactly one XML tag:
- Probe query: <query_probe>0,1</query_probe>
- Route query: <query_route>0,[1,2,3]</query_route>
- Outdeg query: <query_outdeg>0</query_outdeg>
- Reach query: <query_reach>0,3</query_reach>

Final answer submission:
- If a primary source exists, provide an example: <answer>exists, vertex=0</answer>
- If not exists: <answer>not_exists</answer>
"""

    contextualized_rule_zh_3 = """\
【教育先修课体系设计】
我们正在建立一个包含 N = {n} 个知识模块的课程体系，模块编号为 {{0, 1, ..., N-1}}。

课程之间存在单向的先修依赖关系，这些关系由一个固定的偏移规则集合 S 决定。对于任意模块 u，仅当 (v - u) mod N 属于集合 S 时，模块 u 是模块 v 的直接先修课（即学完 u 即可解锁 v）。这一结构模式在整个知识体系中全局一致。

“可达性”指的是可以通过一条或多条先修依赖链，依次解锁后续课程。

你的任务是：判断是否存在一门“核心导论课” w，使得学生只要从这门课开始学习，最终就能逐步解锁并学完全部 {{0, 1, ..., N-1}} 个模块。若存在，请给出任意一门这样的课程编号。

你可以向教务系统发起以下查询：
1. Probe(u, v)：询问模块 u 是否是模块 v 的直接先修课。
2. Route(u, [a1, a2, ..., ak])：验证一条从 u 开始，依次解锁 a1, a2, ..., ak 的学习路径。
3. Outdeg(u)：询问以模块 u 为直接先修课的后续模块数量。
4. Reach(u, L)：询问从模块 u 开始，最多经过 L 层先修解锁链，总共能开放多少个模块。

信息充分后，请提交你的教研分析结论。

每次提交仅限一个 XML 标签：
- Probe 查询：<query_probe>0,1</query_probe>
- Route 查询：<query_route>0,[1,2,3]</query_route>
- Outdeg 查询：<query_outdeg>0</query_outdeg>
- Reach 查询：<query_reach>0,3</query_reach>

最终答案提交：
- 若存在核心导论课，给出课程编号：<answer>exists, vertex=0</answer>
- 若不存在：<answer>not_exists</answer>
"""

    contextualized_rule_en_3 = """\
[Educational Prerequisite System Scenario]
We are building a curriculum system comprising N = {n} knowledge modules, numbered {{0, 1, ..., N-1}}.

There are one-way prerequisite dependencies between modules, governed by a fixed set of offset rules S. For any module u, u is a direct prerequisite for v (i.e., completing u unlocks v) if and only if (v - u) mod N belongs to set S. This structural pattern is globally consistent across the entire curriculum.

"Reachability" means that subsequent courses can be sequentially unlocked through zero or more prerequisite dependency chains.

Your task is to determine if there exists a "core introductory course" w such that starting from this course, a student can eventually unlock and study all {{0, 1, ..., N-1}} modules. If so, provide the ID of any one such course.

You can query the academic system using the following commands:
1. Probe(u, v): Query if module u is a direct prerequisite for module v.
2. Route(u, [a1, a2, ..., ak]): Verify a study path starting from u and sequentially unlocking a1, a2, ..., ak.
3. Outdeg(u): Query the number of subsequent modules that have module u as their direct prerequisite.
4. Reach(u, L): Query the total number of distinct modules that can be unlocked starting from u within at most L dependency layers.

Submit your pedagogical conclusion once you have enough information.

Each query must contain exactly one XML tag:
- Probe query: <query_probe>0,1</query_probe>
- Route query: <query_route>0,[1,2,3]</query_route>
- Outdeg query: <query_outdeg>0</query_outdeg>
- Reach query: <query_reach>0,3</query_reach>

Final answer submission:
- If a core introductory course exists, provide an example: <answer>exists, vertex=0</answer>
- If not exists: <answer>not_exists</answer>
"""

    contextualized_rule_zh_4 = """\
【工业流水线物料流转】
在一个自动化车间内，部署了 N = {n} 个加工工站，编号为 {{0, 1, ..., N-1}}。这些工站由一系列单向物料传送带相连。

由于标准化装配要求，传送带的连接服从一个固定的偏移集合 S。对于任意工站 u，当且仅当 (v - u) mod N 属于集合 S 时，存在一条从 u 流向 v 的单向传送带。所有工站的物料输出逻辑完全一致。

“可达性”是指物料可以从一个工站被放入，经过一条或多条传送带接力，最终抵达目标工站。

你的任务是：诊断是否存在一个“总控投料站” w，使得将原材料投入 w 后，物料能够顺着流水线被输送至所有的 {{0, 1, ..., N-1}} 个工站。如果存在，请指出任意一个这样的投料站编号。

你可以向中控系统发起以下探测指令：
1. Probe(u, v)：探测是否存在从工站 u 直达工站 v 的单向传送带。
2. Route(u, [a1, a2, ..., ak])：模拟物料从 u 投放，能否依次流转经过 a1, a2, ..., ak。
3. Outdeg(u)：查询工站 u 连接出的直接传送带数量。
4. Reach(u, L)：查询从工站 u 投料，经过最多 L 次传送带接力，物料能够抵达的不同工站数量。

排查完毕后，请提交诊断报告。

单次只能发送一个 XML 标签：
- Probe 探测：<query_probe>0,1</query_probe>
- Route 模拟：<query_route>0,[1,2,3]</query_route>
- Outdeg 统计：<query_outdeg>0</query_outdeg>
- Reach 统计：<query_reach>0,3</query_reach>

最终答案提交：
- 若存在总控投料站，给出站点编号：<answer>exists, vertex=0</answer>
- 若不存在：<answer>not_exists</answer>
"""

    contextualized_rule_en_4 = """\
[Industrial Assembly Line Scenario]
In an automated workshop, N = {n} processing stations are deployed, numbered {{0, 1, ..., N-1}}. These stations are connected by a series of one-way material conveyor belts.

Due to standardized assembly requirements, the conveyor connections follow a fixed offset set S. For any station u, a one-way conveyor belt from u to v exists if and only if (v - u) mod N belongs to set S. This material output logic is perfectly uniform across all stations.

"Reachability" means that materials introduced at a station can be transported to a target station via zero or multiple relay conveyor belts.

Your task is to diagnose whether there exists a "master feeding station" w such that raw materials fed into w can be transported along the assembly line to all {{0, 1, ..., N-1}} stations. If so, indicate the ID of any one such feeding station.

You can issue the following probing commands to the central control system:
1. Probe(u, v): Detect if there is a direct one-way conveyor belt from station u to v.
2. Route(u, [a1, a2, ..., ak]): Simulate whether material fed at u can sequentially flow through a1, a2, ..., ak.
3. Outdeg(u): Query the number of outbound conveyor belts connected from station u.
4. Reach(u, L): Query the total number of distinct stations materials can reach from station u within at most L conveyor relays.

Submit your diagnostic report once the inspection is complete.

Each query must contain exactly one XML tag:
- Probe query: <query_probe>0,1</query_probe>
- Route query: <query_route>0,[1,2,3]</query_route>
- Outdeg query: <query_outdeg>0</query_outdeg>
- Reach query: <query_reach>0,3</query_reach>

Final answer submission:
- If a master feeding station exists, provide an example: <answer>exists, vertex=0</answer>
- If not exists: <answer>not_exists</answer>
"""

    contextualized_rule_zh_5 = """\
【法律条款引用溯源】
一份新颁布的法典包含 N = {n} 个法理节点（条款），编号为 {{0, 1, ..., N-1}}。这些条款之间存在严格的单向引用关系。

法典的编纂采用了一种结构化的引用逻辑，即固定的偏移集合 S。对于任意条款 u，当且仅当 (v - u) mod N 属于集合 S 时，条款 u 会明确直接引用条款 v 作为下位释明。这一法律逻辑框架在所有条款上保持一致。

“可达性”是指从一个条款出发，可以通过零次或多次递归引用，推演出另一个条款的内容。

你的职责是：分析是否存在一个“基础法理条款” w，使得只要确立了条款 w，就能通过层层引用逻辑涵盖并解释所有的 {{0, 1, ..., N-1}} 个法理节点。如果存在，请提供任意一个此类条款的编号。

你可以向法务数据库检索以下关联信息：
1. Probe(u, v)：查询条款 u 是否直接引用了条款 v。
2. Route(u, [a1, a2, ..., ak])：验证从条款 u 出发，能否按照 a1, a2, ..., ak 的顺序进行合法引用推演。
3. Outdeg(u)：查询条款 u 直接引用了多少个其他条款。
4. Reach(u, L)：查询从条款 u 展开，最多经过 L 层引用深度，能够覆盖到的不同条款总数。

完成法理推演后，请提交你的法务分析结论。

每次检索需提供唯一的 XML 标签：
- Probe 检索：<query_probe>0,1</query_probe>
- Route 检索：<query_route>0,[1,2,3]</query_route>
- Outdeg 检索：<query_outdeg>0</query_outdeg>
- Reach 检索：<query_reach>0,3</query_reach>

最终答案提交：
- 若存在基础法理条款，给出条款编号：<answer>exists, vertex=0</answer>
- 若不存在：<answer>not_exists</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Code Citation Tracing Scenario]
A newly promulgated legal code contains N = {n} jurisprudential nodes (clauses), numbered {{0, 1, ..., N-1}}. These clauses exhibit a strict one-way citation relationship.

The drafting of the code employs a structured citation logic determined by a fixed offset set S. For any clause u, clause u explicitly cites clause v as its subordinate interpretation if and only if (v - u) mod N belongs to set S. This legal logic framework remains consistent across all clauses.

"Reachability" refers to the ability to deduce the content of a target clause starting from an initial clause through zero or multiple recursive citations.

Your duty is to analyze whether there exists a "fundamental jurisprudential clause" w such that establishing clause w allows for the interpretation of all {{0, 1, ..., N-1}} jurisprudential nodes through cascaded citation logic. If so, provide the ID of any such clause.

You can retrieve the following relational data from the legal database:
1. Probe(u, v): Query if clause u directly cites clause v.
2. Route(u, [a1, a2, ..., ak]): Verify if a legitimate citation deduction can proceed from clause u sequentially through a1, a2, ..., ak.
3. Outdeg(u): Query the number of other clauses directly cited by clause u.
4. Reach(u, L): Query the total number of distinct clauses covered starting from clause u within a maximum citation depth of L.

Submit your legal analysis conclusion upon completing the deduction.

Each retrieval must contain exactly one XML tag:
- Probe query: <query_probe>0,1</query_probe>
- Route query: <query_route>0,[1,2,3]</query_route>
- Outdeg query: <query_outdeg>0</query_outdeg>
- Reach query: <query_reach>0,3</query_reach>

Final answer submission:
- If a fundamental jurisprudential clause exists, provide an example: <answer>exists, vertex=0</answer>
- If not exists: <answer>not_exists</answer>
"""

    tags = ["answer", "query_probe", "query_route", "query_outdeg", "query_reach"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 5, "offsets": [1]},
            2: {"n": 6, "offsets": [1, 2]},
            3: {"n": 8, "offsets": [2, 3]},
            4: {"n": 10, "offsets": [2, 4]},
            5: {"n": 12, "offsets": [3, 6]},
        },
        "en": {
            1: {"n": 5, "offsets": [1]},
            2: {"n": 6, "offsets": [1, 2]},
            3: {"n": 8, "offsets": [2, 3]},
            4: {"n": 10, "offsets": [2, 4]},
            5: {"n": 12, "offsets": [3, 6]},
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
        self.n = cfg["n"]
        self.offsets = set(cfg["offsets"])
        
        self._game_info["n"] = self.n
        
        self.reachable = {}
        for u in range(self.n):
            self.reachable[u] = self._compute_reachable(u)
        
        self.universal_vertices = []
        for u in range(self.n):
            if len(self.reachable[u]) == self.n:
                self.universal_vertices.append(u)
        
        self.exists_universal = len(self.universal_vertices) > 0

    def _compute_reachable(self, start):
        visited = set([start])
        queue = [start]
        
        while queue:
            u = queue.pop(0)
            for offset in self.offsets:
                v = (u + offset) % self.n
                if v not in visited:
                    visited.add(v)
                    queue.append(v)
        
        return visited

    def _has_edge(self, u, v):
        offset = (v - u) % self.n
        return offset in self.offsets

    def _compute_reachable_within_hops(self, start, max_hops):
        if max_hops < 0:
            return 0
        
        visited = set([start])
        current_level = {start}
        
        for hop in range(max_hops):
            next_level = set()
            for u in current_level:
                for offset in self.offsets:
                    v = (u + offset) % self.n
                    if v not in visited:
                        visited.add(v)
                        next_level.add(v)
            current_level = next_level
            if not current_level:
                break
        
        return len(visited)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans.startswith("not_exists"):
            return not self.exists_universal
        elif raw_ans.startswith("exists"):
            try:
                parts = raw_ans.split(",")
                vertex_part = None
                for part in parts:
                    if "vertex=" in part:
                        vertex_part = part.split("=")[1].strip()
                        break
                
                if vertex_part is None:
                    return False
                
                vertex = int(vertex_part)
                
                if vertex < 0 or vertex >= self.n:
                    return False
                
                return len(self.reachable[vertex]) == self.n
            except:
                return False
        else:
            return False

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        mapping = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes",
            "yes": "no",
            "no": "yes"
        }
        
        if correct in mapping:
            return mapping[correct]
        
        if "成功" in correct or "Success" in correct:
            return "失败：第 1 步不存在" if self.config.language == "zh" else "Failed: step 1 does not exist"
        
        if "失败" in correct or "Failed" in correct:
            return "成功，终点 0" if self.config.language == "zh" else "Success, endpoint 0"
        
        return correct + "_WRONG"

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        try:
            if "query_probe" in parsed_info:
                raw = parsed_info["query_probe"].strip()
                u, v = [int(x.strip()) for x in raw.split(",")]
                
                if u < 0 or u >= self.n or v < 0 or v >= self.n:
                    return "错误：顶点编号超出范围。" if self.config.language == "zh" else "Error: Vertex number out of range."
                
                return yes_res if self._has_edge(u, v) else no_res

            elif "query_route" in parsed_info:
                raw = parsed_info["query_route"].strip()
                parts = raw.split("[", 1)
                if len(parts) != 2:
                    return "错误：格式无效。" if self.config.language == "zh" else "Error: Invalid format."
                
                u_str = parts[0].strip().rstrip(",")
                u = int(u_str.strip())
                
                path_str = parts[1].strip().rstrip("]")
                path = [int(x.strip()) for x in path_str.split(",") if x.strip()]
                
                if u < 0 or u >= self.n:
                    return "错误：起点编号超出范围。" if self.config.language == "zh" else "Error: Start vertex out of range."
                
                current = u
                for i, next_vertex in enumerate(path, 1):
                    if next_vertex < 0 or next_vertex >= self.n:
                        return "错误：路径中顶点编号超出范围。" if self.config.language == "zh" else "Error: Vertex in path out of range."
                    
                    if not self._has_edge(current, next_vertex):
                        if self.config.language == "zh":
                            return f"失败：第 {i} 步（从 {current} 到 {next_vertex}）不存在"
                        else:
                            return f"Failed: step {i} (from {current} to {next_vertex}) does not exist"
                    current = next_vertex
                
                if self.config.language == "zh":
                    return f"成功，终点 {current}"
                else:
                    return f"Success, endpoint {current}"

            elif "query_outdeg" in parsed_info:
                u = int(parsed_info["query_outdeg"].strip())
                
                if u < 0 or u >= self.n:
                    return "错误：顶点编号超出范围。" if self.config.language == "zh" else "Error: Vertex number out of range."
                
                return str(len(self.offsets))

            elif "query_reach" in parsed_info:
                raw = parsed_info["query_reach"].strip()
                u, L = [int(x.strip()) for x in raw.split(",")]
                
                if u < 0 or u >= self.n:
                    return "错误：顶点编号超出范围。" if self.config.language == "zh" else "Error: Vertex number out of range."
                
                if L < 0:
                    return "错误：跳数不能为负。" if self.config.language == "zh" else "Error: Hops cannot be negative."
                
                count = self._compute_reachable_within_hops(u, L)
                return str(count)

            else:
                raise ValueError("No valid query tag found.")
                
        except Exception as e:
            return f"错误：{str(e)}" if self.config.language == "zh" else f"Error: {str(e)}"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for u in range(self.n):
            for v in range(self.n):
                content = f"{u},{v}"
                
                parsed_info = {"query_probe": content}
                
                answer = self._cf_core_produce(parsed_info)
                
                queries.append({
                    "query": f"<query_probe>{content}</query_probe>",
                    "answer": answer
                })
        
        return queries