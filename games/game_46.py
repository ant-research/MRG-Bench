from .base import Game
import re
import itertools

class CyclicSubsetInferenceGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "集合"

    game_rule_zh = """\
我们现在来玩一个"周期子集推理"游戏，规则如下：

游戏设定了一个有限集合 U = {{1, 2, ..., {n}}}。我已秘密选定了一个周期长度 K（K 可能是 2、3 或 4），以及 K 个非空子集 R1, R2, ..., RK，它们构成一个循环序列。游戏从第 1 轮开始，每一轮都有一个"当前目标子集"：

- 第 t 轮的当前目标子集为：R_((t-1) mod K + 1)
- 例如：若 K=3，则第 1 轮目标是 R1，第 2 轮是 R2，第 3 轮是 R3，第 4 轮又回到 R1，依此类推。

你的目标是通过尽可能少的测试，推断出周期长度 K 以及所有目标子集 R1, ..., RK 的具体元素。

每次你可以选择以下三种操作之一：

1. **子集包含测试**：提交一个子集 S（用逗号分隔的编号），我会告诉你：
   - 当前目标子集是否完全包含在 S 中（"是"或"否"）
   - 当前目标子集中有多少元素不在 S 中（一个非负整数，若包含判定为"是"，则为 0）

2. **推进轮次**：请求进入下一轮，当前目标子集将按周期切换到下一个。

3. **提交最终答案**：当你认为已经推断出答案时，提交周期长度 K 以及所有子集 R1, ..., RK。

每次只能提交一个操作标签。请使用以下 XML 格式：

- 子集包含测试（例如测试子集 {{1,2,3}}）：
<test_subset>1,2,3</test_subset>

- 推进轮次（内容为空）：
<next_round></next_round>

- 提交最终答案（例如 K=3，R1={{1,2}}, R2={{3}}, R3={{1,4}}）：
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

注意：
- 提交答案时，子集顺序很重要，必须与实际的循环序列对应（允许循环位移，例如 R1,R2,R3 和 R2,R3,R1 视为等价）
- 若答案错误累计三次，游戏失败
- 空集不能包含在测试或答案中
"""

    game_rule_en = """\
Let's play a "Cyclic Subset Inference" game. Here are the rules:

The game has a finite set U = {{1, 2, ..., {n}}}. I have secretly chosen a cycle length K (K can be 2, 3, or 4), and K non-empty subsets R1, R2, ..., RK that form a cyclic sequence. The game starts from round 1, and each round has a "current target subset":

- The current target subset of round t is: R_((t-1) mod K + 1)
- For example: if K=3, round 1's target is R1, round 2's is R2, round 3's is R3, round 4's is R1 again, and so on.

Your goal is to infer the cycle length K and all target subsets R1, ..., RK with as few tests as possible.

Each time you can choose one of the following three operations:

1. **Subset Containment Test**: Submit a subset S (comma-separated IDs), and I will tell you:
   - Whether the current target subset is fully contained in S ("Yes" or "No")
   - How many elements of the current target subset are not in S (a non-negative integer; 0 if containment is "Yes")

2. **Advance Round**: Request to move to the next round, and the current target subset will switch to the next one in the cycle.

3. **Submit Final Answer**: When you think you have inferred the answer, submit the cycle length K and all subsets R1, ..., RK.

Each submission must contain only one operation tag. Use the following XML format:

- Subset Containment Test (e.g., testing subset {{1,2,3}}):
<test_subset>1,2,3</test_subset>

- Advance Round (empty content):
<next_round></next_round>

- Submit Final Answer (e.g., K=3, R1={{1,2}}, R2={{3}}, R3={{1,4}}):
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

Note:
- When submitting the answer, the order of subsets matters and must correspond to the actual cyclic sequence (cyclic shifts are allowed, e.g., R1,R2,R3 and R2,R3,R1 are considered equivalent)
- If the answer is wrong three times in total, the game fails
- Empty sets cannot be included in tests or answers
"""

    contextualized_rule_zh_1 = """\
我们现在来进行"交通信号灯相位调度"推演，规则如下：

系统设定了一个复杂的交叉路口，共有流量方向集合 U = {{1, 2, ..., {n}}}。智能交通系统秘密选用了一个相位周期长度 K（K 可能是 2、3 或 4），以及 K 个非空通行流向集合 R1, R2, ..., RK，它们构成一个循环的相位序列。推演从第 1 个相位（轮次）开始，每个相位都有一个"当前通行流向集合"：

- 第 t 个相位的当前通行集合为：R_((t-1) mod K + 1)
- 例如：若 K=3，则第 1 个相位通行 R1，第 2 个相位通行 R2，第 3 个相位通行 R3，第 4 个相位又回到 R1，依此类推。

你的目标是通过尽可能少的监控测试，推断出周期长度 K 以及所有通行流向集合 R1, ..., RK 的具体编号。

每次你可以选择以下三种操作之一：

1. **监控覆盖测试**：提交一个监控流向集合 S（用逗号分隔的编号），系统会返回：
   - 当前相位的通行流向是否完全被包含在监控集合 S 中（"是"或"否"）
   - 当前相位有多少个通行流向未被 S 监控覆盖（一个非负整数，若判定为"是"，则为 0）

2. **推进相位**：请求进入下一个相位，当前通行流向集合将按周期切换到下一个。

3. **提交最终调度方案**：当你认为已经推断出系统设置时，提交周期长度 K 以及所有流向集合 R1, ..., RK。

每次只能提交一个操作标签。请使用以下 XML 格式：

- 监控覆盖测试（例如测试流向 {{1,2,3}}）：
<test_subset>1,2,3</test_subset>

- 推进相位（内容为空）：
<next_round></next_round>

- 提交最终调度方案（例如 K=3，R1={{1,2}}, R2={{3}}, R3={{1,4}}）：
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

注意：
- 提交方案时，集合顺序很重要，必须与实际的相位循环序列对应（允许循环位移，例如 R1,R2,R3 和 R2,R3,R1 视为等价）
- 若方案错误累计三次，推演失败
- 空集不能包含在测试或最终方案中
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's engage in a "Traffic Signal Phase Scheduling" simulation. Here are the rules:

The system involves a complex intersection with a set of traffic flow directions U = {{1, 2, ..., {n}}}. The intelligent traffic system has secretly chosen a phase cycle length K (K can be 2, 3, or 4) and K non-empty allowed flow subsets R1, R2, ..., RK that form a cyclic phase sequence. The simulation starts from phase (round) 1, and each phase has a "current allowed flow subset":

- The current allowed flow subset for phase t is: R_((t-1) mod K + 1)
- For example: if K=3, phase 1 allows R1, phase 2 allows R2, phase 3 allows R3, phase 4 reverts to R1, and so on.

Your goal is to infer the cycle length K and all allowed flow subsets R1, ..., RK with as few monitoring tests as possible.

Each time you can choose one of the following three operations:

1. **Monitoring Coverage Test**: Submit a subset of monitored flows S (comma-separated IDs), and the system will return:
   - Whether the current phase's allowed flows are fully contained in the monitored subset S ("Yes" or "No")
   - How many allowed flows of the current phase are not covered by S (a non-negative integer; 0 if containment is "Yes")

2. **Advance Phase**: Request to move to the next phase, and the current allowed flow subset will switch to the next one in the cycle.

3. **Submit Final Scheduling Plan**: When you think you have inferred the system settings, submit the cycle length K and all subsets R1, ..., RK.

Each submission must contain only one operation tag. Use the following XML format:

- Monitoring Coverage Test (e.g., testing flows {{1,2,3}}):
<test_subset>1,2,3</test_subset>

- Advance Phase (empty content):
<next_round></next_round>

- Submit Final Scheduling Plan (e.g., K=3, R1={{1,2}}, R2={{3}}, R3={{1,4}}):
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

Note:
- When submitting the plan, the order of subsets matters and must correspond to the actual cyclic sequence (cyclic shifts are allowed, e.g., R1,R2,R3 and R2,R3,R1 are considered equivalent)
- If the plan is wrong three times in total, the simulation fails
- Empty sets cannot be included in tests or the final plan
"""

    contextualized_rule_zh_2 = """\
我们现在来进行"慢性病周期性联合用药方案"推演，规则如下：

药房备有可用药物集合 U = {{1, 2, ..., {n}}}。医生为患者秘密制定了一个用药周期 K（K 可能是 2、3 或 4 天），以及 K 个非空的日服药物组合 R1, R2, ..., RK，它们构成一个循环用药序列。推演从第 1 天（轮次）开始，每天都有一个"当日处方药物组合"：

- 第 t 天的当日处方药物组合为：R_((t-1) mod K + 1)
- 例如：若 K=3，则第 1 天服药 R1，第 2 天服药 R2，第 3 天服药 R3，第 4 天又回到 R1，依此类推。

你的目标是通过尽可能少的配药测试，推断出用药周期 K 以及所有药物组合 R1, ..., RK 的具体药物编号。

每次你可以选择以下三种操作之一：

1. **配药覆盖测试**：提交一个备选药物包 S（用逗号分隔的编号），系统会返回：
   - 当日处方药物是否完全包含在备选药物包 S 中（"是"或"否"）
   - 当日处方药物中有多少种未在 S 中（一个非负整数，若判定为"是"，则为 0）

2. **推进用药日**：请求进入下一天，当日处方药物将按周期切换到下一个组合。

3. **提交最终治疗方案**：当你认为已经推断出具体用药时，提交周期 K 以及所有药物组合 R1, ..., RK。

每次只能提交一个操作标签。请使用以下 XML format：

- 配药覆盖测试（例如测试药物包 {{1,2,3}}）：
<test_subset>1,2,3</test_subset>

- 推进用药日（内容为空）：
<next_round></next_round>

- 提交最终治疗方案（例如 K=3，R1={{1,2}}, R2={{3}}, R3={{1,4}}）：
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

注意：
- 提交方案时，组合顺序很重要，必须与实际的用药循环序列对应（允许循环位移，例如 R1,R2,R3 和 R2,R3,R1 视为等价）
- 若方案错误累计三次，推演失败
- 空集不能包含在测试或最终方案中
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's engage in a "Chronic Disease Cyclic Medication Plan" simulation. Here are the rules:

The pharmacy has an available medication set U = {{1, 2, ..., {n}}}. The doctor has secretly formulated a medication cycle length K (K can be 2, 3, or 4 days) and K non-empty daily medication combinations R1, R2, ..., RK that form a cyclic medication sequence. The simulation starts from day (round) 1, and each day has a "current prescribed medication combination":

- The current prescribed medication combination for day t is: R_((t-1) mod K + 1)
- For example: if K=3, day 1 requires R1, day 2 requires R2, day 3 requires R3, day 4 reverts to R1, and so on.

Your goal is to infer the cycle length K and all daily medication combinations R1, ..., RK with as few dispensing tests as possible.

Each time you can choose one of the following three operations:

1. **Dispensing Coverage Test**: Submit a subset of prepared medications S (comma-separated IDs), and the system will return:
   - Whether the current day's prescribed medications are fully contained in the prepared subset S ("Yes" or "No")
   - How many prescribed medications of the current day are missing from S (a non-negative integer; 0 if containment is "Yes")

2. **Advance Medication Day**: Request to move to the next day, and the current prescribed combination will switch to the next one in the cycle.

3. **Submit Final Treatment Plan**: When you think you have inferred the plan, submit the cycle length K and all subsets R1, ..., RK.

Each submission must contain only one operation tag. Use the following XML format:

- Dispensing Coverage Test (e.g., testing medications {{1,2,3}}):
<test_subset>1,2,3</test_subset>

- Advance Medication Day (empty content):
<next_round></next_round>

- Submit Final Treatment Plan (e.g., K=3, R1={{1,2}}, R2={{3}}, R3={{1,4}}):
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

Note:
- When submitting the plan, the order of combinations matters and must correspond to the actual cyclic sequence (cyclic shifts are allowed, e.g., R1,R2,R3 and R2,R3,R1 are considered equivalent)
- If the plan is wrong three times in total, the simulation fails
- Empty sets cannot be included in tests or the final plan
"""

    contextualized_rule_zh_3 = """\
我们现在来进行"轮动式互动教学课程排班"推演，规则如下：

学校开设了总兴趣模块集合 U = {{1, 2, ..., {n}}}。教学组秘密制定了一个周期长度 K（K 可能是 2、3 或 4 周），以及 K 个非空的核心学习模块组合 R1, R2, ..., RK，它们构成一个循环的教学大纲。推演从第 1 周（轮次）开始，每周都有一个"当前核心模块组合"：

- 第 t 周的当前核心模块组合为：R_((t-1) mod K + 1)
- 例如：若 K=3，则第 1 周学习 R1，第 2 周学习 R2，第 3 周学习 R3，第 4 周又回到 R1，依此类推。

你的目标是通过尽可能少的材料覆盖测试，推断出教学周期 K 以及所有核心模块组合 R1, ..., RK 的具体编号。

每次你可以选择以下三种操作之一：

1. **材料覆盖测试**：准备一个教学材料包 S（用逗号分隔的模块编号），系统会返回：
   - 当前周的核心学习模块是否完全被该材料包 S 覆盖（"是"或"否"）
   - 当前周的核心模块中有多少个缺少教学材料（一个非负整数，若判定为"是"，则为 0）

2.教学**推进教学周**：请求进入下一个教学周，当前核心模块组合将按周期切换到下一个。

3. **提交最终教学大纲**：当你认为已经推断出系统设置时，提交周期长度 K 以及所有模块组合 R1, ..., RK。

每次只能提交一个操作标签。请使用以下 XML 格式：

- 材料覆盖测试（例如测试材料包 {{1,2,3}}）：
<test_subset>1,2,3</test_subset>

- 推进教学周（内容为空）：
<next_round></next_round>

- 提交最终教学大纲（例如 K=3，R1={{1,2}}, R2={{3}}, R3={{1,4}}）：
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

注意：
- 提交大纲时，组合顺序很重要，必须与实际的教学循环序列对应（允许循环位移，例如 R1,R2,R3 和 R2,R3,R1 视为等价）
- 若大纲错误累计三次，推演失败
- 空集不能包含在测试或最终大纲中
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's engage in a "Rotating Interactive Teaching Syllabus" simulation. Here are the rules:

The school offers a total set of interest modules U = {{1, 2, ..., {n}}}. The teaching committee has secretly formulated a teaching cycle length K (K can be 2, 3, or 4 weeks) and K non-empty core learning module combinations R1, R2, ..., RK that form a cyclic syllabus. The simulation starts from week (round) 1, and each week has a "current core module combination":

- The current core module combination for week t is: R_((t-1) mod K + 1)
- For example: if K=3, week 1 focuses on R1, week 2 focuses on R2, week 3 focuses on R3, week 4 reverts to R1, and so on.

Your goal is to infer the teaching cycle length K and all core module combinations R1, ..., RK with as few material coverage tests as possible.

Each time you can choose one of the following three operations:

1. **Material Coverage Test**: Prepare a teaching material package S (comma-separated module IDs), and the system will return:
   - Whether the current week's core modules are fully covered by the material package S ("Yes" or "No")
   - How many core modules of the current week lack teaching materials in S (a non-negative integer; 0 if containment is "Yes")

2. **Advance Teaching Week**: Request to move to the next teaching week, and the current core module combination will switch to the next one in the cycle.

3. **Submit Final Syllabus**: When you think you have inferred the syllabus, submit the cycle length K and all combinations R1, ..., RK.

Each submission must contain only one operation tag. Use the following XML format:

- Material Coverage Test (e.g., testing package {{1,2,3}}):
<test_subset>1,2,3</test_subset>

- Advance Teaching Week (empty content):
<next_round></next_round>

- Submit Final Syllabus (e.g., K=3, R1={{1,2}}, R2={{3}}, R3={{1,4}}):
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

Note:
- When submitting the syllabus, the order of combinations matters and must correspond to the actual cyclic sequence (cyclic shifts are allowed, e.g., R1,R2,R3 and R2,R3,R1 are considered equivalent)
- If the syllabus is wrong three times in total, the simulation fails
- Empty sets cannot be included in tests or the final syllabus
"""

    contextualized_rule_zh_4 = """\
我们现在来进行"自动化流水线多工序循环加工"推演，规则如下：

工厂车间具有可用设备集合 U = {{1, 2, ..., {n}}}。系统内部设定了一个工艺节拍周期 K（K 可能是 2、3 或 4 个节拍），以及 K 个非空的并发设备组合 R1, R2, ..., RK，它们构成一个循环运转的加工序列。推演从第 1 节拍（轮次）开始，每个节拍都有一个"当前必需设备组合"：

- 第 t 节拍的当前必需设备组合为：R_((t-1) mod K + 1)
- 例如：若 K=3，则第 1 节拍启动 R1，第 2 节拍启动 R2，第 3 节拍启动 R3，第 4 节拍又回到 R1，依此类推。

你的目标是通过尽可能少的供电测试，推断出节拍周期 K 以及所有设备组合 R1, ..., RK 的具体编号。

每次你可以选择以下三种操作之一：

1. **设备供电测试**：提交一组通电的设备集合 S（用逗号分隔的编号），系统会返回：
   - 当前节拍所需的全部设备是否均已包含在供电集合 S 中（"是"或"否"）
   - 当前节拍有多少台必需设备未被供电（一个非负整数，若判定为"是"，则为 0）

2. **推进工艺节拍**：请求进入流水线的下一个节拍，当前必需设备组合将按周期切换到下一个。

3. **提交最终工艺流程**：当你认为已经推断出系统设定时，提交节拍周期 K 以及所有设备组合 R1, ..., RK。

每次只能提交一个操作标签。请使用以下 XML 格式：

- 设备供电测试（例如为设备 {{1,2,3}} 供电）：
<test_subset>1,2,3</test_subset>

- 推进工艺节拍（内容为空）：
<next_round></next_round>

- 提交最终工艺流程（例如 K=3，R1={{1,2}}, R2={{3}}, R3={{1,4}}）：
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

注意：
- 提交流程时，组合顺序很重要，必须与实际的节拍循环序列对应（允许循环位移，例如 R1,R2,R3 和 R2,R3,R1 视为等价）
- 若流程错误累计三次，推演失败
- 空集不能包含在测试或最终流程中
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's engage in an "Automated Assembly Line Multi-process Cycle" simulation. Here are the rules:

The factory floor has a set of available machines U = {{1, 2, ..., {n}}}. The system has secretly configured a process beat cycle length K (K can be 2, 3, or 4 beats) and K non-empty concurrent machine combinations R1, R2, ..., RK that form a cyclic operational sequence. The simulation starts from beat (round) 1, and each beat has a "current required machine combination":

- The current required machine combination for beat t is: R_((t-1) mod K + 1)
- For example: if K=3, beat 1 activates R1, beat 2 activates R2, beat 3 activates R3, beat 4 reverts to R1, and so on.

Your goal is to infer the cycle length K and all machine combinations R1, ..., RK with as few power tests as possible.

Each time you can choose one of the following three operations:

1. **Machine Power Test**: Submit a subset of powered machines S (comma-separated IDs), and the system will return:
   - Whether all required machines for the current beat are fully contained in the powered subset S ("Yes" or "No")
   - How many required machines of the current beat are not powered in S (a non-negative integer; 0 if containment is "Yes")

2. **Advance Process Beat**: Request to move the assembly line to the next beat, and the current required combination will switch to the next one in the cycle.

3. **Submit Final Process Flow**: When you think you have inferred the system configuration, submit the cycle length K and all subsets R1, ..., RK.

Each submission must contain only one operation tag. Use the following XML format:

- Machine Power Test (e.g., testing machines {{1,2,3}}):
<test_subset>1,2,3</test_subset>

- Advance Process Beat (empty content):
<next_round></next_round>

- Submit Final Process Flow (e.g., K=3, R1={{1,2}}, R2={{3}}, R3={{1,4}}):
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

Note:
- When submitting the flow, the order of combinations matters and must correspond to the actual cyclic sequence (cyclic shifts are allowed, e.g., R1,R2,R3 and R2,R3,R1 are considered equivalent)
- If the flow is wrong three times in total, the simulation fails
- Empty sets cannot be included in tests or the final flow
"""

    contextualized_rule_zh_5 = """\
我们现在来进行"合规审查循环抽检机制"推演，规则如下：

公司总共有核心业务部门集合 U = {{1, 2, ..., {n}}}。法务部秘密确立了一个审查周期 K（K 可能是 2、3 或 4 个季度），以及 K 个非空的抽检部门组合 R1, R2, ..., RK，它们构成一个循环的审查序列。推演从第 1 季度（轮次）开始，每个季度都有一个"当前待审部门组合"：

- 第 t 季度的当前待审组合为：R_((t-1) mod K + 1)
- 例如：若 K=3，则第 1 季度审查 R1，第 2 季度审查 R2，第 3 季度审查 R3，第 4 季度又回到 R1，依此类推。

你的目标是通过尽可能少的档案调取测试，推断出审查周期 K 以及所有待审部门组合 R1, ..., RK 的具体编号。

每次你可以选择以下三种操作之一：

1. **调档覆盖测试**：申请调取一个部门档案集合 S（用逗号分隔的编号），系统会返回：
   - 当前季度的所有待审部门档案是否都已包含在调取集合 S 中（"是"或"否"）
   - 当前季度有多少个待审部门的档案未被包含在 S 中（一个非负整数，若判定为"是"，则为 0）

2. **推进审查季度**：请求进入下一个财务季度，当前待审部门组合将按周期切换到下一个。

3. **提交最终抽检计划**：当你认为已经推断出法务部机制时，提交审查周期 K 以及所有部门组合 R1, ..., RK。

每次只能提交一个操作标签。请使用以下 XML 格式：

- 调档覆盖测试（例如调取部门 {{1,2,3}}）：
<test_subset>1,2,3</test_subset>

- 推进审查季度（内容为空）：
<next_round></next_round>

- 提交最终抽检计划（例如 K=3，R1={{1,2}}, R2={{3}}, R3={{1,4}}）：
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

注意：
- 提交计划时，组合顺序很重要，必须与实际的审查循环序列对应（允许循环位移，例如 R1,R2,R3 和 R2,R3,R1 视为等价）
- 若计划错误累计三次，推演失败
- 空集不能包含在测试或最终计划中
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's engage in a "Compliance Audit Cyclic Sampling Mechanism" simulation. Here are the rules:

The company has a set of core business departments U = {{1, 2, ..., {n}}}. The legal department has secretly established an audit cycle length K (K can be 2, 3, or 4 quarters) and K non-empty targeted department combinations R1, R2, ..., RK that form a cyclic audit sequence. The simulation starts from quarter (round) 1, and each quarter has a "current targeted department combination":

- The current targeted combination for quarter t is: R_((t-1) mod K + 1)
- For example: if K=3, quarter 1 audits R1, quarter 2 audits R2, quarter 3 audits R3, quarter 4 reverts to R1, and so on.

Your goal is to infer the cycle length K and all targeted department combinations R1, ..., RK with as few archive retrieval tests as possible.

Each time you can choose one of the following three operations:

1. **Archive Retrieval Coverage Test**: Request to retrieve an archive subset S (comma-separated department IDs), and the system will return:
   - Whether the archives of all targeted departments for the current quarter are fully contained in subset S ("Yes" or "No")
   - How many targeted departments of the current quarter are missing from the retrieved subset S (a non-negative integer; 0 if containment is "Yes")

2. **Advance Audit Quarter**: Request to move to the next financial quarter, and the current targeted combination will switch to the next one in the cycle.

3. **Submit Final Sampling Plan**: When you think you have inferred the legal department's mechanism, submit the cycle length K and all subsets R1, ..., RK.

Each submission must contain only one operation tag. Use the following XML format:

- Archive Retrieval Coverage Test (e.g., retrieving departments {{1,2,3}}):
<test_subset>1,2,3</test_subset>

- Advance Audit Quarter (empty content):
<next_round></next_round>

- Submit Final Sampling Plan (e.g., K=3, R1={{1,2}}, R2={{3}}, R3={{1,4}}):
<answer>K=3, R1=1,2, R2=3, R3=1,4</answer>

Note:
- When submitting the plan, the order of combinations matters and must correspond to the actual cyclic sequence (cyclic shifts are allowed, e.g., R1,R2,R3 and R2,R3,R1 are considered equivalent)
- If the plan is wrong three times in total, the simulation fails
- Empty sets cannot be included in tests or the final plan
"""

    tags = ["answer", "test_subset", "next_round"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "K": 2,
                "subsets": ["1,2", "4,5,6"],
            },
            2: {
                "n": 8,
                "K": 2,
                "subsets": ["1,2,3", "3,5,7"],
            },
            3: {
                "n": 9,
                "K": 3,
                "subsets": ["1,2", "4,5,6", "7,8"],
            },
            4: {
                "n": 10,
                "K": 3,
                "subsets": ["1,2,3,4", "3,5,7", "2,6,8,9"],
            },
            5: {
                "n": 12,
                "K": 4,
                "subsets": ["1,3,5", "2,4,6,8", "5,7,9", "1,10,11,12"],
            },
        },
        "en": {
            1: {
                "n": 6,
                "K": 2,
                "subsets": ["1,2", "4,5,6"],
            },
            2: {
                "n": 8,
                "K": 2,
                "subsets": ["1,2,3", "3,5,7"],
            },
            3: {
                "n": 9,
                "K": 3,
                "subsets": ["1,2", "4,5,6", "7,8"],
            },
            4: {
                "n": 10,
                "K": 3,
                "subsets": ["1,2,3,4", "3,5,7", "2,6,8,9"],
            },
            5: {
                "n": 12,
                "K": 4,
                "subsets": ["1,3,5", "2,4,6,8", "5,7,9", "1,10,11,12"],
            },
        },
    }

    def __init__(self, config):
        self.wrong_answer_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        self.K = cfg["K"]
        self.R_sequence = []
        for subset_str in cfg["subsets"]:
            subset = set(x.strip() for x in subset_str.split(",") if x.strip())
            self.R_sequence.append(subset)
        
        self.current_round = 1

    def _get_current_target(self):
        idx = (self.current_round - 1) % self.K
        return self.R_sequence[idx]

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            
            k_part = None
            r_parts = []
            temp = []
            for part in parts:
                if part.startswith("K="):
                    k_part = part
                elif part.startswith("R"):
                    if temp:
                        r_parts.append(",".join(temp))
                    temp = [part]
                else:
                    temp.append(part)
            if temp:
                r_parts.append(",".join(temp))
            
            if not k_part:
                return False
            
            model_K = int(k_part.split("=")[1].strip())
            
            if model_K != self.K:
                return False
            
            model_subsets = []
            for r_part in r_parts:
                if "=" not in r_part:
                    continue
                _, elements_str = r_part.split("=", 1)
                elements = set(x.strip() for x in elements_str.split(",") if x.strip())
                if elements:
                    model_subsets.append(elements)
            
            if len(model_subsets) != self.K:
                return False
            
            for offset in range(self.K):
                match = True
                for i in range(self.K):
                    true_idx = i
                    model_idx = (i + offset) % self.K
                    if self.R_sequence[true_idx] != model_subsets[model_idx]:
                        match = False
                        break
                if match:
                    return True
            
            return False
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            round_msg = f"当前是第 {self.current_round} 轮。"
            next_round_msg = f"已进入第 {self.current_round} 轮。"
            error_format = "错误：格式无效或编号超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            round_msg = f"Current round: {self.current_round}."
            next_round_msg = f"Advanced to round {self.current_round}."
            error_format = "Error: Invalid format or ID out of range."

        if "test_subset" in parsed_info:
            try:
                raw = parsed_info["test_subset"].strip()
                if not raw:
                    return error_format
                
                S = set(x.strip() for x in raw.split(",") if x.strip())
                
                valid_ids = set(str(i) for i in range(1, self._game_info["n"] + 1))
                if not S.issubset(valid_ids):
                    return error_format
                
                R_current = self._get_current_target()
                
                is_contained = R_current.issubset(S)
                missing_count = len(R_current - S)
                
                if self.config.language == "zh":
                    containment_str = yes_res if is_contained else no_res
                    response = f"{round_msg}\n包含判定：{containment_str}\n缺失元素数量：{missing_count}"
                else:
                    containment_str = yes_res if is_contained else no_res
                    response = f"{round_msg}\nContainment: {containment_str}\nMissing count: {missing_count}"
                
                return response
                
            except Exception as e:
                return error_format

        elif "next_round" in parsed_info:
            self.current_round += 1
            return next_round_msg

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]

        original_round = self.current_round

        for k in range(self.K):
            self.current_round = k + 1
            R_current = self._get_current_target()

            if self.config.language == "zh":
                yes_res, no_res = "是", "否"
                round_msg = f"当前是第 {self.current_round} 轮。"
                next_round_msg = f"已进入第 {self.current_round} 轮。"
            else:
                yes_res, no_res = "Yes", "No"
                round_msg = f"Current round: {self.current_round}."
                next_round_msg = f"Advanced to round {self.current_round}."

            for r in range(1, n + 1):
                for combo in itertools.combinations(range(1, n + 1), r):
                    query_content = ",".join(map(str, combo))
                    query_str = f"<test_subset>{query_content}</test_subset>"
                    
                    S = set(str(x) for x in combo)
                    is_contained = R_current.issubset(S)
                    missing_count = len(R_current - S)

                    if self.config.language == "zh":
                        containment_str = yes_res if is_contained else no_res
                        response = f"{round_msg}\n包含判定：{containment_str}\n缺失元素数量：{missing_count}"
                    else:
                        containment_str = yes_res if is_contained else no_res
                        response = f"{round_msg}\nContainment: {containment_str}\nMissing count: {missing_count}"
                    
                    queries.append({
                        "query": query_str,
                        "answer": response
                    })
            
            queries.append({
                "query": "<next_round></next_round>",
                "answer": next_round_msg
            })

        self.current_round = original_round
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        modified = correct
        replaced = False
        
        if "是" in modified or "否" in modified:
            modified = modified.replace("是", "TEMP").replace("否", "是").replace("TEMP", "否")
            replaced = True
        
        elif "Yes" in modified or "No" in modified:
            modified = modified.replace("Yes", "TEMP").replace("No", "Yes").replace("TEMP", "No")
            replaced = True
            
        if not replaced:
            modified += "_WRONG"
            
        return modified

    def step(self, response: str) -> 'GameState':
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确！" if self.config.language == "zh" else "Correct answer!"
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    self.wrong_answer_count += 1
                    if self.wrong_answer_count >= 3:
                        res = "答案错误，已累计三次错误，游戏失败。" if self.config.language == "zh" else "Incorrect answer. Three wrong attempts reached. Game failed."
                        self.state.set_state("failed", "three incorrect answers")
                        self.state.add_message("user", res)
                    else:
                        remaining = 3 - self.wrong_answer_count
                        if self.config.language == "zh":
                            res = f"答案错误，还有 {remaining} 次机会。"
                        else:
                            res = f"Incorrect answer. {remaining} attempt(s) remaining."
                        self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))    
        
        return self.state