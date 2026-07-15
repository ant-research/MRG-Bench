from .base import Game
import re

class BinaryHypercubeReachabilityGame(Game):

    game_rule_zh = """\
我们来玩一个"二进制超立方体可达性推理"游戏。规则如下：

存在一个由所有 4 位二进制串（0000 到 1111，共 16 个节点）构成的图。任意两个仅在一位上不同的节点之间可能存在有向边。

对于每一位（第 1、2、3、4 位），系统已秘密设定了该位翻转时的边方向类型，且该类型在全图保持一致。可能的类型有三种：
- 双向：沿该位翻转的边是双向的（既可 0→1 也可 1→0）
- 仅 0→1：沿该位翻转的边只能从 0 指向 1
- 仅 1→0：沿该位翻转的边只能从 1 指向 0

给定两个节点 U = {u} 和 V = {v}，你需要判断它们是否互相可达（即是否存在 U 到 V 的有向路径，同时也存在 V 到 U 的有向路径）。

你有 12 点查询预算，可以使用以下三种查询方式：

询问从节点 X 到节点 Y 是否存在有向边。X 和 Y必须仅在一位上不同，否则返回"否"且仍消耗 1 点。

格式：
<query_edge>X,Y</query_edge>

示例：
<query_edge>0000,0001</query_edge>

尝试沿指定节点序列 X0→X1→...→Xm 行走。每对相邻节点必须仅一位不同。如果某一步的边不存在或节点格式错误，会在首个失败步 t 停止，消耗 t 点预算。

格式：
<query_path>X0,X1,X2,...,Xm</query_path>

示例：
<query_path>0000,0001,0011,0111</query_path>

给定节点 X 和一组候选邻居节点 Y1,...,Yk（每个必须与 X 仅一位不同），返回其中实际可从 X 到达的节点数量。

格式：
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

示例：
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

当你准备好答案时，请使用以下格式提交：

<answer>yes</answer>  或  <answer>no</answer>

其中 yes 表示 U 和 V 互相可达，no 表示不互相可达。

- 所有二进制串必须是 4 位（例如 0000、1010、1111）
- 预算用尽后不得继续查询
- 答案必须正确，否则游戏失败
- 尽可能用最少的查询次数完成任务
"""

    game_rule_en = """\
Let's play a "Binary Hypercube Reachability Reasoning" game. Here are the rules:

There is a graph consisting of all 4-bit binary strings (0000 to 1111, a total of 16 nodes). Any two nodes differing in exactly one bit may have a directed edge between them.

For each bit position (1st, 2nd, 3rd, 4th), the system has secretly set the edge direction type for flipping that bit, and this type is consistent throughout the entire graph. There are three possible types:
- Bidirectional: edges along this bit flip are bidirectional (both 0→1 and 1→0)
- Only 0→1: edges along this bit flip can only go from 0 to 1
- Only 1→0: edges along this bit flip can only go from 1 to 0

Given two nodes U = {u} and V = {v}, you need to determine whether they are mutually reachable (i.e., whether there exists a directed path from U to V and also a directed path from V to U).

You have 12 query points budget and can use the following three types of queries:

Ask whether there exists a directed edge from node X to node Y. X and Y must differ in exactly one bit, otherwise it returns "No" and still consumes 1 point.

Format:
<query_edge>X,Y</query_edge>

Example:
<query_edge>0000,0001</query_edge>

Attempt to walk along a specified node sequence X0→X1→...→Xm. Each pair of adjacent nodes must differ in exactly one bit. If an edge does not exist or node format is wrong at some step, it stops at the first failing step t, consuming t points.

Format:
<query_path>X0,X1,X2,...,Xm</query_path>

Example:
<query_path>0000,0001,0011,0111</query_path>

Given node X and a set of candidate neighbor nodes Y1,...,Yk (each must differ from X in exactly one bit), return the number of nodes that are actually reachable from X.

Format:
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

Example:
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

When you are ready with your answer, use the following format:

<answer>yes</answer>  or  <answer>no</answer>

where yes means U and V are mutually reachable, no means they are not mutually reachable.

- All binary strings must be 4 bits (e.g., 0000, 1010, 1111)
- No more queries after budget is exhausted
- Answer must be correct, otherwise the game fails
- Try to complete the task with as few queries as possible
"""

    contextualized_rule_zh_1 = """\
我们来使用"智能交通信号协同控制网络"分析系统。规则如下：

存在一个由所有 4 位二进制串（0000 到 1111，共 16 种调度状态）构成的信号调度图。每一位代表一个关键路口的信号灯状态（0为红灯禁行，1为绿灯通行）。任意两种仅在一个路口状态上不同的配置之间可能存在切换路径。

对于每个路口（第 1、2、3、4 位），系统预设了该路口状态切换的控制流向，且该规则在全局保持一致。可能的流向有三种：
- 双向：该路口的红绿灯切换是自由可逆的（既可 0→1 也可 1→0）
- 仅 0→1：该路口受强制通行干预，只能从红灯变为绿灯
- 仅 1→0：该路口受强制截流干预，只能从绿灯变为红灯

给定两种交通调度策略配置 U = {u} 和 V = {v}，你需要判断它们是否能互相平滑可达（即是否存在 U 到 V 的合规切换路径，同时也存在 V 到 U 的合规切换路径）。

你有 12 点查询预算，可以使用以下三种验证方式：

询问从策略 X 到策略 Y 是否存在合规的切换路径。X 和 Y 必须仅在一个路口状态上不同，否则返回"否"且仍消耗 1 点。

格式：
<query_edge>X,Y</query_edge>

示例：
<query_edge>0000,0001</query_edge>

尝试沿指定策略序列 X0→X1→...→Xm 进行连续调度。每对相邻策略必须仅一个路口不同。如果某一步的切换被拦截或格式错误，会在首个失败步 t 停止，消耗 t 点预算。

格式：
<query_path>X0,X1,X2,...,Xm</query_path>

示例：
<query_path>0000,0001,0011,0111</query_path>

给定策略 X 和一组候选相邻策略 Y1,...,Yk（每个必须与 X 仅一个路口不同），返回其中实际可从 X 合规切换到的策略数量。

格式：
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

示例：
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

当你准备好评估结论时，请使用以下格式提交：

<answer>yes</answer>  或  <answer>no</answer>

其中 yes 表示 U 和 V 互相平滑可达，no 表示不互相平滑可达。

- 所有二进制串必须是 4 位（例如 0000、1010、1111）
- 预算用尽后系统将拒绝响应
- 结论必须绝对正确，否则会导致调度事故
- 尽可能用最少的测试资源完成诊断任务
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's use the "Intelligent Traffic Signal Collaborative Control Network" analysis system. Here are the rules:

There is a signal scheduling graph consisting of all 4-bit binary strings (0000 to 1111, a total of 16 scheduling states). Each bit represents the signal status of a key intersection (0 for red light prohibition, 1 for green light pass). Any two configurations differing in exactly one intersection status may have a switching path between them.

For each intersection (1st, 2nd, 3rd, 4th bit), the system has preset the control flow for its status switch, and this rule is consistent globally. There are three possible flows:
- Bidirectional: The red/green light switch at this intersection is freely reversible (both 0→1 and 1→0).
- Only 0→1: Forced pass intervention, strictly from red to green.
- Only 1→0: Forced interception intervention, strictly from green to red.

Given two traffic scheduling strategy configurations U = {u} and V = {v}, you need to determine whether they are mutually smoothly reachable (i.e., whether there is a compliant switching path from U to V and also from V to U).

You have a budget of 12 query points. You can use three validation methods:

Ask whether there is a compliant switching path from strategy X to strategy Y. X and Y must differ in exactly one intersection, otherwise it returns "No" and consumes 1 point.

Format:
<query_edge>X,Y</query_edge>

Example:
<query_edge>0000,0001</query_edge>

Attempt continuous scheduling along the specified strategy sequence X0→X1→...→Xm. Adjacent strategies must differ by only one intersection. If a switch is blocked or formatting is incorrect, it stops at the first failing step t, consuming t points.

Format:
<query_path>X0,X1,X2,...,Xm</query_path>

Example:
<query_path>0000,0001,0011,0111</query_path>

Given strategy X and candidate adjacent strategies Y1,...,Yk (each differing by one intersection), return the count of strategies legally switchable from X.

Format:
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

Example:
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

Submit your assessment conclusion using:

<answer>yes</answer>  or  <answer>no</answer>

where yes means U and V are mutually reachable, no means they are not.

- All binary strings must be 4 bits (e.g., 0000, 1010).
- System rejects queries after budget exhaustion.
- The conclusion must be absolutely correct to prevent scheduling incidents.
- Minimize resource consumption for the diagnosis.
"""

    contextualized_rule_zh_2 = """\
我们来使用"患者并发症演化模型"评估系统。规则如下：

存在一个由所有 4 位二进制串（0000 到 1111，共 16 种体征组合）构成的临床状态网络。每一位代表一个关键器官的衰竭状态（0为健康，1为衰竭）。任意两个仅在一项体征上不同的状态组合之间可能存在病理演变路径。

对于每个器官（第 1、2、3、4 位），模型设定了该项体征发生变化的演变规律，且规律在全身机制中保持一致。可能的演变规律有三种：
- 双向：该器官的状况存在波动的可能（既可健康转衰竭 0→1，也能治愈恢复 1→0）
- 仅 0→1：该器官病变不可逆，只能从健康走向衰竭
- 仅 1→0：该器官被特效药靶向干预，一旦好转将不再复发恶化（只能 1→0）

给定两种患者体征状态 U = {u} 和 V = {v}，你需要判断它们是否可能互相演化（即是否存在 U 恶化/缓解为 V 的病理路径，同时也存在 V 反向演变回 U 的可能，形成疾病反复循环）。

你有 12 点查询预算，可以使用以下三种检验方式：

询问从体征 X 到体征 Y 是否存在演变路径。X 和 Y 必须仅在一个器官状态上不同，否则返回"否"且仍消耗 1 点。

格式：
<query_edge>X,Y</query_edge>

示例：
<query_edge>0000,0001</query_edge>

尝试沿体征恶化/好转序列 X0→X1→...→Xm 进行推演。每对相邻状态必须仅一个器官不同。如果某一步演变不符合病理或格式错误，会在首个失败步 t 停止，消耗 t 点预算。

格式：
<query_path>X0,X1,X2,...,Xm</query_path>

示例：
<query_path>0000,0001,0011,0111</query_path>

给定状态 X 和一组候选的单病变差异状态 Y1,...,Yk，返回其中实际可能由 X 演变过去的体征状态数量。

格式：
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

示例：
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

当你确诊后，请使用以下格式提交：

<answer>yes</answer>  或  <answer>no</answer>

其中 yes 表示 U 和 V 可能陷入反复演化循环，no 表示不会形成这种互相演化。

- 所有二进制串必须是 4 位（例如 0000、1010、1111）
- 诊疗预算用尽后不得继续测试
- 诊断结果必须严谨准确，否则评估失败
- 尽可能以最小的代价完成疾病演变链的排查
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's use the "Patient Complication Evolution Model" assessment system. Here are the rules:

There is a clinical state network consisting of all 4-bit binary strings (0000 to 1111, a total of 16 sign combinations). Each bit represents the failure status of a key organ (0 for healthy, 1 for failed). Any two state combinations differing in exactly one organ status may have a pathological evolution path between them.

For each organ (1st, 2nd, 3rd, 4th bit), the model has set an evolution rule, consistent throughout the systemic mechanism. There are three possible rules:
- Bidirectional: The organ's condition can fluctuate (both healthy to failed 0→1, and healed 1→0).
- Only 0→1: The organ lesion is irreversible, strictly from healthy to failed.
- Only 1→0: Targeted by specific medication, once healed, it won't relapse (strictly 1→0).

Given two patient sign states U = {u} and V = {v}, determine if they can mutually evolve into each other (i.e., a pathological path from U to V exists, and a reverse path from V to U exists, forming a recurring disease loop).

You have 12 query points budget. You can use three diagnostic tests:

Ask if there is an evolution path from state X to Y. X and Y must differ in exactly one organ, otherwise it returns "No" and consumes 1 point.

Format:
<query_edge>X,Y</query_edge>

Example:
<query_edge>0000,0001</query_edge>

Attempt a deduction along the sequence X0→X1→...→Xm. Adjacent states must differ by only one organ. If a step violates pathology or formatting, it stops at the first failing step t, consuming t points.

Format:
<query_path>X0,X1,X2,...,Xm</query_path>

Example:
<query_path>0000,0001,0011,0111</query_path>

Given state X and candidate adjacent states Y1,...,Yk, return the count of states that can actually evolve from X.

Format:
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

Example:
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

Submit your clinical diagnosis using:

<answer>yes</answer>  or  <answer>no</answer>

where yes means U and V form a mutually evolving loop, no means they do not.

- All binary strings must be 4 bits (e.g., 0000, 1010).
- No more tests allowed after diagnostic budget exhaustion.
- Diagnosis must be strictly accurate.
- Try to complete the pathological chain investigation with minimal cost.
"""

    contextualized_rule_zh_3 = """\
我们来使用"自适应学习知识图谱"诊断系统。规则如下：

存在一个由所有 4 位二进制串（0000 到 1111，共 16 种知识状态集合）构成的认知网络。每一位代表一个核心前置知识模块的掌握情况（0为未达标，1为已掌握）。任何仅在一个知识点上存在差异的两个状态之间，可能存在认知转移路径。

对于每个知识模块（第 1、2、3、4 位），系统定义了该模块的记忆与遗忘规律，规律对全体学生一致。可能的规律有三种：
- 双向：该模块既可以通过学习掌握，也可能随着时间遗忘（既可 0→1 也可 1→0）
- 仅 0→1：属于深层原理认知，一旦领悟就不会再遗忘（只能 0→1）
- 仅 1→0：属于临时机械记忆，只会随时间消退，当前路径不支持重新习得（只能 1→0）

给定学生的两种认知状态集合 U = {u} 和 V = {v}，你需要判断它们是否能互相重构（即学生是否可以通过学习和遗忘从状态 U 转变到 V，同时也能从 V 转变回 U）。

你有 12 点查询预算，可以使用以下三种诊断方式：

测试从认知状态 X 到状态 Y 是否存在合理的迁移路径。X 和 Y 必须仅在一个知识点上不同，否则返回"否"且仍消耗 1 点。

格式：
<query_edge>X,Y</query_edge>

示例：
<query_edge>0000,0001</query_edge>

尝试沿着设定的学习演进路线 X0→X1→...→Xm 进行追踪。相邻状态必须仅一个知识点不同。如果中间某一步不符合认知规律或格式错误，将在首个失败步 t 停止，消耗 t 点预算。

格式：
<query_path>X0,X1,X2,...,Xm</query_path>

示例：
<query_path>0000,0001,0011,0111</query_path>

给定当前状态 X 和一组可能相邻的认知状态 Y1,...,Yk，返回从 X 出发实际可能自然演进到的状态数量。

格式：
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

示例：
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

当你完成学习路径评估后，请使用以下格式提交：

<answer>yes</answer>  或  <answer>no</answer>

其中 yes 表示 U 和 V 能够互相重构，no 表示不能。

- 所有二进制串必须是 4 位（例如 0000、1010、1111）
- 诊断算力（预算）用尽后强制中断
- 评估结果必须完全正确，否则会导致教学方案误判
- 请以最高效的测试路径查明真相
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's use the "Adaptive Learning Knowledge Graph" diagnostic system. Here are the rules:

There is a cognitive network consisting of all 4-bit binary strings (0000 to 1111, 16 knowledge state sets). Each bit represents the mastery of a core prerequisite knowledge module (0 for unmet, 1 for mastered). A cognitive transition path may exist between any two states differing by exactly one knowledge point.

For each knowledge module (1st, 2nd, 3rd, 4th bit), the system defines its memory and forgetting pattern, applied consistently. There are three possible patterns:
- Bidirectional: Can be learned and can also be forgotten over time (both 0→1 and 1→0).
- Only 0→1: Deep conceptual understanding; once grasped, it's never forgotten.
- Only 1→0: Temporary rote memory; it only decays over time and cannot be relearned via the current path.

Given two student cognitive state sets U = {u} and V = {v}, determine if they can mutually reconstruct each other (i.e., whether learning/forgetting paths exist from U to V, and back from V to U).

You have a budget of 12 query points, supporting three diagnostic methods:

Test if a valid transition path exists from cognitive state X to Y. X and Y must differ by exactly one knowledge point, otherwise it returns "No" and consumes 1 point.

Format:
<query_edge>X,Y</query_edge>

Example:
<query_edge>0000,0001</query_edge>

Trace a designated learning evolution route X0→X1→...→Xm. Adjacent states must differ by one knowledge point. If a step breaks cognitive rules or formatting, it halts at the first failing step t, consuming t points.

Format:
<query_path>X0,X1,X2,...,Xm</query_path>

Example:
<query_path>0000,0001,0011,0111</query_path>

Given current state X and candidate adjacent states Y1,...,Yk, return the count of states naturally reachable from X.

Format:
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

Example:
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

Submit your learning path assessment using:

<answer>yes</answer>  or  <answer>no</answer>

where yes means U and V are mutually reconstructible, no means they are not.

- All binary strings must be 4 bits (e.g., 0000, 1010).
- Diagnostics forcibly halt when budget is exhausted.
- Incorrect assessments will lead to misjudged teaching plans.
- Discover the truth using the most efficient testing route.
"""

    contextualized_rule_zh_4 = """\
我们来操作"工业反应堆阀门联锁系统"安全校验台。规则如下：

反应堆的联锁图由所有 4 位二进制串（0000 到 1111，共 16 种工作模式）构成。每一位代表一个关键安全阀门的开闭状态（0为关闭，1为开启）。任意两个仅在一只阀门状态上不同的模式之间可能存在操作切换路径。

对于每只阀门（第 1、2、3、4 位），安全规程硬编码了该阀门的动作方向限制，且在所有模式中一致。可能的限制有三种：
- 双向：该阀门支持随时开启或关闭（既可 0→1 也可 1→0）
- 仅 0→1：防回流单向阀，操作规程规定仅允许将其开启，严禁在线关闭
- 仅 1→0：泄压保安阀，一旦闭合必须停机人工复位，在线状态仅允许执行关闭动作

给定两种工艺工作模式 U = {u} 和 V = {v}，你需要校验它们是否能互相安全切换（即是否存在从模式 U 调整至 V 的合规路径，且能从 V 再次合规调回 U，无死锁）。

你有 12 点测试能耗（预算），可使用三种遥测指令：

发送指令试探从模式 X 到模式 Y 的切换是否符合规程。X 和 Y 必须仅在一个阀门上不同，否则返回"否"且仍消耗 1 点能耗。

格式：
<query_edge>X,Y</query_edge>

示例：
<query_edge>0000,0001</query_edge>

模拟执行一连串的工艺状态切换序列 X0→X1→...→Xm。每对相邻模式仅允许一个阀门动作。遇到违规动作或报文格式错误时，会在首个失败步 t 触发安全拦截，并扣除 t 点能耗。

格式：
<query_path>X0,X1,X2,...,Xm</query_path>

示例：
<query_path>0000,0001,0011,0111</query_path>

基于当前模式 X 和一组候选的单阀动作模式 Y1,...,Yk，扫描出实际符合安全规程的下一步模式数量。

格式：
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

示例：
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

校验得出结论后，按以下格式上报：

<answer>yes</answer>  或  <answer>no</answer>

yes 表示模式 U 和 V 可以互相安全切换；no 表示不可互相切换，存在不可逆死锁。

- 所有模式编码必须是 4 位二进制（例如 0000、1010）
- 能耗耗尽系统将锁定操作权限
- 上报结论必须 100% 正确，否则判定严重安全事故
- 用尽可能少的操作步数完成校验
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's operate the "Industrial Reactor Valve Interlock System" safety verification console. Here are the rules:

The reactor's interlock graph consists of all 4-bit binary strings (0000 to 1111, 16 operating modes). Each bit represents the open/close status of a key safety valve (0 for closed, 1 for open). An operational switching path may exist between any two modes differing by exactly one valve status.

For each valve (1st, 2nd, 3rd, 4th bit), safety protocols hardcode its action direction limits, consistent across all modes. There are three possible limits:
- Bidirectional: The valve supports opening or closing at any time (both 0→1 and 1→0).
- Only 0→1: Anti-backflow check valve; protocols only allow it to be opened, strict prohibition on closing online.
- Only 1→0: Pressure relief security valve; once closed, it requires manual manual reset after shutdown. Only closing actions are allowed online.

Given two process operating modes U = {u} and V = {v}, verify if they can be safely switched back and forth (i.e., a compliant path from U to V exists, and a reverse path from V to U exists, with no deadlocks).

You have 12 units of testing energy (budget), supporting three telemetry commands:

Send a command to probe if switching from mode X to Y complies with protocols. X and Y must differ by exactly one valve, otherwise it returns "No" and consumes 1 unit.

Format:
<query_edge>X,Y</query_edge>

Example:
<query_edge>0000,0001</query_edge>

Simulate executing a sequence of process state switches X0→X1→...→Xm. Adjacent modes allow only one valve action. Upon illegal action or formatting error, a safety interlock triggers at failing step t, costing t units.

Format:
<query_path>X0,X1,X2,...,Xm</query_path>

Example:
<query_path>0000,0001,0011,0111</query_path>

Based on current mode X and candidate single-valve-action modes Y1,...,Yk, scan the count of valid next modes adhering to safety protocols.

Format:
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

Example:
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

Upon reaching a conclusion, report via:

<answer>yes</answer>  or  <answer>no</answer>

where yes means U and V can mutually switch safely, no indicates irreversible deadlock.

- Mode codes must be 4-bit binary (e.g., 0000, 1010).
- System locks operating permissions when energy is depleted.
- The conclusion must be 100% correct to prevent severe safety incidents.
- Accomplish the verification using minimal operation steps.
"""

    contextualized_rule_zh_5 = """\
我们来使用"法庭庭审证据链推演"辅助决策系统。规则如下：

所有的诉讼局势可以映射为一个由 4 位二进制串（0000 到 1111，共 16 种局势）构成的推演图。每一位代表一项核心诉讼主张的庭审采信状态（0为被驳回，1为被采信支持）。庭审辩论使得任意两个仅在一项主张上不同的局势间存在变更的可能。

对于每项主张（第 1、2、3、4 位），证据法规则决定了其状态能否在庭审期间发生变更，且适用于整个庭审阶段。可能的变更规则有三种：
- 双向：该主张存在高度争议，可以在支持与驳回之间反复摇摆（既可 0→1 也可 1→0）
- 仅 0→1：该主张属于对方当事人自认，一旦提交被采信即刻固定，不可撤回（只能 0→1）
- 仅 1→0：该主张因己方失误宣布放弃或核心证据被伪证鉴定推翻，一旦失效不可再重新主张（只能 1→0）

给定两种案情局势状态 U = {u} 和 V = {v}，你需要判断它们是否可能在控辩交锋中互相反转（即是否存在一套辩论策略能将局势从 U 推向 V，同时也存在应对策略能将局势从 V 挽回至 U）。

你有 12 点推演预算（代表庭审有限的时间），可采取三种法庭推演手段：

向系统询问从局势 X 变更为局势 Y 在法理上是否可行。X 和 Y 必须仅存在一项主张不同，否则系统返回"否"且庭审时间仍扣除 1 点。

格式：
<query_edge>X,Y</query_edge>

示例：
<query_edge>0000,0001</query_edge>

尝试论证一连串的局势演进路线 X0→X1→...→Xm。相邻局势仅能变更一项主张状态。若某个逻辑环环相扣的步骤不符合证据规则或陈述格式错误，法官会在此步 t 打断，消耗 t 点时间。

格式：
<query_path>X0,X1,X2,...,Xm</query_path>

示例：
<query_path>0000,0001,0011,0111</query_path>

在当前局势 X 下，针对提供的 k 种可能只变动一项主张的后续局势 Y1,...,Yk，盘点出法理上实际可能走向的有效局势数量。

格式：
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

示例：
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

当你完成卷宗分析后，递交你的最终法律意见：

<answer>yes</answer>  或  <answer>no</answer>

yes 表示局势 U 和 V 可能陷入互相反转的拉锯战，no 表示不会发生互逆演变。

- 局势编码严格为 4 位二进制（如 0000、1010）
- 时间预算耗尽意味着休庭，无法继续推演
- 法律意见需绝对准确，关系到最终诉讼胜败
- 请作为资深律师，以最精简的试探锁定胜局
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's employ the "Court Trial Evidence Chain Deduction" decision-support system. Here are the rules:

All litigation situations can be mapped into a deduction graph composed of all 4-bit binary strings (0000 to 1111, 16 situations). Each bit represents the acceptance status of a core litigation claim (0 for rejected, 1 for supported). Courtroom debates allow state changes between any two situations differing by exactly one claim.

For each claim (1st, 2nd, 3rd, 4th bit), evidence law rules dictate its changeability during the trial, applying across the entire proceeding. There are three variation rules:
- Bidirectional: The claim is highly contentious and can swing repeatedly between supported and rejected (both 0→1 and 1→0).
- Only 0→1: Admission by the opposing party; once submitted and accepted, it is fixed and irrevocable.
- Only 1→0: Waived by error or overturned by perjury identification; once invalidated, it cannot be re-asserted.

Given two case situations U = {u} and V = {v}, deduce if they could mutually reverse during the prosecution-defense clashes (i.e., debate strategies can shift U to V, and countermeasures can salvage V back to U).

You have 12 deduction points budget (representing limited trial time), offering three tactical tools:

Query if changing from situation X to Y is legally viable. X and Y must differ by exactly one claim, otherwise the system returns "No" while still deducting 1 point of trial time.

Format:
<query_edge>X,Y</query_edge>

Example:
<query_edge>0000,0001</query_edge>

Argue a sequence of situation evolutions X0→X1→...→Xm. Adjacent situations can alter only one claim status. If any interconnected step breaches evidence rules or is improperly formatted, the judge interrupts at step t, costing t points.

Format:
<query_path>X0,X1,X2,...,Xm</query_path>

Example:
<query_path>0000,0001,0011,0111</query_path>

Under situation X, evaluate the provided candidate subsequent situations Y1,...,Yk (single claim variance). Return the count of legally reachable valid situations.

Format:
<query_neighbors>X;Y1,Y2,...,Yk</query_neighbors>

Example:
<query_neighbors>0000;0001,0010,0100,1000</query_neighbors>

Upon concluding the case file analysis, submit your final legal opinion:

<answer>yes</answer>  or  <answer>no</answer>

where yes indicates situations U and V could enter a seesaw battle of mutual reversals, no means reciprocal evolution is impossible.

- Situation codes strictly require 4-bit binary (e.g., 0000, 1010).
- Budget exhaustion means court adjournment, halting further deduction.
- Legal opinion must be flawlessly accurate, dictating case victory or defeat.
- Act as a senior attorney and secure the victory using the most concise probing.
"""

    tags = ["answer", "query_edge", "query_path", "query_neighbors"]
    reasoning_type = "归纳推理"
    data_structure = "图"

    
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "u": "0000",
                "v": "0000",
                "directions": [0, 0, 1, 1],
                "answer": True,
            },
            2: {
                "u": "0000",
                "v": "0011",
                "directions": [1, 1, 0, 0],
                "answer": True,
            },
            3: {
                "u": "0000",
                "v": "0100",
                "directions": [0, 1, 1, 2],
                "answer": False,
            },
            4: {
                "u": "0011",
                "v": "1100",
                "directions": [0, 0, 1, 2],
                "answer": False,
            },
            5: {
                "u": "0101",
                "v": "1010",
                "directions": [1, 0, 2, 0],
                "answer": False,
            },
        },
        "en": {
            1: {
                "u": "0000",
                "v": "0000",
                "directions": [0, 0, 1, 1],
                "answer": True,
            },
            2: {
                "u": "0000",
                "v": "0011",
                "directions": [1, 1, 0, 0],
                "answer": True,
            },
            3: {
                "u": "0000",
                "v": "0100",
                "directions": [0, 1, 1, 2],
                "answer": False,
            },
            4: {
                "u": "0011",
                "v": "1100",
                "directions": [0, 0, 1, 2],
                "answer": False,
            },
            5: {
                "u": "0101",
                "v": "1010",
                "directions": [1, 0, 2, 0],
                "answer": False,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["u"] = cfg["u"]
        self._game_info["v"] = cfg["v"]
        
        self.directions = cfg["directions"]
        self.correct_answer = cfg["answer"]
        
        self.budget_used = 0
        self.budget_limit = 12

    def _is_valid_binary(self, s):
        return isinstance(s, str) and len(s) == 4 and all(c in '01' for c in s)

    def _hamming_distance(self, s1, s2):
        if not (self._is_valid_binary(s1) and self._is_valid_binary(s2)):
            return -1
        return sum(c1 != c2 for c1, c2 in zip(s1, s2))

    def _get_diff_bit(self, s1, s2):
        if self._hamming_distance(s1, s2) != 1:
            return -1
        for i in range(4):
            if s1[i] != s2[i]:
                return i
        return -1

    def _has_edge(self, x, y):
        bit_idx = self._get_diff_bit(x, y)
        if bit_idx == -1:
            return False
        
        direction = self.directions[bit_idx]
        x_bit = int(x[bit_idx])
        y_bit = int(y[bit_idx])
        
        if direction == 0:
            return True
        elif direction == 1:
            return x_bit == 0 and y_bit == 1
        elif direction == 2:
            return x_bit == 1 and y_bit == 0
        return False

    def evaluate(self, parsed_info):
        answer = parsed_info["answer"].strip().lower()
        if answer == "yes":
            return self.correct_answer == True
        elif answer == "no":
            return self.correct_answer == False
        else:
            return False

    def _cf_core_produce(self, parsed_info):
        yes_str = "是" if self.config.language == "zh" else "Yes"
        no_str = "否" if self.config.language == "zh" else "No"
        error_budget = ("查询预算已用尽，请直接提交答案。" 
                       if self.config.language == "zh" 
                       else "Query budget exhausted. Please submit your answer directly.")
        error_format = "格式错误" if self.config.language == "zh" else "Invalid format"
        
        if self.budget_used >= self.budget_limit:
            return error_budget

        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [p.strip() for p in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError()
                x, y = parts
                
                self.budget_used += 1
                remaining = max(0, self.budget_limit - self.budget_used)
                
                if not (self._is_valid_binary(x) and self._is_valid_binary(y)):
                    result = no_str
                elif self._hamming_distance(x, y) != 1:
                    result = no_str
                else:
                    result = yes_str if self._has_edge(x, y) else no_str
                
                budget_info = f"（剩余预算：{remaining}）" if self.config.language == "zh" else f"(Remaining budget: {remaining})"
                return f"{result} {budget_info}"
            except:
                self.budget_used += 1
                remaining = max(0, self.budget_limit - self.budget_used)
                budget_info = f"（剩余预算：{remaining}）" if self.config.language == "zh" else f"(Remaining budget: {remaining})"
                return f"{error_format} {budget_info}"

        elif "query_path" in parsed_info:
            try:
                raw = parsed_info["query_path"].strip()
                nodes = [n.strip() for n in raw.split(",")]
                
                if len(nodes) < 2:
                    raise ValueError()
                
                if not self._is_valid_binary(nodes[0]):
                    self.budget_used += 1
                    remaining = max(0, self.budget_limit - self.budget_used)
                    budget_info = f"（剩余预算：{remaining}）" if self.config.language == "zh" else f"(Remaining budget: {remaining})"
                    return f"{error_format} {budget_info}"
                
                for i in range(len(nodes) - 1):
                    step_num = i + 1
                    if not self._is_valid_binary(nodes[i + 1]):
                        cost = step_num
                        self.budget_used += cost
                        remaining = max(0, self.budget_limit - self.budget_used)
                        fail_msg = f"第 {step_num} 步失败" if self.config.language == "zh" else f"Failed at step {step_num}"
                        budget_info = f"（消耗 {cost} 点，剩余预算：{remaining}）" if self.config.language == "zh" else f"(Cost {cost} points, remaining: {remaining})"
                        return f"{fail_msg} {budget_info}"
                    if self._hamming_distance(nodes[i], nodes[i + 1]) != 1:
                        cost = step_num
                        self.budget_used += cost
                        remaining = max(0, self.budget_limit - self.budget_used)
                        fail_msg = f"第 {step_num} 步失败" if self.config.language == "zh" else f"Failed at step {step_num}"
                        budget_info = f"（消耗 {cost} 点，剩余预算：{remaining}）" if self.config.language == "zh" else f"(Cost {cost} points, remaining: {remaining})"
                        return f"{fail_msg} {budget_info}"
                    if not self._has_edge(nodes[i], nodes[i + 1]):
                        cost = step_num
                        self.budget_used += cost
                        remaining = max(0, self.budget_limit - self.budget_used)
                        fail_msg = f"第 {step_num} 步失败" if self.config.language == "zh" else f"Failed at step {step_num}"
                        budget_info = f"（消耗 {cost} 点，剩余预算：{remaining}）" if self.config.language == "zh" else f"(Cost {cost} points, remaining: {remaining})"
                        return f"{fail_msg} {budget_info}"
                
                cost = len(nodes) - 1
                self.budget_used += cost
                remaining = max(0, self.budget_limit - self.budget_used)
                success_msg = "成功" if self.config.language == "zh" else "Success"
                budget_info = f"（消耗 {cost} 点，剩余预算：{remaining}）" if self.config.language == "zh" else f"(Cost {cost} points, remaining: {remaining})"
                return f"{success_msg} {budget_info}"
            except:
                self.budget_used += 1
                remaining = max(0, self.budget_limit - self.budget_used)
                budget_info = f"（剩余预算：{remaining}）" if self.config.language == "zh" else f"(Remaining budget: {remaining})"
                return f"{error_format} {budget_info}"

        elif "query_neighbors" in parsed_info:
            try:
                raw = parsed_info["query_neighbors"].strip()
                parts = raw.split(";")
                if len(parts) != 2:
                    raise ValueError()
                
                x = parts[0].strip()
                neighbors = [n.strip() for n in parts[1].split(",")]
                
                if not self._is_valid_binary(x):
                    raise ValueError()
                
                k = len(neighbors)
                self.budget_used += k
                remaining = max(0, self.budget_limit - self.budget_used)
                
                count = 0
                for y in neighbors:
                    if self._is_valid_binary(y) and self._hamming_distance(x, y) == 1 and self._has_edge(x, y):
                        count += 1
                
                budget_info = f"（消耗 {k} 点，剩余预算：{remaining}）" if self.config.language == "zh" else f"(Cost {k} points, remaining: {remaining})"
                return f"{count} {budget_info}"
            except:
                self.budget_used += 1
                remaining = max(0, self.budget_limit - self.budget_used)
                budget_info = f"（剩余预算：{remaining}）" if self.config.language == "zh" else f"(Remaining budget: {remaining})"
                return f"{error_format} {budget_info}"

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        yes_str = "是" if self.config.language == "zh" else "Yes"
        no_str = "否" if self.config.language == "zh" else "No"
        
        nodes = [f"{i:04b}" for i in range(16)]
        
        for u in nodes:
            for v in nodes:
                if self._hamming_distance(u, v) == 1:
                    is_edge = self._has_edge(u, v)
                    ans = yes_str if is_edge else no_str
                    queries.append({
                        "query": f"<query_edge>{u},{v}</query_edge>",
                        "answer": ans
                    })

        for u in nodes:
            neighbors = []
            for v in nodes:
                if self._hamming_distance(u, v) == 1:
                    neighbors.append(v)
            
            neighbors.sort()
            neighbors_str = ",".join(neighbors)
            
            count = 0
            for v in neighbors:
                if self._has_edge(u, v):
                    count += 1
            
            queries.append({
                "query": f"<query_neighbors>{u};{neighbors_str}</query_neighbors>",
                "answer": str(count)
            })
            
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            if "No" in correct:
                return correct.replace("No", "Yes")
            if "yes" in correct:
                return correct.replace("yes", "no")
            if "no" in correct:
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"