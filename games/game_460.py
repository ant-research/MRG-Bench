from .base import Game
import re

class GraphArticulationGame(Game):
    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图割点推理"游戏，规则如下：

游戏设定了一个无向图 G，顶点集合为 V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}}，边集合为：
- A-B, B-C, C-A（三角形）
- B-X
- D-E, E-J, J-K, K-D（四边形）
- D-X
- F-G, G-L, L-F（三角形）
- F-X
- X-H, H-P, H-Q

除上述边外不存在其他边。

对于任意顶点 v，定义 C(v) 为：从图 G 中删除顶点 v 及其所有邻接边后，得到的图的连通分量数。

系统内部设定了一个固定但未知的映射函数 f，它从以下四种方案中选择其一，且在整个游戏过程中保持不变：
- 方案 A：f(C) = C
- 方案 B：f(C) = C + 1
- 方案 C：f(C) = 1（当 C 等于 1 时），否则 f(C) = 2
- 方案 D：若顶点的度数等于 1，则 f(C) = C + 1，否则 f(C) = C

你的目标是：
1. 通过探测操作识别出真实的映射函数 f
2. 判断目标顶点 {target_node} 是否为割点（即删除该顶点后连通分量数是否大于 1）

1. **探测操作**：探测删除某个顶点后的连通分量信息
   <probe_close>顶点名</probe_close>
   例如：<probe_close>A</probe_close>

2. **确认映射**：提交你认为的映射函数方案
   <confirm_mapping>方案字母</confirm_mapping>
   例如：<confirm_mapping>A</confirm_mapping>
   （方案字母必须是 A、B、C 或 D 之一）

3. **最终判断**：对目标顶点 {target_node} 提交是否为割点的判断
   <final_verdict>Yes</final_verdict> 或 <final_verdict>No</final_verdict>

- 探测操作会返回 "clusters = N" 的形式，其中 N = f(C(顶点))
- 确认映射操作若正确会返回 "Correct"，若错误会返回 "Incorrect" 并导致游戏失败
- 最终判断操作若正确会返回 "Right"，若错误会返回 "Wrong" 并导致游戏失败
- 你需要合理安排操作顺序，用尽可能少的探测次数完成任务

当你完成映射函数识别和割点判断后，使用：
<answer>完成</answer>
来结束游戏（仅在已成功执行确认映射和最终判断后使用）
"""

    game_rule_en = """\
Let's play a "Graph Articulation Point Inference" game. Here are the rules:

The game defines an undirected graph G with vertex set V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}} and edge set:
- A-B, B-C, C-A (triangle)
- B-X
- D-E, E-J, J-K, K-D (quadrilateral)
- D-X
- F-G, G-L, L-F (triangle)
- F-X
- X-H, H-P, H-Q

No other edges exist.

For any vertex v, define C(v) as: the number of connected components in the graph obtained by removing vertex v and all its adjacent edges from graph G.

The system has set a fixed but unknown mapping function f, chosen from one of the following four schemes, which remains constant throughout the game:
- Scheme A: f(C) = C
- Scheme B: f(C) = C + 1
- Scheme C: f(C) = 1 (when C equals 1), otherwise f(C) = 2
- Scheme D: if the vertex degree equals 1, then f(C) = C + 1, otherwise f(C) = C

Your goals are:
1. Identify the true mapping function f through probe operations
2. Determine whether the target vertex {target_node} is an articulation point (i.e., whether the number of connected components is greater than 1 after removing it)

1. **Probe Operation**: Probe the connected component information after removing a vertex
   <probe_close>vertex_name</probe_close>
   Example: <probe_close>A</probe_close>

2. **Confirm Mapping**: Submit your identified mapping function scheme
   <confirm_mapping>scheme_letter</confirm_mapping>
   Example: <confirm_mapping>A</confirm_mapping>
   (scheme_letter must be one of A, B, C, or D)

3. **Final Verdict**: Submit your judgment on whether target vertex {target_node} is an articulation point
   <final_verdict>Yes</final_verdict> or <final_verdict>No</final_verdict>

- Probe operation returns "clusters = N" format, where N = f(C(vertex))
- Confirm mapping returns "Correct" if right, "Incorrect" if wrong (causing game failure)
- Final verdict returns "Right" if correct, "Wrong" if incorrect (causing game failure)
- You need to arrange operations reasonably and complete the task with as few probes as possible

After completing mapping function identification and articulation point judgment, use:
<answer>done</answer>
to end the game (only use after successfully executing confirm mapping and final verdict)
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项“交通路网关键咽喉排查”任务，规则如下：

系统接入了一个城市核心无向交通路网 G，交通枢纽（顶点）集合为 V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}}，道路（边）集合为：
- A-B, B-C, C-A（环形交叉口群）
- B-X
- D-E, E-J, J-K, K-D（四路网格）
- D-X
- F-G, G-L, L-F（环形交叉口群）
- F-X
- X-H, H-P, H-Q

除上述道路外不存在其他连通道路。

对于任意枢纽 v，定义 C(v) 为：从路网 G 中完全封闭（删除）枢纽 v 及其相连的所有道路后，剩余路网被分割成的独立连通区域数量。

系统内部的交通流量监控传感器使用了固定但未知的标定算法 f，它从以下四种方案中选择其一，且在整个排查过程中保持不变：
- 方案 A（精准模式）：f(C) = C
- 方案 B（冗余模式）：f(C) = C + 1
- 方案 C（阈值模式）：f(C) = 1（当 C 等于 1 时），否则 f(C) = 2
- 方案 D（边缘补偿模式）：若该枢纽仅连接 1 条道路（度数为1），则 f(C) = C + 1，否则 f(C) = C

你的目标是：
1. 通过封闭测试操作，识别出传感器当前真实使用的标定算法 f
2. 判断目标枢纽 {target_node} 是否为交通咽喉（即割点：封闭该枢纽后，剩余路网的独立连通区域数量是否大于 1）

1. **探测操作**：测试封闭某个枢纽后系统反馈的连通区域信息
   <probe_close>枢纽名</probe_close>
   例如：<probe_close>A</probe_close>

2. **确认映射**：提交你认为的传感器标定算法方案
   <confirm_mapping>方案字母</confirm_mapping>
   例如：<confirm_mapping>A</confirm_mapping>
   （方案字母必须是 A、B、C 或 D 之一）

3. **最终判断**：对目标枢纽 {target_node} 提交是否为交通咽喉（割点）的研判
   <final_verdict>Yes</final_verdict> 或 <final_verdict>No</final_verdict>

- 探测操作会返回 "clusters = N" 的形式，其中 N = f(C(枢纽))
- 确认映射操作若正确会返回 "Correct"，若错误会返回 "Incorrect" 并导致任务失败
- 最终判断操作若正确会返回 "Right"，若错误会返回 "Wrong" 并导致任务失败
- 你需要合理安排操作顺序，用尽可能少的探测次数完成任务

当你完成算法识别和咽喉枢纽研判后，使用：
<answer>完成</answer>
来结束任务（仅在已成功执行确认映射和最终判断后使用）
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Traffic Network Critical Bottleneck Inspection" task. Here are the rules:

The system has loaded a core urban undirected traffic network G, with the traffic hub (vertex) set V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}} and road (edge) set:
- A-B, B-C, C-A (roundabout cluster)
- B-X
- D-E, E-J, J-K, K-D (four-way grid)
- D-X
- F-G, G-L, L-F (roundabout cluster)
- F-X
- X-H, H-P, H-Q

No other roads exist.

For any hub v, define C(v) as: the number of independent connected areas the remaining network is divided into after completely closing (removing) hub v and all its connected roads.

The system's internal traffic flow monitoring sensors use a fixed but unknown calibration algorithm f, chosen from one of the following four schemes, which remains constant throughout the inspection:
- Scheme A (Precise Mode): f(C) = C
- Scheme B (Redundant Mode): f(C) = C + 1
- Scheme C (Threshold Mode): f(C) = 1 (when C equals 1), otherwise f(C) = 2
- Scheme D (Edge Compensation Mode): if the hub connects only 1 road (degree is 1), then f(C) = C + 1, otherwise f(C) = C

Your goals are:
1. Identify the true calibration algorithm f used by the sensors through closure testing operations
2. Determine whether the target hub {target_node} is a traffic bottleneck (i.e., articulation point: whether the number of independent connected areas is greater than 1 after closing it)

1. **Probe Operation**: Test the connected area information fed back by the system after closing a hub
   <probe_close>hub_name</probe_close>
   Example: <probe_close>A</probe_close>

2. **Confirm Mapping**: Submit your identified sensor calibration algorithm scheme
   <confirm_mapping>scheme_letter</confirm_mapping>
   Example: <confirm_mapping>A</confirm_mapping>
   (scheme_letter must be one of A, B, C, or D)

3. **Final Verdict**: Submit your judgment on whether target hub {target_node} is a traffic bottleneck
   <final_verdict>Yes</final_verdict> or <final_verdict>No</final_verdict>

- Probe operation returns "clusters = N" format, where N = f(C(hub))
- Confirm mapping returns "Correct" if right, "Incorrect" if wrong (causing task failure)
- Final verdict returns "Right" if correct, "Wrong" if incorrect (causing task failure)
- You need to arrange operations reasonably and complete the task with as few probes as possible

After completing algorithm identification and bottleneck hub judgment, use:
<answer>done</answer>
to end the task (only use after successfully executing confirm mapping and final verdict)
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项“流行病传播接触网阻断排查”任务，规则如下：

系统导入了一个无向的人流传播接触网络 G，社区聚集场所（顶点）集合为 V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}}，人员流动路线（边）集合为：
- A-B, B-C, C-A（聚集活动区）
- B-X
- D-E, E-J, J-K, K-D（社区网格）
- D-X
- F-G, G-L, L-F（聚集活动区）
- F-X
- X-H, H-P, H-Q

除上述路线外不存在其他接触途径。

对于任意聚集场所 v，定义 C(v) 为：从网络 G 中彻底隔离（删除）场所 v 及其相连的所有流动路线后，剩余人群被划分成的独立隔离网格数。

系统内部的流调风险评估模型使用了固定但未知的参数映射 f，它从以下四种方案中选择其一，且在整个排查过程中保持不变：
- 方案 A（精准流调）：f(C) = C
- 方案 B（冗余高估）：f(C) = C + 1
- 方案 C（布尔预警）：f(C) = 1（当 C 等于 1 时），否则 f(C) = 2
- 方案 D（边缘人员补正）：若该场所仅连接 1 条流动路线（度数为1），则 f(C) = C + 1，否则 f(C) = C

你的目标是：
1. 通过隔离测试操作，识别出流调模型当前真实使用的映射方案 f
2. 判断目标场所 {target_node} 是否为超级传播枢纽（即割点：隔离该场所后，独立隔离网格数是否大于 1）

1. **探测操作**：测试隔离某个场所后流调系统反馈的隔离网格信息
   <probe_close>场所名</probe_close>
   例如：<probe_close>A</probe_close>

2. **确认映射**：提交你认为的流调评估模型方案
   <confirm_mapping>方案字母</confirm_mapping>
   例如：<confirm_mapping>A</confirm_mapping>
   （方案字母必须是 A、B、C 或 D 之一）

3. **最终判断**：对目标场所 {target_node} 提交是否为超级传播枢纽（割点）的研判
   <final_verdict>Yes</final_verdict> 或 <final_verdict>No</final_verdict>

- 探测操作会返回 "clusters = N" 的形式，其中 N = f(C(场所))
- 确认映射操作若正确会返回 "Correct"，若错误会返回 "Incorrect" 并导致任务失败
- 最终判断操作若正确会返回 "Right"，若错误会返回 "Wrong" 并导致任务失败
- 你需要合理安排操作顺序，用尽可能少的探测次数完成任务

当你完成模型识别和超级传播枢纽研判后，使用：
<answer>完成</answer>
来结束任务（仅在已成功执行确认映射和最终判断后使用）
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct an "Epidemic Contact Network Blockage Inspection" task. Here are the rules:

The system has imported an undirected human movement contact network G, with the community venue (vertex) set V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}} and movement route (edge) set:
- A-B, B-C, C-A (gathering zone)
- B-X
- D-E, E-J, J-K, K-D (community grid)
- D-X
- F-G, G-L, L-F (gathering zone)
- F-X
- X-H, H-P, H-Q

No other contact routes exist.

For any gathering venue v, define C(v) as: the number of independent isolated grids the remaining population is divided into after completely isolating (removing) venue v and all its connected movement routes.

The system's internal epidemiological risk assessment model uses a fixed but unknown parameter mapping f, chosen from one of the following four schemes, which remains constant throughout the inspection:
- Scheme A (Precise Tracing): f(C) = C
- Scheme B (Over-estimation): f(C) = C + 1
- Scheme C (Boolean Alert): f(C) = 1 (when C equals 1), otherwise f(C) = 2
- Scheme D (Edge Adjustment): if the venue connects only 1 movement route (degree is 1), then f(C) = C + 1, otherwise f(C) = C

Your goals are:
1. Identify the true mapping scheme f used by the assessment model through isolation testing operations
2. Determine whether the target venue {target_node} is a super-spreading hub (i.e., articulation point: whether the number of independent isolated grids is greater than 1 after isolating it)

1. **Probe Operation**: Test the isolated grid information fed back by the epidemiological system after isolating a venue
   <probe_close>venue_name</probe_close>
   Example: <probe_close>A</probe_close>

2. **Confirm Mapping**: Submit your identified epidemiological assessment model scheme
   <confirm_mapping>scheme_letter</confirm_mapping>
   Example: <confirm_mapping>A</confirm_mapping>
   (scheme_letter must be one of A, B, C, or D)

3. **Final Verdict**: Submit your judgment on whether target venue {target_node} is a super-spreading hub
   <final_verdict>Yes</final_verdict> or <final_verdict>No</final_verdict>

- Probe operation returns "clusters = N" format, where N = f(C(venue))
- Confirm mapping returns "Correct" if right, "Incorrect" if wrong (causing task failure)
- Final verdict returns "Right" if correct, "Wrong" if incorrect (causing task failure)
- You need to arrange operations reasonably and complete the task with as few probes as possible

After completing model identification and super-spreading hub judgment, use:
<answer>done</answer>
to end the task (only use after successfully executing confirm mapping and final verdict)
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项“核心知识图谱依赖性分析”任务，规则如下：

系统加载了一个学科的核心无向知识依赖网络 G，核心知识模块（顶点）集合为 V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}}，认知关联（边）集合为：
- A-B, B-C, C-A（闭环知识簇）
- B-X
- D-E, E-J, J-K, K-D（结构化知识群）
- D-X
- F-G, G-L, L-F（闭环知识簇）
- F-X
- X-H, H-P, H-Q

除上述关联外不存在其他认知跳跃路径。

对于任意知识模块 v，定义 C(v) 为：从知识网络 G 中移除（假设未掌握）模块 v 及其相连的所有认知关联后，剩余知识体系被分割成的孤立认知区块数量。

学情测评系统内部使用了固定但未知的评分映射函数 f，它从以下四种方案中选择其一，且在整个分析过程中保持不变：
- 方案 A（精准测评）：f(C) = C
- 方案 B（宽容评估）：f(C) = C + 1
- 方案 C（二元诊断）：f(C) = 1（当 C 等于 1 时），否则 f(C) = 2
- 方案 D（边缘惩罚补偿）：若该模块仅有 1 个认知关联（度数为1），则 f(C) = C + 1，否则 f(C) = C

你的目标是：
1. 通过模块遗忘测试，识别出测评系统当前真实使用的评分映射函数 f
2. 判断目标知识模块 {target_node} 是否为核心基础概念（即割点：未掌握该模块后，孤立认知区块数量是否大于 1）

1. **探测操作**：测试移除某个知识模块后测评系统反馈的孤立区块数量
   <probe_close>模块名</probe_close>
   例如：<probe_close>A</probe_close>

2. **确认映射**：提交你认为的测评系统映射方案
   <confirm_mapping>方案字母</confirm_mapping>
   例如：<confirm_mapping>A</confirm_mapping>
   （方案字母必须是 A、B、C 或 D 之一）

3. **最终判断**：对目标模块 {target_node} 提交是否为核心基础概念（割点）的诊断
   <final_verdict>Yes</final_verdict> 或 <final_verdict>No</final_verdict>

- 探测操作会返回 "clusters = N" 的形式，其中 N = f(C(模块))
- 确认映射操作若正确会返回 "Correct"，若错误会返回 "Incorrect" 并导致任务失败
- 最终判断操作若正确会返回 "Right"，若错误会返回 "Wrong" 并导致任务失败
- 你需要合理安排操作顺序，用尽可能少的探测次数完成任务

当你完成映射方案识别和核心概念诊断后，使用：
<answer>完成</answer>
来结束任务（仅在已成功执行确认映射和最终判断后使用）
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Core Knowledge Graph Dependency Analysis" task. Here are the rules:

The system has loaded a subject's core undirected knowledge dependency network G, with the core knowledge module (vertex) set V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}} and cognitive connection (edge) set:
- A-B, B-C, C-A (closed-loop knowledge cluster)
- B-X
- D-E, E-J, J-K, K-D (structured knowledge group)
- D-X
- F-G, G-L, L-F (closed-loop knowledge cluster)
- F-X
- X-H, H-P, H-Q

No other cognitive leap paths exist.

For any knowledge module v, define C(v) as: the number of isolated cognitive blocks the remaining knowledge structure is divided into after removing (assuming unmastered) module v and all its connected cognitive connections.

The learning assessment system internally uses a fixed but unknown scoring mapping function f, chosen from one of the following four schemes, which remains constant throughout the analysis:
- Scheme A (Exact Count): f(C) = C
- Scheme B (Over-evaluation): f(C) = C + 1
- Scheme C (Binary Diagnosis): f(C) = 1 (when C equals 1), otherwise f(C) = 2
- Scheme D (Edge Penalty Compensation): if the module has only 1 cognitive connection (degree is 1), then f(C) = C + 1, otherwise f(C) = C

Your goals are:
1. Identify the true scoring mapping function f used by the assessment system through module omission testing
2. Determine whether the target knowledge module {target_node} is a core fundamental concept (i.e., articulation point: whether the number of isolated cognitive blocks is greater than 1 after leaving it unmastered)

1. **Probe Operation**: Test the isolated block quantity fed back by the assessment system after removing a knowledge module
   <probe_close>module_name</probe_close>
   Example: <probe_close>A</probe_close>

2. **Confirm Mapping**: Submit your identified assessment system mapping scheme
   <confirm_mapping>scheme_letter</confirm_mapping>
   Example: <confirm_mapping>A</confirm_mapping>
   (scheme_letter must be one of A, B, C, or D)

3. **Final Verdict**: Submit your diagnosis on whether target module {target_node} is a core fundamental concept
   <final_verdict>Yes</final_verdict> or <final_verdict>No</final_verdict>

- Probe operation returns "clusters = N" format, where N = f(C(module))
- Confirm mapping returns "Correct" if right, "Incorrect" if wrong (causing task failure)
- Final verdict returns "Right" if correct, "Wrong" if incorrect (causing task failure)
- You need to arrange operations reasonably and complete the task with as few probes as possible

After completing mapping scheme identification and core concept diagnosis, use:
<answer>done</answer>
to end the task (only use after successfully executing confirm mapping and final verdict)
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项“工业微电网关键节点排查”任务，规则如下：

系统监控着一个无向的工业区供电网络 G，变电节点（顶点）集合为 V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}}，输电线（边）集合为：
- A-B, B-C, C-A（环形供电区）
- B-X
- D-E, E-J, J-K, K-D（网格化供电区）
- D-X
- F-G, G-L, L-F（环形供电区）
- F-X
- X-H, H-P, H-Q

除上述输电线外不存在其他输电链路。

对于任意变电节点 v，定义 C(v) 为：从电网 G 中彻底切断（删除）节点 v 及其相连的所有输电线后，剩余电网分化成的独立供电孤岛数量。

微电网的 SCADA 监测系统内部配置了固定但未知的传感器标定策略 f，它从以下四种方案中选择其一，且在整个排查过程中保持不变：
- 方案 A（标准直读）：f(C) = C
- 方案 B（保守冗余）：f(C) = C + 1
- 方案 C（告警阈值）：f(C) = 1（当 C 等于 1 时），否则 f(C) = 2
- 方案 D（末端补偿）：若该变电节点仅连接 1 条输电线（度数为1），则 f(C) = C + 1，否则 f(C) = C

你的目标是：
1. 通过断电测试操作，识别出 SCADA 系统当前真实使用的标定策略 f
2. 判断目标节点 {target_node} 是否为关键输电枢纽（即割点：切断该节点后，独立供电孤岛数量是否大于 1）

1. **探测操作**：测试切断某个节点后 SCADA 系统反馈的孤岛数量信息
   <probe_close>节点名</probe_close>
   例如：<probe_close>A</probe_close>

2. **确认映射**：提交你认为的 SCADA 系统标定策略方案
   <confirm_mapping>方案字母</confirm_mapping>
   例如：<confirm_mapping>A</confirm_mapping>
   （方案字母必须是 A、B、C 或 D 之一）

3. **最终判断**：对目标节点 {target_node} 提交是否为关键输电枢纽（割点）的诊断
   <final_verdict>Yes</final_verdict> 或 <final_verdict>No</final_verdict>

- 探测操作会返回 "clusters = N" 的形式，其中 N = f(C(节点))
- 确认映射操作若正确会返回 "Correct"，若错误会返回 "Incorrect" 并导致任务失败
- 最终判断操作若正确会返回 "Right"，若错误会返回 "Wrong" 并导致任务失败
- 你需要合理安排操作顺序，用尽可能少的探测次数完成任务

当你完成标定策略识别和输电枢纽诊断后，使用：
<answer>完成</answer>
来结束任务（仅在已成功执行确认映射和最终判断后使用）
"""

    contextualized_rule_en_4 = """\
[Industrial Scenario]
Let's conduct an "Industrial Microgrid Critical Node Inspection" task. Here are the rules:

The system monitors an undirected industrial power supply network G, with the substation node (vertex) set V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}} and transmission line (edge) set:
- A-B, B-C, C-A (ring power zone)
- B-X
- D-E, E-J, J-K, K-D (meshed power zone)
- D-X
- F-G, G-L, L-F (ring power zone)
- F-X
- X-H, H-P, H-Q

No other transmission links exist.

For any substation node v, define C(v) as: the number of independent power islands the remaining grid breaks into after completely cutting off (removing) node v and all its connected transmission lines.

The microgrid's SCADA monitoring system is internally configured with a fixed but unknown sensor calibration strategy f, chosen from one of the following four schemes, which remains constant throughout the inspection:
- Scheme A (Standard Reading): f(C) = C
- Scheme B (Conservative Redundancy): f(C) = C + 1
- Scheme C (Alarm Threshold): f(C) = 1 (when C equals 1), otherwise f(C) = 2
- Scheme D (Terminal Node Compensation): if the node connects only 1 transmission line (degree is 1), then f(C) = C + 1, otherwise f(C) = C

Your goals are:
1. Identify the true calibration strategy f used by the SCADA system through power cutoff testing operations
2. Determine whether the target node {target_node} is a critical transmission hub (i.e., articulation point: whether the number of independent power islands is greater than 1 after cutting it off)

1. **Probe Operation**: Test the power island quantity information fed back by the SCADA system after cutting off a node
   <probe_close>node_name</probe_close>
   Example: <probe_close>A</probe_close>

2. **Confirm Mapping**: Submit your identified SCADA system calibration strategy scheme
   <confirm_mapping>scheme_letter</confirm_mapping>
   Example: <confirm_mapping>A</confirm_mapping>
   (scheme_letter must be one of A, B, C, or D)

3. **Final Verdict**: Submit your diagnosis on whether target node {target_node} is a critical transmission hub
   <final_verdict>Yes</final_verdict> or <final_verdict>No</final_verdict>

- Probe operation returns "clusters = N" format, where N = f(C(node))
- Confirm mapping returns "Correct" if right, "Incorrect" if wrong (causing task failure)
- Final verdict returns "Right" if correct, "Wrong" if incorrect (causing task failure)
- You need to arrange operations reasonably and complete the task with as few probes as possible

After completing calibration strategy identification and transmission hub diagnosis, use:
<answer>done</answer>
to end the task (only use after successfully executing confirm mapping and final verdict)
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项“案件证据链关键支撑点分析”任务，规则如下：

法证系统构建了一个无向的案件证据关联网络 G，关键证据（顶点）集合为 V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}}，相互印证关系（边）集合为：
- A-B, B-C, C-A（交叉印证环）
- B-X
- D-E, E-J, J-K, K-D（连环印证网）
- D-X
- F-G, G-L, L-F（交叉印证环）
- F-X
- X-H, H-P, H-Q

除上述关系外不存在其他逻辑关联。

对于任意证据 v，定义 C(v) 为：从证据链 G 中排除（推翻）证据 v 及其所有直接印证关系后，剩余证据网络分裂成的独立逻辑闭环数量。

法证分析系统内部设定了一个固定但未知的系统评估规则 f，它从以下四种方案中选择其一，且在整个分析过程中保持不变：
- 方案 A（严谨提取）：f(C) = C
- 方案 B（宽容计数）：f(C) = C + 1
- 方案 C（二元指示）：f(C) = 1（当 C 等于 1 时），否则 f(C) = 2
- 方案 D（边缘证据补偿）：若该证据仅有 1 处印证关系（度数为1），则 f(C) = C + 1，否则 f(C) = C

你的目标是：
1. 通过证据排除测试，识别出系统真实使用的评估规则 f
2. 判断目标证据 {target_node} 是否为核心定罪证据（即割点：排除该证据后，独立逻辑闭环数量是否大于 1）

1. **探测操作**：测试排除某项证据后系统反馈的独立逻辑闭环数
   <probe_close>证据名</probe_close>
   例如：<probe_close>A</probe_close>

2. **确认映射**：提交你认为的系统评估规则方案
   <confirm_mapping>方案字母</confirm_mapping>
   例如：<confirm_mapping>A</confirm_mapping>
   （方案字母必须是 A、B、C 或 D 之一）

3. **最终判断**：对目标证据 {target_node} 提交是否为核心定罪证据（割点）的裁断
   <final_verdict>Yes</final_verdict> 或 <final_verdict>No</final_verdict>

- 探测操作会返回 "clusters = N" 的形式，其中 N = f(C(证据))
- 确认映射操作若正确会返回 "Correct"，若错误会返回 "Incorrect" 并导致任务失败
- 最终判断操作若正确会返回 "Right"，若错误会返回 "Wrong" 并导致任务失败
- 你需要合理安排操作顺序，用尽可能少的探测次数完成任务

当你完成评估规则识别和核心证据裁断后，使用：
<answer>完成</answer>
来结束任务（仅在已成功执行确认映射和最终判断后使用）
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Case Evidence Chain Critical Support Analysis" task. Here are the rules:

The forensic system has built an undirected case evidence corroboration network G, with the key evidence (vertex) set V = {{A, B, C, D, E, J, K, F, G, L, H, P, Q, X}} and mutual corroboration relationship (edge) set:
- A-B, B-C, C-A (cross-corroboration loop)
- B-X
- D-E, E-J, J-K, K-D (chained corroboration web)
- D-X
- F-G, G-L, L-F (cross-corroboration loop)
- F-X
- X-H, H-P, H-Q

No other logical correlations exist.

For any evidence v, define C(v) as: the number of independent logical loops the remaining evidence network breaks into after excluding (overturning) evidence v and all its direct corroboration relationships.

The forensic analysis system internally uses a fixed but unknown evaluation rule f, chosen from one of the following four schemes, which remains constant throughout the analysis:
- Scheme A (Rigorous Extraction): f(C) = C
- Scheme B (Lenient Counting): f(C) = C + 1
- Scheme C (Binary Indicator): f(C) = 1 (when C equals 1), otherwise f(C) = 2
- Scheme D (Peripheral Evidence Compensation): if the evidence has only 1 corroboration relationship (degree is 1), then f(C) = C + 1, otherwise f(C) = C

Your goals are:
1. Identify the true evaluation rule f used by the system through evidence exclusion testing
2. Determine whether the target evidence {target_node} is a core convictive evidence (i.e., articulation point: whether the number of independent logical loops is greater than 1 after excluding it)

1. **Probe Operation**: Test the independent logical loop quantity fed back by the system after excluding an evidence
   <probe_close>evidence_name</probe_close>
   Example: <probe_close>A</probe_close>

2. **Confirm Mapping**: Submit your identified system evaluation rule scheme
   <confirm_mapping>scheme_letter</confirm_mapping>
   Example: <confirm_mapping>A</confirm_mapping>
   (scheme_letter must be one of A, B, C, or D)

3. **Final Verdict**: Submit your verdict on whether target evidence {target_node} is a core convictive evidence
   <final_verdict>Yes</final_verdict> or <final_verdict>No</final_verdict>

- Probe operation returns "clusters = N" format, where N = f(C(evidence))
- Confirm mapping returns "Correct" if right, "Incorrect" if wrong (causing task failure)
- Final verdict returns "Right" if correct, "Wrong" if incorrect (causing task failure)
- You need to arrange operations reasonably and complete the task with as few probes as possible

After completing evaluation rule identification and core evidence verdict, use:
<answer>done</answer>
to end the task (only use after successfully executing confirm mapping and final verdict)
"""

    tags = ["answer", "probe_close", "confirm_mapping", "final_verdict"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"mapping_scheme": "A", "target_node": "H"},
            2: {"mapping_scheme": "B", "target_node": "H"},
            3: {"mapping_scheme": "C", "target_node": "H"},
            4: {"mapping_scheme": "D", "target_node": "H"},
            5: {"mapping_scheme": "D", "target_node": "B"},
        },
        "en": {
            1: {"mapping_scheme": "A", "target_node": "H"},
            2: {"mapping_scheme": "B", "target_node": "H"},
            3: {"mapping_scheme": "C", "target_node": "H"},
            4: {"mapping_scheme": "D", "target_node": "H"},
            5: {"mapping_scheme": "D", "target_node": "B"},
        },
    }

    def __init__(self, config):
        self.graph = {
            'A': ['B', 'C'],
            'B': ['A', 'C', 'X'],
            'C': ['A', 'B'],
            'D': ['E', 'K', 'X'],
            'E': ['D', 'J'],
            'J': ['E', 'K'],
            'K': ['D', 'J'],
            'F': ['G', 'L', 'X'],
            'G': ['F', 'L'],
            'L': ['F', 'G'],
            'H': ['X', 'P', 'Q'],
            'P': ['H'],
            'Q': ['H'],
            'X': ['B', 'D', 'F', 'H'],
        }
        
        self.degrees = {node: len(neighbors) for node, neighbors in self.graph.items()}
        self.probe_count = 0
        self.mapping_confirmed = False
        self.verdict_submitted = False
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.mapping_scheme = cfg["mapping_scheme"]
        self.target_node = cfg["target_node"]
        
        self._game_info["target_node"] = self.target_node

    def _count_components(self, removed_node):
        if removed_node not in self.graph:
            return 0
        
        temp_graph = {}
        for node, neighbors in self.graph.items():
            if node == removed_node:
                continue
            temp_graph[node] = [n for n in neighbors if n != removed_node]
        
        visited = set()
        components = 0
        
        def dfs(node):
            visited.add(node)
            for neighbor in temp_graph.get(node, []):
                if neighbor not in visited:
                    dfs(neighbor)
        
        for node in temp_graph:
            if node not in visited:
                components += 1
                dfs(node)
        
        return components

    def _apply_mapping(self, real_c, node):
        if self.mapping_scheme == "A":
            return real_c
        elif self.mapping_scheme == "B":
            return real_c + 1
        elif self.mapping_scheme == "C":
            return 1 if real_c == 1 else 2
        elif self.mapping_scheme == "D":
            if self.degrees[node] == 1:
                return real_c + 1
            else:
                return real_c
        else:
            raise ValueError(f"Unknown mapping scheme: {self.mapping_scheme}")

    def evaluate(self, parsed_info):
        if self.probe_count < 1:
            return False
        if not self.mapping_confirmed:
            return False
        if not self.verdict_submitted:
            return False
        return True

    def _cf_core_produce(self, parsed_info):
        if "probe_close" in parsed_info:
            node = parsed_info["probe_close"].strip()
            if node not in self.graph:
                if self.config.language == "zh":
                    return "错误：顶点不存在。"
                else:
                    return "Error: Vertex does not exist."
            
            real_c = self._count_components(node)
            self.probe_count += 1
            observed = self._apply_mapping(real_c, node)
            return f"clusters = {observed}"
        
        elif "confirm_mapping" in parsed_info:
            scheme = parsed_info["confirm_mapping"].strip().upper()
            if scheme not in ["A", "B", "C", "D"]:
                if self.config.language == "zh":
                    return "错误：方案必须是 A、B、C 或 D。"
                else:
                    return "Error: Scheme must be A, B, C, or D."
            
            if scheme == self.mapping_scheme:
                self.mapping_confirmed = True
                return "Correct"
            else:
                self.state.set_state("failed", "incorrect mapping confirmation")
                return "Incorrect"
        
        elif "final_verdict" in parsed_info:
            verdict = parsed_info["final_verdict"].strip()
            if verdict not in ["Yes", "No"]:
                if self.config.language == "zh":
                    return "错误：判断必须是 Yes 或 No。"
                else:
                    return "Error: Verdict must be Yes or No."
            
            target_c = self._count_components(self.target_node)
            is_articulation = target_c > 1
            
            if (verdict == "Yes" and is_articulation) or (verdict == "No" and not is_articulation):
                self.verdict_submitted = True
                return "Right"
            else:
                self.state.set_state("failed", "incorrect final verdict")
                return "Wrong"
        
        else:
            raise ValueError("No valid operation tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        for node in self.graph.keys():
            real_c = self._count_components(node)
            observed = self._apply_mapping(real_c, node)
            answer = f"clusters = {observed}"
            results.append({
                "query": f"<probe_close>{node}</probe_close>",
                "answer": answer
            })
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        m = re.match(r'^(clusters\s*=\s*)(\d+)$', correct.strip())
        if m:
            prefix, val = m.group(1), int(m.group(2))
            wrong_val = val + 1 if val > 0 else val + 2
            return f"{prefix}{wrong_val}"

        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)

        if correct.strip() in ("Correct", "正确"):
            self.mapping_confirmed = False
            self.state.set_state("failed", "incorrect mapping confirmation")
            return "Incorrect" if "Correct" in correct else "错误"
        if correct.strip() in ("Incorrect", "错误"):
            self.mapping_confirmed = True
            self.state.set_state("in_progress", "")
            return "Correct" if "Incorrect" in correct else "正确"

        if correct.strip() == "Right":
            self.verdict_submitted = False
            self.state.set_state("failed", "incorrect final verdict")
            return "Wrong"
        if correct.strip() == "Wrong":
            self.verdict_submitted = True
            self.state.set_state("in_progress", "")
            return "Right"

        if "是" in correct:
            return correct.replace("是", "TEMP").replace("否", "是").replace("TEMP", "否")
        if "否" in correct:
            return correct.replace("否", "是")

        def swap_en(match):
            word = match.group(0)
            if word.isupper():
                return 'NO' if word == 'YES' else 'YES'
            if word.istitle():
                return 'No' if word == 'Yes' else 'Yes'
            return 'no' if word.lower() == 'yes' else 'yes'

        if re.search(r'\b(yes|no)\b', correct, re.IGNORECASE):
            return re.sub(r'\b(yes|no)\b', swap_en, correct, flags=re.IGNORECASE)

        return correct + "_WRONG"