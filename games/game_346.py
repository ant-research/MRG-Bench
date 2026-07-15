from .base import Game
import re

class TreePreorderPositionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树前序遍历位置推理"游戏，规则如下：

游戏设定了一棵固定但未知边结构的有根有序树，节点总数为 {n}。每个节点都有唯一标识（整数编号）。树的根节点为 {root}，目标节点为 {target}。每个节点的子节点按照从 1 开始的固定顺序排列。

遍历规则为前序遍历：访问某节点后，按其子节点的既定顺序依次递归访问每个子树。

你的目标是通过询问问题，确定目标节点 {target} 在整棵树的前序遍历中的访问序号（从 1 开始）。

你可以反复向我提出以下七类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 父节点查询：询问节点 X 的直接父节点标识。若 X 是根节点，回答"无"。
2. 子节点数量查询：询问节点 X 的直接子节点数量。回答一个非负整数。
3. 第 k 个子节点查询：询问节点 X 的第 k 个子节点标识。若 k 越界，回答"不存在"。
4. 在父节点中的序位查询：询问节点 X 在其父节点的子序中的排名（从 1 开始）。若 X 是根节点，回答"无"。
5. 祖先关系查询：询问节点 U 是否为节点 V 的祖先（包含直接父及更高层）。回答"是"或"否"。
6. 子树大小查询：询问以节点 X 为根的子树的节点总数（包含 X 自身）。回答一个正整数。
7. 同父节点先后查询：若节点 A 和 B 有相同父节点，询问 A 是否在父节点的子序中先于 B。若同父，回答"是"或"否"；若不同父，回答"不适用"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 父节点查询（例如查询节点 5 的父节点）：
<query_parent>5</query_parent>

- 子节点数量查询（例如查询节点 3 的子节点数量）：
<query_children_count>3</query_children_count>

- 第 k 个子节点查询（例如查询节点 3 的第 2 个子节点）：
<query_kth_child>3,2</query_kth_child>

- 在父节点中的序位查询（例如查询节点 5 在其父节点中的序位）：
<query_position>5</query_position>

- 祖先关系查询（例如查询节点 1 是否为节点 5 的祖先）：
<query_ancestor>1,5</query_ancestor>

- 子树大小查询（例如查询节点 3 为根的子树大小）：
<query_subtree_size>3</query_subtree_size>

- 同父节点先后查询（例如查询节点 2 和 3 的先后关系）：
<query_sibling_order>2,3</query_sibling_order>

提交最终答案时，请提供目标节点 {target} 在前序遍历中的访问序号（从 1 开始的正整数），格式如下：

<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Tree Preorder Position Reasoning" game. Here are the rules:

The game has a fixed but unknown rooted ordered tree with {n} nodes in total. Each node has a unique identifier (integer ID). The root node is {root}, and the target node is {target}. Each node's children are arranged in a fixed order starting from 1.

The traversal rule is preorder traversal: after visiting a node, recursively visit each of its child subtrees in the predefined order.

Your goal is to determine the visiting position (1-based) of the target node {target} in the entire tree's preorder traversal by asking questions.

You can repeatedly ask me the following seven types of questions (one per turn), and I will answer truthfully based on the true structure:

1. Parent Query: Ask for the direct parent node ID of node X. If X is the root, answer "None".
2. Children Count Query: Ask for the number of direct children of node X. Answer a non-negative integer.
3. K-th Child Query: Ask for the k-th child node ID of node X. If k is out of bounds, answer "NotExist".
4. Position Query: Ask for the rank (1-based) of node X among its parent's children. If X is the root, answer "None".
5. Ancestor Query: Ask if node U is an ancestor of node V (including direct parent and higher levels). Answer "Yes" or "No".
6. Subtree Size Query: Ask for the total number of nodes in the subtree rooted at node X (including X itself). Answer a positive integer.
7. Sibling Order Query: If nodes A and B share the same parent, ask if A comes before B in the parent's child order. If they share the same parent, answer "Yes" or "No"; otherwise, answer "NotApplicable".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Parent Query (e.g., querying parent of node 5):
<query_parent>5</query_parent>

- Children Count Query (e.g., querying children count of node 3):
<query_children_count>3</query_children_count>

- K-th Child Query (e.g., querying the 2nd child of node 3):
<query_kth_child>3,2</query_kth_child>

- Position Query (e.g., querying position of node 5 in its parent's children):
<query_position>5</query_position>

- Ancestor Query (e.g., querying if node 1 is ancestor of node 5):
<query_ancestor>1,5</query_ancestor>

- Subtree Size Query (e.g., querying subtree size rooted at node 3):
<query_subtree_size>3</query_subtree_size>

- Sibling Order Query (e.g., querying order between nodes 2 and 3):
<query_sibling_order>2,3</query_sibling_order>

When submitting the final answer, provide the visiting position (1-based positive integer) of target node {target} in the preorder traversal:

<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个基于"高铁调度网络"的指令下达推理游戏，规则如下：

游戏设定了一个固定但未知边结构的树形调度网络，节点总数为 {n}。每个节点代表一个调度中心或站点（用唯一的整数编号标识）。全国总调度中心（根节点）为 {root}，目标被查站点为 {target}。每个站点的直属下级站点按照从 1 开始的固定优先级顺序排列。

指令下达规则为深度优先的逐级确认流程：总调度中心下发指令后，每个中心在确认收到后，会按既定优先级顺序依次将其完整传达到辖区内的一个分支到底，才会轮到下一个下级分支。

你的目标是通过询问问题，确定目标站点 {target} 在整轮指令下达流程中的绝对通知序号（从 1 开始）。

你可以反复向我提出以下七类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 直属上级查询：询问站点 X 的直接上级调度中心标识。若 X 是总调度中心，回答"无"。
2. 直管下级数量查询：询问站点 X 直接管理的下级站点数量。回答一个非负整数。
3. 第 k 个下级查询：询问站点 X 的第 k 个下级站点标识。若 k 越界，回答"不存在"。
4. 上级管辖内的序位查询：询问站点 X 在其直属上级的下发顺序中的排名（从 1 开始）。若 X 是总中心，回答"无"。
5. 管辖关系查询：询问机构 U 是否为站点 V 的上级管理方（包含直接及更高层）。回答"是"或"否"。
6. 辖区规模查询：询问以站点 X 为首的整个辖区（含 X 自身及所有直接和间接下级）的站点总数。回答一个正整数。
7. 同级先后查询：若站点 A 和 B 直属同一个上级，询问 A 是否在该上级的指令下达中先于 B。若同属一上级，回答"是"或"否"；若不是，回答"不适用"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 直属上级查询（例如查询站点 5 的上级）：
<query_parent>5</query_parent>

- 直管下级数量查询（例如查询站点 3 的下级数量）：
<query_children_count>3</query_children_count>

- 第 k 个下级查询（例如查询站点 3 的第 2 个下级）：
<query_kth_child>3,2</query_kth_child>

- 上级管辖内的序位查询（例如查询站点 5 在其上级中的排位）：
<query_position>5</query_position>

- 管辖关系查询（例如查询机构 1 是否为 5 的上级）：
<query_ancestor>1,5</query_ancestor>

- 辖区规模查询（例如查询站点 3 的辖区大小）：
<query_subtree_size>3</query_subtree_size>

- 同级先后查询（例如查询同级站点 2 和 3 的先后）：
<query_sibling_order>2,3</query_sibling_order>

提交最终答案时，请提供目标站点 {target} 在指令下达流程中的接收序号（从 1 开始的正整数）：

<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "High-Speed Rail Dispatch Network" reasoning game. Here are the rules:

The game features a fixed but unknown tree-structured dispatch network with {n} nodes in total. Each node represents a dispatch center or station (with a unique integer ID). The national primary dispatch center (root node) is {root}, and the target station is {target}. Each station's direct subordinate stations are arranged in a fixed priority order starting from 1.

The instruction transmission rule follows a depth-first hierarchical confirmation process: after receiving the instruction, each center recursively transmits it to each of its subordinate branches completely in the predefined priority order.

Your goal is to determine the absolute receiving sequence number (1-based) of the target station {target} in the entire network's instruction transmission process by asking questions.

You can repeatedly ask me the following seven types of questions (one per turn), and I will answer truthfully based on the true structure:

1. Direct Superior Query: Ask for the direct superior center ID of station X. If X is the primary center, answer "None".
2. Subordinate Count Query: Ask for the number of direct subordinate stations of station X. Answer a non-negative integer.
3. K-th Subordinate Query: Ask for the k-th subordinate station ID of station X. If k is out of bounds, answer "NotExist".
4. Position Query: Ask for the rank (1-based) of station X among its direct superior's transmission order. If X is the primary center, answer "None".
5. Jurisdiction Query: Ask if organization U is a superior management entity of station V (including direct and higher levels). Answer "Yes" or "No".
6. Jurisdiction Size Query: Ask for the total number of stations in the jurisdiction headed by station X (including X itself). Answer a positive integer.
7. Sibling Order Query: If stations A and B share the same direct superior, ask if A comes before B in the superior's transmission order. If they share the same superior, answer "Yes" or "No"; otherwise, answer "NotApplicable".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Direct Superior Query (e.g., querying superior of station 5):
<query_parent>5</query_parent>

- Subordinate Count Query (e.g., querying subordinate count of station 3):
<query_children_count>3</query_children_count>

- K-th Subordinate Query (e.g., querying the 2nd subordinate of station 3):
<query_kth_child>3,2</query_kth_child>

- Position Query (e.g., querying transmission rank of station 5):
<query_position>5</query_position>

- Jurisdiction Query (e.g., querying if org 1 is superior of station 5):
<query_ancestor>1,5</query_ancestor>

- Jurisdiction Size Query (e.g., querying jurisdiction size of station 3):
<query_subtree_size>3</query_subtree_size>

- Sibling Order Query (e.g., querying priority between stations 2 and 3):
<query_sibling_order>2,3</query_sibling_order>

When submitting the final answer, provide the receiving sequence number (1-based positive integer) of target station {target} in the transmission process:

<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个基于"传染病传播溯源"的流行病学调查游戏，规则如下：

系统截获了一段固定但未知结构的树形传染链网络，节点总数为 {n}。每个节点代表一名确诊患者（用唯一的整数编号标识）。该链条的"零号病人"（根节点）为 {root}，疾控中心当前追踪的目标患者为 {target}。每名患者直接传染的下游病例按确诊时间的先后顺序从 1 开始固定排列。

排查机制为深度追踪溯源流程：疾控人员确认一名确诊者后，会按确诊先后顺序，递归地将其某一分支传染的下游全部病例追踪到底，才会排查该确诊者的下一个同级感染者。

你的目标是通过询问问题，确定目标患者 {target} 在这轮传染链溯源清查中的绝对排查序号（从 1 开始）。

你可以反复向我提出以下七类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 直接传染源查询：询问患者 X 的直接传染源（上游患者）标识。若 X 是零号病人，回答"无"。
2. 直接传染人数查询：询问患者 X 直接传染的下游患者数量。回答一个非负整数。
3. 第 k 个感染者查询：询问患者 X 传染的第 k 个下游患者标识。若 k 越界，回答"不存在"。
4. 同源感染序位查询：询问患者 X 在其直接传染源传染的所有人中的排位（从 1 开始）。若 X 是零号病人，回答"无"。
5. 溯源关系查询：询问患者 U 是否在患者 V 的传染传播链上游（包含直接及间接）。回答"是"或"否"。
6. 传播链规模查询：询问由患者 X 直接或间接引发的所有后续病例总数（包含 X 自身）。回答一个正整数。
7. 同源先后查询：若患者 A 和 B 被同一个源头传染，询问 A 是否先于 B 被感染。若是，回答"是"或"否"；若不是同源，回答"不适用"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 直接传染源查询（例如查询患者 5 的传染源）：
<query_parent>5</query_parent>

- 直接传染人数查询（例如查询患者 3 传染的人数）：
<query_children_count>3</query_children_count>

- 第 k 个感染者查询（例如查询患者 3 传染的第 2 个人）：
<query_kth_child>3,2</query_kth_child>

- 同源感染序位查询（例如查询患者 5 在同源感染者中的排位）：
<query_position>5</query_position>

- 溯源关系查询（例如查询患者 1 是否为患者 5 的传染源头）：
<query_ancestor>1,5</query_ancestor>

- 传播链规模查询（例如查询患者 3 引发的传播链总人数）：
<query_subtree_size>3</query_subtree_size>

- 同源先后查询（例如查询同源患者 2 和 3 的感染先后）：
<query_sibling_order>2,3</query_sibling_order>

提交最终答案时，请提供目标患者 {target} 在溯源清查流程中的排查序号（从 1 开始的正整数）：

<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play an "Epidemiological Traceback" reasoning game. Here are the rules:

The system has intercepted a fixed but unknown tree-structured transmission network with {n} nodes in total. Each node represents a confirmed patient (with a unique integer ID). The "Patient Zero" (root node) is {root}, and the target patient to trace is {target}. Each patient's direct downstream infectees are arranged in a fixed chronological order starting from 1.

The investigation mechanism follows a depth-first traceback process: after confirming a patient, epidemiological investigators recursively trace all downstream cases of a single branch completely in chronological order before moving to the patient's next direct infectee.

Your goal is to determine the absolute investigation sequence number (1-based) of the target patient {target} in the entire traceback process by asking questions.

You can repeatedly ask me the following seven types of questions (one per turn), and I will answer truthfully based on the true structure:

1. Direct Source Query: Ask for the direct source (upstream patient) ID of patient X. If X is Patient Zero, answer "None".
2. Direct Infectee Count Query: Ask for the number of direct downstream infectees of patient X. Answer a non-negative integer.
3. K-th Infectee Query: Ask for the k-th downstream infectee ID of patient X. If k is out of bounds, answer "NotExist".
4. Position Query: Ask for the chronological rank (1-based) of patient X among those infected by the same direct source. If X is Patient Zero, answer "None".
5. Transmission Lineage Query: Ask if patient U is in the upstream transmission lineage of patient V (including direct and indirect). Answer "Yes" or "No".
6. Outbreak Size Query: Ask for the total number of subsequent cases caused by patient X directly or indirectly (including X itself). Answer a positive integer.
7. Sibling Order Query: If patients A and B share the same direct source, ask if A was infected before B. If they share the same source, answer "Yes" or "No"; otherwise, answer "NotApplicable".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Direct Source Query (e.g., querying source of patient 5):
<query_parent>5</query_parent>

- Direct Infectee Count Query (e.g., querying infectees of patient 3):
<query_children_count>3</query_children_count>

- K-th Infectee Query (e.g., querying the 2nd infectee of patient 3):
<query_kth_child>3,2</query_kth_child>

- Position Query (e.g., querying rank of patient 5 among co-infectees):
<query_position>5</query_position>

- Transmission Lineage Query (e.g., querying if patient 1 is upstream of 5):
<query_ancestor>1,5</query_ancestor>

- Outbreak Size Query (e.g., querying total outbreak size from patient 3):
<query_subtree_size>3</query_subtree_size>

- Sibling Order Query (e.g., querying order between co-infectees 2 and 3):
<query_sibling_order>2,3</query_sibling_order>

When submitting the final answer, provide the investigation sequence number (1-based positive integer) of target patient {target} in the traceback process:

<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个基于"课程知识图谱"的教学大纲推演游戏，规则如下：

某学科构建了一套固定但未知的树形知识体系图谱，节点总数为 {n}。每个节点代表一个独立的知识点（用唯一的整数编号标识）。学科的"基础导论"（根节点）为 {root}，目标被讲授的知识点为 {target}。基于每个前置知识衍生出的下级重点，按大纲编排的顺序从 1 开始固定排列。

课程讲解规则采用深度优先的教学展开原则：讲师讲授完一个主干基础知识后，会按大纲编排顺序，顺着某一分支将其衍生出的全部进阶内容讲透，才会讲授该主干的下一个同级衍生分支。

你的目标是通过询问问题，确定目标知识点 {target} 在整门学科大纲里的绝对讲授节次（从 1 开始）。

你可以反复向我提出以下七类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 直接前置基础查询：询问知识点 X 的直接前置先修知识点标识。若 X 是基础导论，回答"无"。
2. 衍生知识点数量查询：询问以知识点 X 为直接基础的衍生知识点数量。回答一个非负整数。
3. 第 k 个衍生点查询：询问知识点 X 衍生出的第 k 个下级知识点标识。若 k 越界，回答"不存在"。
4. 基础衍生序位查询：询问知识点 X 在其直接前置知识的所有同级衍生点中的大纲排位（从 1 开始）。若 X 是基础导论，回答"无"。
5. 知识体系依赖查询：询问知识点 U 是否为知识点 V 的底层依赖（包含直接及间接先修）。回答"是"或"否"。
6. 知识分支规模查询：询问以知识点 X 为起点的整条垂直知识体系分支包含的节点总数（含 X 自身）。回答一个正整数。
7. 同基础讲解先后查询：若知识点 A 和 B 基于同一个直接前置知识衍生，询问大纲中 A 是否先于 B 讲授。若是，回答"是"或"否"；若不是同基础，回答"不适用"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 直接前置基础查询（例如查询知识点 5 的先修点）：
<query_parent>5</query_parent>

- 衍生知识点数量查询（例如查询知识点 3 衍生的数量）：
<query_children_count>3</query_children_count>

- 第 k 个衍生点查询（例如查询知识点 3 衍生的第 2 个知识点）：
<query_kth_child>3,2</query_kth_child>

- 基础衍生序位查询（例如查询知识点 5 在其同级衍生中的排位）：
<query_position>5</query_position>

- 知识体系依赖查询（例如查询知识点 1 是否为 5 的底层依赖）：
<query_ancestor>1,5</query_ancestor>

- 知识分支规模查询（例如查询以知识点 3 为起点的分支总数）：
<query_subtree_size>3</query_subtree_size>

- 同基础讲解先后查询（例如查询同基础的知识点 2 和 3 的先后）：
<query_sibling_order>2,3</query_sibling_order>

提交最终答案时，请提供目标知识点 {target} 在整个学科讲解过程中的讲授节次（从 1 开始的正整数）：

<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Course Knowledge Graph" reasoning game. Here are the rules:

A subject has a fixed but unknown tree-structured knowledge graph with {n} nodes in total. Each node represents an independent knowledge point (with a unique integer ID). The "Subject Foundation" (root node) is {root}, and the target knowledge point to be taught is {target}. The subordinate derivative points based on each prerequisite are arranged in a fixed syllabus order starting from 1.

The curriculum delivery follows a depth-first expansion principle: after teaching a foundational point, the instructor will thoroughly teach all advanced content derived along one branch in syllabus order before moving to the next sibling derivative branch.

Your goal is to determine the absolute teaching sequence number (1-based) of the target knowledge point {target} in the entire subject's syllabus by asking questions.

You can repeatedly ask me the following seven types of questions (one per turn), and I will answer truthfully based on the true structure:

1. Direct Prerequisite Query: Ask for the direct prerequisite knowledge point ID of point X. If X is the Foundation, answer "None".
2. Derivative Count Query: Ask for the number of direct derivative knowledge points of point X. Answer a non-negative integer.
3. K-th Derivative Query: Ask for the k-th derivative knowledge point ID of point X. If k is out of bounds, answer "NotExist".
4. Position Query: Ask for the syllabus rank (1-based) of point X among the derivatives of its direct prerequisite. If X is the Foundation, answer "None".
5. Dependency Query: Ask if point U is a foundational dependency of point V (including direct and indirect prerequisites). Answer "Yes" or "No".
6. Branch Size Query: Ask for the total number of knowledge points in the vertical branch starting from point X (including X itself). Answer a positive integer.
7. Sibling Order Query: If points A and B share the same direct prerequisite, ask if A is taught before B in the syllabus. If they share the same prerequisite, answer "Yes" or "No"; otherwise, answer "NotApplicable".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Direct Prerequisite Query (e.g., querying prerequisite of point 5):
<query_parent>5</query_parent>

- Derivative Count Query (e.g., querying derivative count of point 3):
<query_children_count>3</query_children_count>

- K-th Derivative Query (e.g., querying the 2nd derivative of point 3):
<query_kth_child>3,2</query_kth_child>

- Position Query (e.g., querying syllabus rank of point 5):
<query_position>5</query_position>

- Dependency Query (e.g., querying if point 1 is a dependency of 5):
<query_ancestor>1,5</query_ancestor>

- Branch Size Query (e.g., querying total points in branch starting from 3):
<query_subtree_size>3</query_subtree_size>

- Sibling Order Query (e.g., querying teaching order between siblings 2 and 3):
<query_sibling_order>2,3</query_sibling_order>

When submitting the final answer, provide the teaching sequence number (1-based positive integer) of target knowledge point {target} in the syllabus:

<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个基于"复杂机械 BOM 拆解"的工业装配推演游戏，规则如下：

工业系统导入了一份固定但未知结构的树形物料清单（BOM），节点总数为 {n}。每个节点代表一个组件或基础零件（用唯一的整数编号标识）。设备的"最终总成部件"（根节点）为 {root}，目标需单独剥离分析的零件为 {target}。每个组件直接包含的下一级部件按工序规定的顺序从 1 开始固定排列。

设备拆解采用自顶向下的深度拆解工序：工程师拆开一个组件后，会按规定的工序顺序，将其某一分支包含的所有下级零件全部拆解到底，才会去拆解该组件的下一个同级部件。

你的目标是通过询问问题，确定目标零件 {target} 在整套标准工序中是绝对第几个被拆解分离下来的（序号从 1 开始）。

你可以反复向我提出以下七类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 所属上级组件查询：询问零件 X 直接隶属的上一级装配组件标识。若 X 是最终总成，回答"无"。
2. 直属下级部件数量查询：询问组件 X 直接包含的下一级部件数量。回答一个非负整数。
3. 第 k 个下级部件查询：询问组件 X 按工序拆解出的第 k 个直接下级部件标识。若 k 越界，回答"不存在"。
4. 拆解序位查询：询问部件 X 在其直属上级包含的所有部件中的拆解顺位（从 1 开始）。若 X 是最终总成，回答"无"。
5. 装配层级关系查询：询问部件 U 是否处于部件 V 的装配结构上层（即直接或间接包含 V）。回答"是"或"否"。
6. 总成部件规模查询：询问以组件 X 为顶点的整个局部 BOM 结构包含的零件总数（含 X 自身）。回答一个正整数。
7. 同组件拆解先后查询：若部件 A 和 B 隶属于同一个直接上级组件，询问 A 的工序是否先于 B 拆解。若是同属一组件，回答"是"或"否"；若不是，回答"不适用"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 所属上级组件查询（例如查询零件 5 的上级组件）：
<query_parent>5</query_parent>

- 直属下级部件数量查询（例如查询组件 3 包含的下级数量）：
<query_children_count>3</query_children_count>

- 第 k 个下级部件查询（例如查询组件 3 的第 2 个下级部件）：
<query_kth_child>3,2</query_kth_child>

- 拆解序位查询（例如查询部件 5 在同属组件中的拆解顺位）：
<query_position>5</query_position>

- 装配层级关系查询（例如查询部件 1 是否为部件 5 的上层总成）：
<query_ancestor>1,5</query_ancestor>

- 总成部件规模查询（例如查询以组件 3 为顶点的部件规模）：
<query_subtree_size>3</query_subtree_size>

- 同组件拆解先后查询（例如查询同组件的部件 2 和 3 的先后）：
<query_sibling_order>2,3</query_sibling_order>

提交最终答案时，请提供目标零件 {target} 在全部拆解工序中的拆解序号（从 1 开始的正整数）：

<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play a "Complex Machinery BOM Disassembly" reasoning game. Here are the rules:

The system has imported a fixed but unknown tree-structured Bill of Materials (BOM) with {n} nodes in total. Each node represents an assembly or a basic part (with a unique integer ID). The "Final Assembly" (root node) is {root}, and the target part to be isolated is {target}. Each assembly's direct sub-components are arranged in a fixed procedural order starting from 1.

The disassembly process follows a top-down, depth-first procedural rule: after opening an assembly, the engineer will completely disassemble all sub-parts along one branch in procedural order before moving to the assembly's next sibling component.

Your goal is to determine the absolute disassembly sequence number (1-based) of the target part {target} in the entire standard process by asking questions.

You can repeatedly ask me the following seven types of questions (one per turn), and I will answer truthfully based on the true structure:

1. Direct Parent Assembly Query: Ask for the direct parent assembly ID of part X. If X is the Final Assembly, answer "None".
2. Sub-component Count Query: Ask for the number of direct sub-components of assembly X. Answer a non-negative integer.
3. K-th Sub-component Query: Ask for the k-th direct sub-component ID of assembly X. If k is out of bounds, answer "NotExist".
4. Position Query: Ask for the procedural rank (1-based) of part X among the sub-components of its direct parent. If X is the Final Assembly, answer "None".
5. Assembly Hierarchy Query: Ask if component U is in the upper assembly hierarchy of component V (i.e., contains V directly or indirectly). Answer "Yes" or "No".
6. Assembly Size Query: Ask for the total number of parts in the partial BOM structure starting from assembly X (including X itself). Answer a positive integer.
7. Sibling Order Query: If parts A and B belong to the same direct parent assembly, ask if A is disassembled before B. If they belong to the same parent, answer "Yes" or "No"; otherwise, answer "NotApplicable".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Direct Parent Assembly Query (e.g., querying parent of part 5):
<query_parent>5</query_parent>

- Sub-component Count Query (e.g., querying sub-components of assembly 3):
<query_children_count>3</query_children_count>

- K-th Sub-component Query (e.g., querying the 2nd sub-component of assembly 3):
<query_kth_child>3,2</query_kth_child>

- Position Query (e.g., querying disassembly rank of part 5):
<query_position>5</query_position>

- Assembly Hierarchy Query (e.g., querying if part 1 is an upper assembly of 5):
<query_ancestor>1,5</query_ancestor>

- Assembly Size Query (e.g., querying total BOM size under assembly 3):
<query_subtree_size>3</query_subtree_size>

- Sibling Order Query (e.g., querying order between co-components 2 and 3):
<query_sibling_order>2,3</query_sibling_order>

When submitting the final answer, provide the disassembly sequence number (1-based positive integer) of target part {target} in the standard process:

<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个基于"企业股权穿透"的审计推演游戏，规则如下：

风控系统映射出了一家资本系固定但未知结构的树形控股网络，公司总数为 {n}。每个节点代表一家企业（用唯一的整数编号标识）。该体系的"最终控股母公司"（根节点）为 {root}，目标被重点查账的子公司为 {target}。每家母公司直接控股的子公司按持股比例及注册顺序等法定维度从 1 开始固定排位。

审计流程采用深度优先的股权穿透原则：审计组在清查一家企业后，会按规定的子公司排位顺次往下，将某一持股分支到底层壳公司全部查验完毕，才会去核查该企业的下一家同级子公司。

你的目标是通过询问问题，确定目标企业 {target} 在这场全集团穿透审计中的绝对清查序号（从 1 开始）。

你可以反复向我提出以下七类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 直接控股母公司查询：询问企业 X 的直接控股母公司标识。若 X 是最终母公司，回答"无"。
2. 直属子公司数量查询：询问企业 X 直接控股的下属公司数量。回答一个非负整数。
3. 第 k 家子公司查询：询问企业 X 控股排位第 k 的直属子公司标识。若 k 越界，回答"不存在"。
4. 母公司内的审计序位查询：询问企业 X 在其直接控股母公司名下的清查顺位（从 1 开始）。若 X 是最终母公司，回答"无"。
5. 控股层级关系查询：询问企业 U 是否为企业 V 的控股方（包含直接和间接多层级控股）。回答"是"或"否"。
6. 资本系总规模查询：询问以企业 X 为顶点的整个附属资本系（含 X 自身及所有层级子公司）的企业总数。回答一个正整数。
7. 同母系审计先后查询：若企业 A 和 B 同属一个直接控股母公司，询问 A 是否先于 B 接受审计。若是同母系，回答"是"或"否"；若不是，回答"不适用"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 直接控股母公司查询（例如查询企业 5 的母公司）：
<query_parent>5</query_parent>

- 直属子公司数量查询（例如查询企业 3 的子公司数量）：
<query_children_count>3</query_children_count>

- 第 k 家子公司查询（例如查询企业 3 的第 2 家子公司）：
<query_kth_child>3,2</query_kth_child>

- 母公司内的审计序位查询（例如查询企业 5 在其同系公司中的顺位）：
<query_position>5</query_position>

- 控股层级关系查询（例如查询企业 1 是否为企业 5 的控股方）：
<query_ancestor>1,5</query_ancestor>

- 资本系总规模查询（例如查询以企业 3 为顶点的资本系企业总数）：
<query_subtree_size>3</query_subtree_size>

- 同母系审计先后查询（例如查询同母系的企业 2 和 3 的清查先后）：
<query_sibling_order>2,3</query_sibling_order>

提交最终答案时，请提供目标企业 {target} 在穿透审计流程中的清查序号（从 1 开始的正整数）：

<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Corporate Equity Audit" reasoning game. Here are the rules:

The risk control system maps out a fixed but unknown tree-structured holding network with {n} companies in total. Each node represents a company (with a unique integer ID). The "Ultimate Parent Company" (root node) is {root}, and the target subsidiary to be deeply audited is {target}. Each parent company's direct subsidiaries are arranged in a fixed statutory order starting from 1.

The audit process follows a depth-first equity penetration principle: after auditing an enterprise, the audit team will thoroughly verify all subsidiaries along a single holding branch down to the bottom shell companies before checking the next sibling subsidiary.

Your goal is to determine the absolute audit sequence number (1-based) of the target enterprise {target} in the entire group's penetration audit by asking questions.

You can repeatedly ask me the following seven types of questions (one per turn), and I will answer truthfully based on the true structure:

1. Direct Parent Company Query: Ask for the direct parent company ID of enterprise X. If X is the Ultimate Parent, answer "None".
2. Subsidiary Count Query: Ask for the number of direct subsidiaries held by enterprise X. Answer a non-negative integer.
3. K-th Subsidiary Query: Ask for the k-th direct subsidiary ID of enterprise X. If k is out of bounds, answer "NotExist".
4. Position Query: Ask for the audit rank (1-based) of enterprise X among its direct parent's subsidiaries. If X is the Ultimate Parent, answer "None".
5. Holding Hierarchy Query: Ask if enterprise U is a holding entity of enterprise V (including direct and indirect multi-level holding). Answer "Yes" or "No".
6. Capital System Size Query: Ask for the total number of companies in the affiliated capital system starting from enterprise X (including X itself). Answer a positive integer.
7. Sibling Order Query: If enterprises A and B share the same direct parent company, ask if A is audited before B. If they share the same parent, answer "Yes" or "No"; otherwise, answer "NotApplicable".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Direct Parent Company Query (e.g., querying parent of enterprise 5):
<query_parent>5</query_parent>

- Subsidiary Count Query (e.g., querying subsidiaries of enterprise 3):
<query_children_count>3</query_children_count>

- K-th Subsidiary Query (e.g., querying the 2nd subsidiary of enterprise 3):
<query_kth_child>3,2</query_kth_child>

- Position Query (e.g., querying audit rank of enterprise 5):
<query_position>5</query_position>

- Holding Hierarchy Query (e.g., querying if enterprise 1 holds 5):
<query_ancestor>1,5</query_ancestor>

- Capital System Size Query (e.g., querying total system size of enterprise 3):
<query_subtree_size>3</query_subtree_size>

- Sibling Order Query (e.g., querying audit order between siblings 2 and 3):
<query_sibling_order>2,3</query_sibling_order>

When submitting the final answer, provide the audit sequence number (1-based positive integer) of target enterprise {target} in the penetration audit process:

<answer>5</answer>
"""

    tags = ["answer", "query_parent", "query_children_count", "query_kth_child", 
            "query_position", "query_ancestor", "query_subtree_size", "query_sibling_order"]

    reasoning_type = "演绎推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5, "root": 1, "target": 4,
                "tree": {
                    1: {"parent": None, "children": [2, 3]},
                    2: {"parent": 1, "children": [4, 5]},
                    3: {"parent": 1, "children": []},
                    4: {"parent": 2, "children": []},
                    5: {"parent": 2, "children": []},
                },
                "answer": 3,
            },
            2: {
                "n": 8, "root": 1, "target": 6,
                "tree": {
                    1: {"parent": None, "children": [2, 3, 4]},
                    2: {"parent": 1, "children": [5]},
                    3: {"parent": 1, "children": [6, 7]},
                    4: {"parent": 1, "children": [8]},
                    5: {"parent": 2, "children": []},
                    6: {"parent": 3, "children": []},
                    7: {"parent": 3, "children": []},
                    8: {"parent": 4, "children": []},
                },
                "answer": 5,
            },
            3: {
                "n": 10, "root": 1, "target": 9,
                "tree": {
                    1: {"parent": None, "children": [2, 3]},
                    2: {"parent": 1, "children": [4, 5, 6]},
                    3: {"parent": 1, "children": [7, 8]},
                    4: {"parent": 2, "children": []},
                    5: {"parent": 2, "children": [9, 10]},
                    6: {"parent": 2, "children": []},
                    7: {"parent": 3, "children": []},
                    8: {"parent": 3, "children": []},
                    9: {"parent": 5, "children": []},
                    10: {"parent": 5, "children": []},
                },
                "answer": 5,
            },
            4: {
                "n": 13, "root": 1, "target": 11,
                "tree": {
                    1: {"parent": None, "children": [2, 3, 4]},
                    2: {"parent": 1, "children": [5, 6]},
                    3: {"parent": 1, "children": [7, 8, 9]},
                    4: {"parent": 1, "children": [10, 11]},
                    5: {"parent": 2, "children": []},
                    6: {"parent": 2, "children": [12, 13]},
                    7: {"parent": 3, "children": []},
                    8: {"parent": 3, "children": []},
                    9: {"parent": 3, "children": []},
                    10: {"parent": 4, "children": []},
                    11: {"parent": 4, "children": []},
                    12: {"parent": 6, "children": []},
                    13: {"parent": 6, "children": []},
                },
                "answer": 13,
            },
            5: {
                "n": 17, "root": 1, "target": 15,
                "tree": {
                    1: {"parent": None, "children": [2, 3]},
                    2: {"parent": 1, "children": [4, 5, 6]},
                    3: {"parent": 1, "children": [7, 8]},
                    4: {"parent": 2, "children": [9, 10]},
                    5: {"parent": 2, "children": [11, 12]},
                    6: {"parent": 2, "children": [13, 14]},
                    7: {"parent": 3, "children": []},
                    8: {"parent": 3, "children": [15, 16, 17]},
                    9: {"parent": 4, "children": []},
                    10: {"parent": 4, "children": []},
                    11: {"parent": 5, "children": []},
                    12: {"parent": 5, "children": []},
                    13: {"parent": 6, "children": []},
                    14: {"parent": 6, "children": []},
                    15: {"parent": 8, "children": []},
                    16: {"parent": 8, "children": []},
                    17: {"parent": 8, "children": []},
                },
                "answer": 15,
            },
        },
        "en": {
            1: {
                "n": 5, "root": 1, "target": 4,
                "tree": {
                    1: {"parent": None, "children": [2, 3]},
                    2: {"parent": 1, "children": [4, 5]},
                    3: {"parent": 1, "children": []},
                    4: {"parent": 2, "children": []},
                    5: {"parent": 2, "children": []},
                },
                "answer": 3,
            },
            2: {
                "n": 8, "root": 1, "target": 6,
                "tree": {
                    1: {"parent": None, "children": [2, 3, 4]},
                    2: {"parent": 1, "children": [5]},
                    3: {"parent": 1, "children": [6, 7]},
                    4: {"parent": 1, "children": [8]},
                    5: {"parent": 2, "children": []},
                    6: {"parent": 3, "children": []},
                    7: {"parent": 3, "children": []},
                    8: {"parent": 4, "children": []},
                },
                "answer": 5,
            },
            3: {
                "n": 10, "root": 1, "target": 9,
                "tree": {
                    1: {"parent": None, "children": [2, 3]},
                    2: {"parent": 1, "children": [4, 5, 6]},
                    3: {"parent": 1, "children": [7, 8]},
                    4: {"parent": 2, "children": []},
                    5: {"parent": 2, "children": [9, 10]},
                    6: {"parent": 2, "children": []},
                    7: {"parent": 3, "children": []},
                    8: {"parent": 3, "children": []},
                    9: {"parent": 5, "children": []},
                    10: {"parent": 5, "children": []},
                },
                "answer": 5,
            },
            4: {
                "n": 13, "root": 1, "target": 11,
                "tree": {
                    1: {"parent": None, "children": [2, 3, 4]},
                    2: {"parent": 1, "children": [5, 6]},
                    3: {"parent": 1, "children": [7, 8, 9]},
                    4: {"parent": 1, "children": [10, 11]},
                    5: {"parent": 2, "children": []},
                    6: {"parent": 2, "children": [12, 13]},
                    7: {"parent": 3, "children": []},
                    8: {"parent": 3, "children": []},
                    9: {"parent": 3, "children": []},
                    10: {"parent": 4, "children": []},
                    11: {"parent": 4, "children": []},
                    12: {"parent": 6, "children": []},
                    13: {"parent": 6, "children": []},
                },
                "answer": 13,
            },
            5: {
                "n": 17, "root": 1, "target": 15,
                "tree": {
                    1: {"parent": None, "children": [2, 3]},
                    2: {"parent": 1, "children": [4, 5, 6]},
                    3: {"parent": 1, "children": [7, 8]},
                    4: {"parent": 2, "children": [9, 10]},
                    5: {"parent": 2, "children": [11, 12]},
                    6: {"parent": 2, "children": [13, 14]},
                    7: {"parent": 3, "children": []},
                    8: {"parent": 3, "children": [15, 16, 17]},
                    9: {"parent": 4, "children": []},
                    10: {"parent": 4, "children": []},
                    11: {"parent": 5, "children": []},
                    12: {"parent": 5, "children": []},
                    13: {"parent": 6, "children": []},
                    14: {"parent": 6, "children": []},
                    15: {"parent": 8, "children": []},
                    16: {"parent": 8, "children": []},
                    17: {"parent": 8, "children": []},
                },
                "answer": 15,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self._game_info["target"] = cfg["target"]
        
        self.tree = cfg["tree"]
        self.correct_answer = cfg["answer"]
        
        self._compute_subtree_sizes()

    def _compute_subtree_sizes(self):
        self.subtree_sizes = {}
        
        def compute_size(node_id):
            if node_id in self.subtree_sizes:
                return self.subtree_sizes[node_id]
            
            size = 1
            children = self.tree[node_id]["children"]
            for child in children:
                size += compute_size(child)
            
            self.subtree_sizes[node_id] = size
            return size
        
        for node_id in self.tree:
            compute_size(node_id)

    def evaluate(self, parsed_info):
        try:
            answer_str = parsed_info["answer"].strip()
            answer = int(answer_str)
            return answer == self.correct_answer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            none_res, not_exist_res, not_applicable_res = "无", "不存在", "不适用"
            error_msg = "错误：节点不存在或查询格式错误。"
        else:
            yes_res, no_res = "Yes", "No"
            none_res, not_exist_res, not_applicable_res = "None", "NotExist", "NotApplicable"
            error_msg = "Error: Node does not exist or query format is invalid."

        try:
            if "query_parent" in parsed_info:
                node_id = int(parsed_info["query_parent"].strip())
                if node_id not in self.tree:
                    return error_msg
                parent = self.tree[node_id]["parent"]
                return none_res if parent is None else str(parent)

            elif "query_children_count" in parsed_info:
                node_id = int(parsed_info["query_children_count"].strip())
                if node_id not in self.tree:
                    return error_msg
                return str(len(self.tree[node_id]["children"]))

            elif "query_kth_child" in parsed_info:
                parts = [x.strip() for x in parsed_info["query_kth_child"].split(",")]
                node_id, k = int(parts[0]), int(parts[1])
                if node_id not in self.tree:
                    return error_msg
                children = self.tree[node_id]["children"]
                if k < 1 or k > len(children):
                    return not_exist_res
                return str(children[k - 1])

            elif "query_position" in parsed_info:
                node_id = int(parsed_info["query_position"].strip())
                if node_id not in self.tree:
                    return error_msg
                parent = self.tree[node_id]["parent"]
                if parent is None:
                    return none_res
                children = self.tree[parent]["children"]
                position = children.index(node_id) + 1
                return str(position)

            elif "query_ancestor" in parsed_info:
                parts = [x.strip() for x in parsed_info["query_ancestor"].split(",")]
                u, v = int(parts[0]), int(parts[1])
                if u not in self.tree or v not in self.tree:
                    return error_msg
                current = self.tree[v]["parent"]
                while current is not None:
                    if current == u:
                        return yes_res
                    current = self.tree[current]["parent"]
                return no_res

            elif "query_subtree_size" in parsed_info:
                node_id = int(parsed_info["query_subtree_size"].strip())
                if node_id not in self.tree:
                    return error_msg
                return str(self.subtree_sizes[node_id])

            elif "query_sibling_order" in parsed_info:
                parts = [x.strip() for x in parsed_info["query_sibling_order"].split(",")]
                a, b = int(parts[0]), int(parts[1])
                if a not in self.tree or b not in self.tree:
                    return error_msg
                parent_a = self.tree[a]["parent"]
                parent_b = self.tree[b]["parent"]
                if parent_a is None or parent_b is None or parent_a != parent_b:
                    return not_applicable_res
                children = self.tree[parent_a]["children"]
                pos_a = children.index(a)
                pos_b = children.index(b)
                return yes_res if pos_a < pos_b else no_res

            else:
                raise ValueError("No valid query tag found.")

        except Exception as e:
            return error_msg

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass
        
        if correct == "是": return "否"
        if correct == "否": return "是"
        if correct == "无": return "1"
        if correct == "不存在": return "1"
        if correct == "不适用": return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
        if lower_correct == "none":
            return "1"
        if lower_correct == "notexist":
            return "1"
        if lower_correct == "notapplicable":
            return "Yes" if self.config.language == "en" else "是"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        queries = []
        nodes = sorted(self.tree.keys())
        
        def add_query(tag, content):
            parsed_info = {tag: str(content)}
            answer = self._cf_core_produce(parsed_info)
            query_str = f"<{tag}>{content}</{tag}>"
            queries.append({"query": query_str, "answer": answer})

        for node_id in nodes:
            add_query("query_parent", node_id)

        for node_id in nodes:
            add_query("query_children_count", node_id)

        for node_id in nodes:
            child_count = len(self.tree[node_id]["children"])
            for k in range(1, child_count + 1):
                add_query("query_kth_child", f"{node_id},{k}")

        for node_id in nodes:
            add_query("query_position", node_id)

        target = self._game_info["target"]
        for u in nodes:
            add_query("query_ancestor", f"{u},{target}")

        for node_id in nodes:
            add_query("query_subtree_size", node_id)

        for node_id in nodes:
            children = self.tree[node_id]["children"]
            for i in range(len(children)):
                for j in range(i + 1, len(children)):
                    add_query("query_sibling_order", f"{children[i]},{children[j]}")

        return queries