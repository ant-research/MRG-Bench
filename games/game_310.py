import re
from typing import Set, List, Tuple, Dict
from .base import Game

class GraphPathDeductionGame(Game):

    game_rule_zh = """\
我们来玩一个"图路径推理"游戏，规则如下：

游戏设定了一个无向带颜色的图。节点为：{nodes}。

边与颜色如下：
{edges_desc_zh}

隐藏设定：系统已从集合 {mode_set} 中秘密选择了一个"激活模式"。激活模式的含义是：仅该模式指定的颜色集合中的边处于"可用"状态，其余颜色的边处于"不可用"状态。

你的目标是：
1. 通过查询唯一确定当前的激活模式。
2. 在该模式下，枚举从 {start} 到 {end} 的所有简单路径。简单路径定义为：起点为 {start}，终点为 {end}，中间节点不重复，每相邻节点对为图中的边，且所用边均为当前模式下可用的边。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 边查询：询问两个节点之间的边在当前模式下是否可用。
   格式：<query_edge>U,V</query_edge>
   响应：
   - 若 (U,V) 不是图中的边：返回"无效"
   - 若是边且颜色被激活：返回"可用"
   - 若是边但颜色未被激活：返回"不可用"

2. 路径测试：给定一条路径序列，测试该路径上的所有边是否可用。
   格式：<query_path>U1-U2-...-Uk</query_path>
   约束：U1 必须为 {start}，路径至少包含 2 个节点。
   响应：
   - 若存在相邻对不是图中的边：返回"无效（步骤 i）"
   - 若所有相邻对均为图中的边，但在第 i 步首次遇到未被激活的边：返回"阻塞（步骤 i）"
   - 若所有边均被激活：返回"成功"

3. 计数查询：询问在当前激活模式下，图中有多少条边是可用的。
   格式：<query_count></query_count>
   响应：返回一个整数。

当你收集到足够信息后，请提交最终答案。答案必须包含：
1. 模式判定：在 {mode_set} 中给出唯一的激活模式。
2. 路径集合：列出从 {start} 到 {end} 的所有简单路径，每条路径用节点的连字符序列表示（如 A-C-E）。
3. 证据集：给出一组查询及其响应，说明如何通过这些证据排除其他模式，唯一确定你的判定。

提交格式：
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

示例：
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):可用|edge(A,C):可用|edge(B,C):不可用</answer>

注意：
- 若答案错误或格式不符，游戏失败。
- 请尽可能少地使用查询次数。
"""

    game_rule_en = """\
Let's play a "Graph Path Deduction" game. Here are the rules:

The game features an undirected colored graph. Nodes are: {nodes}.

Edges and their colors:
{edges_desc_en}

Hidden Setting: The system has secretly selected an "activation mode" from the set {mode_set}. The activation mode means: only edges with colors specified in that mode are "available", all other colored edges are "unavailable".

Your goal is to:
1. Uniquely determine the current activation mode through queries.
2. Enumerate all simple paths from {start} to {end} under that mode. A simple path is defined as: starts at {start}, ends at {end}, no repeated intermediate nodes, each adjacent node pair is an edge in the graph, and all edges used are available under the current mode.

You can repeatedly make the following three types of queries (one query per turn):

1. Edge Query: Ask if an edge between two nodes is available under the current mode.
   Format: <query_edge>U,V</query_edge>
   Response:
   - If (U,V) is not an edge in the graph: return "INVALID"
   - If it is an edge and its color is activated: return "ACTIVE"
   - If it is an edge but its color is not activated: return "INACTIVE"

2. Path Test: Given a path sequence, test if all edges in the path are available.
   Format: <query_path>U1-U2-...-Uk</query_path>
   Constraint: U1 must be {start}, path must contain at least 2 nodes.
   Response:
   - If any adjacent pair is not an edge in the graph: return "INVALID at step i"
   - If all adjacent pairs are edges but the first unavailable edge is encountered at step i: return "BLOCKED at step i"
   - If all edges are activated: return "SUCCESS"

3. Count Query: Ask how many edges are available under the current activation mode.
   Format: <query_count></query_count>
   Response: Return an integer.

When you have gathered sufficient information, submit your final answer. The answer must include:
1. Mode determination: Specify the unique activation mode from {mode_set}.
2. Path set: List all simple paths from {start} to {end}, each path represented as a hyphen-separated node sequence (e.g., A-C-E).
3. Evidence set: Provide a set of queries and their responses, explaining how these evidences exclude other modes and uniquely determine your judgment.

Submission format:
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

Example:
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):ACTIVE|edge(A,C):ACTIVE|edge(B,C):INACTIVE</answer>

Note:
- If the answer is incorrect or improperly formatted, the game fails.
- Please use as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市交通路网调度系统”。
系统映射了一个无向的城市路网图。交通枢纽节点为：{nodes}。

枢纽间的路段及其所属线路类型（颜色）如下：
{edges_desc_zh}

隐藏设定：交通指挥中心已从预设配置集合 {mode_set} 中秘密下发了一种"通行许可模式"。该模式的含义是：仅该模式指定的线路类型的路段处于"可用"（允许通行）状态，其余线路类型的路段处于"不可用"（封闭）状态。

你的目标是：
1. 通过查询唯一确定当前的通行许可模式。
2. 在该模式下，规划从起点 {start} 到终点 {end} 的所有可行简单路径。简单路径定义为：起点为 {start}，终点为 {end}，中间不经过重复枢纽，相邻枢纽间有物理路段，且所用路段均为当前模式下可用的路段。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 路段查询：询问两个枢纽之间的路段在当前模式下是否可用。
   格式：<query_edge>U,V</query_edge>
   响应：
   - 若 (U,V) 之间根本不存在路段：返回"无效"
   - 若有路段且其类型被许可：返回"可用"
   - 若有路段但其类型未被许可：返回"不可用"

2. 路线测试：给定一条行驶路线，测试该路线上所有经过的路段是否均畅通。
   格式：<query_path>U1-U2-...-Uk</query_path>
   约束：U1 必须为 {start}，路线至少包含 2 个枢纽。
   响应：
   - 若存在相邻枢纽间无物理路段：返回"无效（步骤 i）"
   - 若所有相邻枢纽均有路段，但在第 i 步首次遇到未被许可的封闭路段：返回"阻塞（步骤 i）"
   - 若全线所有路段均可用：返回"成功"

3. 计数查询：询问在当前通行许可模式下，全网共有多少个路段是可用的。
   格式：<query_count></query_count>
   响应：返回一个整数。

当你收集到足够信息后，请提交最终报告。报告必须包含：
1. 模式判定：在 {mode_set} 中给出唯一的通行许可模式。
2. 路线集合：列出从 {start} 到 {end} 的所有可行简单路径，每条路径用连字符分隔的枢纽序列表示（如 A-C-E）。
3. 证据集：给出一组查询及其响应，说明如何通过这些证据排除其他模式，唯一确定你的判定。

提交格式：
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

示例：
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):可用|edge(A,C):可用|edge(B,C):不可用</answer>

注意：
- 若报告错误或格式不符，调度系统将拒绝受理。
- 请尽可能少地使用查询次数。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Traffic Network Dispatch System".
The system maps an undirected city traffic graph. The transport hub nodes are: {nodes}.

The road segments between hubs and their line types (colors) are as follows:
{edges_desc_en}

Hidden Setting: The Traffic Command Center has secretly issued an "activation mode" (Passage Permission Mode) from the configuration set {mode_set}. This means: only road segments with line types specified in that mode are "available" (open for traffic), while all other segments are "unavailable" (closed).

Your goal is to:
1. Uniquely determine the current activation mode through queries.
2. Enumerate all feasible simple paths from the start hub {start} to the destination hub {end} under that mode. A simple path is defined as: starting at {start}, ending at {end}, with no repeated intermediate hubs, each adjacent hub pair connected by a physical road segment, and all segments used being available under the current mode.

You can repeatedly make the following three types of queries (one query per turn):

1. Segment Query: Ask if a road segment between two hubs is available under the current mode.
   Format: <query_edge>U,V</query_edge>
   Response:
   - If (U,V) is not a physical segment in the network: return "INVALID"
   - If it is a segment and its type is permitted: return "ACTIVE"
   - If it is a segment but its type is not permitted: return "INACTIVE"

2. Route Test: Given a driving route sequence, test if all segments in the route are passable.
   Format: <query_path>U1-U2-...-Uk</query_path>
   Constraint: U1 must be {start}, the route must contain at least 2 hubs.
   Response:
   - If any adjacent pair lacks a physical segment: return "INVALID at step i"
   - If all pairs are physical segments but the first closed segment is encountered at step i: return "BLOCKED at step i"
   - If all segments are permitted: return "SUCCESS"

3. Count Query: Ask how many road segments are currently available under the active mode.
   Format: <query_count></query_count>
   Response: Return an integer.

When you have gathered sufficient information, submit your final dispatch report. The answer must include:
1. Mode determination: Specify the unique activation mode from {mode_set}.
2. Path set: List all feasible simple paths from {start} to {end}, each path represented as a hyphen-separated hub sequence (e.g., A-C-E).
3. Evidence set: Provide a set of queries and their responses, explaining how these evidences exclude other modes and uniquely determine your judgment.

Submission format:
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

Example:
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):ACTIVE|edge(A,C):ACTIVE|edge(B,C):INACTIVE</answer>

Note:
- If the answer is incorrect or improperly formatted, the dispatch fails.
- Please use as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“生物神经网络分析系统”。
系统映射了一个无向的生理组织图。生理节点为：{nodes}。

节点间的生物通路及其组织类型（颜色）如下：
{edges_desc_zh}

隐藏设定：系统已根据患者体征从集合 {mode_set} 中秘密锁定了一种"生理激活状态"。该状态意味着：仅特定组织类型的生物通路处于"可用"（导通）状态，其余通路的生理机能暂时处于"不可用"（闭塞）状态。

你的目标是：
1. 通过检测唯一确定当前的生理激活状态。
2. 在该状态下，枚举从起始节点 {start} 到靶向节点 {end} 的所有有效简单传导路径。简单路径定义为：起点为 {start}，终点为 {end}，中间节点不重复，每相邻节点对存在生物通路，且所用通路均为当前状态下可用的通路。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 通路检测：询问两个生理节点之间的通路在当前状态下是否可用。
   格式：<query_edge>U,V</query_edge>
   响应：
   - 若 (U,V) 之间无生物通路：返回"无效"
   - 若有通路且处于导通状态：返回"可用"
   - 若有通路但处于闭塞状态：返回"不可用"

2. 传导测试：给定一条传导路径，测试沿线的生物通路是否全部畅通。
   格式：<query_path>U1-U2-...-Uk</query_path>
   约束：U1 必须为 {start}，路径至少包含 2 个节点。
   响应：
   - 若存在相邻对无通路连接：返回"无效（步骤 i）"
   - 若相邻对均有通路连接，但在第 i 步首次遇到闭塞通路：返回"阻塞（步骤 i）"
   - 若整条路径的通路均导通：返回"成功"

3. 计数查询：询问在当前生理激活状态下，共有多少条通路是可用的。
   格式：<query_count></query_count>
   响应：返回一个整数。

当你收集到足够信息后，请提交最终诊断。诊断必须包含：
1. 模式判定：在 {mode_set} 中给出唯一的生理激活状态。
2. 路径集合：列出从 {start} 到 {end} 的所有简单路径，每条路径用连字符序列表示（如 A-C-E）。
3. 证据集：给出一组查询及其响应，说明如何通过这些证据排除其他状态，唯一确定你的判定。

提交格式：
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

示例：
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):可用|edge(A,C):可用|edge(B,C):不可用</answer>

注意：
- 若诊断错误或格式不符，分析将宣告失败。
- 请尽可能少地使用检测次数。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Biological Neural Network Analysis System".
The system maps an undirected physiological tissue graph. Physiological nodes are: {nodes}.

Biological pathways between nodes and their tissue types (colors) are as follows:
{edges_desc_en}

Hidden Setting: Based on patient signs, the system has secretly locked an "activation mode" (Physiological Activation State) from the set {mode_set}. This means: only biological pathways of specific tissue types are "available" (conductive), while others are temporarily "unavailable" (occluded).

Your goal is to:
1. Uniquely determine the current physiological activation state through queries.
2. Enumerate all effective simple conduction paths from the starting node {start} to the target node {end} under that state. A simple path is defined as: starting at {start}, ending at {end}, no repeated intermediate nodes, each adjacent pair has a biological pathway, and all pathways used are available.

You can repeatedly make the following three types of queries (one query per turn):

1. Pathway Query: Ask if a pathway between two physiological nodes is available.
   Format: <query_edge>U,V</query_edge>
   Response:
   - If (U,V) is not a pathway in the graph: return "INVALID"
   - If it is a pathway and is conductive: return "ACTIVE"
   - If it is a pathway but occluded: return "INACTIVE"

2. Conduction Test: Given a conduction sequence, test if all pathways along the route are clear.
   Format: <query_path>U1-U2-...-Uk</query_path>
   Constraint: U1 must be {start}, path must contain at least 2 nodes.
   Response:
   - If any adjacent pair lacks a pathway connection: return "INVALID at step i"
   - If all pairs have pathways but the first occluded pathway is encountered at step i: return "BLOCKED at step i"
   - If all pathways are conductive: return "SUCCESS"

3. Count Query: Ask how many pathways are available under the current state.
   Format: <query_count></query_count>
   Response: Return an integer.

When you have gathered sufficient information, submit your final diagnosis. The answer must include:
1. Mode determination: Specify the unique activation state from {mode_set}.
2. Path set: List all simple paths from {start} to {end}, each path represented as a hyphen-separated node sequence (e.g., A-C-E).
3. Evidence set: Provide a set of queries and responses, explaining how they exclude other states and uniquely determine your judgment.

Submission format:
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

Example:
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):ACTIVE|edge(A,C):ACTIVE|edge(B,C):INACTIVE</answer>

Note:
- If the answer is incorrect or improperly formatted, the diagnosis fails.
- Please use as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
欢迎进入“知识图谱学习路径推演工具”。
系统构建了一个无向的学科概念图谱。核心知识点为：{nodes}。

知识点间的认知关联及其关联类型（颜色）如下：
{edges_desc_zh}

隐藏设定：教学委员会已从预设配置集合 {mode_set} 中选择了一套"教学大纲模式"。该模式表明：仅该模式指定的关联类型的知识点连接处于"可用"（被启用）状态，其余关联类型在当前大纲中处于"不可用"（未启用）状态。

你的目标是：
1. 通过查询唯一确定当前的教学大纲模式。
2. 在该大纲下，规划出从初始知识点 {start} 进阶到目标知识点 {end} 的所有连贯学习路径。简单路径定义为：起点为 {start}，终点为 {end}，中间知识点不重复，相邻知识点必须存在认知关联，且所涉及的关联均为当前大纲下可用的。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 关联查询：询问两个知识点之间的关联在当前大纲下是否可用。
   格式：<query_edge>U,V</query_edge>
   响应：
   - 若 (U,V) 之间本身不存在认知关联：返回"无效"
   - 若有关联且类型被大纲启用：返回"可用"
   - 若有关联但类型未被启用：返回"不可用"

2. 学习路径测试：给定一串知识点学习顺序，测试其内在关联是否均被启用。
   格式：<query_path>U1-U2-...-Uk</query_path>
   约束：U1 必须为 {start}，路径至少包含 2 个知识点。
   响应：
   - 若存在相邻对无认知关联：返回"无效（步骤 i）"
   - 若所有相邻对均有关联，但在第 i 步首次遇到未启用的跨度：返回"阻塞（步骤 i）"
   - 若所有学习跨度均可用：返回"成功"

3. 计数查询：询问在当前教学大纲模式下，图谱中共有多少条关联是被启用的。
   格式：<query_count></query_count>
   响应：返回一个整数。

当你收集到足够信息后，请提交最终规划。规划必须包含：
1. 模式判定：在 {mode_set} 中给出唯一的教学大纲模式。
2. 路径集合：列出从 {start} 到 {end} 的所有简单学习路径，每条路径用连字符表示（如 A-C-E）。
3. 证据集：给出一组查询及其响应，说明如何通过这些证据排除其他大纲模式，唯一确定你的判定。

提交格式：
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

示例：
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):可用|edge(A,C):可用|edge(B,C):不可用</answer>

注意：
- 若规划错误或格式不符，评估将失败。
- 请尽可能少地使用查询次数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Learning Path Deduction Tool".
The system constructs an undirected academic concept graph. The core knowledge points are: {nodes}.

The cognitive associations between points and their association types (colors) are as follows:
{edges_desc_en}

Hidden Setting: The Teaching Committee has selected a "Syllabus Mode" (activation mode) from the configuration set {mode_set}. This mode indicates: only knowledge point connections of specified association types are "available" (activated), while other association types are "unavailable" (inactive) under the current syllabus.

Your goal is to:
1. Uniquely determine the current Syllabus Mode through queries.
2. Plan all coherent learning simple paths from the initial knowledge point {start} to the target knowledge point {end} under that syllabus. A simple path is defined as: starting at {start}, ending at {end}, no repeated intermediate points, each adjacent point must have a cognitive association, and all involved associations are available.

You can repeatedly make the following three types of queries (one query per turn):

1. Association Query: Ask if an association between two knowledge points is available under the current syllabus.
   Format: <query_edge>U,V</query_edge>
   Response:
   - If there is fundamentally no cognitive association between (U,V): return "INVALID"
   - If there is an association and its type is activated: return "ACTIVE"
   - If there is an association but its type is not activated: return "INACTIVE"

2. Learning Path Test: Given a sequence of knowledge points, test if all internal associations are activated.
   Format: <query_path>U1-U2-...-Uk</query_path>
   Constraint: U1 must be {start}, path must contain at least 2 knowledge points.
   Response:
   - If any adjacent pair lacks a cognitive association: return "INVALID at step i"
   - If all pairs have associations but the first inactive leap is encountered at step i: return "BLOCKED at step i"
   - If all learning leaps are available: return "SUCCESS"

3. Count Query: Ask how many associations are activated in the graph under the current syllabus.
   Format: <query_count></query_count>
   Response: Return an integer.

When you have gathered sufficient information, submit your final planning. The answer must include:
1. Mode determination: Specify the unique syllabus mode from {mode_set}.
2. Path set: List all simple learning paths from {start} to {end}, each path represented as a hyphen-separated sequence (e.g., A-C-E).
3. Evidence set: Provide a set of queries and responses, explaining how they exclude other syllabus modes and uniquely determine your judgment.

Submission format:
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

Example:
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):ACTIVE|edge(A,C):ACTIVE|edge(B,C):INACTIVE</answer>

Note:
- If the answer is incorrect or improperly formatted, the evaluation fails.
- Please use as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
欢迎访问“工厂流水线物流网络规划平台”。
平台映射了一个无向的厂区物料传输网络。加工工作站为：{nodes}。

工作站之间的传输带及其传输类型（颜色）如下：
{edges_desc_zh}

隐藏设定：中控室已从策略池 {mode_set} 中选定了一个"产线运行模式"。此模式意味着：只有特定传输类型的传输带被开启并处于"可用"（运转）状态，其余传输带则被断电并处于"不可用"（停机）状态。

你的目标是：
1. 通过查询排查出当前的产线运行模式。
2. 在该模式下，找出从装料工作站 {start} 到卸料工作站 {end} 的所有安全物流线路。简单路径定义为：起点为 {start}，终点为 {end}，中间不经过重复的工作站，相邻工作站间必须铺设传输带，且所经传输带均为当前模式下可用的。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 传输带查询：询问两个工作站之间的传输带当前是否可用。
   格式：<query_edge>U,V</query_edge>
   响应：
   - 若 (U,V) 间根本未铺设传输带：返回"无效"
   - 若有传输带且正常运转：返回"可用"
   - 若有传输带但处于停机状态：返回"不可用"

2. 物流线路测试：给定一条流水线路，测试物料是否能沿该线全段输送。
   格式：<query_path>U1-U2-...-Uk</query_path>
   约束：U1 必须为 {start}，线路至少包含 2 个工作站。
   响应：
   - 若存在相邻工作站间无传输带物理连接：返回"无效（步骤 i）"
   - 若均有传输带，但在第 i 步首次遇到停机断电的传输带：返回"阻塞（步骤 i）"
   - 若全线所有传输带均在运转：返回"成功"

3. 计数查询：询问在当前运行模式下，全厂共有多少条传输带处于可用状态。
   格式：<query_count></query_count>
   响应：返回一个整数。

当你收集到足够信息后，请提交最终网络排布报告。报告必须包含：
1. 模式判定：在 {mode_set} 中给出唯一的产线运行模式。
2. 线路集合：列出从 {start} 到 {end} 的所有运转顺畅的简单路径，每条路径用连字符表示（如 A-C-E）。
3. 证据集：给出一组查询及其响应，说明如何通过这些证据排除其他模式，唯一确定你的判定。

提交格式：
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

示例：
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):可用|edge(A,C):可用|edge(B,C):不可用</answer>

注意：
- 若规划结果不准确或格式不符，系统会提示部署失败。
- 请尽可能少地使用测试资源。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Factory Assembly Line Logistics Network Planning Platform".
The platform maps an undirected plant material transmission network. The processing workstations are: {nodes}.

The conveyor belts between workstations and their transmission types (colors) are as follows:
{edges_desc_en}

Hidden Setting: The control room has selected an "activation mode" (Production Line Running Mode) from the strategy pool {mode_set}. This mode means: only conveyor belts of specific transmission types are turned on and "available" (running), while others are powered off and "unavailable" (stopped).

Your goal is to:
1. Uniquely determine the current production line running mode through queries.
2. Find all safe logistics simple paths from the loading workstation {start} to the unloading workstation {end} under that mode. A simple path is defined as: starting at {start}, ending at {end}, no repeated intermediate workstations, adjacent workstations must be connected by conveyor belts, and all belts traversed must be available.

You can repeatedly make the following three types of queries (one query per turn):

1. Conveyor Belt Query: Ask if a conveyor belt between two workstations is currently available.
   Format: <query_edge>U,V</query_edge>
   Response:
   - If there is no conveyor belt deployed between (U,V): return "INVALID"
   - If there is a belt and it's running normally: return "ACTIVE"
   - If there is a belt but it is stopped: return "INACTIVE"

2. Logistics Route Test: Given an assembly route, test if materials can be transported along the entire line.
   Format: <query_path>U1-U2-...-Uk</query_path>
   Constraint: U1 must be {start}, the route must contain at least 2 workstations.
   Response:
   - If any adjacent pair lacks a physical conveyor belt connection: return "INVALID at step i"
   - If all pairs have belts but the first powered-off belt is encountered at step i: return "BLOCKED at step i"
   - If all conveyor belts on the line are running: return "SUCCESS"

3. Count Query: Ask how many conveyor belts are available in the entire plant under the current mode.
   Format: <query_count></query_count>
   Response: Return an integer.

When you have gathered sufficient information, submit your final network layout report. The answer must include:
1. Mode determination: Specify the unique running mode from {mode_set}.
2. Route set: List all smoothly running simple paths from {start} to {end}, each path represented as a hyphen-separated sequence (e.g., A-C-E).
3. Evidence set: Provide a set of queries and responses, explaining how they exclude other modes and uniquely determine your judgment.

Submission format:
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

Example:
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):ACTIVE|edge(A,C):ACTIVE|edge(B,C):INACTIVE</answer>

Note:
- If the planning result is inaccurate or improperly formatted, the deployment fails.
- Please use as few query resources as possible.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“案件证据链逻辑推演系统”。
系统构建了一张无向的案件实体关联图。案件事实或实体节点为：{nodes}。

实体间的证据关联及其证据类型（颜色）如下：
{edges_desc_zh}

隐藏设定：法庭已从预设集合 {mode_set} 中敲定了一套严格的"法庭采信标准"。这意味着：仅属于该标准允许采信的证据类型的关联处于"可用"（被采信）状态，其余类型的证据关联均不予认定，处于"不可用"（驳回）状态。

你的目标是：
1. 通过查询推断出法庭当前确立的采信标准。
2. 在该标准下，梳理出从起始案情 {start} 到关键控罪事实 {end} 的所有完整逻辑闭环（简单路径）。简单路径定义为：起点为 {start}，终点为 {end}，中间不经过重复的事实节点，相邻节点必须具备证据关联，且所用证据关联必须全被法庭采信。

你可以反复提出以下三类查询（每次仅限一个查询）：

1. 证据关联审查：询问两个事实间的证据关联在当前标准下是否可用。
   格式：<query_edge>U,V</query_edge>
   响应：
   - 若 (U,V) 间毫无关联：返回"无效"
   - 若有关联且符合采信标准：返回"可用"
   - 若有关联但被法庭排除：返回"不可用"

2. 证据链条测试：给定一条逻辑推理链条，测试其各个环节的关联是否都能经受质证。
   格式：<query_path>U1-U2-...-Uk</query_path>
   约束：U1 必须为 {start}，链条至少包含 2 个实体节点。
   响应：
   - 若存在相邻节点缺乏证据支撑：返回"无效（步骤 i）"
   - 若均有证据支撑，但在第 i 步首次遇到被驳回的证据关联：返回"阻塞（步骤 i）"
   - 若整条证据链的环节均被采信：返回"成功"

3. 计数查询：询问在当前采信标准下，案卷中共有多少条证据关联是可用的。
   格式：<query_count></query_count>
   响应：返回一个整数。

当你收集到足够信息后，请提交最终出庭辩护策略。策略必须包含：
1. 模式判定：在 {mode_set} 中给出唯一的法庭采信标准。
2. 证据链集合：列出从 {start} 到 {end} 的所有无懈可击的简单路径，每条链用连字符表示（如 A-C-E）。
3. 证据集：给出一组查询及其响应，说明如何通过这些质证信息排除其他标准，唯一确定你的推断。

提交格式：
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

示例：
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):可用|edge(A,C):可用|edge(B,C):不可用</answer>

注意：
- 若逻辑推理错误或格式不符，法庭将驳回你的辩护。
- 请尽可能少地消耗庭审时间进行查询。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Case Evidence Chain Logic Deduction System".
The system constructs an undirected case entity association graph. The case facts or entity nodes are: {nodes}.

The evidence associations between entities and their evidence types (colors) are as follows:
{edges_desc_en}

Hidden Setting: The court has finalized a strict "Court Admissibility Standard" (activation mode) from the preset set {mode_set}. This means: only evidence associations of admissible types are "available" (admitted), while all other types are not recognized and are "unavailable" (rejected).

Your goal is to:
1. Uniquely determine the current admissibility standard established by the court through queries.
2. Sort out all complete logical closed loops (simple paths) from the starting fact {start} to the key charge fact {end} under that standard. A simple path is defined as: starting at {start}, ending at {end}, no repeated intermediate fact nodes, adjacent nodes must possess an evidence association, and all utilized evidence associations must be fully admitted by the court.

You can repeatedly make the following three types of queries (one query per turn):

1. Evidence Association Review: Ask if an evidence association between two facts is available under the current standard.
   Format: <query_edge>U,V</query_edge>
   Response:
   - If there is absolutely no association between (U,V): return "INVALID"
   - If there is an association and it meets the standard: return "ACTIVE"
   - If there is an association but it is excluded by the court: return "INACTIVE"

2. Evidence Chain Test: Given a logical deduction chain, test if all links can withstand cross-examination.
   Format: <query_path>U1-U2-...-Uk</query_path>
   Constraint: U1 must be {start}, the chain must contain at least 2 entity nodes.
   Response:
   - If any adjacent pair lacks evidence support: return "INVALID at step i"
   - If all pairs have evidence but the first rejected association is encountered at step i: return "BLOCKED at step i"
   - If all links in the entire evidence chain are admitted: return "SUCCESS"

3. Count Query: Ask how many evidence associations in the case file are available under the current standard.
   Format: <query_count></query_count>
   Response: Return an integer.

When you have gathered sufficient information, submit your final trial defense strategy. The answer must include:
1. Mode determination: Specify the unique admissibility standard from {mode_set}.
2. Evidence chain set: List all unassailable simple paths from {start} to {end}, each chain represented as a hyphen-separated sequence (e.g., A-C-E).
3. Evidence set: Provide a set of queries and responses, explaining how these cross-examination details exclude other standards and uniquely determine your deduction.

Submission format:
<answer>mode=XX, paths=path1;path2;..., evidence=query1:response1|query2:response2|...</answer>

Example:
<answer>mode=RB, paths=A-B-D-E;A-C-D-E, evidence=edge(A,B):ACTIVE|edge(A,C):ACTIVE|edge(B,C):INACTIVE</answer>

Note:
- If the logical deduction is incorrect or improperly formatted, the court will overrule your defense.
- Please use as few queries as possible to save trial time.
"""

    tags = ["answer", "query_edge", "query_path", "query_count"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "nodes": "A, B, C, D, E",
                "edges": [
                    ("A", "B", "红"),
                    ("A", "C", "蓝"),
                    ("B", "C", "绿"),
                    ("B", "D", "蓝"),
                    ("C", "D", "红"),
                    ("C", "E", "蓝"),
                    ("D", "E", "绿"),
                ],
                "modes": ["R", "B", "G", "RB", "BG", "RG"],
                "active_mode": "B",
                "start": "A",
                "end": "E",
            },
            2: {
                "nodes": "A, B, C, D, E",
                "edges": [
                    ("A", "B", "红"),
                    ("A", "C", "蓝"),
                    ("B", "C", "绿"),
                    ("B", "D", "蓝"),
                    ("C", "D", "红"),
                    ("C", "E", "蓝"),
                    ("D", "E", "绿"),
                ],
                "modes": ["R", "B", "G", "RB", "BG", "RG"],
                "active_mode": "RB",
                "start": "A",
                "end": "E",
            },
            3: {
                "nodes": "A, B, C, D, E, F",
                "edges": [
                    ("A", "B", "红"),
                    ("A", "C", "蓝"),
                    ("B", "C", "绿"),
                    ("B", "D", "红"),
                    ("C", "D", "蓝"),
                    ("C", "E", "绿"),
                    ("D", "E", "红"),
                    ("D", "F", "蓝"),
                    ("E", "F", "绿"),
                ],
                "modes": ["R", "B", "G", "RB", "BG", "RG"],
                "active_mode": "BG",
                "start": "A",
                "end": "F",
            },
            4: {
                "nodes": "A, B, C, D, E, F",
                "edges": [
                    ("A", "B", "红"),
                    ("A", "C", "蓝"),
                    ("A", "D", "绿"),
                    ("B", "C", "绿"),
                    ("B", "E", "蓝"),
                    ("C", "D", "红"),
                    ("C", "E", "红"),
                    ("D", "E", "蓝"),
                    ("D", "F", "绿"),
                    ("E", "F", "红"),
                ],
                "modes": ["R", "B", "G", "RB", "BG", "RG"],
                "active_mode": "RG",
                "start": "A",
                "end": "F",
            },
            5: {
                "nodes": "A, B, C, D, E, F, G",
                "edges": [
                    ("A", "B", "红"),
                    ("A", "C", "蓝"),
                    ("A", "D", "绿"),
                    ("B", "C", "绿"),
                    ("B", "E", "红"),
                    ("C", "D", "红"),
                    ("C", "E", "蓝"),
                    ("C", "F", "绿"),
                    ("D", "F", "蓝"),
                    ("E", "F", "红"),
                    ("E", "G", "绿"),
                    ("F", "G", "蓝"),
                ],
                "modes": ["R", "B", "G", "RB", "BG", "RG"],
                "active_mode": "BG",
                "start": "A",
                "end": "G",
            },
        },
        "en": {
            1: {
                "nodes": "A, B, C, D, E",
                "edges": [
                    ("A", "B", "Red"),
                    ("A", "C", "Blue"),
                    ("B", "C", "Green"),
                    ("B", "D", "Blue"),
                    ("C", "D", "Red"),
                    ("C", "E", "Blue"),
                    ("D", "E", "Green"),
                ],
                "modes": ["R", "B", "G", "RB", "BG", "RG"],
                "active_mode": "B",
                "start": "A",
                "end": "E",
            },
            2: {
                "nodes": "A, B, C, D, E",
                "edges": [
                    ("A", "B", "Red"),
                    ("A", "C", "Blue"),
                    ("B", "C", "Green"),
                    ("B", "D", "Blue"),
                    ("C", "D", "Red"),
                    ("C", "E", "Blue"),
                    ("D", "E", "Green"),
                ],
                "modes": ["R", "B", "G", "RB", "BG", "RG"],
                "active_mode": "RB",
                "start": "A",
                "end": "E",
            },
            3: {
                "nodes": "A, B, C, D, E, F",
                "edges": [
                    ("A", "B", "Red"),
                    ("A", "C", "Blue"),
                    ("B", "C", "Green"),
                    ("B", "D", "Red"),
                    ("C", "D", "Blue"),
                    ("C", "E", "Green"),
                    ("D", "E", "Red"),
                    ("D", "F", "Blue"),
                    ("E", "F", "Green"),
                ],
                "modes": ["R", "B", "G", "RB", "BG", "RG"],
                "active_mode": "BG",
                "start": "A",
                "end": "F",
            },
            4: {
                "nodes": "A, B, C, D, E, F",
                "edges": [
                    ("A", "B", "Red"),
                    ("A", "C", "Blue"),
                    ("A", "D", "Green"),
                    ("B", "C", "Green"),
                    ("B", "E", "Blue"),
                    ("C", "D", "Red"),
                    ("C", "E", "Red"),
                    ("D", "E", "Blue"),
                    ("D", "F", "Green"),
                    ("E", "F", "Red"),
                ],
                "modes": ["R", "B", "G", "RB", "BG", "RG"],
                "active_mode": "RG",
                "start": "A",
                "end": "F",
            },
            5: {
                "nodes": "A, B, C, D, E, F, G",
                "edges": [
                    ("A", "B", "Red"),
                    ("A", "C", "Blue"),
                    ("A", "D", "Green"),
                    ("B", "C", "Green"),
                    ("B", "E", "Red"),
                    ("C", "D", "Red"),
                    ("C", "E", "Blue"),
                    ("C", "F", "Green"),
                    ("D", "F", "Blue"),
                    ("E", "F", "Red"),
                    ("E", "G", "Green"),
                    ("F", "G", "Blue"),
                ],
                "modes": ["R", "B", "G", "RB", "BG", "RG"],
                "active_mode": "BG",
                "start": "A",
                "end": "G",
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
        
        self._game_info["nodes"] = cfg["nodes"]
        self._game_info["start"] = cfg["start"]
        self._game_info["end"] = cfg["end"]
        self._game_info["mode_set"] = "{" + ", ".join(cfg["modes"]) + "}"
        
        edges_desc_zh = "\n".join([f"- {u}-{v}（{c}）" for u, v, c in cfg["edges"]])
        edges_desc_en = "\n".join([f"- {u}-{v} ({c})" for u, v, c in cfg["edges"]])
        self._game_info["edges_desc_zh"] = edges_desc_zh
        self._game_info["edges_desc_en"] = edges_desc_en
        
        self.graph = {}
        for u, v, color in cfg["edges"]:
            self.graph[(u, v)] = color
            self.graph[(v, u)] = color
        
        self.active_mode = cfg["active_mode"]
        self.start_node = cfg["start"]
        self.end_node = cfg["end"]
        
        self.active_edges = self._get_active_edges(self.active_mode)
        
        self.correct_paths = self._find_all_simple_paths()

    def _get_active_edges(self, mode: str) -> Set[Tuple[str, str]]:
        color_map_zh = {"红": "R", "蓝": "B", "绿": "G"}
        color_map_en = {"Red": "R", "Blue": "B", "Green": "G"}
        
        active_colors = set(mode)
        active_edges = set()
        
        for (u, v), color in self.graph.items():
            if self.config.language == "zh":
                color_code = color_map_zh.get(color, color[0].upper())
            else:
                color_code = color_map_en.get(color, color[0].upper())
            
            if color_code in active_colors:
                active_edges.add((u, v))
        
        return active_edges

    def _find_all_simple_paths(self) -> List[str]:
        paths = []
        
        def dfs(current: str, target: str, visited: Set[str], path: List[str]):
            if current == target:
                paths.append("-".join(path))
                return
            
            for (u, v) in self.active_edges:
                if u == current and v not in visited:
                    visited.add(v)
                    path.append(v)
                    dfs(v, target, visited, path)
                    path.pop()
                    visited.remove(v)
        
        dfs(self.start_node, self.end_node, {self.start_node}, [self.start_node])
        return sorted(paths)

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"]
            
            mode_match = re.search(r'mode\s*=\s*(\S+)', raw_ans, re.IGNORECASE)
            paths_match = re.search(r'paths\s*=\s*(.+?)(?:\s*,\s*evidence\s*=)', raw_ans, re.IGNORECASE | re.DOTALL)
            evidence_match = re.search(r'evidence\s*=\s*(.+)', raw_ans, re.IGNORECASE | re.DOTALL)
            
            if not mode_match or not paths_match:
                return False
            
            mode_str = mode_match.group(1).strip().rstrip(",")
            paths_str = paths_match.group(1).strip()
            
            if mode_str != self.active_mode:
                return False
            
            try:
                model_paths = set(p.strip() for p in paths_str.split(";") if p.strip())
            except:
                return False
            
            correct_paths_set = set(self.correct_paths)
            if model_paths != correct_paths_set:
                return False
            
            if evidence_match:
                evidence_str = evidence_match.group(1).strip()
                try:
                    evidence_valid = self._validate_evidence(evidence_str)
                except Exception:
                    pass
            
            return True
            
        except Exception as e:
            return False

    def _validate_evidence(self, evidence_str: str) -> bool:
        try:
            evidence_pairs = []
            for item in evidence_str.split("|"):
                if ":" not in item:
                    continue
                query_part, response_part = item.split(":", 1)
                evidence_pairs.append((query_part.strip(), response_part.strip()))
            
            if len(evidence_pairs) == 0:
                return False
            
            cfg = self.DIFFICULTY_CONFIG[self.config.language][self.config.difficulty]
            all_modes = cfg["modes"]
            
            consistent_modes = []
            for mode in all_modes:
                if self._check_mode_consistency(mode, evidence_pairs):
                    consistent_modes.append(mode)
            
            return len(consistent_modes) == 1 and consistent_modes[0] == self.active_mode
            
        except Exception:
            return False

    def _check_mode_consistency(self, mode: str, evidence_pairs: List[Tuple[str, str]]) -> bool:
        mode_edges = self._get_active_edges(mode)
        
        for query, response in evidence_pairs:
            if "edge" in query.lower():
                match = re.search(r'\(([^,]+),([^)]+)\)', query)
                if match:
                    u, v = match.group(1).strip(), match.group(2).strip()
                    expected = self._get_edge_response(u, v, mode_edges)
                    if expected.lower() != response.lower():
                        return False
            elif "path" in query.lower():
                match = re.search(r'\(([^)]+)\)', query)
                if not match:
                    match = re.search(r'([A-Z](?:-[A-Z])+)', query)
                if match:
                    path_str = match.group(1).strip()
                    expected = self._simulate_path_query(path_str, mode_edges)
                    if expected.lower() != response.lower():
                        return False
            elif "count" in query.lower():
                expected_count = len(mode_edges) // 2
                try:
                    response_count = int(re.search(r'\d+', response).group())
                    if response_count != expected_count:
                        return False
                except (AttributeError, ValueError):
                    return False
        
        return True

    def _simulate_path_query(self, path_str: str, mode_edges: Set[Tuple[str, str]]) -> str:
        nodes = [n.strip() for n in path_str.split("-")]
        
        if len(nodes) < 2:
            return "ERROR"
        
        for i in range(1, len(nodes)):
            u, v = nodes[i-1], nodes[i]
            
            if (u, v) not in self.graph and (v, u) not in self.graph:
                if self.config.language == "zh":
                    return f"无效（步骤 {i}）"
                else:
                    return f"INVALID at step {i}"
            
            if (u, v) not in mode_edges and (v, u) not in mode_edges:
                if self.config.language == "zh":
                    return f"阻塞（步骤 {i}）"
                else:
                    return f"BLOCKED at step {i}"
        
        return "成功" if self.config.language == "zh" else "SUCCESS"

    def _get_edge_response(self, u: str, v: str, active_edges: Set[Tuple[str, str]]) -> str:
        if (u, v) not in self.graph and (v, u) not in self.graph:
            return "INVALID" if self.config.language == "en" else "无效"
        
        if (u, v) in active_edges or (v, u) in active_edges:
            return "ACTIVE" if self.config.language == "en" else "可用"
        else:
            return "INACTIVE" if self.config.language == "en" else "不可用"

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "query_edge" in parsed_info:
            return self._handle_edge_query(parsed_info["query_edge"])
        
        elif "query_path" in parsed_info:
            return self._handle_path_query(parsed_info["query_path"])
        
        elif "query_count" in parsed_info:
            return self._handle_count_query()
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct in ("ACTIVE", "可用"):
            return "INACTIVE" if self.config.language == "en" else "不可用"
        if correct in ("INACTIVE", "不可用"):
            return "ACTIVE" if self.config.language == "en" else "可用"
        if correct in ("INVALID", "无效"):
            return "ACTIVE" if self.config.language == "en" else "可用"
        
        if correct in ("SUCCESS", "成功"):
            return ("BLOCKED at step 1" if self.config.language == "en" 
                    else "阻塞（步骤 1）")
        
        if "BLOCKED" in correct or "阻塞" in correct:
            return "SUCCESS" if self.config.language == "en" else "成功"
        
        if "INVALID at step" in correct or "无效（步骤" in correct:
            return "SUCCESS" if self.config.language == "en" else "成功"
        
        try:
            count = int(correct)
            wrong_count = count + 1
            return str(wrong_count)
        except ValueError:
            pass
        
        return correct + " (wrong)"

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        queries = []

        unique_edges = set()
        for (u, v) in self.graph.keys():
            if u < v:
                unique_edges.add((u, v))
        
        for u, v in sorted(list(unique_edges)):
            content = f"{u},{v}"
            query_xml = f"<query_edge>{content}</query_edge>"
            ans = self._handle_edge_query(content)
            queries.append({"query": query_xml, "answer": ans})

        adj = {}
        for (u, v) in self.graph.keys():
            if u not in adj: adj[u] = []
            adj[u].append(v)
            
        all_nodes = set()
        for (u, v) in self.graph.keys():
            all_nodes.add(u)
            all_nodes.add(v)
        max_path_len = len(all_nodes)
        
        stack = [(self.start_node, [self.start_node])]
        
        while stack:
            curr, path = stack.pop()
            
            if len(path) >= 2:
                content = "-".join(path)
                query_xml = f"<query_path>{content}</query_path>"
                ans = self._handle_path_query(content)
                queries.append({"query": query_xml, "answer": ans})
            
            if len(path) < max_path_len:
                if curr in adj:
                    for neighbor in sorted(adj[curr], reverse=True):
                        if neighbor not in path:
                            stack.append((neighbor, path + [neighbor]))

        query_xml = "<query_count></query_count>"
        ans = self._handle_count_query()
        queries.append({"query": query_xml, "answer": ans})

        return queries

    def _handle_edge_query(self, query_str: str) -> str:
        try:
            nodes = [n.strip() for n in query_str.split(",")]
            if len(nodes) != 2:
                raise ValueError
            
            u, v = nodes[0], nodes[1]
            
            if (u, v) not in self.graph and (v, u) not in self.graph:
                return "无效" if self.config.language == "zh" else "INVALID"
            
            if (u, v) in self.active_edges or (v, u) in self.active_edges:
                return "可用" if self.config.language == "zh" else "ACTIVE"
            else:
                return "不可用" if self.config.language == "zh" else "INACTIVE"
        
        except:
            return "错误：格式无效。" if self.config.language == "zh" else "Error: Invalid format."

    def _handle_path_query(self, query_str: str) -> str:
        try:
            nodes = [n.strip() for n in query_str.split("-")]
            
            if len(nodes) < 2:
                return "错误：路径至少需要 2 个节点。" if self.config.language == "zh" else "Error: Path must contain at least 2 nodes."
            
            if nodes[0] != self.start_node:
                return f"错误：路径必须从 {self.start_node} 开始。" if self.config.language == "zh" else f"Error: Path must start from {self.start_node}."
            
            for i in range(1, len(nodes)):
                u, v = nodes[i-1], nodes[i]
                
                if (u, v) not in self.graph and (v, u) not in self.graph:
                    if self.config.language == "zh":
                        return f"无效（步骤 {i}）"
                    else:
                        return f"INVALID at step {i}"
                
                if (u, v) not in self.active_edges and (v, u) not in self.active_edges:
                    if self.config.language == "zh":
                        return f"阻塞（步骤 {i}）"
                    else:
                        return f"BLOCKED at step {i}"
            
            return "成功" if self.config.language == "zh" else "SUCCESS"
        
        except:
            return "错误：格式无效。" if self.config.language == "zh" else "Error: Invalid format."

    def _handle_count_query(self) -> str:
        count = len(self.active_edges) // 2
        return str(count)