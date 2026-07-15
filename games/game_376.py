from .base import Game
import re
import random

class DistanceRuleFindingGame(Game):

    game_rule_zh = """\
我们来玩一个"距离规则推理"游戏，规则如下：

游戏设定了一个长度为 {n} 的线性有序序列，位置编号为 1, 2, ..., {n}。

对于任意两个不同的位置 i 和 j，它们的原始距离定义为 d(i,j) = |i - j|。

系统使用一个隐藏的映射函数 f，将任意原始距离 d（d 是 1 到 {n_minus_1} 之间的整数）映射为一个非负整数。该映射函数遵循以下规则：

f(d) = floor((d + B) / S)

其中：
- S 是一个大于等于 2 的整数（缩放参数）
- B 是一个整数且满足 0 小于等于 B 小于 S（偏移参数）
- floor 表示向下取整

对于任意查询的位置对 (i,j)，系统定义响应函数 R(i,j) = f(|i - j|)。系统保证对所有查询使用相同的参数 S 和 B，且满足对称性 R(i,j) = R(j,i)。

你的目标是通过尽可能少的查询，推断出隐藏的参数 S 和 B。

你可以进行以下三类查询（每次只能进行一个查询）：

1. **精确查询**：询问两个位置 i 和 j 的响应值 R(i,j) 是多少。系统会返回一个非负整数。
2. **比较查询**：询问 R(i,j) 与 R(p,q) 的大小关系。系统会返回三种结果之一："小于"、"等于"或"大于"。
3. **阈值查询**：询问 R(i,j) 是否大于等于某个阈值 t。系统会返回"是"或"否"。

所有查询中的位置编号必须在 1 到 {n} 范围内，且位置对中的两个位置必须不同。

当你收集到足够信息后，请提交最终答案。答案必须指定参数 S 和 B，要求 S 大于等于 2 且 0 小于等于 B 小于 S。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 精确查询（例如查询位置 2 和 5 的响应值）：
<query_ask>2,5</query_ask>

- 比较查询（例如比较 R(1,3) 与 R(2,6)）：
<query_cmp>1,3,2,6</query_cmp>

- 阈值查询（例如查询 R(3,7) 是否大于等于 2）：
<query_ge>3,7,2</query_ge>

提交最终答案时，必须指定参数 S 和 B，格式如下：

<answer>S=3,B=1</answer>
"""

    game_rule_en = """\
Let's play a "Distance Rule Finding" game. Here are the rules:

The game is set on a linear ordered sequence of length {n}, with positions numbered 1, 2, ..., {n}.

For any two different positions i and j, their original distance is defined as d(i,j) = |i - j|.

The system uses a hidden mapping function f that maps any original distance d (an integer between 1 and {n_minus_1}) to a non-negative integer. This mapping follows the rule:

f(d) = floor((d + B) / S)

Where:
- S is an integer greater than or equal to 2 (scaling parameter)
- B is an integer satisfying 0 less than or equal to B less than S (offset parameter)
- floor denotes rounding down to the nearest integer

For any queried position pair (i,j), the system defines a response function R(i,j) = f(|i - j|). The system guarantees to use the same parameters S and B for all queries, and satisfies symmetry R(i,j) = R(j,i).

Your goal is to infer the hidden parameters S and B through as few queries as possible.

You can perform the following three types of queries (only one query per turn):

1. **Ask Query**: Ask for the exact response value R(i,j) for positions i and j. The system returns a non-negative integer.
2. **Compare Query**: Ask for the comparison between R(i,j) and R(p,q). The system returns one of three results: "less than", "equal to", or "greater than".
3. **Threshold Query**: Ask whether R(i,j) is greater than or equal to a threshold t. The system returns "yes" or "no".

All position numbers in queries must be within the range 1 to {n}, and the two positions in a pair must be different.

When you have gathered enough information, submit your final answer. The answer must specify parameters S and B, with S greater than or equal to 2 and 0 less than or equal to B less than S. If the answer is incorrect or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Ask Query (e.g., querying the response value for positions 2 and 5):
<query_ask>2,5</query_ask>

- Compare Query (e.g., comparing R(1,3) with R(2,6)):
<query_cmp>1,3,2,6</query_cmp>

- Threshold Query (e.g., querying whether R(3,7) is greater than or equal to 2):
<query_ge>3,7,2</query_ge>

When submitting the final answer, specify parameters S and B in this format:

<answer>S=3,B=1</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“公路收费规则推演”系统。在本系统中，设定了一条具有 {n} 个连续收费站的线性公路，站点编号为 1 至 {n}。

对于任意两个不同收费站 i 和 j，它们的实际距离定义为跨度 d(i,j) = |i - j|。

计费系统后台使用一个隐藏的映射函数 f，将该跨度 d（d 是 1 到 {n_minus_1} 之间的整数）映射为实际的收费区段数量（非负整数）。该计费函数遵循以下规则：

f(d) = floor((d + B) / S)

其中：
- S 是区段长度参数（大于等于 2 的整数）
- B 是免费缓冲参数（满足 0 小于等于 B 小于 S 的整数）
- floor 表示向下取整

对于任意查询的收费站对 (i,j)，系统定义响应函数 R(i,j) = f(|i - j|) 表示往返 i 和 j 的收费区段数。系统保证对所有查询使用相同的参数 S 和 B，且满足对称性 R(i,j) = R(j,i)。

你的目标是通过尽可能少的查询，推断出隐藏的参数 S 和 B。

你可以进行以下三类查询（每次只能进行一个查询）：

1. **精确查询**：询问收费站 i 和 j 的响应值 R(i,j) 是多少。系统会返回一个非负整数。
2. **比较查询**：询问 R(i,j) 与 R(p,q) 的大小关系。系统会返回三种结果之一："小于"、"等于"或"大于"。
3. **阈值查询**：询问 R(i,j) 是否大于等于某个阈值 t。系统会返回"是"或"否"。

所有查询中的站点编号必须在 1 到 {n} 范围内，且站点对中的两个位置必须不同。

当你收集到足够信息后，请提交最终答案。答案必须指定参数 S 和 B，要求 S 大于等于 2 且 0 小于等于 B 小于 S。若答案错误或格式不符，测试失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 精确查询（例如查询站点 2 和 5 的收费区段数）：
<query_ask>2,5</query_ask>

- 比较查询（例如比较 R(1,3) 与 R(2,6)）：
<query_cmp>1,3,2,6</query_cmp>

- 阈值查询（例如查询 R(3,7) 是否大于等于 2）：
<query_ge>3,7,2</query_ge>

提交最终答案时，必须指定参数 S 和 B，格式如下：

<answer>S=3,B=1</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the 'Highway Toll Rule Deduction' system. The system features a linear highway with {n} sequential toll stations, numbered 1 to {n}.

For any two different stations i and j, their span is defined as d(i,j) = |i - j|.

The billing system uses a hidden mapping function f that maps this span d (an integer between 1 and {n_minus_1}) to the actual number of charged zones (a non-negative integer). This billing follows the rule:

f(d) = floor((d + B) / S)

Where:
- S is the zone length parameter (an integer greater than or equal to 2)
- B is the free buffer parameter (an integer satisfying 0 less than or equal to B less than S)
- floor denotes rounding down to the nearest integer

For any queried station pair (i,j), the system defines a response function R(i,j) = f(|i - j|) representing the charged zones between i and j. The system guarantees to use the same parameters S and B for all queries, and satisfies symmetry R(i,j) = R(j,i).

Your goal is to infer the hidden parameters S and B through as few queries as possible.

You can perform the following three types of queries (only one query per turn):

1. **Ask Query**: Ask for the exact response value R(i,j) for stations i and j. The system returns a non-negative integer.
2. **Compare Query**: Ask for the comparison between R(i,j) and R(p,q). The system returns one of three results: "less than", "equal to", or "greater than".
3. **Threshold Query**: Ask whether R(i,j) is greater than or equal to a threshold t. The system returns "yes" or "no".

All station numbers in queries must be within the range 1 to {n}, and the two stations in a pair must be different.

When you have gathered enough information, submit your final answer. The answer must specify parameters S and B, with S greater than or equal to 2 and 0 less than or equal to B less than S. If the answer is incorrect or the format is invalid, the test fails.

Each query must contain only one tag. Use the following XML format:

- Ask Query (e.g., querying the response value for stations 2 and 5):
<query_ask>2,5</query_ask>

- Compare Query (e.g., comparing R(1,3) with R(2,6)):
<query_cmp>1,3,2,6</query_cmp>

- Threshold Query (e.g., querying whether R(3,7) is greater than or equal to 2):
<query_ge>3,7,2</query_ge>

When submitting the final answer, specify parameters S and B in this format:

<answer>S=3,B=1</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“靶向药物代谢推演”系统。本疗程包含 {n} 个连续的给药日，编号为 1 至 {n}。

对于任意两个不同的给药日 i 和 j，它们的时间间隔定义为 d(i,j) = |i - j|。

医疗系统根据一个隐藏的代谢函数 f，将时间间隔 d（d 是 1 到 {n_minus_1} 之间的整数）映射为患者的抗体生成指数（非负整数）。计算公式为：

f(d) = floor((d + B) / S)

其中：
- S 是代谢速率衰减系数（大于等于 2 的整数）
- B 是基础代谢偏移量（满足 0 小于等于 B 小于 S 的整数）
- floor 表示向下取整

对于任意查询的给药日组合 (i,j)，系统定义响应函数 R(i,j) = f(|i - j|) 反映了这两天联合给药的抗体指数。系统保证对所有查询使用相同的参数 S 和 B，且满足对称性 R(i,j) = R(j,i)。

你的任务是通过最少的查询，推断出隐藏的代谢参数 S 和 B。

你可以进行以下三类查询（每次只能进行一个查询）：

1. **精确查询**：询问给药日 i 和 j 的响应值 R(i,j) 是多少。系统会返回一个非负整数。
2. **比较查询**：询问 R(i,j) 与 R(p,q) 的大小关系。系统会返回三种结果之一："小于"、"等于"或"大于"。
3. **阈值查询**：询问 R(i,j) 是否大于等于某个阈值 t。系统会返回"是"或"否"。

所有查询中的日期编号必须在 1 到 {n} 范围内，且日期对中的两天必须不同。

当你收集到足够信息后，请提交最终答案。答案必须指定参数 S 和 B，要求 S 大于等于 2 且 0 小于等于 B 小于 S。若答案错误或格式不符，推演失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 精确查询（例如查询第 2 和第 5 天的抗体指数）：
<query_ask>2,5</query_ask>

- 比较查询（例如比较 R(1,3) 与 R(2,6)）：
<query_cmp>1,3,2,6</query_cmp>

- 阈值查询（例如查询 R(3,7) 是否大于等于 2）：
<query_ge>3,7,2</query_ge>

提交最终答案时，必须指定参数 S 和 B，格式如下：

<answer>S=3,B=1</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the 'Targeted Drug Metabolism Deduction' system. The therapy protocol consists of {n} sequential medication days, numbered 1 to {n}.

For any two different medication days i and j, their time interval is defined as d(i,j) = |i - j|.

The medical system uses a hidden metabolic function f to map the interval d (an integer between 1 and {n_minus_1}) to the patient's antibody generation index (a non-negative integer). The formula is:

f(d) = floor((d + B) / S)

Where:
- S is the metabolic decay coefficient (an integer greater than or equal to 2)
- B is the basal offset (an integer satisfying 0 less than or equal to B less than S)
- floor denotes rounding down to the nearest integer

For any queried medication day pair (i,j), the system defines a response function R(i,j) = f(|i - j|) representing the antibody index for joint medication on these days. The system guarantees to use the same parameters S and B for all queries, and satisfies symmetry R(i,j) = R(j,i).

Your task is to infer the hidden metabolic parameters S and B using as few queries as possible.

You can perform the following three types of queries (only one query per turn):

1. **Ask Query**: Ask for the exact response value R(i,j) for days i and j. The system returns a non-negative integer.
2. **Compare Query**: Ask for the comparison between R(i,j) and R(p,q). The system returns one of three results: "less than", "equal to", or "greater than".
3. **Threshold Query**: Ask whether R(i,j) is greater than or equal to a threshold t. The system returns "yes" or "no".

All day numbers in queries must be within the range 1 to {n}, and the two days in a pair must be different.

When you have gathered enough information, submit your final answer. The answer must specify parameters S and B, with S greater than or equal to 2 and 0 less than or equal to B less than S. If the answer is incorrect or the format is invalid, the deduction fails.

Each query must contain only one tag. Use the following XML format:

- Ask Query (e.g., querying the antibody index for days 2 and 5):
<query_ask>2,5</query_ask>

- Compare Query (e.g., comparing R(1,3) with R(2,6)):
<query_cmp>1,3,2,6</query_cmp>

- Threshold Query (e.g., querying whether R(3,7) is greater than or equal to 2):
<query_ge>3,7,2</query_ge>

When submitting the final answer, specify parameters S and B in this format:

<answer>S=3,B=1</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“认知负荷评估”系统。本课程大纲包含 {n} 个难度递进的学习模块，编号为 1 至 {n}。

对于任意两个不同的模块 i 和 j，它们的难度跨度定义为 d(i,j) = |i - j|。

教育系统使用一个隐藏的评估函数 f，将难度跨度 d（d 是 1 到 {n_minus_1} 之间的整数）映射为额外的认知负荷指数（非负整数）。该评估公式遵循以下规则：

f(d) = floor((d + B) / S)

其中：
- S 是认知支架跨度参数（大于等于 2 的整数）
- B 是基础知识补偿参数（满足 0 小于等于 B 小于 S 的整数）
- floor 表示向下取整

对于任意查询的模块对 (i,j)，系统定义响应函数 R(i,j) = f(|i - j|) 反映了同时修读这两个模块时的额外认知负荷。系统保证对所有查询使用相同的参数 S 和 B，且满足对称性 R(i,j) = R(j,i)。

你的任务是通过最少的查询，推断出隐藏的参数 S 和 B。

你可以进行以下三类查询（每次只能进行一个查询）：

1. **精确查询**：询问模块 i 和 j 的响应值 R(i,j) 是多少。系统会返回一个非负整数。
2. **比较查询**：询问 R(i,j) 与 R(p,q) 的大小关系。系统会返回三种结果之一："小于"、"等于"或"大于"。
3. **阈值查询**：询问 R(i,j) 是否大于等于某个阈值 t。系统会返回"是"或"否"。

所有查询中的模块编号必须在 1 到 {n} 范围内，且模块对中的两个位置必须不同。

当你收集到足够信息后，请提交最终答案。答案必须指定参数 S 和 B，要求 S 大于等于 2 且 0 小于等于 B 小于 S。若答案错误或格式不符，评估失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 精确查询（例如查询模块 2 和 5 的额外认知负荷）：
<query_ask>2,5</query_ask>

- 比较查询（例如比较 R(1,3) 与 R(2,6)）：
<query_cmp>1,3,2,6</query_cmp>

- 阈值查询（例如查询 R(3,7) 是否大于等于 2）：
<query_ge>3,7,2</query_ge>

提交最终答案时，必须指定参数 S 和 B，格式如下：

<answer>S=3,B=1</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the 'Cognitive Load Assessment' system. This curriculum contains {n} progressively difficult learning modules, numbered 1 to {n}.

For any two different modules i and j, their difficulty span is defined as d(i,j) = |i - j|.

The educational system uses a hidden evaluation function f to map the span d (an integer between 1 and {n_minus_1}) to an additional cognitive load index (a non-negative integer). The formula follows this rule:

f(d) = floor((d + B) / S)

Where:
- S is the cognitive scaffold span parameter (an integer greater than or equal to 2)
- B is the foundational compensation parameter (an integer satisfying 0 less than or equal to B less than S)
- floor denotes rounding down to the nearest integer

For any queried module pair (i,j), the system defines a response function R(i,j) = f(|i - j|) representing the additional load of taking both modules simultaneously. The system guarantees to use the same parameters S and B for all queries, and satisfies symmetry R(i,j) = R(j,i).

Your task is to infer the hidden parameters S and B using as few queries as possible.

You can perform the following three types of queries (only one query per turn):

1. **Ask Query**: Ask for the exact response value R(i,j) for modules i and j. The system returns a non-negative integer.
2. **Compare Query**: Ask for the comparison between R(i,j) and R(p,q). The system returns one of three results: "less than", "equal to", or "greater than".
3. **Threshold Query**: Ask whether R(i,j) is greater than or equal to a threshold t. The system returns "yes" or "no".

All module numbers in queries must be within the range 1 to {n}, and the two modules in a pair must be different.

When you have gathered enough information, submit your final answer. The answer must specify parameters S and B, with S greater than or equal to 2 and 0 less than or equal to B less than S. If the answer is incorrect or the format is invalid, the assessment fails.

Each query must contain only one tag. Use the following XML format:

- Ask Query (e.g., querying the additional cognitive load for modules 2 and 5):
<query_ask>2,5</query_ask>

- Compare Query (e.g., comparing R(1,3) with R(2,6)):
<query_cmp>1,3,2,6</query_cmp>

- Threshold Query (e.g., querying whether R(3,7) is greater than or equal to 2):
<query_ge>3,7,2</query_ge>

When submitting the final answer, specify parameters S and B in this format:

<answer>S=3,B=1</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“流水线物流节拍测算”系统。在智能车间内，部署了一条包含 {n} 个连续工位的直线装配线，工位编号为 1 至 {n}。

对于任意两个不同的工位 i 和 j，它们的物理站距定义为 d(i,j) = |i - j|。

自动化系统使用一个隐藏的传输函数 f，将站距 d（d 是 1 到 {n_minus_1} 之间的整数）转换为标准化的物流传输节拍（非负整数）。转换规则如下：

f(d) = floor((d + B) / S)

其中：
- S 是传送带速度因子（大于等于 2 的整数）
- B 是机械臂抓取耗时补偿（满足 0 小于等于 B 小于 S 的整数）
- floor 表示向下取整

对于任意查询的工位对 (i,j)，系统定义响应函数 R(i,j) = f(|i - j|) 代表两工位间的确切物流节拍数。系统保证对所有查询使用相同的参数 S 和 B，且满足对称性 R(i,j) = R(j,i)。

你的目标是通过最少次数的查询，测算出隐藏的控制参数 S 和 B。

你可以进行以下三类查询（每次只能进行一个查询）：

1. **精确查询**：询问工位 i 和 j 的响应值 R(i,j) 是多少。系统会返回一个非负整数。
2. **比较查询**：询问 R(i,j) 与 R(p,q) 的大小关系。系统会返回三种结果之一："小于"、"等于"或"大于"。
3. **阈值查询**：询问 R(i,j) 是否大于等于某个阈值 t。系统会返回"是"或"否"。

所有查询中的工位编号必须在 1 到 {n} 范围内，且工位对中的两个位置必须不同。

当你收集到足够信息后，请提交最终答案。答案必须指定参数 S 和 B，要求 S 大于等于 2 且 0 小于等于 B 小于 S。若答案错误或格式不符，测算失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 精确查询（例如查询工位 2 和 5 的物流节拍数）：
<query_ask>2,5</query_ask>

- 比较查询（例如比较 R(1,3) 与 R(2,6)）：
<query_cmp>1,3,2,6</query_cmp>

- 阈值查询（例如查询 R(3,7) 是否大于等于 2）：
<query_ge>3,7,2</query_ge>

提交最终答案时，必须指定参数 S 和 B，格式如下：

<answer>S=3,B=1</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the 'Assembly Line Logistics Cycle Calculation' system. The smart workshop features a linear assembly line with {n} sequential workstations, numbered 1 to {n}.

For any two different stations i and j, their physical station distance is defined as d(i,j) = |i - j|.

The automation system uses a hidden transfer function f to convert the distance d (an integer between 1 and {n_minus_1}) into standardized logistics transfer cycles (a non-negative integer). The rule is:

f(d) = floor((d + B) / S)

Where:
- S is the conveyor speed factor (an integer greater than or equal to 2)
- B is the robotic arm handling compensation (an integer satisfying 0 less than or equal to B less than S)
- floor denotes rounding down to the nearest integer

For any queried station pair (i,j), the system defines a response function R(i,j) = f(|i - j|) representing the exact logistics transfer cycles between the two stations. The system guarantees to use the same parameters S and B for all queries, and satisfies symmetry R(i,j) = R(j,i).

Your goal is to infer the hidden control parameters S and B through as few queries as possible.

You can perform the following three types of queries (only one query per turn):

1. **Ask Query**: Ask for the exact response value R(i,j) for stations i and j. The system returns a non-negative integer.
2. **Compare Query**: Ask for the comparison between R(i,j) and R(p,q). The system returns one of three results: "less than", "equal to", or "greater than".
3. **Threshold Query**: Ask whether R(i,j) is greater than or equal to a threshold t. The system returns "yes" or "no".

All station numbers in queries must be within the range 1 to {n}, and the two stations in a pair must be different.

When you have gathered enough information, submit your final answer. The answer must specify parameters S and B, with S greater than or equal to 2 and 0 less than or equal to B less than S. If the answer is incorrect or the format is invalid, the calculation fails.

Each query must contain only one tag. Use the following XML format:

- Ask Query (e.g., querying the logistics cycles for stations 2 and 5):
<query_ask>2,5</query_ask>

- Compare Query (e.g., comparing R(1,3) with R(2,6)):
<query_cmp>1,3,2,6</query_cmp>

- Threshold Query (e.g., querying whether R(3,7) is greater than or equal to 2):
<query_ge>3,7,2</query_ge>

When submitting the final answer, specify parameters S and B in this format:

<answer>S=3,B=1</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“合规性定级裁量”系统。该规范法典包含 {n} 条按严厉程度递增的连续条款，编号为 1 至 {n}。

对于任意两条适用的不同条款 i 和 j，它们的法理跨度定义为 d(i,j) = |i - j|。

裁量系统依据一个隐藏的量刑函数 f，将法理跨度 d（d 是 1 到 {n_minus_1} 之间的整数）映射为最终的处罚倍率（非负整数）。裁量公式如下：

f(d) = floor((d + B) / S)

其中：
- S 是法定量刑阶梯系数（大于等于 2 的整数）
- B 是从宽裁量缓冲值（满足 0 小于等于 B 小于 S 的整数）
- floor 表示向下取整

对于任意查询的适用条款对 (i,j)，系统定义响应函数 R(i,j) = f(|i - j|) 作为同时触犯这两款的最终处罚倍率。系统保证对所有查询使用相同的参数 S 和 B，且满足法理对称性 R(i,j) = R(j,i)。

你的目标是通过最少次数的查询测试，揭示隐藏的裁量参数 S 和 B。

你可以进行以下三类查询（每次只能进行一个查询）：

1. **精确查询**：询问条款 i 和 j 的响应值 R(i,j) 是多少。系统会返回一个非负整数。
2. **比较查询**：询问 R(i,j) 与 R(p,q) 的大小关系。系统会返回三种结果之一："小于"、"等于"或"大于"。
3. **阈值查询**：询问 R(i,j) 是否大于等于某个阈值 t。系统会返回"是"或"否"。

所有查询中的条款编号必须在 1 到 {n} 范围内，且条款对中的两个编号必须不同。

当你收集到足够信息后，请提交最终答案。答案必须指定参数 S 和 B，要求 S 大于等于 2 且 0 小于等于 B 小于 S。若答案错误或格式不符，测试即告失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 精确查询（例如查询条款 2 和 5 的处罚倍率）：
<query_ask>2,5</query_ask>

- 比较查询（例如比较 R(1,3) 与 R(2,6)）：
<query_cmp>1,3,2,6</query_cmp>

- 阈值查询（例如查询 R(3,7) 是否大于等于 2）：
<query_ge>3,7,2</query_ge>

提交最终答案时，必须指定参数 S 和 B，格式如下：

<answer>S=3,B=1</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the 'Compliance Grading Discretion' system. The legal code contains {n} sequential articles of increasing severity, numbered 1 to {n}.

For any two applicable different articles i and j, their jurisprudential span is defined as d(i,j) = |i - j|.

The discretion system uses a hidden sentencing function f to map the span d (an integer between 1 and {n_minus_1}) to the final penalty multiplier (a non-negative integer). The formula is:

f(d) = floor((d + B) / S)

Where:
- S is the statutory sentencing tier coefficient (an integer greater than or equal to 2)
- B is the leniency buffer value (an integer satisfying 0 less than or equal to B less than S)
- floor denotes rounding down to the nearest integer

For any queried applicable article pair (i,j), the system defines a response function R(i,j) = f(|i - j|) representing the final penalty multiplier for violating both articles. The system guarantees to use the same parameters S and B for all queries, and satisfies jurisprudential symmetry R(i,j) = R(j,i).

Your goal is to reveal the hidden discretion parameters S and B through as few query tests as possible.

You can perform the following three types of queries (only one query per turn):

1. **Ask Query**: Ask for the exact response value R(i,j) for articles i and j. The system returns a non-negative integer.
2. **Compare Query**: Ask for the comparison between R(i,j) and R(p,q). The system returns one of three results: "less than", "equal to", or "greater than".
3. **Threshold Query**: Ask whether R(i,j) is greater than or equal to a threshold t. The system returns "yes" or "no".

All article numbers in queries must be within the range 1 to {n}, and the two articles in a pair must be different.

When you have gathered enough information, submit your final answer. The answer must specify parameters S and B, with S greater than or equal to 2 and 0 less than or equal to B less than S. If the answer is incorrect or the format is invalid, the test fails.

Each query must contain only one tag. Use the following XML format:

- Ask Query (e.g., querying the penalty multiplier for articles 2 and 5):
<query_ask>2,5</query_ask>

- Compare Query (e.g., comparing R(1,3) with R(2,6)):
<query_cmp>1,3,2,6</query_cmp>

- Threshold Query (e.g., querying whether R(3,7) is greater than or equal to 2):
<query_ge>3,7,2</query_ge>

When submitting the final answer, specify parameters S and B in this format:

<answer>S=3,B=1</answer>
"""

    tags = ["answer", "query_ask", "query_cmp", "query_ge"]

    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 8, "S": 3, "B": 0},
            2: {"n": 10, "S": 3, "B": 1},
            3: {"n": 12, "S": 4, "B": 2},
            4: {"n": 15, "S": 5, "B": 3},
            5: {"n": 20, "S": 6, "B": 4},
        },
        "en": {
            1: {"n": 8, "S": 3, "B": 0},
            2: {"n": 10, "S": 3, "B": 1},
            3: {"n": 12, "S": 4, "B": 2},
            4: {"n": 15, "S": 5, "B": 3},
            5: {"n": 20, "S": 6, "B": 4},
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
        self.n = cfg["n"]
        
        s_base = cfg["S"]
        self.S = random.randint(max(2, s_base - 1), s_base + 1)
        self.B = random.randint(0, self.S - 1)
        
        self._game_info["n"] = self.n
        self._game_info["n_minus_1"] = self.n - 1
        
        self.query_history = []

    def _compute_response(self, i, j):
        d = abs(i - j)
        return (d + self.B) // self.S

    def _validate_positions(self, i, j):
        if not (1 <= i <= self.n and 1 <= j <= self.n):
            return False
        if i == j:
            return False
        return True

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        ans_dict = {}
        parts = [p.strip() for p in raw_ans.split(",")]
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "S" not in ans_dict or "B" not in ans_dict:
            return False
        
        try:
            ans_S = int(ans_dict["S"])
            ans_B = int(ans_dict["B"])
        except ValueError:
            return False
        
        if ans_S < 2:
            return False
        if not (0 <= ans_B < ans_S):
            return False
        
        for query_type, query_data, response in self.query_history:
            if query_type == "ask":
                i, j = query_data
                expected = (abs(i - j) + ans_B) // ans_S
                if expected != response:
                    return False
            elif query_type == "cmp":
                i, j, p, q = query_data
                r1 = (abs(i - j) + ans_B) // ans_S
                r2 = (abs(p - q) + ans_B) // ans_S
                if r1 < r2:
                    expected = "lt"
                elif r1 == r2:
                    expected = "eq"
                else:
                    expected = "gt"
                if expected != response:
                    return False
            elif query_type == "ge":
                i, j, t = query_data
                r = (abs(i - j) + ans_B) // ans_S
                expected = r >= t
                if expected != response:
                    return False
        
        return ans_S == self.S and ans_B == self.B

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        query_tags_present = [tag for tag in ["query_ask", "query_cmp", "query_ge"] if tag in parsed_info]
        if len(query_tags_present) > 1:
            return ("错误：每次只能进行一个查询。" if lang == "zh" 
                    else "Error: Only one query per turn is allowed.")
        
        if "query_ask" in parsed_info:
            try:
                raw = parsed_info["query_ask"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                i, j = int(parts[0]), int(parts[1])
                
                if not self._validate_positions(i, j):
                    return "错误：位置编号无效或相同。" if lang == "zh" else "Error: Invalid or identical position numbers."
                
                result = self._compute_response(i, j)
                self.query_history.append(("ask", (i, j), result))
                return str(result)
            except (ValueError, IndexError, TypeError):
                return "错误：查询格式无效。" if lang == "zh" else "Error: Invalid query format."
        
        elif "query_cmp" in parsed_info:
            try:
                raw = parsed_info["query_cmp"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 4:
                    raise ValueError
                i, j, p, q = int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])
                
                if not (self._validate_positions(i, j) and self._validate_positions(p, q)):
                    return "错误：位置编号无效或相同。" if lang == "zh" else "Error: Invalid or identical position numbers."
                
                r1 = self._compute_response(i, j)
                r2 = self._compute_response(p, q)
                
                if r1 < r2:
                    result = "小于" if lang == "zh" else "less than"
                    result_code = "lt"
                elif r1 == r2:
                    result = "等于" if lang == "zh" else "equal to"
                    result_code = "eq"
                else:
                    result = "大于" if lang == "zh" else "greater than"
                    result_code = "gt"
                
                self.query_history.append(("cmp", (i, j, p, q), result_code))
                return result
            except (ValueError, IndexError, TypeError):
                return "错误：查询格式无效。" if lang == "zh" else "Error: Invalid query format."
        
        elif "query_ge" in parsed_info:
            try:
                raw = parsed_info["query_ge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 3:
                    raise ValueError
                i, j, t = int(parts[0]), int(parts[1]), int(parts[2])
                
                if not self._validate_positions(i, j):
                    return "错误：位置编号无效或相同。" if lang == "zh" else "Error: Invalid or identical position numbers."
                
                r = self._compute_response(i, j)
                result_bool = r >= t
                result = "是" if result_bool else "否"
                if lang == "en":
                    result = "yes" if result_bool else "no"
                
                self.query_history.append(("ge", (i, j, t), result_bool))
                return result
            except (ValueError, IndexError, TypeError):
                return "错误：查询格式无效。" if lang == "zh" else "Error: Invalid query format."
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        for d in range(1, self.n):
            i = 1
            j = 1 + d
            query_content = f"{i},{j}"
            answer_val = self._compute_response(i, j)
            answer_str = str(answer_val)
            
            queries.append({
                "query": f"<query_ask>{query_content}</query_ask>",
                "answer": answer_str
            })
            
        return queries

    def _cf_make_wrong(self, correct):
        if correct.lstrip('-').isdigit():
            val = int(correct)
            return str(val + 1) if val == 0 else str(val - 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"

        if correct == "小于":
            return "大于"
        if correct == "大于":
            return "小于"
        if correct == "等于":
            return "大于"

        if lower_correct == "less than":
            return "greater than"
        if lower_correct == "greater than":
            return "less than"
        if lower_correct == "equal to":
            return "greater than"

        return f"{correct}_WRONG"