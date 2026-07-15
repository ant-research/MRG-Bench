from .base import Game
import re
import random
from typing import List, Dict

class PeriodicPatternDiscoveryGame(Game):

    game_rule_zh = """\
我们现在来玩一个"周期基块识别"的推理游戏，规则如下：

游戏设定了一个字母表，包含四个符号：A、B、C、D。

存在一个未知的原始序列 M，其长度 P 在 2 到 6 之间，且 M 是原始的（不是更短序列的重复）。观测序列 S 由 M 重复 T 次（T 大于等于 3）串联而成，即 S = M 重复 T 次。S 的总长度 N 等于 P 乘以 T。S 的第 1 个位置与 M 的第 1 个位置对齐。

你不知道 P、N 或 M 的内容。

定义 pos(X, k) 为序列 S 中从左到右第 k 次出现符号 X 的位置索引（位置从 1 开始计数）。

你的目标是通过提问推断出原始序列 M 的完整内容（包括长度和符号序列）。你需要尽可能少的提问次数来完成任务。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **存在性查询**：询问符号 X 的第 k 次出现是否存在。
   - 我会回答"是"或"否"。

2. **距离查询**：从符号 X 的第 k 次出现向右，最近的符号 Y 与它之间相隔多少个位置？
   - 若 pos(X, k) 不存在，我会回答"无第 k 次 X"。
   - 若存在但右侧无任何 Y，我会回答"右侧无 Y"。
   - 否则，我会回答一个非负整数 d（表示中间间隔的位置数，相邻则 d = 0）。

每次提问只能包含一个标签。请使用以下 XML 格式：

- 存在性查询（例如询问符号 A 的第 3 次出现是否存在）：
<query_exist>A,3</query_exist>

- 距离查询（例如询问从符号 A 的第 2 次出现向右，最近的符号 B 与它之间相隔多少个位置）：
<query_distance>A,2,B</query_distance>

当你准备好提交最终答案时，请按以下格式提交原始序列 M：

<answer>ABC</answer>

注意：答案必须是由字母表中的符号组成的字符串，不含空格或其他字符。
"""

    game_rule_en = """\
Let's play a "Periodic Pattern Discovery" deduction game. Here are the rules:

The game defines an alphabet containing four symbols: A, B, C, D.

There exists an unknown primitive sequence M with length P between 2 and 6, and M is primitive (not a repetition of a shorter sequence). The observation sequence S is formed by concatenating M repeated T times (T is greater than or equal to 3), i.e., S = M repeated T times. The total length of S, N, equals P times T. The first position of S aligns with the first position of M.

You do not know P, N, or the content of M.

Define pos(X, k) as the position index (1-indexed) of the k-th occurrence of symbol X in sequence S from left to right.

Your goal is to infer the complete content of the primitive sequence M (including its length and symbol sequence) through queries. You should use as few queries as possible to accomplish the task.

You can repeatedly ask me the following two types of questions (one question per turn):

1. **Existence Query**: Ask whether the k-th occurrence of symbol X exists.
   - I will answer "Yes" or "No".

2. **Distance Query**: From the k-th occurrence of symbol X to the right, how many positions are there between it and the nearest symbol Y?
   - If pos(X, k) does not exist, I will answer "No k-th X".
   - If it exists but there is no Y to its right, I will answer "No Y on right".
   - Otherwise, I will answer a non-negative integer d (representing the number of positions in between; d = 0 if adjacent).

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., asking if the 3rd occurrence of symbol A exists):
<query_exist>A,3</query_exist>

- Distance Query (e.g., asking the distance from the 2nd occurrence of symbol A to the nearest symbol B on the right):
<query_distance>A,2,B</query_distance>

When you are ready to submit your final answer, submit the primitive sequence M in the following format:

<answer>ABC</answer>

Note: The answer must be a string composed of symbols from the alphabet, without spaces or other characters.
"""

    contextualized_rule_zh_1 = """\
我们在进行“智能交通信号调度周期识别”的推理游戏，规则如下：

游戏设定了一个交通信号系统，包含四个相位：A、B、C、D。

存在一个未知的核心调度周期序列 M，其长度 P 在 2 到 6 之间，且 M 是最简周期（不可由更短序列的重复构成）。观测到的全天调度日志 S 由 M 重复 T 次（T 大于等于 3）串联而成，即 S = M 重复 T 次。S 的总长度 N 等于 P 乘以 T。S 的第 1 个记录与 M 的第 1 个位置对齐。

你不知道 P、N 或 M 的内容。

定义 pos(X, k) 为日志 S 中从左到右第 k 次出现相位 X 的位置索引（位置从 1 开始计数）。

你的目标是通过提问推断出核心调度周期 M 的完整内容（包括长度和相位序列）。你需要尽可能少的提问次数来完成任务。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **存在性查询**：询问相位 X 的第 k 次出现是否存在。
   - 我会回答“是”或“否”。

2. **距离查询**：从相位 X 的第 k 次出现向右，最近的相位 Y 与它之间相隔几个调度位？
   - 若 pos(X, k) 不存在，我会回答“无第 k 次 X”。
   - 若存在但右侧无任何 Y，我会回答“右侧无 Y”。
   - 否则，我会回答一个非负整数 d（表示中间间隔的调度位数，相邻则 d = 0）。

每次提问只能包含一个标签。请使用以下 XML 格式：

- 存在性查询（例如询问相位 A 的第 3 次出现是否存在）：
<query_exist>A,3</query_exist>

- 距离查询（例如询问从相位 A 的第 2 次出现向右，最近的相位 B 与它之间相隔几个调度位）：
<query_distance>A,2,B</query_distance>

当你准备好提交最终答案时，请按以下格式提交核心调度周期 M：

<answer>ABC</answer>

注意：答案必须是由系统设定的相位代号组成的字符串，不含空格或其他字符。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play an "Intelligent Traffic Signal Dispatch Cycle Recognition" deduction game. Here are the rules:

The game defines a traffic signal system containing four phases: A, B, C, D.

There exists an unknown core dispatch cycle sequence M with length P between 2 and 6, and M is primitive (not a repetition of a shorter sequence). The observed daily dispatch log S is formed by concatenating M repeated T times (T is greater than or equal to 3), i.e., S = M repeated T times. The total length of S, N, equals P times T. The first position of S aligns with the first position of M.

You do not know P, N, or the content of M.

Define pos(X, k) as the position index (1-indexed) of the k-th occurrence of phase X in log S from left to right.

Your goal is to infer the complete content of the core dispatch cycle M (including its length and phase sequence) through queries. You should use as few queries as possible to accomplish the task.

You can repeatedly ask me the following two types of questions (one question per turn):

1. **Existence Query**: Ask whether the k-th occurrence of phase X exists.
   - I will answer "Yes" or "No".

2. **Distance Query**: From the k-th occurrence of phase X to the right, how many dispatch slots are there between it and the nearest phase Y?
   - If pos(X, k) does not exist, I will answer "No k-th X".
   - If it exists but there is no Y to its right, I will answer "No Y on right".
   - Otherwise, I will answer a non-negative integer d (representing the number of slots in between; d = 0 if adjacent).

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., asking if the 3rd occurrence of phase A exists):
<query_exist>A,3</query_exist>

- Distance Query (e.g., asking the distance from the 2nd occurrence of phase A to the nearest phase B on the right):
<query_distance>A,2,B</query_distance>

When you are ready to submit your final answer, submit the core dispatch cycle M in the following format:

<answer>ABC</answer>

Note: The answer must be a string composed of phase codes from the system, without spaces or other characters.
"""

    contextualized_rule_zh_2 = """\
我们在进行“患者用药周期节律识别”的推理游戏，规则如下：

临床设定了四类靶向药物代号：A、B、C、D。

存在一个未知的核心用药循环序列 M，其长度 P 在 2 到 6 之间，且 M 是原始循环（不可由更短序列的重复构成）。患者的完整给药记录 S 由 M 重复 T 次（T 大于等于 3）串联而成，即 S = M 重复 T 次。S 的总长度 N 等于 P 乘以 T。S 的第 1 次给药与 M 的第 1 个位置对齐。

你不知道 P、N 或 M 的内容。

定义 pos(X, k) 为记录 S 中从左到右第 k 次给予药物 X 的给药顺位序号（顺位从 1 开始计数）。

你的目标是通过提问推断出核心用药循环序列 M 的完整内容（包括长度和药物序列）。你需要尽可能少的提问次数来完成任务。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **存在性查询**：询问药物 X 的第 k 次给予是否存在。
   - 我会回答“是”或“否”。

2. **距离查询**：从药物 X 的第 k 次给予向右，最近的药物 Y 与它之间相隔几次给药？
   - 若 pos(X, k) 不存在，我会回答“无第 k 次 X”。
   - 若存在但右侧无任何 Y，我会回答“右侧无 Y”。
   - 否则，我会回答一个非负整数 d（表示中间间隔的给药次数，相邻则 d = 0）。

每次提问只能包含一个标签。请使用以下 XML 格式：

- 存在性查询（例如询问药物 A 的第 3 次给予是否存在）：
<query_exist>A,3</query_exist>

- 距离查询（例如询问从药物 A 的第 2 次给予向右，最近的药物 B 与它之间相隔几次给药）：
<query_distance>A,2,B</query_distance>

当你准备好提交最终答案时，请按以下格式提交核心用药循环 M：

<answer>ABC</answer>

注意：答案必须是由设定的药物代号组成的字符串，不含空格或其他字符。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Patient Medication Cycle Rhythm Recognition" deduction game. Here are the rules:

The clinic defines four targeted drug codes: A, B, C, D.

There exists an unknown core medication cycle sequence M with length P between 2 and 6, and M is primitive (not a repetition of a shorter sequence). The patient's complete medication record S is formed by concatenating M repeated T times (T is greater than or equal to 3), i.e., S = M repeated T times. The total length of S, N, equals P times T. The first medication of S aligns with the first position of M.

You do not know P, N, or the content of M.

Define pos(X, k) as the position index (1-indexed) of the k-th administration of drug X in record S from left to right.

Your goal is to infer the complete content of the core medication cycle M (including its length and drug sequence) through queries. You should use as few queries as possible to accomplish the task.

You can repeatedly ask me the following two types of questions (one question per turn):

1. **Existence Query**: Ask whether the k-th administration of drug X exists.
   - I will answer "Yes" or "No".

2. **Distance Query**: From the k-th administration of drug X to the right, how many medication intervals are there between it and the nearest drug Y?
   - If pos(X, k) does not exist, I will answer "No k-th X".
   - If it exists but there is no Y to its right, I will answer "No Y on right".
   - Otherwise, I will answer a non-negative integer d (representing the number of intervals in between; d = 0 if adjacent).

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., asking if the 3rd administration of drug A exists):
<query_exist>A,3</query_exist>

- Distance Query (e.g., asking the distance from the 2nd administration of drug A to the nearest drug B on the right):
<query_distance>A,2,B</query_distance>

When you are ready to submit your final answer, submit the core medication cycle M in the following format:

<answer>ABC</answer>

Note: The answer must be a string composed of the defined drug codes, without spaces or other characters.
"""

    contextualized_rule_zh_3 = """\
我们在进行“标准化教学模块周期识别”的推理游戏，规则如下：

课程库设定了四种教学模块：A、B、C、D。

存在一个未知的核心教学计划序列 M，其长度 P 在 2 到 6 之间，且 M 是基础计划（不可由更短序列的重复构成）。观测到的学期总课表 S 由 M 重复 T 次（T 大于等于 3）串联而成，即 S = M 重复 T 次。S 的总长度 N 等于 P 乘以 T。S 的第 1 个课时与 M 的第 1 个位置对齐。

你不知道 P、N 或 M 的内容。

定义 pos(X, k) 为总课表 S 中从左到右第 k 次教授模块 X 的课时序号（序号从 1 开始计数）。

你的目标是通过提问推断出核心教学计划 M 的完整内容（包括长度和模块序列）。你需要尽可能少的提问次数来完成任务。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **存在性查询**：询问模块 X 的第 k 次教授是否存在。
   - 我会回答“是”或“否”。

2. **距离查询**：从模块 X 的第 k 次教授向右，最近的模块 Y 与它之间相隔几个课时？
   - 若 pos(X, k) 不存在，我会回答“无第 k 次 X”。
   - 若存在但右侧无任何 Y，我会回答“右侧无 Y”。
   - 否则，我会回答一个非负整数 d（表示中间间隔的课时数，相邻则 d = 0）。

每次提问只能包含一个标签。请使用以下 XML 格式：

- 存在性查询（例如询问模块 A 的第 3 次教授是否存在）：
<query_exist>A,3</query_exist>

- 距离查询（例如询问从模块 A 的第 2 次教授向右，最近的模块 B 与它之间相隔几个课时）：
<query_distance>A,2,B</query_distance>

当你准备好提交最终答案时，请按以下格式提交核心教学计划 M：

<answer>ABC</answer>

注意：答案必须是由设定的模块代号组成的字符串，不含空格或其他字符。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Standardized Teaching Module Cycle Recognition" deduction game. Here are the rules:

The curriculum library defines four teaching modules: A, B, C, D.

There exists an unknown core teaching plan sequence M with length P between 2 and 6, and M is foundational (not a repetition of a shorter sequence). The observed full semester syllabus S is formed by concatenating M repeated T times (T is greater than or equal to 3), i.e., S = M repeated T times. The total length of S, N, equals P times T. The first slot of S aligns with the first position of M.

You do not know P, N, or the content of M.

Define pos(X, k) as the position index (1-indexed) of the k-th session of module X in the syllabus S from left to right.

Your goal is to infer the complete content of the core teaching plan M (including its length and module sequence) through queries. You should use as few queries as possible to accomplish the task.

You can repeatedly ask me the following two types of questions (one question per turn):

1. **Existence Query**: Ask whether the k-th session of module X exists.
   - I will answer "Yes" or "No".

2. **Distance Query**: From the k-th session of module X to the right, how many teaching slots are there between it and the nearest module Y?
   - If pos(X, k) does not exist, I will answer "No k-th X".
   - If it exists but there is no Y to its right, I will answer "No Y on right".
   - Otherwise, I will answer a non-negative integer d (representing the number of slots in between; d = 0 if adjacent).

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., asking if the 3rd session of module A exists):
<query_exist>A,3</query_exist>

- Distance Query (e.g., asking the distance from the 2nd session of module A to the nearest module B on the right):
<query_distance>A,2,B</query_distance>

When you are ready to submit your final answer, submit the core teaching plan M in the following format:

<answer>ABC</answer>

Note: The answer must be a string composed of the defined module codes, without spaces or other characters.
"""

    contextualized_rule_zh_4 = """\
我们在进行“柔性流水线生产节拍识别”的推理游戏，规则如下：

产线上设定了四类加工作业：A、B、C、D。

存在一个未知的标准生产批次序列 M，其长度 P 在 2 到 6 之间，且 M 是最小工艺循环（不可由更短序列的重复构成）。观测到的连续排产序列 S 由 M 重复 T 次（T 大于等于 3）串联而成，即 S = M 重复 T 次。S 的总长度 N 等于 P 乘以 T。S 的第 1 个加工作业与 M 的第 1 个位置对齐。

你不知道 P、N 或 M 的内容。

定义 pos(X, k) 为排产序列 S 中从左到右第 k 次执行作业 X 的工位序号（序号从 1 开始计数）。

你的目标是通过提问推断出标准生产批次序列 M 的完整内容（包括长度和作业序列）。你需要尽可能少的提问次数来完成任务。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **存在性查询**：询问作业 X 的第 k 次执行是否存在。
   - 我会回答“是”或“否”。

2. **距离查询**：从作业 X 的第 k 次执行向右，最近的作业 Y 与它之间相隔几个工位？
   - 若 pos(X, k) 不存在，我会回答“无第 k 次 X”。
   - 若存在但右侧无任何 Y，我会回答“右侧无 Y”。
   - 否则，我会回答一个非负整数 d（表示中间间隔的工位数，相邻则 d = 0）。

每次提问只能包含一个标签。请使用以下 XML 格式：

- 存在性查询（例如询问作业 A 的第 3 次执行是否存在）：
<query_exist>A,3</query_exist>

- 距离查询（例如询问从作业 A 的第 2 次执行向右，最近的作业 B 与它之间相隔几个工位）：
<query_distance>A,2,B</query_distance>

当你准备好提交最终答案时，请按以下格式提交标准生产批次 M：

<answer>ABC</answer>

注意：答案必须是由设定的作业代号组成的字符串，不含空格或其他字符。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's play a "Flexible Assembly Line Production Takt Recognition" deduction game. Here are the rules:

The assembly line defines four types of operations: A, B, C, D.

There exists an unknown standard production batch sequence M with length P between 2 and 6, and M is the minimal process cycle (not a repetition of a shorter sequence). The observed continuous production sequence S is formed by concatenating M repeated T times (T is greater than or equal to 3), i.e., S = M repeated T times. The total length of S, N, equals P times T. The first operation of S aligns with the first position of M.

You do not know P, N, or the content of M.

Define pos(X, k) as the position index (1-indexed) of the k-th execution of operation X in the sequence S from left to right.

Your goal is to infer the complete content of the standard production batch sequence M (including its length and operation sequence) through queries. You should use as few queries as possible to accomplish the task.

You can repeatedly ask me the following two types of questions (one question per turn):

1. **Existence Query**: Ask whether the k-th execution of operation X exists.
   - I will answer "Yes" or "No".

2. **Distance Query**: From the k-th execution of operation X to the right, how many operational steps are there between it and the nearest operation Y?
   - If pos(X, k) does not exist, I will answer "No k-th X".
   - If it exists but there is no Y to its right, I will answer "No Y on right".
   - Otherwise, I will answer a non-negative integer d (representing the number of operational steps in between; d = 0 if adjacent).

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., asking if the 3rd execution of operation A exists):
<query_exist>A,3</query_exist>

- Distance Query (e.g., asking the distance from the 2nd execution of operation A to the nearest operation B on the right):
<query_distance>A,2,B</query_distance>

When you are ready to submit your final answer, submit the standard production batch sequence M in the following format:

<answer>ABC</answer>

Note: The answer must be a string composed of the defined operation codes, without spaces or other characters.
"""

    contextualized_rule_zh_5 = """\
我们在进行“合规审计程序周期识别”的推理游戏，规则如下：

审计流程设定了四类审查项：A、B、C、D。

存在一个未知的核心审计循环序列 M，其长度 P 在 2 到 6 之间，且 M 是最简循环（不可由更短序列的重复构成）。观测到的总审计流水 S 由 M 重复 T 次（T 大于等于 3）串联而成，即 S = M 重复 T 次。S 的总长度 N 等于 P 乘以 T。S 的第 1 个动作与 M 的第 1 个位置对齐。

你不知道 P、N 或 M 的内容。

定义 pos(X, k) 为审计流水 S 中从左到右第 k 次执行审查项 X 的次序索引（次序从 1 开始计数）。

你的目标是通过提问推断出核心审计循环 M 的完整内容（包括长度和审查项序列）。你需要尽可能少的提问次数来完成任务。

你可以反复向我提出以下两类问题（每次仅限一个问题）：

1. **存在性查询**：询问审查项 X 的第 k 次执行是否存在。
   - 我会回答“是”或“否”。

2. **距离查询**：从审查项 X 的第 k 次执行向右，最近的审查项 Y 与它之间相隔几个审计步？
   - 若 pos(X, k) 不存在，我会回答“无第 k 次 X”。
   - 若存在但右侧无任何 Y，我会回答“右侧无 Y”。
   - 否则，我会回答一个非负整数 d（表示中间间隔的审计步数，相邻则 d = 0）。

每次提问只能包含一个标签。请使用以下 XML 格式：

- 存在性查询（例如询问审查项 A 的第 3 次执行是否存在）：
<query_exist>A,3</query_exist>

- 距离查询（例如询问从审查项 A 的第 2 次执行向右，最近的审查项 B 与它之间相隔几个审计步）：
<query_distance>A,2,B</query_distance>

当你准备好提交最终答案时，请按以下格式提交核心审计循环 M：

<answer>ABC</answer>

注意：答案必须是由设定的审查项代号组成的字符串，不含空格或其他字符。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Compliance Audit Procedure Cycle Recognition" deduction game. Here are the rules:

The audit workflow defines four types of items: A, B, C, D.

There exists an unknown core audit cycle sequence M with length P between 2 and 6, and M is the minimal cycle (not a repetition of a shorter sequence). The observed total audit log S is formed by concatenating M repeated T times (T is greater than or equal to 3), i.e., S = M repeated T times. The total length of S, N, equals P times T. The first action of S aligns with the first position of M.

You do not know P, N, or the content of M.

Define pos(X, k) as the position index (1-indexed) of the k-th execution of item X in the log S from left to right.

Your goal is to infer the complete content of the core audit cycle sequence M (including its length and item sequence) through queries. You should use as few queries as possible to accomplish the task.

You can repeatedly ask me the following two types of questions (one question per turn):

1. **Existence Query**: Ask whether the k-th execution of item X exists.
   - I will answer "Yes" or "No".

2. **Distance Query**: From the k-th execution of item X to the right, how many audit steps are there between it and the nearest item Y?
   - If pos(X, k) does not exist, I will answer "No k-th X".
   - If it exists but there is no Y to its right, I will answer "No Y on right".
   - Otherwise, I will answer a non-negative integer d (representing the number of audit steps in between; d = 0 if adjacent).

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., asking if the 3rd execution of item A exists):
<query_exist>A,3</query_exist>

- Distance Query (e.g., asking the distance from the 2nd execution of item A to the nearest item B on the right):
<query_distance>A,2,B</query_distance>

When you are ready to submit your final answer, submit the core audit cycle sequence M in the following format:

<answer>ABC</answer>

Note: The answer must be a string composed of the defined item codes, without spaces or other characters.
"""

    tags = ["answer", "query_exist", "query_distance"]

    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"M": "AB", "T": 4},
            2: {"M": "ABC", "T": 4},
            3: {"M": "ABCD", "T": 3},
            4: {"M": "ABCDA", "T": 3},
            5: {"M": "ABCDAB", "T": 3},
        },
        "en": {
            1: {"M": "AB", "T": 4},
            2: {"M": "ABC", "T": 4},
            3: {"M": "ABCD", "T": 3},
            4: {"M": "ABCDA", "T": 3},
            5: {"M": "ABCDAB", "T": 3},
        },
    }

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        base_letters = ["A", "B", "C", "D"]
        random.shuffle(base_letters)
        base_str = "".join(base_letters)
        
        if diff == 1:
            self.M = base_str[:2]
        elif diff == 2:
            self.M = base_str[:3]
        elif diff == 3:
            self.M = base_str[:4]
        elif diff == 4:
            self.M = base_str[:4] + base_str[:1]
        elif diff == 5:
            self.M = base_str[:4] + base_str[:2]
        else:
            self.M = cfg["M"]
            
        self.T = cfg["T"]
        self.P = len(self.M)
        self.S = self.M * self.T
        self.N = len(self.S)

        self.symbol_positions = {}
        for symbol in "ABCD":
            positions = []
            for i, char in enumerate(self.S, start=1):
                if char == symbol:
                    positions.append(i)
            self.symbol_positions[symbol] = positions

        self._game_info = {}

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip().upper()
        
        if not all(c in "ABCD" for c in raw_ans):
            return False
        
        return raw_ans == self.M

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            no_kth_x = "无第 {k} 次 {X}"
            no_y_right = "右侧无 {Y}"
        else:
            yes_res, no_res = "Yes", "No"
            no_kth_x = "No {k}-th {X}"
            no_y_right = "No {Y} on right"

        if "query_exist" in parsed_info:
            try:
                raw = parsed_info["query_exist"].strip()
                parts = [x.strip().upper() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                X, k_str = parts
                k = int(k_str)
                
                if X not in ("A", "B", "C", "D") or k < 1:
                    raise ValueError
                
                positions = self.symbol_positions.get(X, [])
                if k <= len(positions):
                    return yes_res
                else:
                    return no_res
            except:
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"

        elif "query_distance" in parsed_info:
            try:
                raw = parsed_info["query_distance"].strip()
                parts = [x.strip().upper() for x in raw.split(",")]
                if len(parts) != 3:
                    raise ValueError
                X, k_str, Y = parts
                k = int(k_str)
                
                if X not in ("A", "B", "C", "D") or Y not in ("A", "B", "C", "D") or k < 1:
                    raise ValueError
                
                x_positions = self.symbol_positions.get(X, [])
                if k > len(x_positions):
                    return no_kth_x.format(k=k, X=X)
                
                pos_x = x_positions[k - 1]
                
                y_positions = self.symbol_positions.get(Y, [])
                right_y_positions = [p for p in y_positions if p > pos_x]
                
                if not right_y_positions:
                    return no_y_right.format(Y=Y)
                
                nearest_y = min(right_y_positions)
                distance = nearest_y - pos_x - 1
                
                return str(distance)
            except:
                return "Error: Invalid format." if self.config.language == "en" else "错误：格式无效。"

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.lstrip('-').isdigit():
            val = int(correct)
            return str(val + 1) if val >= 0 else str(val - 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        low_correct = correct.lower()
        if low_correct == "yes":
            if correct.istitle(): return "No"
            if correct.isupper(): return "NO"
            return "no"
        if low_correct == "no":
            if correct.istitle(): return "Yes"
            if correct.isupper(): return "YES"
            return "yes"

        if self.config.language == "zh":
            if correct.startswith("无第"):
                return "是"
            if correct.startswith("右侧无"):
                return "0"
        else:
            if correct.startswith("No ") and "-th" in correct:
                return "Yes"
            if correct.startswith("No ") and "on right" in correct:
                return "0"

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        queries = []
        lang = self.config.language

        if lang == "zh":
            yes_res, no_res = "是", "否"
            no_y_right = "右侧无 {Y}"
        else:
            yes_res, no_res = "Yes", "No"
            no_y_right = "No {Y} on right"
        
        symbols = ["A", "B", "C", "D"]

        for X in symbols:
            positions = self.symbol_positions.get(X, [])
            max_k = len(positions)
            
            for k in range(1, max_k + 2):
                query_content = f"{X},{k}"
                
                if k <= max_k:
                    ans = yes_res
                else:
                    ans = no_res
                
                queries.append({
                    "query": f"<query_exist>{query_content}</query_exist>",
                    "answer": ans
                })

        for X in symbols:
            x_positions = self.symbol_positions.get(X, [])
            for i, pos_x in enumerate(x_positions):
                k = i + 1
                
                for Y in symbols:
                    query_content = f"{X},{k},{Y}"
                    
                    y_positions = self.symbol_positions.get(Y, [])
                    right_y_positions = [p for p in y_positions if p > pos_x]
                    
                    if not right_y_positions:
                        ans = no_y_right.format(Y=Y)
                    else:
                        nearest_y = min(right_y_positions)
                        distance = nearest_y - pos_x - 1
                        ans = str(distance)
                    
                    queries.append({
                        "query": f"<query_distance>{query_content}</query_distance>",
                        "answer": ans
                    })

        return queries