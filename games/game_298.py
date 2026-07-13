# -*- coding: utf-8 -*-
# 自动生成 | 场景化改造
# 推理类型: 溯因推理
# 数据结构: 树
# ============================================================

from .base import Game
from collections import defaultdict, deque

class TreeIsomorphismGame(Game):

    game_rule_zh = """\
您正在参与一个树结构等价关系推理任务。

系统中存在一棵包含 {n} 个节点的有序树（编号 1 至 {n}，节点 1 为根）。每个节点的子节点有严格的排列顺序。

系统秘密选择了一种"等价关系"R，属于以下四种之一：
1. 规则 A（严格有序同构）：两棵子树结构完全相同，且每个节点处子节点的排列顺序完全一致。
2. 规则 B（逐级整体反转）：结构相同，但在任何节点处，允许将所有子节点的顺序整体反转后匹配；各节点独立决定是否反转。
3. 规则 C（无序同构）：结构相同，但忽略子节点的排列顺序，将子节点视为多重集合进行递归匹配。
4. 规则 D（压缩后无序同构）：先压缩子树（反复移除"非根且仅有单一子节点"的节点），再按规则C比较。

您的任务是通过查询推理出等价关系R是哪一种，并对新的节点对做出正确预测。

可用操作：
1. 比较查询：询问节点 u 和 v 的子树在关系 R 下是否等价。
   - 格式：<query_compare>u,v</query_compare>
   - 返回：是 或 否

2. 提交等价关系：声明你认为的等价关系类型。
   - 格式：<claim>X</claim>（X 是 A、B、C 或 D）
   - 必须先进行至少 2 次有效比较查询。
   - 返回：正确 或 错误（错误则任务失败）

3. 预测查询：在成功提交后，对未比较过的节点对预测。
   - 格式：<query_predict>u,v,answer</query_predict>（answer 是"是"或"否"）
   - 返回：命中 或 未命中

成功条件：至少 2 次比较查询；正确提交关系；预测正确。
失败条件：不满 2 次查询即提交；关系错误；预测错误。

注意：每次回复中请只使用一种操作标签。
"""

    game_rule_en = """\
You are participating in a tree structure equivalence relation reasoning task.

The system has a rooted ordered tree with {n} nodes (numbered 1 to {n}, node 1 is the root). Children of each node have a strict ordering.

The system has secretly chosen an "equivalence relation" R from the following four:
1. Rule A (Strict Ordered Isomorphism): Two subtrees are structurally identical with matching child orderings at every node.
2. Rule B (Layer-wise Reversible): Same structure, but at any node the entire child sequence may be reversed before matching; each node independently decides.
3. Rule C (Unordered Isomorphism): Same structure, ignoring child ordering, treating children as multisets for recursive matching.
4. Rule D (Compressed Unordered Isomorphism): First compress the subtree (repeatedly remove non-root nodes with exactly one child), then compare using Rule C.

Your task is to deduce relation R through queries and make a correct prediction on a new pair of nodes.

Available operations:
1. Comparison Query: Ask if the subtrees rooted at nodes u and v are equivalent under R.
   - Format: <query_compare>u,v</query_compare>
   - Returns: Yes or No

2. Claim Relation: Declare the equivalence relation type.
   - Format: <claim>X</claim> (X is A, B, C, or D)
   - You must perform at least 2 comparison queries first.
   - Returns: Correct or Wrong (wrong ends the task in failure)

3. Prediction Query: After a successful claim, predict for an uncompared pair.
   - Format: <query_predict>u,v,answer</query_predict> (answer is "Yes" or "No")
   - Returns: Hit or Miss

Success: At least 2 comparison queries; correct claim; correct prediction.
Failure: Claiming before 2 queries; incorrect relation; incorrect prediction.

Note: Please use only one operation tag per response.
"""

    contextualized_rule_zh_1 = """\
您已接入『交通线网拓扑等价关系分析系统』。

系统载入了一个包含 {n} 个枢纽节点的定向分发线网结构（编号 1 至 {n}，其中节点 1 为主干枢纽）。每个节点的下游分支都存在严格的物理排序。

目前系统在评估两套局部线网时，秘密采用了一种"等价通行关系"R，它属于以下四种之一：
1. 规则 A（严格有序同构）：两个线网结构完全相同，且每个枢纽处的下游分支排列顺序完全一致。
2. 规则 B（逐级整体镜像）：结构相同，在任何枢纽节点处，允许将下游所有分支顺序进行整体镜像反转后匹配；各节点独立决定是否反转。
3. 规则 C（无序同构）：结构相同，但忽略下游分支的物理排列顺序，仅将下游线网视为集合进行递归连通性匹配。
4. 规则 D（压缩后无序同构）：先精简线网（反复移除"非当前线网起点且仅有单一出向分支"的直行过境节点），随后按规则C比较精简后的拓扑结构。

您的任务是通过探测与推理，排查出当前采用的等价关系 R 是哪一种，并对一对新的线网进行等价预测。

您可以进行以下操作：
1. 比较查询（Compare）：询问枢纽 u 和 v 统领的下游线网在关系 R 下是否等价。
   - 格式：<query_compare>u,v</query_compare>
   - 返回：是 或 否

2. 提交等价关系（Claim）：当你收集了足够信息后，声明你认为的等价关系类型。
   - 格式：<claim>X</claim>（其中 X 是 A、B、C 或 D）
   - 注意：你必须先进行至少 2 次有效的比较查询后，才能提交声明。
   - 返回：正确 或 错误（若错误，任务立即失败）

3. 预测查询（Predict）：在成功提交等价关系后，对一对此前未比较过的节点进行预测。
   - 格式：<query_predict>u,v,answer</query_predict>（其中 answer 是"是"或"否"）
   - 返回：命中 或 未命中

成功条件：至少 2 次有效比较查询；正确提交关系类型；预测查询正确。
失败条件：未满 2 次查询即提交；关系类型错误；预测答案错误。
请尽可能少地使用查询次数来完成任务。

注意：每次回复中请只使用一种操作标签（query_compare、claim 或 query_predict 中的一个），不要同时使用多个标签。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
You have accessed the "Traffic Network Topology Equivalence Analysis System".

The system has loaded a directional distribution network containing {n} hub nodes (numbered 1 to {n}, with node 1 as the primary hub). The downstream branches of each node have a strict physical ordering.

Currently, when evaluating local networks, the system secretly applies an "Equivalence Routing Relation" R, chosen from the following four:
1. Rule A (Strict Ordered Isomorphism): Two network structures are identical, and the arrangement order of downstream branches at each hub matches exactly.
2. Rule B (Layer-wise Reversible): Same structure, but at any hub node, the downstream branch sequence may be entirely reversed (mirrored) before matching; each node independently decides whether to reverse.
3. Rule C (Unordered Isomorphism): Same structure, but ignoring the physical order of downstream branches, treating them as multisets for recursive connectivity matching.
4. Rule D (Compressed Unordered Isomorphism): First streamline the network (repeatedly remove straight-through transit nodes that are "not the starting hub and have only 1 downstream branch"), then compare the streamlined topologies using Rule C.

Your task is to deduce which equivalence relation R is active through probing, and then make a correct equivalence prediction for a new pair of networks.

Available operations:
1. Comparison Query (Compare): Ask if the downstream networks of hubs u and v are equivalent under relation R.
   - Format: <query_compare>u,v</query_compare>
   - Returns: Yes or No

2. Claim Equivalence Relation (Claim): Declare which equivalence relation type you believe is correct.
   - Format: <claim>X</claim> (where X is A, B, C, or D)
   - Note: You must perform at least 2 valid comparison queries before making a claim.
   - Returns: Correct or Wrong (if wrong, the task ends in failure)

3. Prediction Query (Predict): After successfully claiming the relation, make a prediction on a previously uncompared pair of hubs.
   - Format: <query_predict>u,v,answer</query_predict> (where answer is "Yes" or "No")
   - Returns: Hit or Miss

Success conditions: At least 2 valid comparison queries; correct relation claimed; correct prediction.
Failure conditions: Claiming before 2 queries; incorrect relation; incorrect prediction.
Try to complete the task with minimal queries.

Note: Please use only one operation tag per response (one of query_compare, claim, or query_predict). Do not use multiple tags simultaneously.
"""

    contextualized_rule_zh_2 = """\
欢迎使用『医疗临床诊疗路径等价性分析系统』。

系统中定义了一套包含 {n} 个诊疗阶段的标准路径树（节点编号 1 到 {n}，其中节点 1 为初始确诊节点）。每个阶段的后续备选治疗方案有着严格的优先级排序。

为了比对不同医院的临床路径，系统内置了一种隐藏的"等价诊疗关系"R，从以下四种中选取：
1. 方案 A（严格有序同构）：两套路径结构完全一致，且每个阶段的备选治疗方案优先级顺序完全对应。
2. 方案 B（逐级整体反转）：结构一致，但在任何诊疗节点处，允许将所有备选治疗方案的优先级顺序完全颠倒后进行匹配；各节点独立决定。
3. 方案 C（无序同构）：结构一致，但不考虑治疗方案的优先级，仅将备选方案视为集合进行递归匹配。
4. 方案 D（压缩后无序同构）：先对临床路径进行压缩（反复移除"非起始点且仅有单一后续观察步骤"的冗余节点），随后按方案C比较压缩后的路径。

您的目标是通过比对查询，推理出系统当前使用的等价关系 R，并在一对新的临床路径上做出准确预测。

您可以进行以下操作：
1. 比较查询（Compare）：询问节点 u 和 v 代表的诊疗子路径在关系 R 下是否等价。
   - 格式：<query_compare>u,v</query_compare>
   - 返回：是 或 否

2. 提交等价关系（Claim）：当你收集了足够信息后，声明你认为的等价关系类型。
   - 格式：<claim>X</claim>（其中 X 是 A、B、C 或 D）
   - 注意：你必须先进行至少 2 次有效的比较查询后，才能提交声明。
   - 返回：正确 或 错误（若错误，任务立即失败）

3. 预测查询（Predict）：在成功提交等价关系后，对一对此前未比较过的节点进行预测。
   - 格式：<query_predict>u,v,answer</query_predict>（其中 answer 是"是"或"否"）
   - 返回：命中 或 未命中

成功条件：至少 2 次有效比较查询；正确提交关系类型；预测查询正确。
失败条件：未满 2 次查询即提交；关系类型错误；预测答案错误。
请尽可能少地使用查询次数来完成任务。

注意：每次回复中请只使用一种操作标签（query_compare、claim 或 query_predict 中的一个），不要同时使用多个标签。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Pathway Equivalence Analysis System".

The system defines a standard clinical pathway tree comprising {n} treatment stages (nodes numbered 1 to {n}, with node 1 as the initial diagnosis). The subsequent alternative treatments at each stage have a strict priority ranking.

To compare clinical pathways from different hospitals, the system secretly employs an "Equivalence Treatment Relation" R, selected from the following four:
1. Protocol A (Strict Ordered Isomorphism): The two pathway structures are identical, and the priority order of alternative treatments at each stage matches exactly.
2. Protocol B (Layer-wise Reversible): Same structure, but at any clinical node, the priority sequence of alternative treatments may be completely reversed before matching; each node independently decides.
3. Protocol C (Unordered Isomorphism): Same structure, but ignoring the priority of treatments, treating the alternatives as multisets for recursive matching.
4. Protocol D (Compressed Unordered Isomorphism): First compress the pathway (repeatedly remove redundant nodes that are "not the starting point and have only a single subsequent monitoring step"), then compare the compressed pathways using Protocol C.

Your objective is to deduce the active equivalence relation R through comparative queries and make an accurate prediction on a new pair of clinical pathways.

Available operations:
1. Comparison Query (Compare): Ask if the sub-pathways starting at nodes u and v are equivalent under relation R.
   - Format: <query_compare>u,v</query_compare>
   - Returns: Yes or No

2. Claim Equivalence Relation (Claim): Declare which equivalence relation type you believe is correct.
   - Format: <claim>X</claim> (where X is A, B, C, or D)
   - Note: You must perform at least 2 valid comparison queries before making a claim.
   - Returns: Correct or Wrong (if wrong, the task ends in failure)

3. Prediction Query (Predict): After successfully claiming the relation, make a prediction on a previously uncompared pair of nodes.
   - Format: <query_predict>u,v,answer</query_predict> (where answer is "Yes" or "No")
   - Returns: Hit or Miss

Success conditions: At least 2 valid comparison queries; correct relation claimed; correct prediction.
Failure conditions: Claiming before 2 queries; incorrect relation; incorrect prediction.
Try to complete the task with minimal queries.

Note: Please use only one operation tag per response (one of query_compare, claim, or query_predict). Do not use multiple tags simultaneously.
"""

    contextualized_rule_zh_3 = """\
欢迎来到『教育课程体系等价性评估平台』。

平台录入了一套由 {n} 个知识模块构成的课程大纲树（模块编号 1 到 {n}，其中 1 为基础前置导论）。每个模块的后续子课题授课顺序有着严格的编排。

为评估不同教学方案的等价性，平台后台设定了一种隐藏的"等价教学关系"R，它属于以下四种之一：
1. 模式 A（严格有序同构）：两个课程子体系结构相同，且每个模块下级子课题的授课顺序完全一致。
2. 模式 B（逐级整体倒序）：结构相同，在任何模块节点处，允许将下级所有子课题的授课顺序整体倒置后进行匹配；各模块独立决定。
3. 模式 C（无序同构）：结构相同，但忽略下级课题的授课先后顺序，仅视作知识点集合进行递归匹配。
4. 模式 D（压缩后无序同构）：先对体系进行精简（反复剔除"非当前子体系根节点且仅包含单一子课题"的过渡性模块），然后按模式C比较精简后的体系。

你的目标是通过探测与逻辑推理，识别出当前的等价关系 R 是哪一种，并对一对新的课程模块的等价性进行正确预测。

你可以进行以下操作：
1. 比较查询（Compare）：询问模块 u 和 v 的后续教学体系在关系 R 下是否等价。
   - 格式：<query_compare>u,v</query_compare>
   - 返回：是 或 否

2. 提交等价关系（Claim）：当你收集了足够信息后，声明你认为的等价关系类型。
   - 格式：<claim>X</claim>（其中 X 是 A、B、C 或 D）
   - 注意：你必须先进行至少 2 次有效的比较查询后，才能提交声明。
   - 返回：正确 或 错误（若错误，评估立即失败）

3. 预测查询（Predict）：在成功提交等价关系后，对一对此前未比较过的模块进行预测。
   - 格式：<query_predict>u,v,answer</query_predict>（其中 answer 是"是"或"否"）
   - 返回：命中 或 未命中

成功条件：至少 2 次有效比较查询；正确提交关系类型；预测查询正确。
失败条件：未满 2 次查询即提交；关系类型错误；预测答案错误。
请尽可能少地使用查询次数来完成任务。

注意：每次回复中请只使用一种操作标签（query_compare、claim 或 query_predict 中的一个），不要同时使用多个标签。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Curriculum System Equivalence Evaluation Platform".

The platform has recorded a syllabus tree consisting of {n} knowledge modules (numbered 1 to {n}, with module 1 as the fundamental prerequisite). The subsequent sub-topics of each module have a strict instructional order.

To evaluate the equivalence of different teaching schemes, the platform secretly applies a hidden "Equivalence Teaching Relation" R, chosen from one of the following four:
1. Mode A (Strict Ordered Isomorphism): The two curriculum sub-systems have identical structures, and the instructional order of subordinate sub-topics under each module matches exactly.
2. Mode B (Layer-wise Reversible): Same structure, but at any module node, the instructional sequence of all subordinate sub-topics may be entirely reversed before matching; each module independently decides.
3. Mode C (Unordered Isomorphism): Same structure, but ignoring the instructional order of subordinate topics, treating them as multisets of knowledge points for recursive matching.
4. Mode D (Compressed Unordered Isomorphism): First streamline the system (repeatedly remove transitional modules that are "not the current sub-system's root and contain only a single sub-topic"), then compare the streamlined systems using Mode C.

Your goal is to deduce the active equivalence relation R through probing and logical reasoning, and make a correct prediction regarding the equivalence of a new pair of curriculum modules.

Available operations:
1. Comparison Query (Compare): Ask if the subsequent teaching systems of modules u and v are equivalent under relation R.
   - Format: <query_compare>u,v</query_compare>
   - Returns: Yes or No

2. Claim Equivalence Relation (Claim): Declare which equivalence relation type you believe is correct.
   - Format: <claim>X</claim> (where X is A, B, C, or D)
   - Note: You must perform at least 2 valid comparison queries before making a claim.
   - Returns: Correct or Wrong (if wrong, the evaluation ends in failure)

3. Prediction Query (Predict): After successfully claiming the relation, make a prediction on a previously uncompared pair of modules.
   - Format: <query_predict>u,v,answer</query_predict> (where answer is "Yes" or "No")
   - Returns: Hit or Miss

Success conditions: At least 2 valid comparison queries; correct relation claimed; correct prediction.
Failure conditions: Claiming before 2 queries; incorrect relation; incorrect prediction.
Try to complete the task with minimal queries.

Note: Please use only one operation tag per response (one of query_compare, claim, or query_predict). Do not use multiple tags simultaneously.
"""

    contextualized_rule_zh_4 = """\
欢迎登录『智能制造生产线等价性核验系统』。

系统载入了一套包含 {n} 个加工工序节点的标准装配树（节点编号 1 到 {n}，其中节点 1 为总装起始节点）。每个工序的下游子工序排列有着严格的物理加工顺序。

目前系统在对比不同车间的生产线时，后台隐蔽地使用了一种“等价装配关系” R，它属于以下四种之一：
1. 模式 A（严格有序同构）：两条产线结构完全一致，且每个工序节点处的下游子工序排列顺序完全相同。
2. 模式 B（逐级整体镜像）：结构一致，但在任何工序节点处，允许将下游所有子工序的加工顺序进行整体镜像反转后匹配；各节点独立决定。
3. 模式 C（无序同构）：结构一致，但不考虑下游子工序的物理加工顺序，仅将其视为物料集合进行递归匹配。
4. 模式 D（压缩后无序同构）：先精简产线（反复移除“非起始节点且仅包含单一单向下游工序”的流转节点），随后按模式 C 比较精简后的拓扑结构。

您的任务是通过探测与推理，排查出当前采用的等价关系 R 是哪一种，并对一对新的装配子树进行等价预测。

您可以进行以下操作：
1. 比较查询（Compare）：询问工序 u 和 v 代表的下游产线在关系 R 下是否等价。
   - 格式：<query_compare>u,v</query_compare>
   - 返回：是 或 否

2. 提交等价关系（Claim）：当你收集了足够信息后，声明你认为的等价关系类型。
   - 格式：<claim>X</claim>（其中 X 是 A、B、C 或 D）
   - 注意：你必须先进行至少 2 次有效的比较查询后，才能提交声明。
   - 返回：正确 或 错误（若错误，核验立即失败）

3. 预测查询（Predict）：在成功提交等价关系后，对一对此前未比较过的节点进行预测。
   - 格式：<query_predict>u,v,answer</query_predict>（其中 answer 是"是"或"否"）
   - 返回：命中 或 未命中

成功条件：至少 2 次有效比较查询；正确提交关系类型；预测查询正确。
失败条件：未满 2 次查询即提交；关系类型错误；预测答案错误。
请尽可能少地使用查询次数来完成任务。

注意：每次回复中请只使用一种操作标签（query_compare、claim 或 query_predict 中的一个），不要同时使用多个标签。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Smart Manufacturing Assembly Line Equivalence Verification System".

The system has loaded a standard assembly tree comprising {n} processing nodes (numbered 1 to {n}, with node 1 as the primary assembly root). The downstream sub-processes of each node have a strict physical processing order.

Currently, when comparing production lines from different workshops, the system secretly employs an "Equivalence Assembly Relation" R, selected from the following four:
1. Mode A (Strict Ordered Isomorphism): The two assembly structures are identical, and the arrangement order of downstream sub-processes at each node matches exactly.
2. Mode B (Layer-wise Reversible): Same structure, but at any processing node, the sequence of downstream sub-processes may be entirely mirror-reversed before matching; each node independently decides.
3. Mode C (Unordered Isomorphism): Same structure, but ignoring the physical processing order of downstream sub-processes, treating them as multisets of materials for recursive matching.
4. Mode D (Compressed Unordered Isomorphism): First streamline the production line (repeatedly remove redundant transit nodes that are "not the starting root and have only a single downstream process"), then compare the streamlined topologies using Mode C.

Your task is to deduce the active equivalence relation R through probing and make an accurate equivalence prediction for a new pair of assembly sub-trees.

Available operations:
1. Comparison Query (Compare): Ask if the downstream assembly lines of processes u and v are equivalent under relation R.
   - Format: <query_compare>u,v</query_compare>
   - Returns: Yes or No

2. Claim Equivalence Relation (Claim): Declare which equivalence relation type you believe is correct.
   - Format: <claim>X</claim> (where X is A, B, C, or D)
   - Note: You must perform at least 2 valid comparison queries before making a claim.
   - Returns: Correct or Wrong (if wrong, the verification ends in failure)

3. Prediction Query (Predict): After successfully claiming the relation, make a prediction on a previously uncompared pair of nodes.
   - Format: <query_predict>u,v,answer</query_predict> (where answer is "Yes" or "No")
   - Returns: Hit or Miss

Success conditions: At least 2 valid comparison queries; correct relation claimed; correct prediction.
Failure conditions: Claiming before 2 queries; incorrect relation; incorrect prediction.
Try to complete the task with minimal queries.

Note: Please use only one operation tag per response (one of query_compare, claim, or query_predict). Do not use multiple tags simultaneously.
"""

    contextualized_rule_zh_5 = """\
您已登入『法律合同条款逻辑等价性审查系统』。

系统中导入了一套包含 {n} 个条款节点的标准合同逻辑树（编号 1 至 {n}，其中节点 1 为核心主旨条款）。每个条款的下级附属条款存在严格的文本宣读顺序。

为审查不同草案的等价性，系统在后台设定了一种隐藏的“等价法理关系” R，选自以下四种：
1. 规则 A（严格有序同构）：两份草案的逻辑结构完全一致，且每个条款下的附属条款排列顺序完全相同。
2. 规则 B（逐级整体反转）：结构一致，但在任何条款节点处，允许将所有下级附属条款的顺序进行整体倒叙反转后匹配；各条款独立决定。
3. 规则 C（无序同构）：结构一致，但忽略下级条款的宣读先后顺序，仅视作条款集合进行递归匹配。
4. 规则 D（压缩后无序同构）：先对草案进行精简（反复剔除“非核心主旨条款且仅包含单一附属条款”的过渡性格式条款），随后按规则 C 比较精简后的法理结构。

您的任务是通过对比探测，推理出系统当前使用的等价关系 R 是哪一种，并对一对新提取的合同条款分支做出准确预测。

您可以进行以下操作：
1. 比较查询（Compare）：询问条款 u 和 v 引申的附属条款分支在关系 R 下是否等价。
   - 格式：<query_compare>u,v</query_compare>
   - 返回：是 或 否

2. 提交等价关系（Claim）：当你收集了足够信息后，声明你认为的等价关系类型。
   - 格式：<claim>X</claim>（其中 X 是 A、B、C 或 D）
   - 注意：你必须先进行至少 2 次有效的比较查询后，才能提交声明。
   - 返回：正确 或 错误（若错误，审查立即失败）

3. 预测查询（Predict）：在成功提交等价关系后，对一对此前未比较过的条款进行预测。
   - 格式：<query_predict>u,v,answer</query_predict>（其中 answer 是"是"或"否"）
   - 返回：命中 或 未命中

成功条件：至少 2 次有效比较查询；正确提交关系类型；预测查询正确。
失败条件：未满 2 次查询即提交；关系类型错误；预测答案错误。
请尽可能少地使用查询次数来完成任务。

注意：每次回复中请只使用一种操作标签（query_compare、claim 或 query_predict 中的一个），不要同时使用多个标签。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
You have logged into the "Legal Contract Clause Logical Equivalence Review System".

The system has imported a standard contract logic tree comprising {n} clause nodes (numbered 1 to {n}, with node 1 as the core master clause). The subordinate clauses under each node have a strict textual reading order.

To review the equivalence of different drafts, the system secretly sets a hidden "Equivalence Jurisprudential Relation" R, chosen from the following four:
1. Rule A (Strict Ordered Isomorphism): The logic structures of the two drafts are identical, and the arrangement order of subordinate clauses under each clause matches exactly.
2. Rule B (Layer-wise Reversible): Same structure, but at any clause node, the sequence of all subordinate clauses may be entirely reversed before matching; each clause independently decides.
3. Rule C (Unordered Isomorphism): Same structure, but ignoring the reading order of subordinate clauses, treating them as multisets of terms for recursive matching.
4. Rule D (Compressed Unordered Isomorphism): First condense the draft (repeatedly remove transitional boilerplate clauses that are "not the core master clause and have only a single subordinate clause"), then compare the condensed jurisprudential topologies using Rule C.

Your task is to deduce the active equivalence relation R through comparative probing and make an accurate prediction on a new pair of contract clause branches.

Available operations:
1. Comparison Query (Compare): Ask if the subordinate branches of clauses u and v are equivalent under relation R.
   - Format: <query_compare>u,v</query_compare>
   - Returns: Yes or No

2. Claim Equivalence Relation (Claim): Declare which equivalence relation type you believe is correct.
   - Format: <claim>X</claim> (where X is A, B, C, or D)
   - Note: You must perform at least 2 valid comparison queries before making a claim.
   - Returns: Correct or Wrong (if wrong, the review ends in failure)

3. Prediction Query (Predict): After successfully claiming the relation, make a prediction on a previously uncompared pair of clauses.
   - Format: <query_predict>u,v,answer</query_predict> (where answer is "Yes" or "No")
   - Returns: Hit or Miss

Success conditions: At least 2 valid comparison queries; correct relation claimed; correct prediction.
Failure conditions: Claiming before 2 queries; incorrect relation; incorrect prediction.
Try to complete the task with minimal queries.

Note: Please use only one operation tag per response (one of query_compare, claim, or query_predict). Do not use multiple tags simultaneously.
"""

    tags = ["answer", "query_compare", "claim", "query_predict"]
    reasoning_type = "溯因推理"
    data_structure = "树"

    # 树结构定义（固定38节点）
    TREE_STRUCTURE = {
        1: [2, 3, 4, 5, 16, 17],
        2: [6, 7, 8],
        3: [10, 11, 12],
        4: [21, 22, 23],
        5: [27, 28, 30],
        16: [33, 34],
        17: [37],
        6: [13, 14],
        7: [],
        8: [15],
        10: [18],
        11: [],
        12: [19, 20],
        21: [24, 25],
        22: [26],
        23: [],
        27: [],
        28: [29],
        30: [31, 32],
        33: [35],
        34: [36],
        37: [38],
        13: [], 14: [], 15: [], 18: [], 19: [], 20: [],
        24: [], 25: [], 26: [], 29: [], 31: [], 32: [],
        35: [], 36: [], 38: []
    }

    # 难度配置
    # 难度1（简单）: A - 严格有序同构
    # 难度2（中等偏下）: B - 逐层可整体反转
    # 难度3（中等偏上）: C - 无序同构
    # 难度4（较难）: D - 压缩后无序同构
    # 难度5（难）: 随机选择（但在实现中我们固定为B，以保证可复现）
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"relation": "A"},
            2: {"relation": "B"},
            3: {"relation": "C"},
            4: {"relation": "D"},
            5: {"relation": "B"},  # 难度5可设为更复杂情况，这里用B
        },
        "en": {
            1: {"relation": "A"},
            2: {"relation": "B"},
            3: {"relation": "C"},
            4: {"relation": "D"},
            5: {"relation": "B"},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据语言和难度选择等价关系R"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.relation_type = cfg["relation"]
        self._game_info["n"] = 38

        # 记录比较次数、已比较的节点对、是否已声明正确
        self.compare_count = 0
        self.compared_pairs = set()
        self.claimed_success = False

    def _get_subtree_structure(self, node):
        """递归获取以node为根的子树结构（用于后续比较算法）"""
        children = self.TREE_STRUCTURE.get(node, [])
        return {
            "node": node,
            "children": [self._get_subtree_structure(c) for c in children]
        }

    def _check_isomorphism_A(self, tree1, tree2):
        """关系A：严格有序同构"""
        if len(tree1["children"]) != len(tree2["children"]):
            return False
        for c1, c2 in zip(tree1["children"], tree2["children"]):
            if not self._check_isomorphism_A(c1, c2):
                return False
        return True

    def _check_isomorphism_B(self, tree1, tree2):
        """关系B：逐层可整体反转"""
        if len(tree1["children"]) != len(tree2["children"]):
            return False
        children1 = tree1["children"]
        children2 = tree2["children"]
        # 尝试不反转
        if all(self._check_isomorphism_B(c1, c2) for c1, c2 in zip(children1, children2)):
            return True
        # 尝试反转tree2的子女序列
        if all(self._check_isomorphism_B(c1, c2) for c1, c2 in zip(children1, reversed(children2))):
            return True
        return False

    def _check_isomorphism_C(self, tree1, tree2):
        """关系C：无序同构（子女视为多重集合）"""
        if len(tree1["children"]) != len(tree2["children"]):
            return False
        # 使用贪心匹配：为tree1的每个孩子找tree2中未匹配的等价孩子
        children2_available = list(tree2["children"])
        for c1 in tree1["children"]:
            matched = False
            for i, c2 in enumerate(children2_available):
                if self._check_isomorphism_C(c1, c2):
                    children2_available.pop(i)
                    matched = True
                    break
            if not matched:
                return False
        return True

    def _compress_tree(self, tree):
        """关系D辅助：压缩子树（删除非根且出度为1的节点）"""
        # 递归压缩所有孩子
        children = [self._compress_tree(c) for c in tree["children"]]
        # 如果当前节点只有一个孩子，且当前节点不是原始子树的根，则跳过（但我们总是从某个根开始，所以这里简化处理）
        # 压缩规则：非根且出度为1的节点被删除，这里我们从子树根开始，所以根保留，递归处理子女
        compressed_children = []
        for child in children:
            # 如果child只有一个孙子，则提升孙子（压缩child）
            while len(child["children"]) == 1:
                child = child["children"][0]
            compressed_children.append(child)
        return {
            "node": tree["node"],
            "children": compressed_children
        }

    def _check_isomorphism_D(self, tree1, tree2):
        """关系D：压缩后无序同构"""
        compressed1 = self._compress_tree(tree1)
        compressed2 = self._compress_tree(tree2)
        return self._check_isomorphism_C(compressed1, compressed2)

    def _compare_subtrees(self, u, v):
        """根据当前关系类型比较节点u和v的子树"""
        tree_u = self._get_subtree_structure(u)
        tree_v = self._get_subtree_structure(v)

        if self.relation_type == "A":
            return self._check_isomorphism_A(tree_u, tree_v)
        elif self.relation_type == "B":
            return self._check_isomorphism_B(tree_u, tree_v)
        elif self.relation_type == "C":
            return self._check_isomorphism_C(tree_u, tree_v)
        elif self.relation_type == "D":
            return self._check_isomorphism_D(tree_u, tree_v)
        else:
            raise ValueError(f"Unknown relation type: {self.relation_type}")

    def evaluate(self, parsed_info):
        """评估最终答案（此游戏通过claim和predict完成，answer标签作为备用）"""
        # 本游戏主要通过claim和predict判定，answer标签可作为综合提交
        # 如果模型直接使用answer提交，可解析为 "relation=X, predict=u,v,ans"
        raw_ans = parsed_info["answer"]
        # 简化处理：要求格式 relation=X
        if "relation=" in raw_ans:
            parts = raw_ans.split(",")
            rel = None
            for part in parts:
                if "relation=" in part:
                    rel = part.split("=")[1].strip().upper()
                    break
            if rel and rel == self.relation_type:
                # 如果还包含预测部分，也可解析，这里简化为只检查relation
                self.claimed_success = True
                return True
        return False

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑，根据不同的查询类型生成响应"""
        yes_res = "是" if self.config.language == "zh" else "Yes"
        no_res = "否" if self.config.language == "zh" else "No"
        error_format = "错误：格式无效。" if self.config.language == "zh" else "Error: Invalid format."
        error_range = "错误：节点编号超出范围。" if self.config.language == "zh" else "Error: Node ID out of range."

        # 优先级：query_compare > claim > query_predict
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                if u not in self.TREE_STRUCTURE or v not in self.TREE_STRUCTURE:
                    return error_range

                # 记录已比较的节点对（无序）
                pair = tuple(sorted([u, v]))
                self.compared_pairs.add(pair)
                self.compare_count += 1

                result = self._compare_subtrees(u, v)
                return yes_res if result else no_res

            except Exception as e:
                return error_format

        elif "claim" in parsed_info:
            # 检查是否已进行至少2次比较
            if self.compare_count < 2:
                msg = "错误：你必须先进行至少2次比较查询才能提交声明。" if self.config.language == "zh" else "Error: You must perform at least 2 comparison queries before claiming."
                self.state.set_state("failed", "claim_too_early")
                return msg

            claimed_relation = parsed_info["claim"].strip().upper()
            if claimed_relation == self.relation_type:
                self.claimed_success = True
                return "正确" if self.config.language == "zh" else "Correct"
            else:
                msg = "错误" if self.config.language == "zh" else "Wrong"
                self.state.set_state("failed", "incorrect_claim")
                return msg

        elif "query_predict" in parsed_info:
            if not self.claimed_success:
                msg = "错误：你必须先正确提交等价关系声明才能进行预测。" if self.config.language == "zh" else "Error: You must correctly claim the relation before predicting."
                self.state.set_state("failed", "predict_without_claim")
                return msg

            try:
                raw = parsed_info["query_predict"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                user_answer = parts[2]

                if u not in self.TREE_STRUCTURE or v not in self.TREE_STRUCTURE:
                    return error_range

                # 检查是否是未比较过的节点对
                pair = tuple(sorted([u, v]))
                if pair in self.compared_pairs:
                    msg = "错误：该节点对已被比较过，请选择新的节点对。" if self.config.language == "zh" else "Error: This pair has been compared before. Choose a new pair."
                    return msg

                # 计算真实答案
                real_result = self._compare_subtrees(u, v)
                real_answer = yes_res if real_result else no_res

                # 标准化用户答案
                if self.config.language == "zh":
                    user_answer_normalized = "是" if user_answer in ["是", "Yes", "yes", "Y", "y"] else "否"
                else:
                    user_answer_normalized = "Yes" if user_answer in ["是", "Yes", "yes", "Y", "y"] else "No"

                if user_answer_normalized == real_answer:
                    msg = "命中" if self.config.language == "zh" else "Hit"
                    self.state.set_state("success", "prediction_correct")
                    return msg
                else:
                    msg = "未命中" if self.config.language == "zh" else "Miss"
                    self.state.set_state("failed", "prediction_incorrect")
                    return msg

            except Exception as e:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """将正确的比较结果反转，用于反事实干预"""
        yes_res = "是" if self.config.language == "zh" else "Yes"
        no_res = "否" if self.config.language == "zh" else "No"
        
        if correct == yes_res:
            return no_res
        elif correct == no_res:
            return yes_res
        elif correct in ("正确", "Correct"):
            return "错误" if self.config.language == "zh" else "Wrong"
        elif correct in ("命中", "Hit"):
            return "未命中" if self.config.language == "zh" else "Miss"
        else:
            # 兜底：返回一个显然错误的答案
            return no_res

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        possible_queries = []
        yes_res = "是" if self.config.language == "zh" else "Yes"
        no_res = "否" if self.config.language == "zh" else "No"
        
        # 获取所有节点编号并排序
        nodes = sorted(list(self.TREE_STRUCTURE.keys()))
        n = len(nodes)
        
        # 枚举所有唯一的节点对 (u, v)，其中 u < v
        for i in range(n):
            for j in range(i + 1, n):
                u = nodes[i]
                v = nodes[j]
                
                # 直接调用内部比较逻辑计算结果
                # 不调用 produce_response 以避免改变游戏状态或触发反事实逻辑
                result = self._compare_subtrees(u, v)
                ans = yes_res if result else no_res
                
                # 构造返回对象
                # query 字段对应 query_compare 标签的内容
                possible_queries.append({
                    "query": f"<query_compare>{u},{v}</query_compare>",
                    "answer": ans
                })
                
        return possible_queries