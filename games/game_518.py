# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个N节点的树。
# 知识点:   树的宽度：树中某层/最宽一层有多少个节点
# ============================================================

from .base import Game
import re


class SequenceMultiplierGame(Game):

    game_rule_zh = """\
我们来玩一个"序列乘子推理"游戏，规则如下：

游戏设定了一个整数序列 W(d)，索引 d 属于集合 {{0, 1, ..., {H}}}，其中 W(0) = 1。

存在一个未知的周期 T，T 可能是 2、3、4 或 5。同时存在一个未知的整数乘子序列 f[0], f[1], ..., f[T-1]，每个乘子 f[k] 的取值范围是 1 到 4 之间的整数。

对于任意索引 d（0 小于等于 d 小于 {H}），序列满足递推关系：
W(d+1) = W(d) × f[d mod T]

也就是说，每一步的值等于上一步的值乘以对应周期位置的乘子。

游戏参数：
- H = {H}：序列的最大索引
- L* = {L_star}：目标索引（这是你需要预测其值的索引，但不能直接查询它）
- B = {B}：数值查询的次数上限

你的目标是：在不超过预算次数的前提下，通过查询其他索引的值，推断出 W(L*) 的准确数值。

你可以进行以下操作：

1. 数值查询（会消耗查询次数）：查询某个索引 L 的值
   - 约束：L 必须是 0 到 {H} 之间的整数，且 L 不能等于 {L_star}
   - 返回：W(L) 的精确整数值，以及剩余的查询次数
   - 注意：如果你查询 L = {L_star}，将被视为违规，游戏直接失败

2. 预算查询（不消耗查询次数）：询问当前剩余的数值查询次数
   - 返回：剩余查询次数的整数

3. 参数查询（不消耗查询次数）：询问游戏参数 H、L*、B
   - 返回：这三个参数的当前值

4. 最终提交（不消耗查询次数）：提交你对目标索引值的预测
   - 必须指定索引为 {L_star}，并给出预测值
   - 如果预测正确，游戏成功；否则游戏失败

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 数值查询（例如查询索引 5 的值）：
<query_value>5</query_value>

- 预算查询（查询剩余次数）：
<query_budget></query_budget>

- 参数查询（查询 H、L*、B）：
<query_params></query_params>

- 最终提交（例如预测索引 {L_star} 的值为 1024）：
<answer>index={L_star}, value=1024</answer>

注意：提交答案时，索引必须等于 {L_star}，否则提交无效。
"""

    game_rule_en = """\
Let's play a "Sequence Multiplier Inference" game. Here are the rules:

There is an integer sequence W(d) with index d in the set {{0, 1, ..., {H}}}, where W(0) = 1.

There exists an unknown period T, which can be 2, 3, 4, or 5. There also exists an unknown integer multiplier sequence f[0], f[1], ..., f[T-1], where each multiplier f[k] is an integer between 1 and 4.

For any index d (0 less than or equal to d less than {H}), the sequence follows the recurrence relation:
W(d+1) = W(d) × f[d mod T]

That is, each step's value equals the previous step's value multiplied by the corresponding multiplier at that period position.

Game parameters:
- H = {H}: maximum index of the sequence
- L* = {L_star}: target index (the index whose value you need to predict, but cannot directly query)
- B = {B}: maximum number of value queries allowed

Your goal is: within the query budget, infer the exact value of W(L*) by querying values at other indices.

You can perform the following operations:

1. Value Query (consumes a query count): query the value at index L
   - Constraint: L must be an integer between 0 and {H}, and L cannot equal {L_star}
   - Returns: the exact integer value W(L) and the remaining query count
   - Note: if you query L = {L_star}, it is a violation and the game fails immediately

2. Budget Query (does not consume a query count): ask for the remaining number of value queries
   - Returns: an integer representing the remaining query count

3. Parameters Query (does not consume a query count): ask for the game parameters H, L*, B
   - Returns: the current values of these three parameters

4. Final Submission (does not consume a query count): submit your prediction for the target index value
   - Must specify index as {L_star} and provide the predicted value
   - If the prediction is correct, the game succeeds; otherwise, it fails

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag. Use the following XML format:

- Value Query (e.g., query value at index 5):
<query_value>5</query_value>

- Budget Query (query remaining count):
<query_budget></query_budget>

- Parameters Query (query H, L*, B):
<query_params></query_params>

- Final Submission (e.g., predict value at index {L_star} is 1024):
<answer>index={L_star}, value=1024</answer>

Note: when submitting an answer, the index must equal {L_star}, otherwise the submission is invalid.
"""

    contextualized_rule_zh_1 = """\
我们来操作“交通枢纽流量预测系统”，规则如下：

系统记录了一个交通流量基数序列 W(d)，天数索引 d 属于集合 {{0, 1, ..., {H}}}，其中初始日流量 W(0) = 1。

该枢纽存在一个未知的交通潮汐周期 T，T 可能是 2、3、4 或 5 天。同时存在一个未知的日流量放大乘子序列 f[0], f[1], ..., f[T-1]，每个乘子 f[k] 的取值范围是 1 到 4 之间的整数。

对于任意天数 d（0 小于等于 d 小于 {H}），流量基数满足递推关系：
W(d+1) = W(d) × f[d mod T]

也就是说，明天的流量基数等于今天的流量基数乘以该潮汐周期特定位置的放大乘子。

系统参数：
- H = {H}：流量监控的最大天数索引
- L* = {L_star}：目标预测天数（这是你需要预测其流量的索引，但不能直接查询它）
- B = {B}：系统允许的历史流量查询次数上限

你的目标是：在不超过预算次数的前提下，通过查询其他天数的流量基数，推断出第 L* 天的确切流量基数 W(L*)。

你可以进行以下操作：

1. 数值查询（会消耗查询次数）：查询某一天数 L 的流量值
   - 约束：L 必须是 0 到 {H} 之间的整数，且 L 不能等于 {L_star}
   - 返回：W(L) 的精确整数值，以及剩余的查询次数
   - 注意：如果你查询 L = {L_star}，将被视为违规，系统将锁定并导致任务失败

2. 预算查询（不消耗查询次数）：询问当前剩余的流量查询次数
   - 返回：剩余查询次数的整数

3. 参数查询（不消耗查询次数）：询问系统参数 H、L*、B
   - 返回：这三个参数的当前值

4. 最终提交（不消耗查询次数）：提交你对目标天数流量基数的预测
   - 必须指定索引为 {L_star}，并给出预测值
   - 如果预测正确，任务成功；否则任务失败

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 数值查询（例如查询天数 5 的流量值）：
<query_value>5</query_value>

- 预算查询（查询剩余次数）：
<query_budget></query_budget>

- 参数查询（查询 H、L*、B）：
<query_params></query_params>

- 最终提交（例如预测天数 {L_star} 的流量值为 1024）：
<answer>index={L_star}, value=1024</answer>

注意：提交答案时，索引必须等于 {L_star}，否则提交无效。
"""

    contextualized_rule_en_1 = """\
[Transport Scenario]
Let's operate the "Traffic Hub Flow Prediction System". Here are the rules:

The system records a traffic flow base sequence W(d) with the day index d in the set {{0, 1, ..., {H}}}, where the initial daily flow W(0) = 1.

The hub has an unknown traffic tidal period T, which can be 2, 3, 4, or 5 days. There also exists an unknown daily flow multiplier sequence f[0], f[1], ..., f[T-1], where each multiplier f[k] is an integer between 1 and 4.

For any day d (0 less than or equal to d less than {H}), the flow base follows the recurrence relation:
W(d+1) = W(d) × f[d mod T]

That is, tomorrow's flow base equals today's flow base multiplied by the corresponding multiplier at that position in the tidal period.

System parameters:
- H = {H}: maximum day index for flow monitoring
- L* = {L_star}: target prediction day (the index whose flow you need to predict, but cannot directly query)
- B = {B}: maximum number of historical flow queries allowed

Your goal is: within the query budget, infer the exact traffic flow base W(L*) for day L* by querying the flow values at other days.

You can perform the following operations:

1. Value Query (consumes a query count): query the flow value at day L
   - Constraint: L must be an integer between 0 and {H}, and L cannot equal {L_star}
   - Returns: the exact integer value W(L) and the remaining query count
   - Note: if you query L = {L_star}, it is a violation and the system locks, causing immediate failure

2. Budget Query (does not consume a query count): ask for the remaining number of flow queries
   - Returns: an integer representing the remaining query count

3. Parameters Query (does not consume a query count): ask for the system parameters H, L*, B
   - Returns: the current values of these three parameters

4. Final Submission (does not consume a query count): submit your prediction for the target day's flow base
   - Must specify index as {L_star} and provide the predicted value
   - If the prediction is correct, the task succeeds; otherwise, it fails

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag. Use the following XML format:

- Value Query (e.g., query flow value at day 5):
<query_value>5</query_value>

- Budget Query (query remaining count):
<query_budget></query_budget>

- Parameters Query (query H, L*, B):
<query_params></query_params>

- Final Submission (e.g., predict flow value at day {L_star} is 1024):
<answer>index={L_star}, value=1024</answer>

Note: when submitting an answer, the index must equal {L_star}, otherwise the submission is invalid.
"""

    contextualized_rule_zh_2 = """\
我们来操作“病原体增殖追踪系统”，规则如下：

系统记录了一个病原体浓度序列 W(d)，培养周期索引 d 属于集合 {{0, 1, ..., {H}}}，其中初始浓度 W(0) = 1。

病原体存在一个未知的突变周期 T，T 可能是 2、3、4 或 5 个培养周期。同时存在一个未知的浓度繁殖倍率序列 f[0], f[1], ..., f[T-1]，每个倍率 f[k] 的取值范围是 1 到 4 之间的整数。

对于任意周期索引 d（0 小于等于 d 小于 {H}），浓度满足递推关系：
W(d+1) = W(d) × f[d mod T]

也就是说，下一个培养周期的浓度等于上一个周期的浓度乘以突变周期内对应阶段的繁殖倍率。

系统参数：
- H = {H}：培养监控的最大周期索引
- L* = {L_star}：目标预测周期（这是你需要预测其浓度的索引，但不能直接查询它）
- B = {B}：系统允许的浓度采样查询次数上限

你的目标是：在不超过预算次数的前提下，通过查询其他培养周期的浓度，推断出目标周期 L* 的确切病原体浓度 W(L*)。

你可以进行以下操作：

1. 数值查询（会消耗查询次数）：采样查询某个培养周期 L 的浓度
   - 约束：L 必须是 0 到 {H} 之间的整数，且 L 不能等于 {L_star}
   - 返回：W(L) 的精确整数值，以及剩余的查询次数
   - 注意：如果你查询 L = {L_star}，将被视为违规操作，导致样本污染，任务直接失败

2. 预算查询（不消耗查询次数）：询问当前剩余的采样查询次数
   - 返回：剩余查询次数的整数

3. 参数查询（不消耗查询次数）：询问系统参数 H、L*、B
   - 返回：这三个参数的当前值

4. 最终提交（不消耗查询次数）：提交你对目标培养周期浓度的预测
   - 必须指定索引为 {L_star}，并给出预测值
   - 如果预测正确，诊断成功；否则诊断失败

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 数值查询（例如查询周期 5 的浓度）：
<query_value>5</query_value>

- 预算查询（查询剩余次数）：
<query_budget></query_budget>

- 参数查询（查询 H、L*、B）：
<query_params></query_params>

- 最终提交（例如预测周期 {L_star} 的浓度值为 1024）：
<answer>index={L_star}, value=1024</answer>

注意：提交答案时，索引必须等于 {L_star}，否则提交无效。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's operate the "Pathogen Proliferation Tracking System". Here are the rules:

The system records a pathogen concentration sequence W(d) with the culture period index d in the set {{0, 1, ..., {H}}}, where the initial concentration W(0) = 1.

The pathogen has an unknown mutation cycle T, which can be 2, 3, 4, or 5 culture periods. There also exists an unknown concentration reproduction rate sequence f[0], f[1], ..., f[T-1], where each rate f[k] is an integer between 1 and 4.

For any period index d (0 less than or equal to d less than {H}), the concentration follows the recurrence relation:
W(d+1) = W(d) × f[d mod T]

That is, the concentration in the next culture period equals the previous period's concentration multiplied by the reproduction rate at the corresponding stage of the mutation cycle.

System parameters:
- H = {H}: maximum period index for culture monitoring
- L* = {L_star}: target prediction period (the index whose concentration you need to predict, but cannot directly query)
- B = {B}: maximum number of concentration sampling queries allowed

Your goal is: within the query budget, infer the exact pathogen concentration W(L*) for the target period L* by querying concentrations at other periods.

You can perform the following operations:

1. Value Query (consumes a query count): sample query the concentration at period L
   - Constraint: L must be an integer between 0 and {H}, and L cannot equal {L_star}
   - Returns: the exact integer value W(L) and the remaining query count
   - Note: if you query L = {L_star}, it is a violation leading to sample contamination, and the task fails immediately

2. Budget Query (does not consume a query count): ask for the remaining number of sampling queries
   - Returns: an integer representing the remaining query count

3. Parameters Query (does not consume a query count): ask for the system parameters H, L*, B
   - Returns: the current values of these three parameters

4. Final Submission (does not consume a query count): submit your prediction for the target culture period's concentration
   - Must specify index as {L_star} and provide the predicted value
   - If the prediction is correct, the diagnosis succeeds; otherwise, it fails

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag. Use the following XML format:

- Value Query (e.g., query concentration at period 5):
<query_value>5</query_value>

- Budget Query (query remaining count):
<query_budget></query_budget>

- Parameters Query (query H, L*, B):
<query_params></query_params>

- Final Submission (e.g., predict concentration at period {L_star} is 1024):
<answer>index={L_star}, value=1024</answer>

Note: when submitting an answer, the index must equal {L_star}, otherwise the submission is invalid.
"""

    contextualized_rule_zh_3 = """\
我们来使用“学生知识点掌握度评估系统”，规则如下：

系统记录了一个学习指数序列 W(d)，课时索引 d 属于集合 {{0, 1, ..., {H}}}，其中初始学习指数 W(0) = 1。

学生的认知存在一个未知的记忆周期 T，T 可能是 2、3、4 或 5 个课时。同时存在一个未知的知识吸收倍率序列 f[0], f[1], ..., f[T-1]，每个倍率 f[k] 的取值范围是 1 到 4 之间的整数。

对于任意课时 d（0 小于等于 d 小于 {H}），学习指数满足递推关系：
W(d+1) = W(d) × f[d mod T]

也就是说，下一课时的学习指数等于上一课时的指数乘以该记忆周期特定阶段的知识吸收倍率。

系统参数：
- H = {H}：教学追踪的最大课时索引
- L* = {L_star}：目标评估课时（这是你需要预测其学习指数的索引，但不能直接查询它）
- B = {B}：系统允许的历史水平测试查询次数上限

你的目标是：在不超过预算次数的前提下，通过查询其他课时的学习指数，推断出第 L* 课时的确切学习指数 W(L*)。

你可以进行以下操作：

1. 数值查询（会消耗查询次数）：查询某个课时 L 的学习指数
   - 约束：L 必须是 0 到 {H} 之间的整数，且 L 不能等于 {L_star}
   - 返回：W(L) 的精确整数值，以及剩余的查询次数
   - 注意：如果你查询 L = {L_star}，将被视为过度测验，导致系统锁定并评估失败

2. 预算查询（不消耗查询次数）：询问当前剩余的测试查询次数
   - 返回：剩余查询次数的整数

3. 参数查询（不消耗查询次数）：询问系统参数 H、L*、B
   - 返回：这三个参数的当前值

4. 最终提交（不消耗查询次数）：提交你对目标课时学习指数的预测
   - 必须指定索引为 {L_star}，并给出预测值
   - 如果预测正确，评估成功；否则评估失败

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 数值查询（例如查询课时 5 的学习指数）：
<query_value>5</query_value>

- 预算查询（查询剩余次数）：
<query_budget></query_budget>

- 参数查询（查询 H、L*、B）：
<query_params></query_params>

- 最终提交（例如预测课时 {L_star} 的学习指数为 1024）：
<answer>index={L_star}, value=1024</answer>

注意：提交答案时，索引必须等于 {L_star}，否则提交无效。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's use the "Student Knowledge Mastery Assessment System". Here are the rules:

The system records a learning index sequence W(d) with the lesson index d in the set {{0, 1, ..., {H}}}, where the initial learning index W(0) = 1.

The student's cognition has an unknown memory cycle T, which can be 2, 3, 4, or 5 lessons. There also exists an unknown knowledge absorption rate sequence f[0], f[1], ..., f[T-1], where each rate f[k] is an integer between 1 and 4.

For any lesson d (0 less than or equal to d less than {H}), the learning index follows the recurrence relation:
W(d+1) = W(d) × f[d mod T]

That is, the learning index of the next lesson equals the previous lesson's index multiplied by the absorption rate at that specific stage of the memory cycle.

System parameters:
- H = {H}: maximum lesson index for teaching tracking
- L* = {L_star}: target assessment lesson (the index whose learning index you need to predict, but cannot directly query)
- B = {B}: maximum number of historical proficiency test queries allowed

Your goal is: within the query budget, infer the exact learning index W(L*) for lesson L* by querying indices at other lessons.

You can perform the following operations:

1. Value Query (consumes a query count): query the learning index at lesson L
   - Constraint: L must be an integer between 0 and {H}, and L cannot equal {L_star}
   - Returns: the exact integer value W(L) and the remaining query count
   - Note: if you query L = {L_star}, it is treated as over-testing, which locks the system and fails the assessment

2. Budget Query (does not consume a query count): ask for the remaining number of test queries
   - Returns: an integer representing the remaining query count

3. Parameters Query (does not consume a query count): ask for the system parameters H, L*, B
   - Returns: the current values of these three parameters

4. Final Submission (does not consume a query count): submit your prediction for the target lesson's learning index
   - Must specify index as {L_star} and provide the predicted value
   - If the prediction is correct, the assessment succeeds; otherwise, it fails

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag. Use the following XML format:

- Value Query (e.g., query learning index at lesson 5):
<query_value>5</query_value>

- Budget Query (query remaining count):
<query_budget></query_budget>

- Parameters Query (query H, L*, B):
<query_params></query_params>

- Final Submission (e.g., predict learning index at lesson {L_star} is 1024):
<answer>index={L_star}, value=1024</answer>

Note: when submitting an answer, the index must equal {L_star}, otherwise the submission is invalid.
"""

    contextualized_rule_zh_4 = """\
我们来操作“自动化产线产能推演系统”，规则如下：

系统记录了一个产出量序列 W(d)，工序层级索引 d 属于集合 {{0, 1, ..., {H}}}，其中第一道基础工序产出 W(0) = 1。

流水线存在一个未知的机器运作周期 T，T 可能是 2、3、4 或 5 道工序。同时存在一个未知的产能放大系数序列 f[0], f[1], ..., f[T-1]，每个系数 f[k] 的取值范围是 1 到 4 之间的整数。

对于任意工序 d（0 小于等于 d 小于 {H}），产出量满足递推关系：
W(d+1) = W(d) × f[d mod T]

也就是说，下一道工序的产出量等于上一道工序的产出量乘以机器运作周期内对应节点的放大系数。

系统参数：
- H = {H}：产线记录的最大工序层级
- L* = {L_star}：目标预测工序（这是你需要预测其产出量的层级，但不能直接查询它）
- B = {B}：系统允许的质检采样查询次数上限

你的目标是：在不超过预算次数的前提下，通过查询其他工序的产出量，推断出第 L* 道工序的确切产出量 W(L*)。

你可以进行以下操作：

1. 数值查询（会消耗查询次数）：查询某道工序 L 的产出量
   - 约束：L 必须是 0 到 {H} 之间的整数，且 L 不能等于 {L_star}
   - 返回：W(L) 的精确整数值，以及剩余的查询次数
   - 注意：如果你查询 L = {L_star}，将触发安全警报并导致生产线停机，推演直接失败

2. 预算查询（不消耗查询次数）：询问当前剩余的采样查询次数
   - 返回：剩余查询次数的整数

3. 参数查询（不消耗查询次数）：询问系统参数 H、L*、B
   - 返回：这三个参数的当前值

4. 最终提交（不消耗查询次数）：提交你对目标工序产出量的预测
   - 必须指定索引为 {L_star}，并给出预测值
   - 如果预测正确，推演成功；否则推演失败

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 数值查询（例如查询工序 5 的产出量）：
<query_value>5</query_value>

- 预算查询（查询剩余次数）：
<query_budget></query_budget>

- 参数查询（查询 H、L*、B）：
<query_params></query_params>

- 最终提交（例如预测工序 {L_star} 的产出量为 1024）：
<answer>index={L_star}, value=1024</answer>

注意：提交答案时，索引必须等于 {L_star}，否则提交无效。
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Let's operate the "Automated Production Line Capacity Deduction System". Here are the rules:

The system records an output sequence W(d) with the process level index d in the set {{0, 1, ..., {H}}}, where the initial base process output W(0) = 1.

The assembly line has an unknown machine operation cycle T, which can be 2, 3, 4, or 5 processes. There also exists an unknown capacity amplification coefficient sequence f[0], f[1], ..., f[T-1], where each coefficient f[k] is an integer between 1 and 4.

For any process d (0 less than or equal to d less than {H}), the output follows the recurrence relation:
W(d+1) = W(d) × f[d mod T]

That is, the output of the next process equals the previous process's output multiplied by the amplification coefficient at the corresponding node in the machine operation cycle.

System parameters:
- H = {H}: maximum process level recorded on the line
- L* = {L_star}: target prediction process (the level whose output you need to predict, but cannot directly query)
- B = {B}: maximum number of quality inspection sampling queries allowed

Your goal is: within the query budget, infer the exact output W(L*) for process L* by querying outputs at other processes.

You can perform the following operations:

1. Value Query (consumes a query count): query the output at process L
   - Constraint: L must be an integer between 0 and {H}, and L cannot equal {L_star}
   - Returns: the exact integer value W(L) and the remaining query count
   - Note: if you query L = {L_star}, it triggers a safety alarm causing the production line to halt, and the deduction fails immediately

2. Budget Query (does not consume a query count): ask for the remaining number of sampling queries
   - Returns: an integer representing the remaining query count

3. Parameters Query (does not consume a query count): ask for the system parameters H, L*, B
   - Returns: the current values of these three parameters

4. Final Submission (does not consume a query count): submit your prediction for the target process's output
   - Must specify index as {L_star} and provide the predicted value
   - If the prediction is correct, the deduction succeeds; otherwise, it fails

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag. Use the following XML format:

- Value Query (e.g., query output at process 5):
<query_value>5</query_value>

- Budget Query (query remaining count):
<query_budget></query_budget>

- Parameters Query (query H, L*, B):
<query_params></query_params>

- Final Submission (e.g., predict output at process {L_star} is 1024):
<answer>index={L_star}, value=1024</answer>

Note: when submitting an answer, the index must equal {L_star}, otherwise the submission is invalid.
"""

    contextualized_rule_zh_5 = """\
我们来操作“案件证据链效力推演系统”，规则如下：

系统记录了一个法律效力指数序列 W(d)，证据传导层级 d 属于集合 {{0, 1, ..., {H}}}，其中初始核心证据的效力 W(0) = 1。

司法审查存在一个未知的流程周期 T，T 可能是 2、3、4 或 5 个层级。同时存在一个未知的效力放大系数序列 f[0], f[1], ..., f[T-1]，每个系数 f[k] 的取值范围是 1 到 4 之间的整数。

对于任意传导层级 d（0 小于等于 d 小于 {H}），效力指数满足递推关系：
W(d+1) = W(d) × f[d mod T]

也就是说，下一级传导的效力等于上一级效力乘以审查周期内对应环节的放大系数。

系统参数：
- H = {H}：证据追踪的最大传导层级
- L* = {L_star}：目标推演层级（这是你需要预测其效力指数的层级，但不能直接查询它）
- B = {B}：系统允许的卷宗调阅次数上限

你的目标是：在不超过预算次数的前提下，通过调阅其他层级的效力指数，推断出第 L* 级证据的确切效力指数 W(L*)。

你可以进行以下操作：

1. 数值查询（会消耗查询次数）：调阅某一层级 L 的效力指数
   - 约束：L 必须是 0 到 {H} 之间的整数，且 L 不能等于 {L_star}
   - 返回：W(L) 的精确整数值，以及剩余的查询次数
   - 注意：如果你越权调阅 L = {L_star}，将被视为违规干预司法，系统将封锁并导致推演失败

2. 预算查询（不消耗查询次数）：询问当前剩余的调阅次数
   - 返回：剩余查询次数的整数

3. 参数查询（不消耗查询次数）：询问系统参数 H、L*、B
   - 返回：这三个参数的当前值

4. 最终提交（不消耗查询次数）：提交你对目标层级效力指数的预测
   - 必须指定索引为 {L_star}，并给出预测值
   - 如果预测正确，推演成功；否则推演失败

## 查询与提交格式（必须严格遵守）

每次只能包含一个操作标签。请使用以下 XML 格式：

- 数值查询（例如查询层级 5 的效力指数）：
<query_value>5</query_value>

- 预算查询（查询剩余次数）：
<query_budget></query_budget>

- 参数查询（查询 H、L*、B）：
<query_params></query_params>

- 最终提交（例如预测层级 {L_star} 的效力指数为 1024）：
<answer>index={L_star}, value=1024</answer>

注意：提交答案时，索引必须等于 {L_star}，否则提交无效。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's operate the "Case Evidence Chain Validity Deduction System". Here are the rules:

The system records a legal validity index sequence W(d) with the evidence transmission level d in the set {{0, 1, ..., {H}}}, where the initial core evidence validity W(0) = 1.

The judicial review has an unknown process cycle T, which can be 2, 3, 4, or 5 levels. There also exists an unknown validity amplification coefficient sequence f[0], f[1], ..., f[T-1], where each coefficient f[k] is an integer between 1 and 4.

For any transmission level d (0 less than or equal to d less than {H}), the validity index follows the recurrence relation:
W(d+1) = W(d) × f[d mod T]

That is, the validity of the next transmission level equals the previous level's validity multiplied by the amplification coefficient at the corresponding stage of the review cycle.

System parameters:
- H = {H}: maximum transmission level for evidence tracking
- L* = {L_star}: target deduction level (the level whose validity index you need to predict, but cannot directly query)
- B = {B}: maximum number of dossier access queries allowed

Your goal is: within the query budget, infer the exact validity index W(L*) for level L* by accessing indices at other levels.

You can perform the following operations:

1. Value Query (consumes a query count): access the validity index at level L
   - Constraint: L must be an integer between 0 and {H}, and L cannot equal {L_star}
   - Returns: the exact integer value W(L) and the remaining query count
   - Note: if you access L = {L_star} without authorization, it is treated as illegal judicial interference, causing system lockdown and immediate failure

2. Budget Query (does not consume a query count): ask for the remaining number of access queries
   - Returns: an integer representing the remaining query count

3. Parameters Query (does not consume a query count): ask for the system parameters H, L*, B
   - Returns: the current values of these three parameters

4. Final Submission (does not consume a query count): submit your prediction for the target level's validity index
   - Must specify index as {L_star} and provide the predicted value
   - If the prediction is correct, the deduction succeeds; otherwise, it fails

## Query and Submission Format (must strictly follow)

Each operation must contain only one tag. Use the following XML format:

- Value Query (e.g., query validity index at level 5):
<query_value>5</query_value>

- Budget Query (query remaining count):
<query_budget></query_budget>

- Parameters Query (query H, L*, B):
<query_params></query_params>

- Final Submission (e.g., predict validity index at level {L_star} is 1024):
<answer>index={L_star}, value=1024</answer>

Note: when submitting an answer, the index must equal {L_star}, otherwise the submission is invalid.
"""

    tags = ["answer", "query_value", "query_budget", "query_params"]

    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "H": 10,
                "L_star": 6,
                "B": 6,
                "T": 2,
                "f": [2, 3],
            },
            2: {
                "H": 15,
                "L_star": 10,
                "B": 8,
                "T": 3,
                "f": [2, 2, 3],
            },
            3: {
                "H": 20,
                "L_star": 15,
                "B": 10,
                "T": 4,
                "f": [2, 3, 2, 4],
            },
            4: {
                "H": 25,
                "L_star": 18,
                "B": 12,
                "T": 4,
                "f": [3, 2, 4, 2],
            },
            5: {
                "H": 30,
                "L_star": 22,
                "B": 14,
                "T": 5,
                "f": [2, 3, 2, 4, 3],
            },
        },
        "en": {
            1: {
                "H": 10,
                "L_star": 6,
                "B": 6,
                "T": 2,
                "f": [2, 3],
            },
            2: {
                "H": 15,
                "L_star": 10,
                "B": 8,
                "T": 3,
                "f": [2, 2, 3],
            },
            3: {
                "H": 20,
                "L_star": 15,
                "B": 10,
                "T": 4,
                "f": [2, 3, 2, 4],
            },
            4: {
                "H": 25,
                "L_star": 18,
                "B": 12,
                "T": 4,
                "f": [3, 2, 4, 2],
            },
            5: {
                "H": 30,
                "L_star": 22,
                "B": 14,
                "T": 5,
                "f": [2, 3, 2, 4, 3],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏参数和序列"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保 difficulty 是整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 游戏参数
        self.H = cfg["H"]
        self.L_star = cfg["L_star"]
        self.B = cfg["B"]
        self.T = cfg["T"]
        self.f = cfg["f"]
        
        # 用于格式化规则文本
        self._game_info["H"] = self.H
        self._game_info["L_star"] = self.L_star
        self._game_info["B"] = self.B
        
        # 剩余查询次数
        self.remaining_queries = self.B
        
        # 预计算整个序列
        self.W = [0] * (self.H + 1)
        self.W[0] = 1
        for d in range(self.H):
            multiplier = self.f[d % self.T]
            self.W[d + 1] = self.W[d] * multiplier

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法的数值查询并返回对应的正确答案。
        最多生成 B 个查询（受预算限制）。
        """
        queries = []
        
        simulated_remaining = self.B
        
        for L in range(self.H + 1):
            if L == self.L_star:
                continue
            
            if simulated_remaining <= 0:
                break
                
            value = self.W[L]
            simulated_remaining -= 1
            
            query_str = f"<query_value>{L}</query_value>"
            
            if self.config.language == "zh":
                answer = f"W({L}) = {value}。剩余查询次数：{simulated_remaining}。"
            else:
                answer = f"W({L}) = {value}. Remaining queries: {simulated_remaining}."
                
            queries.append({
                "query": query_str,
                "answer": answer
            })
            
        return queries

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                if "=" not in kv:
                    continue
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "index" not in ans_dict or "value" not in ans_dict:
                return False
            
            submitted_index = int(ans_dict["index"])
            if submitted_index != self.L_star:
                return False
            
            predicted_value = int(ans_dict["value"])
            return predicted_value == self.W[self.L_star]
            
        except (ValueError, KeyError):
            return False

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的查询响应篡改为一个错误的响应。
        通过修改返回值中的数值来生成错误答案。
        """
        import re as _re
        # 尝试匹配 W(L) = <value> 格式中的数值并篡改
        match = _re.search(r'W\(\d+\)\s*=\s*(\d+)', correct)
        if match:
            original_value = int(match.group(1))
            # 生成一个不同的错误值
            wrong_value = original_value + 1 if original_value > 0 else 2
            return correct.replace(match.group(1), str(wrong_value), 1)
        # 如果无法解析，简单地在前面加上错误标记
        return correct + " [tampered]"

    def _cf_core_produce(self, parsed_info):
        # 1. 数值查询（消耗次数）
        if "query_value" in parsed_info:
            try:
                L = int(parsed_info["query_value"].strip())
                
                # 检查索引范围
                if L < 0 or L > self.H:
                    if self.config.language == "zh":
                        return f"错误：索引超出范围。索引必须在 0 到 {self.H} 之间。"
                    else:
                        return f"Error: Index out of range. Index must be between 0 and {self.H}."
                
                # 检查是否查询了禁止的目标索引
                if L == self.L_star:
                    if self.config.language == "zh":
                        self.state.set_state("failed", "违规查询目标索引")
                        return f"违规！你不能查询目标索引 {self.L_star}。游戏失败。"
                    else:
                        self.state.set_state("failed", "illegal query of target index")
                        return f"Violation! You cannot query the target index {self.L_star}. Game failed."
                
                # 检查是否还有剩余次数（不设为failed，允许玩家继续提交答案）
                if self.remaining_queries <= 0:
                    if self.config.language == "zh":
                        return "错误：已用完所有查询次数。你不能再进行数值查询，但可以直接提交答案。"
                    else:
                        return "Error: All query counts have been used. You cannot make more value queries, but you can submit your answer."
                
                # 执行查询
                self.remaining_queries -= 1
                value = self.W[L]
                
                if self.config.language == "zh":
                    return f"W({L}) = {value}。剩余查询次数：{self.remaining_queries}。"
                else:
                    return f"W({L}) = {value}. Remaining queries: {self.remaining_queries}."
                    
            except ValueError:
                if self.config.language == "zh":
                    return "错误：索引必须是整数。"
                else:
                    return "Error: Index must be an integer."
        
        # 2. 预算查询（不消耗次数）
        elif "query_budget" in parsed_info:
            if self.config.language == "zh":
                return f"剩余查询次数：{self.remaining_queries}。"
            else:
                return f"Remaining queries: {self.remaining_queries}."
        
        # 3. 参数查询（不消耗次数）
        elif "query_params" in parsed_info:
            if self.config.language == "zh":
                return f"H = {self.H}, L* = {self.L_star}, B = {self.B}。"
            else:
                return f"H = {self.H}, L* = {self.L_star}, B = {self.B}."
        
        else:
            raise ValueError("No valid query tag found.")