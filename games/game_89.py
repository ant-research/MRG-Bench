from .base import Game
import re

class TreePredicateGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树谓词识别"游戏，规则如下：

游戏设定了一棵有根树，包含 {n} 个节点，编号为 1 到 {n}，根节点为 {root}。

我已秘密选择了一个隐藏谓词，用于判定每个节点是否被"标记"。该谓词的形式为：
选择某个子树特征 F，一个模数 m（范围 2 到 5），以及一个余数 r（范围 0 到 m-1）。
对于任意节点 u，当且仅当 F(u) 除以 m 的余数等于 r 时，该节点被标记为 YES，否则标记为 NO。

子树特征 F 可能是以下四种之一（均以 u 为根的子树计算）：
1. SIZE：子树节点总数（包含 u 自身）
2. LEAVES：子树中叶子节点个数（在该子树内无子节点的节点）
3. HEIGHT：从 u 到其子树中最远叶子的最长路径边数（叶子节点的 HEIGHT 为 0）
4. BRANCH：子树内拥有至少 2 个孩子的节点数

你的目标是通过查询推断出隐藏谓词的三个参数：特征类型 F、模数 m、余数 r。

你可以进行两类查询：

**结构查询**（次数不限，不计入配额）：
- 查询节点 v 的父节点
- 查询节点 v 的所有孩子节点
- 查询节点 v 的 SIZE 值
- 查询节点 v 的 LEAVES 值
- 查询节点 v 的 HEIGHT 值
- 查询节点 v 的 BRANCH 值

**标签查询**（计入配额，配额为 {quota} 次）：
- 查询节点 v 的标签（YES 或 NO）

当你收集足够信息后，请提交最终答案。若答案错误或超过标签查询配额，游戏失败。

每次查询只能包含一个标签。请使用以下格式：

- 查询父节点（例如查询节点 5 的父节点）：
<query_parent>5</query_parent>

- 查询孩子节点（例如查询节点 3 的孩子）：
<query_children>3</query_children>

- 查询 SIZE 值（例如查询节点 2）：
<query_size>2</query_size>

- 查询 LEAVES 值（例如查询节点 4）：
<query_leaves>4</query_leaves>

- 查询 HEIGHT 值（例如查询节点 1）：
<query_height>1</query_height>

- 查询 BRANCH 值（例如查询节点 6）：
<query_branch>6</query_branch>

- 标签查询（例如查询节点 7 的标签）：
<query_label>7</query_label>

提交最终答案时，必须指明特征类型（SIZE、LEAVES、HEIGHT 或 BRANCH）、模数 m 和余数 r，格式如下：

<answer>F=SIZE, m=3, r=1</answer>
"""

    game_rule_en = """\
Let's play a "Tree Predicate Identification" game. Here are the rules:

The game is set on a rooted tree with {n} nodes, numbered 1 to {n}, with root node {root}.

I have secretly chosen a hidden predicate to determine whether each node is "marked". The predicate has the form:
Choose a subtree feature F, a modulus m (range 2 to 5), and a remainder r (range 0 to m-1).
For any node u, it is marked as YES if and only if F(u) modulo m equals r, otherwise marked as NO.

The subtree feature F can be one of the following four (all calculated for the subtree rooted at u):
1. SIZE: Total number of nodes in the subtree (including u itself)
2. LEAVES: Number of leaf nodes in the subtree (nodes with no children in that subtree)
3. HEIGHT: Length of the longest path from u to any leaf in its subtree (in edges; HEIGHT of a leaf is 0)
4. BRANCH: Number of nodes in the subtree that have at least 2 children

Your goal is to infer the three parameters of the hidden predicate through queries: feature type F, modulus m, and remainder r.

You can make two types of queries:

**Structure Queries** (unlimited, not counted toward quota):
- Query the parent of node v
- Query all children of node v
- Query the SIZE value of node v
- Query the LEAVES value of node v
- Query the HEIGHT value of node v
- Query the BRANCH value of node v

**Label Queries** (counted toward quota, quota is {quota} times):
- Query the label of node v (YES or NO)

When you have gathered enough information, submit your final answer. If the answer is incorrect or you exceed the label query quota, the game fails.

Each query must contain only one tag. Use the following format:

- Query parent node (e.g., query parent of node 5):
<query_parent>5</query_parent>

- Query children nodes (e.g., query children of node 3):
<query_children>3</query_children>

- Query SIZE value (e.g., query node 2):
<query_size>2</query_size>

- Query LEAVES value (e.g., query node 4):
<query_leaves>4</query_leaves>

- Query HEIGHT value (e.g., query node 1):
<query_height>1</query_height>

- Query BRANCH value (e.g., query node 6):
<query_branch>6</query_branch>

- Label query (e.g., query label of node 7):
<query_label>7</query_label>

When submitting the final answer, specify the feature type (SIZE, LEAVES, HEIGHT, or BRANCH), modulus m, and remainder r, using this format:

<answer>F=SIZE, m=3, r=1</answer>
"""

    contextualized_rule_zh_1 = """\
[交通场景]
我们来玩一个"智慧交通调度网络"的推理分析游戏，规则如下：

系统设定了一个具有层级结构的交通路网，包含 {n} 个交通枢纽（节点），编号为 1 到 {n}，总指挥中心（根节点）为 {root}。

交通调度系统秘密使用了一套隐藏算法，来判断每个枢纽是否需要被标记为"高风险拥堵区"（YES 或 NO）。该算法的判定方式为：
选择某个路网特征 F，一个模数 m（范围 2 到 5），以及一个余数 r（范围 0 到 m-1）。
对于任意枢纽 u，当且仅当 F(u) 除以 m 的余数等于 r 时，该枢纽被标记为 YES，否则标记为 NO。

路网特征 F 可能是以下四种之一（均以枢纽 u 为首的下游管辖子网计算）：
1. SIZE：该管辖路网中的枢纽总数（包含 u 自身）
2. LEAVES：该管辖路网中的终端站点个数（在子网内无下游节点的枢纽）
3. HEIGHT：从 u 到其子网中最远终端站点的最长路线深度（边数，终端站点的 HEIGHT 为 0）
4. BRANCH：子网内作为多向分流枢纽（至少有 2 个直接下游节点）的枢纽数

你的目标是通过查询推断出隐藏算法的三个参数：特征类型 F、模数 m、余数 r。

你可以进行两类查询：

**结构查询**（次数不限，不计入配额）：
- 查询节点 v 的上级枢纽
- 查询节点 v 的所有直接下游枢纽
- 查询节点 v 的 SIZE 值
- 查询节点 v 的 LEAVES 值
- 查询节点 v 的 HEIGHT 值
- 查询节点 v 的 BRANCH 值

**标签查询**（计入配额，配额为 {quota} 次）：
- 查询节点 v 的状态标签（YES 或 NO）

当你收集足够信息后，请提交最终答案。若答案错误或超过标签查询配额，游戏失败。

每次查询只能包含一个标签。请使用以下格式：

- 查询上级节点（例如查询枢纽 5 的上级）：
<query_parent>5</query_parent>

- 查询下游节点（例如查询枢纽 3 的下游）：
<query_children>3</query_children>

- 查询 SIZE 值（例如查询枢纽 2）：
<query_size>2</query_size>

- 查询 LEAVES 值（例如查询枢纽 4）：
<query_leaves>4</query_leaves>

- 查询 HEIGHT 值（例如查询枢纽 1）：
<query_height>1</query_height>

- 查询 BRANCH 值（例如查询枢纽 6）：
<query_branch>6</query_branch>

- 标签查询（例如查询枢纽 7 的标签）：
<query_label>7</query_label>

提交最终答案时，必须指明特征类型（SIZE、LEAVES、HEIGHT 或 BRANCH）、模数 m 和余数 r，格式如下：

<answer>F=SIZE, m=3, r=1</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's play a "Smart Traffic Dispatch Network" reasoning game. Here are the rules:

The system is set on a hierarchical traffic network with {n} transit hubs (nodes), numbered 1 to {n}, with the main command center (root) at {root}.

The dispatch system secretly uses a hidden algorithm to determine whether each hub should be flagged as a "high-risk congestion zone" (YES or NO). The algorithm works as follows:
Choose a network feature F, a modulus m (range 2 to 5), and a remainder r (range 0 to m-1).
For any hub u, it is flagged as YES if and only if F(u) modulo m equals r, otherwise flagged as NO.

The network feature F can be one of the following four (all calculated for the downstream sub-network governed by u):
1. SIZE: Total number of hubs in the governed sub-network (including u itself)
2. LEAVES: Number of terminal stations in the sub-network (hubs with no downstream nodes)
3. HEIGHT: Length of the longest route from u to any terminal station in its sub-network (in edges; HEIGHT of a terminal station is 0)
4. BRANCH: Number of multi-directional diversion hubs in the sub-network (hubs with at least 2 direct downstream nodes)

Your goal is to infer the three parameters of the hidden algorithm through queries: feature type F, modulus m, and remainder r.

You can make two types of queries:

**Structure Queries** (unlimited, not counted toward quota):
- Query the upstream hub of node v
- Query all direct downstream hubs of node v
- Query the SIZE value of node v
- Query the LEAVES value of node v
- Query the HEIGHT value of node v
- Query the BRANCH value of node v

**Label Queries** (counted toward quota, quota is {quota} times):
- Query the status label of node v (YES or NO)

When you have gathered enough information, submit your final answer. If the answer is incorrect or you exceed the label query quota, the game fails.

Each query must contain only one tag. Use the following format:

- Query upstream hub (e.g., query upstream of hub 5):
<query_parent>5</query_parent>

- Query downstream hubs (e.g., query downstream of hub 3):
<query_children>3</query_children>

- Query SIZE value (e.g., query hub 2):
<query_size>2</query_size>

- Query LEAVES value (e.g., query hub 4):
<query_leaves>4</query_leaves>

- Query HEIGHT value (e.g., query hub 1):
<query_height>1</query_height>

- Query BRANCH value (e.g., query hub 6):
<query_branch>6</query_branch>

- Label query (e.g., query label of hub 7):
<query_label>7</query_label>

When submitting the final answer, specify the feature type (SIZE, LEAVES, HEIGHT, or BRANCH), modulus m, and remainder r, using this format:

<answer>F=SIZE, m=3, r=1</answer>
"""

    contextualized_rule_zh_2 = """\
[医疗场景]
我们来玩一个"分级诊疗医疗网络"的推理分析游戏，规则如下：

系统设定了一个具有层级结构的医疗网络，包含 {n} 个医疗机构（节点），编号为 1 到 {n}，国家中心医院（根节点）为 {root}。

卫生管理部门秘密制定了一套审计标准，来判断每个医疗机构是否需要被标记为"重点资源调配节点"（YES 或 NO）。该标准的判定方式为：
选择某个管辖网络特征 F，一个模数 m（范围 2 到 5），以及一个余数 r（范围 0 到 m-1）。
对于任意机构 u，当且仅当 F(u) 除以 m 的余数等于 r 时，该机构被标记为 YES，否则标记为 NO。

管辖网络特征 F 可能是以下四种之一（均以机构 u 为首的下级分支网络计算）：
1. SIZE：该管辖网络内的医疗机构总数（包含 u 自身）
2. LEAVES：该管辖网络内的基层卫生所个数（在子网内无进一步下级机构）
3. HEIGHT：从 u 到其子网中最远基层卫生所的最长转诊层级（转诊次数，基层卫生所的 HEIGHT 为 0）
4. BRANCH：子网内作为区域医疗中心（具有至少 2 家直接下级机构）的机构数

你的目标是通过查询推断出隐藏标准的三个参数：特征类型 F、模数 m、余数 r。

你可以进行两类查询：

**结构查询**（次数不限，不计入配额）：
- 查询节点 v 的直接上级机构
- 查询节点 v 的所有直接下级机构
- 查询节点 v 的 SIZE 值
- 查询节点 v 的 LEAVES 值
- 查询节点 v 的 HEIGHT 值
- 查询节点 v 的 BRANCH 值

**标签查询**（计入配额，配额为 {quota} 次）：
- 查询节点 v 的状态标签（YES 或 NO）

当你收集足够信息后，请提交最终答案。若答案错误或超过标签查询配额，游戏失败。

每次查询只能包含一个标签。请使用以下格式：

- 查询上级机构（例如查询机构 5 的上级）：
<query_parent>5</query_parent>

- 查询下级机构（例如查询机构 3 的下级）：
<query_children>3</query_children>

- 查询 SIZE 值（例如查询机构 2）：
<query_size>2</query_size>

- 查询 LEAVES 值（例如查询机构 4）：
<query_leaves>4</query_leaves>

- 查询 HEIGHT 值（例如查询机构 1）：
<query_height>1</query_height>

- 查询 BRANCH 值（例如查询机构 6）：
<query_branch>6</query_branch>

- 标签查询（例如查询机构 7 的标签）：
<query_label>7</query_label>

提交最终答案时，必须指明特征类型（SIZE、LEAVES、HEIGHT 或 BRANCH）、模数 m 和余数 r，格式如下：

<answer>F=SIZE, m=3, r=1</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's play a "Hierarchical Medical Referral Network" reasoning game. Here are the rules:

The system is set on a hierarchical medical network with {n} healthcare facilities (nodes), numbered 1 to {n}, with the national central hospital (root) at {root}.

The health administration has secretly established an audit standard to determine whether each facility should be flagged as a "key resource allocation target" (YES or NO). The standard works as follows:
Choose a network feature F, a modulus m (range 2 to 5), and a remainder r (range 0 to m-1).
For any facility u, it is flagged as YES if and only if F(u) modulo m equals r, otherwise flagged as NO.

The network feature F can be one of the following four (all calculated for the subordinate network governed by u):
1. SIZE: Total number of facilities in the governed network (including u itself)
2. LEAVES: Number of grassroots clinics in the network (facilities with no further subordinate institutions)
3. HEIGHT: Length of the longest referral path from u to any grassroots clinic in its network (in referral steps; HEIGHT of a grassroots clinic is 0)
4. BRANCH: Number of regional medical centers in the network (facilities managing at least 2 direct subordinate institutions)

Your goal is to infer the three parameters of the hidden standard through queries: feature type F, modulus m, and remainder r.

You can make two types of queries:

**Structure Queries** (unlimited, not counted toward quota):
- Query the superior facility of node v
- Query all direct subordinate facilities of node v
- Query the SIZE value of node v
- Query the LEAVES value of node v
- Query the HEIGHT value of node v
- Query the BRANCH value of node v

**Label Queries** (counted toward quota, quota is {quota} times):
- Query the status label of node v (YES or NO)

When you have gathered enough information, submit your final answer. If the answer is incorrect or you exceed the label query quota, the game fails.

Each query must contain only one tag. Use the following format:

- Query superior facility (e.g., query superior of facility 5):
<query_parent>5</query_parent>

- Query subordinate facilities (e.g., query subordinates of facility 3):
<query_children>3</query_children>

- Query SIZE value (e.g., query facility 2):
<query_size>2</query_size>

- Query LEAVES value (e.g., query facility 4):
<query_leaves>4</query_leaves>

- Query HEIGHT value (e.g., query facility 1):
<query_height>1</query_height>

- Query BRANCH value (e.g., query facility 6):
<query_branch>6</query_branch>

- Label query (e.g., query label of facility 7):
<query_label>7</query_label>

When submitting the final answer, specify the feature type (SIZE, LEAVES, HEIGHT, or BRANCH), modulus m, and remainder r, using this format:

<answer>F=SIZE, m=3, r=1</answer>
"""

    contextualized_rule_zh_3 = """\
[教育场景]
我们来玩一个"课程知识点图谱"的推理分析游戏，规则如下：

系统设定了一个具有前置依赖关系的知识图谱树，包含 {n} 个知识模块（节点），编号为 1 到 {n}，学科核心基础（根节点）为 {root}。

教学大纲秘密使用了一套评估规则，来判断每个知识模块是否需要被标记为"核心必考点"（YES 或 NO）。该规则的判定方式为：
选择某个衍生结构特征 F，一个模数 m（范围 2 到 5），以及一个余数 r（范围 0 到 m-1）。
对于任意模块 u，当且仅当 F(u) 除以 m 的余数等于 r 时，该模块被标记为 YES，否则标记为 NO。

衍生结构特征 F 可能是以下四种之一（均以模块 u 及其所有后续衍生知识构成的子树计算）：
1. SIZE：该衍生知识树中的模块总数（包含 u 自身）
2. LEAVES：该衍生树中的终点概念个数（不再向下衍生的基础模块）
3. HEIGHT：从 u 到其衍生树中最远终点概念的最长学习路径深度（步数，终点概念的 HEIGHT 为 0）
4. BRANCH：子树内作为核心前置节点（衍生出至少 2 个直接分支模块）的模块数

你的目标是通过查询推断出隐藏规则的三个参数：特征类型 F、模数 m、余数 r。

你可以进行两类查询：

**结构查询**（次数不限，不计入配额）：
- 查询节点 v 的直接前置模块（父节点）
- 查询节点 v 的所有直接衍生模块（子节点）
- 查询节点 v 的 SIZE 值
- 查询节点 v 的 LEAVES 值
- 查询节点 v 的 HEIGHT 值
- 查询节点 v 的 BRANCH 值

**标签查询**（计入配额，配额为 {quota} 次）：
- 查询节点 v 的状态标签（YES 或 NO）

当你收集足够信息后，请提交最终答案。若答案错误或超过标签查询配额，游戏失败。

每次查询只能包含一个标签。请使用以下格式：

- 查询前置模块（例如查询模块 5 的前置）：
<query_parent>5</query_parent>

- 查询衍生模块（例如查询模块 3 的衍生）：
<query_children>3</query_children>

- 查询 SIZE 值（例如查询模块 2）：
<query_size>2</query_size>

- 查询 LEAVES 值（例如查询模块 4）：
<query_leaves>4</query_leaves>

- 查询 HEIGHT 值（例如查询模块 1）：
<query_height>1</query_height>

- 查询 BRANCH 值（例如查询模块 6）：
<query_branch>6</query_branch>

- 标签查询（例如查询模块 7 的标签）：
<query_label>7</query_label>

提交最终答案时，必须指明特征类型（SIZE、LEAVES、HEIGHT 或 BRANCH）、模数 m 和余数 r，格式如下：

<answer>F=SIZE, m=3, r=1</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Curriculum Knowledge Graph" reasoning game. Here are the rules:

The system is set on a prerequisite dependency tree with {n} knowledge modules (nodes), numbered 1 to {n}, with the core subject foundation (root) at {root}.

The syllabus secretly uses an assessment rule to determine whether each module should be flagged as a "mandatory key assessment node" (YES or NO). The rule works as follows:
Choose a derived structural feature F, a modulus m (range 2 to 5), and a remainder r (range 0 to m-1).
For any module u, it is flagged as YES if and only if F(u) modulo m equals r, otherwise flagged as NO.

The derived structural feature F can be one of the following four (all calculated for the subtree of subsequent knowledge derived from u):
1. SIZE: Total number of modules in the derived knowledge tree (including u itself)
2. LEAVES: Number of terminal concepts in the derived tree (foundational modules with no further derivations)
3. HEIGHT: Length of the longest learning path from u to any terminal concept in its derived tree (in steps; HEIGHT of a terminal concept is 0)
4. BRANCH: Number of core prerequisite nodes in the derived tree (modules branching into at least 2 direct sub-modules)

Your goal is to infer the three parameters of the hidden rule through queries: feature type F, modulus m, and remainder r.

You can make two types of queries:

**Structure Queries** (unlimited, not counted toward quota):
- Query the direct prerequisite module (parent) of node v
- Query all direct derived modules (children) of node v
- Query the SIZE value of node v
- Query the LEAVES value of node v
- Query the HEIGHT value of node v
- Query the BRANCH value of node v

**Label Queries** (counted toward quota, quota is {quota} times):
- Query the status label of node v (YES or NO)

When you have gathered enough information, submit your final answer. If the answer is incorrect or you exceed the label query quota, the game fails.

Each query must contain only one tag. Use the following format:

- Query prerequisite module (e.g., query prerequisite of module 5):
<query_parent>5</query_parent>

- Query derived modules (e.g., query derivations of module 3):
<query_children>3</query_children>

- Query SIZE value (e.g., query module 2):
<query_size>2</query_size>

- Query LEAVES value (e.g., query module 4):
<query_leaves>4</query_leaves>

- Query HEIGHT value (e.g., query module 1):
<query_height>1</query_height>

- Query BRANCH value (e.g., query module 6):
<query_branch>6</query_branch>

- Label query (e.g., query label of module 7):
<query_label>7</query_label>

When submitting the final answer, specify the feature type (SIZE, LEAVES, HEIGHT, or BRANCH), modulus m, and remainder r, using this format:

<answer>F=SIZE, m=3, r=1</answer>
"""

    contextualized_rule_zh_4 = """\
[工业制造场景]
我们来玩一个"工业产品物料清单（BOM）树"的推理分析游戏，规则如下：

系统设定了一个具有组装依赖关系的物料清单树，包含 {n} 个零部件（节点），编号为 1 到 {n}，最终成品（根节点）为 {root}。

质量控制系统秘密使用了一套质检标准，来判断每个零部件是否需要被标记为"需深度质检"（YES 或 NO）。该标准的判定方式为：
选择某个组件结构特征 F，一个模数 m（范围 2 到 5），以及一个余数 r（范围 0 到 m-1）。
对于任意零部件 u，当且仅当 F(u) 除以 m 的余数等于 r 时，该零部件被标记为 YES，否则标记为 NO。

组件结构特征 F 可能是以下四种之一（均以零部件 u 为总成的子装配体计算）：
1. SIZE：该装配体包含的零部件总数（包含 u 自身）
2. LEAVES：该装配体中的基础原材料个数（不再细分的底层零件）
3. HEIGHT：从 u 到其子零件中最远原材料的最长组装工序链深度（步数，原材料的 HEIGHT 为 0）
4. BRANCH：装配体内作为复杂组件（由至少 2 个直接子零件组装而成）的节点数

你的目标是通过查询推断出隐藏质检标准的三个参数：特征类型 F、模数 m、余数 r。

你可以进行两类查询：

**结构查询**（次数不限，不计入配额）：
- 查询节点 v 的所属父组件
- 查询节点 v 的所有直接子零件
- 查询节点 v 的 SIZE 值
- 查询节点 v 的 LEAVES 值
- 查询节点 v 的 HEIGHT 值
- 查询节点 v 的 BRANCH 值

**标签查询**（计入配额，配额为 {quota} 次）：
- 查询节点 v 的状态标签（YES 或 NO）

当你收集足够信息后，请提交最终答案。若答案错误或超过标签查询配额，游戏失败。

每次查询只能包含一个标签。请使用以下格式：

- 查询父组件（例如查询零部件 5 的所属父组件）：
<query_parent>5</query_parent>

- 查询子零件（例如查询零部件 3 的直接子零件）：
<query_children>3</query_children>

- 查询 SIZE 值（例如查询零部件 2）：
<query_size>2</query_size>

- 查询 LEAVES 值（例如查询零部件 4）：
<query_leaves>4</query_leaves>

- 查询 HEIGHT 值（例如查询零部件 1）：
<query_height>1</query_height>

- 查询 BRANCH 值（例如查询零部件 6）：
<query_branch>6</query_branch>

- 标签查询（例如查询零部件 7 的标签）：
<query_label>7</query_label>

提交最终答案时，必须指明特征类型（SIZE、LEAVES、HEIGHT 或 BRANCH）、模数 m 和余数 r，格式如下：

<answer>F=SIZE, m=3, r=1</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Industry Scenario]
Let's play an "Industrial Bill of Materials (BOM) Tree" reasoning game. Here are the rules:

The system is set on an assembly dependency tree with {n} components (nodes), numbered 1 to {n}, with the final assembled product (root) at {root}.

The quality control system secretly uses an inspection standard to determine whether each component should be flagged as "requiring deep quality inspection" (YES or NO). The standard works as follows:
Choose an assembly structural feature F, a modulus m (range 2 to 5), and a remainder r (range 0 to m-1).
For any component u, it is flagged as YES if and only if F(u) modulo m equals r, otherwise flagged as NO.

The structural feature F can be one of the following four (all calculated for the sub-assembly formed under component u):
1. SIZE: Total number of sub-components in the assembly (including u itself)
2. LEAVES: Number of base raw materials in the assembly (bottom-level parts with no further subdivisions)
3. HEIGHT: Length of the longest assembly sequence chain from u to any raw material (in steps; HEIGHT of a raw material is 0)
4. BRANCH: Number of complex sub-assemblies in the structure (components assembled from at least 2 direct sub-parts)

Your goal is to infer the three parameters of the hidden inspection standard through queries: feature type F, modulus m, and remainder r.

You can make two types of queries:

**Structure Queries** (unlimited, not counted toward quota):
- Query the parent assembly of node v
- Query all direct sub-components of node v
- Query the SIZE value of node v
- Query the LEAVES value of node v
- Query the HEIGHT value of node v
- Query the BRANCH value of node v

**Label Queries** (counted toward quota, quota is {quota} times):
- Query the status label of node v (YES or NO)

When you have gathered enough information, submit your final answer. If the answer is incorrect or you exceed the label query quota, the game fails.

Each query must contain only one tag. Use the following format:

- Query parent assembly (e.g., query parent assembly of component 5):
<query_parent>5</query_parent>

- Query sub-components (e.g., query sub-components of component 3):
<query_children>3</query_children>

- Query SIZE value (e.g., query component 2):
<query_size>2</query_size>

- Query LEAVES value (e.g., query component 4):
<query_leaves>4</query_leaves>

- Query HEIGHT value (e.g., query component 1):
<query_height>1</query_height>

- Query BRANCH value (e.g., query component 6):
<query_branch>6</query_branch>

- Label query (e.g., query label of component 7):
<query_label>7</query_label>

When submitting the final answer, specify the feature type (SIZE, LEAVES, HEIGHT, or BRANCH), modulus m, and remainder r, using this format:

<answer>F=SIZE, m=3, r=1</answer>
"""

    contextualized_rule_zh_5 = """\
[法律/合规场景]
我们来玩一个"跨国企业控股架构追踪"的推理分析游戏，规则如下：

系统设定了一个具有从属关系的控股架构树，包含 {n} 个企业实体（节点），编号为 1 到 {n}，顶层母公司（根节点）为 {root}。

监管机构秘密使用了一套合规审查规则，来判断每个企业实体是否需要被标记为"需反洗钱/深度合规审查"（YES 或 NO）。该规则的判定方式为：
选择某个控股链条特征 F，一个模数 m（范围 2 到 5），以及一个余数 r（范围 0 到 m-1）。
对于任意企业实体 u，当且仅当 F(u) 除以 m 的余数等于 r 时，该实体被标记为 YES，否则标记为 NO。

控股链条特征 F 可能是以下四种之一（均以实体 u 及其控制的子公司构成的控股子树计算）：
1. SIZE：该控股链条上的企业实体总数（包含 u 自身）
2. LEAVES：该控股子树中的底层运营公司个数（无进一步子公司的基层实体或空壳公司）
3. HEIGHT：从 u 到其控股子树中最远基层实体的最长嵌套控股层级深度（步数，底层运营公司的 HEIGHT 为 0）
4. BRANCH：控股子树内作为控股集团（拥有至少 2 家直接子公司）的实体数

你的目标是通过查询推断出隐藏合规规则的三个参数：特征类型 F、模数 m、余数 r。

你可以进行两类查询：

**结构查询**（次数不限，不计入配额）：
- 查询节点 v 的直接上级控股公司
- 查询节点 v 的所有直接子公司
- 查询节点 v 的 SIZE 值
- 查询节点 v 的 LEAVES 值
- 查询节点 v 的 HEIGHT 值
- 查询节点 v 的 BRANCH 值

**标签查询**（计入配额，配额为 {quota} 次）：
- 查询节点 v 的状态标签（YES 或 NO）

当你收集足够信息后，请提交最终答案。若答案错误或超过标签查询配额，游戏失败。

每次查询只能包含一个标签。请使用以下格式：

- 查询上级控股公司（例如查询企业 5 的上级）：
<query_parent>5</query_parent>

- 查询子公司（例如查询企业 3 的直接子公司）：
<query_children>3</query_children>

- 查询 SIZE 值（例如查询企业 2）：
<query_size>2</query_size>

- 查询 LEAVES 值（例如查询企业 4）：
<query_leaves>4</query_leaves>

- 查询 HEIGHT 值（例如查询企业 1）：
<query_height>1</query_height>

- 查询 BRANCH 值（例如查询企业 6）：
<query_branch>6</query_branch>

- 标签查询（例如查询企业 7 的标签）：
<query_label>7</query_label>

提交最终答案时，必须指明特征类型（SIZE、LEAVES、HEIGHT 或 BRANCH）、模数 m 和余数 r，格式如下：

<answer>F=SIZE, m=3, r=1</answer>
"""

    contextualized_rule_en_5 = """\
[Legal/Compliance Scenario]
Let's play a "Multinational Corporate Holding Structure Tracking" reasoning game. Here are the rules:

The system is set on a corporate holding dependency tree with {n} corporate entities (nodes), numbered 1 to {n}, with the top-level parent company (root) at {root}.

The regulatory agency secretly uses a compliance audit rule to determine whether each corporate entity should be flagged for "Anti-Money Laundering (AML) / deep compliance audit" (YES or NO). The rule works as follows:
Choose a holding chain feature F, a modulus m (range 2 to 5), and a remainder r (range 0 to m-1).
For any corporate entity u, it is flagged as YES if and only if F(u) modulo m equals r, otherwise flagged as NO.

The holding chain feature F can be one of the following four (all calculated for the holding subtree governed by entity u):
1. SIZE: Total number of corporate entities in the holding chain (including u itself)
2. LEAVES: Number of bottom-level operating companies in the holding subtree (grassroots entities or shell companies with no subsidiaries)
3. HEIGHT: Length of the longest nested holding layer from u to any bottom-level entity in its subtree (in steps; HEIGHT of a bottom-level entity is 0)
4. BRANCH: Number of holding conglomerates in the subtree (entities owning at least 2 direct subsidiaries)

Your goal is to infer the three parameters of the hidden compliance rule through queries: feature type F, modulus m, and remainder r.

You can make two types of queries:

**Structure Queries** (unlimited, not counted toward quota):
- Query the direct parent holding company of node v
- Query all direct subsidiaries of node v
- Query the SIZE value of node v
- Query the LEAVES value of node v
- Query the HEIGHT value of node v
- Query the BRANCH value of node v

**Label Queries** (counted toward quota, quota is {quota} times):
- Query the status label of node v (YES or NO)

When you have gathered enough information, submit your final answer. If the answer is incorrect or you exceed the label query quota, the game fails.

Each query must contain only one tag. Use the following format:

- Query parent holding company (e.g., query parent company of entity 5):
<query_parent>5</query_parent>

- Query subsidiaries (e.g., query direct subsidiaries of entity 3):
<query_children>3</query_children>

- Query SIZE value (e.g., query entity 2):
<query_size>2</query_size>

- Query LEAVES value (e.g., query entity 4):
<query_leaves>4</query_leaves>

- Query HEIGHT value (e.g., query entity 1):
<query_height>1</query_height>

- Query HEIGHT value (e.g., query entity 6):
<query_branch>6</query_branch>

- Label query (e.g., query label of entity 7):
<query_label>7</query_label>

When submitting the final answer, specify the feature type (SIZE, LEAVES, HEIGHT, or BRANCH), modulus m, and remainder r, using this format:

<answer>F=SIZE, m=3, r=1</answer>
"""

    tags = ["answer", "query_parent", "query_children", "query_size", 
            "query_leaves", "query_height", "query_branch", "query_label"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "root": 1,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7",
                "feature": "SIZE",
                "modulus": 3,
                "remainder": 1,
            },
            2: {
                "n": 10,
                "root": 1,
                "edges": "1-2,1-3,1-4,2-5,2-6,3-7,4-8,4-9,4-10",
                "feature": "LEAVES",
                "modulus": 3,
                "remainder": 1,
            },
            3: {
                "n": 12,
                "root": 1,
                "edges": "1-2,1-3,2-4,2-5,3-6,4-7,4-8,5-9,6-10,6-11,10-12",
                "feature": "HEIGHT",
                "modulus": 3,
                "remainder": 2,
            },
            4: {
                "n": 15,
                "root": 1,
                "edges": "1-2,1-3,1-4,2-5,2-6,3-7,3-8,3-9,4-10,5-11,5-12,7-13,8-14,8-15",
                "feature": "BRANCH",
                "modulus": 4,
                "remainder": 1,
            },
            5: {
                "n": 20,
                "root": 1,
                "edges": "1-2,1-3,1-4,2-5,2-6,2-7,3-8,3-9,4-10,4-11,5-12,6-13,6-14,7-15,9-16,10-17,10-18,11-19,11-20",
                "feature": "HEIGHT",
                "modulus": 5,
                "remainder": 3,
            },
        },
        "en": {
            1: {
                "n": 7,
                "root": 1,
                "edges": "1-2,1-3,2-4,2-5,3-6,3-7",
                "feature": "SIZE",
                "modulus": 3,
                "remainder": 1,
            },
            2: {
                "n": 10,
                "root": 1,
                "edges": "1-2,1-3,1-4,2-5,2-6,3-7,4-8,4-9,4-10",
                "feature": "LEAVES",
                "modulus": 3,
                "remainder": 1,
            },
            3: {
                "n": 12,
                "root": 1,
                "edges": "1-2,1-3,2-4,2-5,3-6,4-7,4-8,5-9,6-10,6-11,10-12",
                "feature": "HEIGHT",
                "modulus": 3,
                "remainder": 2,
            },
            4: {
                "n": 15,
                "root": 1,
                "edges": "1-2,1-3,1-4,2-5,2-6,3-7,3-8,3-9,4-10,5-11,5-12,7-13,8-14,8-15",
                "feature": "BRANCH",
                "modulus": 4,
                "remainder": 1,
            },
            5: {
                "n": 20,
                "root": 1,
                "edges": "1-2,1-3,1-4,2-5,2-6,2-7,3-8,3-9,4-10,4-11,5-12,6-13,6-14,7-15,9-16,10-17,10-18,11-19,11-20",
                "feature": "HEIGHT",
                "modulus": 5,
                "remainder": 3,
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
        self._game_info["root"] = cfg["root"]
        self._game_info["quota"] = min(12, cfg["n"])
        
        self.n = cfg["n"]
        self.root = cfg["root"]
        self.parent = {i: 0 for i in range(1, self.n + 1)}
        self.children = {i: [] for i in range(1, self.n + 1)}
        
        edges = cfg["edges"].split(",")
        for edge in edges:
            u, v = map(int, edge.split("-"))
            self.parent[v] = u
            self.children[u].append(v)
        
        self.parent[self.root] = 0
        
        self._compute_features()
        
        self.target_feature = cfg["feature"]
        self.target_modulus = cfg["modulus"]
        self.target_remainder = cfg["remainder"]
        
        self.label_query_count = 0
        self.max_label_queries = self._game_info["quota"]

    def _compute_features(self):
        self.size_map = {}
        self.leaves_map = {}
        self.height_map = {}
        self.branch_map = {}
        
        def dfs(u):
            if not self.children[u]:
                self.size_map[u] = 1
                self.leaves_map[u] = 1
                self.height_map[u] = 0
                self.branch_map[u] = 0
                return
            
            total_size = 1
            total_leaves = 0
            max_height = -1
            total_branch = 0
            
            for child in self.children[u]:
                dfs(child)
                total_size += self.size_map[child]
                total_leaves += self.leaves_map[child]
                max_height = max(max_height, self.height_map[child])
                total_branch += self.branch_map[child]
            
            self.size_map[u] = total_size
            self.leaves_map[u] = total_leaves
            self.height_map[u] = max_height + 1
            
            if len(self.children[u]) >= 2:
                total_branch += 1
            self.branch_map[u] = total_branch
        
        dfs(self.root)

    def _get_feature_value(self, node, feature):
        if feature == "SIZE":
            return self.size_map[node]
        elif feature == "LEAVES":
            return self.leaves_map[node]
        elif feature == "HEIGHT":
            return self.height_map[node]
        elif feature == "BRANCH":
            return self.branch_map[node]
        else:
            raise ValueError(f"Unknown feature: {feature}")

    def _compute_label(self, node):
        feature_value = self._get_feature_value(node, self.target_feature)
        return (feature_value % self.target_modulus) == self.target_remainder

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "F" not in ans_dict or "m" not in ans_dict or "r" not in ans_dict:
            return False
        
        try:
            claimed_feature = ans_dict["F"].upper()
            if claimed_feature not in ["SIZE", "LEAVES", "HEIGHT", "BRANCH"]:
                return False
            
            claimed_modulus = int(ans_dict["m"])
            claimed_remainder = int(ans_dict["r"])
            
            if claimed_modulus < 2 or claimed_modulus > 5:
                return False
            if claimed_remainder < 0 or claimed_remainder >= claimed_modulus:
                return False
            
            if (claimed_feature == self.target_feature and 
                    claimed_modulus == self.target_modulus and 
                    claimed_remainder == self.target_remainder):
                return True
            
            for node in range(1, self.n + 1):
                true_label = self._compute_label(node)
                claimed_value = self._get_feature_value(node, claimed_feature)
                claimed_label = (claimed_value % claimed_modulus) == claimed_remainder
                if true_label != claimed_label:
                    return False
            return True
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "YES", "NO"
            error_range = "错误：节点编号超出范围。"
            error_quota = "错误：标签查询次数已达上限。"
            error_format = "错误：格式无效。"
        else:
            yes_res, no_res = "YES", "NO"
            error_range = "Error: Node ID out of range."
            error_quota = "Error: Label query quota exceeded."
            error_format = "Error: Invalid format."

        
        if "query_label" in parsed_info:
            if self.label_query_count >= self.max_label_queries:
                self.state.set_state("failed", "quota exceeded")
                return error_quota
            
            try:
                node = int(parsed_info["query_label"].strip())
                if node < 1 or node > self.n:
                    return error_range
                
                self.label_query_count += 1
                is_marked = self._compute_label(node)
                return yes_res if is_marked else no_res
            except:
                return error_format

        if "query_parent" in parsed_info:
            try:
                node = int(parsed_info["query_parent"].strip())
                if node < 1 or node > self.n:
                    return error_range
                return str(self.parent[node])
            except:
                return error_format

        if "query_children" in parsed_info:
            try:
                node = int(parsed_info["query_children"].strip())
                if node < 1 or node > self.n:
                    return error_range
                children_list = self.children[node]
                if not children_list:
                    return "[]"
                return "[" + ",".join(map(str, children_list)) + "]"
            except:
                return error_format

        if "query_size" in parsed_info:
            try:
                node = int(parsed_info["query_size"].strip())
                if node < 1 or node > self.n:
                    return error_range
                return str(self.size_map[node])
            except:
                return error_format

        if "query_leaves" in parsed_info:
            try:
                node = int(parsed_info["query_leaves"].strip())
                if node < 1 or node > self.n:
                    return error_range
                return str(self.leaves_map[node])
            except:
                return error_format

        if "query_height" in parsed_info:
            try:
                node = int(parsed_info["query_height"].strip())
                if node < 1 or node > self.n:
                    return error_range
                return str(self.height_map[node])
            except:
                return error_format

        if "query_branch" in parsed_info:
            try:
                node = int(parsed_info["query_branch"].strip())
                if node < 1 or node > self.n:
                    return error_range
                return str(self.branch_map[node])
            except:
                return error_format

        raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        stripped = correct.strip()
        
        if stripped.upper() == "YES":
            return "NO"
        if stripped.upper() == "NO":
            return "YES"
        
        try:
            val = int(stripped)
            wrong_val = val + 1
            return str(wrong_val)
        except ValueError:
            pass
        
        if stripped.startswith("[") and stripped.endswith("]"):
            inner = stripped[1:-1].strip()
            if not inner:
                return "[0]"
            else:
                return stripped[:-1] + "," + str(self.n + 1) + "]"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        yes_res, no_res = "YES", "NO"

        for node in range(1, self.n + 1):
            q = f"<query_parent>{node}</query_parent>"
            a = str(self.parent[node])
            results.append({"query": q, "answer": a})

            q = f"<query_children>{node}</query_children>"
            children_list = self.children[node]
            if not children_list:
                a = "[]"
            else:
                a = "[" + ",".join(map(str, children_list)) + "]"
            results.append({"query": q, "answer": a})

            q = f"<query_size>{node}</query_size>"
            a = str(self.size_map[node])
            results.append({"query": q, "answer": a})

            q = f"<query_leaves>{node}</query_leaves>"
            a = str(self.leaves_map[node])
            results.append({"query": q, "answer": a})

            q = f"<query_height>{node}</query_height>"
            a = str(self.height_map[node])
            results.append({"query": q, "answer": a})

            q = f"<query_branch>{node}</query_branch>"
            a = str(self.branch_map[node])
            results.append({"query": q, "answer": a})

            q = f"<query_label>{node}</query_label>"
            is_marked = self._compute_label(node)
            a = yes_res if is_marked else no_res
            results.append({"query": q, "answer": a})

        return results