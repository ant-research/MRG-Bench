from .base import Game
import re

class GraphBipartitionGame(Game):

    game_rule_zh = """\
我们来玩一个"图二分类推理"游戏，规则如下：

游戏设定了一个无向简单图 G，包含 {n} 个顶点（编号 1 到 {n}）和若干条边（无自环、无重边）。
边的集合为：{edges}

你的目标是将所有顶点分为两个不交的子集 L 和 R（L 和 R 的并集为所有顶点，交集为空）。

然而，我已秘密选择了以下四种模式之一，它决定了什么样的二分类是合法的：
- 模式 A（边-相对）：对于图中的每条边 (u,v)，要求 u 和 v 必须属于不同侧；对于非边则无要求。
- 模式 B（边-相同）：对于图中的每条边 (u,v)，要求 u 和 v 必须属于同一侧；对于非边则无要求。
- 模式 C（非边-相对）：对于图中的每对非边 (u,v)，要求 u 和 v 必须属于不同侧；对于边则无要求。
- 模式 D（非边-相同）：对于图中的每对非边 (u,v)，要求 u 和 v 必须属于同一侧；对于边则无要求。

你可以通过以下方式与我交互（每次只能使用一种查询）：

1. **局部关系查询**：试探性询问两个顶点按某种关系摆放是否满足当前模式。
   - 关系类型：同侧 或 对侧
   - 我会回答：满足 或 冲突

2. **全局方案校验**：提交一个完整的二分类方案，我会检查是否全局满足当前模式。
   - 若满足，返回：全局满足
   - 若冲突，返回：发现冲突，并给出一个冲突对及其关系

3. **模式宣告**：当你收集足够证据后，可以宣告你推断出的模式。
   - 需要提供至少两条先前的试探记录作为证据：一条针对边对，一条针对非边对
   - 证据格式：边对=(x,y),关系=同侧/对侧,结果=满足/冲突; 非边对=(a,b),关系=同侧/对侧,结果=满足/冲突
   - 我会验证证据是否能唯一指向该模式

4. **不可行证据**（仅在模式为 A 或 C 且图不可二分时使用）：
   - 若模式为 A：提交图中的一个奇环（顶点数为奇数的环，相邻顶点间均有边）
   - 若模式为 C：提交补图中的一个奇环（相邻顶点间均无边）
   - 环的格式：顶点序列，例如 1,2,3,1

5. **最终方案提交**：在成功判定模式后，提交模式和对应的二分类方案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 局部关系查询（例如询问顶点 1 和 2 是否可以同侧）：
<query_local>1,2,同侧</query_local>

- 全局方案校验（例如 L=1,2 和 R=3,4,5）：
<query_global>L=1,2;R=3,4,5</query_global>

- 模式宣告（例如宣告模式 A，并提供证据）：
<declare_mode>mode=A, evidence=边对=(1,2),关系=对侧,结果=满足; 非边对=(1,3),关系=对侧,结果=冲突</declare_mode>

- 不可行证据（例如提交模式 A 的奇环证明）：
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- 最终方案提交（例如模式 A，L=1,3 和 R=2,4）：
<answer>mode=A, L=1,3, R=2,4</answer>

注意：查询要尽可能少，以最高效的方式推理出答案。
"""

    game_rule_en = """\
Let's play a "Graph Bipartition Reasoning" game. Here are the rules:

A simple undirected graph G is given, containing {n} vertices (numbered 1 to {n}) and several edges (no self-loops, no multiple edges).
The edge set is: {edges}

Your goal is to partition all vertices into two disjoint subsets L and R (L union R equals all vertices, L intersect R is empty).

However, I have secretly chosen one of the following four modes, which determines what bipartition is valid:
- Mode A (Edge-Opposite): For each edge (u,v) in the graph, u and v must be on different sides; non-edges have no requirement.
- Mode B (Edge-Same): For each edge (u,v) in the graph, u and v must be on the same side; non-edges have no requirement.
- Mode C (NonEdge-Opposite): For each pair of non-edges (u,v), u and v must be on different sides; edges have no requirement.
- Mode D (NonEdge-Same): For each pair of non-edges (u,v), u and v must be on the same side; edges have no requirement.

You can interact with me in the following ways (one query type at a time):

1. **Local Relation Query**: Test whether two vertices can be placed with a certain relation under the current mode.
   - Relation types: same or opposite
   - I will answer: satisfied or conflict

2. **Global Scheme Verification**: Submit a complete bipartition scheme, and I will check if it globally satisfies the current mode.
   - If satisfied, return: globally satisfied
   - If conflict, return: conflict found, with one conflicting pair and its relation

3. **Mode Declaration**: When you have enough evidence, declare the mode you inferred.
   - Provide at least two prior test records as evidence: one for an edge pair, one for a non-edge pair
   - Evidence format: edge=(x,y),relation=same/opposite,result=satisfied/conflict; nonedge=(a,b),relation=same/opposite,result=satisfied/conflict
   - I will verify if the evidence uniquely points to that mode

4. **Impossibility Proof** (only when mode is A or C and the graph is not bipartite):
   - If mode A: Submit an odd cycle in the graph (odd number of vertices, adjacent vertices connected by edges)
   - If mode C: Submit an odd cycle in the complement graph (adjacent vertices not connected by edges)
   - Cycle format: vertex sequence, e.g., 1,2,3,1

5. **Final Scheme Submission**: After successfully determining the mode, submit the mode and the corresponding bipartition.

Each query can only contain one tag, using the following XML format:

- Local relation query (e.g., asking if vertices 1 and 2 can be on the same side):
<query_local>1,2,same</query_local>

- Global scheme verification (e.g., L=1,2 and R=3,4,5):
<query_global>L=1,2;R=3,4,5</query_global>

- Mode declaration (e.g., declare mode A with evidence):
<declare_mode>mode=A, evidence=edge=(1,2),relation=opposite,result=satisfied; nonedge=(1,3),relation=opposite,result=conflict</declare_mode>

- Impossibility proof (e.g., submit an odd cycle for mode A):
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- Final scheme submission (e.g., mode A, L=1,3 and R=2,4):
<answer>mode=A, L=1,3, R=2,4</answer>

Note: Use as few queries as possible to efficiently deduce the answer.
"""

    contextualized_rule_zh_1 = """\
我们来操作"路网管控区划分"规划系统，规则如下：

系统导入了一个交通路网 G，包含 {n} 个关键路口（编号 1 到 {n}）和若干条直达快速路（无自环、无重边）。
快速路（对应逻辑中的边）的集合为：{edges}

你的目标是将所有路口划分为两个不交的交通管控大区 L 和 R（L 和 R 的并集为所有路口，交集为空）。

然而，系统秘密激活了以下四种调控模式之一，它决定了什么样的划分是合法的：
- 模式 A（连线-分设）：对于存在快速路相连的每对路口 (u,v)，要求 u 和 v 必须分属不同侧（即不同大区）；对于无快速路的路口则无要求。
- 模式 B（连线-同组）：对于存在快速路相连的每对路口 (u,v)，要求 u 和 v 必须属于同侧（即同一大区）以实现绿波协同；对于无快速路的路口则无要求。
- 模式 C（无连线-分设）：对于无快速路直达的每对路口 (u,v)，要求 u 和 v 必须分属不同侧；对于有快速路的路口则无要求。
- 模式 D（无连线-同组）：对于无快速路直达的每对路口 (u,v)，要求 u 和 v 必须属于同侧；对于有快速路的路口则无要求。

你可以通过以下方式与系统交互（每次只能使用一种查询）：

1. **局部关系查询**：试探性询问两个路口按某种关系摆放是否满足当前模式。
   - 关系类型：同侧 或 对侧
   - 系统会回答：满足 或 冲突

2. **全局方案校验**：提交一个完整的管控区划分方案，系统会检查是否全局满足当前模式。
   - 若满足，返回：全局满足
   - 若冲突，返回：发现冲突，并给出一个冲突路口对及其划分关系

3. **模式宣告**：当你收集足够证据后，可以宣告你推断出的系统模式。
   - 需要提供至少两条先前的试探记录作为证据：一条针对存在快速路的路口对（指令中严格使用"边对"表示），一条针对无快速路的路口对（指令中严格使用"非边对"表示）
   - 证据格式：边对=(x,y),关系=同侧/对侧,结果=满足/冲突; 非边对=(a,b),关系=同侧/对侧,结果=满足/冲突
   - 系统会验证证据是否能唯一指向该模式

4. **不可行证据**（仅在模式为 A 或 C 且由于路网拓扑导致无法合法划分时使用）：
   - 若模式为 A：提交路网中的一个奇环（由奇数个路口组成的环线，相邻路口间均有快速路）
   - 若模式为 C：提交补图中的一个奇环（相邻路口间均无快速路）
   - 环的格式：路口序列，例如 1,2,3,1

5. **最终方案提交**：在成功判定模式后，提交模式和对应的划分方案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 局部关系查询（例如询问路口 1 和 2 是否可以同侧）：
<query_local>1,2,同侧</query_local>

- 全局方案校验（例如管控区 L 包含路口 1,2，R 包含 3,4,5）：
<query_global>L=1,2;R=3,4,5</query_global>

- 模式宣告（例如宣告模式 A，并提供证据）：
<declare_mode>mode=A, evidence=边对=(1,2),关系=对侧,结果=满足; 非边对=(1,3),关系=对侧,结果=冲突</declare_mode>

- 不可行证据（例如提交模式 A 的奇环拓扑证明）：
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- 最终方案提交（例如模式 A，L=1,3 和 R=2,4）：
<answer>mode=A, L=1,3, R=2,4</answer>

注意：查询要尽可能少，以最高效的方式推理出答案。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's operate the "Road Network Control Zone Partitioning" system. Here are the rules:

The system has loaded a traffic road network G, containing {n} key intersections/hubs (numbered 1 to {n}) and several direct expressways (no self-loops, no multiple expressways).
The set of expressways (representing edges) is: {edges}

Your goal is to partition all hubs into two disjoint traffic control zones, L and R (L union R equals all hubs, L intersect R is empty).

However, the system has secretly activated one of the following four regulation modes, which determines what partition is valid:
- Mode A (Connected-Opposite): For each pair of hubs (u,v) connected by an expressway, u and v must be on different sides (different zones); unconnected hubs have no requirement.
- Mode B (Connected-Same): For each pair of hubs (u,v) connected by an expressway, u and v must be on the same side (same zone) for green wave coordination; unconnected hubs have no requirement.
- Mode C (Unconnected-Opposite): For each pair of unconnected hubs (u,v), u and v must be on different sides; connected hubs have no requirement.
- Mode D (Unconnected-Same): For each pair of unconnected hubs (u,v), u and v must be on the same side; connected hubs have no requirement.

You can interact with the system in the following ways (one query type at a time):

1. **Local Relation Query**: Test whether two hubs can be assigned with a certain relation under the current mode.
   - Relation types: same or opposite
   - The system will answer: satisfied or conflict

2. **Global Scheme Verification**: Submit a complete zone partition scheme, and the system will check if it globally satisfies the current mode.
   - If satisfied, return: globally satisfied
   - If conflict, return: conflict found, with one conflicting hub pair and its assigned relation

3. **Mode Declaration**: When you have enough evidence, declare the regulation mode you inferred.
   - Provide at least two prior test records as evidence: one for a connected hub pair (must strictly use the keyword "edge"), one for an unconnected hub pair (must strictly use the keyword "nonedge")
   - Evidence format: edge=(x,y),relation=same/opposite,result=satisfied/conflict; nonedge=(a,b),relation=same/opposite,result=satisfied/conflict
   - The system will verify if the evidence uniquely points to that mode

4. **Impossibility Proof** (only when mode is A or C and the network cannot be validly partitioned):
   - If mode A: Submit an odd cycle in the network (odd number of hubs, adjacent hubs connected by expressways)
   - If mode C: Submit an odd cycle in the complement network (adjacent hubs not connected by expressways)
   - Cycle format: hub sequence, e.g., 1,2,3,1

5. **Final Scheme Submission**: After successfully determining the mode, submit the mode and the corresponding partition.

Each query can only contain one tag, using the following XML format:

- Local relation query (e.g., asking if hubs 1 and 2 can be on the same side):
<query_local>1,2,same</query_local>

- Global scheme verification (e.g., L=1,2 and R=3,4,5):
<query_global>L=1,2;R=3,4,5</query_global>

- Mode declaration (e.g., declare mode A with evidence):
<declare_mode>mode=A, evidence=edge=(1,2),relation=opposite,result=satisfied; nonedge=(1,3),relation=opposite,result=conflict</declare_mode>

- Impossibility proof (e.g., submit an odd cycle topology proof for mode A):
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- Final scheme submission (e.g., mode A, L=1,3 and R=2,4):
<answer>mode=A, L=1,3, R=2,4</answer>

Note: Use as few queries as possible to efficiently deduce the answer.
"""

    contextualized_rule_zh_2 = """\
我们来操作"联合用药配方筛查"系统，规则如下：

系统导入了一个候选药物相互作用图 G，包含 {n} 个药物分子（编号 1 到 {n}）和若干已知交叉反应关系（无自环、无重边）。
交叉反应关系（对应逻辑中的边）的集合为：{edges}

你的目标是将所有药物分子分配到两个不交的治疗方案组 L 和 R 中（L 和 R 的并集为所有药物分子，交集为空）。

然而，系统秘密激活了以下四种筛选模式之一，它决定了什么样的药物组合是合法的：
- 模式 A（反应-隔离）：对于存在交叉反应的每对药物 (u,v)，要求 u 和 v 必须分属不同侧（不同方案组）以避免副作用；对于无交叉反应的药物则无要求。
- 模式 B（反应-同组）：对于存在交叉反应的每对药物 (u,v)，要求 u 和 v 必须属于同侧（同一方案组）以产生协同效应；对于无交叉反应的药物则无要求。
- 模式 C（无反应-隔离）：对于无已知交叉反应的每对药物 (u,v)，要求 u 和 v 必须分属不同侧；对于有交叉反应的药物则无要求。
- 模式 D（无反应-同组）：对于无已知交叉反应的每对药物 (u,v)，要求 u 和 v 必须属于同侧；对于有交叉反应的药物则无要求。

你可以通过以下方式与系统交互（每次只能使用一种查询）：

1. **局部关系查询**：试探性询问两种药物按某种关系调配是否满足当前模式。
   - 关系类型：同侧 或 对侧
   - 系统会回答：满足 或 冲突

2. **全局方案校验**：提交一个完整的治疗方案编排，系统会检查是否全局满足当前模式。
   - 若满足，返回：全局满足
   - 若冲突，返回：发现冲突，并给出一个冲突药物对及其分组关系

3. **模式宣告**：当你收集足够证据后，可以宣告你推断出的筛选模式。
   - 需要提供至少两条先前的试探记录作为证据：一条针对有交叉反应的药物对（指令中严格使用"边对"表示），一条针对无交叉反应的药物对（指令中严格使用"非边对"表示）
   - 证据格式：边对=(x,y),关系=同侧/对侧,结果=满足/冲突; 非边对=(a,b),关系=同侧/对侧,结果=满足/冲突
   - 系统会验证证据是否能唯一指向该模式

4. **不可行证据**（仅在模式为 A 或 C 且由于药物相互作用链无法成功分组时使用）：
   - 若模式为 A：提交图中的一个奇环（奇数个药物组成的闭环，相邻药物间均有交叉反应）
   - 若模式为 C：提交补图中的一个奇环（相邻药物间均无交叉反应）
   - 环的格式：药物序列，例如 1,2,3,1

5. **最终方案提交**：在成功判定模式后，提交模式和对应的分组方案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 局部关系查询（例如询问药物 1 和 2 是否可以同侧）：
<query_local>1,2,同侧</query_local>

- 全局方案校验（例如方案 L 包含药物 1,2，R 包含 3,4,5）：
<query_global>L=1,2;R=3,4,5</query_global>

- 模式宣告（例如宣告模式 A，并提供证据）：
<declare_mode>mode=A, evidence=边对=(1,2),关系=对侧,结果=满足; 非边对=(1,3),关系=对侧,结果=冲突</declare_mode>

- 不可行证据（例如提交模式 A 的奇数相互作用链证明）：
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- 最终方案提交（例如模式 A，L=1,3 和 R=2,4）：
<answer>mode=A, L=1,3, R=2,4</answer>

注意：查询要尽可能少，以最高效的方式推理出答案。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's operate the "Combination Therapy Screening" system. Here are the rules:

The system has loaded a drug interaction graph G, containing {n} drug molecules (numbered 1 to {n}) and several known cross-reactions (no self-loops, no multiple interactions).
The set of cross-reactions (representing edges) is: {edges}

Your goal is to allocate all drug molecules into two disjoint treatment regimens, L and R (L union R equals all drugs, L intersect R is empty).

However, the system has secretly activated one of the following four screening modes, which determines what regimen composition is valid:
- Mode A (Interacting-Opposite): For each pair of interacting drugs (u,v), u and v must be on different sides (different regimens) to avoid adverse side effects; non-interacting drugs have no requirement.
- Mode B (Interacting-Same): For each pair of interacting drugs (u,v), u and v must be on the same side (same regimen) to produce synergistic effects; non-interacting drugs have no requirement.
- Mode C (NonInteracting-Opposite): For each pair of non-interacting drugs (u,v), u and v must be on different sides; interacting drugs have no requirement.
- Mode D (NonInteracting-Same): For each pair of non-interacting drugs (u,v), u and v must be on the same side; interacting drugs have no requirement.

You can interact with the system in the following ways (one query type at a time):

1. **Local Relation Query**: Test whether two drugs can be prescribed with a certain relation under the current mode.
   - Relation types: same or opposite
   - The system will answer: satisfied or conflict

2. **Global Scheme Verification**: Submit a complete regimen layout, and the system will check if it globally satisfies the current mode.
   - If satisfied, return: globally satisfied
   - If conflict, return: conflict found, with one conflicting drug pair and its relation

3. **Mode Declaration**: When you have enough evidence, declare the screening mode you inferred.
   - Provide at least two prior test records as evidence: one for a pair of interacting drugs (must strictly use the keyword "edge"), one for a pair of non-interacting drugs (must strictly use the keyword "nonedge")
   - Evidence format: edge=(x,y),relation=same/opposite,result=satisfied/conflict; nonedge=(a,b),relation=same/opposite,result=satisfied/conflict
   - The system will verify if the evidence uniquely points to that mode

4. **Impossibility Proof** (only when mode is A or C and the drugs cannot be validly distributed):
   - If mode A: Submit an odd cycle of interacting drugs (odd number of drugs, adjacent drugs interact)
   - If mode C: Submit an odd cycle in the complement interaction graph (adjacent drugs do not interact)
   - Cycle format: drug sequence, e.g., 1,2,3,1

5. **Final Scheme Submission**: After successfully determining the mode, submit the mode and the corresponding regimens.

Each query can only contain one tag, using the following XML format:

- Local relation query (e.g., asking if drugs 1 and 2 can be on the same regimen):
<query_local>1,2,same</query_local>

- Global scheme verification (e.g., L=1,2 and R=3,4,5):
<query_global>L=1,2;R=3,4,5</query_global>

- Mode declaration (e.g., declare mode A with evidence):
<declare_mode>mode=A, evidence=edge=(1,2),relation=opposite,result=satisfied; nonedge=(1,3),relation=opposite,result=conflict</declare_mode>

- Impossibility proof (e.g., submit an odd cycle interaction proof for mode A):
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- Final scheme submission (e.g., mode A, L=1,3 and R=2,4):
<answer>mode=A, L=1,3, R=2,4</answer>

Note: Use as few queries as possible to efficiently deduce the answer.
"""

    contextualized_rule_zh_3 = """\
我们来操作"平行班级人员编排"系统，规则如下：

系统记录了 {n} 名重点关注学生（编号 1 到 {n}）和若干对已知的严重冲突关系（无自环、无重边）。
冲突关系（对应逻辑中的边）的集合为：{edges}

你的目标是将所有学生分配到两个不交的平行班级 L 和 R 中（L 和 R 的并集为所有学生，交集为空）。

然而，系统根据心理评估秘密激活了以下四种编排模式之一，它决定了什么样的人员分配是合法的：
- 模式 A（冲突-隔离）：对于存在严重冲突的每对学生 (u,v)，要求 u 和 v 必须分属不同侧（不同班级）以保证教学氛围和谐；对于无冲突的学生则无要求。
- 模式 B（冲突-同班）：对于存在严重冲突的每对学生 (u,v)，要求 u 和 v 必须属于同侧（同一班级）以便进行针对性的矛盾调解；对于无冲突的学生则无要求。
- 模式 C（无冲突-隔离）：对于无冲突关系的每对学生 (u,v)，要求 u 和 v 必须分属不同侧；对于有冲突的学生则无要求。
- 模式 D（无冲突-同班）：对于无冲突关系的每对学生 (u,v)，要求 u 和 v 必须属于同侧；对于有冲突的学生则无要求。

你可以通过以下方式与系统交互（每次只能使用一种查询）：

1. **局部关系查询**：试探性询问两名学生按某种关系编排是否满足当前模式。
   - 关系类型：同侧 或 对侧
   - 系统会回答：满足 或 冲突

2. **全局方案校验**：提交一个完整的班级分配方案，系统会检查是否全局满足当前模式。
   - 若满足，返回：全局满足
   - 若冲突，返回：发现冲突，并给出一个冲突学生对及其分配关系

3. **模式宣告**：当你收集足够证据后，可以宣告你推断出的编排模式。
   - 需要提供至少两条先前的试探记录作为证据：一条针对有冲突的学生对（指令中严格使用"边对"表示），一条针对无冲突的学生对（指令中严格使用"非边对"表示）
   - 证据格式：边对=(x,y),关系=同侧/对侧,结果=满足/冲突; 非边对=(a,b),关系=同侧/对侧,结果=满足/冲突
   - 系统会验证证据是否能唯一指向该模式

4. **不可行证据**（仅在模式为 A 或 C 且由于人际关系死结无法分班时使用）：
   - 若模式为 A：提交学生中的一个奇环（奇数名学生形成的冲突闭环，相邻学生间均有冲突）
   - 若模式为 C：提交补图中的一个奇环（相邻学生间均无冲突）
   - 环的格式：学生序列，例如 1,2,3,1

5. **最终方案提交**：在成功判定模式后，提交模式和对应的班级分配。

每次查询只能包含一个标签，使用以下 XML 格式：

- 局部关系查询（例如询问学生 1 和 2 是否可以同侧）：
<query_local>1,2,同侧</query_local>

- 全局方案校验（例如班级 L 包含学生 1,2，班级 R 包含 3,4,5）：
<query_global>L=1,2;R=3,4,5</query_global>

- 模式宣告（例如宣告模式 A，并提供证据）：
<declare_mode>mode=A, evidence=边对=(1,2),关系=对侧,结果=满足; 非边对=(1,3),关系=对侧,结果=冲突</declare_mode>

- 不可行证据（例如提交模式 A 的奇数冲突闭环证明）：
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- 最终方案提交（例如模式 A，L=1,3 和 R=2,4）：
<answer>mode=A, L=1,3, R=2,4</answer>

注意：查询要尽可能少，以最高效的方式推理出答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's operate the "Parallel Class Roster Arrangement" system. Here are the rules:

The system has documented {n} students of concern (numbered 1 to {n}) and several known severe conflict relations (no self-loops, no multiple conflicts).
The set of conflicts (representing edges) is: {edges}

Your goal is to assign all students into two disjoint parallel classes, L and R (L union R equals all students, L intersect R is empty).

However, based on psychological assessments, the system has secretly activated one of the following four arrangement modes, determining what assignment is valid:
- Mode A (Conflict-Opposite): For each pair of conflicting students (u,v), u and v must be on different sides (different classes) to maintain a harmonious atmosphere; non-conflicting students have no requirement.
- Mode B (Conflict-Same): For each pair of conflicting students (u,v), u and v must be on the same side (same class) for targeted mediation; non-conflicting students have no requirement.
- Mode C (NonConflict-Opposite): For each pair of non-conflicting students (u,v), u and v must be on different sides; conflicting students have no requirement.
- Mode D (NonConflict-Same): For each pair of non-conflicting students (u,v), u and v must be on the same side; conflicting students have no requirement.

You can interact with the system in the following ways (one query type at a time):

1. **Local Relation Query**: Test whether two students can be placed with a certain relation under the current mode.
   - Relation types: same or opposite
   - The system will answer: satisfied or conflict

2. **Global Scheme Verification**: Submit a complete roster assignment, and the system will check if it globally satisfies the current mode.
   - If satisfied, return: globally satisfied
   - If conflict, return: conflict found, with one conflicting student pair and its relation

3. **Mode Declaration**: When you have enough evidence, declare the arrangement mode you inferred.
   - Provide at least two prior test records as evidence: one for a conflicting student pair (must strictly use the keyword "edge"), one for a non-conflicting student pair (must strictly use the keyword "nonedge")
   - Evidence format: edge=(x,y),relation=same/opposite,result=satisfied/conflict; nonedge=(a,b),relation=same/opposite,result=satisfied/conflict
   - The system will verify if the evidence uniquely points to that mode

4. **Impossibility Proof** (only when mode is A or C and the assignment is impossible due to relationship deadlocks):
   - If mode A: Submit an odd cycle of conflicting students (odd number of students, adjacent students have conflicts)
   - If mode C: Submit an odd cycle in the complement conflict graph (adjacent students do not have conflicts)
   - Cycle format: student sequence, e.g., 1,2,3,1

5. **Final Scheme Submission**: After successfully determining the mode, submit the mode and the corresponding rosters.

Each query can only contain one tag, using the following XML format:

- Local relation query (e.g., asking if students 1 and 2 can be in the same class):
<query_local>1,2,same</query_local>

- Global scheme verification (e.g., L=1,2 and R=3,4,5):
<query_global>L=1,2;R=3,4,5</query_global>

- Mode declaration (e.g., declare mode A with evidence):
<declare_mode>mode=A, evidence=edge=(1,2),relation=opposite,result=satisfied; nonedge=(1,3),relation=opposite,result=conflict</declare_mode>

- Impossibility proof (e.g., submit an odd conflict cycle proof for mode A):
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- Final scheme submission (e.g., mode A, L=1,3 and R=2,4):
<answer>mode=A, L=1,3, R=2,4</answer>

Note: Use as few queries as possible to efficiently deduce the answer.
"""

    contextualized_rule_zh_4 = """\
我们来操作"车间流水线批次调度"系统，规则如下：

系统映射了一个工业生产拓扑 G，包含 {n} 个生产设备（编号 1 到 {n}）和若干对物理资源抢占关系（无自环、无重边）。
资源抢占关系（对应逻辑中的边）的集合为：{edges}

你的目标是将所有生产设备划分至两个独立的执行批次 L 和 R 中（L 和 R 的并集为所有设备，交集为空）。

然而，工艺调度引擎秘密激活了以下四种排产模式之一，它决定了什么样的批次分配是合法的：
- 模式 A（抢占-隔离）：对于存在资源抢占的每对设备 (u,v)，要求 u 和 v 必须分属不同侧（即安排在不同批次），以避免干涉死锁；对于无抢占关系的设备则无要求。
- 模式 B（抢占-同组）：对于存在资源抢占的每对设备 (u,v)，要求 u 和 v 必须属于同侧（即安排在同一批次）以实现集中式资源调度；对于无抢占关系的设备则无要求。
- 模式 C（无抢占-隔离）：对于不存在资源抢占的每对设备 (u,v)，要求 u 和 v 必须分属不同侧；对于有抢占关系的设备则无要求。
- 模式 D（无抢占-同组）：对于不存在资源抢占的每对设备 (u,v)，要求 u 和 v 必须属于同侧；对于有抢占关系的设备则无要求。

你可以通过以下方式与系统交互（每次只能使用一种查询）：

1. **局部关系查询**：试探性询问两台设备按某种关系排产是否满足当前模式。
   - 关系类型：同侧 或 对侧
   - 系统会回答：满足 或 冲突

2. **全局方案校验**：提交一个完整的排产批次分配方案，系统会检查是否全局满足当前模式。
   - 若满足，返回：全局满足
   - 若冲突，返回：发现冲突，并给出一个冲突设备对及其排产关系

3. **模式宣告**：当你收集足够验证数据后，可以宣告你推断出的排产模式。
   - 需要提供至少两条先前的试探记录作为证据：一条针对存在资源抢占的设备对（指令中严格使用"边对"表示），一条针对无抢占关系的设备对（指令中严格使用"非边对"表示）
   - 证据格式：边对=(x,y),关系=同侧/对侧,结果=满足/冲突; 非边对=(a,b),关系=同侧/对侧,结果=满足/冲突
   - 系统会验证证据是否能唯一指向该模式

4. **不可行证据**（仅在模式为 A 或 C 且由于资源死锁无法完成批次划分时使用）：
   - 若模式为 A：提交拓扑中的一个奇环（奇数台设备构成的死锁环路，相邻设备间均有抢占关系）
   - 若模式为 C：提交补图中的一个奇环（相邻设备间均无抢占关系）
   - 环的格式：设备序列，例如 1,2,3,1

5. **最终方案提交**：在成功判定模式后，提交模式和对应的批次分配。

每次查询只能包含一个标签，使用以下 XML 格式：

- 局部关系查询（例如询问设备 1 和 2 是否可以同侧分配）：
<query_local>1,2,同侧</query_local>

- 全局方案校验（例如批次 L 包含设备 1,2，R 包含 3,4,5）：
<query_global>L=1,2;R=3,4,5</query_global>

- 模式宣告（例如宣告模式 A，并提供证据）：
<declare_mode>mode=A, evidence=边对=(1,2),关系=对侧,结果=满足; 非边对=(1,3),关系=对侧,结果=冲突</declare_mode>

- 不可行证据（例如提交模式 A 的奇数死锁环路证明）：
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- 最终方案提交（例如模式 A，L=1,3 和 R=2,4）：
<answer>mode=A, L=1,3, R=2,4</answer>

注意：查询要尽可能少，以最高效的方式推理出答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's operate the "Workshop Pipeline Batch Scheduling" system. Here are the rules:

The system has mapped an industrial production topology G, containing {n} production machines (numbered 1 to {n}) and several physical resource contentions (no self-loops, no multiple contentions).
The set of resource contentions (representing edges) is: {edges}

Your goal is to divide all machines into two separate execution batches, L and R (L union R equals all machines, L intersect R is empty).

However, the process scheduling engine has secretly activated one of the following four production modes, determining what batch assignment is valid:
- Mode A (Contention-Opposite): For each pair of contending machines (u,v), u and v must be on different sides (different batches) to avoid interference deadlocks; non-contending machines have no requirement.
- Mode B (Contention-Same): For each pair of contending machines (u,v), u and v must be on the same side (same batch) for centralized resource dispatching; non-contending machines have no requirement.
- Mode C (NonContention-Opposite): For each pair of non-contending machines (u,v), u and v must be on different sides; contending machines have no requirement.
- Mode D (NonContention-Same): For each pair of non-contending machines (u,v), u and v must be on the same side; contending machines have no requirement.

You can interact with the system in the following ways (one query type at a time):

1. **Local Relation Query**: Test whether two machines can be assigned with a certain relation under the current mode.
   - Relation types: same or opposite
   - The system will answer: satisfied or conflict

2. **Global Scheme Verification**: Submit a complete batch allocation scheme, and the system will check if it globally satisfies the current mode.
   - If satisfied, return: globally satisfied
   - If conflict, return: conflict found, with one conflicting machine pair and its relation

3. **Mode Declaration**: When you have enough empirical data, declare the production mode you inferred.
   - Provide at least two prior test records as evidence: one for a contending machine pair (must strictly use the keyword "edge"), one for a non-contending machine pair (must strictly use the keyword "nonedge")
   - Evidence format: edge=(x,y),relation=same/opposite,result=satisfied/conflict; nonedge=(a,b),relation=same/opposite,result=satisfied/conflict
   - The system will verify if the evidence uniquely points to that mode

4. **Impossibility Proof** (only when mode is A or C and the scheduling is impossible due to deadlocks):
   - If mode A: Submit an odd cycle in the topology (odd deadlock cycle, adjacent machines contend for resources)
   - If mode C: Submit an odd cycle in the complement topology (adjacent machines do not contend)
   - Cycle format: machine sequence, e.g., 1,2,3,1

5. **Final Scheme Submission**: After successfully determining the mode, submit the mode and the corresponding batch allocation.

Each query can only contain one tag, using the following XML format:

- Local relation query (e.g., asking if machines 1 and 2 can be in the same batch):
<query_local>1,2,same</query_local>

- Global scheme verification (e.g., L=1,2 and R=3,4,5):
<query_global>L=1,2;R=3,4,5</query_global>

- Mode declaration (e.g., declare mode A with evidence):
<declare_mode>mode=A, evidence=edge=(1,2),relation=opposite,result=satisfied; nonedge=(1,3),relation=opposite,result=conflict</declare_mode>

- Impossibility proof (e.g., submit an odd deadlock cycle proof for mode A):
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- Final scheme submission (e.g., mode A, L=1,3 and R=2,4):
<answer>mode=A, L=1,3, R=2,4</answer>

Note: Use as few queries as possible to efficiently deduce the answer.
"""

    contextualized_rule_zh_5 = """\
我们来操作"涉案人员隔离审查"系统，规则如下：

案情梳理网络 G 包含了 {n} 名核心嫌疑人（编号 1 到 {n}）和若干已确认的利益输送关系（无自环、无重边）。
利益关系（对应逻辑中的边）的集合为：{edges}

你的目标是将所有嫌疑人分为两个不交的隔离审查组 L 和 R（L 和 R 的并集为所有人，交集为空）。

然而，专案组秘密设定了以下四种审查策略模式之一，它决定了什么样的人员分组是合法的：
- 模式 A（利益-隔离）：对于存在直接利益关系的每对嫌疑人 (u,v)，要求 u 和 v 必须分属不同侧（不同审查组）以防串供；对于无直接利益关系的人员则无要求。
- 模式 B（利益-同组）：对于存在直接利益关系的每对嫌疑人 (u,v)，要求 u 和 v 必须属于同侧（同一审查组）以便安排当面对质；对于无直接利益关系的人员则无要求。
- 模式 C（无利益-隔离）：对于不存在直接利益关系的每对嫌疑人 (u,v)，要求 u 和 v 必须分属不同侧；对于有利益关系的人员则无要求。
- 模式 D（无利益-同组）：对于不存在直接利益关系的每对嫌疑人 (u,v)，要求 u 和 v 必须属于同侧；对于有利益关系的人员则无要求。

你可以通过以下方式与系统交互（每次只能使用一种查询）：

1. **局部关系查询**：试探性询问两名嫌疑人按某种关系分组是否满足当前模式。
   - 关系类型：同侧 或 对侧
   - 系统会回答：满足 或 冲突

2. **全局方案校验**：提交一个完整的隔离审查分组方案，系统会检查是否全局满足当前模式。
   - 若满足，返回：全局满足
   - 若冲突，返回：发现冲突，并给出一个冲突嫌疑人对及其分组关系

3. **模式宣告**：当你收集足够审讯线索后，可以宣告你推断出的审查策略模式。
   - 需要提供至少两条先前的试探记录作为证据：一条针对存在利益关系的嫌疑人对（指令中严格使用"边对"表示），一条针对无利益关系的嫌疑人对（指令中严格使用"非边对"表示）
   - 证据格式：边对=(x,y),关系=同侧/对侧,结果=满足/冲突; 非边对=(a,b),关系=同侧/对侧,结果=满足/冲突
   - 系统会验证证据是否能唯一指向该模式

4. **不可行证据**（仅在模式为 A 或 C 且由于涉案利益网闭环导致无法合法分组时使用）：
   - 若模式为 A：提交案情网中的一个奇环（由奇数名嫌疑人构成的利益闭环，相邻嫌疑人间均有利益输送）
   - 若模式为 C：提交补图中的一个奇环（相邻嫌疑人间均无利益关系）
   - 环的格式：嫌疑人序列，例如 1,2,3,1

5. **最终方案提交**：在成功判定模式后，提交模式和对应的分组方案。

每次查询只能包含一个标签，使用以下 XML 格式：

- 局部关系查询（例如询问嫌疑人 1 和 2 是否可以同组）：
<query_local>1,2,同侧</query_local>

- 全局方案校验（例如审查组 L 包含 1,2，R 包含 3,4,5）：
<query_global>L=1,2;R=3,4,5</query_global>

- 模式宣告（例如宣告模式 A，并提供证据）：
<declare_mode>mode=A, evidence=边对=(1,2),关系=对侧,结果=满足; 非边对=(1,3),关系=对侧,结果=冲突</declare_mode>

- 不可行证据（例如提交模式 A 的奇数利益闭环证明）：
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- 最终方案提交（例如模式 A，L=1,3 和 R=2,4）：
<answer>mode=A, L=1,3, R=2,4</answer>

注意：查询要尽可能少，以最高效的方式推理出答案。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's operate the "Suspect Isolation and Interrogation" system. Here are the rules:

The case network G contains {n} core suspects (numbered 1 to {n}) and several confirmed conflicts of interest or improper transfers (no self-loops, no multiple links).
The set of interest links (representing edges) is: {edges}

Your goal is to divide all suspects into two disjoint isolation interrogation groups, L and R (L union R equals all suspects, L intersect R is empty).

However, the task force has secretly established one of the following four interrogation strategy modes, determining what grouping is valid:
- Mode A (Linked-Opposite): For each pair of suspects (u,v) with a direct interest link, u and v must be on different sides (different groups) to prevent collusion; unlinked suspects have no requirement.
- Mode B (Linked-Same): For each pair of suspects (u,v) with a direct interest link, u and v must be on the same side (same group) for direct confrontation; unlinked suspects have no requirement.
- Mode C (Unlinked-Opposite): For each pair of unlinked suspects (u,v), u and v must be on different sides; linked suspects have no requirement.
- Mode D (Unlinked-Same): For each pair of unlinked suspects (u,v), u and v must be on the same side; linked suspects have no requirement.

You can interact with the system in the following ways (one query type at a time):

1. **Local Relation Query**: Test whether two suspects can be grouped with a certain relation under the current mode.
   - Relation types: same or opposite
   - The system will answer: satisfied or conflict

2. **Global Scheme Verification**: Submit a complete isolation grouping scheme, and the system will check if it globally satisfies the current mode.
   - If satisfied, return: globally satisfied
   - If conflict, return: conflict found, with one conflicting suspect pair and its relation

3. **Mode Declaration**: When you have enough interrogation clues, declare the strategy mode you inferred.
   - Provide at least two prior test records as evidence: one for a linked suspect pair (must strictly use the keyword "edge"), one for an unlinked suspect pair (must strictly use the keyword "nonedge")
   - Evidence format: edge=(x,y),relation=same/opposite,result=satisfied/conflict; nonedge=(a,b),relation=same/opposite,result=satisfied/conflict
   - The system will verify if the evidence uniquely points to that mode

4. **Impossibility Proof** (only when mode is A or C and grouping is impossible due to closed-loop interest networks):
   - If mode A: Submit an odd cycle in the case network (odd number of suspects forming a closed loop, adjacent suspects have interest links)
   - If mode C: Submit an odd cycle in the complement network (adjacent suspects have no links)
   - Cycle format: suspect sequence, e.g., 1,2,3,1

5. **Final Scheme Submission**: After successfully determining the mode, submit the mode and the corresponding grouping.

Each query can only contain one tag, using the following XML format:

- Local relation query (e.g., asking if suspects 1 and 2 can be in the same group):
<query_local>1,2,same</query_local>

- Global scheme verification (e.g., L=1,2 and R=3,4,5):
<query_global>L=1,2;R=3,4,5</query_global>

- Mode declaration (e.g., declare mode A with evidence):
<declare_mode>mode=A, evidence=edge=(1,2),relation=opposite,result=satisfied; nonedge=(1,3),relation=opposite,result=conflict</declare_mode>

- Impossibility proof (e.g., submit an odd closed-loop proof for mode A):
<prove_impossible>mode=A, cycle=1,2,3,1</prove_impossible>

- Final scheme submission (e.g., mode A, L=1,3 and R=2,4):
<answer>mode=A, L=1,3, R=2,4</answer>

Note: Use as few queries as possible to efficiently deduce the answer.
"""

    tags = ["answer", "query_local", "query_global", "declare_mode", "prove_impossible"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "edges": "1-2, 2-3",
                "mode": "B",
                "solution_L": "1,2,3",
                "solution_R": "4",
            },
            2: {
                "n": 6,
                "edges": "1-2, 2-3, 3-4, 4-5, 5-6, 6-1",
                "mode": "A",
                "solution_L": "1,3,5",
                "solution_R": "2,4,6",
            },
            3: {
                "n": 4,
                "edges": "1-2, 2-3, 3-4, 4-1, 1-3",
                "mode": "D",
                "solution_L": "1,2,4",
                "solution_R": "3",
            },
            4: {
                "n": 6,
                "edges": "1-2, 1-3, 2-3, 4-5, 4-6, 5-6",
                "mode": "C",
                "solution_L": "1,2,3",
                "solution_R": "4,5,6",
            },
            5: {
                "n": 7,
                "edges": "1-2, 2-3, 3-4, 4-5, 5-6, 6-1, 1-7, 7-4",
                "mode": "A",
                "odd_cycle": "1,7,4,5,6,1",
            },
        },
        "en": {
            1: {
                "n": 4,
                "edges": "1-2, 2-3",
                "mode": "B",
                "solution_L": "1,2,3",
                "solution_R": "4",
            },
            2: {
                "n": 6,
                "edges": "1-2, 2-3, 3-4, 4-5, 5-6, 6-1",
                "mode": "A",
                "solution_L": "1,3,5",
                "solution_R": "2,4,6",
            },
            3: {
                "n": 4,
                "edges": "1-2, 2-3, 3-4, 4-1, 1-3",
                "mode": "D",
                "solution_L": "1,2,4",
                "solution_R": "3",
            },
            4: {
                "n": 6,
                "edges": "1-2, 1-3, 2-3, 4-5, 4-6, 5-6",
                "mode": "C",
                "solution_L": "1,2,3",
                "solution_R": "4,5,6",
            },
            5: {
                "n": 7,
                "edges": "1-2, 2-3, 3-4, 4-5, 5-6, 6-1, 1-7, 7-4",
                "mode": "A",
                "odd_cycle": "1,7,4,5,6,1",
            },
        },
    }

    def __init__(self, config):
        self.query_history = []
        self.mode_declared = False
        self.declared_mode = None
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
        self._game_info["edges"] = cfg["edges"]

        self.edges = set()
        for edge_str in cfg["edges"].split(","):
            edge_str = edge_str.strip()
            u, v = edge_str.split("-")
            u, v = u.strip(), v.strip()
            self.edges.add((u, v))
            self.edges.add((v, u))

        self.vertices = set(str(i) for i in range(1, cfg["n"] + 1))

        self.hidden_mode = cfg["mode"]

        if "solution_L" in cfg:
            self.reference_L = set(cfg["solution_L"].split(","))
            self.reference_R = set(cfg["solution_R"].split(","))
        else:
            self.reference_L = None
            self.reference_R = None

        self.odd_cycle = cfg.get("odd_cycle", None)

    def _is_edge(self, u, v):
        return (u, v) in self.edges

    def _check_relation(self, u, v, relation):
        is_edge = self._is_edge(u, v)
        
        if self.config.language == "zh":
            is_same = (relation == "同侧")
        else:
            is_same = (relation == "same")

        mode = self.hidden_mode

        if mode == "A":
            if is_edge:
                return not is_same
            else:
                return True
        elif mode == "B":
            if is_edge:
                return is_same
            else:
                return True
        elif mode == "C":
            if not is_edge:
                return not is_same
            else:
                return True
        elif mode == "D":
            if not is_edge:
                return is_same
            else:
                return True
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def _check_global_scheme(self, L_set, R_set):
        for u in self.vertices:
            for v in self.vertices:
                if u >= v:
                    continue
                
                u_in_L = u in L_set
                v_in_L = v in L_set
                actual_same = (u_in_L == v_in_L)
                
                is_edge = self._is_edge(u, v)
                mode = self.hidden_mode
                
                if mode == "A":
                    if is_edge and actual_same:
                        rel = "同侧" if self.config.language == "zh" else "same"
                        return False, (u, v), rel
                elif mode == "B":
                    if is_edge and not actual_same:
                        rel = "对侧" if self.config.language == "zh" else "opposite"
                        return False, (u, v), rel
                elif mode == "C":
                    if not is_edge and actual_same:
                        rel = "同侧" if self.config.language == "zh" else "same"
                        return False, (u, v), rel
                elif mode == "D":
                    if not is_edge and not actual_same:
                        rel = "对侧" if self.config.language == "zh" else "opposite"
                        return False, (u, v), rel
        
        return True, None, None

    def _verify_mode_evidence(self, mode, evidence_str):
        try:
            parts = evidence_str.split(";")
            edge_evidence = None
            nonedge_evidence = None
            
            for part in parts:
                part = part.strip()
                if self.config.language == "zh":
                    if part.startswith("边对="):
                        edge_evidence = self._parse_evidence_item(part, "边对=")
                    elif part.startswith("非边对="):
                        nonedge_evidence = self._parse_evidence_item(part, "非边对=")
                else:
                    if part.startswith("edge="):
                        edge_evidence = self._parse_evidence_item(part, "edge=")
                    elif part.startswith("nonedge="):
                        nonedge_evidence = self._parse_evidence_item(part, "nonedge=")
            
            if not edge_evidence or not nonedge_evidence:
                return False, "证据不完整" if self.config.language == "zh" else "Incomplete evidence"
            
            edge_match = any(
                h["u"] == edge_evidence["u"] and
                h["v"] == edge_evidence["v"] and
                h["relation"] == edge_evidence["relation"] and
                h["result"] == edge_evidence["result"]
                for h in self.query_history if h["type"] == "local"
            )
            
            nonedge_match = any(
                h["u"] == nonedge_evidence["u"] and
                h["v"] == nonedge_evidence["v"] and
                h["relation"] == nonedge_evidence["relation"] and
                h["result"] == nonedge_evidence["result"]
                for h in self.query_history if h["type"] == "local"
            )
            
            if not edge_match or not nonedge_match:
                return False, "证据未找到于历史记录" if self.config.language == "zh" else "Evidence not found in history"
            
            edge_u, edge_v = edge_evidence["u"], edge_evidence["v"]
            edge_rel = edge_evidence["relation"]
            edge_res = edge_evidence["result"]
            
            nonedge_u, nonedge_v = nonedge_evidence["u"], nonedge_evidence["v"]
            nonedge_rel = nonedge_evidence["relation"]
            nonedge_res = nonedge_evidence["result"]
            
            if not self._is_edge(edge_u, edge_v):
                return False, "边对证据实际不是边" if self.config.language == "zh" else "Edge evidence is not an edge"
            if self._is_edge(nonedge_u, nonedge_v):
                return False, "非边对证据实际是边" if self.config.language == "zh" else "Non-edge evidence is actually an edge"
            
            possible_modes = []
            for test_mode in ["A", "B", "C", "D"]:
                original_mode = self.hidden_mode
                self.hidden_mode = test_mode
                
                edge_check = self._check_relation(edge_u, edge_v, edge_rel)
                nonedge_check = self._check_relation(nonedge_u, nonedge_v, nonedge_rel)
                
                self.hidden_mode = original_mode
                
                if self.config.language == "zh":
                    edge_expected = (edge_res == "满足")
                    nonedge_expected = (nonedge_res == "满足")
                else:
                    edge_expected = (edge_res == "satisfied")
                    nonedge_expected = (nonedge_res == "satisfied")
                
                if edge_check == edge_expected and nonedge_check == nonedge_expected:
                    possible_modes.append(test_mode)
            
            if len(possible_modes) == 1 and possible_modes[0] == mode:
                return True, ""
            else:
                return False, "证据不能唯一指向该模式" if self.config.language == "zh" else "Evidence does not uniquely point to the mode"
                
        except Exception as e:
            return False, str(e)

    def _parse_evidence_item(self, item_str, prefix):
        item_str = item_str[len(prefix):].strip()
        start = item_str.find('(')
        end = item_str.find(')')
        if start == -1 or end == -1 or end < start:
            raise ValueError("找不到顶点对")
            
        pair_str = item_str[start+1:end]
        u, v = pair_str.split(",")
        u, v = u.strip(), v.strip()
        
        rest_str = item_str[end+1:]
        parts = rest_str.split(",")
        
        relation = None
        result = None
        for part in parts:
            part = part.strip()
            if "=" in part:
                key, val = part.split("=", 1)
                key = key.strip()
                val = val.strip()
                if self.config.language == "zh":
                    if key == "关系":
                        relation = val
                    elif key == "结果":
                        result = val
                else:
                    if key == "relation":
                        relation = val
                    elif key == "result":
                        result = val
        
        return {"u": u, "v": v, "relation": relation, "result": result}

    def _verify_odd_cycle(self, mode, cycle_str):
        try:
            vertices_in_cycle = [v.strip() for v in cycle_str.split(",")]
            
            if vertices_in_cycle[0] != vertices_in_cycle[-1]:
                return False, "环不闭合" if self.config.language == "zh" else "Cycle not closed"
            
            vertices_in_cycle = vertices_in_cycle[:-1]
            
            if len(vertices_in_cycle) % 2 == 0:
                return False, "环的长度不是奇数" if self.config.language == "zh" else "Cycle length is not odd"
            
            if mode == "A":
                for i in range(len(vertices_in_cycle)):
                    u = vertices_in_cycle[i]
                    v = vertices_in_cycle[(i + 1) % len(vertices_in_cycle)]
                    if not self._is_edge(u, v):
                        return False, f"顶点 {u} 和 {v} 之间无边" if self.config.language == "zh" else f"No edge between {u} and {v}"
            elif mode == "C":
                for i in range(len(vertices_in_cycle)):
                    u = vertices_in_cycle[i]
                    v = vertices_in_cycle[(i + 1) % len(vertices_in_cycle)]
                    if self._is_edge(u, v):
                        return False, f"顶点 {u} 和 {v} 之间有边" if self.config.language == "zh" else f"Edge exists between {u} and {v}"
            else:
                return False, "该模式不需要奇环证明" if self.config.language == "zh" else "This mode does not require odd cycle proof"
            
            return True, ""
            
        except Exception as e:
            return False, str(e)

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"]
            
            mode_match = re.search(r'mode\s*=\s*([A-D])', raw_ans, re.IGNORECASE)
            l_match = re.search(r'L\s*=\s*([\d,\s]+?)(?:\s*,\s*R\s*=|$)', raw_ans)
            r_match = re.search(r'R\s*=\s*([\d,\s]+)', raw_ans)
            
            if not mode_match or not l_match or not r_match:
                return False
            
            mode = mode_match.group(1).upper()
            L_str = l_match.group(1).strip().rstrip(',')
            R_str = r_match.group(1).strip().rstrip(',')
            
            if mode != self.hidden_mode:
                return False
            
            L_set = set(v.strip() for v in L_str.split(",") if v.strip())
            R_set = set(v.strip() for v in R_str.split(",") if v.strip())
            
            if L_set.union(R_set) != self.vertices:
                return False
            
            if L_set.intersection(R_set):
                return False
            
            is_valid, _, _ = self._check_global_scheme(L_set, R_set)
            return is_valid
            
        except Exception:
            return False
    
    def _cf_core_produce(self, parsed_info):
        if "query_local" in parsed_info:
            try:
                raw = parsed_info["query_local"].strip()
                parts = [p.strip() for p in raw.split(",")]
                if len(parts) != 3:
                    raise ValueError("格式错误")
                
                u, v, relation = parts[0], parts[1], parts[2]
                
                if u not in self.vertices or v not in self.vertices:
                    return "错误：顶点不存在" if self.config.language == "zh" else "Error: Vertex does not exist"
                
                if u == v:
                    return "错误：不能查询相同顶点" if self.config.language == "zh" else "Error: Cannot query same vertex"
                
                is_satisfied = self._check_relation(u, v, relation)
                
                result_str = "满足" if is_satisfied else "冲突"
                if self.config.language == "en":
                    result_str = "satisfied" if is_satisfied else "conflict"
                
                self.query_history.append({
                    "type": "local",
                    "u": u,
                    "v": v,
                    "relation": relation,
                    "result": result_str
                })
                
                return result_str
                
            except Exception as e:
                return f"错误：{str(e)}" if self.config.language == "zh" else f"Error: {str(e)}"
        
        elif "query_global" in parsed_info:
            try:
                raw = parsed_info["query_global"].strip()
                parts = raw.split(";")
                L_str = None
                R_str = None
                
                for part in parts:
                    part = part.strip()
                    if part.startswith("L="):
                        L_str = part[2:].strip()
                    elif part.startswith("R="):
                        R_str = part[2:].strip()
                
                if not L_str or not R_str:
                    raise ValueError("格式错误")
                
                L_set = set(v.strip() for v in L_str.split(",") if v.strip())
                R_set = set(v.strip() for v in R_str.split(",") if v.strip())
                
                is_valid, conflict_pair, conflict_rel = self._check_global_scheme(L_set, R_set)
                
                if is_valid:
                    return "全局满足" if self.config.language == "zh" else "Globally satisfied"
                else:
                    u, v = conflict_pair
                    if self.config.language == "zh":
                        return f"发现冲突：冲突对=({u},{v})，相对关系={conflict_rel}"
                    else:
                        return f"Conflict found: pair=({u},{v}), relation={conflict_rel}"
                    
            except Exception as e:
                return f"错误：{str(e)}" if self.config.language == "zh" else f"Error: {str(e)}"
        
        elif "declare_mode" in parsed_info:
            try:
                raw = parsed_info["declare_mode"].strip()
                mode_match = re.search(r'mode\s*=\s*([A-D])', raw, re.IGNORECASE)
                evidence_match = re.search(r'evidence\s*=\s*(.+)', raw, re.IGNORECASE)
                
                if not mode_match or not evidence_match:
                    raise ValueError("格式错误")
                
                mode = mode_match.group(1).upper()
                evidence = evidence_match.group(1).strip()
                
                is_valid, error_msg = self._verify_mode_evidence(mode, evidence)
                
                if is_valid:
                    if mode == self.hidden_mode:
                        self.mode_declared = True
                        self.declared_mode = mode
                        return "模式判断正确" if self.config.language == "zh" else "Mode judgment correct"
                    else:
                        self.state.set_state("failed", "wrong mode declaration")
                        return "模式判断错误" if self.config.language == "zh" else "Mode judgment incorrect"
                else:
                    return f"证据不足：{error_msg}" if self.config.language == "zh" else f"Insufficient evidence: {error_msg}"
                    
            except Exception as e:
                return f"错误：{str(e)}" if self.config.language == "zh" else f"Error: {str(e)}"
        
        elif "prove_impossible" in parsed_info:
            try:
                raw = parsed_info["prove_impossible"].strip()
                mode_match = re.search(r'mode\s*=\s*([A-D])', raw, re.IGNORECASE)
                cycle_match = re.search(r'cycle\s*=\s*(.+)', raw, re.IGNORECASE)
                
                if not mode_match or not cycle_match:
                    raise ValueError("格式错误")
                
                mode = mode_match.group(1).upper()
                cycle = cycle_match.group(1).strip()
                
                if mode != self.hidden_mode:
                    return "模式不匹配" if self.config.language == "zh" else "Mode mismatch"
                
                is_valid, error_msg = self._verify_odd_cycle(mode, cycle)
                
                if is_valid:
                    self.state.set_state("success", "proved impossible with odd cycle")
                    return "证据成立：不可能" if self.config.language == "zh" else "Proof valid: impossible"
                else:
                    return f"证据不成立：{error_msg}" if self.config.language == "zh" else f"Proof invalid: {error_msg}"
                    
            except Exception as e:
                return f"错误：{str(e)}" if self.config.language == "zh" else f"Error: {str(e)}"
        
        else:
            raise ValueError("未找到有效的查询标签" if self.config.language == "zh" else "No valid query tag found")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        vertices = sorted([str(i) for i in range(1, n + 1)], key=int)
        
        is_zh = (self.config.language == "zh")
        if is_zh:
            relations = ["同侧", "对侧"]
        else:
            relations = ["same", "opposite"]
            
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                u = vertices[i]
                v = vertices[j]
                
                for relation in relations:
                    query_content = f"{u},{v},{relation}"
                    query_str = f"<query_local>{query_content}</query_local>"
                    
                    is_satisfied = self._check_relation(u, v, relation)
                    
                    if is_zh:
                        ans = "满足" if is_satisfied else "冲突"
                    else:
                        ans = "satisfied" if is_satisfied else "conflict"
                        
                    queries.append({
                        "query": query_str,
                        "answer": ans
                    })
                    
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        is_zh = self.config.language == "zh"

        if is_zh:
            if correct == "满足":
                return "冲突"
            if correct == "冲突":
                return "满足"
        else:
            if correct == "satisfied":
                return "conflict"
            if correct == "conflict":
                return "satisfied"

        if is_zh:
            if correct == "全局满足":
                return "发现冲突：冲突对=(1,2)，相对关系=同侧"
            if correct.startswith("发现冲突"):
                return "全局满足"
        else:
            if correct == "Globally satisfied":
                return "Conflict found: pair=(1,2), relation=same"
            if correct.startswith("Conflict found"):
                return "Globally satisfied"

        return correct + "_WRONG"