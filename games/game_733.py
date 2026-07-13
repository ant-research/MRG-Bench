# -*- coding: utf-8 -*-
from .base import Game
import random

class TreeParentFindingGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树父节点查询"的推理游戏，规则如下：

游戏设定了一棵未知的有根无向无权树，节点编号为 1 到 {n}，根节点为 {root}。树是连通的且无环，任意两个节点间存在唯一的简单路径。

你需要通过查询来推断出目标节点 {target} 的父节点。{target_note}

## 定义
- 距离：两个节点 u 和 v 之间唯一简单路径的边数。
- 深度：节点 x 到根节点的距离，根节点的深度为 0。
- 最近公共祖先：同时为两个节点 u 和 v 的祖先且深度最大的节点。

## 允许的查询

你可以反复向我提出以下四类问题（每次仅限一个问题），我会根据真实的树结构如实回答：

1. 深度查询：询问节点 x 的深度。回答一个非负整数。
2. 距离查询：询问节点 u 和 v 之间的距离。回答一个非负整数。
3. 最近公共祖先查询：询问节点 u 和 v 的最近公共祖先。回答一个节点编号。
4. 距离比较查询：给定三个节点 u、v、w，比较 u 到 w 的距离与 v 到 w 的距离。回答"u更近"、"v更近"或"相等"。

注意：你不能直接询问父子关系、相邻性或边是否存在。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 深度查询（例如问节点 5 的深度）：
<query_depth>5</query_depth>

- 距离查询（例如问节点 1 和 3 之间的距离）：
<query_distance>1,3</query_distance>

- 最近公共祖先查询（例如问节点 2 和 4 的最近公共祖先）：
<query_lca>2,4</query_lca>

- 距离比较查询（例如比较节点 1 和 2 到节点 5 的距离）：
<query_compare>1,2,5</query_compare>

提交最终答案时，请给出目标节点的父节点编号，格式如下：

<answer>3</answer>

{root_answer_note}
"""

    game_rule_en = """\
Let's play a "Tree Parent Finding" deduction game. Here are the rules:

The game involves an unknown rooted undirected unweighted tree with nodes numbered from 1 to {n}, and the root is node {root}. The tree is connected and acyclic, with a unique simple path between any two nodes.

You need to infer the parent node of the target node {target} through queries. {target_note}

## Definitions
- Distance: The number of edges in the unique simple path between two nodes u and v.
- Depth: The distance from node x to the root node; the root has depth 0.
- Lowest Common Ancestor (LCA): The node that is an ancestor of both u and v with the maximum depth.

## Allowed Queries

You can repeatedly ask me four types of questions (one per turn), and I will answer truthfully based on the actual tree structure:

1. Depth Query: Ask for the depth of node x. Returns a non-negative integer.
2. Distance Query: Ask for the distance between nodes u and v. Returns a non-negative integer.
3. LCA Query: Ask for the lowest common ancestor of nodes u and v. Returns a node number.
4. Distance Comparison Query: Given three nodes u, v, w, compare the distance from u to w with the distance from v to w. Returns "u closer", "v closer", or "equal".

Note: You cannot directly ask about parent-child relationships, adjacency, or whether an edge exists.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Depth Query (e.g., asking about the depth of node 5):
<query_depth>5</query_depth>

- Distance Query (e.g., asking about the distance between nodes 1 and 3):
<query_distance>1,3</query_distance>

- LCA Query (e.g., asking about the LCA of nodes 2 and 4):
<query_lca>2,4</query_lca>

- Distance Comparison Query (e.g., comparing distances from nodes 1 and 2 to node 5):
<query_compare>1,2,5</query_compare>

When submitting the final answer, provide the parent node number of the target node using this format:

<answer>3</answer>

{root_answer_note}
"""

    contextualized_rule_zh_1 = """\
这是交通规划部门的“轨道交通网络拓扑溯源”系统。

系统记录了一个未知的无环连通交通网，包含站点 1 到 {n}，其中中央枢纽总站为 {root}。任意两站点间存在唯一的乘车路线。
你需要通过查询，推断出目标站点 {target} 的前序站点（即朝向中央枢纽的直接相邻站，对应树的父节点）。{target_note}

## 术语定义
- 距离：两个站点 u 和 v 之间相隔的路线站数。
- 深度：站点 x 距离中央枢纽总站的站数，中央枢纽的深度为 0。
- 最近公共枢纽：同时为两个站点 u 和 v 通往总站路径上的公共换乘站，且距离总站最远的那个站点。

## 允许的查询

你可以反复提出以下四类问题（每次仅限一个）：
1. 深度查询：询问站点 x 距离总站的站数。回答一个非负整数。
2. 距离查询：询问站点 u 和 v 之间的距离站数。回答一个非负整数。
3. 最近公共枢纽查询：询问站点 u 和 v 的最近公共枢纽。回答一个站点编号。
4. 距离比较查询：给定三个站点 u、v、w，比较 u 到 w 与 v 到 w 的距离站数。回答"u更近"、"v更近"或"相等"。

注意：你不能直接询问站点的相邻关系或具体的线路连接。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：
- 深度查询：<query_depth>5</query_depth>
- 距离查询：<query_distance>1,3</query_distance>
- 最近公共枢纽查询：<query_lca>2,4</query_lca>
- 距离比较查询：<query_compare>1,2,5</query_compare>

提交最终答案时，请给出目标站点的前序站点编号：
<answer>3</answer>

{root_answer_note}
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Transit Network Topology Tracing System.

The system maps an unknown connected acyclic transit network with stations numbered from 1 to {n}. The central hub is station {root}. There is a unique route between any two stations.
You need to infer the immediate inbound station of the target station {target} (i.e., its parent node, the direct next stop towards the central hub). {target_note}

## Definitions
- Distance: The number of stops on the unique route between stations u and v.
- Depth: The distance from station x to the central hub; the central hub has depth 0.
- Lowest Common Hub (LCA): The station that serves as a common transfer point for both u and v on their way to the central hub, located furthest from the central hub.

## Allowed Queries

You can repeatedly ask four types of questions (one per turn):
1. Depth Query: Ask for the depth of station x. Returns a non-negative integer.
2. Distance Query: Ask for the distance between stations u and v. Returns a non-negative integer.
3. Lowest Common Hub Query: Ask for the lowest common hub of stations u and v. Returns a station number.
4. Distance Comparison Query: Given three stations u, v, w, compare the distance from u to w with the distance from v to w. Returns "u closer", "v closer", or "equal".

Note: You cannot directly ask about adjacent stations or exact line connections.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:
- Depth Query: <query_depth>5</query_depth>
- Distance Query: <query_distance>1,3</query_distance>
- Lowest Common Hub Query: <query_lca>2,4</query_lca>
- Distance Comparison Query: <query_compare>1,2,5</query_compare>

When submitting the final answer, provide the immediate inbound station number of the target station:
<answer>3</answer>

{root_answer_note}
"""

    contextualized_rule_zh_2 = """\
这是疾控中心的“传染病流调溯源”系统。

本系统追踪了一起聚集性疫情的传播链（呈树状拓扑），涉及感染者 1 到 {n}，其中零号病人（首发病例）为 {root}。
你需要通过查询，推断出传染给目标病例 {target} 的直接传染源（即树的父节点）。{target_note}

## 术语定义
- 距离：两个病例 u 和 v 之间相隔的传播链环节数。
- 深度：病例 x 距离零号病人的感染代际数，零号病人的深度为 0。
- 最近公共传染源：同时为病例 u 和 v 提供传播溯源的共同上游感染者中，距离零号病人最远的病例。

## 允许的查询

你可以反复提出以下四类问题（每次仅限一个）：
1. 深度查询：询问病例 x 的感染代际数。回答一个非负整数。
2. 距离查询：询问病例 u 和 v 之间的传播链距离。回答一个非负整数。
3. 最近公共传染源查询：询问病例 u 和 v 的最近公共传染源。回答一个病例编号。
4. 距离比较查询：给定三个病例 u、v、w，比较 u 到 w 与 v 到 w 的链条距离。回答"u更近"、"v更近"或"相等"。

注意：你不能直接询问两人的直接传染关系。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：
- 深度查询：<query_depth>5</query_depth>
- 距离查询：<query_distance>1,3</query_distance>
- 最近公共传染源查询：<query_lca>2,4</query_lca>
- 距离比较查询：<query_compare>1,2,5</query_compare>

提交最终答案时，请给出目标病例的直接传染源编号：
<answer>3</answer>

{root_answer_note}
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the CDC's "Infectious Disease Tracing" system.

The system tracks a transmission chain (structured as a tree) of a cluster outbreak, involving cases 1 to {n}. Patient Zero (the index case) is {root}. 
You need to infer the direct infector (i.e., the parent node) of the target case {target}. {target_note}

## Definitions
- Distance: The number of transmission links between two cases u and v.
- Depth: The generation of infection from Patient Zero; Patient Zero has depth 0.
- Most Recent Common Infector (LCA): The case that serves as a common source of infection for both u and v, located furthest from Patient Zero.

## Allowed Queries

You can repeatedly ask four types of questions (one per turn):
1. Depth Query: Ask for the infection depth of case x. Returns a non-negative integer.
2. Distance Query: Ask for the transmission distance between cases u and v. Returns a non-negative integer.
3. Most Recent Common Infector Query: Ask for the most recent common infector of cases u and v. Returns a case number.
4. Distance Comparison Query: Given three cases u, v, w, compare the distance from u to w with the distance from v to w. Returns "u closer", "v closer", or "equal".

Note: You cannot directly ask about direct transmission relationships.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:
- Depth Query: <query_depth>5</query_depth>
- Distance Query: <query_distance>1,3</query_distance>
- Most Recent Common Infector Query: <query_lca>2,4</query_lca>
- Distance Comparison Query: <query_compare>1,2,5</query_compare>

When submitting the final answer, provide the direct infector's case number for the target case:
<answer>3</answer>

{root_answer_note}
"""

    contextualized_rule_zh_3 = """\
这是一个“知识点前置依赖图”分析系统。

本系统包含一个树状的前置课程网络，涵盖课题 1 到 {n}，其中最底层的核心基础概念为 {root}。
你需要通过查询，推断出学习目标课题 {target} 所需的直接先修课题（即树的父节点）。{target_note}

## 术语定义
- 距离：两个课题 u 和 v 之间的推导路径跨度（涉及的课题数）。
- 深度：课题 x 距离核心基础概念的层级跨度，核心基础的深度为 0。
- 最近公共前置基础：同时为课题 u 和 v 的前置先修基础中，距离核心基础最远（最具体）的课题。

## 允许的查询

你可以反复提出以下四类问题（每次仅限一个）：
1. 深度查询：询问课题 x 距离核心基础的层级。回答一个非负整数。
2. 距离查询：询问课题 u 和 v 之间的推导跨度。回答一个非负整数。
3. 最近公共前置基础查询：询问课题 u 和 v 的最近公共前置基础。回答一个课题编号。
4. 距离比较查询：给定三个课题 u、v、w，比较 u 到 w 与 v 到 w 的推导跨度。回答"u更近"、"v更近"或"相等"。

注意：你不能直接询问课题之间的直接依赖关系。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：
- 深度查询：<query_depth>5</query_depth>
- 距离查询：<query_distance>1,3</query_distance>
- 最近公共前置基础查询：<query_lca>2,4</query_lca>
- 距离比较查询：<query_compare>1,2,5</query_compare>

提交最终答案时，请给出目标课题的直接先修课题编号：
<answer>3</answer>

{root_answer_note}
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Prerequisite Dependency Graph" analysis system.

This system contains a tree-like prerequisite course network covering topics 1 to {n}. The fundamental core concept is {root}.
You need to infer the direct prerequisite topic (i.e., the parent node) required to study the target topic {target}. {target_note}

## Definitions
- Distance: The number of dependency steps between topics u and v.
- Depth: The dependency layers from the core concept; the core concept has depth 0.
- Most Specific Common Prerequisite (LCA): The topic that serves as a common prerequisite for both u and v, located furthest from the core concept.

## Allowed Queries

You can repeatedly ask four types of questions (one per turn):
1. Depth Query: Ask for the depth of topic x. Returns a non-negative integer.
2. Distance Query: Ask for the distance between topics u and v. Returns a non-negative integer.
3. Most Specific Common Prerequisite Query: Ask for the most specific common prerequisite of topics u and v. Returns a topic number.
4. Distance Comparison Query: Given three topics u, v, w, compare the distance from u to w with the distance from v to w. Returns "u closer", "v closer", or "equal".

Note: You cannot directly ask about direct prerequisite relationships.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:
- Depth Query: <query_depth>5</query_depth>
- Distance Query: <query_distance>1,3</query_distance>
- Most Specific Common Prerequisite Query: <query_lca>2,4</query_lca>
- Distance Comparison Query: <query_compare>1,2,5</query_compare>

When submitting the final answer, provide the direct prerequisite topic number for the target topic:
<answer>3</answer>

{root_answer_note}
"""

    contextualized_rule_zh_4 = """\
这是一个“产品BOM（物料清单）装配树”分析系统。

本系统记录了一款复杂产品的层级装配结构，包含组件 1 到 {n}，其中最终主产品（总成）为 {root}。
你需要通过查询，推断出目标组件 {target} 直接所属的上级总成（即树的父节点）。{target_note}

## 术语定义
- 距离：两个组件 u 和 v 之间的装配层级跨度。
- 深度：组件 x 距离最终主产品的装配层级，最终主产品的深度为 0。
- 最低级公共总成：同时包含组件 u 和 v 的直接或间接装配总成中，层级最深（最底层）的那个。

## 允许的查询

你可以反复提出以下四类问题（每次仅限一个）：
1. 深度查询：询问组件 x 距离最终产品的装配层级。回答一个非负整数。
2. 距离查询：询问组件 u 和 v 之间的装配层级跨度。回答一个非负整数。
3. 最低级公共总成查询：询问组件 u 和 v 的最低级公共总成。回答一个组件编号。
4. 距离比较查询：给定三个组件 u、v、w，比较 u 到 w 与 v 到 w 的层级跨度。回答"u更近"、"v更近"或"相等"。

注意：你不能直接询问组件的所属装配关系。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：
- 深度查询：<query_depth>5</query_depth>
- 距离查询：<query_distance>1,3</query_distance>
- 最低级公共总成查询：<query_lca>2,4</query_lca>
- 距离比较查询：<query_compare>1,2,5</query_compare>

提交最终答案时，请给出目标组件的直接上级总成编号：
<answer>3</answer>

{root_answer_note}
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Product BOM (Bill of Materials) Assembly Tree" analysis system.

This system records the hierarchical assembly structure of a complex product, containing components 1 to {n}. The final main product (main assembly) is {root}.
You need to infer the immediate parent assembly (i.e., the parent node) that directly contains the target component {target}. {target_note}

## Definitions
- Distance: The number of assembly steps between components u and v.
- Depth: The assembly layers from the final product; the final product has depth 0.
- Lowest Common Assembly (LCA): The component that serves as a common overarching assembly for both u and v, located furthest from the final product.

## Allowed Queries

You can repeatedly ask four types of questions (one per turn):
1. Depth Query: Ask for the depth of component x. Returns a non-negative integer.
2. Distance Query: Ask for the distance between components u and v. Returns a non-negative integer.
3. Lowest Common Assembly Query: Ask for the lowest common assembly of components u and v. Returns a component number.
4. Distance Comparison Query: Given three components u, v, w, compare the distance from u to w with the distance from v to w. Returns "u closer", "v closer", or "equal".

Note: You cannot directly ask about direct assembly relationships.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:
- Depth Query: <query_depth>5</query_depth>
- Distance Query: <query_distance>1,3</query_distance>
- Lowest Common Assembly Query: <query_lca>2,4</query_lca>
- Distance Comparison Query: <query_compare>1,2,5</query_compare>

When submitting the final answer, provide the immediate parent assembly component number for the target component:
<answer>3</answer>

{root_answer_note}
"""

    contextualized_rule_zh_5 = """\
这是一个“企业股权穿透与控制权”调查系统。

本系统掌握了一个复杂的树状商业帝国网络，涉及实体公司 1 到 {n}，其中顶层最终控股集团为 {root}。
你需要通过查询，推断出直接控股目标公司 {target} 的上一级母公司（即树的父节点）。{target_note}

## 术语定义
- 距离：两家实体 u 和 v 之间的持股链条跨度。
- 深度：实体 x 距离顶层控股集团的持股层级，顶层集团的深度为 0。
- 最低层级公共控股方：同时间接或直接控股实体 u 和 v 的母公司中，距离顶层集团最远（最底层）的一家。

## 允许的查询

你可以反复提出以下四类问题（每次仅限一个）：
1. 深度查询：询问实体 x 距离顶层集团的持股层级。回答一个非负整数。
2. 距离查询：询问实体 u 和 v 之间的持股链条跨度。回答一个非负整数。
3. 最低层级公共控股方查询：询问实体 u 和 v 的最低层级公共控股方。回答一个实体编号。
4. 距离比较查询：给定三个实体 u、v、w，比较 u 到 w 与 v 到 w 的链条跨度。回答"u更近"、"v更近"或"相等"。

注意：你不能直接询问两家实体的直接控股关系。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：
- 深度查询：<query_depth>5</query_depth>
- 距离查询：<query_distance>1,3</query_distance>
- 最低层级公共控股方查询：<query_lca>2,4</query_lca>
- 距离比较查询：<query_compare>1,2,5</query_compare>

提交最终答案时，请给出目标公司的直接母公司编号：
<answer>3</answer>

{root_answer_note}
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Corporate Equity Penetration and Control" investigation system.

This system maps a complex tree-like business empire network involving corporate entities 1 to {n}. The ultimate holding group at the top is {root}.
You need to infer the immediate parent company (i.e., the parent node) that directly controls the target company {target}. {target_note}

## Definitions
- Distance: The number of holding steps between entities u and v.
- Depth: The ownership layers from the ultimate holding group; the holding group has depth 0.
- Lowest Common Holding Company (LCA): The entity that serves as a common controlling parent for both u and v, located furthest from the ultimate holding group.

## Allowed Queries

You can repeatedly ask four types of questions (one per turn):
1. Depth Query: Ask for the depth of entity x. Returns a non-negative integer.
2. Distance Query: Ask for the distance between entities u and v. Returns a non-negative integer.
3. Lowest Common Holding Company Query: Ask for the lowest common holding company of entities u and v. Returns an entity number.
4. Distance Comparison Query: Given three entities u, v, w, compare the distance from u to w with the distance from v to w. Returns "u closer", "v closer", or "equal".

Note: You cannot directly ask about direct subsidiary relationships.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:
- Depth Query: <query_depth>5</query_depth>
- Distance Query: <query_distance>1,3</query_distance>
- Lowest Common Holding Company Query: <query_lca>2,4</query_lca>
- Distance Comparison Query: <query_compare>1,2,5</query_compare>

When submitting the final answer, provide the immediate parent company number for the target company:
<answer>3</answer>

{root_answer_note}
"""

    tags = ["answer", "query_depth", "query_distance", "query_lca", "query_compare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "root": 1,
                "target": 3,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "parent": 2,
            },
            2: {
                "n": 7,
                "root": 1,
                "target": 5,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "parent": 2,
            },
            3: {
                "n": 10,
                "root": 1,
                "target": 8,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "parent": 4,
            },
            4: {
                "n": 12,
                "root": 1,
                "target": 10,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (4, 9), (6, 10), (7, 11), (8, 12)],
                "parent": 6,
            },
            5: {
                "n": 15,
                "root": 1,
                "target": 13,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (5, 10), (6, 11), (7, 12), (7, 13), (10, 14), (11, 15)],
                "parent": 7,
            },
        },
        "en": {
            1: {
                "n": 5,
                "root": 1,
                "target": 3,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "parent": 2,
            },
            2: {
                "n": 7,
                "root": 1,
                "target": 5,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "parent": 2,
            },
            3: {
                "n": 10,
                "root": 1,
                "target": 8,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "parent": 4,
            },
            4: {
                "n": 12,
                "root": 1,
                "target": 10,
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (4, 9), (6, 10), (7, 11), (8, 12)],
                "parent": 6,
            },
            5: {
                "n": 15,
                "root": 1,
                "target": 13,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (5, 10), (6, 11), (7, 12), (7, 13), (10, 14), (11, 15)],
                "parent": 7,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self._game_info["target"] = cfg["target"]
        
        # 根据语言设置注释
        if cfg["target"] == cfg["root"]:
            if lang == "zh":
                self._game_info["target_note"] = "注意：目标节点就是根节点（或起点），因此没有父节点。"
                self._game_info["root_answer_note"] = "如果目标节点是根节点，请提交 <answer>无</answer>"
            else:
                self._game_info["target_note"] = "Note: The target node is the root/start point, so it has no parent."
                self._game_info["root_answer_note"] = "If the target node is the root, submit <answer>none</answer>"
        else:
            self._game_info["target_note"] = ""
            self._game_info["root_answer_note"] = ""

        # 构建树结构
        self.n = cfg["n"]
        self.root = cfg["root"]
        self.target = cfg["target"]
        self.edges = cfg["edges"]
        self.correct_parent = cfg["parent"]

        # 构建邻接表
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

        # 计算每个节点的父节点、深度
        self.parent_map = {}
        self.depth_map = {}
        self._bfs_build_tree()

    def _bfs_build_tree(self):
        """从根节点开始BFS构建父节点关系和深度"""
        from collections import deque
        
        queue = deque([self.root])
        self.parent_map[self.root] = None
        self.depth_map[self.root] = 0
        visited = {self.root}

        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    self.parent_map[v] = u
                    self.depth_map[v] = self.depth_map[u] + 1
                    queue.append(v)

    def _get_distance(self, u, v):
        """计算两个节点之间的距离"""
        # 通过LCA计算距离
        lca = self._get_lca(u, v)
        return self.depth_map[u] + self.depth_map[v] - 2 * self.depth_map[lca]

    def _get_lca(self, u, v):
        """计算两个节点的最近公共祖先"""
        # 将u和v移动到同一深度
        while self.depth_map[u] > self.depth_map[v]:
            u = self.parent_map[u]
        while self.depth_map[v] > self.depth_map[u]:
            v = self.parent_map[v]
        
        # 同时向上移动直到相遇
        while u != v:
            u = self.parent_map[u]
            v = self.parent_map[v]
        
        return u

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 处理根节点情况
        if self.target == self.root:
            if self.config.language == "zh":
                return raw_ans in ["无", "None", "none"]
            else:
                return raw_ans.lower() in ["none", "无"]
        
        # 尝试解析为整数
        try:
            ans_node = int(raw_ans)
            return ans_node == self.correct_parent
        except ValueError:
            return False

    def _cf_core_produce(self, parsed_info):
        """根据查询类型产生真实的业务逻辑响应"""
        if self.config.language == "zh":
            error_format = "错误：格式无效或节点编号错误。"
            error_range = "错误：节点编号超出范围。"
        else:
            error_format = "Error: Invalid format or node number."
            error_range = "Error: Node number out of range."

        # 深度查询
        if "query_depth" in parsed_info:
            try:
                node = int(parsed_info["query_depth"].strip())
                if node < 1 or node > self.n:
                    return error_range
                return str(self.depth_map[node])
            except ValueError:
                return error_format

        # 距离查询
        elif "query_distance" in parsed_info:
            try:
                raw = parsed_info["query_distance"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return error_range
                dist = self._get_distance(u, v)
                return str(dist)
            except (ValueError, IndexError):
                return error_format

        # LCA查询
        elif "query_lca" in parsed_info:
            try:
                raw = parsed_info["query_lca"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                if u < 1 or u > self.n or v < 1 or v > self.n:
                    return error_range
                lca = self._get_lca(u, v)
                return str(lca)
            except (ValueError, IndexError):
                return error_format

        # 距离比较查询
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return error_format
                u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
                if u < 1 or u > self.n or v < 1 or v > self.n or w < 1 or w > self.n:
                    return error_range
                
                dist_u_w = self._get_distance(u, w)
                dist_v_w = self._get_distance(v, w)
                
                if self.config.language == "zh":
                    if dist_u_w < dist_v_w:
                        return "u更近"
                    elif dist_u_w > dist_v_w:
                        return "v更近"
                    else:
                        return "相等"
                else:
                    if dist_u_w < dist_v_w:
                        return "u closer"
                    elif dist_u_w > dist_v_w:
                        return "v closer"
                    else:
                        return "equal"
            except (ValueError, IndexError):
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个与正确答案不同的错误响应，用于反事实干预"""
        # 尝试将正确答案解析为整数并偏移
        try:
            val = int(correct)
            # 返回一个不同的数值
            wrong_val = val + 1 if val + 1 <= self.n else val - 1
            return str(wrong_val)
        except ValueError:
            pass
        
        # 对于文本类答案（如距离比较的结果）
        alternatives_zh = ["u更近", "v更近", "相等"]
        alternatives_en = ["u closer", "v closer", "equal"]
        
        if correct in alternatives_zh:
            candidates = [a for a in alternatives_zh if a != correct]
            return random.choice(candidates)
        elif correct in alternatives_en:
            candidates = [a for a in alternatives_en if a != correct]
            return random.choice(candidates)
        
        # 兜底
        return correct + "_wrong"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        去除对称重复以控制查询集大小。
        """
        results = []
        
        # 1. 深度查询 (query_depth)
        for x in range(1, self.n + 1):
            query_str = f"<query_depth>{x}</query_depth>"
            ans = str(self.depth_map[x])
            results.append({"query": query_str, "answer": ans})
            
        # 2. 距离查询 (query_distance) - 只枚举 u < v，距离具有对称性
        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                query_str = f"<query_distance>{u},{v}</query_distance>"
                ans = str(self._get_distance(u, v))
                results.append({"query": query_str, "answer": ans})

        # 3. 最近公共祖先查询 (query_lca) - 只枚举 u < v，LCA 具有对称性
        for u in range(1, self.n + 1):
            for v in range(u + 1, self.n + 1):
                query_str = f"<query_lca>{u},{v}</query_lca>"
                ans = str(self._get_lca(u, v))
                results.append({"query": query_str, "answer": ans})

        # 4. 距离比较查询 (query_compare)
        # 注意：交换 u 和 v 会导致答案翻转（u closer <-> v closer），不是对称的
        # 因此需要枚举所有不同的 (u, v) 对，u != v
        for u in range(1, self.n + 1):
            for v in range(1, self.n + 1):
                if u == v:
                    continue
                for w in range(1, self.n + 1):
                    query_str = f"<query_compare>{u},{v},{w}</query_compare>"
                    
                    dist_u_w = self._get_distance(u, w)
                    dist_v_w = self._get_distance(v, w)
                    
                    if self.config.language == "zh":
                        if dist_u_w < dist_v_w:
                            ans = "u更近"
                        elif dist_u_w > dist_v_w:
                            ans = "v更近"
                        else:
                            ans = "相等"
                    else:
                        if dist_u_w < dist_v_w:
                            ans = "u closer"
                        elif dist_u_w > dist_v_w:
                            ans = "v closer"
                        else:
                            ans = "equal"
                            
                    results.append({"query": query_str, "answer": ans})
                    
        return results