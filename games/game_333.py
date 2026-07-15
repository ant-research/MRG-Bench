from .base import Game
import random

class SequenceSwapGame(Game):

    game_rule_zh = """\
我们现在来玩一个"序列互换推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的序列。理想状态下，该序列应为严格递增的标号序列 [1, 2, 3, ..., {n}]。

但实际序列是由理想序列进行恰好一次位置互换得到的：存在唯一一对位置 (p, q)，其中 p 小于 q，使得位置 p 和位置 q 上的元素被互换了，而其他位置上的元素保持不变。

定义"相邻违例"：如果序列中某个位置 i 的值大于等于其下一个位置 i+1 的值，则称位置 i 处存在一个相邻违例。相邻违例数量是指这样的位置总数。

你的目标是通过提问推断出被互换的位置对 (p, q)。你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 恢复查询：询问"如果将位置 i 与位置 j 的元素互换，得到的新序列是否严格递增？" 回答"是"或"否"。
2. 违例查询：询问"如果将位置 i 与位置 j 的元素互换，交换后的相邻违例数量是多少？" 回答一个非负整数。
3. 当前违例查询：询问"当前序列的相邻违例数量是多少？" 回答一个非负整数。

注意：所有的"假设交换"仅用于回答问题，不会改变实际序列。实际序列在整个游戏过程中保持不变。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 恢复查询（例如询问位置 2 和位置 5）：
<query_restore>2,5</query_restore>

- 违例查询（例如询问位置 1 和位置 3）：
<query_violation>1,3</query_violation>

- 当前违例查询（内容为空）：
<query_current></query_current>

提交最终答案时，必须给出被互换的两个位置（用逗号隔开，顺序不限），格式如下：

<answer>3,7</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Swap Deduction" game. Here are the rules:

The game has a sequence of length {n}. Ideally, this sequence should be a strictly increasing sequence [1, 2, 3, ..., {n}].

However, the actual sequence is obtained by performing exactly one position swap on the ideal sequence: there exists a unique pair of positions (p, q), where p is less than q, such that the elements at positions p and q are swapped, while elements at all other positions remain unchanged.

Define "adjacent violation": if the value at position i in the sequence is greater than or equal to the value at position i+1, then position i has an adjacent violation. The number of adjacent violations is the total count of such positions.

Your goal is to infer the swapped position pair (p, q) through queries. You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the actual setup:

1. Restore Query: Ask "If we swap the elements at positions i and j, will the resulting sequence be strictly increasing?" Answer "Yes" or "No".
2. Violation Query: Ask "If we swap the elements at positions i and j, how many adjacent violations will the resulting sequence have?" Answer a non-negative integer.
3. Current Violation Query: Ask "How many adjacent violations does the current sequence have?" Answer a non-negative integer.

Note: All "hypothetical swaps" are only used for answering questions and do not change the actual sequence. The actual sequence remains unchanged throughout the game.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Restore Query (e.g., asking about positions 2 and 5):
<query_restore>2,5</query_restore>

- Violation Query (e.g., asking about positions 1 and 3):
<query_violation>1,3</query_violation>

- Current Violation Query (empty content):
<query_current></query_current>

When submitting the final answer, provide the two swapped positions (comma-separated, order does not matter), using this format:

<answer>3,7</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来操作"智能列车调度诊断系统"。

当前调度时间表共有 {n} 个连续的始发时间槽。在理想状态下，列车应按其编号严格以 [1, 2, 3, ..., {n}] 的顺序依次发车。

但系统警报显示，由于调度台指令出错，实际发车序列中恰好有唯一一对时间槽 (p, q)（其中 p 小于 q）上的列车被互换了，而其他时间槽的列车保持原位。

系统定义了"发车冲突"：如果时间槽 i 的列车编号大于或等于紧接着的时间槽 i+1 的列车编号，则认为时间槽 i 处存在一个发车冲突。发车冲突数量即为这种时间槽的总数。

你的目标是通过在虚拟沙盒中进行假设测试，找出被互换的时间槽对 (p, q)。你可以反复提出以下三类诊断查询（每次仅限一个），系统会根据真实设定如实返回测试结果：

1. 恢复查询：询问"如果在沙盒中将时间槽 i 与时间槽 j 的列车互换，发车序列是否恢复严格的先后顺序？" 诊断系统将回答"是"或"否"。
2. 违例查询：询问"如果在沙盒中将时间槽 i 与时间槽 j 的列车互换，沙盒序列中的发车冲突数量是多少？" 诊断系统将回答一个非负整数。
3. 当前违例查询：询问"当前实际调度序列的发车冲突数量是多少？" 诊断系统将回答一个非负整数。

注意：所有的"沙盒互换"仅用于诊断分析，不会改变实际的调度序列。实际序列在整个排查过程中保持不变。

当你收集到足够的数据后，请提交故障报告。若排查错误或格式不符，诊断任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 恢复查询（例如测试时间槽 2 和 5）：
<query_restore>2,5</query_restore>

- 违例查询（例如测试时间槽 1 和 3）：
<query_violation>1,3</query_violation>

- 当前违例查询（内容为空）：
<query_current></query_current>

提交最终故障报告时，必须给出被互换的两个时间槽（用逗号隔开，顺序不限），格式如下：

<answer>3,7</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's operate the "Intelligent Train Dispatch Diagnostic System".

The current dispatch schedule has {n} consecutive departure time slots. Under ideal conditions, trains should depart strictly in the order of their ID numbers: [1, 2, 3, ..., {n}].

However, system alerts indicate that due to a command error, exactly one pair of time slots (p, q) (where p is less than q) has had their trains swapped in the actual departure sequence. Trains in all other time slots remain in their original positions.

The system defines a "Departure Conflict": if the train ID in time slot i is greater than or equal to the train ID in the subsequent time slot i+1, then a departure conflict exists at time slot i. The number of departure conflicts is the total count of such time slots.

Your goal is to identify the swapped time slot pair (p, q) by performing hypothetical tests in a virtual sandbox. You can repeatedly make three types of diagnostic queries (one per turn), and the system will answer truthfully based on the actual schedule:

1. Restore Query: Ask "If we swap the trains at time slots i and j in the sandbox, will the departure sequence be restored to strictly increasing order?" The diagnostic system will answer "Yes" or "No".
2. Violation Query: Ask "If we swap the trains at time slots i and j in the sandbox, how many departure conflicts will the resulting sequence have?" The diagnostic system will answer a non-negative integer.
3. Current Violation Query: Ask "How many departure conflicts does the current actual schedule have?" The diagnostic system will answer a non-negative integer.

Note: All "sandbox swaps" are for diagnostic purposes only and do not alter the actual departure schedule. The actual sequence remains unchanged throughout the troubleshooting process.

When you have gathered enough data, please submit your fault report. If the diagnosis is incorrect or the format is invalid, the mission fails.

Each query must contain only one tag. Use the following XML format:

- Restore Query (e.g., testing time slots 2 and 5):
<query_restore>2,5</query_restore>

- Violation Query (e.g., testing time slots 1 and 3):
<query_violation>1,3</query_violation>

- Current Violation Query (empty content):
<query_current></query_current>

When submitting the final fault report, provide the two swapped time slots (comma-separated, order does not matter), using this format:

<answer>3,7</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来操作"临床路径追踪与纠错系统"。

当前的标准化治疗方案包含 {n} 个连续的临床步骤位置。在理想状态下，这些操作应当严格按照阶段编号 [1, 2, 3, ..., {n}] 的递增顺序执行。

但核查预警显示，由于电子病历系统的录入差错，目前的治疗方案中存在唯一一对步骤位置 (p, q)（其中 p 小于 q）上的操作被互换了，而其余位置的操作仍保持原样。

系统定义了"程序逆转风险"：如果步骤位置 i 的阶段编号大于或等于紧接着的步骤位置 i+1 的阶段编号，则认为位置 i 处存在一处程序逆转风险。风险数量即为出现此种异常的位置总数。

你的目标是通过向推演引擎提问，查出被互换的步骤位置对 (p, q)。你可以反复进行以下三类推演查询（每次仅限一个问题），引擎会基于真实设定的方案如实反馈：

1. 恢复查询：询问"如果在推演中将位置 i 与位置 j 的操作互换，整个治疗方案是否能恢复严格的阶段递增顺序？" 引擎将回答"是"或"否"。
2. 违例查询：询问"如果在推演中将位置 i 与位置 j 的操作互换，新方案会包含多少处程序逆转风险？" 引擎将回答一个非负整数。
3. 当前违例查询：询问"当前实际治疗方案中存在多少处程序逆转风险？" 引擎将回答一个非负整数。

注意：所有的"推演互换"仅仅是在计算机中进行的模拟测试，不会改变患者实际的电子病历方案。实际方案在整个排查过程中始终不变。

当你掌握了确凿的证据后，请提交最终的修正报告。若报告错误或格式不符，纠错任务将判定为失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 恢复查询（例如推演位置 2 和 5）：
<query_restore>2,5</query_restore>

- 违例查询（例如推演位置 1 和 3）：
<query_violation>1,3</query_violation>

- 当前违例查询（内容为空）：
<query_current></query_current>

提交最终修正报告时，必须给出被互换的两个步骤位置（用逗号隔开，顺序不限），格式如下：

<answer>3,7</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's operate the "Clinical Pathway Tracking and Correction System".

The current standardized treatment plan consists of {n} consecutive clinical step positions. Ideally, these operations should be executed strictly in the increasing order of their phase numbers: [1, 2, 3, ..., {n}].

However, a verification alert indicates that due to an electronic medical record entry error, exactly one pair of step positions (p, q) (where p is less than q) has had their operations swapped in the current plan, while all other positions remain unchanged.

The system defines a "Procedure Reversal Risk": if the phase number at position i is greater than or equal to the phase number at the subsequent position i+1, a procedure reversal risk is identified at position i. The total number of risks is the count of such positions.

Your goal is to determine the swapped position pair (p, q) by querying the simulation engine. You can repeatedly make three types of simulation queries (one per turn), and the engine will provide truthful feedback based on the actual plan:

1. Restore Query: Ask "If we simulate swapping the operations at positions i and j, will the treatment plan be restored to a strictly increasing phase order?" The engine will answer "Yes" or "No".
2. Violation Query: Ask "If we simulate swapping the operations at positions i and j, how many procedure reversal risks will the resulting plan contain?" The engine will answer a non-negative integer.
3. Current Violation Query: Ask "How many procedure reversal risks exist in the current actual treatment plan?" The engine will answer a non-negative integer.

Note: All "simulation swaps" are purely computerized tests and do not alter the patient's actual medical record. The actual plan remains unchanged throughout the troubleshooting process.

Once you have conclusive evidence, please submit the final correction report. If the report is incorrect or improperly formatted, the correction task fails.

Each query must contain only one tag. Use the following XML format:

- Restore Query (e.g., simulating positions 2 and 5):
<query_restore>2,5</query_restore>

- Violation Query (e.g., simulating positions 1 and 3):
<query_violation>1,3</query_violation>

- Current Violation Query (empty content):
<query_current></query_current>

When submitting the final correction report, provide the two swapped step positions (comma-separated, order does not matter), using this format:

<answer>3,7</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来操作"教学大纲知识图谱诊断工具"。

当前课程体系预设了 {n} 个教学模块。在理想的认知规律下，这些模块应当按照难度层级 [1, 2, 3, ..., {n}] 严格递增排列。

但教务处的审查发现，在最近一次大纲修订中出现了排版失误，导致目前大纲中恰好有一对模块位置 (p, q)（其中 p 小于 q）的内容被互换了，而其他模块的顺序完好无损。

工具定义了"认知跳跃断层"：如果大纲中位置 i 的模块难度层级大于或等于紧接着的位置 i+1 的难度层级，则说明位置 i 处存在一个认知跳跃断层。断层数量即为符合该条件的位置总数。

你的目标是通过分析平台的沙盒推演，找出大纲中被互换的模块位置对 (p, q)。你可以反复向系统提出以下三类分析查询（每次仅限一个问题），系统会依据大纲的真实设定如实回复：

1. 恢复查询：询问"如果在沙盒中将位置 i 与位置 j 的教学模块互换，大纲是否能恢复严格的难度递增顺序？" 系统将回答"是"或"否"。
2. 违例查询：询问"如果在沙盒中将位置 i 与位置 j 的教学模块互换，大纲中会存在多少处认知跳跃断层？" 系统将回答一个非负整数。
3. 当前违例查询：询问"当前实际教学大纲中存在多少处认知跳跃断层？" 系统将回答一个非负整数。

注意：所有的"沙盒互换"仅是用于诊断的理论计算，不会影响正在使用的实际教学大纲。实际大纲在整个排查期间保持不变。

当你确认了失误的根源后，请提交修订建议。若位置判断错误或格式不符，诊断任务将判定为失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 恢复查询（例如测试位置 2 和 5）：
<query_restore>2,5</query_restore>

- 违例查询（例如测试位置 1 和 3）：
<query_violation>1,3</query_violation>

- 当前违例查询（内容为空）：
<query_current></query_current>

提交最终修订建议时，必须给出被互换的两个模块位置（用逗号隔开，顺序不限），格式如下：

<answer>3,7</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's operate the "Syllabus Knowledge Graph Diagnostic Tool".

The current curriculum structure designates {n} teaching modules. Following ideal cognitive learning paths, these modules should be arranged in strictly increasing order of difficulty levels: [1, 2, 3, ..., {n}].

However, an academic review revealed a formatting error during the recent syllabus revision, causing exactly one pair of module positions (p, q) (where p is less than q) to have their contents swapped. All other modules remain in their correct order.

The tool defines a "Cognitive Leap Fault": if the difficulty level of the module at position i is greater than or equal to that of the subsequent position i+1, a cognitive leap fault exists at position i. The number of faults is the total count of such positions.

Your goal is to identify the swapped module position pair (p, q) through sandbox deductions on the analysis platform. You can repeatedly submit three types of analytical queries (one per turn), and the system will reply truthfully based on the actual syllabus setup:

1. Restore Query: Ask "If we swap the teaching modules at positions i and j in the sandbox, will the syllabus be restored to strictly increasing difficulty order?" The system will answer "Yes" or "No".
2. Violation Query: Ask "If we swap the teaching modules at positions i and j in the sandbox, how many cognitive leap faults will exist in the syllabus?" The system will answer a non-negative integer.
3. Current Violation Query: Ask "How many cognitive leap faults exist in the current actual syllabus?" The system will answer a non-negative integer.

Note: All "sandbox swaps" are theoretical calculations used solely for diagnosis and will not affect the actual syllabus in use. The actual syllabus remains unchanged throughout the investigation.

Once you have pinpointed the root cause of the error, please submit your revision proposal. If the identified positions are incorrect or the format is invalid, the diagnostic task fails.

Each query must contain only one tag. Use the following XML format:

- Restore Query (e.g., testing positions 2 and 5):
<query_restore>2,5</query_restore>

- Violation Query (e.g., testing positions 1 and 3):
<query_violation>1,3</query_violation>

- Current Violation Query (empty content):
<query_current></query_current>

When submitting the final revision proposal, provide the two swapped module positions (comma-separated, order does not matter), using this format:

<answer>3,7</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来操作"自动化流水线装配校验系统"。

当前的装配产线由 {n} 个连续的工位组成。在工艺的理想状态下，各工位上分配的零件应按照装配优先级 [1, 2, 3, ..., {n}] 严格递增的顺序进行组装。

但控制台报错显示，由于机械臂寻址系统出现罕见故障，导致流水线上恰好有一对工位 (p, q)（其中 p 小于 q）的零件被互相调换了，而其他工位的零件分配依然正确。

系统将此定义为"工序倒置缺陷"：如果工位 i 的零件优先级大于或等于其后置工位 i+1 的零件优先级，则判定工位 i 处出现了一次工序倒置缺陷。此类缺陷的总数量即为流水线的异常节点数。

你的目标是通过向虚拟测试环境发送查询指令，锁定被互换的工位对 (p, q)。你可以反复进行以下三类测试查询（每次仅限下发一条指令），测试环境将基于真实的物理分配状态予以精确反馈：

1. 恢复查询：询问"如果在测试环境中将工位 i 与工位 j 的零件互换，整条流水线是否能恢复严格的优先级递增顺序？" 系统将回答"是"或"否"。
2. 违例查询：询问"如果在测试环境中将工位 i 与工位 j 的零件互换，流水线上会出现多少个工序倒置缺陷？" 系统将回答一个非负整数。
3. 当前违例查询：询问"当前实际的装配流水线上有多少个工序倒置缺陷？" 系统将回答一个非负整数。

注意：所有的"测试互换"均是基于数字孪生技术的模拟推演，不会驱动真实的机械臂去改变流水线现况。实际的工序在整个校验排查阶段保持冻结状态。

当完成故障隔离并确信查明问题后，请提交维修坐标指令。若坐标错误或指令格式不符，校验任务判定失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 恢复查询（例如测试工位 2 和 5）：
<query_restore>2,5</query_restore>

- 违例查询（例如测试工位 1 和 3）：
<query_violation>1,3</query_violation>

- 当前违例查询（内容为空）：
<query_current></query_current>

提交最终维修坐标指令时，必须给出被互换的两个工位（用逗号隔开，顺序不限），格式如下：

<answer>3,7</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's operate the "Automated Assembly Line Validation System".

The current assembly line consists of {n} consecutive workstations. Under ideal manufacturing processes, the parts assigned to each workstation should be assembled in a strictly increasing order of their assembly priorities: [1, 2, 3, ..., {n}].

However, the console reports an error indicating that due to a rare fault in the robotic arm addressing system, exactly one pair of workstations (p, q) (where p is less than q) has had their assigned parts swapped on the assembly line, while the parts at all other workstations remain correctly allocated.

The system defines this as a "Sequence Inversion Defect": if the part priority at workstation i is greater than or equal to the part priority at the subsequent workstation i+1, a sequence inversion defect is recorded at workstation i. The total count of such defects represents the number of abnormal nodes on the line.

Your goal is to pinpoint the swapped workstation pair (p, q) by sending query commands to the virtual testing environment. You can repeatedly issue three types of test queries (one per turn), and the environment will provide precise feedback based on the actual physical allocations:

1. Restore Query: Ask "If we swap the parts at workstations i and j in the test environment, will the entire assembly line be restored to a strictly increasing priority order?" The system will answer "Yes" or "No".
2. Violation Query: Ask "If we swap the parts at workstations i and j in the test environment, how many sequence inversion defects will appear on the assembly line?" The system will answer a non-negative integer.
3. Current Violation Query: Ask "How many sequence inversion defects are there on the current actual assembly line?" The system will answer a non-negative integer.

Note: All "test swaps" are simulated deductions using digital twin technology and will not drive actual robotic arms to alter the assembly line. The actual physical sequence remains frozen throughout the validation and troubleshooting phase.

Once fault isolation is complete and you are confident in your findings, please submit the maintenance coordinate command. If the coordinates are incorrect or the command format is invalid, the validation task fails.

Each query must contain only one tag. Use the following XML format:

- Restore Query (e.g., testing workstations 2 and 5):
<query_restore>2,5</query_restore>

- Violation Query (e.g., testing workstations 1 and 3):
<query_violation>1,3</query_violation>

- Current Violation Query (empty content):
<query_current></query_current>

When submitting the final maintenance coordinate command, provide the two swapped workstations (comma-separated, order does not matter), using this format:

<answer>3,7</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来操作"案件证据链逻辑审查系统"。

当前案卷中汇总了 {n} 个关键证据节点。在理想状态下，为了保证司法程序的严密性，这些证据必须严格按照事件发生的时间编号 [1, 2, 3, ..., {n}] 递增排列。

但质证环节指出，由于书记员整理案卷时的疏漏，目前案卷中恰好有一对节点位置 (p, q)（其中 p 小于 q）的证据被互换了，而案卷中其他位置的证据编排均无误。

系统定义了"逻辑时序矛盾"：如果证据链中位置 i 处的证据时间编号大于或等于紧接其后的位置 i+1 处的证据时间编号，则认定位置 i 处存在一处逻辑时序矛盾。矛盾总数即为出现此时序倒置的位置数量。

你的目标是通过向审查中台进行逻辑推演，查明被错误互换的证据节点位置对 (p, q)。你可以反复提交以下三类推演请求（每次仅限一个请求），系统会根据案卷的真实状态给出客观回答：

1. 恢复查询：询问"如果在逻辑推演中将位置 i 与位置 j 的证据互换，整本案卷是否能恢复严格的时间递增顺序？" 系统将回答"是"或"否"。
2. 违例查询：询问"如果在逻辑推演中将位置 i 与位置 j 的证据互换，案卷中会产生多少处逻辑时序矛盾？" 系统将回答一个非负整数。
3. 当前违例查询：询问"当前实际案卷中存在多少处逻辑时序矛盾？" 系统将回答一个非负整数。

注意：所有的"推演互换"只在审查中台的内存中进行沙盘演练，绝不会篡改或破坏实体案卷中的实际证据顺序。真实案卷在整个质证期间保持封存状态不变。

当你搜集到充分的证明材料后，请提交证据修正动议。若位置判定错误或动议格式不符，审查任务将被驳回。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 恢复查询（例如推演位置 2 和 5）：
<query_restore>2,5</query_restore>

- 违例查询（例如推演位置 1 和 3）：
<query_violation>1,3</query_violation>

- 当前违例查询（内容为空）：
<query_current></query_current>

提交最终证据修正动议时，必须给出被互换的两个节点位置（用逗号隔开，顺序不限），格式如下：

<answer>3,7</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's operate the "Case Evidence Chain Logic Review System".

The current case file compiles {n} key evidence nodes. Under ideal circumstances, to ensure the rigor of judicial procedures, these pieces of evidence must be arranged strictly in the increasing order of their chronological occurrence numbers: [1, 2, 3, ..., {n}].

However, cross-examination revealed an oversight by the clerk during the compilation of the file, resulting in exactly one pair of node positions (p, q) (where p is less than q) having their evidence swapped in the current file. The arrangement of evidence at all other positions remains correct.

The system defines a "Logical Chronological Contradiction": if the evidence chronological number at position i is greater than or equal to the evidence chronological number at the immediately following position i+1, a logical chronological contradiction is identified at position i. The total number of contradictions is the count of positions exhibiting such temporal inversion.

Your goal is to ascertain the erroneously swapped evidence node position pair (p, q) by submitting logical deductions to the review platform. You can repeatedly submit three types of deduction requests (one per turn), and the system will provide objective answers based on the actual state of the case file:

1. Restore Query: Ask "If we swap the evidence at positions i and j in a logical deduction, will the entire case file be restored to strictly increasing chronological order?" The system will answer "Yes" or "No".
2. Violation Query: Ask "If we swap the evidence at positions i and j in a logical deduction, how many logical chronological contradictions will be produced in the case file?" The system will answer a non-negative integer.
3. Current Violation Query: Ask "How many logical chronological contradictions exist in the current actual case file?" The system will answer a non-negative integer.

Note: All "deduction swaps" are conducted purely as tabletop exercises within the review platform's memory and will absolutely not tamper with or destroy the actual sequence of evidence in the physical case file. The true case file remains sealed and unchanged throughout the cross-examination period.

Once you have gathered sufficient corroborating material, please submit the evidence correction motion. If the position determination is incorrect or the motion format is invalid, the review task will be dismissed.

Each query must contain only one tag. Use the following XML format:

- Restore Query (e.g., deducting positions 2 and 5):
<query_restore>2,5</query_restore>

- Violation Query (e.g., deducting positions 1 and 3):
<query_violation>1,3</query_violation>

- Current Violation Query (empty content):
<query_current></query_current>

When submitting the final evidence correction motion, provide the two swapped node positions (comma-separated, order does not matter), using this format:

<answer>3,7</answer>
"""

    tags = ["answer", "query_restore", "query_violation", "query_current"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 5, "p": 2, "q": 3},
            2: {"n": 8, "p": 3, "q": 5},
            3: {"n": 10, "p": 2, "q": 6},
            4: {"n": 12, "p": 3, "q": 9},
            5: {"n": 15, "p": 4, "q": 12},
        },
        "en": {
            1: {"n": 5, "p": 2, "q": 3},
            2: {"n": 8, "p": 3, "q": 5},
            3: {"n": 10, "p": 2, "q": 6},
            4: {"n": 12, "p": 3, "q": 9},
            5: {"n": 15, "p": 4, "q": 12},
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
        n = cfg["n"]
        self.p = cfg["p"]
        self.q = cfg["q"]
        
        self._game_info["n"] = n

        self.sequence = list(range(1, n + 1))
        self.sequence[self.p - 1], self.sequence[self.q - 1] = self.sequence[self.q - 1], self.sequence[self.p - 1]

    def _count_violations(self, seq):
        count = 0
        for i in range(len(seq) - 1):
            if seq[i] >= seq[i + 1]:
                count += 1
        return count

    def _is_strictly_increasing(self, seq):
        for i in range(len(seq) - 1):
            if seq[i] >= seq[i + 1]:
                return False
        return True

    def _swap_and_check(self, i, j):
        temp_seq = self.sequence.copy()
        temp_seq[i - 1], temp_seq[j - 1] = temp_seq[j - 1], temp_seq[i - 1]
        
        is_increasing = self._is_strictly_increasing(temp_seq)
        violation_count = self._count_violations(temp_seq)
        
        return is_increasing, violation_count

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            if len(parts) != 2:
                return False
            
            pos1, pos2 = int(parts[0]), int(parts[1])
            
            submitted_pair = tuple(sorted([pos1, pos2]))
            correct_pair = tuple(sorted([self.p, self.q]))
            
            return submitted_pair == correct_pair
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或位置超出范围。"
            error_range = "错误：位置必须在 1 到 {n} 之间，且两个位置不能相同。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or positions out of range."
            error_range = "Error: Positions must be between 1 and {n}, and must not be equal."

        if "query_restore" in parsed_info:
            try:
                raw = parsed_info["query_restore"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                i, j = int(parts[0]), int(parts[1])
                
                if i == j or i < 1 or j < 1 or i > self._game_info["n"] or j > self._game_info["n"]:
                    return error_range.format(n=self._game_info["n"])
                if i > j:
                    i, j = j, i
                
                is_increasing, _ = self._swap_and_check(i, j)
                return yes_res if is_increasing else no_res
                
            except Exception:
                return error_format

        elif "query_violation" in parsed_info:
            try:
                raw = parsed_info["query_violation"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                
                i, j = int(parts[0]), int(parts[1])
                
                if i == j or i < 1 or j < 1 or i > self._game_info["n"] or j > self._game_info["n"]:
                    return error_range.format(n=self._game_info["n"])
                if i > j:
                    i, j = j, i
                
                _, violation_count = self._swap_and_check(i, j)
                return str(violation_count)
                
            except Exception:
                return error_format

        elif "query_current" in parsed_info:
            current_violations = self._count_violations(self.sequence)
            return str(current_violations)

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        low_correct = correct.lower()
        if low_correct == "yes":
            if correct.isupper(): return "NO"
            if correct.islower(): return "no"
            return "No"
        if low_correct == "no":
            if correct.isupper(): return "YES"
            if correct.islower(): return "yes"
            return "Yes"

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        lang = self.config.language
        
        if lang == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                query_restore = f"<query_restore>{i},{j}</query_restore>"
                is_increasing, _ = self._swap_and_check(i, j)
                ans_restore = yes_res if is_increasing else no_res
                queries.append({
                    "query": query_restore,
                    "answer": ans_restore
                })

                query_violation = f"<query_violation>{i},{j}</query_violation>"
                _, violation_count = self._swap_and_check(i, j)
                ans_violation = str(violation_count)
                queries.append({
                    "query": query_violation,
                    "answer": ans_violation
                })
        
        query_current = "<query_current></query_current>"
        current_violations = self._count_violations(self.sequence)
        ans_current = str(current_violations)
        queries.append({
            "query": query_current,
            "answer": ans_current
        })
        
        return queries