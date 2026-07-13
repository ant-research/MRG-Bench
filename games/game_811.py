# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   最小覆盖：能覆盖所有元素所需的最少子集数量
# ============================================================

from .base import Game
import re
import itertools


class MinimalSetCoverGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "集合"

    game_rule_zh = """\
我们现在来玩一个"最小集合覆盖"的推理游戏，规则如下：

游戏设定了一个宇宙集合 S，包含编号 1 到 {n} 的元素。同时提供了 {m} 个已命名的子集：{subset_names}。

每个子集包含若干元素，但具体包含哪些元素是隐藏的。这些子集的构造遵循特殊的内在规律：元素之间存在隐藏的"类型"划分，属于同一类型的元素在所有子集中的出现模式完全一致。保证至少存在一种使用若干子集完全覆盖所有元素的方案。

你的目标是：通过查询交互，推断出使用最少数量的子集来覆盖全部元素的方案，并提交该方案。

## 可用的查询类型

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实设定如实回答：

1. **子集枚举查询**：列出某个子集包含的所有元素。
2. **元素隶属查询**：询问某个元素是否属于某个子集。
3. **交集大小查询**：询问两个子集的交集包含多少个元素。
4. **覆盖测试查询**：测试给定的若干子集的并集是否覆盖了全部元素。
5. **冗余检测查询**：对于给定的若干子集，判断是否存在可删除且仍保持全覆盖的冗余子集。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 子集枚举查询（例如查询子集 U1）：
<query_list>U1</query_list>

- 元素隶属查询（例如询问元素 3 是否属于子集 U2）：
<query_member>3,U2</query_member>

- 交集大小查询（例如询问子集 U1 和 U3 的交集大小）：
<query_intersect>U1,U3</query_intersect>

- Coverage Test Query（例如测试子集 U1、U2、U4 的并集）：
<query_cover>U1,U2,U4</query_cover>

- 冗余检测查询（例如检测子集 U1、U2、U3 中是否有冗余）：
<query_redundant>U1,U2,U3</query_redundant>

## 提交最终答案

当你确定找到最小覆盖方案后，请提交答案。格式如下：

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

其中 K 是使用的子集数量，subsets 后列出所有子集名称（用逗号隔开，顺序不限）。

## 判定规则

- 若提交的方案未能覆盖全部元素：判定失败。
- 若提交的方案覆盖了全部元素但不是最少数量：判定失败。
- 若提交的方案覆盖了全部元素且使用了最少数量的子集：判定成功。
"""

    game_rule_en = """\
Let's play a "Minimal Set Cover" deduction game. Here are the rules:

There is a universe set S containing elements numbered from 1 to {n}. You are also given {m} named subsets: {subset_names}.

Each subset contains certain elements, but which elements are included is hidden. These subsets follow a special internal pattern: there is a hidden "type" classification among elements, and elements of the same type appear in exactly the same pattern across all subsets. It is guaranteed that at least one combination of subsets can completely cover all elements.

Your goal is: through query interactions, infer the minimal number of subsets needed to cover all elements and submit that solution.

## Available Query Types

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully:

1. **Subset Enumeration Query**: List all elements contained in a specific subset.
2. **Element Membership Query**: Ask whether a specific element belongs to a specific subset.
3. **Intersection Size Query**: Ask how many elements are in the intersection of two subsets.
4. **Coverage Test Query**: Test whether the union of given subsets covers all elements.
5. **Redundancy Detection Query**: For given subsets, determine if there exists a redundant subset that can be removed while maintaining full coverage.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Subset Enumeration Query (e.g., query subset U1):
<query_list>U1</query_list>

- Element Membership Query (e.g., ask if element 3 belongs to subset U2):
<query_member>3,U2</query_member>

- Intersection Size Query (e.g., ask the intersection size of U1 and U3):
<query_intersect>U1,U3</query_intersect>

- Coverage Test Query (e.g., test the union of subsets U1, U2, U4):
<query_cover>U1,U2,U4</query_cover>

- Redundancy Detection Query (e.g., check if U1, U2, U3 contain redundancy):
<query_redundant>U1,U2,U3</query_redundant>

## Submit Final Answer

When you have determined the minimal cover solution, submit your answer in this format:

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

Where K is the number of subsets used, and subsets lists all subset names (comma-separated, order does not matter).

## Judgment Rules

- If the submitted solution does not cover all elements: failure.
- If the submitted solution covers all elements but is not minimal: failure.
- If the submitted solution covers all elements and uses the minimal number of subsets: success.
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
我们现在进入"城市公交线网优化"系统。

系统设定了一个服务盲区集合 S，包含编号 1 到 {n} 的待覆盖交通站点。同时提供了 {m} 条规划好的候选公交线路：{subset_names}。

每条线路停靠若干站点，但具体停靠哪些站点是隐藏的。这些线路的规划遵循内在规律：站点间存在隐藏的"交通区域"划分，属于同一区域的站点在所有线路中的停靠模式完全一致。保证至少存在一种使用若干线路完全覆盖所有站点的方案。

你的目标是：通过查询交互，推断出开通最少数量的公交线路来覆盖全部站点的方案，并提交该方案。

## 可用的查询类型

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实设定如实回答：

1. **线路枚举查询**：列出某条线路停靠的所有站点。
2. **站点隶属查询**：询问某个站点是否属于某条线路。
3. **交集大小查询**：询问两条线路共有的站点数量。
4. **覆盖测试查询**：测试给定的若干线路的联合是否覆盖了全部站点。
5. **冗余检测查询**：对于给定的若干线路，判断是否存在可删除且仍保持全线网覆盖的冗余线路。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 线路枚举查询（例如查询线路 U1）：
<query_list>U1</query_list>

- 站点隶属查询（例如询问站点 3 是否属于线路 U2）：
<query_member>3,U2</query_member>

- 交集大小查询（例如询问线路 U1 和 U3 的交集大小）：
<query_intersect>U1,U3</query_intersect>

- 覆盖测试查询（例如测试线路 U1、U2、U4 的联合覆盖情况）：
<query_cover>U1,U2,U4</query_cover>

- 冗余检测查询（例如检测线路 U1、U2、U3 中是否有冗余）：
<query_redundant>U1,U2,U3</query_redundant>

## 提交最终答案

当你确定找到最小覆盖方案后，请提交答案。格式如下：

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

其中 K 是使用的线路数量，subsets 后列出所有线路名称（用逗号隔开，顺序不限）。

## 判定规则

- 若提交的方案未能覆盖全部站点：判定失败。
- 若提交的方案覆盖了全部站点但不是最少数量：判定失败。
- 若提交的方案覆盖了全部站点且使用了最少数量的线路：判定成功。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Transit Network Optimization" system.

The system defines a service area set S containing transit stops numbered from 1 to {n} that need coverage. You are also provided with {m} candidate transit routes: {subset_names}.

Each route covers certain stops, but the exact stops are hidden. The route designs follow a specific internal pattern: there is a hidden "zone" classification among the stops, and stops in the same zone appear in exactly the same pattern across all routes. It is guaranteed that at least one combination of routes can completely cover all stops.

Your goal is: through query interactions, infer the minimal number of transit routes needed to cover all stops and submit that solution.

## Available Query Types

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully:

1. **Route Enumeration Query**: List all stops covered by a specific route.
2. **Stop Membership Query**: Ask whether a specific stop belongs to a specific route.
3. **Intersection Size Query**: Ask how many stops are shared between two routes.
4. **Coverage Test Query**: Test whether the combination of given routes covers all stops.
5. **Redundancy Detection Query**: For given routes, determine if there exists a redundant route that can be removed while maintaining full network coverage.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Route Enumeration Query (e.g., query route U1):
<query_list>U1</query_list>

- Stop Membership Query (e.g., ask if stop 3 belongs to route U2):
<query_member>3,U2</query_member>

- Intersection Size Query (e.g., ask the intersection size of routes U1 and U3):
<query_intersect>U1,U3</query_intersect>

- Coverage Test Query (e.g., test the combination of routes U1, U2, U4):
<query_cover>U1,U2,U4</query_cover>

- Redundancy Detection Query (e.g., check if routes U1, U2, U3 contain redundancy):
<query_redundant>U1,U2,U3</query_redundant>

## Submit Final Answer

When you have determined the minimal cover solution, submit your answer in this format:

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

Where K is the number of routes used, and subsets lists all route names (comma-separated, order does not matter).

## Judgment Rules

- If the submitted solution does not cover all stops: failure.
- If the submitted solution covers all stops but is not minimal: failure.
- If the submitted solution covers all stops and uses the minimal number of routes: success.
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
我们现在进入"精准医疗联合靶向治疗"系统。

系统针对一名复杂病患，整理出了变异基因与临床表现集合 S，包含编号 1 到 {n} 的临床靶点。同时药房提供了 {m} 种候选靶向药物包：{subset_names}。

每种药物包能覆盖若干靶点，但具体覆盖哪些是隐藏的。药物包的设计遵循药理规律：靶点之间存在隐藏的"生理系统"划分，属于同一系统的靶点在所有药物包中的起效模式完全一致。保证至少存在一种药物组合能覆盖患者所有的靶点。

你的目标是：通过查询交互，推断出开出最少数量的药物包来覆盖全部靶点的处方方案，并提交该处方。

## 可用的查询类型

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实设定如实回答：

1. **药物包枚举查询**：列出某种药物包覆盖的所有靶点。
2. **靶点隶属查询**：询问某个靶点是否被某种药物包覆盖。
3. **交集大小查询**：询问两种药物包共同覆盖的靶点数量。
4. **覆盖测试查询**：测试给定的若干药物包的联合用药是否覆盖了全部靶点。
5. **冗余检测查询**：对于给定的若干药物包，判断是否存在可停用且仍保持全面覆盖的冗余药物包。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML format：

- 药物包枚举查询（例如查询药物包 U1）：
<query_list>U1</query_list>

- 靶点隶属查询（例如询问靶点 3 是否被药物包 U2 覆盖）：
<query_member>3,U2</query_member>

- 交集大小查询（例如询问药物包 U1 和 U3 的交集大小）：
<query_intersect>U1,U3</query_intersect>

- 覆盖测试查询（例如测试药物包 U1、U2、U4 的联合）：
<query_cover>U1,U2,U4</query_cover>

- 冗余检测查询（例如检测药物包 U1、U2、U3 中是否有冗余）：
<query_redundant>U1,U2,U3</query_redundant>

## 提交最终答案

当你确定找到最小覆盖方案后，请提交答案。格式如下：

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

其中 K 是使用的药物包数量，subsets 后列出所有药物包名称（用逗号隔开，顺序不限）。

## 判定规则

- 若提交的方案未能覆盖全部靶点：判定失败。
- 若提交的方案覆盖了全部靶点但不是最少数量：判定失败。
- 若提交的方案覆盖了全部靶点且使用了最少数量的药物包：判定成功。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Precision Medicine Combination Therapy" system.

For a complex patient case, the system has identified a set S containing clinical targets numbered from 1 to {n} that require intervention. The pharmacy also provides {m} candidate targeted drug panels: {subset_names}.

Each drug panel covers certain targets, but the exact coverage is hidden. The panel formulations follow pharmacological patterns: there is a hidden "physiological system" classification among targets, and targets within the same system respond in exactly the same pattern across all drug panels. It is guaranteed that at least one combination of drug panels can completely cover all targets.

Your goal is: through query interactions, infer the minimal number of drug panels needed to cover all clinical targets and submit that prescription plan.

## Available Query Types

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully:

1. **Panel Enumeration Query**: List all targets covered by a specific drug panel.
2. **Target Membership Query**: Ask whether a specific target is covered by a specific drug panel.
3. **Intersection Size Query**: Ask how many targets are shared between two drug panels.
4. **Coverage Test Query**: Test whether the combination of given drug panels covers all targets.
5. **Redundancy Detection Query**: For given drug panels, determine if there exists a redundant panel that can be withdrawn while maintaining full clinical coverage.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Panel Enumeration Query (e.g., query panel U1):
<query_list>U1</query_list>

- Target Membership Query (e.g., ask if target 3 is covered by panel U2):
<query_member>3,U2</query_member>

- Intersection Size Query (e.g., ask the intersection size of panels U1 and U3):
<query_intersect>U1,U3</query_intersect>

- Coverage Test Query (e.g., test the combination of panels U1, U2, U4):
<query_cover>U1,U2,U4</query_cover>

- Redundancy Detection Query (e.g., check if panels U1, U2, U3 contain redundancy):
<query_redundant>U1,U2,U3</query_redundant>

## Submit Final Answer

When you have determined the minimal cover solution, submit your answer in this format:

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

Where K is the number of drug panels used, and subsets lists all panel names (comma-separated, order does not matter).

## Judgment Rules

- If the submitted solution does not cover all targets: failure.
- If the submitted solution covers all targets but is not minimal: failure.
- If the submitted solution covers all targets and uses the minimal number of drug panels: success.
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
我们现在进入"核心素养课程体系培养"系统。

系统制定了毕业要求的技能集合 S，包含编号 1 到 {n} 的核心知识点。同时教务处提供了 {m} 门综合选修课程：{subset_names}。

每门课程涵盖若干知识点，但具体教学大纲是隐藏的。这些课程的设置遵循学科规律：知识点之间存在隐藏的"学科模块"划分，属于同一模块的知识点在所有课程中的分布模式完全一致。保证至少存在一种选课组合能覆盖毕业要求的所有知识点。

你的目标是：通过查询交互，推断出修读最少数量的课程来覆盖全部知识点的学业方案，并提交该方案。

## 可用的查询类型

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实设定如实回答：

1. **课程枚举查询**：列出某门课程涵盖的所有知识点。
2. **知识点隶属查询**：询问某个知识点是否包含在某门课程中。
3. **交集大小查询**：询问两门课程重叠的知识点数量。
4. **覆盖测试查询**：测试给定的若干课程组合是否覆盖了全部知识点。
5. **冗余检测查询**：对于给定的若干课程，判断是否存在可退选且仍保持全部知识点覆盖的冗余课程。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 课程枚举查询（例如查询课程 U1）：
<query_list>U1</query_list>

- 知识点隶属查询（例如询问知识点 3 是否属于课程 U2）：
<query_member>3,U2</query_member>

- 交集大小查询（例如询问课程 U1 和 U3 的交集大小）：
<query_intersect>U1,U3</query_intersect>

- 覆盖测试查询（例如测试课程 U1、U2、U4 的联合）：
<query_cover>U1,U2,U4</query_cover>

- 冗余检测查询（例如检测课程 U1、U2、U3 中是否有冗余）：
<query_redundant>U1,U2,U3</query_redundant>

## 提交最终答案

当你确定找到最小覆盖方案后，请提交答案。格式如下：

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

其中 K 是修读的课程数量，subsets 后列出所有课程名称（用逗号隔开，顺序不限）。

## 判定规则

- 若提交的方案未能覆盖全部知识点：判定失败。
- 若提交的方案覆盖了全部知识点但不是最少数量：判定失败。
- 若提交的方案覆盖了全部知识点且使用了最少数量的课程：判定成功。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Core Competency Curriculum" system.

The system defines a graduation requirement set S containing core knowledge points numbered from 1 to {n}. The academic affairs office also provides {m} comprehensive elective courses: {subset_names}.

Each course covers certain knowledge points, but the exact syllabus is hidden. The curriculum design follows academic patterns: there is a hidden "subject module" classification among knowledge points, and points within the same module appear in exactly the same pattern across all courses. It is guaranteed that at least one combination of courses can completely cover all required knowledge points.

Your goal is: through query interactions, infer the minimal number of courses needed to cover all knowledge points and submit that academic plan.

## Available Query Types

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully:

1. **Course Enumeration Query**: List all knowledge points covered by a specific course.
2. **Point Membership Query**: Ask whether a specific knowledge point is included in a specific course.
3. **Intersection Size Query**: Ask how many knowledge points are shared between two courses.
4. **Coverage Test Query**: Test whether the combination of given courses covers all knowledge points.
5. **Redundancy Detection Query**: For given courses, determine if there exists a redundant course that can be dropped while maintaining full curriculum coverage.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Course Enumeration Query (e.g., query course U1):
<query_list>U1</query_list>

- Point Membership Query (e.g., ask if point 3 is in course U2):
<query_member>3,U2</query_member>

- Intersection Size Query (e.g., ask the intersection size of courses U1 and U3):
<query_intersect>U1,U3</query_intersect>

- Coverage Test Query (e.g., test the combination of courses U1, U2, U4):
<query_cover>U1,U2,U4</query_cover>

- Redundancy Detection Query (e.g., check if courses U1, U2, U3 contain redundancy):
<query_redundant>U1,U2,U3</query_redundant>

## Submit Final Answer

When you have determined the minimal cover solution, submit your answer in this format:

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

Where K is the number of courses taken, and subsets lists all course names (comma-separated, order does not matter).

## Judgment Rules

- If the submitted solution does not cover all knowledge points: failure.
- If the submitted solution covers all knowledge points but is not minimal: failure.
- If the submitted solution covers all knowledge points and uses the minimal number of courses: success.
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
我们现在进入"柔性生产线工序配置"系统。

系统解析了一张复杂零件图纸，提炼出加工特征集合 S，包含编号 1 到 {n} 的加工工序。同时车间提供了 {m} 个复合加工中心（工作站）：{subset_names}。

每个工作站能完成若干工序，但具体能力参数是隐藏的。工作站的功能配置遵循工艺规律：工序之间存在隐藏的"切削类型"划分，属于同一类型的工序在所有工作站中的加工支持模式完全一致。保证至少存在一种工作站编组方案能完成所有的加工工序。

你的目标是：通过查询交互，推断出启用最少数量的工作站来覆盖全部工序的生产方案，并提交该方案。

## 可用的查询类型

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实设定如实回答：

1. **工作站枚举查询**：列出某个工作站能完成的所有工序。
2. **工序隶属查询**：询问某个工序是否能由某个工作站完成。
3. **交集大小查询**：询问两个工作站共同支持的工序数量。
4. **覆盖测试查询**：测试给定的若干工作站的组合是否覆盖了全部工序。
5. **冗余检测查询**：对于给定的若干工作站，判断是否存在可停用且仍能完成所有加工特征的冗余工作站。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 工作站枚举查询（例如查询工作站 U1）：
<query_list>U1</query_list>

- 工序隶属查询（例如询问工序 3 是否支持工作站 U2）：
<query_member>3,U2</query_member>

- 交集大小查询（例如询问工作站 U1 和 U3 的交集大小）：
<query_intersect>U1,U3</query_intersect>

- 覆盖测试查询（例如测试工作站 U1、U2、U4 的组合）：
<query_cover>U1,U2,U4</query_cover>

- 冗余检测查询（例如检测工作站 U1、U2、U3 中是否有冗余）：
<query_redundant>U1,U2,U3</query_redundant>

## 提交最终答案

当你确定找到最小覆盖方案后，请提交答案。格式如下：

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

其中 K 是启用的工作站数量，subsets 后列出所有工作站名称（用逗号隔开，顺序不限）。

## 判定规则

- 若提交的方案未能覆盖全部工序：判定失败。
- 若提交的方案覆盖了全部工序但不是最少数量：判定失败。
- 若提交的方案覆盖了全部工序且启用了最少数量的工作站：判定成功。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Flexible Production Line Configuration" system.

The system has analyzed a complex part drawing and extracted a set S containing machining operations numbered from 1 to {n}. The workshop also provides {m} candidate multi-tasking machining centers (workstations): {subset_names}.

Each workstation can perform certain operations, but the exact capabilities are hidden. The workstation configurations follow engineering patterns: there is a hidden "machining type" classification among operations, and operations of the same type are supported in exactly the same pattern across all workstations. It is guaranteed that at least one combination of workstations can completely cover all machining operations.

Your goal is: through query interactions, infer the minimal number of workstations needed to cover all operations and submit that production plan.

## Available Query Types

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully:

1. **Workstation Enumeration Query**: List all operations supported by a specific workstation.
2. **Operation Membership Query**: Ask whether a specific operation can be performed by a specific workstation.
3. **Intersection Size Query**: Ask how many operations are shared between two workstations.
4. **Coverage Test Query**: Test whether the combination of given workstations covers all operations.
5. **Redundancy Detection Query**: For given workstations, determine if there exists a redundant workstation that can be deactivated while maintaining full production capability.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Workstation Enumeration Query (e.g., query workstation U1):
<query_list>U1</query_list>

- Operation Membership Query (e.g., ask if operation 3 belongs to workstation U2):
<query_member>3,U2</query_member>

- Intersection Size Query (e.g., ask the intersection size of workstations U1 and U3):
<query_intersect>U1,U3</query_intersect>

- Coverage Test Query (e.g., test the combination of workstations U1, U2, U4):
<query_cover>U1,U2,U4</query_cover>

- Redundancy Detection Query (e.g., check if workstations U1, U2, U3 contain redundancy):
<query_redundant>U1,U2,U3</query_redundant>

## Submit Final Answer

When you have determined the minimal cover solution, submit your answer in this format:

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

Where K is the number of workstations activated, and subsets lists all workstation names (comma-separated, order does not matter).

## Judgment Rules

- If the submitted solution does not cover all operations: failure.
- If the submitted solution covers all operations but is not minimal: failure.
- If the submitted solution covers all operations and uses the minimal number of workstations: success.
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
我们现在进入"合规审查与证据链构建"系统。

系统针对一起复杂诉讼，列出了法定要求集合 S，包含编号 1 到 {n} 的必须证明的合规要件。同时法务部整理了 {m} 份综合证据卷宗：{subset_names}。

每份卷宗能证明若干要件，但具体包含哪些证据点是隐藏的。证据的分布遵循法理规律：要件之间存在隐藏的"法条归属"划分，属于同一法条的要件在所有卷宗中的印证模式完全一致。保证至少存在一种卷宗组合方案能覆盖法庭要求的所有合规要件。

你的目标是：通过查询交互，推断出提交最少数量的卷宗来覆盖全部合规要件的举证方案，并提交该方案。

## 可用的查询类型

你可以反复向我提出以下查询（每次仅限一个查询），我会根据真实设定如实回答：

1. **卷宗枚举查询**：列出某份卷宗能证明的所有要件。
2. **要件隶属查询**：询问某个要件是否包含在某份卷宗中。
3. **交集大小查询**：询问两份卷宗共同印证的要件数量。
4. **覆盖测试查询**：测试给定的若干卷宗的组合是否覆盖了全部要件。
5. **冗余检测查询**：对于给定的若干卷宗，判断是否存在可撤回且仍保持证据链完整的冗余卷宗。

## 查询格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 卷宗枚举查询（例如查询卷宗 U1）：
<query_list>U1</query_list>

- 要件隶属查询（例如询问要件 3 是否属于卷宗 U2）：
<query_member>3,U2</query_member>

- 交集大小查询（例如询问卷宗 U1 和 U3 的交集大小）：
<query_intersect>U1,U3</query_intersect>

- 覆盖测试查询（例如测试卷宗 U1、U2、U4 的组合）：
<query_cover>U1,U2,U4</query_cover>

- 冗余检测查询（例如检测卷宗 U1、U2、U3 中是否有冗余）：
<query_redundant>U1,U2,U3</query_redundant>

## 提交最终答案

当你确定找到最小覆盖方案后，请提交答案。格式如下：

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

其中 K 是提交的卷宗数量，subsets 后列出所有卷宗名称（用逗号隔开，顺序不限）。

## 判定规则

- 若提交的方案未能覆盖全部要件：判定失败。
- 若提交的方案覆盖了全部要件但不是最少数量：判定失败。
- 若提交的方案覆盖了全部要件且提交了最少数量的卷宗：判定成功。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Compliance Review and Evidence Chain" system.

For a complex litigation case, the system has outlined a statutory requirement set S containing compliance elements numbered from 1 to {n} that must be proven. The legal department has also prepared {m} comprehensive evidence dossiers: {subset_names}.

Each dossier can prove certain elements, but the exact evidence points are hidden. The distribution of evidence follows legal patterns: there is a hidden "statutory provision" classification among elements, and elements under the same provision are corroborated in exactly the same pattern across all dossiers. It is guaranteed that at least one combination of dossiers can completely cover all compliance elements.

Your goal is: through query interactions, infer the minimal number of dossiers needed to cover all compliance elements and submit that evidentiary plan.

## Available Query Types

You can repeatedly ask me the following queries (one query per turn), and I will answer truthfully:

1. **Dossier Enumeration Query**: List all elements proven by a specific dossier.
2. **Element Membership Query**: Ask whether a specific element is included in a specific dossier.
3. **Intersection Size Query**: Ask how many elements are corroborated by both dossiers.
4. **Coverage Test Query**: Test whether the combination of given dossiers covers all elements.
5. **Redundancy Detection Query**: For given dossiers, determine if there exists a redundant dossier that can be withdrawn while maintaining a complete evidence chain.

## Query Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Dossier Enumeration Query (e.g., query dossier U1):
<query_list>U1</query_list>

- Element Membership Query (e.g., ask if element 3 is in dossier U2):
<query_member>3,U2</query_member>

- Intersection Size Query (e.g., ask the intersection size of dossiers U1 and U3):
<query_intersect>U1,U3</query_intersect>

- Coverage Test Query (e.g., test the combination of dossiers U1, U2, U4):
<query_cover>U1,U2,U4</query_cover>

- Redundancy Detection Query (e.g., check if dossiers U1, U2, U3 contain redundancy):
<query_redundant>U1,U2,U3</query_redundant>

## Submit Final Answer

When you have determined the minimal cover solution, submit your answer in this format:

<answer>count=K, subsets=Uj1,Uj2,...,UjK</answer>

Where K is the number of dossiers submitted, and subsets lists all dossier names (comma-separated, order does not matter).

## Judgment Rules

- If the submitted solution does not cover all compliance elements: failure.
- If the submitted solution covers all elements but is not minimal: failure.
- If the submitted solution covers all elements and uses the minimal number of dossiers: success.
"""

    tags = ["answer", "query_list", "query_member", "query_intersect", "query_cover", "query_redundant"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "subsets": {
                    "U1": [1, 2, 3],      # 类型A
                    "U2": [4, 5, 6],      # 类型B
                    "U3": [1, 2, 3, 4, 5, 6],  # A+B (冗余)
                },
                "types": {
                    1: "A", 2: "A", 3: "A",
                    4: "B", 5: "B", 6: "B",
                },
                "min_cover": 1,
                "min_cover_solutions": [["U3"]],
            },
            2: {
                "n": 8,
                "subsets": {
                    "U1": [1, 2],         # 类型A
                    "U2": [3, 4, 5],      # 类型B
                    "U3": [6, 7, 8],      # 类型C
                    "U4": [1, 2, 3, 4, 5],  # A+B
                },
                "types": {
                    1: "A", 2: "A",
                    3: "B", 4: "B", 5: "B",
                    6: "C", 7: "C", 8: "C",
                },
                "min_cover": 2,
                "min_cover_solutions": [["U3", "U4"]],
            },
            3: {
                "n": 10,
                "subsets": {
                    "U1": [1, 2],         # 类型A
                    "U2": [3, 4],         # 类型B
                    "U3": [5, 6, 7],      # 类型C
                    "U4": [8, 9, 10],     # 类型D
                    "U5": [1, 2, 3, 4],   # A+B
                },
                "types": {
                    1: "A", 2: "A",
                    3: "B", 4: "B",
                    5: "C", 6: "C", 7: "C",
                    8: "D", 9: "D", 10: "D",
                },
                "min_cover": 3,
                "min_cover_solutions": [["U3", "U4", "U5"]],
            },
            4: {
                "n": 12,
                "subsets": {
                    "U1": [1, 2, 3],      # 类型A
                    "U2": [4, 5, 6],      # 类型B
                    "U3": [7, 8, 9],      # 类型C
                    "U4": [10, 11, 12],   # 类型D
                    "U5": [1, 2, 3, 7, 8, 9],      # A+C
                    "U6": [4, 5, 6, 10, 11, 12],   # B+D
                },
                "types": {
                    1: "A", 2: "A", 3: "A",
                    4: "B", 5: "B", 6: "B",
                    7: "C", 8: "C", 9: "C",
                    10: "D", 11: "D", 12: "D",
                },
                "min_cover": 2,
                "min_cover_solutions": [["U5", "U6"]],
            },
            5: {
                "n": 15,
                "subsets": {
                    "U1": [1, 2, 3],      # 类型A
                    "U2": [4, 5, 6],      # 类型B
                    "U3": [7, 8, 9],      # 类型C
                    "U4": [10, 11, 12],   # 类型D
                    "U5": [13, 14, 15],   # 类型E
                    "U6": [1, 2, 3, 4, 5, 6],      # A+B
                    "U7": [7, 8, 9, 10, 11, 12],   # C+D
                },
                "types": {
                    1: "A", 2: "A", 3: "A",
                    4: "B", 5: "B", 6: "B",
                    7: "C", 8: "C", 9: "C",
                    10: "D", 11: "D", 12: "D",
                    13: "E", 14: "E", 15: "E",
                },
                "min_cover": 3,
                "min_cover_solutions": [["U5", "U6", "U7"]],
            },
        },
        "en": {
            1: {
                "n": 6,
                "subsets": {
                    "U1": [1, 2, 3],
                    "U2": [4, 5, 6],
                    "U3": [1, 2, 3, 4, 5, 6],
                },
                "types": {
                    1: "A", 2: "A", 3: "A",
                    4: "B", 5: "B", 6: "B",
                },
                "min_cover": 1,
                "min_cover_solutions": [["U3"]],
            },
            2: {
                "n": 8,
                "subsets": {
                    "U1": [1, 2],
                    "U2": [3, 4, 5],
                    "U3": [6, 7, 8],
                    "U4": [1, 2, 3, 4, 5],
                },
                "types": {
                    1: "A", 2: "A",
                    3: "B", 4: "B", 5: "B",
                    6: "C", 7: "C", 8: "C",
                },
                "min_cover": 2,
                "min_cover_solutions": [["U3", "U4"]],
            },
            3: {
                "n": 10,
                "subsets": {
                    "U1": [1, 2],
                    "U2": [3, 4],
                    "U3": [5, 6, 7],
                    "U4": [8, 9, 10],
                    "U5": [1, 2, 3, 4],
                },
                "types": {
                    1: "A", 2: "A",
                    3: "B", 4: "B",
                    5: "C", 6: "C", 7: "C",
                    8: "D", 9: "D", 10: "D",
                },
                "min_cover": 3,
                "min_cover_solutions": [["U3", "U4", "U5"]],
            },
            4: {
                "n": 12,
                "subsets": {
                    "U1": [1, 2, 3],
                    "U2": [4, 5, 6],
                    "U3": [7, 8, 9],
                    "U4": [10, 11, 12],
                    "U5": [1, 2, 3, 7, 8, 9],
                    "U6": [4, 5, 6, 10, 11, 12],
                },
                "types": {
                    1: "A", 2: "A", 3: "A",
                    4: "B", 5: "B", 6: "B",
                    7: "C", 8: "C", 9: "C",
                    10: "D", 11: "D", 12: "D",
                },
                "min_cover": 2,
                "min_cover_solutions": [["U5", "U6"]],
            },
            5: {
                "n": 15,
                "subsets": {
                    "U1": [1, 2, 3],
                    "U2": [4, 5, 6],
                    "U3": [7, 8, 9],
                    "U4": [10, 11, 12],
                    "U5": [13, 14, 15],
                    "U6": [1, 2, 3, 4, 5, 6],
                    "U7": [7, 8, 9, 10, 11, 12],
                },
                "types": {
                    1: "A", 2: "A", 3: "A",
                    4: "B", 5: "B", 6: "B",
                    7: "C", 8: "C", 9: "C",
                    10: "D", 11: "D", 12: "D",
                    13: "E", 14: "E", 15: "E",
                },
                "min_cover": 3,
                "min_cover_solutions": [["U5", "U6", "U7"]],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 基本信息
        self._game_info["n"] = cfg["n"]
        self._game_info["m"] = len(cfg["subsets"])
        self._game_info["subset_names"] = ", ".join(cfg["subsets"].keys())
        
        # 子集定义（元素编号列表）
        self.subsets = {k: set(v) for k, v in cfg["subsets"].items()}
        
        # 类型映射（用于验证一致性，但不直接暴露）
        self.types = cfg["types"]
        
        # 最小覆盖数量和方案
        self.min_cover_count = cfg["min_cover"]
        self.min_cover_solutions = cfg["min_cover_solutions"]

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        # 解析答案格式: count=K, subsets=Uj1,Uj2,...
        raw_ans = parsed_info["answer"]
        
        # 提取 count 和 subsets
        count_match = re.search(r'count\s*=\s*(\d+)', raw_ans, re.IGNORECASE)
        subsets_match = re.search(r'subsets\s*=\s*([A-Za-z0-9,\s]+)', raw_ans, re.IGNORECASE)
        
        if not count_match or not subsets_match:
            return False
        
        try:
            proposed_count = int(count_match.group(1))
            proposed_subsets = [s.strip() for s in subsets_match.group(1).split(",") if s.strip()]
        except:
            return False
        
        # 1. 检查数量是否一致
        if proposed_count != len(proposed_subsets):
            return False
            
        # 1.5 检查是否有重复子集
        if len(proposed_subsets) != len(set(proposed_subsets)):
            return False
        
        # 2. 检查子集名称是否有效
        for subset_name in proposed_subsets:
            if subset_name not in self.subsets:
                return False
        
        # 3. 检查是否覆盖全部元素
        covered = set()
        for subset_name in proposed_subsets:
            covered |= self.subsets[subset_name]
        
        all_elements = set(range(1, self._game_info["n"] + 1))
        if covered != all_elements:
            return False
        
        # 4. 检查是否为最小覆盖
        if proposed_count != self.min_cover_count:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """原始的查询处理逻辑"""
        lang = self.config.language
        
        # 1. 子集枚举查询
        if "query_list" in parsed_info:
            subset_name = parsed_info["query_list"].strip()
            if subset_name not in self.subsets:
                return "错误：子集名称无效。" if lang == "zh" else "Error: Invalid subset name."
            
            elements = sorted(list(self.subsets[subset_name]))
            if lang == "zh":
                return f"元素列表：{elements}；数量：{len(elements)}"
            else:
                return f"Element list: {elements}; Count: {len(elements)}"
        
        # 2. 元素隶属查询
        elif "query_member" in parsed_info:
            try:
                parts = [p.strip() for p in parsed_info["query_member"].split(",")]
                if len(parts) != 2:
                    raise ValueError
                element_id = int(parts[0])
                subset_name = parts[1]
                
                if subset_name not in self.subsets:
                    raise ValueError
                if element_id < 1 or element_id > self._game_info["n"]:
                    raise ValueError
                
                is_member = element_id in self.subsets[subset_name]
                return "是" if is_member else "否" if lang == "zh" else "Yes" if is_member else "No"
            except:
                return "错误：格式无效或参数错误。" if lang == "zh" else "Error: Invalid format or parameters."
        
        # 3. 交集大小查询
        elif "query_intersect" in parsed_info:
            try:
                parts = [p.strip() for p in parsed_info["query_intersect"].split(",")]
                if len(parts) != 2:
                    raise ValueError
                subset1, subset2 = parts[0], parts[1]
                
                if subset1 not in self.subsets or subset2 not in self.subsets:
                    raise ValueError
                
                intersect_size = len(self.subsets[subset1] & self.subsets[subset2])
                if lang == "zh":
                    return f"交集数量：{intersect_size}"
                else:
                    return f"Intersection count: {intersect_size}"
            except:
                return "错误：格式无效或子集名称错误。" if lang == "zh" else "Error: Invalid format or subset names."
        
        # 4. 覆盖测试查询
        elif "query_cover" in parsed_info:
            try:
                subset_names = [s.strip() for s in parsed_info["query_cover"].split(",") if s.strip()]
                if not subset_names:
                    raise ValueError
                
                for name in subset_names:
                    if name not in self.subsets:
                        raise ValueError
                
                # 计算并集
                union = set()
                for name in subset_names:
                    union |= self.subsets[name]
                
                all_elements = set(range(1, self._game_info["n"] + 1))
                uncovered = sorted(list(all_elements - union))
                
                if not uncovered:
                    return "是否覆盖全部：是" if lang == "zh" else "Covers all: Yes"
                else:
                    if lang == "zh":
                        return f"是否覆盖全部：否；未覆盖编号列表：{uncovered}"
                    else:
                        return f"Covers all: No; Uncovered elements: {uncovered}"
            except:
                return "错误：格式无效或子集名称错误。" if lang == "zh" else "Error: Invalid format or subset names."
        
        # 5. 冗余检测查询
        elif "query_redundant" in parsed_info:
            try:
                subset_names = [s.strip() for s in parsed_info["query_redundant"].split(",") if s.strip()]
                if not subset_names:
                    raise ValueError
                
                for name in subset_names:
                    if name not in self.subsets:
                        raise ValueError
                
                # 计算完整并集
                full_union = set()
                for name in subset_names:
                    full_union |= self.subsets[name]
                
                # 检查每个子集是否可删除
                redundant = []
                for name in subset_names:
                    union_without = set()
                    for other_name in subset_names:
                        if other_name != name:
                            union_without |= self.subsets[other_name]
                    
                    if union_without == full_union:
                        redundant.append(name)
                
                if redundant:
                    if lang == "zh":
                        return f"是，冗余候选：{redundant}"
                    else:
                        return f"Yes, redundant candidates: {redundant}"
                else:
                    return "否" if lang == "zh" else "No"
            except:
                return "错误：格式无效或子集名称错误。" if lang == "zh" else "Error: Invalid format or subset names."
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        为避免组合爆炸，覆盖测试和冗余检测仅枚举长度 <= 3 的组合。
        """
        queries = []
        subset_names = sorted(list(self.subsets.keys()))
        n = self._game_info["n"]
        
        # 1. 子集枚举查询
        for name in subset_names:
            query_content = name
            query_xml = f"<query_list>{query_content}</query_list>"
            parsed = {"query_list": query_content}
            queries.append({"query": query_xml, "answer": self._cf_core_produce(parsed)})
            
        # 2. 元素隶属查询
        for name in subset_names:
            for i in range(1, n + 1):
                query_content = f"{i},{name}"
                query_xml = f"<query_member>{query_content}</query_member>"
                parsed = {"query_member": query_content}
                queries.append({"query": query_xml, "answer": self._cf_core_produce(parsed)})
                
        # 3. 交集大小查询 (组合而非排列)
        for pair in itertools.combinations(subset_names, 2):
            query_content = f"{pair[0]},{pair[1]}"
            query_xml = f"<query_intersect>{query_content}</query_intersect>"
            parsed = {"query_intersect": query_content}
            queries.append({"query": query_xml, "answer": self._cf_core_produce(parsed)})
            
        # 4. 覆盖测试查询 & 5. 冗余检测查询 (组合，长度 1 到 min(3, len(subset_names)))
        max_r = min(3, len(subset_names))
        for r in range(1, max_r + 1):
            for combo in itertools.combinations(subset_names, r):
                query_content = ",".join(combo)
                
                # Coverage
                query_xml_cov = f"<query_cover>{query_content}</query_cover>"
                parsed_cov = {"query_cover": query_content}
                queries.append({"query": query_xml_cov, "answer": self._cf_core_produce(parsed_cov)})
                
                # Redundancy
                query_xml_red = f"<query_redundant>{query_content}</query_redundant>"
                parsed_red = {"query_redundant": query_content}
                queries.append({"query": query_xml_red, "answer": self._cf_core_produce(parsed_red)})
                
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成错误答案"""
        lang = self.config.language
        
        # 处理纯数字
        if correct.strip().isdigit():
            val = int(correct.strip())
            return str(val + 1)
        
        if lang == "zh":
            # 处理覆盖测试查询结果
            if "是否覆盖全部：是" in correct:
                return correct.replace("是否覆盖全部：是", "是否覆盖全部：否；未覆盖编号列表：[1]")
            if "是否覆盖全部：否" in correct:
                return correct.replace("是否覆盖全部：否", "是否覆盖全部：是").split("；")[0]
            
            # 处理冗余检测查询结果（带候选列表的）
            if correct.startswith("是，冗余候选"):
                return "否"
            
            # 处理交集数量
            m = re.search(r'交集数量：(\d+)', correct)
            if m:
                val = int(m.group(1))
                new_val = val + 1 if val == 0 else val - 1
                return correct.replace(f"交集数量：{val}", f"交集数量：{new_val}")
            
            # 处理元素列表（子集枚举）- 修改列表本身
            m_list = re.search(r'元素列表：(\[.*?\])；数量：(\d+)', correct)
            if m_list:
                val = int(m_list.group(2))
                fake_elem = self._game_info["n"] + 1
                list_str = m_list.group(1)
                if list_str == "[]":
                    new_list_str = f"[{fake_elem}]"
                else:
                    new_list_str = list_str[:-1] + f", {fake_elem}]"
                return f"元素列表：{new_list_str}；数量：{val + 1}"
            
            # 处理简单的 是/否（元素隶属 + 冗余检测的"否"）
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
            
        else:  # en
            # 处理覆盖测试
            if "Covers all: Yes" in correct:
                return correct.replace("Covers all: Yes", "Covers all: No; Uncovered elements: [1]")
            if "Covers all: No" in correct:
                return "Covers all: Yes"
            
            # 处理冗余检测（带候选列表的）
            if correct.startswith("Yes, redundant candidates"):
                return "No"
            
            # 处理交集大小
            m = re.search(r'Intersection count: (\d+)', correct)
            if m:
                val = int(m.group(1))
                new_val = val + 1 if val == 0 else val - 1
                return correct.replace(f"Intersection count: {val}", f"Intersection count: {new_val}")
            
            # 处理元素列表 - 修改列表本身
            m_list = re.search(r'Element list: (\[.*?\]); Count: (\d+)', correct)
            if m_list:
                val = int(m_list.group(2))
                fake_elem = self._game_info["n"] + 1
                list_str = m_list.group(1)
                if list_str == "[]":
                    new_list_str = f"[{fake_elem}]"
                else:
                    new_list_str = list_str[:-1] + f", {fake_elem}]"
                return f"Element list: {new_list_str}; Count: {val + 1}"
            
            # 处理简单的 Yes/No（元素隶属 + 冗余检测的"No"）
            if correct == "Yes":
                return "No"
            if correct == "No":
                return "Yes"
        
        # 兜底
        return correct + "_WRONG"