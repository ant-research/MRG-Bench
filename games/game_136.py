# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   首尾元素：序列的第一个或最后一个元素是什么
# ============================================================

from .base import Game
import random


class SequencePermutationGame(Game):

    game_rule_zh = """\
我们来玩一个"序列置换推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列 S[1..{n}]，其中每个元素来自四个字母 {{A, B, C, D}} 之一。存在一个隐藏的置换映射 F，它将四个字母一一对应地映射到四个字母（例如 A→B, B→C, C→D, D→A），并且序列满足：对于所有相邻位置 i 和 i+1，都有 S[i+1] = F(S[i])。

你的目标是通过有限次查询，推断出 S[1]（序列首元素）或 S[N]（序列尾元素）的值。

你可以使用以下两种查询方式，每次查询消耗一次查询预算：

1. 取值查询：询问序列中某个位置的具体值（注意：只能查询位置 2 到 {n_minus_1} 之间的元素，不能直接查询首尾）
2. 相等性查询：询问两个位置的元素是否相等（同样限制在位置 2 到 {n_minus_1} 之间）

当你收集到足够信息后，可以提交最终答案。你需要猜测 S[1] 或 S[N] 的值（或两者都猜）。

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个查询或提交答案。请使用以下 XML 格式：

- 取值查询（例如查询位置 5 的值）：
<query_reveal>5</query_reveal>

- 相等性查询（例如查询位置 3 和位置 7 是否相等）：
<query_equal>3,7</query_equal>

- 提交答案（猜测首元素或尾元素，或两者都猜）：
<answer>head=A</answer>
或
<answer>tail=D</answer>
或
<answer>head=A, tail=D</answer>

注意：
- 位置编号必须在 2 到 {n_minus_1} 之间
- 答案中的字母必须是 A、B、C、D 之一
- 请尽可能用最少的查询次数完成推理
"""

    game_rule_en = """\
Let's play a "Sequence Permutation Inference" game. Here are the rules:

There is an ordered sequence S[1..{n}] of length {n}, where each element is one of four letters {{A, B, C, D}}. There exists a hidden permutation mapping F that bijectively maps the four letters to the four letters (e.g., A→B, B→C, C→D, D→A), and the sequence satisfies: for all adjacent positions i and i+1, S[i+1] = F(S[i]).

Your goal is to infer the value of S[1] (the first element) or S[N] (the last element) through a limited number of queries.

You can use the following two types of queries, each consuming one query budget:

1. Reveal Query: Ask for the specific value at a certain position (Note: you can only query positions from 2 to {n_minus_1}, not the first or last positions directly)
2. Equality Query: Ask whether two positions have the same element (also restricted to positions from 2 to {n_minus_1})

When you have collected enough information, you can submit your final answer. You need to guess the value of S[1] or S[N] (or both).

## Query and Answer Format (strictly required)

Each turn must contain only one query or answer submission. Use the following XML format:

- Reveal Query (e.g., querying position 5):
<query_reveal>5</query_reveal>

- Equality Query (e.g., querying whether positions 3 and 7 are equal):
<query_equal>3,7</query_equal>

- Submit Answer (guess the first element or last element, or both):
<answer>head=A</answer>
or
<answer>tail=D</answer>
or
<answer>head=A, tail=D</answer>

Notes:
- Position indices must be between 2 and {n_minus_1}
- Letters in the answer must be one of A, B, C, or D
- Try to complete the inference with as few queries as possible
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
我们来模拟一个"城市干线绿波带信号推理"场景。

在一个城市的主干道上，存在一个包含 {n} 个连续路口的信号协调序列 S[1..{n}]。每个路口的当前信号相位方案属于四种预设模式 {{A, B, C, D}} 之一。该干线的信号控制系统设置了一个隐藏的相位转移函数 F，它将四种模式一一对应地映射（例如 A→B, B→C, C→D, D→A），并且满足：对于所有相邻路口 i 和 i+1，都满足 S[i+1] = F(S[i])。

你的目标是通过有限次远程探测，推断出路口 1（起点 S[1]）或路口 N（终点 S[N]）的信号相位模式。

你可以使用以下两种探测指令，每次消耗一次查询预算：

1. 定点查询：读取某个路口的当前相位模式（注意：由于权限限制，只能查询路口 2 到 {n_minus_1} 之间的节点，不能直接查询首尾路口）
2. 一致性核对：验证两个路口当前的相位模式是否完全相同（同样限制在路口 2 到 {n_minus_1} 之间）

当你收集到足够信息后，可以提交最终的推断报告。你需要确定 S[1] 或 S[N] 的模式（或两者都确定）。

## 探测与报告提交格式（必须严格遵守）

每次只能进行一个查询或提交报告。请使用以下 XML 格式：

- 定点查询（例如查询路口 5 的模式）：
<query_reveal>5</query_reveal>

- 一致性核对（例如查询路口 3 和路口 7 是否模式相同）：
<query_equal>3,7</query_equal>

- 提交报告（推断起点或终点模式，或两者都推断）：
<answer>head=A</answer>
或
<answer>tail=D</answer>
或
<answer>head=A, tail=D</answer>

注意：
- 路口编号必须在 2 到 {n_minus_1} 之间
- 答案中的模式字母必须是 A、B、C、D 之一
- 请尽可能用最少的探测次数完成推理
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's simulate an "Arterial Green Wave Signal Inference" scenario.

Along a major city arterial, there is an ordered sequence of {n} consecutive intersections S[1..{n}]. The current signal phase plan at each intersection is one of four preset modes {{A, B, C, D}}. The signal coordination system employs a hidden phase transition function F that bijectively maps the four modes (e.g., A→B, B→C, C→D, D→A), satisfying the condition: for all adjacent intersections i and i+1, S[i+1] = F(S[i]).

Your objective is to deduce the signal phase mode at intersection 1 (the origin S[1]) or intersection N (the terminus S[N]) through a limited number of remote probes.

You can use the following two types of probe commands, each consuming one query budget:

1. Reveal Query: Read the current phase mode of a specific intersection (Note: due to access restrictions, you can only probe intersections from 2 to {n_minus_1}, not the first or last ones directly).
2. Equality Query: Verify whether two intersections currently operate on the exact same phase mode (also restricted to intersections from 2 to {n_minus_1}).

Once sufficient telemetry is gathered, you can submit your final inference report. You need to determine the mode for S[1] or S[N] (or both).

## Probe and Report Format (strictly required)

Each turn must contain only one probe or report submission. Use the following XML format:

- Reveal Query (e.g., probing intersection 5):
<query_reveal>5</query_reveal>

- Equality Query (e.g., checking if intersections 3 and 7 share the same mode):
<query_equal>3,7</query_equal>

- Submit Report (deduce the origin or terminus mode, or both):
<answer>head=A</answer>
or
<answer>tail=D</answer>
or
<answer>head=A, tail=D</answer>

Notes:
- Intersection indices must be between 2 and {n_minus_1}
- Letters in the answer must be one of A, B, C, or D
- Try to complete the inference with as few probes as possible
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
我们来模拟一个"病毒变异代系推理"场景。

在一次流行病学调查中，研究人员发现了一条包含 {n} 个连续传播代系的病毒突变序列 S[1..{n}]。每一代病毒的表面抗原表型属于四种类型 {{A, B, C, D}} 之一。实验表明，该病毒的突变受一种隐藏的确定性机制 F 控制，它将四种表型一一对应地转化（例如 A→B, B→C, C→D, D→A），且满足：对于所有的相邻传播代系 i 和 i+1，都满足 S[i+1] = F(S[i])。

你的目标是通过有限次基因测序采样，推断出初代（零号病人 S[1]）或末代（最新变种 S[N]）的抗原表型。

你可以使用以下两种检测手段，每次消耗一次测序预算：

1. 表型测序：检测某个特定代系的抗原表型（注意：由于样本缺失，只能检测第 2 到 {n_minus_1} 代之间的样本，不能直接检测首尾）
2. 同源比对：验证两个代系的病毒表型是否完全一致（同样限制在第 2 到 {n_minus_1} 代之间）

当你收集到足够信息后，可以提交最终的流调结论。你需要推断 S[1] 或 S[N] 的表型（或两者都推断）。

## 检测与结论提交格式（必须严格遵守）

每次只能进行一项检测或提交结论。请使用以下 XML 格式：

- 表型测序（例如检测第 5 代的表型）：
<query_reveal>5</query_reveal>

- 同源比对（例如比对第 3 代和第 7 代是否为同种表型）：
<query_equal>3,7</query_equal>

- 提交结论（推测初代或末代病毒表型，或两者都推测）：
<answer>head=A</answer>
或
<answer>tail=D</answer>
或
<answer>head=A, tail=D</answer>

注意：
- 代系编号必须在 2 到 {n_minus_1} 之间
- 答案中的表型字母必须是 A、B、C、D 之一
- 请尽可能用最少的检测次数完成推理
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's simulate a "Viral Mutation Generation Inference" scenario.

During an epidemiological investigation, researchers identified a chain of {n} consecutive transmission generations forming a viral mutation sequence S[1..{n}]. The surface antigen phenotype of each generation falls into one of four types {{A, B, C, D}}. Experiments show that the mutation is governed by a hidden deterministic mechanism F that bijectively transforms the four phenotypes (e.g., A→B, B→C, C→D, D→A), ensuring that for all adjacent generations i and i+1, S[i+1] = F(S[i]).

Your goal is to infer the antigen phenotype of the first generation (patient zero S[1]) or the latest generation S[N] through a limited number of genomic sequencings.

You can use the following two types of diagnostic assays, each consuming one sequencing budget:

1. Phenotype Sequencing: Assay the specific phenotype of a given generation (Note: due to missing samples, you can only test generations from 2 to {n_minus_1}, not the first or last directly).
2. Homology Alignment: Verify whether the viral phenotypes of two generations are completely identical (also restricted to generations from 2 to {n_minus_1}).

Once sufficient epidemiological data is gathered, you can submit your final conclusion. You need to infer the phenotype of S[1] or S[N] (or both).

## Assay and Conclusion Format (strictly required)

Each turn must contain only one assay or conclusion submission. Use the following XML format:

- Phenotype Sequencing (e.g., assaying generation 5):
<query_reveal>5</query_reveal>

- Homology Alignment (e.g., checking if generations 3 and 7 share the same phenotype):
<query_equal>3,7</query_equal>

- Submit Conclusion (infer the phenotype of patient zero or the latest variant, or both):
<answer>head=A</answer>
or
<answer>tail=D</answer>
or
<answer>head=A, tail=D</answer>

Notes:
- Generation indices must be between 2 and {n_minus_1}
- Letters in the answer must be one of A, B, C, or D
- Try to complete the inference with as few assays as possible
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
我们来模拟一个"认知模块递进推理"场景。

在一个自适应学习系统中，存在一条包含 {n} 个连续学习节点的课程知识图谱路径 S[1..{n}]。每个节点所使用的认知训练模块属于四种分类 {{A, B, C, D}} 之一。教学引擎根据一套隐藏的认知递进法则 F 进行模块的自动升阶，该法则将四种模块一一对应地映射（例如 A→B, B→C, C→D, D→A），并且满足：对于所有相邻的学习节点 i 和 i+1，都满足 S[i+1] = F(S[i])。

你的目标是通过有限次诊断测试，推断出该路径起始节点 S[1] 或最终考核节点 S[N] 所使用的模块分类。

你可以使用以下两种诊断方式，每次消耗一次测试预算：

1. 模块探查：查询某个具体学习节点所部署的训练模块（注意：只能探查节点 2 到 {n_minus_1} 之间的模块，不能直接探查起点和终点）
2. 模块比对：验证两个学习节点是否采用了完全相同的训练模块（同样限制在节点 2 到 {n_minus_1} 之间）

当你收集到足够信息后，可以提交最终的教学评估报告。你需要推断 S[1] 或 S[N] 的模块（或两者都推测）。

## 探查与报告提交格式（必须严格遵守）

每次只能进行一次探查或提交报告。请使用以下 XML 格式：

- 模块探查（例如查询节点 5 的模块）：
<query_reveal>5</query_reveal>

- 模块比对（例如查询节点 3 和节点 7 的模块是否相同）：
<query_equal>3,7</query_equal>

- 提交报告（推断起点或终点模块，或两者都推测）：
<answer>head=A</answer>
或
<answer>tail=D</answer>
或
<answer>head=A, tail=D</answer>

注意：
- 节点编号必须在 2 到 {n_minus_1} 之间
- 答案中的模块字母必须是 A、B、C、D 之一
- 请尽可能用最少的测试次数完成推理
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's simulate a "Cognitive Module Progression Inference" scenario.

In an adaptive learning system, there is a curriculum knowledge graph path consisting of {n} consecutive learning nodes S[1..{n}]. The cognitive training module deployed at each node belongs to one of four categories {{A, B, C, D}}. The pedagogical engine automatically upgrades modules based on a hidden cognitive progression rule F that bijectively maps the four categories (e.g., A→B, B→C, C→D, D→A), ensuring that for all adjacent nodes i and i+1, S[i+1] = F(S[i]).

Your goal is to infer the module category of the starting node S[1] or the final assessment node S[N] through a limited number of diagnostic tests.

You can use the following two types of diagnostic queries, each consuming one test budget:

1. Module Probe: Query the specific training module deployed at a given node (Note: you can only probe nodes from 2 to {n_minus_1}, not the origin or terminus directly).
2. Module Comparison: Verify whether two learning nodes utilize the exact same training module (also restricted to nodes from 2 to {n_minus_1}).

Once sufficient assessment data is gathered, you can submit your final pedagogical report. You need to infer the module of S[1] or S[N] (or both).

## Probe and Report Format (strictly required)

Each turn must contain only one probe or report submission. Use the following XML format:

- Module Probe (e.g., probing node 5):
<query_reveal>5</query_reveal>

- Module Comparison (e.g., checking if nodes 3 and 7 use the same module):
<query_equal>3,7</query_equal>

- Submit Report (infer the starting or final module, or both):
<answer>head=A</answer>
or
<answer>tail=D</answer>
or
<answer>head=A, tail=D</answer>

Notes:
- Node indices must be between 2 and {n_minus_1}
- Letters in the answer must be one of A, B, C, or D
- Try to complete the inference with as few tests as possible
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
我们来模拟一个"流水线工位状态推理"场景。

在一条自动化柔性生产线上，排列着 {n} 个连续的机器人装配工位，形成序列 S[1..{n}]。每个工位当前的作业状态代码属于四类标准状态 {{A, B, C, D}} 之一。生产控制系统依据一套隐藏的状态转换协议 F 进行流水线调度，该协议将四种状态一一对应地流转（例如 A→B, B→C, C→D, D→A），且满足：对于所有相邻的工位 i 和 i+1，都满足 S[i+1] = F(S[i])。

你的目标是通过有限次传感器读取，推断出首道工序（工位 S[1]）或末道工序（工位 S[N]）的作业状态代码。

你可以使用以下两种读取指令，每次消耗一次系统调用预算：

1. 状态轮询：读取某个指定工位的具体状态代码（注意：为避免干扰首尾物料进出，只能读取工位 2 到 {n_minus_1} 的状态，不能直接读取首尾）
2. 状态校验：校验两个工位的状态代码是否完全一致（同样限制在工位 2 到 {n_minus_1} 之间）

当你收集到足够信息后，可以提交最终的生产状态诊断书。你需要判断 S[1] 或 S[N] 的状态（或两者都判断）。

## 读取与诊断提交格式（必须严格遵守）

每次只能进行一项读取或提交诊断书。请使用以下 XML 格式：

- 状态轮询（例如读取工位 5 的状态）：
<query_reveal>5</query_reveal>

- 状态校验（例如校验工位 3 和工位 7 的状态是否相同）：
<query_equal>3,7</query_equal>

- 提交诊断书（推断首道或末道工位的状态，或两者都推断）：
<answer>head=A</answer>
或
<answer>tail=D</answer>
或
<answer>head=A, tail=D</answer>

注意：
- 工位编号必须在 2 到 {n_minus_1} 之间
- 答案中的状态字母必须是 A、B、C、D 之一
- 请尽可能用最少的调用次数完成推理
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's simulate an "Assembly Line Workstation State Inference" scenario.

On an automated flexible production line, there is a sequence of {n} consecutive robotic assembly workstations S[1..{n}]. The current operational state code of each workstation is one of four standard states {{A, B, C, D}}. The production control system schedules the line based on a hidden state transition protocol F that bijectively rotates the four states (e.g., A→B, B→C, C→D, D→A), ensuring that for all adjacent workstations i and i+1, S[i+1] = F(S[i]).

Your objective is to deduce the operational state code of the initial process (workstation S[1]) or the final process (workstation S[N]) through a limited number of sensor readings.

You can use the following two types of reading commands, each consuming one system call budget:

1. State Polling: Read the specific state code of a given workstation (Note: to avoid disrupting material intake/output, you can only poll workstations from 2 to {n_minus_1}, not the first or last directly).
2. State Verification: Verify whether two workstations share the exact same state code (also restricted to workstations from 2 to {n_minus_1}).

Once sufficient telemetry is gathered, you can submit your final production state diagnostic. You need to determine the state of S[1] or S[N] (or both).

## Command and Diagnostic Format (strictly required)

Each turn must contain only one command or diagnostic submission. Use the following XML format:

- State Polling (e.g., polling workstation 5):
<query_reveal>5</query_reveal>

- State Verification (e.g., verifying if workstations 3 and 7 are in the same state):
<query_equal>3,7</query_equal>

- Submit Diagnostic (deduce the initial or final workstation state, or both):
<answer>head=A</answer>
or
<answer>tail=D</answer>
or
<answer>head=A, tail=D</answer>

Notes:
- Workstation indices must be between 2 and {n_minus_1}
- Letters in the answer must be one of A, B, C, or D
- Try to complete the inference with as few system calls as possible
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
我们来模拟一个"证据链密级流转推理"场景。

在一宗复杂案件的司法审查中，一份关键物证经历了一条包含 {n} 个连续交接环节的证据链 S[1..{n}]。在每一个环节，该证据被赋予的保密级别标识属于四类法定密级 {{A, B, C, D}} 之一。司法程序规定了一套隐藏的密级转换协议 F，它将四类密级一一对应地在各环节间流转变更（例如 A→B, B→C, C→D, D→A），并且满足：对于所有相邻的交接环节 i 和 i+1，都满足 S[i+1] = F(S[i])。

你的目标是通过有限次调卷审查，推断出证据在初始提取环节（S[1]）或最终归档环节（S[N]）的保密级别。

你可以使用以下两种审查权限，每次消耗一次调查配额：

1. 卷宗查阅：查阅某中间交接环节证据的具体密级（注意：基于保密法限制，只能查阅环节 2 到 {n_minus_1} 的卷宗，不能直接触及源头和最终归档）
2. 密级核针对：核对两个交接环节的密级标识是否完全一致（同样限制在环节 2 到 {n_minus_1} 之间）

当你收集到足够信息后，可以提交最终的法务取证报告。你需要推断 S[1] 或 S[N] 的密级（或两者都推断）。

## 审查与报告提交格式（必须严格遵守）

每次只能行使一项审查权限或提交报告。请使用以下 XML 格式：

- 卷宗查阅（例如查阅环节 5 的密级）：
<query_reveal>5</query_reveal>

- 密级核对（例如核对环节 3 和环节 7 的密级是否相同）：
<query_equal>3,7</query_equal>

- 提交报告（推断初始或最终环节的密级，或两者都推断）：
<answer>head=A</answer>
或
<answer>tail=D</answer>
或
<answer>head=A, tail=D</answer>

注意：
- 环节编号必须在 2 到 {n_minus_1} 之间
- 答案中的密级字母必须是 A、B、C、D 之一
- 请尽可能用最少的调查次数完成推理
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's simulate a "Chain of Custody Classification Inference" scenario.

During the judicial review of a complex case, a piece of key physical evidence moves through a chain of custody consisting of {n} consecutive transfer steps S[1..{n}]. At each step, the security classification assigned to the evidence falls into one of four statutory levels {{A, B, C, D}}. Judicial procedure mandates a hidden classification transition protocol F that bijectively alters the classification between steps (e.g., A→B, B→C, C→D, D→A), ensuring that for all adjacent transfer steps i and i+1, S[i+1] = F(S[i]).

Your objective is to deduce the security classification at the initial extraction step (S[1]) or the final archiving step (S[N]) through a limited number of file audits.

You can use the following two types of audit queries, each consuming one investigation quota:

1. File Audit: Reveal the specific classification level at a given intermediate step (Note: due to confidentiality laws, you can only audit steps from 2 to {n_minus_1}, not the source or final archive directly).
2. Classification Cross-Check: Verify whether the classification levels at two transfer steps are exactly identical (also restricted to steps from 2 to {n_minus_1}).

Once sufficient evidentiary data is gathered, you can submit your final forensic legal report. You need to infer the classification of S[1] or S[N] (or both).

## Audit and Report Format (strictly required)

Each turn must contain only one audit query or report submission. Use the following XML format:

- File Audit (e.g., auditing step 5):
<query_reveal>5</query_reveal>

- Classification Cross-Check (e.g., checking if steps 3 and 7 share the same classification):
<query_equal>3,7</query_equal>

- Submit Report (deduce the initial or final step classification, or both):
<answer>head=A</answer>
or
<answer>tail=D</answer>
or
<answer>head=A, tail=D</answer>

Notes:
- Step indices must be between 2 and {n_minus_1}
- Letters in the answer must be one of A, B, C, or D
- Try to complete the inference with as few audits as possible
"""

    tags = ["answer", "query_reveal", "query_equal"]
    
    # 类属性
    reasoning_type = "归纳推理"
    data_structure = "序列"

    # 难度配置：
    # 1 (简单)        - N=8,  T=6,  置换简单（循环）
    # 2 (中等偏下)    - N=10, T=8,  置换稍复杂
    # 3 (中等偏上)    - N=12, T=10, 置换较复杂
    # 4 (较难)        - N=15, T=12, 置换复杂
    # 5 (难)          - N=20, T=12, 置换非常复杂

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "permutation": {"A": "B", "B": "C", "C": "D", "D": "A"},  # 简单循环
                "start": "A",  # S[1] = A
            },
            2: {
                "n": 10,
                "permutation": {"A": "C", "C": "B", "B": "D", "D": "A"},
                "start": "B",
            },
            3: {
                "n": 12,
                "permutation": {"A": "D", "D": "C", "C": "B", "B": "A"},
                "start": "C",
            },
            4: {
                "n": 15,
                "permutation": {"A": "B", "B": "D", "D": "C", "C": "A"},
                "start": "A",
            },
            5: {
                "n": 20,
                "permutation": {"A": "C", "C": "D", "D": "B", "B": "A"},
                "start": "D",
            },
        },
        "en": {
            1: {
                "n": 8,
                "permutation": {"A": "B", "B": "C", "C": "D", "D": "A"},
                "start": "A",
            },
            2: {
                "n": 10,
                "permutation": {"A": "C", "C": "B", "B": "D", "D": "A"},
                "start": "B",
            },
            3: {
                "n": 12,
                "permutation": {"A": "D", "D": "C", "C": "B", "B": "A"},
                "start": "C",
            },
            4: {
                "n": 15,
                "permutation": {"A": "B", "B": "D", "D": "C", "C": "A"},
                "start": "A",
            },
            5: {
                "n": 20,
                "permutation": {"A": "C", "C": "D", "D": "B", "B": "A"},
                "start": "D",
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 查询计数器
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.permutation = cfg["permutation"]
        self.start = cfg["start"]
        
        # 计算查询预算 T = min(12, N-2)
        self.max_queries = min(12, self.n - 2)
        
        # 生成完整序列 S[1..N]
        self.sequence = [None] * (self.n + 1)  # 索引 0 不使用，1..N
        self.sequence[1] = self.start
        for i in range(2, self.n + 1):
            self.sequence[i] = self.permutation[self.sequence[i - 1]]
        
        # 用于格式化游戏规则
        self._game_info["n"] = self.n
        self._game_info["n_minus_1"] = self.n - 1

    def evaluate(self, parsed_info):
        """
        评估答案是否正确
        答案格式：head=X 或 tail=X 或 head=X, tail=Y
        """
        raw_ans = parsed_info["answer"]
        
        # 解析答案
        parts = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                ans_dict[k.strip().lower()] = v.strip().upper()
        
        # 至少要有 head 或 tail 之一
        if "head" not in ans_dict and "tail" not in ans_dict:
            return False
        
        # 检查 head（S[1]）
        if "head" in ans_dict:
            if ans_dict["head"] != self.sequence[1]:
                return False
        
        # 检查 tail（S[N]）
        if "tail" in ans_dict:
            if ans_dict["tail"] != self.sequence[self.n]:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """
        原始业务逻辑：处理查询并生成响应
        """
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_range = f"错误：位置必须在 2 到 {self.n - 1} 之间。此次查询不计入预算。"
            error_format = "错误：格式无效。此次查询不计入预算。"
            budget_exceeded = f"已超过最大查询次数限制（{self.max_queries}次），请直接提交你的答案。"
        else:
            yes_res, no_res = "Yes", "No"
            error_range = f"Error: Position must be between 2 and {self.n - 1}. This query does not count."
            error_format = "Error: Invalid format. This query does not count."
            budget_exceeded = f"Exceeded maximum query limit ({self.max_queries} queries). Please submit your answer directly."
        
        # 检查是否超过查询预算
        if self.query_count >= self.max_queries:
            return budget_exceeded
        
        # 处理取值查询
        if "query_reveal" in parsed_info:
            try:
                pos = int(parsed_info["query_reveal"].strip())
                if pos < 2 or pos > self.n - 1:
                    return error_range
                self.query_count += 1
                return self.sequence[pos]
            except (ValueError, TypeError):
                return error_format
        
        # 处理相等性查询
        elif "query_equal" in parsed_info:
            try:
                raw = parsed_info["query_equal"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                pos1, pos2 = int(parts[0]), int(parts[1])
                if pos1 < 2 or pos1 > self.n - 1 or pos2 < 2 or pos2 > self.n - 1:
                    return error_range
                self.query_count += 1
                return yes_res if self.sequence[pos1] == self.sequence[pos2] else no_res
            except (ValueError, TypeError):
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """
        根据正确答案生成一个明显不同的错误答案。
        """
        correct_str = str(correct)
        
        # 处理单个字母 A/B/C/D（reveal query 的返回值）
        if correct_str.upper() in {"A", "B", "C", "D"}:
            alternatives = [c for c in ["A", "B", "C", "D"] if c != correct_str.upper()]
            return alternatives[0]
        
        # 若 correct 是纯整数字符串
        if correct_str.isdigit():
            return str(int(correct_str) + 1)
        
        # 中文处理
        if self.config.language == "zh":
            if correct_str == "是":
                return "否"
            elif correct_str == "否":
                return "是"
        
        # 英文处理 (忽略大小写，但保持原始大小写风格不太容易完全通用，这里简单处理常见情况)
        lower_correct = correct_str.lower()
        if lower_correct == "yes":
            # 尝试保持大小写
            if correct_str.isupper(): return "NO"
            if correct_str.istitle(): return "No"
            return "no"
        elif lower_correct == "no":
            if correct_str.isupper(): return "YES"
            if correct_str.istitle(): return "Yes"
            return "yes"

        # 若都不匹配
        return correct_str + "_WRONG"

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
        results = []
        
        # 根据语言设置确定回答文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        # 1. 枚举取值查询 (Reveal Query)
        # 范围：2 到 n-1
        # self.n 是序列长度，有效索引 2..n-1
        for pos in range(2, self.n):
            # 构造 XML 格式的查询字符串
            xml_query = f"<query_reveal>{pos}</query_reveal>"
            # 获取正确答案
            ans = self.sequence[pos]
            results.append({
                "query": xml_query,
                "answer": str(ans)
            })
            
        # 2. 枚举相等性查询 (Equality Query)
        # 仅枚举相邻位置的相等性查询以控制总量
        for pos1 in range(2, self.n):
            for pos2 in range(pos1 + 1, min(pos1 + 4, self.n)):  # 限制间距不超过3
                # 构造 XML 格式的查询字符串
                xml_query = f"<query_equal>{pos1},{pos2}</query_equal>"
                # 获取正确答案
                is_equal = (self.sequence[pos1] == self.sequence[pos2])
                ans = yes_res if is_equal else no_res
                results.append({
                    "query": xml_query,
                    "answer": str(ans)
                })
                
        return results