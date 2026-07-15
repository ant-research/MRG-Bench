from .base import Game
import random

class HiddenTreeLCAGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"隐藏树结构推理"游戏，规则如下：

游戏设定了一棵有根树，节点编号为 1 到 {n}，其中节点 1 是根。这棵树遵循一个固定但未知的参数 k（k 大于等于 2）的规则：
- 树是按层序编号的 k 叉树在前 {n} 个节点上的截断。
- 对于编号 i 大于 1 的节点，其父节点编号可由一个确定的公式计算得出（但公式中的 k 未知）。
- 第 p 个节点的子节点（若存在）在某个连续的编号区间内。

你的目标是通过有限次数的查询，推断出这棵树的隐藏结构规律，并最终正确回答 {m} 对节点的最近公共祖先（LCA）。

你可以使用以下四种查询（每次只能进行一个查询）：

1. **深度查询**：询问节点 x 到根的距离（根的深度为 0）。
2. **祖先判定**：询问节点 u 是否为节点 v 的祖先（u 等于 v 时返回"是"）。
3. **向上爬升**：询问从节点 x 沿父链向上 t 步后到达的节点编号（若越过根则返回"无"）。
4. **深度比较**：询问节点 u 和 v 谁的深度更小（或相同）。

所有查询的回答均由隐藏的树结构唯一确定。你应该尽可能少地使用查询次数来推断出树的规律。

每次查询只能包含一个标签：

- 深度查询（例如查询节点 5 的深度）：
<query_depth>5</query_depth>

- 祖先判定（例如查询节点 2 是否为节点 8 的祖先）：
<query_ancestor>2,8</query_ancestor>

- 向上爬升（例如从节点 7 向上移动 2 步）：
<query_climb>7,2</query_climb>

- 深度比较（例如比较节点 3 和节点 5 谁更接近根）：
<query_compare_depth>3,5</query_compare_depth>

当你准备好回答所有节点对的 LCA 时，请按以下格式提交：

<answer>1:3, 2:1, 3:5</answer>

其中数字对应第 1 到第 {m} 对节点的 LCA 编号，用逗号分隔。答案顺序必须与题目给出的节点对顺序一致。

{pairs_description}

请开始你的查询。
"""

    game_rule_en = """\
Let's play a "Hidden Tree Structure Deduction" game. Here are the rules:

The game has a rooted tree with nodes numbered from 1 to {n}, where node 1 is the root. This tree follows a fixed but unknown parameter k (k greater than or equal to 2):
- The tree is a k-ary tree numbered in level order, truncated at the first {n} nodes.
- For nodes with ID i greater than 1, the parent node ID can be computed by a deterministic formula (but k in the formula is unknown).
- The children of node p (if they exist) lie in a certain contiguous range of IDs.

Your goal is to infer the hidden tree structure through a limited number of queries, and ultimately correctly answer the Lowest Common Ancestor (LCA) for {m} pairs of nodes.

You can use the following four types of queries (one query per turn):

1. **Depth Query**: Ask for the distance from node x to the root (root has depth 0).
2. **Ancestor Query**: Ask whether node u is an ancestor of node v (returns "Yes" when u equals v).
3. **Climb Query**: Ask for the node ID reached by climbing t steps upward from node x along the parent chain (returns "None" if it goes beyond the root).
4. **Depth Comparison Query**: Ask which of nodes u and v is closer to the root (or if they have the same depth).

All query answers are uniquely determined by the hidden tree structure. You should use as few queries as possible to deduce the tree pattern.

Each query must contain only one tag:

- Depth Query (e.g., querying depth of node 5):
<query_depth>5</query_depth>

- Ancestor Query (e.g., asking if node 2 is an ancestor of node 8):
<query_ancestor>2,8</query_ancestor>

- Climb Query (e.g., climbing 2 steps up from node 7):
<query_climb>7,2</query_climb>

- Depth Comparison Query (e.g., comparing which of nodes 3 and 5 is closer to root):
<query_compare_depth>3,5</query_compare_depth>

When you are ready to answer the LCA for all node pairs, submit in the following format:

<answer>1:3, 2:1, 3:5</answer>

Where the numbers correspond to the LCA IDs for pairs 1 to {m}, separated by commas. The answer order must match the order of the given node pairs.

{pairs_description}

You may start your queries now.
"""

    contextualized_rule_zh_1 = """\
欢迎使用智能交通路网层级结构分析系统。本系统记录了一个以总枢纽（编号 1）为核心的辐射状交通路网，包含 {n} 个枢纽节点。
该路网规划遵循一个严格但未知的参数 k（k 大于等于 2）进行层级建设：
- 它是按规划批次（层序）编号的 k 叉干线网络在前 {n} 个节点上的截断。
- 对于编号 i 大于 1 的枢纽，其上级干线枢纽（父节点）的编号可通过统一公式计算得出（但公式中的 k 未知）。
- 任何枢纽的下级分支枢纽均在一个连续的编号区间内。

你的任务是通过最少次数的查询，推断出该路网的隐藏层级规律，并找出 {m} 对枢纽的“最近共同中转枢纽”（即最近公共祖先，LCA）。

每次查询仅可使用以下四种指令之一：

1. **层级深度查询**：查询枢纽 x 距离总枢纽的层级步数（总枢纽深度为 0）。
2. **干线判定**：查询枢纽 u 是否在枢纽 v 到总枢纽的干线上（u 等于 v 时返回"是"）。
3. **干线溯源**：从枢纽 x 沿干线向总枢纽移动 t 步，查询到达的上级枢纽编号（若超出总枢纽则返回"无"）。
4. **层级比较**：比较枢纽 u 和 v 谁距离总枢纽更近（或深度相同）。

所有查询的回答均由隐藏的路网结构唯一确定。

每次查询只能包含一个标签：

- 层级深度查询（例如查询枢纽 5 的深度）：
<query_depth>5</query_depth>

- 干线判定（例如查枢纽 2 是否为枢纽 8 的干线上级）：
<query_ancestor>2,8</query_ancestor>

- 干线溯源（例如从枢纽 7 向上级移动 2 步）：
<query_climb>7,2</query_climb>

- 层级比较（例如比较枢纽 3 和枢纽 5）：
<query_compare_depth>3,5</query_compare_depth>

当你准备好回答所有枢纽对的最近共同中转枢纽时，请按以下格式提交：

<answer>1:3, 2:1, 3:5</answer>

其中数字对应第 1 到第 {m} 对的共同中转枢纽编号，用逗号分隔。答案顺序必须与题目给出的枢纽对顺序一致。

{pairs_description}

请开始你的查询。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Transportation Network Hierarchical Analysis System. This system records a radial traffic network centered at the main hub (ID 1), containing {n} hub nodes.
The network construction follows a strict but unknown parameter k (k greater than or equal to 2):
- It is a truncated k-ary arterial network numbered in planning order (level order) up to {n} nodes.
- For hub i greater than 1, its upstream arterial hub (parent node) ID can be calculated by a uniform formula (but k is unknown).
- The downstream branch hubs of any hub lie in a contiguous range of IDs.

Your task is to infer the hidden hierarchical pattern with minimal queries and find the "lowest common transfer hub" (Lowest Common Ancestor, LCA) for {m} pairs of hubs.

You can use the following four types of queries (one query per turn):

1. **Hierarchy Depth Query**: Ask for the number of hierarchy steps from hub x to the main hub (main hub has depth 0).
2. **Arterial Query**: Ask whether hub u is on the arterial route from hub v to the main hub (returns "Yes" when u equals v).
3. **Arterial Trace Query**: Ask for the hub ID reached by moving t steps toward the main hub along the arterial route from hub x (returns "None" if it goes beyond the main hub).
4. **Hierarchy Comparison Query**: Ask which of hubs u and v is closer to the main hub (or if they are at the same depth).

All query answers are uniquely determined by the hidden network structure.

Each query must contain only one tag:

- Hierarchy Depth Query (e.g., querying depth of hub 5):
<query_depth>5</query_depth>

- Arterial Query (e.g., asking if hub 2 is an upstream arterial of hub 8):
<query_ancestor>2,8</query_ancestor>

- Arterial Trace Query (e.g., moving 2 steps upstream from hub 7):
<query_climb>7,2</query_climb>

- Hierarchy Comparison Query (e.g., comparing which of hubs 3 and 5 is closer to main hub):
<query_compare_depth>3,5</query_compare_depth>

When you are ready to answer the lowest common transfer hub for all pairs, submit in the following format:

<answer>1:3, 2:1, 3:5</answer>

Where the numbers correspond to the common transfer hub IDs for pairs 1 to {m}, separated by commas. The answer order must match the order of the given hub pairs.

{pairs_description}

You may start your queries now.
"""

    contextualized_rule_zh_2 = """\
欢迎进入病毒变异溯源分析系统。当前数据库记录了一棵病毒演化树，包含 {n} 种变异毒株，编号 1 为零号原始株。
该演化树遵循一种固定但未知的变异参数 k（k 大于等于 2）：
- 毒株是按发现顺序（层序）编号的 k 叉变异树在前 {n} 个节点上的截断。
- 对于编号 i 大于 1 的毒株，其直接变异来源（父节点）的编号由确定公式计算得出（但公式中的 k 未知）。
- 某毒株的直接衍生子代毒株均位于一个连续的编号区间内。

你的任务是通过有限次数的检验查询，推断出变异规律，并准确找出 {m} 对毒株的“最近共同变异祖先”（LCA）。

每次查询仅可使用以下四种指令之一：

1. **变异代数查询**：查询毒株 x 距离零号原始株的变异代数（原始株深度为 0）。
2. **溯源判定**：查询毒株 u 是否为毒株 v 的变异祖先（u 等于 v 时返回"是"）。
3. **代系追溯**：从毒株 x 向上追溯 t 代变异祖先，查询该祖先的编号（若越过原始株则返回"无"）。
4. **代数比较**：比较毒株 u 和 v 谁距离原始株的变异代数更少（或相同）。

所有查询的回答均由隐藏的病毒演化树唯一确定。

每次查询只能包含一个标签：

- 变异代数查询（例如查询毒株 5 的变异代数）：
<query_depth>5</query_depth>

- 溯源判定（例如查毒株 2 是否为毒株 8 的变异祖先）：
<query_ancestor>2,8</query_ancestor>

- 代系追溯（例如从毒株 7 向上追溯 2 代祖先）：
<query_climb>7,2</query_climb>

- 代数比较（例如比较毒株 3 和毒株 5）：
<query_compare_depth>3,5</query_compare_depth>

当你准备好回答所有毒株对的最近共同变异祖先时，请按以下格式提交：

<answer>1:3, 2:1, 3:5</answer>

其中数字对应第 1 到第 {m} 对的共同变异祖先毒株编号，用逗号分隔。答案顺序必须与题目给出的毒株对顺序一致。

{pairs_description}

请开始你的查询。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Virus Mutation Traceability Analysis System. The current database records a virus evolution tree containing {n} variants, with variant 1 being the patient zero strain.
The evolution tree follows a fixed but unknown mutation parameter k (k greater than or equal to 2):
- It is a truncated k-ary mutation tree numbered in discovery order (level order) up to {n} nodes.
- For variant i greater than 1, its direct mutation source (parent node) ID can be computed by a deterministic formula (but k is unknown).
- The direct derivative offspring of any variant lie in a contiguous range of IDs.

Your task is to infer the hidden mutation pattern through limited queries and accurately find the "lowest common mutation ancestor" (Lowest Common Ancestor, LCA) for {m} pairs of variants.

You can use the following four types of queries (one query per turn):

1. **Mutation Generation Query**: Ask for the number of mutation generations from variant x to patient zero (patient zero has depth 0).
2. **Traceability Query**: Ask whether variant u is a mutation ancestor of variant v (returns "Yes" when u equals v).
3. **Lineage Trace Query**: Ask for the ancestor ID reached by tracing t generations back from variant x (returns "None" if it goes beyond patient zero).
4. **Generation Comparison Query**: Ask which of variants u and v has fewer mutation generations from patient zero (or if they are the same).

All query answers are uniquely determined by the hidden evolution tree.

Each query must contain only one tag:

- Mutation Generation Query (e.g., querying generations of variant 5):
<query_depth>5</query_depth>

- Traceability Query (e.g., asking if variant 2 is an ancestor of variant 8):
<query_ancestor>2,8</query_ancestor>

- Lineage Trace Query (e.g., tracing 2 generations back from variant 7):
<query_climb>7,2</query_climb>

- Generation Comparison Query (e.g., comparing which of variants 3 and 5 is closer to patient zero):
<query_compare_depth>3,5</query_compare_depth>

When you are ready to answer the lowest common mutation ancestor for all pairs, submit in the following format:

<answer>1:3, 2:1, 3:5</answer>

Where the numbers correspond to the common ancestor IDs for pairs 1 to {m}, separated by commas. The answer order must match the order of the given variant pairs.

{pairs_description}

You may start your queries now.
"""

    contextualized_rule_zh_3 = """\
欢迎使用学科知识图谱分析系统。本系统内含一个学科知识前置依赖树，共 {n} 个知识点，其中知识点 1 是最核心的基础概念。
该知识树遵循一个隐藏的衍生难度参数 k（k 大于等于 2）：
- 它是一个按层级推进（层序）编号的 k 叉衍生结构，截断于前 {n} 个知识点。
- 对于编号 i 大于 1 的知识点，其直接前置知识点（父节点）的编号由固定公式决定（但公式中的 k 未知）。
- 任何知识点的直接后置衍生知识点在一段连续的编号区间内。

你需要通过最少次数的查询，推导出这门学科的隐藏衍生规律，并计算出 {m} 对知识点的“最近共同前置基础”（LCA）。

每次查询仅可使用以下四种指令之一：

1. **依赖层级查询**：查询知识点 x 距离核心基础概念的衍生层级（核心概念深度为 0）。
2. **前置判定**：查询知识点 u 是否为知识点 v 的前置基础（u 等于 v 时返回"是"）。
3. **前置溯源**：从知识点 x 向上追溯 t 层前置基础，查询其编号（若越过核心概念则返回"无"）。
4. **层级比较**：比较知识点 u 和 v 谁在知识树中更偏向核心基础层（或层级相同）。

所有查询的回答均由隐藏的学科知识树唯一确定。

每次查询只能包含一个标签：

- 依赖层级查询（例如查询知识点 5 的衍生层级）：
<query_depth>5</query_depth>

- 前置判定（例如查知识点 2 是否为知识点 8 的前置基础）：
<query_ancestor>2,8</query_ancestor>

- 前置溯源（例如从知识点 7 向上追溯 2 层基础）：
<query_climb>7,2</query_climb>

- 层级比较（例如比较知识点 3 和知识点 5）：
<query_compare_depth>3,5</query_compare_depth>

当你准备好回答所有知识点对的最近共同前置基础时，请按以下格式提交：

<answer>1:3, 2:1, 3:5</answer>

其中数字对应第 1 到第 {m} 对的共同前置基础知识点编号，用逗号分隔。答案顺序必须与题目给出的知识点对顺序一致。

{pairs_description}

请开始你的查询。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Subject Knowledge Graph Analysis System. This system contains a knowledge prerequisite dependency tree with {n} knowledge nodes, where node 1 is the core foundational concept.
The knowledge tree follows a hidden derivation difficulty parameter k (k greater than or equal to 2):
- It is a truncated k-ary derivation structure numbered in progressive progression (level order) up to {n} nodes.
- For node i greater than 1, its direct prerequisite knowledge node (parent node) ID is determined by a fixed formula (but k is unknown).
- The direct subsequent derivative nodes of any knowledge node lie in a contiguous range of IDs.

You need to deduce the hidden derivation pattern of this subject through minimal queries and calculate the "lowest common prerequisite foundation" (Lowest Common Ancestor, LCA) for {m} pairs of knowledge nodes.

You can use the following four types of queries (one query per turn):

1. **Dependency Level Query**: Ask for the derivation level from knowledge node x to the core concept (core concept has depth 0).
2. **Prerequisite Query**: Ask whether node u is a prerequisite foundation of node v (returns "Yes" when u equals v).
3. **Prerequisite Trace Query**: Ask for the node ID reached by tracing t prerequisite levels back from node x (returns "None" if it goes beyond the core concept).
4. **Level Comparison Query**: Ask which of nodes u and v leans more towards the core foundation in the knowledge tree (or if they are at the same level).

All query answers are uniquely determined by the hidden knowledge tree.

Each query must contain only one tag:

- Dependency Level Query (e.g., querying level of node 5):
<query_depth>5</query_depth>

- Prerequisite Query (e.g., asking if node 2 is a prerequisite of node 8):
<query_ancestor>2,8</query_ancestor>

- Prerequisite Trace Query (e.g., tracing 2 prerequisite levels back from node 7):
<query_climb>7,2</query_climb>

- Level Comparison Query (e.g., comparing which of nodes 3 and 5 is closer to core concept):
<query_compare_depth>3,5</query_compare_depth>

When you are ready to answer the lowest common prerequisite foundation for all pairs, submit in the following format:

<answer>1:3, 2:1, 3:5</answer>

Where the numbers correspond to the common prerequisite IDs for pairs 1 to {m}, separated by commas. The answer order must match the order of the given knowledge node pairs.

{pairs_description}

You may start your queries now.
"""

    contextualized_rule_zh_4 = """\
欢迎使用智能制造物料清单(BOM)分析系统。这里记录了一个产品的装配结构树，包含 {n} 个组件/零件，编号 1 代表最终完整产品（顶层总成）。
该装配树遵循统一但未知的拆解参数 k（k 大于等于 2）：
- 它是按装配拆解层级（层序）编号的 k 叉树在前 {n} 个节点上的截断。
- 对于编号 i 大于 1 的零件，其直接所属上级组件（父节点）的编号由确定公式得出（但公式中的 k 未知）。
- 某组件包含的下一级子零件在一个连续的编号区间内。

你的目标是利用有限的结构查询，推断出 BOM 表的拆解层级规律，并找出 {m} 对零件的“最近共同所属总成”（LCA）。

每次查询仅可使用以下四种指令之一：

1. **拆解层级查询**：查询零件 x 距离最终完整产品的拆解深度（最终产品深度为 0）。
2. **从属判定**：查询组件 u 是否包含零件 v，即 u 是否为 v 的上级总成（u 等于 v 时返回"是"）。
3. **总成追溯**：从零件 x 向上级装配追溯 t 层，查询该上级组件的编号（若越过最终产品则返回"无"）。
4. **层级比较**：比较组件/零件 u 和 v 谁在 BOM 树中更接近最终完整产品（或层级相同）。

所有查询的回答均由隐藏的装配结构树唯一确定。

每次查询只能包含一个标签：

- 拆解层级查询（例如查询零件 5 的拆解层级）：
<query_depth>5</query_depth>

- 从属判定（例如查组件 2 是否为零件 8 的上级总成）：
<query_ancestor>2,8</query_ancestor>

- 总成追溯（例如从零件 7 向上级追溯 2 层组件）：
<query_climb>7,2</query_climb>

- 层级比较（例如比较零件 3 和零件 5）：
<query_compare_depth>3,5</query_compare_depth>

当你准备好回答所有零件对的最近共同所属总成时，请按以下格式提交：

<answer>1:3, 2:1, 3:5</answer>

其中数字对应第 1 到第 {m} 对的共同所属总成组件编号，用逗号分隔。答案顺序必须与题目给出的零件对顺序一致。

{pairs_description}

请开始你的查询。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart Manufacturing Bill of Materials (BOM) Analysis System. Here is recorded an assembly structure tree of a product, containing {n} components/parts, where ID 1 represents the final assembled product (top-level assembly).
The assembly tree follows a uniform but unknown disassembly parameter k (k greater than or equal to 2):
- It is a truncated k-ary tree numbered in assembly disassembly level (level order) up to {n} nodes.
- For part i greater than 1, its direct parent component (parent node) ID is derived from a deterministic formula (but k is unknown).
- The direct sub-parts contained within a certain component lie in a contiguous range of IDs.

Your goal is to infer the disassembly level pattern of the BOM with limited structural queries and find the "lowest common parent assembly" (Lowest Common Ancestor, LCA) for {m} pairs of parts.

You can use the following four types of queries (one query per turn):

1. **Disassembly Level Query**: Ask for the disassembly depth of part x from the final product (final product has depth 0).
2. **Subordination Query**: Ask whether component u contains part v, i.e., whether u is a parent assembly of v (returns "Yes" when u equals v).
3. **Assembly Trace Query**: Ask for the parent component ID reached by tracing t assembly levels up from part x (returns "None" if it goes beyond the final product).
4. **Level Comparison Query**: Ask which of components/parts u and v is closer to the final assembled product in the BOM tree (or if they are at the same level).

All query answers are uniquely determined by the hidden assembly tree.

Each query must contain only one tag:

- Disassembly Level Query (e.g., querying disassembly level of part 5):
<query_depth>5</query_depth>

- Subordination Query (e.g., asking if component 2 contains part 8):
<query_ancestor>2,8</query_ancestor>

- Assembly Trace Query (e.g., tracing 2 levels up from part 7):
<query_climb>7,2</query_climb>

- Level Comparison Query (e.g., comparing which of parts 3 and 5 is closer to final product):
<query_compare_depth>3,5</query_compare_depth>

When you are ready to answer the lowest common parent assembly for all pairs, submit in the following format:

<answer>1:3, 2:1, 3:5</answer>

Where the numbers correspond to the common parent assembly IDs for pairs 1 to {m}, separated by commas. The answer order must match the order of the given part pairs.

{pairs_description}

You may start your queries now.
"""

    contextualized_rule_zh_5 = """\
欢迎使用法律法规效力渊源分析系统。本系统包含一棵法律效力衍生树，收录 {n} 条法律规范，条款 1 代表根本大法（如宪法或基本法）。
该法律树根据立法权限遵循一个隐藏参数 k（k 大于等于 2）：
- 它是按效力层级和颁布顺序（层序）编号的 k 叉衍生树在前 {n} 个节点上的截断。
- 对于编号 i 大于 1 的条款，其直接上位法渊源（父节点）的编号由严密公式推算（但公式中的 k 未知）。
- 任何条款的直接下位实施细则或衍生条款均在一个连续的编号区间内。

请通过最少次数的法理查询，掌握该法律体系的衍生规律，并裁定出 {m} 对细则/条款的“最近共同上位法渊源”（LCA）。

每次查询仅可使用以下四种指令之一：

1. **效力层级查询**：查询条款 x 距离根本大法的衍生层级（根本大法深度为 0）。
2. **渊源判定**：查询条款 u 是否为条款 v 的上位法渊源（u 等于 v 时返回"是"）。
3. **渊源溯源**：从条款 x 向上位法方向追溯 t 个层级，查询其渊源条款编号（若越过根本大法则返回"无"）。
4. **层级比较**：比较条款 u 和 v 谁的法律效力层级更高，即更接近根本大法（或层级相同）。

所有查询的回答均由隐藏的法律效力树唯一确定。

每次查询只能包含一个标签：

- 效力层级查询（例如查询条款 5 的层级）：
<query_depth>5</query_depth>

- 渊源判定（例如查条款 2 是否为条款 8 的上位法渊源）：
<query_ancestor>2,8</query_ancestor>

- 渊源溯源（例如从条款 7 向上位法追溯 2 层）：
<query_climb>7,2</query_climb>

- 层级比较（例如比较条款 3 和条款 5）：
<query_compare_depth>3,5</query_compare_depth>

当你准备好回答所有条款对的最近共同上位法渊源时，请按以下格式提交：

<answer>1:3, 2:1, 3:5</answer>

其中数字对应第 1 到第 {m} 对的共同上位法条款编号，用逗号分隔。答案顺序必须与题目给出的条款对顺序一致。

{pairs_description}

请开始你的查询。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Legal Source and Efficacy Analysis System. This system contains a legal efficacy derivation tree encompassing {n} legal norms, where clause 1 represents the fundamental law (e.g., Constitution or Basic Law).
The legal tree follows a hidden legislative parameter k (k greater than or equal to 2):
- It is a truncated k-ary derivation tree numbered by efficacy level and promulgation order (level order) up to {n} nodes.
- For clause i greater than 1, its direct higher-level legal source (parent node) ID is calculated by a strict formula (but k is unknown).
- The direct lower-level implementation rules or derivative clauses of any norm lie in a contiguous range of IDs.

Please master the derivation pattern of this legal system through minimal jurisprudential queries, and adjudicate the "lowest common higher-level legal source" (Lowest Common Ancestor, LCA) for {m} pairs of clauses.

You can use the following four types of queries (one query per turn):

1. **Efficacy Level Query**: Ask for the derivation level of clause x from the fundamental law (fundamental law has depth 0).
2. **Legal Source Query**: Ask whether clause u is a higher-level legal source of clause v (returns "Yes" when u equals v).
3. **Source Trace Query**: Ask for the source clause ID reached by tracing t levels upward to higher-level laws from clause x (returns "None" if it goes beyond the fundamental law).
4. **Level Comparison Query**: Ask which of clauses u and v has higher legal efficacy, i.e., is closer to the fundamental law (or if they are at the same level).

All query answers are uniquely determined by the hidden legal efficacy tree.

Each query must contain only one tag:

- Efficacy Level Query (e.g., querying level of clause 5):
<query_depth>5</query_depth>

- Legal Source Query (e.g., asking if clause 2 is a higher-level source of clause 8):
<query_ancestor>2,8</query_ancestor>

- Source Trace Query (e.g., tracing 2 levels upward from clause 7):
<query_climb>7,2</query_climb>

- Level Comparison Query (e.g., comparing which of clauses 3 and 5 is closer to fundamental law):
<query_compare_depth>3,5</query_compare_depth>

When you are ready to answer the lowest common higher-level legal source for all pairs, submit in the following format:

<answer>1:3, 2:1, 3:5</answer>

Where the numbers correspond to the common source clause IDs for pairs 1 to {m}, separated by commas. The answer order must match the order of the given clause pairs.

{pairs_description}

You may start your queries now.
"""

    tags = ["answer", "query_depth", "query_ancestor", "query_climb", "query_compare_depth"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "k": 2,
                "pairs": [(3, 5), (2, 7), (4, 6)],
            },
            2: {
                "n": 15,
                "k": 3,
                "pairs": [(5, 9), (8, 14), (3, 11), (6, 7)],
            },
            3: {
                "n": 22,
                "k": 4,
                "pairs": [(6, 14), (10, 18), (3, 21), (9, 13), (2, 22)],
            },
            4: {
                "n": 26,
                "k": 5,
                "pairs": [(8, 15), (12, 22), (4, 19), (7, 26), (11, 13), (3, 20)],
            },
            5: {
                "n": 31,
                "k": 6,
                "pairs": [(9, 18), (14, 25), (5, 28), (11, 21), (8, 30), (3, 19), (7, 24)],
            },
        },
        "en": {
            1: {
                "n": 7,
                "k": 2,
                "pairs": [(3, 5), (2, 7), (4, 6)],
            },
            2: {
                "n": 15,
                "k": 3,
                "pairs": [(5, 9), (8, 14), (3, 11), (6, 7)],
            },
            3: {
                "n": 22,
                "k": 4,
                "pairs": [(6, 14), (10, 18), (3, 21), (9, 13), (2, 22)],
            },
            4: {
                "n": 26,
                "k": 5,
                "pairs": [(8, 15), (12, 22), (4, 19), (7, 26), (11, 13), (3, 20)],
            },
            5: {
                "n": 31,
                "k": 6,
                "pairs": [(9, 18), (14, 25), (5, 28), (11, 21), (8, 30), (3, 19), (7, 24)],
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
        self.n = cfg["n"]
        self.k = cfg["k"]
        self.pairs = cfg["pairs"]
        
        self._game_info["n"] = self.n
        self._game_info["m"] = len(self.pairs)
        
        self._build_tree()
        
        self._compute_ground_truth()
        
        self._generate_pairs_description()
        
        self.query_count = 0

    def _build_tree(self):
        self.parent = {1: 0}
        self.depth = {1: 0}
        
        for i in range(2, self.n + 1):
            p = (i - 2) // self.k + 1
            self.parent[i] = p
            self.depth[i] = self.depth[p] + 1

    def _compute_ground_truth(self):
        self.ground_truth_lcas = []
        
        for a, b in self.pairs:
            lca = self._compute_lca(a, b)
            self.ground_truth_lcas.append(lca)

    def _compute_lca(self, u, v):
        while self.depth[u] > self.depth[v]:
            u = self.parent[u]
        while self.depth[v] > self.depth[u]:
            v = self.parent[v]
        
        while u != v:
            u = self.parent[u]
            v = self.parent[v]
        
        return u

    def _generate_pairs_description(self):
        if self.config.language == "zh":
            lines = []
            for idx, (a, b) in enumerate(self.pairs, 1):
                lines.append(f"第 {idx} 对：节点 {a} 和节点 {b}")
            self._game_info["pairs_description"] = "\n".join(lines)
        else:
            lines = []
            for idx, (a, b) in enumerate(self.pairs, 1):
                lines.append(f"Pair {idx}: node {a} and node {b}")
            self._game_info["pairs_description"] = "\n".join(lines)

    def _is_ancestor(self, u, v):
        current = v
        while current != 0:
            if current == u:
                return True
            if current == 1:
                break
            current = self.parent[current]
        return False

    def _climb_up(self, x, t):
        current = x
        for _ in range(t):
            if current == 1:
                return None
            if current == 0:
                return None
            current = self.parent[current]
        return current

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            if len(parts) != len(self.pairs):
                return False
            
            model_lcas = []
            for part in parts:
                if ":" not in part:
                    return False
                idx_str, lca_str = part.split(":", 1)
                idx = int(idx_str.strip())
                lca = int(lca_str.strip())
                model_lcas.append((idx, lca))
            
            model_lcas.sort(key=lambda x: x[0])
            for i, (idx, lca) in enumerate(model_lcas, 1):
                if idx != i:
                    return False
                if lca != self.ground_truth_lcas[i - 1]:
                    return False
            
            return True
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        self.query_count += 1
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            none_res = "无"
            same_res = "相同"
            error_res = "错误：无效的查询格式或节点编号超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            none_res = "None"
            same_res = "Same"
            error_res = "Error: Invalid query format or node ID out of range."

        if "query_depth" in parsed_info:
            try:
                x = int(parsed_info["query_depth"].strip())
                if x < 1 or x > self.n:
                    return error_res
                return str(self.depth[x])
            except:
                return error_res

        elif "query_ancestor" in parsed_info:
            try:
                raw = parsed_info["query_ancestor"]
                u, v = [int(x.strip()) for x in raw.split(",")]
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return error_res
                return yes_res if self._is_ancestor(u, v) else no_res
            except:
                return error_res

        elif "query_climb" in parsed_info:
            try:
                raw = parsed_info["query_climb"]
                x, t = [int(x.strip()) for x in raw.split(",")]
                if x < 1 or x > self.n or t < 0:
                    return error_res
                result = self._climb_up(x, t)
                return none_res if result is None else str(result)
            except:
                return error_res

        elif "query_compare_depth" in parsed_info:
            try:
                raw = parsed_info["query_compare_depth"]
                u, v = [int(x.strip()) for x in raw.split(",")]
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return error_res
                
                if self.depth[u] < self.depth[v]:
                    return "u"
                elif self.depth[u] > self.depth[v]:
                    return "v"
                else:
                    return same_res
            except:
                return error_res

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        val_lower = correct.lower()
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
            elif correct == "相同":
                return "u"
        else:
            if val_lower == "yes":
                return "No"
            elif val_lower == "no":
                return "Yes"
            elif val_lower == "same":
                return "u"
                
        if correct == "u":
            return "v"
        if correct == "v":
            return "u"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            none_res = "无"
            same_res = "相同"
        else:
            yes_res, no_res = "Yes", "No"
            none_res = "None"
            same_res = "Same"

        for x in range(1, self.n + 1):
            query_str = f"<query_depth>{x}</query_depth>"
            answer_str = str(self.depth[x])
            results.append({"query": query_str, "answer": answer_str})
        
        for u in range(1, self.n + 1):
            for v in range(1, self.n + 1):
                query_str = f"<query_ancestor>{u},{v}</query_ancestor>"
                is_anc = self._is_ancestor(u, v)
                answer_str = yes_res if is_anc else no_res
                results.append({"query": query_str, "answer": answer_str})

        for x in range(1, self.n + 1):
            max_climb = self.depth[x] + 1
            for t in range(1, max_climb + 2):
                query_str = f"<query_climb>{x},{t}</query_climb>"
                result_node = self._climb_up(x, t)
                if result_node is None:
                    answer_str = none_res
                else:
                    answer_str = str(result_node)
                results.append({"query": query_str, "answer": answer_str})

        for u in range(1, self.n + 1):
            for v in range(1, self.n + 1):
                if u == v:
                    continue
                query_str = f"<query_compare_depth>{u},{v}</query_compare_depth>"
                d_u = self.depth[u]
                d_v = self.depth[v]
                if d_u < d_v:
                    answer_str = "u"
                elif d_u > d_v:
                    answer_str = "v"
                else:
                    answer_str = same_res
                results.append({"query": query_str, "answer": answer_str})
        
        return results