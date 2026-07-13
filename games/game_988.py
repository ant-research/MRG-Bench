# -*- coding: utf-8 -*-
from .base import Game
import math

class TrafficEdgeWeightIdentificationGame(Game):
    reasoning_type = "溯因推理"
    data_structure = "图"

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通路网阻抗识别系统”。
本系统设定了一个区域内的城际高速公路网，包含6个交通枢纽节点及其基准流量编码：
- A=1, B=2, C=4, D=3, E=6, F=5

路网中已开通以下可查询的高速通道（14条）：
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

特别注意：规划中的高速通道 D-F 是目标路段，暂不开放探测查询，但你需要在最终评估中给出其预估通行费。

系统已秘密匹配了一种基于节点流量编码的动态计费模式函数，从以下四种中选取：
1. Alpha模式：通行费 = 两枢纽基准流量编码差的绝对值
2. Beta模式：通行费 = 两枢纽基准流量编码之和对10取模
3. Gamma模式：通行费 = 两枢纽基准流量编码的最大公约数
4. Delta模式：通行费 = 两枢纽基准流量编码的按位异或值

你的目标是通过查询现有路段的通行费来推断真实的计费模式，并计算目标通道 D-F 的预估通行费。

## 可进行的操作

1. **通行费查询**：查询某条已开通路段的通行费数值
   格式：<query>X-Y</query>
   例如：<query>A-B</query>
   系统会回复该路段的通行费。若路段未开通或格式错误，会返回错误提示。

2. **模式推断声明**（可选）：在探测过程中记录当前推测的计费模式
   格式：<declare>模式名</declare>
   例如：<declare>Alpha</declare>
   这仅作为系统日志记录，不影响分析进程，也不会得到对错反馈。

3. **最终作答**：提交最终分析报告，包含计费模式名称和目标通道 D-F 的预估通行费
   格式：<answer>pattern=模式名, weight=数值</answer>
   例如：<answer>pattern=Alpha, weight=2</answer>

## 约束条件

- 最多可进行{max_queries}次路段探测查询
- 不可直接查询目标通道 D-F
- 必须同时正确识别计费模式和计算出 D-F 的通行费才能完成任务

## 胜利与失败

- 胜利：在探测次数限制内，最终提交的模式和 D-F 通行费预估值均正确
- 失败：超过查询次数上限；最终作答错误；查询格式错误或试图越权探测 D-F

请开始你的第一次探测或作答。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Impedance Identification System".

The system defines an intercity highway network with 6 major traffic hubs and their baseline traffic encodings:
- A=1, B=2, C=4, D=3, E=6, F=5

The network currently has the following queryable active highway corridors (14 in total):
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

Important: The planned corridor D-F is the target route. It cannot be probed directly, but you must provide its estimated toll index (referred to as "toll") in your final report.

The system has secretly selected a dynamic toll calculation pattern from the following four options:
1. Alpha: toll = absolute difference of hub encodings
2. Beta: toll = sum of hub encodings modulo 10
3. Gamma: toll = greatest common divisor of hub encodings
4. Delta: toll = bitwise XOR of hub encodings

Your goal is to infer the true pattern function by probing the tolls of active corridors, and calculate the toll for the target corridor D-F.

## Available Operations

1. **Toll Query**: Query the toll of an active corridor
   Format: <query>X-Y</query>
   Example: <query>A-B</query>
   The system will respond with the toll. If the corridor is inactive or the format is invalid, an error message will be returned.

2. **Pattern Declaration** (optional): Declare your current inference of the pattern during probes
   Format: <declare>PatternName</declare>
   Example: <declare>Alpha</declare>
   This is only for system logging and does not affect the analysis or provide feedback.

3. **Final Answer**: Submit your final analysis report, including the pattern name and the estimated toll of corridor D-F
   Format: <answer>pattern=PatternName, weight=Value</answer>
   Example: <answer>pattern=Alpha, weight=2</answer>

## Constraints

- Maximum of {max_queries} corridor probes allowed
- Target corridor D-F cannot be queried directly
- Both the pattern and D-F toll must be correct to complete the task

## Victory and Failure

- Victory: Within query limit, both pattern and D-F toll in final answer are correct
- Failure: Exceeding query limit; incorrect final answer; invalid query format or attempting to probe D-F

Please start your first probe or answer.
"""


    contextualized_rule_zh_2 = """\
欢迎使用“脑神经元通路阻抗分析系统”。
系统映射了一个局部神经网络，包含6个关键皮层节点及其固定的神经元活跃度编码：
- A=1, B=2, C=4, D=3, E=6, F=5

神经网中已确认存在以下可探测的突触通路（14条）：
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

特别注意：病变阻断的通路 D-F 是目标靶点，无法直接探测，但你需要在最终诊断中给出该通路的能量损耗指数（即“通行费”）。

系统后台已通过临床数据匹配了一种神经信号衰减模式函数，从以下四种中选取：
1. Alpha模式：通行费 = 两节点活跃度编码差的绝对值
2. Beta模式：通行费 = 两节点活跃度编码之和对10取模
3. Gamma模式：通行费 = 两节点活跃度编码的最大公约数
4. Delta模式：通行费 = 两节点活跃度编码的按位异或值

你的目标是通过查询已知突触通路的能量损耗（通行费）来推断真实的衰减模式，并计算目标通路 D-F 的通行费。

## 可进行的操作

1. **通行费查询**：查询某条已知通路的衰减能量损耗值
   格式：<query>X-Y</query>
   例如：<query>A-B</query>
   系统会回复该通路的通行费。若通路不存在或格式错误，会返回错误提示。

2. **模式推断声明**（可选）：在分析过程中声明当前推断的衰减模式
   格式：<declare>模式名</declare>
   例如：<declare>Alpha</declare>
   这仅作为诊断记录，不影响分析进程，也不会得到对错反馈。

3. **最终作答**：提交最终诊断报告，包含模式名称和目标通路 D-F 的通行费预估值
   格式：<answer>pattern=模式名, weight=数值</answer>
   例如：<answer>pattern=Alpha, weight=2</answer>

## 约束条件

- 最多可进行{max_queries}次通路探测查询
- 不可查询目标通路 D-F
- 必须同时正确识别衰减模式和计算出 D-F 的通行费才能完成诊断

## 胜利与失败

- 胜利：在探测次数限制内，最终作答的模式和 D-F 通行费值均正确
- 失败：超过查询次数上限；最终作答错误；查询格式错误或试图越权探测 D-F

请开始你的第一次探测或作答。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Neural Pathway Impedance Analysis System".

The system maps a localized neural network, containing 6 key cortical nodes with their fixed neural activity encodings:
- A=1, B=2, C=4, D=3, E=6, F=5

The neural network currently has the following queryable active synaptic pathways (14 in total):
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

Important: The pathologically blocked pathway D-F is the target focal point. It cannot be probed directly, but you must provide its estimated energy depletion index (referred to as "toll") in your final diagnostic report.

The system backend has secretly matched a neural signal attenuation pattern function based on clinical data from the following four options:
1. Alpha: toll = absolute difference of node encodings
2. Beta: toll = sum of node encodings modulo 10
3. Gamma: toll = greatest common divisor of node encodings
4. Delta: toll = bitwise XOR of node encodings

Your goal is to infer the true attenuation pattern by probing the energy depletion (toll) of known pathways, and calculate the toll for the target pathway D-F.

## Available Operations

1. **Toll Query**: Query the energy depletion index (toll) of an active pathway
   Format: <query>X-Y</query>
   Example: <query>A-B</query>
   The system will respond with the toll. If the pathway does not exist or the format is invalid, an error message will be returned.

2. **Pattern Declaration** (optional): Declare your current inference of the attenuation pattern
   Format: <declare>PatternName</declare>
   Example: <declare>Alpha</declare>
   This is only for diagnostic records and does not affect the analysis or provide feedback.

3. **Final Answer**: Submit your final diagnostic report, including the pattern name and the estimated toll of target pathway D-F
   Format: <answer>pattern=PatternName, weight=Value</answer>
   Example: <answer>pattern=Alpha, weight=2</answer>

## Constraints

- Maximum of {max_queries} pathway probes allowed
- Target pathway D-F cannot be queried directly
- Both the pattern and D-F toll must be correct to complete the diagnosis

## Victory and Failure

- Victory: Within query limit, both pattern and D-F toll in final answer are correct
- Failure: Exceeding query limit; incorrect final answer; invalid query format or attempting to probe D-F

Please start your first probe or answer.
"""

    contextualized_rule_zh_3 = """\
欢迎进入“学科认知跨度测评系统”。
系统构建了一个核心学科的知识图谱，包含6个基准知识点及其难度层级编码：
- A=1, B=2, C=4, D=3, E=6, F=5

图谱中已建立以下可测评的知识点关联路径（14条）：
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

特别注意：跨学科衍生路径 D-F 是目标评估对象，暂无实证数据供查询，但你需要在最终测评报告中给出其认知负荷成本（即“通行费”）。

系统基于教育心理学选取了一种认知负荷计算模式，该模式从以下四种中选取：
1. Alpha模式：通行费 = 两知识点编码差的绝对值
2. Beta模式：通行费 = 两知识点编码之和对10取模
3. Gamma模式：通行费 = 两知识点编码的最大公约数
4. Delta模式：通行费 = 两知识点编码的按位异或值

你的目标是通过查询已有路径的认知负荷（通行费）来推断真实的计算模式，并推算出衍生路径 D-F 的通行费。

## 可进行的操作

1. **通行费查询**：查询某条已知路径的认知负荷值
   格式：<query>X-Y</query>
   例如：<query>A-B</query>
   系统会回复该路径的通行费。若路径不存在或格式错误，会返回错误提示。

2. **模式推断声明**（可选）：在测评过程中声明当前推断的计算模式
   格式：<declare>模式名</declare>
   例如：<declare>Alpha</declare>
   这仅作为测评日志，不影响测评进程，也不会得到对错反馈。

3. **最终作答**：提交最终测评报告，包含模式名称和目标路径 D-F 的通行费
   格式：<answer>pattern=模式名, weight=数值</answer>
   例如：<answer>pattern=Alpha, weight=2</answer>

## 约束条件

- 最多可进行{max_queries}次路径测评查询
- 不可直接测评目标路径 D-F
- 必须同时正确识别计算模式和推算出 D-F 的通行费才能完成任务

## 胜利与失败

- 胜利：在测评次数限制内，最终作答的模式和 D-F 通行费均正确
- 失败：超过测评次数上限；最终作答错误；查询格式错误或试图越权测评 D-F

请开始你的第一次测评或作答。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Disciplinary Cognitive Span Assessment System".

The system constructs a knowledge graph of a core discipline, containing 6 foundational knowledge points and their difficulty level encodings:
- A=1, B=2, C=4, D=3, E=6, F=5

The graph has established the following queryable prerequisite paths (14 in total):
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

Important: The cross-disciplinary derivative path D-F is the target assessment object. It cannot be probed, but you must provide its estimated cognitive load cost (referred to as "toll") in your final report.

The system has selected a cognitive load calculation pattern based on educational psychology from the following four options:
1. Alpha: toll = absolute difference of knowledge point encodings
2. Beta: toll = sum of knowledge point encodings modulo 10
3. Gamma: toll = greatest common divisor of knowledge point encodings
4. Delta: toll = bitwise XOR of knowledge point encodings

Your goal is to infer the true calculation pattern by querying the cognitive load (toll) of existing paths, and calculate the toll for the target path D-F.

## Available Operations

1. **Toll Query**: Query the cognitive load cost (toll) of an established path
   Format: <query>X-Y</query>
   Example: <query>A-B</query>
   The system will respond with the toll. If the path does not exist or the format is invalid, an error message will be returned.

2. **Pattern Declaration** (optional): Declare your current inference of the calculation pattern
   Format: <declare>PatternName</declare>
   Example: <declare>Alpha</declare>
   This is only for system logging and does not affect the assessment or provide feedback.

3. **Final Answer**: Submit your final assessment report, including the pattern name and the estimated toll of target path D-F
   Format: <answer>pattern=PatternName, weight=Value</answer>
   Example: <answer>pattern=Alpha, weight=2</answer>

## Constraints

- Maximum of {max_queries} path queries allowed
- Target path D-F cannot be queried directly
- Both the pattern and D-F toll must be correct to complete the assessment

## Victory and Failure

- Victory: Within query limit, both pattern and D-F toll in final answer are correct
- Failure: Exceeding query limit; incorrect final answer; invalid query format or attempting to query D-F

Please start your first query or answer.
"""

    contextualized_rule_zh_4 = """\
欢迎登录“柔性产线物流耗散评估系统”。
本系统监控着一个自动化车间，包含6个关键工作站及其设备能耗基准编码：
- A=1, B=2, C=4, D=3, E=6, F=5

车间内已部署了以下可监测的物料传输带（14条）：
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

特别注意：计划增设的传输带 D-F 是目标改造链路，无法进行实测查询，但你需要在最终规划中给出其预估的物流耗散指数（即“通行费”）。

系统已根据产线特点激活了一种耗散散算模式函数，从以下四种中选取：
1. Alpha模式：通行费 = 两工作站编码差的绝对值
2. Beta模式：通行费 = 两工作站编码之和对10取模
3. Gamma模式：通行费 = 两工作站编码的最大公约数
4. Delta模式：通行费 = 两工作站编码的按位异或值

你的目标是通过查询现有传输带的耗散指数（通行费）来推断真实的散算模式，并计算目标链路 D-F 的预估通行费。

## 可进行的操作

1. **通行费查询**：查询某条已知传输带的物流耗散指数
   格式：<query>X-Y</query>
   例如：<query>A-B</query>
   系统会回复该传输带的通行费。若传输带不存在或格式错误，会返回错误提示。

2. **模式推断声明**（可选）：在评估过程中记录当前推测的散算模式
   格式：<declare>模式名</declare>
   例如：<declare>Alpha</declare>
   这仅作为后台记录，不影响评估进程，也不会得到对错反馈。

3. **最终作答**：提交最终规划报告，包含耗散散算模式名称和目标链路 D-F 的通行费
   格式：<answer>pattern=模式名, weight=数值</answer>
   例如：<answer>pattern=Alpha, weight=2</answer>

## 约束条件

- 最多可进行{max_queries}次链路监测查询
- 不可直接监测目标链路 D-F
- 必须同时正确识别散算模式和计算出 D-F 的通行费才能完成评估

## 胜利与失败

- 胜利：在监测次数限制内，最终提交的模式和 D-F 通行费预估值均正确
- 失败：超过监测次数上限；最终作答错误；查询格式错误或试图越权监测 D-F

请开始你的第一次监测或作答。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Flexible Production Line Logistics Dissipation Evaluation System".

The system monitors an automated workshop, containing 6 critical workstations and their energy baseline encodings:
- A=1, B=2, C=4, D=3, E=6, F=5

The workshop has deployed the following queryable material conveyor belts (14 in total):
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

Important: The planned conveyor belt D-F is the target modification link. It cannot be probed directly, but you must provide its estimated logistics dissipation index (referred to as "toll") in your final planning report.

The system has activated a dissipation calculation pattern based on production line characteristics from the following four options:
1. Alpha: toll = absolute difference of workstation encodings
2. Beta: toll = sum of workstation encodings modulo 10
3. Gamma: toll = greatest common divisor of workstation encodings
4. Delta: toll = bitwise XOR of workstation encodings

Your goal is to infer the true calculation pattern by querying the dissipation indices (tolls) of existing belts, and calculate the toll for the target link D-F.

## Available Operations

1. **Toll Query**: Query the logistics dissipation index (toll) of an active conveyor belt
   Format: <query>X-Y</query>
   Example: <query>A-B</query>
   The system will respond with the toll. If the belt does not exist or the format is invalid, an error message will be returned.

2. **Pattern Declaration** (optional): Declare your current inference of the calculation pattern
   Format: <declare>PatternName</declare>
   Example: <declare>Alpha</declare>
   This is only for system logging and does not affect the evaluation or provide feedback.

3. **Final Answer**: Submit your final planning report, including the pattern name and the estimated toll of target link D-F
   Format: <answer>pattern=PatternName, weight=Value</answer>
   Example: <answer>pattern=Alpha, weight=2</answer>

## Constraints

- Maximum of {max_queries} link monitoring queries allowed
- Target link D-F cannot be queried directly
- Both the pattern and D-F toll must be correct to complete the evaluation

## Victory and Failure

- Victory: Within query limit, both pattern and D-F toll in final answer are correct
- Failure: Exceeding query limit; incorrect final answer; invalid query format or attempting to monitor D-F

Please start your first query or answer.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法证据链冲突强度研判系统”。
系统提取了一起复杂诉讼案中的6个核心证据节点，并赋予其法理效力级别编码：
- A=1, B=2, C=4, D=3, E=6, F=5

案卷中存在以下已被交叉质证的关联逻辑线（14条）：
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

特别注意：控辩双方争议的焦点逻辑线 D-F 是目标判断线，目前无法直接提取裁判指标，但你需要在最终结案报告中给出其冲突指数（即“通行费”）。

本研判系统已设定了一种法理逻辑演算模式，从以下四种中选取：
1. Alpha模式：通行费 = 两证据节点效力编码差的绝对值
2. Beta模式：通行费 = 两证据节点效力编码之和对10取模
3. Gamma模式：通行费 = 两证据节点效力编码的最大公约数
4. Delta模式：通行费 = 两证据节点效力编码的按位异或值

你的目标是通过调阅已知逻辑线的冲突指数（通行费）来推断真实的演算模式，并推断争议逻辑线 D-F 的通行费。

## 可进行的操作

1. **通行费调阅**：调阅某条已质证逻辑线的冲突指数
   格式：<query>X-Y</query>
   例如：<query>A-B</query>
   系统会回复该逻辑线的通行费。若逻辑线未入卷或格式错误，会返回错误提示。

2. **模式推断声明**（可选）：在研判过程中声明当前推断的演算模式
   格式：<declare>模式名</declare>
   例如：<declare>Alpha</declare>
   这仅作为研判笔录，不影响调查进程，也不会得到对错反馈。

3. **最终作答**：提交最终结案报告，包含演算模式名称和目标逻辑线 D-F 的通行费
   格式：<answer>pattern=模式名, weight=数值</answer>
   例如：<answer>pattern=Alpha, weight=2</answer>

## 约束条件

- 最多可进行{max_queries}次逻辑线调阅操作
- 不可直接调阅争议逻辑线 D-F
- 必须同时正确识别演算模式和计算出 D-F 的通行费才能出具报告

## 胜利与失败

- 胜利：在调阅次数限制内，最终作答的模式和 D-F 通行费值均正确
- 失败：超过调阅次数上限；最终作答错误；调阅格式错误或试图越权查看 D-F

请开始你的第一次调阅或作答。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Evidence Chain Conflict Intensity Judgment System".

The system has extracted 6 core evidence nodes from a complex litigation case, assigning them legal validity encodings:
- A=1, B=2, C=4, D=3, E=6, F=5

The case files contain the following cross-examined logical links that can be queried (14 in total):
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

Important: The disputed focal logical link D-F is the target judgment line. It cannot be queried directly, but you must provide its estimated conflict index (referred to as "toll") in your final closing report.

The system has applied a jurisprudential logic calculation pattern selected from the following four options:
1. Alpha: toll = absolute difference of evidence node encodings
2. Beta: toll = sum of evidence node encodings modulo 10
3. Gamma: toll = greatest common divisor of evidence node encodings
4. Delta: toll = bitwise XOR of evidence node encodings

Your goal is to infer the true logic pattern by querying the conflict indices (tolls) of known logical links, and deduce the toll for the target link D-F.

## Available Operations

1. **Toll Query**: Query the conflict index (toll) of a cross-examined logical link
   Format: <query>X-Y</query>
   Example: <query>A-B</query>
   The system will respond with the toll. If the link is not in the file or the format is invalid, an error message will be returned.

2. **Pattern Declaration** (optional): Declare your current inference of the calculation pattern
   Format: <declare>PatternName</declare>
   Example: <declare>Alpha</declare>
   This is only for investigation transcripts and does not affect the process or provide feedback.

3. **Final Answer**: Submit your final closing report, including the pattern name and the estimated toll of target link D-F
   Format: <answer>pattern=PatternName, weight=Value</answer>
   Example: <answer>pattern=Alpha, weight=2</answer>

## Constraints

- Maximum of {max_queries} link query operations allowed
- Target link D-F cannot be queried directly
- Both the pattern and D-F toll must be correct to issue the report

## Victory and Failure

- Victory: Within query limit, both pattern and D-F toll in final answer are correct
- Failure: Exceeding query limit; incorrect final answer; invalid query format or attempting to access D-F

Please start your first query or answer.
"""



    game_rule_zh = """\
我们来玩一个"边权识别与计算"的推理游戏，规则如下：

游戏设定了一个无向图，包含6个节点及其固定编码：
- A=1, B=2, C=4, D=3, E=6, F=5

图中有以下可查询的边（14条）：
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

特别注意：边 D-F 是目标边，不可查询，但需要在最终答案中给出其边权值。

我已秘密选定了一个模式函数来计算所有边的权重，该模式从以下四种中选取：
1. Alpha：权重 = 节点编码差的绝对值
2. Beta：权重 = 两节点编码之和对10取模
3. Gamma：权重 = 两节点编码的最大公约数
4. Delta：权重 = 两节点编码的按位异或值

你的目标是通过查询可查询边的权重来推断真实的模式函数，并计算目标边 D-F 的权重值。

## 可进行的操作

1. **通行费查询**：查询某条可查询边的权重值
   格式：<query>X-Y</query>
   例如：<query>A-B</query>
   我会回复该边的权重值。若边不在可查询集合中或格式错误，会返回错误提示。

2. **模式推断声明**（可选）：在查询过程中声明当前推断的模式
   格式：<declare>模式名</declare>
   例如：<declare>Alpha</declare>
   这仅作为记录，不影响游戏进程，也不会得到对错反馈。

3. **最终作答**：提交最终答案，包含模式名称和目标边 D-F 的权重值
   格式：<answer>pattern=模式名, weight=数值</answer>
   例如：<answer>pattern=Alpha, weight=2</answer>

## 约束条件

- 最多可进行{max_queries}次通行费查询
- 不可查询目标边 D-F
- 必须同时正确识别模式和计算出 D-F 的权重才能获胜

## 胜利与失败

- 胜利：在查询次数限制内，最终作答的模式和 D-F 权重值均正确
- 失败：超过查询次数上限；最终作答错误；查询格式错误或试图查询 D-F

请开始你的第一次查询或作答。
"""

    game_rule_en = """\
Let's play an "Edge Weight Identification and Calculation" deduction game with the following rules:

The game defines an undirected graph with 6 nodes and their fixed encodings:
- A=1, B=2, C=4, D=3, E=6, F=5

The graph has the following queryable edges (14 in total):
A-B, A-C, A-D, A-E, A-F, B-C, B-D, B-E, B-F, C-D, C-E, C-F, D-E, E-F

Important: Edge D-F is the target edge. It cannot be queried, but you must provide its weight in your final answer.

I have secretly selected a pattern function to calculate all edge weights from the following four options:
1. Alpha: weight = absolute difference of node encodings
2. Beta: weight = sum of node encodings modulo 10
3. Gamma: weight = greatest common divisor of node encodings
4. Delta: weight = bitwise XOR of node encodings

Your goal is to infer the true pattern function by querying the weights of queryable edges, and then calculate the weight of the target edge D-F.

## Available Operations

1. **Toll Query**: Query the weight of a queryable edge
   Format: <query>X-Y</query>
   Example: <query>A-B</query>
   I will respond with the weight of that edge. If the edge is not in the queryable set or the format is invalid, an error message will be returned.

2. **Pattern Declaration** (optional): Declare your current inference of the pattern during queries
   Format: <declare>PatternName</declare>
   Example: <declare>Alpha</declare>
   This is only for record keeping and does not affect the game or provide correctness feedback.

3. **Final Answer**: Submit your final answer, including the pattern name and the weight of target edge D-F
   Format: <answer>pattern=PatternName, weight=Value</answer>
   Example: <answer>pattern=Alpha, weight=2</answer>

## Constraints

- Maximum of {max_queries} toll queries allowed
- Target edge D-F cannot be queried
- Both the pattern and D-F weight must be correct to win

## Victory and Failure

- Victory: Within query limit, both pattern and D-F weight in final answer are correct
- Failure: Exceeding query limit; incorrect final answer; invalid query format or attempting to query D-F

You may now start your first query or answer.
"""


    user_prompt_zh = "请开始你的第一次查询或作答。"
    user_prompt_en = "Please start your first query or answer."

    tags = ["answer", "query", "declare"]

    NODE_CODES = {
        "A": 1, "B": 2, "C": 4, "D": 3, "E": 6, "F": 5
    }

    QUERYABLE_EDGES = {
        "A-B", "A-C", "A-D", "A-E", "A-F",
        "B-C", "B-D", "B-E", "B-F",
        "C-D", "C-E", "C-F",
        "D-E", "E-F"
    }

    TARGET_EDGE = "D-F"

    @staticmethod
    def pattern_alpha(u, v):
        """权重 = 节点编码差的绝对值"""
        return abs(u - v)

    @staticmethod
    def pattern_beta(u, v):
        """权重 = 两节点编码之和对10取模"""
        return (u + v) % 10

    @staticmethod
    def pattern_gamma(u, v):
        """权重 = 两节点编码的最大公约数"""
        return math.gcd(u, v)

    @staticmethod
    def pattern_delta(u, v):
        """权重 = 两节点编码的按位异或值"""
        return u ^ v

    PATTERNS = {
        "Alpha": pattern_alpha.__func__,
        "Beta": pattern_beta.__func__,
        "Gamma": pattern_gamma.__func__,
        "Delta": pattern_delta.__func__
    }

    DIFFICULTY_CONFIG = {
        1: {"max_queries": 6, "pattern": "Alpha"},
        2: {"max_queries": 5, "pattern": "Beta"},
        3: {"max_queries": 4, "pattern": "Gamma"},
        4: {"max_queries": 4, "pattern": "Delta"},
        5: {"max_queries": 3, "pattern": "Beta"},
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态"""
        diff = int(self.config.difficulty)
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.max_queries = cfg["max_queries"]
        self.true_pattern = cfg["pattern"]
        
        # 获取模式函数
        self.pattern_func = self.PATTERNS[self.true_pattern]
        
        # 计算目标边D-F的权重（ground truth）
        d_code = self.NODE_CODES["D"]
        f_code = self.NODE_CODES["F"]
        self.target_weight = self.pattern_func(d_code, f_code)
        
        # 查询计数器
        self.query_count = 0
        
        # 用于格式化规则
        self._game_info["max_queries"] = self.max_queries

    def _parse_edge(self, edge_str):
        """解析边字符串，返回规范化的边名称和两个节点编码"""
        edge_str = edge_str.strip().upper()
        
        if "-" not in edge_str:
            return None, None, None
            
        parts = edge_str.split("-")
        if len(parts) != 2:
            return None, None, None
            
        node1, node2 = parts[0].strip(), parts[1].strip()
        
        if node1 not in self.NODE_CODES or node2 not in self.NODE_CODES:
            return None, None, None
        
        normalized = f"{min(node1, node2)}-{max(node1, node2)}"
        
        return normalized, self.NODE_CODES[node1], self.NODE_CODES[node2]

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip().lower()] = v.strip()
        
        if "pattern" not in ans_dict or "weight" not in ans_dict:
            return False
        
        model_pattern = ans_dict["pattern"]
        if model_pattern.lower() != self.true_pattern.lower():
            return False
        
        try:
            model_weight = int(ans_dict["weight"])
        except ValueError:
            return False
            
        return model_weight == self.target_weight

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑：根据查询产生响应"""
        is_zh = self.config.language == "zh"
        
        if "query" in parsed_info:
            edge_query = parsed_info["query"]
            
            normalized_edge, code1, code2 = self._parse_edge(edge_query)
            
            if normalized_edge is None:
                return "错误：边格式无效。" if is_zh else "Error: Invalid edge format."
            
            if normalized_edge == self.TARGET_EDGE:
                return "错误：目标边 D-F 不可查询。" if is_zh else "Error: Target edge D-F cannot be queried."
            
            if normalized_edge not in self.QUERYABLE_EDGES:
                return "错误：此边不在可查询集合中。" if is_zh else "Error: This edge is not in the queryable set."
            
            if self.query_count >= self.max_queries:
                self.state.set_state("failed", "exceeded query limit")
                return f"失败：超过查询次数上限（{self.max_queries}次）。" if is_zh else f"Failure: Exceeded query limit ({self.max_queries} queries)."
            
            weight = self.pattern_func(code1, code2)
            self.query_count += 1
            
            remaining = self.max_queries - self.query_count
            if is_zh:
                return f"通行费={weight}（剩余查询次数：{remaining}）"
            else:
                return f"Toll={weight} (Remaining queries: {remaining})"
        
        elif "declare" in parsed_info:
            declared_pattern = parsed_info["declare"].strip()
            if is_zh:
                return f"已记录你的推断：{declared_pattern}（这不影响游戏进程）"
            else:
                return f"Recorded your inference: {declared_pattern} (This does not affect the game)"
        
        else:
            raise ValueError("No valid query or declare tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        possible_queries = []
        is_zh = self.config.language == "zh"
        
        sorted_edges = sorted(list(self.QUERYABLE_EDGES))
        
        for edge_str in sorted_edges:
            _, code1, code2 = self._parse_edge(edge_str)
            weight = self.pattern_func(code1, code2)
            
            remaining = self.max_queries - (len(possible_queries) + 1)
            if remaining < 0:
                remaining = 0
            
            if is_zh:
                ans = f"通行费={weight}（剩余查询次数：{remaining}）"
            else:
                ans = f"Toll={weight} (Remaining queries: {remaining})"
                
            possible_queries.append({
                "query": f"<query>{edge_str}</query>",
                "answer": ans
            })
            
        return possible_queries

    def step(self, response: str):
        """处理一轮交互"""
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                is_zh = self.config.language == "zh"
                
                if is_success:
                    res = f"胜利！正确答案：模式={self.true_pattern}，D-F通行费={self.target_weight}" if is_zh else f"Victory! Correct answer: pattern={self.true_pattern}, D-F weight={self.target_weight}"
                    self.state.set_state("success", "correct answer")
                    self.state.add_message("user", res)
                else:
                    res = f"失败！正确答案：模式={self.true_pattern}，D-F通行费={self.target_weight}" if is_zh else f"Failure! Correct answer: pattern={self.true_pattern}, D-F weight={self.target_weight}"
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state

    def _cf_make_wrong(self, correct: str) -> str:
        """将正确的查询响应中的通行费数值篡改为错误值"""
        import re as _re
        is_zh = self.config.language == "zh"

        # 处理中文格式：通行费=3（剩余查询次数：5）
        if is_zh:
            m = _re.match(r'^通行费=(\d+)', correct)
            if m:
                orig = int(m.group(1))
                wrong_val = orig + 1
                return correct.replace(f"通行费={orig}", f"通行费={wrong_val}", 1)
        # 处理英文格式：Toll=3 (Remaining queries: 5)
        else:
            m = _re.match(r'^Toll=(\d+)', correct)
            if m:
                orig = int(m.group(1))
                wrong_val = orig + 1
                return correct.replace(f"Toll={orig}", f"Toll={wrong_val}", 1)

        # declare 响应和错误提示原样返回
        return correct + "_WRONG"