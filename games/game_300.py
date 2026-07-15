from .base import Game
import re

class SymbolTreeNavigationGame(Game):

    game_rule_zh = """\
我们来玩一个"符号树导航"推理游戏，规则如下：

给定一棵有根有序树 T，根节点为 r。每个节点至多有 3 个有序子槽位，槽位编号为 1、2、3。

**蓝图结构：**
{blueprint}

**目标门位地址：** {target_address}

**符号集合：** 符号A、符号B、符号C

**隐藏置换规则：**
系统已秘密选择以下六种置换方案之一，定义了符号到槽位的映射：
- 方案A：符号A→1，符号B→2，符号C→3
- 方案B：符号A→1，符号B→3，符号C→2
- 方案C：符号A→2，符号B→1，符号C→3
- 方案D：符号A→2，符号B→3，符号C→1
- 方案E：符号A→3，符号B→1，符号C→2
- 方案F：符号A→3，符号B→2，符号C→1

你需要通过交互推断出真实的置换方案，并利用该方案将目标门位地址翻译为符号序列，成功导航到目标节点。

**胜利条件（必须同时满足）：**
1. 当前节点到达目标节点
2. 正确声明真实的置换方案

游戏开始时，你位于根节点 {root}。你可以进行以下操作（每次只能一个操作）：

1. **移动操作**：尝试沿指定符号对应的槽位移动
   - 格式：<walk>符号A</walk> 或 <walk>符号B</walk> 或 <walk>符号C</walk>
   - 若对应槽位存在子节点，则移动成功；否则撞墙，停留原处

2. **位置查询**：查询当前所在节点ID
   - 格式：<query_position></query_position>

3. **目标检查**：检查当前节点是否为目标节点
   - 格式：<query_target></query_target>

4. **回到根节点**：将当前位置重置为根节点
   - 格式：<reset></reset>

5. **批量移动**：从根节点开始按符号序列依次移动（遇撞墙即中止）
   - 格式：<walk_sequence>符号A,符号B,符号C</walk_sequence>
   - 注意：符号之间用逗号分隔，无空格

6. **声明置换**：声明你认为的真实置换方案
   - 格式：<declare>方案A</declare>（方案可为 A/B/C/D/E/F）

当你准备好提交最终答案时，必须同时提供：
1. 到达目标的符号序列（从根节点开始）
2. 置换方案声明

格式：
<answer>sequence=符号A,符号B,符号C, permutation=方案A</answer>

注意：符号之间用逗号分隔，无空格。

- 步数上限为 {max_steps} 步
- 每次移动、批量移动中的每步、查询等都计为 1 步
- 利用蓝图的已知结构和观测结果推断隐藏置换
- 答案错误或超过步数上限将导致游戏失败
"""

    game_rule_en = """\
Let's play a "Symbol Tree Navigation" deduction game with the following rules:

Given a rooted ordered tree T with root node r. Each node has at most 3 ordered child slots, numbered 1, 2, 3.

**Blueprint Structure:**
{blueprint}

**Target Gate Address:** {target_address}

**Symbol Set:** SymbolA, SymbolB, SymbolC

**Hidden Permutation Rule:**
The system has secretly chosen one of the following six permutation schemes, defining the mapping from symbols to slots:
- SchemeA: SymbolA→1, SymbolB→2, SymbolC→3
- SchemeB: SymbolA→1, SymbolB→3, SymbolC→2
- SchemeC: SymbolA→2, SymbolB→1, SymbolC→3
- SchemeD: SymbolA→2, SymbolB→3, SymbolC→1
- SchemeE: SymbolA→3, SymbolB→1, SymbolC→2
- SchemeF: SymbolA→3, SymbolB→2, SymbolC→1

You need to infer the true permutation scheme through interaction and use it to translate the target gate address into a symbol sequence, successfully navigating to the target node.

**Victory Conditions (both must be satisfied):**
1. Current node reaches the target node
2. Correctly declare the true permutation scheme

You start at root node {root}. You can perform the following operations (one at a time):

1. **Walk Operation**: Attempt to move along the slot corresponding to the specified symbol
   - Format: <walk>SymbolA</walk> or <walk>SymbolB</walk> or <walk>SymbolC</walk>
   - If the corresponding slot has a child node, move succeeds; otherwise hit wall and stay

2. **Position Query**: Query current node ID
   - Format: <query_position></query_position>

3. **Target Check**: Check if current node is the target node
   - Format: <query_target></query_target>

4. **Reset to Root**: Reset current position to root node
   - Format: <reset></reset>

5. **Batch Walk**: Walk from root following symbol sequence (stops on hitting wall)
   - Format: <walk_sequence>SymbolA,SymbolB,SymbolC</walk_sequence>
   - Note: Symbols separated by comma, no spaces

6. **Declare Permutation**: Declare what you believe is the true permutation scheme
   - Format: <declare>SchemeA</declare> (scheme can be A/B/C/D/E/F)

When ready to submit your final answer, you must provide both:
1. Symbol sequence to reach target (from root)
2. Permutation scheme declaration

Format:
<answer>sequence=SymbolA,SymbolB,SymbolC, permutation=SchemeA</answer>

Note: Symbols separated by comma, no spaces.

- Step limit is {max_steps} steps
- Each walk, each step in batch walk, and each query counts as 1 step
- Use the known blueprint structure and observations to infer the hidden permutation
- Wrong answer or exceeding step limit leads to game failure
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市地下交通网络智能调度系统”。系统正面临线路映射配置丢失的突发状况。
我们需要进行紧急的“符号树导航”调度推演，规则如下：

给定一棵代表地下交通网络的有根有序树 T，根枢纽为 r。每个交通枢纽（节点）至多有 3 个单向出站隧道（槽位），编号为 1、2、3。

**网络蓝图：**
{blueprint}

**目标区域地址：** {target_address}

**可用调度指令（符号）：** 符号A、符号B、符号C

**隐藏映射规则：**
系统中央控制逻辑秘密采用了以下六种底层调度方案之一，定义了调度指令（符号）到出站隧道的路由配置：
- 方案A：符号A→1，符号B→2，符号C→3
- 方案B：符号A→1，符号B→3，符号C→2
- 方案C：符号A→2，符号B→1，符号C→3
- 方案D：符号A→2，符号B→3，符号C→1
- 方案E：符号A→3，符号B→1，符号C→2
- 方案F：符号A→3，符号B→2，符号C→1

你需要通过试探性交互，推测出现行的真实调度方案，并利用该方案将目标区域地址翻译为指令序列，成功将测试车辆导航到目标枢纽。

**胜利条件（必须同时满足）：**
1. 测试车辆到达目标枢纽
2. 正确声明真实的路由调度方案

推演开始时，测试车辆位于根枢纽 {root}。你可以进行以下操作（每次只能执行一个）：

1. **单步调度（移动操作）**：发送指令尝试沿对应隧道行进
   - 格式：<walk>符号A</walk> 或 <walk>符号B</walk> 或 <walk>符号C</walk>
   - 若对应隧道连通下一枢纽，则移动成功；否则通道受阻（撞墙），停留原处

2. **定位查询（位置查询）**：查询当前车辆所在枢纽ID
   - 格式：<query_position></query_position>

3. **目标确认（目标检查）**：检查当前枢纽是否为目标区域
   - 格式：<query_target></query_target>

4. **强制返航（回到根节点）**：将测试车辆瞬间重置为根枢纽
   - 格式：<reset></reset>

5. **自动驾驶（批量移动）**：从根枢纽开始按指令序列连续行驶（遇受阻即中止）
   - 格式：<walk_sequence>符号A,符号B,符号C</walk_sequence>
   - 注意：符号之间用逗号分隔，无空格

6. **锁定配置（声明置换）**：声明你推断出的真实映射方案
   - 格式：<declare>方案A</declare>（方案可为 A/B/C/D/E/F）

当你准备好提交最终调度结果时，必须同时提供：
1. 成功到达目标的指令序列（从根枢纽开始）
2. 路由方案声明

格式：
<answer>sequence=符号A,符号B,符号C, permutation=方案A</answer>

注意：符号之间用逗号分隔，无空格。

- 系统操作上限为 {max_steps} 步
- 每次移动、自动驾驶中的每个指令、查询等都计为 1 步
- 利用蓝图已知结构和车辆运行反馈推测隐藏映射配置
- 答案错误或超过步数上限将导致车辆迷失，任务失败
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Underground Traffic Intelligent Routing System." The system is facing an emergency loss of its route mapping configuration.
We need to perform an urgent "Symbol Tree Navigation" simulation with the following rules:

Given a rooted ordered tree T representing the underground traffic network, with root hub r. Each traffic hub (node) has at most 3 one-way outbound tunnels (slots), numbered 1, 2, 3.

**Network Blueprint:**
{blueprint}

**Target Area Address:** {target_address}

**Available Routing Commands (Symbols):** SymbolA, SymbolB, SymbolC

**Hidden Mapping Rule:**
The central control logic has secretly adopted one of the following six underlying routing schemes, defining the mapping from routing commands (symbols) to outbound tunnels:
- SchemeA: SymbolA→1, SymbolB→2, SymbolC→3
- SchemeB: SymbolA→1, SymbolB→3, SymbolC→2
- SchemeC: SymbolA→2, SymbolB→1, SymbolC→3
- SchemeD: SymbolA→2, SymbolB→3, SymbolC→1
- SchemeE: SymbolA→3, SymbolB→1, SymbolC→2
- SchemeF: SymbolA→3, SymbolB→2, SymbolC→1

You need to infer the currently active true routing scheme through trial interactions and use it to translate the target area address into a command sequence, successfully navigating the test vehicle to the target hub.

**Victory Conditions (both must be satisfied):**
1. Test vehicle reaches the target hub
2. Correctly declare the true routing scheme

Simulation starts with the test vehicle at root hub {root}. You can perform the following operations (one at a time):

1. **Single-step Route (Walk Operation)**: Send command to attempt moving along the corresponding tunnel
   - Format: <walk>SymbolA</walk> or <walk>SymbolB</walk> or <walk>SymbolC</walk>
   - If the tunnel connects to the next hub, movement succeeds; otherwise, passage is blocked (hit wall), and vehicle stays.

2. **Location Query (Position Query)**: Query the ID of the hub where the vehicle is currently located
   - Format: <query_position></query_position>

3. **Target Confirmation (Target Check)**: Check if the current hub is the target area
   - Format: <query_target></query_target>

4. **Forced Return (Reset to Root)**: Instantly reset the test vehicle to the root hub
   - Format: <reset></reset>

5. **Autopilot (Batch Walk)**: Drive continuously from the root hub following a command sequence (stops if blocked)
   - Format: <walk_sequence>SymbolA,SymbolB,SymbolC</walk_sequence>
   - Note: Symbols separated by comma, no spaces

6. **Lock Configuration (Declare Permutation)**: Declare the true mapping scheme you have inferred
   - Format: <declare>SchemeA</declare> (scheme can be A/B/C/D/E/F)

When ready to submit your final routing result, you must provide both:
1. Command sequence to successfully reach the target (from root hub)
2. Routing scheme declaration

Format:
<answer>sequence=SymbolA,SymbolB,SymbolC, permutation=SchemeA</answer>

Note: Symbols separated by comma, no spaces.

- System operation limit is {max_steps} steps
- Each movement, each command in autopilot, and each query counts as 1 step
- Use the known blueprint structure and vehicle feedback to infer the hidden mapping configuration
- Wrong answer or exceeding step limit leads to vehicle getting lost and mission failure
"""

    contextualized_rule_zh_2 = """\
欢迎使用“微创手术机器人介入导航系统”。由于患者个体血管发育变异，标准的控制脉冲映射发生了偏移。
我们需要进行“符号树导航”预演来校准操作，规则如下：

给定一棵代表病灶周围血管拓扑的树 T，穿刺入口（根节点）为 r。每个血管分叉点（节点）至多有 3 个分支血管（槽位），解剖学编号为 1、2、3。

**血管造影蓝图：**
{blueprint}

**目标病灶地址：** {target_address}

**可用微控脉冲（符号）：** 符号A、符号B、符号C

**隐藏神经/血管映射变异：**
由于患者体质差异，脉冲刺激（符号）到分支血管转向的映射必定属于以下六种解剖变异方案之一：
- 方案A：符号A→1，符号B→2，符号C→3
- 方案B：符号A→1，符号B→3，符号C→2
- 方案C：符号A→2，符号B→1，符号C→3
- 方案D：符号A→2，符号B→3，符号C→1
- 方案E：符号A→3，符号B→1，符号C→2
- 方案F：符号A→3，符号B→2，符号C→1

你需要通过低剂量试探交互，测定出该患者真实的映射方案，并将目标病灶地址转化为手术脉冲序列，成功将导管送达目标血管。

**胜利条件（必须同时满足）：**
1. 机器人探头安全抵达目标病灶节点
2. 正确声明该患者真实的映射方案

手术预演开始时，探头位于入口 {root}。你可以进行以下操作（每次只能执行一个）：

1. **单步推进（移动操作）**：发送脉冲尝试让探头进入对应分支血管
   - 格式：<walk>符号A</walk> 或 <walk>符号B</walk> 或 <walk>符号C</walk>
   - 若对应分支确实存在，则推进成功；否则探头顶壁（撞墙），留在原分叉点

2. **影像定位（位置查询）**：查询探头当前的解剖节点ID
   - 格式：<query_position></query_position>

3. **病灶确认（目标检查）**：检查当前节点是否为病灶目标
   - 格式：<query_target></query_target>

4. **撤回探头（回到根节点）**：将导管完全抽出回到入口处
   - 格式：<reset></reset>

5. **连续推送（批量移动）**：从入口开始按设定脉冲序列自动推进（遇阻力即中止以防穿孔）
   - 格式：<walk_sequence>符号A,符号B,符号C</walk_sequence>
   - 注意：符号之间用逗号分隔，无空格

6. **确诊变异型（声明置换）**：声明你推断出的患者真实映射方案
   - 格式：<declare>方案A</declare>（方案可为 A/B/C/D/E/F）

准备执行正式介入治疗时，必须同时提供：
1. 抵达病灶的完整脉冲序列（从入口开始）
2. 解剖变异方案声明

格式：
<answer>sequence=符号A,符号B,符号C, permutation=方案A</answer>

注意：符号之间用逗号分隔，无空格。

- 探头试探次数上限为 {max_steps} 步以避免并发症
- 每次推进、连续推送中的每一动、影像查询等都计为 1 步
- 利用术前蓝图和探头反馈推断隐藏的生理映射
- 答案错误或超过步数上限将导致预演失败，手术取消
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Minimally Invasive Surgery Robot Navigation System." Due to the patient's individual vascular developmental variation, the standard control pulse mapping has shifted.
We need to perform a "Symbol Tree Navigation" rehearsal to calibrate operations with the following rules:

Given a tree T representing the vascular topology around the lesion, with the puncture entry (root node) r. Each vascular bifurcation (node) has at most 3 branch vessels (slots), anatomically numbered 1, 2, 3.

**Angiography Blueprint:**
{blueprint}

**Target Lesion Address:** {target_address}

**Available Micro-pulses (Symbols):** SymbolA, SymbolB, SymbolC

**Hidden Anatomical Mapping Variation:**
Due to physical differences, the mapping of pulse stimulation (symbols) to branch vessel steering must belong to one of the following six anatomical variation schemes:
- SchemeA: SymbolA→1, SymbolB→2, SymbolC→3
- SchemeB: SymbolA→1, SymbolB→3, SymbolC→2
- SchemeC: SymbolA→2, SymbolB→1, SymbolC→3
- SchemeD: SymbolA→2, SymbolB→3, SymbolC→1
- SchemeE: SymbolA→3, SymbolB→1, SymbolC→2
- SchemeF: SymbolA→3, SymbolB→2, SymbolC→1

You need to determine the patient's true mapping scheme through low-dose trial interactions and convert the target lesion address into a surgical pulse sequence, successfully delivering the catheter to the target vessel.

**Victory Conditions (both must be satisfied):**
1. Robotic probe safely reaches the target lesion node
2. Correctly declare the patient's true mapping scheme

The surgical rehearsal starts with the probe at entry {root}. You can perform the following operations (one at a time):

1. **Single-step Advance (Walk Operation)**: Send a pulse to attempt steering the probe into the corresponding branch
   - Format: <walk>SymbolA</walk> or <walk>SymbolB</walk> or <walk>SymbolC</walk>
   - If the corresponding branch exists, advance succeeds; otherwise, the probe hits the vascular wall (hit wall) and stays at the current bifurcation.

2. **Imaging Localization (Position Query)**: Query the current anatomical node ID of the probe
   - Format: <query_position></query_position>

3. **Lesion Confirmation (Target Check)**: Check if the current node is the target lesion
   - Format: <query_target></query_target>

4. **Withdraw Probe (Reset to Root)**: Completely retract the catheter back to the entry point
   - Format: <reset></reset>

5. **Continuous Push (Batch Walk)**: Automatically advance from the entry following a set pulse sequence (stops upon resistance to prevent perforation)
   - Format: <walk_sequence>SymbolA,SymbolB,SymbolC</walk_sequence>
   - Note: Symbols separated by comma, no spaces

6. **Diagnose Variant (Declare Permutation)**: Declare the true patient mapping scheme you inferred
   - Format: <declare>SchemeA</declare> (scheme can be A/B/C/D/E/F)

When ready to execute the formal intervention, you must provide both:
1. Complete pulse sequence to reach the lesion (from entry)
2. Anatomical variation scheme declaration

Format:
<answer>sequence=SymbolA,SymbolB,SymbolC, permutation=SchemeA</answer>

Note: Symbols separated by comma, no spaces.

- Probe trial limit is {max_steps} steps to avoid complications
- Each advance, each movement in continuous push, and imaging query counts as 1 step
- Use preoperative blueprint and probe feedback to infer hidden physiological mapping
- Wrong answer or exceeding step limit leads to rehearsal failure and surgery cancellation
"""

    contextualized_rule_zh_3 = """\
欢迎进入“自适应学习图谱路径规划器”。本系统正根据学生的个体认知习惯动态调整知识引导策略。
我们将进行一次“符号树导航”学习规划演练，规则如下：

给定一棵代表学科知识图谱的树 T，基础起点为 r。每个知识点模块（节点）至多引出 3 条进阶学习路径（槽位），难度编号为 1、2、3。

**知识图谱蓝图：**
{blueprint}

**目标考点地址：** {target_address}

**可用学习指令（符号）：** 符号A、符号B、符号C

**隐藏认知倾向映射：**
系统的推荐算法根据学生测评，悄悄锁定了以下六种认知倾向方案之一，定义了学习指令（符号）到进阶路径的触发配置：
- 方案A：符号A→1，符号B→2，符号C→3
- 方案B：符号A→1，符号B→3，符号C→2
- 方案C：符号A→2，符号B→1，符号C→3
- 方案D：符号A→2，符号B→3，符号C→1
- 方案E：符号A→3，符号B→1，符号C→2
- 方案F：符号A→3，符号B→2，符号C→1

你需要通过互动试探，识别出该学生潜藏的真实认知配置方案，并用该方案将目标考点地址翻译为一系列学习指令，成功引导至目标知识点。

**胜利条件（必须同时满足）：**
1. 学习进度到达目标考点模块
2. 正确声明该学生的认知倾向方案

演练开始时，进度处于基础起点 {root}。你可以进行以下操作（每次只能执行一个）：

1. **单次引导（移动操作）**：下发学习指令尝试解锁对应的进阶路径
   - 格式：<walk>符号A</walk> 或 <walk>符号B</walk> 或 <walk>符号C</walk>
   - 若对应难度路径存在后续内容，则解锁成功；否则遇到认知盲区（撞墙），停留在原模块

2. **进度查询（位置查询）**：查询当前正学习的知识点ID
   - 格式：<query_position></query_position>

3. **考点检测（目标检查）**：检测当前知识点是否为最终目标
   - 格式：<query_target></query_target>

4. **基础重修（回到根节点）**：将学习进度清零，退回基础起点
   - 格式：<reset></reset>

5. **连贯推演（批量移动）**：从起点开始按指令序列连续学习（遇盲区即中止）
   - 格式：<walk_sequence>符号A,符号B,符号C</walk_sequence>
   - 注意：符号之间用逗号分隔，无空格

6. **确立认知模型（声明置换）**：声明你推断出的真实认知方案
   - 格式：<declare>方案A</declare>（方案可为 A/B/C/D/E/F）

当教学计划确认无误准备提交时，必须同时提供：
1. 攻克目标考点的完整指令序列（从基础起点开始）
2. 认知方案模型声明

格式：
<answer>sequence=符号A,符号B,符号C, permutation=方案A</answer>

注意：符号之间用逗号分隔，无空格。

- 互动演练步数不可超过 {max_steps} 步，避免学生疲劳
- 每次引导、连贯推演中的每一步骤、进度查询等均计为 1 步
- 利用已知图谱结构和引导反馈逆向分析出隐藏认知倾向
- 答案错误或超过操作上限将被判定为无效教案，规划失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Graph Path Planner." The system is dynamically adjusting knowledge guidance strategies based on individual student cognitive habits.
We will conduct a "Symbol Tree Navigation" learning planning exercise with the following rules:

Given a tree T representing the subject knowledge graph, with the fundamental starting point r. Each knowledge module (node) branches into at most 3 advanced learning paths (slots), difficulty-numbered 1, 2, 3.

**Knowledge Graph Blueprint:**
{blueprint}

**Target Exam Topic Address:** {target_address}

**Available Learning Commands (Symbols):** SymbolA, SymbolB, SymbolC

**Hidden Cognitive Tendency Mapping:**
Based on student assessments, the recommendation algorithm has secretly locked into one of the following six cognitive tendency schemes, defining the trigger configuration from learning commands (symbols) to advanced paths:
- SchemeA: SymbolA→1, SymbolB→2, SymbolC→3
- SchemeB: SymbolA→1, SymbolB→3, SymbolC→2
- SchemeC: SymbolA→2, SymbolB→1, SymbolC→3
- SchemeD: SymbolA→2, SymbolB→3, SymbolC→1
- SchemeE: SymbolA→3, SymbolB→1, SymbolC→2
- SchemeF: SymbolA→3, SymbolB→2, SymbolC→1

You need to identify the student's hidden true cognitive configuration scheme through interactive trials, and use it to translate the target exam topic address into a series of learning commands, successfully guiding to the target knowledge point.

**Victory Conditions (both must be satisfied):**
1. Learning progress reaches the target exam topic module
2. Correctly declare the student's cognitive tendency scheme

The exercise starts with progress at the fundamental starting point {root}. You can perform the following operations (one at a time):

1. **Single Guidance (Walk Operation)**: Issue a learning command to attempt unlocking the corresponding advanced path
   - Format: <walk>SymbolA</walk> or <walk>SymbolB</walk> or <walk>SymbolC</walk>
   - If subsequent content exists for the difficulty path, unlocking succeeds; otherwise, encountering a cognitive blind spot (hit wall), staying at the current module.

2. **Progress Query (Position Query)**: Query the ID of the knowledge point currently being studied
   - Format: <query_position></query_position>

3. **Topic Detection (Target Check)**: Detect if the current knowledge point is the ultimate target
   - Format: <query_target></query_target>

4. **Foundation Retake (Reset to Root)**: Clear learning progress, retreating to the fundamental starting point
   - Format: <reset></reset>

5. **Coherent Deduction (Batch Walk)**: Continuously learn from the start point following a command sequence (stops upon hitting a blind spot)
   - Format: <walk_sequence>SymbolA,SymbolB,SymbolC</walk_sequence>
   - Note: Symbols separated by comma, no spaces

6. **Establish Cognitive Model (Declare Permutation)**: Declare the true cognitive scheme you inferred
   - Format: <declare>SchemeA</declare> (scheme can be A/B/C/D/E/F)

When the teaching plan is confirmed and ready for submission, you must provide both:
1. Complete command sequence to conquer the target topic (from starting point)
2. Cognitive scheme model declaration

Format:
<answer>sequence=SymbolA,SymbolB,SymbolC, permutation=SchemeA</answer>

Note: Symbols separated by comma, no spaces.

- Interactive exercise steps cannot exceed {max_steps} steps to avoid student fatigue
- Each guidance, each step in coherent deduction, and progress query counts as 1 step
- Use the known graph structure and guidance feedback to reverse-analyze the hidden cognitive tendency
- Wrong answer or exceeding operation limit will be judged as an invalid lesson plan, leading to planning failure
"""

    contextualized_rule_zh_4 = """\
接入“自动化工厂物料智能分拣系统”。今日机床排产计划已更新，物理传送带与控制码的映射发生变动。
请执行“符号树导航”分拣验证程序，规则如下：

给定一棵代表工厂流水线分发网络的树 T，总入料口（根节点）为 r。每个分拣基站（节点）至多带有 3 条下级传送带（槽位），端口编号为 1、2、3。

**分发管线蓝图：**
{blueprint}

**目标加工区地址：** {target_address}

**可用分拣控制码（符号）：** 符号A、符号B、符号C

**隐藏排产映射规则：**
车间PLC控制器根据排产计划，已暗中激活了以下六种布线方案之一，它决定了控制码（符号）对应哪一条传送带端口：
- 方案A：符号A→1，符号B→2，符号C→3
- 方案B：符号A→1，符号B→3，符号C→2
- 方案C：符号A→2，符号B→1，符号C→3
- 方案D：符号A→2，符号B→3，符号C→1
- 方案E：符号A→3，符号B→1，符号C→2
- 方案F：符号A→3，符号B→2，符号C→1

你需要通过发送测试件摸底，排查出现有的真实布线方案，并运用该方案将目标加工区地址转换成分拣控制码序列，确保物料精准送达目标基站。

**胜利条件（必须同时满足）：**
1. 测试物料顺利落入目标分拣基站
2. 正确声明当日真实的控制布线方案

测试开始时，测试件处于总入料口 {root}。你可以进行以下操作（每次只能执行一个）：

1. **单次流转（移动操作）**：发送控制码使物料经由对应端口流入下一级
   - 格式：<walk>符号A</walk> 或 <walk>符号B</walk> 或 <walk>符号C</walk>
   - 若对应端口接有传送带，物料流转成功；否则挡板拦截（撞墙），滞留原基站

2. **射频追踪（位置查询）**：查询测试物料当前停靠的基站ID
   - 格式：<query_position></query_position>

3. **终点校验（目标检查）**：核对当前基站是否为指定的目标加工区
   - 格式：<query_target></query_target>

4. **强制回流（回到根节点）**：将测试件通过回收带直接打回总入料口
   - 格式：<reset></reset>

5. **连贯派发（批量移动）**：从入料口开始向系统一次性灌入控制码序列（遇拦截即中止报错）
   - 格式：<walk_sequence>符号A,符号B,符号C</walk_sequence>
   - 注意：符号之间用逗号分隔，无空格

6. **上报配置（声明置换）**：声明你反推得出的真实布线方案
   - 格式：<declare>方案A</declare>（方案可为 A/B/C/D/E/F）

当完成调试准备下发量产配置时，必须同时提供：
1. 连通目标加工区的有效控制码序列（从入料口起算）
2. 布线方案声明

格式：
<answer>sequence=符号A,符号B,符号C, permutation=方案A</answer>

注意：符号之间用逗号分隔，无空格。

- 调试能耗限制为 {max_steps} 个操作步数
- 每次单次流转、连贯派发中的每一次传送、以及系统查询等均计为 1 步
- 基于分发蓝图与物料阻滞反馈，推演出隐藏的机电映射规则
- 答案错误或耗时超限将引发停机警报，调试失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Accessing the "Automated Factory Intelligent Material Sorting System." Today's machine scheduling plan has been updated, altering the mapping between physical conveyor belts and control codes.
Please execute the "Symbol Tree Navigation" sorting verification program with the following rules:

Given a tree T representing the factory's distribution network, with the main feed inlet (root node) r. Each sorting base station (node) has at most 3 subordinate conveyor belts (slots), port-numbered 1, 2, 3.

**Distribution Pipeline Blueprint:**
{blueprint}

**Target Processing Area Address:** {target_address}

**Available Sorting Control Codes (Symbols):** SymbolA, SymbolB, SymbolC

**Hidden Scheduling Mapping Rule:**
According to the scheduling plan, the workshop PLC controller has secretly activated one of the following six wiring schemes, determining which conveyor belt port a control code (symbol) corresponds to:
- SchemeA: SymbolA→1, SymbolB→2, SymbolC→3
- SchemeB: SymbolA→1, SymbolB→3, SymbolC→2
- SchemeC: SymbolA→2, SymbolB→1, SymbolC→3
- SchemeD: SymbolA→2, SymbolB→3, SymbolC→1
- SchemeE: SymbolA→3, SymbolB→1, SymbolC→2
- SchemeF: SymbolA→3, SymbolB→2, SymbolC→1

You need to troubleshoot the current true wiring scheme by sending test pieces, and use this scheme to convert the target processing area address into a sorting control code sequence, ensuring precise material delivery to the target base station.

**Victory Conditions (both must be satisfied):**
1. Test material successfully drops into the target sorting base station
2. Correctly declare today's true control wiring scheme

Testing starts with the test piece at the main inlet {root}. You can perform the following operations (one at a time):

1. **Single Transfer (Walk Operation)**: Send a control code to make the material flow through the corresponding port to the next level
   - Format: <walk>SymbolA</walk> or <walk>SymbolB</walk> or <walk>SymbolC</walk>
   - If the corresponding port has an attached conveyor belt, transfer succeeds; otherwise, interceptor baffle blocks (hit wall), and material stays at the current station.

2. **RFID Tracking (Position Query)**: Query the ID of the base station where the test material is currently halted
   - Format: <query_position></query_position>

3. **Endpoint Verification (Target Check)**: Verify if the current base station is the designated target processing area
   - Format: <query_target></query_target>

4. **Forced Return Flow (Reset to Root)**: Send the test piece directly back to the main inlet via the recycling belt
   - Format: <reset></reset>

5. **Coherent Dispatch (Batch Walk)**: Inject a control code sequence into the system from the inlet all at once (stops and errors out upon interception)
   - Format: <walk_sequence>SymbolA,SymbolB,SymbolC</walk_sequence>
   - Note: Symbols separated by comma, no spaces

6. **Report Configuration (Declare Permutation)**: Declare the true wiring scheme you have reverse-engineered
   - Format: <declare>SchemeA</declare> (scheme can be A/B/C/D/E/F)

When debugging is complete and ready to deploy mass production configuration, you must provide both:
1. Valid control code sequence connecting to the target area (starting from inlet)
2. Wiring scheme declaration

Format:
<answer>sequence=SymbolA,SymbolB,SymbolC, permutation=SchemeA</answer>

Note: Symbols separated by comma, no spaces.

- Debugging energy consumption limit is {max_steps} operating steps
- Each single transfer, each conveyance in coherent dispatch, and system query counts as 1 step
- Deduce the hidden electromechanical mapping rules based on the distribution blueprint and material blockage feedback
- Wrong answer or exceeding time limit triggers a shutdown alarm, resulting in debugging failure
"""

    contextualized_rule_zh_5 = """\
欢迎使用“复杂案件法律适用推演系统”。在本次模拟庭审中，法理依据的输入与裁判走向的映射隐含了特定的预设立场。
请主导这场“符号树导航”法律推演，规则如下：

给定一棵代表案件事实审理脉络的逻辑树 T，案件起点为 r。每个事实认定阶段（节点）至多面临 3 个判决分支（槽位），顺位编号为 1、2、3。

**案件逻辑蓝图：**
{blueprint}

**目标胜诉判决地址：** {target_address}

**可用法理辩护策略（符号）：** 符号A、符号B、符号C

**隐藏裁判倾向映射：**
合议庭的裁判逻辑已被系统暗中设定为以下六种法理映射方案之一，该方案决定了辩护策略（符号）将导向哪一个判决分支：
- 方案A：符号A→1，符号B→2，符号C→3
- 方案B：符号A→1，符号B→3，符号C→2
- 方案C：符号A→2，符号B→1，符号C→3
- 方案D：符号A→2，符号B→3，符号C→1
- 方案E：符号A→3，符号B→1，符号C→2
- 方案F：符号A→3，符号B→2，符号C→1

你必须通过反复质证探明合议庭真实的裁判倾向方案，并依此将目标胜诉判决的地址转化为严密的法理策略序列，使庭审走向期望的最终判决。

**胜利条件（必须同时满足）：**
1. 庭审逻辑成功推进至目标胜诉判决节点
2. 准确指出系统预设的真实裁判方案

庭审推演从起点 {root} 开始。你可以进行以下操作（每次只能执行一个）：

1. **提出辩护（移动操作）**：抛出特定策略试图引导至对应判决分支
   - 格式：<walk>符号A</walk> 或 <walk>符号B</walk> 或 <walk>符号C</walk>
   - 若合议庭认可该分支存在延伸事实，则推进成功；否则论点被驳回（撞墙），庭审停留在原焦点

2. **卷宗核对（位置查询）**：查询当前所处的事实认定节点ID
   - 格式：<query_position></query_position>

3. **裁决预判（目标检查）**：审视当前的节点是否已达成目标胜诉判决
   - 格式：<query_target></query_target>

4. **撤诉重审（回到根节点）**：推翻先前进度，从案件起点重新展开辩论
   - 格式：<reset></reset>

5. **连贯陈词（批量移动）**：从起点开始提供一套连贯的策略序列进行论证（遭遇驳回即中止陈述）
   - 格式：<walk_sequence>符号A,符号B,符号C</walk_sequence>
   - 注意：符号之间用逗号分隔，无空格

6. **洞察法理（声明置换）**：声明你所洞悉的真实法理倾向方案
   - 格式：<declare>方案A</declare>（方案可为 A/B/C/D/E/F）

当准备就绪提交最终辩护方案时，必须同时提供：
1. 导向胜诉的完整辩护策略序列（从案件起点开始）
2. 裁判倾向方案声明

格式：
<answer>sequence=符号A,符号B,符号C, permutation=方案A</answer>

注意：符号之间用逗号分隔，无空格。

- 法庭辩论回合上限为 {max_steps} 步
- 每次提出辩护、连贯陈词中的每一项论据、卷宗核对等均消耗 1 个回合步数
- 结合案件蓝图和驳回反馈深挖隐藏的审判逻辑体系
- 策略失误或回合超限将导致败诉，推演直接终结
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Complex Case Legal Application Adjudication System." In this mock trial, the mapping between legal arguments input and adjudication outcomes contains a specific preset judicial stance.
Please lead this "Symbol Tree Navigation" legal deduction with the following rules:

Given a logical tree T representing the case's factual trial progression, with the case starting point r. Each fact-finding stage (node) faces at most 3 judgment branches (slots), sequentially numbered 1, 2, 3.

**Case Logic Blueprint:**
{blueprint}

**Target Favorable Verdict Address:** {target_address}

**Available Legal Defense Strategies (Symbols):** SymbolA, SymbolB, SymbolC

**Hidden Judicial Tendency Mapping:**
The collegial panel's adjudicative logic has been secretly preset by the system to one of the following six legal mapping schemes, which determines which judgment branch a defense strategy (symbol) will lead to:
- SchemeA: SymbolA→1, SymbolB→2, SymbolC→3
- SchemeB: SymbolA→1, SymbolB→3, SymbolC→2
- SchemeC: SymbolA→2, SymbolB→1, SymbolC→3
- SchemeD: SymbolA→2, SymbolB→3, SymbolC→1
- SchemeE: SymbolA→3, SymbolB→1, SymbolC→2
- SchemeF: SymbolA→3, SymbolB→2, SymbolC→1

You must ascertain the collegial panel's true adjudicative tendency scheme through repeated cross-examination, and use it to translate the target favorable verdict address into a rigorous legal strategy sequence, steering the trial toward the desired final verdict.

**Victory Conditions (both must be satisfied):**
1. Trial logic successfully advances to the target favorable verdict node
2. Accurately identify the system's preset true adjudicative scheme

The trial deduction starts from the starting point {root}. You can perform the following operations (one at a time):

1. **Present Defense (Walk Operation)**: Pitch a specific strategy attempting to guide to the corresponding judgment branch
   - Format: <walk>SymbolA</walk> or <walk>SymbolB</walk> or <walk>SymbolC</walk>
   - If the panel acknowledges extending facts in that branch, advancement succeeds; otherwise, the argument is overruled (hit wall), and the trial stays at the current focus.

2. **Dossier Check (Position Query)**: Query the ID of the current fact-finding node
   - Format: <query_position></query_position>

3. **Verdict Anticipation (Target Check)**: Review whether the current node has achieved the target favorable verdict
   - Format: <query_target></query_target>

4. **Withdraw and Retrial (Reset to Root)**: Overturn previous progress and restart the debate from the case's starting point
   - Format: <reset></reset>

5. **Coherent Statement (Batch Walk)**: Provide a coherent sequence of strategies for argumentation starting from the beginning (stops stating upon being overruled)
   - Format: <walk_sequence>SymbolA,SymbolB,SymbolC</walk_sequence>
   - Note: Symbols separated by comma, no spaces

6. **Insight into Jurisprudence (Declare Permutation)**: Declare the true legal tendency scheme you have discerned
   - Format: <declare>SchemeA</declare> (scheme can be A/B/C/D/E/F)

When ready to submit the final defense plan, you must provide both:
1. Complete defense strategy sequence leading to the favorable verdict (from the case starting point)
2. Adjudicative tendency scheme declaration

Format:
<answer>sequence=SymbolA,SymbolB,SymbolC, permutation=SchemeA</answer>

Note: Symbols separated by comma, no spaces.

- Court debate limit is {max_steps} steps
- Each presented defense, each argument in a coherent statement, dossier check, etc., consumes 1 round step
- Combine the case blueprint and overrule feedback to deeply uncover the hidden trial logic system
- Strategic error or exceeding round limit leads to losing the case, immediately terminating the deduction
"""

    tags = ["answer", "walk", "query_position", "query_target", "reset", "walk_sequence", "declare"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "root": "n1",
                "tree": {
                    "n1": ["n2", "n3", None],
                    "n2": [None, None, None],
                    "n3": [None, None, None],
                },
                "target_address": [2],
                "target_node": "n3",
                "permutation": "A", 
                "max_steps": 20,
            },
            2: {
                "root": "n1",
                "tree": {
                    "n1": ["n2", "n3", "n4"],
                    "n2": ["n5", None, None],
                    "n3": [None, None, None],
                    "n4": [None, None, None],
                    "n5": [None, None, None],
                },
                "target_address": [1, 1],
                "target_node": "n5",
                "permutation": "C", 
                "max_steps": 25,
            },
            3: {
                "root": "n1",
                "tree": {
                    "n1": ["n2", "n3", "n4"],
                    "n2": ["n5", None, None],
                    "n3": [None, "n6", "n7"],
                    "n4": [None, None, None],
                    "n5": [None, None, None],
                    "n6": [None, None, None],
                    "n7": [None, None, None],
                },
                "target_address": [2, 3],
                "target_node": "n7",
                "permutation": "E", 
                "max_steps": 30,
            },
            4: {
                "root": "n1",
                "tree": {
                    "n1": ["n2", "n3", "n4"],
                    "n2": ["n5", "n6", None],
                    "n3": ["n7", None, None],
                    "n4": [None, None, None],
                    "n5": ["n8", "n9", "n10"],
                    "n6": [None, None, None],
                    "n7": [None, None, None],
                    "n8": [None, None, None],
                    "n9": [None, None, None],
                    "n10": [None, None, None],
                },
                "target_address": [1, 1, 3],
                "target_node": "n10",
                "permutation": "B", 
                "max_steps": 40,
            },
            5: {
                "root": "n1",
                "tree": {
                    "n1": ["n2", "n3", "n4"],
                    "n2": ["n5", "n6", "n7"],
                    "n3": ["n8", None, "n9"],
                    "n4": [None, None, None],
                    "n5": [None, None, None],
                    "n6": ["n10", "n11", None],
                    "n7": [None, None, None],
                    "n8": [None, None, "n12"],
                    "n9": [None, None, None],
                    "n10": [None, None, None],
                    "n11": [None, None, None],
                    "n12": ["n13", None, None],
                    "n13": [None, None, None],
                },
                "target_address": [2, 1, 3, 1],
                "target_node": "n13",
                "permutation": "D", 
                "max_steps": 50,
            },
        },
        "en": {
            1: {
                "root": "n1",
                "tree": {
                    "n1": ["n2", "n3", None],
                    "n2": [None, None, None],
                    "n3": [None, None, None],
                },
                "target_address": [2],
                "target_node": "n3",
                "permutation": "A",
                "max_steps": 20,
            },
            2: {
                "root": "n1",
                "tree": {
                    "n1": ["n2", "n3", "n4"],
                    "n2": ["n5", None, None],
                    "n3": [None, None, None],
                    "n4": [None, None, None],
                    "n5": [None, None, None],
                },
                "target_address": [1, 1],
                "target_node": "n5",
                "permutation": "C",
                "max_steps": 25,
            },
            3: {
                "root": "n1",
                "tree": {
                    "n1": ["n2", "n3", "n4"],
                    "n2": ["n5", None, None],
                    "n3": [None, "n6", "n7"],
                    "n4": [None, None, None],
                    "n5": [None, None, None],
                    "n6": [None, None, None],
                    "n7": [None, None, None],
                },
                "target_address": [2, 3],
                "target_node": "n7",
                "permutation": "E",
                "max_steps": 30,
            },
            4: {
                "root": "n1",
                "tree": {
                    "n1": ["n2", "n3", "n4"],
                    "n2": ["n5", "n6", None],
                    "n3": ["n7", None, None],
                    "n4": [None, None, None],
                    "n5": ["n8", "n9", "n10"],
                    "n6": [None, None, None],
                    "n7": [None, None, None],
                    "n8": [None, None, None],
                    "n9": [None, None, None],
                    "n10": [None, None, None],
                },
                "target_address": [1, 1, 3],
                "target_node": "n10",
                "permutation": "B",
                "max_steps": 40,
            },
            5: {
                "root": "n1",
                "tree": {
                    "n1": ["n2", "n3", "n4"],
                    "n2": ["n5", "n6", "n7"],
                    "n3": ["n8", None, "n9"],
                    "n4": [None, None, None],
                    "n5": [None, None, None],
                    "n6": ["n10", "n11", None],
                    "n7": [None, None, None],
                    "n8": [None, None, "n12"],
                    "n9": [None, None, None],
                    "n10": [None, None, None],
                    "n11": [None, None, None],
                    "n12": ["n13", None, None],
                    "n13": [None, None, None],
                },
                "target_address": [2, 1, 3, 1],
                "target_node": "n13",
                "permutation": "D",
                "max_steps": 50,
            },
        },
    }

    PERMUTATIONS = {
        "A": {"符号A": 1, "符号B": 2, "符号C": 3, "SymbolA": 1, "SymbolB": 2, "SymbolC": 3},
        "B": {"符号A": 1, "符号B": 3, "符号C": 2, "SymbolA": 1, "SymbolB": 3, "SymbolC": 2},
        "C": {"符号A": 2, "符号B": 1, "符号C": 3, "SymbolA": 2, "SymbolB": 1, "SymbolC": 3},
        "D": {"符号A": 2, "符号B": 3, "符号C": 1, "SymbolA": 2, "SymbolB": 3, "SymbolC": 1},
        "E": {"符号A": 3, "符号B": 1, "符号C": 2, "SymbolA": 3, "SymbolB": 1, "SymbolC": 2},
        "F": {"符号A": 3, "符号B": 2, "符号C": 1, "SymbolA": 3, "SymbolB": 2, "SymbolC": 1},
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
        
        self.root = cfg["root"]
        self.tree = cfg["tree"]
        self.target_address = cfg["target_address"]
        self.target_node = cfg["target_node"]
        self.permutation_key = cfg["permutation"]
        self.max_steps = cfg["max_steps"]
        
        self.current_node = self.root
        self.step_count = 0
        self.declared_permutation = None
        
        blueprint_lines = []
        blueprint_lines.append(f"- 根节点: {self.root}" if lang == "zh" else f"- Root node: {self.root}")
        blueprint_lines.append("- 树结构（节点: [槽位1, 槽位2, 槽位3]）:" if lang == "zh" else "- Tree structure (node: [slot1, slot2, slot3]):")
        for node, children in sorted(self.tree.items()):
            child_str = ", ".join([c if c else ("无" if lang == "zh" else "None") for c in children])
            blueprint_lines.append(f"  {node}: [{child_str}]")
        
        self._game_info["blueprint"] = "\n".join(blueprint_lines)
        self._game_info["target_address"] = str(self.target_address)
        self._game_info["root"] = self.root
        self._game_info["max_steps"] = self.max_steps

    def _walk_symbol(self, symbol):
        perm = self.PERMUTATIONS[self.permutation_key]
        
        if symbol not in perm:
            if self.config.language == "zh":
                return f"错误：未知符号 {symbol}"
            else:
                return f"Error: Unknown symbol {symbol}"
        
        slot_idx = perm[symbol] - 1  
        
        if self.current_node not in self.tree:
            if self.config.language == "zh":
                return f"错误：节点 {self.current_node} 不在树中"
            else:
                return f"Error: Node {self.current_node} not in tree"
        
        children = self.tree[self.current_node]
        if slot_idx >= len(children) or children[slot_idx] is None:
            if self.config.language == "zh":
                return f"撞墙，仍在节点 {self.current_node}"
            else:
                return f"Hit wall, still at node {self.current_node}"
        
        self.current_node = children[slot_idx]
        if self.config.language == "zh":
            return f"到达节点 {self.current_node}"
        else:
            return f"Reached node {self.current_node}"

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        try:
            perm_pattern = re.search(r',\s*permutation\s*=\s*(.+)', raw_ans, re.IGNORECASE)
            seq_pattern = re.search(r'sequence\s*=\s*(.+?)(?:,\s*permutation\s*=)', raw_ans, re.IGNORECASE)
            
            if not perm_pattern or not seq_pattern:
                return False
            
            sequence_str = seq_pattern.group(1).strip().rstrip(',').strip()
            perm_str = perm_pattern.group(1).strip()
            
            perm_match = re.search(r'方案([A-F])|Scheme([A-F])', perm_str, re.IGNORECASE)
            if not perm_match:
                return False
            declared_perm = (perm_match.group(1) or perm_match.group(2)).upper()
            
            if declared_perm != self.permutation_key:
                return False
            
            test_node = self.root
            symbols = [s.strip() for s in sequence_str.split(",")]
            perm = self.PERMUTATIONS[self.permutation_key]
            
            for symbol in symbols:
                if not symbol:
                    continue
                if symbol not in perm:
                    return False
                slot_idx = perm[symbol] - 1
                if test_node not in self.tree:
                    return False
                children = self.tree[test_node]
                if slot_idx >= len(children) or children[slot_idx] is None:
                    return False
                test_node = children[slot_idx]
            
            return test_node == self.target_node
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if "walk_sequence" in parsed_info:
            sequence_str = parsed_info["walk_sequence"].strip()
            symbols = [s.strip() for s in sequence_str.split(",")]
            
            self.current_node = self.root
            responses = []
            
            if self.config.language == "zh":
                responses.append(f"从根节点 {self.root} 开始批量移动：")
            else:
                responses.append(f"Batch walk from root {self.root}:")
            
            for i, symbol in enumerate(symbols):
                self.step_count += 1
                if self.step_count > self.max_steps:
                    if self.config.language == "zh":
                        raise ValueError(f"超过最大步数限制 {self.max_steps}")
                    else:
                        raise ValueError(f"Exceeded maximum steps {self.max_steps}")
                
                result = self._walk_symbol(symbol)
                responses.append(f"步骤{i+1}: {result}" if self.config.language == "zh" else f"Step {i+1}: {result}")
                if "撞墙" in result or "Hit wall" in result:
                    break
            
            return "\n".join(responses)
        
        self.step_count += 1
        
        if self.step_count > self.max_steps:
            if self.config.language == "zh":
                raise ValueError(f"超过最大步数限制 {self.max_steps}")
            else:
                raise ValueError(f"Exceeded maximum steps {self.max_steps}")
        
        if "walk" in parsed_info:
            symbol = parsed_info["walk"].strip()
            return self._walk_symbol(symbol)
        
        elif "query_position" in parsed_info:
            if self.config.language == "zh":
                return f"当前在节点 {self.current_node}"
            else:
                return f"Currently at node {self.current_node}"
        
        elif "query_target" in parsed_info:
            is_target = self.current_node == self.target_node
            if self.config.language == "zh":
                return "是" if is_target else "否"
            else:
                return "Yes" if is_target else "No"
        
        elif "reset" in parsed_info:
            self.current_node = self.root
            if self.config.language == "zh":
                return f"已回到根节点 {self.root}"
            else:
                return f"Reset to root node {self.root}"
        
        elif "declare" in parsed_info:
            decl = parsed_info["declare"].strip()
            perm_match = re.search(r'方案([A-F])|Scheme([A-F])', decl, re.IGNORECASE)
            if perm_match:
                self.declared_permutation = (perm_match.group(1) or perm_match.group(2)).upper()
            else:
                self.declared_permutation = decl
            
            if self.config.language == "zh":
                return f"记录：你的声明是 {decl}"
            else:
                return f"Recorded: Your declaration is {decl}"
        
        else:
            if self.config.language == "zh":
                raise ValueError("未找到有效的操作标签")
            else:
                raise ValueError("No valid operation tag found")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "到达节点" in correct or "撞墙" in correct or "当前在节点" in correct:
                res = correct
                if "到达节点" in res:
                    res = re.sub(r"到达节点 n\d+", f"撞墙，仍在节点 {self.root}", res)
                elif "撞墙" in res:
                    res = re.sub(r"撞墙，仍在节点 n\d+", "到达节点 n99", res)
                if "当前在节点" in res:
                    res = re.sub(r"当前在节点 n\d+", "当前在节点 n99", res)
                return res
            
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            if "Reached node" in correct or "Hit wall" in correct or "Currently at node" in correct:
                res = correct
                if "Reached node" in res:
                    res = re.sub(r"Reached node n\d+", f"Hit wall, still at node {self.root}", res)
                elif "Hit wall" in res:
                    res = re.sub(r"Hit wall, still at node n\d+", "Reached node n99", res)
                if "Currently at node" in res:
                    res = re.sub(r"Currently at node n\d+", "Currently at node n99", res)
                return res

            pattern = r'\b(Yes|No)\b'
            
            def replace_yn(match):
                word = match.group()
                lower = word.lower()
                if lower == "yes":
                    if word.isupper(): return "NO"
                    if word.istitle(): return "No"
                    return "no"
                else: 
                    if word.isupper(): return "YES"
                    if word.istitle(): return "Yes"
                    return "yes"
            
            if re.search(pattern, correct, re.IGNORECASE):
                return re.sub(pattern, replace_yn, correct, flags=re.IGNORECASE)
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        saved_node = self.current_node
        saved_decl = self.declared_permutation
        
        try:
            if self.config.language == "zh":
                symbols = ["符号A", "符号B", "符号C"]
                schemes = ["方案A", "方案B", "方案C", "方案D", "方案E", "方案F"]
            else:
                symbols = ["SymbolA", "SymbolB", "SymbolC"]
                schemes = ["SchemeA", "SchemeB", "SchemeC", "SchemeD", "SchemeE", "SchemeF"]
            
            for sym in symbols:
                self.current_node = saved_node
                ans = self._walk_symbol(sym)
                queries.append({
                    "query": f"<walk>{sym}</walk>",
                    "answer": ans
                })

            self.current_node = saved_node
            if self.config.language == "zh":
                ans = f"当前在节点 {self.current_node}"
            else:
                ans = f"Currently at node {self.current_node}"
            queries.append({
                "query": "<query_position></query_position>",
                "answer": ans
            })

            self.current_node = saved_node
            is_target = self.current_node == self.target_node
            if self.config.language == "zh":
                ans = "是" if is_target else "否"
            else:
                ans = "Yes" if is_target else "No"
            queries.append({
                "query": "<query_target></query_target>",
                "answer": ans
            })

            if self.config.language == "zh":
                ans = f"已回到根节点 {self.root}"
            else:
                ans = f"Reset to root node {self.root}"
            queries.append({
                "query": "<reset></reset>",
                "answer": ans
            })
            
            for scheme in schemes:
                if self.config.language == "zh":
                    ans = f"记录：你的声明是 {scheme}"
                else:
                    ans = f"Recorded: Your declaration is {scheme}"
                queries.append({
                    "query": f"<declare>{scheme}</declare>",
                    "answer": ans
                })

            perm = self.PERMUTATIONS[self.permutation_key]
            inv_perm = {}
            for s, slot in perm.items():
                if self.config.language == "zh" and s.startswith("符号"):
                    inv_perm[slot] = s
                elif self.config.language == "en" and s.startswith("Symbol"):
                    inv_perm[slot] = s

            def _get_paths(node, path_symbols):
                paths = []
                children = self.tree.get(node, [None, None, None])
                for slot_idx in range(3):
                    if slot_idx < len(children) and children[slot_idx] is not None:
                        sym = inv_perm[slot_idx + 1]
                        new_path = path_symbols + [sym]
                        paths.append(new_path)
                        paths.extend(_get_paths(children[slot_idx], new_path))
                return paths

            all_paths = _get_paths(self.root, [])
            for path in all_paths:
                seq_str = ",".join(path)
                self.current_node = self.root
                responses = []
                if self.config.language == "zh":
                    responses.append(f"从根节点 {self.root} 开始批量移动：")
                else:
                    responses.append(f"Batch walk from root {self.root}:")
                
                for i, sym in enumerate(path):
                    res = self._walk_symbol(sym)
                    responses.append(f"步骤{i+1}: {res}" if self.config.language == "zh" else f"Step {i+1}: {res}")
                    if "撞墙" in res or "Hit wall" in res:
                        break
                
                queries.append({
                    "query": f"<walk_sequence>{seq_str}</walk_sequence>",
                    "answer": "\n".join(responses)
                })

        finally:
            self.current_node = saved_node
            self.declared_permutation = saved_decl
            
        return queries