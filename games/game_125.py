from .base import Game
import re

class ScanProtocolReconstructionGame(Game):

    game_rule_zh = """\
我们来玩一个"扫描协议重建"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的二值序列 S[1..{n}]，其中每个位置的值为 0 或 1。序列的具体内容是未知的，需要你推理出来。

同时，存在一个固定但未知的测量协议（从三种候选协议中选择一种），该协议决定了如何响应你的 SCAN 查询。三种候选协议如下：

1. 协议 A（区间奇偶）：SCAN(a,b) 返回区间 [min(a,b) 到 max(a,b)] 上所有值为 1 的位置数量的奇偶性。
2. 协议 B（左前缀奇偶）：SCAN(a,b) 返回区间 [1 到 a] 上所有值为 1 的位置数量的奇偶性（忽略参数 b）。
3. 协议 C（右后缀奇偶）：SCAN(a,b) 返回区间 [N-b+1 到 N] 上所有值为 1 的位置数量的奇偶性（忽略参数 a）。

你的目标是：
1. 通过 SCAN 查询，首先识别当前使用的是哪个协议（A、B 或 C）。
2. 在识别协议后，利用查询结果精确重建序列中所有值为 1 的位置。
3. 最后提交你的答案，包括协议类型和所有值为 1 的位置索引。

每次 SCAN 查询的格式如下（a 和 b 都必须在 1 到 {n} 的范围内）：

<scan>a,b</scan>

系统会返回 0 或 1：
- 0 表示相应子集中值为 1 的位置数量为偶数（包括 0 个）
- 1 表示相应子集中值为 1 的位置数量为奇数

当你确定了协议类型和所有值为 1 的位置后，使用以下格式提交答案：

<answer>mode=X, positions=i1,i2,i3</answer>

其中：
- mode 为协议类型，必须是 A、B 或 C 之一
- positions 为所有值为 1 的位置索引，按递增顺序排列，用逗号分隔
- 如果没有任何位置的值为 1，则写成：<answer>mode=X, positions=</answer>

注意：答案必须同时包含正确的协议类型和完整的位置列表，否则游戏失败。
"""

    game_rule_en = """\
Let's play a "Scan Protocol Reconstruction" deduction game. Here are the rules:

The game has a binary sequence S[1..{n}] of length {n}, where each position contains either 0 or 1. The actual content of the sequence is unknown and needs to be inferred by you.

Additionally, there is a fixed but unknown measurement protocol (chosen from three candidates) that determines how SCAN queries are answered. The three candidate protocols are:

1. Protocol A (Interval Parity): SCAN(a,b) returns the parity of the count of 1s in the interval [min(a,b) to max(a,b)].
2. Protocol B (Left Prefix Parity): SCAN(a,b) returns the parity of the count of 1s in the interval [1 to a] (ignoring parameter b).
3. Protocol C (Right Suffix Parity): SCAN(a,b) returns the parity of the count of 1s in the interval [N-b+1 to N] (ignoring parameter a).

Your goals are:
1. Through SCAN queries, first identify which protocol (A, B, or C) is currently in use.
2. After identifying the protocol, use query results to precisely reconstruct all positions with value 1 in the sequence.
3. Finally, submit your answer including both the protocol type and all position indices with value 1.

Each SCAN query should use the following format (both a and b must be in the range 1 to {n}):

<scan>a,b</scan>

The system will return 0 or 1:
- 0 means the count of 1s in the corresponding subset is even (including 0)
- 1 means the count of 1s in the corresponding subset is odd

When you have determined the protocol type and all positions with value 1, submit your answer in the following format:

<answer>mode=X, positions=i1,i2,i3</answer>

Where:
- mode is the protocol type, must be one of A, B, or C
- positions are all position indices with value 1, in ascending order, separated by commas
- If no positions have value 1, write: <answer>mode=X, positions=</answer>

Note: The answer must contain both the correct protocol type and the complete position list, otherwise the game fails.
"""

    contextualized_rule_zh_1 = """\
我们来执行一项"交通路网拥堵点排查"任务，规则如下：

一条主干道被划分为长度为 {n} 的连续路段序列 S[1..{n}]，每个路段的状态为 0（畅通）或 1（拥堵）。实际的拥堵路段分布是未知的，需要你通过探查排查出来。

目前交管系统调用了三种未知的传感器扫描协议之一，该协议决定了如何响应你的 SCAN 探查指令。三种候选协议如下：

1. 协议 A（区间协同扫描）：SCAN(a,b) 返回路段区间 [min(a,b) 到 max(a,b)] 内拥堵路段总数的奇偶性。
2. 协议 B（起点前缀扫描）：SCAN(a,b) 返回从路网起点 1 到路段 a 的区间内拥堵路段总数的奇偶性（忽略参数 b）。
3. 协议 C（终点后缀扫描）：SCAN(a,b) 返回从路网终点倒数 b 个路段（即 [N-b+1 到 N]）内拥堵路段总数的奇偶性（忽略参数 a）。

你的目标是：
1. 通过 SCAN 探查，首先识别当前激活的是哪种传感器协议（A、B 或 C）。
2. 在识别协议后，利用探查结果精确重建所有状态为 1（拥堵）的路段位置。
3. 最后提交你的排查报告，包括协议类型和所有拥堵路段的编号。

每次 SCAN 探查的指令格式如下（a 和 b 都必须在 1 到 {n} 的范围内）：

<scan>a,b</scan>

系统会返回 0 或 1：
- 0 表示相应探测范围内拥堵路段的数量为偶数（包括 0 个）
- 1 表示相应探测范围内拥堵路段的数量为奇数

当你确定了传感器协议类型和所有拥堵路段的位置后，使用以下格式提交报告：

<answer>mode=X, positions=i1,i2,i3</answer>

其中：
- mode 为协议类型，必须是 A、B 或 C 之一
- positions 为所有状态为 1（拥堵）的路段编号，按递增顺序排列，用逗号分隔
- 如果全线畅通没有任何拥堵路段，则写成：<answer>mode=X, positions=</answer>

注意：报告必须同时包含正确的协议类型和完整的拥堵路段列表，否则排查任务失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's execute a "Traffic Network Congestion Point Troubleshooting" task. Here are the rules:

A main road is divided into a continuous segment sequence S[1..{n}] of length {n}, where each segment's status is either 0 (clear) or 1 (congested). The actual distribution of congested segments is unknown and needs to be identified by you through probing.

The traffic management system has currently activated one of three unknown sensor scanning protocols, which determines how your SCAN probing commands are answered. The three candidate protocols are:

1. Protocol A (Interval Collaborative Scan): SCAN(a,b) returns the parity of the total number of congested segments in the interval [min(a,b) to max(a,b)].
2. Protocol B (Start-point Prefix Scan): SCAN(a,b) returns the parity of the total number of congested segments from the network start point 1 to segment a (ignoring parameter b).
3. Protocol C (End-point Suffix Scan): SCAN(a,b) returns the parity of the total number of congested segments in the last b segments from the network end, i.e., [N-b+1 to N] (ignoring parameter a).

Your goals are:
1. Through SCAN probing, first identify which sensor protocol (A, B, or C) is currently active.
2. After identifying the protocol, use the probe results to precisely reconstruct the positions of all segments with status 1 (congested).
3. Finally, submit your troubleshooting report, including both the protocol type and the IDs of all congested segments.

Each SCAN probing command should use the following format (both a and b must be in the range 1 to {n}):

<scan>a,b</scan>

The system will return 0 or 1:
- 0 means the number of congested segments in the corresponding detection range is even (including 0)
- 1 means the number of congested segments in the corresponding detection range is odd

When you have determined the sensor protocol type and the positions of all congested segments, submit your report in the following format:

<answer>mode=X, positions=i1,i2,i3</answer>

Where:
- mode is the protocol type, must be one of A, B, or C
- positions are all IDs of the congested segments (status 1), in ascending order, separated by commas
- If the entire road is clear with no congested segments, write: <answer>mode=X, positions=</answer>

Note: The report must contain both the correct protocol type and the complete list of congested segments, otherwise the troubleshooting task fails.
"""

    contextualized_rule_zh_2 = """\
我们来执行一项"基因靶点变异测序"任务，规则如下：

系统设定了一个长度为 {n} 的基因组片段序列 S[1..{n}]，其中每个靶点的检测状态为 0（正常）或 1（变异）。变异靶点的具体分布是未知的，需要你通过检测推理出来。

同时，测序仪内置了一种固定但未知的检测协议（从三种候选协议中选择一种），该协议决定了如何响应你的 SCAN 检测指令。三种候选协议如下：

1. 协议 A（靶向区间测序）：SCAN(a,b) 返回靶点区间 [min(a,b) 到 max(a,b)] 上所有发生变异的靶点数量的奇偶性。
2. 协议 B（左侧端粒截断测序）：SCAN(a,b) 返回从首端第 1 个靶点到第 a 个靶点上所有发生变异的靶点数量的奇偶性（忽略参数 b）。
3. 协议 C（右侧端粒截断测序）：SCAN(a,b) 返回从末端倒数 b 个靶点（即 [N-b+1 到 N]）上所有发生变异的靶点数量的奇偶性（忽略参数 a）。

你的目标是：
1. 通过 SCAN 检测，首先识别当前使用的是哪种测序协议（A、B 或 C）。
2. 在识别协议后，利用检测结果精确重建基因片段中所有发生变异（状态为 1）的靶点位置。
3. 最后提交你的诊断结论，包括协议类型和所有变异靶点的索引。

每次 SCAN 检测的指令格式如下（a 和 b 都必须在 1 到 {n} 的范围内）：

<scan>a,b</scan>

系统会返回 0 或 1：
- 0 表示相应基因子集中变异靶点的数量为偶数（包括 0 个）
- 1 表示相应基因子集中变异靶点的数量为奇数

当你确定了测序协议类型和所有变异靶点的位置后，使用以下格式提交诊断结论：

<answer>mode=X, positions=i1,i2,i3</answer>

其中：
- mode 为协议类型，必须是 A、B 或 C 之一
- positions 为所有变异（状态为 1）的靶点索引，按递增顺序排列，用逗号分隔
- 如果没有任何靶点发生变异，则写成：<answer>mode=X, positions=</answer>

注意：诊断结论必须同时包含正确的协议类型和完整的变异靶点列表，否则测序任务失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's execute a "Gene Target Mutation Sequencing" task. Here are the rules:

The system defines a genome fragment sequence S[1..{n}] of length {n}, where the detection status of each target is either 0 (normal) or 1 (mutated). The specific distribution of mutated targets is unknown and needs to be inferred by you through testing.

Meanwhile, the sequencer has a fixed but unknown detection protocol (chosen from three candidates) that determines how your SCAN test commands are answered. The three candidate protocols are:

1. Protocol A (Targeted Interval Sequencing): SCAN(a,b) returns the parity of the number of mutated targets in the interval [min(a,b) to max(a,b)].
2. Protocol B (Left Telomere Truncation Sequencing): SCAN(a,b) returns the parity of the number of mutated targets from the 1st target at the 5' end to target a (ignoring parameter b).
3. Protocol C (Right Telomere Truncation Sequencing): SCAN(a,b) returns the parity of the number of mutated targets in the last b targets at the 3' end, i.e., [N-b+1 to N] (ignoring parameter a).

Your goals are:
1. Through SCAN testing, first identify which sequencing protocol (A, B, or C) is currently in use.
2. After identifying the protocol, use the test results to precisely reconstruct the positions of all mutated targets (status 1) in the genome fragment.
3. Finally, submit your diagnostic conclusion, including both the protocol type and the indices of all mutated targets.

Each SCAN test command should use the following format (both a and b must be in the range 1 to {n}):

<scan>a,b</scan>

The system will return 0 or 1:
- 0 means the number of mutated targets in the corresponding gene subset is even (including 0)
- 1 means the number of mutated targets in the corresponding gene subset is odd

When you have determined the sequencing protocol type and the positions of all mutated targets, submit your diagnostic conclusion in the following format:

<answer>mode=X, positions=i1,i2,i3</answer>

Where:
- mode is the protocol type, must be one of A, B, or C
- positions are the indices of all mutated targets (status 1), in ascending order, separated by commas
- If no targets have mutated, write: <answer>mode=X, positions=</answer>

Note: The diagnostic conclusion must contain both the correct protocol type and the complete list of mutated targets, otherwise the sequencing task fails.
"""

    contextualized_rule_zh_3 = """\
我们来执行一项"学生知识盲区诊断"任务，规则如下：

系统针对某学科生成了一份包含 {n} 个连续知识模块的学习序列 S[1..{n}]，其中每个模块的掌握状态为 0（已掌握）或 1（存在盲区）。学生的具体薄弱模块分布是未知的，需要你通过测试诊断出来。

同时，测试系统采用了一种固定但未知的抽题协议（从三种候选协议中选择一种），该协议决定了如何响应你的 SCAN 测评指令。三种候选协议如下：

1. 协议 A（区间综合抽测）：SCAN(a,b) 返回模块区间 [min(a,b) 到 max(a,b)] 内存在盲区的模块数量的奇偶性。
2. 协议 B（前置基础抽测）：SCAN(a,b) 返回从第 1 个模块到第 a 个模块内存在盲区的模块数量的奇偶性（忽略参数 b）。
3. 协议 C（后置进阶抽测）：SCAN(a,b) 返回从末尾倒数 b 个模块（即 [N-b+1 到 N]）内存在盲区的模块数量的奇偶性（忽略参数 a）。

你的目标是：
1. 通过 SCAN 测评，首先识别当前使用的是哪种抽题协议（A、B 或 C）。
2. 在识别协议后，利用测评结果精确重建序列中所有存在盲区（状态为 1）的模块位置。
3. 最后提交你的学情报告，包括协议类型和所有盲区模块的编号。

每次 SCAN 测评的指令格式如下（a 和 b 都必须在 1 到 {n} 的范围内）：

<scan>a,b</scan>

系统会返回 0 或 1：
- 0 表示相应测试范围内存在盲区的模块数量为偶数（包括 0 个）
- 1 表示相应测试范围内存在盲区的模块数量为奇数

当你确定了抽题协议类型和所有存在盲区的模块位置后，使用以下格式提交学情报告：

<answer>mode=X, positions=i1,i2,i3</answer>

其中：
- mode 为协议类型，必须是 A、B 或 C 之一
- positions 为所有存在盲区（状态为 1）的模块编号，按递增顺序排列，用逗号分隔
- 如果该学生完全没有知识盲区，则写成：<answer>mode=X, positions=</answer>

注意：学情报告必须同时包含正确的协议类型和完整的盲区模块列表，否则诊断任务失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's execute a "Student Knowledge Blind Spot Diagnosis" task. Here are the rules:

The system has generated a learning sequence S[1..{n}] containing {n} continuous knowledge modules for a specific subject, where the mastery status of each module is either 0 (mastered) or 1 (blind spot exists). The student's specific distribution of weak modules is unknown and needs to be diagnosed by you through testing.

Meanwhile, the testing system employs a fixed but unknown question sampling protocol (chosen from three candidates) that determines how your SCAN assessment commands are answered. The three candidate protocols are:

1. Protocol A (Interval Comprehensive Sampling): SCAN(a,b) returns the parity of the number of modules with blind spots in the interval [min(a,b) to max(a,b)].
2. Protocol B (Prerequisite Basic Sampling): SCAN(a,b) returns the parity of the number of modules with blind spots from the 1st module to module a (ignoring parameter b).
3. Protocol C (Advanced Suffix Sampling): SCAN(a,b) returns the parity of the number of modules with blind spots in the last b modules, i.e., [N-b+1 to N] (ignoring parameter a).

Your goals are:
1. Through SCAN assessment, first identify which sampling protocol (A, B, or C) is currently in use.
2. After identifying the protocol, use the assessment results to precisely reconstruct the positions of all modules with blind spots (status 1) in the sequence.
3. Finally, submit your academic report, including both the protocol type and the IDs of all blind spot modules.

Each SCAN assessment command should use the following format (both a and b must be in the range 1 to {n}):

<scan>a,b</scan>

The system will return 0 or 1:
- 0 means the number of blind spot modules in the corresponding testing range is even (including 0)
- 1 means the number of blind spot modules in the corresponding testing range is odd

When you have determined the sampling protocol type and the positions of all modules with blind spots, submit your academic report in the following format:

<answer>mode=X, positions=i1,i2,i3</answer>

Where:
- mode is the protocol type, must be one of A, B, or C
- positions are all IDs of the modules with blind spots (status 1), in ascending order, separated by commas
- If the student has absolutely no knowledge blind spots, write: <answer>mode=X, positions=</answer>

Note: The academic report must contain both the correct protocol type and the complete list of blind spot modules, otherwise the diagnosis task fails.
"""

    contextualized_rule_zh_4 = """\
我们来执行一项"流水线产品缺陷无损检测"任务，规则如下：

一条生产线上有长度为 {n} 的连续工件序列 S[1..{n}]，其中每个工件的质检状态为 0（合格）或 1（存在缺陷）。具体哪些工件存在缺陷是未知的，需要你通过仪器检测出来。

同时，探伤仪配置了一种固定但未知的扫描协议（从三种候选协议中选择一种），该协议决定了如何响应你的 SCAN 扫描指令。三种候选协议如下：

1. 协议 A（区间联合扫描）：SCAN(a,b) 返回工件区间 [min(a,b) 到 max(a,b)] 内存在缺陷的工件数量的奇偶性。
2. 协议 B（流水线前段扫描）：SCAN(a,b) 返回从首个工件 1 到工件 a 的区间内存在缺陷的工件数量的奇偶性（忽略参数 b）。
3. 协议 C（流水线后段扫描）：SCAN(a,b) 返回从末尾倒数 b 个工件（即 [N-b+1 到 N]）内存在缺陷的工件数量的奇偶性（忽略参数 a）。

你的目标是：
1. 通过 SCAN 扫描，首先识别当前探伤仪激活的是哪种扫描协议（A、B 或 C）。
2. 在识别协议后，利用扫描结果精确重建序列中所有存在缺陷（状态为 1）的工件位置。
3. 最后提交你的质检报告，包括协议类型和所有缺陷工件的编号。

每次 SCAN 扫描的指令格式如下（a 和 b 都必须在 1 到 {n} 的范围内）：

<scan>a,b</scan>

系统会返回 0 或 1：
- 0 表示相应批次中存在缺陷的工件数量为偶数（包括 0 个）
- 1 表示相应批次中存在缺陷的工件数量为奇数

当你确定了扫描协议类型和所有缺陷工件的位置后，使用以下格式提交质检报告：

<answer>mode=X, positions=i1,i2,i3</answer>

其中：
- mode 为协议类型，必须是 A、B 或 C 之一
- positions 为所有存在缺陷（状态为 1）的工件编号，按递增顺序排列，用逗号分隔
- 如果该批次产品全部合格没有任何缺陷，则写成：<answer>mode=X, positions=</answer>

注意：质检报告必须同时包含正确的协议类型和完整的缺陷工件列表，否则检测任务失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's execute a "Pipeline Product Defect Nondestructive Testing" task. Here are the rules:

A production line has a continuous workpiece sequence S[1..{n}] of length {n}, where the quality inspection status of each workpiece is either 0 (qualified) or 1 (defective). The specific distribution of defective workpieces is unknown and needs to be identified by you through instrument testing.

Meanwhile, the flaw detector is configured with a fixed but unknown scanning protocol (chosen from three candidates) that determines how your SCAN scanning commands are answered. The three candidate protocols are:

1. Protocol A (Interval Joint Scan): SCAN(a,b) returns the parity of the number of defective workpieces in the interval [min(a,b) to max(a,b)].
2. Protocol B (Pipeline Front-end Scan): SCAN(a,b) returns the parity of the number of defective workpieces from the first workpiece 1 to workpiece a (ignoring parameter b).
3. Protocol C (Pipeline Back-end Scan): SCAN(a,b) returns the parity of the number of defective workpieces in the last b workpieces, i.e., [N-b+1 to N] (ignoring parameter a).

Your goals are:
1. Through SCAN scanning, first identify which scanning protocol (A, B, or C) is currently active on the flaw detector.
2. After identifying the protocol, use the scan results to precisely reconstruct the positions of all defective workpieces (status 1) in the sequence.
3. Finally, submit your quality inspection report, including both the protocol type and the IDs of all defective workpieces.

Each SCAN scanning command should use the following format (both a and b must be in the range 1 to {n}):

<scan>a,b</scan>

The system will return 0 or 1:
- 0 means the number of defective workpieces in the corresponding batch is even (including 0)
- 1 means the number of defective workpieces in the corresponding batch is odd

When you have determined the scanning protocol type and the positions of all defective workpieces, submit your quality inspection report in the following format:

<answer>mode=X, positions=i1,i2,i3</answer>

Where:
- mode is the protocol type, must be one of A, B, or C
- positions are all IDs of the defective workpieces (status 1), in ascending order, separated by commas
- If the entire batch is qualified with zero defects, write: <answer>mode=X, positions=</answer>

Note: The quality inspection report must contain both the correct protocol type and the complete list of defective workpieces, otherwise the testing task fails.
"""

    contextualized_rule_zh_5 = """\
我们来执行一项"商业合同法律风险审查"任务，规则如下：

一份复杂的商业合同包含长度为 {n} 的连续条款序列 S[1..{n}]，其中每个条款的审查状态为 0（合规）或 1（存在法律漏洞）。漏洞条款的具体分布是未知的，需要你通过审查程序排查出来。

同时，法务智能审查系统设定了一种固定但未知的审查协议（从三种候选协议中选择一种），该协议决定了如何响应你的 SCAN 审查指令。三种候选协议如下：

1. 协议 A（条款区间审查）：SCAN(a,b) 返回条款区间 [min(a,b) 到 max(a,b)] 内存在法律漏洞的条款数量的奇偶性。
2. 协议 B（前序条款审查）：SCAN(a,b) 返回从首个条款 1 到条款 a 的区间内存在法律漏洞的条款数量的奇偶性（忽略参数 b）。
3. 协议 C（后序条款审查）：SCAN(a,b) 返回从合同末尾倒数 b 个条款（即 [N-b+1 到 N]）内存在法律漏洞的条款数量的奇偶性（忽略参数 a）。

你的目标是：
1. 通过 SCAN 审查，首先识别当前法务系统使用的是哪种审查协议（A、B 或 C）。
2. 在识别协议后，利用审查结果精确重建合同中所有存在法律漏洞（状态为 1）的条款位置。
3. 最后提交你的法务审查报告，包括协议类型和所有漏洞条款的编号。

每次 SCAN 审查的指令格式如下（a 和 b 都必须在 1 到 {n} 的范围内）：

<scan>a,b</scan>

系统会返回 0 或 1：
- 0 表示相应审查范围内存在漏洞的条款数量为偶数（包括 0 个）
- 1 表示相应审查范围内存在漏洞的条款数量为奇数

当你确定了审查协议类型和所有漏洞条款的位置后，使用以下格式提交法务审查报告：

<answer>mode=X, positions=i1,i2,i3</answer>

其中：
- mode 为协议类型，必须是 A、B 或 C 之一
- positions 为所有存在法律漏洞（状态为 1）的条款编号，按递增顺序排列，用逗号分隔
- 如果该合同完全合规没有任何法律漏洞，则写成：<answer>mode=X, positions=</answer>

注意：法务审查报告必须同时包含正确的协议类型和完整的漏洞条款列表，否则审查任务失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's execute a "Commercial Contract Legal Risk Review" task. Here are the rules:

A complex commercial contract contains a continuous clause sequence S[1..{n}] of length {n}, where the review status of each clause is either 0 (compliant) or 1 (contains a legal loophole). The specific distribution of loophole clauses is unknown and needs to be identified by you through the review process.

Meanwhile, the legal intelligent review system has set a fixed but unknown review protocol (chosen from three candidates) that determines how your SCAN review commands are answered. The three candidate protocols are:

1. Protocol A (Clause Interval Review): SCAN(a,b) returns the parity of the number of clauses with legal loopholes in the interval [min(a,b) to max(a,b)].
2. Protocol B (Preceding Clause Review): SCAN(a,b) returns the parity of the number of clauses with legal loopholes from the first clause 1 to clause a (ignoring parameter b).
3. Protocol C (Succeeding Clause Review): SCAN(a,b) returns the parity of the number of clauses with legal loopholes in the last b clauses, i.e., [N-b+1 to N] (ignoring parameter a).

Your goals are:
1. Through SCAN reviews, first identify which review protocol (A, B, or C) the legal system is currently using.
2. After identifying the protocol, use the review results to precisely reconstruct the positions of all clauses with legal loopholes (status 1) in the contract.
3. Finally, submit your legal review report, including both the protocol type and the IDs of all loophole clauses.

Each SCAN review command should use the following format (both a and b must be in the range 1 to {n}):

<scan>a,b</scan>

The system will return 0 or 1:
- 0 means the number of loophole clauses in the corresponding review range is even (including 0)
- 1 means the number of loophole clauses in the corresponding review range is odd

When you have determined the review protocol type and the positions of all loophole clauses, submit your legal review report in the following format:

<answer>mode=X, positions=i1,i2,i3</answer>

Where:
- mode is the protocol type, must be one of A, B, or C
- positions are all IDs of the clauses with legal loopholes (status 1), in ascending order, separated by commas
- If the contract is completely compliant with no legal loopholes, write: <answer>mode=X, positions=</answer>

Note: The legal review report must contain both the correct protocol type and the complete list of loophole clauses, otherwise the review task fails.
"""

    tags = ["answer", "scan"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "sequence": "0,1,0,1,0",
                "protocol": "A",
            },
            2: {
                "n": 7,
                "sequence": "1,0,1,0,1,0,0",
                "protocol": "B",
            },
            3: {
                "n": 8,
                "sequence": "0,1,1,0,1,1,0,1",
                "protocol": "C",
            },
            4: {
                "n": 10,
                "sequence": "1,0,0,1,0,0,1,0,1,0",
                "protocol": "A",
            },
            5: {
                "n": 12,
                "sequence": "0,1,0,1,1,0,1,0,0,1,1,0",
                "protocol": "B",
            },
        },
        "en": {
            1: {
                "n": 5,
                "sequence": "0,1,0,1,0",
                "protocol": "A",
            },
            2: {
                "n": 7,
                "sequence": "1,0,1,0,1,0,0",
                "protocol": "B",
            },
            3: {
                "n": 8,
                "sequence": "0,1,1,0,1,1,0,1",
                "protocol": "C",
            },
            4: {
                "n": 10,
                "sequence": "1,0,0,1,0,0,1,0,1,0",
                "protocol": "A",
            },
            5: {
                "n": 12,
                "sequence": "0,1,0,1,1,0,1,0,0,1,1,0",
                "protocol": "B",
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
        self._game_info["n"] = cfg["n"]
        
        self.sequence = [int(x.strip()) for x in cfg["sequence"].split(",")]
        if len(self.sequence) != cfg["n"]:
            raise ValueError(f"Sequence length mismatch: expected {cfg['n']}, got {len(self.sequence)}")
        
        self.protocol = cfg["protocol"]
        
        self.true_positions = set()
        for i, val in enumerate(self.sequence):
            if val == 1:
                self.true_positions.add(i + 1)

    def _compute_scan_result(self, a, b):
        n = self._game_info["n"]
        
        if not (1 <= a <= n and 1 <= b <= n):
            raise ValueError(f"Parameters out of range: a={a}, b={b}, n={n}")
        
        count = 0
        
        if self.protocol == "A":
            left = min(a, b)
            right = max(a, b)
            for pos in self.true_positions:
                if left <= pos <= right:
                    count += 1
                    
        elif self.protocol == "B":
            for pos in self.true_positions:
                if pos <= a:
                    count += 1
                    
        elif self.protocol == "C":
            left = n - b + 1
            for pos in self.true_positions:
                if pos >= left:
                    count += 1
        else:
            raise ValueError(f"Unknown protocol: {self.protocol}")
        
        return count % 2

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            mode_match = re.search(r'mode\s*=\s*([ABCabc])', raw_ans)
            pos_match = re.search(r'positions\s*=\s*([\d,\s]*)', raw_ans)
            
            if not mode_match or pos_match is None:
                return False
            
            submitted_mode = mode_match.group(1).strip().upper()
            pos_value = pos_match.group(1).strip()
            
            if submitted_mode != self.protocol:
                return False
            
            if pos_value == "":
                submitted_positions = set()
            else:
                submitted_positions = set()
                for p in pos_value.split(","):
                    p = p.strip()
                    if p:
                        submitted_positions.add(int(p))
            
            return submitted_positions == self.true_positions
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if "scan" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."
        
        try:
            raw = parsed_info["scan"].strip()
            parts = [x.strip() for x in raw.split(",")]
            
            if len(parts) != 2:
                raise ValueError("SCAN requires exactly 2 parameters")
            
            a = int(parts[0])
            b = int(parts[1])
            
            result = self._compute_scan_result(a, b)
            return str(result)
            
        except ValueError as e:
            if self.config.language == "zh":
                return f"错误：参数格式无效或超出范围。{str(e)}"
            else:
                return f"Error: Invalid parameter format or out of range. {str(e)}"
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：查询处理失败。{str(e)}"
            else:
                return f"Error: Query processing failed. {str(e)}"

    def _cf_make_wrong(self, correct: str) -> str:
        stripped = correct.strip()
        if stripped == "0":
            return "1"
        elif stripped == "1":
            return "0"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        
        for a in range(1, n + 1):
            for b in range(1, n + 1):
                result = self._compute_scan_result(a, b)
                
                queries.append({
                    "query": f"<scan>{a},{b}</scan>",
                    "answer": str(result)
                })
                
        return queries