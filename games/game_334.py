from .base import Game
import re
import random as _random

class SequenceRecoveryGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"序列恢复"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列 a1, a2, ..., a{n}，其中每个元素 ai 均为非负整数。序列长度 {n} 已公开，但序列中每个元素的具体值对你不可见。

你的目标是通过有限次数的查询，推理出序列中每个位置的精确值。

你可以向我发起以下两种查询：

1. **两邻项和查询**：询问位置 i 和 i+1 两个相邻元素的和，即 ai + a(i+1)。索引 i 的有效范围是 1 到 {n_minus_1}。

2. **三邻项和查询**：询问位置 i、i+1、i+2 三个相邻元素的和，即 ai + a(i+1) + a(i+2)。索引 i 的有效范围是 1 到 {n_minus_2}。**此类查询在整个游戏过程中最多只能使用一次。**

- 总查询次数（两邻项和查询次数 + 三邻项和查询次数）不能超过 {n} 次。
- 三邻项和查询最多使用一次。
- 若索引超出有效范围、超过总查询次数限制、或三邻项和查询超过一次，系统将返回错误提示。

每次查询只能包含一个标签，使用以下 XML 格式：

- 两邻项和查询（例如查询位置 1 和 2 的和）：
<query_pair>1</query_pair>

- 三邻项和查询（例如查询位置 2、3、4 的和）：
<query_triple>2</query_triple>

当你收集到足够信息后，请提交最终答案。答案必须是一个长度为 {n} 的非负整数序列，按位置从 1 到 {n} 依次给出，元素之间用逗号分隔：

<answer>a1,a2,a3,...,a{n}</answer>

例如，若序列长度为 5，你推理出的序列为 3, 1, 4, 1, 5，则提交：
<answer>3,1,4,1,5</answer>

若答案与真实序列不符或格式错误，游戏将失败。请尽可能少地使用查询次数完成推理。
"""

    game_rule_en = """\
Let's play a "Sequence Recovery" deduction game. Here are the rules:

There is an ordered sequence of length {n}: a1, a2, ..., a{n}, where each element ai is a non-negative integer. The length {n} is publicly known, but the specific values of the elements are hidden from you.

Your goal is to infer the exact value at each position through a limited number of queries.

You can make the following two types of queries:

1. **Pair Sum Query**: Ask for the sum of two adjacent elements at positions i and i+1, i.e., ai + a(i+1). Valid index range for i is 1 to {n_minus_1}.

2. **Triple Sum Query**: Ask for the sum of three adjacent elements at positions i, i+1, and i+2, i.e., ai + a(i+1) + a(i+2). Valid index range for i is 1 to {n_minus_2}. **This type of query can be used at most once throughout the entire game.**

- Total number of queries (pair sum queries + triple sum queries) cannot exceed {n}.
- Triple sum query can be used at most once.
- If the index is out of valid range, total query limit is exceeded, or triple sum query is used more than once, the system will return an error message.

Each query must contain only one tag, using the following XML format:

- Pair Sum Query (e.g., querying the sum of positions 1 and 2):
<query_pair>1</query_pair>

- Triple Sum Query (e.g., querying the sum of positions 2, 3, and 4):
<query_triple>2</query_triple>

When you have collected enough information, submit your final answer. The answer must be a sequence of {n} non-negative integers, listed in order from position 1 to {n}, separated by commas:

<answer>a1,a2,a3,...,a{n}</answer>

For example, if the sequence length is 5 and your inferred sequence is 3, 1, 4, 1, 5, submit:
<answer>3,1,4,1,5</answer>

If the answer does not match the true sequence or the format is incorrect, the game will fail. Try to complete the reasoning with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行“交通主干道车流特征分析”任务，规则如下：

市中心的一条主干道被划分为 {n} 个连续的监控路段（编号1到{n}）。系统已知总路段数 {n}，但每个路段当前的滞留车辆数（非负整数）由于前端传感器故障暂时不可见。

你的目标是通过调度有限的备用监测设备，精准推断出每个路段的具体车辆数。

你可以下达以下两种指令：

1. **双路段联动流调**：查询第 i 和第 i+1 两个相邻路段的车辆总和。输入参数 i 的有效范围是 1 到 {n_minus_1}。

2. **三路段无人机巡查**：查询第 i、i+1、i+2 三个相邻路段的车辆总和。输入参数 i 的有效范围是 1 到 {n_minus_2}。**由于空域管制，此类巡查在整个任务中最多只能执行一次。**

- 总查询次数（双路段联动流调 + 三路段无人机巡查）不能超过 {n} 次。
- 三路段无人机巡查最多使用一次。
- 若索引超出有效范围、超过总查询次数限制、或多次调用无人机巡查，系统将返回错误提示。

每次指令只能包含一个标签，使用以下 XML 格式：

- 双路段联动流调（例如查询路段 1 和 2 的总和）：
<query_pair>1</query_pair>

- 三路段无人机巡查（例如查询路段 2、3、4 的总和）：
<query_triple>2</query_triple>

当你收集到足够信息后，请提交最终流调报告。报告必须是一个长度为 {n} 的非负整数序列，按路段从 1 到 {n} 依次给出，数值之间用逗号分隔：

<answer>a1,a2,a3,...,a{n}</answer>

例如，若路段总数为 5，你推理出的车辆分布为 3, 1, 4, 1, 5，则提交：
<answer>3,1,4,1,5</answer>

若报告与真实数据不符或格式错误，任务将宣告失败。请尽可能高效地调度监测指令完成分析。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's perform the "Arterial Traffic Flow Analysis" task. Here are the rules:

A main arterial road in the city center is divided into {n} consecutive monitored segments (numbered 1 to {n}). The total number of segments {n} is known, but the current number of stranded vehicles (a non-negative integer) in each segment is temporarily invisible due to frontend sensor failures.

Your goal is to accurately infer the specific number of vehicles in each segment by dispatching a limited number of backup monitoring devices.

You can issue the following two types of commands:

1. **Dual-Segment Linked Survey**: Query the total number of vehicles in two adjacent segments, i and i+1. The valid range for parameter i is 1 to {n_minus_1}.

2. **Tri-Segment Drone Patrol**: Query the total number of vehicles in three adjacent segments, i, i+1, and i+2. The valid range for parameter i is 1 to {n_minus_2}. **Due to airspace control, this type of patrol can be executed at most once throughout the entire task.**

- The total number of queries (Dual-Segment Linked Survey + Tri-Segment Drone Patrol) cannot exceed {n}.
- The Tri-Segment Drone Patrol can be used at most once.
- If the index is out of the valid range, the total query limit is exceeded, or the drone patrol is used more than once, the system will return an error message.

Each command must contain only one tag, using the following XML format:

- Dual-Segment Linked Survey (e.g., querying the sum of segments 1 and 2):
<query_pair>1</query_pair>

- Tri-Segment Drone Patrol (e.g., querying the sum of segments 2, 3, and 4):
<query_triple>2</query_triple>

When you have collected enough information, please submit your final report. The report must be a sequence of {n} non-negative integers, listed in order from segment 1 to {n}, separated by commas:

<answer>a1,a2,a3,...,a{n}</answer>

For example, if the total number of segments is 5 and your inferred vehicle distribution is 3, 1, 4, 1, 5, submit:
<answer>3,1,4,1,5</answer>

If the report does not match the actual data or the format is incorrect, the task will fail. Try to complete the analysis using as few monitoring commands as possible.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行“靶向药物阶梯剂量推演”任务，规则如下：

一项临床治疗方案包含 {n} 个连续的给药周期（编号1到{n}）。周期总数 {n} 已知，但每个周期具体的药物剂量（非负整数，单位：毫克）对盲法评估人员不可见。

你的目标是通过调阅有限的联合代谢物检测报告，逆向推导每个周期的精确给药剂量。

你可以发起以下两种化验单查询：

1. **双周期代谢物联合化验**：查询第 i 和第 i+1 两个相邻周期的剂量之和。参数 i 的有效范围是 1 到 {n_minus_1}。

2. **三周期深度靶向筛查**：查询第 i、i+1、i+2 三个相邻周期的剂量之和。参数 i 的有效范围是 1 到 {n_minus_2}。**因该项筛查会消耗极珍贵的生物样本，整个评估过程中最多只能使用一次。**

- 总查询次数（双周期化验 + 三周期筛查）不能超过 {n} 次。
- 三周期深度靶向筛查最多使用一次。
- 若周期索引超出有效范围、超过总查询次数限制、或多次调用深度筛查，系统将返回错误提示。

每次查询只能包含一个标签，使用以下 XML 格式：

- 双周期代谢物联合化验（例如查询周期 1 和 2 的总剂量）：
<query_pair>1</query_pair>

- 三周期深度靶向筛查（例如查询周期 2、3、4 的总剂量）：
<query_triple>2</query_triple>

当数据收集完成后，请提交最终剂量评估报告。报告必须是一个长度为 {n} 的非负整数序列，按周期从 1 到 {n} 依次给出，数值之间用逗号分隔：

<answer>a1,a2,a3,...,a{n}</answer>

例如，若周期总数为 5，你推演出的剂量序列为 3, 1, 4, 1, 5，则提交：
<answer>3,1,4,1,5</answer>

若报告与真实处方不符或格式错误，评估将失败。请在确保证据充分的前提下尽量减少化验次数。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's perform the "Targeted Drug Step-Dose Deduction" task. Here are the rules:

A clinical treatment plan consists of {n} consecutive dosing cycles (numbered 1 to {n}). The total number of cycles {n} is known, but the specific drug dosage (a non-negative integer in mg) for each cycle is blinded to the evaluating staff.

Your goal is to reverse-engineer the precise dosage administered in each cycle by reviewing a limited number of joint metabolite test reports.

You can initiate the following two types of lab queries:

1. **Dual-Cycle Metabolite Joint Test**: Query the total combined dosage of two adjacent cycles, i and i+1. The valid range for parameter i is 1 to {n_minus_1}.

2. **Tri-Cycle Deep Targeted Screening**: Query the total combined dosage of three adjacent cycles, i, i+1, and i+2. The valid range for parameter i is 1 to {n_minus_2}. **Because this screening consumes extremely precious biological samples, it can be used at most once during the entire evaluation.**

- The total number of queries (Dual-Cycle Test + Tri-Cycle Screening) cannot exceed {n}.
- The Tri-Cycle Deep Targeted Screening can be used at most once.
- If the index is out of the valid range, the total query limit is exceeded, or the deep screening is used more than once, the system will return an error message.

Each query must contain only one tag, using the following XML format:

- Dual-Cycle Metabolite Joint Test (e.g., querying the total dose of cycles 1 and 2):
<query_pair>1</query_pair>

- Tri-Cycle Deep Targeted Screening (e.g., querying the total dose of cycles 2, 3, and 4):
<query_triple>2</query_triple>

When data collection is complete, please submit the final dosage evaluation report. The report must be a sequence of {n} non-negative integers, listed in order from cycle 1 to {n}, separated by commas:

<answer>a1,a2,a3,...,a{n}</answer>

For example, if there are 5 cycles and your deduced dosage sequence is 3, 1, 4, 1, 5, submit:
<answer>3,1,4,1,5</answer>

If the report does not match the actual prescription or the format is incorrect, the evaluation will fail. Try to minimize the number of tests while ensuring sufficient evidence.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行“进阶式课程学时评估”任务，规则如下：

一套核心专业课程由 {n} 个连续的教学模块（编号1到{n}）组成。模块总数 {n} 为公开信息，但每个模块系统分配的标准学时（非负整数）对你隐藏。

你的目标是通过有限次跨模块考核数据的调用，准确推断出所有模块的独立学时。

你可以向教务系统发起以下两种查询：

1. **双模块联合考核用时**：查询第 i 和第 i+1 两个相邻模块的标准学时总和。索引 i 的有效范围是 1 到 {n_minus_1}。

2. **三模块综合定级测试用时**：查询第 i、i+1、i+2 三个相邻模块的标准学时总和。索引 i 的有效范围是 1 到 {n_minus_2}。**由于防作弊风控机制，此类综合查询在整个评估中最多只能调用一次。**

- 总查询次数（双模块查询 + 三模块查询）不能超过 {n} 次。
- 三模块综合定级测试查询最多使用一次。
- 若模块索引超出有效范围、超过总查询次数限制、或多次调用三模块查询，系统将返回错误提示。

每次查询只能包含一个标签，使用以下 XML 格式：

- 双模块联合考核用时（例如查询模块 1 和 2 的学时总和）：
<query_pair>1</query_pair>

- 三模块综合定级测试用时（例如查询模块 2、3、4 的学时总和）：
<query_triple>2</query_triple>

当确认各模块课时后，请提交最终课表规划。报告必须是一个长度为 {n} 的非负整数序列，按模块从 1 到 {n} 依次给出，数值之间用逗号分隔：

<answer>a1,a2,a3,...,a{n}</answer>

例如，若模块总数为 5，你推断出的学时分配为 3, 1, 4, 1, 5，则提交：
<answer>3,1,4,1,5</answer>

若规划与教务大纲不符或格式错误，评估将被驳回。请合理利用查询次数完成学时逆推。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform the "Progressive Curriculum Hours Evaluation" task. Here are the rules:

A core professional course consists of {n} consecutive teaching modules (numbered 1 to {n}). The total number of modules {n} is public knowledge, but the standard credit hours (a non-negative integer) allocated to each individual module are hidden from you.

Your goal is to accurately deduce the independent hours of all modules by invoking cross-module assessment data a limited number of times.

You can initiate the following two types of queries to the academic system:

1. **Dual-Module Joint Assessment Time**: Query the total standard hours of two adjacent modules, i and i+1. The valid range for index i is 1 to {n_minus_1}.

2. **Tri-Module Comprehensive Placement Test Time**: Query the total standard hours of three adjacent modules, i, i+1, and i+2. The valid range for index i is 1 to {n_minus_2}. **Due to anti-cheating risk control mechanisms, this comprehensive query can be invoked at most once throughout the evaluation.**

- The total number of queries (Dual-Module Query + Tri-Module Query) cannot exceed {n}.
- The Tri-Module Comprehensive Placement Test can be used at most once.
- If the module index is out of the valid range, the total query limit is exceeded, or the tri-module query is invoked more than once, the system will return an error message.

Each query must contain only one tag, using the following XML format:

- Dual-Module Joint Assessment Time (e.g., querying the total hours of modules 1 and 2):
<query_pair>1</query_pair>

- Tri-Module Comprehensive Placement Test Time (e.g., querying the total hours of modules 2, 3, and 4):
<query_triple>2</query_triple>

When the hours for each module are confirmed, please submit the final syllabus plan. The report must be a sequence of {n} non-negative integers, listed in order from module 1 to {n}, separated by commas:

<answer>a1,a2,a3,...,a{n}</answer>

For example, if there are 5 modules and your deduced hour allocation is 3, 1, 4, 1, 5, submit:
<answer>3,1,4,1,5</answer>

If the plan does not match the academic syllabus or the format is incorrect, the evaluation will be rejected. Please utilize your query limits reasonably to complete the reverse calculation.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行“流水线工位产能排查”任务，规则如下：

一条精密制造流水线包含 {n} 个连续的装配工位（编号1到{n}）。工位总数 {n} 已知，但由于中央面板故障，每个工位当前的实际产出件数（非负整数）显示为乱码并对你隐藏。

你的目标是通过调取有限的区间复检记录，精确还原出每个工位的实际产能数据。

你可以通过 SCADA 系统发起以下两种区间查询：

1. **双工位缓冲段计数**：查询第 i 和第 i+1 两个相邻工位的产出总件数。索引 i 的有效范围是 1 到 {n_minus_1}。

2. **三工位全检抽测**：查询第 i、i+1、i+2 三个相邻工位的产出总件数。索引 i 的有效范围是 1 到 {n_minus_2}。**由于全检会导致产线短暂停机，该指令在整个排查过程中最多只能使用一次。**

- 总查询次数（双工位计数 + 三工位抽测）不能超过 {n} 次。
- 三工位全检抽测最多使用一次。
- 若索引超出有效范围、超过总查询次数限制、或多次触发全检抽测，系统将返回错误提示。

每次查询只能包含一个标签，使用以下 XML 格式：

- 双工位缓冲段计数（例如查询工位 1 和 2 的总件数）：
<query_pair>1</query_pair>

- 三工位全检抽测（例如查询工位 2、3、4 的总件数）：
<query_triple>2</query_triple>

当你收集到足够信息后，请提交最终产能修复报告。报告必须是一个长度为 {n} 的非负整数序列，按工位从 1 到 {n} 依次给出，数值之间用逗号分隔：

<answer>a1,a2,a3,...,a{n}</answer>

例如，若工位总数为 5，你还原出的产出序列为 3, 1, 4, 1, 5，则提交：
<answer>3,1,4,1,5</answer>

若报告与物理台账不符或格式错误，排查任务将失败。请用最少的系统资源完成产能还原。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's perform the "Assembly Line Station Capacity Audit" task. Here are the rules:

A precision manufacturing assembly line contains {n} consecutive assembly stations (numbered 1 to {n}). The total number of stations {n} is known, but due to a central panel malfunction, the current actual production output (a non-negative integer in pieces) of each station is displayed as garbled text and hidden from you.

Your goal is to accurately reconstruct the actual capacity data for each station by retrieving a limited number of interval re-inspection records.

You can initiate the following two types of interval queries via the SCADA system:

1. **Dual-Station Buffer Zone Count**: Query the total production output of two adjacent stations, i and i+1. The valid range for index i is 1 to {n_minus_1}.

2. **Tri-Station Full Inspection Sampling**: Query the total production output of three adjacent stations, i, i+1, and i+2. The valid range for index i is 1 to {n_minus_2}. **Because a full inspection causes brief production line downtime, this command can be used at most once throughout the entire audit.**

- The total number of queries (Dual-Station Count + Tri-Station Sampling) cannot exceed {n}.
- The Tri-Station Full Inspection Sampling can be used at most once.
- If the index is out of the valid range, the total query limit is exceeded, or the full inspection is triggered more than once, the system will return an error message.

Each query must contain only one tag, using the following XML format:

- Dual-Station Buffer Zone Count (e.g., querying the total output of stations 1 and 2):
<query_pair>1</query_pair>

- Tri-Station Full Inspection Sampling (e.g., querying the total output of stations 2, 3, and 4):
<query_triple>2</query_triple>

When you have collected enough information, please submit the final capacity restoration report. The report must be a sequence of {n} non-negative integers, listed in order from station 1 to {n}, separated by commas:

<answer>a1,a2,a3,...,a{n}</answer>

For example, if the total number of stations is 5 and your reconstructed output sequence is 3, 1, 4, 1, 5, submit:
<answer>3,1,4,1,5</answer>

If the report does not match the physical ledger or the format is incorrect, the audit task will fail. Try to restore the capacity data using the minimum amount of system resources.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行“隐匿资金链穿透追踪”任务，规则如下：

在一次反洗钱调查中，确认嫌疑人使用了 {n} 个连续的离岸连环账户（编号1到{n}）进行资金转移。账户总数 {n} 已知，但每个账户沉淀的非法资金额（非负整数，单位：万）被严格加密隐藏。

你的目标是通过向国际金融合规网络提交有限的审计申请，精准查清每个账户的具体留存金额。

你可以提交以下两种类型的联合审计：

1. **双账户常规协查**：查询第 i 和第 i+1 两个相邻账户的资金总和。账户索引 i 的有效范围是 1 到 {n_minus_1}。

2. **三账户穿透式特调**：查询第 i、i+1、i+2 三个相邻账户的资金总和。账户索引 i 的有效范围是 1 到 {n_minus_2}。**此类特调需要高级别司法授权，在整个案件侦查中最多只能获批使用一次。**

- 总查询次数（双账户协查 + 三账户特调）不能超过 {n} 次。
- 三账户穿透式特调最多使用一次。
- 若账户索引超出有效范围、超过总查询次数限制、或违规多次提交特调申请，系统将返回错误提示。

每次审计申请只能包含一个标签，使用以下 XML 格式：

- 双账户常规协查（例如查询账户 1 和 2 的资金和）：
<query_pair>1</query_pair>

- 三账户穿透式特调（例如查询账户 2、3、4 的资金和）：
<query_triple>2</query_triple>

当你锁定所有证据后，请提交最终查封卷宗。卷宗内容必须是一个长度为 {n} 的非负整数序列，按账户从 1 到 {n} 依次给出，金额之间用逗号分隔：

<answer>a1,a2,a3,...,a{n}</answer>

例如，若嫌疑账户总数为 5，你查实的资金分布为 3, 1, 4, 1, 5，则提交：
<answer>3,1,4,1,5</answer>

若卷宗与实际流水不符或格式错误，指控将因证据链断裂而失败。请在确凿推演的基础上以最少的申请次数破案。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's perform the "Hidden Funds Chain Penetration Tracking" task. Here are the rules:

In an anti-money laundering investigation, it has been confirmed that a suspect used {n} consecutive offshore chained accounts (numbered 1 to {n}) for fund transfers. The total number of accounts {n} is known, but the illicit fund amount (a non-negative integer, in ten-thousands) deposited in each account is strictly encrypted and hidden.

Your goal is to accurately determine the specific retained amount in each account by submitting a limited number of audit requests to the international financial compliance network.

You can submit the following two types of joint audits:

1. **Dual-Account Routine Coordination**: Query the total funds of two adjacent accounts, i and i+1. The valid range for account index i is 1 to {n_minus_1}.

2. **Tri-Account Penetrative Special Probe**: Query the total funds of three adjacent accounts, i, i+1, and i+2. The valid range for account index i is 1 to {n_minus_2}. **This type of special probe requires a high-level judicial warrant and can be approved for use at most once during the entire case investigation.**

- The total number of queries (Dual-Account Coordination + Tri-Account Probe) cannot exceed {n}.
- The Tri-Account Penetrative Special Probe can be used at most once.
- If the account index is out of the valid range, the total query limit is exceeded, or multiple probe requests are submitted in violation of protocols, the system will return an error message.

Each audit request must contain only one tag, using the following XML format:

- Dual-Account Routine Coordination (e.g., querying the sum of accounts 1 and 2):
<query_pair>1</query_pair>

- Tri-Account Penetrative Special Probe (e.g., querying the sum of accounts 2, 3, and 4):
<query_triple>2</query_triple>

When you have locked in all the evidence, please submit the final seizure dossier. The dossier content must be a sequence of {n} non-negative integers, listed in order from account 1 to {n}, separated by commas:

<answer>a1,a2,a3,...,a{n}</answer>

For example, if the total number of suspect accounts is 5 and your verified fund distribution is 3, 1, 4, 1, 5, submit:
<answer>3,1,4,1,5</answer>

If the dossier does not match the actual transaction logs or the format is incorrect, the prosecution will fail due to a broken chain of evidence. Please solve the case with the minimum number of requests based on solid deductions.
"""

    tags = ["answer", "query_pair", "query_triple"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 3,
                "sequence": [2, 3, 5],
            },
            2: {
                "n": 4,
                "sequence": [1, 4, 2, 7],
            },
            3: {
                "n": 5,
                "sequence": [3, 0, 5, 1, 4],
            },
            4: {
                "n": 6,
                "sequence": [2, 5, 1, 8, 3, 6],
            },
            5: {
                "n": 8,
                "sequence": [1, 7, 2, 9, 0, 4, 6, 3],
            },
        },
        "en": {
            1: {
                "n": 3,
                "sequence": [2, 3, 5],
            },
            2: {
                "n": 4,
                "sequence": [1, 4, 2, 7],
            },
            3: {
                "n": 5,
                "sequence": [3, 0, 5, 1, 4],
            },
            4: {
                "n": 6,
                "sequence": [2, 5, 1, 8, 3, 6],
            },
            5: {
                "n": 8,
                "sequence": [1, 7, 2, 9, 0, 4, 6, 3],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        n = cfg["n"]
        sequence = cfg["sequence"]

        self._game_info["n"] = n
        self._game_info["n_minus_1"] = n - 1
        self._game_info["n_minus_2"] = n - 2

        self.sequence = [None] + list(sequence)

        self.query_count = 0
        self.triple_query_count = 0
        self.max_queries = n

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            ans_list = [int(x.strip()) for x in raw_ans.split(",")]
            
            if len(ans_list) != self._game_info["n"]:
                return False
            
            if any(x < 0 for x in ans_list):
                return False
            
            true_sequence = self.sequence[1:]
            return ans_list == true_sequence
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_out_of_range = "错误：索引超出有效范围。"
            error_triple_limit = "错误：三邻项和查询已超过一次使用限制。"
            error_invalid_index = "错误：索引格式无效。"
            error_multiple_tags = "错误：每次查询只能包含一个标签，请勿同时使用两种查询类型。"
        else:
            error_out_of_range = "Error: Index out of valid range."
            error_triple_limit = "Error: Triple sum query limit exceeded (max 1)."
            error_invalid_index = "Error: Invalid index format."
            error_multiple_tags = "Error: Each query must contain only one tag. Do not use both query types at once."

        n = self._game_info["n"]

        has_pair = "query_pair" in parsed_info
        has_triple = "query_triple" in parsed_info
        if has_pair and has_triple:
            return error_multiple_tags

        if self.query_count >= self.max_queries:
            if self.config.language == "zh":
                return "错误：已达到最大查询次数限制（{}/{}）。请不要再进行查询，直接提交你的最终答案。".format(
                    self.query_count, self.max_queries)
            else:
                return "Error: Maximum query limit reached ({}/{}). Please stop querying and submit your final answer now.".format(
                    self.query_count, self.max_queries)

        if has_pair:
            try:
                i = int(parsed_info["query_pair"].strip())
                
                if i < 1 or i > n - 1:
                    return error_out_of_range
                
                self.query_count += 1
                
                result = self.sequence[i] + self.sequence[i + 1]
                return str(result)
                
            except ValueError:
                return error_invalid_index

        elif has_triple:
            if self.triple_query_count >= 1:
                return error_triple_limit
            
            try:
                i = int(parsed_info["query_triple"].strip())
                
                if i < 1 or i > n - 2:
                    return error_out_of_range
                
                self.query_count += 1
                self.triple_query_count += 1
                
                result = self.sequence[i] + self.sequence[i + 1] + self.sequence[i + 2]
                return str(result)
                
            except ValueError:
                return error_invalid_index

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            correct_val = int(correct)
            wrong_val = correct_val + 1
            return str(wrong_val)
        except (ValueError, TypeError):
            return correct + " (error)"

    def get_all_possible_queries(self) -> list[dict]:
        n = self._game_info["n"]
        results = []

        for i in range(1, n):
            val = self.sequence[i] + self.sequence[i + 1]
            results.append({
                "query": f"<query_pair>{i}</query_pair>",
                "answer": str(val)
            })

        for i in range(1, n - 1):
            val = self.sequence[i] + self.sequence[i + 1] + self.sequence[i + 2]
            results.append({
                "query": f"<query_triple>{i}</query_triple>",
                "answer": str(val)
            })

        return results

