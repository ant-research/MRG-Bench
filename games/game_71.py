from .base import Game
import random
import itertools

class InteractiveLCSGame(Game):

    game_rule_zh = """\
我们现在来玩一个"最长公共子序列长度推断"游戏，规则如下：

游戏设定了一个有限字母表 Σ = {alphabet_display}，以及两个隐藏的序列 S 和 T。S 的长度为 {n1}，T 的长度为 {n2}，它们都由字母表 Σ 中的字符组成。

你的目标是通过查询推断出这两个隐藏序列的最长公共子序列（LCS）的长度。

- 子序列：由原序列删除若干个（可以为零）字符，且保持剩余字符的相对顺序得到的序列。
- LCS(X, Y)：序列 X 与 Y 的所有公共子序列中，长度最大的那个子序列的长度。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. **LCS查询**：提交任意序列 P（由字母表 Σ 中的字符组成），我会返回两个整数 (a, b)，其中：
   - a = LCS(P, S)：P 与隐藏序列 S 的最长公共子序列长度
   - b = LCS(P, T)：P 与隐藏序列 T 的最长公共子序列长度

2. **子序列验证查询**：提交任意序列 P，询问它是否同时是 S 和 T 的公共子序列。我会回答"是"或"否"。
   - 当且仅当 LCS(P, S) 等于 P 的长度，且 LCS(P, T) 也等于 P 的长度时，答案为"是"。

请尽可能用少的查询次数完成推断。当你收集到足够信息后，请提交最终答案。

每次询问只能包含一个标签。请使用以下 XML 格式：

- LCS查询（例如查询序列 "ABC"）：
<query_lcs>ABC</query_lcs>

- 子序列验证查询（例如验证序列 "AB"）：
<query_subseq>AB</query_subseq>

提交最终答案时，必须给出一个整数 K，表示你推断的 LCS(S, T) 的值。你也可以选择性地给出一个长度为 K 的证据序列 W（可选）。格式如下：

- 仅提交长度（例如答案为 5）：
<answer>5</answer>

- 提交长度和证据序列（例如答案为 3，证据为 "ACB"）：
<answer>K=3, W=ACB</answer>
"""

    game_rule_en = """\
Let's play an "Interactive LCS Length Inference" game. Here are the rules:

The game has defined a finite alphabet Σ = {alphabet_display} and two hidden sequences S and T. S has length {n1}, and T has length {n2}. Both are composed of characters from the alphabet Σ.

Your goal is to infer the length of the Longest Common Subsequence (LCS) of these two hidden sequences through queries.

- Subsequence: A sequence obtained by deleting zero or more characters from the original sequence while maintaining the relative order of the remaining characters.
- LCS(X, Y): The length of the longest subsequence that is common to both sequences X and Y.

You can repeatedly ask me the following two types of queries (one query per turn):

1. **LCS Query**: Submit any sequence P (composed of characters from alphabet Σ), and I will return two integers (a, b), where:
   - a = LCS(P, S): The LCS length between P and hidden sequence S
   - b = LCS(P, T): The LCS length between P and hidden sequence T

2. **Subsequence Verification Query**: Submit any sequence P and ask whether it is a common subsequence of both S and T. I will answer "Yes" or "No".
   - The answer is "Yes" if and only if LCS(P, S) equals the length of P and LCS(P, T) also equals the length of P.

Please try to complete the inference with as few queries as possible. When you have gathered enough information, submit your final answer.

Each query must contain only one tag. Use the following XML format:

- LCS Query (e.g., querying sequence "ABC"):
<query_lcs>ABC</query_lcs>

- Subsequence Verification Query (e.g., verifying sequence "AB"):
<query_subseq>AB</query_subseq>

When submitting the final answer, you must provide an integer K representing your inferred value of LCS(S, T). You may optionally provide a witness sequence W of length K. Format:

- Submit only the length (e.g., answer is 5):
<answer>5</answer>

- Submit length with witness sequence (e.g., answer is 3 with witness "ACB"):
<answer>K=3, W=ACB</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市路网共用路线评估系统”。本系统旨在规划两条主干道路的最长重叠共用路径，以优化公交线路布局。

系统设定了一个有限的路口节点代号表 Σ = {alphabet_display}，并在数据库中隐藏了两条主干道的路口序列 S 和 T。S 的路口数为 {n1}，T 的路口数为 {n2}，它们都由代号表 Σ 中的代号组成。

你的目标是通过探测查询，推断出这两条主干道的最长重叠共用路径（即最长公共子序列 LCS）的长度。

- 共用路径（子序列）：由原道路路线中跳过若干个（可以为零）路口，且保持剩余路口相对行车顺序不变所得到的路线。
- LCS(X, Y)：路线 X 与 Y 的所有共用路径中，包含路口数量最多的那条路径的长度。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. **路网重叠查询（LCS查询）**：提交任意试探路线 P（由代号表 Σ 中的节点组成），我会返回两个整数 (a, b)，其中：
   - a = LCS(P, S)：路线 P 与主干道 S 的最长重叠共用路径长度
   - b = LCS(P, T)：路线 P 与主干道 T 的最长重叠共用路径长度

2. **路线可行性验证（子序列验证查询）**：提交任意路线 P，询问它是否同时是主干道 S 和 T 的可行共用子路线。我会回答"是"或"否"。
   - 当且仅当 LCS(P, S) 等于 P 的长度，且 LCS(P, T) 也等于 P 的长度时，答案为"是"。

请尽可能用少的查询次数完成推断。当你收集到足够信息后，请提交最终答案。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 路网重叠查询（例如查询路线 "ABC"）：
<query_lcs>ABC</query_lcs>

- 路线可行性验证（例如验证路线 "AB"）：
<query_subseq>AB</query_subseq>

提交最终答案时，必须给出一个整数 K，表示你推断的最长共用路径长度 LCS(S, T) 的值。你也可以选择性地给出一个长度为 K 的路线证据 W（可选）。格式如下：

- 仅提交长度（例如答案为 5）：
<answer>5</answer>

- 提交长度和证据路线（例如答案为 3，证据为 "ACB"）：
<answer>K=3, W=ACB</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Road Network Shared Route Evaluation System". This system aims to plan the longest shared routes between two main roads to optimize bus line layouts.

The system has defined a finite intersection node alphabet Σ = {alphabet_display} and two hidden main road node sequences S and T. S contains {n1} nodes, and T contains {n2} nodes. Both are composed of node codes from the alphabet Σ.

Your goal is to infer the length of the Longest Shared Route (i.e., Longest Common Subsequence LCS) of these two main roads through exploratory queries.

- Shared Route (Subsequence): A route obtained by skipping zero or more intersections from the original route while maintaining the relative driving order of the remaining intersections.
- LCS(X, Y): The length of the path with the maximum number of intersections among all shared routes between route X and Y.

You can repeatedly ask me the following two types of queries (one query per turn):

1. **Network Overlap Query (LCS Query)**: Submit any trial route P (composed of nodes from alphabet Σ), and I will return two integers (a, b), where:
   - a = LCS(P, S): The longest shared route length between P and main road S
   - b = LCS(P, T): The longest shared route length between P and main road T

2. **Route Feasibility Verification (Subsequence Verification Query)**: Submit any route P and ask whether it is a feasible common sub-route for both main roads S and T. I will answer "Yes" or "No".
   - The answer is "Yes" if and only if LCS(P, S) equals the length of P and LCS(P, T) also equals the length of P.

Please try to complete the inference with as few queries as possible. When you have gathered enough information, submit your final answer.

Each query must contain only one tag. Use the following XML format:

- Network Overlap Query (e.g., querying route "ABC"):
<query_lcs>ABC</query_lcs>

- Route Feasibility Verification (e.g., verifying route "AB"):
<query_subseq>AB</query_subseq>

When submitting the final answer, you must provide an integer K representing your inferred value of the longest shared route length LCS(S, T). You may optionally provide a witness route W of length K. Format:

- Submit only the length (e.g., answer is 5):
<answer>5</answer>

- Submit length with witness route (e.g., answer is 3 with witness "ACB"):
<answer>K=3, W=ACB</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“基因同源序列分析系统”。本系统旨在对比病毒变异株的基因序列，协助研究人员提取广谱疫苗的核心标靶。

系统设定了一个有限的核苷酸序列字母表 Σ = {alphabet_display}，以及两个隐藏的变异株基因片段 S 和 T。S 的序列长度为 {n1}，T 的序列长度为 {n2}，它们都由字母表 Σ 中的字符组成。

你的目标是通过探测查询，推断出这两个变异株的最长保守基因序列（即最长公共子序列 LCS）的长度。

- 保守片段（子序列）：由原基因序列剔除若干个（可以为零）变异位点，且保持剩余核苷酸相对排列顺序不变所得到的片段。
- LCS(X, Y)：序列 X 与 Y 的所有同源片段中，保留核苷酸数量最多的那个片段的长度。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. **同源匹配查询（LCS查询）**：提交任意探测序列 P（由字母表 Σ 中的字符组成），我会返回两个整数 (a, b)，其中：
   - a = LCS(P, S)：探测序列 P 与变异株 S 的最长同源片段长度
   - b = LCS(P, T)：探测序列 P 与变异株 T 的最长同源片段长度

2. **保守片段验证（子序列验证查询）**：提交任意序列 P，询问它是否同时是变异株 S 和 T 的共有保守基因片段。我会回答"是"或"否"。
   - 当且仅当 LCS(P, S) 等于 P 的长度，且 LCS(P, T) 也等于 P 的长度时，答案为"是"。

请尽可能用少的查询次数完成推断。当你收集到足够信息后，请提交最终答案。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 同源匹配查询（例如查询序列 "ABC"）：
<query_lcs>ABC</query_lcs>

- 保守片段验证（例如验证序列 "AB"）：
<query_subseq>AB</query_subseq>

提交最终答案时，必须给出一个整数 K，表示你推断的最长保守基因序列长度 LCS(S, T) 的值。你也可以选择性地给出一个长度为 K 的序列证据 W（可选）。格式如下：

- 仅提交长度（例如答案为 5）：
<answer>5</answer>

- 提交长度和证据序列（例如答案为 3，证据为 "ACB"）：
<answer>K=3, W=ACB</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Gene Homology Sequence Analysis System". This system aims to compare the genetic sequences of virus variants to assist researchers in extracting core targets for broad-spectrum vaccines.

The system has defined a finite nucleotide alphabet Σ = {alphabet_display} and two hidden mutant strain gene fragments S and T. S has a sequence length of {n1}, and T has a sequence length of {n2}. Both are composed of characters from the alphabet Σ.

Your goal is to infer the length of the Longest Conserved Gene Sequence (i.e., Longest Common Subsequence LCS) of these two mutant strains through exploratory queries.

- Conserved Fragment (Subsequence): A fragment obtained by removing zero or more mutation sites from the original gene sequence while maintaining the relative order of the remaining nucleotides.
- LCS(X, Y): The length of the homologous fragment that retains the maximum number of nucleotides among all conserved fragments between sequence X and Y.

You can repeatedly ask me the following two types of queries (one query per turn):

1. **Homology Matching Query (LCS Query)**: Submit any probe sequence P (composed of characters from alphabet Σ), and I will return two integers (a, b), where:
   - a = LCS(P, S): The longest homologous fragment length between probe P and mutant strain S
   - b = LCS(P, T): The longest homologous fragment length between probe P and mutant strain T

2. **Conserved Fragment Verification (Subsequence Verification Query)**: Submit any sequence P and ask whether it is a shared conserved gene fragment of both strains S and T. I will answer "Yes" or "No".
   - The answer is "Yes" if and only if LCS(P, S) equals the length of P and LCS(P, T) also equals the length of P.

Please try to complete the inference with as few queries as possible. When you have gathered enough information, submit your final answer.

Each query must contain only one tag. Use the following XML format:

- Homology Matching Query (e.g., querying sequence "ABC"):
<query_lcs>ABC</query_lcs>

- Conserved Fragment Verification (e.g., verifying sequence "AB"):
<query_subseq>AB</query_subseq>

When submitting the final answer, you must provide an integer K representing your inferred value of the longest conserved gene sequence length LCS(S, T). You may optionally provide a witness sequence W of length K. Format:

- Submit only the length (e.g., answer is 5):
<answer>5</answer>

- Submit length with witness sequence (e.g., answer is 3 with witness "ACB"):
<answer>K=3, W=ACB</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学生思维路径比对系统”。本系统用于追踪并分析不同学生的答题逻辑链条，以评估群体认知共性或筛查异常雷同卷。

系统设定了一个有限的知识节点代号表 Σ = {alphabet_display}，以及两名隐藏学生的答题逻辑链 S 和 T。S 的知识节点数为 {n1}，T 的知识节点数为 {n2}，它们都由代号表 Σ 中的节点代号组成。

你的目标是通过测试查询，推断出这两名学生的最长共同逻辑链（即最长公共子序列 LCS）的长度。

- 思维子路径（子序列）：由原解答逻辑中跳跃忽略若干个（可以为零）中间步骤，且保持剩余推理步骤先后顺序不变所得到的路径。
- LCS(X, Y)：逻辑链 X 与 Y 的所有共同思维子路径中，涵盖知识节点最多的那条路径的长度。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. **逻辑链匹配查询（LCS查询）**：提交任意测试思维链 P（由代号表 Σ 中的节点组成），我会返回两个整数 (a, b)，其中：
   - a = LCS(P, S)：测试链 P 与学生 S 答题逻辑的最大匹配知识节点数
   - b = LCS(P, T)：测试链 P 与学生 T 答题逻辑的最大匹配知识节点数

2. **思维路径验证（子序列验证查询）**：提交任意测试链 P，询问它是否同时完整存在于两名学生的思维路径中（顺序一致）。我会回答"是"或"否"。
   - 当且仅当 LCS(P, S) 等于 P 的长度，且 LCS(P, T) 也等于 P 的长度时，答案为"是"。

请尽可能用少的查询次数完成推断。当你收集到足够信息后，请提交最终答案。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 逻辑链匹配查询（例如查询测试链 "ABC"）：
<query_lcs>ABC</query_lcs>

- 思维路径验证（例如验证测试链 "AB"）：
<query_subseq>AB</query_subseq>

提交最终答案时，必须给出一个整数 K，表示你推断的最长共同逻辑链长度 LCS(S, T) 的值。你也可以选择性地给出一个长度为 K 的路径证据 W（可选）。格式如下：

- 仅提交长度（例如答案为 5）：
<answer>5</answer>

- 提交长度和证据路径（例如答案为 3，证据为 "ACB"）：
<answer>K=3, W=ACB</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Student Cognitive Path Comparison System". This system is used to track and analyze the answering logic chains of different students to evaluate group cognitive commonalities or screen for abnormally similar papers.

The system has defined a finite knowledge node alphabet Σ = {alphabet_display} and two hidden student cognitive logic chains S and T. S contains {n1} nodes, and T contains {n2} nodes. Both are composed of node codes from the alphabet Σ.

Your goal is to infer the length of the Longest Common Logic Chain (ie., Longest Common Subsequence LCS) between these two students through testing queries.

- Cognitive Sub-path (Subsequence): A path obtained by skipping zero or more intermediate steps from the original reasoning logic while maintaining the chronological order of the remaining reasoning steps.
- LCS(X, Y): The length of the cognitive path covering the most knowledge nodes among all common cognitive sub-paths of logic chain X and Y.

You can repeatedly ask me the following two types of queries (one query per turn):

1. **Logic Chain Matching Query (LCS Query)**: Submit any test logic chain P (composed of nodes from alphabet Σ), and I will return two integers (a, b), where:
   - a = LCS(P, S): The maximum matched knowledge nodes between test chain P and student S's logic
   - b = LCS(P, T): The maximum matched knowledge nodes between test chain P and student T's logic

2. **Cognitive Path Verification (Subsequence Verification Query)**: Submit any test chain P and ask whether it is completely present in both students' cognitive paths (with consistent order). I will answer "Yes" or "No".
   - The answer is "Yes" if and only if LCS(P, S) equals the length of P and LCS(P, T) also equals the length of P.

Please try to complete the inference with as few queries as possible. When you have gathered enough information, submit your final answer.

Each query must contain only one tag. Use the following XML format:

- Logic Chain Matching Query (e.g., querying test chain "ABC"):
<query_lcs>ABC</query_lcs>

- Cognitive Path Verification (e.g., verifying test chain "AB"):
<query_subseq>AB</query_subseq>

When submitting the final answer, you must provide an integer K representing your inferred value of the longest common logic chain length LCS(S, T). You may optionally provide a witness path W of length K. Format:

- Submit only the length (e.g., answer is 5):
<answer>5</answer>

- Submit length with witness path (e.g., answer is 3 with witness "ACB"):
<answer>K=3, W=ACB</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“自动化装配流水线工艺对齐系统”。本系统负责对齐不同批次产品的生产环节，以最大化生产线模块的复用率。

系统设定了一个有限的标准工序代号表 Σ = {alphabet_display}，以及两条隐藏的装配流水线工序链 S 和 T。S 包含 {n1} 道工序，T 包含 {n2} 道工序，它们都由代号表 Σ 中的代号组成。

你的目标是通过探测查询，推断出这两条流水线的最长公共标准工序链（即最长公共子序列 LCS）的长度。

- 工序子集（子序列）：由原装配流水线剥离若干个（可以为零）非核心组装步骤，且保持剩余基础步骤先后工艺顺序不变所得到的工序链。
- LCS(X, Y)：工序链 X 与 Y 的所有通用基础工序子集中，包含工序数量最多的那条标准链的长度。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. **工序兼容查询（LCS查询）**：提交任意试探工序组合 P（由代号表 Σ 中的代号组成），我会返回两个整数 (a, b)，其中：
   - a = LCS(P, S)：工序组合 P 与流水线 S 能够兼容的最长工序数量
   - b = LCS(P, T)：工序组合 P 与流水线 T 能够兼容的最长工序数量

2. **工序子集验证（子序列验证查询）**：提交任意工序组合 P，询问它是否同时为两条流水线的通用基础工序子集（工艺顺序一致）。我会回答"是"或"否"。
   - 当且仅当 LCS(P, S) 等于 P 的长度，且 LCS(P, T) 也等于 P 的长度时，答案为"是"。

请尽可能用少的查询次数完成推断。当你收集到足够信息后，请提交最终答案。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 工序兼容查询（例如查询工序组合 "ABC"）：
<query_lcs>ABC</query_lcs>

- 工序子集验证（例如验证工序组合 "AB"）：
<query_subseq>AB</query_subseq>

提交最终答案时，必须给出一个整数 K，表示你推断的最长公共标准工序链长度 LCS(S, T) 的值。你也可以选择性地给出一个长度为 K 的工艺链证据 W（可选）。格式如下：

- 仅提交长度（例如答案为 5）：
<answer>5</answer>

- 提交长度和证据工艺链（例如答案为 3，证据为 "ACB"）：
<answer>K=3, W=ACB</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Automated Assembly Line Process Alignment System". This system is responsible for aligning the production stages of different batch products to maximize the reuse rate of production line modules.

The system has defined a finite standard process alphabet Σ = {alphabet_display} and two hidden assembly line process chains S and T. S contains {n1} processes, and T contains {n2} processes. Both are composed of process codes from the alphabet Σ.

Your goal is to infer the length of the Longest Common Standard Process Chain (i.e., Longest Common Subsequence LCS) of these two assembly lines through trial queries.

- Process Subset (Subsequence): A process chain obtained by stripping zero or more non-core assembly steps from the original assembly line while maintaining the chronological craftsmanship order of the remaining basic steps.
- LCS(X, Y): The length of the standard chain containing the most processes among all general basic process subsets of process chain X and Y.

You can repeatedly ask me the following two types of queries (one query per turn):

1. **Process Compatibility Query (LCS Query)**: Submit any trial process combination P (composed of codes from alphabet Σ), and I will return two integers (a, b), where:
   - a = LCS(P, S): The maximum compatible process count between combination P and assembly line S
   - b = LCS(P, T): The maximum compatible process count between combination P and assembly line T

2. **Process Subset Verification (Subsequence Verification Query)**: Submit any process combination P and ask whether it serves as a general basic process subset for both assembly lines simultaneously (with consistent craftsmanship order). I will answer "Yes" or "No".
   - The answer is "Yes" if and only if LCS(P, S) equals the length of P and LCS(P, T) also equals the length of P.

Please try to complete the inference with as few queries as possible. When you have gathered enough information, submit your final answer.

Each query must contain only one tag. Use the following XML format:

- Process Compatibility Query (e.g., querying process combination "ABC"):
<query_lcs>ABC</query_lcs>

- Process Subset Verification (e.g., verifying process combination "AB"):
<query_subseq>AB</query_subseq>

When submitting the final answer, you must provide an integer K representing your inferred value of the longest common standard process chain length LCS(S, T). You may optionally provide a witness process chain W of length K. Format:

- Submit only the length (e.g., answer is 5):
<answer>5</answer>

- Submit length with witness process chain (e.g., answer is 3 with witness "ACB"):
<answer>K=3, W=ACB</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“庭审证据链审查与比对系统”。本系统旨在提取存在争议的商业合同或双方口供事件中，无可争议的核心共识部分。

系统设定了一个有限的核心事实节点代号表 Σ = {alphabet_display}，以及两份隐藏的争议合同条款序列（或口供事件链） S 和 T。S 的条款节点数为 {n1}，T 的条款节点数为 {n2}，它们都由代号表 Σ 中的节点组成。

你的目标是通过查询推断，审查出这两份材料的最长一致性事实链（即最长公共子序列 LCS）的长度。

- 事实子链（子序列）：由原合同条款序列中搁置若干项（可以为零）存疑条款，且保持剩余条款或事件相对先后发生顺序不变所形成的事实逻辑链。
- LCS(X, Y)：材料 X 与 Y 的所有共识子链中，能够互相印证的事实节点数量最多的那条事实链的长度。

你可以反复向我提出以下两类查询（每次仅限一个查询）：

1. **事实印证查询（LCS查询）**：提出任意事实假设链 P（由代号表 Σ 中的节点组成），我会返回两个整数 (a, b)，其中：
   - a = LCS(P, S)：事实假设链 P 在材料 S 中能被最大程度印证的连贯事实节点数
   - b = LCS(P, T)：事实假设链 P 在材料 T 中能被最大程度印证的连贯事实节点数

2. **共识条款验证（子序列验证查询）**：提出任意事实假设链 P，询问它是否同时是两份材料中完全一致且未被破坏先后顺序的共识事实。我会回答"是"或"否"。
   - 当且仅当 LCS(P, S) 等于 P 的长度，且 LCS(P, T) 也等于 P 的长度时，答案为"是"。

请尽可能用少的查询次数完成推断。当你收集到足够信息后，请提交最终审查答案。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 事实印证查询（例如提出假设链 "ABC"）：
<query_lcs>ABC</query_lcs>

- 共识条款验证（例如验证假设链 "AB"）：
<query_subseq>AB</query_subseq>

提交最终答案时，必须给出一个整数 K，表示你推断的最长一致性事实链长度 LCS(S, T) 的值。你也可以选择性地给出一个长度为 K 的事实证据链 W（可选）。格式如下：

- 仅提交长度（例如答案为 5）：
<answer>5</answer>

- 提交长度和事实证据链（例如答案为 3，证据为 "ACB"）：
<answer>K=3, W=ACB</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Court Evidence Chain Review and Comparison System". This system aims to extract the indisputable core consensus parts from disputed commercial contracts or testimony event chains provided by both parties.

The system has defined a finite core factual node alphabet Σ = {alphabet_display} and two hidden disputed contract clause sequences (or testimony chains) S and T. S contains {n1} clause nodes, and T contains {n2} clause nodes. Both are composed of nodes from the alphabet Σ.

Your goal is to infer the length of the Longest Consistent Factual Chain (i.e., Longest Common Subsequence LCS) between these two materials through query inference.

- Factual Sub-chain (Subsequence): A factual logic chain formed by shelving zero or more doubtful clauses from the original contract sequence while maintaining the relative chronological order of the remaining clauses or events.
- LCS(X, Y): The length of the factual chain capable of corroborating the maximum number of factual nodes among all consensus sub-chains of material X and Y.

You can repeatedly ask me the following two types of queries (one query per turn):

1. **Factual Corroboration Query (LCS Query)**: Submit any factual hypothesis chain P (composed of nodes from alphabet Σ), and I will return two integers (a, b), where:
   - a = LCS(P, S): The maximum corroborated coherent factual node count for hypothesis chain P within material S
   - b = LCS(P, T): The maximum corroborated coherent factual node count for hypothesis chain P within material T

2. **Consensus Clause Verification (Subsequence Verification Query)**: Submit any factual hypothesis chain P and ask whether it serves as a completely consistent consensus fact with an unbroken chronological order in both materials simultaneously. I will answer "Yes" or "No".
   - The answer is "Yes" if and only if LCS(P, S) equals the length of P and LCS(P, T) also equals the length of P.

Please try to complete the inference with as few queries as possible. When you have gathered enough information, submit your final review answer.

Each query must contain only one tag. Use the following XML format:

- Factual Corroboration Query (e.g., submitting hypothesis chain "ABC"):
<query_lcs>ABC</query_lcs>

- Consensus Clause Verification (e.g., verifying hypothesis chain "AB"):
<query_subseq>AB</query_subseq>

When submitting the final answer, you must provide an integer K representing your inferred value of the longest consistent factual chain length LCS(S, T). You may optionally provide a witness factual chain W of length K. Format:

- Submit only the length (e.g., answer is 5):
<answer>5</answer>

- Submit length with witness factual chain (e.g., answer is 3 with witness "ACB"):
<answer>K=3, W=ACB</answer>
"""

    tags = ["answer", "query_lcs", "query_subseq"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "alphabet": "ABC",
                "n1": 4,
                "n2": 4,
                "s": "ABAC",
                "t": "ABBC",
                "lcs_length": 3,
            },
            2: {
                "alphabet": "ABCD",
                "n1": 6,
                "n2": 6,
                "s": "ABCDAB",
                "t": "ACBDAC",
                "lcs_length": 4,
            },
            3: {
                "alphabet": "ABCDE",
                "n1": 8,
                "n2": 8,
                "s": "ABCDEABC",
                "t": "ACEABCDE",
                "lcs_length": 6,
            },
            4: {
                "alphabet": "ABCDEF",
                "n1": 10,
                "n2": 10,
                "s": "ABCDEFABCD",
                "t": "ACEFBDACEF",
                "lcs_length": 6,
            },
            5: {
                "alphabet": "ABCDEFGH",
                "n1": 12,
                "n2": 12,
                "s": "ABCDEFGHABCD",
                "t": "ACEGBDFHACEG",
                "lcs_length": 7,
            },
        },
        "en": {
            1: {
                "alphabet": "ABC",
                "n1": 4,
                "n2": 4,
                "s": "ABAC",
                "t": "ABBC",
                "lcs_length": 3,
            },
            2: {
                "alphabet": "ABCD",
                "n1": 6,
                "n2": 6,
                "s": "ABCDAB",
                "t": "ACBDAC",
                "lcs_length": 4,
            },
            3: {
                "alphabet": "ABCDE",
                "n1": 8,
                "n2": 8,
                "s": "ABCDEABC",
                "t": "ACEABCDE",
                "lcs_length": 6,
            },
            4: {
                "alphabet": "ABCDEF",
                "n1": 10,
                "n2": 10,
                "s": "ABCDEFABCD",
                "t": "ACEFBDACEF",
                "lcs_length": 6,
            },
            5: {
                "alphabet": "ABCDEFGH",
                "n1": 12,
                "n2": 12,
                "s": "ABCDEFGHABCD",
                "t": "ACEGBDFHACEG",
                "lcs_length": 7,
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
        
        alphabet_display = "{" + ", ".join(cfg["alphabet"]) + "}"
        
        self._game_info["alphabet"] = cfg["alphabet"]
        self._game_info["alphabet_display"] = alphabet_display
        self._game_info["n1"] = cfg["n1"]
        self._game_info["n2"] = cfg["n2"]
        
        self.sequence_s = cfg["s"]
        self.sequence_t = cfg["t"]
        
        self.true_lcs_length = cfg["lcs_length"]
        
        assert len(self.sequence_s) == cfg["n1"], "S length mismatch"
        assert len(self.sequence_t) == cfg["n2"], "T length mismatch"
        
        computed_lcs = self._compute_lcs_length(self.sequence_s, self.sequence_t)
        assert computed_lcs == self.true_lcs_length, (
            f"LCS length mismatch for difficulty {diff}: "
            f"configured {self.true_lcs_length}, computed {computed_lcs}"
        )

    def _compute_lcs_length(self, x, y):
        m, n = len(x), len(y)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if x[i - 1] == y[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        
        return dp[m][n]

    def _is_subsequence(self, subseq, seq):
        it = iter(seq)
        return all(char in it for char in subseq)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        
        if "K=" in raw_ans or "k=" in raw_ans:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip().upper()] = v.strip()
            
            if "K" not in ans_dict:
                return False
            
            try:
                k_value = int(ans_dict["K"])
            except ValueError:
                return False
            
            if k_value != self.true_lcs_length:
                return False
            
            if "W" in ans_dict:
                w_seq = ans_dict["W"]
                if len(w_seq) != k_value:
                    return False
                if not (self._is_subsequence(w_seq, self.sequence_s) and 
                        self._is_subsequence(w_seq, self.sequence_t)):
                    return False
            
            return True
        else:
            try:
                k_value = int(raw_ans)
                return k_value == self.true_lcs_length
            except ValueError:
                return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format."

        if "query_lcs" in parsed_info:
            p_seq = parsed_info["query_lcs"].strip()
            
            if not all(c in self._game_info["alphabet"] for c in p_seq):
                return error_format
            
            a = self._compute_lcs_length(p_seq, self.sequence_s)
            b = self._compute_lcs_length(p_seq, self.sequence_t)
            
            return f"({a}, {b})"

        elif "query_subseq" in parsed_info:
            p_seq = parsed_info["query_subseq"].strip()
            
            if not all(c in self._game_info["alphabet"] for c in p_seq):
                return error_format
            
            is_subseq_s = self._is_subsequence(p_seq, self.sequence_s)
            is_subseq_t = self._is_subsequence(p_seq, self.sequence_t)
            
            return yes_res if (is_subseq_s and is_subseq_t) else no_res

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        import re as _re
        
        tuple_match = _re.match(r'^\((\d+),\s*(\d+)\)$', correct.strip())
        if tuple_match:
            a, b = int(tuple_match.group(1)), int(tuple_match.group(2))
            return f"({a + 1}, {b})"
        
        if correct.strip().lstrip('-').isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        
        if self.config.language == "en":
            if correct == "Yes": return "No"
            if correct == "No": return "Yes"
            if correct == "YES": return "NO"
            if correct == "NO": return "YES"
            if correct == "yes": return "no"
            if correct == "no": return "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        alphabet = self._game_info["alphabet"]
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        max_query_length = 2
        candidates = []
        for length in range(1, max_query_length + 1):
            for p in itertools.product(alphabet, repeat=length):
                candidates.append("".join(p))
        
        for p_seq in candidates:
            a = self._compute_lcs_length(p_seq, self.sequence_s)
            b = self._compute_lcs_length(p_seq, self.sequence_t)
            lcs_ans = f"({a}, {b})"
            
            queries.append({
                "query": f"<query_lcs>{p_seq}</query_lcs>",
                "answer": lcs_ans
            })
            
            is_subseq_s = self._is_subsequence(p_seq, self.sequence_s)
            is_subseq_t = self._is_subsequence(p_seq, self.sequence_t)
            subseq_ans = yes_res if (is_subseq_s and is_subseq_t) else no_res
            
            queries.append({
                "query": f"<query_subseq>{p_seq}</query_subseq>",
                "answer": subseq_ans
            })
            
        return queries