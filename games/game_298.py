from .base import Game
import re

class EquivalenceLCSGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"等价关系下的LCS推理"游戏，规则如下：

游戏设定了一个字母表 Σ = {{A, B, C, D}}。我已秘密选定了一个等价关系 E，它将这四个字母分组。可能的等价关系有四种：
- 类型α：每个字母自成一组
- 类型β：{{A,B}} 和 {{C,D}} 两组
- 类型γ：{{A,C}} 和 {{B,D}} 两组
- 类型δ：{{A,D}} 和 {{B,C}} 两组

同时，我已经固定了两条序列 S 和 T：
- S = {s}
- T = {t}

在等价关系 E 下，两个序列 X 和 Y 的最长公共子序列长度 LCS_E(X,Y) 定义为：找到 X 和 Y 中最长的一对子序列（保持原顺序），使得对应位置的字母在等价关系 E 下是等价的。

你的任务是：
1. 通过探测来推断出隐藏的等价关系类型（α/β/γ/δ）
2. 计算在该等价关系下，S 和 T 的 LCS_E(S,T) 值

你可以进行探测，每次探测提交两条序列 X 和 Y，我会返回在隐藏等价关系下的 LCS_E(X,Y) 值。

限制条件：
- 每条序列的长度不超过 12
- 序列中的字母必须来自 {{A, B, C, D}}
- 你必须进行至少 2 次探测，最多 6 次探测
- 如果出现 2 次非法输入，游戏直接失败

进行探测时，使用以下 XML 格式：

<query_probe>X,Y</query_probe>

例如，探测序列 "ABC" 和 "BCD"：
<query_probe>ABC,BCD</query_probe>

提交最终答案时，必须说明等价关系类型（α/β/γ/δ）和 LCS_E(S,T) 的值，格式如下：

<answer>type=β, lcs=5</answer>

注意：必须在完成至少 2 次且不超过 6 次探测后才能提交答案。请尽可能少地使用探测次数。
"""

    game_rule_en = """\
Let's play an "Equivalence Relation LCS Deduction" game. Here are the rules:

The game uses an alphabet Σ = {{A, B, C, D}}. I have secretly chosen an equivalence relation E that groups these four letters. There are four possible equivalence relations:
- Type α: Each letter forms its own group
- Type β: {{A,B}} and {{C,D}} as two groups
- Type γ: {{A,C}} and {{B,D}} as two groups
- Type δ: {{A,D}} and {{B,C}} as two groups

Additionally, I have fixed two sequences S and T:
- S = {s}
- T = {t}

Under equivalence relation E, the longest common subsequence length LCS_E(X,Y) of two sequences X and Y is defined as: finding the longest pair of subsequences (maintaining original order) from X and Y such that corresponding positions contain letters that are equivalent under relation E.

Your task is:
1. Deduce the hidden equivalence relation type (α/β/γ/δ) through probing
2. Calculate LCS_E(S,T) under that equivalence relation

You can perform probes. Each probe submits two sequences X and Y, and I will return the LCS_E(X,Y) value under the hidden equivalence relation.

Constraints:
- Each sequence length must not exceed 12
- Sequence letters must be from {{A, B, C, D}}
- You must perform at least 2 probes and at most 6 probes
- If 2 invalid inputs occur, the game fails immediately

To perform a probe, use the following XML format:

<query_probe>X,Y</query_probe>

For example, to probe sequences "ABC" and "BCD":
<query_probe>ABC,BCD</query_probe>

When submitting the final answer, specify the equivalence relation type (α/β/γ/δ) and the LCS_E(S,T) value using this format:

<answer>type=β, lcs=5</answer>

Note: You must submit the answer after completing at least 2 and at most 6 probes. Use as few probes as possible.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通系统车道兼容性分析”终端。游戏设定了一个车辆分类系统 Σ = {{A, B, C, D}}，分别代表：A(电动轿车)、B(燃油轿车)、C(电动SUV)、D(燃油SUV)。
我已在后台秘密设定了当前收费站的“车道合并规则”（等价关系 E）。可能存在四种合并规则：
- 类型α：每种车辆必须使用专属车道（各自独立）
- 类型β：按车型合并车道（{{A,B}} 轿车组，{{C,D}} SUV组）
- 类型γ：按动力类型合并车道（{{A,C}} 电动组，{{B,D}} 燃油组）
- 类型δ：特殊潮汐混合车道（{{A,D}} 和 {{B,C}} 两组）

同时，系统锁定了两个待处理的主车队序列 S 和 T：
- S = {s}
- T = {t}

在当前的合并规则 E 下，两个车队序列 X 和 Y 的最大同步放行长度 LCS_E(X,Y) 定义为：在保持原车队顺序的前提下，找到 X 和 Y 中最长的一对子序列，使得对应位置的车辆在规则 E 下可以共用同一个收费站车道。

你的任务是：
1. 通过发送测试车队进行探测，推断出隐藏的车道合并规则类型（α/β/γ/δ）
2. 计算在该规则下，主车队 S 和 T 的最大同步放行长度 LCS_E(S,T)

你可以进行探测，每次探测提交两支测试车队序列 X 和 Y，系统会返回在隐藏合并规则下的 LCS_E(X,Y) 值。

限制条件：
- 每支测试车队的长度不超过 12
- 车队序列中的车辆代号必须来自 {{A, B, C, D}}
- 你必须进行至少 2 次探测，最多 6 次探测
- 如果出现 2 次非法输入，系统分析将直接失败

进行探测时，使用以下 XML 格式：

<query_probe>X,Y</query_probe>

例如，探测测试车队序列 "ABC" 和 "BCD"：
<query_probe>ABC,BCD</query_probe>

提交最终答案时，必须说明合并规则类型（α/β/γ/δ）和 LCS_E(S,T) 的值，格式如下：

<answer>type=β, lcs=5</answer>

注意：必须在完成至少 2 次且不超过 6 次探测后才能提交答案。请尽可能少地使用探测次数。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Intelligent Traffic Lane Compatibility Analysis" terminal. The system defines a vehicle classification alphabet Σ = {{A, B, C, D}}, representing: A (Electric Sedan), B (Fuel Sedan), C (Electric SUV), and D (Fuel SUV).
I have secretly set the "Lane Merging Rule" (equivalence relation E) for the current toll gate. There are four possible merging rules:
- Type α: Each vehicle type requires a dedicated lane (independent)
- Type β: Merged by vehicle body type ({{A,B}} Sedans, {{C,D}} SUVs)
- Type γ: Merged by power source ({{A,C}} Electric, {{B,D}} Fuel)
- Type δ: Special tidal mixed lanes ({{A,D}} and {{B,C}})

Meanwhile, I have locked two main incoming convoy sequences S and T:
- S = {s}
- T = {t}

Under merging rule E, the maximum synchronized dispatch length LCS_E(X,Y) of two convoy sequences X and Y is defined as: finding the longest pair of subsequences (maintaining original order) from X and Y such that corresponding vehicles can share a lane under rule E.

Your task is:
1. Deduce the hidden lane merging rule type (α/β/γ/δ) through probing with test convoys
2. Calculate LCS_E(S,T) for the main convoys S and T under that rule

You can perform probes. Each probe submits two test convoy sequences X and Y, and the system will return the LCS_E(X,Y) value under the hidden lane merging rule.

Constraints:
- Each sequence length must not exceed 12
- Sequence vehicle codes must be from {{A, B, C, D}}
- You must perform at least 2 probes and at most 6 probes
- If 2 invalid inputs occur, the analysis fails immediately

To perform a probe, use the following XML format:

<query_probe>X,Y</query_probe>

For example, to probe test convoy sequences "ABC" and "BCD":
<query_probe>ABC,BCD</query_probe>

When submitting the final answer, specify the lane merging rule type (α/β/γ/δ) and the LCS_E(S,T) value using this format:

<answer>type=β, lcs=5</answer>

Note: You must submit the answer after completing at least 2 and at most 6 probes. Use as few probes as possible.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“医疗临床方案相容性推演”系统。系统定义了四种核心药物成分 Σ = {{A, B, C, D}}，分别为：A(口服抗生素)、B(注射抗生素)、C(口服抗病毒药)、D(注射抗病毒药)。
我已秘密设定了这四种药物的“受体代谢同源规则”（等价关系 E）。可能的同源规则有四种：
- 类型α：每种药物均具有独特的代谢途径（独立且不互通）
- 类型β：按药效类别共享途径（{{A,B}} 抗细菌组，{{C,D}} 抗病毒组）
- 类型γ：按给药途径共享代谢（{{A,C}} 口服组，{{B,D}} 注射组）
- 类型δ：特定靶向交叉代谢（{{A,D}} 和 {{B,C}} 两组）

当前选定了两组标准临床治疗序列 S 和 T：
- S = {s}
- T = {t}

在同源规则 E 下，两个治疗序列 X 和 Y 的最大同步治疗里程 LCS_E(X,Y) 定义为：找到 X 和 Y 中最长的一对子序列（保持给药顺序），使得对应位置的药物在规则 E 下共享相同的代谢途径。

你的任务是：
1. 通过提交测试序列来推断隐藏的代谢同源规则类型（α/β/γ/δ）
2. 计算在该规则下，方案 S 和 T 的最大同步治疗里程 LCS_E(S,T)

你可以进行探测，每次探测提交两组测试序列 X 和 Y，系统会返回在隐藏同源规则下的 LCS_E(X,Y) 值。

限制条件：
- 每组序列的长度不超过 12
- 序列中的药物代号必须来自 {{A, B, C, D}}
- 你必须进行至少 2 次探测，最多 6 次探测
- 如果出现 2 次非法输入，推演将直接失败

进行探测时，使用以下 XML 格式：

<query_probe>X,Y</query_probe>

例如，探测序列 "ABC" 和 "BCD"：
<query_probe>ABC,BCD</query_probe>

提交最终答案时，必须说明同源规则类型（α/β/γ/δ）和 LCS_E(S,T) 的值，格式如下：

<answer>type=β, lcs=5</answer>

注意：必须在完成至少 2 次且不超过 6 次探测后才能提交答案。请尽可能少地使用探测次数。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Clinical Regimen Compatibility Deduction" system. The system defines four core drug components Σ = {{A, B, C, D}}: A (Oral Antibiotic), B (IV Antibiotic), C (Oral Antiviral), and D (IV Antiviral).
I have secretly chosen a "Metabolic Pathway Homology Rule" (equivalence relation E). There are four possible rules:
- Type α: Each drug has a unique, independent pathway
- Type β: Grouped by therapeutic effect ({{A,B}} Antibacterial, {{C,D}} Antiviral)
- Type γ: Grouped by administration route ({{A,C}} Oral, {{B,D}} Intravenous)
- Type δ: Specific targeted cross-metabolism ({{A,D}} and {{B,C}})

Two standard clinical treatment sequences S and T are fixed:
- S = {s}
- T = {t}

Under homology rule E, the maximum synchronized therapeutic milestone length LCS_E(X,Y) of two regimens X and Y is defined as: finding the longest pair of subsequences (maintaining administration order) such that corresponding drugs share the same metabolic pathway under rule E.

Your task is:
1. Deduce the hidden metabolic homology rule type (α/β/γ/δ) through probing with test sequences
2. Calculate LCS_E(S,T) under that rule for S and T

You can perform probes. Each probe submits two test sequences X and Y, and the system will return the LCS_E(X,Y) value under the hidden homology rule.

Constraints:
- Each sequence length must not exceed 12
- Sequence drug codes must be from {{A, B, C, D}}
- You must perform at least 2 probes and at most 6 probes
- If 2 invalid inputs occur, the deduction fails immediately

To perform a probe, use the following XML format:

<query_probe>X,Y</query_probe>

For example, to probe sequences "ABC" and "BCD":
<query_probe>ABC,BCD</query_probe>

When submitting the final answer, specify the homology rule type (α/β/γ/δ) and the LCS_E(S,T) value using this format:

<answer>type=β, lcs=5</answer>

Note: You must submit the answer after completing at least 2 and at most 6 probes. Use as few probes as possible.
"""

    contextualized_rule_zh_3 = """\
欢迎来到“教务系统跨学科分互认”平台。平台设定了四个核心课程模块 Σ = {{A, B, C, D}}，对应：A(线上理科)、B(线下理科)、C(线上文科)、D(线下文科)。
系统后台已秘密选定了一种“学分互认策略”（等价关系 E）。可能的互认策略有四种：
- 类型α：严格对口（各模块独立，不进行跨模块互认）
- 类型β：按学科类别互认（{{A,B}} 理科组，{{C,D}} 文科组）
- 类型γ：按授课模式互认（{{A,C}} 线上组，{{B,D}} 线下组）
- 类型δ：实验性交叉互认（{{A,D}} 和 {{B,C}} 两组）

现有两条标准培养方案序列 S 和 T：
- S = {s}
- T = {t}

在互认策略 E 下，两个培养方案 X 和 Y 的最大通用互认学分长度 LCS_E(X,Y) 定义为：在保持修读顺序的前提下，找到 X 和 Y 中最长的一对子序列，使得对应位置的课程模块在策略 E 下可以互认学分。

你的任务是：
1. 提交测试方案以推断隐藏的学分互认策略类型（α/β/γ/δ）
2. 计算在该策略下，方案 S 和 T 的互认长度 LCS_E(S,T)

你可以进行探测，每次探测提交两条测试培养方案 X 和 Y，平台会返回在隐藏互认策略下的 LCS_E(X,Y) 值。

限制条件：
- 每条方案的长度不超过 12
- 方案序列中的模块代号必须来自 {{A, B, C, D}}
- 你必须进行至少 2 次探测，最多 6 次探测
- 如果出现 2 次非法输入，评估将直接失败

进行探测时，使用以下 XML 格式：

<query_probe>X,Y</query_probe>

例如，探测方案 "ABC" 和 "BCD"：
<query_probe>ABC,BCD</query_probe>

提交最终答案时，必须说明互认策略类型（α/β/γ/δ）和 LCS_E(S,T) 的值，格式如下：

<answer>type=β, lcs=5</answer>

注意：必须在完成至少 2 次且不超过 6 次探测后才能提交答案。请尽可能少地使用探测次数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Cross-Disciplinary Credit Transfer" platform. The system defines four core course modules Σ = {{A, B, C, D}}: A (Online Science), B (Offline Science), C (Online Humanities), and D (Offline Humanities).
A "Credit Transfer Strategy" (equivalence relation E) has been secretly selected by the backend. There are four possible strategies:
- Type α: Strict alignment (no cross-module transfers)
- Type β: Grouped by discipline ({{A,B}} Science, {{C,D}} Humanities)
- Type γ: Grouped by delivery mode ({{A,C}} Online, {{B,D}} Offline)
- Type δ: Experimental hybrid transfer ({{A,D}} and {{B,C}})

Two standard curriculum pathways S and T are fixed:
- S = {s}
- T = {t}

Under strategy E, the maximum mutually recognized credit length LCS_E(X,Y) of two pathways X and Y is defined as: finding the longest pair of subsequences (maintaining prerequisite order) such that corresponding modules can be transferred for credit under strategy E.

Your task is:
1. Deduce the hidden credit transfer strategy type (α/β/γ/δ) through probing
2. Calculate LCS_E(S,T) under that strategy for pathways S and T

You can perform probes. Each probe submits two test pathways X and Y, and the platform will return the LCS_E(X,Y) value under the hidden transfer strategy.

Constraints:
- Each pathway length must not exceed 12
- Pathway module codes must be from {{A, B, C, D}}
- You must perform at least 2 probes and at most 6 probes
- If 2 invalid inputs occur, the evaluation fails immediately

To perform a probe, use the following XML format:

<query_probe>X,Y</query_probe>

For example, to probe pathways "ABC" and "BCD":
<query_probe>ABC,BCD</query_probe>

When submitting the final answer, specify the transfer strategy type (α/β/γ/δ) and the LCS_E(S,T) value using this format:

<answer>type=β, lcs=5</answer>

Note: You must submit the answer after completing at least 2 and at most 6 probes. Use as few probes as possible.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“柔性产线工装兼容性”验证系统。物料库中包含四种核心紧固件 Σ = {{A, B, C, D}}，分别为：A(铝制螺栓)、B(钢制螺栓)、C(铝制铆钉)、D(钢制铆钉)。
我已秘密设定了当前产线的“工装快换兼容关系”（等价关系 E）。可能存在四种兼容关系：
- 类型α：专件专机（每种紧固件需独立工装）
- 类型β：按紧固类型兼容（{{A,B}} 螺栓工装，{{C,D}} 铆钉工装）
- 类型γ：按材质属性兼容（{{A,C}} 铝材工装，{{B,D}} 钢材工装）
- 类型δ：定制交叉工装（{{A,D}} 和 {{B,C}} 两组）

当前待排产的两条主要装配指令序列 S 和 T：
- S = {s}
- T = {t}

在兼容关系 E 下，两条装配序列 X 和 Y 的最大无换线并行工序数 LCS_E(X,Y) 定义为：保持原有装配步骤的前提下，找到 X 和 Y 中最长的一对子序列，使得对应位置的紧固件在该产线下可以共用工装。

你的任务是：
1. 投入测试装配序列，探测并推断隐藏的工装兼容关系类型（α/β/γ/δ）
2. 计算在该关系下，主产序列 S 和 T 的 LCS_E(S,T) 值

你可以进行探测，每次探测提交两条测试装配序列 X 和 Y，系统会返回在隐藏兼容关系下的 LCS_E(X,Y) 值。

限制条件：
- 每条序列的长度不超过 12
- 序列中的紧固件代号必须来自 {{A, B, C, D}}
- 你必须进行至少 2 次探测，最多 6 次探测
- 如果出现 2 次非法输入，验证将直接失败

进行探测时，使用以下 XML 格式：

<query_probe>X,Y</query_probe>

例如，探测装配序列 "ABC" 和 "BCD"：
<query_probe>ABC,BCD</query_probe>

提交最终答案时，必须说明兼容关系类型（α/β/γ/δ）和 LCS_E(S,T) 的值，格式如下：

<answer>type=β, lcs=5</answer>

注意：必须在完成至少 2 次且不超过 6 次探测后才能提交答案。请尽可能少地使用探测次数。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Flexible Production Line Tooling Compatibility" system. The inventory contains four core fasteners Σ = {{A, B, C, D}}: A (Aluminum Screws), B (Steel Screws), C (Aluminum Rivets), and D (Steel Rivets).
I have secretly set the "Tooling Quick-Change Compatibility" (equivalence relation E) for the assembly line. There are four possible compatibilities:
- Type α: Strictly independent tooling for each fastener
- Type β: Compatible by fastening method ({{A,B}} Screws, {{C,D}} Rivets)
- Type γ: Compatible by material ({{A,C}} Aluminum, {{B,D}} Steel)
- Type δ: Customized cross-tooling ({{A,D}} and {{B,C}})

Two main batches of assembly sequences S and T are pending:
- S = {s}
- T = {t}

Under compatibility E, the maximum parallel operation length without re-tooling LCS_E(X,Y) of two sequences X and Y is defined as: finding the longest pair of subsequences (maintaining assembly order) such that corresponding fasteners can share tooling under E.

Your task is:
1. Deduce the hidden tooling compatibility type (α/β/γ/δ) by probing test sequences
2. Calculate LCS_E(S,T) for the main batches S and T

You can perform probes. Each probe submits two test assembly sequences X and Y, and the system will return the LCS_E(X,Y) value under the hidden compatibility.

Constraints:
- Each sequence length must not exceed 12
- Sequence fastener codes must be from {{A, B, C, D}}
- You must perform at least 2 probes and at most 6 probes
- If 2 invalid inputs occur, the verification fails immediately

To perform a probe, use the following XML format:

<query_probe>X,Y</query_probe>

For example, to probe sequences "ABC" and "BCD":
<query_probe>ABC,BCD</query_probe>

When submitting the final answer, specify the compatibility type (α/β/γ/δ) and the LCS_E(S,T) value using this format:

<answer>type=β, lcs=5</answer>

Note: You must submit the answer after completing at least 2 and at most 6 probes. Use as few probes as possible.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法判例适用性推演”系统。法条库划分为四个核心领域 Σ = {{A, B, C, D}}，代表：A(企业税法)、B(个人税法)、C(企业劳动法)、D(个人劳动法)。
系统已秘密确立了当前法庭的“司法解释等效关系”（等价关系 E）。四种可能的等效关系为：
- 类型α：严格字面适用（每种法条独立解释）
- 类型β：按法律部门等效（{{A,B}} 税法解释，{{C,D}} 劳动法解释）
- 类型γ：按适用主体等效（{{A,C}} 企业解释，{{B,D}} 个人解释）
- 类型δ：特定历史判例交叉等效（{{A,D}} 和 {{B,C}} 两组）

现有原被告双方提交的两份主要辩护逻辑序列 S 和 T：
- S = {s}
- T = {t}

在等效关系 E 下，两份逻辑序列 X 和 Y 的最大法理共识长度 LCS_E(X,Y) 定义为：在保持辩护先后顺序的情况下，找到 X 和 Y 中最长的一对子序列，使得对应位置引用的法条在关系 E 下属于等效解释。

你的任务是：
1. 通过向系统提交假设辩护序列，推断出隐藏的等效关系类型（α/β/γ/δ）
2. 计算在该关系下，真实序列 S 和 T 的共识长度 LCS_E(S,T)

你可以进行探测，每次探测提交两份假设辩护序列 X 和 Y，系统会返回在隐藏等效关系下的 LCS_E(X,Y) 值。

限制条件：
- 每份序列的长度不超过 12
- 序列中的法条代号必须来自 {{A, B, C, D}}
- 你必须进行至少 2 次探测，最多 6 次探测
- 如果出现 2 次非法输入，推演将直接失败

进行探测时，使用以下 XML 格式：

<query_probe>X,Y</query_probe>

例如，探测辩护序列 "ABC" 和 "BCD"：
<query_probe>ABC,BCD</query_probe>

提交最终答案时，必须说明等效关系类型（α/β/γ/δ）和 LCS_E(S,T) 的值，格式如下：

<answer>type=β, lcs=5</answer>

注意：必须在完成至少 2 次且不超过 6 次探测后才能提交答案。请尽可能少地使用探测次数。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Precedent Applicability Deduction" system. The legal database is divided into four domains Σ = {{A, B, C, D}}: A (Corporate Tax Law), B (Individual Tax Law), C (Corporate Labor Law), and D (Individual Labor Law).
The court's "Judicial Interpretation Equivalence" (equivalence relation E) has been secretly established. There are four possible equivalences:
- Type α: Strict literal application (each clause interpreted independently)
- Type β: Equivalent by legal branch ({{A,B}} Tax, {{C,D}} Labor)
- Type γ: Equivalent by target entity ({{A,C}} Corporate, {{B,D}} Individual)
- Type δ: Specific cross-interpretation based on historical precedent ({{A,D}} and {{B,C}})

Two main sequences of legal arguments S and T submitted by plaintiff and defendant are fixed:
- S = {s}
- T = {t}

Under equivalence E, the maximum jurisprudential consensus length LCS_E(X,Y) of two argument sequences X and Y is defined as: finding the longest pair of subsequences (maintaining argument order) such that corresponding cited clauses are equivalent under E.

Your task is:
1. Deduce the hidden judicial equivalence type (α/β/γ/δ) by submitting hypothetical arguments
2. Calculate LCS_E(S,T) for the actual arguments S and T

You can perform probes. Each probe submits two hypothetical argument sequences X and Y, and the system will return the LCS_E(X,Y) value under the hidden equivalence.

Constraints:
- Each sequence length must not exceed 12
- Sequence clause codes must be from {{A, B, C, D}}
- You must perform at least 2 probes and at most 6 probes
- If 2 invalid inputs occur, the deduction fails immediately

To perform a probe, use the following XML format:

<query_probe>X,Y</query_probe>

For example, to probe argument sequences "ABC" and "BCD":
<query_probe>ABC,BCD</query_probe>

When submitting the final answer, specify the equivalence type (α/β/γ/δ) and the LCS_E(S,T) value using this format:

<answer>type=β, lcs=5</answer>

Note: You must submit the answer after completing at least 2 and at most 6 probes. Use as few probes as possible.
"""

    tags = ["answer", "query_probe"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "s": "ABCD",
                "t": "DCBA",
                "equiv_type": "α",
            },
            2: {
                "s": "AABBCC",
                "t": "BBCCDD",
                "equiv_type": "β",
            },
            3: {
                "s": "ABCDABCD",
                "t": "CDABCDAB",
                "equiv_type": "γ",
            },
            4: {
                "s": "AABCDDCBAA",
                "t": "DDABCCBADD",
                "equiv_type": "δ",
            },
            5: {
                "s": "ABCDABCDABCD",
                "t": "DCBADCBADCBA",
                "equiv_type": "β",
            },
        },
        "en": {
            1: {
                "s": "ABCD",
                "t": "DCBA",
                "equiv_type": "α",
            },
            2: {
                "s": "AABBCC",
                "t": "BBCCDD",
                "equiv_type": "β",
            },
            3: {
                "s": "ABCDABCD",
                "t": "CDABCDAB",
                "equiv_type": "γ",
            },
            4: {
                "s": "AABCDDCBAA",
                "t": "DDABCCBADD",
                "equiv_type": "δ",
            },
            5: {
                "s": "ABCDABCDABCD",
                "t": "DCBADCBADCBA",
                "equiv_type": "β",
            },
        },
    }

    def __init__(self, config):
        self.probe_count = 0
        self.invalid_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["s"] = cfg["s"]
        self._game_info["t"] = cfg["t"]
        self.s_seq = cfg["s"]
        self.t_seq = cfg["t"]
        self.equiv_type = cfg["equiv_type"]
        
        self.equivalence_relations = {
            "α": {"A": {"A"}, "B": {"B"}, "C": {"C"}, "D": {"D"}},
            "β": {"A": {"A", "B"}, "B": {"A", "B"}, "C": {"C", "D"}, "D": {"C", "D"}},
            "γ": {"A": {"A", "C"}, "B": {"B", "D"}, "C": {"A", "C"}, "D": {"B", "D"}},
            "δ": {"A": {"A", "D"}, "B": {"B", "C"}, "C": {"B", "C"}, "D": {"A", "D"}},
        }
        
        self.correct_lcs = self._compute_lcs(self.s_seq, self.t_seq, self.equiv_type)

    def _is_equivalent(self, char1, char2, equiv_type):
        if char1 not in self.equivalence_relations[equiv_type]:
            return False
        return char2 in self.equivalence_relations[equiv_type][char1]

    def _compute_lcs(self, seq1, seq2, equiv_type):
        n, m = len(seq1), len(seq2)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if self._is_equivalent(seq1[i-1], seq2[j-1], equiv_type):
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[n][m]

    def _validate_sequence(self, seq):
        if len(seq) > 12:
            return False
        valid_chars = set("ABCD")
        return all(c in valid_chars for c in seq)

    def evaluate(self, parsed_info):
        if self.probe_count < 2 or self.probe_count > 6:
            return False
        
        raw_ans = parsed_info["answer"]
        
        type_match = re.search(r'type\s*=\s*([αβγδ])', raw_ans)
        lcs_match = re.search(r'lcs\s*=\s*(\d+)', raw_ans)
        
        if not type_match or not lcs_match:
            return False
        
        ans_type = type_match.group(1)
        ans_lcs = int(lcs_match.group(1))
        
        if ans_type != self.equiv_type:
            return False
        
        return ans_lcs == self.correct_lcs

    def _cf_core_produce(self, parsed_info):
        if "query_probe" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        if self.probe_count >= 6:
            if self.config.language == "zh":
                return "错误：已达到最大探测次数（6次）。请提交最终答案。"
            else:
                return "Error: Maximum probe count (6) reached. Please submit final answer."
        
        raw_query = parsed_info["query_probe"]
        
        try:
            parts = raw_query.split(",")
            if len(parts) != 2:
                raise ValueError("Invalid format")
            
            seq_x = parts[0].strip().upper()
            seq_y = parts[1].strip().upper()
            
            if not self._validate_sequence(seq_x) or not self._validate_sequence(seq_y):
                self.invalid_count += 1
                if self.invalid_count >= 2:
                    self.state.set_state("failed", "too many invalid inputs")
                    if self.config.language == "zh":
                        return "错误：非法输入次数过多，游戏失败。"
                    else:
                        return "Error: Too many invalid inputs. Game failed."
                
                if self.config.language == "zh":
                    return "输入非法：序列长度不能超过12，且字母必须来自{A,B,C,D}。"
                else:
                    return "Invalid input: Sequence length must not exceed 12, and letters must be from {A,B,C,D}."
            
            self.probe_count += 1
            lcs_value = self._compute_lcs(seq_x, seq_y, self.equiv_type)
            
            return str(lcs_value)
            
        except Exception as e:
            self.invalid_count += 1
            if self.invalid_count >= 2:
                self.state.set_state("failed", "too many invalid inputs")
                if self.config.language == "zh":
                    return "错误：非法输入次数过多，游戏失败。"
                else:
                    return "Error: Too many invalid inputs. Game failed."
            
            if self.config.language == "zh":
                return "输入非法：格式错误。请使用格式 <query_probe>X,Y</query_probe>"
            else:
                return "Invalid input: Format error. Please use format <query_probe>X,Y</query_probe>"

    def _cf_make_wrong(self, correct):
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            try:
                val = int(correct)
                return str(val + 1)
            except ValueError:
                pass

        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            def replace_case_insensitive(match):
                word = match.group(0)
                lower_word = word.lower()
                target = "no" if lower_word == "yes" else "yes"
                
                if word.isupper():
                    return target.upper()
                elif word[0].isupper():
                    return target.capitalize()
                else:
                    return target

            if re.search(r'\b(yes|no)\b', correct, re.IGNORECASE):
                return re.sub(r'\b(yes|no)\b', replace_case_insensitive, correct, flags=re.IGNORECASE)

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        chars = ["A", "B", "C", "D"]
        
        for c1 in chars:
            for c2 in chars:
                query_str = f"{c1},{c2}"
                
                lcs_val = self._compute_lcs(c1, c2, self.equiv_type)
                
                queries.append({
                    "query": query_str,
                    "answer": str(lcs_val)
                })
        
        return queries