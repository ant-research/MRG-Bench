from .base import Game
import re

class HiddenPropertyGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"隐藏性质推理"游戏，规则如下：

游戏设定了一个有限无向加权图 G=(V,E)，你可以看到全部顶点、边及其整数权重。图的具体信息如下：

顶点集合 V：{vertices}

边集合 E 及权重：
{edges_info}

隐藏设定：
存在一个固定且未知的布尔判定函数 P，它只依赖边的权重 w。对于任意边 e，当且仅当 P(w(e))=1 时，我们称边 e "满足性质"。函数 P 在整个游戏过程中保持不变。

你的目标：
通过查询推断出函数 P 的规则，并对一个新的边集合做出准确的计数预测。

可用的查询类型（每次只能提交一个查询）：

1. 边集合计数查询：询问指定边集合中有多少条边满足性质。
   格式示例：<query_count_edges>E1,E3,E5</query_count_edges>

2. 权重区间计数查询：询问权重在指定区间内的边中有多少条满足性质。
   格式示例：<query_count_range>10,50</query_count_range>
   （表示查询权重在 [10,50] 区间内的边）

3. 顶点邻接计数查询：询问与指定顶点相邻的所有边中有多少条满足性质。
   格式示例：<query_count_incident>N1,N3</query_count_incident>
   （查询所有与 N1 或 N3 相邻的边，每条边只计数一次）

4. 单边判定查询：询问某条边是否满足性质。
   格式示例：<query_single>E5</query_single>

5. 比较查询：比较两个边集合中满足性质的边的数量。
   格式示例：<query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   （比较显式边集 {{E1,E2,E3}} 与权重区间 [20,40] 内的边集）
   支持的集合指定方式：edges:边列表、range:L,R、incident:顶点列表

提交最终答案时，需要同时给出：
1. 你推断出的 P 函数规则（假设）
2. 对一个新边集合的计数预测

答案格式：
<answer>hypothesis=[你的规则描述], predict_set=[边列表], predict_count=[数字]</answer>

示例：
<answer>hypothesis=权重大于等于50, predict_set=E9,E10,E11, predict_count=3</answer>

注意：
- 每次只能提交一个查询标签
- 规则描述需要清晰明确，能够对任意整数权重做出判定
- 预测集合必须是之前未完整查询过的边集合
- 答案错误将导致游戏失败
"""

    game_rule_en = """\
Let's play a "Hidden Property Inference" game. Here are the rules:

The game features a finite undirected weighted graph G=(V,E). You can see all vertices, edges, and their integer weights. The graph information is as follows:

Vertex set V: {vertices}

Edge set E and weights:
{edges_info}

Hidden Setting:
There exists a fixed and unknown boolean decision function P that depends only on the edge weight w. For any edge e, we say edge e "satisfies the property" if and only if P(w(e))=1. Function P remains constant throughout the game.

Your Goal:
Infer the rule of function P through queries and make an accurate count prediction for a new edge set.

Available Query Types (only one query per turn):

1. Edge Set Count Query: Ask how many edges in a specified edge set satisfy the property.
   Format example: <query_count_edges>E1,E3,E5</query_count_edges>

2. Weight Range Count Query: Ask how many edges with weights in a specified range satisfy the property.
   Format example: <query_count_range>10,50</query_count_range>
   (Query edges with weights in [10,50])

3. Vertex Incident Count Query: Ask how many edges incident to specified vertices satisfy the property.
   Format example: <query_count_incident>N1,N3</query_count_incident>
   (Query all edges incident to N1 or N3, each edge counted once)

4. Single Edge Decision Query: Ask if a specific edge satisfies the property.
   Format example: <query_single>E5</query_single>

5. Comparison Query: Compare the count of edges satisfying the property in two edge sets.
   Format example: <query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   (Compare explicit edge set {{E1,E2,E3}} with edges in weight range [20,40])
   Supported set specification: edges:edge_list, range:L,R, incident:vertex_list

When submitting the final answer, provide:
1. Your inferred rule for function P (hypothesis)
2. A count prediction for a new edge set

Answer format:
<answer>hypothesis=[your rule description], predict_set=[edge list], predict_count=[number]</answer>

Example:
<answer>hypothesis=weight greater than or equal to 50, predict_set=E9,E10,E11, predict_count=3</answer>

Notes:
- Only one query tag per turn
- Rule description must be clear and applicable to any integer weight
- Prediction set must be a previously unqueried complete edge set
- Incorrect answer leads to game failure
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通路网分析系统”。
系统映射了一个有限的无向交通路网图 G=(V,E)，你可以查阅所有的交通枢纽（顶点）、连接路段（边）及其日均车流量（整数权重）。路网的具体信息如下：

枢纽节点集合 V：{vertices}

路段集合 E 及日均车流量：
{edges_info}

隐藏设定：
路网中存在一个固定的布尔评估模型 P，该模型仅依赖路段的车流量 w。对于任意路段 e，当且仅当 P(w(e))=1 时，我们判定该路段为“高风险拥堵路段”。评估模型 P 在整个分析过程中保持不变。

你的目标：
通过查询指令推断出评估模型 P 的判定规则，并对一组新的路段集合做出准确的高风险路段数量预测。

可用的查询指令（每次只能提交一个查询）：

1. 指定路段计数查询：询问特定路段集合中有多少条是高风险拥堵路段。
   格式示例：<query_count_edges>E1,E3,E5</query_count_edges>

2. 流量区间计数查询：询问日均车流量在指定区间内的路段中，有多少条是高风险拥堵路段。
   格式示例：<query_count_range>10,50</query_count_range>
   （表示查询流量在 [10,50] 区间内的路段）

3. 枢纽邻接计数查询：询问与指定枢纽相连的所有路段中，有多少条是高风险拥堵路段。
   格式示例：<query_count_incident>N1,N3</query_count_incident>
   （查询所有接入 N1 或 N3 的路段，每条路段只计数一次）

4. 单一判定查询：询问某条特定路段是否为高风险拥堵路段。
   格式示例：<query_single>E5</query_single>

5. 对比分析查询：比较两组路段集合中高风险拥堵路段的数量。
   格式示例：<query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   （比较显式指定的路段集合 {{E1,E2,E3}} 与车流量在 [20,40] 区间内的路段集合）
   支持的集合指定方式：edges:路段列表、range:L,R、incident:枢纽列表

提交最终分析报告时，需要同时给出：
1. 你推断出的 P 模型规则（假设）
2. 对一个全新的路段集合的拥堵数量预测

报告格式：
<answer>hypothesis=[你的规则描述], predict_set=[路段列表], predict_count=[数字]</answer>

示例：
<answer>hypothesis=车流量大于等于50, predict_set=E9,E10,E11, predict_count=3</answer>

注意：
- 每次只能提交一个查询标签
- 规则描述需要清晰明确，能够对任意整数流量做出判定
- 预测集合必须是之前未完整查询过的路段集合
- 预测错误将导致分析任务失败
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Intelligent Traffic Network Analysis System".
The system maps a finite undirected traffic network graph G=(V,E). You can view all traffic hubs (vertices), connecting road segments (edges), and their average daily traffic volume (integer weights). The network information is as follows:

Hub Node Set V: {vertices}

Road Segment Set E and Daily Traffic Volume:
{edges_info}

Hidden Setting:
There exists a fixed boolean evaluation model P that depends solely on the traffic volume w. For any road segment e, it is classified as a "High-Risk Congestion Road" if and only if P(w(e))=1. The model P remains constant throughout the analysis.

Your Goal:
Infer the evaluation rule of model P through queries and make an accurate prediction of the number of high-risk roads for a new set of road segments.

Available Query Directives (only one query per turn):

1. Specified Road Count Query: Ask how many road segments in a specific set are high-risk.
   Format example: <query_count_edges>E1,E3,E5</query_count_edges>

2. Volume Range Count Query: Ask how many road segments with traffic volume in a specified range are high-risk.
   Format example: <query_count_range>10,50</query_count_range>
   (Query roads with volume in [10,50])

3. Hub Incident Count Query: Ask how many road segments connected to specified hubs are high-risk.
   Format example: <query_count_incident>N1,N3</query_count_incident>
   (Query all roads connected to N1 or N3, each road counted once)

4. Single Decision Query: Ask if a specific road segment is high-risk.
   Format example: <query_single>E5</query_single>

5. Comparative Analysis Query: Compare the number of high-risk road segments between two sets.
   Format example: <query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   (Compare explicit road set {{E1,E2,E3}} with roads in volume range [20,40])
   Supported set specifications: edges:road_list, range:L,R, incident:hub_list

When submitting the final analysis report, provide:
1. Your inferred rule for model P (hypothesis)
2. A count prediction for a completely new set of road segments

Report format:
<answer>hypothesis=[your rule description], predict_set=[road list], predict_count=[number]</answer>

Example:
<answer>hypothesis=traffic volume greater than or equal to 50, predict_set=E9,E10,E11, predict_count=3</answer>

Notes:
- Only one query tag per turn
- Rule description must be clear and applicable to any integer volume
- Prediction set must be a previously unqueried complete road set
- Incorrect prediction leads to task failure
"""

    contextualized_rule_zh_2 = """\
欢迎使用“蛋白质相互作用网络推演系统”。
系统构建了一个有限的无向生物分子图 G=(V,E)，你可以查阅所有蛋白质节点（顶点）、相互作用路径（边）及其结合亲和力指数（整数权重）。网络图的具体信息如下：

蛋白质节点集合 V：{vertices}

相互作用路径集合 E 及结合亲和力：
{edges_info}

隐藏设定：
系统中存在一个固定的布尔靶向判定函数 P，该函数仅依赖路径的结合亲和力 w。对于任意路径 e，当且仅当 P(w(e))=1 时，我们称该路径具有“临床显著靶向性”。函数 P 在整个推演过程中保持不变。

你的目标：
通过实验查询推断出函数 P 的判定规则，并对一组新的交互路径集合做出准确的靶向路径数量预测。

可用的实验查询（每次只能提交一个查询）：

1. 路径集合计数查询：询问指定相互作用路径集合中有多少条具有临床显著靶向性。
   格式示例：<query_count_edges>E1,E3,E5</query_count_edges>

2. 亲和力区间计数查询：询问亲和力在指定区间内的路径中，有多少条具有临床显著靶向性。
   格式示例：<query_count_range>10,50</query_count_range>
   （表示查询亲和力在 [10,50] 区间内的路径）

3. 节点邻接计数查询：询问与指定蛋白质相邻的所有路径中，有多少条具有临床显著靶向性。
   格式示例：<query_count_incident>N1,N3</query_count_incident>
   （查询所有与 N1 或 N3 相邻的路径，每条路径只计数一次）

4. 单一路径判定查询：询问某条特定相互作用路径是否具有临床显著靶向性。
   格式示例：<query_single>E5</query_single>

5. 对比分析查询：比较两组路径集合中具有临床显著靶向性的路径数量。
   格式示例：<query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   （比较显式路径集合 {{E1,E2,E3}} 与亲和力区间 [20,40] 内的路径集合）
   支持的集合指定方式：edges:路径列表、range:L,R、incident:蛋白质列表

提交最终推演结果时，需要同时给出：
1. 你推断出的 P 函数规则（假设）
2. 对一个新的路径集合的计数预测

结果格式：
<answer>hypothesis=[你的规则描述], predict_set=[路径列表], predict_count=[数字]</answer>

示例：
<answer>hypothesis=亲和力大于等于50, predict_set=E9,E10,E11, predict_count=3</answer>

注意：
- 每次只能提交一个查询标签
- 规则描述需要清晰明确，能够对任意整数亲和力做出判定
- 预测集合必须是之前未完整查询过的路径集合
- 预测错误将导致推演失败
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Protein Interaction Network Deduction System".
The system constructs a finite undirected biomolecular graph G=(V,E). You can view all protein nodes (vertices), interaction pathways (edges), and their binding affinity indices (integer weights). The network details are as follows:

Protein Node Set V: {vertices}

Interaction Pathway Set E and Binding Affinity:
{edges_info}

Hidden Setting:
There exists a fixed boolean targeting decision function P that depends only on the pathway's binding affinity w. For any pathway e, it possesses "Clinically Significant Targeting" if and only if P(w(e))=1. Function P remains constant throughout the deduction process.

Your Goal:
Infer the rule of function P through experimental queries and make an accurate count prediction of targeted pathways for a new set of interaction pathways.

Available Experimental Queries (only one query per turn):

1. Pathway Set Count Query: Ask how many pathways in a specified set possess clinically significant targeting.
   Format example: <query_count_edges>E1,E3,E5</query_count_edges>

2. Affinity Range Count Query: Ask how many pathways with affinity in a specified range possess clinically significant targeting.
   Format example: <query_count_range>10,50</query_count_range>
   (Query pathways with affinity in [10,50])

3. Node Incident Count Query: Ask how many pathways incident to specified proteins possess clinically significant targeting.
   Format example: <query_count_incident>N1,N3</query_count_incident>
   (Query all pathways incident to N1 or N3, each pathway counted once)

4. Single Pathway Decision Query: Ask if a specific interaction pathway possesses clinically significant targeting.
   Format example: <query_single>E5</query_single>

5. Comparative Analysis Query: Compare the number of targeted pathways between two pathway sets.
   Format example: <query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   (Compare explicit pathway set {{E1,E2,E3}} with pathways in affinity range [20,40])
   Supported set specifications: edges:pathway_list, range:L,R, incident:protein_list

When submitting the final deduction result, provide:
1. Your inferred rule for function P (hypothesis)
2. A count prediction for a new pathway set

Result format:
<answer>hypothesis=[your rule description], predict_set=[pathway list], predict_count=[number]</answer>

Example:
<answer>hypothesis=affinity greater than or equal to 50, predict_set=E9,E10,E11, predict_count=3</answer>

Notes:
- Only one query tag per turn
- Rule description must be clear and applicable to any integer affinity
- Prediction set must be a previously unqueried complete pathway set
- Incorrect prediction leads to deduction failure
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学科知识图谱分析引擎”。
引擎载入了一个有限的无向知识图谱 G=(V,E)，你可以看到所有知识概念（顶点）、认知关联路径（边）及其关联强度评估值（整数权重）。图谱的具体信息如下：

概念节点集合 V：{vertices}

关联路径集合 E 及关联强度：
{edges_info}

隐藏设定：
课程体系中存在一个固定的布尔评估规则 P，它只依赖关联路径的强度值 w。对于任意关联路径 e，当且仅当 P(w(e))=1 时，我们称该路径为“核心先修依赖”。规则 P 在整个分析过程中保持不变。

你的目标：
通过探索查询推断出规则 P 的逻辑，并对一组新的关联路径集合做出准确的核心依赖数量预测。

可用的探索查询（每次只能提交一个查询）：

1. 路径集合计数查询：询问指定的关联路径集合中有多少条是核心先修依赖。
   格式示例：<query_count_edges>E1,E3,E5</query_count_edges>

2. 强度区间计数查询：询问关联强度在指定区间内的路径中，有多少条是核心先修依赖。
   格式示例：<query_count_range>10,50</query_count_range>
   （表示查询强度在 [10,50] 区间内的路径）

3. 概念邻接计数查询：询问与指定概念节点相连的所有路径中，有多少条是核心先修依赖。
   格式示例：<query_count_incident>N1,N3</query_count_incident>
   （查询所有与 N1 或 N3 相连的路径，每条路径只计数一次）

4. 单一判定查询：询问某条特定的关联路径是否为核心先修依赖。
   格式示例：<query_single>E5</query_single>

5. 对比评估查询：比较两组路径集合中核心先修依赖的数量。
   格式示例：<query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   （比较显式路径集合 {{E1,E2,E3}} 与关联强度在 [20,40] 区间内的路径集合）
   支持的集合指定方式：edges:路径列表、range:L,R、incident:概念节点列表

提交最终分析结论时，需要同时给出：
1. 你推断出的 P 规则逻辑（假设）
2. 对一个新的关联路径集合的计数预测

结论格式：
<answer>hypothesis=[你的规则描述], predict_set=[路径列表], predict_count=[数字]</answer>

示例：
<answer>hypothesis=关联强度大于等于50, predict_set=E9,E10,E11, predict_count=3</answer>

注意：
- 每次只能提交一个查询标签
- 规则描述需要清晰明确，能够对任意整数强度值做出判定
- 预测集合必须是之前未完整查询过的路径集合
- 预测错误将导致分析任务失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Subject Knowledge Graph Analysis Engine".
The engine has loaded a finite undirected knowledge graph G=(V,E). You can see all knowledge concepts (vertices), cognitive association links (edges), and their association strength evaluation values (integer weights). The graph details are as follows:

Concept Node Set V: {vertices}

Association Link Set E and Association Strength:
{edges_info}

Hidden Setting:
Within the curriculum system, there exists a fixed boolean evaluation rule P that depends only on the link's association strength w. For any association link e, it is classified as a "Core Prerequisite Dependency" if and only if P(w(e))=1. Rule P remains constant throughout the analysis.

Your Goal:
Infer the logic of rule P through exploratory queries and make an accurate count prediction of core dependencies for a new set of association links.

Available Exploratory Queries (only one query per turn):

1. Link Set Count Query: Ask how many links in a specified association link set are core prerequisite dependencies.
   Format example: <query_count_edges>E1,E3,E5</query_count_edges>

2. Strength Range Count Query: Ask how many links with association strength in a specified range are core prerequisite dependencies.
   Format example: <query_count_range>10,50</query_count_range>
   (Query links with strength in [10,50])

3. Concept Incident Count Query: Ask how many links connected to specified concept nodes are core prerequisite dependencies.
   Format example: <query_count_incident>N1,N3</query_count_incident>
   (Query all links connected to N1 or N3, each link counted once)

4. Single Decision Query: Ask if a specific association link is a core prerequisite dependency.
   Format example: <query_single>E5</query_single>

5. Comparative Evaluation Query: Compare the number of core prerequisite dependencies between two link sets.
   Format example: <query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   (Compare explicit link set {{E1,E2,E3}} with links in strength range [20,40])
   Supported set specifications: edges:link_list, range:L,R, incident:concept_list

When submitting the final analysis conclusion, provide:
1. Your inferred logic for rule P (hypothesis)
2. A count prediction for a new association link set

Conclusion format:
<answer>hypothesis=[your rule description], predict_set=[link list], predict_count=[number]</answer>

Example:
<answer>hypothesis=association strength greater than or equal to 50, predict_set=E9,E10,E11, predict_count=3</answer>

Notes:
- Only one query tag per turn
- Rule description must be clear and applicable to any integer strength value
- Prediction set must be a previously unqueried complete link set
- Incorrect prediction leads to analysis failure
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业流水线瓶颈排查系统”。
系统建立了一个有限的无向车间拓扑图 G=(V,E)，你可以监控所有生产工作站（顶点）、物料传送带（边）及其额定负载量（整数权重）。车间的具体拓扑信息如下：

工作站集合 V：{vertices}

传送带集合 E 及额定负载量：
{edges_info}

隐藏设定：
生产调度系统中存在一个固定的布尔安全判定函数 P，它仅取决于传送带的额定负载量 w。对于任意传送带 e，当且仅当 P(w(e))=1 时，我们判定该传送带“存在瓶颈风险”。函数 P 在整个排查过程中保持不变。

你的目标：
通过系统查询推断出函数 P 的判定规则，并对一组新的传送带集合做出准确的瓶颈风险计数预测。

可用的系统查询（每次只能提交一个查询）：

1. 传送带集合计数查询：询问指定的传送带集合中有多少条存在瓶颈风险。
   格式示例：<query_count_edges>E1,E3,E5</query_count_edges>

2. 负载区间计数查询：询问额定负载量在指定区间内的传送带中，有多少条存在瓶颈风险。
   格式示例：<query_count_range>10,50</query_count_range>
   （表示查询负载在 [10,50] 区间内的传送带）

3. 工作站邻接计数查询：询问与指定工作站相连的所有传送带中，有多少条存在瓶颈风险。
   格式示例：<query_count_incident>N1,N3</query_count_incident>
   （查询所有连接到 N1 或 N3 的传送带，每条传送带只计数一次）

4. 单一状态查询：询问某条特定传送带是否存在瓶颈风险。
   格式示例：<query_single>E5</query_single>

5. 对比排查查询：比较两组传送带集合中存在瓶颈风险的传送带数量。
   格式示例：<query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   （比较显式传送带集合 {{E1,E2,E3}} 与负载在 [20,40] 区间内的传送带集合）
   支持的集合指定方式：edges:传送带列表、range:L,R、incident:工作站列表

提交最终排查报告时，需要同时给出：
1. 你推断出的 P 判定规则（假设）
2. 对一个新的传送带集合的风险计数预测

报告格式：
<answer>hypothesis=[你的规则描述], predict_set=[传送带列表], predict_count=[数字]</answer>

示例：
<answer>hypothesis=负载量大于等于50, predict_set=E9,E10,E11, predict_count=3</answer>

注意：
- 每次只能提交一个查询标签
- 规则描述需要清晰明确，能够对任意整数负载量做出判定
- 预测集合必须是之前未完整查询过的传送带集合
- 预测错误将导致排查任务失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Industrial Assembly Line Bottleneck Diagnostics System".
The system establishes a finite undirected workshop topology graph G=(V,E). You can monitor all production workstations (vertices), material conveyor belts (edges), and their rated load capacities (integer weights). The specific workshop topology is as follows:

Workstation Set V: {vertices}

Conveyor Belt Set E and Rated Load Capacity:
{edges_info}

Hidden Setting:
The production scheduling system contains a fixed boolean safety decision function P, which depends solely on the conveyor belt's rated load capacity w. For any conveyor belt e, it is classified as having a "Bottleneck Risk Present" if and only if P(w(e))=1. Function P remains constant throughout the diagnostics process.

Your Goal:
Infer the rule of function P through system queries and make an accurate count prediction of bottleneck risks for a new set of conveyor belts.

Available System Queries (only one query per turn):

1. Conveyor Belt Set Count Query: Ask how many conveyor belts in a specified set have a bottleneck risk.
   Format example: <query_count_edges>E1,E3,E5</query_count_edges>

2. Load Range Count Query: Ask how many conveyor belts with load capacities in a specified range have a bottleneck risk.
   Format example: <query_count_range>10,50</query_count_range>
   (Query conveyor belts with loads in [10,50])

3. Workstation Incident Count Query: Ask how many conveyor belts connected to specified workstations have a bottleneck risk.
   Format example: <query_count_incident>N1,N3</query_count_incident>
   (Query all conveyor belts connected to N1 or N3, each belt counted once)

4. Single Status Query: Ask if a specific conveyor belt has a bottleneck risk.
   Format example: <query_single>E5</query_single>

5. Comparative Diagnostics Query: Compare the number of at-risk conveyor belts between two sets.
   Format example: <query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   (Compare explicit belt set {{E1,E2,E3}} with belts in load range [20,40])
   Supported set specifications: edges:belt_list, range:L,R, incident:workstation_list

When submitting the final diagnostics report, provide:
1. Your inferred rule for function P (hypothesis)
2. A risk count prediction for a new set of conveyor belts

Report format:
<answer>hypothesis=[your rule description], predict_set=[belt list], predict_count=[number]</answer>

Example:
<answer>hypothesis=load capacity greater than or equal to 50, predict_set=E9,E10,E11, predict_count=3</answer>

Notes:
- Only one query tag per turn
- Rule description must be clear and applicable to any integer load capacity
- Prediction set must be a previously unqueried complete conveyor belt set
- Incorrect prediction leads to diagnostics failure
"""

    contextualized_rule_zh_5 = """\
欢迎使用“反洗钱资金链审计系统”。
系统抓取了一个有限的无向资金转移图 G=(V,E)，你可以查看所有涉案实体账户（顶点）、资金交易流水（边）及其交易金额（整数权重）。资金图的具体信息如下：

账户节点集合 V：{vertices}

交易流水集合 E 及交易金额：
{edges_info}

隐藏设定：
合规系统中固化了一个未知的布尔审计规则 P，该规则只依赖流水的交易金额 w。对于任意交易 e，当且仅当 P(w(e))=1 时，我们认定该流水为“涉嫌洗钱的异常交易”。审计规则 P 在整个调查过程中保持不变。

你的目标：
通过审计查询推断出规则 P 的判定逻辑，并对一组新的交易流水集合做出准确的异常流水数量预测。

可用的审计查询（每次只能提交一个查询）：

1. 交易集合计数查询：询问指定的交易流水集合中有多少条是异常交易。
   格式示例：<query_count_edges>E1,E3,E5</query_count_edges>

2. 金额区间计数查询：询问交易金额在指定区间内的流水中，有多少条是异常交易。
   格式示例：<query_count_range>10,50</query_count_range>
   （表示查询金额在 [10,50] 区间内的流水）

3. 账户关联计数查询：询问与指定账户相关联的所有流水中，有多少条是异常交易。
   格式示例：<query_count_incident>N1,N3</query_count_incident>
   （查询所有与 N1 或 N3 相关的交易流水，每条流水只计数一次）

4. 单一流水判定查询：询问某条特定的交易流水是否为异常交易。
   格式示例：<query_single>E5</query_single>

5. 对比穿透查询：比较两组交易流水集合中异常交易的数量。
   格式示例：<query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   （比较显式流水集合 {{E1,E2,E3}} 与金额在 [20,40] 区间内的流水集合）
   支持的集合指定方式：edges:流水列表、range:L,R、incident:账户列表

提交最终审计结案报告时，需要同时给出：
1. 你推断出的 P 审计规则（假设）
2. 对一个新的交易流水集合的异常计数预测

报告格式：
<answer>hypothesis=[你的规则描述], predict_set=[流水列表], predict_count=[数字]</answer>

示例：
<answer>hypothesis=交易金额大于等于50, predict_set=E9,E10,E11, predict_count=3</answer>

注意：
- 每次只能提交一个查询标签
- 规则描述需要清晰明确，能够对任意整数金额做出判定
- 预测集合必须是之前未完整查询过的交易流水集合
- 预测错误将导致审计任务失败
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Anti-Money Laundering Financial Chain Audit System".
The system has captured a finite undirected fund transfer graph G=(V,E). You can view all involved entity accounts (vertices), financial transactions (edges), and their transaction amounts (integer weights). The financial graph details are as follows:

Account Node Set V: {vertices}

Transaction Set E and Transaction Amounts:
{edges_info}

Hidden Setting:
The compliance system embeds an unknown boolean audit rule P that depends solely on the transaction amount w. For any transaction e, it is flagged as a "Suspicious Transaction of Money Laundering" if and only if P(w(e))=1. The audit rule P remains constant throughout the investigation.

Your Goal:
Infer the logic of rule P through audit queries and make an accurate count prediction of suspicious transactions for a new set of financial transactions.

Available Audit Queries (only one query per turn):

1. Transaction Set Count Query: Ask how many transactions in a specified set are suspicious.
   Format example: <query_count_edges>E1,E3,E5</query_count_edges>

2. Amount Range Count Query: Ask how many transactions with amounts in a specified range are suspicious.
   Format example: <query_count_range>10,50</query_count_range>
   (Query transactions with amounts in [10,50])

3. Account Associated Count Query: Ask how many transactions associated with specified accounts are suspicious.
   Format example: <query_count_incident>N1,N3</query_count_incident>
   (Query all transactions involving N1 or N3, each transaction counted once)

4. Single Transaction Decision Query: Ask if a specific financial transaction is suspicious.
   Format example: <query_single>E5</query_single>

5. Comparative Penetration Query: Compare the number of suspicious transactions between two sets.
   Format example: <query_compare>edges:E1,E2,E3|range:20,40</query_compare>
   (Compare explicit transaction set {{E1,E2,E3}} with transactions in amount range [20,40])
   Supported set specifications: edges:transaction_list, range:L,R, incident:account_list

When submitting the final audit closure report, provide:
1. Your inferred audit rule P (hypothesis)
2. A suspicious count prediction for a new set of financial transactions

Report format:
<answer>hypothesis=[your rule description], predict_set=[transaction list], predict_count=[number]</answer>

Example:
<answer>hypothesis=transaction amount greater than or equal to 50, predict_set=E9,E10,E11, predict_count=3</answer>

Notes:
- Only one query tag per turn
- Rule description must be clear and applicable to any integer amount
- Prediction set must be a previously unqueried complete transaction set
- Incorrect prediction leads to audit failure
"""

    tags = ["answer", "query_count_edges", "query_count_range", "query_count_incident", 
            "query_single", "query_compare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "vertices": ["N1", "N2", "N3", "N4"],
                "edges": [
                    ("E1", "N1", "N2", 8),
                    ("E2", "N1", "N3", 15),
                    ("E3", "N2", "N3", 22),
                    ("E4", "N2", "N4", 37),
                    ("E5", "N3", "N4", 44),
                ],
                "property_func": lambda w: w % 2 == 0,
                "property_desc": "权重是偶数",
            },
            2: {
                "vertices": ["N1", "N2", "N3", "N4", "N5"],
                "edges": [
                    ("E1", "N1", "N2", 20),
                    ("E2", "N1", "N3", 35),
                    ("E3", "N2", "N3", 45),
                    ("E4", "N2", "N4", 50),
                    ("E5", "N3", "N4", 60),
                    ("E6", "N3", "N5", 70),
                    ("E7", "N4", "N5", 80),
                ],
                "property_func": lambda w: w >= 50,
                "property_desc": "权重大于等于50",
            },
            3: {
                "vertices": ["N1", "N2", "N3", "N4", "N5", "N6"],
                "edges": [
                    ("E1", "N1", "N2", 7),
                    ("E2", "N1", "N3", 14),
                    ("E3", "N2", "N3", 22),
                    ("E4", "N2", "N4", 28),
                    ("E5", "N3", "N4", 35),
                    ("E6", "N3", "N5", 41),
                    ("E7", "N4", "N5", 49),
                    ("E8", "N4", "N6", 55),
                    ("E9", "N5", "N6", 63),
                ],
                "property_func": lambda w: w % 7 == 0,
                "property_desc": "权重是7的倍数",
            },
            4: {
                "vertices": ["N1", "N2", "N3", "N4", "N5", "N6", "N7"],
                "edges": [
                    ("E1", "N1", "N2", 12),
                    ("E2", "N1", "N3", 23),
                    ("E3", "N2", "N3", 34),
                    ("E4", "N2", "N4", 47),
                    ("E5", "N3", "N4", 56),
                    ("E6", "N3", "N5", 68),
                    ("E7", "N4", "N5", 79),
                    ("E8", "N4", "N6", 81),
                    ("E9", "N5", "N6", 92),
                    ("E10", "N5", "N7", 105),
                    ("E11", "N6", "N7", 118),
                ],
                "property_func": lambda w: w % 10 > 5,
                "property_desc": "权重模10的结果大于5",
            },
            5: {
                "vertices": ["N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8"],
                "edges": [
                    ("E1", "N1", "N2", 7),
                    ("E2", "N1", "N3", 12),
                    ("E3", "N2", "N3", 19),
                    ("E4", "N2", "N4", 21),
                    ("E5", "N3", "N4", 28),
                    ("E6", "N3", "N5", 33),
                    ("E7", "N4", "N5", 40),
                    ("E8", "N4", "N6", 42),
                    ("E9", "N5", "N6", 55),
                    ("E10", "N5", "N7", 60),
                    ("E11", "N6", "N7", 63),
                    ("E12", "N6", "N8", 75),
                    ("E13", "N7", "N8", 82),
                    ("E14", "N1", "N8", 91),
                    ("E15", "N2", "N7", 100),
                    ("E16", "N3", "N8", 105),
                ],
                "property_func": lambda w: w > 1 and all(w % i != 0 for i in range(2, int(w**0.5) + 1)),
                "property_desc": "权重是质数",
            },
        },
        "en": {
            1: {
                "vertices": ["N1", "N2", "N3", "N4"],
                "edges": [
                    ("E1", "N1", "N2", 8),
                    ("E2", "N1", "N3", 15),
                    ("E3", "N2", "N3", 22),
                    ("E4", "N2", "N4", 37),
                    ("E5", "N3", "N4", 44),
                ],
                "property_func": lambda w: w % 2 == 0,
                "property_desc": "weight is even",
            },
            2: {
                "vertices": ["N1", "N2", "N3", "N4", "N5"],
                "edges": [
                    ("E1", "N1", "N2", 20),
                    ("E2", "N1", "N3", 35),
                    ("E3", "N2", "N3", 45),
                    ("E4", "N2", "N4", 50),
                    ("E5", "N3", "N4", 60),
                    ("E6", "N3", "N5", 70),
                    ("E7", "N4", "N5", 80),
                ],
                "property_func": lambda w: w >= 50,
                "property_desc": "weight greater than or equal to 50",
            },
            3: {
                "vertices": ["N1", "N2", "N3", "N4", "N5", "N6"],
                "edges": [
                    ("E1", "N1", "N2", 7),
                    ("E2", "N1", "N3", 14),
                    ("E3", "N2", "N3", 22),
                    ("E4", "N2", "N4", 28),
                    ("E5", "N3", "N4", 35),
                    ("E6", "N3", "N5", 41),
                    ("E7", "N4", "N5", 49),
                    ("E8", "N4", "N6", 55),
                    ("E9", "N5", "N6", 63),
                ],
                "property_func": lambda w: w % 7 == 0,
                "property_desc": "weight is divisible by 7",
            },
            4: {
                "vertices": ["N1", "N2", "N3", "N4", "N5", "N6", "N7"],
                "edges": [
                    ("E1", "N1", "N2", 12),
                    ("E2", "N1", "N3", 23),
                    ("E3", "N2", "N3", 34),
                    ("E4", "N2", "N4", 47),
                    ("E5", "N3", "N4", 56),
                    ("E6", "N3", "N5", 68),
                    ("E7", "N4", "N5", 79),
                    ("E8", "N4", "N6", 81),
                    ("E9", "N5", "N6", 92),
                    ("E10", "N5", "N7", 105),
                    ("E11", "N6", "N7", 118),
                ],
                "property_func": lambda w: w % 10 > 5,
                "property_desc": "weight modulo 10 is greater than 5",
            },
            5: {
                "vertices": ["N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8"],
                "edges": [
                    ("E1", "N1", "N2", 7),
                    ("E2", "N1", "N3", 12),
                    ("E3", "N2", "N3", 19),
                    ("E4", "N2", "N4", 21),
                    ("E5", "N3", "N4", 28),
                    ("E6", "N3", "N5", 33),
                    ("E7", "N4", "N5", 40),
                    ("E8", "N4", "N6", 42),
                    ("E9", "N5", "N6", 55),
                    ("E10", "N5", "N7", 60),
                    ("E11", "N6", "N7", 63),
                    ("E12", "N6", "N8", 75),
                    ("E13", "N7", "N8", 82),
                    ("E14", "N1", "N8", 91),
                    ("E15", "N2", "N7", 100),
                    ("E16", "N3", "N8", 105),
                ],
                "property_func": lambda w: w > 1 and all(w % i != 0 for i in range(2, int(w**0.5) + 1)),
                "property_desc": "weight is prime",
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
        
        self.vertices = cfg["vertices"]
        self.edges = cfg["edges"]
        self.property_func = cfg["property_func"]
        self.property_desc = cfg["property_desc"]
        
        self.edge_map = {e[0]: e for e in self.edges}
        
        self.incident_map = {v: [] for v in self.vertices}
        for eid, v1, v2, w in self.edges:
            self.incident_map[v1].append(eid)
            self.incident_map[v2].append(eid)
        
        self.queried_sets = set()
        
        edges_info_lines = []
        for eid, v1, v2, w in self.edges:
            edges_info_lines.append(f"  {eid}: {v1}–{v2}, w={w}")
        
        self._game_info["vertices"] = ", ".join(self.vertices)
        self._game_info["edges_info"] = "\n".join(edges_info_lines)

    def _count_satisfying_edges(self, edge_ids):
        count = 0
        for eid in edge_ids:
            if eid in self.edge_map:
                weight = self.edge_map[eid][3]
                if self.property_func(weight):
                    count += 1
        return count

    def _parse_edge_set_spec(self, spec):
        spec = spec.strip()
        
        if spec.startswith("edges:"):
            edge_list = spec[6:].strip()
            return set(e.strip() for e in edge_list.split(",") if e.strip())
        
        elif spec.startswith("range:"):
            range_part = spec[6:].strip()
            try:
                l_str, r_str = range_part.split(",")
                L, R = int(l_str.strip()), int(r_str.strip())
                result = set()
                for eid, v1, v2, w in self.edges:
                    if L <= w <= R:
                        result.add(eid)
                return result
            except:
                raise ValueError("Invalid range format")
        
        elif spec.startswith("incident:"):
            vertex_list = spec[9:].strip()
            vertices = set(v.strip() for v in vertex_list.split(",") if v.strip())
            result = set()
            for v in vertices:
                if v in self.incident_map:
                    result.update(self.incident_map[v])
            return result
        
        else:
            raise ValueError("Unknown edge set specification format")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            count_match = re.search(r'predict_count\s*=\s*(\d+)\s*$', raw_ans, re.IGNORECASE)
            if not count_match:
                return False
            predict_count = int(count_match.group(1).strip())
            
            before_count = raw_ans[:count_match.start()].rstrip().rstrip(',').strip()
            
            set_match = re.search(r'predict_set\s*=\s*(.+)$', before_count, re.IGNORECASE)
            if not set_match:
                return False
            predict_set_str = set_match.group(1).strip()
            
            before_set = before_count[:set_match.start()].rstrip().rstrip(',').strip()
            
            hyp_match = re.search(r'hypothesis\s*=\s*(.+)$', before_set, re.IGNORECASE)
            if not hyp_match:
                return False
            hypothesis = hyp_match.group(1).strip()
            
        except Exception:
            return False
        
        try:
            predict_edges = set(e.strip() for e in predict_set_str.split(",") if e.strip())
        except Exception:
            return False
        
        if not predict_edges:
            return False
        
        for eid in predict_edges:
            if eid not in self.edge_map:
                return False
        
        actual_count = self._count_satisfying_edges(predict_edges)
        if predict_count != actual_count:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "query_count_edges" in parsed_info:
            edge_list_str = parsed_info["query_count_edges"].strip()
            try:
                edge_ids = set(e.strip() for e in edge_list_str.split(",") if e.strip())
                self.queried_sets.add(frozenset(edge_ids))
                count = self._count_satisfying_edges(edge_ids)
                return str(count)
            except:
                return "错误：无效的边列表格式。" if self.config.language == "zh" else "Error: Invalid edge list format."
        
        elif "query_count_range" in parsed_info:
            range_str = parsed_info["query_count_range"].strip()
            try:
                l_str, r_str = range_str.split(",")
                L, R = int(l_str.strip()), int(r_str.strip())
                edge_ids = set()
                for eid, v1, v2, w in self.edges:
                    if L <= w <= R:
                        edge_ids.add(eid)
                count = self._count_satisfying_edges(edge_ids)
                return str(count)
            except:
                return "错误：无效的区间格式。" if self.config.language == "zh" else "Error: Invalid range format."
        
        elif "query_count_incident" in parsed_info:
            vertex_list_str = parsed_info["query_count_incident"].strip()
            try:
                vertices = set(v.strip() for v in vertex_list_str.split(",") if v.strip())
                edge_ids = set()
                for v in vertices:
                    if v in self.incident_map:
                        edge_ids.update(self.incident_map[v])
                count = self._count_satisfying_edges(edge_ids)
                return str(count)
            except:
                return "错误：无效的顶点列表。" if self.config.language == "zh" else "Error: Invalid vertex list."
        
        elif "query_single" in parsed_info:
            eid = parsed_info["query_single"].strip()
            if eid not in self.edge_map:
                return "错误：边不存在。" if self.config.language == "zh" else "Error: Edge does not exist."
            weight = self.edge_map[eid][3]
            is_satisfied = self.property_func(weight)
            if self.config.language == "zh":
                return "是" if is_satisfied else "否"
            else:
                return "Yes" if is_satisfied else "No"
        
        elif "query_compare" in parsed_info:
            compare_str = parsed_info["query_compare"].strip()
            try:
                parts = compare_str.split("|")
                if len(parts) != 2:
                    raise ValueError("Need exactly two sets")
                
                set_a = self._parse_edge_set_spec(parts[0].strip())
                set_b = self._parse_edge_set_spec(parts[1].strip())
                
                count_a = self._count_satisfying_edges(set_a)
                count_b = self._count_satisfying_edges(set_b)
                
                if count_a > count_b:
                    return "A>B"
                elif count_a < count_b:
                    return "A<B"
                else:
                    return "A=B"
            except Exception as e:
                return "错误：无效的比较查询格式。" if self.config.language == "zh" else "Error: Invalid comparison query format."
        
        else:
            raise ValueError("No valid query tag found.")
    
    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for eid in self.edge_map:
            query_tag = "query_single"
            query_content = eid
            query_xml = f"<{query_tag}>{query_content}</{query_tag}>"
            
            weight = self.edge_map[eid][3]
            is_satisfied = self.property_func(weight)
            if self.config.language == "zh":
                ans = "是" if is_satisfied else "否"
            else:
                ans = "Yes" if is_satisfied else "No"
            
            queries.append({"query": query_xml, "answer": ans})

        for eid in self.edge_map:
            query_tag = "query_count_edges"
            query_content = eid
            query_xml = f"<{query_tag}>{query_content}</{query_tag}>"
            
            count = self._count_satisfying_edges({eid})
            queries.append({"query": query_xml, "answer": str(count)})

        for vid in self.vertices:
            query_tag = "query_count_incident"
            query_content = vid
            query_xml = f"<{query_tag}>{query_content}</{query_tag}>"
            
            edge_ids = set()
            if vid in self.incident_map:
                edge_ids.update(self.incident_map[vid])
            count = self._count_satisfying_edges(edge_ids)
            
            queries.append({"query": query_xml, "answer": str(count)})
            
        query_tag = "query_count_range"
        query_content = "0,200"
        query_xml = f"<{query_tag}>{query_content}</{query_tag}>"
        
        edge_ids = set()
        for eid, _, _, w in self.edges:
            if 0 <= w <= 200:
                edge_ids.add(eid)
        count = self._count_satisfying_edges(edge_ids)
        queries.append({"query": query_xml, "answer": str(count)})

        return queries

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
        
        if correct == "A>B":
            return "A<B"
        if correct == "A<B":
            return "A>B"
        if correct == "A=B":
            return "A>B"
        
        return correct + "_WRONG"