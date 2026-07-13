# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   祖先判断：某节点是否为另一节点的祖先
# ============================================================

from .base import Game
import random


class ThresholdTreeGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树结构阈值推理"的游戏，规则如下：

游戏设定了一个含有 {n} 个节点的有根树，根节点为 {root}。树的结构已完全给出：

节点：{nodes}
边（无向）：{edges}

## 基础定义

- **深度**：节点到根的边数。根节点深度为 0。
- **祖先关系**：节点 u 是节点 v 的祖先，当且仅当 u 不等于 v，且 u 在从根到 v 的唯一路径上。

## 隐藏参数

系统已秘密设定了一个整数阈值 K（1 到 {max_k} 之间），在整个游戏中固定不变。

## 判定规则

对于任意有序节点对 (X, Y)，定义布尔谓词 A(X, Y)：
- 当且仅当同时满足以下两个条件时为真：
  1. X 是 Y 的严格祖先
  2. Y 的深度减去 X 的深度小于等于 K

## 你的任务

通过尽可能少的询问，推断出隐藏阈值 K 的确切数值。

## 交互方式

你可以反复向我提问，每次询问一对有序节点 (X, Y)，询问 A(X, Y) 是否为真。我会根据隐藏的 K 值如实回答"是"或"否"。

注意：
- X 和 Y 必须是不同的节点
- 如果 X 和 Y 相同，回答固定为"否"
- 你可以自行计算树的结构、深度和祖先关系

## 询问与提交答案的格式

每次询问使用以下 XML 格式（X 和 Y 用逗号分隔）：

<query>X,Y</query>

当你确定阈值 K 后，使用以下格式提交最终答案：

<answer>K</answer>

其中 K 为你推断出的阈值数值。

若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Tree Threshold Inference" game. Here are the rules:

The game is set on a rooted tree with {n} nodes, where the root is {root}. The tree structure is fully given:

Nodes: {nodes}
Edges (undirected): {edges}

## Basic Definitions

- **Depth**: The number of edges from a node to the root. The root has depth 0.
- **Ancestor Relation**: Node u is an ancestor of node v if and only if u is not equal to v and u is on the unique path from the root to v.

## Hidden Parameter

The system has secretly set an integer threshold K (between 1 and {max_k}), which remains fixed throughout the game.

## Decision Rule

For any ordered pair of nodes (X, Y), define the boolean predicate A(X, Y):
- It is true if and only if both of the following conditions are satisfied:
  1. X is a strict ancestor of Y
  2. The depth of Y minus the depth of X is less than or equal to K

## Your Task

Through as few queries as possible, deduce the exact value of the hidden threshold K.

## Interaction

You can repeatedly ask questions. Each time, query an ordered pair of nodes (X, Y), asking whether A(X, Y) is true. I will answer "Yes" or "No" truthfully based on the hidden K value.

Notes:
- X and Y must be different nodes
- If X and Y are the same, the answer is always "No"
- You can compute the tree structure, depths, and ancestor relationships yourself

## Query and Answer Format

For each query, use the following XML format (X and Y separated by comma):

<query>X,Y</query>

When you have determined the threshold K, submit your final answer using this format:

<answer>K</answer>

where K is the threshold value you inferred.

If the answer is wrong or the format is invalid, the game fails.
"""

    contextualized_rule_zh_1 = """\
您好，系统规划员。我们现在进行"轨道交通区间票价与通达性推演"测试。
本测试基于一个包含 {n} 个站点的轨道交通辐射网络，中心枢纽站为 {root}。网络拓扑结构如下：

站点：{nodes}
线路（双向）：{edges}

## 基础定义

- **层级**：站点距离中心枢纽站的站数。中心枢纽站层级为 0。
- **线路直达关系**：站点 u 是站点 v 的"上游站"，当且仅当 u 不等于 v，且 u 位于从中心枢纽站到 v 的唯一乘车路径上。

## 隐藏参数

公交系统秘密设置了一个"直达票价区域限制"常数 K（1 到 {max_k} 之间），在整个推演中保持不变。

## 判定规则

对于任意一对发到站 (X, Y)，定义票务有效性 A(X, Y)：
- 当且仅当同时满足以下两个条件时，该区间车票有效（为真）：
  1. X 是 Y 的严格上游站（即乘客可以顺向乘车无需折返）
  2. Y 的层级减去 X 的层级的差值（即乘坐站数）小于或等于限制区域 K

## 你的任务

通过尽可能少的系统查询，准确推断出隐藏的区域限制 K 的数值。

## 交互方式

你可以反复向我提交线路查询。每次询问输入一对有序站点 (X, Y)，查询 A(X, Y) 是否有效。我会根据隐藏的 K 值如实返回"是"或"否"。

注意：
- X 和 Y 必须是不同的站点
- 如果 X 和 Y 相同，回答固定为"否"
- 你可以自行计算网络拓扑、层级和上下游关系

## 询问与提交答案的格式

每次询问使用以下 XML 格式（X 和 Y 用逗号分隔）：

<query>X,Y</query>

当你确定限制常数 K 后，使用以下格式提交最终答案：

<answer>K</answer>

若答案错误或格式不符，推演失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Hello, System Planner. We are now conducting the "Rail Transit Fare Zone and Accessibility Inference" test.
This test is based on a radial rail transit network containing {n} stations, with the central hub station being {root}. The network topology is as follows:

Stations: {nodes}
Lines (two-way): {edges}

## Basic Definitions

- **Tier**: The number of stops a station is from the central hub. The central hub has a tier of 0.
- **Direct Route Relationship**: Station u is an "upstream station" of station v if and only if u is not equal to v, and u lies on the unique travel path from the central hub to v.

## Hidden Parameter

The transit system has secretly set a "direct fare zone limit" constant K (between 1 and {max_k}), which remains fixed throughout the inference.

## Decision Rule

For any ordered pair of departure and arrival stations (X, Y), ticket validity A(X, Y) is defined:
- The ticket for this interval is valid (True) if and only if both of the following conditions are met:
  1. X is a strict upstream station of Y (i.e., the passenger can travel forward without turning back).
  2. The difference between Y's tier and X's tier (i.e., the number of stops traveled) is less than or equal to the zone limit K.

## Your Task

Through as few system queries as possible, accurately deduce the hidden zone limit K.

## Interaction

You can repeatedly submit route queries. Each time, query an ordered pair of stations (X, Y) to check if A(X, Y) is valid. I will answer "Yes" or "No" truthfully based on the hidden K value.

Notes:
- X and Y must be different stations.
- If X and Y are the same, the answer is always "No".
- You can compute the network topology, tiers, and upstream relationships yourself.

## Query and Answer Format

For each query, use the following XML format (X and Y separated by comma):

<query>X,Y</query>

When you have determined the limit constant K, submit your final answer using this format:

<answer>K</answer>

If the answer is wrong or the format is invalid, the inference fails.
"""

    contextualized_rule_zh_2 = """\
您好，流行病学专家。我们现在进行"病毒变异株交叉免疫屏障"的流行病学推演。
系统记录了一个包含 {n} 个变异株的病毒进化树，原始毒株为 {root}。进化谱系如下：

毒株编号：{nodes}
变异路径（无向）：{edges}

## 基础定义

- **变异代数**：某毒株距离原始毒株的变异突变次数。原始毒株代数为 0。
- **进化溯源关系**：毒株 u 是毒株 v 的"进化先驱"，当且仅当 u 不等于 v，且 u 存在于从原始毒株到 v 的唯一进化路径上。

## 隐藏参数

系统根据当前疫苗特性秘密设定了一个"交叉免疫代际极限"常量 K（1 到 {max_k} 之间），在整个推演中固定不变。

## 判定规则

对于任意有序毒株对 (X, Y)，定义免疫有效性 A(X, Y)：
- 针对 X 毒株研发的疫苗对 Y 毒株具有保护效力（为真），当且仅当同时满足以下两个条件：
  1. X 是 Y 的严格进化先驱
  2. Y 的变异代数减去 X 的变异代数小于或等于极限 K

## 你的任务

通过尽可能少的抗体中和试验（询问），推断出隐藏的免疫代际极限 K 的确切数值。

## 交互方式

你可以反复向我提交中和试验。每次询问一对有序毒株 (X, Y)，测试 A(X, Y) 是否有效。我会根据隐藏的 K 值如实回答"是"或"否"。

注意：
- X 和 Y 必须是不同的毒株
- 如果 X 和 Y 相同，系统返回固定为"否"
- 你可以自行计算谱系结构、变异代数和进化先驱关系

## 询问与提交答案的格式

每次询问使用以下 XML 格式（X 和 Y 用逗号分隔）：

<query>X,Y</query>

当你确定免疫代际极限 K 后，使用以下格式提交最终答案：

<answer>K</answer>

若答案错误或格式不符，推演失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Hello, Epidemiologist. We are now conducting the "Viral Variant Cross-Immunity Barrier" epidemiological inference.
The system has recorded a viral phylogenetic tree containing {n} variants, with the original strain being {root}. The evolutionary lineage is as follows:

Strain IDs: {nodes}
Mutation Paths (undirected): {edges}

## Basic Definitions

- **Mutation Generation**: The number of mutation events a strain is from the original strain. The original strain is at generation 0.
- **Evolutionary Ancestry**: Strain u is an "evolutionary precursor" to strain v if and only if u is not equal to v, and u is on the unique evolutionary path from the original strain to v.

## Hidden Parameter

Based on current vaccine characteristics, the system has secretly set a "cross-immunity generational limit" constant K (between 1 and {max_k}), which remains fixed throughout the inference.

## Decision Rule

For any ordered pair of strains (X, Y), immune efficacy A(X, Y) is defined:
- A vaccine developed against strain X provides protective efficacy against strain Y (True) if and only if both conditions are met:
  1. X is a strict evolutionary precursor to Y.
  2. The mutation generation of Y minus the mutation generation of X is less than or equal to the limit K.

## Your Task

Through as few antibody neutralization tests (queries) as possible, deduce the exact value of the hidden immune generational limit K.

## Interaction

You can repeatedly submit neutralization tests. Each time, query an ordered pair of strains (X, Y) to test if A(X, Y) is effective. I will answer "Yes" or "No" truthfully based on the hidden K value.

Notes:
- X and Y must be different strains.
- If X and Y are the same, the answer is always "No".
- You can compute the lineage structure, mutation generations, and evolutionary ancestry yourself.

## Query and Answer Format

For each query, use the following XML format (X and Y separated by comma):

<query>X,Y</query>

When you have determined the immune generational limit K, submit your final answer using this format:

<answer>K</answer>

If the answer is wrong or the format is invalid, the inference fails.
"""

    contextualized_rule_zh_3 = """\
您好，课程设计师。我们现在进行"认知脚手架与前置知识跨度"评估测试。
系统构建了一个包含 {n} 个知识点的课程技能树，基础核心概念为 {root}。技能树结构如下：

知识点节点：{nodes}
前置关联（无向）：{edges}

## 基础定义

- **认知深度**：知识点距离核心概念的递进层数。核心概念深度为 0。
- **前置依赖关系**：知识点 u 是知识点 v 的"基础前置"，当且仅当 u 不等于 v，且 u 位于从核心概念到 v 的唯一学习路径上。

## 隐藏参数

系统根据学生认知负荷极限，秘密设定了一个"最大跳跃学习跨度"整数阈值 K（1 到 {max_k} 之间），在整个评估中固定不变。

## 判定规则

对于任意有序知识点对 (X, Y)，定义学习路径连贯性 A(X, Y)：
- 学生在掌握 X 的情况下能直接跳跃理解 Y（为真），当且仅当同时满足以下两个条件：
  1. X 是 Y 的严格基础前置知识
  2. Y 的认知深度减去 X 的认知深度的差值小于或等于跨度 K

## 你的任务

通过尽可能少的教研查询，推断出隐藏的最大跳跃学习跨度 K 的确切数值。

## 交互方式

你可以反复向我提问。每次询问一对有序知识点 (X, Y)，测试 A(X, Y) 是否成立。我会根据隐藏的 K 值如实回答"是"或"否"。

注意：
- X 和 Y 必须是不同的知识点
- 如果 X 和 Y 相同，回答固定为"否"
- 你可以自行计算技能树结构、认知深度和前置依赖关系

## 询问与提交答案的格式

每次询问使用以下 XML 格式（X 和 Y 用逗号分隔）：

<query>X,Y</query>

当你确定最大跨度 K 后，使用以下格式提交最终答案：

<answer>K</answer>

若答案错误或格式不符，评估失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Hello, Curriculum Designer. We are now conducting the "Cognitive Scaffolding and Prerequisite Span" assessment test.
The system has constructed a course skill tree containing {n} knowledge points, with the foundational core concept being {root}. The skill tree structure is as follows:

Knowledge Nodes: {nodes}
Prerequisite Links (undirected): {edges}

## Basic Definitions

- **Cognitive Depth**: The number of progression layers a knowledge point is from the core concept. The core concept has a depth of 0.
- **Prerequisite Dependency**: Knowledge point u is a "foundational prerequisite" of v if and only if u is not equal to v, and u lies on the unique learning path from the core concept to v.

## Hidden Parameter

Based on the students' cognitive load limit, the system has secretly set a "maximum learning leap span" integer threshold K (between 1 and {max_k}), which remains fixed throughout the assessment.

## Decision Rule

For any ordered pair of knowledge points (X, Y), the learning path coherence A(X, Y) is defined:
- A student who has mastered X can directly leap to understand Y (True) if and only if both conditions are met:
  1. X is a strict foundational prerequisite of Y.
  2. The cognitive depth of Y minus the cognitive depth of X is less than or equal to the leap span K.

## Your Task

Through as few pedagogical queries as possible, deduce the exact value of the hidden learning leap span K.

## Interaction

You can repeatedly ask questions. Each time, query an ordered pair of knowledge points (X, Y) to test if A(X, Y) holds. I will answer "Yes" or "No" truthfully based on the hidden K value.

Notes:
- X and Y must be different knowledge points.
- If X and Y are the same, the answer is always "No".
- You can compute the skill tree structure, cognitive depths, and prerequisite dependencies yourself.

## Query and Answer Format

For each query, use the following XML format (X and Y separated by comma):

<query>X,Y</query>

When you have determined the maximum leap span K, submit your final answer using this format:

<answer>K</answer>

If the answer is wrong or the format is invalid, the assessment fails.
"""

    contextualized_rule_zh_4 = """\
您好，供应链架构师。我们现在进行"BOM（物料清单）层级与管理穿透度"推演。
系统导出了一个包含 {n} 个组件的装配BOM树，顶级成品编号为 {root}。物料拆解结构如下：

组件编号：{nodes}
装配关系（无向）：{edges}

## 基础定义

- **装配层级**：某组件在BOM中距离顶级成品的拆解层数。顶级成品层级为 0。
- **包含关系**：组件 u 是组件 v 的"上级总成"，当且仅当 u 不等于 v，且 u 存在于从顶级成品到 v 的唯一装配路径上（即 u 包含 v）。

## 隐藏参数

工厂管理系统秘密设定了一个"最大管理穿透深度"整数阈值 K（1 到 {max_k} 之间），在整个推演中固定不变。

## 判定规则

对于任意有序组件对 (X, Y)，定义管理穿透有效性 A(X, Y)：
- 负责组件 X 的工程师有权直接调度下级组件 Y（为真），当且仅当同时满足以下两个条件：
  1. X 是 Y 的严格上级总成
  2. Y 的装配层级减去 X 的装配层级小于或等于穿透深度 K

## 你的任务

通过尽可能少的权限查询，推断出隐藏的穿透深度 K 的确切数值。

## 交互方式

你可以反复向我发起查询。每次询问一对有序组件 (X, Y)，测试调度权限 A(X, Y) 是否有效。我会根据隐藏的 K 值如实回答"是"或"否"。

注意：
- X 和 Y 必须是不同的组件
- 如果 X 和 Y 相同，回答固定为"否"
- 你可以自行计算BOM结构、装配层级和包含关系

## 询问与提交答案的格式

每次询问使用以下 XML 格式（X 和 Y 用逗号分隔）：

<query>X,Y</query>

当你确定管理穿透深度 K 后，使用以下格式提交最终答案：

<answer>K</answer>

若答案错误或格式不符，推演失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Hello, Supply Chain Architect. We are now conducting the "BOM (Bill of Materials) Hierarchy and Management Penetration" inference.
The system has exported an assembly BOM tree containing {n} components, with the top-level final product being {root}. The material breakdown structure is as follows:

Component IDs: {nodes}
Assembly Relations (undirected): {edges}

## Basic Definitions

- **Assembly Level**: The number of breakdown layers a component is from the top-level product. The top-level product is at level 0.
- **Inclusion Relationship**: Component u is a "parent assembly" of component v if and only if u is not equal to v, and u exists on the unique assembly path from the top-level product to v (i.e., u includes v).

## Hidden Parameter

The factory management system has secretly set a "maximum management penetration depth" integer threshold K (between 1 and {max_k}), which remains fixed throughout the inference.

## Decision Rule

For any ordered pair of components (X, Y), the management penetration validity A(X, Y) is defined:
- An engineer responsible for component X has the authority to directly dispatch the subordinate component Y (True) if and only if both conditions are met:
  1. X is a strict parent assembly of Y.
  2. The assembly level of Y minus the assembly level of X is less than or equal to the penetration depth K.

## Your Task

Through as few permission queries as possible, deduce the exact value of the hidden penetration depth K.

## Interaction

You can repeatedly initiate queries. Each time, query an ordered pair of components (X, Y) to test if the dispatch permission A(X, Y) is valid. I will answer "Yes" or "No" truthfully based on the hidden K value.

Notes:
- X and Y must be different components.
- If X and Y are the same, the answer is always "No".
- You can compute the BOM structure, assembly levels, and inclusion relationships yourself.

## Query and Answer Format

For each query, use the following XML format (X and Y separated by comma):

<query>X,Y</query>

When you have determined the management penetration depth K, submit your final answer using this format:

<answer>K</answer>

If the answer is wrong or the format is invalid, the inference fails.
"""

    contextualized_rule_zh_5 = """\
您好，合规审查员。我们现在进行"公司控制权与法人人格否认"穿透测试。
工商库反馈了一个包含 {n} 个法人的股权控制树，顶层绝对控股母公司为 {root}。股权架构如下：

法人实体：{nodes}
控股链路（无向）：{edges}

## 基础定义

- **控制层级**：某实体距离顶层控股母公司的股权嵌套层数。顶层母公司层级为 0。
- **实际控制关系**：实体 u 是实体 v 的"上层控股方"，当且仅当 u 不等于 v，且 u 存在于从顶层母公司到 v 的唯一控制链条上。

## 隐藏参数

反垄断系统秘密设定了一个"责任穿透最高层数"整数阈值 K（1 到 {max_k} 之间），在整个审查中固定不变。

## 判定规则

对于任意有序实体对 (X, Y)，定义连带责任追溯 A(X, Y)：
- 当 Y 发生违规时，司法机关可直接刺破法人面纱追究 X 的连带责任（为真），当且仅当同时满足以下两个条件：
  1. X 是 Y 的严格上层控股方
  2. Y 的控制层级减去 X 的控制层级小于或等于穿透最高层数 K

## 你的任务

通过尽可能少的穿透问询，推断出隐藏的责任穿透阈值 K 的确切数值。

## 交互方式

你可以反复向我发起问询。每次询问一对有序实体 (X, Y)，测试 A(X, Y) 是否成立。我会根据隐藏的 K 值如实回答"是"或"否"。

注意：
- X 和 Y 必须是不同的实体
- 如果 X 和 Y 相同，回答固定为"否"
- 你可以自行计算控制权架构、层级和实际控制关系

## 询问与提交答案的格式

每次询问使用以下 XML 格式（X 和 Y 用逗号分隔）：

<query>X,Y</query>

当你确定责任穿透最高层数 K 后，使用以下格式提交最终答案：

<answer>K</answer>

若答案错误或格式不符，审查失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Hello, Compliance Auditor. We are now conducting the "Corporate Control and Piercing the Corporate Veil" penetration test.
The registry has returned an equity control tree containing {n} legal entities, with the top-level ultimate holding company being {root}. The equity architecture is as follows:

Legal Entities: {nodes}
Control Links (undirected): {edges}

## Basic Definitions

- **Control Tier**: The number of nested equity layers an entity is from the top-level holding company. The top-level company is at tier 0.
- **Actual Control Relationship**: Entity u is an "upstream holding party" of entity v if and only if u is not equal to v, and u exists on the unique chain of control from the top-level company to v.

## Hidden Parameter

The antitrust system has secretly set a "maximum liability penetration layer" integer threshold K (between 1 and {max_k}), which remains fixed throughout the audit.

## Decision Rule

For any ordered pair of entities (X, Y), the joint liability trace A(X, Y) is defined:
- When Y commits a violation, the judicial authority can directly pierce the corporate veil to hold X jointly liable (True) if and only if both conditions are met:
  1. X is a strict upstream holding party of Y.
  2. The control tier of Y minus the control tier of X is less than or equal to the maximum penetration layer K.

## Your Task

Through as few penetration inquiries as possible, deduce the exact value of the hidden liability penetration threshold K.

## Interaction

You can repeatedly initiate inquiries. Each time, query an ordered pair of entities (X, Y) to test if A(X, Y) holds. I will answer "Yes" or "No" truthfully based on the hidden K value.

Notes:
- X and Y must be different entities.
- If X and Y are the same, the answer is always "No".
- You can compute the control architecture, tiers, and actual control relationships yourself.

## Query and Answer Format

For each query, use the following XML format (X and Y separated by comma):

<query>X,Y</query>

When you have determined the maximum liability penetration layer K, submit your final answer using this format:

<answer>K</answer>

If the answer is wrong or the format is invalid, the audit fails.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置说明：
    # 1 (简单)        - 小树(5节点)，链状，K较小
    # 2 (中等偏下)    - 中等树(8节点)，稍有分支，K中等
    # 3 (中等偏上)    - 中等树(10节点)，多分支，K较大
    # 4 (较难)        - 较大树(12节点)，复杂结构，K接近最大深度
    # 5 (难)          - 大树(15节点)，高度复杂，K需要精确推断

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "root": "1",
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "k": 2,
            },
            2: {
                "n": 8,
                "root": "1",
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8)],
                "k": 2,
            },
            3: {
                "n": 10,
                "root": "1",
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (7, 10)],
                "k": 3,
            },
            4: {
                "n": 12,
                "root": "1",
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (11, 12)],
                "k": 3,
            },
            5: {
                "n": 15,
                "root": "1",
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (14, 15)],
                "k": 3,
            },
        },
        "en": {
            1: {
                "n": 5,
                "root": "1",
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "k": 2,
            },
            2: {
                "n": 8,
                "root": "1",
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8)],
                "k": 2,
            },
            3: {
                "n": 10,
                "root": "1",
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (7, 10)],
                "k": 3,
            },
            4: {
                "n": 12,
                "root": "1",
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (11, 12)],
                "k": 3,
            },
            5: {
                "n": 15,
                "root": "1",
                "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (14, 15)],
                "k": 3,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数类型

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        
        # 格式化节点和边的显示
        nodes = [str(i) for i in range(1, cfg["n"] + 1)]
        self._game_info["nodes"] = ", ".join(nodes)
        
        edges_str = ", ".join([f"({u},{v})" for u, v in cfg["edges"]])
        self._game_info["edges"] = edges_str
        
        # 保存树的结构信息
        self.root = int(cfg["root"])
        self.edges = cfg["edges"]
        
        # 构建树的邻接表
        self.adj = {i: [] for i in range(1, cfg["n"] + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        # 计算每个节点的深度和父节点
        self.depth = {}
        self.parent = {}
        self._build_tree(self.root, -1, 0)
        
        # 计算最大深度，用于规则说明
        max_depth = max(self.depth.values())
        self._game_info["max_k"] = max_depth
        
        # 使用配置中预设的固定 K 值，保证基准可复现
        self.k = cfg["k"]

    def _build_tree(self, node, par, d):
        """
        DFS构建树结构，计算深度和父节点
        """
        self.depth[node] = d
        self.parent[node] = par
        for neighbor in self.adj[node]:
            if neighbor != par:
                self._build_tree(neighbor, node, d + 1)

    def _is_ancestor(self, u, v):
        """
        判断 u 是否是 v 的严格祖先
        """
        if u == v:
            return False
        # 从 v 向上追溯到根，看是否经过 u
        current = self.parent[v]
        while current != -1:
            if current == u:
                return True
            current = self.parent[current]
        return False

    def _evaluate_predicate(self, x, y):
        """
        计算 A(x, y) 的真值
        """
        if x == y:
            return False
        if not self._is_ancestor(x, y):
            return False
        depth_diff = self.depth[y] - self.depth[x]
        return depth_diff <= self.k

    def evaluate(self, parsed_info):
        """
        评估最终答案是否正确
        """
        try:
            ans_k = int(parsed_info["answer"].strip())
            return ans_k == self.k
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """
        原始的业务逻辑，处理查询并生成响应
        """
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            err_format = "错误：查询格式无效，请使用 'X,Y' 格式。"
            err_node = "错误：节点不存在。"
        else:
            yes_res, no_res = "Yes", "No"
            err_format = "Error: Invalid query format. Please use 'X,Y' format."
            err_node = "Error: Node does not exist."

        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")

        raw = parsed_info["query"].strip()
        try:
            parts = [p.strip() for p in raw.split(",")]
            if len(parts) != 2:
                return err_format
            
            x, y = int(parts[0]), int(parts[1])
            
            # 检查节点是否存在
            if x not in self.depth or y not in self.depth:
                return err_node
            
            # 计算并返回结果
            result = self._evaluate_predicate(x, y)
            return yes_res if result else no_res
            
        except (ValueError, TypeError):
            return err_format

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文处理
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
        # 英文处理
        else:
            correct_lower = correct.lower()
            if correct_lower == "yes":
                return "No" if correct[0].isupper() else "no"
            if correct_lower == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        # 若都不匹配
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        possible_queries = []
        n = self._game_info["n"]
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        # 节点编号从1到n
        nodes = range(1, n + 1)
        
        for x in nodes:
            for y in nodes:
                # 规则提示：X 和 Y 必须是不同的节点
                # 虽然规则说相同返回否，但通常"合法查询"意味着符合提问约束
                # 这里我们遍历所有 X != Y 的情况
                if x == y:
                    continue
                    
                # 构造查询字符串，必须是合法的 XML 标签格式
                query_str = f"<query>{x},{y}</query>"
                
                # 计算逻辑真值
                result = self._evaluate_predicate(x, y)
                answer_str = yes_res if result else no_res
                
                possible_queries.append({
                    "query": query_str,
                    "answer": answer_str
                })
                
        return possible_queries