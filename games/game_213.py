from .base import Game
import random
import itertools

class GlobalOrderingGame(Game):

    game_rule_zh = """\
我们来玩一个"全局排序推理"游戏，规则如下：

游戏设定了 9 个带编号的对象，编号为 1 到 9。每个对象具有三个离散属性，记为 A、B、C。每个属性有 3 种可能的取值：
- 属性 A 的取值为：A1、A2、A3
- 属性 B 的取值为：B1、B2、B3
- 属性 C 的取值为：C1、C2、C3

九个对象的属性三元组如下（格式为 编号:(A,B,C)）：
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

系统已秘密确定一个"字典序规则"，用于对这 9 个对象进行完整排序：
1. 首先确定三个属性的比较优先级顺序（例如：先比较 A，再比较 B，最后比较 C）。
2. 对每个属性的三个取值确定一个顺序关系（例如：A1 < A2 < A3）。
3. 比较两个对象时，先按优先级最高的属性比较；若相同，再按第二优先级属性比较；仍相同则按第三优先级属性比较。

这个规则在整个游戏过程中保持不变。

你的目标是：推断出在该隐藏规则下，所有 9 个对象完整排序后第 {target_position} 位的对象编号是什么。

你可以使用以下三种查询方式（每次只能提出一个查询）：

1. **成对比较查询**：询问两个对象的相对顺序。
2. **子集排序查询**：给定一个不超过 4 个对象的子集，获取该子集内部的完整排序。
3. **子集第 t 位查询**：给定一个子集及位置 t，询问该子集排序后第 t 位是哪个对象。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成对比较查询（例如询问编号 1 和编号 3 的顺序）：
<query_pair>1,3</query_pair>

- 子集排序查询（例如询问编号 1,2,3,4 组成的子集的排序）：
<query_subset>1,2,3,4</query_subset>

- 子集第 t 位查询（例如询问子集 1,2,3 排序后第 2 位是谁）：
<query_position>subset=1,2,3;position=2</query_position>

提交最终答案时，直接给出对象编号：

<answer>5</answer>

请尽可能高效地使用查询次数来推断出答案。
"""

    game_rule_en = """\
Let's play a "Global Ordering Inference" game. Here are the rules:

There are 9 numbered objects, labeled 1 to 9. Each object has three discrete attributes: A, B, and C. Each attribute has 3 possible values:
- Attribute A: A1, A2, A3
- Attribute B: B1, B2, B3
- Attribute C: C1, C2, C3

The attribute triples for the nine objects are as follows (format: ID:(A,B,C)):
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

The system has secretly determined a "lexicographic ordering rule" for sorting these 9 objects:
1. First, determine the priority order of the three attributes (e.g., compare A first, then B, then C).
2. For each attribute, determine an ordering among its three values (e.g., A1 < A2 < A3).
3. When comparing two objects, first compare by the highest priority attribute; if equal, compare by the second priority; if still equal, compare by the third.

This rule remains fixed throughout the game.

Your goal is: deduce which object is in position {target_position} when all 9 objects are sorted according to this hidden rule.

You can use the following three types of queries (one query per turn):

1. **Pairwise comparison query**: Ask about the relative order of two objects.
2. **Subset sorting query**: Given a subset of at most 4 objects, get the complete ordering within that subset.
3. **Subset position query**: Given a subset and a position t, ask which object is at position t in the sorted subset.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Pairwise comparison query (e.g., asking about the order of ID 1 and ID 3):
<query_pair>1,3</query_pair>

- Subset sorting query (e.g., asking for the ordering of subset 1,2,3,4):
<query_subset>1,2,3,4</query_subset>

- Subset position query (e.g., asking which object is at position 2 in sorted subset 1,2,3):
<query_position>subset=1,2,3;position=2</query_position>

When submitting the final answer, directly provide the object ID:

<answer>5</answer>

Please use your queries as efficiently as possible to deduce the answer.
"""

    contextualized_rule_zh_1 = """\
智能交通调度系统已启动。这里有 9 条待评估的自动驾驶路线，编号为 1 到 9。每条路线具有三个维度的评估属性：拥堵指数（A）、路面通行条件（B）、气象影响评级（C）。
每个属性有 3 种可能的取值（A1/A2/A3，B1/B2/B3，C1/C2/C3）。

九条路线的属性三元组如下（格式为 路线编号:(A,B,C)）：
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

调度后台秘密应用了一套"字典序优先级算法"对这 9 条路线进行全局最优排序：
1. 首先确立三个属性的决策优先级（例如：最优先考虑拥堵指数，其次是通行条件，最后考虑气象）。
2. 对每个属性的三个层级设定优劣顺序（例如：A1 < A2 < A3）。
3. 比较两条路线时，严格按最高优先级属性对比；若表现相同则比对次级属性；仍相同则比对最次级属性。

此算法规则在本次调度中固定不变。

你的目标是：推断出在该隐藏算法下，所有 9 条路线经过完整排序后，位列第 {target_position} 位的最优推荐路线编号是什么。

你可以调用以下三种系统接口（每次只能发起一次调用）：

1. **成对比较查询**：询问两条路线的相对优先级顺序。
2. **子集排序查询**：给定不超过 4 条路线的子集，获取该子集内部的完整排序结果。
3. **子集第 t 位查询**：给定路线子集及名次 t，询问该子集内部排在第 t 位的是哪条路线。

当你收集足够信息后，请提交最终路线编号。若答案错误或格式不符，调度评估失败。

每次调用只能包含一个标签。请使用以下 XML 格式：

- 成对比较查询（例如询问路线 1 和路线 3 的顺序）：
<query_pair>1,3</query_pair>

- 子集排序查询（例如询问路线 1,2,3,4 组成的子集的排序）：
<query_subset>1,2,3,4</query_subset>

- 子集第 t 位查询（例如询问子集 1,2,3 排序后第 2 位的路线）：
<query_position>subset=1,2,3;position=2</query_position>

提交最终答案时，直接给出路线编号：
<answer>5</answer>

请尽可能高效地使用调用次数来推断出最优推荐路线。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The smart traffic dispatch system is online. There are 9 autonomous driving routes to be evaluated, numbered 1 to 9. Each route has three dimensions of evaluation attributes: Congestion Level (A), Road Condition (B), and Weather Impact Rating (C).
Each attribute has 3 possible discrete values: (A1/A2/A3, B1/B2/B3, C1/C2/C3).

The attribute triples for the 9 routes are (Format: Route ID:(A,B,C)):
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

The dispatch backend secretly applies a "lexicographical priority algorithm" to comprehensively rank these 9 routes:
1. First, establish the decision priority among the three attributes (e.g., Congestion Level prioritized first, then Road Condition, finally Weather).
2. Establish a relative hierarchy for the three levels of each attribute (e.g., A1 < A2 < A3).
3. When comparing two routes, strictly compare by the highest priority attribute; if they tie, compare by the secondary attribute; if still tied, compare by the tertiary attribute.

This algorithmic rule remains constant during this dispatch phase.

Your goal is to deduce: Under this hidden algorithm, which route number sits at position {target_position} once all 9 routes are fully ranked?

You can invoke the following three system interfaces (one call per turn):

1. **Pairwise comparison query**: Ask about the relative priority order of two routes.
2. **Subset sorting query**: Given a subset of up to 4 routes, obtain the complete ranking within that subset.
3. **Subset position query**: Given a subset and a position t, inquire which route ranks at position t within that subset.

When you have gathered enough information, submit the final route number. Incorrect answers or invalid formats will cause the dispatch evaluation to fail.

Each call must contain only one tag. Use the following XML format:

- Pairwise comparison query (e.g., querying the order of routes 1 and 3):
<query_pair>1,3</query_pair>

- Subset sorting query (e.g., querying the ranking of the route subset 1,2,3,4):
<query_subset>1,2,3,4</query_subset>

- Subset position query (e.g., querying which route is in position 2 in the sorted subset 1,2,3):
<query_position>subset=1,2,3;position=2</query_position>

When submitting the final answer, directly provide the route ID:
<answer>5</answer>

Please invoke the interfaces as efficiently as possible to deduce the optimal recommended route.
"""

    contextualized_rule_zh_2 = """\
急诊分诊系统已激活。现有 9 个急诊病例待评估，编号为 1 到 9。每个病例具有三个维度的医疗属性：生命体征危急度（A）、并发症风险等级（B）、资源消耗预估（C）。
每个属性有 3 种可能的取值（A1/A2/A3，B1/B2/B3，C1/C2/C3）。

九个病例的属性三元组如下（格式为 病例编号:(A,B,C)）：
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

分诊系统秘密执行一套"多维分级量表算法"用于对这 9 个病例确立收治顺序：
1. 首先确立三个属性的临床判定优先级（例如：优先看危急度，其次看并发症，最后看资源消耗）。
2. 对每个属性的三个等级设定临床先后顺序（例如：A1 < A2 < A3）。
3. 比较两个病例时，严格按最高优先级属性对比；若表现相同则比对次级属性；仍相同则比对最次级属性。

此量表规则在本次分诊中保持不变。

你的目标是：推断出在该隐藏算法下，所有 9 个病例经过完整分诊排序后，位列第 {target_position} 位的病例编号是什么。

你可以调用以下三种急诊查询接口（每次只能发起一次调用）：

1. **成对比较查询**：询问两个病例的相对收治优先级顺序。
2. **子集排序查询**：给定不超过 4 个病例的子集，获取该子集内部的完整收治排序。
3. **子集第 t 位查询**：给定病例子集及排位 t，询问该子集内部排在第 t 位的是哪个病例。

当你收集足够信息后，请提交最终病例编号。若答案错误或格式不符，分诊操作失败。

每次调用只能包含一个标签。请使用以下 XML 格式：

- 成对比较查询（例如询问病例 1 和 3 的收治顺序）：
<query_pair>1,3</query_pair>

- 子集排序查询（例如询问病例 1,2,3,4 组成的子集的顺序）：
<query_subset>1,2,3,4</query_subset>

- 子集第 t 位查询（例如询问子集 1,2,3 排序后第 2 位的病例）：
<query_position>subset=1,2,3;position=2</query_position>

提交最终答案时，直接给出病例编号：
<answer>5</answer>

请尽可能高效地使用调用次数来推断出该病例。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The emergency triage system is activated. There are 9 emergency cases awaiting evaluation, numbered 1 to 9. Each case exhibits three dimensions of medical attributes: Vitals Criticality (A), Complication Risk (B), and Resource Demand (C).
Each attribute has 3 possible discrete values: (A1/A2/A3, B1/B2/B3, C1/C2/C3).

The attribute triples for the 9 cases are (Format: Case ID:(A,B,C)):
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

The triage system secretly executes a "multi-dimensional grading scale algorithm" to establish the admission sequence for these 9 cases:
1. First, establish the clinical triage priority among the three attributes (e.g., prioritize Vitals Criticality first, then Complication Risk, finally Resource Demand).
2. Establish a clinical sequence for the three levels of each attribute (e.g., A1 < A2 < A3).
3. When comparing two cases, strictly compare by the highest priority attribute; if tied, compare by the secondary attribute; if still tied, evaluate the tertiary attribute.

This grading rule remains constant during this triage phase.

Your goal is to deduce: Under this hidden algorithm, which case number is positioned at rank {target_position} once all 9 cases are fully triaged?

You can invoke the following three emergency query interfaces (one call per turn):

1. **Pairwise comparison query**: Ask about the relative admission priority of two cases.
2. **Subset sorting query**: Given a subset of up to 4 cases, obtain the complete admission ranking within that subset.
3. **Subset position query**: Given a subset and a position t, inquire which case ranks at position t within that subset.

When you have gathered enough information, submit the final case number. Incorrect answers or invalid formats will result in a triage failure.

Each call must contain only one tag. Use the following XML format:

- Pairwise comparison query (e.g., querying the order of cases 1 and 3):
<query_pair>1,3</query_pair>

- Subset sorting query (e.g., querying the ranking of the case subset 1,2,3,4):
<query_subset>1,2,3,4</query_subset>

- Subset position query (e.g., querying which case is in position 2 in the sorted subset 1,2,3):
<query_position>subset=1,2,3;position=2</query_position>

When submitting the final answer, directly provide the case ID:
<answer>5</answer>

Please invoke the interfaces as efficiently as possible to deduce the targeted case.
"""

    contextualized_rule_zh_3 = """\
特长生档案评估系统已启动。现有 9 名学生的档案待审核，编号为 1 到 9。每份档案具有三个维度的考核属性：学术竞赛成绩（A）、综合素质评价（B）、社会实践学分（C）。
每个属性有 3 种可能的取值（A1/A2/A3，B1/B2/B3，C1/C2/C3）。

九名学生的档案属性三元组如下（格式为 学生编号:(A,B,C)）：
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

评委会秘密执行一套"综合权重评估规则"对这 9 名学生进行奖学金顺位排序：
1. 首先确立三个属性的评审优先级（例如：优先看学术成绩，其次看综合评价，最后看实践学分）。
2. 对每个属性的三个评级设定优劣顺序（例如：A1 < A2 < A3）。
3. 比较两名学生时，严格按最高优先级属性对比；若表现相同则比对次级属性；仍相同则比对最次级属性。

此评估规则在本次评审期内保持不变。

你的目标是：推断出在该隐藏规则下，所有 9 名学生经过完整顺位排序后，位列第 {target_position} 位的学生编号是什么。

你可以调用以下三种档案查询接口（每次只能发起一次调用）：

1. **成对比较查询**：询问两名学生的相对顺位先后。
2. **子集排序查询**：给定不超过 4 名学生的子集，获取该子集内部的完整顺位排序。
3. **子集第 t 位查询**：给定学生子集及排位 t，询问该子集内部排在第 t 位的是哪名学生。

当你收集足够信息后，请提交最终学生编号。若答案错误或格式不符，档案审核即告失败。

每次调用只能包含一个标签。请使用以下 XML格式：

- 成对比较查询（例如询问学生 1 和 3 的顺位先后）：
<query_pair>1,3</query_pair>

- 子集排序查询（例如询问学生 1,2,3,4 组成的子集的顺位排序）：
<query_subset>1,2,3,4</query_subset>

- 子集第 t 位查询（例如询问子集 1,2,3 排序后第 2 位的学生）：
<query_position>subset=1,2,3;position=2</query_position>

提交最终答案时，直接给出学生编号：
<answer>5</answer>

请尽可能高效地使用调用次数来推断出该学生档案。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The gifted student portfolio evaluation system is online. There are 9 student portfolios awaiting review, numbered 1 to 9. Each portfolio contains three dimensions of assessment attributes: Academic Performance (A), Comprehensive Evaluation (B), and Social Practice Credits (C).
Each attribute has 3 possible discrete values: (A1/A2/A3, B1/B2/B3, C1/C2/C3).

The attribute triples for the 9 students are (Format: Student ID:(A,B,C)):
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

The review committee secretly applies a "comprehensive weight assessment rule" to strictly rank these 9 students for scholarship sequencing:
1. First, establish the review priority among the three attributes (e.g., Academic Performance is prioritized first, then Comprehensive Evaluation, finally Social Practice Credits).
2. Establish a qualitative sequence for the three levels of each attribute (e.g., A1 < A2 < A3).
3. When comparing two students, strictly compare by the highest priority attribute; if they tie, compare by the secondary attribute; if still tied, evaluate the tertiary attribute.

This assessment rule remains strictly constant throughout this review session.

Your goal is to deduce: Under this hidden rule, which student number secures the rank at position {target_position} once all 9 students are fully sequenced?

You can invoke the following three portfolio query interfaces (one call per turn):

1. **Pairwise comparison query**: Ask about the relative scholarship sequence priority of two students.
2. **Subset sorting query**: Given a subset of up to 4 students, obtain the complete sequence ranking within that subset.
3. **Subset position query**: Given a subset and a position t, inquire which student ranks at position t within that subset.

When you have gathered enough information, submit the final student number. Incorrect answers or invalid formats will cause the portfolio audit to fail.

Each call must contain only one tag. Use the following XML format:

- Pairwise comparison query (e.g., querying the sequence order of students 1 and 3):
<query_pair>1,3</query_pair>

- Subset sorting query (e.g., querying the ranking of the student subset 1,2,3,4):
<query_subset>1,2,3,4</query_subset>

- Subset position query (e.g., querying which student is in position 2 in the sorted subset 1,2,3):
<query_position>subset=1,2,3;position=2</query_position>

When submitting the final answer, directly provide the student ID:
<answer>5</answer>

Please invoke the interfaces as efficiently as possible to deduce the targeted student portfolio.
"""

    contextualized_rule_zh_4 = """\
自动化质检系统已开启。现有 9 批次待检零部件，编号为 1 到 9。每批次零件具备三个核心工艺参数的检测属性：公差符合度（A）、材料应力表现（B）、表面缺陷等级（C）。
每个属性有 3 种可能的取值（A1/A2/A3，B1/B2/B3，C1/C2/C3）。

九个批次的属性三元组如下（格式为 批次编号:(A,B,C)）：
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

品控中心秘密应用一套"缺陷优先级矩阵"对这 9 个批次进行出库检验排序：
1. 首先确立三个工艺属性的品控权重优先级（例如：最看重公差符合度，其次是材料应力，最后看表面缺陷）。
2. 对每个属性的三个等级设定优劣排序顺序（例如：A1 < A2 < A3）。
3. 比较两个批次时，严格按最高优先级工艺对比；若表现相同则比对次级工艺参数；仍相同则比对最次级参数。

此优先矩阵在本次出库检验中固定不变。

你的目标是：推断出在该隐藏矩阵下，所有 9 个批次经过完整检验排序后，位列第 {target_position} 位的批次编号是什么。

你可以调用以下三种质检系统接口（每次只能发起一次调用）：

1. **成对比较查询**：询问两批次零件的出库先后顺序。
2. **子集排序查询**：给定不超过 4 个批次的子集，获取该子集内部的完整出库排序。
3. **子集第 t 位查询**：给定批次子集及名次 t，询问该子集内部排在第 t 位的是哪个批次。

当你收集足够信息后，请提交最终批次编号。若答案错误或格式不符，质检流转中断。

每次调用只能包含一个标签。请使用以下 XML 格式：

- 成对比较查询（例如询问批次 1 和 3 的先后顺序）：
<query_pair>1,3</query_pair>

- 子集排序查询（例如询问批次 1,2,3,4 组成的子集的顺序）：
<query_subset>1,2,3,4</query_subset>

- 子集第 t 位查询（例如询问子集 1,2,3 排序后第 2 位的批次）：
<query_position>subset=1,2,3;position=2</query_position>

提交最终答案时，直接给出批次编号：
<answer>5</answer>

请尽可能高效地使用调用次数来推断出该零部件批次。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The automated quality inspection system is online. There are 9 batches of components pending inspection, numbered 1 to 9. Each batch holds three core process testing attributes: Tolerance Compliance (A), Material Stress Performance (B), and Surface Defect Grade (C).
Each attribute has 3 possible discrete values: (A1/A2/A3, B1/B2/B3, C1/C2/C3).

The attribute triples for the 9 batches are (Format: Batch ID:(A,B,C)):
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

The quality control center secretly applies a "defect priority matrix" to establish the clearance sequence for these 9 batches:
1. First, establish the QC weight priority among the three process attributes (e.g., prioritize Tolerance Compliance first, then Material Stress, finally Surface Defects).
2. Establish a qualitative sequence for the three levels of each attribute (e.g., A1 < A2 < A3).
3. When comparing two batches, strictly compare by the highest priority process attribute; if tied, compare by the secondary parameter; if still tied, evaluate the tertiary parameter.

This priority matrix remains strictly constant throughout this clearance inspection cycle.

Your goal is to deduce: Under this hidden matrix, which batch number is designated at position {target_position} once all 9 batches are fully sequenced?

You can invoke the following three QA system interfaces (one call per turn):

1. **Pairwise comparison query**: Ask about the relative clearance priority sequence of two batches.
2. **Subset sorting query**: Given a subset of up to 4 batches, obtain the complete clearance ranking within that subset.
3. **Subset position query**: Given a subset and a position t, inquire which batch ranks at position t within that subset.

When you have gathered enough information, submit the final batch number. Incorrect answers or invalid formats will disrupt the inspection workflow.

Each call must contain only one tag. Use the following XML format:

- Pairwise comparison query (e.g., querying the clearance order of batches 1 and 3):
<query_pair>1,3</query_pair>

- Subset sorting query (e.g., querying the ranking of the batch subset 1,2,3,4):
<query_subset>1,2,3,4</query_subset>

- Subset position query (e.g., querying which batch is in position 2 in the sorted subset 1,2,3):
<query_position>subset=1,2,3;position=2</query_position>

When submitting the final answer, directly provide the batch ID:
<answer>5</answer>

Please invoke the interfaces as efficiently as possible to deduce the targeted component batch.
"""

    contextualized_rule_zh_5 = """\
智能案件排期系统已就绪。现有 9 宗待审理的商业诉讼案件，编号为 1 到 9。每宗案件具有三个维度的案情评估属性：涉案金额规模（A）、证据链完整度（B）、社会影响预警（C）。
每个属性有 3 种可能的取值（A1/A2/A3，B1/B2/B3，C1/C2/C3）。

九宗案件的属性三元组如下（格式为 案件编号:(A,B,C)）：
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

法院后台秘密依据一套"案情复杂度定级规则"对这 9 宗案件进行庭审排期排序：
1. 首先确立三个属性的法务优先级（例如：最先评估涉案金额，其次看证据完整度，最后看社会影响）。
2. 对每个属性的三个量级设定紧急顺位规则（例如：A1 < A2 < A3）。
3. 比较两宗案件时，严格按最高优先级案情属性对比；若表现相同则比对次级属性；仍相同则比对最次级属性。

此定级规则在本次庭审排期中固定不变。

你的目标是：推断出在该隐藏规则下，所有 9 宗案件经过完整排期排序后，位列第 {target_position} 位的案件编号是什么。

你可以调用以下三种司法排期查询接口（每次只能发起一次调用）：

1. **成对比较查询**：询问两宗案件的相对排期先后。
2. **子集排序查询**：给定不超过 4 宗案件的案卷子集，获取该子集内部的完整排期顺序。
3. **子集第 t 位查询**：给定案件子集及顺位 t，询问该子集内部排在第 t 位的是哪宗案件。

当你收集足够信息后，请提交最终案件编号。若答案错误或格式不符，排期操作无效。

每次调用只能包含一个标签。请使用以下 XML 格式：

- 成对比较查询（例如询问案件 1 和 3 的排期先后）：
<query_pair>1,3</query_pair>

- 子集排序查询（例如询问案件 1,2,3,4 组成的子集的排期顺序）：
<query_subset>1,2,3,4</query_subset>

- 子集第 t 位查询（例如询问子集 1,2,3 排序后第 2 位的案件）：
<query_position>subset=1,2,3;position=2</query_position>

提交最终答案时，直接给出案件编号：
<answer>5</answer>

请尽可能高效地使用调用次数来推断出该案件编号。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The smart case docketing system is ready. There are 9 commercial litigation cases pending trial scheduling, numbered 1 to 9. Each case possesses three dimensions of assessment attributes: Claim Amount Scale (A), Evidence Completeness (B), and Social Impact Warning (C).
Each attribute has 3 possible discrete values: (A1/A2/A3, B1/B2/B3, C1/C2/C3).

The attribute triples for the 9 cases are (Format: Case ID:(A,B,C)):
- 1:(A1,B1,C1)
- 2:(A1,B2,C2)
- 3:(A1,B3,C3)
- 4:(A2,B1,C2)
- 5:(A2,B2,C3)
- 6:(A2,B3,C1)
- 7:(A3,B1,C3)
- 8:(A3,B2,C1)
- 9:(A3,B3,C2)

The court backend secretly relies on a "case complexity grading rule" to strictly sequence these 9 cases for trial docketing:
1. First, establish the judicial priority among the three attributes (e.g., prioritize Claim Amount first, then Evidence Completeness, finally Social Impact).
2. Establish an urgency sequence for the three levels of each attribute (e.g., A1 < A2 < A3).
3. When comparing two cases, strictly compare by the highest priority case attribute; if they tie, compare by the secondary attribute; if still tied, evaluate the tertiary attribute.

This grading rule remains strictly constant for this trial docketing session.

Your goal is to deduce: Under this hidden rule, which case number assumes the docket position {target_position} once all 9 cases are fully sequenced?

You can invoke the following three judicial scheduling query interfaces (one call per turn):

1. **Pairwise comparison query**: Ask about the relative trial docketing sequence of two cases.
2. **Subset sorting query**: Given a docket subset of up to 4 cases, obtain the complete sequence ranking within that subset.
3. **Subset position query**: Given a subset and a position t, inquire which case ranks at position t within that subset.

When you have gathered enough information, submit the final case number. Incorrect answers or invalid formats will render the docketing operation void.

Each call must contain only one tag. Use the following XML format:

- Pairwise comparison query (e.g., querying the docket order of cases 1 and 3):
<query_pair>1,3</query_pair>

- Subset sorting query (e.g., querying the ranking of the case subset 1,2,3,4):
<query_subset>1,2,3,4</query_subset>

- Subset position query (e.g., querying which case is in position 2 in the sorted subset 1,2,3):
<query_position>subset=1,2,3;position=2</query_position>

When submitting the final answer, directly provide the case ID:
<answer>5</answer>

Please invoke the interfaces as efficiently as possible to deduce the targeted case docket number.
"""

    tags = ["answer", "query_pair", "query_subset", "query_position"]

    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "priority": [0, 1, 2],
                "order_A": [1, 2, 3],
                "order_B": [1, 2, 3],
                "order_C": [1, 2, 3],
                "target_position": 5
            },
            2: {
                "priority": [0, 2, 1],
                "order_A": [1, 2, 3],
                "order_B": [2, 1, 3],
                "order_C": [1, 3, 2],
                "target_position": 5
            },
            3: {
                "priority": [1, 0, 2],
                "order_A": [2, 1, 3],
                "order_B": [1, 2, 3],
                "order_C": [3, 1, 2],
                "target_position": 5
            },
            4: {
                "priority": [2, 1, 0],
                "order_A": [3, 2, 1],
                "order_B": [2, 3, 1],
                "order_C": [1, 2, 3],
                "target_position": 5
            },
            5: {
                "priority": [1, 2, 0],
                "order_A": [3, 1, 2],
                "order_B": [3, 2, 1],
                "order_C": [2, 3, 1],
                "target_position": 5
            }
        },
        "en": {
            1: {
                "priority": [0, 1, 2],
                "order_A": [1, 2, 3],
                "order_B": [1, 2, 3],
                "order_C": [1, 2, 3],
                "target_position": 5
            },
            2: {
                "priority": [0, 2, 1],
                "order_A": [1, 2, 3],
                "order_B": [2, 1, 3],
                "order_C": [1, 3, 2],
                "target_position": 5
            },
            3: {
                "priority": [1, 0, 2],
                "order_A": [2, 1, 3],
                "order_B": [1, 2, 3],
                "order_C": [3, 1, 2],
                "target_position": 5
            },
            4: {
                "priority": [2, 1, 0],
                "order_A": [3, 2, 1],
                "order_B": [2, 3, 1],
                "order_C": [1, 2, 3],
                "target_position": 5
            },
            5: {
                "priority": [1, 2, 0],
                "order_A": [3, 1, 2],
                "order_B": [3, 2, 1],
                "order_C": [2, 3, 1],
                "target_position": 5
            }
        }
    }

    OBJECTS = {
        1: (1, 1, 1),
        2: (1, 2, 2),
        3: (1, 3, 3),
        4: (2, 1, 2),
        5: (2, 2, 3),
        6: (2, 3, 1),
        7: (3, 1, 3),
        8: (3, 2, 1),
        9: (3, 3, 2)
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.priority = cfg["priority"]
        
        self.order_A = cfg["order_A"]
        self.order_B = cfg["order_B"]
        self.order_C = cfg["order_C"]
        
        self.target_position = cfg["target_position"]
        self._game_info["target_position"] = self.target_position
        
        self._compute_global_order()

    def _get_sort_key(self, obj_id):
        attrs = self.OBJECTS[obj_id]
        
        weights = [
            self.order_A[attrs[0] - 1],
            self.order_B[attrs[1] - 1],
            self.order_C[attrs[2] - 1]
        ]
        
        key = tuple(weights[self.priority[i]] for i in range(3))
        return key

    def _compute_global_order(self):
        all_ids = list(self.OBJECTS.keys())
        self.global_order = sorted(all_ids, key=self._get_sort_key)
        self.correct_answer = self.global_order[self.target_position - 1]

    def _compare_objects(self, id1, id2):
        key1 = self._get_sort_key(id1)
        key2 = self._get_sort_key(id2)
        return key1 < key2

    def _sort_subset(self, subset):
        return sorted(subset, key=self._get_sort_key)

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.correct_answer
        except:
            return False

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        all_ids = sorted(list(self.OBJECTS.keys()))
        lang = self.config.language

        for id1, id2 in itertools.permutations(all_ids, 2):
            query_content = f"{id1},{id2}"
            query_xml = f"<query_pair>{query_content}</query_pair>"
            
            if self._compare_objects(id1, id2):
                if lang == "zh":
                    ans = f"{id1} 在 {id2} 之前"
                else:
                    ans = f"{id1} is before {id2}"
            else:
                if lang == "zh":
                    ans = f"{id2} 在 {id1} 之前"
                else:
                    ans = f"{id2} is before {id1}"
            
            results.append({
                "query": query_xml,
                "answer": ans
            })

        for size in range(2, 5):
            for subset in itertools.combinations(all_ids, size):
                subset_list = list(subset)
                subset_str = ",".join(map(str, subset_list))
                
                sorted_subset = self._sort_subset(subset_list)
                sorted_str = ",".join(map(str, sorted_subset))
                
                q_subset_xml = f"<query_subset>{subset_str}</query_subset>"
                results.append({
                    "query": q_subset_xml,
                    "answer": sorted_str
                })
                
                for t in range(1, size + 1):
                    q_pos_content = f"subset={subset_str};position={t}"
                    q_pos_xml = f"<query_position>{q_pos_content}</query_position>"
                    
                    target_obj = sorted_subset[t - 1]
                    ans_pos = str(target_obj)
                    
                    results.append({
                        "query": q_pos_xml,
                        "answer": ans_pos
                    })
        
        return results

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效。"
            error_range = "错误：对象编号超出范围。"
            error_subset_size = "错误：子集大小超过 4 个对象。"
            before_msg = "{} 在 {} 之前"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format."
            error_range = "Error: Object ID out of range."
            error_subset_size = "Error: Subset size exceeds 4 objects."
            before_msg = "{} is before {}"

        if "query_pair" in parsed_info:
            try:
                raw = parsed_info["query_pair"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                id1, id2 = int(parts[0]), int(parts[1])
                
                if id1 not in self.OBJECTS or id2 not in self.OBJECTS:
                    return error_range
                
                if self._compare_objects(id1, id2):
                    return before_msg.format(id1, id2)
                else:
                    return before_msg.format(id2, id1)
            except:
                return error_format

        elif "query_subset" in parsed_info:
            try:
                raw = parsed_info["query_subset"]
                subset = [int(x.strip()) for x in raw.split(",")]
                
                if len(subset) > 4:
                    return error_subset_size
                
                for obj_id in subset:
                    if obj_id not in self.OBJECTS:
                        return error_range
                
                sorted_subset = self._sort_subset(subset)
                return ",".join(map(str, sorted_subset))
            except:
                return error_format

        elif "query_position" in parsed_info:
            try:
                raw = parsed_info["query_position"]
                parts = raw.split(";")
                subset_part = None
                position_part = None
                
                for part in parts:
                    if "subset=" in part:
                        subset_part = part.split("=", 1)[1]
                    elif "position=" in part:
                        position_part = part.split("=", 1)[1]
                
                if subset_part is None or position_part is None:
                    return error_format
                
                subset = [int(x.strip()) for x in subset_part.split(",")]
                position = int(position_part.strip())
                
                if len(subset) > 4:
                    return error_subset_size
                
                for obj_id in subset:
                    if obj_id not in self.OBJECTS:
                        return error_range
                
                sorted_subset = self._sort_subset(subset)
                
                if position < 1 or position > len(sorted_subset):
                    if self.config.language == "zh":
                        return f"错误：位置 {position} 超出子集范围。"
                    else:
                        return f"Error: Position {position} out of subset range."
                
                return str(sorted_subset[position - 1])
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit() or (correct.startswith("-") and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        if correct == "是": return "否"
        if correct == "否": return "是"
        
        correct_lower = correct.lower()
        if correct_lower == "yes":
            if correct.isupper(): return "NO"
            if correct.islower(): return "no"
            return "No"
        if correct_lower == "no":
            if correct.isupper(): return "YES"
            if correct.islower(): return "yes"
            return "Yes"
            
        return correct + "_WRONG"