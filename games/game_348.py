from .base import Game
import re

class TreeIsomorphismGame(Game):

    game_rule_zh = """\
我们现在来玩一个"无序根树同构判定"的推理游戏，规则如下：

游戏设定了一棵固定的有根树 T，节点集合为 {{1..{n}}}。现在给定两个不同的节点 A={nodeA} 和 B={nodeB}，这两个节点互不为对方的祖先（即两侧目标子树不相交）。

你的目标是：判定以 A 为根的子树和以 B 为根的子树是否作为无序根树同构。

- 初始时，你只能看到节点 A 和 B（可见集 V = {{A, B}}）。
- 你只能对可见集 V 中的节点提问。
- 当你对某节点执行 CHILDREN 查询后，其所有子节点会被加入可见集 V。
- PARENT 查询不会扩展可见集。

你可以使用以下四种查询原语：

1. **COUNT(x)**：查询节点 x 的直接子节点数量。返回一个非负整数。
   - 有效条件：x 必须在可见集 V 中。

2. **CHILDREN(x)**：查询节点 x 的所有子节点列表（按固定顺序返回）。
   - 有效条件：x 必须在可见集 V 中。
   - 执行后，所有子节点会被加入可见集 V。

3. **PARENT(x)**：查询节点 x 的父节点编号。如果 x 是整棵树的根节点，返回 NONE。
   - 有效条件：x 必须在可见集 V 中。
   - 此查询不会扩展可见集。

4. **DEPTH_EQ(u,v)**：判断节点 u 相对于 A 的深度是否等于节点 v 相对于 B 的深度。
   - 有效条件：u 必须位于以 A 为根的已可见子树中，v 必须位于以 B 为根的已可见子树中。
   - 返回"是"或"否"。

两棵以 A、B 为根的子树无序同构，当且仅当：
- A 和 B 的子节点数量相等（COUNT(A) = COUNT(B)），且
- 可以将 A 的每个子树与 B 的某个子树一一配对，使得配对后的对应子树递归同构（忽略子节点顺序）。

- 不允许直接询问"子树是否同构"或请求任何全局签名/编码/摘要。
- 如果对不在可见集 V 中的节点提问，或问题格式不符，会返回"无效"。
- 请尽可能少地使用查询次数。

每次查询只能包含一个标签，使用以下 XML 格式：

- COUNT 查询（例如查询节点 5）：
<query_count>5</query_count>

- CHILDREN 查询（例如查询节点 3）：
<query_children>3</query_children>

- PARENT 查询（例如查询节点 7）：
<query_parent>7</query_parent>

- DEPTH_EQ 查询（例如比较节点 2 和 8）：
<query_depth_eq>2,8</query_depth_eq>

当你收集足够信息后，请提交最终答案。答案必须包含判定结果和证据：

**如果同构**，提供一个从 A 的子树到 B 的子树的节点映射。格式如下：
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

其中 mapping 表示节点对应关系（A侧节点:B侧节点），用逗号分隔。

**如果不同构**，提供以下证据之一：
1. 给出某个相对深度 d，两侧在该深度的度数多重集不相等：
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>

2. 给出一对深度相等但度数不等的节点：
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    game_rule_en = """\
Let's play a "Unordered Rooted Tree Isomorphism" deduction game. Here are the rules:

The game has a fixed rooted tree T with node set {{1..{n}}}. You are given two different nodes A={nodeA} and B={nodeB}, where neither is an ancestor of the other (the two target subtrees are disjoint).

Your goal is: determine whether the subtree rooted at A and the subtree rooted at B are isomorphic as unordered rooted trees.

- Initially, you can only see nodes A and B (visible set V = {{A, B}}).
- You can only query nodes in the visible set V.
- When you execute a CHILDREN query on a node, all its children are added to the visible set V.
- PARENT queries do not expand the visible set.

You can use the following four query primitives:

1. **COUNT(x)**: Query the number of direct children of node x. Returns a non-negative integer.
   - Valid condition: x must be in the visible set V.

2. **CHILDREN(x)**: Query the list of all children of node x (returned in a fixed order).
   - Valid condition: x must be in the visible set V.
   - After execution, all children are added to the visible set V.

3. **PARENT(x)**: Query the parent node ID of x. If x is the root of the entire tree, returns NONE.
   - Valid condition: x must be in the visible set V.
   - This query does not expand the visible set.

4. **DEPTH_EQ(u,v)**: Check if node u's depth relative to A equals node v's depth relative to B.
   - Valid condition: u must be in the visible subtree rooted at A, v must be in the visible subtree rooted at B.
   - Returns "Yes" or "No".

Two subtrees rooted at A and B are isomorphic as unordered trees if and only if:
- A and B have the same number of children (COUNT(A) = COUNT(B)), and
- Each child subtree of A can be paired one-to-one with some child subtree of B such that paired subtrees are recursively isomorphic (ignoring child order).

- You cannot directly ask "are subtrees isomorphic" or request any global signature/encoding/digest.
- If you query a node not in the visible set V, or the query format is invalid, the response will be "Invalid".
- Please use as few queries as possible.

Each query must contain only one tag, using the following XML format:

- COUNT query (e.g., querying node 5):
<query_count>5</query_count>

- CHILDREN query (e.g., querying node 3):
<query_children>3</query_children>

- PARENT query (e.g., querying node 7):
<query_parent>7</query_parent>

- DEPTH_EQ query (e.g., comparing nodes 2 and 8):
<query_depth_eq>2,8</query_depth_eq>

When you have gathered enough information, submit your final answer. The answer must include the determination result and evidence:

**If isomorphic**, provide a node mapping from A's subtree to B's subtree. Format:
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

where mapping indicates node correspondences (A-side node:B-side node), separated by commas.

**If not isomorphic**, provide one of the following evidences:
1. Give a relative depth d where the degree multisets at that depth differ:
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>

2. Give a pair of nodes with equal depth but unequal degree:
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项“交通路网拓扑结构一致性分析”的任务。

系统记录了一个区域内的单向交通路网树，包含节点（路口/站点） {{1..{n}}}。现在我们重点关注两个不同的交通枢纽 A={nodeA} 和 B={nodeB}，它们各自辐射出的下游路网没有交集。

你的目标是：判定以 A 为起点的下游辐射路网和以 B 为起点的下游辐射路网，在拓扑结构上是否完全等效（即无序根树同构）。

- 初始时，你只能观测到枢纽 A 和 B（可见集 V = {{A, B}}）。
- 你只能对可见集 V 中的站点进行查询。
- 当你对某站点执行 CHILDREN（下游直达站点）查询后，其所有直接下游站点会被加入可见集 V。
- PARENT（上游来源站点）查询不会扩展可见集。

1. **COUNT(x)**：查询站点 x 的直接下游站点数量。返回一个非负整数。
   - 格式：<query_count>x</query_count>
2. **CHILDREN(x)**：查询站点 x 的所有直接下游站点列表。
   - 格式：<query_children>x</query_children>
3. **PARENT(x)**：查询站点 x 的上游来源站点编号。若无上游则返回 NONE。
   - 格式：<query_parent>x</query_parent>
4. **DEPTH_EQ(u,v)**：判断站点 u 相对于枢纽 A 的网络深度是否等于站点 v 相对于枢纽 B 的网络深度。
   - 格式：<query_depth_eq>u,v</query_depth_eq>

两个路网结构等效，当且仅当：
- A 和 B 拥有相同数量的直接下游站点，且
- A 的每个直接下游分支可以与 B 的某个直接下游分支一一配对，配对后的分支路网在拓扑上递归等效（忽略分支的绝对顺序）。

- 不允许直接询问“结构是否等效”。如果对不在可见集 V 中的站点提问，或问题格式不符，会返回“无效”。
- 请尽可能少地使用查询次数。

收集足够信息后，请提交最终判定和证据：

**如果等效**，提供一个从 A 的下游路网到 B 的下游路网的节点映射。格式如下：
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

**如果不等效**，提供以下证据之一：
1. 给出某个网络深度 d，两侧在该深度的下游分支数量分布不相等：
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>
2. 给出一对深度相等但直接下游站点数量不等的节点：
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Traffic Network Topology Consistency Analysis" task.

The system has recorded a unidirectional traffic network tree within a region, containing nodes (intersections/stations) {{1..{n}}}. We now focus on two different traffic hubs A={nodeA} and B={nodeB}, whose respective downstream radiating networks are disjoint.

Your goal is: determine whether the downstream radiating network starting from A and the downstream radiating network starting from B are topologically equivalent (i.e., isomorphic as unordered rooted trees).

- Initially, you can only observe hubs A and B (visible set V = {{A, B}}).
- You can only query stations in the visible set V.
- When you execute a CHILDREN (direct downstream stations) query on a station, all its direct downstream stations are added to the visible set V.
- PARENT (upstream source station) queries do not expand the visible set.

1. **COUNT(x)**: Query the number of direct downstream stations of station x. Returns a non-negative integer.
   - Format: <query_count>x</query_count>
2. **CHILDREN(x)**: Query the list of all direct downstream stations of station x.
   - Format: <query_children>x</query_children>
3. **PARENT(x)**: Query the upstream source station ID of x. If there is no upstream source, returns NONE.
   - Format: <query_parent>x</query_parent>
4. **DEPTH_EQ(u,v)**: Check if station u's network depth relative to hub A equals station v's network depth relative to hub B.
   - Format: <query_depth_eq>u,v</query_depth_eq>

Two network structures are equivalent if and only if:
- A and B have the same number of direct downstream stations, and
- Each direct downstream branch of A can be paired one-to-one with some direct downstream branch of B such that the paired branches are recursively equivalent in topology (ignoring the absolute order of branches).

- You cannot directly ask "are structures equivalent". If you query a station not in the visible set V, or the query format is invalid, the response will be "Invalid".
- Please use as few queries as possible.

When you have gathered enough information, please submit your final determination and evidence:

**If equivalent**, provide a node mapping from A's downstream network to B's downstream network. Format:
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

**If not equivalent**, provide one of the following evidences:
1. Give a network depth d where the distribution of downstream branch quantities differs:
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>
2. Give a pair of nodes with equal depth but unequal number of direct downstream stations:
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项“病毒传播链拓扑结构一致性比通”任务。

流行病学调查记录了一个包含 {{1..{n}}} 个感染者的传播链树结构。现在给定两个互不隶属的早期感染者（零号病人） A={nodeA} 和 B={nodeB}，他们各自引发了独立的传播分支。

你的目标是：判定由 A 引发的传播链与由 B 引发的传播链，其感染扩散结构是否等效（即无序根树同构）。

- 初始时，你只能观测到零号病人 A 和 B（可见集 V = {{A, B}}）。
- 你只能对可见集 V 中的感染者进行查询。
- 当你对某感染者执行 CHILDREN（直接下线）查询后，其所有直接传染的下线会被加入可见集 V。
- PARENT（传染源）查询不会扩展可见集。

1. **COUNT(x)**：查询感染者 x 的直接下线数量。返回一个非负整数。
   - 格式：<query_count>x</query_count>
2. **CHILDREN(x)**：查询感染者 x 的所有直接下线列表。
   - 格式：<query_children>x</query_children>
3. **PARENT(x)**：查询感染者 x 的传染源编号。若无传染源则返回 NONE。
   - 格式：<query_parent>x</query_parent>
4. **DEPTH_EQ(u,v)**：判断感染者 u 相对于零号病人 A 的传播代际深度是否等于感染者 v 相对于零号病人 B 的传播代际深度。
   - 格式：<query_depth_eq>u,v</query_depth_eq>

两条传播链等效，当且仅当：
- A 和 B 拥有相同数量的直接下线，且
- A 的每个直接传播分支可以与 B 的某个直接传播分支一一对应，对应后的传播链在拓扑上继续保持等效（忽略感染的时间或登记顺序）。

- 不允许直接询问“传播链是否等效”。如果对不在可见集 V 中的感染者提问，或问题格式不符，会返回“无效”。
- 请尽可能少地使用查询次数。

收集足够信息后，请提交最终判定和证据：

**如果等效**，提供一个从 A 的传播链到 B 的传播链的节点映射。格式如下：
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

**如果不等效**，提供以下证据之一：
1. 给出某个传播代际深度 d，两侧在该深度的下线数量分布不相等：
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>
2. 给出一对传播代际相同但直接下线数量不等的感染者：
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Virus Transmission Chain Topology Consistency Comparison" task.

Epidemiological investigations have recorded a transmission chain tree containing infected individuals {{1..{n}}}. We are now given two early infected individuals (Patient Zeros) A={nodeA} and B={nodeB}, who do not belong to each other's chains and have each triggered independent transmission branches.

Your goal is: determine whether the transmission chain triggered by A and the transmission chain triggered by B are structurally equivalent in their infection spread (i.e., isomorphic as unordered rooted trees).

- Initially, you can only observe Patient Zeros A and B (visible set V = {{A, B}}).
- You can only query individuals in the visible set V.
- When you execute a CHILDREN (direct infectees) query on an individual, all their direct infectees are added to the visible set V.
- PARENT (infector) queries do not expand the visible set.

1. **COUNT(x)**: Query the number of direct infectees of individual x. Returns a non-negative integer.
   - Format: <query_count>x</query_count>
2. **CHILDREN(x)**: Query the list of all direct infectees of individual x.
   - Format: <query_children>x</query_children>
3. **PARENT(x)**: Query the infector ID of individual x. If there is no infector, returns NONE.
   - Format: <query_parent>x</query_parent>
4. **DEPTH_EQ(u,v)**: Check if individual u's transmission generation depth relative to Patient Zero A equals individual v's generation depth relative to Patient Zero B.
   - Format: <query_depth_eq>u,v</query_depth_eq>

Two transmission chains are equivalent if and only if:
- A and B have the same number of direct infectees, and
- Each direct transmission branch of A can be paired one-to-one with some direct transmission branch of B such that the paired chains are recursively equivalent in topology (ignoring the absolute chronological order of infections).

- You cannot directly ask "are transmission chains equivalent". If you query an individual not in the visible set V, or the query format is invalid, the response will be "Invalid".
- Please use as few queries as possible.

When you have gathered enough information, please submit your final determination and evidence:

**If equivalent**, provide a node mapping from A's transmission chain to B's transmission chain. Format:
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

**If not equivalent**, provide one of the following evidences:
1. Give a generation depth d where the distribution of direct infectee quantities differs:
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>
2. Give a pair of individuals with equal depth but unequal number of direct infectees:
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项“学科知识图谱依赖结构比对”的任务。

教务系统构建了一棵包含核心知识点 {{1..{n}}} 的前置依赖树。现在提取出两个不同的基础核心知识点 A={nodeA} 和 B={nodeB}，它们衍生出的进阶知识体系互不重叠。

你的目标是：判定以 A 为前置基础衍生出的知识体系和以 B 为前置基础衍生出的知识体系，在逻辑依赖结构上是否完全一致（即无序根树同构）。

- 初始时，你只能观测到核心知识点 A 和 B（可见集 V = {{A, B}}）。
- 你只能对可见集 V 中的知识点进行查询。
- 当你对某知识点执行 CHILDREN（直接进阶知识点）查询后，其所有直接依赖该知识点的高阶内容会被加入可见集 V。
- PARENT（前置知识点）查询不会扩展可见集。

1. **COUNT(x)**：查询知识点 x 直接支撑的进阶知识点数量。返回一个非负整数。
   - 格式：<query_count>x</query_count>
2. **CHILDREN(x)**：查询依赖知识点 x 的所有直接进阶知识点列表。
   - 格式：<query_children>x</query_children>
3. **PARENT(x)**：查询知识点 x 的直接前置基础知识点编号。若无前置则返回 NONE。
   - 格式：<query_parent>x</query_parent>
4. **DEPTH_EQ(u,v)**：判断知识点 u 相对于基础知识点 A 的进阶层级深度是否等于知识点 v 相对于基础知识点 B 的进阶层级深度。
   - 格式：<query_depth_eq>u,v</query_depth_eq>

两个知识体系结构等效，当且仅当：
- A 和 B 支撑了相同数量的直接进阶知识点，且
- A 的每个进阶分支可以与 B 的某个进阶分支一一配对，配对后的分支依赖图谱在拓扑上继续保持等效（不考虑知识点展示顺序）。

- 不允许直接询问“知识结构是否等效”。如果对不在可见集 V 中的知识点提问，或问题格式不符，会返回“无效”。
- 请尽可能少地使用查询次数。

收集足够信息后，请提交最终判定和证据：

**如果等效**，提供一个从 A 的知识体系到 B 的知识体系的节点映射。格式如下：
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

**如果不等效**，提供以下证据之一：
1. 给出某个进阶层级深度 d，两侧在该深度的支撑数量分布不相等：
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>
2. 给出一对进阶层级相同但直接支撑的进阶知识点数量不等的节点：
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Subject Knowledge Graph Dependency Structure Comparison" task.

The academic system has built a prerequisite dependency tree containing core knowledge points {{1..{n}}}. We now extract two different foundational knowledge points A={nodeA} and B={nodeB}, whose derived advanced knowledge structures do not overlap.

Your goal is: determine whether the knowledge structure derived from foundation A and the knowledge structure derived from foundation B are completely consistent in their logical dependency structure (i.e., isomorphic as unordered rooted trees).

- Initially, you can only observe core knowledge points A and B (visible set V = {{A, B}}).
- You can only query knowledge points in the visible set V.
- When you execute a CHILDREN (direct advanced knowledge points) query on a point, all higher-level concepts directly depending on it are added to the visible set V.
- PARENT (prerequisite knowledge point) queries do not expand the visible set.

1. **COUNT(x)**: Query the number of advanced knowledge points directly supported by x. Returns a non-negative integer.
   - Format: <query_count>x</query_count>
2. **CHILDREN(x)**: Query the list of all direct advanced knowledge points depending on x.
   - Format: <query_children>x</query_children>
3. **PARENT(x)**: Query the direct prerequisite foundation ID of x. If there is no prerequisite, returns NONE.
   - Format: <query_parent>x</query_parent>
4. **DEPTH_EQ(u,v)**: Check if knowledge point u's advancement level depth relative to foundation A equals knowledge point v's advancement level depth relative to foundation B.
   - Format: <query_depth_eq>u,v</query_depth_eq>

Two knowledge structures are equivalent if and only if:
- A and B support the same number of direct advanced knowledge points, and
- Each advanced branch of A can be paired one-to-one with some advanced branch of B such that the paired dependency graphs are recursively equivalent in topology (ignoring the display order of knowledge points).

- You cannot directly ask "are knowledge structures equivalent". If you query a knowledge point not in the visible set V, or the query format is invalid, the response will be "Invalid".
- Please use as few queries as possible.

When you have gathered enough information, please submit your final determination and evidence:

**If equivalent**, provide a node mapping from A's knowledge structure to B's knowledge structure. Format:
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

**If not equivalent**, provide one of the following evidences:
1. Give an advancement level depth d where the distribution of supported concept quantities differs:
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>
2. Give a pair of points with equal depth but unequal number of directly supported advanced knowledge points:
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项“产品 BOM (物料清单) 分解结构一致性核查”的任务。

系统中存储了一套包含 {{1..{n}}} 个零部件的装配分解树。现在锁定两个不同的核心总成件 A={nodeA} 和 B={nodeB}，它们各自向下拆解的子级物料互不通用。

你的目标是：判定总成件 A 的底层拆解装配结构与总成件 B 的拆解装配结构是否等效（即无序根树同构），以评估它们的产线替代性。

- 初始时，你只能观测到核心总成件 A 和 B（可见集 V = {{A, B}}）。
- 你只能对可见集 V 中的零部件进行查询。
- 当你对某零部件执行 CHILDREN（直接子件）查询后，其所有直接组成的下级物料会被加入可见集 V。
- PARENT（所属父组件）查询不会扩展可见集。

1. **COUNT(x)**：查询零部件 x 包含的直接下级子件种类数量。返回一个非负整数。
   - 格式：<query_count>x</query_count>
2. **CHILDREN(x)**：查询组成零部件 x 的所有直接子件列表。
   - 格式：<query_children>x</query_children>
3. **PARENT(x)**：查询零部件 x 所属的直接父组件编号。若为顶层件则返回 NONE。
   - 格式：<query_parent>x</query_parent>
4. **DEPTH_EQ(u,v)**：判断零部件 u 相对于总成件 A 的拆解层级深度是否等于零部件 v 相对于总成件 B 的拆解层级深度。
   - 格式：<query_depth_eq>u,v</query_depth_eq>

两套装配结构等效，当且仅当：
- A 和 B 包含相同数量的直接子件种类，且
- A 的每个子件拆解分支可以与 B 的某个子件拆解分支一一配对，配对后的装配逻辑在拓扑上继续保持等效（忽略子件清单的排列顺序）。

- 不允许直接询问“装配结构是否等效”。如果对不在可见集 V 中的零部件提问，或问题格式不符，会返回“无效”。
- 请尽可能少地使用查询次数。

收集足够信息后，请提交最终判定和证据：

**如果等效**，提供一个从 A 的装配树到 B 的装配树的节点映射。格式如下：
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

**如果不等效**，提供以下证据之一：
1. 给出某个拆解层级深度 d，两侧在该深度的子件构成数量分布不相等：
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>
2. 给出一对拆解层级相同但直接包含下级子件数量不等的零部件：
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct a "Product BOM (Bill of Materials) Breakdown Structure Consistency Check" task.

The system stores an assembly breakdown tree containing components {{1..{n}}}. We now target two different core assemblies A={nodeA} and B={nodeB}, whose downwardly broken-down sub-materials are mutually exclusive.

Your goal is: determine whether the low-level breakdown assembly structure of assembly A is equivalent to that of assembly B (i.e., isomorphic as unordered rooted trees), to evaluate their production line substitutability.

- Initially, you can only observe core assemblies A and B (visible set V = {{A, B}}).
- You can only query components in the visible set V.
- When you execute a CHILDREN (direct sub-components) query on a component, all sub-materials directly composing it are added to the visible set V.
- PARENT (parent assembly) queries do not expand the visible set.

1. **COUNT(x)**: Query the number of direct sub-component types contained in component x. Returns a non-negative integer.
   - Format: <query_count>x</query_count>
2. **CHILDREN(x)**: Query the list of all direct sub-components comprising component x.
   - Format: <query_children>x</query_children>
3. **PARENT(x)**: Query the direct parent assembly ID to which component x belongs. If it is a top-level component, returns NONE.
   - Format: <query_parent>x</query_parent>
4. **DEPTH_EQ(u,v)**: Check if component u's breakdown level depth relative to assembly A equals component v's breakdown level depth relative to assembly B.
   - Format: <query_depth_eq>u,v</query_depth_eq>

Two assembly structures are equivalent if and only if:
- A and B contain the same number of direct sub-component types, and
- Each sub-component breakdown branch of A can be paired one-to-one with some sub-component breakdown branch of B such that the paired assembly logics are recursively equivalent in topology (ignoring the arrangement order of sub-components).

- You cannot directly ask "are assembly structures equivalent". If you query a component not in the visible set V, or the query format is invalid, the response will be "Invalid".
- Please use as few queries as possible.

When you have gathered enough information, please submit your final determination and evidence:

**If equivalent**, provide a node mapping from A's assembly tree to B's assembly tree. Format:
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

**If not equivalent**, provide one of the following evidences:
1. Give a breakdown level depth d where the distribution of sub-component quantities differs:
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>
2. Give a pair of components with equal depth but unequal number of direct sub-components:
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项“涉案资金洗钱网络拓扑一致性分析”的任务。

经侦部门梳理了一张包含 {{1..{n}}} 个涉案实体的单向资金流转树。现在锁定两个无直接关联的源头嫌疑实体 A={nodeA} 和 B={nodeB}，它们向外分发资金的下游网络没有交集。

你的目标是：判定以 A 为源头的资金分发网络与以 B 为源头的资金分发网络，在洗钱隐匿拓扑结构上是否完全一致（即无序根树同构）。

- 初始时，你只能观测到源头实体 A 和 B（可见集 V = {{A, B}}）。
- 你只能对可见集 V 中的实体进行查询。
- 当你对某实体执行 CHILDREN（资金直接流入实体）查询后，所有接收其资金的直接下游实体会被加入可见集 V。
- PARENT（资金来源实体）查询不会扩展可见集。

1. **COUNT(x)**：查询接收实体 x 资金的直接下游实体数量。返回一个非负整数。
   - 格式：<query_count>x</query_count>
2. **CHILDREN(x)**：查询接收实体 x 资金的所有直接下游实体列表。
   - 格式：<query_children>x</query_children>
3. **PARENT(x)**：查询向实体 x 汇入资金的直接上游实体编号。若无上游则返回 NONE。
   - 格式：<query_parent>x</query_parent>
4. **DEPTH_EQ(u,v)**：判断实体 u 相对于源头 A 的资金流转层级深度是否等于实体 v 相对于源头 B 的资金流转层级深度。
   - 格式：<query_depth_eq>u,v</query_depth_eq>

两个资金网络等效，当且仅当：
- A 和 B 向相同数量的直接下游实体分发了资金，且
- A 的每个下游洗钱分支可以与 B 的某个下游洗钱分支一一对应，对应后的流转网络在拓扑上继续保持等效（不考虑资金划转的时间先后）。

- 不允许直接询问“网络结构是否一致”。如果对不在可见集 V 中的实体提问，或问题格式不符，会返回“无效”。
- 请尽可能少地使用查询次数。

收集足够信息后，请提交最终判定和证据：

**如果等效**，提供一个从 A 的资金网络到 B 的资金网络的节点映射。格式如下：
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

**如果不等效**，提供以下证据之一：
1. 给出某个资金流转层级 d，两侧在该层级的下游分发数量分布不相等：
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>
2. 给出一对流转层级相同但直接下游分发数量不等的实体：
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct an "Illicit Fund Laundering Network Topology Consistency Analysis" task.

The economic crime investigation department has charted a unidirectional fund transfer tree containing entities {{1..{n}}}. We now target two source suspect entities A={nodeA} and B={nodeB} with no direct correlation, and their outward fund distribution networks have no intersection.

Your goal is: determine whether the fund distribution network originating from A and the fund distribution network originating from B are completely consistent in their laundering concealment topology (i.e., isomorphic as unordered rooted trees).

- Initially, you can only observe source entities A and B (visible set V = {{A, B}}).
- You can only query entities in the visible set V.
- When you execute a CHILDREN (direct downstream fund-receiving entities) query on an entity, all direct downstream entities receiving its funds are added to the visible set V.
- PARENT (upstream funding entity) queries do not expand the visible set.

1. **COUNT(x)**: Query the number of direct downstream entities receiving funds from entity x. Returns a non-negative integer.
   - Format: <query_count>x</query_count>
2. **CHILDREN(x)**: Query the list of all direct downstream entities receiving funds from entity x.
   - Format: <query_children>x</query_children>
3. **PARENT(x)**: Query the direct upstream entity ID that remitted funds to entity x. If there is no upstream source, returns NONE.
   - Format: <query_parent>x</query_parent>
4. **DEPTH_EQ(u,v)**: Check if entity u's fund transfer layer depth relative to source A equals entity v's fund transfer layer depth relative to source B.
   - Format: <query_depth_eq>u,v</query_depth_eq>

Two fund networks are equivalent if and only if:
- A and B distributed funds to the same number of direct downstream entities, and
- Each downstream laundering branch of A can be paired one-to-one with some downstream laundering branch of B such that the paired transfer networks are recursively equivalent in topology (ignoring the chronological order of fund transfers).

- You cannot directly ask "are network structures equivalent". If you query an entity not in the visible set V, or the query format is invalid, the response will be "Invalid".
- Please use as few queries as possible.

When you have gathered enough information, please submit your final determination and evidence:

**If equivalent**, provide a node mapping from A's fund network to B's fund network. Format:
<answer>isomorphic=yes, mapping=1:5,2:6,3:7</answer>

**If not equivalent**, provide one of the following evidences:
1. Give a fund transfer layer depth d where the distribution of downstream dispatch quantities differs:
<answer>isomorphic=no, evidence=depth_degree, depth=2, degrees_A=1,1,2, degrees_B=1,2,2</answer>
2. Give a pair of entities with equal depth but unequal number of direct downstream entities:
<answer>isomorphic=no, evidence=node_pair, node_A=3, node_B=8, count_A=2, count_B=1</answer>
"""

    tags = ["answer", "query_count", "query_children", "query_parent", "query_depth_eq"]
    
    reasoning_type = "演绎推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "tree": {
                    1: [], 
                    2: [1], 3: [1],
                    4: [2], 5: [2],
                    6: [], 
                    7: [6],
                },
                "nodeA": 1,
                "nodeB": 6,
                "is_isomorphic": False,
                "expected_mapping": None,
            },
            2: {
                "n": 9,
                "tree": {
                    1: [], 2: [1], 3: [1], 4: [2], 5: [3],
                    6: [], 7: [6], 8: [6], 9: [7],
                },
                "nodeA": 1,
                "nodeB": 6,
                "is_isomorphic": True,
                "expected_mapping": {1: 6, 2: 7, 3: 8, 4: 9, 5: -1},
            },
            3: {
                "n": 11,
                "tree": {
                    1: [], 2: [1], 3: [1], 4: [2], 5: [2], 6: [3],
                    7: [], 8: [7], 9: [7], 10: [8], 11: [9],
                },
                "nodeA": 1,
                "nodeB": 7,
                "is_isomorphic": True,
                "expected_mapping": {1: 7, 2: 9, 3: 8, 4: 11, 5: -1, 6: 10},
            },
            4: {
                "n": 13,
                "tree": {
                    1: [], 2: [1], 3: [1], 4: [1], 5: [2], 6: [2], 7: [3], 8: [4],
                    9: [], 10: [9], 11: [9], 12: [9], 13: [10],
                },
                "nodeA": 1,
                "nodeB": 9,
                "is_isomorphic": False,
                "expected_mapping": None,
            },
            5: {
                "n": 15,
                "tree": {
                    1: [], 2: [1], 3: [1], 4: [2], 5: [2], 6: [3], 7: [3], 8: [4], 9: [5],
                    10: [], 11: [10], 12: [10], 13: [11], 14: [11], 15: [12],
                },
                "nodeA": 1,
                "nodeB": 10,
                "is_isomorphic": True,
                "expected_mapping": {1: 10, 2: 11, 3: 12, 4: 13, 5: 14, 6: 15, 7: -1, 8: -1, 9: -1},
            },
        },
        "en": {
            1: {
                "n": 7,
                "tree": {
                    1: [], 2: [1], 3: [1], 4: [2], 5: [2],
                    6: [], 7: [6],
                },
                "nodeA": 1,
                "nodeB": 6,
                "is_isomorphic": False,
                "expected_mapping": None,
            },
            2: {
                "n": 9,
                "tree": {
                    1: [], 2: [1], 3: [1], 4: [2], 5: [3],
                    6: [], 7: [6], 8: [6], 9: [7],
                },
                "nodeA": 1,
                "nodeB": 6,
                "is_isomorphic": True,
                "expected_mapping": {1: 6, 2: 7, 3: 8, 4: 9, 5: -1},
            },
            3: {
                "n": 11,
                "tree": {
                    1: [], 2: [1], 3: [1], 4: [2], 5: [2], 6: [3],
                    7: [], 8: [7], 9: [7], 10: [8], 11: [9],
                },
                "nodeA": 1,
                "nodeB": 7,
                "is_isomorphic": True,
                "expected_mapping": {1: 7, 2: 9, 3: 8, 4: 11, 5: -1, 6: 10},
            },
            4: {
                "n": 13,
                "tree": {
                    1: [], 2: [1], 3: [1], 4: [1], 5: [2], 6: [2], 7: [3], 8: [4],
                    9: [], 10: [9], 11: [9], 12: [9], 13: [10],
                },
                "nodeA": 1,
                "nodeB": 9,
                "is_isomorphic": False,
                "expected_mapping": None,
            },
            5: {
                "n": 15,
                "tree": {
                    1: [], 2: [1], 3: [1], 4: [2], 5: [2], 6: [3], 7: [3], 8: [4], 9: [5],
                    10: [], 11: [10], 12: [10], 13: [11], 14: [11], 15: [12],
                },
                "nodeA": 1,
                "nodeB": 10,
                "is_isomorphic": True,
                "expected_mapping": {1: 10, 2: 11, 3: 12, 4: 13, 5: 14, 6: 15, 7: -1, 8: -1, 9: -1},
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
        self._game_info["nodeA"] = cfg["nodeA"]
        self._game_info["nodeB"] = cfg["nodeB"]

        self.parent_map = {}
        self.children_map = {}
        
        for node, parents in cfg["tree"].items():
            if len(parents) == 0:
                self.parent_map[node] = None
            else:
                self.parent_map[node] = parents[0]
        
        for node in self.parent_map:
            self.children_map[node] = []
        
        for node, parent in self.parent_map.items():
            if parent is not None:
                self.children_map[parent].append(node)
        
        for node in self.children_map:
            self.children_map[node].sort()
        
        self.nodeA = cfg["nodeA"]
        self.nodeB = cfg["nodeB"]
        self.is_isomorphic = cfg["is_isomorphic"]
        
        self.visible_set = {self.nodeA, self.nodeB}
        
        self.query_history = []

    def _get_subtree_nodes(self, root):
        nodes = {root}
        queue = [root]
        while queue:
            curr = queue.pop(0)
            for child in self.children_map.get(curr, []):
                nodes.add(child)
                queue.append(child)
        return nodes

    def _is_in_subtree(self, node, root):
        return node in self._get_subtree_nodes(root)

    def _get_depth(self, node, root):
        if node == root:
            return 0
        depth = 0
        curr = node
        while curr != root and curr is not None:
            curr = self.parent_map.get(curr)
            depth += 1
            if depth > 1000:
                return -1
        if curr == root:
            return depth
        return -1

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            iso_match = re.search(r'isomorphic\s*=\s*(yes|no)', raw_ans, re.IGNORECASE)
            if not iso_match:
                return False
            
            is_iso_claim = iso_match.group(1).lower() == "yes"
            
            if is_iso_claim != self.is_isomorphic:
                return False
            
            if is_iso_claim:
                mapping_match = re.search(r'mapping\s*=\s*([0-9,:\s]+)', raw_ans)
                if not mapping_match:
                    return False
                
                mapping_str = mapping_match.group(1).strip()
                mapping = {}
                for pair in mapping_str.split(','):
                    pair = pair.strip()
                    if ':' not in pair:
                        continue
                    parts = pair.split(':')
                    if len(parts) != 2:
                        continue
                    a_node, b_node = int(parts[0].strip()), int(parts[1].strip())
                    mapping[a_node] = b_node
                
                subtree_a = self._get_subtree_nodes(self.nodeA)
                subtree_b = self._get_subtree_nodes(self.nodeB)
                
                if mapping.get(self.nodeA) != self.nodeB:
                    return False
                
                if set(mapping.keys()) != subtree_a:
                    return False
                
                if set(mapping.values()) != subtree_b:
                    return False
                
                if len(set(mapping.values())) != len(mapping):
                    return False
                
                for node_a in subtree_a:
                    node_b = mapping[node_a]
                    children_a = self.children_map.get(node_a, [])
                    children_b = self.children_map.get(node_b, [])
                    
                    if len(children_a) != len(children_b):
                        return False
                    
                    mapped_children = sorted([mapping[c] for c in children_a])
                    if mapped_children != sorted(children_b):
                        return False
                
                return True
            else:
                evidence_match = re.search(r'evidence\s*=\s*(\w+)', raw_ans)
                if not evidence_match:
                    return False
                
                evidence_type = evidence_match.group(1)
                
                if evidence_type == "depth_degree":
                    depth_match = re.search(r'depth\s*=\s*(\d+)', raw_ans)
                    degrees_a_match = re.search(r'degrees_A\s*=\s*([\d,]+)', raw_ans)
                    degrees_b_match = re.search(r'degrees_B\s*=\s*([\d,]+)', raw_ans)
                    if not (depth_match and degrees_a_match and degrees_b_match):
                        return False
                    deg_a = sorted([int(x.strip()) for x in degrees_a_match.group(1).split(',')])
                    deg_b = sorted([int(x.strip()) for x in degrees_b_match.group(1).split(',')])
                    if deg_a == deg_b:
                        return False
                    return True
                elif evidence_type == "node_pair":
                    na_match = re.search(r'node_A\s*=\s*(\d+)', raw_ans)
                    nb_match = re.search(r'node_B\s*=\s*(\d+)', raw_ans)
                    ca_match = re.search(r'count_A\s*=\s*(\d+)', raw_ans)
                    cb_match = re.search(r'count_B\s*=\s*(\d+)', raw_ans)
                    if not (na_match and nb_match and ca_match and cb_match):
                        return False
                    na = int(na_match.group(1))
                    nb = int(nb_match.group(1))
                    ca = int(ca_match.group(1))
                    cb = int(cb_match.group(1))
                    actual_ca = len(self.children_map.get(na, []))
                    actual_cb = len(self.children_map.get(nb, []))
                    if actual_ca != ca or actual_cb != cb:
                        return False
                    if ca == cb:
                        return False
                    return True
                else:
                    return False
                    
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        invalid_msg = "Invalid" if lang == "en" else "无效"
        yes_msg = "Yes" if lang == "en" else "是"
        no_msg = "No" if lang == "en" else "否"
        
        if "query_count" in parsed_info:
            try:
                node = int(parsed_info["query_count"].strip())
                if node not in self.visible_set:
                    return invalid_msg
                count = len(self.children_map.get(node, []))
                self.query_history.append(f"COUNT({node})={count}")
                return str(count)
            except:
                return invalid_msg
        
        elif "query_children" in parsed_info:
            try:
                node = int(parsed_info["query_children"].strip())
                if node not in self.visible_set:
                    return invalid_msg
                children = self.children_map.get(node, [])
                for child in children:
                    self.visible_set.add(child)
                self.query_history.append(f"CHILDREN({node})={children}")
                if len(children) == 0:
                    return "[]" if lang == "en" else "[]"
                return str(children)
            except:
                return invalid_msg
        
        elif "query_parent" in parsed_info:
            try:
                node = int(parsed_info["query_parent"].strip())
                if node not in self.visible_set:
                    return invalid_msg
                parent = self.parent_map.get(node)
                self.query_history.append(f"PARENT({node})={parent}")
                if parent is None:
                    return "NONE"
                return str(parent)
            except:
                return invalid_msg
        
        elif "query_depth_eq" in parsed_info:
            try:
                nodes_str = parsed_info["query_depth_eq"].strip()
                u, v = [int(x.strip()) for x in nodes_str.split(',')]
                
                if u not in self.visible_set or v not in self.visible_set:
                    return invalid_msg
                
                in_a = self._is_in_subtree(u, self.nodeA)
                in_b = self._is_in_subtree(v, self.nodeB)
                
                if not in_a or not in_b:
                    return invalid_msg
                
                depth_u = self._get_depth(u, self.nodeA)
                depth_v = self._get_depth(v, self.nodeB)
                
                if depth_u == -1 or depth_v == -1:
                    return invalid_msg
                
                result = yes_msg if depth_u == depth_v else no_msg
                self.query_history.append(f"DEPTH_EQ({u},{v})={result}")
                return result
            except:
                return invalid_msg
        
        else:
            return invalid_msg

    def get_all_possible_queries(self) -> list[dict]:
        original_visible = self.visible_set.copy()
        original_history = list(self.query_history)

        queries = []
        
        try:
            nodes_a = self._get_subtree_nodes(self.nodeA)
            nodes_b = self._get_subtree_nodes(self.nodeB)
            all_nodes = nodes_a.union(nodes_b)

            for node in all_nodes:
                self.visible_set = original_visible.union({node})
                q_tag = "query_count"
                q_content = str(node)
                parsed = {q_tag: q_content}
                ans = self._cf_core_produce(parsed)
                queries.append({
                    "query": f"<{q_tag}>{q_content}</{q_tag}>",
                    "answer": ans
                })

                self.visible_set = original_visible.union({node})
                q_tag = "query_children"
                q_content = str(node)
                parsed = {q_tag: q_content}
                ans = self._cf_core_produce(parsed)
                queries.append({
                    "query": f"<{q_tag}>{q_content}</{q_tag}>",
                    "answer": ans
                })

                self.visible_set = original_visible.union({node})
                q_tag = "query_parent"
                q_content = str(node)
                parsed = {q_tag: q_content}
                ans = self._cf_core_produce(parsed)
                queries.append({
                    "query": f"<{q_tag}>{q_content}</{q_tag}>",
                    "answer": ans
                })

            for u in nodes_a:
                for v in nodes_b:
                    self.visible_set = original_visible.union({u, v})
                    q_tag = "query_depth_eq"
                    q_content = f"{u},{v}"
                    parsed = {q_tag: q_content}
                    ans = self._cf_core_produce(parsed)
                    queries.append({
                        "query": f"<{q_tag}>{q_content}</{q_tag}>",
                        "answer": ans
                    })
                    
        finally:
            self.visible_set = original_visible
            self.query_history = original_history

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        lang = self.config.language
        yes_msg = "Yes" if lang == "en" else "是"
        no_msg = "No" if lang == "en" else "否"

        if correct.strip() == yes_msg:
            return no_msg
        if correct.strip() == no_msg:
            return yes_msg

        try:
            num = int(correct.strip())
            return str(num + 1)
        except ValueError:
            pass

        if correct.strip() == "NONE":
            return "999"

        if correct.strip().startswith("["):
            return "[]"

        return correct + " (corrupted)"