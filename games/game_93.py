from .base import Game
import random

class TreeStructureIdentificationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"交互式图结构识别"的推理游戏，规则如下：

游戏设定了一个节点集合，编号为 1 到 {n}。这些节点组成了一棵未知的无向树 T（即有 {n_minus_1} 条边的连通无环图），你的目标是通过交互查询来推断出这棵树的完整边集。

游戏内部维护一个子图 S，初始为空集。S 中的边始终是树 T 的子集，且保证 S 构成一个森林（无环）。

你可以反复进行以下查询（每次一个查询）：

**查询格式**：询问两个不同的节点 u 和 v（u 不等于 v）。

**查询反馈**（包含三个信息）：
1. **连通性**：在当前子图 S 中，u 和 v 是否连通（是/否）。
2. **状态更新**：系统会自动沿着树 T 中 u 到 v 的唯一路径进行"边切换"操作——路径上的每条边，如果已在 S 中则删除，否则加入 S。
3. **更新后统计**：
   - 连通块数量：更新后 S 形成的连通分量个数（范围 1 到 {n}）
   - 开启边数量：更新后 S 中包含的边数（范围 0 到 {n_minus_1}）

当你认为已收集足够信息时，可以提交你推断出的树的边集。答案格式为一个包含 {n_minus_1} 条边的列表，每条边用两个节点编号表示（用短横线连接，顺序不限）。

**重要提示**：
- 每次只能进行一个查询或提交一次答案
- 错误的提交将导致游戏失败
- 尽量用最少的查询次数完成任务

**查询格式**（询问节点 u 和 v）：
<query>u,v</query>

**提交答案格式**（例如树有 3 条边：1-2, 2-3, 3-4）：
<answer>1-2,2-3,3-4</answer>
"""

    game_rule_en = """\
Let's play a "Tree Structure Identification" deduction game. Here are the rules:

There is a set of nodes numbered from 1 to {n}. These nodes form an unknown undirected tree T (i.e., a connected acyclic graph with {n_minus_1} edges). Your goal is to infer the complete edge set of this tree through interactive queries.

The game internally maintains a subgraph S, initially empty. Edges in S are always a subset of tree T, and S is guaranteed to form a forest (acyclic).

You can repeatedly perform the following query (one per turn):

**Query format**: Ask about two different nodes u and v (u not equal to v).

**Query feedback** (contains three pieces of information):
1. **Connectivity**: Whether u and v are connected in the current subgraph S (Yes/No).
2. **State update**: The system will automatically perform an "edge toggle" operation along the unique path from u to v in tree T—for each edge on the path, if it's already in S, remove it; otherwise, add it to S.
3. **Post-update statistics**:
   - Component count: Number of connected components formed by S after the update (range 1 to {n})
   - Active edges: Number of edges in S after the update (range 0 to {n_minus_1})

When you believe you have gathered enough information, you can submit your inferred edge set of the tree. The answer format is a list of {n_minus_1} edges, each edge represented by two node numbers (connected by a hyphen, order doesn't matter).

**Important notes**:
- Only one query or one answer submission per turn
- An incorrect submission will result in game failure
- Try to complete the task with the minimum number of queries

**Query format** (asking about nodes u and v):
<query>u,v</query>

**Answer submission format** (e.g., tree with 3 edges: 1-2, 2-3, 3-4):
<answer>1-2,2-3,3-4</answer>
"""

    contextualized_rule_zh_1 = """\
【交通场景】
我们现在来玩一个“核心路网拓扑探测”推理游戏，规则如下：

某地区的交通枢纽编号为 1 到 {n}。这些枢纽之间存在一条未知的核心主干道路网 T（这是一棵有 {n_minus_1} 条路段的连通无环网络），你的目标是通过交互调度查询来推断出这棵主干网的完整分布。

系统内部维护一个当前处于开放状态的路段子网 S，初始时路段全部封闭（空集）。S 中的路段始终是主干道 T 的一部分，且保证不存在环路。

你可以反复进行以下查询调度（每次一项）：

**查询格式**：询问两个不同的枢纽 u 和 v（u 不等于 v）。

**查询反馈**（包含三个信息）：
1. **连通性**：在当前开放的子网 S 中，枢纽 u 和 v 之间是否可以直接或间接通行（是/否）。
2. **状态更新**：系统会自动沿着主干网 T 中 u 到 v 的唯一通勤路径进行“路段状态切换”——路径上的每个路段，如果当前是开放状态则封闭（移出 S），如果当前是封闭状态则开放（加入 S）。
3. **更新后统计**：
   - 连通块数量：更新后 S 形成的互相连通的枢纽群个数（范围 1 到 {n}）
   - 开启边数量：更新后 S 中处于开放状态的路段总数（范围 0 到 {n_minus_1}）

当你认为已收集足够信息时，可以提交你推断出的主干网路段分布。答案格式为一个包含 {n_minus_1} 条路段的列表，每条路段用两个枢纽编号表示（用短横线连接，顺序不限）。

**重要提示**：
- 每次只能进行一个查询或提交一次答案
- 错误的提交将导致调查失败
- 尽量用最少的查询次数完成任务

**查询格式**（询问枢纽 u 和 v）：
<query>u,v</query>

**提交答案格式**（例如路网有 3 条路段：1-2, 2-3, 3-4）：
<answer>1-2,2-3,3-4</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Core Road Network Topology Detection" deduction game. Here are the rules:

There are traffic hubs numbered from 1 to {n} in a region. These hubs form an unknown core arterial road network T (a connected acyclic network with {n_minus_1} road segments). Your goal is to infer the complete distribution of this main network through interactive scheduling queries.

The system internally maintains a sub-network S of road segments that are currently open, initially all closed (empty set). Segments in S are always a subset of the main network T, and it is guaranteed that S forms no cycles.

You can repeatedly perform the following scheduling query (one per turn):

**Query format**: Ask about two different hubs u and v (u not equal to v).

**Query feedback** (contains three pieces of information):
1. **Connectivity**: Whether hubs u and v are mutually accessible in the currently open sub-network S (Yes/No).
2. **State update**: The system will automatically perform a "segment state toggle" along the unique commute route from u to v in the main network T—for each segment on the route, if it's currently open, it will be closed (removed from S); if closed, it will be opened (added to S).
3. **Post-update statistics**:
   - Component count: Number of interconnected hub groups formed by S after the update (range 1 to {n})
   - Active edges: Total number of open road segments in S after the update (range 0 to {n_minus_1})

When you believe you have gathered enough information, you can submit your inferred road segment distribution of the main network. The answer format is a list of {n_minus_1} segments, each represented by two hub numbers (connected by a hyphen, order doesn't matter).

**Important notes**:
- Only one query or one answer submission per turn
- An incorrect submission will result in investigation failure
- Try to complete the task with the minimum number of queries

**Query format** (asking about hubs u and v):
<query>u,v</query>

**Answer submission format** (e.g., network with 3 segments: 1-2, 2-3, 3-4):
<answer>1-2,2-3,3-4</answer>
"""

    contextualized_rule_zh_2 = """\
【医疗场景】
我们现在来玩一个“神经网络传导通路定位”推理游戏，规则如下：

生物体内有一组关键神经元，编号为 1 到 {n}。这些神经元之间存在一条未知的核心传导通路 T（这是一棵有 {n_minus_1} 条突触连接的连通无环网络），你的目标是通过电生理交互刺激来推断出该通路的完整拓扑结构。

系统内部监测一个当前处于激活状态的突触子网 S，初始时均处于休眠状态（空集）。S 中的连接始终是核心通路 T 的一部分，且保证不存在传导环路。

你可以反复进行以下刺激测试（每次一项）：

**查询格式**：刺激两个不同的神经元 u 和 v（u 不等于 v）。

**查询反馈**（包含三个信息）：
1. **连通性**：在当前激活的子网 S 中，神经元 u 和 v 的生物信号是否连通（是/否）。
2. **状态更新**：机体会沿着核心通路 T 中 u 到 v 的唯一神经传导路径产生“极化逆转”——路径上的每个突触连接，如果当前处于激活态则被抑制（移出 S），如果处于休眠态则被激活（加入 S）。
3. **更新后统计**：
   - 连通块数量：更新后 S 形成的独立信号传导区块个数（范围 1 到 {n}）
   - 开启边数量：更新后 S 中处于激活状态的突触连接总数（范围 0 到 {n_minus_1}）

当你认为已收集足够信息时，可以提交你推断出的完整通路连接图。答案格式为一个包含 {n_minus_1} 条连接的列表，每条连接用两个神经元编号表示（用短横线连接，顺序不限）。

**重要提示**：
- 每次只能进行一个查询或提交一次答案
- 错误的提交将导致定位失败
- 尽量用最少的刺激次数完成任务

**查询格式**（刺激神经元 u 和 v）：
<query>u,v</query>

**提交答案格式**（例如通路有 3 条连接：1-2, 2-3, 3-4）：
<answer>1-2,2-3,3-4</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Neural Pathway Localization" deduction game. Here are the rules:

There is a set of critical neurons in an organism numbered from 1 to {n}. These neurons form an unknown core conduction pathway T (a connected acyclic network with {n_minus_1} synaptic connections). Your goal is to infer the complete topology of this pathway through interactive electrophysiological stimulation.

The system monitors a sub-network S of currently active synaptic connections, initially all in a dormant state (empty set). Connections in S are always a subset of the core pathway T, and it is guaranteed that there are no conduction loops.

You can repeatedly perform the following stimulation test (one per turn):

**Query format**: Stimulate two different neurons u and v (u not equal to v).

**Query feedback** (contains three pieces of information):
1. **Connectivity**: Whether biological signals between neurons u and v are connected in the currently active sub-network S (Yes/No).
2. **State update**: The organism will trigger a "polarization reversal" along the unique neural conduction route from u to v in the core pathway T—for each synaptic connection on the route, if it's currently active, it gets inhibited (removed from S); if dormant, it gets activated (added to S).
3. **Post-update statistics**:
   - Component count: Number of independent signal conduction blocks formed by S after the update (range 1 to {n})
   - Active edges: Total number of active synaptic connections in S after the update (range 0 to {n_minus_1})

When you believe you have gathered enough information, you can submit your inferred complete pathway connection graph. The answer format is a list of {n_minus_1} connections, each represented by two neuron numbers (connected by a hyphen, order doesn't matter).

**Important notes**:
- Only one query or one answer submission per turn
- An incorrect submission will result in localization failure
- Try to complete the task with the minimum number of stimulations

**Query format** (stimulating neurons u and v):
<query>u,v</query>

**Answer submission format** (e.g., pathway with 3 connections: 1-2, 2-3, 3-4):
<answer>1-2,2-3,3-4</answer>
"""

    contextualized_rule_zh_3 = """\
【教育场景】
我们现在来玩一个“知识图谱前置依赖挖掘”推理游戏，规则如下：

某学科有核心知识点编号为 1 到 {n}。这些知识点之间存在一套未知的底层逻辑依赖关系 T（这是一棵有 {n_minus_1} 条依赖连线的连通无环网络），你的目标是通过互动式摸底测试推断出这套完整的依赖网络。

系统追踪一个当前学生已“点亮”的认知关联子网 S，初始为空白状态。S 中的关联始终是逻辑依赖关系 T 的一部分，且保证不存在循环论证（无环）。

你可以反复发起以下摸底测试（每次一项）：

**查询格式**：考察两个不同的知识点 u 和 v（u 不等于 v）。

**查询反馈**（包含三个信息）：
1. **连通性**：在当前已点亮的认知子网 S 中，知识点 u 和 v 的思维逻辑是否能够串联（是/否）。
2. **状态更新**：系统会顺着底层依赖关系 T 中 u 到 v 的唯一逻辑推演路径引发“认知翻转”——路径上的每个逻辑关联，如果当前已被学生掌握则暂时屏蔽（移出 S），如果未掌握则被触发理解（加入 S）。
3. **更新后统计**：
   - 连通块数量：更新后 S 形成的孤立认知聚类个数（范围 1 到 {n}）
   - 开启边数量：更新后 S 中处于点亮状态的逻辑连线总数（范围 0 到 {n_minus_1}）

当你认为已收集足够信息时，可以提交你推断出的学科依赖网络图。答案格式为一个包含 {n_minus_1} 条依赖连线的列表，每条连线用两个知识点编号表示（用短横线连接，顺序不限）。

**重要提示**：
- 每次只能发起一个查询或提交一次答案
- 错误的提交将导致评估失败
- 尽量用最少的测试次数完成评估

**查询格式**（考察知识点 u 和 v）：
<query>u,v</query>

**提交答案格式**（例如网络有 3 条连线：1-2, 2-3, 3-4）：
<answer>1-2,2-3,3-4</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Knowledge Graph Prerequisite Mining" deduction game. Here are the rules:

There are core knowledge points in a subject numbered from 1 to {n}. These points form an unknown underlying logical dependency relation T (a connected acyclic network with {n_minus_1} dependency links). Your goal is to infer the complete dependency network through interactive diagnostic testing.

The system tracks a sub-network S of cognitive associations currently "illuminated" by the student, initially blank (empty set). Associations in S are always a subset of the logical relation T, and it is guaranteed that there are no circular arguments (acyclic).

You can repeatedly initiate the following diagnostic test (one per turn):

**Query format**: Test two different knowledge points u and v (u not equal to v).

**Query feedback** (contains three pieces of information):
1. **Connectivity**: Whether the reasoning logic between points u and v can be linked in the currently illuminated cognitive sub-network S (Yes/No).
2. **State update**: The system will trigger a "cognitive flip" along the unique logical deduction path from u to v in the underlying dependency T—for each logical link on the path, if currently mastered by the student, it gets temporarily masked (removed from S); if unmastered, it gets comprehended (added to S).
3. **Post-update statistics**:
   - Component count: Number of isolated cognitive clusters formed by S after the update (range 1 to {n})
   - Active edges: Total number of illuminated logical links in S after the update (range 0 to {n_minus_1})

When you believe you have gathered enough information, you can submit your inferred subject dependency network graph. The answer format is a list of {n_minus_1} dependency links, each represented by two knowledge point numbers (connected by a hyphen, order doesn't matter).

**Important notes**:
- Only one query or one answer submission per turn
- An incorrect submission will result in assessment failure
- Try to complete the evaluation with the minimum number of tests

**Query format** (testing knowledge points u and v):
<query>u,v</query>

**Answer submission format** (e.g., network with 3 links: 1-2, 2-3, 3-4):
<answer>1-2,2-3,3-4</answer>
"""

    contextualized_rule_zh_4 = """\
【工业场景】
我们现在来玩一个“车间隐蔽供电线缆排查”推理游戏，规则如下：

某自动化工厂内有关键生产设备编号为 1 到 {n}。这些设备依靠一套未知的地下主供电线缆 T 相连（这是一棵有 {n_minus_1} 段线缆的连通无环网络），你的目标是通过试送电指令推断出整套线缆的走线布局。

控制系统监测一个当前处于“通电”状态的线缆子网 S，初始时全部断电。S 中的线缆始终是主供电线缆 T 的一部分，且保证不存在供电短路环。

你可以反复发送以下试送电指令（每次一项）：

**查询格式**：检测两个不同的设备 u 和 v（u 不等于 v）。

**查询反馈**（包含三个信息）：
1. **连通性**：在当前通电的子网 S 中，设备 u 和 v 是否处于同一供电回路上（是/否）。
2. **状态更新**：PLC控制柜会沿着供电主线缆 T 中 u 到 v 的唯一电路走线执行“继电器翻转”——路径上的每段线缆，如果当前已通电则强制断开（移出 S），如果当前已断开则闭合通电（加入 S）。
3. **更新后统计**：
   - 连通块数量：更新后 S 形成的独立供电岛个数（范围 1 到 {n}）
   - 开启边数量：更新后 S 中处于通电状态的线缆总段数（范围 0 到 {n_minus_1}）

当你认为已收集足够信息时，可以提交你推断出的地下线缆拓扑图。答案格式为一个包含 {n_minus_1} 段线缆的列表，每段线缆用两端连接的设备编号表示（用短横线连接，顺序不限）。

**重要提示**：
- 每次只能发送一个指令或提交一次答案
- 错误的提交将导致排查任务失败并触发警报
- 尽量用最少的试送电次数完成排查

**查询格式**（检测设备 u 和 v）：
<query>u,v</query>

**提交答案格式**（例如线缆有 3 段：1-2, 2-3, 3-4）：
<answer>1-2,2-3,3-4</answer>
"""

    contextualized_rule_en_4 = """\
[Industrial Scenario]
Let's play a "Workshop Hidden Power Cable Inspection" deduction game. Here are the rules:

There are critical production equipments in an automated factory numbered from 1 to {n}. These equipments are connected by an unknown underground main power cable network T (a connected acyclic network with {n_minus_1} cable segments). Your goal is to infer the entire cable routing layout through trial power-transmission commands.

The control system monitors a sub-network S of cable segments currently in an "energized" state, initially all de-energized (empty set). Segments in S are always a subset of the main power cable T, and it is guaranteed that there are no short-circuit loops.

You can repeatedly send the following trial command (one per turn):

**Query format**: Inspect two different equipments u and v (u not equal to v).

**Query feedback** (contains three pieces of information):
1. **Connectivity**: Whether equipments u and v are on the same power circuit in the currently energized sub-network S (Yes/No).
2. **State update**: The PLC control cabinet will execute a "relay toggle" along the unique circuit routing from u to v in the main cable T—for each cable segment on the route, if currently energized, it is forcibly disconnected (removed from S); if disconnected, it is closed and energized (added to S).
3. **Post-update statistics**:
   - Component count: Number of independent power supply islands formed by S after the update (range 1 to {n})
   - Active edges: Total number of energized cable segments in S after the update (range 0 to {n_minus_1})

When you believe you have gathered enough information, you can submit your inferred underground cable topology graph. The answer format is a list of {n_minus_1} cable segments, each represented by two connected equipment numbers (connected by a hyphen, order doesn't matter).

**Important notes**:
- Only one command or one answer submission per turn
- An incorrect submission will fail the inspection and trigger an alarm
- Try to complete the inspection with the minimum number of trial commands

**Query format** (inspecting equipments u and v):
<query>u,v</query>

**Answer submission format** (e.g., cable with 3 segments: 1-2, 2-3, 3-4):
<answer>1-2,2-3,3-4</answer>
"""

    contextualized_rule_zh_5 = """\
【法律场景】
我们现在来玩一个“非法资金流转隐秘链路追踪”推理游戏，规则如下：

经侦部门锁定了涉案嫌疑账户，编号为 1 到 {n}。这些账户之间利用一套未知的地下资金转移网络 T 进行洗钱（这是一棵有 {n_minus_1} 条流水链路的连通无环网络），你的目标是通过穿透审查操作推断出整套洗钱链路的真实结构。

调查系统维护一个当前已被成功“冻结追踪”的资金链路子网 S，初始时无任何线索（空集）。S 中的链路始终是地下网络 T 的一部分，且保证不存在洗钱资金回流闭环。

你可以反复发起以下穿透审查（每次一项）：

**查询格式**：审查两个不同的账户 u 和 v（u 不等于 v）。

**查询反馈**（包含三个信息）：
1. **连通性**：在当前已被追踪的子网 S 中，账户 u 和 v 之间是否存在明确的资金关联（是/否）。
2. **状态更新**：审查操作会触发犯罪集团在网络 T 中 u 到 v 的唯一流转路径上进行“反侦察切换”——路径上的流水链路，如果当前已被冻结追踪，则会被黑客手段隐藏（移出 S）；如果尚未被追踪，则会因暴露而落入法网被冻结（加入 S）。
3. **更新后统计**：
   - 连通块数量：更新后 S 形成的独立资金追踪团伙个数（范围 1 到 {n}）
   - 开启边数量：更新后 S 中处于冻结追踪状态的流水链路总数（范围 0 到 {n_minus_1}）

当你认为已收集足够证据时，可以提交你推断出的完整洗钱网络图谱。答案格式为一个包含 {n_minus_1} 条流水链路的列表，每条链路用两个账户编号表示（用短横线连接，顺序不限）。

**重要提示**：
- 每次只能发起一项审查或提交一次答案
- 错误的提交将导致打草惊蛇，调查失败
- 尽量用最少的审查次数完成取证

**查询格式**（审查账户 u 和 v）：
<query>u,v</query>

**提交答案格式**（例如链路有 3 条：1-2, 2-3, 3-4）：
<answer>1-2,2-3,3-4</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play an "Illicit Fund Transfer Hidden Link Tracking" deduction game. Here are the rules:

The economic crime investigation department has locked onto suspect accounts numbered from 1 to {n}. These accounts use an unknown underground fund transfer network T for money laundering (a connected acyclic network with {n_minus_1} transaction links). Your goal is to infer the true structure of the entire money laundering network through penetration auditing operations.

The investigation system maintains a sub-network S of transaction links currently successfully "frozen and tracked", initially with no clues (empty set). Links in S are always a subset of the underground network T, and it is guaranteed that there are no fund recirculation loops.

You can repeatedly initiate the following penetration audit (one per turn):

**Query format**: Audit two different accounts u and v (u not equal to v).

**Query feedback** (contains three pieces of information):
1. **Connectivity**: Whether there is a clear financial association between accounts u and v in the currently tracked sub-network S (Yes/No).
2. **State update**: The auditing operation triggers an "anti-reconnaissance toggle" by the criminal syndicate along the unique transfer route from u to v in network T—for each transaction link on the route, if currently frozen and tracked, it is hidden via hacker methods (removed from S); if not yet tracked, it becomes exposed and frozen by law enforcement (added to S).
3. **Post-update statistics**:
   - Component count: Number of independent tracked fund syndicates formed by S after the update (range 1 to {n})
   - Active edges: Total number of transaction links in the frozen tracking state in S after the update (range 0 to {n_minus_1})

When you believe you have gathered enough evidence, you can submit your inferred complete money laundering network graph. The answer format is a list of {n_minus_1} transaction links, each represented by two account numbers (connected by a hyphen, order doesn't matter).

**Important notes**:
- Only one audit or one answer submission per turn
- An incorrect submission will alert the suspects and fail the investigation
- Try to complete the evidence gathering with the minimum number of audits

**Query format** (auditing accounts u and v):
<query>u,v</query>

**Answer submission format** (e.g., network with 3 links: 1-2, 2-3, 3-4):
<answer>1-2,2-3,3-4</answer>
"""

    tags = ["answer", "query"]
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 4,
                "edges": [(1, 2), (2, 3), (3, 4)],
            },
            2: {
                "n": 5,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5)],
            },
            3: {
                "n": 6,
                "edges": [(1, 2), (2, 3), (2, 4), (3, 5), (3, 6)],
            },
            4: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            },
            5: {
                "n": 8,
                "edges": [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (3, 7), (7, 8)],
            },
        },
        "en": {
            1: {
                "n": 4,
                "edges": [(1, 2), (2, 3), (3, 4)],
            },
            2: {
                "n": 5,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5)],
            },
            3: {
                "n": 6,
                "edges": [(1, 2), (2, 3), (2, 4), (3, 5), (3, 6)],
            },
            4: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            },
            5: {
                "n": 8,
                "edges": [(1, 2), (2, 3), (3, 4), (2, 5), (5, 6), (3, 7), (7, 8)],
            },
        },
    }

    def __init__(self, config):
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
        self._game_info["n_minus_1"] = cfg["n"] - 1
        
        self.tree_edges = set()
        for u, v in cfg["edges"]:
            self.tree_edges.add((min(u, v), max(u, v)))
        
        self.adj = {i: [] for i in range(1, cfg["n"] + 1)}
        for u, v in self.tree_edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.active_edges = set()

    def _find_path(self, u, v):
        if u == v:
            return []
        
        from collections import deque
        queue = deque([u])
        visited = {u}
        parent = {u: None}
        
        while queue:
            node = queue.popleft()
            if node == v:
                break
            for neighbor in self.adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = node
                    queue.append(neighbor)
        
        path = []
        if v not in parent:
            return []
        current = v
        while parent[current] is not None:
            prev = parent[current]
            path.append((min(prev, current), max(prev, current)))
            current = prev
        
        return path

    def _is_connected(self, u, v):
        if u == v:
            return True
        
        current_adj = {i: [] for i in range(1, self._game_info["n"] + 1)}
        for edge_u, edge_v in self.active_edges:
            current_adj[edge_u].append(edge_v)
            current_adj[edge_v].append(edge_u)
        
        from collections import deque
        queue = deque([u])
        visited = {u}
        
        while queue:
            node = queue.popleft()
            if node == v:
                return True
            for neighbor in current_adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False

    def _count_components(self):
        n = self._game_info["n"]
        visited = set()
        components = 0
        
        current_adj = {i: [] for i in range(1, n + 1)}
        for u, v in self.active_edges:
            current_adj[u].append(v)
            current_adj[v].append(u)
        
        def dfs(node):
            visited.add(node)
            for neighbor in current_adj[node]:
                if neighbor not in visited:
                    dfs(neighbor)
        
        for i in range(1, n + 1):
            if i not in visited:
                dfs(i)
                components += 1
        
        return components

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            submitted_edges = set()
            edge_strs = [x.strip() for x in raw_ans.split(",") if x.strip()]
            
            for edge_str in edge_strs:
                if "-" not in edge_str:
                    return False
                parts = edge_str.split("-")
                if len(parts) != 2:
                    return False
                u, v = int(parts[0].strip()), int(parts[1].strip())
                if u == v:
                    return False
                submitted_edges.add((min(u, v), max(u, v)))
            
            if len(submitted_edges) != self._game_info["n_minus_1"]:
                return False
            
            return submitted_edges == self.tree_edges
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        try:
            raw_query = parsed_info["query"].strip()
            parts = [x.strip() for x in raw_query.split(",")]
            if len(parts) != 2:
                raise ValueError("Query must contain exactly two nodes.")
            
            u, v = int(parts[0]), int(parts[1])
            n = self._game_info["n"]
            
            if u < 1 or u > n or v < 1 or v > n or u == v:
                if self.config.language == "zh":
                    return "错误：节点编号无效或相同。"
                else:
                    return "Error: Invalid or identical node numbers."
            
            is_connected = self._is_connected(u, v)
            
            path = self._find_path(u, v)
            for edge in path:
                if edge in self.active_edges:
                    self.active_edges.remove(edge)
                else:
                    self.active_edges.add(edge)
            
            components = self._count_components()
            edge_count = len(self.active_edges)
            
            if self.config.language == "zh":
                conn_str = "是" if is_connected else "否"
                return f"连通={conn_str}, 连通块={components}, 开启边={edge_count}"
            else:
                conn_str = "Yes" if is_connected else "No"
                return f"connected={conn_str}, components={components}, edges={edge_count}"
            
        except ValueError as e:
            if self.config.language == "zh":
                return f"错误：{str(e)}"
            else:
                return f"Error: {str(e)}"
        except Exception:
            if self.config.language == "zh":
                return "错误：查询格式无效。"
            else:
                return "Error: Invalid query format."

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        
        original_active_edges = self.active_edges.copy()
        
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                
                is_connected = self._is_connected(u, v)
                
                path = self._find_path(u, v)
                for edge in path:
                    if edge in self.active_edges:
                        self.active_edges.remove(edge)
                    else:
                        self.active_edges.add(edge)
                
                components = self._count_components()
                edge_count = len(self.active_edges)
                
                if self.config.language == "zh":
                    conn_str = "是" if is_connected else "否"
                    ans = f"连通={conn_str}, 连通块={components}, 开启边={edge_count}"
                else:
                    conn_str = "Yes" if is_connected else "No"
                    ans = f"connected={conn_str}, components={components}, edges={edge_count}"
                
                results.append({
                    "query": f"<query>{u},{v}</query>",
                    "answer": ans
                })
                
                self.active_edges = original_active_edges.copy()
                
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                if "Yes" in correct:
                    return correct.replace("Yes", "No")
                return correct.replace("yes", "no")
            elif "no" in lower_correct:
                if "No" in correct:
                    return correct.replace("No", "Yes")
                return correct.replace("no", "yes")

        return correct + "_WRONG"