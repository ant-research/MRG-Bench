from .base import Game
import random
import itertools

class TreeTraversalInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"树遍历规则推断"游戏，规则如下：

游戏设定了一棵带根的有序树，包含 {n} 个节点。树的完整结构已知：
- 根节点：{root}
- 树结构：{tree_structure}

我已经秘密选择了一种遍历规则 R，它会对这棵树产生一个包含全部 {n} 个节点的排列序列 π（每个节点恰好出现一次）。这个遍历规则在整个游戏过程中保持不变。

你的目标是：推断出目标节点 {target} 在排列 π 中的位置（从 1 开始计数）。

你可以通过以下查询来收集信息（请尽可能少地使用查询）：

1. **比较查询**：询问节点 A 是否在节点 B 之前出现。回答"是"或"否"。
   - 使用次数：无限制

2. **后继查询**：询问某节点 A 的下一个节点是谁。若 A 是最后一个节点，返回"NONE"。
   - 使用次数：无限制

3. **首节点查询**：询问排列的第一个节点是谁。
   - 使用次数：每局最多 1 次

4. **前缀查询**：询问排列的前 k 个节点（1 到 5 之间）。
   - 使用次数：每局最多 3 次

5. **子集排序查询**：给定 2 到 6 个不重复的节点，返回它们在排列中的相对顺序。
   - 使用次数：每局最多 5 次

每次只能提出一个查询。请使用以下 XML 格式：

- 比较查询（例如询问节点 A 是否在节点 B 之前）：
<query_compare>A,B</query_compare>

- 后继查询（例如询问节点 A 的下一个节点）：
<query_next>A</query_next>

- 首节点查询：
<query_first></query_first>

- 前缀查询（例如询问前 3 个节点）：
<query_prefix>3</query_prefix>

- 子集排序查询（例如询问节点 A、B、C 的相对顺序）：
<query_order>A,B,C</query_order>

提交最终答案时，给出目标节点在排列中的位置（从 1 开始），格式如下：

<answer>位置</answer>

例如：<answer>5</answer> 表示目标节点在排列中的第 5 个位置。
"""

    game_rule_en = """\
Let's play a "Tree Traversal Inference" game. Here are the rules:

The game has a rooted ordered tree with {n} nodes. The complete tree structure is known:
- Root node: {root}
- Tree structure: {tree_structure}

I have secretly chosen a traversal rule R that produces a permutation sequence π containing all {n} nodes (each node appears exactly once). This traversal rule remains fixed throughout the game.

Your goal is: infer the position (1-indexed) of the target node {target} in the permutation π.

You can collect information through the following queries (use as few queries as possible):

1. **Compare Query**: Ask if node A appears before node B. Answer "Yes" or "No".
   - Usage limit: unlimited

2. **Next Query**: Ask for the next node after node A. Returns "NONE" if A is the last node.
   - Usage limit: unlimited

3. **First Query**: Ask for the first node in the permutation.
   - Usage limit: at most 1 per game

4. **Prefix Query**: Ask for the first k nodes (k between 1 and 5) in the permutation.
   - Usage limit: at most 3 per game

5. **Order Query**: Given 2 to 6 distinct nodes, return their relative order in the permutation.
   - Usage limit: at most 5 per game

Only one query per turn. Use the following XML format:

- Compare Query (e.g., ask if node A is before node B):
<query_compare>A,B</query_compare>

- Next Query (e.g., ask for the next node after A):
<query_next>A</query_next>

- First Query:
<query_first></query_first>

- Prefix Query (e.g., ask for the first 3 nodes):
<query_prefix>3</query_prefix>

- Order Query (e.g., ask for the relative order of nodes A, B, C):
<query_order>A,B,C</query_order>

When submitting the final answer, provide the position (1-indexed) of the target node in the permutation:

<answer>position</answer>

For example: <answer>5</answer> means the target node is at position 5 in the permutation.
"""

    contextualized_rule_zh_1 = """\
智能城市交通管理中心正在规划城市道路的自动清扫路线。作为路线规划分析师，你需要推断出清扫车的完整作业顺序。

城市路网具有树状拓扑结构，包含 {n} 个关键路口。路网的完整结构已知：
- 中心枢纽路口（根节点）：{root}
- 路口连接结构：{tree_structure}

系统已经秘密设定了一种路线规划算法 R，它会对这棵树产生一个包含全部 {n} 个路口的清扫访问序列 π（每个路口恰好被清扫一次）。这个规划算法在整个分析过程中保持不变。

你的目标是：推断出目标路口 {target} 在清扫序列 π 中的作业次序（从 1 开始计数）。

你可以通过以下查询来收集信息（请尽可能少地使用查询）：

1. **比较查询**：询问路口 A 是否在路口 B 之前被清扫。回答"是"或"否"。
   - 使用次数：无限制

2. **后继查询**：询问路口 A 清扫完毕后的下一个清扫路口是谁。若 A 是最后一个，返回"NONE"。
   - 使用次数：无限制

3. **首节点查询**：询问清扫序列的第一个路口是谁。
   - 使用次数：每局最多 1 次

4. **前缀查询**：询问清扫序列的前 k 个路口（1 到 5 之间）。
   - 使用次数：每局最多 3 次

5. **子集排序查询**：给定 2 到 6 个不重复的路口，返回它们在清扫序列中的相对先后顺序。
   - 使用次数：每局最多 5 次

每次只能提出一个查询。请使用以下 XML 格式：

- 比较查询（例如询问路口 A 是否在路口 B 之前）：
<query_compare>A,B</query_compare>

- 后继查询（例如询问路口 A 的下一个路口）：
<query_next>A</query_next>

- 首节点查询：
<query_first></query_first>

- 前缀查询（例如询问前 3 个路口）：
<query_prefix>3</query_prefix>

- 子集排序查询（例如询问路口 A、B、C 的相对顺序）：
<query_order>A,B,C</query_order>

提交最终答案时，给出目标路口在清扫序列中的作业次序（从 1 开始），格式如下：

<answer>位次</answer>

例如：<answer>5</answer> 表示目标路口是第 5 个被清扫的。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The smart city traffic management center is planning automated street sweeping routes. As a route planning analyst, you need to infer the complete operational sequence of the sweepers.

The urban road network has a tree-like topological structure containing {n} key intersections. The complete structure is known:
- Central Hub Intersection (Root node): {root}
- Intersection Connections: {tree_structure}

The system has secretly configured a route planning algorithm R that produces a sweeping visitation sequence π containing all {n} intersections (each intersection is swept exactly once). This algorithm remains fixed throughout the analysis.

Your goal is: infer the operational position (1-indexed) of the target intersection {target} in the sweeping sequence π.

You can collect information through the following queries (use as few queries as possible):

1. **Compare Query**: Ask if intersection A is swept before intersection B. Answer "Yes" or "No".
   - Usage limit: unlimited

2. **Next Query**: Ask for the next intersection to be swept after A. Returns "NONE" if A is the last one.
   - Usage limit: unlimited

3. **First Query**: Ask for the first intersection in the sweeping sequence.
   - Usage limit: at most 1 per game

4. **Prefix Query**: Ask for the first k intersections (k between 1 and 5) in the sequence.
   - Usage limit: at most 3 per game

5. **Order Query**: Given 2 to 6 distinct intersections, return their relative sweeping order.
   - Usage limit: at most 5 per game

Only one query per turn. Use the following XML format:

- Compare Query (e.g., ask if intersection A is before intersection B):
<query_compare>A,B</query_compare>

- Next Query (e.g., ask for the next intersection after A):
<query_next>A</query_next>

- First Query:
<query_first></query_first>

- Prefix Query (e.g., ask for the first 3 intersections):
<query_prefix>3</query_prefix>

- Order Query (e.g., ask for the relative order of intersections A, B, C):
<query_order>A,B,C</query_order>

When submitting the final answer, provide the operational position (1-indexed) of the target intersection in the sweeping sequence:

<answer>position</answer>

For example: <answer>5</answer> means the target intersection is swept 5th in the sequence.
"""

    contextualized_rule_zh_2 = """\
区域医疗中心正在紧急调度医疗物资配送网络。作为医疗物资调度员，你需要推断出运输车队的准确配送站点顺序。

该地区的医疗救治体系呈层级拓扑结构，包含 {n} 个医疗站点。网络体系结构已知：
- 总院（根节点）：{root}
- 下级医院及社区服务中心连接结构：{tree_structure}

调度系统已经秘密采用了一种物资配送规则 R，它会对这棵层级树产生一个包含全部 {n} 个站点的配送序列 π（每个站点恰好被访问一次）。该配送规则在整个调度过程中保持不变。

你的目标是：推断出目标医疗站点 {target} 在配送序列 π 中的接收次序（从 1 开始计数）。

你可以通过以下查询来收集信息（请尽可能少地使用查询）：

1. **比较查询**：询问站点 A 是否在站点 B 之前接收物资。回答"是"或"否"。
   - 使用次数：无限制

2. **后继查询**：询问站点 A 配送完毕后的下一个站点是谁。若 A 是最后一个站点，返回"NONE"。
   - 使用次数：无限制

3. **首节点查询**：询问首个接收配送物资的站点是谁。
   - 使用次数：每局最多 1 次

4. **前缀查询**：询问前 k 个接收物资的站点（1 到 5 之间）。
   - 使用次数：每局最多 3 次

5. **子集排序查询**：给定 2 到 6 个不重复的站点，返回它们在配送序列中的相对先后顺序。
   - 使用次数：每局最多 5 次

每次只能提出一个查询。请使用以下 XML 格式：

- 比较查询（例如询问站点 A 是否在站点 B 之前）：
<query_compare>A,B</query_compare>

- 后继查询（例如询问站点 A 的下一个配送站点）：
<query_next>A</query_next>

- 首节点查询：
<query_first></query_first>

- 前缀查询（例如询问前 3 个站点）：
<query_prefix>3</query_prefix>

- 子集排序查询（例如询问站点 A、B、C 的相对顺序）：
<query_order>A,B,C</query_order>

提交最终答案时，给出目标站点在配送序列中的接收次序（从 1 开始），格式如下：

<answer>位次</answer>

例如：<answer>5</answer> 表示目标站点是第 5 个接收物资的。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The regional medical center is urgently dispatching a medical supply distribution network. As a medical supply dispatcher, you need to infer the exact delivery sequence of the transport fleet.

The healthcare system in this region forms a hierarchical topological structure containing {n} medical sites. The network structure is known:
- General Hospital (Root node): {root}
- Subordinate hospitals and community centers connections: {tree_structure}

The dispatch system has secretly adopted a distribution rule R that produces a delivery sequence π containing all {n} sites (each site is visited exactly once) across this hierarchical tree. This distribution rule remains fixed throughout the dispatch process.

Your goal is: infer the receiving position (1-indexed) of the target medical site {target} in the delivery sequence π.

You can collect information through the following queries (use as few queries as possible):

1. **Compare Query**: Ask if site A receives supplies before site B. Answer "Yes" or "No".
   - Usage limit: unlimited

2. **Next Query**: Ask for the next site to be delivered after site A. Returns "NONE" if A is the last site.
   - Usage limit: unlimited

3. **First Query**: Ask for the very first site to receive supplies.
   - Usage limit: at most 1 per game

4. **Prefix Query**: Ask for the first k sites (k between 1 and 5) to receive supplies.
   - Usage limit: at most 3 per game

5. **Order Query**: Given 2 to 6 distinct sites, return their relative delivery order.
   - Usage limit: at most 5 per game

Only one query per turn. Use the following XML format:

- Compare Query (e.g., ask if site A is before site B):
<query_compare>A,B</query_compare>

- Next Query (e.g., ask for the next site after A):
<query_next>A</query_next>

- First Query:
<query_first></query_first>

- Prefix Query (e.g., ask for the first 3 sites):
<query_prefix>3</query_prefix>

- Order Query (e.g., ask for the relative order of sites A, B, C):
<query_order>A,B,C</query_order>

When submitting the final answer, provide the receiving position (1-indexed) of the target site in the delivery sequence:

<answer>position</answer>

For example: <answer>5</answer> means the target site is the 5th to receive supplies.
"""

    contextualized_rule_zh_3 = """\
在线教育平台正在为一门核心课程制定教学大纲。作为课程教研员，你需要推导出一套符合认知规律的知识点授课顺序。

该课程的知识体系呈现出严格的依赖关系树，包含 {n} 个核心知识点。知识树的完整结构已知：
- 导论知识点（根节点）：{root}
- 知识点前置依赖结构：{tree_structure}

教务系统已经秘密选定了一种大纲编排规则 R，它会对这棵知识树产生一个包含全部 {n} 个知识点的授课序列 π（每个知识点恰好被讲授一次）。该编排规则在整个教研过程中保持不变。

你的目标是：推断出目标知识点 {target} 在授课序列 π 中的排课位次（从 1 开始计数）。

你可以通过以下查询来收集信息（请尽可能少地使用查询）：

1. **比较查询**：询问知识点 A 是否在知识点 B 之前授课。回答"是"或"否"。
   - 使用次数：无限制

2. **后继查询**：询问讲授完知识点 A 后的下一个知识点是谁。若 A 是最后一个，返回"NONE"。
   - 使用次数：无限制

3. **首节点查询**：询问第一节课讲授的知识点是谁。
   - 使用次数：每局最多 1 次

4. **前缀查询**：询问授课序列的前 k 个知识点（1 到 5 之间）。
   - 使用次数：每局最多 3 次

5. **子集排序查询**：给定 2 到 6 个不重复的知识点，返回它们在授课序列中的相对先后顺序。
   - 使用次数：每局最多 5 次

每次只能提出一个查询。请使用以下 XML 格式：

- 比较查询（例如询问知识点 A 是否在知识点 B 之前）：
<query_compare>A,B</query_compare>

- 后继查询（例如询问知识点 A 的下一个知识点）：
<query_next>A</query_next>

- 首节点查询：
<query_first></query_first>

- 前缀查询（例如询问前 3 个知识点）：
<query_prefix>3</query_prefix>

- 子集排序查询（例如询问知识点 A、B、C 的相对顺序）：
<query_order>A,B,C</query_order>

提交最终答案时，给出目标知识点在授课序列中的排课位次（从 1 开始），格式如下：

<answer>位次</answer>

例如：<answer>5</answer> 表示目标知识点是第 5 个被讲授的。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
An online education platform is developing the syllabus for a core course. As a curriculum researcher, you need to deduce a teaching sequence of knowledge points that aligns with cognitive principles.

The course's knowledge system presents a strict dependency tree containing {n} core knowledge points. The complete structure of the knowledge tree is known:
- Introductory Point (Root node): {root}
- Knowledge dependency structure: {tree_structure}

The academic system has secretly chosen a syllabus scheduling rule R that produces a teaching sequence π containing all {n} knowledge points (each point is taught exactly once) based on this tree. This scheduling rule remains fixed throughout your research.

Your goal is: infer the scheduled position (1-indexed) of the target knowledge point {target} in the teaching sequence π.

You can collect information through the following queries (use as few queries as possible):

1. **Compare Query**: Ask if knowledge point A is taught before point B. Answer "Yes" or "No".
   - Usage limit: unlimited

2. **Next Query**: Ask for the next knowledge point to be taught after A. Returns "NONE" if A is the last one.
   - Usage limit: unlimited

3. **First Query**: Ask for the very first knowledge point in the teaching sequence.
   - Usage limit: at most 1 per game

4. **Prefix Query**: Ask for the first k knowledge points (k between 1 and 5) in the sequence.
   - Usage limit: at most 3 per game

5. **Order Query**: Given 2 to 6 distinct knowledge points, return their relative teaching order.
   - Usage limit: at most 5 per game

Only one query per turn. Use the following XML format:

- Compare Query (e.g., ask if point A is taught before point B):
<query_compare>A,B</query_compare>

- Next Query (e.g., ask for the next knowledge point after A):
<query_next>A</query_next>

- First Query:
<query_first></query_first>

- Prefix Query (e.g., ask for the first 3 knowledge points):
<query_prefix>3</query_prefix>

- Order Query (e.g., ask for the relative order of points A, B, C):
<query_order>A,B,C</query_order>

When submitting the final answer, provide the scheduled position (1-indexed) of the target knowledge point in the teaching sequence:

<answer>position</answer>

For example: <answer>5</answer> means the target knowledge point is taught 5th in the sequence.
"""

    contextualized_rule_zh_4 = """\
大型智能制造工厂正在调试一条自动化组装流水线。作为制造工艺工程师，你需要解析出产品的精确装配工序。

该产品的物料清单（BOM）呈现标准树状分解结构，包含 {n} 个总成或零部件工序。工艺树的完整结构已知：
- 最终成品总成（根节点）：{root}
- 子部件装配层级结构：{tree_structure}

制造执行系统（MES）已经秘密下发了一种自动化调度策略 R，它会对这棵工艺树产生一个包含全部 {n} 个工序的装配执行序列 π（每个工序恰好执行一次）。该调度策略在整个生产调试期间保持不变。

你的目标是：推断出目标工序 {target} 在装配执行序列 π 中的加工作业位次（从 1 开始计数）。

你可以通过以下查询来收集信息（请尽可能少地使用查询）：

1. **比较查询**：询问工序 A 是否在工序 B 之前装配。回答"是"或"否"。
   - 使用次数：无限制

2. **后继查询**：询问工序 A 完成后的下一个装配工序是谁。若 A 是最后一道工序，返回"NONE"。
   - 使用次数：无限制

3. **首节点查询**：询问整条流水线的首个装配工序是谁。
   - 使用次数：每局最多 1 次

4. **前缀查询**：询问装配序列的前 k 个工序（1 到 5 之间）。
   - 使用次数：每局最多 3 次

5. **子集排序查询**：给定 2 到 6 个不重复的工序，返回它们在装配序列中的相对先后顺序。
   - 使用次数：每局最多 5 次

每次只能提出一个查询。请使用以下 XML 格式：

- 比较查询（例如询问工序 A 是否在工序 B 之前）：
<query_compare>A,B</query_compare>

- 后继查询（例如询问工序 A 的下一个工序）：
<query_next>A</query_next>

- 首节点查询：
<query_first></query_first>

- 前缀查询（例如询问前 3 个工序）：
<query_prefix>3</query_prefix>

- 子集排序查询（例如询问工序 A、B、C 的相对顺序）：
<query_order>A,B,C</query_order>

提交最终答案时，给出目标工序在装配序列中的加工作业位次（从 1 开始），格式如下：

<answer>位次</answer>

例如：<answer>5</answer> 表示目标工序是第 5 个被执行的。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
A large smart manufacturing plant is commissioning an automated assembly line. As a manufacturing process engineer, you need to parse the precise assembly sequence of the product.

The product's Bill of Materials (BOM) presents a standard tree-like decomposition structure containing {n} subassemblies or component operations. The complete structure of the process tree is known:
- Final Product Assembly (Root node): {root}
- Sub-component assembly hierarchy: {tree_structure}

The Manufacturing Execution System (MES) has secretly issued an automated scheduling strategy R that produces an assembly execution sequence π containing all {n} operations (each operation is executed exactly once) based on this process tree. This scheduling strategy remains fixed throughout the commissioning period.

Your goal is: infer the operational position (1-indexed) of the target operation {target} in the assembly execution sequence π.

You can collect information through the following queries (use as few queries as possible):

1. **Compare Query**: Ask if operation A is assembled before operation B. Answer "Yes" or "No".
   - Usage limit: unlimited

2. **Next Query**: Ask for the next assembly operation after A. Returns "NONE" if A is the final operation.
   - Usage limit: unlimited

3. **First Query**: Ask for the very first assembly operation on the line.
   - Usage limit: at most 1 per game

4. **Prefix Query**: Ask for the first k operations (k between 1 and 5) in the sequence.
   - Usage limit: at most 3 per game

5. **Order Query**: Given 2 to 6 distinct operations, return their relative assembly order.
   - Usage limit: at most 5 per game

Only one query per turn. Use the following XML format:

- Compare Query (e.g., ask if operation A is before operation B):
<query_compare>A,B</query_compare>

- Next Query (e.g., ask for the next operation after A):
<query_next>A</query_next>

- First Query:
<query_first></query_first>

- Prefix Query (e.g., ask for the first 3 operations):
<query_prefix>3</query_prefix>

- Order Query (e.g., ask for the relative order of operations A, B, C):
<query_order>A,B,C</query_order>

When submitting the final answer, provide the operational position (1-indexed) of the target operation in the assembly execution sequence:

<answer>position</answer>

For example: <answer>5</answer> means the target operation is the 5th to be executed.
"""

    contextualized_rule_zh_5 = """\
法院正在对一起复杂的商业纠纷案进行开庭审理。作为诉讼律师，你需要准确预判法官审查各项证据的法定程序顺序。

该案件的证据链具有严密的树状层级引用结构，包含 {n} 份关键证据。证据树的完整结构已知：
- 核心主张证据（根节点）：{root}
- 附属证据链条与相互印证结构：{tree_structure}

法庭审理已经秘密确立了一种证据审查规则 R，它会对这棵证据树产生一个包含全部 {n} 份证据的质证序列 π（每份证据恰好被审查一次）。该审查规则在整个庭审阶段保持不变。

你的目标是：推断出目标证据 {target} 在质证序列 π 中的审查位次（从 1 开始计数）。

你可以通过以下查询来收集信息（请尽可能少地使用查询）：

1. **比较查询**：询问证据 A 是否在证据 B 之前进行审查。回答"是"或"否"。
   - 使用次数：无限制

2. **后继查询**：询问证据 A 审查完毕后的下一份质证证据是谁。若 A 是最后一份，返回"NONE"。
   - 使用次数：无限制

3. **首节点查询**：询问法庭上第一份宣读审查的证据是谁。
   - 使用次数：每局最多 1 次

4. **前缀查询**：询问质证序列的前 k 份证据（1 到 5 之间）。
   - 使用次数：每局最多 3 次

5. **子集排序查询**：给定 2 到 6 份不重复的证据，返回它们在法庭审查中的相对先后顺序。
   - 使用次数：每局最多 5 次

每次只能提出一个查询。请使用以下 XML 格式：

- 比较查询（例如询问证据 A 是否在证据 B 之前）：
<query_compare>A,B</query_compare>

- 后继查询（例如询问证据 A 的下一份审查证据）：
<query_next>A</query_next>

- 首节点查询：
<query_first></query_first>

- 前缀查询（例如询问前 3 份证据）：
<query_prefix>3</query_prefix>

- 子集排序查询（例如询问证据 A、B、C 的相对顺序）：
<query_order>A,B,C</query_order>

提交最终答案时，给出目标证据在法庭质证序列中的审查位次（从 1 开始），格式如下：

<answer>位次</answer>

例如：<answer>5</answer> 表示目标证据是第 5 份被审查的。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The court is holding a hearing for a complex commercial dispute. As a litigator, you need to accurately predict the statutory procedural sequence in which the judge will examine the evidence.

The chain of evidence for this case has a strict tree-like hierarchical reference structure containing {n} key pieces of evidence. The complete structure of the evidence tree is known:
- Core Claim Evidence (Root node): {root}
- Subordinate evidence chains and corroboration structure: {tree_structure}

The court proceedings have secretly established an evidence examination rule R that produces a cross-examination sequence π containing all {n} pieces of evidence (each piece is examined exactly once) based on this evidence tree. This examination rule remains fixed throughout the trial phase.

Your goal is: infer the examination position (1-indexed) of the target evidence {target} in the cross-examination sequence π.

You can collect information through the following queries (use as few queries as possible):

1. **Compare Query**: Ask if evidence A is examined before evidence B. Answer "Yes" or "No".
   - Usage limit: unlimited

2. **Next Query**: Ask for the next evidence to be cross-examined after A. Returns "NONE" if A is the last piece.
   - Usage limit: unlimited

3. **First Query**: Ask for the very first piece of evidence to be presented and examined in court.
   - Usage limit: at most 1 per game

4. **Prefix Query**: Ask for the first k pieces of evidence (k between 1 and 5) in the sequence.
   - Usage limit: at most 3 per game

5. **Order Query**: Given 2 to 6 distinct pieces of evidence, return their relative examination order.
   - Usage limit: at most 5 per game

Only one query per turn. Use the following XML format:

- Compare Query (e.g., ask if evidence A is before evidence B):
<query_compare>A,B</query_compare>

- Next Query (e.g., ask for the next evidence after A):
<query_next>A</query_next>

- First Query:
<query_first></query_first>

- Prefix Query (e.g., ask for the first 3 pieces of evidence):
<query_prefix>3</query_prefix>

- Order Query (e.g., ask for the relative order of evidence A, B, C):
<query_order>A,B,C</query_order>

When submitting the final answer, provide the examination position (1-indexed) of the target evidence in the cross-examination sequence:

<answer>position</answer>

For example: <answer>5</answer> means the target evidence is the 5th to be examined.
"""

    tags = ["answer", "query_compare", "query_next", "query_first", "query_prefix", "query_order"]

    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "root": "A",
                "tree": {
                    "A": ["B", "C"],
                    "B": ["D"],
                    "C": ["E"],
                    "D": [],
                    "E": []
                },
                "traversal": "preorder",
                "target": "D"
            },
            2: {
                "n": 7,
                "root": "A",
                "tree": {
                    "A": ["B", "C"],
                    "B": ["D", "E"],
                    "C": ["F"],
                    "D": [],
                    "E": [],
                    "F": ["G"],
                    "G": []
                },
                "traversal": "inorder",
                "target": "F"
            },
            3: {
                "n": 9,
                "root": "A",
                "tree": {
                    "A": ["B", "C"],
                    "B": ["D", "E"],
                    "C": ["F", "G"],
                    "D": ["H"],
                    "E": [],
                    "F": [],
                    "G": ["I"],
                    "H": [],
                    "I": []
                },
                "traversal": "postorder",
                "target": "G"
            },
            4: {
                "n": 11,
                "root": "A",
                "tree": {
                    "A": ["B", "C", "D"],
                    "B": ["E", "F"],
                    "C": ["G"],
                    "D": ["H", "I"],
                    "E": ["J"],
                    "F": [],
                    "G": ["K"],
                    "H": [],
                    "I": [],
                    "J": [],
                    "K": []
                },
                "traversal": "levelorder",
                "target": "H"
            },
            5: {
                "n": 13,
                "root": "A",
                "tree": {
                    "A": ["B", "C"],
                    "B": ["D", "E", "F"],
                    "C": ["G", "H"],
                    "D": ["I"],
                    "E": [],
                    "F": ["J"],
                    "G": ["K", "L"],
                    "H": [],
                    "I": [],
                    "J": ["M"],
                    "K": [],
                    "L": [],
                    "M": []
                },
                "traversal": "right_first_preorder",
                "target": "J"
            }
        },
        "en": {
            1: {
                "n": 5,
                "root": "A",
                "tree": {
                    "A": ["B", "C"],
                    "B": ["D"],
                    "C": ["E"],
                    "D": [],
                    "E": []
                },
                "traversal": "preorder",
                "target": "D"
            },
            2: {
                "n": 7,
                "root": "A",
                "tree": {
                    "A": ["B", "C"],
                    "B": ["D", "E"],
                    "C": ["F"],
                    "D": [],
                    "E": [],
                    "F": ["G"],
                    "G": []
                },
                "traversal": "inorder",
                "target": "F"
            },
            3: {
                "n": 9,
                "root": "A",
                "tree": {
                    "A": ["B", "C"],
                    "B": ["D", "E"],
                    "C": ["F", "G"],
                    "D": ["H"],
                    "E": [],
                    "F": [],
                    "G": ["I"],
                    "H": [],
                    "I": []
                },
                "traversal": "postorder",
                "target": "G"
            },
            4: {
                "n": 11,
                "root": "A",
                "tree": {
                    "A": ["B", "C", "D"],
                    "B": ["E", "F"],
                    "C": ["G"],
                    "D": ["H", "I"],
                    "E": ["J"],
                    "F": [],
                    "G": ["K"],
                    "H": [],
                    "I": [],
                    "J": [],
                    "K": []
                },
                "traversal": "levelorder",
                "target": "H"
            },
            5: {
                "n": 13,
                "root": "A",
                "tree": {
                    "A": ["B", "C"],
                    "B": ["D", "E", "F"],
                    "C": ["G", "H"],
                    "D": ["I"],
                    "E": [],
                    "F": ["J"],
                    "G": ["K", "L"],
                    "H": [],
                    "I": [],
                    "J": ["M"],
                    "K": [],
                    "L": [],
                    "M": []
                },
                "traversal": "right_first_preorder",
                "target": "J"
            }
        }
    }

    def __init__(self, config):
        self.query_first_count = 0
        self.query_prefix_count = 0
        self.query_order_count = 0
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
        self._game_info["root"] = cfg["root"]
        
        tree_desc = []
        for node, children in cfg["tree"].items():
            if children:
                tree_desc.append(f"{node} -> [{', '.join(children)}]")
            else:
                tree_desc.append(f"{node} -> []")
        self._game_info["tree_structure"] = "; ".join(tree_desc)
        
        self.tree = cfg["tree"]
        self.root = cfg["root"]
        
        traversal_type = cfg["traversal"]
        self.permutation = self._generate_traversal(traversal_type)
        
        self.target_node = random.choice(self.permutation)
        self._game_info["target"] = self.target_node
        
        self.pos_map = {node: idx for idx, node in enumerate(self.permutation)}
        self.target_position = self.pos_map[self.target_node] + 1

    def _generate_traversal(self, traversal_type):
        if traversal_type == "preorder":
            return self._preorder(self.root)
        elif traversal_type == "inorder":
            return self._inorder(self.root)
        elif traversal_type == "postorder":
            return self._postorder(self.root)
        elif traversal_type == "levelorder":
            return self._levelorder(self.root)
        elif traversal_type == "right_first_preorder":
            return self._right_first_preorder(self.root)
        else:
            raise ValueError(f"Unknown traversal type: {traversal_type}")

    def _preorder(self, node):
        if node is None:
            return []
        result = [node]
        for child in self.tree[node]:
            result.extend(self._preorder(child))
        return result

    def _inorder(self, node):
        if node is None:
            return []
        children = self.tree[node]
        result = []
        if len(children) > 0:
            result.extend(self._inorder(children[0]))
        result.append(node)
        for child in children[1:]:
            result.extend(self._inorder(child))
        return result

    def _postorder(self, node):
        if node is None:
            return []
        result = []
        for child in self.tree[node]:
            result.extend(self._postorder(child))
        result.append(node)
        return result

    def _levelorder(self, node):
        if node is None:
            return []
        result = []
        queue = [node]
        while queue:
            current = queue.pop(0)
            result.append(current)
            queue.extend(self.tree[current])
        return result

    def _right_first_preorder(self, node):
        if node is None:
            return []
        result = [node]
        for child in reversed(self.tree[node]):
            result.extend(self._right_first_preorder(child))
        return result

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.target_position
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"
        error_msg = "错误：" if lang == "zh" else "Error: "
        
        if "query_compare" in parsed_info:
            try:
                nodes = [n.strip() for n in parsed_info["query_compare"].split(",")]
                if len(nodes) != 2:
                    raise ValueError
                a, b = nodes
                if a not in self.pos_map or b not in self.pos_map:
                    return error_msg + ("节点不存在" if lang == "zh" else "Node does not exist")
                return yes_res if self.pos_map[a] < self.pos_map[b] else no_res
            except Exception:
                return error_msg + ("格式无效" if lang == "zh" else "Invalid format")
        
        elif "query_next" in parsed_info:
            try:
                node = parsed_info["query_next"].strip()
                if node not in self.pos_map:
                    return error_msg + ("节点不存在" if lang == "zh" else "Node does not exist")
                pos = self.pos_map[node]
                if pos == len(self.permutation) - 1:
                    return "NONE"
                return self.permutation[pos + 1]
            except Exception:
                return error_msg + ("格式无效" if lang == "zh" else "Invalid format")
        
        elif "query_first" in parsed_info:
            self.query_first_count += 1
            if self.query_first_count > 1:
                return error_msg + ("首节点查询次数超限" if lang == "zh" else "First query limit exceeded")
            return self.permutation[0]
        
        elif "query_prefix" in parsed_info:
            self.query_prefix_count += 1
            if self.query_prefix_count > 3:
                return error_msg + ("前缀查询次数超限" if lang == "zh" else "Prefix query limit exceeded")
            try:
                k = int(parsed_info["query_prefix"].strip())
                if k < 1 or k > 5:
                    return error_msg + ("k 必须在 1 到 5 之间" if lang == "zh" else "k must be between 1 and 5")
                if k > len(self.permutation):
                    k = len(self.permutation)
                return ", ".join(self.permutation[:k])
            except Exception:
                return error_msg + ("格式无效" if lang == "zh" else "Invalid format")
        
        elif "query_order" in parsed_info:
            self.query_order_count += 1
            if self.query_order_count > 5:
                return error_msg + ("子集排序查询次数超限" if lang == "zh" else "Order query limit exceeded")
            try:
                nodes = [n.strip() for n in parsed_info["query_order"].split(",")]
                if len(nodes) < 2 or len(nodes) > 6:
                    return error_msg + ("节点数必须在 2 到 6 之间" if lang == "zh" else "Node count must be between 2 and 6")
                if len(nodes) != len(set(nodes)):
                    return error_msg + ("节点不能重复" if lang == "zh" else "Nodes must be distinct")
                for node in nodes:
                    if node not in self.pos_map:
                        return error_msg + ("节点不存在" if lang == "zh" else "Node does not exist")
                sorted_nodes = sorted(nodes, key=lambda n: self.pos_map[n])
                return ", ".join(sorted_nodes)
            except Exception:
                return error_msg + ("格式无效" if lang == "zh" else "Invalid format")
        
        else:
            raise ValueError("No valid query tag found")

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            s_lower = correct.lower()
            if s_lower == "yes":
                if correct.isupper(): return "NO"
                if correct[0].isupper(): return "No"
                return "no"
            elif s_lower == "no":
                if correct.isupper(): return "YES"
                if correct[0].isupper(): return "Yes"
                return "yes"
        
        if correct == "NONE":
            return self.permutation[0]
        
        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)
        
        if correct.strip() in self.pos_map:
            idx = self.pos_map[correct.strip()]
            wrong_idx = (idx + 1) % len(self.permutation)
            return self.permutation[wrong_idx]
        
        parts = [p.strip() for p in correct.split(",")]
        if len(parts) > 1 and all(p in self.pos_map for p in parts):
            return ", ".join(reversed(parts))
        
        return correct + "_WRONG"
    
    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        lang = self.config.language
        nodes = self.permutation
        n_count = len(nodes)
        
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"
        
        queries.append({
            "query": "<query_first></query_first>",
            "answer": nodes[0]
        })
        
        limit_k = min(5, n_count)
        for k in range(1, limit_k + 1):
            queries.append({
                "query": f"<query_prefix>{k}</query_prefix>",
                "answer": ", ".join(nodes[:k])
            })
            
        for node in nodes:
            idx = self.pos_map[node]
            if idx == n_count - 1:
                ans = "NONE"
            else:
                ans = nodes[idx + 1]
            queries.append({
                "query": f"<query_next>{node}</query_next>",
                "answer": ans
            })
            
        for a, b in itertools.permutations(nodes, 2):
            is_before = self.pos_map[a] < self.pos_map[b]
            ans = yes_res if is_before else no_res
            queries.append({
                "query": f"<query_compare>{a},{b}</query_compare>",
                "answer": ans
            })
            
        for subset in itertools.combinations(nodes, 2):
            input_nodes = list(subset)
            sorted_nodes = sorted(input_nodes, key=lambda n: self.pos_map[n])
            ans = ", ".join(sorted_nodes)
            input_str = ",".join(input_nodes)
            queries.append({
                "query": f"<query_order>{input_str}</query_order>",
                "answer": ans
            })
        
        for subset in itertools.combinations(nodes, 3):
            input_nodes = list(subset)
            sorted_nodes = sorted(input_nodes, key=lambda n: self.pos_map[n])
            ans = ", ".join(sorted_nodes)
            input_str = ",".join(input_nodes)
            queries.append({
                "query": f"<query_order>{input_str}</query_order>",
                "answer": ans
            })

        return queries