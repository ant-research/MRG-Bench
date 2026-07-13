from .base import Game
import re


class SequenceOrderingGame(Game):

    game_rule_zh = """\
我们来玩一个"序列排序推理"游戏，规则如下：

游戏设定了一个整数序列 X = [x1, x2, …, x{n}]，共 {n} 个元素，序列为：{sequence}

存在一个固定但未知的比较规则 r，它属于以下四种规则之一：
- 规则 A（数值递增）：a 小于等于 b 当且仅当 a 的数值小于等于 b 的数值。
- 规则 B（数值递减）：a 小于等于 b 当且仅当 a 的数值大于等于 b 的数值。
- 规则 C（先偶后奇，组内递增）：所有偶数按升序排在前面，所有奇数按升序排在后面。
- 规则 D（绝对值递增）：先按绝对值升序，绝对值相同时按数值升序。

你的目标是通过询问推断出正确的规则类型，并判断该序列是否按照该规则"整齐"排列（即满足 x1 小于等于 x2 小于等于 ... 小于等于 x{n}）。

你可以反复提出以下三类问题（每次仅限一个问题），我会根据真实的规则如实回答：

1. PairCheck(i, j)：询问位置 i 和位置 j 的元素（i 小于 j）是否满足 xi 小于等于 xj。回答"是"或"否"。
2. AdjCheck(i)：询问位置 i 和位置 i+1 的相邻元素是否满足 xi 小于等于 xi+1。回答"是"或"否"。
3. TripleTrend(i)：询问从位置 i 开始的三个连续元素 (xi, xi+1, xi+2) 的趋势。回答"上升"（xi 小于等于 xi+1 且 xi+1 小于等于 xi+2）、"下降"（xi 大于等于 xi+1 且 xi+1 大于等于 xi+2）或"交错"（其他情况）。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- PairCheck 询问（例如询问位置 1 和 3）：
<query_pair>1,3</query_pair>

- AdjCheck 询问（例如询问位置 2）：
<query_adj>2</query_adj>

- TripleTrend 询问（例如询问位置 1）：
<query_triple>1</query_triple>

提交最终答案时，必须说明规则类型（A、B、C 或 D）和排列状态（整齐 或 不整齐），格式如下：

<answer>rule=A, sorted=整齐</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Ordering Deduction" game. Here are the rules:

There is a fixed integer sequence X = [x1, x2, …, x{n}] with {n} elements: {sequence}

There exists a fixed but unknown comparison rule r, which is one of the following four rules:
- Rule A (Numeric Ascending): a is less than or equal to b if and only if a's numeric value is less than or equal to b's numeric value.
- Rule B (Numeric Descending): a is less than or equal to b if and only if a's numeric value is greater than or equal to b's numeric value.
- Rule C (Even First, Then Odd, Ascending Within Groups): All even numbers in ascending order come first, followed by all odd numbers in ascending order.
- Rule D (Absolute Value Ascending): Sorted by absolute value ascending; when absolute values are equal, sorted by numeric value ascending.

Your goal is to infer the correct rule type through queries and determine whether the sequence is "sorted" under that rule (i.e., satisfying x1 less than or equal to x2 less than or equal to ... less than or equal to x{n}).

You can repeatedly ask the following three types of questions (one per turn), and I will answer truthfully based on the actual rule:

1. PairCheck(i, j): Ask whether elements at positions i and j (where i is less than j) satisfy xi less than or equal to xj. Answer "Yes" or "No".
2. AdjCheck(i): Ask whether adjacent elements at positions i and i+1 satisfy xi less than or equal to xi+1. Answer "Yes" or "No".
3. TripleTrend(i): Ask about the trend of three consecutive elements (xi, xi+1, xi+2) starting from position i. Answer "Ascending" (xi less than or equal to xi+1 and xi+1 less than or equal to xi+2), "Descending" (xi greater than or equal to xi+1 and xi+1 greater than or equal to xi+2), or "Mixed" (otherwise).

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- PairCheck query (e.g., asking about positions 1 and 3):
<query_pair>1,3</query_pair>

- AdjCheck query (e.g., asking about position 2):
<query_adj>2</query_adj>

- TripleTrend query (e.g., asking about position 1):
<query_triple>1</query_triple>

When submitting the final answer, specify the rule type (A, B, C, or D) and sorting status (Sorted or Unsorted), using this format:

<answer>rule=A, sorted=Sorted</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
我们来执行一项"交通枢纽车辆放行序列"的调度推演。

枢纽控制系统生成了一个待放行序列 X = [x1, x2, …, x{n}]，共 {n} 辆车的识别码，序列为：{sequence}

系统内部存在一个固定但未知的优先级排布规则 r，属于以下四种之一：
- 规则 A（常规按序放行）：车辆 a 的优先级小于等于 b 当且仅当 a 的识别码数值小于等于 b。
- 规则 B（逆序放行优先）：车辆 a 的优先级小于等于 b 当且仅当 a 的识别码数值大于等于 b。
- 规则 C（特种车辆优先）：偶数识别码代表特种车辆，需按升序优先放行；奇数识别码为常规车辆，在后方按升序放行。
- 规则 D（权重基准放行）：先按识别码的绝对值升序放行，绝对值相同时按数值本身升序放行。

你的目标是通过系统指令推断出正确的调度规则类型，并判断该序列是否按照该规则"整齐"排布（即满足 x1 小于等于 x2 小于等于 ... 小于等于 x{n}）。

你可以反复调用以下三类检查指令（每次仅限一个指令），系统将根据真实的规则如实反馈：

1. PairCheck(i, j)：询问位置 i 和位置 j 的车辆（i 小于 j）是否满足 xi 优先级小于等于 xj。回答"是"或"否"。
2. AdjCheck(i)：询问位置 i 和位置 i+1 的相邻车辆是否满足 xi 优先级小于等于 xi+1。回答"是"或"否"。
3. TripleTrend(i)：询问从位置 i 开始的三辆连续车辆 (xi, xi+1, xi+2) 的优先级趋势。回答"上升"（xi 小于等于 xi+1 且 xi+1 小于等于 xi+2）、"下降"（xi 大于等于 xi+1 且 xi+1 大于等于 xi+2）或"交错"（其他情况）。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，调度系统将锁定并导致推演失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- PairCheck 询问（例如询问位置 1 和 3）：
<query_pair>1,3</query_pair>

- AdjCheck 询问（例如询问位置 2）：
<query_adj>2</query_adj>

- TripleTrend 询问（例如询问位置 1）：
<query_triple>1</query_triple>

提交最终答案时，必须说明规则类型（A、B、C 或 D）和排布状态（整齐 或 不整齐），格式如下：

<answer>rule=A, sorted=整齐</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Traffic Hub Vehicle Release Sequence" dispatch deduction.

The hub control system has generated a release sequence X = [x1, x2, …, x{n}] with {n} vehicle identification codes: {sequence}

There exists a fixed but unknown priority scheduling rule r, which is one of the following four rules:
- Rule A (Standard Ascending Release): Vehicle a's priority is less than or equal to b if and only if a's numeric code is less than or equal to b.
- Rule B (Reverse Descending Release): Vehicle a's priority is less than or equal to b if and only if a's numeric code is greater than or equal to b.
- Rule C (Special Vehicle Priority): Even codes represent special vehicles and are released first in ascending order; odd codes are regular vehicles, released afterwards in ascending order.
- Rule D (Weight-Based Release): Sorted by the absolute value of the code ascending; when absolute values are equal, sorted by the numeric value ascending.

Your goal is to infer the correct scheduling rule type through system queries and determine whether the sequence is "sorted" under that rule (i.e., satisfying x1 less than or equal to x2 less than or equal to ... less than or equal to x{n}).

You can repeatedly invoke the following three types of query commands (one per turn), and the system will answer truthfully based on the actual rule:

1. PairCheck(i, j): Ask whether vehicles at positions i and j (where i is less than j) satisfy xi priority less than or equal to xj. Answer "Yes" or "No".
2. AdjCheck(i): Ask whether adjacent vehicles at positions i and i+1 satisfy xi priority less than or equal to xi+1. Answer "Yes" or "No".
3. TripleTrend(i): Ask about the priority trend of three consecutive vehicles (xi, xi+1, xi+2) starting from position i. Answer "Ascending" (xi less than or equal to xi+1 and xi+1 less than or equal to xi+2), "Descending" (xi greater than or equal to xi+1 and xi+1 greater than or equal to xi+2), or "Mixed" (otherwise).

When you have enough information, submit your final judgment. If the judgment is wrong or the format is invalid, the scheduling system will be locked.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- PairCheck query (e.g., asking about positions 1 and 3):
<query_pair>1,3</query_pair>

- AdjCheck query (e.g., asking about position 2):
<query_adj>2</query_adj>

- TripleTrend query (e.g., asking about position 1):
<query_triple>1</query_triple>

When submitting the final answer, specify the rule type (A, B, C, or D) and sorting status (Sorted or Unsorted), using this format:

<answer>rule=A, sorted=Sorted</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
我们来执行一项"急诊病患就诊顺序"的医疗分诊推演。

急诊系统录入了一个就诊序列 X = [x1, x2, …, x{n}]，共 {n} 个病患的病情严重度指数，序列为：{sequence}

分诊台存在一个固定但未知的评估规则 r，属于以下四种之一：
- 规则 A（指数递增分诊）：病患 a 的优先级小于等于 b 当且仅当 a 的病情指数数值小于等于 b。
- 规则 B（指数递减分诊）：病患 a 的优先级小于等于 b 当且仅当 a 的病情指数数值大于等于 b。
- 规则 C（特殊体质优先）：偶数指数代表特殊体质患者，按升序优先安排；奇数指数为普通患者，在后方按升序安排。
- 规则 D（偏离度基准分诊）：先按病情指数的绝对值（代表生命体征偏离正常值的程度）升序安排，绝对值相同时按指数本身升序安排。

你的目标是通过系统询问推断出正确的分诊规则类型，并判断该序列是否按照该规则"整齐"排列（即满足 x1 小于等于 x2 小于等于 ... 小于等于 x{n}）。

你可以反复提出以下三类询问指令（每次仅限一个），分诊系统将根据真实的规则如实反馈：

1. PairCheck(i, j)：询问位置 i 和位置 j 的病患（i 小于 j）是否满足 xi 优先级小于等于 xj。回答"是"或"否"。
2. AdjCheck(i)：询问位置 i 和位置 i+1 的相邻病患是否满足 xi 优先级小于等于 xi+1。回答"是"或"否"。
3. TripleTrend(i)：询问从位置 i 开始的三个连续病患 (xi, xi+1, xi+2) 的优先级趋势。回答"上升"（xi 小于等于 xi+1 且 xi+1 小于等于 xi+2）、"下降"（xi 大于等于 xi+1 且 xi+1 大于等于 xi+2）或"交错"（其他情况）。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，将导致推演失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- PairCheck 询问（例如询问位置 1 和 3）：
<query_pair>1,3</query_pair>

- AdjCheck 询问（例如询问位置 2）：
<query_adj>2</query_adj>

- TripleTrend 询问（例如询问位置 1）：
<query_triple>1</query_triple>

提交最终答案时，必须说明规则类型（A、B、C 或 D）和排布状态（整齐 或 不整齐），格式如下：

<answer>rule=A, sorted=整齐</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct an "Emergency Patient Triage Sequence" medical deduction.

The emergency system has recorded a sequence X = [x1, x2, …, x{n}] with {n} patient severity indices: {sequence}

There exists a fixed but unknown evaluation rule r at the triage desk, which is one of the following four rules:
- Rule A (Index Ascending Triage): Patient a's priority is less than or equal to b if and only if a's severity index is less than or equal to b.
- Rule B (Index Descending Triage): Patient a's priority is less than or equal to b if and only if a's severity index is greater than or equal to b.
- Rule C (Special Constitution Priority): Even indices represent patients with special constitutions, arranged first in ascending order; odd indices are regular patients, arranged afterwards in ascending order.
- Rule D (Deviation-Based Triage): Arranged by the absolute value of the index (representing the deviation of vital signs from normal values) ascending; when absolute values are equal, arranged by the numeric index ascending.

Your goal is to infer the correct triage rule type through system queries and determine whether the sequence is "sorted" under that rule (i.e., satisfying x1 less than or equal to x2 less than or equal to ... less than or equal to x{n}).

You can repeatedly invoke the following three types of query commands (one per turn), and the triage system will answer truthfully based on the actual rule:

1. PairCheck(i, j): Ask whether patients at positions i and j (where i is less than j) satisfy xi priority less than or equal to xj. Answer "Yes" or "No".
2. AdjCheck(i): Ask whether adjacent patients at positions i and i+1 satisfy xi priority less than or equal to xi+1. Answer "Yes" or "No".
3. TripleTrend(i): Ask about the priority trend of three consecutive patients (xi, xi+1, xi+2) starting from position i. Answer "Ascending" (xi less than or equal to xi+1 and xi+1 less than or equal to xi+2), "Descending" (xi greater than or equal to xi+1 and xi+1 greater than or equal to xi+2), or "Mixed" (otherwise).

When you have enough information, submit your final judgment. If the judgment is wrong or the format is invalid, the deduction fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- PairCheck query (e.g., asking about positions 1 and 3):
<query_pair>1,3</query_pair>

- AdjCheck query (e.g., asking about position 2):
<query_adj>2</query_adj>

- TripleTrend query (e.g., asking about position 1):
<query_triple>1</query_triple>

When submitting the final answer, specify the rule type (A, B, C, or D) and sorting status (Sorted or Unsorted), using this format:

<answer>rule=A, sorted=Sorted</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
我们来执行一项"考场座位编排序列"的考务审核推演。

教务系统分配了一个座位序列 X = [x1, x2, …, x{n}]，共 {n} 个考生的综合考号，序列为：{sequence}

系统存在一个固定但未知的排序规则 r，属于以下四种之一：
- 规则 A（考号递增排座）：考生 a 的座位次序小于等于 b 当且仅当 a 的考号数值小于等于 b。
- 规则 B（考号递减排座）：考生 a 的座位次序小于等于 b 当且仅当 a 的考号数值大于等于 b。
- 规则 C（理科文科分组排座）：偶数考号代表理科生，按升序优先排在前面；奇数考号为文科生，按升序排在后面。
- 规则 D（绩点偏离度排座）：先按综合考号的绝对值升序排座，绝对值相同时按考号本身升序排座。

你的目标是通过系统指令推断出正确的排序规则类型，并判断该序列是否按照该规则"整齐"排布（即满足 x1 小于等于 x2 小于等于 ... 小于等于 x{n}）。

你可以反复调用以下三类检查指令（每次仅限一个指令），系统将根据真实的规则如实反馈：

1. PairCheck(i, j)：询问位置 i 和位置 j 的考生（i 小于 j）是否满足 xi 座位次序小于等于 xj。回答"是"或"否"。
2. AdjCheck(i)：询问位置 i 和位置 i+1 的相邻考生是否满足 xi 座位次序小于等于 xi+1。回答"是"或"否"。
3. TripleTrend(i)：询问从位置 i 开始的三名连续考生 (xi, xi+1, xi+2) 的座位次序趋势。回答"上升"（xi 小于等于 xi+1 且 xi+1 小于等于 xi+2）、"下降"（xi 大于等于 xi+1 且 xi+1 大于等于 xi+2）或"交错"（其他情况）。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，将导致审核推演失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- PairCheck 询问（例如询问位置 1 和 3）：
<query_pair>1,3</query_pair>

- AdjCheck 询问（例如询问位置 2）：
<query_adj>2</query_adj>

- TripleTrend 询问（例如询问位置 1）：
<query_triple>1</query_triple>

提交最终答案时，必须说明规则类型（A、B、C 或 D）和排布状态（整齐 或 不整齐），格式如下：

<answer>rule=A, sorted=整齐</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct an "Exam Seating Arrangement Sequence" academic review deduction.

The educational administration system has assigned a seating sequence X = [x1, x2, …, x{n}] with {n} comprehensive candidate numbers: {sequence}

There exists a fixed but unknown sorting rule r, which is one of the following four rules:
- Rule A (Ascending Seating): Candidate a's seating order is less than or equal to b if and only if a's candidate number is less than or equal to b.
- Rule B (Descending Seating): Candidate a's seating order is less than or equal to b if and only if a's candidate number is greater than or equal to b.
- Rule C (Science-Arts Grouping Seating): Even candidate numbers represent science students, seated first in ascending order; odd numbers are arts students, seated afterwards in ascending order.
- Rule D (GPA Deviation Seating): Seated by the absolute value of the comprehensive number ascending; when absolute values are equal, seated by the numeric number ascending.

Your goal is to infer the correct sorting rule type through system queries and determine whether the sequence is "sorted" under that rule (i.e., satisfying x1 less than or equal to x2 less than or equal to ... less than or equal to x{n}).

You can repeatedly invoke the following three types of query commands (one per turn), and the system will answer truthfully based on the actual rule:

1. PairCheck(i, j): Ask whether candidates at positions i and j (where i is less than j) satisfy xi seating order less than or equal to xj. Answer "Yes" or "No".
2. AdjCheck(i): Ask whether adjacent candidates at positions i and i+1 satisfy xi seating order less than or equal to xi+1. Answer "Yes" or "No".
3. TripleTrend(i): Ask about the seating order trend of three consecutive candidates (xi, xi+1, xi+2) starting from position i. Answer "Ascending" (xi less than or equal to xi+1 and xi+1 less than or equal to xi+2), "Descending" (xi greater than or equal to xi+1 and xi+1 greater than or equal to xi+2), or "Mixed" (otherwise).

When you have enough information, submit your final judgment. If the judgment is wrong or the format is invalid, the review deduction fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- PairCheck query (e.g., asking about positions 1 and 3):
<query_pair>1,3</query_pair>

- AdjCheck query (e.g., asking about position 2):
<query_adj>2</query_adj>

- TripleTrend query (e.g., asking about position 1):
<query_triple>1</query_triple>

When submitting the final answer, specify the rule type (A, B, C, or D) and sorting status (Sorted or Unsorted), using this format:

<answer>rule=A, sorted=Sorted</answer>
"""

    # ================= 场景 4：工业/制造业 =================
    contextualized_rule_zh_4 = """\
我们来执行一项"精密加工工序流转"的生产线推演。

中控主机生成了一个加工序列 X = [x1, x2, …, x{n}]，共 {n} 个工件的加工作业码，序列为：{sequence}

主机内含一个固定但未知的工序调度规则 r，属于以下四种之一：
- 规则 A（常规递增加工）：工件 a 的加工优先级小于等于 b 当且仅当 a 的作业码数值小于等于 b。
- 规则 B（常规递减加工）：工件 a 的加工优先级小于等于 b 当且仅当 a 的作业码数值大于等于 b。
- 规则 C（核心部件优先）：偶数作业码代表核心部件，按升序优先加工；奇数作业码为外围部件，在后方按升序加工。
- 规则 D（公差基准加工）：先按作业码的绝对值升序加工，绝对值相同时按作业码本身升序加工。

你的目标是通过系统指令推断出正确的工序调度规则类型，并判断该序列是否按照该规则"整齐"排布（即满足 x1 小于等于 x2 小于等于 ... 小于等于 x{n}）。

你可以反复调用以下三类检查指令（每次仅限一个指令），主机将根据真实的规则如实反馈：

1. PairCheck(i, j): 询问位置 i 和位置 j 的工件（i 小于 j）是否满足 xi 加工优先级小于等于 xj。回答"是"或"否"。
2. AdjCheck(i): 询问位置 i 和位置 i+1 的相邻工件是否满足 xi 加工优先级小于等于 xi+1。回答"是"或"否"。
3. TripleTrend(i): 询问从位置 i 开始的三个连续工件 (xi, xi+1, xi+2) 的优先级趋势。回答"上升"（xi 小于等于 xi+1 且 xi+1 小于等于 xi+2）、"下降"（xi 大于等于 xi+1 且 xi+1 大于等于 xi+2）或"交错"（其他情况）。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，将导致推演失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- PairCheck 询问（例如询问位置 1 和 3）：
<query_pair>1,3</query_pair>

- AdjCheck 询问（例如询问位置 2）：
<query_adj>2</query_adj>

- TripleTrend 询问（例如询问位置 1）：
<query_triple>1</query_triple>

提交最终答案时，必须说明规则类型（A、B、C 或 D）和排布状态（整齐 或 不整齐），格式如下：

<answer>rule=A, sorted=整齐</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's conduct a "Precision Machining Process Flow" production line deduction.

The central control host has generated a machining sequence X = [x1, x2, …, x{n}] with {n} workpiece operation codes: {sequence}

The host contains a fixed but unknown process scheduling rule r, which is one of the following four rules:
- Rule A (Standard Ascending Machining): Workpiece a's machining priority is less than or equal to b if and only if a's operation code is less than or equal to b.
- Rule B (Standard Descending Machining): Workpiece a's machining priority is less than or equal to b if and only if a's operation code is greater than or equal to b.
- Rule C (Core Component Priority): Even operation codes represent core components, machined first in ascending order; odd codes are peripheral components, machined afterwards in ascending order.
- Rule D (Tolerance-Based Machining): Machined by the absolute value of the operation code ascending; when absolute values are equal, machined by the numeric code ascending.

Your goal is to infer the correct scheduling rule type through system queries and determine whether the sequence is "sorted" under that rule (i.e., satisfying x1 less than or equal to x2 less than or equal to ... less than or equal to x{n}).

You can repeatedly invoke the following three types of query commands (one per turn), and the host will answer truthfully based on the actual rule:

1. PairCheck(i, j): Ask whether workpieces at positions i and j (where i is less than j) satisfy xi machining priority less than or equal to xj. Answer "Yes" or "No".
2. AdjCheck(i): Ask whether adjacent workpieces at positions i and i+1 satisfy xi machining priority less than or equal to xi+1. Answer "Yes" or "No".
3. TripleTrend(i): Ask about the machining priority trend of three consecutive workpieces (xi, xi+1, xi+2) starting from position i. Answer "Ascending" (xi less than or equal to xi+1 and xi+1 less than or equal to xi+2), "Descending" (xi greater than or equal to xi+1 and xi+1 greater than or equal to xi+2), or "Mixed" (otherwise).

When you have enough information, submit your final judgment. If the judgment is wrong or the format is invalid, the deduction fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- PairCheck query (e.g., asking about positions 1 and 3):
<query_pair>1,3</query_pair>

- AdjCheck query (e.g., asking about position 2):
<query_adj>2</query_adj>

- TripleTrend query (e.g., asking about position 1):
<query_triple>1</query_triple>

When submitting the final answer, specify the rule type (A, B, C, or D) and sorting status (Sorted or Unsorted), using this format:

<answer>rule=A, sorted=Sorted</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
我们来执行一项"案件卷宗归档序列"的法务审查推演。

法院档案系统提取了一个案卷序列 X = [x1, x2, …, x{n}]，共 {n} 个案卷的索引编号，序列为：{sequence}

系统底层设置了一个固定但未知的归档规则 r，属于以下四种之一：
- 规则 A（正向归档）：案卷 a 的归档顺位小于等于 b 当且仅当 a 的编号数值小于等于 b。
- 规则 B（逆向归档）：案卷 a 的归档顺位小于等于 b 当且仅当 a 的编号数值大于等于 b。
- 规则 C（刑事民事分类归档）：偶数编号代表刑事案卷，按升序优先归档；奇数编号为民事案卷，在后方按升序归档。
- 规则 D（涉案金额权重归档）：先按索引编号的绝对值升序归档，绝对值相同时按编号本身升序归档。

你的目标是通过系统指令推断出正确的归档规则类型，并判断该序列是否按照该规则"整齐"排布（即满足 x1 小于等于 x2 小于等于 ... 小于等于 x{n}）。

你可以反复调用以下三类检查指令（每次仅限一个指令），系统将根据真实的规则如实反馈：

1. PairCheck(i, j)：询问位置 i 和位置 j 的案卷（i 小于 j）是否满足 xi 归档顺位小于等于 xj。回答"是"或"否"。
2. AdjCheck(i)：询问位置 i 和位置 i+1 的相邻案卷是否满足 xi 归档顺位小于等于 xi+1。回答"是"或"否"。
3. TripleTrend(i)：询问从位置 i 开始的三个连续案卷 (xi, xi+1, xi+2) 的归档顺位趋势。回答"上升"（xi 小于等于 xi+1 且 xi+1 小于等于 xi+2）、"下降"（xi 大于等于 xi+1 且 xi+1 大于等于 xi+2）或"交错"（其他情况）。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，将导致推演失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- PairCheck 询问（例如询问位置 1 和 3）：
<query_pair>1,3</query_pair>

- AdjCheck 询问（例如询问位置 2）：
<query_adj>2</query_adj>

- TripleTrend 询问（例如询问位置 1）：
<query_triple>1</query_triple>

提交最终答案时，必须说明规则类型（A、B、C 或 D）和排布状态（整齐 或 不整齐），格式如下：

<answer>rule=A, sorted=整齐</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Case File Archiving Sequence" legal review deduction.

The court archive system has extracted a file sequence X = [x1, x2, …, x{n}] with {n} file index numbers: {sequence}

The system underlyingly sets a fixed but unknown archiving rule r, which is one of the following four rules:
- Rule A (Forward Archiving): File a's archiving order is less than or equal to b if and only if a's index number is less than or equal to b.
- Rule B (Reverse Archiving): File a's archiving order is less than or equal to b if and only if a's index number is greater than or equal to b.
- Rule C (Criminal-Civil Classified Archiving): Even index numbers represent criminal files, archived first in ascending order; odd numbers are civil files, archived afterwards in ascending order.
- Rule D (Amount-Based Archiving): Archived by the absolute value of the index number ascending; when absolute values are equal, archived by the numeric number ascending.

Your goal is to infer the correct archiving rule type through system queries and determine whether the sequence is "sorted" under that rule (i.e., satisfying x1 less than or equal to x2 less than or equal to ... less than or equal to x{n}).

You can repeatedly invoke the following three types of query commands (one per turn), and the system will answer truthfully based on the actual rule:

1. PairCheck(i, j): Ask whether files at positions i and j (where i is less than j) satisfy xi archiving order less than or equal to xj. Answer "Yes" or "No".
2. AdjCheck(i): Ask whether adjacent files at positions i and i+1 satisfy xi archiving order less than or equal to xi+1. Answer "Yes" or "No".
3. TripleTrend(i): Ask about the archiving order trend of three consecutive files (xi, xi+1, xi+2) starting from position i. Answer "Ascending" (xi less than or equal to xi+1 and xi+1 less than or equal to xi+2), "Descending" (xi greater than or equal to xi+1 and xi+1 greater than or equal to xi+2), or "Mixed" (otherwise).

When you have enough information, submit your final judgment. If the judgment is wrong or the format is invalid, the deduction fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- PairCheck query (e.g., asking about positions 1 and 3):
<query_pair>1,3</query_pair>

- AdjCheck query (e.g., asking about position 2):
<query_adj>2</query_adj>

- TripleTrend query (e.g., asking about position 1):
<query_triple>1</query_triple>

When submitting the final answer, specify the rule type (A, B, C, or D) and sorting status (Sorted or Unsorted), using this format:

<answer>rule=A, sorted=Sorted</answer>
"""

    tags = ["answer", "query_pair", "query_adj", "query_triple"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "sequence": [1, 3, 5, 7],
                "rule": "A",
                "is_sorted": True,
            },
            2: {
                "n": 5,
                "sequence": [2, 4, 6, 1, 3],
                "rule": "C",
                "is_sorted": True,
            },
            3: {
                "n": 6,
                "sequence": [-3, 2, -5, 1, 4, -1],
                "rule": "D",
                "is_sorted": False,
            },
            4: {
                "n": 7,
                "sequence": [10, 8, 5, 4, 3, 2, 1],
                "rule": "B",
                "is_sorted": True,
            },
            5: {
                "n": 8,
                "sequence": [3, 2, 4, 6, 8, 1, 5, 7],
                "rule": "C",
                "is_sorted": False,
            },
        },
        "en": {
            1: {
                "n": 4,
                "sequence": [1, 3, 5, 7],
                "rule": "A",
                "is_sorted": True,
            },
            2: {
                "n": 5,
                "sequence": [2, 4, 6, 1, 3],
                "rule": "C",
                "is_sorted": True,
            },
            3: {
                "n": 6,
                "sequence": [-3, 2, -5, 1, 4, -1],
                "rule": "D",
                "is_sorted": False,
            },
            4: {
                "n": 7,
                "sequence": [10, 8, 5, 4, 3, 2, 1],
                "rule": "B",
                "is_sorted": True,
            },
            5: {
                "n": 8,
                "sequence": [3, 2, 4, 6, 8, 1, 5, 7],
                "rule": "C",
                "is_sorted": False,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置和内部状态"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数，兼容字符串传入

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["sequence"] = str(cfg["sequence"])
        
        # 内部状态
        self.sequence = cfg["sequence"]
        self.rule = cfg["rule"]
        self.is_sorted = cfg["is_sorted"]

    def _compare_by_rule(self, a, b):
        """根据当前规则比较两个数 a 和 b，返回 a 是否小于等于 b"""
        if self.rule == "A":
            # 数值递增
            return a <= b
        elif self.rule == "B":
            # 数值递减
            return a >= b
        elif self.rule == "C":
            # 先偶后奇，组内递增
            key_a = (0 if a % 2 == 0 else 1, a)
            key_b = (0 if b % 2 == 0 else 1, b)
            return key_a <= key_b
        elif self.rule == "D":
            # 绝对值递增，值作次键
            key_a = (abs(a), a)
            key_b = (abs(b), b)
            return key_a <= key_b
        else:
            raise ValueError(f"Unknown rule: {self.rule}")

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: rule=X, sorted=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip().lower()] = v.strip()
        
        if "rule" not in ans_dict or "sorted" not in ans_dict:
            return False
        
        # 检查规则类型（大小写不敏感）
        if ans_dict["rule"].upper() != self.rule:
            return False
        
        # 检查排序状态（大小写不敏感）
        sorted_str = ans_dict["sorted"].lower()
        if self.config.language == "zh":
            expected_sorted = "整齐" if self.is_sorted else "不整齐"
        else:
            expected_sorted = "sorted" if self.is_sorted else "unsorted"
        
        return sorted_str == expected_sorted

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            asc_res, desc_res, mix_res = "上升", "下降", "交错"
            error_format = "错误：格式无效或位置超出范围。"
            error_range = "错误：位置超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            asc_res, desc_res, mix_res = "Ascending", "Descending", "Mixed"
            error_format = "Error: Invalid format or position out of range."
            error_range = "Error: Position out of range."

        # 处理 PairCheck
        if "query_pair" in parsed_info:
            try:
                raw = parsed_info["query_pair"]
                i, j = [int(x.strip()) for x in raw.split(",")]
                if i < 1 or j < 1 or i > self._game_info["n"] or j > self._game_info["n"] or i >= j:
                    return error_format
                # 位置从1开始，数组从0开始
                a = self.sequence[i - 1]
                b = self.sequence[j - 1]
                return yes_res if self._compare_by_rule(a, b) else no_res
            except:
                return error_format

        # 处理 AdjCheck
        elif "query_adj" in parsed_info:
            try:
                i = int(parsed_info["query_adj"].strip())
                if i < 1 or i >= self._game_info["n"]:
                    return error_range
                a = self.sequence[i - 1]
                b = self.sequence[i]  # i+1 位置
                return yes_res if self._compare_by_rule(a, b) else no_res
            except:
                return error_format

        # 处理 TripleTrend
        elif "query_triple" in parsed_info:
            try:
                i = int(parsed_info["query_triple"].strip())
                if i < 1 or i > self._game_info["n"] - 2:
                    return error_range
                x1 = self.sequence[i - 1]
                x2 = self.sequence[i]
                x3 = self.sequence[i + 1]
                
                # 判断趋势
                cmp1 = self._compare_by_rule(x1, x2)
                cmp2 = self._compare_by_rule(x2, x3)
                cmp3 = self._compare_by_rule(x2, x1)
                cmp4 = self._compare_by_rule(x3, x2)
                
                if cmp1 and cmp2:
                    return asc_res
                elif cmp3 and cmp4:
                    return desc_res
                else:
                    return mix_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，例如 "<query_pair>1,3</query_pair>"
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        n = self._game_info["n"]
        
        # 1. 枚举 PairCheck: 1 <= i < j <= n
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                query_content = f"{i},{j}"
                # 构造符合 parse 解析后的字典格式
                parsed_info = {"query_pair": query_content}
                # 直接调用内部逻辑计算答案，不经过 counterfactual 计数
                answer = self._cf_core_produce(parsed_info)
                results.append({
                    "query": f"<query_pair>{query_content}</query_pair>",
                    "answer": answer
                })
        
        # 2. 枚举 AdjCheck: 1 <= i <= n-1
        for i in range(1, n):
            query_content = str(i)
            parsed_info = {"query_adj": query_content}
            answer = self._cf_core_produce(parsed_info)
            results.append({
                "query": f"<query_adj>{query_content}</query_adj>",
                "answer": answer
            })
            
        # 3. 枚举 TripleTrend: 1 <= i <= n-2
        if n >= 3:
            for i in range(1, n - 1): # range end is exclusive, so n-1 means up to n-2
                query_content = str(i)
                parsed_info = {"query_triple": query_content}
                answer = self._cf_core_produce(parsed_info)
                results.append({
                    "query": f"<query_triple>{query_content}</query_triple>",
                    "answer": answer
                })
        
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案"""
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文替换
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        if correct == "上升":
            return "下降"
        if correct == "下降":
            return "上升"
        if correct == "交错":
            return "上升"
        
        # 英文替换 (忽略大小写，保持原始大小写风格)
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
        if lower_correct == "ascending":
            return "Descending" if correct[0].isupper() else "descending"
        if lower_correct == "descending":
            return "Ascending" if correct[0].isupper() else "ascending"
        if lower_correct == "mixed":
            return "Ascending" if correct[0].isupper() else "ascending"
            
        # 若都不匹配：在字符串末尾追加 "_WRONG"
        return f"{correct}_WRONG"