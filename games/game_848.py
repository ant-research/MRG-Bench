# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   兄弟节点：某给定节点的兄弟节点（同父节点）有哪些
# ============================================================

from .base import Game
import random


class SiblingRelationGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"隐藏关系推理"的多轮游戏，规则如下：

游戏设定了一个包含 {n} 个节点的隐藏结构。每个节点都有唯一的标识符，所有节点列表为：{node_list}。
在这个结构中存在一个隐藏的二元关系 R，你的目标是：
1. 通过多轮交互，推测出关系 R 的真实语义
2. 在每一轮中，针对给定的目标节点 T，找出所有与 T 满足关系 R 的节点集合

## 当前轮次信息
- 节点总数：{n}
- 节点列表：{node_list}
- 目标节点：{target}
- 本轮查询预算：{query_budget} 次

## 可用的查询接口

你可以使用以下五种查询方式（每次只能使用一种，每次查询消耗 1 次预算）：

1. **成对判断**：询问节点 X 和节点 Y 是否满足关系 R
   格式：<query_pair>X,Y</query_pair>
   返回：YES 或 NO

2. **计数查询**：询问有多少个节点与节点 X 满足关系 R（不包含 X 自身）
   格式：<query_count>X</query_count>
   返回：一个非负整数

3. **子集存在性**：询问集合中是否存在至少一个节点与 X 满足关系 R
   格式：<query_any>X:S1,S2,S3</query_any>
   返回：YES 或 NO
   注意：集合中不能包含 X 自身

4. **三元互相关系**：询问三个节点 A、B、C 是否两两都满足关系 R
   格式：<query_mutual>A,B,C</query_mutual>
   返回：YES 或 NO

5. **计数比较**：比较与 X、Y 分别满足关系 R 的节点数量
   格式：<query_compare>X,Y</query_compare>
   返回：< 或 = 或 >（表示与 X 相关的数量与 Y 相关的数量的比较结果）

## 提交答案

当你收集到足够信息后，请提交与目标节点 T 满足关系 R 的所有节点集合（用逗号分隔，顺序不限）：

<answer>node1,node2,node3</answer>

如果没有任何节点与 T 满足关系 R，请提交：

<answer>NONE</answer>

## 全局归纳任务

在完成至少 3 轮游戏后，你需要对关系 R 的语义进行归纳说明。提交格式：

<induction>
自然语言描述：[用一句话描述关系 R 的含义]
形式化描述：[用形式化语言描述 R(x,y) 成立的条件]
</induction>

## 胜利条件

满足以下条件之一即可获胜：
1. 至少 2 轮正确给出与目标节点相关的完整集合，且归纳说明正确
2. 连续 3 轮全部正确给出与目标节点相关的完整集合，且归纳说明正确

## 注意事项

- 请尽可能高效地使用查询预算
- 所有节点名称必须来自给定的节点列表
- 每次只能进行一个查询或提交一个答案
- 答案错误时，系统会公布正确集合帮助你进行跨轮归纳
"""

    game_rule_en = """\
Let's play a multi-round "Hidden Relation Inference" game with the following rules:

The game has a hidden structure containing {n} nodes. Each node has a unique identifier. The complete node list is: {node_list}.
There exists a hidden binary relation R in this structure. Your goals are:
1. Infer the true semantics of relation R through multiple rounds of interaction
2. In each round, for a given target node T, find all nodes that satisfy relation R with T

## Current Round Information
- Total nodes: {n}
- Node list: {node_list}
- Target node: {target}
- Query budget for this round: {query_budget}

## Available Query Interfaces

You can use the following five query types (one per turn, each query consumes 1 from your budget):

1. **Pair Query**: Ask if nodes X and Y satisfy relation R
   Format: <query_pair>X,Y</query_pair>
   Returns: YES or NO

2. **Count Query**: Ask how many nodes satisfy relation R with node X (excluding X itself)
   Format: <query_count>X</query_count>
   Returns: A non-negative integer

3. **Subset Existence**: Ask if at least one node in the set satisfies relation R with X
   Format: <query_any>X:S1,S2,S3</query_any>
   Returns: YES or NO
   Note: The set cannot contain X itself

4. **Mutual Triple**: Ask if three nodes A, B, C all pairwise satisfy relation R
   Format: <query_mutual>A,B,C</query_mutual>
   Returns: YES or NO

5. **Count Comparison**: Compare the number of nodes satisfying R with X versus Y
   Format: <query_compare>X,Y</query_compare>
   Returns: < or = or > (indicating the comparison result)

## Submit Answer

When you have gathered enough information, submit all nodes that satisfy relation R with target node T (comma-separated, order does not matter):

<answer>node1,node2,node3</answer>

If no nodes satisfy relation R with T, submit:

<answer>NONE</answer>

## Global Induction Task

After completing at least 3 rounds, you need to provide an inductive explanation of relation R. Submission format:

<induction>
Natural language: [Describe the meaning of relation R in one sentence]
Formal description: [Describe the condition for R(x,y) to hold in formal language]
</induction>

## Victory Conditions

Win by satisfying one of the following:
1. Correctly provide the complete set for at least 2 rounds, with correct induction
2. Correctly provide the complete set for 3 consecutive rounds, with correct induction

## Important Notes

- Use your query budget as efficiently as possible
- All node names must come from the given node list
- Only one query or answer submission per turn
- When your answer is wrong, the system will reveal the correct set to help with cross-round induction
"""

    # ---------------- 场景1：交通 ----------------
    contextualized_rule_zh_1 = """\
欢迎使用“区域交通枢纽关系推演”系统。

本系统设定了一个包含 {n} 个交通站点的隐藏层级网络。每个站点都有唯一的标识符，站点列表为：{node_list}。
在这些站点间，存在一种隐藏的业务关联 R，你的目标是：
1. 通过多轮试探性查询，推测出关联 R 的真实语义
2. 在每一轮中，针对给定的目标站点 T，找出所有与 T 满足关联 R 的站点集合

## 当前轮次信息
- 站点总数：{n}
- 站点列表：{node_list}
- 目标站点：{target}
- 本轮查询预算：{query_budget} 次

## 可用的查询接口

你可以使用以下五种查询方式（每次只能使用一种，每次查询消耗 1 次预算）：

1. **成对判断**：询问站点 X 和站点 Y 是否满足关联 R
   格式：<query_pair>X,Y</query_pair>
   返回：YES 或 NO

2. **计数查询**：询问有多少个站点与站点 X 满足关联 R（不包含 X 自身）
   格式：<query_count>X</query_count>
   返回：一个非负整数

3. **子集存在性**：询问集合中是否存在至少一个站点与 X 满足关联 R
   格式：<query_any>X:S1,S2,S3</query_any>
   返回：YES 或 NO
   注意：集合中不能包含 X 自身

4. **三元互相关系**：询问三个站点 A、B、C 是否两两都满足关联 R
   格式：<query_mutual>A,B,C</query_mutual>
   返回：YES 或 NO

5. **计数比较**：比较与 X、Y 分别满足关联 R 的站点数量
   格式：<query_compare>X,Y</query_compare>
   返回：< 或 = 或 >（表示与 X 相关的数量与 Y 相关的数量的比较结果）

## 提交答案

当你收集到足够信息后，请提交与目标站点 T 满足关联 R 的所有站点集合（用逗号分隔，顺序不限）：

<answer>node1,node2,node3</answer>

如果没有任何站点与 T 满足关联 R，请提交：

<answer>NONE</answer>

## 全局归纳任务

在完成至少 3 轮推演后，你需要对关联 R 的语义进行归纳说明。提交格式：

<induction>
自然语言描述：[用一句话描述关联 R 的含义]
形式化描述：[用形式化语言描述 R(x,y) 成立的条件]
</induction>

## 胜利条件

满足以下条件之一即可获胜：
1. 至少 2 轮正确给出与目标站点相关的完整集合，且归纳说明正确
2. 连续 3 轮全部正确给出与目标站点相关的完整集合，且归纳说明正确

## 注意事项

- 请尽可能高效地使用查询预算
- 所有站点名称必须来自给定的站点列表
- 每次只能进行一个查询或提交一个答案
- 答案错误时，系统会公布正确集合帮助你进行跨轮归纳
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Regional Transit Hub Relation Inference" system.

The system features a hidden hierarchical network containing {n} transit stations. Each station has a unique identifier, and the complete station list is: {node_list}.
There exists a hidden operational relation R among these stations. Your goals are:
1. Infer the true semantics of relation R through multiple rounds of interaction
2. In each round, for a given target station T, find all stations that satisfy relation R with T

## Current Round Information
- Total stations: {n}
- Station list: {node_list}
- Target station: {target}
- Query budget for this round: {query_budget}

## Available Query Interfaces

You can use the following five query types (one per turn, each query consumes 1 from your budget):

1. **Pair Query**: Ask if stations X and Y satisfy relation R
   Format: <query_pair>X,Y</query_pair>
   Returns: YES or NO

2. **Count Query**: Ask how many stations satisfy relation R with station X (excluding X itself)
   Format: <query_count>X</query_count>
   Returns: A non-negative integer

3. **Subset Existence**: Ask if at least one station in the set satisfies relation R with X
   Format: <query_any>X:S1,S2,S3</query_any>
   Returns: YES or NO
   Note: The set cannot contain X itself

4. **Mutual Triple**: Ask if three stations A, B, C all pairwise satisfy relation R
   Format: <query_mutual>A,B,C</query_mutual>
   Returns: YES or NO

5. **Count Comparison**: Compare the number of stations satisfying R with X versus Y
   Format: <query_compare>X,Y</query_compare>
   Returns: < or = or > (indicating the comparison result)

## Submit Answer

When you have gathered enough information, submit all stations that satisfy relation R with target station T (comma-separated, order does not matter):

<answer>node1,node2,node3</answer>

If no stations satisfy relation R with T, submit:

<answer>NONE</answer>

## Global Induction Task

After completing at least 3 rounds, you need to provide an inductive explanation of relation R. Submission format:

<induction>
Natural language: [Describe the meaning of relation R in one sentence]
Formal description: [Describe the condition for R(x,y) to hold in formal language]
</induction>

## Victory Conditions

Win by satisfying one of the following:
1. Correctly provide the complete set for at least 2 rounds, with correct induction
2. Correctly provide the complete set for 3 consecutive rounds, with correct induction

## Important Notes

- Use your query budget as efficiently as possible
- All station names must come from the given station list
- Only one query or answer submission per turn
- When your answer is wrong, the system will reveal the correct set to help with cross-round induction
"""

    # ---------------- 场景2：医疗 ----------------
    contextualized_rule_zh_2 = """\
欢迎进入“临床实体关系推演”系统。

本系统收录了一个包含 {n} 个临床实体的隐藏病理分类层级。每个实体都有唯一的标识符，实体列表为：{node_list}。
在这些实体间，存在一种隐藏的病理关联 R，你的目标是：
1. 通过多轮试探性查询，推测出关联 R 的真实语义
2. 在每一轮中，针对给定的目标实体 T，找出所有与 T 满足关联 R 的实体集合

## 当前诊断任务信息
- 实体总数：{n}
- 实体列表：{node_list}
- 目标实体：{target}
- 本轮查询预算：{query_budget} 次

## 可用的查询接口

你可以使用以下五种查询方式（每次只能使用一种，每次查询消耗 1 次预算）：

1. **成对判断**：询问实体 X 和实体 Y 是否满足关联 R
   格式：<query_pair>X,Y</query_pair>
   返回：YES 或 NO

2. **计数查询**：询问有多少个实体与实体 X 满足关联 R（不包含 X 自身）
   格式：<query_count>X</query_count>
   返回：一个非负整数

3. **子集存在性**：询问集合中是否存在至少一个实体与 X 满足关联 R
   格式：<query_any>X:S1,S2,S3</query_any>
   返回：YES 或 NO
   注意：集合中不能包含 X 自身

4. **三元互相关系**：询问三个实体 A、B、C 是否两两都满足关联 R
   格式：<query_mutual>A,B,C</query_mutual>
   返回：YES 或 NO

5. **计数比较**：比较与 X、Y 分别满足关联 R 的实体数量
   格式：<query_compare>X,Y</query_compare>
   返回：< 或 = 或 >（表示与 X 相关的数量与 Y 相关的数量的比较结果）

## 提交答案

当你收集到足够信息后，请提交与目标实体 T 满足关联 R 的所有实体集合（用逗号分隔，顺序不限）：

<answer>node1,node2,node3</answer>

如果没有任何实体与 T 满足关联 R，请提交：

<answer>NONE</answer>

## 全局归纳任务

在完成至少 3 轮推演后，你需要对关联 R 的语义进行归纳说明。提交格式：

<induction>
自然语言描述：[用一句话描述关联 R 的含义]
形式化描述：[用形式化语言描述 R(x,y) 成立的条件]
</induction>

## 胜利条件

满足以下条件之一即可获胜：
1. 至少 2 轮正确给出与目标实体相关的完整集合，且归纳说明正确
2. 连续 3 轮全部正确给出与目标实体相关的完整集合，且归纳说明正确

## 注意事项

- 请尽可能高效地分配查询预算
- 所有实体名称必须来自给定的实体列表
- 每次只能进行一个查询或提交一个答案
- 答案错误时，系统会公布正确集合帮助你进行跨轮归纳
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Clinical Entity Relation Inference" system.

The system incorporates a hidden pathological classification hierarchy containing {n} clinical entities. Each entity has a unique identifier, and the complete entity list is: {node_list}.
There exists a hidden pathological relation R among these entities. Your goals are:
1. Infer the true semantics of relation R through multiple rounds of interaction
2. In each round, for a given target entity T, find all entities that satisfy relation R with T

## Current Round Information
- Total entities: {n}
- Entity list: {node_list}
- Target entity: {target}
- Query budget for this round: {query_budget}

## Available Query Interfaces

You can use the following five query types (one per turn, each query consumes 1 from your budget):

1. **Pair Query**: Ask if entities X and Y satisfy relation R
   Format: <query_pair>X,Y</query_pair>
   Returns: YES or NO

2. **Count Query**: Ask how many entities satisfy relation R with entity X (excluding X itself)
   Format: <query_count>X</query_count>
   Returns: A non-negative integer

3. **Subset Existence**: Ask if at least one entity in the set satisfies relation R with X
   Format: <query_any>X:S1,S2,S3</query_any>
   Returns: YES or NO
   Note: The set cannot contain X itself

4. **Mutual Triple**: Ask if three entities A, B, C all pairwise satisfy relation R
   Format: <query_mutual>A,B,C</query_mutual>
   Returns: YES or NO

5. **Count Comparison**: Compare the number of entities satisfying R with X versus Y
   Format: <query_compare>X,Y</query_compare>
   Returns: < or = or > (indicating the comparison result)

## Submit Answer

When you have gathered enough information, submit all entities that satisfy relation R with target entity T (comma-separated, order does not matter):

<answer>node1,node2,node3</answer>

If no entities satisfy relation R with T, submit:

<answer>NONE</answer>

## Global Induction Task

After completing at least 3 rounds, you need to provide an inductive explanation of relation R. Submission format:

<induction>
Natural language: [Describe the meaning of relation R in one sentence]
Formal description: [Describe the condition for R(x,y) to hold in formal language]
</induction>

## Victory Conditions

Win by satisfying one of the following:
1. Correctly provide the complete set for at least 2 rounds, with correct induction
2. Correctly provide the complete set for 3 consecutive rounds, with correct induction

## Important Notes

- Allocate your query budget as efficiently as possible
- All entity names must come from the given entity list
- Only one query or answer submission per turn
- When your answer is wrong, the system will reveal the correct set to help with cross-round induction
"""

    # ---------------- 场景3：教育 ----------------
    contextualized_rule_zh_3 = """\
欢迎使用“学科知识图谱关系推演”系统。

本系统构建了一个包含 {n} 个知识点的隐藏模块层级树。每个知识点都有唯一的标识符，知识点列表为：{node_list}。
在这些知识点间，存在一种隐藏的学科关联 R，你的目标是：
1. 通过多轮试探性查询，推测出关联 R 的真实语义
2. 在每一轮中，针对给定的目标知识点 T，找出所有与 T 满足关联 R 的知识点集合

## 当前探究任务信息
- 知识点总数：{n}
- 知识点列表：{node_list}
- 目标知识点：{target}
- 本轮查询预算：{query_budget} 次

## 可用的查询接口

你可以使用以下五种查询方式（每次只能使用一种，每次查询消耗 1 次预算）：

1. **成对判断**：询问知识点 X 和知识点 Y 是否满足关联 R
   格式：<query_pair>X,Y</query_pair>
   返回：YES 或 NO

2. **计数查询**：询问有多少个知识点与知识点 X 满足关联 R（不包含 X 自身）
   格式：<query_count>X</query_count>
   返回：一个非负整数

3. **子集存在性**：询问集合中是否存在至少一个知识点与 X 满足关联 R
   格式：<query_any>X:S1,S2,S3</query_any>
   返回：YES 或 NO
   注意：集合中不能包含 X 自身

4. **三元互相关系**：询问三个知识点 A、B、C 是否两两都满足关联 R
   格式：<query_mutual>A,B,C</query_mutual>
   返回：YES 或 NO

5. **计数比较**：比较与 X、Y 分别满足关联 R 的知识点数量
   格式：<query_compare>X,Y</query_compare>
   返回：< 或 = 或 >（表示与 X 相关的数量与 Y 相关的数量的比较结果）

## 提交答案

当你收集到足够信息后，请提交与目标知识点 T 满足关联 R 的所有知识点集合（用逗号分隔，顺序不限）：

<answer>node1,node2,node3</answer>

如果没有任何知识点与 T 满足关联 R，请提交：

<answer>NONE</answer>

## 全局归纳任务

在完成至少 3 轮推演后，你需要对关联 R 的语义进行归纳说明。提交格式：

<induction>
自然语言描述：[用一句话描述关联 R 的含义]
形式化描述：[用形式化语言描述 R(x,y) 成立的条件]
</induction>

## 胜利条件

满足以下条件之一即可获胜：
1. 至少 2 轮正确给出与目标知识点相关的完整集合，且归纳说明正确
2. 连续 3 轮全部正确给出与目标知识点相关的完整集合，且归纳说明正确

## 注意事项

- 请尽可能高效地分配查询预算
- 所有知识点名称必须来自给定的知识点列表
- 每次只能进行一个查询或提交一个答案
- 答案错误时，系统会公布正确集合帮助你进行跨轮归纳
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Subject Knowledge Graph Relation Inference" system.

The system constructs a hidden module hierarchy tree containing {n} knowledge concepts. Each concept has a unique identifier, and the complete concept list is: {node_list}.
There exists a hidden pedagogical relation R among these concepts. Your goals are:
1. Infer the true semantics of relation R through multiple rounds of interaction
2. In each round, for a given target concept T, find all concepts that satisfy relation R with T

## Current Round Information
- Total concepts: {n}
- Concept list: {node_list}
- Target concept: {target}
- Query budget for this round: {query_budget}

## Available Query Interfaces

You can use the following five query types (one per turn, each query consumes 1 from your budget):

1. **Pair Query**: Ask if concepts X and Y satisfy relation R
   Format: <query_pair>X,Y</query_pair>
   Returns: YES or NO

2. **Count Query**: Ask how many concepts satisfy relation R with concept X (excluding X itself)
   Format: <query_count>X</query_count>
   Returns: A non-negative integer

3. **Subset Existence**: Ask if at least one concept in the set satisfies relation R with X
   Format: <query_any>X:S1,S2,S3</query_any>
   Returns: YES or NO
   Note: The set cannot contain X itself

4. **Mutual Triple**: Ask if three concepts A, B, C all pairwise satisfy relation R
   Format: <query_mutual>A,B,C</query_mutual>
   Returns: YES or NO

5. **Count Comparison**: Compare the number of concepts satisfying R with X versus Y
   Format: <query_compare>X,Y</query_compare>
   Returns: < or = or > (indicating the comparison result)

## Submit Answer

When you have gathered enough information, submit all concepts that satisfy relation R with target concept T (comma-separated, order does not matter):

<answer>node1,node2,node3</answer>

If no concepts satisfy relation R with T, submit:

<answer>NONE</answer>

## Global Induction Task

After completing at least 3 rounds, you need to provide an inductive explanation of relation R. Submission format:

<induction>
Natural language: [Describe the meaning of relation R in one sentence]
Formal description: [Describe the condition for R(x,y) to hold in formal language]
</induction>

## Victory Conditions

Win by satisfying one of the following:
1. Correctly provide the complete set for at least 2 rounds, with correct induction
2. Correctly provide the complete set for 3 consecutive rounds, with correct induction

## Important Notes

- Allocate your query budget as efficiently as possible
- All concept names must come from the given concept list
- Only one query or answer submission per turn
- When your answer is wrong, the system will reveal the correct set to help with cross-round induction
"""

    # ---------------- 场景4：制造业/工业 ----------------
    contextualized_rule_zh_4 = """\
欢迎启动“工业组件关联推演”系统。

本系统记录了一个包含 {n} 个工艺组件的隐藏装配层级图。每个组件都有唯一的标识符，组件列表为：{node_list}。
在这些组件间，存在一种隐藏的装配关联 R，你的目标是：
1. 通过多轮试探性查询，推测出关联 R 的真实语义
2. 在每一轮中，针对给定的目标组件 T，找出所有与 T 满足关联 R 的组件集合

## 当前推演任务信息
- 组件总数：{n}
- 组件列表：{node_list}
- 目标组件：{target}
- 本轮查询预算：{query_budget} 次

## 可用的查询接口

你可以使用以下五种查询方式（每次只能使用一种，每次查询消耗 1 次预算）：

1. **成对判断**：询问组件 X 和组件 Y 是否满足关联 R
   格式：<query_pair>X,Y</query_pair>
   返回：YES 或 NO

2. **计数查询**：询问有多少个组件与组件 X 满足关联 R（不包含 X 自身）
   格式：<query_count>X</query_count>
   返回：一个非负整数

3. **子集存在性**：询问集合中是否存在至少一个组件与 X 满足关联 R
   格式：<query_any>X:S1,S2,S3</query_any>
   返回：YES 或 NO
   注意：集合中不能包含 X 自身

4. **三元互相关系**：询问三个组件 A、B、C 是否两两都满足关联 R
   格式：<query_mutual>A,B,C</query_mutual>
   返回：YES 或 NO

5. **计数比较**：比较与 X、Y 分别满足关联 R 的组件数量
   格式：<query_compare>X,Y</query_compare>
   返回：< 或 = 或 >（表示与 X 相关的数量与 Y 相关的数量的比较结果）

## 提交答案

当你收集到足够信息后，请提交与目标组件 T 满足关联 R 的所有组件集合（用逗号分隔，顺序不限）：

<answer>node1,node2,node3</answer>

如果没有任何组件与 T 满足关联 R，请提交：

<answer>NONE</answer>

## 全局归纳任务

在完成至少 3 轮推演后，你需要对关联 R 的语义进行归纳说明。提交格式：

<induction>
自然语言描述：[用一句话描述关联 R 的含义]
形式化描述：[用形式化语言描述 R(x,y) 成立的条件]
</induction>

## 胜利条件

满足以下条件之一即可获胜：
1. 至少 2 轮正确给出与目标组件相关的完整集合，且归纳说明正确
2. 连续 3 轮全部正确给出与目标组件相关的完整集合，且归纳说明正确

## 注意事项

- 请尽可能高效地分配查询预算
- 所有组件名称必须来自给定的组件列表
- 每次只能进行一个查询或提交一个答案
- 答案错误时，系统会公布正确集合帮助你进行跨轮归纳
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Component Relation Inference" system.

The system registers a hidden assembly hierarchy diagram containing {n} process components. Each component has a unique identifier, and the complete component list is: {node_list}.
There exists a hidden assembly relation R among these components. Your goals are:
1. Infer the true semantics of relation R through multiple rounds of interaction
2. In each round, for a given target component T, find all components that satisfy relation R with T

## Current Round Information
- Total components: {n}
- Component list: {node_list}
- Target component: {target}
- Query budget for this round: {query_budget}

## Available Query Interfaces

You can use the following five query types (one per turn, each query consumes 1 from your budget):

1. **Pair Query**: Ask if components X and Y satisfy relation R
   Format: <query_pair>X,Y</query_pair>
   Returns: YES or NO

2. **Count Query**: Ask how many components satisfy relation R with component X (excluding X itself)
   Format: <query_count>X</query_count>
   Returns: A non-negative integer

3. **Subset Existence**: Ask if at least one component in the set satisfies relation R with X
   Format: <query_any>X:S1,S2,S3</query_any>
   Returns: YES or NO
   Note: The set cannot contain X itself

4. **Mutual Triple**: Ask if three components A, B, C all pairwise satisfy relation R
   Format: <query_mutual>A,B,C</query_mutual>
   Returns: YES or NO

5. **Count Comparison**: Compare the number of components satisfying R with X versus Y
   Format: <query_compare>X,Y</query_compare>
   Returns: < or = or > (indicating the comparison result)

## Submit Answer

When you have gathered enough information, submit all components that satisfy relation R with target component T (comma-separated, order does not matter):

<answer>node1,node2,node3</answer>

If no components satisfy relation R with T, submit:

<answer>NONE</answer>

## Global Induction Task

After completing at least 3 rounds, you need to provide an inductive explanation of relation R. Submission format:

<induction>
Natural language: [Describe the meaning of relation R in one sentence]
Formal description: [Describe the condition for R(x,y) to hold in formal language]
</induction>

## Victory Conditions

Win by satisfying one of the following:
1. Correctly provide the complete set for at least 2 rounds, with correct induction
2. Correctly provide the complete set for 3 consecutive rounds, with correct induction

## Important Notes

- Allocate your query budget as efficiently as possible
- All component names must come from the given component list
- Only one query or answer submission per turn
- When your answer is wrong, the system will reveal the correct set to help with cross-round induction
"""

    # ---------------- 场景5：法律 ----------------
    contextualized_rule_zh_5 = """\
欢迎访问“法理逻辑关系推演”系统。

本卷宗库提炼了一个包含 {n} 个法条节点的隐藏适用原则层级。每个节点都有唯一的标识符，节点列表为：{node_list}。
在这些节点间，存在一种隐藏的法理关联 R，你的目标是：
1. 通过多轮质证查询，推演并确立关联 R 的核心法理语义
2. 在每一轮中，针对给定的目标法条节点 T，找出所有与 T 满足关联 R 的节点集合

## 当前质证任务信息
- 节点总数：{n}
- 节点列表：{node_list}
- 目标节点：{target}
- 本轮查询预算：{query_budget} 次

## 可用的查询接口

你可以使用以下五种查询方式（每次只能使用一种，每次查询消耗 1 次预算）：

1. **成对判断**：询问节点 X 和节点 Y 是否满足关联 R
   格式：<query_pair>X,Y</query_pair>
   返回：YES 或 NO

2. **计数查询**：询问有多少个节点与节点 X 满足关联 R（不包含 X 自身）
   格式：<query_count>X</query_count>
   返回：一个非负整数

3. **子集存在性**：询问集合中是否存在至少一个节点与 X 满足关联 R
   格式：<query_any>X:S1,S2,S3</query_any>
   返回：YES 或 NO
   注意：集合中不能包含 X 自身

4. **三元互相关系**：询问三个节点 A、B、C 是否两两都满足关联 R
   格式：<query_mutual>A,B,C</query_mutual>
   返回：YES 或 NO

5. **计数比较**：比较与 X、Y 分别满足关联 R 的节点数量
   格式：<query_compare>X,Y</query_compare>
   返回：< 或 = 或 >（表示与 X 相关的数量与 Y 相关的数量的比较结果）

## 提交答案

当你收集到足够信息后，请提交与目标节点 T 满足关联 R 的所有节点集合（用逗号分隔，顺序不限）：

<answer>node1,node2,node3</answer>

如果没有任何节点与 T 满足关联 R，请提交：

<answer>NONE</answer>

## 全局归纳任务

在完成至少 3 轮推演后，你需要对关联 R 的语义进行归纳说明。提交格式：

<induction>
自然语言描述：[用一句话描述关联 R 的含义]
形式化描述：[用形式化语言描述 R(x,y) 成立的条件]
</induction>

## 胜利条件

满足以下条件之一即可获胜：
1. 至少 2 轮正确给出与目标节点相关的完整集合，且归纳说明正确
2. 连续 3 轮全部正确给出与目标节点相关的完整集合，且归纳说明正确

## 注意事项

- 请尽可能高效地分配查询预算
- 所有节点名称必须来自给定的节点列表
- 每次只能进行一个查询或提交一个答案
- 答案错误时，系统会公布正确集合帮助你进行跨轮归纳
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Legal Logic Relation Inference" system.

The database extracts a hidden applicable principle hierarchy containing {n} legal clause nodes. Each node has a unique identifier, and the complete node list is: {node_list}.
There exists a hidden jurisprudential relation R among these nodes. Your goals are:
1. Infer the true semantics of relation R through multiple rounds of interaction
2. In each round, for a given target node T, find all nodes that satisfy relation R with T

## Current Round Information
- Total nodes: {n}
- Node list: {node_list}
- Target node: {target}
- Query budget for this round: {query_budget}

## Available Query Interfaces

You can use the following five query types (one per turn, each query consumes 1 from your budget):

1. **Pair Query**: Ask if nodes X and Y satisfy relation R
   Format: <query_pair>X,Y</query_pair>
   Returns: YES or NO

2. **Count Query**: Ask how many nodes satisfy relation R with node X (excluding X itself)
   Format: <query_count>X</query_count>
   Returns: A non-negative integer

3. **Subset Existence**: Ask if at least one node in the set satisfies relation R with X
   Format: <query_any>X:S1,S2,S3</query_any>
   Returns: YES or NO
   Note: The set cannot contain X itself

4. **Mutual Triple**: Ask if three nodes A, B, C all pairwise satisfy relation R
   Format: <query_mutual>A,B,C</query_mutual>
   Returns: YES or NO

5. **Count Comparison**: Compare the number of nodes satisfying R with X versus Y
   Format: <query_compare>X,Y</query_compare>
   Returns: < or = or > (indicating the comparison result)

## Submit Answer

When you have gathered enough information, submit all nodes that satisfy relation R with target node T (comma-separated, order does not matter):

<answer>node1,node2,node3</answer>

If no nodes satisfy relation R with T, submit:

<answer>NONE</answer>

## Global Induction Task

After completing at least 3 rounds, you need to provide an inductive explanation of relation R. Submission format:

<induction>
Natural language: [Describe the meaning of relation R in one sentence]
Formal description: [Describe the condition for R(x,y) to hold in formal language]
</induction>

## Victory Conditions

Win by satisfying one of the following:
1. Correctly provide the complete set for at least 2 rounds, with correct induction
2. Correctly provide the complete set for 3 consecutive rounds, with correct induction

## Important Notes

- Allocate your query budget as efficiently as possible
- All node names must come from the given node list
- Only one query or answer submission per turn
- When your answer is wrong, the system will reveal the correct set to help with cross-round induction
"""

    tags = ["answer", "query_pair", "query_count", "query_any", "query_mutual", "query_compare", "induction"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "tree_structure": {
                    "A": ["B", "C", "D"],
                    "B": ["E", "F", "G"],
                    "C": ["H", "I"],
                    "D": ["J", "K", "L"],
                },
                "target": "F",
                "query_budget": 12,
            },
            2: {
                "n": 18,
                "tree_structure": {
                    "A": ["B", "C", "D", "E"],
                    "B": ["F", "G", "H"],
                    "C": ["I", "J", "K", "L"],
                    "D": ["M", "N"],
                    "E": ["O", "P", "Q", "R"],
                },
                "target": "I",
                "query_budget": 12,
            },
            3: {
                "n": 25,
                "tree_structure": {
                    "A": ["B", "C", "D"],
                    "B": ["E", "F", "G", "H"],
                    "C": ["I", "J", "K", "L", "M"],
                    "D": ["N", "O", "P"],
                    "E": ["Q", "R"],
                    "F": ["S", "T", "U"],
                    "G": ["V", "W", "X", "Y"],
                },
                "target": "J",
                "query_budget": 12,
            },
            4: {
                "n": 32,
                "tree_structure": {
                    "A": ["B", "C", "D", "E"],
                    "B": ["F", "G", "H"],
                    "C": ["I", "J", "K", "L"],
                    "D": ["M", "N", "O", "P", "Q"],
                    "E": ["R", "S"],
                    "F": ["T", "U", "V"],
                    "G": ["W", "X"],
                    "I": ["Y", "Z", "AA", "AB"],
                    "J": ["AC", "AD"],
                    "M": ["AE", "AF", "AG", "AH", "AI"],
                },
                "target": "AE",
                "query_budget": 12,
            },
            5: {
                "n": 40,
                "tree_structure": {
                    "A": ["B", "C", "D", "E", "F"],
                    "B": ["G", "H", "I"],
                    "C": ["J", "K", "L", "M"],
                    "D": ["N", "O", "P"],
                    "E": ["Q", "R", "S", "T"],
                    "F": ["U", "V"],
                    "G": ["W", "X", "Y"],
                    "H": ["Z", "AA", "AB", "AC"],
                    "J": ["AD", "AE"],
                    "K": ["AF", "AG", "AH"],
                    "L": ["AI", "AJ", "AK", "AL"],
                    "N": ["AM", "AN", "AO", "AP", "AQ"],
                    "Q": ["AR", "AS"],
                    "R": ["AT", "AU", "AV"],
                },
                "target": "AF",
                "query_budget": 12,
            },
        },
        "en": {
            1: {
                "n": 12,
                "tree_structure": {
                    "A": ["B", "C", "D"],
                    "B": ["E", "F", "G"],
                    "C": ["H", "I"],
                    "D": ["J", "K", "L"],
                },
                "target": "F",
                "query_budget": 12,
            },
            2: {
                "n": 18,
                "tree_structure": {
                    "A": ["B", "C", "D", "E"],
                    "B": ["F", "G", "H"],
                    "C": ["I", "J", "K", "L"],
                    "D": ["M", "N"],
                    "E": ["O", "P", "Q", "R"],
                },
                "target": "I",
                "query_budget": 12,
            },
            3: {
                "n": 25,
                "tree_structure": {
                    "A": ["B", "C", "D"],
                    "B": ["E", "F", "G", "H"],
                    "C": ["I", "J", "K", "L", "M"],
                    "D": ["N", "O", "P"],
                    "E": ["Q", "R"],
                    "F": ["S", "T", "U"],
                    "G": ["V", "W", "X", "Y"],
                },
                "target": "J",
                "query_budget": 12,
            },
            4: {
                "n": 32,
                "tree_structure": {
                    "A": ["B", "C", "D", "E"],
                    "B": ["F", "G", "H"],
                    "C": ["I", "J", "K", "L"],
                    "D": ["M", "N", "O", "P", "Q"],
                    "E": ["R", "S"],
                    "F": ["T", "U", "V"],
                    "G": ["W", "X"],
                    "I": ["Y", "Z", "AA", "AB"],
                    "J": ["AC", "AD"],
                    "M": ["AE", "AF", "AG", "AH", "AI"],
                },
                "target": "AE",
                "query_budget": 12,
            },
            5: {
                "n": 40,
                "tree_structure": {
                    "A": ["B", "C", "D", "E", "F"],
                    "B": ["G", "H", "I"],
                    "C": ["J", "K", "L", "M"],
                    "D": ["N", "O", "P"],
                    "E": ["Q", "R", "S", "T"],
                    "F": ["U", "V"],
                    "G": ["W", "X", "Y"],
                    "H": ["Z", "AA", "AB", "AC"],
                    "J": ["AD", "AE"],
                    "K": ["AF", "AG", "AH"],
                    "L": ["AI", "AJ", "AK", "AL"],
                    "N": ["AM", "AN", "AO", "AP", "AQ"],
                    "Q": ["AR", "AS"],
                    "R": ["AT", "AU", "AV"],
                },
                "target": "AF",
                "query_budget": 12,
            },
        },
    }

    def __init__(self, config):
        # 初始化多轮游戏状态
        self.round_number = 0
        self.round_results = []  # 记录每轮的正确/错误
        self.queries_used = 0
        self.induction_submitted = False
        self.induction_correct = False
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：构建树结构，计算兄弟关系"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 构建节点到父节点的映射
        self.tree_structure = cfg["tree_structure"]
        self.node_to_parent = {}
        self.all_nodes = set()
        
        # 根节点（没有父节点的节点）
        roots = set(self.tree_structure.keys())
        
        for parent, children in self.tree_structure.items():
            self.all_nodes.add(parent)
            for child in children:
                self.node_to_parent[child] = parent
                self.all_nodes.add(child)
        
        # 计算每个节点的兄弟节点（真实关系 R）
        self.sibling_map = {}
        for node in self.all_nodes:
            siblings = set()
            if node in self.node_to_parent:
                parent = self.node_to_parent[node]
                # 同一父节点下的其他子节点
                siblings = set(self.tree_structure[parent]) - {node}
            self.sibling_map[node] = siblings
        
        # 动态计算实际节点数，而非信任配置中的 n
        actual_n = len(self.all_nodes)
        
        # 设置游戏信息
        self._game_info["n"] = actual_n
        self._game_info["node_list"] = ", ".join(sorted(self.all_nodes))
        self._game_info["target"] = cfg["target"]
        self._game_info["query_budget"] = cfg["query_budget"]
        
        self.target_node = cfg["target"]
        self.query_budget = cfg["query_budget"]
        self.queries_used = 0
        self.round_number += 1

    def evaluate(self, parsed_info):
        """评估答案：检查提交的兄弟节点集合是否正确"""
        answer_text = parsed_info["answer"].strip()
        
        if answer_text.upper() == "NONE":
            submitted_set = set()
        else:
            submitted_set = set(x.strip() for x in answer_text.split(",") if x.strip())
        
        correct_set = self.sibling_map[self.target_node]
        
        return submitted_set == correct_set

    def _cf_core_produce(self, parsed_info):
        """处理查询并返回读数"""
        
        # 处理 induction 标签 - 直接忽略并提示继续查询或提交答案
        if "induction" in parsed_info and len(parsed_info) == 1:
            if self.config.language == "zh":
                return "已收到归纳说明。请继续查询或提交答案。"
            else:
                return "Induction noted. Please continue querying or submit your answer."
                
        # 检查查询预算
        if self.queries_used >= self.query_budget:
            if self.config.language == "zh":
                return "错误：已超出本轮查询预算。"
            else:
                return "Error: Query budget exceeded for this round."
        
        self.queries_used += 1
        
        if self.config.language == "zh":
            yes_res, no_res = "YES", "NO"
            err_format = "错误：格式无效或节点不存在。"
            err_self = "错误：查询中不能包含相同的节点。"
        else:
            yes_res, no_res = "YES", "NO"
            err_format = "Error: Invalid format or node does not exist."
            err_self = "Error: Query cannot contain the same node."
        
        try:
            # 1. 成对判断
            if "query_pair" in parsed_info:
                raw = parsed_info["query_pair"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return err_format
                x, y = parts
                if x not in self.all_nodes or y not in self.all_nodes:
                    return err_format
                if x == y:
                    return err_self
                # R(x,y) 当且仅当 x 和 y 有相同的父节点
                return yes_res if y in self.sibling_map[x] else no_res
            
            # 2. 计数查询
            elif "query_count" in parsed_info:
                x = parsed_info["query_count"].strip()
                if x not in self.all_nodes:
                    return err_format
                return str(len(self.sibling_map[x]))
            
            # 3. 子集存在性
            elif "query_any" in parsed_info:
                raw = parsed_info["query_any"]
                if ":" not in raw:
                    return err_format
                x_part, set_part = raw.split(":", 1)
                x = x_part.strip()
                subset = set(s.strip() for s in set_part.split(",") if s.strip())
                
                if x not in self.all_nodes:
                    return err_format
                if x in subset:
                    return err_self
                if not all(s in self.all_nodes for s in subset):
                    return err_format
                
                # 检查subset中是否有任何节点与x是兄弟
                has_sibling = any(s in self.sibling_map[x] for s in subset)
                return yes_res if has_sibling else no_res
            
            # 4. 三元互相关系
            elif "query_mutual" in parsed_info:
                raw = parsed_info["query_mutual"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return err_format
                a, b, c = parts
                if not all(node in self.all_nodes for node in [a, b, c]):
                    return err_format
                if len(set([a, b, c])) != 3:
                    return err_self
                
                # 检查 a-b, b-c, a-c 是否都是兄弟关系
                mutual = (b in self.sibling_map[a] and 
                         c in self.sibling_map[b] and 
                         c in self.sibling_map[a])
                return yes_res if mutual else no_res
            
            # 5. 计数比较
            elif "query_compare" in parsed_info:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return err_format
                x, y = parts
                if x not in self.all_nodes or y not in self.all_nodes:
                    return err_format
                
                count_x = len(self.sibling_map[x])
                count_y = len(self.sibling_map[y])
                
                if count_x < count_y:
                    return "<"
                elif count_x == count_y:
                    return "="
                else:
                    return ">"
            
            else:
                return err_format
                
        except Exception as e:
            return err_format

    def _cf_make_wrong(self, correct: str) -> str:
        """将正确的查询响应篡改为错误的"""
        # 如果是 YES/NO，反转
        if correct == "YES":
            return "NO"
        if correct == "NO":
            return "YES"
        
        # 如果是数字，加减一个随机偏移
        try:
            val = int(correct)
            offset = random.choice([-2, -1, 1, 2])
            wrong_val = max(0, val + offset)
            if wrong_val == val:
                wrong_val = val + 1
            return str(wrong_val)
        except ValueError:
            pass
        
        # 如果是比较符号 <, =, >
        if correct in ("<", "=", ">"):
            options = ["<", "=", ">"]
            options.remove(correct)
            return random.choice(options)
        
        # 其他情况，返回一个明显错误的值
        return correct + " [MODIFIED]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        限于组合数量，这里只枚举以下类型的查询：
        1. query_pair: 所有不重复的节点对
        2. query_count: 所有节点
        3. query_compare: 所有不重复的节点对
        
        query_any (子集组合无限) 和 query_mutual (三元组数量庞大) 不在此列。
        """
        queries = []
        sorted_nodes = sorted(list(self.all_nodes))
        
        # 预计算常数
        if self.config.language == "zh":
            YES, NO = "YES", "NO"
        else:
            YES, NO = "YES", "NO"

        for n1 in sorted_nodes:
            # 2. 计数查询
            count_val = len(self.sibling_map[n1])
            queries.append({
                "query": f"<query_count>{n1}</query_count>",
                "answer": str(count_val)
            })

            for n2 in sorted_nodes:
                if n1 == n2:
                    continue

                # 1. 成单判断
                is_sibling = n2 in self.sibling_map[n1]
                queries.append({
                    "query": f"<query_pair>{n1},{n2}</query_pair>",
                    "answer": YES if is_sibling else NO
                })

                # 5. 计数比较
                c1 = len(self.sibling_map[n1])
                c2 = len(self.sibling_map[n2])
                if c1 < c2:
                    res = "<"
                elif c1 == c2:
                    res = "="
                else:
                    res = ">"
                
                queries.append({
                    "query": f"<query_compare>{n1},{n2}</query_compare>",
                    "answer": res
                })

        return queries