from .base import Game
import random

class HiddenIndexTransformGame(Game):
    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"隐藏索引变换"的推理游戏，规则如下：

游戏设定了一个已知的整数 D = {D}，以及一个未知数组 W[0..D]，其中每个元素都是非负整数。同时存在一个未知的索引变换函数 f，它从以下四个候选函数中选取其一，且在整个游戏过程中保持不变：
- A: f(i) = i
- B: f(i) = i + 1（若 i + 1 大于 D，则视作越界）
- C: f(i) = D − i
- D: f(i) = 2i（若 2i 大于 D，则视作越界）

你的目标是通过有限次查询，推断出当前使用的变换函数 f 是哪一个，并找到使得 W 数组取得最大值的真实索引 L*，以及该最大值本身。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 值查询：询问索引 i 对应的值。返回 V(i)，其中：
   - 若 f(i) 在 [0..D] 范围内，则 V(i) = W[f(i)]
   - 若 f(i) 越界，则 V(i) = 0

2. 比较查询：询问索引 i 和 j 对应值的大小关系。返回 ">"、"=" 或 "<"，表示 V(i) 与 V(j) 的比较结果。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 值查询（例如查询索引 3）：
<query_value>3</query_value>

- 比较查询（例如比较索引 2 和 5）：
<query_compare>2,5</query_compare>

提交最终答案时，必须说明变换函数类型（A、B、C 或 D）、真实索引 L* 以及对应的最大值，格式如下：

<answer>func=A, index=3, max_value=42</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Index Transform" deduction game. Here are the rules:

The game has a known integer D = {D}, and an unknown array W[0..D] where each element is a non-negative integer. There also exists an unknown index transformation function f, selected from one of the following four candidates and remains fixed throughout the game:
- A: f(i) = i
- B: f(i) = i + 1 (out of bounds if i + 1 is greater than D)
- C: f(i) = D − i
- D: f(i) = 2i (out of bounds if 2i is greater than D)

Your goal is to determine which transformation function f is being used through a finite number of queries, and find the true index L* that achieves the maximum value in array W, along with that maximum value itself.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully based on the actual setup:

1. Value Query: Ask for the value corresponding to index i. Returns V(i), where:
   - If f(i) is within [0..D], then V(i) = W[f(i)]
   - If f(i) is out of bounds, then V(i) = 0

2. Comparison Query: Ask for the comparison between values at indices i and j. Returns ">", "=", or "<", representing the comparison result between V(i) and V(j).

When you have gathered sufficient information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying index 3):
<query_value>3</query_value>

- Comparison Query (e.g., comparing indices 2 and 5):
<query_compare>2,5</query_compare>

When submitting the final answer, specify the transformation function type (A, B, C, or D), the true index L*, and the corresponding maximum value, using this format:

<answer>func=A, index=3, max_value=42</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来处理一起交通监测系统的"隐蔽数据偏移"故障排查任务，规则如下：

智能交通系统设定了编号为 0 到 D（已知 D = {D}）的若干个监测点。系统内部有一个未知数组 W[0..D]，记录着每个真实监测点的实际车流量（非负整数）。由于系统升级故障，当前数据显示所使用的传感器索引发生了未知的映射变换 f。该变换函数必然是以下四种之一，且在排查期间保持不变：
- A: 正常映射，f(i) = i
- B: 传感器向后错位，f(i) = i + 1（若 i + 1 大于 D，则视作断联越界）
- C: 线路反向连接，f(i) = D − i
- D: 间隔站错乱连接，f(i) = 2i（若 2i 大于 D，则视作断联越界）

你的目标是通过有限次查询，诊断出当前系统使用的变换函数 f，并找出实际车流量最大的真实监测点索引 L*，以及该最大车流量数值。

你可以反复向我提出以下两类指令（每次仅限一个），我会根据交通系统的真实情况如实反馈：

1. 流量查询：询问系统显示索引 i 处的车流量。返回 V(i)，其中：
   - 若 f(i) 在 [0..D] 范围内，则 V(i) = W[f(i)]
   - 若 f(i) 越界断联，则 V(i) = 0

2. 比较查询：对比系统显示索引 i 和 j 处的车流量大小关系。返回 ">"、"=" 或 "<"，表示 V(i) 与 V(j) 的比较结果。

当你收集到足够的数据后，请提交最终的故障排查报告。若结论错误或格式不符，任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 流量查询（例如查询显示索引 3）：
<query_value>3</query_value>

- 比较查询（例如比较显示索引 2 和 5）：
<query_compare>2,5</query_compare>

提交最终报告时，必须说明故障变换函数类型（A、B、C 或 D）、真实监测点索引 L* 以及对应的最大车流量，格式如下：

<answer>func=A, index=3, max_value=42</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a troubleshooting task for a "Hidden Data Shift" in the traffic monitoring system. Here are the rules:

The intelligent traffic system has monitoring points numbered from 0 to D (known D = {D}). There is an internal unknown array W[0..D] recording the actual traffic flow (non-negative integers) at each true monitoring point. Due to a system upgrade malfunction, the current data display uses an unknown index transformation function f for the sensors. This function is strictly one of the following four and remains fixed during troubleshooting:
- A: Normal mapping, f(i) = i
- B: Sensor shifted backward, f(i) = i + 1 (out of bounds if i + 1 is greater than D)
- C: Reverse line connection, f(i) = D − i
- D: Alternating station misconnection, f(i) = 2i (out of bounds if 2i is greater than D)

Your goal is to diagnose which transformation function f is currently applied through a finite number of queries, and pinpoint the true monitoring point index L* that has the maximum actual traffic flow, along with that maximum flow value.

You can repeatedly issue the following two types of queries to me (one per turn), and I will feedback truthfully based on the actual system status:

1. Flow Query: Ask for the traffic flow at the displayed index i. Returns V(i), where:
   - If f(i) is within [0..D], then V(i) = W[f(i)]
   - If f(i) is out of bounds/disconnected, then V(i) = 0

2. Comparison Query: Ask for the comparison of traffic flows between displayed indices i and j. Returns ">", "=", or "<", representing the comparison result between V(i) and V(j).

When you have gathered sufficient data, submit your final troubleshooting report. If the conclusion is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Flow Query (e.g., querying displayed index 3):
<query_value>3</query_value>

- Comparison Query (e.g., comparing displayed indices 2 and 5):
<query_compare>2,5</query_compare>

When submitting the final report, specify the malfunction transformation function type (A, B, C, or D), the true monitoring point index L*, and the corresponding maximum traffic flow, using this format:

<answer>func=A, index=3, max_value=42</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项医疗药物代谢监测的"隐藏通道映射"分析，规则如下：

临床测试设定了 D = {D} 个采样时间点。系统内部有一个未知数组 W[0..D]，记录着每个真实时间点的实际药物浓度（非负整数）。由于设备接口发生混淆，当前仪器显示的记录通道受到未知映射函数 f 的影响。该函数必然是以下四种之一，且在分析期间保持不变：
- A: 正常记录通道，f(i) = i
- B: 通道延迟一期，f(i) = i + 1（若 i + 1 大于 D，则视作无效越界）
- C: 通道逆序记录，f(i) = D − i
- D: 通道双倍间隔，f(i) = 2i（若 2i 大于 D，则视作无效越界）

你的目标是通过有限次查询，诊断出当前设备使用的映射函数 f，并找出实际药物浓度最高的真实时间点索引 L*，以及该最高浓度数值。

你可以反复向我提出以下两类调阅申请（每次仅限一个），我会根据设备真实数据如实反馈：

1. 浓度查询：检测仪器记录索引 i 处的药物浓度。返回 V(i)，其中：
   - 若 f(i) 在 [0..D] 范围内，则 V(i) = W[f(i)]
   - 若 f(i) 无效越界，则 V(i) = 0

2. 比较查询：比对仪器记录索引 i 和 j 处的浓度大小关系。返回 ">"、"=" 或 "<"，表示 V(i) 与 V(j) 的比对结果。

当你收集到足够的临床数据后，请提交最终的分析结论。若结论错误或格式不符，分析将宣告失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 浓度查询（例如检测记录索引 3）：
<query_value>3</query_value>

- 比较查询（例如比对记录索引 2 和 5）：
<query_compare>2,5</query_compare>

提交最终结论时，必须说明接口映射函数类型（A、B、C 或 D）、真实时间点索引 L* 以及对应的最高浓度，格式如下：

<answer>func=A, index=3, max_value=42</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Hidden Channel Mapping" analysis for medical drug metabolism monitoring. Here are the rules:

The clinical test has D = {D} sampling time points. There is an internal unknown array W[0..D] recording the actual drug concentration (non-negative integers) at each true time point. Due to device interface confusion, the current recording channels displayed by the instrument are affected by an unknown mapping function f. This function is strictly one of the following four and remains fixed during the analysis:
- A: Normal recording channel, f(i) = i
- B: Channel delayed by one phase, f(i) = i + 1 (out of bounds/invalid if i + 1 is greater than D)
- C: Channel recorded in reverse, f(i) = D − i
- D: Channel doubled in interval, f(i) = 2i (out of bounds/invalid if 2i is greater than D)

Your goal is to diagnose which mapping function f is currently used by the device through a finite number of queries, and pinpoint the true time point index L* that has the highest actual drug concentration, along with that highest concentration value.

You can repeatedly submit the following two types of queries to me (one per turn), and I will feedback truthfully based on the actual device data:

1. Concentration Query: Test the drug concentration at the recorded index i. Returns V(i), where:
   - If f(i) is within [0..D], then V(i) = W[f(i)]
   - If f(i) is out of bounds/invalid, then V(i) = 0

2. Comparison Query: Compare the concentrations at recorded indices i and j. Returns ">", "=", or "<", representing the comparison result between V(i) and V(j).

When you have gathered sufficient clinical data, submit your final analysis conclusion. If the conclusion is wrong or the format is invalid, the analysis fails.

Each query must contain only one tag. Use the following XML format:

- Concentration Query (e.g., testing recorded index 3):
<query_value>3</query_value>

- Comparison Query (e.g., comparing recorded indices 2 and 5):
<query_compare>2,5</query_compare>

When submitting the final conclusion, specify the interface mapping function type (A, B, C, or D), the true time point index L*, and the corresponding highest concentration, using this format:

<answer>func=A, index=3, max_value=42</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项自适应学习系统的"隐藏题号映射"评估，规则如下：

自适应题库包含 D = {D} 个难度级别的核心考题。系统内部有一个未知数组 W[0..D]，记录着每个真实难度级别题目对应的核心素养标准分（非负整数）。由于组卷算法发生偏移，当前系统呈现给学生的题号受到了未知映射函数 f 的影响。该函数必然是以下四种之一，且在评估期间保持不变：
- A: 原序出题，f(i) = i
- B: 难度递进移位，f(i) = i + 1（若 i + 1 大于 D，则视作超纲越界）
- C: 倒序出题，f(i) = D − i
- D: 跳级出题，f(i) = 2i（若 2i 大于 D，则视作超纲越界）

你的目标是通过有限次查询，评估出当前组卷算法使用的映射函数 f，并找出核心素养标准分最高的真实难度级别索引 L*，以及该最高分数值。

你可以反复向我提出以下两类试探查询（每次仅限一个），我会根据题库的真实标准如实反馈：

1. 抽题查询：查询系统显示题号 i 处的素养分。返回 V(i)，其中：
   - 若 f(i) 在 [0..D] 范围内，则 V(i) = W[f(i)]
   - 若 f(i) 超纲越界，则 V(i) = 0

2. 比较查询：比对系统显示题号 i 和 j 处的素养分高低。返回 ">"、"=" 或 "<"，表示 V(i) 与 V(j) 的比对结果。

当你收集到足够的测评数据后，请提交最终的系统评估报告。若结论错误或格式不符，评估将宣告失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 抽题查询（例如查询显示题号 3）：
<query_value>3</query_value>

- 比较查询（例如比对显示题号 2 和 5）：
<query_compare>2,5</query_compare>

提交最终报告时，必须说明组卷映射函数类型（A、B、C 或 D）、真实难度级别索引 L* 以及对应的最高素养分，格式如下：

<answer>func=A, index=3, max_value=42</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Hidden Question Mapping" evaluation for an adaptive learning system. Here are the rules:

The adaptive question bank contains D = {D} difficulty levels of core questions. There is an internal unknown array W[0..D] recording the standard core competency score (non-negative integers) corresponding to each true difficulty level. Due to a shift in the test generation algorithm, the question numbers presented to students are affected by an unknown mapping function f. This function is strictly one of the following four and remains fixed during the evaluation:
- A: Original sequence, f(i) = i
- B: Progressive difficulty shift, f(i) = i + 1 (out of syllabus bounds if i + 1 is greater than D)
- C: Reverse sequence, f(i) = D − i
- D: Skipped level generation, f(i) = 2i (out of syllabus bounds if 2i is greater than D)

Your goal is to evaluate which mapping function f is currently used by the test generation algorithm through a finite number of queries, and pinpoint the true difficulty level index L* that has the highest standard competency score, along with that highest score value.

You can repeatedly submit the following two types of probing queries to me (one per turn), and I will feedback truthfully based on the actual question bank standards:

1. Draw Query: Ask for the competency score at the displayed question number i. Returns V(i), where:
   - If f(i) is within [0..D], then V(i) = W[f(i)]
   - If f(i) is out of bounds, then V(i) = 0

2. Comparison Query: Compare the competency scores at displayed question numbers i and j. Returns ">", "=", or "<", representing the comparison result between V(i) and V(j).

When you have gathered sufficient assessment data, submit your final system evaluation report. If the conclusion is wrong or the format is invalid, the evaluation fails.

Each query must contain only one tag. Use the following XML format:

- Draw Query (e.g., querying displayed question number 3):
<query_value>3</query_value>

- Comparison Query (e.g., comparing displayed question numbers 2 and 5):
<query_compare>2,5</query_compare>

When submitting the final report, specify the test generation mapping function type (A, B, C, or D), the true difficulty level index L*, and the corresponding highest competency score, using this format:

<answer>func=A, index=3, max_value=42</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来执行一项自动化流水线的"隐蔽工序置换"故障诊断，规则如下：

生产流水线共有 D = {D} 道标准加工工序。控制系统内部有一个未知数组 W[0..D]，记录着每道真实工序所能带来的实际良品率增益（非负整数）。由于PLC控制程序更新失误，当前流水线执行的工序顺序受到了未知置换函数 f 的影响。该函数必然是以下四种之一，且在诊断期间保持不变：
- A: 顺序加工，f(i) = i
- B: 错位加工，f(i) = i + 1（若 i + 1 大于 D，则视作空载越界）
- C: 逆向加工，f(i) = D − i
- D: 跨越式加工，f(i) = 2i（若 2i 大于 D，则视作空载越界）

你的目标是通过有限次查验，诊断出当前的工序置换函数 f，并找出实际良品率增益最高的核心标准工序索引 L*，以及该最高增益数值。

你可以反复向我提出以下两类查验指令（每次仅限一个），我会根据生产线的真实状况如实反馈：

1. 节点查验：检查当前执行程序中节点 i 的良品率增益。返回 V(i)，其中：
   - 若 f(i) 在 [0..D] 范围内，则 V(i) = W[f(i)]
   - 若 f(i) 空载越界，则 V(i) = 0

2. 比较查验：对比当前执行程序中节点 i 和 j 的增益大小关系。返回 ">"、"=" 或 "<"，表示 V(i) 与 V(j) 的对比结果。

当你收集到足够的测试数据后，请提交最终的故障诊断报告。若诊断错误或格式不符，排查将宣告失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 节点查验（例如检查程序节点 3）：
<query_value>3</query_value>

- 比较查验（例如对比程序节点 2 和 5）：
<query_compare>2,5</query_compare>

提交最终报告时，必须说明工序置换函数类型（A、B、C 或 D）、核心标准工序索引 L* 以及对应的最高良品率增益，格式如下：

<answer>func=A, index=3, max_value=42</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's execute a fault diagnosis for a "Hidden Process Permutation" on an automated assembly line. Here are the rules:

The production line has D = {D} standard processing steps. The control system has an internal unknown array W[0..D] recording the actual yield rate gain (non-negative integers) provided by each true standard step. Due to a PLC control program update error, the current execution order is affected by an unknown permutation function f. This function is strictly one of the following four and remains fixed during diagnosis:
- A: Sequential processing, f(i) = i
- B: Misaligned processing, f(i) = i + 1 (empty load/out of bounds if i + 1 is greater than D)
- C: Reverse processing, f(i) = D − i
- D: Leapfrog processing, f(i) = 2i (empty load/out of bounds if 2i is greater than D)

Your goal is to diagnose which permutation function f is currently applied through a finite number of inspections, and pinpoint the core standard step index L* that yields the highest actual gain, along with that highest gain value.

You can repeatedly issue the following two types of inspection commands to me (one per turn), and I will feedback truthfully based on the actual production line status:

1. Node Inspection: Check the yield rate gain at the currently executed program node i. Returns V(i), where:
   - If f(i) is within [0..D], then V(i) = W[f(i)]
   - If f(i) is out of bounds (empty load), then V(i) = 0

2. Comparison Inspection: Compare the yield rate gains between program nodes i and j. Returns ">", "=", or "<", representing the comparison result between V(i) and V(j).

When you have gathered sufficient test data, submit your final fault diagnosis report. If the diagnosis is wrong or the format is invalid, the troubleshooting fails.

Each query must contain only one tag. Use the following XML format:

- Node Inspection (e.g., checking program node 3):
<query_value>3</query_value>

- Comparison Inspection (e.g., comparing program nodes 2 and 5):
<query_compare>2,5</query_compare>

When submitting the final report, specify the process permutation function type (A, B, C, or D), the core standard step index L*, and the corresponding highest yield rate gain, using this format:

<answer>func=A, index=3, max_value=42</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来开展一项司法卷宗档案的"隐藏重组映射"审查，规则如下：

案卷档案室设有 D = {D} 个按年份排列的标准档案柜。档案系统内部有一个未知数组 W[0..D]，记录着每个标准柜中存放的关键证据机密指数（非负整数）。由于近期档案数字化系统的重组，当前调阅编号受到了未知映射规则 f 的影响。该规则必然是以下四种之一，且在审查期间保持不变：
- A: 原位归档，f(i) = i
- B: 顺延一柜归档，f(i) = i + 1（若 i + 1 大于 D，则视作空柜越界）
- C: 倒序归档，f(i) = D − i
- D: 偶数跳跃归档，f(i) = 2i（若 2i 大于 D，则视作空柜越界）

你的目标是通过有限次调阅查询，推断出当前档案系统使用的重组映射规则 f，并找出实际机密指数最高的标准档案柜原索引 L*，以及该最高机密指数。

你可以反复向我提出以下两类调阅申请（每次仅限一个），我会根据档案库的真实状况如实反馈：

1. 查阅申请：查询当前调阅编号为 i 的柜子的机密指数。返回 V(i)，其中：
   - 若 f(i) 在 [0..D] 范围内，则 V(i) = W[f(i)]
   - 若 f(i) 空柜越界，则 V(i) = 0

2. 比较申请：比对当前调阅编号 i 和 j 的柜子机密指数大小关系。返回 ">"、"=" 或 "<"，表示 V(i) 与 V(j) 的比对结果。

当你收集到足够的调查线索后，请提交最终的审查鉴定意见。若结论错误或格式不符，审查将宣告失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 查阅申请（例如查询调阅编号 3）：
<query_value>3</query_value>

- 比较申请（例如比对调阅编号 2 和 5）：
<query_compare>2,5</query_compare>

提交最终鉴定意见时，必须说明档案重组映射规则类型（A、B、C 或 D）、标准档案柜原索引 L* 以及对应的最高机密指数，格式如下：

<answer>func=A, index=3, max_value=42</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Hidden Reorganization Mapping" review for judicial case archives. Here are the rules:

The case archive room has D = {D} standard filing cabinets arranged by year. The archive system has an internal unknown array W[0..D] recording the confidentiality index (non-negative integers) of key evidence stored in each standard cabinet. Due to a recent reorganization of the digital archive system, the current access numbers are affected by an unknown mapping rule f. This rule is strictly one of the following four and remains fixed during the review:
- A: Original archiving, f(i) = i
- B: Shifted archiving by one cabinet, f(i) = i + 1 (empty cabinet/out of bounds if i + 1 is greater than D)
- C: Reverse archiving, f(i) = D − i
- D: Even-jump archiving, f(i) = 2i (empty cabinet/out of bounds if 2i is greater than D)

Your goal is to infer which reorganization mapping rule f is currently used by the system through a finite number of access queries, and pinpoint the original standard cabinet index L* that holds the highest actual confidentiality index, along with that highest index value.

You can repeatedly submit the following two types of access requests to me (one per turn), and I will feedback truthfully based on the actual status of the archive:

1. Access Request: Query the confidentiality index of the cabinet with current access number i. Returns V(i), where:
   - If f(i) is within [0..D], then V(i) = W[f(i)]
   - If f(i) is out of bounds (empty cabinet), then V(i) = 0

2. Comparison Request: Compare the confidentiality indices of cabinets with current access numbers i and j. Returns ">", "=", or "<", representing the comparison result between V(i) and V(j).

When you have gathered sufficient investigative clues, submit your final review evaluation. If the conclusion is wrong or the format is invalid, the review fails.

Each query must contain only one tag. Use the following XML format:

- Access Request (e.g., querying access number 3):
<query_value>3</query_value>

- Comparison Request (e.g., comparing access numbers 2 and 5):
<query_compare>2,5</query_compare>

When submitting the final evaluation, specify the archive reorganization mapping rule type (A, B, C, or D), the original standard cabinet index L*, and the corresponding highest confidentiality index, using this format:

<answer>func=A, index=3, max_value=42</answer>
"""

    tags = ["answer", "query_value", "query_compare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "D": 5,
                "W": [5, 10, 15, 20, 25, 30],
                "func": "A",
            },
            2: {
                "D": 6,
                "W": [8, 12, 7, 15, 9, 11, 6],
                "func": "B",
            },
            3: {
                "D": 7,
                "W": [3, 8, 12, 20, 15, 10, 5, 2],
                "func": "C",
            },
            4: {
                "D": 8,
                "W": [10, 5, 18, 8, 22, 7, 12, 9, 15],
                "func": "D",
            },
            5: {
                "D": 10,
                "W": [7, 14, 9, 22, 11, 28, 13, 8, 19, 5, 25],
                "func": "D",
            },
        },
        "en": {
            1: {
                "D": 5,
                "W": [5, 10, 15, 20, 25, 30],
                "func": "A",
            },
            2: {
                "D": 6,
                "W": [8, 12, 7, 15, 9, 11, 6],
                "func": "B",
            },
            3: {
                "D": 7,
                "W": [3, 8, 12, 20, 15, 10, 5, 2],
                "func": "C",
            },
            4: {
                "D": 8,
                "W": [10, 5, 18, 8, 22, 7, 12, 9, 15],
                "func": "D",
            },
            5: {
                "D": 10,
                "W": [7, 14, 9, 22, 11, 28, 13, 8, 19, 5, 25],
                "func": "D",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.D = cfg["D"]
        self.W = cfg["W"]
        self.func_type = cfg["func"]
        
        self._game_info["D"] = self.D

        self.transform_funcs = {
            "A": lambda i: i if i <= self.D else None,
            "B": lambda i: (i + 1) if (i + 1 <= self.D) else None,
            "C": lambda i: (self.D - i) if (self.D - i >= 0 and self.D - i <= self.D) else None,
            "D": lambda i: (2 * i) if (2 * i <= self.D) else None,
        }

        self.f = self.transform_funcs[self.func_type]

        self.true_max_index = self.W.index(max(self.W))
        self.true_max_value = self.W[self.true_max_index]

    def _compute_V(self, i):
        if i < 0 or i > self.D:
            return 0
        
        transformed_index = self.f(i)
        if transformed_index is None or transformed_index < 0 or transformed_index > self.D:
            return 0
        
        return self.W[transformed_index]

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "func" not in ans_dict or "index" not in ans_dict or "max_value" not in ans_dict:
            return False
        
        if ans_dict["func"].upper() != self.func_type:
            return False
        
        try:
            model_index = int(ans_dict["index"])
        except:
            return False
        
        if model_index != self.true_max_index:
            return False
        
        try:
            model_max_value = int(ans_dict["max_value"])
        except:
            return False
        
        if model_max_value != self.true_max_value:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "query_value" in parsed_info:
            try:
                i = int(parsed_info["query_value"].strip())
                if i < 0 or i > self.D:
                    return "Error: Index out of range." if self.config.language == "en" else "错误：索引超出范围。"
                
                value = self._compute_V(i)
                return str(value)
            except:
                return "Error: Invalid index format." if self.config.language == "en" else "错误：索引格式无效。"
        
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                
                i, j = int(parts[0]), int(parts[1])
                
                if i < 0 or i > self.D or j < 0 or j > self.D:
                    return "Error: Index out of range." if self.config.language == "en" else "错误：索引超出范围。"
                
                v_i = self._compute_V(i)
                v_j = self._compute_V(j)
                
                if v_i > v_j:
                    return ">"
                elif v_i < v_j:
                    return "<"
                else:
                    return "="
            except:
                return "Error: Invalid comparison format." if self.config.language == "en" else "错误：比较格式无效。"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.lstrip('-').isdigit():
            val = int(correct)
            return str(val + 1)

        if correct == ">":
            return "<"
        if correct == "<":
            return ">"
        if correct == "=":
            return ">"

        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            if "no" in lower_correct:
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []

        for i in range(self.D + 1):
            val = self._compute_V(i)
            ans = str(val)
            queries.append({
                "query": f"<query_value>{i}</query_value>",
                "answer": ans
            })

        for i in range(self.D + 1):
            for j in range(self.D + 1):
                if i == j:
                    continue
                v_i = self._compute_V(i)
                v_j = self._compute_V(j)

                if v_i > v_j:
                    ans = ">"
                elif v_i < v_j:
                    ans = "<"
                else:
                    ans = "="

                queries.append({
                    "query": f"<query_compare>{i},{j}</query_compare>",
                    "answer": ans
                })
        
        return queries