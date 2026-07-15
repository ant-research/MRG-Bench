from .base import Game
import random

class PeriodicSequenceGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"周期识别问题"的推理游戏，规则如下：

游戏设定了一个固定但隐藏的序列 S，序列长度为 {n}，序列中的每个元素都是从符号集合 {{A, B, C, D}} 中选取的。

你的目标是判定这个序列是否存在非平凡周期。具体来说：
- 如果存在某个正整数 P（1 小于等于 P 小于 {n}），使得对于所有满足条件的位置 i（1 小于等于 i 小于等于 {n_minus_p}），都有 S[i] = S[i+P]，则称序列存在周期 P。
- 若存在这样的周期，你需要找出最小的那个周期值。
- 若不存在任何这样的周期，则称序列无非平凡周期。

你可以通过以下三种查询方式来获取信息（尽可能少地使用查询次数）：

1. **观察查询**：询问序列中第 i 个位置的符号是什么（1 小于等于 i 小于等于 {n}）。我会直接告诉你该位置的符号（A、B、C 或 D）。

2. **比较查询**：询问序列中第 i 个位置和第 j 个位置的符号是否相同（1 小于等于 i, j 小于等于 {n}，且 i 不等于 j）。我会回答"相同"或"不同"。

3. **验证周期查询**：询问某个正整数 p 是否为序列的周期（1 小于等于 p 小于 {n}）。我会回答"是"或"否"。注意：此类查询在整个游戏中最多只能使用 2 次。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 观察查询（例如询问第 3 个位置）：
<query_observe>3</query_observe>

- 比较查询（例如比较第 2 和第 5 个位置）：
<query_compare>2,5</query_compare>

- 验证周期查询（例如验证周期是否为 4）：
<query_verify>4</query_verify>

提交最终答案时，必须明确说明是否存在非平凡周期。格式如下：

- 若不存在非平凡周期：
<answer>no_period</answer>

- 若存在非平凡周期（例如最小周期为 3）：
<answer>period=3</answer>
"""

    game_rule_en = """\
Let's play a "Periodic Sequence Recognition" deduction game. Here are the rules:

There is a fixed but hidden sequence S of length {n}, where each element is chosen from the symbol set {{A, B, C, D}}.

Your goal is to determine whether this sequence has a non-trivial period. Specifically:
- If there exists a positive integer P (1 less than or equal to P less than {n}) such that for all valid positions i (1 less than or equal to i less than or equal to {n_minus_p}), S[i] = S[i+P], then the sequence has period P.
- If such a period exists, you need to find the minimum period value.
- If no such period exists, the sequence has no non-trivial period.

You can gather information through three types of queries (try to use as few queries as possible):

1. **Observe Query**: Ask for the symbol at position i in the sequence (1 less than or equal to i less than or equal to {n}). I will tell you the symbol at that position (A, B, C, or D).

2. **Compare Query**: Ask whether the symbols at position i and position j are the same (1 less than or equal to i, j less than or equal to {n}, and i not equal to j). I will answer "Same" or "Different".

3. **Verify Period Query**: Ask whether a positive integer p is a period of the sequence (1 less than or equal to p less than {n}). I will answer "Yes" or "No". Note: This type of query can be used at most 2 times throughout the game.

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Observe Query (e.g., asking about position 3):
<query_observe>3</query_observe>

- Compare Query (e.g., comparing positions 2 and 5):
<query_compare>2,5</query_compare>

- Verify Period Query (e.g., verifying if period is 4):
<query_verify>4</query_verify>

When submitting the final answer, you must clearly state whether a non-trivial period exists. Use this format:

- If no non-trivial period exists:
<answer>no_period</answer>

- If a non-trivial period exists (e.g., minimum period is 3):
<answer>period=3</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通控制系统记录了一段连续的时间序列 S，记录了某关键路口的交通调度策略，序列长度为 {n}，每个时间窗口的策略为 {{A, B, C, D}} 之一。

你的目标是判定该调度序列是否存在规律性的循环周期。具体来说：
- 如果存在某个正整数 P（1 小于等于 P 小于 {n}），使得对于所有满足条件的时间窗口 i（1 小于等于 i 小于等于 {n_minus_p}），都有 S[i] = S[i+P]，则称系统存在调度周期 P。
- 若存在，你需要找出最小的那个周期值。
- 若不存在，则称调度序列无非平凡周期。

你可以通过以下三种查询方式来获取信息（尽可能少地使用查询次数）：

1. **观察查询**：询问序列中第 i 个时间窗口的调度策略（1 小于等于 i 小于等于 {n}）。我会直接告诉你该位置的策略（A、B、C 或 D）。
2. **比较查询**：询问第 i 个和第 j 个时间窗口的策略是否相同（1 小于等于 i, j 小于等于 {n}，且 i 不等于 j）。我会回答"相同"或"不同"。
3. **验证周期查询**：询问某个正整数 p 是否为系统的调度周期（1 小于等于 p 小于 {n}）。我会回答"是"或"否"。注意：此类查询最多只能使用 2 次。

当你收集到足够信息后，请提交最终答案。若答案错误或格式不符，排查失败。

每次查询只能包含一个标签。请使用以下 XML 格式：
- 观察查询：<query_observe>3</query_observe>
- 比较查询：<query_compare>2,5</query_compare>
- 验证周期查询：<query_verify>4</query_verify>

提交最终答案时，必须明确说明是否存在非平凡周期。格式如下：
- 若不存在非平凡周期：<answer>no_period</answer>
- 若存在非平凡周期（例如最小周期为 3）：<answer>period=3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The intelligent traffic control system has recorded a continuous time sequence S of traffic dispatch strategies at a key intersection. The sequence length is {n}, and the strategy for each time window is chosen from {{A, B, C, D}}.

Your goal is to determine whether this dispatch sequence has a regular, non-trivial period. Specifically:
- If there exists a positive integer P (1 less than or equal to P less than {n}) such that for all valid time windows i (1 less than or equal to i less than or equal to {n_minus_p}), S[i] = S[i+P], then the system has a dispatch period P.
- If such a period exists, you need to find the minimum period value.
- If no such period exists, the sequence has no non-trivial period.

You can gather information through three types of queries (try to use as few queries as possible):

1. **Observe Query**: Ask for the strategy at time window i (1 less than or equal to i less than or equal to {n}). I will output A, B, C, or D.
2. **Compare Query**: Ask whether the strategies at time window i and j are the same (1 less than or equal to i, j less than or equal to {n}, and i not equal to j). I will output "Same" or "Different".
3. **Verify Period Query**: Ask whether a positive integer p is a dispatch period (1 less than or equal to p less than {n}). I will output "Yes" or "No". Note: This query can be used at most 2 times.

When you have enough information, submit your final answer. If wrong or invalid format, the diagnosis fails.

Each query must contain only one tag. Use the following XML format:
- Observe Query: <query_observe>3</query_observe>
- Compare Query: <query_compare>2,5</query_compare>
- Verify Period Query: <query_verify>4</query_verify>

Final answer format:
- If no non-trivial period exists: <answer>no_period</answer>
- If a non-trivial period exists (e.g., minimum period is 3): <answer>period=3</answer>
"""

    contextualized_rule_zh_2 = """\
作为临床医学研究员，你正在分析一名患者连续记录的神经生理电信号特征序列 S。序列总长度为 {n}，每次记录的波形特征被归类为 {{A, B, C, D}} 四种状态之一。

你的目标是判定该患者的神经电信号是否存在非平凡的发作周期。具体来说：
- 如果存在某个正整数 P（1 小于等于 P 小于 {n}），使得对于所有满足条件的记录位置 i（1 小于等于 i 小于等于 {n_minus_p}），都有 S[i] = S[i+P]，则称信号特征存在周期 P。
- 若存在这样的发作周期，你需要找出最小的那个周期值。
- 若不存在任何这样的周期，则称该特征序列无非平凡周期。

你可以通过以下三种查询方式来获取信息（尽可能少地使用查询次数）：

1. **观察查询**：询问序列中第 i 次记录的特征状态是什么（1 小于等于 i 小于等于 {n}）。我会直接告诉你（A、B、C 或 D）。
2. **比较查询**：询问第 i 次和第 j 次记录的特征是否相同（1 小于等于 i, j 小于等于 {n}，且 i 不等于 j）。我会回答"相同"或"不同"。
3. **验证周期查询**：询问某个正整数 p 是否为发作周期（1 小于等于 p 小于 {n}）。我会回答"是"或"否"。注意：此类查询在整个游戏中最多只能使用 2 次。

当你收集到足够信息后，请提交最终诊断结论。若答案错误或格式不符，分析失败。

每次查询只能包含一个标签。请使用以下 XML 格式：
- 观察查询：<query_observe>3</query_observe>
- 比较查询：<query_compare>2,5</query_compare>
- 验证周期查询：<query_verify>4</query_verify>

提交最终答案时，必须明确说明是否存在非平凡周期。格式如下：
- 若不存在非平凡周期：<answer>no_period</answer>
- 若存在非平凡周期（例如最小周期为 3）：<answer>period=3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
As a clinical medical researcher, you are analyzing a continuously recorded sequence S of a patient's neurophysiological electrical signal characteristics. The sequence length is {n}, and the waveform feature of each record is classified into one of four states: {{A, B, C, D}}.

Your goal is to determine whether these signal characteristics have a non-trivial attack period. Specifically:
- If there exists a positive integer P (1 less than or equal to P less than {n}) such that for all valid record positions i (1 less than or equal to i less than or equal to {n_minus_p}), S[i] = S[i+P], then the signal characteristics have a period P.
- If such an attack period exists, you need to find the minimum period value.
- If no such period exists, the sequence has no non-trivial period.

You can gather information through three types of queries (try to use as few queries as possible):

1. **Observe Query**: Ask for the characteristic state of the i-th record (1 less than or equal to i less than or equal to {n}). I will output A, B, C, or D.
2. **Compare Query**: Ask whether the characteristics of the i-th and j-th records are the same (1 less than or equal to i, j less than or equal to {n}, and i not equal to j). I will output "Same" or "Different".
3. **Verify Period Query**: Ask whether a positive integer p is an attack period (1 less than or equal to p less than {n}). I will output "Yes" or "No". Note: This query can be used at most 2 times.

When you have enough information, submit your final diagnosis. If wrong or invalid format, the analysis fails.

Each query must contain only one tag. Use the following XML format:
- Observe Query: <query_observe>3</query_observe>
- Compare Query: <query_compare>2,5</query_compare>
- Verify Period Query: <query_verify>4</query_verify>

Final answer format:
- If no non-trivial period exists: <answer>no_period</answer>
- If a non-trivial period exists (e.g., minimum period is 3): <answer>period=3</answer>
"""

    contextualized_rule_zh_3 = """\
智能辅导系统记录了一名学生在连续的学习模块中的认知专注度序列 S。序列总长度为 {n}，每个模块的专注度状态分为 {{A, B, C, D}} 四个不同等级。

你的目标是判定该学生的学习状态是否存在固定的循环周期。具体来说：
- 如果存在某个正整数 P（1 小于等于 P 小于 {n}），使得对于所有满足条件的学习模块 i（1 小于等于 i 小于等于 {n_minus_p}），都有 S[i] = S[i+P]，则称认知状态存在循环周期 P。
- 若存在这样的学习周期，你需要找出最小的那个周期值。
- 若不存在任何这样的周期，则称该专注度序列无非平凡周期。

你可以通过以下三种查询方式来获取信息（尽可能少地使用查询次数）：

1. **观察查询**：询问序列中第 i 个模块的专注度等级是什么（1 小于等于 i 小于等于 {n}）。我会直接告诉你该等级（A、B、C 或 D）。
2. **比较查询**：询问第 i 个和第 j 个模块的专注度等级是否相同（1 小于等于 i, j 小于等于 {n}，且 i 不等于 j）。我会回答"相同"或"不同"。
3. **验证周期查询**：询问某个正整数 p 是否为认知循环周期（1 小于等于 p 小于 {n}）。我会回答"是"或"否"。注意：此类查询在整个学习评估中最多只能使用 2 次。

当你收集到足够信息后，请提交最终结论。若答案错误或格式不符，评估失败。

每次查询只能包含一个标签。请使用以下 XML 格式：
- 观察查询：<query_observe>3</query_observe>
- 比较查询：<query_compare>2,5</query_compare>
- 验证周期查询：<query_verify>4</query_verify>

提交最终答案时，必须明确说明是否存在非平凡周期。格式如下：
- 若不存在非平凡周期：<answer>no_period</answer>
- 若存在非平凡周期（例如最小周期为 3）：<answer>period=3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The intelligent tutoring system has recorded a sequence S of a student's cognitive engagement across continuous learning modules. The total sequence length is {n}, and the engagement state for each module is categorized into four levels: {{A, B, C, D}}.

Your goal is to determine whether the student's learning state exhibits a fixed cyclic period. Specifically:
- If there exists a positive integer P (1 less than or equal to P less than {n}) such that for all valid modules i (1 less than or equal to i less than or equal to {n_minus_p}), S[i] = S[i+P], then the cognitive state has a cyclic period P.
- If such a learning period exists, you need to find the minimum period value.
- If no such period exists, the sequence has no non-trivial period.

You can gather information through three types of queries (try to use as few queries as possible):

1. **Observe Query**: Ask for the engagement level of the i-th module (1 less than or equal to i less than or equal to {n}). I will output A, B, C, or D.
2. **Compare Query**: Ask whether the engagement levels of the i-th and j-th modules are the same (1 less than or equal to i, j less than or equal to {n}, and i not equal to j). I will output "Same" or "Different".
3. **Verify Period Query**: Ask whether a positive integer p is a cyclic period (1 less than or equal to p less than {n}). I will output "Yes" or "No". Note: This query can be used at most 2 times.

When you have enough information, submit your final conclusion. If wrong or invalid format, the evaluation fails.

Each query must contain only one tag. Use the following XML format:
- Observe Query: <query_observe>3</query_observe>
- Compare Query: <query_compare>2,5</query_compare>
- Verify Period Query: <query_verify>4</query_verify>

Final answer format:
- If no non-trivial period exists: <answer>no_period</answer>
- If a non-trivial period exists (e.g., minimum period is 3): <answer>period=3</answer>
"""

    contextualized_rule_zh_4 = """\
工业物联网系统捕捉到了一台核心数控机床在连续作业时的振动模式序列 S。该序列长度为 {n}，每次作业的振动模式属于 {{A, B, C, D}} 四种诊断类型之一。

你的目标是分析该设备的运行是否存在异常的机械周期。具体来说：
- 如果存在某个正整数 P（1 小于等于 P 小于 {n}），使得对于所有满足条件的加工作业 i（1 小于等于 i 小于等于 {n_minus_p}），都有 S[i] = S[i+P]，则称机床存在机械运行周期 P。
- 若存在这样的运行周期，你需要找出最小的那个周期值。
- 若不存在任何这样的周期，则称设备的振动模式无非平凡周期。

你可以通过以下三种查询方式来获取机床数据（尽可能少地使用查询次数）：

1. **观察查询**：询问序列中第 i 次加工作业的振动模式（1 小于等于 i 小于等于 {n}）。我会直接告诉你（A、B、C 或 D）。
2. **比较查询**：询问第 i 次和第 j 次加工作业的振动模式是否相同（1 小于等于 i, j 小于等于 {n}，且 i 不等于 j）。我会回答"相同"或"不同"。
3. **验证周期查询**：询问某个正整数 p 是否为该机床的运行周期（1 小于等于 p 小于 {n}）。我会回答"是"或"否"。注意：此类查询在整个诊断中最多只能使用 2 次。

当你收集到足够信息后，请提交最终结论。若答案错误或格式不符，故障诊断失败。

每次查询只能包含一个标签。请使用以下 XML 格式：
- 观察查询：<query_observe>3</query_observe>
- 比较查询：<query_compare>2,5</query_compare>
- 验证周期查询：<query_verify>4</query_verify>

提交最终答案时，必须明确说明是否存在非平凡周期。格式如下：
- 若不存在非平凡周期：<answer>no_period</answer>
- 若存在非平凡周期（例如最小周期为 3）：<answer>period=3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
The Industrial IoT system has captured a vibration pattern sequence S of a core CNC machine during continuous operation. The sequence length is {n}, and the vibration pattern of each operation belongs to one of four diagnostic types: {{A, B, C, D}}.

Your goal is to determine whether the equipment's operation exhibits an abnormal mechanical period. Specifically:
- If there exists a positive integer P (1 less than or equal to P less than {n}) such that for all valid operations i (1 less than or equal to i less than or equal to {n_minus_p}), S[i] = S[i+P], then the machine has a mechanical operation period P.
- If such an operation period exists, you need to find the minimum period value.
- If no such period exists, the sequence has no non-trivial period.

You can gather information through three types of queries (try to use as few queries as possible):

1. **Observe Query**: Ask for the vibration pattern of the i-th operation (1 less than or equal to i less than or equal to {n}). I will output A, B, C, or D.
2. **Compare Query**: Ask whether the patterns of the i-th and j-th operations are the same (1 less than or equal to i, j less than or equal to {n}, and i not equal to j). I will output "Same" or "Different".
3. **Verify Period Query**: Ask whether a positive integer p is a mechanical operation period (1 less than or equal to p less than {n}). I will output "Yes" or "No". Note: This query can be used at most 2 times.

When you have enough information, submit your final conclusion. If wrong or invalid format, the diagnosis fails.

Each query must contain only one tag. Use the following XML format:
- Observe Query: <query_observe>3</query_observe>
- Compare Query: <query_compare>2,5</query_compare>
- Verify Period Query: <query_verify>4</query_verify>

Final answer format:
- If no non-trivial period exists: <answer>no_period</answer>
- If a non-trivial period exists (e.g., minimum period is 3): <answer>period=3</answer>
"""

    contextualized_rule_zh_5 = """\
你作为合规调查员，正在审查某高风险企业提交的连续业务交易状态序列 S。该序列包含 {n} 个交易记录，每个记录的合规审查结果被标记为 {{A, B, C, D}} 四类风险级别之一。

你的目标是判定该企业的交易行为是否存在掩人耳目的规律性周期。具体来说：
- 如果存在某个正整数 P（1 小于等于 P 小于 {n}），使得对于所有满足条件的交易记录 i（1 小于等于 i 小于等于 {n_minus_p}），都有 S[i] = S[i+P]，则称该交易序列存在风险周期 P。
- 若存在这样的风险行为周期，你需要找出最小的那个周期值。
- 若不存在任何这样的周期，则称交易序列无非平凡周期。

你可以通过以下三种查询方式来获取取证信息（尽可能少地使用查询次数）：

1. **观察查询**：询问序列中第 i 笔交易的风险级别（1 小于等于 i 小于等于 {n}）。我会直接告诉你（A、B、C 或 D）。
2. **比较查询**：询问第 i 笔和第 j 笔交易的风险级别是否相同（1 小于等于 i, j 小于等于 {n}，且 i 不等于 j）。我会回答"相同"或"不同"。
3. **验证周期查询**：询问某个正整数 p 是否为该企业的风险周期（1 小于等于 p 小于 {n}）。我会回答"是"或"否"。注意：此类查询在整个调查中最多只能使用 2 次。

当你收集到足够信息后，请提交最终调查结论。若答案错误或格式不符，合规审查失败。

每次查询只能包含一个标签。请使用以下 XML 格式：
- 观察查询：<query_observe>3</query_observe>
- 比较查询：<query_compare>2,5</query_compare>
- 验证周期查询：<query_verify>4</query_verify>

提交最终答案时，必须明确说明是否存在非平凡周期。格式如下：
- 若不存在非平凡周期：<answer>no_period</answer>
- 若存在非平凡周期（例如最小周期为 3）：<answer>period=3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
As a compliance investigator, you are reviewing a continuous business transaction status sequence S submitted by a high-risk enterprise. The sequence contains {n} transaction records, and the compliance review result of each record is marked as one of four risk levels: {{A, B, C, D}}.

Your goal is to determine whether the enterprise's transaction behavior exhibits a deceptive regular period. Specifically:
- If there exists a positive integer P (1 less than or equal to P less than {n}) such that for all valid transaction records i (1 less than or equal to i less than or equal to {n_minus_p}), S[i] = S[i+P], then the transaction sequence has a risk period P.
- If such a behavior period exists, you need to find the minimum period value.
- If no such period exists, the sequence has no non-trivial period.

You can gather information through three types of queries (try to use as few queries as possible):

1. **Observe Query**: Ask for the risk level of the i-th transaction (1 less than or equal to i less than or equal to {n}). I will output A, B, C, or D.
2. **Compare Query**: Ask whether the risk levels of the i-th and j-th transactions are the same (1 less than or equal to i, j less than or equal to {n}, and i not equal to j). I will output "Same" or "Different".
3. **Verify Period Query**: Ask whether a positive integer p is a risk period (1 less than or equal to p less than {n}). I will output "Yes" or "No". Note: This query can be used at most 2 times.

When you have enough information, submit your final investigation conclusion. If wrong or invalid format, the compliance review fails.

Each query must contain only one tag. Use the following XML format:
- Observe Query: <query_observe>3</query_observe>
- Compare Query: <query_compare>2,5</query_compare>
- Verify Period Query: <query_verify>4</query_verify>

Final answer format:
- If no non-trivial period exists: <answer>no_period</answer>
- If a non-trivial period exists (e.g., minimum period is 3): <answer>period=3</answer>
"""

    tags = ["answer", "query_observe", "query_compare", "query_verify"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "sequence": "A,B,A,B,A,B,A,B",
                "has_period": True,
                "min_period": 2,
            },
            2: {
                "n": 10,
                "sequence": "A,B,C,D,A,A,B,C,D,A",
                "has_period": True,
                "min_period": 5,
            },
            3: {
                "n": 12,
                "sequence": "A,B,C,A,B,C,A,B,C,A,B,C",
                "has_period": True,
                "min_period": 3,
            },
            4: {
                "n": 15,
                "sequence": "A,B,C,D,A,B,C,A,D,B,C,A,B,D,C",
                "has_period": False,
                "min_period": None,
            },
            5: {
                "n": 16,
                "sequence": "A,B,C,D,A,B,A,B,C,D,A,B,A,B,C,D",
                "has_period": True,
                "min_period": 6,
            },
        },
        "en": {
            1: {
                "n": 8,
                "sequence": "A,B,A,B,A,B,A,B",
                "has_period": True,
                "min_period": 2,
            },
            2: {
                "n": 10,
                "sequence": "A,B,C,D,A,A,B,C,D,A",
                "has_period": True,
                "min_period": 5,
            },
            3: {
                "n": 12,
                "sequence": "A,B,C,A,B,C,A,B,C,A,B,C",
                "has_period": True,
                "min_period": 3,
            },
            4: {
                "n": 15,
                "sequence": "A,B,C,D,A,B,C,A,D,B,C,A,B,D,C",
                "has_period": False,
                "min_period": None,
            },
            5: {
                "n": 16,
                "sequence": "A,B,C,D,A,B,A,B,C,D,A,B,A,B,C,D",
                "has_period": True,
                "min_period": 6,
            },
        },
    }

    def __init__(self, config):
        self.verify_count = 0
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
        self._game_info["n_minus_p"] = "N-P"
        
        self.sequence = [s.strip() for s in cfg["sequence"].split(",")]
        self.has_period = cfg["has_period"]
        self.min_period = cfg["min_period"]
        
        if len(self.sequence) != cfg["n"]:
            raise ValueError(f"Sequence length mismatch: expected {cfg['n']}, got {len(self.sequence)}")

    def _is_valid_period(self, p):
        n = len(self.sequence)
        if p <= 0 or p >= n:
            return False
        
        for i in range(n - p):
            if self.sequence[i] != self.sequence[i + p]:
                return False
        return True

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        if raw_ans.lower() == "no_period":
            return not self.has_period
        
        if raw_ans.lower().startswith("period="):
            try:
                period_str = raw_ans.split("=", 1)[1].strip()
                claimed_period = int(period_str)
                
                if not self.has_period:
                    return False
                
                return claimed_period == self.min_period
            except:
                return False
        
        return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            same_res, diff_res = "相同", "不同"
            yes_res, no_res = "是", "否"
            err_range = "错误：位置超出范围。"
            err_format = "错误：格式无效。"
            err_verify_limit = "错误：验证周期查询次数已达上限（最多2次）。"
        else:
            same_res, diff_res = "Same", "Different"
            yes_res, no_res = "Yes", "No"
            err_range = "Error: Position out of range."
            err_format = "Error: Invalid format."
            err_verify_limit = "Error: Verify period query limit reached (maximum 2 times)."

        n = len(self.sequence)

        if "query_observe" in parsed_info:
            try:
                pos_str = parsed_info["query_observe"].strip()
                pos = int(pos_str)
                if pos < 1 or pos > n:
                    return err_range
                return self.sequence[pos - 1]
            except:
                return err_format

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return err_format
                i, j = int(parts[0]), int(parts[1])
                if i < 1 or i > n or j < 1 or j > n or i == j:
                    return err_range
                return same_res if self.sequence[i - 1] == self.sequence[j - 1] else diff_res
            except:
                return err_format

        elif "query_verify" in parsed_info:
            if self.verify_count >= 2:
                return err_verify_limit
            
            try:
                p_str = parsed_info["query_verify"].strip()
                p = int(p_str)
                if p < 1 or p >= n:
                    return err_range
                
                self.verify_count += 1
                
                is_period = self._is_valid_period(p)
                return yes_res if is_period else no_res
            except:
                return err_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if self.config.language == "zh":
            same_res, diff_res = "相同", "不同"
            yes_res, no_res = "是", "否"
            symbol_set = ["A", "B", "C", "D"]
        else:
            same_res, diff_res = "Same", "Different"
            yes_res, no_res = "Yes", "No"
            symbol_set = ["A", "B", "C", "D"]

        if correct in symbol_set:
            wrong_choices = [s for s in symbol_set if s != correct]
            return random.choice(wrong_choices)

        if correct == same_res:
            return diff_res
        if correct == diff_res:
            return same_res

        if correct == yes_res:
            return no_res
        if correct == no_res:
            return yes_res

        return correct + " [WRONG]"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        n = len(self.sequence)
        
        if self.config.language == "zh":
            same_res, diff_res = "相同", "不同"
            yes_res, no_res = "是", "否"
        else:
            same_res, diff_res = "Same", "Different"
            yes_res, no_res = "Yes", "No"

        for i in range(1, n + 1):
            results.append({
                "query": f"<query_observe>{i}</query_observe>",
                "answer": self.sequence[i - 1]
            })

        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                ans = same_res if self.sequence[i - 1] == self.sequence[j - 1] else diff_res
                results.append({
                    "query": f"<query_compare>{i},{j}</query_compare>",
                    "answer": ans
                })

        for p in range(1, n):
            is_period = self._is_valid_period(p)
            ans = yes_res if is_period else no_res
            results.append({
                "query": f"<query_verify>{p}</query_verify>",
                "answer": ans
            })

        return results