from .base import Game
import random
import re

class TreeDistanceQueryGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树图距离查询"的推理游戏，规则如下：

游戏设定了一个未知的无向树图 T，包含 N 个顶点，编号为 1 到 N。树图是连通的且无环。我已指定一个起点 S = {start} 和一个距离阈值 K = {threshold}。

你的目标是：确定从起点 S 出发，距离小于等于 K 的顶点总数 X。这里的距离指的是两点之间唯一简单路径的边数。

初始时，你只知道起点 S = {start}，它在"已发现顶点集合"D 中。你只能对 D 中的顶点发起查询。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **邻居查询**：询问某个已发现顶点 u 的所有相邻顶点。返回一个列表，所有返回的顶点会自动加入已发现集合 D。
2. **距离查询**：询问两个已发现顶点 u 和 v 之间的距离。返回一个整数。
3. **范围判定查询**：询问某个已发现顶点 u 是否在距离起点 S 不超过 K 的范围内。返回"是"或"否"。

注意：
- 任何涉及未发现顶点的查询都是非法的，会返回"非法查询"。
- 你不能直接询问"距离 S 不超过 K 的顶点总数是多少"。

每次查询只能包含一个标签，使用以下 XML 格式：

- 邻居查询（例如查询顶点 5 的邻居）：
<query_neighbor>5</query_neighbor>

- 距离查询（例如查询顶点 1 和 3 之间的距离）：
<query_distance>1,3</query_distance>

- 范围判定查询（例如查询顶点 7 是否在范围内）：
<query_in_range>7</query_in_range>

当你收集到足够信息后，提交最终答案。答案必须包含顶点总数 X，可选地附加顶点列表作为佐证：

<answer>count=5, nodes=1,2,3,4,5</answer>

或仅提交总数：

<answer>count=5</answer>

若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Tree Distance Query" deduction game. Here are the rules:

The game is set on an unknown undirected tree graph T with N vertices, numbered from 1 to N. The tree is connected and acyclic. I have specified a starting vertex S = {start} and a distance threshold K = {threshold}.

Your goal is: determine the total number X of vertices whose distance from the starting vertex S is at most K. Distance here refers to the number of edges in the unique simple path between two vertices.

Initially, you only know the starting vertex S = {start}, which is in the "discovered vertex set" D. You can only query vertices in D.

You can repeatedly make the following three types of queries (one query per turn):

1. **Neighbor Query**: Ask for all adjacent vertices of a discovered vertex u. Returns a list, and all returned vertices are automatically added to the discovered set D.
2. **Distance Query**: Ask for the distance between two discovered vertices u and v. Returns an integer.
3. **Range Check Query**: Ask whether a discovered vertex u is within distance K from the starting vertex S. Returns "Yes" or "No".

Note:
- Any query involving undiscovered vertices is illegal and will return "Illegal query".
- You cannot directly ask "What is the total number of vertices within distance K from S".

Each query must contain only one tag, using the following XML format:

- Neighbor Query (e.g., querying neighbors of vertex 5):
<query_neighbor>5</query_neighbor>

- Distance Query (e.g., querying distance between vertices 1 and 3):
<query_distance>1,3</query_distance>

- Range Check Query (e.g., checking if vertex 7 is in range):
<query_in_range>7</query_in_range>

When you have gathered enough information, submit your final answer. The answer must include the total count X, and optionally a list of vertices as evidence:

<answer>count=5, nodes=1,2,3,4,5</answer>

Or submit only the count:

<answer>count=5</answer>

If the answer is incorrect or the format is invalid, the game fails.
"""

    contextualized_rule_zh_1 = """\
我们正在进行“城市路网应急封控”的推演，规则如下：

系统设定了一个未知的城市道路管网（无向树图 T），包含 N 个交通枢纽（编号 1 到 N），枢纽间连通且无环路。当前已确定事故核心枢纽 S = {start}，并下达了封控距离阈值 K = {threshold}。

你的目标是：确定从核心枢纽 S 出发，连通距离小于等于 K 的受影响枢纽总数 X。这里的距离指两枢纽间唯一通道所包含的路段数（边数）。

初始时，你只掌握核心枢纽 S = {start} 的情报，它处于“已知枢纽集合”D 中。你只能对 D 中的枢纽发起勘测查询。

你可以反复提出以下三类指令（每次仅限一个）：

1. **路段连通查询**（邻居查询）：询问某个已知枢纽 u 的所有直接相连枢纽。返回一个列表，返回的枢纽自动加入已知集合 D。
2. **枢纽距离查询**（距离查询）：询问两个已知枢纽 u 和 v 之间的路段数距离。返回一个整数。
3. **封控范围判定**（范围判定查询）：询问某个已知枢纽 u 是否处于距核心 S 不超过 K 的封控范围内。返回"是"或"否"。

注意：
- 任何涉及未知枢纽的指令都会被驳回并返回"非法查询"。
- 你不能直接询问"距离 S 不超过 K 的枢纽总数是多少"。

每次查询只能包含一个标签，使用以下 XML 格式：

- 邻居查询（例如查询枢纽 5 的相邻枢纽）：
<query_neighbor>5</query_neighbor>

- 距离查询（例如查询枢纽 1 和 3 之间的路段距离）：
<query_distance>1,3</query_distance>

- 范围判定查询（例如查询枢纽 7 是否在封控范围内）：
<query_in_range>7</query_in_range>

当你收集到足够信息后，提交最终评估。答案必须包含受影响枢纽总数 X，可选地附加枢纽列表作为佐证：

<answer>count=5, nodes=1,2,3,4,5</answer>

或仅提交总数：

<answer>count=5</answer>

若评估错误或格式不符，推演失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are conducting an "Urban Road Network Emergency Lockdown" simulation. Here are the rules:

The system models an unknown urban road network (undirected tree graph T) containing N traffic hubs (numbered from 1 to N). The network is connected and has no cyclic routes. The core accident hub S = {start} has been identified, and a lockdown distance threshold K = {threshold} is designated.

Your goal is: determine the total number X of affected traffic hubs whose connected distance from the core hub S is at most K. The distance here refers to the number of road segments (edges) in the unique simple path between two hubs.

Initially, you only have intelligence on the core hub S = {start}, which is in the "known hubs set" D. You can only query hubs in D.

You can repeatedly issue the following three types of queries (one query per turn):

1. **Segment Connection Query** (Neighbor Query): Ask for all directly connected hubs of a known hub u. Returns a list, and the returned hubs are automatically added to the known set D.
2. **Hub Distance Query** (Distance Query): Ask for the distance in road segments between two known hubs u and v. Returns an integer.
3. **Lockdown Range Check** (Range Check Query): Ask whether a known hub u is within the lockdown range of distance K from the core S. Returns "Yes" or "No".

Note:
- Any query involving unknown hubs will be rejected as an "Illegal query".
- You cannot directly ask "What is the total number of hubs within distance K from S".

Each query must contain only one tag, using the following XML format:

- Neighbor Query (e.g., querying adjacent hubs of hub 5):
<query_neighbor>5</query_neighbor>

- Distance Query (e.g., querying road distance between hubs 1 and 3):
<query_distance>1,3</query_distance>

- Range Check Query (e.g., checking if hub 7 is in the lockdown range):
<query_in_range>7</query_in_range>

When you have gathered enough information, submit your final evaluation. The answer must include the total count X, and optionally a list of hubs as evidence:

<answer>count=5, nodes=1,2,3,4,5</answer>

Or submit only the count:

<answer>count=5</answer>

If the assessment is incorrect or the format is invalid, the simulation fails.
"""

    contextualized_rule_zh_2 = """\
我们正在进行“流行病接触史追踪”推演，规则如下：

系统设定了一个未知的传染病传播网络（无向树图 T），包含 N 名涉疫人员（编号 1 到 N），传播链连续且无交叉感染（无环）。已确定源头病例 S = {start}，并设定最大追踪代际 K = {threshold}。

你的目标是：确定从源头病例 S 算起，传播代际小于等于 K 的高危感染者总数 X。这里的代际指的是两名人员之间最短接触链条的人数（边数）。

初始时，你只掌握源头病例 S = {start} 的信息，该人员处于“已排查名单”D 中。你只能对 D 中的人员发起流调查询。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **密接查询**（邻居查询）：询问某位已排查人员 u 的所有直接接触者。返回一个列表，名单内人员自动加入排查名单 D。
2. **传播跨度查询**（距离查询）：询问两名已排查人员 u 和 v 之间的接触代差。返回一个整数。
3. **高危判定**（范围判定查询）：询问某位已排查人员 u 是否在距源头 S 不超过 K 代的追踪范围内。返回"是"或"否"。

注意：
- 任何涉及未排查人员的查询都是非法的，会返回"非法查询"。
- 你不能直接询问"距离 S 不超过 K 代的总人数是多少"。

每次查询只能包含一个标签，使用以下 XML 格式：

- 邻居查询（例如查询人员 5 的直接密接）：
<query_neighbor>5</query_neighbor>

- 距离查询（例如查询人员 1 和 3 之间的代差）：
<query_distance>1,3</query_distance>

- 范围判定查询（例如查询人员 7 是否属于高危范围）：
<query_in_range>7</query_in_range>

当你收集到足够信息后，提交最终排查报告。答案必须包含高危总人数 X，可选地附加人员名单作为佐证：

<answer>count=5, nodes=1,2,3,4,5</answer>

或仅提交总数：

<answer>count=5</answer>

若报告错误或格式不符，推演失败。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
We are conducting an "Epidemic Contact Tracing" simulation. Here are the rules:

The system outlines an unknown infectious disease transmission network (undirected tree graph T) involving N exposed individuals (numbered 1 to N). The transmission chain is continuous with no cross-infections (acyclic). The patient zero S = {start} has been identified, and a maximum tracing generation K = {threshold} is set.

Your goal is: determine the total number X of high-risk infected individuals whose transmission generation from patient zero S is at most K. Generation here refers to the number of steps (edges) in the shortest contact chain between two individuals.

Initially, you only have the profile of patient zero S = {start}, who is in the "investigated list" D. You can only initiate epidemiological queries on individuals in D.

You can repeatedly make the following three types of queries (one query per turn):

1. **Close Contact Query** (Neighbor Query): Ask for all direct contacts of an investigated individual u. Returns a list, and those individuals are automatically added to the investigated list D.
2. **Transmission Span Query** (Distance Query): Ask for the contact generation gap between two investigated individuals u and v. Returns an integer.
3. **High-Risk Check** (Range Check Query): Ask whether an investigated individual u is within K generations of tracing range from the source S. Returns "Yes" or "No".

Note:
- Any query involving uninvestigated individuals is invalid and will return "Illegal query".
- You cannot directly ask "What is the total number of individuals within K generations from S".

Each query must contain only one tag, using the following XML format:

- Neighbor Query (e.g., querying direct contacts of individual 5):
<query_neighbor>5</query_neighbor>

- Distance Query (e.g., querying generation gap between individuals 1 and 3):
<query_distance>1,3</query_distance>

- Range Check Query (e.g., checking if individual 7 is in the high-risk range):
<query_in_range>7</query_in_range>

When you have gathered enough information, submit your final tracing report. The answer must include the total high-risk count X, and optionally a list of individuals as evidence:

<answer>count=5, nodes=1,2,3,4,5</answer>

Or submit only the count:

<answer>count=5</answer>

If the report is incorrect or the format is invalid, the simulation fails.
"""

    contextualized_rule_zh_3 = """\
我们来体验“知识图谱前置依赖分析”系统，规则如下：

系统设定了一个未知的学科知识结构（无向树图 T），包含 N 个知识模块（编号 1 到 N），知识点间存在严密的关联且无循环依赖。现指定当前核心概念 S = {start}，以及大纲要求的拓展深度 K = {threshold}。

你的目标是：确定从核心概念 S 出发，关联层级小于等于 K 的必需知识模块总数 X。这里的层级指的是两模块间唯一的推理路径跨度（边数）。

初始时，你只解锁了核心概念 S = {start}，它位于“已解析概念库”D 中。你只能对 D 中的概念发起分析。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **关联概念查询**（邻居查询）：询问某个已解析概念 u 的所有直接关联概念。返回一个列表，返回的概念自动加入解析库 D。
2. **认知跨度查询**（距离查询）：询问两个已解析概念 u 和 v 之间的推理路径跨度。返回一个整数。
3. **大纲范围判定**（范围判定查询）：询问某个已解析概念 u 是否处于距核心 S 不超过 K 的教学拓展范围内。返回"是"或"否"。

注意：
- 任何涉及未解析概念的查询都会失败并返回"非法查询"。
- 你不能直接询问"距离 S 不超过 K 的概念总数是多少"。

每次查询只能包含一个标签，使用以下 XML 格式：

- 邻居查询（例如查询概念 5 的直接关联）：
<query_neighbor>5</query_neighbor>

- 距离查询（例如查询概念 1 和 3 之间的认知跨度）：
<query_distance>1,3</query_distance>

- 范围判定查询（例如查询概念 7 是否在大纲拓展范围内）：
<query_in_range>7</query_in_range>

当你收集到足够信息后，提交最终的大纲分析。答案必须包含必需知识模块总数 X，可选地附加模块列表作为佐证：

<answer>count=5, nodes=1,2,3,4,5</answer>

或仅提交总数：

<answer>count=5</answer>

若分析错误或格式不符，任务失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's experience the "Knowledge Graph Prerequisite Analysis" system. Here are the rules:

The system constructs an unknown subject knowledge structure (undirected tree graph T) consisting of N knowledge modules (numbered 1 to N). The concepts have strict correlations and no circular dependencies. The core concept S = {start} is designated, along with an expansion depth K = {threshold} required by the syllabus.

Your goal is: determine the total number X of essential knowledge modules whose correlation level from the core concept S is at most K. The level here refers to the span of the unique reasoning path (edges) between two modules.

Initially, you have only unlocked the core concept S = {start}, which resides in the "parsed concept repository" D. You can only analyze concepts present in D.

You can repeatedly make the following three types of queries (one query per turn):

1. **Correlated Concept Query** (Neighbor Query): Ask for all directly correlated concepts of a parsed concept u. Returns a list, and the returned concepts are automatically added to the parsed repository D.
2. **Cognitive Span Query** (Distance Query): Ask for the reasoning path span between two parsed concepts u and v. Returns an integer.
3. **Syllabus Scope Check** (Range Check Query): Ask whether a parsed concept u falls within the teaching expansion scope of distance K from the core S. Returns "Yes" or "No".

Note:
- Any query involving unparsed concepts will fail and return "Illegal query".
- You cannot directly ask "What is the total number of concepts within distance K from S".

Each query must contain only one tag, using the following XML format:

- Neighbor Query (e.g., querying directly correlated concepts of concept 5):
<query_neighbor>5</query_neighbor>

- Distance Query (e.g., querying cognitive span between concepts 1 and 3):
<query_distance>1,3</query_distance>

- Range Check Query (e.g., checking if concept 7 is within the syllabus expansion scope):
<query_in_range>7</query_in_range>

When you have gathered enough information, submit your final syllabus analysis. The answer must include the total count of essential modules X, and optionally a list of modules as evidence:

<answer>count=5, nodes=1,2,3,4,5</answer>

Or submit only the count:

<answer>count=5</answer>

If the analysis is incorrect or the format is invalid, the task fails.
"""

    contextualized_rule_zh_4 = """\
我们正在进行“工业管网故障排查”模拟，规则如下：

系统设定了一个未知的供压管网系统（无向树图 T），包含 N 个阀门节点（编号 1 到 N），管线全连通且无回路。当前核心故障泵站 S = {start} 已停机，系统发出了压力波及层级警报 K = {threshold}。

你的目标是：确定从故障泵站 S 算起，受波及层级小于等于 K 的必须停机检修阀门总数 X。这里的层级指两节点间唯一管道路径所包含的管段数（边数）。

初始时，你只定位了故障泵站 S = {start}，记录于“已排查节点集”D 中。你只能对 D 中的节点进行检测。

你可以反复提出以下三类指令（每次仅限一个）：

1. **连通管段查询**（邻居查询）：询问某个已排查节点 u 沿管道直接相邻的所有阀门。返回一个列表，返回的节点自动加入排查集 D。
2. **管网距离查询**（距离查询）：询问两个已排查节点 u 和 v 之间的管段数。返回一个整数。
3. **波及范围判定**（范围判定查询）：询问某个已排查节点 u 是否在距故障源 S 不超过 K 的波及范围内。返回"是"或"否"。

注意：
- 任何涉及未排查节点的指令都会被系统拦截并返回"非法查询"。
- 你不能直接询问"距离 S 不超过 K 的阀门总数是多少"。

每次查询只能包含一个标签，使用以下 XML 格式：

- 邻居查询（例如查询节点 5 的相邻阀门）：
<query_neighbor>5</query_neighbor>

- 距离查询（例如查询节点 1 和 3 之间的管段数）：
<query_distance>1,3</query_distance>

- 范围判定查询（例如查询节点 7 是否在波及范围内）：
<query_in_range>7</query_in_range>

当你收集到足够信息后，提交最终检修工单。答案必须包含停机检修阀门总数 X，可选地附加节点列表作为佐证：

<answer>count=5, nodes=1,2,3,4,5</answer>

或仅提交总数：

<answer>count=5</answer>

若工单评估错误或格式不符，模拟失败。
"""

    contextualized_rule_en_4 = """\
[Industrial Scenario]
We are conducting an "Industrial Pipeline Fault Troubleshooting" simulation. Here are the rules:

The system configures an unknown pressure supply pipeline network (undirected tree graph T) comprising N valve nodes (numbered 1 to N). The pipelines are fully connected with no loops. The core faulty pump station S = {start} has been shut down, and the system has issued a pressure impact tier alert K = {threshold}.

Your goal is: determine the total number X of valve nodes that must be shut down for maintenance, which are impacted within tier K from the faulty station S. The tier refers to the number of pipe segments (edges) in the unique path between two nodes.

Initially, you have only located the faulty pump station S = {start}, recorded in the "inspected node set" D. You can only perform diagnostics on nodes in D.

You can repeatedly issue the following three types of commands (one command per turn):

1. **Connected Segment Query** (Neighbor Query): Ask for all adjacent valves directly connected by pipes to an inspected node u. Returns a list, and the returned nodes are automatically added to the inspected set D.
2. **Pipeline Distance Query** (Distance Query): Ask for the number of pipe segments between two inspected nodes u and v. Returns an integer.
3. **Impact Range Check** (Range Check Query): Ask whether an inspected node u is within the impact range of tier K from the fault source S. Returns "Yes" or "No".

Note:
- Any command involving uninspected nodes will be intercepted by the system and return "Illegal query".
- You cannot directly ask "What is the total number of valves within tier K from S".

Each command must contain only one tag, using the following XML format:

- Neighbor Query (e.g., querying adjacent valves of node 5):
<query_neighbor>5</query_neighbor>

- Distance Query (e.g., querying the number of pipe segments between nodes 1 and 3):
<query_distance>1,3</query_distance>

- Range Check Query (e.g., checking if node 7 is within the impact range):
<query_in_range>7</query_in_range>

When you have gathered enough information, submit the final maintenance work order. The answer must include the total shut-down valve count X, and optionally a list of nodes as evidence:

<answer>count=5, nodes=1,2,3,4,5</answer>

Or submit only the count:

<answer>count=5</answer>

If the work order evaluation is incorrect or the format is invalid, the simulation fails.
"""

    contextualized_rule_zh_5 = """\
我们正在进行“反洗钱资金链穿透”调查，规则如下：

系统设定了一个未知的涉案资金流转网络（无向树图 T），包含 N 个实体账户（编号 1 到 N），资金转移关系确凿且无循环转账。现锁定核心洗钱账户 S = {start}，法定的穿透追溯层级为 K = {threshold}。

你的目标是：确定从核心账户 S 算起，资金穿透层级小于等于 K 的需冻结关联账户总数 X。这里的层级指的是两账户间唯一的转账链路跳数（边数）。

初始时，你只掌握核心账户 S = {start} 的卷宗，存放在“已穿透账户清单”D 中。你只能对 D 中的账户发起调证。

你可以反复提出以下三类调证请求（每次仅限一个）：

1. **直接流水查询**（邻居查询）：询问某个已穿透账户 u 有直接资金往来的所有账户。返回一个列表，涉案账户自动并入穿透清单 D。
2. **流转链路查询**（距离查询）：询问两个已穿透账户 u 和 v 之间的流转跳数。返回一个整数。
3. **冻结范围判定**（范围判定查询）：询问某个已穿透账户 u 是否在距核心 S 不超过 K 层的法定冻结范围内。返回"是"或"否"。

注意：
- 任何涉及未穿透账户的请求都是越权的，会返回"非法查询"。
- 你不能直接询问"距离 S 不超过 K 层的账户总数是多少"。

每次请求只能包含一个标签，使用以下 XML 格式：

- 邻居查询（例如查询账户 5 的直接资金往来账户）：
<query_neighbor>5</query_neighbor>

- 距离查询（例如查询账户 1 和 3 之间的流转跳数）：
<query_distance>1,3</query_distance>

- 范围判定查询（例如查询账户 7 是否在法定冻结范围内）：
<query_in_range>7</query_in_range>

当你收集到足够线索后，提交最终查封令。答案必须包含需冻结关联账户总数 X，可选地附加账户列表作为佐证：

<answer>count=5, nodes=1,2,3,4,5</answer>

或仅提交总数：

<answer>count=5</answer>

若查封令错误或格式不符，调查宣告失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are conducting an "Anti-Money Laundering Fund Penetration" investigation. Here are the rules:

The system models an unknown illicit fund transfer network (undirected tree graph T) involving N entity accounts (numbered 1 to N). The fund transfer relationships are well-established without circular transfers. The core money laundering account S = {start} is targeted, and the statutory penetration tracing tier is K = {threshold}.

Your goal is: determine the total number X of associated accounts that need to be frozen, whose fund penetration tier from the core account S is at most K. The tier refers to the number of transfer linkage hops (edges) in the unique path between two accounts.

Initially, you only possess the dossier of the core account S = {start}, stored in the "penetrated account list" D. You can only request subpoenas for accounts in D.

You can repeatedly issue the following three types of subpoena requests (one request per turn):

1. **Direct Transaction Query** (Neighbor Query): Ask for all accounts that have direct fund transfers with a penetrated account u. Returns a list, and the involved accounts are automatically merged into the penetrated list D.
2. **Transfer Linkage Query** (Distance Query): Ask for the number of transfer hops between two penetrated accounts u and v. Returns an integer.
3. **Freeze Scope Check** (Range Check Query): Ask whether a penetrated account u is within the statutory freeze range of K tiers from the core S. Returns "Yes" or "No".

Note:
- Any request involving unpenetrated accounts is unauthorized and will return "Illegal query".
- You cannot directly ask "What is the total number of accounts within K tiers from S".

Each request must contain only one tag, using the following XML format:

- Neighbor Query (e.g., querying direct transaction accounts of account 5):
<query_neighbor>5</query_neighbor>

- Distance Query (e.g., querying transfer hops between accounts 1 and 3):
<query_distance>1,3</query_distance>

- Range Check Query (e.g., checking if account 7 is within the statutory freeze range):
<query_in_range>7</query_in_range>

When you have collected sufficient evidence, submit the final freezing injunction. The answer must include the total frozen account count X, and optionally a list of accounts as evidence:

<answer>count=5, nodes=1,2,3,4,5</answer>

Or submit only the count:

<answer>count=5</answer>

If the injunction is incorrect or the format is invalid, the investigation fails.
"""

    tags = ["answer", "query_neighbor", "query_distance", "query_in_range"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "start": 3,
                "threshold": 1,
                "edges": [(1,2), (2,3), (3,4), (4,5)],
            },
            2: {
                "n": 7,
                "start": 1,
                "threshold": 2,
                "edges": [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7)],
            },
            3: {
                "n": 10,
                "start": 5,
                "threshold": 2,
                "edges": [(1,2), (1,3), (2,4), (2,5), (5,6), (5,7), (3,8), (8,9), (8,10)],
            },
            4: {
                "n": 12,
                "start": 1,
                "threshold": 3,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (6,10), (7,11), (11,12)],
            },
            5: {
                "n": 15,
                "start": 8,
                "threshold": 3,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,10), (10,11), (3,12), (5,13), (9,14), (11,15)],
            },
        },
        "en": {
            1: {
                "n": 5,
                "start": 3,
                "threshold": 1,
                "edges": [(1,2), (2,3), (3,4), (4,5)],
            },
            2: {
                "n": 7,
                "start": 1,
                "threshold": 2,
                "edges": [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7)],
            },
            3: {
                "n": 10,
                "start": 5,
                "threshold": 2,
                "edges": [(1,2), (1,3), (2,4), (2,5), (5,6), (5,7), (3,8), (8,9), (8,10)],
            },
            4: {
                "n": 12,
                "start": 1,
                "threshold": 3,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (6,10), (7,11), (11,12)],
            },
            5: {
                "n": 15,
                "start": 8,
                "threshold": 3,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,10), (10,11), (3,12), (5,13), (9,14), (11,15)],
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
        
        self._game_info["start"] = cfg["start"]
        self._game_info["threshold"] = cfg["threshold"]
        
        self.n = cfg["n"]
        self.start = cfg["start"]
        self.threshold = cfg["threshold"]
        self.edges = cfg["edges"]
        
        self.adjacency = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adjacency[u].append(v)
            self.adjacency[v].append(u)
        
        self.distances = self._compute_distances()
        
        self.target_vertices = set()
        for v in range(1, self.n + 1):
            if self.distances[v] <= self.threshold:
                self.target_vertices.add(v)
        
        self.discovered = {self.start}

    def _compute_distances(self):
        distances = {i: float('inf') for i in range(1, self.n + 1)}
        distances[self.start] = 0
        queue = [self.start]
        head = 0
        
        while head < len(queue):
            u = queue[head]
            head += 1
            for v in self.adjacency[u]:
                if distances[v] == float('inf'):
                    distances[v] = distances[u] + 1
                    queue.append(v)
        
        return distances

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        ans_dict = {}
        count_match = re.search(r"count\s*=\s*(\d+)", raw_ans)
        if count_match:
            ans_dict["count"] = count_match.group(1)
            
        nodes_match = re.search(r"nodes\s*=\s*([\d\s,]+)", raw_ans)
        if nodes_match:
            ans_dict["nodes"] = nodes_match.group(1)
            
        if "count" not in ans_dict:
            return False
        
        try:
            submitted_count = int(ans_dict["count"])
        except:
            return False
        
        if submitted_count != len(self.target_vertices):
            return False
        
        if "nodes" in ans_dict:
            try:
                node_str = ans_dict["nodes"].strip()
                if node_str:
                    submitted_nodes = set(int(x.strip()) for x in node_str.split(",") if x.strip())
                    if submitted_nodes != self.target_vertices:
                        return False
            except:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            illegal = "非法查询"
            error_format = "错误：查询格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            illegal = "Illegal query"
            error_format = "Error: Invalid query format."

        if "query_neighbor" in parsed_info:
            try:
                u = int(parsed_info["query_neighbor"].strip())
                if u not in self.discovered:
                    return illegal
                if u < 1 or u > self.n:
                    return illegal
                
                neighbors = self.adjacency[u]
                for v in neighbors:
                    self.discovered.add(v)
                
                neighbor_str = ",".join(str(v) for v in sorted(neighbors))
                return f"[{neighbor_str}]"
            except:
                return error_format

        elif "query_distance" in parsed_info:
            try:
                raw = parsed_info["query_distance"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                u, v = int(parts[0]), int(parts[1])
                
                if u not in self.discovered or v not in self.discovered:
                    return illegal
                
                dist = self._compute_distance_between(u, v)
                return str(dist)
            except:
                return error_format

        elif "query_in_range" in parsed_info:
            try:
                u = int(parsed_info["query_in_range"].strip())
                if u not in self.discovered:
                    return illegal
                if u < 1 or u > self.n:
                    return illegal
                
                in_range = self.distances[u] <= self.threshold
                return yes_res if in_range else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for u in range(1, self.n + 1):
            neighbors = sorted(self.adjacency[u])
            neighbor_str = ",".join(str(v) for v in neighbors)
            ans = f"[{neighbor_str}]"
            queries.append({
                "query": f"<query_neighbor>{u}</query_neighbor>",
                "answer": ans
            })

        for u in range(1, self.n + 1):
            for v in range(u, self.n + 1):
                dist = self._compute_distance_between(u, v)
                queries.append({
                    "query": f"<query_distance>{u},{v}</query_distance>",
                    "answer": str(dist)
                })

        for u in range(1, self.n + 1):
            in_range = self.distances[u] <= self.threshold
            ans = yes_res if in_range else no_res
            queries.append({
                "query": f"<query_in_range>{u}</query_in_range>",
                "answer": ans
            })

        return queries

    def _cf_make_wrong(self, correct):
        s = str(correct)
        
        if s.isdigit():
            return str(int(s) + 1)
        
        if s == "是": return "否"
        if s == "否": return "是"
        
        if s.lower() == "yes":
            if s.isupper(): return "NO"
            if s.istitle(): return "No"
            return "no"
        if s.lower() == "no":
            if s.isupper(): return "YES"
            if s.istitle(): return "Yes"
            return "yes"
            
        return s + "_WRONG"

    def _compute_distance_between(self, u, v):
        if u == v:
            return 0
        
        distances = {u: 0}
        queue = [u]
        head = 0
        
        while head < len(queue):
            current = queue[head]
            head += 1
            
            if current == v:
                return distances[v]
            
            for neighbor in self.adjacency[current]:
                if neighbor not in distances:
                    distances[neighbor] = distances[current] + 1
                    queue.append(neighbor)
        
        return distances.get(v, float('inf'))