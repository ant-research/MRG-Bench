# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   元素排名：某元素在排序后处于第几位
# ============================================================

from .base import Game
import random
import itertools
import re


class GAME495(Game):

    game_rule_zh = """\
我们来玩一个"隐藏排序规则"的推理游戏，规则如下：

游戏设定了一组大小为 {n} 的离散对象，每个对象具有：
- 一个唯一标识符 ID（从 1 到 {n}）
- 一个公开且互不相同的码（固定长度的数字字符串）

存在一个对所有对象一致的、固定的、保密的确定性函数 f(code)，对每个对象的 code 计算排序键。全体对象按键值升序排列；若键值相同，则按 code 的字典序（从小到大）作为唯一且稳定的并列打破规则，从而形成一个严格的全序。

## 初始公开信息

对象列表：
{objects_list}

目标对象 ID：{target_id}

## 你的任务

确定目标对象在全体 {n} 个对象按隐藏规则排序后的全局名次 R（R 为 1 到 {n} 的整数）。

## 允许的查询类型

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据隐藏的排序规则如实回答：

1. **成对比较**：询问对象 X 和对象 Y 在全序下的相对位置。
   - 回答："X 在 Y 前"或"Y 在 X 前"

2. **小批量排序**：询问一组对象（2 到 4 个）在全序下的完整排序。
   - 回答：该子集按全序排序后的 ID 列表

3. **局部名次**：询问对象 X 在指定子集（2 到 4 个，包含 X）中的局部名次。
   - 回答：X 在该子集中的位置（1 到子集大小的整数）

## 约束

- 每次查询的对象 ID 必须互不相同，且来自已公布的 {n} 个对象
- 任何一次查询的子集规模最多为 4
- 不允许对全体对象进行直接或等价的整体排序查询
- 请尽可能少地使用查询次数

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成对比较（例如比较 ID 1 和 ID 3）：
<query_compare>1,3</query_compare>

- 小批量排序（例如对 ID 1、3、5 进行排序）：
<query_sort>1,3,5</query_sort>

- 局部名次（例如询问 ID 2 在子集 [2,4,6] 中的名次）：
<query_rank>2 in 2,4,6</query_rank>

提交最终答案时，请给出目标对象的全局名次（1 到 {n} 的整数），格式如下：

<answer>5</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Sorting Rule" deduction game. Here are the rules:

There is a set of {n} discrete objects, each with:
- A unique identifier ID (from 1 to {n})
- A public and distinct code (a fixed-length numeric string)

There exists a consistent, fixed, secret deterministic function f(code) that computes a sort key for each object's code. All objects are arranged in ascending order by key value; if key values are equal, lexicographic order of codes (ascending) serves as the unique and stable tiebreaker, forming a strict total order.

## Initial Public Information

Object list:
{objects_list}

Target object ID: {target_id}

## Your Task

Determine the global rank R of the target object in the total order of all {n} objects (R is an integer from 1 to {n}).

## Allowed Query Types

You can repeatedly ask me the following three types of questions (one per turn), and I will answer truthfully according to the hidden sorting rule:

1. **Pairwise Comparison**: Ask the relative position of object X and object Y in the total order.
   - Answer: "X before Y" or "Y before X"

2. **Small Batch Sort**: Ask for the complete ordering of a subset (2 to 4 objects) in the total order.
   - Answer: The ID list of that subset sorted by the total order

3. **Local Rank**: Ask for the local rank of object X within a specified subset (2 to 4 objects, including X).
   - Answer: The position of X in that subset (an integer from 1 to subset size)

## Constraints

- Each query's object IDs must be distinct and from the published {n} objects
- Any single query's subset size is at most 4
- Direct or equivalent whole-set sorting queries are not allowed
- Please use as few queries as possible

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Pairwise Comparison (e.g., comparing ID 1 and ID 3):
<query_compare>1,3</query_compare>

- Small Batch Sort (e.g., sorting IDs 1, 3, 5):
<query_sort>1,3,5</query_sort>

- Local Rank (e.g., asking for rank of ID 2 in subset [2,4,6]):
<query_rank>2 in 2,4,6</query_rank>

When submitting the final answer, provide the global rank of the target object (an integer from 1 to {n}), using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通调度中心正在进行一项“隐藏优先权分配”校准演练，规则如下：

演练设定了一组规模为 {n} 的自动驾驶车辆，每辆车具备：
- 一个唯一调度 ID（从 1 到 {n}）
- 一串公开且互不相同的环境特征码（固定长度的数字字符串）

系统调度内核包含一个统一、固定的机密评估函数 f(code)，计算各车辆的通行权权重。所有车辆按权重值升序编排发车顺序（权重越小越优先）；若权重相同，则以特征码的字典序（从小到大）作为唯一的顺位打破规则，形成严格的绝对通行队列。

## 初始公开信息

车辆列表：
{objects_list}

目标车辆 ID：{target_id}

## 你的任务

确定目标车辆在全体 {n} 辆车按隐藏规则排定后的全局绝对通行名次 R（R 为 1 到 {n} 的整数）。

## 允许的查询类型

你可以反复向调度系统提出以下三类查询（每次仅限一个问题），系统将根据隐藏的调度规则如实反馈：

1. **成对比较**：询问车辆 X 和车辆 Y 在全局队列中的相对发车顺序。
   - 回答："X 在 Y 前"或"Y 在 X 前"

2. **小批量排序**：询问一个微型车队（2 到 4 辆车）在全局队列中的完整发车顺序。
   - 回答：该车队按发车队列排序后的 ID 列表

3. **局部名次**：询问车辆 X 在指定编队（2 到 4 辆车，包含 X）中的局部放行顺位。
   - 回答：X 在该编队中的顺位（1 到编队大小的整数）

## 约束

- 每次查询的车辆 ID 必须互不相同，且来自已广播的 {n} 辆车
- 任何一次查询的编队规模最多为 4
- 不允许对全体车辆进行直接或等价的整体放行查询
- 请尽可能少地消耗查询频次

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成对比较（例如比较车辆 ID 1 和 3）：
<query_compare>1,3</query_compare>

- 小批量排序（例如对车辆 ID 1、3、5 进行排序）：
<query_sort>1,3,5</query_sort>

- 局部名次（例如询问车辆 ID 2 在编队 [2,4,6] 中的顺位）：
<query_rank>2 in 2,4,6</query_rank>

提交最终答案时，请给出目标车辆的全局通行名次（1 到 {n} 的整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Intelligent Traffic Control Center is conducting a "Hidden Priority Allocation" calibration drill. Here are the rules:

The drill involves a set of {n} autonomous vehicles, each equipped with:
- A unique dispatch ID (from 1 to {n})
- A public and distinct environmental feature code (a fixed-length numeric string)

The dispatch kernel incorporates a consistent, fixed, and classified evaluation function f(code) that computes a right-of-way weight for each vehicle's code. All vehicles are arranged in ascending order by weight for departure (lower weight means higher priority); if weights are equal, the lexicographic order of codes (ascending) serves as the unique tiebreaker, forming a strict absolute departure queue.

## Initial Public Information

Vehicle list:
{objects_list}

Target vehicle ID: {target_id}

## Your Task

Determine the global departure rank R of the target vehicle in the strict queue of all {n} vehicles (R is an integer from 1 to {n}).

## Allowed Query Types

You can repeatedly send the following three types of queries to the dispatch system (one per turn), and the system will answer truthfully according to the hidden traffic rule:

1. **Pairwise Comparison**: Ask the relative departure sequence of vehicle X and vehicle Y in the total queue.
   - Answer: "X before Y" or "Y before X"

2. **Small Batch Sort**: Ask for the complete departure order of a micro-fleet (2 to 4 vehicles) based on the absolute queue.
   - Answer: The ID list of that fleet sorted by the departure queue

3. **Local Rank**: Ask for the local departure position of vehicle X within a specified formation (2 to 4 vehicles, including X).
   - Answer: The position of X in that formation (an integer from 1 to formation size)

## Constraints

- Each query's vehicle IDs must be distinct and from the broadcasted {n} vehicles
- Any single query's formation size is at most 4
- Direct or equivalent whole-fleet sorting queries are prohibited
- Please minimize the consumption of query frequency

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Pairwise Comparison (e.g., comparing vehicle IDs 1 and 3):
<query_compare>1,3</query_compare>

- Small Batch Sort (e.g., sorting vehicle IDs 1, 3, 5):
<query_sort>1,3,5</query_sort>

- Local Rank (e.g., asking for the rank of ID 2 in formation [2,4,6]):
<query_rank>2 in 2,4,6</query_rank>

When submitting the final answer, provide the global departure rank of the target vehicle (an integer from 1 to {n}), using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_2 = """\
基因组学实验室正在对医疗测序仪的“样本盲序排队”机制进行校准，规则如下：

待处理流水线上有 {n} 份基因样本，每份样本具有：
- 一个唯一的试管 ID（从 1 到 {n}）
- 一串公开且互不相同的分子特征码（固定长度的数字字符串）

测序仪底层置入了一个对所有样本一致、固定的保密降解评估函数 f(code)，计算各样本的上机优先级键值。全体样本按键值升序排列（键值越小越急迫）；若键值相同，则按特征码的字典序（从小到大）作为唯一的打破并列规则，从而建立严格的先后处理时序。

## 初始公开信息

样本列表：
{objects_list}

目标样本试管 ID：{target_id}

## 你的任务

确定目标样本在全体 {n} 份样本按隐秘降解规则排定后的全局上机绝对名次 R（R 为 1 到 {n} 的整数）。

## 允许的查询类型

你可以反复向仪器总线发出以下三类指令（每次仅限一个指令），仪器会根据底层时序规则如实反馈：

1. **成对比较**：核实样本 X 和样本 Y 上机测序的相对先后顺序。
   - 回答："X 在 Y 前"或"Y 在 X 前"

2. **小批量排序**：请求一簇微孔板样本（2 到 4 份样本）的完整内部处理顺序。
   - 回答：该子集按上机要求排序后的试管 ID 列表

3. **局部名次**：查询样本 X 在指定子集（2 到 4 份样本，包含 X）中的优先顺位。
   - 回答：X 在该子集中的顺位（1 到子集大小的整数）

## 约束

- 每次查询的试管 ID 必须互不相同，且来自已记录的 {n} 份样本
- 任何一次查询的子集规模最多为 4
- 不允许对全部样本进行直接或等价的整体测序排班查询
- 请尽可能少地使用总线查询次数

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成对比较（例如比较试管 ID 1 和 3）：
<query_compare>1,3</query_compare>

- 小批量排序（例如对试管 ID 1、3、5 进行测序排序）：
<query_sort>1,3,5</query_sort>

- 局部名次（例如询问试管 ID 2 在子集 [2,4,6] 中的顺位）：
<query_rank>2 in 2,4,6</query_rank>

提交最终答案时，请给出目标样本的全局测序名次（1 到 {n} 的整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The genomics laboratory is calibrating the "Blind Sequencing Queue" mechanism of the medical sequencer. Here are the rules:

There are {n} genetic samples on the processing pipeline, each with:
- A unique test tube ID (from 1 to {n})
- A public and distinct molecular feature code (a fixed-length numeric string)

The sequencer firmware includes a consistent, fixed, and confidential degradation evaluation function f(code) that computes a sequencing priority key for each sample. All samples are ordered in ascending order by key (smaller keys mean higher urgency); if keys are equal, the lexicographic order of codes (ascending) serves as the unique tiebreaker, establishing a strict processing sequence.

## Initial Public Information

Sample list:
{objects_list}

Target sample tube ID: {target_id}

## Your Task

Determine the global sequencing rank R of the target sample among all {n} samples (R is an integer from 1 to {n}).

## Allowed Query Types

You can repeatedly send the following three types of instructions to the instrument bus (one per turn), and the system will answer truthfully according to the underlying sequencing rule:

1. **Pairwise Comparison**: Verify the relative sequencing order of sample X and sample Y.
   - Answer: "X before Y" or "Y before X"

2. **Small Batch Sort**: Request the complete internal processing sequence of a microplate cluster (2 to 4 samples).
   - Answer: The tube ID list of that cluster sorted by the sequencing sequence

3. **Local Rank**: Ask for the priority position of sample X within a specified subset (2 to 4 samples, including X).
   - Answer: The position of X in that subset (an integer from 1 to subset size)

## Constraints

- Each query's tube IDs must be distinct and from the recorded {n} samples
- Any single query's cluster size is at most 4
- Direct or equivalent whole-batch sequencing schedule queries are not allowed
- Please minimize the use of bus query counts

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Pairwise Comparison (e.g., comparing tube IDs 1 and 3):
<query_compare>1,3</query_compare>

- Small Batch Sort (e.g., sorting tube IDs 1, 3, 5):
<query_sort>1,3,5</query_sort>

- Local Rank (e.g., asking for the rank of tube ID 2 in subset [2,4,6]):
<query_rank>2 in 2,4,6</query_rank>

When submitting the final answer, provide the global sequencing rank of the target sample (an integer from 1 to {n}), using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_3 = """\
教务评估系统当前正在执行一次“匿存档案盲审基准”计算，规则如下：

系统内录入了 {n} 份匿名学生综合素质测评档案，每份档案具备：
- 一个独立的档案编号 ID（从 1 到 {n}）
- 一组公开的标准化量化评估码（互不相同的固定长度数字字符串）

系统后台运用了一个未公开的综合评价函数 f(code) 来生成每份档案的基准排序值。全体档案按基准值升序进行综合名次编排；当基准值持平时，则依据评估码的字典序（从小到大）进行唯一稳定的裁决，从而得出严格的班级总评顺位。

## 初始公开信息

档案列表：
{objects_list}

目标档案编号 ID：{target_id}

## 你的任务

推演出目标档案在全部 {n} 份档案中经过系统综合评定后的全局确切排位 R（R 为 1 到 {n} 的整数）。

## 允许的查询类型

你可以反复向教务系统数据库提请以下三种数据比对（每次仅限一个查询），系统将按内置评价规则如实返回：

1. **成对比较**：查询档案 X 与档案 Y 在全景综合顺位中的相对优劣次序。
   - 回答："X 在 Y 前"或"Y 在 X 前"

2. **小批量排序**：圈定一个研讨小组（2 到 4 份档案），查询其内部的完整排位结果。
   - 回答：该小组按综合评定排序后的档案 ID 列表

3. **局部名次**：指定档案 X 并在自选的对照组（2 到 4 份档案，包含 X）内，查询其相对名次。
   - 回答：X 在该对照组中的名次（1 到对照组大小的整数）

## 约束

- 每次查询涉及的档案 ID 不可重复，且仅限于已公布的 {n} 份档案
- 任何一次比对的对照组规模至多为 4 份档案
- 禁止对全体档案列表发起直接或变相的整体排名拉取
- 请以最少的数据比对次数完成任务

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成对比较（例如比对档案 ID 1 和 3）：
<query_compare>1,3</query_compare>

- 小批量排序（例如对档案 ID 1、3、5 的小组进行排名）：
<query_sort>1,3,5</query_sort>

- 局部名次（例如询问档案 ID 2 在对照组 [2,4,6] 中的名次）：
<query_rank>2 in 2,4,6</query_rank>

提交最终答案时，请给出目标档案的全局综合排位（1 到 {n} 的整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The academic evaluation system is currently executing a "Blind Review Benchmark" calculation for anonymous profiles. Here are the rules:

The system has registered {n} anonymous student comprehensive assessment profiles, each equipped with:
- A unique profile ID (from 1 to {n})
- A set of public standardized quantitative assessment codes (distinct, fixed-length numeric strings)

The backend utilizes an undisclosed comprehensive evaluation function f(code) to generate a baseline sorting value for each profile. All profiles are ranked in ascending order by their baseline values; in the event of a tie, the lexicographic order of the assessment codes (ascending) acts as the unique and stable tiebreaker, yielding a strict overall class ranking.

## Initial Public Information

Profile list:
{objects_list}

Target profile ID: {target_id}

## Your Task

Deduce the exact global ranking R of the target profile among all {n} profiles after the system's comprehensive evaluation (R is an integer from 1 to {n}).

## Allowed Query Types

You may repeatedly submit the following three types of data comparisons to the academic database (one query per turn), and the system will respond truthfully based on the built-in evaluation rules:

1. **Pairwise Comparison**: Check the relative ranking order of profile X and profile Y in the global landscape.
   - Answer: "X before Y" or "Y before X"

2. **Small Batch Sort**: Select a seminar group (2 to 4 profiles) and request its complete internal ranking result.
   - Answer: The profile ID list of that group sorted by comprehensive evaluation

3. **Local Rank**: Check the relative rank of profile X within a self-selected control group (2 to 4 profiles, including X).
   - Answer: The position of X in that control group (an integer from 1 to group size)

## Constraints

- Profile IDs in each query must be distinct and chosen from the published {n} profiles
- The size of the control group in any single comparison is at most 4 profiles
- Direct or disguised whole-list ranking extraction queries are strictly prohibited
- Please complete the task with the minimum number of data comparisons

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Pairwise Comparison (e.g., comparing profile IDs 1 and 3):
<query_compare>1,3</query_compare>

- Small Batch Sort (e.g., ranking seminar group with profile IDs 1, 3, 5):
<query_sort>1,3,5</query_sort>

- Local Rank (e.g., asking for the rank of profile ID 2 in control group [2,4,6]):
<query_rank>2 in 2,4,6</query_rank>

When submitting the final answer, provide the global exact ranking of the target profile (an integer from 1 to {n}), using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_4 = """\
智能制造基地的质检中枢正在执行“隐式探伤批次排期”，流水线规则如下：

当前抽检批次包含 {n} 个精密机械零件，每个零件携带：
- 一个唯一的流水线追踪 ID（从 1 到 {n}）
- 一串公开且独一无二的物料光谱码（固定长度的数字字符串）

智能质检中枢内嵌了一套核心机密的应力疲劳函数 f(code) 来测算每个零件的检测次序键值。所有零件严格按键值升序被送入探伤舱（键值越小越早进舱）；倘若键值等同，则依照光谱码的字典序（从小到大）进行托底排序，由此得出不可更改的绝对质检次序。

## 初始公开信息

零件批次列表：
{objects_list}

目标零件追踪 ID：{target_id}

## 你的任务

精准锁定目标零件在全批次 {n} 个零件中被排定的全局绝对质检位次 R（R 为 1 到 {n} 的整数）。

## 允许的查询类型

你可以反复通过工控机向质检中枢发起以下三种抽查指令（每次仅限一个指令），中枢将按隐藏排期如实回传数据：

1. **成对比较**：校验零件 X 和零件 Y 进入探伤舱的先后时序。
   - 回答："X 在 Y 前"或"Y 在 X 前"

2. **小批量排序**：截取 2 到 4 个零件作为一个上料架子集，索取该架的精确检测顺序。
   - 回答：该上料架按检测次序排序后的追踪 ID 列表

3. **局部名次**：指定零件 X 并查询其在某个托盘合集（2 到 4 个零件，包含 X）内的局部位次。
   - 回答：X 在该托盘合集中的顺位（1 到合集大小的整数）

## 约束

- 每次抽查的追踪 ID 必须相互独立，且来源于已登记的 {n} 个零件
- 任一抽查指令的合集零件数最高不能超过 4 个
- 严禁调取或通过变通手段请求整条流水线的全量质检排期表
- 请尽最大努力压缩工控机的交互指令次数

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成对比较（例如校验零件 ID 1 和 3）：
<query_compare>1,3</query_compare>

- 小批量排序（例如对零件 ID 1、3、5 的上料架排序）：
<query_sort>1,3,5</query_sort>

- 局部名次（例如询问零件 ID 2 在托盘合集 [2,4,6] 中的顺位）：
<query_rank>2 in 2,4,6</query_rank>

提交最终答案时，请给出目标零件的全局质检位次（1 到 {n} 的整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
The quality inspection hub of the smart manufacturing base is executing an "Implicit Defect Detection Batch Scheduling". Here are the assembly line rules:

The current sampling batch contains {n} precision mechanical parts, each carrying:
- A unique assembly line tracking ID (from 1 to {n})
- A public and unique material spectrum code (a fixed-length numeric string)

The smart quality inspection hub embeds a highly confidential stress-fatigue function f(code) to calculate the inspection sequence key for each part. All parts are strictly fed into the flaw detection cabin in ascending order of their keys (smaller keys mean earlier entry); if keys are identical, the lexicographic order of the spectrum codes (ascending) acts as the baseline sorting rule, thus yielding an immutable absolute inspection sequence.

## Initial Public Information

Part batch list:
{objects_list}

Target part tracking ID: {target_id}

## Your Task

Accurately pinpoint the global absolute inspection rank R of the target part among all {n} parts in the batch (R is an integer from 1 to {n}).

## Allowed Query Types

You can repeatedly send the following three types of sampling commands to the inspection hub via the IPC (one command per turn), and the hub will return data truthfully according to the hidden schedule:

1. **Pairwise Comparison**: Verify the temporal sequence of part X and part Y entering the flaw detection cabin.
   - Answer: "X before Y" or "Y before X"

2. **Small Batch Sort**: Intercept 2 to 4 parts as a loading rack subset and request the exact inspection order for that rack.
   - Answer: The tracking ID list of that loading rack sorted by inspection sequence

3. **Local Rank**: Specify part X and query its local rank within a tray collection (2 to 4 parts, including X).
   - Answer: The rank of X in that tray collection (an integer from 1 to collection size)

## Constraints

- Tracking IDs in each command must be independent and sourced from the registered {n} parts
- The number of parts in any command's collection cannot exceed 4
- Fetching or functionally bypassing to request the full inspection schedule of the entire assembly line is strictly forbidden
- Please make every effort to minimize the number of IPC interaction commands

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Pairwise Comparison (e.g., verifying part IDs 1 and 3):
<query_compare>1,3</query_compare>

- Small Batch Sort (e.g., sorting the loading rack for part IDs 1, 3, 5):
<query_sort>1,3,5</query_sort>

- Local Rank (e.g., asking for the rank of part ID 2 in tray collection [2,4,6]):
<query_rank>2 in 2,4,6</query_rank>

When submitting the final answer, provide the global inspection rank of the target part (an integer from 1 to {n}), using this format:

<answer>5</answer>
"""

    contextualized_rule_zh_5 = """\
最高法务审计系统正在进行一项关于“卷宗盲审急迫度”的调度推演，规则如下：

庭审前备查数据库包含 {n} 份数字案卷，每份案卷附有：
- 一个不可复用的立案 ID（从 1 到 {n}）
- 一串公开且彼此迥异的哈希特征码（固定长度的数字字符串）

审计系统应用了一套深度保密的法理测算算法 f(code) 来计算每一份案卷的审查急迫指数。全部卷宗须依照指数的升序排定审查顺位（指数越低，优先级越高）；一旦指数重合，系统将利用特征码的字典序（从小到大）作为唯一基准来破除并列，以此维系绝无歧义的法务审查排期。

## 初始公开信息

卷宗备查列表：
{objects_list}

目标卷宗立案 ID：{target_id}

## 你的任务

推断出目标卷宗在这批 {n} 宗案件里确切的全局审查绝对排期 R（R 为 1 到 {n} 的整数）。

## 允许的查询类型

你获准向审计系统终端提交以下三类审查指令（每次仅限一个提交），终端将依保密急迫度模型给出属实应答：

1. **成对比较**：对比卷宗 X 与卷宗 Y 提呈庭审的先后位次。
   - 回答："X 在 Y 前"或"Y 在 X 前"

2. **小批量排序**：抽取 2 到 4 份关联卷宗形成并案子集，提取其微观维度的庭审排序链。
   - 回答：该子集按照审查排期排序完成后的立案 ID 列表

3. **局部名次**：锁定卷宗 X，并在你指定的抽样并案组（2 到 4 份卷宗，须包含 X）中查勘它的相对次序。
   - 回答：X 在该并案组中的次序（1 到合集大小的整数）

## 约束

- 每次指令所引用的立案 ID 必须不相干，且存在于已披露的 {n} 份卷宗范围内
- 单次检索的并案组合规模上限限定为 4 宗案件
- 封禁对全体案卷进行直接宏观排序或具有同等效力的大规模接口拉取
- 请恪守司法效率准则，最大限度地缩减系统检索次数

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 成对比较（例如对比卷宗 ID 1 和 3）：
<query_compare>1,3</query_compare>

- 小批量排序（例如对关联卷宗 ID 1、3、5 的排序）：
<query_sort>1,3,5</query_sort>

- 局部名次（例如查勘卷宗 ID 2 在抽样并案组 [2,4,6] 中的次序）：
<query_rank>2 in 2,4,6</query_rank>

提交最终答案时，请给出目标卷宗的全局审查绝对排期（1 到 {n} 的整数），格式如下：

<answer>5</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
The Supreme Legal Audit System is conducting a scheduling deduction on the "Urgency of Blind Case Review". Here are the rules:

The pre-trial database contains {n} digital case files, each attached with:
- A non-reusable case ID (from 1 to {n})
- A public and distinct hash feature code (a fixed-length numeric string)

The audit system applies a deeply confidential jurisprudential calculation algorithm f(code) to compute the review urgency index of every case file. All files must be sequenced for review in ascending order of this index (a lower index means higher priority); should the indices overlap, the system will utilize the lexicographic order of the feature codes (ascending) as the sole benchmark to break the tie, thereby maintaining an unambiguous legal review schedule.

## Initial Public Information

Case file list:
{objects_list}

Target case ID: {target_id}

## Your Task

Deduce the exact global absolute review schedule R of the target case file among this batch of {n} cases (R is an integer from 1 to {n}).

## Allowed Query Types

You are authorized to submit the following three types of review commands to the audit system terminal (one submission per turn), and the terminal will provide truthful responses according to the confidential urgency model:

1. **Pairwise Comparison**: Contrast the sequential order of presenting case file X and case file Y for hearing.
   - Answer: "X before Y" or "Y before X"

2. **Small Batch Sort**: Extract 2 to 4 associated files to form a consolidated subset, retrieving its micro-dimensional hearing sorting chain.
   - Answer: The case ID list of that subset sorted according to the review schedule

3. **Local Rank**: Pinpoint case file X and inspect its relative sequence within a sampling consolidated group of your designation (2 to 4 files, must include X).
   - Answer: The sequence of X in that consolidated group (an integer from 1 to group size)

## Constraints

- Case IDs referenced in each command must be disjoint and fall within the scope of the disclosed {n} case files
- The upper limit of the consolidated group size for a single retrieval is constrained to 4 cases
- Direct macro-sorting of all files or large-scale API pulling with equivalent effect is blocked
- Please adhere to judicial efficiency guidelines and minimize system retrieval counts to the greatest extent possible

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Pairwise Comparison (e.g., contrasting case IDs 1 and 3):
<query_compare>1,3</query_compare>

- Small Batch Sort (e.g., sorting associated case IDs 1, 3, 5):
<query_sort>1,3,5</query_sort>

- Local Rank (e.g., inspecting case ID 2's sequence in sampling group [2,4,6]):
<query_rank>2 in 2,4,6</query_rank>

When submitting the final answer, provide the global absolute review schedule of the target case file (an integer from 1 to {n}), using this format:

<answer>5</answer>
"""

    tags = ["answer", "query_compare", "query_sort", "query_rank"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "objects": [
                    (1, "1023"),
                    (2, "4567"),
                    (3, "2891"),
                    (4, "3456"),
                    (5, "7890")
                ],
                "target_id": 3,
                "func_type": "last_digit"
            },
            2: {
                "n": 8,
                "objects": [
                    (1, "1234"),
                    (2, "5678"),
                    (3, "2468"),
                    (4, "1357"),
                    (5, "9876"),
                    (6, "3141"),
                    (7, "2718"),
                    (8, "1618")
                ],
                "target_id": 5,
                "func_type": "sum_digits"
            },
            3: {
                "n": 10,
                "objects": [
                    (1, "1001"),
                    (2, "2002"),
                    (3, "3003"),
                    (4, "4004"),
                    (5, "5005"),
                    (6, "6006"),
                    (7, "7007"),
                    (8, "8008"),
                    (9, "9009"),
                    (10, "1111")
                ],
                "target_id": 7,
                "func_type": "sum_mod7"
            },
            4: {
                "n": 12,
                "objects": [
                    (1, "1234"),
                    (2, "2345"),
                    (3, "3456"),
                    (4, "4567"),
                    (5, "5678"),
                    (6, "6789"),
                    (7, "7890"),
                    (8, "8901"),
                    (9, "9012"),
                    (10, "1111"),
                    (11, "2222"),
                    (12, "3333")
                ],
                "target_id": 8,
                "func_type": "first_two_sum"
            },
            5: {
                "n": 15,
                "objects": [
                    (1, "1234"),
                    (2, "5678"),
                    (3, "9012"),
                    (4, "3456"),
                    (5, "7890"),
                    (6, "2468"),
                    (7, "1357"),
                    (8, "9876"),
                    (9, "5432"),
                    (10, "1111"),
                    (11, "2222"),
                    (12, "3333"),
                    (13, "4444"),
                    (14, "5555"),
                    (15, "6666")
                ],
                "target_id": 10,
                "func_type": "alternating_sum"
            }
        },
        "en": {
            1: {
                "n": 5,
                "objects": [
                    (1, "1023"),
                    (2, "4567"),
                    (3, "2891"),
                    (4, "3456"),
                    (5, "7890")
                ],
                "target_id": 3,
                "func_type": "last_digit"
            },
            2: {
                "n": 8,
                "objects": [
                    (1, "1234"),
                    (2, "5678"),
                    (3, "2468"),
                    (4, "1357"),
                    (5, "9876"),
                    (6, "3141"),
                    (7, "2718"),
                    (8, "1618")
                ],
                "target_id": 5,
                "func_type": "sum_digits"
            },
            3: {
                "n": 10,
                "objects": [
                    (1, "1001"),
                    (2, "2002"),
                    (3, "3003"),
                    (4, "4004"),
                    (5, "5005"),
                    (6, "6006"),
                    (7, "7007"),
                    (8, "8008"),
                    (9, "9009"),
                    (10, "1111")
                ],
                "target_id": 7,
                "func_type": "sum_mod7"
            },
            4: {
                "n": 12,
                "objects": [
                    (1, "1234"),
                    (2, "2345"),
                    (3, "3456"),
                    (4, "4567"),
                    (5, "5678"),
                    (6, "6789"),
                    (7, "7890"),
                    (8, "8901"),
                    (9, "9012"),
                    (10, "1111"),
                    (11, "2222"),
                    (12, "3333")
                ],
                "target_id": 8,
                "func_type": "first_two_sum"
            },
            5: {
                "n": 15,
                "objects": [
                    (1, "1234"),
                    (2, "5678"),
                    (3, "9012"),
                    (4, "3456"),
                    (5, "7890"),
                    (6, "2468"),
                    (7, "1357"),
                    (8, "9876"),
                    (9, "5432"),
                    (10, "1111"),
                    (11, "2222"),
                    (12, "3333"),
                    (13, "4444"),
                    (14, "5555"),
                    (15, "6666")
                ],
                "target_id": 10,
                "func_type": "alternating_sum"
            }
        }
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
        self._game_info["target_id"] = cfg["target_id"]
        
        # 存储对象信息：ID -> code
        self.objects = {}
        for obj_id, code in cfg["objects"]:
            self.objects[obj_id] = code
        
        # 根据函数类型计算排序键
        self.func_type = cfg["func_type"]
        self.sort_keys = {}
        for obj_id, code in self.objects.items():
            self.sort_keys[obj_id] = self._compute_sort_key(code, self.func_type)
        
        # 计算全局排序（按键值升序，键值相同按 code 字典序）
        sorted_ids = sorted(
            self.objects.keys(),
            key=lambda x: (self.sort_keys[x], self.objects[x])
        )
        
        # 存储真实的全局名次（ID -> rank）
        self.global_ranks = {}
        for rank, obj_id in enumerate(sorted_ids, start=1):
            self.global_ranks[obj_id] = rank
        
        # 目标对象的真实名次
        self.target_id = cfg["target_id"]
        self.target_rank = self.global_ranks[self.target_id]
        
        # 格式化对象列表用于展示
        objects_lines = []
        for obj_id, code in sorted(self.objects.items()):
            objects_lines.append(f"ID {obj_id}: code = {code}")
        self._game_info["objects_list"] = "\n".join(objects_lines)

    def _compute_sort_key(self, code, func_type):
        """根据函数类型计算排序键"""
        if func_type == "last_digit":
            # 取最后一位数字
            return int(code[-1])
        elif func_type == "sum_digits":
            # 各位数字之和
            return sum(int(d) for d in code)
        elif func_type == "sum_mod7":
            # 各位数字之和模 7
            return sum(int(d) for d in code) % 7
        elif func_type == "first_two_sum":
            # 前两位数字之和
            return int(code[0]) + int(code[1])
        elif func_type == "alternating_sum":
            # 交替和（奇数位减偶数位，从第1位开始计数）
            total = 0
            for i, d in enumerate(code, start=1):
                if i % 2 == 1:
                    total += int(d)
                else:
                    total -= int(d)
            return total
        else:
            raise ValueError(f"Unknown function type: {func_type}")

    def _sort_subset(self, id_list):
        """对给定的 ID 列表按全序排序"""
        return sorted(id_list, key=lambda x: (self.sort_keys[x], self.objects[x]))

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        为控制总量，仅生成包含 target_id 的查询。
        """
        queries = []
        n = self._game_info["n"]
        ids = list(range(1, n + 1))
        tid = self.target_id
        
        # 1. 成对比较：target_id 与每个其他 ID
        for other_id in ids:
            if other_id == tid:
                continue
            id1, id2 = min(tid, other_id), max(tid, other_id)
            query_content = f"{id1},{id2}"
            parsed_info = {"query_compare": query_content}
            ans = self._cf_core_produce(parsed_info)
            queries.append({
                "query": f"<query_compare>{query_content}</query_compare>",
                "answer": ans
            })

        # 2. 小批量排序：包含 target_id 的子集，大小 2~4
        other_ids = [x for x in ids if x != tid]
        for k in range(1, min(4, len(other_ids) + 1)):  # 子集中除 target 外的元素数
            for others in itertools.combinations(other_ids, k):
                subset = sorted([tid] + list(others))
                query_content = ",".join(map(str, subset))
                parsed_info = {"query_sort": query_content}
                ans = self._cf_core_produce(parsed_info)
                queries.append({
                    "query": f"<query_sort>{query_content}</query_sort>",
                    "answer": ans
                })

        # 3. 局部名次：target_id 在包含自身的子集中的名次
        for k in range(1, min(4, len(other_ids) + 1)):
            for others in itertools.combinations(other_ids, k):
                subset = sorted([tid] + list(others))
                subset_str = ",".join(map(str, subset))
                query_content = f"{tid} in {subset_str}"
                parsed_info = {"query_rank": query_content}
                ans = self._cf_core_produce(parsed_info)
                queries.append({
                    "query": f"<query_rank>{query_content}</query_rank>",
                    "answer": ans
                })

        return queries

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.target_rank
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑，用于生成正确答案"""
        lang = self.config.language
        
        try:
            # 处理成对比较查询
            if "query_compare" in parsed_info:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Compare query must contain exactly 2 IDs")
                
                id1, id2 = int(parts[0]), int(parts[1])
                if id1 not in self.objects or id2 not in self.objects:
                    raise ValueError("ID out of range")
                if id1 == id2:
                    raise ValueError("IDs must be distinct")
                
                # 比较在全序中的位置
                sorted_pair = self._sort_subset([id1, id2])
                if sorted_pair[0] == id1:
                    if lang == "zh":
                        return f"{id1} 在 {id2} 前"
                    else:
                        return f"{id1} before {id2}"
                else:
                    if lang == "zh":
                        return f"{id2} 在 {id1} 前"
                    else:
                        return f"{id2} before {id1}"
            
            # 处理小批量排序查询
            elif "query_sort" in parsed_info:
                raw = parsed_info["query_sort"].strip()
                parts = [int(x.strip()) for x in raw.split(",")]
                
                if len(parts) < 2 or len(parts) > 4:
                    raise ValueError("Sort query must contain 2 to 4 IDs")
                if len(parts) != len(set(parts)):
                    raise ValueError("IDs must be distinct")
                if any(obj_id not in self.objects for obj_id in parts):
                    raise ValueError("ID out of range")
                
                sorted_ids = self._sort_subset(parts)
                return ",".join(str(obj_id) for obj_id in sorted_ids)
            
            # 处理局部名次查询
            elif "query_rank" in parsed_info:
                raw = parsed_info["query_rank"].strip()
                if " in " not in raw:
                    raise ValueError("Rank query must use format: X in X1,X2,...")
                
                target_part, subset_part = raw.split(" in ", 1)
                target_id = int(target_part.strip())
                subset_ids = [int(x.strip()) for x in subset_part.split(",")]
                
                if len(subset_ids) < 2 or len(subset_ids) > 4:
                    raise ValueError("Rank query subset must contain 2 to 4 IDs")
                if len(subset_ids) != len(set(subset_ids)):
                    raise ValueError("IDs must be distinct")
                if target_id not in subset_ids:
                    raise ValueError("Target ID must be in the subset")
                if any(obj_id not in self.objects for obj_id in subset_ids):
                    raise ValueError("ID out of range")
                
                sorted_subset = self._sort_subset(subset_ids)
                rank = sorted_subset.index(target_id) + 1
                return str(rank)
            
            else:
                raise ValueError("No valid query tag found")
        
        except ValueError as e:
            if lang == "zh":
                return f"错误：{str(e)}"
            else:
                return f"Error: {str(e)}"
        except Exception as e:
            if lang == "zh":
                return f"错误：无效的查询格式"
            else:
                return f"Error: Invalid query format"

    def _cf_make_wrong(self, correct):
        lang = self.config.language

        # 局部名次结果：纯数字字符串
        if correct.strip().isdigit():
            val = int(correct.strip())
            # 确保生成一个与原值不同的错误值
            if val > 1:
                return str(val - 1)
            else:
                return str(val + 1)

        # 成对比较结果：含 "before" 或 "在...前"
        if lang == "zh" and " 在 " in correct and " 前" in correct:
            m = re.match(r"(\S+)\s+在\s+(\S+)\s+前", correct)
            if m:
                return f"{m.group(2)} 在 {m.group(1)} 前"
        if lang == "en" and " before " in correct:
            parts = correct.split(" before ")
            if len(parts) == 2:
                return f"{parts[1].strip()} before {parts[0].strip()}"

        # 小批量排序结果：逗号分隔的 ID 列表
        if "," in correct:
            parts = correct.split(",")
            if len(parts) >= 2:
                return ",".join(reversed(parts))

        # 兜底
        return f"{correct}_WRONG"