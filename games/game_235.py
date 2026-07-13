# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   子集包含：某子集是否完全被另一子集包含
# ============================================================

from .base import Game
import re
import itertools


class SubsetRuleIdentificationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"包含关系假设识别"的推理游戏，规则如下：

游戏设定了一个全集 U = {{1, 2, 3, 4, 5, 6}}，包含 6 个不同的元素。我已秘密选定了一个非空真子集 M（M 是 U 的子集，且 M 不为空也不等于 U），并选择了一个判定规则 R。规则 R 从以下四种候选中选出：

1. R1：当且仅当你提交的集合 Q 是 M 的子集时接受
2. R2：当且仅当 M 是你提交的集合 Q 的子集时接受
3. R3：当且仅当你提交的集合 Q 是 M 的补集的子集时接受
4. R4：当且仅当你提交的集合 Q 恰好等于 M 时接受

你的目标是通过试探性提交不同的子集来推断出真实的规则 R 以及隐藏的集合 M，然后构造一个能被该规则接受的最终子集。

你可以进行以下两类操作：

1. 试询：提交一个子集 Q（可以是空集、全集或任意子集），我会告诉你该子集是"接受"还是"拒绝"。
2. 终局宣告：当你认为已经收集足够信息后，同时提交你识别出的规则类型（R1/R2/R3/R4）和一个最终子集 Q*。

注意：你必须至少进行 3 次试询后才能进行终局宣告，否则游戏失败。

## 询问与提交答案的格式（必须严格遵守）

- 试询（例如查询子集 {{1,3,5}}）：
<query_subset>1,3,5</query_subset>

- 试询空集：
<query_subset></query_subset>

- 终局宣告（例如识别规则为 R1，最终子集为 {{2,4}}）：
<answer>rule=R1, subset=2,4</answer>

- 终局宣告最终子集为空集：
<answer>rule=R2, subset=</answer>

成功条件：在至少 3 次试询后，正确识别规则类型，且提交的最终子集能被该规则接受。
"""

    game_rule_en = """\
Let's play a "Subset Rule Identification" deduction game. Here are the rules:

The game defines a universe U = {{1, 2, 3, 4, 5, 6}} containing 6 distinct elements. I have secretly selected a non-empty proper subset M (M is a subset of U, where M is neither empty nor equal to U), and chosen a judgment rule R. Rule R is selected from the following four candidates:

1. R1: Accept if and only if your submitted set Q is a subset of M
2. R2: Accept if and only if M is a subset of your submitted set Q
3. R3: Accept if and only if your submitted set Q is a subset of the complement of M
4. R4: Accept if and only if your submitted set Q equals M exactly

Your goal is to infer the true rule R and the hidden set M through exploratory submissions of different subsets, then construct a final subset that can be accepted by the rule.

You can perform the following two types of operations:

1. Query: Submit a subset Q (can be empty set, full set, or any subset), and I will tell you whether it is "Accept" or "Reject".
2. Final Declaration: When you believe you have collected sufficient information, simultaneously submit the rule type you identified (R1/R2/R3/R4) and a final subset Q*.

Note: You must perform at least 3 queries before making a final declaration, otherwise the game fails.

## Query and Answer Format (must strictly follow)

- Query (e.g., querying subset {{1,3,5}}):
<query_subset>1,3,5</query_subset>

- Query empty set:
<query_subset></query_subset>

- Final Declaration (e.g., identifying rule as R1, final subset as {{2,4}}):
<answer>rule=R1, subset=2,4</answer>

- Final Declaration with empty final subset:
<answer>rule=R2, subset=</answer>

Success condition: After at least 3 queries, correctly identify the rule type and submit a final subset that is accepted by the rule.
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎接入“城市交通枢纽智能管控”系统。我们现在进行一项通行规则与重点管控区域的推断测试。

系统设定了一个城市核心交通网络 U = {{1, 2, 3, 4, 5, 6}}，包含 6 个关键交通枢纽。目前交管部门已秘密划定了一个非空且非全集的重点监控枢纽集合 M，并启动了某种通行许可规则 R。规则 R 从以下四种管控策略中选出：

1. R1（内控策略）：当且仅当你提交的巡逻计划 Q 完全在重点监控枢纽 M 范围内时，系统予以接受。
2. R2（覆盖策略）：当且仅当重点监控枢纽 M 被你提交的巡逻计划 Q 完全包含时，系统予以接受。
3. R3（规避策略）：当且仅当你提交的巡逻计划 Q 完全避开重点监控枢纽 M 时，系统予以接受。
4. R4（精准策略）：当且仅当你提交的巡逻计划 Q 恰好等于重点监控枢纽集合 M 时，系统予以接受。

你的目标是通过试探性提交不同的巡逻计划 Q 来推断出真实的通行规则 R 以及隐藏的监控枢纽集合 M，最终构造一个能被该规则接受的有效巡逻计划。

你可以进行以下两类操作：
1. 试询：提交一个巡逻计划枢纽集合 Q（可以是空集、全集或任意子集），系统会反馈“接受”或“拒绝”。
2. 终局宣告：当你认为已掌握足够信息后，同时提交你识别出的规则类型（R1/R2/R3/R4）和一个最终巡逻计划 Q*。

注意：你必须至少进行 3 次试询后才能进行终局宣告，否则测试将被判定为不合格。

## 询问与提交答案的格式（必须严格遵守）

- 试询（例如查询枢纽 {{1,3,5}}）：
<query_subset>1,3,5</query_subset>

- 试询空集：
<query_subset></query_subset>

- 终局宣告（例如识别规则为 R1，最终计划包含枢纽 {{2,4}}）：
<answer>rule=R1, subset=2,4</answer>

- 终局宣告最终计划为空集：
<answer>rule=R2, subset=</answer>

成功条件：在至少 3 次试询后，正确识别规则类型，且提交的最终巡逻计划能被该管控规则接受。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Hub Intelligent Control" system. We are now conducting a deduction test on traffic rules and key control areas.

The system defines a core urban traffic network U = {{1, 2, 3, 4, 5, 6}}, containing 6 key traffic hubs. The traffic management department has secretly designated a non-empty proper subset M as the key monitoring hub set, and activated a certain pass permission rule R. Rule R is selected from the following four control strategies:

1. R1 (Internal Control Strategy): Accept if and only if your submitted patrol plan Q is a subset of the monitoring set M.
2. R2 (Coverage Strategy): Accept if and only if the monitoring set M is a subset of your submitted patrol plan Q.
3. R3 (Evasion Strategy): Accept if and only if your submitted patrol plan Q is a subset of the complement of M (completely avoiding M).
4. R4 (Precise Strategy): Accept if and only if your submitted patrol plan Q equals M exactly.

Your goal is to infer the true rule R and the hidden hub set M through exploratory submissions of different patrol plans Q, then construct a final plan that can be accepted by the rule.

You can perform the following two types of operations:
1. Query: Submit a patrol plan hub set Q (can be empty set, full set, or any subset), and the system will feedback "Accept" or "Reject".
2. Final Declaration: When you believe you have collected sufficient information, simultaneously submit the rule type you identified (R1/R2/R3/R4) and a final patrol plan Q*.

Note: You must perform at least 3 queries before making a final declaration, otherwise the test fails.

## Query and Answer Format (must strictly follow)

- Query (e.g., querying hubs {{1,3,5}}):
<query_subset>1,3,5</query_subset>

- Query empty set:
<query_subset></query_subset>

- Final Declaration (e.g., identifying rule as R1, final plan as {{2,4}}):
<answer>rule=R1, subset=2,4</answer>

- Final Declaration with empty final plan:
<answer>rule=R2, subset=</answer>

Success condition: After at least 3 queries, correctly identify the rule type and submit a final patrol plan that is accepted by the control rule.
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎进入“靶向药物联合用药”分析系统。我们现在来进行一项药物交互作用的推断分析。

系统设定了一个备选药物库 U = {{1, 2, 3, 4, 5, 6}}，包含 6 种靶向药物。研究中心已秘密发现了一个非空且非全集的特定交互药物组合 M，并设定了药物联合生效的判定规则 R。规则 R 从以下四种药理机制中选出：

1. R1（保守用药）：当且仅当你提交的测试用药方案 Q 完全属于交互组合 M 时，系统判定为安全接受。
2. R2（全面覆盖）：当且仅当交互组合 M 被你提交的测试用药方案 Q 完全包含时，系统判定为有效接受。
3. R3（脱敏避开）：当且仅当你提交的测试用药方案 Q 完全避开交互组合 M 中的任何药物时，系统判定为安全接受。
4. R4（靶向匹配）：当且仅当你提交的测试用药方案 Q 恰好等于交互组合 M 时，系统判定为精准接受。

你的目标是通过试探性提交不同的用药方案 Q 来推断出真实的生效规则 R 以及隐藏的交互组合 M，最终开具一个能被该规则接受的最终处方。

你可以进行以下两类操作：
1. 试询：提交一个用药方案 Q（可以是空集、全集或任意组合），系统会反馈“接受”或“拒绝”。
2. 终局宣告：当你认为已掌握足够信息后，同时提交你识别出的规则类型（R1/R2/R3/R4）和一个最终处方 Q*。

注意：你必须至少进行 3 次试询后才能进行终局宣告，否则分析将被判定为失败。

## 询问与提交答案的格式（必须严格遵守）

- 试询（例如查询药物组合 {{1,3,5}}）：
<query_subset>1,3,5</query_subset>

- 试询空处方：
<query_subset></query_subset>

- 终局宣告（例如识别规则为 R1，最终处方为 {{2,4}}）：
<answer>rule=R1, subset=2,4</answer>

- 终局宣告最终处方为空：
<answer>rule=R2, subset=</answer>

成功条件：在至少 3 次试询后，正确识别规则类型，且提交的最终处方能被该药理规则接受。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Targeted Drug Combination" analysis system. We are now conducting a deductive analysis of drug interactions.

The system defines an alternative drug library U = {{1, 2, 3, 4, 5, 6}}, containing 6 targeted drugs. The research center has secretly discovered a non-empty proper subset M representing a specific interacting drug combination, and established a judgment rule R for the efficacy of the combination. Rule R is selected from the following four pharmacological mechanisms:

1. R1 (Conservative Medication): Accept if and only if your submitted test prescription Q is a subset of the interacting combination M.
2. R2 (Comprehensive Coverage): Accept if and only if the interacting combination M is a subset of your submitted test prescription Q.
3. R3 (Desensitization Evasion): Accept if and only if your submitted test prescription Q is a subset of the complement of M (completely avoiding M).
4. R4 (Targeted Matching): Accept if and only if your submitted test prescription Q equals M exactly.

Your goal is to infer the true rule R and the hidden interacting combination M through exploratory submissions of different test prescriptions Q, then issue a final prescription that can be accepted by the rule.

You can perform the following two types of operations:
1. Query: Submit a test prescription Q (can be empty set, full set, or any subset), and the system will feedback "Accept" or "Reject".
2. Final Declaration: When you believe you have collected sufficient information, simultaneously submit the rule type you identified (R1/R2/R3/R4) and a final prescription Q*.

Note: You must perform at least 3 queries before making a final declaration, otherwise the analysis fails.

## Query and Answer Format (must strictly follow)

- Query (e.g., querying drug combination {{1,3,5}}):
<query_subset>1,3,5</query_subset>

- Query empty prescription:
<query_subset></query_subset>

- Final Declaration (e.g., identifying rule as R1, final prescription as {{2,4}}):
<answer>rule=R1, subset=2,4</answer>

- Final Declaration with empty final prescription:
<answer>rule=R2, subset=</answer>

Success condition: After at least 3 queries, correctly identify the rule type and submit a final prescription that is accepted by the pharmacological rule.
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎进入“学生核心素养考核与选课”评估系统。我们现在来进行一项专业课程要求的推断游戏。

系统设定了一个选修课程池 U = {{1, 2, 3, 4, 5, 6}}，包含 6 门不同课程。教务处已秘密设定了一个非空且非全集的重点必修先导课程集合 M，并为毕业资格审核制定了规则 R。规则 R 从以下四种考核标准中选出：

1. R1（基础深造）：当且仅当你提交的选课方案 Q 完全属于先导课程集合 M 时，系统审核接受。
2. R2（全面达标）：当且仅当先导课程集合 M 被你提交的选课方案 Q 完全包含时，系统审核接受。
3. R3（拓宽视野）：当且仅当你提交的选课方案 Q 完全避开先导课程集合 M（即仅选修其他通识课）时，系统审核接受。
4. R4（精确修读）：当且仅当你提交的选课方案 Q 恰好等于先导课程集合 M 时，系统审核接受。

你的目标是通过试探性提交不同的选课方案 Q 来推断出真实的审核规则 R 以及隐藏的先导课程集合 M，最终制定一份能通过审核的最终选课方案。

你可以进行以下两类操作：
1. 试询：提交一个选课方案 Q（可以是空集、全选或任意组合），系统会反馈“接受”或“拒绝”。
2. 终局宣告：当你认为已掌握足够信息后，同时提交你识别出的规则类型（R1/R2/R3/R4）和一个最终选课方案 Q*。

注意：你必须至少进行 3 次试询后才能进行终局宣告，否则评估将失败。

## 询问与提交答案的格式（必须严格遵守）

- 试询（例如查询选课方案 {{1,3,5}}）：
<query_subset>1,3,5</query_subset>

- 试询未选任何课：
<query_subset></query_subset>

- 终局宣告（例如识别规则为 R1，最终选课方案为 {{2,4}}）：
<answer>rule=R1, subset=2,4</answer>

- 终局宣告最终方案为不选课：
<answer>rule=R2, subset=</answer>

成功条件：在至少 3 次试询后，正确识别规则类型，且提交的最终选课方案能被审核规则接受。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Student Core Competency Assessment and Course Selection" system. We are now playing a deduction game on major course requirements.

The system defines an elective course pool U = {{1, 2, 3, 4, 5, 6}}, containing 6 different courses. The academic affairs office has secretly established a non-empty proper subset M representing the key prerequisite course set, and formulated a rule R for graduation qualification review. Rule R is selected from the following four assessment standards:

1. R1 (Foundational Study): Accept if and only if your submitted course selection Q is a subset of the prerequisite course set M.
2. R2 (Comprehensive Standard): Accept if and only if the prerequisite course set M is a subset of your submitted course selection Q.
3. R3 (Broadening Horizons): Accept if and only if your submitted course selection Q is a subset of the complement of M (completely avoiding M).
4. R4 (Precise Enrollment): Accept if and only if your submitted course selection Q equals M exactly.

Your goal is to infer the true rule R and the hidden prerequisite course set M through exploratory submissions of different course selections Q, then formulate a final course selection plan that passes the review.

You can perform the following two types of operations:
1. Query: Submit a course selection Q (can be empty set, full set, or any subset), and the system will feedback "Accept" or "Reject".
2. Final Declaration: When you believe you have collected sufficient information, simultaneously submit the rule type you identified (R1/R2/R3/R4) and a final course selection Q*.

Note: You must perform at least 3 queries before making a final declaration, otherwise the assessment fails.

## Query and Answer Format (must strictly follow)

- Query (e.g., querying courses {{1,3,5}}):
<query_subset>1,3,5</query_subset>

- Query empty selection:
<query_subset></query_subset>

- Final Declaration (e.g., identifying rule as R1, final course selection as {{2,4}}):
<answer>rule=R1, subset=2,4</answer>

- Final Declaration with empty final selection:
<answer>rule=R2, subset=</answer>

Success condition: After at least 3 queries, correctly identify the rule type and submit a final course selection that is accepted by the review rule.
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎使用“精密流水线质检流程”分析仪。我们现在进行一项关于核心缺陷检测规则的排查任务。

系统监控着一条拥有全集 U = {{1, 2, 3, 4, 5, 6}}（代表 6 个标准检测工序）的生产线。质量工程师已秘密圈定了一个非空且非全集的核心缺陷易发工序集合 M，并配置了质检放行规则 R。规则 R 从以下四种检验标准中选出：

1. R1（重点抽检）：当且仅当你提交的抽检计划 Q 仅包含易发工序（属于 M）时，系统接受方案。
2. R2（全覆盖抽检）：当且仅当核心易发工序集合 M 被你提交的抽检计划 Q 完全覆盖时，系统接受方案。
3. R3（常规避开）：当且仅当你提交的抽检计划 Q 仅针对非易发工序（完全避开 M）时，系统接受方案。
4. R4（精准对标）：当且仅当你提交的抽检计划 Q 与易发工序集合 M 完全对应时，系统接受方案。

你的目标是通过试探性提交不同的抽检计划 Q 来推断出真实的放行规则 R 以及隐藏的易发工序集合 M，最终输出一个能被规则通过的标准抽检计划。

你可以进行以下两类操作：
1. 试询：提交一个抽检计划 Q（可以是空集、全工序或任意组合），系统会反馈“接受”或“拒绝”。
2. 终局宣告：当你认为已掌握足够信息后，同时提交你识别出的规则类型（R1/R2/R3/R4）和一个最终抽检计划 Q*。

注意：你必须至少进行 3 次试询后才能进行终局宣告，否则排查任务将被强制终止。

## 询问与提交答案的格式（必须严格遵守）

- 试询（例如查询工序 {{1,3,5}}）：
<query_subset>1,3,5</query_subset>

- 试询空工序：
<query_subset></query_subset>

- 终局宣告（例如识别规则为 R1，最终计划为 {{2,4}}）：
<answer>rule=R1, subset=2,4</answer>

- 终局宣告最终计划为空：
<answer>rule=R2, subset=</answer>

成功条件：在至少 3 次试询后，正确识别规则类型，且提交的最终抽检计划能被质检系统接受。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Precision Assembly Line Quality Inspection" analyzer. We are now conducting a troubleshooting task regarding core defect detection rules.

The system monitors a production line with a universal set U = {{1, 2, 3, 4, 5, 6}} representing 6 standard inspection processes. Quality engineers have secretly pinpointed a non-empty proper subset M representing the core defect-prone processes, and configured a quality release rule R. Rule R is selected from the following four inspection standards:

1. R1 (Focused Sampling): Accept if and only if your submitted sampling plan Q is a subset of the defect-prone processes M.
2. R2 (Full Coverage Sampling): Accept if and only if the core defect-prone process set M is a subset of your submitted sampling plan Q.
3. R3 (Routine Evasion): Accept if and only if your submitted sampling plan Q is a subset of the complement of M (completely avoiding M).
4. R4 (Precise Alignment): Accept if and only if your submitted sampling plan Q equals M exactly.

Your goal is to infer the true release rule R and the hidden defect-prone process set M through exploratory submissions of different sampling plans Q, then output a standard sampling plan that passes the rule.

You can perform the following two types of operations:
1. Query: Submit a sampling plan Q (can be empty set, full processes, or any combination), and the system will feedback "Accept" or "Reject".
2. Final Declaration: When you believe you have collected sufficient information, simultaneously submit the rule type you identified (R1/R2/R3/R4) and a final sampling plan Q*.

Note: You must perform at least 3 queries before making a final declaration, otherwise the troubleshooting task will be forcefully terminated.

## Query and Answer Format (must strictly follow)

- Query (e.g., querying processes {{1,3,5}}):
<query_subset>1,3,5</query_subset>

- Query empty process:
<query_subset></query_subset>

- Final Declaration (e.g., identifying rule as R1, final plan as {{2,4}}):
<answer>rule=R1, subset=2,4</answer>

- Final Declaration with empty final plan:
<answer>rule=R2, subset=</answer>

Success condition: After at least 3 queries, correctly identify the rule type and submit a final sampling plan that is accepted by the quality inspection system.
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎使用“商业合规性与反垄断审查”系统。我们现在来进行一项高风险条款识别的模拟推演。

系统载入了一份包含全集 U = {{1, 2, 3, 4, 5, 6}}（代表 6 项商业行为条款）的协议草案。法务合规官已秘密标记了一个非空且非全集的高风险反垄断审查条款集合 M，并应用了审查规则 R。规则 R 从以下四种合规口径中选出：

1. R1（专项审查）：当且仅当你提交的协议条款 Q 仅包含高风险条款时，系统接受并立卷。
2. R2（整体合规）：当且仅当高风险审查条款集合 M 被你提交的协议条款 Q 完整包含时，系统确认接受。
3. R3（安全港豁免）：当且仅当你提交的协议条款 Q 完全不含高风险条款（避开 M）时，系统予以豁免接受。
4. R4（精准备案）：当且仅当你提交的协议条款 Q 恰好等于高风险条款集合 M 时，系统予以备案接受。

你的目标是通过试探性提交不同的协议条款组合 Q 来推断出真实的审查规则 R 以及隐藏的高风险条款集合 M，最终出具一份能通过系统审查的有效协议组合。

你可以进行以下两类操作：
1. 试询：提交一个协议条款组合 Q（可以是空集、全部条款或任意子集），系统会反馈“接受”或“拒绝”。
2. 终局宣告：当你认为已掌握足够信息后，同时提交你识别出的规则类型（R1/R2/R3/R4）和一个最终条款组合 Q*。

注意：你必须至少进行 3 次试询后才能进行终局宣告，否则审查流程将不予通过。

## 询问与提交答案的格式（必须严格遵守）

- 试询（例如查询条款 {{1,3,5}}）：
<query_subset>1,3,5</query_subset>

- 试询空条款：
<query_subset></query_subset>

- 终局宣告（例如识别规则为 R1，最终组合为 {{2,4}}）：
<answer>rule=R1, subset=2,4</answer>

- 终局宣告最终组合为空：
<answer>rule=R2, subset=</answer>

成功条件：在至少 3 次试询后，正确识别规则类型，且提交的最终条款组合能被系统合规审查接受。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Commercial Compliance and Antitrust Review" system. We are now conducting a mock deduction of high-risk clause identification.

The system has loaded a draft agreement containing a universal set U = {{1, 2, 3, 4, 5, 6}} representing 6 commercial behavior clauses. The legal compliance officer has secretly flagged a non-empty proper subset M representing high-risk antitrust review clauses, and applied a review rule R. Rule R is selected from the following four compliance standards:

1. R1 (Special Review): Accept and file if and only if your submitted agreement clauses Q consist solely of high-risk clauses.
2. R2 (Overall Compliance): Accept if and only if the high-risk clause set M is completely covered by your submitted agreement clauses Q.
3. R3 (Safe Harbor Exemption): Accept for exemption if and only if your submitted agreement clauses Q is a subset of the complement of M (completely avoiding high-risk clauses).
4. R4 (Precise Filing): Accept for filing if and only if your submitted agreement clauses Q equals M exactly.

Your goal is to infer the true review rule R and the hidden high-risk clause set M through exploratory submissions of different agreement clause combinations Q, then issue a valid clause combination that passes the system's review.

You can perform the following two types of operations:
1. Query: Submit an agreement clause combination Q (can be empty set, full clauses, or any subset), and the system will feedback "Accept" or "Reject".
2. Final Declaration: When you believe you have collected sufficient information, simultaneously submit the rule type you identified (R1/R2/R3/R4) and a final clause combination Q*.

Note: You must perform at least 3 queries before making a final declaration, otherwise the review process will not pass.

## Query and Answer Format (must strictly follow)

- Query (e.g., querying clauses {{1,3,5}}):
<query_subset>1,3,5</query_subset>

- Query empty clause:
<query_subset></query_subset>

- Final Declaration (e.g., identifying rule as R1, final combination as {{2,4}}):
<answer>rule=R1, subset=2,4</answer>

- Final Declaration with empty final combination:
<answer>rule=R2, subset=</answer>

Success condition: After at least 3 queries, correctly identify the rule type and submit a final clause combination that is accepted by the compliance review system.
"""

    tags = ["answer", "query_subset"]
    reasoning_type = "溯因推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "M": {2, 3, 5},
                "rule": "R2",
            },
            2: {
                "M": {1, 4},
                "rule": "R1",
            },
            3: {
                "M": {1, 3, 6},
                "rule": "R3",
            },
            4: {
                "M": {2, 5},
                "rule": "R4",
            },
            5: {
                "M": {1, 2, 4, 6},
                "rule": "R4",
            },
        },
        "en": {
            1: {
                "M": {2, 3, 5},
                "rule": "R2",
            },
            2: {
                "M": {1, 4},
                "rule": "R1",
            },
            3: {
                "M": {1, 3, 6},
                "rule": "R3",
            },
            4: {
                "M": {2, 5},
                "rule": "R4",
            },
            5: {
                "M": {1, 2, 4, 6},
                "rule": "R4",
            },
        },
    }

    def __init__(self, config):
        self.U = {1, 2, 3, 4, 5, 6}  # 全集
        self.query_count = 0  # 试询次数计数
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度配置设置隐藏集合 M 和判定规则 R"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.M = cfg["M"]  # 隐藏的主集
        self.rule = cfg["rule"]  # 隐藏的判定规则
        self._game_info["n"] = 6  # 用于格式化游戏规则（如果需要）

    def _check_rule(self, Q):
        """
        根据当前规则 R 判定提交的集合 Q 是否被接受
        Q: 提交的集合
        返回: True 表示接受，False 表示拒绝
        """
        if self.rule == "R1":
            # R1: Q ⊆ M
            return Q.issubset(self.M)
        elif self.rule == "R2":
            # R2: M ⊆ Q
            return self.M.issubset(Q)
        elif self.rule == "R3":
            # R3: Q ⊆ (U \ M)
            complement_M = self.U - self.M
            return Q.issubset(complement_M)
        elif self.rule == "R4":
            # R4: Q = M
            return Q == self.M
        else:
            raise ValueError(f"Unknown rule: {self.rule}")

    def evaluate(self, parsed_info):
        """
        评估终局宣告的答案
        parsed_info: 包含 'answer' 键，格式为 "rule=R1, subset=1,2,3"
        返回: True 表示答案正确，False 表示错误
        """
        # 注意：在冗余评估模式下，query_count 可能不会被正常递增
        # 仅在标准游戏模式下检查最少试询次数
        # 通过检查 enable_counterfactual 或直接跳过此检查（因为冗余评估走不同路径）
        # 更安全的做法：只在标准交互模式下强制检查
        if not getattr(self, '_skip_query_count_check', False) and getattr(self, 'query_count', 0) < 3:
            return False

        raw_ans = parsed_info["answer"]
        
        # 使用正则解析 rule 和 subset
        rule_match = re.search(r'rule\s*=\s*(R[1-4])', raw_ans, re.IGNORECASE)
        subset_match = re.search(r'subset\s*=\s*([\d,\s]*)', raw_ans)
        
        if not rule_match or subset_match is None:
            return False
        
        # 1. 检查规则识别是否正确
        identified_rule = rule_match.group(1).upper()
        if identified_rule != self.rule:
            return False
        
        # 2. 解析最终子集
        try:
            subset_str = subset_match.group(1).strip()
            if subset_str == "":
                final_subset = set()
            else:
                final_subset = set(int(x.strip()) for x in subset_str.split(",") if x.strip())
            
            # 检查子集元素是否都在全集 U 中
            if not final_subset.issubset(self.U):
                return False
                
        except (ValueError, TypeError):
            return False
        
        # 3. 检查最终子集是否被规则接受
        return self._check_rule(final_subset)

    def _cf_make_wrong(self, correct):
        """
        将正确的接受/拒绝反馈反转，用于反事实干预模式。
        correct: 正确的反馈字符串，如 "Accept" / "Reject" / "接受" / "拒绝"
        返回: 错误的反馈字符串
        """
        if self.config.language == "zh":
            if correct == "接受":
                return "拒绝"
            elif correct == "拒绝":
                return "接受"
            else:
                return "拒绝"  # fallback
        else:
            if correct == "Accept":
                return "Reject"
            elif correct == "Reject":
                return "Accept"
            else:
                return "Reject"  # fallback

    def _cf_core_produce(self, parsed_info):
        """
        处理试询请求并返回接受/拒绝的反馈（作为基类的内部调用节点）
        """
        if self.config.language == "zh":
            accept_res, reject_res = "接受", "拒绝"
            error_msg = "错误：提交的集合包含无效元素或格式错误。"
        else:
            accept_res, reject_res = "Accept", "Reject"
            error_msg = "Error: The submitted set contains invalid elements or format error."

        if "query_subset" in parsed_info:
            # 增加试询计数
            self.query_count += 1
            
            try:
                subset_str = parsed_info["query_subset"].strip()
                
                # 处理空集情况
                if subset_str == "":
                    Q = set()
                else:
                    Q = set(int(x.strip()) for x in subset_str.split(",") if x.strip())
                
                # 检查集合元素是否都在全集 U 中
                if not Q.issubset(self.U):
                    return error_msg
                
                # 根据规则判定是否接受
                is_accepted = self._check_rule(Q)
                return accept_res if is_accepted else reject_res
                
            except:
                return error_msg
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        同时标记此实例用于冗余评估，

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        self._skip_query_count_check = True
        self.__class__._skip_query_count_check = True

        results = []
        # U = {1, 2, 3, 4, 5, 6}
        elements = sorted(list(self.U))
        
        # 根据语言配置确定返回文本
        if self.config.language == "zh":
            accept_res, reject_res = "接受", "拒绝"
        else:
            accept_res, reject_res = "Accept", "Reject"
        
        # 枚举 U 的所有子集 (2^6 = 64 个)
        for r in range(len(elements) + 1):
            for combo in itertools.combinations(elements, r):
                subset = set(combo)
                
                # 构造查询内容字符串
                query_content = ",".join(map(str, sorted(list(subset))))
                
                # 包装为 XML 标签字符串
                query_xml = f"<query_subset>{query_content}</query_subset>"
                
                # 直接调用内部逻辑判定
                is_accepted = self._check_rule(subset)
                
                results.append({
                    "query": query_xml,
                    "answer": accept_res if is_accepted else reject_res
                })
        
        return results