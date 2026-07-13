# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   祖先判断：某节点是否为另一节点的祖先
# ============================================================

import random
from .base import Game


class TreeAncestorMappingGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树祖先关系推理"游戏，规则如下：

游戏设定了一棵未知结构的有根树，包含 {n} 个已标号的节点（标号为 {node_list}）。树的具体边和层级结构不会公开。

## 关系定义

对于节点 A 和 B，祖先关系采用严格定义（即 A 不等于 B）：
- **关系类别 C1**：A 是 B 的祖先（存在从 A 到 B 的向下路径）
- **关系类别 C2**：B 是 A 的祖先（存在从 B 到 A 的向下路径）
- **关系类别 C3**：A 和 B 互不为对方祖先（处于不同分支）

## 黑箱测试

系统提供了三个二元判定测试：T1、T2、T3。存在一个固定但未知的一一对应映射 f，将这三个测试与三个关系类别一一配对。

当你查询 Ti(X, Y) 时：
- 如果节点对 (X, Y) 的关系属于 f(Ti) 对应的类别，返回"是"
- 否则返回"否"

注意：映射 f 在整个游戏过程中保持不变，同一查询重复调用返回一致结果。

## 已知先验信息

以下关系已经确定：
{prior_info}

除此之外，树的其他结构信息不会公开。

## 你的任务

你的目标是判断命题"{target_query}"的真值（是或否）。

你可以通过查询来收集信息，但请尽可能少地使用查询次数。

## 查询格式

每次只能提交一个查询，使用以下 XML 格式：

查询测试 Ti 对节点对 (X, Y) 的结果（例如查询 T1 对节点对 (a, b)）：
<query>T1, a, b</query>

## 提交答案格式

当你准备好提交最终答案时，请使用以下格式：

<answer>是</answer>

或

<answer>否</answer>

如果答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Tree Ancestor Relationship Reasoning" game. Here are the rules:

The game features an unknown rooted tree structure with {n} labeled nodes (labels: {node_list}). The specific edges and hierarchy of the tree are not disclosed.

## Relationship Definitions

For nodes A and B, the ancestor relationship uses a strict definition (A is not equal to B):
- **Relationship Category C1**: A is an ancestor of B (there exists a downward path from A to B)
- **Relationship Category C2**: B is an ancestor of A (there exists a downward path from B to A)
- **Relationship Category C3**: A and B are not ancestors of each other (they are in different branches)

## Black Box Tests

The system provides three binary decision tests: T1, T2, T3. There exists a fixed but unknown one-to-one mapping f that pairs these three tests with the three relationship categories.

When you query Ti(X, Y):
- If the relationship of node pair (X, Y) belongs to the category corresponding to f(Ti), return "Yes"
- Otherwise, return "No"

Note: The mapping f remains constant throughout the game, and the same query will return consistent results.

## Known Prior Information

The following relationships are already established:
{prior_info}

Beyond this, no other structural information about the tree will be disclosed.

## Your Task

Your goal is to determine the truth value (Yes or No) of the proposition "{target_query}".

You can collect information through queries, but please use as few queries as possible.

## Query Format

You can only submit one query at a time, using the following XML format:

To query test Ti on node pair (X, Y) (e.g., query T1 on node pair (a, b)):
<query>T1, a, b</query>

## Answer Submission Format

When you are ready to submit your final answer, please use the following format:

<answer>Yes</answer>

or

<answer>No</answer>

If the answer is incorrect or the format is invalid, the game fails.
"""

    # ------------------ 场景 1：交通 ------------------
    contextualized_rule_zh_1 = """\
【交通网络溯源系统】
你现在被指派调查一个未知的单向分流交通拓扑网络（呈有根树结构）。该路网包含 {n} 个标号的枢纽节点（标号为 {node_list}）。具体路线图和分级结构处于加密状态。

## 节点关系定义

在交通分析中，如果车辆可以从一个枢纽向下游顺行到达另一个枢纽，前者被称为后者的“祖先”。对于枢纽节点 A 和 B（A 不等于 B）：
- **关系类别 C1**：A 是 B 的祖先（存在从 A 到 B 的顺行通路）
- **关系类别 C2**：B 是 A 的祖先（存在从 B 到 A 的顺行通路）
- **关系类别 C3**：A 和 B 互不为对方祖先（处于不同分流支路上，无法相互抵达）

## 黑箱探针测试

系统配备了三种电子探针测试：T1、T2、T3。存在一个固定但未知的一一对应映射 f，将这三个探针测试与三种路网关系类别一一配配。

当你调用探针 Ti(X, Y) 时：
- 如果枢纽对 (X, Y) 的关系属于 f(Ti) 对应的类别，系统返回“是”
- 否则返回“否”

注意：映射 f 在整个勘测过程中保持稳定不变，同一查询重复调用将返回一致结果。

## 已知先验信息

通过早期路勘，以下关系已经确定：
{prior_info}

除此之外，路网的其他结构信息不会公开。

## 你的任务

你的目标是研判关于交通路网的命题"{target_query}"的真值（是或否）。

你可以通过调用探针测试来收集信息，但请尽可能少地使用测试次数以节约系统资源。

## 查询格式

每次只能提交一个探针查询，使用以下 XML 格式：

查询测试 Ti 对枢纽对 (X, Y) 的探测结果（例如查询 T1 对节点对 (a, b)）：
<query>T1, a, b</query>

## 提交答案格式

当你准备好提交最终勘测结论时，请使用以下格式：

<answer>是</answer>
或
<answer>否</answer>

如果答案错误或格式不符，交通分析任务失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
【Traffic Network Tracing System】
You are assigned to investigate an unknown one-way divergent traffic topology network (structured as a rooted tree). The road network contains {n} labeled hub nodes (labels: {node_list}). The specific route maps and hierarchical structures are encrypted.

## Node Relationship Definitions

In traffic analysis, if a vehicle can travel downstream from one hub to reach another, the former is considered the "ancestor" of the latter. For hub nodes A and B (A is not equal to B):
- **Relationship Category C1**: A is an ancestor of B (there exists a valid downstream path from A to B)
- **Relationship Category C2**: B is an ancestor of A (there exists a valid downstream path from B to A)
- **Relationship Category C3**: A and B are not ancestors of each other (they are on different diverging branches and cannot reach each other)

## Black Box Probe Tests

The system is equipped with three types of electronic probe tests: T1, T2, T3. There exists a fixed but unknown one-to-one mapping f that pairs these three probes with the three traffic relationship categories.

When you trigger probe Ti(X, Y):
- If the relationship of hub pair (X, Y) belongs to the category corresponding to f(Ti), the system returns "Yes"
- Otherwise, it returns "No"

Note: The mapping f remains constant throughout the survey. Repeated identical queries will yield consistent results.

## Known Prior Information

Through early surveys, the following relationships have been confirmed:
{prior_info}

Beyond this, no other structural information about the network will be disclosed.

## Your Task

Your goal is to determine the truth value (Yes or No) of the traffic proposition "{target_query}".

You can collect information by running probe tests, but please use as few queries as possible to save system resources.

## Query Format

You can submit only one probe query at a time, using the following XML format:

To query test Ti on hub pair (X, Y) (e.g., query T1 on node pair (a, b)):
<query>T1, a, b</query>

## Answer Submission Format

When you are ready to submit your final survey conclusion, please use the following format:

<answer>Yes</answer>
or
<answer>No</answer>

If the answer is incorrect or the format is invalid, the traffic analysis task fails.
"""

    # ------------------ 场景 2：医疗 ------------------
    contextualized_rule_zh_2 = """\
【病毒变异溯源系统】
我们正在使用计算流行病学工具追踪一种新型病毒。该病毒的变异过程构成了一棵未知的变异有根树，包含 {n} 个已标记的毒株样本（标号为 {node_list}）。具体的变异路径不会公开。

## 演化关系定义

在病毒发生学中，如果毒株通过变异衍生出下游毒株，前者即为后者的“祖先”毒株。对于样本 A 和 B（A 不等于 B）：
- **关系类别 C1**：A 是 B 的祖先（存在从 A 变异演化到 B 的路径）
- **关系类别 C2**：B 是 A 的祖先（存在从 B 变异演化到 A 的路径）
- **关系类别 C3**：A 和 B 互不为对方祖先（属于完全平行的独立变异分支）

## 基因序列黑箱比对

实验室提供了三种快速抗体比对测试：T1、T2、T3。存在一个固定但未知的映射 f，将这三种比对测试与上述三个关系类别一一配对。

当你提交测试 Ti(X, Y) 时：
- 如果毒株对 (X, Y) 的关系属于 f(Ti) 对应的变异关系类别，试剂呈阳性，返回“是”
- 否则呈阴性，返回“否”

注意：映射 f 在整体验测过程中保持恒定，同一组合多次测试返回结果一致。

## 已知先验信息

通过早期测序，以下演化关系已确认：
{prior_info}

除此以外，病毒的其他变异链节点不会公开。

## 你的任务

你的核心目标是判定病理命题"{target_query}"的真值（是或否）。

你可以通过试剂测试来获取数据，但请以最少的检测试剂消耗完成溯源。

## 查询格式

每次只能提交一次比对测试请求，使用以下 XML 格式：

测试 Ti 对毒株样本对 (X, Y) 的比对结果（例如测试 T1 对样本 (a, b)）：
<query>T1, a, b</query>

## 提交答案格式

当你确认最终溯源结论时，请使用以下格式：

<answer>是</answer>
或
<answer>否</answer>

若结论错误或格式有误，疫情阻击任务失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
【Viral Mutation Tracing System】
We are utilizing computational epidemiology tools to trace a novel virus. The mutation process of the virus forms an unknown rooted mutation tree, containing {n} labeled strain samples (labels: {node_list}). The specific mutation pathways will not be disclosed.

## Evolutionary Relationship Definitions

In viral ontogeny, if a strain evolves into a downstream strain through mutation, the former is referred to as the "ancestor" strain of the latter. For samples A and B (A is not equal to B):
- **Relationship Category C1**: A is an ancestor of B (there exists a mutation path evolving from A to B)
- **Relationship Category C2**: B is an ancestor of A (there exists a mutation path evolving from B to A)
- **Relationship Category C3**: A and B are not ancestors of each other (they belong to completely parallel, independent mutation branches)

## Black Box Sequence Matching

The laboratory provides three types of rapid antibody matching tests: T1, T2, T3. There exists a fixed but unknown mapping f that pairs these three matching tests with the three relationship categories mentioned above.

When you submit test Ti(X, Y):
- If the relationship of strain pair (X, Y) belongs to the evolutionary category corresponding to f(Ti), the reagent shows a positive reaction and returns "Yes"
- Otherwise, it shows negative and returns "No"

Note: The mapping f remains constant during the entire tracing process, and the same combination of queries will consistently return the same results.

## Known Prior Information

Through early sequencing, the following evolutionary relationships have been established:
{prior_info}

Beyond this, no other nodes in the viral mutation chain will be disclosed.

## Your Task

Your core objective is to determine the truth value (Yes or No) of the pathological proposition "{target_query}".

You can acquire data through reagent tests, but please achieve the tracing with the minimal consumption of test reagents.

## Query Format

You can only submit one matching test request at a time, using the following XML format:

To test matching result of Ti on strain sample pair (X, Y) (e.g., test T1 on sample pair (a, b)):
<query>T1, a, b</query>

## Answer Submission Format

When you confirm your final tracing conclusion, please use the following format:

<answer>Yes</answer>
or
<answer>No</answer>

If the conclusion is incorrect or the format is invalid, the outbreak mitigation task fails.
"""

    # ------------------ 场景 3：教育 ------------------
    contextualized_rule_zh_3 = """\
【教学大纲依赖分析系统】
你正在审查一套复杂的专业课程体系。该体系由 {n} 个知识模块（标号为 {node_list}）组成，整体构成一棵未知的有根先决条件树。各模块的具体修读先后顺序处于未解密状态。

## 模块依赖关系定义

在教学体系中，如果某个模块是另一个模块的必修前置基础，我们称基础模块为后续模块的“祖先”。对于知识模块 A 和 B（A 不等于 B）：
- **关系类别 C1**：A 是 B 的祖先（必须先学 A 并沿着修读路径才能学 B）
- **关系类别 C2**：B 是 A 的祖先（必须先学 B 并沿着修读路径才能学 A）
- **关系类别 C3**：A 和 B 互不为对方祖先（属于不同专业选修方向，互无前置依赖）

## 黑箱评估测试

教务系统提供了三种数据接口测试：T1、T2、T3。存在一个固定但未知的规则 f，将这三种测试与上述三类依赖关系一一对应。

当你调用接口 Ti(X, Y) 时：
- 如果模块对 (X, Y) 实际关系匹配 f(Ti) 对应的依赖类别，接口响应“是”
- 否则响应“否”

注意：对应规则 f 在整个审查期内固定生效，相同请求必然获得相同响应。

## 已知先验信息

教务处已公开以下核心修读关系：
{prior_info}

其余模块的深层依赖逻辑仍然未知。

## 你的任务

请论证课程体系命题"{target_query}"的真实性（是或否）。

允许通过接口请求收集线索，但请尽量精简你的查询步骤以符合系统速率限制。

## 查询格式

每次只允许提交一次请求，严格遵守以下 XML 格式：

通过接口 Ti 查询模块对 (X, Y)（例如查询 T1 对知识模块 (a, b)）：
<query>T1, a, b</query>

## 提交答案格式

得到最终论证结果后，请采用如下格式提交：

<answer>是</answer>
或
<answer>否</answer>

一旦回答错误或格式校验失败，课程审查即告失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
【Syllabus Prerequisite Dependency Analysis System】
You are reviewing a complex professional curriculum system. This system consists of {n} knowledge modules (labels: {node_list}), forming an unknown rooted prerequisite tree. The specific sequential study order of each module remains unclassified.

## Module Dependency Relationship Definitions

In the educational framework, if a module is a mandatory prerequisite foundation for another module, the foundational module is termed the "ancestor" of the subsequent one. For knowledge modules A and B (A is not equal to B):
- **Relationship Category C1**: A is an ancestor of B (you must study A first and follow the curriculum path to study B)
- **Relationship Category C2**: B is an ancestor of A (you must study B first and follow the curriculum path to study A)
- **Relationship Category C3**: A and B are not ancestors of each other (they belong to different elective tracks with no mutual prerequisite dependency)

## Black Box Evaluation Tests

The academic system provides three data interface tests: T1, T2, T3. There exists a fixed but unknown rule f that pairs these three tests with the three dependency categories.

When you invoke interface Ti(X, Y):
- If the actual relationship of module pair (X, Y) matches the dependency category designated by f(Ti), the interface responds with "Yes"
- Otherwise, it responds with "No"

Note: The corresponding rule f remains rigidly in effect throughout the review period, and identical requests will invariably yield identical responses.

## Known Prior Information

The registrar's office has disclosed the following core study relationships:
{prior_info}

The deeper dependency logic for the remaining modules remains unknown.

## Your Task

Please verify the authenticity (Yes or No) of the curriculum proposition "{target_query}".

You are allowed to collect clues via interface requests, but please streamline your query steps as much as possible to comply with system rate limits.

## Query Format

Only one request may be submitted at a time, strictly adhering to the following XML format:

To query module pair (X, Y) through interface Ti (e.g., query T1 on knowledge module pair (a, b)):
<query>T1, a, b</query>

## Answer Submission Format

Upon deriving your final verification result, please submit it using this format:

<answer>Yes</answer>
or
<answer>No</answer>

Any erroneous answer or format validation failure will result in the immediate failure of the curriculum review.
"""

    # ------------------ 场景 4：制造业/工业 ------------------
    contextualized_rule_zh_4 = """\
【供应链BOM（物料清单）溯源系统】
系统导入了一份复杂机电产品的制造层级树，共包含 {n} 个加工组件/总成（标号为 {node_list}）。树的顶部为基础原料，向下分层加工。具体的装配和拆解从属架构暂未公开。

## 制造层级定义

在物料追踪中，如果一个组件经过后续工序加工或组装流转为另一个组件，处于上游工序位置的组件被称为“祖先”组件。对于组件 A 和 B（A 不等于 B）：
- **关系类别 C1**：A 是 B 的祖先（A 处于加工链上游，存在经由 A 最终装配/流转至 B 的路径）
- **关系类别 C2**：B 是 A 的祖先（B 处于加工链上游，存在经由 B 最终装配/流转至 A 的路径）
- **关系类别 C3**：A 和 B 互不为对方祖先（分属平行不同的生产加工支线）

## 自动化黑箱检测

系统配备了三种工艺探伤指令：T1、T2、T3。存在一个内置且未知的固定映射 f，将三条指令与三类上下游层级关系一一对应。

当你输入检测指令 Ti(X, Y) 时：
- 若组件对 (X, Y) 的真实层级符合 f(Ti) 所指代的关系，诊断仪反馈“是”
- 反之反馈“否”

注意：映射机制 f 从始至终保持不变，重复测定不会产生数据偏差。

## 已知先验信息

工厂数据库现阶段已查明的工序关系如下：
{prior_info}

除所列项外，其余装配层级均无法直接阅览。

## 你的任务

请研判工艺验证命题"{target_query}"是否成立（是或否）。

允许利用探伤指令排查层级架构，但要求用最少的诊断次数获取结果，以保证产线效率。

## 查询格式

每次仅限输入一条验证指令，标准 XML 语法如下：

运用指令 Ti 检测组件对 (X, Y)（例如利用 T1 检测组件 (a, b)）：
<query>T1, a, b</query>

## 提交答案格式

得出准确工艺判断后，按规范格式输出结案报告：

<answer>是</answer>
或
<answer>否</answer>

若判定失误或报告不合规，产线溯源立即终止。
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industry Scenario]
【Supply Chain BOM (Bill of Materials) Tracing System】
The system has imported the manufacturing hierarchy tree of a complex electromechanical product, comprising {n} processing components/assemblies (labels: {node_list}). The top of the tree represents fundamental raw materials that undergo layered downstream processing. The specific assembly and disassembly substructures are not disclosed.

## Manufacturing Hierarchy Definitions

In material tracking, if a component flows into another component through subsequent processing or assembly steps, the component positioned upstream is referred to as the "ancestor" component. For components A and B (A is not equal to B):
- **Relationship Category C1**: A is an ancestor of B (A is upstream in the processing chain, and there is a path resulting in B via processing/assembly from A)
- **Relationship Category C2**: B is an ancestor of A (B is upstream in the processing chain, and there is a path resulting in A via processing/assembly from B)
- **Relationship Category C3**: A and B are not ancestors of each other (they belong to parallel and distinct production branches)

## Automated Black Box Diagnostics

The system is equipped with three process defect-detection commands: T1, T2, T3. There is an embedded, unknown, yet fixed mapping f that pairs these three commands with the three hierarchical relationships.

When you input diagnostic command Ti(X, Y):
- If the true hierarchy of component pair (X, Y) matches the relationship denoted by f(Ti), the diagnostic tool returns "Yes"
- Conversely, it returns "No"

Note: The mapping mechanism f remains invariant from beginning to end, and repeated measurements will not produce data deviations.

## Known Prior Information

The relationships currently verified by the factory database are as follows:
{prior_info}

Apart from those listed, the other assembly hierarchies cannot be directly viewed.

## Your Task

Please determine whether the process validation proposition "{target_query}" holds true (Yes or No).

You are permitted to use defect-detection commands to deduce the hierarchical structure, but you are required to attain the result with the fewest possible diagnostic iterations to ensure production line efficiency.

## Query Format

Input is restricted to a single validation command per instance, using the standard XML syntax:

To inspect component pair (X, Y) using command Ti (e.g., inspect component pair (a, b) using T1):
<query>T1, a, b</query>

## Answer Submission Format

Once an accurate process judgment is reached, output the final report in the standardized format:

<answer>Yes</answer>
or
<answer>No</answer>

If the judgment is flawed or the report is non-compliant, the production line tracing terminates immediately.
"""

    # ------------------ 场景 5：法律 ------------------
    contextualized_rule_zh_5 = """\
【企业股权穿透审计系统】
你正在办理一起反垄断案件，需要理清某财团旗下 {n} 家关联公司（注册代号为 {node_list}）的实际控制网络。该网络表现为一棵单一顶层控制的有根树架构，具体的绝对控股链条属于商业机密。

## 穿透控制关系定义

在股权穿透审计中，若一家公司通过层层全资持股或绝对控股影响另一家公司，前者在法律地位上被认定为后者的母公司或“祖先”。对于实体 A 和实体 B（A 不等于 B）：
- **关系类别 C1**：A 是 B 的祖先（A 处于控股链顶端/上游，存在自 A 向下穿透控制 B 的持股路径）
- **关系类别 C2**：B 是 A 的祖先（B 处于控股链顶端/上游，存在自 B 向下穿透控制 A 的持股路径）
- **关系类别 C3**：A 和 B 互不为对方祖先（分属不同的控制分支，无直接上下游控股关系）

## 穿透核查黑箱

金融监管局提供了三种独立的资本穿透核查函数：T1、T2、T3。存在一个未向调查员公布的固定映射 f，将这三种函数与上述三类控股关系绑定。

当你执行穿透核查 Ti(X, Y) 时：
- 假如实体对 (X, Y) 契合 f(Ti) 锁定的控制关系，系统提示“是”
- 不契合则提示“否”

注意：控制权映射法则 f 在全案侦查期间完全固定，同样的数据请求返回同样的结果。

## 已知先验信息

依据工商初步建档，已确认如下投资事实：
{prior_info}

其余公司的深层投资持股架构皆无确切备案。

## 你的任务

你必须证实或证伪本次质询的核心法律命题："{target_query}"（是或否）。

虽然允许随时调用穿透核查接口，但须遵循审计流程规范，最大限度减少调查动作。

## 查询格式

单次发函只能发配一个核查请求，严格采取 XML 报文：

通过核查函 Ti 穿透调查实体对 (X, Y)（例如函件 T1 核查实体 (a, b)）：
<query>T1, a, b</query>

## 提交答案格式

当掌握足够的案卷证据时，以此格式提交审计定论：

<answer>是</answer>
或
<answer>否</answer>

如有误判或格式文书缺陷，案件线索即视为中断失败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
【Corporate Equity Penetration Audit System】
You are handling an antitrust case and need to untangle the actual control network of {n} affiliated entities (registration codes: {node_list}) under a certain conglomerate. This network manifests as a rooted tree architecture with a single ultimate parent control. The precise absolute controlling chains are classified as trade secrets.

## Penetrating Control Relationship Definitions

In an equity penetration audit, if one company exerts influence over another through layered wholly-owned shares or absolute controlling stakes, the former is legally identified as the parent or "ancestor" company. For entities A and B (A is not equal to B):
- **Relationship Category C1**: A is an ancestor of B (A is situated at the top/upstream of the controlling chain, and there exists a direct penetrating ownership path from A controlling B)
- **Relationship Category C2**: B is an ancestor of A (B is situated at the top/upstream of the controlling chain, and there exists a direct penetrating ownership path from B controlling A)
- **Relationship Category C3**: A and B are not ancestors of each other (they belong to different controlling branches with no direct upstream-downstream ownership relation)

## Penetration Verification Black Box

The Financial Regulatory Bureau has provided three independent capital penetration verification functions: T1, T2, T3. There is an undisclosed but fixed mapping f that binds these three functions to the aforementioned three control relationship categories.

When you execute a penetration verification Ti(X, Y):
- If the entity pair (X, Y) conforms to the control relationship locked by f(Ti), the system prompts "Yes"
- If it does not conform, it prompts "No"

Note: The control power mapping rule f is completely fixed during the entirety of the case investigation; identical data requests will return identical results.

## Known Prior Information

Based on preliminary corporate registry filings, the following investment facts have been confirmed:
{prior_info}

The profound investment and shareholding structures of the remaining companies are not definitively documented.

## Your Task

You must validate or invalidate the core legal proposition of this inquiry: "{target_query}" (Yes or No).

While you may call the penetration verification interface at any time, you must strictly follow audit procedural norms and minimize investigation actions to the greatest extent possible.

## Query Format

A single dispatch can only issue one verification request, strictly employing the XML payload:

To penetrate and investigate entity pair (X, Y) via verification letter Ti (e.g., use T1 to verify entity pair (a, b)):
<query>T1, a, b</query>

## Answer Submission Format

When sufficient docket evidence is secured, submit the final audit conclusion in this format:

<answer>Yes</answer>
or
<answer>No</answer>

Any misjudgment or defect in the formatting of the instrument will lead to the forfeiture of the case leads.
"""

    tags = ["answer", "query"]
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "nodes": ["a", "b", "c", "d", "e", "f", "g", "h"],
                # 树结构：root-a-b-c, a-d, root-e-f, e-g, e-h
                # a是b的祖先，b是c的祖先，d和e不相关
                "edges": [("root", "a"), ("a", "b"), ("b", "c"), ("a", "d"), 
                         ("root", "e"), ("e", "f"), ("e", "g"), ("e", "h")],
                "prior_pairs": [("a", "b", "C1"), ("b", "c", "C1"), ("b", "a", "C2"), ("d", "e", "C3")],
                "target_pair": ("a", "c"),  # a是c的祖先
                "target_answer": True,
                "test_mapping": {"T1": "C1", "T2": "C2", "T3": "C3"},
            },
            2: {
                "n": 10,
                "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
                # root-a-b-c-d, a-e-f, root-g-h, g-i-j
                "edges": [("root", "a"), ("a", "b"), ("b", "c"), ("c", "d"), ("a", "e"), ("e", "f"),
                         ("root", "g"), ("g", "h"), ("g", "i"), ("i", "j")],
                "prior_pairs": [("a", "b", "C1"), ("b", "c", "C1"), ("b", "a", "C2"), ("d", "g", "C3")],
                "target_pair": ("e", "d"),  # e不是d的祖先
                "target_answer": False,
                "test_mapping": {"T1": "C2", "T2": "C1", "T3": "C3"},
            },
            3: {
                "n": 12,
                "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"],
                # root-a-b-c, b-d-e, a-f-g-h, root-i-j-k, i-l
                "edges": [("root", "a"), ("a", "b"), ("b", "c"), ("b", "d"), ("d", "e"),
                         ("a", "f"), ("f", "g"), ("g", "h"), ("root", "i"), ("i", "j"), 
                         ("j", "k"), ("i", "l")],
                "prior_pairs": [("a", "b", "C1"), ("b", "c", "C1"), ("b", "a", "C2"), ("e", "i", "C3")],
                "target_pair": ("f", "h"),  # f是h的祖先
                "target_answer": True,
                "test_mapping": {"T1": "C3", "T2": "C1", "T3": "C2"},
            },
            4: {
                "n": 14,
                "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"],
                # root-a-b-c-d, b-e-f, a-g-h-i, root-j-k, j-l-m, j-n
                "edges": [("root", "a"), ("a", "b"), ("b", "c"), ("c", "d"), ("b", "e"), ("e", "f"),
                         ("a", "g"), ("g", "h"), ("h", "i"), ("root", "j"), ("j", "k"), 
                         ("j", "l"), ("l", "m"), ("j", "n")],
                "prior_pairs": [("a", "b", "C1"), ("b", "c", "C1"), ("b", "a", "C2"), ("d", "j", "C3")],
                "target_pair": ("c", "f"),  # c不是f的祖先
                "target_answer": False,
                "test_mapping": {"T1": "C2", "T2": "C3", "T3": "C1"},
            },
            5: {
                "n": 16,
                "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"],
                # 复杂树结构
                "edges": [("root", "a"), ("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"),
                         ("b", "f"), ("f", "g"), ("a", "h"), ("h", "i"), ("i", "j"),
                         ("root", "k"), ("k", "l"), ("l", "m"), ("k", "n"), ("n", "o"), ("n", "p")],
                "prior_pairs": [("a", "b", "C1"), ("b", "c", "C1"), ("b", "a", "C2"), ("e", "k", "C3")],
                "target_pair": ("h", "j"),  # h是j的祖先
                "target_answer": True,
                "test_mapping": {"T1": "C3", "T2": "C2", "T3": "C1"},
            },
        },
        "en": {
            1: {
                "n": 8,
                "nodes": ["a", "b", "c", "d", "e", "f", "g", "h"],
                "edges": [("root", "a"), ("a", "b"), ("b", "c"), ("a", "d"), 
                         ("root", "e"), ("e", "f"), ("e", "g"), ("e", "h")],
                "prior_pairs": [("a", "b", "C1"), ("b", "c", "C1"), ("b", "a", "C2"), ("d", "e", "C3")],
                "target_pair": ("a", "c"),
                "target_answer": True,
                "test_mapping": {"T1": "C1", "T2": "C2", "T3": "C3"},
            },
            2: {
                "n": 10,
                "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
                "edges": [("root", "a"), ("a", "b"), ("b", "c"), ("c", "d"), ("a", "e"), ("e", "f"),
                         ("root", "g"), ("g", "h"), ("g", "i"), ("i", "j")],
                "prior_pairs": [("a", "b", "C1"), ("b", "c", "C1"), ("b", "a", "C2"), ("d", "g", "C3")],
                "target_pair": ("e", "d"),
                "target_answer": False,
                "test_mapping": {"T1": "C2", "T2": "C1", "T3": "C3"},
            },
            3: {
                "n": 12,
                "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l"],
                "edges": [("root", "a"), ("a", "b"), ("b", "c"), ("b", "d"), ("d", "e"),
                         ("a", "f"), ("f", "g"), ("g", "h"), ("root", "i"), ("i", "j"), 
                         ("j", "k"), ("i", "l")],
                "prior_pairs": [("a", "b", "C1"), ("b", "c", "C1"), ("b", "a", "C2"), ("e", "i", "C3")],
                "target_pair": ("f", "h"),
                "target_answer": True,
                "test_mapping": {"T1": "C3", "T2": "C1", "T3": "C2"},
            },
            4: {
                "n": 14,
                "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n"],
                "edges": [("root", "a"), ("a", "b"), ("b", "c"), ("c", "d"), ("b", "e"), ("e", "f"),
                         ("a", "g"), ("g", "h"), ("h", "i"), ("root", "j"), ("j", "k"), 
                         ("j", "l"), ("l", "m"), ("j", "n")],
                "prior_pairs": [("a", "b", "C1"), ("b", "c", "C1"), ("b", "a", "C2"), ("d", "j", "C3")],
                "target_pair": ("c", "f"),
                "target_answer": False,
                "test_mapping": {"T1": "C2", "T2": "C3", "T3": "C1"},
            },
            5: {
                "n": 16,
                "nodes": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p"],
                "edges": [("root", "a"), ("a", "b"), ("b", "c"), ("c", "d"), ("d", "e"),
                         ("b", "f"), ("f", "g"), ("a", "h"), ("h", "i"), ("i", "j"),
                         ("root", "k"), ("k", "l"), ("l", "m"), ("k", "n"), ("n", "o"), ("n", "p")],
                "prior_pairs": [("a", "b", "C1"), ("b", "c", "C1"), ("b", "a", "C2"), ("e", "k", "C3")],
                "target_pair": ("h", "j"),
                "target_answer": True,
                "test_mapping": {"T1": "C3", "T2": "C2", "T3": "C1"},
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 使用随机种子对 test_mapping 进行洗牌，增加变化性
        rng = random.Random()  # 不固定种子，每次不同
        categories = ["C1", "C2", "C3"]
        rng.shuffle(categories)
        self.test_mapping = {f"T{i+1}": categories[i] for i in range(3)}
        
        # 基本信息
        self._game_info["n"] = cfg["n"]
        self._game_info["node_list"] = ", ".join(cfg["nodes"])
        
        # 构建树结构（用于计算祖先关系）
        self.nodes = cfg["nodes"]
        self.edges = cfg["edges"]
        self.target_pair = cfg["target_pair"]
        self.target_answer = cfg["target_answer"]
        
        # 构建祖先关系映射
        self._build_ancestor_map()
        
        # 生成先验信息文本
        prior_texts = []
        for x, y, cat in cfg["prior_pairs"]:
            if lang == "zh":
                if cat == "C1":
                    prior_texts.append(f"- {x} 是 {y} 的祖先")
                elif cat == "C2":
                    prior_texts.append(f"- {y} 是 {x} 的祖先")
                else:  # C3
                    prior_texts.append(f"- {x} 和 {y} 互不为对方祖先")
            else:
                if cat == "C1":
                    prior_texts.append(f"- {x} is an ancestor of {y}")
                elif cat == "C2":
                    prior_texts.append(f"- {y} is an ancestor of {x}")
                else:  # C3
                    prior_texts.append(f"- {x} and {y} are not ancestors of each other")
        
        self._game_info["prior_info"] = "\n".join(prior_texts)
        
        # 目标查询文本
        if lang == "zh":
            self._game_info["target_query"] = f"{self.target_pair[0]} 是 {self.target_pair[1]} 的祖先"
        else:
            self._game_info["target_query"] = f"{self.target_pair[0]} is an ancestor of {self.target_pair[1]}"

    def _build_ancestor_map(self):
        """构建祖先关系映射：对于每个节点，计算其所有祖先"""
        # 首先构建父子关系
        children = {}
        for parent, child in self.edges:
            if parent not in children:
                children[parent] = []
            children[parent].append(child)
        
        # 使用DFS计算每个节点的所有祖先
        self.ancestors = {node: set() for node in self.nodes}
        
        def dfs(node, ancestor_set):
            self.ancestors[node] = ancestor_set.copy()
            if node in children:
                for child in children[node]:
                    dfs(child, ancestor_set | {node})
        
        # 从root开始DFS
        dfs("root", set())

    def _get_relationship(self, x, y):
        """判断节点对(x, y)的关系类别"""
        if x == y:
            return None  # 不定义自环
        
        if x in self.ancestors.get(y, set()):
            return "C1"  # x是y的祖先
        elif y in self.ancestors.get(x, set()):
            return "C2"  # y是x的祖先
        else:
            return "C3"  # 互不为祖先

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        answer = parsed_info["answer"].strip().lower()
        
        if self.config.language == "zh":
            correct_answer = "是" if self.target_answer else "否"
            return answer == correct_answer
        else:
            correct_answer = "yes" if self.target_answer else "no"
            return answer == correct_answer

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑（原 produce_response 的内容）"""
        if "query" not in parsed_info:
            raise ValueError("No valid query found.")
        
        query_str = parsed_info["query"].strip()
        parts = [p.strip() for p in query_str.split(",")]
        
        if len(parts) != 3:
            if self.config.language == "zh":
                return "错误：查询格式无效，应为 'Ti, X, Y' 的形式。"
            else:
                return "Error: Invalid query format. Should be 'Ti, X, Y'."
        
        test_name, node_x, node_y = parts
        
        # 验证测试名称
        if test_name not in ["T1", "T2", "T3"]:
            if self.config.language == "zh":
                return f"错误：测试名称 '{test_name}' 无效，应为 T1、T2 或 T3。"
            else:
                return f"Error: Invalid test name '{test_name}'. Should be T1, T2, or T3."
        
        # 验证节点
        if node_x not in self.nodes or node_y not in self.nodes:
            if self.config.language == "zh":
                return "错误：节点不在允许的节点列表中。"
            else:
                return "Error: Node not in the allowed node list."
        
        if node_x == node_y:
            if self.config.language == "zh":
                return "错误：不能查询相同的节点。"
            else:
                return "Error: Cannot query the same node."
        
        # 获取关系类别
        relationship = self._get_relationship(node_x, node_y)
        
        # 获取该测试对应的关系类别
        test_category = self.test_mapping[test_name]
        
        # 判断是否匹配
        matches = (relationship == test_category)
        
        if self.config.language == "zh":
            return "是" if matches else "否"
        else:
            return "Yes" if matches else "No"

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文替换
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 英文替换（忽略大小写，保持原始大小写风格）
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        # 若都不匹配，追加后缀
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        test_names = ["T1", "T2", "T3"]
        
        # 遍历所有测试类型
        for test_name in test_names:
            # 遍历所有节点对 (x, y)
            for node_x in self.nodes:
                for node_y in self.nodes:
                    # 排除自身查询，因为 _cf_core_produce 中禁止 node_x == node_y
                    if node_x == node_y:
                        continue
                    
                    # 构建查询字符串，包含 XML 标签
                    query_content = f"<query>{test_name}, {node_x}, {node_y}</query>"
                    
                    # 获取真实关系
                    relationship = self._get_relationship(node_x, node_y)
                    
                    # 获取测试映射对应的类别
                    test_category = self.test_mapping[test_name]
                    
                    # 判断真假
                    matches = (relationship == test_category)
                    
                    # 根据语言生成答案
                    if self.config.language == "zh":
                        ans = "是" if matches else "否"
                    else:
                        ans = "Yes" if matches else "No"
                    
                    queries.append({
                        "query": query_content,
                        "answer": ans
                    })
        
        return queries