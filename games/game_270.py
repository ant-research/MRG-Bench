from .base import Game
import random
import itertools

class HiddenPredicateGraphGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏谓词图推理"游戏，规则如下：

游戏设定了一个带权无向图 G，包含 {num_vertices} 个顶点和 {num_edges} 条边。每条边都有一个整数权重。图的结构和所有边的权重都是公开的：

{graph_info}

存在一个隐藏的谓词 P，它将任意整数映射为 True 或 False。该谓词在整个游戏过程中保持一致，仅依赖于输入的整数值本身。

你的目标是：推断出图中有多少条边的权重满足谓词 P（即有多少条边 e 使得 P(w(e)) = True）。

你可以通过以下三种查询方式收集信息（注意每种查询都有次数限制）：

1. 单边判定查询（至多 {max_single} 次）：
   询问某条边是否满足谓词。回答 True 或 False。

2. 子集计数查询（至多 {max_subset} 次，每次子集大小不超过 {max_subset_size} 条边）：
   询问给定的一组边中，有多少条边满足谓词。回答一个整数。

3. 假设权重查询（至多 {max_hypo} 次）：
   询问如果某条边的权重改为某个假设值，该假设权重是否满足谓词。回答 True 或 False。
   注意：此查询不会改变图中边的真实权重，仅用于测试谓词对不同权重值的判定。

当你收集到足够信息后，请提交最终答案。若答案错误、格式不符或超出任一查询次数限制，游戏失败。

每次只能进行一种查询。请使用以下 XML 格式：

- 单边判定查询（例如查询边 1）：
<query_single>1</query_single>

- 子集计数查询（例如查询边 1,3,5）：
<query_subset>1,3,5</query_subset>

- 假设权重查询（例如查询边 2 的权重假设为 10）：
<query_hypothetical>2,10</query_hypothetical>

提交最终答案时，请给出满足谓词的边的总数，格式如下：

<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Predicate Graph Reasoning" game. Here are the rules:

The game is set on a weighted undirected graph G with {num_vertices} vertices and {num_edges} edges. Each edge has an integer weight. The graph structure and all edge weights are public:

{graph_info}

There exists a hidden predicate P that maps any integer to True or False. This predicate remains consistent throughout the game and depends only on the input integer value itself.

Your goal is: Determine how many edges in the graph have weights that satisfy predicate P (i.e., how many edges e satisfy P(w(e)) = True).

You can gather information through three types of queries (note that each query type has a usage limit):

1. Single Edge Query (at most {max_single} times):
   Ask whether a specific edge satisfies the predicate. Answer is True or False.

2. Subset Count Query (at most {max_subset} times, each subset size at most {max_subset_size} edges):
   Ask how many edges in a given subset satisfy the predicate. Answer is an integer.

3. Hypothetical Weight Query (at most {max_hypo} times):
   Ask whether a hypothetical weight would satisfy the predicate if assigned to a specific edge. Answer is True or False.
   Note: This query does not change the actual edge weight; it only tests the predicate on different weight values.

When you have gathered enough information, submit your final answer. If the answer is wrong, the format is invalid, or any query limit is exceeded, the game fails.

Only one query type per turn. Use the following XML format:

- Single Edge Query (e.g., query edge 1):
<query_single>1</query_single>

- Subset Count Query (e.g., query edges 1,3,5):
<query_subset>1,3,5</query_subset>

- Hypothetical Weight Query (e.g., query edge 2 with hypothetical weight 10):
<query_hypothetical>2,10</query_hypothetical>

When submitting the final answer, provide the total count of edges satisfying the predicate:

<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用交通路网“隐藏风险研判”推演系统。

系统导入了一个城市交通网络结构图 G，包含 {num_vertices} 个路口（顶点）和 {num_edges} 条路段（边）。每条路段记录了实时的拥堵指数（整数权重）。路网结构和拥堵指数是公开的：

{graph_info}

系统中存在一个未知的安全评估规则 P，它将任意拥堵指数映射为 True（高风险需限行）或 False（安全畅通）。该评估规则在研判过程中保持一致，仅依赖于输入的拥堵指数本身。

你的目标是：推断出路网中有多少条路段的拥堵指数达到了高风险限行标准（即有多少条路段 e 使得 P(w(e)) = True）。

你可以通过以下三种指令进行勘测（注意系统资源限制）：

1. 单一路段探测（至多 {max_single} 次）：
   询问某特定路段是否触发限行规则。系统返回 True 或 False。

2. 区域路段群查（至多 {max_subset} 次，每次不超过 {max_subset_size} 条路段）：
   询问给定的一组路段中，共有多少条触发了限行规则。系统返回一个整数。

3. 流量演变沙盘（至多 {max_hypo} 次）：
   询问如果某条路段的拥堵指数突变为某个假设值，该假设值是否会触发限行规则。系统返回 True 或 False。
   注意：此操作不会改变真实路网的拥堵情况，仅用于反推系统的风险判定阈值。

勘测完成后，请提交最终的高风险路段总数。若研判错误、格式不符或超出查询次数限制，系统将判定任务失败。

每次只能执行一种查询。请使用以下 XML 格式：

- 单一路段探测（例如探测路段 1）：
<query_single>1</query_single>

- 区域路段群查（例如群查路段 1,3,5）：
<query_subset>1,3,5</query_subset>

- 流量演变沙盘（例如假设路段 2 的拥堵指数变为 10）：
<query_hypothetical>2,10</query_hypothetical>

提交最终答案时，请给出高风险限行路段的总数：

<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Traffic Network "Hidden Risk Assessment" Simulation System.

The system has loaded a city traffic network graph G with {num_vertices} intersections (vertices) and {num_edges} road segments (edges). Each segment has a real-time congestion index (integer weight). The network structure and congestion indices are public:

{graph_info}

There exists an unknown safety evaluation rule P that maps any congestion index to True (high risk, requires traffic restriction) or False (safe and clear). This rule remains consistent during the assessment and depends solely on the congestion index value.

Your goal is: Determine how many road segments in the network meet the high-risk restriction criteria (i.e., how many edges e satisfy P(w(e)) = True).

You can gather information through three types of queries (note the system resource limits):

1. Single Segment Probe (at most {max_single} times):
   Ask whether a specific road segment triggers the restriction rule. The system returns True or False.

2. Regional Segment Scan (at most {max_subset} times, each subset size at most {max_subset_size} segments):
   Ask how many segments in a given subset trigger the restriction rule. The system returns an integer.

3. Traffic Evolution Sandbox (at most {max_hypo} times):
   Ask whether a hypothetical congestion index would trigger the restriction rule if assigned to a specific segment. The system returns True or False.
   Note: This query does not change the actual congestion indices; it is only used to reverse-engineer the risk threshold.

When your assessment is complete, submit the total count of high-risk segments. If the assessment is wrong, the format is invalid, or any query limit is exceeded, the task fails.

Only one query type per turn. Use the following XML format:

- Single Segment Probe (e.g., probe segment 1):
<query_single>1</query_single>

- Regional Segment Scan (e.g., scan segments 1,3,5):
<query_subset>1,3,5</query_subset>

- Traffic Evolution Sandbox (e.g., hypothesize segment 2's index as 10):
<query_hypothetical>2,10</query_hypothetical>

When submitting the final answer, provide the total count of high-risk road segments:

<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用传染病学“高危接触网络”溯源系统。

系统构建了一个患者接触史网络图 G，包含 {num_vertices} 名患者（顶点）和 {num_edges} 条接触轨迹（边）。每条轨迹记录了两人间的接触时长（整数权重，单位：分钟）。网络结构和所有接触时长数据均已公开：

{graph_info}

病理模型中存在一个隐藏的感染判定规则 P，它将任意接触时长映射为 True（高危感染路径）或 False（低风险接触）。该规则在整个溯源过程中保持一致，仅受接触时长本身的数值影响。

你的目标是：推断出当前接触网络中有多少条轨迹被判定为高危感染路径（即有多少条轨迹 e 使得 P(w(e)) = True）。

你可以通过以下三种分析手段进行排查（注意计算资源配额）：

1. 单一轨迹流调（至多 {max_single} 次）：
   询问某条特定接触轨迹是否为高危感染路径。系统返回 True 或 False。

2. 接触史批量筛查（至多 {max_subset} 次，每次不超过 {max_subset_size} 条轨迹）：
   询问给定的一组轨迹中，共有多少条被判定为高危感染路径。系统返回一个整数。

3. 变异推演沙盘（至多 {max_hypo} 次）：
   询问如果某条轨迹的接触时长假设为某个数值，该数值是否会触发高危感染判定。系统返回 True 或 False。
   注意：此操作不会修改真实的流行病学档案，仅用于推导病毒的高危传播阈值。

排查完毕后，请提交网络中实际的高危感染路径总数。若溯源错误、指令格式不符或超出分析配额，系统将强制重置。

每次只能执行一种分析手段。请使用以下 XML 格式：

- 单一轨迹流调（例如流调轨迹 1）：
<query_single>1</query_single>

- 接触史批量筛查（例如筛查轨迹 1,3,5）：
<query_subset>1,3,5</query_subset>

- 变异推演沙盘（例如假设轨迹 2 的接触时长变为 10 分钟）：
<query_hypothetical>2,10</query_hypothetical>

提交最终答案时，请给出高危感染路径的总条数：

<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Epidemiological "High-Risk Contact Network" Tracing System.

The system has generated a patient contact history graph G with {num_vertices} patients (vertices) and {num_edges} contact trajectories (edges). Each trajectory records the exposure duration (integer weight, in minutes) between two individuals. The network structure and all duration data are public:

{graph_info}

There exists a hidden pathological infection rule P that maps any exposure duration to True (high-risk infection path) or False (low-risk contact). This rule remains strictly consistent throughout the tracing process and is influenced solely by the duration value.

Your goal is: Deduce how many trajectories in the current network are classified as high-risk infection paths (i.e., how many edges e satisfy P(w(e)) = True).

You may conduct your investigation using three analytical tools (mind your computing quotas):

1. Single Trajectory Test (at most {max_single} times):
   Ask whether a specific contact trajectory is a high-risk infection path. Returns True or False.

2. Batch Contact Screening (at most {max_subset} times, up to {max_subset_size} trajectories per batch):
   Ask how many trajectories within a given subset are classified as high-risk infection paths. Returns an integer.

3. Mutation Simulation Sandbox (at most {max_hypo} times):
   Ask whether a hypothetical exposure duration would trigger the high-risk infection criterion if applied to a specific trajectory. Returns True or False.
   Note: This does not alter actual epidemiological records; it is used only to reverse-engineer the transmission threshold.

Upon completing your investigation, submit the actual total count of high-risk infection paths. Task fails if the deduction is wrong, the format is invalid, or the quota is exceeded.

Only one query type per turn. Use the following XML format:

- Single Trajectory Test (e.g., test trajectory 1):
<query_single>1</query_single>

- Batch Contact Screening (e.g., screen trajectories 1,3,5):
<query_subset>1,3,5</query_subset>

- Mutation Simulation Sandbox (e.g., hypothesize trajectory 2 with duration 10):
<query_hypothetical>2,10</query_hypothetical>

When submitting the final answer, provide the total count of high-risk infection paths:

<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用智慧教育“核心学习路径”挖掘引擎。

引擎载入了一个学科的知识点关联图谱 G，包含 {num_vertices} 个知识点（顶点）和 {num_edges} 条知识关联（边）。每条知识关联都拥有一个教育学层面的关联度评分（整数权重）。图谱结构和所有评分信息均是对外可见的：

{graph_info}

教研模型中内嵌了一个未知的判定标准 P，它将任意关联度评分映射为 True（确认为核心学习路径）或 False（仅为辅助拓展路径）。该标准在单次分析过程中保持恒定，仅取决于关联度评分的数值。

你的任务是：挖掘出当前图谱中有多少条关联真正符合“核心学习路径”的判定标准（即有多少条关联 e 使得 P(w(e)) = True）。

你可以运用以下三种教研工具进行挖掘（注意工具的使用频次受限）：

1. 单一关联评估（至多 {max_single} 次）：
   询问某条特定的知识关联是否被视为核心学习路径。引擎返回 True 或 False。

2. 路径批量统计（至多 {max_subset} 次，每次抽样不超过 {max_subset_size} 条关联）：
   询问给出的一组知识关联中，有多少条属于核心学习路径。引擎返回一个整数。

3. 教学假设推演（至多 {max_hypo} 次）：
   询问如果将某条知识关联的评分调整为某个假设值，该评分是否会使其成为核心学习路径。引擎返回 True 或 False。
   注意：此操作旨在试探底层教研逻辑的阈值，不会真正篡改现有的图谱关联评分。

收集到充分的教研数据后，请提交图谱中实际存在的核心学习路径总数。如若计算错误、反馈格式不合规或耗尽工具频次，本次挖掘任务即告失败。

每次只能调用一种教研工具。请使用以下 XML 格式：

- 单一关联评估（例如评估关联 1）：
<query_single>1</query_single>

- 路径批量统计（例如统计关联 1,3,5）：
<query_subset>1,3,5</query_subset>

- 教学假设推演（例如假设关联 2 的评分设定为 10）：
<query_hypothetical>2,10</query_hypothetical>

提交最终答案时，请给出核心学习路径的总条数：

<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Smart Education "Core Learning Path" Discovery Engine.

The engine has loaded a knowledge association graph G for a given subject, containing {num_vertices} knowledge nodes (vertices) and {num_edges} knowledge associations (edges). Each association possesses a pedagogical relevance score (integer weight). The graph structure and all scores are fully visible:

{graph_info}

Embedded within the pedagogical model is an unknown evaluation criterion P that maps any relevance score to True (confirmed as a core learning path) or False (supplementary path). This criterion remains constant during the analysis and relies solely on the numerical value of the relevance score.

Your task is: Discover how many associations in the current graph actually meet the "core learning path" criteria (i.e., how many edges e satisfy P(w(e)) = True).

You may utilize three pedagogical tools for discovery (subject to usage limits):

1. Single Association Evaluation (at most {max_single} times):
   Ask whether a specific knowledge association is considered a core learning path. The engine returns True or False.

2. Batch Path Statistics (at most {max_subset} times, sampling up to {max_subset_size} associations at once):
   Ask how many associations within a provided subset qualify as core learning paths. The engine returns an integer.

3. Pedagogical Assumption Query (at most {max_hypo} times):
   Ask whether adjusting an association's score to a hypothetical value would qualify it as a core learning path. The engine returns True or False.
   Note: This query is intended to probe the underlying pedagogical threshold and will not alter the actual graph scores.

Once sufficient data has been collected, submit the actual total count of core learning paths. The discovery task fails if your calculation is incorrect, the format is invalid, or tool usage limits are exceeded.

Only one pedagogical tool per turn. Use the following XML format:

- Single Association Evaluation (e.g., evaluate association 1):
<query_single>1</query_single>

- Batch Path Statistics (e.g., compute for associations 1,3,5):
<query_subset>1,3,5</query_subset>

- Pedagogical Assumption Query (e.g., hypothesize association 2 with a score of 10):
<query_hypothetical>2,10</query_hypothetical>

When submitting the final answer, provide the total count of core learning paths:

<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用智能制造“产能瓶颈排查”系统。

系统构建了一条复杂生产线的工序流转图 G，包含 {num_vertices} 个工序站点（顶点）和 {num_edges} 条流转环节（边）。每个流转环节都记录了平均流转耗时（整数权重，单位：秒）。当前的流水线结构与全部耗时数据如下：

{graph_info}

系统的工艺分析模块中预设了一个隐藏判定条件 P，能够将任意流转耗时映射为 True（确认为产能瓶颈环节）或 False（流转正常）。该条件在整机排查期间绝对一致，且仅基于耗时数值本身进行判定。

你的目标是：排查出当前整条生产线中，究竟有多少条流转环节构成了真实的“产能瓶颈”（即有多少条环节 e 使得 P(w(e)) = True）。

系统为你提供了三种设备自检指令（请留意安全调用次数上限）：

1. 单一环节测试（至多 {max_single} 次）：
   询问某条特定的流转环节是否构成了产能瓶颈。系统返回 True 或 False。

2. 区域批量检阅（至多 {max_subset} 次，每次抽检不超过 {max_subset_size} 条环节）：
   询问在指定的一组流转环节中，总共有多少条属于产能瓶颈。系统返回一个整数。

3. 工艺改进沙盘（至多 {max_hypo} 次）：
   询问如果某环节的耗时通过技术改造变更为某个假设值，该状态是否仍被系统判定为瓶颈。系统返回 True 或 False。
   注意：此操作纯属虚拟仿真，不干预物理车间的实际参数，仅用于测算瓶颈的临界时间。

完成全面排查后，请输出生产线上实际的产能瓶颈环节总数。一旦最终上报数据有误、通信格式非法或调用次数超载，本次系统自检宣告失败。

每次只能输入一种自检指令。请使用以下 XML 格式：

- 单一环节测试（例如测试环节 1）：
<query_single>1</query_single>

- 区域批量检阅（例如检阅环节 1,3,5）：
<query_subset>1,3,5</query_subset>

- 工艺改进沙盘（例如假设环节 2 的流转耗时优化至 10 秒）：
<query_hypothetical>2,10</query_hypothetical>

提交最终答案时，请给出产能瓶颈环节的总条数：

<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart Manufacturing "Bottleneck Identification" System.

The system has generated a routing graph G for a complex production line, comprising {num_vertices} workstations (vertices) and {num_edges} routing steps (edges). Each routing step records the average processing time (integer weight, in seconds). The current line structure and all processing times are mapped out below:

{graph_info}

A hidden evaluation condition P is preset within the process analysis module. It maps any processing time to True (confirmed as a capacity bottleneck) or False (normal flow). This condition remains strictly consistent throughout the inspection and relies solely on the time value.

Your objective is: Identify exactly how many routing steps across the production line constitute actual "capacity bottlenecks" (i.e., how many edges e satisfy P(w(e)) = True).

The system provides three diagnostic commands (please observe the safe usage limits):

1. Single Routing Test (at most {max_single} times):
   Ask whether a specific routing step constitutes a capacity bottleneck. The system returns True or False.

2. Batch Routing Inspection (at most {max_subset} times, sampling up to {max_subset_size} steps per batch):
   Ask how many steps within a specified subset are identified as bottlenecks. The system returns an integer.

3. Process Improvement Sandbox (at most {max_hypo} times):
   Ask whether a hypothetical processing time, assuming a technical upgrade, would still be classified as a bottleneck. The system returns True or False.
   Note: This is strictly a virtual simulation to calculate critical thresholds and does not interfere with the physical shop floor.

Upon completing a comprehensive inspection, report the total number of actual bottleneck steps. The system diagnostic will fail if your reported data is incorrect, the communication format is invalid, or command limits are exceeded.

Submit only one diagnostic command per turn. Use the following XML format:

- Single Routing Test (e.g., test step 1):
<query_single>1</query_single>

- Batch Routing Inspection (e.g., inspect steps 1,3,5):
<query_subset>1,3,5</query_subset>

- Process Improvement Sandbox (e.g., hypothesize step 2 optimized to 10 seconds):
<query_hypothetical>2,10</query_hypothetical>

When submitting the final answer, provide the total count of bottleneck steps:

<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎登录经侦“洗钱网络异常交易”审计平台。

平台现已锁定一个涉案资金流向图 G，包含 {num_vertices} 个涉案账户（顶点）和 {num_edges} 笔转账记录（边）。每笔转账记录均附带确切的交易金额（整数权重）。账户拓扑结构及转账金额明细已向审查员公开：

{graph_info}

审计算法库中封装了一套隐秘的洗钱判定逻辑 P，能够将任意交易金额归类为 True（洗钱嫌疑交易）或 False（合规流水）。该逻辑在整个取证环节中保持闭环一致，且判定依据仅为金额数值本身。

你的职责是：查明该资金流向图中，共有多少笔转账记录触碰了审计逻辑底线，构成了“洗钱嫌疑交易”（即有多少笔转账 e 使得 P(w(e)) = True）。

你获权使用以下三种取证探针（注意权限调用次数）：

1. 专项流水审查（至多 {max_single} 次）：
   对某笔特定转账记录发起询问，查实其是否涉嫌洗钱。平台反馈 True 或 False。

2. 账目批量调阅（至多 {max_subset} 次，每次调取不超过 {max_subset_size} 笔转账）：
   询问在指定的一组账单记录中，共有多少笔被标记为涉嫌洗钱。平台反馈一个整数。

3. 法理逻辑推演（至多 {max_hypo} 次）：
   询问若某笔账单的交易金额虚构为某一具体数值，该金额是否会触发洗钱预警。平台反馈 True 或 False。
   注意：此操作为预警模型压力测试，不会篡改金融机构的真实流水账单，仅用于摸底风控算法的红线标准。

在完成确凿的侦查后，请提交当前网络中实际的洗钱嫌疑交易总笔数。如果结案数据错误、报文格式异常或越权调用探针，本次侦查将不予立案。

每次仅限激活一枚探针。请使用以下 XML 格式：

- 专项流水审查（例如审查转账记录 1）：
<query_single>1</query_single>

- 账目批量调阅（例如调阅转账记录 1,3,5）：
<query_subset>1,3,5</query_subset>

- 法理逻辑推演（例如假设转账记录 2 的金额为 10）：
<query_hypothetical>2,10</query_hypothetical>

提交结案答案时，请给出洗钱嫌疑交易的总笔数：

<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Economic Crime "Suspicious Transaction Audit" Platform.

The platform has locked onto a targeted fund flow graph G, containing {num_vertices} involved accounts (vertices) and {num_edges} transfer records (edges). Each transfer record is accompanied by a precise transaction amount (integer weight). The account topology and detailed transfer amounts are disclosed to the auditor:

{graph_info}

Encapsulated within the audit algorithmic library is a covert money laundering identification logic P, which categorizes any transaction amount as True (suspicious money laundering activity) or False (compliant flow). This logic remains closed-loop and strictly consistent throughout the evidence collection process, based solely on the numerical transaction amount.

Your duty is: Ascertain exactly how many transfer records in this graph cross the audit threshold and constitute "suspicious money laundering activity" (i.e., how many transfers e satisfy P(w(e)) = True).

You are authorized to use three forensic probes (mind your clearance invocation limits):

1. Single Transfer Audit (at most {max_single} times):
   Query a specific transfer record to verify if it is suspected of money laundering. The platform returns True or False.

2. Batch Record Review (at most {max_subset} times, pulling up to {max_subset_size} transfers per query):
   Query a specified batch of transaction records to find out how many are flagged as suspicious. The platform returns an integer.

3. Legal Deduction Sandbox (at most {max_hypo} times):
   Query whether a hypothetical transaction amount, if forged for a transfer, would trigger a money laundering alert. The platform returns True or False.
   Note: This is a stress test for the early warning model. It does not tamper with real financial ledger records and is solely meant to trace the algorithm's red-line criteria.

After establishing conclusive evidence, submit the actual total count of suspicious money laundering transactions. The investigation will be dismissed if the closure data is incorrect, the message format is invalid, or probe privileges are exceeded.

Activate only one probe per turn. Use the following XML format:

- Single Transfer Audit (e.g., audit transfer record 1):
<query_single>1</query_single>

- Batch Record Review (e.g., review transfer records 1,3,5):
<query_subset>1,3,5</query_subset>

- Legal Deduction Sandbox (e.g., hypothesize transfer record 2 with an amount of 10):
<query_hypothetical>2,10</query_hypothetical>

When submitting your final closure answer, provide the total count of suspicious transactions:

<answer>5</answer>
"""

    tags = ["answer", "query_single", "query_subset", "query_hypothetical"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "num_vertices": 4,
                "edges": [
                    (1, 2, 5),
                    (1, 3, 8),
                    (2, 3, 3),
                    (2, 4, 12),
                    (3, 4, 7)
                ],
                "predicate_type": "threshold",
                "predicate_param": 6,
                "max_single": 10,
                "max_subset": 3,
                "max_subset_size": 8,
                "max_hypo": 12
            },
            2: {
                "num_vertices": 5,
                "edges": [
                    (1, 2, 10),
                    (1, 3, 15),
                    (2, 3, 7),
                    (2, 4, 21),
                    (3, 4, 14),
                    (3, 5, 9),
                    (4, 5, 18)
                ],
                "predicate_type": "modulo",
                "predicate_param": 3,
                "max_single": 10,
                "max_subset": 3,
                "max_subset_size": 8,
                "max_hypo": 12
            },
            3: {
                "num_vertices": 6,
                "edges": [
                    (1, 2, 4),
                    (1, 3, 11),
                    (2, 3, 8),
                    (2, 4, 15),
                    (3, 4, 6),
                    (3, 5, 13),
                    (4, 5, 9),
                    (4, 6, 7),
                    (5, 6, 12)
                ],
                "predicate_type": "range",
                "predicate_param": (7, 12),
                "max_single": 10,
                "max_subset": 3,
                "max_subset_size": 8,
                "max_hypo": 12
            },
            4: {
                "num_vertices": 7,
                "edges": [
                    (1, 2, 2),
                    (1, 3, 13),
                    (2, 3, 8),
                    (2, 4, 17),
                    (3, 4, 11),
                    (3, 5, 5),
                    (4, 5, 19),
                    (4, 6, 7),
                    (5, 6, 23),
                    (5, 7, 4),
                    (6, 7, 3)
                ],
                "predicate_type": "prime",
                "predicate_param": None,
                "max_single": 10,
                "max_subset": 3,
                "max_subset_size": 8,
                "max_hypo": 12
            },
            5: {
                "num_vertices": 8,
                "edges": [
                    (1, 2, 6),
                    (1, 3, 14),
                    (2, 3, 10),
                    (2, 4, 21),
                    (3, 4, 15),
                    (3, 5, 8),
                    (4, 5, 28),
                    (4, 6, 12),
                    (5, 6, 35),
                    (5, 7, 9),
                    (6, 7, 18),
                    (6, 8, 20),
                    (7, 8, 24)
                ],
                "predicate_type": "composite",
                "predicate_param": None,
                "max_single": 10,
                "max_subset": 3,
                "max_subset_size": 8,
                "max_hypo": 12
            }
        },
        "en": {
            1: {
                "num_vertices": 4,
                "edges": [
                    (1, 2, 5),
                    (1, 3, 8),
                    (2, 3, 3),
                    (2, 4, 12),
                    (3, 4, 7)
                ],
                "predicate_type": "threshold",
                "predicate_param": 6,
                "max_single": 10,
                "max_subset": 3,
                "max_subset_size": 8,
                "max_hypo": 12
            },
            2: {
                "num_vertices": 5,
                "edges": [
                    (1, 2, 10),
                    (1, 3, 15),
                    (2, 3, 7),
                    (2, 4, 21),
                    (3, 4, 14),
                    (3, 5, 9),
                    (4, 5, 18)
                ],
                "predicate_type": "modulo",
                "predicate_param": 3,
                "max_single": 10,
                "max_subset": 3,
                "max_subset_size": 8,
                "max_hypo": 12
            },
            3: {
                "num_vertices": 6,
                "edges": [
                    (1, 2, 4),
                    (1, 3, 11),
                    (2, 3, 8),
                    (2, 4, 15),
                    (3, 4, 6),
                    (3, 5, 13),
                    (4, 5, 9),
                    (4, 6, 7),
                    (5, 6, 12)
                ],
                "predicate_type": "range",
                "predicate_param": (7, 12),
                "max_single": 10,
                "max_subset": 3,
                "max_subset_size": 8,
                "max_hypo": 12
            },
            4: {
                "num_vertices": 7,
                "edges": [
                    (1, 2, 2),
                    (1, 3, 13),
                    (2, 3, 8),
                    (2, 4, 17),
                    (3, 4, 11),
                    (3, 5, 5),
                    (4, 5, 19),
                    (4, 6, 7),
                    (5, 6, 23),
                    (5, 7, 4),
                    (6, 7, 3)
                ],
                "predicate_type": "prime",
                "predicate_param": None,
                "max_single": 10,
                "max_subset": 3,
                "max_subset_size": 8,
                "max_hypo": 12
            },
            5: {
                "num_vertices": 8,
                "edges": [
                    (1, 2, 6),
                    (1, 3, 14),
                    (2, 3, 10),
                    (2, 4, 21),
                    (3, 4, 15),
                    (3, 5, 8),
                    (4, 5, 28),
                    (4, 6, 12),
                    (5, 6, 35),
                    (5, 7, 9),
                    (6, 7, 18),
                    (6, 8, 20),
                    (7, 8, 24)
                ],
                "predicate_type": "composite",
                "predicate_param": None,
                "max_single": 10,
                "max_subset": 3,
                "max_subset_size": 8,
                "max_hypo": 12
            }
        }
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
        
        self._game_info["num_vertices"] = cfg["num_vertices"]
        self._game_info["num_edges"] = len(cfg["edges"])
        self._game_info["max_single"] = cfg["max_single"]
        self._game_info["max_subset"] = cfg["max_subset"]
        self._game_info["max_subset_size"] = cfg["max_subset_size"]
        self._game_info["max_hypo"] = cfg["max_hypo"]
        
        self.edges = {}
        self.edge_weights = {}
        for idx, (u, v, w) in enumerate(cfg["edges"], 1):
            self.edges[idx] = (u, v, w)
            self.edge_weights[idx] = w
        
        if lang == "zh":
            graph_lines = [f"边 {idx}: 连接顶点 {u}-{v}，权重 = {w}" 
                          for idx, (u, v, w) in self.edges.items()]
        else:
            graph_lines = [f"Edge {idx}: connects vertices {u}-{v}, weight = {w}" 
                          for idx, (u, v, w) in self.edges.items()]
        self._game_info["graph_info"] = "\n".join(graph_lines)
        
        self.predicate_type = cfg["predicate_type"]
        self.predicate_param = cfg["predicate_param"]
        
        self.true_count = sum(1 for w in self.edge_weights.values() 
                             if self._evaluate_predicate(w))
        
        self.query_counts = {
            "single": 0,
            "subset": 0,
            "hypothetical": 0
        }
        
        self.max_queries = {
            "single": cfg["max_single"],
            "subset": cfg["max_subset"],
            "hypothetical": cfg["max_hypo"]
        }
        self.max_subset_size = cfg["max_subset_size"]

    def _evaluate_predicate(self, weight):
        if self.predicate_type == "threshold":
            return weight > self.predicate_param
        elif self.predicate_type == "modulo":
            return weight % self.predicate_param == 0
        elif self.predicate_type == "range":
            low, high = self.predicate_param
            return low <= weight <= high
        elif self.predicate_type == "prime":
            return self._is_prime(weight)
        elif self.predicate_type == "composite":
            return weight % 3 == 0 or weight % 5 == 0
        else:
            raise ValueError(f"Unknown predicate type: {self.predicate_type}")

    def _is_prime(self, n):
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.true_count
        except:
            return False

    def _cf_make_wrong(self, correct: str) -> str:
        if correct in ("True", "False"):
            return "False" if correct == "True" else "True"
        else:
            try:
                val = int(correct)
                return str(val + 1)
            except ValueError:
                return correct + "_wrong"

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        true_str = "True"
        false_str = "False"
        
        if "query_single" in parsed_info:
            if self.query_counts["single"] >= self.max_queries["single"]:
                raise ValueError("Single edge query limit exceeded." if lang == "en" 
                               else "单边判定查询次数已达上限。")
            
            try:
                edge_id = int(parsed_info["query_single"].strip())
                if edge_id not in self.edges:
                    raise ValueError("Invalid edge ID." if lang == "en" else "边编号无效。")
                
                self.query_counts["single"] += 1
                weight = self.edge_weights[edge_id]
                result = self._evaluate_predicate(weight)
                return true_str if result else false_str
            except ValueError:
                raise
            except Exception:
                raise ValueError("Invalid edge ID." if lang == "en" else "边编号无效。")
        
        elif "query_subset" in parsed_info:
            if self.query_counts["subset"] >= self.max_queries["subset"]:
                raise ValueError("Subset count query limit exceeded." if lang == "en"
                               else "子集计数查询次数已达上限。")
            
            try:
                edge_ids_str = parsed_info["query_subset"].strip()
                edge_ids = [int(x.strip()) for x in edge_ids_str.split(",") if x.strip()]
                
                if len(edge_ids) > self.max_subset_size:
                    raise ValueError(f"Subset size exceeds limit (max {self.max_subset_size} edges)." 
                                   if lang == "en" else f"子集大小超过限制（最多 {self.max_subset_size} 条边）。")
                
                if not all(eid in self.edges for eid in edge_ids):
                    raise ValueError("Invalid subset format or edge ID." if lang == "en"
                                   else "子集格式无效或边编号错误。")
                
                self.query_counts["subset"] += 1
                count = sum(1 for eid in edge_ids 
                           if self._evaluate_predicate(self.edge_weights[eid]))
                return str(count)
            except ValueError:
                raise
            except Exception:
                raise ValueError("Invalid subset format or edge ID." if lang == "en"
                               else "子集格式无效或边编号错误。")
        
        elif "query_hypothetical" in parsed_info:
            if self.query_counts["hypothetical"] >= self.max_queries["hypothetical"]:
                raise ValueError("Hypothetical weight query limit exceeded." if lang == "en"
                               else "假设权重查询次数已达上限。")
            
            try:
                parts = parsed_info["query_hypothetical"].strip().split(",")
                if len(parts) != 2:
                    raise ValueError("Invalid hypothetical weight query format." if lang == "en"
                                   else "假设权重查询格式无效。")
                
                edge_id = int(parts[0].strip())
                hypo_weight = int(parts[1].strip())
                
                if edge_id not in self.edges:
                    raise ValueError("Invalid edge ID." if lang == "en" else "边编号无效。")
                
                self.query_counts["hypothetical"] += 1
                result = self._evaluate_predicate(hypo_weight)
                return true_str if result else false_str
            except ValueError:
                raise
            except Exception:
                raise ValueError("Invalid hypothetical weight query format." if lang == "en"
                               else "假设权重查询格式无效。")
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        true_str = "True"
        false_str = "False"

        all_edge_ids = list(self.edges.keys())

        single_edges = all_edge_ids[:self.max_queries["single"]]
        for edge_id in single_edges:
            weight = self.edge_weights[edge_id]
            res = self._evaluate_predicate(weight)
            queries.append({
                "query": f"<query_single>{edge_id}</query_single>",
                "answer": true_str if res else false_str
            })

        subset_queries = []
        for size in range(1, min(3, self.max_subset_size + 1)):
            for subset in itertools.combinations(all_edge_ids, size):
                subset_str = ",".join(map(str, subset))
                count = sum(1 for eid in subset if self._evaluate_predicate(self.edge_weights[eid]))
                subset_queries.append({
                    "query": f"<query_subset>{subset_str}</query_subset>",
                    "answer": str(count)
                })
        if len(all_edge_ids) <= self.max_subset_size:
            subset_str = ",".join(map(str, all_edge_ids))
            count = sum(1 for eid in all_edge_ids if self._evaluate_predicate(self.edge_weights[eid]))
            subset_queries.append({
                "query": f"<query_subset>{subset_str}</query_subset>",
                "answer": str(count)
            })

        queries.extend(subset_queries[:self.max_queries["subset"]])

        hypo_queries = []
        target_edge = 1
        if target_edge in self.edges:
            for w in range(0, 41):
                res = self._evaluate_predicate(w)
                hypo_queries.append({
                    "query": f"<query_hypothetical>{target_edge},{w}</query_hypothetical>",
                    "answer": true_str if res else false_str
                })

        queries.extend(hypo_queries[:self.max_queries["hypothetical"]])

        return queries