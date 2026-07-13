# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   根到节点路径：从根节点到某给定节点经过哪些节点
# ============================================================

from .base import Game
import re


class WiringSchemaPuzzle(Game):

    game_rule_zh = """\
我们来玩一个"接线方案推理"游戏。游戏设定如下：

给定一棵固定的有序根树T，节点以整数编号，每个节点的子节点有从左到右的固定顺序。树的结构如下：

{tree_structure}

起始节点：{start_node}（根节点）
目标节点：{target_node}

游戏中有三个操作符（控制信号）：c1、c2、c3。每次你在当前节点执行其中一个操作符，会尝试选择该节点的第k个子节点并移动到该子节点。k由一个未知但固定的接线方案S决定。

接线方案S只可能是以下四种之一（在整个游戏过程中保持不变）：
- S_A: c1选第1子, c2选第1子, c3选第2子
- S_B: c1选第1子, c2选第2子, c3选第1子
- S_C: c1选第2子, c2选第1子, c3选第2子
- S_D: c1选第2子, c2选第2子, c3选第1子

注意：如果当前节点的子节点数量小于所选的子序号（越界），则不会移动，视为"受阻"。

## 可用操作

你可以使用以下操作与游戏交互：

1. 移动操作：在当前节点执行操作符（c1、c2或c3）
<move>c1</move>

2. 重置位置：将位置重置回起始节点
<reset></reset>

3. 查询当前位置：询问当前所在节点编号
<where></where>

4. 查询度数：询问当前节点的子节点数量
<degree></degree>

5. 查询子节点：询问指定节点的有序子节点列表
<children>6</children>

6. 检查目标：询问当前节点是否为目标节点
<is_target></is_target>

## 提交最终答案

当你推断出接线方案并找到从起始节点到目标节点的路径后，必须一次性提交三项内容：

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

答案格式说明：
- DECLARE：接线方案（S_A、S_B、S_C或S_D之一）
- PATH：节点序列，用"-"连接（例如：1-2-6-12）
- LABELS：操作符序列，用"-"连接，与PATH中的边一一对应（例如：c2-c1-c3）

校验规则：
1. DECLARE必须是四种方案之一
2. 使用DECLARE指定的方案，将LABELS映射为子序号序列，必须与PATH中相邻节点之间的父子关系匹配
3. PATH必须从起始节点开始，准确到达目标节点
4. 每一步移动都不能越界或受阻

你的目标是用尽可能少的操作次数识别接线方案，并构造正确的路径和操作序列。
"""

    game_rule_en = """\
Let's play a "Wiring Schema Inference" puzzle. The game setup is as follows:

Given a fixed ordered rooted tree T, where nodes are numbered with integers and each node's children have a fixed left-to-right order. The tree structure is:

{tree_structure}

Starting node: {start_node} (root)
Target node: {target_node}

There are three operators (control signals): c1, c2, c3. Each time you execute one operator at the current node, it attempts to select the k-th child of that node and move to it. The value k is determined by an unknown but fixed wiring schema S.

Schema S can only be one of the following four (remains constant throughout the game):
- S_A: c1→1st child, c2→1st child, c3→2nd child
- S_B: c1→1st child, c2→2nd child, c3→1st child
- S_C: c1→2nd child, c2→1st child, c3→2nd child
- S_D: c1→2nd child, c2→2nd child, c3→1st child

Note: If the current node has fewer children than the selected child index (out of bounds), no movement occurs and it is considered "blocked".

## Available Operations

You can use the following operations to interact with the game:

1. Move operation: Execute an operator (c1, c2, or c3) at the current node
<move>c1</move>

2. Reset position: Reset position back to the starting node
<reset></reset>

3. Query current position: Ask for the current node number
<where></where>

4. Query degree: Ask for the number of children of the current node
<degree></degree>

5. Query children: Ask for the ordered list of children of a specified node
<children>6</children>

6. Check target: Ask if the current node is the target node
<is_target></is_target>

## Submit Final Answer

When you have inferred the wiring schema and found the path from the starting node to the target node, you must submit all three items at once:

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

Answer format explanation:
- DECLARE: The wiring schema (one of S_A, S_B, S_C, or S_D)
- PATH: Node sequence connected by "-" (e.g., 1-2-6-12)
- LABELS: Operator sequence connected by "-", corresponding one-to-one with edges in PATH (e.g., c2-c1-c3)

Validation rules:
1. DECLARE must be one of the four schemas
2. Using the schema specified by DECLARE, map LABELS to child index sequence, which must match the parent-child relationships between adjacent nodes in PATH
3. PATH must start from the starting node and arrive exactly at the target node
4. Each move must not be out of bounds or blocked

Your goal is to identify the wiring schema with as few operations as possible and construct the correct path and operation sequence.
"""

    # ================= 场景1：交通 =================
    contextualized_rule_zh_1 = """\
我们来操作“智能交通路网寻轨”系统。

给定一个固定的树形交通路网T，节点代表路口（以整数编号），每个路口的分支道路有从左到右的固定顺序。路网结构如下：

{tree_structure}

起点路口：{start_node}（首发站）
目标路口：{target_node}

系统中有三种调度指令（控制信号）：c1、c2、c3。每次你在当前路口下达其中一个指令，系统会尝试选择该路口的第k条分支并引导车辆驶入下一路口。k由一个未知但固定的底层调度协议S决定。

调度协议S只可能是以下四种之一（在整个调度过程中保持不变）：
- S_A: c1驶入第1分支, c2驶入第1分支, c3驶入第2分支
- S_B: c1驶入第1分支, c2驶入第2分支, c3驶入第1分支
- S_C: c1驶入第2分支, c2驶入第1分支, c3驶入第2分支
- S_D: c1驶入第2分支, c2驶入第2分支, c3驶入第1分支

注意：如果当前路口的分支道路数量小于所选的分支序号（越界），车辆将不会移动，视为"受阻"。

## 可用操作

你可以使用以下操作与系统交互：

1. 移动操作：在当前路口执行调度指令（c1、c2或c3）
<move>c1</move>

2. 重置位置：将车辆重置回起点路口
<reset></reset>

3. 查询当前位置：询问当前所在的路口编号
<where></where>

4. 查询度数：询问当前路口的分支道路数量
<degree></degree>

5. 查询子节点：询问指定路口的有序分支路口列表
<children>6</children>

6. 检查目标：询问当前路口是否为目标路口
<is_target></is_target>

## 提交最终答案

当你推断出调度协议并找到从起点路口到目标路口的正确行驶路径后，必须一次性提交三项内容：

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

答案格式说明：
- DECLARE：调度协议（S_A、S_B、S_C或S_D之一）
- PATH：路口序列，用"-"连接（例如：1-2-6-12）
- LABELS：指令序列，用"-"连接，与PATH中的路段一一对应（例如：c2-c1-c3）

校验规则：
1. DECLARE必须是四种协议之一
2. 使用DECLARE指定的协议，将LABELS映射为分支序号序列，必须与PATH中相邻路口之间的连通关系匹配
3. PATH必须从起点路口开始，准确到达目标路口
4. 每一步移动都不能越界或受阻

你的目标是用尽可能少的指令操作识别出正确的调度协议，并构造畅通无阻的路径和指令序列。
"""

    contextualized_rule_en_1 = """\
[Traffic Control Scenario]
Let's operate the "Smart Traffic Routing" system. The setup is as follows:

Given a fixed ordered rooted tree T representing the traffic network, where nodes are intersections (numbered with integers) and each intersection's branching roads have a fixed left-to-right order. The network structure is:

{tree_structure}

Starting intersection: {start_node} (Start)
Target intersection: {target_node}

There are three dispatch commands (control signals): c1, c2, c3. Each time you execute a command at the current intersection, the system attempts to select the k-th branching road of that intersection and guide the vehicle into it. The value k is determined by an unknown but fixed underlying dispatch protocol S.

Protocol S can only be one of the following four (remains constant throughout):
- S_A: c1→1st branch, c2→1st branch, c3→2nd branch
- S_B: c1→1st branch, c2→2nd branch, c3→1st branch
- S_C: c1→2nd branch, c2→1st branch, c3→2nd branch
- S_D: c1→2nd branch, c2→2nd branch, c3→1st branch

Note: If the current intersection has fewer branching roads than the selected branch index (out of bounds), no movement occurs and it is considered "blocked".

## Available Operations

You can use the following operations to interact with the system:

1. Move operation: Execute a dispatch command (c1, c2, or c3) at the current intersection
<move>c1</move>

2. Reset position: Reset vehicle back to the starting intersection
<reset></reset>

3. Query current position: Ask for the current intersection number
<where></where>

4. Query degree: Ask for the number of branching roads of the current intersection
<degree></degree>

5. Query children: Ask for the ordered list of branch intersections of a specified intersection
<children>6</children>

6. Check target: Ask if the current intersection is the target intersection
<is_target></is_target>

## Submit Final Answer

When you have inferred the dispatch protocol and found the path from the starting intersection to the target intersection, you must submit all three items at once:

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

Answer format explanation:
- DECLARE: The dispatch protocol (one of S_A, S_B, S_C, or S_D)
- PATH: Intersection sequence connected by "-" (e.g., 1-2-6-12)
- LABELS: Command sequence connected by "-", corresponding one-to-one with road segments in PATH (e.g., c2-c1-c3)

Validation rules:
1. DECLARE must be one of the four protocols
2. Using the protocol specified by DECLARE, map LABELS to branch index sequence, which must match the connectivity relationships between adjacent intersections in PATH
3. PATH must start from the starting intersection and arrive exactly at the target intersection
4. Each move must not be out of bounds or blocked

Your goal is to identify the dispatch protocol with as few operations as possible and construct the correct path and command sequence.
"""

    # ================= 场景2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎使用“临床路径反应推理”系统。

给定一棵固定的有序临床阶段树T，节点代表临床状态（以整数编号），每个状态的后续发展阶段有从左到右的固定顺序。路径结构如下：

{tree_structure}

初始状态：{start_node}（根节点）
康复状态：{target_node}

系统中有三种干预方案（治疗手段）：c1、c2、c3。每次你在当前临床状态执行其中一种干预方案，机体就会尝试选择该状态的第k个后续阶段并转化。k由患者未知但固定的底层机体反应分型S决定。

机体反应分型S只可能是以下四种之一（在整个治疗过程中保持不变）：
- S_A: 方案c1导向第1阶段, c2导向第1阶段, c3导向第2阶段
- S_B: 方案c1导向第1阶段, c2导向第2阶段, c3导向第1阶段
- S_C: 方案c1导向第2阶段, c2导向第1阶段, c3导向第2阶段
- S_D: 方案c1导向第2阶段, c2导向第2阶段, c3导向第1阶段

注意：如果当前状态的后续可能阶段数量小于所选的阶段序号（越界），则机体状态不会发生转化，视为"受阻"（维持原状）。

## 可用操作

你可以使用以下操作与系统交互：

1. 移动操作：在当前状态执行干预方案（c1、c2或c3）
<move>c1</move>

2. 重置位置：将机体状态洗脱回初始状态
<reset></reset>

3. 查询当前位置：询问当前的临床状态编号
<where></where>

4. 查询度数：询问当前状态的后续发展阶段数量
<degree></degree>

5. 查询子节点：询问指定状态的有序后续阶段列表
<children>6</children>

6. 检查目标：询问当前是否已达到康复状态
<is_target></is_target>

## 提交最终答案

当你推断出机体反应分型并找到从初始状态到康复状态的治疗路径后，必须一次性提交三项内容：

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

答案格式说明：
- DECLARE：机体反应分型（S_A、S_B、S_C或S_D之一）
- PATH：临床状态序列，用"-"连接（例如：1-2-6-12）
- LABELS：干预方案序列，用"-"连接，与PATH中的阶段演进一一对应（例如：c2-c1-c3）

校验规则：
1. DECLARE必须是四种分型之一
2. 使用DECLARE指定的分型，将LABELS映射为阶段序号序列，必须与PATH中相邻状态之间的演进关系匹配
3. PATH必须从初始状态开始，准确达到康复状态
4. 每一步干预都不能越界或受阻

你的目标是用尽可能少的干预操作识别患者的机体反应分型，并制定出正确的临床治疗路径及干预序列。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Pathway Response Inference" system. 

Given a fixed ordered rooted clinical stage tree T, where nodes represent clinical states (numbered with integers) and each state's subsequent developmental stages have a fixed left-to-right order. The structure is:

{tree_structure}

Initial state: {start_node} (root)
Recovery state: {target_node}

There are three intervention therapies (treatments): c1, c2, c3. Each time you execute one intervention at the current clinical state, the body attempts to select the k-th subsequent stage of that state and transition to it. The value k is determined by an unknown but fixed underlying Patient Response Profile S.

Profile S can only be one of the following four (remains constant throughout):
- S_A: c1→1st stage, c2→1st stage, c3→2nd stage
- S_B: c1→1st stage, c2→2nd stage, c3→1st stage
- S_C: c1→2nd stage, c2→1st stage, c3→2nd stage
- S_D: c1→2nd stage, c2→2nd stage, c3→1st stage

Note: If the current state has fewer subsequent stages than the selected stage index (out of bounds), no transition occurs and it is considered "blocked" (remains unchanged).

## Available Operations

You can use the following operations to interact with the system:

1. Move operation: Execute an intervention therapy (c1, c2, or c3) at the current state
<move>c1</move>

2. Reset position: Wash out and reset the body back to the initial state
<reset></reset>

3. Query current position: Ask for the current clinical state number
<where></where>

4. Query degree: Ask for the number of subsequent stages from the current state
<degree></degree>

5. Query children: Ask for the ordered list of subsequent stages of a specified state
<children>6</children>

6. Check target: Ask if the current state is the recovery state
<is_target></is_target>

## Submit Final Answer

When you have inferred the response profile and found the treatment pathway from the initial state to the recovery state, you must submit all three items at once:

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

Answer format explanation:
- DECLARE: The response profile (one of S_A, S_B, S_C, or S_D)
- PATH: Clinical state sequence connected by "-" (e.g., 1-2-6-12)
- LABELS: Therapy sequence connected by "-", corresponding one-to-one with transitions in PATH (e.g., c2-c1-c3)

Validation rules:
1. DECLARE must be one of the four profiles
2. Using the profile specified by DECLARE, map LABELS to stage index sequence, which must match the transitional relationships between adjacent states in PATH
3. PATH must start from the initial state and arrive exactly at the recovery state
4. Each intervention must not be out of bounds or blocked

Your goal is to identify the patient response profile with as few interventions as possible and construct the correct clinical pathway and treatment sequence.
"""

    # ================= 场景3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎使用“自适应学习路径推理”系统。

给定一棵固定的有序知识图谱树T，节点代表知识模块（以整数编号），每个模块的进阶子模块有从左到右的固定顺序。图谱结构如下：

{tree_structure}

基础模块：{start_node}（起点节点）
目标模块：{target_node}（掌握目标）

系统中有三种教学策略：c1、c2、c3。每次你在当前知识模块应用其中一种策略，系统会尝试引导学生进入该模块的第k个进阶子模块。k由学生未知但固定的认知吸收模式S决定。

认知吸收模式S只可能是以下四种之一（在整个学习周期中保持不变）：
- S_A: 策略c1引导至第1模块, c2引导至第1模块, c3引导至第2模块
- S_B: 策略c1引导至第1模块, c2引导至第2模块, c3引导至第1模块
- S_C: 策略c1引导至第2模块, c2引导至第1模块, c3引导至第2模块
- S_D: 策略c1引导至第2模块, c2引导至第2模块, c3引导至第1模块

注意：如果当前模块的进阶子模块数量小于所选的模块序号（越界），则学生无法推进学习，视为"受阻"。

## 可用操作

你可以使用以下操作与系统交互：

1. 移动操作：在当前知识模块应用教学策略（c1、c2或c3）
<move>c1</move>

2. 重置位置：将学习进度重置回基础模块
<reset></reset>

3. 查询当前位置：询问当前所处的知识模块编号
<where></where>

4. 查询度数：询问当前模块的进阶子模块数量
<degree></degree>

5. 查询子节点：询问指定模块的有序进阶子模块列表
<children>6</children>

6. 检查目标：询问当前模块是否为最终目标模块
<is_target></is_target>

## 提交最终答案

当你推断出认知吸收模式并找到从基础模块到目标模块的最佳学习路径后，必须一次性提交三项内容：

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

答案格式说明：
- DECLARE：认知吸收模式（S_A、S_B、S_C或S_D之一）
- PATH：知识模块序列，用"-"连接（例如：1-2-6-12）
- LABELS：教学策略序列，用"-"连接，与PATH中的知识递进一一对应（例如：c2-c1-c3）

校验规则：
1. DECLARE必须是四种模式之一
2. 使用DECLARE指定的模式，将LABELS映射为模块序号序列，必须与PATH中相邻模块之间的前置/后置关系匹配
3. PATH必须从基础模块开始，准确到达目标模块
4. 每一步学习引导都不能越界或受阻

你的目标是用尽可能少的探测操作识别学生的认知模式，并为他规划出正确的学习路径及教学策略序列。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Inference" system.

Given a fixed ordered knowledge graph tree T, where nodes represent knowledge modules (numbered with integers) and each module's advanced sub-modules have a fixed left-to-right order. The structure is:

{tree_structure}

Foundation module: {start_node} (Starting point)
Mastery target: {target_node} (Target module)

There are three teaching strategies: c1, c2, c3. Each time you apply one strategy at the current knowledge module, the system attempts to guide the student to the k-th advanced sub-module of that module. The value k is determined by the student's unknown but fixed Cognitive Absorption Pattern S.

Pattern S can only be one of the following four (remains constant throughout):
- S_A: c1→1st module, c2→1st module, c3→2nd module
- S_B: c1→1st module, c2→2nd module, c3→1st module
- S_C: c1→2nd module, c2→1st module, c3→2nd module
- S_D: c1→2nd module, c2→2nd module, c3→1st module

Note: If the current module has fewer advanced sub-modules than the selected index (out of bounds), the student cannot progress and it is considered "blocked".

## Available Operations

You can use the following operations to interact with the system:

1. Move operation: Apply a teaching strategy (c1, c2, or c3) at the current module
<move>c1</move>

2. Reset position: Reset learning progress back to the foundation module
<reset></reset>

3. Query current position: Ask for the current knowledge module number
<where></where>

4. Query degree: Ask for the number of advanced sub-modules from the current module
<degree></degree>

5. Query children: Ask for the ordered list of advanced sub-modules of a specified module
<children>6</children>

6. Check target: Ask if the current module is the mastery target
<is_target></is_target>

## Submit Final Answer

When you have inferred the cognitive pattern and found the learning path from the foundation module to the mastery target, you must submit all three items at once:

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

Answer format explanation:
- DECLARE: The cognitive pattern (one of S_A, S_B, S_C, or S_D)
- PATH: Knowledge module sequence connected by "-" (e.g., 1-2-6-12)
- LABELS: Teaching strategy sequence connected by "-", corresponding one-to-one with progression in PATH (e.g., c2-c1-c3)

Validation rules:
1. DECLARE must be one of the four patterns
2. Using the pattern specified by DECLARE, map LABELS to module index sequence, which must match the prerequisite/advanced relationships between adjacent modules in PATH
3. PATH must start from the foundation module and arrive exactly at the mastery target
4. Each teaching guidance must not be out of bounds or blocked

Your goal is to identify the cognitive absorption pattern with as few operations as possible and construct the correct learning path and strategy sequence.
"""

    # ================= 场景4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎使用“自动化流水线分拣”系统。

给定一棵固定的生产流转树T，节点代表工作站（以整数编号），每个工作站的下游分拣口有从左到右的固定顺序。流水线结构如下：

{tree_structure}

原料站：{start_node}（起始节点）
成品站：{target_node}（目标节点）

系统中有三种控制流（指令）：c1、c2、c3。每次你在当前工作站下发其中一个控制流指令，传送带会尝试将物料推入该工作站的第k个下游分拣口并送达下一站。k由一个未知但固定的底层路由分拣逻辑S决定。

分拣逻辑S只可能是以下四种之一（在整个加工批次中保持不变）：
- S_A: 指令c1推向第1口, c2推向第1口, c3推向第2口
- S_B: 指令c1推向第1口, c2推向第2口, c3推向第1口
- S_C: 指令c1推向第2口, c2推向第1口, c3推向第2口
- S_D: 指令c1推向第2口, c2推向第2口, c3推向第1口

注意：如果当前工作站的下游接口数量小于所选的分拣口序号（越界），则物料无法流转，视为"受阻"。

## 可用操作

你可以使用以下操作与系统交互：

1. 移动操作：在当前工作站下发控制流指令（c1、c2或c3）
<move>c1</move>

2. 重置位置：将物料退回至原料站重新投产
<reset></reset>

3. 查询当前位置：询问当前所在的工作站编号
<where></where>

4. 查询度数：询问当前工作站的下游分拣口数量
<degree></degree>

5. 查询子节点：询问指定工作站的有序下游站点列表
<children>6</children>

6. 检查目标：询问当前工作站是否为成品站
<is_target></is_target>

## 提交最终答案

当你推断出路由分拣逻辑并打通从原料站到成品站的生产流转路径后，必须一次性提交三项内容：

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

答案格式说明：
- DECLARE：分拣逻辑（S_A、S_B、S_C或S_D之一）
- PATH：工作站序列，用"-"连接（例如：1-2-6-12）
- LABELS：控制流指令序列，用"-"连接，与PATH中的流转段一一对应（例如：c2-c1-c3）

校验规则：
1. DECLARE必须是四种逻辑之一
2. 使用DECLARE指定的逻辑，将LABELS映射为分拣口序号序列，必须与PATH中相邻工作站之间的上下游关系匹配
3. PATH必须从原料站开始，准确流转到成品站
4. 每次物料推送都不能越界或受阻

你的目标是用尽可能少的指令操作识别出正确的路由逻辑，并构造畅通的高效流水线路径及控制流序列。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Automated Assembly Routing" system.

Given a fixed production flow tree T, where nodes represent workstations (numbered with integers) and each workstation's downstream sorting ports have a fixed left-to-right order. The assembly structure is:

{tree_structure}

Raw material station: {start_node} (Start)
Finished product station: {target_node} (Target)

There are three control streams (commands): c1, c2, c3. Each time you issue one control command at the current workstation, the conveyor attempts to push the material into the k-th downstream port of that station. The value k is determined by an unknown but fixed underlying Routing Logic S.

Logic S can only be one of the following four (remains constant throughout the batch):
- S_A: c1→1st port, c2→1st port, c3→2nd port
- S_B: c1→1st port, c2→2nd port, c3→1st port
- S_C: c1→2nd port, c2→1st port, c3→2nd port
- S_D: c1→2nd port, c2→2nd port, c3→1st port

Note: If the current workstation has fewer downstream ports than the selected port index (out of bounds), material flow stops and it is considered "blocked".

## Available Operations

You can use the following operations to interact with the system:

1. Move operation: Issue a control stream command (c1, c2, or c3) at the current workstation
<move>c1</move>

2. Reset position: Send material back to the raw material station
<reset></reset>

3. Query current position: Ask for the current workstation number
<where></where>

4. Query degree: Ask for the number of downstream ports of the current workstation
<degree></degree>

5. Query children: Ask for the ordered list of downstream stations of a specified workstation
<children>6</children>

6. Check target: Ask if the current workstation is the finished product station
<is_target></is_target>

## Submit Final Answer

When you have inferred the routing logic and cleared the flow path from the raw material station to the finished product station, you must submit all three items at once:

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

Answer format explanation:
- DECLARE: The routing logic (one of S_A, S_B, S_C, or S_D)
- PATH: Workstation sequence connected by "-" (e.g., 1-2-6-12)
- LABELS: Command sequence connected by "-", corresponding one-to-one with transfer segments in PATH (e.g., c2-c1-c3)

Validation rules:
1. DECLARE must be one of the four routing logics
2. Using the logic specified by DECLARE, map LABELS to port index sequence, which must match the upstream-downstream relationships between adjacent stations in PATH
3. PATH must start from the raw material station and arrive exactly at the finished product station
4. Each material push must not be out of bounds or blocked

Your goal is to identify the routing logic with as few operations as possible and construct the correct assembly path and command sequence.
"""

    # ================= 场景5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎使用“司法程序推演”系统。

给定一棵固定的诉讼程序树T，节点代表司法审理阶段（以整数编号），每个阶段的后续法定程序路径有从左到右的固定顺序。程序结构如下：

{tree_structure}

立案阶段：{start_node}（起始节点）
终审阶段：{target_node}（目标节点）

系统中有三种诉讼动议（法律行为）：c1、c2、c3。每次你在当前审理阶段提起其中一项动议，系统会依据动议尝试进入该阶段的第k个后续程序。k由一个未知但固定的裁决演进规则S决定。

裁决演进规则S只可能是以下四种之一（在整个案卷处理中保持不变）：
- S_A: 动议c1导向第1程序, c2导向第1程序, c3导向第2程序
- S_B: 动议c1导向第1程序, c2导向第2程序, c3导向第1程序
- S_C: 动议c1导向第2程序, c2导向第1程序, c3导向第2程序
- S_D: 动议c1导向第2程序, c2导向第2程序, c3导向第1程序

注意：如果当前阶段的后续可用程序数量小于所选的程序序号（越界），则法庭会驳回动议，流程视为"受阻"。

## 可用操作

你可以使用以下操作与系统交互：

1. 移动操作：在当前审理阶段提起诉讼动议（c1、c2或c3）
<move>c1</move>

2. 重置位置：撤诉并重新回到立案阶段
<reset></reset>

3. 查询当前位置：询问当前的审理阶段编号
<where></where>

4. 查询度数：询问当前审理阶段可衍生的后续程序数量
<degree></degree>

5. 查询子节点：询问指定阶段的有序后续程序列表
<children>6</children>

6. 检查目标：询问当前阶段是否为终审阶段
<is_target></is_target>

## 提交最终答案

当你推断出裁决规则并找到从立案阶段到终审阶段的完整诉讼路径后，必须一次性提交三项内容：

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

答案格式说明：
- DECLARE：裁决演进规则（S_A、S_B、S_C或S_D之一）
- PATH：审理阶段序列，用"-"连接（例如：1-2-6-12）
- LABELS：诉讼动议序列，用"-"连接，与PATH中的程序推进一一对应（例如：c2-c1-c3）

校验规则：
1. DECLARE必须是四种裁决规则之一
2. 使用DECLARE指定的规则，将LABELS映射为程序序号序列，必须与PATH中相邻阶段之间的法定继承关系匹配
3. PATH必须从立案阶段开始，准确到达终审阶段
4. 每一步动议提起都不能越界或被驳回（受阻）

你的目标是用尽可能少的动议探测识别底层裁决规则，并规划出能够顺利结案的诉讼路径及动议序列。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Procedure Deduction" system.

Given a fixed legal procedure tree T, where nodes represent litigation stages (numbered with integers) and each stage's subsequent legal procedures have a fixed left-to-right order. The structure is:

{tree_structure}

Filing stage: {start_node} (Starting node)
Final verdict: {target_node} (Target node)

There are three legal motions (actions): c1, c2, c3. Each time you file one motion at the current litigation stage, the system attempts to enter the k-th subsequent procedure of that stage. The value k is determined by an unknown but fixed Adjudication Rule Set S.

Rule Set S can only be one of the following four (remains constant throughout the case):
- S_A: Motion c1→1st procedure, c2→1st procedure, c3→2nd procedure
- S_B: Motion c1→1st procedure, c2→2nd procedure, c3→1st procedure
- S_C: Motion c1→2nd procedure, c2→1st procedure, c3→2nd procedure
- S_D: Motion c1→2nd procedure, c2→2nd procedure, c3→1st procedure

Note: If the current stage has fewer available subsequent procedures than the selected index (out of bounds), the court dismisses the motion and the flow is considered "blocked".

## Available Operations

You can use the following operations to interact with the system:

1. Move operation: File a legal motion (c1, c2, or c3) at the current litigation stage
<move>c1</move>

2. Reset position: Withdraw the suit and restart at the filing stage
<reset></reset>

3. Query current position: Ask for the current litigation stage number
<where></where>

4. Query degree: Ask for the number of subsequent procedures from the current stage
<degree></degree>

5. Query children: Ask for the ordered list of subsequent procedures of a specified stage
<children>6</children>

6. Check target: Ask if the current stage is the final verdict
<is_target></is_target>

## Submit Final Answer

When you have inferred the rule set and found the complete litigation path from the filing stage to the final verdict, you must submit all three items at once:

<answer>
DECLARE: S_A
PATH: 1-2-6-12
LABELS: c2-c1-c3
</answer>

Answer format explanation:
- DECLARE: The adjudication rule set (one of S_A, S_B, S_C, or S_D)
- PATH: Litigation stage sequence connected by "-" (e.g., 1-2-6-12)
- LABELS: Legal motion sequence connected by "-", corresponding one-to-one with procedure advancements in PATH (e.g., c2-c1-c3)

Validation rules:
1. DECLARE must be one of the four rule sets
2. Using the rules specified by DECLARE, map LABELS to procedure index sequence, which must match the legal successive relationships between adjacent stages in PATH
3. PATH must start from the filing stage and arrive exactly at the final verdict
4. Each motion filed must not be out of bounds or dismissed (blocked)

Your goal is to identify the adjudication rules with as few motions as possible and construct a smooth litigation path and motion sequence.
"""

    tags = ["answer", "move", "reset", "where", "degree", "children", "is_target"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "tree": {1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [], 5: [], 6: [], 7: []},
                "start": 1, "target": 4, "schema": "S_A",
                "correct_path": [1, 2, 4], "correct_labels": ["c1", "c1"]
            },
            2: {
                "tree": {1: [2, 3, 4], 2: [5, 6], 3: [7, 8], 4: [9, 10], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []},
                "start": 1, "target": 8, "schema": "S_B",
                "correct_path": [1, 3, 8], "correct_labels": ["c2", "c2"]
            },
            3: {
                "tree": {1: [2, 3, 4], 2: [5, 6], 3: [7, 8, 9], 4: [10], 5: [], 6: [11, 12], 7: [], 8: [], 9: [13], 10: [], 11: [], 12: [], 13: []},
                "start": 1, "target": 12, "schema": "S_C",
                "correct_path": [1, 2, 6, 12], "correct_labels": ["c2", "c3", "c3"]
            },
            4: {
                "tree": {1: [2, 3], 2: [4, 5, 6], 3: [7, 8], 4: [9], 5: [10, 11], 6: [12, 13], 7: [14], 8: [15, 16], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 15: [], 16: []},
                "start": 1, "target": 16, "schema": "S_D",
                "correct_path": [1, 3, 8, 16], "correct_labels": ["c1", "c1", "c1"]
            },
            5: {
                "tree": {1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [8, 9], 5: [10, 11], 
                         6: [12, 13], 7: [14, 15], 8: [], 9: [], 10: [], 11: [], 
                         12: [], 13: [], 14: [], 15: []},
                "start": 1, "target": 15, "schema": "S_C",
                "correct_path": [1, 3, 7, 15], "correct_labels": ["c1", "c1", "c1"]
            }
        },
        "en": {
            1: {
                "tree": {1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [], 5: [], 6: [], 7: []},
                "start": 1, "target": 4, "schema": "S_A",
                "correct_path": [1, 2, 4], "correct_labels": ["c1", "c1"]
            },
            2: {
                "tree": {1: [2, 3, 4], 2: [5, 6], 3: [7, 8], 4: [9, 10], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []},
                "start": 1, "target": 8, "schema": "S_B",
                "correct_path": [1, 3, 8], "correct_labels": ["c2", "c2"]
            },
            3: {
                "tree": {1: [2, 3, 4], 2: [5, 6], 3: [7, 8, 9], 4: [10], 5: [], 6: [11, 12], 7: [], 8: [], 9: [13], 10: [], 11: [], 12: [], 13: []},
                "start": 1, "target": 12, "schema": "S_C",
                "correct_path": [1, 2, 6, 12], "correct_labels": ["c2", "c3", "c3"]
            },
            4: {
                "tree": {1: [2, 3], 2: [4, 5, 6], 3: [7, 8], 4: [9], 5: [10, 11], 6: [12, 13], 7: [14], 8: [15, 16], 9: [], 10: [], 11: [], 12: [], 13: [], 14: [], 15: [], 16: []},
                "start": 1, "target": 16, "schema": "S_D",
                "correct_path": [1, 3, 8, 16], "correct_labels": ["c1", "c1", "c1"]
            },
            5: {
                "tree": {1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [8, 9], 5: [10, 11], 
                         6: [12, 13], 7: [14, 15], 8: [], 9: [], 10: [], 11: [], 
                         12: [], 13: [], 14: [], 15: []},
                "start": 1, "target": 15, "schema": "S_C",
                "correct_path": [1, 3, 7, 15], "correct_labels": ["c1", "c1", "c1"]
            }
        }
    }

    SCHEMA_MAP = {
        "S_A": {"c1": 1, "c2": 1, "c3": 2},
        "S_B": {"c1": 1, "c2": 2, "c3": 1},
        "S_C": {"c1": 2, "c2": 1, "c3": 2},
        "S_D": {"c1": 2, "c2": 2, "c3": 1}
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：设置树结构、起始节点、目标节点、接线方案等"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 树结构
        self.tree = cfg["tree"]
        self.start_node = cfg["start"]
        self.target_node = cfg["target"]
        self.schema = cfg["schema"]
        self.correct_path = cfg["correct_path"]
        self.correct_labels = cfg["correct_labels"]
        
        # 当前位置
        self.current_node = self.start_node
        
        # 格式化树结构显示
        tree_lines = []
        for node in sorted(self.tree.keys()):
            children = self.tree[node]
            if children:
                tree_lines.append(f"  节点 {node}: [{', '.join(map(str, children))}]" if lang == "zh" else f"  Node {node}: [{', '.join(map(str, children))}]")
            else:
                tree_lines.append(f"  节点 {node}: []" if lang == "zh" else f"  Node {node}: []")
        
        self._game_info["tree_structure"] = "\n".join(tree_lines)
        self._game_info["start_node"] = self.start_node
        self._game_info["target_node"] = self.target_node

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            raw_ans = parsed_info["answer"]
            
            # 解析答案的三个部分
            declare_match = re.search(r'DECLARE:\s*(S_[A-D])', raw_ans, re.IGNORECASE)
            path_match = re.search(r'PATH:\s*([\d\-]+)', raw_ans, re.IGNORECASE)
            labels_match = re.search(r'LABELS:\s*([\w\-]+)', raw_ans, re.IGNORECASE)
            
            if not (declare_match and path_match and labels_match):
                return False
            
            declared_schema = declare_match.group(1).upper()
            path_str = path_match.group(1)
            labels_str = labels_match.group(1)
            
            # 1. 检查DECLARE是否有效
            if declared_schema not in self.SCHEMA_MAP:
                return False
            
            # 2. 解析PATH和LABELS
            try:
                path = [int(x) for x in path_str.split("-")]
                labels = labels_str.split("-")
            except:
                return False
            
            # 3. 检查PATH长度和LABELS长度是否匹配
            if len(path) != len(labels) + 1:
                return False
            
            # 4. 检查PATH是否从起始节点开始
            if path[0] != self.start_node:
                return False
            
            # 5. 检查PATH是否到达目标节点
            if path[-1] != self.target_node:
                return False
            
            # 6. 验证路径：使用declared_schema验证每一步移动
            schema_mapping = self.SCHEMA_MAP[declared_schema]
            
            for i in range(len(labels)):
                current = path[i]
                next_node = path[i + 1]
                operator = labels[i]
                
                # 检查operator是否有效
                if operator not in schema_mapping:
                    return False
                
                # 获取应该选择的子节点索引
                child_index = schema_mapping[operator]  # 1-based
                
                # 检查当前节点是否存在于树中
                if current not in self.tree:
                    return False
                
                children = self.tree[current]
                
                # 检查是否越界
                if child_index > len(children):
                    return False
                
                # 检查下一个节点是否正确
                expected_next = children[child_index - 1]  # 转换为0-based索引
                if next_node != expected_next:
                    return False
            
            # 所有检查通过
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑，重命名为 _cf_core_produce 以供调用"""
        lang = self.config.language
        
        # 移动操作
        if "move" in parsed_info:
            operator = parsed_info["move"].strip()
            if operator not in ["c1", "c2", "c3"]:
                return "错误：无效的操作符。" if lang == "zh" else "Error: Invalid operator."
            
            # 获取当前接线方案下该操作符对应的子节点索引
            child_index = self.SCHEMA_MAP[self.schema][operator]  # 1-based
            
            # 检查当前节点的子节点
            children = self.tree[self.current_node]
            
            # 检查是否越界
            if child_index > len(children):
                return f"受阻（停留在节点 {self.current_node}）" if lang == "zh" else f"Blocked (stay at {self.current_node})"
            
            # 移动到目标子节点
            self.current_node = children[child_index - 1]  # 转换为0-based索引
            return f"到达节点 {self.current_node}" if lang == "zh" else f"Arrived {self.current_node}"
        
        # 重置操作
        elif "reset" in parsed_info:
            self.current_node = self.start_node
            return f"到达节点 {self.start_node}" if lang == "zh" else f"Arrived {self.start_node}"
        
        # 查询当前位置
        elif "where" in parsed_info:
            return f"当前节点：{self.current_node}" if lang == "zh" else f"Current {self.current_node}"
        
        # 查询度数
        elif "degree" in parsed_info:
            degree = len(self.tree[self.current_node])
            return f"度数：{degree}" if lang == "zh" else f"Degree {degree}"
        
        # 查询子节点
        elif "children" in parsed_info:
            try:
                node = int(parsed_info["children"].strip())
                if node not in self.tree:
                    return "错误：节点不存在。" if lang == "zh" else "Error: Node does not exist."
                children = self.tree[node]
                children_str = ", ".join(map(str, children)) if children else ""
                return f"节点 {node} 的子节点：[{children_str}]" if lang == "zh" else f"ChildrenOf {node}: [{children_str}]"
            except:
                return "错误：无效的节点编号。" if lang == "zh" else "Error: Invalid node number."
        
        # 检查是否为目标
        elif "is_target" in parsed_info:
            if self.current_node == self.target_node:
                return "是" if lang == "zh" else "Yes"
            else:
                return "否" if lang == "zh" else "No"
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯整数字符串（如 "0", "1", "2"）：返回 str(int(correct) + 1)
        if re.match(r'^\d+$', correct):
            return str(int(correct) + 1)
        
        # 否则按以下规则替换关键词（区分语言）：
        if correct == "是": return "否"
        if correct == "否": return "是"
        if correct == "Yes": return "No"
        if correct == "No": return "Yes"

        # 如果响应中包含数字，则将提取到的第一个数字+1制造错误答案
        if match := re.search(r'\d+', correct):
            return correct.replace(match.group(), str(int(match.group()) + 1), 1)

        # 若都不匹配：在字符串末尾追加 "_WRONG"
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        results = []
        original_node = self.current_node
        
        # 1. 移动操作
        for op in ["c1", "c2", "c3"]:
            query_str = f"<move>{op}</move>"
            parsed = {"move": op}
            self.current_node = original_node
            ans = self._cf_core_produce(parsed)
            results.append({"query": query_str, "answer": ans})

        # 2. 重置操作
        query_str = "<reset></reset>"
        parsed = {"reset": ""}
        self.current_node = original_node
        ans = self._cf_core_produce(parsed)
        results.append({"query": query_str, "answer": ans})

        # 3. 查询当前位置
        query_str = "<where></where>"
        parsed = {"where": ""}
        self.current_node = original_node
        ans = self._cf_core_produce(parsed)
        results.append({"query": query_str, "answer": ans})

        # 4. 查询度数
        query_str = "<degree></degree>"
        parsed = {"degree": ""}
        self.current_node = original_node
        ans = self._cf_core_produce(parsed)
        results.append({"query": query_str, "answer": ans})

        # 5. 查询子节点（遍历所有节点）
        for node in sorted(self.tree.keys()):
            query_str = f"<children>{node}</children>"
            parsed = {"children": str(node)}
            self.current_node = original_node
            ans = self._cf_core_produce(parsed)
            results.append({"query": query_str, "answer": ans})

        # 6. 检查目标
        query_str = "<is_target></is_target>"
        parsed = {"is_target": ""}
        self.current_node = original_node
        ans = self._cf_core_produce(parsed)
        results.append({"query": query_str, "answer": ans})

        # 恢复初始状态
        self.current_node = original_node
        
        return results