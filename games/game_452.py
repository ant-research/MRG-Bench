# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   元素存在性：某个特定元素是否存在于集合中
# ============================================================

from .base import Game
import re

class PeriodicOracleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"周期性诚实问答"的推理游戏，规则如下：

游戏设定了一个宇宙 U = {{1, 2, ..., 12}}，以及一个隐藏的子集 S，其中 S 的大小在 3 到 9 之间。同时，我按照一个隐藏的周期模式 P 来回答你的问题。模式 P 是一个长度为 L（2 到 5 之间）的 0-1 序列，其中 1 表示"诚实回答"，0 表示"相反回答"。在第 i 轮提问时，我会根据 P 的第 ((i-1) mod L) + 1 位来决定回答方式。

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据当前轮次对应的周期位来如实或相反地回答：

1. 成员查询：询问某个元素 e（1 到 12 之间）是否在集合 S 中。
2. 相等查询：询问两个数 a 和 b 是否相等（仅当 a 等于 b 时为真）。
3. 大小查询：询问宇宙 U 的大小是否等于某个数 k（仅当 k 等于 12 时为真）。

你的目标是：
1. 推断元素 7 是否在集合 S 中。
2. 识别周期模式 P（允许与真实模式存在循环位移）。
3. 给出至少两次成员查询的对齐说明，指出它们位于"诚实位"，并说明这些命题在该位上的真值。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 成员查询（例如询问元素 5）：
<query_in>5</query_in>

- 相等查询（例如询问 3 和 3 是否相等）：
<query_equal>3,3</query_equal>

- 大小查询（例如询问宇宙大小是否为 12）：
<query_size>12</query_size>

提交最终答案时，必须包含三个部分：
1. 元素 7 的存在性（EXISTS 或 NOT_EXISTS）
2. 周期模式（一个长度 2 到 5 的 01 串）
3. 对齐说明（至少引用两次成员查询的轮次，说明它们位于诚实位及对应真值）

格式如下：
<answer>
declaration=EXISTS
pattern=101
alignment=第3轮IN 7为诚实位真值为真，第6轮IN 5为诚实位真值为假
</answer>

或者：
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    game_rule_en = """\
Let's play a "Periodic Honest Oracle" deduction game. Here are the rules:

The game has a universe U = {{1, 2, ..., 12}} and a hidden subset S, where the size of S is between 3 and 9. Additionally, I answer your questions according to a hidden periodic pattern P. Pattern P is a binary sequence of length L (between 2 and 5), where 1 means "honest answer" and 0 means "opposite answer". In round i, I will decide how to answer based on the ((i-1) mod L) + 1-th bit of P.

You can repeatedly ask me three types of questions (one per turn), and I will answer honestly or oppositely based on the current round's corresponding position in the pattern:

1. Membership Query: Ask if an element e (between 1 and 12) is in set S.
2. Equality Query: Ask if two numbers a and b are equal (true only when a equals b).
3. Size Query: Ask if the size of universe U equals some number k (true only when k equals 12).

Your goals are:
1. Infer whether element 7 is in set S.
2. Identify the periodic pattern P (cyclic shifts of the true pattern are allowed).
3. Provide alignment explanation for at least two membership queries, indicating they are at "honest positions" and stating the true values of those propositions.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Membership Query (e.g., asking about element 5):
<query_in>5</query_in>

- Equality Query (e.g., asking if 3 and 3 are equal):
<query_equal>3,3</query_equal>

- Size Query (e.g., asking if universe size is 12):
<query_size>12</query_size>

When submitting the final answer, you must include three parts:
1. The existence of element 7 (EXISTS or NOT_EXISTS)
2. The periodic pattern (a binary string of length 2 to 5)
3. Alignment explanation (referencing at least two membership query rounds, indicating they are at honest positions with corresponding true values)

Format:
<answer>
declaration=EXISTS
pattern=101
alignment=Round 3 IN 7 at honest position with true value true, Round 6 IN 5 at honest position with true value false
</answer>

Or:
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
智能交通控制系统启动中。当前城市核心区划分为 12 个交通枢纽（编号 U = {{1, 2, ..., 12}}）。
系统内存在一个隐蔽的“常态拥堵枢纽”集合 S，其大小在 3 到 9 之间。
我们的路网传感器存在一种未知的周期性信号反转现象，遵循一个隐藏的周期模式 P。
模式 P 是一个长度为 L（2 到 5 之间）的 0-1 序列，1 表示“传感器反馈真实状况”，0 表示“传感器反馈完全相反的状况”。
在第 i 次探测时，传感器将根据 P 的第 ((i-1) mod L) + 1 位来决定反馈真实或反转的结果。

你可以反复调用控制台进行以下三类数据探测（每次仅限一项操作），传感器会依据当前轮次的周期位返回反馈：

1. 枢纽状态探测：询问某个枢纽 e（1 到 12 之间）是否属于常态拥堵集合 S。
2. 编号一致性校验：询问两个编号 a 和 b 是否相同（仅当 a 等于 b 时为真）。
3. 网络规模校验：询问交通枢纽总数是否等于某个数 k（仅当 k 等于 12 时为真）。

任务目标：
1. 推断枢纽 7 是否属于常态拥堵集合 S。
2. 识别传感器的信号反转周期模式 P（允许与真实模式存在循环位移）。
3. 给出至少两次枢纽状态探测的对齐说明，指出它们处于“传感器反馈真实”的探测轮次，并说明当时的真实拥堵状态。

当你收集足够信息后，请提交排查报告。若报告有误或格式不符，诊断将失败。

## 探测与提交报告的指令格式（必须严格遵守）

每次探测只能包含一个标签。请使用以下 XML 格式：

- 枢纽状态探测（例如探测枢纽 5）：
<query_in>5</query_in>

- 编号一致性校验（例如校验 3 和 3）：
<query_equal>3,3</query_equal>

- 网络规模校验（例如校验总数是否为 12）：
<query_size>12</query_size>

提交排查报告时，必须包含三个部分：
1. 枢纽 7 的拥堵状态（EXISTS 或 NOT_EXISTS）
2. 周期模式（一个长度 2 到 5 的 01 串）
3. 对齐说明（至少引用两次枢纽探测的轮次，说明它们位于真实反馈位及对应真值）

格式如下：
<answer>
declaration=EXISTS
pattern=101
alignment=第3轮IN 7为真实位真值为真，第6轮IN 5为真实位真值为假
</answer>

或者：
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Intelligent traffic control system initiated. The core urban area is divided into 12 traffic hubs (Universe U = {{1, 2, ..., 12}}).
There is a hidden set S of "frequent congestion hubs", with a size between 3 and 9.
Our road network sensors experience an unknown periodic signal inversion phenomenon, following a hidden periodic pattern P.
Pattern P is a binary sequence of length L (between 2 and 5), where 1 means "sensor returns accurate data" and 0 means "sensor returns inverted data".
During your i-th probe, the sensor's feedback is determined by the ((i-1) mod L) + 1-th bit of P.

You can repeatedly perform three types of probes (one per turn), and the sensor will reply accurately or inversely based on the current round's position in the pattern:

1. Hub Status Probe: Ask if a hub e (between 1 and 12) belongs to the congestion set S.
2. ID Consistency Check: Ask if two IDs a and b are identical (true only when a equals b).
3. Network Scale Check: Ask if the total number of hubs equals k (true only when k equals 12).

Your mission objectives:
1. Infer whether hub 7 is in the congestion set S.
2. Identify the sensor's signal inversion pattern P (cyclic shifts of the true pattern are allowed).
3. Provide an alignment explanation for at least two hub status probes, indicating they occurred during "accurate data" rounds and stating their true congestion status.

When you have gathered enough data, submit your diagnostic report. If incorrect or improperly formatted, the system diagnosis will fail.

## Probe and Report Format (strictly required)

Each probe must contain only one tag. Use the following XML format:

- Hub Status Probe (e.g., probing hub 5):
<query_in>5</query_in>

- ID Consistency Check (e.g., checking 3 and 3):
<query_equal>3,3</query_equal>

- Network Scale Check (e.g., checking if total size is 12):
<query_size>12</query_size>

When submitting the final report, you must include three parts:
1. Congestion status of hub 7 (EXISTS or NOT_EXISTS)
2. The periodic pattern (a binary string of length 2 to 5)
3. Alignment explanation (referencing at least two hub probe rounds, indicating they are at accurate positions with corresponding true values)

Format:
<answer>
declaration=EXISTS
pattern=101
alignment=Round 3 IN 7 at honest position with true value true, Round 6 IN 5 at honest position with true value false
</answer>

Or:
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
临床辅助诊断系统初始化。系统中收录了 12 项潜在生化指标异常（编号 U = {{1, 2, ..., 12}}）。
该患者存在一个隐藏的确诊异常组合 S，其大小在 3 到 9 之间。
生化检测仪器当前受到某种未知电磁干扰，呈现周期性偏差模式 P。
模式 P 是一个长度为 L（2 到 5 之间）的 0-1 序列，1 表示“检测结果准确”，0 表示“检测结果呈假阳性/假阴性（完全反转）”。
在第 i 轮检测时，仪器将根据 P 的第 ((i-1) mod L) + 1 位决定是否反转读数。

你可以反复进行以下三类医疗查询（每次仅限一项操作），系统会依据仪器当前轮次的周期位返回诊断反馈：

1. 指标筛查：询问某项生化指标 e（1 到 12 之间）是否在确诊异常组合 S 中。
2. 检验项目校准：询问两个编号 a 和 b 是否代表同一检测项（仅当 a 等于 b 时为真）。
3. 监测总数校验：询问仪器支持的总生化指标数是否为 k（仅当 k 等于 12 时为真）。

你的诊断目标：
1. 推断生化指标 7 是否属于确诊异常组合 S。
2. 识别仪器的检测偏差周期模式 P（允许与真实模式存在循环位移）。
3. 给出至少两次指标筛查的对齐说明，指出它们位于“检测结果准确”的轮次，并说明这些指标真实的异常状态。

收集足够诊断数据后，请提交综合诊断书。若诊断有误或格式不符，分析将宣告失败。

## 筛查与提交诊断书的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 指标筛查（例如筛查指标 5）：
<query_in>5</query_in>

- 检验项目校准（例如校准 3 和 3）：
<query_equal>3,3</query_equal>

- 监测总数校验（例如校验总数是否为 12）：
<query_size>12</query_size>

提交诊断书时，必须包含三个部分：
1. 指标 7 的异常确诊结果（EXISTS 或 NOT_EXISTS）
2. 干扰周期模式（一个长度 2 到 5 的 01 串）
3. 对齐说明（至少引用两次指标筛查的轮次，说明它们位于准确检测位及对应真值）

格式如下：
<answer>
declaration=EXISTS
pattern=101
alignment=第3轮IN 7为准确位真值为真，第6轮IN 5为准确位真值为假
</answer>

或者：
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Clinical auxiliary diagnostic system initialized. The system includes 12 potential biochemical indicator abnormalities (Universe U = {{1, 2, ..., 12}}).
The patient has a hidden confirmed abnormal combination S, with a size between 3 and 9.
The biochemical testing instrument is currently affected by an unknown electromagnetic interference, exhibiting a periodic deviation pattern P.
Pattern P is a binary sequence of length L (between 2 and 5), where 1 means "accurate test result" and 0 means "false positive/negative (completely inverted result)".
During the i-th round of testing, the instrument decides whether to invert the reading based on the ((i-1) mod L) + 1-th bit of P.

You can repeatedly perform three types of medical queries (one operation per turn), and the system will return diagnostic feedback accurately or inversely based on the current round's position in the pattern:

1. Indicator Screening: Ask if a biochemical indicator e (between 1 and 12) is in the confirmed abnormal combination S.
2. Test Item Calibration: Ask if two IDs a and b represent the same test item (true only when a equals b).
3. Monitor Capacity Check: Ask if the total number of biochemical indicators supported by the instrument equals k (true only when k equals 12).

Your diagnostic objectives:
1. Infer whether biochemical indicator 7 belongs to the confirmed abnormal combination S.
2. Identify the instrument's deviation pattern P (cyclic shifts of the true pattern are allowed).
3. Provide an alignment explanation for at least two indicator screenings, indicating they occurred during "accurate test result" rounds and stating their true abnormal status.

When you have gathered enough diagnostic data, submit your comprehensive diagnosis. If incorrect or improperly formatted, the analysis will fail.

## Screening and Diagnosis Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Indicator Screening (e.g., screening indicator 5):
<query_in>5</query_in>

- Test Item Calibration (e.g., calibrating 3 and 3):
<query_equal>3,3</query_equal>

- Monitor Capacity Check (e.g., checking if total size is 12):
<query_size>12</query_size>

When submitting the final diagnosis, you must include three parts:
1. Confirmed abnormal result for indicator 7 (EXISTS or NOT_EXISTS)
2. The deviation periodic pattern (a binary string of length 2 to 5)
3. Alignment explanation (referencing at least two indicator screening rounds, indicating they are at accurate positions with corresponding true values)

Format:
<answer>
declaration=EXISTS
pattern=101
alignment=Round 3 IN 7 at honest position with true value true, Round 6 IN 5 at honest position with true value false
</answer>

Or:
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
自适应学习评估系统启动。该学科库共包含 12 个核心知识模块（编号 U = {{1, 2, ..., 12}}）。
当前接受测试的学生已经掌握了其中的部分核心模块集合 S，其大小在 3 到 9 之间。
自适应测试系统在执行动态评估时存在一种周期性的评分波动模式 P。
模式 P 是一个长度为 L（2 到 5 之间）的 0-1 序列，1 表示“评估结果准确反馈学生掌握情况”，0 表示“评估结果出现逻辑反转”。
在对该学生进行第 i 轮提问时，系统会根据 P 的第 ((i-1) mod L) + 1 位决定是否反转评分判断。

你可以反复发起以下三类测试操作（每次仅限一项），系统会依据当前轮次对应的周期位给出如实或相反的结论：

1. 模块掌握度测试：询问某个知识模块 e（1 到 12 之间）是否被该学生掌握（是否属于 S）。
2. 题库交叉校验：询问编号 a 和 b 是否对应同一个核心知识模块（仅当 a 等于 b 时为真）。
3. 考点总数核实：询问学科库的总模块数是否等于某个数 k（仅当 k 等于 12 时为真）。

你的教学评估目标：
1. 推断该学生是否掌握了核心模块 7。
2. 识别自适应测试系统的评分波动模式 P（允许与真实模式存在循环位移）。
3. 给出至少两次模块掌握度测试的对齐说明，指出它们位于“评估准确”的评分轮次，并说明学生真实的掌握情况。

当你收集足够评估数据后，请提交最终学情报告。若报告有误或格式不符，评估判定失败。

## 测试与提交报告的格式（必须严格遵守）

每次测试操作只能包含一个标签。请使用以下 XML 格式：

- 模块掌握度测试（例如测试模块 5）：
<query_in>5</query_in>

- 题库交叉校验（例如校验 3 和 3）：
<query_equal>3,3</query_equal>

- 考点总数核实（例如核实总数是否为 12）：
<query_size>12</query_size>

提交学情报告时，必须包含三个部分：
1. 模块 7 的掌握情况（EXISTS 或 NOT_EXISTS）
2. 系统的评分波动模式（一个长度 2 到 5 的 01 串）
3. 对齐说明（至少引用两次模块测试的轮次，说明它们位于评估准确位及对应真值）

格式如下：
<answer>
declaration=EXISTS
pattern=101
alignment=第3轮IN 7为准确位真值为真，第6轮IN 5为准确位真值为假
</answer>

或者：
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Adaptive learning evaluation system launched. The subject library contains 12 core knowledge modules (Universe U = {{1, 2, ..., 12}}).
The currently evaluated student has mastered a hidden subset of core modules S, with a size between 3 and 9.
The adaptive testing system exhibits a periodic grading fluctuation pattern P during dynamic evaluation.
Pattern P is a binary sequence of length L (between 2 and 5), where 1 means "evaluation accurately reflects student mastery" and 0 means "evaluation result logically inverted".
During your i-th test query, the system decides whether to invert the evaluation based on the ((i-1) mod L) + 1-th bit of P.

You can repeatedly initiate three types of testing operations (one per turn), and the system will reply accurately or inversely based on the current round's position in the pattern:

1. Module Mastery Test: Ask if a core knowledge module e (between 1 and 12) is mastered by the student (belongs to S).
2. Question Bank Cross-Check: Ask if IDs a and b correspond to the same core knowledge module (true only when a equals b).
3. Total Topics Verification: Ask if the total number of modules in the subject library equals k (true only when k equals 12).

Your pedagogical evaluation objectives:
1. Infer whether the student has mastered core module 7.
2. Identify the system's grading fluctuation pattern P (cyclic shifts of the true pattern are allowed).
3. Provide an alignment explanation for at least two module mastery tests, indicating they occurred during "accurate evaluation" rounds and stating the student's true mastery status.

When you have gathered enough evaluation data, submit the final learning report. If incorrect or improperly formatted, the evaluation process fails.

## Testing and Report Format (strictly required)

Each test query must contain only one tag. Use the following XML format:

- Module Mastery Test (e.g., testing module 5):
<query_in>5</query_in>

- Question Bank Cross-Check (e.g., checking 3 and 3):
<query_equal>3,3</query_equal>

- Total Topics Verification (e.g., verifying if total size is 12):
<query_size>12</query_size>

When submitting the final report, you must include three parts:
1. Mastery status for module 7 (EXISTS or NOT_EXISTS)
2. The grading fluctuation pattern (a binary string of length 2 to 5)
3. Alignment explanation (referencing at least two module test rounds, indicating they are at accurate positions with corresponding true values)

Format:
<answer>
declaration=EXISTS
pattern=101
alignment=Round 3 IN 7 at honest position with true value true, Round 6 IN 5 at honest position with true value false
</answer>

Or:
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    # 场景 4：工业/制造业
    contextualized_rule_zh_4 = """\
自动化流水线质检系统接入。当前核心生产线设有 12 个关键质检节点（编号 U = {{1, 2, ..., 12}}）。
经初步研判，线上存在一批隐藏的“良率不达标”节点集合 S，其大小在 3 到 9 之间。
现场监控探头的信号传输受到工业环境影响，呈现周期性干扰模式 P。
模式 P 是一个长度为 L（2 到 5 之间）的 0-1 序列，1 表示“探头信号正常反馈”，0 表示“探头信号出现逻辑翻转”。
在执行第 i 次质检轮询时，探头将根据 P 的第 ((i-1) mod L) + 1 位决定是否返回翻转后的良率判定。

你可以反复通过工控机发起以下三类信号检测（每次仅限单项指令），系统会依据当前轮询对应的周期位返回反馈：

1. 节点质检探测：询问节点 e（1 到 12 之间）是否属于良率不达标的集合 S。
2. 工位一致性校验：询问编号 a 和 b 是否为同一物理节点（仅当 a 等于 b 时为真）。
3. 产线规模校验：询问全线覆盖的关键质检节点总数是否等于 k（仅当 k 等于 12 时为真）。

你的巡检排查目标：
1. 推断关键节点 7 是否良率不达标。
2. 识别探头的信号翻转周期模式 P（允许与真实模式存在循环位移）。
3. 给出至少两次节点质检探测的对齐说明，指出它们处于“信号正常反馈”的轮次，并说明当时的真实良率达标状态。

当排查完毕后，请提交最终维护检修报告。若结论错误或格式非法，维护指令将被驳回。

## 检测指令与维护报告的格式（必须严格遵守）

每次检测只能包含一个标签。请使用以下 XML 格式：

- 节点质检探测（例如探测节点 5）：
<query_in>5</query_in>

- 工位一致性校验（例如校验 3 和 3）：
<query_equal>3,3</query_equal>

- 产线规模校验（例如校验总数是否为 12）：
<query_size>12</query_size>

提交维护检修报告时，必须包含三个部分：
1. 节点 7 的不达标状态判定（EXISTS 或 NOT_EXISTS）
2. 探头信号周期模式（一个长度 2 到 5 的 01 串）
3. 对齐说明（至少引用两次节点探测的轮次，说明它们位于正常反馈位及对应真值）

格式如下：
<answer>
declaration=EXISTS
pattern=101
alignment=第3轮IN 7为正常位真值为真，第6轮IN 5为正常位真值为假
</answer>

或者：
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Automated assembly line quality inspection system connected. The core production line has 12 critical quality inspection nodes (Universe U = {{1, 2, ..., 12}}).
Preliminary analysis shows there is a hidden set S of "substandard yield rate" nodes, with a size between 3 and 9.
Signal transmission from on-site monitoring probes is affected by the industrial environment, exhibiting a periodic interference pattern P.
Pattern P is a binary sequence of length L (between 2 and 5), where 1 means "probe signal returns normal feedback" and 0 means "probe signal returns a logical inversion".
During the i-th polling sequence, the probe decides whether to invert the yield judgment based on the ((i-1) mod L) + 1-th bit of P.

You can repeatedly initiate three types of signal detections via the industrial PC (one command per turn), and the system will reply accurately or inversely based on the current round's position in the pattern:

1. Node Quality Probe: Ask if node e (between 1 and 12) belongs to the substandard yield set S.
2. Workstation Consistency Check: Ask if IDs a and b correspond to the same physical node (true only when a equals b).
3. Production Line Scale Check: Ask if the total number of critical inspection nodes equals k (true only when k equals 12).

Your inspection and troubleshooting objectives:
1. Infer whether critical node 7 has a substandard yield rate.
2. Identify the probe's signal inversion pattern P (cyclic shifts of the true pattern are allowed).
3. Provide an alignment explanation for at least two node quality probes, indicating they occurred during "normal feedback" rounds and stating their true yield status.

Once troubleshooting is complete, submit the final maintenance report. If incorrect or improperly formatted, the maintenance command will be rejected.

## Detection Command and Report Format (strictly required)

Each detection command must contain only one tag. Use the following XML format:

- Node Quality Probe (e.g., probing node 5):
<query_in>5</query_in>

- Workstation Consistency Check (e.g., checking 3 and 3):
<query_equal>3,3</query_equal>

- Production Line Scale Check (e.g., checking if total size is 12):
<query_size>12</query_size>

When submitting the final maintenance report, you must include three parts:
1. Substandard yield status for node 7 (EXISTS or NOT_EXISTS)
2. The probe signal periodic pattern (a binary string of length 2 to 5)
3. Alignment explanation (referencing at least two node probe rounds, indicating they are at normal positions with corresponding true values)

Format:
<answer>
declaration=EXISTS
pattern=101
alignment=Round 3 IN 7 at honest position with true value true, Round 6 IN 5 at honest position with true value false
</answer>

Or:
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
金融犯罪资金链追踪行动。本案共提取了 12 份关键证据卷宗（编号 U = {{1, 2, ..., 12}}）。
其中有部分核心卷宗构成了一条闭环的“资金伪造链”集合 S，其大小在 3 到 9 之间。
本案的一名关键污点证人在接受质询时，表现出一种高度周期性的说谎模式 P。
模式 P 是一个长度为 L（2 到 5 之间）的 0-1 序列，1 表示“证人提供真实的供述”，0 表示“证人提供完全相反的伪证”。
在法庭展开第 i 轮质询时，该证人将根据 P 的第 ((i-1) mod L) + 1 位决定是供出实情还是作伪证。

你可以反复对该证人提出以下三类质询（每次仅限一个问题），证人会根据当前轮次对应的周期位来如实或相反地作答：

1. 卷宗质证：询问卷宗 e（1 到 12 之间）是否属于资金伪造链 S。
2. 证据同一性审查：询问编号 a 和 b 的卷宗是否为同一份材料（仅当 a 等于 b 时为真）。
3. 案件规模核实：询问警方查扣的关键涉案卷宗总数是否为 k（仅当 k 等于 12 时为真）。

你的庭审质证目标：
1. 推断卷宗 7 是否属于资金伪造链。
2. 识别该证人的供述周期模式 P（允许与真实模式存在循环位移）。
3. 给出至少两次卷宗质证的对齐说明，指出它们位于“证人说真话”的质询轮次，并说明当时的真实资金链属性。

当质证环节结束后，请向法庭提交最终审查结案陈词。若结论错误或格式违规，指控将被撤销。

## 质询与提交结案陈词的格式（必须严格遵守）

每次质询只能包含一个标签。请使用以下 XML 格式：

- 卷宗质证（例如质证卷宗 5）：
<query_in>5</query_in>

- 证据同一性审查（例如审查 3 和 3）：
<query_equal>3,3</query_equal>

- 案件规模核实（例如核实总数是否为 12）：
<query_size>12</query_size>

提交结案陈词时，必须包含三个部分：
1. 卷宗 7 是否在伪造链中（EXISTS 或 NOT_EXISTS）
2. 证人说谎的周期模式（一个长度 2 到 5 的 01 串）
3. 对齐说明（至少引用两次卷宗质证的轮次，说明它们位于真话位及对应真值）

格式如下：
<answer>
declaration=EXISTS
pattern=101
alignment=第3轮IN 7为真话位真值为真，第6轮IN 5为真话位真值为假
</answer>

或者：
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Financial crime fund tracking operation. The case involves 12 key evidence files (Universe U = {{1, 2, ..., 12}}).
Among them, certain core files form a closed-loop "forged fund chain" set S, with a size between 3 and 9.
A key tainted witness in this case exhibits a highly periodic lying pattern P during cross-examination.
Pattern P is a binary sequence of length L (between 2 and 5), where 1 means "witness gives truthful testimony" and 0 means "witness gives completely contrary perjury".
During the i-th round of courtroom questioning, the witness decides whether to tell the truth or commit perjury based on the ((i-1) mod L) + 1-th bit of P.

You can repeatedly ask the witness three types of questions (one per turn), and the witness will answer honestly or oppositely based on the current round's position in the pattern:

1. File Cross-Examination: Ask if file e (between 1 and 12) belongs to the forged fund chain S.
2. Evidence Identity Review: Ask if IDs a and b correspond to the exact same file material (true only when a equals b).
3. Case Scale Verification: Ask if the total number of key seized files equals k (true only when k equals 12).

Your courtroom objectives:
1. Infer whether file 7 is part of the forged fund chain.
2. Identify the witness's testimony cycle pattern P (cyclic shifts of the true pattern are allowed).
3. Provide an alignment explanation for at least two file cross-examinations, indicating they occurred during "truthful testimony" rounds and stating the true nature of the fund chain.

When the cross-examination is concluded, submit your final closing statement to the court. If incorrect or improperly formatted, the charges will be dismissed.

## Questioning and Closing Statement Format (strictly required)

Each question must contain only one tag. Use the following XML format:

- File Cross-Examination (e.g., examining file 5):
<query_in>5</query_in>

- Evidence Identity Review (e.g., reviewing 3 and 3):
<query_equal>3,3</query_equal>

- Case Scale Verification (e.g., verifying if total size is 12):
<query_size>12</query_size>

When submitting the final closing statement, you must include three parts:
1. Inclusion of file 7 in the forged chain (EXISTS or NOT_EXISTS)
2. The witness perjury periodic pattern (a binary string of length 2 to 5)
3. Alignment explanation (referencing at least two file cross-examination rounds, indicating they are at honest positions with corresponding true values)

Format:
<answer>
declaration=EXISTS
pattern=101
alignment=Round 3 IN 7 at honest position with true value true, Round 6 IN 5 at honest position with true value false
</answer>

Or:
<answer>
declaration=NOT_EXISTS
pattern=01
alignment=Round 2 IN 7 at honest position with true value false, Round 4 IN 3 at honest position with true value true
</answer>
"""

    tags = ["answer", "query_in", "query_equal", "query_size"]

    reasoning_type = "归纳推理"
    data_structure = "集合"

    # 难度配置说明：
    # 1 (简单)      - |S|=3, L=2, 模式简单，7在S中
    # 2 (中等偏下)  - |S|=5, L=3, 7在S中
    # 3 (中等偏上)  - |S|=6, L=3, 7不在S中
    # 4 (较难)      - |S|=7, L=4, 7在S中
    # 5 (难)        - |S|=9, L=5, 7不在S中

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "S": {1, 7, 12},  # 7在S中
                "P": [1, 0],       # 周期：诚实-相反
            },
            2: {
                "S": {2, 5, 7, 9, 11},  # 7在S中
                "P": [1, 0, 1],          # 周期：诚实-相反-诚实
            },
            3: {
                "S": {1, 2, 3, 8, 10, 12},  # 7不在S中
                "P": [1, 1, 0],              # 周期：诚实-诚实-相反
            },
            4: {
                "S": {1, 4, 6, 7, 8, 10, 11},  # 7在S中
                "P": [1, 0, 1, 0],              # 周期：诚实-相反-诚实-相反
            },
            5: {
                "S": {1, 2, 3, 4, 5, 8, 9, 10, 12},  # 7不在S中
                "P": [1, 0, 0, 1, 0],                 # 周期：诚实-相反-相反-诚实-相反
            },
        },
        "en": {
            1: {
                "S": {1, 7, 12},
                "P": [1, 0],
            },
            2: {
                "S": {2, 5, 7, 9, 11},
                "P": [1, 0, 1],
            },
            3: {
                "S": {1, 2, 3, 8, 10, 12},
                "P": [1, 1, 0],
            },
            4: {
                "S": {1, 4, 6, 7, 8, 10, 11},
                "P": [1, 0, 1, 0],
            },
            5: {
                "S": {1, 2, 3, 4, 5, 8, 9, 10, 12},
                "P": [1, 0, 0, 1, 0],
            },
        },
    }

    def __init__(self, config):
        self.round_count = 0  # 当前轮次计数
        self.query_history = []  # 记录所有查询历史：[(round, query_type, query_content, answer)]
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        # 确保 difficulty 为整数
        try:
            diff = int(diff)
        except (ValueError, TypeError):
            raise KeyError(f"Unsupported difficulty: {diff}")

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.S = cfg["S"]  # 隐藏的子集
        self.P = cfg["P"]  # 周期模式
        self.L = len(self.P)  # 周期长度
        
        # 记录真实答案供最后验证
        self.seven_in_S = 7 in self.S
        
        # 初始化游戏信息（用于规则模板，这里不需要动态替换）
        self._game_info = {}

    def _get_honest_bit(self, round_num):
        """获取当前轮次的诚实位"""
        return self.P[(round_num - 1) % self.L]

    def _answer_with_pattern(self, truth_value, round_num):
        """根据周期模式返回答案"""
        honest = self._get_honest_bit(round_num)
        if honest == 1:
            return truth_value
        else:
            return not truth_value

    def evaluate(self, parsed_info):
        """评估最终答案"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案的三个部分
        declaration = None
        pattern = None
        alignment = None
        
        # 提取 declaration
        decl_match = re.search(r'declaration\s*=\s*(\w+)', raw_ans, re.IGNORECASE)
        if decl_match:
            declaration = decl_match.group(1).strip().upper()
        
        # 提取 pattern
        pattern_match = re.search(r'pattern\s*=\s*([01]+)', raw_ans, re.IGNORECASE)
        if pattern_match:
            pattern = pattern_match.group(1).strip()
        
        # 提取 alignment —— 取 alignment= 之后到答案末尾的所有内容
        align_match = re.search(r'alignment\s*=\s*(.*)', raw_ans, re.IGNORECASE | re.DOTALL)
        if align_match:
            alignment = align_match.group(1).strip()
        
        # 检查必要字段是否存在
        if not declaration or not pattern or not alignment:
            return False
        
        # 1. 检查 declaration 是否正确
        if self.seven_in_S:
            if declaration != "EXISTS":
                return False
        else:
            if declaration != "NOT_EXISTS":
                return False
        
        # 2. 检查 pattern 是否与真实模式等价（允许循环位移）
        if not self._check_pattern_equivalence(pattern):
            return False
        
        # 3. 检查 alignment 说明
        # 如果没有查询历史（如冗余性测试），仅验证 declaration 和 pattern
        if self.query_history:
            if not self._check_alignment(alignment):
                return False
        else:
            # 宽松检查：至少有一定长度的对齐说明文本
            if not alignment or len(alignment) < 10:
                return False
        
        return True

    def _check_pattern_equivalence(self, pattern_str):
        """检查给定模式是否与真实模式等价（允许循环位移）"""
        if len(pattern_str) != self.L:
            return False
        
        real_pattern = ''.join(map(str, self.P))
        # 检查所有循环位移
        for i in range(self.L):
            rotated = pattern_str[i:] + pattern_str[:i]
            if rotated == real_pattern:
                return True
        return False

    def _check_alignment(self, alignment_text):
        """
        检查对齐说明是否合理
        要求：至少引用两次成员查询，指出它们在诚实位，并说明真值
        如果没有查询历史（例如冗余性测试中直接评估），则仅做格式宽松检查。
        """
        # 从查询历史中找出所有成员查询
        member_queries = [
            (i+1, q[1], q[2], q[3]) 
            for i, q in enumerate(self.query_history) 
            if q[1] == "IN"
        ]
        
        # 如果没有查询历史（冗余性测试等场景），采用宽松验证
        if not self.query_history:
            if alignment_text and len(alignment_text) >= 10:
                return True
            return False
        
        # 找出位于诚实位的成员查询
        honest_member_queries = []
        for round_num, qtype, elem, answer in member_queries:
            honest_bit = self._get_honest_bit(round_num)
            if honest_bit == 1:
                honest_member_queries.append((round_num, elem))
        
        if len(honest_member_queries) < 2:
            # 如果诚实位的成员查询不足两次，无法完成对齐
            return False
        
        # 检查对齐说明中提到的诚实位成员查询
        mentioned_count = 0
        for round_num, elem in honest_member_queries:
            # 使用词边界匹配避免子串误匹配
            round_pattern = r'(?<!\d)' + str(round_num) + r'(?!\d)'
            elem_pattern = r'(?<!\d)' + str(elem) + r'(?!\d)'
            if re.search(round_pattern, alignment_text) or re.search(elem_pattern, alignment_text):
                mentioned_count += 1
        
        return mentioned_count >= 2

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑（原 produce_response 的内容）"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效。"
            error_range = "错误：数字超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format."
            error_range = "Error: Number out of range."

        # 处理成员查询
        if "query_in" in parsed_info:
            try:
                elem = int(parsed_info["query_in"].strip())
                if elem < 1 or elem > 12:
                    return error_range
                
                self.round_count += 1
                current_round = self.round_count
                
                truth_value = elem in self.S
                result = self._answer_with_pattern(truth_value, current_round)
                answer = yes_res if result else no_res
                
                # 记录查询历史
                self.query_history.append((current_round, "IN", elem, answer))
                return answer
            except (ValueError, TypeError):
                return error_format

        # 处理相等查询
        elif "query_equal" in parsed_info:
            try:
                raw = parsed_info["query_equal"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                a, b = int(parts[0]), int(parts[1])
                if a < 1 or a > 12 or b < 1 or b > 12:
                    return error_range
                
                self.round_count += 1
                current_round = self.round_count
                
                truth_value = (a == b)
                result = self._answer_with_pattern(truth_value, current_round)
                answer = yes_res if result else no_res
                
                # 记录查询历史
                self.query_history.append((current_round, "EQUAL", f"{a},{b}", answer))
                return answer
            except (ValueError, TypeError):
                return error_format

        # 处理大小查询
        elif "query_size" in parsed_info:
            try:
                k = int(parsed_info["query_size"].strip())
                
                self.round_count += 1
                current_round = self.round_count
                
                truth_value = (k == 12)
                result = self._answer_with_pattern(truth_value, current_round)
                answer = yes_res if result else no_res
                
                # 记录查询历史
                self.query_history.append((current_round, "SIZE", k, answer))
                return answer
            except (ValueError, TypeError):
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 处理英文 Yes/No，忽略大小写但保持原始大小写风格
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        每个查询按顺序对应一个递增的轮次编号，
        与 _cf_core_produce 中 round_count 自增的行为保持一致。
        精简相等查询以避免过多无意义查询。
        """
        possible_queries = []

        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 收集所有待计算的查询（先不计算答案）
        raw_queries = []

        # 1. 成员查询 (query_in): 1 到 12
        for e in range(1, 13):
            xml_query = f"<query_in>{e}</query_in>"
            truth_val = e in self.S
            raw_queries.append((xml_query, truth_val))

        # 2. 相等查询 (query_equal): 只保留有代表性的子集
        # a == b 的情况（12个）
        for a in range(1, 13):
            xml_query = f"<query_equal>{a},{a}</query_equal>"
            raw_queries.append((xml_query, True))
        # a != b 的少量样本（4个）
        for a, b in [(1, 2), (3, 7), (5, 10), (8, 12)]:
            xml_query = f"<query_equal>{a},{b}</query_equal>"
            raw_queries.append((xml_query, False))

        # 3. 大小查询 (query_size): 保留关键的几个
        for k in [1, 6, 12]:
            xml_query = f"<query_size>{k}</query_size>"
            truth_val = (k == 12)
            raw_queries.append((xml_query, truth_val))

        # 按顺序为每个查询分配轮次编号，从 round_count+1 开始递增
        for idx, (xml_query, truth_val) in enumerate(raw_queries):
            round_num = self.round_count + 1 + idx
            result_bool = self._answer_with_pattern(truth_val, round_num)
            ans = yes_res if result_bool else no_res
            possible_queries.append({
                "query": xml_query,
                "answer": ans
            })

        return possible_queries