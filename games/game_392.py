from .base import Game
import re

class TreePathRecoveryGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树路径恢复"的推理游戏，规则如下：

游戏设定了一棵未知的无向连通无环图（树），共有 {n} 个节点，编号为 1 到 {n}。我已秘密构造了这棵树的结构，并指定了两个特殊节点：起点 S = {s} 和终点 T = {t}。

你的目标是推断出从 S 到 T 的唯一路径上的所有节点序列（按从 S 到 T 的顺序）。你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的树结构如实回答：

1. 路径长度查询：询问节点 a 和 b 之间的路径长度（边数）。回答一个非负整数。
2. 路径成员查询：询问节点 c 是否在节点 a 和 b 之间的路径上（包含端点）。回答"是"或"否"。
3. 路径顺序查询：询问在节点 a 到 b 的路径上，节点 c 和 d 的相对顺序。回答以下之一：
   - "c先"：c 和 d 都在路径上，从 a 到 b 方向先遇到 c
   - "d先"：c 和 d 都在路径上，从 a 到 b 方向先遇到 d
   - "仅c在路径上"：只有 c 在路径上
   - "仅d在路径上"：只有 d 在路径上
   - "都不在"：c 和 d 都不在路径上
   - "并列"：c 和 d 是同一个节点且在路径上
4. 路径交集查询：询问路径 (a, b) 和路径 (c, d) 有多少个公共节点。回答一个非负整数。

当你收集足够信息后，请提交最终答案。你应该尽可能少地使用查询次数。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 路径长度查询（例如查询节点 1 和 5 之间的距离）：
<query_length>1,5</query_length>

- 路径成员查询（例如查询节点 3 是否在节点 1 和 5 的路径上）：
<query_member>1,5,3</query_member>

- 路径顺序查询（例如查询在节点 1 和 5 的路径上，节点 2 和 3 的相对顺序）：
<query_order>1,5,2,3</query_order>

- 路径交集查询（例如查询路径 (1,5) 和路径 (2,6) 的公共节点数）：
<query_intersection>1,5,2,6</query_intersection>

提交最终答案时，必须给出从 S 到 T 的完整路径节点序列（用逗号隔开），格式如下：

<answer>{s},...,{t}</answer>

例如，如果从 S={s} 到 T={t} 的路径经过节点 x, y，则提交：
<answer>{s},x,y,{t}</answer>

注意：答案必须以 S 开始，以 T 结束，且包含所有中间节点，相邻节点之间必须有边相连。
"""

    game_rule_en = """\
Let's play a "Tree Path Recovery" deduction game. Here are the rules:

The game involves an unknown undirected connected acyclic graph (tree) with {n} nodes, numbered from 1 to {n}. I have secretly constructed the tree structure and designated two special nodes: start node S = {s} and end node T = {t}.

Your goal is to infer the complete sequence of nodes on the unique path from S to T (in order from S to T). You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the real tree structure:

1. Path Length Query: Ask for the path length (number of edges) between nodes a and b. Answer is a non-negative integer.
2. Path Membership Query: Ask whether node c is on the path between nodes a and b (including endpoints). Answer "Yes" or "No".
3. Path Order Query: Ask about the relative order of nodes c and d on the path from a to b. Answer one of:
   - "c first": both c and d are on the path, c is encountered first from a to b
   - "d first": both c and d are on the path, d is encountered first from a to b
   - "only c on path": only c is on the path
   - "only d on path": only d is on the path
   - "neither on path": neither c nor d is on the path
   - "tied": c and d are the same node and on the path
4. Path Intersection Query: Ask how many common nodes paths (a, b) and (c, d) share. Answer is a non-negative integer.

When you have gathered enough information, submit your final answer. You should use as few queries as possible. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Path Length Query (e.g., querying distance between nodes 1 and 5):
<query_length>1,5</query_length>

- Path Membership Query (e.g., querying if node 3 is on the path between nodes 1 and 5):
<query_member>1,5,3</query_member>

- Path Order Query (e.g., querying the relative order of nodes 2 and 3 on the path from 1 to 5):
<query_order>1,5,2,3</query_order>

- Path Intersection Query (e.g., querying the number of common nodes between paths (1,5) and (2,6)):
<query_intersection>1,5,2,6</query_intersection>

When submitting the final answer, provide the complete path node sequence from S to T (comma-separated), in this format:

<answer>{s},...,{t}</answer>

For example, if the path from S={s} to T={t} passes through nodes x and y, submit:
<answer>{s},x,y,{t}</answer>

Note: The answer must start with S and end with T, including all intermediate nodes, with adjacent nodes connected by edges.
"""

    contextualized_rule_zh_1 = """\
[交通场景] 欢迎参与“秘密物流专线”规划系统。

系统设定了一张未知的树状物流网络（无向连通无环图），共有 {n} 个集散中心，编号为 1 到 {n}。我已秘密构造了该网络结构，并指定了专线的起点集散中心 S = {s} 和终点集散中心 T = {t}。

你的目标是推断出从 S 到 T 的唯一专线上的所有集散中心序列（按流转顺序）。你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的物流网络如实回答：

1. 路径长度查询：询问集散中心 a 和 b 之间的中转跳数（边数）。回答一个非负整数。
2. 路径成员查询：询问集散中心 c 是否在 a 和 b 之间的专线上（包含端点）。回答"是"或"否"。
3. 路径顺序查询：询问在集散中心 a 到 b 的专线上，c 和 d 的相对途经顺序。回答以下之一：
   - "c先"：c 和 d 都在专线上，从 a 到 b方向先途经 c
   - "d先"：c 和 d 都在专线上，从 a 到 b方向先途经 d
   - "仅c在路径上"：只有 c 在专线上
   - "仅d在路径上"：只有 d 在专线上
   - "都不在"：c 和 d 都不在专线上
   - "并列"：c 和 d 是同一个集散中心且在专线上
4. 路径交集查询：询问专线 (a, b) 和专线 (c, d) 有多少个公共集散中心。回答一个非负整数。

当你收集足够信息后，请提交最终答案。你应该尽可能少地使用查询次数。若答案错误或格式不符，规划任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 路径长度查询（例如查询集散中心 1 和 5 之间的距离）：
<query_length>1,5</query_length>

- 路径成员查询（例如查询集散中心 3 是否在 1 和 5 的专线上）：
<query_member>1,5,3</query_member>

- 路径顺序查询（例如查询在 1 和 5 的专线上，2 和 3 的相对顺序）：
<query_order>1,5,2,3</query_order>

- 路径交集查询（例如查询专线 (1,5) 和专线 (2,6) 的公共节点数）：
<query_intersection>1,5,2,6</query_intersection>

提交最终答案时，必须给出从 S 到 T 的完整物流节点序列（用逗号隔开），格式如下：

<answer>{s},...,{t}</answer>

例如，如果从 S={s} 到 T={t} 的路径经过 x, y，则提交：
<answer>{s},x,y,{t}</answer>

注意：答案必须以 S 开始，以 T 结束，且包含所有中间节点，相邻集散中心之间必须有真实网段相连。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario] Welcome to the "Secret Logistics Route" planning system.

The game involves an unknown tree-structured logistics network (undirected connected acyclic graph) with {n} distribution centers, numbered from 1 to {n}. I have secretly constructed the network and designated two special centers: origin S = {s} and destination T = {t}.

Your goal is to infer the complete sequence of centers on the unique route from S to T (in order of transit). You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the actual network:

1. Path Length Query: Ask for the number of transit hops (edges) between center a and b. Answer is a non-negative integer.
2. Path Membership Query: Ask whether center c is on the route between a and b (including endpoints). Answer "Yes" or "No".
3. Path Order Query: Ask about the relative transit order of centers c and d on the route from a to b. Answer one of:
   - "c first": both c and d are on the route, c is encountered first from a to b
   - "d first": both c and d are on the route, d is encountered first from a to b
   - "only c on path": only c is on the route
   - "only d on path": only d is on the route
   - "neither on path": neither c nor d is on the route
   - "tied": c and d are the same center and on the route
4. Path Intersection Query: Ask how many common centers routes (a, b) and (c, d) share. Answer is a non-negative integer.

When you have gathered enough information, submit your final answer. You should use as few queries as possible. If the answer is wrong or the format is invalid, the planning task fails.

Each query must contain only one tag. Use the following XML format:

- Path Length Query (e.g., querying transit distance between centers 1 and 5):
<query_length>1,5</query_length>

- Path Membership Query (e.g., querying if center 3 is on the route between 1 and 5):
<query_member>1,5,3</query_member>

- Path Order Query (e.g., querying the relative order of centers 2 and 3 on the route from 1 to 5):
<query_order>1,5,2,3</query_order>

- Path Intersection Query (e.g., querying the number of shared centers between routes (1,5) and (2,6)):
<query_intersection>1,5,2,6</query_intersection>

When submitting the final answer, provide the complete distribution center sequence from S to T (comma-separated), in this format:

<answer>{s},...,{t}</answer>

For example, if the path from S={s} to T={t} passes through x and y, submit:
<answer>{s},x,y,{t}</answer>

Note: The answer must start with S and end with T, including all intermediate nodes, with adjacent centers directly connected by transit links.
"""

    contextualized_rule_zh_2 = """\
[医疗场景] 欢迎参与“分级诊疗网络”推演系统。

系统设定了一张未知的树状分级诊疗网络（无向连通无环图），共有 {n} 家医疗机构，编号为 1 到 {n}。我已秘密构造了该转诊网络结构，并指定了患者转诊的初始接诊机构 S = {s} 和最终确诊机构 T = {t}。

你的目标是推断出从 S 到 T 的唯一转诊通道上的所有医疗机构序列（按转诊顺次）。你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的医疗网络如实回答：

1. 路径长度查询：询问医疗机构 a 和 b 之间的转诊跳数（边数）。回答一个非负整数。
2. 路径成员查询：询问医疗机构 c 是否在 a 和 b 之间的转诊通道上（包含端点）。回答"是"或"否"。
3. 路径顺序查询：询问在医疗机构 a 到 b 的转诊通道上，c 和 d 的相对先后顺序。回答以下之一：
   - "c先"：c 和 d 都在通道上，从 a 到 b 方向先转诊至 c
   - "d先"：c 和 d 都在通道上，从 a 到 b 方向先转诊至 d
   - "仅c在路径上"：只有 c 在通道上
   - "仅d在路径上"：只有 d 在通道上
   - "都不在"：c 和 d 都不在通道上
   - "并列"：c 和 d 是同一家医疗机构且在通道上
4. 路径交集查询：询问转诊通道 (a, b) 和转诊通道 (c, d) 有多少家公共医疗机构。回答一个非负整数。

当你收集足够信息后，请提交最终答案。你应该尽可能少地使用查询次数。若答案错误或格式不符，推演任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 路径长度查询（例如查询机构 1 和 5 之间的距离）：
<query_length>1,5</query_length>

- 路径成员查询（例如查询机构 3 是否在 1 和 5 的通道上）：
<query_member>1,5,3</query_member>

- 路径顺序查询（例如查询在 1 和 5 的通道上，2 和 3 的相对顺序）：
<query_order>1,5,2,3</query_order>

- 路径交集查询（例如查询通道 (1,5) 和通道 (2,6) 的公共节点数）：
<query_intersection>1,5,2,6</query_intersection>

提交最终答案时，必须给出从 S 到 T 的完整医疗机构序列（用逗号隔开），格式如下：

<answer>{s},...,{t}</answer>

例如，如果从 S={s} 到 T={t} 的路径经过 x, y，则提交：
<answer>{s},x,y,{t}</answer>

注意：答案必须以 S 开始，以 T 结束，且包含所有中间节点，相邻医疗机构之间必须有直接的转诊关联。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario] Welcome to the "Hierarchical Referral Network" deduction system.

The game involves an unknown tree-structured medical referral network (undirected connected acyclic graph) with {n} medical facilities, numbered from 1 to {n}. I have secretly constructed the network structure and designated two special facilities: initial primary clinic S = {s} and final specialized hospital T = {t}.

Your goal is to infer the complete sequence of facilities on the unique referral pathway from S to T (in order of patient transfer). You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the actual medical network:

1. Path Length Query: Ask for the number of referral steps (edges) between facility a and b. Answer is a non-negative integer.
2. Path Membership Query: Ask whether facility c is on the referral pathway between a and b (including endpoints). Answer "Yes" or "No".
3. Path Order Query: Ask about the relative order of patient transfer to facilities c and d on the pathway from a to b. Answer one of:
   - "c first": both c and d are on the pathway, c is encountered first from a to b
   - "d first": both c and d are on the pathway, d is encountered first from a to b
   - "only c on path": only c is on the pathway
   - "only d on path": only d is on the pathway
   - "neither on path": neither c nor d is on the pathway
   - "tied": c and d are the same facility and on the pathway
4. Path Intersection Query: Ask how many common facilities pathways (a, b) and (c, d) share. Answer is a non-negative integer.

When you have gathered enough information, submit your final answer. You should use as few queries as possible. If the answer is wrong or the format is invalid, the deduction task fails.

Each query must contain only one tag. Use the following XML format:

- Path Length Query (e.g., querying referral distance between facilities 1 and 5):
<query_length>1,5</query_length>

- Path Membership Query (e.g., querying if facility 3 is on the pathway between 1 and 5):
<query_member>1,5,3</query_member>

- Path Order Query (e.g., querying the relative order of facilities 2 and 3 on the pathway from 1 to 5):
<query_order>1,5,2,3</query_order>

- Path Intersection Query (e.g., querying the number of shared facilities between pathways (1,5) and (2,6)):
<query_intersection>1,5,2,6</query_intersection>

When submitting the final answer, provide the complete medical facility sequence from S to T (comma-separated), in this format:

<answer>{s},...,{t}</answer>

For example, if the path from S={s} to T={t} passes through x and y, submit:
<answer>{s},x,y,{t}</answer>

Note: The answer must start with S and end with T, including all intermediate nodes, with adjacent facilities directly connected by referral links.
"""

    contextualized_rule_zh_3 = """\
[教育场景] 欢迎参与“先修知识图谱”推演系统。

系统设定了一张未知的树状知识依赖图谱（无向连通无环图），共有 {n} 个学习模块，编号为 1 到 {n}。我已秘密构造了该图谱结构，并指定了学习路径的起点基础模块 S = {s} 和终点核心目标模块 T = {t}。

你的目标是推断出从 S 到 T 的唯一学习进阶路径上的所有模块序列（按学习先后顺序）。你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的知识图谱如实回答：

1. 路径长度查询：询问学习模块 a 和 b 之间的学习推导步数（边数）。回答一个非负整数。
2. 路径成员查询：询问学习模块 c 是否在进阶模块 a 和 b 之间的路径上（包含端点）。回答"是"或"否"。
3. 路径顺序查询：询问在从模块 a 到 b 的学习路径上，c 和 d 的相对学习先后顺序。回答以下之一：
   - "c先"：c 和 d 都在路径上，从 a 到 b 方向先学习 c
   - "d先"：c 和 d 都在路径上，从 a 到 b 方向先学习 d
   - "仅c在路径上"：只有 c 在路径上
   - "仅d在路径上"：只有 d 在路径上
   - "都不在"：c 和 d 都不在路径上
   - "并列"：c 和 d 是同一个模块且在路径上
4. 路径交集查询：询问学习路径 (a, b) 和学习路径 (c, d) 有多少个公共基础模块。回答一个非负整数。

当你收集足够信息后，请提交最终答案。你应该尽可能少地使用查询次数。若答案错误或格式不符，推演任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 路径长度查询（例如查询模块 1 和 5 之间的推导步数）：
<query_length>1,5</query_length>

- 路径成员查询（例如查询模块 3 是否在 1 和 5 的学习路径上）：
<query_member>1,5,3</query_member>

- 路径顺序查询（例如查询在 1 和 5 的学习路径上，2 和 3 的相对顺序）：
<query_order>1,5,2,3</query_order>

- 路径交集查询（例如查询路径 (1,5) 和路径 (2,6) 的公共节点数）：
<query_intersection>1,5,2,6</query_intersection>

提交最终答案时，必须给出从 S 到 T 的完整学习模块序列（用逗号隔开），格式如下：

<answer>{s},...,{t}</answer>

例如，如果从 S={s} 到 T={t} 的路径经过 x, y，则提交：
<answer>{s},x,y,{t}</answer>

注意：答案必须以 S 开始，以 T 结束，且包含所有中间节点，相邻模块之间必须有直接的先修依赖关系。
"""

    contextualized_rule_en_3 = """\
[Education Scenario] Welcome to the "Prerequisite Knowledge Graph" deduction system.

The game involves an unknown tree-structured knowledge dependency graph (undirected connected acyclic graph) with {n} learning modules, numbered from 1 to {n}. I have secretly constructed the graph structure and designated two special modules: baseline start module S = {s} and target advanced module T = {t}.

Your goal is to infer the complete sequence of modules on the unique learning pathway from S to T (in order of progression). You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the actual knowledge graph:

1. Path Length Query: Ask for the number of learning steps (edges) between module a and b. Answer is a non-negative integer.
2. Path Membership Query: Ask whether module c is on the learning pathway between a and b (including endpoints). Answer "Yes" or "No".
3. Path Order Query: Ask about the relative learning order of modules c and d on the pathway from a to b. Answer one of:
   - "c first": both c and d are on the pathway, c is learned first from a to b
   - "d first": both c and d are on the pathway, d is learned first from a to b
   - "only c on path": only c is on the pathway
   - "only d on path": only d is on the pathway
   - "neither on path": neither c nor d is on the pathway
   - "tied": c and d are the same module and on the pathway
4. Path Intersection Query: Ask how many common modules pathways (a, b) and (c, d) share. Answer is a non-negative integer.

When you have gathered enough information, submit your final answer. You should use as few queries as possible. If the answer is wrong or the format is invalid, the deduction task fails.

Each query must contain only one tag. Use the following XML format:

- Path Length Query (e.g., querying learning steps between modules 1 and 5):
<query_length>1,5</query_length>

- Path Membership Query (e.g., querying if module 3 is on the pathway between 1 and 5):
<query_member>1,5,3</query_member>

- Path Order Query (e.g., querying the relative order of modules 2 and 3 on the pathway from 1 to 5):
<query_order>1,5,2,3</query_order>

- Path Intersection Query (e.g., querying the number of shared modules between pathways (1,5) and (2,6)):
<query_intersection>1,5,2,6</query_intersection>

When submitting the final answer, provide the complete learning module sequence from S to T (comma-separated), in this format:

<answer>{s},...,{t}</answer>

For example, if the path from S={s} to T={t} passes through x and y, submit:
<answer>{s},x,y,{t}</answer>

Note: The answer must start with S and end with T, including all intermediate nodes, with adjacent modules directly connected by prerequisite links.
"""

    contextualized_rule_zh_4 = """\
[制造业/工业场景] 欢迎参与“工业流水线”追踪系统。

系统设定了一张未知的树状生产流水线网络（无向连通无环图），共有 {n} 个加工工作站，编号为 1 到 {n}。我已秘密构造了该生产线结构，并指定了核心工艺的投料工作站 S = {s} 和总装工作站 T = {t}。

你的目标是推断出从 S 到 T 的唯一工序流转路径上的所有工作站序列（按加工流转顺序）。你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的流水线网络如实回答：

1. 路径长度查询：询问工作站 a 和 b 之间的流转工序数（边数）。回答一个非负整数。
2. 路径成员查询：询问工作站 c 是否在 a 和 b 之间的工艺流转路径上（包含端点）。回答"是"或"否"。
3. 路径顺序查询：询问在工作站 a 到 b 的流转路径上，c 和 d 的相对加工作业顺序。回答以下之一：
   - "c先"：c 和 d 都在路径上，从 a 到 b 方向先流转至 c
   - "d先"：c 和 d 都在路径上，从 a 到 b 方向先流转至 d
   - "仅c在路径上"：只有 c 在路径上
   - "仅d在路径上"：只有 d 在路径上
   - "都不在"：c 和 d 都不在路径上
   - "并列"：c 和 d 是同一个工作站且在路径上
4. 路径交集查询：询问工艺路径 (a, b) 和工艺路径 (c, d) 有多少个公共工作站。回答一个非负整数。

当你收集足够信息后，请提交最终答案。你应该尽可能少地使用查询次数。若答案错误或格式不符，追踪任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 路径长度查询（例如查询工作站 1 和 5 之间的流转工序数）：
<query_length>1,5</query_length>

- 路径成员查询（例如查询工作站 3 是否在 1 和 5 的流转路径上）：
<query_member>1,5,3</query_member>

- 路径顺序查询（例如查询在 1 和 5 的流转路径上，2 和 3 的相对顺序）：
<query_order>1,5,2,3</query_order>

- 路径交集查询（例如查询路径 (1,5) 和路径 (2,6) 的公共节点数）：
<query_intersection>1,5,2,6</query_intersection>

提交最终答案时，必须给出从 S 到 T 的完整工作站序列（用逗号隔开），格式如下：

<answer>{s},...,{t}</answer>

例如，如果从 S={s} 到 T={t} 的路径经过 x, y，则提交：
<answer>{s},x,y,{t}</answer>

注意：答案必须以 S 开始，以 T 结束，且包含所有中间节点，相邻工作站之间必须有直接的工序关联传送。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario] Welcome to the "Industrial Assembly Line" tracking system.

The game involves an unknown tree-structured production line network (undirected connected acyclic graph) with {n} processing workstations, numbered from 1 to {n}. I have secretly constructed the production line and designated two special stations: raw material input station S = {s} and final assembly station T = {t}.

Your goal is to infer the complete sequence of workstations on the unique process flow pathway from S to T (in order of manufacturing). You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the actual assembly network:

1. Path Length Query: Ask for the number of process steps (edges) between workstation a and b. Answer is a non-negative integer.
2. Path Membership Query: Ask whether workstation c is on the process flow pathway between a and b (including endpoints). Answer "Yes" or "No".
3. Path Order Query: Ask about the relative processing order of workstations c and d on the pathway from a to b. Answer one of:
   - "c first": both c and d are on the pathway, c is encountered first from a to b
   - "d first": both c and d are on the pathway, d is encountered first from a to b
   - "only c on path": only c is on the pathway
   - "only d on path": only d is on the pathway
   - "neither on path": neither c nor d is on the pathway
   - "tied": c and d are the same workstation and on the pathway
4. Path Intersection Query: Ask how many common workstations pathways (a, b) and (c, d) share. Answer is a non-negative integer.

When you have gathered enough information, submit your final answer. You should use as few queries as possible. If the answer is wrong or the format is invalid, the tracking task fails.

Each query must contain only one tag. Use the following XML format:

- Path Length Query (e.g., querying process steps between workstations 1 and 5):
<query_length>1,5</query_length>

- Path Membership Query (e.g., querying if workstation 3 is on the pathway between 1 and 5):
<query_member>1,5,3</query_member>

- Path Order Query (e.g., querying the relative order of workstations 2 and 3 on the pathway from 1 to 5):
<query_order>1,5,2,3</query_order>

- Path Intersection Query (e.g., querying the number of shared workstations between pathways (1,5) and (2,6)):
<query_intersection>1,5,2,6</query_intersection>

When submitting the final answer, provide the complete workstation sequence from S to T (comma-separated), in this format:

<answer>{s},...,{t}</answer>

For example, if the path from S={s} to T={t} passes through x and y, submit:
<answer>{s},x,y,{t}</answer>

Note: The answer must start with S and end with T, including all intermediate nodes, with adjacent workstations directly connected by a process link.
"""

    contextualized_rule_zh_5 = """\
[法律场景] 欢迎参与“证据逻辑链条”推演系统。

系统设定了一张未知的树状逻辑推演网络（无向连通无环图），共有 {n} 个证据节点，编号为 1 到 {n}。我已秘密构造了该法理逻辑结构，并指定了案情的初始线索节点 S = {s} 和核心定罪节点 T = {t}。

你的目标是推断出从 S 到 T 的唯一闭环逻辑链条上的所有证据序列（按推演衍生顺序）。你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的证据逻辑链如实回答：

1. 路径长度查询：询问证据节点 a 和 b 之间的逻辑衍生步数（边数）。回答一个非负整数。
2. 路径成员查询：询问证据节点 c 是否在 a 和 b 之间的推演链条上（包含端点）。回答"是"或"否"。
3. 路径顺序查询：询问在证据节点 a 到 b 的推演链条上，c 和 d 的相对审查顺序。回答以下之一：
   - "c先"：c 和 d 都在链条上，从 a 到 b 方向先审查 c
   - "d先"：c 和 d 都在链条上，从 a 到 b 方向先审查 d
   - "仅c在路径上"：只有 c 在链条上
   - "仅d在路径上"：只有 d 在链条上
   - "都不在"：c 和 d 都不在链条上
   - "并列"：c 和 d 是同一个证据节点且在链条上
4. 路径交集查询：询问推演链条 (a, b) 和推演链条 (c, d) 有多少个公共证据节点。回答一个非负整数。

当你收集足够信息后，请提交最终答案。你应该尽可能少地使用查询次数。若答案错误或格式不符，推演任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 路径长度查询（例如查询证据 1 和 5 之间的逻辑步数）：
<query_length>1,5</query_length>

- 路径成员查询（例如查询证据 3 是否在 1 和 5 的推演链条上）：
<query_member>1,5,3</query_member>

- 路径顺序查询（例如查询在 1 和 5 的链条上，2 和 3 的相对顺序）：
<query_order>1,5,2,3</query_order>

- 路径交集查询（例如查询链条 (1,5) 和链条 (2,6) 的公共节点数）：
<query_intersection>1,5,2,6</query_intersection>

提交最终答案时，必须给出从 S 到 T 的完整证据节点序列（用逗号隔开），格式如下：

<answer>{s},...,{t}</answer>

例如，如果从 S={s} 到 T={t} 的路径经过 x, y，则提交：
<answer>{s},x,y,{t}</answer>

注意：答案必须以 S 开始，以 T 结束，且包含所有中间节点，相邻证据之间必须有严密的逻辑衍生关联。
"""

    contextualized_rule_en_5 = """\
[Law Scenario] Welcome to the "Evidence Logic Chain" deduction system.

The game involves an unknown tree-structured logical deduction network (undirected connected acyclic graph) with {n} evidence nodes, numbered from 1 to {n}. I have secretly constructed the logical structure and designated two special nodes: initial clue node S = {s} and conclusive conviction node T = {t}.

Your goal is to infer the complete sequence of evidence nodes on the unique logical chain from S to T (in order of derivation). You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the actual evidence network:

1. Path Length Query: Ask for the number of logical derivation steps (edges) between node a and b. Answer is a non-negative integer.
2. Path Membership Query: Ask whether evidence node c is on the deduction chain between a and b (including endpoints). Answer "Yes" or "No".
3. Path Order Query: Ask about the relative examination order of evidence nodes c and d on the chain from a to b. Answer one of:
   - "c first": both c and d are on the chain, c is examined first from a to b
   - "d first": both c and d are on the chain, d is examined first from a to b
   - "only c on path": only c is on the chain
   - "only d on path": only d is on the chain
   - "neither on path": neither c nor d is on the chain
   - "tied": c and d are the same node and on the chain
4. Path Intersection Query: Ask how many common evidence nodes chains (a, b) and (c, d) share. Answer is a non-negative integer.

When you have gathered enough information, submit your final answer. You should use as few queries as possible. If the answer is wrong or the format is invalid, the deduction task fails.

Each query must contain only one tag. Use the following XML format:

- Path Length Query (e.g., querying derivation steps between nodes 1 and 5):
<query_length>1,5</query_length>

- Path Membership Query (e.g., querying if node 3 is on the chain between 1 and 5):
<query_member>1,5,3</query_member>

- Path Order Query (e.g., querying the relative order of nodes 2 and 3 on the chain from 1 to 5):
<query_order>1,5,2,3</query_order>

- Path Intersection Query (e.g., querying the number of shared nodes between chains (1,5) and (2,6)):
<query_intersection>1,5,2,6</query_intersection>

When submitting the final answer, provide the complete evidence node sequence from S to T (comma-separated), in this format:

<answer>{s},...,{t}</answer>

For example, if the path from S={s} to T={t} passes through x and y, submit:
<answer>{s},x,y,{t}</answer>

Note: The answer must start with S and end with T, including all intermediate nodes, with adjacent evidence nodes directly connected by logical derivation links.
"""

    tags = ["answer", "query_length", "query_member", "query_order", "query_intersection"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "s": 1,
                "t": 5,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "s": 4,
                "t": 7,
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10)],
                "s": 7,
                "t": 10,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (11, 12)],
                "s": 8,
                "t": 12,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), 
                          (7, 11), (8, 12), (9, 13), (10, 14), (11, 15)],
                "s": 12,
                "t": 15,
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "s": 1,
                "t": 5,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "s": 4,
                "t": 7,
            },
            3: {
                "n": 10,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9), (6, 10)],
                "s": 7,
                "t": 10,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (11, 12)],
                "s": 8,
                "t": 12,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), 
                          (7, 11), (8, 12), (9, 13), (10, 14), (11, 15)],
                "s": 12,
                "t": 15,
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
        
        self.n = cfg["n"]
        self.s = cfg["s"]
        self.t = cfg["t"]
        self.edges = cfg["edges"]
        
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.correct_path = self._find_path(self.s, self.t)

    def _find_path(self, start, end):
        from collections import deque
        
        if start == end:
            return [start]
        
        queue = deque([(start, [start])])
        visited = {start}
        
        while queue:
            node, path = queue.popleft()
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    if neighbor == end:
                        return new_path
                    queue.append((neighbor, new_path))
        
        return []

    def _path_length(self, a, b):
        path = self._find_path(a, b)
        return len(path) - 1 if len(path) > 0 else 0

    def _is_on_path(self, a, b, c):
        path = self._find_path(a, b)
        return c in path

    def _path_order(self, a, b, c, d):
        path = self._find_path(a, b)
        c_in = c in path
        d_in = d in path
        
        if not c_in and not d_in:
            return "都不在" if self.config.language == "zh" else "neither on path"
        if c_in and not d_in:
            return "仅c在路径上" if self.config.language == "zh" else "only c on path"
        if d_in and not c_in:
            return "仅d在路径上" if self.config.language == "zh" else "only d on path"
        
        if c == d:
            return "并列" if self.config.language == "zh" else "tied"
        
        c_idx = path.index(c)
        d_idx = path.index(d)
        
        if c_idx < d_idx:
            return "c先" if self.config.language == "zh" else "c first"
        else:
            return "d先" if self.config.language == "zh" else "d first"

    def _path_intersection(self, a, b, c, d):
        path1 = set(self._find_path(a, b))
        path2 = set(self._find_path(c, d))
        return len(path1 & path2)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            submitted_path = [int(x.strip()) for x in raw_ans.split(",")]
            
            if len(submitted_path) < 2:
                return False
            if submitted_path[0] != self.s or submitted_path[-1] != self.t:
                return False
            
            for node in submitted_path:
                if node < 1 or node > self.n:
                    return False
            
            for i in range(len(submitted_path) - 1):
                u, v = submitted_path[i], submitted_path[i + 1]
                if v not in self.adj[u]:
                    return False
            
            return submitted_path == self.correct_path
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。"
            error_range = "错误：节点编号超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format."
            error_range = "Error: Node ID out of range."

        if "query_length" in parsed_info:
            try:
                raw = parsed_info["query_length"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                a, b = int(parts[0]), int(parts[1])
                if a < 1 or a > self.n or b < 1 or b > self.n:
                    return error_range
                if a == b:
                    return "0"
                return str(self._path_length(a, b))
            except:
                return error_format

        elif "query_member" in parsed_info:
            try:
                raw = parsed_info["query_member"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return error_format
                a, b, c = int(parts[0]), int(parts[1]), int(parts[2])
                if a < 1 or a > self.n or b < 1 or b > self.n or c < 1 or c > self.n:
                    return error_range
                return yes_res if self._is_on_path(a, b, c) else no_res
            except:
                return error_format

        elif "query_order" in parsed_info:
            try:
                raw = parsed_info["query_order"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 4:
                    return error_format
                a, b, c, d = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
                if a < 1 or a > self.n or b < 1 or b > self.n or c < 1 or c > self.n or d < 1 or d > self.n:
                    return error_range
                return self._path_order(a, b, c, d)
            except:
                return error_format

        elif "query_intersection" in parsed_info:
            try:
                raw = parsed_info["query_intersection"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 4:
                    return error_format
                a, b, c, d = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
                if a < 1 or a > self.n or b < 1 or b > self.n or c < 1 or c > self.n or d < 1 or d > self.n:
                    return error_range
                return str(self._path_intersection(a, b, c, d))
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            wrong_val = val + 1
            return str(wrong_val)
        except ValueError:
            pass

        if correct in ("是", "否"):
            return "否" if correct == "是" else "是"
        if correct in ("Yes", "No"):
            return "No" if correct == "Yes" else "Yes"

        swap_map_zh = {
            "c先": "d先",
            "d先": "c先",
            "仅c在路径上": "仅d在路径上",
            "仅d在路径上": "仅c在路径上",
            "都不在": "并列",
            "并列": "都不在",
        }
        swap_map_en = {
            "c first": "d first",
            "d first": "c first",
            "only c on path": "only d on path",
            "only d on path": "only c on path",
            "neither on path": "tied",
            "tied": "neither on path",
        }
        if correct in swap_map_zh:
            return swap_map_zh[correct]
        if correct in swap_map_en:
            return swap_map_en[correct]

        return correct + " (error)"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self.n
        nodes = list(range(1, n + 1))
        
        is_zh = self.config.language == "zh"
        yes_res = "是" if is_zh else "Yes"
        no_res = "否" if is_zh else "No"
        
        for i, a in enumerate(nodes):
            for b in nodes[i+1:]:
                ans = str(self._path_length(a, b))
                queries.append({
                    "query": f"<query_length>{a},{b}</query_length>",
                    "answer": ans
                })

        for c in nodes:
            ans = yes_res if self._is_on_path(self.s, self.t, c) else no_res
            queries.append({
                "query": f"<query_member>{self.s},{self.t},{c}</query_member>",
                "answer": ans
            })

        for i, c in enumerate(nodes):
            for d in nodes[i+1:]:
                ans = self._path_order(self.s, self.t, c, d)
                queries.append({
                    "query": f"<query_order>{self.s},{self.t},{c},{d}</query_order>",
                    "answer": ans
                })

        for i, c in enumerate(nodes):
            for d in nodes[i+1:]:
                ans = str(self._path_intersection(self.s, self.t, c, d))
                queries.append({
                    "query": f"<query_intersection>{self.s},{self.t},{c},{d}</query_intersection>",
                    "answer": ans
                })
        
        return queries