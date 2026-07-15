from .base import Game
import random
import itertools
import re
from typing import List, Dict

class LongestCommonSubsequenceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"最长公共子序列推断"游戏，规则如下：

游戏设定了两个固定的隐藏序列 A 和 B，每个序列长度为 {n}，由字母表 {alphabet_display} 中的字符组成。

你的目标是推断出这两个序列的最长公共子序列（LCS）的长度 L。

- 子序列：从原序列中删除若干个（可以为零）字符，保持剩余字符的相对顺序不变所得到的序列。
- 最长公共子序列长度（LCS_len）：两个序列的所有公共子序列中最长的那个的长度。

你可以反复向我提出以下三类查询（每次仅限一个查询），我会根据隐藏序列如实回答：

1. **LCS探测查询**：提交一个序列 S（长度不超过 {n}），我会返回两个数值：S与A的LCS长度，以及S与B的LCS长度。

2. **公共子序列判定查询**：提交一个序列 T，我会回答 T 是否同时为 A 和 B 的子序列（回答"是"或"否"）。

3. **单序列子序列判定查询**：提交一个序列 U 并指明要判定的目标（A 或 B），我会回答 U 是否为指定序列的子序列（回答"是"或"否"）。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- LCS探测查询（例如探测序列"ABC"）：
<query_lcs>ABC</query_lcs>

- 公共子序列判定查询（例如判定序列"AB"）：
<query_common>AB</query_common>

- 单序列子序列判定查询（例如判定"AC"是否为A的子序列）：
<query_single>seq=AC, target=A</query_single>

提交最终答案时，必须给出你推断的最长公共子序列长度（一个非负整数），格式如下：

<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Longest Common Subsequence Inference" game. Here are the rules:

The game has set up two fixed hidden sequences A and B, each of length {n}, composed of characters from the alphabet {alphabet_display}.

Your goal is to infer the length L of the longest common subsequence (LCS) of these two sequences.

- Subsequence: A sequence derived from the original by deleting some (possibly zero) characters while maintaining the relative order of the remaining characters.
- Longest Common Subsequence Length (LCS_len): The length of the longest subsequence that is common to both sequences.

You can repeatedly ask me the following three types of queries (one per turn), and I will answer truthfully based on the hidden sequences:

1. **LCS Probe Query**: Submit a sequence S (length not exceeding {n}), and I will return two values: the LCS length between S and A, and the LCS length between S and B.

2. **Common Subsequence Check Query**: Submit a sequence T, and I will answer whether T is a subsequence of both A and B (answer "Yes" or "No").

3. **Single Sequence Subsequence Check Query**: Submit a sequence U and specify the target (A or B), and I will answer whether U is a subsequence of the specified sequence (answer "Yes" or "No").

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- LCS Probe Query (e.g., probing sequence "ABC"):
<query_lcs>ABC</query_lcs>

- Common Subsequence Check Query (e.g., checking sequence "AB"):
<query_common>AB</query_common>

- Single Sequence Subsequence Check Query (e.g., checking if "AC" is a subsequence of A):
<query_single>seq=AC, target=A</query_single>

When submitting the final answer, provide your inferred longest common subsequence length (a non-negative integer) in this format:

<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎进入城市交通路网分析系统。我们现在进行"城市路网关键共线枢纽推断"分析，规则如下：

系统记录了两条主干道（路线 A 和 路线 B）沿途经过的交通枢纽序列。
每条路线包含 {n} 个枢纽站点，由编号集合 {alphabet_display} 中的字符表示。

你的目标是推断出这两条主干道按相同顺序途径的最长公共枢纽链路的长度 L。

- 子路径（子序列）：按车辆实际行驶先后顺序经过的枢纽组合（可跳过部分非停靠站，但相对顺序不变）。
- 最大共线站数（LCS_len）：两条路线的所有公共子路径中最长的那一条所包含的枢纽数量。

你可以反复向系统提交以下三类探测查询（每次仅限一个查询）：

1. **共线探测查询**：提交一个测试路径 S（长度不超过 {n}），系统会返回两个数值：S与路线A的共线枢纽数，以及S与路线B的共线枢纽数。

2. **公共子路径判定查询**：提交一个测试路径 T，系统会回答 T 是否同时为路线 A 和 B 的子路径（回答"是"或"否"）。

3. **单一路线判定查询**：提交一个测试路径 U 并指明要判定的目标路线（A 或 B），系统会回答 U 是否为指定路线的子路径（回答"是"或"否"）。

当你收集到足够信息后，请提交最终推断的共线站数。若答案错误或格式不符，分析任务将判定失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 共线探测查询（例如探测路径"ABC"）：
<query_lcs>ABC</query_lcs>

- 公共子路径判定查询（例如判定路径"AB"）：
<query_common>AB</query_common>

- 单一路线判定查询（例如判定"AC"是否为路线A的子路径）：
<query_single>seq=AC, target=A</query_single>

提交最终答案时，必须给出你推断的最长公共枢纽链路长度（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Urban Traffic Network Analysis System. Let's conduct a "City Road Network Key Common Hub Inference" analysis. Here are the rules:

The system has recorded the sequence of transit hubs for two main arterial roads, Route A and Route B.
Each route consists of {n} hub stations, represented by characters from the set {alphabet_display}.

Your goal is to infer the length L of the longest common sequence of transit hubs visited in the same relative order by both routes.

- Sub-route (Subsequence): A combination of transit hubs visited in the actual chronological driving order (some non-stop stations can be skipped, but the relative order remains).
- Maximum Common Hubs Length (LCS_len): The number of hubs in the longest common sub-route shared by both routes.

You can repeatedly submit the following three types of probe queries to the system (one per turn):

1. **Collinear Probe Query**: Submit a test route S (length not exceeding {n}). The system will return two values: the collinear hub count between S and Route A, and the collinear hub count between S and Route B.

2. **Common Sub-route Check Query**: Submit a test route T. The system will answer whether T is a valid sub-route for both A and B (answer "Yes" or "No").

3. **Single Route Check Query**: Submit a test route U and specify the target route (A or B). The system will answer whether U is a valid sub-route of the specified route (answer "Yes" or "No").

When you have gathered enough information, submit your final inferred maximum common hubs length. If the answer is incorrect or improperly formatted, the analysis task fails.

Each query must contain only one tag. Use the following XML format:

- Collinear Probe Query (e.g., probing route "ABC"):
<query_lcs>ABC</query_lcs>

- Common Sub-route Check Query (e.g., checking route "AB"):
<query_common>AB</query_common>

- Single Route Check Query (e.g., checking if "AC" is a sub-route of Route A):
<query_single>seq=AC, target=A</query_single>

When submitting the final answer, provide your inferred maximum common hubs length (a non-negative integer) in this format:

<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用临床医学诊断辅助系统。我们现在进行"患者病理演变路径比对"分析，规则如下：

系统记录了两名罕见病患者（患者 A 和 患者 B）的基因突变或症状演变序列。
每位患者的完整演变记录包含 {n} 个阶段，由基因/症状标记集 {alphabet_display} 中的字符表示。

你的目标是推断出这两名患者按相同时间顺序表现出的最长公共演变路径的长度 L。

- 演变子路径（子序列）：按时间先后顺序发生的病情特征组合（可忽略部分次要中间特征，但整体发展顺序不变）。
- 最长公共演变路径长度（LCS_len）：两名患者所有的共同演变子路径中最长的那一条的标记数量。

你可以反复向系统提出以下三类病理探测查询（每次仅限一个查询）：

1. **演变路径探测查询**：提交一个测试路径 S（长度不超过 {n}），系统会返回两个数值：S与患者A演变记录的匹配长度，以及S与患者B演变记录的匹配长度。

2. **公共演变判定查询**：提交一个测试路径 T，系统会回答 T 是否同时为患者 A 和 B 经历过的演变子路径（回答"是"或"否"）。

3. **单患者演变判定查询**：提交一个测试路径 U 并指明要判定的目标（A 或 B），系统会回答 U 是否为指定患者经历过的演变子路径（回答"是"或"否"）。

当你收集到足够比对信息后，请提交最终推断的公共演变长度。若答案错误或格式不符，诊断分析将判定失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 演变路径探测查询（例如探测路径"ABC"）：
<query_lcs>ABC</query_lcs>

- 公共演变判定查询（例如判定路径"AB"）：
<query_common>AB</query_common>

- 单患者演变判定查询（例如判定"AC"是否为患者A的演变子路径）：
<query_single>seq=AC, target=A</query_single>

提交最终答案时，必须给出你推断的最长公共演变路径长度（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Clinical Diagnostic Assistant System. Let's conduct a "Patient Pathological Evolution Path Alignment" analysis. Here are the rules:

The system has recorded the genetic mutation or symptom evolution sequences for two patients with rare diseases, Patient A and Patient B.
Each patient's complete evolution record spans {n} stages, represented by characters from the genetic/symptom marker set {alphabet_display}.

Your goal is to infer the length L of the longest common evolution path exhibited by both patients in the same chronological order.

- Evolution Sub-path (Subsequence): A combination of pathological features occurring in chronological order (some minor intermediate features can be ignored, but the overall progression order remains unchanged).
- Longest Common Evolution Path Length (LCS_len): The number of markers in the longest common evolution sub-path shared by both patients.

You can repeatedly submit the following three types of pathological probe queries to the system (one per turn):

1. **Evolution Path Probe Query**: Submit a test path S (length not exceeding {n}). The system will return two values: the matching length between S and Patient A's record, and the matching length between S and Patient B's record.

2. **Common Evolution Check Query**: Submit a test path T. The system will answer whether T is a valid evolution sub-path experienced by both Patient A and Patient B (answer "Yes" or "No").

3. **Single Patient Evolution Check Query**: Submit a test path U and specify the target patient (A or B). The system will answer whether U is a valid evolution sub-path for the specified patient (answer "Yes" or "No").

When you have gathered enough alignment information, submit your final inferred common evolution length. If the answer is incorrect or improperly formatted, the diagnostic analysis fails.

Each query must contain only one tag. Use the following XML format:

- Evolution Path Probe Query (e.g., probing path "ABC"):
<query_lcs>ABC</query_lcs>

- Common Evolution Check Query (e.g., checking path "AB"):
<query_common>AB</query_common>

- Single Patient Evolution Check Query (e.g., checking if "AC" is an evolution sub-path of Patient A):
<query_single>seq=AC, target=A</query_single>

When submitting the final answer, provide your inferred longest common evolution path length (a non-negative integer) in this format:

<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎进入教研大纲分析终端。我们现在进行"跨版本教材知识链路比对"分析，规则如下：

系统收录了两套权威教材（版本 A 和 版本 B）的核心知识点教学大纲序列。
每套教材大纲包含 {n} 个知识模块，由学科模块代码集 {alphabet_display} 中的字符表示。

你的目标是推断出这两套教材在教学顺序上最长的一致知识点链路长度 L。

- 教学子链路（子序列）：按教材编排先后顺序出现的知识模块组合（可跳过部分拓展模块，但核心模块的教学相对顺序不变）。
- 最大一致教学链路长度（LCS_len）：两套教材所有的共同教学子链路中最长的那一条所包含的模块数量。

你可以反复向系统提交以下三类教研比对查询（每次仅限一个查询）：

1. **知识链路探测查询**：提交一个测试链路 S（长度不超过 {n}），系统会返回两个数值：S与教材A大纲的匹配长度，以及S与教材B大纲的匹配长度。

2. **公共链路判定查询**：提交一个测试链路 T，系统会回答 T 是否同时为教材 A 和 B 共有的教学子链路（回答"是"或"否"）。

3. **单一教材链路判定查询**：提交一个测试链路 U 并指明要判定的目标教材（A 或 B），系统会回答 U 是否为指定教材的教学子链路（回答"是"或"否"）。

当你收集到足够信息后，请提交最终推断的一致链路长度。若答案错误或格式不符，教研分析任务将判定失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 知识链路探测查询（例如探测链路"ABC"）：
<query_lcs>ABC</query_lcs>

- 公共链路判定查询（例如判定链路"AB"）：
<query_common>AB</query_common>

- 单一教材链路判定查询（例如判定"AC"是否为教材A的教学子链路）：
<query_single>seq=AC, target=A</query_single>

提交最终答案时，必须给出你推断的最长公共知识点链路长度（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Syllabus Analysis Terminal. Let's conduct a "Cross-Version Textbook Knowledge Chain Alignment" analysis. Here are the rules:

The system has cataloged the core knowledge syllabus sequences of two authoritative textbooks, Version A and Version B.
Each syllabus contains {n} knowledge modules, represented by characters from the subject module code set {alphabet_display}.

Your goal is to infer the length L of the longest consistent knowledge chain shared by both textbooks in their instructional order.

- Instructional Sub-chain (Subsequence): A combination of knowledge modules appearing in the textbook's sequential order (some expansion modules can be skipped, but the relative teaching order of the core modules remains unchanged).
- Maximum Consistent Instructional Chain Length (LCS_len): The number of modules in the longest common instructional sub-chain shared by both textbooks.

You can repeatedly submit the following three types of alignment queries to the system (one per turn):

1. **Knowledge Chain Probe Query**: Submit a test chain S (length not exceeding {n}). The system will return two values: the matching length between S and Textbook A's syllabus, and the matching length between S and Textbook B's syllabus.

2. **Common Chain Check Query**: Submit a test chain T. The system will answer whether T is a valid instructional sub-chain shared by both Textbook A and Textbook B (answer "Yes" or "No").

3. **Single Textbook Chain Check Query**: Submit a test chain U and specify the target textbook (A or B). The system will answer whether U is a valid instructional sub-chain for the specified textbook (answer "Yes" or "No").

When you have gathered enough information, submit your final inferred consistent chain length. If the answer is incorrect or improperly formatted, the analysis task fails.

Each query must contain only one tag. Use the following XML format:

- Knowledge Chain Probe Query (e.g., probing chain "ABC"):
<query_lcs>ABC</query_lcs>

- Common Chain Check Query (e.g., checking chain "AB"):
<query_common>AB</query_common>

- Single Textbook Chain Check Query (e.g., checking if "AC" is an instructional sub-chain of Textbook A):
<query_single>seq=AC, target=A</query_single>

When submitting the final answer, provide your inferred longest common knowledge chain length (a non-negative integer) in this format:

<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎访问工业控制与工艺分析中台。我们现在进行"自动化产线核心装配工序比对"分析，规则如下：

系统记录了两条自动化生产线（流水线 A 和 流水线 B）的标准装配工序序列。
每条流水线包含 {n} 个加工工位/工序节点，由工序代码集 {alphabet_display} 中的字符表示。

你的目标是推断出这两条生产线按相同顺序执行的最长公共核心装配流程的长度 L。

- 工序子序列（子序列）：按流水线加工先后顺序执行的操作组合（可忽略部分辅助工步，但核心工艺操作的相对顺序不变）。
- 最长一致装配流程长度（LCS_len）：两条流水线所有的公共工序子序列中最长的那一条所包含的工步数量。

你可以反复向工艺分析系统提交以下三类查询（每次仅限一个查询）：

1. **工序段探测查询**：提交一个测试工序段 S（长度不超过 {n}），系统会返回两个数值：S与流水线A的工艺匹配长度，以及S与流水线B的工艺匹配长度。

2. **公共工艺判定查询**：提交一个测试工序段 T，系统会回答 T 是否同时为流水线 A 和 B 的合法工序子序列（回答"是"或"否"）。

3. **单线工艺判定查询**：提交一个测试工序段 U 并指明要判定的目标生产线（A 或 B），系统会回答 U 是否为指定流水线的合法工序子序列（回答"是"或"否"）。

当你收集到足够信息后，请提交最终推断的一致工序长度。若答案错误或格式不符，工艺分析将判定失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 工序段探测查询（例如探测工艺段"ABC"）：
<query_lcs>ABC</query_lcs>

- 公共工艺判定查询（例如判定工艺段"AB"）：
<query_common>AB</query_common>

- 单线工艺判定查询（例如判定"AC"是否为流水线A的工序子序列）：
<query_single>seq=AC, target=A</query_single>

提交最终答案时，必须给出你推断的最长公共核心装配流程长度（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Control and Process Analysis Hub. Let's conduct an "Automated Production Line Core Assembly Process Alignment" analysis. Here are the rules:

The system has recorded the standard assembly process sequences for two automated production lines, Assembly Line A and Assembly Line B.
Each production line consists of {n} processing stations/nodes, represented by characters from the process code set {alphabet_display}.

Your goal is to infer the length L of the longest common core assembly workflow executed in the same order by both production lines.

- Process Subsequence: A combination of operations executed in the chronological order of the assembly line (some auxiliary steps can be ignored, but the relative order of core technical operations remains unchanged).
- Maximum Consistent Assembly Workflow Length (LCS_len): The number of processing steps in the longest common process subsequence shared by both assembly lines.

You can repeatedly submit the following three types of queries to the process analysis system (one per turn):

1. **Process Segment Probe Query**: Submit a test process segment S (length not exceeding {n}). The system will return two values: the process matching length between S and Assembly Line A, and the matching length between S and Assembly Line B.

2. **Common Process Check Query**: Submit a test process segment T. The system will answer whether T is a valid process subsequence for both Line A and Line B (answer "Yes" or "No").

3. **Single Line Process Check Query**: Submit a test process segment U and specify the target production line (A or B). The system will answer whether U is a valid process subsequence of the specified line (answer "Yes" or "No").

When you have gathered enough information, submit your final inferred consistent process length. If the answer is incorrect or improperly formatted, the process analysis fails.

Each query must contain only one tag. Use the following XML format:

- Process Segment Probe Query (e.g., probing segment "ABC"):
<query_lcs>ABC</query_lcs>

- Common Process Check Query (e.g., checking segment "AB"):
<query_common>AB</query_common>

- Single Line Process Check Query (e.g., checking if "AC" is a process subsequence of Assembly Line A):
<query_single>seq=AC, target=A</query_single>

When submitting the final answer, provide your inferred longest common core assembly workflow length (a non-negative integer) in this format:

<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用法务文档合规审查系统。我们现在进行"跨合同版本核心条款链比对"分析，规则如下：

系统提取了两份复杂商业合同（合同 A 和 合同 B）的核心条款架构序列。
每份合同正文包含 {n} 个条款模块，由条款类型代码集 {alphabet_display} 中的字符表示。

你的目标是比对并推断出这两份合同按相同顺序架构的最长公共核心条款链的长度 L。

- 核心条款链（子序列）：按合同正文先后顺序排列的条款组合（可跳过部分补充说明性质的条款，但核心约定的层级与相对顺序不变）。
- 最长一致条款架构长度（LCS_len）：两份合同所有的公共核心条款链中最长的那一条所包含的模块数量。

你可以反复向审查系统提交以下三类法务探测查询（每次仅限一个查询）：

1. **条款链探测查询**：提交一个测试条款序列 S（长度不超过 {n}），系统会返回两个数值：S与合同A的架构匹配长度，以及S与合同B的架构匹配长度。

2. **公共架构判定查询**：提交一个测试条款序列 T，系统会回答 T 是否同时为合同 A 和 B 共有的核心条款链（回答"是"或"否"）。

3. **单合同架构判定查询**：提交一个测试条款序列 U 并指明要判定的目标合同（A 或 B），系统会回答 U 是否为指定合同的合法条款链（回答"是"或"否"）。

当你收集到足够信息后，请提交最终推断的一致架构长度。若答案错误或格式不符，合规审查分析将判定失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 条款链探测查询（例如探测条款"ABC"）：
<query_lcs>ABC</query_lcs>

- 公共架构判定查询（例如判定条款链"AB"）：
<query_common>AB</query_common>

- 单合同架构判定查询（例如判定"AC"是否为合同A的核心条款链）：
<query_single>seq=AC, target=A</query_single>

提交最终答案时，必须给出你推断的最长公共核心条款链长度（一个非负整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Legal Document Compliance Review System. Let's conduct a "Cross-Contract Core Clause Chain Alignment" analysis. Here are the rules:

The system has extracted the core clause architectural sequences of two complex commercial contracts, Contract A and Contract B.
The main body of each contract consists of {n} clause modules, represented by characters from the clause type code set {alphabet_display}.

Your goal is to align and infer the length L of the longest common core clause chain structured in the same order across both contracts.

- Core Clause Chain (Subsequence): A combination of clauses arranged in the sequential order of the contract text (some supplementary clauses can be skipped, but the hierarchy and relative order of core agreements remain unchanged).
- Maximum Consistent Clause Architecture Length (LCS_len): The number of modules in the longest common core clause chain shared by both contracts.

You can repeatedly submit the following three types of legal probe queries to the review system (one per turn):

1. **Clause Chain Probe Query**: Submit a test clause sequence S (length not exceeding {n}). The system will return two values: the architectural matching length between S and Contract A, and the matching length between S and Contract B.

2. **Common Architecture Check Query**: Submit a test clause sequence T. The system will answer whether T is a valid core clause chain shared by both Contract A and Contract B (answer "Yes" or "No").

3. **Single Contract Architecture Check Query**: Submit a test clause sequence U and specify the target contract (A or B). The system will answer whether U is a valid clause chain within the specified contract (answer "Yes" or "No").

When you have gathered enough information, submit your final inferred consistent architecture length. If the answer is incorrect or improperly formatted, the compliance review analysis fails.

Each query must contain only one tag. Use the following XML format:

- Clause Chain Probe Query (e.g., probing sequence "ABC"):
<query_lcs>ABC</query_lcs>

- Common Architecture Check Query (e.g., checking chain "AB"):
<query_common>AB</query_common>

- Single Contract Architecture Check Query (e.g., checking if "AC" is a core clause chain of Contract A):
<query_single>seq=AC, target=A</query_single>

When submitting the final answer, provide your inferred longest common core clause chain length (a non-negative integer) in this format:

<answer>5</answer>
"""

    tags = ["answer", "query_lcs", "query_common", "query_single"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "alphabet": ["A", "B"],
                "sequence_A": "AABBA",
                "sequence_B": "ABAAB",
                "lcs_length": 3,
            },
            2: {
                "n": 6,
                "alphabet": ["A", "B", "C"],
                "sequence_A": "ABCABC",
                "sequence_B": "ACBACB",
                "lcs_length": 4,
            },
            3: {
                "n": 8,
                "alphabet": ["A", "B", "C", "D"],
                "sequence_A": "ABCDABCD",
                "sequence_B": "ACBDACBD",
                "lcs_length": 6,
            },
            4: {
                "n": 10,
                "alphabet": ["A", "B", "C", "D", "E"],
                "sequence_A": "ABCDEABCDE",
                "sequence_B": "ACEBDACEBD",
                "lcs_length": 6,
            },
            5: {
                "n": 12,
                "alphabet": ["A", "B", "C", "D", "E", "F"],
                "sequence_A": "ABCDEFABCDEF",
                "sequence_B": "ACEDBFACEDBF",
                "lcs_length": 8,
            },
        },
        "en": {
            1: {
                "n": 5,
                "alphabet": ["A", "B"],
                "sequence_A": "AABBA",
                "sequence_B": "ABAAB",
                "lcs_length": 3,
            },
            2: {
                "n": 6,
                "alphabet": ["A", "B", "C"],
                "sequence_A": "ABCABC",
                "sequence_B": "ACBACB",
                "lcs_length": 4,
            },
            3: {
                "n": 8,
                "alphabet": ["A", "B", "C", "D"],
                "sequence_A": "ABCDABCD",
                "sequence_B": "ACBDACBD",
                "lcs_length": 6,
            },
            4: {
                "n": 10,
                "alphabet": ["A", "B", "C", "D", "E"],
                "sequence_A": "ABCDEABCDE",
                "sequence_B": "ACEBDACEBD",
                "lcs_length": 6,
            },
            5: {
                "n": 12,
                "alphabet": ["A", "B", "C", "D", "E", "F"],
                "sequence_A": "ABCDEFABCDEF",
                "sequence_B": "ACEDBFACEDBF",
                "lcs_length": 8,
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
        self._game_info["alphabet_display"] = "{" + ", ".join(cfg["alphabet"]) + "}"
        
        self.sequence_A = cfg["sequence_A"]
        self.sequence_B = cfg["sequence_B"]
        self.correct_lcs_length = cfg["lcs_length"]
        self.alphabet = set(cfg["alphabet"])

    def _compute_lcs_length(self, seq1, seq2):
        m, n = len(seq1), len(seq2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if seq1[i-1] == seq2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        return dp[m][n]

    def _is_subsequence(self, subseq, seq):
        it = iter(seq)
        return all(char in it for char in subseq)

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.correct_lcs_length
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效。"
            error_target = "错误：目标必须是 A 或 B。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format."
            error_target = "Error: Target must be A or B."

        if "query_lcs" in parsed_info:
            seq_s = parsed_info["query_lcs"].strip()
            lcs_a = self._compute_lcs_length(seq_s, self.sequence_A)
            lcs_b = self._compute_lcs_length(seq_s, self.sequence_B)
            return f"({lcs_a}, {lcs_b})"

        elif "query_common" in parsed_info:
            seq_t = parsed_info["query_common"].strip()
            is_sub_a = self._is_subsequence(seq_t, self.sequence_A)
            is_sub_b = self._is_subsequence(seq_t, self.sequence_B)
            return yes_res if (is_sub_a and is_sub_b) else no_res

        elif "query_single" in parsed_info:
            try:
                raw = parsed_info["query_single"]
                parts = [x.strip() for x in raw.split(",")]
                query_dict = {}
                for part in parts:
                    if "=" in part:
                        k, v = part.split("=", 1)
                        query_dict[k.strip()] = v.strip()
                
                if "seq" not in query_dict or "target" not in query_dict:
                    return error_format
                
                seq_u = query_dict["seq"]
                target = query_dict["target"].upper()
                
                if target == "A":
                    result = self._is_subsequence(seq_u, self.sequence_A)
                elif target == "B":
                    result = self._is_subsequence(seq_u, self.sequence_B)
                else:
                    return error_target
                
                return yes_res if result else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            yes_str, no_str = "是", "否"
        else:
            yes_str, no_str = "Yes", "No"
        
        if correct == yes_str:
            return no_str
        if correct == no_str:
            return yes_str
        
        match = re.match(r'\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)\s*', correct)
        if match:
            a, b = int(match.group(1)), int(match.group(2))
            wrong_a = a + 1 if a == 0 else a - 1
            return f"({wrong_a}, {b})"
        
        return correct + " (modified)"

    def get_all_possible_queries(self) -> List[Dict]:
        queries = []
        n = self._game_info["n"]
        alphabet = sorted(list(self.alphabet))
        
        limit_len = min(n, 2)

        if self.config.language == "zh":
            yes_str, no_str = "是", "否"
        else:
            yes_str, no_str = "Yes", "No"

        for length in range(1, limit_len + 1):
            for p in itertools.product(alphabet, repeat=length):
                seq_str = "".join(p)
                
                lcs_a = self._compute_lcs_length(seq_str, self.sequence_A)
                lcs_b = self._compute_lcs_length(seq_str, self.sequence_B)
                queries.append({
                    "query": f"<query_lcs>{seq_str}</query_lcs>",
                    "answer": f"({lcs_a}, {lcs_b})"
                })
                
                is_sub_a = self._is_subsequence(seq_str, self.sequence_A)
                is_sub_b = self._is_subsequence(seq_str, self.sequence_B)
                ans_common = yes_str if (is_sub_a and is_sub_b) else no_str
                queries.append({
                    "query": f"<query_common>{seq_str}</query_common>",
                    "answer": ans_common
                })
                
                ans_a = yes_str if is_sub_a else no_str
                queries.append({
                    "query": f"<query_single>seq={seq_str}, target=A</query_single>",
                    "answer": ans_a
                })
                
                ans_b = yes_str if is_sub_b else no_str
                queries.append({
                    "query": f"<query_single>seq={seq_str}, target=B</query_single>",
                    "answer": ans_b
                })
                
        return queries