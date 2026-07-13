from .base import Game
import re


class MaxPathInTreeGame(Game):

    game_rule_zh = """\
我们来玩一个"树中最大路径查询"游戏。规则如下：

游戏设定了一棵未知结构的有根树，节点编号为 1 到 N，根节点编号为 1。每个节点 u 有一个整数权重 w(u)，可以是正数、零或负数。边没有权重。

你的目标是：在所有从根到叶的路径中，找出节点权重之和最大的那条路径，以及该路径的权重总和。保证所有根到叶路径的总和两两不同，即唯一最优路径一定存在。

初始时你只知道根节点的编号是 1，其余的树结构和节点权重都是未知的。你需要通过局部查询逐步获得信息。

## 查询规则

每次你只能对一个节点或一条候选路径发起一次查询。不允许请求整棵树或整层的批量信息。

允许的查询类型如下（请严格按照 XML 格式）：

1. 查询节点总数：
<query_n></query_n>

2. 查询节点 u 的权重：
<query_value>u</query_value>

3. 查询节点 u 的所有子节点（返回升序列表，若 u 为叶则返回空列表）：
<query_children>u</query_children>

4. 查询节点 u 是否为叶节点：
<query_isleaf>u</query_isleaf>

5. 查询节点 u 的父节点（若 u=1 则返回 NONE）：
<query_parent>u</query_parent>

6. 验证并查询一条根到叶路径的总和（路径必须以 1 开头、以某叶结尾，且相邻节点为父子关系）：
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. 标注（仅作记录，不触发信息回应，不计入查询次数）：
<note>你的标注内容</note>

## 裁判回应格式

- 对 query_n：返回节点总数
- 对 query_value：返回该节点的权重值
- 对 query_children：返回子节点列表（升序），若无子节点则返回空列表
- 对 query_isleaf：返回"是"或"否"
- 对 query_parent：返回父节点编号，若为根则返回"无"
- 对 query_pathsum：若为有效路径则返回总和，否则返回"无效路径"
- 对 note：不回应

## 提交答案

当你收集到足够信息后，可以提交最终答案。格式如下：

<answer>path=1,a2,a3,...,L;sum=S</answer>

其中 path 是从根到叶的完整路径（用逗号分隔），sum 是该路径的权重总和。

判定标准：
- path 必须是有效的根到叶路径
- sum 必须与该路径的真实总和一致
- 该总和必须是所有根到叶路径中的最大值

若答案正确，返回"答案正确"；否则返回"答案错误"。

## 注意事项

- 请尽可能减少查询次数
- 每次只能进行一个查询
- 格式错误的查询不会被响应
"""

    game_rule_en = """\
Let's play a "Maximum Path in Tree Query" game. Here are the rules:

The game involves an unknown rooted tree with nodes numbered from 1 to N, where node 1 is the root. Each node u has an integer weight w(u), which can be positive, zero, or negative. Edges have no weights.

Your goal is: among all root-to-leaf paths, find the one with the maximum sum of node weights, and determine that sum. It is guaranteed that all root-to-leaf path sums are distinct, so a unique optimal path exists.

Initially, you only know the root node is numbered 1. The rest of the tree structure and node weights are unknown. You must gradually gather information through local queries.

## Query Rules

Each time you can only query about one node or one candidate path. Batch requests for the entire tree or entire levels are not allowed.

Allowed query types (strictly follow XML format):

1. Query total number of nodes:
<query_n></query_n>

2. Query the weight of node u:
<query_value>u</query_value>

3. Query all children of node u (returns sorted list; empty if u is a leaf):
<query_children>u</query_children>

4. Query whether node u is a leaf:
<query_isleaf>u</query_isleaf>

5. Query the parent of node u (returns NONE if u=1):
<query_parent>u</query_parent>

6. Verify and query the sum of a root-to-leaf path (must start with 1, end at a leaf, with adjacent nodes being parent-child):
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. Note (for annotation only, no response, does not count as a query):
<note>your annotation</note>

## Judge Response Format

- For query_n: returns total number of nodes
- For query_value: returns the node's weight value
- For query_children: returns list of children (sorted); empty list if no children
- For query_isleaf: returns "Yes" or "No"
- For query_parent: returns parent node number; "None" if root
- For query_pathsum: returns sum if valid path; "Invalid path" otherwise
- For note: no response

## Submit Answer

When you have gathered enough information, submit your final answer in this format:

<answer>path=1,a2,a3,...,L;sum=S</answer>

where path is the complete root-to-leaf path (comma-separated), and sum is the total weight of that path.

Judgment criteria:
- path must be a valid root-to-leaf path
- sum must match the actual sum of that path
- that sum must be the maximum among all root-to-leaf paths

If correct, returns "Correct answer"; otherwise returns "Incorrect answer".

## Notes

- Try to minimize the number of queries
- Only one query per turn
- Incorrectly formatted queries will not be responded to
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
我们来进行一项“交通网络最优通行路线规划”任务。规则如下：

游戏设定了一个未知结构的交通管网系统，站点编号为 1 到 N，总枢纽编号为 1。每个站点 u 都有一个整数净收益 w(u)（代表客流收益减去运营成本），可以是正数、零或负数。站点间的连接路段没有独立权重。

你的目标是：在所有从总枢纽到最终目的站（终点站）的通行路线中，找出站点净收益之和最大的那条路线，以及该路线的总收益。保证所有从总枢纽到终点站的路线收益总和两两不同，即唯一最优路线一定存在。

初始时你只知道总枢纽的编号是 1，其余的管网结构和站点收益都是未知的。你需要通过局部查询逐步获得信息。

## 查询规则

每次你只能对一个站点或一条候选路线发起一次查询。不允许请求全局管网或整层路网的批量信息。

允许的查询类型如下（请严格按照 XML 格式）：

1. 查询系统站点总数：
<query_n></query_n>

2. 查询站点 u 的净收益：
<query_value>u</query_value>

3. 查询站点 u 的所有下游站点（返回升序列表，若 u 为终点站则返回空列表）：
<query_children>u</query_children>

4. 查询站点 u 是否为终点站：
<query_isleaf>u</query_isleaf>

5. 查询站点 u 的直属上游站点（若 u=1 则返回 NONE）：
<query_parent>u</query_parent>

6. 验证并查询一条完整通行路线的总收益（路线必须以 1 开头、以某终点站结尾，且相邻站点为上下游关系）：
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. 标注（仅作记录，不触发信息回应，不计入查询次数）：
<note>你的标注内容</note>

## 裁判回应格式

- 对 query_n：返回站点总数
- 对 query_value：返回该站点的净收益值
- 对 query_children：返回下游站点列表（升序），若无下游站点则返回空列表
- 对 query_isleaf：返回"是"或"否"
- 对 query_parent：返回上游站点编号，若为总枢纽则返回"无"
- 对 query_pathsum：若为有效路线则返回总收益，否则返回"无效路径"
- 对 note：不回应

## 提交答案

当你收集到足够信息后，可以提交最终方案。格式如下：

<answer>path=1,a2,a3,...,L;sum=S</answer>

其中 path 是从总枢纽到终点站的完整路线（用逗号分隔），sum 是该路线的净收益总和。

判定标准：
- path 必须是有效的完整通行路线
- sum 必须与该路线的真实总收益一致
- 该总收益必须是所有完整路线中的最大值

若方案正确，返回"答案正确"；否则返回"答案错误"。

## 注意事项

- 请尽可能减少查询次数
- 每次只能进行一个查询
- 格式错误的查询不会被响应
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct an "Optimal Traffic Network Route Planning" task. Here are the rules:

The system involves an unknown traffic network structure with stations numbered from 1 to N, where station 1 is the main hub. Each station u has an integer net benefit w(u) (representing passenger revenue minus operational costs), which can be positive, zero, or negative. Route connections between stations have no independent weights.

Your goal is: among all possible routes from the main hub to any terminal station, find the one with the maximum sum of station net benefits, and determine that total benefit. It is guaranteed that all complete route sums are distinct, so a unique optimal route exists.

Initially, you only know the main hub is numbered 1. The rest of the network structure and station benefits are unknown. You must gradually gather information through local queries.

## Query Rules

Each time you can only query about one station or one candidate route. Batch requests for the entire network or entire levels are not allowed.

Allowed query types (strictly follow XML format):

1. Query total number of stations:
<query_n></query_n>

2. Query the net benefit of station u:
<query_value>u</query_value>

3. Query all downstream stations of station u (returns sorted list; empty if u is a terminal station):
<query_children>u</query_children>

4. Query whether station u is a terminal station:
<query_isleaf>u</query_isleaf>

5. Query the direct upstream station of u (returns NONE if u=1):
<query_parent>u</query_parent>

6. Verify and query the total benefit of a complete route (must start with 1, end at a terminal station, with adjacent stations being upstream-downstream):
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. Note (for annotation only, no response, does not count as a query):
<note>your annotation</note>

## Judge Response Format

- For query_n: returns total number of stations
- For query_value: returns the station's net benefit value
- For query_children: returns list of downstream stations (sorted); empty list if none
- For query_isleaf: returns "Yes" or "No"
- For query_parent: returns upstream station number; "None" if main hub
- For query_pathsum: returns total benefit if valid route; "Invalid path" otherwise
- For note: no response

## Submit Answer

When you have gathered enough information, submit your final plan in this format:

<answer>path=1,a2,a3,...,L;sum=S</answer>

where path is the complete route from the main hub to a terminal station (comma-separated), and sum is the total net benefit of that route.

Judgment criteria:
- path must be a valid complete route
- sum must match the actual total benefit of that route
- that sum must be the maximum among all complete routes

If correct, returns "Correct answer"; otherwise returns "Incorrect answer".

## Notes

- Try to minimize the number of queries
- Only one query per turn
- Incorrectly formatted queries will not be responded to
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
我们来进行一项“最优临床诊疗路径推演”任务。规则如下：

系统设定了一套未知结构的临床诊疗决策树，诊疗步骤（节点）编号为 1 到 N，初始接诊步骤编号为 1。每个步骤 u 都有一个整数效用得分 w(u)（代表对患者健康改善或确诊的综合贡献），可以是正数、零或负数。步骤间的流转本身没有独立权重。

你的目标是：在所有从初始接诊到最终确诊方案（终端步骤）的完整诊疗路径中，找出效用得分之和最大的那条路径，以及该路径的总得分。保证所有完整诊疗路径的总得分两两不同，即唯一最优路径一定存在。

初始时你只知道初始接诊步骤的编号是 1，其余的决策树结构和步骤得分都是未知的。你需要通过局部查询逐步获得信息。

## 查询规则

每次你只能对一个诊疗步骤或一条候选路径发起一次查询。不允许请求全局决策树或整层步骤的批量信息。

允许的查询类型如下（请严格按照 XML 格式）：

1. 查询步骤总数：
<query_n></query_n>

2. 查询步骤 u 的效用得分：
<query_value>u</query_value>

3. 查询步骤 u 的所有后续步骤（返回升序列表，若 u 为终端步骤则返回空列表）：
<query_children>u</query_children>

4. 查询步骤 u 是否为最终的确诊终端步骤：
<query_isleaf>u</query_isleaf>

5. 查询步骤 u 的直属前置步骤（若 u=1 则返回 NONE）：
<query_parent>u</query_parent>

6. 验证并查询一条完整诊疗路径的总得分（路径必须以 1 开头、以某终端步骤结尾，且相邻步骤为前后置关系）：
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. 标注（仅作记录，不触发信息回应，不计入查询次数）：
<note>你的标注内容</note>

## 裁判回应格式

- 对 query_n：返回步骤总数
- 对 query_value：返回该步骤的效用得分
- 对 query_children：返回后续步骤列表（升序），若无后续步骤则返回空列表
- 对 query_isleaf：返回"是"或"否"
- 对 query_parent：返回前置步骤编号，若为初始步骤则返回"无"
- 对 query_pathsum：若为有效诊疗路径则返回总得分，否则返回"无效路径"
- 对 note：不回应

## 提交答案

当你收集到足够信息后，可以提交最终临床路径。格式如下：

<answer>path=1,a2,a3,...,L;sum=S</answer>

其中 path 是从初始接诊到终端步骤的完整路径（用逗号分隔），sum 是该路径的效用总得分。

判定标准：
- path 必须是有效的完整诊疗路径
- sum 必须与该路径的真实总得分一致
- 该总得分必须是所有完整路径中的最大值

若路径正确，返回"答案正确"；否则返回"答案错误"。

## 注意事项

- 请尽可能减少查询次数
- 每次只能进行一个查询
- 格式错误的查询不会被响应
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct an "Optimal Clinical Pathway Deduction" task. Here are the rules:

The system involves an unknown clinical decision tree structure with medical steps (nodes) numbered from 1 to N, where the initial consultation step is numbered 1. Each step u has an integer utility score w(u) (representing the comprehensive contribution to the patient's health improvement or diagnosis certainty), which can be positive, zero, or negative. Transitions between steps have no independent weights.

Your goal is: among all complete clinical pathways from the initial consultation to any final diagnostic regimen (terminal step), find the one with the maximum sum of utility scores, and determine that total score. It is guaranteed that all complete pathway sums are distinct, so a unique optimal pathway exists.

Initially, you only know the initial step is numbered 1. The rest of the decision tree structure and step scores are unknown. You must gradually gather information through local queries.

## Query Rules

Each time you can only query about one medical step or one candidate pathway. Batch requests for the entire decision tree or entire levels are not allowed.

Allowed query types (strictly follow XML format):

1. Query total number of steps:
<query_n></query_n>

2. Query the utility score of step u:
<query_value>u</query_value>

3. Query all subsequent steps of step u (returns sorted list; empty if u is a terminal step):
<query_children>u</query_children>

4. Query whether step u is a final terminal step:
<query_isleaf>u</query_isleaf>

5. Query the direct prerequisite step of u (returns NONE if u=1):
<query_parent>u</query_parent>

6. Verify and query the total score of a complete clinical pathway (must start with 1, end at a terminal step, with adjacent steps having a prerequisite-subsequent relationship):
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. Note (for annotation only, no response, does not count as a query):
<note>your annotation</note>

## Judge Response Format

- For query_n: returns total number of steps
- For query_value: returns the step's utility score
- For query_children: returns list of subsequent steps (sorted); empty list if none
- For query_isleaf: returns "Yes" or "No"
- For query_parent: returns prerequisite step number; "None" if initial step
- For query_pathsum: returns total score if valid pathway; "Invalid path" otherwise
- For note: no response

## Submit Answer

When you have gathered enough information, submit your final pathway in this format:

<answer>path=1,a2,a3,...,L;sum=S</answer>

where path is the complete pathway from the initial to a terminal step (comma-separated), and sum is the total utility score of that pathway.

Judgment criteria:
- path must be a valid complete clinical pathway
- sum must match the actual total score of that pathway
- that sum must be the maximum among all complete pathways

If correct, returns "Correct answer"; otherwise returns "Incorrect answer".

## Notes

- Try to minimize the number of queries
- Only one query per turn
- Incorrectly formatted queries will not be responded to
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
我们来进行一项“个性化学习路线最优化”任务。规则如下：

游戏设定了一个未知结构的学科知识树，学习模块编号为 1 到 N，基础起点模块编号为 1。每个学习模块 u 有一个整数的能力提升值 w(u)（代表掌握该模块带来的综合收益），可以是正数、零或负数。模块间的前置依赖关系没有权重。

你的目标是：在所有从基础起点到高阶专业方向（终端模块）的完整学习路线中，找出能力提升值之和最大的那条路线，以及该路线的总提升值。保证所有完整路线的总提升值两两不同，即唯一最优路线一定存在。

初始时你只知道基础起点的编号是 1，其余的学科树结构和模块提升值都是未知的。你需要通过局部查询逐步获得信息。

## 查询规则

每次你只能对一个学习模块或一条候选路线发起一次查询。不允许请求全局学科树或整层模块的批量信息。

允许的查询类型如下（请严格按照 XML format）：

1. 查询学习模块总数：
<query_n></query_n>

2. 查询模块 u 的能力提升值：
<query_value>u</query_value>

3. 查询模块 u 的所有后续衍生模块（返回升序列表，若 u 为终端方向则返回空列表）：
<query_children>u</query_children>

4. 查询模块 u 是否为终端高阶方向：
<query_isleaf>u</query_isleaf>

5. 查询模块 u 的直接先修模块（若 u=1 则返回 NONE）：
<query_parent>u</query_parent>

6. 验证并查询一条完整学习路线的总提升值（路线必须以 1 开头、以某终端模块结尾，且相邻模块为先修-衍生关系）：
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. 标注（仅作记录，不触发信息回应，不计入查询次数）：
<note>你的标注内容</note>

## 裁判回应格式

- 对 query_n：返回模块总数
- 对 query_value：返回该模块的能力提升值
- 对 query_children：返回后续模块列表（升序），若无后续模块则返回空列表
- 对 query_isleaf：返回"是"或"否"
- 对 query_parent：返回先修模块编号，若为基础起点则返回"无"
- 对 query_pathsum：若为有效路线则返回总提升值，否则返回"无效路径"
- 对 note：不回应

## 提交答案

当你收集到足够信息后，可以提交最终学习路线。格式如下：

<answer>path=1,a2,a3,...,L;sum=S</answer>

其中 path 是从基础起点到终端模块的完整路线（用逗号分隔），sum 是该路线的能力提升总和。

判定标准：
- path 必须是有效的完整学习路线
- sum 必须与该路线的真实总提升值一致
- 该总提升值必须是所有完整路线中的最大值

若路线正确，返回"答案正确"；否则返回"答案错误"。

## 注意事项

- 请尽可能减少查询次数
- 每次只能进行一个查询
- 格式错误的查询不会被响应
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Personalized Learning Route Optimization" task. Here are the rules:

The system involves an unknown academic knowledge tree structure with learning modules numbered from 1 to N, where the foundational starting module is numbered 1. Each module u has an integer capability enhancement value w(u) (representing the comprehensive benefit of mastering that module), which can be positive, zero, or negative. Prerequisite dependencies between modules have no weights.

Your goal is: among all complete learning routes from the foundational start to any advanced professional direction (terminal module), find the one with the maximum sum of capability enhancement values, and determine that total value. It is guaranteed that all complete route sums are distinct, so a unique optimal route exists.

Initially, you only know the starting module is numbered 1. The rest of the knowledge tree structure and module values are unknown. You must gradually gather information through local queries.

## Query Rules

Each time you can only query about one learning module or one candidate route. Batch requests for the entire knowledge tree or entire levels are not allowed.

Allowed query types (strictly follow XML format):

1. Query total number of learning modules:
<query_n></query_n>

2. Query the capability enhancement value of module u:
<query_value>u</query_value>

3. Query all subsequent derived modules of module u (returns sorted list; empty if u is a terminal direction):
<query_children>u</query_children>

4. Query whether module u is a terminal advanced direction:
<query_isleaf>u</query_isleaf>

5. Query the direct prerequisite module of u (returns NONE if u=1):
<query_parent>u</query_parent>

6. Verify and query the total value of a complete learning route (must start with 1, end at a terminal module, with adjacent modules having a prerequisite-derived relationship):
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. Note (for annotation only, no response, does not count as a query):
<note>your annotation</note>

## Judge Response Format

- For query_n: returns total number of modules
- For query_value: returns the module's capability enhancement value
- For query_children: returns list of subsequent modules (sorted); empty list if none
- For query_isleaf: returns "Yes" or "No"
- For query_parent: returns prerequisite module number; "None" if foundational start
- For query_pathsum: returns total value if valid route; "Invalid path" otherwise
- For note: no response

## Submit Answer

When you have gathered enough information, submit your final learning route in this format:

<answer>path=1,a2,a3,...,L;sum=S</answer>

where path is the complete route from the foundational start to a terminal module (comma-separated), and sum is the total enhancement value of that route.

Judgment criteria:
- path must be a valid complete learning route
- sum must match the actual total value of that route
- that sum must be the maximum among all complete routes

If correct, returns "Correct answer"; otherwise returns "Incorrect answer".

## Notes

- Try to minimize the number of queries
- Only one query per turn
- Incorrectly formatted queries will not be responded to
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
我们来进行一项“工业生产流程价值最大化”任务。规则如下：

游戏设定了一套未知结构的生产工序树，工序编号为 1 到 N，初始原料加工工序编号为 1。每道工序 u 都有一个整数的附加价值 w(u)（代表该道工艺的利润增值扣除损耗），可以是正数、零或负数。工序间的流转本身不产生额外价值。

你的目标是：在所有从初始加工到最终成品入库（终端工序）的生产流水线中，找出附加价值之和最大的那条流水线，以及该流水线的总附加价值。保证所有生产流水线的总价值两两不同，即唯一最优流水线一定存在。

初始时你只知道初始加工工序的编号是 1，其余的工艺结构和工序附加价值都是未知的。你需要通过局部查询逐步获得信息。

## 查询规则

每次你只能对一道生产工序或一条候选流水线发起一次查询。不允许请求全局工艺图或整层工序的批量信息。

允许的查询类型如下（请严格按照 XML 格式）：

1. 查询涉及的生产工序总数：
<query_n></query_n>

2. 查询工序 u 的附加价值：
<query_value>u</query_value>

3. 查询工序 u 的所有下一道候选工序（返回升序列表，若 u 为终端工序则返回空列表）：
<query_children>u</query_children>

4. 查询工序 u 是否为最终的成品终端工序：
<query_isleaf>u</query_isleaf>

5. 查询工序 u 的上一道直属工序（若 u=1 则返回 NONE）：
<query_parent>u</query_parent>

6. 验证并查询一条完整流水线的总价值（流水线必须以 1 开头、以某终端工序结尾，且相邻工序为前后承接关系）：
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. 标注（仅作记录，不触发信息回应，不计入查询次数）：
<note>你的标注内容</note>

## 裁判回应格式

- 对 query_n：返回工序总数
- 对 query_value：返回该工序的附加价值
- 对 query_children：返回后续工序列表（升序），若无则返回空列表
- 对 query_isleaf：返回"是"或"否"
- 对 query_parent：返回上一道工序编号，若为初始加工则返回"无"
- 对 query_pathsum：若为有效流水线则返回总价值，否则返回"无效路径"
- 对 note：不回应

## 提交答案

当你收集到足够信息后，可以提交最优生产流水线。格式如下：

<answer>path=1,a2,a3,...,L;sum=S</answer>

其中 path 是从初始加工到终端成品的完整流水线（用逗号分隔），sum 是该流水线的附加价值总和。

判定标准：
- path 必须是有效的完整流水线
- sum 必须与该流水线的真实总价值一致
- 该总价值必须是所有完整流水线中的最大值

若方案正确，返回"答案正确"；否则返回"答案错误"。

## 注意事项

- 请尽可能减少查询次数
- 每次只能进行一个查询
- 格式错误的查询不会被响应
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct an "Industrial Production Process Value Maximization" task. Here are the rules:

The system involves an unknown production process tree structure with operational steps numbered from 1 to N, where the initial raw material processing step is numbered 1. Each step u has an integer added value w(u) (representing profit increase minus material loss), which can be positive, zero, or negative. Transitions between steps do not generate extra value.

Your goal is: among all complete production assembly lines from the initial processing to final product warehousing (terminal step), find the one with the maximum sum of added values, and determine that total value. It is guaranteed that all complete assembly line sums are distinct, so a unique optimal assembly line exists.

Initially, you only know the initial step is numbered 1. The rest of the process structure and step values are unknown. You must gradually gather information through local queries.

## Query Rules

Each time you can only query about one operational step or one candidate assembly line. Batch requests for the entire process tree or entire levels are not allowed.

Allowed query types (strictly follow XML format):

1. Query total number of operational steps:
<query_n></query_n>

2. Query the added value of step u:
<query_value>u</query_value>

3. Query all potential next steps of step u (returns sorted list; empty if u is a terminal step):
<query_children>u</query_children>

4. Query whether step u is a final terminal product step:
<query_isleaf>u</query_isleaf>

5. Query the direct previous step of u (returns NONE if u=1):
<query_parent>u</query_parent>

6. Verify and query the total value of a complete assembly line (must start with 1, end at a terminal step, with adjacent steps being in sequential order):
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. Note (for annotation only, no response, does not count as a query):
<note>your annotation</note>

## Judge Response Format

- For query_n: returns total number of steps
- For query_value: returns the step's added value
- For query_children: returns list of next steps (sorted); empty list if none
- For query_isleaf: returns "Yes" or "No"
- For query_parent: returns previous step number; "None" if initial processing
- For query_pathsum: returns total value if valid assembly line; "Invalid path" otherwise
- For note: no response

## Submit Answer

When you have gathered enough information, submit your optimal assembly line in this format:

<answer>path=1,a2,a3,...,L;sum=S</answer>

where path is the complete assembly line from initial processing to terminal product (comma-separated), and sum is the total added value of that line.

Judgment criteria:
- path must be a valid complete assembly line
- sum must match the actual total value of that assembly line
- that sum must be the maximum among all complete assembly lines

If correct, returns "Correct answer"; otherwise returns "Incorrect answer".

## Notes

- Try to minimize the number of queries
- Only one query per turn
- Incorrectly formatted queries will not be responded to
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
我们来进行一项“诉讼策略链利益最大化”任务。规则如下：

系统设定了一套未知结构的法律程序决策树，程序或策略节点编号为 1 到 N，初步立案阶段编号为 1。每个策略节点 u 都有一个整数的预期利益 w(u)（代表该策略带来的收益扣除诉讼成本），可以是正数、零或负数。程序间的推进不单独计算利益。

你的目标是：在所有从初步立案到最终结案（终端程序）的完整策略链中，找出预期利益之和最大的那条策略链，以及该策略链的总利益。保证所有完整策略链的总利益两两不同，即唯一最优策略链一定存在。

初始时你只知道初步立案节点的编号是 1，其余的决策树结构和策略预期利益都是未知的。你需要通过局部查询逐步获得信息。

## 查询规则

每次你只能对一个法律程序节点或一条候选策略链发起一次查询。不允许请求全局决策树或整层程序的批量信息。

允许的查询类型如下（请严格按照 XML 格式）：

1. 查询涉及的策略节点总数：
<query_n></query_n>

2. 查询节点 u 的预期利益：
<query_value>u</query_value>

3. 查询节点 u 的所有后续衍生程序（返回升序列表，若 u 为结案程序则返回空列表）：
<query_children>u</query_children>

4. 查询节点 u 是否为最终的结案程序：
<query_isleaf>u</query_isleaf>

5. 查询节点 u 的直接前置程序（若 u=1 则返回 NONE）：
<query_parent>u</query_parent>

6. 验证并查询一条完整策略链的总利益（策略链必须以 1 开头、以某结案程序结尾，且相邻节点为先后程序关系）：
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. 标注（仅作记录，不触发信息回应，不计入查询次数）：
<note>你的标注内容</note>

## 裁判回应格式

- 对 query_n：返回节点总数
- 对 query_value：返回该节点的预期利益
- 对 query_children：返回后续程序列表（升序），若无后续程序则返回空列表
- 对 query_isleaf：返回"是"或"否"
- 对 query_parent：返回前置程序编号，若为初步立案则返回"无"
- 对 query_pathsum：若为有效策略链则返回总利益，否则返回"无效路径"
- 对 note：不回应

## 提交答案

当你收集到足够信息后，可以提交最优诉讼策略。格式如下：

<answer>path=1,a2,a3,...,L;sum=S</answer>

其中 path 是从初步立案到结案程序的完整策略链（用逗号分隔），sum 是该策略链的预期利益总和。

判定标准：
- path 必须是有效的完整策略链
- sum 必须与该策略链的真实总利益一致
- 该总利益必须是所有完整策略链中的最大值

若策略正确，返回"答案正确"；否则返回"答案错误"。

## 注意事项

- 请尽可能减少查询次数
- 每次只能进行一个查询
- 格式错误的查询不会被响应
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's conduct a "Litigation Strategy Chain Benefit Maximization" task. Here are the rules:

The system involves an unknown legal procedure decision tree structure with procedural or strategy nodes numbered from 1 to N, where the preliminary case filing phase is numbered 1. Each node u has an integer expected benefit w(u) (representing the revenue brought by the strategy minus litigation costs), which can be positive, zero, or negative. Transitions between procedures do not carry independent benefits.

Your goal is: among all complete strategy chains from the preliminary case filing to the final case closure (terminal procedure), find the one with the maximum sum of expected benefits, and determine that total benefit. It is guaranteed that all complete strategy chain sums are distinct, so a unique optimal strategy chain exists.

Initially, you only know the preliminary case filing node is numbered 1. The rest of the decision tree structure and expected benefits are unknown. You must gradually gather information through local queries.

## Query Rules

Each time you can only query about one legal procedural node or one candidate strategy chain. Batch requests for the entire decision tree or entire levels are not allowed.

Allowed query types (strictly follow XML format):

1. Query total number of strategy nodes:
<query_n></query_n>

2. Query the expected benefit of node u:
<query_value>u</query_value>

3. Query all subsequent derived procedures of node u (returns sorted list; empty if u is a case closure procedure):
<query_children>u</query_children>

4. Query whether node u is a final case closure procedure:
<query_isleaf>u</query_isleaf>

5. Query the direct preceding procedure of u (returns NONE if u=1):
<query_parent>u</query_parent>

6. Verify and query the total benefit of a complete strategy chain (must start with 1, end at a case closure procedure, with adjacent nodes having a consecutive procedural relationship):
<query_pathsum>v1,v2,...,vk</query_pathsum>

7. Note (for annotation only, no response, does not count as a query):
<note>your annotation</note>

## Judge Response Format

- For query_n: returns total number of nodes
- For query_value: returns the node's expected benefit
- For query_children: returns list of subsequent procedures (sorted); empty list if none
- For query_isleaf: returns "Yes" or "No"
- For query_parent: returns preceding procedure number; "None" if preliminary case filing
- For query_pathsum: returns total benefit if valid strategy chain; "Invalid path" otherwise
- For note: no response

## Submit Answer

When you have gathered enough information, submit your optimal litigation strategy in this format:

<answer>path=1,a2,a3,...,L;sum=S</answer>

where path is the complete strategy chain from preliminary filing to case closure (comma-separated), and sum is the total expected benefit of that chain.

Judgment criteria:
- path must be a valid complete strategy chain
- sum must match the actual total benefit of that strategy chain
- that sum must be the maximum among all complete strategy chains

If correct, returns "Correct answer"; otherwise returns "Incorrect answer".

## Notes

- Try to minimize the number of queries
- Only one query per turn
- Incorrectly formatted queries will not be responded to
"""

    tags = ["answer", "query_n", "query_value", "query_children", "query_isleaf", 
            "query_parent", "query_pathsum", "note"]
    
    reasoning_type = "演绎推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "tree": {
                    1: {"weight": 10, "children": [2, 3]},
                    2: {"weight": 5, "children": [4]},
                    3: {"weight": -3, "children": [5]},
                    4: {"weight": 8, "children": []},
                    5: {"weight": 20, "children": []},
                },
                "max_path": [1, 3, 5],
                "max_sum": 27,
            },
            2: {
                "n": 8,
                "tree": {
                    1: {"weight": 5, "children": [2, 3]},
                    2: {"weight": 10, "children": [4, 5]},
                    3: {"weight": -5, "children": [6]},
                    4: {"weight": 3, "children": []},
                    5: {"weight": -2, "children": [7, 8]},
                    6: {"weight": 15, "children": []},
                    7: {"weight": 20, "children": []},
                    8: {"weight": 1, "children": []},
                },
                "max_path": [1, 2, 5, 7],
                "max_sum": 33,
            },
            3: {
                "n": 10,
                "tree": {
                    1: {"weight": 8, "children": [2, 3]},
                    2: {"weight": -3, "children": [4, 5]},
                    3: {"weight": 6, "children": [6, 7]},
                    4: {"weight": 15, "children": [8]},
                    5: {"weight": -10, "children": [9, 10]},
                    6: {"weight": -2, "children": []},
                    7: {"weight": 12, "children": []},
                    8: {"weight": 5, "children": []},
                    9: {"weight": 29, "children": []},
                    10: {"weight": -5, "children": []},
                },
                "max_path": [1, 3, 7],
                "max_sum": 26,
            },
            4: {
                "n": 12,
                "tree": {
                    1: {"weight": 12, "children": [2, 3]},
                    2: {"weight": -8, "children": [4, 5, 6]},
                    3: {"weight": 5, "children": [7, 8]},
                    4: {"weight": 25, "children": []},
                    5: {"weight": 18, "children": [9, 10]},
                    6: {"weight": -15, "children": []},
                    7: {"weight": -3, "children": [11, 12]},
                    8: {"weight": 8, "children": []},
                    9: {"weight": -5, "children": []},
                    10: {"weight": 22, "children": []},
                    11: {"weight": 30, "children": []},
                    12: {"weight": -8, "children": []},
                },
                "max_path": [1, 3, 7, 11],
                "max_sum": 44,
            },
            5: {
                "n": 15,
                "tree": {
                    1: {"weight": 20, "children": [2, 3]},
                    2: {"weight": -15, "children": [4, 5, 6]},
                    3: {"weight": 10, "children": [7, 8]},
                    4: {"weight": 8, "children": [9]},
                    5: {"weight": 25, "children": [10, 11]},
                    6: {"weight": -20, "children": []},
                    7: {"weight": -8, "children": [12, 13]},
                    8: {"weight": 15, "children": [14, 15]},
                    9: {"weight": 40, "children": []},
                    10: {"weight": -10, "children": []},
                    11: {"weight": 35, "children": []},
                    12: {"weight": 28, "children": []},
                    13: {"weight": -12, "children": []},
                    14: {"weight": -5, "children": []},
                    15: {"weight": 30, "children": []},
                },
                "max_path": [1, 3, 8, 15],
                "max_sum": 75,
            },
        },
        "en": {
            1: {
                "n": 5,
                "tree": {
                    1: {"weight": 10, "children": [2, 3]},
                    2: {"weight": 5, "children": [4]},
                    3: {"weight": -3, "children": [5]},
                    4: {"weight": 8, "children": []},
                    5: {"weight": 20, "children": []},
                },
                "max_path": [1, 3, 5],
                "max_sum": 27,
            },
            2: {
                "n": 8,
                "tree": {
                    1: {"weight": 5, "children": [2, 3]},
                    2: {"weight": 10, "children": [4, 5]},
                    3: {"weight": -5, "children": [6]},
                    4: {"weight": 3, "children": []},
                    5: {"weight": -2, "children": [7, 8]},
                    6: {"weight": 15, "children": []},
                    7: {"weight": 20, "children": []},
                    8: {"weight": 1, "children": []},
                },
                "max_path": [1, 2, 5, 7],
                "max_sum": 33,
            },
            3: {
                "n": 10,
                "tree": {
                    1: {"weight": 8, "children": [2, 3]},
                    2: {"weight": -3, "children": [4, 5]},
                    3: {"weight": 6, "children": [6, 7]},
                    4: {"weight": 15, "children": [8]},
                    5: {"weight": -10, "children": [9, 10]},
                    6: {"weight": -2, "children": []},
                    7: {"weight": 12, "children": []},
                    8: {"weight": 5, "children": []},
                    9: {"weight": 29, "children": []},
                    10: {"weight": -5, "children": []},
                },
                "max_path": [1, 3, 7],
                "max_sum": 26,
            },
            4: {
                "n": 12,
                "tree": {
                    1: {"weight": 12, "children": [2, 3]},
                    2: {"weight": -8, "children": [4, 5, 6]},
                    3: {"weight": 5, "children": [7, 8]},
                    4: {"weight": 25, "children": []},
                    5: {"weight": 18, "children": [9, 10]},
                    6: {"weight": -15, "children": []},
                    7: {"weight": -3, "children": [11, 12]},
                    8: {"weight": 8, "children": []},
                    9: {"weight": -5, "children": []},
                    10: {"weight": 22, "children": []},
                    11: {"weight": 30, "children": []},
                    12: {"weight": -8, "children": []},
                },
                "max_path": [1, 3, 7, 11],
                "max_sum": 44,
            },
            5: {
                "n": 15,
                "tree": {
                    1: {"weight": 20, "children": [2, 3]},
                    2: {"weight": -15, "children": [4, 5, 6]},
                    3: {"weight": 10, "children": [7, 8]},
                    4: {"weight": 8, "children": [9]},
                    5: {"weight": 25, "children": [10, 11]},
                    6: {"weight": -20, "children": []},
                    7: {"weight": -8, "children": [12, 13]},
                    8: {"weight": 15, "children": [14, 15]},
                    9: {"weight": 40, "children": []},
                    10: {"weight": -10, "children": []},
                    11: {"weight": 35, "children": []},
                    12: {"weight": 28, "children": []},
                    13: {"weight": -12, "children": []},
                    14: {"weight": -5, "children": []},
                    15: {"weight": 30, "children": []},
                },
                "max_path": [1, 3, 8, 15],
                "max_sum": 75,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，加载树结构"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 加载树结构
        self.tree = cfg["tree"]
        self.max_path = cfg["max_path"]
        self.max_sum = cfg["max_sum"]
        
        # 构建父节点映射
        self.parent_map = {1: None}
        for node_id, node_info in self.tree.items():
            for child in node_info["children"]:
                self.parent_map[child] = node_id

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            parts = raw_ans.split(";")
            path_part = None
            sum_part = None
            
            for part in parts:
                part = part.strip()
                if part.startswith("path="):
                    path_part = part[5:].strip()
                elif part.startswith("sum="):
                    sum_part = part[4:].strip()
            
            if not path_part or not sum_part:
                return False
            
            # 解析路径
            submitted_path = [int(x.strip()) for x in path_part.split(",")]
            submitted_sum = int(sum_part)
            
            # 验证路径有效性
            if not self._is_valid_path(submitted_path):
                return False
            
            # 验证总和是否正确
            actual_sum = self._calculate_path_sum(submitted_path)
            if actual_sum != submitted_sum:
                return False
            
            # 验证是否为最大路径（与预计算的最大值比较）
            return actual_sum == self.max_sum
            
        except:
            return False

    def _is_valid_path(self, path):
        """验证路径是否有效（从根到叶，相邻节点为父子关系）"""
        if not path or path[0] != 1:
            return False
        
        for i in range(len(path) - 1):
            curr = path[i]
            next_node = path[i + 1]
            if curr not in self.tree or next_node not in self.tree[curr]["children"]:
                return False
        
        # 最后一个节点必须是叶子
        last_node = path[-1]
        if last_node not in self.tree or len(self.tree[last_node]["children"]) > 0:
            return False
        
        return True

    def _calculate_path_sum(self, path):
        """计算路径的权重总和"""
        return sum(self.tree[node]["weight"] for node in path)

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        # 从 parsed_info 中移除 note，然后处理剩余查询
        working_info = {k: v for k, v in parsed_info.items() if k != "note"}
        
        if not working_info:
            # 仅有 note 标签
            # 根据规则，note 不应触发回应
            # 但 step() 的流程要求 produce_response 返回字符串
            # 返回一个最小化的确认，告知继续提问
            if is_zh:
                return "请继续你的查询。"
            else:
                return "Please continue with your query."
        
        # query_n: 查询节点总数
        if "query_n" in working_info:
            return str(self._game_info["n"])
        
        # query_value: 查询节点权重
        if "query_value" in working_info:
            try:
                node_id = int(working_info["query_value"].strip())
                if node_id not in self.tree:
                    return "节点不存在" if is_zh else "Node does not exist"
                return str(self.tree[node_id]["weight"])
            except:
                return "格式错误" if is_zh else "Format error"
        
        # query_children: 查询子节点列表
        if "query_children" in working_info:
            try:
                node_id = int(working_info["query_children"].strip())
                if node_id not in self.tree:
                    return "节点不存在" if is_zh else "Node does not exist"
                children = self.tree[node_id]["children"]
                return str(children)
            except:
                return "格式错误" if is_zh else "Format error"
        
        # query_isleaf: 查询是否为叶节点
        if "query_isleaf" in working_info:
            try:
                node_id = int(working_info["query_isleaf"].strip())
                if node_id not in self.tree:
                    return "节点不存在" if is_zh else "Node does not exist"
                is_leaf = len(self.tree[node_id]["children"]) == 0
                if is_leaf:
                    return "是" if is_zh else "Yes"
                else:
                    return "否" if is_zh else "No"
            except:
                return "格式错误" if is_zh else "Format error"
        
        # query_parent: 查询父节点
        if "query_parent" in working_info:
            try:
                node_id = int(working_info["query_parent"].strip())
                if node_id not in self.tree:
                    return "节点不存在" if is_zh else "Node does not exist"
                parent = self.parent_map.get(node_id)
                if parent is None:
                    return "无" if is_zh else "None"
                return str(parent)
            except:
                return "格式错误" if is_zh else "Format error"
        
        # query_pathsum: 查询路径总和
        if "query_pathsum" in working_info:
            try:
                path_str = working_info["query_pathsum"].strip()
                path = [int(x.strip()) for x in path_str.split(",")]
                if self._is_valid_path(path):
                    path_sum = self._calculate_path_sum(path)
                    return str(path_sum)
                else:
                    return "无效路径" if is_zh else "Invalid path"
            except:
                return "格式错误" if is_zh else "Format error"
        
        return "无效查询" if is_zh else "Invalid query"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        is_zh = self.config.language == "zh"
        n = self._game_info["n"]

        # 1. query_n
        queries.append({
            "query": "<query_n></query_n>",
            "answer": str(n)
        })

        # 2-5. 遍历所有节点的相关查询
        for u in range(1, n + 1):
            if u not in self.tree:
                continue

            # query_value
            w = self.tree[u]["weight"]
            queries.append({
                "query": f"<query_value>{u}</query_value>",
                "answer": str(w)
            })

            # query_children
            children = self.tree[u]["children"]
            queries.append({
                "query": f"<query_children>{u}</query_children>",
                "answer": str(children)
            })

            # query_isleaf
            is_leaf = len(children) == 0
            if is_zh:
                ans_leaf = "是" if is_leaf else "否"
            else:
                ans_leaf = "Yes" if is_leaf else "No"
            queries.append({
                "query": f"<query_isleaf>{u}</query_isleaf>",
                "answer": ans_leaf
            })

            # query_parent
            parent = self.parent_map.get(u)
            if parent is None:
                ans_parent = "无" if is_zh else "None"
            else:
                ans_parent = str(parent)
            queries.append({
                "query": f"<query_parent>{u}</query_parent>",
                "answer": ans_parent
            })

        # 6. query_pathsum: 遍历所有有效的根到叶路径
        # DFS 查找所有从根(1)到叶节点的路径
        stack = [[1]]
        valid_paths = []
        
        while stack:
            current_path = stack.pop()
            curr_node = current_path[-1]
            children = self.tree[curr_node]["children"]
            
            if not children:
                # 已经是叶节点，记录路径
                valid_paths.append(current_path)
            else:
                # 继续延伸
                for child in children:
                    stack.append(current_path + [child])
        
        for path in valid_paths:
            path_str = ",".join(str(x) for x in path)
            total_sum = self._calculate_path_sum(path)
            queries.append({
                "query": f"<query_pathsum>{path_str}</query_pathsum>",
                "answer": str(total_sum)
            })

        return queries

    def _cf_make_wrong(self, correct):
        """生成一个错误的回复"""
        # 若 correct 是纯整数字符串
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        # 中文替换
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        # 英文替换
        lower = correct.lower()
        if lower == "yes":
            if correct == "YES": return "NO"
            if correct == "Yes": return "No"
            return "no"
        if lower == "no":
            if correct == "NO": return "YES"
            if correct == "No": return "Yes"
            return "yes"

        # 中文特殊回复
        if correct == "无":
            return "1"
        if correct == "无效路径":
            return "0"
        if correct == "节点不存在":
            return "0"
        
        # 英文特殊回复
        if correct == "None":
            return "1"
        if correct == "Invalid path":
            return "0"
        if correct == "Node does not exist":
            return "0"
        if correct == "Format error":
            return "0"
        if correct == "格式错误":
            return "0"
        
        # 列表字符串（如 "[2, 3]"）
        if correct.startswith("[") and correct.endswith("]"):
            try:
                lst = eval(correct)
                if isinstance(lst, list):
                    if len(lst) == 0:
                        return "[0]"
                    else:
                        # 修改第一个元素
                        modified = lst.copy()
                        modified[0] = modified[0] + 1
                        return str(modified)
            except:
                pass

        # note 回复
        if correct in ["（已记录标注）", "(Note recorded)"]:
            return "（错误标注）" if "已记录" in correct else "(Wrong note)"
        if correct in ["请继续你的查询。", "Please continue with your query."]:
            return "停止查询。" if "请继续" in correct else "Stop querying."
        
        # 都不匹配，添加错误后缀
        return correct + "_WRONG"