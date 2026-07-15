from .base import Game
import random

class TreeTraversalRuleGame(Game):
    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树遍历规则推理"游戏，规则如下：

游戏设定了一棵有根树，根节点为1，树结构如下：
- 节点1的子节点：{{2, 3, 4}}
- 节点2的子节点：{{5, 6}}
- 节点3的子节点：{{7}}
- 节点4的子节点：{{8, 9, 10}}
- 节点7的子节点：{{11}}
- 其余节点均为叶节点

我已秘密选定了一种"子节点排序规则"，并使用该规则对这棵树进行前序遍历。前序遍历的定义是：到达某节点后立刻计为已访问，然后按照该节点子节点的特定排序规则，依次递归访问每个子树。

子节点排序规则只可能是以下四种之一（全局固定但未知）：
- A. 全局升序：每个父节点处，子节点按编号升序访问
- B. 全局降序：每个父节点处，子节点按编号降序访问
- C. 奇数优先：每个父节点处，先访问奇数编号子节点（按升序），再访问偶数编号子节点（按升序）
- D. 层次交替升降：根深度为0；深度为偶数的父节点，其子节点按升序访问；深度为奇数的父节点，其子节点按降序访问

你的目标是：
1. 识别当前启用的排序规则（A/B/C/D）
2. 确定节点{target_node}在前序遍历中的访问序号（第几个被访问，从1开始计数）

你可以使用以下三种查询方式（每种查询有次数限制）：

1. 窥视前缀：查询前序序列的前k个节点编号（k的取值范围：1到3）
2. 成对比较：查询两个节点u和v中哪个更早被访问
3. 最先孩子：查询某个父节点p的子节点中，哪个最先被访问

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次只能提交一个查询或答案。请使用以下XML格式：

- 窥视前缀查询（例如查看前3个节点）：
<query_peek>3</query_peek>

- 成对比较查询（例如比较节点2和节点5）：
<query_compare>2,5</query_compare>

- 最先孩子查询（例如查询节点1的最先访问子节点）：
<query_first_child>1</query_first_child>

- 提交最终答案时，必须说明规则类型（A、B、C或D）和目标节点的序号，格式如下：
<answer>rule=A, position=5</answer>
"""

    game_rule_en = """\
Let's play a "Tree Traversal Rule Inference" game. Here are the rules:

A rooted tree is defined with root node 1, structured as follows:
- Node 1's children: {{2, 3, 4}}
- Node 2's children: {{5, 6}}
- Node 3's children: {{7}}
- Node 4's children: {{8, 9, 10}}
- Node 7's children: {{11}}
- All other nodes are leaf nodes

I have secretly selected a "child node sorting rule" and used it to perform a pre-order traversal of this tree. Pre-order traversal is defined as: when reaching a node, it is immediately counted as visited, then each child subtree is recursively visited according to a specific sorting rule for that node's children.

The child node sorting rule can only be one of the following four (globally fixed but unknown):
- A. Global Ascending: At each parent node, children are visited in ascending order by ID
- B. Global Descending: At each parent node, children are visited in descending order by ID
- C. Odd Priority: At each parent node, odd-numbered children are visited first (in ascending order), then even-numbered children (in ascending order)
- D. Level Alternating: Root has depth 0; for parents at even depth, children are visited in ascending order; for parents at odd depth, children are visited in descending order

Your goals are:
1. Identify the active sorting rule (A/B/C/D)
2. Determine the visit position of node {target_node} in the pre-order traversal (which position it is visited, counting from 1)

You can use the following three types of queries (each type has usage limits):

1. Peek Prefix: Query the first k node IDs in the pre-order sequence (k ranges from 1 to 3)
2. Pairwise Comparison: Query which of two nodes u and v is visited earlier
3. First Child: Query which child of a parent node p is visited first

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each turn you can only submit one query or answer. Use the following XML format:

- Peek prefix query (e.g., view first 3 nodes):
<query_peek>3</query_peek>

- Pairwise comparison query (e.g., compare node 2 and node 5):
<query_compare>2,5</query_compare>

- First child query (e.g., query the first visited child of node 1):
<query_first_child>1</query_first_child>

- When submitting the final answer, specify the rule type (A, B, C, or D) and the target node's position:
<answer>rule=A, position=5</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通调度系统。我们要确定一条“巡逻车路线规则”。

系统设定了一个具有层级结构的交通路网，根节点（总调度中心）为1，路口连接如下：
- 节点1的下级路口：{{2, 3, 4}}
- 节点2的下级路口：{{5, 6}}
- 节点3的下级路口：{{7}}
- 节点4的下级路口：{{8, 9, 10}}
- 节点7的下级路口：{{11}}
- 其余节点均为末端路口

我已秘密选定了一种“下级路口优先级规则”，并指挥巡逻车对路网进行深度优先的调度巡逻（前序遍历）。即到达某路口立刻计为已巡逻，然后按特定规则依次递归巡逻各个下属分支。

下级路口优先级规则只可能是以下四种之一（全局固定但未知）：
- A. 全局升序：每个分岔路口处，下级路口按编号升序巡逻
- B. 全局降序：每个分岔路口处，下级路口按编号降序巡逻
- C. 干道优先（奇数优先）：每个分岔路口处，先巡逻干道（奇数编号，按升序），再巡逻支路（偶数编号，按升序）
- D. 区域级别交替：总中心区域级别为0；区域级别为偶数的路口，其下级路口按升序巡逻；区域级别为奇数的路口，其下级路口按降序巡逻

你的目标是：
1. 识别当前启用的优先级规则（A/B/C/D）
2. 确定路口{target_node}在巡逻序列中的访问序号（第几个被巡逻，从1开始计数）

你可以使用以下三种调度查询（每种查询有次数限制）：
1. 窥视前缀：查询巡逻序列的前k个路口编号（k的取值范围：1到3）
2. 成对比较：查询两个路口u和v中哪个更早被巡逻
3. 最先孩子：查询某个分岔路口p的下级路口中，哪个最先被巡逻

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，调度任务失败。

每次只能提交一个查询或答案。请使用以下XML格式：
- 窥视前缀查询（例如查看前3个路口）：<query_peek>3</query_peek>
- 成对比较查询（例如比较路口2和5）：<query_compare>2,5</query_compare>
- 最先孩子查询（例如查询路口1的最先巡逻下级）：<query_first_child>1</query_first_child>
- 提交最终答案时，必须说明规则类型（A、B、C或D）和目标路口的序号：<answer>rule=A, position=5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the intelligent traffic dispatch system. Let's determine the "Patrol Route Rule".

The system defines a hierarchical traffic network with root node 1 (Central Dispatch) structured as follows:
- Node 1's subordinate junctions: {{2, 3, 4}}
- Node 2's subordinate junctions: {{5, 6}}
- Node 3's subordinate junctions: {{7}}
- Node 4's subordinate junctions: {{8, 9, 10}}
- Node 7's subordinate junctions: {{11}}
- All other nodes are terminal junctions

I have secretly selected a "subordinate junction priority rule" and used it to command a patrol car for a depth-first dispatch patrol (pre-order traversal). Reaching a junction immediately counts as patrolled, then each subordinate branch is recursively patrolled according to the specific rule.

The priority rule can only be one of the following four (globally fixed but unknown):
- A. Global Ascending: At each fork, subordinate junctions are patrolled in ascending order by ID
- B. Global Descending: At each fork, subordinate junctions are patrolled in descending order by ID
- C. Main Road Priority (Odd Priority): At each fork, main roads (odd IDs) are patrolled first (in ascending order), then branch roads (even IDs) (in ascending order)
- D. Level Alternating: Central Dispatch level is 0; for junctions at even levels, subordinates are patrolled in ascending order; for junctions at odd levels, subordinates are patrolled in descending order

Your goals are:
1. Identify the active priority rule (A/B/C/D)
2. Determine the patrol position of junction {target_node} in the sequence (which position it is patrolled, counting from 1)

You can use the following three types of queries (with usage limits):
1. Peek Prefix: Query the first k junction IDs in the patrol sequence (k ranges from 1 to 3)
2. Pairwise Comparison: Query which of two junctions u and v is patrolled earlier
3. First Child: Query which subordinate junction of a fork p is patrolled first

Submit your final answer when ready.

Each turn you can only submit one query or answer. Use the following XML format:
- Peek prefix query (e.g., view first 3 junctions): <query_peek>3</query_peek>
- Pairwise comparison query (e.g., compare junction 2 and 5): <query_compare>2,5</query_compare>
- First child query (e.g., query the first patrolled subordinate of junction 1): <query_first_child>1</query_first_child>
- Final answer (specify rule A/B/C/D and target junction's position): <answer>rule=A, position=5</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用医院智能物流系统。我们要推理解析一台“物资配送机器人的导航规则”。

医院的科室被划分为一棵多级树状结构，根节点（分诊总台/物流中心）为1，科室分布如下：
- 节点1的下级科室：{{2, 3, 4}}
- 节点2的下级科室：{{5, 6}}
- 节点3的下级科室：{{7}}
- 节点4的下级科室：{{8, 9, 10}}
- 节点7的下级科室：{{11}}
- 其余节点均为末端病房

我已秘密选定了一种“子科室排序规则”，机器人依据该规则对所有科室进行深度优先的配送（前序遍历）。即到达某科室立刻计为已配送，然后按特定规则依次递归配送其所有下级科室。

子科室排序规则只可能是以下四种之一（全局固定但未知）：
- A. 全局升序：每个上级科室处，下级科室按编号升序配送
- B. 全局降序：每个上级科室处，下级科室按编号降序配送
- C. 急诊优先（奇数优先）：每个上级科室处，先配送急诊/特殊科室（奇数编号，按升序），再配送普通病房（偶数编号，按升序）
- D. 楼层交替：总台楼层深度为0；深度为偶数的科室，其下级科室按升序配送；深度为奇数的科室，其下级科室按降序配送

你的目标是：
1. 识别当前启用的排序规则（A/B/C/D）
2. 确定科室{target_node}在配送序列中的访问序号（第几个被配送，从1开始计数）

你可以使用以下三种调度查询（每种查询有次数限制）：
1. 窥视前缀：查询配送序列的前k个科室编号（k的取值范围：1到3）
2. 成对比较：查询两个科室u和v中哪个更早被配送
3. 最先孩子：查询某个上级科室p的下级科室中，哪个最先被配送

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，配送任务失败。

每次只能提交一个查询或答案。请使用以下XML格式：
- 窥视前缀查询（例如查看前3个科室）：<query_peek>3</query_peek>
- 成对比较查询（例如比较科室2和5）：<query_compare>2,5</query_compare>
- 最先孩子查询（例如查询科室1的最先配送下级）：<query_first_child>1</query_first_child>
- 提交最终答案时，必须说明规则类型（A、B、C或D）和目标科室的序号：<answer>rule=A, position=5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the hospital intelligent logistics system. Let's infer the "Navigation Rule for the Delivery Robot".

The hospital departments are structured as a hierarchical tree with root node 1 (Triage/Logistics Center):
- Node 1's sub-departments: {{2, 3, 4}}
- Node 2's sub-departments: {{5, 6}}
- Node 3's sub-departments: {{7}}
- Node 4's sub-departments: {{8, 9, 10}}
- Node 7's sub-departments: {{11}}
- All other nodes are terminal wards

I have secretly selected a "sub-department sorting rule" used by the robot to perform a depth-first delivery (pre-order traversal). Reaching a department counts as delivered, then each sub-department is recursively delivered according to the rule.

The sorting rule can only be one of the following four (globally fixed but unknown):
- A. Global Ascending: At each superior department, sub-departments are delivered in ascending order by ID
- B. Global Descending: At each superior department, sub-departments are delivered in descending order by ID
- C. Emergency Priority (Odd Priority): At each superior department, emergency/special units (odd IDs) are delivered first (in ascending order), then regular wards (even IDs) (in ascending order)
- D. Floor Alternating: Logistics Center depth is 0; for departments at even depths, sub-departments are delivered in ascending order; for those at odd depths, sub-departments are delivered in descending order

Your goals are:
1. Identify the active sorting rule (A/B/C/D)
2. Determine the delivery position of department {target_node} in the sequence (which position it is delivered, counting from 1)

You can use the following three types of queries (with usage limits):
1. Peek Prefix: Query the first k department IDs in the delivery sequence (k ranges from 1 to 3)
2. Pairwise Comparison: Query which of two departments u and v is delivered earlier
3. First Child: Query which sub-department of a superior department p is delivered first

Submit your final answer when ready.

Each turn you can only submit one query or answer. Use the following XML format:
- Peek prefix query (e.g., view first 3 departments): <query_peek>3</query_peek>
- Pairwise comparison query (e.g., compare department 2 and 5): <query_compare>2,5</query_compare>
- First child query (e.g., query the first delivered sub-department of department 1): <query_first_child>1</query_first_child>
- Final answer (specify rule A/B/C/D and target department's position): <answer>rule=A, position=5</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用校园考务督导系统。我们将共同推演“巡考路线规则”。

学校的考场被组织为一棵管理层级树，根节点（教务处）为1，考场分布如下：
- 节点1的下辖考区：{{2, 3, 4}}
- 节点2的下辖考区：{{5, 6}}
- 节点3的下辖考区：{{7}}
- 节点4的下辖考区：{{8, 9, 10}}
- 节点7的下辖考区：{{11}}
- 其余节点均为具体考场

我已秘密选定了一种“下辖考区排序规则”，并安排督导员根据该规则进行深度优先的巡考（前序遍历）。即到达某考区立刻计为已巡查，然后按特定规则依次递归巡查其所有下辖分支。

下辖考区排序规则只可能是以下四种之一（全局固定但未知）：
- A. 全局升序：每个上级考区处，下辖考区按编号升序巡查
- B. 全局降序：每个上级考区处，下辖考区按编号降序巡查
- C. 文科优先（奇数优先）：每个上级考区处，先巡查文科考场（奇数编号，按升序），再巡查理科考场（偶数编号，按升序）
- D. 年级交替：教务处层级深度为0；深度为偶数的考区，其下辖考区按升序巡查；深度为奇数的考区，其下辖考区按降序巡查

你的目标是：
1. 识别当前启用的排序规则（A/B/C/D）
2. 确定考区{target_node}在巡考序列中的访问序号（第几个被巡查，从1开始计数）

你可以使用以下三种督导查询（每种查询有次数限制）：
1. 窥视前缀：查询巡考序列的前k个考区编号（k的取值范围：1到3）
2. 成对比较：查询两个考区u和v中哪个更早被巡查
3. 最先孩子：查询某个上级考区p的下辖考区中，哪个最先被巡查

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，督导任务失败。

每次只能提交一个查询或答案。请使用以下XML格式：
- 窥视前缀查询（例如查看前3个考区）：<query_peek>3</query_peek>
- 成对比较查询（例如比较考区2和5）：<query_compare>2,5</query_compare>
- 最先孩子查询（例如查询考区1的最先巡查下辖考区）：<query_first_child>1</query_first_child>
- 提交最终答案时，必须说明规则类型（A、B、C或D）和目标考区的序号：<answer>rule=A, position=5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the campus examination supervision system. Let's deduce the "Exam Patrol Route Rule".

The school's examination rooms are organized into a management hierarchy tree with root node 1 (Academic Affairs Office):
- Node 1's subordinate exam areas: {{2, 3, 4}}
- Node 2's subordinate exam areas: {{5, 6}}
- Node 3's subordinate exam areas: {{7}}
- Node 4's subordinate exam areas: {{8, 9, 10}}
- Node 7's subordinate exam areas: {{11}}
- All other nodes are specific exam rooms

I have secretly selected a "subordinate area sorting rule" and arranged for a supervisor to perform a depth-first patrol (pre-order traversal). Reaching an exam area counts as inspected, then each subordinate branch is recursively inspected according to the rule.

The sorting rule can only be one of the following four (globally fixed but unknown):
- A. Global Ascending: At each superior area, subordinate areas are inspected in ascending order by ID
- B. Global Descending: At each superior area, subordinate areas are inspected in descending order by ID
- C. Arts Priority (Odd Priority): At each superior area, arts exam rooms (odd IDs) are inspected first (in ascending order), then science exam rooms (even IDs) (in ascending order)
- D. Grade Alternating: Academic Affairs Office depth is 0; for areas at even depths, subordinates are inspected in ascending order; for areas at odd depths, subordinates are inspected in descending order

Your goals are:
1. Identify the active sorting rule (A/B/C/D)
2. Determine the patrol position of area {target_node} in the sequence (which position it is inspected, counting from 1)

You can use the following three types of queries (with usage limits):
1. Peek Prefix: Query the first k area IDs in the patrol sequence (k ranges from 1 to 3)
2. Pairwise Comparison: Query which of two areas u and v is inspected earlier
3. First Child: Query which subordinate area of a superior area p is inspected first

Submit your final answer when ready.

Each turn you can only submit one query or answer. Use the following XML format:
- Peek prefix query (e.g., view first 3 areas): <query_peek>3</query_peek>
- Pairwise comparison query (e.g., compare area 2 and 5): <query_compare>2,5</query_compare>
- First child query (e.g., query the first inspected subordinate of area 1): <query_first_child>1</query_first_child>
- Final answer (specify rule A/B/C/D and target area's position): <answer>rule=A, position=5</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用智能工厂点检系统。请推断工业机器人的“设备巡检规则”。

工厂的生产单元构成了树状监控拓扑，根节点（总控室）为1，设备级联关系如下：
- 节点1的下级生产线：{{2, 3, 4}}
- 节点2的下级生产线：{{5, 6}}
- 节点3的下级生产线：{{7}}
- 节点4的下级生产线：{{8, 9, 10}}
- 节点7的下级生产线：{{11}}
- 其余节点均为末端工作站

我已秘密配置了一种“下级节点排序规则”，机器人依靠该规则对系统进行深度优先的设备点检（前序遍历）。即到达某节点立刻计为已点检，然后按特定规则依次递归点检其所有下级工作站。

下级节点排序规则只可能是以下四种之一（全局固定但未知）：
- A. 全局升序：每个上级节点处，下级设备按编号升序点检
- B. 全局降序：每个上级节点处，下级设备按编号降序点检
- C. 高耗能优先（奇数优先）：每个上级节点处，先点检高耗能设备（奇数编号，按升序），再点检常规设备（偶数编号，按升序）
- D. 层级交替：总控室级次为0；级次为偶数的节点，其下级设备按升序点检；级次为奇数的节点，其下级设备按降序点检

你的目标是：
1. 识别当前启用的排序规则（A/B/C/D）
2. 确定设备节点{target_node}在点检序列中的访问序号（第几个被点检，从1开始计数）

你可以使用以下三种点检查询（每种查询有次数限制）：
1. 窥视前缀：查询点检序列的前k个设备编号（k的取值范围：1到3）
2. 成对比较：查询两个设备u和v中哪个更早被点检
3. 最先孩子：查询某个上级节点p的下级设备中，哪个最先被点检

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，点检流程将报错终止。

每次只能提交一个查询或答案。请使用以下XML格式：
- 窥视前缀查询（例如查看前3个设备）：<query_peek>3</query_peek>
- 成对比较查询（例如比较设备2和5）：<query_compare>2,5</query_compare>
- 最先孩子查询（例如查询设备1的最先点检下级）：<query_first_child>1</query_first_child>
- 提交最终答案时，必须说明规则类型（A、B、C或D）和目标设备的序号：<answer>rule=A, position=5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the smart factory inspection system. Please deduce the "Equipment Inspection Rule" for the industrial robot.

The factory's production units form a tree-like monitoring topology with root node 1 (Main Control Room):
- Node 1's subordinate lines: {{2, 3, 4}}
- Node 2's subordinate lines: {{5, 6}}
- Node 3's subordinate lines: {{7}}
- Node 4's subordinate lines: {{8, 9, 10}}
- Node 7's subordinate lines: {{11}}
- All other nodes are terminal workstations

I have secretly configured a "subordinate node sorting rule" for the robot to perform a depth-first equipment inspection (pre-order traversal). Reaching a node counts as inspected, then each subordinate workstation is recursively inspected according to the rule.

The sorting rule can only be one of the following four (globally fixed but unknown):
- A. Global Ascending: At each superior node, subordinate equipment is inspected in ascending order by ID
- B. Global Descending: At each superior node, subordinate equipment is inspected in descending order by ID
- C. High-Energy Priority (Odd Priority): At each superior node, high-energy equipment (odd IDs) is inspected first (in ascending order), then regular equipment (even IDs) (in ascending order)
- D. Tier Alternating: Main Control Room tier is 0; for nodes at even tiers, subordinate equipment is inspected in ascending order; for nodes at odd tiers, subordinate equipment is inspected in descending order

Your goals are:
1. Identify the active sorting rule (A/B/C/D)
2. Determine the inspection position of equipment node {target_node} in the sequence (which position it is inspected, counting from 1)

You can use the following three types of queries (with usage limits):
1. Peek Prefix: Query the first k equipment IDs in the inspection sequence (k ranges from 1 to 3)
2. Pairwise Comparison: Query which of two equipment nodes u and v is inspected earlier
3. First Child: Query which subordinate equipment of a superior node p is inspected first

Submit your final answer when ready.

Each turn you can only submit one query or answer. Use the following XML format:
- Peek prefix query (e.g., view first 3 equipment): <query_peek>3</query_peek>
- Pairwise comparison query (e.g., compare equipment 2 and 5): <query_compare>2,5</query_compare>
- First child query (e.g., query the first inspected subordinate of equipment 1): <query_first_child>1</query_first_child>
- Final answer (specify rule A/B/C/D and target equipment's position): <answer>rule=A, position=5</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用法院智慧审判流转系统。请推理当前的“案件卷宗审查规则”。

案件的处理流程被抽象为一棵司法节点树，根节点（立案大厅）为1，流转结构如下：
- 节点1的下级审查节点：{{2, 3, 4}}
- 节点2的下级审查节点：{{5, 6}}
- 节点3的下级审查节点：{{7}}
- 节点4的下级审查节点：{{8, 9, 10}}
- 节点7的下级审查节点：{{11}}
- 其余节点均为结案节点

我已秘密设置了一种“下级节点排序规则”，系统依此对所有流程节点进行深度优先的审查（前序遍历）。即流转至某节点立刻计为已审查，然后按特定规则依次递归审查其所有后续节点。

下级节点排序规则只可能是以下四种之一（全局固定但未知）：
- A. 全局升序：每个上级节点处，后续节点按编号升序审查
- B. 全局降序：每个上级节点处，后续节点按编号降序审查
- C. 刑事优先（奇数优先）：每个上级节点处，先审查刑事类节点（奇数编号，按升序），再审查民事类节点（偶数编号，按升序）
- D. 审级交替：立案大厅审级为0；审级为偶数的节点，其后续节点按升序审查；审级为奇数的节点，其后续节点按降序审查

你的目标是：
1. 识别当前启用的排序规则（A/B/C/D）
2. 确定流程节点{target_node}在审查序列中的访问序号（第几个被审查，从1开始计数）

你可以使用以下三种调卷查询（每种查询有次数限制）：
1. 窥视前缀：查询审查序列的前k个节点编号（k的取值范围：1到3）
2. 成对比较：查询两个节点u和v中哪个更早被审查
3. 最先孩子：查询某个上级节点p的后续节点中，哪个最先被审查

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，卷宗流转将被驳回。

每次只能提交一个查询或答案。请使用以下XML格式：
- 窥视前缀查询（例如查看前3个节点）：<query_peek>3</query_peek>
- 成对比较查询（例如比较节点2和5）：<query_compare>2,5</query_compare>
- 最先孩子查询（例如查询节点1的最先审查后续节点）：<query_first_child>1</query_first_child>
- 提交最终答案时，必须说明规则类型（A、B、C或D）和目标节点的序号：<answer>rule=A, position=5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the court smart trial workflow system. Please infer the current "Case File Review Rule".

The case processing workflow is abstracted as a judicial node tree with root node 1 (Filing Hall):
- Node 1's subsequent review nodes: {{2, 3, 4}}
- Node 2's subsequent review nodes: {{5, 6}}
- Node 3's subsequent review nodes: {{7}}
- Node 4's subsequent review nodes: {{8, 9, 10}}
- Node 7's subsequent review nodes: {{11}}
- All other nodes are case-closing nodes

I have secretly set a "subsequent node sorting rule", which the system uses to perform a depth-first review (pre-order traversal). Reaching a node counts as reviewed, then each subsequent node is recursively reviewed according to the rule.

The sorting rule can only be one of the following four (globally fixed but unknown):
- A. Global Ascending: At each superior node, subsequent nodes are reviewed in ascending order by ID
- B. Global Descending: At each superior node, subsequent nodes are reviewed in descending order by ID
- C. Criminal Priority (Odd Priority): At each superior node, criminal nodes (odd IDs) are reviewed first (in ascending order), then civil nodes (even IDs) (in ascending order)
- D. Trial Level Alternating: Filing Hall level is 0; for nodes at even levels, subsequent nodes are reviewed in ascending order; for nodes at odd levels, subsequent nodes are reviewed in descending order

Your goals are:
1. Identify the active sorting rule (A/B/C/D)
2. Determine the review position of workflow node {target_node} in the sequence (which position it is reviewed, counting from 1)

You can use the following three types of file queries (with usage limits):
1. Peek Prefix: Query the first k node IDs in the review sequence (k ranges from 1 to 3)
2. Pairwise Comparison: Query which of two nodes u and v is reviewed earlier
3. First Child: Query which subsequent node of a superior node p is reviewed first

Submit your final answer when ready.

Each turn you can only submit one query or answer. Use the following XML format:
- Peek prefix query (e.g., view first 3 nodes): <query_peek>3</query_peek>
- Pairwise comparison query (e.g., compare node 2 and 5): <query_compare>2,5</query_compare>
- First child query (e.g., query the first reviewed subsequent node of node 1): <query_first_child>1</query_first_child>
- Final answer (specify rule A/B/C/D and target node's position): <answer>rule=A, position=5</answer>
"""

    tags = ["answer", "query_peek", "query_compare", "query_first_child"]

    DIFFICULTY_CONFIG = {
        1: {
            "target_node": 6,
            "rule": "A",
            "max_peek": 3,
            "max_compare": 7,
            "max_first_child": 3,
        },
        2: {
            "target_node": 6,
            "rule": "C",
            "max_peek": 2,
            "max_compare": 6,
            "max_first_child": 3,
        },
        3: {
            "target_node": 6,
            "rule": "D",
            "max_peek": 2,
            "max_compare": 5,
            "max_first_child": 2,
        },
        4: {
            "target_node": 6,
            "rule": "B",
            "max_peek": 2,
            "max_compare": 4,
            "max_first_child": 2,
        },
        5: {
            "target_node": 6,
            "rule": "random",
            "max_peek": 2,
            "max_compare": 3,
            "max_first_child": 2,
        },
    }

    def __init__(self, config):
        self.tree = {
            1: [2, 3, 4],
            2: [5, 6],
            3: [7],
            4: [8, 9, 10],
            7: [11],
            5: [],
            6: [],
            8: [],
            9: [],
            10: [],
            11: [],
        }
        
        self.depths = {
            1: 0,
            2: 1, 3: 1, 4: 1,
            5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2,
            11: 3,
        }
        
        self.peek_count = 0
        self.compare_count = 0
        self.first_child_count = 0
        
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[diff]
        
        self._game_info["target_node"] = cfg["target_node"]
        self.target_node = cfg["target_node"]
        
        if cfg["rule"] == "random":
            seed_val = self.config.difficulty * 1000 + getattr(self.config, 'seed', 42)
            rng = random.Random(seed_val)
            self.rule = rng.choice(["A", "B", "C", "D"])
        else:
            self.rule = cfg["rule"]
        
        self.max_peek = cfg["max_peek"]
        self.max_compare = cfg["max_compare"]
        self.max_first_child = cfg["max_first_child"]
        
        self.traversal_sequence = self._generate_traversal()
        
        self.target_position = self.traversal_sequence.index(self.target_node) + 1

    def _sort_children(self, parent, children):
        if self.rule == "A":
            return sorted(children)
        elif self.rule == "B":
            return sorted(children, reverse=True)
        elif self.rule == "C":
            odd = sorted([c for c in children if c % 2 == 1])
            even = sorted([c for c in children if c % 2 == 0])
            return odd + even
        elif self.rule == "D":
            depth = self.depths[parent]
            if depth % 2 == 0:
                return sorted(children)
            else:
                return sorted(children, reverse=True)
        else:
            raise ValueError(f"Unknown rule: {self.rule}")

    def _generate_traversal(self):
        sequence = []
        
        def preorder(node):
            sequence.append(node)
            children = self.tree[node]
            if children:
                sorted_children = self._sort_children(node, children)
                for child in sorted_children:
                    preorder(child)
        
        preorder(1)
        return sequence

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
            ans_dict = {}
            for kv in kv_pairs:
                k, v = kv.split("=", 1)
                ans_dict[k.strip().lower()] = v.strip()
            
            if "rule" not in ans_dict or "position" not in ans_dict:
                return False
            
            if ans_dict["rule"].upper() != self.rule:
                return False
            
            try:
                position = int(ans_dict["position"])
                return position == self.target_position
            except ValueError:
                return False
                
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "query_peek" in parsed_info:
            self.peek_count += 1
            if self.peek_count > self.max_peek:
                if lang == "zh":
                    return f"错误：窥视前缀查询次数超限（最多{self.max_peek}次）"
                else:
                    return f"Error: Peek query limit exceeded (max {self.max_peek} times)"
            
            try:
                k = int(parsed_info["query_peek"].strip())
                if k < 1 or k > 3:
                    if lang == "zh":
                        return "错误：k的取值范围必须在1到3之间"
                    else:
                        return "Error: k must be between 1 and 3"
                
                prefix = self.traversal_sequence[:k]
                return " ".join(map(str, prefix))
            except ValueError:
                if lang == "zh":
                    return "错误：无效的k值"
                else:
                    return "Error: Invalid k value"
        
        elif "query_compare" in parsed_info:
            self.compare_count += 1
            if self.compare_count > self.max_compare:
                if lang == "zh":
                    return f"错误：成对比较查询次数超限（最多{self.max_compare}次）"
                else:
                    return f"Error: Comparison query limit exceeded (max {self.max_compare} times)"
            
            try:
                raw = parsed_info["query_compare"]
                u, v = [int(x.strip()) for x in raw.split(",")]
                
                if u not in self.traversal_sequence or v not in self.traversal_sequence:
                    if lang == "zh":
                        return "错误：节点编号无效"
                    else:
                        return "Error: Invalid node ID"
                
                pos_u = self.traversal_sequence.index(u)
                pos_v = self.traversal_sequence.index(v)
                
                return str(u) if pos_u < pos_v else str(v)
            except (ValueError, IndexError):
                if lang == "zh":
                    return "错误：格式无效或节点编号错误"
                else:
                    return "Error: Invalid format or node ID"
        
        elif "query_first_child" in parsed_info:
            self.first_child_count += 1
            if self.first_child_count > self.max_first_child:
                if lang == "zh":
                    return f"错误：最先孩子查询次数超限（最多{self.max_first_child}次）"
                else:
                    return f"Error: First child query limit exceeded (max {self.max_first_child} times)"
            
            try:
                p = int(parsed_info["query_first_child"].strip())
                
                if p not in self.tree:
                    if lang == "zh":
                        return "错误：节点编号无效"
                    else:
                        return "Error: Invalid node ID"
                
                children = self.tree[p]
                if not children:
                    if lang == "zh":
                        return "错误：该节点没有子节点"
                    else:
                        return "Error: Node has no children"
                
                sorted_children = self._sort_children(p, children)
                return str(sorted_children[0])
            except ValueError:
                if lang == "zh":
                    return "错误：无效的节点编号"
                else:
                    return "Error: Invalid node ID"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        parts = correct.split()
        if len(parts) > 1 and all(p.isdigit() for p in parts):
            nums = [int(p) for p in parts]
            nums[-1] = nums[-1] + 1
            return " ".join(str(n) for n in nums)
        
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if "是" in correct:
            return correct.replace("是", "否")
        elif "否" in correct:
            return correct.replace("否", "是")
            
        if "Yes" in correct:
            return correct.replace("Yes", "No")
        elif "yes" in correct:
            return correct.replace("yes", "no")
        elif "No" in correct:
            return correct.replace("No", "Yes")
        elif "no" in correct:
            return correct.replace("no", "yes")
            
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        queries = []
        
        for k in range(1, 4):
            if k <= len(self.traversal_sequence):
                prefix = self.traversal_sequence[:k]
                ans = " ".join(map(str, prefix))
                queries.append({
                    "query": f"<query_peek>{k}</query_peek>",
                    "answer": ans
                })
        
        all_nodes = list(range(1, 12))
        for u in all_nodes:
            for v in all_nodes:
                if u == v:
                    continue
                
                pos_u = self.traversal_sequence.index(u)
                pos_v = self.traversal_sequence.index(v)
                ans = str(u) if pos_u < pos_v else str(v)
                
                queries.append({
                    "query": f"<query_compare>{u},{v}</query_compare>",
                    "answer": ans
                })
        
        parents = [1, 2, 3, 4, 7]
        for p in parents:
            children = self.tree[p]
            sorted_children = self._sort_children(p, children)
            ans = str(sorted_children[0])
            
            queries.append({
                "query": f"<query_first_child>{p}</query_first_child>",
                "answer": ans
            })
            
        return queries