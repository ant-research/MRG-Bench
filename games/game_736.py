# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   最近公共祖先：两个给定节点的最近公共祖先是哪个节点
# ============================================================

from .base import Game
import random


class TreeLCAGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"隐藏树结构推理"游戏，规则如下：

游戏设定了一棵有根树 T，包含 {n} 个节点，标识为 {nodes}。树是连通的、无环的，且存在唯一的根节点 {root}。

公开信息：
- 节点总数：{n}
- 所有节点标识：{nodes}
- 根节点：{root}
- 两个目标节点：{target_a} 和 {target_b}

隐藏信息：
- 树的边集（即所有父子关系和整体拓扑结构）

你的目标是推断出节点 {target_a} 和 {target_b} 的最近公共祖先（LCA）。最近公共祖先是指同时是这两个节点的祖先、且深度最大的那个节点。

术语说明：
- 父节点：每个非根节点有且仅有一个父节点
- 祖先关系：X 是 Y 的祖先，当且仅当沿父链从 Y 可到达 X（允许 X 等于 Y）
- 深度：根节点深度为 0；任一节点的深度为从根到该节点路径的边数

你可以反复向我提出以下五类查询（每次仅限一个查询），我会根据真实的树结构如实回答：

1. parent(X)：询问节点 X 的父节点是谁
2. depth(X)：询问节点 X 的深度是多少
3. isAncestor(X,Y)：询问 X 是否为 Y 的祖先（包含自身）
4. compareDepth(X,Y)：询问 X 与 Y 谁更靠近根
5. jumpUp(X,k)：询问从 X 沿父链向上跳 k 步到达哪里（k 为非负整数）

约束条件：
- 禁止直接询问最近公共祖先相关问题
- 禁止请求某节点的子节点列表或整棵树结构
- 查询必须使用有效的节点标识和合法参数

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询父节点（例如查询 H1 的父节点）：
<query_parent>H1</query_parent>

- 查询深度（例如查询 H1 的深度）：
<query_depth>H1</query_depth>

- 查询祖先关系（例如查询 H1 是否为 H3 的祖先）：
<query_ancestor>H1,H3</query_ancestor>

- 比较深度（例如比较 H1 和 H2 的深度）：
<query_compare_depth>H1,H2</query_compare_depth>

- 向上跳跃（例如从 H5 向上跳 2 步）：
<query_jump>H5,2</query_jump>

提交最终答案时，请使用以下格式：

<answer>H3</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Tree Structure Deduction" game. Here are the rules:

The game has a rooted tree T with {n} nodes, identified as {nodes}. The tree is connected, acyclic, and has a unique root node {root}.

Public Information:
- Total number of nodes: {n}
- All node identifiers: {nodes}
- Root node: {root}
- Two target nodes: {target_a} and {target_b}

Hidden Information:
- The edge set of the tree (i.e., all parent-child relationships and the overall topology)

Your goal is to infer the Lowest Common Ancestor (LCA) of nodes {target_a} and {target_b}. The LCA is the common ancestor of both nodes with the maximum depth.

Terminology:
- Parent node: Each non-root node has exactly one parent
- Ancestor relation: X is an ancestor of Y if and only if Y can reach X by following parent links (X may equal Y)
- Depth: The root has depth 0; any node's depth is the number of edges from the root to that node

You can repeatedly ask me five types of queries (one query per turn), and I will answer truthfully based on the real tree structure:

1. parent(X): Ask who is the parent of node X
2. depth(X): Ask what is the depth of node X
3. isAncestor(X,Y): Ask whether X is an ancestor of Y (including self)
4. compareDepth(X,Y): Ask which of X and Y is closer to the root
5. jumpUp(X,k): Ask where you reach by jumping up k steps from X along the parent chain (k is a non-negative integer)

Constraints:
- Direct queries about the lowest common ancestor are forbidden
- Requesting a node's child list or the entire tree structure is forbidden
- Queries must use valid node identifiers and legal parameters

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query parent (e.g., query parent of H1):
<query_parent>H1</query_parent>

- Query depth (e.g., query depth of H1):
<query_depth>H1</query_depth>

- Query ancestor relation (e.g., query if H1 is ancestor of H3):
<query_ancestor>H1,H3</query_ancestor>

- Compare depth (e.g., compare depth of H1 and H2):
<query_compare_depth>H1,H2</query_compare_depth>

- Jump up (e.g., jump up 2 steps from H5):
<query_jump>H5,2</query_jump>

When submitting the final answer, use this format:

<answer>H3</answer>
"""

    # ================= 场景改造 1：交通 =================
    contextualized_rule_zh_1 = """\
我们来玩一个"交通路网指挥层级推理"系统，规则如下：

系统设定了一棵有根指挥树 T，包含 {n} 个指挥枢纽，标识为 {nodes}。指挥网是连通的、无环的，且存在唯一的总指挥中心 {root}。

公开信息：
- 枢纽总数：{n}
- 所有枢纽标识：{nodes}
- 总指挥中心：{root}
- 两个目标枢纽：{target_a} 和 {target_b}

隐藏信息：
- 指挥树的边集（即所有上下级管辖关系和整体拓扑结构）

你的目标是推断出枢纽 {target_a} 和 {target_b} 的最近共同上级中心（LCA）。最近共同上级是指同时是这两个枢纽的上级、且指挥深度最大的那个中心。

术语说明：
- 上级中心：每个非总指挥中心的枢纽有且仅有一个直接上级中心
- 管辖关系：X 是 Y 的上级，当且仅当沿指挥链从 Y 可到达 X（允许 X 等于 Y）
- 深度：总指挥中心深度为 0；任一枢纽的深度为从总指挥中心到该枢纽路径的层级数

你可以反复向我提出以下五类查询（每次仅限一个查询），我会根据真实的指挥网结构如实回答：

1. parent(X)：询问枢纽 X 的直接上级中心是谁
2. depth(X)：询问枢纽 X 的指挥深度是多少
3. isAncestor(X,Y)：询问 X 是否为 Y 的上级管辖中心（包含自身）
4. compareDepth(X,Y)：询问 X 与 Y 谁更靠近总指挥中心
5. jumpUp(X,k)：询问从 X 沿指挥链向上跳 k 级到达哪里（k 为非负整数）

约束条件：
- 禁止直接询问最近共同上级相关问题
- 禁止请求某枢纽的下属列表或整个指挥网结构
- 查询必须使用有效的枢纽标识和合法参数

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询直接上级中心（例如查询 H1 的直接上级）：
<query_parent>H1</query_parent>

- 查询指挥深度（例如查询 H1 的深度）：
<query_depth>H1</query_depth>

- 查询管辖关系（例如查询 H1 是否为 H3 的上级）：
<query_ancestor>H1,H3</query_ancestor>

- 比较深度（例如比较 H1 和 H2 谁更靠近总指挥中心）：
<query_compare_depth>H1,H2</query_compare_depth>

- 向上跳跃（例如从 H5 沿指挥链向上跳 2 级）：
<query_jump>H5,2</query_jump>

提交最终答案时，请使用以下格式：

<answer>H3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Traffic Network Command Hierarchy Deduction" game. Here are the rules:

The system features a rooted command tree T with {n} command hubs, identified as {nodes}. The hierarchy is connected, acyclic, and has a unique General Command Center {root}.

Public Information:
- Total number of hubs: {n}
- All hub identifiers: {nodes}
- General Command Center: {root}
- Two target hubs: {target_a} and {target_b}

Hidden Information:
- The edge set of the command tree (i.e., all superior-subordinate relationships and overall topology)

Your goal is to infer the Lowest Common Superior Command Center (LCA) of hubs {target_a} and {target_b}. The LCA is the common superior of both hubs with the maximum command depth.

Terminology:
- Superior center: Each non-general center hub has exactly one direct superior center
- Jurisdiction relation: X is a superior of Y if and only if Y can reach X by following the command chain (X may equal Y)
- Depth: The General Command Center has depth 0; any hub's depth is the number of levels from the general center to that hub

You can repeatedly ask me five types of queries (one query per turn), and I will answer truthfully based on the real network structure:

1. parent(X): Ask who is the direct superior center of hub X
2. depth(X): Ask what is the command depth of hub X
3. isAncestor(X,Y): Ask whether X is a superior center of Y (including self)
4. compareDepth(X,Y): Ask which of X and Y is closer to the General Command Center
5. jumpUp(X,k): Ask where you reach by jumping up k levels from X along the command chain (k is a non-negative integer)

Constraints:
- Direct queries about the lowest common superior are forbidden
- Requesting a hub's subordinate list or the entire network structure is forbidden
- Queries must use valid hub identifiers and legal parameters

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query superior center (e.g., query superior of H1):
<query_parent>H1</query_parent>

- Query depth (e.g., query depth of H1):
<query_depth>H1</query_depth>

- Query jurisdiction relation (e.g., query if H1 is superior of H3):
<query_ancestor>H1,H3</query_ancestor>

- Compare depth (e.g., compare depth of H1 and H2):
<query_compare_depth>H1,H2</query_compare_depth>

- Jump up (e.g., jump up 2 levels from H5):
<query_jump>H5,2</query_jump>

When submitting the final answer, use this format:

<answer>H3</answer>
"""

    # ================= 场景改造 2：医疗 =================
    contextualized_rule_zh_2 = """\
我们来玩一个"病毒变异溯源推理"系统，规则如下：

系统设定了一棵有根变异树 T，包含 {n} 个病毒毒株，标识为 {nodes}。变异体系是连通的、无环的，且存在唯一的原始毒株（零号毒株） {root}。

公开信息：
- 毒株总数：{n}
- 所有毒株标识：{nodes}
- 原始毒株：{root}
- 两个目标毒株：{target_a} 和 {target_b}

隐藏信息：
- 变异树的边集（即所有直接突变关系和整体演化拓扑）

你的目标是推断出毒株 {target_a} 和 {target_b} 的最近共同变异祖先（LCA）。最近共同变异祖先是指同时是这两个毒株的前驱、且变异代数深度最大的那个毒株。

术语说明：
- 前驱株：每个非原始毒株有且仅有一个直接前驱变异株
- 演化关系：X 是 Y 的前驱，当且仅当沿变异链从 Y 可追溯到 X（允许 X 等于 Y）
- 深度：原始毒株深度为 0；任一毒株的深度为从原始毒株突变到该毒株的代数

你可以反复向我提出以下五类查询（每次仅限一个查询），我会根据真实的病毒演化结构如实回答：

1. parent(X)：询问毒株 X 的直接前驱株是谁
2. depth(X)：询问毒株 X 的变异深度（代数）是多少
3. isAncestor(X,Y)：询问 X 是否为 Y 的前驱株（包含自身）
4. compareDepth(X,Y)：询问 X 与 Y 谁更靠近原始毒株
5. jumpUp(X,k)：询问从 X 沿变异链向上回溯 k 代到达哪里（k 为非负整数）

约束条件：
- 禁止直接询问最近共同变异祖先相关问题
- 禁止请求某毒株的衍生突变列表或整个变异树结构
- 查询必须使用有效的毒株标识和合法参数

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询直接前驱株（例如查询 H1 的前驱）：
<query_parent>H1</query_parent>

- 查询变异深度（例如查询 H1 的深度）：
<query_depth>H1</query_depth>

- 查询演化关系（例如查询 H1 是否为 H3 的前驱）：
<query_ancestor>H1,H3</query_ancestor>

- 比较深度（例如比较 H1 和 H2 谁更靠近原始毒株）：
<query_compare_depth>H1,H2</query_compare_depth>

- 向上回溯（例如从 H5 沿变异链回溯 2 代）：
<query_jump>H5,2</query_jump>

提交最终答案时，请使用以下格式：

<answer>H3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Viral Mutation Phylogeny Deduction" game. Here are the rules:

The system has a rooted mutation tree T with {n} viral strains, identified as {nodes}. The phylogeny is connected, acyclic, and has a unique Patient Zero strain {root}.

Public Information:
- Total number of strains: {n}
- All strain identifiers: {nodes}
- Patient Zero strain: {root}
- Two target strains: {target_a} and {target_b}

Hidden Information:
- The edge set of the mutation tree (i.e., all direct mutation events and overall evolutionary topology)

Your goal is to infer the Most Recent Common Ancestor (LCA) strain of {target_a} and {target_b}. The LCA is the common precursor of both strains with the maximum generational depth.

Terminology:
- Precursor strain: Each non-root strain has exactly one direct precursor
- Evolutionary relation: X is an ancestor of Y if and only if Y can trace back to X via the mutation chain (X may equal Y)
- Depth: Patient Zero has depth 0; any strain's depth is the number of mutation generations from Patient Zero

You can repeatedly ask me five types of queries (one query per turn), and I will answer truthfully based on the real phylogeny:

1. parent(X): Ask who is the direct precursor of strain X
2. depth(X): Ask what is the mutation depth (generation) of strain X
3. isAncestor(X,Y): Ask whether X is a precursor of Y (including self)
4. compareDepth(X,Y): Ask which of X and Y is closer to Patient Zero
5. jumpUp(X,k): Ask where you reach by tracing back k generations from X along the mutation chain (k is a non-negative integer)

Constraints:
- Direct queries about the most recent common ancestor are forbidden
- Requesting a strain's descendent list or the entire tree structure is forbidden
- Queries must use valid strain identifiers and legal parameters

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query precursor (e.g., query precursor of H1):
<query_parent>H1</query_parent>

- Query depth (e.g., query depth of H1):
<query_depth>H1</query_depth>

- Query evolutionary relation (e.g., query if H1 is precursor of H3):
<query_ancestor>H1,H3</query_ancestor>

- Compare depth (e.g., compare depth of H1 and H2):
<query_compare_depth>H1,H2</query_compare_depth>

- Trace back (e.g., trace back 2 generations from H5):
<query_jump>H5,2</query_jump>

When submitting the final answer, use this format:

<answer>H3</answer>
"""

    # ================= 场景改造 3：教育 =================
    contextualized_rule_zh_3 = """\
我们来玩一个"学科知识前置依赖树推理"系统，规则如下：

系统设定了一棵有根知识树 T，包含 {n} 个知识点，标识为 {nodes}。依赖结构是连通的、无环的，且存在唯一的基础本源知识点 {root}。

公开信息：
- 知识点总数：{n}
- 所有知识点标识：{nodes}
- 基础本源知识点：{root}
- 两个目标知识点：{target_a} 和 {target_b}

隐藏信息：
- 知识树的边集（即所有直接前置依赖关系和整体学科拓扑）

你的目标是推断出知识点 {target_a} 和 {target_b} 的最深层共同前置知识（LCA）。最深层共同前置知识是指同时是这两个知识点的前置基础、且知识体系深度最大的那个节点。

术语说明：
- 直接前置：每个非本源知识点有且仅有一个最直接的前置依赖知识点
- 依赖关系：X 是 Y 的前置基础，当且仅当沿前置链从 Y 可回溯到 X（允许 X 等于 Y）
- 深度：基础本源节点深度为 0；任一知识点的深度为从本源到该知识点所需的学习进阶步数

你可以反复向我提出以下五类查询（每次仅限一个查询），我会根据真实的学科结构如实回答：

1. parent(X)：询问知识点 X 的直接前置节点是谁
2. depth(X)：询问知识点 X 的体系深度是多少
3. isAncestor(X,Y)：询问 X 是否为 Y 的前置节点（包含自身）
4. compareDepth(X,Y)：询问 X 与 Y 谁更靠近基础本源
5. jumpUp(X,k)：询问从 X 沿前置链向上跳跃 k 步到达哪里（k 为非负整数）

约束条件：
- 禁止直接询问最深层共同前置知识相关问题
- 禁止请求某知识点的后续扩展列表或整体知识树结构
- 查询必须使用有效的知识点标识和合法参数

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询直接前置节点（例如查询 H1 的前置）：
<query_parent>H1</query_parent>

- 查询知识深度（例如查询 H1 的深度）：
<query_depth>H1</query_depth>

- 查询依赖关系（例如查询 H1 是否为 H3 的前置）：
<query_ancestor>H1,H3</query_ancestor>

- 比较深度（例如比较 H1 和 H2 谁更靠近本源）：
<query_compare_depth>H1,H2</query_compare_depth>

- 向上跳跃（例如从 H5 沿前置链向上跳 2 步）：
<query_jump>H5,2</query_jump>

提交最终答案时，请使用以下格式：

<answer>H3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play an "Academic Prerequisite Tree Deduction" game. Here are the rules:

The system defines a rooted knowledge tree T with {n} concepts, identified as {nodes}. The structure is connected, acyclic, and has a unique foundational root concept {root}.

Public Information:
- Total number of concepts: {n}
- All concept identifiers: {nodes}
- Foundational root concept: {root}
- Two target concepts: {target_a} and {target_b}

Hidden Information:
- The edge set of the knowledge tree (i.e., all direct prerequisite dependencies and overall academic topology)

Your goal is to infer the Deepest Common Prerequisite Concept (LCA) of {target_a} and {target_b}. The LCA is the common prerequisite of both concepts with the maximum curriculum depth.

Terminology:
- Direct prerequisite: Each non-root concept has exactly one direct prerequisite concept
- Dependency relation: X is a prerequisite of Y if and only if Y can trace back to X via the prerequisite chain (X may equal Y)
- Depth: The root concept has depth 0; any concept's depth is the number of progression steps from the foundation

You can repeatedly ask me five types of queries (one query per turn), and I will answer truthfully based on the real curriculum:

1. parent(X): Ask who is the direct prerequisite of concept X
2. depth(X): Ask what is the curriculum depth of concept X
3. isAncestor(X,Y): Ask whether X is a prerequisite of Y (including self)
4. compareDepth(X,Y): Ask which of X and Y is closer to the foundational root
5. jumpUp(X,k): Ask where you reach by tracing back k steps from X along the prerequisite chain (k is a non-negative integer)

Constraints:
- Direct queries about the deepest common prerequisite are forbidden
- Requesting a concept's subsequent progression list or the entire tree structure is forbidden
- Queries must use valid concept identifiers and legal parameters

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query direct prerequisite (e.g., query prerequisite of H1):
<query_parent>H1</query_parent>

- Query depth (e.g., query depth of H1):
<query_depth>H1</query_depth>

- Query dependency relation (e.g., query if H1 is prerequisite of H3):
<query_ancestor>H1,H3</query_ancestor>

- Compare depth (e.g., compare depth of H1 and H2):
<query_compare_depth>H1,H2</query_compare_depth>

- Trace back (e.g., trace back 2 steps from H5):
<query_jump>H5,2</query_jump>

When submitting the final answer, use this format:

<answer>H3</answer>
"""

    # ================= 场景改造 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
我们来玩一个"工业产品装配BOM树推理"系统，规则如下：

系统设定了一棵有根装配树 T，包含 {n} 个组件，标识为 {nodes}。装配结构是连通的、无环的，且存在唯一的最终成品 {root}。

公开信息：
- 组件总数：{n}
- 所有组件标识：{nodes}
- 最终成品：{root}
- 两个目标组件：{target_a} 和 {target_b}

隐藏信息：
- 装配树的边集（即所有直接所属关系和整体BOM层级拓扑）

你的目标是推断出组件 {target_a} 和 {target_b} 的最小共同所属总成（LCA）。最小共同所属总成是指同时包含这两个组件、且装配深度最大的那个上级组件。

术语说明：
- 上级总成：每个非成品的组件有且仅有一个直接所属的上级总成
- 包含关系：X 包含 Y，当且仅当沿装配链从 Y 可追溯到 X（允许 X 等于 Y）
- 深度：最终成品深度为 0；任一组件的深度为从最终成品拆解到该组件的装配级数

你可以反复向我提出以下五类查询（每次仅限一个查询），我会根据真实的BOM结构如实回答：

1. parent(X)：询问组件 X 的直接所属上级组件是谁
2. depth(X)：询问组件 X 的装配级数（深度）是多少
3. isAncestor(X,Y)：询问 X 是否包含 Y（包含自身）
4. compareDepth(X,Y)：询问 X 与 Y 谁更靠近最终成品
5. jumpUp(X,k)：询问从 X 沿装配链向上追溯 k 级到达哪里（k 为非负整数）

约束条件：
- 禁止直接询问最小共同所属总成相关问题
- 禁止请求某总成的子零件列表或整个BOM结构
- 查询必须使用有效的组件标识和合法参数

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询直接所属上级（例如查询 H1 的上级总成）：
<query_parent>H1</query_parent>

- 查询装配深度（例如查询 H1 的深度）：
<query_depth>H1</query_depth>

- 查询包含关系（例如查询 H1 是否包含 H3）：
<query_ancestor>H1,H3</query_ancestor>

- 比较深度（例如比较 H1 和 H2 谁更靠近最终成品）：
<query_compare_depth>H1,H2</query_compare_depth>

- 向上追溯（例如从 H5 沿装配链追溯 2 级）：
<query_jump>H5,2</query_jump>

提交最终答案时，请使用以下格式：

<answer>H3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Industrial Assembly BOM Tree Deduction" game. Here are the rules:

The system has a rooted assembly tree T with {n} components, identified as {nodes}. The BOM is connected, acyclic, and has a unique final product {root}.

Public Information:
- Total number of components: {n}
- All component identifiers: {nodes}
- Final product: {root}
- Two target components: {target_a} and {target_b}

Hidden Information:
- The edge set of the assembly tree (i.e., all parent-assembly relationships and overall BOM topology)

Your goal is to infer the Lowest Common Sub-assembly (LCA) of components {target_a} and {target_b}. The LCA is the common assembly containing both components with the maximum assembly depth.

Terminology:
- Parent assembly: Each non-final component belongs directly to exactly one parent sub-assembly
- Containment relation: X contains Y if and only if Y can trace back to X via the assembly chain (X may equal Y)
- Depth: The final product has depth 0; any component's depth is the number of breakdown levels from the final product

You can repeatedly ask me five types of queries (one query per turn), and I will answer truthfully based on the real BOM structure:

1. parent(X): Ask who is the direct parent assembly of component X
2. depth(X): Ask what is the assembly depth of component X
3. isAncestor(X,Y): Ask whether X contains component Y (including self)
4. compareDepth(X,Y): Ask which of X and Y is closer to the final product
5. jumpUp(X,k): Ask where you reach by tracing back k levels from X along the assembly chain (k is a non-negative integer)

Constraints:
- Direct queries about the lowest common sub-assembly are forbidden
- Requesting an assembly's parts list or the entire BOM structure is forbidden
- Queries must use valid component identifiers and legal parameters

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query parent assembly (e.g., query parent of H1):
<query_parent>H1</query_parent>

- Query depth (e.g., query depth of H1):
<query_depth>H1</query_depth>

- Query containment relation (e.g., query if H1 contains H3):
<query_ancestor>H1,H3</query_ancestor>

- Compare depth (e.g., compare depth of H1 and H2):
<query_compare_depth>H1,H2</query_compare_depth>

- Trace back (e.g., trace back 2 levels from H5):
<query_jump>H5,2</query_jump>

When submitting the final answer, use this format:

<answer>H3</answer>
"""

    # ================= 场景改造 5：法律 =================
    contextualized_rule_zh_5 = """\
我们来玩一个"跨国企业股权穿透推理"系统，规则如下：

系统设定了一棵有根股权树 T，包含 {n} 个公司实体，标识为 {nodes}。控股结构是连通的、无环的，且存在唯一的绝对控股母公司 {root}。

公开信息：
- 实体总数：{n}
- 所有实体标识：{nodes}
- 绝对控股母公司：{root}
- 两个目标实体：{target_a} 和 {target_b}

隐藏信息：
- 股权树的边集（即所有直接控股关系和整体公司架构拓扑）

你的目标是推断出实体 {target_a} 和 {target_b} 的最底层共同控股母公司（LCA）。最底层共同控股是指同时控股这两个实体、且处在股权结构中最深层级的母公司。

术语说明：
- 控股母公司：每个非根实体有且仅有一个直接控股母公司
- 控股关系：X 是 Y 的控股上级，当且仅当沿控股链从 Y 可穿透到 X（允许 X 等于 Y）
- 深度：绝对控股母公司深度为 0；任一实体的深度为从最高母公司到该实体穿透的层级数

你可以反复向我提出以下五类查询（每次仅限一个查询），我会根据真实的股权架构如实回答：

1. parent(X)：询问实体 X 的直接控股母公司是谁
2. depth(X)：询问实体 X 的股权层级深度是多少
3. isAncestor(X,Y)：询问 X 是否为 Y 的控股上级（包含自身）
4. compareDepth(X,Y)：询问 X 与 Y 谁更靠近绝对控股母公司
5. jumpUp(X,k)：询问从 X 沿股权链向上穿透 k 层到达哪里（k 为非负整数）

约束条件：
- 禁止直接询问共同控股母公司相关问题
- 禁止请求某公司的子公司列表或整体股权架构
- 查询必须使用有效的实体标识和合法参数

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询直接控股母公司（例如查询 H1 的母公司）：
<query_parent>H1</query_parent>

- 查询股权深度（例如查询 H1 的深度）：
<query_depth>H1</query_depth>

- 查询控股关系（例如查询 H1 是否为 H3 的控股上级）：
<query_ancestor>H1,H3</query_ancestor>

- 比较深度（例如比较 H1 和 H2 谁更靠近绝对母公司）：
<query_compare_depth>H1,H2</query_compare_depth>

- 向上穿透（例如从 H5 沿股权链穿透 2 层）：
<query_jump>H5,2</query_jump>

提交最终答案时，请使用以下格式：

<answer>H3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Corporate Ownership Penetration Deduction" game. Here are the rules:

The system defines a rooted corporate tree T with {n} entities, identified as {nodes}. The ownership is connected, acyclic, and has a unique ultimate parent holding company {root}.

Public Information:
- Total number of entities: {n}
- All entity identifiers: {nodes}
- Ultimate parent holding company: {root}
- Two target entities: {target_a} and {target_b}

Hidden Information:
- The edge set of the corporate tree (i.e., all direct holding relationships and overall corporate architecture)

Your goal is to infer the Lowest Common Holding Company (LCA) of entities {target_a} and {target_b}. The LCA is the common holding company of both entities with the maximum ownership depth.

Terminology:
- Holding company: Each non-root entity has exactly one direct holding parent company
- Holding relation: X is a superior holding of Y if and only if Y can penetrate back to X via the ownership chain (X may equal Y)
- Depth: The ultimate parent company has depth 0; any entity's depth is the number of penetration layers from the ultimate parent

You can repeatedly ask me five types of queries (one query per turn), and I will answer truthfully based on the real corporate architecture:

1. parent(X): Ask who is the direct holding company of entity X
2. depth(X): Ask what is the ownership depth of entity X
3. isAncestor(X,Y): Ask whether X is a holding superior of Y (including self)
4. compareDepth(X,Y): Ask which of X and Y is closer to the ultimate parent company
5. jumpUp(X,k): Ask where you reach by penetrating up k layers from X along the ownership chain (k is a non-negative integer)

Constraints:
- Direct queries about the lowest common holding company are forbidden
- Requesting an entity's subsidiary list or the entire corporate structure is forbidden
- Queries must use valid entity identifiers and legal parameters

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Query holding company (e.g., query parent of H1):
<query_parent>H1</query_parent>

- Query depth (e.g., query depth of H1):
<query_depth>H1</query_depth>

- Query holding relation (e.g., query if H1 is superior of H3):
<query_ancestor>H1,H3</query_ancestor>

- Compare depth (e.g., compare depth of H1 and H2):
<query_compare_depth>H1,H2</query_compare_depth>

- Penetrate up (e.g., penetrate up 2 layers from H5):
<query_jump>H5,2</query_jump>

When submitting the final answer, use this format:

<answer>H3</answer>
"""

    tags = ["answer", "query_parent", "query_depth", "query_ancestor", "query_compare_depth", "query_jump"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "nodes": "H1, H2, H3, H4, H5",
                "root": "H1",
                "target_a": "H4",
                "target_b": "H5",
                "edges": [
                    ("H1", "H2"),
                    ("H2", "H3"),
                    ("H3", "H4"),
                    ("H2", "H5"),
                ],
                "lca": "H2",
            },
            2: {
                "n": 7,
                "nodes": "H1, H2, H3, H4, H5, H6, H7",
                "root": "H1",
                "target_a": "H4",
                "target_b": "H5",
                "edges": [
                    ("H1", "H2"),
                    ("H1", "H3"),
                    ("H2", "H4"),
                    ("H2", "H5"),
                    ("H3", "H6"),
                    ("H3", "H7"),
                ],
                "lca": "H2",
            },
            3: {
                "n": 10,
                "nodes": "H1, H2, H3, H4, H5, H6, H7, H8, H9, H10",
                "root": "H1",
                "target_a": "H8",
                "target_b": "H10",
                "edges": [
                    ("H1", "H2"),
                    ("H1", "H3"),
                    ("H2", "H4"),
                    ("H2", "H5"),
                    ("H3", "H6"),
                    ("H4", "H7"),
                    ("H5", "H8"),
                    ("H5", "H9"),
                    ("H6", "H10"),
                ],
                "lca": "H1",
            },
            4: {
                "n": 12,
                "nodes": "H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12",
                "root": "H1",
                "target_a": "H9",
                "target_b": "H12",
                "edges": [
                    ("H1", "H2"),
                    ("H1", "H3"),
                    ("H2", "H4"),
                    ("H2", "H5"),
                    ("H3", "H6"),
                    ("H4", "H7"),
                    ("H5", "H8"),
                    ("H5", "H9"),
                    ("H6", "H10"),
                    ("H6", "H11"),
                    ("H11", "H12"),
                ],
                "lca": "H1",
            },
            5: {
                "n": 15,
                "nodes": "H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13, H14, H15",
                "root": "H1",
                "target_a": "H13",
                "target_b": "H15",
                "edges": [
                    ("H1", "H2"),
                    ("H1", "H3"),
                    ("H2", "H4"),
                    ("H2", "H5"),
                    ("H3", "H6"),
                    ("H4", "H7"),
                    ("H5", "H8"),
                    ("H5", "H9"),
                    ("H6", "H10"),
                    ("H6", "H11"),
                    ("H7", "H12"),
                    ("H9", "H13"),
                    ("H12", "H14"),
                    ("H13", "H15"),
                ],
                "lca": "H13",
            },
        },
        "en": {
            1: {
                "n": 5,
                "nodes": "H1, H2, H3, H4, H5",
                "root": "H1",
                "target_a": "H4",
                "target_b": "H5",
                "edges": [
                    ("H1", "H2"),
                    ("H2", "H3"),
                    ("H3", "H4"),
                    ("H2", "H5"),
                ],
                "lca": "H2",
            },
            2: {
                "n": 7,
                "nodes": "H1, H2, H3, H4, H5, H6, H7",
                "root": "H1",
                "target_a": "H4",
                "target_b": "H5",
                "edges": [
                    ("H1", "H2"),
                    ("H1", "H3"),
                    ("H2", "H4"),
                    ("H2", "H5"),
                    ("H3", "H6"),
                    ("H3", "H7"),
                ],
                "lca": "H2",
            },
            3: {
                "n": 10,
                "nodes": "H1, H2, H3, H4, H5, H6, H7, H8, H9, H10",
                "root": "H1",
                "target_a": "H8",
                "target_b": "H10",
                "edges": [
                    ("H1", "H2"),
                    ("H1", "H3"),
                    ("H2", "H4"),
                    ("H2", "H5"),
                    ("H3", "H6"),
                    ("H4", "H7"),
                    ("H5", "H8"),
                    ("H5", "H9"),
                    ("H6", "H10"),
                ],
                "lca": "H1",
            },
            4: {
                "n": 12,
                "nodes": "H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12",
                "root": "H1",
                "target_a": "H9",
                "target_b": "H12",
                "edges": [
                    ("H1", "H2"),
                    ("H1", "H3"),
                    ("H2", "H4"),
                    ("H2", "H5"),
                    ("H3", "H6"),
                    ("H4", "H7"),
                    ("H5", "H8"),
                    ("H5", "H9"),
                    ("H6", "H10"),
                    ("H6", "H11"),
                    ("H11", "H12"),
                ],
                "lca": "H1",
            },
            5: {
                "n": 15,
                "nodes": "H1, H2, H3, H4, H5, H6, H7, H8, H9, H10, H11, H12, H13, H14, H15",
                "root": "H1",
                "target_a": "H13",
                "target_b": "H15",
                "edges": [
                    ("H1", "H2"),
                    ("H1", "H3"),
                    ("H2", "H4"),
                    ("H2", "H5"),
                    ("H3", "H6"),
                    ("H4", "H7"),
                    ("H5", "H8"),
                    ("H5", "H9"),
                    ("H6", "H10"),
                    ("H6", "H11"),
                    ("H7", "H12"),
                    ("H9", "H13"),
                    ("H12", "H14"),
                    ("H13", "H15"),
                ],
                "lca": "H13",
            },
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
        
        # 设置游戏信息
        self._game_info["n"] = cfg["n"]
        self._game_info["nodes"] = cfg["nodes"]
        self._game_info["root"] = cfg["root"]
        self._game_info["target_a"] = cfg["target_a"]
        self._game_info["target_b"] = cfg["target_b"]
        
        # 构建树结构
        self.root = cfg["root"]
        self.target_a = cfg["target_a"]
        self.target_b = cfg["target_b"]
        self.lca = cfg["lca"]
        
        # 从边集构建父子关系映射
        self.parent_map = {self.root: None}  # 根节点无父节点
        self.children_map = {}  # 用于内部验证，不对外暴露
        
        for parent, child in cfg["edges"]:
            self.parent_map[child] = parent
            if parent not in self.children_map:
                self.children_map[parent] = []
            self.children_map[parent].append(child)
        
        # 预计算所有节点的深度
        self.depth_map = {}
        self._compute_depths(self.root, 0)
        
        # 预计算祖先关系（用于快速查询）
        self.ancestors_map = {}
        for node in self.parent_map:
            self.ancestors_map[node] = self._get_ancestors(node)

    def _compute_depths(self, node, depth):
        """递归计算所有节点的深度"""
        self.depth_map[node] = depth
        if node in self.children_map:
            for child in self.children_map[node]:
                self._compute_depths(child, depth + 1)

    def _get_ancestors(self, node):
        """获取某节点的所有祖先（包括自身）"""
        ancestors = set()
        current = node
        while current is not None:
            ancestors.add(current)
            current = self.parent_map.get(current)
        return ancestors

    def _jump_up(self, node, k):
        """从节点 node 向上跳 k 步"""
        current = node
        for _ in range(k):
            if current is None:
                return None
            current = self.parent_map.get(current)
        return current

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        answer = parsed_info["answer"].strip()
        return answer == self.lca

    def _cf_make_wrong(self, correct: str) -> str:
        """
        给定正确的查询结果字符串，生成一个错误的查询结果。
        策略：对于不同类型的返回，进行合理的篡改。
        """
        import re as _re

        # 如果正确答案是 Yes/No 或 是/否，直接取反
        if correct in ("Yes", "No"):
            return "No" if correct == "Yes" else "Yes"
        if correct in ("是", "否"):
            return "否" if correct == "是" else "是"
        
        # 如果包含节点名（如 "Parent of H3 is H2"），尝试替换成其他节点
        nodes = list(self.parent_map.keys())
        # 按名称长度降序排列，优先匹配长名称，避免 H1 匹配 H10 的前缀
        nodes_sorted = sorted(nodes, key=len, reverse=True)
        
        # 尝试找到答案中出现的完整节点名，使用单词边界匹配
        for node in nodes_sorted:
            # 使用单词边界确保精确匹配
            pattern = _re.compile(r'\b' + _re.escape(node) + r'\b')
            if pattern.search(correct):
                candidates = [n for n in nodes if n != node]
                if candidates:
                    wrong = pattern.sub(random.choice(candidates), correct, count=1)
                    if wrong != correct:
                        return wrong
        
        # 如果包含数字（如深度），修改数字
        numbers = _re.findall(r'\d+', correct)
        if numbers:
            num = int(numbers[0])
            wrong_num = num + 1
            return correct.replace(str(num), str(wrong_num), 1)
        
        # 兜底：在结果后附加错误标记
        return correct + " [WRONG]"

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            closer_msg = "{} 更靠近根"
            same_depth_msg = "二者深度相同"
            parent_msg = "{} 的父节点是 {}"
            root_msg = "{} 是根节点（无父节点）"
            depth_msg = "{} 的深度是 {}"
            jump_msg = "从 {node} 向上跳 {k} 步到达 {result}"
            jump_over_msg = "越过根节点（不存在该节点）"
            invalid_node_msg = "错误：节点 {} 不存在"
            invalid_format_msg = "错误：格式无效"
            invalid_param_msg = "错误：参数无效"
        else:
            yes_res, no_res = "Yes", "No"
            closer_msg = "{} is closer to root"
            same_depth_msg = "Both have the same depth"
            parent_msg = "Parent of {} is {}"
            root_msg = "{} is the root (no parent)"
            depth_msg = "Depth of {} is {}"
            jump_msg = "Jumping up {k} steps from {node} reaches {result}"
            jump_over_msg = "Over root (node does not exist)"
            invalid_node_msg = "Error: Node {} does not exist"
            invalid_format_msg = "Error: Invalid format"
            invalid_param_msg = "Error: Invalid parameter"

        # 优先级处理各类查询
        if "query_parent" in parsed_info:
            node = parsed_info["query_parent"].strip()
            if node not in self.parent_map:
                return invalid_node_msg.format(node)
            if node == self.root:
                return root_msg.format(node)
            return parent_msg.format(node, self.parent_map[node])

        elif "query_depth" in parsed_info:
            node = parsed_info["query_depth"].strip()
            if node not in self.depth_map:
                return invalid_node_msg.format(node)
            return depth_msg.format(node, self.depth_map[node])

        elif "query_ancestor" in parsed_info:
            try:
                raw = parsed_info["query_ancestor"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_format_msg
                x, y = parts
                if x not in self.ancestors_map or y not in self.ancestors_map:
                    return invalid_node_msg.format(x if x not in self.ancestors_map else y)
                # x 是 y 的祖先？
                return yes_res if x in self.ancestors_map[y] else no_res
            except Exception:
                return invalid_format_msg

        elif "query_compare_depth" in parsed_info:
            try:
                raw = parsed_info["query_compare_depth"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_format_msg
                x, y = parts
                if x not in self.depth_map or y not in self.depth_map:
                    return invalid_node_msg.format(x if x not in self.depth_map else y)
                dx, dy = self.depth_map[x], self.depth_map[y]
                if dx < dy:
                    return closer_msg.format(x)
                elif dx > dy:
                    return closer_msg.format(y)
                else:
                    return same_depth_msg
            except Exception:
                return invalid_format_msg

        elif "query_jump" in parsed_info:
            try:
                raw = parsed_info["query_jump"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_format_msg
                node, k_str = parts
                k = int(k_str)
                if k < 0:
                    return invalid_param_msg
                if node not in self.parent_map:
                    return invalid_node_msg.format(node)
                result = self._jump_up(node, k)
                if result is None:
                    return jump_over_msg
                return jump_msg.format(node=node, k=k, result=result)
            except ValueError:
                return invalid_param_msg
            except Exception:
                return invalid_format_msg

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        nodes = list(self.parent_map.keys())

        # 辅助函数：构造查询并获取答案（直接调用核心逻辑，避开反事实干扰）
        def add_query(tag, content, parsed_payload):
            xml_query = f"<{tag}>{content}</{tag}>"
            answer = self._cf_core_produce(parsed_payload)
            queries.append({
                "query": xml_query,
                "answer": answer
            })

        # 1. 查询父节点
        for node in nodes:
            add_query("query_parent", node, {"query_parent": node})

        # 2. 查询深度
        for node in nodes:
            add_query("query_depth", node, {"query_depth": node})

        # 3. 查询祖先关系 (枚举所有节点对)
        for x in nodes:
            for y in nodes:
                content = f"{x},{y}"
                add_query("query_ancestor", content, {"query_ancestor": content})

        # 4. 比较深度 (枚举所有节点对)
        for x in nodes:
            for y in nodes:
                content = f"{x},{y}"
                add_query("query_compare_depth", content, {"query_compare_depth": content})

        # 5. 向上跳跃
        # 范围：从 0 到 节点深度+1 (深度+1 必定触发“越过根节点”，覆盖所有情况)
        for node in nodes:
            limit = self.depth_map[node] + 2
            for k in range(limit):
                content = f"{node},{k}"
                add_query("query_jump", content, {"query_jump": content})

        return queries