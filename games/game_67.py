from .base import Game
import random
import re

class SequenceOrderVerificationGame(Game):

    game_rule_zh = """\
我们来玩一个"序列顺序验证"的推理游戏，规则如下：

游戏设定了一个可见的序列 s = (s1, s2, ..., sN)，其中 N = {n}，每个符号 si 属于符号集合 {symbol_set}。我已经秘密为所有符号定义了一个严格的全序关系（每两个不同符号都有严格的先后关系，这个顺序在本局游戏中固定不变）。

定义非严格关系：符号 x "不晚于" 符号 y，当且仅当 x 等于 y，或 x 严格早于 y。

序列"合规"的定义：对于所有相邻位置 i 和 i+1（1 <= i < N），都满足 si "不晚于" si+1。

你的序列是：{sequence}

你的目标是：
1. 判断该序列是否合规
2. 提交判断结果并给出形式化的证明
3. 如果判断为合规，还需要给出本局出现过的所有不同符号的相对次序

你可以向我提出以下两类问题（每次仅限一个问题），我会根据隐藏的符号顺序如实回答：

1. 比较查询：询问两个不同符号 a 和 b 的先后关系（a 和 b 必须是序列中出现过的符号，且 a 不等于 b）。我会回答"a 早于 b"或"b 早于 a"。

2. 相邻检查：询问序列中某个相邻位置对（位置 i 和 i+1，其中 1 <= i < N）是否满足"不晚于"关系。我会回答"就位"（表示 si 不晚于 si+1）或"错位"（表示 si 严格晚于 si+1）。

每次询问只能包含一个标签，使用以下 XML 格式：

- 比较查询（例如询问符号 A 和 B 的先后关系）：
<query_compare>A,B</query_compare>

- 相邻检查（例如检查位置 1 和 2，即索引为 1）：
<query_adjacent>1</query_adjacent>

提交最终答案时，必须说明判断结果（合规或不合规）并提供证明，格式如下：

- 若判断为合规，必须给出所有出现符号的完整先后链（用逗号隔开，从早到晚）：
<answer>status=合规, order=A,B,C</answer>

- 若判断为不合规，必须给出一个证据位置对 i,j（i < j）或单个相邻位置 i，证明存在逆序：
<answer>status=不合规, evidence=2,5</answer>
或
<answer>status=不合规, evidence=3</answer>

注意：
- 如果你声明"合规"，我会检查你提供的符号顺序是否与我的隐藏顺序一致，以及序列是否真的合规
- 如果你声明"不合规"，我会检查你提供的证据位置是否真的存在逆序
- 答案错误或格式不符，游戏失败
"""

    game_rule_en = """\
Let's play a "Sequence Order Verification" deduction game. Here are the rules:

A visible sequence s = (s1, s2, ..., sN) is given, where N = {n}, and each symbol si belongs to the symbol set {symbol_set}. I have secretly defined a strict total order over all symbols (every two different symbols have a strict precedence relation, which remains fixed throughout this game).

Define the non-strict relation: symbol x is "no later than" symbol y if and only if x equals y, or x is strictly earlier than y.

A sequence is "compliant" if: for all adjacent positions i and i+1 (1 <= i < N), si is "no later than" si+1.

Your sequence is: {sequence}

Your goals are:
1. Determine whether the sequence is compliant
2. Submit your judgment with formal justification
3. If judged compliant, also provide the relative order of all distinct symbols appearing in this game

You can ask me the following two types of questions (one per turn), and I will answer truthfully based on the hidden symbol order:

1. Comparison Query: Ask about the precedence relation between two different symbols a and b (a and b must appear in the sequence, and a ≠ b). I will answer "a before b" or "b before a".

2. Adjacency Check: Ask whether a specific adjacent position pair in the sequence (position i and i+1, where 1 <= i < N) satisfies the "no later than" relation. I will answer "in-place" (meaning si is no later than si+1) or "out-of-place" (meaning si is strictly later than si+1).

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about symbols A and B):
<query_compare>A,B</query_compare>

- Adjacency Check (e.g., checking positions 1 and 2, with index 1):
<query_adjacent>1</query_adjacent>

When submitting the final answer, specify the judgment result (compliant or non-compliant) and provide justification in the following format:

- If judged compliant, provide the complete precedence chain of all appearing symbols (comma-separated, from earliest to latest):
<answer>status=compliant, order=A,B,C</answer>

- If judged non-compliant, provide evidence as a position pair i,j (i < j) or a single adjacent position i, proving an inversion exists:
<answer>status=non-compliant, evidence=2,5</answer>
or
<answer>status=non-compliant, evidence=3</answer>

Note:
- If you claim "compliant", I will verify whether your provided symbol order matches my hidden order and whether the sequence is truly compliant
- If you claim "non-compliant", I will verify whether your provided evidence position truly has an inversion
- Incorrect answers or invalid formats will result in game failure
"""

    contextualized_rule_zh_1 = """\
[交通场景] 智能交通调度系统控制台。你需要验证列车发车序列的优先级合规性。

我们来玩一个"发车序列顺序验证"的推理游戏，规则如下：

记录显示了一个可见的发车序列 s = (s1, s2, ..., sN)，其中 N = {n}，每个车型代号 si 属于集合 {symbol_set}。我已经秘密为所有车型定义了一个严格的全序关系（每两个不同车型都有严格的调度先后关系，这个顺序在本局固定不变）。

定义非严格关系：车型 x "不晚于" 车型 y，当且仅当 x 等于 y，或 x 严格早于 y。

序列"合规"的定义：对于所有相邻位置 i 和 i+1（1 <= i < N），都满足 si "不晚于" si+1。

你的发车序列是：{sequence}

你的目标是：
1. 判断该序列是否合规
2. 提交判断结果并给出形式化的证明
3. 如果判断为合规，还需要给出本局出现过的所有不同车型的相对调度次序

你可以向我提出以下两类问题（每次仅限一个问题），我会根据隐藏的车型顺序如实回答：

1. 比较查询：询问两个不同车型 a 和 b 的先后关系（a 和 b 必须是序列中出现过的车型，且 a 不等于 b）。我会回答"a 早于 b"或"b 早于 a"。

2. 相邻检查：询问序列中某个相邻位置对（位置 i 和 i+1，其中 1 <= i < N）是否满足"不晚于"关系。我会回答"就位"（表示 si 不晚于 si+1）或"错位"（表示 si 严格晚于 si+1）。

每次询问只能包含一个标签，使用以下 XML 格式：

- 比较查询（例如询问车型 A 和 B 的先后关系）：
<query_compare>A,B</query_compare>

- 相邻检查（例如检查位置 1 和 2，即索引为 1）：
<query_adjacent>1</query_adjacent>

提交最终答案时，必须说明判断结果（合规或不合规）并提供证明，格式如下：

- 若判断为合规，必须给出所有出现车型的完整先后链（用逗号隔开，从早到晚）：
<answer>status=合规, order=A,B,C</answer>

- 若判断为不合规，必须给出一个证据位置对 i,j（i < j）或单个相邻位置 i，证明存在逆序：
<answer>status=不合规, evidence=2,5</answer>
或
<answer>status=不合规, evidence=3</answer>

注意：
- 如果你声明"合规"，我会检查你提供的车型顺序是否与我的隐藏顺序一致，以及序列是否真的合规
- 如果你声明"不合规"，我会检查你提供的证据位置是否真的存在逆序
- 答案错误或格式不符，游戏失败
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario] Intelligent Traffic Dispatch System Console. You need to verify the priority compliance of a train dispatch sequence.

Let's play a "Dispatch Sequence Order Verification" deduction game. Here are the rules:

A visible dispatch sequence s = (s1, s2, ..., sN) is logged, where N = {n}, and each train model si belongs to the set {symbol_set}. I have secretly defined a strict total order over all train models (a hidden dispatch priority order where every two different models have a strict precedence relation, fixed throughout this game).

Define the non-strict relation: model x is "no later than" model y if and only if x equals y, or x is strictly earlier in priority than y.

A sequence is "compliant" if: for all adjacent positions i and i+1 (1 <= i < N), si is "no later than" si+1.

Your dispatch sequence is: {sequence}

Your goals are:
1. Determine whether the sequence is compliant
2. Submit your judgment with formal justification
3. If judged compliant, also provide the relative order of all distinct models appearing in this game

You can ask me the following two types of questions (one per turn), and I will answer truthfully based on the hidden model order:

1. Comparison Query: Ask about the precedence relation between two different models a and b (a and b must appear in the sequence, and a ≠ b). I will answer "a before b" or "b before a".

2. Adjacency Check: Ask whether a specific adjacent position pair in the sequence (position i and i+1, where 1 <= i < N) satisfies the "no later than" relation. I will answer "in-place" (meaning si is no later than si+1) or "out-of-place" (meaning si is strictly later than si+1).

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about models A and B):
<query_compare>A,B</query_compare>

- Adjacency Check (e.g., checking positions 1 and 2, with index 1):
<query_adjacent>1</query_adjacent>

When submitting the final answer, specify the judgment result (compliant or non-compliant) and provide justification in the following format:

- If judged compliant, provide the complete precedence chain of all appearing models (comma-separated, from earliest to latest):
<answer>status=compliant, order=A,B,C</answer>

- If judged non-compliant, provide evidence as a position pair i,j (i < j) or a single adjacent position i, proving an inversion exists:
<answer>status=non-compliant, evidence=2,5</answer>
or
<answer>status=non-compliant, evidence=3</answer>

Note:
- If you claim "compliant", I will verify whether your provided order matches my hidden order and whether the sequence is truly compliant
- If you claim "non-compliant", I will verify whether your provided evidence position truly has an inversion
- Incorrect answers or invalid formats will result in game failure
"""

    contextualized_rule_zh_2 = """\
[医疗场景] 临床诊疗路径审核系统。你需要验证患者治疗步骤的临床阶段合规性。

我们来玩一个"诊疗序列顺序验证"的推理游戏，规则如下：

系统记录了一个可见的诊疗序列 s = (s1, s2, ..., sN)，其中 N = {n}，每个治疗步骤 si 属于集合 {symbol_set}。我已经秘密为所有步骤定义了一个严格的全序关系（即隐藏的临床阶段标准顺序，每两个不同步骤都有严格的先后关系，本局固定不变）。

定义非严格关系：步骤 x "不晚于" 步骤 y，当且仅当 x 等于 y，或 x 的标准阶段严格早于 y。

序列"合规"的定义：对于所有相邻的步骤位置 i 和 i+1（1 <= i < N），都满足 si 的阶段"不晚于" si+1。

你的诊疗序列是：{sequence}

你的目标是：
1. 判断该序列是否合规
2. 提交判断结果并给出形式化的证明
3. 如果判断为合规，还需要给出本局出现过的所有不同步骤的相对临床次序

你可以向我提出以下两类问题（每次仅限一个问题），我会根据隐藏的阶段顺序如实回答：

1. 比较查询：询问两个不同步骤 a 和 b 的先后关系（a 和 b 必须是序列中出现过的步骤，且 a 不等于 b）。我会回答"a 早于 b"或"b 早于 a"。

2. 相邻检查：询问序列中某个相邻位置对（位置 i 和 i+1，其中 1 <= i < N）是否满足"不晚于"关系。我会回答"就位"（表示 si 不晚于 si+1）或"错位"（表示 si 严格晚于 si+1）。

每次询问只能包含一个标签，使用以下 XML 格式：

- 比较查询（例如询问步骤 A 和 B 的先后关系）：
<query_compare>A,B</query_compare>

- 相邻检查（例如检查位置 1 和 2，即索引为 1）：
<query_adjacent>1</query_adjacent>

提交最终答案时，必须说明判断结果（合规或不合规）并提供证明，格式如下：

- 若判断为合规，必须给出所有出现步骤的完整先后链（用逗号隔开，从早到晚）：
<answer>status=合规, order=A,B,C</answer>

- 若判断为不合规，必须给出一个证据位置对 i,j（i < j）或单个相邻位置 i，证明存在逆序：
<answer>status=不合规, evidence=2,5</answer>
或
<answer>status=不合规, evidence=3</answer>

注意：
- 如果你声明"合规"，我会检查你提供的步骤顺序是否与我的隐藏顺序一致，以及序列是否真的合规
- 如果你声明"不合规"，我会检查你提供的证据位置是否真的存在逆序
- 答案错误或格式不符，游戏失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario] Clinical Pathway Audit System. You need to verify the clinical phase compliance of a patient's treatment step sequence.

Let's play a "Treatment Sequence Order Verification" deduction game. Here are the rules:

A visible treatment sequence s = (s1, s2, ..., sN) is given, where N = {n}, and each treatment step si belongs to the set {symbol_set}. I have secretly defined a strict total order over all steps (every two different steps have a strict precedence relation representing standard clinical phases, which remains fixed throughout this game).

Define the non-strict relation: step x is "no later than" step y if and only if x equals y, or x is strictly earlier in the clinical pathway than y.

A sequence is "compliant" if: for all adjacent positions i and i+1 (1 <= i < N), si is "no later than" si+1.

Your treatment sequence is: {sequence}

Your goals are:
1. Determine whether the sequence is compliant
2. Submit your judgment with formal justification
3. If judged compliant, also provide the relative order of all distinct steps appearing in this game

You can ask me the following two types of questions (one per turn), and I will answer truthfully based on the hidden clinical order:

1. Comparison Query: Ask about the precedence relation between two different steps a and b (a and b must appear in the sequence, and a ≠ b). I will answer "a before b" or "b before a".

2. Adjacency Check: Ask whether a specific adjacent position pair in the sequence (position i and i+1, where 1 <= i < N) satisfies the "no later than" relation. I will answer "in-place" (meaning si is no later than si+1) or "out-of-place" (meaning si is strictly later than si+1).

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about steps A and B):
<query_compare>A,B</query_compare>

- Adjacency Check (e.g., checking positions 1 and 2, with index 1):
<query_adjacent>1</query_adjacent>

When submitting the final answer, specify the judgment result (compliant or non-compliant) and provide justification in the following format:

- If judged compliant, provide the complete precedence chain of all appearing steps (comma-separated, from earliest to latest):
<answer>status=compliant, order=A,B,C</answer>

- If judged non-compliant, provide evidence as a position pair i,j (i < j) or a single adjacent position i, proving an inversion exists:
<answer>status=non-compliant, evidence=2,5</answer>
or
<answer>status=non-compliant, evidence=3</answer>

Note:
- If you claim "compliant", I will verify whether your provided step order matches my hidden order and whether the sequence is truly compliant
- If you claim "non-compliant", I will verify whether your provided evidence position truly has an inversion
- Incorrect answers or invalid formats will result in game failure
"""

    contextualized_rule_zh_3 = """\
[教育场景] 智能教学大纲评估系统。你需要验证教学模块序列的先修依赖合规性。

我们来玩一个"教学序列顺序验证"的推理游戏，规则如下：

系统排布了一个可见的教学序列 s = (s1, s2, ..., sN)，其中 N = {n}，每个教学模块 si 属于集合 {symbol_set}。我已经秘密为所有模块定义了一个严格的全序关系（即隐藏的先修依赖顺序，每两个不同模块都有严格的先后关系，本局固定不变）。

定义非严格关系：模块 x "不晚于" 模块 y，当且仅当 x 等于 y，或 x 的依赖层级严格早于 y。

序列"合规"的定义：对于所有相邻的教学位置 i 和 i+1（1 <= i < N），都满足 si 的层级"不晚于" si+1。

你的教学序列是：{sequence}

你的目标是：
1. 判断该序列是否合规
2. 提交判断结果并给出形式化的证明
3. 如果判断为合规，还需要给出本局出现过的所有不同模块的相对先修次序

你可以向我提出以下两类问题（每次仅限一个问题），我会根据隐藏的依赖顺序如实回答：

1. 比较查询：询问两个不同模块 a 和 b 的先后关系（a 和 b 必须是序列中出现过的模块，且 a 不等于 b）。我会回答"a 早于 b"或"b 早于 a"。

2. 相邻检查：询问序列中某个相邻位置对（位置 i 和 i+1，其中 1 <= i < N）是否满足"不晚于"关系。我会回答"就位"（表示 si 不晚于 si+1）或"错位"（表示 si 严格晚于 si+1）。

每次询问只能包含一个标签，使用以下 XML 格式：

- 比较查询（例如询问模块 A 和 B 的先后关系）：
<query_compare>A,B</query_compare>

- 相邻检查（例如检查位置 1 和 2，即索引为 1）：
<query_adjacent>1</query_adjacent>

提交最终答案时，必须说明判断结果（合规或不合规）并提供证明，格式如下：

- 若判断为合规，必须给出所有出现模块的完整先后链（用逗号隔开，从早到晚）：
<answer>status=合规, order=A,B,C</answer>

- 若判断为不合规，必须给出一个证据位置对 i,j（i < j）或单个相邻位置 i，证明存在逆序：
<answer>status=不合规, evidence=2,5</answer>
或
<answer>status=不合规, evidence=3</answer>

注意：
- 如果你声明"合规"，我会检查你提供的模块顺序是否与我的隐藏顺序一致，以及序列是否真的合规
- 如果你声明"不合规"，我会检查你提供的证据位置是否真的存在逆序
- 答案错误或格式不符，游戏失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario] Intelligent Syllabus Evaluation System. You need to verify the prerequisite compliance of a teaching module sequence.

Let's play a "Syllabus Sequence Order Verification" deduction game. Here are the rules:

A visible teaching sequence s = (s1, s2, ..., sN) is given, where N = {n}, and each teaching module si belongs to the set {symbol_set}. I have secretly defined a strict total order over all modules (every two different modules have a strict prerequisite precedence relation, which remains fixed throughout this game).

Define the non-strict relation: module x is "no later than" module y if and only if x equals y, or x is strictly earlier in the prerequisite hierarchy than y.

A sequence is "compliant" if: for all adjacent positions i and i+1 (1 <= i < N), si is "no later than" si+1.

Your teaching sequence is: {sequence}

Your goals are:
1. Determine whether the sequence is compliant
2. Submit your judgment with formal justification
3. If judged compliant, also provide the relative order of all distinct modules appearing in this game

You can ask me the following two types of questions (one per turn), and I will answer truthfully based on the hidden prerequisite order:

1. Comparison Query: Ask about the precedence relation between two different modules a and b (a and b must appear in the sequence, and a ≠ b). I will answer "a before b" or "b before a".

2. Adjacency Check: Ask whether a specific adjacent position pair in the sequence (position i and i+1, where 1 <= i < N) satisfies the "no later than" relation. I will answer "in-place" (meaning si is no later than si+1) or "out-of-place" (meaning si is strictly later than si+1).

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about modules A and B):
<query_compare>A,B</query_compare>

- Adjacency Check (e.g., checking positions 1 and 2, with index 1):
<query_adjacent>1</query_adjacent>

When submitting the final answer, specify the judgment result (compliant or non-compliant) and provide justification in the following format:

- If judged compliant, provide the complete precedence chain of all appearing modules (comma-separated, from earliest to latest):
<answer>status=compliant, order=A,B,C</answer>

- If judged non-compliant, provide evidence as a position pair i,j (i < j) or a single adjacent position i, proving an inversion exists:
<answer>status=non-compliant, evidence=2,5</answer>
or
<answer>status=non-compliant, evidence=3</answer>

Note:
- If you claim "compliant", I will verify whether your provided module order matches my hidden order and whether the sequence is truly compliant
- If you claim "non-compliant", I will verify whether your provided evidence position truly has an inversion
- Incorrect answers or invalid formats will result in game failure
"""

    contextualized_rule_zh_4 = """\
[工业制造场景] 自动化流水线工艺校验系统。你需要验证生产加工工序序列的依赖合规性。

我们来玩一个"工序序列顺序验证"的推理游戏，规则如下：

系统生成了一个可见的加工序列 s = (s1, s2, ..., sN)，其中 N = {n}，每道工序 si 属于集合 {symbol_set}。我已经秘密为所有工序定义了一个严格的全序关系（即隐藏的工艺约束顺序，每两个不同工序都有严格的先后关系，本局固定不变）。

定义非严格关系：工序 x "不晚于" 工序 y，当且仅当 x 等于 y，或 x 的工艺约束严格早于 y。

序列"合规"的定义：对于所有相邻的加工位置 i 和 i+1（1 <= i < N），都满足 si 的工艺"不晚于" si+1。

你的加工序列是：{sequence}

你的目标是：
1. 判断该序列是否合规
2. 提交判断结果并给出形式化的证明
3. 如果判断为合规，还需要给出本局出现过的所有不同工序的相对约束次序

你可以向我提出以下两类问题（每次仅限一个问题），我会根据隐藏的工艺顺序如实回答：

1. 比较查询：询问两个不同工序 a 和 b 的先后关系（a 和 b 必须是序列中出现过的工序，且 a 不等于 b）。我会回答"a 早于 b"或"b 早于 a"。

2. 相邻检查：询问序列中某个相邻位置对（位置 i 和 i+1，其中 1 <= i < N）是否满足"不晚于"关系。我会回答"就位"（表示 si 不晚于 si+1）或"错位"（表示 si 严格晚于 si+1）。

每次询问只能包含一个标签，使用以下 XML 格式：

- 比较查询（例如询问工序 A 和 B 的先后关系）：
<query_compare>A,B</query_compare>

- 相邻检查（例如检查位置 1 和 2，即索引为 1）：
<query_adjacent>1</query_adjacent>

提交最终答案时，必须说明判断结果（合规或不合规）并提供证明，格式如下：

- 若判断为合规，必须给出所有出现工序的完整先后链（用逗号隔开，从早到晚）：
<answer>status=合规, order=A,B,C</answer>

- 若判断为不合规，必须给出一个证据位置对 i,j（i < j）或单个相邻位置 i，证明存在逆序：
<answer>status=不合规, evidence=2,5</answer>
或
<answer>status=不合规, evidence=3</answer>

注意：
- 如果你声明"合规"，我会检查你提供的工序顺序是否与我的隐藏顺序一致，以及序列是否真的合规
- 如果你声明"不合规"，我会检查你提供的证据位置是否真的存在逆序
- 答案错误或格式不符，游戏失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario] Automated Assembly Line Audit System. You need to verify the dependency compliance of a production process sequence.

Let's play a "Production Sequence Order Verification" deduction game. Here are the rules:

A visible production sequence s = (s1, s2, ..., sN) is given, where N = {n}, and each process step si belongs to the set {symbol_set}. I have secretly defined a strict total order over all steps (every two different steps have a strict operational precedence relation, which remains fixed throughout this game).

Define the non-strict relation: step x is "no later than" step y if and only if x equals y, or x is strictly earlier in process dependency than y.

A sequence is "compliant" if: for all adjacent positions i and i+1 (1 <= i < N), si is "no later than" si+1.

Your production sequence is: {sequence}

Your goals are:
1. Determine whether the sequence is compliant
2. Submit your judgment with formal justification
3. If judged compliant, also provide the relative order of all distinct steps appearing in this game

You can ask me the following two types of questions (one per turn), and I will answer truthfully based on the hidden process order:

1. Comparison Query: Ask about the precedence relation between two different steps a and b (a and b must appear in the sequence, and a ≠ b). I will answer "a before b" or "b before a".

2. Adjacency Check: Ask whether a specific adjacent position pair in the sequence (position i and i+1, where 1 <= i < N) satisfies the "no later than" relation. I will answer "in-place" (meaning si is no later than si+1) or "out-of-place" (meaning si is strictly later than si+1).

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about steps A and B):
<query_compare>A,B</query_compare>

- Adjacency Check (e.g., checking positions 1 and 2, with index 1):
<query_adjacent>1</query_adjacent>

When submitting the final answer, specify the judgment result (compliant or non-compliant) and provide justification in the following format:

- If judged compliant, provide the complete precedence chain of all appearing steps (comma-separated, from earliest to latest):
<answer>status=compliant, order=A,B,C</answer>

- If judged non-compliant, provide evidence as a position pair i,j (i < j) or a single adjacent position i, proving an inversion exists:
<answer>status=non-compliant, evidence=2,5</answer>
or
<answer>status=non-compliant, evidence=3</answer>

Note:
- If you claim "compliant", I will verify whether your provided step order matches my hidden order and whether the sequence is truly compliant
- If you claim "non-compliant", I will verify whether your provided evidence position truly has an inversion
- Incorrect answers or invalid formats will result in game failure
"""

    contextualized_rule_zh_5 = """\
[法律场景] 司法程序合规性审查系统。你需要验证案件诉讼流程的法定程序合规性。

我们来玩一个"诉讼序列顺序验证"的推理游戏，规则如下：

卷宗记录了一个可见的诉讼序列 s = (s1, s2, ..., sN)，其中 N = {n}，每个程序动作 si 属于集合 {symbol_set}。我已经秘密为所有动作定义了一个严格的全序关系（即隐藏的法定程序顺序，每两个不同动作都有严格的先后关系，本案固定不变）。

定义非严格关系：动作 x "不晚于" 动作 y，当且仅当 x 等于 y，或 x 的法定顺位严格早于 y。

序列"合规"的定义：对于所有相邻的动作位置 i 和 i+1（1 <= i < N），都满足 si 的法定顺位"不晚于" si+1。

你的诉讼序列是：{sequence}

你的目标是：
1. 判断该序列是否合规
2. 提交判断结果并给出形式化的证明
3. 如果判断为合规，还需要给出本局出现过的所有不同动作的相对法定次序

你可以向我提出以下两类问题（每次仅限一个问题），我会根据隐藏的程序顺序如实回答：

1. 比较查询：询问两个不同动作 a 和 b 的先后关系（a 和 b 必须是序列中出现过的动作，且 a 不等于 b）。我会回答"a 早于 b"或"b 早于 a"。

2. 相邻检查：询问序列中某个相邻位置对（位置 i 和 i+1，其中 1 <= i < N）是否满足"不晚于"关系。我会回答"就位"（表示 si 不晚于 si+1）或"错位"（表示 si 严格晚于 si+1）。

每次询问只能包含一个标签，使用以下 XML 格式：

- 比较查询（例如询问动作 A 和 B 的先后关系）：
<query_compare>A,B</query_compare>

- 相邻检查（例如检查位置 1 和 2，即索引为 1）：
<query_adjacent>1</query_adjacent>

提交最终答案时，必须说明判断结果（合规或不合规）并提供证明，格式如下：

- 若判断为合规，必须给出所有出现动作的完整先后链（用逗号隔开，从早到晚）：
<answer>status=合规, order=A,B,C</answer>

- 若判断为不合规，必须给出一个证据位置对 i,j（i < j）或单个相邻位置 i，证明存在逆序：
<answer>status=不合规, evidence=2,5</answer>
或
<answer>status=不合规, evidence=3</answer>

注意：
- 如果你声明"合规"，我会检查你提供的动作顺序是否与我的隐藏顺序一致，以及序列是否真的合规
- 如果你声明"不合规"，我会检查你提供的证据位置是否真的存在逆序
- 答案错误或格式不符，游戏失败
"""

    contextualized_rule_en_5 = """\
[Law Scenario] Judicial Procedural Compliance Review System. You need to verify the statutory procedural compliance of a litigation sequence.

Let's play a "Litigation Sequence Order Verification" deduction game. Here are the rules:

A visible litigation sequence s = (s1, s2, ..., sN) is given, where N = {n}, and each procedural action si belongs to the set {symbol_set}. I have secretly defined a strict total order over all actions (every two different actions have a strict statutory precedence relation, which remains fixed throughout this game).

Define the non-strict relation: action x is "no later than" action y if and only if x equals y, or x is strictly earlier in the statutory timeline than y.

A sequence is "compliant" if: for all adjacent positions i and i+1 (1 <= i < N), si is "no later than" si+1.

Your litigation sequence is: {sequence}

Your goals are:
1. Determine whether the sequence is compliant
2. Submit your judgment with formal justification
3. If judged compliant, also provide the relative order of all distinct actions appearing in this game

You can ask me the following two types of questions (one per turn), and I will answer truthfully based on the hidden statutory order:

1. Comparison Query: Ask about the precedence relation between two different actions a and b (a and b must appear in the sequence, and a ≠ b). I will answer "a before b" or "b before a".

2. Adjacency Check: Ask whether a specific adjacent position pair in the sequence (position i and i+1, where 1 <= i < N) satisfies the "no later than" relation. I will answer "in-place" (meaning si is no later than si+1) or "out-of-place" (meaning si is strictly later than si+1).

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about actions A and B):
<query_compare>A,B</query_compare>

- Adjacency Check (e.g., checking positions 1 and 2, with index 1):
<query_adjacent>1</query_adjacent>

When submitting the final answer, specify the judgment result (compliant or non-compliant) and provide justification in the following format:

- If judged compliant, provide the complete precedence chain of all appearing actions (comma-separated, from earliest to latest):
<answer>status=compliant, order=A,B,C</answer>

- If judged non-compliant, provide evidence as a position pair i,j (i < j) or a single adjacent position i, proving an inversion exists:
<answer>status=non-compliant, evidence=2,5</answer>
or
<answer>status=non-compliant, evidence=3</answer>

Note:
- If you claim "compliant", I will verify whether your provided action order matches my hidden order and whether the sequence is truly compliant
- If you claim "non-compliant", I will verify whether your provided evidence position truly has an inversion
- Incorrect answers or invalid formats will result in game failure
"""

    tags = ["answer", "query_compare", "query_adjacent"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 3,
                "sequence": ["A", "B", "C"],
                "hidden_order": ["A", "B", "C"],
                "is_compliant": True,
            },
            2: {
                "n": 4,
                "sequence": ["A", "C", "B", "D"],
                "hidden_order": ["A", "B", "C", "D"],
                "is_compliant": False,
            },
            3: {
                "n": 5,
                "sequence": ["A", "A", "B", "C", "C"],
                "hidden_order": ["A", "B", "C", "D"],
                "is_compliant": True,
            },
            4: {
                "n": 6,
                "sequence": ["A", "B", "C", "D", "C", "E"],
                "hidden_order": ["A", "B", "C", "D", "E"],
                "is_compliant": False,
            },
            5: {
                "n": 7,
                "sequence": ["A", "A", "B", "C", "C", "D", "E"],
                "hidden_order": ["A", "B", "C", "D", "E"],
                "is_compliant": True,
            },
        },
        "en": {
            1: {
                "n": 3,
                "sequence": ["A", "B", "C"],
                "hidden_order": ["A", "B", "C"],
                "is_compliant": True,
            },
            2: {
                "n": 4,
                "sequence": ["A", "C", "B", "D"],
                "hidden_order": ["A", "B", "C", "D"],
                "is_compliant": False,
            },
            3: {
                "n": 5,
                "sequence": ["A", "A", "B", "C", "C"],
                "hidden_order": ["A", "B", "C", "D"],
                "is_compliant": True,
            },
            4: {
                "n": 6,
                "sequence": ["A", "B", "C", "D", "C", "E"],
                "hidden_order": ["A", "B", "C", "D", "E"],
                "is_compliant": False,
            },
            5: {
                "n": 7,
                "sequence": ["A", "A", "B", "C", "C", "D", "E"],
                "hidden_order": ["A", "B", "C", "D", "E"],
                "is_compliant": True,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self.sequence = cfg["sequence"]
        self.hidden_order = cfg["hidden_order"]
        self.is_compliant = cfg["is_compliant"]
        
        self.order_map = {symbol: idx for idx, symbol in enumerate(self.hidden_order)}
        
        self.appearing_symbols = sorted(set(self.sequence))
        
        self._game_info["sequence"] = ", ".join(self.sequence)
        self._game_info["symbol_set"] = "{" + ", ".join(sorted(set(self.sequence))) + "}"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            before_text = "{} 早于 {}"
            in_place_text = "就位"
            out_of_place_text = "错位"
        else:
            before_text = "{} before {}"
            in_place_text = "in-place"
            out_of_place_text = "out-of-place"

        for i in range(len(self.appearing_symbols)):
            for j in range(i + 1, len(self.appearing_symbols)):
                sym_a = self.appearing_symbols[i]
                sym_b = self.appearing_symbols[j]
                
                query_str = f"<query_compare>{sym_a},{sym_b}</query_compare>"
                
                if self.order_map[sym_a] < self.order_map[sym_b]:
                    ans = before_text.format(sym_a, sym_b)
                else:
                    ans = before_text.format(sym_b, sym_a)
                
                results.append({
                    "query": query_str,
                    "answer": ans
                })

        N = len(self.sequence)
        for idx in range(1, N):
            query_str = f"<query_adjacent>{idx}</query_adjacent>"
            
            internal_idx = idx - 1
            sym_i = self.sequence[internal_idx]
            sym_j = self.sequence[internal_idx + 1]
            
            if sym_i == sym_j:
                ans = in_place_text
            elif self.order_map[sym_i] < self.order_map[sym_j]:
                ans = in_place_text
            else:
                ans = out_of_place_text
            
            results.append({
                "query": query_str,
                "answer": ans
            })
            
        return results

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        ans_dict = {}
        
        status_match = re.search(r'status\s*=\s*([^,]+?)(?:\s*,\s*(?:order|evidence)\s*=|$)', raw_ans)
        if status_match:
            ans_dict["status"] = status_match.group(1).strip()
        
        order_match = re.search(r'order\s*=\s*(.+)$', raw_ans)
        if order_match:
            ans_dict["order"] = order_match.group(1).strip()
        
        evidence_match = re.search(r'evidence\s*=\s*(.+)$', raw_ans)
        if evidence_match:
            ans_dict["evidence"] = evidence_match.group(1).strip()
        
        if "status" not in ans_dict:
            return False
        
        status = ans_dict["status"]
        
        if self.config.language == "zh":
            compliant_keywords = ["合规"]
            non_compliant_keywords = ["不合规"]
        else:
            compliant_keywords = ["compliant"]
            non_compliant_keywords = ["non-compliant", "non_compliant", "noncompliant"]
        
        is_claim_compliant = any(kw in status for kw in compliant_keywords) and \
                            not any(kw in status for kw in non_compliant_keywords)
        
        if is_claim_compliant:
            if not self.is_compliant:
                return False
            
            if "order" not in ans_dict:
                return False
            
            try:
                provided_order = [s.strip() for s in ans_dict["order"].split(",")]
            except:
                return False
            
            provided_set = set(provided_order)
            appearing_set = set(self.appearing_symbols)
            
            if provided_set != appearing_set:
                return False
            
            for i in range(len(provided_order)):
                for j in range(i + 1, len(provided_order)):
                    sym_i, sym_j = provided_order[i], provided_order[j]
                    if sym_i in self.order_map and sym_j in self.order_map:
                        if self.order_map[sym_i] >= self.order_map[sym_j]:
                            return False
            
            return True
        
        else:
            if self.is_compliant:
                return False
            
            if "evidence" not in ans_dict:
                return False
            
            try:
                evidence_parts = [s.strip() for s in ans_dict["evidence"].split(",")]
                
                if len(evidence_parts) == 1:
                    idx = int(evidence_parts[0]) - 1
                    if idx < 0 or idx >= len(self.sequence) - 1:
                        return False
                    
                    sym_i = self.sequence[idx]
                    sym_j = self.sequence[idx + 1]
                    
                    if sym_i == sym_j:
                        return False
                    
                    return self.order_map[sym_i] > self.order_map[sym_j]
                
                elif len(evidence_parts) == 2:
                    pos_i = int(evidence_parts[0]) - 1
                    pos_j = int(evidence_parts[1]) - 1
                    
                    if pos_i < 0 or pos_j < 0 or pos_i >= len(self.sequence) or pos_j >= len(self.sequence):
                        return False
                    
                    if pos_i >= pos_j:
                        return False
                    
                    sym_i = self.sequence[pos_i]
                    sym_j = self.sequence[pos_j]
                    
                    if sym_i == sym_j:
                        return False
                    
                    return self.order_map[sym_i] > self.order_map[sym_j]
                
                else:
                    return False
                    
            except:
                return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            before_text = "{} 早于 {}"
            in_place_text = "就位"
            out_of_place_text = "错位"
            invalid_text = "无效问题"
        else:
            before_text = "{} before {}"
            in_place_text = "in-place"
            out_of_place_text = "out-of-place"
            invalid_text = "invalid query"
        
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 2:
                    return invalid_text
                
                sym_a, sym_b = parts[0], parts[1]
                
                if sym_a == sym_b:
                    return invalid_text
                
                if sym_a not in self.appearing_symbols or sym_b not in self.appearing_symbols:
                    return invalid_text
                
                if sym_a not in self.order_map or sym_b not in self.order_map:
                    return invalid_text
                
                if self.order_map[sym_a] < self.order_map[sym_b]:
                    return before_text.format(sym_a, sym_b)
                else:
                    return before_text.format(sym_b, sym_a)
                    
            except:
                return invalid_text
        
        elif "query_adjacent" in parsed_info:
            try:
                idx_str = parsed_info["query_adjacent"].strip()
                idx = int(idx_str) - 1
                
                if idx < 0 or idx >= len(self.sequence) - 1:
                    return invalid_text
                
                sym_i = self.sequence[idx]
                sym_j = self.sequence[idx + 1]
                
                if sym_i == sym_j:
                    return in_place_text
                
                if self.order_map[sym_i] < self.order_map[sym_j]:
                    return in_place_text
                else:
                    return out_of_place_text
                    
            except:
                return invalid_text
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "错位" in correct:
                return correct.replace("错位", "就位")
            if "就位" in correct:
                return correct.replace("就位", "错位")
            if "早于" in correct:
                match = re.match(r'(.+?)\s*早于\s*(.+)', correct)
                if match:
                    return f"{match.group(2).strip()} 早于 {match.group(1).strip()}"
        else:
            if "out-of-place" in correct:
                return correct.replace("out-of-place", "in-place")
            if "in-place" in correct:
                return correct.replace("in-place", "out-of-place")
            if " before " in correct:
                match = re.match(r'(.+?)\s+before\s+(.+)', correct)
                if match:
                    return f"{match.group(2).strip()} before {match.group(1).strip()}"

        return correct + "_WRONG"