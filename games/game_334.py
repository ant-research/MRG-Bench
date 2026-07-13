# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   改边权影响：将某边权重修改后，全局最短路是否受影响
# ============================================================

# graph_mode_inference.py

from .base import Game
import math
import re


class GraphModeInferenceGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"图模式推理"游戏，规则如下：

游戏设定了一个无向加权图，权重均为正整数。节点包括：S（源点）、A、B、C、D、T（汇点）。

初始边及权重（基线图）：
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

在基线图中，从S到T的最短路径成本为 {baseline_cost}，最短路径集合为 {baseline_paths}。

游戏中存在六条候选路径：
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

可调整的边仅限于：{adjustable_edges_str}

我已秘密选择了一种"模式"（A、B或C之一），该模式决定了边权重如何变化：
- 减少操作：权重按特定规则减小（但不低于1）
- 增加操作：权重按特定规则增大

你可以进行以下操作：

1. 试运行：选择一条可调整边和一种操作（减少/增加），我会告诉你操作后的最短成本、最短路径集合（用P1-P6标识），以及该边是否出现在最短路径上。注意：每次试运行后图会立即重置为基线，多次试运行互不影响。

2. 复述基线：我会重新告诉你基线图的最短成本和最短路径集合。

3. 提交答案：当你确定模式后，需要宣判模式（A、B或C）并执行一次边操作，使得路径 {target_path} 成为执行后图的最短路径之一（可以与其他路径并列）。

## 操作格式（必须严格遵守）

试运行查询（例如对边S-C执行减少操作）：
<query_trial>S-C,减少</query_trial>

复述基线：
<query_baseline></query_baseline>

提交最终答案（例如宣判模式为A，对边S-B执行增加操作）：
<answer>mode=A,edge=S-B,op=增加</answer>

注意：
- 边名称使用连字符连接两个节点，如"S-C"、"B-T"等
- 操作只能是"减少"或"增加"
- 每次只能包含一个标签
- 试运行次数应尽可能少

你的目标是：
1. 正确识别隐藏的模式（A、B或C）
2. 给出一次边操作，使 {target_path} 成为最短路径之一
"""

    game_rule_en = """\
Let's play a "Graph Mode Inference" game. Here are the rules:

The game features an undirected weighted graph with positive integer weights. Nodes include: S (source), A, B, C, D, T (sink).

Initial edges and weights (baseline graph):
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

In the baseline graph, the shortest path cost from S to T is {baseline_cost}, and the shortest path set is {baseline_paths}.

There are six candidate paths in the game:
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

Adjustable edges are limited to: {adjustable_edges_str}

I have secretly selected a "mode" (A, B, or C), which determines how edge weights change:
- Decrease operation: weight decreases according to specific rules (but not below 1)
- Increase operation: weight increases according to specific rules

You can perform the following operations:

1. Trial run: Select an adjustable edge and an operation (decrease/increase). I will tell you the resulting shortest cost, shortest path set (identified by P1-P6), and whether the edge appears in the shortest paths. Note: After each trial, the graph immediately resets to baseline; trials do not stack.

2. Repeat baseline: I will remind you of the baseline graph's shortest cost and path set.

3. Submit answer: When you determine the mode, declare the mode (A, B, or C) and execute one edge operation to make path {target_path} one of the shortest paths (can be tied with others).

## Operation Format (must strictly follow)

Trial query (e.g., decrease edge S-C):
<query_trial>S-C,decrease</query_trial>

Repeat baseline:
<query_baseline></query_baseline>

Submit final answer (e.g., declare mode A, increase edge S-B):
<answer>mode=A,edge=S-B,op=increase</answer>

Notes:
- Edge names use hyphen to connect two nodes, e.g., "S-C", "B-T"
- Operation can only be "decrease" or "increase"
- Each query must contain only one tag
- Number of trials should be minimized

Your goals are:
1. Correctly identify the hidden mode (A, B, or C)
2. Provide one edge operation to make {target_path} one of the shortest paths
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通路网调度系统”。你是一名城市交通规划师，需要优化从起点（S）到终点（T）的通勤时间。

系统设定了一个无向加权路网图，权重代表通行时间（单位：分钟，均为正整数）。交叉路口包括：S（起点）、A、B、C、D、T（终点）。

初始路段及通行时间（基线路网）：
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

在基线路网中，从S到T的最短通勤时间为 {baseline_cost}，最快路线集合为 {baseline_paths}。

路网中存在六条主要通勤路线：
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

可实施交通干预（扩建或限行）的路段仅限于：{adjustable_edges_str}

系统已秘密设定了一种“交通演变模式”（A、B或C之一），该模式决定了干预措施如何影响通行时间：
- 减少操作（道路扩建）：通行时间按特定规则减小（但不低于1分钟）
- 增加操作（施工限行）：通行时间按特定规则增大

你可以进行以下操作：

1. 试运行：选择一条可干预路段和一种操作（减少/增加），我会告诉你操作后的最短通勤时间、最快路线集合（用P1-P6标识），以及该路段是否出现在最快路线上。注意：每次试运行后路网会立即重置为基线，多次试运行互不影响。

2. 复述基线：我会重新告诉你基线路网的最短通勤时间和最快路线集合。

3. 提交答案：当你确定交通演变模式后，需要宣判模式（A、B或C）并执行一次路段操作，使得路线 {target_path} 成为执行后路网的最快路线之一（可以与其他路线并列）。

## 操作格式（必须严格遵守）

试运行查询（例如对路段S-C执行减少操作）：
<query_trial>S-C,减少</query_trial>

复述基线：
<query_baseline></query_baseline>

提交最终答案（例如宣判模式为A，对路段S-B执行增加操作）：
<answer>mode=A,edge=S-B,op=增加</answer>

注意：
- 路段名称使用连字符连接两个节点，如"S-C"、"B-T"等
- 操作只能是"减少"或"增加"
- 每次只能包含一个标签
- 试运行次数应尽可能少

你的目标是：
1. 正确识别隐藏的交通演变模式（A、B或C）
2. 给出一次干预操作，使 {target_path} 成为最快路线之一
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Dispatch System." You are an urban traffic planner tasked with optimizing the commute time from the starting point (S) to the destination (T).

The system features an undirected weighted road network graph, where weights represent travel time (in minutes, all positive integers). Intersections include: S (start), A, B, C, D, T (destination).

Initial road segments and travel times (baseline network):
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

In the baseline network, the shortest commute time from S to T is {baseline_cost}, and the fastest route set is {baseline_paths}.

There are six major commute routes in the network:
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

Road segments adjustable via traffic interventions (expansion or restriction) are limited to: {adjustable_edges_str}

The system has secretly selected a "traffic evolution mode" (A, B, or C), which determines how interventions affect travel times:
- Decrease operation (road expansion): time decreases according to specific rules (but not below 1 minute)
- Increase operation (construction restriction): time increases according to specific rules

You can perform the following operations:

1. Trial run: Select an adjustable segment and an operation (decrease/increase). I will tell you the resulting shortest commute time, fastest route set (identified by P1-P6), and whether the segment appears in the fastest routes. Note: After each trial, the network immediately resets to baseline; trials do not stack.

2. Repeat baseline: I will remind you of the baseline network's shortest commute time and fastest route set.

3. Submit answer: When you determine the evolution mode, declare the mode (A, B, or C) and execute one segment operation to make route {target_path} one of the fastest routes in the resulting network (can be tied with others).

## Operation Format (must strictly follow)

Trial query (e.g., decrease segment S-C):
<query_trial>S-C,decrease</query_trial>

Repeat baseline:
<query_baseline></query_baseline>

Submit final answer (e.g., declare mode A, increase segment S-B):
<answer>mode=A,edge=S-B,op=increase</answer>

Notes:
- Segment names use hyphen to connect two nodes, e.g., "S-C", "B-T"
- Operation can only be "decrease" or "increase"
- Each query must contain only one tag
- Number of trials should be minimized

Your goals are:
1. Correctly identify the hidden traffic evolution mode (A, B, or C)
2. Provide one intervention operation to make {target_path} one of the fastest routes
"""

    contextualized_rule_zh_2 = """\
欢迎使用“临床诊疗路径推演系统”。你是一名主治医师，需要为患者规划从确诊状态（S）到完全康复（T）的最佳治疗方案。

系统设定了一个无向加权疾病进展图，权重代表各治疗阶段的康复周期（单位：天，均为正整数）。阶段节点包括：S（确诊）、A、B、C、D、T（康复）。

初始干预手段及康复周期（基线状态）：
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

在基线状态中，从S到T的最短康复周期为 {baseline_cost} 天，最佳治疗路径集合为 {baseline_paths}。

临床上存在六条候选治疗路径：
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

允许调整用药剂量的干预阶段仅限于：{adjustable_edges_str}

患者体质隐藏着一种“药物反应模式”（A、B或C之一），该模式决定了剂量调整如何影响康复周期：
- 减少操作（增加特效药剂量）：周期按特定规则缩短（但不低于1天）
- 增加操作（采取保守减量）：周期按特定规则延长

你可以进行以下操作：

1. 试运行：选择一个可调整阶段和一种操作（减少/增加），我会告诉你操作后的最短康复周期、最佳治疗路径集合（用P1-P6标识），以及该阶段是否出现在最佳路径上。注意：每次试运行后患者状态会立即重置为基线，多次试运行互不影响。

2. 复述基线：我会重新告诉你基线状态的最短康复周期和最佳路径集合。

3. 提交答案：当你确定药物反应模式后，需要宣判模式（A、B或C）并执行一次剂量操作，使得治疗路径 {target_path} 成为执行后临床的最短路径之一（可以与其他路径并列）。

## 操作格式（必须严格遵守）

试运行查询（例如对阶段S-C执行减少操作）：
<query_trial>S-C,减少</query_trial>

复述基线：
<query_baseline></query_baseline>

提交最终答案（例如宣判模式为A，对阶段S-B执行增加操作）：
<answer>mode=A,edge=S-B,op=增加</answer>

注意：
- 阶段名称使用连字符连接两个节点，如"S-C"、"B-T"等
- 操作只能是"减少"或"增加"
- 每次只能包含一个标签
- 试运行次数应尽可能少

你的目标是：
1. 正确识别隐藏的药物反应模式（A、B或C）
2. 给出一次剂量调整操作，使 {target_path} 成为最短康复路径之一
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Pathway Deduction System." You are an attending physician tasked with planning the optimal treatment plan from diagnosis (S) to full recovery (T) for a patient.

The system features an undirected weighted disease progression graph, where weights represent the recovery cycle of each treatment stage (in days, all positive integers). Stage nodes include: S (diagnosis), A, B, C, D, T (recovery).

Initial interventions and recovery cycles (baseline state):
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

In the baseline state, the shortest recovery cycle from S to T is {baseline_cost} days, and the optimal clinical pathway set is {baseline_paths}.

There are six candidate clinical pathways:
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

Treatment stages where dosage adjustments are permitted are limited to: {adjustable_edges_str}

The patient's constitution hides a "drug response mode" (A, B, or C), which determines how dosage adjustments affect the recovery cycle:
- Decrease operation (increase specific drug dose): cycle shortens according to specific rules (but not below 1 day)
- Increase operation (conservative dose reduction): cycle lengthens according to specific rules

You can perform the following operations:

1. Trial run: Select an adjustable stage and an operation (decrease/increase). I will tell you the resulting shortest recovery cycle, optimal pathway set (identified by P1-P6), and whether the stage appears in the optimal pathways. Note: After each trial, the patient's state immediately resets to baseline; trials do not stack.

2. Repeat baseline: I will remind you of the baseline state's shortest recovery cycle and optimal pathway set.

3. Submit answer: When you determine the drug response mode, declare the mode (A, B, or C) and execute one dosage operation to make pathway {target_path} one of the optimal pathways in the resulting clinical state (can be tied with others).

## Operation Format (must strictly follow)

Trial query (e.g., decrease stage S-C):
<query_trial>S-C,decrease</query_trial>

Repeat baseline:
<query_baseline></query_baseline>

Submit final answer (e.g., declare mode A, increase stage S-B):
<answer>mode=A,edge=S-B,op=increase</answer>

Notes:
- Stage names use hyphen to connect two nodes, e.g., "S-C", "B-T"
- Operation can only be "decrease" or "increase"
- Each query must contain only one tag
- Number of trials should be minimized

Your goals are:
1. Correctly identify the hidden drug response mode (A, B, or C)
2. Provide one dosage adjustment operation to make {target_path} one of the shortest recovery pathways
"""

    contextualized_rule_zh_3 = """\
欢迎进入“自适应学习路径规划引擎”。你是一名教研专家，需要为学生定制从零基础（S）到掌握核心技能（T）的最优学习路线。

系统设定了一个无向加权知识图谱，权重代表掌握特定模块组合所需的课时（单位：小时，均为正整数）。知识节点包括：S（零基础）、A、B、C、D、T（精通）。

初始学习模块及所需课时（基线图谱）：
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

在基线图谱中，从S到T的最少学习课时为 {baseline_cost}，最快学习路线集合为 {baseline_paths}。

系统中存在六条可选的完整学习路线：
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

可进行教学干预的模块衔接仅限于：{adjustable_edges_str}

该学生具备一种隐藏的“认知吸收模式”（A、B或C之一），该模式决定了教学干预如何影响学习课时：
- 减少操作（提供一对一辅导）：课时按特定规则减小（但不低于1小时）
- 增加操作（布置拓展自学任务）：课时按特定规则增大

你可以进行以下操作：

1. 试运行：选择一条可干预模块衔接和一种操作（减少/增加），我会告诉你操作后的最少课时、最快路线集合（用P1-P6标识），以及该模块衔接是否出现在最快路线上。注意：每次试运行后图谱会立即重置为基线，多次试运行互不影响。

2. 复述基线：我会重新告诉你基线图谱的最少课时和最快路线集合。

3. 提交答案：当你确定认知吸收模式后，需要宣判模式（A、B或C）并执行一次教学操作，使得学习路线 {target_path} 成为执行后图谱的最快路线之一（可以与其他路线并列）。

## 操作格式（必须严格遵守）

试运行查询（例如对模块衔接S-C执行减少操作）：
<query_trial>S-C,减少</query_trial>

复述基线：
<query_baseline></query_baseline>

提交最终答案（例如宣判模式为A，对模块衔接S-B执行增加操作）：
<answer>mode=A,edge=S-B,op=增加</answer>

注意：
- 衔接名称使用连字符连接两个节点，如"S-C"、"B-T"等
- 操作只能是"减少"或"增加"
- 每次只能包含一个标签
- 试运行次数应尽可能少

你的目标是：
1. 正确识别隐藏的认知吸收模式（A、B或C）
2. 给出一次教学干预操作，使 {target_path} 成为最快学习路线之一
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Planning Engine." You are an educational research expert tasked with customizing the optimal learning route for a student from zero foundation (S) to mastering core skills (T).

The system features an undirected weighted knowledge graph, where weights represent the learning hours required to master specific module transitions (in hours, all positive integers). Knowledge nodes include: S (zero foundation), A, B, C, D, T (mastery).

Initial learning modules and required hours (baseline graph):
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

In the baseline graph, the minimum learning hours from S to T is {baseline_cost}, and the fastest route set is {baseline_paths}.

There are six optional complete learning routes in the system:
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

Module transitions adjustable via teaching interventions are limited to: {adjustable_edges_str}

The student possesses a hidden "cognitive absorption mode" (A, B, or C), which determines how teaching interventions affect learning hours:
- Decrease operation (provide one-on-one tutoring): hours decrease according to specific rules (but not below 1 hour)
- Increase operation (assign extended self-study tasks): hours increase according to specific rules

You can perform the following operations:

1. Trial run: Select an adjustable module transition and an operation (decrease/increase). I will tell you the resulting minimum hours, fastest route set (identified by P1-P6), and whether the transition appears in the fastest routes. Note: After each trial, the graph immediately resets to baseline; trials do not stack.

2. Repeat baseline: I will remind you of the baseline graph's minimum hours and fastest route set.

3. Submit answer: When you determine the cognitive absorption mode, declare the mode (A, B, or C) and execute one teaching operation to make route {target_path} one of the fastest routes in the resulting graph (can be tied with others).

## Operation Format (must strictly follow)

Trial query (e.g., decrease transition S-C):
<query_trial>S-C,decrease</query_trial>

Repeat baseline:
<query_baseline></query_baseline>

Submit final answer (e.g., declare mode A, increase transition S-B):
<answer>mode=A,edge=S-B,op=increase</answer>

Notes:
- Transition names use hyphen to connect two nodes, e.g., "S-C", "B-T"
- Operation can only be "decrease" or "increase"
- Each query must contain only one tag
- Number of trials should be minimized

Your goals are:
1. Correctly identify the hidden cognitive absorption mode (A, B, or C)
2. Provide one teaching intervention operation to make {target_path} one of the fastest learning routes
"""

    contextualized_rule_zh_4 = """\
欢迎进入“智能制造柔性排产系统”。你是一名工艺工程师，需要优化从原材料投料（S）到成品入库（T）的生产周期。

系统设定了一个无向加权工艺流程图，权重代表各生产工序的加工工时（单位：小时，均为正整数）。车间节点包括：S（投料）、A、B、C、D、T（入库）。

初始工序及加工工时（基线排产）：
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

在基线排产中，从S到T的最短生产周期为 {baseline_cost} 小时，最快流水线集合为 {baseline_paths}。

车间内存在六条候选的生产流水线：
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

可进行参数调整的生产工序仅限于：{adjustable_edges_str}

生产线设备受一种隐藏的“效能波动模式”（A、B或C之一）影响，该模式决定了参数调整如何改变加工工时：
- 减少操作（超频运转/工艺优化）：工时按特定规则缩短（但不低于1小时）
- 增加操作（设备保养/降频运转）：工时按特定规则延长

你可以进行以下操作：

1. 试运行：选择一条可调整工序和一种操作（减少/增加），我会告诉你操作后的最短生产周期、最快流水线集合（用P1-P6标识），以及该工序是否出现在最快流水线上。注意：每次试运行后产线参数会立即重置为基线，多次试运行互不影响。

2. 复述基线：我会重新告诉你基线排产的最短生产周期和最快流水线集合。

3. 提交答案：当你确定效能波动模式后，需要宣判模式（A、B或C）并执行一次工序操作，使得流水线 {target_path} 成为执行后排产的最快流水线之一（可以与其他流水线并列）。

## 操作格式（必须严格遵守）

试运行查询（例如对工序S-C执行减少操作）：
<query_trial>S-C,减少</query_trial>

复述基线：
<query_baseline></query_baseline>

提交最终答案（例如宣判模式为A，对工序S-B执行增加操作）：
<answer>mode=A,edge=S-B,op=增加</answer>

注意：
- 工序名称使用连字符连接两个节点，如"S-C"、"B-T"等
- 操作只能是"减少"或"增加"
- 每次只能包含一个标签
- 试运行次数应尽可能少

你的目标是：
1. 正确识别隐藏的效能波动模式（A、B或C）
2. 给出一次工序参数调整操作，使 {target_path} 成为最快生产流水线之一
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Intelligent Manufacturing Flexible Scheduling System." You are a process engineer tasked with optimizing the production cycle from raw material feeding (S) to finished product storage (T).

The system features an undirected weighted process flow graph, where weights represent the processing hours of each production step (in hours, all positive integers). Workshop nodes include: S (feeding), A, B, C, D, T (storage).

Initial process steps and processing hours (baseline schedule):
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

In the baseline schedule, the shortest production cycle from S to T is {baseline_cost} hours, and the fastest assembly line set is {baseline_paths}.

There are six candidate production assembly lines in the workshop:
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

Production steps adjustable via parameter tuning are limited to: {adjustable_edges_str}

The production line equipment is influenced by a hidden "efficiency fluctuation mode" (A, B, or C), which determines how parameter tuning changes processing hours:
- Decrease operation (overclocking/process optimization): hours shorten according to specific rules (but not below 1 hour)
- Increase operation (equipment maintenance/underclocking): hours lengthen according to specific rules

You can perform the following operations:

1. Trial run: Select an adjustable step and an operation (decrease/increase). I will tell you the resulting shortest production cycle, fastest assembly line set (identified by P1-P6), and whether the step appears in the fastest lines. Note: After each trial, line parameters immediately reset to baseline; trials do not stack.

2. Repeat baseline: I will remind you of the baseline schedule's shortest production cycle and fastest assembly line set.

3. Submit answer: When you determine the efficiency fluctuation mode, declare the mode (A, B, or C) and execute one step operation to make assembly line {target_path} one of the fastest lines in the resulting schedule (can be tied with others).

## Operation Format (must strictly follow)

Trial query (e.g., decrease step S-C):
<query_trial>S-C,decrease</query_trial>

Repeat baseline:
<query_baseline></query_baseline>

Submit final answer (e.g., declare mode A, increase step S-B):
<answer>mode=A,edge=S-B,op=increase</answer>

Notes:
- Step names use hyphen to connect two nodes, e.g., "S-C", "B-T"
- Operation can only be "decrease" or "increase"
- Each query must contain only one tag
- Number of trials should be minimized

Your goals are:
1. Correctly identify the hidden efficiency fluctuation mode (A, B, or C)
2. Provide one process parameter tuning operation to make {target_path} one of the fastest production assembly lines
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法诉讼程序推演工具”。你是一名资深律师，需要为当事人规划从立案（S）到最终结案（T）的最优诉讼策略。

工具设定了一个无向加权法律程序流转图，权重代表各程序阶段的审理耗时（单位：周，均为正整数）。程序节点包括：S（立案）、A、B、C、D、T（结案）。

初始程序流转及耗时（基线流转）：
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

在基线流转中，从S到T的最短结案耗时为 {baseline_cost} 周，最高效诉讼路线集合为 {baseline_paths}。

实务中存在六条可选的诉讼策略路线：
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

可通过法律手段干预的程序阶段仅限于：{adjustable_edges_str}

该管辖区法院存在一种隐藏的“司法审查模式”（A、B或C之一），该模式决定了法律手段干预如何影响程序耗时：
- 减少操作（申请适用简易程序）：耗时按特定规则缩短（但不低于1周）
- 增加操作（提出管辖权异议/延期举证）：耗时按特定规则延长

你可以进行以下操作：

1. 试运行：选择一个可干预程序阶段和一种操作（减少/增加），我会告诉你操作后的最短结案耗时、最高效路线集合（用P1-P6标识），以及该程序是否出现在最高效路线上。注意：每次试运行后法院状态会立即重置为基线，多次试运行互不影响。

2. 复述基线：我会重新告诉你基线流转的最短结案耗时和最高效路线集合。

3. 提交答案：当你确定司法审查模式后，需要宣判模式（A、B或C）并执行一次程序干预，使得诉讼路线 {target_path} 成为执行后流转的最高效路线之一（可以与其他路线并列）。

## 操作格式（必须严格遵守）

试运行查询（例如对程序S-C执行减少操作）：
<query_trial>S-C,减少</query_trial>

复述基线：
<query_baseline></query_baseline>

提交最终答案（例如宣判模式为A，对程序S-B执行增加操作）：
<answer>mode=A,edge=S-B,op=增加</answer>

注意：
- 程序名称使用连字符连接两个节点，如"S-C"、"B-T"等
- 操作只能是"减少"或"增加"
- 每次只能包含一个标签
- 试运行次数应尽可能少

你的目标是：
1. 正确识别隐藏的司法审查模式（A、B或C）
2. 给出一次法律干预操作，使 {target_path} 成为最高效诉讼路线之一
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Litigation Procedure Deduction Tool." You are a senior lawyer tasked with planning the optimal litigation strategy for your client from case filing (S) to final settlement (T).

The tool features an undirected weighted legal procedure flow graph, where weights represent the trial time of each procedural stage (in weeks, all positive integers). Procedure nodes include: S (filing), A, B, C, D, T (settlement).

Initial procedural flows and times (baseline flow):
- S-A: 3
- A-T: 6
- S-B: 4
- B-T: 4
- S-C: 2
- C-D: 4
- D-T: 4
- A-B: 1
- B-C: 1
- C-A: 4
- B-D: 3

In the baseline flow, the shortest settlement time from S to T is {baseline_cost} weeks, and the most efficient litigation route set is {baseline_paths}.

In practice, there are six optional litigation strategy routes:
- P1: S-C-B-T
- P2: S-B-T
- P3: S-A-B-T
- P4: S-A-T
- P5: S-C-D-T
- P6: S-B-D-T

Procedural stages adjustable via legal interventions are limited to: {adjustable_edges_str}

The jurisdiction's court exhibits a hidden "judicial review mode" (A, B, or C), which determines how legal interventions affect procedural time:
- Decrease operation (apply for summary procedure): time shortens according to specific rules (but not below 1 week)
- Increase operation (raise jurisdictional objection/extend evidence presentation): time lengthens according to specific rules

You can perform the following operations:

1. Trial run: Select an adjustable procedural stage and an operation (decrease/increase). I will tell you the resulting shortest settlement time, most efficient route set (identified by P1-P6), and whether the procedure appears in the most efficient routes. Note: After each trial, the court state immediately resets to baseline; trials do not stack.

2. Repeat baseline: I will remind you of the baseline flow's shortest settlement time and most efficient route set.

3. Submit answer: When you determine the judicial review mode, declare the mode (A, B, or C) and execute one procedural intervention to make litigation route {target_path} one of the most efficient routes in the resulting flow (can be tied with others).

## Operation Format (must strictly follow)

Trial query (e.g., decrease procedure S-C):
<query_trial>S-C,decrease</query_trial>

Repeat baseline:
<query_baseline></query_baseline>

Submit final answer (e.g., declare mode A, increase procedure S-B):
<answer>mode=A,edge=S-B,op=increase</answer>

Notes:
- Procedure names use hyphen to connect two nodes, e.g., "S-C", "B-T"
- Operation can only be "decrease" or "increase"
- Each query must contain only one tag
- Number of trials should be minimized

Your goals are:
1. Correctly identify the hidden judicial review mode (A, B, or C)
2. Provide one legal intervention operation to make {target_path} one of the most efficient litigation routes
"""

    tags = ["answer", "query_trial", "query_baseline"]

    # 难度配置：
    # 1 (简单)         - 模式A，目标P2，较明显的权重变化
    # 2 (中等偏下)     - 模式B，目标P2，倍增模式
    # 3 (中等偏上)     - 模式C，目标P2，极端模式
    # 4 (较难)         - 模式A，目标P3，需要更精细的调整
    # 5 (难)           - 模式B，目标P6，复杂的路径关系

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "mode": "A",
                "target_path": "P2",
                "adjustable_edges": ["S-C", "B-C", "B-T", "S-B"],
                "baseline_cost": 7,
                "baseline_paths": ["P1"],
            },
            2: {
                "mode": "B",
                "target_path": "P2",
                "adjustable_edges": ["S-C", "B-C", "B-T", "S-B"],
                "baseline_cost": 7,
                "baseline_paths": ["P1"],
            },
            3: {
                "mode": "C",
                "target_path": "P2",
                "adjustable_edges": ["S-C", "B-C", "B-T", "S-B"],
                "baseline_cost": 7,
                "baseline_paths": ["P1"],
            },
            4: {
                "mode": "A",
                "target_path": "P3",
                "adjustable_edges": ["S-C", "B-C", "B-T", "S-B"],
                "baseline_cost": 7,
                "baseline_paths": ["P1"],
            },
            5: {
                "mode": "B",
                "target_path": "P6",
                "adjustable_edges": ["S-C", "B-C", "B-T", "S-B"],
                "baseline_cost": 7,
                "baseline_paths": ["P1"],
            },
        },
        "en": {
            1: {
                "mode": "A",
                "target_path": "P2",
                "adjustable_edges": ["S-C", "B-C", "B-T", "S-B"],
                "baseline_cost": 7,
                "baseline_paths": ["P1"],
            },
            2: {
                "mode": "B",
                "target_path": "P2",
                "adjustable_edges": ["S-C", "B-C", "B-T", "S-B"],
                "baseline_cost": 7,
                "baseline_paths": ["P1"],
            },
            3: {
                "mode": "C",
                "target_path": "P2",
                "adjustable_edges": ["S-C", "B-C", "B-T", "S-B"],
                "baseline_cost": 7,
                "baseline_paths": ["P1"],
            },
            4: {
                "mode": "A",
                "target_path": "P3",
                "adjustable_edges": ["S-C", "B-C", "B-T", "S-B"],
                "baseline_cost": 7,
                "baseline_paths": ["P1"],
            },
            5: {
                "mode": "B",
                "target_path": "P6",
                "adjustable_edges": ["S-C", "B-C", "B-T", "S-B"],
                "baseline_cost": 7,
                "baseline_paths": ["P1"],
            },
        },
    }

    # 基线图的边权重
    BASELINE_EDGES = {
        ("S", "A"): 3,
        ("A", "T"): 6,
        ("S", "B"): 4,
        ("B", "T"): 4,
        ("S", "C"): 2,
        ("C", "D"): 4,
        ("D", "T"): 4,
        ("A", "B"): 1,
        ("B", "C"): 1,
        ("C", "A"): 4,
        ("B", "D"): 3,
    }

    # 候选路径定义
    PATHS = {
        "P1": [("S", "C"), ("C", "B"), ("B", "T")],
        "P2": [("S", "B"), ("B", "T")],
        "P3": [("S", "A"), ("A", "B"), ("B", "T")],
        "P4": [("S", "A"), ("A", "T")],
        "P5": [("S", "C"), ("C", "D"), ("D", "T")],
        "P6": [("S", "B"), ("B", "D"), ("D", "T")],
    }

    def __init__(self, config):
        self.trial_count = 0  # 试运行计数器
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 保存游戏配置
        self.hidden_mode = cfg["mode"]
        self.target_path = cfg["target_path"]
        self.adjustable_edges = cfg["adjustable_edges"]
        
        # 初始化当前图（从基线复制）
        self.current_edges = dict(self.BASELINE_EDGES)
        
        # 为游戏规则准备信息
        self._game_info["baseline_cost"] = cfg["baseline_cost"]
        self._game_info["baseline_paths"] = ", ".join(cfg["baseline_paths"])
        self._game_info["target_path"] = self.target_path
        
        if lang == "zh":
            self._game_info["adjustable_edges_str"] = "、".join(self.adjustable_edges)
        else:
            self._game_info["adjustable_edges_str"] = ", ".join(self.adjustable_edges)

    def _normalize_edge(self, edge_str):
        """标准化边表示（无向图，确保一致性）"""
        parts = edge_str.strip().split("-")
        if len(parts) != 2:
            return None
        a, b = parts[0].strip(), parts[1].strip()
        # 无向图：统一按字典序排列
        if (a, b) in self.BASELINE_EDGES:
            return (a, b)
        elif (b, a) in self.BASELINE_EDGES:
            return (b, a)
        return None

    def _apply_mode_operation(self, weight, operation):
        """根据隐藏模式应用权重变化"""
        if self.hidden_mode == "A":
            # 模式A：均匀
            if operation == "decrease" or operation == "减少":
                return max(1, weight - 1)
            else:  # increase/增加
                return weight + 1
        elif self.hidden_mode == "B":
            # 模式B：倍增
            if operation == "decrease" or operation == "减少":
                return math.ceil(weight / 2)
            else:  # increase/增加
                return weight * 2
        elif self.hidden_mode == "C":
            # 模式C：极端
            if operation == "decrease" or operation == "减少":
                return 1 if weight > 1 else 1
            else:  # increase/增加
                return weight + 2
        return weight

    def _calculate_path_cost(self, path_edges, edge_weights):
        """计算路径成本"""
        cost = 0
        for edge in path_edges:
            a, b = edge
            if (a, b) in edge_weights:
                cost += edge_weights[(a, b)]
            elif (b, a) in edge_weights:
                cost += edge_weights[(b, a)]
            else:
                return float('inf')
        return cost

    def _find_shortest_paths(self, edge_weights):
        """找到所有最短路径及其成本"""
        path_costs = {}
        for path_name, path_edges in self.PATHS.items():
            path_costs[path_name] = self._calculate_path_cost(path_edges, edge_weights)
        
        min_cost = min(path_costs.values())
        shortest_paths = [p for p, c in path_costs.items() if c == min_cost]
        return min_cost, shortest_paths

    def _edge_in_paths(self, edge, path_list):
        """检查边是否出现在给定路径列表中的任一路径"""
        a, b = edge
        for path_name in path_list:
            path_edges = self.PATHS[path_name]
            for pe in path_edges:
                if (pe == (a, b)) or (pe == (b, a)):
                    return True
        return False

    def evaluate(self, parsed_info):
        """评估最终答案"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案格式：mode=X,edge=Y,op=Z
        parts = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        # 检查必需字段
        if "mode" not in ans_dict or "edge" not in ans_dict or "op" not in ans_dict:
            return False
        
        declared_mode = ans_dict["mode"]
        edge_str = ans_dict["edge"]
        operation = ans_dict["op"]
        
        # 1. 检查模式是否正确
        if declared_mode != self.hidden_mode:
            return False
        
        # 2. 标准化边
        edge = self._normalize_edge(edge_str)
        if edge is None:
            return False
        
        # 3. 检查边是否可调整
        if edge_str not in self.adjustable_edges:
            # 尝试反向
            reversed_edge = "-".join(reversed(edge_str.split("-")))
            if reversed_edge not in self.adjustable_edges:
                return False
        
        # 4. 执行操作并计算结果
        test_edges = dict(self.BASELINE_EDGES)
        old_weight = test_edges[edge]
        new_weight = self._apply_mode_operation(old_weight, operation)
        test_edges[edge] = new_weight
        
        # 5. 检查目标路径是否在最短路径集合中
        _, shortest_paths = self._find_shortest_paths(test_edges)
        return self.target_path in shortest_paths

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        is_zh = (self.config.language == "zh")
        
        # 处理复述基线
        if "query_baseline" in parsed_info:
            if is_zh:
                return f"基线图的最短成本为 {self._game_info['baseline_cost']}，最短路径集合为 {self._game_info['baseline_paths']}。"
            else:
                return f"The baseline graph has shortest cost {self._game_info['baseline_cost']} and shortest path set {self._game_info['baseline_paths']}."
        
        # 处理试运行
        if "query_trial" in parsed_info:
            self.trial_count += 1
            
            raw = parsed_info["query_trial"]
            parts = [x.strip() for x in raw.split(",")]
            if len(parts) != 2:
                if is_zh:
                    return "错误：格式无效。应为'边,操作'。"
                else:
                    return "Error: Invalid format. Should be 'edge,operation'."
            
            edge_str, operation = parts[0], parts[1]
            
            # 标准化边
            edge = self._normalize_edge(edge_str)
            if edge is None:
                if is_zh:
                    return "错误：无效的边。"
                else:
                    return "Error: Invalid edge."
            
            # 检查边是否可调整
            if edge_str not in self.adjustable_edges:
                reversed_edge = "-".join(reversed(edge_str.split("-")))
                if reversed_edge not in self.adjustable_edges:
                    if is_zh:
                        return f"错误：边 {edge_str} 不可调整。"
                    else:
                        return f"Error: Edge {edge_str} is not adjustable."
            
            # 应用操作（在基线图上）
            test_edges = dict(self.BASELINE_EDGES)
            old_weight = test_edges[edge]
            new_weight = self._apply_mode_operation(old_weight, operation)
            test_edges[edge] = new_weight
            
            # 计算最短路径
            min_cost, shortest_paths = self._find_shortest_paths(test_edges)
            
            # 检查边是否在最短路径上
            edge_in_shortest = self._edge_in_paths(edge, shortest_paths)
            
            # 构建响应
            paths_str = ", ".join(shortest_paths)
            if is_zh:
                in_path_str = "是" if edge_in_shortest else "否"
                return f"最短成本：{min_cost}\n最短路径集合：{paths_str}\n所选边是否在最短路径上：{in_path_str}"
            else:
                in_path_str = "Yes" if edge_in_shortest else "No"
                return f"Shortest cost: {min_cost}\nShortest path set: {paths_str}\nIs selected edge in shortest paths: {in_path_str}"
        
        # 不应到达这里
        raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        is_zh = (self.config.language == "zh")
        
        # 1. Baseline query
        baseline_ans = ""
        if is_zh:
            baseline_ans = f"基线图的最短成本为 {self._game_info['baseline_cost']}，最短路径集合为 {self._game_info['baseline_paths']}。"
        else:
            baseline_ans = f"The baseline graph has shortest cost {self._game_info['baseline_cost']} and shortest path set {self._game_info['baseline_paths']}."
            
        queries.append({
            "query": "<query_baseline></query_baseline>",
            "answer": baseline_ans
        })
        
        # 2. Trial queries
        # Define operations based on language
        ops = ["减少", "增加"] if is_zh else ["decrease", "increase"]
        
        for edge_str in self.adjustable_edges:
            for op in ops:
                # Logic copied from _cf_core_produce to ensure consistency without side effects
                # Normalize edge
                edge = self._normalize_edge(edge_str)
                # Note: edge is guaranteed valid as it comes from adjustable_edges
                
                # Apply operation on baseline
                test_edges = dict(self.BASELINE_EDGES)
                old_weight = test_edges[edge]
                new_weight = self._apply_mode_operation(old_weight, op)
                test_edges[edge] = new_weight
                
                # Calculate shortest paths
                min_cost, shortest_paths = self._find_shortest_paths(test_edges)
                edge_in_shortest = self._edge_in_paths(edge, shortest_paths)
                
                paths_str = ", ".join(shortest_paths)
                
                # Format answer
                if is_zh:
                    in_path_str = "是" if edge_in_shortest else "否"
                    ans = f"最短成本：{min_cost}\n最短路径集合：{paths_str}\n所选边是否在最短路径上：{in_path_str}"
                else:
                    in_path_str = "Yes" if edge_in_shortest else "No"
                    ans = f"Shortest cost: {min_cost}\nShortest path set: {paths_str}\nIs selected edge in shortest paths: {in_path_str}"
                
                queries.append({
                    "query": f"<query_trial>{edge_str},{op}</query_trial>",
                    "answer": ans
                })
                
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个与正确答案不同的错误答案，用于反事实干预"""
        if self.config.language == "zh":
            # 仅替换最后一个"是"或"否"（即回答部分），避免替换问句中的"是否"
            if correct.rstrip().endswith("是"):
                return correct.rstrip()[:-1] + "否"
            elif correct.rstrip().endswith("否"):
                return correct.rstrip()[:-1] + "是"
            # 尝试修改最短成本数字
            m = re.search(r'最短成本[：:]\s*(\d+)', correct)
            if m:
                old_val = int(m.group(1))
                new_val = old_val + 1
                return correct.replace(m.group(1), str(new_val), 1)
        else:
            # 英文：仅替换 "Is selected edge in shortest paths: Yes/No" 中的 Yes/No
            if ": Yes" in correct:
                return correct.replace(": Yes", ": No", 1)
            elif ": No" in correct:
                return correct.replace(": No", ": Yes", 1)
            # 尝试修改最短成本数字
            m = re.search(r'Shortest cost:\s*(\d+)', correct)
            if m:
                old_val = int(m.group(1))
                new_val = old_val + 1
                return correct.replace(m.group(1), str(new_val), 1)
        
        return correct + " [WRONG]"