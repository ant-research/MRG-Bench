import random
from .base import Game

class SequencePeriodGame(Game):

    game_rule_zh = """\
我们来玩一个"序列周期推理"游戏，规则如下：

游戏设定了一条长度为 N = {n} 的未知序列 S，索引范围为 [1, N]。序列中的每个元素都是四种符号之一（用 A、B、C、D 表示，仅作为可区分的符号）。

你的目标是判定这条序列是否存在周期性：
- 若存在整数 k（1 小于等于 k 小于 N），使得对所有位置 i（1 小于等于 i 小于等于 N-k），都有 S[i] = S[i+k]，则称序列存在周期性。
- 若存在周期性，你需要找出最小的这样的 k；若不存在周期性，你需要给出否定结论。

你可以通过以下五种方式向我提问（每轮可提出一个问题），我会根据真实序列如实回答：

1. 单点查看（整个游戏中最多使用 3 次）：询问位置 i 的具体符号是什么。
2. 两点相同性判断：询问位置 i 和位置 j 的符号是否相同。
3. 窗口一致性判断：询问从位置 i 开始长度为 w 的区间，与从位置 j 开始长度为 w 的区间，是否逐位完全一致。
4. 窗口差异计数：询问从位置 i 开始长度为 w 的区间，与从位置 j 开始长度为 w 的区间，逐位比较有多少个位置不同（汉明距离）。
5. 周期候选验证（使用次数不限）：询问某个整数 k 是否为序列的一个周期。

注意：
- 所有位置索引必须在 [1, {n}] 范围内。
- 窗口查询时，窗口不能越界，即 i + w - 1 和 j + w - 1 都必须小于等于 {n}。
- 周期候选验证中，k 必须满足 1 小于等于 k 小于 {n}。
- 越界或格式错误的提问会得到错误提示，但不计入单点查看次数。

每次只能提一个问题，使用以下 XML 格式：

- 单点查看（例如查看位置 5）：
<query_view>5</query_view>

- 两点相同性判断（例如询问位置 2 和位置 7）：
<query_same>2,7</query_same>

- 窗口一致性判断（例如询问位置 1 开始长度 3 的窗口与位置 4 开始长度 3 的窗口）：
<query_window>1,4,3</query_window>

- 窗口差异计数（例如询问位置 1 开始长度 5 的窗口与位置 6 开始长度 5 的窗口）：
<query_diff>1,6,5</query_diff>

- 周期候选验证（例如验证 k=3 是否为周期）：
<query_period>3</query_period>

当你收集到足够信息后，提交最终结论，格式如下：

- 若存在周期性（例如最小周期为 4）：
<answer>periodic=yes,min_period=4</answer>

- 若不存在周期性：
<answer>periodic=no,min_period=none</answer>

请使用尽可能少的提问次数找出答案。若答案错误、格式不符或单点查看超过 3 次，游戏失败。
"""

    game_rule_en = """\
Let's play a "Sequence Periodicity Inference" game. Here are the rules:

There is a hidden sequence S of length N = {n}, indexed from 1 to N. Each element in the sequence is one of four symbols (represented as A, B, C, D).

Your goal is to determine whether the sequence has periodicity:
- If there exists an integer k (1 less than or equal to k less than N) such that for all positions i (1 less than or equal to i less than or equal to N-k), we have S[i] = S[i+k], then the sequence is periodic.
- If periodic, find the minimum such k; otherwise, conclude that it is not periodic.

You can ask me questions using the following five types (one question per turn), and I will answer truthfully based on the real sequence:

1. View Single Position (at most 3 times in total): Ask for the specific symbol at position i.
2. Check Two Positions: Ask whether positions i and j have the same symbol.
3. Window Equality Check: Ask whether the window [i, i+w-1] is identical to the window [j, j+w-1] position by position.
4. Window Difference Count: Ask for the Hamming distance between windows [i, i+w-1] and [j, j+w-1].
5. Period Candidate Verification (unlimited): Ask whether a given integer k is a period of the sequence.

Notes:
- All position indices must be in the range [1, {n}].
- For window queries, windows must not exceed bounds: i + w - 1 and j + w - 1 must both be less than or equal to {n}.
- For period verification, k must satisfy 1 less than or equal to k less than {n}.
- Out-of-bounds or malformed queries will receive error messages but won't count toward the single-view limit.

Each turn allows only one question. Use the following XML format:

- View Single Position (e.g., position 5):
<query_view>5</query_view>

- Check Two Positions (e.g., positions 2 and 7):
<query_same>2,7</query_same>

- Window Equality Check (e.g., window starting at 1 with length 3 vs. window starting at 4 with length 3):
<query_window>1,4,3</query_window>

- Window Difference Count (e.g., window starting at 1 with length 5 vs. window starting at 6 with length 5):
<query_diff>1,6,5</query_diff>

- Period Candidate Verification (e.g., check if k=3 is a period):
<query_period>3</query_period>

When you have enough information, submit your final conclusion:

- If periodic (e.g., minimum period is 4):
<answer>periodic=yes,min_period=4</answer>

- If not periodic:
<answer>periodic=no,min_period=none</answer>

Try to use as few queries as possible. The game fails if the answer is incorrect, format is invalid, or single-view queries exceed 3 times.
"""

    contextualized_rule_zh_1 = """\
“交通信号波浪模式分析”系统已启动。

系统正在监测一条主干道上的 N = {n} 个连续路口，索引范围为 [1, {n}]。每个路口的交通流状态呈现四种相位特征之一（用 A、B、C、D 表示，仅作为可区分的符号）。

你的目标是判定该干道的交通流是否形成了周期性：
- 若存在整数 k（1 小于等于 k 小于 {n}），使得对所有路口 i（1 小于等于 i 小于等于 {n}-k），都有 S[i] = S[i+k]，则称系统存在周期性。
- 若存在周期性，你需要找出最小的这样的 k；若不存在周期性，你需要给出否定结论。

你可以通过以下五种方式向我提问（每轮可提出一个问题），我会根据真实序列如实回答：

1. 单点查看（整个排查中最多使用 3 次）：询问路口 i 的具体状态是什么。
2. 两点相同性判断：询问路口 i 和路口 j 的状态是否相同。
3. 窗口一致性判断：询问从路口 i 开始长度为 w 的路段，与从路口 j 开始长度为 w 的路段，是否逐个路口完全一致。
4. 窗口差异计数：询问从路口 i 开始长度为 w 的路段，与从路口 j 开始长度为 w 的路段，逐个路口比较有多少个状态不同（汉明距离）。
5. 周期候选验证（使用次数不限）：询问某个整数 k 是否为该干道交通状态的一个周期。

注意：
- 所有路口索引必须在 [1, {n}] 范围内。
- 窗口查询时，窗口不能越界，即 i + w - 1 和 j + w - 1 都必须小于等于 {n}。
- 周期候选验证中，k 必须满足 1 小于等于 k 小于 {n}。
- 越界或格式错误的提问会得到错误提示，但不计入单点查看次数。

每次只能提一个问题，使用以下 XML 格式：

- 单点查看（例如查看路口 5）：
<query_view>5</query_view>

- 两点相同性判断（例如询问路口 2 和路口 7）：
<query_same>2,7</query_same>

- 窗口一致性判断（例如询问路口 1 开始长度 3 的路段与路口 4 开始长度 3 的路段）：
<query_window>1,4,3</query_window>

- 窗口差异计数（例如询问路口 1 开始长度 5 的路段与路口 6 开始长度 5 的路段）：
<query_diff>1,6,5</query_diff>

- 周期候选验证（例如验证 k=3 是否为周期）：
<query_period>3</query_period>

当你收集到足够信息后，提交最终结论，格式如下：

- 若存在周期性（例如最小周期为 4）：
<answer>periodic=yes,min_period=4</answer>

- 若不存在周期性：
<answer>periodic=no,min_period=none</answer>

请使用尽可能少的提问次数找出答案。若答案错误、格式不符或单点查看超过 3 次，排查失败。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
The "Traffic Signal Wave Pattern Analysis" system is online.

There is a sequence S representing N = {n} consecutive intersections along an arterial road, indexed from 1 to {n}. The traffic flow state at each intersection exhibits one of four phase characteristics (represented as A, B, C, D, purely as distinguishable symbols).

Your goal is to determine whether the sequence of traffic states has periodicity:
- If there exists an integer k (1 less than or equal to k less than {n}) such that for all positions i (1 less than or equal to i less than or equal to {n}-k), we have S[i] = S[i+k], then the traffic sequence is periodic.
- If periodic, find the minimum such k; otherwise, conclude that it is not periodic.

You can ask me questions using the following five types (one question per turn), and I will answer truthfully based on the real sequence:

1. View Single Position (at most 3 times in total): Ask for the specific phase characteristic at intersection i.
2. Check Two Positions: Ask whether intersections i and j have the same state.
3. Window Equality Check: Ask whether the road segment starting at i with length w is identical to the road segment starting at j with length w, intersection by intersection.
4. Window Difference Count: Ask for the Hamming distance (number of differing intersections) between the road segment starting at i with length w and the road segment starting at j with length w.
5. Period Candidate Verification (unlimited): Ask whether a given integer k is a period of the traffic sequence.

Notes:
- All intersection indices must be in the range [1, {n}].
- For window queries, segments must not exceed bounds: i + w - 1 and j + w - 1 must both be less than or equal to {n}.
- For period verification, k must satisfy 1 less than or equal to k less than {n}.
- Out-of-bounds or malformed queries will receive error messages but won't count toward the single-view limit.

Each turn allows only one question. Use the following XML format:

- View Single Position (e.g., view intersection 5):
<query_view>5</query_view>

- Check Two Positions (e.g., check intersections 2 and 7):
<query_same>2,7</query_same>

- Window Equality Check (e.g., segment starting at 1 with length 3 vs. segment starting at 4 with length 3):
<query_window>1,4,3</query_window>

- Window Difference Count (e.g., segment starting at 1 with length 5 vs. segment starting at 6 with length 5):
<query_diff>1,6,5</query_diff>

- Period Candidate Verification (e.g., check if k=3 is a period):
<query_period>3</query_period>

When you have enough information, submit your final conclusion:

- If periodic (e.g., minimum period is 4):
<answer>periodic=yes,min_period=4</answer>

- If not periodic:
<answer>periodic=no,min_period=none</answer>

Try to use as few queries as possible. The task fails if the answer is incorrect, format is invalid, or single-view queries exceed 3 times.
"""

    contextualized_rule_zh_2 = """\
“基因序列微卫星重复检测”任务已建立。

你面对的是一条长度为 N = {n} 的未知 DNA 标志物序列 S，索引范围为 [1, {n}]。序列上的每个位点表现为四种碱基多态性状态之一（用 A、B、C、D 表示，仅作为可区分的符号）。

你的目标是判定该基因序列是否存在周期性（串联重复）：
- 若存在整数 k（1 小于等于 k 小于 {n}），使得对所有位点 i（1 小于等于 i 小于等于 {n}-k），都有 S[i] = S[i+k]，则称序列存在周期性。
- 若存在周期性，你需要找出最小的这样的 k；若不存在周期性，你需要给出否定结论。

你可以通过以下五种方式向我提问（每轮可提出一个问题），我会根据真实序列如实回答：

1. 单点查看（整个诊断中最多使用 3 次）：询问位点 i 的具体多态性状态是什么。
2. 两点相同性判断：询问位点 i 和位点 j 的状态是否相同。
3. 窗口一致性判断：询问从位点 i 开始长度为 w 的基因片段，与从位点 j 开始长度为 w 的基因片段，是否逐个位点完全一致。
4. 窗口差异计数：询问从位点 i 开始长度为 w 的基因片段，与从位点 j 开始长度为 w 的基因片段，逐个位点比较有多少个状态不同（汉明距离）。
5. 周期候选验证（使用次数不限）：询问某个整数 k 是否为该基因序列的一个重复周期。

注意：
- 所有位点索引必须在 [1, {n}] 范围内。
- 窗口查询时，片段不能越界，即 i + w - 1 和 j + w - 1 都必须小于等于 {n}。
- 周期候选验证中，k 必须满足 1 小于等于 k 小于 {n}。
- 越界或格式错误的提问会得到错误提示，但不计入单点查看次数。

每次只能提一个问题，使用以下 XML 格式：

- 单点查看（例如测序位点 5）：
<query_view>5</query_view>

- 两点相同性判断（例如比对位点 2 和位点 7）：
<query_same>2,7</query_same>

- 窗口一致性判断（例如比对位点 1 开始长度 3 的片段与位点 4 开始长度 3 的片段）：
<query_window>1,4,3</query_window>

- 窗口差异计数（例如比对位点 1 开始长度 5 的片段与位点 6 开始长度 5 的片段）：
<query_diff>1,6,5</query_diff>

- 周期候选验证（例如验证 k=3 是否为重复周期）：
<query_period>3</query_period>

当你收集到足够信息后，提交最终诊断结论，格式如下：

- 若存在周期性（例如最小周期为 4）：
<answer>periodic=yes,min_period=4</answer>

- 若不存在周期性：
<answer>periodic=no,min_period=none</answer>

请使用尽可能少的提问次数找出答案。若答案错误、格式不符或单点查看超过 3 次，诊断失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The "Gene Sequence Microsatellite Repeat Detection" task is established.

You are analyzing an unknown DNA marker sequence S of length N = {n}, indexed from 1 to {n}. Each locus on the sequence exhibits one of four base polymorphism states (represented as A, B, C, D, purely as distinguishable symbols).

Your goal is to determine whether the genetic sequence has periodicity (tandem repeats):
- If there exists an integer k (1 less than or equal to k less than {n}) such that for all loci i (1 less than or equal to i less than or equal to {n}-k), we have S[i] = S[i+k], then the sequence is periodic.
- If periodic, find the minimum such k; otherwise, conclude that it is not periodic.

You can ask me questions using the following five types (one question per turn), and I will answer truthfully based on the real sequence:

1. View Single Position (at most 3 times in total): Ask for the specific polymorphism state at locus i.
2. Check Two Positions: Ask whether loci i and j have the same state.
3. Window Equality Check: Ask whether the gene fragment starting at i with length w is identical to the gene fragment starting at j with length w, locus by locus.
4. Window Difference Count: Ask for the Hamming distance (number of differing loci) between the gene fragment starting at i with length w and the gene fragment starting at j with length w.
5. Period Candidate Verification (unlimited): Ask whether a given integer k is a repeat period of the genetic sequence.

Notes:
- All locus indices must be in the range [1, {n}].
- For window queries, fragments must not exceed bounds: i + w - 1 and j + w - 1 must both be less than or equal to {n}.
- For period verification, k must satisfy 1 less than or equal to k less than {n}.
- Out-of-bounds or malformed queries will receive error messages but won't count toward the single-view limit.

Each turn allows only one question. Use the following XML format:

- View Single Position (e.g., sequence locus 5):
<query_view>5</query_view>

- Check Two Positions (e.g., match loci 2 and 7):
<query_same>2,7</query_same>

- Window Equality Check (e.g., fragment starting at 1 with length 3 vs. fragment starting at 4 with length 3):
<query_window>1,4,3</query_window>

- Window Difference Count (e.g., fragment starting at 1 with length 5 vs. fragment starting at 6 with length 5):
<query_diff>1,6,5</query_diff>

- Period Candidate Verification (e.g., check if k=3 is a repeat period):
<query_period>3</query_period>

When you have enough information, submit your final diagnosis:

- If periodic (e.g., minimum period is 4):
<answer>periodic=yes,min_period=4</answer>

- If not periodic:
<answer>periodic=no,min_period=none</answer>

Try to use as few queries as possible. The task fails if the answer is incorrect, format is invalid, or single-view queries exceed 3 times.
"""

    contextualized_rule_zh_3 = """\
“学生行为状态周期性评估”系统已启动。

系统记录了某学生连续 N = {n} 周的学习行为数据 S，索引范围为 [1, {n}]。每周的学习状态被归类为四种效能等级之一（用 A、B、C、D 表示，仅作为可区分的符号）。

你的目标是判定该学生的学习状态是否存在周期性循环：
- 若存在整数 k（1 小于等于 k 小于 {n}），使得对所有周次 i（1 小于等于 i 小于等于 {n}-k），都有 S[i] = S[i+k]，则称学习状态存在周期性。
- 若存在周期性，你需要找出最小的这样的 k；若不存在周期性，你需要给出否定结论。

你可以通过以下五种方式向我提问（每轮可提出一个问题），我会根据真实数据如实回答：

1. 单点查看（整个评估中最多使用 3 次）：询问第 i 周的具体效能等级是什么。
2. 两点相同性判断：询问第 i 周和第 j 周的效能等级是否相同。
3. 窗口一致性判断：询问从第 i 周开始长度为 w 的学习阶段，与从第 j 周开始长度为 w 的学习阶段，是否逐周完全一致。
4. 窗口差异计数：询问从第 i 周开始长度为 w 的学习阶段，与从第 j 周开始长度为 w 的学习阶段，逐周比较有多少个效能等级不同（汉明距离）。
5. 周期候选验证（使用次数不限）：询问某个整数 k 是否为该学生学习状态的一个循环周期。

注意：
- 所有周次索引必须在 [1, {n}] 范围内。
- 窗口查询时，学习阶段不能越界，即 i + w - 1 和 j + w - 1 都必须小于等于 {n}。
- 周期候选验证中，k 必须满足 1 小于等于 k 小于 {n}。
- 越界或格式错误的提问会得到错误提示，但不计入单点查看次数。

每次只能提一个问题，使用以下 XML 格式：

- 单点查看（例如查看第 5 周）：
<query_view>5</query_view>

- 两点相同性判断（例如询问第 2 周和第 7 周）：
<query_same>2,7</query_same>

- 窗口一致性判断（例如询问第 1 周开始长度 3 的阶段与第 4 周开始长度 3 的阶段）：
<query_window>1,4,3</query_window>

- 窗口差异计数（例如询问第 1 周开始长度 5 的阶段与第 6 周开始长度 5 的阶段）：
<query_diff>1,6,5</query_diff>

- 周期候选验证（例如验证 k=3 是否为循环周期）：
<query_period>3</query_period>

当你收集到足够信息后，提交最终评估结论，格式如下：

- 若存在周期性（例如最小周期为 4）：
<answer>periodic=yes,min_period=4</answer>

- 若不存在周期性：
<answer>periodic=no,min_period=none</answer>

请使用尽可能少的提问次数找出答案。若答案错误、格式不符或单点查看超过 3 次，评估失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The "Student Behavior Periodicity Assessment" system is initialized.

The system recorded a student's learning behavior data S for N = {n} consecutive weeks, indexed from 1 to {n}. Each week's learning state is classified into one of four efficacy levels (represented as A, B, C, D, purely as distinguishable symbols).

Your goal is to determine whether the student's learning state sequence has periodicity:
- If there exists an integer k (1 less than or equal to k less than {n}) such that for all weeks i (1 less than or equal to i less than or equal to {n}-k), we have S[i] = S[i+k], then the learning sequence is periodic.
- If periodic, find the minimum such k; otherwise, conclude that it is not periodic.

You can ask me questions using the following five types (one question per turn), and I will answer truthfully based on the real data:

1. View Single Position (at most 3 times in total): Ask for the specific efficacy level at week i.
2. Check Two Positions: Ask whether week i and week j have the same level.
3. Window Equality Check: Ask whether the learning phase starting at i with length w is identical to the phase starting at j with length w, week by week.
4. Window Difference Count: Ask for the Hamming distance (number of differing weeks) between the learning phase starting at i with length w and the phase starting at j with length w.
5. Period Candidate Verification (unlimited): Ask whether a given integer k is a cycle period of the learning state.

Notes:
- All week indices must be in the range [1, {n}].
- For window queries, phases must not exceed bounds: i + w - 1 and j + w - 1 must both be less than or equal to {n}.
- For period verification, k must satisfy 1 less than or equal to k less than {n}.
- Out-of-bounds or malformed queries will receive error messages but won't count toward the single-view limit.

Each turn allows only one question. Use the following XML format:

- View Single Position (e.g., view week 5):
<query_view>5</query_view>

- Check Two Positions (e.g., check week 2 and week 7):
<query_same>2,7</query_same>

- Window Equality Check (e.g., phase starting at 1 with length 3 vs. phase starting at 4 with length 3):
<query_window>1,4,3</query_window>

- Window Difference Count (e.g., phase starting at 1 with length 5 vs. phase starting at 6 with length 5):
<query_diff>1,6,5</query_diff>

- Period Candidate Verification (e.g., check if k=3 is a cycle period):
<query_period>3</query_period>

When you have enough information, submit your final assessment:

- If periodic (e.g., minimum period is 4):
<answer>periodic=yes,min_period=4</answer>

- If not periodic:
<answer>periodic=no,min_period=none</answer>

Try to use as few queries as possible. The task fails if the answer is incorrect, format is invalid, or single-view queries exceed 3 times.
"""

    contextualized_rule_zh_4 = """\
“自动化流水线缺陷周期排查”任务已分配。

当前批次生产了 N = {n} 个连续的精密部件 S，索引范围为 [1, {n}]。每个部件经过质检，被判定为四种质量特征类型之一（用 A、B、C、D 表示，仅作为可区分的符号）。

你的目标是查明该流水线机器的质量特征是否存在周期性偏差：
- 若存在整数 k（1 小于等于 k 小于 {n}），使得对所有部件 i（1 小于等于 i 小于等于 {n}-k），都有 S[i] = S[i+k]，则称生产质量存在周期性。
- 若存在周期性，你需要找出最小的这样的 k；若不存在周期性，你需要给出否定结论。

你可以通过以下五种方式向我提问（每轮可提出一个问题），我会根据真实批次如实回答：

1. 单点查看（整个排查中最多使用 3 次）：询问部件 i 的具体质量特征是什么。
2. 两点相同性判断：询问部件 i 和部件 j 的质量特征是否相同。
3. 窗口一致性判断：询问从部件 i 开始长度为 w 的连续生产段，与从部件 j 开始长度为 w 的连续生产段，是否逐件完全一致。
4. 窗口差异计数：询问从部件 i 开始长度为 w 的连续生产段，与从部件 j 开始长度为 w 的连续生产段，逐件比较有多少个质量特征不同（汉明距离）。
5. 周期候选验证（使用次数不限）：询问某个整数 k 是否为该流水线生产特征的一个周期。

注意：
- 所有部件索引必须在 [1, {n}] 范围内。
- 窗口查询时，连续生产段不能越界，即 i + w - 1 和 j + w - 1 都必须小于等于 {n}。
- 周期候选验证中，k 必须满足 1 小于等于 k 小于 {n}。
- 越界或格式错误的提问会得到错误提示，但不计入单点查看次数。

每次只能提一个问题，使用以下 XML 格式：

- 单点查看（例如抽检部件 5）：
<query_view>5</query_view>

- 两点相同性判断（例如询问部件 2 和部件 7）：
<query_same>2,7</query_same>

- 窗口一致性判断（例如询问部件 1 开始长度 3 的生产段与部件 4 开始长度 3 的生产段）：
<query_window>1,4,3</query_window>

- 窗口差异计数（例如询问部件 1 开始长度 5 的生产段与部件 6 开始长度 5 的生产段）：
<query_diff>1,6,5</query_diff>

- 周期候选验证（例如验证 k=3 是否为特征周期）：
<query_period>3</query_period>

当你收集到足够信息后，提交最终排查结论，格式如下：

- 若存在周期性（例如最小周期为 4）：
<answer>periodic=yes,min_period=4</answer>

- 若不存在周期性：
<answer>periodic=no,min_period=none</answer>

请使用尽可能少的提问次数找出答案。若答案错误、格式不符或单点查看超过 3 次，排查失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
The "Automated Assembly Line Defect Periodicity Troubleshooting" task is assigned.

The current batch produced a sequence S of N = {n} consecutive precision components, indexed from 1 to {n}. Each component is inspected and assigned one of four quality characteristic types (represented as A, B, C, D, purely as distinguishable symbols).

Your goal is to determine whether the assembly line's quality characteristics exhibit periodicity:
- If there exists an integer k (1 less than or equal to k less than {n}) such that for all components i (1 less than or equal to i less than or equal to {n}-k), we have S[i] = S[i+k], then the production quality is periodic.
- If periodic, find the minimum such k; otherwise, conclude that it is not periodic.

You can ask me questions using the following five types (one question per turn), and I will answer truthfully based on the real batch:

1. View Single Position (at most 3 times in total): Ask for the specific quality characteristic of component i.
2. Check Two Positions: Ask whether components i and j have the same characteristic.
3. Window Equality Check: Ask whether the production segment starting at i with length w is identical to the segment starting at j with length w, piece by piece.
4. Window Difference Count: Ask for the Hamming distance (number of differing components) between the segment starting at i with length w and the segment starting at j with length w.
5. Period Candidate Verification (unlimited): Ask whether a given integer k is a cycle period of the production characteristics.

Notes:
- All component indices must be in the range [1, {n}].
- For window queries, segments must not exceed bounds: i + w - 1 and j + w - 1 must both be less than or equal to {n}.
- For period verification, k must satisfy 1 less than or equal to k less than {n}.
- Out-of-bounds or malformed queries will receive error messages but won't count toward the single-view limit.

Each turn allows only one question. Use the following XML format:

- View Single Position (e.g., inspect component 5):
<query_view>5</query_view>

- Check Two Positions (e.g., check components 2 and 7):
<query_same>2,7</query_same>

- Window Equality Check (e.g., segment starting at 1 with length 3 vs. segment starting at 4 with length 3):
<query_window>1,4,3</query_window>

- Window Difference Count (e.g., segment starting at 1 with length 5 vs. segment starting at 6 with length 5):
<query_diff>1,6,5</query_diff>

- Period Candidate Verification (e.g., check if k=3 is a characteristic period):
<query_period>3</query_period>

When you have enough information, submit your final troubleshooting conclusion:

- If periodic (e.g., minimum period is 4):
<answer>periodic=yes,min_period=4</answer>

- If not periodic:
<answer>periodic=no,min_period=none</answer>

Try to use as few queries as possible. The task fails if the answer is incorrect, format is invalid, or single-view queries exceed 3 times.
"""

    contextualized_rule_zh_5 = """\
“金融交易账户洗钱循环侦测”已启动。

反洗钱系统拦截了某可疑账户连续 N = {n} 笔按时间排序的资金交易记录 S，索引范围为 [1, {n}]。每笔交易的操作手法被判定为四种风险标签之一（用 A、B、C、D 表示，仅作为可区分的符号）。

你的目标是判定该账户的交易行为是否构成周期性的洗钱循环：
- 若存在整数 k（1 小于等于 k 小于 {n}），使得对所有交易 i（1 小于等于 i 小于等于 {n}-k），都有 S[i] = S[i+k]，则称交易行为存在周期性。
- 若存在周期性，你需要找出最小的这样的 k；若不存在周期性，你需要给出否定结论。

你可以通过以下五种方式向法证系统提问（每轮可提出一个问题），系统会根据真实账本如实回答：

1. 单点查看（整个侦测中最多使用 3 次）：询问交易 i 的具体风险标签是什么。
2. 两点相同性判断：询问交易 i 和交易 j 的风险标签是否相同。
3. 窗口一致性判断：询问从交易 i 开始长度为 w 的交易区间，与从交易 j 开始长度为 w 的交易区间，是否逐笔完全一致。
4. 窗口差异计数：询问从交易 i 开始长度为 w 的交易区间，与从交易 j 开始长度为 w 的交易区间，逐笔比较有多少个风险标签不同（汉明距离）。
5. 周期候选验证（使用次数不限）：询问某个整数 k 是否为该账户交易行为的一个循环周期。

注意：
- 所有交易索引必须在 [1, {n}] 范围内。
- 窗口查询时，交易区间不能越界，即 i + w - 1 和 j + w - 1 都必须小于等于 {n}。
- 周期候选验证中，k 必须满足 1 小于等于 k 小于 {n}。
- 越界或格式错误的提问会得到错误提示，但不计入单点查看次数。

每次只能提一个问题，使用以下 XML 格式：

- 单点查看（例如审查交易 5）：
<query_view>5</query_view>

- 两点相同性判断（例如比对交易 2 和交易 7）：
<query_same>2,7</query_same>

- 窗口一致性判断（例如比对交易 1 开始长度 3 的区间与交易 4 开始长度 3 的区间）：
<query_window>1,4,3</query_window>

- 窗口差异计数（例如比对交易 1 开始长度 5 的区间与交易 6 开始长度 5 的区间）：
<query_diff>1,6,5</query_diff>

- 周期候选验证（例如验证 k=3 是否为洗钱周期）：
<query_period>3</query_period>

当你收集到足够信息后，提交法证结论，格式如下：

- 若存在周期性（例如最小周期为 4）：
<answer>periodic=yes,min_period=4</answer>

- 若不存在周期性：
<answer>periodic=no,min_period=none</answer>

请使用尽可能少的提问次数找出答案。若答案错误、格式不符或单点查看超过 3 次，侦测失败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
The "Financial Transaction Account Money Laundering Loop Detection" is activated.

The AML system intercepted a suspicious account's sequence S of N = {n} chronological fund transaction records, indexed from 1 to {n}. The operational methodology of each transaction is classified into one of four risk labels (represented as A, B, C, D, purely as distinguishable symbols).

Your goal is to determine whether the account's trading behavior constitutes a periodic money laundering loop:
- If there exists an integer k (1 less than or equal to k less than {n}) such that for all transactions i (1 less than or equal to i less than or equal to {n}-k), we have S[i] = S[i+k], then the transaction sequence is periodic.
- If periodic, find the minimum such k; otherwise, conclude that it is not periodic.

You can ask me questions using the following five types (one question per turn), and I will answer truthfully based on the real ledger:

1. View Single Position (at most 3 times in total): Ask for the specific risk label of transaction i.
2. Check Two Positions: Ask whether transactions i and j share the same risk label.
3. Window Equality Check: Ask whether the transaction window starting at i with length w is identical to the window starting at j with length w, transaction by transaction.
4. Window Difference Count: Ask for the Hamming distance (number of differing transactions) between the window starting at i with length w and the window starting at j with length w.
5. Period Candidate Verification (unlimited): Ask whether a given integer k is a cycle period of the transaction behavior.

Notes:
- All transaction indices must be in the range [1, {n}].
- For window queries, windows must not exceed bounds: i + w - 1 and j + w - 1 must both be less than or equal to {n}.
- For period verification, k must satisfy 1 less than or equal to k less than {n}.
- Out-of-bounds or malformed queries will receive error messages but won't count toward the single-view limit.

Each turn allows only one question. Use the following XML format:

- View Single Position (e.g., review transaction 5):
<query_view>5</query_view>

- Check Two Positions (e.g., check transactions 2 and 7):
<query_same>2,7</query_same>

- Window Equality Check (e.g., window starting at 1 with length 3 vs. window starting at 4 with length 3):
<query_window>1,4,3</query_window>

- Window Difference Count (e.g., window starting at 1 with length 5 vs. window starting at 6 with length 5):
<query_diff>1,6,5</query_diff>

- Period Candidate Verification (e.g., check if k=3 is a laundering cycle):
<query_period>3</query_period>

When you have enough information, submit your final forensic conclusion:

- If periodic (e.g., minimum period is 4):
<answer>periodic=yes,min_period=4</answer>

- If not periodic:
<answer>periodic=no,min_period=none</answer>

Try to use as few queries as possible. The detection fails if the answer is incorrect, format is invalid, or single-view queries exceed 3 times.
"""

    tags = ["answer", "query_view", "query_same", "query_window", "query_diff", "query_period"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 8,
                "sequence": "ABABABAB",  
                "has_period": True,
                "min_period": 2,
            },
            2: {
                "n": 10,
                "sequence": "ABCDAABCDA",  
                "has_period": True,
                "min_period": 5,
            },
            3: {
                "n": 12,
                "sequence": "ABCDABCDABCD",  
                "has_period": True,
                "min_period": 4,
            },
            4: {
                "n": 15,
                "sequence": "ABCDABCDABCDABD",  
                "has_period": False,
                "min_period": None,
            },
            5: {
                "n": 16,
                "sequence": "ABCDABCDABCDABCD",  
                "has_period": True,
                "min_period": 4,
            },
        },
        "en": {
            1: {
                "n": 8,
                "sequence": "ABABABAB",
                "has_period": True,
                "min_period": 2,
            },
            2: {
                "n": 10,
                "sequence": "ABCDAABCDA",
                "has_period": True,
                "min_period": 5,
            },
            3: {
                "n": 12,
                "sequence": "ABCDABCDABCD",
                "has_period": True,
                "min_period": 4,
            },
            4: {
                "n": 15,
                "sequence": "ABCDABCDABCDABD",  
                "has_period": False,
                "min_period": None,
            },
            5: {
                "n": 16,
                "sequence": "ABCDABCDABCDABCD",
                "has_period": True,
                "min_period": 4,
            },
        },
    }

    def __init__(self, config):
        self.view_count = 0
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
        
        raw_seq = cfg["sequence"]
        self.sequence = self._normalize_sequence(raw_seq)
        
        self.has_period = cfg["has_period"]
        self.min_period = cfg["min_period"]
        self.n = cfg["n"]

    def _normalize_sequence(self, seq):
        for ch in seq:
            if ch not in 'ABCD':
                raise ValueError(f"Sequence contains invalid character: {ch}")
        return seq

    def _check_period(self, k):
        if k < 1 or k >= self.n:
            return False
        for i in range(1, self.n - k + 1):
            if self.sequence[i-1] != self.sequence[i+k-1]:
                return False
        return True

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "periodic" not in ans_dict or "min_period" not in ans_dict:
                return False
            
            periodic_ans = ans_dict["periodic"].lower()
            period_ans = ans_dict["min_period"].lower()
            
            if self.has_period:
                if periodic_ans != "yes":
                    return False
                try:
                    k = int(period_ans)
                    return k == self.min_period
                except:
                    return False
            else:
                if periodic_ans != "no":
                    return False
                if period_ans != "none":
                    return False
                return True
                
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "query_view" in parsed_info:
            try:
                i = int(parsed_info["query_view"].strip())
                if i < 1 or i > self.n:
                    return "错误：位置越界。" if lang == "zh" else "Error: Position out of bounds."
            except Exception:
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
                
            self.view_count += 1
            if self.view_count > 3:
                raise ValueError(
                    "单点查看次数超过 3 次限制。" if lang == "zh" 
                    else "Single-view query limit (3 times) exceeded."
                )
            
            symbol = self.sequence[i-1]
            return f"符号：{symbol}" if lang == "zh" else f"Symbol: {symbol}"
        
        elif "query_same" in parsed_info:
            try:
                raw = parsed_info["query_same"].strip()
                i, j = [int(x.strip()) for x in raw.split(",")]
                if i < 1 or i > self.n or j < 1 or j > self.n:
                    return "错误：位置越界。" if lang == "zh" else "Error: Position out of bounds."
                same = self.sequence[i-1] == self.sequence[j-1]
                if lang == "zh":
                    return "是" if same else "否"
                else:
                    return "Yes" if same else "No"
            except Exception:
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
        
        elif "query_window" in parsed_info:
            try:
                raw = parsed_info["query_window"].strip()
                i, j, w = [int(x.strip()) for x in raw.split(",")]
                if i < 1 or j < 1 or w < 1:
                    return "错误：参数无效。" if lang == "zh" else "Error: Invalid parameters."
                if i + w - 1 > self.n or j + w - 1 > self.n:
                    return "错误：窗口越界。" if lang == "zh" else "Error: Window out of bounds."
                
                window1 = self.sequence[i-1:i-1+w]
                window2 = self.sequence[j-1:j-1+w]
                same = window1 == window2
                if lang == "zh":
                    return "是" if same else "否"
                else:
                    return "Yes" if same else "No"
            except Exception:
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
        
        elif "query_diff" in parsed_info:
            try:
                raw = parsed_info["query_diff"].strip()
                i, j, w = [int(x.strip()) for x in raw.split(",")]
                if i < 1 or j < 1 or w < 1:
                    return "错误：参数无效。" if lang == "zh" else "Error: Invalid parameters."
                if i + w - 1 > self.n or j + w - 1 > self.n:
                    return "错误：窗口越界。" if lang == "zh" else "Error: Window out of bounds."
                
                window1 = self.sequence[i-1:i-1+w]
                window2 = self.sequence[j-1:j-1+w]
                diff_count = sum(1 for a, b in zip(window1, window2) if a != b)
                return f"差异数：{diff_count}" if lang == "zh" else f"Differences: {diff_count}"
            except Exception:
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
        
        elif "query_period" in parsed_info:
            try:
                k = int(parsed_info["query_period"].strip())
                if k < 1 or k >= self.n:
                    return "错误：k 必须满足 1 <= k < N。" if lang == "zh" else "Error: k must satisfy 1 <= k < N."
                is_period = self._check_period(k)
                if lang == "zh":
                    return "是" if is_period else "否"
                else:
                    return "Yes" if is_period else "No"
            except Exception:
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
        
        else:
            raise ValueError(
                "未找到有效的查询标签。" if lang == "zh" 
                else "No valid query tag found."
            )

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        lang = self.config.language
        n = self.n
        
        for i in range(1, n + 1):
            query_content = f"<query_view>{i}</query_view>"
            symbol = self.sequence[i-1]
            ans = f"符号：{symbol}" if lang == "zh" else f"Symbol: {symbol}"
            queries.append({"query": query_content, "answer": ans})

        for i in range(1, n + 1):
            for j in range(1, n + 1):
                query_content = f"<query_same>{i},{j}</query_same>"
                same = (self.sequence[i-1] == self.sequence[j-1])
                ans = ("是" if same else "否") if lang == "zh" else ("Yes" if same else "No")
                queries.append({"query": query_content, "answer": ans})

        for w in range(1, n + 1):
            max_start = n - w + 1
            for i in range(1, max_start + 1):
                for j in range(1, max_start + 1):
                    win1 = self.sequence[i-1 : i-1+w]
                    win2 = self.sequence[j-1 : j-1+w]
                    
                    is_same = (win1 == win2)
                    q_win = f"<query_window>{i},{j},{w}</query_window>"
                    a_win = ("是" if is_same else "否") if lang == "zh" else ("Yes" if is_same else "No")
                    queries.append({"query": q_win, "answer": a_win})
                    
                    diff_cnt = sum(1 for a, b in zip(win1, win2) if a != b)
                    q_diff = f"<query_diff>{i},{j},{w}</query_diff>"
                    a_diff = (f"差异数：{diff_cnt}" if lang == "zh" else f"Differences: {diff_cnt}")
                    queries.append({"query": q_diff, "answer": a_diff})

        for k in range(1, n):
            query_content = f"<query_period>{k}</query_period>"
            is_period = self._check_period(k)
            ans = ("是" if is_period else "否") if lang == "zh" else ("Yes" if is_period else "No")
            queries.append({"query": query_content, "answer": ans})

        return queries

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        if correct.startswith("符号："):
            sym = correct[3:]
            wrong_sym = "B" if sym == "A" else "A"
            return f"符号：{wrong_sym}"
            
        if correct.startswith("Symbol: "):
            sym = correct[8:]
            wrong_sym = "B" if sym == "A" else "A"
            return f"Symbol: {wrong_sym}"
            
        if correct.startswith("差异数："):
            try:
                num = int(correct[4:])
                return f"差异数：{num + 1}"
            except Exception:
                pass
                
        if correct.startswith("Differences: "):
            try:
                num = int(correct[13:])
                return f"Differences: {num + 1}"
            except Exception:
                pass
                
        return correct + "_WRONG"