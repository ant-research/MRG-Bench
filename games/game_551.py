# -*- coding: utf-8 -*-

from .base import Game
import random


class HiddenDirectedGraphGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"
    
    game_rule_zh = """\
我们现在来玩一个"隐藏有向图探索"的推理游戏，规则如下：

游戏设定了一个隐藏的有向图，节点集合为 {{1..{n}}}。图中存在某些有向边，每个节点上可能有若干标签（从 {{G1, G2, G3, R}} 中选取），按下这些标签会让你沿着有向边移动到其他节点。

你的目标是判断是否存在一个节点 h，从该节点出发，通过有限次按压标签可以到达所有其他节点。如果你认为存在这样的节点，需要提交一个覆盖方案；如果你认为不存在，需要提交一个反证。

## 查询操作

你可以使用以下四种查询操作（总预算为 {budget} 点）：

1. **Peek 查询（消耗 1 点）**：查看节点 x 上存在哪些标签。
   - 格式：<query_peek>x</query_peek>
   - 返回：该节点上的标签集合，如 "G1,G2,R" 或 "None"（无标签）

2. **Press 查询（消耗 1 点）**：从节点 x 按下指定标签。
   - 格式：<query_press>x,label</query_press>
   - 返回：到达的节点编号，或 "None"（标签无效）

3. **Path 查询（消耗 k 点，k 为标签序列长度）**：从节点 x 依次按下一系列标签。
   - 格式：<query_path>x,label1,label2,...,labelk</query_path>
   - 返回：最终到达的节点编号，或 "None at step i"（第 i 步失败）

4. **Incoming 查询（消耗 1 点）**：查询是否存在某个节点能一步到达节点 x。
   - 格式：<query_incoming>x</query_incoming>
   - 返回：Yes 或 No

## 提交答案

你有最多 2 次提交机会（提交不消耗预算）：

**方案一：提交覆盖方案**（认为存在全局可达节点）

格式：
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

其中 h 是起始节点，每行给出从 h 到达其他节点 v 的标签序列。例如：
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**方案二：提交反证**（认为不存在全局可达节点）

格式：
<answer>
Refute u,v,L
</answer>

表示你认为不存在任何节点能在 L 步内同时到达节点 u 和节点 v。建议 L 大于等于 {n_minus_1}。

## 注意事项

- 请合理规划预算使用
- 查询结果始终一致，隐藏图结构固定不变
- 提交答案前请确保逻辑正确
"""

    game_rule_en = """\
Let's play a "Hidden Directed Graph Exploration" deduction game. Here are the rules:

The game has a hidden directed graph with node set {{1..{n}}}. There are some directed edges in the graph. Each node may have several labels (from {{G1, G2, G3, R}}). Pressing these labels moves you along directed edges to other nodes.

Your goal is to determine whether there exists a node h from which you can reach all other nodes through finite label presses. If you believe such a node exists, submit a coverage plan; if you believe it doesn't exist, submit a refutation.

## Query Operations

You can use the following four query operations (total budget: {budget} points):

1. **Peek Query (costs 1 point)**: View which labels exist on node x.
   - Format: <query_peek>x</query_peek>
   - Returns: Label set on the node, e.g., "G1,G2,R" or "None" (no labels)

2. **Press Query (costs 1 point)**: Press a specified label from node x.
   - Format: <query_press>x,label</query_press>
   - Returns: Node number reached, or "None" (invalid label)

3. **Path Query (costs k points, k is the length of label sequence)**: Press a series of labels from node x.
   - Format: <query_path>x,label1,label2,...,labelk</query_path>
   - Returns: Final node number reached, or "None at step i" (step i failed)

4. **Incoming Query (costs 1 point)**: Check if there exists a node that can reach node x in one step.
   - Format: <query_incoming>x</query_incoming>
   - Returns: Yes or No

## Submit Answer

You have at most 2 submission attempts (submissions don't consume budget):

**Option 1: Submit Coverage Plan** (believe a globally reachable node exists)

Format:
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

Where h is the starting node, each line gives a label sequence from h to other node v. Example:
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**Option 2: Submit Refutation** (believe no globally reachable node exists)

Format:
<answer>
Refute u,v,L
</answer>

Meaning you believe no node can reach both node u and node v within L steps. Suggest L greater than or equal to {n_minus_1}.

## Notes

- Plan your budget usage carefully
- Query results are always consistent; the hidden graph structure is fixed
- Ensure your logic is correct before submitting
"""

    contextualized_rule_zh_1 = """\
欢迎进入【智能交通调度排查】系统。

系统设定了一个隐藏的城市交通单向调度路网，节点集合为路口 {{1..{n}}}。路网中存在单向路段，每个路口处可能配置有若干引流调度指令标签（从 {{G1, G2, G3, R}} 中选取），激活这些指令可使车流沿单向路段转移至其他路口。

你的目标是判断是否存在一个主干总控枢纽 h，从该路口出发，通过有限次激活指令可以到达所有其他路口。如果你认为存在这样的总控枢纽，需要提交一个调度覆盖方案；如果你认为不存在，需要提交一个反证。

## 查询操作

你可以使用以下四种查询操作（总预算为 {budget} 点）：

1. **Peek 查询（消耗 1 点）**：查看路口 x 上配置了哪些指令标签。
   - 格式：<query_peek>x</query_peek>
   - 返回：该路口上的指令标签集合，如 "G1,G2,R" 或 "None"（无配置）

2. **Press 查询（消耗 1 点）**：在路口 x 激活指定指令标签。
   - 格式：<query_press>x,label</query_press>
   - 返回：到达的路口编号，或 "None"（指令无效）

3. **Path 查询（消耗 k 点，k 为标签序列长度）**：从路口 x 依次激活一系列指令标签。
   - 格式：<query_path>x,label1,label2,...,labelk</query_path>
   - 返回：最终到达的路口编号，或 "None at step i"（第 i 步流转失败）

4. **Incoming 查询（消耗 1 点）**：查询是否存在某个路口能一步转移车流到路口 x。
   - 格式：<query_incoming>x</query_incoming>
   - 返回：Yes 或 No

## 提交答案

你有最多 2 次提交机会（提交不消耗预算）：

**方案一：提交调度覆盖方案**（认为存在全局可达的主干枢纽）

格式：
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

其中 h 是主干枢纽路口，每行给出从 h 到达其他路口 v 的指令标签序列。例如：
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**方案二：提交反证**（认为不存在总控枢纽）

格式：
<answer>
Refute u,v,L
</answer>

表示你认为不存在任何路口能在 L 步内同时转移车流至路口 u 和路口 v。建议 L 大于等于 {n_minus_1}。

## 注意事项
- 请合理规划预算使用
- 查询结果始终一致，隐藏的交通调度路网结构固定不变
- 提交答案前请确保逻辑排查准确
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Dispatch Diagnosis System.

The system features a hidden urban one-way traffic dispatch network, with a node set of intersections {{1..{n}}}. There are one-way road segments in the network, and each intersection may have several dispatch command labels (from {{G1, G2, G3, R}}). Activating these commands transfers the traffic flow along one-way segments to other intersections.

Your goal is to determine whether there exists a main control hub h, from which you can reach all other intersections through finite command activations. If you believe such a hub exists, submit a dispatch coverage plan; if you believe it doesn't exist, submit a refutation.

## Query Operations

You can use the following four query operations (total budget: {budget} points):

1. **Peek Query (costs 1 point)**: View which command labels exist at intersection x.
   - Format: <query_peek>x</query_peek>
   - Returns: Label set at the intersection, e.g., "G1,G2,R" or "None" (no labels)

2. **Press Query (costs 1 point)**: Activate a specified command label at intersection x.
   - Format: <query_press>x,label</query_press>
   - Returns: Reached intersection number, or "None" (invalid command)

3. **Path Query (costs k points, k is the length of label sequence)**: Activate a series of command labels from intersection x.
   - Format: <query_path>x,label1,label2,...,labelk</query_path>
   - Returns: Final intersection number reached, or "None at step i" (step i failed)

4. **Incoming Query (costs 1 point)**: Check if there exists an intersection that can transfer traffic flow to intersection x in one step.
   - Format: <query_incoming>x</query_incoming>
   - Returns: Yes or No

## Submit Answer

You have at most 2 submission attempts (submissions don't consume budget):

**Option 1: Submit Dispatch Coverage Plan** (believe a globally reachable hub exists)

Format:
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

Where h is the main control hub intersection, each line gives a command sequence from h to other intersection v. Example:
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**Option 2: Submit Refutation** (believe no main control hub exists)

Format:
<answer>
Refute u,v,L
</answer>

Meaning you believe no intersection can transfer flow to both intersection u and intersection v within L steps. Suggest L greater than or equal to {n_minus_1}.

## Notes
- Plan your budget usage carefully
- Query results are always consistent; the hidden dispatch network structure is fixed
- Ensure your diagnostic logic is correct before submitting
"""

    contextualized_rule_zh_2 = """\
欢迎进入【流行病理传播溯源】系统。

系统记录了一个隐藏的疾病传导网络，节点集合为器官组织 {{1..{n}}}。网络中存在单向的病理扩散路径，每个器官上可能有若干传导途径标签（从 {{G1, G2, G3, R}} 中选取），触发这些标签会使病原体沿着扩散路径蔓延到其他器官。

你的目标是判断是否存在一个原发病灶 h，从该病灶出发，通过有限次蔓延可以感染所有其他器官。如果你认为存在这样的病灶，需要提交一个感染扩散方案；如果你认为不存在，需要提交一个反证。

## 查询操作

你可以使用以下四种溯源查询操作（总预算为 {budget} 点）：

1. **Peek 查询（消耗 1 点）**：查看器官 x 上存在哪些传导途径标签。
   - 格式：<query_peek>x</query_peek>
   - 返回：该器官上的途径标签集合，如 "G1,G2,R" 或 "None"（无扩散途径）

2. **Press 查询（消耗 1 点）**：在器官 x 触发指定传导途径标签。
   - 格式：<query_press>x,label</query_press>
   - 返回：被蔓延的器官编号，或 "None"（途径无效）

3. **Path 查询（消耗 k 点，k 为标签序列长度）**：从器官 x 依次触发一系列传导途径标签。
   - 格式：<query_path>x,label1,label2,...,labelk</query_path>
   - 返回：最终蔓延到的器官编号，或 "None at step i"（第 i 步感染失败）

4. **Incoming 查询（消耗 1 点）**：查询是否存在某个器官能一步将病原体扩散到器官 x。
   - 格式：<query_incoming>x</query_incoming>
   - 返回：Yes 或 No

## 提交答案

你有最多 2 次提交机会（提交不消耗预算）：

**方案一：提交感染扩散方案**（认为存在全局原发病灶）

格式：
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

其中 h 是原发病灶器官，每行给出从 h 感染其他器官 v 的途径序列。例如：
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**方案二：提交反证**（认为不存在全局原发病灶）

格式：
<answer>
Refute u,v,L
</answer>

表示你认为不存在任何器官能在 L 步内同时将疾病扩散至器官 u 和器官 v。建议 L 大于等于 {n_minus_1}。

## 注意事项
- 请合理分配临床排查预算
- 查询结果始终一致，隐藏的传导网络结构固定不变
- 提交答案前请确保病理溯源逻辑正确
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Epidemiological Pathology Tracing System.

The system records a hidden disease transmission network, with a node set of organs/tissues {{1..{n}}}. There are one-way diffusion pathways in the network, and each organ may have several transmission pathway labels (from {{G1, G2, G3, R}}). Triggering these labels spreads pathogens along diffusion pathways to other organs.

Your goal is to determine whether there exists a primary lesion h, from which pathogens can spread to all other organs through finite pathway triggers. If you believe such a primary lesion exists, submit an infection diffusion plan; if you believe it doesn't exist, submit a refutation.

## Query Operations

You can use the following four tracing query operations (total budget: {budget} points):

1. **Peek Query (costs 1 point)**: View which pathway labels exist on organ x.
   - Format: <query_peek>x</query_peek>
   - Returns: Label set on the organ, e.g., "G1,G2,R" or "None" (no diffusion pathways)

2. **Press Query (costs 1 point)**: Trigger a specified pathway label at organ x.
   - Format: <query_press>x,label</query_press>
   - Returns: Organ number reached by the spread, or "None" (invalid pathway)

3. **Path Query (costs k points, k is the length of label sequence)**: Trigger a series of pathway labels from organ x.
   - Format: <query_path>x,label1,label2,...,labelk</query_path>
   - Returns: Final organ number infected, or "None at step i" (step i failed)

4. **Incoming Query (costs 1 point)**: Check if there exists an organ that can directly spread pathogens to organ x in one step.
   - Format: <query_incoming>x</query_incoming>
   - Returns: Yes or No

## Submit Answer

You have at most 2 submission attempts (submissions don't consume budget):

**Option 1: Submit Infection Diffusion Plan** (believe a globally spreading primary lesion exists)

Format:
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

Where h is the primary lesion organ, each line gives a pathway sequence from h to other infected organ v. Example:
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**Option 2: Submit Refutation** (believe no global primary lesion exists)

Format:
<answer>
Refute u,v,L
</answer>

Meaning you believe no organ can spread the disease to both organ u and organ v within L steps. Suggest L greater than or equal to {n_minus_1}.

## Notes
- Allocate your clinical diagnostic budget carefully
- Query results are always consistent; the hidden transmission network structure is fixed
- Ensure your pathology tracing logic is correct before submitting
"""

    contextualized_rule_zh_3 = """\
欢迎进入【学科先修知识图谱推演】系统。

系统设定了一套隐藏的学科知识图谱，节点集合为核心知识点 {{1..{n}}}。图谱中存在单向的知识推导链路，每个知识点上可能有若干进阶学习标签（从 {{G1, G2, G3, R}} 中选取），掌握并应用这些标签会让你顺着链路推导学习到其他前沿知识点。

你的目标是判断是否存在一个核心公理节点 h，从该公理出发，通过有限次推导可以掌握所有其他知识点。如果你认为存在这样的核心公理，需要提交一个全知识掌握方案；如果你认为不存在，需要提交一个反证。

## 查询操作

你可以使用以下四种学习查询操作（总预算为 {budget} 点）：

1. **Peek 查询（消耗 1 点）**：查看知识点 x 上配置了哪些进阶学习标签。
   - 格式：<query_peek>x</query_peek>
   - 返回：该知识点上的标签集合，如 "G1,G2,R" 或 "None"（无进阶标签）

2. **Press 查询（消耗 1 点）**：在知识点 x 应用指定的进阶学习标签。
   - 格式：<query_press>x,label</query_press>
   - 返回：推导出的知识点编号，或 "None"（进阶无效）

3. **Path 查询（消耗 k 点，k 为标签序列长度）**：从知识点 x 依次应用一系列进阶学习标签。
   - 格式：<query_path>x,label1,label2,...,labelk</query_path>
   - 返回：最终掌握的知识点编号，或 "None at step i"（第 i 步推导失败）

4. **Incoming 查询（消耗 1 点）**：查询是否存在某个知识点能一步直接推导到知识点 x。
   - 格式：<query_incoming>x</query_incoming>
   - 返回：Yes 或 No

## 提交答案

你有最多 2 次提交机会（提交不消耗预算）：

**方案一：提交全知识掌握方案**（认为存在学科核心公理）

格式：
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

其中 h 是核心公理知识点，每行给出从 h 推导到其他知识点 v 的学习标签序列。例如：
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**方案二：提交反证**（认为不存在涵盖全图谱的核心公理）

格式：
<answer>
Refute u,v,L
</answer>

表示你认为不存在任何知识点能在 L 步内同时推导掌握知识点 u 和知识点 v。建议 L 大于等于 {n_minus_1}。

## 注意事项
- 请合理规划你的研究预算
- 查询结果始终一致，隐藏的知识图谱结构固定不变
- 提交答案前请确保推导逻辑正确无误
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Pre-requisite Knowledge Graph Deduction System.

The system defines a hidden academic knowledge graph, with a node set of core knowledge points {{1..{n}}}. There are one-way deduction links in the graph, and each knowledge point may have several learning progression labels (from {{G1, G2, G3, R}}). Mastering and applying these labels allows you to deduce and learn advanced knowledge points along the links.

Your goal is to determine whether there exists a core axiom node h, from which you can deduce and master all other knowledge points through finite progressions. If you believe such a core axiom exists, submit a comprehensive mastery plan; if you believe it doesn't exist, submit a refutation.

## Query Operations

You can use the following four study query operations (total budget: {budget} points):

1. **Peek Query (costs 1 point)**: View which progression labels exist on knowledge point x.
   - Format: <query_peek>x</query_peek>
   - Returns: Label set on the knowledge point, e.g., "G1,G2,R" or "None" (no progression labels)

2. **Press Query (costs 1 point)**: Apply a specified learning progression label at knowledge point x.
   - Format: <query_press>x,label</query_press>
   - Returns: Deduced knowledge point number, or "None" (invalid progression)

3. **Path Query (costs k points, k is the length of label sequence)**: Apply a series of progression labels from knowledge point x.
   - Format: <query_path>x,label1,label2,...,labelk</query_path>
   - Returns: Final knowledge point mastered, or "None at step i" (step i failed)

4. **Incoming Query (costs 1 point)**: Check if there exists a knowledge point that can directly deduce knowledge point x in one step.
   - Format: <query_incoming>x</query_incoming>
   - Returns: Yes or No

## Submit Answer

You have at most 2 submission attempts (submissions don't consume budget):

**Option 1: Submit Comprehensive Mastery Plan** (believe a global core axiom exists)

Format:
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

Where h is the core axiom knowledge point, each line gives a progression sequence from h to other knowledge point v. Example:
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**Option 2: Submit Refutation** (believe no global core axiom exists)

Format:
<answer>
Refute u,v,L
</answer>

Meaning you believe no knowledge point can deduce both knowledge point u and knowledge point v within L steps. Suggest L greater than or equal to {n_minus_1}.

## Notes
- Plan your research budget usage carefully
- Query results are always consistent; the hidden knowledge graph structure is fixed
- Ensure your deduction logic is correct before submitting
"""

    contextualized_rule_zh_4 = """\
欢迎进入【自动化流水线工艺溯源】系统。

系统模拟了一个隐藏的自动化装配流水线工艺网络，节点集合为加工工作站 {{1..{n}}}。网络中存在单向的物料流转轨道，每个工作站上可能配置有若干传送路由标签（从 {{G1, G2, G3, R}} 中选取），激活这些标签会使物料沿着传送带流转到下一个工序阶段的工作站。

你的目标是判断是否存在一个初始供料站 h，从该站出发，通过有限次路由操作可以将物料送达所有其他工作站。如果你认为存在这样的供料站，需要提交一个全工位配送方案；如果你认为不存在，需要提交一个反证。

## 查询操作

你可以使用以下四种工控查询操作（总预算为 {budget} 点）：

1. **Peek 查询（消耗 1 点）**：查看工作站 x 上存在哪些传送路由标签。
   - 格式：<query_peek>x</query_peek>
   - 返回：该工作站上的路由标签集合，如 "G1,G2,R" 或 "None"（无流转路由）

2. **Press 查询（消耗 1 点）**：在工作站 x 激活指定的传送路由标签。
   - 格式：<query_press>x,label</query_press>
   - 返回：物料到达的工作站编号，或 "None"（路由无效）

3. **Path 查询（消耗 k 点，k 为标签序列长度）**：从工作站 x 依次激活一系列传送路由标签。
   - 格式：<query_path>x,label1,label2,...,labelk</query_path>
   - 返回：最终物料到达的工作站编号，或 "None at step i"（第 i 步流转卡阻）

4. **Incoming 查询（消耗 1 点）**：查询是否存在某个工作站能一步将物料传送到工作站 x。
   - 格式：<query_incoming>x</query_incoming>
   - 返回：Yes 或 No

## 提交答案

你有最多 2 次提交机会（提交不消耗预算）：

**方案一：提交全工位配送方案**（认为存在全局供料站）

格式：
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

其中 h 是初始供料站，每行给出从 h 将物料送达到其他工作站 v 的路由序列。例如：
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**方案二：提交反证**（认为不存在全局单一供料节点）

格式：
<answer>
Refute u,v,L
</answer>

表示你认为不存在任何供料站能在 L 步内同时将物料流转至工作站 u 和工作站 v。建议 L 大于等于 {n_minus_1}。

## 注意事项
- 请合理使用调试诊断预算
- 查询结果始终一致，隐藏的工艺流水线结构固定不变
- 提交答案前请确保溯源逻辑正确
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Automated Assembly Line Process Tracing System.

The system simulates a hidden automated assembly line process network, with a node set of workstations {{1..{n}}}. There are one-way material transport tracks in the network, and each workstation may have several routing labels configured (from {{G1, G2, G3, R}}). Activating these labels transfers materials along the conveyor belt to the workstation of the next process stage.

Your goal is to determine whether there exists an initial feeder station h, from which materials can be delivered to all other workstations through finite routing operations. If you believe such a feeder station exists, submit a full-station delivery plan; if you believe it doesn't exist, submit a refutation.

## Query Operations

You can use the following four industrial control queries (total budget: {budget} points):

1. **Peek Query (costs 1 point)**: View which routing labels exist on workstation x.
   - Format: <query_peek>x</query_peek>
   - Returns: Label set on the workstation, e.g., "G1,G2,R" or "None" (no routing)

2. **Press Query (costs 1 point)**: Activate a specified routing label at workstation x.
   - Format: <query_press>x,label</query_press>
   - Returns: Reached workstation number, or "None" (invalid routing)

3. **Path Query (costs k points, k is the length of label sequence)**: Activate a series of routing labels from workstation x.
   - Format: <query_path>x,label1,label2,...,labelk</query_path>
   - Returns: Final workstation number reached, or "None at step i" (step i blocked)

4. **Incoming Query (costs 1 point)**: Check if there exists a workstation that can transfer material directly to workstation x in one step.
   - Format: <query_incoming>x</query_incoming>
   - Returns: Yes or No

## Submit Answer

You have at most 2 submission attempts (submissions don't consume budget):

**Option 1: Submit Full-Station Delivery Plan** (believe a global feeder station exists)

Format:
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

Where h is the initial feeder station, each line gives a routing sequence from h to other workstation v. Example:
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**Option 2: Submit Refutation** (believe no global initial feeder node exists)

Format:
<answer>
Refute u,v,L
</answer>

Meaning you believe no workstation can transfer materials to both workstation u and workstation v within L steps. Suggest L greater than or equal to {n_minus_1}.

## Notes
- Plan your diagnostic budget usage carefully
- Query results are always consistent; the hidden assembly line structure is fixed
- Ensure your tracing logic is correct before submitting
"""

    contextualized_rule_zh_5 = """\
欢迎使用【金融犯罪追踪及反洗钱审计】系统。

本系统重构了一个隐藏的跨境洗钱网络，节点集合为涉案账户 {{1..{n}}}。网络中存在单向资金流转渠道，每个账户上可能记录有若干转移手段标签（从 {{G1, G2, G3, R}} 中选取），执行这些标签操作会使资金沿着隐蔽的洗钱链路转移到下一个收款账户。

你的目标是判断是否存在一个资金源头账户 h，从该账户出发，通过有限次资金转移操作可以将黑金流入所有其他关联账户。如果你认为存在这样的源头账户，需要提交一个资金全量渗透方案；如果你认为不存在，需要提交一个反证（证据链断裂证明）。

## 查询操作

你可以使用以下四种审计查询操作（总预算为 {budget} 审计点数）：

1. **Peek 查询（消耗 1 点）**：调阅涉案账户 x 上存在哪些转移手段标签。
   - 格式：<query_peek>x</query_peek>
   - 返回：该账户记录的标签集合，如 "G1,G2,R" 或 "None"（无下游渠道）

2. **Press 查询（消耗 1 点）**：在账户 x 执行指定的转移手段标签追踪单笔转移。
   - 格式：<query_press>x,label</query_press>
   - 返回：资金流向的账户编号，或 "None"（该手段无效）

3. **Path 查询（消耗 k 点，k 为标签序列长度）**：从账户 x 依次追踪一系列转移操作。
   - 格式：<query_path>x,label1,label2,...,labelk</query_path>
   - 返回：资金最终抵达的账户编号，或 "None at step i"（第 i 步追踪失败）

4. **Incoming 查询（消耗 1 点）**：查询是否存在某个账户能单步将资金直接汇入账户 x。
   - 格式：<query_incoming>x</query_incoming>
   - 返回：Yes 或 No

## 提交答案

你有最多 2 次提交结案机会（提交不消耗预算）：

**方案一：提交资金全量渗透方案**（认为查实存在唯一的资金源头账户）

格式：
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

其中 h 是资金源头账户，每行给出从 h 洗钱至其他涉案账户 v 的转移手段序列。例如：
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**方案二：提交反证**（认为不存在单一的资金源头）

格式：
<answer>
Refute u,v,L
</answer>

表示你认为不存在任何账户能在 L 步内同时将资金流转至涉案账户 u 和涉案账户 v。建议 L 大于等于 {n_minus_1}。

## 注意事项
- 请在有限的审计资源内合理规划查询策略
- 调阅查询结果始终一致，隐藏的洗钱网络结构固定不变
- 提交结案前请确保证据链推理逻辑无懈可击
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Financial Crime Tracking and AML Audit System.

The system reconstructs a hidden cross-border money laundering network, with a node set of involved accounts {{1..{n}}}. There are one-way fund flow channels in the network, and each account may record several transfer method labels (from {{G1, G2, G3, R}}). Executing these labels transfers funds along concealed laundering links to the next receiving account.

Your goal is to determine whether there exists a source account h, from which illicit funds can flow into all other associated accounts through finite transfer operations. If you believe such a source account exists, submit a full-fund infiltration plan; if you believe it doesn't exist, submit a refutation (proof of broken evidence chain).

## Query Operations

You can use the following four audit query operations (total budget: {budget} audit points):

1. **Peek Query (costs 1 point)**: Review which transfer method labels exist on account x.
   - Format: <query_peek>x</query_peek>
   - Returns: Label set recorded on the account, e.g., "G1,G2,R" or "None" (no downstream channels)

2. **Press Query (costs 1 point)**: Trace a single transfer by executing a specified transfer method label at account x.
   - Format: <query_press>x,label</query_press>
   - Returns: Account number where funds flowed, or "None" (invalid method)

3. **Path Query (costs k points, k is the length of label sequence)**: Trace a series of transfer operations from account x.
   - Format: <query_path>x,label1,label2,...,labelk</query_path>
   - Returns: Final account number funds reached, or "None at step i" (step i tracking failed)

4. **Incoming Query (costs 1 point)**: Check if there exists an account that can remit funds directly into account x in a single step.
   - Format: <query_incoming>x</query_incoming>
   - Returns: Yes or No

## Submit Answer

You have at most 2 case submission attempts (submissions don't consume budget):

**Option 1: Submit Full-Fund Infiltration Plan** (believe a single source account exists)

Format:
<answer>
SubmitPlan h
v1: seq_v1
v2: seq_v2
...
</answer>

Where h is the source account, each line gives a transfer method sequence from h to other involved account v. Example:
<answer>
SubmitPlan 1
2: G1
3: G1,R
4: G2
</answer>

**Option 2: Submit Refutation** (believe no single source account exists)

Format:
<answer>
Refute u,v,L
</answer>

Meaning you believe no account can transfer funds to both account u and account v within L steps. Suggest L greater than or equal to {n_minus_1}.

## Notes
- Plan your inquiry strategy wisely within the limited audit resources
- Review query results are always consistent; the hidden laundering network structure is fixed
- Ensure your evidence chain deduction logic is flawless before submitting
"""

    tags = ["answer", "query_peek", "query_press", "query_path", "query_incoming"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "budget": 25,
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [1],
                    5: [2],
                    6: [2],
                    7: [3],
                    8: [4],
                },
                "root": 1,
            },
            2: {
                "n": 9,
                "budget": 25,
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [2],
                    5: [2],
                    6: [2],
                    7: [3],
                    8: [3],
                    9: [4],
                },
                "root": 1,
            },
            3: {
                "n": 10,
                "budget": 25,
                "tree": {
                    5: [],
                    1: [5],
                    2: [5],
                    3: [5],
                    4: [1],
                    6: [1],
                    7: [2],
                    8: [3],
                    9: [3],
                    10: [6],
                },
                "root": 5,
            },
            4: {
                "n": 11,
                "budget": 25,
                "tree": {
                    6: [],
                    1: [6],
                    2: [6],
                    3: [6],
                    4: [1],
                    5: [1],
                    7: [2],
                    8: [2],
                    9: [3],
                    10: [5],
                    11: [7],
                },
                "root": 6,
            },
            5: {
                "n": 12,
                "budget": 25,
                "tree": {
                    7: [],
                    1: [7],
                    2: [7],
                    3: [7],
                    4: [1],
                    5: [1],
                    6: [1],
                    8: [2],
                    9: [2],
                    10: [3],
                    11: [5],
                    12: [8],
                },
                "root": 7,
            },
        },
        "en": {
            1: {
                "n": 8,
                "budget": 25,
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [1],
                    5: [2],
                    6: [2],
                    7: [3],
                    8: [4],
                },
                "root": 1,
            },
            2: {
                "n": 9,
                "budget": 25,
                "tree": {
                    1: [],
                    2: [1],
                    3: [1],
                    4: [2],
                    5: [2],
                    6: [2],
                    7: [3],
                    8: [3],
                    9: [4],
                },
                "root": 1,
            },
            3: {
                "n": 10,
                "budget": 25,
                "tree": {
                    5: [],
                    1: [5],
                    2: [5],
                    3: [5],
                    4: [1],
                    6: [1],
                    7: [2],
                    8: [3],
                    9: [3],
                    10: [6],
                },
                "root": 5,
            },
            4: {
                "n": 11,
                "budget": 25,
                "tree": {
                    6: [],
                    1: [6],
                    2: [6],
                    3: [6],
                    4: [1],
                    5: [1],
                    7: [2],
                    8: [2],
                    9: [3],
                    10: [5],
                    11: [7],
                },
                "root": 6,
            },
            5: {
                "n": 12,
                "budget": 25,
                "tree": {
                    7: [],
                    1: [7],
                    2: [7],
                    3: [7],
                    4: [1],
                    5: [1],
                    6: [1],
                    8: [2],
                    9: [2],
                    10: [3],
                    11: [5],
                    12: [8],
                },
                "root": 7,
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
        self._game_info["n"] = cfg["n"]
        self._game_info["budget"] = cfg["budget"]
        self._game_info["n_minus_1"] = cfg["n"] - 1
        
        self.n = cfg["n"]
        self.budget = cfg["budget"]
        self.remaining_budget = cfg["budget"]
        self.root = cfg["root"]
        self.tree_structure = cfg["tree"]
        
        # 构建图结构：parent->children 映射，以及 children 在同一父节点下的顺序
        self.parent_map = {}  # node -> parent
        self.children_map = {}  # node -> [child1, child2, ...]
        
        # 从 tree_structure 构建父子关系
        for node, parents in self.tree_structure.items():
            if parents:
                parent = parents[0]
                self.parent_map[node] = parent
                if parent not in self.children_map:
                    self.children_map[parent] = []
                self.children_map[parent].append(node)
        
        # 构建标签映射：node -> {label: target_node}
        self.labels_map = {}  # node -> {label: target}
        
        for node in range(1, self.n + 1):
            self.labels_map[node] = {}
            
            # 添加子边标签 G1, G2, G3
            if node in self.children_map:
                children = self.children_map[node]
                for i, child in enumerate(children):
                    label = f"G{i+1}"
                    self.labels_map[node][label] = child
            
            # 添加兄弟横移标签 R
            if node in self.parent_map:
                parent = self.parent_map[node]
                siblings = self.children_map[parent]
                node_index = siblings.index(node)
                # 如果不是最后一个兄弟，添加 R 标签
                if node_index < len(siblings) - 1:
                    self.labels_map[node]["R"] = siblings[node_index + 1]
        
        self.submission_count = 0  # 提交次数计数

    def evaluate(self, parsed_info):
        """评估提交的答案"""
        answer_text = parsed_info["answer"].strip()
        
        # 判断是 SubmitPlan 还是 Refute
        if answer_text.startswith("SubmitPlan"):
            return self._evaluate_plan(answer_text)
        elif answer_text.startswith("Refute"):
            return self._evaluate_refute(answer_text)
        else:
            return False

    def _evaluate_plan(self, answer_text):
        """评估覆盖方案"""
        lines = [line.strip() for line in answer_text.split("\n") if line.strip()]
        
        if len(lines) < 1:
            return False
        
        # 解析起始节点 h
        first_line = lines[0]
        if not first_line.startswith("SubmitPlan"):
            return False
        
        try:
            h = int(first_line.split()[1])
        except:
            return False
        
        if h < 1 or h > self.n:
            return False
        
        # 解析路径方案
        paths = {}
        for line in lines[1:]:
            if ":" not in line:
                continue
            try:
                node_str, seq_str = line.split(":", 1)
                target = int(node_str.strip())
                seq = seq_str.strip()
                paths[target] = seq
            except:
                return False
        
        # 验证是否覆盖所有其他节点
        all_nodes = set(range(1, self.n + 1))
        all_nodes.discard(h)
        
        if set(paths.keys()) != all_nodes:
            return False
        
        # 验证每条路径是否正确
        for target, seq in paths.items():
            labels = [s.strip() for s in seq.split(",") if s.strip()]
            current = h
            for label in labels:
                if current not in self.labels_map or label not in self.labels_map[current]:
                    return False
                current = self.labels_map[current][label]
            
            if current != target:
                return False
        
        # 所有路径验证通过即可，无需硬编码检查根节点
        return True

    def _evaluate_refute(self, answer_text):
        """评估反证"""
        try:
            # 格式：Refute u,v,L
            parts = answer_text.replace("Refute", "").strip().split(",")
            if len(parts) != 3:
                return False
            
            u = int(parts[0].strip())
            v = int(parts[1].strip())
            L = int(parts[2].strip())
            
            if u < 1 or u > self.n or v < 1 or v > self.n:
                return False
            
            if u == v:
                return False
            
            # 检查是否所有节点 h 都无法在 L 步内同时到达 u 和 v
            # 如果存在某个节点能同时到达，则反证不成立
            for h in range(1, self.n + 1):
                can_reach_u = self._can_reach_in_steps(h, u, L)
                can_reach_v = self._can_reach_in_steps(h, v, L)
                
                if can_reach_u and can_reach_v:
                    # 存在一个节点能在 L 步内同时到达 u 和 v，反证失败
                    return False
            
            # 没有任何节点能在 L 步内同时到达 u 和 v，反证成立
            return True
            
        except:
            return False

    def _can_reach_in_steps(self, start, target, max_steps):
        """BFS检查从start能否在max_steps步内到达target"""
        if start == target:
            return True
        
        visited = {start}
        queue = [(start, 0)]
        
        while queue:
            node, steps = queue.pop(0)
            
            if steps >= max_steps:
                continue
            
            if node in self.labels_map:
                for label, next_node in self.labels_map[node].items():
                    if next_node == target:
                        return True
                    if next_node not in visited:
                        visited.add(next_node)
                        queue.append((next_node, steps + 1))
        
        return False

    def _cf_core_produce(self, parsed_info):
        """核心查询处理逻辑"""
        # 检查预算
        if self.remaining_budget <= 0:
            if self.config.language == "zh":
                return "预算已用尽。"
            else:
                return "Budget exhausted."
        
        # 优先级：peek > press > path > incoming
        if "query_peek" in parsed_info:
            cost = 1
            if self.remaining_budget < cost:
                return "预算不足。" if self.config.language == "zh" else "Insufficient budget."
            self.remaining_budget -= cost
            return self._handle_peek(parsed_info["query_peek"])
        
        elif "query_press" in parsed_info:
            cost = 1
            if self.remaining_budget < cost:
                return "预算不足。" if self.config.language == "zh" else "Insufficient budget."
            self.remaining_budget -= cost
            return self._handle_press(parsed_info["query_press"])
        
        elif "query_path" in parsed_info:
            query = parsed_info["query_path"]
            try:
                parts = [p.strip() for p in query.split(",")]
                cost = max(0, len(parts) - 1)
            except:
                cost = 0
                
            if cost > 0:
                if self.remaining_budget < cost:
                    return "预算不足。" if self.config.language == "zh" else "Insufficient budget."
                self.remaining_budget -= cost
            
            return self._handle_path(query)
        
        elif "query_incoming" in parsed_info:
            cost = 1
            if self.remaining_budget < cost:
                return "预算不足。" if self.config.language == "zh" else "Insufficient budget."
            self.remaining_budget -= cost
            return self._handle_incoming(parsed_info["query_incoming"])
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        # 处理纯数字（节点编号）
        if correct.isdigit():
            val = int(correct)
            # 确保返回一个不同的合法范围内的值
            wrong_val = val + 1 if val < self.n else val - 1
            return str(wrong_val)
        
        # 处理 Yes/No
        if correct.lower() == "yes":
            return "No"
        if correct.lower() == "no":
            return "Yes"
        
        # 处理 "None"
        if correct == "None":
            return "1"  # 返回一个存在的节点编号作为错误答案
        
        # 处理 "None at step i" 格式
        if correct.startswith("None at step"):
            return str(self.root)  # 返回根节点作为错误答案
        
        # 处理标签列表（如 "G1,G2,R"）
        if "," in correct and all(part.strip() in {"G1", "G2", "G3", "R"} for part in correct.split(",")):
            all_labels = {"G1", "G2", "G3", "R"}
            current_labels = {part.strip() for part in correct.split(",")}
            missing = all_labels - current_labels
            if missing:
                # 添加一个不存在的标签
                return correct + "," + sorted(missing)[0]
            else:
                # 去掉一个标签
                labels_list = [part.strip() for part in correct.split(",")]
                return ",".join(labels_list[:-1]) if len(labels_list) > 1 else "None"
        
        # 处理单个标签（如 "G1"）
        if correct.strip() in {"G1", "G2", "G3", "R"}:
            alternatives = {"G1", "G2", "G3", "R"} - {correct.strip()}
            return sorted(alternatives)[0]
        
        # 处理预算不足消息
        if "budget" in correct.lower() or "预算" in correct:
            return "1"
        
        return correct + "_WRONG"

    def _handle_peek(self, query):
        """处理 Peek 查询"""
        try:
            node = int(query.strip())
            if node < 1 or node > self.n:
                return "None"
            
            if node in self.labels_map and self.labels_map[node]:
                labels = sorted(self.labels_map[node].keys())
                return ",".join(labels)
            else:
                return "None"
        except:
            return "None"

    def _handle_press(self, query):
        """处理 Press 查询"""
        try:
            parts = query.split(",")
            if len(parts) != 2:
                return "None"
            
            node = int(parts[0].strip())
            label = parts[1].strip()
            
            if node < 1 or node > self.n:
                return "None"
            
            if node in self.labels_map and label in self.labels_map[node]:
                return str(self.labels_map[node][label])
            else:
                return "None"
        except:
            return "None"

    def _handle_path(self, query):
        """处理 Path 查询"""
        try:
            parts = [p.strip() for p in query.split(",")]
            if len(parts) < 1:
                return "None at step 1"
                
            node = int(parts[0])
            if node < 1 or node > self.n:
                return "None at step 1"
            
            if len(parts) < 2:
                return str(node)
            
            labels = parts[1:]
            
            current = node
            for i, label in enumerate(labels):
                if current not in self.labels_map or label not in self.labels_map[current]:
                    return f"None at step {i+1}"
                current = self.labels_map[current][label]
            
            return str(current)
        except:
            return "None at step 1"

    def _handle_incoming(self, query):
        """处理 Incoming 查询"""
        try:
            node = int(query.strip())
            if node < 1 or node > self.n:
                return "No"
            
            # 检查是否存在某个节点的某个标签指向该节点
            for src in range(1, self.n + 1):
                if src in self.labels_map:
                    for label, target in self.labels_map[src].items():
                        if target == node:
                            return "Yes"
            
            return "No"
        except:
            return "No"

    def step(self, response: str):
        """执行一步"""
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                # 检查提交次数
                self.submission_count += 1
                if self.submission_count > 2:
                    if self.config.language == "zh":
                        res = "提交次数已用完，答案错误。"
                    else:
                        res = "Submission limit exceeded, incorrect answer."
                    self.state.set_state("failed", "too many submissions")
                    self.state.add_message("user", res)
                else:
                    is_success = self.evaluate(parsed_info)
                    if is_success:
                        res = "答案正确" if self.config.language == "zh" else "Correct answer."
                        self.state.set_state("success", "success")
                        self.state.add_message("user", res)
                    else:
                        if self.submission_count >= 2:
                            res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                            self.state.set_state("failed", "incorrect answer")
                        else:
                            res = f"答案错误，你还有 {2 - self.submission_count} 次提交机会。" if self.config.language == "zh" else f"Incorrect answer, you have {2 - self.submission_count} submission(s) left."
                        self.state.add_message("user", res)
            else:
                # 处理查询
                game_response = self.produce_response(parsed_info)
                
                # 添加剩余预算信息
                budget_info = f"（剩余预算：{self.remaining_budget}）" if self.config.language == "zh" else f"(Remaining budget: {self.remaining_budget})"
                full_response = f"{game_response} {budget_info}"
                
                self.state.add_message("user", full_response)
                
                # 预算耗尽时提示但不直接结束游戏，允许玩家提交答案
                if self.remaining_budget <= 0:
                    warn_msg = "预算已耗尽，请直接提交你的答案。" if self.config.language == "zh" else "Budget exhausted, please submit your answer directly."
                    self.state.add_message("user", warn_msg)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state

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
        queries = []
        
        # 1. 枚举 Peek 查询 (1..n)
        for node in range(1, self.n + 1):
            query_str = str(node)
            # 使用内部处理函数避免副作用
            ans = self._handle_peek(query_str)
            queries.append({
                "query": f"<query_peek>{query_str}</query_peek>",
                "answer": ans
            })

        # 2. 枚举 Incoming 查询 (1..n)
        for node in range(1, self.n + 1):
            query_str = str(node)
            ans = self._handle_incoming(query_str)
            queries.append({
                "query": f"<query_incoming>{query_str}</query_incoming>",
                "answer": ans
            })

        # 3. 枚举 Press 查询 (1..n, labels=[G1, G2, G3, R])
        # 根据游戏规则，合法标签集合固定为 {{G1, G2, G3, R}}，即使该节点无此标签也可查询（返回 None）
        possible_labels = ["G1", "G2", "G3", "R"]
        for node in range(1, self.n + 1):
            for label in possible_labels:
                query_content = f"{node},{label}"
                ans = self._handle_press(query_content)
                queries.append({
                    "query": f"<query_press>{query_content}</query_press>",
                    "answer": ans
                })
        
        # 注意：不枚举 Path 查询，因为其组合空间巨大且本质上是 Press 的组合，
        # 且 Path 查询会修改预算状态，这里仅枚举描述图结构的基础原子查询。

        return queries