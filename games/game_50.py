from .base import Game
import random
import itertools

class MinimalSetCoverGame(Game):

    game_rule_zh = """\
我们来玩一个"最小覆盖推理"游戏，规则如下：

游戏设定了一个未知的全集 U 和若干子集 S1, S2, ..., S{m}。全集 U 包含 {n} 个元素，每个子集 Si 是 U 的子集，且所有子集的并集覆盖全集 U。

你的目标是找到最少数量的子集，使得它们的并集恰好等于全集 U。我们称这个最小数量为 k*。你需要确定 k* 的值，并给出一个由 k* 个子集组成的索引集合。

你可以使用以下四种查询（每次只能提交一种查询）：

1. 计数查询 (COUNT)：查询指定若干子集的并集包含多少个元素。
   格式示例：<query_count>1,3,5</query_count>
   返回：这些子集并集的元素个数。

2. 边际查询 (MARG)：查询在已有若干子集的并集基础上，再加入一个新子集会增加多少个新元素。
   格式示例：<query_marg>1,2+3</query_marg>（表示在子集1、2的并集基础上加入子集3）
   返回：新增的元素个数。

3. 比较查询 (COMP)：比较两组子集的并集大小。
   格式示例：<query_comp>1,2 vs 3,4</query_comp>
   返回：A>B（左边大）、A<B（左边小）或 A=B（相等）。

4. 进度查询 (PROG)：查询已使用的查询次数和剩余次数。
   格式示例：<query_prog></query_prog>
   返回：已用次数和剩余次数。

你有总共 {quota} 次查询配额。超出配额将导致游戏失败。

当你确定答案后，请提交最终答案。格式如下：

<answer>k=3; SET=1,4,5</answer>

其中 k 是你认为的最小覆盖数量，SET 是具体的子集索引集合（用逗号分隔）。

提交后系统会进行校验：
- 首先检查你提交的子集是否覆盖全集
- 如果覆盖全集，再检查数量是否最小

请谨慎提交答案，答案错误将直接导致游戏失败。祝你好运！
"""

    game_rule_en = """\
Let's play a "Minimal Set Cover Inference" game. Here are the rules:

The game involves an unknown universal set U and several subsets S1, S2, ..., S{m}. The universal set U contains {n} elements, each subset Si is a subset of U, and the union of all subsets covers U.

Your goal is to find the minimum number of subsets whose union equals the universal set U. We call this minimum number k*. You need to determine the value of k* and provide an index set consisting of k* subsets.

You can use the following four types of queries (only one query per submission):

1. Count Query (COUNT): Query how many elements are in the union of specified subsets.
   Format example: <query_count>1,3,5</query_count>
   Returns: The number of elements in the union of these subsets.

2. Marginal Query (MARG): Query how many new elements would be added when adding a new subset to the union of existing subsets.
   Format example: <query_marg>1,2+3</query_marg> (means adding subset 3 to the union of subsets 1 and 2)
   Returns: The number of newly added elements.

3. Comparison Query (COMP): Compare the sizes of unions of two groups of subsets.
   Format example: <query_comp>1,2 vs 3,4</query_comp>
   Returns: A>B (left is larger), A<B (left is smaller), or A=B (equal).

4. Progress Query (PROG): Query the number of queries used and remaining.
   Format example: <query_prog></query_prog>
   Returns: Used and remaining query counts.

You have a total of {quota} query quota. Exceeding the quota will result in game failure.

When you determine the answer, submit your final answer in this format:

<answer>k=3; SET=1,4,5</answer>

Where k is your answer for the minimum cover size, and SET is the specific subset index set (comma-separated).

After submission, the system will verify:
- First check if your submitted subsets cover the universal set
- If they cover, then check if the number is minimal

Please submit your answer carefully, as an incorrect answer will directly lead to game failure. Good luck!
"""

    contextualized_rule_zh_1 = """\
我们来玩一个"交通监控盲区最小化部署"游戏，规则如下：

作为城市交通规划师，你需要监控该市的一个核心交通网（全集 U）。该交通网包含 {n} 个关键路口，现有 {m} 种不同型号的监控摄像头部署方案（方案 S1, S2, ..., S{m}）。每种方案能覆盖特定的几个路口，且所有方案综合起来能覆盖全部 {n} 个路口。

你的目标是找到最少数量的部署方案组合，使得它们的监控范围恰好无死角覆盖所有的核心路口。我们称这个最小数量为 k*。你需要确定 k* 的值，并给出一个由 k* 个方案组成的索引集合。

你可以使用以下四种系统查询（每次只能提交一种查询）：

1. 计数查询 (COUNT)：查询指定若干方案的联合覆盖范围包含多少个路口。
   格式示例：<query_count>1,3,5</query_count>
   返回：这些方案联合覆盖的路口总数。

2. 边际查询 (MARG)：查询在已有若干方案的基础上，再增加一个新方案会多覆盖多少个未知路口。
   格式示例：<query_marg>1,2+3</query_marg>（表示在方案1、2的基础上加入方案3）
   返回：新增覆盖的路口个数。

3. 比较查询 (COMP)：比较两套不同方案组合的覆盖路口数量。
   格式示例：<query_comp>1,2 vs 3,4</query_comp>
   返回：A>B（左边覆盖多）、A<B（左边覆盖少）或 A=B（相等）。

4. 进度查询 (PROG)：查询已使用的系统评估次数和剩余次数。
   格式示例：<query_prog></query_prog>
   返回：已用次数和剩余次数。

你有总共 {quota} 次评估配额。超出配额将导致规划任务失败。

当你确定最优部署方案后，请提交最终答案。格式如下：

<answer>k=3; SET=1,4,5</answer>

其中 k 是你认为的最少方案数量，SET 是具体的方案索引集合（用逗号分隔）。

提交后系统会进行校验：
- 首先检查你提交的方案组合是否无死角覆盖了所有路口
- 如果完全覆盖，再检查使用的方案数量是否做到了最小化

请谨慎提交答案，答案错误将直接导致游戏失败。祝你好运！
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Traffic Surveillance Minimal Deployment" game. Here are the rules:

As a city traffic planner, you need to monitor a core traffic network (the universal set U). This network contains {n} key intersections, and there are {m} different surveillance camera deployment plans available (plans S1, S2, ..., S{m}). Each plan covers specific intersections, and collectively, all plans cover all {n} intersections.

Your goal is to find the minimum number of deployment plans whose combined coverage monitors the entire network without blind spots. We call this minimum number k*. You need to determine the value of k* and provide an index set consisting of k* plans.

You can use the following four types of system queries (only one query per submission):

1. Count Query (COUNT): Query how many intersections are covered by the combination of specified plans.
   Format example: <query_count>1,3,5</query_count>
   Returns: The total number of intersections covered by these plans.

2. Marginal Query (MARG): Query how many new intersections would be covered by adding a new plan to the existing combination of plans.
   Format example: <query_marg>1,2+3</query_marg> (means adding plan 3 to plans 1 and 2)
   Returns: The number of newly covered intersections.

3. Comparison Query (COMP): Compare the coverage sizes of two groups of plans.
   Format example: <query_comp>1,2 vs 3,4</query_comp>
   Returns: A>B (left covers more), A<B (left covers less), or A=B (equal coverage).

4. Progress Query (PROG): Query the number of evaluation queries used and remaining.
   Format example: <query_prog></query_prog>
   Returns: Used and remaining query counts.

You have a total of {quota} evaluation quota. Exceeding the quota will result in planning failure.

When you determine the optimal deployment, submit your final answer in this format:

<answer>k=3; SET=1,4,5</answer>

Where k is your answer for the minimum number of plans, and SET is the specific plan index set (comma-separated).

After submission, the system will verify:
- First check if your submitted combination covers all intersections without blind spots
- If fully covered, then check if the number of plans is minimal

Please submit your answer carefully, as an incorrect answer will directly lead to game failure. Good luck!
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"医疗检测套餐最优化"游戏，规则如下：

作为首席诊断医师，你面对一种罕见综合征，其全部确诊指征构成了全集 U。该疾病共有 {n} 个关键临床症状，医院提供了 {m} 种生化检测套餐（套餐 S1, S2, ..., S{m}）。每种检测套餐能确诊特定的几个症状，且所有套餐综合起来能够确诊全部 {n} 个症状。

你的目标是为患者开出最少数量的检测套餐，使得它们能够覆盖并确诊所有的关键症状。我们称这个最少套餐数量为 k*。你需要确定 k* 的值，并给出一个由 k* 个套餐组成的索引集合。

你可以使用以下四种系统查询（每次只能提交一种查询）：

1. 计数查询 (COUNT)：查询指定若干套餐的联合诊断能覆盖多少个症状。
   格式示例：<query_count>1,3,5</query_count>
   返回：这些套餐联合覆盖的症状总数。

2. 边际查询 (MARG)：查询在已有若干套餐的基础上，再增加一个新检测套餐会多覆盖多少个未知症状。
   格式示例：<query_marg>1,2+3</query_marg>（表示在套餐1、2的基础上加入套餐3）
   返回：新增覆盖的症状个数。

3. 比较查询 (COMP)：比较两组检测套餐的症状覆盖数量。
   格式示例：<query_comp>1,2 vs 3,4</query_comp>
   返回：A>B（左边覆盖多）、A<B（左边覆盖少）或 A=B（相等）。

4. 进度查询 (PROG)：查询已使用的诊断评估次数和剩余次数。
   格式示例：<query_prog></query_prog>
   返回：已用次数和剩余次数。

你有总共 {quota} 次评估配额。超出配额将导致延误诊断，游戏失败。

当你确定最优诊断方案后，请提交最终答案。格式如下：

<answer>k=3; SET=1,4,5</answer>

其中 k 是你认为的最少套餐数量，SET 是具体的检测套餐索引集合（用逗号分隔）。

提交后系统会进行校验：
- 首先检查你提交的检测套餐是否涵盖了全部关键症状
- 如果完全涵盖，再检查开具的套餐数量是否做到了最小化

请谨慎提交答案，答案错误将直接导致游戏失败。祝你好运！
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play an "Optimal Medical Testing Panel" game. Here are the rules:

As the chief diagnostic physician, you are dealing with a rare syndrome whose definitive diagnostic indicators make up the universal set U. The disease has {n} key clinical symptoms, and the hospital offers {m} biochemical testing panels (panels S1, S2, ..., S{m}). Each testing panel can confirm specific symptoms, and altogether they can cover all {n} symptoms.

Your goal is to prescribe the minimum number of testing panels that collectively cover and confirm all key symptoms. We call this minimum number k*. You need to determine the value of k* and provide an index set consisting of k* panels.

You can use the following four types of system queries (only one query per submission):

1. Count Query (COUNT): Query how many symptoms are covered by the combined diagnosis of specified testing panels.
   Format example: <query_count>1,3,5</query_count>
   Returns: The total number of symptoms covered by these panels.

2. Marginal Query (MARG): Query how many new symptoms would be covered by adding a new testing panel to the existing combination of panels.
   Format example: <query_marg>1,2+3</query_marg> (means adding panel 3 to panels 1 and 2)
   Returns: The number of newly covered symptoms.

3. Comparison Query (COMP): Compare the symptom coverage sizes of two groups of testing panels.
   Format example: <query_comp>1,2 vs 3,4</query_comp>
   Returns: A>B (left covers more), A<B (left covers less), or A=B (equal coverage).

4. Progress Query (PROG): Query the number of diagnostic evaluation queries used and remaining.
   Format example: <query_prog></query_prog>
   Returns: Used and remaining query counts.

You have a total of {quota} evaluation quota. Exceeding the quota will delay diagnosis and result in failure.

When you determine the optimal diagnostic plan, submit your final answer in this format:

<answer>k=3; SET=1,4,5</answer>

Where k is your answer for the minimum number of panels, and SET is the specific testing panel index set (comma-separated).

After submission, the system will verify:
- First check if your submitted panels cover all key symptoms
- If fully covered, then check if the number of prescribed panels is minimal

Please submit your answer carefully, as an incorrect answer will directly lead to game failure. Good luck!
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"精准复习资料筛选"游戏，规则如下：

作为一名冲刺备考的学生，你需要复习某门课程的核心大纲（全集 U）。该大纲包含 {n} 个必考知识点，目前市面上有 {m} 种教辅题库（题库 S1, S2, ..., S{m}）。每种教辅题库涵盖了特定的几个知识点，且所有题库综合起来能覆盖全部 {n} 个知识点。

你的目标是购买最少数量的教辅题库，使得它们能够覆盖所有的必考知识点，做到复习无死角。我们称这个最少题库数量为 k*。你需要确定 k* 的值，并给出一个由 k* 个题库组成的索引集合。

你可以使用以下四种系统查询（每次只能提交一种查询）：

1. 计数查询 (COUNT)：查询指定若干题库的联合内容能覆盖多少个大纲知识点。
   格式示例：<query_count>1,3,5</query_count>
   返回：这些题库联合覆盖的知识点总数。

2. 边际查询 (MARG)：查询在已有若干题库的基础上，再购买一本新题库会多覆盖多少个未复习的知识点。
   格式示例：<query_marg>1,2+3</query_marg>（表示在题库1、2的基础上加入题库3）
   返回：新增覆盖的知识点个数。

3. 比较查询 (COMP)：比较两组教辅题库的知识点覆盖数量。
   格式示例：<query_comp>1,2 vs 3,4</query_comp>
   返回：A>B（左边覆盖多）、A<B（左边覆盖少）或 A=B（相等）。

4. 进度查询 (PROG)：查询已使用的试读查询次数和剩余次数。
   格式示例：<query_prog></query_prog>
   返回：已用次数和剩余次数。

你有总共 {quota} 次试读查询配额。超出配额将导致备考计划失败。

当你确定最优购买方案后，请提交最终答案。格式如下：

<answer>k=3; SET=1,4,5</answer>

其中 k 是你认为的最少题库数量，SET 是具体的题库索引集合（用逗号分隔）。

提交后系统会进行校验：
- 首先检查你提交的题库组合是否涵盖了大纲的所有知识点
- 如果完全涵盖，再检查所选的题库数量是否做到了最少

请谨慎提交答案，答案错误将直接导致游戏失败。祝你好运！
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Precise Study Material Screening" game. Here are the rules:

As a student preparing for final exams, you need to review the core syllabus of a course (the universal set U). The syllabus contains {n} essential knowledge points, and there are currently {m} test bank workbooks available on the market (workbooks S1, S2, ..., S{m}). Each workbook covers specific knowledge points, and collectively, all workbooks cover all {n} points.

Your goal is to purchase the minimum number of workbooks so that they cover all the essential knowledge points without any blind spots. We call this minimum number k*. You need to determine the value of k* and provide an index set consisting of k* workbooks.

You can use the following four types of system queries (only one query per submission):

1. Count Query (COUNT): Query how many syllabus points are covered by the combined content of specified workbooks.
   Format example: <query_count>1,3,5</query_count>
   Returns: The total number of knowledge points covered by these workbooks.

2. Marginal Query (MARG): Query how many unreviewed knowledge points would be newly covered by purchasing an additional workbook to the existing combination.
   Format example: <query_marg>1,2+3</query_marg> (means adding workbook 3 to workbooks 1 and 2)
   Returns: The number of newly covered knowledge points.

3. Comparison Query (COMP): Compare the knowledge point coverage sizes of two groups of workbooks.
   Format example: <query_comp>1,2 vs 3,4</query_comp>
   Returns: A>B (left covers more), A<B (left covers less), or A=B (equal coverage).

4. Progress Query (PROG): Query the number of trial reading queries used and remaining.
   Format example: <query_prog></query_prog>
   Returns: Used and remaining query counts.

You have a total of {quota} trial reading quota. Exceeding the quota will result in study plan failure.

When you determine the optimal purchase plan, submit your final answer in this format:

<answer>k=3; SET=1,4,5</answer>

Where k is your answer for the minimum number of workbooks, and SET is the specific workbook index set (comma-separated).

After submission, the system will verify:
- First check if your submitted combination of workbooks covers all knowledge points in the syllabus
- If fully covered, then check if the number of selected workbooks is minimal

Please submit your answer carefully, as an incorrect answer will directly lead to game failure. Good luck!
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"工业传感器网络极简覆盖"游戏，规则如下：

作为大型制造厂的可靠性工程师，你需要监控一套精密设备的所有潜在故障点（全集 U）。该设备共有 {n} 个核心故障点，系统供应商提供了 {m} 种不同拓扑的传感器网络（网络 S1, S2, ..., S{m}）。每种传感器网络能监测到特定的几个故障点，且所有网络组合起来能监测到全部 {n} 个点。

你的目标是部署最少数量的传感器网络，使得它们的监控范围恰好覆盖所有的潜在故障点。我们称这个最小数量为 k*。你需要确定 k* 的值，并给出一个由 k* 个传感器网络组成的索引集合。

你可以使用以下四种系统查询（每次只能提交一种查询）：

1. 计数查询 (COUNT)：查询指定若干传感器网络的联合监测能覆盖多少个故障点。
   格式示例：<query_count>1,3,5</query_count>
   返回：这些网络联合覆盖的故障点总数。

2. 边际查询 (MARG)：查询在已有若干网络的基础上，再接入一个新传感器网络会多监测到多少个盲区故障点。
   格式示例：<query_marg>1,2+3</query_marg>（表示在网络1、2的基础上加入网络3）
   返回：新增监测到的故障点个数。

3. 比较查询 (COMP)：比较两组传感器网络的故障点监控数量。
   格式示例：<query_comp>1,2 vs 3,4</query_comp>
   返回：A>B（左边监测多）、A<B（左边监测少）或 A=B（相等）。

4. 进度查询 (PROG)：查询已使用的测试查询次数和剩余次数。
   格式示例：<query_prog></query_prog>
   返回：已用次数和剩余次数。

你有总共 {quota} 次测试查询配额。超出配额将导致设备维保规划失败。

当你确定最优部署方案后，请提交最终答案。格式如下：

<answer>k=3; SET=1,4,5</answer>

其中 k 是你认为的最少网络数量，SET 是具体的传感器网络索引集合（用逗号分隔）。

提交后系统会进行校验：
- 首先检查你提交的网络组合是否无死角监测了所有故障点
- 如果完全覆盖，再检查使用的传感器网络数量是否做到了最少

请谨慎提交答案，答案错误将直接导致游戏失败。祝你好运！
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's play an "Industrial Sensor Network Minimal Coverage" game. Here are the rules:

As a reliability engineer in a large manufacturing plant, you need to monitor all potential failure points of a precision equipment (the universal set U). The equipment has {n} core failure points, and the system supplier offers {m} sensor networks with different topologies (networks S1, S2, ..., S{m}). Each sensor network can detect specific failure points, and combined, all networks can monitor all {n} points.

Your goal is to deploy the minimum number of sensor networks whose monitoring scope perfectly covers all potential failure points. We call this minimum number k*. You need to determine the value of k* and provide an index set consisting of k* sensor networks.

You can use the following four types of system queries (only one query per submission):

1. Count Query (COUNT): Query how many failure points are covered by the combined monitoring of specified sensor networks.
   Format example: <query_count>1,3,5</query_count>
   Returns: The total number of failure points covered by these networks.

2. Marginal Query (MARG): Query how many blind-spot failure points would be newly detected by adding a new sensor network to the existing ones.
   Format example: <query_marg>1,2+3</query_marg> (means adding network 3 to networks 1 and 2)
   Returns: The number of newly detected failure points.

3. Comparison Query (COMP): Compare the monitored failure point coverage of two groups of sensor networks.
   Format example: <query_comp>1,2 vs 3,4</query_comp>
   Returns: A>B (left monitors more), A<B (left monitors less), or A=B (equal coverage).

4. Progress Query (PROG): Query the number of testing queries used and remaining.
   Format example: <query_prog></query_prog>
   Returns: Used and remaining query counts.

You have a total of {quota} testing query quota. Exceeding the quota will result in equipment maintenance planning failure.

When you determine the optimal deployment plan, submit your final answer in this format:

<answer>k=3; SET=1,4,5</answer>

Where k is your answer for the minimum number of networks, and SET is the specific sensor network index set (comma-separated).

After submission, the system will verify:
- First check if your submitted combination of networks monitors all failure points without blind spots
- If fully covered, then check if the number of deployed sensor networks is minimal

Please submit your answer carefully, as an incorrect answer will directly lead to game failure. Good luck!
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"完美证据链最简构建"游戏，规则如下：

作为首席控方律师，你需要为一宗复杂案件构建完整的证据链（全集 U）。该案件包含 {n} 个必须被证明的关键事实，你手里有 {m} 位证人/专家（证人 S1, S2, ..., S{m}）。每位证人的证词能证实特定的几个事实，且所有证人加起来能够证实全部 {n} 个关键事实。

你的目标是传唤最少数量的证人，使得他们的证词组合起来恰好能证实所有的关键事实，从而形成完美证据链。我们称这个最少证人数量为 k*。你需要确定 k* 的值，并给出一个由 k* 位证人组成的索引集合。

你可以使用以下四种庭前调查查询（每次只能提交一种查询）：

1. 计数查询 (COUNT)：查询指定若干证人的联合证词能证实多少个关键事实。
   格式示例：<query_count>1,3,5</query_count>
   返回：这些证人联合证实的事实总数。

2. 边际查询 (MARG)：查询在已有若干证人的基础上，再传唤一位新证人会多证实多少个缺乏证据的事实。
   格式示例：<query_marg>1,2+3</query_marg>（表示在证人1、2的基础上加入证人3）
   返回：新增证实的事实个数。

3. 比较查询 (COMP)：比较两组证人的事实证实数量。
   格式示例：<query_comp>1,2 vs 3,4</query_comp>
   返回：A>B（左边证实多）、A<B（左边证实少）或 A=B（相等）。

4. 进度查询 (PROG)：查询已使用的调查评估次数和剩余次数。
   格式示例：<query_prog></query_prog>
   返回：已用次数和剩余次数。

你有总共 {quota} 次调查评估配额。超出配额将导致庭审准备失败。

当你确定最优传唤名单后，请提交最终答案。格式如下：

<answer>k=3; SET=1,4,5</answer>

其中 k 是你认为的最少证人数量，SET 是具体的证人索引集合（用逗号分隔）。

提交后系统会进行校验：
- 首先检查你提交的证人组合是否证实了案件的所有关键事实
- 如果完全证实，再检查传唤的证人数量是否做到了最少

请谨慎提交答案，答案错误将直接导致游戏失败。祝你好运！
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Perfect Evidence Chain Minimal Construction" game. Here are the rules:

As the lead prosecuting attorney, you need to construct a complete evidence chain for a complex case (the universal set U). The case involves {n} key facts that must be proven, and you have {m} witnesses/experts available (witnesses S1, S2, ..., S{m}). Each witness's testimony can prove specific facts, and collectively, all witnesses can prove all {n} key facts.

Your goal is to subpoena the minimum number of witnesses whose combined testimonies precisely prove all key facts, forming a perfect evidence chain. We call this minimum number k*. You need to determine the value of k* and provide an index set consisting of k* witnesses.

You can use the following four types of pre-trial investigation queries (only one query per submission):

1. Count Query (COUNT): Query how many key facts are proven by the combined testimony of specified witnesses.
   Format example: <query_count>1,3,5</query_count>
   Returns: The total number of facts proven by these witnesses.

2. Marginal Query (MARG): Query how many unsupported facts would be newly proven by subpoenaing an additional witness to the existing group.
   Format example: <query_marg>1,2+3</query_marg> (means adding witness 3 to witnesses 1 and 2)
   Returns: The number of newly proven facts.

3. Comparison Query (COMP): Compare the number of facts proven by two groups of witnesses.
   Format example: <query_comp>1,2 vs 3,4</query_comp>
   Returns: A>B (left proves more), A<B (left proves less), or A=B (equal coverage).

4. Progress Query (PROG): Query the number of investigation evaluation queries used and remaining.
   Format example: <query_prog></query_prog>
   Returns: Used and remaining query counts.

You have a total of {quota} investigation evaluation quota. Exceeding the quota will result in trial preparation failure.

When you determine the optimal subpoena list, submit your final answer in this format:

<answer>k=3; SET=1,4,5</answer>

Where k is your answer for the minimum number of witnesses, and SET is the specific witness index set (comma-separated).

After submission, the system will verify:
- First check if your submitted combination of witnesses proves all key facts of the case
- If fully proven, then check if the number of subpoenaed witnesses is minimal

Please submit your answer carefully, as an incorrect answer will directly lead to game failure. Good luck!
"""

    tags = ["answer", "query_count", "query_marg", "query_comp", "query_prog"]

    reasoning_type = "归纳推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        1: {
            "n": 6,
            "m": 4,
            "k_star": 2,
            "subsets": [
                {0, 1, 2},
                {3, 4, 5},
                {0, 3},
                {1, 4}
            ]
        },
        2: {
            "n": 8,
            "m": 5,
            "k_star": 2,
            "subsets": [
                {0, 1, 2, 3},
                {4, 5, 6, 7},
                {0, 4},
                {1, 5},
                {2, 6}
            ]
        },
        3: {
            "n": 10,
            "m": 6,
            "k_star": 3,
            "subsets": [
                {0, 1, 2, 3},
                {4, 5, 6},
                {7, 8, 9},
                {0, 4, 7},
                {1, 5, 8},
                {2, 3, 6, 9}
            ]
        },
        4: {
            "n": 12,
            "m": 7,
            "k_star": 3,
            "subsets": [
                {0, 1, 2, 3},
                {4, 5, 6, 7},
                {8, 9, 10, 11},
                {0, 4, 8},
                {1, 5, 9},
                {2, 6},
                {3, 7}
            ]
        },
        5: {
            "n": 15,
            "m": 8,
            "k_star": 4,
            "subsets": [
                {0, 1, 2, 3, 4},
                {5, 6, 7, 8},
                {9, 10, 11},
                {12, 13, 14},
                {0, 5, 9, 12},
                {1, 6, 10, 13},
                {2, 7, 11, 14},
                {3, 8}
            ]
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        self.n = cfg["n"]
        self.m = cfg["m"]
        self.k_star = cfg["k_star"]
        self.subsets = [s.copy() for s in cfg["subsets"]]
        
        self.U = set(range(self.n))
        
        self.quota = 3 * self.m
        self.query_used = 0
        
        self._game_info = {
            "n": self.n,
            "m": self.m,
            "quota": self.quota
        }

    def _parse_indices(self, s):
        if not s or s.strip() == "":
            return []
        return [int(x.strip()) for x in s.split(",") if x.strip()]

    def _get_union(self, indices):
        union = set()
        for idx in indices:
            if 1 <= idx <= self.m:
                union |= self.subsets[idx - 1]
        return union

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            parts = raw_ans.split(";")
            k_part = None
            set_part = None
            
            for part in parts:
                part = part.strip()
                if part.lower().startswith("k="):
                    k_part = part.split("=", 1)[1].strip()
                elif part.lower().startswith("set="):
                    set_part = part.split("=", 1)[1].strip()
            
            if k_part is None or set_part is None:
                return False
            
            k_ans = int(k_part)
            set_indices = self._parse_indices(set_part)
            
            if len(set_indices) != k_ans:
                return False
            
            if any(idx < 1 or idx > self.m for idx in set_indices):
                return False
            
            union = self._get_union(set_indices)
            if union != self.U:
                return False
            
            if k_ans == self.k_star:
                return True
            else:
                return False
                
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_prog" in parsed_info:
            remain = self.quota - self.query_used
            if self.config.language == "zh":
                return f"已用={self.query_used}, 剩余={remain}"
            else:
                return f"used={self.query_used}, remain={remain}"
        
        if self.query_used >= self.quota:
            raise ValueError("Query budget exhausted / 查询配额已用尽")
        
        try:
            self.query_used += 1
            
            if "query_count" in parsed_info:
                indices = self._parse_indices(parsed_info["query_count"])
                if not indices:
                    raise ValueError("Empty index list")
                if any(idx < 1 or idx > self.m for idx in indices):
                    raise ValueError("Index out of range")
                union = self._get_union(indices)
                return str(len(union))
            
            elif "query_marg" in parsed_info:
                raw = parsed_info["query_marg"]
                if "+" not in raw:
                    raise ValueError("Invalid MARG format")
                base_part, new_part = raw.split("+", 1)
                base_indices = self._parse_indices(base_part)
                new_indices = self._parse_indices(new_part)
                
                if not new_indices:
                    raise ValueError("No new index specified")
                if any(idx < 1 or idx > self.m for idx in base_indices + new_indices):
                    raise ValueError("Index out of range")
                
                base_union = self._get_union(base_indices)
                full_union = self._get_union(base_indices + new_indices)
                marginal = len(full_union) - len(base_union)
                return str(marginal)
            
            elif "query_comp" in parsed_info:
                raw = parsed_info["query_comp"]
                if " vs " not in raw:
                    raise ValueError("Invalid COMP format")
                left_part, right_part = raw.split(" vs ", 1)
                left_indices = self._parse_indices(left_part)
                right_indices = self._parse_indices(right_part)
                
                if not left_indices or not right_indices:
                    raise ValueError("Empty index list in comparison")
                if any(idx < 1 or idx > self.m for idx in left_indices + right_indices):
                    raise ValueError("Index out of range")
                
                left_union = self._get_union(left_indices)
                right_union = self._get_union(right_indices)
                
                if len(left_union) > len(right_union):
                    return "A>B"
                elif len(left_union) < len(right_union):
                    return "A<B"
                else:
                    return "A=B"
            
            else:
                raise ValueError("No valid query tag found")
                
        except Exception as e:
            self.query_used -= 1
            raise

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "A>B":
            return "A<B"
        if correct == "A<B":
            return "A>B"
        if correct == "A=B":
            return "A>B"
        
        if "已用" in correct:
            return correct + "（数据有误）"
        if "used" in correct.lower():
            return correct + " (Data Error)"
            
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            if correct == "Yes": return "No"
            if correct == "YES": return "NO"
            if correct == "yes": return "no"
            return correct.replace("Yes", "No").replace("yes", "no")
        if "no" in lower_correct:
            if correct == "No": return "Yes"
            if correct == "NO": return "YES"
            if correct == "no": return "yes"
            return correct.replace("No", "Yes").replace("no", "yes")
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for r in range(1, self.m + 1):
            for combo in itertools.combinations(range(1, self.m + 1), r):
                indices = list(combo)
                indices_str = ",".join(map(str, indices))
                query_content = f"<query_count>{indices_str}</query_count>"
                
                union = self._get_union(indices)
                ans = str(len(union))
                
                queries.append({
                    "query": query_content,
                    "answer": ans
                })
        
        for r in range(0, self.m + 1):
            for base_combo in itertools.combinations(range(1, self.m + 1), r):
                base_indices = list(base_combo)
                base_str = ",".join(map(str, base_indices)) if base_indices else ""
                
                for new_idx in range(1, self.m + 1):
                    if not base_str:
                        marg_str = f"+{new_idx}"
                    else:
                        marg_str = f"{base_str}+{new_idx}"
                    
                    query_content = f"<query_marg>{marg_str}</query_marg>"
                    
                    new_indices = [new_idx]
                    base_union = self._get_union(base_indices)
                    full_union = self._get_union(base_indices + new_indices)
                    marginal = len(full_union) - len(base_union)
                    
                    queries.append({
                        "query": query_content,
                        "answer": str(marginal)
                    })
        
        for i in range(1, self.m + 1):
            for j in range(1, self.m + 1):
                if i == j: 
                    continue
                
                query_content = f"<query_comp>{i} vs {j}</query_comp>"
                
                u1 = self._get_union([i])
                u2 = self._get_union([j])
                
                if len(u1) > len(u2):
                    ans = "A>B"
                elif len(u1) < len(u2):
                    ans = "A<B"
                else:
                    ans = "A=B"
                    
                queries.append({
                    "query": query_content,
                    "answer": ans
                })
        
        return queries