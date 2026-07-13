# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   层序遍历层内容：层序遍历中第k层包含哪些节点
# ============================================================

from .base import Game
import random


class TreeDepthExplorationGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树深度探索"游戏，规则如下：

游戏设定了一棵固定的有根树，包含 {n} 个节点，每个节点有唯一的 ID。树的根节点 ID 为 {root}，根节点的深度定义为 0，任意其他节点的深度为该节点到根节点唯一路径上的边数。

初始时，你仅知道根节点 {root}，其他节点的 ID 需要通过查询获得。

你的目标是：唯一确定深度为 {k} 的全部节点 ID 的集合。

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据树的真实结构如实回答：

1. 孩子查询：询问节点 X 的所有直接子节点 ID 列表。若无子节点，返回空列表。
2. 层数查询：询问节点 X 的深度（非负整数）。
3. 直连查询：询问节点 C 是否为节点 P 的直接子节点。回答"是"或"否"。
4. 层宽查询：询问深度为 d 的节点数量（非负整数）。

注意：查询只能针对已知的节点 ID 或已定义的整数参数发起。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 孩子查询（例如查询节点 5 的子节点）：
<query_children>5</query_children>

- 层数查询（例如查询节点 3 的深度）：
<query_depth>3</query_depth>

- 直连查询（例如查询节点 7 是否为节点 3 的直接子节点）：
<query_parent>3,7</query_parent>

- 层宽查询（例如查询深度为 2 的节点数量）：
<query_width>2</query_width>

提交最终答案时，必须列出深度为 {k} 的所有节点 ID（用逗号隔开，顺序不限），格式如下：

<answer>1,2,3</answer>
"""

    game_rule_en = """\
Let's play a "Tree Depth Exploration" game. Here are the rules:

The game features a fixed rooted tree with {n} nodes, each having a unique ID. The root node has ID {root}, with depth 0. The depth of any other node is defined as the number of edges on the unique path from that node to the root.

Initially, you only know the root node {root}. Other node IDs must be discovered through queries.

Your goal is: to uniquely determine the complete set of node IDs at depth {k}.

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the tree's actual structure:

1. Children Query: Ask for the list of all direct child node IDs of node X. Returns an empty list if no children exist.
2. Depth Query: Ask for the depth (non-negative integer) of node X.
3. Parent Query: Ask if node C is a direct child of node P. Answer "Yes" or "No".
4. Width Query: Ask for the number of nodes at depth d (non-negative integer).

Note: Queries can only be made for known node IDs or defined integer parameters.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Children Query (e.g., querying children of node 5):
<query_children>5</query_children>

- Depth Query (e.g., querying depth of node 3):
<query_depth>3</query_depth>

- Parent Query (e.g., querying if node 7 is a direct child of node 3):
<query_parent>3,7</query_parent>

- Width Query (e.g., querying number of nodes at depth 2):
<query_width>2</query_width>

When submitting the final answer, list all node IDs at depth {k} (comma-separated, order does not matter), using this format:

<answer>1,2,3</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“交通路网拓扑分析系统”。你作为一名资深交通规划师，需要对一片未知区域的交通网络进行梳理。

系统设定了一个固定的交通管辖网络（树形结构），包含 {n} 个站点，每个站点有唯一的 ID。网络的总枢纽站点 ID 为 {root}，其层级深度定义为 0。任意其他站点的层级深度，定义为该站点到总枢纽的唯一换乘路径上的区段数（边数）。

初始时，你仅掌握总枢纽节点 {root} 的情报，其他站点的 ID 需要通过系统查询获得。

你的目标是：唯一确定层级深度为 {k} 的全部站点 ID 的集合（即第 {k} 级支线站点）。

你可以反复向系统提出以下四类查询（每次仅限一个查询），系统会根据真实的交通网络拓扑如实反馈：

1. 孩子查询：询问站点 X 的所有直接下一级站点 ID 列表。若无下一级站点，返回空列表。
2. 层数查询：询问站点 X 的层级深度（非负整数）。
3. 直连查询：询问站点 C 是否为站点 P 的直接下一级站点。回答“是”或“否”。
4. 层宽查询：询问层级深度为 d 的站点数量（非负整数）。

注意：查询只能针对已知的站点 ID 或已定义的整数参数发起。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，规划任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 孩子查询（例如查询站点 5 的直接下一级站点）：
<query_children>5</query_children>

- 层数查询（例如查询站点 3 的层级深度）：
<query_depth>3</query_depth>

- 直连查询（例如查询站点 7 是否为站点 3 的直接下一级站点）：
<query_parent>3,7</query_parent>

- 层宽查询（例如查询层级深度为 2 的站点数量）：
<query_width>2</query_width>

提交最终答案时，必须列出层级深度为 {k} 的所有站点 ID（用逗号隔开，顺序不限），格式如下：

<answer>1,2,3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Traffic Network Topology Analysis System". As a senior traffic planner, you need to map out the transportation network of an uncharted region.

The system features a fixed hierarchical transit network (a rooted tree) with {n} stations, each having a unique ID. The central hub station has the ID {root}, with a hierarchy depth of 0. The depth of any other station is defined as the number of transit segments (edges) on its unique path to the central hub.

Initially, you only know the central hub {root}. Other station IDs must be discovered through system queries.

Your goal is: to uniquely determine the complete set of station IDs at depth {k} (i.e., the {k}-th level branch stations).

You can repeatedly ask the system four types of queries (one per turn), and the system will answer truthfully based on the actual network topology:

1. Children Query: Ask for the list of all direct next-level station IDs of station X. Returns an empty list if none exist.
2. Depth Query: Ask for the hierarchy depth (non-negative integer) of station X.
3. Parent Query: Ask if station C is a direct next-level station of station P. Answer "Yes" or "No".
4. Width Query: Ask for the number of stations at depth d (non-negative integer).

Note: Queries can only be made for known station IDs or defined integer parameters.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the planning task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Children Query (e.g., querying next-level stations of station 5):
<query_children>5</query_children>

- Depth Query (e.g., querying depth of station 3):
<query_depth>3</query_depth>

- Parent Query (e.g., querying if station 7 is a direct next-level station of station 3):
<query_parent>3,7</query_parent>

- Width Query (e.g., querying number of stations at depth 2):
<query_width>2</query_width>

When submitting the final answer, list all station IDs at depth {k} (comma-separated, order does not matter), using this format:

<answer>1,2,3</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“病毒变异图谱追踪系统”。你作为一名流行病学专家，需要厘清一种新型病毒的变异谱系。

系统记录了一棵固定的变异株进化树，包含 {n} 个变异株节点，每个节点有唯一的 ID。进化树的原始毒株 ID 为 {root}，其变异代次（深度）定义为 0。任意其他变异株的变异代次，定义为该毒株溯源至原始毒株的唯一进化路径上的突变次数（边数）。

初始时，你仅分离出了原始毒株 {root}，其他变异株的 ID 需要通过检测查询获得。

你的目标是：唯一确定变异代次为 {k} 的全部变异株 ID 的集合（即第 {k} 代变异株）。

你可以反复向系统提出以下四类查询（每次仅限一个查询），系统会根据真实的进化树如实反馈：

1. 孩子查询：询问变异株 X 的所有直接衍生下一代变异株 ID 列表。若无衍生变异株，返回空列表。
2. 层数查询：询问变异株 X 的变异代次（非负整数）。
3. 直连查询：询问变异株 C 是否由变异株 P 直接突变衍生而来。回答“是”或“否”。
4. 层宽查询：询问变异代次为 d 的变异株数量（非负整数）。

注意：查询只能针对已知的变异株 ID 或已定义的整数参数发起。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，溯源任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 孩子查询（例如查询变异株 5 的直接衍生毒株）：
<query_children>5</query_children>

- 层数查询（例如查询变异株 3 的变异代次）：
<query_depth>3</query_depth>

- 直连查询（例如查询变异株 7 是否为变异株 3 的直接衍生毒株）：
<query_parent>3,7</query_parent>

- 层宽查询（例如查询变异代次为 2 的变异株数量）：
<query_width>2</query_width>

提交最终答案时，必须列出变异代次为 {k} 的所有变异株 ID（用逗号隔开，顺序不限），格式如下：

<answer>1,2,3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Viral Mutation Lineage Tracking System". As an epidemiologist, your task is to clarify the mutation pedigree of a novel virus.

The system records a fixed mutation evolutionary tree comprising {n} strain nodes, each with a unique ID. The original strain in the tree has ID {root}, and its mutation generation (depth) is defined as 0. The generation of any other strain is defined as the number of mutations (edges) on its unique evolutionary path back to the original strain.

Initially, you have only isolated the original strain {root}. Other strain IDs must be discovered through testing queries.

Your goal is: to uniquely determine the complete set of strain IDs at mutation generation {k} (i.e., the {k}-th generation strains).

You can repeatedly ask the system four types of queries (one per turn), and the system will answer truthfully based on the actual evolutionary tree:

1. Children Query: Ask for the list of all direct descendant strain IDs derived from strain X. Returns an empty list if none exist.
2. Depth Query: Ask for the mutation generation (non-negative integer) of strain X.
3. Parent Query: Ask if strain C is a direct mutation derived from strain P. Answer "Yes" or "No".
4. Width Query: Ask for the number of strains at mutation generation d (non-negative integer).

Note: Queries can only be made for known strain IDs or defined integer parameters.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the tracking task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Children Query (e.g., querying direct descendants of strain 5):
<query_children>5</query_children>

- Depth Query (e.g., querying mutation generation of strain 3):
<query_depth>3</query_depth>

- Parent Query (e.g., querying if strain 7 is directly derived from strain 3):
<query_parent>3,7</query_parent>

- Width Query (e.g., querying number of strains at generation 2):
<query_width>2</query_width>

When submitting the final answer, list all strain IDs at generation {k} (comma-separated, order does not matter), using this format:

<answer>1,2,3</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学科知识图谱分析平台”。你作为一名课程设计专家，需要梳理一门复杂学科的前置依赖层级。

系统内置了一棵固定的知识体系依赖树，包含 {n} 个知识模块，每个模块有唯一的 ID。该学科的基石模块 ID 为 {root}，其进阶深度定义为 0。任意其他模块的进阶深度，定义为掌握该模块所需经过的、从基石模块出发的唯一先修路径上的模块跨度（边数）。

初始时，你仅了解基石模块 {root}，其他进阶模块的 ID 需要通过查阅大纲获得。

你的目标是：唯一确定进阶深度为 {k} 的全部知识模块 ID 的集合（即第 {k} 层级的进阶知识点）。

你可以反复向系统提出以下四类查询（每次仅限一个查询），系统会根据真实的课程图谱如实反馈：

1. 孩子查询：询问知识模块 X 的所有直接后继进阶模块 ID 列表。若无后继模块，返回空列表。
2. 层数查询：询问知识模块 X 的进阶深度（非负整数）。
3. 直连查询：询问知识模块 C 是否以知识模块 P 为直接先决条件。回答“是”或“否”。
4. 层宽查询：询问进阶深度为 d 的模块数量（非负整数）。

注意：查询只能针对已知的知识模块 ID 或已定义的整数参数发起。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，教案规划任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 孩子查询（例如查询模块 5 的直接后继模块）：
<query_children>5</query_children>

- 层数查询（例如查询模块 3 的进阶深度）：
<query_depth>3</query_depth>

- 直连查询（例如查询模块 7 是否直接依赖于模块 3）：
<query_parent>3,7</query_parent>

- 层宽查询（例如查询进阶深度为 2 的知识模块数量）：
<query_width>2</query_width>

提交最终答案时，必须列出进阶深度为 {k} 的所有知识模块 ID（用逗号隔开，顺序不限），格式如下：

<answer>1,2,3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Subject Knowledge Graph Analysis Platform". As a curriculum design expert, you need to map out the prerequisite hierarchy of a complex academic discipline.

The system contains a fixed dependency tree of knowledge modules, consisting of {n} modules, each with a unique ID. The foundational module of the subject has ID {root}, and its advanced depth is defined as 0. The advanced depth of any other module is defined as the number of learning steps (edges) on its unique prerequisite path starting from the foundational module.

Initially, you are only aware of the foundational module {root}. The IDs of other advanced modules must be acquired by consulting the syllabus.

Your goal is: to uniquely determine the complete set of knowledge module IDs at an advanced depth of {k} (i.e., the {k}-th level advanced topics).

You can repeatedly ask the system four types of queries (one per turn), and the system will answer truthfully based on the actual curriculum graph:

1. Children Query: Ask for the list of all direct successor module IDs for knowledge module X. Returns an empty list if none exist.
2. Depth Query: Ask for the advanced depth (non-negative integer) of knowledge module X.
3. Parent Query: Ask if knowledge module C has knowledge module P as its direct prerequisite. Answer "Yes" or "No".
4. Width Query: Ask for the number of modules at advanced depth d (non-negative integer).

Note: Queries can only be made for known module IDs or defined integer parameters.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the curriculum planning task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Children Query (e.g., querying successor modules of module 5):
<query_children>5</query_children>

- Depth Query (e.g., querying depth of module 3):
<query_depth>3</query_depth>

- Parent Query (e.g., querying if module 7 directly depends on module 3):
<query_parent>3,7</query_parent>

- Width Query (e.g., querying number of modules at depth 2):
<query_width>2</query_width>

When submitting the final answer, list all knowledge module IDs at advanced depth {k} (comma-separated, order does not matter), using this format:

<answer>1,2,3</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“产品 BOM (物料清单) 解析系统”。你作为一名工业制造工程师，需要反向拆解一款精密设备的部件装配层级。

系统内载入了一款产品的固定 BOM 树，包含 {n} 个零部件，每个零部件有唯一的物料 ID。最终组装成品的 ID 为 {root}，其拆解层级定义为 0。任意其他零部件的拆解层级，定义为该零件到最终成品唯一装配路径上的拆解嵌套次数（边数）。

初始时，你仅掌握成品的物料 ID {root}，其他底层零部件的 ID 需要通过查阅系统图纸获得。

你的目标是：唯一确定拆解层级为 {k} 的全部零部件 ID 的集合（即第 {k} 级子装配体/零件）。

你可以反复向系统提出以下四类查询（每次仅限一个查询），系统会根据真实的物理装配结构如实反馈：

1. 孩子查询：询问零部件 X 的所有直接下级组成零件 ID 列表。若无下级零件，返回空列表。
2. 层数查询：询问零部件 X 的拆解层级（非负整数）。
3. 直连查询：询问零部件 C 是否为零部件 P 的直接下属装配组件。回答“是”或“否”。
4. 层宽查询：询问拆解层级为 d 的零部件数量（非负整数）。

注意：查询只能针对已知的零部件 ID 或已定义的整数参数发起。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，解析任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 孩子查询（例如查询零部件 5 的直接下级组件）：
<query_children>5</query_children>

- 层数查询（例如查询零部件 3 的拆解层级）：
<query_depth>3</query_depth>

- 直连查询（例如查询零部件 7 是否为零部件 3 的直接组成部分）：
<query_parent>3,7</query_parent>

- 层宽查询（例如查询拆解层级为 2 的零部件数量）：
<query_width>2</query_width>

提交最终答案时，必须列出拆解层级为 {k} 的所有零部件 ID（用逗号隔开，顺序不限），格式如下：

<answer>1,2,3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Product BOM (Bill of Materials) Parsing System". As an industrial manufacturing engineer, you need to reverse-engineer the component assembly hierarchy of a precision device.

The system loads a fixed BOM tree for a product, encompassing {n} parts, each with a unique material ID. The final assembled product has the ID {root}, and its disassembly level is defined as 0. The disassembly level of any other part is defined as the number of nesting layers (edges) on its unique assembly path up to the final product.

Initially, you only possess the material ID of the final product {root}. The IDs of other underlying components must be retrieved by consulting the system's blueprints.

Your goal is: to uniquely determine the complete set of component IDs at disassembly level {k} (i.e., the {k}-th level sub-assemblies/parts).

You can repeatedly ask the system four types of queries (one per turn), and the system will answer truthfully based on the actual physical assembly structure:

1. Children Query: Ask for the list of all direct lower-level sub-component IDs for part X. Returns an empty list if none exist.
2. Depth Query: Ask for the disassembly level (non-negative integer) of part X.
3. Parent Query: Ask if part C is a direct sub-assembly component of part P. Answer "Yes" or "No".
4. Width Query: Ask for the number of parts at disassembly level d (non-negative integer).

Note: Queries can only be made for known part IDs or defined integer parameters.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the parsing task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Children Query (e.g., querying direct sub-components of part 5):
<query_children>5</query_children>

- Depth Query (e.g., querying disassembly level of part 3):
<query_depth>3</query_depth>

- Parent Query (e.g., querying if part 7 is a direct structural element of part 3):
<query_parent>3,7</query_parent>

- Width Query (e.g., querying number of parts at disassembly level 2):
<query_width>2</query_width>

When submitting the final answer, list all part IDs at disassembly level {k} (comma-separated, order does not matter), using this format:

<answer>1,2,3</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“法律条款渊源与派生检索系统”。你作为一名法务资深研究员，需要理清某部庞大法典的条款层级结构。

系统收录了一棵固定的法典条款树，包含 {n} 项法条，每个条款有唯一的法条 ID。该法典的核心根本法案（上位法）ID 为 {root}，其派生深度定义为 0。任意其他细则的派生深度，定义为该条款回溯至根本法案的唯一法理渊源路径上的派生层数（边数）。

初始时，你仅知晓根本法案 {root} 的 ID，其他派生细则的 ID 需要通过法理检索获得。

你的目标是：唯一确定派生深度为 {k} 的全部法律条款 ID 的集合（即第 {k} 级下位法/细则）。

你可以反复向系统提出以下四类查询（每次仅限一个查询），系统会根据真实的法典体系如实反馈：

1. 孩子查询：询问条款 X 的所有直接派生下位条款 ID 列表。若无下位条款，返回空列表。
2. 层数查询：询问条款 X 的派生深度（非负整数）。
3. 直连查询：询问条款 C 是否为条款 P 的直接派生细则。回答“是”或“否”。
4. 层宽查询：询问派生深度为 d 的条款数量（非负整数）。

注意：查询只能针对已知的条款 ID 或已定义的整数参数发起。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，法理梳理任务失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 孩子查询（例如查询条款 5 的直接派生条款）：
<query_children>5</query_children>

- 层数查询（例如查询条款 3 的派生深度）：
<query_depth>3</query_depth>

- 直连查询（例如查询条款 7 是否为条款 3 的直接下位条款）：
<query_parent>3,7</query_parent>

- 层宽查询（例如查询派生深度为 2 的条款数量）：
<query_width>2</query_width>

提交最终答案时，必须列出派生深度为 {k} 的所有法律条款 ID（用逗号隔开，顺序不限），格式如下：

<answer>1,2,3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Legal Article Source and Derivation Retrieval System". As a senior legal researcher, you are required to clarify the hierarchical structure of a voluminous legal code.

The system encapsulates a fixed tree of legal articles, containing {n} clauses, each with a unique article ID. The core root act (superior law) of this code has the ID {root}, and its derivation depth is defined as 0. The derivation depth of any other specific rule is defined as the number of derivation layers (edges) on its unique jurisprudential path tracing back to the root act.

Initially, you are only aware of the root act {root}. The IDs of other derived regulations must be retrieved through legal queries.

Your goal is: to uniquely determine the complete set of legal article IDs at derivation depth {k} (i.e., the {k}-th level subordinate laws/regulations).

You can repeatedly ask the system four types of queries (one per turn), and the system will answer truthfully based on the actual legal framework:

1. Children Query: Ask for the list of all direct subordinate article IDs derived from article X. Returns an empty list if none exist.
2. Depth Query: Ask for the derivation depth (non-negative integer) of article X.
3. Parent Query: Ask if article C is a directly derived specific rule of article P. Answer "Yes" or "No".
4. Width Query: Ask for the number of articles at derivation depth d (non-negative integer).

Note: Queries can only be made for known article IDs or defined integer parameters.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the jurisprudential mapping task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Children Query (e.g., querying direct derived articles of article 5):
<query_children>5</query_children>

- Depth Query (e.g., querying derivation depth of article 3):
<query_depth>3</query_depth>

- Parent Query (e.g., querying if article 7 is a direct subordinate clause of article 3):
<query_parent>3,7</query_parent>

- Width Query (e.g., querying number of articles at derivation depth 2):
<query_width>2</query_width>

When submitting the final answer, list all legal article IDs at derivation depth {k} (comma-separated, order does not matter), using this format:

<answer>1,2,3</answer>
"""

    tags = ["answer", "query_children", "query_depth", "query_parent", "query_width"]

    # 难度配置：
    # 1 (简单)       - N=7,  k=2, 简单的完全二叉树
    # 2 (中等偏下)   - N=10, k=3, 非对称树
    # 3 (中等偏上)   - N=15, k=3, 较复杂的多叉树
    # 4 (较难)       - N=20, k=4, 深度较大的不平衡树
    # 5 (难)         - N=25, k=4, 复杂的多分支树

    _SHARED_DIFFICULTY_CONFIG = {
        1: {
            "n": 7,
            "root": 1,
            "k": 2,
            # 树结构: 1 -> [2,3], 2 -> [4,5], 3 -> [6,7]
            "tree": {
                1: [2, 3],
                2: [4, 5],
                3: [6, 7],
                4: [],
                5: [],
                6: [],
                7: []
            }
        },
        2: {
            "n": 10,
            "root": 1,
            "k": 3,
            # 树结构: 1 -> [2,3], 2 -> [4,5,6], 3 -> [7], 4 -> [8,9], 5 -> [10]
            "tree": {
                1: [2, 3],
                2: [4, 5, 6],
                3: [7],
                4: [8, 9],
                5: [10],
                6: [],
                7: [],
                8: [],
                9: [],
                10: []
            }
        },
        3: {
            "n": 15,
            "root": 1,
            "k": 3,
            # 树结构: 1 -> [2,3,4], 2 -> [5,6], 3 -> [7,8,9], 4 -> [10], 5 -> [11,12], 7 -> [13,14], 8 -> [15]
            "tree": {
                1: [2, 3, 4],
                2: [5, 6],
                3: [7, 8, 9],
                4: [10],
                5: [11, 12],
                6: [],
                7: [13, 14],
                8: [15],
                9: [],
                10: [],
                11: [],
                12: [],
                13: [],
                14: [],
                15: []
            }
        },
        4: {
            "n": 20,
            "root": 1,
            "k": 4,
            # 更复杂的树结构
            "tree": {
                1: [2, 3],
                2: [4, 5, 6],
                3: [7, 8],
                4: [9, 10],
                5: [11],
                6: [12, 13],
                7: [14, 15],
                8: [16],
                9: [17, 18],
                10: [19],
                12: [20],
                11: [],
                13: [],
                14: [],
                15: [],
                16: [],
                17: [],
                18: [],
                19: [],
                20: []
            }
        },
        5: {
            "n": 25,
            "root": 1,
            "k": 4,
            # 最复杂的树结构
            "tree": {
                1: [2, 3, 4],
                2: [5, 6, 7],
                3: [8, 9],
                4: [10, 11, 12],
                5: [13, 14],
                6: [15],
                7: [16, 17],
                8: [18, 19],
                9: [20],
                10: [21],
                11: [22, 23],
                12: [24, 25],
                13: [],
                14: [],
                15: [],
                16: [],
                17: [],
                18: [],
                19: [],
                20: [],
                21: [],
                22: [],
                23: [],
                24: [],
                25: []
            }
        }
    }

    DIFFICULTY_CONFIG = {
        "zh": _SHARED_DIFFICULTY_CONFIG,
        "en": _SHARED_DIFFICULTY_CONFIG
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
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self._game_info["k"] = cfg["k"]
        
        # 保存树结构
        self.tree = cfg["tree"]
        self.root = cfg["root"]
        self.target_depth = cfg["k"]
        
        # 计算每个节点的深度
        self.node_depths = {}
        self._compute_depths(self.root, 0)
        
        # 计算目标深度的节点集合（Ground Truth）
        self.target_nodes = set()
        for node_id, depth in self.node_depths.items():
            if depth == self.target_depth:
                self.target_nodes.add(node_id)
        
        # 记录已知节点（初始只有根节点已知）
        self.known_nodes = {self.root}

    def _compute_depths(self, node, depth):
        """递归计算所有节点的深度"""
        self.node_depths[node] = depth
        for child in self.tree[node]:
            self._compute_depths(child, depth + 1)

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            # 解析答案中的节点 ID 列表
            if not raw_ans:
                return False
            model_nodes = set(int(x.strip()) for x in raw_ans.split(",") if x.strip())
        except:
            return False
        
        # 检查答案集合是否与目标集合完全一致
        return model_nodes == self.target_nodes

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_unknown = "错误：节点 ID 未知或不存在。"
            error_format = "错误：查询格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_unknown = "Error: Node ID is unknown or does not exist."
            error_format = "Error: Invalid query format."

        # 优先级：children > depth > parent > width
        if "query_children" in parsed_info:
            try:
                node_id = int(parsed_info["query_children"].strip())
                # 检查节点是否已知
                if node_id not in self.known_nodes:
                    return error_unknown
                if node_id not in self.tree:
                    return error_unknown
                
                children = self.tree[node_id]
                # 将子节点加入已知节点集合
                self.known_nodes.update(children)
                
                if not children:
                    return "[]"
                return "[" + ",".join(map(str, children)) + "]"
            except:
                return error_format

        elif "query_depth" in parsed_info:
            try:
                node_id = int(parsed_info["query_depth"].strip())
                # 检查节点是否已知
                if node_id not in self.known_nodes:
                    return error_unknown
                if node_id not in self.node_depths:
                    return error_unknown
                return str(self.node_depths[node_id])
            except:
                return error_format

        elif "query_parent" in parsed_info:
            try:
                raw = parsed_info["query_parent"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                parent_id = int(parts[0])
                child_id = int(parts[1])
                
                # 检查节点是否已知
                if parent_id not in self.known_nodes or child_id not in self.known_nodes:
                    return error_unknown
                if parent_id not in self.tree:
                    return error_unknown
                
                is_child = child_id in self.tree[parent_id]
                return yes_res if is_child else no_res
            except:
                return error_format

        elif "query_width" in parsed_info:
            try:
                depth = int(parsed_info["query_width"].strip())
                if depth < 0:
                    return error_format
                
                # 统计指定深度的节点数量
                count = sum(1 for d in self.node_depths.values() if d == depth)
                return str(count)
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        correct_str = str(correct).strip()

        # 1. 纯整数 -> +1
        try:
            val = int(correct_str)
            return str(val + 1)
        except ValueError:
            pass

        # 2. Yes/No 关键词替换
        if correct_str == "是":
            return "否"
        elif correct_str == "否":
            return "是"
        elif correct_str.lower() == "yes":
            return "No"
        elif correct_str.lower() == "no":
            return "Yes"

        # 3. 列表格式 -> 篡改内容
        if correct_str.startswith("[") and correct_str.endswith("]"):
            inner = correct_str[1:-1].strip()
            if not inner:
                # 空列表 -> 伪造一个节点
                return "[999]"
            else:
                # 非空列表 -> 移除最后一个元素
                parts = [x.strip() for x in inner.split(",") if x.strip()]
                if len(parts) > 1:
                    return "[" + ",".join(parts[:-1]) + "]"
                else:
                    # 只有一个元素 -> 替换为不同的值
                    try:
                        return "[" + str(int(parts[0]) + 100) + "]"
                    except ValueError:
                        return "[999]"

        # 4. 其他情况 -> 追加 _WRONG
        return f"{correct_str}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        
        # 获取所有节点 ID 并排序
        all_nodes = sorted(list(self.tree.keys()))
        # 计算最大深度
        max_depth = max(self.node_depths.values()) if self.node_depths else 0
        
        # 预定义回答文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 1. 孩子查询
        for node_id in all_nodes:
            children = self.tree.get(node_id, [])
            if not children:
                ans = "[]"
            else:
                ans = "[" + ",".join(map(str, children)) + "]"
            
            queries.append({
                "query": f"<query_children>{node_id}</query_children>",
                "answer": ans
            })

        # 2. 层数查询
        for node_id in all_nodes:
            depth = self.node_depths.get(node_id, 0)
            queries.append({
                "query": f"<query_depth>{node_id}</query_depth>",
                "answer": str(depth)
            })

        # 3. 直连查询 (Parent Query)
        # 枚举所有节点对 (P, C)，这里简单起见枚举所有 P 和所有 C (除去 P=C)
        for p_id in all_nodes:
            for c_id in all_nodes:
                if p_id == c_id:
                    continue
                
                is_child = c_id in self.tree.get(p_id, [])
                ans = yes_res if is_child else no_res
                
                queries.append({
                    "query": f"<query_parent>{p_id},{c_id}</query_parent>",
                    "answer": ans
                })

        # 4. 层宽查询
        # 从 0 层到 max_depth + 1 (包含空层以展示0的情况)
        for d in range(max_depth + 2):
            count = sum(1 for depth in self.node_depths.values() if depth == d)
            queries.append({
                "query": f"<query_width>{d}</query_width>",
                "answer": str(count)
            })

        return queries