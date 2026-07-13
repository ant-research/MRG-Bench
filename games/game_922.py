# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   集合差集：两个给定集合的差集中包含哪些元素
# ============================================================

from .base import Game
import re


class SetOperatorInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"集合算子推理"游戏，规则如下：

游戏设定了一个固定的宇宙集合 U = {{甲, 乙, 丙, 丁, 戊, 己, 庚, 辛}}。

我已秘密选择了一个集合算子 f，它属于以下四种规则之一：
- 规则 α：输出 A 去掉 B 的部分
- 规则 β：输出 B 去掉 A 的部分  
- 规则 γ：输出 A 和 B 的对称差（恰好在其中一个集合中的元素）
- 规则 δ：若 A 的元素个数大于等于 B 的元素个数，输出 A 去掉 B 的部分；否则输出 B 去掉 A 的部分

对于任意一对集合 (A, B)，算子 f 会产生一个输出集合 O = f(A, B)。

你的任务是：通过对预设的探测实例提问，推断出真实的算子规则，并将其应用到终局集合对上。

## 可用的探测实例

以下是你可以查询的集合对（编号 P1 到 P7）：
- P1: A={{甲,乙,丙}}, B={{甲,乙,丙}}
- P2: A={{甲,乙,丙}}, B={{丙,丁,戊}}
- P3: A={{甲,乙}}, B={{丙,丁}}
- P4: A={{甲,乙,丙,丁}}, B={{乙,丙}}
- P5: A={{丁,戊}}, B={{丁,戊,己}}
- P6: A=∅, B={{庚,辛}}
- P7: A={{甲,乙,丙}}, B={{丁,戊,己}}

终局集合对 PF: A={{乙,庚,辛}}, B={{甲,乙,丁,庚}}

## 可提出的问题类型

你可以对任意探测实例提出以下两类问题之一：

1. 基数奇偶查询：询问某个探测实例 Pi 上的输出集合 O 的元素个数是奇数还是偶数。我会回答"奇"或"偶"。

2. 成员查询：询问某个探测实例 Pi 上的输出集合 O 是否包含指定元素 x（x 必须是 U 中的元素）。我会回答"是"或"否"。

注意：你不能直接询问完整的输出集合 O，只能通过上述两种方式间接获取信息。

## 提问与答案格式（必须严格遵守）

每次只能提出一个问题，使用以下 XML 格式：

- 基数奇偶查询（例如询问 P3）：
<query_parity>P3</query_parity>

- 成员查询（例如询问 P2 的输出是否包含"甲"）：
<query_member>P2,甲</query_member>

提交最终答案时，必须说明推断出的规则（α、β、γ 或 δ）和终局集合对 PF 上的输出集合元素（用逗号隔开，顺序不限）：

<answer>rule=α, output=甲,丙</answer>

注意：如果输出集合为空集，请写作：
<answer>rule=α, output=空集</answer>

请尽可能少地提问，推断出正确的算子规则并计算终局输出。
"""

    game_rule_en = """\
Let's play a "Set Operator Inference" game. Here are the rules:

The game defines a fixed universe U = {{Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin}}.

I have secretly selected a set operator f, which is one of the following four rules:
- Rule α: Output A minus B
- Rule β: Output B minus A
- Rule γ: Output the symmetric difference of A and B (elements in exactly one set)
- Rule δ: If the size of A is greater than or equal to the size of B, output A minus B; otherwise output B minus A

For any pair of sets (A, B), the operator f produces an output set O = f(A, B).

Your task is: infer the true operator rule by querying preset probe instances, and apply it to the final set pair.

## Available Probe Instances

Here are the set pairs you can query (numbered P1 to P7):
- P1: A={{Jia,Yi,Bing}}, B={{Jia,Yi,Bing}}
- P2: A={{Jia,Yi,Bing}}, B={{Bing,Ding,Wu}}
- P3: A={{Jia,Yi}}, B={{Bing,Ding}}
- P4: A={{Jia,Yi,Bing,Ding}}, B={{Yi,Bing}}
- P5: A={{Ding,Wu}}, B={{Ding,Wu,Ji}}
- P6: A=∅, B={{Geng,Xin}}
- P7: A={{Jia,Yi,Bing}}, B={{Ding,Wu,Ji}}

Final set pair PF: A={{Yi,Geng,Xin}}, B={{Jia,Yi,Ding,Geng}}

## Question Types

You can ask one of the following two types of questions about any probe instance:

1. Parity Query: Ask whether the size of the output set O for probe instance Pi is odd or even. I will answer "odd" or "even".

2. Membership Query: Ask whether the output set O for probe instance Pi contains a specified element x (x must be in U). I will answer "yes" or "no".

Note: You cannot directly ask for the complete output set O; you can only obtain information indirectly through the above two methods.

## Query and Answer Format (strictly required)

Each turn you can only ask one question, using the following XML format:

- Parity Query (e.g., asking about P3):
<query_parity>P3</query_parity>

- Membership Query (e.g., asking if P2's output contains "Jia"):
<query_member>P2,Jia</query_member>

When submitting the final answer, you must specify the inferred rule (α, β, γ, or δ) and the output set elements for the final pair PF (comma-separated, order does not matter):

<answer>rule=α, output=Jia,Bing</answer>

Note: If the output set is empty, write:
<answer>rule=α, output=empty</answer>

Please use as few queries as possible to infer the correct operator rule and calculate the final output.
"""

    contextualized_rule_zh_1 = """\
欢迎使用「智能交通枢纽流量分析系统」。

系统监控着固定的路网节点集合 U = {{甲, 乙, 丙, 丁, 戊, 己, 庚, 辛}}。

我已秘密配置了一个流量过滤算子 f，它执行以下四种调度规则之一：
- 规则 α：输出节点组 A 中剔除节点组 B 后的剩余拥堵节点
- 规则 β：输出节点组 B 中剔除节点组 A 后的剩余拥堵节点
- 规则 γ：输出节点组 A 和 B 的对称差（即仅在其中一个节点组中发生拥堵的节点）
- 规则 δ：若节点组 A 的节点数大于等于 B，则输出 A 去掉 B 的部分；否则输出 B 去掉 A 的部分

对于任意一对节点组 (A, B)，算子 f 会产生一个输出节点组 O = f(A, B)。

你的任务是：通过对预设的探测实例提问，推断出真实的调度规则，并将其应用到终局节点组对上。

## 可用的探测实例

以下是你可以查询的集合对（编号 P1 到 P7）：
- P1: A={{甲,乙,丙}}, B={{甲,乙,丙}}
- P2: A={{甲,乙,丙}}, B={{丙,丁,戊}}
- P3: A={{甲,乙}}, B={{丙,丁}}
- P4: A={{甲,乙,丙,丁}}, B={{乙,丙}}
- P5: A={{丁,戊}}, B={{丁,戊,己}}
- P6: A=∅, B={{庚,辛}}
- P7: A={{甲,乙,丙}}, B={{丁,戊,己}}

终局集合对 PF: A={{乙,庚,辛}}, B={{甲,乙,丁,庚}}

## 可提出的问题类型

你可以对任意探测实例提出以下两类问题之一：

1. 基数奇偶查询：询问某个探测实例 Pi 上的输出集合 O 的元素个数是奇数还是偶数。我会回答"奇"或"偶"。

2. 成员查询：询问某个探测实例 Pi 上的输出集合 O 是否包含指定元素 x（x 必须是 U 中的元素）。我会回答"是"或"否"。

注意：你不能直接询问完整的输出集合 O，只能通过上述两种方式间接获取信息。

## 提问与答案格式（必须严格遵守）

每次只能提出一个问题，使用以下 XML 格式：

- 基数奇偶查询（例如询问 P3）：
<query_parity>P3</query_parity>

- 成员查询（例如询问 P2 的输出是否包含"甲"）：
<query_member>P2,甲</query_member>

提交最终答案时，必须说明推断出的规则（α、β、γ 或 δ）和终局集合对 PF 上的输出集合元素（用逗号隔开，顺序不限）：

<answer>rule=α, output=甲,丙</answer>

注意：如果输出集合为空集，请写作：
<answer>rule=α, output=空集</answer>

请尽可能少地提问，推断出正确的算子规则并计算终局输出。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Intelligent Transit Hub Traffic Analysis System.

The system monitors a fixed universe of network nodes U = {{Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin}}.

I have secretly configured a traffic filtering operator f, which applies one of the following four dispatch rules:
- Rule α: Output nodes in group A excluding group B
- Rule β: Output nodes in group B excluding group A
- Rule γ: Output the symmetric difference of groups A and B (nodes congested in exactly one group)
- Rule δ: If the size of group A is greater than or equal to group B, output A minus B; otherwise output B minus A

For any pair of node groups (A, B), the operator f produces an output group O = f(A, B).

Your task is: infer the true dispatch rule by querying preset probe instances, and apply it to the final node group pair.

## Available Probe Instances

Here are the set pairs you can query (numbered P1 to P7):
- P1: A={{Jia,Yi,Bing}}, B={{Jia,Yi,Bing}}
- P2: A={{Jia,Yi,Bing}}, B={{Bing,Ding,Wu}}
- P3: A={{Jia,Yi}}, B={{Bing,Ding}}
- P4: A={{Jia,Yi,Bing,Ding}}, B={{Yi,Bing}}
- P5: A={{Ding,Wu}}, B={{Ding,Wu,Ji}}
- P6: A=∅, B={{Geng,Xin}}
- P7: A={{Jia,Yi,Bing}}, B={{Ding,Wu,Ji}}

Final set pair PF: A={{Yi,Geng,Xin}}, B={{Jia,Yi,Ding,Geng}}

## Question Types

You can ask one of the following two types of questions about any probe instance:

1. Parity Query: Ask whether the size of the output set O for probe instance Pi is odd or even. I will answer "odd" or "even".

2. Membership Query: Ask whether the output set O for probe instance Pi contains a specified element x (x must be in U). I will answer "yes" or "no".

Note: You cannot directly ask for the complete output set O; you can only obtain information indirectly through the above two methods.

## Query and Answer Format (strictly required)

Each turn you can only ask one question, using the following XML format:

- Parity Query (e.g., asking about P3):
<query_parity>P3</query_parity>

- Membership Query (e.g., asking if P2's output contains "Jia"):
<query_member>P2,Jia</query_member>

When submitting the final answer, you must specify the inferred rule (α, β, γ, or δ) and the output set elements for the final pair PF (comma-separated, order does not matter):

<answer>rule=α, output=Jia,Bing</answer>

Note: If the output set is empty, write:
<answer>rule=α, output=empty</answer>

Please use as few queries as possible to infer the correct operator rule and calculate the final output.
"""

    contextualized_rule_zh_2 = """\
欢迎进入「流行病学病株交叉比对系统」。

系统收录了固定的目标毒株集合 U = {{甲, 乙, 丙, 丁, 戊, 己, 庚, 辛}}。

我已秘密设定了一个诊断筛查算子 f，它遵循以下四种分离规则之一：
- 规则 α：输出样本池 A 排除样本池 B 后的特异性毒株
- 规则 β：输出样本池 B 排除样本池 A 后的特异性毒株
- 规则 γ：输出样本池 A 和 B 的对称差（恰好仅在其中一个样本池内检出的毒株）
- 规则 δ：若样本池 A 的检出毒株数大于等于 B，输出 A 去掉 B 的部分；否则输出 B 去掉 A 的部分

对于任意一对样本池 (A, B)，算子 f 会产生一个特异性毒株输出集 O = f(A, B)。

你的任务是：通过对预设的探测实例提问，推断出真实的筛查规则，并将其应用到终局样本池对上。

## 可用的探测实例

以下是你可以查询的集合对（编号 P1 到 P7）：
- P1: A={{甲,乙,丙}}, B={{甲,乙,丙}}
- P2: A={{甲,乙,丙}}, B={{丙,丁,戊}}
- P3: A={{甲,乙}}, B={{丙,丁}}
- P4: A={{甲,乙,丙,丁}}, B={{乙,丙}}
- P5: A={{丁,戊}}, B={{丁,戊,己}}
- P6: A=∅, B={{庚,辛}}
- P7: A={{甲,乙,丙}}, B={{丁,戊,己}}

终局集合对 PF: A={{乙,庚,辛}}, B={{甲,乙,丁,庚}}

## 可提出的问题类型

你可以对任意探测实例提出以下两类问题之一：

1. 基数奇偶查询：询问某个探测实例 Pi 上的输出集合 O 的元素个数是奇数还是偶数。我会回答"奇"或"偶"。

2. 成员查询：询问某个探测实例 Pi 上的输出集合 O 是否包含指定元素 x（x 必须是 U 中的元素）。我会回答"是"或"否"。

注意：你不能直接询问完整的输出集合 O，只能通过上述两种方式间接获取信息。

## 提问与答案格式（必须严格遵守）

每次只能提出一个问题，使用以下 XML 格式：

- 基数奇偶查询（例如询问 P3）：
<query_parity>P3</query_parity>

- 成员查询（例如询问 P2 的输出是否包含"甲"）：
<query_member>P2,甲</query_member>

提交最终答案时，必须说明推断出的规则（α、β、γ 或 δ）和终局集合对 PF 上的输出集合元素（用逗号隔开，顺序不限）：

<answer>rule=α, output=甲,丙</answer>

注意：如果输出集合为空集，请写作：
<answer>rule=α, output=空集</answer>

请尽可能少地提问，推断出正确的算子规则并计算终局输出。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Epidemiological Strain Cross-Matching System.

The system tracks a fixed universe of target virus strains U = {{Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin}}.

I have secretly configured a diagnostic screening operator f, which follows one of four isolation rules:
- Rule α: Output sample pool A excluding sample pool B
- Rule β: Output sample pool B excluding sample pool A
- Rule γ: Output the symmetric difference of pools A and B (strains detected in exactly one pool)
- Rule δ: If the size of pool A is greater than or equal to pool B, output A minus B; otherwise output B minus A

For any pair of sample pools (A, B), the operator f produces an output strain set O = f(A, B).

Your task is: infer the true isolation rule by querying preset probe instances, and apply it to the final sample pool pair.

## Available Probe Instances

Here are the set pairs you can query (numbered P1 to P7):
- P1: A={{Jia,Yi,Bing}}, B={{Jia,Yi,Bing}}
- P2: A={{Jia,Yi,Bing}}, B={{Bing,Ding,Wu}}
- P3: A={{Jia,Yi}}, B={{Bing,Ding}}
- P4: A={{Jia,Yi,Bing,Ding}}, B={{Yi,Bing}}
- P5: A={{Ding,Wu}}, B={{Ding,Wu,Ji}}
- P6: A=∅, B={{Geng,Xin}}
- P7: A={{Jia,Yi,Bing}}, B={{Ding,Wu,Ji}}

Final set pair PF: A={{Yi,Geng,Xin}}, B={{Jia,Yi,Ding,Geng}}

## Question Types

You can ask one of the following two types of questions about any probe instance:

1. Parity Query: Ask whether the size of the output set O for probe instance Pi is odd or even. I will answer "odd" or "even".

2. Membership Query: Ask whether the output set O for probe instance Pi contains a specified element x (x must be in U). I will answer "yes" or "no".

Note: You cannot directly ask for the complete output set O; you can only obtain information indirectly through the above two methods.

## Query and Answer Format (strictly required)

Each turn you can only ask one question, using the following XML format:

- Parity Query (e.g., asking about P3):
<query_parity>P3</query_parity>

- Membership Query (e.g., asking if P2's output contains "Jia"):
<query_member>P2,Jia</query_member>

When submitting the final answer, you must specify the inferred rule (α, β, γ, or δ) and the output set elements for the final pair PF (comma-separated, order does not matter):

<answer>rule=α, output=Jia,Bing</answer>

Note: If the output set is empty, write:
<answer>rule=α, output=empty</answer>

Please use as few queries as possible to infer the correct operator rule and calculate the final output.
"""

    contextualized_rule_zh_3 = """\
欢迎使用「AI自适应学情图谱分析引擎」。

我们的核心能力知识库设定为固定的知识点集合 U = {{甲, 乙, 丙, 丁, 戊, 己, 庚, 辛}}。

我已秘密调用了一个学情比对算子 f，它属于以下四种评估规则之一：
- 规则 α：输出掌握图谱 A 中超出目标图谱 B 的冗余知识点
- 规则 β：输出目标图谱 B 中学生掌握图谱 A 欠缺的薄弱知识点
- 规则 γ：输出图谱 A 和 B 的对称差（恰好在其中一个图谱中的知识点偏差）
- 规则 δ：若图谱 A 的知识点个数大于等于 B，输出 A 去掉 B 的部分；否则输出 B 去掉 A 的部分

对于任意一对知识图谱 (A, B)，算子 f 会产生一个诊断输出图谱 O = f(A, B)。

你的任务是：通过对预设的探测实例提问，推断出真实的评估规则，并将其应用到终局图谱对上。

## 可用的探测实例

以下是你可以查询的集合对（编号 P1 到 P7）：
- P1: A={{甲,乙,丙}}, B={{甲,乙,丙}}
- P2: A={{甲,乙,丙}}, B={{丙,丁,戊}}
- P3: A={{甲,乙}}, B={{丙,丁}}
- P4: A={{甲,乙,丙,丁}}, B={{乙,丙}}
- P5: A={{丁,戊}}, B={{丁,戊,己}}
- P6: A=∅, B={{庚,辛}}
- P7: A={{甲,乙,丙}}, B={{丁,戊,己}}

终局集合对 PF: A={{乙,庚,辛}}, B={{甲,乙,丁,庚}}

## 可提出的问题类型

你可以对任意探测实例提出以下两类问题之一：

1. 基数奇偶查询：询问某个探测实例 Pi 上的输出集合 O 的元素个数是奇数还是偶数。我会回答"奇"或"偶"。

2. 成员查询：询问某个探测实例 Pi 上的输出集合 O 是否包含指定元素 x（x 必须是 U 中的元素）。我会回答"是"或"否"。

注意：你不能直接询问完整的输出集合 O，只能通过上述两种方式间接获取信息。

## 提问与答案格式（必须严格遵守）

每次只能提出一个问题，使用以下 XML 格式：

- 基数奇偶查询（例如询问 P3）：
<query_parity>P3</query_parity>

- 成员查询（例如询问 P2 的输出是否包含"甲"）：
<query_member>P2,甲</query_member>

提交最终答案时，必须说明推断出的规则（α、β、γ 或 δ）和终局集合对 PF 上的输出集合元素（用逗号隔开，顺序不限）：

<answer>rule=α, output=甲,丙</answer>

注意：如果输出集合为空集，请写作：
<answer>rule=α, output=空集</answer>

请尽可能少地提问，推断出正确的算子规则并计算终局输出。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the AI Adaptive Learning Profile Analysis Engine.

Our core competency repository is defined by a fixed universe of knowledge modules U = {{Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin}}.

I have secretly invoked a learning comparison operator f, applying one of the following four assessment rules:
- Rule α: Output mastered profile A excluding target profile B
- Rule β: Output target profile B excluding mastered profile A
- Rule γ: Output the symmetric difference of profiles A and B (modules present in exactly one profile)
- Rule δ: If the size of profile A is greater than or equal to profile B, output A minus B; otherwise output B minus A

For any pair of knowledge profiles (A, B), the operator f produces an output diagnostic profile O = f(A, B).

Your task is: infer the true assessment rule by querying preset probe instances, and apply it to the final profile pair.

## Available Probe Instances

Here are the set pairs you can query (numbered P1 to P7):
- P1: A={{Jia,Yi,Bing}}, B={{Jia,Yi,Bing}}
- P2: A={{Jia,Yi,Bing}}, B={{Bing,Ding,Wu}}
- P3: A={{Jia,Yi}}, B={{Bing,Ding}}
- P4: A={{Jia,Yi,Bing,Ding}}, B={{Yi,Bing}}
- P5: A={{Ding,Wu}}, B={{Ding,Wu,Ji}}
- P6: A=∅, B={{Geng,Xin}}
- P7: A={{Jia,Yi,Bing}}, B={{Ding,Wu,Ji}}

Final set pair PF: A={{Yi,Geng,Xin}}, B={{Jia,Yi,Ding,Geng}}

## Question Types

You can ask one of the following two types of questions about any probe instance:

1. Parity Query: Ask whether the size of the output set O for probe instance Pi is odd or even. I will answer "odd" or "even".

2. Membership Query: Ask whether the output set O for probe instance Pi contains a specified element x (x must be in U). I will answer "yes" or "no".

Note: You cannot directly ask for the complete output set O; you can only obtain information indirectly through the above two methods.

## Query and Answer Format (strictly required)

Each turn you can only ask one question, using the following XML format:

- Parity Query (e.g., asking about P3):
<query_parity>P3</query_parity>

- Membership Query (e.g., asking if P2's output contains "Jia"):
<query_member>P2,Jia</query_member>

When submitting the final answer, you must specify the inferred rule (α, β, γ, or δ) and the output set elements for the final pair PF (comma-separated, order does not matter):

<answer>rule=α, output=Jia,Bing</answer>

Note: If the output set is empty, write:
<answer>rule=α, output=empty</answer>

Please use as few queries as possible to infer the correct operator rule and calculate the final output.
"""

    contextualized_rule_zh_4 = """\
欢迎使用「工业产线缺陷隔离诊断系统」。

系统预设了固定的核心零部件故障代码集合 U = {{甲, 乙, 丙, 丁, 戊, 己, 庚, 辛}}。

我已秘密加载了一个缺陷隔离算子 f，它执行以下四种排查规则之一：
- 规则 α：输出检验批次 A 中剔除对照批次 B 后的特有故障代码
- 规则 β：输出对照批次 B 中剔除检验批次 A 后的特有故障代码
- 规则 γ：输出批次 A 和 B 的对称差（恰好在单一批次中出现的孤立故障）
- 规则 δ：若批次 A 的故障数大于等于 B，输出 A 剔除 B 的部分；否则输出 B 剔除 A 的部分

对于任意一对检验批次 (A, B)，算子 f 会产生一个核心故障输出集 O = f(A, B)。

你的任务是：通过对预设的探测实例提问，推断出真实的排查规则，并将其应用到终局检验批次对上。

## 可用的探测实例

以下是你可以查询的集合对（编号 P1 到 P7）：
- P1: A={{甲,乙,丙}}, B={{甲,乙,丙}}
- P2: A={{甲,乙,丙}}, B={{丙,丁,戊}}
- P3: A={{甲,乙}}, B={{丙,丁}}
- P4: A={{甲,乙,丙,丁}}, B={{乙,丙}}
- P5: A={{丁,戊}}, B={{丁,戊,己}}
- P6: A=∅, B={{庚,辛}}
- P7: A={{甲,乙,丙}}, B={{丁,戊,己}}

终局集合对 PF: A={{乙,庚,辛}}, B={{甲,乙,丁,庚}}

## 可提出的问题类型

你可以对任意探测实例提出以下两类问题之一：

1. 基数奇偶查询：询问某个探测实例 Pi 上的输出集合 O 的元素个数是奇数还是偶数。我会回答"奇"或"偶"。

2. 成员查询：询问某个探测实例 Pi 上的输出集合 O 是否包含指定元素 x（x 必须是 U 中的元素）。我会回答"是"或"否"。

注意：你不能直接询问完整的输出集合 O，只能通过上述两种方式间接获取信息。

## 提问与答案格式（必须严格遵守）

每次只能提出一个问题，使用以下 XML 格式：

- 基数奇偶查询（例如询问 P3）：
<query_parity>P3</query_parity>

- 成员查询（例如询问 P2 的输出是否包含"甲"）：
<query_member>P2,甲</query_member>

提交最终答案时，必须说明推断出的规则（α、β、γ 或 δ）和终局集合对 PF 上的输出集合元素（用逗号隔开，顺序不限）：

<answer>rule=α, output=甲,丙</answer>

注意：如果输出集合为空集，请写作：
<answer>rule=α, output=空集</answer>

请尽可能少地提问，推断出正确的算子规则并计算终局输出。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Industrial Assembly Defect Isolation System.

The system presets a fixed universe of core component fault codes U = {{Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin}}.

I have secretly loaded a defect isolation operator f, executing one of the following four diagnostic rules:
- Rule α: Output inspection batch A excluding control batch B
- Rule β: Output control batch B excluding inspection batch A
- Rule γ: Output the symmetric difference of batches A and B (faults isolated to exactly one batch)
- Rule δ: If the size of batch A is greater than or equal to batch B, output A minus B; otherwise output B minus A

For any pair of inspection batches (A, B), the operator f produces an output fault set O = f(A, B).

Your task is: infer the true diagnostic rule by querying preset probe instances, and apply it to the final batch pair.

## Available Probe Instances

Here are the set pairs you can query (numbered P1 to P7):
- P1: A={{Jia,Yi,Bing}}, B={{Jia,Yi,Bing}}
- P2: A={{Jia,Yi,Bing}}, B={{Bing,Ding,Wu}}
- P3: A={{Jia,Yi}}, B={{Bing,Ding}}
- P4: A={{Jia,Yi,Bing,Ding}}, B={{Yi,Bing}}
- P5: A={{Ding,Wu}}, B={{Ding,Wu,Ji}}
- P6: A=∅, B={{Geng,Xin}}
- P7: A={{Jia,Yi,Bing}}, B={{Ding,Wu,Ji}}

Final set pair PF: A={{Yi,Geng,Xin}}, B={{Jia,Yi,Ding,Geng}}

## Question Types

You can ask one of the following two types of questions about any probe instance:

1. Parity Query: Ask whether the size of the output set O for probe instance Pi is odd or even. I will answer "odd" or "even".

2. Membership Query: Ask whether the output set O for probe instance Pi contains a specified element x (x must be in U). I will answer "yes" or "no".

Note: You cannot directly ask for the complete output set O; you can only obtain information indirectly through the above two methods.

## Query and Answer Format (strictly required)

Each turn you can only ask one question, using the following XML format:

- Parity Query (e.g., asking about P3):
<query_parity>P3</query_parity>

- Membership Query (e.g., asking if P2's output contains "Jia"):
<query_member>P2,Jia</query_member>

When submitting the final answer, you must specify the inferred rule (α, β, γ, or δ) and the output set elements for the final pair PF (comma-separated, order does not matter):

<answer>rule=α, output=Jia,Bing</answer>

Note: If the output set is empty, write:
<answer>rule=α, output=empty</answer>

Please use as few queries as possible to infer the correct operator rule and calculate the final output.
"""

    contextualized_rule_zh_5 = """\
欢迎使用「智能法务证据链交叉审查系统」。

法庭采信了固定的关键证据标号集合 U = {{甲, 乙, 丙, 丁, 戊, 己, 庚, 辛}}。

我已秘密启用了一个证据核验算子 f，它属于以下四种质证规则之一：
- 规则 α：输出原告证据集 A 中未被被告证据集 B 覆盖的部分
- 规则 β：输出被告证据集 B 中未被原告证据集 A 涵盖的部分
- 规则 γ：输出证据集 A 和 B 的对称差（即仅被单方出示的争议证据）
- 规则 δ：若证据集 A 的数量大于等于 B，输出 A 排除 B 的部分；否则输出 B 排除 A 的部分

对于任意一对证据集 (A, B)，算子 f 会产生一个有效质证输出集 O = f(A, B)。

你的任务是：通过对预设的探测实例提问，推断出真实的质证规则，并将其应用到终局证据集对上。

## 可用的探测实例

以下是你可以查询的集合对（编号 P1 到 P7）：
- P1: A={{甲,乙,丙}}, B={{甲,乙,丙}}
- P2: A={{甲,乙,丙}}, B={{丙,丁,戊}}
- P3: A={{甲,乙}}, B={{丙,丁}}
- P4: A={{甲,乙,丙,丁}}, B={{乙,丙}}
- P5: A={{丁,戊}}, B={{丁,戊,己}}
- P6: A=∅, B={{庚,辛}}
- P7: A={{甲,乙,丙}}, B={{丁,戊,己}}

终局集合对 PF: A={{乙,庚,辛}}, B={{甲,乙,丁,庚}}

## 可提出的问题类型

你可以对任意探测实例提出以下两类问题之一：

1. 基数奇偶查询：询问某个探测实例 Pi 上的输出集合 O 的元素个数是奇数还是偶数。我会回答"奇"或"偶"。

2. 成员查询：询问某个探测实例 Pi 上的输出集合 O 是否包含指定元素 x（x 必须是 U 中的元素）。我会回答"是"或"否"。

注意：你不能直接询问完整的输出集合 O，只能通过上述两种方式间接获取信息。

## 提问与答案格式（必须严格遵守）

每次只能提出一个问题，使用以下 XML 格式：

- 基数奇偶查询（例如询问 P3）：
<query_parity>P3</query_parity>

- 成员查询（例如询问 P2 的输出是否包含"甲"）：
<query_member>P2,甲</query_member>

提交最终答案时，必须说明推断出的规则（α、β、γ 或 δ）和终局集合对 PF 上的输出集合元素（用逗号隔开，顺序不限）：

<answer>rule=α, output=甲,丙</answer>

注意：如果输出集合为空集，请写作：
<answer>rule=α, output=空集</answer>

请尽可能少地提问，推断出正确的算子规则并计算终局输出。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Intelligent Legal Evidence Cross-Examination System.

The court admits a fixed universe of key evidence markers U = {{Jia, Yi, Bing, Ding, Wu, Ji, Geng, Xin}}.

I have secretly activated an evidence verification operator f, which applies one of the following four cross-examination rules:
- Rule α: Output plaintiff's evidence set A excluding defendant's set B
- Rule β: Output defendant's set B excluding plaintiff's set A
- Rule γ: Output the symmetric difference of sets A and B (disputed evidence presented by exactly one side)
- Rule δ: If the size of set A is greater than or equal to set B, output A minus B; otherwise output B minus A

For any pair of evidence sets (A, B), the operator f produces an output valid evidence set O = f(A, B).

Your task is: infer the true cross-examination rule by querying preset probe instances, and apply it to the final evidence set pair.

## Available Probe Instances

Here are the set pairs you can query (numbered P1 to P7):
- P1: A={{Jia,Yi,Bing}}, B={{Jia,Yi,Bing}}
- P2: A={{Jia,Yi,Bing}}, B={{Bing,Ding,Wu}}
- P3: A={{Jia,Yi}}, B={{Bing,Ding}}
- P4: A={{Jia,Yi,Bing,Ding}}, B={{Yi,Bing}}
- P5: A={{Ding,Wu}}, B={{Ding,Wu,Ji}}
- P6: A=∅, B={{Geng,Xin}}
- P7: A={{Jia,Yi,Bing}}, B={{Ding,Wu,Ji}}

Final set pair PF: A={{Yi,Geng,Xin}}, B={{Jia,Yi,Ding,Geng}}

## Question Types

You can ask one of the following two types of questions about any probe instance:

1. Parity Query: Ask whether the size of the output set O for probe instance Pi is odd or even. I will answer "odd" or "even".

2. Membership Query: Ask whether the output set O for probe instance Pi contains a specified element x (x must be in U). I will answer "yes" or "no".

Note: You cannot directly ask for the complete output set O; you can only obtain information indirectly through the above two methods.

## Query and Answer Format (strictly required)

Each turn you can only ask one question, using the following XML format:

- Parity Query (e.g., asking about P3):
<query_parity>P3</query_parity>

- Membership Query (e.g., asking if P2's output contains "Jia"):
<query_member>P2,Jia</query_member>

When submitting the final answer, you must specify the inferred rule (α, β, γ, or δ) and the output set elements for the final pair PF (comma-separated, order does not matter):

<answer>rule=α, output=Jia,Bing</answer>

Note: If the output set is empty, write:
<answer>rule=α, output=empty</answer>

Please use as few queries as possible to infer the correct operator rule and calculate the final output.
"""

    tags = ["answer", "query_parity", "query_member"]

    # 游戏元数据
    reasoning_type = "溯因推理"
    data_structure = "集合"

    # 难度配置：
    # 1 (简单)       - 规则 α，较容易区分
    # 2 (中等偏下)   - 规则 β，需要2-3次查询
    # 3 (中等偏上)   - 规则 γ，需要理解对称差
    # 4 (较难)       - 规则 δ，需要考虑大小关系
    # 5 (难)         - 规则 δ，边界情况更复杂

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"rule": "α"},  # A \ B
            2: {"rule": "β"},  # B \ A
            3: {"rule": "γ"},  # A Δ B
            4: {"rule": "δ"},  # 条件规则
            5: {"rule": "δ"},  # 条件规则（更难验证）
        },
        "en": {
            1: {"rule": "α"},
            2: {"rule": "β"},
            3: {"rule": "γ"},
            4: {"rule": "δ"},
            5: {"rule": "δ"},
        },
    }

    def __init__(self, config):
        # 定义宇宙集合和探测实例（中英文版本）
        self.universe_zh = {"甲", "乙", "丙", "丁", "戊", "己", "庚", "辛"}
        self.universe_en = {"Jia", "Yi", "Bing", "Ding", "Wu", "Ji", "Geng", "Xin"}
        
        # 探测实例定义（中文版）
        self.probes_zh = {
            "P1": ({"甲", "乙", "丙"}, {"甲", "乙", "丙"}),
            "P2": ({"甲", "乙", "丙"}, {"丙", "丁", "戊"}),
            "P3": ({"甲", "乙"}, {"丙", "丁"}),
            "P4": ({"甲", "乙", "丙", "丁"}, {"乙", "丙"}),
            "P5": ({"丁", "戊"}, {"丁", "戊", "己"}),
            "P6": (set(), {"庚", "辛"}),
            "P7": ({"甲", "乙", "丙"}, {"丁", "戊", "己"}),
            "PF": ({"乙", "庚", "辛"}, {"甲", "乙", "丁", "庚"}),
        }
        
        # 探测实例定义（英文版）
        self.probes_en = {
            "P1": ({"Jia", "Yi", "Bing"}, {"Jia", "Yi", "Bing"}),
            "P2": ({"Jia", "Yi", "Bing"}, {"Bing", "Ding", "Wu"}),
            "P3": ({"Jia", "Yi"}, {"Bing", "Ding"}),
            "P4": ({"Jia", "Yi", "Bing", "Ding"}, {"Yi", "Bing"}),
            "P5": ({"Ding", "Wu"}, {"Ding", "Wu", "Ji"}),
            "P6": (set(), {"Geng", "Xin"}),
            "P7": ({"Jia", "Yi", "Bing"}, {"Ding", "Wu", "Ji"}),
            "PF": ({"Yi", "Geng", "Xin"}, {"Jia", "Yi", "Ding", "Geng"}),
        }
        
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：选择规则和语言配置"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数类型

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.rule = cfg["rule"]
        
        # 根据语言选择对应的集合定义
        if lang == "zh":
            self.universe = self.universe_zh
            self.probes = self.probes_zh
            self.empty_word = "空集"
        else:
            self.universe = self.universe_en
            self.probes = self.probes_en
            self.empty_word = "empty"
        
        # 预计算所有探测实例的输出（Ground Truth）
        self.outputs = {}
        for probe_id, (A, B) in self.probes.items():
            self.outputs[probe_id] = self._apply_rule(A, B, self.rule)
        
        self._game_info = {}  # 无需向规则中注入变量

    def _apply_rule(self, A, B, rule):
        """根据规则计算输出集合"""
        if rule == "α":
            return A - B
        elif rule == "β":
            return B - A
        elif rule == "γ":
            return A.symmetric_difference(B)
        elif rule == "δ":
            if len(A) >= len(B):
                return A - B
            else:
                return B - A
        else:
            raise ValueError(f"Unknown rule: {rule}")

    def evaluate(self, parsed_info):
        """评估玩家提交的答案"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析答案格式：rule=X, output=a,b,c 或 rule=X, output=空集
        # 使用正则提取 rule 和 output 两个字段
        rule_match = re.search(r'rule\s*=\s*([αβγδ])', raw_ans)
        # 更鲁棒的处理：非贪婪匹配到行尾，防止提取到跨行的多余文本
        output_match = re.search(r'output\s*=\s*(.*?)(?=\n|$)', raw_ans)
        
        if not rule_match or not output_match:
            return False
        
        ans_rule = rule_match.group(1).strip()
        ans_output_str = output_match.group(1).strip()
        
        # 1. 检查规则是否正确
        if ans_rule != self.rule:
            return False
        
        # 2. 检查终局输出集合是否正确
        correct_output = self.outputs["PF"]
        
        try:
            # 去除可能的额外文本和中文标点（使解析更鲁棒）
            ans_output_str = ans_output_str.split("这是")[0].split("This is")[0].strip()
            ans_output_str = ans_output_str.replace("，", ",")
            ans_output_str = ans_output_str.rstrip('。.!！ ')
            
            if ans_output_str == self.empty_word:
                model_output = set()
            else:
                model_output = set(x.strip() for x in ans_output_str.split(",") if x.strip())
        except:
            return False
        
        return model_output == correct_output

    def _cf_core_produce(self, parsed_info):
        """执行原始的查询逻辑"""
        if self.config.language == "zh":
            odd_word, even_word = "奇", "偶"
            yes_word, no_word = "是", "否"
            error_invalid = "错误：无效的探测实例编号。"
            error_element = "错误：元素不在宇宙集合中。"
            error_format = "错误：格式无效。"
            error_pf = "错误：不能直接查询终局集合对 PF，请通过 P1-P7 推断规则后计算。"
        else:
            odd_word, even_word = "odd", "even"
            yes_word, no_word = "yes", "no"
            error_invalid = "Error: Invalid probe instance ID."
            error_element = "Error: Element not in universe."
            error_format = "Error: Invalid format."
            error_pf = "Error: Cannot query the final pair PF directly. Please infer the rule from P1-P7."

        valid_probe_ids = {pid for pid in self.probes.keys() if pid != "PF"}

        # 优先级：parity > member
        if "query_parity" in parsed_info:
            probe_id = parsed_info["query_parity"].strip()
            if probe_id == "PF":
                return error_pf
            if probe_id not in valid_probe_ids:
                return error_invalid
            
            output_set = self.outputs[probe_id]
            size = len(output_set)
            return odd_word if size % 2 == 1 else even_word

        elif "query_member" in parsed_info:
            try:
                raw = parsed_info["query_member"]
                parts = raw.split(",")
                if len(parts) != 2:
                    return error_format
                
                probe_id = parts[0].strip()
                element = parts[1].strip()
                
                if probe_id == "PF":
                    return error_pf
                if probe_id not in valid_probe_ids:
                    return error_invalid
                
                if element not in self.universe:
                    return error_element
                
                output_set = self.outputs[probe_id]
                return yes_word if element in output_set else no_word
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """根据正确答案生成一个明显不同的错误答案"""
        if self.config.language == "zh":
            swap_map = {"是": "否", "否": "是", "奇": "偶", "偶": "奇"}
            if correct in swap_map:
                return swap_map[correct]
        else:
            correct_lower = correct.lower()
            swap_map = {"yes": "no", "no": "yes", "odd": "even", "even": "odd"}
            if correct_lower in swap_map:
                return swap_map[correct_lower]
        
        # 若都不匹配，追加 _WRONG
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
        queries = []
        
        # 获取所有探测实例ID（排除终局实例 PF，仅包含 P1-P7）
        # 虽然代码逻辑允许查询 PF，但游戏规则描述中仅 P1-P7 为可用探测实例
        probe_ids = sorted([pid for pid in self.probes.keys() if pid != "PF"])
        
        # 获取宇宙集合中的所有元素并排序
        universe_elements = sorted(list(self.universe))

        for pid in probe_ids:
            # 1. 生成基数奇偶查询
            # 构造查询字符串
            parity_query_str = f"<query_parity>{pid}</query_parity>"
            # 构造解析后的 info 字典
            parity_info = {"query_parity": pid}
            # 获取正确答案（直接调用核心逻辑，避开反事实干扰）
            parity_ans = self._cf_core_produce(parity_info)
            
            queries.append({
                "query": parity_query_str,
                "answer": parity_ans
            })

            # 2. 生成成员查询
            for elem in universe_elements:
                # 构造查询内容：ProbeID,Element
                member_content = f"{pid},{elem}"
                # 构造查询字符串
                member_query_str = f"<query_member>{member_content}</query_member>"
                # 构造解析后的 info 字典
                member_info = {"query_member": member_content}
                # 获取正确答案
                member_ans = self._cf_core_produce(member_info)
                
                queries.append({
                    "query": member_query_str,
                    "answer": member_ans
                })
                
        return queries