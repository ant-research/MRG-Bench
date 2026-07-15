import re
from .base import Game

class TreeRelationGame(Game):

    game_rule_zh = """\
我们来玩一个"树上关系推理与路径规划"游戏，规则如下：

游戏设定了一棵有根树，根节点为 A。树的结构如下：
- 节点：A, B, C, D, E, F, G, H, I
- 边（无向）：{edges}

在这棵树上，我已秘密选择了一个二元关系 R，它是以下四种关系之一：
1. 祖先（包含自身）
2. 严格祖先（不含自身）
3. 子孙（包含自身）
4. 严格子孙（不含自身）

说明：
- U 是 V 的祖先，当且仅当 U 位于从根 A 到 V 的唯一路径上。
- V 是 U 的子孙，是祖先关系的逆关系。
- "包含自身"表示节点与自己也满足该关系；"严格"表示不包含自身。

你的目标有两个：
1. 通过提问确定隐藏的关系 R 是哪一种。
2. 给出一条从起点 {start} 到终点 {end} 的路径，路径需满足：
   - 每一步只能沿着树的边移动到相邻节点
   - 对路径中每一步从节点 u 移动到节点 v，必须满足 R(v, u) 为真

你可以反复提问"R(X, Y) 是否为真？"，我会如实回答"是"或"否"。请尽可能少地提问以完成任务。

每次提问使用以下 XML 格式（X 和 Y 为节点名称）：

<query>X,Y</query>

提交最终答案时，需要同时指明关系类型和路径（或声明无法抵达）。关系类型使用以下代号：
- ancestor_inclusive: 祖先（包含自身）
- ancestor_strict: 严格祖先（不含自身）
- descendant_inclusive: 子孙（包含自身）
- descendant_strict: 严格子孙（不含自身）

答案格式如下：

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

或若无法抵达：

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    game_rule_en = """\
Let's play a "Tree Relation Inference and Path Planning" game. Here are the rules:

The game is set on a rooted tree with root node A. The tree structure is:
- Nodes: A, B, C, D, E, F, G, H, I
- Edges (undirected): {edges}

On this tree, I have secretly chosen a binary relation R, which is one of the following four relations:
1. Ancestor (including self)
2. Strict Ancestor (excluding self)
3. Descendant (including self)
4. Strict Descendant (excluding self)

Explanation:
- U is an ancestor of V if and only if U is on the unique path from root A to V.
- V is a descendant of U is the inverse of the ancestor relation.
- "Including self" means a node satisfies the relation with itself; "strict" means excluding self.

Your goals are twofold:
1. Determine which of the four relations is the hidden relation R through queries.
2. Provide a path from start node {start} to end node {end}, where the path must satisfy:
   - Each step can only move along a tree edge to an adjacent node
   - For each step from node u to node v in the path, R(v, u) must be true

You can repeatedly ask "Is R(X, Y) true?" and I will answer "Yes" or "No" truthfully. Try to complete the task with as few queries as possible.

Use the following XML format for queries (X and Y are node names):

<query>X,Y</query>

When submitting the final answer, specify both the relation type and the path (or declare unreachable). Use these codes for relation types:
- ancestor_inclusive: Ancestor (including self)
- ancestor_strict: Strict Ancestor (excluding self)
- descendant_inclusive: Descendant (including self)
- descendant_strict: Strict Descendant (excluding self)

Answer format:

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

Or if unreachable:

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"路网调度与物流路径规划"游戏，规则如下：

游戏设定了一个层级路网，调度中心为 A。路网的结构如下：
- 站点：A, B, C, D, E, F, G, H, I
- 道路（无向）：{edges}

在这个路网上，我已秘密选择了一个二元关系 R，它是以下四种关系之一：
1. 供货上游（包含自身）
2. 严格供货上游（不含自身）
3. 接收下游（包含自身）
4. 严格接收下游（不含自身）

说明：
- 站点 U 是 V 的供货上游，当且仅当 U 位于从调度中心 A 到 V 的唯一主干线路上。
- 接收下游是供货上游的逆关系。
- "包含自身"表示站点与自己也满足该关系；"严格"表示不包含自身。

你的目标有两个：
1. 通过提问确定隐藏的关系 R 是哪一种。
2. 给出一条从起点 {start} 到终点 {end} 的物流路径，路径需满足：
   - 每一步只能沿着道路移动到相邻站点
   - 对路径中每一步从站点 u 移动到站点 v，必须满足 R(v, u) 为真

你可以反复提问"R(X, Y) 是否为真？"，我会如实回答"是"或"否"。请尽可能少地提问以完成任务。

每次提问使用以下 XML 格式（X 和 Y 为站点名称）：

<query>X,Y</query>

提交最终答案时，需要同时指明关系类型和路径（或声明无法抵达）。关系类型使用以下代号：
- ancestor_inclusive: 供货上游（包含自身）
- ancestor_strict: 严格供货上游（不含自身）
- descendant_inclusive: 接收下游（包含自身）
- descendant_strict: 严格接收下游（不含自身）

答案格式如下：

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

或若无法抵达：

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's play a "Network Dispatch and Logistics Path Planning" game. Here are the rules:

The game is set on a hierarchical road network with the dispatch center at A. The network structure is:
- Stations: A, B, C, D, E, F, G, H, I
- Roads (undirected): {edges}

On this network, I have secretly chosen a binary relation R, which is one of the following four relations:
1. Supply Upstream (including self)
2. Strict Supply Upstream (excluding self)
3. Receiving Downstream (including self)
4. Strict Receiving Downstream (excluding self)

Explanation:
- Station U is a supply upstream of V if and only if U is on the unique main route from dispatch center A to V.
- Receiving downstream is the inverse of the supply upstream relation.
- "Including self" means a station satisfies the relation with itself; "strict" means excluding self.

Your goals are twofold:
1. Determine which of the four relations is the hidden relation R through queries.
2. Provide a logistics path from start station {start} to end station {end}, where the path must satisfy:
   - Each step can only move along a road to an adjacent station
   - For each step from station u to station v in the path, R(v, u) must be true

You can repeatedly ask "Is R(X, Y) true?" and I will answer "Yes" or "No" truthfully. Try to complete the task with as few queries as possible.

Use the following XML format for queries (X and Y are station names):

<query>X,Y</query>

When submitting the final answer, specify both the relation type and the path (or declare unreachable). Use these codes for relation types:
- ancestor_inclusive: Supply Upstream (including self)
- ancestor_strict: Strict Supply Upstream (excluding self)
- descendant_inclusive: Receiving Downstream (including self)
- descendant_strict: Strict Receiving Downstream (excluding self)

Answer format:

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

Or if unreachable:

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"传染病溯源与传播路径分析"游戏，规则如下：

游戏设定了一个感染传播树，零号病人（初始暴发点）所在的群组为 A。树的结构如下：
- 群组：A, B, C, D, E, F, G, H, I
- 传播链（无向）：{edges}

在这棵树上，我已秘密选择了一个二元关系 R，它是以下四种关系之一：
1. 传染源头（包含自身）
2. 严格传染源头（不含自身）
3. 衍生感染者（包含自身）
4. 严格衍生感染者（不含自身）

说明：
- 群组 U 是 V 的传染源头，当且仅当 U 位于从初始群组 A 到 V 的唯一传播链条上。
- 衍生感染者是传染源头的逆关系。
- "包含自身"表示群组与自己也满足该关系；"严格"表示不包含自身。

你的目标有两个：
1. 通过提问确定隐藏的关系 R 是哪一种。
2. 给出一条从起点 {start} 到终点 {end} 的病毒演化路径，路径需满足：
   - 每一步只能沿着传播链移动到相邻群组
   - 对路径中每一步从群组 u 移动到群组 v，必须满足 R(v, u) 为真

你可以反复提问"R(X, Y) 是否为真？"，我会如实回答"是"或"否"。请尽可能少地提问以完成任务。

每次提问使用以下 XML 格式（X 和 Y 为群组名称）：

<query>X,Y</query>

提交最终答案时，需要同时指明关系类型和路径（或声明无法抵达）。关系类型使用以下代号：
- ancestor_inclusive: 传染源头（包含自身）
- ancestor_strict: 严格传染源头（不含自身）
- descendant_inclusive: 衍生感染者（包含自身）
- descendant_strict: 严格衍生感染者（不含自身）

答案格式如下：

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

或若无法抵达：

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play an "Infectious Disease Tracing and Transmission Path Analysis" game. Here are the rules:

The game is set on an infection transmission tree, with patient zero (the initial outbreak point) at group A. The tree structure is:
- Groups: A, B, C, D, E, F, G, H, I
- Transmission Chains (undirected): {edges}

On this tree, I have secretly chosen a binary relation R, which is one of the following four relations:
1. Infection Source (including self)
2. Strict Infection Source (excluding self)
3. Derived Infected (including self)
4. Strict Derived Infected (excluding self)

Explanation:
- Group U is an infection source of V if and only if U is on the unique transmission chain from initial group A to V.
- Derived infected is the inverse of the infection source relation.
- "Including self" means a group satisfies the relation with itself; "strict" means excluding self.

Your goals are twofold:
1. Determine which of the four relations is the hidden relation R through queries.
2. Provide a viral evolution path from start group {start} to end group {end}, where the path must satisfy:
   - Each step can only move along a transmission chain to an adjacent group
   - For each step from group u to group v in the path, R(v, u) must be true

You can repeatedly ask "Is R(X, Y) true?" and I will answer "Yes" or "No" truthfully. Try to complete the task with as few queries as possible.

Use the following XML format for queries (X and Y are group names):

<query>X,Y</query>

When submitting the final answer, specify both the relation type and the path (or declare unreachable). Use these codes for relation types:
- ancestor_inclusive: Infection Source (including self)
- ancestor_strict: Strict Infection Source (excluding self)
- descendant_inclusive: Derived Infected (including self)
- descendant_strict: Strict Derived Infected (excluding self)

Answer format:

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

Or if unreachable:

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"知识图谱先决条件与学习路径规划"游戏，规则如下：

游戏设定了一个层级知识图谱，基础核心概念为 A。图谱结构如下：
- 知识模块：A, B, C, D, E, F, G, H, I
- 关联边（无向）：{edges}

在这个图谱上，我已秘密选择了一个二元关系 R，它是以下四种关系之一：
1. 先决基础（包含自身）
2. 严格先决基础（不含自身）
3. 衍生进阶（包含自身）
4. 严格衍生进阶（不含自身）

说明：
- 模块 U 是 V 的先决基础，当且仅当 U 位于从核心概念 A 到 V 的唯一学习路径上。
- 衍生进阶是先决基础的逆关系。
- "包含自身"表示模块与自己也满足该关系；"严格"表示不包含自身。

你的目标有两个：
1. 通过提问确定隐藏的关系 R 是哪一种。
2. 给出一条从起点 {start} 到终点 {end} 的学习路径，路径需满足：
   - 每一步只能沿着关联边移动到相邻模块
   - 对路径中每一步从模块 u 移动到模块 v，必须满足 R(v, u) 为真

你可以反复提问"R(X, Y) 是否为真？"，我会如实回答"是"或"否"。请尽可能少地提问以完成任务。

每次提问使用以下 XML 格式（X 和 Y 为模块名称）：

<query>X,Y</query>

提交最终答案时，需要同时指明关系类型和路径（或声明无法抵达）。关系类型使用以下代号：
- ancestor_inclusive: 先决基础（包含自身）
- ancestor_strict: 严格先决基础（不含自身）
- descendant_inclusive: 衍生进阶（包含自身）
- descendant_strict: 严格衍生进阶（不含自身）

答案格式如下：

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

或若无法抵达：

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Graph Prerequisites and Learning Path Planning" game. Here are the rules:

The game is set on a hierarchical knowledge graph, with the core foundational concept at A. The graph structure is:
- Knowledge Modules: A, B, C, D, E, F, G, H, I
- Association Edges (undirected): {edges}

On this graph, I have secretly chosen a binary relation R, which is one of the following four relations:
1. Prerequisite Foundation (including self)
2. Strict Prerequisite Foundation (excluding self)
3. Derived Advanced (including self)
4. Strict Derived Advanced (excluding self)

Explanation:
- Module U is a prerequisite foundation of V if and only if U is on the unique learning path from core concept A to V.
- Derived advanced is the inverse of the prerequisite foundation relation.
- "Including self" means a module satisfies the relation with itself; "strict" means excluding self.

Your goals are twofold:
1. Determine which of the four relations is the hidden relation R through queries.
2. Provide a learning path from start module {start} to end module {end}, where the path must satisfy:
   - Each step can only move along an association edge to an adjacent module
   - For each step from module u to module v in the path, R(v, u) must be true

You can repeatedly ask "Is R(X, Y) true?" and I will answer "Yes" or "No" truthfully. Try to complete the task with as few queries as possible.

Use the following XML format for queries (X and Y are module names):

<query>X,Y</query>

When submitting the final answer, specify both the relation type and the path (or declare unreachable). Use these codes for relation types:
- ancestor_inclusive: Prerequisite Foundation (including self)
- ancestor_strict: Strict Prerequisite Foundation (excluding self)
- descendant_inclusive: Derived Advanced (including self)
- descendant_strict: Strict Derived Advanced (excluding self)

Answer format:

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

Or if unreachable:

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"产品BOM层级与装配路径追踪"游戏，规则如下：

游戏设定了一个产品物料清单（BOM）树，最终成品为 A。树的结构如下：
- 组件/零件：A, B, C, D, E, F, G, H, I
- 装配边（无向）：{edges}

在这棵树上，我已秘密选择了一个二元关系 R，它是以下四种关系之一：
1. 所属总成（包含自身）
2. 严格所属总成（不含自身）
3. 组成部件（包含自身）
4. 严格组成部件（不含自身）

说明：
- 节点 U 是 V 的所属总成，当且仅当 U 位于从最终成品 A 到节点 V 的唯一拆解层级路径上。
- 组成部件是所属总成的逆关系。
- "包含自身"表示节点与自己也满足该关系；"严格"表示不包含自身。

你的目标有两个：
1. 通过提问确定隐藏的关系 R 是哪一种。
2. 给出一条从起点 {start} 到终点 {end} 的追溯路径，路径需满足：
   - 每一步只能沿着装配边移动到相邻节点
   - 对路径中每一步从节点 u 移动到节点 v，必须满足 R(v, u) 为真

你可以反复提问"R(X, Y) 是否为真？"，我会如实回答"是"或"否"。请尽可能少地提问以完成任务。

每次提问使用以下 XML 格式（X 和 Y 为组件/零件名称）：

<query>X,Y</query>

提交最终答案时，需要同时指明关系类型和路径（或声明无法抵达）。关系类型使用以下代号：
- ancestor_inclusive: 所属总成（包含自身）
- ancestor_strict: 严格所属总成（不含自身）
- descendant_inclusive: 组成部件（包含自身）
- descendant_strict: 严格组成部件（不含自身）

答案格式如下：

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

或若无法抵达：

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's play a "Product BOM Hierarchy and Assembly Path Tracing" game. Here are the rules:

The game is set on a product Bill of Materials (BOM) tree, with the final product at A. The tree structure is:
- Components/Parts: A, B, C, D, E, F, G, H, I
- Assembly Edges (undirected): {edges}

On this tree, I have secretly chosen a binary relation R, which is one of the following four relations:
1. Parent Assembly (including self)
2. Strict Parent Assembly (excluding self)
3. Constituent Part (including self)
4. Strict Constituent Part (excluding self)

Explanation:
- Node U is a parent assembly of V if and only if U is on the unique disassembly hierarchical path from the final product A to node V.
- Constituent part is the inverse of the parent assembly relation.
- "Including self" means a node satisfies the relation with itself; "strict" means excluding self.

Your goals are twofold:
1. Determine which of the four relations is the hidden relation R through queries.
2. Provide a tracing path from start node {start} to end node {end}, where the path must satisfy:
   - Each step can only move along an assembly edge to an adjacent node
   - For each step from node u to node v in the path, R(v, u) must be true

You can repeatedly ask "Is R(X, Y) true?" and I will answer "Yes" or "No" truthfully. Try to complete the task with as few queries as possible.

Use the following XML format for queries (X and Y are node names):

<query>X,Y</query>

When submitting the final answer, specify both the relation type and the path (or declare unreachable). Use these codes for relation types:
- ancestor_inclusive: Parent Assembly (including self)
- ancestor_strict: Strict Parent Assembly (excluding self)
- descendant_inclusive: Constituent Part (including self)
- descendant_strict: Strict Constituent Part (excluding self)

Answer format:

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

Or if unreachable:

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"公司股权穿透与资金流向审查"游戏，规则如下：

游戏设定了一个复杂的企业集团控制树，最终控股母公司为 A。树的结构如下：
- 企业主体：A, B, C, D, E, F, G, H, I
- 股权关联（无向）：{edges}

在这个集团树上，我已秘密选择了一个二元关系 R，它是以下四种关系之一：
1. 控股母公司（包含自身）
2. 严格控股母公司（不含自身）
3. 附属子公司（包含自身）
4. 严格附属子公司（不含自身）

说明：
- 主体 U 是 V 的控股母公司，当且仅当 U 位于从最终母公司 A 到 V 的唯一股权控制链条上。
- 附属子公司是控股母公司的逆关系。
- "包含自身"表示主体与自己也满足该关系；"严格"表示不包含自身。

你的目标有两个：
1. 通过提问确定隐藏的关系 R 是哪一种。
2. 给出一条从起点 {start} 到终点 {end} 的资金审计路径，路径需满足：
   - 每一步只能沿着股权关联移动到相邻企业主体
   - 对路径中每一步从主体 u 移动到主体 v，必须满足 R(v, u) 为真

你可以反复提问"R(X, Y) 是否为真？"，我会如实回答"是"或"否"。请尽可能少地提问以完成任务。

每次提问使用以下 XML 格式（X 和 Y 为企业主体名称）：

<query>X,Y</query>

提交最终答案时，需要同时指明关系类型和路径（或声明无法抵达）。关系类型使用以下代号：
- ancestor_inclusive: 控股母公司（包含自身）
- ancestor_strict: 严格控股母公司（不含自身）
- descendant_inclusive: 附属子公司（包含自身）
- descendant_strict: 严格附属子公司（不含自身）

答案格式如下：

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

或若无法抵达：

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Corporate Equity Penetration and Fund Flow Audit" game. Here are the rules:

The game is set on a complex corporate group control tree, with the ultimate holding parent company at A. The tree structure is:
- Corporate Entities: A, B, C, D, E, F, G, H, I
- Equity Associations (undirected): {edges}

On this group tree, I have secretly chosen a binary relation R, which is one of the following four relations:
1. Holding Parent Company (including self)
2. Strict Holding Parent Company (excluding self)
3. Subsidiary Company (including self)
4. Strict Subsidiary Company (excluding self)

Explanation:
- Entity U is a holding parent company of V if and only if U is on the unique equity control chain from the ultimate parent company A to V.
- Subsidiary company is the inverse of the holding parent company relation.
- "Including self" means an entity satisfies the relation with itself; "strict" means excluding self.

Your goals are twofold:
1. Determine which of the four relations is the hidden relation R through queries.
2. Provide a fund audit path from start entity {start} to end entity {end}, where the path must satisfy:
   - Each step can only move along an equity association to an adjacent entity
   - For each step from entity u to entity v in the path, R(v, u) must be true

You can repeatedly ask "Is R(X, Y) true?" and I will answer "Yes" or "No" truthfully. Try to complete the task with as few queries as possible.

Use the following XML format for queries (X and Y are entity names):

<query>X,Y</query>

When submitting the final answer, specify both the relation type and the path (or declare unreachable). Use these codes for relation types:
- ancestor_inclusive: Holding Parent Company (including self)
- ancestor_strict: Strict Holding Parent Company (excluding self)
- descendant_inclusive: Subsidiary Company (including self)
- descendant_strict: Strict Subsidiary Company (excluding self)

Answer format:

<answer>relation=ancestor_inclusive, path=I,H,E,B,A</answer>

Or if unreachable:

<answer>relation=descendant_strict, path=unreachable</answer>
"""

    tags = ["answer", "query"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    TREE_EDGES = [
        ("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"),
        ("C", "F"), ("E", "G"), ("E", "H"), ("H", "I")
    ]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "relation": "ancestor_inclusive",
                "start": "I",
                "end": "A",
                "expected_path": ["I", "H", "E", "B", "A"]
            },
            2: {
                "relation": "descendant_inclusive",
                "start": "A",
                "end": "I",
                "expected_path": ["A", "B", "E", "H", "I"]
            },
            3: {
                "relation": "ancestor_strict",
                "start": "I",
                "end": "A",
                "expected_path": ["I", "H", "E", "B", "A"]
            },
            4: {
                "relation": "descendant_strict",
                "start": "I",
                "end": "A",
                "expected_path": None
            },
            5: {
                "relation": "ancestor_inclusive",
                "start": "D",
                "end": "F",
                "expected_path": None
            }
        },
        "en": {
            1: {
                "relation": "ancestor_inclusive",
                "start": "I",
                "end": "A",
                "expected_path": ["I", "H", "E", "B", "A"]
            },
            2: {
                "relation": "descendant_inclusive",
                "start": "A",
                "end": "I",
                "expected_path": ["A", "B", "E", "H", "I"]
            },
            3: {
                "relation": "ancestor_strict",
                "start": "I",
                "end": "A",
                "expected_path": ["I", "H", "E", "B", "A"]
            },
            4: {
                "relation": "descendant_strict",
                "start": "I",
                "end": "A",
                "expected_path": None
            },
            5: {
                "relation": "ancestor_inclusive",
                "start": "D",
                "end": "F",
                "expected_path": None
            }
        }
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
        
        self.adjacency = {}
        for u, v in self.TREE_EDGES:
            if u not in self.adjacency:
                self.adjacency[u] = []
            if v not in self.adjacency:
                self.adjacency[v] = []
            self.adjacency[u].append(v)
            self.adjacency[v].append(u)
        
        self.parent = {}
        self.ancestors = {}
        
        self._build_tree_structure()
        
        self.hidden_relation = cfg["relation"]
        self.start_node = cfg["start"]
        self.end_node = cfg["end"]
        self.expected_path = cfg["expected_path"]
        
        edges_str = ", ".join([f"{u}-{v}" for u, v in self.TREE_EDGES])
        self._game_info = {
            "edges": edges_str,
            "start": self.start_node,
            "end": self.end_node
        }

    def _build_tree_structure(self):
        from collections import deque
        
        root = "A"
        visited = {root}
        queue = deque([root])
        self.parent[root] = None
        self.ancestors[root] = {root}
        
        while queue:
            u = queue.popleft()
            for v in self.adjacency[u]:
                if v not in visited:
                    visited.add(v)
                    self.parent[v] = u
                    self.ancestors[v] = self.ancestors[u] | {v}
                    queue.append(v)

    def _check_relation(self, x, y):
        if x == y:
            return "inclusive" in self.hidden_relation
        
        is_x_ancestor_of_y = x in self.ancestors[y] and x != y
        is_y_ancestor_of_x = y in self.ancestors[x] and y != x
        
        if self.hidden_relation == "ancestor_inclusive":
            return is_x_ancestor_of_y or (x == y)
        elif self.hidden_relation == "ancestor_strict":
            return is_x_ancestor_of_y
        elif self.hidden_relation == "descendant_inclusive":
            return is_y_ancestor_of_x or (x == y)
        elif self.hidden_relation == "descendant_strict":
            return is_y_ancestor_of_x
        
        return False

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        rel_match = re.search(r"relation\s*=\s*([^,\s]+)", raw_ans)
        path_match = re.search(r"path\s*=\s*(.*)", raw_ans)
        
        if not rel_match or not path_match:
            return False
            
        model_relation = rel_match.group(1).strip()
        path_str = path_match.group(1).strip()
        
        if model_relation != self.hidden_relation:
            return False
        
        if path_str.lower() == "unreachable":
            return self.expected_path is None
        
        if self.expected_path is None:
            return False
        
        try:
            model_path = [node.strip() for node in path_str.split(",") if node.strip()]
        except:
            return False
            
        all_nodes = set(self.adjacency.keys())
        
        for node in model_path:
            if node not in all_nodes:
                return False
        
        if len(model_path) < 2:
            return False
        if model_path[0] != self.start_node or model_path[-1] != self.end_node:
            return False
        
        for i in range(len(model_path) - 1):
            u = model_path[i]
            v = model_path[i + 1]
            
            if v not in self.adjacency.get(u, []):
                return False
            
            if not self._check_relation(v, u):
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No query tag found.")
        
        query_str = parsed_info["query"].strip()
        
        try:
            parts = [x.strip() for x in query_str.split(",")]
            if len(parts) != 2:
                raise ValueError("Query must contain exactly two nodes.")
            
            x, y = parts[0], parts[1]
            
            all_nodes = set(self.adjacency.keys())
            if x not in all_nodes or y not in all_nodes:
                if self.config.language == "zh":
                    return "错误：无效的节点名称。"
                else:
                    return "Error: Invalid node name."
            
            result = self._check_relation(x, y)
            
            if self.config.language == "zh":
                return "是" if result else "否"
            else:
                return "Yes" if result else "No"
                
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：查询格式无效。"
            else:
                return f"Error: Invalid query format."

    def _cf_make_wrong(self, correct: str) -> str:
        if str(correct).isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是": return "否"
            if correct == "否": return "是"
            
        if correct.lower() == "yes": return "No"
        if correct.lower() == "no": return "Yes"
        
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        nodes = sorted(list(self.adjacency.keys()))
        
        for x in nodes:
            for y in nodes:
                query_str = f"<query>{x},{y}</query>"
                
                result = self._check_relation(x, y)
                
                if self.config.language == "zh":
                    ans_str = "是" if result else "否"
                else:
                    ans_str = "Yes" if result else "No"
                
                queries.append({
                    "query": query_str,
                    "answer": ans_str
                })
        
        return queries