from .base import Game
import random


class BinarySequenceDeductionGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"二值序列推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的未知二值序列 S[1..{n}]，每个位置的值为 0 或 1。已知 S[1] = 1。

定义相邻差分变量 E[1..{n_minus_1}]，其中 E[i] 表示 S[i] 和 S[i+1] 的异或值（当 S[i] 和 S[i+1] 相等时 E[i] = 0，不相等时 E[i] = 1）。

你的目标是推理出完整的序列 S[1..{n}]。你可以反复提出以下三类问题（每次仅限一个问题），我会如实回答：

1. 差分查询：询问 E[i] 的值（i 的范围是 1 到 {n_minus_1}）。回答为 0 或 1。
2. 差分比较查询：询问 E[i] 和 E[i+1] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。
3. 跨位比较查询：询问 S[i] 和 S[i+2] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 差分查询（例如询问 E[3]）：
<query_diff>3</query_diff>

- 差分比较查询（例如询问 E[2] 和 E[3] 是否相等）：
<query_diff_compare>2</query_diff_compare>

- 跨位比较查询（例如询问 S[1] 和 S[3] 是否相等）：
<query_skip_compare>1</query_skip_compare>

提交最终答案时，请列出完整序列（用逗号隔开），格式如下：

<answer>1,0,0,1,1,0</answer>
"""

    game_rule_en = """\
Let's play a "Binary Sequence Deduction" game. Here are the rules:

There is a hidden binary sequence S[1..{n}] of length {n}, where each position has a value of 0 or 1. It is known that S[1] = 1.

Define the adjacent difference variable E[1..{n_minus_1}], where E[i] represents the XOR of S[i] and S[i+1] (E[i] = 0 when S[i] and S[i+1] are equal, E[i] = 1 when they are different).

Your goal is to deduce the complete sequence S[1..{n}]. You can repeatedly ask the following three types of questions (one per turn), and I will answer truthfully:

1. Difference Query: Ask for the value of E[i] (i ranges from 1 to {n_minus_1}). Answer is 0 or 1.
2. Difference Comparison Query: Ask if E[i] and E[i+1] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".
3. Skip Comparison Query: Ask if S[i] and S[i+2] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Difference Query (e.g., asking for E[3]):
<query_diff>3</query_diff>

- Difference Comparison Query (e.g., asking if E[2] and E[3] are equal):
<query_diff_compare>2</query_diff_compare>

- Skip Comparison Query (e.g., asking if S[1] and S[3] are equal):
<query_skip_compare>1</query_skip_compare>

When submitting the final answer, list the complete sequence (comma-separated), using this format:

<answer>1,0,0,1,1,0</answer>
"""

    contextualized_rule_zh_1 = """\
【交通场景】
我们来进入一个交通信号灯控制推理任务，规则如下：

有一条包含 {n} 个连续路口的干道，每个路口的信号灯状态 S[1..{n}] 未知。状态 S[i] 的值为 1（绿灯）或 0（红灯）。已知第 1 个路口是绿灯（S[1] = 1）。

定义相邻路口的状态切换指示器 E[1..{n_minus_1}]，其中 E[i] 表示 S[i] 和 S[i+1] 的异或值（当 S[i] 和 S[i+1] 状态相同时 E[i] = 0，不相同时 E[i] = 1）。

你的目标是推理出所有路口的完整信号灯状态序列 S[1..{n}]。你可以反复提出以下三类问题（每次仅限一个问题），我会如实回答：

1. 切换状态查询：询问 E[i] 的值（i 的范围是 1 到 {n_minus_1}）。回答为 0 或 1。
2. 切换比较查询：询问 E[i] 和 E[i+1] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。
3. 跨路口状态比较查询：询问 S[i] 和 S[i+2] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 切换状态查询（例如询问 E[3]）：
<query_diff>3</query_diff>

- 切换比较查询（例如询问 E[2] 和 E[3] 是否相等）：
<query_diff_compare>2</query_diff_compare>

- 跨路口状态比较查询（例如询问 S[1] 和 S[3] 是否相等）：
<query_skip_compare>1</query_skip_compare>

提交最终答案时，请列出完整序列（用逗号隔开），格式如下：

<answer>1,0,0,1,1,0</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's engage in a traffic light control deduction task. Here are the rules:

There is an arterial road with {n} consecutive intersections. The traffic light status at each intersection S[1..{n}] is hidden. Each status S[i] is either 1 (Green) or 0 (Red). It is known that the first intersection is green (S[1] = 1).

Define the adjacent intersection status transition indicator E[1..{n_minus_1}], where E[i] represents the XOR of S[i] and S[i+1] (E[i] = 0 when S[i] and S[i+1] are identical, E[i] = 1 when they differ).

Your goal is to deduce the complete traffic light status sequence S[1..{n}]. You can repeatedly ask the following three types of questions (one per turn), and I will answer truthfully:

1. Transition Indicator Query: Ask for the value of E[i] (i ranges from 1 to {n_minus_1}). Answer is 0 or 1.
2. Transition Comparison Query: Ask if E[i] and E[i+1] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".
3. Skip Intersection Status Comparison Query: Ask if S[i] and S[i+2] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Transition Indicator Query (e.g., asking for E[3]):
<query_diff>3</query_diff>

- Transition Comparison Query (e.g., asking if E[2] and E[3] are equal):
<query_diff_compare>2</query_diff_compare>

- Skip Intersection Status Comparison Query (e.g., asking if S[1] and S[3] are equal):
<query_skip_compare>1</query_skip_compare>

When submitting the final answer, list the complete sequence (comma-separated), using this format:

<answer>1,0,0,1,1,0</answer>
"""

    contextualized_rule_zh_2 = """\
【医疗场景】
我们来进行一项患者生命体征监测数据的推理任务，规则如下：

有一组按时间顺序排列的 {n} 次患者体征监测记录，每次记录的异常标志 S[1..{n}] 未知。S[i] 的值为 1（异常）或 0（正常）。已知第 1 次记录为异常（S[1] = 1）。

定义相邻记录的体征突变标志 E[1..{n_minus_1}]，其中 E[i] 表示 S[i] 和 S[i+1] 的异或值（当 S[i] 和 S[i+1] 状态相同时 E[i] = 0，不相同时 E[i] = 1）。

你的目标是推理出全部 {n} 次监测记录的完整异常标志序列 S[1..{n}]。你可以反复提出以下三类问题（每次仅限一个问题），我会如实回答：

1. 突变标志查询：询问 E[i] 的值（i 的范围是 1 到 {n_minus_1}）。回答为 0 或 1。
2. 突变比较查询：询问 E[i] 和 E[i+1] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。
3. 跨次体征比较查询：询问 S[i] 和 S[i+2] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 突变标志查询（例如询问 E[3]）：
<query_diff>3</query_diff>

- 突变比较查询（例如询问 E[2] 和 E[3] 是否相等）：
<query_diff_compare>2</query_diff_compare>

- 跨次体征比较查询（例如询问 S[1] 和 S[3] 是否相等）：
<query_skip_compare>1</query_skip_compare>

提交最终答案时，请列出完整序列（用逗号隔开），格式如下：

<answer>1,0,0,1,1,0</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's conduct a deduction task for a patient's vital sign monitoring data. Here are the rules:

There is a chronological series of {n} patient vital sign monitoring records. The abnormality flag S[1..{n}] for each record is hidden. Each flag S[i] is either 1 (Abnormal) or 0 (Normal). It is known that the first record is abnormal (S[1] = 1).

Define the adjacent record mutation flag E[1..{n_minus_1}], where E[i] represents the XOR of S[i] and S[i+1] (E[i] = 0 when S[i] and S[i+1] are identical, E[i] = 1 when they differ).

Your goal is to deduce the complete abnormality flag sequence S[1..{n}]. You can repeatedly ask the following three types of questions (one per turn), and I will answer truthfully:

1. Mutation Flag Query: Ask for the value of E[i] (i ranges from 1 to {n_minus_1}). Answer is 0 or 1.
2. Mutation Comparison Query: Ask if E[i] and E[i+1] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".
3. Skip Record Comparison Query: Ask if S[i] and S[i+2] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Mutation Flag Query (e.g., asking for E[3]):
<query_diff>3</query_diff>

- Mutation Comparison Query (e.g., asking if E[2] and E[3] are equal):
<query_diff_compare>2</query_diff_compare>

- Skip Record Comparison Query (e.g., asking if S[1] and S[3] are equal):
<query_skip_compare>1</query_skip_compare>

When submitting the final answer, list the complete sequence (comma-separated), using this format:

<answer>1,0,0,1,1,0</answer>
"""

    contextualized_rule_zh_3 = """\
【教育场景】
我们来进行一项自适应学习系统的学情诊断推理任务，规则如下：

有一套包含 {n} 道题目的自适应测试卷，每道题的知识点掌握度状态 S[1..{n}] 未知。状态 S[i] 为 1（已掌握）或 0（未掌握）。已知第 1 道题的状态为已掌握（S[1] = 1）。

定义相邻题目的掌握度跳变系数 E[1..{n_minus_1}]，其中 E[i] 表示 S[i] 和 S[i+1] 的异或值（当 S[i] 和 S[i+1] 状态相同时 E[i] = 0，不相同时 E[i] = 1）。

你的目标是推断出完整的掌握度状态序列 S[1..{n}]。你可以反复提出以下三类问题（每次仅限一个问题），我会如实回答：

1. 跳变系数查询：询问 E[i] 的值（i 的范围是 1 到 {n_minus_1}）。回答为 0 或 1。
2. 跳变比较查询：询问 E[i] 和 E[i+1] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。
3. 跨题状态比较查询：询问 S[i] 和 S[i+2] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，诊断失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 跳变系数查询（例如询问 E[3]）：
<query_diff>3</query_diff>

- 跳变比较查询（例如询问 E[2] 和 E[3] 是否相等）：
<query_diff_compare>2</query_diff_compare>

- 跨题状态比较查询（例如询问 S[1] 和 S[3] 是否相等）：
<query_skip_compare>1</query_skip_compare>

提交最终答案时，请列出完整序列（用逗号隔开），格式如下：

<answer>1,0,0,1,1,0</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a learning profile diagnostic task for an adaptive learning system. Here are the rules:

There is an adaptive test paper containing {n} questions. The mastery status S[1..{n}] of the knowledge points for each question is hidden. Each status S[i] is either 1 (Mastered) or 0 (Unmastered). It is known that the first question is mastered (S[1] = 1).

Define the adjacent question mastery jump coefficient E[1..{n_minus_1}], where E[i] represents the XOR of S[i] and S[i+1] (E[i] = 0 when S[i] and S[i+1] share the same status, E[i] = 1 when they differ).

Your goal is to deduce the complete mastery status sequence S[1..{n}]. You can repeatedly ask the following three types of questions (one per turn), and I will answer truthfully:

1. Jump Coefficient Query: Ask for the value of E[i] (i ranges from 1 to {n_minus_1}). Answer is 0 or 1.
2. Jump Comparison Query: Ask if E[i] and E[i+1] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".
3. Skip Question Status Comparison Query: Ask if S[i] and S[i+2] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the diagnosis fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Jump Coefficient Query (e.g., asking for E[3]):
<query_diff>3</query_diff>

- Jump Comparison Query (e.g., asking if E[2] and E[3] are equal):
<query_diff_compare>2</query_diff_compare>

- Skip Question Status Comparison Query (e.g., asking if S[1] and S[3] are equal):
<query_skip_compare>1</query_skip_compare>

When submitting the final answer, list the complete sequence (comma-separated), using this format:

<answer>1,0,0,1,1,0</answer>
"""

    contextualized_rule_zh_4 = """\
【制造业/工业场景】
我们来执行一项流水线质检结果的逆向工程任务，规则如下：

流水线上有 {n} 个连续的质检工位，每个工位的检测结果 S[1..{n}] 未知。结果 S[i] 的值为 1（合格）或 0（不合格）。已知第 1 个工位的检测结果为合格（S[1] = 1）。

定义相邻工位的偏差指标 E[1..{n_minus_1}]，其中 E[i] 表示 S[i] 和 S[i+1] 的异或值（当 S[i] 和 S[i+1] 结果一致时 E[i] = 0，不一致时 E[i] = 1）。

你的目标是还原出所有工位的完整检测结果序列 S[1..{n}]。你可以反复提出以下三类问题（每次仅限一个问题），我会如实回答：

1. 偏差指标查询：询问 E[i] 的值（i 的范围是 1 到 {n_minus_1}）。回答为 0 或 1。
2. 偏差比较查询：询问 E[i] 和 E[i+1] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。
3. 跨工位结果比较查询：询问 S[i] 和 S[i+2] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 偏差指标查询（例如询问 E[3]）：
<query_diff>3</query_diff>

- 偏差比较查询（例如询问 E[2] 和 E[3] 是否相等）：
<query_diff_compare>2</query_diff_compare>

- 跨工位结果比较查询（例如询问 S[1] 和 S[3] 是否相等）：
<query_skip_compare>1</query_skip_compare>

提交最终答案时，请列出完整序列（用逗号隔开），格式如下：

<answer>1,0,0,1,1,0</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's execute a reverse engineering task for assembly line quality inspection results. Here are the rules:

On an assembly line, there are {n} consecutive quality inspection stations. The inspection result S[1..{n}] for each station is hidden. Each result S[i] is either 1 (Qualified) or 0 (Unqualified). It is known that the first station's result is qualified (S[1] = 1).

Define the adjacent station deviation index E[1..{n_minus_1}], where E[i] represents the XOR of S[i] and S[i+1] (E[i] = 0 when S[i] and S[i+1] are consistent, E[i] = 1 when they are inconsistent).

Your goal is to restore the complete inspection result sequence S[1..{n}]. You can repeatedly ask the following three types of questions (one per turn), and I will answer truthfully:

1. Deviation Index Query: Ask for the value of E[i] (i ranges from 1 to {n_minus_1}). Answer is 0 or 1.
2. Deviation Comparison Query: Ask if E[i] and E[i+1] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".
3. Skip Station Result Comparison Query: Ask if S[i] and S[i+2] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Deviation Index Query (e.g., asking for E[3]):
<query_diff>3</query_diff>

- Deviation Comparison Query (e.g., asking if E[2] and E[3] are equal):
<query_diff_compare>2</query_diff_compare>

- Skip Station Result Comparison Query (e.g., asking if S[1] and S[3] are equal):
<query_skip_compare>1</query_skip_compare>

When submitting the final answer, list the complete sequence (comma-separated), using this format:

<answer>1,0,0,1,1,0</answer>
"""

    contextualized_rule_zh_5 = """\
【法律场景】
我们来参与一场复杂商业纠纷案的证据链推演任务，规则如下：

案件中有 {n} 份按时间排序的关键证据文件，每份文件的证明倾向 S[1..{n}] 暂未公开。倾向 S[i] 的值为 1（支持原告）或 0（支持被告）。已知第 1 份文件支持原告（S[1] = 1）。

定义相邻证据的倾向反转标记 E[1..{n_minus_1}]，其中 E[i] 表示 S[i] 和 S[i+1] 的异或值（当 S[i] 和 S[i+1] 证明倾向一致时 E[i] = 0，对立时 E[i] = 1）。

你的目标是推演出完整的证据倾向序列 S[1..{n}]。你可以反复提出以下三类问题（每次仅限一个问题），我会如实回答：

1. 反转标记查询：询问 E[i] 的值（i 的范围是 1 到 {n_minus_1}）。回答为 0 或 1。
2. 反转比较查询：询问 E[i] 和 E[i+1] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。
3. 跨证据倾向比较查询：询问 S[i] 和 S[i+2] 是否相等（i 的范围是 1 到 {n_minus_2}）。回答"是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或逻辑不符，推演失败。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 反转标记查询（例如询问 E[3]）：
<query_diff>3</query_diff>

- 反转比较查询（例如询问 E[2] 和 E[3] 是否相等）：
<query_diff_compare>2</query_diff_compare>

- 跨证据倾向比较查询（例如询问 S[1] 和 S[3] 是否相等）：
<query_skip_compare>1</query_skip_compare>

提交最终答案时，请列出完整序列（用逗号隔开），格式如下：

<answer>1,0,0,1,1,0</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's engage in an evidentiary chain deduction task for a complex commercial dispute case. Here are the rules:

There are {n} key evidentiary documents sorted chronologically. The probative tendency S[1..{n}] of each document is undisclosed. Each tendency S[i] is either 1 (Pro-Plaintiff) or 0 (Pro-Defendant). It is known that the first document supports the plaintiff (S[1] = 1).

Define the adjacent evidence reversal marker E[1..{n_minus_1}], where E[i] represents the XOR of S[i] and S[i+1] (E[i] = 0 when S[i] and S[i+1] share the same tendency, E[i] = 1 when they conflict).

Your goal is to deduce the complete evidence tendency sequence S[1..{n}]. You can repeatedly ask the following three types of questions (one per turn), and I will answer truthfully:

1. Reversal Marker Query: Ask for the value of E[i] (i ranges from 1 to {n_minus_1}). Answer is 0 or 1.
2. Reversal Comparison Query: Ask if E[i] and E[i+1] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".
3. Skip Evidence Tendency Comparison Query: Ask if S[i] and S[i+2] are equal (i ranges from 1 to {n_minus_2}). Answer "Yes" or "No".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the deduction fails.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Reversal Marker Query (e.g., asking for E[3]):
<query_diff>3</query_diff>

- Reversal Comparison Query (e.g., asking if E[2] and E[3] are equal):
<query_diff_compare>2</query_diff_compare>

- Skip Evidence Tendency Comparison Query (e.g., asking if S[1] and S[3] are equal):
<query_skip_compare>1</query_skip_compare>

When submitting the final answer, list the complete sequence (comma-separated), using this format:

<answer>1,0,0,1,1,0</answer>
"""

    tags = ["answer", "query_diff", "query_diff_compare", "query_skip_compare"]

    # 难度配置：
    # 1 (简单)       - N=3, 确定性序列
    # 2 (中等偏下)   - N=5, 简单模式
    # 3 (中等偏上)   - N=6, 中等复杂度
    # 4 (较难)       - N=8, 较长序列
    # 5 (难)         - N=10, 最长序列

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 3,
                "sequence": [1, 0, 1],
            },
            2: {
                "n": 5,
                "sequence": [1, 1, 0, 0, 1],
            },
            3: {
                "n": 6,
                "sequence": [1, 0, 0, 1, 0, 1],
            },
            4: {
                "n": 8,
                "sequence": [1, 1, 0, 1, 1, 0, 0, 1],
            },
            5: {
                "n": 10,
                "sequence": [1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
            },
        },
        "en": {
            1: {
                "n": 3,
                "sequence": [1, 0, 1],
            },
            2: {
                "n": 5,
                "sequence": [1, 1, 0, 0, 1],
            },
            3: {
                "n": 6,
                "sequence": [1, 0, 0, 1, 0, 1],
            },
            4: {
                "n": 8,
                "sequence": [1, 1, 0, 1, 1, 0, 0, 1],
            },
            5: {
                "n": 10,
                "sequence": [1, 0, 1, 0, 0, 1, 1, 1, 0, 1],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度和语言选择配置，生成序列和差分数组"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        n = cfg["n"]
        self.sequence = cfg["sequence"]
        
        # 验证序列长度和首位
        assert len(self.sequence) == n, "Sequence length mismatch"
        assert self.sequence[0] == 1, "S[1] must be 1"
        
        # 计算差分数组 E[i] = S[i] XOR S[i+1]
        self.diff_array = []
        for i in range(n - 1):
            self.diff_array.append(self.sequence[i] ^ self.sequence[i + 1])
        
        # 设置游戏信息用于规则模板
        self._game_info["n"] = n
        self._game_info["n_minus_1"] = n - 1
        self._game_info["n_minus_2"] = n - 2

    def evaluate(self, parsed_info):
        """评估玩家提交的答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        try:
            # 解析答案：期望格式为逗号分隔的数字序列
            model_sequence = [int(x.strip()) for x in raw_ans.split(",")]
        except:
            return False
        
        # 检查长度是否匹配
        if len(model_sequence) != len(self.sequence):
            return False
        
        # 检查每个位置的值是否匹配
        for i in range(len(self.sequence)):
            if model_sequence[i] != self.sequence[i]:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑，用于计算正确的查询响应"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_range = "错误：索引超出范围。"
            error_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_range = "Error: Index out of range."
            error_format = "Error: Invalid format."

        # 优先级：query_diff > query_diff_compare > query_skip_compare
        if "query_diff" in parsed_info:
            # 差分查询：返回 E[i] 的值
            try:
                idx = int(parsed_info["query_diff"].strip())
                # E[i] 的有效范围是 1 到 n-1
                if idx < 1 or idx > len(self.diff_array):
                    return error_range
                # 返回 E[idx]，注意数组索引从 0 开始
                return str(self.diff_array[idx - 1])
            except:
                return error_format

        elif "query_diff_compare" in parsed_info:
            # 差分比较查询：询问 E[i] 和 E[i+1] 是否相等
            try:
                idx = int(parsed_info["query_diff_compare"].strip())
                # 有效范围是 1 到 n-2
                if idx < 1 or idx > len(self.diff_array) - 1:
                    return error_range
                # 比较 E[idx] 和 E[idx+1]
                are_equal = (self.diff_array[idx - 1] == self.diff_array[idx])
                return yes_res if are_equal else no_res
            except:
                return error_format

        elif "query_skip_compare" in parsed_info:
            # 跨位比较查询：询问 S[i] 和 S[i+2] 是否相等
            try:
                idx = int(parsed_info["query_skip_compare"].strip())
                # 有效范围是 1 到 n-2
                if idx < 1 or idx > len(self.sequence) - 2:
                    return error_range
                # 比较 S[idx] 和 S[idx+2]
                # S[i] 和 S[i+2] 相等当且仅当 E[i] XOR E[i+1] = 0
                are_equal = (self.sequence[idx - 1] == self.sequence[idx + 1])
                return yes_res if are_equal else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """将正确答案翻转为错误答案"""
        # 对于二值结果 "0" / "1"，直接翻转
        if correct == "0":
            return "1"
        elif correct == "1":
            return "0"
        
        # 中文处理
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        
        # 英文处理
        elif self.config.language == "en":
            if correct.lower() == "yes":
                return "No"
            elif correct.lower() == "no":
                return "Yes"
        
        # 都不匹配，追加 "_WRONG"
        return str(correct) + "_WRONG"

    def get_all_possible_queries(self):
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        results = []
        n = self._game_info["n"]
        
        # 1. 差分查询 query_diff: 索引范围 1 到 n-1
        for i in range(1, n):
            query_str = f"<query_diff>{i}</query_diff>"
            # 构造 parsed_info 模拟输入
            parsed = {"query_diff": str(i)}
            # 调用核心逻辑获取答案（避免副作用）
            ans = self._cf_core_produce(parsed)
            results.append({"query": query_str, "answer": ans})

        # 2. 差分比较查询 query_diff_compare: 索引范围 1 到 n-2
        for i in range(1, n - 1):
            query_str = f"<query_diff_compare>{i}</query_diff_compare>"
            parsed = {"query_diff_compare": str(i)}
            ans = self._cf_core_produce(parsed)
            results.append({"query": query_str, "answer": ans})

        # 3. 跨位比较查询 query_skip_compare: 索引范围 1 到 n-2
        for i in range(1, n - 1):
            query_str = f"<query_skip_compare>{i}</query_skip_compare>"
            parsed = {"query_skip_compare": str(i)}
            ans = self._cf_core_produce(parsed)
            results.append({"query": query_str, "answer": ans})
            
        return results