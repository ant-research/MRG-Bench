from .base import Game
import re
import itertools

class SequenceReconstructionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"序列重构"的推理游戏，规则如下：

游戏设定了一个未知的有序序列 S，它由字母表 Σ 中的符号组成，长度为 {N}。字母表包含：{sigma}。序列在整个游戏过程中保持不变，字母表中的符号仅作为区分标签使用。

你的目标是通过询问来推断出这个完整序列 S。你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实序列如实回答：

1. 成员询问：给定一个模式串 P（长度在 1 到 {N} 之间，由字母表中的符号组成），询问 P 是否为 S 的连续子串。回答"是"或"否"。

2. 计数询问：给定一个模式串 P（长度在 1 到 {N} 之间，由字母表中的符号组成），询问 P 在 S 中作为连续子串出现的次数（允许重叠计数）。回答一个非负整数。

3. 完整猜测：给定一个长度为 {N} 的序列 G（由字母表中的符号组成），询问 G 是否与 S 完全一致。回答"是"或"否"。若回答为"是"，游戏立即成功结束。

请注意：
- 无效的请求（模式串长度越界、包含非字母表符号、格式错误等）会返回"无效"提示，且不计入有效询问次数。
- 每次有效请求都会计入你的询问次数。请尽可能用最少的询问次数找到答案。
- 如果超过询问次数限制仍未通过完整猜测得到"是"的回答，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 成员询问（例如询问模式串"AB"）：
<query_member>AB</query_member>

- 计数询问（例如询问模式串"AB"出现次数）：
<query_count>AB</query_count>

- 完整猜测（例如猜测完整序列为"ABCD"）：
<guess>ABCD</guess>

当你确信已经推断出完整序列时，使用完整猜测进行提交。
"""

    game_rule_en = """\
Let's play a "Sequence Reconstruction" deduction game. Here are the rules:

There is an unknown ordered sequence S composed of symbols from alphabet Σ, with length {N}. The alphabet contains: {sigma}. The sequence remains constant throughout the game, and symbols in the alphabet are used only as distinguishing labels.

Your goal is to infer the complete sequence S through queries. You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully based on the real sequence:

1. Membership Query: Given a pattern string P (length between 1 and {N}, composed of symbols from the alphabet), ask if P is a contiguous substring of S. Answer "Yes" or "No".

2. Count Query: Given a pattern string P (length between 1 and {N}, composed of symbols from the alphabet), ask how many times P appears as a contiguous substring in S (overlapping occurrences are counted). Answer a non-negative integer.

3. Complete Guess: Given a sequence G of length {N} (composed of symbols from the alphabet), ask if G is exactly the same as S. Answer "Yes" or "No". If the answer is "Yes", the game ends successfully immediately.

Please note:
- Invalid requests (pattern length out of bounds, containing non-alphabet symbols, format errors, etc.) will return an "invalid" message and do not count toward your valid query count.
- Each valid request counts toward your query count. Try to find the answer with as few queries as possible.
- If you exceed the query limit without getting a "Yes" answer through a complete guess, the game fails.

Each query must contain only one tag. Use the following XML format:

- Membership Query (e.g., querying pattern "AB"):
<query_member>AB</query_member>

- Count Query (e.g., querying occurrence count of pattern "AB"):
<query_count>AB</query_count>

- Complete Guess (e.g., guessing the complete sequence is "ABCD"):
<guess>ABCD</guess>

When you are confident you have inferred the complete sequence, submit it using a complete guess.
"""

    contextualized_rule_zh_1 = """\
欢迎使用交通信号走廊相位序列排查系统。

系统已记录了一条主干道上连续的未知信号相位序列 S，其长度为 {N} 个交叉路口。每个路口的相位由信号代码 Σ 组成，可选代码包含：{sigma}。该走廊的相位序列在排查期间保持稳定，代码仅用于区分不同路口的通行模式。

你的目标是通过系统查询来推断出整条走廊的完整相位序列 S。你可以反复向控制中心提出以下三类查询指令（每次仅限一个），系统将根据真实记录如实反馈：

1. 成员询问：给定一个局部相位串 P（长度在 1 到 {N} 之间，由信号代码组成），询问 P 是否为序列 S 中的连续路口相位组合。回答"是"或"否"。

2. 计数询问：给定一个局部相位串 P（长度在 1 到 {N} 之间，由信号代码组成），询问 P 在整条走廊序列 S 中作为连续相位组合出现的总次数（允许重叠计算）。回答一个非负整数。

3. 完整猜测：给定一个长度为 {N} 的全走廊序列 G（由信号代码组成），询问 G 是否与真实序列 S 完全吻合。回答"是"或"否"。若回答为"是"，排查任务立即成功结束。

请注意：
- 无效的请求（相位串长度越界、包含未注册信号代码、格式错误等）会返回"无效"提示，且不计入有效查询次数。
- 每次有效请求都会计入你的系统调用次数。请尽可能用最少的查询次数完成排查。
- 如果超过调用限制仍未通过完整猜测得到"是"的回答，排查任务失败。

每次查询只能包含一个指令标签。请使用以下 XML 格式：

- 成员询问（例如询问连续相位组合"AB"）：
<query_member>AB</query_member>

- 计数询问（例如询问相位组合"AB"出现次数）：
<query_count>AB</query_count>

- 完整猜测（例如提交全走廊序列为"ABCD"）：
<guess>ABCD</guess>

当你确信已经掌握完整的相位序列时，请使用完整猜测指令进行最终提交。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Traffic Signal Corridor Phase Sequence Investigation System.

The system has recorded an unknown continuous signal phase sequence S along a major arterial road, spanning a length of {N} intersections. The phase at each intersection is represented by a signal code from the set Σ, which includes: {sigma}. The phase sequence remains stable throughout the investigation, and the codes serve solely to distinguish different traffic flow patterns.

Your objective is to deduce the complete phase sequence S of the corridor through system queries. You may repeatedly submit the following three types of queries to the control center (one per request), and the system will provide factual feedback based on the true records:

1. Membership Query: Given a localized phase pattern P (length between 1 and {N}, composed of signal codes), ask whether P exists as a contiguous subsequence of intersections in S. The answer will be "Yes" or "No".

2. Count Query: Given a localized phase pattern P (length between 1 and {N}, composed of signal codes), ask how many times P appears as a contiguous subsequence in S (overlapping occurrences are counted). The answer will be a non-negative integer.

3. Complete Guess: Given a full-corridor sequence G of length {N} (composed of signal codes), ask if G perfectly matches the true sequence S. The answer will be "Yes" or "No". If "Yes", the investigation concludes successfully immediately.

Please note:
- Invalid requests (pattern length out of bounds, containing unregistered signal codes, format errors, etc.) will return an "invalid" message and will not consume your valid query allowance.
- Each valid request consumes one system call. Please aim to complete the investigation with the minimum number of queries.
- If you exceed the query limit without receiving a "Yes" via a Complete Guess, the investigation fails.

Each query must contain only one command tag. Use the following XML format:

- Membership Query (e.g., querying contiguous phase pattern "AB"):
<query_member>AB</query_member>

- Count Query (e.g., querying the occurrence count of phase pattern "AB"):
<query_count>AB</query_count>

- Complete Guess (e.g., submitting the full-corridor sequence "ABCD"):
<guess>ABCD</guess>

When you are confident that you have deduced the full phase sequence, submit it using the Complete Guess command.
"""

    contextualized_rule_zh_2 = """\
欢迎使用基因测序序列重构系统。

系统中载入了一段未知的靶向 DNA 序列 S，它由核苷酸字母表 Σ 中的碱基符号组成，长度为 {N}。已知可选的碱基对包含：{sigma}。该测序样本在整个分析过程中保持稳定，碱基符号严格用于生化标记区分。

你的目标是通过生化探针查询来推断出完整的基因序列 S。你可以反复向分析仪提交以下三类测定请求（每次仅限一个请求），系统将基于真实的测序数据如实反馈：

1. 成员询问：输入一个探针片段 P（长度在 1 到 {N} 之间，由碱基符号组成），询问 P 是否为序列 S 的连续基因片段。回答"是"或"否"。

2. 计数询问：输入一个探针片段 P（长度在 1 到 {N} 之间，由碱基符号组成），询问 P 在序列 S 中作为连续基因片段出现的总频次（允许重叠匹配）。回答一个非负整数。

3. 完整猜测：提交一个长度为 {N} 的完整基因组 G（由碱基符号组成），询问 G 是否与靶向序列 S 完全一致。回答"是"或"否"。若回答为"是"，测序重构任务立即成功结束。

请注意：
- 无效的请求（探针长度越界、包含非靶向碱基、格式错误等）会返回"无效"提示，且不计入有效耗材次数。
- 每次有效请求都会消耗测定次数。请尽可能用最少的探针消耗完成序列破译。
- 如果超过测定次数限制仍未通过完整猜测得到"是"的回答，测序任务失败。

每次查询只能包含一个指令标签。请使用以下 XML 格式：

- 成员询问（例如探测碱基组合"AB"）：
<query_member>AB</query_member>

- 计数询问（例如统计碱基组合"AB"出现频次）：
<query_count>AB</query_count>

- 完整猜测（例如提交完整基因序列为"ABCD"）：
<guess>ABCD</guess>

当你确信已经破译出完整的靶向序列时，请使用完整猜测进行最终结果提交。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Genomic Sequence Reconstruction System.

An unknown targeted DNA sequence S has been loaded into the system. It is composed of nucleotide symbols from alphabet Σ, with a total length of {N}. The available base pairs include: {sigma}. The sequenced sample remains stable throughout the analysis, and the base symbols are strictly used for biochemical marker distinction.

Your objective is to deduce the complete genomic sequence S through biochemical probe queries. You can repeatedly submit the following three types of assay requests to the analyzer (one per request), and the system will provide factual feedback based on the true sequencing data:

1. Membership Query: Input a probe fragment P (length between 1 and {N}, composed of base symbols), and ask if P is a contiguous genetic segment within sequence S. The answer will be "Yes" or "No".

2. Count Query: Input a probe fragment P (length between 1 and {N}, composed of base symbols), and ask for the total frequency of P appearing as a contiguous genetic segment in S (overlapping matches are counted). The answer will be a non-negative integer.

3. Complete Guess: Submit a complete genome G of length {N} (composed of base symbols), and ask if G perfectly matches the targeted sequence S. The answer will be "Yes" or "No". If "Yes", the sequencing reconstruction task concludes successfully immediately.

Please note:
- Invalid requests (probe length out of bounds, containing off-target bases, format errors, etc.) will return an "invalid" message and will not consume your valid assay allowance.
- Each valid request consumes one assay attempt. Please aim to decipher the sequence with minimum probe consumption.
- If you exceed the assay limit without receiving a "Yes" via a Complete Guess, the sequencing task fails.

Each query must contain only one command tag. Use the following XML format:

- Membership Query (e.g., probing base combination "AB"):
<query_member>AB</query_member>

- Count Query (e.g., counting the frequency of base combination "AB"):
<query_count>AB</query_count>

- Complete Guess (e.g., submitting the full genomic sequence "ABCD"):
<guess>ABCD</guess>

When you are confident that you have deciphered the complete targeted sequence, submit your final result using the Complete Guess command.
"""

    contextualized_rule_zh_3 = """\
欢迎进入教学模块路径规划系统。

系统预设了一条未知的最优学习路径序列 S，它由课程知识库 Σ 中的教学模块代码组成，总课时长度为 {N}。可选的模块代码包含：{sigma}。该标准学习路径在整个评估过程中保持固定，模块代码仅用于区分不同的知识单元。

你的目标是通过系统检索来推断出完整的学习路径序列 S。你可以反复向教务系统提出以下三类检视请求（每次仅限一个请求），系统将基于标准大纲如实反馈：

1. 成员询问：选定一个局部模块串 P（长度在 1 到 {N} 之间，由模块代码组成），询问 P 是否为大纲序列 S 中的连续授课环节。回答"是"或"否"。

2. 计数询问：选定一个局部模块串 P（长度在 1 到 {N} 之间，由模块代码组成），询问 P 在大纲序列 S 中作为连续授课环节出现的总次数（允许重叠统计）。回答一个非负整数。

3. 完整猜测：提交一份长度为 {N} 的完整教学大纲 G（由模块代码组成），询问 G 是否与最优路径序列 S 完全一致。回答"是"或"否"。若回答为"是"，路径重构任务立即成功结束。

请注意：
- 无效的请求（模块串长度越界、包含未开设模块、格式错误等）会返回"无效"提示，且不计入有效检索次数。
- 每次有效请求都会计入系统的检索消耗额度。请尽可能用最少的次数完成路径还原。
- 如果超过检索限制仍未通过完整猜测得到"是"的回答，路径还原失败。

每次请求只能包含一个指令标签。请使用以下 XML 格式：

- 成员询问（例如检索连续模块"AB"）：
<query_member>AB</query_member>

- 计数询问（例如统计连续模块"AB"的出现次数）：
<query_count>AB</query_count>

- 完整猜测（例如提交完整学习路径为"ABCD"）：
<guess>ABCD</guess>

当你确信已经推断出完整的学习路径时，请使用完整猜测进行排课提交。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Instructional Module Path Planning System.

The system has pre-configured an unknown optimal learning path sequence S, composed of instructional module codes from the curriculum knowledge base Σ, with a total duration length of {N}. The available module codes include: {sigma}. This standard learning path remains fixed throughout the evaluation, and the codes are used strictly to differentiate distinct knowledge units.

Your objective is to infer the complete learning path sequence S through system retrievals. You can repeatedly submit the following three types of review requests to the academic system (one per request), and the system will provide factual feedback based on the standard syllabus:

1. Membership Query: Select a localized module string P (length between 1 and {N}, composed of module codes), and ask if P is a contiguous teaching phase in the syllabus sequence S. The answer will be "Yes" or "No".

2. Count Query: Select a localized module string P (length between 1 and {N}, composed of module codes), and ask for the total number of times P appears as a contiguous teaching phase in sequence S (overlapping occurrences are counted). The answer will be a non-negative integer.

3. Complete Guess: Submit a complete syllabus G of length {N} (composed of module codes), and ask if G perfectly aligns with the optimal path sequence S. The answer will be "Yes" or "No". If "Yes", the path reconstruction task concludes successfully immediately.

Please note:
- Invalid requests (module string length out of bounds, containing unlisted modules, format errors, etc.) will return an "invalid" message and will not consume your valid retrieval allowance.
- Each valid request consumes one system retrieval quota. Please aim to restore the path with the minimum number of attempts.
- If you exceed the retrieval limit without receiving a "Yes" via a Complete Guess, the path restoration fails.

Each query must contain only one command tag. Use the following XML format:

- Membership Query (e.g., retrieving contiguous modules "AB"):
<query_member>AB</query_member>

- Count Query (e.g., counting the occurrences of continuous modules "AB"):
<query_count>AB</query_count>

- Complete Guess (e.g., submitting the full learning path "ABCD"):
<guess>ABCD</guess>

When you are confident that you have inferred the full learning path, submit your scheduling using the Complete Guess command.
"""

    contextualized_rule_zh_4 = """\
欢迎使用装配流水线工序序列排查系统。

生产线系统中记录了一段未知的标准工艺流程序列 S，它由工位代码库 Σ 中的操作符号组成，总工序长度为 {N}。已知的工位代码包含：{sigma}。该工艺流程在整个排查期间处于锁定状态，代码仅用于标记和区分不同的流水线动作。

你的目标是通过向工控主板发送测试指令来推导完整的工艺流程 S。你可以反复调用以下三类排查指令（每次仅限一个指令），主板将根据底层生产逻辑如实反馈：

1. 成员询问：输入一段局部工序指令 P（长度在 1 到 {N} 之间，由工位代码组成），询问 P 是否为流水线序列 S 中的连续操作段。回答"是"或"否"。

2. 计数询问：输入一段局部工序指令 P（长度在 1 到 {N} 之间，由工位代码组成），询问 P 在序列 S 中作为连续操作段出现的总次数（允许跨周期重叠统计）。回答一个非负整数。

3. 完整猜测：提交一份长度为 {N} 的完整流水线排班 G（由工位代码组成），询问 G 是否与标准工艺流程 S 完全一致。回答"是"或"否"。若回答为"是"，排查作业立即成功结束。

请注意：
- 无效的请求（指令长度越界、包含未识别工位代码、格式错误等）会触发"无效"警告，且不计入有效测试次数。
- 每次有效请求都会计入系统的测试负荷中。请尽可能用最少的指令次数完成流程解析。
- 如果超过测试限制仍未通过完整猜测得到"是"的回答，解析作业失败。

每次测试只能包含一个指令标签。请使用以下 XML 格式：

- 成员询问（例如测试连续工序"AB"）：
<query_member>AB</query_member>

- 计数询问（例如统计连续工序"AB"的执行次数）：
<query_count>AB</query_count>

- 完整猜测（例如提交完整工艺流程为"ABCD"）：
<guess>ABCD</guess>

当你确信已经推导出全部的标准工艺流程时，请使用完整猜测进行最终部署。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Assembly Line Process Sequence Investigation System.

The production line system has recorded an unknown standard operational process sequence S, composed of operation symbols from the workstation code library Σ, with a total process length of {N}. The available workstation codes include: {sigma}. This operational process remains locked throughout the investigation, and the codes are used strictly to tag and distinguish different assembly line actions.

Your objective is to deduce the complete operational process S by sending test commands to the industrial control board. You can repeatedly invoke the following three types of investigation commands (one per request), and the board will provide factual feedback based on the underlying production logic:

1. Membership Query: Input a localized process command P (length between 1 and {N}, composed of workstation codes), and ask if P is a contiguous operational segment in the assembly line sequence S. The answer will be "Yes" or "No".

2. Count Query: Input a localized process command P (length between 1 and {N}, composed of workstation codes), and ask for the total number of times P appears as a contiguous operational segment in sequence S (cross-cycle overlapping statistics are allowed). The answer will be a non-negative integer.

3. Complete Guess: Submit a complete assembly line schedule G of length {N} (composed of workstation codes), and ask if G perfectly matches the standard operational process S. The answer will be "Yes" or "No". If "Yes", the investigation task concludes successfully immediately.

Please note:
- Invalid requests (command length out of bounds, containing unrecognized workstation codes, format errors, etc.) will trigger an "invalid" warning and will not consume your valid test allowance.
- Each valid request adds to the system's test load. Please aim to parse the process with the minimum number of command inputs.
- If you exceed the test limit without receiving a "Yes" via a Complete Guess, the parsing task fails.

Each test must contain only one command tag. Use the following XML format:

- Membership Query (e.g., testing contiguous process "AB"):
<query_member>AB</query_member>

- Count Query (e.g., counting the execution times of continuous process "AB"):
<query_count>AB</query_count>

- Complete Guess (e.g., submitting the full operational process "ABCD"):
<guess>ABCD</guess>

When you are confident that you have deduced the entire standard operational process, submit it for final deployment using the Complete Guess command.
"""

    contextualized_rule_zh_5 = """\
欢迎使用司法程序流转序列审查系统。

案件管理系统中封装了一段未知的标准化诉讼流转序列 S，它由法定程序代码库 Σ 中的程序代号组成，总步骤长度为 {N}。合规的程序代号包含：{sigma}。该标准流转序列在整个审查周期内作为基准保持不变，代号仅用于区分不同的法律步骤。

你的目标是通过档案检索来推演完整的法定流转序列 S。你可以反复向合规数据库发起以下三类查证请求（每次仅限一个请求），系统将依据法定基准如实反馈：

1. 成员询问：提交一段局部程序组合 P（长度在 1 到 {N} 之间，由程序代号组成），询问 P 是否为流转序列 S 中的连续法定步骤。回答"是"或"否"。

2. 计数询问：提交一段局部程序组合 P（长度在 1 到 {N} 之间，由程序代号组成），询问 P 在流转序列 S 中作为连续法定步骤出现的总频次（允许阶段性重叠）。回答一个非负整数。

3. 完整猜测：提交一份长度为 {N} 的完整诉讼程序链 G（由程序代号组成），询问 G 是否与标准流转序列 S 完全吻合。回答"是"或"否"。若回答为"是"，审查结案任务立即成功结束。

请注意：
- 无效的请求（组合长度越界、包含未授权程序代号、格式错误等）将被系统驳回并提示"无效"，且不计入有效查证次数。
- 每次有效请求均会消耗案件查阅调档额度。请尽可能用最少的查证次数完成程序链还原。
- 如果超过调档额度限制仍未通过完整猜测得到"是"的回答，审查任务失败。

每次查证只能包含一个指令标签。请使用以下 XML 格式：

- 成员询问（例如查证连续法定步骤"AB"）：
<query_member>AB</query_member>

- 计数询问（例如统计连续法定步骤"AB"的发生频次）：
<query_count>AB</query_count>

- 完整猜测（例如提交完整诉讼程序链为"ABCD"）：
<guess>ABCD</guess>

当你确信已经推演出完整的标准化诉讼流转序列时，请使用完整猜测进行最终合规提交。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Judicial Procedure Routing Sequence Review System.

The case management system has encapsulated an unknown standardized litigation routing sequence S, composed of procedural codes from the statutory procedure repository Σ, with a total step length of {N}. The compliant procedural codes include: {sigma}. This standard routing sequence remains immutable as the benchmark throughout the review cycle, and the codes serve purely to distinguish different legal steps.

Your objective is to deduce the complete statutory routing sequence S through archive retrievals. You can repeatedly submit the following three types of verification requests to the compliance database (one per request), and the system will provide factual feedback based on the statutory benchmark:

1. Membership Query: Submit a localized procedure combination P (length between 1 and {N}, composed of procedural codes), and ask if P is a contiguous statutory step within the routing sequence S. The answer will be "Yes" or "No".

2. Count Query: Submit a localized procedure combination P (length between 1 and {N}, composed of procedural codes), and ask for the total frequency of P appearing as a contiguous statutory step in the routing sequence S (phase overlaps are allowed). The answer will be a non-negative integer.

3. Complete Guess: Submit a complete litigation procedure chain G of length {N} (composed of procedural codes), and ask if G perfectly matches the standard routing sequence S. The answer will be "Yes" or "No". If "Yes", the review and closure task concludes successfully immediately.

Please note:
- Invalid requests (combination length out of bounds, containing unauthorized procedural codes, format errors, etc.) will be rejected with an "invalid" prompt and will not consume your valid verification allowance.
- Each valid request consumes your case file retrieval quota. Please aim to reconstruct the procedural chain with the minimum number of verifications.
- If you exceed the retrieval quota without receiving a "Yes" via a Complete Guess, the review task fails.

Each verification must contain only one command tag. Use the following XML format:

- Membership Query (e.g., verifying contiguous statutory steps "AB"):
<query_member>AB</query_member>

- Count Query (e.g., counting the frequency of contiguous statutory steps "AB"):
<query_count>AB</query_count>

- Complete Guess (e.g., submitting the full litigation procedure chain "ABCD"):
<guess>ABCD</guess>

When you are confident that you have deduced the complete standardized litigation routing sequence, submit it for final compliance verification using the Complete Guess command.
"""

    tags = ["query_member", "query_count", "guess"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "N": 4,
                "sigma": ["A", "B"],
                "sequence": "ABAB",
                "query_limit": 10,
            },
            2: {
                "N": 6,
                "sigma": ["A", "B", "C"],
                "sequence": "ABCABC",
                "query_limit": 15,
            },
            3: {
                "N": 8,
                "sigma": ["A", "B", "C"],
                "sequence": "AABCBABC",
                "query_limit": 20,
            },
            4: {
                "N": 10,
                "sigma": ["A", "B", "C", "D"],
                "sequence": "ABCDABCDAB",
                "query_limit": 25,
            },
            5: {
                "N": 12,
                "sigma": ["A", "B", "C", "D", "E"],
                "sequence": "ABCDEABCDEBA",
                "query_limit": 30,
            },
        },
        "en": {
            1: {
                "N": 4,
                "sigma": ["A", "B"],
                "sequence": "ABAB",
                "query_limit": 10,
            },
            2: {
                "N": 6,
                "sigma": ["A", "B", "C"],
                "sequence": "ABCABC",
                "query_limit": 15,
            },
            3: {
                "N": 8,
                "sigma": ["A", "B", "C"],
                "sequence": "AABCBABC",
                "query_limit": 20,
            },
            4: {
                "N": 10,
                "sigma": ["A", "B", "C", "D"],
                "sequence": "ABCDABCDAB",
                "query_limit": 25,
            },
            5: {
                "N": 12,
                "sigma": ["A", "B", "C", "D", "E"],
                "sequence": "ABCDEABCDEBA",
                "query_limit": 30,
            },
        },
    }

    def __init__(self, config):
        self.valid_query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.N = cfg["N"]
        self.sigma = set(cfg["sigma"])
        self.sequence = cfg["sequence"]
        self.query_limit = cfg["query_limit"]
        
        self._game_info["N"] = self.N
        self._game_info["sigma"] = ", ".join(cfg["sigma"])

    def parse(self, response: str):
        response = response.strip()
        parsed_info = {}

        for tag in self.tags:
            pattern = rf'<{tag}>\s*(.*?)\s*</{tag}>'
            match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
            if match:
                parsed_info[tag] = match.group(1).strip()

        if "guess" in parsed_info and "answer" not in parsed_info:
            guess_val = parsed_info["guess"]
            is_valid, _ = self._validate_guess(guess_val)
            if is_valid:
                parsed_info["answer"] = parsed_info.pop("guess")
            else:
                pass

        contain_answer = "answer" in parsed_info
        contain_other = any(
            tag in parsed_info
            for tag in self.tags
            if tag not in ("answer", "guess")
        )
        contain_guess_unmapped = "guess" in parsed_info and "answer" not in parsed_info

        if contain_answer or contain_other or contain_guess_unmapped:
            return parsed_info
        else:
            raise ValueError(
                f"Invalid LLM response. Parsed tags: {list(parsed_info.keys())}; "
                f"expected tags: {list(self.tags)}, and require either 'answer' "
                f"or at least one query tag to be present."
            )

    def _validate_pattern(self, pattern: str) -> tuple:
        if not pattern:
            if self.config.language == "zh":
                return False, "错误：模式串不能为空。"
            else:
                return False, "Error: Pattern cannot be empty."
        
        if len(pattern) > self.N:
            if self.config.language == "zh":
                return False, f"错误：模式串长度超过序列长度 {self.N}。"
            else:
                return False, f"Error: Pattern length exceeds sequence length {self.N}."
        
        for char in pattern:
            if char not in self.sigma:
                if self.config.language == "zh":
                    return False, f"错误：模式串包含非字母表符号 '{char}'。"
                else:
                    return False, f"Error: Pattern contains invalid symbol '{char}'."
        
        return True, ""

    def _validate_guess(self, guess: str) -> tuple:
        if len(guess) != self.N:
            if self.config.language == "zh":
                return False, f"错误：猜测序列长度必须为 {self.N}，当前长度为 {len(guess)}。"
            else:
                return False, f"Error: Guess length must be {self.N}, current length is {len(guess)}."
        
        for char in guess:
            if char not in self.sigma:
                if self.config.language == "zh":
                    return False, f"错误：猜测序列包含非字母表符号 '{char}'。"
                else:
                    return False, f"Error: Guess contains invalid symbol '{char}'."
        
        return True, ""

    def evaluate(self, parsed_info):
        guess = parsed_info["answer"].strip()
        
        is_valid, error_msg = self._validate_guess(guess)
        if not is_valid:
            return False
        
        return guess == self.sequence
    
    def _cf_make_wrong(self, correct: str) -> str:
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

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        if "query_member" in parsed_info:
            pattern = parsed_info["query_member"].strip()
            
            is_valid, error_msg = self._validate_pattern(pattern)
            if not is_valid:
                return error_msg
            
            self.valid_query_count += 1
            
            if self.valid_query_count > self.query_limit:
                if self.config.language == "zh":
                    msg = f"已超过询问次数限制 {self.query_limit}。"
                else:
                    msg = f"Query limit {self.query_limit} exceeded."
                self.state.set_state("failed", "query_limit_exceeded")
                return msg
            
            is_substring = pattern in self.sequence
            return yes_res if is_substring else no_res

        elif "query_count" in parsed_info:
            pattern = parsed_info["query_count"].strip()
            
            is_valid, error_msg = self._validate_pattern(pattern)
            if not is_valid:
                return error_msg
            
            self.valid_query_count += 1
            
            if self.valid_query_count > self.query_limit:
                if self.config.language == "zh":
                    msg = f"已超过询问次数限制 {self.query_limit}。"
                else:
                    msg = f"Query limit {self.query_limit} exceeded."
                self.state.set_state("failed", "query_limit_exceeded")
                return msg
            
            count = 0
            pattern_len = len(pattern)
            for i in range(len(self.sequence) - pattern_len + 1):
                if self.sequence[i:i+pattern_len] == pattern:
                    count += 1
            
            return str(count)

        elif "guess" in parsed_info:
            guess_val = parsed_info["guess"].strip()
            is_valid, error_msg = self._validate_guess(guess_val)
            if not is_valid:
                return error_msg
            return yes_res if guess_val == self.sequence else no_res

        else:
            if self.config.language == "zh":
                return "错误：未找到有效的询问标签。"
            else:
                return "Error: No valid query tag found."

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        sorted_sigma = sorted(list(self.sigma))
        
        max_query_len = min(2, self.N)
        
        for length in range(1, max_query_len + 1):
            for p_tuple in itertools.product(sorted_sigma, repeat=length):
                pattern = "".join(p_tuple)
                
                is_substring = pattern in self.sequence
                ans_member = yes_res if is_substring else no_res
                
                queries.append({
                    "query": f"<query_member>{pattern}</query_member>",
                    "answer": ans_member
                })
                
                count = 0
                for i in range(len(self.sequence) - length + 1):
                    if self.sequence[i : i + length] == pattern:
                        count += 1
                ans_count = str(count)
                
                queries.append({
                    "query": f"<query_count>{pattern}</query_count>",
                    "answer": ans_count
                })
                
        return queries