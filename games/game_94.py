from .base import Game
import random

class DiameterTreeTrafficGame(Game):
    reasoning_type = "归纳推理"
    data_structure = "树"

    contextualized_rule_zh_1 = """\
我们在进行一项“交通主干线勘测”任务。系统映射了一个城市的无回路公路网（可视为一棵无向树），节点代表路口或站点，编号从 1 到 N，相邻节点间的距离定义为一个路段。路网中隐藏着两个高度保密的物流枢纽 A 和 B。你的目标是通过有限次的探测，找出该城市公路网中最长的主干线端点（即距离最远的两个节点）及其路段总数（直径长度）。

你可以使用以下几种指令：

1. **路网规模查询**：查询路网中的节点总数 N。不限次数。

2. **枢纽偏离度查询 (ECQ)**：输入一个参考节点 u，系统会对比并返回隐藏枢纽 A、B 中距离 u 更远的那个枢纽 e（距离相等则返回编号较小的枢纽），以及对应的路段数 d(u,e)。
   - 最多可进行 12 次此类查询
   - 提交最终答案前，必须至少完成 5 次 ECQ

3. **节点距离查询 (DQ)**：查询任意两个路口 x 和 y 之间的最短路段数。最多可进行 2 次。

4. **主干线判定 (DCQ)**：判定路口 p 和 q 的距离是否等于全网最长主干线的长度（即路网直径）。系统回答"是"或"否"。不限次数。

5. **路线调取 (PRQ)**：仅在某次 DCQ 返回"是"之后才可使用一次。输入已确认的主干线端点 p,q，系统会返回从 p 到 q 的完整路径节点序列及路段数。最多可进行 1 次。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 路网规模查询：
<query_n></query_n>

- 枢纽偏离度查询（例如查询节点 5）：
<query_ecq>5</query_ecq>

- 节点距离查询（例如查询节点 3 和 7 之间的距离）：
<query_dq>3,7</query_dq>

- 主干线判定（例如判定节点 2 和 8 是否为主干线端点）：
<query_dcq>2,8</query_dcq>

- 路线调取（例如获取节点 2 到 8 的路径）：
<query_prq>2,8</query_prq>

提交最终答案时，必须包含端点和最大路段数（直径）。如果使用了 PRQ，还需包含路径序列。格式如下：

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

或（未使用 PRQ 时）：

<answer>endpoints=2,8, diameter=5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are conducting a "Traffic Arterial Survey" task. The system has mapped a city's loop-free road network (an undirected tree), where nodes represent intersections or stations numbered from 1 to N, and the distance between adjacent nodes is defined as a road segment. Two highly classified logistics hubs, A and B, are hidden within the network. Your goal is to identify the endpoints of the longest arterial route (i.e., the tree's diameter endpoints) and its total segment count (diameter length) through a limited number of probes.

You can use the following query types:

1. **Network Scale Query**: Ask for the total number of nodes N in the network. Unlimited uses.

2. **Hub Deviation Query (ECQ)**: Given a reference node u, the system returns which of the hidden hubs A, B is farther from u (if equal distance, return the one with the smaller ID), along with the corresponding segment count d(u,e).
   - Maximum 12 such queries allowed
   - At least 5 ECQ queries must be completed before submitting the final answer

3. **Node Distance Query (DQ)**: Ask for the shortest segment count between any two intersections x and y. Maximum 2 uses.

4. **Arterial Check Query (DCQ)**: Ask whether the distance between intersections p and q equals the network's longest arterial route (the diameter length). The system answers "Yes" or "No". Unlimited uses.

5. **Route Retrieval Query (PRQ)**: Can only be used once after a DCQ returns "Yes". Input the confirmed arterial endpoints p,q, and the system returns the complete path node sequence from p to q and the segment count. Maximum 1 use.

Each query must contain only one tag. Use the following XML format:

- Network Scale Query:
<query_n></query_n>

- Hub Deviation Query (e.g., query node 5):
<query_ecq>5</query_ecq>

- Node Distance Query (e.g., query distance between nodes 3 and 7):
<query_dq>3,7</query_dq>

- Arterial Check Query (e.g., check if nodes 2 and 8 are arterial endpoints):
<query_dcq>2,8</query_dcq>

- Route Retrieval Query (e.g., get path from node 2 to 8):
<query_prq>2,8</query_prq>

When submitting the final answer, you must include endpoints and the maximum segment count (diameter). If PRQ was used, also include the path sequence. Format:

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

Or (when PRQ was not used):

<answer>endpoints=2,8, diameter=5</answer>
"""

    contextualized_rule_zh_2 = """\
在此“神经网络传导分析”任务中，你需要分析一个特定的神经元树突网络（无向拓扑树），突触节点编号为 1 到 N，节点间距离为信号传导的级数。在该网络中，存在两个尚未准确定位的隐匿性异常病灶节点 A 和 B。你的目标是通过有限的生物电位探测，找出该网络中最长的传导链路两端（即网络直径端点）及链路长度，以评估病理性放电的最大波及范围。

你可以使用以下几种指令：

1. **网络规模查询**：获取网络中突触节点总数 N。不限次数。

2. **病灶偏向性查询 (ECQ)**：刺激节点 u，系统会评估并返回隐匿病灶 A、B 中信号传导距离更远的那个病灶节点 e（距离相等则返回编号较小者），以及距离级数 d(u,e)。
   - 最多可进行 12 次此类查询
   - 提交最终答案前，必须至少完成 5 次 ECQ

3. **传导级数查询 (DQ)**：测定任意节点 x 和 y 之间的传导级数。最多可进行 2 次。

4. **极值链路判定 (DCQ)**：判定节点 p 和 q 之间的传导级数是否等于整个网络的最大传导链路长度（即网络直径）。系统回答"是"或"否"。不限次数。

5. **完整链路追踪 (PRQ)**：仅在某次 DCQ 返回"是"之后才可使用一次。输入已确认的极值链路端点 p,q，系统会返回信号传导的完整突触节点序列及总级数。最多可进行 1 次。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 网络规模查询：
<query_n></query_n>

- 病灶偏向性查询（例如刺激节点 5）：
<query_ecq>5</query_ecq>

- 传导级数查询（例如测定节点 3 和 7 之间的级数）：
<query_dq>3,7</query_dq>

- 极值链路判定（例如判定节点 2 和 8 是否为极值链路端点）：
<query_dcq>2,8</query_dcq>

- 完整链路追踪（例如追踪节点 2 到 8 的链路）：
<query_prq>2,8</query_prq>

提交最终答案时，必须包含端点和最大链路长度（直径）。如果使用了 PRQ，还需包含路径序列。格式如下：

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

或（未使用 PRQ 时）：

<answer>endpoints=2,8, diameter=5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
In this "Neural Network Conduction Analysis" task, you need to analyze a specific neuron dendrite network (an undirected topological tree), with synaptic nodes numbered from 1 to N. The distance between nodes is the number of signal conduction stages. Two hidden, unlocated pathological lesion nodes, A and B, exist in the network. Your objective is to find the two endpoints of the longest conduction pathway (network diameter endpoints) and its length through limited bioelectric probing, in order to assess the maximum spread of pathological discharge.

You can use the following query commands:

1. **Network Scale Query**: Get the total number of synaptic nodes N in the network. Unlimited uses.

2. **Lesion Bias Query (ECQ)**: Stimulate a reference node u; the system assesses and returns the hidden lesion A or B that is farther in conduction distance (if equal, return the smaller ID), and the stage count d(u,e).
   - Maximum 12 such queries allowed
   - At least 5 ECQ queries must be completed before submitting the final answer

3. **Conduction Stage Query (DQ)**: Measure the number of conduction stages between any two nodes x and y. Maximum 2 uses.

4. **Extreme Pathway Check (DCQ)**: Check whether the stages between nodes p and q equal the maximum conduction length of the entire network (the diameter length). The system answers "Yes" or "No". Unlimited uses.

5. **Complete Pathway Trace (PRQ)**: Can only be used once after a DCQ returns "Yes". Input the confirmed extreme pathway endpoints p,q, and the system returns the complete synaptic node sequence and stage count. Maximum 1 use.

Each query must contain only one tag. Use the following XML format:

- Network Scale Query:
<query_n></query_n>

- Lesion Bias Query (e.g., stimulate node 5):
<query_ecq>5</query_ecq>

- Conduction Stage Query (e.g., measure stages between nodes 3 and 7):
<query_dq>3,7</query_dq>

- Extreme Pathway Check (e.g., check if nodes 2 and 8 are extreme endpoints):
<query_dcq>2,8</query_dcq>

- Complete Pathway Trace (e.g., trace pathway from node 2 to 8):
<query_prq>2,8</query_prq>

When submitting the final answer, you must include endpoints and the maximum stage count (diameter). If PRQ was used, also include the path sequence. Format:

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

Or (when PRQ was not used):

<answer>endpoints=2,8, diameter=5</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学科知识图谱跨度评估”系统。该学科的知识点依赖关系构成了一棵无向树，知识模块编号从 1 到 N，相邻模块间的连线表示直接的前置关联。体系中存在两个隐藏的、作为基石的核心考核点 A 和 B。你的教学规划目标是通过最少的检索，找出学科体系中认知跨度最大的两个知识模块（即树直径的两个端点）及其跨度值（直径长度）。

你可以使用以下几种指令：

1. **模块总数查询**：查询体系内的知识模块总数 N。不限次数。

2. **考核点跨度对比 (ECQ)**：给定模块 u，系统将在核心考核点 A、B 中，返回距离 u 关联跨度更大的那个考核点 e（若跨度相同则返回编号较小者），以及对应的跨度 d(u,e)。
   - 最多可进行 12 次此类查询
   - 提交最终答案前，必须至少完成 5 次 ECQ

3. **关联跨度查询 (DQ)**：检索任意模块 x 和 y 之间的关联跨度。最多可进行 2 次。

4. **最大跨度判定 (DCQ)**：判定模块 p 和 q 之间的跨度是否为全体系的最大认知跨度（即树直径）。系统回答"是"或"否"。不限次数。

5. **学习路径生成 (PRQ)**：仅在某次 DCQ 返回"是"之后才可使用一次。输入已确认的最大跨度模块 p,q，系统会生成它们之间的完整过渡模块序列及跨度值。最多可进行 1 次。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 模块总数查询：
<query_n></query_n>

- 考核点跨度对比（例如查询模块 5）：
<query_ecq>5</query_ecq>

- 关联跨度查询（例如检索模块 3 和 7 之间的跨度）：
<query_dq>3,7</query_dq>

- 最大跨度判定（例如判定模块 2 和 8 是否为最大跨度端点）：
<query_dcq>2,8</query_dcq>

- 学习路径生成（例如生成模块 2 到 8 的路径）：
<query_prq>2,8</query_prq>

提交最终答案时，必须包含端点和最大跨度值（直径）。如果使用了 PRQ，还需包含模块序列。格式如下：

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

或（未使用 PRQ 时）：

<answer>endpoints=2,8, diameter=5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Span Assessment" system. The knowledge dependencies form an undirected tree with knowledge modules numbered from 1 to N. The links represent direct prerequisite associations. Two core, hidden cornerstone assessment points, A and B, exist in the system. Your instructional design goal is to find the two knowledge modules with the maximum cognitive span (the tree diameter endpoints) and their span value (diameter length) via minimal retrievals.

You can use the following retrieval commands:

1. **Module Count Query**: Query the total number of knowledge modules N in the system. Unlimited uses.

2. **Assessment Span Comparison (ECQ)**: Given a module u, the system returns the core point A or B with the greater association span from u (if equal, return the smaller ID), and the span d(u,e).
   - Maximum 12 such queries allowed
   - At least 5 ECQ queries must be completed before submitting the final answer

3. **Association Span Query (DQ)**: Retrieve the shortest association span between any two modules x and y. Maximum 2 uses.

4. **Maximum Span Check (DCQ)**: Verify whether the span between modules p and q equals the system's maximum cognitive span (the diameter length). The system answers "Yes" or "No". Unlimited uses.

5. **Learning Path Generation (PRQ)**: Can only be used once after a DCQ returns "Yes". Input the confirmed maximum span modules p,q, and the system generates the transitional module sequence and span value. Maximum 1 use.

Each query must contain only one tag. Use the following XML format:

- Module Count Query:
<query_n></query_n>

- Assessment Span Comparison (e.g., query module 5):
<query_ecq>5</query_ecq>

- Association Span Query (e.g., retrieve span between modules 3 and 7):
<query_dq>3,7</query_dq>

- Maximum Span Check (e.g., verify if modules 2 and 8 are maximum span endpoints):
<query_dcq>2,8</query_dcq>

- Learning Path Generation (e.g., generate path from module 2 to 8):
<query_prq>2,8</query_prq>

When submitting the final answer, you must include endpoints and the maximum span value (diameter). If PRQ was used, also include the path sequence. Format:

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

Or (when PRQ was not used):

<answer>endpoints=2,8, diameter=5</answer>
"""

    contextualized_rule_zh_4 = """\
正在初始化“工业管网极限压损检测”程序。该化工厂的管道系统是一棵无闭环的拓扑树，检测阀门编号从 1 到 N，阀门间的管段数即为距离。管网内部有两个隐藏的高压泵源 A 和 B。工程师的目标是通过有限的传感器调用，找出整个管网中流体输送距离最长的两端（即管网直径端点）及其管段总数（直径长度），以便对最大可能压力损耗进行安全评估。

你可以使用以下几种指令：

1. **节点盘点查询**：获取管网系统内的检测阀门总数 N。不限次数。

2. **泵源远端定位 (ECQ)**：给定检测阀 u，系统在隐藏泵源 A、B 中，返回管段距离更远的那个泵源 e（距离相等则返回编号较小者），以及压损管段数 d(u,e)。
   - 最多可进行 12 次此类查询
   - 提交最终答案前，必须至少完成 5 次 ECQ

3. **管段距离测量 (DQ)**：测量任意阀门 x 和 y 之间的最短管段数。最多可进行 2 次。

4. **极限管径验证 (DCQ)**：验证阀门 p 和 q 之间的距离是否等于管网最长输送距离（即管网直径）。系统回答"是"或"否"。不限次数。

5. **管道拓扑解析 (PRQ)**：仅在某次 DCQ 返回"是"之后才可使用一次。输入已确认的极限端点 p,q，系统会提取它们之间的完整阀门序列与总距离。最多可进行 1 次。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 节点盘点查询：
<query_n></query_n>

- 泵源远端定位（例如定位参考阀门 5）：
<query_ecq>5</query_ecq>

- 管段距离测量（例如测量阀门 3 和 7 之间的管段数）：
<query_dq>3,7</query_dq>

- 极限管径验证（例如验证阀门 2 和 8 是否为极限输送端点）：
<query_dcq>2,8</query_dcq>

- 管道拓扑解析（例如解析阀门 2 到 8 的拓扑）：
<query_prq>2,8</query_prq>

提交最终答案时，必须包含端点和管段总数（直径）。如果使用了 PRQ，还需包含阀门序列。格式如下：

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

或（未使用 PRQ 时）：

<answer>endpoints=2,8, diameter=5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Initializing the "Industrial Pipe Network Pressure Loss Detection" program. The plant's piping is a loop-free topological tree with detection valves numbered from 1 to N. The distance is defined as the pipe segment count. Two critical high-pressure pump sources, A and B, are hidden in the network. Your engineering objective is to find the longest fluid transport ends (the diameter endpoints) and total segment count (diameter length) through limited sensor calls to evaluate the maximum potential pressure loss.

You can use the following sensor protocols:

1. **Node Inventory Query**: Get the total number of valves N in the network. Unlimited uses.

2. **Pump Remote Location (ECQ)**: Given a reference valve u, the system returns the hidden pump A or B that is farther in segment distance (if equal, return the smaller ID), and the segment drop d(u,e).
   - Maximum 12 such queries allowed
   - At least 5 ECQ queries must be completed before submitting the final answer

3. **Segment Measurement Query (DQ)**: Measure the shortest segment count between any two valves x and y. Maximum 2 uses.

4. **Limit Diameter Verification (DCQ)**: Verify whether the distance between valves p and q equals the maximum transport distance of the network (the diameter length). The system answers "Yes" or "No". Unlimited uses.

5. **Topology Parsing (PRQ)**: Can only be used once after a DCQ returns "Yes". Input the confirmed limit endpoints p,q, and the system extracts the full valve sequence and total distance. Maximum 1 use.

Each query must contain only one tag. Use the following XML format:

- Node Inventory Query:
<query_n></query_n>

- Pump Remote Location (e.g., locate relative to valve 5):
<query_ecq>5</query_ecq>

- Segment Measurement Query (e.g., measure segment count between valves 3 and 7):
<query_dq>3,7</query_dq>

- Limit Diameter Verification (e.g., verify if valves 2 and 8 are limit transport ends):
<query_dcq>2,8</query_dcq>

- Topology Parsing (e.g., parse topology from valve 2 to 8):
<query_prq>2,8</query_prq>

When submitting the final answer, you must include endpoints and the maximum segment count (diameter). If PRQ was used, also include the path sequence. Format:

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

Or (when PRQ was not used):

<answer>endpoints=2,8, diameter=5</answer>
"""

    contextualized_rule_zh_5 = """\
你正在执行“商业洗钱网络穿透调查”。目标企业的关联交易网络呈现复杂的无向树状实体结构，各公司/法人节点编号从 1 到 N，节点间距离代表资金流转的层级。调查发现存在两家深度隐藏的幕后空壳公司 A 和 B。为了界定该案件的最高追溯定罪范围，你需要找出整个洗钱网络中最长的资金流转链路的起点和终点（即树的直径端点）及其流转层级数（直径长度）。

你可以使用以下几种手段：

1. **实体规模问询**：查询涉案法人节点总数 N。不限次数。

2. **幕后距离探查 (ECQ)**：锁定基准节点 u，系统将在隐藏空壳公司 A、B 中，反馈资金流转层级更深的那家 e（层级一致取编号小者），以及流转层级数 d(u,e)。
   - 最多可进行 12 次此类查询
   - 提交最终答案前，必须至少完成 5 次 ECQ

3. **流转层级核对 (DQ)**：核对任意节点 x 和 y 之间的最短资金流转层级数。最多可进行 2 次。

4. **极端链路裁定 (DCQ)**：裁定节点 p 和 q 之间的层级数是否构成整个网络中的最长资金流转链路（即网络直径）。系统回答"是"或"否"。不限次数。

5. **资金流水穿透 (PRQ)**：仅在某次 DCQ 返回"是"之后才可使用一次。输入已确认的极端链路端点 p,q，系统将出具完整的资金流转涉案节点序列及层级长度。最多可进行 1 次。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 实体规模问询：
<query_n></query_n>

- 幕后距离探查（例如基准节点 5）：
<query_ecq>5</query_ecq>

- 流转层级核对（例如核对节点 3 和 7 的层级）：
<query_dq>3,7</query_dq>

- 极端链路裁定（例如裁定节点 2 和 8 是否为最长链路端点）：
<query_dcq>2,8</query_dcq>

- 资金流水穿透（例如穿透节点 2 到 8 的流水）：
<query_prq>2,8</query_prq>

提交最终答案时，必须包含端点和最大流转层级数（直径）。如果使用了 PRQ，还需包含节点序列。格式如下：

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

或（未使用 PRQ 时）：

<answer>endpoints=2,8, diameter=5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
You are executing a "Commercial Money Laundering Network Penetration". The target enterprise's transaction network is a complex undirected tree of legal entities, numbered from 1 to N. Distance represents the capital flow tiers. Two deeply hidden shell companies, A and B, have been identified as key behind the scenes. To define the maximum retroactive prosecution scope, you must locate the longest capital flow chain's endpoints (the diameter endpoints) and its tier count (diameter length) via limited investigative means.

You can use the following investigative tools:

1. **Entity Scale Inquiry**: Query the total number of involved entities N. Unlimited uses.

2. **Behind-the-Scenes Probe (ECQ)**: For a base node u, the system returns the hidden shell company A or B with deeper flow tiers (if tied, return the smaller ID), and the tier count d(u,e).
   - Maximum 12 such queries allowed
   - At least 5 ECQ queries must be completed before submitting the final answer

3. **Flow Tier Verification (DQ)**: Verify the shortest capital flow tiers between any two entities x and y. Maximum 2 uses.

4. **Extreme Chain Ruling (DCQ)**: Rule whether the tiers between entities p and q constitute the longest capital flow chain (the diameter length). The system answers "Yes" or "No". Unlimited uses.

5. **Capital Flow Penetration (PRQ)**: Can only be used once after a DCQ ruling is "Yes". Input the confirmed extreme chain endpoints p,q, and the system reveals the full entity sequence and tier length. Maximum 1 use.

Each query must contain only one tag. Use the following XML format:

- Entity Scale Inquiry:
<query_n></query_n>

- Behind-the-Scenes Probe (e.g., probe base node 5):
<query_ecq>5</query_ecq>

- Flow Tier Verification (e.g., verify tiers between entities 3 and 7):
<query_dq>3,7</query_dq>

- Extreme Chain Ruling (e.g., rule if entities 2 and 8 are extreme chain endpoints):
<query_dcq>2,8</query_dcq>

- Capital Flow Penetration (e.g., penetrate flow from entity 2 to 8):
<query_prq>2,8</query_prq>

When submitting the final answer, you must include endpoints and the maximum tier count (diameter). If PRQ was used, also include the path sequence. Format:

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

Or (when PRQ was not used):

<answer>endpoints=2,8, diameter=5</answer>
"""

    game_rule_zh = """\
我们来玩一个"树直径推理"游戏，规则如下：

游戏设定了一棵未知的无向树，节点编号为 1 到 N，节点间的距离定义为最短路径上的边数。树中存在两个固定但隐藏的特殊节点 A 和 B。你的目标是通过有限次数的询问，推断出这棵树的直径端点（即距离最远的两个节点）及其直径长度。

你可以使用以下几种询问方式：

1. **节点总数查询**：询问树的节点总数 N。不限次数。

2. **端点比较查询 (ECQ)**：给定一个节点 u，系统会在隐藏的两个特殊节点 A、B 中，返回与 u 距离更远的那个节点 e（如果距离相等则返回编号较小的节点），以及对应的距离值 d(u,e)。
   - 最多可进行 12 次此类查询
   - 提交最终答案前，必须至少完成 5 次 ECQ

3. **距离查询 (DQ)**：询问任意两个节点 x 和 y 之间的距离。最多可进行 2 次。

4. **直径判定查询 (DCQ)**：询问两个节点 p 和 q 之间的距离是否等于树的直径长度（即树中任意两点间的最大距离）。系统回答"是"或"否"。不限次数。

5. **路径揭示查询 (PRQ)**：仅在某次 DCQ 返回"是"之后才可使用一次。输入已确认为直径端点的节点对 p,q，系统会返回从 p 到 q 的完整路径节点序列及路径长度。最多可进行 1 次。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 节点总数查询：
<query_n></query_n>

- 端点比较查询（例如查询节点 5）：
<query_ecq>5</query_ecq>

- 距离查询（例如查询节点 3 和 7 之间的距离）：
<query_dq>3,7</query_dq>

- 直径判定查询（例如判定节点 2 和 8 是否为直径端点）：
<query_dcq>2,8</query_dcq>

- 路径揭示查询（例如获取节点 2 到 8 的路径）：
<query_prq>2,8</query_prq>

提交最终答案时，必须包含直径端点和直径长度。如果使用了 PRQ，还需包含路径序列。格式如下：

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

或（未使用 PRQ 时）：

<answer>endpoints=2,8, diameter=5</answer>
"""

    game_rule_en = """\
Let's play a "Tree Diameter Deduction" game with the following rules:

The game involves an unknown undirected tree with nodes numbered from 1 to N. The distance between nodes is defined as the number of edges in the shortest path. There are two fixed but hidden special nodes A and B in the tree. Your goal is to deduce the diameter endpoints (the two nodes with the maximum distance) and the diameter length through a limited number of queries.

You can use the following query types:

1. **Node Count Query**: Ask for the total number of nodes N in the tree. Unlimited uses.

2. **Endpoint Comparison Query (ECQ)**: Given a node u, the system returns which of the two hidden special nodes A, B is farther from u (if equal distance, return the one with smaller ID), along with the corresponding distance d(u,e).
   - Maximum 12 such queries allowed
   - At least 5 ECQ queries must be completed before submitting the final answer

3. **Distance Query (DQ)**: Ask for the distance between any two nodes x and y. Maximum 2 uses.

4. **Diameter Check Query (DCQ)**: Ask whether the distance between two nodes p and q equals the tree's diameter length (the maximum distance between any two nodes in the tree). The system answers "Yes" or "No". Unlimited uses.

5. **Path Reveal Query (PRQ)**: Can only be used once after a DCQ returns "Yes". Input the confirmed diameter endpoints p,q, and the system returns the complete path node sequence from p to q and the path length. Maximum 1 use.

Each query must contain only one tag. Use the following XML format:

- Node Count Query:
<query_n></query_n>

- Endpoint Comparison Query (e.g., query node 5):
<query_ecq>5</query_ecq>

- Distance Query (e.g., query distance between nodes 3 and 7):
<query_dq>3,7</query_dq>

- Diameter Check Query (e.g., check if nodes 2 and 8 are diameter endpoints):
<query_dcq>2,8</query_dcq>

- Path Reveal Query (e.g., get path from node 2 to 8):
<query_prq>2,8</query_prq>

When submitting the final answer, you must include diameter endpoints and diameter length. If PRQ was used, also include the path sequence. Format:

<answer>endpoints=2,8, diameter=5, path=2,3,5,7,8</answer>

Or (when PRQ was not used):

<answer>endpoints=2,8, diameter=5</answer>
"""

    tags = ["answer", "query_n", "query_ecq", "query_dq", "query_dcq", "query_prq"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 6, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)], "hidden_a": 1, "hidden_b": 6},
            2: {"n": 8, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (7, 8)], "hidden_a": 5, "hidden_b": 8},
            3: {"n": 10, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (2, 6), (6, 7), (7, 8), (8, 9), (9, 10)], "hidden_a": 5, "hidden_b": 10},
            4: {"n": 12, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7), (7, 8), (8, 9), (2, 10), (10, 11), (11, 12)], "hidden_a": 6, "hidden_b": 12},
            5: {"n": 15, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (3, 8), (8, 9), (9, 10), (2, 11), (11, 12), (12, 13), (13, 14), (14, 15)], "hidden_a": 7, "hidden_b": 15},
        },
        "en": {
            1: {"n": 6, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)], "hidden_a": 1, "hidden_b": 6},
            2: {"n": 8, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (7, 8)], "hidden_a": 5, "hidden_b": 8},
            3: {"n": 10, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (2, 6), (6, 7), (7, 8), (8, 9), (9, 10)], "hidden_a": 5, "hidden_b": 10},
            4: {"n": 12, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 7), (7, 8), (8, 9), (2, 10), (10, 11), (11, 12)], "hidden_a": 6, "hidden_b": 12},
            5: {"n": 15, "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (3, 8), (8, 9), (9, 10), (2, 11), (11, 12), (12, 13), (13, 14), (14, 15)], "hidden_a": 7, "hidden_b": 15},
        },
    }

    def __init__(self, config):
        self.ecq_count = 0
        self.dq_count = 0
        self.prq_count = 0
        self.prq_available = False
        self.confirmed_diameter_pair = None
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        n = cfg["n"]
        edges = cfg["edges"]
        
        self._game_info["n"] = n
        
        self.adj = {i: [] for i in range(1, n + 1)}
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.hidden_a = cfg["hidden_a"]
        self.hidden_b = cfg["hidden_b"]
        
        self._compute_all_distances()
        self._compute_diameter()

    def _compute_all_distances(self):
        self.distances = {}
        n = self._game_info["n"]
        
        for start in range(1, n + 1):
            dist = {start: 0}
            queue = [start]
            head = 0
            
            while head < len(queue):
                u = queue[head]
                head += 1
                
                for v in self.adj[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        queue.append(v)
            
            for end in range(1, n + 1):
                self.distances[(start, end)] = dist[end]

    def _compute_diameter(self):
        n = self._game_info["n"]
        max_dist = 0
        diameter_pairs = []
        
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                d = self.distances[(i, j)]
                if d > max_dist:
                    max_dist = d
                    diameter_pairs = [(i, j)]
                elif d == max_dist:
                    diameter_pairs.append((i, j))
        
        self.diameter_length = max_dist
        self.diameter_pairs = diameter_pairs

    def _get_distance(self, u, v):
        if u > v:
            u, v = v, u
        return self.distances.get((u, v), float('inf'))

    def _get_path(self, start, end):
        if start == end:
            return [start]
        
        parent = {start: None}
        queue = [start]
        head = 0
        
        while head < len(queue):
            u = queue[head]
            head += 1
            
            if u == end:
                path = []
                current = end
                while current is not None:
                    path.append(current)
                    current = parent[current]
                return path[::-1]
            
            for v in self.adj[u]:
                if v not in parent:
                    parent[v] = u
                    queue.append(v)
        
        return []

    def evaluate(self, parsed_info):
        if self.ecq_count < 5:
            return False
        
        raw_ans = parsed_info["answer"]
        parts = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        i = 0
        while i < len(parts):
            part = parts[i]
            if "=" in part:
                k, v = part.split("=", 1)
                k = k.strip()
                v = v.strip()
                
                if k == "path":
                    path_values = [v]
                    i += 1
                    while i < len(parts) and "=" not in parts[i]:
                        path_values.append(parts[i].strip())
                        i += 1
                    ans_dict[k] = ",".join(path_values)
                    continue
                else:
                    ans_dict[k] = v
            i += 1
        
        if "endpoints" not in ans_dict or "diameter" not in ans_dict:
            return False
        
        try:
            ep_str = ans_dict["endpoints"]
            endpoints = tuple(sorted([int(x.strip()) for x in ep_str.split(",")]))
            if len(endpoints) != 2:
                return False
        except:
            return False
        
        normalized_pairs = [tuple(sorted(p)) for p in self.diameter_pairs]
        if endpoints not in normalized_pairs:
            return False
        
        try:
            diameter = int(ans_dict["diameter"])
            if diameter != self.diameter_length:
                return False
        except:
            return False
        
        if "path" in ans_dict:
            try:
                path = [int(x.strip()) for x in ans_dict["path"].split(",")]
                if len(path) - 1 != self.diameter_length:
                    return False
                if sorted([path[0], path[-1]]) != list(endpoints):
                    return False
                for i in range(len(path) - 1):
                    if path[i + 1] not in self.adj[path[i]]:
                        return False
            except:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "query_n" in parsed_info:
            return f"N = {self._game_info['n']}"
        
        elif "query_ecq" in parsed_info:
            if self.ecq_count >= 12:
                return "错误：ECQ 查询次数已达上限（12次）。" if lang == "zh" else "Error: ECQ query limit reached (12 times)."
            
            try:
                u = int(parsed_info["query_ecq"].strip())
                if u < 1 or u > self._game_info["n"]:
                    raise ValueError
            except:
                return "错误：无效的节点编号。" if lang == "zh" else "Error: Invalid node ID."
            
            self.ecq_count += 1
            
            dist_a = self._get_distance(u, self.hidden_a)
            dist_b = self._get_distance(u, self.hidden_b)
            
            if dist_a > dist_b:
                farther_node = self.hidden_a
                distance = dist_a
            elif dist_b > dist_a:
                farther_node = self.hidden_b
                distance = dist_b
            else:
                farther_node = min(self.hidden_a, self.hidden_b)
                distance = dist_a
            
            if lang == "zh":
                return f"节点 {farther_node}，距离 = {distance}"
            else:
                return f"Node {farther_node}, distance = {distance}"
        
        elif "query_dq" in parsed_info:
            if self.dq_count >= 2:
                return "错误：DQ 查询次数已达上限（2次）。" if lang == "zh" else "Error: DQ query limit reached (2 times)."
            
            try:
                raw = parsed_info["query_dq"]
                x, y = [int(v.strip()) for v in raw.split(",")]
                if x < 1 or x > self._game_info["n"] or y < 1 or y > self._game_info["n"]:
                    raise ValueError
            except:
                return "错误：无效的节点编号或格式。" if lang == "zh" else "Error: Invalid node IDs or format."
            
            self.dq_count += 1
            dist = self._get_distance(x, y)
            
            if lang == "zh":
                return f"距离({x}, {y}) = {dist}"
            else:
                return f"distance({x}, {y}) = {dist}"
        
        elif "query_dcq" in parsed_info:
            try:
                raw = parsed_info["query_dcq"]
                p, q = [int(v.strip()) for v in raw.split(",")]
                if p < 1 or p > self._game_info["n"] or q < 1 or q > self._game_info["n"]:
                    raise ValueError
            except:
                return "错误：无效的节点编号或格式。" if lang == "zh" else "Error: Invalid node IDs or format."
            
            dist = self._get_distance(p, q)
            is_diameter = (dist == self.diameter_length)
            
            if is_diameter:
                self.prq_available = True
                self.confirmed_diameter_pair = tuple(sorted([p, q]))
            
            if lang == "zh":
                return "是" if is_diameter else "否"
            else:
                return "Yes" if is_diameter else "No"
        
        elif "query_prq" in parsed_info:
            if self.prq_count >= 1:
                return "错误：PRQ 查询次数已达上限（1次）。" if lang == "zh" else "Error: PRQ query limit reached (1 time)."
            
            if not self.prq_available:
                return "错误：只能在 DCQ 返回是后使用 PRQ。" if lang == "zh" else "Error: PRQ can only be used after a DCQ returns 'Yes'."
            
            try:
                raw = parsed_info["query_prq"]
                p, q = [int(v.strip()) for v in raw.split(",")]
                query_pair = tuple(sorted([p, q]))
                
                if query_pair != self.confirmed_diameter_pair:
                    return "错误：PRQ 只能查询已通过 DCQ 确认的直径端点对。" if lang == "zh" else "Error: PRQ can only query the diameter pair confirmed by DCQ."
            except:
                return "错误：无效的节点编号或格式。" if lang == "zh" else "Error: Invalid node IDs or format."
            
            self.prq_count += 1
            path = self._get_path(p, q)
            path_str = ",".join(map(str, path))
            
            if lang == "zh":
                return f"路径: {path_str}，长度 = {len(path) - 1}"
            else:
                return f"Path: {path_str}, length = {len(path) - 1}"
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        lang = self.config.language
        n = self._game_info["n"]

        q_str_n = "<query_n></query_n>"
        ans_n = f"N = {n}"
        results.append({"query": q_str_n, "answer": ans_n})

        for u in range(1, n + 1):
            q_str = f"<query_ecq>{u}</query_ecq>"
            dist_a = self._get_distance(u, self.hidden_a)
            dist_b = self._get_distance(u, self.hidden_b)
            if dist_a > dist_b:
                farther_node = self.hidden_a
                distance = dist_a
            elif dist_b > dist_a:
                farther_node = self.hidden_b
                distance = dist_b
            else:
                farther_node = min(self.hidden_a, self.hidden_b)
                distance = dist_a
            
            if lang == "zh":
                ans = f"节点 {farther_node}，距离 = {distance}"
            else:
                ans = f"Node {farther_node}, distance = {distance}"
            results.append({"query": q_str, "answer": ans})

        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                q_str = f"<query_dq>{i},{j}</query_dq>"
                dist = self._get_distance(i, j)
                if lang == "zh":
                    ans = f"距离({i}, {j}) = {dist}"
                else:
                    ans = f"distance({i}, {j}) = {dist}"
                results.append({"query": q_str, "answer": ans})

        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                q_str = f"<query_dcq>{i},{j}</query_dcq>"
                dist = self._get_distance(i, j)
                is_diameter = (dist == self.diameter_length)
                if lang == "zh":
                    ans = "是" if is_diameter else "否"
                else:
                    ans = "Yes" if is_diameter else "No"
                results.append({"query": q_str, "answer": ans})

        for (p, q) in self.diameter_pairs:
            q_str = f"<query_prq>{p},{q}</query_prq>"
            path = self._get_path(p, q)
            path_str = ",".join(map(str, path))
            if lang == "zh":
                ans = f"路径: {path_str}，长度 = {len(path) - 1}"
            else:
                ans = f"Path: {path_str}, length = {len(path) - 1}"
            results.append({"query": q_str, "answer": ans})

        return results

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
        if "Yes" in correct:
            return correct.replace("Yes", "No")
        if "No" in correct:
            return correct.replace("No", "Yes")
        return correct + "_WRONG"

