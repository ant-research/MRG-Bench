import re
import random
from .base import Game

class HiddenTreeInferenceGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"隐藏树结构推断"游戏，规则如下：

游戏设定了一棵固定的有根无序树 T，包含 {n} 个节点，节点编号为 1 到 {n}。除了节点数量和编号外，你无法直接看到树的结构。

对于任意两个节点 i 和 j，如果以 i 为根的子树和以 j 为根的子树在有根无序树意义下结构同构，则称 i 和 j 属于同一"子树结构类型"。

你可以发起以下三种查询来获取树的结构信息：

1. **同构测试**：询问节点 i 和 j 的子树是否结构同构
   - 要求：i 不等于 j，且都在 1 到 {n} 范围内
   - 返回：是 或 否
   - 此类查询最多可进行 {p_budget} 次

2. **度数查询**：询问节点 i 有多少个直接子节点
   - 返回：非负整数
   - 与高度查询共享预算

3. **高度查询**：询问以节点 i 为根的子树高度
   - 返回：正整数（叶子节点高度为 1）
   - 与度数查询共享预算

度数查询和高度查询共享预算，总次数不超过 {q_budget} 次。

当你认为已收集足够信息后，需要一次性提交 {m} 对节点配对，每对节点 (a,b) 满足 a 不等于 b，且每个节点编号在所有配对中最多出现一次。系统会判定每对节点的子树是否同构，统计正确配对数。

**成功条件**：正确配对数达到 {k} 对或以上。

每次只能发起一个查询。请使用以下 XML 格式：

- 同构测试（例如询问节点 3 和节点 5）：
<query_isomorphic>3,5</query_isomorphic>

- 度数查询（例如询问节点 2）：
<query_degree>2</query_degree>

- 高度查询（例如询问节点 4）：
<query_height>4</query_height>

当你准备提交最终答案时，必须提供 {m} 对节点配对，格式如下：

<answer>1,2;3,4;5,6;...</answer>

其中每对节点用逗号分隔，不同配对用分号分隔，共 {m} 对。每个节点编号在所有配对中最多出现一次。
"""

    game_rule_en = """\
Let's play a "Hidden Tree Structure Inference" game. Here are the rules:

The game has set up a fixed rooted unordered tree T containing {n} nodes, numbered from 1 to {n}. Apart from the number of nodes and their IDs, you cannot directly see the tree structure.

For any two nodes i and j, if the subtree rooted at i and the subtree rooted at j are structurally isomorphic as rooted unordered trees, then i and j belong to the same "subtree structure type".

You can make the following three types of queries to obtain structural information about the tree:

1. **Isomorphism Test**: Ask whether the subtrees rooted at nodes i and j are structurally isomorphic
   - Requirements: i not equal to j, both within range 1 to {n}
   - Returns: Yes or No
   - Maximum {p_budget} queries allowed

2. **Degree Query**: Ask how many direct children node i has
   - Returns: non-negative integer
   - Shares budget with height queries

3. **Height Query**: Ask the height of the subtree rooted at node i
   - Returns: positive integer (leaf node has height 1)
   - Shares budget with degree queries

Degree queries and height queries share a budget with a total limit of {q_budget} queries.

When you believe you have gathered sufficient information, submit {m} pairs of nodes at once. Each pair (a,b) must satisfy a not equal to b, and each node ID may appear in at most one pair across all pairs. The system will determine whether each pair's subtrees are isomorphic and count the correct pairs.

**Success Condition**: The number of correct pairs reaches {k} or more.

Only one query per turn. Use the following XML format:

- Isomorphism test (e.g., asking about nodes 3 and 5):
<query_isomorphic>3,5</query_isomorphic>

- Degree query (e.g., asking about node 2):
<query_degree>2</query_degree>

- Height query (e.g., asking about node 4):
<query_height>4</query_height>

When ready to submit your final answer, provide {m} pairs of nodes in this format:

<answer>1,2;3,4;5,6;...</answer>

Each pair separated by comma, different pairs separated by semicolon, total {m} pairs. Each node ID may appear in at most one pair.
"""

    contextualized_rule_zh_1 = """\
欢迎进入“综合交通枢纽网络拓扑分析”系统。演练规则如下：

系统已载入一个包含 {n} 个枢纽站点的区域路网层级树 T，节点编号为 1 到 {n}。除站点总数和编号外，你无法直接查看路网的具体辐射结构。

对于任意两个站点 i 和 j，如果以 i 为顶点的下属辐射路网和以 j 为顶点的下属辐射路网在层级拓扑上完全一致，则称 i 和 j 属于同一“路网拓扑类型”。

你可以发起以下三种查询指令来获取路网信息：

1. **拓扑一致性测试**：询问站点 i 和 j 的下属路网结构是否完全一致
   - 要求：i 不等于 j，且都在 1 到 {n} 范围内
   - 返回：是 或 否
   - 此类查询最多可进行 {p_budget} 次

2. **直属分支查询**：询问站点 i 有多少个直接下级管辖站点
   - 返回：非负整数
   - 与管辖深度查询共享预算

3. **管辖深度查询**：询问以站点 i 为顶点的下属路网最大层级深度
   - 返回：正整数（末端站点深度为 1）
   - 与直属分支查询共享预算

直属分支查询和管辖深度查询共享预算，总次数不超过 {q_budget} 次。

当你认为已掌握足够的路网情报后，需要一次性提交 {m} 对站点配对，每对站点 (a,b) 满足 a 不等于 b，且每个站点编号在所有配对中最多出现一次。系统会判定每对站点的下属路网是否属于同一拓扑类型，统计正确配对数。

**成功条件**：正确配对数达到 {k} 对或以上。

每次只能发起一个查询。请使用以下 XML 格式：

- 拓扑一致性测试：
<query_isomorphic>3,5</query_isomorphic>

- 直属分支查询：
<query_degree>2</query_degree>

- 管辖深度查询：
<query_height>4</query_height>

准备提交最终报告时，必须提供 {m} 对配对，格式如下：
<answer>1,2;3,4;5,6;...</answer>
其中每个站点编号在所有配对中最多出现一次。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Comprehensive Transit Hub Network Topology Analysis" system. The drill rules are as follows:

The system has loaded a regional transit hierarchy tree T containing {n} hub stations, numbered 1 to {n}. Apart from the total number of stations and their IDs, the specific network radiation structure is hidden from you.

For any two stations i and j, if the sub-network governed by i and the sub-network governed by j are structurally identical in topology, they share the same "Network Topology Type".

You can issue the following three types of query commands to obtain network intelligence:

1. **Topology Isomorphism Test**: Ask if the sub-networks of stations i and j are structurally identical
   - Requirements: i not equal to j, both within range 1 to {n}
   - Returns: Yes or No
   - Maximum {p_budget} queries allowed

2. **Direct Branch Query**: Ask how many direct subordinate stations station i governs
   - Returns: non-negative integer
   - Shares budget with jurisdiction depth queries

3. **Jurisdiction Depth Query**: Ask the maximum hierarchical depth of the sub-network radiating from station i
   - Returns: positive integer (terminal station depth is 1)
   - Shares budget with direct branch queries

Direct branch and jurisdiction depth queries share a budget with a total limit of {q_budget} queries.

When you believe you have gathered sufficient intelligence, submit {m} pairs of stations at once. Each pair (a,b) must satisfy a not equal to b, and each station ID may appear in at most one pair across all pairs. The system will evaluate whether each pair's sub-networks share the same topology type and count the correct pairs.

**Success Condition**: The number of correct pairs reaches {k} or more.

Only one query per turn. Use the following XML format:

- Topology Isomorphism Test:
<query_isomorphic>3,5</query_isomorphic>

- Direct Branch Query:
<query_degree>2</query_degree>

- Jurisdiction Depth Query:
<query_height>4</query_height>

When ready to submit the final report, provide {m} pairs of stations in this format:
<answer>1,2;3,4;5,6;...</answer>
Each station ID may appear in at most one pair.
"""

    contextualized_rule_zh_2 = """\
我们现在来执行一项“病原体传播链溯源”分析任务，规则如下：

疾控中心锁定了一棵固定的单向传播层级树 T，包含 {n} 个感染簇节点，节点编号为 1 到 {n}。除了节点数量和编号外，你无法直接看到传播链的具体结构。

对于任意两个节点 i 和 j，如果以 i 为源头的下游传播子链和以 j 为源头的下游传播子链在层级拓扑上完全一致，则称 i 和 j 属于同一“传播变异演化类型”。

你可以发起以下三种查询来获取传播链的结构信息：

1. **同源测试**：询问节点 i 和 j 的下游传播链是否结构一致
   - 要求：i 不等于 j，且都在 1 到 {n} 范围内
   - 返回：是 或 否
   - 此类查询最多可进行 {p_budget} 次

2. **次级感染查询**：询问节点 i 有多少个直接导致的次级感染簇
   - 返回：非负整数
   - 与世代查询共享预算

3. **世代高度查询**：询问以节点 i 为源头的传播链最大世代深度
   - 返回：正整数（末端无继发感染的节点深度为 1）
   - 与次级感染查询共享预算

次级感染查询和世代高度查询共享预算，总次数不超过 {q_budget} 次。

当你认为已收集足够信息后，需要一次性提交 {m} 对感染簇配对，每对节点 (a,b) 满足 a 不等于 b，且每个节点编号在所有配对中最多出现一次。系统会判定每对节点的下游传播链是否结构一致，统计正确配令人数。

**成功条件**：正确配对数达到 {k} 对或以上。

每次只能发起一个查询。请使用以下 XML 格式：

- 同源测试：
<query_isomorphic>3,5</query_isomorphic>

- 次级感染查询：
<query_degree>2</query_degree>

- 世代高度查询：
<query_height>4</query_height>

当你准备提交最终分析结果时，必须提供 {m} 对配对，格式如下：
<answer>1,2;3,4;5,6;...</answer>
其中每个节点编号在所有配对中最多出现一次。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
We are now executing a "Pathogen Transmission Chain Tracing" analysis task. The rules are as follows:

The CDC has locked onto a fixed unidirectional transmission hierarchy tree T, containing {n} infection cluster nodes numbered from 1 to {n}. Apart from the node count and IDs, the specific transmission structure is hidden.

For any two nodes i and j, if the downstream transmission sub-chain originating from i and the downstream transmission sub-chain originating from j are topologically identical, then i and j belong to the same "Transmission Evolution Type".

You can initiate the following three types of queries to gather structural info:

1. **Homology Test**: Ask whether the downstream transmission chains of nodes i and j are structurally identical
   - Requirements: i not equal to j, both within range 1 to {n}
   - Returns: Yes or No
   - Maximum {p_budget} queries allowed

2. **Secondary Infection Query**: Ask how many direct secondary infection clusters are caused by node i
   - Returns: non-negative integer
   - Shares budget with generation queries

3. **Generation Height Query**: Ask the maximum generation depth of the transmission chain originating from node i
   - Returns: positive integer (terminal node with no subsequent infection has depth 1)
   - Shares budget with secondary infection queries

Secondary infection queries and generation height queries share a budget with a total limit of {q_budget} queries.

When you believe you have gathered enough information, submit {m} pairs of infection clusters at once. Each pair (a,b) must satisfy a not equal to b, and each node ID may appear in at most one pair across all pairs. The system will determine if each pair's downstream chains are identical.

**Success Condition**: The number of correct pairs reaches {k} or more.

Only one query per turn. Use the following XML format:

- Homology Test:
<query_isomorphic>3,5</query_isomorphic>

- Secondary Infection Query:
<query_degree>2</query_degree>

- Generation Height Query:
<query_height>4</query_height>

When ready to submit the final analysis, provide {m} pairs in this format:
<answer>1,2;3,4;5,6;...</answer>
Each node ID may appear in at most one pair.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“核心素养知识图谱解析”系统。教学规划规则如下：

系统内嵌了一棵固定的知识点前置依赖树 T，包含 {n} 个知识模块，编号为 1 到 {n}。除模块数量和编号外，你无法直接看到知识点的层级依赖关系。

对于任意两个模块 i 和 j，如果以 i 为顶点的后续衍生知识结构和以 j 为顶点的后续衍生知识结构在依赖拓扑上完全一致，则称 i 和 j 属于同一“认知递进模式”。

你可以发起以下三种查询来获取知识树的依赖信息：

1. **认知一致性测试**：询问模块 i 和 j 的衍生知识结构是否完全一致
   - 要求：i 不等于 j，且都在 1 到 {n} 范围内
   - 返回：是 或 否
   - 此类查询最多可进行 {p_budget} 次

2. **直接后继查询**：询问模块 i 有多少个以它为直接前置条件的子模块
   - 返回：非负整数
   - 与路径深度查询共享预算

3. **路径深度查询**：询问以模块 i 为起点的衍生学习路径的最大层级深度
   - 返回：正整数（无后续衍生知识的底层模块深度为 1）
   - 与直接后继查询共享预算

直接后继查询和路径深度查询共享预算，总次数不超过 {q_budget} 次。

当你认为已摸清结构后，需要一次性提交 {m} 对模块配对，每对模块 (a,b) 满足 a 不等于 b，且每个模块编号在所有配对中最多出现一次。系统会判定每对模块的衍生知识结构是否同构。

**成功条件**：正确配对数达到 {k} 对或以上。

每次只能发起一个查询。请使用以下 XML 格式：

- 认知一致性测试：
<query_isomorphic>3,5</query_isomorphic>

- 直接后继查询：
<query_degree>2</query_degree>

- 路径深度查询：
<query_height>4</query_height>

当你准备提交最终评估体系时，提供 {m} 对配对，格式如下：
<answer>1,2;3,4;5,6;...</answer>
其中每个模块编号在所有配对中最多出现一次。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Core Competency Knowledge Graph Analysis" system. The pedagogical planning rules are as follows:

The system contains a fixed prerequisite knowledge dependency tree T with {n} knowledge modules, numbered 1 to {n}. Beyond the module count and IDs, the hierarchical dependencies remain hidden.

For any two modules i and j, if the subsequent derivative knowledge structure originating from i and the one from j are topologically identical, then i and j share the same "Cognitive Progression Pattern".

You can initiate three types of queries to uncover the knowledge tree dependencies:

1. **Cognitive Isomorphism Test**: Ask if the derivative knowledge structures of modules i and j are perfectly identical
   - Requirements: i not equal to j, both within range 1 to {n}
   - Returns: Yes or No
   - Maximum {p_budget} queries allowed

2. **Direct Successor Query**: Ask how many sub-modules strictly require module i as their direct prerequisite
   - Returns: non-negative integer
   - Shares budget with path depth queries

3. **Path Depth Query**: Ask the maximum learning path depth originating from module i
   - Returns: positive integer (fundamental modules with no further derivations have a depth of 1)
   - Shares budget with direct successor queries

Direct successor queries and path depth queries share a budget with a total limit of {q_budget} queries.

When you believe the structure is clear, submit {m} pairs of modules. Each pair (a,b) must satisfy a not equal to b, and each module ID may appear in at most one pair across all pairs. The system will verify if their derivative structures are identical.

**Success Condition**: The number of correct pairs reaches {k} or more.

Only one query per turn. Use the following XML format:

- Cognitive Isomorphism Test:
<query_isomorphic>3,5</query_isomorphic>

- Direct Successor Query:
<query_degree>2</query_degree>

- Path Depth Query:
<query_height>4</query_height>

When ready to submit the final framework, provide {m} pairs in this format:
<answer>1,2;3,4;5,6;...</answer>
Each module ID may appear in at most one pair.
"""

    contextualized_rule_zh_4 = """\
欢迎执行“精密装备BOM（物料清单）层级逆向工程”任务，操作规程如下：

系统导入了一棵固定的装备总成装配树 T，包含 {n} 个组件，编号为 1 到 {n}。除组件总数和编号外，你无法直接读取装配图纸的嵌套结构。

对于任意两个组件 i 和 j，如果构成 i 的子装配体层级与构成 j 的子装配体层级在装配拓扑上完全一致，则称 i 和 j 属于同一“标准化装配类型”。

你可以调用以下三种探测接口来获取BOM层级信息：

1. **装配一致性测试**：询问组件 i 和 j 的子装配体结构是否一致
   - 要求：i 不等于 j，且都在 1 到 {n} 范围内
   - 返回：是 或 否
   - 此类查询最多可进行 {p_budget} 次

2. **直接子件查询**：询问组件 i 需要多少个直接拼装的子件
   - 返回：非负整数
   - 与装配深度查询共享预算

3. **装配深度查询**：询问以组件 i 为顶层的装配体最大嵌套层级
   - 返回：正整数（不可拆分的底层基础零件深度为 1）
   - 与直接子件查询共享预算

直接子件查询和装配深度查询共享预算，总调用次数不超过 {q_budget} 次。

当逆向分析完成后，需要一次性提交 {m} 对组件配对，每对 (a,b) 满足 a 不等于 b，且每个组件编号在所有配对中最多出现一次。系统会检验每对组件的子装配体结构是否属于相同类型。

**成功条件**：正确配对数达到 {k} 对或以上。

每次只能发起一次调用。请使用以下 XML 格式：

- 装配一致性测试：
<query_isomorphic>3,5</query_isomorphic>

- 直接子件查询：
<query_degree>2</query_degree>

- 装配深度查询：
<query_height>4</query_height>

当你准备提交最终逆向报告时，提供 {m} 对组件配对，格式如下：
<answer>1,2;3,4;5,6;...</answer>
其中每个组件编号在所有配对中最多出现一次。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Precision Equipment BOM Reverse Engineering" task. Operating procedures are as follows:

The system has imported a fixed equipment assembly BOM tree T, containing {n} components numbered 1 to {n}. Beyond the total component count and IDs, the nested assembly blueprint is obscured.

For any two components i and j, if the sub-assembly hierarchy constituting i and the hierarchy constituting j are topologically identical, they share the same "Standardized Assembly Type".

You can invoke the following three probe interfaces to acquire BOM hierarchy data:

1. **Assembly Isomorphism Test**: Ask if the sub-assembly structures of components i and j are identical
   - Requirements: i not equal to j, both within range 1 to {n}
   - Returns: Yes or No
   - Maximum {p_budget} queries allowed

2. **Direct Sub-part Query**: Ask how many direct sub-parts are required to assemble component i
   - Returns: non-negative integer
   - Shares budget with assembly depth queries

3. **Assembly Depth Query**: Ask the maximum nesting levels of the assembly topped by component i
   - Returns: positive integer (indivisible base parts have a depth of 1)
   - Shares budget with direct sub-part queries

Direct sub-part queries and assembly depth queries share a budget with a total limit of {q_budget} queries.

Upon completing the reverse analysis, submit {m} pairs of components at once. Each pair (a,b) must satisfy a not equal to b, and each component ID may appear in at most one pair across all pairs. The system will verify if each pair's sub-assemblies share the same structural type.

**Success Condition**: The number of correct pairs reaches {k} or more.

Only one invocation per turn. Use the following XML format:

- Assembly Isomorphism Test:
<query_isomorphic>3,5</query_isomorphic>

- Direct Sub-part Query:
<query_degree>2</query_degree>

- Assembly Depth Query:
<query_height>4</query_height>

When ready to submit the final reverse engineering report, provide {m} pairs in this format:
<answer>1,2;3,4;5,6;...</answer>
Each component ID may appear in at most one pair.
"""

    contextualized_rule_zh_5 = """\
欢迎执行“跨国集团股权代持与控制架构穿透”任务，调查规则如下：

审计系统锁定了一棵固定的企业子公司控制架构树 T，包含 {n} 个壳公司/部门实体，编号为 1 到 {n}。除实体总数和编号外，你无法直接调阅集团的底层股权代持网络。

对于任意两个实体 i 和 j，如果以 i 为顶层控制方的下属全资控制链和以 j 为顶层控制方的下属控制链在组织架构上完全一致，则称 i 和 j 属于同一“资本运作矩阵”。

你可以发起以下三种查证请求来摸排控制权信息：

1. **架构同构测试**：询问实体 i 和 j 的下属控制链是否结构完全一致
   - 要求：i 不等于 j，且都在 1 到 {n} 范围内
   - 返回：是 或 否
   - 此类请求最多可进行 {p_budget} 次

2. **直系控股查询**：询问实体 i 直接全资控股了多少个下级实体
   - 返回：非负整数
   - 与控制层级查询共享预算

3. **控制层级查询**：询问以实体 i 为起点的下属控股链最大穿透层级
   - 返回：正整数（无对外投资的底层壳公司层级为 1）
   - 与直系控股查询共享预算

直系控股查询和控制层级查询共享预算，总次数不超过 {q_budget} 次。

当获取到充分的穿透证据后，需要一次性提交 {m} 对实体配对，每对实体 (a,b) 满足 a 不等于 b，且每个实体编号在所有配对中最多出现一次。系统会判定每对实体的下属控制网络是否属于相同的矩阵结构。

**成功条件**：正确找出 {k} 对或以上的同构实体。

每次只能发起一个请求。请使用以下 XML 格式：

- 架构同构测试：
<query_isomorphic>3,5</query_isomorphic>

- 直系控股查询：
<query_degree>2</query_degree>

- 控制层级查询：
<query_height>4</query_height>

当你准备提交最终合规调查报告时，提供 {m} 对配对，格式如下：
<answer>1,2;3,4;5,6;...</answer>
其中每个实体编号在所有配对中最多出现一次。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Multinational Conglomerate Corporate Control Structure Penetration" task. The investigation rules are as follows:

The audit system has locked onto a fixed corporate subsidiary control hierarchy tree T, containing {n} shell company/department entities, numbered 1 to {n}. Beyond the entity count and IDs, you cannot directly access the underlying equity holding network.

For any two entities i and j, if the subordinate fully-owned control chain led by i and the one led by j are perfectly identical in organizational structure, then i and j belong to the same "Capital Operation Matrix".

You can issue three types of verification requests to map out the control rights:

1. **Structural Isomorphism Test**: Ask if the subordinate control chains of entities i and j are perfectly identical
   - Requirements: i not equal to j, both within range 1 to {n}
   - Returns: Yes or No
   - Maximum {p_budget} requests allowed

2. **Direct Holding Query**: Ask how many lower-level entities entity i directly wholly owns
   - Returns: non-negative integer
   - Shares budget with control tier queries

3. **Control Tier Query**: Ask the maximum penetration depth of the subordinate holding chain originating from entity i
   - Returns: positive integer (bottom-tier shell companies with no investments have a depth of 1)
   - Shares budget with direct holding queries

Direct holding queries and control tier queries share a budget with a total limit of {q_budget} requests.

Upon obtaining sufficient penetration evidence, submit {m} pairs of entities at once. Each pair (a,b) must satisfy a not equal to b, and each entity ID may appear in at most one pair across all pairs. The system will judge if each pair's subordinate networks belong to identical matrix structures.

**Success Condition**: Successfully identify {k} or more correct isomorphic entity pairs.

Only one request per turn. Use the following XML format:

- Structural Isomorphism Test:
<query_isomorphic>3,5</query_isomorphic>

- Direct Holding Query:
<query_degree>2</query_degree>

- Control Tier Query:
<query_height>4</query_height>

When ready to submit the final compliance audit report, provide {m} pairs in this format:
<answer>1,2;3,4;5,6;...</answer>
Each entity ID may appear in at most one pair.
"""

    tags = ["answer", "query_isomorphic", "query_degree", "query_height"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "p_budget": 5,
                "q_budget": 10,
                "m": 3,
                "k": 2,
                "tree": [0, 1, 1, 2, 2, 3, 3, 1],
            },
            2: {
                "n": 10,
                "p_budget": 6,
                "q_budget": 12,
                "m": 4,
                "k": 3,
                "tree": [0, 1, 1, 2, 2, 3, 3, 1, 4, 4],
            },
            3: {
                "n": 12,
                "p_budget": 7,
                "q_budget": 14,
                "m": 5,
                "k": 4,
                "tree": [0, 1, 1, 2, 2, 3, 3, 1, 4, 4, 5, 5],
            },
            4: {
                "n": 15,
                "p_budget": 8,
                "q_budget": 16,
                "m": 6,
                "k": 5,
                "tree": [0, 1, 1, 2, 2, 3, 3, 1, 4, 4, 5, 5, 8, 8, 9],
            },
            5: {
                "n": 20,
                "p_budget": 10,
                "q_budget": 20,
                "m": 8,
                "k": 6,
                "tree": [0, 1, 1, 2, 2, 3, 3, 1, 4, 4, 5, 5, 8, 8, 9, 9, 10, 10, 11, 11],
            },
        },
        "en": {
            1: {
                "n": 8,
                "p_budget": 5,
                "q_budget": 10,
                "m": 3,
                "k": 2,
                "tree": [0, 1, 1, 2, 2, 3, 3, 1],
            },
            2: {
                "n": 10,
                "p_budget": 6,
                "q_budget": 12,
                "m": 4,
                "k": 3,
                "tree": [0, 1, 1, 2, 2, 3, 3, 1, 4, 4],
            },
            3: {
                "n": 12,
                "p_budget": 7,
                "q_budget": 14,
                "m": 5,
                "k": 4,
                "tree": [0, 1, 1, 2, 2, 3, 3, 1, 4, 4, 5, 5],
            },
            4: {
                "n": 15,
                "p_budget": 8,
                "q_budget": 16,
                "m": 6,
                "k": 5,
                "tree": [0, 1, 1, 2, 2, 3, 3, 1, 4, 4, 5, 5, 8, 8, 9],
            },
            5: {
                "n": 20,
                "p_budget": 10,
                "q_budget": 20,
                "m": 8,
                "k": 6,
                "tree": [0, 1, 1, 2, 2, 3, 3, 1, 4, 4, 5, 5, 8, 8, 9, 9, 10, 10, 11, 11],
            },
        },
    }

    def __init__(self, config):
        self.p_used = 0
        self.q_used = 0
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
        self._game_info["n"] = cfg["n"]
        self._game_info["p_budget"] = cfg["p_budget"]
        self._game_info["q_budget"] = cfg["q_budget"]
        self._game_info["m"] = cfg["m"]
        self._game_info["k"] = cfg["k"]

        self.parent = [0] + cfg["tree"]
        self.n = cfg["n"]
        self.p_budget = cfg["p_budget"]
        self.q_budget = cfg["q_budget"]
        self.m = cfg["m"]
        self.k = cfg["k"]

        self.children = [[] for _ in range(self.n + 1)]
        for i in range(1, self.n + 1):
            if self.parent[i] != 0:
                self.children[self.parent[i]].append(i)

        self._compute_degrees()
        self._compute_heights()
        
        self._compute_isomorphism()

    def _compute_degrees(self):
        self.degrees = [0] * (self.n + 1)
        for i in range(1, self.n + 1):
            self.degrees[i] = len(self.children[i])

    def _compute_heights(self):
        self.heights = [0] * (self.n + 1)
        
        def compute_height(node):
            if self.heights[node] > 0:
                return self.heights[node]
            
            if len(self.children[node]) == 0:
                self.heights[node] = 1
            else:
                max_child_height = 0
                for child in self.children[node]:
                    max_child_height = max(max_child_height, compute_height(child))
                self.heights[node] = 1 + max_child_height
            
            return self.heights[node]
        
        for i in range(1, self.n + 1):
            compute_height(i)

    def _get_subtree_signature(self, node):
        if len(self.children[node]) == 0:
            return ("leaf",)
        
        child_sigs = []
        for child in self.children[node]:
            child_sigs.append(self._get_subtree_signature(child))
        
        child_sigs.sort()
        return ("node", tuple(child_sigs))

    def _compute_isomorphism(self):
        self.isomorphic = {}
        self.signatures = {}
        
        for i in range(1, self.n + 1):
            self.signatures[i] = self._get_subtree_signature(i)
        
        for i in range(1, self.n + 1):
            for j in range(i, self.n + 1):
                key = (i, j) if i < j else (j, i)
                self.isomorphic[key] = (self.signatures[i] == self.signatures[j])

    def _check_isomorphic(self, i, j):
        if i == j:
            return True
        key = (i, j) if i < j else (j, i)
        return self.isomorphic.get(key, False)

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"].strip()
            pairs = raw_ans.split(";")
            
            if len(pairs) != self.m:
                return False
            
            correct_count = 0
            seen_nodes = set()
            
            for pair in pairs:
                nodes = pair.strip().split(",")
                if len(nodes) != 2:
                    return False
                
                try:
                    a, b = int(nodes[0].strip()), int(nodes[1].strip())
                except ValueError:
                    return False
                
                if a < 1 or a > self.n or b < 1 or b > self.n or a == b:
                    return False
                
                if a in seen_nodes or b in seen_nodes:
                    return False
                seen_nodes.add(a)
                seen_nodes.add(b)
                
                if self._check_isomorphic(a, b):
                    correct_count += 1
            
            return correct_count >= self.k
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            err_range = "错误：节点编号超出范围。"
            err_same = "错误：同构测试要求两个不同的节点。"
            err_budget_p = f"错误：同构测试次数已用完（最多{self.p_budget}次）。"
            err_budget_q = f"错误：度数/高度查询次数已用完（最多{self.q_budget}次）。"
            err_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            err_range = "Error: Node ID out of range."
            err_same = "Error: Isomorphism test requires two different nodes."
            err_budget_p = f"Error: Isomorphism test budget exhausted (max {self.p_budget})."
            err_budget_q = f"Error: Degree/height query budget exhausted (max {self.q_budget})."
            err_format = "Error: Invalid format."

        if "query_isomorphic" in parsed_info:
            if self.p_used >= self.p_budget:
                return err_budget_p
            
            try:
                raw = parsed_info["query_isomorphic"].strip()
                nodes = raw.split(",")
                if len(nodes) != 2:
                    return err_format
                
                i, j = int(nodes[0].strip()), int(nodes[1].strip())
                
                if i < 1 or i > self.n or j < 1 or j > self.n:
                    return err_range
                
                if i == j:
                    return err_same
                
                self.p_used += 1
                return yes_res if self._check_isomorphic(i, j) else no_res
                
            except (ValueError, IndexError):
                return err_format

        elif "query_degree" in parsed_info:
            if self.q_used >= self.q_budget:
                return err_budget_q
            
            try:
                i = int(parsed_info["query_degree"].strip())
                if i < 1 or i > self.n:
                    return err_range
                
                self.q_used += 1
                return str(self.degrees[i])
                
            except ValueError:
                return err_format

        elif "query_height" in parsed_info:
            if self.q_used >= self.q_budget:
                return err_budget_q
            
            try:
                i = int(parsed_info["query_height"].strip())
                if i < 1 or i > self.n:
                    return err_range
                
                self.q_used += 1
                return str(self.heights[i])
                
            except ValueError:
                return err_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            return str(int(correct) + 1)
        except ValueError:
            pass
        
        mapping = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes",
            "YES": "NO",
            "NO": "YES",
            "yes": "no",
            "no": "yes"
        }
        
        if correct in mapping:
            return mapping[correct]
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            ans_yes = "是"
            ans_no = "否"
        else:
            ans_yes = "Yes"
            ans_no = "No"

        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                is_iso = self._check_isomorphic(i, j)
                ans = ans_yes if is_iso else ans_no
                query_content = f"<query_isomorphic>{i},{j}</query_isomorphic>"
                queries.append({
                    "query": query_content,
                    "answer": ans
                })

        for i in range(1, self.n + 1):
            ans = str(self.degrees[i])
            query_content = f"<query_degree>{i}</query_degree>"
            queries.append({
                "query": query_content,
                "answer": ans
            })

        for i in range(1, self.n + 1):
            ans = str(self.heights[i])
            query_content = f"<query_height>{i}</query_height>"
            queries.append({
                "query": query_content,
                "answer": ans
            })
            
        return queries