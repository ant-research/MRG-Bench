# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   元素距离：两个给定元素之间相隔多少个位置
# ============================================================

from .base import Game
import re


class PositionMappingGame(Game):

    game_rule_zh = """\
我们来玩一个"位置映射推理"游戏，规则如下：

## 游戏设定

存在一个长度为 10 的有序位置序列，位置编号为 1 到 10。
有 10 个可区分的标签，记为 A、B、C、D、E、F、G、H、I、J。

这些标签按照某种隐藏的映射规则分布在这 10 个位置上。存在四种可能的映射方案，但你不知道当前使用的是哪一种。

对于任意两个标签 X 和 Y，它们的"间隔"定义为：它们所在位置之间的距离减 1（即端点不计入）。
例如，若 X 在位置 3，Y 在位置 7，则间隔为 |7-3| - 1 = 3。

## 你的目标

1. 通过有限次数的查询，推断出当前使用的是哪一种映射方案（方案1、方案2、方案3 或 方案4）
2. 在判定方案后，我会给你一对目标标签，你需要计算它们之间的间隔

## 可用的查询类型

你可以进行以下两种查询（每次只能进行一种）：

1. **测距查询**：询问两个不同标签 X 和 Y 之间的间隔。我会返回一个非负整数。

2. **比较查询**：给出两对标签 (X, Y) 和 (U, V)，询问哪一对的间隔更大。我会返回以下三种结果之一：
   - "前者更大"（X和Y的间隔大于U和V的间隔）
   - "后者更大"（X和Y的间隔小于U和V的间隔）
   - "相等"（两对间隔相等）

## 约束条件

- 查询总次数上限为 {max_queries} 次
- 必须至少进行 {min_queries} 次查询后才能提交方案判定
- 一旦提交方案判定，就不能再进行查询

## 查询与答案格式（必须严格遵守）

每次只能包含一个查询或答案标签。

**测距查询**（例如询问 A 和 C 的间隔）：
<query_distance>A,C</query_distance>

**比较查询**（例如比较 (A,B) 和 (C,D) 的间隔）：
<query_compare>A,B,C,D</query_compare>

**提交方案判定**（例如判定为方案2）：
<answer_scheme>方案2</answer_scheme>

**提交最终间隔答案**（在我给出目标标签对后，例如答案是5）：
<answer_distance>5</answer_distance>

注意：标签必须是 A 到 J 中的大写字母，用逗号分隔，不要有多余空格。
"""

    game_rule_en = """\
Let's play a "Position Mapping Reasoning" game. Here are the rules:

## Game Setup

There is an ordered sequence of 10 positions, numbered 1 to 10.
There are 10 distinguishable labels: A, B, C, D, E, F, G, H, I, J.

These labels are distributed across the 10 positions according to a hidden mapping rule. There are four possible mapping schemes, but you don't know which one is currently in use.

For any two labels X and Y, their "interval" is defined as: the distance between their positions minus 1 (endpoints not counted).
For example, if X is at position 3 and Y is at position 7, the interval is |7-3| - 1 = 3.

## Your Goal

1. Through a limited number of queries, deduce which mapping scheme is being used (Scheme1, Scheme2, Scheme3, or Scheme4)
2. After determining the scheme, I will give you a pair of target labels, and you need to calculate the interval between them

## Available Query Types

You can perform the following two types of queries (one at a time):

1. **Distance Query**: Ask for the interval between two different labels X and Y. I will return a non-negative integer.

2. **Comparison Query**: Given two pairs of labels (X, Y) and (U, V), ask which pair has a larger interval. I will return one of three results:
   - "First larger" (interval of X and Y is greater than interval of U and V)
   - "Second larger" (interval of X and Y is less than interval of U and V)
   - "Equal" (both pairs have equal intervals)

## Constraints

- Maximum total queries: {max_queries}
- You must perform at least {min_queries} queries before submitting a scheme determination
- Once you submit a scheme determination, you cannot make any more queries

## Query and Answer Format (must strictly follow)

Each time, only one query or answer tag is allowed.

**Distance Query** (e.g., asking for interval between A and C):
<query_distance>A,C</query_distance>

**Comparison Query** (e.g., comparing intervals of (A,B) and (C,D)):
<query_compare>A,B,C,D</query_compare>

**Submit Scheme Determination** (e.g., determining it's Scheme2):
<answer_scheme>Scheme2</answer_scheme>

**Submit Final Interval Answer** (after I give you the target pair, e.g., answer is 5):
<answer_distance>5</answer_distance>

Note: Labels must be uppercase letters from A to J, separated by commas without extra spaces.
"""

    # ================= 场景化规则 =================

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎使用交通枢纽班次调度推理系统。

## 系统设定
某大型交通枢纽有 10 个按序排列的始发站台，编号为 1 到 10。
目前有 10 条主要公交线路，标识为 A、B、C、D、E、F、G、H、I、J。

这些线路被按照某种隐藏的调度策略分配到这 10 个站台上。系统预设了四种可能的调度方案，但当前生效的方案是未知的。

对于任意两条线路 X 和 Y，它们的“跨度”定义为：它们所在站台之间的间隔站数（即站台编号差的绝对值减 1，端点不计入）。
例如，若线路 X 在 3 号站台，线路 Y 在 7 号站台，则跨度为 |7-3| - 1 = 3。

## 您的任务
1. 通过系统允许的有限次指令调用，分析出当前生效的调度方案（方案1、方案2、方案3 或 方案4）。
2. 在判定调度方案后，系统会下发一对目标线路，您需要准确计算出这两条线路站台之间的跨度。

## 可用指令
您可以调用以下两种指令接口（每次仅限调用一种）：

1. **测距调用**：输入两条不同的线路 X 和 Y，系统将返回它们之间的跨度值（非负整数）。
2. **比较调用**：输入两对线路 (X, Y) 和 (U, V)，系统将对比两对线路的跨度大小，并返回：
   - "前者更大"（X和Y的跨度大于U和V的跨度）
   - "后者更大"（X和Y的跨度小于U和V的跨度）
   - "相等"（两对跨度相等）

## 约束条件
- 指令调用总次数上限为 {max_queries} 次。
- 必须至少进行 {min_queries} 次调用后，才能提交最终方案判定。
- 一旦提交方案判定，系统将锁定，无法再进行任何调用。

## 格式规范（必须严格遵守）
每次交互只能包含一个接口调用或答案标签。

**测距调用**（如查询 A 和 C 的跨度）：
<query_distance>A,C</query_distance>

**比较调用**（如比较 (A,B) 和 (C,D) 的跨度）：
<query_compare>A,B,C,D</query_compare>

**提交方案判定**（如判定当前为方案2）：
<answer_scheme>方案2</answer_scheme>

**提交最终跨度值**（在系统给出目标线路后，例如答案是5）：
<answer_distance>5</answer_distance>

注意：线路标识必须是 A 到 J 的大写字母，用逗号分隔，不要有多余空格。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Transportation Hub Scheduling Reasoning System.

## System Setup
A major transportation hub features an ordered sequence of 10 departure platforms, numbered 1 to 10.
There are 10 main transit lines, identified as A, B, C, D, E, F, G, H, I, J.

These lines are assigned to the 10 platforms according to a hidden scheduling strategy. The system has four possible scheduling schemes, but you do not know which one is currently active.

For any two lines X and Y, their "span" is defined as: the number of interval platforms between their assigned platforms (i.e., the absolute difference between their platform numbers minus 1, excluding the endpoints).
For example, if line X is at platform 3 and line Y is at platform 7, the span is |7-3| - 1 = 3.

## Your Task
1. Through a limited number of command calls, deduce which scheduling scheme is currently active (Scheme1, Scheme2, Scheme3, or Scheme4).
2. After determining the scheme, the system will provide a pair of target lines, and you need to calculate the exact span between them.

## Available Commands
You can invoke the following two types of commands (one at a time):

1. **Distance Call**: Input two different lines X and Y. The system will return their span as a non-negative integer.
2. **Comparison Call**: Input two pairs of lines (X, Y) and (U, V). The system will compare their spans and return:
   - "First larger" (span of X and Y is greater than span of U and V)
   - "Second larger" (span of X and Y is less than span of U and V)
   - "Equal" (both spans are equal)

## Constraints
- Maximum total command calls: {max_queries}.
- You must make at least {min_queries} calls before submitting the scheme determination.
- Once you submit the scheme determination, the system will lock and no further calls can be made.

## Format Requirements (must be strictly followed)
Each interaction must contain exactly one command or answer tag.

**Distance Call** (e.g., querying span between A and C):
<query_distance>A,C</query_distance>

**Comparison Call** (e.g., comparing spans of (A,B) and (C,D)):
<query_compare>A,B,C,D</query_compare>

**Submit Scheme Determination** (e.g., determining it is Scheme2):
<answer_scheme>Scheme2</answer_scheme>

**Submit Final Span Value** (after the system provides the target lines, e.g., if the answer is 5):
<answer_distance>5</answer_distance>

Note: Line identifiers must be uppercase letters from A to J, separated by commas without extra spaces.
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎使用冷链药剂库位推理系统。

## 系统设定
冷链库房内有 10 个按序排列的智能保温箱，编号为 1 到 10。
现接收了 10 种特定疫苗/药剂，标识为 A、B、C、D、E、F、G、H、I、J。

这批药剂按照某种隐藏的温控隔离规则被分配到了这 10 个保温箱中。目前存在四种可能的存放方案，但当前应用的是哪一种尚未知晓。

对于任意两种药剂 X 和 Y，它们的“空箱间隔”定义为：它们所在保温箱之间相隔的箱子数量（即箱子编号差的绝对值减 1，不计入药剂本身的箱子）。
例如，若药剂 X 在 3 号箱，药剂 Y 在 7 号箱，则空箱间隔为 |7-3| - 1 = 3。

## 您的任务
1. 通过有限次的库位检索，分析出当前使用的是哪一种存放方案（方案1、方案2、方案3 或 方案4）。
2. 在判定方案后，系统会指定一对目标药剂，您需要计算它们之间的空箱间隔。

## 可用检索
您可以进行以下两种库位检索（每次只能进行一种）：

1. **测距检索**：输入两种不同药剂 X 和 Y，系统将返回它们之间的空箱间隔（非负整数）。
2. **比较检索**：输入两对药剂 (X, Y) 和 (U, V)，系统将对比哪对药剂的空箱间隔更大，并返回：
   - "前者更大"（X和Y的间隔大于U和V的间隔）
   - "后者更大"（X和Y的间隔小于U和V的间隔）
   - "相等"（两对间隔相等）

## 约束条件
- 检索总次数上限为 {max_queries} 次。
- 必须至少进行 {min_queries} 次检索后，才能提交最终方案判定。
- 一旦提交方案判定，库房检索系统将锁定。

## 格式规范（必须严格遵守）
每次交互仅限包含一个检索或答案标签。

**测距检索**（如查询 A 和 C 的间隔）：
<query_distance>A,C</query_distance>

**比较检索**（如比较 (A,B) 和 (C,D) 的间隔）：
<query_compare>A,B,C,D</query_compare>

**提交方案判定**（如判定当前为方案2）：
<answer_scheme>方案2</answer_scheme>

**提交最终间隔值**（在系统给出目标药剂后，例如答案是5）：
<answer_distance>5</answer_distance>

注意：药剂标识必须是 A 到 J 的大写字母，用逗号分隔，不要有多余空格。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Cold Chain Reagent Storage Reasoning System.

## System Setup
The cold chain facility features an ordered sequence of 10 smart incubators, numbered 1 to 10.
A batch of 10 specific vaccines/reagents, identified as A, B, C, D, E, F, G, H, I, J, has been received.

These reagents are assigned to the 10 incubators according to a hidden temperature-control isolation rule. There are four possible storage schemes, but the currently applied one is unknown.

For any two reagents X and Y, their "incubator interval" is defined as: the number of empty incubators between them (i.e., the absolute difference of their incubator numbers minus 1, excluding the endpoints).
For example, if reagent X is in incubator 3 and reagent Y is in incubator 7, the interval is |7-3| - 1 = 3.

## Your Task
1. Through a limited number of storage queries, deduce which storage scheme is currently in use (Scheme1, Scheme2, Scheme3, or Scheme4).
2. After determining the scheme, the system will specify a pair of target reagents, and you must calculate their incubator interval.

## Available Queries
You can perform the following two types of queries (one at a time):

1. **Distance Query**: Input two different reagents X and Y. The system will return their incubator interval as a non-negative integer.
2. **Comparison Query**: Input two pairs of reagents (X, Y) and (U, V). The system will compare their intervals and return:
   - "First larger" (interval of X and Y is greater than interval of U and V)
   - "Second larger" (interval of X and Y is less than interval of U and V)
   - "Equal" (both intervals are equal)

## Constraints
- Maximum total queries: {max_queries}.
- You must perform at least {min_queries} queries before submitting the scheme determination.
- Once you submit the scheme determination, the storage query system will be locked.

## Format Requirements (must be strictly followed)
Each interaction must contain exactly one query or answer tag.

**Distance Query** (e.g., querying interval between A and C):
<query_distance>A,C</query_distance>

**Comparison Query** (e.g., comparing intervals of (A,B) and (C,D)):
<query_compare>A,B,C,D</query_compare>

**Submit Scheme Determination** (e.g., determining it is Scheme2):
<answer_scheme>Scheme2</answer_scheme>

**Submit Final Interval Value** (after the system gives the target reagents, e.g., if the answer is 5):
<answer_distance>5</answer_distance>

Note: Reagent identifiers must be uppercase letters from A to J, separated by commas without extra spaces.
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎使用标准化考场试卷分配推演系统。

## 系统设定
某考点有 10 个按序排列的标准化考场，编号为 1 到 10。
本次考试共有 10 个不同科目的密封试卷包，科目代码为 A、B、C、D、E、F、G、H、I、J。

考务组按照某种保密分配策略，将这 10 个科目的试卷包分发到了这 10 个考场中。预设了四种分发方案，但你不知晓当前启用的是哪种方案。

对于任意两个科目 X 和 Y，它们的“考场跨度”定义为：它们所在考场之间相隔的考场数量（即考场编号差的绝对值减 1，端点考场不计入）。
例如，若科目 X 的试卷在 3 号考场，科目 Y 的试卷在 7 号考场，则跨度为 |7-3| - 1 = 3。

## 您的任务
1. 通过有限次的考务查询，推演出当前启用的分发方案（方案1、方案2、方案3 或 方案4）。
2. 在判定方案后，系统会给出一对目标科目，您需要精确计算出这两个科目试卷之间的考场跨度。

## 可用查询
您可以进行以下两种查询（每次仅限一种）：

1. **测距查询**：输入两个不同科目 X 和 Y，系统将反馈它们之间的考场跨度（非负整数）。
2. **比较查询**：输入两对科目 (X, Y) 和 (U, V)，系统将比对哪对科目的考场跨度更大，并返回：
   - "前者更大"（X和Y的跨度大于U和V的跨度）
   - "后者更大"（X和Y的跨度小于U和V的跨度）
   - "相等"（两对跨度相等）

## 约束条件
- 考务查询总次数上限为 {max_queries} 次。
- 必须至少执行 {min_queries} 次查询后，方可提交方案判定。
- 提交方案判定后，查询通道将永久关闭。

## 格式规范（必须严格遵守）
每次交互只能包含一个查询或答案标签。

**测距查询**（如查询 A 和 C 的跨度）：
<query_distance>A,C</query_distance>

**比较查询**（如比较 (A,B) 和 (C,D) 的跨度）：
<query_compare>A,B,C,D</query_compare>

**提交方案判定**（如判定为方案2）：
<answer_scheme>方案2</answer_scheme>

**提交最终跨度值**（收到目标科目后，例如答案是5）：
<answer_distance>5</answer_distance>

注意：科目代码必须是 A 到 J 的大写字母，用逗号分隔，不要有多余空格。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Standardized Exam Room Paper Distribution Reasoning System.

## System Setup
A test center has an ordered sequence of 10 standardized exam rooms, numbered 1 to 10.
There are 10 sealed exam paper packages for different subjects, coded A, B, C, D, E, F, G, H, I, J.

The administration has distributed these 10 subject packages to the 10 rooms using a hidden confidential allocation strategy. There are four pre-defined distribution schemes, but you do not know which one is currently active.

For any two subjects X and Y, their "room span" is defined as: the number of rooms between their designated exam rooms (i.e., the absolute difference in room numbers minus 1, excluding the endpoints).
For example, if subject X is in room 3 and subject Y is in room 7, the span is |7-3| - 1 = 3.

## Your Task
1. Through a limited number of administrative queries, deduce the currently active distribution scheme (Scheme1, Scheme2, Scheme3, or Scheme4).
2. After determining the scheme, the system will provide a pair of target subjects, and you must calculate the exact room span between them.

## Available Queries
You can perform the following two types of queries (one at a time):

1. **Distance Query**: Input two different subjects X and Y. The system will return their room span as a non-negative integer.
2. **Comparison Query**: Input two pairs of subjects (X, Y) and (U, V). The system will compare their room spans and return:
   - "First larger" (span of X and Y is greater than span of U and V)
   - "Second larger" (span of X and Y is less than span of U and V)
   - "Equal" (both spans are equal)

## Constraints
- Maximum total administrative queries: {max_queries}.
- You must execute at least {min_queries} queries before submitting the scheme determination.
- Once you submit the scheme determination, the query channel will be permanently closed.

## Format Requirements (must be strictly followed)
Each interaction must contain exactly one query or answer tag.

**Distance Query** (e.g., querying span between A and C):
<query_distance>A,C</query_distance>

**Comparison Query** (e.g., comparing spans of (A,B) and (C,D)):
<query_compare>A,B,C,D</query_compare>

**Submit Scheme Determination** (e.g., determining it is Scheme2):
<answer_scheme>Scheme2</answer_scheme>

**Submit Final Span Value** (after receiving target subjects, e.g., if the answer is 5):
<answer_distance>5</answer_distance>

Note: Subject codes must be uppercase letters from A to J, separated by commas without extra spaces.
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎进入智能装配流水线工位映射诊断系统。

## 系统设定
装配车间的流水线上有 10 个连续排列的工位，编号为 1 到 10。
本次生产需要 10 种核心零部件，标识为 A、B、C、D、E、F、G、H、I、J。

系统根据特定的工艺流程规则，将这些零部件投放到对应的 10 个工位上。存在四种预设的投料方案，但诊断系统暂未明确当前激活的是哪一种。

对于任意两种零部件 X 和 Y，它们的“工位间隔”定义为：它们对应工位之间相隔的工位数（即工位编号差的绝对值减 1，不含首尾工位）。
例如，若零部件 X 在 3 号工位，零部件 Y 在 7 号工位，则间隔为 |7-3| - 1 = 3。

## 您的任务
1. 通过有限次的传感器探测，诊断出当前激活的投料方案（方案1、方案2、方案3 或 方案4）。
2. 诊断出方案后，系统会指定一对目标零部件，您需要精确计算它们之间的工位间隔。

## 可用探测
您可以调用以下两种探测指令（每次仅限一种）：

1. **测距探测**：指定两种不同零部件 X 和 Y，系统将返回它们之间的工位间隔（非负整数）。
2. **比较探测**：指定两对零部件 (X, Y) 和 (U, V)，系统将比对哪对零部件的工位间隔更大，并返回：
   - "前者更大"（X和Y的间隔大于U和V的间隔）
   - "后者更大"（X和Y的间隔小于U和V的间隔）
   - "相等"（两对间隔相等）

## 约束条件
- 探测总次数上限为 {max_queries} 次。
- 必须至少进行 {min_queries} 次探测后，方可提交诊断结果。
- 提交诊断结果后，探测接口将被锁定。

## 格式规范（必须严格遵守）
每次交互只能包含一个探测或答案标签。

**测距探测**（如查询 A 和 C 的间隔）：
<query_distance>A,C</query_distance>

**比较探测**（如比较 (A,B) 和 (C,D) 的间隔）：
<query_compare>A,B,C,D</query_compare>

**提交方案判定**（如诊断为方案2）：
<answer_scheme>方案2</answer_scheme>

**提交最终间隔值**（获取目标零部件后，例如答案是5）：
<answer_distance>5</answer_distance>

注意：零部件标识必须是 A 到 J 的大写字母，用逗号分隔，不要有多余空格。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart Assembly Line Station Mapping Diagnostic System.

## System Setup
The assembly line in the workshop features 10 consecutive workstations, numbered 1 to 10.
The current production requires 10 core components, identified as A, B, C, D, E, F, G, H, I, J.

The system allocates these components to the 10 workstations according to a specific process flow rule. There are four preset feeding schemes, but the diagnostic system does not currently know which one is activated.

For any two components X and Y, their "station interval" is defined as: the number of workstations between them (i.e., the absolute difference in workstation numbers minus 1, excluding the endpoints).
For example, if component X is at station 3 and component Y is at station 7, the interval is |7-3| - 1 = 3.

## Your Task
1. Through a limited number of sensor probes, diagnose the currently activated feeding scheme (Scheme1, Scheme2, Scheme3, or Scheme4).
2. After diagnosing the scheme, the system will specify a pair of target components, and you must calculate the exact station interval between them.

## Available Probes
You can invoke the following two probing commands (one at a time):

1. **Distance Probe**: Specify two different components X and Y. The system will return their station interval as a non-negative integer.
2. **Comparison Probe**: Specify two pairs of components (X, Y) and (U, V). The system will compare their station intervals and return:
   - "First larger" (interval of X and Y is greater than interval of U and V)
   - "Second larger" (interval of X and Y is less than interval of U and V)
   - "Equal" (both intervals are equal)

## Constraints
- Maximum total probes: {max_queries}.
- You must perform at least {min_queries} probes before submitting the diagnostic result.
- Once the diagnostic result is submitted, the probing interface will be locked.

## Format Requirements (must be strictly followed)
Each interaction must contain exactly one probe or answer tag.

**Distance Probe** (e.g., querying interval between A and C):
<query_distance>A,C</query_distance>

**Comparison Probe** (e.g., comparing intervals of (A,B) and (C,D)):
<query_compare>A,B,C,D</query_compare>

**Submit Scheme Determination** (e.g., diagnosing it is Scheme2):
<answer_scheme>Scheme2</answer_scheme>

**Submit Final Interval Value** (after obtaining target components, e.g., if the answer is 5):
<answer_distance>5</answer_distance>

Note: Component identifiers must be uppercase letters from A to J, separated by commas without extra spaces.
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎使用法院档案室卷宗定位分析系统。

## 系统设定
档案室内有 10 个按序排列的智能密集架，编号为 1 到 10。
现存有 10 类不同案由的诉讼卷宗，案件类型代码为 A、B、C、D、E、F、G、H、I、J。

这些卷宗依据某种机密归档规则，被分配到这 10 个密集架中。系统内置了四种归档方案，但当前生效的是哪一种处于未知状态。

对于任意两类卷宗 X 和 Y，它们的“架次跨度”定义为：存放这两个类目的密集架之间相隔的架子数量（即架子编号差的绝对值减 1，端点密集架不计入）。
例如，若卷宗 X 在 3 号架，卷宗 Y 在 7 号架，则架次跨度为 |7-3| - 1 = 3。

## 您的任务
1. 通过有限次的调卷查询，分析出当前的归档方案（方案1、方案2、方案3 或 方案4）。
2. 判定方案后，系统会指定一对目标案件类型，您需要推算出这两类卷宗的架次跨度。

## 可用查询
您可以进行以下两种调卷查询（每次仅限一种）：

1. **测距查询**：输入两类不同卷宗 X 和 Y，系统将返回它们的架次跨度（非负整数）。
2. **比较查询**：输入两对卷宗类型 (X, Y) 和 (U, V)，系统将比对哪对卷宗的架次跨度更大，并返回：
   - "前者更大"（X和Y的跨度大于U和V的跨度）
   - "后者更大"（X和Y的跨度小于U和V的跨度）
   - "相等"（两对跨度相等）

## 约束条件
- 调卷查询总次数上限为 {max_queries} 次。
- 必须至少进行 {min_queries} 次查询后，才能提交归档方案判定。
- 一旦提交判定，查卷系统将自动冻结。

## 格式规范（必须严格遵守）
每次交互仅限包含一个查询或答案标签。

**测距查询**（如查询 A 和 C 的跨度）：
<query_distance>A,C</query_distance>

**比较查询**（如比较 (A,B) 和 (C,D) 的跨度）：
<query_compare>A,B,C,D</query_compare>

**提交方案判定**（如判定当前为方案2）：
<answer_scheme>方案2</answer_scheme>

**提交最终跨度值**（收到目标案件类型后，例如答案是5）：
<answer_distance>5</answer_distance>

注意：卷宗代码必须是 A 到 J 的大写字母，用逗号分隔，不要有多余空格。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Court Archive Case File Location Analysis System.

## System Setup
The archive room contains an ordered sequence of 10 smart mobile shelving units, numbered 1 to 10.
There are 10 categories of litigation case files, with case type codes A, B, C, D, E, F, G, H, I, J.

These files are distributed across the 10 shelving units according to a confidential filing rule. The system has four built-in filing schemes, but the currently active one is unknown.

For any two case types X and Y, their "shelving span" is defined as: the number of shelving units between them (i.e., the absolute difference in unit numbers minus 1, excluding the endpoints).
For example, if case file X is in unit 3 and case file Y is in unit 7, the span is |7-3| - 1 = 3.

## Your Task
1. Through a limited number of file retrieval queries, deduce the current filing scheme (Scheme1, Scheme2, Scheme3, or Scheme4).
2. After determining the scheme, the system will specify a pair of target case types, and you need to calculate the shelving span between them.

## Available Queries
You can perform the following two types of retrieval queries (one at a time):

1. **Distance Query**: Input two different case types X and Y. The system will return their shelving span as a non-negative integer.
2. **Comparison Query**: Input two pairs of case types (X, Y) and (U, V). The system will compare their shelving spans and return:
   - "First larger" (span of X and Y is greater than span of U and V)
   - "Second larger" (span of X and Y is less than span of U and V)
   - "Equal" (both spans are equal)

## Constraints
- Maximum total retrieval queries: {max_queries}.
- You must perform at least {min_queries} queries before submitting the scheme determination.
- Once you submit the determination, the query system will automatically freeze.

## Format Requirements (must be strictly followed)
Each interaction must contain exactly one query or answer tag.

**Distance Query** (e.g., querying span between A and C):
<query_distance>A,C</query_distance>

**Comparison Query** (e.g., comparing spans of (A,B) and (C,D)):
<query_compare>A,B,C,D</query_compare>

**Submit Scheme Determination** (e.g., determining it is Scheme2):
<answer_scheme>Scheme2</answer_scheme>

**Submit Final Span Value** (after receiving target case types, e.g., if the answer is 5):
<answer_distance>5</answer_distance>

Note: Case codes must be uppercase letters from A to J, separated by commas without extra spaces.
"""

    # ================= 场景化规则结束 =================

    tags = ["query_distance", "query_compare", "answer_scheme", "answer_distance", "answer"]

    user_prompt_zh = "你可以开始第一次查询了。"
    user_prompt_en = "You can start your first query now."

    reasoning_type = "溯因推理"
    data_structure = "序列"

    # 五种难度配置
    # 1 (简单): 最多5次查询，至少2次，方案1（正序）
    # 2 (中等偏下): 最多5次查询，至少2次，方案2（逆序）
    # 3 (中等偏上): 最多5次查询，至少3次，方案3（循环右移2）
    # 4 (较难): 最多4次查询，至少2次，方案4（奇偶分组）
    # 5 (难): 最多4次查询，至少3次，方案3（循环右移2）
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "max_queries": 5,
                "min_queries": 2,
                "scheme": "方案1",
                "target_pair": "A,E",  # 目标标签对
            },
            2: {
                "max_queries": 5,
                "min_queries": 2,
                "scheme": "方案2",
                "target_pair": "B,H",
            },
            3: {
                "max_queries": 5,
                "min_queries": 3,
                "scheme": "方案3",
                "target_pair": "C,I",
            },
            4: {
                "max_queries": 4,
                "min_queries": 2,
                "scheme": "方案4",
                "target_pair": "A,J",
            },
            5: {
                "max_queries": 4,
                "min_queries": 3,
                "scheme": "方案3",
                "target_pair": "D,J",
            },
        },
        "en": {
            1: {
                "max_queries": 5,
                "min_queries": 2,
                "scheme": "Scheme1",
                "target_pair": "A,E",
            },
            2: {
                "max_queries": 5,
                "min_queries": 2,
                "scheme": "Scheme2",
                "target_pair": "B,H",
            },
            3: {
                "max_queries": 5,
                "min_queries": 3,
                "scheme": "Scheme3",
                "target_pair": "C,I",
            },
            4: {
                "max_queries": 4,
                "min_queries": 2,
                "scheme": "Scheme4",
                "target_pair": "A,J",
            },
            5: {
                "max_queries": 4,
                "min_queries": 3,
                "scheme": "Scheme3",
                "target_pair": "D,J",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置和状态"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保difficulty为整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["max_queries"] = cfg["max_queries"]
        self._game_info["min_queries"] = cfg["min_queries"]
        
        # 当前使用的方案
        self.ground_truth_scheme = cfg["scheme"]
        
        # 目标标签对（在判定方案后给出）
        self.target_pair = cfg["target_pair"]
        
        # 初始化位置映射（根据方案）
        self._init_position_mapping()
        
        # 查询计数器
        self.query_count = 0
        
        # 是否已经判定方案
        self.scheme_determined = False
        
        # 是否已经给出目标标签对
        self.target_given = False

    def _init_position_mapping(self):
        """根据真实方案初始化标签到位置的映射"""
        # 标签索引映射：A=1, B=2, ..., J=10
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        
        self.pos_map = {}
        scheme_name = self.ground_truth_scheme.replace("Scheme", "方案")
        
        for i, label in enumerate(labels, start=1):
            if scheme_name == "方案1":
                # 正序：pos(i) = i
                self.pos_map[label] = i
            elif scheme_name == "方案2":
                # 逆序：pos(i) = 11 - i
                self.pos_map[label] = 11 - i
            elif scheme_name == "方案3":
                # 循环右移2：pos(i) = ((i - 1 + 2) % 10) + 1
                self.pos_map[label] = ((i - 1 + 2) % 10) + 1
            elif scheme_name == "方案4":
                # 奇偶分组：奇数 (i+1)/2，偶数 5+i/2
                if i % 2 == 1:
                    self.pos_map[label] = (i + 1) // 2
                else:
                    self.pos_map[label] = 5 + i // 2
            else:
                raise ValueError(f"Unknown scheme: {scheme_name}")

    def _calculate_distance(self, label1, label2):
        """计算两个标签之间的间隔"""
        pos1 = self.pos_map[label1]
        pos2 = self.pos_map[label2]
        return abs(pos1 - pos2) - 1

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        if "answer_scheme" in parsed_info:
            user_scheme = parsed_info["answer_scheme"].strip()
            
            # 标准化方案名称
            scheme_map = {
                "方案1": "Scheme1", "Scheme1": "Scheme1",
                "方案2": "Scheme2", "Scheme2": "Scheme2",
                "方案3": "Scheme3", "Scheme3": "Scheme3",
                "方案4": "Scheme4", "Scheme4": "Scheme4",
            }
            
            normalized_user = scheme_map.get(user_scheme)
            normalized_truth = scheme_map.get(self.ground_truth_scheme)
            
            return normalized_user == normalized_truth
            
        elif "answer_distance" in parsed_info or "answer" in parsed_info:
            # 如果 scheme 尚未通过正常流程判定，但模型直接给出了距离答案，
            # 仍然尝试验证（兼容 redundancy 评估等外部调用场景）
            try:
                raw = parsed_info.get("answer_distance", parsed_info.get("answer", "")).strip()
                user_distance = int(raw)
                labels = self.target_pair.split(",")
                correct_distance = self._calculate_distance(labels[0], labels[1])
                return user_distance == correct_distance
            except:
                return False
        
        return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑，用于产生真实的查询结果"""
        # 检查查询次数限制
        if not self.scheme_determined and self.query_count >= self._game_info["max_queries"]:
            raise ValueError("Query limit exceeded" if self.config.language == "en" else "查询次数超限")
        
        # 如果已经判定方案，不允许再查询
        if self.scheme_determined and ("query_distance" in parsed_info or "query_compare" in parsed_info):
            raise ValueError("Cannot query after scheme determination" if self.config.language == "en" 
                           else "判定方案后不能再进行查询")
        
        # 测距查询
        if "query_distance" in parsed_info:
            try:
                raw = parsed_info["query_distance"].strip()
                labels = [x.strip() for x in raw.split(",")]
                
                if len(labels) != 2:
                    raise ValueError("Invalid format")
                
                label1, label2 = labels
                
                if label1 not in self.pos_map or label2 not in self.pos_map:
                    raise ValueError("Invalid label")
                
                if label1 == label2:
                    raise ValueError("Labels must be different")
                
                self.query_count += 1
                distance = self._calculate_distance(label1, label2)
                return str(distance)
                
            except Exception as e:
                raise ValueError("Invalid distance query format" if self.config.language == "en"
                               else "测距查询格式错误")
        
        # 比较查询
        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"].strip()
                labels = [x.strip() for x in raw.split(",")]
                
                if len(labels) != 4:
                    raise ValueError("Invalid format")
                
                x, y, u, v = labels
                
                for label in [x, y, u, v]:
                    if label not in self.pos_map:
                        raise ValueError("Invalid label")
                
                if x == y or u == v:
                    raise ValueError("Pairs must have different labels")
                
                self.query_count += 1
                
                dist_xy = self._calculate_distance(x, y)
                dist_uv = self._calculate_distance(u, v)
                
                if self.config.language == "zh":
                    if dist_xy > dist_uv:
                        return "前者更大"
                    elif dist_xy < dist_uv:
                        return "后者更大"
                    else:
                        return "相等"
                else:
                    if dist_xy > dist_uv:
                        return "First larger"
                    elif dist_xy < dist_uv:
                        return "Second larger"
                    else:
                        return "Equal"
                
            except Exception as e:
                raise ValueError("Invalid comparison query format" if self.config.language == "en"
                               else "比较查询格式错误")
        
        else:
            raise ValueError("No valid query tag found" if self.config.language == "en"
                           else "未找到有效的查询标签")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误的答案"""
        if correct.isdigit():
            val = int(correct)
            # 确保生成的错误答案不同且非负
            return str(val + 1) if val < 9 else str(val - 1)
        
        # 比较查询结果的替换
        compare_swaps = {
            "前者更大": "后者更大",
            "后者更大": "前者更大",
            "相等": "前者更大",
            "First larger": "Second larger",
            "Second larger": "First larger",
            "Equal": "First larger",
        }
        
        if correct in compare_swaps:
            return compare_swaps[correct]
        
        # 通用替换
        swaps = {
            "是": "否", "否": "是",
            "Yes": "No", "No": "Yes",
            "yes": "no", "no": "yes"
        }
        
        if correct in swaps:
            return swaps[correct]
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，包含完整的xml标签
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        
        # 生成所有唯一对 (L1, L2) 其中 index(L1) < index(L2)
        # 这样确保了查询中的两个标签是不同的
        pairs = []
        for i in range(len(labels)):
            for j in range(i + 1, len(labels)):
                pairs.append((labels[i], labels[j]))
        
        # 1. 测距查询
        for p in pairs:
            # 构造查询字符串 <query_distance>A,B</query_distance>
            query_content = f"{p[0]},{p[1]}"
            query_str = f"<query_distance>{query_content}</query_distance>"
            
            # 计算答案
            dist = self._calculate_distance(p[0], p[1])
            answer_str = str(dist)
            
            queries.append({"query": query_str, "answer": answer_str})
            
        return queries

    def step(self, response: str):
        """处理一步交互"""
        try:
            parsed_info = self.parse(response)
            
            # 处理方案判定
            if "answer_scheme" in parsed_info:
                # 先检查查询次数是否满足最低要求
                if self.query_count < self._game_info["min_queries"]:
                    if self.config.language == "zh":
                        res = f"查询次数不足，至少需要 {self._game_info['min_queries']} 次查询后才能提交方案判定。当前已查询 {self.query_count} 次。请继续查询。"
                    else:
                        res = (f"Insufficient queries. You must perform at least {self._game_info['min_queries']} "
                               f"queries before submitting. Current query count: {self.query_count}. Please continue querying.")
                    self.state.add_message("user", res)
                    return self.state
                
                is_success = self.evaluate(parsed_info)
                
                if is_success:
                    self.scheme_determined = True
                    self.target_given = True
                    
                    if self.config.language == "zh":
                        res = f"方案判定正确！现在请计算以下标签对的间隔：{self.target_pair}"
                    else:
                        res = f"Scheme determination correct! Now calculate the interval for: {self.target_pair}"
                    
                    self.state.add_message("user", res)
                else:
                    if self.config.language == "zh":
                        res = "方案判定错误"
                    else:
                        res = "Scheme determination incorrect"
                    self.state.set_state("failed", "incorrect scheme")
                    self.state.add_message("user", res)
            
            # 处理最终间隔答案
            elif "answer_distance" in parsed_info or "answer" in parsed_info:
                is_success = self.evaluate(parsed_info)
                
                if is_success:
                    res = "答案正确" if self.config.language == "zh" else "Correct answer."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                    self.state.set_state("failed", "incorrect distance")
                    self.state.add_message("user", res)
            
            # 处理查询
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state