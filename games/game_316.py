# -*- coding: utf-8 -*-
# 自动生成 | 场景化改造: 交通、医疗、教育、制造业/工业、法律
# 推理类型: 溯因推理
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   环存在性：图中是否存在环
# ============================================================

from .base import Game
import re


class GraphReasoningGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图推理"游戏，规则如下：

游戏设定了一个有向图，包含节点集合：A, B, C, D, E, F。你总是从起始节点 A 开始。

图的结构是三个候选之一，但我不会告诉你具体是哪一个：

- 候选 Alpha：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到A, 操作1到F
  - D: 操作0到E, 操作1到E
  - E: 操作0到F, 操作1到F
  - F: 操作0到D, 操作1到D

- 候选 Beta：
  - A: 操作0到B, 操作1到C
  - B: 操作0到D, 操作1到E
  - C: 操作0到E, 操作1无边
  - D: 操作0到E, 操作1到F
  - E: 操作0到F, 操作1无边
  - F: 操作0无边, 操作1无边

- 候选 Gamma：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到B, 操作1到F
  - D: 操作0到E, 操作1无边
  - E: 操作0到D, 操作1无边
  - F: 操作0无边, 操作1无边

你可以通过以下四类交互请求来探索图的结构：

1. 执行操作：在当前节点尝试走操作0或操作1。如果该边存在，你会移动到目标节点；如果不存在，你会留在原地。
2. 复位：将当前位置重置为起始节点 A。
3. 位置查询：询问当前所在的节点。
4. 计步查询：询问自上次复位以来成功移动的次数（仅计算通过有效边的移动）。

你的目标是：
1. 识别真实的候选图（Alpha、Beta 或 Gamma）
2. 判断该图是否存在有向环（回答"有环"或"无环"）
3. 提供可验证的证据：
   - 如果判定"有环"：给出一条完整的有向环路径，格式为"X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - 如果判定"无环"：给出一个包含所有节点A到F的拓扑序列

## 交互格式要求

每次只能发起一个请求，使用以下XML格式：

- 执行操作（例如在当前节点执行操作1）：
<action>1</action>

- 复位到起始节点：
<reset></reset>

- 查询当前位置：
<query_position></query_position>

- 查询步数：
<query_steps></query_steps>

提交最终答案时，必须包含：候选图名称、环的判定、以及证据，格式如下：

有环的情况（示例）：
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

无环的情况（示例）：
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    game_rule_en = """\
Let's play a "Graph Reasoning" game. Here are the rules:

The game has a directed graph with nodes: A, B, C, D, E, F. You always start from node A.

The graph structure is one of three candidates, but I won't tell you which one:

- Candidate Alpha:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to A, action 1 to F
  - D: action 0 to E, action 1 to E
  - E: action 0 to F, action 1 to F
  - F: action 0 to D, action 1 to D

- Candidate Beta:
  - A: action 0 to B, action 1 to C
  - B: action 0 to D, action 1 to E
  - C: action 0 to E, action 1 no edge
  - D: action 0 to E, action 1 to F
  - E: action 0 to F, action 1 no edge
  - F: action 0 no edge, action 1 no edge

- Candidate Gamma:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to B, action 1 to F
  - D: action 0 to E, action 1 no edge
  - E: action 0 to D, action 1 no edge
  - F: action 0 no edge, action 1 no edge

You can explore the graph structure through four types of interaction:

1. Execute action: Try action 0 or 1 at current node. If the edge exists, you move to the target; otherwise, you stay.
2. Reset: Return to starting node A.
3. Position query: Ask which node you are currently at.
4. Step count query: Ask how many successful moves since last reset (only counts moves via valid edges).

Your goals are:
1. Identify the true candidate graph (Alpha, Beta, or Gamma)
2. Determine whether the graph has a directed cycle (answer "yes" or "no")
3. Provide verifiable evidence:
   - If "yes": Give a complete directed cycle path in format "X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - If "no": Give a topological order containing all nodes A through F

## Interaction Format Requirements

Each request must use one of the following XML formats:

- Execute action (e.g., execute action 1 at current node):
<action>1</action>

- Reset to starting node:
<reset></reset>

- Query current position:
<query_position></query_position>

- Query step count:
<query_steps></query_steps>

When submitting final answer, must include: graph name, cycle determination, and evidence, in this format:

With cycle (example):
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

Without cycle (example):
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
我们现在来执行"交通枢纽通行网络排查"任务，规则如下：

系统设定了一个有向通行图，包含交通枢纽集合：A, B, C, D, E, F。你总是从起始枢纽 A 开始排查。

图的结构是三个候选路线之一，但我不会告诉你具体是哪一个：

- 候选路线 Alpha：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到A, 操作1到F
  - D: 操作0到E, 操作1到E
  - E: 操作0到F, 操作1到F
  - F: 操作0到D, 操作1到D

- 候选路线 Beta：
  - A: 操作0到B, 操作1到C
  - B: 操作0到D, 操作1到E
  - C: 操作0到E, 操作1无边
  - D: 操作0到E, 操作1到F
  - E: 操作0到F, 操作1无边
  - F: 操作0无边, 操作1无边

- 候选路线 Gamma：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到B, 操作1到F
  - D: 操作0到E, 操作1无边
  - E: 操作0到D, 操作1无边
  - F: 操作0无边, 操作1无边

你可以通过以下四类交互请求来探索交通图的结构：

1. 执行操作：在当前枢纽尝试走操作0或操作1。如果该边存在，你会移动到目标枢纽；如果不存在，你会留在原地。
2. 复位：将当前位置重置为起始枢纽 A。
3. 位置查询：询问当前所在的枢纽。
4. 计步查询：询问自上次复位以来成功移动的次数（仅计算通过有效边的移动）。

你的目标是：
1. 识别真实的候选图（Alpha、Beta 或 Gamma）
2. 判断该通行图是否存在有向循环路线（回答"有环"或"无环"）
3. 提供可验证的证据：
   - 如果判定"有环"：给出一条完整的有向循环路径，格式为"X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - 如果判定"无环"：给出一个包含所有枢纽A到F的拓扑单向通行序列

## 交互格式要求

每次只能发起一个请求，使用以下XML格式：

- 执行操作（例如在当前枢纽执行操作1）：
<action>1</action>

- 复位到起始枢纽：
<reset></reset>

- 查询当前位置：
<query_position></query_position>

- 查询步数：
<query_steps></query_steps>

提交最终答案时，必须包含：候选图名称、环的判定、以及证据，格式如下：

有环的情况（示例）：
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

无环的情况（示例）：
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's execute the "Traffic Hub Transit Network Inspection" task. Here are the rules:

The system has a directed transit network graph with transportation hubs: A, B, C, D, E, F. You always start inspecting from the starting hub A.

The graph structure is one of three candidate routes, but I won't tell you which one:

- Candidate Route Alpha:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to A, action 1 to F
  - D: action 0 to E, action 1 to E
  - E: action 0 to F, action 1 to F
  - F: action 0 to D, action 1 to D

- Candidate Route Beta:
  - A: action 0 to B, action 1 to C
  - B: action 0 to D, action 1 to E
  - C: action 0 to E, action 1 no edge
  - D: action 0 to E, action 1 to F
  - E: action 0 to F, action 1 no edge
  - F: action 0 no edge, action 1 no edge

- Candidate Route Gamma:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to B, action 1 to F
  - D: action 0 to E, action 1 no edge
  - E: action 0 to D, action 1 no edge
  - F: action 0 no edge, action 1 no edge

You can explore the network structure through four types of interaction:

1. Execute action: Try action 0 or 1 at the current hub. If the edge exists, you move to the target hub; otherwise, you stay.
2. Reset: Return to the starting hub A.
3. Position query: Ask which hub you are currently at.
4. Step count query: Ask how many successful moves since the last reset (only counts moves via valid edges).

Your goals are:
1. Identify the true candidate graph (Alpha, Beta, or Gamma)
2. Determine whether the transit graph has a directed cyclic route (answer "yes" or "no")
3. Provide verifiable evidence:
   - If "yes": Give a complete directed cycle path in format "X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - If "no": Give a topological one-way transit sequence containing all hubs A through F

## Interaction Format Requirements

Each request must use one of the following XML formats:

- Execute action (e.g., execute action 1 at current hub):
<action>1</action>

- Reset to starting hub:
<reset></reset>

- Query current position:
<query_position></query_position>

- Query step count:
<query_steps></query_steps>

When submitting final answer, must include: graph name, cycle determination, and evidence, in this format:

With cycle (example):
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

Without cycle (example):
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
我们现在来执行"患者转诊流程审查"任务，规则如下：

系统设定了一个有向转诊流程图，包含科室节点集合：A, B, C, D, E, F。患者总是从起始科室 A 开始。

图的结构是三个候选转诊路径之一，但我不会告诉你具体是哪一个：

- 候选路径 Alpha：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到A, 操作1到F
  - D: 操作0到E, 操作1到E
  - E: 操作0到F, 操作1到F
  - F: 操作0到D, 操作1到D

- 候选路径 Beta：
  - A: 操作0到B, 操作1到C
  - B: 操作0到D, 操作1到E
  - C: 操作0到E, 操作1无边
  - D: 操作0到E, 操作1到F
  - E: 操作0到F, 操作1无边
  - F: 操作0无边, 操作1无边

- 候选路径 Gamma：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到B, 操作1到F
  - D: 操作0到E, 操作1无边
  - E: 操作0到D, 操作1无边
  - F: 操作0无边, 操作1无边

你可以通过以下四类交互请求来探索转诊图的结构：

1. 执行操作：在当前科室尝试走操作0或操作1。如果该边存在，你会移动到目标科室；如果不存在，你会留在原地。
2. 复位：将当前患者状态重置为起始科室 A。
3. 位置查询：询问当前所在的科室。
4. 计步查询：询问自上次复位以来成功移动的次数（仅计算通过有效边的移动）。

你的目标是：
1. 识别真实的候选图（Alpha、Beta 或 Gamma）
2. 判断该转诊图是否存在有向死循环（回答"有环"或"无环"）
3. 提供可验证的证据：
   - 如果判定"有环"：给出一条完整的有向死循环路径，格式为"X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - 如果判定"无环"：给出一个包含所有科室A到F的拓扑康复单向流转序列

## 交互格式要求

每次只能发起一个请求，使用以下XML格式：

- 执行操作（例如在当前科室执行操作1）：
<action>1</action>

- 复位到起始科室：
<reset></reset>

- 查询当前位置：
<query_position></query_position>

- 查询步数：
<query_steps></query_steps>

提交最终答案时，必须包含：候选图名称、环的判定、以及证据，格式如下：

有环的情况（示例）：
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

无环的情况（示例）：
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's execute the "Patient Referral Process Review" task. Here are the rules:

The system has a directed referral process graph with department nodes: A, B, C, D, E, F. The patient always starts from the starting department A.

The graph structure is one of three candidate pathways, but I won't tell you which one:

- Candidate Pathway Alpha:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to A, action 1 to F
  - D: action 0 to E, action 1 to E
  - E: action 0 to F, action 1 to F
  - F: action 0 to D, action 1 to D

- Candidate Pathway Beta:
  - A: action 0 to B, action 1 to C
  - B: action 0 to D, action 1 to E
  - C: action 0 to E, action 1 no edge
  - D: action 0 to E, action 1 to F
  - E: action 0 to F, action 1 no edge
  - F: action 0 no edge, action 1 no edge

- Candidate Pathway Gamma:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to B, action 1 to F
  - D: action 0 to E, action 1 no edge
  - E: action 0 to D, action 1 no edge
  - F: action 0 no edge, action 1 no edge

You can explore the referral structure through four types of interaction:

1. Execute action: Try action 0 or 1 at the current department. If the edge exists, you move to the target department; otherwise, you stay.
2. Reset: Return the patient state to the starting department A.
3. Position query: Ask which department you are currently at.
4. Step count query: Ask how many successful moves since the last reset (only counts moves via valid edges).

Your goals are:
1. Identify the true candidate graph (Alpha, Beta, or Gamma)
2. Determine whether the referral graph has a directed cyclic loop (answer "yes" or "no")
3. Provide verifiable evidence:
   - If "yes": Give a complete directed cycle path in format "X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - If "no": Give a topological one-way recovery sequence containing all departments A through F

## Interaction Format Requirements

Each request must use one of the following XML formats:

- Execute action (e.g., execute action 1 at current department):
<action>1</action>

- Reset to starting department:
<reset></reset>

- Query current position:
<query_position></query_position>

- Query step count:
<query_steps></query_steps>

When submitting final answer, must include: graph name, cycle determination, and evidence, in this format:

With cycle (example):
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

Without cycle (example):
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
我们现在来执行"自适应学习路径评估"任务，规则如下：

系统设定了一个有向学习路径图，包含知识模块集合：A, B, C, D, E, F。学生总是从起始模块 A 开始。

图的结构是三个候选教学设计之一，但我不会告诉你具体是哪一个：

- 候选设计 Alpha：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到A, 操作1到F
  - D: 操作0到E, 操作1到E
  - E: 操作0到F, 操作1到F
  - F: 操作0到D, 操作1到D

- 候选设计 Beta：
  - A: 操作0到B, 操作1到C
  - B: 操作0到D, 操作1到E
  - C: 操作0到E, 操作1无边
  - D: 操作0到E, 操作1到F
  - E: 操作0到F, 操作1无边
  - F: 操作0无边, 操作1无边

- 候选设计 Gamma：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到B, 操作1到F
  - D: 操作0到E, 操作1无边
  - E: 操作0到D, 操作1无边
  - F: 操作0无边, 操作1无边

你可以通过以下四类交互请求来探索学习路径的结构：

1. 执行操作：在当前模块尝试走操作0或操作1。如果该边存在，你会移动到目标模块；如果不存在，你会留在原地。
2. 复位：将当前学习进度重置为起始模块 A。
3. 位置查询：询问当前所在的知识模块。
4. 计步查询：询问自上次复位以来成功移动的次数（仅计算通过有效边的移动）。

你的目标是：
1. 识别真实的候选图（Alpha、Beta 或 Gamma）
2. 判断该学习图是否存在有向死循环（回答"有环"或"无环"）
3. 提供可验证的证据：
   - 如果判定"有环"：给出一条完整的有向学习死循环路径，格式为"X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - 如果判定"无环"：给出一个包含所有模块A到F的拓扑单向进阶序列

## 交互格式要求

每次只能发起一个请求，使用以下XML格式：

- 执行操作（例如在当前模块执行操作1）：
<action>1</action>

- 复位到起始模块：
<reset></reset>

- 查询当前位置：
<query_position></query_position>

- 查询步数：
<query_steps></query_steps>

提交最终答案时，必须包含：候选图名称、环的判定、以及证据，格式如下：

有环的情况（示例）：
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

无环的情况（示例）：
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's execute the "Adaptive Learning Path Assessment" task. Here are the rules:

The system has a directed learning path graph with knowledge modules: A, B, C, D, E, F. The student always starts from the initial module A.

The graph structure is one of three candidate instructional designs, but I won't tell you which one:

- Candidate Design Alpha:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to A, action 1 to F
  - D: action 0 to E, action 1 to E
  - E: action 0 to F, action 1 to F
  - F: action 0 to D, action 1 to D

- Candidate Design Beta:
  - A: action 0 to B, action 1 to C
  - B: action 0 to D, action 1 to E
  - C: action 0 to E, action 1 no edge
  - D: action 0 to E, action 1 to F
  - E: action 0 to F, action 1 no edge
  - F: action 0 no edge, action 1 no edge

- Candidate Design Gamma:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to B, action 1 to F
  - D: action 0 to E, action 1 no edge
  - E: action 0 to D, action 1 no edge
  - F: action 0 no edge, action 1 no edge

You can explore the path structure through four types of interaction:

1. Execute action: Try action 0 or 1 at the current module. If the edge exists, you move to the target module; otherwise, you stay.
2. Reset: Return the learning progress to the starting module A.
3. Position query: Ask which knowledge module you are currently at.
4. Step count query: Ask how many successful moves since the last reset (only counts moves via valid edges).

Your goals are:
1. Identify the true candidate graph (Alpha, Beta, or Gamma)
2. Determine whether the learning graph has a directed cyclic loop (answer "yes" or "no")
3. Provide verifiable evidence:
   - If "yes": Give a complete directed cycle path in format "X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - If "no": Give a topological one-way progression sequence containing all modules A through F

## Interaction Format Requirements

Each request must use one of the following XML formats:

- Execute action (e.g., execute action 1 at current module):
<action>1</action>

- Reset to starting module:
<reset></reset>

- Query current position:
<query_position></query_position>

- Query step count:
<query_steps></query_steps>

When submitting final answer, must include: graph name, cycle determination, and evidence, in this format:

With cycle (example):
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

Without cycle (example):
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
我们现在来执行"工厂物料流转检测"任务，规则如下：

系统设定了一个有向物料传送图，包含工作站集合：A, B, C, D, E, F。物料总是从起始工作站 A 开始流转。

图的结构是三个候选流水线配置之一，但我不会告诉你具体是哪一个：

- 候选配置 Alpha：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到A, 操作1到F
  - D: 操作0到E, 操作1到E
  - E: 操作0到F, 操作1到F
  - F: 操作0到D, 操作1到D

- 候选配置 Beta：
  - A: 操作0到B, 操作1到C
  - B: 操作0到D, 操作1到E
  - C: 操作0到E, 操作1无边
  - D: 操作0到E, 操作1到F
  - E: 操作0到F, 操作1无边
  - F: 操作0无边, 操作1无边

- 候选配置 Gamma：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到B, 操作1到F
  - D: 操作0到E, 操作1无边
  - E: 操作0到D, 操作1无边
  - F: 操作0无边, 操作1无边

你可以通过以下四类交互请求来探索传送图的结构：

1. 执行操作：在当前工作站尝试走操作0或操作1。如果该边存在，物料会移动到目标工作站；如果不存在，物料会留在原地。
2. 复位：将当前物料位置重置为起始工作站 A。
3. 位置查询：询问当前物料所在的工作站。
4. 计步查询：询问自上次复位以来成功移动的次数（仅计算通过有效边的移动）。

你的目标是：
1. 识别真实的候选图（Alpha、Beta 或 Gamma）
2. 判断该传送图是否存在有向回环传送（回答"有环"或"无环"）
3. 提供可验证的证据：
   - 如果判定"有环"：给出一条完整的有向回环路径，格式为"X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - 如果判定"无环"：给出一个包含所有工作站A到F的拓扑顺畅加工单向序列

## 交互格式要求

每次只能发起一个请求，使用以下XML格式：

- 执行操作（例如在当前工作站执行操作1）：
<action>1</action>

- 复位到起始工作站：
<reset></reset>

- 查询当前位置：
<query_position></query_position>

- 查询步数：
<query_steps></query_steps>

提交最终答案时，必须包含：候选图名称、环的判定、以及证据，格式如下：

有环的情况（示例）：
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

无环的情况（示例）：
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Let's execute the "Factory Material Flow Detection" task. Here are the rules:

The system has a directed material transfer graph with workstations: A, B, C, D, E, F. Materials always start flowing from the starting workstation A.

The graph structure is one of three candidate assembly line configurations, but I won't tell you which one:

- Candidate Configuration Alpha:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to A, action 1 to F
  - D: action 0 to E, action 1 to E
  - E: action 0 to F, action 1 to F
  - F: action 0 to D, action 1 to D

- Candidate Configuration Beta:
  - A: action 0 to B, action 1 to C
  - B: action 0 to D, action 1 to E
  - C: action 0 to E, action 1 no edge
  - D: action 0 to E, action 1 to F
  - E: action 0 to F, action 1 no edge
  - F: action 0 no edge, action 1 no edge

- Candidate Configuration Gamma:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to B, action 1 to F
  - D: action 0 to E, action 1 no edge
  - E: action 0 to D, action 1 no edge
  - F: action 0 no edge, action 1 no edge

You can explore the transfer structure through four types of interaction:

1. Execute action: Try action 0 or 1 at the current workstation. If the edge exists, the material moves to the target workstation; otherwise, it stays.
2. Reset: Return the material position to the starting workstation A.
3. Position query: Ask which workstation the material is currently at.
4. Step count query: Ask how many successful moves since the last reset (only counts moves via valid edges).

Your goals are:
1. Identify the true candidate graph (Alpha, Beta, or Gamma)
2. Determine whether the transfer graph has a directed cyclic loop (answer "yes" or "no")
3. Provide verifiable evidence:
   - If "yes": Give a complete directed cycle path in format "X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - If "no": Give a topological one-way processing sequence containing all workstations A through F

## Interaction Format Requirements

Each request must use one of the following XML formats:

- Execute action (e.g., execute action 1 at current workstation):
<action>1</action>

- Reset to starting workstation:
<reset></reset>

- Query current position:
<query_position></query_position>

- Query step count:
<query_steps></query_steps>

When submitting final answer, must include: graph name, cycle determination, and evidence, in this format:

With cycle (example):
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

Without cycle (example):
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
我们现在来执行"司法案件流转核查"任务，规则如下：

系统设定了一个有向案件移交图，包含司法审查部门集合：A, B, C, D, E, F。案件总是从起始部门 A 开始流转。

图的结构是三个候选法定流转程序之一，但我不会告诉你具体是哪一个：

- 候选程序 Alpha：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到A, 操作1到F
  - D: 操作0到E, 操作1到E
  - E: 操作0到F, 操作1到F
  - F: 操作0到D, 操作1到D

- 候选程序 Beta：
  - A: 操作0到B, 操作1到C
  - B: 操作0到D, 操作1到E
  - C: 操作0到E, 操作1无边
  - D: 操作0到E, 操作1到F
  - E: 操作0到F, 操作1无边
  - F: 操作0无边, 操作1无边

- 候选程序 Gamma：
  - A: 操作0到B, 操作1到D
  - B: 操作0到C, 操作1到E
  - C: 操作0到B, 操作1到F
  - D: 操作0到E, 操作1无边
  - E: 操作0到D, 操作1无边
  - F: 操作0无边, 操作1无边

你可以通过以下四类交互请求来探索案件移交图的结构：

1. 执行操作：在当前部门尝试走操作0或操作1。如果该边存在，案件会移交到目标部门；如果不存在，案件会留在原部门。
2. 复位：将当前案件状态重置为起始部门 A。
3. 位置查询：询问当前案件所在的部门。
4. 计步查询：询问自上次复位以来成功移交的次数（仅计算通过有效边的流转）。

你的目标是：
1. 识别真实的候选图（Alpha、Beta 或 Gamma）
2. 判断该移交图是否存在有向程序死循环（回答"有环"或"无环"）
3. 提供可验证的证据：
   - 如果判定"有环"：给出一条完整的有向案件循环路径，格式为"X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - 如果判定"无环"：给出一个包含所有部门A到F的拓扑合法结案单向序列

## 交互格式要求

每次只能发起一个请求，使用以下XML格式：

- 执行操作（例如在当前部门执行操作1）：
<action>1</action>

- 复位到起始部门：
<reset></reset>

- 查询当前位置：
<query_position></query_position>

- 查询步数：
<query_steps></query_steps>

提交最终答案时，必须包含：候选图名称、环的判定、以及证据，格式如下：

有环的情况（示例）：
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

无环的情况（示例）：
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's execute the "Judicial Case Flow Verification" task. Here are the rules:

The system has a directed case transfer graph with judicial departments: A, B, C, D, E, F. The case always starts flowing from the initial department A.

The graph structure is one of three candidate legal procedures, but I won't tell you which one:

- Candidate Procedure Alpha:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to A, action 1 to F
  - D: action 0 to E, action 1 to E
  - E: action 0 to F, action 1 to F
  - F: action 0 to D, action 1 to D

- Candidate Procedure Beta:
  - A: action 0 to B, action 1 to C
  - B: action 0 to D, action 1 to E
  - C: action 0 to E, action 1 no edge
  - D: action 0 to E, action 1 to F
  - E: action 0 to F, action 1 no edge
  - F: action 0 no edge, action 1 no edge

- Candidate Procedure Gamma:
  - A: action 0 to B, action 1 to D
  - B: action 0 to C, action 1 to E
  - C: action 0 to B, action 1 to F
  - D: action 0 to E, action 1 no edge
  - E: action 0 to D, action 1 no edge
  - F: action 0 no edge, action 1 no edge

You can explore the case transfer structure through four types of interaction:

1. Execute action: Try action 0 or 1 at the current department. If the edge exists, the case is transferred to the target department; otherwise, it stays.
2. Reset: Return the case state to the starting department A.
3. Position query: Ask which department the case is currently at.
4. Step count query: Ask how many successful transfers since the last reset (only counts moves via valid edges).

Your goals are:
1. Identify the true candidate graph (Alpha, Beta, or Gamma)
2. Determine whether the transfer graph has a directed procedural cyclic loop (answer "yes" or "no")
3. Provide verifiable evidence:
   - If "yes": Give a complete directed cycle path in format "X -(d1)-> Y -(d2)-> ... -(dk)-> X"
   - If "no": Give a topological lawful one-way resolution sequence containing all departments A through F

## Interaction Format Requirements

Each request must use one of the following XML formats:

- Execute action (e.g., execute action 1 at current department):
<action>1</action>

- Reset to starting department:
<reset></reset>

- Query current position:
<query_position></query_position>

- Query step count:
<query_steps></query_steps>

When submitting final answer, must include: graph name, cycle determination, and evidence, in this format:

With cycle (example):
<answer>graph=Alpha, cycle=yes, evidence=C -(0)-> A -(0)-> B -(0)-> C</answer>

Without cycle (example):
<answer>graph=Beta, cycle=no, evidence=A,B,C,D,E,F</answer>
"""

    tags = ["answer", "action", "reset", "query_position", "query_steps"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        1: {"graph": "Beta"},
        2: {"graph": "Gamma"},
        3: {"graph": "Alpha"},
        4: {"graph": "Alpha"},
        5: {"graph": "Gamma"},
    }

    GRAPHS = {
        "Alpha": {
            "A": {0: "B", 1: "D"},
            "B": {0: "C", 1: "E"},
            "C": {0: "A", 1: "F"},
            "D": {0: "E", 1: "E"},
            "E": {0: "F", 1: "F"},
            "F": {0: "D", 1: "D"},
        },
        "Beta": {
            "A": {0: "B", 1: "C"},
            "B": {0: "D", 1: "E"},
            "C": {0: "E"},
            "D": {0: "E", 1: "F"},
            "E": {0: "F"},
            "F": {},
        },
        "Gamma": {
            "A": {0: "B", 1: "D"},
            "B": {0: "C", 1: "E"},
            "C": {0: "B", 1: "F"},
            "D": {0: "E"},
            "E": {0: "D"},
            "F": {},
        },
    }

    CORRECT_ANSWERS = {
        "Alpha": {
            "has_cycle": True,
            "example_cycle": ["C", "A", "B", "C"],
            "cycle_actions": [0, 0, 0]
        },
        "Beta": {
            "has_cycle": False,
            "topo_order": ["A", "B", "C", "D", "E", "F"]
        },
        "Gamma": {
            "has_cycle": True,
            "example_cycle": ["D", "E", "D"],
            "cycle_actions": [0, 0]
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        self.true_graph_name = self.DIFFICULTY_CONFIG[diff]["graph"]
        self.graph = self.GRAPHS[self.true_graph_name]
        
        self.current_node = "A"
        self.step_count = 0
        
        self._game_info = {}

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        try:
            ans_dict = {}
            
            # 提取 graph
            graph_match = re.search(r'graph\s*=\s*(\w+)', raw_ans)
            cycle_match = re.search(r'cycle\s*=\s*(\w+)', raw_ans)
            evidence_match = re.search(r'evidence\s*=\s*(.+)', raw_ans)
            
            if not graph_match or not cycle_match or not evidence_match:
                return False
            
            graph_ans = graph_match.group(1).strip()
            cycle_ans = cycle_match.group(1).strip()
            evidence = evidence_match.group(1).strip()
            
            if graph_ans != self.true_graph_name:
                return False
            
            correct = self.CORRECT_ANSWERS[self.true_graph_name]
            
            if correct["has_cycle"]:
                if cycle_ans not in ["yes", "有环"]:
                    return False
                return self._verify_cycle(evidence)
            else:
                if cycle_ans not in ["no", "无环"]:
                    return False
                return self._verify_topo(evidence)
                
        except Exception as e:
            return False

    def _verify_cycle(self, evidence):
        pattern = r'([A-F])\s*-\((\d)\)->\s*'
        matches = re.findall(pattern, evidence)
        
        if not matches:
            return False
        
        nodes = [m[0] for m in matches]
        actions = [int(m[1]) for m in matches]
        
        last_node_match = re.search(r'->\s*([A-F])\s*$', evidence)
        if not last_node_match:
            return False
        last_node = last_node_match.group(1)
        nodes.append(last_node)
        
        if nodes[0] != nodes[-1]:
            return False
        
        for i in range(len(actions)):
            current = nodes[i]
            action = actions[i]
            expected_next = nodes[i + 1]
            
            if current not in self.graph:
                return False
            if action not in self.graph[current]:
                return False
            if self.graph[current][action] != expected_next:
                return False
        
        return True

    def _verify_topo(self, evidence):
        try:
            topo = [x.strip() for x in evidence.split(",")]
            
            if set(topo) != {"A", "B", "C", "D", "E", "F"}:
                return False
            
            pos = {node: i for i, node in enumerate(topo)}
            
            for node in self.graph:
                for action, target in self.graph[node].items():
                    if pos[node] >= pos[target]:
                        return False
            
            return True
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """根据玩家的操作产生游戏反馈（核心逻辑，供基类 produce_response 调用）"""
        lang = self.config.language
        
        if "action" in parsed_info:
            action_str = parsed_info["action"].strip()
            try:
                action = int(action_str)
                if action not in [0, 1]:
                    raise ValueError
            except:
                return "错误：操作必须是0或1。" if lang == "zh" else "Error: Action must be 0 or 1."
            
            if self.current_node in self.graph and action in self.graph[self.current_node]:
                target = self.graph[self.current_node][action]
                self.current_node = target
                self.step_count += 1
                if lang == "zh":
                    return f"成功，抵达 {target}"
                else:
                    return f"Success, arrived at {target}"
            else:
                if lang == "zh":
                    return f"无效，仍在 {self.current_node}"
                else:
                    return f"Invalid, still at {self.current_node}"
        
        elif "reset" in parsed_info:
            self.current_node = "A"
            self.step_count = 0
            return "已复位到 A" if lang == "zh" else "Reset to A"
        
        elif "query_position" in parsed_info:
            return f"在 {self.current_node}" if lang == "zh" else f"At {self.current_node}"
        
        elif "query_steps" in parsed_info:
            return str(self.step_count)
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """将正确的游戏回复篡改为错误回复，用于反事实干预"""
        lang = self.config.language
        nodes = ["A", "B", "C", "D", "E", "F"]

        if lang == "zh":
            # 处理"成功抵达"
            for node in nodes:
                if f"抵达 {node}" in correct:
                    wrong_nodes = [n for n in nodes if n != node]
                    return correct.replace(f"抵达 {node}", f"抵达 {wrong_nodes[0]}")
            # 处理"无效"
            if "无效" in correct:
                return f"成功，抵达 {nodes[0]}"
            # 处理"复位"
            if "复位" in correct:
                return f"已复位到 B"
            # 处理位置查询
            for node in nodes:
                if f"在 {node}" in correct:
                    wrong_nodes = [n for n in nodes if n != node]
                    return f"在 {wrong_nodes[0]}"
        else:
            for node in nodes:
                if f"arrived at {node}" in correct:
                    wrong_nodes = [n for n in nodes if n != node]
                    return correct.replace(f"arrived at {node}", f"arrived at {wrong_nodes[0]}")
            if "Invalid" in correct:
                return f"Success, arrived at {nodes[0]}"
            # 处理 reset 回复
            if "Reset to" in correct:
                return "Reset to B"
            for node in nodes:
                if f"At {node}" in correct:
                    wrong_nodes = [n for n in nodes if n != node]
                    return f"At {wrong_nodes[0]}"

        # 步数查询
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        return correct + " [error]"

    def get_all_possible_queries(self) -> list[dict]:
        """返回一组足够区分三个候选图并得出正确答案的查询序列。
        模拟一次完整的探索过程，不修改游戏自身状态。"""
        results = []
        lang = self.config.language
        
        # 保存当前状态
        saved_node = self.current_node
        saved_steps = self.step_count
        
        # 设计一个探索序列，可以区分所有三个候选图
        # 策略：从 A 开始，尝试各种操作序列
        exploration = [
            ("action", "0"),   # A -> ? (Alpha/Gamma: B, Beta: B)
            ("action", "1"),   # B -> ? (Alpha: E, Beta: E, Gamma: E)  -- 所有都到E
            ("reset", ""),
            ("action", "1"),   # A -> ? (Alpha: D, Beta: C, Gamma: D) -- 可区分Beta
            ("reset", ""),
            ("action", "0"),   # A -> B
            ("action", "0"),   # B -> C
            ("action", "0"),   # C -> ? (Alpha: A, Beta: E, Gamma: B) -- 可区分所有
            ("query_position", ""),
            ("reset", ""),
            ("action", "1"),   # A -> D or C
            ("action", "0"),   # D->E or C->E
            ("action", "0"),   # E->F or E->F(Alpha) or E->D(Gamma)
            ("query_position", ""),
            ("query_steps", ""),
        ]
        
        # 重置到初始状态进行模拟
        self.current_node = "A"
        self.step_count = 0
        
        for op_type, op_value in exploration:
            if op_type == "action":
                query_str = f"<action>{op_value}</action>"
                action = int(op_value)
                if self.current_node in self.graph and action in self.graph[self.current_node]:
                    target = self.graph[self.current_node][action]
                    self.current_node = target
                    self.step_count += 1
                    ans = f"成功，抵达 {target}" if lang == "zh" else f"Success, arrived at {target}"
                else:
                    ans = f"无效，仍在 {self.current_node}" if lang == "zh" else f"Invalid, still at {self.current_node}"
            elif op_type == "reset":
                query_str = "<reset></reset>"
                self.current_node = "A"
                self.step_count = 0
                ans = "已复位到 A" if lang == "zh" else "Reset to A"
            elif op_type == "query_position":
                query_str = "<query_position></query_position>"
                ans = f"在 {self.current_node}" if lang == "zh" else f"At {self.current_node}"
            elif op_type == "query_steps":
                query_str = "<query_steps></query_steps>"
                ans = str(self.step_count)
            else:
                continue
            
            results.append({"query": query_str, "answer": ans})
        
        # 恢复原始状态
        self.current_node = saved_node
        self.step_count = saved_steps
        
        return results