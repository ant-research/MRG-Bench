from .base import Game
import random

class DegreeZeroIdentificationGame(Game):

    game_rule_zh = """\
我们来玩一个"度零节点识别"的推理游戏，规则如下：

游戏设定了一个固有但未知的无向简单图 G，包含 {n} 个节点，编号为 1 到 {n}。图中某些节点的度为 0（即孤立节点，没有任何边连接），这些节点构成集合 S，该集合在整个游戏中固定但对你未知。

游戏按离散轮次进行（轮次编号 r=1,2,3,...）。每一轮存在一个全局标签基准 L_r，取值为 A 或 B，且满足以下规律：
- 相邻轮次的全局标签基准互为相反，即第 r+1 轮的基准与第 r 轮相反
- 第 1 轮的基准 L_1 未知

在第 r 轮中，每个节点 v 都有一个可见的二值标签，该标签仅由"v 是否属于 S"和当前轮的全局基准 L_r 决定：
- 若节点 v 的度为 0（属于 S），则其标签为 L_r
- 若节点 v 的度不为 0（不属于 S），则其标签为 L_r 的相反值

标签不包含除上述规则外的任何图结构信息。

你可以在每一轮中反复提出以下三类问题（每轮次数不限），我会如实回答：

1. 单点查询：查询节点 i 的当前标签。回答"A"或"B"。
2. 子集计数：给定一个节点子集 U，统计其中标签为 A 的节点个数。回答一个整数。
3. 同标签比较：询问节点 i 和节点 j 的标签是否相同。回答"是"或"否"。

注意：
- 你不能询问邻接关系、度数等图结构信息
- 你不能请求补答历史轮次的查询
- 你不能修改图或节点状态

当你收集到足够信息后，可以提交最终答案。你的目标是准确识别出所有度为 0 的节点。若答案错误、格式不符或交互轮数少于 2 轮，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单点查询（例如查询节点 5）：
<query_node>5</query_node>

- 子集计数（例如统计节点 1,3,5 中标签为 A 的个数）：
<query_count>1,3,5</query_count>

- 同标签比较（例如比较节点 2 和节点 4）：
<query_compare>2,4</query_compare>

- 进入下一轮（当前轮查询结束，准备进入下一轮）：
<next_round></next_round>

提交最终答案时，列出所有度为 0 的节点编号（用逗号隔开，顺序不限），格式如下：
<answer>1,3,5</answer>

如果你认为不存在度为 0 的节点，提交空集：
<answer></answer>
"""

    game_rule_en = """\
Let's play a "Degree-Zero Node Identification" deduction game. Here are the rules:

The game is based on a fixed but unknown undirected simple graph G with {n} nodes, numbered from 1 to {n}. Some nodes in the graph have degree 0 (i.e., isolated nodes with no edges), forming a set S that remains fixed throughout the game but is unknown to you.

The game proceeds in discrete rounds (round number r=1,2,3,...). Each round has a global label baseline L_r, which takes value A or B, and satisfies the following pattern:
- Adjacent rounds have opposite global label baselines, i.e., round r+1's baseline is opposite to round r's
- Round 1's baseline L_1 is unknown

In round r, each node v has a visible binary label determined solely by "whether v belongs to S" and the current round's global baseline L_r:
- If node v has degree 0 (belongs to S), its label is L_r
- If node v has degree not equal to 0 (does not belong to S), its label is the opposite of L_r

The label contains no graph structure information beyond the above rules.

You can repeatedly ask the following three types of questions in each round (unlimited times per round), and I will answer truthfully:

1. Node Query: Query the current label of node i. Answer "A" or "B".
2. Subset Count: Given a node subset U, count how many nodes in it have label A. Answer an integer.
3. Same Label Comparison: Ask whether node i and node j have the same label. Answer "Yes" or "No".

Note:
- You cannot ask about adjacency, degree, or other graph structure information
- You cannot request answers for queries from previous rounds
- You cannot modify the graph or node states

When you have collected enough information, you can submit your final answer. Your goal is to accurately identify all nodes with degree 0. If the answer is wrong, the format is invalid, or the number of interaction rounds is less than 2, the game fails.

Each query must contain only one tag. Use the following XML format:

- Node Query (e.g., querying node 5):
<query_node>5</query_node>

- Subset Count (e.g., counting nodes with label A among nodes 1,3,5):
<query_count>1,3,5</query_count>

- Same Label Comparison (e.g., comparing node 2 and node 4):
<query_compare>2,4</query_compare>

- Next Round (finish current round queries and proceed to next round):
<next_round></next_round>

When submitting the final answer, list all node IDs with degree 0 (comma-separated, order does not matter), using this format:
<answer>1,3,5</answer>

If you believe there are no nodes with degree 0, submit an empty set:
<answer></answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市交通孤岛终端排查系统”。

本系统监控着城市交通主网中的 {n} 个信号灯控制终端，编号为 1 到 {n}。由于施工遗留，部分终端未接入主网，成为没有任何协同连接的“孤岛终端”（构成未知集合 S，该集合在排查期间固定不变）。

排查工作按轮次进行（轮次编号 r=1,2,3,...）。每一轮系统会下发一个全局控制指令 L_r，指令类型为 A（早高峰模式）或 B（晚高峰模式）。指令下发存在以下规律：
- 相邻轮次的全局指令互为相反，即第 r+1 轮的指令与第 r 轮相反
- 第 1 轮的初始指令 L_1 未知

在第 r 轮中，每个终端 v 都会反馈一个可见的运行状态标签，该标签仅由“终端 v 是否属于孤岛终端”和当前轮的全局指令 L_r 决定：
- 若终端 v 是孤岛终端（属于 S），由于未参与协同降噪，其直接反馈原始指令状态，标签为 L_r
- 若终端 v 已接入主网（不属于 S），其为了配合相邻路口相位联动，运行状态将反转，标签为 L_r 的相反值

状态标签不包含除上述规则外的任何网络拓扑结构信息。

你可以在每一轮中反复发起以下三类查询（每轮次数不限），系统会如实返回：

1. 单点状态查询：查询终端 i 的当前运行状态标签。返回“A”或“B”。
2. 区域状态计数：给定一个终端子集 U，统计其中状态标签为 A 的终端个数。返回一个整数。
3. 同态比对查询：询问终端 i 和终端 j 的状态标签是否相同。返回“是”或“否”。

注意：
- 你不能询问网络邻接关系、连接度数等拓扑信息
- 你不能请求系统补答历史轮次的查询
- 你不能修改网络配置或终端状态

当你收集到足够信息后，可以提交最终排查报告。你的目标是准确识别出所有孤岛终端。若答案错误、格式不符或交互轮数少于 2 轮，排查任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单点状态查询（例如查询终端 5）：
<query_node>5</query_node>

- 区域状态计数（例如统计终端 1,3,5 中标签为 A 的个数）：
<query_count>1,3,5</query_count>

- 同态比对查询（例如比较终端 2 和终端 4）：
<query_compare>2,4</query_compare>

- 进入下一轮（当前轮查询结束，系统下发新一轮指令）：
<next_round></next_round>

提交最终排查报告时，列出所有孤岛终端编号（用逗号隔开，顺序不限），格式如下：
<answer>1,3,5</answer>

如果你认为不存在孤岛终端，提交空集：
<answer></answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Isolated Terminal Detection System".

This system monitors {n} traffic light control terminals in the city's main traffic network, numbered from 1 to {n}. Due to legacy construction, some terminals are not connected to the main network, becoming "isolated terminals" with no collaborative connections (forming an unknown set S that remains fixed during the detection process).

The detection operates in rounds (round number r=1,2,3,...). In each round, the system issues a global control command L_r, which can be type A (Morning Peak Mode) or B (Evening Peak Mode). The command issuance follows this pattern:
- Commands in adjacent rounds are completely opposite, i.e., round r+1's command is the opposite of round r's.
- The initial command L_1 in round 1 is unknown.

In round r, each terminal v returns a visible operational state label, determined solely by "whether terminal v is an isolated terminal" and the current round's global command L_r:
- If terminal v is an isolated terminal (belongs to S), it directly reflects the original command state due to the lack of collaborative noise reduction, so its label is L_r.
- If terminal v is connected to the main network (does not belong to S), its operational state is inverted to coordinate phase linkage with adjacent intersections, making its label the opposite of L_r.

The state labels contain no network topology information beyond the above rules.

You can repeatedly initiate the following three types of queries in each round (unlimited times per round), and the system will answer truthfully:

1. Single State Query: Query the current operational state label of terminal i. Returns "A" or "B".
2. Regional State Count: Given a terminal subset U, count how many terminals have the state label A. Returns an integer.
3. Homomorphic Comparison Query: Ask whether terminal i and terminal j have the same state label. Returns "Yes" or "No".

Note:
- You cannot ask about network adjacency, connectivity degree, or other topological information.
- You cannot request the system to retroactively answer queries from previous rounds.
- You cannot modify network configurations or terminal states.

When you have collected enough information, you can submit the final detection report. Your goal is to accurately identify all isolated terminals. If the answer is incorrect, the format is invalid, or the number of interaction rounds is less than 2, the detection task fails.

Each query must contain only one tag. Please use the following XML format:

- Single State Query (e.g., querying terminal 5):
<query_node>5</query_node>

- Regional State Count (e.g., counting terminals with label A among terminals 1,3,5):
<query_count>1,3,5</query_count>

- Homomorphic Comparison Query (e.g., comparing terminal 2 and terminal 4):
<query_compare>2,4</query_compare>

- Next Round (finish current round queries, and the system issues the next round's command):
<next_round></next_round>

When submitting the final detection report, list all isolated terminal IDs (comma-separated, order does not matter) using this format:
<answer>1,3,5</answer>

If you believe there are no isolated terminals, submit an empty set:
<answer></answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“流行病学病房体征监测系统”。

住院部当前有 {n} 名确诊患者，编号为 1 到 {n}。由于体质差异，部分患者为未发生任何病原体交叉感染的“抗体携带者”（这类孤立未感染个体构成未知集合 S，该集合在监测期间固定不变）。

监测程序按周期轮次进行（轮次编号 r=1,2,3,...）。每个监测周期病房会调节出一个全局环境基准 L_r，取值为 A（升温周期）或 B（降温周期）。环境基准的变化存在以下规律：
- 相邻周期的环境基准互为相反，即第 r+1 周期的基准与第 r 周期相反
- 第 1 周期的初始基准 L_1 未知

在第 r 周期中，每位患者 v 都会显现一个可见的二值体征标签，该标签仅由“患者 v 是否为抗体携带者”和当前周期的环境基准 L_r 决定：
- 若患者 v 是抗体携带者（属于 S），其体征正向反馈环境周期，标签为 L_r
- 若患者 v 已发生交叉感染（不属于 S），受群体免疫负反馈机制影响，其体征反应将发生翻转，标签为 L_r 的相反值

体征标签不包含除上述规则外的任何接触史或传播链结构信息。

你可以在每一周期中反复发起以下三类查询（每周期次数不限），系统会如实返回：

1. 单体体征查询：查询患者 i 的当前体征标签。返回“A”或“B”。
2. 群组活跃统计：给定一个患者子集 U，统计其中体征标签为 A 的患者个数。返回一个整数。
3. 同征比弹查询：询问患者 i 和患者 j 的体征标签是否相同。返回“是”或“否”。

注意：
- 你不能询问接触关系、感染链条等流行病学拓扑信息
- 你不能请求系统补答历史周期的查询
- 你不能修改病房参数或患者状态

当你收集到足够信息后，可以提交最终诊断报告。你的目标是准确识别出所有抗体携带者（即孤立个体）。若答案错误、格式不符或交互轮数少于 2 轮，监测任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单体体征查询（例如查询患者 5）：
<query_node>5</query_node>

- 群组活跃统计（例如统计患者 1,3,5 中标签为 A 的个数）：
<query_count>1,3,5</query_count>

- 同征比对查询（例如比较患者 2 和患者 4）：
<query_compare>2,4</query_compare>

- 进入下一周期（当前周期查询结束，系统调节新一周期环境）：
<next_round></next_round>

提交最终诊断报告时，列出所有抗体携带者编号（用逗号隔开，顺序不限），格式如下：
<answer>1,3,5</answer>

如果你认为不存在抗体携带者，提交空集：
<answer></answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Epidemiological Ward Vital Signs Monitoring System".

The inpatient department currently has {n} diagnosed patients, numbered from 1 to {n}. Due to physiological differences, some patients are "antibody carriers" who have not undergone any cross-infection of pathogens (these isolated uninfected individuals form an unknown set S, which remains fixed during monitoring).

The monitoring procedure operates in periodic rounds (round number r=1,2,3,...). In each monitoring period, the ward adjusts to a global environmental baseline L_r, which is either A (Heating Cycle) or B (Cooling Cycle). The environmental baseline shifts follow this pattern:
- The environmental baselines in adjacent periods are entirely opposite, i.e., period r+1's baseline is the opposite of period r's.
- The initial baseline L_1 in period 1 is unknown.

In period r, each patient v exhibits a visible binary vital sign label, determined solely by "whether patient v is an antibody carrier" and the current period's environmental baseline L_r:
- If patient v is an antibody carrier (belongs to S), their vitals provide positive feedback to the environmental cycle, so their label is L_r.
- If patient v has undergone cross-infection (does not belong to S), influenced by the negative feedback mechanism of herd immunity, their vital reaction is inverted, making their label the opposite of L_r.

The vital sign labels contain no contact history or transmission chain topology information beyond the above rules.

You can repeatedly initiate the following three types of queries in each period (unlimited times per period), and the system will answer truthfully:

1. Single Vital Query: Query the current vital sign label of patient i. Returns "A" or "B".
2. Group Activity Statistic: Given a patient subset U, count how many patients have the vital sign label A. Returns an integer.
3. Homogeneous Comparison Query: Ask whether patient i and patient j have the same vital sign label. Returns "Yes" or "No".

Note:
- You cannot ask about contact relationships, infection chains, or other epidemiological topological information.
- You cannot request the system to retroactively answer queries from previous periods.
- You cannot modify ward parameters or patient states.

When you have collected enough information, you can submit the final diagnosis report. Your goal is to accurately identify all antibody carriers (i.e., isolated individuals). If the answer is incorrect, the format is invalid, or the number of interaction rounds is less than 2, the monitoring task fails.

Each query must contain only one tag. Please use the following XML format:

- Single Vital Query (e.g., querying patient 5):
<query_node>5</query_node>

- Group Activity Statistic (e.g., counting patients with label A among patients 1,3,5):
<query_count>1,3,5</query_count>

- Homogeneous Comparison Query (e.g., comparing patient 2 and patient 4):
<query_compare>2,4</query_compare>

- Next Period (finish current period queries, and the system adjusts to the next period's environment):
<next_round></next_round>

When submitting the final diagnosis report, list all antibody carrier IDs (comma-separated, order does not matter) using this format:
<answer>1,3,5</answer>

If you believe there are no antibody carriers, submit an empty set:
<answer></answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“在线学习平台互助分析系统”。

本平台当前运行着 {n} 个学习小组，编号为 1 到 {n}。由于学习习惯的差异，部分小组未与其他任何小组建立互动关联，成为彻底的“独立小组”（这些孤立小组构成未知集合 S，该集合在分析期间固定不变）。

分析工作按教学轮次进行（轮次编号 r=1,2,3,...）。每一轮平台会下发一种全局教学引导模式 L_r，类型为 A（探究模式）或 B（讲授模式）。引导模式存在以下规律：
- 相邻轮次的引导模式互为相反，即第 r+1 轮的模式与第 r 轮相反
- 第 1 轮的初始模式 L_1 未知

在第 r 轮中，每个小组 v 都会呈现一个可见的讨论活跃度标签，该标签仅由“小组 v 是否为独立小组”和当前轮的引导模式 L_r 决定：
- 若小组 v 是独立小组（属于 S），由于无外界干扰，其活跃度严格跟随平台的引导模式，标签为 L_r
- 若小组 v 与外界存在互动关联（不属于 S），受群体互补效应影响，其活跃度表现将发生反转，标签为 L_r 的相反值

活跃度标签不包含除上述规则外的任何小组社交拓扑信息。

你可以在每一轮中反复发起以下三类查询（每轮次数不限），系统会如实返回：

1. 单点活跃度查询：查询小组 i 的当前活跃度标签。返回“A”或“B”。
2. 子集高活跃统计：给定一个小组子集 U，统计其中活跃度标签为 A 的小组个数。返回一个整数。
3. 同活跃度比对：询问小组 i 和小组 j 的活跃度标签是否相同。返回“是”或“否”。

注意：
- 你不能询问小组间的关注关系、互动频次等社交拓扑信息
- 你不能请求系统补答历史轮次的查询
- 你不能修改平台配置或小组状态

当你收集到足够信息后，可以提交最终评估报告。你的目标是准确识别出所有独立小组。若答案错误、格式不符或交互轮数少于 2 轮，分析任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单点活跃度查询（例如查询小组 5）：
<query_node>5</query_node>

- 子集高活跃统计（例如统计小组 1,3,5 中标签为 A 的个数）：
<query_count>1,3,5</query_count>

- 同活跃度比对（例如比较小组 2 和小组 4）：
<query_compare>2,4</query_compare>

- 进入下一轮（当前轮查询结束，平台下发新一轮引导模式）：
<next_round></next_round>

提交最终评估报告时，列出所有独立小组编号（用逗号隔开，顺序不限），格式如下：
<answer>1,3,5</answer>

如果你认为不存在独立小组，提交空集：
<answer></answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Online Learning Platform Peer Analysis System".

The platform currently operates {n} study groups, numbered from 1 to {n}. Due to differences in learning habits, some groups have not established interaction links with any other groups, becoming completely "independent groups" (these isolated groups form an unknown set S that remains fixed during the analysis).

The analysis is conducted in teaching rounds (round number r=1,2,3,...). In each round, the platform issues a global teaching guidance mode L_r, which can be type A (Inquiry Mode) or B (Lecture Mode). The guidance mode follows this pattern:
- The guidance modes in adjacent rounds are completely opposite, i.e., round r+1's mode is the opposite of round r's.
- The initial mode L_1 in round 1 is unknown.

In round r, each group v displays a visible discussion activity label, determined solely by "whether group v is an independent group" and the current round's guidance mode L_r:
- If group v is an independent group (belongs to S), its activity strictly follows the platform's guidance mode due to zero external interference, making its label L_r.
- If group v has interactive connections (does not belong to S), influenced by the group complementary effect, its activity performance will invert, making its label the opposite of L_r.

The activity labels contain no group social topology information beyond the above rules.

You can repeatedly initiate the following three types of queries in each round (unlimited times per round), and the system will answer truthfully:

1. Single Activity Query: Query the current activity label of group i. Returns "A" or "B".
2. Subset High-Activity Statistic: Given a group subset U, count how many groups have the activity label A. Returns an integer.
3. Co-Activity Comparison: Ask whether group i and group j have the same activity label. Returns "Yes" or "No".

Note:
- You cannot ask about follow relationships, interaction frequencies, or other social topological information among groups.
- You cannot request the system to retroactively answer queries from previous rounds.
- You cannot modify platform configurations or group states.

When you have collected enough information, you can submit the final evaluation report. Your goal is to accurately identify all independent groups. If the answer is incorrect, the format is invalid, or the number of interaction rounds is less than 2, the analysis task fails.

Each query must contain only one tag. Please use the following XML format:

- Single Activity Query (e.g., querying group 5):
<query_node>5</query_node>

- Subset High-Activity Statistic (e.g., counting groups with label A among groups 1,3,5):
<query_count>1,3,5</query_count>

- Co-Activity Comparison (e.g., comparing group 2 and group 4):
<query_compare>2,4</query_compare>

- Next Round (finish current round queries, and the platform issues the next round's guidance mode):
<next_round></next_round>

When submitting the final evaluation report, list all independent group IDs (comma-separated, order does not matter) using this format:
<answer>1,3,5</answer>

If you believe there are no independent groups, submit an empty set:
<answer></answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“车间数控设备脱机排查系统”。

本生产线包含 {n} 台数控机床，编号为 1 到 {n}。由于网络故障，部分机床未连入车间局域网，处于完全的“脱机状态”（这些物理孤立设备构成未知集合 S，该集合在排查期间固定不变）。

排查作业按调制周期进行（周期编号 r=1,2,3,...）。每个周期中央调度系统会全网广播一个电源调制信号 L_r，信号频段为 A（高频信号）或 B（低频信号）。信号广播存在以下规律：
- 相邻周期的调制信号互为相反，即第 r+1 周期的信号与第 r 周期相反
- 第 1 周期的初始信号 L_1 未知

在第 r 周期中，每台机床 v 都会输出一个可见的电平状态标签，该标签仅由“机床 v 是否为脱机设备”和当前周期的调制信号 L_r 决定：
- 若机床 v 是脱机设备（属于 S），因无法获取局域网的降噪补偿协议，其输出端直接反馈环境感应的原始信号，标签为 L_r
- 若机床 v 已连入局域网（不属于 S），其相变器会通过网络联动处理信号，导致输出电平状态反相，标签为 L_r 的相反值

电平标签不包含除上述规则外的任何局域网拓扑结构信息。

你可以在每一周期中反复发起以下三类查询（每周期次数不限），系统会如实返回：

1. 单机电平查询：查询机床 i 的当前电平状态标签。返回“A”或“B”。
2. 区域电平计数：给定一个机床子集 U，统计其中电平标签为 A 的机床台数。返回一个整数。
3. 同频比对查询：询问机床 i 和机床 j 的电平标签是否相同。返回“是”或“否”。

注意：
- 你不能询问网络布线、机床通信节点等拓扑信息
- 你不能请求系统补答历史周期的查询
- 你不能修改调度参数或机床物理状态

当你收集到足够信息后，可以提交脱机设备清单。你的目标是准确识别出所有处于脱机状态的机床。若答案错误、格式不符或交互轮数少于 2 轮，排查任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单机电平查询（例如查询机床 5）：
<query_node>5</query_node>

- 区域电平计数（例如统计机床 1,3,5 中标签为 A 的个数）：
<query_count>1,3,5</query_count>

- 同频比对查询（例如比较机床 2 和机床 4）：
<query_compare>2,4</query_compare>

- 进入下一周期（当前周期查询结束，系统广播新一周期信号）：
<next_round></next_round>

提交脱机设备清单时，列出所有脱机机床编号（用逗号隔开，顺序不限），格式如下：
<answer>1,3,5</answer>

如果你认为不存在脱机设备，提交空集：
<answer></answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Workshop CNC Equipment Offline Detection System".

This production line involves {n} CNC machines, numbered from 1 to {n}. Due to network failures, some machines are not connected to the workshop's local area network (LAN), placing them in a completely "offline state" (these physically isolated devices form an unknown set S that remains fixed during the detection).

The detection operation is conducted in modulation periods (period number r=1,2,3,...). In each period, the central scheduling system broadcasts a power modulation signal L_r across the network, which is either band A (High-Frequency Signal) or band B (Low-Frequency Signal). The signal broadcasting follows this pattern:
- Modulation signals in adjacent periods are completely opposite, i.e., period r+1's signal is the opposite of period r's.
- The initial signal L_1 in period 1 is unknown.

In period r, each machine v outputs a visible level state label, determined solely by "whether machine v is an offline device" and the current period's modulation signal L_r:
- If machine v is an offline device (belongs to S), it cannot access the LAN's noise reduction compensation protocol, so its output directly reflects the raw environmentally induced signal, making its label L_r.
- If machine v is connected to the LAN (does not belong to S), its phase converter processes the signal through network linkage, causing its output level state to invert, making its label the opposite of L_r.

The level labels contain no LAN topology structure information beyond the above rules.

You can repeatedly initiate the following three types of queries in each period (unlimited times per period), and the system will answer truthfully:

1. Single Machine Level Query: Query the current level state label of machine i. Returns "A" or "B".
2. Regional Level Count: Given a machine subset U, count how many machines have the level label A. Returns an integer.
3. Homogeneous Frequency Comparison Query: Ask whether machine i and machine j have the same level label. Returns "Yes" or "No".

Note:
- You cannot ask about network wiring, machine communication nodes, or other topological information.
- You cannot request the system to retroactively answer queries from previous periods.
- You cannot modify scheduling parameters or the physical states of the machines.

When you have collected enough information, you can submit the offline equipment inventory. Your goal is to accurately identify all machines in an offline state. If the answer is incorrect, the format is invalid, or the number of interaction rounds is less than 2, the detection task fails.

Each query must contain only one tag. Please use the following XML format:

- Single Machine Level Query (e.g., querying machine 5):
<query_node>5</query_node>

- Regional Level Count (e.g., counting machines with label A among machines 1,3,5):
<query_count>1,3,5</query_count>

- Homogeneous Frequency Comparison Query (e.g., comparing machine 2 and machine 4):
<query_compare>2,4</query_compare>

- Next Period (finish current period queries, and the system broadcasts the next period's signal):
<next_round></next_round>

When submitting the offline equipment inventory, list all offline machine IDs (comma-separated, order does not matter) using this format:
<answer>1,3,5</answer>

If you believe there are no offline machines, submit an empty set:
<answer></answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法资金流向审计追踪系统”。

本宗大型商业纠纷案包含 {n} 个涉案账户，编号为 1 到 {n}。由于洗钱网络的复杂性，部分账户属于完全未与其他涉案账户发生资金往来的“孤立账户”（这些干净账户构成未知集合 S，该集合在审计期间固定不变）。

审计程序按追踪轮次进行（轮次编号 r=1,2,3,...）。每一轮司法系统会注入一种全局追踪探针 L_r，探针类型为 A（正向追踪探针）或 B（逆向追踪探针）。探针注入存在以下规律：
- 相邻轮次的探针类型互为相反，即第 r+1 轮的探针与第 r 轮相反
- 第 1 轮的初始探针 L_1 未知

在第 r 轮中，每个账户 v 都会返回一个可见的审计回执特征码标签，该标签仅由“账户 v 是否为孤立账户”和当前轮的探针类型 L_r 决定：
- 若账户 v 是孤立账户（属于 S），因无资金往来数据混淆，其原样返回探针特征，标签为 L_r
- 若账户 v 存在资金往来（不属于 S），受非法混币协议干扰，其回执特征码会发生逻辑取反，标签为 L_r 的相反值

回执标签不包含除上述规则外的任何转账网络拓扑信息。

你可以在每一轮中反复发起以下三类查询（每轮次数不限），系统会如实返回：

1. 单点特征查询：查询账户 i 的当前回执特征码标签。返回“A”或“B”。
2. 子集特征统计：给定一个账户子集 U，统计其中回执标签为 A 的账户个数。返回一个整数。
3. 同码比对查询：询问账户 i 和账户 j 的回执标签是否相同。返回“是”或“否”。

注意：
- 你不能询问转账金额、关联节点等资金网络拓扑信息
- 你不能请求系统补答历史轮次的查询
- 你不能修改探针参数或账户查封状态

当你收集到足够信息后，可以提交孤立账户清单。你的目标是准确识别出所有未产生资金往来的孤立账户。若答案错误、格式不符或交互轮数少于 2 轮，审计任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单点特征查询（例如查询账户 5）：
<query_node>5</query_node>

- 子集特征统计（例如统计账户 1,3,5 中标签为 A 的个数）：
<query_count>1,3,5</query_count>

- 同码比对查询（例如比较账户 2 和账户 4）：
<query_compare>2,4</query_compare>

- 进入下一轮（当前轮查询结束，系统注入新一轮追踪探针）：
<next_round></next_round>

提交孤立账户清单时，列出所有孤立账户编号（用逗号隔开，顺序不限），格式如下：
<answer>1,3,5</answer>

如果你认为不存在孤立账户，提交空集：
<answer></answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Fund Flow Audit Tracking System".

This massive commercial dispute case involves {n} implicated accounts, numbered from 1 to {n}. Due to the complexity of the money laundering network, some accounts are entirely "isolated accounts" that have had no financial transactions with any other implicated accounts (these clean accounts form an unknown set S that remains fixed during the audit).

The audit procedure is conducted in tracking rounds (round number r=1,2,3,...). In each round, the judicial system injects a global tracking probe L_r, which is either type A (Forward Tracking Probe) or B (Reverse Tracking Probe). The probe injection follows this pattern:
- The probe types in adjacent rounds are completely opposite, i.e., round r+1's probe is the opposite of round r's.
- The initial probe L_1 in round 1 is unknown.

In round r, each account v returns a visible audit receipt characteristic code label, determined solely by "whether account v is an isolated account" and the current round's probe type L_r:
- If account v is an isolated account (belongs to S), it returns the raw probe characteristic intact due to the absence of financial transaction data obfuscation, making its label L_r.
- If account v has financial transactions (does not belong to S), intercepted by illegal coin-mixing protocols, its receipt characteristic code undergoes logical negation, making its label the opposite of L_r.

The receipt labels contain no transaction network topology information beyond the above rules.

You can repeatedly initiate the following three types of queries in each round (unlimited times per round), and the system will answer truthfully:

1. Single Characteristic Query: Query the current receipt characteristic code label of account i. Returns "A" or "B".
2. Subset Characteristic Statistic: Given an account subset U, count how many accounts have the receipt label A. Returns an integer.
3. Homogeneous Code Comparison Query: Ask whether account i and account j have the same receipt label. Returns "Yes" or "No".

Note:
- You cannot ask about transaction amounts, associated nodes, or other fund network topological information.
- You cannot request the system to retroactively answer queries from previous rounds.
- You cannot modify probe parameters or the seizure status of the accounts.

When you have collected enough information, you can submit the isolated account inventory. Your goal is to accurately identify all isolated accounts with no financial transactions. If the answer is incorrect, the format is invalid, or the number of interaction rounds is less than 2, the audit task fails.

Each query must contain only one tag. Please use the following XML format:

- Single Characteristic Query (e.g., querying account 5):
<query_node>5</query_node>

- Subset Characteristic Statistic (e.g., counting accounts with label A among accounts 1,3,5):
<query_count>1,3,5</query_count>

- Homogeneous Code Comparison Query (e.g., comparing account 2 and account 4):
<query_compare>2,4</query_compare>

- Next Round (finish current round queries, and the system injects the next round's tracking probe):
<next_round></next_round>

When submitting the isolated account inventory, list all isolated account IDs (comma-separated, order does not matter) using this format:
<answer>1,3,5</answer>

If you believe there are no isolated accounts, submit an empty set:
<answer></answer>
"""

    tags = ["answer", "query_node", "query_count", "query_compare", "next_round"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "degree_zero_nodes": [1, 5],
                "seed": 42,
            },
            2: {
                "n": 7,
                "degree_zero_nodes": [2],
                "seed": 123,
            },
            3: {
                "n": 8,
                "degree_zero_nodes": [1, 4, 8],
                "seed": 256,
            },
            4: {
                "n": 10,
                "degree_zero_nodes": [3, 7],
                "seed": 789,
            },
            5: {
                "n": 12,
                "degree_zero_nodes": [],
                "seed": 1024,
            },
        },
        "en": {
            1: {
                "n": 5,
                "degree_zero_nodes": [1, 5],
                "seed": 42,
            },
            2: {
                "n": 7,
                "degree_zero_nodes": [2],
                "seed": 123,
            },
            3: {
                "n": 8,
                "degree_zero_nodes": [1, 4, 8],
                "seed": 256,
            },
            4: {
                "n": 10,
                "degree_zero_nodes": [3, 7],
                "seed": 789,
            },
            5: {
                "n": 12,
                "degree_zero_nodes": [],
                "seed": 1024,
            },
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
        self._game_info["n"] = cfg["n"]
        
        self.degree_zero_nodes = set(cfg["degree_zero_nodes"])
        
        rng = random.Random(cfg["seed"])
        self.current_round = 1
        self.global_baseline = rng.choice(["A", "B"])
        
        self.all_nodes = set(range(1, cfg["n"] + 1))

    def _get_node_label(self, node_id):
        if node_id in self.degree_zero_nodes:
            return self.global_baseline
        else:
            return "B" if self.global_baseline == "A" else "A"

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if not raw_ans:
            submitted_nodes = set()
        else:
            try:
                submitted_nodes = set(int(x.strip()) for x in raw_ans.split(",") if x.strip())
            except Exception:
                return False
        
        return submitted_nodes == self.degree_zero_nodes

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_range = "错误：节点编号超出范围。"
            error_format = "错误：格式无效。"
            next_round_msg = "已进入第 {round} 轮。"
        else:
            yes_res, no_res = "Yes", "No"
            error_range = "Error: Node ID out of range."
            error_format = "Error: Invalid format."
            next_round_msg = "Entered round {round}."

        if "next_round" in parsed_info:
            self.current_round += 1
            self.global_baseline = "B" if self.global_baseline == "A" else "A"
            return next_round_msg.format(round=self.current_round)

        elif "query_node" in parsed_info:
            try:
                node_id = int(parsed_info["query_node"].strip())
                if node_id not in self.all_nodes:
                    return error_range
                label = self._get_node_label(node_id)
                return label
            except:
                return error_format

        elif "query_count" in parsed_info:
            try:
                raw = parsed_info["query_count"].strip()
                if not raw:
                    return "0"
                node_ids = [int(x.strip()) for x in raw.split(",") if x.strip()]
                if not all(nid in self.all_nodes for nid in node_ids):
                    return error_range
                count = sum(1 for nid in node_ids if self._get_node_label(nid) == "A")
                return str(count)
            except:
                return error_format

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                node1, node2 = int(parts[0]), int(parts[1])
                if node1 not in self.all_nodes or node2 not in self.all_nodes:
                    return error_range
                label1 = self._get_node_label(node1)
                label2 = self._get_node_label(node2)
                return yes_res if label1 == label2 else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct == "A":
            return "B"
        elif correct == "B":
            return "A"
        
        if correct in ("Yes", "No"):
            return "No" if correct == "Yes" else "Yes"
        if correct in ("是", "否"):
            return "否" if correct == "是" else "是"
        
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass
        
        return correct + " [ERROR]"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"

        original_round = self.current_round
        original_baseline = self.global_baseline

        for round_idx in range(2):
            node_labels = {i: self._get_node_label(i) for i in range(1, n + 1)}

            for i in range(1, n + 1):
                queries.append({
                    "query": f"<query_node>{i}</query_node>",
                    "answer": node_labels[i]
                })

            for i in range(1, n + 1):
                for j in range(i + 1, n + 1):
                    is_same = (node_labels[i] == node_labels[j])
                    queries.append({
                        "query": f"<query_compare>{i},{j}</query_compare>",
                        "answer": yes_res if is_same else no_res
                    })

            all_nodes_str = ",".join(str(i) for i in range(1, n + 1))
            count_a = sum(1 for label in node_labels.values() if label == "A")
            queries.append({
                "query": f"<query_count>{all_nodes_str}</query_count>",
                "answer": str(count_a)
            })

            if round_idx == 0:
                self.current_round += 1
                self.global_baseline = "B" if self.global_baseline == "A" else "A"
                if lang == "zh":
                    msg = f"已进入第 {self.current_round} 轮。"
                else:
                    msg = f"Entered round {self.current_round}."
                queries.append({
                    "query": "<next_round></next_round>",
                    "answer": msg
                })

        self.current_round = original_round
        self.global_baseline = original_baseline

        return queries