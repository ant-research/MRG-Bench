from .base import Game
import random

class HiddenSequenceReconstructionGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    contextualized_rule_zh_1 = """\
欢迎使用城市智能交通路网诊断系统。
本系统记录了一条干道上连续的 {n} 个路口（按顺序编号）在特定高峰时段的交通流状态评级。每个路口的状态从集合 {{A, B, C, D}} 中取值（分别代表通畅、缓行、拥堵、严重拥堵）。系统已自动记录了这些固定状态，且整条干道并非单一状态。

你的任务是推断出关键路口 {k} 的交通流状态。为了防止直接干预该路口的数据流，你不能直接查询路口 {k}，也不能在任何操作中包含路口 {k}。

你有 {budget} 次系统调用机会，可以使用以下五种分析指令（每次仅限一种）：

1. 单点观察：查询特定路口 i 的状态（i 不能等于 {k}）
2. 相等比较：对比路口 i 和路口 j 的状态是否相同（i 和 j 均不能等于 {k}）
3. 区间计数：统计路段 [L, R] 中特定状态出现的次数（路段范围内不能包含路口 {k}）
4. 周期检验：检测路段 [L, R] 是否存在空间周期 p（即对于所有满足 L 小于等于 i 小于等于 R-p 的 i，路口 i 和路口 i+p 的状态完全一致，且这些路口都不能等于 {k}）
5. 镜像检验：检测路段 [L, R] 的状态分布是否呈镜像对称（即对于所有满足 0 小于等于 t 小于等于 R-L 的 t，路口 L+t 和路口 R-t 的状态相同，且涉及路口不能等于 {k}）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点观察（例如查询路口 3）：
<query_observe>3</query_observe>

- 相等比较（例如对比路口 2 和路口 5）：
<query_compare>2,5</query_compare>

- 区间计数（例如统计路段 [1, 4] 中状态 A 的数量）：
<query_count>1,4,A</query_count>

- 周期检验（例如测试路段 [1, 6] 的空间周期 2）：
<query_period>1,6,2</query_period>

- 镜像检验（例如测试路段 [2, 5] 是否镜像对称）：
<query_mirror>2,5</query_mirror>

提交最终诊断结论时，直接说明路口 {k} 的状态，格式如下：

<answer>A</answer>

注意：答案必须是 A、B、C、D 中的一个。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Intelligent Traffic Network Diagnostic System.
The system has recorded the traffic flow state ratings for {n} consecutive intersections (numbered sequentially) along a main arterial road during a specific peak period. The state of each intersection takes a value from the set {{A, B, C, D}} (representing Smooth, Slow, Congested, and Severely Congested, respectively). The system has secretly logged these fixed states, forming a sequence (not all intersections share the same state).

Your objective is to infer the traffic state at the critical intersection {k}. To prevent direct interference with the data stream of this node, you cannot query intersection {k} directly, nor can you involve intersection {k} in any operations.

You have {budget} system call opportunities and can use the following five analytical commands (one per turn):

1. Single Observation: Query the state of specific intersection i (i cannot equal {k})
2. Equality Comparison: Check if intersections i and j share the same state (neither i nor j can equal {k})
3. Range Count: Count how many times a specific state appears in the road segment [L, R] (the segment cannot include intersection {k})
4. Period Check: Test if the road segment [L, R] exhibits a spatial period p (i.e., for all i satisfying L less than or equal to i less than or equal to R-p, intersections i and i+p have the identical state, and these intersections cannot equal {k})
5. Mirror Check: Verify if the state distribution in the road segment [L, R] is mirror-symmetric (i.e., for all t satisfying 0 less than or equal to t less than or equal to R-L, intersections L+t and R-t have the same state, and these intersections cannot equal {k})

Each query must contain only one tag. Use the following XML format:

- Single Observation (e.g., query intersection 3):
<query_observe>3</query_observe>

- Equality Comparison (e.g., compare intersections 2 and 5):
<query_compare>2,5</query_compare>

- Range Count (e.g., count state A in segment [1, 4]):
<query_count>1,4,A</query_count>

- Period Check (e.g., test period 2 in segment [1, 6]):
<query_period>1,6,2</query_period>

- Mirror Check (e.g., test if segment [2, 5] is mirror-symmetric):
<query_mirror>2,5</query_mirror>

When submitting the final diagnostic conclusion, directly specify the state at intersection {k}, using this format:

<answer>A</answer>

Note: The answer must be one of A, B, C, or D.
"""

    contextualized_rule_zh_2 = """\
欢迎使用临床基因组学序列推演辅助系统。
系统对某异常基因链的 {n} 个连续位点进行了靶向测序。每个位点的核苷酸由集合 {{A, B, C, D}} 表示（分别代表腺嘌呤、胸腺嘧啶、胞嘧啶和鸟嘌呤的突变分型）。系统已锁定了一个固定的核苷酸序列（并非完全纯合）。

你的临床推断目标是确定靶点突变位点 {k} 的核苷酸类型。由于测序盲区限制，你无法直接读取位点 {k} 的信息，也严禁在任何探针查询中覆盖位点 {k}。

你有 {budget} 次测序探针调用机会，可使用以下五种测序分析策略（每次限用一种）：

1. 单点观察：检测特定位点 i 的核苷酸类型（i 不能等于 {k}）
2. 相等比较：比对位点 i 和位点 j 的核苷酸是否相同（i 和 j 均不能等于 {k}）
3. 区间计数：统计基因片段 [L, R] 中某种特定核苷酸的数量（片段区间不能包含位点 {k}）
4. 周期检验：分析基因片段 [L, R] 是否具备重复序列周期 p（即对于所有满足 L 小于等于 i 小于等于 R-p 的 i，位点 i 和位点 i+p 核苷酸相同，且不能涉及位点 {k}）
5. 镜像检验：验证基因片段 [L, R] 是否构成回文镜像对称（即对于所有满足 0 小于等于 t 小于等于 R-L 的 t，位点 L+t 和位点 R-t 核苷酸相同，且不能涉及位点 {k}）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点观察（例如检测位点 3）：
<query_observe>3</query_observe>

- 相等比较（例如比对位点 2 和位点 5）：
<query_compare>2,5</query_compare>

- 区间计数（例如统计片段 [1, 4] 中核苷酸 A 的数量）：
<query_count>1,4,A</query_count>

- 周期检验（例如测试片段 [1, 6] 的串联重复周期 2）：
<query_period>1,6,2</query_period>

- 镜像检验（例如测试片段 [2, 5] 是否回文对称）：
<query_mirror>2,5</query_mirror>

提交最终临床推断结论时，直接说明位点 {k} 的核苷酸，格式如下：

<answer>A</answer>

注意：答案必须是 A、B、C、D 中的一个。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Clinical Genomics Sequence Inference Assistant.
The system has performed targeted sequencing on {n} consecutive loci of an abnormal genetic chain. The nucleotide at each locus is represented by the set {{A, B, C, D}} (indicating mutation subtypes of Adenine, Thymine, Cytosine, and Guanine). The system has locked in a fixed sequence (not entirely homozygous).

Your clinical inference objective is to determine the nucleotide type at the target mutation locus {k}. Due to sequencing blind spots, you cannot directly read locus {k}, nor can you cover locus {k} in any probe queries.

You have {budget} sequencing probe calls available, utilizing the following five analytical strategies (one per turn):

1. Single Observation: Detect the nucleotide type at specific locus i (i cannot equal {k})
2. Equality Comparison: Compare if the nucleotides at locus i and locus j are identical (neither i nor j can equal {k})
3. Range Count: Count the occurrences of a specific nucleotide in the gene segment [L, R] (the segment cannot include locus {k})
4. Period Check: Analyze if the gene segment [L, R] has a tandem repeat period p (i.e., for all i satisfying L less than or equal to i less than or equal to R-p, loci i and i+p share the same nucleotide, and these loci cannot equal {k})
5. Mirror Check: Verify if the gene segment [L, R] forms a palindromic mirror symmetry (i.e., for all t satisfying 0 less than or equal to t less than or equal to R-L, loci L+t and R-t have the same nucleotide, and these loci cannot equal {k})

Each query must contain only one tag. Use the following XML format:

- Single Observation (e.g., detect locus 3):
<query_observe>3</query_observe>

- Equality Comparison (e.g., compare loci 2 and 5):
<query_compare>2,5</query_compare>

- Range Count (e.g., count nucleotide A in segment [1, 4]):
<query_count>1,4,A</query_count>

- Period Check (e.g., test tandem repeat period 2 in segment [1, 6]):
<query_period>1,6,2</query_period>

- Mirror Check (e.g., test if segment [2, 5] is palindromic):
<query_mirror>2,5</query_mirror>

When submitting the final clinical inference, directly specify the nucleotide at locus {k}, using this format:

<answer>A</answer>

Note: The answer must be one of A, B, C, or D.
"""

    contextualized_rule_zh_3 = """\
欢迎进入学生学情轨迹纵向追踪平台。
本平台收录了某学生在特定学科上的 {n} 次连续随堂测评结果。每次测评的知识掌握评级取自集合 {{A, B, C, D}}（分别对应优秀、良好、及格、待达标）。系统生成了一组反映其学习波动的固有测评序列（并非所有次成绩均一致）。

你的教学干预目标是推断出关键的第 {k} 次测评评级。受限于防作弊与盲测机制，你无法直接调取第 {k} 次的成绩档案，且任何学情数据查询均不可涵盖该次测评。

你有 {budget} 次学情检索额度，可以使用以下五种学情分析工具（每次仅限一项）：

1. 单点观察：查阅第 i 次测评的成绩评级（i 不能等于 {k}）
2. 相等比较：对比第 i 次和第 j 次测评的评级是否一致（i 和 j 均不能等于 {k}）
3. 区间计数：统计在第 [L, R] 次测评区间内某项评级获得的次数（测评区间不能包含第 {k} 次）
4. 周期检验：分析测评区间 [L, R] 是否存在成绩波动的周期 p（即对于所有满足 L 小于等于 i 小于等于 R-p 的 i，第 i 次和第 i+p 次评级完全相同，且不能涉及第 {k} 次）
5. 镜像检验：检验测评区间 [L, R] 的成绩走势是否呈现镜像对称（即对于所有满足 0 小于等于 t 小于等于 R-L 的 t，第 L+t 次和第 R-t 次评级相同，且不能涉及第 {k} 次）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点观察（例如查阅第 3 次测评）：
<query_observe>3</query_observe>

- 相等比较（例如对比第 2 和第 5 次测评）：
<query_compare>2,5</query_compare>

- 区间计数（例如统计第 [1, 4] 次测评中获得评级 A 的次数）：
<query_count>1,4,A</query_count>

- 周期检验（例如测试区间 [1, 6] 的波动周期 2）：
<query_period>1,6,2</query_period>

- 镜像检验（例如测试区间 [2, 5] 成绩走势是否镜像对称）：
<query_mirror>2,5</query_mirror>

提交最终学情推断结论时，直接说明第 {k} 次测评的评级，格式如下：

<answer>A</answer>

注意：答案必须是 A、B、C、D 中的一个。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Student Academic Trajectory Longitudinal Tracking Platform.
This platform has recorded {n} consecutive quiz results for a specific student in a subject. The knowledge mastery rating for each quiz is drawn from the set {{A, B, C, D}} (representing Excellent, Good, Pass, and Needs Improvement). The system holds a fixed inherent sequence reflecting their learning fluctuations (not all quiz ratings are identical).

Your pedagogical intervention goal is to infer the mastery rating of the critical {k}-th quiz. Restricted by blind-test and anti-cheating mechanisms, you cannot directly access the record for the {k}-th quiz, and no academic data queries may encompass this quiz.

You have {budget} academic retrieval quotas and can utilize the following five learning analysis tools (one per turn):

1. Single Observation: Review the rating of the i-th quiz (i cannot equal {k})
2. Equality Comparison: Check if the ratings of the i-th and j-th quizzes are consistent (neither i nor j can equal {k})
3. Range Count: Count how many times a specific rating was achieved within the quiz interval [L, R] (the interval cannot include the {k}-th quiz)
4. Period Check: Analyze if the quiz interval [L, R] exhibits a performance fluctuation period p (i.e., for all i satisfying L less than or equal to i less than or equal to R-p, the i-th and (i+p)-th quiz ratings are completely identical, and these cannot involve the {k}-th quiz)
5. Mirror Check: Verify if the performance trend in quiz interval [L, R] presents a mirror symmetry (i.e., for all t satisfying 0 less than or equal to t less than or equal to R-L, the (L+t)-th and (R-t)-th quiz ratings are identical, and these cannot involve the {k}-th quiz)

Each query must contain only one tag. Use the following XML format:

- Single Observation (e.g., review the 3rd quiz):
<query_observe>3</query_observe>

- Equality Comparison (e.g., compare the 2nd and 5th quizzes):
<query_compare>2,5</query_compare>

- Range Count (e.g., count the occurrences of rating A in the interval [1, 4]):
<query_count>1,4,A</query_count>

- Period Check (e.g., test fluctuation period 2 in interval [1, 6]):
<query_period>1,6,2</query_period>

- Mirror Check (e.g., test if the trend in interval [2, 5] is mirror-symmetric):
<query_mirror>2,5</query_mirror>

When submitting your final pedagogical inference, directly specify the rating of the {k}-th quiz, using this format:

<answer>A</answer>

Note: The answer must be one of A, B, C, or D.
"""

    contextualized_rule_zh_4 = """\
欢迎登录智能制造质量控制与缺陷溯源系统。
我们的自动化产线刚完成了 {n} 个连续批次（按生产顺序编号）的组件制造。每个批次的质检等级从集合 {{A, B, C, D}} 中评定（分别代表优等品、一等品、合格品和残次品）。系统后台记录了这组固定的质量分布序列（各批次质量并非完全一样）。

你的品控任务是推断出核心批次 {k} 的质检等级。由于核心批次样本正处于隔离封存状态，你不能直接调取批次 {k} 的品控参数，也不能在任何抽检指令中包含批次 {k}。

你有 {budget} 次质量检验操作权限，可使用以下五种工业分析指令（每次限用一种）：

1. 单点观察：提取特定批次 i 的质检等级（i 不能等于 {k}）
2. 相等比较：对比批次 i 和批次 j 的质检等级是否相同（i 和 j 均不能等于 {k}）
3. 区间计数：统计生产批次区间 [L, R] 内某特定等级出现的频次（区间内不能包含批次 {k}）
4. 周期检验：检测批次区间 [L, R] 中是否存在工艺偏差周期 p（即对于所有满足 L 小于等于 i 小于等于 R-p 的 i，批次 i 和批次 i+p 的等级完全一致，且均不能涉及批次 {k}）
5. 镜像检验：验证批次区间 [L, R] 的质量分布是否呈镜像对称（即对于所有满足 0 小于等于 t 小于等于 R-L 的 t，批次 L+t 和批次 R-t 等级相同，且均不能涉及批次 {k}）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点观察（例如提取批次 3）：
<query_observe>3</query_observe>

- 相等比较（例如对比批次 2 和批次 5）：
<query_compare>2,5</query_compare>

- 区间计数（例如统计区间 [1, 4] 中等级 A 的批次数量）：
<query_count>1,4,A</query_count>

- 周期检验（例如测试区间 [1, 6] 的工艺周期 2）：
<query_period>1,6,2</query_period>

- 镜像检验（例如测试区间 [2, 5] 的质量分布是否镜像对称）：
<query_mirror>2,5</query_mirror>

提交最终缺陷溯源结论时，直接说明批次 {k} 的质检等级，格式如下：

<answer>A</answer>

注意：答案必须是 A、B、C、D 中的一个。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the Smart Manufacturing Quality Control and Defect Traceability System.
Our automated production line has just completed manufacturing {n} consecutive batches of components (numbered by production sequence). The quality inspection grade for each batch is assessed from the set {{A, B, C, D}} (representing Premium, First-Class, Qualified, and Defective, respectively). The system backend has recorded this fixed quality distribution sequence (the batches are not all of uniform quality).

Your quality control task is to infer the inspection grade of the core batch {k}. Because the core batch samples are currently isolated and sealed, you cannot directly retrieve the QA parameters for batch {k}, nor can you include batch {k} in any sampling instructions.

You have {budget} quality inspection operation privileges and can use the following five industrial analysis commands (one per turn):

1. Single Observation: Extract the inspection grade of specific batch i (i cannot equal {k})
2. Equality Comparison: Compare if batch i and batch j share the same inspection grade (neither i nor j can equal {k})
3. Range Count: Count the frequency of a specific grade within the production batch interval [L, R] (the interval cannot include batch {k})
4. Period Check: Detect if there is a process deviation period p in the batch interval [L, R] (i.e., for all i satisfying L less than or equal to i less than or equal to R-p, batches i and i+p have identical grades, and neither can involve batch {k})
5. Mirror Check: Verify if the quality distribution in the batch interval [L, R] is mirror-symmetric (i.e., for all t satisfying 0 less than or equal to t less than or equal to R-L, batches L+t and R-t share the same grade, and neither can involve batch {k})

Each query must contain only one tag. Use the following XML format:

- Single Observation (e.g., extract batch 3):
<query_observe>3</query_observe>

- Equality Comparison (e.g., compare batches 2 and 5):
<query_compare>2,5</query_compare>

- Range Count (e.g., count grade A batches in interval [1, 4]):
<query_count>1,4,A</query_count>

- Period Check (e.g., test process period 2 in interval [1, 6]):
<query_period>1,6,2</query_period>

- Mirror Check (e.g., test if quality distribution in interval [2, 5] is mirror-symmetric):
<query_mirror>2,5</query_mirror>

When submitting the final defect traceability conclusion, directly specify the inspection grade of batch {k}, using this format:

<answer>A</answer>

Note: The answer must be one of A, B, C, or D.
"""

    contextualized_rule_zh_5 = """\
欢迎使用司法判例类型化分析与类案检索系统。
本系统整理了按时间顺序归档的 {n} 个关联历史判例。每个判例的法理适用类型被严格归入集合 {{A, B, C, D}} 中（分别代表驳回诉讼、部分支持、全部支持和发回重审）。系统已内置了这组确定的裁判链条（并非所有判例判决均一致）。

你的司法研判任务是推断出关键的第 {k} 号争议判例的适用类型。为保证研判程序的独立性，你被禁止直接查阅第 {k} 号判例的卷宗，同时任何卷宗批量检索条件中均不可包含第 {k} 号判例。

你有 {budget} 次司法数据库检索配额，可以使用以下五种法理分析工具（每次仅限一种）：

1. 单点观察：调阅第 i 号判例的适用类型（i 不能等于 {k}）
2. 相等比较：对比第 i 号和第 j 号判例的适用类型是否一致（i 和 j 均不能等于 {k}）
3. 区间计数：统计在第 [L, R] 号判例区间中，特定适用类型作出的次数（卷宗区间不能包含第 {k} 号判例）
4. 周期检验：审查第 [L, R] 号判例区间内是否具有裁判尺度波动的周期 p（即对于所有满足 L 小于等于 i 小于等于 R-p 的 i，第 i 号和第 i+p 号判例适用类型完全相同，且不可涉及第 {k} 号判例）
5. 镜像检验：验证第 [L, R] 号判例区间的裁判演化是否呈现镜像对称（即对于所有满足 0 小于等于 t 小于等于 R-L 的 t，第 L+t 号和第 R-t 号判例适用类型相同，且不可涉及第 {k} 号判例）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点观察（例如调阅第 3 号判例）：
<query_observe>3</query_observe>

- 相等比较（例如对比第 2 和第 5 号判例）：
<query_compare>2,5</query_compare>

- 区间计数（例如统计在第 [1, 4] 号判例区间中类型 A 的数量）：
<query_count>1,4,A</query_count>

- 周期检验（例如测试判例区间 [1, 6] 的裁判波动周期 2）：
<query_period>1,6,2</query_period>

- 镜像检验（例如测试判例区间 [2, 5] 裁判演化是否镜像对称）：
<query_mirror>2,5</query_mirror>

提交最终司法研判结论时，直接说明第 {k} 号判例的适用类型，格式如下：

<answer>A</answer>

注意：答案必须是 A、B、C、D 中的一个。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Judicial Precedent Typological Analysis and Case Retrieval System.
This system has curated {n} chronologically archived, interconnected historical precedents. The jurisprudential application type for each precedent is strictly classified into the set {{A, B, C, D}} (representing Case Dismissed, Partially Supported, Fully Supported, and Remanded for Retrial, respectively). The system has embedded this fixed chain of judgments (the precedents are not uniformly judged).

Your judicial deliberation task is to infer the application type of the critical disputed precedent No. {k}. To ensure the independence of the deliberation procedure, you are prohibited from directly reviewing the dossier of precedent No. {k}, and no bulk dossier retrieval criteria may encompass precedent No. {k}.

You have {budget} judicial database retrieval quotas and can use the following five jurisprudential analysis tools (one per turn):

1. Single Observation: Access the application type of precedent No. i (i cannot equal {k})
2. Equality Comparison: Check if the application types of precedents No. i and No. j are identical (neither i nor j can equal {k})
3. Range Count: Count the frequency of a specific application type within the precedent interval [L, R] (the dossier interval cannot include precedent No. {k})
4. Period Check: Examine if the precedent interval [L, R] exhibits a judgment standard fluctuation period p (i.e., for all i satisfying L less than or equal to i less than or equal to R-p, precedents No. i and No. i+p share the identical application type, and neither can involve precedent No. {k})
5. Mirror Check: Verify if the evolution of judgments in the precedent interval [L, R] demonstrates mirror symmetry (i.e., for all t satisfying 0 less than or equal to t less than or equal to R-L, precedents No. L+t and No. R-t share the same application type, and neither can involve precedent No. {k})

Each query must contain only one tag. Use the following XML format:

- Single Observation (e.g., access precedent No. 3):
<query_observe>3</query_observe>

- Equality Comparison (e.g., compare precedents No. 2 and No. 5):
<query_compare>2,5</query_compare>

- Range Count (e.g., count type A in precedent interval [1, 4]):
<query_count>1,4,A</query_count>

- Period Check (e.g., test judgment fluctuation period 2 in interval [1, 6]):
<query_period>1,6,2</query_period>

- Mirror Check (e.g., test if judgment evolution in interval [2, 5] is mirror-symmetric):
<query_mirror>2,5</query_mirror>

When submitting your final judicial deliberation conclusion, directly specify the application type of precedent No. {k}, using this format:

<answer>A</answer>

Note: The answer must be one of A, B, C, or D.
"""

    game_rule_zh = """\
我们现在来玩一个"隐藏序列推断"游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列，每个位置的元素从符号集合 {{A, B, C, D}} 中取值。我已经秘密为每个位置分配了一个符号，构成了一个固定的序列（不是所有位置都相同）。

你的目标是推断出目标位置 {k} 的符号。但是，你不能直接询问位置 {k}，也不能在任何查询中涉及位置 {k}。

你有 {budget} 次查询机会，可以使用以下五种查询方式（每次只能使用一种）：

1. 单点观察：询问某个位置 i 的符号是什么（i 不能等于 {k}）
2. 相等比较：询问位置 i 和位置 j 的符号是否相同（i 和 j 都不能等于 {k}）
3. 区间计数：询问区间 [L, R] 中某个符号出现的次数（区间内不能包含位置 {k}）
4. 周期检验：询问区间 [L, R] 是否存在周期 p（即对于所有满足 L 小于等于 i 小于等于 R-p 的 i，位置 i 和位置 i+p 的符号都相同，且这些位置都不能等于 {k}）
5. 镜像检验：询问区间 [L, R] 是否镜像对称（即对于所有满足 0 小于等于 t 小于等于 R-L 的 t，位置 L+t 和位置 R-t 的符号都相同，且这些位置都不能等于 {k}）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 单点观察（例如询问位置 3）：
<query_observe>3</query_observe>

- 相等比较（例如比较位置 2 和位置 5）：
<query_compare>2,5</query_compare>

- 区间计数（例如统计区间 [1, 4] 中符号 A 的数量）：
<query_count>1,4,A</query_count>

- 周期检验（例如测试区间 [1, 6] 的周期 2）：
<query_period>1,6,2</query_period>

- 镜像检验（例如测试区间 [2, 5] 是否镜像对称）：
<query_mirror>2,5</query_mirror>

提交最终答案时，直接说明位置 {k} 的符号，格式如下：

<answer>A</answer>

注意：答案必须是 A、B、C、D 中的一个。
"""

    game_rule_en = """\
Let's play a "Hidden Sequence Reconstruction" game. Here are the rules:

A sequence of length {n} has been set up, where each position contains a symbol from the set {{A, B, C, D}}. I have secretly assigned a symbol to each position, forming a fixed sequence (not all positions are the same).

Your goal is to infer the symbol at target position {k}. However, you cannot directly query position {k}, nor can you involve position {k} in any query.

You have {budget} query opportunities and can use the following five query types (one per turn):

1. Single Observation: Ask what symbol is at position i (i cannot equal {k})
2. Equality Comparison: Ask if positions i and j have the same symbol (neither i nor j can equal {k})
3. Range Count: Ask how many times a symbol appears in range [L, R] (the range cannot include position {k})
4. Period Check: Ask if range [L, R] has period p (i.e., for all i satisfying L less than or equal to i less than or equal to R-p, positions i and i+p have the same symbol, and these positions cannot equal {k})
5. Mirror Check: Ask if range [L, R] is mirror-symmetric (i.e., for all t satisfying 0 less than or equal to t less than or equal to R-L, positions L+t and R-t have the same symbol, and these positions cannot equal {k})

Each query must contain only one tag. Use the following XML format:

- Single Observation (e.g., query position 3):
<query_observe>3</query_observe>

- Equality Comparison (e.g., compare positions 2 and 5):
<query_compare>2,5</query_compare>

- Range Count (e.g., count symbol A in range [1, 4]):
<query_count>1,4,A</query_count>

- Period Check (e.g., test period 2 in range [1, 6]):
<query_period>1,6,2</query_period>

- Mirror Check (e.g., test if range [2, 5] is mirror-symmetric):
<query_mirror>2,5</query_mirror>

When submitting the final answer, directly specify the symbol at position {k}, using this format:

<answer>A</answer>

Note: The answer must be one of A, B, C, or D.
"""

    tags = ["answer", "query_observe", "query_compare", "query_count", "query_period", "query_mirror"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "k": 3,
                "budget": 10,
                "sequence": "A,B,A,B,A",
            },
            2: {
                "n": 7,
                "k": 4,
                "budget": 12,
                "sequence": "A,B,C,D,C,B,A",
            },
            3: {
                "n": 9,
                "k": 5,
                "budget": 14,
                "sequence": "A,B,C,A,B,C,A,B,C",
            },
            4: {
                "n": 11,
                "k": 6,
                "budget": 16,
                "sequence": "A,A,B,B,C,D,C,B,B,A,A",
            },
            5: {
                "n": 13,
                "k": 7,
                "budget": 18,
                "sequence": "A,B,A,C,B,C,D,C,B,C,A,B,A",
            },
        },
        "en": {
            1: {
                "n": 5,
                "k": 3,
                "budget": 10,
                "sequence": "A,B,A,B,A",
            },
            2: {
                "n": 7,
                "k": 4,
                "budget": 12,
                "sequence": "A,B,C,D,C,B,A",
            },
            3: {
                "n": 9,
                "k": 5,
                "budget": 14,
                "sequence": "A,B,C,A,B,C,A,B,C",
            },
            4: {
                "n": 11,
                "k": 6,
                "budget": 16,
                "sequence": "A,A,B,B,C,D,C,B,B,A,A",
            },
            5: {
                "n": 13,
                "k": 7,
                "budget": 18,
                "sequence": "A,B,A,C,B,C,D,C,B,C,A,B,A",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)
        self.query_count = 0

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]
        self._game_info["budget"] = cfg["budget"]
        
        symbols = cfg["sequence"].split(",")
        self.sequence = {str(i+1): sym.strip() for i, sym in enumerate(symbols)}
        self.target_k = str(cfg["k"])
        self.budget = cfg["budget"]
        self.answer = self.sequence[self.target_k]

    def evaluate(self, parsed_info):
        submitted_answer = parsed_info["answer"].strip().upper()
        
        if submitted_answer not in ["A", "B", "C", "D"]:
            return False
        
        return submitted_answer == self.answer

    def _cf_core_produce(self, parsed_info):
        self.query_count += 1
        if self.query_count > self.budget:
            raise ValueError(
                f"Query budget exceeded: {self.query_count} > {self.budget}" 
                if self.config.language == "en" 
                else f"查询次数超出预算：{self.query_count} > {self.budget}"
            )

        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            same_res, diff_res = "相同", "不同"
            valid_res, invalid_res = "成立", "不成立"
            error_range = "错误：位置超出范围。"
            error_involve_k = "错误：查询涉及目标位置 {k}。".format(k=self.target_k)
            error_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            same_res, diff_res = "Same", "Different"
            valid_res, invalid_res = "Valid", "Invalid"
            error_range = "Error: Position out of range."
            error_involve_k = f"Error: Query involves target position {self.target_k}."
            error_format = "Error: Invalid format."

        if "query_observe" in parsed_info:
            try:
                pos = parsed_info["query_observe"].strip()
                if pos not in self.sequence:
                    return error_range
                if pos == self.target_k:
                    return error_involve_k
                return self.sequence[pos]
            except:
                return error_format

        elif "query_compare" in parsed_info:
            try:
                parts = [x.strip() for x in parsed_info["query_compare"].split(",")]
                if len(parts) != 2:
                    return error_format
                pos1, pos2 = parts
                if pos1 not in self.sequence or pos2 not in self.sequence:
                    return error_range
                if pos1 == self.target_k or pos2 == self.target_k:
                    return error_involve_k
                return same_res if self.sequence[pos1] == self.sequence[pos2] else diff_res
            except:
                return error_format

        elif "query_count" in parsed_info:
            try:
                parts = [x.strip() for x in parsed_info["query_count"].split(",")]
                if len(parts) != 3:
                    return error_format
                L, R, symbol = parts
                L_int, R_int = int(L), int(R)
                
                if L_int < 1 or R_int > int(self._game_info["n"]) or L_int > R_int:
                    return error_range
                if symbol not in ["A", "B", "C", "D"]:
                    return error_format
                
                target_k_int = int(self.target_k)
                if L_int <= target_k_int <= R_int:
                    return error_involve_k
                
                count = 0
                for i in range(L_int, R_int + 1):
                    if self.sequence[str(i)] == symbol:
                        count += 1
                return str(count)
            except:
                return error_format

        elif "query_period" in parsed_info:
            try:
                parts = [x.strip() for x in parsed_info["query_period"].split(",")]
                if len(parts) != 3:
                    return error_format
                L, R, p = parts
                L_int, R_int, p_int = int(L), int(R), int(p)
                
                if L_int < 1 or R_int > int(self._game_info["n"]) or L_int > R_int or p_int <= 0:
                    return error_range
                
                target_k_int = int(self.target_k)
                
                for i in range(L_int, R_int - p_int + 1):
                    if i == target_k_int or i + p_int == target_k_int:
                        return error_involve_k
                    if self.sequence[str(i)] != self.sequence[str(i + p_int)]:
                        return invalid_res
                return valid_res
            except:
                return error_format

        elif "query_mirror" in parsed_info:
            try:
                parts = [x.strip() for x in parsed_info["query_mirror"].split(",")]
                if len(parts) != 2:
                    return error_format
                L, R = parts
                L_int, R_int = int(L), int(R)
                
                if L_int < 1 or R_int > int(self._game_info["n"]) or L_int > R_int:
                    return error_range
                
                target_k_int = int(self.target_k)
                
                for t in range(R_int - L_int + 1):
                    left_pos = L_int + t
                    right_pos = R_int - t
                    if left_pos == target_k_int or right_pos == target_k_int:
                        return error_involve_k
                    if self.sequence[str(left_pos)] != self.sequence[str(right_pos)]:
                        return invalid_res
                return valid_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        symbols = ["A", "B", "C", "D"]
        if correct.strip().upper() in symbols:
            wrong_choices = [s for s in symbols if s != correct.strip().upper()]
            return random.choice(wrong_choices)
        
        if correct.lstrip('-').isdigit():
            val = int(correct)
            return str(val + 1)
        
        zh_flip = {"是": "否", "否": "是", "相同": "不同", "不同": "相同",
                   "成立": "不成立", "不成立": "成立"}
        if correct in zh_flip:
            return zh_flip[correct]
        
        en_flip = {"Yes": "No", "No": "Yes", "Same": "Different", "Different": "Same",
                   "Valid": "Invalid", "Invalid": "Valid"}
        if correct in en_flip:
            return en_flip[correct]
        for k_word, v_word in en_flip.items():
            if correct.lower() == k_word.lower():
                return v_word
        
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = int(self._game_info["n"])
        k = int(self.target_k)
        
        if self.config.language == "zh":
            same_res, diff_res = "相同", "不同"
            valid_res, invalid_res = "成立", "不成立"
        else:
            same_res, diff_res = "Same", "Different"
            valid_res, invalid_res = "Valid", "Invalid"

        for i in range(1, n + 1):
            if i == k:
                continue
            q_str = f"<query_observe>{i}</query_observe>"
            ans = self.sequence[str(i)]
            queries.append({"query": q_str, "answer": ans})

        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if i == k or j == k:
                    continue
                q_str = f"<query_compare>{i},{j}</query_compare>"
                ans = same_res if self.sequence[str(i)] == self.sequence[str(j)] else diff_res
                queries.append({"query": q_str, "answer": ans})

        for L in range(1, n + 1):
            for R in range(L, n + 1):
                if L <= k <= R:
                    continue
                for sym in ["A", "B", "C", "D"]:
                    q_str = f"<query_count>{L},{R},{sym}</query_count>"
                    count = 0
                    for i in range(L, R + 1):
                        if self.sequence[str(i)] == sym:
                            count += 1
                    queries.append({"query": q_str, "answer": str(count)})

        for L in range(1, n + 1):
            for R in range(L, n + 1):
                max_p = R - L
                if max_p < 1:
                    continue
                
                for p in range(1, max_p + 1):
                    involved = False
                    is_periodic = True
                    
                    for i in range(L, R - p + 1):
                        if i == k or (i + p) == k:
                            involved = True
                            break
                        if self.sequence[str(i)] != self.sequence[str(i + p)]:
                            is_periodic = False
                            break
                    
                    if involved:
                        continue
                    
                    q_str = f"<query_period>{L},{R},{p}</query_period>"
                    ans = valid_res if is_periodic else invalid_res
                    queries.append({"query": q_str, "answer": ans})

        for L in range(1, n + 1):
            for R in range(L, n + 1):
                involved = False
                is_mirror = True
                
                for t in range(R - L + 1):
                    left_pos = L + t
                    right_pos = R - t
                    if left_pos == k or right_pos == k:
                        involved = True
                        break
                    if self.sequence[str(left_pos)] != self.sequence[str(right_pos)]:
                        is_mirror = False
                        break
                
                if involved:
                    continue
                
                q_str = f"<query_mirror>{L},{R}</query_mirror>"
                ans = valid_res if is_mirror else invalid_res
                queries.append({"query": q_str, "answer": ans})

        return queries