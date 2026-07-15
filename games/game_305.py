from .base import Game
import re

class SubtreeEquivalenceGame(Game):

    game_rule_zh = """\
我们来玩一个"子树等价溯因"推理游戏，规则如下：

游戏设定了一棵固定的有序根树，节点编号 1 到 35，根节点为 1。每个节点的孩子有固定顺序。

存在四种候选的子树结构等价关系，它们定义了如何比较两棵子树是否等价：
1. OE（严格有序）：在每一对应节点处，孩子序列长度相同，按原顺序一一对应，且对应孩子子树递归等价。
2. OR（允许整序反转）：在每一对应节点处，允许将一侧的孩子序列整体反转后再逐位比较；若能在该选择下使对应孩子子树递归等价，则视为等价。不得进行除整序反转之外的重排。
3. UE（无序计重）：在每一对应节点处，忽略孩子顺序，将孩子子树视为一个多重集合；存在一个多重集合匹配使对应孩子子树递归等价，且相同形子树的数量需一致。
4. UD（无序去重）：在每一对应节点处，忽略孩子顺序与重复，将孩子子树按形状去重为集合；集合中的每一种不同形状均需在另一侧出现，且对应形状递归等价，不要求计数一致。

我已秘密选择了其中一种等价关系作为真实规则。

你的目标是：
1. 通过询问指定的节点对，根据是/否反馈推断出真实的等价关系。
2. 依据推断出的等价关系，判断另一指定节点对的子树是否等价。

你可以询问的节点对仅限：(2,3)、(13,14)、(25,26)。询问时我会根据真实等价关系判断这两个节点的子树是否等价，并回答"是"或"否"。

注意：若询问不在指定范围内的节点对，会被记为无效询问。若累计两次及以上无效询问，游戏失败。

每次询问使用以下 XML 格式：

- 询问节点对（例如询问节点 2 和节点 3）：
<twin_check>2,3</twin_check>

提交最终答案时，需要指明真实的等价关系（OE、OR、UE 或 UD），以及在该关系下节点对 (13,26) 的子树是否等价（是或否），格式如下：

<answer>relation=OE, result=是</answer>
"""

    game_rule_en = """\
Let's play a "Subtree Equivalence Abduction" reasoning game. Here are the rules:

The game features a fixed ordered rooted tree with nodes numbered 1 to 35, with root node 1. Each node's children have a fixed order.

There are four candidate subtree structural equivalence relations that define how to compare whether two subtrees are equivalent:
1. OE (Ordered Exact): At each corresponding node, the child sequences have the same length, match one-to-one in original order, and corresponding child subtrees are recursively equivalent.
2. OR (Order with Reversal): At each corresponding node, allows reversing the entire child sequence of one side before pairwise comparison; if this choice makes corresponding child subtrees recursively equivalent, they are considered equivalent. No reordering other than full reversal is allowed.
3. UE (Unordered with multiplicity Exact): At each corresponding node, ignores child order and treats child subtrees as a multiset; there exists a multiset matching such that corresponding child subtrees are recursively equivalent, and counts of identical subtrees must match.
4. UD (Unordered Deduplicated): At each corresponding node, ignores both child order and duplicates, deduplicating child subtrees by shape into a set; each distinct shape in the set must appear on the other side with corresponding shapes recursively equivalent, without requiring count consistency.

I have secretly selected one of these equivalence relations as the true rule.

Your goals are:
1. Through querying specified node pairs and receiving Yes/No feedback, deduce the true equivalence relation.
2. Based on the deduced equivalence relation, determine whether another specified node pair's subtrees are equivalent.

You may only query these node pairs: (2,3), (13,14), (25,26). When querying, I will judge whether these two nodes' subtrees are equivalent according to the true equivalence relation, and answer "Yes" or "No".

Note: Querying node pairs outside the specified range will be recorded as invalid queries. If there are two or more invalid queries, the game fails.

Each query uses the following XML format:

- Query node pair (e.g., querying nodes 2 and 3):
<twin_check>2,3</twin_check>

When submitting the final answer, specify the true equivalence relation (OE, OR, UE, or UD) and whether the subtrees of node pair (13,26) are equivalent under that relation (Yes or No), using this format:

<answer>relation=OE, result=Yes</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通路网调度系统。在此进行“交通枢纽拓扑等价”推断分析。

系统记录了一棵固定的单向放射状路网拓扑树，枢纽节点编号 1 到 35，总枢纽为节点 1。每个枢纽的分流路线有固定的空间排布顺序。

目前存在四种评估不同分流区域（子树）等价性的通行量代换规则：
1. OE（严格有序）：在每个对应枢纽处，分流路线数量相同，空间顺序一一对应，且对应的下游路网递归等价。
2. OR（允许整序反转）：在每个对应枢纽处，允许将一侧的路线排布完全镜像反转后再逐位对比；若在该调度下使对应的下游路网递归等价，则视为等价。不得进行除整体反转外的重排。
3. UE（无序计重）：在每个对应枢纽处，忽略路线的空间顺序，仅视下游路网为多重集合；只要存在一种匹配使得下游路网递归等价，且相同拓扑的路网数量一致，则视为等价。
4. UD（无序去重）：在每个对应枢纽处，忽略路线顺序与冗余建设，将下游路网按拓扑去重；每一种独特的拓扑均需在另一侧出现并递归等价，不要求冗余路线数量一致。

我已在后台秘密加载了其中一种代换规则作为当前的真实系统基准。

你的任务是：
1. 通过向系统查验指定的枢纽对，根据“是/否”反馈推断出真实的代换规则。
2. 依据推断出的规则，判断另一指定枢纽对的下游路网是否等价。

你被授权查验的枢纽对仅限：(2,3)、(13,14)、(25,26)。查验时，我会根据真实规则判断这两个枢纽的下游路网是否等价，并回答“是”或“否”。
注意：若查验越权（不在指定范围内），将被记录为无效操作。累计两次及以上无效操作，系统阻断，任务失败。

每次查验请使用以下 XML 格式：
- 查验枢纽对（例如查验枢纽 2 和枢纽 3）：
<twin_check>2,3</twin_check>

提交最终报告时，需指明真实的代换规则（OE、OR、UE 或 UD），以及枢纽对 (13,26) 的下游路网是否等价（是或否）：
<answer>relation=OE, result=是</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Network Scheduling System. You are tasked with analyzing "Traffic Hub Topology Equivalence."

The system maps a fixed, one-way radial road network topology tree, with hub nodes numbered 1 to 35, and the main hub at node 1. Each hub's diverging routes have a fixed spatial layout sequence.

There are four candidate capacity-substitution rules for assessing the equivalence of different diverging areas (subtrees):
1. OE (Ordered Exact): At each corresponding hub, the diverging routes have identical counts, strict one-to-one spatial order, and downstream networks recursively match.
2. OR (Order with Reversal): At each corresponding hub, one side's route layout can be completely mirrored (reversed) before pairwise comparison; if this ensures downstream networks recursively match, they are equivalent. No reshuffling beyond full reversal is allowed.
3. UE (Unordered with multiplicity Exact): At each corresponding hub, spatial order is ignored, treating downstream networks as a multiset; if a matching exists making downstream networks recursively equivalent with identical topology counts, they are equivalent.
4. UD (Unordered Deduplicated): At each corresponding hub, order and redundant construction are ignored, deduplicating downstream networks by topology; each unique topology must appear on the counterpart side and recursively match, without requiring redundant route count consistency.

I have secretly loaded one substitution rule as the active system benchmark.

Your objectives:
1. Deduce the true substitution rule by querying specific hub pairs and analyzing the Yes/No feedback.
2. Based on the deduced rule, determine whether the downstream networks of another specified hub pair are equivalent.

Authorized query hub pairs: (2,3), (13,14), (25,26). I will evaluate their equivalence using the active rule and respond "Yes" or "No".
Note: Queries outside this scope are marked invalid. Two or more invalid queries will trigger a system lockout, resulting in failure.

Format for each query:
- Query hub pair (e.g., hubs 2 and 3):
<twin_check>2,3</twin_check>

When submitting the final report, specify the true rule (OE, OR, UE, or UD), and whether hub pair (13,26) is equivalent (Yes or No):
<answer>relation=OE, result=Yes</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎进入临床血管分支分析系统。在此进行“血管网络拓扑等价”溯因诊断。

系统重建了一棵固定的血管造影结构树，分叉节点编号 1 到 35，主动脉根节点为 1。每个节点发出的微血管分支有固定的解剖学空间顺序。

目前存在四种评估不同血管子网等价性的血流动力学对比规则：
1. OE（严格有序）：在每个对应分叉处，分支数量相同，解剖顺序一一对应，且下游血管网递归等价。
2. OR（允许整序反转）：在每个对应分叉处，允许将一侧的分支序列整体镜像反转后再对比；若反转后能使下游血管网递归等价，即视为等价。不得进行其他错位重排。
3. UE（无序计重）：在每个对应分叉处，忽略血管解剖顺序，视下游血管网为多重集合；只要存在一种匹配使下游网递归等价且特定结构的血管数量一致，则视为等价。
4. UD（无序去重）：在每个对应分叉处，忽略顺序与增生冗余血管，按结构去重；每种独特的血管构型均需在另一侧存在并递归等价，不要求冗余血管数量一致。

我已在后台秘密配置了其中一种对比规则作为本次病例的诊断依据。

你的任务是：
1. 通过向系统比对指定的血管分叉对，根据“是/否”反馈推断出真实的诊断规则。
2. 依据推断出的规则，判断另一指定分叉对的下游血管网是否等价。

你被授权比对的分叉对仅限：(2,3)、(13,14)、(25,26)。比对时，我会根据真实规则判断这两个分叉的下游网是否等价，并回答“是”或“否”。
注意：违规比对将被计为无效操作。累计两次及以上无效操作将导致诊断超时失败。

每次比对请使用以下 XML 格式：
- 比对分叉对（例如比对节点 2 和 3）：
<twin_check>2,3</twin_check>

提交最终诊断时，需指明真实的诊断规则（OE、OR、UE 或 UD），以及分叉对 (13,26) 的下游血管网是否等价（是或否）：
<answer>relation=OE, result=是</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Clinical Vascular Branching Analysis System. You are to perform a "Vascular Network Topology Equivalence" diagnostic deduction.

The system has reconstructed a fixed angiographic structure tree, with bifurcation nodes numbered 1 to 35, and the aortic root at node 1. The microvascular branches emerging from each node follow a fixed anatomical spatial order.

There are four candidate hemodynamic comparison rules for evaluating the equivalence of different vascular subnetworks:
1. OE (Ordered Exact): At each corresponding bifurcation, branch counts are identical, anatomical orders match strictly one-to-one, and downstream vascular networks are recursively equivalent.
2. OR (Order with Reversal): At each corresponding bifurcation, one side's branch sequence can be fully mirrored (reversed) before comparison; if this makes downstream networks recursively equivalent, they are deemed equivalent. No other reshuffling is permitted.
3. UE (Unordered with multiplicity Exact): At each corresponding bifurcation, anatomical order is ignored, treating downstream networks as a multiset; equivalence holds if a matching exists where downstream networks are recursively equivalent and counts of identical vascular structures match.
4. UD (Unordered Deduplicated): At each corresponding bifurcation, order and redundant hyperplastic vessels are ignored, deduplicating by structure; each unique vascular configuration must be present on the counterpart side and recursively match, without requiring redundant vessel count consistency.

I have secretly configured one comparison rule as the diagnostic basis for this case.

Your tasks:
1. Deduce the true diagnostic rule by querying specific bifurcation pairs and utilizing the Yes/No feedback.
2. Based on the deduced rule, determine whether the downstream networks of another specified bifurcation pair are equivalent.

Authorized query bifurcation pairs: (2,3), (13,14), (25,26). I will assess their equivalence using the active rule and respond "Yes" or "No".
Note: Unauthorized queries are logged as invalid operations. Two or more invalid operations will result in diagnostic timeout and failure.

Format for each query:
- Query bifurcation pair (e.g., nodes 2 and 3):
<twin_check>2,3</twin_check>

When submitting the final diagnosis, specify the true diagnostic rule (OE, OR, UE, or UD), and whether bifurcation pair (13,26) is equivalent (Yes or No):
<answer>relation=OE, result=Yes</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入自适应教育知识图谱系统。在此进行“学习路径等价性”推理评估。

系统设定了一棵固定的前置知识依赖树，知识模块编号 1 到 35，根学科核心模块为 1。每个模块的子学习单元有固定的教学顺序。

目前存在四种评估不同学习路径（子树）等价性的教学目标评估规则：
1. OE（严格有序）：在每个对应模块处，子单元数量相同，学习顺序一一对应，且对应的后续知识图谱递归等价。
2. OR（允许整序反转）：在每个对应模块处，允许将一侧的子单元学习顺序完全反转后再逐位对比（例如从后向前学）；若能使对应的后续知识图谱递归等价，则视为等价。不得进行整体反转之外的顺序打乱。
3. UE（无序计重）：在每个对应模块处，忽略学习顺序，将子单元视为多重集合；只要存在匹配使后续知识图谱递归等价，且同类强化的练习模块数量一致，则视为等价。
4. UD（无序去重）：在每个对应模块处，忽略顺序与重复练习，按知识点覆盖去重；每一种知识点分支均需在另一侧覆盖并递归等价，不要求重复练习的次数一致。

我已秘密应用了其中一种评估规则作为当前班级的考核标准。

你的任务是：
1. 通过向系统测试指定的模块对，根据“是/否”反馈推断出真实的评估规则。
2. 依据推断出的规则，判断另一指定模块对的后续学习路径是否等价。

你被授权测试的模块对仅限：(2,3)、(13,14)、(25,26)。测试时，我会根据真实规则判断这两个模块的后续路径是否等价，并回答“是”或“否”。
注意：测试指定范围外的模块将被记为无效请求。累计两次及以上无效请求，评测判定失败。

每次测试请使用以下 XML 格式：
- 测试模块对（例如测试模块 2 和 3）：
<twin_check>2,3</twin_check>

提交最终报告时，需指明真实的评估规则（OE、OR、UE 或 UD），以及模块对 (13,26) 的后续路径是否等价（是或否）：
<answer>relation=OE, result=是</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Education Knowledge Graph System. You will conduct a "Learning Path Equivalence" reasoning assessment.

The system features a fixed prerequisite dependency tree, with knowledge modules numbered 1 to 35, and the core subject root at module 1. Each module's sub-learning units follow a strict pedagogical sequence.

There are four candidate pedagogical objective rules for assessing the equivalence of different learning paths (subtrees):
1. OE (Ordered Exact): At each corresponding module, sub-unit counts are identical, learning sequences match one-to-one, and subsequent knowledge graphs are recursively equivalent.
2. OR (Order with Reversal): At each corresponding module, one side's learning sequence can be entirely reversed (e.g., studying backwards) before comparison; if this makes subsequent knowledge graphs recursively equivalent, they are deemed equivalent. No random shuffling beyond full reversal is allowed.
3. UE (Unordered with multiplicity Exact): At each corresponding module, learning sequence is ignored, treating sub-units as a multiset; equivalence holds if a matching exists where subsequent graphs are recursively equivalent and counts of identical reinforcement modules match.
4. UD (Unordered Deduplicated): At each corresponding module, sequence and repetitive practices are ignored, deduplicating by topic coverage; each unique knowledge branch must be covered on the counterpart side and recursively match, without requiring identical repetition counts.

I have secretly applied one assessment rule as the evaluation standard for the current class.

Your tasks:
1. Deduce the true assessment rule by testing specific module pairs and analyzing the Yes/No feedback.
2. Based on the deduced rule, determine whether the subsequent learning paths of another specified module pair are equivalent.

Authorized test module pairs: (2,3), (13,14), (25,26). I will evaluate their equivalence using the active rule and respond "Yes" or "No".
Note: Testing modules outside the specified range is recorded as an invalid request. Two or more invalid requests will result in an assessment failure.

Format for each test:
- Test module pair (e.g., modules 2 and 3):
<twin_check>2,3</twin_check>

When submitting the final report, specify the true assessment rule (OE, OR, UE, or UD), and whether module pair (13,26) is equivalent (Yes or No):
<answer>relation=OE, result=Yes</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入工业制造BOM（物料清单）验证系统。在此进行“装配子树等价性”逆向推断。

系统载入了一棵固定的复杂机械装配BOM树，组件编号 1 到 35，最终总成节点为 1。每个组件的子装配流程存在固定的工序顺序。

目前存在四种评估不同子装配体可替换性（等价性）的工程验证规则：
1. OE（严格有序）：在每个对应组件处，子工序数量相同，装配顺序一一对应，且对应的下级BOM递归等价。
2. OR（允许整序反转）：在每个对应组件处，允许将一侧的子工序完全镜像反转后再对比；若能在该操作下使对应的下级BOM递归等价，则视为可替换。严禁进行整体反转之外的工序打乱。
3. UE（无序计重）：在每个对应组件处，忽略装配顺序，将子工序视为散件包（多重集合）；只要存在匹配使下级BOM递归等价，且同规格子组件的耗用数量严格一致，则视为可替换。
4. UD（无序去重）：在每个对应组件处，忽略顺序与重复备件，按规格种类去重；每一种规格的子组件均需在另一侧出现并递归等价，假假设备件库无限，不要求消耗数量一致。

我已在制造执行系统中秘密锁定了其中一种工程验证规则。

你的任务是：
1. 通过向系统比对指定的组件对，根据“是/否”反馈推断出真实的验证规则。
2. 依据推断出的规则，判断另一指定组件对的装配逻辑是否等价。

你被授权比对的组件对仅限：(2,3)、(13,14)、(25,26)。比对时，我会根据真实规则判断这两个组件的装配逻辑是否等价，并回答“是”或“否”。
注意：比对系统限制外的组件将被拦截并记为违规。累计两次及以上违规将导致验证流程终止。

每次比对请使用以下 XML 格式：
- 比对组件对（例如比对组件 2 和 3）：
<twin_check>2,3</twin_check>

提交最终结论时，需指明真实的验证规则（OE、OR、UE 或 UD），以及组件对 (13,26) 是否等价（是或否）：
<answer>relation=OE, result=是</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Manufacturing BOM (Bill of Materials) Validation System. You will execute an "Assembly Subtree Equivalence" reverse engineering deduction.

The system has loaded a fixed complex machinery assembly BOM tree, with components numbered 1 to 35, and the final assembly at node 1. Each component's sub-assembly process follows a strict procedural sequence.

There are four candidate engineering validation rules to assess the interchangeability (equivalence) of different sub-assemblies:
1. OE (Ordered Exact): At each corresponding component, sub-procedure counts are identical, assembly sequences match one-to-one, and lower-level BOMs are recursively equivalent.
2. OR (Order with Reversal): At each corresponding component, one side's sub-procedure sequence can be fully mirrored (reversed) before comparison; if this makes lower-level BOMs recursively equivalent, they are deemed interchangeable. No reshuffling beyond full reversal is allowed.
3. UE (Unordered with multiplicity Exact): At each corresponding component, assembly sequence is ignored, treating sub-procedures as a parts kit (multiset); equivalence holds if a matching makes lower-level BOMs recursively equivalent, and consumption quantities of identical sub-components perfectly match.
4. UD (Unordered Deduplicated): At each corresponding component, sequence and duplicate spare parts are ignored, deduplicating by specification; each specification type must appear on the counterpart side and recursively match, assuming infinite spare inventory without requiring identical consumption quantities.

I have secretly locked one engineering validation rule within the Manufacturing Execution System.

Your tasks:
1. Deduce the true validation rule by comparing specific component pairs and utilizing the Yes/No feedback.
2. Based on the deduced rule, determine whether the assembly logic of another specified component pair is equivalent.

Authorized comparison component pairs: (2,3), (13,14), (25,26). I will assess their interchangeability using the active rule and respond "Yes" or "No".
Note: Comparing components outside system limits will be blocked and recorded as a violation. Two or more violations will terminate the validation workflow.

Format for each comparison:
- Compare component pair (e.g., components 2 and 3):
<twin_check>2,3</twin_check>

When submitting the final conclusion, specify the true validation rule (OE, OR, UE, or UD), and whether component pair (13,26) is equivalent (Yes or No):
<answer>relation=OE, result=Yes</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入企业合规与股权穿透分析系统。在此进行“控股架构等价”溯因审查。

系统映射了一棵固定的集团企业控制权属树，实体编号 1 到 35，顶级母公司为节点 1。每个法人的下设子公司有固定的工商登记顺位。

目前存在四种评估不同控股支柱（子树）合规等价性的穿透审查规则：
1. OE（严格有序）：在每个对应母体处，子公司数量相同，设立顺位一一对应，且对应的底层架构递归等价。
2. OR（允许整序反转）：在每个对应母体处，允许将一侧的子公司设立顺位完全反转后再逐位审查；若能使对应的底层架构递归等价，则视为合规等价。严禁进行顺位反转之外的结构腾挪。
3. UE（无序计重）：在每个对应母体处，忽略设立顺位，将子公司群视为多重集合；只要存在匹配使底层架构递归等价，且同类资质实体的持股数量一致，则视为合规等价。
4. UD（无序去重）：在每个对应母体处，忽略顺位与重复注册的壳公司，按业务资质去重；每一种核心资质实体均需在另一侧出现并递归等价，不要求冗余注册数量一致。

我已在法务合规库中秘密指定了其中一种审查规则作为本次尽调的准则。

你的任务是：
1. 通过向系统质询指定的实体对，根据“是/否”反馈推断出真实的审查规则。
2. 依据推断出的规则，判断另一指定实体对的控股架构是否等价。

你被授权质询的实体对仅限：(2,3)、(13,14)、(25,26)。质询时，我会根据真实规则判断这两个实体的架构是否等价，并回答“是”或“否”。
注意：越权质询非指定实体将被风控拦截记为违规。累计两次及以上违规，尽调流程将被强制终止。

每次质询请使用以下 XML 格式：
- 质询实体对（例如质询实体 2 和 3）：
<twin_check>2,3</twin_check>

出具最终意见书时，需指明真实的审查规则（OE、OR、UE 或 UD），以及实体对 (13,26) 是否等价（是或否）：
<answer>relation=OE, result=是</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Corporate Compliance and Shareholding Penetration Analysis System. You will conduct a "Holding Structure Equivalence" due diligence abduction.

The system maps a fixed group corporate control ownership tree, with entities numbered 1 to 35, and the top-tier parent company at node 1. Each legal entity's subsidiaries follow a fixed corporate registration sequence.

There are four candidate penetration review rules for assessing the compliance equivalence of different holding pillars (subtrees):
1. OE (Ordered Exact): At each corresponding parent, subsidiary counts are identical, registration sequences match one-to-one, and underlying structures are recursively equivalent.
2. OR (Order with Reversal): At each corresponding parent, one side's subsidiary sequence can be fully reversed before review; if this makes underlying structures recursively equivalent, they are deemed compliance-equivalent. No restructuring beyond full sequence reversal is allowed.
3. UE (Unordered with multiplicity Exact): At each corresponding parent, registration sequence is ignored, treating subsidiaries as a multiset; equivalence holds if a matching makes underlying structures recursively equivalent, and counts of identical licensed entities perfectly match.
4. UD (Unordered Deduplicated): At each corresponding parent, sequence and redundant shell companies are ignored, deduplicating by business license type; each core licensed entity must appear on the counterpart side and recursively match, without requiring redundant registration count consistency.

I have secretly designated one review rule within the legal compliance database as the standard for this due diligence.

Your tasks:
1. Deduce the true review rule by querying specific entity pairs and utilizing the Yes/No feedback.
2. Based on the deduced rule, determine whether the holding structures of another specified entity pair are equivalent.

Authorized query entity pairs: (2,3), (13,14), (25,26). I will evaluate their structural equivalence using the active rule and respond "Yes" or "No".
Note: Unauthorized queries outside the designated entities will be intercepted by risk control as a violation. Two or more violations will forcefully terminate the due diligence process.

Format for each query:
- Query entity pair (e.g., entities 2 and 3):
<twin_check>2,3</twin_check>

When issuing the final legal opinion, specify the true review rule (OE, OR, UE, or UD), and whether entity pair (13,26) is equivalent (Yes or No):
<answer>relation=OE, result=Yes</answer>
"""

    tags = ["answer", "twin_check"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    TREE_STRUCTURE = {
        1: [2,3,4],
        2: [5,6],
        3: [7,8],
        4: [13,14,25,26],
        5: [],
        6: [9,10],
        7: [11,12],
        8: [],
        9: [],
        10: [],
        11: [],
        12: [],
        13: [15,16,17],
        14: [18,23,24],
        15: [],
        16: [19,20],
        17: [],
        18: [21,22],
        19: [],
        20: [],
        21: [],
        22: [],
        23: [],
        24: [],
        25: [27,28,29],
        26: [32,33],
        27: [],
        28: [],
        29: [30,31],
        30: [],
        31: [],
        32: [],
        33: [34,35],
        34: [],
        35: []
    }

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "relation": "OE",
                "target_result": "否"
            },
            2: {
                "relation": "UD",
                "target_result": "是"
            },
            3: {
                "relation": "UE",
                "target_result": "否"
            },
            4: {
                "relation": "OR",
                "target_result": "否"
            },
            5: {
                "relation": "OE",
                "target_result": "否"
            }
        },
        "en": {
            1: {
                "relation": "OE",
                "target_result": "No"
            },
            2: {
                "relation": "UD",
                "target_result": "Yes"
            },
            3: {
                "relation": "UE",
                "target_result": "No"
            },
            4: {
                "relation": "OR",
                "target_result": "No"
            },
            5: {
                "relation": "OE",
                "target_result": "No"
            }
        }
    }

    ALLOWED_PAIRS = [(2,3), (13,14), (25,26)]
    TARGET_PAIR = (13, 26)

    def __init__(self, config):
        self.invalid_query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.true_relation = cfg["relation"]
        self.target_result = cfg["target_result"]
        
        actual_equiv = self._check_equivalence(
            self.TARGET_PAIR[0], self.TARGET_PAIR[1], self.true_relation
        )
        if lang == "zh":
            actual_result = "是" if actual_equiv else "否"
        else:
            actual_result = "Yes" if actual_equiv else "No"
        assert actual_result == self.target_result, (
            f"Mismatch: computed {actual_result} but config says {self.target_result} "
            f"for relation={self.true_relation}, pair={self.TARGET_PAIR}"
        )
        
        my_sig = tuple(
            self._check_equivalence(a, b, self.true_relation)
            for a, b in self.ALLOWED_PAIRS
        )
        relations = ["OE", "OR", "UE", "UD"]
        for other_rel in relations:
            if other_rel == self.true_relation:
                continue
            other_sig = tuple(
                self._check_equivalence(a, b, other_rel)
                for a, b in self.ALLOWED_PAIRS
            )
            if my_sig == other_sig:
                import warnings
                warnings.warn(
                    f"Query signature for {self.true_relation} is identical to {other_rel}: "
                    f"{my_sig}. Players cannot distinguish these two relations. "
                    f"Consider redesigning the tree or query pairs."
                )
        
        self._game_info = {}

    def _get_subtree_structure(self, node):
        if node not in self.TREE_STRUCTURE:
            return []
        children = self.TREE_STRUCTURE[node]
        return [self._get_subtree_structure(child) for child in children]

    def _check_equivalence_OE(self, node1, node2):
        struct1 = self._get_subtree_structure(node1)
        struct2 = self._get_subtree_structure(node2)
        return struct1 == struct2

    def _check_equivalence_OR(self, node1, node2):
        struct1 = self._get_subtree_structure(node1)
        struct2 = self._get_subtree_structure(node2)
        
        def compare_with_reversal(s1, s2):
            if len(s1) != len(s2):
                return False
            if all(compare_with_reversal(c1, c2) for c1, c2 in zip(s1, s2)):
                return True
            if all(compare_with_reversal(c1, c2) for c1, c2 in zip(s1, s2[::-1])):
                return True
            return False
        
        return compare_with_reversal(struct1, struct2)

    def _check_equivalence_UE(self, node1, node2):
        struct1 = self._get_subtree_structure(node1)
        struct2 = self._get_subtree_structure(node2)
        
        def to_comparable(s):
            return tuple(sorted([to_comparable(child) for child in s]))
        
        def compare_multiset(s1, s2):
            if len(s1) != len(s2):
                return False
            t1 = sorted([to_comparable(c) for c in s1])
            t2 = sorted([to_comparable(c) for c in s2])
            return t1 == t2
        
        return compare_multiset(struct1, struct2)

    def _check_equivalence_UD(self, node1, node2):
        struct1 = self._get_subtree_structure(node1)
        struct2 = self._get_subtree_structure(node2)
        
        def to_comparable(s):
            return tuple(sorted([to_comparable(child) for child in s]))
        
        def compare_set(s1, s2):
            set1 = set([to_comparable(c) for c in s1])
            set2 = set([to_comparable(c) for c in s2])
            return set1 == set2
        
        return compare_set(struct1, struct2)

    def _check_equivalence(self, node1, node2, relation):
        if relation == "OE":
            return self._check_equivalence_OE(node1, node2)
        elif relation == "OR":
            return self._check_equivalence_OR(node1, node2)
        elif relation == "UE":
            return self._check_equivalence_UE(node1, node2)
        elif relation == "UD":
            return self._check_equivalence_UD(node1, node2)
        else:
            raise ValueError(f"Unknown relation: {relation}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" in kv:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "relation" not in ans_dict or "result" not in ans_dict:
            return False
        
        if ans_dict["relation"] != self.true_relation:
            return False
        
        return ans_dict["result"] == self.target_result

    def get_all_possible_queries(self):
        results = []
        for node1, node2 in self.ALLOWED_PAIRS:
            query = f"<twin_check>{node1},{node2}</twin_check>"
            is_equivalent = self._check_equivalence(node1, node2, self.true_relation)
            
            if self.config.language == "zh":
                answer = "是" if is_equivalent else "否"
            else:
                answer = "Yes" if is_equivalent else "No"
            
            results.append({
                "query": query,
                "answer": answer
            })
        
        return results

    def _cf_core_produce(self, parsed_info):
        if "twin_check" in parsed_info:
            raw_query = parsed_info["twin_check"]
            
            try:
                parts = [x.strip() for x in raw_query.split(",")]
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                
                node1 = int(parts[0])
                node2 = int(parts[1])
                
                if (node1, node2) not in self.ALLOWED_PAIRS and (node2, node1) not in self.ALLOWED_PAIRS:
                    self.invalid_query_count += 1
                    if self.invalid_query_count >= 2:
                        if self.config.language == "zh":
                            self.state.set_state("failed", "累计无效询问次数达到2次")
                            return "游戏失败：累计无效询问次数达到2次。"
                        else:
                            self.state.set_state("failed", "2 invalid queries reached")
                            return "Game failed: 2 invalid queries reached."
                    
                    return "无效询问（请只询问证据板三对）" if self.config.language == "zh" else "Invalid query (please only query the three evidence pairs)"
                
                is_equivalent = self._check_equivalence(node1, node2, self.true_relation)
                
                if self.config.language == "zh":
                    return "是" if is_equivalent else "否"
                else:
                    return "Yes" if is_equivalent else "No"
                    
            except Exception as e:
                self.invalid_query_count += 1
                if self.invalid_query_count >= 2:
                    if self.config.language == "zh":
                        self.state.set_state("failed", "累计无效询问次数达到2次")
                        return "游戏失败：累计无效询问次数达到2次。"
                    else:
                        self.state.set_state("failed", "2 invalid queries reached")
                        return "Game failed: 2 invalid queries reached."
                
                return "错误：格式无效或节点错误。" if self.config.language == "zh" else "Error: Invalid format or nodes."
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"