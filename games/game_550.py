from .base import Game
import re
from collections import deque

class FunctionMappingDeductionGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"函数映射推理"游戏，规则如下：

游戏设定了一个节点集合，编号为 0 到 {n_minus_1}（共 {n} 个节点）。存在两种操作 L 和 S，它们分别对应两个函数 fL 和 fS。对于每个节点 i，fL(i) 和 fS(i) 会将其映射到另一个唯一的节点。这两个函数在整个游戏过程中固定不变，但对你不可见。

游戏公布了起点 Start = {start} 和目标 Goal = {goal}。

你的任务是通过有限次数的查询，推推断出 fL 和 fS 的映射规律，并完成以下三项提交：
1. 提交对 fL 和 fS 的规律描述（可以是通用规则描述，也可以是完整的映射表）
2. 提交一条从 Start 到 Goal 的操作序列（由 L 和 S 组成）
3. 提交从 Start 出发的所有可达节点集合

## 可用的查询类型

你可以进行以下三种查询：

1. 试行查询：从某个节点出发，执行一系列操作，观察完整轨迹和终点
   格式：<query_trial>节点编号: 操作序列</query_trial>
   例如：<query_trial>0: L,S,L</query_trial>
   
2. 单步查询：查询某个节点在某个操作下的直接映射结果
   格式：<query_single>节点编号, 操作</query_single>
   例如：<query_single>3, L</query_single>
   
3. 可达性查询：判断从节点 x 是否能到达节点 y
   格式：<query_reachable>起点, 终点</query_reachable>
   例如：<query_reachable>0, 5</query_reachable>
   如果可达，你可以追加询问最短步数：<query_shortest>起点, 终点</query_shortest>

## 提交最终答案的格式

当你收集到足够信息后，请一次性提交所有答案，格式如下：

<answer>
规律描述: [你对 fL 和 fS 的规律总结，或者完整映射表]
路径序列: [从 Start 到 Goal 的操作序列，用逗号分隔，例如 L,S,L,L]
可达集合: [从 Start 可达的所有节点编号，用逗号分隔，例如 0,1,2,3]
</answer>

注意：
- 每次只能进行一个查询
- 请尽可能少地使用查询次数
- 提交答案后不能再进行查询
- 所有答案必须完全正确才能通过
"""

    game_rule_en = """\
Let's play a "Function Mapping Deduction" game. Here are the rules:

The game defines a set of nodes numbered from 0 to {n_minus_1} (total {n} nodes). There are two operations L and S, corresponding to two functions fL and fS. For each node i, fL(i) and fS(i) map it to another unique node. These two functions remain fixed throughout the game but are hidden from you.

The game announces the starting point Start = {start} and the goal Goal = {goal}.

Your task is to deduce the mapping rules of fL and fS through a limited number of queries, and complete the following three submissions:
1. Submit a description of the rules for fL and fS (can be a general rule description or a complete mapping table)
2. Submit an operation sequence from Start to Goal (composed of L and S)
3. Submit the set of all reachable nodes from Start

## Available Query Types

You can perform the following three types of queries:

1. Trial Query: Starting from a node, execute a sequence of operations and observe the complete trajectory and endpoint
   Format: <query_trial>node_id: operation_sequence</query_trial>
   Example: <query_trial>0: L,S,L</query_trial>
   
2. Single-step Query: Query the direct mapping result of a node under a specific operation
   Format: <query_single>node_id, operation</query_single>
   Example: <query_single>3, L</query_single>
   
3. Reachability Query: Determine if node y can be reached from node x
   Format: <query_reachable>start_node, end_node</query_reachable>
   Example: <query_reachable>0, 5</query_reachable>
   If reachable, you can additionally ask for the shortest distance: <query_shortest>start_node, end_node</query_shortest>

## Final Answer Submission Format

When you have collected enough information, submit all answers at once in the following format:

<answer>
Rule Description: [Your summary of the rules for fL and fS, or complete mapping table]
Path Sequence: [Operation sequence from Start to Goal, comma-separated, e.g., L,S,L,L]
Reachable Set: [All reachable node IDs from Start, comma-separated, e.g., 0,1,2,3]
</answer>

Note:
- Only one query can be made at a time
- Try to minimize the number of queries
- No more queries are allowed after submitting the answer
- All answers must be completely correct to pass
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎使用“城市交通盲测系统”。

本系统包含了一个封闭的交通路网，其中的站点编号为 0 到 {n_minus_1}（共 {n} 个站点）。系统内存在两条专线：L线和S线，它们分别对应两种固定的路线转移逻辑 fL 和 fS。对于任意一个站点 i，乘坐L线或S线会将其分别单向传送至另一个确定的站点。这两条路线的转移规则在测试期间固定不变，且对你保密。

系统当前指派的起点站为 Start = {start}，需要到达的终点站为 Goal = {goal}。

你的任务是通过有限次数的系统查询，摸清 L线和S线 的换乘规律，并完成以下三项成果提交：
1. 提交对 L线和S线 路由规律的描述（可以是对换乘规则的总结，或是完整的站点映射表）
2. 提交一条从起点站 Start 到达终点站 Goal 的乘车序列（由 L 和 S 组成）
3. 提交从 Start 站出发，通过任意次换乘能够抵达的所有可达站点集合

## 可用的查询类型

你可以进行以下三种查询：

1. 试行查询：从某个站点出发，连续乘坐一系列路线，获取完整的途径站点轨迹和最终停靠站
   格式：<query_trial>站点编号: 乘车序列</query_trial>
   例如：<query_trial>0: L,S,L</query_trial>
   
2. 单步查询：查询从某个指定站点乘坐特定路线后的直接到达站点
   格式：<query_single>站点编号, 路线</query_single>
   例如：<query_single>3, L</query_single>
   
3. 可达性查询：判断从站点 x 是否有办法通过换乘抵达站点 y
   格式：<query_reachable>起点站, 终点站</query_reachable>
   例如：<query_reachable>0, 5</query_reachable>
   如果可达，你可以追加询问最少换乘次数：<query_shortest>起点站, 终点站</query_shortest>

## 提交最终答案的格式

当你收集到足够信息后，请一次性提交所有答案，格式如下：

<answer>
规律描述: [你对 L线和S线 的规律总结，或者完整的站点映射表]
路径序列: [从 Start 到 Goal 的乘车路线序列，用逗号分隔，例如 L,S,L,L]
可达集合: [从 Start 可达的所有站点编号，用逗号分隔，例如 0,1,2,3]
</answer>

注意：
- 每次只能进行一个查询
- 请尽可能少地使用查询次数
- 提交答案后不能再进行查询
- 所有答案必须完全正确才能通过
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Transit Blind Test System."

This system contains a closed traffic network with stations numbered from 0 to {n_minus_1} (total {n} stations). There are two dedicated lines: Line L and Line S, which correspond to two fixed routing logic functions fL and fS. For any station i, taking Line L or Line S will transfer you one-way to another specific station. The routing rules for these two lines remain fixed during the test but are hidden from you.

The system has assigned the starting station Start = {start} and the destination station Goal = {goal}.

Your task is to figure out the transfer rules of Line L and Line S through a limited number of system queries, and complete the following three submissions:
1. Submit a description of the routing rules for Line L and Line S (can be a summary of the transfer rules or a complete station mapping table)
2. Submit a boarding sequence from Start to Goal (composed of L and S)
3. Submit the set of all reachable stations from Start through any number of transfers

## Available Query Types

You can perform the following three types of queries:

1. Trial Query: Starting from a station, continuously take a sequence of lines, and obtain the complete trajectory of stations passed and the final stop
   Format: <query_trial>station_id: boarding_sequence</query_trial>
   Example: <query_trial>0: L,S,L</query_trial>
   
2. Single-step Query: Query the direct arrival station after taking a specific line from a designated station
   Format: <query_single>station_id, line</query_single>
   Example: <query_single>3, L</query_single>
   
3. Reachability Query: Determine if station y can be reached from station x through transfers
   Format: <query_reachable>start_station, end_station</query_reachable>
   Example: <query_reachable>0, 5</query_reachable>
   If reachable, you can additionally ask for the minimum number of transfers: <query_shortest>start_station, end_station</query_shortest>

## Final Answer Submission Format

When you have collected enough information, submit all answers at once in the following format:

<answer>
Rule Description: [Your summary of the rules for Line L and Line S, or complete station mapping table]
Path Sequence: [Boarding sequence from Start to Goal, comma-separated, e.g., L,S,L,L]
Reachable Set: [All reachable station IDs from Start, comma-separated, e.g., 0,1,2,3]
</answer>

Note:
- Only one query can be made at a time
- Try to minimize the number of queries
- No more queries are allowed after submitting the answer
- All answers must be completely correct to pass
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎进入“临床疗法推演辅助系统”。

系统记录了一组患者的临床指征状态，状态编号为 0 到 {n_minus_1}（共 {n} 种状态）。目前正在测试两种新型干预手段：L疗法和S疗法，它们分别对应两种状态转化机制 fL 和 fS。对于处于状态 i 的患者，施加L疗法或S疗法会使其临床状态不可逆地转化为另一个特定的状态。这两种疗法的转化机制在推演过程中保持恒定，但对作为研究员的你处于盲测掩蔽状态。

本次推演的初始状态 Start = {start}，期望达到的目标康复状态 Goal = {goal}。

你的任务是通过有限次数的临床测试查询，揭示 L疗法和S疗法 的状态转化规律，并完成以下三项报告提交：
1. 提交对 L疗法和S疗法 药效规律的描述（可以是转化机制的总结，或完整的状态转移表）
2. 提交一套从 Start 状态引导至 Goal 状态的干预序列（由 L 和 S 组成）
3. 提交从 Start 状态出发，经过任意次干预可能演变出的所有临床状态集合

## 可用的查询类型

你可以进行以下三种查询：

1. 试行查询：从某个状态开始，连续施加一系列干预手段，观察完整的状态演变轨迹和最终状态
   格式：<query_trial>状态编号: 干预序列</query_trial>
   例如：<query_trial>0: L,S,L</query_trial>
   
2. 单步查询：查询某个状态在单次施加特定疗法后的直接转化结果
   格式：<query_single>状态编号, 疗法</query_single>
   例如：<query_single>3, L</query_single>
   
3. 可达性查询：判断能否通过一系列干预将状态 x 转化为状态 y
   格式：<query_reachable>初始状态, 目标状态</query_reachable>
   例如：<query_reachable>0, 5</query_reachable>
   如果可达，你可以追加询问最少需要几个干预步骤：<query_shortest>初始状态, 目标状态</query_shortest>

## 提交最终答案的格式

当你收集到足够信息后，请一次性提交所有答案，格式如下：

<answer>
规律描述: [你对 L疗法和S疗法 转化机制的总结，或者完整的转移表]
路径序列: [从 Start 到 Goal 的干预序列，用逗号分隔，例如 L,S,L,L]
可达集合: [从 Start 可达的所有状态编号，用逗号分隔，例如 0,1,2,3]
</answer>

注意：
- 每次只能进行一个查询
- 请尽可能少地使用查询次数
- 提交答案后不能再进行查询
- 所有答案必须完全正确才能通过
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Clinical Therapy Deduction Support System."

The system records a set of patient clinical indication states, numbered from 0 to {n_minus_1} (total {n} states). Two novel intervention methods are currently being tested: Therapy L and Therapy S, which correspond to two state transition mechanisms, fL and fS. For a patient in state i, administering Therapy L or Therapy S will irreversibly transform their clinical state to another specific state. The transition mechanisms of these two therapies remain constant during the deduction process but are under a blind test masking state for you as the researcher.

The initial state for this deduction is Start = {start}, and the desired target recovery state is Goal = {goal}.

Your task is to reveal the state transition rules of Therapy L and Therapy S through a limited number of clinical test queries, and complete the following three report submissions:
1. Submit a description of the efficacy rules for Therapy L and Therapy S (can be a summary of the transition mechanisms or a complete state transition table)
2. Submit an intervention sequence from the Start state to the Goal state (composed of L and S)
3. Submit the set of all clinical states that can potentially evolve from the Start state through any number of interventions

## Available Query Types

You can perform the following three types of queries:

1. Trial Query: Starting from a state, continuously administer a sequence of interventions, and observe the complete state evolution trajectory and final state
   Format: <query_trial>state_id: intervention_sequence</query_trial>
   Example: <query_trial>0: L,S,L</query_trial>
   
2. Single-step Query: Query the direct transition result of a state after a single administration of a specific therapy
   Format: <query_single>state_id, therapy</query_single>
   Example: <query_single>3, L</query_single>
   
3. Reachability Query: Determine if state x can be transformed into state y through a series of interventions
   Format: <query_reachable>initial_state, target_state</query_reachable>
   Example: <query_reachable>0, 5</query_reachable>
   If reachable, you can additionally ask for the minimum number of intervention steps: <query_shortest>initial_state, target_state</query_shortest>

## Final Answer Submission Format

When you have collected enough information, submit all answers at once in the following format:

<answer>
Rule Description: [Your summary of the transition mechanisms for Therapy L and Therapy S, or complete transition table]
Path Sequence: [Intervention sequence from Start to Goal, comma-separated, e.g., L,S,L,L]
Reachable Set: [All reachable state IDs from Start, comma-separated, e.g., 0,1,2,3]
</answer>

Note:
- Only one query can be made at a time
- Try to minimize the number of queries
- No more queries are allowed after submitting the answer
- All answers must be completely correct to pass
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎进入“自适应学习路径规划系统”。

课程库中包含了一系列知识模块，编号为 0 到 {n_minus_1}（共 {n} 个模块）。系统提供两种教学活动：L型讲授课和S型研讨课，它们分别对应两种知识进阶逻辑 fL 和 fS。对于当前处于模块 i 的学生，完成L型课或S型课后，系统会将其导向另一个特定的知识模块。这两种课程的导向规则在规划期间固定不变，但需要你通过测试来摸索。

当前学生的起始模块 Start = {start}，需要掌握的核心目标模块 Goal = {goal}。

你的任务是通过有限次数的教学模拟查询，推断出 L型课和S型课 的进阶规律，并完成以下三项方案提交：
1. 提交对 L型课和S型课 导向规律的描述（可以是教学逻辑总结，或是完整的模块映射表）
2. 提交一条从起始模块 Start 推进到目标模块 Goal 的课程修读序列（由 L 和 S 组成）
3. 提交从 Start 模块出发，通过任意课程组合所能解锁的所有可达模块集合

## 可用的查询类型

你可以进行以下三种查询：

1. 试行查询：从某个模块出发，连续完成一系列课程，观察完整的学习轨迹和最终到达的模块
   格式：<query_trial>模块编号: 课程序列</query_trial>
   例如：<query_trial>0: L,S,L</query_trial>
   
2. 单步查询：查询在某个模块完成特定课程后的直接导向结果
   格式：<query_single>模块编号, 课程类型</query_single>
   例如：<query_single>3, L</query_single>
   
3. 可达性查询：判断能否从模块 x 经过一系列学习到达模块 y
   格式：<query_reachable>起始模块, 目标模块</query_reachable>
   例如：<query_reachable>0, 5</query_reachable>
   如果可达，你可以追加询问最少需要完成的课程数：<query_shortest>起始模块, 目标模块</query_shortest>

## 提交最终答案的格式

当你收集到足够信息后，请一次性提交所有答案，格式如下：

<answer>
规律描述: [你对 L型课和S型课 导向规律的总结，或者完整的映射表]
路径序列: [从 Start 到 Goal 的课程序列，用逗号分隔，例如 L,S,L,L]
可达集合: [从 Start 可达的所有模块编号，用逗号分隔，例如 0,1,2,3]
</answer>

注意：
- 每次只能进行一个查询
- 请尽可能少地使用查询次数
- 提交答案后不能再进行查询
- 所有答案必须完全正确才能通过
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Planning System."

The course library contains a series of knowledge modules, numbered from 0 to {n_minus_1} (total {n} modules). The system provides two types of learning activities: Lecture Module (L) and Seminar Module (S), which correspond to two knowledge progression logic functions, fL and fS. For a student currently in module i, completing course L or course S will direct them to another specific knowledge module. The directing rules of these two courses remain fixed during the planning phase, but you need to discover them through testing.

The student's starting module is Start = {start}, and the core target module to master is Goal = {goal}.

Your task is to deduce the progression rules of Course L and Course S through a limited number of teaching simulation queries, and complete the following three plan submissions:
1. Submit a description of the directing rules for Course L and Course S (can be a summary of the teaching logic or a complete module mapping table)
2. Submit a course study sequence to progress from the Start module to the Goal module (composed of L and S)
3. Submit the set of all reachable modules that can be unlocked from the Start module through any combination of courses

## Available Query Types

You can perform the following three types of queries:

1. Trial Query: Starting from a module, continuously complete a sequence of courses, and observe the complete learning trajectory and final reached module
   Format: <query_trial>module_id: course_sequence</query_trial>
   Example: <query_trial>0: L,S,L</query_trial>
   
2. Single-step Query: Query the direct directing result after completing a specific course from a module
   Format: <query_single>module_id, course_type</query_single>
   Example: <query_single>3, L</query_single>
   
3. Reachability Query: Determine if module y can be reached from module x through a series of learning steps
   Format: <query_reachable>start_module, target_module</query_reachable>
   Example: <query_reachable>0, 5</query_reachable>
   If reachable, you can additionally ask for the minimum number of courses required: <query_shortest>start_module, target_module</query_shortest>

## Final Answer Submission Format

When you have collected enough information, submit all answers at once in the following format:

<answer>
Rule Description: [Your summary of the directing rules for Course L and Course S, or complete mapping table]
Path Sequence: [Course sequence from Start to Goal, comma-separated, e.g., L,S,L,L]
Reachable Set: [All reachable module IDs from Start, comma-separated, e.g., 0,1,2,3]
</answer>

Note:
- Only one query can be made at a time
- Try to minimize the number of queries
- No more queries are allowed after submitting the answer
- All answers must be completely correct to pass
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎使用“柔性制造流水线排程系统”。

车间内包含多个标准的生产工序节点，编号为 0 到 {n_minus_1}（共 {n} 个节点）。生产线上配备了两种核心加工工艺：L型工艺和S型工艺，它们分别对应两种工序流转机制 fL 和 fS。对于处于节点 i 的半成品，执行L工艺或S工艺后，会被自动传送至另一个特定的工序节点。这两种工艺的流转规则在当前批次生产中固定不变，但暂未写入你的排程手册。

本次生产任务的初始毛坯节点 Start = {start}，要求交付的成品检验节点 Goal = {goal}。

你的任务是通过有限次数的打样查询，破译 L型和S型工艺 的流转规律，并完成以下三项排程提交：
1. 提交对 L型和S型工艺 流转规律的描述（可以是规则总结，或完整的节点映射表）
2. 提交一条从初始节点 Start 加工至成品节点 Goal 的工艺执行序列（由 L 和 S 组成）
3. 提交从 Start 节点出发，经过任意次加工能触达的所有工序节点集合

## 可用的查询类型

你可以进行以下三种查询：

1. 试行查询：从某个节点投入半成品，连续执行一系列工艺，观察完整的流转轨迹和最终所处节点
   格式：<query_trial>节点编号: 工艺序列</query_trial>
   例如：<query_trial>0: L,S,L</query_trial>
   
2. 单步查询：查询某个节点在执行单次特定工艺后的直接流转结果
   格式：<query_single>节点编号, 工艺</query_single>
   例如：<query_single>3, L</query_single>
   
3. 可达性查询：评估从节点 x 的半成品能否通过后续加工转化为节点 y 的形态
   格式：<query_reachable>起始节点, 目标节点</query_reachable>
   例如：<query_reachable>0, 5</query_reachable>
   如果可达，你可以追加询问最短加工工序数：<query_shortest>起始节点, 目标节点</query_shortest>

## 提交最终答案的格式

当你收集到足够信息后，请一次性提交所有答案，格式如下：

<answer>
规律描述: [你对工艺流转规律的总结，或者完整的流转表]
路径序列: [从 Start 到 Goal 的工艺序列，用逗号分隔，例如 L,S,L,L]
可达集合: [从 Start 可达的所有节点编号，用逗号分隔，例如 0,1,2,3]
</answer>

注意：
- 每次只能进行一个查询
- 请尽可能少地使用查询次数
- 提交答案后不能再进行查询
- 所有答案必须完全正确才能通过
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Flexible Manufacturing Assembly Line Scheduling System."

The workshop contains multiple standard production step nodes, numbered from 0 to {n_minus_1} (total {n} nodes). The production line is equipped with two core processing techniques: Process L and Process S, which correspond to two step routing mechanisms, fL and fS. For a semi-finished product at node i, executing Process L or Process S will automatically transport it to another specific production step node. The routing rules for these two processes remain fixed in the current batch production but have not yet been written into your scheduling manual.

The initial raw material node for this production task is Start = {start}, and the finished product inspection node required for delivery is Goal = {goal}.

Your task is to decipher the routing rules of Process L and Process S through a limited number of proofing queries, and complete the following three scheduling submissions:
1. Submit a description of the routing rules for Process L and Process S (can be a summary of the rules or a complete node mapping table)
2. Submit a process execution sequence to manufacture from the Start node to the Goal node (composed of L and S)
3. Submit the set of all production step nodes that can be reached from the Start node through any number of processing steps

## Available Query Types

You can perform the following three types of queries:

1. Trial Query: Starting from a node with a semi-finished product, continuously execute a sequence of processes, and observe the complete routing trajectory and final node
   Format: <query_trial>node_id: process_sequence</query_trial>
   Example: <query_trial>0: L,S,L</query_trial>
   
2. Single-step Query: Query the direct routing result of a node after executing a single specific process
   Format: <query_single>node_id, process</query_single>
   Example: <query_single>3, L</query_single>
   
3. Reachability Query: Evaluate if a semi-finished product at node x can be transformed into the state at node y through subsequent processing
   Format: <query_reachable>start_node, target_node</query_reachable>
   Example: <query_reachable>0, 5</query_reachable>
   If reachable, you can additionally ask for the minimum number of processing steps: <query_shortest>start_node, target_node</query_shortest>

## Final Answer Submission Format

When you have collected enough information, submit all answers at once in the following format:

<answer>
Rule Description: [Your summary of the process routing rules, or complete routing table]
Path Sequence: [Process sequence from Start to Goal, comma-separated, e.g., L,S,L,L]
Reachable Set: [All reachable node IDs from Start, comma-separated, e.g., 0,1,2,3]
</answer>

Note:
- Only one query can be made at a time
- Try to minimize the number of queries
- No more queries are allowed after submitting the answer
- All answers must be completely correct to pass
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎使用“司法程序流转模拟系统”。

司法管辖区内设立了多个案件流转节点，编号为 0 到 {n_minus_1}（共 {n} 个节点）。在案件审理过程中，存在两种合法的程序操作：L型动议和S型特别审查，它们分别对应两种程序流转规则 fL 和 fS。对于处于节点 i 的案件，提起L型动议或S型审查会使案件移交至另一个特定的流转节点。这两种操作的移交规则在整个模拟庭审期间具有强制约束力且固定不变，但你需要通过实证案例来推演其机制。

当前案件的立案初审节点 Start = {start}，原告期望达到的终审判决节点 Goal = {goal}。

你的任务是通过有限次数的判例查询，推断出 L型动议和S型审查 的流转规律，并完成以下三项法律意见提交：
1. 提交对两种程序流转规律的描述（可以是法理规则总结，或完整的节点映射表）
2. 提交一条从初审节点 Start 推进至终审节点 Goal 的程序操作序列（由 L 和 S 组成）
3. 提交从 Start 节点出发，穷尽所有程序操作后可能涉及的所有流转节点集合

## 可用的查询类型

你可以进行以下三种查询：

1. 试行查询：从某个节点开始，连续提起一系列程序操作，观察完整的案件流转轨迹和最终搁置节点
   格式：<query_trial>节点编号: 操作序列</query_trial>
   例如：<query_trial>0: L,S,L</query_trial>
   
2. 单步查询：查询某个节点在单次执行特定程序操作后的直接移交结果
   格式：<query_single>节点编号, 操作</query_single>
   例如：<query_single>3, L</query_single>
   
3. 可达性查询：判断案件能否从流转节点 x 经过合法程序推进至节点 y
   格式：<query_reachable>当前节点, 目标节点</query_reachable>
   例如：<query_reachable>0, 5</query_reachable>
   如果可达，你可以追加询问最少需要的程序操作次数：<query_shortest>当前节点, 目标节点</query_shortest>

## 提交最终答案的格式

当你收集到足够信息后，请一次性提交所有答案，格式如下：

<answer>
规律描述: [你对程序流转规律的总结，或者完整的映射表]
路径序列: [从 Start 到 Goal 的程序操作序列，用逗号分隔，例如 L,S,L,L]
可达集合: [从 Start 可及的所有节点编号，用逗号分隔，例如 0,1,2,3]
</answer>

注意：
- 每次只能进行一个查询
- 请尽可能少地使用查询次数
- 提交答案后不能再进行查询
- 所有答案必须完全正确才能通过
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Procedure Routing Simulation System."

Within the jurisdiction, multiple case routing nodes have been established, numbered from 0 to {n_minus_1} (total {n} nodes). During the case trial process, there are two legal procedural operations: Motion L and Special Review S, which correspond to two procedural routing rules, fL and fS. For a case at node i, filing Motion L or Review S will transfer the case to another specific routing node. The transfer rules of these two operations have mandatory binding force and remain fixed throughout the mock trial period, but you need to deduce their mechanisms through empirical case studies.

The initial filing review node of the current case is Start = {start}, and the final judgment node desired by the plaintiff is Goal = {goal}.

Your task is to deduce the routing rules of Motion L and Review S through a limited number of precedent queries, and complete the following three legal opinion submissions:
1. Submit a description of the two procedural routing rules (can be a summary of jurisprudential rules or a complete node mapping table)
2. Submit a procedural operation sequence to advance from the Start node to the Goal node (composed of L and S)
3. Submit the set of all routing nodes that can possibly be involved starting from the Start node after exhausting all procedural operations

## Available Query Types

You can perform the following three types of queries:

1. Trial Query: Starting from a node, continuously file a sequence of procedural operations, and observe the complete case routing trajectory and final resting node
   Format: <query_trial>node_id: operation_sequence</query_trial>
   Example: <query_trial>0: L,S,L</query_trial>
   
2. Single-step Query: Query the direct transfer result of a node after a single execution of a specific procedural operation
   Format: <query_single>node_id, operation</query_single>
   Example: <query_single>3, L</query_single>
   
3. Reachability Query: Determine if a case can be legally advanced from routing node x to node y
   Format: <query_reachable>current_node, target_node</query_reachable>
   Example: <query_reachable>0, 5</query_reachable>
   If reachable, you can additionally ask for the minimum number of procedural operations required: <query_shortest>current_node, target_node</query_shortest>

## Final Answer Submission Format

When you have collected enough information, submit all answers at once in the following format:

<answer>
Rule Description: [Your summary of the procedural routing rules, or complete mapping table]
Path Sequence: [Procedural operation sequence from Start to Goal, comma-separated, e.g., L,S,L,L]
Reachable Set: [All reachable node IDs from Start, comma-separated, e.g., 0,1,2,3]
</answer>

Note:
- Only one query can be made at a time
- Try to minimize the number of queries
- No more queries are allowed after submitting the answer
- All answers must be completely correct to pass
"""

    tags = ["answer", "query_trial", "query_single", "query_reachable", "query_shortest"]

    # 五种难度配置
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {  # 简单：N=6, 简单的加法规则
                "n": 6,
                "start": 0,
                "goal": 3,
                "fL": lambda i, n: (i + 1) % n,  # fL(i) = (i+1) mod 6
                "fS": lambda i, n: (i + 2) % n,  # fS(i) = (i+2) mod 6
            },
            2: {  # 中等偏下：N=7, 稍复杂的规则
                "n": 7,
                "start": 0,
                "goal": 5,
                "fL": lambda i, n: (i + 3) % n,  # fL(i) = (i+3) mod 7
                "fS": lambda i, n: (i * 2) % n,  # fS(i) = (i*2) mod 7
            },
            3: {  # 中等偏上：N=8, 混合规则
                "n": 8,
                "start": 1,
                "goal": 6,
                "fL": lambda i, n: (i + 3) % n,  # fL(i) = (i+3) mod 8
                "fS": lambda i, n: (i * 3) % n,  # fS(i) = (i*3) mod 8
            },
            4: {  # 较难：N=10, 更复杂的规则
                "n": 10,
                "start": 0,
                "goal": 7,
                "fL": lambda i, n: (i * 3 + 1) % n,  # fL(i) = (i*3+1) mod 10
                "fS": lambda i, n: (i * 7) % n,      # fS(i) = (i*7) mod 10
            },
            5: {  # 难：N=12, 复杂规则
                "n": 12,
                "start": 0,
                "goal": 11,
                "fL": lambda i, n: (i * 5 + 1) % n,  # fL(i) = (i*5+1) mod 12
                "fS": lambda i, n: (i * 7 + 3) % n,  # fS(i) = (i*7+3) mod 12
            },
        },
        "en": {
            1: {
                "n": 6,
                "start": 0,
                "goal": 3,
                "fL": lambda i, n: (i + 1) % n,
                "fS": lambda i, n: (i + 2) % n,
            },
            2: {
                "n": 7,
                "start": 0,
                "goal": 5,
                "fL": lambda i, n: (i + 3) % n,
                "fS": lambda i, n: (i * 2) % n,
            },
            3: {
                "n": 8,
                "start": 1,
                "goal": 6,
                "fL": lambda i, n: (i + 3) % n,
                "fS": lambda i, n: (i * 3) % n,
            },
            4: {
                "n": 10,
                "start": 0,
                "goal": 7,
                "fL": lambda i, n: (i * 3 + 1) % n,
                "fS": lambda i, n: (i * 7) % n,
            },
            5: {
                "n": 12,
                "start": 0,
                "goal": 11,
                "fL": lambda i, n: (i * 5 + 1) % n,
                "fS": lambda i, n: (i * 7 + 3) % n,
            },
        },
    }

    def __init__(self, config):
        # 查询计数器
        self.trial_count = 0
        self.single_count = 0
        self.reachable_count = 0
        self.shortest_count = 0
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.start = cfg["start"]
        self.goal = cfg["goal"]
        self.fL_func = cfg["fL"]
        self.fS_func = cfg["fS"]

        # 预计算完整映射表
        self.fL_map = {i: self.fL_func(i, self.n) for i in range(self.n)}
        self.fS_map = {i: self.fS_func(i, self.n) for i in range(self.n)}

        # 预计算从 start 的可达节点集合
        self.reachable_set = self._compute_reachable(self.start)

        # 设置游戏信息用于规则模板
        self._game_info = {
            "n": self.n,
            "n_minus_1": self.n - 1,
            "start": self.start,
            "goal": self.goal,
        }

    def _compute_reachable(self, start_node):
        """BFS计算从start_node可达的所有节点"""
        visited = set()
        queue = deque([start_node])
        visited.add(start_node)

        while queue:
            node = queue.popleft()
            for next_node in [self.fL_map[node], self.fS_map[node]]:
                if next_node not in visited:
                    visited.add(next_node)
                    queue.append(next_node)

        return visited

    def _compute_shortest_path(self, start_node, end_node):
        """BFS计算从start_node到end_node的最短步数，返回-1表示不可达"""
        if start_node == end_node:
            return 0

        visited = {start_node: 0}
        queue = deque([start_node])

        while queue:
            node = queue.popleft()
            dist = visited[node]

            for next_node in [self.fL_map[node], self.fS_map[node]]:
                if next_node not in visited:
                    visited[next_node] = dist + 1
                    if next_node == end_node:
                        return dist + 1
                    queue.append(next_node)

        return -1

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        忽略无限的 query_trial，仅覆盖有限的 atomic 查询（单步、可达性、最短路）。
        """
        queries = []
        yes_text = "是" if self.config.language == "zh" else "Yes"
        no_text = "否" if self.config.language == "zh" else "No"
        unreachable_text = "不可达" if self.config.language == "zh" else "Unreachable"

        # 1. 单步查询 <query_single>
        for node in range(self.n):
            for op in ['L', 'S']:
                query_str = f"<query_single>{node}, {op}</query_single>"
                if op == 'L':
                    ans = str(self.fL_map[node])
                else:
                    ans = str(self.fS_map[node])
                queries.append({"query": query_str, "answer": ans})

        # 2. 可达性查询 <query_reachable>
        for start in range(self.n):
            for end in range(self.n):
                query_str = f"<query_reachable>{start}, {end}</query_reachable>"
                reachable = end in self._compute_reachable(start)
                ans = yes_text if reachable else no_text
                queries.append({"query": query_str, "answer": ans})

        # 3. 最短路径查询 <query_shortest>
        for start in range(self.n):
            for end in range(self.n):
                query_str = f"<query_shortest>{start}, {end}</query_shortest>"
                dist = self._compute_shortest_path(start, end)
                if dist == -1:
                    ans = unreachable_text
                else:
                    ans = str(dist)
                queries.append({"query": query_str, "answer": ans})

        return queries

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        answer_text = parsed_info["answer"].strip()

        # 解析答案的三个部分
        rule_match = re.search(r'规律描述[:：]\s*(.+?)(?=路径序列|$)', answer_text, re.DOTALL | re.IGNORECASE)
        if not rule_match:
            rule_match = re.search(r'Rule Description[:：]\s*(.+?)(?=Path Sequence|$)', answer_text, re.DOTALL | re.IGNORECASE)
        
        path_match = re.search(r'路径序列[:：]\s*(.+?)(?=可达集合|$)', answer_text, re.DOTALL | re.IGNORECASE)
        if not path_match:
            path_match = re.search(r'Path Sequence[:：]\s*(.+?)(?=Reachable Set|$)', answer_text, re.DOTALL | re.IGNORECASE)
        
        reach_match = re.search(r'可达集合[:：]\s*(.+?)$', answer_text, re.DOTALL | re.IGNORECASE)
        if not reach_match:
            reach_match = re.search(r'Reachable Set[:：]\s*(.+?)$', answer_text, re.DOTALL | re.IGNORECASE)

        if not (rule_match and path_match and reach_match):
            return False

        rule_desc = rule_match.group(1).strip()
        path_seq = path_match.group(1).strip()
        reachable_set_str = reach_match.group(1).strip()

        # 1. 验证规律描述：检查是否包含完整映射表信息
        #    至少需要包含正确的映射关系（检测是否包含若干关键映射结果）
        if not rule_desc or len(rule_desc) < 5:
            return False
        
        # 验证规律描述中至少包含一些正确的映射信息
        # 检查是否能从描述中提取出至少部分正确的映射
        rule_valid = False
        # 检查是否提到了fL和fS（或L和S）的映射
        for node in range(self.n):
            fL_str = f"{node}" 
            if fL_str in rule_desc:
                rule_valid = True
                break
        # 如果规律描述至少引用了节点编号，认为是有效的描述
        if not rule_valid:
            # 退而求其次，只要描述足够长且非空
            if len(rule_desc) < 10:
                return False

        # 2. 验证路径序列
        try:
            ops = [op.strip().upper() for op in path_seq.split(',') if op.strip()]
            if not ops:
                return False
            current = self.start
            for op in ops:
                if op == 'L':
                    current = self.fL_map[current]
                elif op == 'S':
                    current = self.fS_map[current]
                else:
                    return False
            if current != self.goal:
                return False
        except Exception:
            return False

        # 3. 验证可达集合
        try:
            submitted_set = set(int(x.strip()) for x in reachable_set_str.split(',') if x.strip())
            if submitted_set != self.reachable_set:
                return False
        except Exception:
            return False

        return True

    def _cf_core_produce(self, parsed_info):
        """执行原始的核心业务逻辑"""
        yes_text = "是" if self.config.language == "zh" else "Yes"
        no_text = "否" if self.config.language == "zh" else "No"
        error_text = "错误：无效的查询格式或参数" if self.config.language == "zh" else "Error: Invalid query format or parameters"
        limit_text = "查询次数已用尽，请直接提交答案" if self.config.language == "zh" else "Query limit reached, please submit your answer directly"

        # 1. 试行查询
        if "query_trial" in parsed_info:
            self.trial_count += 1
            if self.trial_count > 20:
                return limit_text
            
            try:
                content = parsed_info["query_trial"].strip()
                # 格式：节点编号: 操作序列
                parts = content.split(':')
                if len(parts) != 2:
                    return error_text
                
                start_node = int(parts[0].strip())
                ops_str = parts[1].strip()
                ops = [op.strip().upper() for op in ops_str.split(',') if op.strip()]

                if start_node < 0 or start_node >= self.n:
                    return error_text

                # 执行操作序列
                trajectory = [start_node]
                current = start_node
                for op in ops:
                    if op == 'L':
                        current = self.fL_map[current]
                    elif op == 'S':
                        current = self.fS_map[current]
                    else:
                        return error_text
                    trajectory.append(current)

                # 构造响应
                if self.config.language == "zh":
                    traj_str = " → ".join(str(x) for x in trajectory)
                    return f"轨迹：{traj_str}，终点：{current}"
                else:
                    traj_str = " → ".join(str(x) for x in trajectory)
                    return f"Trajectory: {traj_str}, Endpoint: {current}"

            except Exception:
                return error_text

        # 2. 单步查询
        elif "query_single" in parsed_info:
            self.single_count += 1
            if self.single_count > 50:
                return limit_text
            
            try:
                content = parsed_info["query_single"].strip()
                parts = [x.strip() for x in content.split(',')]
                if len(parts) != 2:
                    return error_text
                
                node = int(parts[0])
                op = parts[1].upper()

                if node < 0 or node >= self.n:
                    return error_text

                if op == 'L':
                    result = self.fL_map[node]
                elif op == 'S':
                    result = self.fS_map[node]
                else:
                    return error_text

                return str(result)

            except Exception:
                return error_text

        # 3. 可达性查询
        elif "query_reachable" in parsed_info:
            self.reachable_count += 1
            if self.reachable_count > 20:
                return limit_text
            
            try:
                content = parsed_info["query_reachable"].strip()
                parts = [x.strip() for x in content.split(',')]
                if len(parts) != 2:
                    return error_text
                
                start_node = int(parts[0])
                end_node = int(parts[1])

                if start_node < 0 or start_node >= self.n or end_node < 0 or end_node >= self.n:
                    return error_text

                reachable = end_node in self._compute_reachable(start_node)
                return yes_text if reachable else no_text

            except Exception:
                return error_text

        # 4. 最短路径查询
        elif "query_shortest" in parsed_info:
            self.shortest_count += 1
            # 最短路径查询作为可达性查询的追问，不单独计数限制
            
            try:
                content = parsed_info["query_shortest"].strip()
                parts = [x.strip() for x in content.split(',')]
                if len(parts) != 2:
                    return error_text
                
                start_node = int(parts[0])
                end_node = int(parts[1])

                if start_node < 0 or start_node >= self.n or end_node < 0 or end_node >= self.n:
                    return error_text

                dist = self._compute_shortest_path(start_node, end_node)
                if dist == -1:
                    return "不可达" if self.config.language == "zh" else "Unreachable"
                else:
                    return str(dist)

            except Exception:
                return error_text

        else:
            return error_text

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个与正确答案不同的错误答案"""
        try:
            val = int(correct.strip())
            wrong_val = (val + 1) % self.n
            return str(wrong_val)
        except ValueError:
            pass

        if "Endpoint:" in correct or "终点：" in correct:
            def _modify_endpoint(m):
                old = int(m.group(1))
                return str((old + 1) % self.n)
            
            modified = re.sub(r'(\d+)\s*$', _modify_endpoint, correct)
            if modified != correct:
                return modified

        yes_text = "是" if self.config.language == "zh" else "Yes"
        no_text = "否" if self.config.language == "zh" else "No"
        if correct.strip() == yes_text:
            return no_text
        if correct.strip() == no_text:
            return yes_text

        unreachable_zh = "不可达"
        unreachable_en = "Unreachable"
        if correct.strip() in (unreachable_zh, unreachable_en):
            return "2"

        return correct + " [modified]"