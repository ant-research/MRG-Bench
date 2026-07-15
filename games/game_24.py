from .base import Game
import random

class TreeParameterIdentificationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"交互式树参数识别"游戏，规则如下：

游戏设定了一棵固定的、有限的有根树。节点总数为 N（未知）。根节点 ID 为 1，所有节点用不重复的整数 ID 标记，范围为 1 到 N。

对于每个节点 i，定义 c(i) 为其子节点数：
- 叶节点满足 c(i) = 0
- 非叶节点满足 c(i) 大于 0

游戏提供以下公理供你推理：
- 树的边数为 N - 1
- 所有节点的子节点数之和等于 N - 1
- 叶节点总数 L 加上非叶节点数 I 等于 N

初始状态：你仅知道根节点 ID=1 存在，其余节点未知。

你的目标是通过查询确定叶节点的总数 L。

每轮你可以提出以下查询（每次只能包含一个查询标签）：

1. 询问总节点数：
<query_total></query_total>

2. 查询某个节点的子节点信息（仅限已知但未查询过的节点）：
<query_node>节点ID</query_node>

3. 复查已查询节点的记录：
<query_record>节点ID</query_record>

4. 查询当前已发现的所有节点ID：
<query_known></query_known>

5. 查询已查询过的节点数量：
<query_explored_count></query_explored_count>

6. 查询已查询节点的子节点数总和：
<query_children_sum></query_children_sum>

当你确定答案后，使用以下格式提交：
<answer>叶节点总数</answer>

例如：
<answer>5</answer>

注意：答案只有一次提交机会，请确保你的推理正确后再提交。
"""

    game_rule_en = """\
Let's play a "Tree Parameter Identification" game with the following rules:

There is a fixed, finite rooted tree. The total number of nodes is N (unknown). The root node has ID 1, and all nodes are labeled with unique integer IDs ranging from 1 to N.

For each node i, define c(i) as its number of children:
- Leaf nodes satisfy c(i) = 0
- Non-leaf nodes satisfy c(i) greater than 0

The following axioms are provided for reasoning:
- The number of edges is N - 1
- The sum of all nodes' children counts equals N - 1
- The number of leaf nodes L plus the number of internal nodes I equals N

Initial state: You only know that the root node ID=1 exists; other nodes are unknown.

Your goal is to determine the total number of leaf nodes L through queries.

Each turn you can make one of the following queries (only one query tag per turn):

1. Ask for the total number of nodes:
<query_total></query_total>

2. Query a node's children information (only for known but not yet queried nodes):
<query_node>NodeID</query_node>

3. Review the record of an already queried node:
<query_record>NodeID</query_record>

4. Query all currently known node IDs:
<query_known></query_known>

5. Query the count of explored nodes:
<query_explored_count></query_explored_count>

6. Query the sum of children counts of explored nodes:
<query_children_sum></query_children_sum>

When you are ready to submit your answer, use:
<answer>NumberOfLeafNodes</answer>

For example:
<answer>5</answer>

Note: You only have one chance to submit the answer. Make sure your reasoning is correct before submission.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行"交通线网末端站点排查"系统操作，规则如下：

系统映射了一个区域的交通线网，该线网呈严格的单向分支树状结构分布。站点总数为 N（未知）。中心交通枢纽站 ID 为 1，所有站点用不重复的整数 ID 标记，范围为 1 到 N。

对于每个站点 i，定义 c(i) 为其直接连接的下级站点数：
- 末端终点站（叶节点）满足 c(i) = 0
- 中转枢纽站（非叶节点）满足 c(i) 大于 0

系统提供以下公理供你推理：
- 线网的连接路段（边）数为 N - 1
- 所有站点的下级站点数之和等于 N - 1
- 末端终点站总数 L 加上中转枢纽站数 I 等于 N

初始状态：你仅知道中心枢纽站 ID=1 存在，其余站点未知。
（注：为与系统底层查询接口兼容，系统反馈信息中将统一使用“节点”和“子节点”作为标准术语，分别对应本场景中的站点和下级站点）

你的目标是通过调用查询指令，确定末端终点站（叶节点）的总数 L。

每轮你可以提出以下查询（每次只能包含一个查询标签）：

1. 询问总站点数：
<query_total></query_total>

2. 查询某个站点的下级站点信息（仅限已知但未查询过的站点）：
<query_node>站点ID</query_node>

3. 复查已查询站点的记录：
<query_record>站点ID</query_record>

4. 查询当前已发现的所有站点ID：
<query_known></query_known>

5. 查询已排查过的站点数量：
<query_explored_count></query_explored_count>

6. 查询已排查站点的下级站点数总和：
<query_children_sum></query_children_sum>

当你确定答案后，使用以下格式提交：
<answer>末端终点站总数</answer>

例如：
<answer>5</answer>

注意：答案只有一次提交机会，请确保你的推理正确后再提交。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's conduct a "Transport Network Terminal Station Identification" operation with the following rules:

The system maps a regional transport network distributed in a strictly directional branching tree structure. The total number of stations is N (unknown). The central transport hub has ID 1, and all stations are labeled with unique integer IDs ranging from 1 to N.

For each station i, define c(i) as its number of directly connected downstream stations (children):
- Terminal stations (leaf nodes) satisfy c(i) = 0
- Transit hubs (internal nodes) satisfy c(i) greater than 0

The following axioms are provided for reasoning:
- The number of connecting routes (edges) is N - 1
- The sum of all stations' downstream station counts equals N - 1
- The number of terminal stations L plus the number of transit hubs I equals N

Initial state: You only know that the central hub ID=1 exists; other stations are unknown.
(Note: To maintain compatibility with the underlying query interface, system feedback messages will uniformly use the standard terms "node" and "children" to refer to stations and downstream stations respectively.)

Your goal is to determine the total number of terminal stations L through queries.

Each turn you can make one of the following queries (only one query tag per turn):

1. Ask for the total number of stations:
<query_total></query_total>

2. Query a station's downstream information (only for known but not yet queried stations):
<query_node>StationID</query_node>

3. Review the record of an already queried station:
<query_record>StationID</query_record>

4. Query all currently known station IDs:
<query_known></query_known>

5. Query the count of explored stations:
<query_explored_count></query_explored_count>

6. Query the sum of downstream station counts of explored stations:
<query_children_sum></query_children_sum>

When you are ready to submit your answer, use:
<answer>NumberOfTerminalStations</answer>

For example:
<answer>5</answer>

Note: You only have one chance to submit the answer. Make sure your reasoning is correct before submission.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行"病毒传播链末端追踪"系统操作，规则如下：

流行病学调查发现了一起树状聚集性疫情。感染者总数为 N（未知）。零号病人 ID 为 1，所有感染者用不重复的整数 ID 标记，范围为 1 到 N。

对于每个感染者 i，定义 c(i) 为其直接传染的下级感染者数：
- 末端感染者（叶节点，未引发二次传播）满足 c(i) = 0
- 传播者（非叶节点）满足 c(i) 大于 0

系统提供以下公理供你推理：
- 传播事件（边）数为 N - 1
- 所有感染者的直接传染人数之和等于 N - 1
- 末端感染者总数 L 加上传播者数 I 等于 N

初始状态：你仅知道零号病人 ID=1 存在，其余感染者未知。
（注：为与系统底层查询接口兼容，系统反馈信息中将统一使用“节点”和“子节点”作为标准术语，分别对应本场景中的感染者和被传染者）

你的目标是通过调用查询指令，确定末端感染者（叶节点）的总数 L。

每轮你可以提出以下查询（每次只能包含一个查询标签）：

1. 询问总感染者数：
<query_total></query_total>

2. 查询某个感染者的下级传染信息（仅限已知但未查询过的感染者）：
<query_node>感染者ID</query_node>

3. 复查已查询感染者的记录：
<query_record>感染者ID</query_record>

4. 查询当前已发现的所有感染者ID：
<query_known></query_known>

5. 查询已流调过的感染者数量：
<query_explored_count></query_explored_count>

6. 查询已流调感染者的直接传染人数总和：
<query_children_sum></query_children_sum>

当你确定答案后，使用以下格式提交：
<answer>末端感染者总数</answer>

例如：
<answer>5</answer>

注意：答案只有一次提交机会，请确保你的推理正确后再提交。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's conduct a "Viral Transmission Chain Terminal Tracing" operation with the following rules:

Epidemiological investigation has identified a tree-like cluster outbreak. The total number of infected patients is N (unknown). Patient Zero has ID 1, and all patients are labeled with unique integer IDs ranging from 1 to N.

For each patient i, define c(i) as the number of individuals they directly infected (children):
- Terminal patients (leaf nodes, caused no secondary transmission) satisfy c(i) = 0
- Spreaders (internal nodes) satisfy c(i) greater than 0

The following axioms are provided for reasoning:
- The number of transmission events (edges) is N - 1
- The sum of all patients' directly infected counts equals N - 1
- The number of terminal patients L plus the number of spreaders I equals N

Initial state: You only know that Patient Zero ID=1 exists; other patients are unknown.
(Note: To maintain compatibility with the underlying query interface, system feedback messages will uniformly use the standard terms "node" and "children" to refer to patients and their infectees respectively.)

Your goal is to determine the total number of terminal patients L through queries.

Each turn you can make one of the following queries (only one query tag per turn):

1. Ask for the total number of patients:
<query_total></query_total>

2. Query a patient's downstream transmission information (only for known but not yet queried patients):
<query_node>PatientID</query_node>

3. Review the record of an already queried patient:
<query_record>PatientID</query_record>

4. Query all currently known patient IDs:
<query_known></query_known>

5. Query the count of investigated patients:
<query_explored_count></query_explored_count>

6. Query the sum of transmission counts of investigated patients:
<query_children_sum></query_children_sum>

When you are ready to submit your answer, use:
<answer>NumberOfTerminalPatients</answer>

For example:
<answer>5</answer>

Note: You only have one chance to submit the answer. Make sure your reasoning is correct before submission.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行"学科知识图谱末端节点评估"，规则如下：

一门核心学科的知识点构成了严格的有根树状前置依赖图谱。知识点总数为 N（未知）。最底层的核心基础概念 ID 为 1，所有知识点用不重复的整数 ID 标记，范围为 1 到 N。

对于每个知识点 i，定义 c(i) 为直接以其为前置依赖的后续知识点数：
- 终极知识点（叶节点，无后续依赖）满足 c(i) = 0
- 基础/中间知识点（非叶节点）满足 c(i) 大于 0

系统提供以下公理供你推理：
- 知识点间的依赖关系（边）数为 N - 1
- 所有知识点的后续依赖知识点数之和等于 N - 1
- 终极知识点总数 L 加上基础/中间知识点数 I 等于 N

初始状态：你仅知道核心基础概念 ID=1 存在，其余知识点未知。
（注：为与系统底层查询接口兼容，系统反馈信息中将统一使用“节点”和“子节点”作为标准术语，分别对应本场景中的前置知识点和后续知识点）

你的目标是通过调用查询指令，确定终极知识点（叶节点）的总数 L。

每轮你可以提出以下查询（每次只能包含一个查询标签）：

1. 询问总知识点数：
<query_total></query_total>

2. 查询某个知识点的后续依赖信息（仅限已知但未查询过的知识点）：
<query_node>知识点ID</query_node>

3. 复查已查询知识点的记录：
<query_record>知识点ID</query_record>

4. 查询当前已发现的所有知识点ID：
<query_known></query_known>

5. 查询已评估过的知识点数量：
<query_explored_count></query_explored_count>

6. 查询已评估知识点的直接后续依赖数总和：
<query_children_sum></query_children_sum>

当你确定答案后，使用以下格式提交：
<answer>终极知识点总数</answer>

例如：
<answer>5</answer>

注意：答案只有一次提交机会，请确保你的推理正确后再提交。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's evaluate the "Disciplinary Knowledge Graph Terminal Nodes" with the following rules:

The concepts of a core discipline form a strict rooted tree of prerequisite dependencies. The total number of knowledge concepts is N (unknown). The foundational core concept has ID 1, and all concepts are labeled with unique integer IDs ranging from 1 to N.

For each concept i, define c(i) as the number of subsequent concepts that directly depend on it (children):
- Terminal concepts (leaf nodes, having no subsequent dependencies) satisfy c(i) = 0
- Foundational/intermediate concepts (internal nodes) satisfy c(i) greater than 0

The following axioms are provided for reasoning:
- The number of dependency relationships (edges) is N - 1
- The sum of all concepts' subsequent dependent concept counts equals N - 1
- The number of terminal concepts L plus the number of intermediate concepts I equals N

Initial state: You only know that the foundational concept ID=1 exists; other concepts are unknown.
(Note: To maintain compatibility with the underlying query interface, system feedback messages will uniformly use the standard terms "node" and "children" to refer to concepts and their dependent concepts respectively.)

Your goal is to determine the total number of terminal concepts L through queries.

Each turn you can make one of the following queries (only one query tag per turn):

1. Ask for the total number of concepts:
<query_total></query_total>

2. Query a concept's subsequent dependency information (only for known but not yet queried concepts):
<query_node>ConceptID</query_node>

3. Review the record of an already queried concept:
<query_record>ConceptID</query_record>

4. Query all currently known concept IDs:
<query_known></query_known>

5. Query the count of evaluated concepts:
<query_explored_count></query_explored_count>

6. Query the sum of subsequent dependencies of evaluated concepts:
<query_children_sum></query_children_sum>

When you are ready to submit your answer, use:
<answer>NumberOfTerminalConcepts</answer>

For example:
<answer>5</answer>

Note: You only have one chance to submit the answer. Make sure your reasoning is correct before submission.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行"产品BOM(物料清单)底层零件核算"，规则如下：

一款复杂产品的BOM构成了一棵标准的装配树。组件总数为 N（未知）。最终成品 ID 为 1，所有组件用不重复的整数 ID 标记，范围为 1 到 N。

对于每个组件 i，定义 c(i) 为其直接包含的子零件/子组件数：
- 底层基础零件（叶节点，不可再分）满足 c(i) = 0
- 复合组件（非叶节点）满足 c(i) 大于 0

系统提供以下公理供你推理：
- 装配拆解关系（边）数为 N - 1
- 所有组件直接包含的子零件数之和等于 N - 1
- 底层基础零件总数 L 加上复合组件数 I 等于 N

初始状态：你仅知道最终成品 ID=1 存在，其余组件未知。
（注：为与系统底层查询接口兼容，系统反馈信息中将统一使用“节点”和“子节点”作为标准术语，分别对应本场景中的组件和子零件）

你的目标是通过调用查询指令，确定底层基础零件（叶节点）的总数 L。

每轮你可以提出以下查询（每次只能包含一个查询标签）：

1. 询问总组件数：
<query_total></query_total>

2. 查询某个组件的子零件信息（仅限已知但未查询过的组件）：
<query_node>组件ID</query_node>

3. 复查已查询组件的记录：
<query_record>组件ID</query_record>

4. 查询当前已发现的所有组件ID：
<query_known></query_known>

5. 查询已核算过的组件数量：
<query_explored_count></query_explored_count>

6. 查询已核算组件的子零件数总和：
<query_children_sum></query_children_sum>

当你确定答案后，使用以下格式提交：
<answer>底层基础零件总数</answer>

例如：
<answer>5</answer>

注意：答案只有一次提交机会，请确保你的推理正确后再提交。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct a "Product BOM Base Component Audit" with the following rules:

A complex product's Bill of Materials (BOM) forms a standard assembly tree. The total number of components is N (unknown). The final product has ID 1, and all components are labeled with unique integer IDs ranging from 1 to N.

For each component i, define c(i) as the number of sub-components/parts it directly contains (children):
- Base raw materials (leaf nodes, cannot be further disassembled) satisfy c(i) = 0
- Sub-assemblies (internal nodes) satisfy c(i) greater than 0

The following axioms are provided for reasoning:
- The number of assembly relationships (edges) is N - 1
- The sum of all components' sub-component counts equals N - 1
- The number of base raw materials L plus the number of sub-assemblies I equals N

Initial state: You only know that the final product ID=1 exists; other components are unknown.
(Note: To maintain compatibility with the underlying query interface, system feedback messages will uniformly use the standard terms "node" and "children" to refer to components and sub-components respectively.)

Your goal is to determine the total number of base raw materials L through queries.

Each turn you can make one of the following queries (only one query tag per turn):

1. Ask for the total number of components:
<query_total></query_total>

2. Query a component's sub-component information (only for known but not yet queried components):
<query_node>ComponentID</query_node>

3. Review the record of an already queried component:
<query_record>ComponentID</query_record>

4. Query all currently known component IDs:
<query_known></query_known>

5. Query the count of audited components:
<query_explored_count></query_explored_count>

6. Query the sum of sub-component counts of audited components:
<query_children_sum></query_children_sum>

When you are ready to submit your answer, use:
<answer>NumberOfBaseComponents</answer>

For example:
<answer>5</answer>

Note: You only have one chance to submit the answer. Make sure your reasoning is correct before submission.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行"企业股权穿透与底层实体调查"，规则如下：

某跨国集团具有严格树状的层级控股结构。关联企业总数为 N（未知）。顶层控股母公司 ID 为 1，所有企业用不重复的整数 ID 标记，范围为 1 到 N。

对于每个企业 i，定义 c(i) 为其直接控股的子公司数：
- 底层运营实体（叶节点，无下属公司）满足 c(i) = 0
- 中间控股公司（非叶节点）满足 c(i) 大于 0

系统提供以下公理供你推理：
- 控股关系（边）数为 N - 1
- 所有企业的控股子公司数之和等于 N - 1
- 底层运营实体总数 L 加上中间控股公司数 I 等于 N

初始状态：你仅知道顶层控股母公司 ID=1 存在，其余企业未知。
（注：为与系统底层查询接口兼容，系统反馈信息中将统一使用“节点”和“子节点”作为标准术语，分别对应本场景中的母公司和子公司）

你的目标是通过调用查询指令，查清底层运营实体（叶节点）的总数 L。

每轮你可以提出以下查询（每次只能包含一个查询标签）：

1. 询问总企业数：
<query_total></query_total>

2. 查询某个企业的下属公司信息（仅限已知但未查询过的企业）：
<query_node>企业ID</query_node>

3. 复查已查询企业的记录：
<query_record>企业ID</query_record>

4. 查询当前已发现的所有企业ID：
<query_known></query_known>

5. 查询已调查过的企业数量：
<query_explored_count></query_explored_count>

6. 查询已调查企业的直接控股子公司数总和：
<query_children_sum></query_children_sum>

当你确定答案后，使用以下格式提交：
<answer>底层运营实体总数</answer>

例如：
<answer>5</answer>

注意：答案只有一次提交机会，请确保你的推理正确后再提交。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's conduct a "Corporate Equity Penetration and Subsidiary Investigation" with the following rules:

A multinational conglomerate has a strictly tree-like hierarchical holding structure. The total number of affiliated entities is N (unknown). The ultimate holding company has ID 1, and all entities are labeled with unique integer IDs ranging from 1 to N.

For each entity i, define c(i) as the number of subsidiaries it directly controls (children):
- Operating subsidiaries (leaf nodes, with no further subsidiaries) satisfy c(i) = 0
- Intermediate holding companies (internal nodes) satisfy c(i) greater than 0

The following axioms are provided for reasoning:
- The number of control relationships (edges) is N - 1
- The sum of all entities' subsidiary counts equals N - 1
- The number of operating subsidiaries L plus the number of intermediate holding companies I equals N

Initial state: You only know that the ultimate holding company ID=1 exists; other entities are unknown.
(Note: To maintain compatibility with the underlying query interface, system feedback messages will uniformly use the standard terms "node" and "children" to refer to parent entities and subsidiaries respectively.)

Your goal is to determine the total number of operating subsidiaries L through queries.

Each turn you can make one of the following queries (only one query tag per turn):

1. Ask for the total number of entities:
<query_total></query_total>

2. Query an entity's subsidiary information (only for known but not yet queried entities):
<query_node>EntityID</query_node>

3. Review the record of an already queried entity:
<query_record>EntityID</query_record>

4. Query all currently known entity IDs:
<query_known></query_known>

5. Query the count of investigated entities:
<query_explored_count></query_explored_count>

6. Query the sum of subsidiary counts of investigated entities:
<query_children_sum></query_children_sum>

When you are ready to submit your answer, use:
<answer>NumberOfOperatingSubsidiaries</answer>

For example:
<answer>5</answer>

Note: You only have one chance to submit the answer. Make sure your reasoning is correct before submission.
"""

    tags = ["answer", "query_total", "query_node", "query_record", "query_known", 
            "query_explored_count", "query_children_sum"]
    
    reasoning_type = "演绎推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        1: {
            "n": 7,
            "tree": {
                1: [2, 3],
                2: [4, 5],
                3: [6, 7],
                4: [],
                5: [],
                6: [],
                7: []
            },
            "leaf_count": 4
        },
        2: {
            "n": 10,
            "tree": {
                1: [2, 3, 4],
                2: [5, 6],
                3: [7],
                4: [8, 9, 10],
                5: [],
                6: [],
                7: [],
                8: [],
                9: [],
                10: []
            },
            "leaf_count": 6
        },
        3: {
            "n": 15,
            "tree": {
                1: [2, 3, 4],
                2: [5, 6, 7],
                3: [8, 9],
                4: [10],
                5: [11, 12],
                6: [],
                7: [13],
                8: [],
                9: [14, 15],
                10: [],
                11: [],
                12: [],
                13: [],
                14: [],
                15: []
            },
            "leaf_count": 8
        },
        4: {
            "n": 20,
            "tree": {
                1: [2, 3, 4, 5],
                2: [6, 7],
                3: [8, 9, 10],
                4: [11],
                5: [12, 13],
                6: [14, 15],
                7: [],
                8: [16],
                9: [],
                10: [17, 18],
                11: [19],
                12: [],
                13: [20],
                14: [],
                15: [],
                16: [],
                17: [],
                18: [],
                19: [],
                20: []
            },
            "leaf_count": 10
        },
        5: {
            "n": 30,
            "tree": {
                1: [2, 3, 4],
                2: [5, 6, 7, 8],
                3: [9, 10],
                4: [11, 12, 13],
                5: [14, 15],
                6: [16],
                7: [17, 18, 19],
                8: [],
                9: [20, 21],
                10: [22],
                11: [23, 24],
                12: [],
                13: [25, 26],
                14: [],
                15: [27],
                16: [28],
                17: [],
                18: [],
                19: [29, 30],
                20: [],
                21: [],
                22: [],
                23: [],
                24: [],
                25: [],
                26: [],
                27: [],
                28: [],
                29: [],
                30: []
            },
            "leaf_count": 16
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        
        self.tree = cfg["tree"]
        self.n = cfg["n"]
        self.leaf_count = cfg["leaf_count"]
        
        self.known_nodes = {1}
        self.queried_nodes = set()
        
        self.query_cache = {}

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.leaf_count
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            return self._produce_response_zh(parsed_info)
        else:
            return self._produce_response_en(parsed_info)

    def _cf_make_wrong(self, correct):
        import re
        
        def _alter_number(match):
            num = int(match.group(0))
            offset = random.choice([-2, -1, 1, 2])
            new_num = max(0, num + offset)
            if new_num == num:
                new_num = num + 1
            return str(new_num)
        
        altered = re.sub(r'\d+', _alter_number, correct, count=1)
        if altered == correct:
            if self.config.language == "zh":
                return correct + "（附加信息：该节点可能还有隐藏子节点。）"
            else:
                return correct + " (Additional info: this node may have hidden children.)"
        return altered

    def _produce_response_zh(self, parsed_info):
        if "query_total" in parsed_info:
            return f"总节点数 N = {self.n}。"
        
        elif "query_node" in parsed_info:
            try:
                node_id = int(parsed_info["query_node"].strip())
                
                if node_id not in self.known_nodes:
                    return f"错误：节点 {node_id} 尚未被发现，无法查询。"
                
                if node_id in self.queried_nodes:
                    return f"错误：节点 {node_id} 已经查询过，请使用复查记录操作。"
                
                if node_id not in self.tree:
                    return f"错误：节点 {node_id} 不存在。"
                
                children = self.tree[node_id]
                c_i = len(children)
                
                self.queried_nodes.add(node_id)
                self.query_cache[node_id] = (c_i, children)
                self.known_nodes.update(children)
                
                if c_i == 0:
                    return f"节点 {node_id} 的子节点数 c({node_id}) = 0；它是叶节点，无子节点。"
                else:
                    children_str = ", ".join(map(str, children))
                    return f"节点 {node_id} 的子节点数 c({node_id}) = {c_i}；子节点ID列表：{children_str}。"
            
            except ValueError:
                return "错误：节点ID必须是整数。"
        
        elif "query_record" in parsed_info:
            try:
                node_id = int(parsed_info["query_record"].strip())
                
                if node_id not in self.queried_nodes:
                    return f"节点 {node_id} 尚未查询，无记录。"
                
                c_i, children = self.query_cache[node_id]
                if c_i == 0:
                    return f"节点 {node_id} 的记录：c({node_id}) = 0；它是叶节点，无子节点。"
                else:
                    children_str = ", ".join(map(str, children))
                    return f"节点 {node_id} 的记录：c({node_id}) = {c_i}；子节点ID列表：{children_str}。"
            
            except ValueError:
                return "错误：节点ID必须是整数。"
        
        elif "query_known" in parsed_info:
            known_list = sorted(list(self.known_nodes))
            known_str = ", ".join(map(str, known_list))
            return f"当前已发现的节点ID：{known_str}。"
        
        elif "query_explored_count" in parsed_info:
            return f"当前已查询的节点数为 {len(self.queried_nodes)}。"
        
        elif "query_children_sum" in parsed_info:
            total_sum = sum(c_i for c_i, _ in self.query_cache.values())
            return f"已查询节点的子节点数总和为 {total_sum}。"
        
        else:
            raise ValueError("无效的查询标签。")

    def _produce_response_en(self, parsed_info):
        if "query_total" in parsed_info:
            return f"Total number of nodes N = {self.n}."
        
        elif "query_node" in parsed_info:
            try:
                node_id = int(parsed_info["query_node"].strip())
                
                if node_id not in self.known_nodes:
                    return f"Error: Node {node_id} has not been discovered yet and cannot be queried."
                
                if node_id in self.queried_nodes:
                    return f"Error: Node {node_id} has already been queried. Please use query_record to review."
                
                if node_id not in self.tree:
                    return f"Error: Node {node_id} does not exist."
                
                children = self.tree[node_id]
                c_i = len(children)
                
                self.queried_nodes.add(node_id)
                self.query_cache[node_id] = (c_i, children)
                self.known_nodes.update(children)
                
                if c_i == 0:
                    return f"Node {node_id} has c({node_id}) = 0; it is a leaf node with no children."
                else:
                    children_str = ", ".join(map(str, children))
                    return f"Node {node_id} has c({node_id}) = {c_i}; children IDs: {children_str}."
            
            except ValueError:
                return "Error: Node ID must be an integer."
        
        elif "query_record" in parsed_info:
            try:
                node_id = int(parsed_info["query_record"].strip())
                
                if node_id not in self.queried_nodes:
                    return f"Node {node_id} has not been queried yet; no record available."
                
                c_i, children = self.query_cache[node_id]
                if c_i == 0:
                    return f"Node {node_id} record: c({node_id}) = 0; it is a leaf node with no children."
                else:
                    children_str = ", ".join(map(str, children))
                    return f"Node {node_id} record: c({node_id}) = {c_i}; children IDs: {children_str}."
            
            except ValueError:
                return "Error: Node ID must be an integer."
        
        elif "query_known" in parsed_info:
            known_list = sorted(list(self.known_nodes))
            known_str = ", ".join(map(str, known_list))
            return f"Currently known node IDs: {known_str}."
        
        elif "query_explored_count" in parsed_info:
            return f"Number of explored nodes: {len(self.queried_nodes)}."
        
        elif "query_children_sum" in parsed_info:
            total_sum = sum(c_i for c_i, _ in self.query_cache.values())
            return f"Sum of children counts of explored nodes: {total_sum}."
        
        else:
            raise ValueError("Invalid query tag.")

    def get_all_possible_queries(self):
        results = []
        
        def run_safe(tag, content, setup_fn=None):
            saved_known = self.known_nodes.copy()
            saved_queried = self.queried_nodes.copy()
            saved_cache = self.query_cache.copy()
            
            try:
                if setup_fn:
                    setup_fn()
                
                parsed_info = {tag: str(content)}
                
                if self.config.language == "zh":
                    ans = self._produce_response_zh(parsed_info)
                else:
                    ans = self._produce_response_en(parsed_info)
                
                query_str = f"<{tag}>{content}</{tag}>"
                return {"query": query_str, "answer": ans}
                
            except Exception:
                return None
            finally:
                self.known_nodes = saved_known
                self.queried_nodes = saved_queried
                self.query_cache = saved_cache

        res = run_safe("query_total", "")
        if res: results.append(res)
        
        for i in range(1, self.n + 1):
            def setup_node_query(node_id=i):
                self.known_nodes.add(node_id)
                if node_id in self.queried_nodes:
                    self.queried_nodes.remove(node_id)
            
            res = run_safe("query_node", i, setup_node_query)
            if res: results.append(res)
            
        for i in range(1, self.n + 1):
            def setup_record_query(node_id=i):
                self.queried_nodes.add(node_id)
                children = self.tree[node_id]
                c_i = len(children)
                self.query_cache[node_id] = (c_i, children)
                
            res = run_safe("query_record", i, setup_record_query)
            if res: results.append(res)
            
        def setup_all_known():
            self.known_nodes = set(range(1, self.n + 1))
        res = run_safe("query_known", "", setup_all_known)
        if res: results.append(res)
        
        def setup_all_explored_count():
            self.queried_nodes = set(range(1, self.n + 1))
        res = run_safe("query_explored_count", "", setup_all_explored_count)
        if res: results.append(res)
        
        def setup_all_children_sum():
            self.queried_nodes = set(range(1, self.n + 1))
            for node_id in range(1, self.n + 1):
                children = self.tree[node_id]
                self.query_cache[node_id] = (len(children), children)
        res = run_safe("query_children_sum", "", setup_all_children_sum)
        if res: results.append(res)
        
        return results