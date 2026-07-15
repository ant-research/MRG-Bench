from .base import Game
import re

class GAME498(Game):

    contextualized_rule_zh_1 = """\
欢迎使用“交通信号周期推演系统”。系统设定了一个信号指令集 Σ = {{R(红灯), G(绿灯), B(公交专用), Y(黄灯)}}（公开且固定），仅作为符号集合使用。我已秘密锁定了一个非空的本原序列 T（本原序列是指不能拆解为某个更短信号周期的多次重复的基础指令循环），以及一个公开的正整数时间窗长度 N = {n}。

我构造了一个长度为 N 的系统序列 S，它是将 T 无限重复执行后截取前 N 个信号指令得到的。例如，若 T = "RG"，N = 5，则 S = "RGRG" + "R" = "RGRGR"。

你的目标是通过查询推断出这个基础的本原信号序列 T。你可以使用以下四种查询（每次仅限一个查询）：

1. **存在查询**：询问指令模式 p 是否为 S 的连续子串。回答 "是" 或 "否"。
2. **计数查询**：询问指令模式 p 在 S 中出现的次数（重叠计数）。回答一个非负整数。
3. **位置查询**：询问指令模式 p 在 S 中最靠左的起始位置（下标从 1 开始）。若不存在则回答 0。
4. **猜测**：提交你认为的本原序列 p。若 p 的重复截断恰好等于 S 且 p 是本原序列，则推演胜利；否则推演失败。

注意：
- 模式 p 的长度必须在 1 到 N 之间。
- 你需要在尽可能少的查询次数内找到答案。
- 本原序列是指不能表示为某个更短序列的重复。例如 "RG" 是本原序列，但 "RGRG" 不是（它是 "RG" 的 2 次重复）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 存在查询（例如询问 "RG"）：
<query_has>RG</query_has>

- 计数查询（例如询问 "RGB"）：
<query_count>RGB</query_count>

- 位置查询（例如询问 "BY"）：
<query_left>BY</query_left>

- 提交最终答案（例如猜测本原序列为 "RGB"）：
<answer>RGB</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Traffic Signal Cycle Inference System". The system uses a signal state command set Σ = {{R(Red), G(Green), B(Bus-only), Y(Yellow)}} (public and fixed), used only as a symbol set. I have secretly locked a non-empty primitive sequence T (a primitive sequence is a basic instruction loop that cannot be expressed as multiple repetitions of a shorter signal cycle), and a public positive integer time window length N = {n}.

I constructed an actual signal sequence S of length N by infinitely repeating T and taking the first N commands. For example, if T = "RG" and N = 5, then S = "RGRG" + "R" = "RGRGR".

Your goal is to infer this basic primitive signal sequence T through queries. You can use the following four types of queries (one query at a time):

1. **Has Query**: Ask if command pattern p is a contiguous substring of S. Answer "Yes" or "No".
2. **Count Query**: Ask for the number of occurrences of pattern p in S (overlapping count). Answer a non-negative integer.
3. **Left Query**: Ask for the leftmost starting position of pattern p in S (1-indexed). Answer 0 if it doesn't exist.
4. **Guess**: Submit your candidate primitive sequence p. If the repetition and truncation of p exactly equals S and p is primitive, you win; otherwise you fail.

Notes:
- Pattern p must have length between 1 and N.
- You should find the answer with as few queries as possible.
- A primitive sequence cannot be expressed as repetitions of a shorter sequence. For example, "RG" is primitive, but "RGRG" is not (it is "RG" repeated 2 times).

Each query must contain only one tag. Use the following XML format:

- Has Query (e.g., asking about "RG"):
<query_has>RG</query_has>

- Count Query (e.g., asking about "RGB"):
<query_count>RGB</query_count>

- Left Query (e.g., asking about "BY"):
<query_left>BY</query_left>

- Submit final answer (e.g., guessing the primitive sequence is "RGB"):
<answer>RGB</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“致病基因标记推演系统”。在DNA片段分析中，我们标记了四类特定核苷酸突变：Σ = {{R, G, B, Y}}（公开且固定），仅作为基因代号集合使用。我已秘密锁定了一段未知的核心突变基因单元 T（本原序列，即不可再分的最小致病重复单元），并提供测序样本链长度 N = {n}。

系统从患者体内提取了长度为 N 的长基因链 S，它是将 T 连续复制后截取前 N 个标记得到的。例如，若 T = "RG"，N = 5，则 S = "RGRG" + "R" = "RGRGR"。

你的目标是通过查询推断出这个核心的本原基因序列 T。你可以使用以下四种查询（每次仅限一个查询）：

1. **存在查询**：询问基因片段 p 是否为 S 的连续子串。回答 "是" 或 "否"。
2. **计数查询**：询问基因片段 p 在 S 中出现的次数（重叠计数）。回答一个非负整数。
3. **位置查询**：询问基因片段 p 在 S 中最靠左的起始位置（下标从 1 开始）。若不存在则回答 0。
4. **猜测**：提交你认为的本原基因单元 p。若 p 的重复截断恰好等于 S 且 p 是本原序列，则推演胜利；否则推演失败。

注意：
- 片段 p 的长度必须在 1 到 N 之间。
- 你需要在尽可能少的查询次数内找到答案。
- 本原序列是指不能表示为某个更短片段的重复。例如 "RG" 是本原序列，但 "RGRG" 不是（它是 "RG" 的 2 次重复）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 存在查询（例如询问 "RG"）：
<query_has>RG</query_has>

- 计数查询（例如询问 "RGB"）：
<query_count>RGB</query_count>

- 位置查询（例如询问 "BY"）：
<query_left>BY</query_left>

- 提交最终答案（例如猜测本原序列为 "RGB"）：
<answer>RGB</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Pathogenic Gene Marker Inference System". In DNA fragment analysis, we label four specific nucleotide mutations: Σ = {{R, G, B, Y}} (public and fixed), used only as a gene code set. I have secretly locked an unknown core mutated gene unit T (a primitive sequence, which is the indivisible minimum pathogenic repeating unit), and provided a sequencing sample chain length N = {n}.

The system extracted a long gene chain S of length N from the patient, which is obtained by continuously replicating T and taking the first N markers. For example, if T = "RG" and N = 5, then S = "RGRG" + "R" = "RGRGR".

Your goal is to infer this core primitive gene sequence T through queries. You can use the following four types of queries (one query at a time):

1. **Has Query**: Ask if gene fragment p is a contiguous substring of S. Answer "Yes" or "No".
2. **Count Query**: Ask for the number of occurrences of gene fragment p in S (overlapping count). Answer a non-negative integer.
3. **Left Query**: Ask for the leftmost starting position of gene fragment p in S (1-indexed). Answer 0 if it doesn't exist.
4. **Guess**: Submit your candidate primitive gene unit p. If the repetition and truncation of p exactly equals S and p is primitive, you win; otherwise you fail.

Notes:
- Fragment p must have length between 1 and N.
- You should find the answer with as few queries as possible.
- A primitive sequence cannot be expressed as repetitions of a shorter fragment. For example, "RG" is primitive, but "RGRG" is not (it is "RG" repeated 2 times).

Each query must contain only one tag. Use the following XML format:

- Has Query (e.g., asking about "RG"):
<query_has>RG</query_has>

- Count Query (e.g., asking about "RGB"):
<query_count>RGB</query_count>

- Left Query (e.g., asking about "BY"):
<query_left>BY</query_left>

- Submit final answer (e.g., guessing the primitive sequence is "RGB"):
<answer>RGB</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入“学习行为模式分析系统”。我们记录了学生的四类学习活动：Σ = {{R(阅读), G(小组), B(板书), Y(课外)}}（公开且固定），仅作为代号集合使用。我秘密锁定了一个核心学习习惯周期 T（本原序列，即无法拆解为更短学习循环的习惯模式），以及观测总步长 N = {n}。

系统生成的长期学习行为序列 S，是将周期 T 无限循环重复后截取前 N 个活动得到的。例如，若 T = "RG"，N = 5，则 S = "RGRG" + "R" = "RGRGR"。

你的目标是通过查询推断出这个本原学习习惯周期 T。你可以使用以下四种查询（每次仅限一个查询）：

1. **存在查询**：询问行为模式 p 是否为 S 的连续子串。回答 "是" 或 "否"。
2. **计数查询**：询问行为模式 p 在 S 中出现的次数（重叠计数）。回答一个非负整数。
3. **位置查询**：询问行为模式 p 在 S 中最靠左的起始位置（下标从 1 开始）。若不存在则回答 0。
4. **猜测**：提交你认为的本原习惯周期 p。若 p 的重复截断恰好等于 S 且 p 是本原序列，则分析胜利；否则分析失败。

注意：
- 模式 p 的长度必须在 1 到 N 之间。
- 你需要在尽可能少的查询次数内找到答案。
- 本原序列是指不能表示为某个更短周期的重复。例如 "RG" 是本原序列，但 "RGRG" 不是（它是 "RG" 的 2 次重复）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 存在查询（例如询问 "RG"）：
<query_has>RG</query_has>

- 计数查询（例如询问 "RGB"）：
<query_count>RGB</query_count>

- 位置查询（例如询问 "BY"）：
<query_left>BY</query_left>

- 提交最终答案（例如猜测本原序列为 "RGB"）：
<answer>RGB</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Learning Behavior Pattern Analysis System". We record four types of student learning activities: Σ = {{R(Reading), G(Group), B(Board), Y(Yard)}} (public and fixed), used only as a code set. I have secretly locked a core learning habit cycle T (a primitive sequence, which is a habit pattern that cannot be broken down into a shorter learning loop), and a total observation step length N = {n}.

The long-term learning behavior sequence S generated by the system is obtained by infinitely repeating the cycle T and taking the first N activities. For example, if T = "RG" and N = 5, then S = "RGRG" + "R" = "RGRGR".

Your goal is to infer this primitive learning habit cycle T through queries. You can use the following four types of queries (one query at a time):

1. **Has Query**: Ask if behavior pattern p is a contiguous substring of S. Answer "Yes" or "No".
2. **Count Query**: Ask for the number of occurrences of behavior pattern p in S (overlapping count). Answer a non-negative integer.
3. **Left Query**: Ask for the leftmost starting position of behavior pattern p in S (1-indexed). Answer 0 if it doesn't exist.
4. **Guess**: Submit your candidate primitive habit cycle p. If the repetition and truncation of p exactly equals S and p is primitive, you win; otherwise you fail.

Notes:
- Pattern p must have length between 1 and N.
- You should find the answer with as few queries as possible.
- A primitive sequence cannot be expressed as repetitions of a shorter cycle. For example, "RG" is primitive, but "RGRG" is not (it is "RG" repeated 2 times).

Each query must contain only one tag. Use the following XML format:

- Has Query (e.g., asking about "RG"):
<query_has>RG</query_has>

- Count Query (e.g., asking about "RGB"):
<query_count>RGB</query_count>

- Left Query (e.g., asking about "BY"):
<query_left>BY</query_left>

- Submit final answer (e.g., guessing the primitive sequence is "RGB"):
<answer>RGB</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业流水线指令推演系统”。自动化装配线包含四种基础加工指令：Σ = {{R(铆接), G(打磨), B(折弯), Y(检验)}}（公开且固定），仅作为代号集合使用。我已秘密设定了一套标准的本原加工循环 T（本原工序，即不能拆解为更短循环的重复工序），以及记录的工步总数 N = {n}。

系统日志记录的近期工序操作序列 S 长度为 N，它是将 T 无限重复执行后截取前 N 个指令得到的。例如，若 T = "RG"，N = 5，则 S = "RGRG" + "R" = "RGRGR"。

你的目标是通过查询推断出这套标准的本原加工工序 T。你可以使用以下四种查询（每次仅限一个查询）：

1. **存在查询**：询问指令流 p 是否为 S 的连续子序列。回答 "是" 或 "否"。
2. **计数查询**：询问指令流 p 在 S 中出现的次数（重叠计数）。回答一个非负整数。
3. **位置查询**：询问指令流 p 在 S 中最靠左的起始工步（下标从 1 开始）。若不存在则回答 0。
4. **猜测**：提交你认为的本原加工循环 p。若 p 的重复截断恰好等于 S 且 p 是本原序列，则推演胜利；否则推演失败。

注意：
- 指令流 p 的长度必须在 1 到 N 之间。
- 你需要在尽可能少的查询次数内找到答案。
- 本原序列是指不能表示为某个更短循环的重复。例如 "RG" 是本原序列，但 "RGRG" 不是（它是 "RG" 的 2 次重复）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 存在查询（例如询问 "RG"）：
<query_has>RG</query_has>

- 计数查询（例如询问 "RGB"）：
<query_count>RGB</query_count>

- 位置查询（例如询问 "BY"）：
<query_left>BY</query_left>

- 提交最终答案（例如猜测本原序列为 "RGB"）：
<answer>RGB</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Assembly Line Instruction Inference System". The automated assembly line contains four basic processing instructions: Σ = {{R(Riveting), G(Grinding), B(Bending), Y(Yielding)}} (public and fixed), used only as a code set. I have secretly set a standard primitive processing cycle T (a primitive procedure, which cannot be broken down into repetitions of a shorter cycle), and a recorded total number of working steps N = {n}.

The recent procedure operation sequence S recorded by the system log has length N. It is obtained by infinitely executing T and taking the first N instructions. For example, if T = "RG" and N = 5, then S = "RGRG" + "R" = "RGRGR".

Your goal is to infer this standard primitive processing procedure T through queries. You can use the following four types of queries (one query at a time):

1. **Has Query**: Ask if instruction stream p is a contiguous subsequence of S. Answer "Yes" or "No".
2. **Count Query**: Ask for the number of occurrences of instruction stream p in S (overlapping count). Answer a non-negative integer.
3. **Left Query**: Ask for the leftmost starting step of instruction stream p in S (1-indexed). Answer 0 if it doesn't exist.
4. **Guess**: Submit your candidate primitive processing cycle p. If the repetition and truncation of p exactly equals S and p is primitive, you win; otherwise you fail.

Notes:
- Instruction stream p must have length between 1 and N.
- You should find the answer with as few queries as possible.
- A primitive sequence cannot be expressed as repetitions of a shorter cycle. For example, "RG" is primitive, but "RGRG" is not (it is "RG" repeated 2 times).

Each query must contain only one tag. Use the following XML format:

- Has Query (e.g., asking about "RG"):
<query_has>RG</query_has>

- Count Query (e.g., asking about "RGB"):
<query_count>RGB</query_count>

- Left Query (e.g., asking about "BY"):
<query_left>BY</query_left>

- Submit final answer (e.g., guessing the primitive sequence is "RGB"):
<answer>RGB</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“合同条款合规审查系统”。我们对复杂的商业合同提取了四种核心条款类型：Σ = {{R(权利), G(担保), B(违约), Y(免责)}}（公开且固定），仅作为条款代号集合使用。我秘密锁定了一套基础的本原条款组合 T（本原条款组，即不能表示为更短条款组合的重复的标准化模板），以及审查长度 N = {n}。

给定的合同条款序列 S 长度为 N，它是将 T 不断套用后截取前 N 个条款得到的。例如，若 T = "RG"，N = 5，则 S = "RGRG" + "R" = "RGRGR"。

你的目标是通过查询推断出这套基础的本原条款组 T。你可以使用以下四种查询（每次仅限一个查询）：

1. **存在查询**：询问条款模式 p 是否为 S 的连续子串。回答 "是" 或 "否"。
2. **计数查询**：询问条款模式 p 在 S 中出现的次数（重叠计数）。回答一个非负整数。
3. **位置查询**：询问条款模式 p 在 S 中最靠左的起始位置（下标从 1 开始）。若不存在则回答 0。
4. **猜测**：提交你认为的本原条款组 p。若 p 的重复截断恰好等于 S 且 p 是本原序列，则审查胜利；否则审查失败。

注意：
- 模式 p 的长度必须在 1 到 N 之间。
- 你需要在尽可能少的查询次数内找到答案。
- 本原序列是指不能表示为某个更短序列的重复。例如 "RG" 是本原序列，但 "RGRG" 不是（它是 "RG" 的 2 次重复）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 存在查询（例如询问 "RG"）：
<query_has>RG</query_has>

- 计数查询（例如询问 "RGB"）：
<query_count>RGB</query_count>

- 位置查询（例如询问 "BY"）：
<query_left>BY</query_left>

- 提交最终答案（例如猜测本原序列为 "RGB"）：
<answer>RGB</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Contract Clause Compliance Review System". We extract four core clause types for complex commercial contracts: Σ = {{R(Rights), G(Guarantees), B(Breach), Y(Yield)}} (public and fixed), used only as a clause code set. I have secretly locked a basic primitive clause combination T (a primitive clause group, which is a standardized template that cannot be expressed as multiple repetitions of a shorter combination), and a review length N = {n}.

The given contract clause sequence S has length N, which is obtained by continuously applying T and taking the first N clauses. For example, if T = "RG" and N = 5, then S = "RGRG" + "R" = "RGRGR".

Your goal is to infer this basic primitive clause group T through queries. You can use the following four types of queries (one query at a time):

1. **Has Query**: Ask if clause pattern p is a contiguous substring of S. Answer "Yes" or "No".
2. **Count Query**: Ask for the number of occurrences of clause pattern p in S (overlapping count). Answer a non-negative integer.
3. **Left Query**: Ask for the leftmost starting position of clause pattern p in S (1-indexed). Answer 0 if it doesn't exist.
4. **Guess**: Submit your candidate primitive clause group p. If the repetition and truncation of p exactly equals S and p is primitive, you win; otherwise you fail.

Notes:
- Pattern p must have length between 1 and N.
- You should find the answer with as few queries as possible.
- A primitive sequence cannot be expressed as repetitions of a shorter sequence. For example, "RG" is primitive, but "RGRG" is not (it is "RG" repeated 2 times).

Each query must contain only one tag. Use the following XML format:

- Has Query (e.g., asking about "RG"):
<query_has>RG</query_has>

- Count Query (e.g., asking about "RGB"):
<query_count>RGB</query_count>

- Left Query (e.g., asking about "BY"):
<query_left>BY</query_left>

- Submit final answer (e.g., guessing the primitive sequence is "RGB"):
<answer>RGB</answer>
"""

    game_rule_zh = """\
我们来玩一个"本原串推理"游戏，规则如下：

游戏设定了一个字母表 Σ = {{R, G, B, Y}}（公开且固定），仅作为符号集合使用。我已秘密选择了一个非空的本原串 T（本原串是指不能表示为某个更短串的多次重复），以及一个公开的正整数 N = {n}。

我构造了一个长度为 N 的序列 S，它是将 T 无限重复后截取前 N 个字符得到的。例如，若 T = "RG"，N = 5，则 S = "RGRG" + "R" = "RGRGR"。

你的目标是通过询问推断出这个本原串 T。你可以使用以下四种查询（每次仅限一个查询）：

1. **存在查询**：询问模式 p 是否为 S 的连续子串。回答 "是" 或 "否"。
2. **计数查询**：询问模式 p 在 S 中出现的次数（重叠计数）。回答一个非负整数。
3. **位置查询**：询问模式 p 在 S 中最靠左的起始位置（下标从 1 开始）。若不存在则回答 0。
4. **猜测**：提交你认为的本原串 p。若 p 的重复截断恰好等于 S 且 p 是本原串，则游戏胜利；否则游戏失败。

注意：
- 模式 p 的长度必须在 1 到 N 之间。
- 你需要在尽可能少的查询次数内找到答案。
- 本原串是指不能表示为某个更短串的重复。例如 "RG" 是本原串，但 "RGRG" 不是（它是 "RG" 的 2 次重复）。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 存在查询（例如询问 "RG"）：
<query_has>RG</query_has>

- 计数查询（例如询问 "RGB"）：
<query_count>RGB</query_count>

- 位置查询（例如询问 "BY"）：
<query_left>BY</query_left>

- 提交最终答案（例如猜测本原串为 "RGB"）：
<answer>RGB</answer>
"""

    game_rule_en = """\
Let's play a "Primitive String Inference" game. Here are the rules:

The game uses an alphabet Σ = {{R, G, B, Y}} (public and fixed), used only as a symbol set. I have secretly chosen a non-empty primitive string T (a primitive string cannot be expressed as multiple repetitions of a shorter string), and a public positive integer N = {n}.

I constructed a sequence S of length N by infinitely repeating T and taking the first N characters. For example, if T = "RG" and N = 5, then S = "RGRG" + "R" = "RGRGR".

Your goal is to infer the primitive string T through queries. You can use the following four types of queries (one query at a time):

1. **Has Query**: Ask if pattern p is a contiguous substring of S. Answer "Yes" or "No".
2. **Count Query**: Ask for the number of occurrences of pattern p in S (overlapping count). Answer a non-negative integer.
3. **Left Query**: Ask for the leftmost starting position of pattern p in S (1-indexed). Answer 0 if it doesn't exist.
4. **Guess**: Submit your candidate primitive string p. If the repetition and truncation of p exactly equals S and p is primitive, you win; otherwise you fail.

Notes:
- Pattern p must have length between 1 and N.
- You should find the answer with as few queries as possible.
- A primitive string cannot be expressed as repetitions of a shorter string. For example, "RG" is primitive, but "RGRG" is not (it is "RG" repeated 2 times).

Each query must contain only one tag. Use the following XML format:

- Has Query (e.g., asking about "RG"):
<query_has>RG</query_has>

- Count Query (e.g., asking about "RGB"):
<query_count>RGB</query_count>

- Left Query (e.g., asking about "BY"):
<query_left>BY</query_left>

- Submit final answer (e.g., guessing the primitive string is "RGB"):
<answer>RGB</answer>
"""

    tags = ["answer", "query_has", "query_count", "query_left"]

    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 8, "primitive": "RG"},
            2: {"n": 12, "primitive": "RGB"},
            3: {"n": 15, "primitive": "RGBY"},
            4: {"n": 18, "primitive": "RGBYR"},
            5: {"n": 21, "primitive": "RGBYRG"},
        },
        "en": {
            1: {"n": 8, "primitive": "RG"},
            2: {"n": 12, "primitive": "RGB"},
            3: {"n": 15, "primitive": "RGBY"},
            4: {"n": 18, "primitive": "RGBYR"},
            5: {"n": 21, "primitive": "RGBYRG"},
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
        self.n = cfg["n"]
        self.primitive = cfg["primitive"]
        
        self.sequence = self._generate_sequence(self.primitive, self.n)
        
        self._game_info["n"] = self.n

    def _generate_sequence(self, primitive, n):
        result = ""
        while len(result) < n:
            result += primitive
        return result[:n]

    def _is_primitive(self, s):
        if not s:
            return False
        n = len(s)
        for period in range(1, n):
            if n % period == 0:
                if s == (s[:period] * (n // period)):
                    return False
        return True

    def evaluate(self, parsed_info):
        candidate = parsed_info["answer"].strip()
        
        alphabet = {'R', 'G', 'B', 'Y'}
        if not all(c in alphabet for c in candidate):
            return False
        
        if len(candidate) == 0 or len(candidate) > self.n:
            return False
        
        generated = self._generate_sequence(candidate, self.n)
        
        if generated != self.sequence:
            return False
        
        if not self._is_primitive(candidate):
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_length = "错误：模式长度超出范围。"
            error_alphabet = "错误：模式包含非法字符。"
        else:
            yes_res, no_res = "Yes", "No"
            error_length = "Error: Pattern length out of range."
            error_alphabet = "Error: Pattern contains invalid characters."

        alphabet = {'R', 'G', 'B', 'Y'}

        if "query_has" in parsed_info:
            pattern = parsed_info["query_has"].strip()
            
            if not pattern or len(pattern) > self.n:
                return error_length
            if not all(c in alphabet for c in pattern):
                return error_alphabet
            
            return yes_res if pattern in self.sequence else no_res

        elif "query_count" in parsed_info:
            pattern = parsed_info["query_count"].strip()
            
            if not pattern or len(pattern) > self.n:
                return error_length
            if not all(c in alphabet for c in pattern):
                return error_alphabet
            
            count = 0
            for i in range(len(self.sequence) - len(pattern) + 1):
                if self.sequence[i:i+len(pattern)] == pattern:
                    count += 1
            return str(count)

        elif "query_left" in parsed_info:
            pattern = parsed_info["query_left"].strip()
            
            if not pattern or len(pattern) > self.n:
                return error_length
            if not all(c in alphabet for c in pattern):
                return error_alphabet
            
            pos = self.sequence.find(pattern)
            if pos == -1:
                return "0"
            else:
                return str(pos + 1)

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        if correct == yes_res:
            return no_res
        if correct == no_res:
            return yes_res
        
        if correct.isdigit():
            val = int(correct)
            if val == 0:
                return "1"
            else:
                return str(max(0, val - 1))
        
        return correct + "X"

    def get_all_possible_queries(self):
        results = []
        
        substrings = set()
        n = len(self.sequence)
        for length in range(1, n + 1):
            for i in range(n - length + 1):
                substrings.add(self.sequence[i : i + length])
        
        if self.config.language == "zh":
            yes_res = "是"
        else:
            yes_res = "Yes"
            
        for p in substrings:
            results.append({
                "query": f"<query_has>{p}</query_has>",
                "answer": yes_res
            })
            
            count = 0
            for i in range(len(self.sequence) - len(p) + 1):
                if self.sequence[i:i+len(p)] == p:
                    count += 1
            results.append({
                "query": f"<query_count>{p}</query_count>",
                "answer": str(count)
            })
            
            pos = self.sequence.find(p)
            results.append({
                "query": f"<query_left>{p}</query_left>",
                "answer": str(pos + 1)
            })
            
        return results