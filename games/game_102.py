import random
import re
from collections import deque
from .base import Game

class GraphDiameterGame(Game):

    game_rule_zh = """\
我们来玩一个"图直径推断"游戏，规则如下：

存在一个未知的连通、无向、无权图 G=(V,E)，顶点集 V 的规模为 {n} 个顶点，每个顶点有唯一标识。边集 E 不可见。所有边权为 1，最短路距离为整数。

定义：
- dist(u,v) 表示顶点 u 与 v 之间的最短路长度
- ecc(v) = max_u dist(v,u) 表示顶点 v 的离心率（即从 v 出发到其他顶点的最大距离）
- 图的直径 D = max_v ecc(v) = max_(u,v) dist(u,v)（即图中任意两点间的最大距离）

你的目标是：通过允许的查询操作，推断出图的直径 D。

你可以进行以下三种操作：

1. **探测操作 PROBE X**（X 是顶点标识）：
   - 返回该顶点的离心率 TIME T，其中 T = ecc(X)
   - 返回距离 X 最远的所有顶点集合 FAR，即所有满足 dist(X,u) = T 的顶点 u

2. **距离查询 DIST A B**（A、B 是顶点标识，A 不等于 B）：
   - 仅当 A 和 B 都至少一次出现在某次 PROBE 的 FAR 集合中时，查询才有效
   - 有效时返回 A 和 B 之间的最短路距离
   - 若不满足条件，返回 REJECT

3. **提交答案 DECLARE D**（D 是非负整数）：
   - 若 D 等于真实直径，游戏成功
   - 否则游戏失败

每次只能进行一个操作。请使用以下 XML 格式：

- 探测操作（例如探测顶点 v1）：
<probe>v1</probe>

- 距离查询（例如查询顶点 v1 和 v2 之间的距离）：
<dist>v1,v2</dist>

- 提交答案（例如声明直径为 5）：
<answer>5</answer>

请尽可能少地使用查询次数来推断出正确的直径。
"""

    game_rule_en = """\
Let's play a "Graph Diameter Inference" game. Here are the rules:

There is an unknown connected, undirected, unweighted graph G=(V,E), where vertex set V has {n} vertices, each with a unique identifier. Edge set E is not visible. All edges have weight 1, and shortest path distances are integers.

Definitions:
- dist(u,v) denotes the shortest path length between vertices u and v
- ecc(v) = max_u dist(v,u) denotes the eccentricity of vertex v (i.e., the maximum distance from v to any other vertex)
- The diameter of the graph D = max_v ecc(v) = max_(u,v) dist(u,v) (i.e., the maximum distance between any two vertices)

Your goal is: Infer the diameter D of the graph through allowed query operations.

You can perform the following three types of operations:

1. **Probe operation PROBE X** (X is a vertex identifier):
   - Returns the eccentricity TIME T, where T = ecc(X)
   - Returns the set FAR of all farthest vertices from X, i.e., all vertices u satisfying dist(X,u) = T

2. **Distance query DIST A B** (A, B are vertex identifiers, A not equal to B):
   - Valid only if both A and B have appeared at least once in some PROBE's FAR set
   - When valid, returns the shortest path distance between A and B
   - If conditions not met, returns REJECT

3. **Submit answer DECLARE D** (D is a non-negative integer):
   - If D equals the true diameter, the game succeeds
   - Otherwise, the game fails

Each turn can perform only one operation. Use the following XML format:

- Probe operation (e.g., probing vertex v1):
<probe>v1</probe>

- Distance query (e.g., querying distance between v1 and v2):
<dist>v1,v2</dist>

- Submit answer (e.g., declaring diameter as 5):
<answer>5</answer>

Please use as few queries as possible to infer the correct diameter.
"""

    contextualized_rule_zh_1 = """\
我们来推断“交通路网的最长通行时间”，规则如下：

存在一个未知的连通、双向通行且无权重的交通路网 G=(V,E)，路口集 V 的规模为 {n} 个路口，每个路口有唯一标识。道路集 E 不可见。所有道路通行时间为 1，最短通行时间为整数。

定义：
- dist(u,v) 表示路口 u 与 v 之间的最短通行时间
- ecc(v) = max_u dist(v,u) 表示路口 v 的极远通行时间（即从 v 出发到达其他任意路口所需的最大时间）
- 路网的最大通行跨度 D = max_v ecc(v) = max_(u,v) dist(u,v)（即路网中任意两个路口之间的最大通行时间）

你的目标是：通过允许的查询操作，推断出路网的最大通行跨度 D。

你可以进行以下三种操作：

1. **探测操作 PROBE X**（X 是路口标识）：
   - 返回该路口的极远通行时间 TIME T，其中 T = ecc(X)
   - 返回距离 X 耗时最远的所有路口集合 FAR，即所有满足 dist(X,u) = T 的路口 u

2. **距离查询 DIST A B**（A、B 是路口标识，A 不等于 B）：
   - 仅当 A 和 B 都至少一次出现在某次 PROBE 的 FAR 集合中时，查询才有效
   - 有效时返回 A 和 B 之间的最短通行时间
   - 若不满足条件，返回 REJECT

3. **提交答案 DECLARE D**（D 是非负整数）：
   - 若 D 等于真实最大通行跨度，系统验证成功
   - 否则验证失败

每次只能进行一个操作。请使用以下 XML 格式：

- 探测操作（例如探测路口 v1）：
<probe>v1</probe>

- 距离查询（例如查询路口 v1 和 v2 之间的通行时间）：
<dist>v1,v2</dist>

- 提交答案（例如声明最大通行时间为 5）：
<answer>5</answer>

请尽可能少地使用查询次数来推断出正确的时间。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's infer the "Maximum Transit Time of a Traffic Network". Here are the rules:

There is an unknown connected, two-way, unweighted traffic network G=(V,E), where intersection set V has {n} intersections, each with a unique identifier. Road set E is not visible. All roads take a transit time of 1, and shortest transit times are integers.

Definitions:
- dist(u,v) denotes the shortest transit time between intersections u and v
- ecc(v) = max_u dist(v,u) denotes the extreme transit time of intersection v (i.e., the maximum time to reach any other intersection from v)
- The maximum transit span of the network D = max_v ecc(v) = max_(u,v) dist(u,v) (i.e., the maximum transit time between any two intersections)

Your goal is: Infer the maximum transit span D of the network through allowed query operations.

You can perform the following three types of operations:

1. **Probe operation PROBE X** (X is an intersection identifier):
   - Returns the extreme transit time TIME T, where T = ecc(X)
   - Returns the set FAR of all farthest intersections from X, i.e., all intersections u satisfying dist(X,u) = T

2. **Distance query DIST A B** (A, B are intersection identifiers, A not equal to B):
   - Valid only if both A and B have appeared at least once in some PROBE's FAR set
   - When valid, returns the shortest transit time between A and B
   - If conditions not met, returns REJECT

3. **Submit answer DECLARE D** (D is a non-negative integer):
   - If D equals the true maximum transit span, the verification succeeds
   - Otherwise, the verification fails

Each turn can perform only one operation. Use the following XML format:

- Probe operation (e.g., probing intersection v1):
<probe>v1</probe>

- Distance query (e.g., querying transit time between v1 and v2):
<dist>v1,v2</dist>

- Submit answer (e.g., declaring maximum transit span as 5):
<answer>5</answer>

Please use as few queries as possible to infer the correct maximum transit span.
"""

    contextualized_rule_zh_2 = """\
我们来推断“病毒传播链的最大隔离层级”，规则如下：

存在一个未知的连通、无向、无权重的接触者网络 G=(V,E)，人员集 V 的规模为 {n} 人，每个人有唯一标识。接触关系集 E 不可见。所有直接接触的层级距离为 1，最短传播层级为整数。

定义：
- dist(u,v) 表示人员 u 与 v 之间的最短传播层级
- ecc(v) = max_u dist(v,u) 表示人员 v 的最远传播风险层级（即从 v 传播到网络中其他人所需的最大层级数）
- 传播网络的最大层级跨度 D = max_v ecc(v) = max_(u,v) dist(u,v)（即网络中任意两人间的最大传播层级数）

你的目标是：通过允许的流调查询操作，推断出该传播网络的最大层级跨度 D。

你可以进行以下三种操作：

1. **探测操作 PROBE X**（X 是人员标识）：
   - 返回该人员的最远传播风险层级 TIME T，其中 T = ecc(X)
   - 返回距离 X 传播层级最远的所有人员集合 FAR，即所有满足 dist(X,u) = T 的人员 u

2. **层级查询 DIST A B**（A、B 是人员标识，A 不等于 B）：
   - 仅当 A 和 B 都至少一次出现在某次 PROBE 的 FAR 集合中时，查询才有效
   - 有效时返回 A 和 B 之间的最短传播层级
   - 若不满足条件，返回 REJECT

3. **提交答案 DECLARE D**（D 是非负整数）：
   - 若 D 等于真实最大传播层级，流调分析成功
   - 否则分析失败

每次只能进行一个操作。请使用以下 XML 格式：

- 探测操作（例如探测人员 v1）：
<probe>v1</probe>

- 层级查询（例如查询人员 v1 和 v2 之间的传播层级）：
<dist>v1,v2</dist>

- 提交答案（例如声明最大层级为 5）：
<answer>5</answer>

请尽可能少地使用查询次数来推断出正确的最大层级。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's infer the "Maximum Isolation Level of a Virus Transmission Chain". Here are the rules:

There is an unknown connected, undirected, unweighted contact network G=(V,E), where the person set V has {n} individuals, each with a unique identifier. The contact relationship set E is not visible. All direct contacts have a level distance of 1, and shortest transmission levels are integers.

Definitions:
- dist(u,v) denotes the shortest transmission level between individuals u and v
- ecc(v) = max_u dist(v,u) denotes the extreme transmission risk level of person v (i.e., the maximum number of levels required for the virus to spread from v to anyone else)
- The maximum transmission span of the network D = max_v ecc(v) = max_(u,v) dist(u,v) (i.e., the maximum transmission levels between any two individuals in the network)

Your goal is: Infer the maximum transmission span D of the network through allowed epidemiological query operations.

You can perform the following three types of operations:

1. **Probe operation PROBE X** (X is a person identifier):
   - Returns the extreme transmission risk level TIME T, where T = ecc(X)
   - Returns the set FAR of all individuals farthest from X in terms of transmission levels, i.e., all individuals u satisfying dist(X,u) = T

2. **Distance query DIST A B** (A, B are person identifiers, A not equal to B):
   - Valid only if both A and B have appeared at least once in some PROBE's FAR set
   - When valid, returns the shortest transmission level between A and B
   - If conditions not met, returns REJECT

3. **Submit answer DECLARE D** (D is a non-negative integer):
   - If D equals the true maximum transmission span, the epidemiological analysis succeeds
   - Otherwise, the analysis fails

Each turn can perform only one operation. Use the following XML format:

- Probe operation (e.g., probing person v1):
<probe>v1</probe>

- Distance query (e.g., querying transmission levels between v1 and v2):
<dist>v1,v2</dist>

- Submit answer (e.g., declaring maximum level as 5):
<answer>5</answer>

Please use as few queries as possible to infer the correct maximum level.
"""

    contextualized_rule_zh_3 = """\
我们来推断“知识图谱的最长前置学习路径”，规则如下：

存在一个未知的连通、无向、无权重的知识概念图谱 G=(V,E)，知识点集 V 的规模为 {n} 个概念，每个概念有唯一标识。概念关联集 E 不可见。所有直接关联的跨度为 1，最短关联路径为整数。

定义：
- dist(u,v) 表示知识点 u 与 v 之间的最短认知路径跨度
- ecc(v) = max_u dist(v,u) 表示知识点 v 的最远认知跨度（即从 v 联想推导到图谱中其他概念所需的最大步数）
- 图谱的最大认知直径 D = max_v ecc(v) = max_(u,v) dist(u,v)（即知识图谱中任意两个概念之间的最大认知跨度）

你的目标是：通过允许的测验查询操作，推断出图谱的最大认知直径 D。

你可以进行以下三种操作：

1. **探测操作 PROBE X**（X 是知识点标识）：
   - 返回该知识点的最远认知跨度 TIME T，其中 T = ecc(X)
   - 返回距离 X 认知路径最远的所有知识点集合 FAR，即所有满足 dist(X,u) = T 的知识点 u

2. **路径查询 DIST A B**（A、B 是知识点标识，A 不等于 B）：
   - 仅当 A 和 B 都至少一次出现在某次 PROBE 的 FAR 集合中时，查询才有效
   - 有效时返回 A 和 B 之间的最短认知跨度
   - 若不满足条件，返回 REJECT

3. **提交答案 DECLARE D**（D 是非负整数）：
   - 若 D 等于真实最大认知跨度，教研分析成功
   - 否则分析失败

每次只能进行一个操作。请使用以下 XML 格式：

- 探测操作（例如探测知识点 v1）：
<probe>v1</probe>

- 路径查询（例如查询知识点 v1 和 v2 之间的认知跨度）：
<dist>v1,v2</dist>

- 提交答案（例如声明最大跨度为 5）：
<answer>5</answer>

请尽可能少地使用查询次数来推断出正确的最大跨度。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's infer the "Longest Prerequisite Learning Path in a Knowledge Graph". Here are the rules:

There is an unknown connected, undirected, unweighted knowledge concept graph G=(V,E), where the concept set V has {n} concepts, each with a unique identifier. The concept relationship set E is not visible. All direct relationships have a span of 1, and shortest cognitive paths are integers.

Definitions:
- dist(u,v) denotes the shortest cognitive path span between concepts u and v
- ecc(v) = max_u dist(v,u) denotes the extreme cognitive span of concept v (i.e., the maximum number of steps required to associate or deduce from v to any other concept)
- The maximum cognitive diameter of the graph D = max_v ecc(v) = max_(u,v) dist(u,v) (i.e., the maximum cognitive span between any two concepts in the graph)

Your goal is: Infer the maximum cognitive diameter D of the graph through allowed quiz query operations.

You can perform the following three types of operations:

1. **Probe operation PROBE X** (X is a concept identifier):
   - Returns the extreme cognitive span TIME T, where T = ecc(X)
   - Returns the set FAR of all concepts farthest from X in terms of cognitive path, i.e., all concepts u satisfying dist(X,u) = T

2. **Distance query DIST A B** (A, B are concept identifiers, A not equal to B):
   - Valid only if both A and B have appeared at least once in some PROBE's FAR set
   - When valid, returns the shortest cognitive span between A and B
   - If conditions not met, returns REJECT

3. **Submit answer DECLARE D** (D is a non-negative integer):
   - If D equals the true maximum cognitive span, the educational research analysis succeeds
   - Otherwise, the analysis fails

Each turn can perform only one operation. Use the following XML format:

- Probe operation (e.g., probing concept v1):
<probe>v1</probe>

- Distance query (e.g., querying cognitive span between v1 and v2):
<dist>v1,v2</dist>

- Submit answer (e.g., declaring maximum span as 5):
<answer>5</answer>

Please use as few queries as possible to infer the correct maximum span.
"""

    contextualized_rule_zh_4 = """\
我们来推断“流水线工序的最大依赖跨度”，规则如下：

存在一个未知的连通、无向、无权重的工序依赖网络 G=(V,E)，工序集 V 的规模为 {n} 道工序，每道工序有唯一标识。工序流转关系集 E 不可见。所有直接流转的环节跨度为 1，最短流转环节为整数。

定义：
- dist(u,v) 表示工序 u 与 v 之间的最短流转环节数
- ecc(v) = max_u dist(v,u) 表示工序 v 的最大流转影响跨度（即从工序 v 传导至网络中其他任意工序所需的最大环节数）
- 生产线的最大依赖跨度 D = max_v ecc(v) = max_(u,v) dist(u,v)（即生产线中任意两道工序之间的最大流转环节数）

你的目标是：通过允许的排查查询操作，推断出生产线的最大依赖跨度 D。

你可以进行以下三种操作：

1. **探测操作 PROBE X**（X 是工序标识）：
   - 返回该工序的最大流转影响跨度 TIME T，其中 T = ecc(X)
   - 返回距离 X 环节跨度最远的所有工序集合 FAR，即所有满足 dist(X,u) = T 的工序 u

2. **环节查询 DIST A B**（A、B 是工序标识，A 不等于 B）：
   - 仅当 A 和 B 都至少一次出现在某次 PROBE 的 FAR 集合中时，查询才有效
   - 有效时返回 A 和 B 之间的最短流转环节数
   - 若不满足条件，返回 REJECT

3. **提交答案 DECLARE D**（D 是非负整数）：
   - 若 D 等于真实最大依赖跨度，工艺链路解析成功
   - 否则解析失败

每次只能进行一个操作。请使用以下 XML 格式：

- 探测操作（例如探测工序 v1）：
<probe>v1</probe>

- 环节查询（例如查询工序 v1 和 v2 之间的流转环节数）：
<dist>v1,v2</dist>

- 提交答案（例如声明最大跨度为 5）：
<answer>5</answer>

请尽可能少地使用查询次数来推断出正确的最大跨度。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's infer the "Maximum Dependency Span of Assembly Line Processes". Here are the rules:

There is an unknown connected, undirected, unweighted process dependency network G=(V,E), where the process set V has {n} processes, each with a unique identifier. The process workflow set E is not visible. All direct workflow steps have a span of 1, and shortest workflow steps are integers.

Definitions:
- dist(u,v) denotes the shortest workflow steps between processes u and v
- ecc(v) = max_u dist(v,u) denotes the extreme workflow impact span of process v (i.e., the maximum number of steps required to propagate from process v to any other process in the network)
- The maximum dependency span of the production line D = max_v ecc(v) = max_(u,v) dist(u,v) (i.e., the maximum workflow steps between any two processes on the line)

Your goal is: Infer the maximum dependency span D of the production line through allowed diagnostic query operations.

You can perform the following three types of operations:

1. **Probe operation PROBE X** (X is a process identifier):
   - Returns the extreme workflow impact span TIME T, where T = ecc(X)
   - Returns the set FAR of all processes farthest from X in terms of workflow steps, i.e., all processes u satisfying dist(X,u) = T

2. **Distance query DIST A B** (A, B are process identifiers, A not equal to B):
   - Valid only if both A and B have appeared at least once in some PROBE's FAR set
   - When valid, returns the shortest workflow steps between A and B
   - If conditions not met, returns REJECT

3. **Submit answer DECLARE D** (D is a non-negative integer):
   - If D equals the true maximum dependency span, the process chain analysis succeeds
   - Otherwise, the analysis fails

Each turn can perform only one operation. Use the following XML format:

- Probe operation (e.g., probing process v1):
<probe>v1</probe>

- Distance query (e.g., querying workflow steps between v1 and v2):
<dist>v1,v2</dist>

- Submit answer (e.g., declaring maximum span as 5):
<answer>5</answer>

Please use as few queries as possible to infer the correct maximum span.
"""

    contextualized_rule_zh_5 = """\
我们来推断“资金洗钱网络的最大追踪链路”，规则如下：

存在一个未知的连通、无向、无权重的洗钱账户网络 G=(V,E)，账户集 V 的规模为 {n} 个账户，每个账户有唯一标识。资金往来关系集 E 不可见。所有直接的资金转账跳数为 1，最短资金追踪跳数为整数。

定义：
- dist(u,v) 表示账户 u 与 v 之间的最短转账跳数
- ecc(v) = max_u dist(v,u) 表示账户 v 的洗钱渗透极值（即从账户 v 转移资金至网络中其他任意账户所需的最大跳数）
- 资金网络的最大隐匿链路 D = max_v ecc(v) = max_(u,v) dist(u,v)（即资金网络中任意两个账户之间的最大转账跳数）

你的目标是：通过允许的司法调查查询操作，推断出资金网络的最大隐匿链路 D。

你可以进行以下三种操作：

1. **探测操作 PROBE X**（X 是账户标识）：
   - 返回该账户的洗钱渗透极值 TIME T，其中 T = ecc(X)
   - 返回距离 X 追踪跳数最远的所有账户集合 FAR，即所有满足 dist(X,u) = T 的账户 u

2. **链路查询 DIST A B**（A、B 是账户标识，A 不等于 B）：
   - 仅当 A 和 B 都至少一次出现在某次 PROBE 的 FAR 集合中时，查询才有效
   - 有效时返回 A 和 B 之间的最短转账跳数
   - 若不满足条件，返回 REJECT

3. **提交答案 DECLARE D**（D 是非负整数）：
   - 若 D 等于真实最大隐匿链路，网络取证分析成功
   - 否则取证失败

每次只能进行一个操作。请使用以下 XML 格式：

- 探测操作（例如探测账户 v1）：
<probe>v1</probe>

- 链路查询（例如查询账户 v1 和 v2 之间的转账跳数）：
<dist>v1,v2</dist>

- 提交答案（例如声明最大链路为 5）：
<answer>5</answer>

请尽可能少地使用查询次数来推断出正确的最大链路。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's infer the "Maximum Tracing Link in a Money Laundering Network". Here are the rules:

There is an unknown connected, undirected, unweighted money laundering account network G=(V,E), where the account set V has {n} accounts, each with a unique identifier. The financial transaction set E is not visible. All direct fund transfers have a hop count of 1, and shortest tracing hops are integers.

Definitions:
- dist(u,v) denotes the shortest transfer hops between accounts u and v
- ecc(v) = max_u dist(v,u) denotes the extreme money laundering penetration of account v (i.e., the maximum number of hops required to transfer funds from account v to any other account in the network)
- The maximum concealment link of the financial network D = max_v ecc(v) = max_(u,v) dist(u,v) (i.e., the maximum transfer hops between any two accounts in the network)

Your goal is: Infer the maximum concealment link D of the network through allowed judicial investigation queries.

You can perform the following three types of operations:

1. **Probe operation PROBE X** (X is an account identifier):
   - Returns the extreme laundering penetration TIME T, where T = ecc(X)
   - Returns the set FAR of all accounts farthest from X in terms of tracing hops, i.e., all accounts u satisfying dist(X,u) = T

2. **Distance query DIST A B** (A, B are account identifiers, A not equal to B):
   - Valid only if both A and B have appeared at least once in some PROBE's FAR set
   - When valid, returns the shortest transfer hops between A and B
   - If conditions not met, returns REJECT

3. **Submit answer DECLARE D** (D is a non-negative integer):
   - If D equals the true maximum concealment link, the network forensics analysis succeeds
   - Otherwise, the forensics fails

Each turn can perform only one operation. Use the following XML format:

- Probe operation (e.g., probing account v1):
<probe>v1</probe>

- Distance query (e.g., querying transfer hops between v1 and v2):
<dist>v1,v2</dist>

- Submit answer (e.g., declaring maximum link as 5):
<answer>5</answer>

Please use as few queries as possible to infer the correct maximum link.
"""

    tags = ["answer", "probe", "dist"]
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        1: {
            "n": 8,
            "edges": [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7)],
        },
        2: {
            "n": 10,
            "edges": [(0,1),(0,2),(0,3),(0,4),(0,5),(5,6),(5,7),(7,8),(7,9)],
        },
        3: {
            "n": 12,
            "edges": [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),
                     (1,6),(6,7),(3,8),(8,9),(5,10),(10,11)],
        },
        4: {
            "n": 15,
            "edges": [(0,1),(1,2),(2,3),(3,4),(4,0),
                     (5,6),(6,7),(7,8),(8,9),(9,5),
                     (2,5),
                     (0,10),(10,11),(7,12),(12,13),(13,14)],
        },
        5: {
            "n": 20,
            "edges": [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0),
                     (6,7),(7,8),(8,6),
                     (9,10),(10,11),(11,9),
                     (1,6),(4,9),
                     (3,12),(12,13),(13,14),(14,15),
                     (8,16),(16,17),
                     (11,18),(18,19)],
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        n = cfg["n"]
        edges = cfg["edges"]

        self._game_info["n"] = n

        self.n = n
        indices = list(range(n))
        random.shuffle(indices)
        self.vertices = [f"v{indices[i]}" for i in range(n)]
        self.adj = {v: [] for v in self.vertices}

        for u_idx, v_idx in edges:
            u = self.vertices[u_idx]
            v = self.vertices[v_idx]
            self.adj[u].append(v)
            self.adj[v].append(u)

        self.dist_matrix = {}
        for v in self.vertices:
            self.dist_matrix[v] = self._bfs(v)

        self.true_diameter = 0
        for v in self.vertices:
            ecc = max(self.dist_matrix[v].values())
            if ecc > self.true_diameter:
                self.true_diameter = ecc

        self.eligible_for_dist = set()

    def _bfs(self, start):
        distances = {start: 0}
        queue = deque([start])
        
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if v not in distances:
                    distances[v] = distances[u] + 1
                    queue.append(v)
        
        return distances

    def _get_eccentricity_and_far(self, vertex):
        distances = self.dist_matrix[vertex]
        ecc = max(distances.values())
        far_set = sorted([v for v, d in distances.items() if d == ecc])
        return ecc, far_set

    def evaluate(self, parsed_info):
        try:
            declared = int(parsed_info["answer"].strip())
            return declared == self.true_diameter
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            reject_msg = "拒绝：该顶点对不符合查询条件"
            invalid_vertex = "错误：无效的顶点标识"
            invalid_format = "错误：格式无效"
        else:
            reject_msg = "REJECT: Pair not eligible"
            invalid_vertex = "Error: Invalid vertex identifier"
            invalid_format = "Error: Invalid format"

        if "probe" in parsed_info:
            vertex = parsed_info["probe"].strip()
            if vertex not in self.vertices:
                return invalid_vertex
            
            ecc, far_set = self._get_eccentricity_and_far(vertex)
            
            for v in far_set:
                self.eligible_for_dist.add(v)
            
            far_str = ", ".join(far_set)
            
            if self.config.language == "zh":
                return f"TIME {ecc}\nFAR {{{far_str}}}"
            else:
                return f"TIME {ecc}\nFAR {{{far_str}}}"

        elif "dist" in parsed_info:
            try:
                raw = parsed_info["dist"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_format
                
                v1, v2 = parts
                if v1 not in self.vertices or v2 not in self.vertices:
                    return invalid_vertex
                if v1 == v2:
                    return invalid_format
                
                if v1 not in self.eligible_for_dist or v2 not in self.eligible_for_dist:
                    return reject_msg
                
                dist = self.dist_matrix[v1][v2]
                
                if self.config.language == "zh":
                    return f"DISTANCE {dist}"
                else:
                    return f"DISTANCE {dist}"
                    
            except (ValueError, KeyError, IndexError):
                return invalid_format

        else:
            raise ValueError("No valid query tag found.")
            
    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        for v in self.vertices:
            query_str = f"<probe>{v}</probe>"
            ecc, far_set = self._get_eccentricity_and_far(v)
            far_str = ", ".join(far_set)
            
            if self.config.language == "zh":
                answer = f"TIME {ecc}\nFAR {{{far_str}}}"
            else:
                answer = f"TIME {ecc}\nFAR {{{far_str}}}"
                
            queries.append({
                "query": query_str,
                "answer": answer
            })
            
        for i in range(len(self.vertices)):
            for j in range(i + 1, len(self.vertices)):
                v1 = self.vertices[i]
                v2 = self.vertices[j]
                
                query_str = f"<dist>{v1},{v2}</dist>"
                dist = self.dist_matrix[v1][v2]
                
                if self.config.language == "zh":
                    answer = f"DISTANCE {dist}"
                else:
                    answer = f"DISTANCE {dist}"
                
                queries.append({
                    "query": query_str,
                    "answer": answer
                })
                
        return queries

    def _cf_make_wrong(self, correct):
        time_match = re.search(r'TIME\s+(\d+)', correct)
        if time_match:
            old_val = int(time_match.group(1))
            new_val = old_val + 1
            return re.sub(r'TIME\s+\d+', f'TIME {new_val}', correct)
            
        dist_match = re.search(r'DISTANCE\s+(\d+)', correct)
        if dist_match:
            old_val = int(dist_match.group(1))
            new_val = old_val + 1
            return re.sub(r'DISTANCE\s+\d+', f'DISTANCE {new_val}', correct)

        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            elif "No" in correct:
                return correct.replace("No", "Yes")
            elif "yes" in correct:
                return correct.replace("yes", "no")
            elif "no" in correct:
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"