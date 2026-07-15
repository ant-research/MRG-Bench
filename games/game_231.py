from .base import Game
import random

class TreeHeightInferenceGame(Game):
    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树高度推断"的推理游戏，规则如下：

游戏设定了一个未知的有限有根树 T。树的高度 H 定义为从根节点到任一节点的最长路径的边数。

存在两个未知的整数参数 a（大于等于1）和 c（大于等于0）。对于树中的任一节点 u，你可以观察到一个值 P(u)，该值由公式 P(u) = a × h(u) + c 计算得出，其中 h(u) 表示以 u 为根的子树高度（即从 u 到其最深后代的边数）。

你的目标是通过交互式查询和在树上移动，推断出整棵树的高度 H。

你的初始位置在根节点。

你可以执行以下操作（每次只能执行一个操作）：

1. **查询子节点数**：返回当前节点的子节点数量（非负整数）。
2. **查询观察值**：返回当前节点的观察值（非负整数）。
3. **下移到第 k 个子节点**：如果当前节点有子节点，你可以移动到第 k 个子节点（k 从 1 开始计数）。如果 k 超出范围，操作无效。
4. **上移到父节点**：如果当前节点不是根节点，你可以移动到其父节点。如果已在根节点，操作无效。
5. **回到根节点**：将位置重置为根节点。
6. **声明答案**：提交你推断出的树高度 H。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 查询子节点数：
<query_children></query_children>

- 查询观察值：
<query_observation></query_observation>

- 下移到第 k 个子节点（例如移动到第 2 个子节点）：
<move_down>2</move_down>

- 上移到父节点：
<move_up></move_up>

- 回到根节点：
<move_root></move_root>

- 声明答案（例如声明树高度为 5）：
<answer>5</answer>

- 树结构、参数 a 和 c 在整个游戏过程中保持不变。
- 你需要通过尽可能少的操作来推断出树的高度 H。
- 如果声明的答案错误，游戏失败。
"""

    game_rule_en = """\
Let's play a "Tree Height Inference" deduction game. Here are the rules:

The game is set on an unknown finite rooted tree T. The height H of the tree is defined as the maximum number of edges from the root to any node.

There are two unknown integer parameters a (greater than or equal to 1) and c (greater than or equal to 0). For any node u in the tree, you can observe a value P(u), which is calculated by the formula P(u) = a × h(u) + c, where h(u) represents the height of the subtree rooted at u (i.e., the number of edges from u to its deepest descendant).

Your goal is to infer the height H of the entire tree through interactive queries and movements on the tree.

Your initial position is at the root node.

You can perform the following operations (one operation per turn):

1. **Query children count**: Returns the number of children of the current node (non-negative integer).
2. **Query observation value**: Returns the observation value of the current node (non-negative integer).
3. **Move down to the k-th child**: If the current node has children, you can move to the k-th child (k starts from 1). If k is out of range, the operation is invalid.
4. **Move up to parent**: If the current node is not the root, you can move to its parent. If already at root, the operation is invalid.
5. **Move to root**: Reset position to the root node.
6. **Declare answer**: Submit your inferred tree height H.

Each operation must contain only one tag. Use the following XML format:

- Query children count:
<query_children></query_children>

- Query observation value:
<query_observation></query_observation>

- Move down to the k-th child (e.g., move to the 2nd child):
<move_down>2</move_down>

- Move up to parent:
<move_up></move_up>

- Move to root:
<move_root></move_root>

- Declare answer (e.g., declare tree height as 5):
<answer>5</answer>

- The tree structure, parameters a and c remain constant throughout the game.
- You need to infer the tree height H with as few operations as possible.
- If the declared answer is incorrect, the game fails.
"""

    contextualized_rule_zh_1 = """\
欢迎进入“城市交通路网层级分析”系统。

本系统映射了一个未知的封闭城市交通分流路网 T（可视为一棵有限有根树）。路网的最大分流层级 H 定义为从主干道入口（根节点）到末端任一道路（叶子节点）的最长路径的分流节点数（边数）。

存在两个未知的系统参数 a（大于等于1）和 c（大于等于0）。对于路网中的任一分流节点 u，系统会根据后续路况生成一个拥堵预估指数 P(u)，该指数由公式 P(u) = a × h(u) + c 计算得出，其中 h(u) 表示以 u 为起点的子路网的最大连续分流层级（即从 u 到其最深末端道路的边数）。

你的目标是通过交互式查询和在路网节点间移动，推断出整个交通分流路网的最大分流层级 H。

你的初始位置在主干道入口（根节点）。

你可以执行以下操作（每次只能执行一个操作）：

1. **查询下游分流路径数**：返回当前路口分流出的下游道路数量（非负整数）。
2. **查询拥堵预估指数**：返回当前分流节点的拥堵预估指数（非负整数）。
3. **驶入第 k 条下游道路**：如果当前节点有下游分流，你可以驶入第 k 条道路（k 从 1 开始计数）。如果 k 超出范围，操作无效。
4. **回退到上一级路口**：如果当前节点不是主干道入口，你可以回退到其直接上级路口。如果已在入口，操作无效。
5. **回到主干道入口**：将位置重置为路网的主干道入口。
6. **声明分析结果**：提交你推断出的路网最大分流层级 H。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 查询下游分流路径数：
<query_children></query_children>

- 查询拥堵预估指数：
<query_observation></query_observation>

- 驶入第 k 条下游道路（例如驶入第 2 条道路）：
<move_down>2</move_down>

- 回退到上一级路口：
<move_up></move_up>

- 回到主干道入口：
<move_root></move_root>

- 声明分析结果（例如声明层级为 5）：
<answer>5</answer>

- 路网结构、参数 a 和 c 在整个分析过程中保持不变。
- 你需要通过尽可能少的操作来推断出路网的最大分流层级 H。
- 如果声明的分析结果错误，系统研判失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Network Hierarchy Analysis" system.

This system maps an unknown closed urban traffic distribution network T (which can be viewed as a finite rooted tree). The maximum distribution hierarchy H of the network is defined as the maximum number of distribution nodes (edges) from the main arterial entrance (root node) to any terminal road (leaf node).

There are two unknown system parameters a (greater than or equal to 1) and c (greater than or equal to 0). For any distribution node u in the network, the system generates an estimated congestion index P(u), which is calculated by the formula P(u) = a × h(u) + c, where h(u) represents the maximum continuous distribution hierarchy of the sub-network starting from u (i.e., the number of edges from u to its deepest terminal road).

Your goal is to infer the maximum distribution hierarchy H of the entire traffic network through interactive queries and moving between network nodes.

Your initial position is at the main arterial entrance (root node).

You can perform the following operations (one operation per turn):

1. **Query downstream branches count**: Returns the number of downstream roads branching from the current intersection (non-negative integer).
2. **Query estimated congestion index**: Returns the estimated congestion index of the current distribution node (non-negative integer).
3. **Drive into the k-th downstream road**: If the current node has downstream branches, you can move to the k-th road (k starts from 1). If k is out of range, the operation is invalid.
4. **Return to the previous intersection**: If the current node is not the main entrance, you can move to its immediate upstream intersection. If already at the entrance, the operation is invalid.
5. **Return to the main entrance**: Reset position to the main arterial entrance.
6. **Declare analysis result**: Submit your inferred maximum distribution hierarchy H.

Each operation must contain only one tag. Use the following XML format:

- Query downstream branches count:
<query_children></query_children>

- Query estimated congestion index:
<query_observation></query_observation>

- Drive into the k-th downstream road (e.g., move to the 2nd road):
<move_down>2</move_down>

- Return to the previous intersection:
<move_up></move_up>

- Return to the main entrance:
<move_root></move_root>

- Declare analysis result (e.g., declare hierarchy as 5):
<answer>5</answer>

- The network structure, parameters a and c remain constant throughout the analysis.
- You need to infer the maximum distribution hierarchy H with as few operations as possible.
- If the declared result is incorrect, the system analysis fails.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“罕见综合征病理演变推演”辅助诊断系统。

本系统构建了一个未知的病理演变树 T。病理演变的最大阶段数 H 定义为从初始症状（根节点）到任一终末期亚型（叶子节点）的最长演化步数（边数）。

存在两个未知的生理参数 a（大于等于1）和 c（大于等于0）。对于演变树中的任一病理阶段 u，你可以测得一个病情复杂度评分 P(u)，该评分由公式 P(u) = a × h(u) + c 计算得出，其中 h(u) 表示以 u 为起点的后续最大演化步数（即从 u 到其最深终末期亚型的边数）。

你的目标是通过交互式病理特征查询和演变节点回溯，推断出整类综合征的病理演变最大阶段数 H。

你的初始位置在综合征的初始症状阶段（根节点）。

你可以执行以下操作（每次只能执行一个操作）：

1. **查询亚型分支数**：返回当前病理阶段可演化出的下级亚型分支数量（非负整数）。
2. **查询病情复杂度评分**：返回当前病理阶段的病情复杂度评分（非负整数）。
3. **深入第 k 个亚型分支**：如果当前阶段有进一步演化的亚型，你可以追踪第 k 个亚型分支（k 从 1 开始计数）。如果 k 超出范围，操作无效。
4. **回溯到上一级病理阶段**：如果当前不是初始症状，你可以回退到引发当前阶段的上一级阶段。如果已在初始症状，操作无效。
5. **回到初始症状阶段**：将分析位置重置为初始症状（根节点）。
6. **声明诊断结论**：提交你推断出的最大病理演变阶段数 H。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 查询亚型分支数：
<query_children></query_children>

- 查询病情复杂度评分：
<query_observation></query_observation>

- 深入第 k 个亚型分支（例如追踪第 2 个分支）：
<move_down>2</move_down>

- 回溯到上一级病理阶段：
<move_up></move_up>

- 回到初始症状阶段：
<move_root></move_root>

- 声明诊断结论（例如声明阶段数为 5）：
<answer>5</answer>

- 演变结构、参数 a 和 c 在整个推演过程中保持不变。
- 你需要通过尽可能少的操作来推断出病理演变的最大阶段数 H。
- 如果声明的阶段数错误，推演失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Rare Syndrome Pathological Evolution Deduction" auxiliary diagnostic system.

This system constructs an unknown pathological evolution tree T. The maximum number of evolution stages H is defined as the maximum number of evolutionary steps (edges) from the initial symptom (root node) to any terminal subtype (leaf node).

There are two unknown physiological parameters a (greater than or equal to 1) and c (greater than or equal to 0). For any pathological stage u in the evolution tree, you can measure a disease complexity score P(u), which is calculated by the formula P(u) = a × h(u) + c, where h(u) represents the maximum number of subsequent evolutionary steps starting from u (i.e., the number of edges from u to its deepest terminal subtype).

Your goal is to infer the maximum number of pathological evolution stages H of the entire syndrome through interactive pathological feature queries and evolutionary node backtracking.

Your initial position is at the initial symptom stage (root node).

You can perform the following operations (one operation per turn):

1. **Query subtype branches count**: Returns the number of subordinate subtype branches that can evolve from the current pathological stage (non-negative integer).
2. **Query disease complexity score**: Returns the disease complexity score of the current pathological stage (non-negative integer).
3. **Delve into the k-th subtype branch**: If the current stage has further evolving subtypes, you can track the k-th subtype branch (k starts from 1). If k is out of range, the operation is invalid.
4. **Backtrack to the previous pathological stage**: If the current node is not the initial symptom, you can move back to the preceding stage that triggered it. If already at the initial symptom, the operation is invalid.
5. **Return to the initial symptom stage**: Reset the analysis position to the initial symptom (root node).
6. **Declare diagnostic conclusion**: Submit your inferred maximum number of pathological evolution stages H.

Each operation must contain only one tag. Use the following XML format:

- Query subtype branches count:
<query_children></query_children>

- Query disease complexity score:
<query_observation></query_observation>

- Delve into the k-th subtype branch (e.g., track the 2nd branch):
<move_down>2</move_down>

- Backtrack to the previous pathological stage:
<move_up></move_up>

- Return to the initial symptom stage:
<move_root></move_root>

- Declare diagnostic conclusion (e.g., declare 5 stages):
<answer>5</answer>

- The evolutionary structure, parameters a and c remain constant throughout the deduction process.
- You need to infer the maximum number of pathological evolution stages H with as few operations as possible.
- If the declared conclusion is incorrect, the deduction fails.
"""

    contextualized_rule_zh_3 = """\
欢迎进入“学科知识图谱深度测评”系统。

本系统加载了一个未知的特定学科先决知识依赖树 T。知识图谱的最大细分层级 H 定义为从宏观学科顶层（根节点）到任一最底层微观知识点（叶子节点）的最长衍生边数。

存在两个未知的评估参数 a（大于等于1）和 c（大于等于0）。对于知识图谱中的任一知识节点 u，系统会给出一个学习耗时评估值 P(u)，该评估值由公式 P(u) = a × h(u) + c 计算得出，其中 h(u) 表示以 u 为先决条件的子知识图谱的最大细分层级（即从 u 到其最深衍生微观知识点的边数）。

你的目标是通过交互式查询和在知识结构间跳转，推断出整个学科图谱的最大细分层级 H。

你的初始位置在宏观学科顶层（根节点）。

你可以执行以下操作（每次只能执行一个操作）：

1. **查询直接衍生知识点数**：返回当前知识节点直接细分的下级知识点数量（非负整数）。
2. **查询学习耗时评估值**：返回当前知识节点的学习耗时评估值（非负整数）。
3. **钻取到第 k 个衍生知识点**：如果当前节点有进一步细分的知识点，你可以钻取到第 k 个下级知识点（k 从 1 开始计数）。如果 k 超出范围，操作无效。
4. **返回父级知识节点**：如果当前不是宏观学科顶层，你可以退回到其先决父级知识节点。如果已在顶层，操作无效。
5. **回到宏观学科顶层**：将位置重置为知识图谱的宏观学科顶层。
6. **声明测评结果**：提交你推断出的最大细分层级 H。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 查询直接衍生知识点数：
<query_children></query_children>

- 查询学习耗时评估值：
<query_observation></query_observation>

- 钻取到第 k 个衍生知识点（例如钻取到第 2 个知识点）：
<move_down>2</move_down>

- 返回父级知识节点：
<move_up></move_up>

- 回到宏观学科顶层：
<move_root></move_root>

- 声明测评结果（例如声明层级为 5）：
<answer>5</answer>

- 图谱结构、参数 a 和 c 在整个测评过程中保持不变。
- 你需要通过尽可能少的操作来推断出图谱的最大细分层级 H。
- 如果声明的层级结果错误，测评失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Subject Knowledge Graph Depth Assessment" system.

This system loads an unknown prerequisite knowledge dependency tree T for a specific subject. The maximum subdivision depth H of the knowledge graph is defined as the maximum number of derivative edges from the macroscopic subject top-level (root node) to any most microscopic knowledge point (leaf node).

There are two unknown assessment parameters a (greater than or equal to 1) and c (greater than or equal to 0). For any knowledge node u in the graph, the system provides an estimated learning time value P(u), which is calculated by the formula P(u) = a × h(u) + c, where h(u) represents the maximum subdivision depth of the sub-knowledge graph with u as the prerequisite (i.e., the number of edges from u to its deepest derivative microscopic knowledge point).

Your goal is to infer the maximum subdivision depth H of the entire subject graph through interactive queries and jumping between knowledge structures.

Your initial position is at the macroscopic subject top-level (root node).

You can perform the following operations (one operation per turn):

1. **Query direct derivative knowledge points count**: Returns the number of directly subdivided subordinate knowledge points of the current node (non-negative integer).
2. **Query estimated learning time value**: Returns the estimated learning time value of the current knowledge node (non-negative integer).
3. **Drill down to the k-th derivative knowledge point**: If the current node has further subdivided knowledge points, you can drill down to the k-th subordinate node (k starts from 1). If k is out of range, the operation is invalid.
4. **Return to the parent knowledge node**: If the current node is not the top-level, you can return to its prerequisite parent node. If already at the top-level, the operation is invalid.
5. **Return to the macroscopic subject top-level**: Reset position to the top-level of the knowledge graph.
6. **Declare assessment result**: Submit your inferred maximum subdivision depth H.

Each operation must contain only one tag. Use the following XML format:

- Query direct derivative knowledge points count:
<query_children></query_children>

- Query estimated learning time value:
<query_observation></query_observation>

- Drill down to the k-th derivative knowledge point (e.g., drill down to the 2nd point):
<move_down>2</move_down>

- Return to the parent knowledge node:
<move_up></move_up>

- Return to the macroscopic subject top-level:
<move_root></move_root>

- Declare assessment result (e.g., declare depth as 5):
<answer>5</answer>

- The graph structure, parameters a and c remain constant throughout the assessment.
- You need to infer the maximum subdivision depth H with as few operations as possible.
- If the declared depth is incorrect, the assessment fails.
"""

    contextualized_rule_zh_4 = """\
欢迎访问“复杂装备BOM（物料清单）架构测算”终端。

本终端载入了一个未知的工业装备的BOM装配树 T。装备的最大装配深度 H 定义为从最终成品（根节点）到任一不可再分的基础零件（叶子节点）的最长嵌套装配层数（边数）。

存在两个未知的工艺参数 a（大于等于1）和 c（大于等于0）。对于BOM树中的任一组件 u，控制台会输出一个加工耗时预估指标 P(u)，该指标由公式 P(u) = a × h(u) + c 计算得出，其中 h(u) 表示以 u 为顶层部件的子装配体的最大嵌套层数（即从 u 到其最底端基础零件的边数）。

你的目标是通过交互式工艺查询和拆解组件结构，推断出整套复杂装备的最大装配深度 H。

你的初始位置在最终成品（根节点）。

你可以执行以下操作（每次只能执行一个操作）：

1. **查询子组件数量**：返回构成当前组件所需的直接下级子组件数量（非负整数）。
2. **查询加工耗时预估指标**：返回当前组件的加工耗时预估指标（非负整数）。
3. **拆解到第 k 个子组件**：如果当前组件还可以再细分，你可以拆解查看第 k 个子组件（k 从 1 开始计数）。如果 k 超出范围，操作无效。
4. **返回上级装配组件**：如果当前查看的不是最终成品，你可以返回到其直接上级组件。如果已在最终成品级别，操作无效。
5. **复原至最终成品**：将层级视野重置为最终成品级别（根节点）。
6. **声明架构测算结果**：提交你推断出的最大装配深度 H。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 查询子组件数量：
<query_children></query_children>

- 查询加工耗时预估指标：
<query_observation></query_observation>

- 拆解到第 k 个子组件（例如拆解第 2 个子组件）：
<move_down>2</move_down>

- 返回上级装配组件：
<move_up></move_up>

- 复原至最终成品：
<move_root></move_root>

- 声明架构测算结果（例如声明深度为 5）：
<answer>5</answer>

- BOM结构、工艺参数 a 和 c 在整个测算过程中保持不变。
- 你需要通过尽可能少的操作来推断出装备的最大装配深度 H。
- 如果声明的深度测算结果错误，任务失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Complex Equipment BOM (Bill of Materials) Architecture Calculation" terminal.

This terminal loads an unknown BOM assembly tree T of industrial equipment. The maximum assembly depth H of the equipment is defined as the maximum number of nested assembly layers (edges) from the final product (root node) to any indivisible basic part (leaf node).

There are two unknown process parameters a (greater than or equal to 1) and c (greater than or equal to 0). For any component u in the BOM tree, the console outputs an estimated machining time index P(u), which is calculated by the formula P(u) = a × h(u) + c, where h(u) represents the maximum number of nested layers of the sub-assembly with u as the top-level part (i.e., the number of edges from u to its bottom-most basic part).

Your goal is to infer the maximum assembly depth H of the entire complex equipment through interactive process queries and disassembling the component structure.

Your initial position is at the final product (root node).

You can perform the following operations (one operation per turn):

1. **Query subcomponents count**: Returns the number of immediate subordinate subcomponents required to form the current component (non-negative integer).
2. **Query estimated machining time index**: Returns the estimated machining time index of the current component (non-negative integer).
3. **Disassemble into the k-th subcomponent**: If the current component can be further broken down, you can disassemble and view the k-th subcomponent (k starts from 1). If k is out of range, the operation is invalid.
4. **Return to the superior assembly component**: If you are not currently viewing the final product, you can return to its direct superior component. If already at the final product level, the operation is invalid.
5. **Restore to the final product**: Reset the hierarchical view to the final product level (root node).
6. **Declare architecture calculation result**: Submit your inferred maximum assembly depth H.

Each operation must contain only one tag. Use the following XML format:

- Query subcomponents count:
<query_children></query_children>

- Query estimated machining time index:
<query_observation></query_observation>

- Disassemble into the k-th subcomponent (e.g., disassemble the 2nd subcomponent):
<move_down>2</move_down>

- Return to the superior assembly component:
<move_up></move_up>

- Restore to the final product:
<move_root></move_root>

- Declare architecture calculation result (e.g., declare depth as 5):
<answer>5</answer>

- The BOM structure, process parameters a and c remain constant throughout the calculation.
- You need to infer the maximum assembly depth H with as few operations as possible.
- If the declared depth calculation result is incorrect, the task fails.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“法典渊源与细则嵌套深度审查”系统。

本系统引入了一部未知的庞大法典嵌套结构树 T。法典的最大嵌套层级 H 定义为从法典总则（根节点）到任一最底层实施细则（叶子节点）的最长嵌套边数。

存在两个未知的审查参数 a（大于等于1）和 c（大于等于0）。对于法典中的任一条款 u，审查引擎会计算出一个合规审查复杂度得分 P(u)，该得分由公式 P(u) = a × h(u) + c 计算得出，其中 h(u) 表示以条款 u 为上位法的子条款结构的最大嵌套层级（即从 u 到其最底端实施细则的边数）。

你的目标是通过交互式查阅下级细则和层级溯源，推断出整部法典的最大嵌套层级 H。

你的初始查阅位置在法典总则（根节点）。

你可以执行以下操作（每次只能执行一个操作）：

1. **查询下级细则条文数**：返回当前条款直接下属的细则条文数量（非负整数）。
2. **查询合规审查复杂度得分**：返回当前条款的合规审查复杂度得分（非负整数）。
3. **查阅第 k 条下级细则**：如果当前条款有附属细则，你可以向下查阅第 k 条细则（k 从 1 开始计数）。如果 k 超出范围，操作无效。
4. **返回上位法条**：如果当前条款不是法典总则，你可以向上溯源至其直接上位法条。如果已在总则，操作无效。
5. **回到法典总则**：将查阅位置重置为法典总则。
6. **声明审查结论**：提交你推断出的最大嵌套层级 H。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 查询下级细则条文数：
<query_children></query_children>

- 查询合规审查复杂度得分：
<query_observation></query_observation>

- 查阅第 k 条下级细则（例如查阅第 2 条细则）：
<move_down>2</move_down>

- 返回上位法条：
<move_up></move_up>

- 回到法典总则：
<move_root></move_root>

- 声明审查结论（例如声明嵌套层级为 5）：
<answer>5</answer>

- 法典嵌套结构、审查参数 a 和 c 在整个审查过程中保持不变。
- 你需要通过尽可能少的操作来推断出法典的最大嵌套层级 H。
- 如果声明的审查结论错误，系统审查失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Code Source and Subsidiary Rule Nesting Depth Review" system.

This system introduces an unknown massive code nesting structure tree T. The maximum nesting depth H of the code is defined as the maximum number of nesting edges from the general provisions of the code (root node) to any bottom-level implementation rule (leaf node).

There are two unknown review parameters a (greater than or equal to 1) and c (greater than or equal to 0). For any provision u in the code, the review engine calculates a compliance review complexity score P(u), which is derived from the formula P(u) = a × h(u) + c, where h(u) represents the maximum nesting depth of the sub-provision structure with u as the superior law (i.e., the number of edges from u to its bottom-most implementation rule).

Your goal is to infer the maximum nesting depth H of the entire legal code through interactive consultation of subsidiary rules and hierarchical traceability.

Your initial consultation position is at the general provisions of the code (root node).

You can perform the following operations (one operation per turn):

1. **Query subordinate rules count**: Returns the number of implementation rules directly subordinate to the current provision (non-negative integer).
2. **Query compliance review complexity score**: Returns the compliance review complexity score of the current provision (non-negative integer).
3. **Consult the k-th subordinate rule**: If the current provision has subsidiary rules, you can move down to consult the k-th rule (k starts from 1). If k is out of range, the operation is invalid.
4. **Return to the superior provision**: If the current provision is not the general provisions, you can trace back up to its direct superior provision. If already at the general provisions, the operation is invalid.
5. **Return to the general provisions**: Reset the consultation position to the general provisions of the code.
6. **Declare review conclusion**: Submit your inferred maximum nesting depth H.

Each operation must contain only one tag. Use the following XML format:

- Query subordinate rules count:
<query_children></query_children>

- Query compliance review complexity score:
<query_observation></query_observation>

- Consult the k-th subordinate rule (e.g., consult the 2nd rule):
<move_down>2</move_down>

- Return to the superior provision:
<move_up></move_up>

- Return to the general provisions:
<move_root></move_root>

- Declare review conclusion (e.g., declare nesting depth as 5):
<answer>5</answer>

- The code nesting structure, review parameters a and c remain constant throughout the review process.
- You need to infer the maximum nesting depth H with as few operations as possible.
- If the declared review conclusion is incorrect, the system review fails.
"""

    tags = ["answer", "query_children", "query_observation", "move_down", "move_up", "move_root"]

    DIFFICULTY_CONFIG = {
        1: {
            "a": 1,
            "c": 0,
            "tree": {
                "root": {
                    "children": [
                        {"children": [{"children": []}]},
                        {"children": []}
                    ]
                }
            }
        },
        2: {
            "a": 2,
            "c": 1,
            "tree": {
                "root": {
                    "children": [
                        {"children": [
                            {"children": [{"children": []}]},
                            {"children": []}
                        ]},
                        {"children": []},
                        {"children": []}
                    ]
                }
            }
        },
        3: {
            "a": 3,
            "c": 5,
            "tree": {
                "root": {
                    "children": [
                        {"children": [
                            {"children": [
                                {"children": [{"children": []}]}
                            ]},
                            {"children": []}
                        ]},
                        {"children": [{"children": []}]}
                    ]
                }
            }
        },
        4: {
            "a": 2,
            "c": 10,
            "tree": {
                "root": {
                    "children": [
                        {"children": [
                            {"children": [
                                {"children": [
                                    {"children": [{"children": []}]}
                                ]}
                            ]}
                        ]},
                        {"children": [{"children": []}]},
                        {"children": []},
                        {"children": [{"children": [{"children": []}]}]}
                    ]
                }
            }
        },
        5: {
            "a": 4,
            "c": 7,
            "tree": {
                "root": {
                    "children": [
                        {"children": [
                            {"children": [
                                {"children": [
                                    {"children": [
                                        {"children": [{"children": []}]}
                                    ]},
                                    {"children": []}
                                ]}
                            ]},
                            {"children": [{"children": []}]}
                        ]},
                        {"children": [
                            {"children": [{"children": []}]}
                        ]},
                        {"children": []}
                    ]
                }
            }
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[diff]
        self.a = cfg["a"]
        self.c = cfg["c"]
        
        self.tree_root = self._build_tree_node(cfg["tree"]["root"])
        
        self._compute_heights(self.tree_root)
        
        self.tree_height = self._compute_tree_height(self.tree_root, 0)
        
        self.current_node = self.tree_root
        
        self.path_stack = []
        
        self._game_info["tree_height"] = self.tree_height

    def _build_tree_node(self, tree_dict):
        node = {
            "children": [],
            "subtree_height": 0,
            "observation": 0,
            "parent": None
        }
        
        for child_dict in tree_dict.get("children", []):
            child_node = self._build_tree_node(child_dict)
            child_node["parent"] = node
            node["children"].append(child_node)
        
        return node

    def _compute_heights(self, node):
        if not node["children"]:
            node["subtree_height"] = 0
        else:
            node["subtree_height"] = 1 + max(self._compute_heights(child) for child in node["children"])
        
        node["observation"] = self.a * node["subtree_height"] + self.c
        
        return node["subtree_height"]

    def _compute_tree_height(self, node, depth):
        if not node["children"]:
            return depth
        return max(self._compute_tree_height(child, depth + 1) for child in node["children"])

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.tree_height
        except:
            return False

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        is_en = self.config.language != "zh"
        
        def _describe_path(path):
            if not path:
                return "root" if is_en else "根节点"
            steps = []
            for idx in path:
                steps.append(f"child {idx}" if is_en else f"第{idx}个子节点")
            return " -> ".join(["root" if is_en else "根节点"] + steps)
        
        def _traverse(node, path):
            node_desc = _describe_path(path)
            
            q_children = f"Location: {node_desc}\n<query_children></query_children>" if is_en else f"当前位置：{node_desc}\n<query_children></query_children>"
            ans_children = str(len(node["children"]))
            if is_en:
                answer_text = f"Node at [{node_desc}] has {ans_children} children."
            else:
                answer_text = f"节点[{node_desc}]有{ans_children}个子节点。"
            queries.append({"query": q_children, "answer": answer_text})
            
            q_obs = f"Location: {node_desc}\n<query_observation></query_observation>" if is_en else f"当前位置：{node_desc}\n<query_observation></query_observation>"
            ans_obs = str(node["observation"])
            if is_en:
                answer_text = f"Node at [{node_desc}] has observation value {ans_obs}."
            else:
                answer_text = f"节点[{node_desc}]的观察值为{ans_obs}。"
            queries.append({"query": q_obs, "answer": answer_text})
            
            for i, child in enumerate(node["children"]):
                _traverse(child, path + [i + 1])
        
        _traverse(self.tree_root, [])
        return queries

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            invalid_op = "操作无效。"
            out_of_range = "子节点编号超出范围。"
            already_root = "已在根节点。"
        else:
            invalid_op = "Invalid operation."
            out_of_range = "Child index out of range."
            already_root = "Already at root."
        
        if "query_children" in parsed_info:
            return str(len(self.current_node["children"]))
        
        elif "query_observation" in parsed_info:
            return str(self.current_node["observation"])
        
        elif "move_down" in parsed_info:
            try:
                k = int(parsed_info["move_down"].strip())
                if 1 <= k <= len(self.current_node["children"]):
                    self.path_stack.append(self.current_node)
                    self.current_node = self.current_node["children"][k - 1]
                    return "OK" if self.config.language == "en" else "移动成功"
                else:
                    return out_of_range
            except:
                return invalid_op
        
        elif "move_up" in parsed_info:
            if self.current_node["parent"] is not None:
                self.current_node = self.current_node["parent"]
                if self.path_stack:
                    self.path_stack.pop()
                return "OK" if self.config.language == "en" else "移动成功"
            else:
                return already_root
        
        elif "move_root" in parsed_info:
            self.current_node = self.tree_root
            self.path_stack = []
            return "OK" if self.config.language == "en" else "已回到根节点"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if "OK" in correct or "成功" in correct or "已回到" in correct:
            return "Failed" if self.config.language == "en" else "操作失败"

        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            if "yes" in correct:
                return correct.replace("yes", "no")
            if "YES" in correct:
                return correct.replace("YES", "NO")
            if "No" in correct:
                return correct.replace("No", "Yes")
            if "no" in correct:
                return correct.replace("no", "yes")
            if "NO" in correct:
                return correct.replace("NO", "YES")
        
        return correct + "_WRONG"