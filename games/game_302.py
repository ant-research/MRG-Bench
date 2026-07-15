from .base import Game
import random

class TreeAnnotationGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树标注规则推理"游戏，规则如下：

游戏设定了一棵未知的有限有根树 T，节点编号为 1 到 N（N 大于等于 5，但具体值未知）。节点 1 是根节点。

**定义：**
- 叶节点：没有子节点的节点。如果根节点有子节点，则根不是叶节点。
- 存在一个全局统一的节点标注函数 f，它将每个节点映射到一个非负整数。

**标注函数候选：**
函数 f 从以下四个候选之一中选取（具体是哪一个未知）：
- α：f(i) = 节点 i 的子节点数量
- β：f(i) = 节点 i 的无向度数（父节点数加子节点数；根的度数等于其子节点数）
- γ：f(i) = 叶指示（若 i 为叶则为 1，否则为 0）
- δ：f(i) = 以 i 为根的子树大小（包含 i 自身的节点总数）

**可用查询：**
你可以反复向我提出以下查询（每次仅限一个查询）：

1. **标注查询**：询问节点 i 的标注值是多少。回答一个非负整数。
2. **父查询**：询问节点 i 的父节点是谁。回答父节点编号或"无"（若 i 为根）。
3. **子查询**：询问节点 i 的子节点有哪些。回答按升序排列的子节点编号列表（可为空）。
4. **邻接判定**：询问节点 i 与节点 j 是否直接相连。回答"是"或"否"。
5. **祖先判定**：询问节点 i 是否是节点 j 的祖先。回答"是"或"否"。

**约束：**
- 每次查询必须指定具体节点编号 i 或 (i, j)。
- 不允许直接请求整棵树的全局性质。

**目标：**
通过尽可能少的查询次数，确定：
1. 标注函数 f 属于 {{α, β, γ, δ}} 中的哪一个
2. 该树的叶节点总数

若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 标注查询（例如查询节点 5）：
<query_annotation>5</query_annotation>

- 父查询（例如查询节点 3 的父节点）：
<query_parent>3</query_parent>

- 子查询（例如查询节点 2 的子节点）：
<query_children>2</query_children>

- 邻接判定（例如查询节点 1 和节点 3 是否相连）：
<query_adjacent>1,3</query_adjacent>

- 祖先判定（例如查询节点 1 是否是节点 5 的祖先）：
<query_ancestor>1,5</query_ancestor>

提交最终答案时，必须说明标注函数类型（α、β、γ 或 δ）并给出叶节点总数，格式如下：

<answer>function=α, leaves=3</answer>
"""

    game_rule_en = """\
Let's play a "Tree Annotation Rule Inference" game. Here are the rules:

There is an unknown finite rooted tree T with nodes numbered from 1 to N (N is greater than or equal to 5, but the exact value is unknown). Node 1 is the root.

**Definitions:**
- Leaf node: A node with no children. If the root has children, then the root is not a leaf.
- There exists a global unified node annotation function f that maps each node to a non-negative integer.

**Annotation Function Candidates:**
Function f is selected from one of the following four candidates (which one is unknown):
- α: f(i) = number of children of node i
- β: f(i) = undirected degree of node i (number of parent plus number of children; root's degree equals its number of children)
- γ: f(i) = leaf indicator (1 if i is a leaf, 0 otherwise)
- δ: f(i) = size of subtree rooted at i (total number of nodes including i itself)

**Available Queries:**
You can repeatedly ask me the following queries (one query per turn):

1. **Annotation Query**: Ask for the annotation value of node i. Answer is a non-negative integer.
2. **Parent Query**: Ask for the parent of node i. Answer is the parent node number or "None" (if i is root).
3. **Children Query**: Ask for the children of node i. Answer is a list of child node numbers in ascending order (may be empty).
4. **Adjacent Query**: Ask if node i and node j are directly connected. Answer "Yes" or "No".
5. **Ancestor Query**: Ask if node i is an ancestor of node j. Answer "Yes" or "No".

**Constraints:**
- Each query must specify concrete node number(s) i or (i, j).
- You cannot directly request global properties of the entire tree.

**Goal:**
Through as few queries as possible, determine:
1. Which annotation function f belongs to {{α, β, γ, δ}}
2. The total number of leaf nodes in the tree

If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Annotation Query (e.g., querying node 5):
<query_annotation>5</query_annotation>

- Parent Query (e.g., querying parent of node 3):
<query_parent>3</query_parent>

- Children Query (e.g., querying children of node 2):
<query_children>2</query_children>

- Adjacent Query (e.g., querying if node 1 and node 3 are connected):
<query_adjacent>1,3</query_adjacent>

- Ancestor Query (e.g., querying if node 1 is ancestor of node 5):
<query_ancestor>1,5</query_ancestor>

When submitting the final answer, specify the annotation function type (α, β, γ, or δ) and the total number of leaves, using this format:

<answer>function=α, leaves=3</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通规划调度系统。由于突发的数据丢失，我们需要重新摸排道路交通网络分发树的层级结构。
我们来玩一个"树标注规则推理"游戏，规则如下：

游戏设定了一棵未知的有限有根交通分发树 T，站点编号为 1 到 N（N 大于等于 5，但具体值未知）。站点 1 是总枢纽（根节点）。

**定义：**
- 末端站点（叶节点）：没有直属下游站点的站点。如果总枢纽有下游站点，则它不是末端站点。
- 存在一个全局统一的站点标注函数 f，它将每个站点映射到一个非负整数。

**标注函数候选：**
函数 f 从以下四个候选之一中选取（具体是哪一个未知）：
- α：f(i) = 站点 i 的直属下游站点数量
- β：f(i) = 站点 i 的相连站点总数（上游加上直属下游站点数；总枢纽的该值等于其直属下游站点数）
- γ：f(i) = 末端站点指示（若 i 为末端站点则为 1，否则为 0）
- δ：f(i) = 以 i 为起始的所有下游站点总数（包含 i 自身）

**可用查询：**
你可以反复向我提出以下查询（每次仅限一个查询）：

1. **标注查询**：询问站点 i 的标注值是多少。回答一个非负整数。
2. **父查询**：询问站点 i 的上游站点是谁。回答上游站点编号或"无"（若 i 为总枢纽）。
3. **子查询**：询问站点 i 的直属下游站点有哪些。回答按升序排列的站点编号列表（可为空）。
4. **邻接判定**：询问站点 i 与站点 j 是否直接相连。回答"是"或"否"。
5. **祖先判定**：询问站点 i 是否是站点 j 的上游直接或间接来源。回答"是"或"否"。

**约束：**
- 每次查询必须指定具体站点编号 i 或 (i, j)。
- 不允许直接请求整个交通网络的全局性质。

**目标：**
通过尽可能少的查询次数，确定：
1. 标注函数 f 属于 {{α, β, γ, δ}} 中的哪一个
2. 该交通网络的末端站点（叶节点）总数

若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 标注查询（例如查询站点 5）：
<query_annotation>5</query_annotation>

- 父查询（例如查询站点 3 的上游站点）：
<query_parent>3</query_parent>

- 子查询（例如查询站点 2 的直属下游站点）：
<query_children>2</query_children>

- 邻接判定（例如查询站点 1 和站点 3 是否相连）：
<query_adjacent>1,3</query_adjacent>

- 祖先判定（例如查询站点 1 是否是站点 5 的祖先/来源）：
<query_ancestor>1,5</query_ancestor>

提交最终答案时，必须说明标注函数类型（α、β、γ 或 δ）并给出末端站点（叶节点）总数，格式如下：

<answer>function=α, leaves=3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the intelligent traffic planning and scheduling system. Due to a sudden data loss, we need to re-examine the hierarchical structure of the road traffic network distribution tree.
Let's play a "Tree Annotation Rule Inference" game. Here are the rules:

There is an unknown finite rooted traffic distribution tree T with station numbers from 1 to N (N is greater than or equal to 5, but the exact value is unknown). Station 1 is the main hub (root).

**Definitions:**
- Terminal station (Leaf node): A station with no direct downstream stations. If the main hub has downstream stations, it is not a terminal station.
- There exists a global unified station annotation function f that maps each station to a non-negative integer.

**Annotation Function Candidates:**
Function f is selected from one of the following four candidates (which one is unknown):
- α: f(i) = number of direct downstream stations of station i
- β: f(i) = undirected degree of station i (number of upstream plus direct downstream stations; main hub's degree equals its number of downstream stations)
- γ: f(i) = terminal station indicator (1 if i is a terminal station, 0 otherwise)
- δ: f(i) = size of the sub-network starting from i (total number of stations including i itself)

**Available Queries:**
You can repeatedly ask me the following queries (one query per turn):

1. **Annotation Query**: Ask for the annotation value of station i. Answer is a non-negative integer.
2. **Parent Query**: Ask for the upstream station of station i. Answer is the station number or "None" (if i is the main hub).
3. **Children Query**: Ask for the direct downstream stations of station i. Answer is a list of station numbers in ascending order (may be empty).
4. **Adjacent Query**: Ask if station i and station j are directly connected. Answer "Yes" or "No".
5. **Ancestor Query**: Ask if station i is an upstream source (ancestor) of station j. Answer "Yes" or "No".

**Constraints:**
- Each query must specify concrete station number(s) i or (i, j).
- You cannot directly request global properties of the entire traffic network.

**Goal:**
Through as few queries as possible, determine:
1. Which annotation function f belongs to {{α, β, γ, δ}}
2. The total number of terminal stations (leaf nodes) in the network

If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Annotation Query (e.g., querying station 5):
<query_annotation>5</query_annotation>

- Parent Query (e.g., querying upstream station of station 3):
<query_parent>3</query_parent>

- Children Query (e.g., querying downstream stations of station 2):
<query_children>2</query_children>

- Adjacent Query (e.g., querying if station 1 and station 3 are connected):
<query_adjacent>1,3</query_adjacent>

- Ancestor Query (e.g., querying if station 1 is an ancestor of station 5):
<query_ancestor>1,5</query_ancestor>

When submitting the final answer, specify the annotation function type (α, β, γ, or δ) and the total number of terminal stations (leaves), using this format:

<answer>function=α, leaves=3</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用流行病学调查与溯源分析系统。我们需要通过追踪传染病传播链来控制疫情蔓延。
我们来玩一个"传播链标注规则推理"游戏，规则如下：

游戏设定了一棵未知的有限有根传播链树 T，病例编号为 1 到 N（N 大于等于 5，但具体值未知）。病例 1 是零号病人（根节点）。

**定义：**
- 终端病例（叶节点）：没有再传染给其他人的病例。如果零号病人有传染下家，则其不是终端病例。
- 存在一个全局统一的病例标注函数 f，它将每个病例映射到一个非负整数。

**标注函数候选：**
函数 f 从以下四个候选之一中选取（具体是哪一个未知）：
- α：f(i) = 病例 i 直接传染的下家病例数量
- β：f(i) = 病例 i 的密接病例数（传染来源数加直接传染下家数；零号病人的密接数等于其直接传染下家数）
- γ：f(i) = 终端病例指示（若 i 为终端病例则为 1，否则为 0）
- δ：f(i) = 由病例 i 引发的后续传播总规模（包含 i 自身的所有病例总数）

**可用查询：**
你可以反复向我提出以下查询（每次仅限一个查询）：

1. **标注查询**：询问病例 i 的标注值是多少。回答一个非负整数。
2. **父查询**：询问病例 i 的直接传染来源是谁。回答来源病例编号或"无"（若 i 为零号病人）。
3. **子查询**：询问病例 i 直接传染的下家有哪些。回答按升序排列的病例编号列表（可为空）。
4. **邻接判定**：询问病例 i 与病例 j 是否有直接的传染与被传染关系。回答"是"或"否"。
5. **祖先判定**：询问病例 i 是否是引发病例 j 感染的源头（直接或间接）。回答"是"或"否"。

**约束：**
- 每次查询必须指定具体病例编号 i 或 (i, j)。
- 不允许直接请求整条传播链的全局性质。

**目标：**
通过尽可能少的查询次数，确定：
1. 标注函数 f 属于 {{α, β, γ, δ}} 中的哪一个
2. 该传播链中的终端病例（叶节点）总数

若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 标注查询（例如查询病例 5）：
<query_annotation>5</query_annotation>

- 父查询（例如查询病例 3 的传染来源）：
<query_parent>3</query_parent>

- 子查询（例如查询病例 2 直接传染的下家）：
<query_children>2</query_children>

- 邻接判定（例如查询病例 1 和病例 3 是否有直接传染关系）：
<query_adjacent>1,3</query_adjacent>

- 祖先判定（例如查询病例 1 是否是病例 5 的源头）：
<query_ancestor>1,5</query_ancestor>

提交最终答案时，必须说明标注函数类型（α、β、γ 或 δ）并给出终端病例（叶节点）总数，格式如下：

<answer>function=α, leaves=3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the epidemiological investigation and tracing analysis system. We need to control the spread of the epidemic by tracking the transmission chain tree.
Let's play a "Transmission Chain Annotation Rule Inference" game. Here are the rules:

There is an unknown finite rooted transmission chain tree T with case numbers from 1 to N (N is greater than or equal to 5, but the exact value is unknown). Case 1 is patient zero (root).

**Definitions:**
- Terminal case (Leaf node): A case that did not infect anyone else. If patient zero infected others, they are not a terminal case.
- There exists a global unified case annotation function f that maps each case to a non-negative integer.

**Annotation Function Candidates:**
Function f is selected from one of the following four candidates (which one is unknown):
- α: f(i) = number of cases directly infected by case i
- β: f(i) = number of close contact cases for case i (infector plus directly infected cases; patient zero's contacts equal directly infected cases)
- γ: f(i) = terminal case indicator (1 if i is a terminal case, 0 otherwise)
- δ: f(i) = total transmission scale triggered by case i (total number of cases including i itself)

**Available Queries:**
You can repeatedly ask me the following queries (one query per turn):

1. **Annotation Query**: Ask for the annotation value of case i. Answer is a non-negative integer.
2. **Parent Query**: Ask for the direct infector of case i. Answer is the case number or "None" (if i is patient zero).
3. **Children Query**: Ask for the cases directly infected by case i. Answer is a list of case numbers in ascending order (may be empty).
4. **Adjacent Query**: Ask if case i and case j have a direct transmission relationship. Answer "Yes" or "No".
5. **Ancestor Query**: Ask if case i is the origin (ancestor) of case j's infection. Answer "Yes" or "No".

**Constraints:**
- Each query must specify concrete case number(s) i or (i, j).
- You cannot directly request global properties of the entire transmission chain.

**Goal:**
Through as few queries as possible, determine:
1. Which annotation function f belongs to {{α, β, γ, δ}}
2. The total number of terminal cases (leaf nodes) in the chain

If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Annotation Query (e.g., querying case 5):
<query_annotation>5</query_annotation>

- Parent Query (e.g., querying the infector of case 3):
<query_parent>3</query_parent>

- Children Query (e.g., querying cases directly infected by case 2):
<query_children>2</query_children>

- Adjacent Query (e.g., querying if case 1 and case 3 have a direct transmission relationship):
<query_adjacent>1,3</query_adjacent>

- Ancestor Query (e.g., querying if case 1 is the source for case 5):
<query_ancestor>1,5</query_ancestor>

When submitting the final answer, specify the annotation function type (α, β, γ, or δ) and the total number of terminal cases (leaves), using this format:

<answer>function=α, leaves=3</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用智能自适应学习图谱分析引擎。为规划最佳学习路径，我们要解析学科的知识点依赖层级树。
我们来玩一个"知识图谱标注规则推理"游戏，规则如下：

游戏设定了一棵未知的有限有根知识依赖树 T，知识点编号为 1 到 N（N 大于等于 5，但具体值未知）。知识点 1 是学科核心概念（根节点）。

**定义：**
- 基础知识点（叶节点）：没有进一步衍生子知识点的底层概念。如果核心概念有衍生，则它不是基础知识点。
- 存在一个全局统一的知识点特征评估函数 f，它将每个知识点映射到一个非负整数。

**标注函数候选：**
函数 f 从以下四个候选之一中选取（具体是哪一个未知）：
- α：f(i) = 知识点 i 直接衍生的子知识点数量
- β：f(i) = 知识点 i 的直接关联总数（前置知识点加上直接衍生子知识点数；核心概念的该值等于其衍生数）
- γ：f(i) = 基础知识点指示（若 i 为基础知识点则为 1，否则为 0）
- δ：f(i) = 包含知识点 i 及其所有衍生子概念在内的子图谱总大小

**可用查询：**
你可以反复向我提出以下查询（每次仅限一个查询）：

1. **标注查询**：询问知识点 i 的评估特征值是多少。回答一个非负整数。
2. **父查询**：询问知识点 i 的直接前置知识点是谁。回答知识点编号或"无"（若 i 为核心概念）。
3. **子查询**：询问知识点 i 直接衍生的子知识点有哪些。回答按升序排列的知识点编号列表（可为空）。
4. **邻接判定**：询问知识点 i 与知识点 j 是否有直接的前置或衍生关系。回答"是"或"否"。
5. **祖先判定**：询问知识点 i 是否是知识点 j 的宏观前置概念（祖先）。回答"是"或"否"。

**约束：**
- 每次查询必须指定具体知识点编号 i 或 (i, j)。
- 不允许直接请求整个学科知识图谱的全局性质。

**目标：**
通过尽可能少的查询次数，确定：
1. 标注函数 f 属于 {{α, β, γ, δ}} 中的哪一个
2. 该图谱中的底层基础知识点（叶节点）总数

若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 标注查询（例如查询知识点 5）：
<query_annotation>5</query_annotation>

- 父查询（例如查询知识点 3 的前置知识点）：
<query_parent>3</query_parent>

- 子查询（例如查询知识点 2 的衍生子知识点）：
<query_children>2</query_children>

- 邻接判定（例如查询知识点 1 和知识点 3 是否直接关联）：
<query_adjacent>1,3</query_adjacent>

- 祖先判定（例如查询知识点 1 是否是知识点 5 的宏观前置概念）：
<query_ancestor>1,5</query_ancestor>

提交最终答案时，必须说明标注函数类型（α、β、γ 或 δ）并给出基础知识点（叶节点）总数，格式如下：

<answer>function=α, leaves=3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the intelligent adaptive learning graph analysis engine. To plan the optimal learning path, we need to parse the knowledge point dependency tree of the subject.
Let's play a "Knowledge Graph Annotation Rule Inference" game. Here are the rules:

There is an unknown finite rooted knowledge dependency tree T with knowledge points numbered from 1 to N (N is greater than or equal to 5, but the exact value is unknown). Point 1 is the core concept (root).

**Definitions:**
- Foundational knowledge point (Leaf node): A bottom-level concept with no further derived sub-points. If the core concept has derivatives, it is not a foundational point.
- There exists a global unified knowledge point evaluation function f that maps each point to a non-negative integer.

**Annotation Function Candidates:**
Function f is selected from one of the following four candidates (which one is unknown):
- α: f(i) = number of sub-points directly derived from point i
- β: f(i) = total number of direct connections of point i (prerequisite point plus directly derived sub-points; the core concept's value equals its number of derivatives)
- γ: f(i) = foundational point indicator (1 if i is a foundational point, 0 otherwise)
- δ: f(i) = total size of the sub-graph including point i and all its derived concepts

**Available Queries:**
You can repeatedly ask me the following queries (one query per turn):

1. **Annotation Query**: Ask for the evaluation feature value of point i. Answer is a non-negative integer.
2. **Parent Query**: Ask for the direct prerequisite of point i. Answer is the point number or "None" (if i is the core concept).
3. **Children Query**: Ask for the sub-points directly derived from point i. Answer is a list of point numbers in ascending order (may be empty).
4. **Adjacent Query**: Ask if point i and point j have a direct prerequisite or derivative relationship. Answer "Yes" or "No".
5. **Ancestor Query**: Ask if point i is a macro-prerequisite (ancestor) of point j. Answer "Yes" or "No".

**Constraints:**
- Each query must specify concrete point number(s) i or (i, j).
- You cannot directly request global properties of the entire subject knowledge graph.

**Goal:**
Through as few queries as possible, determine:
1. Which annotation function f belongs to {{α, β, γ, δ}}
2. The total number of foundational knowledge points (leaf nodes) in the graph

If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Annotation Query (e.g., querying point 5):
<query_annotation>5</query_annotation>

- Parent Query (e.g., querying the prerequisite of point 3):
<query_parent>3</query_parent>

- Children Query (e.g., querying derived sub-points of point 2):
<query_children>2</query_children>

- Adjacent Query (e.g., querying if point 1 and point 3 are directly related):
<query_adjacent>1,3</query_adjacent>

- Ancestor Query (e.g., querying if point 1 is a macro-prerequisite for point 5):
<query_ancestor>1,5</query_ancestor>

When submitting the final answer, specify the annotation function type (α, β, γ, or δ) and the total number of foundational points (leaves), using this format:

<answer>function=α, leaves=3</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入智能制造ERP系统。在投入生产前，系统需要校验产品BOM（物料清单）的层级装配树结构。
我们来玩一个"BOM组件标注规则推理"游戏，规则如下：

游戏设定了一棵未知的有限有根产品装配树 T，组件编号为 1 到 N（N 大于等于 5，但具体值未知）。组件 1 是最终成品（根节点）。

**定义：**
- 基础零件（叶节点）：无需再拆分的底层采购零件。如果最终成品是由其他组件拼装的，则它不是基础零件。
- 存在一个全局统一的组件评估参数函数 f，它将每个组件映射到一个非负整数。

**标注函数候选：**
函数 f 从以下四个候选之一中选取（具体是哪一个未知）：
- α：f(i) = 组件 i 直接包含的子组件数量
- β：f(i) = 组件 i 的直接组装关联数（所属父组件加上直接包含的子组件数；成品的该值等于其子组件数）
- γ：f(i) = 基础零件指示（若 i 为基础零件则为 1，否则为 0）
- δ：f(i) = 组件 i 完整展开后的所有零部件总数量（包含 i 自身）

**可用查询：**
你可以反复向我提出以下查询（每次仅限一个查询）：

1. **标注查询**：询问组件 i 的评估参数值是多少。回答一个非负整数。
2. **父查询**：询问组件 i 所属的直接父组件是谁。回答组件编号或"无"（若 i 为最终成品）。
3. **子查询**：询问组件 i 直接包含哪些子组件。回答按升序排列的组件编号列表（可为空）。
4. **邻接判定**：询问组件 i 与组件 j 是否有直接的装配包含关系。回答"是"或"否"。
5. **祖先判定**：询问组件 i 是否在层级上完全包含组件 j（祖先）。回答"是"或"否"。

**约束：**
- 每次查询必须指定具体组件编号 i 或 (i, j)。
- 不允许直接请求整个产品BOM的全局性质。

**目标：**
通过尽可能少的查询次数，确定：
1. 标注函数 f 属于 {{α, β, γ, δ}} 中的哪一个
2. 该BOM架构中的底层基础零件（叶节点）总数

若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 标注查询（例如查询组件 5）：
<query_annotation>5</query_annotation>

- 父查询（例如查询组件 3 的父组件）：
<query_parent>3</query_parent>

- 子查询（例如查询组件 2 的子组件）：
<query_children>2</query_children>

- 邻接判定（例如查询组件 1 和组件 3 是否直接装配）：
<query_adjacent>1,3</query_adjacent>

- 祖先判定（例如查询组件 1 是否包含组件 5）：
<query_ancestor>1,5</query_ancestor>

提交最终答案时，必须说明标注函数类型（α、β、γ 或 δ）并给出基础零件（叶节点）总数，格式如下：

<answer>function=α, leaves=3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the intelligent manufacturing ERP system. Before production starts, the system needs to verify the hierarchical assembly tree structure of the product BOM (Bill of Materials).
Let's play a "BOM Component Annotation Rule Inference" game. Here are the rules:

There is an unknown finite rooted product assembly tree T with component numbers from 1 to N (N is greater than or equal to 5, but the exact value is unknown). Component 1 is the final product (root).

**Definitions:**
- Base part (Leaf node): A bottom-level procured part that cannot be disassembled further. If the final product consists of other components, it is not a base part.
- There exists a global unified component evaluation parameter function f that maps each component to a non-negative integer.

**Annotation Function Candidates:**
Function f is selected from one of the following four candidates (which one is unknown):
- α: f(i) = number of sub-components directly contained in component i
- β: f(i) = number of direct assembly associations for component i (parent component plus directly contained sub-components; the final product's value equals its sub-components)
- γ: f(i) = base part indicator (1 if i is a base part, 0 otherwise)
- δ: f(i) = total number of parts and components of component i when fully expanded (including i itself)

**Available Queries:**
You can repeatedly ask me the following queries (one query per turn):

1. **Annotation Query**: Ask for the evaluation parameter value of component i. Answer is a non-negative integer.
2. **Parent Query**: Ask for the direct parent component of component i. Answer is the component number or "None" (if i is the final product).
3. **Children Query**: Ask for the sub-components directly contained by component i. Answer is a list of component numbers in ascending order (may be empty).
4. **Adjacent Query**: Ask if component i and component j have a direct assembly relationship. Answer "Yes" or "No".
5. **Ancestor Query**: Ask if component i hierarchically contains component j (ancestor). Answer "Yes" or "No".

**Constraints:**
- Each query must specify concrete component number(s) i or (i, j).
- You cannot directly request global properties of the entire product BOM.

**Goal:**
Through as few queries as possible, determine:
1. Which annotation function f belongs to {{α, β, γ, δ}}
2. The total number of base parts (leaf nodes) in the BOM structure

If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Annotation Query (e.g., querying component 5):
<query_annotation>5</query_annotation>

- Parent Query (e.g., querying the parent of component 3):
<query_parent>3</query_parent>

- Children Query (e.g., querying sub-components of component 2):
<query_children>2</query_children>

- Adjacent Query (e.g., querying if component 1 and component 3 are directly assembled):
<query_adjacent>1,3</query_adjacent>

- Ancestor Query (e.g., querying if component 1 contains component 5):
<query_ancestor>1,5</query_ancestor>

When submitting the final answer, specify the annotation function type (α, β, γ, or δ) and the total number of base parts (leaves), using this format:

<answer>function=α, leaves=3</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用法律文书及条款结构审查系统。在进行法理分析时，必须理清法条与细则之间的法律条款解释引申树。
我们来玩一个"法理层级标注规则推理"游戏，规则如下：

游戏设定了一棵未知的有限有根法规引申树 T，条款编号为 1 到 N（N 大于等于 5，但具体值未知）。条款 1 是基本法典（根节点）。

**定义：**
- 终端细则（叶节点）：没有下位解释或衍生条款的最终具体判例或规定。如果基本法典存在下位法，则它不是终端细则。
- 存在一个全局统一的法规衍生指标函数 f，它将每个条款映射到一个非负整数。

**标注函数候选：**
函数 f 从以下四个候选之一中选取（具体是哪一个未知）：
- α：f(i) = 条款 i 直接派生的下位条款数量
- β：f(i) = 条款 i 的直接法律关联数（上位法加上直接下位条款数；基本法典的该值等于其下位条款数）
- γ：f(i) = 终端细则指示（若 i 为终端细则则为 1，否则为 0）
- δ：f(i) = 包含条款 i 及其所有衍生下位条款在内的总数量

**可用查询：**
你可以反复向我提出以下查询（每次仅限一个查询）：

1. **标注查询**：询问条款 i 的衍生指标值是多少。回答一个非负整数。
2. **父查询**：询问条款 i 的直接上位条款是谁。回答条款编号或"无"（若 i 为基本法典）。
3. **子查询**：询问条款 i 直接派生的下位条款有哪些。回答按升序排列的条款编号列表（可为空）。
4. **邻接判定**：询问条款 i 与条款 j 是否存在直接的上下位解释关系。回答"是"或"否"。
5. **祖先判定**：询问条款 i 是否是条款 j 的溯源上位法（祖先）。回答"是"或"否"。

**约束：**
- 每次查询必须指定具体条款编号 i 或 (i, j)。
- 不允许直接请求整套法规体系的全局性质。

**目标：**
通过尽可能少的查询次数，确定：
1. 标注函数 f 属于 {{α, β, γ, δ}} 中的哪一个
2. 该法规树中的终端细则（叶节点）总数

若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 标注查询（例如查询条款 5）：
<query_annotation>5</query_annotation>

- 父查询（例如查询条款 3 的上位条款）：
<query_parent>3</query_parent>

- 子查询（例如查询条款 2 的下位条款）：
<query_children>2</query_children>

- 邻接判定（例如查询条款 1 和条款 3 是否有直接关联）：
<query_adjacent>1,3</query_adjacent>

- 祖先判定（例如查询条款 1 是否是条款 5 的溯源上位法）：
<query_ancestor>1,5</query_ancestor>

提交最终答案时，必须说明标注函数类型（α、β、γ 或 δ）并给出终端细则（叶节点）总数，格式如下：

<answer>function=α, leaves=3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the legal document and clause structure review system. For jurisprudential analysis, it is essential to clarify the hierarchical tree of legal clauses and interpretations.
Let's play a "Jurisprudence Hierarchy Annotation Rule Inference" game. Here are the rules:

There is an unknown finite rooted regulation extension tree T with clause numbers from 1 to N (N is greater than or equal to 5, but the exact value is unknown). Clause 1 is the basic code (root).

**Definitions:**
- Terminal provision (Leaf node): A final specific ruling or regulation with no subordinate interpretations. If the basic code has subordinate laws, it is not a terminal provision.
- There exists a global unified regulation derivation index function f that maps each clause to a non-negative integer.

**Annotation Function Candidates:**
Function f is selected from one of the following four candidates (which one is unknown):
- α: f(i) = number of subordinate clauses directly derived from clause i
- β: f(i) = number of direct legal associations for clause i (superior law plus directly subordinate clauses; the basic code's value equals its subordinate clauses)
- γ: f(i) = terminal provision indicator (1 if i is a terminal provision, 0 otherwise)
- δ: f(i) = total number of clauses including clause i and all its derived subordinate clauses

**Available Queries:**
You can repeatedly ask me the following queries (one query per turn):

1. **Annotation Query**: Ask for the derivation index value of clause i. Answer is a non-negative integer.
2. **Parent Query**: Ask for the direct superior clause of clause i. Answer is the clause number or "None" (if i is the basic code).
3. **Children Query**: Ask for the subordinate clauses directly derived from clause i. Answer is a list of clause numbers in ascending order (may be empty).
4. **Adjacent Query**: Ask if clause i and clause j have a direct superior-subordinate interpretation relationship. Answer "Yes" or "No".
5. **Ancestor Query**: Ask if clause i is the tracing superior law (ancestor) of clause j. Answer "Yes" or "No".

**Constraints:**
- Each query must specify concrete clause number(s) i or (i, j).
- You cannot directly request global properties of the entire legal framework.

**Goal:**
Through as few queries as possible, determine:
1. Which annotation function f belongs to {{α, β, γ, δ}}
2. The total number of terminal provisions (leaf nodes) in the regulation tree

If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Annotation Query (e.g., querying clause 5):
<query_annotation>5</query_annotation>

- Parent Query (e.g., querying the superior of clause 3):
<query_parent>3</query_parent>

- Children Query (e.g., querying subordinate clauses of clause 2):
<query_children>2</query_children>

- Adjacent Query (e.g., querying if clause 1 and clause 3 are directly related):
<query_adjacent>1,3</query_adjacent>

- Ancestor Query (e.g., querying if clause 1 is the superior law for clause 5):
<query_ancestor>1,5</query_ancestor>

When submitting the final answer, specify the annotation function type (α, β, γ, or δ) and the total number of terminal provisions (leaves), using this format:

<answer>function=α, leaves=3</answer>
"""

    tags = ["answer", "query_annotation", "query_parent", "query_children", 
            "query_adjacent", "query_ancestor"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "function": "α",
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [2],
                    5: [2],
                },
                "expected_leaves": 3,
            },
            2: {
                "function": "γ",
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [1],
                    5: [2],
                    6: [2],
                    7: [3],
                },
                "expected_leaves": 4,
            },
            3: {
                "function": "β",
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [2],
                    5: [2],
                    6: [2],
                    7: [3],
                    8: [3],
                    9: [5],
                },
                "expected_leaves": 5,
            },
            4: {
                "function": "δ",
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [2],
                    5: [2],
                    6: [3],
                    7: [4],
                    8: [4],
                    9: [5],
                    10: [5],
                },
                "expected_leaves": 5,
            },
            5: {
                "function": "α",
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [1],
                    5: [2],
                    6: [2],
                    7: [2],
                    8: [3],
                    9: [3],
                    10: [4],
                    11: [5],
                    12: [5],
                    13: [8],
                    14: [8],
                    15: [9],
                },
                "expected_leaves": 8,
            },
        },
        "en": {
            1: {
                "function": "α",
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [2],
                    5: [2],
                },
                "expected_leaves": 3,
            },
            2: {
                "function": "γ",
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [1],
                    5: [2],
                    6: [2],
                    7: [3],
                },
                "expected_leaves": 4,
            },
            3: {
                "function": "β",
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [2],
                    5: [2],
                    6: [2],
                    7: [3],
                    8: [3],
                    9: [5],
                },
                "expected_leaves": 5,
            },
            4: {
                "function": "δ",
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [2],
                    5: [2],
                    6: [3],
                    7: [4],
                    8: [4],
                    9: [5],
                    10: [5],
                },
                "expected_leaves": 5,
            },
            5: {
                "function": "α",
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [1],
                    5: [2],
                    6: [2],
                    7: [2],
                    8: [3],
                    9: [3],
                    10: [4],
                    11: [5],
                    12: [5],
                    13: [8],
                    14: [8],
                    15: [9],
                },
                "expected_leaves": 8,
            },
        },
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
        
        parent_map_orig = cfg["tree"]
        self.n = len(parent_map_orig)
        self._game_info["n"] = self.n
        
        nodes = list(range(2, self.n + 1))
        random.shuffle(nodes)
        mapping = {1: 1}
        for orig_n, new_n in zip(range(2, self.n + 1), nodes):
            mapping[orig_n] = new_n
            
        parent_map = {}
        for orig_node, orig_parents in parent_map_orig.items():
            new_node = mapping[orig_node]
            parent_map[new_node] = [mapping[p] for p in orig_parents]
        
        self.parent = {}
        self.children = {i: [] for i in range(1, self.n + 1)}
        
        for node in range(1, self.n + 1):
            if node in parent_map and parent_map[node]:
                parent_node = parent_map[node][0]
                self.parent[node] = parent_node
                self.children[parent_node].append(node)
            else:
                self.parent[node] = None
        
        for node in self.children:
            self.children[node].sort()
        
        self.function_type = random.choice(["α", "β", "γ", "δ"])
        self.expected_leaves = cfg["expected_leaves"]
        
        self._compute_annotations()

    def _compute_annotations(self):
        self.annotation_alpha = {}
        for node in range(1, self.n + 1):
            self.annotation_alpha[node] = len(self.children[node])
        
        self.annotation_beta = {}
        for node in range(1, self.n + 1):
            degree = len(self.children[node])
            if self.parent[node] is not None:
                degree += 1
            self.annotation_beta[node] = degree
        
        self.annotation_gamma = {}
        for node in range(1, self.n + 1):
            self.annotation_gamma[node] = 1 if len(self.children[node]) == 0 else 0
        
        self.annotation_delta = {}
        self._compute_subtree_size(1)
    
    def _compute_subtree_size(self, node):
        size = 1
        for child in self.children[node]:
            size += self._compute_subtree_size(child)
        self.annotation_delta[node] = size
        return size
    
    def _get_annotation(self, node):
        if self.function_type == "α":
            return self.annotation_alpha[node]
        elif self.function_type == "β":
            return self.annotation_beta[node]
        elif self.function_type == "γ":
            return self.annotation_gamma[node]
        elif self.function_type == "δ":
            return self.annotation_delta[node]
        else:
            raise ValueError(f"Unknown function type: {self.function_type}")
    
    def _is_ancestor(self, ancestor, descendant):
        if ancestor == descendant:
            return False
        current = descendant
        while current is not None:
            if current == ancestor:
                return True
            current = self.parent[current]
        return False

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "function" not in ans_dict or "leaves" not in ans_dict:
            return False
        
        if ans_dict["function"] not in ["α", "β", "γ", "δ"]:
            return False
        if ans_dict["function"] != self.function_type:
            return False
        
        try:
            leaves_count = int(ans_dict["leaves"])
        except:
            return False
        
        return leaves_count == self.expected_leaves

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            none_res = "无"
            error_range = "错误：节点编号超出范围。"
            error_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            none_res = "None"
            error_range = "Error: Node ID out of range."
            error_format = "Error: Invalid format."
        
        if "query_annotation" in parsed_info:
            try:
                node = int(parsed_info["query_annotation"].strip())
                if node < 1 or node > self.n:
                    return error_range
                return str(self._get_annotation(node))
            except:
                return error_format
        
        elif "query_parent" in parsed_info:
            try:
                node = int(parsed_info["query_parent"].strip())
                if node < 1 or node > self.n:
                    return error_range
                if self.parent[node] is None:
                    return none_res
                return str(self.parent[node])
            except:
                return error_format
        
        elif "query_children" in parsed_info:
            try:
                node = int(parsed_info["query_children"].strip())
                if node < 1 or node > self.n:
                    return error_range
                children_list = self.children[node]
                if not children_list:
                    return "[]" if self.config.language == "en" else "[]"
                return "[" + ", ".join(map(str, children_list)) + "]"
            except:
                return error_format
        
        elif "query_adjacent" in parsed_info:
            try:
                raw = parsed_info["query_adjacent"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                node1, node2 = int(parts[0]), int(parts[1])
                if node1 < 1 or node1 > self.n or node2 < 1 or node2 > self.n:
                    return error_range
                is_adjacent = (self.parent[node1] == node2 or self.parent[node2] == node1)
                return yes_res if is_adjacent else no_res
            except:
                return error_format
        
        elif "query_ancestor" in parsed_info:
            try:
                raw = parsed_info["query_ancestor"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                node1, node2 = int(parts[0]), int(parts[1])
                if node1 < 1 or node1 > self.n or node2 < 1 or node2 > self.n:
                    return error_range
                is_anc = self._is_ancestor(node1, node2)
                return yes_res if is_anc else no_res
            except:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for node in range(1, self.n + 1):
            parsed_anno = {"query_annotation": str(node)}
            ans_anno = self._cf_core_produce(parsed_anno)
            queries.append({
                "query": f"<query_annotation>{node}</query_annotation>",
                "answer": ans_anno
            })
            
            parsed_parent = {"query_parent": str(node)}
            ans_parent = self._cf_core_produce(parsed_parent)
            queries.append({
                "query": f"<query_parent>{node}</query_parent>",
                "answer": ans_parent
            })
            
            parsed_child = {"query_children": str(node)}
            ans_child = self._cf_core_produce(parsed_child)
            queries.append({
                "query": f"<query_children>{node}</query_children>",
                "answer": ans_child
            })

        for n1 in range(1, self.n + 1):
            for n2 in range(1, self.n + 1):
                if n1 == n2:
                    continue
                
                payload = f"{n1},{n2}"
                
                parsed_adj = {"query_adjacent": payload}
                ans_adj = self._cf_core_produce(parsed_adj)
                queries.append({
                    "query": f"<query_adjacent>{payload}</query_adjacent>",
                    "answer": ans_adj
                })
                
                parsed_anc = {"query_ancestor": payload}
                ans_anc = self._cf_core_produce(parsed_anc)
                queries.append({
                    "query": f"<query_ancestor>{payload}</query_ancestor>",
                    "answer": ans_anc
                })
                
        return queries

    def _cf_make_wrong(self, correct):
        if correct.lstrip('-').isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        if correct.lower() == "yes":
            return "No"
        if correct.lower() == "no":
            return "Yes"
        
        if correct == "无":
            return "1"
        if correct == "None":
            return "1"
        
        if correct.startswith("[") and correct.endswith("]"):
            if correct == "[]":
                return "[1]"
            else:
                return "[]"
                
        return correct + "_WRONG"