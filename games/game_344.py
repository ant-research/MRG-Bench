# -*- coding: utf-8 -*-

from .base import Game
import random

class VectorInferenceGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "集合"

    game_rule_zh = """\
我们来玩一个"向量推理"游戏，规则如下：

游戏设定了一个未知的四维向量 (a, b, c, d)，其中 a、b、c、d 均为非负整数，且满足 a + b + c + d = 17。
你的目标是通过提问来推断出这个向量的精确值。

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答"是"或"否"：

1. **阈值查询**：询问某个分量是否大于等于某个值。例如："第 1 个分量是否大于等于 5？"
2. **余数查询**：询问某个分量除以 2 或 3 的余数是否等于某个值。例如："第 2 个分量除以 2 的余数是否等于 0？"
3. **比较查询**：询问两个不同分量之间的大小关系。例如："第 1 个分量是否大于等于第 3 个分量？"

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 阈值查询（询问第 i 个分量是否大于等于 t）：
<query_threshold>i,t</query_threshold>

其中 i 为 1 到 4 的整数，t 为 0 到 17 的整数。

- 余数查询（询问第 i 个分量除以 m 的余数是否等于 r）：
<query_modulo>i,m,r</query_modulo>

其中 i 为 1 到 4 的整数，m 为 2 或 3，r 为 0 到 m-1 的整数。

- 比较查询（询问第 i 个分量是否大于等于第 j 个分量）：
<query_compare>i,j</query_compare>

其中 i、j 为 1 到 4 的不同整数。

提交最终答案时，按顺序列出四个分量的值（用逗号隔开），格式如下：

<answer>a,b,c,d</answer>

例如：<answer>5,3,6,3</answer>
"""

    game_rule_en = """\
Let's play a "Vector Inference" game. Here are the rules:

The game has set an unknown four-dimensional vector (a, b, c, d), where a, b, c, d are all non-negative integers, and a + b + c + d = 17.
Your goal is to infer the exact values of this vector through queries.

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully with "Yes" or "No":

1. **Threshold Query**: Ask if a component is greater than or equal to a certain value. E.g., "Is the 1st component greater than or equal to 5?"
2. **Modulo Query**: Ask if a component modulo 2 or 3 equals a certain remainder. E.g., "Does the 2nd component modulo 2 equal 0?"
3. **Comparison Query**: Ask about the relationship between two different components. E.g., "Is the 1st component greater than or equal to the 3rd component?"

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Threshold Query (asking if the i-th component is greater than or equal to t):
<query_threshold>i,t</query_threshold>

where i is an integer from 1 to 4, and t is an integer from 0 to 17.

- Modulo Query (asking if the i-th component modulo m equals r):
<query_modulo>i,m,r</query_modulo>

where i is an integer from 1 to 4, m is 2 or 3, and r is an integer from 0 to m-1.

- Comparison Query (asking if the i-th component is greater than or equal to the j-th component):
<query_compare>i,j</query_compare>

where i, j are different integers from 1 to 4.

When submitting the final answer, list the four component values in order (comma-separated), using this format:

<answer>a,b,c,d</answer>

For example: <answer>5,3,6,3</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎使用城市交通指挥中心应急调度辅助系统。

当前，调度中心已将总计 17 辆应急通讯车秘密部署到 4 个关键交通枢纽。每个枢纽分配的车辆数均为非负整数，设这 4 个枢纽的车辆数分别为 a、b、c、d，且满足 a + b + c + d = 17。
作为调度稽查员，你的任务是通过系统接口推断出这 4 个枢纽各自的精确车辆部署数量。

你可以反复提交以下三类查询指令（每次仅限一个），系统会根据真实设定如实返回"是"或"否"：

1. **运力负荷评估（阈值查询）**：询问某个枢纽的车辆数是否大于等于某个值。例如："第 1 个枢纽的车辆数是否大于等于 5？"
2. **轮班编组检测（余数查询）**：询问某个枢纽的车辆数按 2 或 3 车一组进行编组后，余数是否等于某个值。例如："第 2 个枢纽按 2 车编组的余数是否等于 0？"
3. **枢纽运力对比（比较查询）**：询问两个不同枢纽之间车辆数量的大小关系。例如："第 1 个枢纽的车辆数是否大于等于第 3 个枢纽？"

当你收集足够信息后，请提交最终审计结果。若答案错误或格式不符，排查任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 运力负荷评估（询问第 i 个枢纽车辆数是否大于等于 t）：
<query_threshold>i,t</query_threshold>

其中 i 为 1 到 4 的整数，t 为 0 到 17 的整数。

- 轮班编组检测（询问第 i 个枢纽车辆数除以 m 的余数是否等于 r）：
<query_modulo>i,m,r</query_modulo>

其中 i 为 1 到 4 的整数，m 为 2 或 3，r 为 0 到 m-1 的整数。

- 枢纽运力对比（询问第 i 个枢纽车辆数是否大于等于第 j 个枢纽）：
<query_compare>i,j</query_compare>

其中 i、j 为 1 到 4 的不同整数。

提交最终答案时，按顺序列出四个枢纽的部署数量（用逗号隔开），格式如下：

<answer>a,b,c,d</answer>

例如：<answer>5,3,6,3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the City Traffic Command Center Emergency Dispatch System.

The command center has covertly deployed a total of 17 emergency communication vehicles to 4 key traffic hubs. The number of vehicles at each hub is a non-negative integer. Let the vehicle counts for the 4 hubs be a, b, c, and d, satisfying a + b + c + d = 17.
As a dispatch auditor, your task is to infer the exact number of deployed vehicles at each hub through the query interface.

You can repeatedly submit the following three types of queries (one per turn), and the system will truthfully return "Yes" or "No":

1. **Capacity Load Assessment (Threshold Query)**: Ask if the number of vehicles at a hub is greater than or equal to a certain value. E.g., "Is the number of vehicles at the 1st hub greater than or equal to 5?"
2. **Shift Platoon Detection (Modulo Query)**: Ask if the remainder of a hub's vehicle count, when grouped by 2 or 3, equals a certain value. E.g., "Does the 2nd hub's vehicle count modulo 2 equal 0?"
3. **Hub Capacity Comparison (Comparison Query)**: Ask about the relationship between the vehicle counts of two different hubs. E.g., "Is the vehicle count of the 1st hub greater than or equal to that of the 3rd hub?"

When you have enough information, submit your final audit result. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Capacity Load Assessment (asking if the i-th hub is greater than or equal to t):
<query_threshold>i,t</query_threshold>

where i is an integer from 1 to 4, and t is an integer from 0 to 17.

- Shift Platoon Detection (asking if the i-th hub modulo m equals r):
<query_modulo>i,m,r</query_modulo>

where i is an integer from 1 to 4, m is 2 or 3, and r is an integer from 0 to m-1.

- Hub Capacity Comparison (asking if the i-th hub is greater than or equal to the j-th hub):
<query_compare>i,j</query_compare>

where i, j are different integers from 1 to 4.

When submitting the final answer, list the four hub vehicle counts in order (comma-separated), using this format:

<answer>a,b,c,d</answer>

For example: <answer>5,3,6,3</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎进入医疗资源核心调度系统。

药剂科已将最新批次的 17 剂特效靶向药定向分配给 4 个重症病区。每个病区分配到的药剂数均为非负整数，设这 4 个病区的药剂数分别为 a、b、c、d，且满足 a + b + c + d = 17。
作为合规稽查员，你的任务是通过审计查询接口推断出各病区的精确药剂分配量。

你可以反复提交以下三类查询指令（每次仅限一个），系统会根据真实设定如实返回"是"或"否"：

1. **剂量达标测试（阈值查询）**：询问某个病区的药剂数是否大于等于某个标准值。例如："第 1 个病区的药剂数是否大于等于 5？"
2. **用药频次核对（余数查询）**：询问某个病区药剂数按 2 剂或 3 剂一疗程划分后，余数是否等于某个值。例如："第 2 个病区的药剂数按 2 剂划分疗程的余数是否等于 0？"
3. **病区资源优先级比对（比较查询）**：询问两个不同病区之间药剂数量的大小关系。例如："第 1 个病区的药剂数是否大于等于第 3 个病区？"

当你收集足够信息后，请提交最终审查结果。若答案错误或格式不符，审计任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 剂量达标测试（询问第 i 个病区药剂数是否大于等于 t）：
<query_threshold>i,t</query_threshold>

其中 i 为 1 到 4 的整数，t 为 0 到 17 的整数。

- 用药频次核对（询问第 i 个病区药剂数除以 m 的余数是否等于 r）：
<query_modulo>i,m,r</query_modulo>

其中 i 为 1 到 4 的整数，m 为 2 或 3，r 为 0 到 m-1 的整数。

- 病区资源优先级比对（询问第 i 个病区药剂数是否大于等于第 j 个病区）：
<query_compare>i,j</query_compare>

其中 i、j 为 1 到 4 的不同整数。

提交最终答案时，按顺序列出四个病区的药剂分配量（用逗号隔开），格式如下：

<answer>a,b,c,d</answer>

例如：<answer>5,3,6,3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Medical Resource Core Dispatch System.

The pharmacy department has allocated the latest batch of 17 doses of targeted drugs to 4 intensive care wards. The number of doses assigned to each ward is a non-negative integer. Let the drug counts for the 4 wards be a, b, c, and d, satisfying a + b + c + d = 17.
As a compliance auditor, your task is to infer the exact drug allocation for each ward through the audit query interface.

You can repeatedly submit the following three types of queries (one per turn), and the system will truthfully return "Yes" or "No":

1. **Dosage Compliance Test (Threshold Query)**: Ask if the number of doses in a ward is greater than or equal to a certain standard value. E.g., "Is the number of doses in the 1st ward greater than or equal to 5?"
2. **Medication Frequency Verification (Modulo Query)**: Ask if the remainder of a ward's drug count, when divided into regimens of 2 or 3 doses, equals a certain value. E.g., "Does the 2nd ward's dose count modulo 2 equal 0?"
3. **Ward Resource Priority Comparison (Comparison Query)**: Ask about the relationship between the drug counts of two different wards. E.g., "Is the drug count of the 1st ward greater than or equal to that of the 3rd ward?"

When you have enough information, submit your final review result. If the answer is wrong or the format is invalid, the audit fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Dosage Compliance Test (asking if the i-th ward is greater than or equal to t):
<query_threshold>i,t</query_threshold>

where i is an integer from 1 to 4, and t is an integer from 0 to 17.

- Medication Frequency Verification (asking if the i-th ward modulo m equals r):
<query_modulo>i,m,r</query_modulo>

where i is an integer from 1 to 4, m is 2 or 3, and r is an integer from 0 to m-1.

- Ward Resource Priority Comparison (asking if the i-th ward is greater than or equal to the j-th ward):
<query_compare>i,j</query_compare>

where i, j are different integers from 1 to 4.

When submitting the final answer, list the four ward drug allocations in order (comma-separated), using this format:

<answer>a,b,c,d</answer>

For example: <answer>5,3,6,3</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎进入市教育局资源分配核查系统。

本年度共有 17 个稀缺的高级教师进修名额，已被定向分配给 4 所重点高中。各高中获得的名额数均为非负整数，设这 4 所高中的名额数分别为 a、b、c、d，且满足 a + b + c + d = 17。
你的任务是通过系统的评估接口推断出各所高中分得的精确名额数量。

你可以反复提交以下三类查询指令（每次仅限一个），系统会根据真实设定如实返回"是"或"否"：

1. **最低配额审核（阈值查询）**：询问某所高中的名额数是否大于等于某个基准值。例如："第 1 所高中的名额数是否大于等于 5？"
2. **名额均分测试（余数查询）**：询问某所高中的名额按 2 人或 3 人一档进行均分后，余数是否等于某个值。例如："第 2 所高中的名额按 2 人均分后的余数是否等于 0？"
3. **校际名额对比（比较查询）**：询问两所不同高中之间名额分配数量的大小关系。例如："第 1 所高中的名额数是否大于等于第 3 所高中？"

当你收集足够信息后，请提交最终核查结果。若答案错误或格式不符，评估任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 最低配额审核（询问第 i 所高中名额数是否大于等于 t）：
<query_threshold>i,t</query_threshold>

其中 i 为 1 到 4 的整数，t 为 0 到 17 的整数。

- 名额均分测试（询问第 i 所高中名额数除以 m 的余数是否等于 r）：
<query_modulo>i,m,r</query_modulo>

其中 i 为 1 到 4 的整数，m 为 2 或 3，r 为 0 到 m-1 的整数。

- 校际名额对比（询问第 i 所高中名额数是否大于等于第 j 所高中）：
<query_compare>i,j</query_compare>

其中 i、j 为 1 到 4 的不同整数。

提交最终答案时，按顺序列出四所高中的名额数量（用逗号隔开），格式如下：

<answer>a,b,c,d</answer>

例如：<answer>5,3,6,3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Municipal Education Bureau Resource Allocation Audit System.

This year, there are 17 scarce advanced teacher training quotas allocated to 4 key high schools. The number of quotas each school received is a non-negative integer. Let the quota counts for the 4 schools be a, b, c, and d, satisfying a + b + c + d = 17.
Your task is to infer the exact number of quotas allocated to each high school through the system's evaluation interface.

You can repeatedly submit the following three types of queries (one per turn), and the system will truthfully return "Yes" or "No":

1. **Minimum Quota Audit (Threshold Query)**: Ask if a high school's quota count is greater than or equal to a certain benchmark value. E.g., "Is the 1st school's quota count greater than or equal to 5?"
2. **Quota Even-Split Test (Modulo Query)**: Ask if the remainder of a school's quota count, when split evenly into tiers of 2 or 3 people, equals a certain value. E.g., "Does the 2nd school's quota count modulo 2 equal 0?"
3. **Inter-School Quota Comparison (Comparison Query)**: Ask about the relationship between the quota allocations of two different schools. E.g., "Is the 1st school's quota count greater than or equal to the 3rd school's?"

When you have enough information, submit your final audit result. If the answer is wrong or the format is invalid, the evaluation task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Minimum Quota Audit (asking if the i-th school is greater than or equal to t):
<query_threshold>i,t</query_threshold>

where i is an integer from 1 to 4, and t is an integer from 0 to 17.

- Quota Even-Split Test (asking if the i-th school modulo m equals r):
<query_modulo>i,m,r</query_modulo>

where i is an integer from 1 to 4, m is 2 or 3, and r is an integer from 0 to m-1.

- Inter-School Quota Comparison (asking if the i-th school is greater than or equal to the j-th school):
<query_compare>i,j</query_compare>

where i, j are different integers from 1 to 4.

When submitting the final answer, list the four school quota counts in order (comma-separated), using this format:

<answer>a,b,c,d</answer>

For example: <answer>5,3,6,3</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎使用智能制造控制塔物料追踪系统。

目前，系统已将 17 批次的核心原材料调拨至 4 条自动化生产线。各产线分配的物料批次数均为非负整数，设这 4 条产线的物料批次数分别为 a、b、c、d，且满足 a + b + c + d = 17。
你的任务是通过系统的追踪判定接口，推断出每条产线的精确物料批次数量。

你可以反复提交以下三类查询指令（每次仅限一个），系统会根据真实设定如实返回"是"或"否"：

1. **产能达标判定（阈值查询）**：询问某条产线的物料批次是否大于等于某个目标值。例如："第 1 条产线的物料批次是否大于等于 5？"
2. **托盘打包校验（余数查询）**：询问某条产线的物料按 2 批次或 3 批次装满一托盘后，余数是否等于某个值。例如："第 2 条产线按 2 批次装配的余数是否等于 0？"
3. **产线负荷对比（比较查询）**：询问两条不同产线之间物料分配数量的大小关系。例如："第 1 条产线的物料批次是否大于等于第 3 条产线？"

当你收集足够信息后，请提交最终校验报告。若答案错误或格式不符，追踪任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 产能达标判定（询问第 i 条产线物料批次是否大于等于 t）：
<query_threshold>i,t</query_threshold>

其中 i 为 1 到 4 的整数，t 为 0 到 17 的整数。

- 托盘打包校验（询问第 i 条产线物料批次除以 m 的余数是否等于 r）：
<query_modulo>i,m,r</query_modulo>

其中 i 为 1 到 4 的整数，m 为 2 或 3，r 为 0 到 m-1 的整数。

- 产线负荷对比（询问第 i 条产线物料批次是否大于等于第 j 条产线）：
<query_compare>i,j</query_compare>

其中 i、j 为 1 到 4 的不同整数。

提交最终答案时，按顺序列出四条产线的物料批次数（用逗号隔开），格式如下：

<answer>a,b,c,d</answer>

例如：<answer>5,3,6,3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart Manufacturing Control Tower Material Tracking System.

Currently, the system has dispatched 17 batches of critical raw materials to 4 automated production lines. The number of material batches assigned to each line is a non-negative integer. Let the batch counts for the 4 production lines be a, b, c, and d, satisfying a + b + c + d = 17.
Your task is to infer the exact number of material batches for each production line through the tracking assessment interface.

You can repeatedly submit the following three types of queries (one per turn), and the system will truthfully return "Yes" or "No":

1. **Capacity Compliance Assessment (Threshold Query)**: Ask if a production line's material batch count is greater than or equal to a target value. E.g., "Is the 1st line's batch count greater than or equal to 5?"
2. **Pallet Packaging Validation (Modulo Query)**: Ask if the remainder of a line's batches, when packed by 2 or 3 per pallet, equals a certain value. E.g., "Does the 2nd line's batch count modulo 2 equal 0?"
3. **Production Line Load Comparison (Comparison Query)**: Ask about the relationship between the material counts of two different production lines. E.g., "Is the 1st line's batch count greater than or equal to the 3rd line's?"

When you have enough information, submit your final validation report. If the answer is wrong or the format is invalid, the tracking task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Capacity Compliance Assessment (asking if the i-th line is greater than or equal to t):
<query_threshold>i,t</query_threshold>

where i is an integer from 1 to 4, and t is an integer from 0 to 17.

- Pallet Packaging Validation (asking if the i-th line modulo m equals r):
<query_modulo>i,m,r</query_modulo>

where i is an integer from 1 to 4, m is 2 or 3, and r is an integer from 0 to m-1.

- Production Line Load Comparison (asking if the i-th line is greater than or equal to the j-th line):
<query_compare>i,j</query_compare>

where i, j are different integers from 1 to 4.

When submitting the final answer, list the four line batch counts in order (comma-separated), using this format:

<answer>a,b,c,d</answer>

For example: <answer>5,3,6,3</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎登录律所核心案卷分配审计系统。

管理委员会已将 17 宗重大连环并购案的宗卷分配给 4 个核心律师团队。各团队承接的案卷数均为非负整数，设这 4 个团队的案卷数分别为 a、b、c、d，且满足 a + b + c + d = 17。
作为合规审计员，你的任务是通过内部核查系统，推断出各团队承接的精确案卷数量。

你可以反复提交以下三类审计查询指令（每次仅限一个），系统会根据真实设定如实返回"是"或"否"：

1. **工作量合规审查（阈值查询）**：询问某个团队的案卷数是否大于等于某个合规阈值。例如："第 1 个团队的案卷数是否大于等于 5？"
2. **交叉复核编组验证（余数查询）**：询问某个团队的案卷按 2 卷或 3 卷一组进行交叉审阅后，余数是否等于某个值。例如："第 2 个团队按 2 卷编组的余数是否等于 0？"
3. **团队负荷权衡（比较查询）**：询问两个不同团队之间案卷分配数量的大小关系。例如："第 1 个团队的案卷数是否大于等于第 3 个团队？"

当你收集足够信息后，请提交最终审计结果。若答案错误或格式不符，审计任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 工作量合规审查（询问第 i 个团队案卷数是否大于等于 t）：
<query_threshold>i,t</query_threshold>

其中 i 为 1 到 4 的整数，t 为 0 到 17 的整数。

- 交叉复核编组验证（询问第 i 个团队案卷数除以 m 的余数是否等于 r）：
<query_modulo>i,m,r</query_modulo>

其中 i 为 1 到 4 的整数，m 为 2 或 3，r 为 0 到 m-1 的整数。

- 团队负荷权衡（询问第 i 个团队案卷数是否大于等于第 j 个团队）：
<query_compare>i,j</query_compare>

其中 i、j 为 1 到 4 的不同整数。

提交最终答案时，按顺序列出四个团队的案卷数量（用逗号隔开），格式如下：

<answer>a,b,c,d</answer>

例如：<answer>5,3,6,3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Law Firm Core Case File Allocation Audit System.

The management committee has allocated 17 serial M&A case files to 4 core legal teams. The number of case files assigned to each team is a non-negative integer. Let the case file counts for the 4 teams be a, b, c, and d, satisfying a + b + c + d = 17.
As a compliance auditor, your task is to infer the exact number of case files assigned to each team through the internal verification system.

You can repeatedly submit the following three types of audit queries (one per turn), and the system will truthfully return "Yes" or "No":

1. **Workload Compliance Review (Threshold Query)**: Ask if a team's case file count is greater than or equal to a certain compliance threshold. E.g., "Is the 1st team's case count greater than or equal to 5?"
2. **Cross-Review Grouping Validation (Modulo Query)**: Ask if the remainder of a team's case count, when grouped by 2 or 3 for cross-review, equals a certain value. E.g., "Does the 2nd team's case count modulo 2 equal 0?"
3. **Team Load Balancing (Comparison Query)**: Ask about the relationship between the case file counts of two different teams. E.g., "Is the 1st team's case count greater than or equal to the 3rd team's?"

When you have enough information, submit your final audit result. If the answer is wrong or the format is invalid, the audit task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Workload Compliance Review (asking if the i-th team is greater than or equal to t):
<query_threshold>i,t</query_threshold>

where i is an integer from 1 to 4, and t is an integer from 0 to 17.

- Cross-Review Grouping Validation (asking if the i-th team modulo m equals r):
<query_modulo>i,m,r</query_modulo>

where i is an integer from 1 to 4, m is 2 or 3, and r is an integer from 0 to m-1.

- Team Load Balancing (asking if the i-th team is greater than or equal to the j-th team):
<query_compare>i,j</query_compare>

where i, j are different integers from 1 to 4.

When submitting the final answer, list the four team case counts in order (comma-separated), using this format:

<answer>a,b,c,d</answer>

For example: <answer>5,3,6,3</answer>
"""

    tags = ["answer", "query_threshold", "query_modulo", "query_compare"]

    # 使用基于 seed 的可控随机生成，保持可复现性同时避免答案硬编码
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"max_component": 6,  "seed_offset": 0},   # 简单：分量较均匀
            2: {"max_component": 8,  "seed_offset": 100},  # 中等偏下
            3: {"max_component": 10, "seed_offset": 200},  # 中等偏上
            4: {"max_component": 12, "seed_offset": 300},  # 较难
            5: {"max_component": 17, "seed_offset": 400},  # 难：极端分布
        },
        "en": {
            1: {"max_component": 6,  "seed_offset": 0},
            2: {"max_component": 8,  "seed_offset": 100},
            3: {"max_component": 10, "seed_offset": 200},
            4: {"max_component": 12, "seed_offset": 300},
            5: {"max_component": 17, "seed_offset": 400},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，设置目标向量（基于可控随机）"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数，兼容字符串传入

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        max_comp = cfg["max_component"]
        seed_offset = cfg["seed_offset"]

        # 使用固定 seed 保证可复现
        rng = random.Random(42 + seed_offset)
        total = 17
        vector = []
        for _ in range(3):
            upper = min(max_comp, total)
            val = rng.randint(0, upper)
            vector.append(val)
            total -= val
        vector.append(total)

        # 如果最后一个分量超出 max_component 限制，重新打乱直到合法
        # （简单策略：直接用生成的向量，极端分布本身就是高难度的特征）
        rng.shuffle(vector)

        self.target_vector = vector

        # 验证向量合法性
        assert len(self.target_vector) == 4, "Vector must have 4 components"
        assert all(isinstance(x, int) and x >= 0 for x in self.target_vector), "All components must be non-negative integers"
        assert sum(self.target_vector) == 17, "Sum of components must be 17"
        
        # game_info 用于格式化规则文本（本游戏无需填充参数）
        self._game_info = {}

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            # 解析答案：a,b,c,d
            parts = [x.strip() for x in raw_ans.split(",")]
            if len(parts) != 4:
                return False
            
            # 转换为整数
            answer_vector = [int(x) for x in parts]
            
            # 检查是否匹配目标向量
            return answer_vector == self.target_vector
            
        except (ValueError, AttributeError):
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            err_format = "错误：格式无效。"
            err_range = "错误：参数超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            err_format = "Error: Invalid format."
            err_range = "Error: Parameter out of range."

        # 优先级：threshold > modulo > compare
        if "query_threshold" in parsed_info:
            try:
                raw = parsed_info["query_threshold"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return err_format
                
                i = int(parts[0])
                t = int(parts[1])
                
                # 检查参数范围
                if i < 1 or i > 4 or t < 0 or t > 17:
                    return err_range
                
                # 获取对应分量（索引从0开始）
                component = self.target_vector[i - 1]
                return yes_res if component >= t else no_res
                
            except (ValueError, IndexError):
                return err_format

        elif "query_modulo" in parsed_info:
            try:
                raw = parsed_info["query_modulo"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    return err_format
                
                i = int(parts[0])
                m = int(parts[1])
                r = int(parts[2])
                
                # 检查参数范围
                if i < 1 or i > 4:
                    return err_range
                if m not in [2, 3]:
                    return err_range
                if r < 0 or r >= m:
                    return err_range
                
                # 获取对应分量并检查余数
                component = self.target_vector[i - 1]
                return yes_res if component % m == r else no_res
                
            except (ValueError, IndexError):
                return err_format

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return err_format
                
                i = int(parts[0])
                j = int(parts[1])
                
                # 检查参数范围
                if i < 1 or i > 4 or j < 1 or j > 4:
                    return err_range
                if i == j:
                    return err_range
                
                # 比较两个分量
                comp_i = self.target_vector[i - 1]
                comp_j = self.target_vector[j - 1]
                return yes_res if comp_i >= comp_j else no_res
                
            except (ValueError, IndexError):
                return err_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的 Yes/No（是/否）响应取反，生成一个错误答案。
        """
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
            else:
                # 对于错误提示等非标准回复，附加一段干扰文本
                return correct + "（数据异常）"
        else:
            if correct == "Yes":
                return "No"
            elif correct == "No":
                return "Yes"
            else:
                return correct + " (data anomaly)"

    def get_all_possible_queries(self) -> list:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串（完整XML），与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        
        # 1. Threshold queries: i=1..4, t=0..17
        for i in range(1, 5):
            for t in range(18):
                # 构造 content 与 XML
                content = f"{i},{t}"
                query_xml = f"<query_threshold>{content}</query_threshold>"
                
                # 构造 simulation parsed_info
                parsed_info = {"query_threshold": content}
                
                # 获取正确答案
                answer = self._cf_core_produce(parsed_info)
                results.append({"query": query_xml, "answer": answer})
        
        # 2. Modulo queries: i=1..4, m in [2, 3], r in 0..m-1
        for i in range(1, 5):
            for m in [2, 3]:
                for r in range(m):
                    content = f"{i},{m},{r}"
                    query_xml = f"<query_modulo>{content}</query_modulo>"
                    parsed_info = {"query_modulo": content}
                    answer = self._cf_core_produce(parsed_info)
                    results.append({"query": query_xml, "answer": answer})
        
        # 3. Comparison queries: i,j=1..4, i!=j
        for i in range(1, 5):
            for j in range(1, 5):
                if i != j:
                    content = f"{i},{j}"
                    query_xml = f"<query_compare>{content}</query_compare>"
                    parsed_info = {"query_compare": content}
                    answer = self._cf_core_produce(parsed_info)
                    results.append({"query": query_xml, "answer": answer})
                    
        return results