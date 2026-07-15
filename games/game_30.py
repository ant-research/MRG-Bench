import re
import random
from typing import List, Tuple, Set, Dict
from .base import Game

class GraphPathQueryGame(Game):

    game_rule_zh = """\
我们来玩一个"图边权推理"游戏，规则如下：

游戏设定了一个无向连通图，包含 {n} 个节点（编号 1 到 {n}）和若干条边。图的结构（即节点和边的连接关系）是公开的：
{edges_info}

目标边：{target_edge}

每条边都有一个未知的正整数权重，权重范围在 [{L}, {U}] 之间。你的目标是推断出目标边的权重。

1. **路径查询**：你可以询问一条路径上所有边的权重之和。
   - 路径必须至少包含 2 条边（即至少 3 个节点）。
   - 路径上的边必须在图中存在。
   - 路径必须是简单路径（除非首尾节点相同形成简单环，否则中间节点不能重复）。
   - 如果首尾节点相同，则构成简单环（除首尾外节点不重复，且至少包含 3 条边）。

2. **提交答案**：当你有足够信心时，提交目标边的权重。
   - 你必须至少完成 3 次有效查询后才能提交答案。
   - 你最多可以进行 {Q} 次有效查询。
   - 答案错误则游戏失败。

每次只能包含一个操作标签。

- **路径查询**（例如查询路径 1->2->3->4）：
<query_path>1,2,3,4</query_path>

- **提交答案**（例如认为目标边权重为 5）：
<answer>5</answer>

注意：
- 路径节点用英文逗号分隔，节点编号必须在 1 到 {n} 之间。
- 非法查询（边不存在、路径不简单、长度不足等）不会返回有效信息，也不会影响查询次数，但仍请仔细检查。
- 你需要通过尽可能少的查询次数推断出目标边的权重。
"""

    game_rule_en = """\
Let's play a "Graph Edge Weight Inference" game. Here are the rules:

The game is set on an undirected connected graph with {n} nodes (numbered 1 to {n}) and several edges. The graph structure (i.e., which nodes are connected by edges) is public:
{edges_info}

Target edge: {target_edge}

Each edge has an unknown positive integer weight in the range [{L}, {U}]. Your goal is to infer the weight of the target edge.

1. **Path Query**: You can ask for the sum of weights of all edges on a path.
   - The path must contain at least 2 edges (i.e., at least 3 nodes).
   - All edges in the path must exist in the graph.
   - The path must be simple (no repeated intermediate nodes, unless the first and last nodes are the same forming a simple cycle).
   - If the first and last nodes are the same, it forms a simple cycle (no repeated nodes except endpoints, at least 3 edges).

2. **Submit Answer**: When you are confident, submit the weight of the target edge.
   - You must complete at least 3 valid queries before submitting.
   - You can perform at most {Q} valid queries.
   - An incorrect answer results in game failure.

Each operation must contain only one tag.

- **Path Query** (e.g., query path 1->2->3->4):
<query_path>1,2,3,4</query_path>

- **Submit Answer** (e.g., if you think the target edge weight is 5):
<answer>5</answer>

Notes:
- Path nodes are separated by commas, node IDs must be between 1 and {n}.
- Invalid queries (non-existent edges, non-simple paths, insufficient length, etc.) will not return valid information and will not count towards your query limit, but please still check carefully.
- You need to infer the target edge weight with as few queries as possible.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通路网耗时分析系统”。我们将对城市核心路网的通行效率进行评估。

系统接入了一个连通路网，包含 {n} 个交通枢纽（编号 1 到 {n}）和若干条互联公路。路网结构（即枢纽和公路的连接关系）是公开的：
{edges_info}

目标待测路段：{target_edge}

每条公路的实际通行耗时（分钟）为未知正整数，耗时范围在 [{L}, {U}] 之间。你的目标是推断出目标路段的准确耗时。

1. **行程查询**：你可以询问一条连续行程路线上所有公路的耗时之和。
   - 行程必须至少包含 2 条公路（即至少经过 3 个枢纽）。
   - 行程上的公路必须在路网中存在。
   - 行程必须是简单路径（除非首尾枢纽相同形成简单环路，否则中间枢纽不能重复经过）。
   - 如果首尾枢纽相同，则构成简单环路（除首尾外枢纽不重复，且至少包含 3 条公路）。

2. **提交评估**：当你有足够信心时，提交目标路段的耗时评估结果。
   - 你必须至少完成 3 次有效查询后才能提交答案。
   - 你最多可以进行 {Q} 次有效查询。
   - 结果错误则评估失败。

每次只能包含一个操作标签。

- **行程查询**（例如查询行程 1->2->3->4）：
<query_path>1,2,3,4</query_path>

- **提交评估**（例如认为目标路段耗时为 5 分钟）：
<answer>5</answer>

注意：
- 行程枢纽用英文逗号分隔，枢纽编号必须在 1 到 {n} 之间。
- 非法查询（公路不存在、行程不简单、长度不足等）不会返回有效信息，也不会影响查询次数，但仍请仔细检查。
- 你需要通过尽可能少的查询次数推断出目标路段的耗时。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Transit Time Analysis System". We are evaluating the transit efficiency of the core urban road network.

The system features a connected road network with {n} traffic hubs (numbered 1 to {n}) and several interconnected highways. The network structure (i.e., the connections between hubs and highways) is public:
{edges_info}

Target highway for evaluation: {target_edge}

Each highway has an unknown positive integer transit time (in minutes) in the range [{L}, {U}]. Your goal is to infer the exact transit time of the target highway.

1. **Route Query**: You can ask for the sum of transit times of all highways on a continuous route.
   - The route must contain at least 2 highways (i.e., at least 3 hubs).
   - All highways in the route must exist in the network.
   - The route must be a simple path (no repeated intermediate hubs, unless the first and last hubs are the same forming a simple cycle).
   - If the first and last hubs are the same, it forms a simple cycle (no repeated hubs except endpoints, at least 3 highways).

2. **Submit Evaluation**: When you are confident, submit the transit time of the target highway.
   - You must complete at least 3 valid queries before submitting.
   - You can perform at most {Q} valid queries.
   - An incorrect answer results in evaluation failure.

Each operation must contain only one tag.

- **Route Query** (e.g., query route 1->2->3->4):
<query_path>1,2,3,4</query_path>

- **Submit Evaluation** (e.g., if you think the target highway transit time is 5 minutes):
<answer>5</answer>

Notes:
- Route hubs are separated by commas, hub IDs must be between 1 and {n}.
- Invalid queries (non-existent highways, non-simple routes, insufficient length, etc.) will not return valid information and will not count towards your query limit, but please still check carefully.
- You need to infer the target highway transit time with as few queries as possible.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“医疗生化传导分析系统”。本系统用于测定人体特定生理代谢通路的反应延迟。

系统中建立了一个生化网络模型，包含 {n} 个生化指标/器官（编号 1 到 {n}）及若干条代谢通路。网络结构是公开的：
{edges_info}

目标测定通路：{target_edge}

每条代谢通路的反应延迟（毫秒）为未知正整数，范围在 [{L}, {U}] 之间。你的任务是精确推断出目标通路的反应延迟。

1. **链路查询**：你可以询问一条连续的级联反应链路上所有通路的延迟总和。
   - 链路必须至少包含 2 条通路（即至少涉及 3 个指标）。
   - 链路上的通路必须在网络中存在。
   - 链路必须是简单路径（除非首尾指标相同形成简单循环通路，否则中间指标不能重复）。
   - 如果首尾指标相同，则构成简单循环通路（除首尾外指标不重复，且至少包含 3 条通路）。

2. **提交诊断**：当你有足够信心时，提交目标通路的反应延迟结果。
   - 你必须至少完成 3 次有效查询后才能提交答案。
   - 你最多可以进行 {Q} 次有效查询。
   - 结果错误则诊断失败。

每次只能包含一个操作标签。

- **链路查询**（例如查询链路 1->2->3->4）：
<query_path>1,2,3,4</query_path>

- **提交诊断**（例如认为目标通路延迟为 5 毫秒）：
<answer>5</answer>

注意：
- 链路指标用英文逗号分隔，编号必须在 1 到 {n} 之间。
- 非法查询（通路不存在、链路不简单、长度不足等）不会返回有效信息，也不会影响查询次数，但仍请仔细检查。
- 你需要通过尽可能少的查询次数推断出目标通路的反应延迟。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Medical Biochemical Conduction Analysis System". This system is used to determine the reaction delay of specific physiological metabolic pathways.

The system features a biochemical network model with {n} biochemical indicators/organs (numbered 1 to {n}) and several metabolic pathways. The network structure is public:
{edges_info}

Target pathway for determination: {target_edge}

The reaction delay (in milliseconds) of each metabolic pathway is an unknown positive integer in the range [{L}, {U}]. Your task is to accurately infer the reaction delay of the target pathway.

1. **Link Query**: You can ask for the total delay of all pathways on a continuous cascade reaction link.
   - The link must contain at least 2 pathways (i.e., at least 3 indicators).
   - All pathways in the link must exist in the network.
   - The link must be a simple path (no repeated intermediate indicators, unless the first and last indicators are the same forming a simple cycle).
   - If the first and last indicators are the same, it forms a simple cycle (no repeated indicators except endpoints, at least 3 pathways).

2. **Submit Diagnosis**: When you are confident, submit the reaction delay of the target pathway.
   - You must complete at least 3 valid queries before submitting.
   - You can perform at most {Q} valid queries.
   - An incorrect answer results in diagnosis failure.

Each operation must contain only one tag.

- **Link Query** (e.g., query link 1->2->3->4):
<query_path>1,2,3,4</query_path>

- **Submit Diagnosis** (e.g., if you think the target pathway delay is 5 ms):
<answer>5</answer>

Notes:
- Link indicators are separated by commas, IDs must be between 1 and {n}.
- Invalid queries (non-existent pathways, non-simple links, insufficient length, etc.) will not return valid information and will not count towards your query limit, but please still check carefully.
- You need to infer the target pathway reaction delay with as few queries as possible.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“教育图谱学时规划系统”。本系统协助评估完成进阶学习所需的标准时间。

系统载入了知识图谱，包含 {n} 个知识模块（编号 1 到 {n}）及若干条学习关联路径。图谱结构是公开的：
{edges_info}

目标评估路径：{target_edge}

掌握每条学习关联路径所需的标准学时（小时）为未知正整数，范围在 [{L}, {U}] 之间。你的任务是推断出目标路径的确切学时。

1. **轨迹查询**：你可以询问一条连续学习轨迹上所有路径的学时总和。
   - 轨迹必须至少包含 2 条学习路径（即至少覆盖 3 个知识模块）。
   - 轨迹上的路径必须在图谱中存在。
   - 轨迹必须是简单路径（除非首尾模块相同形成简单闭环复习，否则中间模块不能重复）。
   - 如果首尾模块相同，则构成简单闭环复习（除首尾外模块不重复，且至少包含 3 条路径）。

2. **提交规划**：当你有足够信心时，提交目标路径的学时评估结果。
   - 你必须至少完成 3 次有效查询后才能提交答案。
   - 你最多可以进行 {Q} 次有效查询。
   - 结果错误则规划失败。

每次只能包含一个操作标签。

- **轨迹查询**（例如查询轨迹 1->2->3->4）：
<query_path>1,2,3,4</query_path>

- **提交规划**（例如认为目标路径需 5 小时）：
<answer>5</answer>

注意：
- 轨迹模块用英文逗号分隔，编号必须在 1 到 {n} 之间。
- 非法查询（路径不存在、轨迹不简单、跨度不足等）不会返回有效信息，也不会影响查询次数，但仍请仔细检查。
- 你需要通过尽可能少的查询次数推断出目标路径的学时。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Educational Knowledge Graph Study Time Planning System". This system assists in evaluating the standard time required to complete advanced learning.

The system loads a knowledge graph with {n} knowledge modules (numbered 1 to {n}) and several learning association paths. The graph structure is public:
{edges_info}

Target path for evaluation: {target_edge}

The standard study time (in hours) required to master each learning association path is an unknown positive integer in the range [{L}, {U}]. Your task is to infer the exact study time of the target path.

1. **Trajectory Query**: You can ask for the total study time of all paths on a continuous learning trajectory.
   - The trajectory must contain at least 2 paths (i.e., at least 3 modules).
   - All paths in the trajectory must exist in the graph.
   - The trajectory must be a simple path (no repeated intermediate modules, unless the first and last modules are the same forming a simple review cycle).
   - If the first and last modules are the same, it forms a simple review cycle (no repeated modules except endpoints, at least 3 paths).

2. **Submit Plan**: When you are confident, submit the study time evaluation of the target path.
   - You must complete at least 3 valid queries before submitting.
   - You can perform at most {Q} valid queries.
   - An incorrect answer results in planning failure.

Each operation must contain only one tag.

- **Trajectory Query** (e.g., query trajectory 1->2->3->4):
<query_path>1,2,3,4</query_path>

- **Submit Plan** (e.g., if you think the target path requires 5 hours):
<answer>5</answer>

Notes:
- Trajectory modules are separated by commas, IDs must be between 1 and {n}.
- Invalid queries (non-existent paths, non-simple trajectories, insufficient span, etc.) will not return valid information and will not count towards your query limit, but please still check carefully.
- You need to infer the target path study time with as few queries as possible.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业流水线能耗监测系统”。本系统专门用于监控生产车间各流转环节的能源消耗。

系统中配置了一个车间流水线模型，包含 {n} 个生产工位（编号 1 到 {n}）和若干条传输流水线。模型结构是公开的：
{edges_info}

目标监测流水线：{target_edge}

每条传输流水线的流转能耗（千瓦时）为未知正整数，范围在 [{L}, {U}] 之间。你的任务是推测出目标流水线的准确能耗。

1. **流程查询**：你可以询问一条连续工艺流程上所有流水线的能耗总计。
   - 流程必须至少包含 2 条流水线（即经过至少 3 个生产工位）。
   - 流程上的流水线必须在模型中存在。
   - 流程必须是简单路径（除非首尾工位相同形成简单循环加工，否则中间工位不能重复经过）。
   - 如果首尾工位相同，则构成简单循环加工（除首尾外工位不重复，且至少包含 3 条流水线）。

2. **提交监测**：当你有足够信心时，提交目标流水线的能耗数据。
   - 你必须至少完成 3 次有效查询后才能提交答案。
   - 你最多可以进行 {Q} 次有效查询。
   - 结果错误则监测失败。

每次只能包含一个操作标签。

- **流程查询**（例如查询流程 1->2->3->4）：
<query_path>1,2,3,4</query_path>

- **提交监测**（例如认为目标流水线能耗为 5 千瓦时）：
<answer>5</answer>

注意：
- 流程工位用英文逗号分隔，编号必须在 1 到 {n} 之间。
- 非法查询（流水线不存在、流程不简单、长度不足等）不会返回有效信息，也不会影响查询次数，但仍请仔细检查。
- 你需要通过尽可能少的查询次数推断出目标流水线的能耗。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Industrial Assembly Line Energy Monitoring System". This system is dedicated to monitoring the energy consumption of transfer steps in the production workshop.

The system is configured with a workshop assembly model, containing {n} production stations (numbered 1 to {n}) and several transfer assembly lines. The model structure is public:
{edges_info}

Target assembly line for monitoring: {target_edge}

The transfer energy consumption (in kWh) of each assembly line is an unknown positive integer in the range [{L}, {U}]. Your task is to deduce the exact energy consumption of the target assembly line.

1. **Flow Query**: You can ask for the total energy consumption of all assembly lines on a continuous process flow.
   - The flow must contain at least 2 assembly lines (i.e., passing through at least 3 stations).
   - All assembly lines in the flow must exist in the model.
   - The flow must be a simple path (no repeated intermediate stations, unless the first and last stations are the same forming a simple cyclic process).
   - If the first and last stations are the same, it forms a simple cyclic process (no repeated stations except endpoints, at least 3 assembly lines).

2. **Submit Monitoring**: When you are confident, submit the energy consumption data of the target assembly line.
   - You must complete at least 3 valid queries before submitting.
   - You can perform at most {Q} valid queries.
   - An incorrect answer results in monitoring failure.

Each operation must contain only one tag.

- **Flow Query** (e.g., query flow 1->2->3->4):
<query_path>1,2,3,4</query_path>

- **Submit Monitoring** (e.g., if you think the target energy consumption is 5 kWh):
<answer>5</answer>

Notes:
- Flow stations are separated by commas, IDs must be between 1 and {n}.
- Invalid queries (non-existent assembly lines, non-simple flows, insufficient length, etc.) will not return valid information and will not count towards your query limit, but please still check carefully.
- You need to infer the target assembly line energy consumption with as few queries as possible.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法程序流转周期审计系统”。本系统负责核查案件在各法律程序阶段间的流转效率。

系统记录了一套司法流转网络，包含 {n} 个法律程序阶段（编号 1 到 {n}）及若干个案件流转环节。网络结构是公开的：
{edges_info}

目标审计环节：{target_edge}

每个案件流转环节的审查周期（天）为未知正整数，周期范围在 [{L}, {U}] 之间。你的使命是查明目标环节的具体审查天数。

1. **序列查询**：你可以调阅一段连续司法流转序列上所有环节的审查周期总和。
   - 序列必须至少包含 2 个流转环节（即覆盖至少 3 个程序阶段）。
   - 序列上的环节必须在网络中存在。
   - 序列必须是简单路径（除非首尾阶段相同形成简单发回重审，否则中间阶段不能重复进入）。
   - 如果首尾阶段相同，则构成简单发回重审（除首尾外阶段不重复，且至少包含 3 个环节）。

2. **提交审计**：当你有足够确凿的证据时，提交目标环节的周期结论。
   - 你必须至少完成 3 次有效查询后才能提交答案。
   - 你最多可以发起 {Q} 次有效查询。
   - 结论错误则审计失败。

每次只能包含一个操作标签。

- **序列查询**（例如调阅序列 1->2->3->4）：
<query_path>1,2,3,4</query_path>

- **提交审计**（例如认定目标环节周期为 5 天）：
<answer>5</answer>

注意：
- 序列阶段用英文逗号分隔，阶段编号必须在 1 到 {n} 之间。
- 非法查询（环节不存在、序列不简单、跨度不足等）不会返回有效信息，也不会占用查询额度，但仍请仔细检查。
- 你需要通过尽可能少的查询次数查明目标环节的审查周期。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Process Transfer Cycle Audit System". This system is responsible for verifying the transfer efficiency of cases between various legal procedure stages.

The system records a judicial transfer network, containing {n} legal procedure stages (numbered 1 to {n}) and several case transfer steps. The network structure is public:
{edges_info}

Target step for audit: {target_edge}

The review cycle (in days) of each case transfer step is an unknown positive integer in the range [{L}, {U}]. Your mission is to ascertain the exact review days of the target step.

1. **Sequence Query**: You can request the total review cycle of all steps on a continuous judicial transfer sequence.
   - The sequence must contain at least 2 transfer steps (i.e., covering at least 3 stages).
   - All steps in the sequence must exist in the network.
   - The sequence must be a simple path (no repeated intermediate stages, unless the first and last stages are the same forming a simple remand for retrial).
   - If the first and last stages are the same, it forms a simple remand for retrial (no repeated stages except endpoints, at least 3 steps).

2. **Submit Audit**: When you have sufficiently conclusive evidence, submit the cycle conclusion of the target step.
   - You must complete at least 3 valid queries before submitting.
   - You can initiate at most {Q} valid queries.
   - An incorrect conclusion results in audit failure.

Each operation must contain only one tag.

- **Sequence Query** (e.g., request sequence 1->2->3->4):
<query_path>1,2,3,4</query_path>

- **Submit Audit** (e.g., if you conclude the target step cycle is 5 days):
<answer>5</answer>

Notes:
- Sequence stages are separated by commas, stage IDs must be between 1 and {n}.
- Invalid queries (non-existent steps, non-simple sequences, insufficient span, etc.) will not return valid information and will not consume your query quota, but please still check carefully.
- You need to ascertain the target step review cycle with as few queries as possible.
"""

    tags = ["answer", "query_path"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)],
                "target_edge": (1, 3),
                "weights": {(1, 2): 3, (2, 3): 4, (3, 4): 5, (4, 1): 2, (1, 3): 6},
                "L": 1, "U": 9, "Q": 15
            },
            2: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3), (3, 5)],
                "target_edge": (3, 5),
                "weights": {(1, 2): 2, (2, 3): 5, (3, 4): 3, (4, 5): 7, (5, 1): 4, (1, 3): 6, (3, 5): 8},
                "L": 1, "U": 9, "Q": 18
            },
            3: {
                "n": 6,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (1, 3), (3, 5), (2, 4), (4, 6)],
                "target_edge": (2, 4),
                "weights": {(1, 2): 3, (2, 3): 5, (3, 4): 4, (4, 5): 6, (5, 6): 2, (6, 1): 7, 
                           (1, 3): 8, (3, 5): 9, (2, 4): 5, (4, 6): 3},
                "L": 1, "U": 9, "Q": 20
            },
            4: {
                "n": 7,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1), 
                         (1, 3), (3, 5), (5, 7), (2, 4), (4, 6), (6, 1)],
                "target_edge": (4, 6),
                "weights": {(1, 2): 4, (2, 3): 6, (3, 4): 3, (4, 5): 7, (5, 6): 5, (6, 7): 8, (7, 1): 2,
                           (1, 3): 9, (3, 5): 4, (5, 7): 6, (2, 4): 5, (4, 6): 7, (6, 1): 3},
                "L": 1, "U": 9, "Q": 22
            },
            5: {
                "n": 8,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1),
                         (1, 3), (3, 5), (5, 7), (7, 1), (2, 4), (4, 6), (6, 8), (8, 2), (1, 5), (2, 6)],
                "target_edge": (1, 5),
                "weights": {(1, 2): 5, (2, 3): 7, (3, 4): 4, (4, 5): 6, (5, 6): 8, (6, 7): 3, (7, 8): 5, (8, 1): 9,
                           (1, 3): 6, (3, 5): 7, (5, 7): 4, (7, 1): 8, (2, 4): 5, (4, 6): 9, (6, 8): 6, (8, 2): 4,
                           (1, 5): 7, (2, 6): 8},
                "L": 1, "U": 9, "Q": 25
            }
        },
        "en": {
            1: {
                "n": 4,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)],
                "target_edge": (1, 3),
                "weights": {(1, 2): 3, (2, 3): 4, (3, 4): 5, (4, 1): 2, (1, 3): 6},
                "L": 1, "U": 9, "Q": 15
            },
            2: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3), (3, 5)],
                "target_edge": (3, 5),
                "weights": {(1, 2): 2, (2, 3): 5, (3, 4): 3, (4, 5): 7, (5, 1): 4, (1, 3): 6, (3, 5): 8},
                "L": 1, "U": 9, "Q": 18
            },
            3: {
                "n": 6,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 1), (1, 3), (3, 5), (2, 4), (4, 6)],
                "target_edge": (2, 4),
                "weights": {(1, 2): 3, (2, 3): 5, (3, 4): 4, (4, 5): 6, (5, 6): 2, (6, 1): 7, 
                           (1, 3): 8, (3, 5): 9, (2, 4): 5, (4, 6): 3},
                "L": 1, "U": 9, "Q": 20
            },
            4: {
                "n": 7,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 1), 
                         (1, 3), (3, 5), (5, 7), (2, 4), (4, 6), (6, 1)],
                "target_edge": (4, 6),
                "weights": {(1, 2): 4, (2, 3): 6, (3, 4): 3, (4, 5): 7, (5, 6): 5, (6, 7): 8, (7, 1): 2,
                           (1, 3): 9, (3, 5): 4, (5, 7): 6, (2, 4): 5, (4, 6): 7, (6, 1): 3},
                "L": 1, "U": 9, "Q": 22
            },
            5: {
                "n": 8,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 1),
                         (1, 3), (3, 5), (5, 7), (7, 1), (2, 4), (4, 6), (6, 8), (8, 2), (1, 5), (2, 6)],
                "target_edge": (1, 5),
                "weights": {(1, 2): 5, (2, 3): 7, (3, 4): 4, (4, 5): 6, (5, 6): 8, (6, 7): 3, (7, 8): 5, (8, 1): 9,
                           (1, 3): 6, (3, 5): 7, (5, 7): 4, (7, 1): 8, (2, 4): 5, (4, 6): 9, (6, 8): 6, (8, 2): 4,
                           (1, 5): 7, (2, 6): 8},
                "L": 1, "U": 9, "Q": 25
            }
        }
    }

    def __init__(self, config):
        self.valid_query_count = 0
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
        self._game_info["L"] = cfg["L"]
        self._game_info["U"] = cfg["U"]
        self._game_info["Q"] = cfg["Q"]
        
        self.edges = cfg["edges"]
        self.target_edge = cfg["target_edge"]
        self.weights = cfg["weights"]
        
        self.edge_set = set()
        for u, v in self.edges:
            self.edge_set.add((u, v))
            self.edge_set.add((v, u))
            if (u, v) in self.weights:
                self.weights[(v, u)] = self.weights[(u, v)]
            elif (v, u) in self.weights:
                self.weights[(u, v)] = self.weights[(v, u)]
        
        edges_str_list = [f"({u}, {v})" for u, v in sorted(self.edges)]
        if lang == "zh":
            self._game_info["edges_info"] = "边：" + ", ".join(edges_str_list)
            self._game_info["target_edge"] = f"({self.target_edge[0]}, {self.target_edge[1]})"
        else:
            self._game_info["edges_info"] = "Edges: " + ", ".join(edges_str_list)
            self._game_info["target_edge"] = f"({self.target_edge[0]}, {self.target_edge[1]})"

    def _is_valid_path(self, path: List[int]) -> Tuple[bool, str]:
        lang = self.config.language
        
        if len(path) < 3:
            if lang == "zh":
                return False, "路径长度不足，至少需要3个节点（2条边）"
            else:
                return False, "Path too short, at least 3 nodes (2 edges) required"
        
        n = self._game_info["n"]
        for node in path:
            if node < 1 or node > n:
                if lang == "zh":
                    return False, f"节点 {node} 超出范围 [1, {n}]"
                else:
                    return False, f"Node {node} out of range [1, {n}]"
        
        for i in range(len(path) - 1):
            if (path[i], path[i+1]) not in self.edge_set:
                if lang == "zh":
                    return False, f"边 ({path[i]}, {path[i+1]}) 不存在"
                else:
                    return False, f"Edge ({path[i]}, {path[i+1]}) does not exist"
        
        is_cycle = (path[0] == path[-1])
        if is_cycle:
            middle_nodes = path[1:-1]
            if len(middle_nodes) != len(set(middle_nodes)):
                if lang == "zh":
                    return False, "路径不是简单环（中间节点有重复）"
                else:
                    return False, "Path is not a simple cycle (repeated intermediate nodes)"
        else:
            if len(path) != len(set(path)):
                if lang == "zh":
                    return False, "路径不是简单路径（节点有重复）"
                else:
                    return False, "Path is not simple (repeated nodes)"
        
        return True, ""

    def _calculate_path_weight(self, path: List[int]) -> int:
        total = 0
        for i in range(len(path) - 1):
            edge = (path[i], path[i+1])
            total += self.weights[edge]
        return total

    def evaluate(self, parsed_info):
        lang = self.config.language
        
        if self.valid_query_count < 3:
            if lang == "zh":
                raise ValueError(f"至少需要3次有效查询后才能提交答案，当前有效查询次数：{self.valid_query_count}")
            else:
                raise ValueError(f"At least 3 valid queries required before submitting, current: {self.valid_query_count}")
        
        try:
            answer = int(parsed_info["answer"].strip())
        except ValueError:
            if lang == "zh":
                raise ValueError("答案格式错误，必须是整数")
            else:
                raise ValueError("Invalid answer format, must be an integer")
        
        target_weight = self.weights.get(self.target_edge) or self.weights.get((self.target_edge[1], self.target_edge[0]))
        
        return answer == target_weight

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "query_path" not in parsed_info:
            if lang == "zh":
                return "错误：未找到有效的查询标签"
            else:
                return "Error: No valid query tag found"
        
        if self.valid_query_count >= self._game_info["Q"]:
            if lang == "zh":
                return f"错误：已达到最大查询次数限制 {self._game_info['Q']}"
            else:
                return f"Error: Maximum query limit {self._game_info['Q']} reached"
        
        try:
            path_str = parsed_info["query_path"].strip()
            path = [int(x.strip()) for x in path_str.split(",")]
        except:
            if lang == "zh":
                return "错误：路径格式无效，应为用逗号分隔的节点编号"
            else:
                return "Error: Invalid path format, should be comma-separated node IDs"
        
        is_valid, error_msg = self._is_valid_path(path)
        if not is_valid:
            if lang == "zh":
                return f"无效查询：{error_msg}"
            else:
                return f"Invalid query: {error_msg}"
        
        self.valid_query_count += 1
        
        weight_sum = self._calculate_path_weight(path)
        
        if lang == "zh":
            return f"路径权重和：{weight_sum}（有效查询次数：{self.valid_query_count}/{self._game_info['Q']}）"
        else:
            return f"Path weight sum: {weight_sum} (Valid queries: {self.valid_query_count}/{self._game_info['Q']})"

    def get_all_possible_queries(self) -> List[Dict]:
        results = []
        n = self._game_info["n"]
        lang = self.config.language
        
        adj = {i: [] for i in range(1, n + 1)}
        for u, v in self.edge_set:
            adj[u].append(v)
            
        def dfs(current_path):
            if len(results) > 10000:
                return
                
            curr_node = current_path[-1]
            
            if len(current_path) >= 3:
                path_str = ",".join(map(str, current_path))
                weight_sum = self._calculate_path_weight(current_path)
                
                if lang == "zh":
                    ans = f"路径权重和：{weight_sum}"
                else:
                    ans = f"Path weight sum: {weight_sum}"
                
                results.append({
                    "query": f"<query_path>{path_str}</query_path>",
                    "answer": ans
                })
            
            for neighbor in adj[curr_node]:
                if neighbor == current_path[0]:
                    if len(current_path) >= 3:
                        cycle_path = current_path + [neighbor]
                        path_str = ",".join(map(str, cycle_path))
                        weight_sum = self._calculate_path_weight(cycle_path)
                        
                        if lang == "zh":
                            ans = f"路径权重和：{weight_sum}"
                        else:
                            ans = f"Path weight sum: {weight_sum}"
                        
                        results.append({
                            "query": f"<query_path>{path_str}</query_path>",
                            "answer": ans
                        })
                
                elif neighbor not in current_path:
                    dfs(current_path + [neighbor])
        
        for start_node in range(1, n + 1):
            dfs([start_node])
            
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        import re as _re
        
        
        num_match = _re.search(r'(?:Path weight sum|路径权重和)[：:]\s*(\d+)', correct)
        if num_match:
            original_val = int(num_match.group(1))
            wrong_val = original_val + random.choice([1, 2, -1, -2])
            if wrong_val < self._game_info["L"]:
                wrong_val = original_val + 2
            return correct.replace(str(original_val), str(wrong_val), 1)
        
        stripped = correct.strip()
        if stripped.isdigit() or (stripped.startswith('-') and stripped[1:].isdigit()):
            return str(int(stripped) + 1)
        
        return correct + " [INCORRECT]"