from .base import Game
import random
import itertools

class SubsetResponseRuleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"子集响应规则"的推理游戏，规则如下：

游戏设定了一个集合 U，包含 {n} 个元素，分别编号为 1 到 {n}。其中有一个特殊元素 t = {t}（已告知）。我已秘密选定了：
1. 一个隐藏子集 S（S 是 U 的子集，可能包含也可能不包含 t）
2. 一个响应规则 r（从四种规则中选定，整个游戏过程保持不变）

四种响应规则的定义如下：
- r11：当且仅当"t 在 S 中"且"t 在你的查询中"时返回 1，否则返回 0
- r10：当且仅当"t 在 S 中"且"t 不在你的查询中"时返回 1，否则返回 0
- r01：当且仅当"t 不在 S 中"且"t 在你的查询中"时返回 1，否则返回 0
- r00：当且仅当"t 不在 S 中"且"t 不在你的查询中"时返回 1，否则返回 0

你的目标是通过尽可能少的查询，推断出：
1. 使用的是哪个响应规则（r11、r10、r01 或 r00）
2. 特殊元素 t 是否属于隐藏子集 S

你可以反复向我提交查询子集 Q（Q 是 U 的子集，可以包含任意元素，包括空集）。对于每次查询，我会根据固定的响应规则返回 0 或 1。

重要提示：
- 返回值仅取决于"t 是否在 S 中"和"t 是否在你的查询 Q 中"
- 查询中除 t 外的其他元素对返回值没有影响
- 你可以选择在查询中包含或不包含 t

提交查询子集时，使用以下 XML 格式（列出查询子集中的所有元素编号，用逗号分隔，可以为空）：

<query_subset>1,3,5</query_subset>

或查询空集：

<query_subset></query_subset>

提交最终答案时，必须同时说明响应规则和 t 是否在 S 中，格式如下：

<answer>rule=r11, t_in_S=yes</answer>

或

<answer>rule=r00, t_in_S=no</answer>

其中 rule 必须是 r11、r10、r01、r00 之一，t_in_S 必须是 yes 或 no。
"""

    game_rule_en = """\
Let's play a "Subset Response Rule" deduction game. Here are the rules:

There is a set U containing {n} elements, numbered from 1 to {n}. Among them, there is a special element t = {t} (already known to you). I have secretly chosen:
1. A hidden subset S (S is a subset of U, may or may not contain t)
2. A response rule r (selected from four rules, remains constant throughout the game)

The four response rules are defined as follows:
- r11: Returns 1 if and only if "t is in S" and "t is in your query", otherwise returns 0
- r10: Returns 1 if and only if "t is in S" and "t is not in your query", otherwise returns 0
- r01: Returns 1 if and only if "t is not in S" and "t is in your query", otherwise returns 0
- r00: Returns 1 if and only if "t is not in S" and "t is not in your query", otherwise returns 0

Your goal is to infer through as few queries as possible:
1. Which response rule is being used (r11, r10, r01, or r00)
2. Whether the special element t belongs to the hidden subset S

You can repeatedly submit query subsets Q (Q is a subset of U, can contain any elements, including the empty set). For each query, I will return 0 or 1 according to the fixed response rule.

Important notes:
- The return value depends only on "whether t is in S" and "whether t is in your query Q"
- Other elements in the query besides t have no effect on the return value
- You can choose to include or exclude t in your query

When submitting a query subset, use the following XML format (list all element IDs in the query subset, comma-separated, can be empty):

<query_subset>1,3,5</query_subset>

Or query the empty set:

<query_subset></query_subset>

When submitting the final answer, you must specify both the response rule and whether t is in S, using this format:

<answer>rule=r11, t_in_S=yes</answer>

or

<answer>rule=r00, t_in_S=no</answer>

where rule must be one of r11, r10, r01, r00, and t_in_S must be yes or no.
"""

    contextualized_rule_zh_1 = """\
这是一套城市交通路网的诊断系统。系统中包含 {n} 个关键路口，编号为 1 到 {n}。其中路口 t = {t}（已告知）是一个核心枢纽。我已秘密选定了：
1. 一个存在隐蔽故障的路口集合 S（S 是所有路口的子集，可能包含也可能不包含枢纽 t）
2. 系统的全局警报触发规则 r（从四种规则中选定，整个排查过程保持不变）

四种警报触发规则的定义如下：
- r11：当且仅当"枢纽 t 发生故障（在 S 中）"且"枢纽 t 被纳入你的诊断探针中"时返回 1，否则返回 0
- r10：当且仅当"枢纽 t 发生故障（在 S 中）"且"枢纽 t 未被纳入你的诊断探针中"时返回 1，否则返回 0
- r01：当且仅当"枢纽 t 运转正常（不在 S 中）"且"枢纽 t 被纳入你的诊断探针中"时返回 1，否则返回 0
- r00：当且仅当"枢纽 t 运转正常（不在 S 中）"且"枢纽 t 未被纳入你的诊断探针中"时返回 1，否则返回 0

你的目标是通过尽可能少的诊断查询，推断出：
1. 系统使用的是哪个警报触发规则（r11、r10、r01 或 r00）
2. 核心枢纽 t 是否属于故障路口集合 S

你可以反复向我提交诊断查询子集 Q（Q 是路口的子集，可以包含任意路口，包括空集）。对于每次查询，系统会根据固定的触发规则返回 0 或 1。

重要提示：
- 返回值仅取决于"枢纽 t 是否在故障集合 S 中"和"枢纽 t 是否在你的查询 Q 中"
- 查询中除 t 外的其他路口对返回值没有影响
- 你可以选择在查询探针中包含或不包含 t

提交诊断查询子集时，使用以下 XML 格式（列出探针中的所有路口编号，用逗号分隔，可以为空）：

<query_subset>1,3,5</query_subset>

或查询空集：

<query_subset></query_subset>

提交最终排查结论时，必须同时说明警报触发规则和 t 是否在 S 中，格式如下：

<answer>rule=r11, t_in_S=yes</answer>

或

<answer>rule=r00, t_in_S=no</answer>

其中 rule 必须是 r11、r10、r01、r00 之一，t_in_S 必须是 yes 或 no。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
This is a diagnostic system for an urban traffic network. The system contains {n} key intersections, numbered from 1 to {n}. Intersection t = {t} (already known) is a core traffic hub. I have secretly determined:
1. A hidden set of faulty intersections S (S is a subset of all intersections, may or may not contain hub t)
2. A global alarm trigger rule r (selected from four rules, remains constant throughout the diagnostic process)

The four alarm trigger rules are defined as follows:
- r11: Returns 1 if and only if "hub t is faulty (in S)" and "hub t is included in your diagnostic ping", otherwise returns 0
- r10: Returns 1 if and only if "hub t is faulty (in S)" and "hub t is not included in your diagnostic ping", otherwise returns 0
- r01: Returns 1 if and only if "hub t is functioning normally (not in S)" and "hub t is included in your diagnostic ping", otherwise returns 0
- r00: Returns 1 if and only if "hub t is functioning normally (not in S)" and "hub t is not included in your diagnostic ping", otherwise returns 0

Your goal is to infer through as few diagnostic queries as possible:
1. Which alarm trigger rule the system is using (r11, r10, r01, or r00)
2. Whether the core hub t belongs to the faulty intersection set S

You can repeatedly submit diagnostic query subsets Q (Q is a subset of intersections, can contain any intersections, including the empty set). For each query, the system will return 0 or 1 according to the fixed trigger rule.

Important notes:
- The return value depends only on "whether hub t is in the faulty set S" and "whether hub t is in your query Q"
- Other intersections in the query besides t have no effect on the return value
- You can choose to include or exclude t in your diagnostic ping

When submitting a diagnostic query subset, use the following XML format (list all intersection IDs in the ping, comma-separated, can be empty):

<query_subset>1,3,5</query_subset>

Or query the empty set:

<query_subset></query_subset>

When submitting the final diagnostic conclusion, you must specify both the alarm trigger rule and whether t is in S, using this format:

<answer>rule=r11, t_in_S=yes</answer>

or

<answer>rule=r00, t_in_S=no</answer>

where rule must be one of r11, r10, r01, r00, and t_in_S must be yes or no.
"""

    contextualized_rule_zh_2 = """\
这是一项针对罕见病的基因组筛查测试。样本中包含 {n} 个候选生物标志物，编号为 1 到 {n}。其中标志物 t = {t}（已告知）是关键靶标。我已秘密确定了：
1. 患者体内发生突变的标志物集合 S（S 是候选标志物的子集，可能包含也可能不包含靶标 t）
2. 检测试剂的显色反应规则 r（从四种规则中选定，整个检测过程保持不变）

四种显色反应规则的定义如下：
- r11：当且仅当"靶标 t 发生突变（在 S 中）"且"靶标 t 被纳入你的试剂检测池中"时返回 1（阳性显色），否则返回 0
- r10：当且仅当"靶标 t 发生突变（在 S 中）"且"靶标 t 未被纳入你的试剂检测池中"时返回 1，否则返回 0
- r01：当且仅当"靶标 t 未突变（不在 S 中）"且"靶标 t 被纳入你的试剂检测池中"时返回 1，否则返回 0
- r00：当且仅当"靶标 t 未突变（不在 S 中）"且"靶标 t 未被纳入你的试剂检测池中"时返回 1，否则返回 0

你的目标是通过尽可能少的检测查询，推断出：
1. 试剂使用的是哪种显色反应规则（r11、r10、r01 或 r00）
2. 关键靶标 t 是否属于突变标志物集合 S

你可以反复向我提交检测试剂池的标志物子集 Q（Q 是标志物的子集，可以包含任意靶标，包括空集）。对于每次检测，我会根据固定的反应规则返回 0 或 1。

重要提示：
- 返回值仅取决于"靶标 t 是否在突变集合 S 中"和"靶标 t 是否在你的检测池 Q 中"
- 检测池中除 t 外的其他标志物对反应结果没有影响
- 你可以选择在检测池中包含或不包含 t

提交检测池子集时，使用以下 XML 格式（列出检测池中的所有标志物编号，用逗号分隔，可以为空）：

<query_subset>1,3,5</query_subset>

或查询空集：

<query_subset></query_subset>

提交最终临床诊断结论时，必须同时说明显色规则和 t 是否在 S 中，格式如下：

<answer>rule=r11, t_in_S=yes</answer>

或

<answer>rule=r00, t_in_S=no</answer>

其中 rule 必须是 r11、r10、r01、r00 之一，t_in_S 必须是 yes 或 no。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
This is a genomic screening test for a rare disease. The sample contains {n} candidate biomarkers, numbered from 1 to {n}. Biomarker t = {t} (already known) is the primary target. I have secretly determined:
1. The set of mutated biomarkers in the patient S (S is a subset of candidate biomarkers, may or may not contain target t)
2. The colorimetric reaction rule of the assay r (selected from four rules, remains constant throughout the testing process)

The four colorimetric reaction rules are defined as follows:
- r11: Returns 1 (positive color) if and only if "target t is mutated (in S)" and "target t is included in your assay panel", otherwise returns 0
- r10: Returns 1 if and only if "target t is mutated (in S)" and "target t is not included in your assay panel", otherwise returns 0
- r01: Returns 1 if and only if "target t is not mutated (not in S)" and "target t is included in your assay panel", otherwise returns 0
- r00: Returns 1 if and only if "target t is not mutated (not in S)" and "target t is not included in your assay panel", otherwise returns 0

Your goal is to infer through as few test queries as possible:
1. Which colorimetric reaction rule the assay is using (r11, r10, r01, or r00)
2. Whether the primary target t belongs to the mutated biomarker set S

You can repeatedly submit assay panel subsets Q (Q is a subset of biomarkers, can contain any targets, including the empty set). For each test, I will return 0 or 1 according to the fixed reaction rule.

Important notes:
- The return value depends only on "whether target t is in the mutated set S" and "whether target t is in your assay panel Q"
- Other biomarkers in the panel besides t have no effect on the reaction result
- You can choose to include or exclude t in your assay panel

When submitting an assay panel subset, use the following XML format (list all biomarker IDs in the panel, comma-separated, can be empty):

<query_subset>1,3,5</query_subset>

Or query the empty set:

<query_subset></query_subset>

When submitting the final clinical diagnosis conclusion, you must specify both the reaction rule and whether t is in S, using this format:

<answer>rule=r11, t_in_S=yes</answer>

or

<answer>rule=r00, t_in_S=no</answer>

where rule must be one of r11, r10, r01, r00, and t_in_S must be yes or no.
"""

    contextualized_rule_zh_3 = """\
这是一个智能学情分析系统。题库涵盖了 {n} 个核心知识点，编号为 1 到 {n}。其中知识点 t = {t}（已告知）是本单元的重点难点。我已秘密锁定了：
1. 该学生尚未掌握的薄弱知识点集合 S（S 是总知识点的子集，可能包含也可能不包含重难点 t）
2. 系统自动评估的反馈信号规则 r（从四种规则中选定，整个测验过程保持不变）

四种反馈信号规则的定义如下：
- r11：当且仅当"重难点 t 尚未掌握（在 S 中）"且"重难点 t 被纳入你的生成测试卷中"时系统返回 1（发出警告），否则返回 0
- r10：当且仅当"重难点 t 尚未掌握（在 S 中）"且"重难点 t 未被纳入你的生成测试卷中"时返回 1，否则返回 0
- r01：当且仅当"重难点 t 已掌握（不在 S 中）"且"重难点 t 被纳入你的生成测试卷中"时返回 1，否则返回 0
- r00：当且仅当"重难点 t 已掌握（不在 S 中）"且"重难点 t 未被纳入你的生成测试卷中"时返回 1，否则返回 0

你的目标是通过尽可能少的组卷查询，推断出：
1. 系统使用的是哪种反馈信号规则（r11、r10、r01 或 r00）
2. 重难点 t 是否属于薄弱知识点集合 S

你可以反复向我提交测试卷覆盖的知识点子集 Q（Q 是知识点的子集，可以包含任意知识点，包括空集）。对于每次测验，系统会根据固定的反馈规则返回 0 或 1。

重要提示：
- 返回值仅取决于"知识点 t 是否在薄弱集合 S 中"和"知识点 t 是否在你的测试卷 Q 中"
- 测试卷中除 t 外的其他知识点对反馈结果没有影响
- 你可以选择在试卷中包含或不包含知识点 t

提交测试卷子集时，使用以下 XML 格式（列出测试卷中的所有知识点编号，用逗号分隔，可以为空）：

<query_subset>1,3,5</query_subset>

或查询空集：

<query_subset></query_subset>

提交最终学情报告时，必须同时说明评估规则和 t 是否在 S 中，格式如下：

<answer>rule=r11, t_in_S=yes</answer>

或

<answer>rule=r00, t_in_S=no</answer>

其中 rule 必须是 r11、r10、r01、r00 之一，t_in_S 必须是 yes 或 no。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is an intelligent learning analysis system. The question bank covers {n} core knowledge points, numbered from 1 to {n}. Knowledge point t = {t} (already known) is the key difficulty of this unit. I have secretly locked in:
1. The set of weak knowledge points S that the student has not mastered (S is a subset of all knowledge points, may or may not contain difficulty t)
2. The feedback signal rule r for the system's automated assessment (selected from four rules, remains constant throughout the testing process)

The four feedback signal rules are defined as follows:
- r11: Returns 1 (warning triggered) if and only if "difficulty t is not mastered (in S)" and "difficulty t is included in your generated test paper", otherwise returns 0
- r10: Returns 1 if and only if "difficulty t is not mastered (in S)" and "difficulty t is not included in your generated test paper", otherwise returns 0
- r01: Returns 1 if and only if "difficulty t is mastered (not in S)" and "difficulty t is included in your generated test paper", otherwise returns 0
- r00: Returns 1 if and only if "difficulty t is mastered (not in S)" and "difficulty t is not included in your generated test paper", otherwise returns 0

Your goal is to infer through as few test generation queries as possible:
1. Which feedback signal rule the system is using (r11, r10, r01, or r00)
2. Whether the key difficulty t belongs to the weak knowledge point set S

You can repeatedly submit knowledge point subsets Q covered by the test paper (Q is a subset of knowledge points, can contain any points, including the empty set). For each test, the system will return 0 or 1 according to the fixed feedback rule.

Important notes:
- The return value depends only on "whether knowledge point t is in the weak set S" and "whether knowledge point t is in your test paper Q"
- Other knowledge points in the test besides t have no effect on the feedback result
- You can choose to include or exclude knowledge point t in the test

When submitting a test paper subset, use the following XML format (list all knowledge point IDs in the test, comma-separated, can be empty):

<query_subset>1,3,5</query_subset>

Or query the empty set:

<query_subset></query_subset>

When submitting the final learning analysis report, you must specify both the assessment rule and whether t is in S, using this format:

<answer>rule=r11, t_in_S=yes</answer>

or

<answer>rule=r00, t_in_S=no</answer>

where rule must be one of r11, r10, r01, r00, and t_in_S must be yes or no.
"""

    contextualized_rule_zh_4 = """\
这是高精密装配线的自动化质检系统。当前批次包含 {n} 个核心零部件，编号为 1 到 {n}。其中部件 t = {t}（已告知）是主控芯片模块。我已秘密设定了：
1. 存在制造缺陷的零部件集合 S（S 是所有部件的子集，可能包含也可能不包含主控芯片 t）
2. 质检压力舱的报警响应规则 r（从四种规则中选定，整个质检过程保持不变）

四种报警响应规则的定义如下：
- r11：当且仅当"主控芯片 t 存在缺陷（在 S 中）"且"主控芯片 t 被送入压力测试舱中"时返回 1（触发警报），否则返回 0
- r10：当且仅当"主控芯片 t 存在缺陷（在 S 中）"且"主控芯片 t 未被送入压力测试舱中"时返回 1，否则返回 0
- r01：当且仅当"主控芯片 t 完好无损（不在 S 中）"且"主控芯片 t 被送入压力测试舱中"时返回 1，否则返回 0
- r00：当且仅当"主控芯片 t 完好无损（不在 S 中）"且"主控芯片 t 未被送入压力测试舱中"时返回 1，否则返回 0

你的目标是通过尽可能少的抽检查询，推断出：
1. 压力舱使用的是哪种报警响应规则（r11、r10、r01 或 r00）
2. 主控芯片模块 t 是否属于缺陷部件集合 S

你可以反复向我提交送入测试舱的零部件子集 Q（Q 是部件的子集，可以包含任意零部件，包括空集）。对于每次测试，系统会根据固定的响应规则返回 0 或 1。

重要提示：
- 返回值仅取决于"芯片 t 是否在缺陷集合 S 中"和"芯片 t 是否在你的测试舱 Q 中"
- 测试舱中除 t 外的其他部件对报警结果没有影响
- 你可以选择在压力舱中放入或不放入部件 t

提交压力舱子集时，使用以下 XML 格式（列出放入测试舱的所有部件编号，用逗号分隔，可以为空）：

<query_subset>1,3,5</query_subset>

或查询空集：

<query_subset></query_subset>

提交最终批次质检结论时，必须同时说明报警响应规则和 t 是否在 S 中，格式如下：

<answer>rule=r11, t_in_S=yes</answer>

或

<answer>rule=r00, t_in_S=no</answer>

其中 rule 必须是 r11、r10、r01、r00 之一，t_in_S 必须是 yes 或 no。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
This is an automated quality inspection system for a high-precision assembly line. The current batch contains {n} core components, numbered from 1 to {n}. Component t = {t} (already known) is the main control chip module. I have secretly set:
1. The set of defective components S (S is a subset of all components, may or may not contain the main control chip t)
2. The alarm response rule r of the stress testing chamber (selected from four rules, remains constant throughout the inspection process)

The four alarm response rules are defined as follows:
- r11: Returns 1 (triggers alarm) if and only if "control chip t is defective (in S)" and "control chip t is loaded into the stress test chamber", otherwise returns 0
- r10: Returns 1 if and only if "control chip t is defective (in S)" and "control chip t is not loaded into the stress test chamber", otherwise returns 0
- r01: Returns 1 if and only if "control chip t is intact (not in S)" and "control chip t is loaded into the stress test chamber", otherwise returns 0
- r00: Returns 1 if and only if "control chip t is intact (not in S)" and "control chip t is not loaded into the stress test chamber", otherwise returns 0

Your goal is to infer through as few sampling queries as possible:
1. Which alarm response rule the stress chamber is using (r11, r10, r01, or r00)
2. Whether the main control chip module t belongs to the defective component set S

You can repeatedly submit component subsets Q loaded into the test chamber (Q is a subset of components, can contain any components, including the empty set). For each test, the system will return 0 or 1 according to the fixed response rule.

Important notes:
- The return value depends only on "whether chip t is in the defective set S" and "whether chip t is in your test chamber Q"
- Other components in the chamber besides t have no effect on the alarm result
- You can choose to load or not load component t into the stress chamber

When submitting a stress chamber subset, use the following XML format (list all component IDs loaded into the test chamber, comma-separated, can be empty):

<query_subset>1,3,5</query_subset>

Or query the empty set:

<query_subset></query_subset>

When submitting the final batch inspection conclusion, you must specify both the alarm response rule and whether t is in S, using this format:

<answer>rule=r11, t_in_S=yes</answer>

or

<answer>rule=r00, t_in_S=no</answer>

where rule must be one of r11, r10, r01, r00, and t_in_S must be yes or no.
"""

    contextualized_rule_zh_5 = """\
这是一个用于金融反欺诈调查的算法审计系统。案卷中包含 {n} 份关键财务文件，编号为 1 到 {n}。其中文件 t = {t}（已告知）是核心往来账目。我已秘密确定了：
1. 存在数据篡改的伪造文件集合 S（S 是所有文件的子集，可能包含也可能不包含核心账目 t）
2. 算法审计的异常触发规则 r（从四种规则中选定，整个审查过程保持不变）

四种异常触发规则的定义如下：
- r11：当且仅当"核心账目 t 被篡改（在 S 中）"且"核心账目 t 被提交给审计模型"时返回 1（标记异常），否则返回 0
- r10：当且仅当"核心账目 t 被篡改（在 S 中）"且"核心账目 t 未被提交给审计模型"时返回 1，否则返回 0
- r01：当且仅当"核心账目 t 无伪造（不在 S 中）"且"核心账目 t 被提交给审计模型"时返回 1，否则返回 0
- r00：当且仅当"核心账目 t 无伪造（不在 S 中）"且"核心账目 t 未被提交给审计模型"时返回 1，否则返回 0

你的目标是通过尽可能少的提取查询，推断出：
1. 审计系统使用的是哪种异常触发规则（r11、r10、r01 或 r00）
2. 核心账目文件 t 是否属于篡改文件集合 S

你可以反复向我提交送审的文件子集 Q（Q 是文件的子集，可以包含任意财务案卷，包括空集）。对于每次审查，系统会根据固定的触发规则返回 0 或 1。

重要提示：
- 返回值仅取决于"账目 t 是否在篡改集合 S 中"和"账目 t 是否在你的送审卷宗 Q 中"
- 送审卷宗中除 t 外的其他文件对异常标记结果没有影响
- 你可以选择在审计子集中包含或不包含账目 t

提交送审文件子集时，使用以下 XML 格式（列出提交给审计模型的所有文件编号，用逗号分隔，可以为空）：

<query_subset>1,3,5</query_subset>

或查询空集：

<query_subset></query_subset>

提交最终司法审查结论时，必须同时说明触发规则和 t 是否在 S 中，格式如下：

<answer>rule=r11, t_in_S=yes</answer>

或

<answer>rule=r00, t_in_S=no</answer>

其中 rule 必须是 r11、r10、r01、r00 之一，t_in_S 必须是 yes 或 no。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
This is an algorithmic auditing system for financial anti-fraud investigation. The case file contains {n} key financial documents, numbered from 1 to {n}. Document t = {t} (already known) is the core transaction ledger. I have secretly determined:
1. The set of forged documents with tampered data S (S is a subset of all documents, may or may not contain the core ledger t)
2. The anomaly trigger rule r of the algorithmic audit (selected from four rules, remains constant throughout the review process)

The four anomaly trigger rules are defined as follows:
- r11: Returns 1 (flags anomaly) if and only if "core ledger t is tampered (in S)" and "core ledger t is submitted to the audit model", otherwise returns 0
- r10: Returns 1 if and only if "core ledger t is tampered (in S)" and "core ledger t is not submitted to the audit model", otherwise returns 0
- r01: Returns 1 if and only if "core ledger t is authentic (not in S)" and "core ledger t is submitted to the audit model", otherwise returns 0
- r00: Returns 1 if and only if "core ledger t is authentic (not in S)" and "core ledger t is not submitted to the audit model", otherwise returns 0

Your goal is to infer through as few extraction queries as possible:
1. Which anomaly trigger rule the audit system is using (r11, r10, r01, or r00)
2. Whether the core ledger document t belongs to the tampered document set S

You can repeatedly submit document subsets Q for audit (Q is a subset of documents, can contain any financial files, including the empty set). For each review, the system will return 0 or 1 according to the fixed trigger rule.

Important notes:
- The return value depends only on "whether ledger t is in the tampered set S" and "whether ledger t is in your submitted dossier Q"
- Other documents in the submission besides t have no effect on the anomaly flagging result
- You can choose to include or exclude ledger t in the audit subset

When submitting a document subset for audit, use the following XML format (list all document IDs submitted to the audit model, comma-separated, can be empty):

<query_subset>1,3,5</query_subset>

Or query the empty set:

<query_subset></query_subset>

When submitting the final forensic review conclusion, you must specify both the trigger rule and whether t is in S, using this format:

<answer>rule=r11, t_in_S=yes</answer>

or

<answer>rule=r00, t_in_S=no</answer>

where rule must be one of r11, r10, r01, r00, and t_in_S must be yes or no.
"""

    tags = ["answer", "query_subset"]

    reasoning_type = "溯因推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "t": 3,
                "S": [1, 2],
                "rule": "r00",
            },
            2: {
                "n": 8,
                "t": 4,
                "S": [2, 4, 6],
                "rule": "r11",
            },
            3: {
                "n": 10,
                "t": 5,
                "S": [1, 3, 7, 9],
                "rule": "r01",
            },
            4: {
                "n": 12,
                "t": 7,
                "S": [3, 5, 7, 9, 11],
                "rule": "r10",
            },
            5: {
                "n": 15,
                "t": 9,
                "S": [2, 4, 6, 8, 10, 12],
                "rule": "r00",
            },
        },
        "en": {
            1: {
                "n": 5,
                "t": 3,
                "S": [1, 2],
                "rule": "r00",
            },
            2: {
                "n": 8,
                "t": 4,
                "S": [2, 4, 6],
                "rule": "r11",
            },
            3: {
                "n": 10,
                "t": 5,
                "S": [1, 3, 7, 9],
                "rule": "r01",
            },
            4: {
                "n": 12,
                "t": 7,
                "S": [3, 5, 7, 9, 11],
                "rule": "r10",
            },
            5: {
                "n": 15,
                "t": 9,
                "S": [2, 4, 6, 8, 10, 12],
                "rule": "r00",
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
        self._game_info["t"] = cfg["t"]
        
        self.hidden_subset_S = set(cfg["S"])
        self.special_element_t = cfg["t"]
        self.response_rule = cfg["rule"]
        
        self.s = 1 if self.special_element_t in self.hidden_subset_S else 0

    def _compute_response(self, query_set):
        q = 1 if self.special_element_t in query_set else 0
        
        if self.response_rule == "r11":
            return 1 if (self.s == 1 and q == 1) else 0
        elif self.response_rule == "r10":
            return 1 if (self.s == 1 and q == 0) else 0
        elif self.response_rule == "r01":
            return 1 if (self.s == 0 and q == 1) else 0
        elif self.response_rule == "r00":
            return 1 if (self.s == 0 and q == 0) else 0
        else:
            raise ValueError(f"Unknown rule: {self.response_rule}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "rule" not in ans_dict or "t_in_S" not in ans_dict:
            return False
        
        if ans_dict["rule"] != self.response_rule:
            return False
        
        player_t_in_S = ans_dict["t_in_S"].lower()
        if player_t_in_S not in ["yes", "no"]:
            return False
        
        correct_t_in_S = "yes" if self.s == 1 else "no"
        if player_t_in_S != correct_t_in_S:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "query_subset" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."
        
        raw_query = parsed_info["query_subset"].strip()
        
        if not raw_query:
            query_set = set()
        else:
            try:
                elements = [int(x.strip()) for x in raw_query.split(",") if x.strip()]
                query_set = set(elements)
                
                n = self._game_info["n"]
                for elem in query_set:
                    if elem < 1 or elem > n:
                        if self.config.language == "zh":
                            return f"错误：元素 {elem} 超出有效范围 [1, {n}]。"
                        else:
                            return f"Error: Element {elem} is out of valid range [1, {n}]."
            except ValueError:
                if self.config.language == "zh":
                    return "错误：查询格式无效，请使用逗号分隔的数字。"
                else:
                    return "Error: Invalid query format, please use comma-separated numbers."
        
        response = self._compute_response(query_set)
        return str(response)

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        t = self.special_element_t

        query_with_t = str(t)
        ans_with_t = str(self._compute_response({t}))
        queries.append({
            "query": f"<query_subset>{query_with_t}</query_subset>",
            "answer": ans_with_t
        })

        ans_without_t = str(self._compute_response(set()))
        queries.append({
            "query": "<query_subset></query_subset>",
            "answer": ans_without_t
        })

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct == "0":
            return "1"
        if correct == "1":
            return "0"
        
        lower_correct = correct.lower()
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            if "yes" in lower_correct:
                if correct == "Yes": return "No"
                if correct == "YES": return "NO"
                if correct == "yes": return "no"
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            if "no" in lower_correct:
                if correct == "No": return "Yes"
                if correct == "NO": return "YES"
                if correct == "no": return "yes"
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        return correct + "_WRONG"