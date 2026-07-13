# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   路径存在性：某条给定的节点序列是否构成合法路径
# ============================================================

from .base import Game
import re

class ColoredGraphPathGame(Game):

    game_rule_zh = """\
我们现在来玩一个"彩色边路径推理"游戏，规则如下：

游戏设定了一个无向图，顶点集为 A, B, C, D, E。边及其颜色标记如下：
- A—B (红)
- B—C (蓝)
- C—D (红)
- D—E (蓝)
- E—A (红)
- B—D (蓝)
- C—E (红)
- A—D (蓝)

我已经秘密选择了一条路径合规性判定规则，用于评估给定的顶点序列是否"合规"。基础要求是：顶点序列中相邻顶点之间必须存在边（无向）。在此基础上，还附加了一条隐藏规则，但我不会告诉你是哪一条。

你的目标是：
1. 通过查询预设的测试序列来推断隐藏规则；
2. 判定目标序列 R* = A—D—E 是否合规。

你可以查询以下三个预设测试序列（每次查询一个）：
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

对于每次查询，我会告诉你该序列是"合规"还是"不合规"，但不会告诉你违反了哪条规则。

当你收集足够信息后，请提交最终答案。最终答案需要包括：
1. 你推断出的隐藏规则名称（ALT、SIMPLE、EVEN 或 REDSTART 之一）
2. 目标序列 R* 的合规性判断（合规或不合规）

若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

查询测试序列 T1：
<query_path>T1</query_path>

查询测试序列 T2：
<query_path>T2</query_path>

查询测试序列 T3：
<query_path>T3</query_path>

提交最终答案时，必须说明规则名称和目标序列的合规性，格式如下：
<answer>rule=ALT, target=合规</answer>

或：
<answer>rule=SIMPLE, target=不合规</answer>
"""

    game_rule_en = """\
Let's play a "Colored Edge Path Reasoning" game. Here are the rules:

The game has an undirected graph with vertices A, B, C, D, E. The edges and their color labels are:
- A—B (Red)
- B—C (Blue)
- C—D (Red)
- D—E (Blue)
- E—A (Red)
- B—D (Blue)
- C—E (Red)
- A—D (Blue)

I have secretly chosen a path compliance rule to evaluate whether a given vertex sequence is "compliant". The basic requirement is: adjacent vertices in the sequence must be connected by an edge (undirected). Additionally, there is a hidden rule applied, but I won't tell you which one.

Your goal is:
1. Infer the hidden rule by querying preset test sequences;
2. Determine whether the target sequence R* = A—D—E is compliant.

You can query the following three preset test sequences (one per query):
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

For each query, I will tell you whether the sequence is "compliant" or "non-compliant", but I won't tell you which rule it violated.

When you have enough information, submit your final answer. The final answer must include:
1. The hidden rule name you inferred (one of ALT, SIMPLE, EVEN, or REDSTART)
2. The compliance judgment for target sequence R* (compliant or non-compliant)

If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

Query test sequence T1:
<query_path>T1</query_path>

Query test sequence T2:
<query_path>T2</query_path>

Query test sequence T3:
<query_path>T3</query_path>

When submitting the final answer, specify the rule name and target compliance:
<answer>rule=ALT, target=compliant</answer>

or:
<answer>rule=SIMPLE, target=non-compliant</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通路线合规评估系统”。本系统用于校验跨城联运方案。

系统涵盖了五个核心枢纽城市：A, B, C, D, E。枢纽间开通了特定的联运路线，分为高铁（红）和航空（蓝）两种：
- A—B (高铁/红)
- B—C (航空/蓝)
- C—D (高铁/红)
- D—E (航空/蓝)
- E—A (高铁/红)
- B—D (航空/蓝)
- C—E (高铁/红)
- A—D (航空/蓝)

我已经秘密启用了一条调度合规性判定规则，用于评估给定的途径城市序列是否"合规"。基础要求是：序列中相邻城市之间必须存在联运路线。在此基础上，还附加了一条隐藏规则（ALT、SIMPLE、EVEN 或 REDSTART 之一），但我不会告诉你是哪一条。

你的目标是：
1. 通过查询预设的测试路线来推断隐藏的调度规则；
2.判定目标联运路线 R* = A—D—E 是否合规。

你可以查询以下三个预设测试路线（每次查询一个）：
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

对于每次查询，我会告诉你该路线是"合规"还是"不合规"，但不会告诉你违反了哪条规则。

当你收集足够信息后，请提交最终答案。最终答案需要包括：
1. 你推断出的隐藏规则名称（ALT、SIMPLE、EVEN 或 REDSTART 之一）
2. 目标路线 R* 的合规性判断（合规或不合规）

若答案错误或格式不符，评估失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

查询测试路线 T1：
<query_path>T1</query_path>

查询测试路线 T2：
<query_path>T2</query_path>

查询测试路线 T3：
<query_path>T3</query_path>

提交最终答案时，必须说明规则名称和目标路线的合规性，格式如下：
<answer>rule=ALT, target=合规</answer>

或：
<answer>rule=SIMPLE, target=不合规</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Routing Compliance Assessment System". This system verifies intercity transport plans.

The network covers five core hub cities: A, B, C, D, E. Specific intermodal routes are available between hubs, categorized into High-Speed Rail (Red) and Aviation (Blue):
- A—B (HSR/Red)
- B—C (Aviation/Blue)
- C—D (HSR/Red)
- D—E (Aviation/Blue)
- E—A (HSR/Red)
- B—D (Aviation/Blue)
- C—E (HSR/Red)
- A—D (Aviation/Blue)

I have secretly enabled a routing compliance rule to evaluate whether a given sequence of cities is "compliant". The basic requirement is: adjacent cities in the sequence must be connected by a valid route. Additionally, a hidden rule is applied (one of ALT, SIMPLE, EVEN, or REDSTART), but I won't tell you which one.

Your goal is:
1. Infer the hidden scheduling rule by querying preset test routes;
2. Determine whether the target routing plan R* = A—D—E is compliant.

You can query the following three preset test routes (one per query):
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

For each query, I will tell you whether the route is "compliant" or "non-compliant", but I won't specify which rule it violated.

When you have enough information, submit your final answer. The final answer must include:
1. The inferred hidden rule name (ALT, SIMPLE, EVEN, or REDSTART)
2. The compliance judgment for target route R* (compliant or non-compliant)

If the answer is wrong or the format is invalid, the assessment fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

Query test route T1:
<query_path>T1</query_path>

Query test route T2:
<query_path>T2</query_path>

Query test route T3:
<query_path>T3</query_path>

When submitting the final answer, specify the rule name and target compliance:
<answer>rule=ALT, target=compliant</answer>

or:
<answer>rule=SIMPLE, target=non-compliant</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“医疗转诊路径合规审查系统”。本系统用于校验院内患者流转的规范性。

系统涵盖了五个核心科室：A, B, C, D, E。科室间设有特定的转诊通道，分为急诊通道（红）和常规通道（蓝）：
- A—B (急诊通道/红)
- B—C (常规通道/蓝)
- C—D (急诊通道/红)
- D—E (常规通道/蓝)
- E—A (急诊通道/红)
- B—D (常规通道/蓝)
- C—E (急诊通道/红)
- A—D (常规通道/蓝)

我已经秘密选择了一条临床路径合规性判定规则，用于评估给定的科室流转序列是否"合规"。基础要求是：序列中相邻科室之间必须存在转诊通道。在此基础上，还附加了一条隐藏规则（ALT、SIMPLE、EVEN 或 REDSTART 之一），但我不会告诉你是哪一条。

你的目标是：
1. 通过查询预设的测试转诊序列来推断隐藏的医疗规则；
2. 判定目标转诊序列 R* = A—D—E 是否合规。

你可以查询以下三个预设测试序列（每次查询一个）：
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

对于每次查询，我会告诉你该序列是"合规"还是"不合规"，但不会告诉你违反了哪条规则。

当你收集足够信息后，请提交最终答案。最终答案需要包括：
1. 你推断出的隐藏规则名称（ALT、SIMPLE、EVEN 或 REDSTART 之一）
2. 目标序列 R* 的合规性判断（合规或不合规）

若答案错误或格式不符，审查失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

查询测试序列 T1：
<query_path>T1</query_path>

查询测试序列 T2：
<query_path>T2</query_path>

查询测试序列 T3：
<query_path>T3</query_path>

提交最终答案时，必须说明规则名称和目标序列的合规性，格式如下：
<answer>rule=ALT, target=合规</answer>

或：
<answer>rule=SIMPLE, target=不合规</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Medical Referral Path Compliance Review System". This system verifies the standardization of patient workflows within the hospital.

The network covers five core departments: A, B, C, D, E. Specific referral channels exist between departments, categorized into Emergency Channels (Red) and Routine Channels (Blue):
- A—B (Emergency/Red)
- B—C (Routine/Blue)
- C—D (Emergency/Red)
- D—E (Routine/Blue)
- E—A (Emergency/Red)
- B—D (Routine/Blue)
- C—E (Emergency/Red)
- A—D (Routine/Blue)

I have secretly selected a clinical path compliance rule to evaluate whether a given sequence of departments is "compliant". The basic requirement is: adjacent departments in the sequence must be connected by a valid channel. Additionally, a hidden rule is applied (one of ALT, SIMPLE, EVEN, or REDSTART), but I won't tell you which one.

Your goal is:
1. Infer the hidden medical rule by querying preset test referral sequences;
2. Determine whether the target referral sequence R* = A—D—E is compliant.

You can query the following three preset test sequences (one per query):
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

For each query, I will tell you whether the sequence is "compliant" or "non-compliant", but I won't specify which rule it violated.

When you have enough information, submit your final answer. The final answer must include:
1. The inferred hidden rule name (ALT, SIMPLE, EVEN, or REDSTART)
2. The compliance judgment for target sequence R* (compliant or non-compliant)

If the answer is wrong or the format is invalid, the review fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

Query test sequence T1:
<query_path>T1</query_path>

Query test sequence T2:
<query_path>T2</query_path>

Query test sequence T3:
<query_path>T3</query_path>

When submitting the final answer, specify the rule name and target compliance:
<answer>rule=ALT, target=compliant</answer>

or:
<answer>rule=SIMPLE, target=non-compliant</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎来到“自适应学习路径诊断系统”。本系统用于校验课程模块的递进关系。

系统内设五个核心知识模块：A, B, C, D, E。模块间存在特定的学习依赖路径，分为必修关联（红）和拓展关联（蓝）：
- A—B (必修关联/红)
- B—C (拓展关联/蓝)
- C—D (必修关联/红)
- D—E (拓展关联/蓝)
- E—A (必修关联/红)
- B—D (拓展关联/蓝)
- C—E (必修关联/红)
- A—D (拓展关联/蓝)

我已经秘密选择了一条课程规划判定规则，用于评估给定的模块学习序列是否"合规"。基础要求是：序列中相邻模块之间必须存在依赖路径。在此基础上，还附加了一条隐藏规则（ALT、SIMPLE、EVEN 或 REDSTART 之一），但我不会告诉你是哪一条。

你的目标是：
1. 通过查询预设的测试学习序列来推断隐藏的教学规则；
2. 判定目标学习序列 R* = A—D—E 是否合规。

你可以查询以下三个预设测试序列（每次查询一个）：
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

对于每次查询，我会告诉你该序列是"合规"还是"不合规"，但不会告诉你违反了哪条规则。

当你收集足够信息后，请提交最终答案。最终答案需要包括：
1. 你推断出的隐藏规则名称（ALT、SIMPLE、EVEN 或 REDSTART 之一）
2. 目标序列 R* 的合规性判断（合规或不合规）

若答案错误或格式不符，诊断失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

查询测试序列 T1：
<query_path>T1</query_path>

查询测试序列 T2：
<query_path>T2</query_path>

查询测试序列 T3：
<query_path>T3</query_path>

提交最终答案时，必须说明规则名称和目标序列的合规性，格式如下：
<answer>rule=ALT, target=合规</answer>

或：
<answer>rule=SIMPLE, target=不合规</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Diagnostic System". This system verifies the progression of curriculum modules.

The system contains five core knowledge modules: A, B, C, D, E. Specific learning dependencies exist between modules, categorized into Compulsory Links (Red) and Extension Links (Blue):
- A—B (Compulsory/Red)
- B—C (Extension/Blue)
- C—D (Compulsory/Red)
- D—E (Extension/Blue)
- E—A (Compulsory/Red)
- B—D (Extension/Blue)
- C—E (Compulsory/Red)
- A—D (Extension/Blue)

I have secretly selected a curriculum planning rule to evaluate whether a given sequence of study modules is "compliant". The basic requirement is: adjacent modules in the sequence must be connected by a dependency path. Additionally, a hidden rule is applied (one of ALT, SIMPLE, EVEN, or REDSTART), but I won't tell you which one.

Your goal is:
1. Infer the hidden pedagogical rule by querying preset test study sequences;
2. Determine whether the target study sequence R* = A—D—E is compliant.

You can query the following three preset test sequences (one per query):
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

For each query, I will tell you whether the sequence is "compliant" or "non-compliant", but I won't specify which rule it violated.

When you have enough information, submit your final answer. The final answer must include:
1. The inferred hidden rule name (ALT, SIMPLE, EVEN, or REDSTART)
2. The compliance judgment for target sequence R* (compliant or non-compliant)

If the answer is wrong or the format is invalid, the diagnostic fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

Query test sequence T1:
<query_path>T1</query_path>

Query test sequence T2:
<query_path>T2</query_path>

Query test sequence T3:
<query_path>T3</query_path>

When submitting the final answer, specify the rule name and target compliance:
<answer>rule=ALT, target=compliant</answer>

or:
<answer>rule=SIMPLE, target=non-compliant</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业物联网物料流转校验系统”。本系统用于排查生产线工艺路径的合规性。

工厂内设有五个核心加工车间：A, B, C, D, E。车间之间通过物理传送带连接，分为加急传送带（红）和标准传送带（蓝）：
- A—B (加急传送带/红)
- B—C (标准传送带/蓝)
- C—D (加急传送带/红)
- D—E (标准传送带/蓝)
- E—A (加急传送带/红)
- B—D (标准传送带/蓝)
- C—E (加急传送带/红)
- A—D (标准传送带/蓝)

我已经秘密应用了一条工艺约束规则，用于评估给定的物料流转序列是否"合规"。基础要求是：序列中相邻车间之间必须存在物理连通的传送带。在此基础上，还附加了一条隐藏规则（ALT、SIMPLE、EVEN 或 REDSTART 之一），但我不会告诉你是哪一条。

你的目标是：
1. 通过查询预设的测试流转序列来推断隐藏的工艺规则；
2. 判定目标流转序列 R* = A—D—E 是否合规。

你可以查询以下三个预设测试序列（每次查询一个）：
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

对于每次查询，我会告诉你该序列是"合规"还是"不合规"，但不会告诉你违反了哪条规则。

当你收集足够信息后，请提交最终答案。最终答案需要包括：
1. 你推断出的隐藏规则名称（ALT、SIMPLE、EVEN 或 REDSTART 之一）
2. 目标序列 R* 的合规性判断（合规或不合规）

若答案错误或格式不符，校验失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

查询测试序列 T1：
<query_path>T1</query_path>

查询测试序列 T2：
<query_path>T2</query_path>

查询测试序列 T3：
<query_path>T3</query_path>

提交最终答案时，必须说明规则名称和目标序列的合规性，格式如下：
<answer>rule=ALT, target=合规</answer>

或：
<answer>rule=SIMPLE, target=不合规</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "IIoT Material Flow Validation System". This system inspects the compliance of production line routing.

The factory consists of five core processing workshops: A, B, C, D, E. They are connected by physical conveyor belts, categorized into Expedited Belts (Red) and Standard Belts (Blue):
- A—B (Expedited/Red)
- B—C (Standard/Blue)
- C—D (Expedited/Red)
- D—E (Standard/Blue)
- E—A (Expedited/Red)
- B—D (Standard/Blue)
- C—E (Expedited/Red)
- A—D (Standard/Blue)

I have secretly applied a process constraint rule to evaluate whether a given sequence of material flow is "compliant". The basic requirement is: adjacent workshops in the sequence must be physically connected by a conveyor belt. Additionally, a hidden rule is applied (one of ALT, SIMPLE, EVEN, or REDSTART), but I won't tell you which one.

Your goal is:
1. Infer the hidden routing rule by querying preset test flow sequences;
2. Determine whether the target flow sequence R* = A—D—E is compliant.

You can query the following three preset test sequences (one per query):
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

For each query, I will tell you whether the sequence is "compliant" or "non-compliant", but I won't specify which rule it violated.

When you have enough information, submit your final answer. The final answer must include:
1. The inferred hidden rule name (ALT, SIMPLE, EVEN, or REDSTART)
2. The compliance judgment for target sequence R* (compliant or non-compliant)

If the answer is wrong or the format is invalid, the validation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

Query test sequence T1:
<query_path>T1</query_path>

Query test sequence T2:
<query_path>T2</query_path>

Query test sequence T3:
<query_path>T3</query_path>

When submitting the final answer, specify the rule name and target compliance:
<answer>rule=ALT, target=compliant</answer>

or:
<answer>rule=SIMPLE, target=non-compliant</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法程序流转合规审计系统”。本系统用于审查案件在各审批节点间的流转是否合法。

系统内涉及五个核心司法环节：A, B, C, D, E。环节间存在法定的流转渠道，分为简易程序通道（红）和普通程序通道（蓝）：
- A—B (简易程序/红)
- B—C (普通程序/蓝)
- C—D (简易程序/红)
- D—E (普通程序/蓝)
- E—A (简易程序/红)
- B—D (普通程序/蓝)
- C—E (简易程序/红)
- A—D (普通程序/蓝)

我已经秘密载入了一条程序法判定规则，用于评估给定的案件流转序列是否"合规"。基础要求是：序列中相邻环节之间必须存在法定的流转渠道。在此基础上，还附加了一条隐藏规则（ALT、SIMPLE、EVEN 或 REDSTART 之一），但我不会告诉你是哪一条。

你的目标是：
1. 通过查询预设的测试流转序列来推断隐藏的法律程序规则；
2. 判定目标流转序列 R* = A—D—E 是否合规。

你可以查询以下三个预设测试序列（每次查询一个）：
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

对于每次查询，我会告诉你该序列是"合规"还是"不合规"，但不会告诉你违反了哪条规则。

当你收集足够信息后，请提交最终答案。最终答案需要包括：
1. 你推断出的隐藏规则名称（ALT、SIMPLE、EVEN 或 REDSTART 之一）
2. 目标序列 R* 的合规性判断（合规或不合规）

若答案错误或格式不符，审计失败。

## 询问与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

查询测试序列 T1：
<query_path>T1</query_path>

查询测试序列 T2：
<query_path>T2</query_path>

查询测试序列 T3：
<query_path>T3</query_path>

提交最终答案时，必须说明规则名称和目标序列的合规性，格式如下：
<answer>rule=ALT, target=合规</answer>

或：
<answer>rule=SIMPLE, target=不合规</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Process Flow Compliance Audit System". This system reviews whether the routing of cases between approval nodes is legally valid.

The system involves five core judicial nodes: A, B, C, D, E. Statutory routing channels exist between these nodes, categorized into Summary Procedure Channels (Red) and Ordinary Procedure Channels (Blue):
- A—B (Summary Procedure/Red)
- B—C (Ordinary Procedure/Blue)
- C—D (Summary Procedure/Red)
- D—E (Ordinary Procedure/Blue)
- E—A (Summary Procedure/Red)
- B—D (Ordinary Procedure/Blue)
- C—E (Summary Procedure/Red)
- A—D (Ordinary Procedure/Blue)

I have secretly loaded a procedural law rule to evaluate whether a given sequence of case routing is "compliant". The basic requirement is: adjacent nodes in the sequence must be connected by a statutory routing channel. Additionally, a hidden rule is applied (one of ALT, SIMPLE, EVEN, or REDSTART), but I won't tell you which one.

Your goal is:
1. Infer the hidden legal procedural rule by querying preset test routing sequences;
2. Determine whether the target routing sequence R* = A—D—E is compliant.

You can query the following three preset test sequences (one per query):
- T1: B—C—D—E
- T2: A—D—B
- T3: C—E—A—B

For each query, I will tell you whether the sequence is "compliant" or "non-compliant", but I won't specify which rule it violated.

When you have enough information, submit your final answer. The final answer must include:
1. The inferred hidden rule name (ALT, SIMPLE, EVEN, or REDSTART)
2. The compliance judgment for target sequence R* (compliant or non-compliant)

If the answer is wrong or the format is invalid, the audit fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

Query test sequence T1:
<query_path>T1</query_path>

Query test sequence T2:
<query_path>T2</query_path>

Query test sequence T3:
<query_path>T3</query_path>

When submitting the final answer, specify the rule name and target compliance:
<answer>rule=ALT, target=compliant</answer>

or:
<answer>rule=SIMPLE, target=non-compliant</answer>
"""

    tags = ["answer", "query_path"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    # 难度说明：
    # 1 (简单) - 规则: REDSTART，需要两次查询即可确定
    # 2 (中等偏下) - 规则: EVEN，需要两次查询
    # 3 (中等偏上) - 规则: SIMPLE，需要至少两次查询
    # 4 (较难) - 规则: ALT，需要仔细分析
    # 5 (难) - 规则: EVEN，但测试序列更具迷惑性

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "rule": "REDSTART",
                "target_compliant": False,  # A—D—E: A—D是蓝色，不符合REDSTART
            },
            2: {
                "rule": "EVEN",
                "target_compliant": True,  # A—D—E: 2步（偶数）
            },
            3: {
                "rule": "SIMPLE",
                "target_compliant": True,  # A—D—E: 无重复顶点
            },
            4: {
                "rule": "ALT",
                "target_compliant": False,  # A—D—E: A—D(蓝), D—E(蓝)，不交替
            },
            5: {
                "rule": "EVEN",
                "target_compliant": True,  # A—D—E: 2步（偶数）
            },
        },
        "en": {
            1: {
                "rule": "REDSTART",
                "target_compliant": False,  # A—D—E: A—D is Blue, doesn't satisfy REDSTART
            },
            2: {
                "rule": "EVEN",
                "target_compliant": True,  # A—D—E: 2 steps (even)
            },
            3: {
                "rule": "SIMPLE",
                "target_compliant": True,  # A—D—E: no repeated vertices
            },
            4: {
                "rule": "ALT",
                "target_compliant": False,  # A—D—E: A—D(Blue), D—E(Blue), not alternating
            },
            5: {
                "rule": "EVEN",
                "target_compliant": True,  # A—D—E: 2 steps (even)
            },
        },
    }

    def __init__(self, config):
        # 定义图结构：边及其颜色
        self.edges = {
            frozenset(['A', 'B']): 'Red',
            frozenset(['B', 'C']): 'Blue',
            frozenset(['C', 'D']): 'Red',
            frozenset(['D', 'E']): 'Blue',
            frozenset(['E', 'A']): 'Red',
            frozenset(['B', 'D']): 'Blue',
            frozenset(['C', 'E']): 'Red',
            frozenset(['A', 'D']): 'Blue',
        }
        
        # 定义测试序列
        self.test_sequences = {
            'T1': ['B', 'C', 'D', 'E'],
            'T2': ['A', 'D', 'B'],
            'T3': ['C', 'E', 'A', 'B'],
        }
        
        # 目标序列
        self.target_sequence = ['A', 'D', 'E']
        
        # 查询计数器
        self.query_count = 0
        
        super().__init__(config)

    def _initialize_game(self):
        """根据难度初始化游戏"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 显式转为 int，防止字符串传入

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.rule = cfg["rule"]
        self.target_compliant = cfg["target_compliant"]
        
        self._game_info = {}

    def _check_path_basic(self, path):
        """检查路径基础可行性：相邻顶点间是否存在边"""
        for i in range(len(path) - 1):
            edge = frozenset([path[i], path[i+1]])
            if edge not in self.edges:
                return False
        return True

    def _get_path_colors(self, path):
        """获取路径经过的边的颜色序列"""
        colors = []
        for i in range(len(path) - 1):
            edge = frozenset([path[i], path[i+1]])
            colors.append(self.edges[edge])
        return colors

    def _check_rule_alt(self, path):
        """检查ALT规则：边颜色严格红蓝交替"""
        if not self._check_path_basic(path):
            return False
        colors = self._get_path_colors(path)
        for i in range(len(colors) - 1):
            if colors[i] == colors[i+1]:
                return False
        return True

    def _check_rule_simple(self, path):
        """检查SIMPLE规则：无重复顶点"""
        if not self._check_path_basic(path):
            return False
        return len(path) == len(set(path))

    def _check_rule_even(self, path):
        """检查EVEN规则：步数为偶数"""
        if not self._check_path_basic(path):
            return False
        steps = len(path) - 1
        return steps % 2 == 0

    def _check_rule_redstart(self, path):
        """检查REDSTART规则：第一条边为红色"""
        if not self._check_path_basic(path):
            return False
        colors = self._get_path_colors(path)
        return colors[0] == 'Red' if colors else False

    def _check_compliance(self, path):
        """根据当前规则检查路径合规性"""
        if self.rule == "ALT":
            return self._check_rule_alt(path)
        elif self.rule == "SIMPLE":
            return self._check_rule_simple(path)
        elif self.rule == "EVEN":
            return self._check_rule_even(path)
        elif self.rule == "REDSTART":
            return self._check_rule_redstart(path)
        else:
            raise ValueError(f"Unknown rule: {self.rule}")

    def evaluate(self, parsed_info):
        """评估最终答案"""
        # 解析答案: rule=XXX, target=YYY
        raw_ans = parsed_info.get("answer", "")
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip().lower()] = v.strip()
        
        if "rule" not in ans_dict or "target" not in ans_dict:
            return False
        
        # 1. 检查规则是否正确（大小写不敏感）
        if ans_dict["rule"].upper() != self.rule.upper():
            return False
        
        # 2. 检查目标序列合规性判断是否正确
        target_str = ans_dict["target"]
        
        # 判断用户给出的合规性答案
        if self.config.language == "zh":
            user_says_compliant = (target_str == "合规")
        else:
            user_says_compliant = (target_str.lower() == "compliant")
        
        return user_says_compliant == self.target_compliant

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        if "query_path" in parsed_info:
            test_id = parsed_info["query_path"].strip().upper()
            
            if test_id not in self.test_sequences:
                if self.config.language == "zh":
                    return "错误：无效的测试序列编号。请使用 T1、T2 或 T3。"
                else:
                    return "Error: Invalid test sequence ID. Please use T1, T2, or T3."
            
            # 只有有效查询才计数
            self.query_count += 1
            
            path = self.test_sequences[test_id]
            is_compliant = self._check_compliance(path)
            
            if self.config.language == "zh":
                return "合规" if is_compliant else "不合规"
            else:
                return "compliant" if is_compliant else "non-compliant"
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """
        将正确的合规性响应取反，生成一个错误答案用于反事实干预。
        """
        if self.config.language == "zh":
            if correct == "合规":
                return "不合规"
            elif correct == "不合规":
                return "合规"
            else:
                return "不合规"
        else:
            if correct == "compliant":
                return "non-compliant"
            elif correct == "non-compliant":
                return "compliant"
            else:
                return "non-compliant"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 合法的 XML 标签查询字符串
                "answer": str,   # 正确答案字符串
            }
        """
        results = []
        # 本游戏的有效查询仅限于 T1, T2, T3
        for test_id in ['T1', 'T2', 'T3']:
            path = self.test_sequences[test_id]
            is_compliant = self._check_compliance(path)
            
            if self.config.language == "zh":
                ans = "合规" if is_compliant else "不合规"
            else:
                ans = "compliant" if is_compliant else "non-compliant"
            
            results.append({
                "query": f"<query_path>{test_id}</query_path>",
                "answer": ans
            })
        return results

