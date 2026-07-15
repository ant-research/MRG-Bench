from .base import Game
import re

class TreeRootInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"树上根节点推理"游戏，规则如下：

游戏设定了一棵无向树，共10个节点（编号1到10），边连接关系如下：
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

即邻接表为：
- 节点1: 连接2, 3
- 节点2: 连接1, 4, 5
- 节点3: 连接1, 8
- 节点4: 连接2
- 节点5: 连接2, 6, 7
- 节点6: 连接5
- 节点7: 连接5
- 节点8: 连接3, 9, 10
- 节点9: 连接8
- 节点10: 连接8

我已秘密选定了一个根节点R，它只可能是节点4、5、9、10中的一个。你的目标是：
1. 推断出真实的根节点R是哪一个
2. 确定节点2相对于该根的父节点P（P必然是1、4、5中的一个）

在这棵树中，任意两个节点之间的距离定义为连接它们的最短路径上的边数。当根节点确定后，每个非根节点都有唯一的父节点，即与它相邻且距离根更近一步的那个节点。

你可以通过以下查询来收集信息（每次只能提出一个查询）：

**可查询节点集合**：3, 6, 7, 8
**禁止查询节点集合**：1, 2, 4, 5, 9, 10

1. **距离比较查询**：比较两个允许节点与根的距离
   - 格式：<query_compare>a,b</query_compare>
   - 要求：a和b都必须在可查询集合中，且a不等于b
   - 返回：
     - "a" 表示节点a距离根更近
     - "b" 表示节点b距离根更近
     - "equal" 表示两者距离根相等

2. **距离奇偶性查询**：查询某节点与根的距离是奇数还是偶数
   - 格式：<query_parity>x</query_parity>
   - 要求：x必须在可查询集合中
   - 返回：
     - "0" 表示距离为偶数
     - "1" 表示距离为奇数

3. **邻居方向查询**：判断相邻两个节点中哪个更接近根
   - 格式：<query_neighbor>v,u</query_neighbor>
   - 要求：v和u都在可查询集合中，且在树中直接相连
   - 返回：
     - "YES" 表示u比v更接近根
     - "NO" 表示u不比v更接近根

当你认为已收集足够信息时，请提交最终答案：

<answer>root=R, parent_of_2=P</answer>

其中R必须是4、5、9或10；P必须是1、4或5。

**注意**：
- 违反查询约束（如使用禁止节点、查询不相邻的节点等）会导致游戏失败
- 答案错误会导致游戏失败
- 请尽可能少地使用查询次数来推断出正确答案
"""

    game_rule_en = """\
Let's play a "Tree Root Inference" game. Here are the rules:

The game is set on an undirected tree with 10 nodes (numbered 1 to 10), with edges:
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

Adjacency list:
- Node 1: connected to 2, 3
- Node 2: connected to 1, 4, 5
- Node 3: connected to 1, 8
- Node 4: connected to 2
- Node 5: connected to 2, 6, 7
- Node 6: connected to 5
- Node 7: connected to 5
- Node 8: connected to 3, 9, 10
- Node 9: connected to 8
- Node 10: connected to 8

I have secretly selected a root node R, which can only be one of nodes 4, 5, 9, or 10. Your goals are:
1. Infer the true root node R
2. Determine the parent node P of node 2 relative to that root (P must be one of 1, 4, or 5)

In this tree, the distance between any two nodes is defined as the number of edges on the shortest path connecting them. Once the root is determined, each non-root node has a unique parent node, which is the adjacent node that is one step closer to the root.

You can collect information through the following queries (one query per turn):

**Allowed query nodes**: 3, 6, 7, 8
**Forbidden query nodes**: 1, 2, 4, 5, 9, 10

1. **Distance Comparison Query**: Compare distances of two allowed nodes to the root
   - Format: <query_compare>a,b</query_compare>
   - Requirements: Both a and b must be in the allowed set and a not equal to b
   - Returns:
     - "a" means node a is closer to the root
     - "b" means node b is closer to the root
     - "equal" means both are equidistant from the root

2. **Distance Parity Query**: Check if a node's distance to the root is odd or even
   - Format: <query_parity>x</query_parity>
   - Requirements: x must be in the allowed set
   - Returns:
     - "0" means distance is even
     - "1" means distance is odd

3. **Neighbor Direction Query**: Check which of two adjacent nodes is closer to the root
   - Format: <query_neighbor>v,u</query_neighbor>
   - Requirements: Both v and u must be in the allowed set and directly connected in the tree
   - Returns:
     - "YES" means u is closer to the root than v
     - "NO" means u is not closer to the root than v

When you believe you have collected enough information, submit your final answer:

<answer>root=R, parent_of_2=P</answer>

Where R must be 4, 5, 9, or 10; P must be 1, 4, or 5.

**Notes**:
- Violating query constraints (e.g., using forbidden nodes, querying non-adjacent nodes) will cause game failure
- Incorrect answers will cause game failure
- Try to use as few queries as possible to infer the correct answer
"""

    contextualized_rule_zh_1 = """\
我们正在进行一项【城市交通拥堵溯源】分析，规则如下：

系统监控了一个包含10个路口（编号1到10）的城市路网，道路连接关系如下：
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

路口邻接表：
- 路口1: 连接2, 3
- 路口2: 连接1, 4, 5
- 路口3: 连接1, 8
- 路口4: 连接2
- 路口5: 连接2, 6, 7
- 路口6: 连接5
- 路口7: 连接5
- 路口8: 连接3, 9, 10
- 路口9: 连接8
- 路口10: 连接8

现发生了一起严重的连环拥堵，拥堵源头（即根节点R）只可能发生在路口4、5、9、10中的一个。你的目标是：
1. 推断出真正的拥堵源头路口R是哪一个。
2. 确定路口2的拥堵是从哪个上游路口传导过来的（即相对于源头的父节点P，P必然是1、4、5中的一个）。

路网中任意两个路口之间的距离定义为最短路径上的路段数。拥堵源头确定后，每个非源头路口的拥堵都有唯一的上游来源路口，即与其相邻且距离源头更近的那个路口。

由于部分监控损坏，你能调用的监控接口有限（每次只能发起一次接口查询）：

**可用监控路口集合**：3, 6, 7, 8
**损坏无法查询路口集合**：1, 2, 4, 5, 9, 10

1. **溯源距离比较接口**：比较两个可用路口距离拥堵源头的远近
   - 格式：<query_compare>a,b</query_compare>
   - 要求：a和b都必须在可用监控集合中，且a不等于b
   - 返回：
     - "a" 表示路口a距离源头更近
     - "b" 表示路口b距离源头更近
     - "equal" 表示两者距离源头相等

2. **拓扑奇偶性查询接口**：查询某路口与源头之间相隔的路段数量是奇数还是偶数
   - 格式：<query_parity>x</query_parity>
   - 要求：x必须在可用监控集合中
   - 返回：
     - "0" 表示距离路段数为偶数
     - "1" 表示距离路段数为奇数

3. **传导方向验证接口**：判断相邻两个路口中哪个处于更上游（更靠近源头）
   - 格式：<query_neighbor>v,u</query_neighbor>
   - 要求：v和u都在可用监控集合中，且在路网中直接相连
   - 返回：
     - "YES" 表示u比v更靠近源头
     - "NO" 表示u不比v更靠近源头

收集足够证据后，请提交最终分析结论：

<answer>root=R, parent_of_2=P</answer>

其中R必须是4、5、9或10；P必须是1、4或5。违反查询约束或结论错误会导致任务失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are conducting an "Urban Traffic Congestion Tracing" analysis. Here are the rules:

The system monitors an urban road network with 10 intersections (numbered 1 to 10), with road connections:
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

Intersection Adjacency list:
- Intersection 1: connected to 2, 3
- Intersection 2: connected to 1, 4, 5
- Intersection 3: connected to 1, 8
- Intersection 4: connected to 2
- Intersection 5: connected to 2, 6, 7
- Intersection 6: connected to 5
- Intersection 7: connected to 5
- Intersection 8: connected to 3, 9, 10
- Intersection 9: connected to 8
- Intersection 10: connected to 8

A severe cascading congestion has occurred. The epicenter of the congestion (root node R) can only be one of the intersections 4, 5, 9, or 10. Your goals are:
1. Infer the true congestion epicenter R.
2. Determine which upstream intersection transmitted the congestion to intersection 2 (i.e., the parent node P relative to the epicenter, which must be 1, 4, or 5).

The distance between any two intersections is the number of road segments on the shortest path. Once the epicenter is confirmed, every other intersection has a unique upstream source, which is the adjacent intersection one step closer to the epicenter.

Due to damaged traffic cameras, your query capability is limited (one query per turn):

**Monitored accessible intersections**: 3, 6, 7, 8
**Unmonitored inaccessible intersections**: 1, 2, 4, 5, 9, 10

1. **Distance Comparison Query**: Compare distances of two monitored intersections to the epicenter
   - Format: <query_compare>a,b</query_compare>
   - Requirements: Both a and b must be in the accessible set and a not equal to b
   - Returns:
     - "a" means intersection a is closer to the epicenter
     - "b" means intersection b is closer to the epicenter
     - "equal" means both are equidistant

2. **Distance Parity Query**: Check if the number of segments from an intersection to the epicenter is even or odd
   - Format: <query_parity>x</query_parity>
   - Requirements: x must be in the accessible set
   - Returns:
     - "0" means distance is even
     - "1" means distance is odd

3. **Transmission Direction Query**: Check which of two adjacent intersections is further upstream
   - Format: <query_neighbor>v,u</query_neighbor>
   - Requirements: Both v and u must be accessible and directly connected
   - Returns:
     - "YES" means u is closer to the epicenter than v
     - "NO" means u is not closer than v

When you have enough evidence, submit your final conclusion:

<answer>root=R, parent_of_2=P</answer>

Where R must be 4, 5, 9, or 10; P must be 1, 4, or 5. Violating constraints or submitting incorrect conclusions will result in task failure.
"""

    contextualized_rule_zh_2 = """\
我们正在进行一项【流行病学溯源】调查，规则如下：

已知有10名确诊患者（编号1到10），构成了一个无向的接触传播网络，确切的密切接触关系如下：
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

接触关系邻接表：
- 患者1: 密接 2, 3
- 患者2: 密接 1, 4, 5
- 患者3: 密接 1, 8
- 患者4: 密接 2
- 患者5: 密接 2, 6, 7
- 患者6: 密接 5
- 患者7: 密接 5
- 患者8: 密接 3, 9, 10
- 患者9: 密接 8
- 患者10: 密接 8

我们已确认"零号病人"（传播源头R）必定是患者4、5、9、10中的一位。你的目标是：
1. 找出真正的零号病人R是谁。
2. 查明是谁将病毒直接传染给了患者2（即相对于源头的传染父节点P，P必然是1、4、5中的一位）。

在传播网络中，两名患者之间的传播距离定义为最短接触链条上的代数。零号病人确定后，每个非源头患者都有唯一的直接传染源，即与其密接且更早感染（距离零号病人更近一步）的那个人。

由于隐私和配合度原因，你能进行流调问询的对象受限（每次只能发起一次调查）：

**同意接受流调的患者集合**：3, 6, 7, 8
**拒绝/无法流调的患者集合**：1, 2, 4, 5, 9, 10

1. **感染代际比较**：比较两名可用流调患者距离零号病人的传播代数
   - 格式：<query_compare>a,b</query_compare>
   - 要求：a和b都必须在可用流调集合中，且a不等于b
   - 返回：
     - "a" 表示患者a感染更早（距离源头更近）
     - "b" 表示患者b感染更早
     - "equal" 表示两人感染代数相同

2. **传播代数奇偶性查询**：查询某患者到零号病人的传播代数是奇数还是偶数
   - 格式：<query_parity>x</query_parity>
   - 要求：x必须在可用流调集合中
   - 返回：
     - "0" 表示传播代数为偶数
     - "1" 表示传播代数为奇数

3. **传染方向验证**：判断有密接关系的两人中，谁的感染时间更早
   - 格式：<query_neighbor>v,u</query_neighbor>
   - 要求：v和u都在可用流调集合中，且彼此存在确切密接记录
   - 返回：
     - "YES" 表示u比v更早感染
     - "NO" 表示u不比v更早感染

完成溯源后，请提交最终流调报告：

<answer>root=R, parent_of_2=P</answer>

其中R必须是4、5、9或10；P必须是1、4或5。违反调查约束或报告错误将导致任务失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are conducting an "Epidemiological Origin Tracing" investigation. Here are the rules:

There are 10 confirmed patients (numbered 1 to 10) forming an undirected contact transmission network, with exact close contacts as follows:
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

Contact Adjacency list:
- Patient 1: contacts 2, 3
- Patient 2: contacts 1, 4, 5
- Patient 3: contacts 1, 8
- Patient 4: contacts 2
- Patient 5: contacts 2, 6, 7
- Patient 6: contacts 5
- Patient 7: contacts 5
- Patient 8: contacts 3, 9, 10
- Patient 9: contacts 8
- Patient 10: contacts 8

We confirmed that "Patient Zero" (the transmission source R) must be one of patients 4, 5, 9, or 10. Your goals are:
1. Identify the true Patient Zero R.
2. Determine who directly infected patient 2 (i.e., the infectious parent node P relative to the source, which must be 1, 4, or 5).

In this network, the transmission distance between two patients is the number of generations on the shortest contact chain. Once Patient Zero is identified, each other patient has a unique direct infector, which is the close contact who was infected earlier (one step closer to Patient Zero).

Due to privacy and compliance, your epidemiological interview subjects are restricted (one query per turn):

**Consented patients available for query**: 3, 6, 7, 8
**Inaccessible patients**: 1, 2, 4, 5, 9, 10

1. **Infection Generation Comparison**: Compare generation distances of two available patients to Patient Zero
   - Format: <query_compare>a,b</query_compare>
   - Requirements: Both a and b must be in the available set and a not equal to b
   - Returns:
     - "a" means patient a was infected earlier (closer to source)
     - "b" means patient b was infected earlier
     - "equal" means both are at the same generation

2. **Generation Parity Query**: Check if a patient's transmission generations to Patient Zero is even or odd
   - Format: <query_parity>x</query_parity>
   - Requirements: x must be in the available set
   - Returns:
     - "0" means generation distance is even
     - "1" means generation distance is odd

3. **Transmission Direction Query**: Check which of two close contacts was infected earlier
   - Format: <query_neighbor>v,u</query_neighbor>
   - Requirements: Both v and u must be available and have a contact record
   - Returns:
     - "YES" means u was infected earlier than v
     - "NO" means u was not infected earlier than v

When tracing is complete, submit your final epidemiological report:

<answer>root=R, parent_of_2=P</answer>

Where R must be 4, 5, 9, or 10; P must be 1, 4, or 5. Violating constraints or submitting incorrect reports will result in task failure.
"""

    contextualized_rule_zh_3 = """\
我们正在进行一项【核心知识点溯源】的教研分析，规则如下：

课程体系包含10个重要知识点（编号1到10），它们构成了一个无向的认知依赖网络，前置/后续关联关系如下：
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

关联邻接表：
- 概念1: 关联 2, 3
- 概念2: 关联 1, 4, 5
- 概念3: 关联 1, 8
- 概念4: 关联 2
- 概念5: 关联 2, 6, 7
- 概念6: 关联 5
- 概念7: 关联 5
- 概念8: 关联 3, 9, 10
- 概念9: 关联 8
- 概念10: 关联 8

经教研组论证，该学科的"绝对基石概念"（即根节点R）必定是概念4、5、9、10中的一个。你的目标是：
1. 推断出真正的基石概念R是哪一个。
2. 确定在推导概念2时，它的直接前置基础概念P是哪一个（P必然是1、4、5中的一个）。

在这个认知网络中，任意两概念间的认知距离定义为关联路径上的推导步数。基石概念确定后，每个非基石概念都有唯一的直接前置概念，即与其关联且认知距离更接近基石的那个概念。

由于部分概念缺乏标准评估指标，你能调用的测评分析工具受限（每次只能发起一次分析）：

**可测评概念集合**：3, 6, 7, 8
**不可测评概念集合**：1, 2, 4, 5, 9, 10

1. **认知距离比较**：比较两个可测评概念距离基石概念的推导步长
   - 格式：<query_compare>a,b</query_compare>
   - 要求：a和b都必须在可测评集合中，且a不等于b
   - 返回：
     - "a" 表示概念a距离基石更近（更基础）
     - "b" 表示概念b距离基石更近
     - "equal" 表示两者处于相同的基础层级

2. **推导步长奇偶性查询**：查询某概念推导自基石概念的步数是奇数还是偶数
   - 格式：<query_parity>x</query_parity>
   - 要求：x必须在可测评集合中
   - 返回：
     - "0" 表示推导步长为偶数
     - "1" 表示推导步长为奇数

3. **依赖方向验证**：判断两个相互关联的概念中，哪一个更为基础
   - 格式：<query_neighbor>v,u</query_neighbor>
   - 要求：v和u都在可测评集合中，且存在直接关联
   - 返回：
     - "YES" 表示u比v更基础（更接近基石）
     - "NO" 表示u不比v更基础

完成教研分析后，请提交最终结论：

<answer>root=R, parent_of_2=P</answer>

其中R必须是4、5、9或10；P必须是1、4或5。违反测评约束或结论错误将导致任务失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are conducting a "Core Knowledge Tracing" pedagogical analysis. Here are the rules:

The curriculum system contains 10 key concepts (numbered 1 to 10), forming an undirected cognitive dependency network with associative links:
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

Associative Adjacency list:
- Concept 1: linked to 2, 3
- Concept 2: linked to 1, 4, 5
- Concept 3: linked to 1, 8
- Concept 4: linked to 2
- Concept 5: linked to 2, 6, 7
- Concept 6: linked to 5
- Concept 7: linked to 5
- Concept 8: linked to 3, 9, 10
- Concept 9: linked to 8
- Concept 10: linked to 8

The faculty has determined that the "absolute foundational concept" (root node R) must be one of concepts 4, 5, 9, or 10. Your goals are:
1. Infer the true foundational concept R.
2. Determine the direct prerequisite concept P required to derive concept 2 (P must be 1, 4, or 5).

In this cognitive network, the cognitive distance between concepts is the number of derivation steps on the shortest path. Once the foundation is identified, each derived concept has a unique direct prerequisite, which is the linked concept one step closer to the foundation.

Due to a lack of standardized metrics for some concepts, your assessment tools are limited (one query per turn):

**Assessable concept set**: 3, 6, 7, 8
**Unassessable concept set**: 1, 2, 4, 5, 9, 10

1. **Cognitive Distance Comparison**: Compare the derivation lengths of two assessable concepts from the foundation
   - Format: <query_compare>a,b</query_compare>
   - Requirements: Both a and b must be in the assessable set and a not equal to b
   - Returns:
     - "a" means concept a is closer to the foundation
     - "b" means concept b is closer to the foundation
     - "equal" means both are at the same foundational level

2. **Derivation Parity Query**: Check if the number of steps from the foundation to a concept is even or odd
   - Format: <query_parity>x</query_parity>
   - Requirements: x must be in the assessable set
   - Returns:
     - "0" means derivation step count is even
     - "1" means derivation step count is odd

3. **Dependency Direction Query**: Check which of two linked concepts is more foundational
   - Format: <query_neighbor>v,u</query_neighbor>
   - Requirements: Both v and u must be assessable and directly linked
   - Returns:
     - "YES" means u is more foundational than v
     - "NO" means u is not more foundational than v

When the pedagogical analysis is complete, submit your final conclusion:

<answer>root=R, parent_of_2=P</answer>

Where R must be 4, 5, 9, or 10; P must be 1, 4, or 5. Violating constraints or incorrect conclusions will cause task failure.
"""

    contextualized_rule_zh_4 = """\
我们正在进行一项【流水线质量缺陷溯源】诊断，规则如下：

工厂包含10个流水线工位（编号1到10），构成了一个无向的物料流转网络，传送带连接关系如下：
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

工位邻接表：
- 工位1: 连接 2, 3
- 工位2: 连接 1, 4, 5
- 工位3: 连接 1, 8
- 工位4: 连接 2
- 工位5: 连接 2, 6, 7
- 工位6: 连接 5
- 工位7: 连接 5
- 工位8: 连接 3, 9, 10
- 工位9: 连接 8
- 工位10: 连接 8

现查明存在系统级的产品缺陷，缺陷源头工位（即根节点R）只可能是工位4、5、9、10中的一个。你的目标是：
1. 推断出真正的缺陷源头工位R是哪一个。
2. 确定是将残次物料直接输送给工位2的上游工位P是哪一个（P必然是1、4、5中的一个）。

在这条流水线网络中，工位间距离定义为最短流转路径上的传送带段数。源头工位确定后，每个非源头工位都有唯一的上游直接输入站，即与其连接且距离源头更近一步的工位。

由于部分工位的传感器掉线，你能读取的工业互联数据受限（每次只能发起一次读取）：

**传感器在线工位集合**：3, 6, 7, 8
**传感器离线工位集合**：1, 2, 4, 5, 9, 10

1. **流转环节比较指令**：比较两个在线工位距离缺陷源头的环节数
   - 格式：<query_compare>a,b</query_compare>
   - 要求：a和b都必须在在线工位集合中，且a不等于b
   - 返回：
     - "a" 表示工位a距离源头更近（处于更上游）
     - "b" 表示工位b距离源头更近
     - "equal" 表示两者距离源头环节数相等

2. **流转环节奇偶性查询**：查询某工位距离缺陷源头的传送带段数是奇数还是偶数
   - 格式：<query_parity>x</query_parity>
   - 要求：x必须在在线工位集合中
   - 返回：
     - "0" 表示距离段数为偶数
     - "1" 表示距离段数为奇数

3. **上下游方向验证**：判断相邻的两个工位中，谁处于更上游
   - 格式：<query_neighbor>v,u</query_neighbor>
   - 要求：v和u都在在线工位集合中，且存在直接的传送带连接
   - 返回：
     - "YES" 表示u比v更靠近缺陷源头
     - "NO" 表示u不比v更靠近源头

完成诊断后，请提交最终报告：

<answer>root=R, parent_of_2=P</answer>

其中R必须是4、5、9或10；P必须是1、4或5。违反指令约束或诊断错误将导致排查任务失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
We are conducting an "Assembly Line Defect Tracing" diagnosis. Here are the rules:

The factory contains 10 workstations (numbered 1 to 10) forming an undirected material flow network, with conveyor belt connections:
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

Workstation Adjacency list:
- Station 1: connected to 2, 3
- Station 2: connected to 1, 4, 5
- Station 3: connected to 1, 8
- Station 4: connected to 2
- Station 5: connected to 2, 6, 7
- Station 6: connected to 5
- Station 7: connected to 5
- Station 8: connected to 3, 9, 10
- Station 9: connected to 8
- Station 10: connected to 8

A systemic product defect has been detected. The defect origin station (root node R) can only be one of stations 4, 5, 9, or 10. Your goals are:
1. Infer the true defect origin station R.
2. Determine which upstream station fed defective materials directly to station 2 (the parent node P, which must be 1, 4, or 5).

The distance between stations is defined as the number of conveyor segments on the shortest flow path. Once the origin is identified, every other station has a unique direct upstream feeder, which is the connected station one step closer to the origin.

Due to offline sensors, your access to IIoT (Industrial IoT) data is limited (one query per turn):

**Online sensor station set**: 3, 6, 7, 8
**Offline sensor station set**: 1, 2, 4, 5, 9, 10

1. **Flow Stage Comparison**: Compare distances of two online stations to the defect origin
   - Format: <query_compare>a,b</query_compare>
   - Requirements: Both a and b must be in the online set and a not equal to b
   - Returns:
     - "a" means station a is closer to the origin (further upstream)
     - "b" means station b is closer to the origin
     - "equal" means both are at an equal distance

2. **Flow Stage Parity Query**: Check if the number of segments from a station to the origin is even or odd
   - Format: <query_parity>x</query_parity>
   - Requirements: x must be in the online set
   - Returns:
     - "0" means distance is even
     - "1" means distance is odd

3. **Upstream Direction Query**: Check which of two connected stations is further upstream
   - Format: <query_neighbor>v,u</query_neighbor>
   - Requirements: Both v and u must be online and directly connected
   - Returns:
     - "YES" means u is closer to the origin than v
     - "NO" means u is not closer to the origin than v

When the diagnosis is complete, submit your final report:

<answer>root=R, parent_of_2=P</answer>

Where R must be 4, 5, 9, or 10; P must be 1, 4, or 5. Violating constraints or submitting incorrect reports will cause task failure.
"""

    contextualized_rule_zh_5 = """\
我们正在进行一项【金融欺诈证据链重建】分析，规则如下：

案件包含10笔关键资金交易（编号1到10），构成了一个无向的资金流转网络，已核实的转账关联如下：
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

交易关联邻接表：
- 交易1: 关联 2, 3
- 交易2: 关联 1, 4, 5
- 交易3: 关联 1, 8
- 交易4: 关联 2
- 交易5: 关联 2, 6, 7
- 交易6: 关联 5
- 交易7: 关联 5
- 交易8: 关联 3, 9, 10
- 交易9: 关联 8
- 交易10: 关联 8

专案组确认，最初的"欺诈源头交易"（即根节点R）只可能隐藏在交易4、5、9、10之中。你的目标是：
1. 推断出真正的欺诈源头交易R是哪一笔。
2. 确定是哪一笔直接前置交易向交易2输送了资金（即相对于源头的父节点P，P必然是1、4、5中的一个）。

证据链中两笔交易的距离定义为资金流转的最短跳数。源头交易确定后，每笔后续交易都有唯一的直接资金注入方，即与之关联且更接近欺诈源头的那笔交易。

受限于跨国管辖权，你能调阅汇款凭证的交易记录受限（每次只能发起一次调阅）：

**已取得调阅许可的交易集合**：3, 6, 7, 8
**无法调阅的加密交易集合**：1, 2, 4, 5, 9, 10

1. **洗钱层级比较**：比较两笔可调阅交易距离欺诈源头的跳数
   - 格式：<query_compare>a,b</query_compare>
   - 要求：a和b都必须在可调阅集合中，且a不等于b
   - 返回：
     - "a" 表示交易a距离源头更近（层级更高）
     - "b" 表示交易b距离源头更近
     - "equal" 表示两者距离源头跳数相等

2. **流转跳数奇偶性查询**：查询某笔交易距离欺诈源头的流转跳数是奇数还是偶数
   - 格式：<query_parity>x</query_parity>
   - 要求：x必须在可调阅集合中
   - 返回：
     - "0" 表示跳数为偶数
     - "1" 表示跳数为奇数

3. **资金流向验证**：判断两笔存在关联的交易中，哪笔在资金链上更靠前
   - 格式：<query_neighbor>v,u</query_neighbor>
   - 要求：v和u都在可调阅集合中，且存在直接的转账关联
   - 返回：
     - "YES" 表示u比v更靠近欺诈源头
     - "NO" 表示u不比v更靠近源头

完成证据链拼图后，请提交最终结案结论：

<answer>root=R, parent_of_2=P</answer>

其中R必须是4、5、9或10；P必须是1、4或5。违反取证程序或结论错误将导致败诉。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
We are conducting a "Financial Fraud Evidence Chain Reconstruction" analysis. Here are the rules:

The case involves 10 key financial transactions (numbered 1 to 10) forming an undirected fund flow network, with verified transfer links:
(1-2), (1-3), (2-4), (2-5), (5-6), (5-7), (3-8), (8-9), (8-10)

Transaction Adjacency list:
- Transaction 1: linked to 2, 3
- Transaction 2: linked to 1, 4, 5
- Transaction 3: linked to 1, 8
- Transaction 4: linked to 2
- Transaction 5: linked to 2, 6, 7
- Transaction 6: linked to 5
- Transaction 7: linked to 5
- Transaction 8: linked to 3, 9, 10
- Transaction 9: linked to 8
- Transaction 10: linked to 8

The task force confirmed that the initial "fraudulent source transaction" (root node R) must be hidden among transactions 4, 5, 9, or 10. Your goals are:
1. Infer the true fraudulent source transaction R.
2. Determine which direct preceding transaction funneled funds into transaction 2 (the parent node P relative to the source, which must be 1, 4, or 5).

The distance between two transactions in the evidence chain is the number of hops on the shortest fund flow path. Once the source is identified, every subsequent transaction has a unique direct funder, which is the linked transaction one hop closer to the source.

Due to transnational jurisdictions, your subpoena access to remittance records is limited (one query per turn):

**Subpoenaed transactions available for query**: 3, 6, 7, 8
**Encrypted/Inaccessible transactions**: 1, 2, 4, 5, 9, 10

1. **Laundering Layer Comparison**: Compare hop distances of two available transactions to the fraud source
   - Format: <query_compare>a,b</query_compare>
   - Requirements: Both a and b must be in the available set and a not equal to b
   - Returns:
     - "a" means transaction a is closer to the source (higher layer)
     - "b" means transaction b is closer to the source
     - "equal" means both are an equal number of hops away

2. **Flow Hop Parity Query**: Check if the number of hops from a transaction to the fraud source is even or odd
   - Format: <query_parity>x</query_parity>
   - Requirements: x must be in the available set
   - Returns:
     - "0" means hop count is even
     - "1" means hop count is odd

3. **Fund Flow Direction Query**: Check which of two linked transactions is higher up the chain
   - Format: <query_neighbor>v,u</query_neighbor>
   - Requirements: Both v and u must be available and have a verified link
   - Returns:
     - "YES" means u is closer to the fraud source than v
     - "NO" means u is not closer to the source than v

When the evidence chain is reconstructed, submit your final conclusion:

<answer>root=R, parent_of_2=P</answer>

Where R must be 4, 5, 9, or 10; P must be 1, 4, or 5. Violating procedural constraints or submitting incorrect conclusions will result in a lost case.
"""

    tags = ["answer", "query_compare", "query_parity", "query_neighbor"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"root": 4, "parent_of_2": 4},
            2: {"root": 5, "parent_of_2": 5},
            3: {"root": 9, "parent_of_2": 1},
            4: {"root": 10, "parent_of_2": 1},
            5: {"root": 4, "parent_of_2": 4},
        },
        "en": {
            1: {"root": 4, "parent_of_2": 4},
            2: {"root": 5, "parent_of_2": 5},
            3: {"root": 9, "parent_of_2": 1},
            4: {"root": 10, "parent_of_2": 1},
            5: {"root": 4, "parent_of_2": 4},
        },
    }

    reasoning_type = "溯因推理"
    data_structure = "树"

    def __init__(self, config):
        self.adjacency = {
            1: {2, 3},
            2: {1, 4, 5},
            3: {1, 8},
            4: {2},
            5: {2, 6, 7},
            6: {5},
            7: {5},
            8: {3, 9, 10},
            9: {8},
            10: {8},
        }
        self.allowed_nodes = {3, 6, 7, 8}
        self.forbidden_nodes = {1, 2, 4, 5, 9, 10}
        self.root_candidates = {4, 5, 9, 10}
        self.parent_candidates = {1, 4, 5}
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.root = cfg["root"]
        self.correct_parent_of_2 = cfg["parent_of_2"]
        
        self.distances = self._compute_distances(self.root)
        

    def _compute_distances(self, root):
        from collections import deque
        
        distances = {}
        visited = set()
        queue = deque([(root, 0)])
        visited.add(root)
        
        while queue:
            node, dist = queue.popleft()
            distances[node] = dist
            
            for neighbor in self.adjacency[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return distances

    def _validate_query_nodes(self, *nodes):
        for node in nodes:
            try:
                node_int = int(node)
                if node_int not in self.allowed_nodes:
                    return False, f"Invalid query: node {node} is not in the allowed set."
            except ValueError:
                return False, f"Invalid node format: {node}"
        return True, ""

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "root" not in ans_dict or "parent_of_2" not in ans_dict:
                return False
            
            guessed_root = int(ans_dict["root"])
            guessed_parent = int(ans_dict["parent_of_2"])
            
            if guessed_root not in self.root_candidates:
                return False
            if guessed_parent not in self.parent_candidates:
                return False
            
            return guessed_root == self.root and guessed_parent == self.correct_parent_of_2
            
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                nodes = [x.strip() for x in raw.split(",")]
                
                if len(nodes) != 2:
                    raise ValueError("INVALID: expected exactly 2 nodes" if lang == "en" else "无效查询：需要恰好2个节点")
                
                a, b = nodes
                valid, msg = self._validate_query_nodes(a, b)
                if not valid:
                    raise ValueError(msg)
                
                a_int, b_int = int(a), int(b)
                if a_int == b_int:
                    raise ValueError("INVALID: nodes must be different" if lang == "en" else "无效查询：节点必须不同")
                
                dist_a = self.distances[a_int]
                dist_b = self.distances[b_int]
                
                if dist_a < dist_b:
                    return a
                elif dist_b < dist_a:
                    return b
                else:
                    return "equal"
                    
            except (ValueError, KeyError) as e:
                raise ValueError(str(e))
        
        elif "query_parity" in parsed_info:
            try:
                x = parsed_info["query_parity"].strip()
                valid, msg = self._validate_query_nodes(x)
                if not valid:
                    raise ValueError(msg)
                
                x_int = int(x)
                dist = self.distances[x_int]
                return str(dist % 2)
                
            except (ValueError, KeyError) as e:
                raise ValueError(str(e))
        
        elif "query_neighbor" in parsed_info:
            try:
                raw = parsed_info["query_neighbor"].strip()
                nodes = [x.strip() for x in raw.split(",")]
                
                if len(nodes) != 2:
                    raise ValueError("INVALID: expected exactly 2 nodes" if lang == "en" else "无效查询：需要恰好2个节点")
                
                v, u = nodes
                valid, msg = self._validate_query_nodes(v, u)
                if not valid:
                    raise ValueError(msg)
                
                v_int, u_int = int(v), int(u)
                
                if u_int not in self.adjacency[v_int]:
                    raise ValueError("INVALID: nodes are not adjacent" if lang == "en" else "无效查询：节点不相邻")
                
                dist_u = self.distances[u_int]
                dist_v = self.distances[v_int]
                
                if dist_u < dist_v:
                    return "YES"
                else:
                    return "NO"
                    
            except (ValueError, KeyError) as e:
                raise ValueError(str(e))
        
        else:
            raise ValueError("INVALID: unknown query type" if lang == "en" else "无效查询：未知的查询类型")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        sorted_allowed = sorted(list(self.allowed_nodes))
        
        for i, a in enumerate(sorted_allowed):
            for b in sorted_allowed[i+1:]:
                dist_a = self.distances[a]
                dist_b = self.distances[b]
                
                if dist_a < dist_b:
                    ans = str(a)
                elif dist_b < dist_a:
                    ans = str(b)
                else:
                    ans = "equal"
                    
                queries.append({
                    "query": f"<query_compare>{a},{b}</query_compare>",
                    "answer": ans
                })

        for x in sorted_allowed:
            dist = self.distances[x]
            ans = str(dist % 2)
            
            queries.append({
                "query": f"<query_parity>{x}</query_parity>",
                "answer": ans
            })

        for v in sorted_allowed:
            for u in sorted_allowed:
                if u in self.adjacency[v]:
                    dist_v = self.distances[v]
                    dist_u = self.distances[u]
                    
                    if dist_u < dist_v:
                        ans = "YES"
                    else:
                        ans = "NO"
                        
                    queries.append({
                        "query": f"<query_neighbor>{v},{u}</query_neighbor>",
                        "answer": ans
                    })
                    
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        lower_correct = correct.lower().strip()
        
        if correct == "0":
            return "1"
        if correct == "1":
            return "0"
        
        if lower_correct == "equal":
            return str(sorted(self.allowed_nodes)[0])
        
        if "yes" in lower_correct:
            return correct.replace("YES", "NO").replace("Yes", "No").replace("yes", "no")
        if "no" in lower_correct:
            return correct.replace("NO", "YES").replace("No", "Yes").replace("no", "yes")
        
        if correct.isdigit():
            node = int(correct)
            other_nodes = sorted(self.allowed_nodes - {node})
            if other_nodes:
                return str(other_nodes[0])
            return str(node + 1)
        
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        return correct + "_WRONG"