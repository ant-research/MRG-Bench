# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   环存在性：图中是否存在环
# ============================================================

from .base import Game
import re

class GraphRuleDeductionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图规则推理"游戏，规则如下：

游戏设定了一个固定的无向图，节点为 A, B, C, D, E, V。存在若干条可控的无向边（初始均为关闭状态）：
- 三角形区域：AB, BC, CA
- 另一三角形区域：CD, DE, EC
- 连接边：AD
- 与V相关的边：VA, VC, VD

我已秘密选择了一个固定的规则 R（从以下三者中选定，且在整个游戏过程中不变）。一个二值指示器 I 会根据规则 R 作用在当前已开启边构成的子图上给出：

**规则 Alpha**：当且仅当存在任意长度的简单环（是否包含节点V不限）时，I=1。
**规则 Beta**：当且仅当存在至少一个包含节点V的简单环时，I=1；不含V的环不触发。
**规则 Gamma**：当且仅当存在偶数长度的简单环（长度为4、6等）时，I=1；奇数长度环不触发。

你的任务是：
1. 通过交互确定规则 R 是 Alpha、Beta 还是 Gamma
2. 给出一个相对于 R 与当前图的"最小触发集" S（边的集合）：使得 I(S)=1，且对任一边 e 属于 S，有 I(S去除e后)=0

## 允许的操作

你可以进行以下操作（每次只能进行一个操作）：

1. **边状态设定**：设置某条边为开启或关闭状态
   格式：<set_edge>边名,状态</set_edge>
   其中状态为"开启"或"关闭"
   例如：<set_edge>AB,开启</set_edge>

2. **指示器查询**：询问当前指示器是否为1
   格式：<query_indicator></query_indicator>

3. **枚举查询**：询问当前已开启的边有哪些
   格式：<query_edges></query_edges>

4. **数量查询**：询问当前已开启的边数量
   格式：<query_count></query_count>

5. **规则宣告**：宣告你判定的规则类型
   格式：<declare_rule>规则名</declare_rule>
   规则名为 Alpha、Beta 或 Gamma
   例如：<declare_rule>Alpha</declare_rule>

6. **最小性验证**：询问如果将某条边关闭，指示器是否变为0（这是一个假设性查询，不改变实际状态）
   格式：<verify_minimal>边名</verify_minimal>
   例如：<verify_minimal>AB</verify_minimal>

7. **提交最终答案**：提交你的规则判定和最小触发集
   格式：<answer>rule=规则名, edges=边名列表</answer>
   边名用逗号分隔，顺序不限
   例如：<answer>rule=Alpha, edges=AB,BC,CA</answer>

## 游戏要求

- 你需要尽可能少地使用操作次数完成任务
- 成功条件：规则判定正确，且提交的边集确实是最小触发集
- 若规则判定错误或边集不是最小触发集，则游戏失败
"""

    game_rule_en = """\
Let's play a "Graph Rule Deduction" game. Here are the rules:

The game has a fixed undirected graph with nodes A, B, C, D, E, V. There are several controllable undirected edges (all initially closed):
- Triangle area: AB, BC, CA
- Another triangle area: CD, DE, EC
- Connecting edge: AD
- Edges related to V: VA, VC, VD

I have secretly selected a fixed rule R (chosen from the following three, and it remains unchanged throughout the game). A binary indicator I is given by applying rule R to the subgraph formed by currently opened edges:

**Rule Alpha**: I=1 if and only if there exists a simple cycle of any length (whether or not it includes node V).
**Rule Beta**: I=1 if and only if there exists at least one simple cycle that includes node V; cycles without V do not trigger.
**Rule Gamma**: I=1 if and only if there exists an even-length simple cycle (length 4, 6, etc.); odd-length cycles do not trigger.

Your tasks are:
1. Determine through interaction whether rule R is Alpha, Beta, or Gamma
2. Provide a "minimal trigger set" S (a set of edges) relative to R and the current graph: such that I(S)=1, and for any edge e in S, I(S without e)=0

## Allowed Operations

You can perform the following operations (one operation at a time):

1. **Edge State Setting**: Set an edge to open or closed state
   Format: <set_edge>edge_name,state</set_edge>
   State is "open" or "closed"
   Example: <set_edge>AB,open</set_edge>

2. **Indicator Query**: Ask if the current indicator is 1
   Format: <query_indicator></query_indicator>

3. **Enumeration Query**: Ask which edges are currently open
   Format: <query_edges></query_edges>

4. **Count Query**: Ask the number of currently open edges
   Format: <query_count></query_count>

5. **Rule Declaration**: Declare the rule type you have determined
   Format: <declare_rule>rule_name</declare_rule>
   Rule name is Alpha, Beta, or Gamma
   Example: <declare_rule>Alpha</declare_rule>

6. **Minimality Verification**: Ask if closing a certain edge would make the indicator become 0 (this is a hypothetical query, does not change actual state)
   Format: <verify_minimal>edge_name</verify_minimal>
   Example: <verify_minimal>AB</verify_minimal>

7. **Submit Final Answer**: Submit your rule determination and minimal trigger set
   Format: <answer>rule=rule_name, edges=edge_list</answer>
   Edges are comma-separated, order does not matter
   Example: <answer>rule=Alpha, edges=AB,BC,CA</answer>

## Game Requirements

- You need to complete the task using as few operations as possible
- Success conditions: correct rule determination and the submitted edge set is indeed a minimal trigger set
- If the rule determination is wrong or the edge set is not a minimal trigger set, the game fails
"""

    contextualized_rule_zh_1 = """\
欢迎进入"交通路网冗余拓扑分析"系统。

系统中设定了一个固定的交通管网拓扑，节点为 A, B, C, D, E, V，分别代表不同的城市交通枢纽，其中 V 是核心中转枢纽。存在若干条可控的道路/航线（初始均为关闭状态）：
- 东区三角路网：AB, BC, CA
- 西区三角路网：CD, DE, EC
- 跨区联络线：AD
- 与核心枢纽V相连的线路：VA, VC, VD

系统目前正执行一项秘密的连通性监测规则 R（从以下三者中选定，且在整个分析过程中不变）。一个二值预警指示器 I 会根据规则 R 作用在当前已开启线路构成的连通子图上，给出反馈：

**规则 Alpha**：当且仅当存在任意长度的闭环路网（不管是否经过枢纽V）时，触发预警 I=1。
**规则 Beta**：当且仅当存在至少一个包含核心枢纽V的闭环路网时，触发预警 I=1；不含V的闭环不触发。
**规则 Gamma**：当且仅当存在偶数个节点参与的闭环路网（长度为4、6等，用于双向调度平衡）时，触发预警 I=1；奇数长度的闭环不触发。

你的任务是：
1. 通过交互确定监测规则 R 是 Alpha、Beta 还是 Gamma
2. 给出一个相对于 R 与当前管网的"最小触发集" S（线路的集合）：使得 I(S)=1，且对任一线路 e 属于 S，有 I(S去除e后)=0

## 允许的操作

你可以进行以下操作（每次只能进行一个操作）：

1. **线路状态设定**：设置某条线路为开启或关闭状态
   格式：<set_edge>线路名,状态</set_edge>
   其中状态为"开启"或"关闭"
   例如：<set_edge>AB,开启</set_edge>

2. **指示器查询**：询问当前预警指示器是否为1
   格式：<query_indicator></query_indicator>

3. **枚举查询**：询问当前已开启的线路有哪些
   格式：<query_edges></query_edges>

4. **数量查询**：询问当前已开启的线路数量
   格式：<query_count></query_count>

5. **规则宣告**：宣告你判定的监测规则类型
   格式：<declare_rule>规则名</declare_rule>
   规则名为 Alpha、Beta 或 Gamma
   例如：<declare_rule>Alpha</declare_rule>

6. **最小性验证**：询问如果将某条线路关闭，指示器是否变为0（这是一个假设性查询，不改变实际状态）
   格式：<verify_minimal>线路名</verify_minimal>
   例如：<verify_minimal>AB</verify_minimal>

7. **提交最终答案**：提交你的规则判定和最小触发集
   格式：<answer>rule=规则名, edges=线路名列表</answer>
   线路名用逗号分隔，顺序不限
   例如：<answer>rule=Alpha, edges=AB,BC,CA</answer>

## 任务要求

- 你需要尽可能少地使用操作次数完成分析任务
- 成功条件：规则判定正确，且提交的线路集确实是最小触发集
- 若规则判定错误或线路集不是最小触发集，则分析失败
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Traffic Network Redundancy Topology Analysis" system.

The system features a fixed traffic network topology with nodes A, B, C, D, E, V, representing different city transport hubs, where V is the Core Hub. There are several controllable routes (all initially closed):
- East Triangle Network: AB, BC, CA
- West Triangle Network: CD, DE, EC
- Cross-zone Link: AD
- Routes connected to Core Hub V: VA, VC, VD

The system is currently executing a secret connectivity monitoring rule R (chosen from the following three, and it remains unchanged throughout the analysis). A binary warning indicator I is given by applying rule R to the connected subgraph formed by currently opened routes:

**Rule Alpha**: I=1 if and only if there exists a closed loop network of any length (whether or not it includes Hub V).
**Rule Beta**: I=1 if and only if there exists at least one closed loop network that includes Core Hub V; loops without V do not trigger.
**Rule Gamma**: I=1 if and only if there exists an even-node closed loop network (length 4, 6, etc., for bilateral scheduling balance); odd-length loops do not trigger.

Your tasks are:
1. Determine through interaction whether monitoring rule R is Alpha, Beta, or Gamma
2. Provide a "minimal trigger set" S (a set of routes) relative to R and the current network: such that I(S)=1, and for any route e in S, I(S without e)=0

## Allowed Operations

You can perform the following operations (one operation at a time):

1. **Route State Setting**: Set a route to open or closed state
   Format: <set_edge>route_name,state</set_edge>
   State is "open" or "closed"
   Example: <set_edge>AB,open</set_edge>

2. **Indicator Query**: Ask if the current warning indicator is 1
   Format: <query_indicator></query_indicator>

3. **Enumeration Query**: Ask which routes are currently open
   Format: <query_edges></query_edges>

4. **Count Query**: Ask the number of currently open routes
   Format: <query_count></query_count>

5. **Rule Declaration**: Declare the monitoring rule type you have determined
   Format: <declare_rule>rule_name</declare_rule>
   Rule name is Alpha, Beta, or Gamma
   Example: <declare_rule>Alpha</declare_rule>

6. **Minimality Verification**: Ask if closing a certain route would make the indicator become 0 (this is a hypothetical query, does not change actual state)
   Format: <verify_minimal>route_name</verify_minimal>
   Example: <verify_minimal>AB</verify_minimal>

7. **Submit Final Answer**: Submit your rule determination and minimal trigger set
   Format: <answer>rule=rule_name, edges=route_list</answer>
   Routes are comma-separated, order does not matter
   Example: <answer>rule=Alpha, edges=AB,BC,CA</answer>

## Task Requirements

- You need to complete the analysis task using as few operations as possible
- Success conditions: correct rule determination and the submitted route set is indeed a minimal trigger set
- If the rule determination is wrong or the route set is not a minimal trigger set, the task fails
"""

    contextualized_rule_zh_2 = """\
欢迎使用"医疗信息与物流通道链路诊断"系统。

系统中设有一个固定的医疗拓扑，节点 A, B, C, D, E, V 分别代表不同的科室或医疗设备，其中 V 是核心数据库。存在若干条可控的信息流/物流通道（初始均为关闭状态）：
- 东翼数据环路：AB, BC, CA
- 西翼数据环路：CD, DE, EC
- 跨科室通道：AD
- 与核心数据库V相连的通道：VA, VC, VD

系统目前正执行一项隐秘的链路诊断规则 R（从以下三者中选定，且在整个诊断过程中不变）。一个二值连通指示器 I 会根据规则 R 作用在当前已开启通道构成的子图上，给出反馈：

**规则 Alpha**：当且仅当存在任意长度的数据回流闭环（不管是否经过数据库V）时，触发指示器 I=1。
**规则 Beta**：当且仅当存在至少一个包含核心数据库V的数据回流闭环时，触发指示器 I=1；不含V的闭环不触发。
**规则 Gamma**：当且仅当存在偶数个科室参与的数据回流闭环（长度为4、6等，用于多端同步确认）时，触发指示器 I=1；奇数长度的闭环不触发。

你的任务是：
1. 通过交互确定诊断规则 R 是 Alpha、Beta 还是 Gamma
2. 给出一个相对于 R 与当前拓扑的"最小触发集" S（通道的集合）：使得 I(S)=1，且对任一通道 e 属于 S，有 I(S去除e后)=0

## 允许的操作

你可以进行以下操作（每次只能进行一个操作）：

1. **通道状态设定**：设置某条通道为开启或关闭状态
   格式：<set_edge>通道名,状态</set_edge>
   其中状态为"开启"或"关闭"
   例如：<set_edge>AB,开启</set_edge>

2. **指示器查询**：询问当前连通指示器是否为1
   格式：<query_indicator></query_indicator>

3. **枚举查询**：询问当前已开启的通道有哪些
   格式：<query_edges></query_edges>

4. **数量查询**：询问当前已开启的通道数量
   格式：<query_count></query_count>

5. **规则宣告**：宣告你判定的诊断规则类型
   格式：<declare_rule>规则名</declare_rule>
   规则名为 Alpha、Beta 或 Gamma
   例如：<declare_rule>Alpha</declare_rule>

6. **最小性验证**：询问如果将某条通道关闭，指示器是否变为0（这是一个假设性查询，不改变实际状态）
   格式：<verify_minimal>通道名</verify_minimal>
   例如：<verify_minimal>AB</verify_minimal>

7. **提交最终答案**：提交你的规则判定和最小触发集
   格式：<answer>rule=规则名, edges=通道名列表</answer>
   通道名用逗号分隔，顺序不限
   例如：<answer>rule=Alpha, edges=AB,BC,CA</answer>

## 任务要求

- 你需要尽可能少地使用操作次数完成诊断任务
- 成功条件：规则判定正确，且提交的通道集确实是最小触发集
- 若规则判定错误或通道集不是最小触发集，则诊断失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Medical Information & Resource Logistics Routing Diagnosis" system.

The system features a fixed medical topology with nodes A, B, C, D, E, V, representing different departments or medical devices, where V is the Core Database. There are several controllable information/logistics channels (all initially closed):
- East Wing Data Loop: AB, BC, CA
- West Wing Data Loop: CD, DE, EC
- Cross-department Channel: AD
- Channels connected to Core Database V: VA, VC, VD

The system is currently executing a secret routing diagnosis rule R (chosen from the following three, and it remains unchanged throughout the diagnosis). A binary connection indicator I is given by applying rule R to the subgraph formed by currently opened channels:

**Rule Alpha**: I=1 if and only if there exists a data circulation loop of any length (whether or not it includes Database V).
**Rule Beta**: I=1 if and only if there exists at least one data circulation loop that includes Core Database V; loops without V do not trigger.
**Rule Gamma**: I=1 if and only if there exists an even-node data circulation loop (length 4, 6, etc., for multi-end synchronization confirmation); odd-length loops do not trigger.

Your tasks are:
1. Determine through interaction whether diagnosis rule R is Alpha, Beta, or Gamma
2. Provide a "minimal trigger set" S (a set of channels) relative to R and the current topology: such that I(S)=1, and for any channel e in S, I(S without e)=0

## Allowed Operations

You can perform the following operations (one operation at a time):

1. **Channel State Setting**: Set a channel to open or closed state
   Format: <set_edge>channel_name,state</set_edge>
   State is "open" or "closed"
   Example: <set_edge>AB,open</set_edge>

2. **Indicator Query**: Ask if the current connection indicator is 1
   Format: <query_indicator></query_indicator>

3. **Enumeration Query**: Ask which channels are currently open
   Format: <query_edges></query_edges>

4. **Count Query**: Ask the number of currently open channels
   Format: <query_count></query_count>

5. **Rule Declaration**: Declare the diagnosis rule type you have determined
   Format: <declare_rule>rule_name</declare_rule>
   Rule name is Alpha, Beta, or Gamma
   Example: <declare_rule>Alpha</declare_rule>

6. **Minimality Verification**: Ask if closing a certain channel would make the indicator become 0 (this is a hypothetical query, does not change actual state)
   Format: <verify_minimal>channel_name</verify_minimal>
   Example: <verify_minimal>AB</verify_minimal>

7. **Submit Final Answer**: Submit your rule determination and minimal trigger set
   Format: <answer>rule=rule_name, edges=channel_list</answer>
   Channels are comma-separated, order does not matter
   Example: <answer>rule=Alpha, edges=AB,BC,CA</answer>

## Task Requirements

- You need to complete the diagnosis task using as few operations as possible
- Success conditions: correct rule determination and the submitted channel set is indeed a minimal trigger set
- If the rule determination is wrong or the channel set is not a minimal trigger set, the task fails
"""

    contextualized_rule_zh_3 = """\
欢迎使用"知识图谱学习路径推演"系统。

系统中设有一个固定的知识结构拓扑，节点 A, B, C, D, E, V 分别代表不同的学术模块，其中 V 是核心基础理论模块。存在若干条可控的关联引用/学习路径（初始均为关闭状态）：
- 基础理论三角：AB, BC, CA
- 高级应用三角：CD, DE, EC
- 跨学科关联：AD
- 与核心模块V相关的引用路径：VA, VC, VD

系统目前正执行一项秘密的逻辑校验规则 R（从以下三者中选定，且在整个推演过程中不变）。一个二值闭环指示器 I 会根据规则 R 作用在当前已开启路径构成的子图上，给出反馈：

**规则 Alpha**：当且仅当存在任意长度的知识循环引用（不管是否经过核心模块V）时，触发指示器 I=1。
**规则 Beta**：当且仅当存在至少一个包含核心理论模块V的知识循环引用时，触发指示器 I=1；不含V的循环不触发。
**规则 Gamma**：当且仅当存在偶数个模块参与的知识循环引用（长度为4、6等，用于构建对立辩论模型）时，触发指示器 I=1；奇数长度的循环不触发。

你的任务是：
1. 通过交互确定逻辑校验规则 R 是 Alpha、Beta 还是 Gamma
2. 给出一个相对于 R 与当前图谱的"最小触发集" S（路径的集合）：使得 I(S)=1，且对任一路径 e 属于 S，有 I(S去除e后)=0

## 允许的操作

你可以进行以下操作（每次只能进行一个操作）：

1. **路径状态设定**：设置某条路径为开启或关闭状态
   格式：<set_edge>路径名,状态</set_edge>
   其中状态为"开启"或"关闭"
   例如：<set_edge>AB,开启</set_edge>

2. **指示器查询**：询问当前闭环指示器是否为1
   格式：<query_indicator></query_indicator>

3. **枚举查询**：询问当前已开启的路径有哪些
   格式：<query_edges></query_edges>

4. **数量查询**：询问当前已开启的路径数量
   格式：<query_count></query_count>

5. **规则宣告**：宣告你判定的校验规则类型
   格式：<declare_rule>规则名</declare_rule>
   规则名为 Alpha、Beta 或 Gamma
   例如：<declare_rule>Alpha</declare_rule>

6. **最小性验证**：询问如果将某条路径关闭，指示器是否变为0（这是一个假设性查询，不改变实际状态）
   格式：<verify_minimal>路径名</verify_minimal>
   例如：<verify_minimal>AB</verify_minimal>

7. **提交最终答案**：提交你的规则判定和最小触发集
   格式：<answer>rule=规则名, edges=路径名列表</answer>
   路径名用逗号分隔，顺序不限
   例如：<answer>rule=Alpha, edges=AB,BC,CA</answer>

## 任务要求

- 你需要尽可能少地使用操作次数完成推演任务
- 成功条件：规则判定正确，且提交的路径集确实是最小触发集
- 若规则判定错误或路径集不是最小触发集，则推演失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Learning Path Deduction" system.

The system features a fixed knowledge structure topology with nodes A, B, C, D, E, V, representing different academic modules, where V is the Core Fundamental Theory Module. There are several controllable reference/learning paths (all initially closed):
- Basic Theory Triangle: AB, BC, CA
- Advanced Application Triangle: CD, DE, EC
- Cross-disciplinary Link: AD
- Reference paths related to Core Module V: VA, VC, VD

The system is currently executing a secret logic validation rule R (chosen from the following three, and it remains unchanged throughout the deduction). A binary closed-loop indicator I is given by applying rule R to the subgraph formed by currently opened paths:

**Rule Alpha**: I=1 if and only if there exists a circular reference path of any length (whether or not it includes Core Module V).
**Rule Beta**: I=1 if and only if there exists at least one circular reference path that includes Core Fundamental Module V; loops without V do not trigger.
**Rule Gamma**: I=1 if and only if there exists an even-module circular reference path (length 4, 6, etc., used to build opposing debate models); odd-length loops do not trigger.

Your tasks are:
1. Determine through interaction whether validation rule R is Alpha, Beta, or Gamma
2. Provide a "minimal trigger set" S (a set of paths) relative to R and the current graph: such that I(S)=1, and for any path e in S, I(S without e)=0

## Allowed Operations

You can perform the following operations (one operation at a time):

1. **Path State Setting**: Set a path to open or closed state
   Format: <set_edge>path_name,state</set_edge>
   State is "open" or "closed"
   Example: <set_edge>AB,open</set_edge>

2. **Indicator Query**: Ask if the current closed-loop indicator is 1
   Format: <query_indicator></query_indicator>

3. **Enumeration Query**: Ask which paths are currently open
   Format: <query_edges></query_edges>

4. **Count Query**: Ask the number of currently open paths
   Format: <query_count></query_count>

5. **Rule Declaration**: Declare the validation rule type you have determined
   Format: <declare_rule>rule_name</declare_rule>
   Rule name is Alpha, Beta, or Gamma
   Example: <declare_rule>Alpha</declare_rule>

6. **Minimality Verification**: Ask if closing a certain path would make the indicator become 0 (this is a hypothetical query, does not change actual state)
   Format: <verify_minimal>path_name</verify_minimal>
   Example: <verify_minimal>AB</verify_minimal>

7. **Submit Final Answer**: Submit your rule determination and minimal trigger set
   Format: <answer>rule=rule_name, edges=path_list</answer>
   Paths are comma-separated, order does not matter
   Example: <answer>rule=Alpha, edges=AB,BC,CA</answer>

## Task Requirements

- You need to complete the deduction task using as few operations as possible
- Success conditions: correct rule determination and the submitted path set is indeed a minimal trigger set
- If the rule determination is wrong or the path set is not a minimal trigger set, the task fails
"""

    contextualized_rule_zh_4 = """\
欢迎使用"工业制造工序回流与质检控制"系统。

系统中设有一个固定的生产车间拓扑，节点 A, B, C, D, E, V 分别代表不同的生产加工中心，其中 V 是核心质检中心。存在若干条可控的物料传送带（初始均为关闭状态）：
- 预处理流水线：AB, BC, CA
- 总装流水线：CD, DE, EC
- 跨车间传送带：AD
- 与核心质检中心V相连的传送带：VA, VC, VD

系统目前正执行一项严格的物料回流控制规则 R（从以下三者中选定，且在整个控制过程中不变）。一个二值回流警报指示器 I 会根据规则 R 作用在当前已开启传送带构成的子图上，给出反馈：

**规则 Alpha**：当且仅当存在任意长度的物料返工回流环（不管是否经过质检中心V）时，触发警报 I=1。
**规则 Beta**：当且仅当存在至少一个包含核心质检中心V的物料回流环时，触发警报 I=1；不含V的回流环不触发。
**规则 Gamma**：当且仅当存在偶数个工序参与的物料回流环（长度为4、6等，用于多阶段交替返工）时，触发警报 I=1；奇数长度的回流环不触发。

你的任务是：
1. 通过交互确定控制规则 R 是 Alpha、Beta 还是 Gamma
2. 给出一个相对于 R 与当前车间的"最小触发集" S（传送带的集合）：使得 I(S)=1，且对任一传送带 e 属于 S，有 I(S去除e后)=0

## 允许的操作

你可以进行以下操作（每次只能进行一个操作）：

1. **传送带状态设定**：设置某条传送带为开启或关闭状态
   格式：<set_edge>传送带名,状态</set_edge>
   其中状态为"开启"或"关闭"
   例如：<set_edge>AB,开启</set_edge>

2. **指示器查询**：询问当前回流警报指示器是否为1
   格式：<query_indicator></query_indicator>

3. **枚举查询**：询问当前已开启的传送带有哪些
   格式：<query_edges></query_edges>

4. **数量查询**：询问当前已开启的传送带数量
   格式：<query_count></query_count>

5. **规则宣告**：宣告你判定的控制规则类型
   格式：<declare_rule>规则名</declare_rule>
   规则名为 Alpha、Beta 或 Gamma
   例如：<declare_rule>Alpha</declare_rule>

6. **最小性验证**：询问如果将某条传送带关闭，警报指示器是否变为0（这是一个假设性查询，不改变实际状态）
   格式：<verify_minimal>传送带名</verify_minimal>
   例如：<verify_minimal>AB</verify_minimal>

7. **提交最终答案**：提交你的规则判定和最小触发集
   格式：<answer>rule=规则名, edges=传送带名列表</answer>
   传送带名用逗号分隔，顺序不限
   例如：<answer>rule=Alpha, edges=AB,BC,CA</answer>

## 任务要求

- 你需要尽可能少地使用操作次数完成控制排查任务
- 成功条件：规则判定正确，且提交的传送带集确实是最小触发集
- 若规则判定错误或传送带集不是最小触发集，则排查失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Manufacturing Process Flow & Quality Control" system.

The system features a fixed production workshop topology with nodes A, B, C, D, E, V, representing different processing centers, where V is the Core Quality Inspection Center. There are several controllable material conveyors (all initially closed):
- Pre-processing Loop: AB, BC, CA
- Assembly Loop: CD, DE, EC
- Cross-workshop Conveyor: AD
- Conveyors connected to Inspection Center V: VA, VC, VD

The system is currently executing a strict material backflow control rule R (chosen from the following three, and it remains unchanged throughout the process). A binary backflow warning indicator I is given by applying rule R to the subgraph formed by currently opened conveyors:

**Rule Alpha**: I=1 if and only if there exists a material rework backflow loop of any length (whether or not it includes Inspection Center V).
**Rule Beta**: I=1 if and only if there exists at least one material backflow loop that includes Core Quality Inspection Center V; loops without V do not trigger.
**Rule Gamma**: I=1 if and only if there exists an even-stage material backflow loop (length 4, 6, etc., for multi-phase alternating rework); odd-length loops do not trigger.

Your tasks are:
1. Determine through interaction whether control rule R is Alpha, Beta, or Gamma
2. Provide a "minimal trigger set" S (a set of conveyors) relative to R and the current workshop: such that I(S)=1, and for any conveyor e in S, I(S without e)=0

## Allowed Operations

You can perform the following operations (one operation at a time):

1. **Conveyor State Setting**: Set a conveyor to open or closed state
   Format: <set_edge>conveyor_name,state</set_edge>
   State is "open" or "closed"
   Example: <set_edge>AB,open</set_edge>

2. **Indicator Query**: Ask if the current warning indicator is 1
   Format: <query_indicator></query_indicator>

3. **Enumeration Query**: Ask which conveyors are currently open
   Format: <query_edges></query_edges>

4. **Count Query**: Ask the number of currently open conveyors
   Format: <query_count></query_count>

5. **Rule Declaration**: Declare the control rule type you have determined
   Format: <declare_rule>rule_name</declare_rule>
   Rule name is Alpha, Beta, or Gamma
   Example: <declare_rule>Alpha</declare_rule>

6. **Minimality Verification**: Ask if closing a certain conveyor would make the indicator become 0 (this is a hypothetical query, does not change actual state)
   Format: <verify_minimal>conveyor_name</verify_minimal>
   Example: <verify_minimal>AB</verify_minimal>

7. **Submit Final Answer**: Submit your rule determination and minimal trigger set
   Format: <answer>rule=rule_name, edges=conveyor_list</answer>
   Conveyors are comma-separated, order does not matter
   Example: <answer>rule=Alpha, edges=AB,BC,CA</answer>

## Task Requirements

- You need to complete the control troubleshooting task using as few operations as possible
- Success conditions: correct rule determination and the submitted conveyor set is indeed a minimal trigger set
- If the rule determination is wrong or the conveyor set is not a minimal trigger set, the task fails
"""

    contextualized_rule_zh_5 = """\
欢迎使用"法律证据链与资金回溯追踪"系统。

系统中设有一个固定的案件关系拓扑，节点 A, B, C, D, E, V 分别代表不同的案件主体或证据，其中 V 是核心嫌疑人/关键证物。存在若干条可控的逻辑关联/资金流向（初始均为被切断状态）：
- 境内交易三角：AB, BC, CA
- 离岸交易三角：CD, DE, EC
- 跨界转移链路：AD
- 与核心主体V相关的流向：VA, VC, VD

系统目前正执行一项核心的侦查定性规则 R（从以下三者中选定，且在整个追踪过程中不变）。一个二值闭环预警指示器 I 会根据规则 R 作用在当前已接通流向构成的子图上，给出反馈：

**规则 Alpha**：当且仅当存在任意长度的资金/逻辑闭环（不管是否经过核心主体V）时，触发预警 I=1。
**规则 Beta**：当且仅当存在至少一个包含核心主体V的闭环时，触发预警 I=1；不含V的闭环不触发。
**规则 Gamma**：当且仅当存在偶数个主体参与的闭环（长度为4、6等，典型的双边对敲交易特征）时，触发预警 I=1；奇数长度的闭环不触发。

你的任务是：
1. 通过交互确定侦查规则 R 是 Alpha、Beta 还是 Gamma
2. 给出一个相对于 R 与当前关系的"最小触发集" S（流向的集合）：使得 I(S)=1，且对任一流向 e 属于 S，有 I(S去除e后)=0

## 允许的操作

你可以进行以下操作（每次只能进行一个操作）：

1. **流向状态设定**：设置某条流向为接通或切断状态
   格式：<set_edge>流向名,状态</set_edge>
   其中状态为"开启"（接通）或"关闭"（切断）
   例如：<set_edge>AB,开启</set_edge>

2. **指示器查询**：询问当前闭环预警指示器是否为1
   格式：<query_indicator></query_indicator>

3. **枚举查询**：询问当前已接通的流向有哪些
   格式：<query_edges></query_edges>

4. **数量查询**：询问当前已接通的流向数量
   格式：<query_count></query_count>

5. **规则宣告**：宣告你判定的侦查规则类型
   格式：<declare_rule>规则名</declare_rule>
   规则名为 Alpha、Beta 或 Gamma
   例如：<declare_rule>Alpha</declare_rule>

6. **最小性验证**：询问如果将某条流向切断，预警指示器是否变为0（这是一个假设性查询，不改变实际状态）
   格式：<verify_minimal>流向名</verify_minimal>
   例如：<verify_minimal>AB</verify_minimal>

7. **提交最终答案**：提交你的规则判定和最小触发集
   格式：<answer>rule=规则名, edges=流向名列表</answer>
   流向名用逗号分隔，顺序不限
   例如：<answer>rule=Alpha, edges=AB,BC,CA</answer>

## 任务要求

- 你需要尽可能少地使用操作次数完成追踪任务
- 成功条件：规则判定正确，且提交的流向集确实是最小触发集
- 若规则判定错误或流向集不是最小触发集，则追踪失败
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Legal Evidence & Capital Flow Tracing" system.

The system features a fixed case relation topology with nodes A, B, C, D, E, V, representing different case subjects or evidence, where V is the Core Suspect/Key Evidence. There are several controllable logical associations/capital flows (all initially disconnected):
- Domestic Transaction Triangle: AB, BC, CA
- Offshore Transaction Triangle: CD, DE, EC
- Cross-border Transfer Link: AD
- Flows related to Core Subject V: VA, VC, VD

The system is currently executing a core investigation qualification rule R (chosen from the following three, and it remains unchanged throughout the tracing). A binary closed-loop warning indicator I is given by applying rule R to the subgraph formed by currently connected flows:

**Rule Alpha**: I=1 if and only if there exists a capital/logical closed loop of any length (whether or not it includes Core Subject V).
**Rule Beta**: I=1 if and only if there exists at least one closed loop that includes Core Subject V; loops without V do not trigger.
**Rule Gamma**: I=1 if and only if there exists an even-subject closed loop (length 4, 6, etc., typical of bilateral dummy trading); odd-length loops do not trigger.

Your tasks are:
1. Determine through interaction whether investigation rule R is Alpha, Beta, or Gamma
2. Provide a "minimal trigger set" S (a set of flows) relative to R and the current relations: such that I(S)=1, and for any flow e in S, I(S without e)=0

## Allowed Operations

You can perform the following operations (one operation at a time):

1. **Flow State Setting**: Set a flow to connected or disconnected state
   Format: <set_edge>flow_name,state</set_edge>
   State is "open" (connected) or "closed" (disconnected)
   Example: <set_edge>AB,open</set_edge>

2. **Indicator Query**: Ask if the current warning indicator is 1
   Format: <query_indicator></query_indicator>

3. **Enumeration Query**: Ask which flows are currently connected
   Format: <query_edges></query_edges>

4. **Count Query**: Ask the number of currently connected flows
   Format: <query_count></query_count>

5. **Rule Declaration**: Declare the investigation rule type you have determined
   Format: <declare_rule>rule_name</declare_rule>
   Rule name is Alpha, Beta, or Gamma
   Example: <declare_rule>Alpha</declare_rule>

6. **Minimality Verification**: Ask if disconnecting a certain flow would make the indicator become 0 (this is a hypothetical query, does not change actual state)
   Format: <verify_minimal>flow_name</verify_minimal>
   Example: <verify_minimal>AB</verify_minimal>

7. **Submit Final Answer**: Submit your rule determination and minimal trigger set
   Format: <answer>rule=rule_name, edges=flow_list</answer>
   Flows are comma-separated, order does not matter
   Example: <answer>rule=Alpha, edges=AB,BC,CA</answer>

## Task Requirements

- You need to complete the tracing task using as few operations as possible
- Success conditions: correct rule determination and the submitted flow set is indeed a minimal trigger set
- If the rule determination is wrong or the flow set is not a minimal trigger set, the task fails
"""

    tags = ["answer", "set_edge", "query_indicator", "query_edges", "query_count", "declare_rule", "verify_minimal"]

    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "rule": "Alpha",
                "minimal_set": ["AB", "BC", "CA"],
            },
            2: {
                "rule": "Beta",
                "minimal_set": ["VA", "AB", "BC", "VC"],
            },
            3: {
                "rule": "Gamma",
                "minimal_set": ["AB", "BC", "CD", "AD"],
            },
            4: {
                "rule": "Beta",
                "minimal_set": ["VD", "DE", "EC", "BC", "AB", "VA"],
            },
            5: {
                "rule": "Gamma",
                "minimal_set": ["VA", "AD", "CD", "VC"],
            },
        },
        "en": {
            1: {
                "rule": "Alpha",
                "minimal_set": ["AB", "BC", "CA"],
            },
            2: {
                "rule": "Beta",
                "minimal_set": ["VA", "AB", "BC", "VC"],
            },
            3: {
                "rule": "Gamma",
                "minimal_set": ["AB", "BC", "CD", "AD"],
            },
            4: {
                "rule": "Beta",
                "minimal_set": ["VD", "DE", "EC", "BC", "AB", "VA"],
            },
            5: {
                "rule": "Gamma",
                "minimal_set": ["VA", "AD", "CD", "VC"],
            },
        },
    }

    ALL_EDGES = ["AB", "BC", "CA", "CD", "DE", "EC", "AD", "VA", "VC", "VD"]

    def __init__(self, config):
        self.edge_states = {edge: False for edge in self.ALL_EDGES}
        self.rule_declared = None
        self.operation_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["rule"] = cfg["rule"]
        self._game_info["minimal_set"] = set(cfg["minimal_set"])

        self.true_rule = cfg["rule"]
        self.true_minimal_set = set(cfg["minimal_set"])

    def _normalize_edge(self, edge):
        edge = edge.strip().upper()
        if len(edge) != 2:
            return edge
        # 尝试直接匹配
        if edge in self.ALL_EDGES:
            return edge
        # 尝试反转匹配
        reversed_edge = edge[1] + edge[0]
        if reversed_edge in self.ALL_EDGES:
            return reversed_edge
        return edge

    def _find_cycles(self, edges):
        if not edges:
            return []

        graph = {}
        for edge in edges:
            u, v = edge[0], edge[1]
            if u not in graph:
                graph[u] = []
            if v not in graph:
                graph[v] = []
            if v not in graph[u]:
                graph[u].append(v)
            if u not in graph[v]:
                graph[v].append(u)

        cycles = []
        seen = set()

        def _canonical(cycle):
            """将环规范化：找到最小旋转，并取正反两个方向中较小的"""
            n = len(cycle)
            # 正向所有旋转
            min_rot = tuple(cycle)
            for i in range(1, n):
                rot = tuple(cycle[i:] + cycle[:i])
                if rot < min_rot:
                    min_rot = rot
            # 反向所有旋转
            rev = cycle[::-1]
            for i in range(n):
                rot = tuple(rev[i:] + rev[:i])
                if rot < min_rot:
                    min_rot = rot
            return min_rot

        def dfs(start, current, visited, path):
            for neighbor in graph.get(current, []):
                if neighbor == start and len(path) >= 3:
                    cycle = path[:]
                    canon = _canonical(cycle)
                    if canon not in seen:
                        seen.add(canon)
                        cycles.append(cycle)
                elif neighbor not in visited:
                    visited.add(neighbor)
                    path.append(neighbor)
                    dfs(start, neighbor, visited, path)
                    path.pop()
                    visited.remove(neighbor)

        nodes = list(graph.keys())
        for start_node in nodes:
            visited = set([start_node])
            dfs(start_node, start_node, visited, [start_node])

        return cycles

    def _compute_indicator(self, edges):
        if not edges:
            return 0

        cycles = self._find_cycles(edges)
        
        if self.true_rule == "Alpha":
            return 1 if cycles else 0
        
        elif self.true_rule == "Beta":
            for cycle in cycles:
                if 'V' in cycle:
                    return 1
            return 0
        
        elif self.true_rule == "Gamma":
            for cycle in cycles:
                if len(cycle) % 2 == 0:
                    return 1
            return 0
        
        return 0

    def _get_open_edges(self):
        return [edge for edge, state in self.edge_states.items() if state]

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        parts = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        i = 0
        while i < len(parts):
            if "=" in parts[i]:
                key, value = parts[i].split("=", 1)
                key = key.strip()
                value = value.strip()
                
                if key == "edges":
                    edges = [value]
                    i += 1
                    while i < len(parts) and "=" not in parts[i]:
                        edges.append(parts[i].strip())
                        i += 1
                    ans_dict[key] = edges
                else:
                    ans_dict[key] = value
                    i += 1
            else:
                i += 1

        if "rule" not in ans_dict or "edges" not in ans_dict:
            return False

        declared_rule = ans_dict["rule"].strip()
        if declared_rule != self.true_rule:
            return False

        try:
            submitted_edges = set()
            for edge in ans_dict["edges"]:
                normalized = self._normalize_edge(edge)
                if normalized not in self.ALL_EDGES:
                    return False
                submitted_edges.add(normalized)
        except:
            return False

        normalized_minimal = set(self._normalize_edge(e) for e in self.true_minimal_set)
        normalized_submitted = set(self._normalize_edge(e) for e in submitted_edges)

        return normalized_submitted == normalized_minimal

    def _cf_core_produce(self, parsed_info):
        self.operation_count += 1
        lang = self.config.language
        
        if "set_edge" in parsed_info:
            try:
                content = parsed_info["set_edge"].strip()
                parts = content.split(",")
                if len(parts) != 2:
                    return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
                
                edge_name = self._normalize_edge(parts[0])
                state_str = parts[1].strip()
                
                if edge_name not in self.ALL_EDGES:
                    return "错误：边名无效。" if lang == "zh" else "Error: Invalid edge name."
                
                if lang == "zh":
                    if state_str == "开启" or state_str == "接通":
                        self.edge_states[edge_name] = True
                        return "已开启"
                    elif state_str == "关闭" or state_str == "切断":
                        self.edge_states[edge_name] = False
                        return "已关闭"
                    else:
                        return "错误：状态无效。"
                else:
                    if state_str.lower() in ["open", "connected"]:
                        self.edge_states[edge_name] = True
                        return "Opened"
                    elif state_str.lower() in ["closed", "disconnected"]:
                        self.edge_states[edge_name] = False
                        return "Closed"
                    else:
                        return "Error: Invalid state."
            except:
                return "错误：处理失败。" if lang == "zh" else "Error: Processing failed."

        elif "query_indicator" in parsed_info:
            open_edges = self._get_open_edges()
            indicator = self._compute_indicator(open_edges)
            return "是" if indicator == 1 else "否" if lang == "zh" else "Yes" if indicator == 1 else "No"

        elif "query_edges" in parsed_info:
            open_edges = self._get_open_edges()
            if not open_edges:
                return "无" if lang == "zh" else "None"
            return ", ".join(open_edges)

        elif "query_count" in parsed_info:
            open_edges = self._get_open_edges()
            return str(len(open_edges))

        elif "declare_rule" in parsed_info:
            rule = parsed_info["declare_rule"].strip()
            self.rule_declared = rule
            if rule == self.true_rule:
                return "正确" if lang == "zh" else "Correct"
            else:
                return "错误" if lang == "zh" else "Incorrect"

        elif "verify_minimal" in parsed_info:
            edge_name = self._normalize_edge(parsed_info["verify_minimal"])
            if edge_name not in self.ALL_EDGES:
                return "错误：边名/通道名/路径名无效。" if lang == "zh" else "Error: Invalid edge name."
            
            open_edges = self._get_open_edges()
            if edge_name not in open_edges:
                return "错误：该边当前未开启。" if lang == "zh" else "Error: This edge is not currently open."
            
            test_edges = [e for e in open_edges if e != edge_name]
            indicator = self._compute_indicator(test_edges)
            return "是" if indicator == 0 else "否" if lang == "zh" else "Yes" if indicator == 0 else "No"

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        lang = self.config.language
        open_edges = self._get_open_edges()

        ind_val = self._compute_indicator(open_edges)
        if lang == "zh":
            ans_ind = "是" if ind_val == 1 else "否"
        else:
            ans_ind = "Yes" if ind_val == 1 else "No"
        queries.append({"query": "<query_indicator></query_indicator>", "answer": ans_ind})

        if not open_edges:
            ans_edges = "无" if lang == "zh" else "None"
        else:
            ans_edges = ", ".join(open_edges)
        queries.append({"query": "<query_edges></query_edges>", "answer": ans_edges})

        queries.append({"query": "<query_count></query_count>", "answer": str(len(open_edges))})

        for rule in ["Alpha", "Beta", "Gamma"]:
            query_str = f"<declare_rule>{rule}</declare_rule>"
            if rule == self.true_rule:
                ans = "正确" if lang == "zh" else "Correct"
            else:
                ans = "错误" if lang == "zh" else "Incorrect"
            queries.append({"query": query_str, "answer": ans})

        for edge in self.ALL_EDGES:
            query_str = f"<verify_minimal>{edge}</verify_minimal>"
            
            if edge not in open_edges:
                if lang == "zh":
                    ans = "错误：该边当前未开启。"
                else:
                    ans = "Error: This edge is not currently open."
            else:
                test_edges = [e for e in open_edges if e != edge]
                val = self._compute_indicator(test_edges)
                if val == 0:
                    ans = "是" if lang == "zh" else "Yes"
                else:
                    ans = "否" if lang == "zh" else "No"
            
            queries.append({"query": query_str, "answer": ans})

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
        else:
            if correct.lower() == "yes":
                return "No" if correct[0].isupper() else "no"
            if correct.lower() == "no":
                return "Yes" if correct[0].isupper() else "yes"

        return correct + "_WRONG"