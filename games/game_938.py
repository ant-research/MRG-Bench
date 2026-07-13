# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   单调片段：序列中最长的严格递增/递减片段是哪一段
# ============================================================

from .base import Game
import random


class HiddenSequenceMonotonicGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏序列最长单调片段推断"游戏。规则如下：

游戏设定了一个隐藏的整数序列 S，长度为 {n}（下标从 1 到 {n}）。你的目标是找出 S 中"最长严格单调片段"（可以是严格上升或严格下降）的具体位置和类型。

**严格单调的定义：**
- 严格上升片段：连续子段中相邻元素均满足前一个元素小于后一个元素。
- 严格下降片段：连续子段中相邻元素均满足前一个元素大于后一个元素。
- 注意：相等的元素会打断严格单调性。

**唯一性规则（当存在多个同长度最长片段时）：**
1. 优先选择严格上升的片段
2. 若仍有并列，选择起点下标最小的
3. 若仍有并列，选择终点下标最小的

**观测变换：**
你不能直接访问序列 S。所有交互都在一个观测序列 T 的坐标系下进行（T 的下标也是 1 到 {n}）。T 与 S 之间存在一个未知的变换模式 Mode，可能是以下四种之一：
- A（索引保持，语义保持）：T[i] = S[i]，UP 表示大于，DOWN 表示小于
- B（索引反转，语义保持）：T[i] = S[{n}+1-i]，UP 表示大于，DOWN 表示小于
- C（索引保持，语义反转）：T[i] = S[i]，UP 表示小于，DOWN 表示大于
- D（索引反转，语义反转）：T[i] = S[{n}+1-i]，UP 表示小于，DOWN 表示大于

**可用查询：**
你可以反复使用扫描查询（每次一个），格式为：

<query_scan>L,R,Trend</query_scan>

其中：
- L 和 R 是 T 坐标系下的区间边界（1 到 {n}），L 小于等于 R
- Trend 是 UP 或 DOWN

查询会返回三个值 (len, a, b)：
- len：在 T[L..R] 区间内，按 Trend 指定方向的最长严格单调连续子段的长度
- a, b：该子段在 T 坐标系中的起止位置（a 到 b）
- 若有多个同长度子段，返回起点最小的；若仍并列，返回终点最小的

**最终答案格式：**
当你推断出答案后，请提交：

<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

其中：
- Mode 是 A、B、C 或 D
- Type 是 INC（严格上升）或 DEC（严格下降）
- Start and End 是原始序列 S 的下标（1 到 {n}）
- Length 是片段长度

注意：答案中的 Start 和 End 必须是 S 坐标系下的位置，而非 T 坐标系。
"""

    game_rule_en = """\
Let's play a "Hidden Sequence Longest Monotonic Segment Inference" game. Here are the rules:

A hidden integer sequence S of length {n} (indexed from 1 to {n}) has been set up. Your goal is to find the "longest strictly monotonic segment" in S (either strictly increasing or strictly decreasing), including its exact position and type.

**Strictly Monotonic Definition:**
- Strictly increasing segment: consecutive elements satisfy that each element is less than the next.
- Strictly decreasing segment: consecutive elements satisfy that each element is greater than the next.
- Note: Equal elements break strict monotonicity.

**Uniqueness Rules (when multiple segments of the same maximum length exist):**
1. Prioritize strictly increasing segments
2. If still tied, choose the one with the smallest starting index
3. If still tied, choose the one with the smallest ending index

**Observation Transformation:**
You cannot directly access sequence S. All interactions occur in an observation sequence T's coordinate system (T is also indexed from 1 to {n}). There is an unknown transformation mode Mode between T and S, which can be one of four types:
- A (index preserved, semantic preserved): T[i] = S[i], UP means greater than, DOWN means less than
- B (index reversed, semantic preserved): T[i] = S[{n}+1-i], UP means greater than, DOWN means less than
- C (index preserved, semantic reversed): T[i] = S[i], UP means less than, DOWN means greater than
- D (index reversed, semantic reversed): T[i] = S[{n}+1-i], UP means less than, DOWN means greater than

**Available Query:**
You can repeatedly use scan queries (one at a time), in the format:

<query_scan>L,R,Trend</query_scan>

Where:
- L and R are interval boundaries in T's coordinate system (1 to {n}), L less than or equal to R
- Trend is either UP or DOWN

The query returns three values (len, a, b):
- len: the length of the longest strictly monotonic consecutive segment in the specified Trend direction within T[L..R]
- a, b: the start and end positions of this segment in T's coordinate system (from a to b)
- If multiple segments have the same length, return the one with the smallest start; if still tied, return the one with the smallest end

**Final Answer Format:**
When you have inferred the answer, please submit:

<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

Where:
- Mode is A, B, C, or D
- Type is INC (strictly increasing) or DEC (strictly decreasing)
- Start and End are indices in the original sequence S (1 to {n})
- Length is the segment length

Note: Start and End in the answer must be positions in S's coordinate system, not T's coordinate system.
"""

    contextualized_rule_zh_1 = """\
欢迎使用智能交通路网趋势监测系统。

系统后台记录了一段由 {n} 个连续探测节点（编号从 1 到 {n}）组成的真实历史拥堵指数序列 S。你的目标是排查出 S 中“持续恶化或持续缓解的最长连续路段”（即最长严格单调片段）的具体位置和类型。

**严格单调的定义：**
- 持续恶化路段（严格上升）：连续子段中相邻节点的指数均满足前一个小于后一个。
- 持续缓解路段（严格下降）：连续子段中相邻节点的指数均满足前一个大于后一个。
- 注意：指数相同的节点会打断这种单调趋势。

**唯一性规则（存在多个同等最长路段时）：**
1. 优先选择持续恶化（严格上升）的路段
2. 若仍并列，选择起点编号最小的
3. 若仍并列，选择终点编号最小的

**观测变换：**
由于传感器可能接线倒置或采用负压传感模式，你无法直接读取序列 S，只能通过观测平台读取序列 T（节点编号也是 1 到 {n}）。T 与 S 之间存在一种未知的线路变换 Mode：
- A（正向接线，正极性）：T[i] = S[i]，UP 表示指数变大，DOWN 表示指数变小
- B（反向接线，正极性）：T[i] = S[{n}+1-i]，UP 表示指数变大，DOWN 表示指数变小
- C（正向接线，负极性）：T[i] = S[i]，UP 表示指数变小，DOWN 表示指数变大
- D（反向接线，负极性）：T[i] = S[{n}+1-i]，UP 表示指数变小，DOWN 表示指数变大

**可用查询：**
你可以反复调用系统的趋势扫描探针，格式为：
<query_scan>L,R,Trend</query_scan>

其中：
- L 和 R 是 T 平台下的节点区间边界（1 到 {n}），L 小于等于 R
- Trend 是 UP 或 DOWN

探针会返回三个值 (len, a, b)：
- len：在 T[L..R] 区间内，按 Trend 指定方向的最长严格单调连续子段的长度
- a, b：该子段在 T 平台中的起止位置
- 并列时，返回起点最小的；仍并列，返回终点最小的

**最终答案格式：**
查明真相后，请提交：
<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

其中：
- Mode 属于 A、B、C 或 D
- Type 为 INC（严格上升）或 DEC（严格下降）
- Start 和 End 为真实序列 S 下的节点编号（1 到 {n}）
- Length 为路段长度
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Smart Traffic Network Trend Monitoring System.

The system backend has recorded a real historical traffic congestion index sequence S consisting of {n} continuous detection nodes (indexed from 1 to {n}). Your goal is to identify the exact position and type of the "longest continuous segment of sustained deterioration or alleviation" (i.e., the longest strictly monotonic segment) within S.

**Strictly Monotonic Definition:**
- Deteriorating segment (strictly increasing): consecutive nodes where the index of each is strictly greater than the previous.
- Alleviating segment (strictly decreasing): consecutive nodes where the index of each is strictly less than the previous.
- Note: Equal index values break this monotonic trend.

**Uniqueness Rules (when multiple segments of the maximum length exist):**
1. Prioritize deteriorating (strictly increasing) segments
2. If still tied, choose the one with the smallest starting index
3. If still tied, choose the one with the smallest ending index

**Observation Transformation:**
Due to potential inverted wiring or negative-pressure sensing modes of the detectors, you cannot read S directly. Instead, you can only access the observation platform sequence T (also indexed from 1 to {n}). An unknown circuit transformation Mode exists between T and S:
- A (Forward wiring, Positive polarity): T[i] = S[i], UP means increasing index, DOWN means decreasing index
- B (Reverse wiring, Positive polarity): T[i] = S[{n}+1-i], UP means increasing index, DOWN means decreasing index
- C (Forward wiring, Negative polarity): T[i] = S[i], UP means decreasing index, DOWN means increasing index
- D (Reverse wiring, Negative polarity): T[i] = S[{n}+1-i], UP means decreasing index, DOWN means increasing index

**Available Query:**
You can repeatedly use the system's trend scanning probe, formatted as:
<query_scan>L,R,Trend</query_scan>

Where:
- L and R are interval boundaries in T's coordinate system (1 to {n}), L less than or equal to R
- Trend is either UP or DOWN

The probe returns three values (len, a, b):
- len: the length of the longest strictly monotonic consecutive segment in the specified Trend direction within T[L..R]
- a, b: the start and end positions of this segment in T's system
- Ties are broken by the smallest start index, then smallest end index

**Final Answer Format:**
Once determined, please submit:
<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

Where:
- Mode is A, B, C, or D
- Type is INC (strictly increasing) or DEC (strictly decreasing)
- Start and End are node indices in the original sequence S (1 to {n})
- Length is the segment length
"""

    contextualized_rule_zh_2 = """\
欢迎使用患者生命体征连续监测预警系统。

系统记录了一名重点患者在 {n} 个连续时间窗（编号从 1 到 {n}）内的真实心率变异性指标序列 S。你的目标是找出 S 中“指标持续恶化或持续好转的最长生理阶段”（即最长严格单调片段）的具体位置和类型。

**严格单调的定义：**
- 持续恶化阶段（严格上升）：连续时间窗中相邻指标均满足前一个小于后一个。
- 持续好转阶段（严格下降）：连续时间窗中相邻指标均满足前一个大于后一个。
- 注意：指标数值相同会打断这一单调趋势。

**唯一性规则（存在多个同等最长阶段时）：**
1. 优先选择持续恶化（严格上升）的阶段
2. 若仍并列，选择起点时间窗编号最小的
3. 若仍并列，选择终点时间窗编号最小的

**观测变换：**
由于不同厂家的监护仪可能存在时间戳倒序输出或信号极性反转，你无法直接读取真实序列 S，只能通过监控终端读取序列 T（时间窗编号也是 1 到 {n}）。T 与 S 之间存在一种未知的协议变换 Mode：
- A（正序输出，正极性）：T[i] = S[i]，UP 表示指标变大，DOWN 表示指标变小
- B（倒序输出，正极性）：T[i] = S[{n}+1-i]，UP 表示指标变大，DOWN 表示指标变小
- C（正序输出，负极性）：T[i] = S[i]，UP 表示指标变小，DOWN 表示指标变大
- D（倒序输出，负极性）：T[i] = S[{n}+1-i]，UP 表示指标变小，DOWN 表示指标变大

**可用查询：**
你可以反复调用后台的趋势分析探针，格式为：
<query_scan>L,R,Trend</query_scan>

其中：
- L 和 R 是 T 平台下的时间区间边界（1 到 {n}），L 小于等于 R
- Trend 是 UP 或 DOWN

探针会返回三个值 (len, a, b)：
- len：在 T[L..R] 区间内，按 Trend 指定方向的最长严格单调连续子段的长度
- a, b：该子段在 T 终端中的起止位置
- 并列时，返回起点最小的；仍并列，返回终点最小的

**最终答案格式：**
确认诊断阶段后，请提交：
<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

其中：
- Mode 属于 A、B、C 或 D
- Type 为 INC（严格上升）或 DEC（严格下降）
- Start 和 End 为真实生理序列 S 下的时间窗编号（1 到 {n}）
- Length 为阶段长度
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Patient Vital Signs Continuous Monitoring System.

The system has recorded a critical patient's true heart rate variability index sequence S across {n} continuous time windows (indexed from 1 to {n}). Your goal is to identify the exact position and type of the "longest physiological phase of continuous deterioration or improvement" (i.e., the longest strictly monotonic segment) within S.

**Strictly Monotonic Definition:**
- Deteriorating phase (strictly increasing): consecutive time windows where the index strictly increases.
- Improving phase (strictly decreasing): consecutive time windows where the index strictly decreases.
- Note: Equal index values interrupt this monotonic trend.

**Uniqueness Rules (when multiple phases of the maximum length exist):**
1. Prioritize deteriorating (strictly increasing) phases
2. If still tied, choose the one with the smallest starting index
3. If still tied, choose the one with the smallest ending index

**Observation Transformation:**
Due to different monitor manufacturers, data may be output in reverse chronological order or with inverted signal polarity. You cannot read the true sequence S directly, but only the observation sequence T via the terminal (also indexed from 1 to {n}). An unknown protocol transformation Mode exists between T and S:
- A (Chronological, Positive polarity): T[i] = S[i], UP means increasing index, DOWN means decreasing index
- B (Reverse chronological, Positive polarity): T[i] = S[{n}+1-i], UP means increasing index, DOWN means decreasing index
- C (Chronological, Negative polarity): T[i] = S[i], UP means decreasing index, DOWN means increasing index
- D (Reverse chronological, Negative polarity): T[i] = S[{n}+1-i], UP means decreasing index, DOWN means increasing index

**Available Query:**
You can repeatedly query the trend analysis probe, formatted as:
<query_scan>L,R,Trend</query_scan>

Where:
- L and R are interval boundaries in T's coordinate system (1 to {n}), L less than or equal to R
- Trend is either UP or DOWN

The probe returns three values (len, a, b):
- len: the length of the longest strictly monotonic consecutive segment in the specified Trend direction within T[L..R]
- a, b: the start and end positions of this segment in T's system
- Ties are broken by the smallest start index, then smallest end index

**Final Answer Format:**
Once diagnosed, please submit:
<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

Where:
- Mode is A, B, C, or D
- Type is INC (strictly increasing) or DEC (strictly decreasing)
- Start and End are time window indices in the true physiological sequence S (1 to {n})
- Length is the phase length
"""

    contextualized_rule_zh_3 = """\
欢迎使用学生学情表现追踪测评系统。

教务处记录了某核心班级在 {n} 个连续测评期（编号从 1 到 {n}）内的真实学情指标序列 S。你的任务是找出 S 中“成绩持续进步或持续退步的最长周期”（即最长严格单调片段）的具体位置和类型。

**严格单调的定义：**
- 持续进步周期（严格上升）：连续测评期中相邻指标均满足前一个小于后一个。
- 持续退步周期（严格下降）：连续测评期中相邻指标均满足前一个大于后一个。
- 注意：指标得分持平会打断这种单调趋势。

**唯一性规则（存在多个同等最长周期时）：**
1. 优先选择持续进步（严格上升）的周期
2. 若仍并列，选择起点期数编号最小的
3. 若仍并列，选择终点期数编号最小的

**观测变换：**
因系统导出设置差异，数据可能是按时间倒序排列的，或者采用的是排名计分法（排名数值越低代表成绩越好，导致语义反转）。你只能通过前端界面查看观测序列 T（期数编号也是 1 到 {n}）。T 与 S 之间存在一种未知的导出模式 Mode：
- A（正向导出，得分法）：T[i] = S[i]，UP 表示数值变大，DOWN 表示数值变小
- B（逆向导出，得分法）：T[i] = S[{n}+1-i]，UP 表示数值变大，DOWN 表示数值变小
- C（正向导出，排名法）：T[i] = S[i]，UP 表示数值变小，DOWN 表示数值变大
- D（逆向导出，排名法）：T[i] = S[{n}+1-i]，UP 表示数值变小，DOWN 表示数值变大

**可用查询：**
你可以反复使用阶段趋势分析器，格式为：
<query_scan>L,R,Trend</query_scan>

其中：
- L 和 R 是 T 界面下的区间边界（1 到 {n}），L 小于等于 R
- Trend 是 UP 或 DOWN

分析器会返回三个值 (len, a, b)：
- len：在 T[L..R] 区间内，按 Trend 指定方向的最长严格单调连续子段的长度
- a, b：该子段在 T 界面中的起止位置
- 并列时，返回起点最小的；仍并列，返回终点最小的

**最终答案格式：**
得出分析结果后，请提交：
<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

其中：
- Mode 属于 A、B、C 或 D
- Type 为 INC（严格上升）或 DEC（严格下降）
- Start 和 End 为真实学情序列 S 下的测评期编号（1 到 {n}）
- Length 为周期长度
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Student Academic Performance Tracking System.

The academic affairs office has recorded the true academic performance index sequence S of a core class over {n} continuous evaluation periods (indexed from 1 to {n}). Your task is to find the exact position and type of the "longest cycle of continuous progress or regression" (i.e., the longest strictly monotonic segment) within S.

**Strictly Monotonic Definition:**
- Continuous progress cycle (strictly increasing): consecutive periods where the index strictly increases.
- Continuous regression cycle (strictly decreasing): consecutive periods where the index strictly decreases.
- Note: Identical index scores break this monotonic trend.

**Uniqueness Rules (when multiple cycles of the maximum length exist):**
1. Prioritize continuous progress (strictly increasing) cycles
2. If still tied, choose the one with the smallest starting index
3. If still tied, choose the one with the smallest ending index

**Observation Transformation:**
Due to differing system export settings, data might be sorted in reverse chronological order, or a ranking system might be used (where a lower rank implies better performance, reversing the semantics). You can only view the observation sequence T via the frontend interface (also indexed from 1 to {n}). An unknown export Mode exists between T and S:
- A (Forward export, Score-based): T[i] = S[i], UP means increasing value, DOWN means decreasing value
- B (Reverse export, Score-based): T[i] = S[{n}+1-i], UP means increasing value, DOWN means decreasing value
- C (Forward export, Rank-based): T[i] = S[i], UP means decreasing value, DOWN means increasing value
- D (Reverse export, Rank-based): T[i] = S[{n}+1-i], UP means decreasing value, DOWN means increasing value

**Available Query:**
You can repeatedly use the phase trend analyzer, formatted as:
<query_scan>L,R,Trend</query_scan>

Where:
- L and R are interval boundaries in T's coordinate system (1 to {n}), L less than or equal to R
- Trend is either UP or DOWN

The analyzer returns three values (len, a, b):
- len: the length of the longest strictly monotonic consecutive segment in the specified Trend direction within T[L..R]
- a, b: the start and end positions of this segment in T's interface
- Ties are broken by the smallest start index, then smallest end index

**Final Answer Format:**
Upon concluding the analysis, please submit:
<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

Where:
- Mode is A, B, C, or D
- Type is INC (strictly increasing) or DEC (strictly decreasing)
- Start and End are evaluation period indices in the true sequence S (1 to {n})
- Length is the cycle length
"""

    contextualized_rule_zh_4 = """\
欢迎使用工业反应炉温度监控预警系统。

核心数据中心记录了反应炉在 {n} 个连续投料批次（编号从 1 到 {n}）中的真实温度负荷序列 S。你的任务是找出 S 中“持续升温或持续降温的最长危险区间”（即最长严格单调片段）的具体位置和类型。

**严格单调的定义：**
- 持续升温区间（严格上升）：连续批次中相邻温度均满足前一个小于后一个。
- 持续降温区间（严格下降）：连续批次中相邻温度均满足前一个大于后一个。
- 注意：温度持平会打断该单调趋势。

**唯一性规则（存在多个同等最长区间时）：**
1. 优先选择持续升温（严格上升）的区间
2. 若仍并列，选择起点批次编号最小的
3. 若仍并列，选择终点批次编号最小的

**观测变换：**
因为采集终端可能存在时间轴反接，或者传感器采用了 NTC 负温度系数热敏电阻（阻值与温度成反比），你无法直接读取真实负荷 S，只能通过监控面板读取观测序列 T（批次编号也是 1 到 {n}）。T 与 S 之间存在一种未知的标定模式 Mode：
- A（正常接线，正极性传感）：T[i] = S[i]，UP 表示读数变大，DOWN 表示读数变小
- B（反接接线，正极性传感）：T[i] = S[{n}+1-i]，UP 表示读数变大，DOWN 表示读数变小
- C（正常接线，NTC 负极性传感）：T[i] = S[i]，UP 表示读数变小，DOWN 表示读数变大
- D（反接接线，NTC 负极性传感）：T[i] = S[{n}+1-i]，UP 表示读数变小，DOWN 表示读数变大

**可用查询：**
你可以反复向数据中控台下达区间趋势扫描指令，格式为：
<query_scan>L,R,Trend</query_scan>

其中：
- L 和 R 是 T 面板下的区间边界（1 到 {n}），L 小于等于 R
- Trend 是 UP 或 DOWN

指令会返回三个值 (len, a, b)：
- len：在 T[L..R] 区间内，按 Trend 指定方向的最长严格单调连续子段的长度
- a, b：该子段在 T 面板中的起止位置
- 并列时，返回起点最小的；仍并列，返回终点最小的

**最终答案格式：**
排查出危险区间后，请提交：
<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

其中：
- Mode 属于 A、B、C 或 D
- Type 为 INC（严格上升）或 DEC（严格下降）
- Start 和 End 为真实序列 S 下的批次编号（1 到 {n}）
- Length 为区间长度
"""

    contextualized_rule_en_4 = """\
[Industrial Scenario]
Welcome to the Industrial Reactor Temperature Monitoring System.

The core data center has recorded the true temperature load sequence S of a reactor across {n} continuous feeding batches (indexed from 1 to {n}). Your task is to locate the exact position and type of the "longest dangerous interval of continuous heating or cooling" (i.e., the longest strictly monotonic segment) within S.

**Strictly Monotonic Definition:**
- Continuous heating interval (strictly increasing): consecutive batches where the temperature strictly increases.
- Continuous cooling interval (strictly decreasing): consecutive batches where the temperature strictly decreases.
- Note: Unchanged temperatures interrupt this monotonic trend.

**Uniqueness Rules (when multiple intervals of the maximum length exist):**
1. Prioritize continuous heating (strictly increasing) intervals
2. If still tied, choose the one with the smallest starting index
3. If still tied, choose the one with the smallest ending index

**Observation Transformation:**
Because the data acquisition terminal may have reversed timeline wiring, or the sensors may use NTC (Negative Temperature Coefficient) thermistors (where resistance is inversely proportional to temperature), you cannot directly read the true load S. Instead, you can only view the observation sequence T via the monitoring panel (also indexed from 1 to {n}). An unknown calibration Mode exists between T and S:
- A (Normal wiring, Positive sensing): T[i] = S[i], UP means increasing reading, DOWN means decreasing reading
- B (Reversed wiring, Positive sensing): T[i] = S[{n}+1-i], UP means increasing reading, DOWN means decreasing reading
- C (Normal wiring, NTC Negative sensing): T[i] = S[i], UP means decreasing reading, DOWN means increasing reading
- D (Reversed wiring, NTC Negative sensing): T[i] = S[{n}+1-i], UP means decreasing reading, DOWN means increasing reading

**Available Query:**
You can repeatedly send interval trend scan commands to the control console, formatted as:
<query_scan>L,R,Trend</query_scan>

Where:
- L and R are interval boundaries in T's coordinate system (1 to {n}), L less than or equal to R
- Trend is either UP or DOWN

The command returns three values (len, a, b):
- len: the length of the longest strictly monotonic consecutive segment in the specified Trend direction within T[L..R]
- a, b: the start and end positions of this segment on T's panel
- Ties are broken by the smallest start index, then smallest end index

**Final Answer Format:**
Once the dangerous interval is identified, please submit:
<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

Where:
- Mode is A, B, C, or D
- Type is INC (strictly increasing) or DEC (strictly decreasing)
- Start and End are batch indices in the true sequence S (1 to {n})
- Length is the interval length
"""

    contextualized_rule_zh_5 = """\
欢迎使用知识产权案件财务数字审计系统。

专案组缴获了嫌疑企业在 {n} 个连续记账节点（编号从 1 到 {n}）的真实非法资金流转序列 S。你的目标是找出 S 中“资金规模持续扩张或持续转移缩减的最长作案周期”（即最长严格单调片段）的具体位置和类型。

**严格单调的定义：**
- 持续扩张周期（严格上升）：连续账目中相邻资金量均满足前一笔小于后一笔。
- 持续缩减周期（严格下降）：连续账目中相邻资金量均满足前一笔大于后一笔。
- 注意：资金量相等会打断这种单调趋势。

**唯一性规则（存在多个同等最长周期时）：**
1. 优先选择持续扩张（严格上升）的周期
2. 若仍并列，选择起点账目编号最小的
3. 若仍并列，选择终点账目编号最小的

**观测变换：**
嫌疑人可能通过黑客手段对账本施加了时间戳倒序加密，或者伪造了阴阳账本（将收入记为支出，借贷记账反转致使语义颠倒）。你只能对取证平台恢复出的观测序列 T（编号也是 1 到 {n}）进行交互。T 与 S 之间存在一种未知的篡改模式 Mode：
- A（未反转时间，未反转账目）：T[i] = S[i]，UP 表示数值变大，DOWN 表示数值变小
- B（倒序时间，未反转账目）：T[i] = S[{n}+1-i]，UP 表示数值变大，DOWN 表示数值变小
- C（未反转时间，反转账目）：T[i] = S[i]，UP 表示数值变小，DOWN 表示数值变大
- D（倒序时间，反转账目）：T[i] = S[{n}+1-i]，UP 表示数值变小，DOWN 表示数值变大

**可用查询：**
你可以反复使用资金链追溯指令，格式为：
<query_scan>L,R,Trend</query_scan>

其中：
- L 和 R 是 T 平台下的账目区间边界（1 到 {n}），L 小于等于 R
- Trend 是 UP 或 DOWN

指令会返回三个值 (len, a, b)：
- len：在 T[L..R] 区间内，按 Trend 指定方向的最长严格单调连续子段的长度
- a, b：该子段在 T 平台中的起止位置
- 并列时，返回起点最小的；仍并列，返回终点最小的

**最终答案格式：**
完成证据链固定后，请提交：
<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

其中：
- Mode 属于 A、B、C 或 D
- Type 为 INC（严格上升）或 DEC（严格下降）
- Start 和 End 为真实账本序列 S 下的节点编号（1 到 {n}）
- Length 为作案周期长度
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Intellectual Property Financial Audit System.

The task force has seized the true illegal capital flow sequence S of a suspect enterprise across {n} continuous accounting nodes (indexed from 1 to {n}). Your goal is to identify the exact position and type of the "longest crime cycle of continuous expansion or reduction in capital scale" (i.e., the longest strictly monotonic segment) within S.

**Strictly Monotonic Definition:**
- Continuous expansion cycle (strictly increasing): consecutive accounts where each capital amount is strictly greater than the previous.
- Continuous reduction cycle (strictly decreasing): consecutive accounts where each capital amount is strictly less than the previous.
- Note: Equal capital amounts break this monotonic trend.

**Uniqueness Rules (when multiple cycles of the maximum length exist):**
1. Prioritize continuous expansion (strictly increasing) cycles
2. If still tied, choose the one with the smallest starting index
3. If still tied, choose the one with the smallest ending index

**Observation Transformation:**
The suspects may have applied reverse-timestamp encryption via hacking, or forged double-bookkeeping (recording income as expenditure, reversing debit/credit semantics). You can only interact with the recovered observation sequence T via the forensic platform (also indexed from 1 to {n}). An unknown tampering Mode exists between T and S:
- A (Normal timestamp, Normal accounting): T[i] = S[i], UP means increasing value, DOWN means decreasing value
- B (Reversed timestamp, Normal accounting): T[i] = S[{n}+1-i], UP means increasing value, DOWN means decreasing value
- C (Normal timestamp, Reversed accounting): T[i] = S[i], UP means decreasing value, DOWN means increasing value
- D (Reversed timestamp, Reversed accounting): T[i] = S[{n}+1-i], UP means decreasing value, DOWN means increasing value

**Available Query:**
You can repeatedly use the capital chain tracing command, formatted as:
<query_scan>L,R,Trend</query_scan>

Where:
- L and R are interval boundaries in T's coordinate system (1 to {n}), L less than or equal to R
- Trend is either UP or DOWN

The command returns three values (len, a, b):
- len: the length of the longest strictly monotonic consecutive segment in the specified Trend direction within T[L..R]
- a, b: the start and end positions of this segment on T's platform
- Ties are broken by the smallest start index, then smallest end index

**Final Answer Format:**
Once the chain of evidence is secured, please submit:
<answer>Mode=X, Type=Y, Start=S, End=E, Length=L</answer>

Where:
- Mode is A, B, C, or D
- Type is INC (strictly increasing) or DEC (strictly decreasing)
- Start and End are node indices in the true ledger sequence S (1 to {n})
- Length is the crime cycle length
"""

    tags = ["answer", "query_scan"]

    reasoning_type = "溯因推理"
    data_structure = "序列"

    # 难度配置
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {  # 简单：短序列，模式A（无变换）
                "n": 8,
                "sequence": [3, 1, 2, 4, 6, 8, 5, 7],
                "mode": "A",
            },
            2: {  # 中等偏下：中等序列，模式B（索引反转）
                "n": 10,
                "sequence": [5, 4, 3, 2, 1, 6, 7, 8, 9, 10],
                "mode": "B",
            },
            3: {  # 中等偏上：中等序列，模式C（语义反转）
                "n": 12,
                "sequence": [10, 9, 8, 7, 6, 11, 12, 13, 5, 4, 3, 2],
                "mode": "C",
            },
            4: {  # 较难：较长序列，模式D（双重反转）
                "n": 15,
                "sequence": [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 1, 2, 3, 4, 5],
                "mode": "D",
            },
            5: {  # 难：长序列，复杂分布，模式B
                "n": 20,
                "sequence": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13, 14, 20, 19, 18, 17, 16, 15],
                "mode": "B",
            },
        },
        "en": {
            1: {
                "n": 8,
                "sequence": [3, 1, 2, 4, 6, 8, 5, 7],
                "mode": "A",
            },
            2: {
                "n": 10,
                "sequence": [5, 4, 3, 2, 1, 6, 7, 8, 9, 10],
                "mode": "B",
            },
            3: {
                "n": 12,
                "sequence": [10, 9, 8, 7, 6, 11, 12, 13, 5, 4, 3, 2],
                "mode": "C",
            },
            4: {
                "n": 15,
                "sequence": [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 1, 2, 3, 4, 5],
                "mode": "D",
            },
            5: {
                "n": 20,
                "sequence": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 11, 12, 13, 14, 20, 19, 18, 17, 16, 15],
                "mode": "B",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        # 确保 difficulty 是整数类型
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 原始序列 S（1-indexed，所以在索引0处放None）
        self.S = [None] + cfg["sequence"]
        self.mode = cfg["mode"]
        self.n = cfg["n"]
        
        # 构建观测序列 T（根据 mode）
        self.T = [None] * (self.n + 1)
        for i in range(1, self.n + 1):
            if self.mode in ["A", "C"]:  # 索引保持
                self.T[i] = self.S[i]
            else:  # B, D：索引反转
                self.T[i] = self.S[self.n + 1 - i]
        
        # 计算 S 中的答案（Ground Truth）
        self._compute_ground_truth()

    def _compute_ground_truth(self):
        """计算原始序列 S 中满足唯一性规则的最长严格单调片段"""
        n = self.n
        best_len = 0
        best_type = None  # "INC" or "DEC"
        best_start = None
        best_end = None
        
        # 遍历所有可能的起点
        for start in range(1, n + 1):
            # 尝试严格上升
            end = start
            while end < n and self.S[end] < self.S[end + 1]:
                end += 1
            length = end - start + 1
            if length > best_len or (length == best_len and (best_type == "DEC" or (best_type == "INC" and start < best_start) or (best_type == "INC" and start == best_start and end < best_end))):
                best_len = length
                best_type = "INC"
                best_start = start
                best_end = end
            
            # 尝试严格下降
            end = start
            while end < n and self.S[end] > self.S[end + 1]:
                end += 1
            length = end - start + 1
            if length > best_len or (length == best_len and (best_type == "DEC" and (start < best_start or (start == best_start and end < best_end)))):
                best_len = length
                best_type = "DEC"
                best_start = start
                best_end = end
        
        self.answer_mode = self.mode
        self.answer_type = best_type
        self.answer_start = best_start
        self.answer_end = best_end
        self.answer_length = best_len

    def _find_longest_monotonic_in_T(self, L, R, trend):
        """
        在 T[L..R] 区间内查找指定 trend 方向的最长严格单调子段
        trend: "UP" 或 "DOWN"
        返回 (length, start, end)
        """
        # 根据 mode 确定 UP/DOWN 的实际含义
        # A: UP=>, DOWN=<
        # B: UP=>, DOWN=<
        # C: UP=<, DOWN=>
        # D: UP=<, DOWN=>
        
        if self.mode in ["A", "B"]:
            compare_func = lambda a, b: a < b if trend == "UP" else a > b
        else:  # C, D
            compare_func = lambda a, b: a > b if trend == "UP" else a < b
        
        best_len = 0
        best_start = L
        best_end = L
        
        i = L
        while i <= R:
            # 从 i 开始找最长严格单调子段
            j = i
            while j < R and compare_func(self.T[j], self.T[j + 1]):
                j += 1
            
            length = j - i + 1
            if length > best_len or (length == best_len and (i < best_start or (i == best_start and j < best_end))):
                best_len = length
                best_start = i
                best_end = j
            
            i = j + 1
        
        return (best_len, best_start, best_end)

    def evaluate(self, parsed_info):
        """检查答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: Mode=X, Type=Y, Start=S, End=E, Length=L
        try:
            parts = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if not all(k in ans_dict for k in ["Mode", "Type", "Start", "End", "Length"]):
                return False
            
            mode = ans_dict["Mode"]
            seg_type = ans_dict["Type"]
            start = int(ans_dict["Start"])
            end = int(ans_dict["End"])
            length = int(ans_dict["Length"])
            
            # 检查是否与ground truth匹配
            return (mode == self.answer_mode and
                    seg_type == self.answer_type and
                    start == self.answer_start and
                    end == self.answer_end and
                    length == self.answer_length)
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """处理查询并返回结果"""
        if "query_scan" in parsed_info:
            try:
                raw = parsed_info["query_scan"].strip()
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 3:
                    raise ValueError("Invalid query format")
                
                L = int(parts[0])
                R = int(parts[1])
                trend = parts[2].upper()
                
                if not (1 <= L <= R <= self.n):
                    if self.config.language == "zh":
                        return "错误：区间越界。"
                    else:
                        return "Error: Interval out of bounds."
                
                if trend not in ["UP", "DOWN"]:
                    if self.config.language == "zh":
                        return "错误：Trend 必须是 UP 或 DOWN。"
                    else:
                        return "Error: Trend must be UP or DOWN."
                
                # 执行查询
                length, start, end = self._find_longest_monotonic_in_T(L, R, trend)
                
                return f"({length}, {start}, {end})"
                
            except Exception as e:
                if self.config.language == "zh":
                    return f"错误：查询格式无效或参数错误。"
                else:
                    return f"Error: Invalid query format or parameters."
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        import re
        # 尝试匹配 (len, start, end) 格式
        m = re.match(r'\((\d+),\s*(\d+),\s*(\d+)\)', correct)
        if m:
            length = int(m.group(1))
            start = int(m.group(2))
            end = int(m.group(3))
            # 篡改长度值
            wrong_length = length + 1 if length < self.n else length - 1
            return f"({wrong_length}, {start}, {end})"
        
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            if "No" in correct:
                return correct.replace("No", "Yes")
            if "yes" in correct:
                return correct.replace("yes", "no")
            if "no" in correct:
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        # L 从 1 到 n
        for L in range(1, self.n + 1):
            # R 从 L 到 n
            for R in range(L, self.n + 1):
                # Trend 为 UP 或 DOWN
                for trend in ["UP", "DOWN"]:
                    # 构造查询字符串，对应 parsed_info["query_scan"] 的内容
                    query_str = f"<query_scan>{L},{R},{trend}</query_scan>"
                    
                    # 调用内部逻辑计算结果
                    length, start, end = self._find_longest_monotonic_in_T(L, R, trend)
                    answer_str = f"({length}, {start}, {end})"
                    
                    queries.append({
                        "query": query_str,
                        "answer": answer_str
                    })
        
        return queries