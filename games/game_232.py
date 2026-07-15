from .base import Game
import random
import re

class TreeLeafDiscoveryGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树叶探索"的推理游戏，规则如下：

游戏设定了一棵固定的有根树（节点总数 {n}），根节点编号为 1。每个节点的子节点按编号递增排列。存在一个隐藏函数 F，对于任意节点 v，F(v) 返回以 v 为根的子树中叶子节点的数量（叶子节点指没有子节点的节点）。

你的初始位置在根节点，拥有 {budget} 点行动点数。你的目标是通过探索和查询，推断出整棵树的叶子节点总数（即 F(根节点) 的值）。

每次操作会消耗相应的行动点，具体如下：

1. 查询剩余行动点（消耗 0 点）：
   <query_budget></query_budget>

2. 探查第 k 个子节点（消耗 1 点）：
   <probe_child>k</probe_child>
   返回该子节点的编号，若不存在则返回提示。

3. 移动至第 k 个子节点（消耗 1 点）：
   <move_to_child>k</move_to_child>
   移动成功返回新节点编号，失败仍消耗行动点。

4. 返回父节点（消耗 1 点）：
   <move_to_parent></move_to_parent>
   若当前为根节点则移动失败但仍消耗行动点。

5. 查询当前节点的函数值（消耗 1 点）：
   <query_function></query_function>
   返回 F(当前节点) 的值。

6. 重置回到根节点（消耗 1 点）：
   <reset_to_root></reset_to_root>

7. 提交最终答案（消耗 0 点，需至少进行过 3 次函数查询）：
   <answer>叶子总数=X, 规律=你总结的规律描述</answer>

- 每次只能执行一个操作
- 行动点用尽前必须给出正确答案
- 提交答案前必须至少进行 3 次函数查询
- 答案格式必须严格遵守，X 为你推断的叶子节点总数
"""

    game_rule_en = """\
Let's play a "Tree Leaf Discovery" deduction game. Here are the rules:

The game has a fixed rooted tree (total {n} nodes), with the root node numbered 1. Each node's children are ordered by increasing ID. There is a hidden function F where for any node v, F(v) returns the number of leaf nodes in the subtree rooted at v (a leaf node has no children).

You start at the root node with {budget} action points. Your goal is to infer the total number of leaf nodes in the entire tree (i.e., F(root)) through exploration and queries.

Each operation costs action points as follows:

1. Query remaining action points (costs 0 points):
   <query_budget></query_budget>

2. Probe the k-th child (costs 1 point):
   <probe_child>k</probe_child>
   Returns the child's ID if it exists, otherwise returns a message.

3. Move to the k-th child (costs 1 point):
   <move_to_child>k</move_to_child>
   Returns new node ID on success; failure still costs the point.

4. Move to parent node (costs 1 point):
   <move_to_parent></move_to_parent>
   Fails at root but still costs the point.

5. Query function value at current node (costs 1 point):
   <query_function></query_function>
   Returns F(current node).

6. Reset to root node (costs 1 point):
   <reset_to_root></reset_to_root>

7. Submit final answer (costs 0 points, requires at least 3 function queries):
   <answer>total_leaves=X, pattern=your pattern description</answer>

- Only one operation per turn
- Must provide correct answer before action points run out
- Must perform at least 3 function queries before submitting answer
- Answer format must be strictly followed, where X is your inferred total leaf count
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"路网终端探测"的推理游戏，规则如下：

游戏设定了一个固定的层级化道路网络（节点总数 {n}），中心枢纽编号为 1。每个路口的下游分支路口按编号递增排列。存在一个隐藏的流量监测系统，对于任意路口 v，查询该系统会返回从 v 出发最终可以到达的死胡同/终点站（即没有下游分支的叶子节点）的数量。

你的初始位置在中心枢纽（根节点），拥有 {budget} 点调度指令。你的目标是通过探索和查询，推断出整个路网中包含的终点站总数（即查询中心枢纽的返回值）。

每次操作会消耗相应的调度指令，具体如下：

1. 查询剩余调度指令（消耗 0 点）：
   <query_budget></query_budget>

2. 探查第 k 个下游分支（消耗 1 点）：
   <probe_child>k</probe_child>
   返回该分支路口的编号，若不存在则返回提示。

3. 移动至第 k 个下游分支（消耗 1 点）：
   <move_to_child>k</move_to_child>
   移动成功返回新路口编号，失败仍消耗指令。

4. 返回上级路口（消耗 1 点）：
   <move_to_parent></move_to_parent>
   若当前为中心枢纽则移动失败但仍消耗指令。

5. 查询当前路口的终点站数量（消耗 1 点）：
   <query_function></query_function>
   返回从当前路口可达的终点站总数。

6. 重置回到中心枢纽（消耗 1 点）：
   <reset_to_root></reset_to_root>

7. 提交最终答案（消耗 0 点，需至少进行过 3 次系统查询）：
   <answer>叶子总数=X, 规律=你总结的路网结构描述</answer>

- 每次只能执行一个操作
- 调度指令用尽前必须给出正确答案
- 提交答案前必须至少进行 3 次系统查询
- 答案格式必须严格遵守，X 为你推断的终点站总数
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Road Network Terminal Discovery" deduction game. Here are the rules:

The game features a hierarchical road network (total {n} nodes), with the central hub numbered 1. Each intersection's downstream branches are ordered by increasing ID. There is a hidden traffic monitoring system where, for any intersection v, querying it returns the number of dead-ends or final destinations (leaf nodes with no further branches) accessible from v.

You start at the central hub with {budget} dispatch commands. Your goal is to infer the total number of final destinations in the entire network (i.e., the query result for the central hub) through exploration and queries.

Each operation costs dispatch commands as follows:

1. Query remaining dispatch commands (costs 0 points):
   <query_budget></query_budget>

2. Probe the k-th downstream branch (costs 1 point):
   <probe_child>k</probe_child>
   Returns the branch intersection's ID if it exists, otherwise returns a message.

3. Move to the k-th downstream branch (costs 1 point):
   <move_to_child>k</move_to_child>
   Returns new intersection ID on success; failure still costs the command.

4. Return to the previous upstream intersection (costs 1 point):
   <move_to_parent></move_to_parent>
   Fails at the central hub but still costs the command.

5. Query final destinations at current intersection (costs 1 point):
   <query_function></query_function>
   Returns the number of terminal nodes accessible from the current location.

6. Reset to central hub (costs 1 point):
   <reset_to_root></reset_to_root>

7. Submit final answer (costs 0 points, requires at least 3 system queries):
   <answer>total_leaves=X, pattern=your network structure description</answer>

- Only one operation per turn
- Must provide correct answer before dispatch commands run out
- Must perform at least 3 system queries before submitting answer
- Answer format must be strictly followed, where X is your inferred total final destination count
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"罕见病溯源探测"的推理游戏，规则如下：

游戏设定了一套层级化的疾病诊断决策树（节点总数 {n}），初始广泛症状节点编号为 1。每个症状的细分亚型按编号递增排列。存在一个隐藏的医学数据库函数 F，对于任意症状分类 v，F(v) 返回属于该分类下的具体罕见病病种数量（即无法继续细分的叶子节点数量）。

你的初始位置在初始广泛症状节点，拥有 {budget} 点临床诊断耗时。你的目标是通过探索和查询，推断出整个决策树中涵盖的罕见病病种总数（即 F(初始症状) 的值）。

每次操作会消耗相应的诊断耗时，具体如下：

1. 查询剩余诊断耗时（消耗 0 点）：
   <query_budget></query_budget>

2. 探查第 k 个细分亚型（消耗 1 点）：
   <probe_child>k</probe_child>
   返回该亚型的编号，若不存在则返回提示。

3. 深入至第 k 个细分亚型（消耗 1 点）：
   <move_to_child>k</move_to_child>
   深入成功返回新症状编号，失败仍消耗耗时。

4. 回退至上一级症状（消耗 1 点）：
   <move_to_parent></move_to_parent>
   若当前为初始症状则回退失败但仍消耗耗时。

5. 查询当前症状分类的病种数量（消耗 1 点）：
   <query_function></query_function>
   返回 F(当前症状分类) 的值。

6. 重置回到初始广泛症状（消耗 1 点）：
   <reset_to_root></reset_to_root>

7. 提交最终诊断（消耗 0 点，需至少进行过 3 次数据库查询）：
   <answer>叶子总数=X, 规律=你总结的分类规律描述</answer>

- 每次只能执行一个操作
- 诊断耗时用尽前必须给出正确答案
- 提交答案前必须至少进行 3 次数据库查询
- 答案格式必须严格遵守，X 为你推断的罕见病病种总数
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Rare Disease Traceability" deduction game. Here are the rules:

The game features a hierarchical diagnostic decision tree (total {n} nodes), with the initial broad symptom numbered 1. Each symptom's specific sub-types are ordered by increasing ID. There is a hidden medical database function F where, for any symptom category v, F(v) returns the number of specific rare diseases (indivisible leaf nodes) under that category.

You start at the initial broad symptom node with {budget} clinical time points. Your goal is to infer the total number of rare diseases covered in the entire tree (i.e., F(initial symptom)) through exploration and queries.

Each operation costs clinical time points as follows:

1. Query remaining clinical time (costs 0 points):
   <query_budget></query_budget>

2. Probe the k-th sub-type (costs 1 point):
   <probe_child>k</probe_child>
   Returns the sub-type's ID if it exists, otherwise returns a message.

3. Delve into the k-th sub-type (costs 1 point):
   <move_to_child>k</move_to_child>
   Returns new symptom ID on success; failure still costs the point.

4. Return to the broader symptom category (costs 1 point):
   <move_to_parent></move_to_parent>
   Fails at the initial symptom but still costs the point.

5. Query disease count for current category (costs 1 point):
   <query_function></query_function>
   Returns F(current category).

6. Reset to initial broad symptom (costs 1 point):
   <reset_to_root></reset_to_root>

7. Submit final diagnosis (costs 0 points, requires at least 3 database queries):
   <answer>total_leaves=X, pattern=your category pattern description</answer>

- Only one operation per turn
- Must provide correct answer before clinical time runs out
- Must perform at least 3 database queries before submitting answer
- Answer format must be strictly followed, where X is your inferred total rare disease count
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"知识图谱解构"的推理游戏，规则如下：

游戏设定了一棵固定的学科知识树（节点总数 {n}），核心主学科节点编号为 1。每个知识域的子课题按编号递增排列。存在一个隐藏的教研函数 F，对于任意知识域 v，F(v) 返回包含在 v 中的基础知识点数量（基础知识点指不可再分的叶子节点）。

你的初始位置在核心主学科节点，拥有 {budget} 点教研评估算力。你的目标是通过探索和查询，推断出整门学科的基础知识点总数（即 F(核心主学科) 的值）。

每次操作会消耗相应的评估算力，具体如下：

1. 查询剩余评估算力（消耗 0 点）：
   <query_budget></query_budget>

2. 探查第 k 个子课题（消耗 1 点）：
   <probe_child>k</probe_child>
   返回该子课题的编号，若不存在则返回提示。

3. 进入第 k 个子课题（消耗 1 点）：
   <move_to_child>k</move_to_child>
   进入成功返回新知识域编号，失败仍消耗算力。

4. 返回上级知识域（消耗 1 点）：
   <move_to_parent></move_to_parent>
   若当前为核心主学科则移动失败但仍消耗算力。

5. 查询当前知识域的知识点数量（消耗 1 点）：
   <query_function></query_function>
   返回 F(当前知识域) 的值。

6. 重置回到核心主学科（消耗 1 点）：
   <reset_to_root></reset_to_root>

7. 提交最终知识点统计（消耗 0 点，需至少进行过 3 次教研查询）：
   <answer>叶子总数=X, 规律=你总结的学科框架规律描述</answer>

- 每次只能执行一个操作
- 算力用尽前必须给出正确答案
- 提交答案前必须至少进行 3 次教研查询
- 答案格式必须严格遵守，X 为你推断的基础知识点总数
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Graph Deconstruction" deduction game. Here are the rules:

The game features a fixed academic knowledge tree (total {n} nodes), with the core subject node numbered 1. Each knowledge domain's sub-topics are ordered by increasing ID. There is a hidden academic function F where, for any knowledge domain v, F(v) returns the number of fundamental knowledge points (indivisible leaf nodes) contained within v.

You start at the core subject node with {budget} assessment compute tokens. Your goal is to infer the total number of fundamental knowledge points in the entire subject (i.e., F(core subject)) through exploration and queries.

Each operation costs compute tokens as follows:

1. Query remaining compute tokens (costs 0 points):
   <query_budget></query_budget>

2. Probe the k-th sub-topic (costs 1 point):
   <probe_child>k</probe_child>
   Returns the sub-topic's ID if it exists, otherwise returns a message.

3. Enter the k-th sub-topic (costs 1 point):
   <move_to_child>k</move_to_child>
   Returns new domain ID on success; failure still costs the token.

4. Return to the broader knowledge domain (costs 1 point):
   <move_to_parent></move_to_parent>
   Fails at the core subject but still costs the token.

5. Query knowledge point count for current domain (costs 1 point):
   <query_function></query_function>
   Returns F(current domain).

6. Reset to core subject (costs 1 point):
   <reset_to_root></reset_to_root>

7. Submit final point count (costs 0 points, requires at least 3 academic queries):
   <answer>total_leaves=X, pattern=your academic framework pattern description</answer>

- Only one operation per turn
- Must provide correct answer before tokens run out
- Must perform at least 3 academic queries before submitting answer
- Answer format must be strictly followed, where X is your inferred total fundamental knowledge point count
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"BOM 物料溯源"的推理游戏，规则如下：

游戏设定了一套固定的产品物料清单（BOM）树（节点总数 {n}），顶层成品编号为 1。每个组件的下级子组件按编号递增排列。存在一个隐藏的库存盘点函数 F，对于任意组件 v，F(v) 返回组装该组件所需的基础零件种类数量（基础零件指不可再拆解的底层物料/叶子节点）。

你的初始位置在顶层成品节点，拥有 {budget} 点盘点工时。你的目标是通过探索和查询，推断出整台成品所需的基础零件种类总数（即 F(顶层成品) 的值）。

每次操作会消耗相应的盘点工时，具体如下：

1. 查询剩余盘点工时（消耗 0 点）：
   <query_budget></query_budget>

2. 探查第 k 个下级子组件（消耗 1 点）：
   <probe_child>k</probe_child>
   返回该子组件的编号，若不存在则返回提示。

3. 拆解至第 k 个下级子组件（消耗 1 点）：
   <move_to_child>k</move_to_child>
   拆解成功返回新组件编号，失败仍消耗工时。

4. 组装返回上级组件（消耗 1 点）：
   <move_to_parent></move_to_parent>
   若当前为顶层成品则移动失败但仍消耗工时。

5. 查询当前组件所需的基础零件数（消耗 1 点）：
   <query_function></query_function>
   返回 F(当前组件) 的值。

6. 重置回到顶层成品（消耗 1 点）：
   <reset_to_root></reset_to_root>

7. 提交最终BOM报告（消耗 0 点，需至少进行过 3 次库存盘点查询）：
   <answer>叶子总数=X, 规律=你总结的物料结构规律描述</answer>

- 每次只能执行一个操作
- 工时用尽前必须给出正确答案
- 提交答案前必须至少进行 3 次库存盘点查询
- 答案格式必须严格遵守，X 为你推断的基础零件种类总数
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play a "BOM Material Traceability" deduction game. Here are the rules:

The game features a fixed Bill of Materials (BOM) tree for a product (total {n} nodes), with the top-level final assembly numbered 1. Each component's sub-assemblies are ordered by increasing ID. There is a hidden inventory function F where, for any component v, F(v) returns the number of basic raw parts (indivisible bottom-level materials/leaf nodes) required to build it.

You start at the top-level final assembly with {budget} inspection man-hours. Your goal is to infer the total number of basic raw parts needed for the entire final product (i.e., F(final assembly)) through exploration and queries.

Each operation costs man-hours as follows:

1. Query remaining inspection man-hours (costs 0 points):
   <query_budget></query_budget>

2. Probe the k-th sub-assembly (costs 1 point):
   <probe_child>k</probe_child>
   Returns the sub-assembly's ID if it exists, otherwise returns a message.

3. Disassemble to the k-th sub-assembly (costs 1 point):
   <move_to_child>k</move_to_child>
   Returns new component ID on success; failure still costs the man-hour.

4. Reassemble to parent component (costs 1 point):
   <move_to_parent></move_to_parent>
   Fails at the final assembly but still costs the man-hour.

5. Query basic parts count for current component (costs 1 point):
   <query_function></query_function>
   Returns F(current component).

6. Reset to top-level final assembly (costs 1 point):
   <reset_to_root></reset_to_root>

7. Submit final BOM report (costs 0 points, requires at least 3 inventory queries):
   <answer>total_leaves=X, pattern=your BOM structure pattern description</answer>

- Only one operation per turn
- Must provide correct answer before man-hours run out
- Must perform at least 3 inventory queries before submitting answer
- Answer format must be strictly followed, where X is your inferred total basic parts count
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"法典条款剖析"的推理游戏，规则如下：

游戏设定了一部固定的层级化法典结构树（节点总数 {n}），法典总则节点编号为 1。每编/章的下级分卷按编号递增排列。存在一个隐藏的法务索引函数 F，对于任意法律层级 v，F(v) 返回涵盖在 v 之下的具体可执行法条数量（法条指没有更细分条款的底层叶子节点）。

你的初始位置在法典总则节点，拥有 {budget} 点法务检索时长。你的目标是通过探索和查询，推断出整部法典包含的可执行法条总数（即 F(法典总则) 的值）。

每次操作会消耗相应的检索时长，具体如下：

1. 查询剩余检索时长（消耗 0 点）：
   <query_budget></query_budget>

2. 探查第 k 个下级分卷（消耗 1 点）：
   <probe_child>k</probe_child>
   返回该分卷的编号，若不存在则返回提示。

3. 查阅第 k 个下级分卷（消耗 1 点）：
   <move_to_child>k</move_to_child>
   查阅成功返回新层级编号，失败仍消耗时长。

4. 统筹至上级法典层级（消耗 1 点）：
   <move_to_parent></move_to_parent>
   若当前为总则则移动失败但仍消耗时长。

5. 查询当前层级的法条数量（消耗 1 点）：
   <query_function></query_function>
   返回 F(当前法律层级) 的值。

6. 重置回到法典总则（消耗 1 点）：
   <reset_to_root></reset_to_root>

7. 提交最终汇编结果（消耗 0 点，需至少进行过 3 次法务索引查询）：
   <answer>叶子总数=X, 规律=你总结的法典结构规律描述</answer>

- 每次只能执行一个操作
- 检索时长用尽前必须给出正确答案
- 提交答案前必须至少进行 3 次法务索引查询
- 答案格式必须严格遵守，X 为你推断的可执行法条总数
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Legal Code Deconstruction" deduction game. Here are the rules:

The game features a fixed hierarchical legal code tree (total {n} nodes), with the general provisions node numbered 1. Each chapter/section's sub-sections are ordered by increasing ID. There is a hidden legal index function F where, for any legal level v, F(v) returns the number of specific actionable clauses (indivisible bottom-level rules/leaf nodes) covered under v.

You start at the general provisions node with {budget} legal research hours. Your goal is to infer the total number of actionable clauses contained in the entire legal code (i.e., F(general provisions)) through exploration and queries.

Each operation costs research hours as follows:

1. Query remaining research hours (costs 0 points):
   <query_budget></query_budget>

2. Probe the k-th sub-section (costs 1 point):
   <probe_child>k</probe_child>
   Returns the sub-section's ID if it exists, otherwise returns a message.

3. Examine the k-th sub-section (costs 1 point):
   <move_to_child>k</move_to_child>
   Returns new level ID on success; failure still costs the hour.

4. Step back to the broader legal level (costs 1 point):
   <move_to_parent></move_to_parent>
   Fails at the general provisions but still costs the hour.

5. Query clause count for current level (costs 1 point):
   <query_function></query_function>
   Returns F(current level).

6. Reset to general provisions (costs 1 point):
   <reset_to_root></reset_to_root>

7. Submit final compilation (costs 0 points, requires at least 3 legal index queries):
   <answer>total_leaves=X, pattern=your code structure pattern description</answer>

- Only one operation per turn
- Must provide correct answer before research hours run out
- Must perform at least 3 legal index queries before submitting answer
- Answer format must be strictly followed, where X is your inferred total actionable clauses count
"""

    tags = ["answer", "query_budget", "probe_child", "move_to_child", 
            "move_to_parent", "query_function", "reset_to_root"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 15,
                "budget": 12,
                "tree": {
                    1: [2, 3],
                    2: [4, 5, 6],
                    3: [7, 8],
                    4: [9, 10],
                    5: [11, 12],
                    6: [13],
                    7: [14],
                    8: [15],
                }
            },
            2: {
                "n": 20,
                "budget": 12,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6, 7],
                    3: [8, 9],
                    4: [10, 11, 12],
                    5: [13, 14],
                    6: [15],
                    7: [16],
                    8: [17, 18],
                    11: [19, 20],
                }
            },
            3: {
                "n": 25,
                "budget": 12,
                "tree": {
                    1: [2, 3],
                    2: [4, 5],
                    3: [6, 7, 8],
                    4: [9, 10, 11],
                    5: [12],
                    6: [13, 14],
                    7: [15, 16, 17],
                    9: [18, 19],
                    10: [20],
                    11: [21, 22],
                    15: [23],
                    16: [24, 25],
                }
            },
            4: {
                "n": 30,
                "budget": 12,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7, 8, 9],
                    4: [10, 11],
                    5: [12, 13, 14],
                    6: [15, 16],
                    7: [17],
                    8: [18, 19],
                    9: [20, 21],
                    10: [22, 23, 24],
                    11: [25],
                    12: [26],
                    14: [27, 28],
                    18: [29],
                    22: [30],
                }
            },
            5: {
                "n": 40,
                "budget": 12,
                "tree": {
                    1: [2, 3, 4, 5],
                    2: [6, 7, 8],
                    3: [9, 10],
                    4: [11, 12, 13],
                    5: [14, 15],
                    6: [16, 17],
                    7: [18, 19, 20],
                    8: [21],
                    9: [22, 23, 24],
                    10: [25, 26],
                    11: [27],
                    12: [28, 29],
                    13: [30, 31, 32],
                    14: [33, 34],
                    16: [35],
                    18: [36],
                    22: [37, 38],
                    28: [39],
                    30: [40],
                }
            },
        },
        "en": {
            1: {
                "n": 15,
                "budget": 12,
                "tree": {
                    1: [2, 3],
                    2: [4, 5, 6],
                    3: [7, 8],
                    4: [9, 10],
                    5: [11, 12],
                    6: [13],
                    7: [14],
                    8: [15],
                }
            },
            2: {
                "n": 20,
                "budget": 12,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6, 7],
                    3: [8, 9],
                    4: [10, 11, 12],
                    5: [13, 14],
                    6: [15],
                    7: [16],
                    8: [17, 18],
                    11: [19, 20],
                }
            },
            3: {
                "n": 25,
                "budget": 12,
                "tree": {
                    1: [2, 3],
                    2: [4, 5],
                    3: [6, 7, 8],
                    4: [9, 10, 11],
                    5: [12],
                    6: [13, 14],
                    7: [15, 16, 17],
                    9: [18, 19],
                    10: [20],
                    11: [21, 22],
                    15: [23],
                    16: [24, 25],
                }
            },
            4: {
                "n": 30,
                "budget": 12,
                "tree": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7, 8, 9],
                    4: [10, 11],
                    5: [12, 13, 14],
                    6: [15, 16],
                    7: [17],
                    8: [18, 19],
                    9: [20, 21],
                    10: [22, 23, 24],
                    11: [25],
                    12: [26],
                    14: [27, 28],
                    18: [29],
                    22: [30],
                }
            },
            5: {
                "n": 40,
                "budget": 12,
                "tree": {
                    1: [2, 3, 4, 5],
                    2: [6, 7, 8],
                    3: [9, 10],
                    4: [11, 12, 13],
                    5: [14, 15],
                    6: [16, 17],
                    7: [18, 19, 20],
                    8: [21],
                    9: [22, 23, 24],
                    10: [25, 26],
                    11: [27],
                    12: [28, 29],
                    13: [30, 31, 32],
                    14: [33, 34],
                    16: [35],
                    18: [36],
                    22: [37, 38],
                    28: [39],
                    30: [40],
                }
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
        self._game_info["n"] = cfg["n"]
        self._game_info["budget"] = cfg["budget"]
        
        self.tree = cfg["tree"]
        
        self.parent_map = {}
        for parent, children in self.tree.items():
            for child in children:
                self.parent_map[child] = parent
        
        self.function_values = {}
        self._compute_function_values(1)
        
        self.current_node = 1
        self.remaining_budget = cfg["budget"]
        self.function_query_count = 0
        self.total_leaves = self.function_values[1]

    def _compute_function_values(self, node):
        if node not in self.tree or len(self.tree[node]) == 0:
            self.function_values[node] = 1
            return 1
        
        total = 0
        for child in self.tree[node]:
            total += self._compute_function_values(child)
        self.function_values[node] = total
        return total

    def evaluate(self, parsed_info):
        if self.function_query_count < 3:
            return False

        raw_ans = parsed_info["answer"]

        answer_leaves = None
        if self.config.language == "zh":
            parts = raw_ans.split(",")
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    k = k.strip()
                    if k == "叶子总数":
                        try:
                            answer_leaves = int(v.strip())
                        except:
                            pass
        else:
            parts = raw_ans.split(",")
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    k = k.strip()
                    if k == "total_leaves":
                        try:
                            answer_leaves = int(v.strip())
                        except:
                            pass

        if answer_leaves is None:
            return False

        return answer_leaves == self.total_leaves

    def _cf_make_wrong(self, correct: str) -> str:
        match = re.search(r'=\s*(\d+)', correct)
        if match:
            original_val = int(match.group(1))
            wrong_val = original_val + random.choice([1, 2, 3])
            return correct.replace(match.group(1), str(wrong_val))
        else:
            return correct + " [ERROR]"

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        if "query_budget" in parsed_info:
            if is_zh:
                return f"剩余行动点 = {self.remaining_budget}"
            else:
                return f"Remaining action points = {self.remaining_budget}"
        
        if self.remaining_budget <= 0:
            if is_zh:
                raise ValueError("行动点已用尽，游戏结束。")
            else:
                raise ValueError("No action points remaining. Game over.")
        
        if "probe_child" in parsed_info:
            self.remaining_budget -= 1
            try:
                k = int(parsed_info["probe_child"].strip())
                if self.current_node in self.tree and 1 <= k <= len(self.tree[self.current_node]):
                    child_id = self.tree[self.current_node][k - 1]
                    if is_zh:
                        return f"子节点 {k} 的编号 = {child_id}"
                    else:
                        return f"Child {k} has ID = {child_id}"
                else:
                    if is_zh:
                        return f"子节点 {k} 不存在"
                    else:
                        return f"Child {k} does not exist"
            except ValueError:
                if is_zh:
                    return "错误：无效的子节点索引。"
                else:
                    return "Error: Invalid child index."
        
        if "move_to_child" in parsed_info:
            self.remaining_budget -= 1
            try:
                k = int(parsed_info["move_to_child"].strip())
                if self.current_node in self.tree and 1 <= k <= len(self.tree[self.current_node]):
                    child_id = self.tree[self.current_node][k - 1]
                    self.current_node = child_id
                    if is_zh:
                        return f"已移动到节点 {child_id}"
                    else:
                        return f"Moved to node {child_id}"
                else:
                    if is_zh:
                        return f"移动失败：子节点 {k} 不存在（已消耗 1 点）"
                    else:
                        return f"Move failed: Child {k} does not exist (1 point consumed)"
            except ValueError:
                if is_zh:
                    return "错误：无效的子节点索引（已消耗 1 点）。"
                else:
                    return "Error: Invalid child index (1 point consumed)."
        
        if "move_to_parent" in parsed_info:
            self.remaining_budget -= 1
            if self.current_node == 1:
                if is_zh:
                    return "移动失败：根节点无父节点（已消耗 1 点）"
                else:
                    return "Move failed: Root has no parent (1 point consumed)"
            else:
                parent_id = self.parent_map[self.current_node]
                self.current_node = parent_id
                if is_zh:
                    return f"已移动到父节点 {parent_id}"
                else:
                    return f"Moved to parent node {parent_id}"
        
        if "query_function" in parsed_info:
            self.remaining_budget -= 1
            self.function_query_count += 1
            func_value = self.function_values[self.current_node]
            if is_zh:
                return f"响应值 = {func_value}"
            else:
                return f"Response value = {func_value}"
        
        if "reset_to_root" in parsed_info:
            self.remaining_budget -= 1
            self.current_node = 1
            if is_zh:
                return "已回到根节点（ID=1）"
            else:
                return "Reset to root node (ID=1)"
        
        if is_zh:
            return "错误：无效的操作。"
        else:
            return "Error: Invalid operation."

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        is_zh = self.config.language == "zh"

        for node_id in sorted(self.tree.keys()):
            children = self.tree[node_id]
            for i, child_id in enumerate(children):
                k = i + 1
                if is_zh:
                    query_str = f"<probe_child>在节点{node_id}处探查第{k}个子节点</probe_child>"
                    ans = f"子节点 {k} 的编号 = {child_id}"
                else:
                    query_str = f"<probe_child>At node {node_id}, probe child {k}</probe_child>"
                    ans = f"Child {k} has ID = {child_id}"
                queries.append({
                    "query": query_str,
                    "answer": ans,
                })

        all_nodes = set(self.tree.keys())
        for children in self.tree.values():
            for c in children:
                all_nodes.add(c)
        for node_id in sorted(all_nodes):
            f_val = self.function_values[node_id]
            if is_zh:
                query_str = f"<query_function>在节点{node_id}处查询函数值</query_function>"
                ans = f"响应值 = {f_val}"
            else:
                query_str = f"<query_function>Query function value at node {node_id}</query_function>"
                ans = f"Response value = {f_val}"
            queries.append({
                "query": query_str,
                "answer": ans,
            })

        return queries