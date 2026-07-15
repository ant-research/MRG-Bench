import re
from typing import Dict, List, Tuple, Set
from .base import Game

class TreeAttributeGame(Game):

    game_rule_zh = """\
我们来玩一个"树节点属性推理"游戏。规则如下：

给定一棵有根树，共有 {n} 个节点，编号为 1 到 {n}，根节点为 {root}。

对于任一节点 u，定义以下特征：
- Depth(u)：节点 u 到根节点的边数（根节点为 0）
- Child(u)：节点 u 的直接子节点数量
- Subtree(u)：以 u 为根的子树节点总数（包含 u 自身）
- Leaf(u)：以 u 为根的子树中叶子节点（无子节点的节点）的数量

记特征向量 x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u))，其每个分量在模 5 意义下取值（即取值范围为 0 到 4）。

存在一个隐藏的参数向量 c = (c0, c1, c2, c3, c4)，每个分量也在模 5 意义下取值。节点的属性值定义为：
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

已指定目标节点为 {target}。你的任务是推断出目标节点的属性值 Attr({target})。

你可以进行以下两种查询：

1. **特征查询**（不计入查询次数）：查询任意节点 u 的特征值，返回 (Depth(u), Child(u), Subtree(u), Leaf(u))。

2. **属性查询**（计入查询次数）：查询任意节点 u（u 不能是目标节点 {target}）的属性值，返回 Attr(u)，取值为 0 到 4 之间的整数。你最多可以进行 {max_queries} 次属性查询。

- 特征查询（例如查询节点 3）：
<query_feature>3</query_feature>

- 属性查询（例如查询节点 5）：
<query_attribute>5</query_attribute>

当你收集到足够信息后，提交你对目标节点属性值的预测（必须是 0 到 4 之间的整数）：

<answer>2</answer>

注意：
- 树的结构在游戏开始时已知（你可以通过特征查询获取）
- 属性查询有次数限制，请谨慎使用
- 不能对目标节点进行属性查询
- 答案格式错误或答案错误都会导致游戏失败
"""

    game_rule_en = """\
Let's play a "Tree Node Attribute Inference" game. Here are the rules:

Given a rooted tree with {n} nodes, numbered from 1 to {n}, with root node {root}.

For any node u, we define the following features:
- Depth(u): Number of edges from node u to the root (root has depth 0)
- Child(u): Number of direct children of node u
- Subtree(u): Total number of nodes in the subtree rooted at u (including u itself)
- Leaf(u): Number of leaf nodes (nodes with no children) in the subtree rooted at u

Let the feature vector x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u)), where each component is taken modulo 5 (values from 0 to 4).

There exists a hidden parameter vector c = (c0, c1, c2, c3, c4), with each component also in modulo 5. The attribute value of a node is defined as:
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

The target node is {target}. Your task is to infer the attribute value Attr({target}).

You can perform the following two types of queries:

1. **Feature Query** (does not count toward query limit): Query the feature values of any node u, returns (Depth(u), Child(u), Subtree(u), Leaf(u)).

2. **Attribute Query** (counts toward query limit): Query the attribute value of any node u (u cannot be the target node {target}), returns Attr(u), an integer from 0 to 4. You can perform at most {max_queries} attribute queries.

- Feature Query (e.g., querying node 3):
<query_feature>3</query_feature>

- Attribute Query (e.g., querying node 5):
<query_attribute>5</query_attribute>

When you have gathered enough information, submit your prediction for the target node's attribute value (must be an integer from 0 to 4):

<answer>2</answer>

Note:
- The tree structure is known at the start of the game (you can obtain it via feature queries)
- Attribute queries have a limit, use them wisely
- You cannot query the target node's attribute
- Invalid format or incorrect answer will result in game failure
"""

    contextualized_rule_zh_1 = """\
我们要进行一次城市路网的拥堵评级推演。规则如下：

给定一个树形交通路网，共有 {n} 个路口，编号为 1 到 {n}，市中心主枢纽为根节点 {root}。

对于任一路口 u，定义以下拓扑特征：
- Depth(u)：路口 u 到主枢纽的道路级数（根节点为 0）
- Child(u)：路口 u 直接连接的下级路口数量
- Subtree(u)：以 u 为起点的路网分支中路口总数（包含 u 自身）
- Leaf(u)：以 u 为起点的分支中尽头路口（无下级路口）的数量

记特征向量 x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u))，其每个分量在模 5 意义下取值（即取值范围为 0 到 4）。

存在一个隐藏的系统参数向量 c = (c0, c1, c2, c3, c4)，每个分量也在模 5 意义下取值。路口的拥堵指数评级（属性值）定义为：
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

已指定目标路口为 {target}。你的任务是推断出目标路口的拥堵指数评级 Attr({target})。

你可以进行以下两种查询：

1. **特征查询**（不计入查询次数）：查询任意路口 u 的拓扑特征值，返回 (Depth(u), Child(u), Subtree(u), Leaf(u))。

2. **属性查询**（计入查询次数）：查询任意路口 u（u 不能是目标路口 {target}）的拥堵指数评级，返回 Attr(u)，取值为 0 到 4 之间的整数。你最多可以进行 {max_queries} 次属性查询。

- 特征查询（例如查询路口 3）：
<query_feature>3</query_feature>

- 属性查询（例如查询路口 5）：
<query_attribute>5</query_attribute>

当你收集到足够信息后，提交你对目标路口拥堵评级的预测（必须是 0 到 4 之间的整数）：

<answer>2</answer>

注意：
- 路网拓扑结构在评估开始时已知（你可以通过特征查询获取）
- 属性查询有次数限制，请谨慎使用
- 不能对目标路口进行属性查询
- 答案格式错误或答案错误都会导致评估失败
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
We are conducting a congestion rating inference for an urban road network. Here are the rules:

Given a tree-structured road network with {n} intersections, numbered from 1 to {n}, with the city center main hub as the root node {root}.

For any intersection u, we define the following topological features:
- Depth(u): Number of road levels from intersection u to the main hub (root has depth 0)
- Child(u): Number of direct lower-level intersections connected to u
- Subtree(u): Total number of intersections in the network branch starting at u (including u itself)
- Leaf(u): Number of dead-end intersections (with no lower-level connections) in the branch starting at u

Let the feature vector x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u)), where each component is taken modulo 5 (values from 0 to 4).

There exists a hidden system parameter vector c = (c0, c1, c2, c3, c4), with each component also in modulo 5. The congestion index rating (attribute value) of an intersection is defined as:
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

The target intersection is {target}. Your task is to infer the congestion index rating Attr({target}) for the target intersection.

You can perform the following two types of queries:

1. **Feature Query** (does not count toward query limit): Query the topological feature values of any intersection u, returns (Depth(u), Child(u), Subtree(u), Leaf(u)).

2. **Attribute Query** (counts toward query limit): Query the congestion index rating of any intersection u (u cannot be the target intersection {target}), returns Attr(u), an integer from 0 to 4. You can perform at most {max_queries} attribute queries.

- Feature Query (e.g., querying intersection 3):
<query_feature>3</query_feature>

- Attribute Query (e.g., querying intersection 5):
<query_attribute>5</query_attribute>

When you have gathered enough information, submit your prediction for the target intersection's congestion rating (must be an integer from 0 to 4):

<answer>2</answer>

Note:
- The network topology is known at the start of the assessment (you can obtain it via feature queries)
- Attribute queries have a limit, use them wisely
- You cannot query the target intersection's rating
- Invalid format or incorrect answer will result in assessment failure
"""

    contextualized_rule_zh_2 = """\
我们要进行一次病毒传播链的风险评级推演。规则如下：

给定一个树形传播链，共有 {n} 名感染者，编号为 1 到 {n}，零号病人为根节点 {root}。

对于任一患者 u，定义以下传播特征：
- Depth(u)：患者 u 距离零号病人的传播代数（根节点为 0）
- Child(u)：患者 u 直接传染的人数
- Subtree(u)：以 u 为源头的后续感染总人数（包含 u 自身）
- Leaf(u)：以 u 为源头的传播链中终端患者（未进一步传染他人）的数量

记特征向量 x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u))，其每个分量在模 5 意义下取值（即取值范围为 0 到 4）。

存在一个隐藏的病毒突变参数向量 c = (c0, c1, c2, c3, c4)，每个分量也在模 5 意义下取值。患者的变异风险等级（属性值）定义为：
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

已指定目标患者为 {target}。你的任务是推断出目标患者的变异风险等级 Attr({target})。

你可以进行以下两种查询：

1. **特征查询**（不计入查询次数）：查询任意患者 u 的传播特征值，返回 (Depth(u), Child(u), Subtree(u), Leaf(u))。

2. **属性查询**（计入查询次数）：查询任意患者 u（u 不能是目标患者 {target}）的变异风险等级，返回 Attr(u)，取值为 0 到 4 之间的整数。你最多可以进行 {max_queries} 次属性查询。

- 特征查询（例如查询患者 3）：
<query_feature>3</query_feature>

- 属性查询（例如查询患者 5）：
<query_attribute>5</query_attribute>

当你收集到足够信息后，提交你对目标患者风险等级的预测（必须是 0 到 4 之间的整数）：

<answer>2</answer>

注意：
- 传播链结构在评估开始时已知（你可以通过特征查询获取）
- 属性查询有次数限制，请谨慎使用
- 不能对目标患者进行属性查询
- 答案格式错误或答案错误都会导致评估失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are conducting a risk rating inference for a virus transmission chain. Here are the rules:

Given a tree-structured transmission chain with {n} infected individuals, numbered from 1 to {n}, with patient zero as the root node {root}.

For any patient u, we define the following transmission features:
- Depth(u): Number of transmission generations from patient zero to patient u (root has depth 0)
- Child(u): Number of individuals directly infected by patient u
- Subtree(u): Total number of subsequent infections originating from u (including u itself)
- Leaf(u): Number of terminal patients (who did not infect anyone else) in the transmission chain originating from u

Let the feature vector x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u)), where each component is taken modulo 5 (values from 0 to 4).

There exists a hidden viral mutation parameter vector c = (c0, c1, c2, c3, c4), with each component also in modulo 5. The mutation risk rating (attribute value) of a patient is defined as:
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

The target patient is {target}. Your task is to infer the mutation risk rating Attr({target}) for the target patient.

You can perform the following two types of queries:

1. **Feature Query** (does not count toward query limit): Query the transmission feature values of any patient u, returns (Depth(u), Child(u), Subtree(u), Leaf(u)).

2. **Attribute Query** (counts toward query limit): Query the mutation risk rating of any patient u (u cannot be the target patient {target}), returns Attr(u), an integer from 0 to 4. You can perform at most {max_queries} attribute queries.

- Feature Query (e.g., querying patient 3):
<query_feature>3</query_feature>

- Attribute Query (e.g., querying patient 5):
<query_attribute>5</query_attribute>

When you have gathered enough information, submit your prediction for the target patient's risk rating (must be an integer from 0 to 4):

<answer>2</answer>

Note:
- The transmission chain structure is known at the start of the assessment (you can obtain it via feature queries)
- Attribute queries have a limit, use them wisely
- You cannot query the target patient's rating
- Invalid format or incorrect answer will result in assessment failure
"""

    contextualized_rule_zh_3 = """\
我们要进行一次知识图谱的核心难度推演。规则如下：

给定一个树形知识结构，共有 {n} 个知识点，编号为 1 到 {n}，学科核心概念为根节点 {root}。

对于任一知识点 u，定义以下结构特征：
- Depth(u)：知识点 u 距离核心概念的层级深度（根节点为 0）
- Child(u)：知识点 u 直接包含的子知识点数量
- Subtree(u)：以 u 为前置的知识分支中知识点总数（包含 u 自身）
- Leaf(u)：以 u 为前置的分支中基础知识点（无进一步细分）的数量

记特征向量 x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u))，其每个分量在模 5 意义下取值（即取值范围为 0 到 4）。

存在一个隐藏的难度评估参数向量 c = (c0, c1, c2, c3, c4)，每个分量也在模 5 意义下取值。知识点的考核难度星级（属性值）定义为：
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

已指定目标知识点为 {target}。你的任务是推断出目标知识点的考核难度星级 Attr({target})。

你可以进行以下两种查询：

1. **特征查询**（不计入查询次数）：查询任意知识点 u 的结构特征值，返回 (Depth(u), Child(u), Subtree(u), Leaf(u))。

2. **属性查询**（计入查询次数）：查询任意知识点 u（u 不能是目标知识点 {target}）的考核难度星级，返回 Attr(u)，取值为 0 到 4 之间的整数。你最多可以进行 {max_queries} 次属性查询。

- 特征查询（例如查询知识点 3）：
<query_feature>3</query_feature>

- 属性查询（例如查询知识点 5）：
<query_attribute>5</query_attribute>

当你收集到足够信息后，提交你对目标知识点难度星级的预测（必须是 0 到 4 之间的整数）：

<answer>2</answer>

注意：
- 知识图谱结构在评估开始时已知（你可以通过特征查询获取）
- 属性查询有次数限制，请谨慎使用
- 不能对目标知识点进行属性查询
- 答案格式错误或答案错误都会导致评估失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are conducting a core difficulty inference for a knowledge graph. Here are the rules:

Given a tree-structured knowledge graph with {n} knowledge points, numbered from 1 to {n}, with the discipline's core concept as the root node {root}.

For any knowledge point u, we define the following structural features:
- Depth(u): The hierarchical depth from the core concept to knowledge point u (root has depth 0)
- Child(u): Number of sub-knowledge points directly contained by u
- Subtree(u): Total number of knowledge points in the branch starting from u (including u itself)
- Leaf(u): Number of fundamental knowledge points (with no further subdivisions) in the branch starting from u

Let the feature vector x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u)), where each component is taken modulo 5 (values from 0 to 4).

There exists a hidden difficulty evaluation parameter vector c = (c0, c1, c2, c3, c4), with each component also in modulo 5. The assessment difficulty star rating (attribute value) of a knowledge point is defined as:
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

The target knowledge point is {target}. Your task is to infer the assessment difficulty star rating Attr({target}) for the target knowledge point.

You can perform the following two types of queries:

1. **Feature Query** (does not count toward query limit): Query the structural feature values of any knowledge point u, returns (Depth(u), Child(u), Subtree(u), Leaf(u)).

2. **Attribute Query** (counts toward query limit): Query the assessment difficulty star rating of any knowledge point u (u cannot be the target knowledge point {target}), returns Attr(u), an integer from 0 to 4. You can perform at most {max_queries} attribute queries.

- Feature Query (e.g., querying knowledge point 3):
<query_feature>3</query_feature>

- Attribute Query (e.g., querying knowledge point 5):
<query_attribute>5</query_attribute>

When you have gathered enough information, submit your prediction for the target knowledge point's difficulty star rating (must be an integer from 0 to 4):

<answer>2</answer>

Note:
- The knowledge graph structure is known at the start of the assessment (you can obtain it via feature queries)
- Attribute queries have a limit, use them wisely
- You cannot query the target knowledge point's rating
- Invalid format or incorrect answer will result in assessment failure
"""

    contextualized_rule_zh_4 = """\
我们要进行一次产品物料清单(BOM)的供应链风险推演。规则如下：

给定一个树形产品装配结构，共有 {n} 个组件，编号为 1 到 {n}，最终成品为根节点 {root}。

对于任一组件 u，定义以下装配特征：
- Depth(u)：组件 u 在装配层级中的深度（根节点为 0）
- Child(u)：组装组件 u 直接需要的子组件数量
- Subtree(u)：以组件 u 为根的装配分支中所有组件总数（包含 u 自身）
- Leaf(u)：以组件 u 为根的分支中不可再分的基础零件数量

记特征向量 x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u))，其每个分量在模 5 意义下取值（即取值范围为 0 到 4）。

存在一个隐藏的供应链风险参数向量 c = (c0, c1, c2, c3, c4)，每个分量也在模 5 意义下取值。组件的供应链风险等级（属性值）定义为：
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

已指定目标组件为 {target}。你的任务是推断出目标组件的供应链风险等级 Attr({target})。

你可以进行以下两种查询：

1. **特征查询**（不计入查询次数）：查询任意组件 u 的装配特征值，返回 (Depth(u), Child(u), Subtree(u), Leaf(u))。

2. **属性查询**（计入查询次数）：查询任意组件 u（u 不能是目标组件 {target}）的供应链风险等级，返回 Attr(u)，取值为 0 到 4 之间的整数。你最多可以进行 {max_queries} 次属性查询。

- 特征查询（例如查询组件 3）：
<query_feature>3</query_feature>

- 属性查询（例如查询组件 5）：
<query_attribute>5</query_attribute>

当你收集到足够信息后，提交你对目标组件风险等级的预测（必须是 0 到 4 之间的整数）：

<answer>2</answer>

注意：
- 产品装配结构在评估开始时已知（你可以通过特征查询获取）
- 属性查询有次数限制，请谨慎使用
- 不能对目标组件进行属性查询
- 答案格式错误或答案错误都会导致评估失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
We are conducting a supply chain risk inference for a product Bill of Materials (BOM). Here are the rules:

Given a tree-structured product assembly structure with {n} components, numbered from 1 to {n}, with the final product as the root node {root}.

For any component u, we define the following assembly features:
- Depth(u): The depth of component u in the assembly hierarchy (root has depth 0)
- Child(u): Number of sub-components directly required to assemble u
- Subtree(u): Total number of components in the assembly branch rooted at u (including u itself)
- Leaf(u): Number of indivisible basic parts in the branch rooted at u

Let the feature vector x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u)), where each component is taken modulo 5 (values from 0 to 4).

There exists a hidden supply chain risk parameter vector c = (c0, c1, c2, c3, c4), with each component also in modulo 5. The supply chain risk rating (attribute value) of a component is defined as:
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

The target component is {target}. Your task is to infer the supply chain risk rating Attr({target}) for the target component.

You can perform the following two types of queries:

1. **Feature Query** (does not count toward query limit): Query the assembly feature values of any component u, returns (Depth(u), Child(u), Subtree(u), Leaf(u)).

2. **Attribute Query** (counts toward query limit): Query the supply chain risk rating of any component u (u cannot be the target component {target}), returns Attr(u), an integer from 0 to 4. You can perform at most {max_queries} attribute queries.

- Feature Query (e.g., querying component 3):
<query_feature>3</query_feature>

- Attribute Query (e.g., querying component 5):
<query_attribute>5</query_attribute>

When you have gathered enough information, submit your prediction for the target component's risk rating (must be an integer from 0 to 4):

<answer>2</answer>

Note:
- The product assembly structure is known at the start of the assessment (you can obtain it via feature queries)
- Attribute queries have a limit, use them wisely
- You cannot query the target component's rating
- Invalid format or incorrect answer will result in assessment failure
"""

    contextualized_rule_zh_5 = """\
我们要进行一次公司股权架构穿透的审查优先级推演。规则如下：

给定一个树形股权控制结构，共有 {n} 个实体，编号为 1 到 {n}，最终母公司为根节点 {root}。

对于任一实体 u，定义以下穿透特征：
- Depth(u)：实体 u 距离母公司的投资链层级（根节点为 0）
- Child(u)：实体 u 直接投资的子实体数量
- Subtree(u)：实体 u 控制的投资分支中所有实体总数（包含 u 自身）
- Leaf(u)：实体 u 控制的分支中无对外投资的底层实体数量

记特征向量 x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u))，其每个分量在模 5 意义下取值（即取值范围为 0 到 4）。

存在一个隐藏的合规审查参数向量 c = (c0, c1, c2, c3, c4)，每个分量也在模 5 意义下取值。实体的合规审查优先级（属性值）定义为：
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

已指定目标实体为 {target}。你的任务是推断出目标实体的合规审查优先级 Attr({target})。

你可以进行以下两种查询：

1. **特征查询**（不计入查询次数）：查询任意实体 u 的穿透特征值，返回 (Depth(u), Child(u), Subtree(u), Leaf(u))。

2. **属性查询**（计入查询次数）：查询任意实体 u（u 不能是目标实体 {target}）的合规审查优先级，返回 Attr(u)，取值为 0 到 4 之间的整数。你最多可以进行 {max_queries} 次属性查询。

- 特征查询（例如查询实体 3）：
<query_feature>3</query_feature>

- 属性查询（例如查询实体 5）：
<query_attribute>5</query_attribute>

当你收集到足够信息后，提交你对目标实体审查优先级的预测（必须是 0 到 4 之间的整数）：

<answer>2</answer>

注意：
- 股权控制结构在评估开始时已知（你可以通过特征查询获取）
- 属性查询有次数限制，请谨慎使用
- 不能对目标实体进行属性查询
- 答案格式错误或答案错误都会导致评估失败
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are conducting a compliance review priority inference for a corporate equity structure. Here are the rules:

Given a tree-structured equity control network with {n} entities, numbered from 1 to {n}, with the ultimate parent company as the root node {root}.

For any entity u, we define the following penetration features:
- Depth(u): The investment chain level from the parent company to entity u (root has depth 0)
- Child(u): Number of subsidiary entities directly invested in by u
- Subtree(u): Total number of entities in the investment branch controlled by u (including u itself)
- Leaf(u): Number of bottom-level entities (with no outward investments) in the branch controlled by u

Let the feature vector x(u) = (1, Depth(u), Child(u), Subtree(u), Leaf(u)), where each component is taken modulo 5 (values from 0 to 4).

There exists a hidden compliance review parameter vector c = (c0, c1, c2, c3, c4), with each component also in modulo 5. The compliance review priority (attribute value) of an entity is defined as:
Attr(u) = (c0 × 1 + c1 × Depth(u) + c2 × Child(u) + c3 × Subtree(u) + c4 × Leaf(u)) mod 5

The target entity is {target}. Your task is to infer the compliance review priority Attr({target}) for the target entity.

You can perform the following two types of queries:

1. **Feature Query** (does not count toward query limit): Query the penetration feature values of any entity u, returns (Depth(u), Child(u), Subtree(u), Leaf(u)).

2. **Attribute Query** (counts toward query limit): Query the compliance review priority of any entity u (u cannot be the target entity {target}), returns Attr(u), an integer from 0 to 4. You can perform at most {max_queries} attribute queries.

- Feature Query (e.g., querying entity 3):
<query_feature>3</query_feature>

- Attribute Query (e.g., querying entity 5):
<query_attribute>5</query_attribute>

When you have gathered enough information, submit your prediction for the target entity's review priority (must be an integer from 0 to 4):

<answer>2</answer>

Note:
- The equity control structure is known at the start of the assessment (you can obtain it via feature queries)
- Attribute queries have a limit, use them wisely
- You cannot query the target entity's priority
- Invalid format or incorrect answer will result in assessment failure
"""

    user_prompt_zh = "游戏开始，你可以开始查询了。"
    user_prompt_en = "Game started. You may begin querying."

    tags = ["answer", "query_feature", "query_attribute"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        1: {
            "n": 5,
            "root": 1,
            "target": 4,
            "max_queries": 7,
            "edges": [(1, 2), (1, 3), (2, 4), (2, 5)],
            "params": [1, 2, 3, 1, 4],
        },
        2: {
            "n": 7,
            "root": 1,
            "target": 5,
            "max_queries": 6,
            "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            "params": [2, 1, 4, 2, 3],
        },
        3: {
            "n": 10,
            "root": 1,
            "target": 7,
            "max_queries": 6,
            "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (4, 9), (4, 10)],
            "params": [3, 2, 1, 3, 2],
        },
        4: {
            "n": 12,
            "root": 1,
            "target": 9,
            "max_queries": 5,
            "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (2, 6), (3, 7), (3, 8), (5, 9), (5, 10), (7, 11), (7, 12)],
            "params": [4, 3, 2, 1, 4],
        },
        5: {
            "n": 15,
            "root": 1,
            "target": 12,
            "max_queries": 5,
            "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (3, 9), 
                     (4, 10), (6, 11), (6, 12), (8, 13), (10, 14), (10, 15)],
            "params": [1, 4, 3, 2, 1],
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self._game_info["target"] = cfg["target"]
        self._game_info["max_queries"] = cfg["max_queries"]

        self.n = cfg["n"]
        self.root = cfg["root"]
        self.target = cfg["target"]
        self.max_queries = cfg["max_queries"]
        self.params = cfg["params"]
        
        self.children: Dict[int, List[int]] = {i: [] for i in range(1, self.n + 1)}
        for parent, child in cfg["edges"]:
            self.children[parent].append(child)
        
        self.features: Dict[int, Tuple[int, int, int, int, int]] = {}
        self._compute_features()
        
        self.attributes: Dict[int, int] = {}
        for node in range(1, self.n + 1):
            feat = self.features[node]
            attr = sum(self.params[i] * feat[i] for i in range(5)) % 5
            self.attributes[node] = attr
        
        self.attribute_query_count = 0

    def _compute_features(self):
        depths = {}
        
        def compute_depth(node, parent, d):
            depths[node] = d
            for child in self.children[node]:
                if child != parent:
                    compute_depth(child, node, d + 1)
        
        compute_depth(self.root, -1, 0)
        
        subtree_sizes = {}
        leaf_counts = {}
        
        def compute_subtree(node):
            size = 1
            leaves = 0
            child_count = len(self.children[node])
            
            if child_count == 0:
                leaves = 1
            else:
                for child in self.children[node]:
                    child_size, child_leaves = compute_subtree(child)
                    size += child_size
                    leaves += child_leaves
            
            subtree_sizes[node] = size
            leaf_counts[node] = leaves
            return size, leaves
        
        compute_subtree(self.root)
        
        for node in range(1, self.n + 1):
            depth = depths[node] % 5
            child_count = len(self.children[node]) % 5
            subtree = subtree_sizes[node] % 5
            leaf = leaf_counts[node] % 5
            self.features[node] = (1, depth, child_count, subtree, leaf)

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            if answer < 0 or answer > 4:
                return False
            return answer == self.attributes[self.target]
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        has_feature = "query_feature" in parsed_info
        has_attribute = "query_attribute" in parsed_info
        
        if has_feature and has_attribute:
            return ("错误：每次只能进行一种查询，请分开发送。" if is_zh 
                    else "Error: Only one query type per turn. Please send them separately.")
        
        if has_feature:
            try:
                node = int(parsed_info["query_feature"].strip())
                if node < 1 or node > self.n:
                    return "错误：节点编号超出范围。" if is_zh else "Error: Node ID out of range."
                
                feat = self.features[node]
                result = f"Depth={feat[1]}, Child={feat[2]}, Subtree={feat[3]}, Leaf={feat[4]}"
                return result
            except (ValueError, KeyError):
                return "错误：无效的节点编号。" if is_zh else "Error: Invalid node ID."
        
        elif has_attribute:
            try:
                node = int(parsed_info["query_attribute"].strip())
                
                if node == self.target:
                    return "错误：不能查询目标节点的属性。" if is_zh else "Error: Cannot query target node's attribute."
                
                if node < 1 or node > self.n:
                    return "错误：节点编号超出范围。" if is_zh else "Error: Node ID out of range."
                
                if self.attribute_query_count >= self.max_queries:
                    raise ValueError(
                        "错误：超出最大查询次数。" if is_zh else "Error: Exceeded maximum number of queries."
                    )
                
                self.attribute_query_count += 1
                attr = self.attributes[node]
                
                remaining = self.max_queries - self.attribute_query_count
                result = f"Attr({node})={attr}"
                if remaining > 0:
                    suffix = f"（剩余查询次数：{remaining}）" if is_zh else f" (Remaining queries: {remaining})"
                    result += suffix
                else:
                    suffix = "（已用完所有查询次数）" if is_zh else " (All queries used)"
                    result += suffix
                
                return result
                
            except (ValueError, KeyError) as e:
                if "超出" in str(e) or "Exceeded" in str(e):
                    raise
                return "错误：无效的节点编号。" if is_zh else "Error: Invalid node ID."
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        results = []
        is_zh = self.config.language == "zh"

        for node in range(1, self.n + 1):
            query_content = f"<query_feature>{node}</query_feature>"
            
            feat = self.features[node]
            ans = f"Depth={feat[1]}, Child={feat[2]}, Subtree={feat[3]}, Leaf={feat[4]}"
            
            results.append({"query": query_content, "answer": ans})

        simulated_count = 0
            
        for node in range(1, self.n + 1):
            if node == self.target:
                continue
                
            query_content = f"<query_attribute>{node}</query_attribute>"
            
            simulated_count += 1
            remaining = self.max_queries - simulated_count
            
            if remaining > 0:
                suffix = f"（剩余查询次数：{remaining}）" if is_zh else f" (Remaining queries: {remaining})"
            else:
                suffix = "（已用完所有查询次数）" if is_zh else " (All queries used)"
                
            attr = self.attributes[node]
            ans = f"Attr({node})={attr}{suffix}"
            
            results.append({"query": query_content, "answer": ans})
            
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        import re as _re
        
        attr_match = _re.search(r'Attr\(\d+\)=(\d+)', correct)
        if attr_match:
            original_val = int(attr_match.group(1))
            wrong_val = (original_val + 1) % 5
            return correct.replace(f"={original_val}", f"={wrong_val}", 1)
        
        feat_match = _re.search(r'Depth=(\d+)', correct)
        if feat_match:
            original_depth = int(feat_match.group(1))
            wrong_depth = (original_depth + 1) % 5
            return correct.replace(f"Depth={original_depth}", f"Depth={wrong_depth}", 1)
        
        return correct + "_WRONG"