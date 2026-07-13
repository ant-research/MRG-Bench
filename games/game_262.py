from .base import Game
import re


class FunctionIdentificationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"函数识别与验证"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序整数序列 a[1..{n}]，初始序列为：{sequence}。

我已秘密选择了一个指标函数 F，它只可能是以下四个候选之一：
1. 方案A（总和）：计算序列所有元素的总和
2. 方案B（相邻差总和）：计算序列中所有相邻元素差的绝对值之和
3. 方案C（偶数计数）：计算序列中偶数元素的个数
4. 方案D（位置加权和）：计算每个元素与其位置的乘积之和

你的目标是通过查询和试验识别真实的函数方案，并通过两次带预测的正式替换来验证你的判断。

你可以反复向我提出以下类型的请求（每次仅限一个请求）：

1. 查询当前函数值：获取当前序列的函数值
2. 试验替换：临时将某个位置的值替换为新值，查看函数值的变化（试验后序列会恢复原状）
3. 试验比较：对同一位置尝试两个不同的替换值，分别查看函数值变化（试验后序列会恢复原状）
4. 提交方案判定：声明你认为的函数方案（需先完成至少两次试验替换）
5. 正式替换：永久替换某个位置的值，并预测替换后的函数值（最多两次，每次都需要预测）
6. 查询当前序列：获取当前真实序列（仅在正式替换后可用）

## 请求格式（必须严格遵守）

每次请求只能包含一个标签。请使用以下 XML 格式：

- 查询当前函数值：
<query_value></query_value>

- 试验替换（例如将位置 3 的值替换为 5）：
<test_replace>3,5</test_replace>

- 试验比较（例如在位置 2 分别尝试值 4 和 7）：
<test_compare>2,4,7</test_compare>

- 提交方案判定（例如判定为方案A）：
<submit_scheme>A</submit_scheme>

- 正式替换（例如将位置 1 替换为 6，并预测新函数值为 28）：
<formal_replace>1,6,28</formal_replace>

- 查询当前序列：
<query_sequence></query_sequence>

- 提交最终答案（确认完成游戏）：
<answer>completed</answer>

## 胜负判定

胜利条件（需同时满足）：
1. 在进行至少两次试验替换后提交了方案判定
2. 完成两次正式替换，且每次的预测值均与实际值一致
3. 提交最终答案

失败条件（任一满足）：
1. 未达两次试验替换即提交方案判定
2. 两次正式替换中任一次预测不匹配
3. 超出最多2次正式替换
4. 格式错误或无效请求
"""

    game_rule_en = """\
Let's play a "Function Identification and Verification" deduction game. Here are the rules:

The game has set an ordered integer sequence a[1..{n}] of length {n}. The initial sequence is: {sequence}.

I have secretly chosen an indicator function F, which can only be one of the following four candidates:
1. Scheme A (Sum): Calculate the sum of all elements in the sequence
2. Scheme B (Adjacent Difference Sum): Calculate the sum of absolute differences between all adjacent elements
3. Scheme C (Even Count): Count the number of even elements in the sequence
4. Scheme D (Position Weighted Sum): Calculate the sum of products of each element and its position

Your goal is to identify the true function scheme through queries and experiments, and verify your judgment through two formal replacements with predictions.

You can repeatedly make the following types of requests (one request at a time):

1. Query Current Value: Get the function value of the current sequence
2. Test Replace: Temporarily replace a value at a position with a new value and see the function value change (sequence restores after test)
3. Test Compare: Try two different replacement values at the same position and see their respective function value changes (sequence restores after test)
4. Submit Scheme: Declare the function scheme you believe (requires at least two test replacements first)
5. Formal Replace: Permanently replace a value at a position and predict the new function value (maximum twice, prediction required each time)
6. Query Sequence: Get the current real sequence (only available after formal replacements)

## Request Format (must strictly follow)

Each request can only contain one tag. Use the following XML format:

- Query current function value:
<query_value></query_value>

- Test replace (e.g., replace position 3 with value 5):
<test_replace>3,5</test_replace>

- Test compare (e.g., try values 4 and 7 at position 2):
<test_compare>2,4,7</test_compare>

- Submit scheme (e.g., declare scheme A):
<submit_scheme>A</submit_scheme>

- Formal replace (e.g., replace position 1 with 6, predicting new value 28):
<formal_replace>1,6,28</formal_replace>

- Query current sequence:
<query_sequence></query_sequence>

- Submit final answer (confirm completion):
<answer>completed</answer>

## Win/Loss Conditions

Victory conditions (all must be met):
1. Submit scheme determination after at least two test replacements
2. Complete two formal replacements with both predictions matching actual values
3. Submit final answer

Failure conditions (any one met):
1. Submit scheme determination before two test replacements
2. Any prediction mismatch in the two formal replacements
3. Exceed maximum of 2 formal replacements
4. Format error or invalid request
"""

    contextualized_rule_zh_1 = """\
智能交通信号控制系统的初步分析启动。

系统检测到一条主干道上连续 {n} 个路口的初始车流量序列 a[1..{n}]，初始序列为：{sequence}。

指挥中心秘密启用了一个特定的交通评估指标函数 F，它仅可能是以下四个方案之一：
1. 方案A（总交通量）：计算所有路口车流量的总和
2. 方案B（相邻波动总和）：计算所有相邻路口之间车流量差值的绝对值之和
3. 方案C（偶数流量计数）：计算车流量为偶数的路口个数（用于车道对称性评估）
4. 方案D（位置加权流量）：计算每个路口的车流量与其所处顺位（从1开始）的乘积之和，评估拥堵蔓延效应

你的目标是通过查询和试验，识别出真实的评估函数，并通过两次带预测的正式流量修正来验证你的判断。

你可以反复向中心提出以下类型的请求（每次仅限一个请求）：

1. 查询当前指标值：获取当前序列的评估函数值
2. 试验替换：临时调整某个路口的车流量，查看指标值的变化（评估后序列会恢复原状）
3. 试验比较：对同一路口尝试两种不同的车流量，分别查看指标值变化（评估后序列会恢复原状）
4. 提交方案判定：声明你认为的评估函数方案（需先完成至少两次试验替换）
5. 正式替换：永久修正某个路口的车流量，并预测修正后的指标值（最多两次，每次都需要预测）
6. 查询当前序列：获取当前真实的路口车流量序列（仅在正式替换后可用）

## 请求格式（必须严格遵守）

每次请求只能包含一个标签。请使用以下 XML 格式：

- 查询当前指标值：
<query_value></query_value>

- 试验替换（例如将路口 3 的流量调整为 5）：
<test_replace>3,5</test_replace>

- 试验比较（例如在路口 2 分别尝试流量 4 和 7）：
<test_compare>2,4,7</test_compare>

- 提交方案判定（例如判定为方案A）：
<submit_scheme>A</submit_scheme>

- 正式替换（例如将路口 1 流量正式修正为 6，并预测新指标值为 28）：
<formal_replace>1,6,28</formal_replace>

- 查询当前序列：
<query_sequence></query_sequence>

- 提交最终答案（确认完成分析）：
<answer>completed</answer>

## 胜负判定

胜利条件（需同时满足）：
1. 在进行至少两次试验替换后提交了方案判定
2. 完成两次正式替换，且每次的预测值均与实际值一致
3. 提交最终答案

失败条件（任一满足）：
1. 未达两次试验替换即提交方案判定
2. 两次正式替换中任一次预测不匹配
3. 超出最多2次正式替换
4. 格式错误或无效请求
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Initial analysis of the Intelligent Traffic Signal Control System has started.

The system has detected an initial traffic flow sequence a[1..{n}] across {n} consecutive intersections on a main road. The initial sequence is: {sequence}.

The command center has secretly activated a specific traffic evaluation indicator function F, which can only be one of the following four candidates:
1. Scheme A (Total Volume): Calculate the sum of traffic flow across all intersections
2. Scheme B (Adjacent Fluctuation Sum): Calculate the sum of absolute differences in traffic flow between all adjacent intersections
3. Scheme C (Even Flow Count): Count the number of intersections with an even traffic flow (used for lane symmetry evaluation)
4. Scheme D (Position Weighted Flow): Calculate the sum of products of each intersection's traffic flow and its position index (starting from 1), to evaluate congestion spread effect

Your goal is to identify the true evaluation function scheme through queries and experiments, and verify your judgment through two formal flow corrections with predictions.

You can repeatedly make the following types of requests (one request at a time):

1. Query Current Value: Get the indicator function value of the current sequence
2. Test Replace: Temporarily adjust the traffic flow at an intersection with a new value and see the indicator value change (sequence restores after test)
3. Test Compare: Try two different flow values at the same intersection and see their respective indicator value changes (sequence restores after test)
4. Submit Scheme: Declare the evaluation scheme you believe is active (requires at least two test replacements first)
5. Formal Replace: Permanently correct the flow at an intersection and predict the new indicator value (maximum twice, prediction required each time)
6. Query Sequence: Get the current real traffic flow sequence (only available after formal replacements)

## Request Format (must strictly follow)

Each request can only contain one tag. Use the following XML format:

- Query current indicator value:
<query_value></query_value>

- Test replace (e.g., adjust intersection 3 flow to 5):
<test_replace>3,5</test_replace>

- Test compare (e.g., try flows 4 and 7 at intersection 2):
<test_compare>2,4,7</test_compare>

- Submit scheme (e.g., declare scheme A):
<submit_scheme>A</submit_scheme>

- Formal replace (e.g., formally correct intersection 1 flow to 6, predicting new indicator value 28):
<formal_replace>1,6,28</formal_replace>

- Query current sequence:
<query_sequence></query_sequence>

- Submit final answer (confirm completion):
<answer>completed</answer>

## Win/Loss Conditions

Victory conditions (all must be met):
1. Submit scheme determination after at least two test replacements
2. Complete two formal replacements with both predictions matching actual values
3. Submit final answer

Failure conditions (any one met):
1. Submit scheme determination before two test replacements
2. Any prediction mismatch in the two formal replacements
3. Exceed maximum of 2 formal replacements
4. Format error or invalid request
"""

    contextualized_rule_zh_2 = """\
临床药物试验的数据核查已启动。

我们记录了一个疗程内连续 {n} 天的特定药物给药剂量序列 a[1..{n}]，初始序列为：{sequence}。

临床系统后台秘密套用了一个药效评估指标函数 F，它只可能是以下四个候选方案之一：
1. 方案A（累计总剂量）：计算所有天数给药剂量的总和
2. 方案B（日间波动总和）：计算所有相邻天数之间剂量差值的绝对值之和
3. 方案C（常规偶数剂量天数）：计算给药剂量为偶数的天数（用于评估标准化药片分配频次）
4. 方案D（时间加权剂量蓄积）：计算每天的剂量与其所处天数（从1开始）的乘积之和，以评估药物蓄积毒性

你的目标是通过查询和模拟试验，识别出真实的药效评估函数，并通过两次带预测的正式处方修改来验证你的判断。

你可以反复向系统提出以下类型的请求（每次仅限一个请求）：

1. 查询当前指标值：获取当前处方序列的评估函数值
2. 试验替换：临时调整某天的给药剂量，查看指标值的变化（评估后序列会恢复原状）
3. 试验比较：对同一天尝试两种不同的剂量，分别查看指标值变化（评估后序列会恢复原状）
4. 提交方案判定：声明你认为的评估函数方案（需先完成至少两次试验替换）
5. 正式替换：永久修改某天的给药剂量，并预测修改后的指标值（最多两次，每次都需要预测）
6. 查询当前序列：获取当前真实的处方剂量序列（仅在正式替换后可用）

## 请求格式（必须严格遵守）

每次请求只能包含一个标签。请使用以下 XML 格式：

- 查询当前指标值：
<query_value></query_value>

- 试验替换（例如将第 3 天的剂量调整为 5）：
<test_replace>3,5</test_replace>

- 试验比较（例如在第 2 天分别尝试剂量 4 和 7）：
<test_compare>2,4,7</test_compare>

- 提交方案判定（例如判定为方案A）：
<submit_scheme>A</submit_scheme>

- 正式替换（例如将第 1 天的剂量正式修改为 6，并预测新指标值为 28）：
<formal_replace>1,6,28</formal_replace>

- 查询当前序列：
<query_sequence></query_sequence>

- 提交最终答案（确认完成核查）：
<answer>completed</answer>

## 胜负判定

胜利条件（需同时满足）：
1. 在进行至少两次试验替换后提交了方案判定
2. 完成两次正式替换，且每次的预测值均与实际值一致
3. 提交最终答案

失败条件（任一满足）：
1. 未达两次试验替换即提交方案判定
2. 两次正式替换中任一次预测不匹配
3. 超出最多2次正式替换
4. 格式错误或无效请求
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Data verification for the clinical drug trial has been initiated.

We have recorded a sequence a[1..{n}] of specific drug dosages administered over {n} consecutive days in a treatment course. The initial sequence is: {sequence}.

The clinical system has secretly applied an efficacy evaluation indicator function F, which can only be one of the following four candidates:
1. Scheme A (Cumulative Total Dosage): Calculate the sum of dosages across all days
2. Scheme B (Inter-day Fluctuation Sum): Calculate the sum of absolute differences in dosages between all consecutive days
3. Scheme C (Even Dosage Days): Count the number of days with an even dosage (used to evaluate standard pill distribution frequency)
4. Scheme D (Time-Weighted Dosage Accumulation): Calculate the sum of products of each day's dosage and its day index (starting from 1), to assess cumulative drug toxicity

Your goal is to identify the true evaluation function scheme through queries and simulation tests, and verify your judgment through two formal prescription modifications with predictions.

You can repeatedly make the following types of requests (one request at a time):

1. Query Current Value: Get the indicator function value of the current prescription sequence
2. Test Replace: Temporarily adjust the dosage on a specific day with a new value and see the indicator value change (sequence restores after test)
3. Test Compare: Try two different dosages on the same day and see their respective indicator value changes (sequence restores after test)
4. Submit Scheme: Declare the evaluation scheme you believe is active (requires at least two test replacements first)
5. Formal Replace: Permanently modify the dosage on a specific day and predict the new indicator value (maximum twice, prediction required each time)
6. Query Sequence: Get the current real prescription dosage sequence (only available after formal replacements)

## Request Format (must strictly follow)

Each request can only contain one tag. Use the following XML format:

- Query current indicator value:
<query_value></query_value>

- Test replace (e.g., adjust day 3 dosage to 5):
<test_replace>3,5</test_replace>

- Test compare (e.g., try dosages 4 and 7 on day 2):
<test_compare>2,4,7</test_compare>

- Submit scheme (e.g., declare scheme A):
<submit_scheme>A</submit_scheme>

- Formal replace (e.g., formally modify day 1 dosage to 6, predicting new indicator value 28):
<formal_replace>1,6,28</formal_replace>

- Query current sequence:
<query_sequence></query_sequence>

- Submit final answer (confirm completion):
<answer>completed</answer>

## Win/Loss Conditions

Victory conditions (all must be met):
1. Submit scheme determination after at least two test replacements
2. Complete two formal replacements with both predictions matching actual values
3. Submit final answer

Failure conditions (any one met):
1. Submit scheme determination before two test replacements
2. Any prediction mismatch in the two formal replacements
3. Exceed maximum of 2 formal replacements
4. Format error or invalid request
"""

    contextualized_rule_zh_3 = """\
学生学习行为与学情追踪分析系统启动。

系统提取了一名学生在连续 {n} 个学习模块中的测验得分序列 a[1..{n}]，初始序列为：{sequence}。

教务后台秘密设定了一个综合学情评价函数 F，它仅可能是以下四个评估方案之一：
1. 方案A（模块总分）：计算所有模块得分的总和
2. 方案B（成绩波动总和）：计算所有相邻模块之间得分差值的绝对值之和（反映学习状态的稳定性）
3. 方案C（偶数得分模块数）：计算得分数值为偶数的模块个数（用于特定的等级换算统计）
4. 方案D（进度加权得分）：计算每个模块的得分与其所处学习阶段（从1开始）的乘积之和，以强化后期进阶模块的比重

你的目标是通过查询和模拟试验，识别出真实的学情评价函数，并通过两次带预测的正式成绩修正来验证你的判断。

你可以反复向系统提出以下类型的请求（每次仅限一个请求）：

1. 查询当前评价指标：获取当前得分序列的函数评估值
2. 试验替换：临时调整某个模块的得分，查看评价指标的变化（测试后序列会恢复原状）
3. 试验比较：对同一模块尝试两种不同的得分，分别查看评价指标的变化（测试后序列会恢复原状）
4. 提交方案判定：声明你认为的学情评价方案（需先完成至少两次试验替换）
5. 正式替换：永久修正某个模块的得分，并预测修正后的评价指标值（最多两次，每次都需要预测）
6. 查询当前序列：获取当前真实的模块得分序列（仅在正式替换后可用）

## 请求格式（必须严格遵守）

每次请求只能包含一个标签。请使用以下 XML 格式：

- 查询当前评价指标：
<query_value></query_value>

- 试验替换（例如将模块 3 的得分调整为 5）：
<test_replace>3,5</test_replace>

- 试验比较（例如在模块 2 分别尝试得分 4 和 7）：
<test_compare>2,4,7</test_compare>

- 提交方案判定（例如判定为方案A）：
<submit_scheme>A</submit_scheme>

- 正式替换（例如将模块 1 的得分正式修正为 6，并预测新评价指标为 28）：
<formal_replace>1,6,28</formal_replace>

- 查询当前序列：
<query_sequence></query_sequence>

- 提交最终答案（确认完成分析）：
<answer>completed</answer>

## 胜负判定

胜利条件（需同时满足）：
1. 在进行至少两次试验替换后提交了方案判定
2. 完成两次正式替换，且每次的预测值均与实际值一致
3. 提交最终答案

失败条件（任一满足）：
1. 未达两次试验替换即提交方案判定
2. 两次正式替换中任一次预测不匹配
3. 超出最多2次正式替换
4. 格式错误或无效请求
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The student learning behavior and academic tracking analysis system has been activated.

The system has extracted a test score sequence a[1..{n}] of a student across {n} consecutive learning modules. The initial sequence is: {sequence}.

The academic backend has secretly set a comprehensive academic evaluation function F, which can only be one of the following four assessment schemes:
1. Scheme A (Total Module Score): Calculate the sum of scores across all modules
2. Scheme B (Score Fluctuation Sum): Calculate the sum of absolute differences in scores between all adjacent modules (reflecting learning stability)
3. Scheme C (Even Score Modules): Count the number of modules with an even score (used for specific grading conversion statistics)
4. Scheme D (Progress-Weighted Score): Calculate the sum of products of each module's score and its learning stage index (starting from 1), to emphasize advanced later modules

Your goal is to identify the true academic evaluation function through queries and simulation tests, and verify your judgment through two formal score corrections with predictions.

You can repeatedly make the following types of requests (one request at a time):

1. Query Current Value: Get the evaluation function value of the current score sequence
2. Test Replace: Temporarily adjust the score of a module with a new value and see the evaluation value change (sequence restores after test)
3. Test Compare: Try two different scores for the same module and see their respective evaluation value changes (sequence restores after test)
4. Submit Scheme: Declare the evaluation scheme you believe is active (requires at least two test replacements first)
5. Formal Replace: Permanently correct the score of a module and predict the new evaluation value (maximum twice, prediction required each time)
6. Query Sequence: Get the current real module score sequence (only available after formal replacements)

## Request Format (must strictly follow)

Each request can only contain one tag. Use the following XML format:

- Query current evaluation value:
<query_value></query_value>

- Test replace (e.g., adjust module 3 score to 5):
<test_replace>3,5</test_replace>

- Test compare (e.g., try scores 4 and 7 in module 2):
<test_compare>2,4,7</test_compare>

- Submit scheme (e.g., declare scheme A):
<submit_scheme>A</submit_scheme>

- Formal replace (e.g., formally correct module 1 score to 6, predicting new evaluation value 28):
<formal_replace>1,6,28</formal_replace>

- Query current sequence:
<query_sequence></query_sequence>

- Submit final answer (confirm completion):
<answer>completed</answer>

## Win/Loss Conditions

Victory conditions (all must be met):
1. Submit scheme determination after at least two test replacements
2. Complete two formal replacements with both predictions matching actual values
3. Submit final answer

Failure conditions (any one met):
1. Submit scheme determination before two test replacements
2. Any prediction mismatch in the two formal replacements
3. Exceed maximum of 2 formal replacements
4. Format error or invalid request
"""

    contextualized_rule_zh_4 = """\
自动化流水线生产效能分析监控启动。

监控系统采集了连续 {n} 个装配工位的初始产量序列 a[1..{n}]，初始序列为：{sequence}。

工业控制中枢秘密挂载了一个效能评估函数 F，它仅可能是以下四个分析方案之一：
1. 方案A（总产量）：计算所有工位产量的总和
2. 方案B（工位协同波动总和）：计算所有相邻工位之间产量差值的绝对值之和（用于评估流水线节拍的平顺度）
3. 方案C（双规产量工位数）：计算产量为偶数的工位个数（用于评估适用双托盘并发流转的节点数）
4. 方案D（工位加权产能指数）：计算每个工位的产量与其工位序号（从1开始）的乘积之和，以反映后端工位对最终产能的高权重影响

你的目标是通过查询和模拟调整，识别出真实的效能评估函数，并通过两次带预测的正式产量参数重置来验证你的判断。

你可以反复向系统提出以下类型的指令（每次仅限一个指令）：

1. 查询当前效能指标：获取当前产量序列的效能评估函数值
2. 试验替换：临时调整某个工位的产量参数，查看效能指标的变化（评估后序列会恢复原状）
3. 试验比较：对同一工位尝试两组不同的产量参数，分别查看效能指标的变化（评估后序列会恢复原状）
4. 提交方案判定：声明你认为的效能评估方案（需先完成至少两次试验替换）
5. 正式替换：永久重置某个工位的产量参数，并预测重置后的效能指标值（最多两次，每次都需要预测）
6. 查询当前序列：获取当前真实的工位产量序列（仅在正式替换后可用）

## 指令格式（必须严格遵守）

每次指令只能包含一个标签。请使用以下 XML 格式：

- 查询当前效能指标：
<query_value></query_value>

- 试验替换（例如将工位 3 的产量调整为 5）：
<test_replace>3,5</test_replace>

- 试验比较（例如在工位 2 分别尝试产量 4 和 7）：
<test_compare>2,4,7</test_compare>

- 提交方案判定（例如判定为方案A）：
<submit_scheme>A</submit_scheme>

- 正式替换（例如将工位 1 的产量正式重置为 6，并预测新效能指标值为 28）：
<formal_replace>1,6,28</formal_replace>

- 查询当前序列：
<query_sequence></query_sequence>

- 提交最终答案（确认完成分析）：
<answer>completed</answer>

## 胜负判定

胜利条件（需同时满足）：
1. 在进行至少两次试验替换后提交了方案判定
2. 完成两次正式替换，且每次的预测值均与实际值一致
3. 提交最终答案

失败条件（任一满足）：
1. 未达两次试验替换即提交方案判定
2. 两次正式替换中任一次预测不匹配
3. 超出最多2次正式替换
4. 格式错误或无效请求
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Automated assembly line production efficiency analysis and monitoring has been initiated.

The monitoring system has collected an initial production output sequence a[1..{n}] across {n} consecutive assembly stations. The initial sequence is: {sequence}.

The industrial control hub has secretly mounted an efficiency evaluation function F, which can only be one of the following four analysis schemes:
1. Scheme A (Total Output): Calculate the sum of production output across all stations
2. Scheme B (Station Synergy Fluctuation Sum): Calculate the sum of absolute differences in output between all adjacent stations (used to evaluate the smoothness of the assembly line tact time)
3. Scheme C (Dual-Pallet Output Stations): Count the number of stations with an even output (used to evaluate nodes suitable for dual-pallet concurrent routing)
4. Scheme D (Station-Weighted Capacity Index): Calculate the sum of products of each station's output and its station sequence number (starting from 1), reflecting the higher weight of backend stations on final capacity

Your goal is to identify the true efficiency evaluation function through queries and simulated adjustments, and verify your judgment through two formal output parameter resets with predictions.

You can repeatedly issue the following types of commands (one command at a time):

1. Query Current Value: Get the efficiency evaluation function value of the current output sequence
2. Test Replace: Temporarily adjust the output parameter of a station with a new value and see the efficiency value change (sequence restores after test)
3. Test Compare: Try two different output parameters at the same station and see their respective efficiency value changes (sequence restores after test)
4. Submit Scheme: Declare the efficiency evaluation scheme you believe is active (requires at least two test replacements first)
5. Formal Replace: Permanently reset the output parameter of a station and predict the new efficiency value (maximum twice, prediction required each time)
6. Query Sequence: Get the current real station output sequence (only available after formal replacements)

## Command Format (must strictly follow)

Each command can only contain one tag. Use the following XML format:

- Query current efficiency indicator value:
<query_value></query_value>

- Test replace (e.g., adjust station 3 output to 5):
<test_replace>3,5</test_replace>

- Test compare (e.g., try outputs 4 and 7 at station 2):
<test_compare>2,4,7</test_compare>

- Submit scheme (e.g., declare scheme A):
<submit_scheme>A</submit_scheme>

- Formal replace (e.g., formally reset station 1 output to 6, predicting new efficiency value 28):
<formal_replace>1,6,28</formal_replace>

- Query current sequence:
<query_sequence></query_sequence>

- Submit final answer (confirm completion):
<answer>completed</answer>

## Win/Loss Conditions

Victory conditions (all must be met):
1. Submit scheme determination after at least two test replacements
2. Complete two formal replacements with both predictions matching actual values
3. Submit final answer

Failure conditions (any one met):
1. Submit scheme determination before two test replacements
2. Any prediction mismatch in the two formal replacements
3. Exceed maximum of 2 formal replacements
4. Format error or invalid request
"""

    contextualized_rule_zh_5 = """\
司法案件量刑与违规记分审查程序启动。

司法辅助系统梳理了一组连续 {n} 个同类案件审查中的违规记分序列 a[1..{n}]，初始序列为：{sequence}。

审查后台秘密采用了一个综合裁量评估函数 F，它仅可能是以下四个量刑指导方案之一：
1. 方案A（累计总记分）：计算所有案件违规记分的总和
2. 方案B（裁量波动总和）：计算所有相邻审查案件之间记分差值的绝对值之和（用于审查裁量尺度的统一性）
3. 方案C（偶数记分案件数）：计算记分为偶数的案件个数（对接特定的标准罚金倍率统计算法）
4. 方案D（判例顺位加权记分）：计算每个案件的记分与其审理顺位（从1开始）的乘积之和，以体现最新判例对指导性指标的更大权重

你的目标是通过查询和模拟推演，识别出真实的裁量评估函数，并通过两次带预测的正式记分改判来验证你的判断。

你可以反复向系统提出以下类型的请求（每次仅限一个请求）：

1. 查询当前裁量指标：获取当前记分序列的评估函数值
2. 试验替换：临时调整某个案件的违规记分，查看裁量指标的变化（推演后序列会恢复原状）
3. 试验比较：对同一案件尝试两种不同的记分，分别查看裁量指标的变化（推演后序列会恢复原状）
4. 提交方案判定：声明你认为的裁量评估方案（需先完成至少两次试验替换）
5. 正式替换：永久改判某个案件的违规记分，并预测改判后的裁量指标值（最多两次，每次都需要预测）
6. 查询当前序列：获取当前真实的案件记分序列（仅在正式替换后可用）

## 请求格式（必须严格遵守）

每次请求只能包含一个标签。请使用以下 XML 格式：

- 查询当前裁量指标：
<query_value></query_value>

- 试验替换（例如将案件 3 的记分调整为 5）：
<test_replace>3,5</test_replace>

- 试验比较（例如在案件 2 分别尝试记分 4 和 7）：
<test_compare>2,4,7</test_compare>

- 提交方案判定（例如判定为方案A）：
<submit_scheme>A</submit_scheme>

- 正式替换（例如将案件 1 的记分正式改判为 6，并预测新裁量指标为 28）：
<formal_replace>1,6,28</formal_replace>

- 查询当前序列：
<query_sequence></query_sequence>

- 提交最终答案（确认完成审查）：
<answer>completed</answer>

## 胜负判定

胜利条件（需同时满足）：
1. 在进行至少两次试验替换后提交了方案判定
2. 完成两次正式替换，且每次的预测值均与实际值一致
3. 提交最终答案

失败条件（任一满足）：
1. 未达两次试验替换即提交方案判定
2. 两次正式替换中任一次预测不匹配
3. 超出最多2次正式替换
4. 格式错误或无效请求
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
The judicial case sentencing and violation penalty points review process has been initiated.

The judicial auxiliary system has compiled a sequence of violation penalty points a[1..{n}] from {n} consecutive similar case reviews. The initial sequence is: {sequence}.

The review backend has secretly applied a comprehensive discretionary evaluation function F, which can only be one of the following four sentencing guidance schemes:
1. Scheme A (Cumulative Total Points): Calculate the sum of penalty points across all cases
2. Scheme B (Discretionary Fluctuation Sum): Calculate the sum of absolute differences in penalty points between all adjacent reviewed cases (used to review the uniformity of discretionary standards)
3. Scheme C (Even Point Cases): Count the number of cases with even penalty points (aligning with specific standard fine multiplier statistical algorithms)
4. Scheme D (Precedence-Weighted Points): Calculate the sum of products of each case's penalty points and its review sequence number (starting from 1), to reflect the greater weight of recent precedents on the guiding indicator

Your goal is to identify the true discretionary evaluation function through queries and simulated deductions, and verify your judgment through two formal penalty point reassessments with predictions.

You can repeatedly make the following types of requests (one request at a time):

1. Query Current Value: Get the evaluation function value of the current penalty points sequence
2. Test Replace: Temporarily adjust the penalty points of a case with a new value and see the evaluation value change (sequence restores after deduction)
3. Test Compare: Try two different penalty points for the same case and see their respective evaluation value changes (sequence restores after deduction)
4. Submit Scheme: Declare the evaluation scheme you believe is active (requires at least two test replacements first)
5. Formal Replace: Permanently reassess the penalty points of a case and predict the new evaluation value (maximum twice, prediction required each time)
6. Query Sequence: Get the current real case penalty points sequence (only available after formal replacements)

## Request Format (must strictly follow)

Each request can only contain one tag. Use the following XML format:

- Query current discretionary indicator value:
<query_value></query_value>

- Test replace (e.g., adjust case 3 points to 5):
<test_replace>3,5</test_replace>

- Test compare (e.g., try points 4 and 7 in case 2):
<test_compare>2,4,7</test_compare>

- Submit scheme (e.g., declare scheme A):
<submit_scheme>A</submit_scheme>

- Formal replace (e.g., formally reassess case 1 points to 6, predicting new evaluation value 28):
<formal_replace>1,6,28</formal_replace>

- Query current sequence:
<query_sequence></query_sequence>

- Submit final answer (confirm completion):
<answer>completed</answer>

## Win/Loss Conditions

Victory conditions (all must be met):
1. Submit scheme determination after at least two test replacements
2. Complete two formal replacements with both predictions matching actual values
3. Submit final answer

Failure conditions (any one met):
1. Submit scheme determination before two test replacements
2. Any prediction mismatch in the two formal replacements
3. Exceed maximum of 2 formal replacements
4. Format error or invalid request
"""

    tags = ["answer", "query_value", "test_replace", "test_compare", "submit_scheme", "formal_replace", "query_sequence"]

    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 3,
                "sequence": [2, 3, 5],
                "function_type": "A",
            },
            2: {
                "n": 4,
                "sequence": [1, 4, 6, 8],
                "function_type": "C",
            },
            3: {
                "n": 5,
                "sequence": [3, 1, 4, 2, 5],
                "function_type": "D",
            },
            4: {
                "n": 6,
                "sequence": [5, 2, 8, 1, 6, 3],
                "function_type": "B",
            },
            5: {
                "n": 7,
                "sequence": [4, 7, 2, 9, 1, 5, 3],
                "function_type": "D",
            },
        },
        "en": {
            1: {
                "n": 3,
                "sequence": [2, 3, 5],
                "function_type": "A",
            },
            2: {
                "n": 4,
                "sequence": [1, 4, 6, 8],
                "function_type": "C",
            },
            3: {
                "n": 5,
                "sequence": [3, 1, 4, 2, 5],
                "function_type": "D",
            },
            4: {
                "n": 6,
                "sequence": [5, 2, 8, 1, 6, 3],
                "function_type": "B",
            },
            5: {
                "n": 7,
                "sequence": [4, 7, 2, 9, 1, 5, 3],
                "function_type": "D",
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
        self._game_info["n"] = cfg["n"]
        self._game_info["sequence"] = str(cfg["sequence"])
        
        # 初始化游戏状态
        self.sequence = cfg["sequence"].copy()  # 当前序列
        self.function_type = cfg["function_type"]  # 真实函数类型
        self.test_count = 0  # 试验替换次数
        self.formal_count = 0  # 正式替换次数
        self.scheme_submitted = False  # 是否已提交方案判定
        self.scheme_correct = False  # 方案判定是否正确
        self.predictions_correct = []  # 正式替换预测是否正确

    def _calculate_function(self, seq):
        """计算给定序列的函数值"""
        if self.function_type == "A":
            # 方案A：总和
            return sum(seq)
        elif self.function_type == "B":
            # 方案B：相邻差总和
            return sum(abs(seq[i+1] - seq[i]) for i in range(len(seq) - 1))
        elif self.function_type == "C":
            # 方案C：偶数计数
            return sum(1 for x in seq if x % 2 == 0)
        elif self.function_type == "D":
            # 方案D：位置加权和（位置从1开始）
            return sum((i+1) * seq[i] for i in range(len(seq)))
        else:
            raise ValueError(f"Unknown function type: {self.function_type}")

    def evaluate(self, parsed_info):
        """评估最终答案"""
        # 检查是否满足胜利条件
        if not self.scheme_submitted:
            return False
        if not self.scheme_correct:
            return False
        if self.formal_count != 2:
            return False
        if len(self.predictions_correct) != 2:
            return False
        if not all(self.predictions_correct):
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """生成游戏响应"""
        lang = self.config.language
        
        # 1. 查询当前函数值
        if "query_value" in parsed_info:
            current_value = self._calculate_function(self.sequence)
            if lang == "zh":
                return f"当前函数值为：{current_value}"
            else:
                return f"Current function value: {current_value}"

        # 2. 试验替换
        elif "test_replace" in parsed_info:
            parts = parsed_info["test_replace"].split(",")
            if len(parts) != 2:
                raise ValueError("test_replace requires exactly 2 comma-separated values: position,value")
            pos = int(parts[0].strip()) - 1  # 转为0索引
            val = int(parts[1].strip())
            
            if pos < 0 or pos >= len(self.sequence):
                raise ValueError(f"Position {pos+1} out of range [1, {len(self.sequence)}]")
            
            # 计算当前值
            current_value = self._calculate_function(self.sequence)
            
            # 临时替换并计算新值
            old_val = self.sequence[pos]
            temp_seq = self.sequence.copy()
            temp_seq[pos] = val
            new_value = self._calculate_function(temp_seq)
            delta = new_value - current_value
            
            # 记录试验次数
            self.test_count += 1
            
            if lang == "zh":
                return f"试验结果：新函数值为 {new_value}，变化量为 {delta}（{new_value} - {current_value}）"
            else:
                return f"Test result: New value is {new_value}, change is {delta} ({new_value} - {current_value})"

        # 3. 试验比较
        elif "test_compare" in parsed_info:
            parts = parsed_info["test_compare"].split(",")
            if len(parts) != 3:
                raise ValueError("test_compare requires exactly 3 comma-separated values: position,value1,value2")
            pos = int(parts[0].strip()) - 1  # 转为0索引
            val1 = int(parts[1].strip())
            val2 = int(parts[2].strip())
            
            if pos < 0 or pos >= len(self.sequence):
                raise ValueError(f"Position {pos+1} out of range [1, {len(self.sequence)}]")
            
            # 计算当前值
            current_value = self._calculate_function(self.sequence)
            
            # 第一次试验
            temp_seq1 = self.sequence.copy()
            temp_seq1[pos] = val1
            new_value1 = self._calculate_function(temp_seq1)
            delta1 = new_value1 - current_value
            
            # 第二次试验
            temp_seq2 = self.sequence.copy()
            temp_seq2[pos] = val2
            new_value2 = self._calculate_function(temp_seq2)
            delta2 = new_value2 - current_value
            
            # 记录试验次数（算两次）
            self.test_count += 2
            
            if lang == "zh":
                return (f"比较结果：\n"
                       f"替换为 {val1}：新函数值 {new_value1}，变化量 {delta1}\n"
                       f"替换为 {val2}：新函数值 {new_value2}，变化量 {delta2}")
            else:
                return (f"Comparison result:\n"
                       f"Replace with {val1}: New value {new_value1}, change {delta1}\n"
                       f"Replace with {val2}: New value {new_value2}, change {delta2}")

        # 4. 提交方案判定
        elif "submit_scheme" in parsed_info:
            scheme = parsed_info["submit_scheme"].strip().upper()
            
            if scheme not in ["A", "B", "C", "D"]:
                raise ValueError("Scheme must be one of A, B, C, or D.")
            
            if self.test_count < 2:
                raise ValueError(
                    f"At least two test replacements required before submitting scheme. "
                    f"Current tests: {self.test_count}"
                )
            
            self.scheme_submitted = True
            self.scheme_correct = (scheme == self.function_type)
            
            if lang == "zh":
                return f"已记录你的判定：方案{scheme}。请继续进行正式替换以验证你的判断。"
            else:
                return f"Your determination recorded: Scheme {scheme}. Please proceed with formal replacements to verify."

        # 5. 正式替换
        elif "formal_replace" in parsed_info:
            parts = parsed_info["formal_replace"].split(",")
            if len(parts) != 3:
                raise ValueError("Formal replace requires exactly 3 comma-separated values: position,value,prediction")
            
            pos = int(parts[0].strip()) - 1  # 转为0索引
            val = int(parts[1].strip())
            pred = int(parts[2].strip())
            
            if pos < 0 or pos >= len(self.sequence):
                raise ValueError("Position out of range")
            
            if self.formal_count >= 2:
                raise ValueError("Maximum 2 formal replacements already reached.")
            
            # 执行正式替换
            self.sequence[pos] = val
            actual_value = self._calculate_function(self.sequence)
            is_correct = (pred == actual_value)
            
            self.formal_count += 1
            self.predictions_correct.append(is_correct)
            
            if not is_correct:
                raise ValueError(
                    f"Prediction mismatch: predicted {pred}, actual {actual_value}."
                )
            
            if lang == "zh":
                return (f"正式替换完成（{self.formal_count}/2）。\n"
                       f"实际函数值：{actual_value}\n"
                       f"预测正确！")
            else:
                return (f"Formal replacement completed ({self.formal_count}/2).\n"
                       f"Actual function value: {actual_value}\n"
                       f"Prediction correct!")

        # 6. 查询当前序列
        elif "query_sequence" in parsed_info:
            if self.formal_count == 0:
                if lang == "zh":
                    return "错误：仅在正式替换后可查询当前序列。"
                else:
                    return "Error: Can only query sequence after formal replacements."
            
            if lang == "zh":
                return f"当前序列：{self.sequence}"
            else:
                return f"Current sequence: {self.sequence}"

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确响应中的数值部分做偏移，以产生看起来合理但错误的答案。
        """
        # 找到响应中的所有整数（含负数），将第一个数值 +1
        def _offset_first_number(text):
            def _replacer(m):
                _replacer.called = True
                return str(int(m.group()) + 1)
            _replacer.called = False
            result = re.sub(r'-?\d+', _replacer, text, count=1)
            return result if _replacer.called else text + " [WRONG]"
        
        return _offset_first_number(correct)

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        n = len(self.sequence)
        
        # 保存当前状态，防止污染
        saved_test_count = self.test_count
        saved_formal_count = self.formal_count
        saved_scheme_submitted = self.scheme_submitted
        saved_scheme_correct = self.scheme_correct
        saved_predictions_correct = self.predictions_correct[:]
        saved_sequence = self.sequence.copy()
        
        # 辅助函数：执行查询并恢复状态
        def run_query(parsed_info, override_test_count=None):
            if override_test_count is not None:
                self.test_count = override_test_count
            
            try:
                # 调用 _cf_core_produce 直接获取逻辑结果，绕过反事实计数器
                response = self._cf_core_produce(parsed_info)
            except Exception as e:
                response = f"Error: {str(e)}"
            
            # 恢复状态
            self.test_count = saved_test_count
            self.formal_count = saved_formal_count
            self.scheme_submitted = saved_scheme_submitted
            self.scheme_correct = saved_scheme_correct
            self.predictions_correct = saved_predictions_correct[:]
            self.sequence = saved_sequence.copy()
            return response

        # 1. 查询当前函数值
        queries.append({
            "query": "<query_value></query_value>",
            "answer": run_query({"query_value": ""})
        })
        
        # 定义枚举值的范围 (0-9，覆盖基础测试用例)
        val_range = range(10)

        # 2. 试验替换
        for pos in range(1, n + 1):
            for val in val_range:
                query_str = f"<test_replace>{pos},{val}</test_replace>"
                parsed = {"test_replace": f"{pos},{val}"}
                queries.append({
                    "query": query_str,
                    "answer": run_query(parsed)
                })

        # 3. 试验比较
        # 枚举位置、值1、值2。
        for pos in range(1, n + 1):
            for v1 in val_range:
                for v2 in val_range:
                    if v1 == v2: continue # 跳过相同值比较
                    query_str = f"<test_compare>{pos},{v1},{v2}</test_compare>"
                    parsed = {"test_compare": f"{pos},{v1},{v2}"}
                    queries.append({
                        "query": query_str,
                        "answer": run_query(parsed)
                    })

        # 4. 提交方案判定
        for scheme in ["A", "B", "C", "D"]:
            query_str = f"<submit_scheme>{scheme}</submit_scheme>"
            parsed = {"submit_scheme": scheme}
            queries.append({
                "query": query_str,
                "answer": run_query(parsed, override_test_count=2)
            })
            
        return queries