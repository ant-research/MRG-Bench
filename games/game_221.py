import re
import itertools
from typing import List, Dict, Tuple
from .base import Game

class SequenceResponseGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"序列响应推理"游戏，规则如下：

游戏设定：
- 存在一个长度为 {n} 的二元序列（每个位置只能是 0 或 1）
- 序列从空开始，你需要逐步追加符号直到填满
- 系统内部有一个隐藏的窗口大小 k 和一个响应函数 f
- 每当你追加一个符号后，系统会返回一个响应值（非负整数）
- 响应值仅由"最近的若干个符号"决定（具体数量不超过 k）
- 相同的后缀窗口总会产生相同的响应值

你的目标：
在序列填满之前，推断出规律，并完成一次"预测提交"——给出剩余所有步骤要追加的符号及对应的响应预测。若全部正确则游戏成功。

可用操作：

1. 追加符号：追加 0 或 1 到序列
   格式：<append>0</append> 或 <append>1</append>
   反馈：本步响应值、已追加总数、剩余容量

2. 假设模拟（最多使用 {max_simulations} 次）：提供一段二元串，模拟若依次追加它们会得到什么响应，不影响真实状态
   格式：<simulate>01101</simulate>
   反馈：每一步的响应值列表

3. 状态查询：查看当前已追加数、剩余容量、历史响应
   格式：<query_state></query_state>
   反馈：当前状态信息

4. 预测提交：提供剩余步骤的二元串和对应的响应预测
   格式：<answer>sequence=0110, responses=3,2,1,5</answer>
   说明：sequence 为要追加的符号串，responses 为逗号分隔的整数预测列表，两者长度必须相等且等于剩余容量
   若全部正确则成功；若有错误会告知第几步错误及实际响应，并将预测串的前面部分追加到真实序列

注意事项：
- 每次只能执行一个操作
- 若序列填满仍未完成正确的预测提交，游戏失败
- 请尽可能少地使用操作次数
"""

    game_rule_en = """\
Let's play a "Sequence Response Inference" game. Here are the rules:

Game Setup:
- There is a binary sequence of length {n} (each position can be 0 or 1)
- The sequence starts empty, and you append symbols step by step until full
- The system has a hidden window size k and a response function f
- After each append, the system returns a response value (non-negative integer)
- The response depends only on "the most recent symbols" (up to k symbols)
- Identical suffix windows always produce identical responses

Your Goal:
Before the sequence fills up, deduce the pattern and complete a "prediction submission" — provide all remaining symbols to append and their corresponding response predictions. If all correct, you win.

Available Operations:

1. Append Symbol: Append 0 or 1 to the sequence
   Format: <append>0</append> or <append>1</append>
   Feedback: Current step response, total appended, remaining capacity

2. Hypothetical Simulation (up to {max_simulations} uses): Provide a binary string to simulate responses without changing real state
   Format: <simulate>01101</simulate>
   Feedback: List of response values for each step

3. State Query: View current appended count, remaining capacity, and response history
   Format: <query_state></query_state>
   Feedback: Current state information

4. Prediction Submission: Provide remaining binary string and corresponding response predictions
   Format: <answer>sequence=0110, responses=3,2,1,5</answer>
   Note: sequence is the symbol string to append, responses is comma-separated integer list; both must have same length equal to remaining capacity
   If all correct, success; if wrong, will indicate which step failed and actual response, then append the correct prefix to real sequence

Important:
- Only one operation per turn
- If sequence fills up without successful prediction submission, game fails
- Try to use as few operations as possible
"""

    contextualized_rule_zh_1 = """\
这是一款"智能交通流量响应"演练。你作为交通调度员，需要摸清路网调控系统的内在规律：

演练设定：
- 需要在 {n} 个连续时段内下达交通调控指令（0 代表限流，1 代表放行）
- 指令序列从空开始，你需要逐步下达直到填满整个调度周期
- 交通网格内部有一个隐藏的滞后窗口 k 和拥堵计算模型 f
- 每当下达一个指令后，路网会返回当前的"拥堵指数"（非负整数）
- 拥堵指数仅受"最近的若干次调控指令"影响（具体影响深度不超过 k）
- 相同的指令后缀组合总会产生相同的拥堵指数

你的目标：
在周期填满之前，推断出路网的响应规律，并完成一次"预案提交"——给出剩余所有时段的调控指令及对应的拥堵指数预测。若全部正确则演练成功。

可用操作：

1. 下达指令：向路网下发 0 或 1 的指令
   格式：<append>0</append> 或 <append>1</append>
   反馈：本时段拥堵指数、已下达总数、剩余时段数

2. 沙盘模拟（最多使用 {max_simulations} 次）：提供一段指令串，推演若依次执行它们会得到什么指数，不影响真实路网状态
   格式：<simulate>01101</simulate>
   反馈：每一步的拥堵指数推演列表

3. 状态查询：查看当前已下达数、剩余时段数、历史拥堵记录
   格式：<query_state></query_state>
   反馈：当前状态信息

4. 预案提交：提供剩余时段的指令序列和对应的拥堵预测
   格式：<answer>sequence=0110, responses=3,2,1,5</answer>
   说明：sequence 为要下达的指令串，responses 为逗号分隔的整数预测列表，两者长度必须相等且等于剩余时段数
   若全部正确则成功；若有错误会告知第几步错误及实际指数，并将预测串的前面部分强制下达到真实序列

注意事项：
- 每次只能执行一个操作
- 若周期填满仍未完成正确的预案提交，演练失败
- 请尽可能少地使用操作次数
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Intelligent Traffic Flow Response" drill. As a dispatcher, you need to understand the network control system's pattern:

Drill Setup:
- You must issue traffic control commands over {n} continuous periods (0 for restrict, 1 for release)
- The command sequence starts empty, and you append step by step until the cycle is full
- The traffic grid has a hidden lag window k and a congestion model f
- After each command, the network returns the current "congestion index" (non-negative integer)
- This index is only affected by "the most recent commands" (up to a depth of k)
- Identical command suffix combinations always produce identical congestion indices

Your Goal:
Before the cycle fills up, deduce the network's response pattern and complete a "plan submission" — provide all remaining commands to issue and their corresponding congestion index predictions. If all correct, you succeed.

Available Operations:

1. Issue Command: Issue 0 or 1 to the network
   Format: <append>0</append> or <append>1</append>
   Feedback: Current period congestion index, total issued, remaining periods

2. Sandbox Simulation (up to {max_simulations} uses): Provide a command string to simulate indices without affecting the real network
   Format: <simulate>01101</simulate>
   Feedback: List of congestion indices for each step

3. State Query: View current issued count, remaining periods, and index history
   Format: <query_state></query_state>
   Feedback: Current state information

4. Plan Submission: Provide remaining command sequence and corresponding index predictions
   Format: <answer>sequence=0110, responses=3,2,1,5</answer>
   Note: sequence is the command string to issue, responses is a comma-separated integer list; both must equal remaining periods
   If all correct, success; if wrong, will indicate which step failed and actual index, then enforce the correct prefix to the real sequence

Important:
- Only one operation per turn
- If the cycle fills up without a successful plan submission, the drill fails
- Try to use as few operations as possible
"""

    contextualized_rule_zh_2 = """\
这是一款"基因靶向用药疗程"推理游戏。你作为临床医师，需要掌握某种创新疗法的排异规律：

临床设定：
- 患者需要接受总计 {n} 个阶段的连续用药（0 代表 A药，1 代表 B药）
- 疗程从空开始，你需要逐步给予药物直到填满整个疗程
- 患者体内有隐藏的药物累积窗口 k 和代谢模型 f
- 每当给予一次药物后，系统会返回当前的"排异反应指标"（非负整数）
- 排异反应指标仅由"最近的若干次用药"决定（累积效应不超过 k 次）
- 相同的用药后缀组合总会产生相同的排异反应指标

你的目标：
在疗程结束前，推断出患者的排异响应机制，并完成一次"疗程提交"——规划剩余所有阶段的用药序列及对应的排异指标预测。若全部正确则治疗成功。

可用操作：

1. 临床给药：向患者施用药物 0 或 1
   格式：<append>0</append> 或 <append>1</append>
   反馈：本次排异指标、已用药次数、剩余阶段数

2. 离体推演（最多使用 {max_simulations} 次）：提供一段用药序列，在生化沙盒中模拟它们会带来什么排异反应，不影响患者真实体征
   格式：<simulate>01101</simulate>
   反馈：每一步的排异指标推演列表

3. 病历查询：查看当前已用药次数、剩余阶段数、历史排异记录
   格式：<query_state></query_state>
   反馈：当前状态信息

4. 疗程提交：提供剩余阶段的用药序列和对应的排异指标预测
   格式：<answer>sequence=0110, responses=3,2,1,5</answer>
   说明：sequence 为要施用的药物串，responses 为逗号分隔的整数预测列表，两者长度必须相等且等于剩余阶段数
   若全部正确则成功；若有错误会告知第几步发生偏差及实际指标，并将预测方案的前面部分强制应用到真实疗程

注意事项：
- 每次只能执行一个操作
- 若疗程填满仍未完成正确的疗程提交，治疗判定为失败
- 请尽可能少地使用操作次数
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Targeted Medication Regimen" inference game. As a clinician, you must understand the rejection pattern of an innovative therapy:

Clinical Setup:
- The patient requires a total of {n} continuous medication stages (0 for Drug A, 1 for Drug B)
- The regimen starts empty, and you administer drugs step by step until the full course is completed
- The patient's body has a hidden accumulation window k and a metabolic model f
- After each dose, the system returns the current "rejection index" (non-negative integer)
- The rejection index depends only on "the most recent doses" (accumulation effect up to k times)
- Identical medication suffix combinations always produce identical rejection indices

Your Goal:
Before the regimen ends, deduce the patient's rejection mechanism and complete a "regimen submission" — plan the remaining medication sequence and corresponding rejection index predictions. If all correct, the treatment succeeds.

Available Operations:

1. Administer Drug: Administer Drug 0 or 1 to the patient
   Format: <append>0</append> or <append>1</append>
   Feedback: Current rejection index, total doses administered, remaining stages

2. In-vitro Simulation (up to {max_simulations} uses): Provide a medication sequence to simulate rejection responses in a biochemical sandbox without affecting the real patient
   Format: <simulate>01101</simulate>
   Feedback: List of rejection indices for each step

3. Medical Record Query: View current doses, remaining stages, and index history
   Format: <query_state></query_state>
   Feedback: Current state information

4. Regimen Submission: Provide remaining medication sequence and corresponding rejection predictions
   Format: <answer>sequence=0110, responses=3,2,1,5</answer>
   Note: sequence is the drug string to administer, responses is a comma-separated integer list; both must equal remaining stages
   If all correct, success; if wrong, will indicate which step deviated and actual index, then enforce the correct prefix to the real regimen

Important:
- Only one operation per turn
- If the course fills up without a successful regimen submission, the treatment fails
- Try to use as few operations as possible
"""

    contextualized_rule_zh_3 = """\
这是一款"自适应学习路径响应"评估系统。你作为教务排课系统，需要分析学生的认知负荷规律：

评估设定：
- 存在一个总长为 {n} 节课的课表计划（每节课只能排布 0:理论课 或 1:实践课）
- 课表从空开始，你需要逐节安排课程直到排满
- 学生的认知系统内包含一个疲劳窗口 k 和负荷计算公式 f
- 每当安排完一节课后，系统会反馈学生当前的"认知负荷分"（非负整数）
- 认知负荷分仅受"最近排布的几节课"影响（影响时长不超过 k 节）
- 相同的课程后缀序列总会产生相同的认知负荷分

你的目标：
在课表排满之前，推断出学生的认知规律，并完成一次"方案提交"——给出剩余所有课时的安排及对应的负荷分预测。若全部正确则评估成功。

可用操作：

1. 安排课程：将 0 或 1 写入本节课表
   格式：<append>0</append> 或 <append>1</append>
   反馈：本节课负荷分、已排课节数、剩余课时

2. 教学推演（最多使用 {max_simulations} 次）：提供一段备选排课序列，在虚拟系统中预估带来的负荷分，不影响真实教学进度
   格式：<simulate>01101</simulate>
   反馈：每节课的负荷分预估列表

3. 课表查询：查看当前已排课时、剩余课时、历史负荷分
   格式：<query_state></query_state>
   反馈：当前状态信息

4. 方案提交：提供剩余课时的排课序列和对应的负荷分预测
   格式：<answer>sequence=0110, responses=3,2,1,5</answer>
   说明：sequence 为要安排的课程序列，responses 为逗号分隔的整数预测列表，两者长度必须相等且等于剩余课时
   若全部正确则成功；若有错误会告知第几节课发生偏差及实际负荷分，并将预测方案的前面部分直接写入真实课表

注意事项：
- 每次只能执行一个操作
- 若课表排满仍未完成正确的方案提交，评估失败
- 请尽可能少地使用操作次数
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's use the "Adaptive Learning Path Response" evaluation system. As the scheduling system, you need to analyze the student's cognitive load pattern:

Evaluation Setup:
- There is a curriculum plan of {n} total classes (each class can only be 0: Theory or 1: Practice)
- The schedule starts empty, and you arrange classes step by step until full
- The student's cognitive system has a fatigue window k and a load formula f
- After scheduling a class, the system returns the current "cognitive load score" (non-negative integer)
- The load score is only affected by "the most recently scheduled classes" (duration up to k classes)
- Identical class suffix sequences always produce identical load scores

Your Goal:
Before the schedule fills up, deduce the student's cognitive pattern and complete a "plan submission" — provide all remaining class arrangements and their corresponding load score predictions. If all correct, you succeed.

Available Operations:

1. Schedule Class: Assign 0 or 1 to the schedule
   Format: <append>0</append> or <append>1</append>
   Feedback: Current class load score, total classes scheduled, remaining classes

2. Teaching Simulation (up to {max_simulations} uses): Provide an alternative class sequence to estimate load scores in the virtual system without affecting the real schedule
   Format: <simulate>01101</simulate>
   Feedback: List of estimated load scores for each class

3. Schedule Query: View current scheduled classes, remaining classes, and load score history
   Format: <query_state></query_state>
   Feedback: Current state information

4. Plan Submission: Provide remaining class sequence and corresponding load score predictions
   Format: <answer>sequence=0110, responses=3,2,1,5</answer>
   Note: sequence is the class string to schedule, responses is a comma-separated integer list; both must equal remaining classes
   If all correct, success; if wrong, will indicate which class deviated and actual score, then enforce the correct prefix to the real schedule

Important:
- Only one operation per turn
- If the schedule fills up without a successful plan submission, the evaluation fails
- Try to use as few operations as possible
"""

    contextualized_rule_zh_4 = """\
这是自动化生产线的"流体管道调控"监控任务。你作为工艺控制工程师，需要摸清阀门系统的压力响应特性：

监控设定：
- 生产工艺需要执行连续 {n} 步的阀门开闭控制（0 代表降压排气，1 代表增压进气）
- 调控序列从空开始，你需要逐步输入指令直到填满整个工艺流程
- 管网内部隐藏着一个迟滞效应窗口 k 和压力换算公式 f
- 每执行一步操作后，管网主传感器会返回当前的"压力偏离值"（非负整数）
- 压力偏离值仅由"最近的几步操作"决定（管网记忆不超过 k 步）
- 相同的操作指令后缀总会产生相同的压力偏离值

你的目标：
在流程填满之前，推断出管网压力的响应规律，并完成一次"工序提交"——给出剩余所有步骤的操作指令及对应的压力偏离值预测。若全部正确则生产合格。

可用操作：

1. 阀门调控：输入指令 0 或 1 到控制系统
   格式：<append>0</append> 或 <append>1</append>
   反馈：本步压力偏离值、已执行步数、剩余工序数

2. 测试推演（最多使用 {max_simulations} 次）：提供一段调控指令串，在仿真环境中模拟管网压力变化，不改变真实产线状态
   格式：<simulate>01101</simulate>
   反馈：每一步的压力偏离值模拟列表

3. 仪表查询：查看当前已执行步数、剩余工序数、历史压力记录
   格式：<query_state></query_state>
   反馈：当前状态信息

4. 工序提交：提供剩余流程的指令串和对应的压力预测
   格式：<answer>sequence=0110, responses=3,2,1,5</answer>
   说明：sequence 为要执行的指令串，responses 为逗号分隔的整数预测列表，两者长度必须相等且等于剩余工序数
   若全部正确则成功；若有错误会告知第几步失控及实际压力值，并将预测工序的前面部分直接应用到真实产线

注意事项：
- 每次只能执行一个操作
- 若流程填满仍未完成正确的工序提交，生产判定为不合格
- 请尽可能少地使用操作次数
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
This is a "Fluid Pipeline Control" monitoring task for the automated production line. As a process control engineer, you need to figure out the pressure response characteristics of the valve system:

Monitoring Setup:
- The production process requires {n} continuous steps of valve control (0 for depressurize, 1 for pressurize)
- The control sequence starts empty, and you input commands step by step until the process is complete
- The pipeline network hides a hysteresis window k and a pressure conversion formula f
- After each operation step, the main sensor returns the current "pressure deviation value" (non-negative integer)
- The pressure deviation is only determined by "the most recent operations" (network memory up to k steps)
- Identical command suffixes always produce identical pressure deviation values

Your Goal:
Before the process fills up, deduce the pipeline pressure response pattern and complete a "process submission" — provide the operation commands for all remaining steps and their corresponding pressure deviation predictions. If all correct, the production passes.

Available Operations:

1. Valve Control: Input command 0 or 1 to the control system
   Format: <append>0</append> or <append>1</append>
   Feedback: Current step pressure deviation, total executed steps, remaining steps

2. Test Simulation (up to {max_simulations} uses): Provide a command string to simulate pipeline pressure changes in a virtual environment without altering the real production line
   Format: <simulate>01101</simulate>
   Feedback: List of simulated pressure deviations for each step

3. Instrument Query: View current executed steps, remaining steps, and pressure history
   Format: <query_state></query_state>
   Feedback: Current state information

4. Process Submission: Provide remaining command string and corresponding pressure predictions
   Format: <answer>sequence=0110, responses=3,2,1,5</answer>
   Note: sequence is the command string to execute, responses is a comma-separated integer list; both must equal remaining steps
   If all correct, success; if wrong, will indicate which step lost control and actual pressure, then apply the correct prefix directly to the real line

Important:
- Only one operation per turn
- If the process fills up without a successful process submission, the production fails
- Try to use as few operations as possible
"""

    contextualized_rule_zh_5 = """\
这是"类案裁判特征分析"辅助系统。你作为法律科技研究员，需要逆向推导系统的量刑计算逻辑：

分析设定：
- 案件审查需要录入长度为 {n} 的证据要素序列（0 代表无此要素，1 代表有此要素）
- 序列从空开始，你需要逐一录入证据要素直到完成全部审查
- 系统内部包含一个隐藏的审查窗口 k 和裁决评估模型 f
- 每次录入一个要素后，系统会返回当前的"量刑建议基准点"（非负整数）
- 基准点仅由"最近录入的若干个要素"共同决定（特征组合跨度不超过 k）
- 相同的要素后缀组合总会计算出相同的量刑基准点

你的目标：
在审查完成前，破解系统的裁判计算逻辑，并完成一次"判决推演提交"——给出剩余所有需录入的要素序列及对应的量刑基准点预测。若全部正确则分析成功。

可用操作：

1. 录入要素：在卷宗中补充要素 0 或 1
   格式：<append>0</append> 或 <append>1</append>
   反馈：当前基准点、已录入总数、剩余待录入数

2. 法庭推演（最多使用 {max_simulations} 次）：提供一段要素序列，在虚拟法庭中测试系统的量刑反馈，不影响真实案件卷宗
   格式：<simulate>01101</simulate>
   反馈：每步推演的基准点列表

3. 卷宗查询：查看当前已录入要素数、剩余待录数、历史基准点变化
   格式：<query_state></query_state>
   反馈：当前状态信息

4. 判决推演提交：提供剩余的要素序列和对应的基准点预测
   格式：<answer>sequence=0110, responses=3,2,1,5</answer>
   说明：sequence 为待录入的要素串，responses 为逗号分隔的整数预测列表，两者长度必须相等且等于剩余待录入数
   若全部正确则成功；若有错误会指出第几步逻辑不符及实际基准点，并将预测要素的前面正确部分固化到真实卷宗中

注意事项：
- 每次只能执行一个操作
- 若卷宗录入填满仍未完成正确的预测提交，分析宣告失败
- 请尽可能少地使用操作次数
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
This is the "Similar Case Judgment Feature Analysis" auxiliary system. As a legal tech researcher, you need to reverse-engineer the system's sentencing calculation logic:

Analysis Setup:
- Case review requires inputting an evidence element sequence of length {n} (0 for absent element, 1 for present element)
- The sequence starts empty, and you input evidence elements one by one until the review is complete
- The system contains a hidden review window k and an evaluation model f
- After inputting each element, the system returns the current "sentencing baseline points" (non-negative integer)
- The baseline points are determined only by "the most recently inputted elements" (feature span up to k)
- Identical element suffix combinations always calculate identical sentencing baseline points

Your Goal:
Before the review completes, crack the system's judgment calculation logic and complete a "judgment derivation submission" — provide the remaining element sequence to input and the corresponding baseline points predictions. If all correct, the analysis succeeds.

Available Operations:

1. Input Element: Append element 0 or 1 to the dossier
   Format: <append>0</append> or <append>1</append>
   Feedback: Current baseline points, total inputted, remaining to input

2. Courtroom Simulation (up to {max_simulations} uses): Provide an element sequence to test the system's sentencing feedback in a virtual court without affecting the real case dossier
   Format: <simulate>01101</simulate>
   Feedback: List of derived baseline points for each step

3. Dossier Query: View current inputted count, remaining elements, and baseline points history
   Format: <query_state></query_state>
   Feedback: Current state information

4. Judgment Derivation Submission: Provide remaining element sequence and corresponding baseline points predictions
   Format: <answer>sequence=0110, responses=3,2,1,5</answer>
   Note: sequence is the element string to input, responses is a comma-separated integer list; both must equal remaining to input
   If all correct, success; if wrong, will point out which step's logic mismatched and actual baseline points, then solidify the correct prefix to the real dossier

Important:
- Only one operation per turn
- If the dossier fills up without a successful prediction submission, the analysis fails
- Try to use as few operations as possible
"""

    tags = ["answer", "append", "simulate", "query_state"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 4, "k": 1, "max_simulations": 3, "function_type": "identity"},
            2: {"n": 6, "k": 2, "max_simulations": 3, "function_type": "xor"},
            3: {"n": 8, "k": 2, "max_simulations": 3, "function_type": "sum"},
            4: {"n": 10, "k": 3, "max_simulations": 3, "function_type": "majority"},
            5: {"n": 12, "k": 3, "max_simulations": 3, "function_type": "complex"},
        },
        "en": {
            1: {"n": 4, "k": 1, "max_simulations": 3, "function_type": "identity"},
            2: {"n": 6, "k": 2, "max_simulations": 3, "function_type": "xor"},
            3: {"n": 8, "k": 2, "max_simulations": 3, "function_type": "sum"},
            4: {"n": 10, "k": 3, "max_simulations": 3, "function_type": "majority"},
            5: {"n": 12, "k": 3, "max_simulations": 3, "function_type": "complex"},
        },
    }

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.n = cfg["n"]
        self.k = cfg["k"]
        self.max_simulations = cfg["max_simulations"]
        self.function_type = cfg["function_type"]
        
        self._game_info["n"] = self.n
        self._game_info["max_simulations"] = self.max_simulations
        
        self.sequence = []
        self.responses = []
        self.simulation_count = 0

    def _compute_response(self, sequence: List[int]) -> int:
        if len(sequence) == 0:
            return 0
        
        window_size = min(self.k, len(sequence))
        suffix = sequence[-window_size:]
        
        if self.function_type == "identity":
            return suffix[-1]
        
        elif self.function_type == "xor":
            result = 0
            for bit in suffix:
                result ^= bit
            return result
        
        elif self.function_type == "sum":
            return sum(suffix)
        
        elif self.function_type == "majority":
            ones = sum(suffix)
            zeros = len(suffix) - ones
            return 1 if ones > zeros else 0
        
        elif self.function_type == "complex":
            result = 0
            for i, bit in enumerate(reversed(suffix)):
                result += bit * (2 ** i)
            return result % 5
        
        else:
            raise ValueError(f"Unknown function type: {self.function_type}")

    def _handle_append(self, symbol_str: str) -> str:
        if len(self.sequence) >= self.n:
            return "错误：序列已满，无法追加。" if self.config.language == "zh" else "Error: Sequence is full."
        
        symbol_str = symbol_str.strip()
        if symbol_str not in ["0", "1"]:
            return "错误：只能追加 0 或 1。" if self.config.language == "zh" else "Error: Can only append 0 or 1."
        
        symbol = int(symbol_str)
        self.sequence.append(symbol)
        
        response = self._compute_response(self.sequence)
        self.responses.append(response)
        
        appended = len(self.sequence)
        remaining = self.n - appended
        
        if self.config.language == "zh":
            return f"响应值：{response}，已追加：{appended}，剩余容量：{remaining}"
        else:
            return f"Response: {response}, Appended: {appended}, Remaining: {remaining}"

    def _handle_simulate(self, binary_str: str) -> str:
        if self.simulation_count >= self.max_simulations:
            return f"错误：模拟次数已达上限（{self.max_simulations}次）。" if self.config.language == "zh" \
                else f"Error: Simulation limit reached ({self.max_simulations} times)."
        
        binary_str = binary_str.strip()
        if not all(c in "01" for c in binary_str):
            return "错误：模拟串只能包含 0 和 1。" if self.config.language == "zh" \
                else "Error: Simulation string can only contain 0 and 1."
        
        if len(binary_str) == 0:
            return "错误：模拟串不能为空。" if self.config.language == "zh" \
                else "Error: Simulation string cannot be empty."
        
        if len(self.sequence) + len(binary_str) > self.n:
            return "错误：模拟串过长，会超出总容量。" if self.config.language == "zh" \
                else "Error: Simulation string too long, would exceed capacity."
        
        simulated_responses = []
        temp_sequence = self.sequence.copy()
        
        for char in binary_str:
            symbol = int(char)
            temp_sequence.append(symbol)
            response = self._compute_response(temp_sequence)
            simulated_responses.append(response)
        
        self.simulation_count += 1
        
        responses_str = ",".join(map(str, simulated_responses))
        if self.config.language == "zh":
            return f"模拟响应序列：[{responses_str}]，已使用模拟次数：{self.simulation_count}/{self.max_simulations}"
        else:
            return f"Simulated responses: [{responses_str}], Simulations used: {self.simulation_count}/{self.max_simulations}"

    def _handle_query_state(self) -> str:
        appended = len(self.sequence)
        remaining = self.n - appended
        
        if len(self.responses) > 0:
            responses_str = ",".join(map(str, self.responses))
        else:
            responses_str = "无" if self.config.language == "zh" else "None"
        
        if self.config.language == "zh":
            return f"已追加：{appended}，剩余容量：{remaining}，历史响应：[{responses_str}]"
        else:
            return f"Appended: {appended}, Remaining: {remaining}, Response history: [{responses_str}]"

    def evaluate(self, parsed_info: Dict[str, str]) -> bool:
        raw_ans = parsed_info["answer"]
        
        ans_dict = {}
        try:
            parts = raw_ans.split(",")
            for part in parts:
                part = part.strip()
                if "=" in part:
                    k, v = part.split("=", 1)
                    k = k.strip().lower()
                    v = v.strip()
                    
                    if k == "sequence":
                        ans_dict["sequence"] = v
                    elif k == "responses":
                        ans_dict["responses"] = v
        except:
            return False
        
        if "sequence" not in ans_dict or "responses" not in ans_dict:
            return False
        
        try:
            pred_sequence = ans_dict["sequence"]
            pred_responses_str = ans_dict["responses"]
            
            if not all(c in "01" for c in pred_sequence):
                return False
            
            pred_symbols = [int(c) for c in pred_sequence]
            pred_responses = [int(x.strip()) for x in pred_responses_str.split(",") if x.strip()]
            
        except:
            return False
        
        remaining = self.n - len(self.sequence)
        if len(pred_symbols) != remaining or len(pred_responses) != remaining:
            return False
        
        temp_sequence = self.sequence.copy()
        for i, symbol in enumerate(pred_symbols):
            temp_sequence.append(symbol)
            actual_response = self._compute_response(temp_sequence)
            
            if actual_response != pred_responses[i]:
                for j in range(i + 1):
                    self.sequence.append(pred_symbols[j])
                    self.responses.append(self._compute_response(self.sequence))
                
                self._last_error_step = i + 1
                self._last_error_actual = actual_response
                self._last_error_predicted = pred_responses[i]
                
                return False
        
        for symbol in pred_symbols:
            self.sequence.append(symbol)
            self.responses.append(self._compute_response(self.sequence))
        
        return True

    def _cf_core_produce(self, parsed_info: Dict[str, str]) -> str:
        if "append" in parsed_info:
            return self._handle_append(parsed_info["append"])
        elif "simulate" in parsed_info:
            return self._handle_simulate(parsed_info["simulate"])
        elif "query_state" in parsed_info:
            return self._handle_query_state()
        else:
            raise ValueError("No valid operation tag found.")

    def step(self, response: str) -> 'GameState':
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                
                if is_success:
                    res = "预测全部正确！游戏成功。" if self.config.language == "zh" \
                        else "All predictions correct! Game succeeded."
                    self.state.set_state("success", "correct prediction")
                    self.state.add_message("user", res)
                else:
                    if self.config.language == "zh":
                        res = f"第 {self._last_error_step} 步预测错误。预测响应：{self._last_error_predicted}，实际响应：{self._last_error_actual}。已将预测序列的前 {self._last_error_step} 个符号追加到真实序列。"
                    else:
                        res = f"Prediction error at step {self._last_error_step}. Predicted: {self._last_error_predicted}, Actual: {self._last_error_actual}. First {self._last_error_step} symbols of prediction have been appended to real sequence."
                    
                    if len(self.sequence) >= self.n:
                        if self.config.language == "zh":
                            res += " 序列已满，游戏失败。"
                        else:
                            res += " Sequence is now full. Game failed."
                        self.state.set_state("failed", "sequence full without success")
                    else:
                        if self.config.language == "zh":
                            res += f" 当前已追加：{len(self.sequence)}，剩余容量：{self.n - len(self.sequence)}。"
                        else:
                            res += f" Current appended: {len(self.sequence)}, Remaining: {self.n - len(self.sequence)}."
                        self.state.set_state("failed", "incorrect prediction")
                    
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
                if len(self.sequence) >= self.n and self.state.state == "in_progress":
                    if self.config.language == "zh":
                        fail_msg = "序列已填满，但未完成正确的预测提交。游戏失败。"
                    else:
                        fail_msg = "Sequence is full without successful prediction submission. Game failed."
                    self.state.set_state("failed", "sequence full without prediction")
                    self.state.add_message("user", fail_msg)
                
        except Exception as e:
            self.state.set_state("failed", f"parse or execution error: {str(e)}")
        
        return self.state

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        queries = []
        
        appended = len(self.sequence)
        remaining = self.n - appended
        
        if len(self.responses) > 0:
            responses_str = ",".join(map(str, self.responses))
        else:
            responses_str = "无" if self.config.language == "zh" else "None"
        
        if self.config.language == "zh":
            qs_ans = f"已追加：{appended}，剩余容量：{remaining}，历史响应：[{responses_str}]"
        else:
            qs_ans = f"Appended: {appended}, Remaining: {remaining}, Response history: [{responses_str}]"
            
        queries.append({"query": "<query_state></query_state>", "answer": qs_ans})

        if appended >= self.n:
            return queries

        for bit in [0, 1]:
            temp_seq = self.sequence + [bit]
            resp = self._compute_response(temp_seq)
            
            new_appended = appended + 1
            new_remaining = remaining - 1
            
            if self.config.language == "zh":
                ans = f"响应值：{resp}，已追加：{new_appended}，剩余容量：{new_remaining}"
            else:
                ans = f"Response: {resp}, Appended: {new_appended}, Remaining: {new_remaining}"
            
            queries.append({"query": f"<append>{bit}</append>", "answer": ans})

        if self.simulation_count < self.max_simulations:
            max_sim_len = min(remaining, 4)
            
            for length in range(1, max_sim_len + 1):
                for bits in itertools.product([0, 1], repeat=length):
                    binary_str = "".join(map(str, bits))
                    
                    simulated_responses = []
                    temp_sequence = self.sequence.copy()
                    
                    for char in binary_str:
                        symbol = int(char)
                        temp_sequence.append(symbol)
                        response = self._compute_response(temp_sequence)
                        simulated_responses.append(response)
                    
                    next_sim_count = self.simulation_count + 1
                    responses_str_sim = ",".join(map(str, simulated_responses))
                    
                    if self.config.language == "zh":
                        ans = f"模拟响应序列：[{responses_str_sim}]，已使用模拟次数：{next_sim_count}/{self.max_simulations}"
                    else:
                        ans = f"Simulated responses: [{responses_str_sim}], Simulations used: {next_sim_count}/{self.max_simulations}"
                    
                    queries.append({"query": f"<simulate>{binary_str}</simulate>", "answer": ans})

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        is_zh = self.config.language == "zh"

        if is_zh:
            m = re.match(r'^响应值：(\d+)，', correct)
            if m:
                orig = int(m.group(1))
                wrong_val = orig + 1
                return correct.replace(f"响应值：{orig}，", f"响应值：{wrong_val}，", 1)
        else:
            m = re.match(r'^Response: (\d+),', correct)
            if m:
                orig = int(m.group(1))
                wrong_val = orig + 1
                return correct.replace(f"Response: {orig},", f"Response: {wrong_val},", 1)

        if is_zh:
            m = re.search(r'模拟响应序列：\[([^\]]*)\]', correct)
            if m:
                orig_list = m.group(1)
                nums = orig_list.split(",")
                if nums and nums[0].strip().lstrip("-").isdigit():
                    wrong_first = str(int(nums[0].strip()) + 1)
                    wrong_list = ",".join([wrong_first] + nums[1:])
                    return correct.replace(
                        f"模拟响应序列：[{orig_list}]",
                        f"模拟响应序列：[{wrong_list}]",
                        1
                    )
        else:
            m = re.search(r'Simulated responses: \[([^\]]*)\]', correct)
            if m:
                orig_list = m.group(1)
                nums = orig_list.split(",")
                if nums and nums[0].strip().lstrip("-").isdigit():
                    wrong_first = str(int(nums[0].strip()) + 1)
                    wrong_list = ",".join([wrong_first] + nums[1:])
                    return correct.replace(
                        f"Simulated responses: [{orig_list}]",
                        f"Simulated responses: [{wrong_list}]",
                        1
                    )

        return correct + "_WRONG"