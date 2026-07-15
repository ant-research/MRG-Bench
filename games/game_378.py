from .base import Game

class PeriodicSequenceGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"周期序列推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的二元序列 S，每个位置的值只能是 0 或 1。这个序列具有特殊的生成方式：存在一个未知的基础块 M（块长度记为 b），通过将 M 重复拼接若干次得到完整序列 S。

已知信息：
- 序列总长度 N = {n}
- 基础块长度 b 满足：1 < b ≤ {bmax}，且 b 能整除 N
- 基础块 M 中至少包含一个 1
- 你最多可以进行 {max_queries} 次查询

未知信息：
- 基础块的具体长度 b
- 基础块 M 的具体内容
- 完整序列 S 的内容

你的目标是：推断出序列 S 中所有 1 的总数量 C。

你可以使用以下三种查询方式（每次查询计为一次，请尽可能少地使用查询次数）：

1. 查看查询：询问序列中第 i 个位置的值是 0 还是 1（位置编号从 1 到 {n}）
2. 比较查询：询问第 i 个位置和第 j 个位置的值是否相同
3. 验证周期查询：询问某个长度 k 是否为序列的周期（即对于所有有效位置 p，S[p] 是否等于 S[p+k]）

每次只能进行一种查询。请使用以下 XML 格式：

- 查看查询（例如查看第 5 个位置）：
<query_view>5</query_view>

- 比较查询（例如比较第 3 和第 7 个位置）：
<query_compare>3,7</query_compare>

- 验证周期查询（例如验证周期长度为 4）：
<query_period>4</query_period>

提交最终答案时，请直接给出序列中 1 的总数量，格式如下：

<answer>12</answer>

注意：如果答案错误、格式不符或超过查询次数限制，游戏将失败。
"""

    game_rule_en = """\
Let's play a "Periodic Sequence Deduction" game. Here are the rules:

There is a binary sequence S of length {n}, where each position contains either 0 or 1. This sequence has a special structure: there exists an unknown base block M (with block length b), and S is formed by repeating M multiple times.

Known information:
- Total sequence length N = {n}
- Base block length b satisfies: 1 < b ≤ {bmax}, and b divides N
- Base block M contains at least one 1
- You can make at most {max_queries} queries

Unknown information:
- The exact block length b
- The exact content of base block M
- The exact content of sequence S

Your goal is: Deduce the total count C of all 1s in sequence S.

You can use three types of queries (each query counts as one, please use as few queries as possible):

1. View Query: Ask whether the value at position i is 0 or 1 (positions numbered from 1 to {n})
2. Compare Query: Ask whether the values at position i and position j are the same
3. Period Verification Query: Ask whether a length k is a period of the sequence (i.e., whether S[p] equals S[p+k] for all valid positions p)

Only one type of query per turn. Use the following XML format:

- View Query (e.g., viewing position 5):
<query_view>5</query_view>

- Compare Query (e.g., comparing positions 3 and 7):
<query_compare>3,7</query_compare>

- Period Verification Query (e.g., verifying period length 4):
<query_period>4</query_period>

When submitting the final answer, provide the total count of 1s in the sequence:

<answer>12</answer>

Note: The game fails if the answer is wrong, format is invalid, or query limit is exceeded.
"""

    contextualized_rule_zh_1 = """\
智能交通信号控制系统审计：

我们正在排查一条环城快速路上的智能交通信号灯状态序列 S。该道路共有 {n} 个信号灯节点，状态仅为 0（绿灯畅通）或 1（红灯禁行）。该路段的信号灯配时存在一个未知的循环控制基础方案 M（方案覆盖节点数记为 b），完整的信号灯序列 S 是由基础方案 M 重复实施若干次而形成的。

已知信息：
- 节点总数 N = {n}
- 基础方案覆盖节点数 b 满足：1 < b ≤ {bmax}，且 b 能整除 N
- 基础控制方案 M 中至少包含一个红灯节点（状态为 1）
- 你最多可以调用 {max_queries} 次系统审计查询

未知信息：
- 基础方案的具体覆盖节点数 b
- 基础控制方案 M 的具体配时内容
- 完整道路信号序列 S 的内容

你的目标是：推断出整条道路上所有红灯节点（状态为 1）的总数 C。

你可以使用以下三种审计接口（每次调用计为一次，请尽可能少地使用接口）：

1. 节点状态查询：调取第 i 个节点的信号状态是 0 还是 1（节点编号从 1 到 {n}）
2. 节点对比查询：比对第 i 个节点和第 j 个节点的信号状态是否相同
3. 循环周期验证查询：验证某个节点跨度 k 是否为全路段的循环周期（即对于所有有效节点 p，S[p] 的状态是否必定等于 S[p+k]）

每次只能调用一种接口。请使用以下 XML 格式：

- 节点状态查询（例如查看第 5 个节点）：
<query_view>5</query_view>

- 节点对比查询（例如比对第 3 和第 7 个节点）：
<query_compare>3,7</query_compare>

- 循环周期验证查询（例如验证周期跨度为 4）：
<query_period>4</query_period>

提交最终审计报告时，请直接给出全路段中红灯节点（1）的总数，格式如下：

<answer>12</answer>

注意：如果报告数据错误、格式不符或超过接口调用次数限制，系统审计将自动终止并判定为失败。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Intelligent Traffic Signal Control System Audit:

We are auditing the traffic light status sequence S along a city's ring expressway. The road has {n} signal nodes, and each node's status is either 0 (Green/Clear) or 1 (Red/Stop). The signal timing has a special structure: there exists an unknown base circulation plan M (covering b nodes), and the complete signal sequence S is formed by repeating the base plan M multiple times.

Known information:
- Total number of nodes N = {n}
- Base plan node count b satisfies: 1 < b ≤ {bmax}, and b divides N
- Base plan M contains at least one Red light node (status 1)
- You can make at most {max_queries} system audit queries

Unknown information:
- The exact node count b of the base plan
- The exact timing content of base plan M
- The exact content of the complete signal sequence S

Your goal is: Deduce the total count C of all Red light nodes (status 1) along the entire road.

You can use three types of audit queries (each query counts as one, please use as few queries as possible):

1. View Query: Ask whether the signal status at node i is 0 or 1 (node numbers from 1 to {n})
2. Compare Query: Ask whether the signal statuses at node i and node j are the same
3. Period Verification Query: Ask whether a node span k is a cycle period for the whole road (i.e., whether S[p] equals S[p+k] for all valid nodes p)

Only one type of query per turn. Use the following XML format:

- View Query (e.g., viewing node 5):
<query_view>5</query_view>

- Compare Query (e.g., comparing nodes 3 and 7):
<query_compare>3,7</query_compare>

- Period Verification Query (e.g., verifying cycle span 4):
<query_period>4</query_period>

When submitting the final audit report, provide the total count of Red light nodes (1) along the road:

<answer>12</answer>

Note: The audit fails if the reported data is wrong, format is invalid, or system query limit is exceeded.
"""

    contextualized_rule_zh_2 = """\
心电图（ECG）异常信号监测：

我们正在分析一段连续的心电图（ECG）监测离散信号序列 S。该序列包含 {n} 个时间窗口，每个窗口的信号特征值为 0（正常心搏）或 1（心律失常/异常尖峰）。患者的心电信号呈现特殊的节律：存在一个未知的生理基础循环周期 M（包含 b 个窗口），完整的监测序列 S 是由该基础周期 M 重复多次构成的。

已知信息：
- 总时间窗口数 N = {n}
- 基础周期长度 b 满足：1 < b ≤ {bmax}，且 b 能整除 N
- 基础周期 M 中至少包含一次异常尖峰（值为 1）
- 医疗系统允许你最多进行 {max_queries} 次数据调取查询

未知信息：
- 基础生理周期的具体长度 b
- 基础周期 M 的具体信号特征
- 完整心电序列 S 的内容

你的目标是：推断出整段监测序列 S 中异常尖峰（值为 1）的总次数 C。

你可以使用以下三种临床分析查询（每次查询计为一次，请尽可能少地使用查询次数）：

1. 查看查询：调取第 i 个时间窗口的信号值是 0 还是 1（窗口编号从 1 到 {n}）
2. 比较查询：比对第 i 个窗口和第 j 个窗口的信号值是否相同
3. 验证周期查询：验证某个时间跨度 k 是否为心电序列的全局周期（即对于所有有效窗口 p，S[p] 的信号是否等于 S[p+k]）

每次只能进行一种查询。请使用以下 XML 格式：

- 查看查询（例如查看第 5 个时间窗口）：
<query_view>5</query_view>

- 比较查询（例如比较第 3 和第 7 个时间窗口）：
<query_compare>3,7</query_compare>

- 验证周期查询（例如验证周期跨度为 4）：
<query_period>4</query_period>

提交最终临床分析报告时，请直接给出序列中异常尖峰（1）的总次数，格式如下：

<answer>12</answer>

注意：如果报告数据错误、格式不符或超过调取查询次数限制，监测分析将判定为失败。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Electrocardiogram (ECG) Abnormal Signal Monitoring:

We are analyzing a continuous, discrete Electrocardiogram (ECG) signal sequence S. The sequence consists of {n} time windows, where the signal feature of each window is either 0 (Normal heartbeat) or 1 (Arrhythmia/Abnormal spike). The patient's ECG signal exhibits a special rhythm: there exists an unknown base physiological cycle M (spanning b windows), and the complete monitoring sequence S is formed by repeating this base cycle M multiple times.

Known information:
- Total number of time windows N = {n}
- Base cycle length b satisfies: 1 < b ≤ {bmax}, and b divides N
- Base cycle M contains at least one abnormal spike (value 1)
- The medical system allows you to make at most {max_queries} data queries

Unknown information:
- The exact length b of the base physiological cycle
- The exact signal features of base cycle M
- The exact content of the complete ECG sequence S

Your goal is: Deduce the total count C of abnormal spikes (value 1) in the entire monitoring sequence S.

You can use three types of clinical analysis queries (each query counts as one, please use as few queries as possible):

1. View Query: Ask whether the signal value at time window i is 0 or 1 (window numbers from 1 to {n})
2. Compare Query: Ask whether the signal values at window i and window j are the same
3. Period Verification Query: Ask whether a time span k is a global period of the ECG sequence (i.e., whether S[p] equals S[p+k] for all valid windows p)

Only one type of query per turn. Use the following XML format:

- View Query (e.g., viewing time window 5):
<query_view>5</query_view>

- Compare Query (e.g., comparing windows 3 and 7):
<query_compare>3,7</query_compare>

- Period Verification Query (e.g., verifying period span 4):
<query_period>4</query_period>

When submitting the final clinical report, provide the total count of abnormal spikes (1) in the sequence:

<answer>12</answer>

Note: The analysis fails if the reported data is wrong, format is invalid, or query limit is exceeded.
"""

    contextualized_rule_zh_3 = """\
题库难度模式识别与评估：

我们正在评估一套标准化考试的考题难度序列 S。该试卷共有 {n} 道考题，每道题的难度标识只能是 0（基础题）或 1（拔高题）。这套试卷的生成具有特定的模块化结构：存在一个未知的核心题组 M（包含 b 道题），通过将核心题组 M 重复排列若干次组成了完整的试卷序列 S。

已知信息：
- 试卷总题数 N = {n}
- 核心题组题目数 b 满足：1 < b ≤ {bmax}，且 b 能整除 N
- 核心题组 M 中至少包含一道拔高题（难度为 1）
- 教务系统最多允许你进行 {max_queries} 次抽样查询

未知信息：
- 核心题组的具体题目数 b
- 核心题组 M 的具体难度排布
- 完整试卷序列 S 的内容

你的目标是：推断出整套试卷中所有拔高题（难度为 1）的总数量 C。

你可以使用以下三种抽样查询方式（每次查询计为一次，请尽可能少地使用查询次数）：

1. 查看查询：调阅第 i 道题的难度是 0 还是 1（题目编号从 1 到 {n}）
2. 比较查询：比对第 i 道题和第 j 道题的难度是否相同
3. 验证周期查询：验证某个跨度 k 是否为试卷的难度排布周期（即对于所有有效题号 p，S[p] 的难度是否等于 S[p+k]）

每次只能进行一种查询。请使用以下 XML 格式：

- 查看查询（例如查看第 5 道题）：
<query_view>5</query_view>

- 比较查询（例如比较第 3 和第 7 道题）：
<query_compare>3,7</query_compare>

- 验证周期查询（例如验证周期跨度为 4）：
<query_period>4</query_period>

提交最终评估结果时，请直接给出试卷中拔高题（1）的总数量，格式如下：

<answer>12</answer>

注意：如果答案错误、格式不符或超过查询次数限制，评估任务将失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Question Bank Difficulty Pattern Recognition:

We are evaluating the difficulty sequence S of a standardized test. The test consists of {n} questions, where the difficulty indicator of each question is either 0 (Foundation) or 1 (Advanced/Challenge). This test is generated with a specific modular structure: there exists an unknown core question block M (containing b questions), and the complete test sequence S is formed by repeating the core block M multiple times.

Known information:
- Total number of questions N = {n}
- Core block size b satisfies: 1 < b ≤ {bmax}, and b divides N
- Core block M contains at least one advanced question (difficulty 1)
- The academic system allows you to make at most {max_queries} sampling queries

Unknown information:
- The exact number of questions b in the core block
- The exact difficulty layout of core block M
- The exact content of the complete test sequence S

Your goal is: Deduce the total count C of all advanced questions (difficulty 1) in the entire test.

You can use three types of sampling queries (each query counts as one, please use as few queries as possible):

1. View Query: Ask whether the difficulty of question i is 0 or 1 (question numbers from 1 to {n})
2. Compare Query: Ask whether the difficulties of question i and question j are the same
3. Period Verification Query: Ask whether a span k is a difficulty layout period of the test (i.e., whether S[p] equals S[p+k] for all valid question numbers p)

Only one type of query per turn. Use the following XML format:

- View Query (e.g., viewing question 5):
<query_view>5</query_view>

- Compare Query (e.g., comparing questions 3 and 7):
<query_compare>3,7</query_compare>

- Period Verification Query (e.g., verifying period span 4):
<query_period>4</query_period>

When submitting the final evaluation result, provide the total count of advanced questions (1) in the test:

<answer>12</answer>

Note: The evaluation fails if the answer is wrong, format is invalid, or query limit is exceeded.
"""

    contextualized_rule_zh_4 = """\
流水线自动化质检排查：

我们正在排查一条自动化生产线上的产品质量序列 S。该批次共有 {n} 个连续生产的零部件，每个零件的质检结果只能是 0（合格品）或 1（残次品）。由于机器磨损特性，残次品的出现具有机械周期性：存在一个未知的机器运转基础周期 M（周期内生产 b 个零件），整批产品的质量序列 S 是由基础周期 M 重复多次产生的。

已知信息：
- 零部件总数 N = {n}
- 基础周期产量 b 满足：1 < b ≤ {bmax}，且 b 能整除 N
- 基础运转周期 M 中至少会产生一个残次品（结果为 1）
- 质检设备最多允许你进行 {max_queries} 次检测指令调用

未知信息：
- 机器基础周期的具体产量 b
- 基础运转周期 M 的具体质量分布情况
- 完整产品批次序列 S 的内容

你的目标是：推断出该批次序列 S 中所有残次品（结果为 1）的总数 C。

你可以使用以下三种检测指令（每次指令计为一次调用，请尽可能少地使用）：

1. 质检状态查询：检测第 i 个零件的结果是 0 还是 1（零件编号从 1 到 {n}）
2. 质量对比查询：比对第 i 个和第 j 个零件的质检结果是否相同
3. 机器周期验证查询：验证某个跨度 k 是否为机器运转的故障周期（即对于所有有效零件编号 p，S[p] 的结果是否等于 S[p+k]）

每次只能发送一种指令。请使用以下 XML 格式：

- 质检状态查询（例如检测第 5 个零件）：
<query_view>5</query_view>

- 质量对比查询（例如比较第 3 和第 7 个零件）：
<query_compare>3,7</query_compare>

- 机器周期验证查询（例如验证周期跨度为 4）：
<query_period>4</query_period>

提交最终质检报告时，请直接给出该批次中残次品（1）的总数，格式如下：

<answer>12</answer>

注意：如果报告数据错误、指令格式不符或超过检测次数限制，排查任务将自动失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Automated Assembly Line Quality Inspection Audit:

We are auditing a product quality sequence S from an automated assembly line. This batch consists of {n} continuously produced parts, where the quality inspection result for each part is either 0 (Standard/Pass) or 1 (Defective/Faulty). Due to machine wear characteristics, the occurrence of defects exhibits mechanical periodicity: there exists an unknown base machine operation cycle M (producing b parts per cycle), and the entire batch's quality sequence S is generated by repeating this base cycle M multiple times.

Known information:
- Total number of parts N = {n}
- Base cycle production volume b satisfies: 1 < b ≤ {bmax}, and b divides N
- Base operation cycle M produces at least one defective part (result 1)
- The inspection equipment allows you to issue at most {max_queries} testing commands

Unknown information:
- The exact production volume b of the base machine cycle
- The exact quality distribution of base cycle M
- The exact content of the complete batch sequence S

Your goal is: Deduce the total count C of all defective parts (result 1) in the batch sequence S.

You can use three types of testing commands (each command counts as one, please use as few testing commands as possible):

1. View Query: Inspect whether the result of part i is 0 or 1 (part numbers from 1 to {n})
2. Compare Query: Compare whether the inspection results of part i and part j are the same
3. Period Verification Query: Verify whether a span k is a fault cycle for the machine operation (i.e., whether S[p] equals S[p+k] for all valid part numbers p)

Only one type of command per turn. Use the following XML format:

- View Query (e.g., inspecting part 5):
<query_view>5</query_view>

- Compare Query (e.g., comparing parts 3 and 7):
<query_compare>3,7</query_compare>

- Period Verification Query (e.g., verifying cycle span 4):
<query_period>4</query_period>

When submitting the final report, provide the total count of defective parts (1) in the batch:

<answer>12</answer>

Note: The audit fails if the reported data is wrong, format is invalid, or testing limit is exceeded.
"""

    contextualized_rule_zh_5 = """\
海量制式合同违规条款审计：

我们正在审查一份由系统自动生成的长篇制式合同中的条款风险序列 S。该合同共包含 {n} 个条文，每个条文的法务风险评估值只能是 0（合规条文）或 1（违规/高风险条文）。由于是系统生成的制式合同，条款的排列具有模板复用性：存在一个未知的核心制式模板 M（包含 b 个条文），整份合同的风险序列 S 是由核心模板 M 循环拼接若干次构成的。

已知信息：
- 合同条文总数 N = {n}
- 核心模板条文数 b 满足：1 < b ≤ {bmax}，且 b 能整除 N
- 核心模板 M 中至少包含一项违规/高风险条文（评估值为 1）
- 法务审查系统最多允许你调用 {max_queries} 次审计接口

未知信息：
- 核心制式模板的具体条文数 b
- 核心模板 M 的具体风险分布情况
- 完整合同条款风险序列 S 的内容

你的目标是：推断出整份合同中所有违规/高风险条文（评估值为 1）的总数 C。

你可以使用以下三种审查接口（每次调用计为一次，请尽可能少地使用审查接口）：

1. 条款调阅查询：审查第 i 个条文的评估值是 0 还是 1（条文编号从 1 到 {n}）
2. 风险比对查询：比对第 i 个和第 j 个条文的评估值是否相同
3. 模板复用验证查询：验证某个跨度 k 是否为制式合同的模板复用周期（即对于所有有效条文编号 p，S[p] 的评估值是否等于 S[p+k]）

每次只能调用一种接口。请使用以下 XML 格式：

- 条款调阅查询（例如审查第 5 个条文）：
<query_view>5</query_view>

- 风险比对查询（例如比对第 3 和第 7 个条文）：
<query_compare>3,7</query_compare>

- 模板复用验证查询（例如验证模板复用跨度为 4）：
<query_period>4</query_period>

提交最终审计结果时，请直接给出合同中违规/高风险条文（1）的总数，格式如下：

<answer>12</answer>

注意：如果审计结果错误、格式不符或超过审查接口调用限制，审计任务将判定为失败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Massive Boilerplate Contract Compliance Audit:

We are reviewing a clause risk sequence S within an automatically generated, extensive boilerplate contract. The contract contains {n} clauses, where the legal risk assessment value for each clause is either 0 (Compliant clause) or 1 (Non-compliant/High-risk clause). Because it is a system-generated boilerplate contract, the arrangement of clauses exhibits template reusability: there exists an unknown core boilerplate template M (containing b clauses), and the entire contract's risk sequence S is formed by repeatedly concatenating the core template M.

Known information:
- Total number of clauses N = {n}
- Core template clause count b satisfies: 1 < b ≤ {bmax}, and b divides N
- Core template M contains at least one non-compliant/high-risk clause (assessment value 1)
- The legal review system allows you to call the audit interface at most {max_queries} times

Unknown information:
- The exact clause count b of the core boilerplate template
- The exact risk distribution of core template M
- The exact content of the complete contract risk sequence S

Your goal is: Deduce the total count C of all non-compliant/high-risk clauses (assessment value 1) in the entire contract.

You can use three types of review interfaces (each call counts as one, please use as few calls as possible):

1. View Query: Review whether the assessment value of clause i is 0 or 1 (clause numbers from 1 to {n})
2. Compare Query: Compare whether the assessment values of clause i and clause j are the same
3. Period Verification Query: Verify whether a span k is a template reuse period of the boilerplate contract (i.e., whether S[p] equals S[p+k] for all valid clause numbers p)

Only one type of interface call per turn. Use the following XML format:

- View Query (e.g., reviewing clause 5):
<query_view>5</query_view>

- Compare Query (e.g., comparing clauses 3 and 7):
<query_compare>3,7</query_compare>

- Period Verification Query (e.g., verifying template reuse span of 4):
<query_period>4</query_period>

When submitting the final audit result, provide the total count of non-compliant/high-risk clauses (1) in the contract:

<answer>12</answer>

Note: The audit fails if the result data is wrong, format is invalid, or interface call limit is exceeded.
"""

    tags = ["answer", "query_view", "query_compare", "query_period"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "bmax": 6,
                "b": 3,
                "block": "101",
                "max_queries": 8,
            },
            2: {
                "n": 20,
                "bmax": 10,
                "b": 4,
                "block": "1010",
                "max_queries": 10,
            },
            3: {
                "n": 30,
                "bmax": 15,
                "b": 5,
                "block": "10110",
                "max_queries": 12,
            },
            4: {
                "n": 48,
                "bmax": 24,
                "b": 6,
                "block": "101001",
                "max_queries": 15,
            },
            5: {
                "n": 60,
                "bmax": 30,
                "b": 10,
                "block": "1010010110",
                "max_queries": 18,
            },
        },
        "en": {
            1: {
                "n": 12,
                "bmax": 6,
                "b": 3,
                "block": "101",
                "max_queries": 8,
            },
            2: {
                "n": 20,
                "bmax": 10,
                "b": 4,
                "block": "1010",
                "max_queries": 10,
            },
            3: {
                "n": 30,
                "bmax": 15,
                "b": 5,
                "block": "10110",
                "max_queries": 12,
            },
            4: {
                "n": 48,
                "bmax": 24,
                "b": 6,
                "block": "101001",
                "max_queries": 15,
            },
            5: {
                "n": 60,
                "bmax": 30,
                "b": 10,
                "block": "1010010110",
                "max_queries": 18,
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["bmax"] = cfg["bmax"]
        self._game_info["max_queries"] = cfg["max_queries"]
        
        self.n = cfg["n"]
        self.bmax = cfg["bmax"]
        self.b = cfg["b"]
        self.block = cfg["block"]
        self.max_queries = cfg["max_queries"]
        
        repeat_times = self.n // self.b
        self.sequence = self.block * repeat_times
        
        self.correct_answer = self.sequence.count('1')
        
        self.query_count = 0

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.correct_answer
        except (ValueError, KeyError):
            return False

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            same_res, diff_res = "相同", "不同"
        else:
            yes_res, no_res = "Yes", "No"
            same_res, diff_res = "Same", "Different"

        for i in range(1, self.n + 1):
            query_content = f"<query_view>{i}</query_view>"
            ans = str(self.sequence[i - 1])
            results.append({"query": query_content, "answer": ans})

        for i in range(1, self.n):
            for j in range(i + 1, self.n + 1):
                query_content = f"<query_compare>{i},{j}</query_compare>"
                val1 = self.sequence[i - 1]
                val2 = self.sequence[j - 1]
                ans = same_res if val1 == val2 else diff_res
                results.append({"query": query_content, "answer": ans})

        for k in range(1, self.n):
            query_content = f"<query_period>{k}</query_period>"
            is_period = True
            for p in range(self.n - k):
                if self.sequence[p] != self.sequence[p + k]:
                    is_period = False
                    break
            ans = yes_res if is_period else no_res
            results.append({"query": query_content, "answer": ans})

        return results

    def _cf_core_produce(self, parsed_info):
        if self.query_count >= self.max_queries:
            raise ValueError(
                f"Query limit exceeded: {self.max_queries}" 
                if self.config.language == "en" 
                else f"超出查询次数限制：{self.max_queries}"
            )
        
        self.query_count += 1
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            same_res, diff_res = "相同", "不同"
            error_range = "错误：位置超出范围（有效范围 1 到 {}）。".format(self.n)
            error_format = "错误：格式无效。"
            error_period_range = "错误：周期长度超出范围（有效范围 1 到 {}）。".format(self.n - 1)
        else:
            yes_res, no_res = "Yes", "No"
            same_res, diff_res = "Same", "Different"
            error_range = "Error: Position out of range (valid range: 1 to {}).".format(self.n)
            error_format = "Error: Invalid format."
            error_period_range = "Error: Period length out of range (valid range: 1 to {}).".format(self.n - 1)

        if "query_view" in parsed_info:
            try:
                pos = int(parsed_info["query_view"].strip())
                if pos < 1 or pos > self.n:
                    return error_range
                return self.sequence[pos - 1]
            except (ValueError, IndexError):
                return error_format

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                pos1, pos2 = int(parts[0]), int(parts[1])
                if pos1 < 1 or pos1 > self.n or pos2 < 1 or pos2 > self.n:
                    return error_range
                return same_res if self.sequence[pos1 - 1] == self.sequence[pos2 - 1] else diff_res
            except (ValueError, IndexError):
                return error_format

        elif "query_period" in parsed_info:
            try:
                k = int(parsed_info["query_period"].strip())
                if k < 1 or k >= self.n:
                    return error_period_range
                is_period = True
                for p in range(self.n - k):
                    if self.sequence[p] != self.sequence[p + k]:
                        is_period = False
                        break
                return yes_res if is_period else no_res
            except ValueError:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct == "0":
            return "1"
        if correct == "1":
            return "0"
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        if correct == "相同":
            return "不同"
        if correct == "不同":
            return "相同"
        
        if correct == "Yes":
            return "No"
        if correct == "No":
            return "Yes"
        if correct == "Same":
            return "Different"
        if correct == "Different":
            return "Same"
            
        if str(correct).lstrip('-').isdigit():
            return str(int(correct) + 1)
            
        return f"{correct}_WRONG"