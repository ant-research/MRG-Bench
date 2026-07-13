from .base import Game
import random


class ClusteredGraphGame(Game):

    game_rule_zh = """\
我们来玩一个"簇连接推理"游戏。规则如下：

游戏设定了一个由 {m} 个簇组成的连通无向图 G。每个簇内部的顶点相互完全连接（即簇内任意两点间有边）。在每个簇中，恰有一个特殊的"连接器"顶点负责与其他簇连接。

关键约束：
- 所有跨簇的边仅在连接器顶点之间存在
- 连接器顶点按照某种拓扑模板连接（路径或环）
- 每个簇的连接器由一条统一的命名规则确定（例如：簇内编号最小或最大者）

你的目标是通过查询推断出：对图中每个顶点 v，删除它后剩余图的连通分量数。

## 已知信息

簇的划分：
{cluster_info}

可能的连接器命名规则：
{rules_description}

交互预算：你最多可以进行 {budget} 次查询。

## 查询方式（每次只能使用一种）

1. 单点删除查询：询问删除某个顶点后的连通分量数
<query_delete>顶点名称</query_delete>

2. 比较查询：比较删除两个顶点后的连通分量数大小关系
<query_compare>顶点1,顶点2</query_compare>

比较查询将返回：
- "大于"：删除顶点1后的分量数大于删除顶点2后
- "小于"：删除顶点1后的分量数小于删除顶点2后
- "等于"：两者分量数相同

## 提交答案格式

当你准备提交答案时，必须包含两部分：

1. 对每个顶点的预测（格式：顶点名=分量数）
2. 你推断的模板类型（路径 或 环）
3. 你推断的命名规则（规则描述）

<answer>
predictions=v1=2,v2=1,v3=2,...
template=路径
rule=簇内编号最小者
</answer>

注意：predictions 中必须包含所有顶点，顺序不限，用逗号分隔。
"""

    game_rule_en = """\
Let's play a "Clustered Graph Reasoning" game. Here are the rules:

The game features a connected undirected graph G composed of {m} clusters. Within each cluster, vertices are fully connected (i.e., every pair has an edge). In each cluster, exactly one special "connector" vertex is responsible for connecting to other clusters.

Key constraints:
- All inter-cluster edges exist only between connector vertices
- Connector vertices are connected according to a topological template (Path or Cycle)
- Each cluster's connector is determined by a uniform naming rule (e.g., smallest or largest ID in cluster)

Your goal is to infer through queries: for each vertex v in the graph, the number of connected components after removing it.

## Known Information

Cluster division:
{cluster_info}

Possible connector naming rules:
{rules_description}

Query budget: You may perform at most {budget} queries.

## Query Methods (only one per turn)

1. Deletion query: Ask the number of connected components after deleting a vertex
<query_delete>vertex_name</query_delete>

2. Comparison query: Compare the component counts after deleting two vertices
<query_compare>vertex1,vertex2</query_compare>

Comparison query returns:
- "greater": component count after deleting vertex1 is greater than vertex2
- "less": component count after deleting vertex1 is less than vertex2
- "equal": both have the same component count

## Answer Submission Format

When submitting your answer, you must include:

1. Prediction for each vertex (format: vertex_name=count)
2. Your inferred template type (Path or Cycle)
3. Your inferred naming rule (rule description)

<answer>
predictions=v1=2,v2=1,v3=2,...
template=Path
rule=smallest ID in cluster
</answer>

Note: predictions must include all vertices, order doesn't matter, separated by commas.
"""

    contextualized_rule_zh_1 = """\
你是一名城市交通规划师，当前正在分析一个"跨区路网连通性"问题。规则如下：

系统由 {m} 个交通大区组成。每个大区内部的所有交通枢纽之间都建有直达快速路（即区内任意两个枢纽互通）。在每个大区中，恰有一个特殊的"跨区枢纽"负责与其他大区连接。

关键约束：
- 所有跨区的交通路线仅在"跨区枢纽"之间存在
- 跨区枢纽按照某种路网拓扑模板连接（线型走廊/路径 或 环状路网/环）
- 每个大区的跨区枢纽由一条统一的命名规则确定（例如：大区内编号最小或最大者）

你的目标是通过模拟封闭测试推断出：对路网中每个枢纽 v，将其彻底封闭停运后，剩余路网会被分割成的相互无法到达的独立孤岛数量。

## 已知信息

大区划分：
{cluster_info}

可能的跨区枢纽命名规则：
{rules_description}

交互预算：你最多可以进行 {budget} 次模拟。

## 模拟方式（每次只能使用一种）

1. 单点封闭模拟：询问封闭某个枢纽后，路网变成的独立孤岛数量
<query_delete>枢纽名称</query_delete>

2. 比较模拟：比较封闭两个不同枢纽后的孤岛数量大小关系
<query_compare>枢纽1,枢纽2</query_compare>

比较模拟将返回：
- "大于"：封闭枢纽1后的孤岛数量大于封闭枢纽2后
- "小于"：封闭枢纽1后的孤岛数量小于封闭枢纽2后
- "等于"：两者孤岛数量相同

## 提交答案格式

当你准备提交最终规划评估时，必须包含两部分：

1. 对每个枢纽的孤岛数量预测（格式：枢纽名=孤岛数）
2. 你推断的路网拓扑模板（路径 或 环）
3. 你推断的命名规则（规则描述）

<answer>
predictions=v1=2,v2=1,v3=2,...
template=路径
rule=簇内编号最小者
</answer>

注意：predictions 中必须包含所有枢纽，顺序不限，用逗号分隔。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
You are an urban traffic planner analyzing an "Inter-district Network Connectivity" problem. Here are the rules:

The system consists of {m} traffic districts. Within each district, all transport hubs are fully connected by direct expressways (i.e., every pair of hubs is mutually accessible). In each district, exactly one special "gateway hub" is responsible for connecting to other districts.

Key constraints:
- All inter-district routes exist only between gateway hubs
- Gateway hubs are connected according to a network topological template (Linear Corridor/Path or Circular Network/Cycle)
- Each district's gateway hub is determined by a uniform naming rule (e.g., smallest or largest ID in the district)

Your goal is to infer through simulation queries: for each hub v in the network, the number of independent, unreachable islands the remaining network will be divided into after it is completely closed down.

## Known Information

District division:
{cluster_info}

Possible gateway hub naming rules:
{rules_description}

Simulation budget: You may perform at most {budget} simulations.

## Simulation Methods (only one per turn)

1. Closure query: Ask the number of isolated islands after closing a specific hub
<query_delete>hub_name</query_delete>

2. Comparison query: Compare the island counts after closing two different hubs
<query_compare>hub1,hub2</query_compare>

Comparison query returns:
- "greater": island count after closing hub1 is greater than hub2
- "less": island count after closing hub1 is less than hub2
- "equal": both have the same island count

## Answer Submission Format

When submitting your final evaluation, you must include:

1. Prediction for each hub (format: hub_name=count)
2. Your inferred network template type (Path or Cycle)
3. Your inferred naming rule (rule description)

<answer>
predictions=v1=2,v2=1,v3=2,...
template=Path
rule=smallest ID in cluster
</answer>

Note: predictions must include all hubs, order doesn't matter, separated by commas.
"""

    contextualized_rule_zh_2 = """\
你是一名医疗网络应急协调员，正在排查"跨院区资源调配"系统的抗压能力。规则如下：

系统由 {m} 个医疗院区组成。每个院区内部的所有科室之间通过内部传送带完全互联（即任意两科室间可直接调动物资）。在每个院区中，恰有一个特殊的"调配中心"负责与其他院区连接。

关键约束：
- 所有跨院区的物资专线仅在"调配中心"之间存在
- 调配中心按照某种拓扑模板连接（链式主干/路径 或 循环闭环/环）
- 每个院区的调配中心由一条统一的命名规则确定（例如：簇内编号最小或最大者）

你的目标是通过应急演练推断出：对网络中每个科室 v，将其停诊关闭后，剩余医疗网络会被分割成的相互无法调配物资的独立分诊网络数量。

## 已知信息

院区划分：
{cluster_info}

可能的调配中心命名规则：
{rules_description}

交互预算：你最多可以进行 {budget} 次演练。

## 演练方式（每次只能使用一种）

1. 单点关闭演练：询问关闭某个科室后，网络变成的独立分诊网络数量
<query_delete>科室名称</query_delete>

2. 比较演练：比较关闭两个不同科室后的分诊网络数量大小关系
<query_compare>科室1,科室2</query_compare>

比较演练将返回：
- "大于"：关闭科室1后的分诊网络数量大于关闭科室2后
- "小于"：关闭科室1后的分诊网络数量小于关闭科室2后
- "等于"：两者数量相同

## 提交答案格式

当你准备提交应急报告时，必须包含两部分：

1. 对每个科室的断网数量预测（格式：科室名=分诊网络数）
2. 你推断的拓扑模板（路径 或 环）
3. 你推断的命名规则（规则描述）

<answer>
predictions=v1=2,v2=1,v3=2,...
template=路径
rule=簇内编号最小者
</answer>

注意：predictions 中必须包含所有科室，顺序不限，用逗号分隔。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
You are a medical network emergency coordinator assessing the resilience of an "Inter-campus Resource Dispatch" system. Here are the rules:

The system consists of {m} hospital campuses. Within each campus, all medical wards are fully interconnected via internal transport belts (i.e., supplies can be directly transferred between any two wards). In each campus, exactly one special "dispatch center" is responsible for connecting to other campuses.

Key constraints:
- All inter-campus supply lines exist only between dispatch centers
- Dispatch centers are connected according to a topological template (Chain Mainline/Path or Closed Loop/Cycle)
- Each campus's dispatch center is determined by a uniform naming rule (e.g., smallest or largest ID in cluster)

Your goal is to infer through emergency drills: for each ward v in the network, the number of independent, disconnected triage networks the remaining system will be divided into after shutting it down.

## Known Information

Campus division:
{cluster_info}

Possible dispatch center naming rules:
{rules_description}

Drill budget: You may perform at most {budget} drills.

## Drill Methods (only one per turn)

1. Shutdown drill: Ask the number of independent triage networks after shutting down a specific ward
<query_delete>ward_name</query_delete>

2. Comparison drill: Compare the network counts after shutting down two different wards
<query_compare>ward1,ward2</query_compare>

Comparison drill returns:
- "greater": network count after shutting down ward1 is greater than ward2
- "less": network count after shutting down ward1 is less than ward2
- "equal": both have the same count

## Answer Submission Format

When submitting your emergency report, you must include:

1. Prediction for each ward (format: ward_name=count)
2. Your inferred topological template (Path or Cycle)
3. Your inferred naming rule (rule description)

<answer>
predictions=v1=2,v2=1,v3=2,...
template=Path
rule=smallest ID in cluster
</answer>

Note: predictions must include all wards, order doesn't matter, separated by commas.
"""

    contextualized_rule_zh_3 = """\
你是一名学术网络架构师，正在评估大学联盟的"跨院际学术交流"机制。规则如下：

联盟由 {m} 个学院组成。每个学院内部的所有研究室之间都接入了同一内部协作网，可自由直接交流。在每个学院中，恰有一个特殊的"联络办公室"负责与其他学院进行跨院交流。

关键约束：
- 所有跨院的学术通道仅在"联络办公室"之间存在
- 联络办公室按照某种架构模板连接（线性主干/路径 或 环形回路/环）
- 每个学院的联络办公室由一条统一的命名规则确定（例如：簇内编号最小或最大者）

你的目标是通过剥离测试推断出：对网络中每个研究室 v，将其撤销关闭后，剩余学术网络会被分割成的相互无法交流的独立学术圈数量。

## 已知信息

学院划分：
{cluster_info}

可能的联络办公室命名规则：
{rules_description}

交互预算：你最多可以进行 {budget} 次测试。

## 测试方式（每次只能使用一种）

1. 单点撤销测试：询问撤销某个研究室后，网络变成的独立学术圈数量
<query_delete>研究室名称</query_delete>

2. 比较测试：比较撤销两个不同研究室后的学术圈数量大小关系
<query_compare>研究室1,研究室2</query_compare>

比较测试将返回：
- "大于"：撤销研究室1后的学术圈数量大于撤销研究室2后
- "小于"：撤销研究室1后的学术圈数量小于撤销研究室2后
- "等于"：两者数量相同

## 提交答案格式

当你准备提交架构评估时，必须包含两部分：

1. 对每个研究室的孤岛数量预测（格式：研究室名=学术圈数量）
2. 你推断的架构模板（路径 或 环）
3. 你推断的命名规则（规则描述）

<answer>
predictions=v1=2,v2=1,v3=2,...
template=路径
rule=簇内编号最小者
</answer>

注意：predictions 中必须包含所有研究室，顺序不限，用逗号分隔。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
You are an academic network architect evaluating the "Inter-faculty Academic Exchange" mechanism of a university alliance. Here are the rules:

The alliance consists of {m} faculties. Within each faculty, all research labs are connected to the same internal collaboration grid and can communicate freely. In each faculty, exactly one special "liaison office" is responsible for cross-faculty exchanges.

Key constraints:
- All inter-faculty academic channels exist only between liaison offices
- Liaison offices are connected according to an architectural template (Linear Backbone/Path or Circular Loop/Cycle)
- Each faculty's liaison office is determined by a uniform naming rule (e.g., smallest or largest ID in cluster)

Your goal is to infer through divestment testing: for each research lab v, the number of independent, non-communicating academic circles the remaining network will be divided into after it is closed down.

## Known Information

Faculty division:
{cluster_info}

Possible liaison office naming rules:
{rules_description}

Testing budget: You may perform at most {budget} tests.

## Testing Methods (only one per turn)

1. Closure test: Ask the number of independent academic circles after closing a specific lab
<query_delete>lab_name</query_delete>

2. Comparison test: Compare the circle counts after closing two different labs
<query_compare>lab1,lab2</query_compare>

Comparison test returns:
- "greater": circle count after closing lab1 is greater than lab2
- "less": circle count after closing lab1 is less than lab2
- "equal": both have the same count

## Answer Submission Format

When submitting your architecture evaluation, you must include:

1. Prediction for each lab (format: lab_name=count)
2. Your inferred architectural template (Path or Cycle)
3. Your inferred naming rule (rule description)

<answer>
predictions=v1=2,v2=1,v3=2,...
template=Path
rule=smallest ID in cluster
</answer>

Note: predictions must include all research labs, order doesn't matter, separated by commas.
"""

    contextualized_rule_zh_4 = """\
你是一名工业系统工程师，正在检修大型联合工厂的"跨厂区物流连通性"故障。规则如下：

联合工厂由 {m} 个厂区组成。每个厂区内部的所有生产车间都通过内部流水线完全互联（即物资可在任意两车间流转）。在每个厂区中，恰有一个特殊的"物流中转站"负责与其他厂区连接。

关键约束：
- 所有跨厂区的运输专线仅在"物流中转站"之间存在
- 物流中转站按照某种干线模板连接（流水线主轴/路径 或 闭环输送带/环）
- 每个厂区的中转站由一条统一的命名规则确定（例如：簇内编号最小或最大者）

你的目标是通过停工检修测试推断出：对系统中每个车间 v，将其停工切断后，剩余生产网络会被分割成的相互断开的独立流水线分系统数量。

## 已知信息

厂区划分：
{cluster_info}

可能的中转站命名规则：
{rules_description}

交互预算：你最多可以进行 {budget} 次测试。

## 测试方式（每次只能使用一种）

1. 单点停工测试：询问停工某个车间后，网络变成的独立分系统数量
<query_delete>车间名称</query_delete>

2. 比较测试：比较停工两个不同车间后的分系统数量大小关系
<query_compare>车间1,车间2</query_compare>

比较测试将返回：
- "大于"：停工车间1后的分系统数量大于停工车间2后
- "小于"：停工车间1后的分系统数量小于停工车间2后
- "等于"：两者数量相同

## 提交答案格式

当你准备提交检修报告时，必须包含两部分：

1. 对每个车间的分系统数量预测（格式：车间名=分系统数）
2. 你推断的干线模板（路径 或 环）
3. 你推断的命名规则（规则描述）

<answer>
predictions=v1=2,v2=1,v3=2,...
template=路径
rule=簇内编号最小者
</answer>

注意：predictions 中必须包含所有车间，顺序不限，用逗号分隔。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
You are an industrial systems engineer troubleshooting the "Inter-zone Logistics Connectivity" of a large integrated plant. Here are the rules:

The integrated plant consists of {m} factory zones. Within each zone, all production workshops are fully interconnected via internal assembly lines (i.e., materials can flow between any two workshops). In each zone, exactly one special "logistics hub" is responsible for connecting to other zones.

Key constraints:
- All inter-zone transport lines exist only between logistics hubs
- Logistics hubs are connected according to a mainline template (Mainline Axis/Path or Closed Conveyor Loop/Cycle)
- Each zone's logistics hub is determined by a uniform naming rule (e.g., smallest or largest ID in cluster)

Your goal is to infer through shutdown maintenance tests: for each workshop v in the system, the number of independent, disconnected assembly sub-systems the remaining network will be divided into after it is shut down and isolated.

## Known Information

Factory zone division:
{cluster_info}

Possible logistics hub naming rules:
{rules_description}

Testing budget: You may perform at most {budget} tests.

## Testing Methods (only one per turn)

1. Shutdown test: Ask the number of independent sub-systems after shutting down a specific workshop
<query_delete>workshop_name</query_delete>

2. Comparison test: Compare the sub-system counts after shutting down two different workshops
<query_compare>workshop1,workshop2</query_compare>

Comparison test returns:
- "greater": sub-system count after shutting down workshop1 is greater than workshop2
- "less": sub-system count after shutting down workshop1 is less than workshop2
- "equal": both have the same count

## Answer Submission Format

When submitting your maintenance report, you must include:

1. Prediction for each workshop (format: workshop_name=count)
2. Your inferred mainline template (Path or Cycle)
3. Your inferred naming rule (rule description)

<answer>
predictions=v1=2,v2=1,v3=2,...
template=Path
rule=smallest ID in cluster
</answer>

Note: predictions must include all workshops, order doesn't matter, separated by commas.
"""

    contextualized_rule_zh_5 = """\
你是一名跨区司法协调员，正在审查一套"跨管辖区案件移交"体系的机制漏洞。规则如下：

该司法网络由 {m} 个管辖区组成。每个管辖区内部的所有办案小组都共享内部卷宗系统，实现完全互通。在每个管辖区中，恰有一个特殊的"联合办案中心"负责与其他管辖区进行案件移交。

关键约束：
- 所有跨管辖区的移交流程仅在"联合办案中心"之间存在
- 联合办案中心按照某种协调机制链条连接（层级主线/路径 或 闭环反馈网/环）
- 每个管辖区的办案中心由一条统一的命名规则确定（例如：簇内编号最小或最大者）

你的目标是通过权限撤销测试推断出：对网络中每个小组 v，将其撤销权限后，剩余司法网络会被分割成的相互无法移交案件的独立办案孤岛数量。

## 已知信息

管辖区划分：
{cluster_info}

可能的办案中心命名规则：
{rules_description}

交互预算：你最多可以进行 {budget} 次测试。

## 测试方式（每次只能使用一种）

1. 单点撤销测试：询问撤销某个办案小组后，网络变成的独立孤岛数量
<query_delete>小组名称</query_delete>

2. 比较测试：比较撤销两个不同小组后的孤岛数量大小关系
<query_compare>小组1,小组2</query_compare>

比较测试将返回：
- "大于"：撤销小组1后的孤岛数量大于撤销小组2后
- "小于"：撤销小组1后的孤岛数量小于撤销小组2后
- "等于"：两者数量相同

## 提交答案格式

当你准备提交审查结论时，必须包含两部分：

1. 对每个办案小组的孤岛数量预测（格式：小组名=孤岛数）
2. 你推断的协调机制链条（路径 或 环）
3. 你推断的命名规则（规则描述）

<answer>
predictions=v1=2,v2=1,v3=2,...
template=路径
rule=簇内编号最小者
</answer>

注意：predictions 中必须包含所有办案小组，顺序不限，用逗号分隔。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
You are a cross-regional judicial coordinator reviewing the mechanical loopholes of an "Inter-jurisdiction Case Transfer" system. Here are the rules:

The judicial network consists of {m} jurisdictions. Within each jurisdiction, all case teams share an internal dossier system, achieving complete interconnectivity. In each jurisdiction, exactly one special "joint case center" is responsible for transferring cases to other jurisdictions.

Key constraints:
- All inter-jurisdictional transfer processes exist only between joint case centers
- Joint case centers are connected according to a coordination chain (Hierarchical Mainline/Path or Closed Feedback Loop/Cycle)
- Each jurisdiction's joint case center is determined by a uniform naming rule (e.g., smallest or largest ID in cluster)

Your goal is to infer through revocation testing: for each team v in the network, the number of independent, isolated case-handling islands the remaining judicial network will be divided into after its authority is revoked.

## Known Information

Jurisdiction division:
{cluster_info}

Possible joint case center naming rules:
{rules_description}

Testing budget: You may perform at most {budget} tests.

## Testing Methods (only one per turn)

1. Revocation test: Ask the number of isolated islands after revoking a specific case team
<query_delete>team_name</query_delete>

2. Comparison test: Compare the island counts after revoking two different case teams
<query_compare>team1,team2</query_compare>

Comparison test returns:
- "greater": island count after revoking team1 is greater than team2
- "less": island count after revoking team1 is less than team2
- "equal": both have the same count

## Answer Submission Format

When submitting your review conclusion, you must include:

1. Prediction for each case team (format: team_name=count)
2. Your inferred coordination chain (Path or Cycle)
3. Your inferred naming rule (rule description)

<answer>
predictions=v1=2,v2=1,v3=2,...
template=Path
rule=smallest ID in cluster
</answer>

Note: predictions must include all case teams, order doesn't matter, separated by commas.
"""

    tags = ["answer", "query_delete", "query_compare"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    # 难度配置：
    # 1 (简单) - 3个簇，路径模板，规则：最小编号
    # 2 (中等偏下) - 4个簇，环模板，规则：最大编号
    # 3 (中等偏上) - 5个簇，路径模板，规则：最小编号
    # 4 (较难) - 6个簇，环模板，规则：最大编号
    # 5 (难) - 7个簇，路径模板，规则：最小编号

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "m": 3,
                "clusters": [["v1", "v2"], ["v3", "v4"], ["v5", "v6"]],
                "template": "路径",
                "rule": "簇内编号最小者",
                "budget": 8,
            },
            2: {
                "m": 4,
                "clusters": [["v1", "v2", "v3"], ["v4", "v5"], ["v6", "v7"], ["v8", "v9"]],
                "template": "环",
                "rule": "簇内编号最大者",
                "budget": 12,
            },
            3: {
                "m": 5,
                "clusters": [["v1", "v2"], ["v3", "v4"], ["v5", "v6"], ["v7", "v8"], ["v9", "v10"]],
                "template": "路径",
                "rule": "簇内编号最小者",
                "budget": 15,
            },
            4: {
                "m": 6,
                "clusters": [["v1", "v2"], ["v3", "v4"], ["v5", "v6"], ["v7", "v8"], ["v9", "v10"], ["v11", "v12"]],
                "template": "环",
                "rule": "簇内编号最大者",
                "budget": 18,
            },
            5: {
                "m": 7,
                "clusters": [["v1", "v2"], ["v3", "v4"], ["v5", "v6"], ["v7", "v8"], ["v9", "v10"], ["v11", "v12"], ["v13", "v14"]],
                "template": "路径",
                "rule": "簇内编号最小者",
                "budget": 20,
            },
        },
        "en": {
            1: {
                "m": 3,
                "clusters": [["v1", "v2"], ["v3", "v4"], ["v5", "v6"]],
                "template": "Path",
                "rule": "smallest ID in cluster",
                "budget": 8,
            },
            2: {
                "m": 4,
                "clusters": [["v1", "v2", "v3"], ["v4", "v5"], ["v6", "v7"], ["v8", "v9"]],
                "template": "Cycle",
                "rule": "largest ID in cluster",
                "budget": 12,
            },
            3: {
                "m": 5,
                "clusters": [["v1", "v2"], ["v3", "v4"], ["v5", "v6"], ["v7", "v8"], ["v9", "v10"]],
                "template": "Path",
                "rule": "smallest ID in cluster",
                "budget": 15,
            },
            4: {
                "m": 6,
                "clusters": [["v1", "v2"], ["v3", "v4"], ["v5", "v6"], ["v7", "v8"], ["v9", "v10"], ["v11", "v12"]],
                "template": "Cycle",
                "rule": "largest ID in cluster",
                "budget": 18,
            },
            5: {
                "m": 7,
                "clusters": [["v1", "v2"], ["v3", "v4"], ["v5", "v6"], ["v7", "v8"], ["v9", "v10"], ["v11", "v12"], ["v13", "v14"]],
                "template": "Path",
                "rule": "smallest ID in cluster",
                "budget": 20,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置和图结构"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 基本配置
        self._game_info["m"] = cfg["m"]
        self._game_info["budget"] = cfg["budget"]
        self.clusters = cfg["clusters"]
        self.template = cfg["template"]
        self.rule = cfg["rule"]
        self.query_count = 0
        
        # 辅助函数：按数值提取顶点编号进行比较
        def vertex_key(v):
            """从顶点名中提取数字部分用于数值比较"""
            import re
            m = re.search(r'(\d+)', v)
            return int(m.group(1)) if m else v
        
        # 确定连接器顶点
        self.connectors = []
        for cluster in self.clusters:
            if lang == "zh":
                if self.rule == "簇内编号最小者":
                    connector = min(cluster, key=vertex_key)
                else:  # 簇内编号最大者
                    connector = max(cluster, key=vertex_key)
            else:
                if self.rule == "smallest ID in cluster":
                    connector = min(cluster, key=vertex_key)
                else:  # largest ID in cluster
                    connector = max(cluster, key=vertex_key)
            self.connectors.append(connector)
        
        # 构建簇信息描述
        cluster_lines = []
        for i, cluster in enumerate(self.clusters, 1):
            if lang == "zh":
                cluster_lines.append(f"簇 {i}：{', '.join(cluster)}")
            else:
                cluster_lines.append(f"Cluster {i}: {', '.join(cluster)}")
        self._game_info["cluster_info"] = "\n".join(cluster_lines)
        
        # 规则描述
        if lang == "zh":
            self._game_info["rules_description"] = "1. 簇内编号最小者\n2. 簇内编号最大者"
        else:
            self._game_info["rules_description"] = "1. smallest ID in cluster\n2. largest ID in cluster"
        
        # 计算ground truth：每个顶点删除后的连通分量数
        self.ground_truth = {}
        all_vertices = [v for cluster in self.clusters for v in cluster]
        
        for vertex in all_vertices:
            self.ground_truth[vertex] = self._compute_components_after_deletion(vertex)

    def _compute_components_after_deletion(self, vertex):
        """计算删除指定顶点后的连通分量数"""
        # 找到顶点所在的簇
        vertex_cluster_idx = None
        is_connector = vertex in self.connectors
        
        for i, cluster in enumerate(self.clusters):
            if vertex in cluster:
                vertex_cluster_idx = i
                break
        
        # 如果是连接器顶点
        if is_connector:
            is_path = (self.template == "路径" or self.template == "Path")
            m = len(self.clusters)
            
            if is_path:
                # 路径模板：端点连接器→2个分量，中间连接器→3个分量
                if vertex_cluster_idx == 0 or vertex_cluster_idx == m - 1:
                    return 2
                else:
                    return 3
            else:
                # 环模板：任何连接器→2个分量
                return 2
        else:
            # 非连接器顶点：删除后仍然连通→1个分量
            return 1

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        try:
            raw_ans = parsed_info["answer"]
            
            # 解析答案的各个部分
            lines = [line.strip() for line in raw_ans.strip().split("\n") if line.strip()]
            ans_dict = {}
            
            for line in lines:
                if "=" in line:
                    k, v = line.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            # 检查必需字段
            if "predictions" not in ans_dict:
                return False
            if "template" not in ans_dict:
                return False
            if "rule" not in ans_dict:
                return False
            
            # 检查 template 是否正确
            submitted_template = ans_dict["template"].strip()
            if submitted_template != self.template:
                return False
            
            # 检查 rule 是否正确
            submitted_rule = ans_dict["rule"].strip()
            if submitted_rule != self.rule:
                return False
            
            # 解析预测结果
            predictions_str = ans_dict["predictions"]
            predictions = {}
            
            for item in predictions_str.split(","):
                item = item.strip()
                if "=" in item:
                    v, count = item.split("=")
                    try:
                        predictions[v.strip()] = int(count.strip())
                    except ValueError:
                        return False
            
            # 检查是否覆盖所有顶点
            all_vertices = set(self.ground_truth.keys())
            if set(predictions.keys()) != all_vertices:
                return False
            
            # 检查每个顶点的预测是否正确
            for vertex, predicted_count in predictions.items():
                if predicted_count != self.ground_truth[vertex]:
                    return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑处理"""
        # 检查预算
        self.query_count += 1
        if self.query_count > self._game_info["budget"]:
            if self.config.language == "zh":
                raise ValueError(f"查询次数超过预算限制 {self._game_info['budget']}")
            else:
                raise ValueError(f"Query count exceeds budget limit {self._game_info['budget']}")
        
        # 处理删除查询
        if "query_delete" in parsed_info:
            vertex = parsed_info["query_delete"].strip()
            
            # 检查顶点是否存在
            if vertex not in self.ground_truth:
                if self.config.language == "zh":
                    return "错误：顶点不存在"
                else:
                    return "Error: Vertex does not exist"
            
            return str(self.ground_truth[vertex])
        
        # 处理比较查询
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 2:
                    raise ValueError("Invalid format")
                
                v1, v2 = parts
                
                if v1 not in self.ground_truth or v2 not in self.ground_truth:
                    if self.config.language == "zh":
                        return "错误：顶点不存在"
                    else:
                        return "Error: Vertex does not exist"
                
                count1 = self.ground_truth[v1]
                count2 = self.ground_truth[v2]
                
                if self.config.language == "zh":
                    if count1 > count2:
                        return "大于"
                    elif count1 < count2:
                        return "小于"
                    else:
                        return "等于"
                else:
                    if count1 > count2:
                        return "greater"
                    elif count1 < count2:
                        return "less"
                    else:
                        return "equal"
                        
            except Exception as e:
                if self.config.language == "zh":
                    return "错误：查询格式无效"
                else:
                    return "Error: Invalid query format"
        
        else:
            if self.config.language == "zh":
                raise ValueError("未找到有效的查询标签")
            else:
                raise ValueError("No valid query tag found")

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 若 correct 是纯整数字符串（单点删除查询的结果）
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 处理比较查询结果
        compare_map_zh = {"大于": "小于", "小于": "大于", "等于": "大于"}
        compare_map_en = {"greater": "less", "less": "greater", "equal": "greater"}
        
        if correct in compare_map_zh:
            return compare_map_zh[correct]
        if correct in compare_map_en:
            return compare_map_en[correct]
        
        # 替换关键词
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            # 简单的大小写敏感替换
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            if "No" in correct:
                return correct.replace("No", "Yes")
            if "yes" in correct:
                return correct.replace("yes", "no")
            if "no" in correct:
                return correct.replace("no", "yes")
                
        # 若都不匹配
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串
                "answer": str,   # 正确答案
            }
        """
        queries = []
        all_vertices = [v for cluster in self.clusters for v in cluster]
        is_zh = (self.config.language == "zh")

        # 1. 单点删除查询 <query_delete>v</query_delete>
        for v in all_vertices:
            query_str = f"<query_delete>{v}</query_delete>"
            ans = str(self.ground_truth[v])
            queries.append({
                "query": query_str,
                "answer": ans
            })

        # 2. 比较查询 <query_compare>v1,v2</query_compare>
        for i, v1 in enumerate(all_vertices):
            for j, v2 in enumerate(all_vertices):
                if i >= j:
                    continue
                query_str = f"<query_compare>{v1},{v2}</query_compare>"
                
                c1 = self.ground_truth[v1]
                c2 = self.ground_truth[v2]
                
                if is_zh:
                    if c1 > c2:
                        ans = "大于"
                    elif c1 < c2:
                        ans = "小于"
                    else:
                        ans = "等于"
                else:
                    if c1 > c2:
                        ans = "greater"
                    elif c1 < c2:
                        ans = "less"
                    else:
                        ans = "equal"
                
                queries.append({
                    "query": query_str,
                    "answer": ans
                })

        return queries