# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   树的宽度：树中某层/最宽一层有多少个节点
# ============================================================

from .base import Game
import re


class HiddenTreeExplorationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"隐藏树探索"的推理游戏，规则如下：

游戏设定了一棵隐藏的有根树结构 T。树的根节点位于第 0 层，且第 0 层只有 1 个节点（根）。用 W[d] 表示第 d 层的节点数（层宽度）。树是有限的，存在某个最大层号 D，使得 W[D] 大于 0 且 W[D+1] = 0（即第 D+1 层没有节点）。

你的目标是通过逐层查询，推断出哪一层的节点数最多（称为最宽层），并确定该层的节点数。

## 查询规则

你可以查询某一层的结构信息，但必须遵守以下约束：

1. **必须按层递进查询**：第一次查询必须是第 0 层；之后每次查询的层号必须是上一次成功查询的层号加 1。
2. **不能跳层**：例如查询了第 0 层后，下一次只能查询第 1 层，不能直接查询第 2 层。
3. **不能重复查询同一层**。
4. **只能查询已知存在节点的层**：如果根据上一次查询的结果计算出下一层的节点数为 0，则不能查询该层。

## 查询格式

查询第 d 层时，使用以下格式：

<query_layer>d</query_layer>

例如查询第 0 层：
<query_layer>0</query_layer>

## 查询响应

查询第 d 层后，系统会返回该层的"出度直方图"，格式为一个列表，每个元素是一对数字 (k, c)：
- k 表示子女数（该节点有多少个子节点）
- c 表示具有 k 个子女的节点数量

例如返回 [(0, 2), (3, 1)] 表示：
- 该层有 2 个节点没有子女（叶子节点）
- 该层有 1 个节点有 3 个子女

从出度直方图可以计算：
- 当前层的节点总数 W[d] = 所有 c 值之和
- 下一层的节点总数 W[d+1] = 所有 (k × c) 值之和

## 提交答案

当你收集到足够信息后，需要提交：
1. 最宽层的层号 L（如果有多个层的节点数并列最多，取层号最小的）
2. 最宽层的节点数 W

使用以下格式提交答案：

<answer>L=层号, W=节点数</answer>

例如：
<answer>L=2, W=15</answer>

## 注意事项

- 若查询违反了上述约束（如跳层、重复查询等），会返回错误提示。
- 若提交的答案错误或格式不符，游戏失败。
- 请尽可能少地使用查询次数来找到正确答案。
"""

    game_rule_en = """\
Let's play a "Hidden Tree Exploration" deduction game. Here are the rules:

The game has a hidden rooted tree structure T. The root node is at layer 0, and layer 0 has exactly 1 node (the root). Let W[d] denote the number of nodes at layer d (layer width). The tree is finite: there exists a maximum layer number D such that W[D] is greater than 0 and W[D+1] = 0 (i.e., layer D+1 has no nodes).

Your goal is to determine which layer has the maximum number of nodes (called the widest layer) and how many nodes it has, through layer-by-layer queries.

## Query Rules

You can query the structure information of a layer, but must follow these constraints:

1. **Must query layer by layer**: The first query must be layer 0; each subsequent query must be for the layer number that is one more than the last successful query.
2. **Cannot skip layers**: For example, after querying layer 0, you can only query layer 1 next, not layer 2.
3. **Cannot query the same layer twice**.
4. **Can only query layers known to have nodes**: If the result from the previous query indicates the next layer has 0 nodes, you cannot query that layer.

## Query Format

To query layer d, use this format:

<query_layer>d</query_layer>

For example, to query layer 0:
<query_layer>0</query_layer>

## Query Response

After querying layer d, the system returns an "out-degree histogram" for that layer, formatted as a list where each element is a pair (k, c):
- k represents the number of children (how many child nodes a node has)
- c represents the count of nodes with k children

For example, [(0, 2), (3, 1)] means:
- 2 nodes in this layer have no children (leaf nodes)
- 1 node in this layer has 3 children

From the out-degree histogram, you can calculate:
- Total nodes at current layer W[d] = sum of all c values
- Total nodes at next layer W[d+1] = sum of all (k × c) values

## Submit Answer

When you have collected enough information, submit:
1. The layer number L of the widest layer (if multiple layers tie for maximum width, take the smallest layer number)
2. The node count W of the widest layer

Use this format to submit your answer:

<answer>L=layer_number, W=node_count</answer>

For example:
<answer>L=2, W=15</answer>

## Notes

- If a query violates the constraints (e.g., skipping layers, duplicate queries), an error message will be returned.
- If the submitted answer is incorrect or the format is invalid, the game fails.
- Try to find the correct answer with as few queries as possible.
"""

    # ============================================================
    # 场景 1：交通
    # ============================================================
    contextualized_rule_zh_1 = """\
我们现在来执行一项"路网节点扩散分析"任务，规则如下：

任务设定了一个隐藏的树状路网结构 T。路网的源头是主干道入口，位于第 0 层，且第 0 层只有 1 个节点（入口）。用 W[d] 表示第 d 层的路口节点数（层宽度）。路网的扩散是有限的，存在某个最大层号 D，使得 W[D] 大于 0 且 W[D+1] = 0（即第 D+1 层没有后续路口）。

你的目标是通过逐层查询，推断出哪个层级的路口节点数最多（称为最宽层），并确定该层的具体路口数量。

## 查询规则

你可以查询某一层的路网结构信息，但必须遵守以下约束：

1. **必须按层递进查询**：第一次查询必须是第 0 层；之后每次查询的层号必须是上一次成功查询的层号加 1。
2. **不能跳层**：例如查询了第 0 层后，下一次只能查询第 1 层，不能直接查询第 2 层。
3. **不能重复查询同一层**。
4. **只能查询已知存在路口的层**：如果根据上一次查询的结果计算出下一层的路口数为 0，则不能查询该层。

## 查询格式

查询第 d 层时，使用以下格式：

<query_layer>d</query_layer>

例如查询第 0 层：
<query_layer>0</query_layer>

## 查询响应

查询第 d 层后，系统会返回该层的"分流出境直方图"，格式为一个列表，每个元素是一对数字 (k, c)：
- k 表示分流出境道路数（该路口有多少条通往下一层的道路）
- c 表示具有 k 条出境道路的路口数量

例如返回 [(0, 2), (3, 1)] 表示：
- 该层有 2 个路口没有出境道路（断头路/终端节点）
- 该层有 1 个路口有 3 条出境道路

从直方图可以计算：
- 当前层的路口总数 W[d] = 所有 c 值之和
- 下一层的路口总数 W[d+1] = 所有 (k × c) 值之和

## 提交答案

当你收集到足够信息后，需要提交：
1. 路口数最多的层级号 L（如果有多个层级路口数并列最多，取层号最小的）
2. 该最宽层的路口数 W

使用以下格式提交答案：

<answer>L=层号, W=节点数</answer>

例如：
<answer>L=2, W=15</answer>

## 注意事项

- 若查询违反了上述约束（如跳层、重复查询等），会返回错误提示。
- 若提交的答案错误或格式不符，任务失败。
- 请尽可能少地使用查询次数来找到正确答案。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's perform a "Road Network Node Diffusion Analysis" task. Here are the rules:

The task involves a hidden tree-like road network structure T. The source of the network is the main highway entrance, located at layer 0, and layer 0 has exactly 1 node (the entrance). Let W[d] denote the number of intersection nodes at layer d (layer width). The network diffusion is finite: there exists a maximum layer number D such that W[D] is greater than 0 and W[D+1] = 0 (i.e., layer D+1 has no subsequent intersections).

Your goal is to determine which layer has the maximum number of intersection nodes (called the widest layer) and how many intersections it has, through layer-by-layer queries.

## Query Rules

You can query the structure information of a layer, but must follow these constraints:

1. **Must query layer by layer**: The first query must be layer 0; each subsequent query must be for the layer number that is one more than the last successful query.
2. **Cannot skip layers**: For example, after querying layer 0, you can only query layer 1 next, not layer 2.
3. **Cannot query the same layer twice**.
4. **Can only query layers known to have intersections**: If the result from the previous query indicates the next layer has 0 intersections, you cannot query that layer.

## Query Format

To query layer d, use this format:

<query_layer>d</query_layer>

For example, to query layer 0:
<query_layer>0</query_layer>

## Query Response

After querying layer d, the system returns an "outbound traffic histogram" for that layer, formatted as a list where each element is a pair (k, c):
- k represents the number of outbound roads (how many roads lead to the next layer from an intersection)
- c represents the count of intersections with k outbound roads

For example, [(0, 2), (3, 1)] means:
- 2 intersections in this layer have no outbound roads (dead ends / terminal nodes)
- 1 intersection in this layer has 3 outbound roads

From the histogram, you can calculate:
- Total intersections at current layer W[d] = sum of all c values
- Total intersections at next layer W[d+1] = sum of all (k × c) values

## Submit Answer

When you have collected enough information, submit:
1. The layer number L of the widest layer (if multiple layers tie for maximum width, take the smallest layer number)
2. The intersection count W of the widest layer

Use this format to submit your answer:

<answer>L=layer_number, W=node_count</answer>

For example:
<answer>L=2, W=15</answer>

## Notes

- If a query violates the constraints (e.g., skipping layers, duplicate queries), an error message will be returned.
- If the submitted answer is incorrect or the format is invalid, the task fails.
- Try to find the correct answer with as few queries as possible.
"""

    # ============================================================
    # 场景 2：医疗
    # ============================================================
    contextualized_rule_zh_2 = """\
我们现在来进行一项"病毒传播链追踪"任务，规则如下：

任务设定了一棵隐藏的病毒传播树结构 T。树的根节点是"零号病人"，位于第 0 代（层），且第 0 代只有 1 个节点。用 W[d] 表示第 d 代的感染者人数（层宽度）。传播是有限的，存在某个最大代数 D，使得 W[D] 大于 0 且 W[D+1] = 0（即第 D+1 代没有新的感染者）。

你的目标是通过逐代查询，推断出哪一代的感染者人数最多（称为最宽层），并确定该代的具体感染人数。

## 查询规则

你可以查询某一代的传播结构信息，但必须遵守以下约束：

1. **必须按代递进查询**：第一次查询必须是第 0 代；之后每次查询的代数必须是上一次成功查询的代数加 1。
2. **不能跳代**：例如查询了第 0 代后，下一次只能查询第 1 代，不能直接查询第 2 代。
3. **不能重复查询同一代**。
4. **只能查询已知存在感染者的代**：如果根据上一次查询的结果计算出下一代的感染人数为 0，则不能查询该代。

## 查询格式

查询第 d 代时，使用以下格式：

<query_layer>d</query_layer>

例如查询第 0 代：
<query_layer>0</query_layer>

## 查询响应

查询第 d 代后，系统会返回该代的"传染分支直方图"，格式为一个列表，每个元素是一对数字 (k, c)：
- k 表示直接传染的下家数（该感染者直接传染了多少人）
- c 表示具有 k 个下家的感染者人数

例如返回 [(0, 2), (3, 1)] 表示：
- 该代有 2 个感染者没有传染给任何人（传播链终端）
- 该代有 1 个感染者直接传染了 3 个人

从直方图可以计算：
- 当前代的感染总人数 W[d] = 所有 c 值之和
- 下一代的感染总人数 W[d+1] = 所有 (k × c) 值之和

## 提交答案

当你收集到足够信息后，需要提交：
1. 感染人数最多的一代（代数 L，如果有多个代数感染人数并列最多，取代数最小的）
2. 该代的感染总人数 W

使用以下格式提交答案：

<answer>L=层号, W=节点数</answer>

例如：
<answer>L=2, W=15</answer>

## 注意事项

- 若查询违反了上述约束（如跳层、重复查询等），会返回错误提示。
- 若提交的答案错误或格式不符，任务失败。
- 请尽可能少地使用查询次数来找到正确答案。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's perform a "Viral Transmission Chain Tracking" task. Here are the rules:

The task features a hidden viral transmission tree structure T. The root node is "Patient Zero", located at generation (layer) 0, and generation 0 has exactly 1 node. Let W[d] denote the number of infected individuals at generation d (layer width). The transmission is finite: there exists a maximum generation number D such that W[D] is greater than 0 and W[D+1] = 0 (i.e., generation D+1 has no new infections).

Your goal is to determine which generation has the maximum number of infected individuals (called the widest layer) and how many infections it has, through layer-by-layer queries.

## Query Rules

You can query the transmission structure of a generation, but must follow these constraints:

1. **Must query generation by generation**: The first query must be generation 0; each subsequent query must be for the generation number that is one more than the last successful query.
2. **Cannot skip generations**: For example, after querying generation 0, you can only query generation 1 next, not generation 2.
3. **Cannot query the same generation twice**.
4. **Can only query generations known to have infected individuals**: If the result from the previous query indicates the next generation has 0 infections, you cannot query that generation.

## Query Format

To query generation d, use this format:

<query_layer>d</query_layer>

For example, to query generation 0:
<query_layer>0</query_layer>

## Query Response

After querying generation d, the system returns a "transmission branch histogram" for that layer, formatted as a list where each element is a pair (k, c):
- k represents the number of direct secondary infections (how many people an infected individual directly infected)
- c represents the count of infected individuals who caused k secondary infections

For example, [(0, 2), (3, 1)] means:
- 2 infected individuals in this generation did not infect anyone else (terminal nodes)
- 1 infected individual in this generation directly infected 3 people

From the histogram, you can calculate:
- Total infections at current generation W[d] = sum of all c values
- Total infections at next generation W[d+1] = sum of all (k × c) values

## Submit Answer

When you have collected enough information, submit:
1. The generation number L with the most infections (if multiple generations tie, take the smallest generation number)
2. The total infection count W of that generation

Use this format to submit your answer:

<answer>L=layer_number, W=node_count</answer>

For example:
<answer>L=2, W=15</answer>

## Notes

- If a query violates the constraints, an error message will be returned.
- If the submitted answer is incorrect or the format is invalid, the task fails.
- Try to find the correct answer with as few queries as possible.
"""

    # ============================================================
    # 场景 3：教育
    # ============================================================
    contextualized_rule_zh_3 = """\
我们现在来进行一项"学科知识图谱探索"任务，规则如下：

任务设定了一棵隐藏的学科知识前置依赖树 T。树的根节点是该学科的核心元知识点，位于第 0 层，且第 0 层只有 1 个节点。用 W[d] 表示第 d 层的知识点数量（层宽度）。知识衍生是有限的，存在某个最大层号 D，使得 W[D] 大于 0 且 W[D+1] = 0（即第 D+1 层没有进一步细分的知识点）。

你的目标是通过逐层查询，推断出包含知识点数量最多的深度层级（称为最宽层），并确定该层的具体知识点总数。

## 查询规则

你可以查询某一层的知识体系信息，但必须遵守以下约束：

1. **必须按层递进查询**：第一次查询必须是第 0 层；之后每次查询的层号必须是上一次成功查询的层号加 1。
2. **不能跳层**：例如查询了第 0 层后，下一次只能查询第 1 层，不能直接查询第 2 层。
3. **不能重复查询同一层**。
4. **只能查询已知存在知识点的层**：如果根据上一次查询的结果计算出下一层的知识点数为 0，则不能查询该层。

## 查询格式

查询第 d 层时，使用以下格式：

<query_layer>d</query_layer>

例如查询第 0 层：
<query_layer>0</query_layer>

## 查询响应

查询第 d 层后，系统会返回该层的"知识点衍生直方图"，格式为一个列表，每个元素是一对数字 (k, c)：
- k 表示向下衍生的子知识点数（该知识点直接衍生出多少个更具体的子概念）
- c 表示具有 k 个衍生子节点的知识点数量

例如返回 [(0, 2), (3, 1)] 表示：
- 该层有 2 个知识点没有衍生出更具体的子知识点（基础叶子节点）
- 该层有 1 个知识点直接衍生出了 3 个子知识点

从直方图可以计算：
- 当前层的知识点总数 W[d] = 所有 c 值之和
- 下一层的知识点总数 W[d+1] = 所有 (k × c) 值之和

## 提交答案

当你收集到足够信息后，需要提交：
1. 包含知识点最多的层号 L（如果有多个层的知识点数并列最多，取层号最小的）
2. 该最宽层的知识点总数 W

使用以下格式提交答案：

<answer>L=层号, W=节点数</answer>

例如：
<answer>L=2, W=15</answer>

## 注意事项

- 若查询违反了上述约束（如跳层、重复查询等），会返回错误提示。
- 若提交的答案错误或格式不符，任务失败。
- 请尽可能少地使用查询次数来找到正确答案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform a "Subject Knowledge Graph Exploration" task. Here are the rules:

The task features a hidden prerequisite tree structure T of a subject's knowledge graph. The root node is the core meta-concept, located at layer 0, and layer 0 has exactly 1 node. Let W[d] denote the number of concepts at layer d (layer width). The knowledge derivation is finite: there exists a maximum layer number D such that W[D] is greater than 0 and W[D+1] = 0 (i.e., layer D+1 has no further subdivided concepts).

Your goal is to determine which depth layer has the maximum number of concepts (called the widest layer) and how many concepts it has, through layer-by-layer queries.

## Query Rules

You can query the knowledge structure information of a layer, but must follow these constraints:

1. **Must query layer by layer**: The first query must be layer 0; each subsequent query must be for the layer number that is one more than the last successful query.
2. **Cannot skip layers**: For example, after querying layer 0, you can only query layer 1 next, not layer 2.
3. **Cannot query the same layer twice**.
4. **Can only query layers known to have concepts**: If the result from the previous query indicates the next layer has 0 concepts, you cannot query that layer.

## Query Format

To query layer d, use this format:

<query_layer>d</query_layer>

For example, to query layer 0:
<query_layer>0</query_layer>

## Query Response

After querying layer d, the system returns a "concept derivation histogram" for that layer, formatted as a list where each element is a pair (k, c):
- k represents the number of derived sub-concepts (how many specific sub-concepts this concept directly derives into)
- c represents the count of concepts that derive into k sub-concepts

For example, [(0, 2), (3, 1)] means:
- 2 concepts in this layer do not derive into more specific sub-concepts (fundamental leaf nodes)
- 1 concept in this layer directly derives into 3 sub-concepts

From the histogram, you can calculate:
- Total concepts at current layer W[d] = sum of all c values
- Total concepts at next layer W[d+1] = sum of all (k × c) values

## Submit Answer

When you have collected enough information, submit:
1. The layer number L with the most concepts (if multiple layers tie for maximum width, take the smallest layer number)
2. The total concept count W of that widest layer

Use this format to submit your answer:

<answer>L=layer_number, W=node_count</answer>

For example:
<answer>L=2, W=15</answer>

## Notes

- If a query violates the constraints, an error message will be returned.
- If the submitted answer is incorrect or the format is invalid, the task fails.
- Try to find the correct answer with as few queries as possible.
"""

    # ============================================================
    # 场景 4：制造业/工业
    # ============================================================
    contextualized_rule_zh_4 = """\
我们现在来进行一项"产品BOM（物料清单）层级解析"任务，规则如下：

任务设定了一棵隐藏的产品装配依赖树 T。树的根节点是最终成品，位于第 0 级（层），且第 0 级只有 1 个节点。用 W[d] 表示第 d 级的独立零部件数量（层宽度）。拆解是有限的，存在某个最大级数 D，使得 W[D] 大于 0 且 W[D+1] = 0（即第 D+1 级没有更底层的零件）。

你的目标是通过逐级查询，推断出涉及零部件种类最多的装配层级（称为最宽层），并确定该级的零部件总数。

## 查询规则

你可以查询某一级的物料拆解信息，但必须遵守以下约束：

1. **必须按级递进查询**：第一次查询必须是第 0 级；之后每次查询的层级数必须是上一次成功查询的级数加 1。
2. **不能跳级**：例如查询了第 0 级后，下一次只能查询第 1 级，不能直接查询第 2 级。
3. **不能重复查询同一级**。
4. **只能查询已知存在零件的层级**：如果根据上一次查询的结果计算出下一级的零件数为 0，则不能查询该级。

## 查询格式

查询第 d 级时，使用以下格式：

<query_layer>d</query_layer>

例如查询第 0 级：
<query_layer>0</query_layer>

## 查询响应

查询第 d 级后，系统会返回该级的"组件拆解直方图"，格式为一个列表，每个元素是一对数字 (k, c)：
- k 表示向下拆解的子零件种类数（该组件需要多少种下级零件来组装）
- c 表示需要 k 种子零件的组件数量

例如返回 [(0, 2), (3, 1)] 表示：
- 该级有 2 个组件不需要下级零件（属于底层原材料/基础叶子节点）
- 该级有 1 个组件需要 3 种下级零件

从直方图可以计算：
- 当前级的零部件总数 W[d] = 所有 c 值之和
- 下一级的零部件总数 W[d+1] = 所有 (k × c) 值之和

## 提交答案

当你收集到足够信息后，需要提交：
1. 涉及零件种类最多的层级 L（如果有多个层级零件数并列最多，取级数最小的）
2. 该级的零件总数 W

使用以下格式提交答案：

<answer>L=层号, W=节点数</answer>

例如：
<answer>L=2, W=15</answer>

## 注意事项

- 若查询违反了上述约束（如跳级、重复查询等），会返回错误提示。
- 若提交的答案错误或格式不符，任务失败。
- 请尽可能少地使用查询次数来找到正确答案。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's perform a "Product BOM (Bill of Materials) Level Analysis" task. Here are the rules:

The task features a hidden product assembly dependency tree T. The root node is the final product, located at assembly level (layer) 0, and level 0 has exactly 1 node. Let W[d] denote the number of unique components at level d (layer width). The breakdown is finite: there exists a maximum level number D such that W[D] is greater than 0 and W[D+1] = 0 (i.e., level D+1 has no lower-level parts).

Your goal is to determine which assembly level involves the maximum number of component types (called the widest layer) and how many components it has, through level-by-level queries.

## Query Rules

You can query the material breakdown information of a level, but must follow these constraints:

1. **Must query level by level**: The first query must be level 0; each subsequent query must be for the level number that is one more than the last successful query.
2. **Cannot skip levels**: For example, after querying level 0, you can only query level 1 next, not level 2.
3. **Cannot query the same level twice**.
4. **Can only query levels known to have components**: If the result from the previous query indicates the next level has 0 components, you cannot query that level.

## Query Format

To query level d, use this format:

<query_layer>d</query_layer>

For example, to query level 0:
<query_layer>0</query_layer>

## Query Response

After querying level d, the system returns a "component breakdown histogram" for that level, formatted as a list where each element is a pair (k, c):
- k represents the number of sub-component types required (how many types of lower-level parts this component needs for assembly)
- c represents the count of components that require k types of sub-components

For example, [(0, 2), (3, 1)] means:
- 2 components in this level require no sub-components (base raw materials / leaf nodes)
- 1 component in this level requires 3 types of sub-components

From the histogram, you can calculate:
- Total components at current level W[d] = sum of all c values
- Total components at next level W[d+1] = sum of all (k × c) values

## Submit Answer

When you have collected enough information, submit:
1. The assembly level L with the most components (if multiple levels tie, take the smallest level number)
2. The total component count W of that level

Use this format to submit your answer:

<answer>L=level_number, W=node_count</answer>

For example:
<answer>L=2, W=15</answer>

## Notes

- If a query violates the constraints, an error message will be returned.
- If the submitted answer is incorrect or the format is invalid, the task fails.
- Try to find the correct answer with as few queries as possible.
"""

    # ============================================================
    # 场景 5：法律
    # ============================================================
    contextualized_rule_zh_5 = """\
我们现在来进行一项"涉案资金流向穿透"任务，规则如下：

任务设定了一棵隐藏的洗钱账户树结构 T。树的根节点是初始涉案账户，位于第 0 层，且第 0 层只有 1 个节点。用 W[d] 表示第 d 层的涉案账户数量（层宽度）。资金转移是有限的，存在某个最大层号 D，使得 W[D] 大于 0 且 W[D+1] = 0（即第 D+1 层没有进一步的资金流转）。

你的目标是通过逐层查询，推断出涉及账户数量最多的转移层级（称为最宽层），并确定该层的具体账户总数。

## 查询规则

你可以查询某一层的资金转移结构信息，但必须遵守以下约束：

1. **必须按层递进查询**：第一次查询必须是第 0 层；之后每次查询的层号必须是上一次成功查询的层号加 1。
2. **不能跳层**：例如查询了第 0 层后，下一次只能查询第 1 层，不能直接查询第 2 层。
3. **不能重复查询同一层**。
4. **只能查询已知存在账户的层**：如果根据上一次查询的结果计算出下一层的账户数为 0，则不能查询该层。

## 查询格式

查询第 d 层时，使用以下格式：

<query_layer>d</query_layer>

例如查询第 0 层：
<query_layer>0</query_layer>

## 查询响应

查询第 d 层后，系统会返回该层的"资金流出直方图"，格式为一个列表，每个元素是一对数字 (k, c)：
- k 表示资金流向的下级账户数（该账户向多少个下一层账户转账）
- c 表示向 k 个下级账户转账的本层账户数量

例如返回 [(0, 2), (3, 1)] 表示：
- 该层有 2 个账户没有向任何下级账户转账（沉淀资金账户/终端节点）
- 该层有 1 个账户向 3 个下级账户转账

从直方图可以计算：
- 当前层的账户总数 W[d] = 所有 c 值之和
- 下一层的账户总数 W[d+1] = 所有 (k × c) 值之和

## 提交答案

当你收集到足够信息后，需要提交：
1. 涉及账户最多的转移层号 L（如果有多个层账户数并列最多，取层号最小的）
2. 该层的账户总数 W

使用以下格式提交答案：

<answer>L=层号, W=节点数</answer>

例如：
<answer>L=2, W=15</answer>

## 注意事项

- 若查询违反了上述约束（如跳层、重复查询等），会返回错误提示。
- 若提交的答案错误或格式不符，任务失败。
- 请尽可能少地使用查询次数来找到正确答案。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's perform an "Illicit Fund Flow Penetration" task. Here are the rules:

The task features a hidden money laundering account tree structure T. The root node is the original suspect account, located at transaction layer 0, and layer 0 has exactly 1 node. Let W[d] denote the number of involved accounts at layer d (layer width). The fund transfer is finite: there exists a maximum layer number D such that W[D] is greater than 0 and W[D+1] = 0 (i.e., layer D+1 has no further fund transfers).

Your goal is to determine which transaction layer involves the maximum number of accounts (called the widest layer) and exactly how many accounts it has, through layer-by-layer queries.

## Query Rules

You can query the fund transfer information of a layer, but must follow these constraints:

1. **Must query layer by layer**: The first query must be layer 0; each subsequent query must be for the layer number that is one more than the last successful query.
2. **Cannot skip layers**: For example, after querying layer 0, you can only query layer 1 next, not layer 2.
3. **Cannot query the same layer twice**.
4. **Can only query layers known to have accounts**: If the result from the previous query indicates the next layer has 0 accounts, you cannot query that layer.

## Query Format

To query layer d, use this format:

<query_layer>d</query_layer>

For example, to query layer 0:
<query_layer>0</query_layer>

## Query Response

After querying layer d, the system returns a "fund outflow histogram" for that layer, formatted as a list where each element is a pair (k, c):
- k represents the number of receiving sub-accounts (how many next-layer accounts this account transfers funds to)
- c represents the count of accounts in this layer that transfer funds to k sub-accounts

For example, [(0, 2), (3, 1)] means:
- 2 accounts in this layer do not transfer funds to any further accounts (terminal destination accounts)
- 1 account in this layer transfers funds to 3 sub-accounts

From the histogram, you can calculate:
- Total accounts at current layer W[d] = sum of all c values
- Total accounts at next layer W[d+1] = sum of all (k × c) values

## Submit Answer

When you have collected enough information, submit:
1. The transaction layer L with the most accounts (if multiple layers tie, take the smallest layer number)
2. The total account count W of that layer

Use this format to submit your answer:

<answer>L=layer_number, W=node_count</answer>

For example:
<answer>L=2, W=15</answer>

## Notes

- If a query violates the constraints, an error message will be returned.
- If the submitted answer is incorrect or the format is invalid, the task fails.
- Try to find the correct answer with as few queries as possible.
"""

    tags = ["answer", "query_layer"]
    
    reasoning_type = "演绎推理"
    data_structure = "树"

    # 难度配置说明：
    # 1 (简单)       - 3层树，最宽层在中间
    # 2 (中等偏下)   - 4层树，最宽层在中间靠后
    # 3 (中等偏上)   - 5层树，递增后递减
    # 4 (较难)       - 6层树，多个并列最宽需取最小层号
    # 5 (难)         - 7层树，复杂分支结构

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "tree_structure": [
                    [(2, 1)],           # 第0层: 1个节点有2个子女 -> W[0]=1, W[1]=2
                    [(3, 2)],           # 第1层: 2个节点各有3个子女 -> W[1]=2, W[2]=6
                    [(0, 6)],           # 第2层: 6个叶子节点 -> W[2]=6, W[3]=0
                ],
                "answer": {"L": 2, "W": 6}
            },
            2: {
                "tree_structure": [
                    [(3, 1)],           # 第0层: 1个节点有3个子女 -> W[0]=1, W[1]=3
                    [(2, 3)],           # 第1层: 3个节点各有2个子女 -> W[1]=3, W[2]=6
                    [(1, 4), (2, 2)],   # 第2层: 4个节点有1个子女，2个节点有2个子女 -> W[2]=6, W[3]=8
                    [(0, 8)],           # 第3层: 8个叶子节点 -> W[3]=8, W[4]=0
                ],
                "answer": {"L": 3, "W": 8}
            },
            3: {
                "tree_structure": [
                    [(4, 1)],           # 第0层: W[0]=1, W[1]=4
                    [(3, 4)],           # 第1层: W[1]=4, W[2]=12
                    [(2, 12)],          # 第2层: W[2]=12, W[3]=24
                    [(1, 24)],          # 第3层: W[3]=24, W[4]=24
                    [(0, 24)],          # 第4层: W[4]=24, W[5]=0
                ],
                "answer": {"L": 3, "W": 24}
            },
            4: {
                "tree_structure": [
                    [(2, 1)],                   # 第0层: W[0]=1, W[1]=2
                    [(5, 2)],                   # 第1层: W[1]=2, W[2]=10
                    [(2, 10)],                  # 第2层: W[2]=10, W[3]=20
                    [(1, 20)],                  # 第3层: W[3]=20, W[4]=20
                    [(1, 10), (0, 10)],         # 第4层: W[4]=20, W[5]=10
                    [(0, 10)],                  # 第5层: W[5]=10, W[6]=0
                ],
                "answer": {"L": 3, "W": 20}  # 第3层和第4层都是20，取最小层号3
            },
            5: {
                "tree_structure": [
                    [(5, 1)],                   # 第0层: W[0]=1, W[1]=5
                    [(3, 3), (4, 2)],           # 第1层: W[1]=5, W[2]=17
                    [(2, 10), (3, 7)],          # 第2层: W[2]=17, W[3]=41
                    [(1, 25), (2, 16)],         # 第3层: W[3]=41, W[4]=57
                    [(1, 40), (0, 17)],         # 第4层: W[4]=57, W[5]=40
                    [(1, 20), (0, 20)],         # 第5层: W[5]=40, W[6]=20
                    [(0, 20)],                  # 第6层: W[6]=20, W[7]=0
                ],
                "answer": {"L": 4, "W": 57}
            },
        },
        "en": {
            1: {
                "tree_structure": [
                    [(2, 1)],
                    [(3, 2)],
                    [(0, 6)],
                ],
                "answer": {"L": 2, "W": 6}
            },
            2: {
                "tree_structure": [
                    [(3, 1)],
                    [(2, 3)],
                    [(1, 4), (2, 2)],
                    [(0, 8)],
                ],
                "answer": {"L": 3, "W": 8}
            },
            3: {
                "tree_structure": [
                    [(4, 1)],
                    [(3, 4)],
                    [(2, 12)],
                    [(1, 24)],
                    [(0, 24)],
                ],
                "answer": {"L": 3, "W": 24}
            },
            4: {
                "tree_structure": [
                    [(2, 1)],
                    [(5, 2)],
                    [(2, 10)],
                    [(1, 20)],
                    [(1, 10), (0, 10)],
                    [(0, 10)],
                ],
                "answer": {"L": 3, "W": 20}
            },
            5: {
                "tree_structure": [
                    [(5, 1)],
                    [(3, 3), (4, 2)],
                    [(2, 10), (3, 7)],
                    [(1, 25), (2, 16)],
                    [(1, 40), (0, 17)],
                    [(1, 20), (0, 20)],
                    [(0, 20)],
                ],
                "answer": {"L": 4, "W": 57}
            },
        }
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
        
        # 树结构：每层的出度直方图
        self.tree_structure = cfg["tree_structure"]
        
        # 正确答案
        self.correct_answer = cfg["answer"]
        
        # 追踪查询状态
        self.last_queried_layer = -1  # 上次成功查询的层号
        self.queried_layers = set()   # 已查询过的层号集合
        self.next_layer_width = 1     # 下一层应有的节点数（初始为第0层的1个节点）
        
        # 计算各层宽度序列（用于验证和内部逻辑）
        self.layer_widths = []
        self._compute_layer_widths()

    def _compute_layer_widths(self):
        """预计算各层的宽度序列 W[0], W[1], ..."""
        self.layer_widths = [1]  # W[0] = 1
        for layer_histogram in self.tree_structure:
            current_width = sum(c for _, c in layer_histogram)
            next_width = sum(k * c for k, c in layer_histogram)
            self.layer_widths.append(next_width)

    def evaluate(self, parsed_info):
        """评估提交的答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案格式: L=x, W=y
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                if "=" not in kv:
                    return False
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "L" not in ans_dict or "W" not in ans_dict:
                return False
            
            submitted_L = int(ans_dict["L"])
            submitted_W = int(ans_dict["W"])
            
            # 检查答案是否正确
            return (submitted_L == self.correct_answer["L"] and 
                    submitted_W == self.correct_answer["W"])
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """处理层查询请求（作为反事实核心生产方法）"""
        if "query_layer" not in parsed_info:
            if self.config.language == "zh":
                return "错误：无效的查询格式。"
            else:
                return "Error: Invalid query format."
        
        try:
            layer = int(parsed_info["query_layer"].strip())
        except ValueError:
            if self.config.language == "zh":
                return "错误：层号必须是整数。"
            else:
                return "Error: Layer number must be an integer."
        
        # 检查是否为负数
        if layer < 0:
            if self.config.language == "zh":
                return "错误：层号不能为负数。"
            else:
                return "Error: Layer number cannot be negative."
        
        # 检查是否重复查询
        if layer in self.queried_layers:
            if self.config.language == "zh":
                return f"无效请求：已经查询过第 {layer} 层。"
            else:
                return f"Invalid request: Layer {layer} has already been queried."
        
        # 检查是否按层递进
        if layer != self.last_queried_layer + 1:
            if self.config.language == "zh":
                expected = self.last_queried_layer + 1
                return f"无效请求：未按层顺序。应查询第 {expected} 层，而非第 {layer} 层。"
            else:
                expected = self.last_queried_layer + 1
                return f"Invalid request: Not in layer order. Should query layer {expected}, not layer {layer}."
        
        # 检查该层是否存在（根据上次查询计算的下一层宽度）
        if self.next_layer_width == 0:
            if self.config.language == "zh":
                return f"无效请求：第 {layer} 层不存在节点。"
            else:
                return f"Invalid request: Layer {layer} has no nodes."
        
        # 检查层号是否超出树的深度
        if layer >= len(self.tree_structure):
            if self.config.language == "zh":
                return f"无效请求：第 {layer} 层不存在。"
            else:
                return f"Invalid request: Layer {layer} does not exist."
        
        # 成功查询，返回该层的出度直方图
        histogram = self.tree_structure[layer]
        
        # 更新查询状态
        self.queried_layers.add(layer)
        self.last_queried_layer = layer
        
        # 计算下一层的宽度
        self.next_layer_width = sum(k * c for k, c in histogram)
        
        # 格式化返回结果
        histogram_str = str(histogram)
        
        return histogram_str
    
    def _cf_make_wrong(self, correct):
        """生成一个错误的响应，用于反事实干预"""
        # correct 是一个类似 "[(0, 2), (3, 1)]" 的字符串
        # 策略：解析直方图，篡改其中的计数值
        try:
            import ast
            histogram = ast.literal_eval(correct)
            if isinstance(histogram, list) and len(histogram) > 0:
                # 修改第一个元素的计数 c，使其 +1 或变成不同的值
                k, c = histogram[0]
                wrong_histogram = [(k, c + 2)] + histogram[1:]
                return str(wrong_histogram)
        except:
            pass
        # fallback：返回一个明显不同的直方图
        return "[(0, 1)]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        在这个游戏中，合法的查询是对所有存在节点的层进行查询。
        """
        possible_queries = []
        for layer_idx, histogram in enumerate(self.tree_structure):
            possible_queries.append({
                "query": f"<query_layer>{layer_idx}</query_layer>",
                "answer": str(histogram)
            })
        return possible_queries