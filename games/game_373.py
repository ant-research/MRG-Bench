from .base import Game
import re

class PeriodicSequenceGame(Game):

    game_rule_zh = """\
我们来玩一个"周期序列推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的序列 S[1..{n}]，序列中的每个元素都来自字母表 {alphabet}。这个序列具有周期性结构：存在一个基序列 base[1..P]（长度为 P），使得 S[i] = base[((i-1) mod P)+1]，其中 P 是序列的最小周期。序列末尾可能因截断而不完整。周期 P 和基序列 base 的具体内容是未知的。

你的目标是：确定目标元素 t = {target} 在序列 S 中的首次出现位置和最后出现位置。
- 如果 t 出现在序列中，你需要找出：
  - first(t)：t 在 S 中第一次出现的下标
  - last(t)：t 在 S 中最后一次出现的下标
- 如果 t 不出现在序列中，需要声明"t 不存在"。

你可以通过以下两种查询来获取信息（每次查询只能提出一个问题）：

1. 观察查询：询问序列中某个位置 i 的值是什么。我会告诉你 S[i] 的具体值。
2. 比较查询：询问序列中位置 i 和位置 j 的值是否相等。我会回答"是"或"否"。

注意：
- 你最多可以进行 {budget} 次有效查询。
- 查询的位置必须在 1 到 {n} 的范围内，否则查询无效且不计入预算。
- 你需要尽可能少地使用查询次数来推断答案。
- 不允许直接询问"t 在哪里"、"t 出现了几次"等直接泄露答案的问题。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 观察查询（例如询问位置 5 的值）：
<query_value>5</query_value>

- 比较查询（例如询问位置 3 和位置 7 是否相等）：
<query_equal>3,7</query_equal>

提交最终答案时，请使用以下格式：

- 如果 t 出现在序列中（例如首次出现在位置 2，最后出现在位置 8）：
<answer>2,8</answer>

- 如果 t 不出现在序列中：
<answer>0,0</answer>
"""

    game_rule_en = """\
Let's play a "Periodic Sequence Deduction" game. Here are the rules:

The game has set up a sequence S[1..{n}] of length {n}, where each element comes from the alphabet {alphabet}. This sequence has a periodic structure: there exists a base sequence base[1..P] (of length P) such that S[i] = base[((i-1) mod P)+1], where P is the minimum period of the sequence. The end of the sequence may be truncated and incomplete. The period P and the content of base are unknown.

Your goal is: to determine the first and last occurrence positions of the target element t = {target} in sequence S.
- If t appears in the sequence, you need to find:
  - first(t): the index of the first occurrence of t in S
  - last(t): the index of the last occurrence of t in S
- If t does not appear in the sequence, you need to declare "t does not exist".

You can obtain information through the following two types of queries (only one query per turn):

1. Value Query: Ask for the value at position i in the sequence. I will tell you the specific value of S[i].
2. Equality Query: Ask whether the values at positions i and j in the sequence are equal. I will answer "Yes" or "No".

Notes:
- You can make at most {budget} valid queries.
- Query positions must be within the range 1 to {n}, otherwise the query is invalid and does not count toward the budget.
- You need to use as few queries as possible to deduce the answer.
- Direct questions like "where is t" or "how many times does t appear" that directly reveal the answer are not allowed.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the value at position 5):
<query_value>5</query_value>

- Equality Query (e.g., asking if positions 3 and 7 are equal):
<query_equal>3,7</query_equal>

When submitting the final answer, use the following format:

- If t appears in the sequence (e.g., first at position 2, last at position 8):
<answer>2,8</answer>

- If t does not appear in the sequence:
<answer>0,0</answer>
"""

    contextualized_rule_zh_1 = """\
你是一名城市轨道交通调度员。系统记录了一段时间内的列车发车车型序列 S[1..{n}]，共 {n} 个班次，车型来自集合 {alphabet}。由于排班规律，该序列具有周期性结构：存在一个基序列 base[1..P]（长度为 P），使得 S[i] = base[((i-1) mod P)+1]，其中 P 是序列的最小周期。序列末尾可能因截断而不完整。排班周期 P 和基序列 base 的具体内容对你隐藏。

你的目标是：确定特定车型 t = {target} 在该排班序列中的首次发车班次和最后发车班次的编号。
- 如果车型 t 出现过，你需要找出：
  - first(t)：t 第一次发车的班次编号
  - last(t)：t 最后一次发车的班次编号
- 如果车型 t 未出现过，需要声明"t 不存在"。

你可以通过以下两种查询来获取排班信息（每次查询只能提出一个问题）：

1. 观察查询：询问第 i 个班次发出的具体车型。我会告诉你该班次的车型代号。
2. 比较查询：询问第 i 个和第 j 个班次的车型是否相同。我会回答"是"或"否"。

注意：
- 你最多可以进行 {budget} 次有效查询。
- 查询的班次编号必须在 1 到 {n} 的范围内，否则查询无效且不计入预算。
- 你需要尽可能少地使用查询次数来推断答案。
- 不允许直接询问"车型 t 安排在哪些班次"等直接泄露答案的问题。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 观察查询（例如询问第 5 个班次的车型）：
<query_value>5</query_value>

- 比较查询（例如询问第 3 和第 7 个班次车型是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，请使用以下格式：

- 如果 t 出现过（例如首次在班次 2，最后在班次 8）：
<answer>2,8</answer>

- 如果 t 未出现过：
<answer>0,0</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic / Transportation Scenario]
You are an urban rail transit dispatcher. The system has recorded a sequence of departing train models S[1..{n}] over a period of time, totaling {n} shifts, with models coming from the set {alphabet}. Due to scheduling rules, this sequence has a periodic structure: there exists a base sequence base[1..P] (of length P) such that S[i] = base[((i-1) mod P)+1], where P is the minimum period. The end of the sequence may be truncated. The scheduling period P and the base sequence are hidden from you.

Your goal is: to determine the shift numbers of the first and last departures of a specific train model t = {target} in this schedule.
- If model t has appeared, you need to find:
  - first(t): the shift number of t's first departure
  - last(t): the shift number of t's last departure
- If model t has never appeared, you need to declare "t does not exist".

You can obtain scheduling information through the following two types of queries (only one query per turn):

1. Value Query: Ask for the specific train model of the i-th shift. I will tell you its model code.
2. Equality Query: Ask whether the models of the i-th and j-th shifts are identical. I will answer "Yes" or "No".

Notes:
- You can make at most {budget} valid queries.
- Query shift numbers must be within the range 1 to {n}, otherwise the query is invalid and does not count toward the budget.
- You need to use as few queries as possible to deduce the answer.
- Direct questions like "which shifts are assigned model t" are not allowed.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the model of shift 5):
<query_value>5</query_value>

- Equality Query (e.g., asking if shifts 3 and 7 have identical models):
<query_equal>3,7</query_equal>

When submitting the final answer, use the following format:

- If t has appeared (e.g., first at shift 2, last at shift 8):
<answer>2,8</answer>

- If t has never appeared:
<answer>0,0</answer>
"""

    contextualized_rule_zh_2 = """\
你是一名临床研究员。病人的生命体征监测设备在 {n} 个连续的采样时间点记录了状态代码序列 S[1..{n}]，状态代码来自集合 {alphabet}。病人的生理节律导致该状态序列具有周期性结构：存在一个基序列 base[1..P]（长度为 P），使得 S[i] = base[((i-1) mod P)+1]，其中 P 是序列的最小周期。序列末尾可能因监测中断而不完整。生理周期 P 和基序列的具体内容是未知的。

你的目标是：确定危险状态代码 t = {target} 在该监测序列中的首次出现和最后出现的时间点编号。
- 如果状态 t 出现过，你需要找出：
  - first(t)：t 第一次出现的时间点编号
  - last(t)：t 最后一次出现的时间点编号
- 如果状态 t 未出现过，需要声明"t 不存在"。

你可以通过以下两种查询来获取生命体征信息（每次查询只能提出一个问题）：

1. 观察查询：询问第 i 个时间点的具体状态代码。我会告诉你该时间点的记录值。
2. 比较查询：询问第 i 个和第 j 个时间点的状态代码是否相同。我会回答"是"或"否"。

注意：
- 你最多可以进行 {budget} 次有效查询。
- 查询的时间点编号必须在 1 到 {n} 的范围内，否则查询无效且不计入预算。
- 你需要尽可能少地使用查询次数来推断答案。
- 不允许直接询问"危险状态 t 在哪些时间点发作"等直接泄露答案的问题。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 观察查询（例如询问时间点 5 的状态）：
<query_value>5</query_value>

- 比较查询（例如询问时间点 3 和 7 的状态是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，请使用以下格式：

- 如果 t 出现过（例如首次在时间点 2，最后在时间点 8）：
<answer>2,8</answer>

- 如果 t 未出现过：
<answer>0,0</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
You are a clinical researcher. A patient's vital signs monitoring device has recorded a sequence of status codes S[1..{n}] over {n} continuous sampling time points, with codes coming from the set {alphabet}. The patient's biorhythm causes this status sequence to have a periodic structure: there exists a base sequence base[1..P] (of length P) such that S[i] = base[((i-1) mod P)+1], where P is the minimum period. The end of the sequence may be truncated due to monitoring interruption. The biological period P and the base sequence are unknown.

Your goal is: to determine the time point numbers of the first and last occurrences of a critical status code t = {target} in this monitoring sequence.
- If status t has appeared, you need to find:
  - first(t): the time point number of t's first occurrence
  - last(t): the time point number of t's last occurrence
- If status t has never appeared, you need to declare "t does not exist".

You can obtain vital signs information through the following two types of queries (only one query per turn):

1. Value Query: Ask for the specific status code at the i-th time point. I will tell you the recorded value.
2. Equality Query: Ask whether the status codes at the i-th and j-th time points are identical. I will answer "Yes" or "No".

Notes:
- You can make at most {budget} valid queries.
- Query time point numbers must be within the range 1 to {n}, otherwise the query is invalid and does not count toward the budget.
- You need to use as few queries as possible to deduce the answer.
- Direct questions like "at which time points did critical status t occur" are not allowed.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the status at time point 5):
<query_value>5</query_value>

- Equality Query (e.g., asking if time points 3 and 7 have identical statuses):
<query_equal>3,7</query_equal>

When submitting the final answer, use the following format:

- If t has appeared (e.g., first at time point 2, last at time point 8):
<answer>2,8</answer>

- If t has never appeared:
<answer>0,0</answer>
"""

    contextualized_rule_zh_3 = """\
你是一名教务系统分析师。学校的排课系统生成了一段包含 {n} 个教学日的课程表序列 S[1..{n}]，每天安排的课程类型来自集合 {alphabet}。排课算法按照固定的教学循环安排课程，使得序列具有周期性结构：存在一个基序列 base[1..P]（长度为 P），使得 S[i] = base[((i-1) mod P)+1]，其中 P 是序列的最小周期。序列末尾可能因学期结束而不完整。排课周期 P 和基序列的具体内容是未知的。

你的目标是：确定核心课程 t = {target} 在这段课程表中的首次出现和最后出现的教学日编号。
- 如果课程 t 被安排过，你需要找出：
  - first(t)：t 第一次被安排的教学日编号
  - last(t)：t 最后一次被安排的教学日编号
- 如果课程 t 未被安排，需要声明"t 不存在"。

你可以通过以下两种查询来获取课表信息（每次查询只能提出一个问题）：

1. 观察查询：询问第 i 个教学日安排的具体课程类型。我会告诉你该日的排课代码。
2. 比较查询：询问第 i 个和第 j 个教学日安排的课程类型是否相同。我会回答"是"或"否"。

注意：
- 你最多可以进行 {budget} 次有效查询。
- 查询的教学日编号必须在 1 到 {n} 的范围内，否则查询无效且不计入预算。
- 你需要尽可能少地使用查询次数来推断答案。
- 不允许直接询问"核心课程 t 排在哪些天"等直接泄露答案的问题。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 观察查询（例如询问第 5 天的课程）：
<query_value>5</query_value>

- 比较查询（例如询问第 3 天和第 7 天课程是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，请使用以下格式：

- 如果 t 被安排过（例如首次在第 2 天，最后在第 8 天）：
<answer>2,8</answer>

- 如果 t 未被安排：
<answer>0,0</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
You are an academic system analyst. The school's scheduling system has generated a course schedule sequence S[1..{n}] covering {n} teaching days, where the course type scheduled each day comes from the set {alphabet}. The scheduling algorithm assigns courses in a fixed teaching cycle, creating a periodic structure: there exists a base sequence base[1..P] (of length P) such that S[i] = base[((i-1) mod P)+1], where P is the minimum period. The end of the sequence may be truncated due to the end of the semester. The scheduling period P and the base sequence are unknown.

Your goal is: to determine the teaching day numbers of the first and last occurrences of a core course t = {target} in this schedule.
- If course t is scheduled, you need to find:
  - first(t): the teaching day number of t's first occurrence
  - last(t): the teaching day number of t's last occurrence
- If course t is not scheduled, you need to declare "t does not exist".

You can obtain scheduling information through the following two types of queries (only one query per turn):

1. Value Query: Ask for the specific course type scheduled on the i-th teaching day. I will tell you the schedule code.
2. Equality Query: Ask whether the courses scheduled on the i-th and j-th teaching days are identical. I will answer "Yes" or "No".

Notes:
- You can make at most {budget} valid queries.
- Query day numbers must be within the range 1 to {n}, otherwise the query is invalid and does not count toward the budget.
- You need to use as few queries as possible to deduce the answer.
- Direct questions like "on which days is core course t scheduled" are not allowed.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the course on day 5):
<query_value>5</query_value>

- Equality Query (e.g., asking if days 3 and 7 have identical courses):
<query_equal>3,7</query_equal>

When submitting the final answer, use the following format:

- If t is scheduled (e.g., first on day 2, last on day 8):
<answer>2,8</answer>

- If t is not scheduled:
<answer>0,0</answer>
"""

    contextualized_rule_zh_4 = """\
你是一名工业自动化质检工程师。一条自动化流水线连续生产了 {n} 个产品批次，形成序列 S[1..{n}]，每个批次使用的原材料配方代号来自集合 {alphabet}。由于自动化程序的循环执行设置，配方序列具有周期性结构：存在一个基序列 base[1..P]（长度为 P），使得 S[i] = base[((i-1) mod P)+1]，其中 P 是序列的最小周期。序列末尾可能因生产中断而不完整。生产周期 P 和基序列的具体内容是未知的。

你的目标是：查明关键配方 t = {target} 首次被使用的批次编号和最后一次被使用的批次编号。
- 如果配方 t 被使用过，你需要找出：
  - first(t)：t 第一次被使用的批次编号
  - last(t)：t 最后一次被使用的批次编号
- 如果配方 t 未被使用过，需要声明"t 不存在"。

你可以通过以下两种查询来获取生产线信息（每次查询只能提出一个问题）：

1. 观察查询：询问第 i 个批次使用的具体配方代号。我会告诉你该批次的配方记录。
2. 比较查询：询问第 i 个和第 j 个批次使用的配方代号是否相同。我会回答"是"或"否"。

注意：
- 你最多可以进行 {budget} 次有效查询。
- 查询的批次编号必须在 1 到 {n} 的范围内，否则查询无效且不计入预算。
- 你需要尽可能少地使用查询次数来推断答案。
- 不允许直接询问"关键配方 t 用于哪些批次"等直接泄露答案的问题。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 观察查询（例如询问第 5 个批次的配方）：
<query_value>5</query_value>

- 比较查询（例如询问第 3 个和第 7 个批次的配方是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，请使用以下格式：

- 如果 t 被使用过（例如首次在批次 2，最后在批次 8）：
<answer>2,8</answer>

- 如果 t 未被使用过：
<answer>0,0</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industrial Scenario]
You are an industrial automation quality inspection engineer. An automated assembly line has continuously produced {n} product batches, forming a sequence S[1..{n}], where the raw material recipe code used for each batch comes from the set {alphabet}. Due to the cyclic execution of the automation program, the recipe sequence has a periodic structure: there exists a base sequence base[1..P] (of length P) such that S[i] = base[((i-1) mod P)+1], where P is the minimum period. The end of the sequence may be truncated due to production interruption. The production cycle P and the base sequence are unknown.

Your goal is: to ascertain the batch numbers of the first and last times a critical recipe t = {target} was used.
- If recipe t was used, you need to find:
  - first(t): the batch number of t's first use
  - last(t): the batch number of t's last use
- If recipe t was never used, you need to declare "t does not exist".

You can obtain production line information through the following two types of queries (only one query per turn):

1. Value Query: Ask for the specific recipe code used in the i-th batch. I will tell you the recipe record for that batch.
2. Equality Query: Ask whether the recipe codes used in the i-th and j-th batches are identical. I will answer "Yes" or "No".

Notes:
- You can make at most {budget} valid queries.
- Query batch numbers must be within the range 1 to {n}, otherwise the query is invalid and does not count toward the budget.
- You need to use as few queries as possible to deduce the answer.
- Direct questions like "which batches used critical recipe t" are not allowed.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the recipe of batch 5):
<query_value>5</query_value>

- Equality Query (e.g., asking if batches 3 and 7 used identical recipes):
<query_equal>3,7</query_equal>

When submitting the final answer, use the following format:

- If t was used (e.g., first in batch 2, last in batch 8):
<answer>2,8</answer>

- If t was never used:
<answer>0,0</answer>
"""

    contextualized_rule_zh_5 = """\
你是一名司法审计员。在调查一家涉嫌违规操作的金融机构时，你查获了一份包含 {n} 条记录的交易操作日志序列 S[1..{n}]，操作类型代码来自集合 {alphabet}。鉴定发现，自动交易机器人遵循固定的算法循环执行操作，导致序列具有周期性结构：存在一个基序列 base[1..P]（长度为 P），使得 S[i] = base[((i-1) mod P)+1]，其中 P 是算法的最小执行周期。序列末尾可能因日志截取而不完整。算法周期 P 和基序列的具体内容是未知的。

你的目标是：定位可疑操作代码 t = {target} 首次和最后一次出现的日志记录编号。
- 如果操作 t 存在于日志中，你需要找出：
  - first(t)：t 第一次出现的日志记录编号
  - last(t)：t 最后一次出现的日志记录编号
- 如果操作 t 不存在于日志中，需要声明"t 不存在"。

你可以通过以下两种查询来获取操作日志信息（每次查询只能提出一个问题）：

1. 观察查询：询问第 i 条日志的具体操作代码。我会告诉你该记录的代码值。
2. 比较查询：询问第 i 条和第 j 条日志的操作代码是否相同。我会回答"是"或"否"。

注意：
- 你最多可以进行 {budget} 次有效查询。
- 查询的日志编号必须在 1 到 {n} 的范围内，否则查询无效且不计入预算。
- 你需要尽可能少地使用查询次数来推断答案。
- 不允许直接询问"可疑操作 t 出现在哪些记录中"等直接泄露答案的问题。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 观察查询（例如询问第 5 条日志的操作）：
<query_value>5</query_value>

- 比较查询（例如询问第 3 条和第 7 条日志的操作是否相同）：
<query_equal>3,7</query_equal>

提交最终答案时，请使用以下格式：

- 如果 t 存在（例如首次在记录 2，最后在记录 8）：
<answer>2,8</answer>

- 如果 t 不存在：
<answer>0,0</answer>
"""

    contextualized_rule_en_5 = """\
[Legal / Compliance Scenario]
You are a judicial auditor. During the investigation of a financial institution suspected of regulatory violations, you seized an operational transaction log sequence S[1..{n}] containing {n} records, with operation type codes coming from the set {alphabet}. Forensic analysis revealed that the automated trading bot executes operations in a fixed algorithmic loop, causing the sequence to have a periodic structure: there exists a base sequence base[1..P] (of length P) such that S[i] = base[((i-1) mod P)+1], where P is the algorithm's minimum execution period. The end of the sequence may be truncated due to log extraction. The algorithm period P and the base sequence are unknown.

Your goal is: to locate the record numbers of the first and last occurrences of a suspicious operation code t = {target} in this log.
- If operation t exists in the log, you need to find:
  - first(t): the record number of t's first occurrence
  - last(t): the record number of t's last occurrence
- If operation t does not exist, you need to declare "t does not exist".

You can obtain log information through the following two types of queries (only one query per turn):

1. Value Query: Ask for the specific operation code of the i-th log record. I will tell you its code value.
2. Equality Query: Ask whether the operation codes of the i-th and j-th log records are identical. I will answer "Yes" or "No".

Notes:
- You can make at most {budget} valid queries.
- Query log record numbers must be within the range 1 to {n}, otherwise the query is invalid and does not count toward the budget.
- You need to use as few queries as possible to deduce the answer.
- Direct questions like "in which records does suspicious operation t appear" are not allowed.

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking for the operation in log record 5):
<query_value>5</query_value>

- Equality Query (e.g., asking if log records 3 and 7 have identical operations):
<query_equal>3,7</query_equal>

When submitting the final answer, use the following format:

- If t exists (e.g., first in record 2, last in record 8):
<answer>2,8</answer>

- If t does not exist:
<answer>0,0</answer>
"""

    tags = ["answer", "query_value", "query_equal"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "alphabet": "{A,B}",
                "budget": 8,
                "period": 3,
                "base": ["A", "B", "A"],
                "target": "B",
            },
            2: {
                "n": 20,
                "alphabet": "{A,B,C}",
                "budget": 12,
                "period": 4,
                "base": ["A", "B", "C", "A"],
                "target": "C",
            },
            3: {
                "n": 30,
                "alphabet": "{A,B,C,D}",
                "budget": 15,
                "period": 5,
                "base": ["A", "B", "C", "D", "A"],
                "target": "D",
            },
            4: {
                "n": 50,
                "alphabet": "{A,B,C,D,E}",
                "budget": 18,
                "period": 7,
                "base": ["A", "B", "C", "D", "E", "B", "A"],
                "target": "B",
            },
            5: {
                "n": 100,
                "alphabet": "{A,B,C,D,E,F}",
                "budget": 22,
                "period": 11,
                "base": ["A", "B", "C", "D", "E", "F", "A", "C", "B", "D", "F"],
                "target": "F",
            },
        },
        "en": {
            1: {
                "n": 12,
                "alphabet": "{A,B}",
                "budget": 8,
                "period": 3,
                "base": ["A", "B", "A"],
                "target": "B",
            },
            2: {
                "n": 20,
                "alphabet": "{A,B,C}",
                "budget": 12,
                "period": 4,
                "base": ["A", "B", "C", "A"],
                "target": "C",
            },
            3: {
                "n": 30,
                "alphabet": "{A,B,C,D}",
                "budget": 15,
                "period": 5,
                "base": ["A", "B", "C", "D", "A"],
                "target": "D",
            },
            4: {
                "n": 50,
                "alphabet": "{A,B,C,D,E}",
                "budget": 18,
                "period": 7,
                "base": ["A", "B", "C", "D", "E", "B", "A"],
                "target": "B",
            },
            5: {
                "n": 100,
                "alphabet": "{A,B,C,D,E,F}",
                "budget": 22,
                "period": 11,
                "base": ["A", "B", "C", "D", "E", "F", "A", "C", "B", "D", "F"],
                "target": "F",
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0
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
        self._game_info["alphabet"] = cfg["alphabet"]
        self._game_info["budget"] = cfg["budget"]
        self._game_info["target"] = cfg["target"]
        
        self.n = cfg["n"]
        self.budget = cfg["budget"]
        self.period = cfg["period"]
        self.base = cfg["base"]
        self.target = cfg["target"]
        
        self.sequence = {}
        for i in range(1, self.n + 1):
            base_idx = ((i - 1) % self.period)
            self.sequence[i] = self.base[base_idx]
        
        self._compute_ground_truth()

    def _compute_ground_truth(self):
        self.first_pos = None
        self.last_pos = None
        
        for i in range(1, self.n + 1):
            if self.sequence[i] == self.target:
                if self.first_pos is None:
                    self.first_pos = i
                self.last_pos = i
        
        if self.first_pos is None:
            self.first_pos = 0
            self.last_pos = 0

    def evaluate(self, parsed_info):
        try:
            raw_ans = parsed_info["answer"].strip()
            parts = [x.strip() for x in raw_ans.split(",")]
            
            if len(parts) != 2:
                return False
            
            first_ans = int(parts[0])
            last_ans = int(parts[1])
            
            return first_ans == self.first_pos and last_ans == self.last_pos
        except:
            return False

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for i in range(1, self.n + 1):
            query_tag = f"<query_value>{i}</query_value>"
            answer = str(self.sequence[i])
            queries.append({
                "query": query_tag,
                "answer": answer
            })

        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                query_tag = f"<query_equal>{i},{j}</query_equal>"
                is_equal = self.sequence[i] == self.sequence[j]
                answer = yes_res if is_equal else no_res
                queries.append({
                    "query": query_tag,
                    "answer": answer
                })
        
        return queries

    def _cf_core_produce(self, parsed_info):
        if self.query_count >= self.budget:
            if self.config.language == "zh":
                raise ValueError(f"已超出查询预算限制（最多 {self.budget} 次查询）")
            else:
                raise ValueError(f"Query budget exceeded (max {self.budget} queries)")
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_range = "错误：位置超出范围（必须在 1 到 {} 之间）"
            error_format = "错误：查询格式无效"
        else:
            yes_res, no_res = "Yes", "No"
            error_range = "Error: Position out of range (must be between 1 and {})"
            error_format = "Error: Invalid query format"
        
        if "query_value" in parsed_info:
            try:
                pos = int(parsed_info["query_value"].strip())
                if pos < 1 or pos > self.n:
                    return error_range.format(self.n)
                
                self.query_count += 1
                return self.sequence[pos]
            except:
                return error_format
        
        elif "query_equal" in parsed_info:
            try:
                raw = parsed_info["query_equal"].strip()
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 2:
                    return error_format
                
                pos1 = int(parts[0])
                pos2 = int(parts[1])
                
                if pos1 < 1 or pos1 > self.n or pos2 < 1 or pos2 > self.n:
                    return error_range.format(self.n)
                
                self.query_count += 1
                return yes_res if self.sequence[pos1] == self.sequence[pos2] else no_res
            except:
                return error_format
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是": return "否"
        if correct == "否": return "是"
        
        low = correct.lower()
        if low == "yes":
            if correct == "YES": return "NO"
            if correct == "yes": return "no"
            return "No"
        if low == "no":
            if correct == "NO": return "YES"
            if correct == "no": return "yes"
            return "Yes"

        return correct + "_WRONG"