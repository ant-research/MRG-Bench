from .base import Game
import re

class StateTransitionGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"状态空间探索"游戏，规则如下：

游戏设定了一个有序序列 S = {{1, 2, 3, 4, 5, 6, 7}}。你的初始状态是 {init_state}，目标状态是 {goal_state}。

你有两种控制动作可用，记为 B 与 R。每次执行动作，你的状态会在相邻元素间移动一步。但具体移动规则由一个隐藏的转移方案决定。

环境从四个确定性转移方案中选择了其中一个（记为 H），你需要通过试探来推断它。四个方案由两个维度决定：

1. 动作-方向映射：
   - 对齐：B 表示后继（向右），R 表示前驱（向左）
   - 反转：B 表示前驱（向左），R 表示后继（向右）

2. 边界处理：
   - 堵住（夹持）：在状态 7 时后继仍为 7；在状态 1 时前驱仍为 1
   - 环回（循环）：在状态 7 时后继为 1；在状态 1 时前驱为 7

具体四个方案：
- A（对齐且堵住）：B=后继，R=前驱；边界堵住
- B（反转且堵住）：B=前驱，R=后继；边界堵住
- C（对齐且环回）：B=后继，R=前驱；边界环回
- D（反转且环回）：B=前驱，R=后继；边界环回

其他位置的移动均为相邻一步：后继(i)=i+1（若可行），前驱(i)=i-1（若可行），仅在端点受边界规则修正。

你可以执行以下操作：

1. 执行动作：使用 B 或 R 动作。环境会返回执行后的当前状态编号。

2. 查询状态：询问当前状态是多少（注意：每次动作后环境会自动告知状态，此查询通常是冗余的）。

3. 宣告方案：提交你认为的真实方案（A、B、C 或 D）。
   - 前置条件：已累计执行至少两次动作，且至少有一次动作发生于端点状态（1 或 7）。
   - 若未满足前置条件，环境会提示你继续探索。
   - 若满足前置条件，环境会告知你的宣告是否正确。

你的目标：
1. 通过试探推断出真实的转移方案 H。
2. 正确宣告后，使你的最终状态到达目标状态 {goal_state}。

约束：
- 动作预算有限（仅计 B/R 动作次数；查询与宣告不计入）。
- 请尽可能少地使用动作次数完成任务。

成功条件：
1. 在动作预算内正确宣告真实方案 H。
2. 在正确宣告后最终到达目标状态 {goal_state}。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 执行动作 B：
<action>B</action>

- 执行动作 R：
<action>R</action>

- 查询当前状态：
<query_state></query_state>

- 宣告方案（例如宣告方案 A）：
<declare>A</declare>

- 提交最终答案（当你已正确宣告方案且到达目标状态后）：
<answer>success</answer>
"""

    game_rule_en = """\
Let's play a "State Space Exploration" game. Here are the rules:

The game defines an ordered sequence S = {{1, 2, 3, 4, 5, 6, 7}}. Your initial state is {init_state}, and the goal state is {goal_state}.

You have two control actions available, denoted as B and R. Each action moves your state one step between adjacent elements. However, the specific movement rules are determined by a hidden transition scheme.

The environment has selected one of four deterministic transition schemes (denoted as H), and you need to infer it through exploration. The four schemes are determined by two dimensions:

1. Action-Direction Mapping:
   - Aligned: B means successor (right), R means predecessor (left)
   - Reversed: B means predecessor (left), R means successor (right)

2. Boundary Handling:
   - Clamped: At state 7, successor remains 7; at state 1, predecessor remains 1
   - Wrapped: At state 7, successor becomes 1; at state 1, predecessor becomes 7

The four specific schemes:
- A (Aligned and Clamped): B=successor, R=predecessor; boundaries clamped
- B (Reversed and Clamped): B=predecessor, R=successor; boundaries clamped
- C (Aligned and Wrapped): B=successor, R=predecessor; boundaries wrapped
- D (Reversed and Wrapped): B=predecessor, R=successor; boundaries wrapped

Movement at other positions is always one adjacent step: successor(i)=i+1 (if possible), predecessor(i)=i-1 (if possible), only modified at endpoints by boundary rules.

You can perform the following operations:

1. Execute Action: Use B or R action. The environment will return the current state number after execution.

2. Query State: Ask what the current state is (note: the environment automatically reports the state after each action, so this query is usually redundant).

3. Declare Scheme: Submit what you believe is the true scheme (A, B, C, or D).
   - Precondition: You must have executed at least two actions, and at least one action occurred at a boundary state (1 or 7).
   - If the precondition is not met, the environment will prompt you to continue exploring.
   - If the precondition is met, the environment will tell you whether your declaration is correct.

Your goals:
1. Infer the true transition scheme H through exploration.
2. After correctly declaring, make your final state reach the goal state {goal_state}.

Constraints:
- Action budget is limited (only counts B/R actions; queries and declarations do not count).
- Please use as few actions as possible to complete the task.

Success conditions:
1. Correctly declare the true scheme H within the action budget.
2. Finally reach the goal state {goal_state} after correct declaration.

Each operation can only contain one tag. Use the following XML format:

- Execute action B:
<action>B</action>

- Execute action R:
<action>R</action>

- Query current state:
<query_state></query_state>

- Declare scheme (e.g., declare scheme A):
<declare>A</declare>

- Submit final answer (after you have correctly declared the scheme and reached the goal state):
<answer>success</answer>
"""

    contextualized_rule_zh_1 = """\
这是一款自动驾驶路径控制测试环境。你的测试车辆处于一条具有7个连续路段的跑道序列 S = {{1, 2, 3, 4, 5, 6, 7}} 中。初始所在的路段是 {init_state}，目标路段是 {goal_state}。

你有两种控制指令可用，记为 B 与 R。每次发送指令，车辆会在相邻路段间移动一步。但具体移动方向由一个隐藏的系统调度方案决定。

环境从四个确定性调度方案中选择了其中一个（记为 H），你需要通过试探来推断它。四个方案由两个维度决定：

1. 指令-方向映射：
   - 标准：B 表示前进（路段编号增加），R 表示后退（路段编号减少）
   - 反转：B 表示后退（路段编号减少），R 表示前进（路段编号增加）

2. 边界处理：
   - 尽头死胡同（夹持）：在路段 7 时继续前进仍停在 7；在路段 1 时继续后退仍停在 1
   - 环形立交（环回）：在路段 7 时继续前进将进入路段 1；在路段 1 时继续后退将进入路段 7

具体四个方案：
- A（标准且死胡同）：B=前进，R=后退；边界为尽头死胡同
- B（反转且死胡同）：B=后退，R=前进；边界为尽头死胡同
- C（标准且环形立交）：B=前进，R=后退；边界为环形立交
- D（反转且环形立交）：B=后退，R=前进；边界为环形立交

其他路段的移动均为相邻一步：前进(i)=i+1（若可行），后退(i)=i-1（若可行），仅在端点受边界规则修正。

你可以执行以下操作：

1. 执行指令：使用 B 或 R 指令。环境会返回执行后的当前路段编号。

2. 查询路段：询问当前所在的路段是多少（注意：每次指令后环境会自动告知路段，此查询通常是冗余的）。

3. 宣告方案：提交你认为的真实方案（A、B、C 或 D）。
   - 前置条件：已累计执行至少两次指令，且至少有一次指令发生于端点路段（1 或 7）。
   - 若未满足前置条件，环境会提示你继续探索。
   - 若满足前置条件，环境会告知你的宣告是否正确。

你的目标：
1. 通过试探推断出真实的调度方案 H。
2. 正确宣告后，使车辆最终到达目标路段 {goal_state}。

约束：
- 指令预算有限（仅计 B/R 动作次数；查询与宣告不计入）。
- 请尽可能少地使用指令次数完成任务。

成功条件：
1. 在指令预算内正确宣告真实方案 H。
2. 在正确宣告后最终到达目标路段 {goal_state}。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 发送指令 B：
<action>B</action>

- 发送指令 R：
<action>R</action>

- 查询当前路段：
<query_state></query_state>

- 宣告方案（例如宣告方案 A）：
<declare>A</declare>

- 提交最终答案（当你已正确宣告方案且到达目标路段后）：
<answer>success</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
This is an autonomous vehicle routing test environment. Your test vehicle is on a track sequence of 7 continuous segments S = {{1, 2, 3, 4, 5, 6, 7}}. Your initial segment is {init_state}, and the target segment is {goal_state}.

You have two control commands available, denoted as B and R. Each command moves the vehicle one step to an adjacent segment. However, the specific movement direction is determined by a hidden system scheduling scheme.

The environment has selected one of four deterministic scheduling schemes (denoted as H), and you need to infer it through exploration. The four schemes are defined by two dimensions:

1. Command-Direction Mapping:
   - Standard: B means Forward (segment number increases), R means Backward (segment number decreases)
   - Reversed: B means Backward (segment number decreases), R means Forward (segment number increases)

2. Boundary Handling:
   - Dead End (Clamped): At segment 7, continuing forward remains at 7; at segment 1, continuing backward remains at 1
   - Circular Interchange (Wrapped): At segment 7, continuing forward enters segment 1; at segment 1, continuing backward enters segment 7

The four specific schemes:
- A (Standard & Dead End): B=Forward, R=Backward; boundaries clamped
- B (Reversed & Dead End): B=Backward, R=Forward; boundaries clamped
- C (Standard & Circular): B=Forward, R=Backward; boundaries wrapped
- D (Reversed & Circular): B=Backward, R=Forward; boundaries wrapped

Movement at other segments is always one adjacent step: Forward(i)=i+1 (if possible), Backward(i)=i-1 (if possible), only modified at endpoints by boundary rules.

You can perform the following operations:

1. Execute Command: Use B or R command. The environment will return the current segment number after execution.

2. Query Segment: Ask what the current segment is (note: the environment automatically reports the segment after each command, so this query is usually redundant).

3. Declare Scheme: Submit what you believe is the true scheme (A, B, C, or D).
   - Precondition: You must have executed at least two commands, and at least one command must have occurred at an endpoint segment (1 or 7).
   - If the precondition is not met, the environment will prompt you to continue exploring.
   - If the precondition is met, the environment will tell you whether your declaration is correct.

Your goals:
1. Infer the true scheduling scheme H through exploration.
2. After correctly declaring, make your vehicle reach the target segment {goal_state}.

Constraints:
- Command budget is limited (only counts B/R commands; queries and declarations do not count).
- Please use as few commands as possible to complete the task.

Success conditions:
1. Correctly declare the true scheme H within the command budget.
2. Finally reach the target segment {goal_state} after correct declaration.

Each operation can only contain one tag. Use the following XML format:

- Execute command B:
<action>B</action>

- Execute command R:
<action>R</action>

- Query current segment:
<query_state></query_state>

- Declare scheme (e.g., declare scheme A):
<declare>A</declare>

- Submit final answer (after you have correctly declared the scheme and reached the target segment):
<answer>success</answer>
"""

    contextualized_rule_zh_2 = """\
这是一款临床治疗方案动态调整系统。患者的康复过程被划分为7个阶段序列 S = {{1, 2, 3, 4, 5, 6, 7}}。初始阶段是 {init_state}，目标阶段是 {goal_state}。

你有两种干预药物可用，记为 B 与 R。每次用药，患者的病情阶段会在相邻级别间变化。但具体药效方向由一个隐藏的病理代谢方案决定。

系统从四个确定性代谢方案中选择了其中一个（记为 H），你需要通过临床试探来推断它。四个方案由两个维度决定：

1. 药效-方向映射：
   - 正向：B 表示好转（阶段编号增加），R 表示恶化（阶段编号减少）
   - 反向：B 表示恶化（阶段编号减少），R 表示好转（阶段编号增加）

2. 极值边界处理：
   - 稳定极值（夹持）：在阶段 7 时继续好转仍稳定在 7；在阶段 1 时继续恶化仍停留在 1
   - 周期复发（环回）：在阶段 7 时继续好转将复发跌回阶段 1；在阶段 1 时继续恶化将反弹至阶段 7

具体四个方案：
- A（正向且稳定）：B=好转，R=恶化；极值稳定
- B（反向且稳定）：B=恶化，R=好转；极值稳定
- C（正向且复发）：B=好转，R=恶化；极值周期复发
- D（反向且复发）：B=恶化，R=好转；极值周期复发

其他阶段的药效变化均为相邻一步：好转(i)=i+1（若可行），恶化(i)=i-1（若可行），仅在极值点受边界规则修正。

你可以执行以下操作：

1. 执行干预：使用药物 B 或 R。系统会返回用药后的当前病情阶段。

2. 查询阶段：询问当前的病情阶段（注意：每次用药后系统会自动告知阶段，此查询通常是冗余的）。

3. 宣告方案：提交你认为的真实方案（A、B、C 或 D）。
   - 前置条件：已累计执行至少两次干预，且至少有一次干预发生于极值阶段（1 或 7）。
   - 若未满足前置条件，系统会提示你继续观察。
   - 若满足前置条件，系统会告知你的宣告是否正确。

你的目标：
1. 通过试探推断出真实的病理代谢方案 H。
2. 正确宣告后，使患者最终达到目标阶段 {goal_state}。

约束：
- 用药次数有限（仅计 B/R 药物使用次数；查询与宣告不计入）。
- 请尽可能少地使用干预次数完成任务。

成功条件：
1. 在用药预算内正确宣告真实方案 H。
2. 在正确宣告后最终到达目标阶段 {goal_state}。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 使用药物 B：
<action>B</action>

- 使用药物 R：
<action>R</action>

- 查询当前阶段：
<query_state></query_state>

- 宣告方案（例如宣告方案 A）：
<declare>A</declare>

- 提交最终答案（当你已正确宣告方案且到达目标阶段后）：
<answer>success</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
This is a clinical treatment dynamic adjustment system. The patient's recovery process is divided into a sequence of 7 stages S = {{1, 2, 3, 4, 5, 6, 7}}. The initial stage is {init_state}, and the target stage is {goal_state}.

You have two intervention medications available, denoted as B and R. Each medication causes the patient's condition to shift by one adjacent stage. However, the specific therapeutic direction is determined by a hidden pathological metabolic scheme.

The system has selected one of four deterministic metabolic schemes (denoted as H), and you need to infer it through clinical trials. The four schemes are defined by two dimensions:

1. Therapeutic-Direction Mapping:
   - Direct: B means Improvement (stage number increases), R means Deterioration (stage number decreases)
   - Inverse: B means Deterioration (stage number decreases), R means Improvement (stage number increases)

2. Extreme Boundary Handling:
   - Stable Extremes (Clamped): At stage 7, further improvement remains stable at 7; at stage 1, further deterioration remains at 1
   - Periodic Relapse (Wrapped): At stage 7, further improvement triggers a relapse back to stage 1; at stage 1, further deterioration rebounds to stage 7

The four specific schemes:
- A (Direct & Stable): B=Improvement, R=Deterioration; extremes clamped
- B (Inverse & Stable): B=Deterioration, R=Improvement; extremes clamped
- C (Direct & Relapse): B=Improvement, R=Deterioration; extremes wrapped
- D (Inverse & Relapse): B=Deterioration, R=Improvement; extremes wrapped

Condition changes at other stages are always one adjacent step: Improvement(i)=i+1 (if possible), Deterioration(i)=i-1 (if possible), only modified at extreme points by boundary rules.

You can perform the following operations:

1. Execute Intervention: Administer medication B or R. The system will return the current stage after administration.

2. Query Stage: Ask what the current stage is (note: the system automatically reports the stage after each medication, so this query is usually redundant).

3. Declare Scheme: Submit what you believe is the true scheme (A, B, C, or D).
   - Precondition: You must have executed at least two interventions, and at least one must have occurred at an extreme stage (1 or 7).
   - If the precondition is not met, the system will prompt you to continue observing.
   - If the precondition is met, the system will tell you whether your declaration is correct.

Your goals:
1. Infer the true metabolic scheme H through clinical trials.
2. After correctly declaring, ensure the patient reaches the target stage {goal_state}.

Constraints:
- Medication budget is limited (only counts B/R usage; queries and declarations do not count).
- Please use as few interventions as possible to complete the task.

Success conditions:
1. Correctly declare the true scheme H within the medication budget.
2. Finally reach the target stage {goal_state} after correct declaration.

Each operation can only contain one tag. Use the following XML format:

- Administer medication B:
<action>B</action>

- Administer medication R:
<action>R</action>

- Query current stage:
<query_state></query_state>

- Declare scheme (e.g., declare scheme A):
<declare>A</declare>

- Submit final answer (after you have correctly declared the scheme and reached the target stage):
<answer>success</answer>
"""

    contextualized_rule_zh_3 = """\
这是一款自适应学习难度调节系统。认知等级序列 S = {{1, 2, 3, 4, 5, 6, 7}}，代表了知识深度的7个递进层级。初始所在的等级是 {init_state}，目标等级是 {goal_state}。

你有两种教学策略可用，记为 B 与 R。每次应用策略，学生的认知等级会在相邻层级间浮动。但具体浮动方向由一个隐藏的学习者模型方案决定。

系统从四个确定性模型方案中选择了其中一个（记为 H），你需要通过教学试探来推断它。四个方案由两个维度决定：

1. 策略-方向映射：
   - 顺向：B 表示升级（向更高层级），R 表示降级（向更低层级）
   - 逆向：B 表示降级（向更低层级），R 表示升级（向更高层级）

2. 瓶颈边界处理：
   - 封顶锁死（夹持）：在等级 7 时继续升级仍停留在 7；在等级 1 时继续降级仍停留在 1
   - 循环重置（环回）：在等级 7 时继续升级将重置回等级 1；在等级 1 时继续降级将直接跃迁至等级 7

具体四个方案：
- A（顺向且封顶）：B=升级，R=降级；边界封顶锁死
- B（逆向且封顶）：B=降级，R=升级；边界封顶锁死
- C（顺向且重置）：B=升级，R=降级；边界循环重置
- D（逆向且重置）：B=降级，R=升级；边界循环重置

其他层级的浮动均为相邻一步：升级(i)=i+1（若可行），降级(i)=i-1（若可行），仅在极端层级受边界规则修正。

你可以执行以下操作：

1. 应用策略：使用 B 或 R 策略。系统会返回应用后的当前认知等级。

2. 查询等级：询问当前的认知等级是多少（注意：每次策略应用后系统会自动告知等级，此查询通常是冗余的）。

3. 宣告方案：提交你认为的真实方案（A、B、C 或 D）。
   - 前置条件：已累计应用至少两次策略，且至少有一次策略发生于极端等级（1 或 7）。
   - 若未满足前置条件，系统会提示你继续试探。
   - 若满足前置条件，系统会告知你的宣告是否正确。

你的目标：
1. 通过试探推断出真实的学习者模型方案 H。
2. 正确宣告后，使学生最终达到目标等级 {goal_state}。

约束：
- 策略次数预算有限（仅计 B/R 策略次数；查询与宣告不计入）。
- 请尽可能少地应用策略完成任务。

成功条件：
1. 在策略预算内正确宣告真实方案 H。
2. 在正确宣告后最终到达目标等级 {goal_state}。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 应用策略 B：
<action>B</action>

- 应用策略 R：
<action>R</action>

- 查询当前等级：
<query_state></query_state>

- 宣告方案（例如宣告方案 A）：
<declare>A</declare>

- 提交最终答案（当你已正确宣告方案且到达目标等级后）：
<answer>success</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
This is an adaptive learning difficulty adjustment system. The cognitive level sequence is S = {{1, 2, 3, 4, 5, 6, 7}}, representing 7 progressive layers of knowledge depth. The initial level is {init_state}, and the target level is {goal_state}.

You have two teaching strategies available, denoted as B and R. Each applied strategy shifts the student's cognitive level to an adjacent layer. However, the specific shift direction is determined by a hidden learner model scheme.

The system has selected one of four deterministic model schemes (denoted as H), and you need to infer it through pedagogical trials. The four schemes are defined by two dimensions:

1. Strategy-Direction Mapping:
   - Proactive: B means Level Up (to a higher layer), R means Level Down (to a lower layer)
   - Reactive: B means Level Down (to a lower layer), R means Level Up (to a higher layer)

2. Bottleneck Boundary Handling:
   - Locked Cap (Clamped): At level 7, leveling up remains at 7; at level 1, leveling down remains at 1
   - Cycle Reset (Wrapped): At level 7, leveling up resets back to level 1; at level 1, leveling down leaps to level 7

The four specific schemes:
- A (Proactive & Locked): B=Level Up, R=Level Down; boundaries clamped
- B (Reactive & Locked): B=Level Down, R=Level Up; boundaries clamped
- C (Proactive & Reset): B=Level Up, R=Level Down; boundaries wrapped
- D (Reactive & Reset): B=Level Down, R=Level Up; boundaries wrapped

Level shifts at other layers are always one adjacent step: Level Up(i)=i+1 (if possible), Level Down(i)=i-1 (if possible), only modified at extreme levels by boundary rules.

You can perform the following operations:

1. Apply Strategy: Use strategy B or R. The system will return the current cognitive level after application.

2. Query Level: Ask what the current cognitive level is (note: the system automatically reports the level after each strategy, so this query is usually redundant).

3. Declare Scheme: Submit what you believe is the true scheme (A, B, C, or D).
   - Precondition: You must have applied at least two strategies, and at least one must have occurred at an extreme level (1 or 7).
   - If the precondition is not met, the system will prompt you to continue testing.
   - If the precondition is met, the system will tell you whether your declaration is correct.

Your goals:
1. Infer the true learner model scheme H through pedagogical trials.
2. After correctly declaring, guide the student to the target level {goal_state}.

Constraints:
- Strategy budget is limited (only counts B/R applications; queries and declarations do not count).
- Please use as few strategies as possible to complete the task.

Success conditions:
1. Correctly declare the true scheme H within the strategy budget.
2. Finally reach the target level {goal_state} after correct declaration.

Each operation can only contain one tag. Use the following XML format:

- Apply strategy B:
<action>B</action>

- Apply strategy R:
<action>R</action>

- Query current level:
<query_state></query_state>

- Declare scheme (e.g., declare scheme A):
<declare>A</declare>

- Submit final answer (after you have correctly declared the scheme and reached the target level):
<answer>success</answer>
"""

    contextualized_rule_zh_4 = """\
这是一款柔性制造流水线调度系统。工位序列 S = {{1, 2, 3, 4, 5, 6, 7}}，代表生产线上的7个关键装配节点。物料的初始工位是 {init_state}，目标工位是 {goal_state}。

你有两种传送带驱动指令，记为 B 与 R。每次下达指令，物料会在相邻工位间流转。但具体流转方向由当前隐藏的机械传动方案决定。

控制台从四个确定性传动方案中选择了其中一个（记为 H），你需要通过流转测试来推断它。四个方案由两个维度决定：

1. 指令-方向映射：
   - 顺流：B 表示流向下游（工位编号增加），R 表示退回上游（工位编号减少）
   - 逆流：B 表示退回上游（工位编号减少），R 表示流向下游（工位编号增加）

2. 传送带边界处理：
   - 物理挡板（夹持）：在工位 7 时继续向下游仍滞留于 7；在工位 1 时继续向上游仍滞留于 1
   - 闭环轨道（环回）：在工位 7 时继续向下游将重新传回工位 1；在工位 1 时继续向上游将倒退至工位 7

具体四个方案：
- A（顺流且物理阻挡）：B=下游，R=上游；边界为物理挡板
- B（逆流且物理阻挡）：B=上游，R=下游；边界为物理挡板
- C（顺流且闭环轨道）：B=下游，R=上游；边界为闭环轨道
- D（逆流且闭环轨道）：B=上游，R=下游；边界为闭环轨道

其他工位的流转均为相邻一步：下游(i)=i+1（若可行），上游(i)=i-1（若可行），仅在首尾工位受边界规则修正。

你可以执行以下操作：

1. 下达指令：发送 B 或 R 指令。系统会返回执行后的物料当前工位。

2. 查询工位：询问当前的物料所在工位（注意：每次指令后系统会自动告知工位，此查询通常是冗余的）。

3. 宣告方案：提交你认为的真实传动方案（A、B、C 或 D）。
   - 前置条件：已累计下达至少两次指令，且至少有一次指令发生于首尾工位（1 或 7）。
   - 若未满足前置条件，系统会提示你继续测试。
   - 若满足前置条件，系统会告知你的宣告是否正确。

你的目标：
1. 通过流转测试推断出真实的传动方案 H。
2. 正确宣告后，使物料最终停靠在目标工位 {goal_state}。

约束：
- 驱动能耗预算有限（仅计 B/R 指令次数；查询与宣告不计入）。
- 请尽可能少地消耗指令次数完成调度任务。

成功条件：
1. 在指令预算内正确宣告真实方案 H。
2. 在正确宣告后物料最终到达目标工位 {goal_state}。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 下达指令 B：
<action>B</action>

- 下达指令 R：
<action>R</action>

- 查询当前工位：
<query_state></query_state>

- 宣告方案（例如宣告方案 A）：
<declare>A</declare>

- 提交最终调度结果（当你已正确宣告方案且到达目标工位后）：
<answer>success</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
This is a flexible manufacturing pipeline scheduling system. The workstation sequence is S = {{1, 2, 3, 4, 5, 6, 7}}, representing 7 key assembly nodes on the production line. The material's initial workstation is {init_state}, and the target workstation is {goal_state}.

You have two conveyor drive commands available, denoted as B and R. Each issued command transfers the material between adjacent workstations. However, the specific transfer direction is determined by a hidden mechanical transmission scheme.

The console has selected one of four deterministic transmission schemes (denoted as H), and you need to infer it through transfer testing. The four schemes are defined by two dimensions:

1. Command-Direction Mapping:
   - Downstream Focus: B means Flow Downstream (workstation number increases), R means Return Upstream (workstation number decreases)
   - Upstream Focus: B means Return Upstream (workstation number decreases), R means Flow Downstream (workstation number increases)

2. Conveyor Boundary Handling:
   - Physical Stop (Clamped): At workstation 7, further downstream flow stalls at 7; at workstation 1, further upstream return stalls at 1
   - Closed-Loop Track (Wrapped): At workstation 7, further downstream flow loops back to workstation 1; at workstation 1, further upstream return shifts to workstation 7

The four specific schemes:
- A (Downstream & Physical Stop): B=Downstream, R=Upstream; boundaries clamped
- B (Upstream & Physical Stop): B=Upstream, R=Downstream; boundaries clamped
- C (Downstream & Closed-Loop): B=Downstream, R=Upstream; boundaries wrapped
- D (Upstream & Closed-Loop): B=Upstream, R=Downstream; boundaries wrapped

Transfers at other workstations are always one adjacent step: Downstream(i)=i+1 (if possible), Upstream(i)=i-1 (if possible), only modified at endpoints by boundary rules.

You can perform the following operations:

1. Issue Command: Send B or R command. The system will return the material's current workstation after execution.

2. Query Workstation: Ask for the current material workstation (note: the system automatically reports the workstation after each command, so this query is usually redundant).

3. Declare Scheme: Submit what you believe is the true scheme (A, B, C, or D).
   - Precondition: You must have issued at least two commands, and at least one must have occurred at an endpoint workstation (1 or 7).
   - If the precondition is not met, the system will prompt you to continue testing.
   - If the precondition is met, the system will tell you whether your declaration is correct.

Your goals:
1. Infer the true transmission scheme H through transfer testing.
2. After correctly declaring, ensure the material parks at the target workstation {goal_state}.

Constraints:
- Drive energy budget is limited (only counts B/R commands; queries and declarations do not count).
- Please use as few commands as possible to complete the scheduling task.

Success conditions:
1. Correctly declare the true scheme H within the command budget.
2. Finally reach the target workstation {goal_state} after correct declaration.

Each operation can only contain one tag. Use the following XML format:

- Issue command B:
<action>B</action>

- Issue command R:
<action>R</action>

- Query current workstation:
<query_state></query_state>

- Declare scheme (e.g., declare scheme A):
<declare>A</declare>

- Submit final result (after you have correctly declared the scheme and reached the target workstation):
<answer>success</answer>
"""

    contextualized_rule_zh_5 = """\
这是一款司法争议解决流程模拟器。案件的审理被划分为7个法定程序阶段序列 S = {{1, 2, 3, 4, 5, 6, 7}}。案件当前的初始阶段是 {init_state}，目标达成阶段是 {goal_state}。

你有两种诉讼动作可用，记为 B 与 R。每次采取诉讼动作，案件会在相邻的程序阶段间推进或退回。但具体流转方向由当前管辖的隐性诉讼规则方案决定。

系统从四个确定性诉讼规则方案中选择了其中一个（记为 H），你需要通过程序试探来推断它。四个方案由两个维度决定：

1. 动作-方向映射：
   - 进取：B 表示上诉推进（向后序阶段流转），R 表示退回异议（向前序阶段退回）
   - 保守：B 表示退回异议（向前序阶段退回），R 表示上诉推进（向后序阶段流转）

2. 审级边界处理：
   - 终审穷尽（夹持）：在阶段 7 时继续推进仍维持终审状态 7；在阶段 1 时继续退回仍滞留于立案阶段 1
   - 发回重审（环回）：在阶段 7 时继续推进将触发程序重启回到阶段 1；在阶段 1 时继续退回将因特殊抗诉直接跃迁至阶段 7

具体四个方案：
- A（进取且终审穷尽）：B=推进，R=退回；边界为终审穷尽
- B（保守且终审穷尽）：B=退回，R=推进；边界为终审穷尽
- C（进取且发回重审）：B=推进，R=退回；边界为发回重审机制
- D（保守且发回重审）：B=退回，R=推进；边界为发回重审机制

其他程序阶段的流转均为相邻一步：推进(i)=i+1（若法定允许），退回(i)=i-1（若法定允许），仅在首尾极端阶段受边界规则修正。

你可以执行以下操作：

1. 采取动作：执行诉讼动作 B 或 R。系统会返回流转后的案件当前阶段。

2. 查询阶段：询问当前的程序阶段（注意：每次动作后系统会自动告知阶段，此查询通常是冗余的）。

3. 宣告方案：提交你认为的真实规则方案（A、B、C 或 D）。
   - 前置条件：已累计采取至少两次诉讼动作，且至少有一次动作发生于极端阶段（1 或 7）。
   - 若未满足前置条件，系统会驳回请求并提示继续推进。
   - 若满足前置条件，系统会裁定你的宣告是否正确。

你的目标：
1. 通过程序试探推断出真实的诉讼规则方案 H。
2. 正确宣告后，使案件程序最终落定在目标阶段 {goal_state}。

约束：
- 法定期限/动议次数有限（仅计 B/R 动作次数；查询与宣告不计入）。
- 请以最精简的诉讼步骤完成任务。

成功条件：
1. 在诉讼预算内正确宣告真实方案 H。
2. 在正确宣告后最终到达目标阶段 {goal_state}。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 采取诉讼动作 B：
<action>B</action>

- 采取诉讼动作 R：
<action>R</action>

- 查询当前阶段：
<query_state></query_state>

- 宣告方案（例如宣告方案 A）：
<declare>A</declare>

- 提交最终结案（当你已正确宣告方案且案件到达目标阶段后）：
<answer>success</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
This is a judicial dispute resolution simulator. The case review procedure is divided into a sequence of 7 statutory stages S = {{1, 2, 3, 4, 5, 6, 7}}. The initial procedural stage is {init_state}, and the target stage is {goal_state}.

You have two litigation motions available, denoted as B and R. Each executed motion causes the case to progress or revert between adjacent procedural stages. However, the specific direction is determined by a hidden jurisdictional rule scheme.

The system has selected one of four deterministic rule schemes (denoted as H), and you need to infer it through procedural testing. The four schemes are defined by two dimensions:

1. Motion-Direction Mapping:
   - Aggressive: B means Escalate (progress to next stage), R means Remand (revert to previous stage)
   - Conservative: B means Remand (revert to previous stage), R means Escalate (progress to next stage)

2. Jurisdiction Boundary Handling:
   - Final Exhaustion (Clamped): At stage 7, further escalation remains stuck at final stage 7; at stage 1, further remand remains stalled at filing stage 1
   - Retrial Refresh (Wrapped): At stage 7, further escalation triggers a retrial refresh back to stage 1; at stage 1, further remand leaps via special appeal to stage 7

The four specific schemes:
- A (Aggressive & Final Exhaustion): B=Escalate, R=Remand; boundaries clamped
- B (Conservative & Final Exhaustion): B=Remand, R=Escalate; boundaries clamped
- C (Aggressive & Retrial Refresh): B=Escalate, R=Remand; boundaries wrapped
- D (Conservative & Retrial Refresh): B=Remand, R=Escalate; boundaries wrapped

Transfers at other stages are always one adjacent step: Escalate(i)=i+1 (if allowed), Remand(i)=i-1 (if allowed), only modified at extreme stages by boundary rules.

You can perform the following operations:

1. Execute Motion: Perform litigation motion B or R. The system will return the current procedural stage.

2. Query Stage: Ask what the current stage is (note: the system automatically reports the stage after each motion, so this query is usually redundant).

3. Declare Scheme: Submit what you believe is the true rule scheme (A, B, C, or D).
   - Precondition: You must have executed at least two motions, and at least one must have occurred at an extreme stage (1 or 7).
   - If the precondition is not met, the system will overrule the request and prompt you to proceed further.
   - If the precondition is met, the system will adjudicate whether your declaration is correct.

Your goals:
1. Infer the true litigation rule scheme H through procedural testing.
2. After correctly declaring, secure the case's final position at the target stage {goal_state}.

Constraints:
- Motion budget / statutory limits are restricted (only counts B/R motions; queries and declarations do not count).
- Please use as few litigation motions as possible to complete the procedure.

Success conditions:
1. Correctly declare the true scheme H within the motion budget.
2. Finally reach the target stage {goal_state} after correct declaration.

Each operation can only contain one tag. Use the following XML format:

- Execute motion B:
<action>B</action>

- Execute motion R:
<action>R</action>

- Query current stage:
<query_state></query_state>

- Declare scheme (e.g., declare scheme A):
<declare>A</declare>

- Submit final closure (after you have correctly declared the scheme and reached the target stage):
<answer>success</answer>
"""

    tags = ["answer", "action", "query_state", "declare"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"init_state": 3, "goal_state": 6, "scheme": "A", "max_actions": 15},
            2: {"init_state": 3, "goal_state": 6, "scheme": "B", "max_actions": 14},
            3: {"init_state": 2, "goal_state": 5, "scheme": "C", "max_actions": 13},
            4: {"init_state": 4, "goal_state": 1, "scheme": "D", "max_actions": 12},
            5: {"init_state": 7, "goal_state": 1, "scheme": "C", "max_actions": 12},
        },
        "en": {
            1: {"init_state": 3, "goal_state": 6, "scheme": "A", "max_actions": 15},
            2: {"init_state": 3, "goal_state": 6, "scheme": "B", "max_actions": 14},
            3: {"init_state": 2, "goal_state": 5, "scheme": "C", "max_actions": 13},
            4: {"init_state": 4, "goal_state": 1, "scheme": "D", "max_actions": 12},
            5: {"init_state": 7, "goal_state": 1, "scheme": "C", "max_actions": 12},
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
        self._game_info["init_state"] = cfg["init_state"]
        self._game_info["goal_state"] = cfg["goal_state"]
        
        self.current_state = cfg["init_state"]
        self.goal_state = cfg["goal_state"]
        self.true_scheme = cfg["scheme"]
        self.max_actions = cfg["max_actions"]
        
        self.action_count = 0
        self.boundary_action_count = 0
        self.declared_correctly = False

    def _apply_transition(self, action, current=None):
        if current is None:
            current = self.current_state
        
        if self.true_scheme == "A":
            if action == "B":
                if current == 7:
                    return 7
                else:
                    return current + 1
            else:
                if current == 1:
                    return 1
                else:
                    return current - 1
        
        elif self.true_scheme == "B":
            if action == "B":
                if current == 1:
                    return 1
                else:
                    return current - 1
            else:
                if current == 7:
                    return 7
                else:
                    return current + 1
        
        elif self.true_scheme == "C":
            if action == "B":
                if current == 7:
                    return 1
                else:
                    return current + 1
            else:
                if current == 1:
                    return 7
                else:
                    return current - 1
        
        elif self.true_scheme == "D":
            if action == "B":
                if current == 1:
                    return 7
                else:
                    return current - 1
            else:
                if current == 7:
                    return 1
                else:
                    return current + 1
        
        return current

    def evaluate(self, parsed_info):
        if "answer" not in parsed_info:
            return False
        
        ans = parsed_info["answer"].strip().lower()
        if ans != "success":
            return False
        
        return self.declared_correctly and self.current_state == self.goal_state

    def _cf_core_produce(self, parsed_info):
        is_zh = self.config.language == "zh"
        
        if "action" in parsed_info:
            action = parsed_info["action"].strip().upper()
            if action not in ["B", "R"]:
                return "错误：动作必须是 B 或 R。" if is_zh else "Error: Action must be B or R."
            
            if self.action_count >= self.max_actions:
                msg = f"动作预算已用尽（{self.max_actions}次）。" if is_zh else f"Action budget exhausted ({self.max_actions} actions)."
                self.state.set_state("failed", "action budget exhausted")
                return msg
            
            if self.current_state in [1, 7]:
                self.boundary_action_count += 1
            
            self.current_state = self._apply_transition(action)
            self.action_count += 1
            
            msg = f"执行动作 {action}。当前状态：{self.current_state}。" if is_zh else f"Action {action} executed. Current state: {self.current_state}."
            
            if self.action_count >= self.max_actions:
                if not self.declared_correctly:
                    self.state.set_state("failed", "action budget exhausted before correct declaration")
                    msg += " 动作预算已用尽，游戏失败。" if is_zh else " Action budget exhausted, game failed."
                elif self.current_state != self.goal_state:
                    self.state.set_state("failed", "action budget exhausted before reaching goal")
                    msg += " 动作预算已用尽，未到达目标，游戏失败。" if is_zh else " Action budget exhausted before reaching goal, game failed."
            
            return msg
        
        if "query_state" in parsed_info:
            return f"当前状态：{self.current_state}。" if is_zh else f"Current state: {self.current_state}."
        
        if "declare" in parsed_info:
            declared = parsed_info["declare"].strip().upper()
            if declared not in ["A", "B", "C", "D"]:
                return "错误：方案必须是 A、B、C 或 D。" if is_zh else "Error: Scheme must be A, B, C, or D."
            
            if self.action_count < 2:
                return "宣告被拒绝：你至少需要执行两次动作。" if is_zh else "Declaration rejected: You must execute at least two actions."
            if self.boundary_action_count < 1:
                return "宣告被拒绝：你至少需要在边界状态（1 或 7）执行一次动作。" if is_zh else "Declaration rejected: You must execute at least one action at a boundary state (1 or 7)."
            
            if declared == self.true_scheme:
                self.declared_correctly = True
                msg = f"宣告正确！真实方案是 {self.true_scheme}。" if is_zh else f"Declaration correct! The true scheme is {self.true_scheme}."
                
                if self.current_state == self.goal_state:
                    msg += " 你已到达目标状态，请提交最终答案。" if is_zh else " You have reached the goal state, please submit your final answer."
                else:
                    msg += f" 现在请移动到目标状态 {self.goal_state}。" if is_zh else f" Now please move to the goal state {self.goal_state}."
                
                return msg
            else:
                self.state.set_state("failed", "incorrect declaration")
                return f"宣告错误。正确方案是 {self.true_scheme}。游戏失败。" if is_zh else f"Declaration incorrect. The correct scheme is {self.true_scheme}. Game failed."
        
        return "错误：未识别的操作。" if is_zh else "Error: Unrecognized operation."

    def _cf_make_wrong(self, correct: str) -> str:
        import re as _re
        
        pattern_en = r'(Current state:\s*)(\d+)'
        pattern_zh = r'(当前状态：)(\d+)'
        
        match = _re.search(pattern_en, correct) or _re.search(pattern_zh, correct)
        if match:
            original_num = int(match.group(2))
            if original_num < 7:
                wrong_num = original_num + 1
            else:
                wrong_num = original_num - 1
            wrong = correct[:match.start(2)] + str(wrong_num) + correct[match.end(2):]
            return wrong
        
        match = _re.search(r'(\d+)', correct)
        if match:
            original_num = int(match.group(1))
            if original_num < 7:
                wrong_num = original_num + 1
            else:
                wrong_num = original_num - 1
            wrong = correct.replace(str(original_num), str(wrong_num), 1)
            return wrong
        
        return correct + " [WRONG]"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        is_zh = self.config.language == "zh"

        for state_val in range(1, 8):
            for action in ["B", "R"]:
                new_state = self._apply_transition(action, current=state_val)
                query_xml = f"<action>{action}</action>"
                if is_zh:
                    answer = f"（当前状态：{state_val}）执行动作 {action}。当前状态：{new_state}。"
                else:
                    answer = f"(Current state: {state_val}) Action {action} executed. Current state: {new_state}."

                results.append({
                    "query": query_xml,
                    "answer": answer
                })

        return results