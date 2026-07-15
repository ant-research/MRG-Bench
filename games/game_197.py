from .base import Game
import random
import itertools

class MinSetCoverGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "集合"

    game_rule_zh = """\
我们来玩一个"最小集合覆盖推理"游戏，规则如下：

存在一个隐藏的元素集合 U，包含若干个元素（记为 E1, E2, ...），以及若干个子集 S1, S2, ...，每个子集覆盖 U 中的部分元素。保证至少存在一种方式，用这些子集的并集完全覆盖 U。

你的目标是：找出最小集合覆盖，即用最少数量的子集完全覆盖所有元素，并提交该最小数量及具体选择的子集编号。

你可以通过以下五种查询方式获取信息（每次只能提一个问题）：

1. 单集揭示：询问某个子集包含哪些元素。
2. 多集并集计数：询问若干个子集的并集包含多少个元素。
3. 两组覆盖比较：比较两组子集的并集，哪一组覆盖的元素更多。
4. 可行性边界：询问是否存在不超过 k 个子集的完整覆盖方案。
5. 局部增量价值：询问在已有若干子集的基础上，新增某个子集能额外覆盖多少个新元素。

当你收集足够信息后，请提交最终答案。答案必须包含最小覆盖大小和具体子集编号。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单集揭示（例如查询 S1）：
<query_reveal>S1</query_reveal>

- 多集并集计数（例如查询 S1, S2, S3 的并集大小）：
<query_union_count>S1,S2,S3</query_union_count>

- 两组覆盖比较（例如比较组 [S1,S2] 与组 [S3,S4]）：
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- 可行性边界（例如询问是否存在不超过 3 个子集的覆盖）：
<query_feasible>3</query_feasible>

- 局部增量价值（例如在 [S1,S2] 基础上加入 S3 新增多少元素）：
<query_incremental>S1,S2|S3</query_incremental>

提交最终答案时，必须指明最小覆盖大小和子集列表（用逗号隔开），格式如下：
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    game_rule_en = """\
Let's play a "Minimum Set Cover Reasoning" game. Here are the rules:

There exists a hidden element set U containing several elements (denoted as E1, E2, ...), and several subsets S1, S2, ..., each covering some elements in U. It is guaranteed that at least one combination of these subsets can completely cover U.

Your goal is: find the minimum set cover, i.e., use the smallest number of subsets to completely cover all elements, and submit both the minimum size and the specific subset indices.

You can obtain information through five types of queries (one question per turn):

1. Reveal Single Set: Ask which elements a specific subset contains.
2. Union Count: Ask how many elements are covered by the union of several subsets.
3. Compare Two Groups: Compare two groups of subsets to determine which covers more elements.
4. Feasibility Bound: Ask whether there exists a complete cover using at most k subsets.
5. Incremental Value: Ask how many new elements would be covered by adding a specific subset to an existing collection.

When you have enough information, submit your final answer. The answer must include the minimum cover size and specific subset indices.

Each query must contain only one tag. Use the following XML format:

- Reveal Single Set (e.g., query S1):
<query_reveal>S1</query_reveal>

- Union Count (e.g., query union size of S1, S2, S3):
<query_union_count>S1,S2,S3</query_union_count>

- Compare Two Groups (e.g., compare group [S1,S2] with group [S3,S4]):
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- Feasibility Bound (e.g., ask if cover with at most 3 subsets exists):
<query_feasible>3</query_feasible>

- Incremental Value (e.g., new elements when adding S3 to [S1,S2]):
<query_incremental>S1,S2|S3</query_incremental>

When submitting the final answer, specify the minimum cover size and subset list (comma-separated), using this format:
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"城市交通监控网络最小化"推理游戏，规则如下：

在一个大型城市中，存在一个隐藏的关键路口集合 U，包含若干个需要监控的核心路口（记为 E1, E2, ...），以及若干个可部署的监控基站 S1, S2, ...。每个基站由于物理位置和视野限制，只能覆盖 U 中的部分路口。系统保证至少存在一种部署方案，用这些基站的并集能够完全监控所有的关键路口。

你的目标是：找出最小监控覆盖方案，即部署最少数量的基站，完全监控所有关键路口，并提交该最小数量及具体选择的基站编号。

你可以通过以下五种查询方式获取网络拓扑信息（每次只能提一个问题）：

1. 单站覆盖揭示：询问某个基站具体监控哪些路口。
2. 多站联合覆盖计数：询问若干个基站组成的网络共能监控多少个路口。
3. 两组方案覆盖比较：比较两组基站部署方案，哪一组监控的路口更多。
4. 部署可行性边界：询问是否存在不超过 k 个基站的完整监控方案。
5. 局部增量覆盖价值：询问在已部署若干基站的基础上，新增某个基站能额外监控多少个新路口。

当你收集足够信息后，请提交最终答案。答案必须包含最小基站数量和具体基站编号。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单站覆盖揭示（例如查询 S1）：
<query_reveal>S1</query_reveal>

- 多站联合覆盖计数（例如查询 S1, S2, S3 的联合监控数量）：
<query_union_count>S1,S2,S3</query_union_count>

- 两组方案覆盖比较（例如比较组 [S1,S2] 与组 [S3,S4]）：
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- 部署可行性边界（例如询问是否存在不超过 3 个基站的完整监控方案）：
<query_feasible>3</query_feasible>

- 局部增量覆盖价值（例如在 [S1,S2] 基础上加入 S3 新增监控多少路口）：
<query_incremental>S1,S2|S3</query_incremental>

提交最终答案时，必须指明最小覆盖大小和基站列表（用逗号隔开），格式如下：
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Urban Traffic Surveillance Minimization" reasoning game. Here are the rules:

In a large city, there exists a hidden set U of critical intersections (denoted as E1, E2, ...) that require surveillance, along with several deployable surveillance base stations S1, S2, .... Due to physical locations and field-of-view limits, each base station can only monitor some intersections in U. It is guaranteed that at least one combination of these base stations can completely monitor all critical intersections.

Your goal is: find the minimum surveillance cover, i.e., use the smallest number of base stations to completely monitor all critical intersections, and submit both the minimum size and the specific base station indices.

You can obtain network topology information through five types of queries (one question per turn):

1. Reveal Single Station Coverage: Ask which intersections a specific base station monitors.
2. Union Coverage Count: Ask how many intersections are monitored by the union of several base stations.
3. Compare Two Deployment Groups: Compare two groups of base stations to determine which monitors more intersections.
4. Deployment Feasibility Bound: Ask whether there exists a complete monitoring scheme using at most k base stations.
5. Incremental Coverage Value: Ask how many new intersections would be monitored by adding a specific base station to an existing network.

When you have enough information, submit your final answer. The answer must include the minimum cover size and specific base station indices.

Each query must contain only one tag. Use the following XML format:

- Reveal Single Station Coverage (e.g., query S1):
<query_reveal>S1</query_reveal>

- Union Coverage Count (e.g., query union size of S1, S2, S3):
<query_union_count>S1,S2,S3</query_union_count>

- Compare Two Deployment Groups (e.g., compare group [S1,S2] with group [S3,S4]):
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- Deployment Feasibility Bound (e.g., ask if a complete scheme with at most 3 stations exists):
<query_feasible>3</query_feasible>

- Incremental Coverage Value (e.g., new intersections when adding S3 to [S1,S2]):
<query_incremental>S1,S2|S3</query_incremental>

When submitting the final answer, specify the minimum cover size and base station list (comma-separated), using this format:
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"精准联合用药最小化"推理游戏，规则如下：

在一次复杂的感染病例中，存在一个隐藏的病原体集合 U，包含若干种必须被清除的病原微生物（记为 E1, E2, ...），以及若干种可选的联合用药方案/抗生素 S1, S2, ...。每种药物具有不同的抗菌谱，能够覆盖 U 中的部分病原体。医学指南保证至少存在一种联合用药方式，能够完全杀灭 U 中的所有病原体。

你的目标是：找出最小药物覆盖组合，即开具最少数量的药物种类来完全清除所有病原体（以降低副作用和耐药性风险），并提交该最小数量及具体的药物编号。

你可以通过以下五种查询方式获取药理信息（每次只能提一个问题）：

1. 单药抗菌谱揭示：询问某种药物具体覆盖哪些病原体。
2. 联合用药覆盖计数：询问若干种药物联合使用共能杀灭多少种病原体。
3. 两组处方覆盖比较：比较两组用药方案，哪一组能覆盖更多的病原体。
4. 处方可行性边界：询问是否存在不超过 k 种药物的完整清除方案。
5. 局部增量治疗价值：询问在已有若干药物的基础上，追加某种药物能额外杀灭多少种新病原体。

当你收集足够信息后，请提交最终答案。答案必须包含最小药物数量和具体药物编号。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单药抗菌谱揭示（例如查询药物 S1）：
<query_reveal>S1</query_reveal>

- 联合用药覆盖计数（例如查询 S1, S2, S3 的联合覆盖数量）：
<query_union_count>S1,S2,S3</query_union_count>

- 两组处方覆盖比较（例如比较组 [S1,S2] 与组 [S3,S4]）：
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- 处方可行性边界（例如询问是否存在不超过 3 种药物的完整清除方案）：
<query_feasible>3</query_feasible>

- 局部增量治疗价值（例如在 [S1,S2] 基础上加入 S3 新增覆盖多少种病原体）：
<query_incremental>S1,S2|S3</query_incremental>

提交最终答案时，必须指明最小覆盖大小和药物列表（用逗号隔开），格式如下：
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Precision Combination Therapy Minimization" reasoning game. Here are the rules:

In a complex infection case, there exists a hidden set U of pathogens (denoted as E1, E2, ...) that must be eradicated, along with several optional antibiotic regimens S1, S2, .... Each medication has a distinct antimicrobial spectrum, covering some pathogens in U. Medical guidelines guarantee that at least one combination of these medications can completely eradicate all pathogens in U.

Your goal is: find the minimum medication cover, i.e., prescribe the smallest number of medications to completely clear all pathogens (minimizing side effects and resistance risks), and submit both the minimum size and the specific medication indices.

You can obtain pharmacological information through five types of queries (one question per turn):

1. Reveal Single Medication Spectrum: Ask which pathogens a specific medication covers.
2. Combination Therapy Count: Ask how many pathogens are eradicated by the union of several medications.
3. Compare Two Prescription Groups: Compare two medication groups to determine which covers more pathogens.
4. Prescription Feasibility Bound: Ask whether there exists a complete eradication scheme using at most k medications.
5. Incremental Therapeutic Value: Ask how many new pathogens would be eradicated by adding a specific medication to an existing regimen.

When you have enough information, submit your final answer. The answer must include the minimum cover size and specific medication indices.

Each query must contain only one tag. Use the following XML format:

- Reveal Single Medication Spectrum (e.g., query S1):
<query_reveal>S1</query_reveal>

- Combination Therapy Count (e.g., query union size of S1, S2, S3):
<query_union_count>S1,S2,S3</query_union_count>

- Compare Two Prescription Groups (e.g., compare group [S1,S2] with group [S3,S4]):
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- Prescription Feasibility Bound (e.g., ask if a complete scheme with at most 3 medications exists):
<query_feasible>3</query_feasible>

- Incremental Therapeutic Value (e.g., new pathogens when adding S3 to [S1,S2]):
<query_incremental>S1,S2|S3</query_incremental>

When submitting the final answer, specify the minimum cover size and medication list (comma-separated), using this format:
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"核心课程体系最小化"推理游戏，规则如下：

在某项职业认证考试中，存在一个隐藏的考纲知识点集合 U，包含若干个必须掌握的核心考点（记为 E1, E2, ...），以及若干门可供选修的综合性课程模块 S1, S2, ...。每门课程由于侧重点不同，只能覆盖 U 中的部分考点。教学主管保证至少存在一种选课组合，能够让学生完全覆盖所有的必考考点。

你的目标是：找出最小课程覆盖方案，即为学生规划最少数量的选修课程来完全覆盖所有核心考点（以最大化学习效率），并提交该最小数量及具体的课程编号。

你可以通过以下五种查询方式获取教学大纲信息（每次只能提一个问题）：

1. 单课考点揭示：询问某门课程具体涵盖哪些考点。
2. 多课联合考点计数：询问若干门课程的组合共能涵盖多少个考点。
3. 两组选课覆盖比较：比较两组选课方案，哪一组涵盖的考点更多。
4. 学习可行性边界：询问是否存在不超过 k 门课程的完整考点覆盖方案。
5. 局部增量学习价值：询问在已修读若干课程的基础上，加修某门课程能额外学到多少个新考点。

当你收集足够信息后，请提交最终答案。答案必须包含最小覆盖大小和具体课程编号。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单课考点揭示（例如查询课程 S1）：
<query_reveal>S1</query_reveal>

- 多课联合考点计数（例如查询 S1, S2, S3 的联合考点数量）：
<query_union_count>S1,S2,S3</query_union_count>

- 两组选课覆盖比较（例如比较组 [S1,S2] 与组 [S3,S4]）：
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- 学习可行性边界（例如询问是否存在不超过 3 门课程的完整覆盖方案）：
<query_feasible>3</query_feasible>

- 局部增量学习价值（例如在 [S1,S2] 基础上加修 S3 新增覆盖多少考点）：
<query_incremental>S1,S2|S3</query_incremental>

提交最终答案时，必须指明最小课程数量和课程列表（用逗号隔开），格式如下：
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Core Curriculum Minimization" reasoning game. Here are the rules:

In a professional certification exam, there exists a hidden set U of syllabus topics (denoted as E1, E2, ...) that must be mastered, along with several elective course modules S1, S2, .... Due to different academic focuses, each course only covers some topics in U. The academic director guarantees that at least one combination of these courses can completely cover all required topics.

Your goal is: find the minimum curriculum cover, i.e., plan the smallest number of elective courses to completely cover all core topics (to maximize learning efficiency), and submit both the minimum size and the specific course indices.

You can obtain syllabus information through five types of queries (one question per turn):

1. Reveal Single Course Topics: Ask which topics a specific course covers.
2. Combined Course Topics Count: Ask how many topics are covered by the union of several courses.
3. Compare Two Curriculum Groups: Compare two course groups to determine which covers more topics.
4. Study Feasibility Bound: Ask whether there exists a complete topic coverage scheme using at most k courses.
5. Incremental Learning Value: Ask how many new topics would be covered by adding a specific course to an existing study plan.

When you have enough information, submit your final answer. The answer must include the minimum cover size and specific course indices.

Each query must contain only one tag. Use the following XML format:

- Reveal Single Course Topics (e.g., query S1):
<query_reveal>S1</query_reveal>

- Combined Course Topics Count (e.g., query union size of S1, S2, S3):
<query_union_count>S1,S2,S3</query_union_count>

- Compare Two Curriculum Groups (e.g., compare group [S1,S2] with group [S3,S4]):
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- Study Feasibility Bound (e.g., ask if a complete scheme with at most 3 courses exists):
<query_feasible>3</query_feasible>

- Incremental Learning Value (e.g., new topics when adding S3 to [S1,S2]):
<query_incremental>S1,S2|S3</query_incremental>

When submitting the final answer, specify the minimum cover size and course list (comma-separated), using this format:
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"工业模块化装配最小化"推理游戏，规则如下：

在一条高端制造装配线中，存在一个隐藏的核心零部件需求集合 U（记为 E1, E2, ...），以及若干个由供应商提供的标准化集成套件 S1, S2, ...。每个集成套件包含 U 中的部分零部件。供应链协议保证，至少存在一种采购组合，通过合并这些集成套件能够凑齐所有必须的零部件。

你的目标是：找出最小套件采购覆盖，即采购最少数量的标准化套件来完全满足所有零部件需求（以降低物流和库存管理成本），并提交该最小数量及具体的套件编号。

你可以通过以下五种查询方式获取供应链信息（每次只能提一个问题）：

1. 单套件清单揭示：询问某个集成套件具体包含哪些零部件。
2. 多套件联合计数：询问若干个套件组合在一起共包含多少种去重后的零部件。
3. 两组采购方案比较：比较两组采购方案，哪一组涵盖的零部件种类更多。
4. 采购可行性边界：询问是否存在不超过 k 个套件的完整物料采购方案。
5. 局部增量装配价值：询问在已采购若干套件的基础上，增购某个套件能额外提供多少种新的零部件。

当你收集足够信息后，请提交最终答案。答案必须包含最小套件数量和具体套件编号。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单套件清单揭示（例如查询套件 S1）：
<query_reveal>S1</query_reveal>

- 多套件联合计数（例如查询 S1, S2, S3 的联合零部件数量）：
<query_union_count>S1,S2,S3</query_union_count>

- 两组采购方案比较（例如比较组 [S1,S2] 与组 [S3,S4]）：
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- 采购可行性边界（例如询问是否存在不超过 3 个套件的完整物料方案）：
<query_feasible>3</query_feasible>

- 局部增量装配价值（例如在 [S1,S2] 基础上增购 S3 新增多少零部件）：
<query_incremental>S1,S2|S3</query_incremental>

提交最终答案时，必须指明最小套件数量和套件列表（用逗号隔开），格式如下：
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Industrial Modular Assembly Minimization" reasoning game. Here are the rules:

On a high-end manufacturing assembly line, there exists a hidden set U of essential components (denoted as E1, E2, ...) required for production, along with several standardized integrated kits S1, S2, ... provided by suppliers. Each integrated kit contains some components in U. Supply chain agreements guarantee that at least one procurement combination of these kits can provide all essential components.

Your goal is: find the minimum kit procurement cover, i.e., purchase the smallest number of standardized kits to completely satisfy all component requirements (to reduce logistics and inventory costs), and submit both the minimum size and the specific kit indices.

You can obtain supply chain information through five types of queries (one question per turn):

1. Reveal Single Kit Inventory: Ask which components a specific kit contains.
2. Joint Kit Components Count: Ask how many unique components are provided by the union of several kits.
3. Compare Two Procurement Plans: Compare two groups of kits to determine which provides more unique components.
4. Procurement Feasibility Bound: Ask whether there exists a complete bill of materials using at most k kits.
5. Incremental Assembly Value: Ask how many new components would be provided by adding a specific kit to an existing procurement plan.

When you have enough information, submit your final answer. The answer must include the minimum cover size and specific kit indices.

Each query must contain only one tag. Use the following XML format:

- Reveal Single Kit Inventory (e.g., query kit S1):
<query_reveal>S1</query_reveal>

- Joint Kit Components Count (e.g., query union size of S1, S2, S3):
<query_union_count>S1,S2,S3</query_union_count>

- Compare Two Procurement Plans (e.g., compare group [S1,S2] with group [S3,S4]):
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- Procurement Feasibility Bound (e.g., ask if a complete scheme with at most 3 kits exists):
<query_feasible>3</query_feasible>

- Incremental Assembly Value (e.g., new components when adding S3 to [S1,S2]):
<query_incremental>S1,S2|S3</query_incremental>

When submitting the final answer, specify the minimum cover size and kit list (comma-separated), using this format:
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"完美证据链最小化"推理游戏，规则如下：

在一宗错综复杂的诉讼案件中，存在一个隐藏的争议焦点集合 U，包含若干个法庭必须查明的核心法律事实（记为 E1, E2, ...），以及若干名可传唤的专家证人或调取的卷宗包 S1, S2, ...。每位证人或每份卷宗只能提供能够证实 U 中部分争议焦点的证据。诉讼程序保证，只要合理组织证人和卷宗的并集，至少存在一种举证方案能够构建出覆盖所有争议焦点的完整证据链。

你的目标是：找出最小举证覆盖方案，即传唤最少数量的证人/卷宗来完全查明所有争议焦点（以节约司法资源和庭审时间），并提交该最小数量及具体的证人/卷宗编号。

你可以通过以下五种查询方式获取证据摸底信息（每次只能提一个问题）：

1. 单一证据效力揭示：询问某位证人/卷宗具体能证实哪些争议焦点。
2. 联合质证覆盖计数：询问若干名证人/卷宗的组合共能查明多少个争议焦点。
3. 两组举证方案比较：比较两组举证策略，哪一组能覆盖更多的争议焦点。
4. 庭审可行性边界：询问是否存在不超过 k 名证人/卷宗的完整证据链构建方案。
5. 局部增量举证价值：询问在已有若干证据的基础上，追加某位证人/卷宗能额外查明多少个新的争议焦点。

当你收集足够信息后，请提交最终答案。答案必须包含最小证据数量和具体证人/卷宗编号。

每次查询只能包含一个标签，使用以下 XML 格式：

- 单一证据效力揭示（例如查询证据 S1）：
<query_reveal>S1</query_reveal>

- 联合质证覆盖计数（例如查询 S1, S2, S3 的联合证据效力数量）：
<query_union_count>S1,S2,S3</query_union_count>

- 两组举证方案比较（例如比较组 [S1,S2] 与组 [S3,S4]）：
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- 庭审可行性边界（例如询问是否存在不超过 3 份证据的完整证据链方案）：
<query_feasible>3</query_feasible>

- 局部增量举证价值（例如在 [S1,S2] 基础上追加 S3 新增查明多少争议焦点）：
<query_incremental>S1,S2|S3</query_incremental>

提交最终答案时，必须指明最小证据数量和证据列表（用逗号隔开），格式如下：
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Perfect Chain of Evidence Minimization" reasoning game. Here are the rules:

In a complex litigation case, there exists a hidden set U of disputed issues (denoted as E1, E2, ...) that the court must clarify, along with several summonable expert witnesses or obtainable case files S1, S2, .... Each witness or file can only provide evidence corroborating some issues in U. Legal procedures guarantee that at least one evidentiary strategy can build a complete chain of evidence covering all disputed issues.

Your goal is: find the minimum evidentiary cover, i.e., summon the smallest number of witnesses/files to completely clarify all disputed issues (to save judicial resources and trial time), and submit both the minimum size and the specific witness/file indices.

You can obtain evidentiary information through five types of queries (one question per turn):

1. Reveal Single Evidence Efficacy: Ask which disputed issues a specific witness/file corroborates.
2. Joint Cross-Examination Count: Ask how many disputed issues are clarified by the union of several witnesses/files.
3. Compare Two Evidentiary Strategies: Compare two groups of witnesses/files to determine which covers more disputed issues.
4. Trial Feasibility Bound: Ask whether there exists a complete evidentiary chain scheme using at most k witnesses/files.
5. Incremental Evidentiary Value: Ask how many new disputed issues would be clarified by adding a specific witness/file to an existing evidentiary portfolio.

When you have enough information, submit your final answer. The answer must include the minimum cover size and specific witness/file indices.

Each query must contain only one tag. Use the following XML format:

- Reveal Single Evidence Efficacy (e.g., query evidence S1):
<query_reveal>S1</query_reveal>

- Joint Cross-Examination Count (e.g., query union size of S1, S2, S3):
<query_union_count>S1,S2,S3</query_union_count>

- Compare Two Evidentiary Strategies (e.g., compare group [S1,S2] with group [S3,S4]):
<query_compare_groups>S1,S2|S3,S4</query_compare_groups>

- Trial Feasibility Bound (e.g., ask if a complete scheme with at most 3 evidence sources exists):
<query_feasible>3</query_feasible>

- Incremental Evidentiary Value (e.g., new issues clarified when adding S3 to [S1,S2]):
<query_incremental>S1,S2|S3</query_incremental>

When submitting the final answer, specify the minimum cover size and evidence list (comma-separated), using this format:
<answer>size=3, subsets=S1,S3,S5</answer>
"""

    tags = ["answer", "query_reveal", "query_union_count", "query_compare_groups", 
            "query_feasible", "query_incremental"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n_elements": 5,
                "subsets": {
                    "S1": [1, 2, 3],
                    "S2": [3, 4, 5],
                    "S3": [1, 2],
                    "S4": [4, 5],
                },
                "optimal_size": 2,
                "optimal_solution": ["S1", "S2"],
            },
            2: {
                "n_elements": 8,
                "subsets": {
                    "S1": [1, 2, 3],
                    "S2": [4, 5, 6],
                    "S3": [7, 8],
                    "S4": [1, 4, 7],
                    "S5": [2, 5, 8],
                },
                "optimal_size": 3,
                "optimal_solution": ["S1", "S2", "S3"],
            },
            3: {
                "n_elements": 10,
                "subsets": {
                    "S1": [1, 2, 3, 4],
                    "S2": [5, 6, 7],
                    "S3": [8, 9, 10],
                    "S4": [1, 5, 8],
                    "S5": [2, 6, 9],
                    "S6": [3, 7, 10],
                    "S7": [4],
                },
                "optimal_size": 3,
                "optimal_solution": ["S1", "S2", "S3"],
            },
            4: {
                "n_elements": 12,
                "subsets": {
                    "S1": [1, 2, 3],
                    "S2": [4, 5, 6],
                    "S3": [7, 8, 9],
                    "S4": [10, 11, 12],
                    "S5": [1, 4, 7, 10],
                    "S6": [2, 5, 8, 11],
                    "S7": [3, 6, 9, 12],
                    "S8": [1, 6, 8],
                },
                "optimal_size": 4,
                "optimal_solution": ["S1", "S2", "S3", "S4"],
            },
            5: {
                "n_elements": 15,
                "subsets": {
                    "S1": [1, 2, 3, 4],
                    "S2": [5, 6, 7, 8],
                    "S3": [9, 10, 11],
                    "S4": [12, 13, 14, 15],
                    "S5": [1, 5, 9, 12],
                    "S6": [2, 6, 10, 13],
                    "S7": [3, 7, 11, 14],
                    "S8": [4, 8, 15],
                    "S9": [1, 6, 11],
                    "S10": [2, 7, 12],
                },
                "optimal_size": 4,
                "optimal_solution": ["S1", "S2", "S3", "S4"],
            },
        },
        "en": {
            1: {
                "n_elements": 5,
                "subsets": {
                    "S1": [1, 2, 3],
                    "S2": [3, 4, 5],
                    "S3": [1, 2],
                    "S4": [4, 5],
                },
                "optimal_size": 2,
                "optimal_solution": ["S1", "S2"],
            },
            2: {
                "n_elements": 8,
                "subsets": {
                    "S1": [1, 2, 3],
                    "S2": [4, 5, 6],
                    "S3": [7, 8],
                    "S4": [1, 4, 7],
                    "S5": [2, 5, 8],
                },
                "optimal_size": 3,
                "optimal_solution": ["S1", "S2", "S3"],
            },
            3: {
                "n_elements": 10,
                "subsets": {
                    "S1": [1, 2, 3, 4],
                    "S2": [5, 6, 7],
                    "S3": [8, 9, 10],
                    "S4": [1, 5, 8],
                    "S5": [2, 6, 9],
                    "S6": [3, 7, 10],
                    "S7": [4],
                },
                "optimal_size": 3,
                "optimal_solution": ["S1", "S2", "S3"],
            },
            4: {
                "n_elements": 12,
                "subsets": {
                    "S1": [1, 2, 3],
                    "S2": [4, 5, 6],
                    "S3": [7, 8, 9],
                    "S4": [10, 11, 12],
                    "S5": [1, 4, 7, 10],
                    "S6": [2, 5, 8, 11],
                    "S7": [3, 6, 9, 12],
                    "S8": [1, 6, 8],
                },
                "optimal_size": 4,
                "optimal_solution": ["S1", "S2", "S3", "S4"],
            },
            5: {
                "n_elements": 15,
                "subsets": {
                    "S1": [1, 2, 3, 4],
                    "S2": [5, 6, 7, 8],
                    "S3": [9, 10, 11],
                    "S4": [12, 13, 14, 15],
                    "S5": [1, 5, 9, 12],
                    "S6": [2, 6, 10, 13],
                    "S7": [3, 7, 11, 14],
                    "S8": [4, 8, 15],
                    "S9": [1, 6, 11],
                    "S10": [2, 7, 12],
                },
                "optimal_size": 4,
                "optimal_solution": ["S1", "S2", "S3", "S4"],
            },
        },
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
        
        self.n_elements = cfg["n_elements"]
        self.subsets = cfg["subsets"]
        self.optimal_size = cfg["optimal_size"]
        self.optimal_solution = set(cfg["optimal_solution"])
        
        self._game_info = {}

    def _parse_subset_list(self, text):
        return [s.strip() for s in text.split(",") if s.strip()]

    def _compute_union(self, subset_names):
        union = set()
        for name in subset_names:
            if name in self.subsets:
                union.update(self.subsets[name])
        return union

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            
            size_part = parts[0]
            if "=" in size_part:
                k, v = size_part.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            subsets_start = raw_ans.find("subsets=")
            if subsets_start != -1:
                subsets_value = raw_ans[subsets_start + 8:].strip()
                ans_dict["subsets"] = subsets_value
            
            if "size" not in ans_dict or "subsets" not in ans_dict:
                return False
            
            submitted_size = int(ans_dict["size"])
            
            submitted_subsets = self._parse_subset_list(ans_dict["subsets"])
            
            for s in submitted_subsets:
                if s not in self.subsets:
                    return False
            
            union = self._compute_union(submitted_subsets)
            
            all_elements = set(range(1, self.n_elements + 1))
            if union != all_elements:
                return False
            
            if len(submitted_subsets) != self.optimal_size:
                return False
            
            if submitted_size != len(submitted_subsets):
                return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "query_reveal" in parsed_info:
            subset_name = parsed_info["query_reveal"].strip()
            if subset_name not in self.subsets:
                return "错误：子集不存在。" if lang == "zh" else "Error: Subset does not exist."
            
            elements = self.subsets[subset_name]
            if not elements:
                return "空" if lang == "zh" else "Empty"
            
            elem_str = ", ".join([f"E{e}" for e in sorted(elements)])
            return elem_str
        
        elif "query_union_count" in parsed_info:
            subset_names = self._parse_subset_list(parsed_info["query_union_count"])
            
            for name in subset_names:
                if name not in self.subsets:
                    return "错误：包含不存在的子集。" if lang == "zh" else "Error: Contains non-existent subset."
            
            union = self._compute_union(subset_names)
            return str(len(union))
        
        elif "query_compare_groups" in parsed_info:
            try:
                groups = parsed_info["query_compare_groups"].split("|")
                if len(groups) != 2:
                    raise ValueError
                
                group_a = self._parse_subset_list(groups[0])
                group_b = self._parse_subset_list(groups[1])
                
                for name in group_a + group_b:
                    if name not in self.subsets:
                        raise ValueError
                
                union_a = self._compute_union(group_a)
                union_b = self._compute_union(group_b)
                
                if len(union_a) > len(union_b):
                    return "组A更多" if lang == "zh" else "Group A covers more"
                elif len(union_a) < len(union_b):
                    return "组B更多" if lang == "zh" else "Group B covers more"
                else:
                    return "相等" if lang == "zh" else "Equal"
                    
            except:
                return "错误：格式无效或子集不存在。" if lang == "zh" else "Error: Invalid format or subset does not exist."
        
        elif "query_feasible" in parsed_info:
            try:
                k = int(parsed_info["query_feasible"].strip())
                if k >= self.optimal_size:
                    return "是" if lang == "zh" else "Yes"
                else:
                    return "否" if lang == "zh" else "No"
            except:
                return "错误：无效的数字。" if lang == "zh" else "Error: Invalid number."
        
        elif "query_incremental" in parsed_info:
            try:
                parts = parsed_info["query_incremental"].split("|")
                if len(parts) != 2:
                    raise ValueError
                
                base_subsets = self._parse_subset_list(parts[0]) if parts[0].strip() else []
                new_subset = parts[1].strip()
                
                for name in base_subsets:
                    if name not in self.subsets:
                        raise ValueError
                if new_subset not in self.subsets:
                    raise ValueError
                
                base_union = self._compute_union(base_subsets)
                
                new_elements = set(self.subsets[new_subset]) - base_union
                
                return str(len(new_elements))
                
            except:
                return "错误：格式无效或子集不存在。" if lang == "zh" else "Error: Invalid format or subset does not exist."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.strip().isdigit():
            val = int(correct.strip())
            if val == 0:
                return str(val + 1)
            return str(val + 1)

        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
            elif correct == "组A更多":
                return "组B更多"
            elif correct == "组B更多":
                return "组A更多"
            elif correct == "相等":
                return "组A更多"

        if self.config.language == "en":
            low_correct = correct.lower()
            if low_correct == "yes":
                return "No" if correct[0].isupper() else "no"
            elif low_correct == "no":
                return "Yes" if correct[0].isupper() else "yes"
            elif low_correct == "group a covers more":
                return "Group B covers more"
            elif low_correct == "group b covers more":
                return "Group A covers more"
            elif low_correct == "equal":
                return "Group A covers more"

        if correct.startswith("E") and "," in correct:
            elements = [e.strip() for e in correct.split(",")]
            if len(elements) > 1:
                return ", ".join(elements[:-1])
            else:
                return correct + ", E999"

        return correct + "_WRONG"

    def get_all_possible_queries(self):
        queries = []
        lang = self.config.language
        subset_names = sorted(list(self.subsets.keys()))
        n_subsets = len(subset_names)

        max_combo_size = min(n_subsets, 3)

        for name in subset_names:
            elements = self.subsets[name]
            if not elements:
                ans = "空" if lang == "zh" else "Empty"
            else:
                ans = ", ".join([f"E{e}" for e in sorted(elements)])
            queries.append({
                "query": f"<query_reveal>{name}</query_reveal>",
                "answer": ans
            })

        for r in range(2, max_combo_size + 1):
            for combo in itertools.combinations(subset_names, r):
                union = self._compute_union(combo)
                query_str = ",".join(combo)
                queries.append({
                    "query": f"<query_union_count>{query_str}</query_union_count>",
                    "answer": str(len(union))
                })

        for k in range(1, n_subsets + 1):
            if k >= self.optimal_size:
                ans = "是" if lang == "zh" else "Yes"
            else:
                ans = "否" if lang == "zh" else "No"
            queries.append({
                "query": f"<query_feasible>{k}</query_feasible>",
                "answer": ans
            })

        for r in range(0, min(n_subsets, 3)):
            for base_combo in itertools.combinations(subset_names, r):
                base_union = self._compute_union(base_combo)
                base_str = ",".join(base_combo)

                remaining_subsets = [s for s in subset_names if s not in base_combo]

                for new_subset in remaining_subsets:
                    new_elements = set(self.subsets[new_subset]) - base_union
                    queries.append({
                        "query": f"<query_incremental>{base_str}|{new_subset}</query_incremental>",
                        "answer": str(len(new_elements))
                    })

        for s1 in subset_names:
            for s2 in subset_names:
                if s1 == s2:
                    continue

                union_a = self._compute_union([s1])
                union_b = self._compute_union([s2])

                if len(union_a) > len(union_b):
                    ans = "组A更多" if lang == "zh" else "Group A covers more"
                elif len(union_a) < len(union_b):
                    ans = "组B更多" if lang == "zh" else "Group B covers more"
                else:
                    ans = "相等" if lang == "zh" else "Equal"

                queries.append({
                    "query": f"<query_compare_groups>{s1}|{s2}</query_compare_groups>",
                    "answer": ans
                })

        return queries