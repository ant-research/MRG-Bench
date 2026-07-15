from .base import Game
import random

class SequencePositionMappingGame(Game):

    game_rule_zh = """\
我们来玩一个"序列位置映射识别"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的未知有序序列 S，序列中的元素均为大写字母。序列的索引从 1 到 {n}。

系统已秘密选择了一个目标符号 τ = {target}，它保证在序列中至少出现一次。同时，系统从以下四种映射模式中秘密选择了一种作为隐藏规则：

1. LF 模式：对任意符号 x，返回 x 在序列中首次出现的位置
2. LL 模式：对任意符号 x，返回 x 在序列中最后出现的位置
3. RF 模式：对任意符号 x，返回从右往左数，x 最后出现位置到右端的距离加 1
4. RL 模式：对任意符号 x，返回从右往左数，x 首次出现位置到右端的距离加 1

注意：当符号 x 不在序列中时，映射值定义为 0。

你的目标是通过尽可能少的询问，识别出隐藏的映射模式，并计算出目标符号 τ 在该模式下的数值。

你可以进行以下两种类型的询问（每次仅限一个操作）：

1. 检查位置：查看序列中某个位置的符号是什么
   格式：<inspect>位置编号</inspect>
   示例：<inspect>3</inspect>
   返回：Symbol=X（其中 X 是该位置的大写字母）

2. 查询符号：查询某个符号在当前隐藏模式下的映射值
   格式：<query>符号</query>
   示例：<query>A</query>
   返回：
   - 如果查询的是目标符号 τ：Silence（系统保持沉默，不返回数值）
   - 如果符号不在序列中：0
   - 否则：Echo=数值（一个 1 到 {n} 之间的整数）

当你准备好提交答案时，必须同时声明映射模式和目标符号的数值，格式如下：

<answer>Mode=模式, Value=数值</answer>

其中模式必须是 LF、LL、RF、RL 之一，数值必须是 1 到 {n} 之间的整数。

示例：<answer>Mode=LF, Value=5</answer>

若模式或数值任一错误，游戏失败。
"""

    game_rule_en = """\
Let's play a "Sequence Position Mapping Recognition" deduction game. Here are the rules:

The game has an unknown ordered sequence S of length {n}, where all elements are uppercase letters. The sequence is indexed from 1 to {n}.

The system has secretly selected a target symbol τ = {target}, which is guaranteed to appear at least once in the sequence. Additionally, the system has secretly chosen one of the following four mapping modes as the hidden rule:

1. LF Mode: For any symbol x, return the position of its first occurrence in the sequence
2. LL Mode: For any symbol x, return the position of its last occurrence in the sequence
3. RF Mode: For any symbol x, return the distance from its last occurrence to the right end plus 1 (counting from right)
4. RL Mode: For any symbol x, return the distance from its first occurrence to the right end plus 1 (counting from right)

Note: When symbol x does not exist in the sequence, the mapping value is defined as 0.

Your goal is to identify the hidden mapping mode and calculate the value of the target symbol τ under that mode, using as few queries as possible.

You can perform the following two types of queries (one operation per turn):

1. Inspect Position: Check what symbol is at a certain position in the sequence
   Format: <inspect>position_number</inspect>
   Example: <inspect>3</inspect>
   Returns: Symbol=X (where X is the uppercase letter at that position)

2. Query Symbol: Query the mapping value of a symbol under the current hidden mode
   Format: <query>symbol</query>
   Example: <query>A</query>
   Returns:
   - If querying the target symbol τ: Silence (system remains silent, no value returned)
   - If symbol not in sequence: 0
   - Otherwise: Echo=value (an integer between 1 and {n})

When you are ready to submit your answer, you must declare both the mapping mode and the target symbol's value in the following format:

<answer>Mode=mode, Value=value</answer>

The mode must be one of LF, LL, RF, RL, and the value must be an integer between 1 and {n}.

Example: <answer>Mode=LF, Value=5</answer>

If either the mode or value is incorrect, the game fails.
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通信号排班分析系统。本系统用于分析复杂的车流序列并提取特定目标车辆的通行模式特征。

系统捕获了一段长度为 {n} 的未知时序路口通行记录序列 S，序列中的元素均为代表不同车辆类型或方向的大写字母。时间节点编号从 1 到 {n}。

系统已秘密锁定了一类重点监测的车辆类型 τ = {target}，它保证在序列中至少出现一次。同时，系统从以下四种评估模式中秘密选择了一种作为隐藏的排班规则：

1. LF 模式：对任意车辆类型 x，返回其在序列中当日首次通行的时间节点
2. LL 模式：对任意车辆类型 x，返回其在序列中当日最后一次通行的时间节点
3. RF 模式：对任意车辆类型 x，返回从右往左数，其最后一次通行节点距晚高峰结束（右端）的倒数节点距离加 1
4. RL 模式：对任意车辆类型 x，返回从右往左数，其首次通行节点距晚高峰结束（右端）的倒数节点距离加 1

注意：当车辆类型 x 未出现时，评估值定义为 0。

你的目标是通过尽可能少的系统询问，识别出隐藏的排班模式，并计算出重点监测车辆类型 τ 在该模式下的数值。

你可以进行以下两种类型的询问（每次仅限一个操作）：

1. 检查节点：查看序列中某个时间节点的车辆类型是什么
   格式：<inspect>节点编号</inspect>
   示例：<inspect>3</inspect>
   返回：Symbol=X（其中 X 是该节点的大写字母代表的车辆类型）

2. 查询特征：查询某个车辆类型在当前隐藏模式下的评估值
   格式：<query>车辆类型</query>
   示例：<query>A</query>
   返回：
   - 如果查询的是重点监测车辆类型 τ：Silence（系统保持沉默，由于权限限制不返回数值）
   - 如果该车辆类型未在序列中出现：0
   - 否则：Echo=数值（一个 1 到 {n} 之间的整数）

当你准备好提交分析结果时，必须同时声明排班模式和目标车辆类型的特征数值，格式如下：

<answer>Mode=模式, Value=数值</answer>

其中模式必须是 LF、LL、RF、RL 之一，数值必须是 1 到 {n} 之间的整数。

示例：<answer>Mode=LF, Value=5</answer>

若模式或数值任一错误，分析任务失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Signal Scheduling Analysis System. This system is designed to analyze complex traffic flow sequences and extract the passing pattern features of specific target vehicles.

The system has captured an unknown temporal traffic sequence S of length {n}, where all elements are uppercase letters representing different vehicle types or directions. The time nodes are indexed from 1 to {n}.

The system has secretly locked onto a key monitored vehicle type τ = {target}, which is guaranteed to appear at least once in the sequence. Additionally, the system has secretly chosen one of the following four evaluation modes as the hidden scheduling rule:

1. LF Mode: For any vehicle type x, return the time node of its first passing in the sequence today
2. LL Mode: For any vehicle type x, return the time node of its last passing in the sequence today
3. RF Mode: For any vehicle type x, return the distance from its last passing node to the end of the evening peak (right end) plus 1 (counting from right)
4. RL Mode: For any vehicle type x, return the distance from its first passing node to the end of the evening peak (right end) plus 1 (counting from right)

Note: When vehicle type x does not appear in the sequence, the evaluation value is defined as 0.

Your goal is to identify the hidden scheduling mode and calculate the value of the key monitored vehicle type τ under that mode, using as few system queries as possible.

You can perform the following two types of queries (one operation per turn):

1. Inspect Node: Check what vehicle type is at a certain time node in the sequence
   Format: <inspect>node_number</inspect>
   Example: <inspect>3</inspect>
   Returns: Symbol=X (where X is the uppercase letter representing the vehicle type at that node)

2. Query Feature: Query the evaluation value of a vehicle type under the current hidden mode
   Format: <query>vehicle_type</query>
   Example: <query>A</query>
   Returns:
   - If querying the key monitored vehicle type τ: Silence (system remains silent due to permission limits, no value returned)
   - If the vehicle type does not appear in the sequence: 0
   - Otherwise: Echo=value (an integer between 1 and {n})

When you are ready to submit your analysis results, you must declare both the scheduling mode and the target vehicle type's feature value in the following format:

<answer>Mode=mode, Value=value</answer>

The mode must be one of LF, LL, RF, RL, and the value must be an integer between 1 and {n}.

Example: <answer>Mode=LF, Value=5</answer>

If either the mode or value is incorrect, the analysis task fails.
"""

    contextualized_rule_zh_2 = """\
欢迎使用临床用药疗效监测与评估系统。本系统致力于分析患者整个疗程的用药干预序列，并识别核心药物的疗效模式。

系统载入了一段长度为 {n} 的未知患者用药记录周期 S，序列中的元素均为代表不同药物种类的大写字母。疗程的阶段编号从 1 到 {n}。

系统已秘密锁定了一种重点关注的药物种类 τ = {target}，它保证在疗程中至少给药一次。同时，系统从以下四种评估模式中秘密选择了一种作为隐藏的疗效计算规则：

1. LF 模式：对任意药物 x，返回其在疗程中首次给药的阶段编号
2. LL 模式：对任意药物 x，返回其在疗程中最后一次给药的阶段编号
3. RF 模式：对任意药物 x，返回从右往左数，其最后一次给药阶段距疗程结束（右端）的倒数距离加 1
4. RL 模式：对任意药物 x，返回从右往左数，其首次给药阶段距疗程结束（右端）的倒数距离加 1

注意：当药物 x 未在疗程中开出时，评估值定义为 0。

你的目标是通过尽可能少的系统询问，识别出隐藏的疗效评估模式，并计算出重点关注药物 τ 在该模式下的数值。

你可以进行以下两种类型的询问（每次仅限一个操作）：

1. 检查阶段：查看疗程序列中某个阶段的药物种类是什么
   格式：<inspect>阶段编号</inspect>
   示例：<inspect>3</inspect>
   返回：Symbol=X（其中 X 是该阶段的大写字母代表的药物）

2. 查询疗效：查询某个药物在当前隐藏模式下的评估值
   格式：<query>药物种类</query>
   示例：<query>A</query>
   返回：
   - 如果查询的是重点关注药物 τ：Silence（基于双盲原则，系统保持沉默）
   - 如果该药物未在序列中出现：0
   - 否则：Echo=数值（一个 1 到 {n} 之间的整数）

当你准备好提交结论时，必须同时声明疗效评估模式和核心药物的特征数值，格式如下：

<answer>Mode=模式, Value=数值</answer>

其中模式必须是 LF、LL、RF、RL 之一，数值必须是 1 到 {n} 之间的整数。

示例：<answer>Mode=LF, Value=5</answer>

若模式或数值任一错误，则临床评估失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Clinical Medication Efficacy Monitoring and Evaluation System. This system is dedicated to analyzing the medication intervention sequence throughout a patient's course of treatment to identify the efficacy pattern of core drugs.

The system has loaded an unknown patient medication record sequence S of length {n}, where all elements are uppercase letters representing different drug types. The treatment stages are indexed from 1 to {n}.

The system has secretly locked onto a focal drug type τ = {target}, which is guaranteed to be administered at least once during the treatment. Additionally, the system has secretly chosen one of the following four evaluation modes as the hidden efficacy calculation rule:

1. LF Mode: For any drug x, return the stage number of its first administration in the sequence
2. LL Mode: For any drug x, return the stage number of its last administration in the sequence
3. RF Mode: For any drug x, return the distance from its last administration stage to the end of the treatment (right end) plus 1 (counting from right)
4. RL Mode: For any drug x, return the distance from its first administration stage to the end of the treatment (right end) plus 1 (counting from right)

Note: When drug x is not prescribed during the treatment, the evaluation value is defined as 0.

Your goal is to identify the hidden efficacy evaluation mode and calculate the value of the focal drug τ under that mode, using as few system queries as possible.

You can perform the following two types of queries (one operation per turn):

1. Inspect Stage: Check what drug type was administered at a certain stage in the sequence
   Format: <inspect>stage_number</inspect>
   Example: <inspect>3</inspect>
   Returns: Symbol=X (where X is the uppercase letter representing the drug at that stage)

2. Query Efficacy: Query the evaluation value of a drug under the current hidden mode
   Format: <query>drug_type</query>
   Example: <query>A</query>
   Returns:
   - If querying the focal drug τ: Silence (system remains silent based on double-blind principles)
   - If the drug does not appear in the sequence: 0
   - Otherwise: Echo=value (an integer between 1 and {n})

When you are ready to submit your conclusion, you must declare both the efficacy evaluation mode and the focal drug's feature value in the following format:

<answer>Mode=mode, Value=value</answer>

The mode must be one of LF, LL, RF, RL, and the value must be an integer between 1 and {n}.

Example: <answer>Mode=LF, Value=5</answer>

If either the mode or value is incorrect, the clinical evaluation fails.
"""

    contextualized_rule_zh_3 = """\
欢迎登录学生知识点掌握轨迹评测系统。本系统用于分析学生的连续学习评测记录，以洞察知识模块的复习与考查规律。

系统生成了一段长度为 {n} 的未知学习评测序列 S，序列中的元素均为代表不同知识模块的大写字母。测试的轮次编号从 1 到 {n}。

系统已秘密圈定了一个核心考查知识模块 τ = {target}，它保证在整个评测序列中至少出现一次。同时，系统从以下四种评估模式中秘密选择了一种作为隐藏的考查规律：

1. LF 模式：对任意知识模块 x，返回其在序列中首次出现的测试轮次
2. LL 模式：对任意知识模块 x，返回其在序列中最后一次出现的测试轮次
3. RF 模式：对任意知识模块 x，返回从右往左数，其最后一次考查距期末测试（右端）的倒数轮次距离加 1
4. RL 模式：对任意知识模块 x，返回从右往左数，其首次考查距期末测试（右端）的倒数轮次距离加 1

注意：当知识模块 x 未在序列中涉及，评估值定义为 0。

你的目标是通过尽可能少的系统询问，识别出隐藏的考查规律，并计算出核心知识模块 τ 在该规律下的数值。

你可以进行以下两种类型的询问（每次仅限一个操作）：

1. 检查轮次：查看评测序列中某个测试轮次考查的知识模块是什么
   格式：<inspect>轮次编号</inspect>
   示例：<inspect>3</inspect>
   返回：Symbol=X（其中 X 是该轮次考查的大写字母代表的知识模块）

2. 查询规律：查询某个知识模块在当前隐藏规律下的评估值
   格式：<query>知识模块</query>
   示例：<query>A</query>
   返回：
   - 如果查询的是核心知识模块 τ：Silence（为防作弊，系统拒绝返回该核心模块的数据）
   - 如果该模块未在序列中出现：0
   - 否则：Echo=数值（一个 1 到 {n} 之间的整数）

当你准备好提交结果时，必须同时声明考查规律模式和核心模块的评估数值，格式如下：

<answer>Mode=模式, Value=数值</answer>

其中模式必须是 LF、LL、RF、RL 之一，数值必须是 1 到 {n} 之间的整数。

示例：<answer>Mode=LF, Value=5</answer>

若模式或数值任一错误，评测分析失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Student Knowledge Mastery Trajectory Assessment System. This system analyzes students' continuous learning assessment records to gain insights into the review and examination patterns of knowledge modules.

The system has generated an unknown learning assessment sequence S of length {n}, where all elements are uppercase letters representing different knowledge modules. The test rounds are indexed from 1 to {n}.

The system has secretly designated a core examined knowledge module τ = {target}, which is guaranteed to appear at least once in the entire assessment sequence. Additionally, the system has secretly chosen one of the following four evaluation modes as the hidden examination pattern:

1. LF Mode: For any knowledge module x, return the test round of its first appearance in the sequence
2. LL Mode: For any knowledge module x, return the test round of its last appearance in the sequence
3. RF Mode: For any knowledge module x, return the distance from its last examination round to the final test (right end) plus 1 (counting from right)
4. RL Mode: For any knowledge module x, return the distance from its first examination round to the final test (right end) plus 1 (counting from right)

Note: When knowledge module x is not covered in the sequence, the evaluation value is defined as 0.

Your goal is to identify the hidden examination pattern and calculate the value of the core knowledge module τ under that pattern, using as few system queries as possible.

You can perform the following two types of queries (one operation per turn):

1. Inspect Round: Check what knowledge module was examined in a certain test round of the sequence
   Format: <inspect>round_number</inspect>
   Example: <inspect>3</inspect>
   Returns: Symbol=X (where X is the uppercase letter representing the knowledge module examined in that round)

2. Query Pattern: Query the evaluation value of a knowledge module under the current hidden pattern
   Format: <query>knowledge_module</query>
   Example: <query>A</query>
   Returns:
   - If querying the core knowledge module τ: Silence (system refuses to return data for the core module to prevent cheating)
   - If the module does not appear in the sequence: 0
   - Otherwise: Echo=value (an integer between 1 and {n})

When you are ready to submit your result, you must declare both the examination pattern mode and the core module's evaluation value in the following format:

<answer>Mode=mode, Value=value</answer>

The mode must be one of LF, LL, RF, RL, and the value must be an integer between 1 and {n}.

Example: <answer>Mode=LF, Value=5</answer>

If either the mode or value is incorrect, the assessment analysis fails.
"""

    contextualized_rule_zh_4 = """\
欢迎使用流水线质检工序排布追溯系统。本系统用于分析复杂的生产线检验配置，并优化关键产品缺陷的拦截率。

系统获取了一段长度为 {n} 的未知质检站点序列 S，序列中的元素均为代表不同检验项目的大写字母。流水线的工位编号从 1 到 {n}。

系统已秘密标记了一个关键检验项目 τ = {target}, 它保证在整条流水线上至少被配置一次。同时，系统从以下四种追溯模式中秘密选择了一种作为隐藏的质检规则：

1. LF 模式：对任意检验项目 x，返回其在流水线上首次进行检测的工位编号
2. LL 模式：对任意检验项目 x，返回其在流水线上最后一次进行检测的工位编号
3. RF 模式：对任意检验项目 x，返回从右往左数，其最后一次检测距流水线末端（右端）的倒数工位距离加 1
4. RL 模式：对任意检验项目 x，返回从右往左数，其首次检测距流水线末端（右端）的倒数工位距离加 1

注意：当检验项目 x 未在流水线配置中出现时，追溯值定义为 0。

你的目标是通过尽可能少的系统询问，识别出隐藏的质检追溯模式，并计算出关键检验项目 τ 在该模式下的工位数值。

你可以进行以下两种类型的询问（每次仅限一个操作）：

1. 检查工位：查看流水线序列中某个工位的检验项目是什么
   格式：<inspect>工位编号</inspect>
   示例：<inspect>3</inspect>
   返回：Symbol=X（其中 X 是该工位大写字母代表的检验项目）

2. 查询追溯：查询某个检验项目在当前隐藏规则下的追溯值
   格式：<query>检验项目</query>
   示例：<query>A</query>
   返回：
   - 如果查询的是关键检验项目 τ：Silence（传感器故障或数据屏蔽，系统不返回数值）
   - 如果该项目未在序列中出现：0
   - 否则：Echo=数值（一个 1 到 {n} 之间的整数）

当你准备好提交分析报告时，必须同时声明质检规则模式和关键项目的追溯数值，格式如下：

<answer>Mode=模式, Value=数值</answer>

其中模式必须是 LF、LL、RF、RL 之一，数值必须是 1 到 {n} 之间的整数。

示例：<answer>Mode=LF, Value=5</answer>

若模式或数值任一错误，流水线排查任务失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Assembly Line Quality Inspection Process Traceability System. This system is used to analyze complex production line inspection configurations and optimize the interception rate of key product defects.

The system has obtained an unknown quality inspection station sequence S of length {n}, where all elements are uppercase letters representing different inspection items. The workstations on the assembly line are indexed from 1 to {n}.

The system has secretly marked a key inspection item τ = {target}, which is guaranteed to be configured at least once on the entire line. Additionally, the system has secretly chosen one of the following four traceability modes as the hidden quality inspection rule:

1. LF Mode: For any inspection item x, return the workstation number of its first detection on the assembly line
2. LL Mode: For any inspection item x, return the workstation number of its last detection on the assembly line
3. RF Mode: For any inspection item x, return the distance from its last detection station to the end of the assembly line (right end) plus 1 (counting from right)
4. RL Mode: For any inspection item x, return the distance from its first detection station to the end of the assembly line (right end) plus 1 (counting from right)

Note: When inspection item x is not configured on the line, the traceability value is defined as 0.

Your goal is to identify the hidden quality inspection traceability mode and calculate the workstation value of the key inspection item τ under that mode, using as few system queries as possible.

You can perform the following two types of queries (one operation per turn):

1. Inspect Workstation: Check what inspection item is configured at a certain workstation in the sequence
   Format: <inspect>workstation_number</inspect>
   Example: <inspect>3</inspect>
   Returns: Symbol=X (where X is the uppercase letter representing the inspection item at that workstation)

2. Query Traceability: Query the traceability value of an inspection item under the current hidden rule
   Format: <query>inspection_item</query>
   Example: <query>A</query>
   Returns:
   - If querying the key inspection item τ: Silence (sensor failure or data masked, system returns no value)
   - If the item does not appear in the sequence: 0
   - Otherwise: Echo=value (an integer between 1 and {n})

When you are ready to submit your analysis report, you must declare both the inspection rule mode and the key item's traceability value in the following format:

<answer>Mode=mode, Value=value</answer>

The mode must be one of LF, LL, RF, RL, and the value must be an integer between 1 and {n}.

Example: <answer>Mode=LF, Value=5</answer>

If either the mode or value is incorrect, the assembly line troubleshooting task fails.
"""

    contextualized_rule_zh_5 = """\
欢迎进入案件证据链审查评估系统。本系统致力于梳理复杂的庭审时间线证据提交记录，并校验关键证据的法律效力。

系统提取了一段长度为 {n} 的未知时间线证据提交序列 S，序列中的元素均为代表不同证据类别的大写字母。庭审阶段的编号从 1 到 {n}。

系统已秘密指定了一项核心证据类别 τ = {target}，它保证在整个庭审过程中至少被提交一次。同时，系统从以下四种审查模式中秘密选择了一种作为隐藏的效力评估规则：

1. LF 模式：对任意证据类别 x，返回其在时间线上首次提交的庭审阶段编号
2. LL 模式：对任意证据类别 x，返回其在时间线上最后一次提交的庭审阶段编号
3. RF 模式：对任意证据类别 x，返回从右往左数，其最后一次提交距终审结案（右端）的倒数阶段距离加 1
4. RL 模式：对任意证据类别 x，返回从右往左数，其首次提交距终审结案（右端）的倒数阶段距离加 1

注意：当证据类别 x 未被提交时，评估值定义为 0。

你的目标是通过尽可能少的系统询问，识别出隐藏的审查规则模式，并计算出核心证据 τ 在该模式下的效力数值。

你可以进行以下两种类型的询问（每次仅限一个操作）：

1. 检查阶段：查看时间线序列中某个阶段提交的证据类别是什么
   格式：<inspect>阶段编号</inspect>
   示例：<inspect>3</inspect>
   返回：Symbol=X（其中 X 是该阶段的大写字母代表的证据类别）

2. 查询审查：查询某个证据类别在当前隐藏规则下的评估值
   格式：<query>证据类别</query>
   示例：<query>A</query>
   返回：
   - 如果查询的是核心证据类别 τ：Silence（因涉密或法庭隔离，系统拒绝返回数值）
   - 如果该证据未在序列中出现：0
   - 否则：Echo=数值（一个 1 到 {n} 之间的整数）

当你准备好提交审查结论时，必须同时声明审查规则模式和核心证据的效力数值，格式如下：

<answer>Mode=模式, Value=数值</answer>

其中模式必须是 LF、LL、RF、RL 之一，数值必须是 1 到 {n} 之间的整数。

示例：<answer>Mode=LF, Value=5</answer>

若模式或数值任一错误，案件审查失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Case Evidence Chain Review and Evaluation System. This system is dedicated to sorting out complex chronological evidence submission records and verifying the legal validity of key evidence.

The system has extracted an unknown chronological evidence submission sequence S of length {n}, where all elements are uppercase letters representing different evidence categories. The trial stages are indexed from 1 to {n}.

The system has secretly designated a core evidence category τ = {target}, which is guaranteed to be submitted at least once during the trial. Additionally, the system has secretly chosen one of the following four review modes as the hidden validity evaluation rule:

1. LF Mode: For any evidence category x, return the trial stage number of its first submission on the timeline
2. LL Mode: For any evidence category x, return the trial stage number of its last submission on the timeline
3. RF Mode: For any evidence category x, return the distance from its last submission stage to the final judgment (right end) plus 1 (counting from right)
4. RL Mode: For any evidence category x, return the distance from its first submission stage to the final judgment (right end) plus 1 (counting from right)

Note: When evidence category x is not submitted, the evaluation value is defined as 0.

Your goal is to identify the hidden review rule mode and calculate the validity value of the core evidence τ under that mode, using as few system queries as possible.

You can perform the following two types of queries (one operation per turn):

1. Inspect Stage: Check what evidence category was submitted at a certain stage in the timeline sequence
   Format: <inspect>stage_number</inspect>
   Example: <inspect>3</inspect>
   Returns: Symbol=X (where X is the uppercase letter representing the evidence category at that stage)

2. Query Review: Query the evaluation value of an evidence category under the current hidden rule
   Format: <query>evidence_category</query>
   Example: <query>A</query>
   Returns:
   - If querying the core evidence category τ: Silence (due to confidentiality or court isolation, the system refuses to return a value)
   - If the evidence does not appear in the sequence: 0
   - Otherwise: Echo=value (an integer between 1 and {n})

When you are ready to submit your review conclusion, you must declare both the review rule mode and the core evidence's validity value in the following format:

<answer>Mode=mode, Value=value</answer>

The mode must be one of LF, LL, RF, RL, and the value must be an integer between 1 and {n}.

Example: <answer>Mode=LF, Value=5</answer>

If either the mode or value is incorrect, the case review fails.
"""

    tags = ["answer", "inspect", "query"]

    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "sequence": "A,B,C,A,E",
                "target": "C",
                "mode": "LF",
            },
            2: {
                "n": 8,
                "sequence": "A,B,C,A,D,E,F,G",
                "target": "A",
                "mode": "LL",
            },
            3: {
                "n": 10,
                "sequence": "A,B,C,D,B,E,F,B,G,H",
                "target": "B",
                "mode": "RF",
            },
            4: {
                "n": 12,
                "sequence": "A,B,C,D,E,A,F,G,H,A,I,J",
                "target": "A",
                "mode": "RL",
            },
            5: {
                "n": 15,
                "sequence": "A,B,C,D,E,F,B,G,H,I,B,J,K,L,M",
                "target": "B",
                "mode": "LF",
            },
        },
        "en": {
            1: {
                "n": 5,
                "sequence": "A,B,C,A,E",
                "target": "C",
                "mode": "LF",
            },
            2: {
                "n": 8,
                "sequence": "A,B,C,A,D,E,F,G",
                "target": "A",
                "mode": "LL",
            },
            3: {
                "n": 10,
                "sequence": "A,B,C,D,B,E,F,B,G,H",
                "target": "B",
                "mode": "RF",
            },
            4: {
                "n": 12,
                "sequence": "A,B,C,D,E,A,F,G,H,A,I,J",
                "target": "A",
                "mode": "RL",
            },
            5: {
                "n": 15,
                "sequence": "A,B,C,D,E,F,B,G,H,I,B,J,K,L,M",
                "target": "B",
                "mode": "LF",
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
        
        self.sequence = [s.strip() for s in cfg["sequence"].split(",")]
        self.n = cfg["n"]
        self.target = cfg["target"]
        self.mode = cfg["mode"]
        
        self._game_info["n"] = self.n
        self._game_info["target"] = self.target
        
        self.first_pos = {}
        self.last_pos = {}
        
        for i, symbol in enumerate(self.sequence, start=1):
            if symbol not in self.first_pos:
                self.first_pos[symbol] = i
            self.last_pos[symbol] = i
        
        self.correct_value = self._compute_mapping(self.target, self.mode)

    def _compute_mapping(self, symbol, mode):
        if symbol not in self.first_pos:
            return 0
        
        if mode == "LF":
            return self.first_pos[symbol]
        elif mode == "LL":
            return self.last_pos[symbol]
        elif mode == "RF":
            return self.n - self.last_pos[symbol] + 1
        elif mode == "RL":
            return self.n - self.first_pos[symbol] + 1
        else:
            raise ValueError(f"Unknown mode: {mode}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "Mode" not in ans_dict or "Value" not in ans_dict:
            return False
        
        if ans_dict["Mode"] != self.mode:
            return False
        
        try:
            submitted_value = int(ans_dict["Value"])
        except ValueError:
            return False
        
        return submitted_value == self.correct_value

    def _cf_core_produce(self, parsed_info):
        
        if "inspect" in parsed_info:
            try:
                pos = int(parsed_info["inspect"].strip())
                if pos < 1 or pos > self.n:
                    if self.config.language == "zh":
                        return "错误：位置超出范围。"
                    else:
                        return "Error: Position out of range."
                
                symbol = self.sequence[pos - 1]
                return f"Symbol={symbol}"
            except ValueError:
                if self.config.language == "zh":
                    return "错误：无效的位置格式。"
                else:
                    return "Error: Invalid position format."
        
        elif "query" in parsed_info:
            symbol = parsed_info["query"].strip()
            
            if len(symbol) != 1 or not symbol.isupper():
                if self.config.language == "zh":
                    return "错误：符号必须是单个大写字母。"
                else:
                    return "Error: Symbol must be a single uppercase letter."
            
            if symbol == self.target:
                return "Silence"
            
            value = self._compute_mapping(symbol, self.mode)
            
            if value == 0:
                return "0"
            else:
                return f"Echo={value}"
        
        else:
            raise ValueError("No valid query tag found.")
    
    def get_all_possible_queries(self) -> list[dict]:
        import string
        results = []

        for i in range(1, self.n + 1):
            query_content = str(i)
            parsed_info = {"inspect": query_content}
            answer = self._cf_core_produce(parsed_info)
            results.append({
                "query": f"<inspect>{query_content}</inspect>",
                "answer": answer
            })

        for char in string.ascii_uppercase:
            parsed_info = {"query": char}
            answer = self._cf_core_produce(parsed_info)
            results.append({
                "query": f"<query>{char}</query>",
                "answer": answer
            })

        return results

    def _cf_make_wrong(self, correct):
        import re
        
        m = re.match(r'^Symbol=([A-Z])$', correct)
        if m:
            original = m.group(1)
            for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                if c != original:
                    return f"Symbol={c}"
        
        m = re.match(r'^Echo=(\d+)$', correct)
        if m:
            val = int(m.group(1))
            wrong_val = val + 1 if val < self.n else val - 1
            return f"Echo={wrong_val}"
        
        if correct == "0":
            return "Echo=1"
        
        if correct == "Silence":
            return "Echo=1"
        
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                if "Yes" in correct: return correct.replace("Yes", "No")
                if "YES" in correct: return correct.replace("YES", "NO")
                if "yes" in correct: return correct.replace("yes", "no")
            if "no" in lower_correct:
                if "No" in correct: return correct.replace("No", "Yes")
                if "NO" in correct: return correct.replace("NO", "YES")
                if "no" in correct: return correct.replace("no", "yes")

        return f"{correct}_WRONG"