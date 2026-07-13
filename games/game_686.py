# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   子集交集：多个给定子集的公共元素有哪些
# ============================================================

from .base import Game
import random
import itertools


class HiddenIntersectionGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "集合"

    game_rule_zh = """\
我们现在来玩一个"隐藏交集推理"游戏，规则如下：

游戏设定了一个包含 {n} 个元素的集合 U，元素用无序代号标记：{elements}。这些元素之间没有任何顺序、相邻或度量关系。

我已经秘密确定了四个属性子集 S1、S2、S3、S4，它们都是 U 的子集。这四个子集在游戏开始前已固定，且在整个游戏过程中保持不变。

你的目标是：找出这四个属性子集的交集 I，即同时属于 S1、S2、S3、S4 的所有元素（交集可能为空集）。

你可以向我提出以下两类问题，我会根据真实设定如实回答：

1. 单元素成员测试：询问某个元素 x 是否属于某个属性子集 Si（i 为 1 到 4 之间的整数）。回答"是"或"否"。

2. 子集交集计数：给定一个元素子集 S 和一个或多个属性索引集合 T（T 是 1、2、3、4 的非空子集），询问 S 中有多少个元素同时属于 T 中所有对应的属性子集。回答一个整数。

当你收集足够信息后，请提交最终答案。若答案错误、格式不符或超过询问次数上限，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单元素成员测试（例如询问元素 A 是否属于属性子集 S2）：
<query_member>A,2</query_member>

- 子集交集计数（例如询问子集 A,B,C 中有多少元素同时属于 S1 和 S3）：
<query_count>elements=A,B,C;attributes=1,3</query_count>

注意：子集交集计数中，elements 为要查询的元素列表（用逗号分隔），attributes 为属性索引列表（用逗号分隔，至少包含一个属性）。

提交最终答案时，请列出你认为属于交集 I 的所有元素（用逗号隔开，顺序不限）。如果交集为空，则答案为空字符串。格式如下：

<answer>A,C,E</answer>

或（空集情况）：

<answer></answer>

请尽可能用最少的询问次数找到答案。
"""

    game_rule_en = """\
Let's play a "Hidden Intersection Deduction" game. Here are the rules:

The game has a set U containing {n} elements, labeled with unordered identifiers: {elements}. There is no ordering, adjacency, or metric relationship among these elements.

I have secretly determined four attribute subsets S1, S2, S3, S4, all of which are subsets of U. These four subsets are fixed before the game starts and remain unchanged throughout the game.

Your goal is: to find the intersection I of these four attribute subsets, i.e., all elements that belong to S1, S2, S3, and S4 simultaneously (the intersection may be empty).

You can ask me the following two types of questions, and I will answer truthfully based on the actual setup:

1. Single Element Membership Test: Ask whether an element x belongs to a specific attribute subset Si (i is an integer between 1 and 4). Answer "Yes" or "No".

2. Subset Intersection Count: Given an element subset S and one or more attribute indices T (T is a non-empty subset of 1, 2, 3, 4), ask how many elements in S belong to all corresponding attribute subsets in T. Answer an integer.

When you have collected enough information, submit your final answer. If the answer is incorrect, the format is invalid, or the query limit is exceeded, the game fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Single Element Membership Test (e.g., asking if element A belongs to attribute subset S2):
<query_member>A,2</query_member>

- Subset Intersection Count (e.g., asking how many elements in subset A,B,C belong to both S1 and S3):
<query_count>elements=A,B,C;attributes=1,3</query_count>

Note: In subset intersection count, elements is the list of elements to query (comma-separated), and attributes is the list of attribute indices (comma-separated, must contain at least one attribute).

When submitting the final answer, list all elements you believe belong to the intersection I (comma-separated, order does not matter). If the intersection is empty, the answer should be an empty string. Format:

<answer>A,C,E</answer>

Or (for empty set):

<answer></answer>

Please find the answer with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“重点车辆联合监管智能系统”。

系统记录了一个包含 {n} 辆机动车的监控集合 U，车辆用无序代号标记：{elements}。这些车辆之间没有任何顺序或空间位置关系。

系统已经秘密确定了四个违规记录子集 S1（超速）、S2（闯红灯）、S3（违停）、S4（未礼让行人），它们都是 U 的子集。这四个记录子集在审查开始前已固定，且在整个排查过程中保持不变。

你的目标是：找出这四个违规记录子集的交集 I，即同时存在 S1、S2、S3、S4 四项违规记录的重点监管车辆（交集可能为空集）。

你可以向我提出以下两类查询，我会根据数据库真实记录如实回答：

1. 单车辆记录测试：询问某辆机动车 x 是否存在某项违规记录 Si（i 为 1 到 4 之间的整数）。回答"是"或"否"。

2. 车辆组合违规计数：给定一个车辆子集 S 和一个或多个违规记录索引集合 T（T 是 1、2、3、4 的非空子集），询问 S 中有多少辆机动车同时存在 T 中所有对应的违规记录。回答一个整数。

当你收集足够信息后，请提交最终排查结果。若结果错误、格式不符或超过查询次数上限，排查任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单车辆记录测试（例如询问车辆 A 是否存在违规记录 S2）：
<query_member>A,2</query_member>

- 车辆组合违规计数（例如询问车辆 A,B,C 中有多少辆同时存在 S1 和 S3 违规记录）：
<query_count>elements=A,B,C;attributes=1,3</query_count>

注意：车辆组合违规计数中，elements 为要查询的车辆列表（用逗号分隔），attributes 为违规记录索引列表（用逗号分隔，至少包含一项记录）。

提交最终结果时，请列出你认为属于重点监管车辆交集 I 的所有车辆代号（用逗号隔开，顺序不限）。如果没有符合条件的车辆，则答案为空字符串。格式如下：

<answer>A,C,E</answer>

或（无符合条件车辆情况）：

<answer></answer>

请尽可能用最少的查询次数找到确切名单。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Key Vehicle Joint Monitoring Intelligence System".

The system monitors a set U containing {n} motor vehicles, labeled with unordered identifiers: {elements}. There is no ordering or spatial relationship among these vehicles.

The system has secretly determined four violation subsets S1 (Speeding), S2 (Red Light Running), S3 (Illegal Parking), S4 (Failure to Yield), all of which are subsets of U. These four subsets are fixed before the review starts and remain unchanged throughout the investigation.

Your goal is: to find the intersection I of these four violation subsets, i.e., all key target vehicles that have violations S1, S2, S3, and S4 simultaneously (the intersection may be empty).

You can ask me the following two types of queries, and I will answer truthfully based on the actual database:

1. Single Vehicle Record Test: Ask whether a vehicle x has a specific violation record Si (i is an integer between 1 and 4). Answer "Yes" or "No".

2. Vehicle Subset Violation Count: Given a subset of vehicles S and one or more violation record indices T (T is a non-empty subset of 1, 2, 3, 4), ask how many vehicles in S simultaneously have all corresponding violation records in T. Answer an integer.

When you have collected enough information, submit your final investigation result. If the result is incorrect, the format is invalid, or the query limit is exceeded, the task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Single Vehicle Record Test (e.g., asking if vehicle A has violation record S2):
<query_member>A,2</query_member>

- Vehicle Subset Violation Count (e.g., asking how many vehicles in subset A,B,C have both violations S1 and S3):
<query_count>elements=A,B,C;attributes=1,3</query_count>

Note: In the vehicle subset violation count, elements is the list of vehicles to query (comma-separated), and attributes is the list of violation record indices (comma-separated, must contain at least one attribute).

When submitting the final result, list all vehicle identifiers you believe belong to the intersection I (comma-separated, order does not matter). If there are no such vehicles, the answer should be an empty string. Format:

<answer>A,C,E</answer>

Or (for empty set):

<answer></answer>

Please find the exact list with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“罕见共病临床诊断辅助系统”。

系统收录了一个包含 {n} 名患者的临床队列 U，患者用无序代号标记：{elements}。这些患者之间没有任何生理顺序或传染关联。

系统已经秘密确定了四个临床特征子集 S1（高血压）、S2（糖尿病）、S3（高血脂）、S4（特定基因突变），它们都是 U 的子集。这四个特征子集在诊断开始前已固定，且在整个排查过程中保持不变。

你的目标是：找出这四个临床特征子集的交集 I，即同时确诊 S1、S2、S3、S4 四项特征的罕见共病患者（交集可能为空集）。

你可以向我提出以下两类查询，我会根据电子病历系统如实回答：

1. 单患者指标测试：询问某名患者 x 是否具备某项临床特征 Si（i 为 1 到 4 之间的整数）。回答"是"或"否"。

2. 患者群组特征计数：给定一个患者子集 S 和一个或多个特征索引集合 T（T 是 1、2、3、4 的非空子集），询问 S 中有多少名患者同时具备 T 中所有对应的临床特征。回答一个整数。

当你收集足够信息后，请提交最终确诊名单。若名单错误、格式不符或超过查询次数上限，诊断任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单患者指标测试（例如询问患者 A 是否具备临床特征 S2）：
<query_member>A,2</query_member>

- 患者群组特征计数（例如询问患者 A,B,C 中有多少人同时具备特征 S1 和 S3）：
<query_count>elements=A,B,C;attributes=1,3</query_count>

注意：患者群组特征计数中，elements 为要查询的患者列表（用逗号分隔），attributes 为临床特征索引列表（用逗号分隔，至少包含一项特征）。

提交最终名单时，请列出你认为属于罕见共病交集 I 的所有患者代号（用逗号隔开，顺序不限）。如果没有符合条件的患者，则答案为空字符串。格式如下：

<answer>A,C,E</answer>

或（无符合条件患者情况）：

<answer></answer>

请尽可能用最少的查询次数找到确切名单。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Rare Comorbidity Clinical Diagnosis Support System".

The system has registered a clinical cohort U containing {n} patients, labeled with unordered identifiers: {elements}. There is no physiological sequence or contagion relationship among these patients.

The system has secretly determined four clinical feature subsets S1 (Hypertension), S2 (Diabetes), S3 (Hyperlipidemia), S4 (Specific Gene Mutation), all of which are subsets of U. These four feature subsets are fixed before the diagnosis starts and remain unchanged throughout the screening process.

Your goal is: to find the intersection I of these four clinical feature subsets, i.e., all rare comorbidity patients who simultaneously possess features S1, S2, S3, and S4 (the intersection may be empty).

You can ask me the following two types of queries, and I will answer truthfully based on the electronic medical records:

1. Single Patient Indicator Test: Ask whether a patient x possesses a specific clinical feature Si (i is an integer between 1 and 4). Answer "Yes" or "No".

2. Patient Cohort Feature Count: Given a patient subset S and one or more feature indices T (T is a non-empty subset of 1, 2, 3, 4), ask how many patients in S simultaneously possess all corresponding clinical features in T. Answer an integer.

When you have collected enough information, submit your final confirmed list. If the list is incorrect, the format is invalid, or the query limit is exceeded, the diagnostic task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Single Patient Indicator Test (e.g., asking if patient A possesses clinical feature S2):
<query_member>A,2</query_member>

- Patient Cohort Feature Count (e.g., asking how many patients in cohort A,B,C possess both features S1 and S3):
<query_count>elements=A,B,C;attributes=1,3</query_count>

Note: In the patient cohort feature count, elements is the list of patients to query (comma-separated), and attributes is the list of clinical feature indices (comma-separated, must contain at least one feature).

When submitting the final list, list all patient identifiers you believe belong to the rare comorbidity intersection I (comma-separated, order does not matter). If there are no such patients, the answer should be an empty string. Format:

<answer>A,C,E</answer>

Or (for empty set):

<answer></answer>

Please find the exact list with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“拔尖创新人才选拔分析系统”。

系统收录了一个包含 {n} 名候选学生的档案库 U，学生用无序代号标记：{elements}。这些学生之间没有任何排名或年级先后关系。

系统已经秘密确定了四个能力达标子集 S1（高等数学优秀）、S2（物理竞赛获奖）、S3（编程能力认证）、S4（英语六级达标），它们都是 U 的子集。这四个达标子集在选拔开始前已固定，且在整个评估过程中保持不变。

你的目标是：找出这四个能力达标子集的交集 I，即同时满足 S1、S2、S3、S4 四项评定条件的拔尖创新候选人（交集可能为空集）。

你可以向我提出以下两类查询，我会根据教务考核系统如实回答：

1. 单学生资质测试：询问某名学生 x 是否满足某项能力条件 Si（i 为 1 到 4 之间的整数）。回答"是"或"否"。

2. 学生群组达标计数：给定一个学生子集 S 和一个或多个条件索引集合 T（T 是 1、2、3、4 的非空子集），询问 S 中有多少名学生同时满足 T 中所有对应的能力条件。回答一个整数。

当你收集足够信息后，请提交最终选拔名单。若名单错误、格式不符或超过查询次数上限，选拔任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单学生资质测试（例如询问学生 A 是否满足能力条件 S2）：
<query_member>A,2</query_member>

- 学生群组达标计数（例如询问学生 A,B,C 中有多少人同时满足条件 S1 和 S3）：
<query_count>elements=A,B,C;attributes=1,3</query_count>

注意：学生群组达标计数中，elements 为要查询的学生列表（用逗号分隔），attributes 为能力条件索引列表（用逗号分隔，至少包含一项条件）。

提交最终名单时，请列出你认为属于拔尖创新人才交集 I 的所有学生代号（用逗号隔开，顺序不限）。如果没有符合条件的学生，则答案为空字符串。格式如下：

<answer>A,C,E</answer>

或（无符合条件学生情况）：

<answer></answer>

请尽可能用最少的查询次数找到确切名单。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Top Innovative Talent Selection Analysis System".

The system includes a database U containing {n} candidate students, labeled with unordered identifiers: {elements}. There is no ranking or grade seniority relationship among these students.

The system has secretly determined four competency fulfillment subsets S1 (Advanced Math Excellence), S2 (Physics Competition Award), S3 (Programming Certification), S4 (CET-6 Proficiency), all of which are subsets of U. These four subsets are fixed before the selection starts and remain unchanged throughout the evaluation process.

Your goal is: to find the intersection I of these four competency subsets, i.e., all top innovative candidates who simultaneously meet criteria S1, S2, S3, and S4 (the intersection may be empty).

You can ask me the following two types of queries, and I will answer truthfully based on the academic assessment system:

1. Single Student Qualification Test: Ask whether a student x meets a specific competency criterion Si (i is an integer between 1 and 4). Answer "Yes" or "No".

2. Student Group Fulfillment Count: Given a student subset S and one or more criterion indices T (T is a non-empty subset of 1, 2, 3, 4), ask how many students in S simultaneously meet all corresponding competency criteria in T. Answer an integer.

When you have collected enough information, submit your final selection list. If the list is incorrect, the format is invalid, or the query limit is exceeded, the selection task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Single Student Qualification Test (e.g., asking if student A meets competency criterion S2):
<query_member>A,2</query_member>

- Student Group Fulfillment Count (e.g., asking how many students in group A,B,C meet both criteria S1 and S3):
<query_count>elements=A,B,C;attributes=1,3</query_count>

Note: In the student group fulfillment count, elements is the list of students to query (comma-separated), and attributes is the list of competency criterion indices (comma-separated, must contain at least one criterion).

When submitting the final list, list all student identifiers you believe belong to the top talent intersection I (comma-separated, order does not matter). If there are no such students, the answer should be an empty string. Format:

<answer>A,C,E</answer>

Or (for empty set):

<answer></answer>

Please find the exact list with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业零部件联合质检追溯系统”。

系统接入了一个包含 {n} 批次零部件的生产批次集合 U，批次用无序代号标记：{elements}。这些批次之间没有任何生产线先后或装配层级关系。

系统已经秘密确定了四个潜在缺陷子集 S1（尺寸超标）、S2（表面划痕）、S3（硬度不达标）、S4（材质疲劳），它们都是 U 的子集。这四个缺陷子集在质检开始前已固定，且在整个排查过程中保持不变。

你的目标是：找出这四个缺陷子集的交集 I，即同时存在 S1、S2、S3、S4 四种致命缺陷的必须报废批次（交集可能为空集）。

你可以向我提出以下两类查询，我会根据自动化质检日志如实回答：

1. 单批次缺陷测试：询问某批次零部件 x 是否存在某种缺陷 Si（i 为 1 到 4 之间的整数）。回答"是"或"否"。

2. 批次组合缺陷计数：给定一个批次子集 S 和一个或多个缺陷索引集合 T（T 是 1、2、3、4 的非空子集），询问 S 中有多少个批次同时存在 T 中所有对应的缺陷。回答一个整数。

当你收集足够信息后，请提交最终追溯名单。若名单错误、格式不符或超过查询次数上限，质检任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单批次缺陷测试（例如询问批次 A 是否存在缺陷 S2）：
<query_member>A,2</query_member>

- 批次组合缺陷计数（例如询问批次 A,B,C 中有多少个同时存在缺陷 S1 和 S3）：
<query_count>elements=A,B,C;attributes=1,3</query_count>

注意：批次组合缺陷计数中，elements 为要查询的批次列表（用逗号分隔），attributes 为缺陷索引列表（用逗号分隔，至少包含一种缺陷）。

提交最终名单时，请列出你认为属于致命报废交集 I 的所有批次代号（用逗号隔开，顺序不限）。如果没有符合条件的批次，则答案为空字符串。格式如下：

<answer>A,C,E</answer>

或（无符合条件批次情况）：

<answer></answer>

请尽可能用最少的查询次数找到确切名单。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Component Joint Quality Inspection Traceability System".

The system accesses a production batch set U containing {n} batches of components, labeled with unordered identifiers: {elements}. There is no assembly line sequence or hierarchical relationship among these batches.

The system has secretly determined four potential defect subsets S1 (Oversized), S2 (Surface Scratches), S3 (Substandard Hardness), S4 (Material Fatigue), all of which are subsets of U. These four defect subsets are fixed before the inspection starts and remain unchanged throughout the troubleshooting process.

Your goal is: to find the intersection I of these four defect subsets, i.e., the critical scrap batches that simultaneously possess defects S1, S2, S3, and S4 (the intersection may be empty).

You can ask me the following two types of queries, and I will answer truthfully based on automated quality inspection logs:

1. Single Batch Defect Test: Ask whether a component batch x has a specific defect Si (i is an integer between 1 and 4). Answer "Yes" or "No".

2. Batch Combination Defect Count: Given a batch subset S and one or more defect indices T (T is a non-empty subset of 1, 2, 3, 4), ask how many batches in S simultaneously possess all corresponding defects in T. Answer an integer.

When you have collected enough information, submit your final traceability list. If the list is incorrect, the format is invalid, or the query limit is exceeded, the quality inspection task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Single Batch Defect Test (e.g., asking if batch A has defect S2):
<query_member>A,2</query_member>

- Batch Combination Defect Count (e.g., asking how many batches in A,B,C possess both defects S1 and S3):
<query_count>elements=A,B,C;attributes=1,3</query_count>

Note: In the batch combination defect count, elements is the list of batches to query (comma-separated), and attributes is the list of defect indices (comma-separated, must contain at least one defect).

When submitting the final list, list all batch identifiers you believe belong to the critical scrap intersection I (comma-separated, order does not matter). If there are no such batches, the answer should be an empty string. Format:

<answer>A,C,E</answer>

Or (for empty set):

<answer></answer>

Please find the exact list with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“核心嫌疑人证据链综合研判系统”。

系统导入了一个包含 {n} 个涉案主体的档案库 U，主体用无序代号标记：{elements}。这些主体之间没有任何从属、上下级或物理距离关联。

系统已经秘密确定了四个关键证据维度子集 S1（具备作案动机）、S2（在案发现场）、S3（作案工具指纹匹配）、S4（资金流向异常），它们都是 U 的子集。这四个证据子集在研判开始前已固定，且在整个侦查过程中保持不变。

你的目标是：找出这四个证据维度子集的交集 I，即同时满足 S1、S2、S3、S4 四大证据闭环的核心嫌疑人（交集可能为空集）。

你可以向我提出以下两类查询，我会根据法证鉴定结果如实回答：

1. 单主体证据测试：询问某涉案主体 x 是否符合某项证据维度 Si（i 为 1 到 4 之间的整数）。回答"是"或"否"。

2. 主体群组证据计数：给定一个主体子集 S 和一个或多个证据维度索引集合 T（T 是 1、2、3、4 的非空子集），询问 S 中有多少个主体同时符合 T 中所有对应的证据维度。回答一个整数。

当你收集足够信息后，请提交最终锁定名单。若名单错误、格式不符或超过查询次数上限，研判任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单主体证据测试（例如询问主体 A 是否符合证据维度 S2）：
<query_member>A,2</query_member>

- 主体群组证据计数（例如询问主体 A,B,C 中有多少人同时符合维度 S1 和 S3）：
<query_count>elements=A,B,C;attributes=1,3</query_count>

注意：主体群组证据计数中，elements 为要查询的主体列表（用逗号分隔），attributes 为证据维度索引列表（用逗号分隔，至少包含一个维度）。

提交最终名单时，请列出你认为属于核心嫌疑人交集 I 的所有主体代号（用逗号隔开，顺序不限）。如果没有符合条件的主体，则答案为空字符串。格式如下：

<answer>A,C,E</answer>

或（无符合条件主体情况）：

<answer></answer>

请尽可能用最少的查询次数锁定确切名单。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Core Suspect Evidence Chain Comprehensive Analysis System".

The system has imported a database U containing {n} involved subjects, labeled with unordered identifiers: {elements}. There is no subordination, hierarchical, or physical distance relationship among these subjects.

The system has secretly determined four key evidence dimension subsets S1 (Motive Present), S2 (At the Crime Scene), S3 (Weapon Fingerprint Match), S4 (Abnormal Fund Flow), all of which are subsets of U. These four evidence subsets are fixed before the analysis starts and remain unchanged throughout the investigation.

Your goal is: to find the intersection I of these four evidence subsets, i.e., the core suspects who simultaneously complete the evidence loop of S1, S2, S3, and S4 (the intersection may be empty).

You can ask me the following two types of queries, and I will answer truthfully based on forensic identification results:

1. Single Subject Evidence Test: Ask whether a subject x meets a specific evidence dimension Si (i is an integer between 1 and 4). Answer "Yes" or "No".

2. Subject Group Evidence Count: Given a subject subset S and one or more evidence dimension indices T (T is a non-empty subset of 1, 2, 3, 4), ask how many subjects in S simultaneously meet all corresponding evidence dimensions in T. Answer an integer.

When you have collected enough information, submit your final lockdown list. If the list is incorrect, the format is invalid, or the query limit is exceeded, the analysis task fails.

## Query and Answer Format (must be strictly followed)

Each query must contain only one tag. Use the following XML format:

- Single Subject Evidence Test (e.g., asking if subject A meets evidence dimension S2):
<query_member>A,2</query_member>

- Subject Group Evidence Count (e.g., asking how many subjects in group A,B,C meet both dimensions S1 and S3):
<query_count>elements=A,B,C;attributes=1,3</query_count>

Note: In the subject group evidence count, elements is the list of subjects to query (comma-separated), and attributes is the list of evidence dimension indices (comma-separated, must contain at least one dimension).

When submitting the final list, list all subject identifiers you believe belong to the core suspect intersection I (comma-separated, order does not matter). If there are no such subjects, the answer should be an empty string. Format:

<answer>A,C,E</answer>

Or (for empty set):

<answer></answer>

Please lock down the exact list with as few queries as possible.
"""

    tags = ["answer", "query_member", "query_count"]

    # 难度配置：
    # 1 (easy)       - N=8, 询问上限=10, 交集大小=2
    # 2 (medium-low) - N=10, 询问上限=9, 交集大小=1
    # 3 (medium-high)- N=12, 询问上限=9, 交集大小=2
    # 4 (hard)       - N=12, 询问上限=8, 交集大小=0（空集）
    # 5 (very hard)  - N=15, 询问上限=10, 交集大小=3

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "max_queries": 10,
                "S1": ["A", "B", "C", "D"],
                "S2": ["B", "C", "D", "F"],
                "S3": ["C", "D", "E", "G"],
                "S4": ["A", "C", "D", "H"],
                "answer": ["C", "D"],  # 交集
            },
            2: {
                "n": 10,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "max_queries": 9,
                "S1": ["A", "C", "E", "G", "I"],
                "S2": ["C", "D", "F", "H", "J"],
                "S3": ["B", "C", "E", "H"],
                "S4": ["C", "F", "G", "I"],
                "answer": ["C"],
            },
            3: {
                "n": 12,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "max_queries": 9,
                "S1": ["A", "B", "C", "D", "E", "F"],
                "S2": ["B", "D", "E", "G", "H", "I"],
                "S3": ["C", "D", "E", "J", "K"],
                "S4": ["D", "E", "F", "H", "L"],
                "answer": ["D", "E"],
            },
            4: {
                "n": 12,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "max_queries": 8,
                "S1": ["A", "B", "C", "D"],
                "S2": ["E", "F", "G", "H"],
                "S3": ["I", "J", "K"],
                "S4": ["L", "A", "E", "I"],
                "answer": [],  # 空集
            },
            5: {
                "n": 15,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
                "max_queries": 10,
                "S1": ["A", "C", "E", "G", "I", "K", "M"],
                "S2": ["B", "C", "F", "G", "J", "K", "N"],
                "S3": ["C", "D", "G", "H", "K", "L"],
                "S4": ["C", "E", "G", "I", "K", "O"],
                "answer": ["C", "G", "K"],
            },
        },
        "en": {
            1: {
                "n": 8,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "max_queries": 10,
                "S1": ["A", "B", "C", "D"],
                "S2": ["B", "C", "D", "F"],
                "S3": ["C", "D", "E", "G"],
                "S4": ["A", "C", "D", "H"],
                "answer": ["C", "D"],
            },
            2: {
                "n": 10,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "max_queries": 9,
                "S1": ["A", "C", "E", "G", "I"],
                "S2": ["C", "D", "F", "H", "J"],
                "S3": ["B", "C", "E", "H"],
                "S4": ["C", "F", "G", "I"],
                "answer": ["C"],
            },
            3: {
                "n": 12,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "max_queries": 9,
                "S1": ["A", "B", "C", "D", "E", "F"],
                "S2": ["B", "D", "E", "G", "H", "I"],
                "S3": ["C", "D", "E", "J", "K"],
                "S4": ["D", "E", "F", "H", "L"],
                "answer": ["D", "E"],
            },
            4: {
                "n": 12,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"],
                "max_queries": 8,
                "S1": ["A", "B", "C", "D"],
                "S2": ["E", "F", "G", "H"],
                "S3": ["I", "J", "K"],
                "S4": ["L", "A", "E", "I"],
                "answer": [],
            },
            5: {
                "n": 15,
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O"],
                "max_queries": 10,
                "S1": ["A", "C", "E", "G", "I", "K", "M"],
                "S2": ["B", "C", "F", "G", "J", "K", "N"],
                "S3": ["C", "D", "G", "H", "K", "L"],
                "S4": ["C", "E", "G", "I", "K", "O"],
                "answer": ["C", "G", "K"],
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 记录询问次数
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["elements"] = ", ".join(cfg["elements"])
        
        # 初始化游戏数据
        self.elements = cfg["elements"]
        self.max_queries = cfg["max_queries"]
        self.S1 = set(cfg["S1"])
        self.S2 = set(cfg["S2"])
        self.S3 = set(cfg["S3"])
        self.S4 = set(cfg["S4"])
        self.attribute_sets = [self.S1, self.S2, self.S3, self.S4]
        
        # 计算真实交集
        self.true_answer = set(cfg["answer"])

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 处理空集情况
        if not raw_ans:
            model_answer = set()
        else:
            # 解析模型提交的答案
            model_answer = set(x.strip() for x in raw_ans.split(",") if x.strip())
        
        # 检查答案是否完全匹配
        return model_answer == self.true_answer

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或参数错误。"
            error_element = "错误：元素不在集合中。"
            error_attribute = "错误：属性索引必须是1到4之间的整数。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or parameters."
            error_element = "Error: Element not in set."
            error_attribute = "Error: Attribute index must be between 1 and 4."

        # 先确认存在有效查询标签，再递增计数
        has_query = "query_member" in parsed_info or "query_count" in parsed_info
        if not has_query:
            raise ValueError("No valid query tag found.")

        # 检查是否超过询问次数上限
        self.query_count += 1
        if self.query_count > self.max_queries:
            if self.config.language == "zh":
                raise ValueError(f"已超过询问次数上限（{self.max_queries}次）")
            else:
                raise ValueError(f"Query limit exceeded ({self.max_queries} queries)")

        # 处理单元素成员测试
        if "query_member" in parsed_info:
            try:
                raw = parsed_info["query_member"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                element, attr_idx = parts[0], parts[1]
                
                # 验证元素是否有效
                if element not in self.elements:
                    return error_element
                
                # 验证属性索引是否有效
                try:
                    idx = int(attr_idx)
                    if idx < 1 or idx > 4:
                        return error_attribute
                except ValueError:
                    return error_attribute
                
                # 检查元素是否在对应的属性子集中
                is_member = element in self.attribute_sets[idx - 1]
                return yes_res if is_member else no_res
                
            except Exception:
                return error_format

        # 处理子集交集计数
        elif "query_count" in parsed_info:
            try:
                raw = parsed_info["query_count"].strip()
                
                # 解析 elements=A,B,C;attributes=1,3 格式
                parts = raw.split(";")
                if len(parts) != 2:
                    return error_format
                
                elements_part = parts[0].strip()
                attributes_part = parts[1].strip()
                
                # 提取元素列表
                if not elements_part.startswith("elements="):
                    return error_format
                elements_str = elements_part[9:]  # 去掉 "elements="
                query_elements = [x.strip() for x in elements_str.split(",") if x.strip()]
                
                # 验证所有元素是否有效
                for elem in query_elements:
                    if elem not in self.elements:
                        return error_element
                
                # 提取属性索引列表
                if not attributes_part.startswith("attributes="):
                    return error_format
                attributes_str = attributes_part[11:]  # 去掉 "attributes="
                attr_indices = [x.strip() for x in attributes_str.split(",") if x.strip()]
                
                if not attr_indices:
                    return error_format
                
                # 验证并转换属性索引
                try:
                    attr_nums = [int(idx) for idx in attr_indices]
                    for num in attr_nums:
                        if num < 1 or num > 4:
                            return error_attribute
                except ValueError:
                    return error_attribute
                
                # 计算交集
                # 从查询的元素集合开始
                result_set = set(query_elements)
                # 与所有指定的属性子集求交集
                for attr_idx in attr_nums:
                    result_set = result_set.intersection(self.attribute_sets[attr_idx - 1])
                
                return str(len(result_set))
                
            except Exception:
                return error_format

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是": return "否"
        if correct == "否": return "是"
        if correct.lower() == "yes": return "No"
        if correct.lower() == "no": return "Yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        
        策略：
        1. 枚举所有【单元素成员测试】：这是游戏的基础原子信息。
        2. 枚举针对【全集U】的【子集交集计数】：对于所有可能的非空属性组合T，
           查询全集U中有多少元素同时属于T中的属性。这提供了宏观的交集分布信息。
           注：不枚举任意子集S的计数查询，因为组合数量呈指数级爆炸(2^N)，且通常通过单元素测试已足够推断。
        
        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 完整的 XML 查询字符串
                "answer": str,   # 对应的正确答案
            }
        """
        queries = []
        
        # 设置语言对应的回答
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 1. 枚举所有单元素成员测试 (query_member)
        # 格式: <query_member>element,attr_idx</query_member>
        for elem in self.elements:
            for attr_idx in range(1, 5):
                # 构造内部内容和完整XML
                content = f"{elem},{attr_idx}"
                xml_query = f"<query_member>{content}</query_member>"
                
                # 计算逻辑：直接检查集合成员资格
                is_member = elem in self.attribute_sets[attr_idx - 1]
                ans = yes_res if is_member else no_res
                
                queries.append({
                    "query": xml_query,
                    "answer": ans
                })

        # 2. 枚举针对全集U的所有属性组合的交集计数 (query_count)
        # 格式: <query_count>elements=ALL;attributes=ATTRS</query_count>
        all_elements_str = ",".join(self.elements)
        full_set = set(self.elements)
        
        # 属性索引集合为 {1, 2, 3, 4}，枚举所有非空子集 T
        for r in range(1, 5):
            for attrs in itertools.combinations(range(1, 5), r):
                attrs_str = ",".join(map(str, attrs))
                
                # 构造内部内容和完整XML
                content = f"elements={all_elements_str};attributes={attrs_str}"
                xml_query = f"<query_count>{content}</query_count>"
                
                # 计算逻辑：全集与指定属性集的交集大小
                result_set = full_set.copy()
                for idx in attrs:
                    result_set = result_set.intersection(self.attribute_sets[idx - 1])
                
                ans = str(len(result_set))
                
                queries.append({
                    "query": xml_query,
                    "answer": ans
                })

        return queries