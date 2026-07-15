from .base import Game
import re
import random
from typing import List, Dict

class LogicSequenceGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"逻辑序列推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的序列 S[1..{n}]，序列中的元素两两不同，并且定义在一个严格全序集合上（即任意两个元素都可以比较大小）。

同时，我还秘密选择了一种未知的布尔逻辑 L，它属于四种逻辑之一（标记为 A、B、C、D）。这个逻辑用于对任意三个连续位置 (i, i+1, i+2) 进行计算并产生一个比特输出。

设 x1 = 1 若 S[i] < S[i+1]，否则 x1 = 0；x2 = 1 若 S[i+1] < S[i+2]，否则 x2 = 0。四种逻辑定义如下：
- 逻辑 A（AND）：若 x1 == 1 且 x2 == 1，则输出 1，否则输出 0
- 逻辑 B（传递比较）：若 S[i] < S[i+2]，则输出 1，否则输出 0
- 逻辑 C（XOR）：若 x1 != x2，则输出 1，否则输出 0
- 逻辑 D（OR）：若 x1 == 1 或 x2 == 1，则输出 1，否则输出 0

你的目标是：
1. 识别出未知逻辑 L 是哪一种（A、B、C 或 D）
2. 判定序列是否全局严格递增（即对于所有相邻位置，前一个元素都小于后一个元素）

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 二元查询 Q2：询问位置 i 和 i+1 的大小关系（1 <= i <= {n_minus_1}）
   - 返回 1 表示 S[i] < S[i+1]
   - 返回 0 表示 S[i] >= S[i+1]

2. 三元查询 Q3：询问位置 i、i+1、i+2 在未知逻辑 L 下的输出（1 <= i <= {n_minus_2}）
   - 返回 1 或 0，具体取决于未知逻辑 L 的规则
   - 注意：不同的逻辑 L 会对相同的三元组产生不同的输出

每次查询只能包含一个标签。请使用以下 XML 格式：

- 二元查询（例如查询位置 2 和 3）：
<query_q2>2</query_q2>

- 三元查询（例如查询位置 3、4、5）：
<query_q3>3</query_q3>

提交最终答案时，必须说明逻辑类型（A、B、C 或 D）和序列是否全局严格递增（yes 或 no），格式如下：

<answer>logic=A, sorted=yes</answer>
"""

    game_rule_en = """\
Let's play a "Logic Sequence Reasoning" game. Here are the rules:

There is a sequence S[1..{n}] of length {n}, where all elements are distinct and defined on a strictly totally ordered set (i.e., any two elements can be compared).

Additionally, I have secretly chosen an unknown Boolean logic L, which belongs to one of four logic types (labeled as A, B, C, D). This logic is used to compute a bit output for any three consecutive positions (i, i+1, i+2).

Let x1 = 1 if S[i] < S[i+1], else x1 = 0; and x2 = 1 if S[i+1] < S[i+2], else x2 = 0. The four logics are defined as:
- Logic A (AND): output = 1 if x1 == 1 AND x2 == 1, else 0
- Logic B (Transitive Compare): output = 1 if S[i] < S[i+2], else 0
- Logic C (XOR): output = 1 if x1 != x2, else 0
- Logic D (OR): output = 1 if x1 == 1 OR x2 == 1, else 0

Your goals are:
1. Identify which unknown logic L is (A, B, C, or D)
2. Determine whether the sequence is globally strictly increasing (i.e., for all adjacent positions, the previous element is smaller than the next element)

You can repeatedly ask me the following two types of queries (one query per turn), and I will answer truthfully:

1. Binary Query Q2: Ask about the ordering relationship between positions i and i+1 (1 <= i <= {n_minus_1})
   - Returns 1 if S[i] < S[i+1]
   - Returns 0 if S[i] >= S[i+1]

2. Ternary Query Q3: Ask about the output for positions i, i+1, i+2 under unknown logic L (1 <= i <= {n_minus_2})
   - Returns 1 or 0, depending on the rule of unknown logic L
   - Note: Different logics L will produce different outputs for the same triplet

Each query must contain only one tag. Use the following XML format:

- Binary Query (e.g., querying positions 2 and 3):
<query_q2>2</query_q2>

- Ternary Query (e.g., querying positions 3, 4, 5):
<query_q3>3</query_q3>

When submitting the final answer, specify the logic type (A, B, C, or D) and whether the sequence is globally strictly increasing (yes or no), using this format:

<answer>logic=A, sorted=yes</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入“城市干道交通流分析”系统。

我们正在排查一条包含 {n} 个连续路口的主干道。每个路口的拥堵指数序列记为 S[1..{n}]，各路口拥堵指数两两不同，且定义在严格全序集合上。

同时，交通指挥中心采用了一种未知的信号灯联动判定逻辑 L（属于 A、B、C、D 四种模式之一）。该逻辑会提取任意三个连续路口 (i, i+1, i+2) 的拥堵指数，进行计算并产生一个比特的联动信号输出。

设 x1 = 1 若 S[i] < S[i+1]，否则 x1 = 0；x2 = 1 若 S[i+1] < S[i+2]，否则 x2 = 0。四种逻辑定义如下：
- 逻辑 A（AND）：若 x1 == 1 且 x2 == 1，则输出 1，否则输出 0
- 逻辑 B（传递比较）：若 S[i] < S[i+2]，则输出 1，否则输出 0
- 逻辑 C（XOR）：若 x1 != x2，则输出 1，否则输出 0
- 逻辑 D（OR）：若 x1 == 1 或 x2 == 1，则输出 1，否则输出 0

你的目标是：
1. 识别出当前采用的未知联动逻辑 L 是哪一种模式（A、B、C 或 D）。
2. 判定这条干道的拥堵指数是否沿途全局严格递增（即对于所有相邻路口，后一个路口的拥堵指数始终大于前一个）。

你可以反复向系统提出以下两类查询（每次仅限一个查询）：

1. 二元查询 Q2：比对路口 i 和 i+1 的拥堵指数（1 <= i <= {n_minus_1}）
   - 返回 1 表示 路口 i 的拥堵指数 < 路口 i+1 的拥堵指数
   - 返回 0 表示 路口 i 的拥堵指数 >= 路口 i+1 的拥堵指数

2. 三元查询 Q3：查询路口 i、i+1、i+2 在未知联动逻辑 L 下的信号输出（1 <= i <= {n_minus_2}）
   - 返回 1 或 0，具体取决于联动逻辑 L 的规则
   - 注意：不同的逻辑 L 会对相同的三路口组合产生不同的信号输出

每次查询只能包含一个标签。请使用以下 XML 格式：

- 二元查询（例如查询路口 2 和 3）：
<query_q2>2</query_q2>

- 三元查询（例如查询路口 3、4、5）：
<query_q3>3</query_q3>

提交最终诊断时，必须说明联动逻辑模式（A、B、C 或 D）和拥堵指数是否全局严格递增（yes 或 no），格式如下：

<answer>logic=A, sorted=yes</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Arterial Traffic Flow Analysis" system.

We are inspecting a main road containing {n} consecutive intersections. The congestion index sequence for each intersection is denoted as S[1..{n}]. All indices are distinct and defined on a strictly totally ordered set.

Meanwhile, the traffic command center is testing an unknown traffic light linkage logic L (belonging to one of four modes: A, B, C, D). This logic extracts the congestion indices of any three consecutive intersections (i, i+1, i+2) to compute and generate a 1-bit linkage signal output.

Let x1 = 1 if S[i] < S[i+1], else x1 = 0; and x2 = 1 if S[i+1] < S[i+2], else x2 = 0. The four logics are defined as:
- Logic A (AND): output = 1 if x1 == 1 AND x2 == 1, else 0
- Logic B (Transitive Compare): output = 1 if S[i] < S[i+2], else 0
- Logic C (XOR): output = 1 if x1 != x2, else 0
- Logic D (OR): output = 1 if x1 == 1 OR x2 == 1, else 0

Your goals are:
1. Identify which mode the unknown linkage logic L is (A, B, C, or D).
2. Determine whether the congestion index along this arterial road is globally strictly increasing (i.e., for all adjacent intersections, the subsequent intersection's congestion index is always greater than the previous one).

You can repeatedly submit the following two types of queries to the system (one query per turn):

1. Binary Query Q2: Compare the congestion indices of intersections i and i+1 (1 <= i <= {n_minus_1})
   - Returns 1 if intersection i's index < intersection i+1's index
   - Returns 0 if intersection i's index >= intersection i+1's index

2. Ternary Query Q3: Query the signal output for intersections i, i+1, i+2 under the unknown linkage logic L (1 <= i <= {n_minus_2})
   - Returns 1 or 0, depending on the rule of logic L
   - Note: Different logics L will produce different signal outputs for the same triplet of intersections

Each query must contain only one tag. Use the following XML format:

- Binary Query (e.g., querying intersections 2 and 3):
<query_q2>2</query_q2>

- Ternary Query (e.g., querying intersections 3, 4, 5):
<query_q3>3</query_q3>

When submitting the final diagnosis, specify the linkage logic mode (A, B, C, or D) and whether the congestion index is globally strictly increasing (yes or no), using this format:

<answer>logic=A, sorted=yes</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎进入“患者生物标志物序列监控”系统。

我们正在分析一名患者在 {n} 个连续采血时间点上的抗体浓度序列 S[1..{n}]。各个时间点的浓度值两两不同，并且定义在一个严格全序集合上。

同时，我们的医疗诊断系统采用了一种未知的综合症发作预警模型 L（属于 A、B、C、D 四型之一）。该预警模型会对任意三个连续时间点 (i, i+1, i+2) 的数据进行计算并产生一个比特的预警输出。

设 x1 = 1 若 S[i] < S[i+1]，否则 x1 = 0；x2 = 1 若 S[i+1] < S[i+2]，否则 x2 = 0。四种逻辑定义如下：
- 逻辑 A（AND）：若 x1 == 1 且 x2 == 1，则输出 1，否则输出 0
- 逻辑 B（传递比较）：若 S[i] < S[i+2]，则输出 1，否则输出 0
- 逻辑 C（XOR）：若 x1 != x2，则输出 1，否则输出 0
- 逻辑 D（OR）：若 x1 == 1 或 x2 == 1，则输出 1，否则输出 0

你的目标是：
1. 识别出预警模型 L 是哪一型（A、B、C 或 D）。
2. 判定该抗体浓度是否随时间全局严格递增（即对于所有相邻时间点，后一个时间点的浓度始终大于前一个）。

你可以反复向系统提出以下两类化验单查询（每次仅限一个查询）：

1. 二元查询 Q2：对比时间点 i 和 i+1 的抗体浓度（1 <= i <= {n_minus_1}）
   - 返回 1 表示 时间点 i 浓度 < 时间点 i+1 浓度
   - 返回 0 表示 时间点 i 浓度 >= 时间点 i+1 浓度

2. 三元查询 Q3：查询时间点 i、i+1、i+2 在未知预警模型 L 下的输出（1 <= i <= {n_minus_2}）
   - 返回 1 或 0，具体取决于模型 L 的内部机制
   - 注意：不同分型的预警模型会对相同的三点数据序列产生不同的预警输出

每次查询只能包含一个标签。请使用以下 XML 格式：

- 二元查询（例如查询采血点 2 和 3）：
<query_q2>2</query_q2>

- 三元查询（例如查询采血点 3、4、5）：
<query_q3>3</query_q3>

提交最终病理分析结果时，必须说明预警模型分型（A、B、C 或 D）和浓度是否全局严格递增（yes 或 no），格式如下：

<answer>logic=A, sorted=yes</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Patient Biomarker Sequence Monitoring" system.

We are analyzing a patient's antibody concentration sequence S[1..{n}] across {n} consecutive blood sampling time points. All concentration values are distinct and defined on a strictly totally ordered set.

Meanwhile, our medical diagnostic system employs an unknown syndrome onset warning model L (belonging to one of four types: A, B, C, D). This warning model evaluates the data from any three consecutive time points (i, i+1, i+2) to generate a 1-bit warning output.

Let x1 = 1 if S[i] < S[i+1], else x1 = 0; and x2 = 1 if S[i+1] < S[i+2], else x2 = 0. The four logics are defined as:
- Logic A (AND): output = 1 if x1 == 1 AND x2 == 1, else 0
- Logic B (Transitive Compare): output = 1 if S[i] < S[i+2], else 0
- Logic C (XOR): output = 1 if x1 != x2, else 0
- Logic D (OR): output = 1 if x1 == 1 OR x2 == 1, else 0

Your goals are:
1. Identify which type the unknown warning model L is (A, B, C, or D).
2. Determine whether the antibody concentration is globally strictly increasing over time (i.e., for all adjacent time points, the subsequent time point's concentration is always greater than the previous one).

You can repeatedly submit the following two types of lab queries to the system (one query per turn):

1. Binary Query Q2: Compare the antibody concentrations of time points i and i+1 (1 <= i <= {n_minus_1})
   - Returns 1 if time point i's concentration < time point i+1's concentration
   - Returns 0 if time point i's concentration >= time point i+1's concentration

2. Ternary Query Q3: Query the output for time points i, i+1, i+2 under the unknown warning model L (1 <= i <= {n_minus_2})
   - Returns 1 or 0, depending on the internal mechanism of model L
   - Note: Different types of warning models will produce different outputs for the same triplet of data points

Each query must contain only one tag. Use the following XML format:

- Binary Query (e.g., querying sampling points 2 and 3):
<query_q2>2</query_q2>

- Ternary Query (e.g., querying sampling points 3, 4, 5):
<query_q3>3</query_q3>

When submitting the final pathology analysis, specify the warning model type (A, B, C, or D) and whether the concentration is globally strictly increasing (yes or no), using this format:

<answer>logic=A, sorted=yes</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入“自适应学习路径评估”系统。

我们正在审核一套包含 {n} 个连续层级的自适应课程，各层级的实际难度系数序列记为 S[1..{n}]，难度系数两两不同，且定义在严格全序集合上。

同时，教务系统内嵌了一种未知的跳级资格审批机制 L（属于 A、B、C、D 四类之一）。该机制会对任意三个连续层级 (i, i+1, i+2) 的难度进行评估，并产生一个比特的审批输出。

设 x1 = 1 若 S[i] < S[i+1]，否则 x1 = 0；x2 = 1 若 S[i+1] < S[i+2]，否则 x2 = 0。四种逻辑定义如下：
- 逻辑 A（AND）：若 x1 == 1 且 x2 == 1，则输出 1，否则输出 0
- 逻辑 B（传递比较）：若 S[i] < S[i+2]，则输出 1，否则输出 0
- 逻辑 C（XOR）：若 x1 != x2，则输出 1，否则输出 0
- 逻辑 D（OR）：若 x1 == 1 或 x2 == 1，则输出 1，否则输出 0

你的目标是：
1. 识别出未知的审批机制 L 属于哪一类（A、B、C 或 D）。
2. 判定这套课程的难度是否呈现全局严格阶梯式上升（即对于所有相邻层级，后一级的难度始终大于前一级）。

你可以反复向系统提出以下两类试探查询（每次仅限一个查询）：

1. 二元查询 Q2：评估层级 i 和 i+1 的难度大小关系（1 <= i <= {n_minus_1}）
   - 返回 1 表示 层级 i 难度 < 层级 i+1 难度
   - 返回 0 表示 层级 i 难度 >= 层级 i+1 难度

2. 三元查询 Q3：输入连续层级 i、i+1、i+2 以测试审批机制 L 的通过状态（1 <= i <= {n_minus_2}）
   - 返回 1 或 0，具体取决于审批机制 L 的设定
   - 注意：不同类别的审批机制会对相同的三层级组合给出不同的审批结果

每次查询只能包含一个标签。请使用以下 XML 格式：

- 二元查询（例如查询层级 2 和 3）：
<query_q2>2</query_q2>

- 三元查询（例如查询层级 3、4、5）：
<query_q3>3</query_q3>

提交最终评估报告时，必须说明审批机制类别（A、B、C 或 D）和难度是否全局严格递增（yes 或 no），格式如下：

<answer>logic=A, sorted=yes</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Evaluation" system.

We are reviewing an adaptive curriculum containing {n} consecutive levels. The actual difficulty coefficient sequence of each level is denoted as S[1..{n}]. The difficulty coefficients are distinct and defined on a strictly totally ordered set.

At the same time, the academic system has an embedded unknown grade-skipping approval mechanism L (belonging to one of four categories: A, B, C, D). This mechanism evaluates the difficulty of any three consecutive levels (i, i+1, i+2) to generate a 1-bit approval output.

Let x1 = 1 if S[i] < S[i+1], else x1 = 0; and x2 = 1 if S[i+1] < S[i+2], else x2 = 0. The four logics are defined as:
- Logic A (AND): output = 1 if x1 == 1 AND x2 == 1, else 0
- Logic B (Transitive Compare): output = 1 if S[i] < S[i+2], else 0
- Logic C (XOR): output = 1 if x1 != x2, else 0
- Logic D (OR): output = 1 if x1 == 1 OR x2 == 1, else 0

Your goals are:
1. Identify which category the unknown approval mechanism L belongs to (A, B, C, or D).
2. Determine whether the difficulty of this curriculum exhibits a globally strict stepwise escalation (i.e., for all adjacent levels, the subsequent level's difficulty is always greater than the previous one).

You can repeatedly submit the following two types of exploratory queries to the system (one query per turn):

1. Binary Query Q2: Evaluate the difficulty relationship between levels i and i+1 (1 <= i <= {n_minus_1})
   - Returns 1 if level i difficulty < level i+1 difficulty
   - Returns 0 if level i difficulty >= level i+1 difficulty

2. Ternary Query Q3: Input consecutive levels i, i+1, i+2 to test the pass status of the approval mechanism L (1 <= i <= {n_minus_2})
   - Returns 1 or 0, depending on the settings of approval mechanism L
   - Note: Different categories of approval mechanisms will yield different approval results for the same triplet of levels

Each query must contain only one tag. Use the following XML format:

- Binary Query (e.g., querying levels 2 and 3):
<query_q2>2</query_q2>

- Ternary Query (e.g., querying levels 3, 4, 5):
<query_q3>3</query_q3>

When submitting the final evaluation report, specify the approval mechanism category (A, B, C, or D) and whether the difficulty is globally strictly increasing (yes or no), using this format:

<answer>logic=A, sorted=yes</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业流水线热应力检测”系统。

我们正在监测一条具有 {n} 个连续加工工序的生产线，各工序的部件热应力值构成序列 S[1..{n}]。热应力值两两不同，且定义在严格全序集合上。

同时，产线配备了一种未知的废品熔断报警器触发逻辑 L（分为 A、B、C、D 四种型号）。该逻辑会扫描任意三个连续工序 (i, i+1, i+2) 的热应力状况，并产生一个比特的报警器激活输出。

设 x1 = 1 若 S[i] < S[i+1]，否则 x1 = 0；x2 = 1 若 S[i+1] < S[i+2]，否则 x2 = 0。四种逻辑定义如下：
- 逻辑 A（AND）：若 x1 == 1 且 x2 == 1，则输出 1，否则输出 0
- 逻辑 B（传递比较）：若 S[i] < S[i+2]，则输出 1，否则输出 0
- 逻辑 C（XOR）：若 x1 != x2，则输出 1，否则输出 0
- 逻辑 D（OR）：若 x1 == 1 或 x2 == 1，则输出 1，否则输出 0

你的目标是：
1. 识别出未知的报警器触发逻辑 L 是哪一种型号（A、B、C 或 D）。
2. 判定整条生产线的热应力是否沿工序全局严格递增（即对于所有相邻工序，后一道工序的热应力始终大于前一道）。

你可以反复向系统提出以下两类诊断查询（每次仅限一个查询）：

1. 二元查询 Q2：检测相邻工序 i 和 i+1 的热应力大小关系（1 <= i <= {n_minus_1}）
   - 返回 1 表示 工序 i 热应力 < 工序 i+1 热应力
   - 返回 0 表示 工序 i 热应力 >= 工序 i+1 热应力

2. 三元查询 Q3：在连续三个工序 i、i+1、i+2 上测试报警器触发逻辑 L 的状态（1 <= i <= {n_minus_2}）
   - 返回 1 或 0，具体取决于触发逻辑 L 的电路设计
   - 注意：不同型号的报警器对相同的三工序热应力组合会给出不同的触发响应

每次查询只能包含一个标签。请使用以下 XML 格式：

- 二元查询（例如查询工序 2 和 3）：
<query_q2>2</query_q2>

- 三元查询（例如查询工序 3、4、5）：
<query_q3>3</query_q3>

提交最终检修日志时，必须说明报警器逻辑型号（A、B、C 或 D）和热应力是否沿生产线全局严格递增（yes 或 no），格式如下：

<answer>logic=A, sorted=yes</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Pipeline Thermal Stress Inspection" system.

We are monitoring a production line with {n} consecutive processing stages, where the component thermal stress values form a sequence S[1..{n}]. The thermal stress values are distinct and defined on a strictly totally ordered set.

Concurrently, the pipeline is equipped with an unknown defect fuse alarm trigger logic L (categorized into four models: A, B, C, D). This logic scans the thermal stress conditions of any three consecutive stages (i, i+1, i+2) to produce a 1-bit alarm activation output.

Let x1 = 1 if S[i] < S[i+1], else x1 = 0; and x2 = 1 if S[i+1] < S[i+2], else x2 = 0. The four logics are defined as:
- Logic A (AND): output = 1 if x1 == 1 AND x2 == 1, else 0
- Logic B (Transitive Compare): output = 1 if S[i] < S[i+2], else 0
- Logic C (XOR): output = 1 if x1 != x2, else 0
- Logic D (OR): output = 1 if x1 == 1 OR x2 == 1, else 0

Your goals are:
1. Identify which model the unknown alarm trigger logic L belongs to (A, B, C, or D).
2. Determine whether the thermal stress of the entire production line is globally strictly increasing along the stages (i.e., for all adjacent stages, the subsequent stage's thermal stress is always greater than the previous one).

You can repeatedly submit the following two types of diagnostic queries to the system (one query per turn):

1. Binary Query Q2: Inspect the thermal stress relationship between adjacent stages i and i+1 (1 <= i <= {n_minus_1})
   - Returns 1 if stage i thermal stress < stage i+1 thermal stress
   - Returns 0 if stage i thermal stress >= stage i+1 thermal stress

2. Ternary Query Q3: Test the status of the alarm trigger logic L across three consecutive stages i, i+1, i+2 (1 <= i <= {n_minus_2})
   - Returns 1 or 0, depending on the circuit design of trigger logic L
   - Note: Different models of alarms will yield different trigger responses for the same triplet of thermal stress states

Each query must contain only one tag. Use the following XML format:

- Binary Query (e.g., querying stages 2 and 3):
<query_q2>2</query_q2>

- Ternary Query (e.g., querying stages 3, 4, 5):
<query_q3>3</query_q3>

When submitting the final maintenance log, specify the alarm logic model (A, B, C, or D) and whether the thermal stress is globally strictly increasing (yes or no), using this format:

<answer>logic=A, sorted=yes</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入“诉讼证据链效力核查”系统。

我们正在梳理一桩复杂案件中按时间排序的 {n} 份证据文件，其证明力（权重）构成序列 S[1..{n}]。各证据的证明力两两不同，且定义在严格全序集合上。

同时，法庭针对此案采用了一种未知的证据链采信规则 L（分属 A、B、C、D 四种法理逻辑之一）。该规则会对任意三份连续提交的证据 (i, i+1, i+2) 进行综合考量，并产生一个比特的法定效力输出。

设 x1 = 1 若 S[i] < S[i+1]，否则 x1 = 0；x2 = 1 若 S[i+1] < S[i+2]，否则 x2 = 0。四种逻辑定义如下：
- 逻辑 A（AND）：若 x1 == 1 且 x2 == 1，则输出 1，否则输出 0
- 逻辑 B（传递比较）：若 S[i] < S[i+2]，则输出 1，否则输出 0
- 逻辑 C（XOR）：若 x1 != x2，则输出 1，否则输出 0
- 逻辑 D（OR）：若 x1 == 1 或 x2 == 1，则输出 1，否则输出 0

你的目标是：
1. 识别出未知的法庭采信规则 L 是哪一种法理逻辑（A、B、C 或 D）。
2. 判定这套证据链的证明力是否随着提交顺序全局严格递增（即对于所有相邻证据，后一份的证明力始终大于前一份）。

你可以反复向系统提出以下两类案卷查询（每次仅限一个查询）：

1. 二元查询 Q2：质证相邻两份证据 i 和 i+1 的证明力高低（1 <= i <= {n_minus_1}）
   - 返回 1 表示 证据 i 证明力 < 证据 i+1 证明力
   - 返回 0 表示 证据 i 证明力 >= 证据 i+1 证明力

2. 三元查询 Q3：提交连续三份证据 i、i+1、i+2 来探测采信规则 L 的判定结果（1 <= i <= {n_minus_2}）
   - 返回 1 或 0，具体取决于采信规则 L 的司法判定原则
   - 注意：不同类型的采信规则会对相同的三份证据组合给出不同的法庭裁定

每次查询只能包含一个标签。请使用以下 XML 格式：

- 二元查询（例如质证证据 2 和 3）：
<query_q2>2</query_q2>

- 三元查询（例如提交证据 3、4、5）：
<query_q3>3</query_q3>

提交最终法务意见书时，必须说明证据链采信法理逻辑（A、B、C 或 D）和证明力是否全局严格递增（yes 或 no），格式如下：

<answer>logic=A, sorted=yes</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Litigation Evidence Chain Validity Verification" system.

We are reviewing {n} chronologically ordered evidence documents in a complex case, whose probative force (weight) forms a sequence S[1..{n}]. The probative force of each piece of evidence is distinct and defined on a strictly totally ordered set.

Meanwhile, the court applies an unknown evidence chain admissibility rule L (belonging to one of four jurisprudential logics: A, B, C, D) for this case. This rule conducts a comprehensive assessment of any three consecutively submitted pieces of evidence (i, i+1, i+2) to produce a 1-bit legal validity output.

Let x1 = 1 if S[i] < S[i+1], else x1 = 0; and x2 = 1 if S[i+1] < S[i+2], else x2 = 0. The four logics are defined as:
- Logic A (AND): output = 1 if x1 == 1 AND x2 == 1, else 0
- Logic B (Transitive Compare): output = 1 if S[i] < S[i+2], else 0
- Logic C (XOR): output = 1 if x1 != x2, else 0
- Logic D (OR): output = 1 if x1 == 1 OR x2 == 1, else 0

Your goals are:
1. Identify which jurisprudential logic the unknown court admissibility rule L represents (A, B, C, or D).
2. Determine whether the probative force of this evidence chain is globally strictly increasing along the submission order (i.e., for all adjacent evidence, the subsequent document's probative force is always greater than the previous one).

You can repeatedly submit the following two types of docket queries to the system (one query per turn):

1. Binary Query Q2: Cross-examine the probative force ranking between adjacent evidence i and i+1 (1 <= i <= {n_minus_1})
   - Returns 1 if evidence i probative force < evidence i+1 probative force
   - Returns 0 if evidence i probative force >= evidence i+1 probative force

2. Ternary Query Q3: Submit three consecutive pieces of evidence i, i+1, i+2 to probe the adjudication result of admissibility rule L (1 <= i <= {n_minus_2})
   - Returns 1 or 0, depending on the judicial principles of the admissibility rule L
   - Note: Different types of admissibility rules will yield different court rulings for the same triplet of evidence

Each query must contain only one tag. Use the following XML format:

- Binary Query (e.g., cross-examining evidence 2 and 3):
<query_q2>2</query_q2>

- Ternary Query (e.g., submitting evidence 3, 4, 5):
<query_q3>3</query_q3>

When submitting the final legal opinion, specify the jurisprudential logic of admissibility (A, B, C, or D) and whether the probative force is globally strictly increasing (yes or no), using this format:

<answer>logic=A, sorted=yes</answer>
"""

    tags = ["answer", "query_q2", "query_q3"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "sequence": [5, 10, 15, 20, 25],
                "logic": "A",
                "sorted": "yes",
            },
            2: {
                "n": 5,
                "sequence": [5, 15, 10, 25, 30],
                "logic": "B",
                "sorted": "no",
            },
            3: {
                "n": 6,
                "sequence": [8, 12, 6, 18, 14, 22],
                "logic": "C",
                "sorted": "no",
            },
            4: {
                "n": 7,
                "sequence": [3, 5, 7, 9, 11, 15, 20],
                "logic": "D",
                "sorted": "yes",
            },
            5: {
                "n": 8,
                "sequence": [50, 30, 40, 20, 35, 25, 45, 15],
                "logic": "C",
                "sorted": "no",
            },
        },
        "en": {
            1: {
                "n": 5,
                "sequence": [5, 10, 15, 20, 25],
                "logic": "A",
                "sorted": "yes",
            },
            2: {
                "n": 5,
                "sequence": [5, 15, 10, 25, 30],
                "logic": "B",
                "sorted": "no",
            },
            3: {
                "n": 6,
                "sequence": [8, 12, 6, 18, 14, 22],
                "logic": "C",
                "sorted": "no",
            },
            4: {
                "n": 7,
                "sequence": [3, 5, 7, 9, 11, 15, 20],
                "logic": "D",
                "sorted": "yes",
            },
            5: {
                "n": 8,
                "sequence": [50, 30, 40, 20, 35, 25, 45, 15],
                "logic": "C",
                "sorted": "no",
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
        
        self.sequence = cfg["sequence"]
        self.n = cfg["n"]
        self._game_info["n"] = self.n
        self._game_info["n_minus_1"] = self.n - 1
        self._game_info["n_minus_2"] = self.n - 2
        
        self.logic = cfg["logic"]
        
        actually_sorted = all(self.sequence[i] < self.sequence[i+1] for i in range(self.n - 1))
        expected_sorted = cfg["sorted"]
        computed_sorted = "yes" if actually_sorted else "no"
        assert computed_sorted == expected_sorted, (
            f"Inconsistency: sequence {self.sequence} is_sorted={computed_sorted} "
            f"but config says sorted={expected_sorted}"
        )
        self.is_sorted = computed_sorted
        
    def _compute_q2(self, i):
        if i < 1 or i >= self.n:
            return None
        return 1 if self.sequence[i-1] < self.sequence[i] else 0
    
    def _compute_q3(self, i):
        if i < 1 or i > self.n - 2:
            return None
        
        s1, s2, s3 = self.sequence[i-1], self.sequence[i], self.sequence[i+1]
        
        x1 = 1 if s1 < s2 else 0  
        x2 = 1 if s2 < s3 else 0  
        
        if self.logic == "A":
            return 1 if (x1 == 1 and x2 == 1) else 0
        elif self.logic == "B":
            return 1 if s1 < s3 else 0
        elif self.logic == "C":
            return 1 if (x1 != x2) else 0
        elif self.logic == "D":
            return 1 if (x1 == 1 or x2 == 1) else 0
        else:
            raise ValueError(f"Unknown logic type: {self.logic}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "logic" not in ans_dict or "sorted" not in ans_dict:
            return False
        
        if ans_dict["logic"].upper() != self.logic:
            return False
        
        if ans_dict["sorted"].lower() != self.is_sorted:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_format = "错误：查询格式无效。"
            error_range = "错误：查询位置超出范围。"
        else:
            error_format = "Error: Invalid query format."
            error_range = "Error: Query position out of range."

        if "query_q2" in parsed_info:
            try:
                i = int(parsed_info["query_q2"].strip())
                if i < 1 or i >= self.n:
                    return error_range
                result = self._compute_q2(i)
                return str(result)
            except ValueError:
                return error_format

        elif "query_q3" in parsed_info:
            try:
                i = int(parsed_info["query_q3"].strip())
                if i < 1 or i > self.n - 2:
                    return error_range
                result = self._compute_q3(i)
                return str(result)
            except ValueError:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.strip() == "0":
            return "1"
        if correct.strip() == "1":
            return "0"
            
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        if "是" in correct:
            return correct.replace("是", "否")
        elif "否" in correct:
            return correct.replace("否", "是")
        
        lower_c = correct.lower()
        if "yes" in lower_c:
            return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
        elif "no" in lower_c:
            return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        results = []
        
        for i in range(1, self.n):
            query_str = f"<query_q2>{i}</query_q2>"
            ans = str(self._compute_q2(i))
            results.append({"query": query_str, "answer": ans})
            
        for i in range(1, self.n - 1):
            query_str = f"<query_q3>{i}</query_q3>"
            ans = str(self._compute_q3(i))
            results.append({"query": query_str, "answer": ans})
            
        return results