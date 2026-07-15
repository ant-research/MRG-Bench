from .base import Game
import random

class PatternRecognitionGame(Game):

    game_rule_zh = """\
我们来玩一个"序列生成机制推断"游戏。规则如下：

我拥有一个长度为 36 的有序序列 S，其中每个位置的元素取自符号集 {{A, B, C, D}}。这个序列是由一个长度为 p 的基础图样 M 按照某种机制生成的，其中 p 可能是 3、4 或 5。基础图样 M 至少包含两种不同的符号。

生成机制只有以下三种可能：

1. **机制 A（直接重复）**：序列由基础图样 M 直接重复拼接而成。即第 b 个块的内容与 M 完全相同。

2. **机制 B（反向交替）**：奇数块（第 1、3、5...块）的内容等于 M，偶数块（第 2、4、6...块）的内容等于 M 的反向序列。注意 M 本身不是回文串。

3. **机制 C（逐步循环移位）**：第 b 个块等于将 M 右循环位移 (b−1) 位所得的结果。M 不存在更短的非平凡周期。

说明：每个块的长度均为 p，块的编号 b 从 1 开始计数。如果序列在 36 个位置处截断了某个块，那么该块的已定义位置仍按对应机制生成。

你的目标是通过查询推断出：
- 采用的生成机制（A、B 或 C）
- 基础图样的长度 p（3、4 或 5）
- 序列的最小周期长度
- 位置 37、38、39、40、41 上的符号

你可以进行以下类型的查询，但需要尽可能少地使用查询次数：

1. **查看查询**：查看位置 i 的符号（1 小于等于 i 小于等于 36）
2. **对比查询**：询问位置 i 和位置 j 的符号是否相同（1 小于等于 i, j 小于等于 36）
3. **测试间隔查询**：询问位置 k 和位置 k+q 的符号是否相同（要求 1 小于等于 k 小于等于 36−q）

每次可以提出 1 到 4 个查询，每个查询必须使用以下 XML 格式之一：

- 查看查询（例如查看位置 5）：
<query_view>5</query_view>

- 对比查询（例如对比位置 3 和位置 8）：
<query_compare>3,8</query_compare>

- 测试间隔查询（例如测试间隔为 4，起始位置为 10）：
<query_interval>4,10</query_interval>

提交最终答案时，必须包含以下四项信息，格式如下：

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

其中：
- mechanism：生成机制，必须是 A、B 或 C
- p：基础图样长度，必须是 3、4 或 5
- min_period：最小周期长度，必须是正整数
- next_symbols：位置 37 到 41 的 5 个符号，用空格分隔或直接连写
"""

    game_rule_en = """\
Let's play a "Sequence Generation Mechanism Inference" game. Here are the rules:

I have an ordered sequence S of length 36, where each element is drawn from the symbol set {{A, B, C, D}}. This sequence is generated from a base pattern M of length p using a specific mechanism, where p can be 3, 4, or 5. The base pattern M contains at least two different symbols.

There are only three possible generation mechanisms:

1. **Mechanism A (Direct Repetition)**: The sequence is formed by directly repeating the base pattern M. Each block b has the same content as M.

2. **Mechanism B (Reverse Alternation)**: Odd-numbered blocks (1st, 3rd, 5th...) equal M, and even-numbered blocks (2nd, 4th, 6th...) equal the reverse of M. Note that M itself is not a palindrome.

3. **Mechanism C (Progressive Cyclic Shift)**: Block b equals M right-cyclically shifted by (b−1) positions. M has no shorter non-trivial period.

Note: Each block has length p, and block numbering b starts from 1. If the sequence truncates a block at position 36, the defined positions of that block still follow the corresponding mechanism.

Your goal is to infer through queries:
- The generation mechanism used (A, B, or C)
- The length p of the base pattern (3, 4, or 5)
- The minimum period length of the sequence
- The symbols at positions 37, 38, 39, 40, 41

You can perform the following types of queries, but should use as few queries as possible:

1. **View Query**: View the symbol at position i (1 less than or equal to i less than or equal to 36)
2. **Compare Query**: Ask whether the symbols at positions i and j are the same (1 less than or equal to i, j less than or equal to 36)
3. **Interval Test Query**: Ask whether the symbols at positions k and k+q are the same (requires 1 less than or equal to k less than or equal to 36−q)

You can ask 1 to 4 queries at a time, each using one of the following XML formats:

- View Query (e.g., view position 5):
<query_view>5</query_view>

- Compare Query (e.g., compare positions 3 and 8):
<query_compare>3,8</query_compare>

- Interval Test Query (e.g., test interval of 4 starting at position 10):
<query_interval>4,10</query_interval>

When submitting your final answer, you must include the following four items in this format:

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

Where:
- mechanism: The generation mechanism, must be A, B, or C
- p: The base pattern length, must be 3, 4, or 5
- min_period: The minimum period length, must be a positive integer
- next_symbols: The 5 symbols at positions 37 to 41, space-separated or concatenated
"""

    contextualized_rule_zh_1 = """\
欢迎进入智能交通路网调度指挥中心。我们现在需要对一段未知的"交通信号相位序列"进行分析。规则如下：

系统记录了一个长度为 36 的时段序列 S，每个时段的相位指令取自指令集 {{A, B, C, D}}。这个序列是由一个长度为 p 的基础调度模式 M 按照某种排班机制生成的，其中 p 可能是 3、4 或 5。基础模式 M 至少包含两种不同的指令。

排班机制只有以下三种可能：

1. **机制 A（固定周期循环）**：整体序列由基础模式 M 直接重复拼接而成。即第 b 个调度块的内容与 M 完全相同。

2. **机制 B（双向通勤对称）**：奇数块（第 1、3、5...块）的指令等于 M，偶数块（第 2、4、6...块）的指令等于 M 的反向序列，用于平衡对向车流。注意 M 本身不是回文序列。

3. **机制 C（潮汐车道相位偏移）**：第 b 个块等于将 M 按照时间差右循环位移 (b−1) 位所得的结果，以适应潮汐车流的演变。M 不存在更短的非平凡周期。

说明：每个调度块的长度均为 p，块的编号 b 从 1 开始计数。如果序列在 36 个位置处截断了某个块，那么该块的已定义时段仍按对应机制生成。

你的目标是通过查询推断出：
- 采用的排班机制（A、B 或 C）
- 基础调度模式的长度 p（3、4 或 5）
- 信号序列的最小排班周期长度
- 时段 37、38、39、40、41 上的指令类型

你可以进行以下类型的查询（请尽可能少地使用查询次数）：

1. **调取查询**：查看时段 i 的指令（1 小于等于 i 小于等于 36）
2. **比对查询**：询问时段 i 和时段 j 的指令是否相同（1 小于等于 i, j 小于等于 36）
3. **周期测试查询**：询问时段 k 和时段 k+q 的指令是否相同（要求 1 小于等于 k 小于等于 36−q）

每次可以提出 1 到 4 个查询，每个查询必须使用以下 XML 格式之一：

- 调取查询（例如调取时段 5）：
<query_view>5</query_view>

- 比对查询（例如比对时段 3 和时段 8）：
<query_compare>3,8</query_compare>

- 周期测试查询（例如测试间隔为 4，起始时段为 10）：
<query_interval>4,10</query_interval>

提交最终答案时，必须包含以下四项信息，格式如下：

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

其中：
- mechanism：排班机制，必须是 A、B 或 C
- p：基础调度模式长度，必须是 3、4 或 5
- min_period：最小排班周期长度，必须是正整数
- next_symbols：时段 37 到 41 的 5 个指令，用空格分隔或直接连写
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Transportation Network Dispatch Center. We need to analyze an unknown "traffic signal phase sequence". Here are the rules:

The system has recorded a sequence S of length 36 representing different time intervals, where each interval's phase command is drawn from the set {{A, B, C, D}}. This sequence is generated from a base dispatch pattern M of length p using a specific scheduling mechanism, where p can be 3, 4, or 5. The base pattern M contains at least two different commands.

There are only three possible scheduling mechanisms:

1. **Mechanism A (Fixed Period Loop)**: The entire sequence is formed by directly repeating the base pattern M. Each dispatch block b has the same content as M.

2. **Mechanism B (Bidirectional Commute Symmetry)**: Odd-numbered blocks (1st, 3rd, 5th...) equal M, and even-numbered blocks (2nd, 4th, 6th...) equal the reverse of M, used to balance opposing traffic flows. Note that M itself is not a palindrome.

3. **Mechanism C (Tidal Lane Phase Shift)**: Block b equals M right-cyclically shifted by (b−1) positions, adapting to the evolution of tidal traffic flows. M has no shorter non-trivial period.

Note: Each dispatch block has length p, and block numbering b starts from 1. If the sequence truncates a block at position 36, the defined intervals of that block still follow the corresponding mechanism.

Your goal is to infer through queries:
- The scheduling mechanism used (A, B, or C)
- The length p of the base dispatch pattern (3, 4, or 5)
- The minimum scheduling period length of the signal sequence
- The commands at intervals 37, 38, 39, 40, 41

You can perform the following types of queries (please use as few queries as possible):

1. **Retrieve Query**: View the command at interval i (1 less than or equal to i less than or equal to 36)
2. **Compare Query**: Ask whether the commands at intervals i and j are the same (1 less than or equal to i, j less than or equal to 36)
3. **Period Test Query**: Ask whether the commands at intervals k and k+q are the same (requires 1 less than or equal to k less than or equal to 36−q)

You can ask 1 to 4 queries at a time, each using one of the following XML formats:

- Retrieve Query (e.g., retrieve interval 5):
<query_view>5</query_view>

- Compare Query (e.g., compare intervals 3 and 8):
<query_compare>3,8</query_compare>

- Period Test Query (e.g., test interval of 4 starting at interval 10):
<query_interval>4,10</query_interval>

When submitting your final answer, you must include the following four items in this format:

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

Where:
- mechanism: The scheduling mechanism, must be A, B, or C
- p: The base dispatch pattern length, must be 3, 4, or 5
- min_period: The minimum scheduling period length, must be a positive integer
- next_symbols: The 5 commands at intervals 37 to 41, space-separated or concatenated
"""

    contextualized_rule_zh_2 = """\
欢迎进入精准医疗与基因测序分析系统。我们现在需要对一段未知的"异常基因表达序列"进行分析。规则如下：

系统测得了一段长度为 36 的靶点序列 S，其中每个位点的核苷酸片段取自标记集 {{A, B, C, D}}。这个序列是由一个长度为 p 的核心基因模体（Motif）M 按照某种突变与表达机制生成的，其中 p 可能是 3、4 或 5。核心模体 M 至少包含两种不同的核苷酸。

表达机制只有以下三种可能：

1. **机制 A（串联重复序列）**：完整序列由核心模体 M 直接重复拼接而成。即第 b 个转录块的内容与 M 完全相同。

2. **机制 B（回文配对交替）**：奇数块（第 1、3、5...块）的片段等于 M，偶数块（第 2、4、6...块）的片段等于 M 的反向序列，反映了 DNA 复制时的反向链表现。注意 M 本身不是回文序列。

3. **机制 C（移码突变循环）**：第 b 个块等于将 M 右循环位移 (b−1) 位所得的结果，呈现出典型的移码突变特征。M 不存在更短的非平凡周期。

说明：每个转录块的长度均为 p，块的编号 b 从 1 开始计数。如果序列在 36 个位点处截断了某个块，那么该块的已表达位点仍按对应机制生成。

你的目标是通过查询推断出：
- 采用的突变与表达机制（A、B 或 C）
- 核心基因模体的长度 p（3、4 或 5）
- 基因序列的最小转录周期长度
- 位点 37、38、39、40、41 上的核苷酸片段

你可以进行以下类型的查询，但需要尽可能少地使用检测资源：

1. **靶向查询**：查看位点 i 的核苷酸（1 小于等于 i 小于等于 36）
2. **同源比对查询**：询问位点 i 和位点 j 的核苷酸是否相同（1 小于等于 i, j 小于等于 36）
3. **周期性检测查询**：询问位点 k 和位点 k+q 的核苷酸是否相同（要求 1 小于等于 k 小于等于 36−q）

每次可以提出 1 到 4 个查询，每个查询必须使用以下 XML 格式之一：

- 靶向查询（例如查看位点 5）：
<query_view>5</query_view>

- 同源比对查询（例如对比位点 3 和位点 8）：
<query_compare>3,8</query_compare>

- 周期性检测查询（例如测试间隔为 4，起始位点为 10）：
<query_interval>4,10</query_interval>

提交最终答案时，必须包含以下四项信息，格式如下：

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

其中：
- mechanism：突变与表达机制，必须是 A、B 或 C
- p：核心模体长度，必须是 3、4 或 5
- min_period：最小转录周期长度，必须是正整数
- next_symbols：位点 37 到 41 的 5 个片段，用空格分隔或直接连写
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Precision Medicine and Gene Sequencing Analysis System. We now need to analyze an unknown "abnormal gene expression sequence". Here are the rules:

The system has measured a target sequence S of length 36, where each locus's nucleotide fragment is drawn from the marker set {{A, B, C, D}}. This sequence is generated from a core gene motif M of length p using a specific mutation and expression mechanism, where p can be 3, 4, or 5. The core motif M contains at least two different nucleotides.

There are only three possible expression mechanisms:

1. **Mechanism A (Tandem Repeat Sequence)**: The entire sequence is formed by directly repeating the core motif M. Each transcription block b has the same content as M.

2. **Mechanism B (Palindromic Pairing Alternation)**: Odd-numbered blocks (1st, 3rd, 5th...) equal M, and even-numbered blocks (2nd, 4th, 6th...) equal the reverse of M, reflecting the reverse strand behavior during DNA replication. Note that M itself is not a palindrome.

3. **Mechanism C (Frameshift Mutation Cycle)**: Block b equals M right-cyclically shifted by (b−1) positions, showing typical frameshift mutation characteristics. M has no shorter non-trivial period.

Note: Each transcription block has length p, and block numbering b starts from 1. If the sequence truncates a block at position 36, the defined loci of that block still follow the corresponding mechanism.

Your goal is to infer through queries:
- The mutation and expression mechanism used (A, B, or C)
- The length p of the core gene motif (3, 4, or 5)
- The minimum transcription period length of the gene sequence
- The nucleotide fragments at loci 37, 38, 39, 40, 41

You can perform the following types of queries, but should use as few testing resources as possible:

1. **Targeted Query**: View the nucleotide at locus i (1 less than or equal to i less than or equal to 36)
2. **Homologous Compare Query**: Ask whether the nucleotides at loci i and j are the same (1 less than or equal to i, j less than or equal to 36)
3. **Periodicity Test Query**: Ask whether the nucleotides at loci k and k+q are the same (requires 1 less than or equal to k less than or equal to 36−q)

You can ask 1 to 4 queries at a time, each using one of the following XML formats:

- Targeted Query (e.g., view locus 5):
<query_view>5</query_view>

- Homologous Compare Query (e.g., compare loci 3 and 8):
<query_compare>3,8</query_compare>

- Periodicity Test Query (e.g., test interval of 4 starting at locus 10):
<query_interval>4,10</query_interval>

When submitting your final answer, you must include the following four items in this format:

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

Where:
- mechanism: The mutation and expression mechanism, must be A, B, or C
- p: The core motif length, must be 3, 4, or 5
- min_period: The minimum transcription period length, must be a positive integer
- next_symbols: The 5 fragments at loci 37 to 41, space-separated or concatenated
"""

    contextualized_rule_zh_3 = """\
欢迎进入自适应教育个性化抽题系统。我们来推演一段未知的"抽题序列机制"。规则如下：

系统生成了一份长度为 36 的练习题序列 S，其中每道题的认知能力类型取自集合 {{A, B, C, D}}。这个题目序列是由一个长度为 p 的基础能力考核模块 M 按照某种抽题机制生成的，其中 p 可能是 3、4 或 5。基础模块 M 至少包含两种不同的题型。

抽题机制只有以下三种可能：

1. **机制 A（模块化重复）**：试卷由基础模块 M 直接重复拼接而成。即第 b 个题组块的内容与 M 完全相同，用于强化训练。

2. **机制 B（螺旋式复习）**：奇数块（第 1、3、5...块）的内容等于 M，偶数块（第 2、4、6...块）的内容等于 M 的反向序列，通过反向顺序进行防遗忘复习。注意 M 本身不具有对称性。

3. **机制 C（进阶能力轮转）**：第 b 个块等于将 M 右循环位移 (b−1) 位所得的结果，避免学生产生做题惯性。M 不存在更短的非平凡周期。

说明：每个题组块的长度均为 p，块的编号 b 从 1 开始计数。如果序列在 36 个位置处截断了某个块，那么该块的已出题位置仍按对应机制生成。

你的目标是通过查询推断出：
- 采用的抽题机制（A、B 或 C）
- 基础考核模块的题量 p（3、4 或 5）
- 完整考卷的出题最小周期长度
- 题目位置 37、38、39、40、41 上的题型

你可以进行以下类型的查询，但需要尽可能少地使用查询次数：

1. **抽样查询**：查看位置 i 的题型（1 小于等于 i 小于等于 36）
2. **同构对比查询**：询问位置 i 和位置 j 的题型是否相同（1 小于等于 i, j 小于等于 36）
3. **跨度复测查询**：询问位置 k 和位置 k+q 的题型是否相同（要求 1 小于等于 k 小于等于 36−q）

每次可以提出 1 到 4 个查询，每个查询必须使用以下 XML 格式之一：

- 抽样查询（例如查看位置 5）：
<query_view>5</query_view>

- 同构对比查询（例如对比位置 3 和位置 8）：
<query_compare>3,8</query_compare>

- 跨度复测查询（例如测试间隔为 4，起始位置为 10）：
<query_interval>4,10</query_interval>

提交最终答案时，必须包含以下四项信息，格式如下：

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

其中：
- mechanism：抽题机制，必须是 A、B 或 C
- p：基础模块长度，必须是 3、4 或 5
- min_period：最小周期长度，必须是正整数
- next_symbols：位置 37 到 41 的 5 个题型，用空格分隔或直接连写
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Education Personalized Question Selection System. Let's infer an unknown "question selection sequence mechanism". Here are the rules:

The system has generated a practice sequence S of length 36, where each question's cognitive ability type is drawn from the set {{A, B, C, D}}. This sequence is generated from a base assessment module M of length p using a specific question selection mechanism, where p can be 3, 4, or 5. The base module M contains at least two different question types.

There are only three possible selection mechanisms:

1. **Mechanism A (Modular Repetition)**: The test paper is formed by directly repeating the base module M. Each question block b has the same content as M, used for intensive training.

2. **Mechanism B (Spiral Review)**: Odd-numbered blocks (1st, 3rd, 5th...) equal M, and even-numbered blocks (2nd, 4th, 6th...) equal the reverse of M, conducting anti-forgetting reviews in reverse order. Note that M itself is not symmetric.

3. **Mechanism C (Advanced Ability Rotation)**: Block b equals M right-cyclically shifted by (b−1) positions, preventing students from forming predictable answering habits. M has no shorter non-trivial period.

Note: Each question block has length p, and block numbering b starts from 1. If the sequence truncates a block at position 36, the defined questions of that block still follow the corresponding mechanism.

Your goal is to infer through queries:
- The question selection mechanism used (A, B, or C)
- The length p of the base assessment module (3, 4, or 5)
- The minimum period length of the test generation sequence
- The question types at positions 37, 38, 39, 40, 41

You can perform the following types of queries, but should use as few queries as possible:

1. **Sampling Query**: View the question type at position i (1 less than or equal to i less than or equal to 36)
2. **Isomorphic Compare Query**: Ask whether the question types at positions i and j are the same (1 less than or equal to i, j less than or equal to 36)
3. **Span Retest Query**: Ask whether the question types at positions k and k+q are the same (requires 1 less than or equal to k less than or equal to 36−q)

You can ask 1 to 4 queries at a time, each using one of the following XML formats:

- Sampling Query (e.g., view position 5):
<query_view>5</query_view>

- Isomorphic Compare Query (e.g., compare positions 3 and 8):
<query_compare>3,8</query_compare>

- Span Retest Query (e.g., test interval of 4 starting at position 10):
<query_interval>4,10</query_interval>

When submitting your final answer, you must include the following four items in this format:

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

Where:
- mechanism: The selection mechanism, must be A, B, or C
- p: The base module length, must be 3, 4, or 5
- min_period: The minimum period length, must be a positive integer
- next_symbols: The 5 question types at positions 37 to 41, space-separated or concatenated
"""

    contextualized_rule_zh_4 = """\
欢迎进入智能工业控制与自动化制造中心。我们现在要对一段"流水线装配工序模式"进行分析。规则如下：

中控机记录了一个长度为 36 的操作序列 S，其中每个工位的动作指令取自指令集 {{A, B, C, D}}。这个流水线序列是由一个长度为 p 的核心工艺程序 M 按照某种排产机制生成的，其中 p 可能是 3、4 或 5。核心工艺 M 至少包含两种不同的动作。

排产控制机制只有以下三种可能：

1. **机制 A（标准流水线重复）**：加工序列由核心工艺 M 直接重复执行而成。即第 b 个加工块的动作序列与 M 完全相同。

2. **机制 B（往复式加工）**：奇数块（第 1、3、5...块）的动作序列等于 M，偶数块（第 2、4、6...块）的动作序列等于 M 的反向序列，通常用于机械臂来回往返喷涂或组装。注意 M 本身不是对称的。

3. **机制 C（分度盘旋转加工）**：第 b 个块等于将 M 右循环位移 (b−1) 位所得的结果，这是为了适配工位转盘的逐步推进。M 不存在更短的非平凡周期。

说明：每个加工块的长度均为 p，块的编号 b 从 1 开始计数。如果序列在 36 个工位处截断了某个块，那么该块的已执行工位仍按对应机制生成。

你的目标是通过查询推断出：
- 采用的排产机制（A、B 或 C）
- 核心工艺程序的步骤数 p（3、4 或 5）
- 流水线动作的最小循环周期长度
- 工位 37、38、39、40、41 上的操作动作

你可以进行以下类型的查询，但需要尽可能少地进行干预：

1. **监控查询**：查看工位 i 的动作指令（1 小于等于 i 小于等于 36）
2. **动作比对查询**：询问工位 i 和工位 j 的动作指令是否相同（1 小于等于 i, j 小于等于 36）
3. **步长校验查询**：询问工位 k 和工位 k+q 的动作指令是否相同（要求 1 小于等于 k 小于等于 36−q）

每次可以提出 1 到 4 个查询，每个查询必须使用以下 XML 格式之一：

- 监控查询（例如查看工位 5）：
<query_view>5</query_view>

- 动作比对查询（例如对比工位 3 和工位 8）：
<query_compare>3,8</query_compare>

- 步长校验查询（例如测试间隔为 4，起始工位为 10）：
<query_interval>4,10</query_interval>

提交最终答案时，必须包含以下四项信息，格式如下：

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

其中：
- mechanism：排产机制，必须是 A、B 或 C
- p：核心工艺步骤数，必须是 3、4 或 5
- min_period：最小循环周期长度，必须是正整数
- next_symbols：工位 37 到 41 的 5 个动作，用空格分隔或直接连写
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the Intelligent Industrial Control and Automated Manufacturing Center. We now need to analyze an unknown "assembly line operation pattern". Here are the rules:

The central console has recorded an operation sequence S of length 36, where each station's action command is drawn from the set {{A, B, C, D}}. This pipeline sequence is generated from a core process program M of length p using a specific production scheduling mechanism, where p can be 3, 4, or 5. The core process M contains at least two different actions.

There are only three possible scheduling mechanisms:

1. **Mechanism A (Standard Pipeline Repetition)**: The processing sequence is formed by directly repeating the core process M. Each processing block b has the exact same action sequence as M.

2. **Mechanism B (Reciprocating Processing)**: Odd-numbered blocks (1st, 3rd, 5th...) equal M, and even-numbered blocks (2nd, 4th, 6th...) equal the reverse of M, typically used for reciprocating robotic arm spraying or assembly. Note that M itself is not symmetric.

3. **Mechanism C (Indexing Dial Rotation Processing)**: Block b equals M right-cyclically shifted by (b−1) positions, designed to adapt to the progressive advancement of station dials. M has no shorter non-trivial period.

Note: Each processing block has length p, and block numbering b starts from 1. If the sequence truncates a block at position 36, the executed stations of that block still follow the corresponding mechanism.

Your goal is to infer through queries:
- The production scheduling mechanism used (A, B, or C)
- The number of steps p in the core process program (3, 4, or 5)
- The minimum cycle period length of the pipeline actions
- The action commands at stations 37, 38, 39, 40, 41

You can perform the following types of queries, but should use as few interventions as possible:

1. **Monitor Query**: View the action command at station i (1 less than or equal to i less than or equal to 36)
2. **Action Compare Query**: Ask whether the action commands at stations i and j are the same (1 less than or equal to i, j less than or equal to 36)
3. **Step Check Query**: Ask whether the action commands at stations k and k+q are the same (requires 1 less than or equal to k less than or equal to 36−q)

You can ask 1 to 4 queries at a time, each using one of the following XML formats:

- Monitor Query (e.g., view station 5):
<query_view>5</query_view>

- Action Compare Query (e.g., compare stations 3 and 8):
<query_compare>3,8</query_compare>

- Step Check Query (e.g., test interval of 4 starting at station 10):
<query_interval>4,10</query_interval>

When submitting your final answer, you must include the following four items in this format:

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

Where:
- mechanism: The scheduling mechanism, must be A, B, or C
- p: The core process steps, must be 3, 4, or 5
- min_period: The minimum cycle period length, must be a positive integer
- next_symbols: The 5 actions at stations 37 to 41, space-separated or concatenated
"""

    contextualized_rule_zh_5 = """\
欢迎进入反洗钱司法审计与合规审查平台。我们需要对一段隐藏的"资金流转网络模式"进行破解。规则如下：

审计日志捕获了一条长度为 36 的转账交易序列 S，其中每个节点的资金流向账户类型取自类型库 {{A, B, C, D}}。这个序列是由一个长度为 p 的基础洗钱交易链 M 按照某种混淆机制生成的，其中 p 可能是 3、4 或 5。基础交易链 M 至少涉及两种不同的账户类型。

资金混淆机制只有以下三种可能：

1. **机制 A（固定结构嵌套）**：整体流水由基础交易链 M 直接重复构成。即第 b 个转账批次的内容与 M 完全相同，用于固定渠道的资金输送。

2. **机制 B（对冲账户反向交易）**：奇数批次（第 1、3、5...批）的交易等同于 M，偶数批次（第 2、4、6...批）的交易等同于 M 的反向序列，用于制造正反向对冲回流假象。注意 M 本身不是回文序列。

3. **机制 C（离岸滚动转移）**：第 b 个批次等于将 M 右循环位移 (b−1) 位所得的结果，通过滚动偏移躲避静态规则的追踪。M 不存在更短的非平凡周期。

说明：每个转账批次的长度均为 p，批次编号 b 从 1 开始计数。如果流水在 36 个节点处截断了某个批次，那么该批次的已记录节点仍按对应机制生成。

你的目标是通过查询推断出：
- 采用的资金混淆机制（A、B 或 C）
- 基础交易链的长度 p（3、4 或 5）
- 资金流转的最小闭环周期长度
- 节点 37、38、39、40、41 上的账户类型

你可以进行以下类型的查询，但需要尽量控制调证次数以免打草惊蛇：

1. **穿透查询**：查看节点 i 的账户类型（1 小于等于 i 小于等于 36）
2. **账户比对查询**：询问节点 i 和节点 j 的账户类型是否相同（1 小于等于 i, j 小于等于 36）
3. **链路间隔查询**：询问节点 k 和节点 k+q 的账户类型是否相同（要求 1 小于等于 k 小于等于 36−q）

每次可以提出 1 到 4 个查询，每个查询必须使用以下 XML 格式之一：

- 穿透查询（例如查看节点 5）：
<query_view>5</query_view>

- 账户比对查询（例如对比节点 3 和节点 8）：
<query_compare>3,8</query_compare>

- 链路间隔查询（例如测试间隔为 4，起始节点为 10）：
<query_interval>4,10</query_interval>

提交最终答案时，必须包含以下四项信息，格式如下：

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

其中：
- mechanism：资金混淆机制，必须是 A、B 或 C
- p：基础交易链长度，必须是 3、4 或 5
- min_period：最小闭环周期长度，必须是正整数
- next_symbols：节点 37 到 41 的 5 个账户类型，用空格分隔或直接连写
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Anti-Money Laundering Forensic Audit and Compliance Review Platform. We need to decrypt a hidden "fund flow network pattern". Here are the rules:

The audit log has captured a transfer transaction sequence S of length 36, where each node's fund flow account type is drawn from the library {{A, B, C, D}}. This sequence is generated from a base laundering transaction chain M of length p using a specific obfuscation mechanism, where p can be 3, 4, or 5. The base transaction chain M involves at least two different account types.

There are only three possible fund obfuscation mechanisms:

1. **Mechanism A (Fixed Structural Nesting)**: The overall flow is formed by directly repeating the base transaction chain M. Each transfer batch b has the exact same content as M, used for fixed-channel fund delivery.

2. **Mechanism B (Hedged Account Reverse Trading)**: Odd-numbered batches (1st, 3rd, 5th...) equal M, and even-numbered batches (2nd, 4th, 6th...) equal the reverse of M, intended to create the illusion of forward-reverse hedging backflows. Note that M itself is not a palindrome.

3. **Mechanism C (Offshore Rolling Transfer)**: Batch b equals M right-cyclically shifted by (b−1) positions, evading static rule tracking through rolling offsets. M has no shorter non-trivial period.

Note: Each transfer batch has length p, and batch numbering b starts from 1. If the flow truncates a batch at position 36, the recorded nodes of that batch still follow the corresponding mechanism.

Your goal is to infer through queries:
- The fund obfuscation mechanism used (A, B, or C)
- The length p of the base transaction chain (3, 4, or 5)
- The minimum closed-loop period length of the fund flow
- The account types at nodes 37, 38, 39, 40, 41

You can perform the following types of queries, but should minimize forensic interventions to avoid alerting the suspects:

1. **Penetration Query**: View the account type at node i (1 less than or equal to i less than or equal to 36)
2. **Account Compare Query**: Ask whether the account types at nodes i and j are the same (1 less than or equal to i, j less than or equal to 36)
3. **Link Interval Query**: Ask whether the account types at nodes k and k+q are the same (requires 1 less than or equal to k less than or equal to 36−q)

You can ask 1 to 4 queries at a time, each using one of the following XML formats:

- Penetration Query (e.g., view node 5):
<query_view>5</query_view>

- Account Compare Query (e.g., compare nodes 3 and 8):
<query_compare>3,8</query_compare>

- Link Interval Query (e.g., test interval of 4 starting at node 10):
<query_interval>4,10</query_interval>

When submitting your final answer, you must include the following four items in this format:

<answer>mechanism=A, p=3, min_period=3, next_symbols=ABCDA</answer>

Where:
- mechanism: The fund obfuscation mechanism, must be A, B, or C
- p: The base transaction chain length, must be 3, 4, or 5
- min_period: The minimum closed-loop period length, must be a positive integer
- next_symbols: The 5 account types at nodes 37 to 41, space-separated or concatenated
"""

    tags = ["answer", "query_view", "query_compare", "query_interval"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "mechanism": "A",
                "p": 3,
                "pattern": "ABC",
            },
            2: {
                "mechanism": "B",
                "p": 4,
                "pattern": "ABCD",
            },
            3: {
                "mechanism": "A",
                "p": 5,
                "pattern": "ABCDA",
            },
            4: {
                "mechanism": "B",
                "p": 5,
                "pattern": "ABCDB",
            },
            5: {
                "mechanism": "C",
                "p": 4,
                "pattern": "ABCD",
            },
        },
        "en": {
            1: {
                "mechanism": "A",
                "p": 3,
                "pattern": "ABC",
            },
            2: {
                "mechanism": "B",
                "p": 4,
                "pattern": "ABCD",
            },
            3: {
                "mechanism": "A",
                "p": 5,
                "pattern": "ABCDA",
            },
            4: {
                "mechanism": "B",
                "p": 5,
                "pattern": "ABCDB",
            },
            5: {
                "mechanism": "C",
                "p": 4,
                "pattern": "ABCD",
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
        self.mechanism = cfg["mechanism"]
        self.p = cfg["p"]
        self.pattern = list(cfg["pattern"])
        
        self.view_count = 0
        self.compare_count = 0
        self.max_view = 12
        self.max_compare = 12
        
        self.sequence = self._generate_sequence(41)
        
        self.min_period = self._calculate_min_period()
        
        self._game_info["p"] = self.p

    def _generate_sequence(self, length):
        sequence = []
        block_num = 1
        
        for i in range(length):
            block_num = i // self.p + 1
            offset = i % self.p
            
            if self.mechanism == "A":
                sequence.append(self.pattern[offset])
            elif self.mechanism == "B":
                if block_num % 2 == 1:
                    sequence.append(self.pattern[offset])
                else:
                    sequence.append(self.pattern[self.p - 1 - offset])
            elif self.mechanism == "C":
                shift = (block_num - 1) % self.p
                shifted_pos = (offset - shift) % self.p
                sequence.append(self.pattern[shifted_pos])
        
        return sequence

    def _calculate_min_period(self):
        if self.mechanism == "A":
            return self.p
        elif self.mechanism == "B":
            return 2 * self.p
        elif self.mechanism == "C":
            return self.p * self.p
        return self.p

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"]
            ans_dict = {}
            parts = [x.strip() for x in raw_ans.split(",")]
            
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            required_keys = ["mechanism", "p", "min_period", "next_symbols"]
            for key in required_keys:
                if key not in ans_dict:
                    return False
            
            if ans_dict["mechanism"] != self.mechanism:
                return False
            
            if int(ans_dict["p"]) != self.p:
                return False
            
            if int(ans_dict["min_period"]) != self.min_period:
                return False
            
            next_symbols = ans_dict["next_symbols"].replace(" ", "").replace(",", "")
            if len(next_symbols) != 5:
                return False
            
            expected_symbols = "".join(self.sequence[36:41])
            if next_symbols != expected_symbols:
                return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            invalid_index = "错误：索引超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            invalid_index = "Error: Index out of range."
        
        responses = []
        
        if "query_view" in parsed_info:
            try:
                idx = int(parsed_info["query_view"].strip())
                if idx < 1 or idx > 36:
                    return invalid_index
                symbol = self.sequence[idx - 1]
                responses.append(symbol)
            except:
                return invalid_index
        
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                i, j = [int(x.strip()) for x in raw.split(",")]
                if i < 1 or i > 36 or j < 1 or j > 36:
                    return invalid_index
                result = yes_res if self.sequence[i-1] == self.sequence[j-1] else no_res
                responses.append(result)
            except:
                return invalid_index
        
        if "query_interval" in parsed_info:
            try:
                raw = parsed_info["query_interval"]
                q, k = [int(x.strip()) for x in raw.split(",")]
                if k < 1 or k + q > 36:
                    return invalid_index
                result = yes_res if self.sequence[k-1] == self.sequence[k+q-1] else no_res
                responses.append(result)
            except:
                return invalid_index
        
        if not responses:
            raise ValueError("No valid query tag found.")
        
        return "\n".join(responses)

    def _cf_make_wrong(self, correct):
        if correct in ["A", "B", "C", "D"]:
            return "B" if correct == "A" else "A"
        
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct or "否" in correct:
                return correct.replace("是", "TEMP_YES").replace("否", "是").replace("TEMP_YES", "否")
        else:
            if "Yes" in correct or "No" in correct:
                return correct.replace("Yes", "TEMP_YES").replace("No", "Yes").replace("TEMP_YES", "No")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list:
        results = []

        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for i in range(1, 37):
            results.append({
                "query":  f"<query_view>{i}</query_view>",
                "answer": self.sequence[i - 1],
            })

        for i in range(1, 37):
            for j in range(i + 1, 37):
                ans = yes_res if self.sequence[i - 1] == self.sequence[j - 1] else no_res
                results.append({
                    "query":  f"<query_compare>{i},{j}</query_compare>",
                    "answer": ans,
                })

        for q in range(1, 36):
            for k in range(1, 36 - q + 1):
                ans = yes_res if self.sequence[k - 1] == self.sequence[k + q - 1] else no_res
                results.append({
                    "query":  f"<query_interval>{q},{k}</query_interval>",
                    "answer": ans,
                })

        return results