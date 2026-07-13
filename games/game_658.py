from .base import Game
import re

class GraphTriangleDetectionGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "图"
    enable_counterfactual = False

    game_rule_zh = """\
我们现在来玩一个"图结构推理"的游戏，规则如下：

游戏设定了一个包含六个节点的无向图，节点标记为 A, B, C, D, E, F。图中已存在以下边：AB, AC, AD, AE, BC, CD, DE, BE, CE。

在图论中，若三个不同节点 X, Y, Z 之间的边 XY、YZ、ZX 都存在，则这三个节点构成一个三角形。每个节点的"三角计数"T(v) 表示包含该节点的三角形总数。

已知图中各节点的真实三角计数为：
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

但是，存在一个隐藏的"接线映射"P，它会将你看到的按钮标签映射到实际的图节点。这个映射 P 只可能是以下三种之一：
1. 恒等映射：P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. 顺时针轮换：P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. 逆时针轮换：P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

你可以通过"探测"操作来获取信息：每次探测一个标签 X（A到F之一），系统会返回 T(P(X)) 的值，即该标签映射到的实际节点的三角计数。

你的目标是：
1. 推断出当前使用的是哪种接线映射 P
2. 找出目标节点 v*

其中目标节点 v* 的定义为：
- 对每个标签 X，记其显示值 R(X) = T(P(X))
- 找到使 R(X) 最大的标签 X*（若有多个，取字母序最小的）
- 则目标节点 v* = P(X*)

你需要用尽可能少的探测次数完成推理（至少需要探测两次）。

## 询问与提交答案的格式

探测某个标签（例如探测 A）：
<probe>A</probe>

提交最终答案时，需指明映射类型（identity、clockwise 或 counterclockwise）和目标节点（A到F之一）：
<answer>mapping=identity, target=A</answer>
"""

    game_rule_en = """\
Let's play a "Graph Structure Reasoning" game. Here are the rules:

The game features an undirected graph with six nodes labeled A, B, C, D, E, F. The graph contains the following edges: AB, AC, AD, AE, BC, CD, DE, BE, CE.

In graph theory, if three distinct nodes X, Y, Z have all three edges XY, YZ, and ZX, they form a triangle. Each node's "triangle count" T(v) represents the total number of triangles containing that node.

The true triangle counts for each node are:
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

However, there is a hidden "wiring mapping" P that maps the button labels you see to actual graph nodes. This mapping P can only be one of three types:
1. Identity mapping: P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. Clockwise rotation: P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. Counterclockwise rotation: P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

You can use "probe" operations to gather information: each time you probe a label X (one of A through F), the system returns the value T(P(X)), which is the triangle count of the actual node that the label maps to.

Your objectives are:
1. Determine which wiring mapping P is currently in use
2. Identify the target node v*

The target node v* is defined as:
- For each label X, let R(X) = T(P(X)) be its displayed value
- Find the label X* that maximizes R(X) (if there are ties, take the lexicographically smallest)
- Then the target node v* = P(X*)

You should complete the reasoning with as few probes as possible (at least two probes are required).

## Query and Answer Format

To probe a label (e.g., probe A):
<probe>A</probe>

When submitting your final answer, specify the mapping type (identity, clockwise, or counterclockwise) and the target node (one of A through F):
<answer>mapping=identity, target=A</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个"交通网络路由分析"的游戏，规则如下：

游戏设定了一个包含六个核心交通枢纽的管网图，枢纽标记为 A, B, C, D, E, F。图中枢纽间已开通以下双向直达线路：AB, AC, AD, AE, BC, CD, DE, BE, CE。

在交通流分析中，若三个不同枢纽 X, Y, Z 之间的线路 XY、YZ、ZX 都存在，则这三个枢纽构成一个"三角换乘微循环"。每个枢纽的"微循环计数"T(v) 表示包含该枢纽的微循环总数，它直接代表了该枢纽的交通负荷。

已知系统中各物理枢纽真实的微循环计数为：
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

但是，信号控制系统存在一个隐藏的"路由映射配置"P，它会将你看到的控制台标签映射到实际的物理枢纽。这个映射 P 只可能是以下三种之一：
1. 正常路由 (identity)：P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. 顺时针路由偏移 (clockwise)：P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. 逆时针路由偏移 (counterclockwise)：P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

你可以通过"探测"操作来获取信息：每次在控制台探测一个标签 X（A到F之一），系统会返回 T(P(X)) 的值，即该标签映射到的实际物理枢纽的微循环计数。

你的目标是：
1. 推断出当前使用的是哪种路由映射配置 P
2. 找出交通负荷最大（即微循环最多）的目标物理枢纽 v*

其中目标枢纽 v* 的定义为：
- 对每个面板标签 X，记其探测值为 R(X) = T(P(X))
- 找到使 R(X) 最大的标签 X*（若有多个，取字母序最小的）
- 则目标枢纽 v* = P(X*)

你需要用尽可能少的探测次数完成推理（至少需要探测两次）。

## 询问与提交答案的格式

探测某个面板标签（例如探测 A）：
<probe>A</probe>

提交最终答案时，需指明映射类型（identity、clockwise 或 counterclockwise）和目标枢纽（A到F之一）：
<answer>mapping=identity, target=A</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic/Transportation Scenario]
Let's play a "Traffic Network Routing Analysis" game. Here are the rules:

The game features a network graph with six core traffic hubs labeled A, B, C, D, E, F. The following bidirectional direct routes have been established between the hubs: AB, AC, AD, AE, BC, CD, DE, BE, CE.

In traffic flow analysis, if three distinct hubs X, Y, Z all have interconnected routes XY, YZ, and ZX, they form a "triangular transfer micro-cycle". Each hub's "micro-cycle count" T(v) represents the total number of micro-cycles it participates in, which directly indicates its traffic load.

The true micro-cycle counts for each physical hub are:
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

However, there is a hidden "routing mapping configuration" P in the signal control system that maps the console labels you see to the actual physical hubs. This mapping P can only be one of three types:
1. Normal routing (identity): P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. Clockwise routing offset (clockwise): P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. Counterclockwise routing offset (counterclockwise): P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

You can use "probe" operations to gather information: each time you probe a console label X (one of A through F), the system returns T(P(X)), which is the micro-cycle count of the actual physical hub mapped to that label.

Your objectives are:
1. Determine which routing mapping configuration P is currently active
2. Identify the target physical hub v* with the heaviest traffic load

The target hub v* is defined as:
- For each console label X, let its probed value be R(X) = T(P(X))
- Find the label X* that maximizes R(X) (if there are ties, take the lexicographically smallest)
- Then the target physical hub v* = P(X*)

You must complete the reasoning with as few probes as possible (at least two probes are required).

## Query and Answer Format

To probe a console label (e.g., probe A):
<probe>A</probe>

When submitting your final answer, specify the mapping type (identity, clockwise, or counterclockwise) and the target hub (one of A through F):
<answer>mapping=identity, target=A</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个"医疗调度系统诊断"的游戏，规则如下：

游戏设定了医院内的六个核心医疗科室，科室标记为 A, B, C, D, E, F。科室间已建立以下患者绿色转诊通道：AB, AC, AD, AE, BC, CD, DE, BE, CE。

在现代医疗管理中，若三个不同科室 X, Y, Z 之间的转诊通道 XY、YZ、ZX 都互通，则这三个科室构成一个"多学科联合会诊(MDT)闭环"。每个科室的"闭环计数"T(v) 表示该科室参与的 MDT 闭环总数，这代表了其医疗资源调度的核心度。

已知各科室真实的 MDT 闭环计数为：
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

但是，医院排班调度系统的接口存在一个隐藏的"接线映射配置"P，它会将你看到的系统端点标签映射到实际的物理科室。这个映射 P 只可能是以下三种之一：
1. 标准映射 (identity)：P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. 顺时针轮换接线 (clockwise)：P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. 逆时针轮换接线 (counterclockwise)：P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

你可以通过发送"诊断"指令来获取信息：每次探测一个端点标签 X（A到F之一），系统会返回 T(P(X)) 的值，即该标签实际连接科室的 MDT 闭环计数。

你的目标是：
1. 排查出当前调度系统使用的是哪种接线映射 P
2. 确认医疗资源调度压力最大的目标科室 v*

其中目标科室 v* 的定义为：
- 对每个端点标签 X，记其诊断反馈值为 R(X) = T(P(X))
- 找到使 R(X) 最大的标签 X*（若有多个，取字母序最小的）
- 则目标科室 v* = P(X*)

你需要用尽可能少的探测次数完成推理（至少需要探测两次）。

## 询问与提交答案的格式

探测某个端点标签（例如探测 A）：
<probe>A</probe>

提交最终诊断答案时，需指明映射类型（identity、clockwise 或 counterclockwise）和目标科室（A到F之一）：
<answer>mapping=identity, target=A</answer>
"""

    contextualized_rule_en_2 = """\
[Medical/Healthcare Scenario]
Let's play a "Medical Dispatch System Diagnostic" game. Here are the rules:

The game features six core medical departments in a hospital, labeled A, B, C, D, E, F. Green referral channels for patients have been established between these departments: AB, AC, AD, AE, BC, CD, DE, BE, CE.

In modern healthcare management, if three distinct departments X, Y, Z all have mutually connected channels XY, YZ, and ZX, they form a "Multidisciplinary Team (MDT) closed loop". Each department's "loop count" T(v) represents the total number of MDT closed loops it participates in, reflecting its centrality in medical resource scheduling.

The true MDT loop counts for each department are:
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

However, there is a hidden "wiring mapping configuration" P in the hospital's scheduling system interface that maps the system endpoint labels you see to the actual physical departments. This mapping P can only be one of three types:
1. Standard mapping (identity): P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. Clockwise rotation wiring (clockwise): P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. Counterclockwise rotation wiring (counterclockwise): P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

You can use "probe" diagnostic commands to gather information: each time you probe an endpoint label X (one of A through F), the system returns T(P(X)), which is the MDT loop count of the actual department connected to that label.

Your objectives are:
1. Diagnose which wiring mapping P the scheduling system is currently using
2. Identify the target department v* with the highest resource scheduling pressure

The target department v* is defined as:
- For each endpoint label X, let its diagnostic feedback value be R(X) = T(P(X))
- Find the label X* that maximizes R(X) (if there are ties, take the lexicographically smallest)
- Then the target department v* = P(X*)

You must complete the reasoning with as few diagnostic probes as possible (at least two probes are required).

## Query and Answer Format

To probe an endpoint label (e.g., probe A):
<probe>A</probe>

When submitting your final diagnostic answer, specify the mapping type (identity, clockwise, or counterclockwise) and the target department (one of A through F):
<answer>mapping=identity, target=A</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个"学术创新网络解析"的游戏，规则如下：

游戏设定了一个包含六个跨学科研究中心的教育网络，中心标记为 A, B, C, D, E, F。这些中心之间已签订了以下数据共享协议：AB, AC, AD, AE, BC, CD, DE, BE, CE。

在教育协作分析中，若三个不同中心 X, Y, Z 之间的共享协议 XY、YZ、ZX 都存在，则这三个中心构成一个"三方联合创新集群"。每个研究中心的"集群计数"T(v) 表示包含该中心的创新集群总数，这体现了其学术枢纽度。

已知各中心真实的集群计数为：
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

但是，校园网子网域名解析系统存在一个隐藏的"解析映射配置"P，它会将你查询的域名标签映射到实际的研究中心。这个映射 P 只可能是以下三种之一：
1. 静态解析 (identity)：P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. 正向轮转解析 (clockwise)：P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. 反向轮转解析 (counterclockwise)：P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

你可以通过"探测"操作来获取信息：每次对一个域名标签 X（A到F之一）进行解析测试，系统会返回 T(P(X)) 的值，即该域名实际指向中心的集群计数。

你的目标是：
1. 推断出当前 DNS 系统使用的是哪种解析映射配置 P
2. 找出学术枢纽度最高的目标研究中心 v*

其中目标中心 v* 的定义为：
- 对每个域名标签 X，记其探测值为 R(X) = T(P(X))
- 找到使 R(X) 最大的标签 X*（若有多个，取字母序最小的）
- 则目标中心 v* = P(X*)

你需要用尽可能少的探测次数完成推理（至少需要探测两次）。

## 询问与提交答案的格式

探测某个域名标签（例如探测 A）：
<probe>A</probe>

提交最终答案时，需指明映射类型（identity、clockwise 或 counterclockwise）和目标中心（A到F之一）：
<answer>mapping=identity, target=A</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play an "Academic Innovation Network Resolution" game. Here are the rules:

The game features an educational network containing six interdisciplinary research centers labeled A, B, C, D, E, F. Data sharing agreements have been signed between the centers as follows: AB, AC, AD, AE, BC, CD, DE, BE, CE.

In educational collaboration analysis, if three distinct centers X, Y, Z all have active agreements XY, YZ, and ZX, they form a "tripartite joint innovation cluster". Each research center's "cluster count" T(v) represents the total number of innovation clusters it belongs to, reflecting its degree as an academic hub.

The true cluster counts for each center are:
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

However, there is a hidden "resolution mapping configuration" P in the campus subnet DNS that maps the domain labels you query to the actual research centers. This mapping P can only be one of three types:
1. Static resolution (identity): P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. Forward rotational resolution (clockwise): P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. Reverse rotational resolution (counterclockwise): P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

You can use "probe" operations to gather information: each time you run a resolution test on a domain label X (one of A through F), the system returns T(P(X)), which is the cluster count of the actual center pointed to by that domain.

Your objectives are:
1. Determine which resolution mapping configuration P the DNS is currently using
2. Identify the target research center v* with the highest degree as an academic hub

The target center v* is defined as:
- For each domain label X, let its probed value be R(X) = T(P(X))
- Find the label X* that maximizes R(X) (if there are ties, take the lexicographically smallest)
- Then the target center v* = P(X*)

You must complete the reasoning with as few probes as possible (at least two probes are required).

## Query and Answer Format

To probe a domain label (e.g., probe A):
<probe>A</probe>

When submitting your final answer, specify the mapping type (identity, clockwise, or counterclockwise) and the target center (one of A through F):
<answer>mapping=identity, target=A</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个"工业控制总线排查"的游戏，规则如下：

游戏设定了一个包含六个自动化生产车间的厂区，车间标记为 A, B, C, D, E, F。车间之间已部署了以下物料自动输送带：AB, AC, AD, AE, BC, CD, DE, BE, CE。

在柔性制造管理中，若三个不同车间 X, Y, Z 之间的输送带 XY、YZ、ZX 都通畅，则这三个车间构成一个"柔性生产协作三角"。每个车间的"协作三角计数"T(v) 表示包含该车间的协作三角总数，这体现了其产能调度的复杂度。

已知厂区内各实际车间的协作三角计数为：
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

但是，工业控制总线(PLC)存在一个隐藏的"寻址映射模式"P，它会将你读取的寄存器标签映射到实际的生产车间。这个映射 P 只可能是以下三种之一：
1. 直连寻址 (identity)：P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. 顺时针移位寻址 (clockwise)：P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. 逆时针移位寻址 (counterclockwise)：P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

你可以通过"探测"操作来获取信息：每次通过总线探测一个寄存器标签 X（A到F之一），系统会返回 T(P(X)) 的值，即该寄存器实际对应的车间的协作三角计数。

你的目标是：
1. 排查出当前 PLC 总线使用的是哪种寻址映射模式 P
2. 锁定产能调度复杂度最大的核心生产车间 v*

其中核心车间 v* 的定义为：
- 对每个寄存器标签 X，记其探测值为 R(X) = T(P(X))
- 找到使 R(X) 最大的标签 X*（若有多个，取字母序最小的）
- 则核心车间 v* = P(X*)

你需要用尽可能少的探测次数完成排查（至少需要探测两次）。

## 询问与提交答案的格式

探测某个寄存器标签（例如探测 A）：
<probe>A</probe>

提交最终排查结论时，需指明映射类型（identity、clockwise 或 counterclockwise）和核心车间（A到F之一）：
<answer>mapping=identity, target=A</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's play an "Industrial Control Bus Troubleshooting" game. Here are the rules:

The game features a factory zone containing six automated production workshops labeled A, B, C, D, E, F. Automated material conveyor belts have been deployed between the workshops as follows: AB, AC, AD, AE, BC, CD, DE, BE, CE.

In flexible manufacturing management, if three distinct workshops X, Y, Z all have operational conveyor belts XY, YZ, and ZX, they form a "flexible production collaboration triangle". Each workshop's "collaboration triangle count" T(v) represents the total number of collaboration triangles it participates in, reflecting the complexity of its capacity scheduling.

The true collaboration triangle counts for each actual workshop are:
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

However, the Programmable Logic Controller (PLC) bus operates under a hidden "addressing mapping mode" P that maps the register labels you read to the actual production workshops. This mapping P can only be one of three types:
1. Direct addressing (identity): P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. Clockwise shift addressing (clockwise): P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. Counterclockwise shift addressing (counterclockwise): P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

You can use "probe" operations to gather information: each time you probe a register label X (one of A through F) via the bus, the system returns T(P(X)), which is the collaboration triangle count of the actual workshop corresponding to that register.

Your objectives are:
1. Troubleshoot which addressing mapping mode P the PLC bus is currently using
2. Identify the core production workshop v* with the highest capacity scheduling complexity

The core workshop v* is defined as:
- For each register label X, let its probed value be R(X) = T(P(X))
- Find the label X* that maximizes R(X) (if there are ties, take the lexicographically smallest)
- Then the core workshop v* = P(X*)

You must complete the troubleshooting with as few probes as possible (at least two probes are required).

## Query and Answer Format

To probe a register label (e.g., probe A):
<probe>A</probe>

When submitting your final conclusion, specify the mapping type (identity, clockwise, or counterclockwise) and the core workshop (one of A through F):
<answer>mapping=identity, target=A</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个"犯罪网络资金流追踪"的游戏，规则如下：

案件档案中记录了六个关键涉案实体（公司/账户），其实际代号标记为 A, B, C, D, E, F。警方已查实实体之间存在以下资金往来通道：AB, AC, AD, AE, BC, CD, DE, BE, CE。

在经济犯罪分析中，若三个不同实体 X, Y, Z 之间的资金通道 XY、YZ、ZX 都存在，则这三个实体构成一个"资金洗钱闭环"。每个实体的"闭环计数"T(v) 表示包含该实体的洗钱闭环总数，这揭示了其在整个犯罪网络中的核心地位。

已知警方掌握各实体的真实闭环计数为：
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

但是，黑客在系统中留下了一套隐藏的"加密置换规则"P，它会将你查阅的案卷代号映射到案件中真实的涉案实体。这个映射 P 只可能是以下三种之一：
1. 明文不变 (identity)：P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. 正向字母推演 (clockwise)：P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. 反向字母推演 (counterclockwise)：P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

你可以通过"提审探测"操作来获取信息：每次提审一个案卷代号 X（A到F之一），系统会返回 T(P(X)) 的值，即该代号实际指向实体的洗钱闭环数量。

你的目标是：
1. 破解出当前系统使用的是哪种加密置换规则 P
2. 锁定整个犯罪网络中的首脑实体 v*（即闭环数最大的实体）

其中首脑实体 v* 的定义为：
- 对每个案卷代号 X，记其提审结果为 R(X) = T(P(X))
- 找到使 R(X) 最大的代号 X*（若有多个，取字母序最小的）
- 则首脑实体 v* = P(X*)

你需要用尽可能少的提审探测次数完成破解（至少需要探测两次）。

## 询问与提交答案的格式

探测某个案卷代号（例如探测 A）：
<probe>A</probe>

提交最终破案报告时，需指明映射类型（identity、clockwise 或 counterclockwise）和首脑实体（A到F之一）：
<answer>mapping=identity, target=A</answer>
"""

    contextualized_rule_en_5 = """\
[Legal/Law Scenario]
Let's play a "Criminal Network Fund Flow Tracking" game. Here are the rules:

The case files record six key involved entities (companies/accounts), actually marked as A, B, C, D, E, F. The police have verified the following fund transfer channels between the entities: AB, AC, AD, AE, BC, CD, DE, BE, CE.

In economic crime analysis, if three distinct entities X, Y, Z all have interconnected fund channels XY, YZ, and ZX, they form a "money laundering closed loop". Each entity's "loop count" T(v) represents the total number of laundering loops it participates in, revealing its core status in the criminal network.

The true loop counts known to the police for each actual entity are:
- T(A) = 5
- T(B) = 3
- T(C) = 5
- T(D) = 3
- T(E) = 5
- T(F) = 0

However, a hacker left a hidden "cryptographic permutation rule" P in the system that maps the case file codes you review to the actual involved entities in the case. This mapping P can only be one of three types:
1. Plaintext unchanged (identity): P(A)=A, P(B)=B, P(C)=C, P(D)=D, P(E)=E, P(F)=F
2. Forward alphabetical deduction (clockwise): P(A)=B, P(B)=C, P(C)=D, P(D)=E, P(E)=F, P(F)=A
3. Reverse alphabetical deduction (counterclockwise): P(A)=F, P(B)=A, P(C)=B, P(D)=C, P(E)=D, P(F)=E

You can use "interrogation probe" operations to gather information: each time you probe a case file code X (one of A through F), the system returns T(P(X)), which is the number of money laundering loops for the actual entity that code points to.

Your objectives are:
1. Crack which cryptographic permutation rule P the system is currently using
2. Identify the mastermind entity v* in the criminal network (the entity with the most closed loops)

The mastermind entity v* is defined as:
- For each case file code X, let its interrogation result be R(X) = T(P(X))
- Find the code X* that maximizes R(X) (if there are ties, take the lexicographically smallest)
- Then the mastermind entity v* = P(X*)

You must complete the cracking with as few probes as possible (at least two probes are required).

## Query and Answer Format

To probe a case file code (e.g., probe A):
<probe>A</probe>

When submitting your final case report, specify the mapping type (identity, clockwise, or counterclockwise) and the mastermind entity (one of A through F):
<answer>mapping=identity, target=A</answer>
"""

    tags = ["answer", "probe"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "mapping_type": "identity",
                "description": "恒等映射，最大值为5对应A、C、E，需取A"
            },
            2: {
                "mapping_type": "clockwise",
                "description": "顺时针映射，最大值为5对应B、D、F，需取B"
            },
            3: {
                "mapping_type": "counterclockwise",
                "description": "逆时针映射，最大值为5对应B、D、F，需取B"
            },
            4: {
                "mapping_type": "clockwise",
                "description": "顺时针映射，最大值为5对应B、D、F，需取B"
            },
            5: {
                "mapping_type": "counterclockwise",
                "description": "逆时针映射，最大值为5对应B、D、F，需取B"
            },
        },
        "en": {
            1: {
                "mapping_type": "identity",
                "description": "Identity mapping, max value 5 at A, C, E, choose A"
            },
            2: {
                "mapping_type": "clockwise",
                "description": "Clockwise mapping, max value 5 at B, D, F, choose B"
            },
            3: {
                "mapping_type": "counterclockwise",
                "description": "Counterclockwise mapping, max value 5 at B, D, F, choose B"
            },
            4: {
                "mapping_type": "clockwise",
                "description": "Clockwise mapping, max value 5 at B, D, F, choose B"
            },
            5: {
                "mapping_type": "counterclockwise",
                "description": "Counterclockwise mapping, max value 5 at B, D, F, choose B"
            },
        },
    }

    def __init__(self, config):
        self.true_triangle_counts = {
            'A': 5,
            'B': 3,
            'C': 5,
            'D': 3,
            'E': 5,
            'F': 0
        }
        
        self.mappings = {
            'identity': {
                'A': 'A', 'B': 'B', 'C': 'C', 'D': 'D', 'E': 'E', 'F': 'F'
            },
            'clockwise': {
                'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': 'A'
            },
            'counterclockwise': {
                'A': 'F', 'B': 'A', 'C': 'B', 'D': 'C', 'E': 'D', 'F': 'E'
            }
        }
        
        self.probe_count = 0 
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.mapping_type = cfg["mapping_type"]
        self.current_mapping = self.mappings[self.mapping_type]
        
        self._calculate_correct_answer()
        self._game_info = {}

    def _calculate_correct_answer(self):
        readings = {}
        for label in ['A', 'B', 'C', 'D', 'E', 'F']:
            actual_node = self.current_mapping[label]
            readings[label] = self.true_triangle_counts[actual_node]
        
        max_reading = max(readings.values())
        candidates = [label for label, val in readings.items() if val == max_reading]
        candidates.sort()
        target_label = candidates[0]
        
        self.correct_target = self.current_mapping[target_label]

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        parts = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "mapping" not in ans_dict or "target" not in ans_dict:
            return False
        
        submitted_mapping = ans_dict["mapping"].lower()
        submitted_target = ans_dict["target"].upper()
        
        if submitted_mapping != self.mapping_type:
            return False
        
        if submitted_target != self.correct_target:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "probe" not in parsed_info:
            raise ValueError("No valid probe tag found.")
        
        label = parsed_info["probe"].strip().upper()
        
        if label not in ['A', 'B', 'C', 'D', 'E', 'F']:
            if self.config.language == "zh":
                return "错误：无效的标签。请使用 A 到 F 之间的标签。"
            else:
                return "Error: Invalid label. Please use labels from A to F."
        
        self.probe_count += 1
        actual_node = self.current_mapping[label]
        count = self.true_triangle_counts[actual_node]
        
        return str(count)

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        for label in ['A', 'B', 'C', 'D', 'E', 'F']:
            actual_node = self.current_mapping[label]
            count = self.true_triangle_counts[actual_node]
            results.append({
                "query": f"<probe>{label}</probe>",
                "answer": str(count)
            })
            
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
        
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            if correct == "Yes": return "No"
            if correct == "YES": return "NO"
            if correct == "yes": return "no"
            return correct.replace("Yes", "No").replace("YES", "NO").replace("yes", "no")
        if "no" in lower_correct:
            if correct == "No": return "Yes"
            if correct == "NO": return "YES"
            if correct == "no": return "yes"
            return correct.replace("No", "Yes").replace("NO", "YES").replace("no", "yes")

        return correct + "_WRONG"

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            if "answer" in parsed_info:
                if self.probe_count < 2:
                    msg = "错误：至少需要进行两次探测才能提交答案。" if self.config.language == "zh" else "Error: At least two probes are required before submitting an answer."
                    self.state.set_state("failed", "insufficient probes")
                    self.state.add_message("user", msg)
                else:
                    is_success = self.evaluate(parsed_info)
                    if is_success:
                        res = "答案正确" if self.config.language == "zh" else "Correct answer."
                        self.state.set_state("success", "success")
                        self.state.add_message("user", res)
                    else:
                        res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                        self.state.set_state("failed", "incorrect answer")
                        self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state