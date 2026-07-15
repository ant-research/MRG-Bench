from .base import Game
import random
import itertools

class SequencePatternGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"序列识别"推理游戏，规则如下：

游戏设定了一个隐藏的字符序列 S，由字母表 {{R, G, B, Y}} 中的字符组成，长度为 {n}。

这个序列有一个特殊性质：它是由某个"基础块" M0 重复拼接而成的。例如，如果基础块是 "RGB"，序列就是 "RGBRGBRGB..."。基础块的长度 T 未知，但满足以下条件：
- T 大于等于 2 且小于等于 {t_max}
- 基础块 M0 是序列 S 的最小重复单元（不存在更短的周期）
- 序列长度 {n} 正好是 T 的整数倍

你的目标是通过提问推断出这个基础块 M0 及其长度 T。

每次你可以提交一个"判定查询"，格式如下：
- 指定一个区间 [L, R]（L 和 R 都是位置编号，从 1 到 {n}）
- 提供一个候选字符串 X（长度至少为 2）

我会告诉你：在区间 [L, R] 内，是否存在某个位置开始的子串恰好等于 X。
- 如果存在，回答"是"
- 如果不存在，回答"否"

注意：
- 区间必须足够容纳候选串（R - L + 1 必须大于等于 X 的长度），否则答案必为"否"
- 我只会告诉你"是"或"否"，不会告诉你具体位置、出现次数或其他信息
- 请尽可能少地使用提问次数

提问时使用以下 XML 格式：

<query>L,R,X</query>

其中 L 和 R 是区间端点（整数），X 是候选字符串（只包含 R、G、B、Y）。

例如，查询区间 [1, 10] 内是否存在子串 "RGB"：
<query>1,10,RGB</query>

当你准备好提交最终答案时，使用以下格式：

<answer>M0</answer>

其中 M0 是你推断出的基础块字符串。

例如：
<answer>RGB</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Pattern Recognition" deduction game. Here are the rules:

There is a hidden character sequence S composed of letters from the alphabet {{R, G, B, Y}}, with a length of {n}.

This sequence has a special property: it is formed by repeating a "base block" M0. For example, if the base block is "RGB", the sequence would be "RGBRGBRGB...". The length T of the base block is unknown, but satisfies the following conditions:
- T is greater than or equal to 2 and less than or equal to {t_max}
- The base block M0 is the minimal repeating unit of sequence S (no shorter period exists)
- The sequence length {n} is exactly a multiple of T

Your goal is to infer the base block M0 and its length T through queries.

Each time you can submit a "decision query" in the following format:
- Specify an interval [L, R] (L and R are position indices from 1 to {n})
- Provide a candidate string X (length at least 2)

I will tell you: whether there exists a substring starting at some position within interval [L, R] that exactly equals X.
- If it exists, answer "Yes"
- If it doesn't exist, answer "No"

Note:
- The interval must be large enough to contain the candidate string (R - L + 1 must be greater than or equal to the length of X), otherwise the answer will be "No"
- I will only tell you "Yes" or "No", without revealing specific positions, occurrence counts, or other information
- Please use as few queries as possible

For queries, use the following XML format:

<query>L,R,X</query>

Where L and R are interval endpoints (integers), and X is the candidate string (containing only R, G, B, Y).

For example, to query whether substring "RGB" exists in interval [1, 10]:
<query>1,10,RGB</query>

When you are ready to submit your final answer, use the following format:

<answer>M0</answer>

Where M0 is the base block string you inferred.

For example:
<answer>RGB</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项"交通信号周期识别"排查任务，规则如下：

交通控制系统记录了一段长度为 {n} 的交通信号相位序列 S，由 {{R, G, B, Y}} 四种状态代码组成（分别代表红灯、绿灯、公交专用灯、黄灯）。

该路口的信号灯有一个强制循环特性：它是按照某个最小的"基础周期" M0 不断往复执行拼接而成的。例如，如果基础周期是 "RGB"，整个时间轴序列就是 "RGBRGBRGB..."。基础周期 M0 的步长 T 未知，但满足以下条件：
- T 大于等于 2 且小于等于 {t_max}
- 基础周期 M0 是序列 S 的最小重复单元（不存在更短的循环逻辑）
- 总时长 {n} 正好是 T 的整数倍

你的目标是通过向系统查询，推断出这个基础信号周期 M0 及其步长 T。

每次你可以提交一个"相位区间验证"，格式如下：
- 指定一个时间区间 [L, R]（L 和 R 都是时间步编号，从 1 到 {n}）
- 提供一个候选相位串 X（长度至少为 2）

系统会告诉你：在区间 [L, R] 内，是否存在某个时间点开始的连续片段恰好等于 X。
- 如果存在，回答"是"
- 如果不存在，回答"否"

注意：
- 区间必须足够容纳候选串（R - L + 1 必须大于等于 X 的长度），否则答案必为"否"
- 系统只会返回"是"或"否"，不会告知具体发生位置、出现次数等详细日志
- 请尽可能少地使用查询次数

提问时使用以下 XML 格式：

<query>L,R,X</query>

其中 L 和 R 是区间端点（整数），X 是候选相位串（只包含 R、G、B、Y）。

例如，查询时间区间 [1, 10] 内是否出现了连续相位 "RGB"：
<query>1,10,RGB</query>

当你准备好提交最终排查结果时，使用以下格式：

<answer>M0</answer>

其中 M0 是你推断出的基础周期串。

例如：
<answer>RGB</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Traffic Signal Cycle Recognition" diagnostic task. Here are the rules:

The traffic control system has recorded a traffic signal phase sequence S with a length of {n}, composed of status codes {{R, G, B, Y}} (representing Red, Green, Bus-only, and Yellow lights respectively).

This intersection's signals have a mandatory loop property: they are formed by continuously repeating a minimal "base cycle" M0. For example, if the base cycle is "RGB", the entire timeline sequence would be "RGBRGBRGB...". The length T of the base cycle is unknown, but satisfies the following conditions:
- T is greater than or equal to 2 and less than or equal to {t_max}
- The base cycle M0 is the minimal repeating unit of sequence S (no shorter cycle logic exists)
- The total duration {n} is exactly a multiple of T

Your goal is to infer the base signal cycle M0 and its length T through system queries.

Each time you can submit a "phase interval verification" in the following format:
- Specify a time interval [L, R] (L and R are time step indices from 1 to {n})
- Provide a candidate phase string X (length at least 2)

The system will tell you: whether there exists a continuous segment starting at some point within interval [L, R] that exactly equals X.
- If it exists, answer "Yes"
- If it doesn't exist, answer "No"

Note:
- The interval must be large enough to contain the candidate string (R - L + 1 must be greater than or equal to the length of X), otherwise the answer will be "No"
- The system will only tell you "Yes" or "No", without revealing specific occurrence positions, counts, or other detailed logs
- Please use as few queries as possible

For queries, use the following XML format:

<query>L,R,X</query>

Where L and R are interval endpoints (integers), and X is the candidate phase string (containing only R, G, B, Y).

For example, to query whether the continuous phase "RGB" occurred in time interval [1, 10]:
<query>1,10,RGB</query>

When you are ready to submit your final diagnostic result, use the following format:

<answer>M0</answer>

Where M0 is the base cycle string you inferred.

For example:
<answer>RGB</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项"基因序列基序识别"分析任务，规则如下：

检测设备提取了一段长度为 {n} 的大分子链序列 S，由 {{R, G, B, Y}} 四类特定生物标志物代码组成。

该分子链具有高度规律性：它是由于某个核心"基因基序" M0 连续复制拼接而成的。例如，如果核心基序是 "RGB"，整个分子链就是 "RGBRGBRGB..."。基序 M0 的长度 T 未知，但满足以下条件：
- T 大于等于 2 且小于等于 {t_max}
- 核心基序 M0 是序列 S 的最小表达单元（不存在更短的有效重复片段）
- 序列总长 {n} 正好是 T 的整数倍

你的目标是通过定向探测，推断出这个核心基因基序 M0 及其长度 T。

每次你可以提交一个"片段探针验证"，格式如下：
- 指定一个测序区间 [L, R]（L 和 R 都是位点编号，从 1 到 {n}）
- 提供一个候选靶向序列 X（长度至少为 2）

仪器会告诉你：在区间 [L, R] 内，是否存在某个位点开始的连续片段恰好与 X 匹配。
- 如果存在，回答"是"
- 如果不存在，回答"否"

注意：
- 区间必须足够容纳靶向序列（R - L + 1 必须大于等于 X 的长度），否则答案必为"否"
- 仪器只会返回"是"或"否"，不会提供具体结合位点、荧光强度等其他参数
- 请尽可能少地消耗探测次数

提问时使用以下 XML 格式：

<query>L,R,X</query>

其中 L 和 R 是区间端点（整数），X 是候选靶向序列（只包含 R、G、B、Y）。

例如，探测位点区间 [1, 10] 内是否存在靶向片段 "RGB"：
<query>1,10,RGB</query>

当你准备好提交最终测序结果时，使用以下格式：

<answer>M0</answer>

其中 M0 是你推断出的核心基序。

例如：
<answer>RGB</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Genetic Motif Recognition" analysis task. Here are the rules:

The testing equipment has extracted a macromolecular chain sequence S with a length of {n}, composed of four specific biomarker codes {{R, G, B, Y}}.

This molecular chain has high regularity: it is formed by continuously replicating a core "gene motif" M0. For example, if the core motif is "RGB", the entire chain would be "RGBRGBRGB...". The length T of motif M0 is unknown, but satisfies the following conditions:
- T is greater than or equal to 2 and less than or equal to {t_max}
- The core motif M0 is the minimal expression unit of sequence S (no shorter valid repeating segment exists)
- The total chain length {n} is exactly a multiple of T

Your goal is to infer the core gene motif M0 and its length T through targeted probing.

Each time you can submit a "segment probe verification" in the following format:
- Specify a sequencing interval [L, R] (L and R are locus indices from 1 to {n})
- Provide a candidate target sequence X (length at least 2)

The instrument will tell you: whether there exists a continuous segment starting at some locus within interval [L, R] that exactly matches X.
- If it exists, answer "Yes"
- If it doesn't exist, answer "No"

Note:
- The interval must be large enough to contain the target sequence (R - L + 1 must be greater than or equal to the length of X), otherwise the answer will be "No"
- The instrument will only tell you "Yes" or "No", without providing specific binding loci, fluorescence intensity, or other parameters
- Please use as few probe attempts as possible

For queries, use the following XML format:

<query>L,R,X</query>

Where L and R are interval endpoints (integers), and X is the candidate target sequence (containing only R, G, B, Y).

For example, to probe whether target segment "RGB" exists within locus interval [1, 10]:
<query>1,10,RGB</query>

When you are ready to submit your final sequencing result, use the following format:

<answer>M0</answer>

Where M0 is the core motif you inferred.

For example:
<answer>RGB</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项"教学模块周期识别"评估任务，规则如下：

教务系统记录了一套长度为 {n} 的标准化教学活动序列 S，由 {{R, G, B, Y}} 四种活动代码组成（分别代表阅读、小组、板书、延展活动）。

该课程设计遵循严格的循环逻辑：它是由某个最小的"基础教学模块" M0 重复排布而成的。例如，如果基础模块是 "RGB"，整个学期序列就是 "RGBRGBRGB..."。基础模块 M0 的课时数 T 未知，但满足以下条件：
- T 大于等于 2 且小于等于 {t_max}
- 基础模块 M0 是序列 S 的最小重复教学单元（不存在更短的循环排课）
- 总课时序列长度 {n} 正好是 T 的整数倍

你的目标是通过评估查询，推断出这个基础教学模块 M0 及其课时数 T。

每次你可以提交一个"教案区间比对"，格式如下：
- 指定一个课时区间 [L, R]（L 和 R 都是课时编号，从 1 到 {n}）
- 提供一个候选活动串 X（长度至少为 2）

系统会告诉你：在区间 [L, R] 内，是否存在某个课时开始的连续教学安排恰好等于 X。
- 如果存在，回答"是"
- 如果不存在，回答"否"

注意：
- 区间必须足够容纳候选活动串（R - L + 1 必须大于等于 X 的长度），否则答案必为"否"
- 系统只会返回"是"或"否"，不会告知具体发生课时、重复开展次数等其他信息
- 请尽可能少地使用查询次数

提问时使用以下 XML 格式：

<query>L,R,X</query>

其中 L 和 R 是区间端点（整数），X 是候选活动串（只包含 R、G、B、Y）。

例如，查询课时区间 [1, 10] 内是否执行了连续活动 "RGB"：
<query>1,10,RGB</query>

当你准备好提交最终评估结论时，使用以下格式：

<answer>M0</answer>

其中 M0 是你推断出的基础教学模块串。

例如：
<answer>RGB</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Teaching Module Cycle Recognition" assessment task. Here are the rules:

The academic system has recorded a standardized learning activity sequence S of length {n}, composed of activity codes {{R, G, B, Y}} (representing Reading, Group work, Board work, and Yielding/Extension activities).

This curriculum design follows a strict cyclical logic: it is formed by repeatedly scheduling a minimal "base teaching module" M0. For example, if the base module is "RGB", the entire semester sequence would be "RGBRGBRGB...". The number of periods T for module M0 is unknown, but satisfies the following conditions:
- T is greater than or equal to 2 and less than or equal to {t_max}
- The base module M0 is the minimal repeating teaching unit of sequence S (no shorter cyclical schedule exists)
- The total sequence length {n} is exactly a multiple of T

Your goal is to infer the base teaching module M0 and its length T through assessment queries.

Each time you can submit a "lesson plan interval comparison" in the following format:
- Specify a period interval [L, R] (L and R are period indices from 1 to {n})
- Provide a candidate activity string X (length at least 2)

The system will tell you: whether there exists a continuous teaching schedule starting at some period within interval [L, R] that exactly equals X.
- If it exists, answer "Yes"
- If it doesn't exist, answer "No"

Note:
- The interval must be large enough to contain the candidate activity string (R - L + 1 must be greater than or equal to the length of X), otherwise the answer will be "No"
- The system will only return "Yes" or "No", without revealing specific occurrence periods, execution frequencies, or other information
- Please use as few query attempts as possible

For queries, use the following XML format:

<query>L,R,X</query>

Where L and R are interval endpoints (integers), and X is the candidate activity string (containing only R, G, B, Y).

For example, to query whether the continuous activity "RGB" was executed within period interval [1, 10]:
<query>1,10,RGB</query>

When you are ready to submit your final assessment conclusion, use the following format:

<answer>M0</answer>

Where M0 is the base teaching module string you inferred.

For example:
<answer>RGB</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项"流水线工序周期识别"排错任务，规则如下：

工厂流水线正在执行一段长度为 {n} 的连续作业序列 S，由 {{R, G, B, Y}} 四种工序指令组成（分别代表铆接、打磨、组装、检验）。

该产线的自动化程序有一个强制标准：它是由一个最小的"标准循环工序" M0 往复执行构成的。例如，如果循环工序是 "RGB"，整条流水线的动作序列就是 "RGBRGBRGB..."。循环工序 M0 的指令数 T 未知，但满足以下条件：
- T 大于等于 2 且小于等于 {t_max}
- 标准循环工序 M0 是序列 S 的最小重复生产单元（不存在更短的动作循环）
- 总作业长度 {n} 正好是 T 的整数倍

你的目标是通过设备调试查询，推断出这个标准循环工序 M0 及其指令数 T。

每次你可以提交一个"作业区间校验"，格式如下：
- 指定一个流水位区间 [L, R]（L 和 R 都是流水位编号，从 1 到 {n}）
- 提供一个候选指令串 X（长度至少为 2）

中控台会告诉你：在区间 [L, R] 内，是否存在某个位置开始的连续加工动作恰好等于 X。
- 如果存在，回答"是"
- 如果不存在，回答"否"

注意：
- 区间必须足够容纳候选指令串（R - L + 1 必须大于等于 X 的长度），否则答案必为"否"
- 中控台只会返回"是"或"否"，不会告知具体发生工位、合格率等其他制造数据
- 请尽可能少地使用调试查询次数

提问时使用以下 XML 格式：

<query>L,R,X</query>

其中 L 和 R 是区间端点（整数），X 是候选指令串（只包含 R、G、B、Y）。

例如，查询流水位区间 [1, 10] 内是否执行了连续动作 "RGB"：
<query>1,10,RGB</query>

当你准备好提交最终排错报告时，使用以下格式：

<answer>M0</answer>

其中 M0 是你推断出的标准循环工序串。

例如：
<answer>RGB</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct an "Assembly Line Process Cycle Recognition" troubleshooting task. Here are the rules:

The factory assembly line is executing a continuous operation sequence S of length {n}, composed of process instruction codes {{R, G, B, Y}} (representing Riveting, Grinding, Bending, and Yielding/Testing).

This automated production line has a strict standard: it is formed by repeatedly executing a minimal "standard production cycle" M0. For example, if the production cycle is "RGB", the entire assembly line action sequence would be "RGBRGBRGB...". The number of instructions T in cycle M0 is unknown, but satisfies the following conditions:
- T is greater than or equal to 2 and less than or equal to {t_max}
- The standard production cycle M0 is the minimal repeating production unit of sequence S (no shorter action loop exists)
- The total operation length {n} is exactly a multiple of T

Your goal is to infer the standard production cycle M0 and its instruction count T through equipment debugging queries.

Each time you can submit an "operation interval validation" in the following format:
- Specify an assembly station interval [L, R] (L and R are station indices from 1 to {n})
- Provide a candidate instruction string X (length at least 2)

The central console will tell you: whether there exists a continuous processing action starting at some station within interval [L, R] that exactly equals X.
- If it exists, answer "Yes"
- If it doesn't exist, answer "No"

Note:
- The interval must be large enough to contain the candidate instruction string (R - L + 1 must be greater than or equal to the length of X), otherwise the answer will be "No"
- The central console will only return "Yes" or "No", without revealing specific executing stations, yield rates, or other manufacturing data
- Please use as few debugging queries as possible

For queries, use the following XML format:

<query>L,R,X</query>

Where L and R are interval endpoints (integers), and X is the candidate instruction string (containing only R, G, B, Y).

For example, to query whether the continuous action "RGB" was executed within station interval [1, 10]:
<query>1,10,RGB</query>

When you are ready to submit your final troubleshooting report, use the following format:

<answer>M0</answer>

Where M0 is the standard production cycle string you inferred.

For example:
<answer>RGB</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项"合规审查程序识别"审计任务，规则如下：

案卷系统中记录了一套长度为 {n} 的审计流转序列 S，由 {{R, G, B, Y}} 四类审查节点代码组成（分别代表复核、授权、封存、移交）。

该审计流程具有严格的周期性标准：它是由某个最小的"基础合规闭环" M0 重复执行构成的。例如，如果合规闭环是 "RGB"，整个案卷流转就是 "RGBRGBRGB..."。合规闭环 M0 的步骤数 T 未知，但满足以下条件：
- T 大于等于 2 且小于等于 {t_max}
- 基础合规闭环 M0 是序列 S 的最小重复操作单元（不存在更短的有效审查周期）
- 总节点数 {n} 正好是 T 的整数倍

你的目标是通过调阅查询，推断出这个基础合规闭环 M0 及其步骤数 T。

每次你可以提交一个"程序区间审查"，格式如下：
- 指定一个节点区间 [L, R]（L 和 R 都是流转节点编号，从 1 到 {n}）
- 提供一个候选流程串 X（长度至少为 2）

审计系统会告诉你：在区间 [L, R] 内，是否存在某个节点开始的连续流转动作恰好等于 X。
- 如果存在，回答"是"
- 如果不存在，回答"否"

注意：
- 区间必须足够容纳候选流程串（R - L + 1 必须大于等于 X 的长度），否则答案必为"否"
- 系统只会返回"是"或"否"，不会告知具体发生案卷号、责任人等其他法务信息
- 请尽可能少地发起调阅查询

提问时使用以下 XML 格式：

<query>L,R,X</query>

其中 L 和 R 是区间端点（整数），X 是候选流程串（只包含 R、G、B、Y）。

例如，查询流转节点区间 [1, 10] 内是否存在连续程序 "RGB"：
<query>1,10,RGB</query>

当你准备好提交最终审计结果时，使用以下格式：

<answer>M0</answer>

其中 M0 是你推断出的基础合规闭环串。

例如：
<answer>RGB</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Compliance Review Process Recognition" audit task. Here are the rules:

The case management system has recorded an audit workflow sequence S of length {n}, composed of review node codes {{R, G, B, Y}} (representing Review, Grant, Ban, and Yield/Transfer).

This auditing process has a strict periodic standard: it is formed by repeatedly executing a minimal "base compliance loop" M0. For example, if the compliance loop is "RGB", the entire case workflow would be "RGBRGBRGB...". The number of steps T in loop M0 is unknown, but satisfies the following conditions:
- T is greater than or equal to 2 and less than or equal to {t_max}
- The base compliance loop M0 is the minimal repeating operational unit of sequence S (no shorter valid review cycle exists)
- The total node count {n} is exactly a multiple of T

Your goal is to infer the base compliance loop M0 and its step count T through record queries.

Each time you can submit a "procedure interval review" in the following format:
- Specify a node interval [L, R] (L and R are workflow node indices from 1 to {n})
- Provide a candidate process string X (length at least 2)

The auditing system will tell you: whether there exists a continuous workflow action starting at some node within interval [L, R] that exactly equals X.
- If it exists, answer "Yes"
- If it doesn't exist, answer "No"

Note:
- The interval must be large enough to contain the candidate process string (R - L + 1 must be greater than or equal to the length of X), otherwise the answer will be "No"
- The system will only return "Yes" or "No", without revealing specific case numbers, responsible persons, or other legal information
- Please initiate as few record queries as possible

For queries, use the following XML format:

<query>L,R,X</query>

Where L and R are interval endpoints (integers), and X is the candidate process string (containing only R, G, B, Y).

For example, to query whether the continuous procedure "RGB" exists within node interval [1, 10]:
<query>1,10,RGB</query>

When you are ready to submit your final audit result, use the following format:

<answer>M0</answer>

Where M0 is the base compliance loop string you inferred.

For example:
<answer>RGB</answer>
"""

    tags = ["answer", "query"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "t_max": 6,
                "base_block": "RG",
            },
            2: {
                "n": 15,
                "t_max": 7,
                "base_block": "RGB",
            },
            3: {
                "n": 20,
                "t_max": 10,
                "base_block": "RGYB",
            },
            4: {
                "n": 25,
                "t_max": 12,
                "base_block": "RGBYR",
            },
            5: {
                "n": 30,
                "t_max": 15,
                "base_block": "RGBYYR",
            },
        },
        "en": {
            1: {
                "n": 12,
                "t_max": 6,
                "base_block": "RG",
            },
            2: {
                "n": 15,
                "t_max": 7,
                "base_block": "RGB",
            },
            3: {
                "n": 20,
                "t_max": 10,
                "base_block": "RGYB",
            },
            4: {
                "n": 25,
                "t_max": 12,
                "base_block": "RGBYR",
            },
            5: {
                "n": 30,
                "t_max": 15,
                "base_block": "RGBYYR",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["t_max"] = cfg["t_max"]
        
        block = cfg["base_block"]
        block_len = len(block)
        
        for sub_len in range(1, block_len):
            if block_len % sub_len == 0:
                sub_block = block[:sub_len]
                if sub_block * (block_len // sub_len) == block:
                    raise ValueError(
                        f"Configured base_block '{block}' is not minimal: "
                        f"it has a shorter period '{sub_block}'"
                    )
        
        self.base_block = block
        self.t = len(self.base_block)
        
        if cfg["n"] % self.t != 0:
            raise ValueError(f"N={cfg['n']} must be a multiple of T={self.t}")
        
        self.k = cfg["n"] // self.t
        self.hidden_sequence = self.base_block * self.k
        
        assert len(self.hidden_sequence) == cfg["n"], "Sequence length mismatch"

    def evaluate(self, parsed_info):
        submitted_block = parsed_info["answer"].strip()
        
        if submitted_block != self.base_block:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。请使用格式 <query>L,R,X</query>"
            error_range = "错误：区间超出范围或无效。"
            error_string = "错误：候选串只能包含字母 R、G、B、Y。"
            error_length = "错误：候选串长度必须至少为 2。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format. Please use format <query>L,R,X</query>"
            error_range = "Error: Interval out of range or invalid."
            error_string = "Error: Candidate string can only contain letters R, G, B, Y."
            error_length = "Error: Candidate string length must be at least 2."

        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        query_content = parsed_info["query"].strip()
        parts = query_content.split(",", 2)
        
        if len(parts) != 3:
            return error_format
        
        l_str, r_str, x = parts
        
        try:
            L = int(l_str.strip())
            R = int(r_str.strip())
        except ValueError:
            return error_format
        
        X = x.strip()
        
        if not all(c in "RGBY" for c in X):
            return error_string
        
        if len(X) < 2:
            return error_length
        
        if L < 1 or R > self._game_info["n"] or L > R:
            return error_range
        
        if R - L + 1 < len(X):
            return no_res
        
        interval_start = L - 1
        interval_end = R
        
        substring = self.hidden_sequence[interval_start:interval_end]
        
        if X in substring:
            return yes_res
        else:
            return no_res

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = self._game_info["n"]
        vocab = ['R', 'G', 'B', 'Y']
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        candidate_xs = []
        for length in [2, 3]:
            for p in itertools.product(vocab, repeat=length):
                candidate_xs.append("".join(p))
        
        for X in candidate_xs:
            interval_substring = self.hidden_sequence
            ans = yes_res if X in interval_substring else no_res
            results.append({
                "query": f"<query>1,{n},{X}</query>",
                "answer": ans
            })
        
        t = self.t
        for start_block in range(self.k):
            L = start_block * t + 1
            R = min(L + 2 * t - 1, n)
            interval_substring = self.hidden_sequence[L-1:R]
            for X in candidate_xs:
                if R - L + 1 < len(X):
                    continue
                ans = yes_res if X in interval_substring else no_res
                results.append({
                    "query": f"<query>{L},{R},{X}</query>",
                    "answer": ans
                })
        
        seen = set()
        deduped = []
        for item in results:
            key = (item["query"], item["answer"])
            if key not in seen:
                seen.add(key)
                deduped.append(item)
        
        return deduped

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        mapping = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes",
            "YES": "NO",
            "NO": "YES",
            "yes": "no",
            "no": "yes"
        }
        
        if correct in mapping:
            return mapping[correct]
        
        return correct + "_WRONG"