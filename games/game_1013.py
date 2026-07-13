# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   最大匹配规模：图中最大匹配包含多少条边
# ============================================================

import re
from itertools import combinations
from .base import Game


class BipartiteMatchingGame(Game):

    game_rule_zh = """\
我们来玩一个"二分图匹配推理"游戏，规则如下：

游戏中有一个二分图结构：左侧有 4 个顶点 L1, L2, L3, L4，右侧有 4 个顶点 R1, R2, R3, R4。每个顶点都有两个二值属性 (X, Y)，其中 X 和 Y 的取值均为 0 或 1。

我已经秘密选定了一个"顶点属性布局"和一个"可连边判定规则"：

**候选顶点属性布局（三选一）：**
- 布局 I：左侧 L1(0,0), L2(0,0), L3(1,1), L4(1,1)；右侧 R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- 布局 II：左侧 L1(0,0), L2(0,1), L3(0,1), L4(1,0)；右侧 R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- 布局 III：左侧 L1(0,0), L2(1,0), L3(1,0), L4(1,1)；右侧 R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**候选可连边判定规则（三选一）：**
- 规则 A（X 异）：左顶点 Li 和右顶点 Rj 之间存在边，当且仅当它们的 X 属性值不同
- 规则 B（Y 异）：左顶点 Li 和右顶点 Rj 之间存在边，当且仅当它们的 Y 属性值不同
- 规则 C（双异）：左顶点 Li 和右顶点 Rj 之间存在边，当且仅当它们的 X 属性值不同且 Y 属性值不同

你的目标是推断出实际使用的布局类型（I/II/III）、规则类型（A/B/C），以及在该组合下全图（所有 8 个顶点）的最大匹配规模。

## 你可以进行的询问

每次可以提出一个询问，指定左侧顶点子集 S 和右侧顶点子集 T，其中 S 的大小为 2 或 3，T 的大小也为 2 或 3。我会返回在 S 和 T 之间诱导的二分子图的最大匹配规模（一个整数，范围 0 到 3）。

**询问格式：**
<query>L1,L2;R1,R3</query>

说明：左侧顶点用逗号分隔，右侧顶点用逗号分隔，两侧用分号分隔。

**返回示例：**
如果该子图的最大匹配规模为 2，我会回复：2

你需要收集足够的信息后，提交最终答案。

## 提交最终答案的格式

<answer>layout=I, rule=A, max_matching=3</answer>

说明：
- layout 为 I、II 或 III
- rule 为 A、B 或 C
- max_matching 为全图的最大匹配规模（整数）

三项必须全部正确才算成功。
"""

    game_rule_en = """\
Let's play a "Bipartite Matching Deduction" game. Here are the rules:

The game involves a bipartite graph structure: the left side has 4 vertices L1, L2, L3, L4, and the right side has 4 vertices R1, R2, R3, R4. Each vertex has two binary attributes (X, Y), where both X and Y take values in {{0, 1}}.

I have secretly selected a "vertex attribute layout" and an "edge connectivity rule":

**Candidate Vertex Attribute Layouts (choose one):**
- Layout I: Left L1(0,0), L2(0,0), L3(1,1), L4(1,1); Right R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- Layout II: Left L1(0,0), L2(0,1), L3(0,1), L4(1,0); Right R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- Layout III: Left L1(0,0), L2(1,0), L3(1,0), L4(1,1); Right R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**Candidate Edge Connectivity Rules (choose one):**
- Rule A (X differs): An edge exists between left vertex Li and right vertex Rj if and only if their X attribute values differ
- Rule B (Y differs): An edge exists between left vertex Li and right vertex Rj if and only if their Y attribute values differ
- Rule C (both differ): An edge exists between left vertex Li and right vertex Rj if and only if both their X and Y attribute values differ

Your goal is to deduce the actual layout type (I/II/III), rule type (A/B/C), and the maximum matching size of the full graph (all 8 vertices) under this combination.

## Queries You Can Make

Each query specifies a left vertex subset S and a right vertex subset T, where the size of S is 2 or 3, and the size of T is also 2 or 3. I will return the maximum matching size of the induced bipartite subgraph between S and T (an integer from 0 to 3).

**Query Format:**
<query>L1,L2;R1,R3</query>

Note: Left vertices are separated by commas, right vertices are separated by commas, and the two sides are separated by a semicolon.

**Response Example:**
If the maximum matching size of this subgraph is 2, I will reply: 2

You need to gather sufficient information before submitting your final answer.

## Final Answer Format

<answer>layout=I, rule=A, max_matching=3</answer>

Note:
- layout should be I, II, or III
- rule should be A, B, or C
- max_matching is the maximum matching size of the full graph (integer)

All three items must be correct to succeed.
"""

    contextualized_rule_zh_1 = """\
基于交通规划场景的"智能调度匹配推理"系统，规则如下：

我们正在开发一套智能交通调度系统。系统网络包含 4 个调度中心 L1, L2, L3, L4（左侧节点）和 4 个车队枢纽 R1, R2, R3, R4（右侧节点）。每个节点具备两个二值属性 (X, Y)，X 和 Y 的取值均为 0 或 1，分别代表“是否具备高速公路直通权限”与“是否支持重载特种车辆”。

系统内部预设了一个"节点属性布局"和一个"有效路线判定规则"：

**候选节点属性布局（三选一）：**
- 布局 I：左侧 L1(0,0), L2(0,0), L3(1,1), L4(1,1)；右侧 R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- 布局 II：左侧 L1(0,0), L2(0,1), L3(0,1), L4(1,0)；右侧 R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- 布局 III：左侧 L1(0,0), L2(1,0), L3(1,0), L4(1,1)；右侧 R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**候选有效路线判定规则（三选一）：**
- 规则 A（X 异）：调度中心 Li 和枢纽 Rj 之间存在有效调度路线，当且仅当它们的高速直通权限（X）属性不同，以形成路权互补
- 规则 B（Y 异）：调度中心 Li 和枢纽 Rj 之间存在有效调度路线，当且仅当它们的重载支持（Y）属性不同，以实现运力混编
- 规则 C（双异）：调度中心 Li 和枢纽 Rj 之间存在有效调度路线，当且仅当它们的 X 属性和 Y 属性均不同

你的目标是推断出实际使用的布局类型（I/II/III）、规则类型（A/B/C），以及在该组合下全网（所有 8 个节点）的最大并发调度路线数（最大匹配规模）。

## 你可以进行的询问
每次可以提出一个询问，指定左侧调度中心子集 S 和右侧枢纽子集 T，其中 S 和 T 的大小均为 2 或 3。我会返回在 S 和 T 之间诱导的子网的最大并发调度路线数（一个整数，范围 0 到 3）。

**询问格式：**
<query>L1,L2;R1,R3</query>

**返回示例：**
如果该子网的最大并发调度路线数为 2，我会回复：2

你需要收集足够的信息后，提交最终答案。

## 提交最终答案的格式
<answer>layout=I, rule=A, max_matching=3</answer>
（三项必须全部正确才算成功。）
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "Smart Dispatch Matching Deduction" game based on traffic planning. Here are the rules:

We are developing an intelligent traffic dispatch system. The network involves 4 Dispatch Centers L1, L2, L3, L4 (left nodes) and 4 Fleet Hubs R1, R2, R3, R4 (right nodes). Each node possesses two binary attributes (X, Y) taking values in {{0, 1}}, representing "Highway Access Permission" and "Heavy-Duty Vehicle Support" respectively.

The system has a secretly predefined "node attribute layout" and a "valid route connectivity rule":

**Candidate Node Attribute Layouts (choose one):**
- Layout I: Left L1(0,0), L2(0,0), L3(1,1), L4(1,1); Right R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- Layout II: Left L1(0,0), L2(0,1), L3(0,1), L4(1,0); Right R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- Layout III: Left L1(0,0), L2(1,0), L3(1,0), L4(1,1); Right R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**Candidate Valid Route Connectivity Rules (choose one):**
- Rule A (X differs): A valid dispatch route exists between center Li and hub Rj if and only if their Highway Access (X) attributes differ, ensuring route complementarity
- Rule B (Y differs): A valid dispatch route exists between center Li and hub Rj if and only if their Heavy-Duty Support (Y) attributes differ, enabling mixed capacity dispatch
- Rule C (both differ): A valid dispatch route exists between center Li and hub Rj if and only if both their X and Y attributes differ

Your goal is to deduce the actual layout type (I/II/III), rule type (A/B/C), and the maximum concurrent dispatch routes (maximum matching size) of the full network (all 8 nodes) under this combination.

## Queries You Can Make
Each query specifies a subset S of dispatch centers and a subset T of fleet hubs, where the sizes of both S and T are 2 or 3. I will return the maximum concurrent dispatch routes (an integer from 0 to 3) within the induced subnetwork between S and T.

**Query Format:**
<query>L1,L2;R1,R3</query>

**Response Example:**
If the maximum concurrent dispatch routes for this subnetwork is 2, I will reply: 2

You need to gather sufficient information before submitting your final answer.

## Final Answer Format
<answer>layout=I, rule=A, max_matching=3</answer>
(All three items must be correct to succeed.)
"""

    contextualized_rule_zh_2 = """\
基于医疗器官移植场景的"供受体配型推理"系统，规则如下：

我们正在构建一个器官移植智能匹配数据库。包含 4 名潜在供体 L1, L2, L3, L4（左侧顶点）和 4 名等待受体 R1, R2, R3, R4（右侧顶点）。每个对象具有两个基因标志物属性 (X, Y)，X 和 Y 的取值均为 0 或 1，分别代表“血液表面抗原”与“组织相容性分型”。

数据库中锁定了一个"标志物属性布局"和一个"成功配型判定规则"：

**候选标志物属性布局（三选一）：**
- 布局 I：供体 L1(0,0), L2(0,0), L3(1,1), L4(1,1)；受体 R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- 布局 II：供体 L1(0,0), L2(0,1), L3(0,1), L4(1,0)；受体 R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- 布局 III：供体 L1(0,0), L2(1,0), L3(1,0), L4(1,1)；受体 R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**候选成功配型判定规则（三选一）：**
- 规则 A（X 异）：供体 Li 和受体 Rj 之间配型成功，当且仅当它们的血液抗原（X）属性不同（触发特定的免疫耐受）
- 规则 B（Y 异）：供体 Li 和受体 Rj 之间配型成功，当且仅当它们的组织相容性（Y）属性不同
- 规则 C（双异）：供体 Li 和受体 Rj 之间配型成功，当且仅当它们的 X 和 Y 属性均不同

你的目标是推断出实际使用的布局类型（I/II/III）、规则类型（A/B/C），以及在该组合下整个队列（所有 8 名对象）的最大成功移植对数（最大匹配规模）。

## 你可以进行的询问
每次可以提出一个询问，指定供体子集 S 和受体子集 T，其中 S 和 T 的大小均为 2 或 3。我会返回在 S 和 T 之间构成的子队列中的最大成功移植对数（一个整数，范围 0 到 3）。

**询问格式：**
<query>L1,L2;R1,R3</query>

**返回示例：**
如果该子队列的最大成功移植对数为 2，我会回复：2

你需要收集足够的信息后，提交最终答案。

## 提交最终答案的格式
<answer>layout=I, rule=A, max_matching=3</answer>
（三项必须全部正确才算成功。）
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play an "Organ Transplant Matching Deduction" game based on medical compatibility. Here are the rules:

We are building a smart organ transplant matching database. It contains 4 potential donors L1, L2, L3, L4 (left vertices) and 4 waitlisted recipients R1, R2, R3, R4 (right vertices). Each individual has two genetic marker attributes (X, Y) taking values in {{0, 1}}, representing "Blood Surface Antigen" and "Histocompatibility Typing" respectively.

The database operates under a locked "marker attribute layout" and a "successful compatibility rule":

**Candidate Marker Attribute Layouts (choose one):**
- Layout I: Donors L1(0,0), L2(0,0), L3(1,1), L4(1,1); Recipients R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- Layout II: Donors L1(0,0), L2(0,1), L3(0,1), L4(1,0); Recipients R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- Layout III: Donors L1(0,0), L2(1,0), L3(1,0), L4(1,1); Recipients R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**Candidate Successful Compatibility Rules (choose one):**
- Rule A (X differs): A successful transplant match exists between donor Li and recipient Rj if and only if their Blood Antigen (X) attributes differ (triggering specific immune tolerance)
- Rule B (Y differs): A successful transplant match exists between donor Li and recipient Rj if and only if their Histocompatibility (Y) attributes differ
- Rule C (both differ): A successful transplant match exists between donor Li and recipient Rj if and only if both their X and Y attributes differ

Your goal is to deduce the actual layout type (I/II/III), rule type (A/B/C), and the maximum number of successful transplant pairs (maximum matching size) for the entire cohort (all 8 individuals) under this combination.

## Queries You Can Make
Each query specifies a donor subset S and a recipient subset T, where the sizes of both S and T are 2 or 3. I will return the maximum number of successful transplant pairs (an integer from 0 to 3) within the induced sub-cohort between S and T.

**Query Format:**
<query>L1,L2;R1,R3</query>

**Response Example:**
If the maximum successful transplant pairs for this sub-cohort is 2, I will reply: 2

You need to gather sufficient information before submitting your final answer.

## Final Answer Format
<answer>layout=I, rule=A, max_matching=3</answer>
(All three items must be correct to succeed.)
"""

    contextualized_rule_zh_3 = """\
基于跨学科教育场景的"师生互选推理"平台，规则如下：

我们正在规划一个跨学科师生双选平台。平台库内有 4 名导师 L1, L2, L3, L4（左侧顶点）和 4 个学生项目组 R1, R2, R3, R4（右侧顶点）。每个对象均有两个教学偏好属性 (X, Y)，取值均为 0 或 1，分别代表“侧重理论与否”及“采用创新教法与否”。

平台后台已生成了一个"教学属性布局"和一个"有效指导匹配规则"：

**候选教学属性布局（三选一）：**
- 布局 I：导师 L1(0,0), L2(0,0), L3(1,1), L4(1,1)；项目组 R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- 布局 II：导师 L1(0,0), L2(0,1), L3(0,1), L4(1,0)；项目组 R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- 布局 III：导师 L1(0,0), L2(1,0), L3(1,0), L4(1,1)；项目组 R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**候选有效指导匹配规则（三选一）：**
- 规则 A（X 异）：导师 Li 和项目组 Rj 之间能形成有效指导关系，当且仅当他们的理论侧重点（X）不同（以促进交叉融合）
- 规则 B（Y 异）：导师 Li 和项目组 Rj 之间能形成有效指导关系，当且仅当他们的教法风格（Y）不同
- 规则 C（双异）：导师 Li 和项目组 Rj 之间能形成有效指导关系，当且仅当他们的 X 和 Y 属性均不同

你的目标是推断出实际使用的布局类型（I/II/III）、规则类型（A/B/C），以及在该组合下全部对象（共 8 个）的最大并发指导配对数（最大匹配规模）。

## 你可以进行的询问
每次可以提出一个询问，指定导师子集 S 和项目组子集 T，其中 S 和 T 的大小均为 2 或 3。我会返回在 S 和 T 之间诱导的最大并发指导配对数（一个整数，范围 0 到 3）。

**询问格式：**
<query>L1,L2;R1,R3</query>

**返回示例：**
如果该组群的最大并发指导配对数为 2，我会回复：2

你需要收集足够的信息后，提交最终答案。

## 提交最终答案的格式
<answer>layout=I, rule=A, max_matching=3</answer>
（三项必须全部正确才算成功。）
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play an "Academic Mentorship Matching Deduction" game based on interdisciplinary education. Here are the rules:

We are planning a cross-disciplinary mentor-student selection platform. The platform includes 4 Mentors L1, L2, L3, L4 (left vertices) and 4 Student Project Groups R1, R2, R3, R4 (right vertices). Each participant has two pedagogical attributes (X, Y) taking values in {{0, 1}}, representing "Theoretical Focus" and "Innovative Methodology" respectively.

The backend has generated a "pedagogical attribute layout" and an "effective mentorship matching rule":

**Candidate Pedagogical Attribute Layouts (choose one):**
- Layout I: Mentors L1(0,0), L2(0,0), L3(1,1), L4(1,1); Groups R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- Layout II: Mentors L1(0,0), L2(0,1), L3(0,1), L4(1,0); Groups R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- Layout III: Mentors L1(0,0), L2(1,0), L3(1,0), L4(1,1); Groups R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**Candidate Effective Mentorship Matching Rules (choose one):**
- Rule A (X differs): An effective mentorship relationship exists between mentor Li and group Rj if and only if their Theoretical Focus (X) attributes differ (promoting interdisciplinary fusion)
- Rule B (Y differs): An effective mentorship relationship exists between mentor Li and group Rj if and only if their Methodology (Y) attributes differ
- Rule C (both differ): An effective mentorship relationship exists between mentor Li and group Rj if and only if both their X and Y attributes differ

Your goal is to deduce the actual layout type (I/II/III), rule type (A/B/C), and the maximum concurrent mentorship pairings (maximum matching size) for all participants (all 8 entities) under this combination.

## Queries You Can Make
Each query specifies a mentor subset S and a group subset T, where the sizes of both S and T are 2 or 3. I will return the maximum concurrent mentorship pairings (an integer from 0 to 3) within the induced subgroup between S and T.

**Query Format:**
<query>L1,L2;R1,R3</query>

**Response Example:**
If the maximum concurrent mentorship pairings for this subgroup is 2, I will reply: 2

You need to gather sufficient information before submitting your final answer.

## Final Answer Format
<answer>layout=I, rule=A, max_matching=3</answer>
(All three items must be correct to succeed.)
"""

    contextualized_rule_zh_4 = """\
基于工业制造供应链场景的"产能网络配置推理"，规则如下：

我们正在优化一个工业供应链网络。该网络包含 4 条总装线 L1, L2, L3, L4（左侧节点）和 4 家零件供应商 R1, R2, R3, R4（右侧节点）。每个实体具有两个工艺参数属性 (X, Y)，X 和 Y 的取值均为 0 或 1，分别代表“精度标准等级”与“复合材料规格”。

系统中预设了一个"工艺参数布局"和一个"有效供应合同判定规则"：

**候选工艺参数布局（三选一）：**
- 布局 I：总装线 L1(0,0), L2(0,0), L3(1,1), L4(1,1)；供应商 R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- 布局 II：总装线 L1(0,0), L2(0,1), L3(0,1), L4(1,0)；供应商 R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- 布局 III：总装线 L1(0,0), L2(1,0), L3(1,0), L4(1,1)；供应商 R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**候选有效供应合同判定规则（三选一）：**
- 规则 A（X 异）：总装线 Li 和供应商 Rj 之间能签署有效供应合同，当且仅当它们的精度标准（X）属性不同（触发高低精度互补装配）
- 规则 B（Y 异）：总装线 Li 和供应商 Rj 之间能签署有效供应合同，当且仅当它们的材料规格（Y）属性不同
- 规则 C（双异）：总装线 Li 和供应商 Rj 之间能签署有效供应合同，当且仅当它们的 X 和 Y 属性均不同

你的目标是推断出实际使用的布局类型（I/II/III）、规则类型（A/B/C），以及在该组合下整个供应链（所有 8 个节点）的最大并行合同数（最大匹配规模）。

## 你可以进行的询问
每次可以提出一个询问，指定总装线子集 S 和供应商子集 T，其中 S 和 T 的大小均为 2 或 3。我会返回在 S 和 T 之间诱导的子供应链网络中的最大并行合同数（一个整数，范围 0 到 3）。

**询问格式：**
<query>L1,L2;R1,R3</query>

**返回示例：**
如果该子网络的最大并行合同数为 2，我会回复：2

你需要收集足够的信息后，提交最终答案。

## 提交最终答案的格式
<answer>layout=I, rule=A, max_matching=3</answer>
（三项必须全部正确才算成功。）
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play a "Capacity Network Configuration Deduction" game based on industrial supply chains. Here are the rules:

We are optimizing an industrial supply chain network. The network includes 4 Assembly Lines L1, L2, L3, L4 (left nodes) and 4 Component Suppliers R1, R2, R3, R4 (right nodes). Each entity has two technical parameter attributes (X, Y) taking values in {{0, 1}}, representing "Precision Standard Level" and "Composite Material Spec" respectively.

The system is configured with a "technical parameter layout" and a "valid supply contract rule":

**Candidate Technical Parameter Layouts (choose one):**
- Layout I: Lines L1(0,0), L2(0,0), L3(1,1), L4(1,1); Suppliers R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- Layout II: Lines L1(0,0), L2(0,1), L3(0,1), L4(1,0); Suppliers R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- Layout III: Lines L1(0,0), L2(1,0), L3(1,0), L4(1,1); Suppliers R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**Candidate Valid Supply Contract Rules (choose one):**
- Rule A (X differs): A valid supply contract can be signed between line Li and supplier Rj if and only if their Precision Standard (X) attributes differ (triggering complementary precision assembly)
- Rule B (Y differs): A valid supply contract can be signed between line Li and supplier Rj if and only if their Material Spec (Y) attributes differ
- Rule C (both differ): A valid supply contract can be signed between line Li and supplier Rj if and only if both their X and Y attributes differ

Your goal is to deduce the actual layout type (I/II/III), rule type (A/B/C), and the maximum parallel supply contracts (maximum matching size) of the entire supply chain (all 8 nodes) under this combination.

## Queries You Can Make
Each query specifies an assembly line subset S and a supplier subset T, where the sizes of both S and T are 2 or 3. I will return the maximum parallel supply contracts (an integer from 0 to 3) within the induced sub-network between S and T.

**Query Format:**
<query>L1,L2;R1,R3</query>

**Response Example:**
If the maximum parallel supply contracts for this sub-network is 2, I will reply: 2

You need to gather sufficient information before submitting your final answer.

## Final Answer Format
<answer>layout=I, rule=A, max_matching=3</answer>
(All three items must be correct to succeed.)
"""

    contextualized_rule_zh_5 = """\
基于法律案件委派场景的"无冲突代理匹配推理"，规则如下：

我们正在为一家大型律所设计案件委派系统。系统收录了 4 名合伙人律师 L1, L2, L3, L4（左侧顶点）和 4 个企业客户 R1, R2, R3, R4（右侧顶点）。每个主体均有两个法务属性 (X, Y)，X 和 Y 的取值均为 0 或 1，分别代表“专精业务领域（民商事/刑事）”与“熟悉司法管辖区（州级/联邦）”。

系统底层固化了一个"法务属性布局"和一个"有效代理关系判定规则"：

**候选法务属性布局（三选一）：**
- 布局 I：律师 L1(0,0), L2(0,0), L3(1,1), L4(1,1)；客户 R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- 布局 II：律师 L1(0,0), L2(0,1), L3(0,1), L4(1,0)；客户 R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- 布局 III：律师 L1(0,0), L2(1,0), L3(1,0), L4(1,1)；客户 R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**候选有效代理判定规则（三选一）：**
- 规则 A（X 异）：律师 Li 和客户 Rj 之间能建立合规的代理关系，当且仅当他们的业务领域（X）属性不同（触发跨领域交叉顾问需求）
- 规则 B（Y 异）：律师 Li 和客户 Rj 之间能建立合规的代理关系，当且仅当他们的司法管辖区（Y）属性不同
- 规则 C（双异）：律师 Li 和客户 Rj 之间能建立合规的代理关系，当且仅当他们的 X 和 Y 属性均不同

你的目标是推断出实际使用的布局类型（I/II/III）、规则类型（A/B/C），以及在该组合下整个案件组（所有 8 个主体）的最大并发代理案数（最大匹配规模）。

## 你可以进行的询问
每次可以提出一个询问，指定律师子集 S 和企业客户子集 T，其中 S 和 T 的大小均为 2 或 3。我会返回在 S 和 T 之间构成的小型委派网络中的最大并发代理案数（一个整数，范围 0 到 3）。

**询问格式：**
<query>L1,L2;R1,R3</query>

**返回示例：**
如果该组委派网络的最大并发代理案数为 2，我会回复：2

你需要收集足够的信息后，提交最终答案。

## 提交最终答案的格式
<answer>layout=I, rule=A, max_matching=3</answer>
（三项必须全部正确才算成功。）
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Conflict-Free Representation Deduction" game based on legal case delegation. Here are the rules:

We are designing a case delegation system for a major law firm. The system includes 4 Partner Attorneys L1, L2, L3, L4 (left vertices) and 4 Corporate Clients R1, R2, R3, R4 (right vertices). Each entity has two legal attributes (X, Y) taking values in {{0, 1}}, representing "Specialty Domain (Civil/Criminal)" and "Jurisdictional Familiarity (State/Federal)" respectively.

The system internally relies on a fixed "legal attribute layout" and a "valid retainer connectivity rule":

**Candidate Legal Attribute Layouts (choose one):**
- Layout I: Attorneys L1(0,0), L2(0,0), L3(1,1), L4(1,1); Clients R1(1,0), R2(1,0), R3(1,1), R4(0,1)
- Layout II: Attorneys L1(0,0), L2(0,1), L3(0,1), L4(1,0); Clients R1(0,0), R2(1,0), R3(1,1), R4(1,1)
- Layout III: Attorneys L1(0,0), L2(1,0), L3(1,0), L4(1,1); Clients R1(0,0), R2(0,0), R3(1,1), R4(1,1)

**Candidate Valid Retainer Connectivity Rules (choose one):**
- Rule A (X differs): A compliant retainer relationship exists between attorney Li and client Rj if and only if their Specialty Domain (X) attributes differ (triggering cross-specialty advisory needs)
- Rule B (Y differs): A compliant retainer relationship exists between attorney Li and client Rj if and only if their Jurisdictional Familiarity (Y) attributes differ
- Rule C (both differ): A compliant retainer relationship exists between attorney Li and client Rj if and only if both their X and Y attributes differ

Your goal is to deduce the actual layout type (I/II/III), rule type (A/B/C), and the maximum concurrent legal representations (maximum matching size) across the entire group (all 8 entities) under this combination.

## Queries You Can Make
Each query specifies an attorney subset S and a corporate client subset T, where the sizes of both S and T are 2 or 3. I will return the maximum concurrent legal representations (an integer from 0 to 3) within the induced sub-network between S and T.

**Query Format:**
<query>L1,L2;R1,R3</query>

**Response Example:**
If the maximum concurrent legal representations for this network is 2, I will reply: 2

You need to gather sufficient information before submitting your final answer.

## Final Answer Format
<answer>layout=I, rule=A, max_matching=3</answer>
(All three items must be correct to succeed.)
"""

    tags = ["answer", "query"]

    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        1: {
            "layout": "I",
            "rule": "A",
        },
        2: {
            "layout": "II",
            "rule": "B",
        },
        3: {
            "layout": "III",
            "rule": "A",
        },
        4: {
            "layout": "I",
            "rule": "C",
        },
        5: {
            "layout": "III",
            "rule": "C",
        },
    }

    LAYOUTS = {
        "I": {
            "L1": (0, 0), "L2": (0, 0), "L3": (1, 1), "L4": (1, 1),
            "R1": (1, 0), "R2": (1, 0), "R3": (1, 1), "R4": (0, 1),
        },
        "II": {
            "L1": (0, 0), "L2": (0, 1), "L3": (0, 1), "L4": (1, 0),
            "R1": (0, 0), "R2": (1, 0), "R3": (1, 1), "R4": (1, 1),
        },
        "III": {
            "L1": (0, 0), "L2": (1, 0), "L3": (1, 0), "L4": (1, 1),
            "R1": (0, 0), "R2": (0, 0), "R3": (1, 1), "R4": (1, 1),
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """根据难度初始化游戏配置"""
        diff = int(self.config.difficulty)
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.layout_type = cfg["layout"]
        self.rule_type = cfg["rule"]

        # 获取顶点属性
        self.vertex_attrs = self.LAYOUTS[self.layout_type]

        # 计算全图边集和最大匹配
        self.edges = self._compute_edges(
            ["L1", "L2", "L3", "L4"],
            ["R1", "R2", "R3", "R4"]
        )
        self.max_matching_size = self._compute_max_matching(
            ["L1", "L2", "L3", "L4"],
            ["R1", "R2", "R3", "R4"]
        )

        # 用于游戏规则模板（如果需要）
        self._game_info = {}

    def _can_connect(self, left_v, right_v):
        """根据当前规则判断两个顶点是否可连边"""
        x_l, y_l = self.vertex_attrs[left_v]
        x_r, y_r = self.vertex_attrs[right_v]

        if self.rule_type == "A":
            # X 异
            return x_l != x_r
        elif self.rule_type == "B":
            # Y 异
            return y_l != y_r
        elif self.rule_type == "C":
            # 双异
            return (x_l != x_r) and (y_l != y_r)
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def _compute_edges(self, left_set, right_set):
        """计算给定左右顶点集合间的所有边"""
        edges = []
        for lv in left_set:
            for rv in right_set:
                if self._can_connect(lv, rv):
                    edges.append((lv, rv))
        return edges

    def _compute_max_matching(self, left_set, right_set):
        """
        计算给定左右顶点集合间的最大匹配规模。
        使用增广路算法（匈牙利算法的简化版）。
        """
        # 构建边集
        edges = self._compute_edges(left_set, right_set)
        
        # 构建邻接表
        adj = {lv: [] for lv in left_set}
        for lv, rv in edges:
            adj[lv].append(rv)

        # 右侧顶点的匹配记录
        match_right = {}

        def dfs(u, visited):
            """寻找增广路"""
            for v in adj[u]:
                if v in visited:
                    continue
                visited.add(v)
                # 如果 v 未匹配，或者 v 的匹配对象可以找到增广路
                if v not in match_right or dfs(match_right[v], visited):
                    match_right[v] = u
                    return True
            return False

        # 对每个左侧顶点尝试寻找增广路
        for lv in left_set:
            dfs(lv, set())

        return len(match_right)

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        # 解析答案: layout=X, rule=Y, max_matching=Z
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()

        # 检查必要字段
        if "layout" not in ans_dict or "rule" not in ans_dict or "max_matching" not in ans_dict:
            return False

        # 检查布局
        if ans_dict["layout"] != self.layout_type:
            return False

        # 检查规则
        if ans_dict["rule"] != self.rule_type:
            return False

        # 检查最大匹配规模
        try:
            model_matching = int(ans_dict["max_matching"])
        except:
            return False

        return model_matching == self.max_matching_size

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."

        raw_query = parsed_info["query"].strip()

        # 解析格式：L1,L2;R1,R3
        try:
            parts = raw_query.split(";")
            if len(parts) != 2:
                raise ValueError("Query format error")

            left_part, right_part = parts
            left_vertices = [x.strip() for x in left_part.split(",") if x.strip()]
            right_vertices = [x.strip() for x in right_part.split(",") if x.strip()]

            # 检查集合大小
            if len(left_vertices) not in [2, 3] or len(right_vertices) not in [2, 3]:
                raise ValueError("Subset size must be 2 or 3")

            # 检查顶点有效性
            valid_left = {"L1", "L2", "L3", "L4"}
            valid_right = {"R1", "R2", "R3", "R4"}
            for lv in left_vertices:
                if lv not in valid_left:
                    raise ValueError(f"Invalid left vertex: {lv}")
            for rv in right_vertices:
                if rv not in valid_right:
                    raise ValueError(f"Invalid right vertex: {rv}")

            # 检查是否有重复
            if len(left_vertices) != len(set(left_vertices)) or len(right_vertices) != len(set(right_vertices)):
                raise ValueError("Duplicate vertices in query")

            # 计算该子图的最大匹配规模
            matching_size = self._compute_max_matching(left_vertices, right_vertices)
            return str(matching_size)

        except Exception as e:
            if self.config.language == "zh":
                return f"错误：查询格式无效或顶点不合法。请使用格式 <query>L1,L2;R1,R3</query>，其中左右子集大小均为 2 或 3。"
            else:
                return f"Error: Invalid query format or illegal vertices. Please use format <query>L1,L2;R1,R3</query>, where both subsets have size 2 or 3."

    def _cf_make_wrong(self, correct: str) -> str:
        import random as _rng
        if correct.isdigit():
            val = int(correct)
            choices = [i for i in range(4) if i != val]
            if choices:
                return str(_rng.choice(choices))
            return str(val + 1)
        
        # 否则按以下规则替换关键词（区分语言）
        # 中文："是" ↔ "否"
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        # 英文："Yes" ↔ "No"（忽略大小写，保持原始大小写风格）
        # 这里做简单的替换处理
        if "Yes" in correct:
            return correct.replace("Yes", "No")
        if "No" in correct:
            return correct.replace("No", "Yes")
        if "yes" in correct:
            return correct.replace("yes", "no")
        if "no" in correct:
            return correct.replace("no", "yes")

        # 若都不匹配：在字符串末尾追加 "_WRONG"
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        合法查询定义：左子集 S 大小为 2 或 3，右子集 T 大小为 2 或 3。
        """
        possible_queries = []
        left_candidates = ["L1", "L2", "L3", "L4"]
        right_candidates = ["R1", "R2", "R3", "R4"]

        # 枚举所有 S
        s_list = []
        for r in [2, 3]:
            s_list.extend(list(combinations(left_candidates, r)))

        # 枚举所有 T
        t_list = []
        for r in [2, 3]:
            t_list.extend(list(combinations(right_candidates, r)))

        # 组合生成查询
        for s in s_list:
            for t in t_list:
                # 格式化查询字符串
                left_str = ",".join(s)
                right_str = ",".join(t)
                query_content = f"{left_str};{right_str}"

                # 计算正确答案
                # 直接使用内部计算逻辑，避免影响反事实计数器或其他状态
                ans = self._compute_max_matching(list(s), list(t))

                possible_queries.append({
                    "query": f"<query>{query_content}</query>",
                    "answer": str(ans)
                })

        return possible_queries