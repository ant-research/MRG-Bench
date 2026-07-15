from .base import Game
import random
import itertools

class GraphNeighborDiscoveryGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图邻居发现"的推理游戏，规则如下：

游戏设定了一个无向简单图（无自环、无多重边），图有 {n} 个节点，编号为 {node_list}。我已选定了一个特殊节点 B = {target_node}，你的目标是通过查询推断出与 B 直接相邻的所有节点（即 B 的邻居集合）。

你可以反复向我提出以下查询（尽可能用少的次数完成推理），我会根据真实设定如实回答：

1. 子集计数查询：给定一个节点子集 S（不包含 B），询问 S 中有多少个节点是 B 的邻居。回答一个非负整数。
2. 成员确认查询：询问某个具体节点 v（v 不等于 B）是否是 B 的邻居。回答"是"或"否"。注意：此类查询在整局游戏中最多只能使用 2 次。
3. 度数查询：询问 B 的邻居总数（即 B 的度数）。回答一个非负整数。

当你收集足够信息后，请提交最终答案。若答案错误或违反查询次数限制，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 子集计数查询（例如查询节点 1, 3, 5 组成的子集）：
<query_subset>1,3,5</query_subset>

- 成员确认查询（例如查询节点 2）：
<query_member>2</query_member>

- 度数查询（内容为空）：
<query_degree></query_degree>

提交最终答案时，列出所有 B 的邻居节点（用逗号隔开，顺序不限）。如果 B 没有邻居，则提交空集。格式如下：

<answer>1,3,5</answer>

或（若无邻居）：

<answer></answer>
"""

    game_rule_en = """\
Let's play a "Graph Neighbor Discovery" deduction game. Here are the rules:

There is an undirected simple graph (no self-loops, no multi-edges) with {n} nodes, labeled as {node_list}. I have selected a special node B = {target_node}. Your goal is to infer all nodes directly adjacent to B (i.e., B's neighbor set) through queries.

You can repeatedly ask me the following queries (try to complete the inference with as few queries as possible), and I will answer truthfully:

1. Subset Count Query: Given a subset S of nodes (not including B), ask how many nodes in S are neighbors of B. Answer: a non-negative integer.
2. Membership Confirmation Query: Ask whether a specific node v (v not equal to B) is a neighbor of B. Answer: "Yes" or "No". Note: This type of query can be used at most 2 times in the entire game.
3. Degree Query: Ask for the total number of B's neighbors (i.e., B's degree). Answer: a non-negative integer.

When you have enough information, submit your final answer. If the answer is wrong or the query limit is violated, the game fails.

Each query must contain only one tag. Use the following XML format:

- Subset Count Query (e.g., querying subset containing nodes 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Membership Confirmation Query (e.g., querying node 2):
<query_member>2</query_member>

- Degree Query (empty content):
<query_degree></query_degree>

When submitting the final answer, list all neighbor nodes of B (comma-separated, order does not matter). If B has no neighbors, submit an empty set. Format:

<answer>1,3,5</answer>

Or (if no neighbors):

<answer></answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市交通路网拓扑探测系统。
我们设定了一个无向简单路网图（无自环、无多重边），路网有 {n} 个路口，编号为 {node_list}。我已选定了一个特殊的核心交通枢纽 B = {target_node}，你的目标是通过查询推断出与枢纽 B 直接相连的所有路口（即 B 的直达邻接集合）。

你可以反复向我提出以下查询（尽可能用少的次数完成探测），我会根据真实的交通网络设定如实回答：

1. 区域连接统计（子集计数查询）：给定一个路口子集 S（不包含枢纽 B），询问 S 中有多少个路口与枢纽 B 直接相连。回答一个非负整数。
2. 专线状态确认（成员确认查询）：询问某个具体路口 v（v 不等于 B）是否与枢纽 B 直接相连。回答"是"或"否"。注意：此类查询在整局探测中最多只能使用 2 次。
3. 枢纽连通度检测（度数查询）：询问与枢纽 B 直接相连的路口总数（即 B 的节点度数）。回答一个非负整数。

当你收集足够信息后，请提交最终探测结果。若答案错误或违反查询次数限制，系统将判定探测失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 区域连接统计（例如查询路口 1, 3, 5 组成的子集）：
<query_subset>1,3,5</query_subset>

- 专线状态确认（例如查询路口 2）：
<query_member>2</query_member>

- 枢纽连通度检测（内容为空）：
<query_degree></query_degree>

提交最终答案时，列出所有与枢纽 B 直接相连的路口（用逗号隔开，顺序不限）。如果枢纽 B 是孤立节点没有相连路口，则提交空集。格式如下：

<answer>1,3,5</answer>

或（若无相连路口）：

<answer></answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Traffic Network Topology Detection System.
We have set up an undirected simple road network graph (no self-loops, no multi-edges) with {n} intersections, labeled as {node_list}. A specific core traffic hub B = {target_node} has been selected. Your goal is to infer all intersections directly connected to hub B (i.e., B's direct adjacency set) through queries.

You can repeatedly submit the following queries (try to complete the detection with as few queries as possible), and I will answer truthfully based on the actual traffic network configuration:

1. Regional Connection Survey (Subset Count Query): Given a subset S of intersections (not including hub B), ask how many intersections in S are directly connected to B. Answer: a non-negative integer.
2. Direct Route Verification (Membership Confirmation Query): Ask whether a specific intersection v (v not equal to B) is directly connected to B. Answer: "Yes" or "No". Note: This query can be used at most 2 times in the entire detection process.
3. Hub Connectivity Check (Degree Query): Ask for the total number of intersections directly connected to hub B (i.e., B's degree). Answer: a non-negative integer.

When you have gathered enough information, submit your final detection results. If the answer is wrong or the query limit is violated, the detection fails.

Each query must contain only one tag. Use the following XML format:

- Regional Connection Survey (e.g., querying subset containing intersections 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Direct Route Verification (e.g., querying intersection 2):
<query_member>2</query_member>

- Hub Connectivity Check (empty content):
<query_degree></query_degree>

When submitting the final answer, list all intersections directly connected to hub B (comma-separated, order does not matter). If hub B is isolated, submit an empty set. Format:

<answer>1,3,5</answer>

Or (if no connected intersections):

<answer></answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用分子生物学蛋白质互作网络推导系统。
我们设定了一个无向的蛋白质互作图（无自相互作用、无多重结合），网络包含 {n} 种蛋白质，编号为 {node_list}。我已选定了一个特殊靶标蛋白 B = {target_node}，你的目标是通过生化实验查询，推断出与靶标 B 发生直接相互作用的所有蛋白质（即 B 的互作邻居集合）。

你可以反复向我提出以下查询（尽可能用少的实验次数完成推断），我会根据真实的生化实验数据如实回答：

1. 混合物互作计数（子集计数查询）：给定一个蛋白质子集 S（不包含靶标 B），询问 S 中有多少种蛋白质与靶标 B 发生直接相互作用。回答一个非负整数。
2. 特异性结合测试（成员确认查询）：询问某个具体蛋白质 v（v 不等于 B）是否与靶标 B 直接相互作用。回答"是"或"否"。注意：由于高精度试剂昂贵，此类查询在整局实验中最多只能使用 2 次。
3. 靶标结合位点总数（度数查询）：询问与靶标 B 结合的蛋白质总数（即 B 的互作度数）。回答一个非负整数。

当你收集足够信息后，请提交最终互作清单。若答案错误或违反实验次数限制，系统将判定推导失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 混合物互作计数（例如查询蛋白质 1, 3, 5 组成的子集）：
<query_subset>1,3,5</query_subset>

- 特异性结合测试（例如查询蛋白质 2）：
<query_member>2</query_member>

- 靶标结合位点总数（内容为空）：
<query_degree></query_degree>

提交最终答案时，列出所有与靶标 B 直接互作的蛋白质节点（用逗号隔开，顺序不限）。如果靶标 B 无互作蛋白，则提交空集。格式如下：

<answer>1,3,5</answer>

或（若无互作蛋白）：

<answer></answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Molecular Biology Protein Interaction Inference System.
We have configured an undirected protein interaction graph (no self-interactions, no multi-bindings) containing {n} proteins, labeled as {node_list}. A specific target protein B = {target_node} has been selected. Your goal is to infer all proteins that directly interact with target B (i.e., B's interaction neighbor set) through biochemical queries.

You can repeatedly ask the following queries (try to deduce the network with minimal experiments), and I will answer truthfully based on actual biochemical assay data:

1. Batch Interaction Assay (Subset Count Query): Given a subset S of proteins (not including target B), ask how many proteins in S directly interact with B. Answer: a non-negative integer.
2. Specific Binding Test (Membership Confirmation Query): Ask whether a specific protein v (v not equal to B) directly interacts with B. Answer: "Yes" or "No". Note: Due to costly reagents, this test can be used at most 2 times per session.
3. Total Binding Sites Check (Degree Query): Ask for the total number of proteins interacting with target B (i.e., B's interaction degree). Answer: a non-negative integer.

When you have collected enough data, submit your final interaction list. If the answer is wrong or the experiment limit is exceeded, the inference fails.

Each query must contain only one tag. Use the following XML format:

- Batch Interaction Assay (e.g., querying subset containing proteins 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Specific Binding Test (e.g., querying protein 2):
<query_member>2</query_member>

- Total Binding Sites Check (empty content):
<query_degree></query_degree>

When submitting the final answer, list all protein nodes directly interacting with target B (comma-separated, order does not matter). If target B has no interacting proteins, submit an empty set. Format:

<answer>1,3,5</answer>

Or (if no interactions):

<answer></answer>
"""

    contextualized_rule_zh_3 = """\
欢迎访问核心课程先修关联知识图谱分析系统。
我们设定了一个无向的课程关联图（无自我依赖、无重复关联），包含 {n} 个知识模块，编号为 {node_list}。我已选定了一个核心课程模块 B = {target_node}，你的目标是通过查询推断出与核心课程 B 存在直接关联（先修或共修）的所有知识模块（即 B 的关联邻居集合）。

你可以反复向我提出以下查询（尽可能用少的次数完成分析），我会根据真实的教学大纲设定如实回答：

1. 模块集关联统计（子集计数查询）：给定一个知识模块子集 S（不包含核心课程 B），询问 S 中有多少个模块与核心课程 B 存在直接关联。回答一个非负整数。
2. 单一课程关联核实（成员确认查询）：询问某个具体模块 v（v 不等于 B）是否与核心课程 B 存在直接关联。回答"是"或"否"。注意：此类精细核实查询在整局分析中最多只能使用 2 次。
3. 核心课程关联总数（度数查询）：询问与核心课程 B 直接关联的模块总数（即 B 的节点度数）。回答一个非负整数。

当你收集足够信息后，请提交最终的课程关联清单。若答案错误或违反查询次数限制，分析任务失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 模块集关联统计（例如查询模块 1, 3, 5 组成的子集）：
<query_subset>1,3,5</query_subset>

- 单一课程关联核实（例如查询模块 2）：
<query_member>2</query_member>

- 核心课程关联总数（内容为空）：
<query_degree></query_degree>

提交最终答案时，列出所有与核心课程 B 直接关联的模块（用逗号隔开，顺序不限）。如果课程 B 没有关联模块，则提交空集。格式如下：

<answer>1,3,5</answer>

或（若无关联）：

<answer></answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Core Curriculum Prerequisite Knowledge Graph Analysis System.
We have established an undirected course correlation graph (no self-dependencies, no duplicate links) containing {n} knowledge modules, labeled as {node_list}. A core course module B = {target_node} has been identified. Your goal is to deduce all knowledge modules directly related (prerequisites or co-requisites) to course B (i.e., B's related neighbor set) via structured queries.

You may submit the following queries repeatedly (aim to complete the analysis with minimal queries), and I will answer truthfully based on the official syllabus:

1. Module Set Correlation (Subset Count Query): Given a subset S of knowledge modules (not including B), ask how many modules in S are directly related to core course B. Answer: a non-negative integer.
2. Single Course Verification (Membership Confirmation Query): Ask whether a specific module v (v not equal to B) is directly related to core course B. Answer: "Yes" or "No". Note: This specific verification is restricted to a maximum of 2 times during the analysis.
3. Core Course Total Relations (Degree Query): Ask for the total number of modules directly related to core course B (i.e., B's node degree). Answer: a non-negative integer.

Once sufficient information is gathered, submit the final list of correlated courses. Incorrect answers or exceeding query limits will result in an analysis failure.

Each query must contain only one tag. Use the following XML format:

- Module Set Correlation (e.g., querying subset containing modules 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Single Course Verification (e.g., querying module 2):
<query_member>2</query_member>

- Core Course Total Relations (empty content):
<query_degree></query_degree>

When submitting the final answer, list all modules directly related to course B (comma-separated, order does not matter). If course B has no related modules, submit an empty set. Format:

<answer>1,3,5</answer>

Or (if no relations):

<answer></answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用复杂装备装配网络拓扑分析系统。
我们设定了一个无向的零件装配图（无自我连接、无多重接口），整个装配体包含 {n} 个组件，编号为 {node_list}。我已选定了一个核心装配基座 B = {target_node}，你的目标是通过检测指令推断出与基座 B 直接物理连接的所有组件（即 B 的接口邻居集合）。

你可以反复向我发出以下检测指令（尽可能用少的指令次数完成拓扑推演），我会根据真实的CAD装配模型如实回答：

1. 批量接口检测（子集计数查询）：给定一个组件子集 S（不包含基座 B），询问 S 中有多少个组件与基座 B 有直接连接。回答一个非负整数。
2. 单一部件干涉核验（成员确认查询）：询问某个具体组件 v（v 不等于 B）是否与基座 B 直接连接。回答"是"或"否"。注意：此干涉核验耗时较长，整局分析中最多只能使用 2 次。
3. 基座接口总数读取（度数查询）：询问与基座 B 直接连接的组件总数（即 B 的接口度数）。回答一个非负整数。

当你收集足够信息后，请提交最终的装配连接清单。若答案错误或违反检测次数限制，拓扑分析失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 批量接口检测（例如查询组件 1, 3, 5 组成的子集）：
<query_subset>1,3,5</query_subset>

- 单一部件干涉核验（例如查询组件 2）：
<query_member>2</query_member>

- 基座接口总数读取（内容为空）：
<query_degree></query_degree>

提交最终答案时，列出所有与基座 B 直接连接的组件（用逗号隔开，顺序不限）。如果基座 B 无任何连接，则提交空集。格式如下：

<answer>1,3,5</answer>

或（若无连接）：

<answer></answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Complex Equipment Assembly Network Topology Analysis System.
We have mapped an undirected part assembly graph (no self-connections, no multiple interfaces), containing {n} components, labeled as {node_list}. A core assembly base B = {target_node} has been selected. Your goal is to infer all components that are directly physically connected to base B (i.e., B's interface neighbor set) using diagnostic commands.

You can issue the following diagnostic commands repeatedly (try to complete the topology deduction with as few commands as possible), and I will answer truthfully based on the precise CAD assembly model:

1. Batch Interface Detection (Subset Count Query): Given a subset S of components (not including base B), ask how many components in S are directly connected to base B. Answer: a non-negative integer.
2. Single Part Interference Check (Membership Confirmation Query): Ask whether a specific component v (v not equal to B) is directly connected to base B. Answer: "Yes" or "No". Note: This time-consuming interference check can be used at most 2 times per analysis.
3. Base Interface Total Readout (Degree Query): Ask for the total number of components directly connected to base B (i.e., B's interface degree). Answer: a non-negative integer.

When you have collected enough interface data, submit your final assembly connection list. If the answer is incorrect or the command limit is exceeded, the topology analysis fails.

Each query must contain only one tag. Use the following XML format:

- Batch Interface Detection (e.g., querying subset containing components 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Single Part Interference Check (e.g., querying component 2):
<query_member>2</query_member>

- Base Interface Total Readout (empty content):
<query_degree></query_degree>

When submitting the final answer, list all components directly connected to base B (comma-separated, order does not matter). If base B has no connections, submit an empty set. Format:

<answer>1,3,5</answer>

Or (if no connections):

<answer></answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用嫌疑人社会关系网络排查系统。
案件设定了一个无向的接触网络图（排除自我接触、无重复记录），网络中锁定了 {n} 名相关人员，编号为 {node_list}。专案组已确定了一名核心嫌疑人 B = {target_node}，你的目标是通过调阅档案推断出与嫌疑人 B 有过直接接触的所有人员（即 B 的直接联系人集合）。

你可以反复向我提交以下排查申请（尽可能用少的次数完成侦查），我会根据真实的调查卷宗如实回答：

1. 团伙接触排查（子集计数查询）：给定一个人员子集 S（不包含嫌疑人 B），询问 S 中有多少人与嫌疑人 B 有过直接接触。回答一个非负整数。
2. 定向传唤审讯（成员确认查询）：询问某个具体人员 v（v 不等于 B）是否与嫌疑人 B 有过直接接触。回答"是"或"否"。注意：由于传唤权限限制，此类申请在整局排查中最多只能使用 2 次。
3. 核心嫌疑人接触总数（度数查询）：询问与嫌疑人 B 直接接触的人员总数（即 B 的接触度数）。回答一个非负整数。

当你收集足够信息后，请提交最终的同伙接触名单。若答案错误或违反申请次数限制，侦查行动失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 团伙接触排查（例如查询人员 1, 3, 5 组成的子集）：
<query_subset>1,3,5</query_subset>

- 定向传唤审讯（例如查询人员 2）：
<query_member>2</query_member>

- 核心嫌疑人接触总数（内容为空）：
<query_degree></query_degree>

提交最终答案时，列出所有与嫌疑人 B 有过直接接触的人员（用逗号隔开，顺序不限）。如果嫌疑人 B 没有接触者，则提交空集。格式如下：

<answer>1,3,5</answer>

或（若无接触者）：

<answer></answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Suspect Social Network Investigation System.
The case involves an undirected contact network graph (excluding self-contact, no duplicate records), locking in {n} individuals, labeled as {node_list}. The task force has identified a prime suspect B = {target_node}. Your objective is to infer all individuals who have had direct contact with suspect B (i.e., B's direct contact set) by reviewing file queries.

You can repeatedly submit the following investigation requests (complete the reconnaissance with minimal requests), and I will answer truthfully based on official investigation dossiers:

1. Group Contact Screening (Subset Count Query): Given a subset S of individuals (not including suspect B), ask how many people in S have had direct contact with B. Answer: a non-negative integer.
2. Targeted Subpoena Interrogation (Membership Confirmation Query): Ask whether a specific individual v (v not equal to B) had direct contact with B. Answer: "Yes" or "No". Note: Due to subpoena authority limits, this request can be used at most 2 times in the entire investigation.
3. Prime Suspect Total Contacts (Degree Query): Ask for the total number of individuals in direct contact with suspect B (i.e., B's contact degree). Answer: a non-negative integer.

Once you have gathered enough intelligence, submit the final list of accomplices in contact. If the answer is wrong or the request limit is breached, the investigation operation fails.

Each query must contain only one tag. Use the following XML format:

- Group Contact Screening (e.g., querying subset containing individuals 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Targeted Subpoena Interrogation (e.g., querying individual 2):
<query_member>2</query_member>

- Prime Suspect Total Contacts (empty content):
<query_degree></query_degree>

When submitting the final answer, list all individuals who had direct contact with suspect B (comma-separated, order does not matter). If suspect B has no contacts, submit an empty set. Format:

<answer>1,3,5</answer>

Or (if no contacts):

<answer></answer>
"""

    tags = ["answer", "query_subset", "query_member", "query_degree"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "nodes": ["1", "2", "3", "4"],
                "target_node": "1",
                "neighbors": ["2", "3"],
            },
            2: {
                "n": 6,
                "nodes": ["1", "2", "3", "4", "5", "6"],
                "target_node": "3",
                "neighbors": ["1", "4", "5"],
            },
            3: {
                "n": 8,
                "nodes": ["1", "2", "3", "4", "5", "6", "7", "8"],
                "target_node": "4",
                "neighbors": ["1", "2", "6", "8"],
            },
            4: {
                "n": 10,
                "nodes": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                "target_node": "5",
                "neighbors": ["1", "3", "6", "7", "9"],
            },
            5: {
                "n": 12,
                "nodes": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
                "target_node": "6",
                "neighbors": ["2", "3", "5", "8", "10", "11"],
            },
        },
        "en": {
            1: {
                "n": 4,
                "nodes": ["1", "2", "3", "4"],
                "target_node": "1",
                "neighbors": ["2", "3"],
            },
            2: {
                "n": 6,
                "nodes": ["1", "2", "3", "4", "5", "6"],
                "target_node": "3",
                "neighbors": ["1", "4", "5"],
            },
            3: {
                "n": 8,
                "nodes": ["1", "2", "3", "4", "5", "6", "7", "8"],
                "target_node": "4",
                "neighbors": ["1", "2", "6", "8"],
            },
            4: {
                "n": 10,
                "nodes": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                "target_node": "5",
                "neighbors": ["1", "3", "6", "7", "9"],
            },
            5: {
                "n": 12,
                "nodes": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"],
                "target_node": "6",
                "neighbors": ["2", "3", "5", "8", "10", "11"],
            },
        },
    }

    def __init__(self, config):
        self.membership_query_count = 0
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
        self._game_info["node_list"] = ", ".join(cfg["nodes"])
        self._game_info["target_node"] = cfg["target_node"]
        
        self.all_nodes = set(cfg["nodes"])
        self.target_node = cfg["target_node"]
        self.neighbors = set(cfg["neighbors"])

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans == "":
            player_neighbors = set()
        else:
            try:
                player_neighbors = set(x.strip() for x in raw_ans.split(",") if x.strip())
            except:
                return False
        
        valid_nodes = self.all_nodes - {self.target_node}
        if not player_neighbors.issubset(valid_nodes):
            return False
        
        return player_neighbors == self.neighbors

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_invalid = "错误：查询的节点无效或包含节点B。"
        else:
            yes_res, no_res = "Yes", "No"
            error_invalid = "Error: Invalid node or query includes node B."

        if "query_degree" in parsed_info:
            return str(len(self.neighbors))

        elif "query_subset" in parsed_info:
            try:
                raw = parsed_info["query_subset"].strip()
                if raw == "":
                    query_set = set()
                else:
                    query_set = set(x.strip() for x in raw.split(",") if x.strip())
                
                valid_nodes = self.all_nodes - {self.target_node}
                if not query_set.issubset(valid_nodes):
                    return error_invalid
                
                count = len(query_set & self.neighbors)
                return str(count)
            except:
                return error_invalid

        elif "query_member" in parsed_info:
            if self.membership_query_count >= 2:
                if self.config.language == "zh":
                    return "错误：成员确认查询已达上限（最多2次），请使用其他查询类型。"
                else:
                    return "Error: Membership confirmation query limit reached (max 2 times). Please use other query types."
            
            self.membership_query_count += 1
            
            try:
                node = parsed_info["query_member"].strip()
                
                if node == self.target_node or node not in self.all_nodes:
                    return error_invalid
                
                return yes_res if node in self.neighbors else no_res
            except:
                return error_invalid

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            if correct.lower() == "yes":
                return "No" if correct[0].isupper() else "no"
            elif correct.lower() == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        valid_nodes = sorted(list(self.all_nodes - {self.target_node}))

        degree_ans = str(len(self.neighbors))
        results.append({
            "query": "<query_degree></query_degree>",
            "answer": degree_ans
        })

        for node in valid_nodes:
            ans = yes_res if node in self.neighbors else no_res
            results.append({
                "query": f"<query_member>{node}</query_member>",
                "answer": ans
            })

        for r in range(1, len(valid_nodes) + 1):
            if len(valid_nodes) > 4 and 2 < r < len(valid_nodes):
                continue
            for subset_tuple in itertools.combinations(valid_nodes, r):
                if len(subset_tuple) == 0:
                    subset_str = ""
                else:
                    subset_str = ",".join(subset_tuple)
                
                query_xml = f"<query_subset>{subset_str}</query_subset>"
                
                count = 0
                for node in subset_tuple:
                    if node in self.neighbors:
                        count += 1
                
                results.append({
                    "query": query_xml,
                    "answer": str(count)
                })

        return results