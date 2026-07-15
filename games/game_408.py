from .base import Game
import random

class GraphReachabilityGame(Game):
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"有向图推理"游戏，规则如下：

游戏设定了一个固定的有向图 G，包含 {n} 个节点，命名为 L1, L2, ..., L{n}。

每个节点具有一个可见标签，标签是由字母集合 {{A, B, C, D, E, F}} 的子集构成，每个标签包含 1 到 3 个字母。

图中的边由一个全局一致但不可见的判定函数 R 决定：对于任意两个节点 Li 和 Lj，如果 R(标签i, 标签j) 为真，则存在有向边 Li→Lj。函数 R 在整局游戏中保持不变，图结构也固定不变。

**初始公开信息：**
节点数量：{n}
各节点标签：{labels}

**可达闭包定义：**
从某个节点 Lx 出发，沿有向边反复传播至稳定所能到达的所有节点集合（包含起点本身），记为 C(Lx)。

**可用查询类型（请尽可能少地使用查询次数）：**

1. 计数查询 - 查询从某节点出发的可达闭包大小
   格式：<query_count>Lx</query_count>
   回答：一个整数，表示 |C(Lx)|

2. 全覆盖查询 - 查询某节点的可达闭包是否覆盖所有节点（每局最多使用 2 次）
   格式：<query_all>Lx</query_all>
   回答："是"或"否"

3. 一跳邻居查询 - 查询某节点的直接出边邻居（每局最多使用 2 次）
   格式：<query_neighbors1>Lx</query_neighbors1>
   回答：按字典序排列的节点名称列表，如 "L1,L3,L5" 或空列表 "[]"

4. 两跳增量查询 - 查询两跳可达但一跳不可达的节点（每局最多使用 2 次）
   格式：<query_delta2>Lx</query_delta2>
   回答：按字典序排列的节点名称列表，或空列表 "[]"

5. 包含查询 - 查询 C(Lx) 是否包含 C(Ly)
   格式：<query_cover_ge>Lx,Ly</query_cover_ge>
   回答："是"或"否"

6. 相等查询 - 查询 C(Lx) 是否等于 C(Ly)
   格式：<query_cover_eq>Lx,Ly</query_cover_eq>
   回答："是"或"否"

**你的目标：**
1. 归纳出边生成规律 R'（用自然语言或形式化描述，需与所有查询反馈一致）
2. 判定是否存在可达闭包为全体节点的节点；若存在则给出其名称，若不存在则明确声明
3. 提供两条可验证的预测

**最终答案格式：**
<answer>
rule: [你归纳的规律描述]
global_node: [节点名称如 L3，或 "不存在"]
prediction1: [预测类型]=[预测内容]
prediction2: [预测类型]=[预测内容]
</answer>

预测类型包括：
- edge:Lx,Ly=[是/否] （预测是否存在边 Lx→Ly）
- all:Lx=[是/否] （预测 C(Lx) 是否为全体）
- count:Lx=[整数] （预测 |C(Lx)| 的值）

示例：
<answer>
rule: 如果源节点标签与目标节点标签有交集，则存在边
global_node: L2
prediction1: edge:L1,L3=是
prediction2: count:L4=5
</answer>
"""

    game_rule_en = """\
Let's play a "Directed Graph Reasoning" game with the following rules:

The game features a fixed directed graph G with {n} nodes, named L1, L2, ..., L{n}.

Each node has a visible label, which is a subset of the letter set {{A, B, C, D, E, F}}, containing 1 to 3 letters.

The edges in the graph are determined by a globally consistent but invisible decision function R: for any two nodes Li and Lj, if R(label_i, label_j) is true, then there exists a directed edge Li→Lj. Function R remains constant throughout the game, and the graph structure is fixed.

**Initial Public Information:**
Number of nodes: {n}
Node labels: {labels}

**Reachability Closure Definition:**
The reachability closure C(Lx) from node Lx is the set of all nodes reachable by repeatedly following directed edges until stable (including the starting point itself).

**Available Query Types (use as few queries as possible):**

1. Count Query - Query the size of reachability closure from a node
   Format: <query_count>Lx</query_count>
   Answer: An integer representing |C(Lx)|

2. All Query - Query whether a node's reachability closure covers all nodes (max 2 uses per game)
   Format: <query_all>Lx</query_all>
   Answer: "Yes" or "No"

3. One-hop Neighbors Query - Query direct out-edge neighbors of a node (max 2 uses per game)
   Format: <query_neighbors1>Lx</query_neighbors1>
   Answer: Lexicographically sorted node names like "L1,L3,L5" or empty list "[]"

4. Two-hop Delta Query - Query nodes reachable in two hops but not one hop (max 2 uses per game)
   Format: <query_delta2>Lx</query_delta2>
   Answer: Lexicographically sorted node names or empty list "[]"

5. Cover-GE Query - Query whether C(Lx) contains C(Ly)
   Format: <query_cover_ge>Lx,Ly</query_cover_ge>
   Answer: "Yes" or "No"

6. Cover-EQ Query - Query whether C(Lx) equals C(Ly)
   Format: <query_cover_eq>Lx,Ly</query_cover_eq>
   Answer: "Yes" or "No"

**Your Goal:**
1. Deduce the edge generation rule R' (in natural language or formal description, consistent with all query feedback)
2. Determine whether there exists a node whose reachability closure is all nodes; if so, provide its name; otherwise, explicitly state it doesn't exist
3. Provide two verifiable predictions

**Final Answer Format:**
<answer>
rule: [your deduced rule description]
global_node: [node name like L3, or "none"]
prediction1: [prediction type]=[prediction content]
prediction2: [prediction type]=[prediction content]
</answer>

Prediction types include:
- edge:Lx,Ly=[Yes/No] (predict whether edge Lx→Ly exists)
- all:Lx=[Yes/No] (predict whether C(Lx) is all nodes)
- count:Lx=[integer] (predict the value of |C(Lx)|)

Example:
<answer>
rule: An edge exists if source label intersects with target label
global_node: L2
prediction1: edge:L1,L3=Yes
prediction2: count:L4=5
</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入“交通枢纽网络”规划系统。

当前区域包含 {n} 个交通枢纽站，命名为 L1, L2, ..., L{n}。
每个枢纽站配备了特定的设施资源，表示为字母集合 {{A, B, C, D, E, F}} 的子集，每个站点拥有 1 到 3 种设施。

枢纽间的单向直达路线由一个全局一致但隐蔽的开通判定规则 R 决定：对于任意两个枢纽站 Li 和 Lj，如果 R(设施i, 设施j) 为真，则存在一条 Li→Lj 的直达路线。判定规则 R 在整个路网规划中保持不变。

**初始公开信息：**
枢纽站数量：{n}
各站点设施：{labels}

**可达网络定义：**
从某个枢纽站 Lx 出发，通过不断换乘直达路线所能到达的所有枢纽站集合（包含起点本身），记为可达网络 C(Lx)。

**可用查询类型（请尽可能少地使用查询次数）：**

1. 计数查询 - 查询从某站点出发的可达网络规模
   格式：<query_count>Lx</query_count>
   回答：一个整数，表示 |C(Lx)|

2. 全覆盖查询 - 查询某站点的可达网络是否覆盖所有站点（每局最多使用 2 次）
   格式：<query_all>Lx</query_all>
   回答："是"或"否"

3. 一跳邻居查询 - 查询某站点可直达的下游站点（每局最多使用 2 次）
   格式：<query_neighbors1>Lx</query_neighbors1>
   回答：按字典序排列的站点名称列表，如 "L1,L3,L5" 或空列表 "[]"

4. 两跳增量查询 - 查询需一次换乘（两跳）可达但直达不可达的站点（每局最多使用 2 次）
   格式：<query_delta2>Lx</query_delta2>
   回答：按字典序排列的站点名称列表，或空列表 "[]"

5. 包含查询 - 查询 C(Lx) 是否完全覆盖 C(Ly)
   格式：<query_cover_ge>Lx,Ly</query_cover_ge>
   回答："是"或"否"

6. 相等查询 - 查询 C(Lx) 是否等同于 C(Ly)
   格式：<query_cover_eq>Lx,Ly</query_cover_eq>
   回答："是"或"否"

**你的目标：**
1. 归纳出路线开通规律 R'（用自然语言或形式化描述，需与所有查询反馈一致）
2. 判定是否存在可达网络覆盖所有站点的“全局核心枢纽”；若存在则给出其名称，若不存在则明确声明
3. 提供两条可验证的预测

**最终答案格式：**
<answer>
rule: [你归纳的规律描述]
global_node: [站点名称如 L3，或 "不存在"]
prediction1: [预测类型]=[预测内容]
prediction2: [预测类型]=[预测内容]
</answer>

预测类型包括：
- edge:Lx,Ly=[是/否] （预测是否存在直达路线 Lx→Ly）
- all:Lx=[是/否] （预测 C(Lx) 是否覆盖全网）
- count:Lx=[整数] （预测 |C(Lx)| 的值）

示例：
<answer>
rule: 如果始发站设施与终点站设施有交集，则存在直达路线
global_node: L2
prediction1: edge:L1,L3=是
prediction2: count:L4=5
</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Transportation Hub Network" planning system.

The current region features {n} transportation hubs, named L1, L2, ..., L{n}.
Each hub is equipped with specific facility resources, represented as a subset of the letter set {{A, B, C, D, E, F}}, containing 1 to 3 facilities.

The one-way direct routes between hubs are determined by a globally consistent but hidden activation rule R: for any two hubs Li and Lj, if R(facilities_i, facilities_j) is true, a direct route Li→Lj exists. This rule R remains constant throughout the network planning.

**Initial Public Information:**
Number of hubs: {n}
Hub facilities: {labels}

**Reachable Network Definition:**
The reachable network C(Lx) from hub Lx is the set of all hubs reachable by successive transfers along direct routes (including the starting hub itself).

**Available Query Types (use as few queries as possible):**

1. Count Query - Query the size of the reachable network from a hub
   Format: <query_count>Lx</query_count>
   Answer: An integer representing |C(Lx)|

2. All Query - Query whether a hub's reachable network covers all hubs (max 2 uses per game)
   Format: <query_all>Lx</query_all>
   Answer: "Yes" or "No"

3. One-hop Neighbors Query - Query direct downstream hubs from a hub (max 2 uses per game)
   Format: <query_neighbors1>Lx</query_neighbors1>
   Answer: Lexicographically sorted hub names like "L1,L3,L5" or empty list "[]"

4. Two-hop Delta Query - Query hubs reachable with exactly one transfer but not directly (max 2 uses per game)
   Format: <query_delta2>Lx</query_delta2>
   Answer: Lexicographically sorted hub names or empty list "[]"

5. Cover-GE Query - Query whether C(Lx) completely covers C(Ly)
   Format: <query_cover_ge>Lx,Ly</query_cover_ge>
   Answer: "Yes" or "No"

6. Cover-EQ Query - Query whether C(Lx) is identical to C(Ly)
   Format: <query_cover_eq>Lx,Ly</query_cover_eq>
   Answer: "Yes" or "No"

**Your Goal:**
1. Deduce the route activation rule R' (in natural language or formal description, consistent with all query feedback)
2. Determine whether there exists a "global core hub" whose reachable network covers all hubs; if so, provide its name; otherwise, explicitly state "none"
3. Provide two verifiable predictions

**Final Answer Format:**
<answer>
rule: [your deduced rule description]
global_node: [hub name like L3, or "none"]
prediction1: [prediction type]=[prediction content]
prediction2: [prediction type]=[prediction content]
</answer>

Prediction types include:
- edge:Lx,Ly=[Yes/No] (predict whether direct route Lx→Ly exists)
- all:Lx=[Yes/No] (predict whether C(Lx) covers all hubs)
- count:Lx=[integer] (predict the value of |C(Lx)|)

Example:
<answer>
rule: A route exists if the origin's facilities intersect with the destination's facilities
global_node: L2
prediction1: edge:L1,L3=Yes
prediction2: count:L4=5
</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎进入“医疗转诊网络”评估系统。

当前医疗机构包含 {n} 个科室，命名为 L1, L2, ..., L{n}。
每个科室具备特定的医疗资质，表示为资质集合 {{A, B, C, D, E, F}} 的子集，每个科室拥有 1 到 3 种资质。

科室间的单向转诊通道由一个全局一致但隐蔽的开放规则 R 决定：对于任意两个科室 Li 和 Lj，如果 R(资质i, 资质j) 为真，则存在一条 Li→Lj 的转诊通道。规则 R 在整个医疗网络中保持不变。

**初始公开信息：**
科室数量：{n}
各科室资质：{labels}

**转诊覆盖面定义：**
从某个科室 Lx 出发，通过连续转诊所能到达的所有科室集合（包含起点本身），记为转诊覆盖面 C(Lx)。

**可用查询类型（请尽可能少地使用查询次数）：**

1. 计数查询 - 查询从某科室出发的转诊覆盖面规模
   格式：<query_count>Lx</query_count>
   回答：一个整数，表示 |C(Lx)|

2. 全覆盖查询 - 查询某科室的转诊覆盖面是否涵盖所有科室（每局最多使用 2 次）
   格式：<query_all>Lx</query_all>
   回答："是"或"否"

3. 一跳邻居查询 - 查询某科室可直接转诊的下游科室（每局最多使用 2 次）
   格式：<query_neighbors1>Lx</query_neighbors1>
   回答：按字典序排列的科室名称列表，如 "L1,L3,L5" 或空列表 "[]"

4. 两跳增量查询 - 查询需一次中转转诊（两跳）可达但直接转诊不可达的科室（每局最多使用 2 次）
   格式：<query_delta2>Lx</query_delta2>
   回答：按字典序排列的科室名称列表，或空列表 "[]"

5. 包含查询 - 查询 C(Lx) 是否完全包含 C(Ly)
   格式：<query_cover_ge>Lx,Ly</query_cover_ge>
   回答："是"或"否"

6. 相等查询 - 查询 C(Lx) 是否等同于 C(Ly)
   格式：<query_cover_eq>Lx,Ly</query_cover_eq>
   回答："是"或"否"

**你的目标：**
1. 归纳出转诊通道开放规律 R'（用自然语言或形式化描述，需与所有查询反馈一致）
2. 判定是否存在转诊覆盖面涵盖所有科室的“综合首诊科室”；若存在则给出其名称，若不存在则明确声明
3. 提供两条可验证的预测

**最终答案格式：**
<answer>
rule: [你归纳的规律描述]
global_node: [科室名称如 L3，或 "不存在"]
prediction1: [预测类型]=[预测内容]
prediction2: [预测类型]=[预测内容]
</answer>

预测类型包括：
- edge:Lx,Ly=[是/否] （预测是否存在转诊通道 Lx→Ly）
- all:Lx=[是/否] （预测 C(Lx) 是否涵盖全网）
- count:Lx=[整数] （预测 |C(Lx)| 的值）

示例：
<answer>
rule: 如果转出科室资质与转入科室资质有交集，则存在转诊通道
global_node: L2
prediction1: edge:L1,L3=是
prediction2: count:L4=5
</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Medical Referral Network" evaluation system.

The current healthcare facility contains {n} medical wards, named L1, L2, ..., L{n}.
Each ward has specific medical qualifications, represented as a subset of the letter set {{A, B, C, D, E, F}}, containing 1 to 3 qualifications.

The one-way referral channels between wards are determined by a globally consistent but hidden activation rule R: for any two wards Li and Lj, if R(qualifications_i, qualifications_j) is true, a direct referral channel Li→Lj exists. This rule R remains constant throughout the entire medical network.

**Initial Public Information:**
Number of wards: {n}
Ward qualifications: {labels}

**Referral Coverage Definition:**
The referral coverage C(Lx) from ward Lx is the set of all wards reachable through continuous referrals (including the starting ward itself).

**Available Query Types (use as few queries as possible):**

1. Count Query - Query the size of the referral coverage from a ward
   Format: <query_count>Lx</query_count>
   Answer: An integer representing |C(Lx)|

2. All Query - Query whether a ward's referral coverage covers all wards (max 2 uses per game)
   Format: <query_all>Lx</query_all>
   Answer: "Yes" or "No"

3. One-hop Neighbors Query - Query direct downstream wards from a ward (max 2 uses per game)
   Format: <query_neighbors1>Lx</query_neighbors1>
   Answer: Lexicographically sorted ward names like "L1,L3,L5" or empty list "[]"

4. Two-hop Delta Query - Query wards reachable with exactly one intermediate referral but not directly (max 2 uses per game)
   Format: <query_delta2>Lx</query_delta2>
   Answer: Lexicographically sorted ward names or empty list "[]"

5. Cover-GE Query - Query whether C(Lx) completely covers C(Ly)
   Format: <query_cover_ge>Lx,Ly</query_cover_ge>
   Answer: "Yes" or "No"

6. Cover-EQ Query - Query whether C(Lx) is identical to C(Ly)
   Format: <query_cover_eq>Lx,Ly</query_cover_eq>
   Answer: "Yes" or "No"

**Your Goal:**
1. Deduce the referral channel activation rule R' (in natural language or formal description, consistent with all query feedback)
2. Determine whether there exists a "comprehensive primary ward" whose referral coverage encompasses all wards; if so, provide its name; otherwise, explicitly state "none"
3. Provide two verifiable predictions

**Final Answer Format:**
<answer>
rule: [your deduced rule description]
global_node: [ward name like L3, or "none"]
prediction1: [prediction type]=[prediction content]
prediction2: [prediction type]=[prediction content]
</answer>

Prediction types include:
- edge:Lx,Ly=[Yes/No] (predict whether direct referral channel Lx→Ly exists)
- all:Lx=[Yes/No] (predict whether C(Lx) covers all wards)
- count:Lx=[integer] (predict the value of |C(Lx)|)

Example:
<answer>
rule: A referral channel exists if the transferring ward's qualifications intersect with the receiving ward's qualifications
global_node: L2
prediction1: edge:L1,L3=Yes
prediction2: count:L4=5
</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入“课程先修网络”分析系统。

当前知识图谱包含 {n} 个课程模块，命名为 L1, L2, ..., L{n}。
每个课程模块覆盖了特定的知识点，表示为知识点集合 {{A, B, C, D, E, F}} 的子集，每门课程包含 1 到 3 个知识点。

课程间的单向先修解锁通道由一个全局一致但隐蔽的逻辑规则 R 决定：对于任意两门课程 Li 和 Lj，如果 R(知识点i, 知识点j) 为真，则存在一条 Li→Lj 的解锁通道。判定规则 R 在整个学科体系中保持不变。

**初始公开信息：**
课程模块数量：{n}
各课程知识点：{labels}

**解锁辐射范围定义：**
从某门课程 Lx 出发，通过不断学习其后续解锁课程所能掌握的所有课程模块集合（包含起点本身），记为解锁辐射范围 C(Lx)。

**可用查询类型（请尽可能少地使用查询次数）：**

1. 计数查询 - 查询从某课程出发的解锁辐射范围规模
   格式：<query_count>Lx</query_count>
   回答：一个整数，表示 |C(Lx)|

2. 全覆盖查询 - 查询某课程的解锁辐射范围是否包含所有课程（每局最多使用 2 次）
   格式：<query_all>Lx</query_all>
   回答："是"或"否"

3. 一跳邻居查询 - 查询某课程可直接解锁的后续课程（每局最多使用 2 次）
   格式：<query_neighbors1>Lx</query_neighbors1>
   回答：按字典序排列的课程名称列表，如 "L1,L3,L5" 或空列表 "[]"

4. 两跳增量查询 - 查询需经过一门中间课程（两跳）才能解锁且无法直接解锁的课程（每局最多使用 2 次）
   格式：<query_delta2>Lx</query_delta2>
   回答：按字典序排列的课程名称列表，或空列表 "[]"

5. 包含查询 - 查询 C(Lx) 是否完全包含 C(Ly)
   格式：<query_cover_ge>Lx,Ly</query_cover_ge>
   回答："是"或"否"

6. 相等查询 - 查询 C(Lx) 是否等同于 C(Ly)
   格式：<query_cover_eq>Lx,Ly</query_cover_eq>
   回答："是"或"否"

**你的目标：**
1. 归纳出先修通道解锁规律 R'（用自然语言或形式化描述，需与所有查询反馈一致）
2. 判定是否存在解锁辐射范围包含所有课程的“基础导论课程”；若存在则给出其名称，若不存在则明确声明
3. 提供两条可验证的预测

**最终答案格式：**
<answer>
rule: [你归纳的规律描述]
global_node: [课程名称如 L3，或 "不存在"]
prediction1: [预测类型]=[预测内容]
prediction2: [预测类型]=[预测内容]
</answer>

预测类型包括：
- edge:Lx,Ly=[是/否] （预测是否存在解锁通道 Lx→Ly）
- all:Lx=[是/否] （预测 C(Lx) 是否覆盖整个学科）
- count:Lx=[整数] （预测 |C(Lx)| 的值）

示例：
<answer>
rule: 如果前置课程知识点与后续课程知识点有交集，则存在先修解锁通道
global_node: L2
prediction1: edge:L1,L3=是
prediction2: count:L4=5
</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Course Prerequisite Network" analysis system.

The current knowledge graph contains {n} course modules, named L1, L2, ..., L{n}.
Each course module covers specific knowledge points, represented as a subset of the letter set {{A, B, C, D, E, F}}, containing 1 to 3 knowledge points.

The one-way prerequisite unlocking channels between courses are determined by a globally consistent but hidden logic rule R: for any two courses Li and Lj, if R(knowledge_points_i, knowledge_points_j) is true, a direct unlocking channel Li→Lj exists. This rule R remains constant throughout the academic curriculum.

**Initial Public Information:**
Number of courses: {n}
Course knowledge points: {labels}

**Unlocked Curriculum Coverage Definition:**
The unlocked curriculum coverage C(Lx) from course Lx is the set of all courses that can be progressively unlocked and learned (including the starting course itself).

**Available Query Types (use as few queries as possible):**

1. Count Query - Query the size of the unlocked curriculum coverage from a course
   Format: <query_count>Lx</query_count>
   Answer: An integer representing |C(Lx)|

2. All Query - Query whether a course's unlocked curriculum coverage includes all courses (max 2 uses per game)
   Format: <query_all>Lx</query_all>
   Answer: "Yes" or "No"

3. One-hop Neighbors Query - Query direct subsequently unlocked courses from a course (max 2 uses per game)
   Format: <query_neighbors1>Lx</query_neighbors1>
   Answer: Lexicographically sorted course names like "L1,L3,L5" or empty list "[]"

4. Two-hop Delta Query - Query courses that can be unlocked with exactly one intermediate course but not directly (max 2 uses per game)
   Format: <query_delta2>Lx</query_delta2>
   Answer: Lexicographically sorted course names or empty list "[]"

5. Cover-GE Query - Query whether C(Lx) completely covers C(Ly)
   Format: <query_cover_ge>Lx,Ly</query_cover_ge>
   Answer: "Yes" or "No"

6. Cover-EQ Query - Query whether C(Lx) is identical to C(Ly)
   Format: <query_cover_eq>Lx,Ly</query_cover_eq>
   Answer: "Yes" or "No"

**Your Goal:**
1. Deduce the prerequisite unlocking channel logic rule R' (in natural language or formal description, consistent with all query feedback)
2. Determine whether there exists a "foundational gateway course" whose unlocked curriculum coverage encompasses all courses; if so, provide its name; otherwise, explicitly state "none"
3. Provide two verifiable predictions

**Final Answer Format:**
<answer>
rule: [your deduced rule description]
global_node: [course name like L3, or "none"]
prediction1: [prediction type]=[prediction content]
prediction2: [prediction type]=[prediction content]
</answer>

Prediction types include:
- edge:Lx,Ly=[Yes/No] (predict whether direct unlocking channel Lx→Ly exists)
- all:Lx=[Yes/No] (predict whether C(Lx) covers all courses)
- count:Lx=[integer] (predict the value of |C(Lx)|)

Example:
<answer>
rule: An unlocking channel exists if the prerequisite course's knowledge points intersect with the subsequent course's knowledge points
global_node: L2
prediction1: edge:L1,L3=Yes
prediction2: count:L4=5
</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入“生产流水线网络”控制系统。

当前车间包含 {n} 个生产工站，命名为 L1, L2, ..., L{n}。
每个工站具备特定的工艺属性，表示为工艺集合 {{A, B, C, D, E, F}} 的子集，每个工站拥有 1 到 3 种工艺属性。

工站间的单向物料流转通道由一个全局一致但隐蔽的工序判定规则 R 决定：对于任意两个工站 Li 和 Lj，如果 R(工艺i, 工艺j) 为真，则存在一条 Li→Lj 的流转通道。判定规则 R 在整条流水线规划中保持不变。

**初始公开信息：**
工站数量：{n}
各工站工艺：{labels}

**下游流转范围定义：**
从某个工站 Lx 出发，半成品物料沿着单向通道经过连续加工所能到达的所有下游工站集合（包含起点本身），记为下游流转范围 C(Lx)。

**可用查询类型（请尽可能少地使用查询次数）：**

1. 计数查询 - 查询从某工站出发的下游流转范围规模
   格式：<query_count>Lx</query_count>
   回答：一个整数，表示 |C(Lx)|

2. 全覆盖查询 - 查询某工站的下游流转范围是否覆盖所有工站（每局最多使用 2 次）
   格式：<query_all>Lx</query_all>
   回答："是"或"否"

3. 一跳邻居查询 - 查询接收某工站直接流转物料的下游工站（每局最多使用 2 次）
   格式：<query_neighbors1>Lx</query_neighbors1>
   回答：按字典序排列的工站名称列表，如 "L1,L3,L5" 或空列表 "[]"

4. 两跳增量查询 - 查询需经过一次中转加工（两跳）可达但直接流转不可达的工站（每局最多使用 2 次）
   格式：<query_delta2>Lx</query_delta2>
   回答：按字典序排列的工站名称列表，或空列表 "[]"

5. 包含查询 - 查询 C(Lx) 是否完全覆盖 C(Ly)
   格式：<query_cover_ge>Lx,Ly</query_cover_ge>
   回答："是"或"否"

6. 相等查询 - 查询 C(Lx) 是否等同于 C(Ly)
   格式：<query_cover_eq>Lx,Ly</query_cover_eq>
   回答："是"或"否"

**你的目标：**
1. 归纳出物料流转通道开启规律 R'（用自然语言或形式化描述，需与所有查询反馈一致）
2. 判定是否存在下游流转范围覆盖所有工站的“初始投料工站”；若存在则给出其名称，若不存在则明确声明
3. 提供两条可验证的预测

**最终答案格式：**
<answer>
rule: [你归纳的规律描述]
global_node: [工站名称如 L3，或 "不存在"]
prediction1: [预测类型]=[预测内容]
prediction2: [预测类型]=[预测内容]
</answer>

预测类型包括：
- edge:Lx,Ly=[是/否] （预测是否存在单向流转通道 Lx→Ly）
- all:Lx=[是/否] （预测 C(Lx) 是否覆盖全流水线）
- count:Lx=[整数] （预测 |C(Lx)| 的值）

示例：
<answer>
rule: 如果上游工站工艺与下游工站工艺有交集，则存在物料流转通道
global_node: L2
prediction1: edge:L1,L3=是
prediction2: count:L4=5
</answer>
"""

    contextualized_rule_en_4 = """\
[Industrial Scenario]
Welcome to the "Production Pipeline Network" control system.

The current facility contains {n} production stations, named L1, L2, ..., L{n}.
Each station possesses specific process attributes, represented as a subset of the letter set {{A, B, C, D, E, F}}, containing 1 to 3 attributes.

The one-way material flow channels between stations are determined by a globally consistent but hidden operational rule R: for any two stations Li and Lj, if R(attributes_i, attributes_j) is true, a direct material flow channel Li→Lj exists. This rule R remains constant throughout the pipeline planning.

**Initial Public Information:**
Number of stations: {n}
Station attributes: {labels}

**Downstream Routing Coverage Definition:**
The downstream routing coverage C(Lx) from station Lx is the set of all stations reachable by continuous processing along the one-way channels (including the starting station itself).

**Available Query Types (use as few queries as possible):**

1. Count Query - Query the size of the downstream routing coverage from a station
   Format: <query_count>Lx</query_count>
   Answer: An integer representing |C(Lx)|

2. All Query - Query whether a station's downstream routing coverage covers all stations (max 2 uses per game)
   Format: <query_all>Lx</query_all>
   Answer: "Yes" or "No"

3. One-hop Neighbors Query - Query direct downstream stations receiving materials from a station (max 2 uses per game)
   Format: <query_neighbors1>Lx</query_neighbors1>
   Answer: Lexicographically sorted station names like "L1,L3,L5" or empty list "[]"

4. Two-hop Delta Query - Query stations reachable with exactly one intermediate processing step but not directly (max 2 uses per game)
   Format: <query_delta2>Lx</query_delta2>
   Answer: Lexicographically sorted station names or empty list "[]"

5. Cover-GE Query - Query whether C(Lx) completely covers C(Ly)
   Format: <query_cover_ge>Lx,Ly</query_cover_ge>
   Answer: "Yes" or "No"

6. Cover-EQ Query - Query whether C(Lx) is identical to C(Ly)
   Format: <query_cover_eq>Lx,Ly</query_cover_eq>
   Answer: "Yes" or "No"

**Your Goal:**
1. Deduce the material flow channel activation rule R' (in natural language or formal description, consistent with all query feedback)
2. Determine whether there exists a "primary feeding station" whose downstream routing coverage encompasses all stations; if so, provide its name; otherwise, explicitly state "none"
3. Provide two verifiable predictions

**Final Answer Format:**
<answer>
rule: [your deduced rule description]
global_node: [station name like L3, or "none"]
prediction1: [prediction type]=[prediction content]
prediction2: [prediction type]=[prediction content]
</answer>

Prediction types include:
- edge:Lx,Ly=[Yes/No] (predict whether a material flow channel Lx→Ly exists)
- all:Lx=[Yes/No] (predict whether C(Lx) covers the entire pipeline)
- count:Lx=[integer] (predict the value of |C(Lx)|)

Example:
<answer>
rule: A material flow channel exists if the upstream station's attributes intersect with the downstream station's attributes
global_node: L2
prediction1: edge:L1,L3=Yes
prediction2: count:L4=5
</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入“案件移送管辖网络”推演系统。

当前辖区包含 {n} 个司法机构，命名为 L1, L2, ..., L{n}。
每个机构具备特定的管辖权属性，表示为属性集合 {{A, B, C, D, E, F}} 的子集，每个机构拥有 1 到 3 种管辖权。

机构间的单向案件移送机制由一个全局一致但保密的法定移送规则 R 决定：对于任意两个司法机构 Li 和 Lj，如果 R(属性i, 属性j) 为真，则存在一条 Li→Lj 的移送机制。法定规则 R 在整个司法管辖网络中保持不变。

**初始公开信息：**
机构数量：{n}
各机构管辖权属性：{labels}

**移送辐射范围定义：**
从某个机构 Lx 立案出发，通过不断启动案件移送机制所能涉及的所有司法机构集合（包含首发机构本身），记为移送辐射范围 C(Lx)。

**可用查询类型（请尽可能少地使用查询次数）：**

1. 计数查询 - 查询从某机构出发的移送辐射范围规模
   格式：<query_count>Lx</query_count>
   回答：一个整数，表示 |C(Lx)|

2. 全覆盖查询 - 查询某机构的移送辐射范围是否波及所有机构（每局最多使用 2 次）
   格式：<query_all>Lx</query_all>
   回答："是"或"否"

3. 一跳邻居查询 - 查询某机构可直接移送案件的接收机构（每局最多使用 2 次）
   格式：<query_neighbors1>Lx</query_neighbors1>
   回答：按字典序排列的机构名称列表，如 "L1,L3,L5" 或空列表 "[]"

4. 两跳增量查询 - 查询需经过一次中转协调（两跳）可达但直接移送无法到达的机构（每局最多使用 2 次）
   格式：<query_delta2>Lx</query_delta2>
   回答：按字典序排列的机构名称列表，或空列表 "[]"

5. 包含查询 - 查询 C(Lx) 是否完全覆盖 C(Ly)
   格式：<query_cover_ge>Lx,Ly</query_cover_ge>
   回答："是"或"否"

6. 相等查询 - 查询 C(Lx) 是否等同于 C(Ly)
   格式：<query_cover_eq>Lx,Ly</query_cover_eq>
   回答："是"或"否"

**你的目标：**
1. 归纳出案件移送管辖规则 R'（用自然语言或形式化描述，需与所有查询反馈一致）
2. 判定是否存在移送辐射范围波及所有机构的“统一立案机构”；若存在则给出其名称，若不存在则明确声明
3. 提供两条可验证的预测

**最终答案格式：**
<answer>
rule: [你归纳的规律描述]
global_node: [机构名称如 L3，或 "不存在"]
prediction1: [预测类型]=[预测内容]
prediction2: [预测类型]=[预测内容]
</answer>

预测类型包括：
- edge:Lx,Ly=[是/否] （预测是否存在案件移送机制 Lx→Ly）
- all:Lx=[是/否] （预测 C(Lx) 是否覆盖整个网络）
- count:Lx=[整数] （预测 |C(Lx)| 的值）

示例：
<answer>
rule: 如果移出机构管辖权与接收机构管辖权有交集，则存在案件移送机制
global_node: L2
prediction1: edge:L1,L3=是
prediction2: count:L4=5
</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Case Jurisdiction Transfer Network" deduction system.

The current jurisdiction encompasses {n} judicial entities, named L1, L2, ..., L{n}.
Each entity possesses specific jurisdiction attributes, represented as a subset of the letter set {{A, B, C, D, E, F}}, containing 1 to 3 attributes.

The one-way case transfer mechanisms between entities are determined by a globally consistent but confidential statutory transfer rule R: for any two entities Li and Lj, if R(attributes_i, attributes_j) is true, a direct transfer mechanism Li→Lj exists. This statutory rule R remains constant throughout the entire jurisdiction network.

**Initial Public Information:**
Number of entities: {n}
Entity jurisdiction attributes: {labels}

**Transfer Jurisdiction Coverage Definition:**
The transfer jurisdiction coverage C(Lx) from entity Lx is the set of all judicial entities that can be progressively involved through the transfer mechanism (including the filing entity itself).

**Available Query Types (use as few queries as possible):**

1. Count Query - Query the size of the transfer jurisdiction coverage from an entity
   Format: <query_count>Lx</query_count>
   Answer: An integer representing |C(Lx)|

2. All Query - Query whether an entity's transfer jurisdiction coverage involves all entities (max 2 uses per game)
   Format: <query_all>Lx</query_all>
   Answer: "Yes" or "No"

3. One-hop Neighbors Query - Query direct receiving entities from a transferring entity (max 2 uses per game)
   Format: <query_neighbors1>Lx</query_neighbors1>
   Answer: Lexicographically sorted entity names like "L1,L3,L5" or empty list "[]"

4. Two-hop Delta Query - Query entities reachable with exactly one intermediate coordination but not directly (max 2 uses per game)
   Format: <query_delta2>Lx</query_delta2>
   Answer: Lexicographically sorted entity names or empty list "[]"

5. Cover-GE Query - Query whether C(Lx) completely covers C(Ly)
   Format: <query_cover_ge>Lx,Ly</query_cover_ge>
   Answer: "Yes" or "No"

6. Cover-EQ Query - Query whether C(Lx) is identical to C(Ly)
   Format: <query_cover_eq>Lx,Ly</query_cover_eq>
   Answer: "Yes" or "No"

**Your Goal:**
1. Deduce the case transfer statutory rule R' (in natural language or formal description, consistent with all query feedback)
2. Determine whether there exists a "central filing entity" whose transfer jurisdiction coverage involves all entities; if so, provide its name; otherwise, explicitly state "none"
3. Provide two verifiable predictions

**Final Answer Format:**
<answer>
rule: [your deduced rule description]
global_node: [entity name like L3, or "none"]
prediction1: [prediction type]=[prediction content]
prediction2: [prediction type]=[prediction content]
</answer>

Prediction types include:
- edge:Lx,Ly=[Yes/No] (predict whether a case transfer mechanism Lx→Ly exists)
- all:Lx=[Yes/No] (predict whether C(Lx) covers the entire network)
- count:Lx=[integer] (predict the value of |C(Lx)|)

Example:
<answer>
rule: A case transfer mechanism exists if the transferring entity's attributes intersect with the receiving entity's attributes
global_node: L2
prediction1: edge:L1,L3=Yes
prediction2: count:L4=5
</answer>
"""

    tags = ["answer", "query_count", "query_all", "query_neighbors1", "query_delta2", "query_cover_ge", "query_cover_eq"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "labels": "L1:{A}, L2:{B}, L3:{A,B}, L4:{C}, L5:{A,C}, L6:{D}, L7:{A,D}, L8:{E}",
                "label_map": {
                    "L1": {"A"},
                    "L2": {"B"},
                    "L3": {"A", "B"},
                    "L4": {"C"},
                    "L5": {"A", "C"},
                    "L6": {"D"},
                    "L7": {"A", "D"},
                    "L8": {"E"},
                },
                "rule_desc": "如果源节点标签包含字母A，则存在从源到目标的边",
                "rule_func": lambda src, tgt: "A" in src,
                "global_node": "L1",
            },
            2: {
                "n": 9,
                "labels": "L1:{A}, L2:{B}, L3:{A,B}, L4:{C}, L5:{B,C}, L6:{D}, L7:{C,D}, L8:{A,C}, L9:{A,E}",
                "label_map": {
                    "L1": {"A"},
                    "L2": {"B"},
                    "L3": {"A", "B"},
                    "L4": {"C"},
                    "L5": {"B", "C"},
                    "L6": {"D"},
                    "L7": {"C", "D"},
                    "L8": {"A", "C"},
                    "L9": {"A", "E"},
                },
                "rule_desc": "如果源节点标签与目标节点标签有交集（共同字母），则存在边",
                "rule_func": lambda src, tgt: len(src & tgt) > 0,
                "global_node": "L3",
            },
            3: {
                "n": 10,
                "labels": "L1:{A}, L2:{B,C}, L3:{A}, L4:{D,E}, L5:{A,B}, L6:{C}, L7:{D}, L8:{A,B,C}, L9:{E,F}, L10:{F}",
                "label_map": {
                    "L1": {"A"},
                    "L2": {"B", "C"},
                    "L3": {"A"},
                    "L4": {"D", "E"},
                    "L5": {"A", "B"},
                    "L6": {"C"},
                    "L7": {"D"},
                    "L8": {"A", "B", "C"},
                    "L9": {"E", "F"},
                    "L10": {"F"},
                },
                "rule_desc": "如果源节点标签的字母数小于等于目标节点标签的字母数，则存在边",
                "rule_func": lambda src, tgt: len(src) <= len(tgt),
                "global_node": "L1",
            },
            4: {
                "n": 11,
                "labels": "L1:{A,B}, L2:{C}, L3:{A,D}, L4:{F}, L5:{B,C}, L6:{A}, L7:{E}, L8:{A,F}, L9:{D}, L10:{A,E}, L11:{B}",
                "label_map": {
                    "L1": {"A", "B"},
                    "L2": {"C"},
                    "L3": {"A", "D"},
                    "L4": {"F"},
                    "L5": {"B", "C"},
                    "L6": {"A"},
                    "L7": {"E"},
                    "L8": {"A", "F"},
                    "L9": {"D"},
                    "L10": {"A", "E"},
                    "L11": {"B"},
                },
                "rule_desc": "如果源节点包含字母A且目标节点不包含字母F，则存在边",
                "rule_func": lambda src, tgt: ("A" in src) and ("F" not in tgt),
                "global_node": "L6",
            },
            5: {
                "n": 12,
                "labels": "L1:{A}, L2:{A,B}, L3:{A,B,C}, L4:{B}, L5:{B,C}, L6:{C}, L7:{D}, L8:{D,E}, L9:{E}, L10:{A,D}, L11:{B,E}, L12:{C,F}",
                "label_map": {
                    "L1": {"A"},
                    "L2": {"A", "B"},
                    "L3": {"A", "B", "C"},
                    "L4": {"B"},
                    "L5": {"B", "C"},
                    "L6": {"C"},
                    "L7": {"D"},
                    "L8": {"D", "E"},
                    "L9": {"E"},
                    "L10": {"A", "D"},
                    "L11": {"B", "E"},
                    "L12": {"C", "F"},
                },
                "rule_desc": "如果源节点标签是目标节点标签的子集，则存在边",
                "rule_func": lambda src, tgt: src.issubset(tgt),
                "global_node": "L1",
            },
        },
        "en": {
            1: {
                "n": 8,
                "labels": "L1:{A}, L2:{B}, L3:{A,B}, L4:{C}, L5:{A,C}, L6:{D}, L7:{A,D}, L8:{E}",
                "label_map": {
                    "L1": {"A"},
                    "L2": {"B"},
                    "L3": {"A", "B"},
                    "L4": {"C"},
                    "L5": {"A", "C"},
                    "L6": {"D"},
                    "L7": {"A", "D"},
                    "L8": {"E"},
                },
                "rule_desc": "An edge exists from source to target if source label contains letter A",
                "rule_func": lambda src, tgt: "A" in src,
                "global_node": "L1",
            },
            2: {
                "n": 9,
                "labels": "L1:{A}, L2:{B}, L3:{A,B}, L4:{C}, L5:{B,C}, L6:{D}, L7:{C,D}, L8:{A,C}, L9:{A,E}",
                "label_map": {
                    "L1": {"A"},
                    "L2": {"B"},
                    "L3": {"A", "B"},
                    "L4": {"C"},
                    "L5": {"B", "C"},
                    "L6": {"D"},
                    "L7": {"C", "D"},
                    "L8": {"A", "C"},
                    "L9": {"A", "E"},
                },
                "rule_desc": "An edge exists if source and target labels have non-empty intersection",
                "rule_func": lambda src, tgt: len(src & tgt) > 0,
                "global_node": "L3",
            },
            3: {
                "n": 10,
                "labels": "L1:{A}, L2:{B,C}, L3:{A}, L4:{D,E}, L5:{A,B}, L6:{C}, L7:{D}, L8:{A,B,C}, L9:{E,F}, L10:{F}",
                "label_map": {
                    "L1": {"A"},
                    "L2": {"B", "C"},
                    "L3": {"A"},
                    "L4": {"D", "E"},
                    "L5": {"A", "B"},
                    "L6": {"C"},
                    "L7": {"D"},
                    "L8": {"A", "B", "C"},
                    "L9": {"E", "F"},
                    "L10": {"F"},
                },
                "rule_desc": "An edge exists if source label size is less than or equal to target label size",
                "rule_func": lambda src, tgt: len(src) <= len(tgt),
                "global_node": "L1",
            },
            4: {
                "n": 11,
                "labels": "L1:{A,B}, L2:{C}, L3:{A,D}, L4:{F}, L5:{B,C}, L6:{A}, L7:{E}, L8:{A,F}, L9:{D}, L10:{A,E}, L11:{B}",
                "label_map": {
                    "L1": {"A", "B"},
                    "L2": {"C"},
                    "L3": {"A", "D"},
                    "L4": {"F"},
                    "L5": {"B", "C"},
                    "L6": {"A"},
                    "L7": {"E"},
                    "L8": {"A", "F"},
                    "L9": {"D"},
                    "L10": {"A", "E"},
                    "L11": {"B"},
                },
                "rule_desc": "An edge exists if source contains A and target does not contain F",
                "rule_func": lambda src, tgt: ("A" in src) and ("F" not in tgt),
                "global_node": "L6",
            },
            5: {
                "n": 12,
                "labels": "L1:{A}, L2:{A,B}, L3:{A,B,C}, L4:{B}, L5:{B,C}, L6:{C}, L7:{D}, L8:{D,E}, L9:{E}, L10:{A,D}, L11:{B,E}, L12:{C,F}",
                "label_map": {
                    "L1": {"A"},
                    "L2": {"A", "B"},
                    "L3": {"A", "B", "C"},
                    "L4": {"B"},
                    "L5": {"B", "C"},
                    "L6": {"C"},
                    "L7": {"D"},
                    "L8": {"D", "E"},
                    "L9": {"E"},
                    "L10": {"A", "D"},
                    "L11": {"B", "E"},
                    "L12": {"C", "F"},
                },
                "rule_desc": "An edge exists if source label is a subset of target label",
                "rule_func": lambda src, tgt: src.issubset(tgt),
                "global_node": "L1",
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
        self._game_info["labels"] = cfg["labels"]
        
        self.label_map = cfg["label_map"]
        self.rule_func = cfg["rule_func"]
        self.rule_desc = cfg["rule_desc"]
        self.expected_global_node = cfg["global_node"]
        
        self.graph = {node: [] for node in self.label_map.keys()}
        for src in self.label_map:
            for tgt in self.label_map:
                if self.rule_func(self.label_map[src], self.label_map[tgt]):
                    self.graph[src].append(tgt)
        
        self.closures = {}
        for node in self.label_map:
            self.closures[node] = self._compute_closure(node)
        
        self.query_limits = {
            "query_all": 2,
            "query_neighbors1": 2,
            "query_delta2": 2,
        }
        self.query_counts = {
            "query_all": 0,
            "query_neighbors1": 0,
            "query_delta2": 0,
        }

    def _compute_closure(self, start_node):
        visited = set()
        queue = [start_node]
        visited.add(start_node)
        
        while queue:
            current = queue.pop(0)
            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return visited

    def _get_one_hop_neighbors(self, node):
        return set(self.graph[node])

    def _get_two_hop_delta(self, node):
        one_hop = self._get_one_hop_neighbors(node)
        two_hop = set()
        
        for neighbor in one_hop:
            two_hop.update(self.graph[neighbor])
        
        delta = two_hop - one_hop - {node}
        return delta

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"]
            lines = [line.strip() for line in raw_ans.split("\n") if line.strip()]
            
            ans_dict = {}
            for line in lines:
                if ":" in line:
                    key, value = line.split(":", 1)
                    ans_dict[key.strip()] = value.strip()
            
            if "rule" not in ans_dict or "global_node" not in ans_dict:
                return False
            if "prediction1" not in ans_dict or "prediction2" not in ans_dict:
                return False
            
            claimed_global = ans_dict["global_node"]
            lang = self.config.language
            
            if lang == "zh":
                none_keywords = ["不存在", "无", "没有"]
            else:
                none_keywords = ["none", "no", "does not exist", "doesn't exist"]
            
            claims_no_global = any(kw in claimed_global.lower() for kw in none_keywords)
            
            actual_has_global = False
            for node in self.label_map:
                if len(self.closures[node]) == self._game_info["n"]:
                    actual_has_global = True
                    if not claims_no_global and claimed_global == node:
                        global_correct = True
                        break
            else:
                global_correct = claims_no_global and not actual_has_global
            
            if not global_correct:
                return False
            
            pred1 = ans_dict["prediction1"]
            pred2 = ans_dict["prediction2"]
            
            if not self._verify_prediction(pred1):
                return False
            if not self._verify_prediction(pred2):
                return False
            
            return True
            
        except Exception as e:
            return False

    def _verify_prediction(self, pred_str):
        try:
            lang = self.config.language
            yes_str = "是" if lang == "zh" else "yes"
            no_str = "否" if lang == "zh" else "no"
            
            if pred_str.startswith("edge:"):
                rest = pred_str[5:]
                nodes_part, answer = rest.rsplit("=", 1)
                answer = answer.strip().lower()
                src, tgt = [x.strip() for x in nodes_part.split(",")]
                
                actual = tgt in self.graph[src]
                expected = (answer == yes_str.lower())
                return actual == expected
                
            elif pred_str.startswith("all:"):
                rest = pred_str[4:]
                node, answer = rest.rsplit("=", 1)
                node = node.strip()
                answer = answer.strip().lower()
                
                actual = (len(self.closures[node]) == self._game_info["n"])
                expected = (answer == yes_str.lower())
                return actual == expected
                
            elif pred_str.startswith("count:"):
                rest = pred_str[6:]
                node, count_str = rest.rsplit("=", 1)
                node = node.strip()
                expected_count = int(count_str.strip())
                
                actual_count = len(self.closures[node])
                return actual_count == expected_count
            
            return False
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        yes_str = "是" if lang == "zh" else "Yes"
        no_str = "否" if lang == "zh" else "No"
        error_limit = "错误：该查询类型已达使用次数上限。" if lang == "zh" else "Error: Query type limit reached."
        error_format = "错误：查询格式无效。" if lang == "zh" else "Error: Invalid query format."
        
        try:
            if "query_count" in parsed_info:
                node = parsed_info["query_count"].strip()
                if node not in self.label_map:
                    return error_format
                return str(len(self.closures[node]))
            
            elif "query_all" in parsed_info:
                if self.query_counts["query_all"] >= self.query_limits["query_all"]:
                    return error_limit
                self.query_counts["query_all"] += 1
                
                node = parsed_info["query_all"].strip()
                if node not in self.label_map:
                    return error_format
                is_all = (len(self.closures[node]) == self._game_info["n"])
                return yes_str if is_all else no_str
            
            elif "query_neighbors1" in parsed_info:
                if self.query_counts["query_neighbors1"] >= self.query_limits["query_neighbors1"]:
                    return error_limit
                self.query_counts["query_neighbors1"] += 1
                
                node = parsed_info["query_neighbors1"].strip()
                if node not in self.label_map:
                    return error_format
                neighbors = sorted(self.graph[node])
                return ",".join(neighbors) if neighbors else "[]"
            
            elif "query_delta2" in parsed_info:
                if self.query_counts["query_delta2"] >= self.query_limits["query_delta2"]:
                    return error_limit
                self.query_counts["query_delta2"] += 1
                
                node = parsed_info["query_delta2"].strip()
                if node not in self.label_map:
                    return error_format
                delta = sorted(self._get_two_hop_delta(node))
                return ",".join(delta) if delta else "[]"
            
            elif "query_cover_ge" in parsed_info:
                raw = parsed_info["query_cover_ge"]
                node1, node2 = [x.strip() for x in raw.split(",")]
                if node1 not in self.label_map or node2 not in self.label_map:
                    return error_format
                is_cover = self.closures[node2].issubset(self.closures[node1])
                return yes_str if is_cover else no_str
            
            elif "query_cover_eq" in parsed_info:
                raw = parsed_info["query_cover_eq"]
                node1, node2 = [x.strip() for x in raw.split(",")]
                if node1 not in self.label_map or node2 not in self.label_map:
                    return error_format
                is_equal = (self.closures[node1] == self.closures[node2])
                return yes_str if is_equal else no_str
            
            else:
                return error_format
                
        except Exception as e:
            return error_format

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        lang = self.config.language
        yes_str = "是" if lang == "zh" else "Yes"
        no_str = "否" if lang == "zh" else "No"
        
        nodes = sorted(self.label_map.keys())
        
        for node in nodes:
            ans_count = str(len(self.closures[node]))
            results.append({
                "query": f"<query_count>{node}</query_count>",
                "answer": ans_count
            })
            
            is_all = (len(self.closures[node]) == self._game_info["n"])
            results.append({
                "query": f"<query_all>{node}</query_all>",
                "answer": yes_str if is_all else no_str
            })
            
            neighbors = sorted(self.graph[node])
            ans_neigh = ",".join(neighbors) if neighbors else "[]"
            results.append({
                "query": f"<query_neighbors1>{node}</query_neighbors1>",
                "answer": ans_neigh
            })
            
            delta = sorted(self._get_two_hop_delta(node))
            ans_delta = ",".join(delta) if delta else "[]"
            results.append({
                "query": f"<query_delta2>{node}</query_delta2>",
                "answer": ans_delta
            })
            
            for node2 in nodes:
                is_cover = self.closures[node2].issubset(self.closures[node])
                results.append({
                    "query": f"<query_cover_ge>{node},{node2}</query_cover_ge>",
                    "answer": yes_str if is_cover else no_str
                })
                
                is_equal = (self.closures[node] == self.closures[node2])
                results.append({
                    "query": f"<query_cover_eq>{node},{node2}</query_cover_eq>",
                    "answer": yes_str if is_equal else no_str
                })
                
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        c_lower = correct.lower()
        if c_lower == "yes":
            if correct.isupper(): return "NO"
            if correct.islower(): return "no"
            return "No"
        if c_lower == "no":
            if correct.isupper(): return "YES"
            if correct.islower(): return "yes"
            return "Yes"
        if correct == "是": return "否"
        if correct == "否": return "是"
        
        return correct + "_WRONG"