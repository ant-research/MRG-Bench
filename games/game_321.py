from .base import Game
import re
from itertools import product

class ObjectAttributeInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"对象属性推理"游戏，规则如下：

游戏设定了一个对象集合 S 和属性集合 A：
- 对象集合 S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- 属性集合 A = {A1, A2, A3, A4, A5, A6}

每个对象都具有若干属性（已公开且固定）：
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

我已秘密选定了一个目标对象集合 T。这个集合满足特定的属性包含和排除规则：
- 存在一个必备属性集合 I（包含2到3个属性），T 中的所有对象都必须包含 I 中的全部属性
- 存在一个禁止属性集合 E（包含0到2个属性），T 中的所有对象都不能包含 E 中的任何属性
- I 和 E 互不相交

你的目标是通过查询推断出完整的目标集合 T，并提交答案。

你可以使用以下三种查询（每次提交一个查询）：

1. **成员查询**：询问某个对象是否属于目标集合 T
   格式：<query_member>Oxx</query_member>
   示例：<query_member>O01</query_member>
   返回："是"或"否"

2. **条件计数查询**：在目标集合 T 的基础上，进一步要求包含/排除某些属性后的对象数量
   格式：<query_count>include 属性列表或none; exclude 属性列表或none</query_count>
   示例：<query_count>include A1,A2; exclude A6</query_count>
   示例：<query_count>include none; exclude A1</query_count>
   返回：满足条件的对象数量（非负整数）

3. **规模查询**：询问目标集合 T 的大小（仅可使用一次）
   格式：<query_size></query_size>
   返回：目标集合中对象的总数

当你准备好提交最终答案时，请列出你认为属于 T 的所有对象（用逗号分隔，顺序不限）：

<answer>O01,O04,O08</answer>

- 在提交最终答案前，你必须至少完成 3 次查询（成员查询、条件计数查询或规模查询）
- 你最多可以提交 2 次错误答案，第2次错误后游戏失败
- 查询总次数（不含答案提交）不能超过 12 次
- 请尽可能用最少的查询次数找到正确答案
"""

    game_rule_en = """\
Let's play an "Object-Attribute Inference" game. Here are the rules:

The game defines an object set S and an attribute set A:
- Object set S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- Attribute set A = {A1, A2, A3, A4, A5, A6}

Each object has several attributes (public and fixed):
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

I have secretly selected a target object set T. This set satisfies specific attribute inclusion and exclusion rules:
- There exists a required attribute set I (containing 2 to 3 attributes), all objects in T must contain all attributes in I
- There exists a forbidden attribute set E (containing 0 to 2 attributes), all objects in T must not contain any attribute in E
- I and E are disjoint

Your goal is to infer the complete target set T through queries and submit your answer.

You can use the following three types of queries (submit one query at a time):

1. **Membership Query**: Ask if a specific object belongs to the target set T
   Format: <query_member>Oxx</query_member>
   Example: <query_member>O01</query_member>
   Returns: "Yes" or "No"

2. **Conditional Count Query**: Count objects in T that further satisfy additional inclusion/exclusion constraints
   Format: <query_count>include attribute_list_or_none; exclude attribute_list_or_none</query_count>
   Example: <query_count>include A1,A2; exclude A6</query_count>
   Example: <query_count>include none; exclude A1</query_count>
   Returns: Count of objects satisfying the conditions (non-negative integer)

3. **Size Query**: Ask for the size of target set T (can only be used once)
   Format: <query_size></query_size>
   Returns: Total number of objects in the target set

When ready to submit your final answer, list all objects you believe belong to T (comma-separated, order doesn't matter):

<answer>O01,O04,O08</answer>

- Before submitting your final answer, you must complete at least 3 queries (membership, conditional count, or size queries)
- You can submit at most 2 incorrect answers; the game fails after the 2nd incorrect answer
- Total number of queries (excluding answer submissions) cannot exceed 12
- Try to find the correct answer with the minimum number of queries
"""

    contextualized_rule_zh_1 = """\
【交通场景：肇事车队排查】
我们来执行一项智能交通稽查任务，规则如下：

系统目前锁定了嫌疑车辆集合 S 和可能的车辆特征代号集合 A：
- 嫌疑车辆集合 S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- 车辆特征集合 A = {A1, A2, A3, A4, A5, A6}

每辆嫌疑车都具有若干特征（系统已录入且公开）：
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

系统已经根据现场痕迹，秘密锁定了真正参与肇事逃逸的同伙车队集合 T。该车队满足高度一致的特征筛选规则：
- 存在一个必备特征集合 I（包含2到3个特征），T 中的所有车辆都必须包含 I 中的全部特征
- 存在一个排除特征集合 E（包含0到2个特征），T 中的所有车辆都绝不包含 E 中的任何特征
- I 和 E 互不相交

你的目标是通过查询交管数据库推断出完整的肇事车队集合 T，并提交结案报告。

你可以使用以下三种指令向交管数据库发起查询（每次提交一个查询）：

1. **目标排查查询**：询问某辆特定车辆是否属于肇事车队 T
   格式：<query_member>Oxx</query_member>
   示例：<query_member>O01</query_member>
   返回："是"或"否"

2. **条件计数查询**：在肇事车队 T 的基础上，进一步要求包含/排除某些特征后的车辆数量
   格式：<query_count>include 特征列表或none; exclude 特征列表或none</query_count>
   示例：<query_count>include A1,A2; exclude A6</query_count>
   示例：<query_count>include none; exclude A1</query_count>
   返回：满足条件的车辆数量（非负整数）

3. **规模查询**：询问肇事车队 T 的总车辆数（仅可使用一次）
   格式：<query_size></query_size>
   返回：目标车队中的车辆总数

当你准备好提交最终结案报告时，请列出你认为属于 T 的所有车辆（用逗号分隔，顺序不限）：
<answer>O01,O04,O08</answer>

- 在提交最终答案前，你必须至少完成 3 次查询
- 你最多可以提交 2 次错误答案，第2次错误后排查任务失败
- 查询总次数（不含答案提交）不能超过 12 次
- 请尽可能用最少的查询次数侦破案件
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario: Hit-and-Run Convoy Investigation]
Let's conduct an intelligent traffic inspection task. Here are the rules:

The system has locked onto a suspect vehicle set S and vehicle feature code set A:
- Suspect vehicle set S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- Vehicle feature set A = {A1, A2, A3, A4, A5, A6}

Each suspect vehicle exhibits several features (publicly recorded in the system):
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

Based on forensic traces, the system has secretly locked onto the hit-and-run convoy set T. This convoy satisfies highly consistent feature screening rules:
- There exists a required feature set I (containing 2 to 3 features), all vehicles in T must contain all features in I
- There exists a forbidden feature set E (containing 0 to 2 features), all vehicles in T must not contain any feature in E
- I and E are disjoint

Your goal is to infer the complete convoy set T through queries to the traffic database and submit your final report.

You can use the following three types of queries (submit one query at a time):

1. **Target Inspection Query**: Ask if a specific vehicle belongs to the convoy set T
   Format: <query_member>Oxx</query_member>
   Example: <query_member>O01</query_member>
   Returns: "Yes" or "No"

2. **Conditional Count Query**: Count vehicles in T that further satisfy additional inclusion/exclusion constraints
   Format: <query_count>include feature_list_or_none; exclude feature_list_or_none</query_count>
   Example: <query_count>include A1,A2; exclude A6</query_count>
   Example: <query_count>include none; exclude A1</query_count>
   Returns: Count of vehicles satisfying the conditions (non-negative integer)

3. **Size Query**: Ask for the total number of vehicles in convoy T (can only be used once)
   Format: <query_size></query_size>
   Returns: Total number of vehicles

When ready to submit your final report, list all vehicles you believe belong to T (comma-separated, order doesn't matter):
<answer>O01,O04,O08</answer>

- Before submitting your final answer, you must complete at least 3 queries
- You can submit at most 2 incorrect answers; the task fails after the 2nd incorrect attempt
- Total number of queries (excluding answer submissions) cannot exceed 12
- Try to crack the case with the minimum number of queries
"""

    contextualized_rule_zh_2 = """\
【医疗场景：罕见病靶向筛查】
我们来执行一项罕见病靶向患者筛查任务，规则如下：

系统目前锁定了疑似患者样本集合 S 和临床指征代号集合 A：
- 患者样本集合 S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- 临床指征集合 A = {A1, A2, A3, A4, A5, A6}

每名疑似患者都表现出若干临床指征（已完成初诊并在系统中公开）：
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

根据基因图谱，医疗系统已经秘密划定了确诊感染变异病毒的靶向患者集合 T。该集合满足严格的病理规律：
- 存在一个必须具备的并发症指征集合 I（包含2到3个指征），T 中的所有患者都必须具有 I 中的全部指征
- 存在一个排除感染的排斥指征集合 E（包含0到2个指征），T 中的所有患者都不能具备 E 中的任何指征
- I 和 E 互不相交

你的目标是通过检索医疗数据库推断出完整的靶向患者集合 T，并提交筛查结果。

你可以向医疗分析系统发起以下三种指令（每次提交一个查询）：

1. **靶向确诊查询**：询问某特定患者样本是否属于靶向患者集合 T
   格式：<query_member>Oxx</query_member>
   示例：<query_member>O01</query_member>
   返回："是"或"否"

2. **条件计数查询**：在确诊集合 T 的基础上，进一步要求包含/排除某些指征后的患者数量
   格式：<query_count>include 指征列表或none; exclude 指征列表或none</query_count>
   示例：<query_count>include A1,A2; exclude A6</query_count>
   示例：<query_count>include none; exclude A1</query_count>
   返回：满足条件的患者数量（非负整数）

3. **规模查询**：询问靶向患者集合 T 的总人数（仅可使用一次）
   格式：<query_size></query_size>
   返回：靶向患者总数

当你准备好提交最终筛查结果时，请列出你认为属于 T 的所有患者编号（用逗号分隔，顺序不限）：
<answer>O01,O04,O08</answer>

- 在提交最终答案前，你必须至少完成 3 次查询
- 你最多可以提交 2 次错误答案，第2次错误后筛查任务失败
- 查询总次数（不含答案提交）不能超过 12 次
- 请尽可能用最少的查询次数完成患者排查
"""

    contextualized_rule_en_2 = """\
[Medical Scenario: Rare Disease Targeted Screening]
Let's conduct a targeted screening task for a rare disease. Here are the rules:

The system has identified suspected patient samples S and clinical indicator codes A:
- Patient sample set S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- Clinical indicator set A = {A1, A2, A3, A4, A5, A6}

Each suspected patient exhibits several clinical indicators (publicly recorded after initial diagnosis):
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

Based on genetic mapping, the system has secretly delineated the target patient group T confirmed with the mutated virus. This group follows strict pathological rules:
- There exists a mandatory complication indicator set I (containing 2 to 3 indicators), all patients in T must present all indicators in I
- There exists an exclusionary rejection indicator set E (containing 0 to 2 indicators), all patients in T must not present any indicator in E
- I and E are disjoint

Your goal is to infer the complete target patient group T by querying the medical database and submit your screening results.

You can issue the following three types of queries to the medical analysis system (submit one query at a time):

1. **Target Diagnosis Query**: Ask if a specific patient belongs to target group T
   Format: <query_member>Oxx</query_member>
   Example: <query_member>O01</query_member>
   Returns: "Yes" or "No"

2. **Conditional Count Query**: Count patients in T that further satisfy additional inclusion/exclusion constraints
   Format: <query_count>include indicator_list_or_none; exclude indicator_list_or_none</query_count>
   Example: <query_count>include A1,A2; exclude A6</query_count>
   Example: <query_count>include none; exclude A1</query_count>
   Returns: Count of patients satisfying the conditions (non-negative integer)

3. **Size Query**: Ask for the total number of patients in target group T (can only be used once)
   Format: <query_size></query_size>
   Returns: Total number of target patients

When ready to submit your final screening result, list all patients you believe belong to T (comma-separated, order doesn't matter):
<answer>O01,O04,O08</answer>

- Before submitting your final answer, you must complete at least 3 queries
- You can submit at most 2 incorrect answers; the task fails after the 2nd incorrect attempt
- Total number of queries (excluding answer submissions) cannot exceed 12
- Try to complete the screening with the minimum number of queries
"""

    contextualized_rule_zh_3 = """\
【教育场景：示范资源库选拔】
我们来进行国家级示范教学资源库的产品选拔任务，规则如下：

平台目前收录了候选教育科技产品集合 S 和教学功能指标集合 A：
- 候选产品集合 S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- 功能指标集合 A = {A1, A2, A3, A4, A5, A6}

每款候选产品都支持若干功能指标（已完成测评并公开）：
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

专家组已秘密划定了最终入选国家示范库的产品集合 T。该入选名单遵循严格的标准：
- 存在一个必须具备的核心教学功能集合 I（包含2到3个功能），T 中的所有产品都必须支持 I 中的全部功能
- 存在一个不符合国家标准的违规特征集合 E（包含0到2个特征），T 中的所有产品都绝不能带有 E 中的任何特征
- I 和 E 互不相交

你的目标是通过查询测评平台推断出完整的入选产品集合 T，并提交终审名单。

你可以使用以下三种指令查询评测系统（每次提交一个查询）：

1. **入库资格查询**：询问某款候选产品是否属于入选名单 T
   格式：<query_member>Oxx</query_member>
   示例：<query_member>O01</query_member>
   返回："是"或"否"

2. **条件计数查询**：在入选名单 T 的基础上，进一步要求包含/排除某些功能后的产品数量
   格式：<query_count>include 功能列表或none; exclude 功能列表或none</query_count>
   示例：<query_count>include A1,A2; exclude A6</query_count>
   示例：<query_count>include none; exclude A1</query_count>
   返回：满足条件的产品数量（非负整数）

3. **规模查询**：询问入选名单 T 的总数（仅可使用一次）
   格式：<query_size></query_size>
   返回：最终入库的产品总数

当你准备好提交最终通过审核的名单时，请列出你认为属于 T 的所有产品（用逗号分隔，顺序不限）：
<answer>O01,O04,O08</answer>

- 在提交最终答案前，你必须至少完成 3 次查询
- 你最多可以提交 2 次错误答案，第2次错误后选拔任务失败
- 查询总次数（不含答案提交）不能超过 12 次
- 请尽可能用最少的查询次数完成资源库名单的评估
"""

    contextualized_rule_en_3 = """\
[Education Scenario: Exemplary Resource Database Selection]
Let's conduct the selection task for the national exemplary teaching resource database. Here are the rules:

The platform has cataloged candidate EdTech products S and pedagogical feature metrics A:
- Candidate product set S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- Pedagogical feature set A = {A1, A2, A3, A4, A5, A6}

Each candidate product supports several pedagogical features (publicly evaluated):
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

The expert panel has secretly determined the final selected product set T for the national database. This list follows strict criteria:
- There exists a mandatory core pedagogical feature set I (containing 2 to 3 features), all products in T must support all features in I
- There exists a non-compliant feature set E failing national standards (containing 0 to 2 features), all products in T must not have any feature in E
- I and E are disjoint

Your goal is to infer the complete selected product set T by querying the evaluation platform and submit the final approval list.

You can issue the following three types of queries to the evaluation system (submit one query at a time):

1. **Qualification Query**: Ask if a specific product belongs to the selected list T
   Format: <query_member>Oxx</query_member>
   Example: <query_member>O01</query_member>
   Returns: "Yes" or "No"

2. **Conditional Count Query**: Count products in T that further satisfy additional inclusion/exclusion constraints
   Format: <query_count>include feature_list_or_none; exclude feature_list_or_none</query_count>
   Example: <query_count>include A1,A2; exclude A6</query_count>
   Example: <query_count>include none; exclude A1</query_count>
   Returns: Count of products satisfying the conditions (non-negative integer)

3. **Size Query**: Ask for the total number of selected products in T (can only be used once)
   Format: <query_size></query_size>
   Returns: Total number of approved products

When ready to submit the final approved list, list all products you believe belong to T (comma-separated, order doesn't matter):
<answer>O01,O04,O08</answer>

- Before submitting your final answer, you must complete at least 3 queries
- You can submit at most 2 incorrect answers; the task fails after the 2nd incorrect attempt
- Total number of queries (excluding answer submissions) cannot exceed 12
- Try to complete the evaluation with the minimum number of queries
"""

    contextualized_rule_zh_4 = """\
【工业场景：航天零件质检】
我们来执行一项特种航天设备零部件的质检筛选任务，规则如下：

制造控制中心锁定了待检工业零部件批次集合 S 和工艺属性集合 A：
- 待检批次集合 S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- 工艺属性集合 A = {A1, A2, A3, A4, A5, A6}

每个批次均具有若干制造工艺属性（已检测并公开记录）：
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

质检核心系统已根据装配蓝图，秘密确定了满足特种航天设备组装需求的高优合格批次集合 T。该集合满足严苛的工艺要求：
- 存在一个关键航天工艺要求集合 I（包含2到3个属性），T 中的所有批次都必须经过 I 中的全部工艺
- 存在一个导致装配不兼容的限制属性集合 E（包含0到2个属性），T 中的所有批次都严禁出现 E 中的任何属性
- I 和 E 互不相交

你的目标是通过质检系统交互推断出完整的高优合格批次集合 T，并提交放行清单。

你可以向质检系统发送以下三种控制台指令（每次提交一个查询）：

1. **批次合格查询**：询问某特定批次是否属于高优合格集合 T
   格式：<query_member>Oxx</query_member>
   示例：<query_member>O01</query_member>
   返回："是"或"否"

2. **条件计数查询**：在高优合格集合 T 的基础上，进一步要求包含/排除某些工艺属性后的批次数量
   格式：<query_count>include 属性列表或none; exclude 属性列表或none</query_count>
   示例：<query_count>include A1,A2; exclude A6</query_count>
   示例：<query_count>include none; exclude A1</query_count>
   返回：满足条件的批次数量（非负整数）

3. **规模查询**：询问高优合格集合 T 的总批次数（仅可使用一次）
   格式：<query_size></query_size>
   返回：合格批次的总数

当你准备好提交最终放行清单时，请列出你认为属于 T 的所有批次（用逗号分隔，顺序不限）：
<answer>O01,O04,O08</answer>

- 在提交最终答案前，你必须至少完成 3 次查询
- 你最多可以提交 2 次错误答案，第2次错误后质检任务失败
- 查询总次数（不含答案提交）不能超过 12 次
- 请尽可能用最少的查询次数完成筛选
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario: Aerospace Component Inspection]
Let's conduct a quality inspection and screening task for special aerospace components. Here are the rules:

The manufacturing control center has logged pending industrial component batches S and process attribute set A:
- Pending batch set S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- Process attribute set A = {A1, A2, A3, A4, A5, A6}

Each batch possesses several manufacturing process attributes (inspected and publicly recorded):
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

Based on assembly blueprints, the core inspection system has secretly determined the high-priority qualified batch set T meeting special aerospace assembly requirements. This set satisfies stringent process demands:
- There exists a critical aerospace process requirement set I (containing 2 to 3 attributes), all batches in T must have undergone all processes in I
- There exists an incompatible restricting attribute set E (containing 0 to 2 attributes), all batches in T are strictly prohibited from having any attribute in E
- I and E are disjoint

Your goal is to infer the complete high-priority qualified batch set T through interactions with the inspection system and submit the clearance list.

You can send the following three console commands to the inspection system (submit one query at a time):

1. **Batch Qualification Query**: Ask if a specific batch belongs to the high-priority qualified set T
   Format: <query_member>Oxx</query_member>
   Example: <query_member>O01</query_member>
   Returns: "Yes" or "No"

2. **Conditional Count Query**: Count batches in T that further satisfy additional inclusion/exclusion constraints
   Format: <query_count>include attribute_list_or_none; exclude attribute_list_or_none</query_count>
   Example: <query_count>include A1,A2; exclude A6</query_count>
   Example: <query_count>include none; exclude A1</query_count>
   Returns: Count of batches satisfying the conditions (non-negative integer)

3. **Size Query**: Ask for the total number of batches in the qualified set T (can only be used once)
   Format: <query_size></query_size>
   Returns: Total number of qualified batches

When ready to submit your final clearance list, list all batches you believe belong to T (comma-separated, order doesn't matter):
<answer>O01,O04,O08</answer>

- Before submitting your final answer, you must complete at least 3 queries
- You can submit at most 2 incorrect answers; the task fails after the 2nd incorrect attempt
- Total number of queries (excluding answer submissions) cannot exceed 12
- Try to complete the screening with the minimum number of queries
"""

    contextualized_rule_zh_5 = """\
【法律场景：指导性判例检索】
我们来执行一项重大商业诉讼的指导性判例检索任务，规则如下：

智能法律数据库目前整理了过往商业纠纷判例集合 S 和案件核心要素集合 A：
- 过往判例集合 S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- 案件要素集合 A = {A1, A2, A3, A4, A5, A6}

每个过往判例都包含若干核心法律要素（已在判决书中公开确认）：
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

针对当前的重大诉讼，法庭逻辑引擎已秘密计算出具有绝对约束力的指导性案例集合 T。该先例集合满足特定的法理推导规则：
- 存在一个构成适用先例的必备法律要件集合 I（包含2到3个要素），T 中的所有案例都必须包含 I 中的全部要素
- 存在一个导致判例效力被推翻的排除情形集合 E（包含0到2个要素），T 中的所有案例都不能涉及 E 中的任何要素
- I 和 E 互不相交

你的目标是通过向法律引擎进行逻辑提问，推断出完整的指导性案例集合 T，并提交检索报告。

你可以使用以下三种指令向法律引擎发起检索（每次提交一个查询）：

1. **判例适用查询**：询问某特定判例是否属于绝对约束力集合 T
   格式：<query_member>Oxx</query_member>
   示例：<query_member>O01</query_member>
   返回："是"或"否"

2. **条件计数查询**：在约束力集合 T 的基础上，进一步要求包含/排除某些案件要素后的判例数量
   格式：<query_count>include 要素列表或none; exclude 要素列表或none</query_count>
   示例：<query_count>include A1,A2; exclude A6</query_count>
   示例：<query_count>include none; exclude A1</query_count>
   返回：满足条件的判例数量（非负整数）

3. **规模查询**：询问绝对约束力集合 T 的总案例数（仅可使用一次）
   格式：<query_size></query_size>
   返回：适用先例的总数

当你准备好出具最终法律检索报告时，请列出你认为属于 T 的所有判例案号（用逗号分隔，顺序不限）：
<answer>O01,O04,O08</answer>

- 在提交最终答案前，你必须至少完成 3 次查询
- 你最多可以提交 2 次错误答案，第2次错误后检索任务宣告失败
- 查询总次数（不含答案提交）不能超过 12 次
- 请尽可能用最少的查询次数完成法理推断
"""

    contextualized_rule_en_5 = """\
[Legal Scenario: Binding Precedent Retrieval]
Let's execute a binding precedent retrieval task for a major commercial lawsuit. Here are the rules:

The intelligent legal database has cataloged past commercial dispute precedents S and key case elements A:
- Past precedent set S = {O01, O02, O03, O04, O05, O06, O07, O08, O09, O10, O11, O12}
- Key case element set A = {A1, A2, A3, A4, A5, A6}

Each past precedent involves several core legal elements (publicly confirmed in judgments):
- O01: {A1, A2, A4}
- O02: {A1, A3, A5}
- O03: {A2, A3, A4}
- O04: {A1, A4, A5}
- O05: {A2, A5, A6}
- O06: {A1, A2, A3}
- O07: {A3, A4, A6}
- O08: {A1, A5, A6}
- O09: {A2, A4, A5}
- O10: {A3, A5}
- O11: {A4, A6}
- O12: {A1, A3, A6}

For the current major lawsuit, the court's logic engine has secretly computed the binding guiding precedent set T. This precedent set satisfies specific jurisprudential deduction rules:
- There exists a required legal element set I constituting applicable precedent (containing 2 to 3 elements), all cases in T must contain all elements in I
- There exists an exclusionary circumstance set E invalidating precedent applicability (containing 0 to 2 elements), all cases in T must not involve any element in E
- I and E are disjoint

Your goal is to infer the complete guiding precedent set T by formulating logical queries to the legal engine, and submit your retrieval report.

You can issue the following three types of queries to the legal engine (submit one query at a time):

1. **Precedent Applicability Query**: Ask if a specific precedent belongs to the binding set T
   Format: <query_member>Oxx</query_member>
   Example: <query_member>O01</query_member>
   Returns: "Yes" or "No"

2. **Conditional Count Query**: Count precedents in T that further satisfy additional inclusion/exclusion constraints
   Format: <query_count>include element_list_or_none; exclude element_list_or_none</query_count>
   Example: <query_count>include A1,A2; exclude A6</query_count>
   Example: <query_count>include none; exclude A1</query_count>
   Returns: Count of precedents satisfying the conditions (non-negative integer)

3. **Size Query**: Ask for the total number of precedents in the binding set T (can only be used once)
   Format: <query_size></query_size>
   Returns: Total number of applicable precedents

When ready to issue the final legal retrieval report, list all precedents you believe belong to T (comma-separated, order doesn't matter):
<answer>O01,O04,O08</answer>

- Before submitting your final answer, you must complete at least 3 queries
- You can submit at most 2 incorrect answers; the retrieval task fails after the 2nd incorrect attempt
- Total number of queries (excluding answer submissions) cannot exceed 12
- Try to complete the jurisprudential deduction with the minimum number of queries
"""

    reasoning_type = "演绎推理"
    data_structure = "集合"

    tags = ["answer", "query_member", "query_count", "query_size"]

    OBJECT_ATTRIBUTES = {
        "O01": {"A1", "A2", "A4"},
        "O02": {"A1", "A3", "A5"},
        "O03": {"A2", "A3", "A4"},
        "O04": {"A1", "A4", "A5"},
        "O05": {"A2", "A5", "A6"},
        "O06": {"A1", "A2", "A3"},
        "O07": {"A3", "A4", "A6"},
        "O08": {"A1", "A5", "A6"},
        "O09": {"A2", "A4", "A5"},
        "O10": {"A3", "A5"},
        "O11": {"A4", "A6"},
        "O12": {"A1", "A3", "A6"},
    }

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "include": ["A1", "A5"],
                "exclude": [],
            },
            2: {
                "include": ["A2", "A4"],
                "exclude": ["A3"],
            },
            3: {
                "include": ["A1", "A2", "A4"],
                "exclude": [],
            },
            4: {
                "include": ["A3", "A4", "A6"],
                "exclude": ["A2"],
            },
            5: {
                "include": ["A1", "A3"],
                "exclude": ["A4", "A5"],
            },
        },
        "en": {
            1: {
                "include": ["A1", "A5"],
                "exclude": [],
            },
            2: {
                "include": ["A2", "A4"],
                "exclude": ["A3"],
            },
            3: {
                "include": ["A3", "A5"],
                "exclude": [],
            },
            4: {
                "include": ["A4", "A6"],
                "exclude": ["A2"],
            },
            5: {
                "include": ["A1", "A3"],
                "exclude": ["A4", "A5"],
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.incorrect_answer_count = 0
        self.size_query_used = False
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.include_attrs = set(cfg["include"])
        self.exclude_attrs = set(cfg["exclude"])
        
        self.target_set = self._compute_target_set()
        
        self._game_info = {}

    def _compute_target_set(self):
        target = set()
        for obj_id, attrs in self.OBJECT_ATTRIBUTES.items():
            if not self.include_attrs.issubset(attrs):
                continue
            if self.exclude_attrs.intersection(attrs):
                continue
            target.add(obj_id)
        return target

    def evaluate(self, parsed_info):
        if self.query_count < 3:
            raise ValueError(
                "在提交答案前至少需要进行3次查询。" if self.config.language == "zh" 
                else "At least 3 queries required before submitting answer."
            )
        
        raw_ans = parsed_info["answer"].strip()
        try:
            submitted_objects = set(obj.strip().upper() for obj in raw_ans.split(",") if obj.strip())
        except:
            self.incorrect_answer_count += 1
            return False
        
        is_correct = submitted_objects == self.target_set
        
        if not is_correct:
            self.incorrect_answer_count += 1
            if self.incorrect_answer_count >= 2:
                pass
        
        return is_correct

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            if correct == "Yes":
                return "No"
            elif correct == "No":
                return "Yes"
        
        try:
            num = int(correct)
            return str(num + 1)
        except ValueError:
            pass
        
        return correct + " [错误]" if self.config.language == "zh" else correct + " [wrong]"

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。"
            error_range = "错误：对象编号无效。"
            error_size_used = "错误：规模查询已使用过。"
            error_max_queries = "错误：查询次数已达上限。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format."
            error_range = "Error: Invalid object ID."
            error_size_used = "Error: Size query already used."
            error_max_queries = "Error: Maximum query count reached."

        if self.query_count >= 12:
            self.state.set_state("failed", "exceeded maximum queries")
            return error_max_queries

        if "query_member" in parsed_info:
            self.query_count += 1
            obj_id = parsed_info["query_member"].strip().upper()
            if obj_id not in self.OBJECT_ATTRIBUTES:
                return error_range
            return yes_res if obj_id in self.target_set else no_res

        elif "query_count" in parsed_info:
            self.query_count += 1
            try:
                raw = parsed_info["query_count"].strip()
                parts = raw.split(";")
                if len(parts) != 2:
                    return error_format
                
                include_part = parts[0].strip()
                exclude_part = parts[1].strip()
                
                if not include_part.startswith("include"):
                    return error_format
                include_str = include_part[7:].strip()
                if include_str.lower() == "none":
                    include_attrs = set()
                else:
                    include_attrs = set(attr.strip().upper() for attr in include_str.split(",") if attr.strip())
                
                if not exclude_part.startswith("exclude"):
                    return error_format
                exclude_str = exclude_part[7:].strip()
                if exclude_str.lower() == "none":
                    exclude_attrs = set()
                else:
                    exclude_attrs = set(attr.strip().upper() for attr in exclude_str.split(",") if attr.strip())
                
                count = 0
                for obj_id in self.target_set:
                    obj_attrs = self.OBJECT_ATTRIBUTES[obj_id]
                    if include_attrs and not include_attrs.issubset(obj_attrs):
                        continue
                    if exclude_attrs and exclude_attrs.intersection(obj_attrs):
                        continue
                    count += 1
                
                return str(count)
            except:
                return error_format

        elif "query_size" in parsed_info:
            if self.size_query_used:
                return error_size_used
            self.query_count += 1
            self.size_query_used = True
            return str(len(self.target_set))

        else:
            return error_format

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        yes_res = "是" if self.config.language == "zh" else "Yes"
        no_res = "否" if self.config.language == "zh" else "No"
        
        for obj_id in sorted(self.OBJECT_ATTRIBUTES.keys()):
            ans = yes_res if obj_id in self.target_set else no_res
            results.append({
                "query": f"<query_member>{obj_id}</query_member>",
                "answer": ans
            })
            
        results.append({
            "query": "<query_size></query_size>",
            "answer": str(len(self.target_set))
        })
        
        attrs = ["A1", "A2", "A3", "A4", "A5", "A6"]
        
        for states in product(range(3), repeat=6):
            inc_list = []
            exc_list = []
            
            for i, s in enumerate(states):
                if s == 1:
                    inc_list.append(attrs[i])
                elif s == 2:
                    exc_list.append(attrs[i])
            
            inc_set = set(inc_list)
            exc_set = set(exc_list)
            if not inc_set.isdisjoint(exc_set):
                continue
            if not inc_list and not exc_list:
                continue
            
            inc_str = ",".join(inc_list) if inc_list else "none"
            exc_str = ",".join(exc_list) if exc_list else "none"
            query_content = f"include {inc_str}; exclude {exc_str}"
            
            count = 0
            for obj_id in self.target_set:
                obj_attrs = self.OBJECT_ATTRIBUTES[obj_id]
                if not inc_set.issubset(obj_attrs):
                    continue
                if not exc_set.isdisjoint(obj_attrs):
                    continue
                count += 1
            
            results.append({
                "query": f"<query_count>{query_content}</query_count>",
                "answer": str(count)
            })
            
        return results

    def step(self, response: str):
        if self.state.state != "in_progress":
            return self.state

        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确！" if self.config.language == "zh" else "Correct answer!"
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    if self.incorrect_answer_count >= 2:
                        res = "答案错误。错误次数已达上限，游戏失败。" if self.config.language == "zh" else "Incorrect answer. Maximum incorrect attempts reached, game failed."
                        self.state.set_state("failed", "too many incorrect answers")
                        self.state.add_message("user", res)
                    else:
                        res = f"答案错误。剩余尝试次数：{2 - self.incorrect_answer_count}" if self.config.language == "zh" else f"Incorrect answer. Remaining attempts: {2 - self.incorrect_answer_count}"
                        self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
                if self.query_count >= 12 and self.state.state == "in_progress":
                    self.state.set_state("failed", "exceeded maximum queries")
                
        except Exception as e:
            self.state.set_state("failed", f"parse error: {str(e)}")
            msg = f"解析错误：{str(e)}" if self.config.language == "zh" else f"Parse error: {str(e)}"
            self.state.add_message("user", msg)
        
        return self.state