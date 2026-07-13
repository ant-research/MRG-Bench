# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   父节点：某给定节点的父节点是哪个
# ============================================================

from .base import Game
import random


class TreeParentFindingGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树中父节点推理"的游戏，规则如下：

游戏设定了一棵有根树，共有 {n} 个节点，每个节点有唯一的名字。树的根节点是 {root}，其深度为 0。你的目标节点是 {target}（保证不是根节点）。

你的任务是：仅通过指定的查询接口，唯一确定目标节点 {target} 的父节点是谁。

## 术语说明

- 深度：从根节点到某节点的边数（根节点深度为 0）
- 严格祖先：节点 a 是节点 b 的严格祖先，意味着 a 位于从根到 b 的唯一路径上且 a 不等于 b
- 最近公共祖先：节点 a 和 b 的最近公共祖先；当 a 等于 b 时，返回 a 本身

## 可用查询

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 深度查询：询问某个节点的深度。我会返回一个非负整数。
2. 祖先判断：询问节点 a 是否是节点 b 的严格祖先。我会回答"是"或"否"（当 a 等于 b 时必为"否"）。
3. 最近公共祖先查询：询问节点 a 和 b 的最近公共祖先。我会返回一个节点名字（当 a 等于 b 时返回 a）。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 深度查询（例如查询节点 A 的深度）：
<query_depth>A</query_depth>

- 祖先判断（例如询问 A 是否是 B 的严格祖先）：
<query_ancestor>A,B</query_ancestor>

- 最近公共祖先查询（例如查询 A 和 B 的最近公共祖先）：
<query_lca>A,B</query_lca>

## 提交答案格式

当你确定了目标节点的父节点后，请使用以下格式提交答案：

<answer>X</answer>

其中 X 是你推断出的 {target} 的父节点名字。

## 注意事项

- 树的所有节点名字为：{nodes}
- 请尽可能少地使用查询次数来确定答案
- 答案错误游戏失败
"""

    game_rule_en = """\
Let's play a "Tree Parent Finding" game. Here are the rules:

There is a rooted tree with {n} nodes, each having a unique name. The root node is {root} with depth 0. Your target node is {target} (guaranteed not to be the root).

Your task is: using only the specified query interface, uniquely determine the parent node of the target node {target}.

## Terminology

- Depth: The number of edges from the root to a node (root has depth 0)
- Strict Ancestor: Node a is a strict ancestor of node b if a is on the unique path from root to b and a is not equal to b
- Lowest Common Ancestor (LCA): The deepest common ancestor of nodes a and b; when a equals b, returns a itself

## Available Queries

You can repeatedly make the following three types of queries (one query per turn):

1. Depth Query: Ask for the depth of a node. I will return a non-negative integer.
2. Ancestor Query: Ask whether node a is a strict ancestor of node b. I will answer "Yes" or "No" (always "No" when a equals b).
3. LCA Query: Ask for the lowest common ancestor of nodes a and b. I will return a node name (returns a when a equals b).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Depth Query (e.g., querying depth of node A):
<query_depth>A</query_depth>

- Ancestor Query (e.g., asking if A is a strict ancestor of B):
<query_ancestor>A,B</query_ancestor>

- LCA Query (e.g., querying LCA of A and B):
<query_lca>A,B</query_lca>

## Answer Submission Format

When you have determined the parent node of the target, submit your answer using:

<answer>X</answer>

where X is the parent node name you inferred for {target}.

## Notes

- All node names in the tree: {nodes}
- Try to use as few queries as possible to determine the answer
- Incorrect answer results in game failure
"""

    contextualized_rule_zh_1 = """\
欢迎使用“物流枢纽溯源系统”。本系统记录了一个呈树状辐射分布的物流网络。

网络共有 {n} 个节点，每个节点有唯一的名字。总枢纽是 {root}，其中转级数为 0。你的目标节点是 {target}（保证不是总枢纽）。

你的任务是：仅通过指定的查询接口，唯一确定目标站点 {target} 的直接上级分拨中心是谁。

## 术语说明

- 中转级数：从总枢纽到某站点的路径长度（总枢纽级数为 0）
- 上游路由：站点 a 是站点 b 的上游路由，意味着 a 位于从总枢纽到 b 的唯一路径上且 a 不等于 b
- 最近公共枢纽：站点 a 和 b 的最近共同上游中转枢纽；当 a 等于 b 时，返回 a 本身

## 可用查询

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 中转级数查询：询问某个站点的中转级数。我会返回一个非负整数。
2. 上游路由判断：询问站点 a 是否是站点 b 的上游路由。我会回答"是"或"否"（当 a 等于 b 时必为"否"）。
3. 最近公共枢纽查询：询问站点 a 和 b 的最近公共枢纽。我会返回一个节点名字（当 a 等于 b 时返回 a）。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 中转级数查询（例如查询站点 A 的级数）：
<query_depth>A</query_depth>

- 上游路由判断（例如询问 A 是否是 B 的上游路由）：
<query_ancestor>A,B</query_ancestor>

- 最近公共枢纽查询（例如查询 A 和 B 的最近公共枢纽）：
<query_lca>A,B</query_lca>

## 提交答案格式

当你确定了目标站点的直接上级分拨中心后，请使用以下格式提交答案：

<answer>X</answer>

其中 X 是你推断出的 {target} 的上级分拨中心名字。

## 注意事项

- 网络的所有节点名字为：{nodes}
- 请尽可能少地使用查询次数来确定答案
- 答案错误将导致溯源失败
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Logistics Hub Tracing System". The system records a tree-like logistics network.

The network consists of {n} nodes, each with a unique name. The main hub is {root}, with a transfer level of 0. Your target node is {target} (guaranteed not to be the main hub).

Your task is: uniquely determine the direct upstream distribution center of the target station {target} using only the specified query interfaces.

## Terminology

- Transfer Level: The number of connections from the main hub to a station (main hub level is 0)
- Upstream Route: Station a is an upstream route of station b if a is on the unique path from the main hub to b, and a is not equal to b
- Lowest Common Hub: The closest common upstream hub of stations a and b; when a equals b, returns a itself

## Available Queries

You can repeatedly make the following three types of queries (one query per turn):

1. Transfer Level Query: Ask for the transfer level of a station. I will return a non-negative integer.
2. Upstream Route Query: Ask whether station a is an upstream route of station b. I will answer "Yes" or "No" (always "No" when a equals b).
3. Lowest Common Hub Query: Ask for the lowest common hub of stations a and b. I will return a node name (returns a when a equals b).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Transfer Level Query (e.g., querying level of station A):
<query_depth>A</query_depth>

- Upstream Route Query (e.g., asking if A is an upstream route of B):
<query_ancestor>A,B</query_ancestor>

- Lowest Common Hub Query (e.g., querying lowest common hub of A and B):
<query_lca>A,B</query_lca>

## Answer Submission Format

When you have determined the direct upstream distribution center of the target, submit your answer using:

<answer>X</answer>

where X is the upstream distribution center name you inferred for {target}.

## Notes

- All node names in the network: {nodes}
- Try to use as few queries as possible to determine the answer
- Incorrect answer results in tracing failure
"""

    contextualized_rule_zh_2 = """\
欢迎使用“病毒变异溯源系统”。系统中有一棵包含 {n} 个毒株节点的变异进化树。

每个毒株具有唯一代号。原始毒株是 {root}（变异代数为 0）。你的目标毒株是 {target}（保证非原始毒株）。

你的任务是：仅通过系统接口，唯一确定目标毒株 {target} 的直接变异母体（父节点）。

## 术语说明

- 变异代数：从原始毒株到某毒株的变异次数（原始毒株代数为 0）
- 进化路径：毒株 a 位于毒株 b 的进化路径上，意味着 a 位于从原始毒株到 b 的唯一进化链上且 a 不等于 b
- 最近公共变异源：毒株 a 和 b 的最近共同变异源头毒株；当 a 等于 b 时，返回 a 本身

## 可用查询

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 变异代数查询：询问某毒株的变异代数。我会返回一个非负整数。
2. 进化路径判断：询问毒株 a 是否在毒株 b 的直接变异前置路径上。我会回答"是"或"否"（当 a 等于 b 时必为"否"）。
3. 最近公共变异源查询：询问毒株 a 和 b 的最近公共变异源头。我会返回一个毒株代号（当 a 等于 b 时返回 a）。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 变异代数查询（例如查询毒株 A 的代数）：
<query_depth>A</query_depth>

- 进化路径判断（例如询问毒株 A 是否在毒株 B 的前置路径上）：
<query_ancestor>A,B</query_ancestor>

- 最近公共变异源查询（例如查询毒株 A 和 B 的共同源头）：
<query_lca>A,B</query_lca>

## 提交答案格式

当你确定了目标毒株的直接变异母体后，请使用以下格式提交答案：

<answer>X</answer>

其中 X 是你推断出的 {target} 的变异母体代号。

## 注意事项

- 系统收录的毒株代号为：{nodes}
- 请尽可能少地使用查询次数来确定答案
- 答案错误将导致溯源失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Virus Mutation Tracing System". The system contains an evolutionary tree with {n} strain nodes.

Each strain has a unique name. The original strain is {root} (mutation generation 0). Your target strain is {target} (guaranteed not to be the original strain).

Your task is: uniquely determine the direct parent strain from which {target} mutated, using only the specified query interfaces.

## Terminology

- Mutation Generation: The number of mutations from the original strain to a strain (original has generation 0)
- Evolutionary Path: Strain a is on the evolutionary path of strain b if a is on the unique lineage from the original strain to b, and a is not equal to b
- Lowest Common Ancestor Strain: The closest common parent strain of a and b; when a equals b, returns a itself

## Available Queries

You can repeatedly make the following three types of queries (one query per turn):

1. Mutation Generation Query: Ask for the mutation generation of a strain. I will return a non-negative integer.
2. Evolutionary Path Query: Ask whether strain a is on the strict evolutionary path of strain b. I will answer "Yes" or "No" (always "No" when a equals b).
3. LCA Strain Query: Ask for the lowest common ancestor strain of a and b. I will return a strain name (returns a when a equals b).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Mutation Generation Query (e.g., querying generation of strain A):
<query_depth>A</query_depth>

- Evolutionary Path Query (e.g., asking if A is on the path of B):
<query_ancestor>A,B</query_ancestor>

- LCA Strain Query (e.g., querying LCA strain of A and B):
<query_lca>A,B</query_lca>

## Answer Submission Format

When you have determined the direct parent strain of the target, submit your answer using:

<answer>X</answer>

where X is the parent strain name you inferred for {target}.

## Notes

- All strain names in the tree: {nodes}
- Try to use as few queries as possible to determine the answer
- Incorrect answer results in tracing failure
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学科知识点层级系统”。这里有一棵包含 {n} 个知识点的先修关系树。

每个知识点有唯一的名称。根知识领域为 {root}（层级深度为 0）。你需要追踪的知识点是 {target}（保证非根领域）。

你的任务是：仅通过指定查询，唯一确定知识点 {target} 的直接前置父级知识点。

## 术语说明

- 知识层级：从根领域到某知识点的细分层级数（根领域为 0）
- 宏观前置领域：知识点 a 是知识点 b 的宏观前置领域，意味着 a 位于从根领域到 b 的唯一学习路径上且 a 不等于 b
- 最近公共领域：知识点 a 和 b 共同从属的最底层的宏观知识领域；当 a 等于 b 时，返回 a 本身

## 可用查询

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 知识层级查询：询问某知识点的细分层级。我会返回一个非负整数。
2. 宏观领域判断：询问知识点 a 是否是涵盖 b 的宏观前置领域。我会回答"是"或"否"（当 a 等于 b 时必为"否"）。
3. 最近公共领域查询：询问知识点 a 和 b 共同从属的最近公共领域。我会返回一个领域名称（当 a 等于 b 时返回 a）。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 知识层级查询（例如查询知识点 A 的层级）：
<query_depth>A</query_depth>

- 宏观领域判断（例如询问 A 是否是 B 的前置领域）：
<query_ancestor>A,B</query_ancestor>

- 最近公共领域查询（例如查询 A 和 B 的最近公共领域）：
<query_lca>A,B</query_lca>

## 提交答案格式

当你确定了目标知识点的直接父级知识点后，请使用以下格式提交答案：

<answer>X</answer>

其中 X 是你推断出的 {target} 的直接前置知识点名称。

## 注意事项

- 图谱中的所有知识点名称为：{nodes}
- 请尽可能少地使用查询次数来确定答案
- 答案错误将导致分析失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Disciplinary Knowledge Hierarchy System". There is a prerequisite tree with {n} knowledge nodes.

Each node has a unique name. The root domain is {root} (hierarchy depth 0). Your target knowledge node is {target} (guaranteed not to be the root).

Your task is: uniquely determine the direct prerequisite parent node of {target} using only the specified queries.

## Terminology

- Knowledge Hierarchy Depth: The number of subdivision levels from the root domain to a node (root has depth 0)
- Macro Prerequisite Domain: Node a is a macro prerequisite domain of node b if a is on the unique learning path from the root to b, and a is not equal to b
- Lowest Common Domain: The deepest common macro domain of nodes a and b; when a equals b, returns a itself

## Available Queries

You can repeatedly make the following three types of queries (one query per turn):

1. Hierarchy Depth Query: Ask for the subdivision depth of a node. I will return a non-negative integer.
2. Macro Domain Query: Ask whether node a is a strict macro prerequisite domain of node b. I will answer "Yes" or "No" (always "No" when a equals b).
3. Lowest Common Domain Query: Ask for the deepest common macro domain of nodes a and b. I will return a node name (returns a when a equals b).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Hierarchy Depth Query (e.g., querying depth of node A):
<query_depth>A</query_depth>

- Macro Domain Query (e.g., asking if A is a macro domain of B):
<query_ancestor>A,B</query_ancestor>

- Lowest Common Domain Query (e.g., querying common domain of A and B):
<query_lca>A,B</query_lca>

## Answer Submission Format

When you have determined the direct prerequisite parent node of the target, submit your answer using:

<answer>X</answer>

where X is the parent node name you inferred for {target}.

## Notes

- All knowledge node names: {nodes}
- Try to use as few queries as possible to determine the answer
- Incorrect answer results in system failure
"""

    contextualized_rule_zh_4 = """\
欢迎使用“设备装配BOM分析系统”。此设备是一棵包含 {n} 个组件节点的装配树。

每个组件有唯一的编号。整机总成是 {root}（装配层级为 0）。你的目标组件是 {target}（保证不是整机）。

你的任务是：仅通过调用系统接口，唯一确定零部件 {target} 直接隶属的上一级组件是谁。

## 术语说明

- 装配层级：从整机总成到某组件的拆解级数（整机总成为 0）
- 上层总成：组件 a 是组件 b 的上层总成，意味着 a 位于从整机到 b 的唯一装配链条上且 a 不等于 b
- 最近公共总成：组件 a 和 b 共同隶属的最小上层装配总成；当 a 等于 b 时，返回 a 本身

## 可用查询

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 装配层级查询：询问某组件的装配层级深度。我会返回一个非负整数。
2. 包含关系判断：询问组件 a 是否是包含子件 b 的严格上层总成。我会回答"是"或"否"（当 a 等于 b 时必为"否"）。
3. 最近公共总成查询：询问组件 a 和 b 共同隶属的最近公共总成。我会返回一个组件编号（当 a 等于 b 时返回 a）。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 装配层级查询（例如查询组件 A 的层级）：
<query_depth>A</query_depth>

- 包含关系判断（例如询问组件 A 是否是组件 B 的上层总成）：
<query_ancestor>A,B</query_ancestor>

- 最近公共总成查询（例如查询组件 A 和 B 的最小公共总成）：
<query_lca>A,B</query_lca>

## 提交答案格式

当你确定了目标组件的上一级组件后，请使用以下格式提交答案：

<answer>X</answer>

其中 X 是你推断出的 {target} 的上一级组件编号。

## 注意事项

- BOM 表中的所有组件编号为：{nodes}
- 请尽可能少地使用查询次数来确定答案
- 答案错误将导致溯源失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Equipment BOM Analysis System". The equipment represents an assembly tree with {n} component nodes.

Each component has a unique ID. The main assembly is {root} (assembly level 0). Your target component is {target} (guaranteed not to be the main assembly).

Your task is: uniquely determine the direct parent assembly to which component {target} belongs, using only the specified queries.

## Terminology

- Assembly Level: The number of disassembly steps from the main assembly to a component (main assembly is 0)
- Parent Assembly: Component a is a parent assembly of component b if a is on the unique assembly chain from the main assembly to b, and a is not equal to b
- Lowest Common Assembly: The smallest common parent assembly of a and b; when a equals b, returns a itself

## Available Queries

You can repeatedly make the following three types of queries (one query per turn):

1. Assembly Level Query: Ask for the assembly depth level of a component. I will return a non-negative integer.
2. Parent Assembly Query: Ask whether component a is a strict parent assembly of component b. I will answer "Yes" or "No" (always "No" when a equals b).
3. Lowest Common Assembly Query: Ask for the smallest common assembly of components a and b. I will return a component ID (returns a when a equals b).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Assembly Level Query (e.g., querying level of component A):
<query_depth>A</query_depth>

- Parent Assembly Query (e.g., asking if A is a parent assembly of B):
<query_ancestor>A,B</query_ancestor>

- Lowest Common Assembly Query (e.g., querying common assembly of A and B):
<query_lca>A,B</query_lca>

## Answer Submission Format

When you have determined the direct parent assembly of the target, submit your answer using:

<answer>X</answer>

where X is the parent assembly ID you inferred for {target}.

## Notes

- All component IDs in the BOM: {nodes}
- Try to use as few queries as possible to determine the answer
- Incorrect answer results in analysis failure
"""

    contextualized_rule_zh_5 = """\
欢迎使用“法条层级溯源系统”。现有一套包含 {n} 个条款节点的树状法律体系。

每个条款有唯一的名称。根本大法是 {root}（效力层级为 0）。你需要分析的目标具体条款是 {target}（保证非根本大法）。

你的任务是：仅通过合法查询接口，唯一确定条款 {target} 的直接上位法理依据（直接父级条款）是谁。

## 术语说明

- 效力层级：从根本大法到某细分条款的衍生级数（根本大法为 0）
- 上位法理渊源：条款 a 是条款 b 的上位法理渊源，意味着 a 位于从根本大法到 b 的唯一释法路径上且 a 不等于 b
- 最近公共法理：条款 a 和 b 共同援引的最低级别共同上位法；当 a 等于 b 时，返回 a 本身

## 可用查询

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 效力层级查询：询问某条款的效力深度层级。我会返回一个非负整数。
2. 上位法判断：询问条款 a 是否是条款 b 的严格上位法。我会回答"是"或"否"（当 a 等于 b 时必为"否"）。
3. 最近公共法理查询：询问条款 a 和 b 共同援引的最低级别上位法。我会返回一个条款名称（当 a 等于 b 时返回 a）。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 效力层级查询（例如查询条款 A 的效力级别）：
<query_depth>A</query_depth>

- 上位法判断（例如询问条款 A 是否是 B 的上位法）：
<query_ancestor>A,B</query_ancestor>

- 最近公共法理查询（例如查询条款 A 和 B 的共同法理源头）：
<query_lca>A,B</query_lca>

## 提交答案格式

当你确定了目标条款的直接上位法依据后，请使用以下格式提交答案：

<answer>X</answer>

其中 X 是你推断出的 {target} 的直接上位法条款名称。

## 注意事项

- 体系中的所有条款名称为：{nodes}
- 请尽可能少地使用查询次数来确定答案
- 答案错误将导致审查失败
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Statutory Hierarchy Tracing System". There is a tree-like legal framework comprising {n} clause nodes.

Each clause has a unique name. The fundamental law is {root} (authority level 0). Your target specific clause is {target} (guaranteed not to be the fundamental law).

Your task is: uniquely determine the direct superseding statutory basis (direct parent clause) for clause {target}, using only the legal query interfaces.

## Terminology

- Authority Level: The number of derivation steps from the fundamental law to a clause (fundamental law is 0)
- Superseding Statutory Source: Clause a is a superseding statutory source of clause b if a is on the unique derivation path from the fundamental law to b, and a is not equal to b
- Lowest Common Statutory Basis: The lowest-level common superseding law invoked by a and b; when a equals b, returns a itself

## Available Queries

You can repeatedly make the following three types of queries (one query per turn):

1. Authority Level Query: Ask for the authority depth of a clause. I will return a non-negative integer.
2. Superseding Law Query: Ask whether clause a is a strict superseding statutory source of clause b. I will answer "Yes" or "No" (always "No" when a equals b).
3. Lowest Common Statutory Basis Query: Ask for the lowest-level common superseding law of clauses a and b. I will return a clause name (returns a when a equals b).

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Authority Level Query (e.g., querying level of clause A):
<query_depth>A</query_depth>

- Superseding Law Query (e.g., asking if A is a superseding source for B):
<query_ancestor>A,B</query_ancestor>

- Lowest Common Statutory Basis Query (e.g., querying common basis for A and B):
<query_lca>A,B</query_lca>

## Answer Submission Format

When you have determined the direct superseding statutory basis of the target, submit your answer using:

<answer>X</answer>

where X is the superseding clause name you inferred for {target}.

## Notes

- All clause names in the framework: {nodes}
- Try to use as few queries as possible to determine the answer
- Incorrect answer results in verification failure
"""

    tags = ["answer", "query_depth", "query_ancestor", "query_lca"]
    
    reasoning_type = "演绎推理"
    data_structure = "树"

    # 难度说明：
    # 1 (简单)        - N=5, 深度2, 线性结构
    # 2 (中等偏下)    - N=7, 深度3, 简单分支
    # 3 (中等偏上)    - N=10, 深度4, 中等分支
    # 4 (较难)        - N=12, 深度4, 复杂分支
    # 5 (难)          - N=15, 深度5, 复杂树结构

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "root": "A",
                "target": "E",
                "nodes": ["A", "B", "C", "D", "E"],
                # 树结构: A -> B -> C -> D -> E (链式)
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")],
            },
            2: {
                "n": 7,
                "root": "A",
                "target": "F",
                "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                # 树结构: A -> B -> D, A -> B -> E, A -> C -> F, A -> C -> G
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G")],
            },
            3: {
                "n": 10,
                "root": "A",
                "target": "H",
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                # 树结构: 
                # A -> B -> D -> H, A -> B -> E, A -> C -> F -> I, A -> C -> G -> J
                "edges": [
                    ("A", "B"), ("A", "C"),
                    ("B", "D"), ("B", "E"),
                    ("C", "F"), ("C", "G"),
                    ("D", "H"), ("F", "I"), ("G", "J")
                ],
            },
            4: {
                "n": 12,
                "root": "R",
                "target": "K",
                "nodes": ["R", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
                # 树结构: R作为根，三个主分支，目标在深层
                # R -> A -> D -> G -> K, R -> A -> E, R -> B -> F -> H, R -> B -> I, R -> C -> J
                "edges": [
                    ("R", "A"), ("R", "B"), ("R", "C"),
                    ("A", "D"), ("A", "E"),
                    ("B", "F"), ("B", "I"),
                    ("C", "J"),
                    ("D", "G"), ("F", "H"),
                    ("G", "K")
                ],
            },
            5: {
                "n": 15,
                "root": "R",
                "target": "N",
                "nodes": ["R", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"],
                # 树结构: 复杂的五层结构
                # R -> A -> D -> H -> L, R -> A -> E -> I -> M -> N, R -> B -> F -> J, R -> B -> G -> K, R -> C
                "edges": [
                    ("R", "A"), ("R", "B"), ("R", "C"),
                    ("A", "D"), ("A", "E"),
                    ("B", "F"), ("B", "G"),
                    ("D", "H"), ("E", "I"),
                    ("F", "J"), ("G", "K"),
                    ("H", "L"), ("I", "M"),
                    ("M", "N")
                ],
            },
        },
        "en": {
            1: {
                "n": 5,
                "root": "A",
                "target": "E",
                "nodes": ["A", "B", "C", "D", "E"],
                "edges": [("A", "B"), ("B", "C"), ("C", "D"), ("D", "E")],
            },
            2: {
                "n": 7,
                "root": "A",
                "target": "F",
                "nodes": ["A", "B", "C", "D", "E", "F", "G"],
                "edges": [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "F"), ("C", "G")],
            },
            3: {
                "n": 10,
                "root": "A",
                "target": "H",
                "nodes": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [
                    ("A", "B"), ("A", "C"),
                    ("B", "D"), ("B", "E"),
                    ("C", "F"), ("C", "G"),
                    ("D", "H"), ("F", "I"), ("G", "J")
                ],
            },
            4: {
                "n": 12,
                "root": "R",
                "target": "K",
                "nodes": ["R", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"],
                "edges": [
                    ("R", "A"), ("R", "B"), ("R", "C"),
                    ("A", "D"), ("A", "E"),
                    ("B", "F"), ("B", "I"),
                    ("C", "J"),
                    ("D", "G"), ("F", "H"),
                    ("G", "K")
                ],
            },
            5: {
                "n": 15,
                "root": "R",
                "target": "N",
                "nodes": ["R", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N"],
                "edges": [
                    ("R", "A"), ("R", "B"), ("R", "C"),
                    ("A", "D"), ("A", "E"),
                    ("B", "F"), ("B", "G"),
                    ("D", "H"), ("E", "I"),
                    ("F", "J"), ("G", "K"),
                    ("H", "L"), ("I", "M"),
                    ("M", "N")
                ],
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
        
        # 使用固定种子进行随机化，保证可复现性
        rng = random.Random(42)
        original_nodes = cfg["nodes"]
        shuffled_nodes = list(original_nodes)
        rng.shuffle(shuffled_nodes)
        name_map = {old: new for old, new in zip(original_nodes, shuffled_nodes)}
        
        mapped_nodes = [name_map[n] for n in original_nodes]
        mapped_root = name_map[cfg["root"]]
        mapped_target = name_map[cfg["target"]]
        mapped_edges = [(name_map[p], name_map[c]) for p, c in cfg["edges"]]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = mapped_root
        self._game_info["target"] = mapped_target
        self._game_info["nodes"] = ", ".join(mapped_nodes)
        
        # 构建树结构
        self.nodes = set(mapped_nodes)
        self.root = mapped_root
        self.target = mapped_target
        self.edges = mapped_edges
        
        # 构建父节点映射和子节点映射
        self.parent = {}  # node -> parent
        self.children = {node: [] for node in self.nodes}  # node -> [children]
        
        for parent, child in self.edges:
            self.parent[child] = parent
            self.children[parent].append(child)
        
        # 计算每个节点的深度
        self.depth_map = {}
        self._compute_depths(self.root, 0)
        
        # 预计算从根到每个节点的路径（用于祖先判断）
        self.path_to_node = {}
        self._compute_paths(self.root, [])

    def _compute_depths(self, node, depth):
        """递归计算每个节点的深度"""
        self.depth_map[node] = depth
        for child in self.children[node]:
            self._compute_depths(child, depth + 1)

    def _compute_paths(self, node, path):
        """递归计算从根到每个节点的路径"""
        current_path = path + [node]
        self.path_to_node[node] = current_path
        for child in self.children[node]:
            self._compute_paths(child, current_path)

    def _is_ancestor(self, a, b):
        """判断a是否是b的严格祖先"""
        if a == b:
            return False
        path_to_b = self.path_to_node[b]
        return a in path_to_b

    def _find_lca(self, a, b):
        """找到a和b的最近公共祖先"""
        if a == b:
            return a
        
        path_a = self.path_to_node[a]
        path_b = self.path_to_node[b]
        
        # 找到最后一个公共节点
        lca = self.root
        for i in range(min(len(path_a), len(path_b))):
            if path_a[i] == path_b[i]:
                lca = path_a[i]
            else:
                break
        return lca

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        answer = parsed_info["answer"].strip()
        
        # 检查答案是否为有效节点
        if answer not in self.nodes:
            return False
        
        # 检查答案是否是目标节点的真实父节点
        true_parent = self.parent.get(self.target)
        return answer == true_parent

    def _cf_core_produce(self, parsed_info):
        """原始的查询处理逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_invalid_node = "错误：节点名字不存在。"
            error_invalid_format = "错误：查询格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_invalid_node = "Error: Node name does not exist."
            error_invalid_format = "Error: Invalid query format."

        # 优先级：depth > ancestor > lca
        if "query_depth" in parsed_info:
            node = parsed_info["query_depth"].strip()
            if node not in self.nodes:
                return error_invalid_node
            return str(self.depth_map[node])

        elif "query_ancestor" in parsed_info:
            try:
                raw = parsed_info["query_ancestor"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_invalid_format
                a, b = parts
                if a not in self.nodes or b not in self.nodes:
                    return error_invalid_node
                return yes_res if self._is_ancestor(a, b) else no_res
            except:
                return error_invalid_format

        elif "query_lca" in parsed_info:
            try:
                raw = parsed_info["query_lca"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_invalid_format
                a, b = parts
                if a not in self.nodes or b not in self.nodes:
                    return error_invalid_node
                return self._find_lca(a, b)
            except:
                return error_invalid_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成一个与正确答案不同的错误答案"""
        # 如果正确答案本身是错误信息，直接返回（不需要伪造）
        if correct.startswith("Error:") or correct.startswith("错误："):
            return correct  # 错误消息无需伪造
        
        # 如果是数字（深度查询结果），返回一个不同的数字
        if correct.isdigit():
            wrong_val = int(correct) + 1
            return str(wrong_val)
        
        # 如果是"是/否"或"Yes/No"（祖先判断结果），取反
        if self.config.language == "zh":
            if correct == "是": return "否"
            if correct == "否": return "是"
        else:
            if correct == "Yes": return "No"
            if correct == "No": return "Yes"
        
        # 如果是节点名（LCA查询结果），返回一个不同的合法节点名
        sorted_nodes = sorted(list(self.nodes))
        for node in sorted_nodes:
            if node != correct:
                return node
        # 如果只有一个节点（不太可能），加后缀
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        """
        枚举所有合法查询并返回对应的正确答案。
        为控制数量，排除 a==b 的冗余情况（自查询意义不大）。
        """
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        sorted_nodes = sorted(list(self.nodes))
        
        # 1. 深度查询
        for node in sorted_nodes:
            query_str = f"<query_depth>{node}</query_depth>"
            answer = str(self.depth_map[node])
            queries.append({
                "query": query_str,
                "answer": answer
            })

        # 2. 祖先判断（排除 a==b，因为结果恒为 No，信息量低）
        for a in sorted_nodes:
            for b in sorted_nodes:
                if a == b:
                    continue
                query_ancestor = f"<query_ancestor>{a},{b}</query_ancestor>"
                is_anc = self._is_ancestor(a, b)
                ans_ancestor = yes_res if is_anc else no_res
                queries.append({
                    "query": query_ancestor,
                    "answer": ans_ancestor
                })

        # 3. LCA 查询（利用对称性，只枚举 a <= b）
        for i, a in enumerate(sorted_nodes):
            for b in sorted_nodes[i:]:
                query_lca = f"<query_lca>{a},{b}</query_lca>"
                ans_lca = self._find_lca(a, b)
                queries.append({
                    "query": query_lca,
                    "answer": ans_lca
                })

        return queries