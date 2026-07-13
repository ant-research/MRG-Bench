from .base import Game
import re

class WindowPatternDetectionGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"窗口模式检测"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列 S，元素只包含 A、B、C 三种字符。序列从左到右的索引为 1 到 {n}。

序列内容为：{sequence}

你的目标是检测这个序列中是否存在目标模式"ABC"（即连续的三个元素依次为 A、B、C）。

但是，你不能直接查看序列，只能通过"窗口查询"来间接获取信息。每次查询时，你需要提供一对整数 (L, R)，其中 1 小于等于 L 小于等于 {n}，1 小于等于 R 小于等于 {n}。

系统会根据一个固定但未知的"窗口解释规则"，将你提供的 (L, R) 映射为一个索引集合 W，然后回答：在 W 对应的序列片段中，是否存在完整的目标模式"ABC"（即存在某个位置 i，使得 i、i+1、i+2 都在 W 中，且对应元素依次为 A、B、C）。

窗口解释规则有四种可能（整场游戏中规则固定不变）：

规则 1（标准左到右闭区间）：
  如果 L 小于等于 R，W 包含从 L 到 R 的所有索引（闭区间）；
  否则 W 为空集。

规则 2（右到左编号闭区间）：
  将序列视为从右到左编号（最右端为 1，最左端为 {n}）。
  如果 L 小于等于 R，将右侧编号区间 [L..R] 转换为左侧编号区间，W 为转换后的索引集合；
  否则 W 为空集。

规则 3（左到右开区间）：
  如果 L 小于 R，W 包含大于 L 且小于 R 的所有索引（开区间）；
  否则 W 为空集。

规则 4（循环闭区间）：
  如果 L 小于等于 R，W 包含从 L 到 R 的所有索引（闭区间）；
  如果 L 大于 R，W 包含从 L 到 {n} 的所有索引，以及从 1 到 R 的所有索引（循环）。

你需要通过尽可能少的查询次数来完成以下任务：
1. 推断出真实的窗口解释规则编号（1、2、3 或 4）
2. 计算在特定查询 (L={target_l}, R={target_r}) 下，按照你推断的规则，目标模式"ABC"在窗口中从左到右最小的起始索引 K（如果不存在则 K=0）

## 查询与提交答案的格式

每次查询时，使用以下 XML 格式（L 和 R 用逗号分隔）：

<query>L,R</query>

例如，查询 L=1, R=5：

<query>1,5</query>

提交最终答案时，需要说明你推断的规则编号和计算出的索引 K，格式如下：

<answer>rule=1, k=3</answer>

其中 rule 为规则编号（1/2/3/4），k 为在查询 (L={target_l}, R={target_r}) 下目标模式的最小起始索引（不存在则为 0）。
"""

    game_rule_en = """\
Let's play a "Window Pattern Detection" deduction game. Here are the rules:

The game has an ordered sequence S of length {n}, containing only three characters: A, B, and C. The sequence is indexed from 1 to {n} (left to right).

The sequence content is: {sequence}

Your goal is to detect whether the target pattern "ABC" exists in this sequence (i.e., three consecutive elements A, B, C in order).

However, you cannot directly view the sequence. You can only obtain information through "window queries". For each query, you provide a pair of integers (L, R), where 1 less than or equal to L less than or equal to {n}, and 1 less than or equal to R less than or equal to {n}.

The system will map your (L, R) to an index set W according to a fixed but unknown "window interpretation rule", then answer: does the complete target pattern "ABC" exist in the sequence fragment corresponding to W (i.e., there exists a position i such that i, i+1, i+2 are all in W, and the corresponding elements are A, B, C in order)?

There are four possible window interpretation rules (the rule is fixed throughout the game):

Rule 1 (Standard left-to-right closed interval):
  If L less than or equal to R, W contains all indices from L to R (closed interval);
  Otherwise W is empty.

Rule 2 (Right-to-left numbered closed interval):
  View the sequence as numbered from right to left (rightmost is 1, leftmost is {n}).
  If L less than or equal to R, convert the right-side numbered interval [L..R] to left-side numbered indices, W is the converted index set;
  Otherwise W is empty.

Rule 3 (Left-to-right open interval):
  If L less than R, W contains all indices greater than L and less than R (open interval);
  Otherwise W is empty.

Rule 4 (Circular closed interval):
  If L less than or equal to R, W contains all indices from L to R (closed interval);
  If L greater than R, W contains all indices from L to {n} and from 1 to R (circular).

You need to complete the following tasks with as few queries as possible:
1. Infer the true window interpretation rule number (1, 2, 3, or 4)
2. Calculate the minimum starting index K (from left to right) of the target pattern "ABC" in the window for the specific query (L={target_l}, R={target_r}) according to your inferred rule (K=0 if it doesn't exist)

## Query and Answer Format

For each query, use the following XML format (L and R separated by comma):

<query>L,R</query>

For example, to query L=1, R=5:

<query>1,5</query>

When submitting the final answer, specify the rule number you inferred and the calculated index K in the following format:

<answer>rule=1, k=3</answer>

Where rule is the rule number (1/2/3/4), and k is the minimum starting index of the target pattern under query (L={target_l}, R={target_r}) (0 if it doesn't exist).
"""

    contextualized_rule_zh_1 = """\
欢迎使用"交通异常演变模式检测系统"。我们来通过排查路网完成以下任务，规则如下：

系统设定了一条长度为 {n} 的路段状态序列 S，元素只包含三种通行状况：A（车流密集）、B（行驶缓慢）、C（拥堵停滞）。路段从左到右的里程节点编号为 1 到 {n}。

当前路段状态序列为：{sequence}

你的目标是检测这个路段中是否存在连续的恶化模式"ABC"（即连续的三个路段状况依次为 A、B、C）。

出于路网监控限制，你不能直接查看全局序列，只能通过"区间探测器"来间接获取信息。每次探测时，你需要提供一对整数节点 (L, R)，其中 1 小于等于 L 小于等于 {n}，1 小于等于 R 小于等于 {n}。

系统会根据一个固定但未知的"探测区间解释规则"，将你提供的 (L, R) 映射为一个实际排查的路段集合 W，然后回答：在 W 对应的路段中，是否存在完整的恶化模式"ABC"（即存在某个起始点 i，使得 i、i+1、i+2 都在 W 中，且对应状况依次为 A、B、C）。

探测区间解释规则有四种可能（整场排查中规则固定不变）：

规则 1（标准顺向路段闭区间）：
  如果 L 小于等于 R，W 包含从 L 到 R 的所有路段节点（闭区间）；
  否则 W 为空集。

规则 2（逆向里程碑闭区间）：
  将路网视为从右到左编号（最右侧终点为 1，最左侧起点为 {n}）。
  如果 L 小于等于 R，将右侧编号区间 [L..R] 转换为左侧标准编号，W 为转换后的节点集合；
  否则 W 为空集。

规则 3（排除端点的顺向开区间）：
  如果 L 小于 R，W 包含大于 L 且小于 R 的所有路段节点（开区间）；
  否则 W 为空集。

规则 4（环城公路循环闭区间）：
  如果 L 小于等于 R，W 包含从 L 到 R 的所有路段节点（闭区间）；
  如果 L 大于 R，W 包含从 L 到 {n} 的所有节点，以及从 1 到 R 的所有节点（环路循环）。

你需要通过尽可能少的探测次数来完成以下任务：
1. 推断出真实的探测区间解释规则编号（1、2、3 或 4）
2. 计算在特定探测指令 (L={target_l}, R={target_r}) 下，按照你推断的规则，恶化模式"ABC"在区间中最早出现的起始节点索引 K（如果不存在则 K=0）

## 查询与提交答案的格式

每次探测时，使用以下 XML 格式（L 和 R 用逗号分隔）：

<query>L,R</query>

例如，探测 L=1, R=5：

<query>1,5</query>

提交最终报告时，需要说明你推断的规则编号和计算出的节点 K，格式如下：

<answer>rule=1, k=3</answer>

其中 rule 为规则编号（1/2/3/4），k 为在探测指令 (L={target_l}, R={target_r}) 下恶化模式的最小起始节点（不存在则为 0）。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Traffic Anomaly Evolution Pattern Detection System". Let's complete the following tasks by inspecting the road network. Here are the rules:

The system has a road status sequence S of length {n}, containing only three traffic conditions: A (Dense Traffic), B (Slow Moving), and C (Congested and Stalled). The road sections are indexed from 1 to {n} (from start to end).

The current road status sequence is: {sequence}

Your goal is to detect whether a continuous deterioration pattern "ABC" exists in this segment (i.e., three consecutive sections are A, B, and C in order).

Due to monitoring limitations, you cannot directly view the global sequence. You can only obtain information through the "Interval Detector". For each detection, you provide a pair of integer nodes (L, R), where 1 less than or equal to L less than or equal to {n}, and 1 less than or equal to R less than or equal to {n}.

The system will map your (L, R) to an actual inspected road section set W according to a fixed but unknown "detection interval interpretation rule", then answer: does the complete deterioration pattern "ABC" exist in the sections corresponding to W (i.e., there exists a starting point i such that i, i+1, i+2 are all in W, and the corresponding conditions are A, B, C in order)?

There are four possible detection interval interpretation rules (fixed throughout the inspection):

Rule 1 (Standard forward section closed interval):
  If L less than or equal to R, W contains all nodes from L to R (closed interval);
  Otherwise W is empty.

Rule 2 (Reverse milestone closed interval):
  View the road network as numbered from right to left (rightmost end is 1, leftmost start is {n}).
  If L less than or equal to R, convert the right-side numbered interval [L..R] to standard left-side indices, W is the converted node set;
  Otherwise W is empty.

Rule 3 (Forward open interval excluding endpoints):
  If L less than R, W contains all nodes greater than L and less than R (open interval);
  Otherwise W is empty.

Rule 4 (Ring road circular closed interval):
  If L less than or equal to R, W contains all nodes from L to R (closed interval);
  If L greater than R, W contains all nodes from L to {n} and from 1 to R (circular).

You need to complete the following tasks with as few detections as possible:
1. Infer the true detection interval interpretation rule number (1, 2, 3, or 4)
2. Calculate the earliest starting node index K (from start to end) of the deterioration pattern "ABC" in the interval for the specific detection command (L={target_l}, R={target_r}) according to your inferred rule (K=0 if it doesn't exist)

## Query and Answer Format

For each detection, use the following XML format (L and R separated by comma):

<query>L,R</query>

For example, to detect L=1, R=5:

<query>1,5</query>

When submitting the final report, specify the rule number you inferred and the calculated node K in the following format:

<answer>rule=1, k=3</answer>

Where rule is the rule number (1/2/3/4), and k is the minimum starting node of the pattern under detection command (L={target_l}, R={target_r}) (0 if it doesn't exist).
"""

    contextualized_rule_zh_2 = """\
欢迎使用"基因变异靶点筛查系统"。我们来执行一次病理特征分析，规则如下：

样本中包含一条长度为 {n} 的核苷酸标记序列 S，片段只包含三种特异性蛋白标志物：A、B、C。片段从左到右的正向排序索引为 1 到 {n}。

当前切片序列内容为：{sequence}

你的目标是检测这个基因序列中是否存在特定的连续变异链"ABC"（即连续的三个标志物依次为 A、B、C）。

由于提取工艺限制，你不能直接观测全链条序列，只能通过"切片采样器"来间接验证。每次采样时，你需要设定一对整数位点 (L, R)，其中 1 小于等于 L 小于等于 {n}，1 小于等于 R 小于等于 {n}。

系统会根据一个固定但未知的"切片提取规则"，将你提供的 (L, R) 映射为一个实际的检测位点集合 W，然后回答：在 W 对应的提取片段中，是否存在完整的变异链"ABC"（即存在某个位点 i，使得 i、i+1、i+2 都在 W 中，且对应标志物依次为 A、B、C）。

切片提取规则有四种可能（整场检测中规则固定不变）：

规则 1（标准正向切片闭区间）：
  如果 L 小于等于 R，W 包含从 L 到 R 的所有位点（闭区间）；
  否则 W 为空集。

规则 2（逆向测序提取闭区间）：
  将序列视为从右到左的逆向测序（最右端为 1，最左端为 {n}）。
  如果 L 小于等于 R，将逆向区间 [L..R] 转换为正向位点索引，W 为转换后的集合；
  否则 W 为空集。

规则 3（内部提取开区间）：
  如果 L 小于 R，W 包含大于 L 且小于 R 的所有位点（开区间）；
  否则 W 为空集。

规则 4（质粒环状DNA循环区间）：
  如果 L 小于等于 R，W 包含从 L 到 R 的所有位点（闭区间）；
  如果 L 大于 R，W 包含从 L 到 {n} 的所有位点，以及从 1 到 R 的所有位点（环状相接）。

你需要通过尽可能少的采样次数来完成以下任务：
1. 推断出真实的切片提取规则编号（1、2、3 或 4）
2. 计算在特定采样参数 (L={target_l}, R={target_r}) 下，按照你推断的规则，变异链"ABC"在切片片段中最先出现的正向起始位点 K（如果不存在则 K=0）

## 查询与提交答案的格式

每次采样时，使用以下 XML 格式（L 和 R 用逗号分隔）：

<query>L,R</query>

例如，采样 L=1, R=5：

<query>1,5</query>

提交分析结果时，需要说明你推断的规则编号和计算出的位点 K，格式如下：

<answer>rule=1, k=3</answer>

其中 rule 为规则编号（1/2/3/4），k 为在采样参数 (L={target_l}, R={target_r}) 下变异链的最早起始位点（不存在则为 0）。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Genomic Mutation Target Screening System". Let's perform a pathological feature analysis with the following rules:

The sample contains a nucleotide marker sequence S of length {n}, consisting only of three specific protein markers: A, B, and C. The fragments are indexed from 1 to {n} in forward order (left to right).

The current slice sequence is: {sequence}

Your goal is to detect whether a specific continuous mutation chain "ABC" exists in this genomic sequence (i.e., three consecutive markers are A, B, and C in order).

Due to extraction process limitations, you cannot directly observe the full-chain sequence. You can only indirectly verify it through the "Slice Sampler". For each sampling, you need to set a pair of integer loci (L, R), where 1 less than or equal to L less than or equal to {n}, and 1 less than or equal to R less than or equal to {n}.

The system will map your (L, R) to an actual tested locus set W according to a fixed but unknown "slice extraction rule", then answer: does the complete mutation chain "ABC" exist in the extracted fragment corresponding to W (i.e., there exists a locus i such that i, i+1, i+2 are all in W, and the corresponding markers are A, B, C in order)?

There are four possible slice extraction rules (fixed throughout the screening):

Rule 1 (Standard forward slice closed interval):
  If L less than or equal to R, W contains all loci from L to R (closed interval);
  Otherwise W is empty.

Rule 2 (Reverse sequencing extraction closed interval):
  View the sequence as reverse sequencing from right to left (rightmost is 1, leftmost is {n}).
  If L less than or equal to R, convert the reverse interval [L..R] to forward locus indices, W is the converted set;
  Otherwise W is empty.

Rule 3 (Internal extraction open interval):
  If L less than R, W contains all loci greater than L and less than R (open interval);
  Otherwise W is empty.

Rule 4 (Plasmid circular DNA interval):
  If L less than or equal to R, W contains all loci from L to R (closed interval);
  If L greater than R, W contains all loci from L to {n} and from 1 to R (circularly connected).

You need to complete the following tasks with as few samplings as possible:
1. Infer the true slice extraction rule number (1, 2, 3, or 4)
2. Calculate the earliest forward starting locus K of the mutation chain "ABC" in the sliced fragment for the specific sampling parameters (L={target_l}, R={target_r}) according to your inferred rule (K=0 if it doesn't exist)

## Query and Answer Format

For each sampling, use the following XML format (L and R separated by comma):

<query>L,R</query>

For example, to sample L=1, R=5:

<query>1,5</query>

When submitting the analysis results, specify the rule number you inferred and the calculated locus K in the following format:

<answer>rule=1, k=3</answer>

Where rule is the rule number (1/2/3/4), and k is the minimum starting locus of the mutation chain under sampling parameters (L={target_l}, R={target_r}) (0 if it doesn't exist).
"""

    contextualized_rule_zh_3 = """\
欢迎使用"学习行为闭环追踪系统"。我们来进行一项学情跟踪分析，规则如下：

系统记录了某学生长度为 {n} 的学习模块序列 S，模块内容仅包含三种行为：A（理论预习）、B（实践听讲）、C（复习考核）。模块按时间先后顺序的学时索引为 1 到 {n}。

学期学习序列记录为：{sequence}

你的目标是检测这个学期序列中是否形成了完整的"ABC"黄金学习闭环（即连续的三个学时行为依次为 A、B、C）。

由于隐私保护限制，你不能直接调阅全周期学习日志，只能通过"学时分析仪"来间接获取信息。每次分析时，你需要提供一对整数节点 (L, R)，其中 1 小于等于 L 小于等于 {n}，1 小于等于 R 小于等于 {n}。

系统会根据一个固定但未知的"学时排查规则"，将你提供的 (L, R) 映射为一个实际分析的学时集合 W，然后回答：在 W 对应的学时范围内，是否存在完整的黄金学习闭环"ABC"（即存在某个起始学时 i，使得 i、i+1、i+2 都在 W 中，且对应行为依次为 A、B、C）。

学时排查规则有四种可能（整场分析中规则固定不变）：

规则 1（标准学期闭区间）：
  如果 L 小于等于 R，W 包含从 L 到 R 的所有学时节点（闭区间）；
  否则 W 为空集。

规则 2（倒计时周次闭区间）：
  将学期视为从期末到期初倒数（期末最后为 1，期初最前为 {n}）。
  如果 L 小于等于 R，将倒数编号区间 [L..R] 转换为正向学时索引，W 为转换后的集合；
  否则 W 为空集。

规则 3（中期排查开区间）：
  如果 L 小于 R，W 包含大于 L 且小于 R 的所有学时节点（开区间，剔除首尾节点）；
  否则 W 为空集。

规则 4（跨学期滚动循环闭区间）：
  如果 L 小于等于 R，W 包含从 L 到 R 的所有学时节点（闭区间）；
  如果 L 大于 R，W 包含从 L 到 {n} 的所有节点，以及从 1 到 R 的所有节点（周期滚动）。

你需要通过尽可能少的分析次数来完成以下任务：
1. 推断出真实的学时排查规则编号（1、2、3 或 4）
2. 计算在特定排查指令 (L={target_l}, R={target_r}) 下，按照你推断的规则，黄金学习闭环"ABC"在排查范围内最早出现的起始学时索引 K（如果不存在则 K=0）

## 查询与提交答案的格式

每次分析时，使用以下 XML 格式（L 和 R 用逗号分隔）：

<query>L,R</query>

例如，分析 L=1, R=5：

<query>1,5</query>

提交综合评价时，需要说明你推断的规则编号和计算出的学时 K，格式如下：

<answer>rule=1, k=3</answer>

其中 rule 为规则编号（1/2/3/4），k 为在排查指令 (L={target_l}, R={target_r}) 下学习闭环的最早起始学时（不存在则为 0）。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Learning Behavior Closed-loop Tracking System". Let's conduct a learning situation analysis with the following rules:

The system records a student's learning module sequence S of length {n}, containing only three behaviors: A (Theoretical Preview), B (Practical Listening), and C (Review and Assessment). The modules are chronologically indexed by study hours from 1 to {n}.

The semester learning sequence record is: {sequence}

Your goal is to detect whether a complete "ABC" golden learning closed-loop has been formed in this semester sequence (i.e., three consecutive study hour behaviors are A, B, and C in order).

Due to privacy protection constraints, you cannot directly access the full-cycle learning logs. You can only indirectly obtain information through the "Study Hour Analyzer". For each analysis, you need to provide a pair of integer nodes (L, R), where 1 less than or equal to L less than or equal to {n}, and 1 less than or equal to R less than or equal to {n}.

The system will map your (L, R) to an actual analyzed study hour set W according to a fixed but unknown "study hour inspection rule", then answer: does the complete golden learning closed-loop "ABC" exist within the hours corresponding to W (i.e., there exists a starting hour i such that i, i+1, i+2 are all in W, and the corresponding behaviors are A, B, C in order)?

There are four possible study hour inspection rules (fixed throughout the analysis):

Rule 1 (Standard semester closed interval):
  If L less than or equal to R, W contains all study hour nodes from L to R (closed interval);
  Otherwise W is empty.

Rule 2 (Countdown week closed interval):
  View the semester as counting down from the end to the beginning (the very end is 1, the very beginning is {n}).
  If L less than or equal to R, convert the countdown interval [L..R] to forward study hour indices, W is the converted set;
  Otherwise W is empty.

Rule 3 (Mid-term inspection open interval):
  If L less than R, W contains all study hour nodes greater than L and less than R (open interval, excluding start and end nodes);
  Otherwise W is empty.

Rule 4 (Cross-semester rolling circular closed interval):
  If L less than or equal to R, W contains all study hour nodes from L to R (closed interval);
  If L greater than R, W contains all nodes from L to {n} and from 1 to R (periodic rolling).

You need to complete the following tasks with as few analyses as possible:
1. Infer the true study hour inspection rule number (1, 2, 3, or 4)
2. Calculate the earliest starting study hour index K of the golden learning closed-loop "ABC" within the inspection scope for the specific inspection command (L={target_l}, R={target_r}) according to your inferred rule (K=0 if it doesn't exist)

## Query and Answer Format

For each analysis, use the following XML format (L and R separated by comma):

<query>L,R</query>

For example, to analyze L=1, R=5:

<query>1,5</query>

When submitting the comprehensive evaluation, specify the rule number you inferred and the calculated study hour K in the following format:

<answer>rule=1, k=3</answer>

Where rule is the rule number (1/2/3/4), and k is the earliest starting study hour of the learning closed-loop under inspection command (L={target_l}, R={target_r}) (0 if it doesn't exist).
"""

    contextualized_rule_zh_4 = """\
欢迎使用"自动化流水线工序校验系统"。我们来进行一次标准工艺流程排查，规则如下：

一条生产线上存在长度为 {n} 的工位状态日志序列 S，记录仅包含三种加工动作：A（上料成型）、B（精细打磨）、C（喷涂质检）。工位从始端到末端的正向编号为 1 到 {n}。

当前批次的工位日志序列为：{sequence}

你的目标是校验该批次日志中是否存在连续的标准合规工艺流"ABC"（即连续的三个工位加工动作依次为 A、B、C）。

由于安全合规协议，你不能直接读取全量原始日志，只能通过"工段审计台"来间接抽检。每次审计时，你需要输入一对整数工位编号 (L, R)，其中 1 小于等于 L 小于等于 {n}，1 小于等于 R 小于等于 {n}。

审计台会根据一个固定但未知的"工段截取规则"，将你提供的 (L, R) 映射为一个实际抽检的工位集合 W，然后回答：在 W 对应的工位范围内，是否存在完整的标准工艺流"ABC"（即存在某个起始工位 i，使得 i、i+1、i+2 都在 W 中，且对应的加工动作依次为 A、B、C）。

工段截取规则有四种可能（整批校验中规则固定不变）：

规则 1（正向流水段闭区间）：
  如果 L 小于等于 R，W 包含从工位 L 到 R 的所有节点（闭区间）；
  否则 W 为空集。

规则 2（尾端逆向溯源闭区间）：
  将生产线视为从末端向始端逆向回溯（最末端为 1，最始端为 {n}）。
  如果 L 小于等于 R，将逆向溯源区间 [L..R] 转换为正向流水编号，W 为转换后的集合；
  否则 W 为空集。

规则 3（排除首尾工位的开区间）：
  如果 L 小于 R，W 包含大于 L 且小于 R 的所有工位节点（开区间，剔除两端）；
  否则 W 为空集。

规则 4（环形传送带工位循环闭区间）：
  如果 L 小于等于 R，W 包含从 L 到 R 的所有工位（闭区间）；
  如果 L 大于 R，W 包含从 L 到 {n} 的所有工位，以及从 1 到 R 的所有工位（环形传送带首尾相接）。

你需要通过尽可能少的审计次数来完成以下任务：
1. 推断出真实的工段截取规则编号（1、2、3 或 4）
2. 计算在特定审计指令 (L={target_l}, R={target_r}) 下，按照你推断的规则，标准工艺流"ABC"在抽检范围中最先出现的起始工位编号 K（如果不存在则 K=0）

## 查询与提交答案的格式

每次审计时，使用以下 XML 格式（L 和 R 用逗号分隔）：

<query>L,R</query>

例如，审计 L=1, R=5：

<query>1,5</query>

提交质检报告时，需要说明你推断的规则编号和计算出的工位 K，格式如下：

<answer>rule=1, k=3</answer>

其中 rule 为规则编号（1/2/3/4），k 为在审计指令 (L={target_l}, R={target_r}) 下标准工艺流的最小起始工位（不存在则为 0）。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Automated Assembly Line Process Validation System". Let's perform a standard process flow inspection with the following rules:

There is a workstation status log sequence S of length {n} on a production line, containing only three processing actions: A (Feeding and Molding), B (Fine Grinding), and C (Coating and Inspection). The workstations are numbered from start to end from 1 to {n}.

The current batch workstation log sequence is: {sequence}

Your goal is to validate whether a continuous standard compliant process flow "ABC" exists in this batch log (i.e., three consecutive workstation actions are A, B, and C in order).

Due to safety and compliance protocols, you cannot directly read the full raw logs. You can only indirectly spot-check them through the "Section Audit Console". For each audit, you need to input a pair of integer workstation numbers (L, R), where 1 less than or equal to L less than or equal to {n}, and 1 less than or equal to R less than or equal to {n}.

The audit console will map your (L, R) to an actually inspected workstation set W according to a fixed but unknown "section interception rule", then answer: does the complete standard process flow "ABC" exist within the workstations corresponding to W (i.e., there exists a starting workstation i such that i, i+1, i+2 are all in W, and the corresponding actions are A, B, C in order)?

There are four possible section interception rules (fixed throughout the batch validation):

Rule 1 (Forward assembly section closed interval):
  If L less than or equal to R, W contains all nodes from workstation L to R (closed interval);
  Otherwise W is empty.

Rule 2 (Tail-end reverse traceability closed interval):
  View the production line as tracing backward from the end to the start (the very end is 1, the very start is {n}).
  If L less than or equal to R, convert the reverse traceability interval [L..R] to forward assembly numbers, W is the converted set;
  Otherwise W is empty.

Rule 3 (Open interval excluding start and end workstations):
  If L less than R, W contains all workstation nodes greater than L and less than R (open interval, excluding both ends);
  Otherwise W is empty.

Rule 4 (Circular conveyor belt workstation circular closed interval):
  If L less than or equal to R, W contains all workstations from L to R (closed interval);
  If L greater than R, W contains all workstations from L to {n} and from 1 to R (circular conveyor belt ends connected).

You need to complete the following tasks with as few audits as possible:
1. Infer the true section interception rule number (1, 2, 3, or 4)
2. Calculate the earliest starting workstation number K of the standard process flow "ABC" in the spot-check scope for the specific audit command (L={target_l}, R={target_r}) according to your inferred rule (K=0 if it doesn't exist)

## Query and Answer Format

For each audit, use the following XML format (L and R separated by comma):

<query>L,R</query>

For example, to audit L=1, R=5:

<query>1,5</query>

When submitting the quality inspection report, specify the rule number you inferred and the calculated workstation K in the following format:

<answer>rule=1, k=3</answer>

Where rule is the rule number (1/2/3/4), and k is the minimum starting workstation of the standard process flow under audit command (L={target_l}, R={target_r}) (0 if it doesn't exist).
"""

    contextualized_rule_zh_5 = """\
欢迎使用"案件卷宗证据链审查系统"。我们来进行一项司法程序复核任务，规则如下：

案件中归档了一份长度为 {n} 的程序推进记录序列 S，各项卷宗节点仅包含三种法定程序：A（确认违约事实）、B（下达正式催告）、C（提起诉讼立案）。卷宗节点按立案时间先后索引为 1 到 {n}。

当前案卷的推进序列内容为：{sequence}

你的目标是审查该卷宗中是否存在一条完整且连续的追诉证据链"ABC"（即连续的三个程序节点依次为 A、B、C）。

鉴于保密卷宗的权限隔离，你无法直接翻阅全部记录，只能通过"案卷调阅系统"间接核实。每次调阅时，你需要指定一对整数卷宗页码 (L, R)，其中 1 小于等于 L 小于等于 {n}，1 小于等于 R 小于等于 {n}。

系统会根据一个固定但未知的"调档审核规则"，将你提供的 (L, R) 映射为实际被审查的节点集合 W，然后回答：在 W 对应的调阅范围内，是否存在完整的追诉证据链"ABC"（即存在某个卷宗节点 i，使得 i、i+1、i+2 都在 W 中，且对应法定程序依次为 A、B、C）。

调档审核规则有四种可能（整个复核过程中规则固定不变）：

规则 1（标准顺延审理期闭区间）：
  如果 L 小于等于 R，W 包含从节点 L 到 R 的所有案卷（闭区间）；
  否则 W 为空集。

规则 2（倒查追溯期闭区间）：
  将案卷记录视为从最新进展向初始立案倒查（最新记录编号为 1，初始记录为 {n}）。
  如果 L 小于等于 R，将倒查区间 [L..R] 转换为正向的时间索引，W 为转换后的集合；
  否则 W 为空集。

规则 3（剔除立结案的中间审查期开区间）：
  如果 L 小于 R，W 包含大于 L 且小于 R 的所有案卷节点（开区间）；
  否则 W 为空集。

规则 4（跨年审计循环闭区间）：
  如果 L 小于等于 R，W 包含从 L 到 R 的所有案卷节点（闭区间）；
  如果 L 大于 R，W 包含从 L 到 {n} 的所有节点，以及从 1 到 R 的所有节点（年度结转跨越）。

你需要通过尽可能少的调阅次数来完成以下任务：
1. 推断出真实的调档审核规则编号（1、2、3 或 4）
2. 计算在特定调阅指令 (L={target_l}, R={target_r}) 下，按照你推断的规则，追诉证据链"ABC"在审查范围内最早成立的起始案卷节点 K（如果证据链不成立则 K=0）

## 查询与提交答案的格式

每次调阅时，使用以下 XML 格式（L 和 R 用逗号分隔）：

<query>L,R</query>

例如，调阅 L=1, R=5：

<query>1,5</query>

提交终审结案词时，需要说明你推断的规则编号和计算出的节点 K，格式如下：

<answer>rule=1, k=3</answer>

其中 rule 为规则编号（1/2/3/4），k 为在调阅指令 (L={target_l}, R={target_r}) 下追诉证据链的最早起始节点（不存在则为 0）。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Case File Evidence Chain Review System". Let's perform a judicial procedure review task with the following rules:

A sequence S of procedure progression records of length {n} has been archived in the case. The file nodes contain only three statutory procedures: A (Confirmation of Default Fact), B (Issuance of Formal Demand), and C (Filing for Litigation). The file nodes are indexed chronologically by filing time from 1 to {n}.

The current progression sequence content of the case file is: {sequence}

Your goal is to review whether a complete and continuous prosecution evidence chain "ABC" exists in this case file (i.e., three consecutive procedure nodes are A, B, and C in order).

Given the permission isolation of confidential files, you cannot browse all records directly. You can only indirectly verify them through the "Case File Requisition System". For each requisition, you need to specify a pair of integer file page numbers (L, R), where 1 less than or equal to L less than or equal to {n}, and 1 less than or equal to R less than or equal to {n}.

The system will map your (L, R) to an actually reviewed node set W according to a fixed but unknown "file audit rule", then answer: does the complete prosecution evidence chain "ABC" exist within the requisition scope corresponding to W (i.e., there exists a file node i such that i, i+1, i+2 are all in W, and the corresponding statutory procedures are A, B, C in order)?

There are four possible file audit rules (fixed throughout the review process):

Rule 1 (Standard extension trial period closed interval):
  If L less than or equal to R, W contains all case files from node L to R (closed interval);
  Otherwise W is empty.

Rule 2 (Retrospective investigation period closed interval):
  View the case file records as tracing backward from the latest progression to the initial filing (latest record is 1, initial record is {n}).
  If L less than or equal to R, convert the retrospective interval [L..R] to forward chronological indices, W is the converted set;
  Otherwise W is empty.

Rule 3 (Intermediate review period open interval excluding filing and closing):
  If L less than R, W contains all file nodes greater than L and less than R (open interval);
  Otherwise W is empty.

Rule 4 (Cross-year audit circular closed interval):
  If L less than or equal to R, W contains all file nodes from L to R (closed interval);
  If L greater than R, W contains all nodes from L to {n} and from 1 to R (annual carryover crossing).

You need to complete the following tasks with as few requisitions as possible:
1. Infer the true file audit rule number (1, 2, 3, or 4)
2. Calculate the earliest established starting file node K of the prosecution evidence chain "ABC" in the review scope for the specific requisition command (L={target_l}, R={target_r}) according to your inferred rule (K=0 if the evidence chain is not established)

## Query and Answer Format

For each requisition, use the following XML format (L and R separated by comma):

<query>L,R</query>

For example, to requisition L=1, R=5:

<query>1,5</query>

When submitting the final review closing statement, specify the rule number you inferred and the calculated node K in the following format:

<answer>rule=1, k=3</answer>

Where rule is the rule number (1/2/3/4), and k is the earliest starting node of the prosecution evidence chain under requisition command (L={target_l}, R={target_r}) (0 if it doesn't exist).
"""

    tags = ["answer", "query"]

    DIFFICULTY_CONFIG = {
        1: {
            "n": 8,
            "sequence": "A B C A B C A B",
            "rule": 1,
            "target_l": 2,
            "target_r": 6,
        },
        2: {
            "n": 10,
            "sequence": "A B A C B A B C B A",
            "rule": 3,
            "target_l": 5,
            "target_r": 9,
        },
        3: {
            "n": 14,
            "sequence": "A B C A B C B A C A B C A B",
            "rule": 4,
            "target_l": 12,
            "target_r": 3,
        },
        4: {
            "n": 12,
            "sequence": "A B C A B C B A C A B C",
            "rule": 2,
            "target_l": 3,
            "target_r": 8,
        },
        5: {
            "n": 16,
            "sequence": "B C A B A C B A B C A B C A B A",
            "rule": 4,
            "target_l": 15,
            "target_r": 4,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        # 初始化序列信息
        self.n = cfg["n"]
        self.sequence_str = cfg["sequence"]
        self.sequence = [x.strip() for x in cfg["sequence"].split()]
        
        # 窗口规则
        self.true_rule = cfg["rule"]
        
        # 目标查询参数
        self.target_l = cfg["target_l"]
        self.target_r = cfg["target_r"]
        
        # 查询计数
        self.query_count = 0
        
        # 设置游戏信息用于规则模板
        self._game_info = {
            "n": self.n,
            "sequence": self.sequence_str,
            "target_l": self.target_l,
            "target_r": self.target_r,
        }

    def _apply_window_rule(self, L, R, rule):
        """
        根据给定规则和查询参数，返回窗口索引集合 W（从1开始的索引）
        """
        W = set()
        
        if rule == 1:
            # 规则1：标准左到右闭区间
            if L <= R:
                W = set(range(L, R + 1))
                
        elif rule == 2:
            # 规则2：右到左编号闭区间
            # 从右到左编号：最右端为1，最左端为n
            # 右侧编号 i 对应左侧编号 (n - i + 1)
            if L <= R:
                # 将右侧 [L, R] 转换为左侧索引
                left_start = self.n - R + 1
                left_end = self.n - L + 1
                W = set(range(left_start, left_end + 1))
                
        elif rule == 3:
            # 规则3：左到右开区间
            if L < R:
                W = set(range(L + 1, R))
                
        elif rule == 4:
            # 规则4：循环闭区间
            if L <= R:
                W = set(range(L, R + 1))
            elif L > R:
                W = set(range(L, self.n + 1)) | set(range(1, R + 1))
                
        return W

    def _check_abc_in_window(self, W):
        """
        检查窗口 W 中是否存在完整的"ABC"模式
        返回：是否存在（布尔值）
        """
        for i in range(1, self.n - 1):  # i 从 1 到 n-2
            # 检查 i, i+1, i+2 是否都在 W 中
            if i in W and (i + 1) in W and (i + 2) in W:
                # 检查对应的元素是否为 A, B, C
                if (self.sequence[i - 1] == 'A' and 
                    self.sequence[i] == 'B' and 
                    self.sequence[i + 1] == 'C'):
                    return True
        return False

    def _find_min_abc_index(self, W):
        """
        在窗口 W 中找到"ABC"模式的最小起始索引
        返回：最小索引（不存在返回0）
        """
        for i in range(1, self.n - 1):
            if i in W and (i + 1) in W and (i + 2) in W:
                if (self.sequence[i - 1] == 'A' and 
                    self.sequence[i] == 'B' and 
                    self.sequence[i + 1] == 'C'):
                    return i
        return 0

    def evaluate(self, parsed_info):
        """
        评估最终答案是否正确
        """
        raw_ans = parsed_info["answer"]
        
        # 解析答案：rule=X, k=Y
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "rule" not in ans_dict or "k" not in ans_dict:
                return False
            
            # 检查规则编号
            guessed_rule = int(ans_dict["rule"])
            if guessed_rule != self.true_rule:
                return False
            
            # 计算正确的 K 值
            W_target = self._apply_window_rule(self.target_l, self.target_r, self.true_rule)
            correct_k = self._find_min_abc_index(W_target)
            
            # 检查 K 值
            guessed_k = int(ans_dict["k"])
            return guessed_k == correct_k
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """
        处理查询并返回响应（原始逻辑）
        """
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        self.query_count += 1
        
        try:
            # 解析查询参数
            raw_query = parsed_info["query"].strip()
            parts = [x.strip() for x in raw_query.split(",")]
            
            if len(parts) != 2:
                if self.config.language == "zh":
                    return "错误：查询格式无效，需要两个参数 L,R"
                else:
                    return "Error: Invalid query format, requires two parameters L,R"
            
            L = int(parts[0])
            R = int(parts[1])
            
            # 验证参数范围
            if L < 1 or L > self.n or R < 1 or R > self.n:
                if self.config.language == "zh":
                    return f"错误：参数超出范围，L 和 R 必须在 1 到 {self.n} 之间"
                else:
                    return f"Error: Parameters out of range, L and R must be between 1 and {self.n}"
            
            # 根据真实规则计算窗口
            W = self._apply_window_rule(L, R, self.true_rule)
            
            # 检查窗口中是否存在 ABC 模式
            has_abc = self._check_abc_in_window(W)
            
            if self.config.language == "zh":
                return "是" if has_abc else "否"
            else:
                return "Yes" if has_abc else "No"
                
        except ValueError:
            if self.config.language == "zh":
                return "错误：参数必须是整数"
            else:
                return "Error: Parameters must be integers"
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：{str(e)}"
            else:
                return f"Error: {str(e)}"

    def _cf_make_wrong(self, correct):
        """
        将正确的查询响应篡改为错误的响应（用于反事实干预模式）。
        """
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            else:
                return "是"
        else:
            if correct == "Yes":
                return "No"
            else:
                return "Yes"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        possible_queries = []
        # L 和 R 的范围都是 1 到 n
        for l in range(1, self.n + 1):
            for r in range(1, self.n + 1):
                # 构建查询字符串，必须包含 XML 标签
                query_str = f"<query>{l},{r}</query>"
                
                # 直接调用内部逻辑计算答案
                W = self._apply_window_rule(l, r, self.true_rule)
                has_abc = self._check_abc_in_window(W)
                
                # 根据语言生成答案
                if self.config.language == "zh":
                    ans = "是" if has_abc else "否"
                else:
                    ans = "Yes" if has_abc else "No"
                
                possible_queries.append({
                    "query": query_str,
                    "answer": ans
                })
        
        return possible_queries