# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   元素唯一性：某个特定元素在集合中是否唯一（不重复）
# ============================================================

from .base import Game
import random
import itertools

class BinaryDetectorGame(Game):

    game_rule_zh = """\
我们现在来玩一个"二值判定器推理"的游戏，规则如下：

游戏设定了一个全集 U = {{1, 2, ..., {n}}}（编号仅作标识）。每个元素都有一个隐藏的二元属性，取值为 0 或 1。属性为 1 的元素个数未知，可能为 0、1 或多于 1。

存在一个固定但未知的二值判定器 f，它对任意子集 S 的检验结果仅由 S 中属性为 1 的元素计数 k 通过以下四种模式之一决定：
- M1（恰一）：当且仅当 k = 1 时，判定器返回"发光"。
- M2（至少一）：当且仅当 k 大于等于 1 时，判定器返回"发光"。
- M3（至少二）：当且仅当 k 大于等于 2 时，判定器返回"发光"。
- M4（偶数）：当且仅当 k 为偶数（包括 0）时，判定器返回"发光"。

模式在整个游戏过程中固定但未知。你可以提交任意子集 S 进行检验（包括空集），我会返回"发光"或"不发光"。

你的目标是通过尽可能少的检验次数推断出：
1. 判定器的模式（M1、M2、M3 或 M4）
2. 全集 U 中属性为 1 的元素是否"恰好出现一次"（回答"是"或"否"）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 子集检验（例如检验编号 1、3、5 的子集）：
<query_subset>1,3,5</query_subset>

- 检验空集：
<query_subset></query_subset>

提交最终答案时，必须说明判定器模式和唯一性判断，格式如下：

<answer>mode=M2, unique=否</answer>

其中 mode 取值为 M1、M2、M3 或 M4 之一，unique 取值为"是"或"否"（英文环境下为 Yes 或 No）。
"""

    game_rule_en = """\
Let's play a "Binary Detector Inference" game. Here are the rules:

The game defines a universal set U = {{1, 2, ..., {n}}} (IDs are for identification only). Each element has a hidden binary attribute valued at 0 or 1. The count of elements with attribute 1 is unknown and may be 0, 1, or more than 1.

There exists a fixed but unknown binary detector f that determines the result for any subset S based solely on the count k of elements with attribute 1 in S, following one of four modes:
- M1 (Exactly One): Returns "glowing" if and only if k = 1.
- M2 (At Least One): Returns "glowing" if and only if k is greater than or equal to 1.
- M3 (At Least Two): Returns "glowing" if and only if k is greater than or equal to 2.
- M4 (Even Count): Returns "glowing" if and only if k is even (including 0).

The mode is fixed throughout the game but unknown. You may submit any subset S for testing (including the empty set), and I will return "glowing" or "not glowing".

Your goal is to infer through as few tests as possible:
1. The detector's mode (M1, M2, M3, or M4)
2. Whether elements with attribute 1 appear "exactly once" in the universal set U (answer Yes or No)

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Subset test (e.g., testing subset with IDs 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Test empty set:
<query_subset></query_subset>

When submitting the final answer, specify the detector mode and uniqueness judgment using this format:

<answer>mode=M2, unique=No</answer>

Where mode is one of M1, M2, M3, or M4, and unique is Yes or No (or 是 or 否 in Chinese environment).
"""

    contextualized_rule_zh_1 = """\
[交通场景]
在城市交通网络中，有一组受监控的交通信号控制节点，集合 U = {{1, 2, ..., {n}}}（编号为路口标识）。部分节点可能存在“隐蔽性硬件故障”（隐藏属性为 1）。实际存在故障的节点数未知（可能为 0、1 或多个）。

现有一台自动网络诊断仪（判定器 f），你可以向它输入任意节点子集 S 进行联合测试。诊断仪的主面板指示灯反馈结果，仅取决于 S 中实际故障节点数量 k，并遵循以下四种硬件诊断模式之一：
- M1（单一激增）：当且仅当 k = 1 时，指示灯返回"发光"。
- M2（阻断报警）：当且仅当 k 大于等于 1 时，指示灯返回"发光"。
- M3（级联风险）：当且仅当 k 大于等于 2 时，指示灯返回"发光"。
- M4（偶数回路）：当且仅当 k 为偶数（包括 0）时，指示灯返回"发光"。

该诊断模式在整个检测过程中固定但未知。你可以提交任意节点子集 S 进行检验（包括空集），系统会返回指示灯"发光"或"不发光"。

你的目标是通过尽可能少的检验次数推断出：
1. 诊断仪当前的模式（M1、M2、M3 或 M4）
2. 全集 U 中存在硬件故障的节点是否"恰好出现一次"（回答"是"或"否"）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，排查任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 子集检验（例如检验编号 1、3、5 的节点子集）：
<query_subset>1,3,5</query_subset>

- 检验空集：
<query_subset></query_subset>

提交最终答案时，必须说明判定器模式和唯一性判断，格式如下：

<answer>mode=M2, unique=否</answer>

其中 mode 取值为 M1、M2、M3 或 M4 之一，unique 取值为"是"或"否"（英文环境下为 Yes 或 No）。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
In an urban traffic network, there is a set of monitored traffic signal control nodes, U = {{1, 2, ..., {n}}} (IDs serve as intersection identifiers). Some nodes may have a "hidden hardware fault" (hidden attribute 1). The exact number of faulty nodes is unknown and may be 0, 1, or more.

You have an automated network diagnostic device (detector f). You can submit any subset of nodes S for joint testing. The device returns a result via its main panel indicator, which depends solely on the count k of faulty nodes in S, following one of four hardware diagnostic modes:
- M1 (Single Surge): Returns "glowing" if and only if k = 1.
- M2 (Blockage Alert): Returns "glowing" if and only if k is greater than or equal to 1.
- M3 (Cascade Risk): Returns "glowing" if and only if k is greater than or equal to 2.
- M4 (Even Circuit): Returns "glowing" if and only if k is even (including 0).

The mode is fixed throughout the detection process but unknown. You may submit any subset S for testing (including the empty set), and the system will return "glowing" or "not glowing".

Your goal is to infer through as few tests as possible:
1. The diagnostic device's current mode (M1, M2, M3, or M4)
2. Whether the node with a hardware fault appears "exactly once" in the universal set U (answer Yes or No)

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, the troubleshooting task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Subset test (e.g., testing subset with IDs 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Test empty set:
<query_subset></query_subset>

When submitting the final answer, specify the detector mode and uniqueness judgment using this format:

<answer>mode=M2, unique=No</answer>

Where mode is one of M1, M2, M3, or M4, and unique is Yes or No (or 是 or 否 in Chinese environment).
"""

    contextualized_rule_zh_2 = """\
[医疗场景]
在罕见病基因组学研究中，全集 U = {{1, 2, ..., {n}}} 代表一组待测的候选基因片段编号。部分基因可能携带某种特定的“隐性致病突变”（隐藏属性为 1）。突变基因的实际数量未知（可能为 0、1 或多个）。

实验室使用一种高级荧光显色试剂（判定器 f）。你可以选择任意基因片段子集 S 加入试剂进行混合测序。试剂的显色反应仅由 S 中携带致病突变的基因数量 k 决定，且遵循以下四种生化反应模式之一：
- M1（特异结合）：当且仅当 k = 1 时，试剂发生荧光反应，呈现"发光"。
- M2（敏感触发）：当且仅当 k 大于等于 1 时，试剂呈现"发光"。
- M3（协同扩增）：当且仅当 k 大于等于 2 时，试剂呈现"发光"。
- M4（配对湮灭）：当且仅当 k 为偶数（包括 0）时，试剂呈现"发光"。

该生化反应模式在整个实验过程中固定但未知。你可以提交任意子集 S 进行检验（包括空集），试剂会返回"发光"或"不发光"。

你的目标是通过尽可能少的检验次数推断出：
1. 试剂当前的生化反应模式（M1、M2、M3 或 M4）
2. 携带该致病突变的基因在全集 U 中是否"恰好出现一次"（回答"是"或"否"）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，实验验证失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 子集检验（例如检验编号 1、3、5 的基因子集）：
<query_subset>1,3,5</query_subset>

- 检验空集：
<query_subset></query_subset>

提交最终答案时，必须说明判定器模式和唯一性判断，格式如下：

<answer>mode=M2, unique=否</answer>

其中 mode 取值为 M1、M2、M3 或 M4 之一，unique 取值为"是"或"否"（英文环境下为 Yes 或 No）。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
In rare disease genomics research, the universal set U = {{1, 2, ..., {n}}} represents a group of candidate gene fragments to be tested. Some genes may carry a specific "recessive pathogenic mutation" (hidden attribute 1). The count of such mutated genes is unknown and may be 0, 1, or more.

The laboratory uses an advanced fluorescent colorimetric reagent (detector f). You can select any subset of gene fragments S and add them to the reagent for pooled sequencing. The reagent's reaction is determined solely by the count k of mutated genes in S, following one of four biochemical reaction modes:
- M1 (Specific Binding): The reagent shows fluorescence, returning "glowing" if and only if k = 1.
- M2 (Sensitive Trigger): Returns "glowing" if and only if k is greater than or equal to 1.
- M3 (Synergistic Amplification): Returns "glowing" if and only if k is greater than or equal to 2.
- M4 (Pair Annihilation): Returns "glowing" if and only if k is even (including 0).

The reaction mode is fixed throughout the experiment but unknown. You may submit any subset S for testing (including the empty set), and the reagent will return "glowing" or "not glowing".

Your goal is to infer through as few tests as possible:
1. The reagent's current biochemical reaction mode (M1, M2, M3, or M4)
2. Whether the gene with the pathogenic mutation appears "exactly once" in the universal set U (answer Yes or No)

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, the experimental validation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Subset test (e.g., testing subset with IDs 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Test empty set:
<query_subset></query_subset>

When submitting the final answer, specify the detector mode and uniqueness judgment using this format:

<answer>mode=M2, unique=No</answer>

Where mode is one of M1, M2, M3, or M4, and unique is Yes or No (or 是 or 否 in Chinese environment).
"""

    contextualized_rule_zh_3 = """\
[教育场景]
在一次教育心理学行为测试中，全集 U = {{1, 2, ..., {n}}} 代表参与测试的实验学生编号。部分学生具备某种“潜在的特定认知天赋”（隐藏属性为 1）。具备该天赋的学生数量未知（可能为 0、1 或多个）。

测试系统采用了一种协同解题验证机（判定器 f）。你可以安排任意学生子集 S 组成讨论组，向验证机提交共同解答。验证机的反馈指示灯仅取决于 S 中具备该天赋的学生数量 k，且测试系统会锁定在以下四种行为评估模式之一：
- M1（独立主导）：当且仅当 k = 1 时，指示灯返回"发光"。
- M2（群体启蒙）：当且仅当 k 大于等于 1 时，指示灯返回"发光"。
- M3（火花碰撞）：当且仅当 k 大于等于 2 时，指示灯返回"发光"。
- M4（成对平衡）：当且仅当 k 为偶数（包括 0）时，指示灯返回"发光"。

该评估模式在整个测试过程中固定但未知。你可以安排任意子集 S 进行评估（包括空集），验证机会返回指示灯"发光"或"不发光"。

你的目标是通过尽可能少的检验次数推断出：
1. 测试系统当前锁定的评估模式（M1、M2、M3 或 M4）
2. 具备该认知天赋的学生在全集 U 中是否"恰好只有一人"（回答"是"或"否"）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，测试评估失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 子集检验（例如检验编号 1、3、5 的学生子集）：
<query_subset>1,3,5</query_subset>

- 检验空集：
<query_subset></query_subset>

提交最终答案时，必须说明判定器模式和唯一性判断，格式如下：

<answer>mode=M2, unique=否</answer>

其中 mode 取值为 M1、M2、M3 或 M4 之一，unique 取值为"是"或"否"（英文环境下为 Yes 或 No）。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
In an educational psychology behavioral test, the universal set U = {{1, 2, ..., {n}}} represents the IDs of participating students. Some students possess a "latent specific cognitive gift" (hidden attribute 1). The count of gifted students is unknown and may be 0, 1, or more.

The test system uses a collaborative problem-solving validator (detector f). You can assign any subset of students S to form a discussion group and submit a joint answer to the validator. The validator's feedback indicator depends solely on the count k of gifted students in S, locked into one of four behavioral assessment modes:
- M1 (Independent Lead): Returns "glowing" if and only if k = 1.
- M2 (Group Enlightenment): Returns "glowing" if and only if k is greater than or equal to 1.
- M3 (Spark Collision): Returns "glowing" if and only if k is greater than or equal to 2.
- M4 (Pair Balance): Returns "glowing" if and only if k is even (including 0).

The assessment mode is fixed throughout the test but unknown. You may submit any subset S for evaluation (including the empty set), and the validator will return "glowing" or "not glowing".

Your goal is to infer through as few tests as possible:
1. The test system's current assessment mode (M1, M2, M3, or M4)
2. Whether the student possessing the cognitive gift appears "exactly once" in the universal set U (answer Yes or No)

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, the test evaluation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Subset test (e.g., testing subset with IDs 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Test empty set:
<query_subset></query_subset>

When submitting the final answer, specify the detector mode and uniqueness judgment using this format:

<answer>mode=M2, unique=No</answer>

Where mode is one of M1, M2, M3, or M4, and unique is Yes or No (or 是 or 否 in Chinese environment).
"""

    contextualized_rule_zh_4 = """\
[制造业/工业场景]
在高端半导体制造流水线上，有一批晶圆批次，全集 U = {{1, 2, ..., {n}}}（编号为晶圆批次号）。部分批次在光刻环节引入了不可见的“微观缺陷”（隐藏属性为 1）。含有微观缺陷的批次数量未知（可能为 0、1 或多个）。

品控部门使用了一台批量扫描分析仪（判定器 f）。你可以将任意批次子集 S 放入扫描仪进行批量无损探伤。分析仪的警报指示灯仅由 S 中含有微观缺陷的批次数量 k 决定，且固定运行于以下四种检测模式之一：
- M1（单点隔离）：当且仅当 k = 1 时，指示灯返回"发光"。
- M2（阈值告警）：当且仅当 k 大于等于 1 时，指示灯返回"发光"。
- M3（交叉污染）：当且仅当 k 大于等于 2 时，指示灯返回"发光"。
- M4（偶数谐波）：当且仅当 k 为偶数（包括 0）时，指示灯返回"发光"。

该检测模式在整个扫描探伤过程中固定但未知。你可以提交任意批次子集 S 进行检测（包括空集），分析仪会返回指示灯"发光"或"不发光"。

你的目标是通过尽可能少的检验次数推断出：
1. 扫描分析仪当前的检测模式（M1、M2、M3 或 M4）
2. 含有微观缺陷的晶圆批次在全集 U 中是否"恰好只有一个"（回答"是"或"否"）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，品质检测任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 子集检验（例如检验编号 1、3、5 的晶圆批次子集）：
<query_subset>1,3,5</query_subset>

- 检验空集：
<query_subset></query_subset>

提交最终答案时，必须说明判定器模式和唯一性判断，格式如下：

<answer>mode=M2, unique=否</answer>

其中 mode 取值为 M1、M2、M3 或 M4 之一，unique 取值为"是"或"否"（英文环境下为 Yes 或 No）。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
On a high-end semiconductor manufacturing line, there is a batch of wafers, U = {{1, 2, ..., {n}}} (IDs are batch numbers). Some batches introduced invisible "micro-defects" during lithography (hidden attribute 1). The count of defective batches is unknown and may be 0, 1, or more.

Quality control uses a batch scanning analyzer (detector f). You can place any subset of batches S into the analyzer for non-destructive batch testing. The analyzer's alert indicator is determined solely by the count k of defective batches in S, operating fixedly in one of four detection modes:
- M1 (Single Isolation): Returns "glowing" if and only if k = 1.
- M2 (Threshold Alert): Returns "glowing" if and only if k is greater than or equal to 1.
- M3 (Cross Contamination): Returns "glowing" if and only if k is greater than or equal to 2.
- M4 (Even Harmonics): Returns "glowing" if and only if k is even (including 0).

The detection mode is fixed throughout the scanning process but unknown. You may submit any subset S for testing (including the empty set), and the analyzer will return "glowing" or "not glowing".

Your goal is to infer through as few tests as possible:
1. The analyzer's current detection mode (M1, M2, M3, or M4)
2. Whether the defective batch appears "exactly once" in the universal set U (answer Yes or No)

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, the quality inspection task fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Subset test (e.g., testing subset with IDs 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Test empty set:
<query_subset></query_subset>

When submitting the final answer, specify the detector mode and uniqueness judgment using this format:

<answer>mode=M2, unique=No</answer>

Where mode is one of M1, M2, M3, or M4, and unique is Yes or No (or 是 or 否 in Chinese environment).
"""

    contextualized_rule_zh_5 = """\
[法律场景]
在一起复杂的金融欺诈案件调查中，全集 U = {{1, 2, ..., {n}}} 代表一系列被查封的离岸银行账户编号。部分账户实际参与了“非法资金洗钱”（隐藏属性为 1）。参与洗钱的账户实际数量未知（可能为 0、1 或多个）。

司法鉴定中心部署了一套自动资金流审查AI（判定器 f）。你可以提交任意账户子集 S 给该系统进行关联交易审计。系统的合规预警指示灯仅受 S 中涉案洗钱账户的数量 k 影响，且遵循以下四种审计逻辑模式之一：
- M1（孤立追溯）：当且仅当 k = 1 时，预警指示灯返回"发光"。
- M2（连带触发）：当且仅当 k 大于等于 1 时，预警指示灯返回"发光"。
- M3（团伙串联）：当且仅当 k 大于等于 2 时，预警指示灯返回"发光"。
- M4（对冲抵消）：当且仅当 k 为偶数（包括 0）时，预警指示灯返回"发光"。

该审计逻辑模式在整个调查过程中固定但未知。你可以提交任意账户子集 S 进行审计（包括空集），AI 系统会返回预警指示灯"发光"或"不发光"。

你的目标是通过尽可能少的查询次数推断出：
1. 审查AI当前采用的审计逻辑模式（M1、M2、M3 或 M4）
2. 参与非法洗钱的账户在全集 U 中是否"恰好只有一个"（回答"是"或"否"）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，案件侦破宣告失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 子集检验（例如检验编号 1、3、5 的账户子集）：
<query_subset>1,3,5</query_subset>

- 检验空集：
<query_subset></query_subset>

提交最终答案时，必须说明判定器模式和唯一性判断，格式如下：

<answer>mode=M2, unique=否</answer>

其中 mode 取值为 M1、M2、M3 或 M4 之一，unique 取值为"是"或"否"（英文环境下为 Yes 或 No）。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
In a complex financial fraud investigation, the universal set U = {{1, 2, ..., {n}}} represents a series of seized offshore bank accounts. Some accounts were actually involved in "illegal money laundering" (hidden attribute 1). The count of money laundering accounts is unknown and may be 0, 1, or more.

The forensic center deployed an automated fund flow review AI (detector f). You can submit any subset of accounts S to this system for related transaction auditing. The system's compliance alert indicator is affected solely by the count k of money laundering accounts in S, following one of four audit logic modes:
- M1 (Isolated Trace): Returns "glowing" if and only if k = 1.
- M2 (Joint Trigger): Returns "glowing" if and only if k is greater than or equal to 1.
- M3 (Syndicate Link): Returns "glowing" if and only if k is greater than or equal to 2.
- M4 (Hedge Offset): Returns "glowing" if and only if k is even (including 0).

The audit logic mode is fixed throughout the investigation but unknown. You may submit any subset S for auditing (including the empty set), and the AI system will return "glowing" or "not glowing".

Your goal is to infer through as few queries as possible:
1. The AI's current audit logic mode (M1, M2, M3, or M4)
2. Whether the account involved in money laundering appears "exactly once" in the universal set U (answer Yes or No)

When you have collected enough information, please submit your final answer. If the answer is wrong or the format is invalid, the investigation fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Subset test (e.g., testing subset with IDs 1, 3, 5):
<query_subset>1,3,5</query_subset>

- Test empty set:
<query_subset></query_subset>

When submitting the final answer, specify the detector mode and uniqueness judgment using this format:

<answer>mode=M2, unique=No</answer>

Where mode is one of M1, M2, M3, or M4, and unique is Yes or No (or 是 or 否 in Chinese environment).
"""

    tags = ["answer", "query_subset"]
    
    reasoning_type = "溯因推理"
    data_structure = "集合"

    # 难度说明：
    # 1 (简单)      - N=4, 恰好1个属性元素, 模式 M1
    # 2 (中等偏下)  - N=5, 2个属性元素, 模式 M2
    # 3 (中等偏上)  - N=6, 3个属性元素, 模式 M3
    # 4 (较难)      - N=7, 0个属性元素, 模式 M4
    # 5 (难)        - N=8, 4个属性元素, 模式 M4

    DIFFICULTY_CONFIG = {
        1: {
            "n": 4,
            "attributes": "2",  # 元素2的属性为1
            "mode": "M1",
        },
        2: {
            "n": 5,
            "attributes": "1,4",  # 元素1和4的属性为1
            "mode": "M2",
        },
        3: {
            "n": 6,
            "attributes": "2,3,5",  # 元素2、3、5的属性为1
            "mode": "M3",
        },
        4: {
            "n": 7,
            "attributes": "",  # 没有元素属性为1
            "mode": "M4",
        },
        5: {
            "n": 8,
            "attributes": "1,3,5,7",  # 元素1、3、5、7的属性为1
            "mode": "M4",
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        
        # 解析属性为1的元素集合
        self.attribute_set = set()
        if cfg["attributes"]:
            for idx in cfg["attributes"].split(","):
                self.attribute_set.add(idx.strip())
        
        # 判定器模式
        self.mode = cfg["mode"]
        
        # 全集
        self.universe = set(str(i) for i in range(1, cfg["n"] + 1))

    def _evaluate_detector(self, subset):
        """
        根据模式和子集，计算判定器的返回值
        subset: 要检验的子集（字符串集合）
        返回: True (发光) 或 False (不发光)
        """
        # 计算子集中属性为1的元素个数
        k = len(subset & self.attribute_set)
        
        if self.mode == "M1":
            return k == 1
        elif self.mode == "M2":
            return k >= 1
        elif self.mode == "M3":
            return k >= 2
        elif self.mode == "M4":
            return k % 2 == 0
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def evaluate(self, parsed_info):
        """
        评估最终答案是否正确
        答案格式: mode=M1, unique=是
        """
        raw_ans = parsed_info["answer"]
        
        # 解析答案
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                return False
            k, v = kv.split("=", 1)
            ans_dict[k.strip().lower()] = v.strip()
        
        if "mode" not in ans_dict or "unique" not in ans_dict:
            return False
        
        # 1. 检查模式是否正确（不区分大小写）
        if ans_dict["mode"].upper() != self.mode:
            return False
        
        # 2. 检查唯一性判断是否正确
        is_unique = len(self.attribute_set) == 1
        
        user_unique = ans_dict["unique"].lower()
        
        if self.config.language == "zh":
            return (user_unique == "是") == is_unique
        else:
            return (user_unique == "yes") == is_unique

    def _cf_core_produce(self, parsed_info):
        if "query_subset" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        raw_subset = parsed_info["query_subset"].strip()
        
        # 解析子集
        query_set = set()
        if raw_subset:  # 非空集
            try:
                for idx in raw_subset.split(","):
                    idx = idx.strip()
                    if not idx:
                        continue
                    # 检查编号是否在全集中
                    if idx not in self.universe:
                        if self.config.language == "zh":
                            return "非法子集，请重提。"
                        else:
                            return "Invalid subset, please resubmit."
                    query_set.add(idx)
            except:
                if self.config.language == "zh":
                    return "非法子集，请重提。"
                else:
                    return "Invalid subset, please resubmit."
        
        # 计算判定器结果
        result = self._evaluate_detector(query_set)
        
        if self.config.language == "zh":
            return "发光" if result else "不发光"
        else:
            return "glowing" if result else "not glowing"

    def _cf_make_wrong(self, correct):
        # 翻转判定器结果
        if correct == "glowing":
            return "not glowing"
        if correct == "not glowing":
            return "glowing"
        if correct == "发光":
            return "不发光"
        if correct == "不发光":
            return "发光"
        
        # 对于非法子集的提示信息等，追加 _WRONG
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        n = self._game_info["n"]
        # 全集元素列表，保持升序
        elements = [str(i) for i in range(1, n + 1)]
        
        possible_queries = []
        
        # 遍历所有可能的子集大小 (从 0 到 n)
        for r in range(n + 1):
            # 遍历该大小下的所有组合
            for subset_tuple in itertools.combinations(elements, r):
                # 构造查询字符串 (例如: "1,3,5" 或 "" 对于空集)
                query_str = ",".join(subset_tuple)
                
                # 构造集合用于内部计算
                query_set = set(subset_tuple)
                
                # 直接调用内部逻辑计算结果
                is_glowing = self._evaluate_detector(query_set)
                
                # 根据语言环境生成对应文本
                if self.config.language == "zh":
                    ans = "发光" if is_glowing else "不发光"
                else:
                    ans = "glowing" if is_glowing else "not glowing"
                
                possible_queries.append({
                    "query": f"<query_subset>{query_str}</query_subset>",
                    "answer": ans
                })
                
        return possible_queries