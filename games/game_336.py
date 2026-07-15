import random
from .base import Game

class PatternOccurrenceGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"模式出现位置推理"游戏，规则如下：

游戏设定了一个长度为 {N} 的隐藏序列 S，序列中每个位置的元素取自一个有限字母表（具体取值保密）。同时给定一个长度为 {K} 的目标模式 P = "{pattern}"。

定义：当存在起点 i 使得序列 S 在位置 i 到 i+{K}−1 处与模式 P完全匹配时，称 P 在 S 中于起点 i 处出现一次。允许不同起点的出现重叠，每个符合条件的起点计为一次独立出现。

你的目标是：确定目标模式 P 在序列 S 中所有出现的起点位置集合（若不存在则报告"无出现"）。

你可以反复提出以下两类问题（每次仅限一个问题），我会根据真实的隐藏序列如实回答：

1. 存在性查询：询问在区间 [L,R] 内是否存在至少一次完整出现。
   - 形式化：是否存在起点 i 满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该位置与模式 P 匹配。
   - 回答："是" 或 "否"。
   - 注意：若 {K} 大于 R−L+1，则必为"否"。

2. 计数查询：询问在区间 [L,R] 内完整出现了多少次。
   - 形式化：返回满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该位置与模式 P 匹配的起点 i 的数量。
   - 回答：一个非负整数。
   - 注意：若 {K} 大于 R−L+1，则必为 0。

每次询问只能包含一个标签，使用以下 XML 格式：

- 存在性查询（例如查询区间 [2,5]）：
<query_exist>2,5</query_exist>

- 计数查询（例如查询区间 [1,8]）：
<query_count>1,8</query_count>

提交最终答案时，必须说明出现次数 M 及所有起点位置（用逗号分隔，严格递增顺序）。若无出现，则次数为 0，位置列表为空。格式如下：

<answer>count=3, positions=2,5,7</answer>

或

<answer>count=0, positions=</answer>

请尽可能少地提问，以高效确定所有出现位置。
"""

    game_rule_en = """\
Let's play a "Pattern Occurrence Inference" game. Here are the rules:

A hidden sequence S of length {N} has been set up, where each position contains an element from a finite alphabet (specific values are secret). You are also given a target pattern P of length {K}: P = "{pattern}".

Definition: When there exists a starting position i such that sequence S matches pattern P exactly from position i to i+{K}−1, we say P occurs at starting position i in S. Occurrences at different starting positions may overlap, and each valid starting position counts as an independent occurrence.

Your goal is: Determine the set of all starting positions where pattern P occurs in sequence S (or report "no occurrence" if none exist).

You may repeatedly ask the following two types of questions (one per turn), and I will answer truthfully based on the real hidden sequence:

1. Existence Query: Ask whether there exists at least one complete occurrence within interval [L,R].
   - Formalization: Does there exist a starting position i such that L is less than or equal to i and i+{K}−1 is less than or equal to R, with the substring matching pattern P.
   - Answer: "Yes" or "No".
   - Note: If {K} is greater than R−L+1, the answer must be "No".

2. Count Query: Ask how many times the pattern occurs completely within interval [L,R].
   - Formalization: Return the count of starting positions i satisfying L is less than or equal to i and i+{K}−1 is less than or equal to R, with the substring matching pattern P.
   - Answer: A non-negative integer.
   - Note: If {K} is greater than R−L+1, the answer must be 0.

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., querying interval [2,5]):
<query_exist>2,5</query_exist>

- Count Query (e.g., querying interval [1,8]):
<query_count>1,8</query_count>

When submitting the final answer, specify the occurrence count M and all starting positions (comma-separated, in strictly increasing order). If no occurrence, count is 0 and positions list is empty. Format:

<answer>count=3, positions=2,5,7</answer>

or

<answer>count=0, positions=</answer>

Try to ask as few questions as possible to efficiently determine all occurrence positions.
"""

    contextualized_rule_zh_1 = """\
我们现在进入智能交通系统的“违规驾驶模式溯源”任务，规则如下：

监控系统记录了一条长度为 {N} 的路网监控时序日志 S，每个时刻的元素记录了路段的交通状态特征（具体状态保密）。同时，交管部门定义了一种长度为 {K} 的高危驾驶行为模式 P = "{pattern}"。

定义：当存在起始时刻 i 使得时序日志 S 在时刻 i 到 i+{K}−1 处与高危模式 P 完全匹配时，称 P 在 S 中于起始时刻 i 处发生一次。允许不同起点的发生重叠，每个符合条件的起始时刻计为一次独立违规事件。

你的目标是：确定高危驾驶行为模式 P 在时序日志 S 中所有发生的起始时刻集合（若不存在则报告"无出现"）。

你可以反复提出以下两类查询（每次仅限一个查询），系统会根据真实的隐藏日志如实回答：

1. 存在性查询：询问在时间区间 [L,R] 内是否存在至少一次完整的高危模式。
   - 形式化：是否存在起始时刻 i 满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该段状态与模式 P 匹配。
   - 回答："是" 或 "否"。
   - 注意：若 {K} 大于 R−L+1，则必为"否"。

2. 计数查询：询问在时间区间 [L,R] 内完整发生了多少次该高危模式。
   - 形式化：返回满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该段状态与模式 P 匹配的起始时刻 i 的数量。
   - 回答：一个非负整数。
   - 注意：若 {K} 大于 R−L+1，则必为 0。

每次询问只能包含一个标签，使用以下 XML 格式：

- 存在性查询（例如查询时间区间 [2,5]）：
<query_exist>2,5</query_exist>

- 计数查询（例如查询时间区间 [1,8]）：
<query_count>1,8</query_count>

提交最终答案时，必须说明发生次数 M 及所有起始时刻位置（用逗号分隔，严格递增顺序）。若无发生，则次数为 0，位置列表为空。格式如下：

<answer>count=3, positions=2,5,7</answer>

或

<answer>count=0, positions=</answer>

请尽可能少地提问，以高效确定所有高危行为的发生时刻。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's step into the "High-Risk Driving Pattern Tracing" task of the intelligent traffic system. Here are the rules:

The monitoring system has recorded a continuous traffic state log S of length {N}, where each timestamp contains a traffic feature element (specific states are secret). Meanwhile, the traffic management department has defined a high-risk driving behavior pattern P of length {K}: P = "{pattern}".

Definition: When there exists a starting timestamp i such that the log S matches pattern P exactly from timestamp i to i+{K}−1, we say P occurs at starting timestamp i in S. Occurrences at different starting timestamps may overlap, and each valid starting timestamp counts as an independent violation event.

Your goal is: Determine the set of all starting timestamps where the high-risk pattern P occurs in the log S (or report "no occurrence" if none exist).

You may repeatedly ask the following two types of queries (one per turn), and the system will answer truthfully based on the real hidden log:

1. Existence Query: Ask whether there exists at least one complete occurrence within the time interval [L,R].
   - Formalization: Does there exist a starting timestamp i such that L is less than or equal to i and i+{K}−1 is less than or equal to R, with the sub-log matching pattern P.
   - Answer: "Yes" or "No".
   - Note: If {K} is greater than R−L+1, the answer must be "No".

2. Count Query: Ask how many times the high-risk pattern occurs completely within the time interval [L,R].
   - Formalization: Return the count of starting timestamps i satisfying L is less than or equal to i and i+{K}−1 is less than or equal to R, with the sub-log matching pattern P.
   - Answer: A non-negative integer.
   - Note: If {K} is greater than R−L+1, the answer must be 0.

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., querying time interval [2,5]):
<query_exist>2,5</query_exist>

- Count Query (e.g., querying time interval [1,8]):
<query_count>1,8</query_count>

When submitting the final answer, specify the occurrence count M and all starting timestamps (comma-separated, in strictly increasing order). If no occurrence, count is 0 and positions list is empty. Format:

<answer>count=3, positions=2,5,7</answer>

or

<answer>count=0, positions=</answer>

Try to ask as few questions as possible to efficiently determine all violation timestamps.
"""

    contextualized_rule_zh_2 = """\
我们现在进入基因组学系统的“致病突变模式溯源”任务，规则如下：

测序设备提取了一段长度为 {N} 的隐藏基因组序列 S，序列中每个位点的核苷酸取自生命密码字母表（具体序列保密）。同时，医学数据库指定了一种长度为 {K} 的致病突变模式 P = "{pattern}"。

定义：当存在起始位点 i 使得基因序列 S 在位点 i 到 i+{K}−1 处与突变模式 P 完全匹配时，称 P 在 S 中于起始位点 i 处出现一次。允许不同起点的突变重叠，每个符合条件的起始位点计为一次独立变异。

你的目标是：确定致病突变模式 P 在基因序列 S 中所有出现的起始位点集合（若不存在则报告"无出现"）。

你可以反复提出以下两类查询（每次仅限一个查询），系统会根据真实的隐藏基因序列如实回答：

1. 存在性查询：询问在序列区间 [L,R] 内是否存在至少一次完整的致病突变。
   - 形式化：是否存在起始位点 i 满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该段序列与突变模式 P 匹配。
   - 回答："是" 或 "否"。
   - 注意：若 {K} 大于 R−L+1，则必为"否"。

2. 计数查询：询问在序列区间 [L,R] 内完整出现了多少次该致病突变。
   - 形式化：返回满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该段序列与突变模式 P 匹配的起始位点 i 的数量。
   - 回答：一个非负整数。
   - 注意：若 {K} 大于 R−L+1，则必为 0。

每次询问只能包含一个标签，使用以下 XML 格式：

- 存在性查询（例如查询序列区间 [2,5]）：
<query_exist>2,5</query_exist>

- 计数查询（例如查询序列区间 [1,8]）：
<query_count>1,8</query_count>

提交最终答案时，必须说明突变发生次数 M 及所有起始位点（用逗号分隔，严格递增顺序）。若无出现，则次数为 0，位置列表为空。格式如下：

<answer>count=3, positions=2,5,7</answer>

或

<answer>count=0, positions=</answer>

请尽可能少地提问，以高效确定所有致病突变位点。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's step into the "Pathogenic Mutation Pattern Tracing" task of the genomics system. Here are the rules:

The sequencing device has extracted a hidden genomic sequence S of length {N}, where each locus contains a nucleotide from the biological alphabet (the specific sequence is secret). Meanwhile, the medical database specifies a pathogenic mutation pattern P of length {K}: P = "{pattern}".

Definition: When there exists a starting locus i such that the genomic sequence S matches the mutation pattern P exactly from locus i to i+{K}−1, we say P occurs at starting locus i in S. Occurrences at different starting loci may overlap, and each valid starting locus counts as an independent variation.

Your goal is: Determine the set of all starting loci where the pathogenic mutation pattern P occurs in the sequence S (or report "no occurrence" if none exist).

You may repeatedly ask the following two types of queries (one per turn), and the system will answer truthfully based on the real hidden genomic sequence:

1. Existence Query: Ask whether there exists at least one complete pathogenic mutation within the sequence interval [L,R].
   - Formalization: Does there exist a starting locus i such that L is less than or equal to i and i+{K}−1 is less than or equal to R, with the sub-sequence matching pattern P.
   - Answer: "Yes" or "No".
   - Note: If {K} is greater than R−L+1, the answer must be "No".

2. Count Query: Ask how many times the pathogenic mutation completely occurs within the sequence interval [L,R].
   - Formalization: Return the count of starting loci i satisfying L is less than or equal to i and i+{K}−1 is less than or equal to R, with the sub-sequence matching pattern P.
   - Answer: A non-negative integer.
   - Note: If {K} is greater than R−L+1, the answer must be 0.

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., querying sequence interval [2,5]):
<query_exist>2,5</query_exist>

- Count Query (e.g., querying sequence interval [1,8]):
<query_count>1,8</query_count>

When submitting the final answer, specify the mutation count M and all starting loci (comma-separated, in strictly increasing order). If no occurrence, count is 0 and positions list is empty. Format:

<answer>count=3, positions=2,5,7</answer>

or

<answer>count=0, positions=</answer>

Try to ask as few questions as possible to efficiently determine all mutation loci.
"""

    contextualized_rule_zh_3 = """\
我们现在进入在线教育系统的“异常作弊行为溯源”任务，规则如下：

平台后端记录了一名学生长度为 {N} 的在线学习行为日志序列 S，每个索引记录了特定的交互动作（具体动作保密）。同时，教务处定义了一种长度为 {K} 的典型作弊行为模式 P = "{pattern}"。

定义：当存在起始日志索引 i 使得行为序列 S 在索引 i 到 i+{K}−1 处与作弊模式 P 完全匹配时，称 P 在 S 中于起始索引 i 处发生一次。允许不同起点的行为重叠，每个符合条件的起始索引计为一次独立作弊动作。

你的目标是：确定作弊行为模式 P 在行为日志序列 S 中所有发生的起始索引集合（若不存在则报告"无出现"）。

你可以反复提出以下两类查询（每次仅限一个查询），系统会根据真实的学生日志如实回答：

1. 存在性查询：询问在日志区间 [L,R] 内是否存在至少一次完整的作弊模式。
   - 形式化：是否存在起始索引 i 满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该段行为与模式 P 匹配。
   - 回答："是" 或 "否"。
   - 注意：若 {K} 大于 R−L+1，则必为"否"。

2. 计数查询：询问在日志区间 [L,R] 内完整发生了多少次该作弊模式。
   - 形式化：返回满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该段行为与模式 P 匹配的起始索引 i 的数量。
   - 回答：一个非负整数。
   - 注意：若 {K} 大于 R−L+1，则必为 0。

每次询问只能包含一个标签，使用以下 XML 格式：

- 存在性查询（例如查询日志区间 [2,5]）：
<query_exist>2,5</query_exist>

- 计数查询（例如查询日志区间 [1,8]）：
<query_count>1,8</query_count>

提交最终答案时，必须说明作弊发生次数 M 及所有起始索引位置（用逗号分隔，严格递增顺序）。若无出现，则次数为 0，位置列表为空。格式如下：

<answer>count=3, positions=2,5,7</answer>

或

<answer>count=0, positions=</answer>

请尽可能少地提问，以高效确定所有违规行为的索引。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's step into the "Abnormal Cheating Behavior Tracing" task of the online education system. Here are the rules:

The platform backend has recorded an online learning behavior log sequence S of length {N} for a student, where each index logs a specific interaction action (specific actions are secret). Meanwhile, the academic office has defined a typical cheating behavior pattern P of length {K}: P = "{pattern}".

Definition: When there exists a starting log index i such that the behavior sequence S matches pattern P exactly from index i to i+{K}−1, we say P occurs at starting index i in S. Occurrences at different starting indices may overlap, and each valid starting index counts as an independent cheating action.

Your goal is: Determine the set of all starting indices where the cheating behavior pattern P occurs in the log sequence S (or report "no occurrence" if none exist).

You may repeatedly ask the following two types of queries (one per turn), and the system will answer truthfully based on the real hidden behavior log:

1. Existence Query: Ask whether there exists at least one complete cheating pattern within the log interval [L,R].
   - Formalization: Does there exist a starting index i such that L is less than or equal to i and i+{K}−1 is less than or equal to R, with the sub-log matching pattern P.
   - Answer: "Yes" or "No".
   - Note: If {K} is greater than R−L+1, the answer must be "No".

2. Count Query: Ask how many times the cheating pattern completely occurs within the log interval [L,R].
   - Formalization: Return the count of starting indices i satisfying L is less than or equal to i and i+{K}−1 is less than or equal to R, with the sub-log matching pattern P.
   - Answer: A non-negative integer.
   - Note: If {K} is greater than R−L+1, the answer must be 0.

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., querying log interval [2,5]):
<query_exist>2,5</query_exist>

- Count Query (e.g., querying log interval [1,8]):
<query_count>1,8</query_count>

When submitting the final answer, specify the cheating count M and all starting indices (comma-separated, in strictly increasing order). If no occurrence, count is 0 and positions list is empty. Format:

<answer>count=3, positions=2,5,7</answer>

or

<answer>count=0, positions=</answer>

Try to ask as few questions as possible to efficiently determine all violation indices.
"""

    contextualized_rule_zh_4 = """\
我们现在进入工业流水线的“致乱波动模式溯源”任务，规则如下：

质检传感器记录了一条长度为 {N} 的加工参数序列 S，每个检测点包含了温度与压力的状态读数（具体参数保密）。同时，品控部门界定了一种长度为 {K} 的致乱波动模式 P = "{pattern}"。

定义：当存在起始检测点 i 使得加工序列 S 在检测点 i 到 i+{K}−1 处与波动模式 P 完全匹配时，称 P 在 S 中于起始检测点 i 处出现一次。允许不同起点的波动重叠，每个符合条件的起始检测点计为一次独立的异常预警。

你的目标是：确定致乱波动模式 P 在加工参数序列 S 中所有出现的起始检测点集合（若不存在则报告"无出现"）。

你可以反复提出以下两类查询（每次仅限一个查询），系统会根据真实的隐藏参数序列如实回答：

1. 存在性查询：询问在检测区间 [L,R] 内是否存在至少一次完整的致乱波动模式。
   - 形式化：是否存在起始检测点 i 满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该段参数与波动模式 P 匹配。
   - 回答："是" 或 "否"。
   - 注意：若 {K} 大于 R−L+1，则必为"否"。

2. 计数查询：询问在检测区间 [L,R] 内完整出现了多少次该波动模式。
   - 形式化：返回满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该段参数与波动模式 P 匹配的起始检测点 i 的数量。
   - 回答：一个非负整数。
   - 注意：若 {K} 大于 R−L+1，则必为 0。

每次询问只能包含一个标签，使用以下 XML 格式：

- 存在性查询（例如查询检测区间 [2,5]）：
<query_exist>2,5</query_exist>

- 计数查询（例如查询检测区间 [1,8]）：
<query_count>1,8</query_count>

提交最终答案时，必须说明异常波动发生次数 M 及所有起始检测点位置（用逗号分隔，严格递增顺序）。若无出现，则次数为 0，位置列表为空。格式如下：

<answer>count=3, positions=2,5,7</answer>

或

<answer>count=0, positions=</answer>

请尽可能少地提问，以高效排查所有流水线异常检测点。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's step into the "Defective Fluctuation Pattern Tracing" task of the industrial assembly line. Here are the rules:

The quality inspection sensor has recorded a processing parameter sequence S of length {N}, where each detection point contains state readings of temperature and pressure (specific parameters are secret). Meanwhile, the quality control department has defined a defective fluctuation pattern P of length {K}: P = "{pattern}".

Definition: When there exists a starting detection point i such that the processing sequence S matches the fluctuation pattern P exactly from point i to i+{K}−1, we say P occurs at starting point i in S. Occurrences at different starting points may overlap, and each valid starting point counts as an independent anomaly alert.

Your goal is: Determine the set of all starting detection points where the defective fluctuation pattern P occurs in the parameter sequence S (or report "no occurrence" if none exist).

You may repeatedly ask the following two types of queries (one per turn), and the system will answer truthfully based on the real hidden parameter sequence:

1. Existence Query: Ask whether there exists at least one complete defective fluctuation pattern within the detection interval [L,R].
   - Formalization: Does there exist a starting point i such that L is less than or equal to i and i+{K}−1 is less than or equal to R, with the sub-sequence matching pattern P.
   - Answer: "Yes" or "No".
   - Note: If {K} is greater than R−L+1, the answer must be "No".

2. Count Query: Ask how many times the fluctuation pattern completely occurs within the detection interval [L,R].
   - Formalization: Return the count of starting points i satisfying L is less than or equal to i and i+{K}−1 is less than or equal to R, with the sub-sequence matching pattern P.
   - Answer: A non-negative integer.
   - Note: If {K} is greater than R−L+1, the answer must be 0.

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., querying detection interval [2,5]):
<query_exist>2,5</query_exist>

- Count Query (e.g., querying detection interval [1,8]):
<query_count>1,8</query_count>

When submitting the final answer, specify the fluctuation anomaly count M and all starting detection points (comma-separated, in strictly increasing order). If no occurrence, count is 0 and positions list is empty. Format:

<answer>count=3, positions=2,5,7</answer>

or

<answer>count=0, positions=</answer>

Try to ask as few questions as possible to efficiently locate all assembly line anomaly points.
"""

    contextualized_rule_zh_5 = """\
我们现在进入智能合同审查系统的“违规条款模式溯源”任务，规则如下：

系统提取了一份长度为 {N} 的商业合同条款序列 S，序列中每个段落的语义特征已被编码化（具体内容保密）。同时，法务部门规定了一种长度为 {K} 的霸王条款违规模式 P = "{pattern}"。

定义：当存在起始段落编号 i 使得条款序列 S 在编号 i 到 i+{K}−1 处与违规模式 P 完全匹配时，称 P 在 S 中于起始段落 i 处出现一次。允许不同起点的违规条款重叠，每个符合条件的起始段落计为一次独立的合规风险。

你的目标是：确定违规条款模式 P 在条款序列 S 中所有出现的起始段落编号集合（若不存在则报告"无风险"）。

你可以反复提出以下两类查询（每次仅限一个查询），审查系统会根据真实的隐藏条款序列如实回答：

1. 存在性查询：询问在条款区间 [L,R] 内是否存在至少一次完整的违规模式。
   - 形式化：是否存在起始段落编号 i 满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该段条款与违规模式 P 匹配。
   - 回答："是" 或 "否"。
   - 注意：若 {K} 大于 R−L+1，则必为"否"。

2. 计数查询：询问在条款区间 [L,R] 内完整出现了多少次该违规模式。
   - 形式化：返回满足 L 小于等于 i 且 i+{K}−1 小于等于 R，并且该段条款与违规模式 P 匹配的起始段落编号 i 的数量。
   - 回答：一个非负整数。
   - 注意：若 {K} 大于 R−L+1，则必为 0。

每次询问只能包含一个标签，使用以下 XML 格式：

- 存在性查询（例如查询条款区间 [2,5]）：
<query_exist>2,5</query_exist>

- 计数查询（例如查询条款区间 [1,8]）：
<query_count>1,8</query_count>

提交最终答案时，必须说明合规风险出现次数 M 及所有起始段落编号（用逗号分隔，严格递增顺序）。若无出现，则次数为 0，位置列表为空。格式如下：

<answer>count=3, positions=2,5,7</answer>

或

<answer>count=0, positions=</answer>

请尽可能少地提问，以高效锁定所有潜藏的法律违规条款。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's step into the "Unfair Term Pattern Tracing" task of the automated contract review system. Here are the rules:

The system has extracted a commercial contract clause sequence S of length {N}, where the semantic feature of each paragraph has been encoded (specific contents are secret). Meanwhile, the legal department has formulated an unfair term violation pattern P of length {K}: P = "{pattern}".

Definition: When there exists a starting paragraph index i such that the clause sequence S matches the violation pattern P exactly from index i to i+{K}−1, we say P occurs at starting paragraph i in S. Occurrences at different starting paragraphs may overlap, and each valid starting paragraph counts as an independent compliance risk.

Your goal is: Determine the set of all starting paragraph indices where the violation pattern P occurs in the clause sequence S (or report "no risk" if none exist).

You may repeatedly ask the following two types of queries (one per turn), and the review system will answer truthfully based on the real hidden clause sequence:

1. Existence Query: Ask whether there exists at least one complete violation pattern within the clause interval [L,R].
   - Formalization: Does there exist a starting paragraph index i such that L is less than or equal to i and i+{K}−1 is less than or equal to R, with the sub-clause matching pattern P.
   - Answer: "Yes" or "No".
   - Note: If {K} is greater than R−L+1, the answer must be "No".

2. Count Query: Ask how many times the violation pattern completely occurs within the clause interval [L,R].
   - Formalization: Return the count of starting paragraph indices i satisfying L is less than or equal to i and i+{K}−1 is less than or equal to R, with the sub-clause matching pattern P.
   - Answer: A non-negative integer.
   - Note: If {K} is greater than R−L+1, the answer must be 0.

Each query must contain only one tag. Use the following XML format:

- Existence Query (e.g., querying clause interval [2,5]):
<query_exist>2,5</query_exist>

- Count Query (e.g., querying clause interval [1,8]):
<query_count>1,8</query_count>

When submitting the final answer, specify the compliance risk count M and all starting paragraph indices (comma-separated, in strictly increasing order). If no risk, count is 0 and positions list is empty. Format:

<answer>count=3, positions=2,5,7</answer>

or

<answer>count=0, positions=</answer>

Try to ask as few questions as possible to efficiently lock down all hidden legal violation clauses.
"""

    tags = ["answer", "query_exist", "query_count"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "N": 10,
                "K": 3,
                "pattern": "ABA",
                "sequence": "XABAXYZABA",
            },
            2: {
                "N": 15,
                "K": 4,
                "pattern": "ABCD",
                "sequence": "XABCDYABCDZABCD",
            },
            3: {
                "N": 20,
                "K": 3,
                "pattern": "AAA",
                "sequence": "XAAAAYZAAAMNAAAAABCD",
            },
            4: {
                "N": 25,
                "K": 5,
                "pattern": "ABABA",
                "sequence": "XYABABABABXYZABABABABQRST",
            },
            5: {
                "N": 30,
                "K": 4,
                "pattern": "XYXY",
                "sequence": "ABXYXYXYCDXYXYEFGHXYXYIJKLMNOP",
            },
        },
        "en": {
            1: {
                "N": 10,
                "K": 3,
                "pattern": "ABA",
                "sequence": "XABAXYZABA",
            },
            2: {
                "N": 15,
                "K": 4,
                "pattern": "ABCD",
                "sequence": "XABCDYABCDZABCD",
            },
            3: {
                "N": 20,
                "K": 3,
                "pattern": "AAA",
                "sequence": "XAAAAYZAAAMNAAAAABCD",
            },
            4: {
                "N": 25,
                "K": 5,
                "pattern": "ABABA",
                "sequence": "XYABABABABXYZABABABABQRST",
            },
            5: {
                "N": 30,
                "K": 4,
                "pattern": "XYXY",
                "sequence": "ABXYXYXYCDXYXYEFGHXYXYIJKLMNOP",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        DIFFICULTY_PARAMS = {
            1: {"N": 10, "K": 3, "alphabet_size": 3, "num_occurrences": 2},
            2: {"N": 15, "K": 4, "alphabet_size": 4, "num_occurrences": 3},
            3: {"N": 20, "K": 3, "alphabet_size": 2, "num_occurrences": 5},
            4: {"N": 25, "K": 5, "alphabet_size": 3, "num_occurrences": 3},
            5: {"N": 30, "K": 4, "alphabet_size": 4, "num_occurrences": 4},
        }

        if diff not in DIFFICULTY_PARAMS:
            raise KeyError(f"Unsupported difficulty: {diff}")

        params = DIFFICULTY_PARAMS[diff]
        N = params["N"]
        K = params["K"]
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:params["alphabet_size"]]
        target_occurrences = params["num_occurrences"]

        pattern = ''.join(random.choice(alphabet) for _ in range(K))

        sequence = list(''.join(random.choice(alphabet) for _ in range(N)))

        possible_starts = list(range(0, N - K + 1))
        random.shuffle(possible_starts)
        planted = []
        for s in possible_starts:
            if len(planted) >= target_occurrences:
                break
            planted.append(s)
            for j in range(K):
                sequence[s + j] = pattern[j]

        self.sequence = ''.join(sequence)
        self.pattern = pattern
        self.N = N
        self.K = K

        self._game_info["N"] = N
        self._game_info["K"] = K
        self._game_info["pattern"] = pattern

        self.true_positions = set()
        for i in range(1, self.N - self.K + 2):
            if self.sequence[i-1:i-1+self.K] == self.pattern:
                self.true_positions.add(i)

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",", 1)]
            ans_dict = {}
            
            for kv in kv_pairs:
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "count" not in ans_dict or "positions" not in ans_dict:
                return False
            
            try:
                reported_count = int(ans_dict["count"])
            except:
                return False
            
            if reported_count != len(self.true_positions):
                return False
            
            positions_str = ans_dict["positions"].strip()
            
            if reported_count == 0:
                return positions_str == "" and len(self.true_positions) == 0
            else:
                try:
                    reported_positions = set(int(x.strip()) for x in positions_str.split(",") if x.strip())
                except:
                    return False
                
                return reported_positions == self.true_positions
                
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或区间参数错误。"
            error_range = "错误：区间超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or interval parameters."
            error_range = "Error: Interval out of range."

        if "query_exist" in parsed_info:
            try:
                raw = parsed_info["query_exist"].strip()
                L, R = [int(x.strip()) for x in raw.split(",")]
                
                if L < 1 or R > self.N or L > R:
                    return error_range
                
                if self.K > R - L + 1:
                    return no_res
                
                exists = any(L <= i <= R - self.K + 1 for i in self.true_positions)
                return yes_res if exists else no_res
                
            except:
                return error_format

        elif "query_count" in parsed_info:
            try:
                raw = parsed_info["query_count"].strip()
                L, R = [int(x.strip()) for x in raw.split(",")]
                
                if L < 1 or R > self.N or L > R:
                    return error_range
                
                if self.K > R - L + 1:
                    return "0"
                
                count = sum(1 for i in self.true_positions if L <= i <= R - self.K + 1)
                return str(count)
                
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是": return "否"
            if correct == "否": return "是"
        
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        queries = []
        
        full_interval = f"1,{self.N}"
        queries.append({
            "query": f"<query_count>{full_interval}</query_count>",
            "answer": self._cf_core_produce({"query_count": full_interval})
        })
        queries.append({
            "query": f"<query_exist>{full_interval}</query_exist>",
            "answer": self._cf_core_produce({"query_exist": full_interval})
        })
        
        for i in range(1, self.N - self.K + 2):
            interval = f"{i},{i + self.K - 1}"
            queries.append({
                "query": f"<query_exist>{interval}</query_exist>",
                "answer": self._cf_core_produce({"query_exist": interval})
            })
        
        def add_bisect_queries(L, R):
            if R - L + 1 < self.K:
                return
            interval = f"{L},{R}"
            queries.append({
                "query": f"<query_count>{interval}</query_count>",
                "answer": self._cf_core_produce({"query_count": interval})
            })
            if R > L:
                mid = (L + R) // 2
                add_bisect_queries(L, mid)
                add_bisect_queries(mid + 1, R)
        
        add_bisect_queries(1, self.N)
        
        seen = set()
        unique_queries = []
        for q in queries:
            key = q["query"]
            if key not in seen:
                seen.add(key)
                unique_queries.append(q)
        
        return unique_queries