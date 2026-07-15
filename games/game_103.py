from .base import Game
import random
import re
import itertools

class GraphIsolatedNodesGame(Game):
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"图孤立节点推理"游戏，规则如下：

游戏设定了一个未知的无向图 G，其中节点集合 V 包含编号 1 到 {n} 的节点，但边集合 E 是未知的。已知图中至少存在一个非孤立节点（度数大于等于1），且至少存在一个度数为 1 的节点。

我提供了 {num_testers} 个测试器（编号为 1 到 {num_testers}）。每个测试器 f 对任意节点 v 的响应由一个未知的布尔函数 P_f(度数) 决定，该函数满足以下性质：
- 对度数为 0 的节点返回负反馈
- 对度数单调不减（度数越高，越可能返回正反馈）
- 至少存在一个测试器对所有度数大于等于 1 的节点都返回正反馈

你的目标是通过查询确定所有孤立节点（度数为 0 的节点）的精确集合。你可以使用以下三种查询方式（每次仅限一个查询）：

1. 探测查询：测试单个节点 v 在测试器 f 下的响应。返回"正反馈"或"负反馈"。
2. 比较查询：比较两个节点 x 和 y 在测试器 f 下的响应。返回"仅x正"、"仅y正"、"两者皆正"或"两者皆负"。
3. 计数查询：统计节点集合 S 中有多少个节点在测试器 f 下返回正反馈。返回一个非负整数。

当你收集足够信息后，请提交你认为的孤立节点集合。若答案正确则游戏成功；若错误，我会告知误报数（你提交的集合中实际非孤立的节点数）和漏报数（实际孤立但你未提交的节点数）。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如用测试器 2 探测节点 5）：
<query_probe>v=5, f=2</query_probe>

- 比较查询（例如用测试器 1 比较节点 3 和 7）：
<query_compare>x=3, y=7, f=1</query_compare>

- 计数查询（例如用测试器 3 统计节点集合 {{1,2,5}}）：
<query_count>S=1,2,5, f=3</query_count>

提交最终答案时，列出所有孤立节点的编号（用逗号隔开，顺序不限）。如果认为没有孤立节点，提交空集：

<answer>isolated=1,3,5</answer>

或

<answer>isolated=</answer>
"""

    game_rule_en = """\
Let's play a "Graph Isolated Nodes Inference" game. Here are the rules:

The game involves an unknown undirected graph G, where the vertex set V contains nodes numbered from 1 to {n}, but the edge set E is unknown. It is known that the graph has at least one non-isolated node (degree greater than or equal to 1), and at least one node with degree 1.

I provide {num_testers} testers (numbered 1 to {num_testers}). Each tester f responds to any node v according to an unknown boolean function P_f(degree), which satisfies:
- Returns negative feedback for nodes with degree 0
- Monotone non-decreasing with respect to degree (higher degree is more likely to return positive feedback)
- At least one tester returns positive feedback for all nodes with degree greater than or equal to 1

Your goal is to determine the exact set of isolated nodes (nodes with degree 0) through queries. You can use the following three query types (one query at a time):

1. Probe Query: Test a single node v using tester f. Returns "positive" or "negative".
2. Compare Query: Compare two nodes x and y using tester f. Returns "only x positive", "only y positive", "both positive", or "both negative".
3. Count Query: Count how many nodes in set S return positive feedback using tester f. Returns a non-negative integer.

When you have enough information, submit the set of isolated nodes you believe. If correct, the game succeeds; if wrong, I will tell you the number of false positives (non-isolated nodes you included) and false negatives (actual isolated nodes you missed).

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., probe node 5 with tester 2):
<query_probe>v=5, f=2</query_probe>

- Compare Query (e.g., compare nodes 3 and 7 with tester 1):
<query_compare>x=3, y=7, f=1</query_compare>

- Count Query (e.g., count nodes {{1,2,5}} with tester 3):
<query_count>S=1,2,5, f=3</query_count>

When submitting the final answer, list all isolated node IDs (comma-separated, order does not matter). If you believe there are no isolated nodes, submit an empty set:

<answer>isolated=1,3,5</answer>

or

<answer>isolated=</answer>
"""

    contextualized_rule_zh_1 = """\
我们来模拟一个"城市交通路网连通性排查"任务，规则如下：

系统设定了一个未知的城市交通路网 G，其中节点集合 V 包含编号 1 到 {n} 的交通路口，但路口之间的直达道路集合 E 是未知的。已知路网中至少存在一个正常连通的路口（至少有一条道路相连），且至少存在一个仅有一条道路相连的末端路口。

指挥中心分配了 {num_testers} 个不同灵敏度的交通流量监测站（编号 1 到 {num_testers}）。每个监测站 f 对任意路口 v 的活动反馈由一个未知的布尔函数 P_f(连通道路数) 决定，该函数满足以下性质：
- 对没有任何连通道路的“废弃孤立路口”始终返回负反馈
- 对道路数单调不减（连通的道路越多，越可能返回正反馈）
- 至少存在一个监测站对所有连通道路数大于等于 1 的路口都返回正反馈

你的目标是通过查询指令，精确找出所有“废弃孤立路口”（连通道路数为 0 的路口）的集合。你可以使用以下三种指令（每次仅限一个）：

1. 探测查询：用监测站 f 探测单个路口 v 的车流活动。返回"正反馈"或"负反馈"。
2. 比较查询：用监测站 f 比较路口 x 和 y 的车流活跃表现。返回"仅x正"、"仅y正"、"两者皆正"或"两者皆负"。
3. 计数查询：用监测站 f 统计路口集合 S 中有多少个路口返回正反馈。返回一个非负整数。

当你收集足够信息后，请提交你认为的废弃孤立路口集合。若答案正确则排查成功；若错误，我会告知误报数（提交中实际非孤立的路口数）和漏报数（实际孤立但未提交的路口数）。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如用监测站 2 探测路口 5）：
<query_probe>v=5, f=2</query_probe>

- 比较查询（例如用监测站 1 比较路口 3 和 7）：
<query_compare>x=3, y=7, f=1</query_compare>

- 计数查询（例如用监测站 3 统计路口集合 {{1,2,5}}）：
<query_count>S=1,2,5, f=3</query_count>

提交最终答案时，列出所有孤立路口的编号（用逗号隔开，顺序不限）。如果认为没有孤立路口，提交空集：

<answer>isolated=1,3,5</answer>

或

<answer>isolated=</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's simulate a "City Traffic Network Connectivity Inspection" task. Here are the rules:

The system involves an unknown city traffic network G, where the junction set V contains traffic junctions numbered from 1 to {n}, but the direct road set E between junctions is unknown. It is known that the network has at least one normally connected junction (with at least one connecting road), and at least one dead-end junction with exactly one connecting road.

The command center provides {num_testers} traffic flow monitoring stations of varying sensitivities (numbered 1 to {num_testers}). Each station f responds to any junction v based on an unknown boolean function P_f(number of connecting roads), which satisfies:
- Returns negative feedback for "abandoned isolated junctions" with no connecting roads
- Monotone non-decreasing with respect to the number of connecting roads (more roads make positive feedback more likely)
- At least one station returns positive feedback for all junctions with 1 or more connecting roads

Your goal is to precisely determine the set of all "abandoned isolated junctions" (junctions with 0 connecting roads) through query commands. You can use the following three types of commands (one query at a time):

1. Probe Query: Detect traffic activity at a single junction v using station f. Returns "positive" or "negative".
2. Compare Query: Compare traffic activity between junctions x and y using station f. Returns "only x positive", "only y positive", "both positive", or "both negative".
3. Count Query: Count how many junctions in set S return positive feedback using station f. Returns a non-negative integer.

When you have gathered enough information, submit the set of abandoned isolated junctions you believe. If correct, the inspection succeeds; if wrong, I will tell you the number of false positives (non-isolated junctions you included) and false negatives (actual isolated junctions you missed).

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., probe junction 5 with station 2):
<query_probe>v=5, f=2</query_probe>

- Compare Query (e.g., compare junctions 3 and 7 with station 1):
<query_compare>x=3, y=7, f=1</query_compare>

- Count Query (e.g., count junction set {{1,2,5}} with station 3):
<query_count>S=1,2,5, f=3</query_count>

When submitting the final answer, list all isolated junction IDs (comma-separated, order does not matter). If you believe there are no isolated junctions, submit an empty set:

<answer>isolated=1,3,5</answer>

or

<answer>isolated=</answer>
"""

    contextualized_rule_zh_2 = """\
我们来进行一项"蛋白互作网络失活排查"任务，规则如下：

系统映射了一个未知的生物体内蛋白互作网络 G，其中节点集合 V 包含编号 1 到 {n} 的蛋白质簇，但蛋白之间的结合链路集合 E 是未知的。已知网络中至少存在一个正常活性的蛋白簇（至少有一条相互作用链路），且至少存在一个仅有一条链路的边缘蛋白簇。

实验室配置了 {num_testers} 种不同浓度的生化试剂（编号 1 到 {num_testers}）。每种试剂 f 对任意蛋白簇 v 的生化反应由一个未知的布尔函数 P_f(结合链路数) 决定，该函数满足以下性质：
- 对没有任何链路的“失活孤立蛋白”始终返回负反馈
- 对链路数单调不减（链路越多，空间结构越稳定，越可能返回正反馈）
- 至少存在一种试剂对所有结合链路数大于等于 1 的蛋白簇都返回正反馈

你的目标是通过实验查询，精确找出所有“失活孤立蛋白”（链路数为 0 的蛋白簇）的集合。你可以使用以下三种实验指令（每次仅限一个）：

1. 探测查询：用试剂 f 测试单个蛋白簇 v 的生化反应。返回"正反馈"或"负反馈"。
2. 比较查询：用试剂 f 比较蛋白簇 x 和 y 的反应强度表现。返回"仅x正"、"仅y正"、"两者皆正"或"两者皆负"。
3. 计数查询：用试剂 f 统计蛋白簇集合 S 中有多少个蛋白呈现正反馈反应。返回一个非负整数。

当你收集足够信息后，请提交你排查出的失活孤立蛋白集合。若答案正确则任务成功；若错误，我会告知误报数（提交中实际具有活性的蛋白数）和漏报数（实际失活但未提交的蛋白数）。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如用试剂 2 探测蛋白簇 5）：
<query_probe>v=5, f=2</query_probe>

- 比较查询（例如用试剂 1 比较蛋白簇 3 和 7）：
<query_compare>x=3, y=7, f=1</query_compare>

- 计数查询（例如用试剂 3 统计蛋白簇集合 {{1,2,5}}）：
<query_count>S=1,2,5, f=3</query_count>

提交最终答案时，列出所有失活蛋白的编号（用逗号隔开，顺序不限）。如果认为没有失活蛋白，提交空集：

<answer>isolated=1,3,5</answer>

或

<answer>isolated=</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's perform a "Protein Interaction Network Inactivation Screening" task. Here are the rules:

The system maps an unknown biological protein interaction network G, where the node set V contains protein clusters numbered from 1 to {n}, but the binding link set E between proteins is unknown. It is known that the network has at least one normally active protein cluster (with at least one interaction link), and at least one marginal cluster with exactly one link.

The laboratory is equipped with {num_testers} biochemical reagents of varying concentrations (numbered 1 to {num_testers}). Each reagent f responds to any protein cluster v based on an unknown boolean function P_f(number of links), which satisfies:
- Returns negative feedback for "inactivated isolated proteins" with no links
- Monotone non-decreasing with respect to the number of links (more links mean higher stability, making positive feedback more likely)
- At least one reagent returns positive feedback for all clusters with 1 or more links

Your goal is to precisely determine the set of all "inactivated isolated proteins" (clusters with 0 links) through experimental queries. You can use the following three types of queries (one query at a time):

1. Probe Query: Test the biochemical reaction of a single cluster v using reagent f. Returns "positive" or "negative".
2. Compare Query: Compare the reaction intensity between clusters x and y using reagent f. Returns "only x positive", "only y positive", "both positive", or "both negative".
3. Count Query: Count how many clusters in set S show positive reactions using reagent f. Returns a non-negative integer.

When you have gathered enough information, submit the set of inactivated isolated proteins. If correct, the screening succeeds; if wrong, I will tell you the number of false positives (active proteins you included) and false negatives (actual inactivated proteins you missed).

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., probe cluster 5 with reagent 2):
<query_probe>v=5, f=2</query_probe>

- Compare Query (e.g., compare clusters 3 and 7 with reagent 1):
<query_compare>x=3, y=7, f=1</query_compare>

- Count Query (e.g., count cluster set {{1,2,5}} with reagent 3):
<query_count>S=1,2,5, f=3</query_count>

When submitting the final answer, list all inactivated protein IDs (comma-separated, order does not matter). If you believe there are no inactivated proteins, submit an empty set:

<answer>isolated=1,3,5</answer>

or

<answer>isolated=</answer>
"""

    contextualized_rule_zh_3 = """\
我们来开展一次"学生知识图谱盲区诊断"任务，规则如下：

系统调取了一名学生的综合知识图谱 G，其中节点集合 V 包含编号 1 到 {n} 的核心知识模块，但模块之间的认知关联集合 E 是未知的。已知图谱中至少存在一个被正常关联的模块（至少能与其他一个模块联系起来），且至少存在一个仅有一个跨模块关联的节点。

教研组提供了 {num_testers} 个不同难度的评估模型（编号 1 到 {num_testers}）。每个模型 f 对任意模块 v 的掌握度反馈由一个未知的布尔函数 P_f(认知关联数) 决定，该函数满足以下性质：
- 对没有任何认知关联的“孤立盲区模块”始终返回负反馈（未达标）
- 对关联数单调不减（能建立联系的知识点越多，越可能返回正反馈）
- 至少存在一个基础评估模型对所有关联数大于等于 1 的模块都返回正反馈

你的目标是通过诊断指令，精确找出所有“孤立盲区模块”（认知关联数为 0 的模块）的集合。你可以使用以下三种指令（每次仅限一个）：

1. 探测查询：用评估模型 f 测试单个模块 v 的掌握情况。返回"正反馈"或"负反馈"。
2. 比较查询：用评估模型 f 比较模块 x 和 y 的掌握表现。返回"仅x正"、"仅y正"、"两者皆正"或"两者皆负"。
3. 计数查询：用评估模型 f 统计模块集合 S 中有多少个模块返回正反馈。返回一个非负整数。

当你收集足够信息后，请提交你诊断出的孤立盲区模块集合。若答案正确则诊断成功；若错误，我会告知误报数（提交中实际有认知关联的模块数）和漏报数（实际是盲区但未提交的模块数）。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如用评估模型 2 测试模块 5）：
<query_probe>v=5, f=2</query_probe>

- 比较查询（例如用评估模型 1 比较模块 3 和 7）：
<query_compare>x=3, y=7, f=1</query_compare>

- 计数查询（例如用评估模型 3 统计模块集合 {{1,2,5}}）：
<query_count>S=1,2,5, f=3</query_count>

提交最终答案时，列出所有盲区模块的编号（用逗号隔开，顺序不限）。如果认为没有盲区模块，提交空集：

<answer>isolated=1,3,5</answer>

或

<answer>isolated=</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Student Knowledge Graph Blind Spot Diagnosis" task. Here are the rules:

The system retrieves a student's comprehensive knowledge graph G, where the node set V contains core knowledge modules numbered from 1 to {n}, but the cognitive association set E between modules is unknown. It is known that the graph has at least one normally associated module (linked to at least one other module), and at least one module with exactly one cross-module association.

The teaching research group provides {num_testers} evaluation models of varying difficulties (numbered 1 to {num_testers}). Each model f responds to any module v based on an unknown boolean function P_f(number of associations), which satisfies:
- Returns negative feedback for "isolated blind spot modules" with no cognitive associations
- Monotone non-decreasing with respect to the number of associations (more linked knowledge makes positive feedback more likely)
- At least one baseline model returns positive feedback for all modules with 1 or more associations

Your goal is to precisely determine the set of all "isolated blind spot modules" (modules with 0 associations) through diagnostic queries. You can use the following three types of queries (one query at a time):

1. Probe Query: Test the mastery of a single module v using model f. Returns "positive" or "negative".
2. Compare Query: Compare the mastery performance between modules x and y using model f. Returns "only x positive", "only y positive", "both positive", or "both negative".
3. Count Query: Count how many modules in set S return positive feedback using model f. Returns a non-negative integer.

When you have gathered enough information, submit the set of blind spot modules you diagnosed. If correct, the diagnosis succeeds; if wrong, I will tell you the number of false positives (associated modules you included) and false negatives (actual blind spots you missed).

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., test module 5 with model 2):
<query_probe>v=5, f=2</query_probe>

- Compare Query (e.g., compare modules 3 and 7 with model 1):
<query_compare>x=3, y=7, f=1</query_compare>

- Count Query (e.g., count module set {{1,2,5}} with model 3):
<query_count>S=1,2,5, f=3</query_count>

When submitting the final answer, list all blind spot module IDs (comma-separated, order does not matter). If you believe there are no blind spot modules, submit an empty set:

<answer>isolated=1,3,5</answer>

or

<answer>isolated=</answer>
"""

    contextualized_rule_zh_4 = """\
我们来执行一项"工厂物联网设备断连排查"任务，规则如下：

系统记录了一个未知的工厂控制网络 G，其中节点集合 V 包含编号 1 到 {n} 的设备节点，但设备之间的通信链路集合 E 是未知的。已知网络中至少存在一台正常连网的设备（至少有一条通信链路），且至少存在一台位于网络末端、仅有一条链路的设备。

运维部门提供了 {num_testers} 个不同频段的网络信号嗅探器（编号 1 到 {num_testers}）。每个嗅探器 f 对任意设备 v 的在线反馈由一个未知的布尔函数 P_f(通信链路数) 决定，该函数满足以下性质：
- 对没有任何通信链路的“断连孤立设备”始终返回负反馈（无法嗅探）
- 对链路数单调不减（连接路径越多，信号越强，越可能返回正反馈）
- 至少存在一个高敏嗅探器对所有链路数大于等于 1 的设备都返回正反馈

你的目标是通过查询指令，精确找出所有“断连孤立设备”（通信链路数为 0 的设备节点）的集合。你可以使用以下三种指令（每次仅限一个）：

1. 探测查询：用嗅探器 f 探测单个设备 v 的在线状态反馈。返回"正反馈"或"负反馈"。
2. 比较查询：用嗅探器 f 比较设备 x 和 y 的信号连通性表现。返回"仅x正"、"仅y正"、"两者皆正"或"两者皆负"。
3. 计数查询：用嗅探器 f 统计设备集合 S 中有多少台设备返回正反馈。返回一个非负整数。

当你收集足够信息后，请提交你排查出的断连孤立设备集合。若答案正确则排查成功；若错误，我会告知误报数（提交中实际在线的设备数）和漏报数（实际已断连但未提交的设备数）。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如用嗅探器 2 探测设备 5）：
<query_probe>v=5, f=2</query_probe>

- 比较查询（例如用嗅探器 1 比较设备 3 和 7）：
<query_compare>x=3, y=7, f=1</query_compare>

- 计数查询（例如用嗅探器 3 统计设备集合 {{1,2,5}}）：
<query_count>S=1,2,5, f=3</query_count>

提交最终答案时，列出所有断连设备的编号（用逗号隔开，顺序不限）。如果认为没有断连设备，提交空集：

<answer>isolated=1,3,5</answer>

或

<answer>isolated=</answer>
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Let's execute a "Factory IoT Device Disconnection Inspection" task. Here are the rules:

The system records an unknown factory control network G, where the node set V contains device nodes numbered from 1 to {n}, but the communication link set E between devices is unknown. It is known that the network has at least one normally online device (with at least one communication link), and at least one end-point device with exactly one link.

The operations department provides {num_testers} network signal sniffers of different frequency bands (numbered 1 to {num_testers}). Each sniffer f responds to any device v based on an unknown boolean function P_f(number of links), which satisfies:
- Returns negative feedback for "disconnected isolated devices" with no communication links
- Monotone non-decreasing with respect to the number of links (more connection paths yield stronger signals, making positive feedback more likely)
- At least one high-sensitivity sniffer returns positive feedback for all devices with 1 or more links

Your goal is to precisely determine the set of all "disconnected isolated devices" (devices with 0 links) through query commands. You can use the following three types of commands (one query at a time):

1. Probe Query: Detect the online status feedback of a single device v using sniffer f. Returns "positive" or "negative".
2. Compare Query: Compare the signal connectivity between devices x and y using sniffer f. Returns "only x positive", "only y positive", "both positive", or "both negative".
3. Count Query: Count how many devices in set S return positive feedback using sniffer f. Returns a non-negative integer.

When you have gathered enough information, submit the set of disconnected isolated devices. If correct, the inspection succeeds; if wrong, I will tell you the number of false positives (online devices you included) and false negatives (actual disconnected devices you missed).

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., probe device 5 with sniffer 2):
<query_probe>v=5, f=2</query_probe>

- Compare Query (e.g., compare devices 3 and 7 with sniffer 1):
<query_compare>x=3, y=7, f=1</query_compare>

- Count Query (e.g., count device set {{1,2,5}} with sniffer 3):
<query_count>S=1,2,5, f=3</query_count>

When submitting the final answer, list all disconnected device IDs (comma-separated, order does not matter). If you believe there are no disconnected devices, submit an empty set:

<answer>isolated=1,3,5</answer>

or

<answer>isolated=</answer>
"""

    contextualized_rule_zh_5 = """\
我们来进行一次"案件证据链效力审查"任务，规则如下：

法庭构建了一个未知的案件证据网络 G，其中节点集合 V 包含编号 1 到 {n} 的证据线索，但证据之间的逻辑印证关系集合 E 是未知的。已知网络中至少存在一份具备关联效力的证据（至少能与另一份证据相互印证），且至少存在一份仅有一条单线印证关系的边缘证据。

司法系统接入了 {num_testers} 套具有不同审查标准的交叉检验程序（编号 1 到 {num_testers}）。每套程序 f 对任意证据 v 的采信反馈由一个未知的布尔函数 P_f(印证关系数) 决定，该函数满足以下性质：
- 对没有任何逻辑印证的“无效孤证”始终返回负反馈（不予采信）
- 对印证数单调不减（能互相印证的节点越多，证据链越完整，越可能返回正反馈）
- 至少存在一套宽口径审查程序对所有印证关系数大于等于 1 的证据都返回正反馈

你的目标是通过审查指令，精确找出所有“无效孤证”（逻辑印证数为 0 的证据）的集合。你可以使用以下三种指令（每次仅限一个）：

1. 探测查询：用审查程序 f 核查单份证据 v 的采信情况。返回"正反馈"或"负反馈"。
2. 比较查询：用审查程序 f 比较证据 x 和 y 的可信度表现。返回"仅x正"、"仅y正"、"两者皆正"或"两者皆负"。
3. 计数查询：用审查程序 f 统计证据集合 S 中有多少份证据被认为具备关联效力并返回正反馈。返回一个非负整数。

当你收集足够信息后，请提交你审查出的无效孤证集合。若答案正确则审查成功；若错误，我会告知误报数（提交中实际有印证效力的证据数）和漏报数（实际是孤证但未提交的证据数）。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 探测查询（例如用审查程序 2 核查证据 5）：
<query_probe>v=5, f=2</query_probe>

- 比较查询（例如用审查程序 1 比较证据 3 和 7）：
<query_compare>x=3, y=7, f=1</query_compare>

- 计数查询（例如用审查程序 3 统计证据集合 {{1,2,5}}）：
<query_count>S=1,2,5, f=3</query_count>

提交最终答案时，列出所有无效孤证的编号（用逗号隔开，顺序不限）。如果认为没有无效孤证，提交空集：

<answer>isolated=1,3,5</answer>

或

<answer>isolated=</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's conduct a "Case Evidence Chain Validity Review" task. Here are the rules:

The court structures an unknown case evidence network G, where the node set V contains evidence clues numbered from 1 to {n}, but the logical corroboration relationship set E between evidence is unknown. It is known that the network has at least one piece of valid associated evidence (corroborating with at least one other piece), and at least one marginal evidence clue with exactly one corroboration.

The judicial system incorporates {num_testers} cross-examination procedures with different review standards (numbered 1 to {num_testers}). Each procedure f responds to any evidence v based on an unknown boolean function P_f(number of corroborations), which satisfies:
- Returns negative feedback for "invalid isolated evidence" with no corroborations (inadmissible)
- Monotone non-decreasing with respect to the number of corroborations (more corroborating nodes make the chain stronger, increasing the likelihood of positive feedback)
- At least one broad-standard procedure returns positive feedback for all evidence with 1 or more corroborations

Your goal is to precisely determine the set of all "invalid isolated evidence" (evidence with 0 corroborations) through review commands. You can use the following three types of commands (one query at a time):

1. Probe Query: Verify the admissibility of a single piece of evidence v using procedure f. Returns "positive" or "negative".
2. Compare Query: Compare the credibility performance between evidence x and y using procedure f. Returns "only x positive", "only y positive", "both positive", or "both negative".
3. Count Query: Count how many pieces of evidence in set S are deemed valid and return positive feedback using procedure f. Returns a non-negative integer.

When you have gathered enough information, submit the set of invalid isolated evidence you identified. If correct, the review succeeds; if wrong, I will tell you the number of false positives (valid evidence you included) and false negatives (actual isolated evidence you missed).

Each query must contain only one tag. Use the following XML format:

- Probe Query (e.g., verify evidence 5 with procedure 2):
<query_probe>v=5, f=2</query_probe>

- Compare Query (e.g., compare evidence 3 and 7 with procedure 1):
<query_compare>x=3, y=7, f=1</query_compare>

- Count Query (e.g., count evidence set {{1,2,5}} with procedure 3):
<query_count>S=1,2,5, f=3</query_count>

When submitting the final answer, list all isolated evidence IDs (comma-separated, order does not matter). If you believe there is no isolated evidence, submit an empty set:

<answer>isolated=1,3,5</answer>

or

<answer>isolated=</answer>
"""

    tags = ["answer", "query_probe", "query_compare", "query_count"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4)],
                "num_testers": 2,
                "tester_thresholds": [1, 2],
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "num_testers": 3,
                "tester_thresholds": [1, 2, 3],
            },
            3: {
                "n": 8,
                "edges": [(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6)],
                "num_testers": 3,
                "tester_thresholds": [1, 2, 3],
            },
            4: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (2, 4), (3, 4), (4, 5), (5, 6), (6, 7)],
                "num_testers": 4,
                "tester_thresholds": [1, 2, 2, 3],
            },
            5: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)],
                "num_testers": 4,
                "tester_thresholds": [1, 2, 3, 3],
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4)],
                "num_testers": 2,
                "tester_thresholds": [1, 2],
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "num_testers": 3,
                "tester_thresholds": [1, 2, 3],
            },
            3: {
                "n": 8,
                "edges": [(1, 2), (1, 3), (2, 3), (3, 4), (4, 5), (5, 6)],
                "num_testers": 3,
                "tester_thresholds": [1, 2, 3],
            },
            4: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (2, 4), (3, 4), (4, 5), (5, 6), (6, 7)],
                "num_testers": 4,
                "tester_thresholds": [1, 2, 2, 3],
            },
            5: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 3), (2, 4), (3, 5), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)],
                "num_testers": 4,
                "tester_thresholds": [1, 2, 3, 3],
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
        self._game_info["n"] = cfg["n"]
        self._game_info["num_testers"] = cfg["num_testers"]
        
        self.n = cfg["n"]
        self.num_testers = cfg["num_testers"]
        self.degrees = {str(i): 0 for i in range(1, self.n + 1)}
        
        for u, v in cfg["edges"]:
            self.degrees[str(u)] += 1
            self.degrees[str(v)] += 1
        
        self.isolated_nodes = {node for node, deg in self.degrees.items() if deg == 0}
        
        self.tester_thresholds = cfg["tester_thresholds"]

    def _tester_response(self, node_id: str, tester_id: int) -> bool:
        if node_id not in self.degrees:
            return False
        
        deg = self.degrees[node_id]
        threshold = self.tester_thresholds[tester_id - 1]
        return deg >= threshold

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        if "isolated=" not in raw_ans:
            return False
        
        isolated_str = raw_ans.split("isolated=", 1)[1].strip()
        
        if isolated_str == "":
            submitted_isolated = set()
        else:
            try:
                submitted_isolated = set(x.strip() for x in isolated_str.split(",") if x.strip())
            except:
                return False
        
        return submitted_isolated == self.isolated_nodes

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            positive, negative = "正反馈", "负反馈"
            only_x, only_y, both_pos, both_neg = "仅x正", "仅y正", "两者皆正", "两者皆负"
            error_msg = "错误：参数格式无效或节点/测试器编号超出范围。"
        else:
            positive, negative = "positive", "negative"
            only_x, only_y, both_pos, both_neg = "only x positive", "only y positive", "both positive", "both negative"
            error_msg = "Error: Invalid parameter format or node/tester ID out of range."

        if "query_probe" in parsed_info:
            try:
                raw = parsed_info["query_probe"]
                params = {}
                for pair in raw.split(","):
                    if not pair.strip():
                        continue
                    k, v = pair.split("=")
                    params[k.strip()] = v.strip()
                
                node_id = params["v"]
                tester_id = int(params["f"])
                
                if node_id not in self.degrees or tester_id < 1 or tester_id > self.num_testers:
                    return error_msg
                
                result = self._tester_response(node_id, tester_id)
                return positive if result else negative
            except:
                return error_msg

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                params = {}
                for pair in raw.split(","):
                    if not pair.strip():
                        continue
                    k, v = pair.split("=")
                    params[k.strip()] = v.strip()
                
                x_id = params["x"]
                y_id = params["y"]
                tester_id = int(params["f"])
                
                if (x_id not in self.degrees or y_id not in self.degrees or 
                    tester_id < 1 or tester_id > self.num_testers):
                    return error_msg
                
                x_result = self._tester_response(x_id, tester_id)
                y_result = self._tester_response(y_id, tester_id)
                
                if x_result and y_result:
                    return both_pos
                elif x_result and not y_result:
                    return only_x
                elif not x_result and y_result:
                    return only_y
                else:
                    return both_neg
            except:
                return error_msg

        elif "query_count" in parsed_info:
            try:
                raw = parsed_info["query_count"]
                
                match = re.search(r'S=(.*?),\s*f=(\d+)', raw, re.IGNORECASE)
                
                if not match:
                    return error_msg

                node_set_str = match.group(1).strip()
                tester_id = int(match.group(2))
                
                if tester_id < 1 or tester_id > self.num_testers:
                    return error_msg
                
                if node_set_str == "":
                    node_set = set()
                else:
                    node_set = set(x.strip() for x in node_set_str.split(",") if x.strip())
                
                for node_id in node_set:
                    if node_id not in self.degrees:
                        return error_msg
                
                count = sum(1 for node_id in node_set if self._tester_response(node_id, tester_id))
                return str(count)
            except:
                return error_msg

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.startswith("Error:") or correct.startswith("错误："):
            return correct

        if correct.isdigit():
            val = int(correct)
            return str(val + 1)
        
        if self.config.language == "zh":
            zh_flip = {
                "正反馈": "负反馈",
                "负反馈": "正反馈",
                "仅x正": "仅y正",
                "仅y正": "仅x正",
                "两者皆正": "两者皆负",
                "两者皆负": "两者皆正",
            }
            if correct in zh_flip:
                return zh_flip[correct]
        else:
            en_flip = {
                "positive": "negative",
                "negative": "positive",
                "only x positive": "only y positive",
                "only y positive": "only x positive",
                "both positive": "both negative",
                "both negative": "both positive",
            }
            if correct in en_flip:
                return en_flip[correct]
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if not hasattr(self, "n") or not hasattr(self, "num_testers"):
            return results

        n = self.n
        nodes = [str(i) for i in range(1, n + 1)]

        for v in nodes:
            content = f"v={v}, f=1"
            parsed_info = {"query_probe": content}
            answer = self._cf_core_produce(parsed_info)
            query_str = f"<query_probe>{content}</query_probe>"
            results.append({"query": query_str, "answer": answer})

        for x, y in itertools.combinations(nodes, 2):
            content = f"x={x}, y={y}, f=1"
            parsed_info = {"query_compare": content}
            answer = self._cf_core_produce(parsed_info)
            query_str = f"<query_compare>{content}</query_compare>"
            results.append({"query": query_str, "answer": answer})

        max_subset_size = min(2, n)
        for r in range(max_subset_size + 1):
            for subset in itertools.combinations(nodes, r):
                subset_str = ",".join(subset)
                content = f"S={subset_str}, f=1"
                parsed_info = {"query_count": content}
                answer = self._cf_core_produce(parsed_info)
                query_str = f"<query_count>{content}</query_count>"
                results.append({"query": query_str, "answer": answer})
        
        subset_str = ",".join(nodes)
        content = f"S={subset_str}, f=1"
        parsed_info = {"query_count": content}
        answer = self._cf_core_produce(parsed_info)
        query_str = f"<query_count>{content}</query_count>"
        results.append({"query": query_str, "answer": answer})

        return results