# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   集合并集：两个给定集合的并集大小是多少
# ============================================================

from .base import Game
import re
import random as _random


class SetQueryBlackBoxGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "集合"

    game_rule_zh = """\
我们现在来玩一个"集合查询黑箱"的推理游戏，规则如下：

游戏设定了一个有限全集 U，包含 N 个元素（N 的值未知且大于等于 0）。在这个全集中，存在两个固定但未知的子集 S 和 T。

你可以通过集合表达式来构造查询，集合表达式的构造规则如下：
- 基本元素：空集 empty、全集 U、子集 S、子集 T
- 运算符：并集 union、交集 intersect、补集 complement
- 表达式示例：
  - (union S T) 表示 S 和 T 的并集
  - (intersect S T) 表示 S 和 T 的交集
  - (complement S) 表示 S 相对于 U 的补集
  - (intersect (union S T) (complement S)) 表示复合运算

每轮你可以提交一对集合表达式 (X, Y)，系统会返回一个非负整数作为应答。

系统的应答模式在整个游戏过程中保持不变，但具体是以下哪一种模式是未知的：
- 模式 A：返回 X 和 Y 的并集的元素个数
- 模式 B：返回 X 和 Y 的交集的元素个数
- 模式 C：返回 X 和 Y 的对称差的元素个数（即只属于其中一个集合的元素个数）
- 模式 D：返回 X 的元素个数加上 Y 的元素个数

你的目标是通过尽可能少的查询，同时推断出：
1. 系统的应答模式（A、B、C 或 D）
2. S 和 T 的并集的元素个数

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询需要提供两个集合表达式 expr1 和 expr2。表达式使用前缀表示法，格式如下：

- 基本集合：empty、U、S、T
- 并集运算：(union E1 E2)
- 交集运算：(intersect E1 E2)
- 补集运算：(complement E)

查询格式：
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

提交最终答案时，需要说明应答模式（A、B、C 或 D）和 S 与 T 并集的元素个数，格式如下：

<answer>mode=A, count=5</answer>
"""

    game_rule_en = """\
Let's play a "Set Query Black Box" deduction game. Here are the rules:

The game defines a finite universal set U containing N elements (N is unknown and greater than or equal to 0). Within this universal set, there exist two fixed but unknown subsets S and T.

You can construct queries using set expressions. The construction rules for set expressions are:
- Basic elements: empty set (empty), universal set (U), subset S, subset T
- Operators: union, intersect, complement
- Expression examples:
  - (union S T) represents the union of S and T
  - (intersect S T) represents the intersection of S and T
  - (complement S) represents the complement of S relative to U
  - (intersect (union S T) (complement S)) represents composite operations

Each round you can submit a pair of set expressions (X, Y), and the system will return a non-negative integer as the response.

The system's response mode remains constant throughout the game, but which of the following modes it is remains unknown:
- Mode A: Returns the number of elements in the union of X and Y
- Mode B: Returns the number of elements in the intersection of X and Y
- Mode C: Returns the number of elements in the symmetric difference of X and Y (elements in exactly one of the sets)
- Mode D: Returns the number of elements in X plus the number of elements in Y

Your goal is to infer, through as few queries as possible:
1. The system's response mode (A, B, C, or D)
2. The number of elements in the union of S and T

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

## Query and Answer Format (must be strictly followed)

Each query requires two set expressions expr1 and expr2. Expressions use prefix notation with the following format:

- Basic sets: empty, U, S, T
- Union operation: (union E1 E2)
- Intersection operation: (intersect E1 E2)
- Complement operation: (complement E)

Query format:
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

When submitting the final answer, specify the response mode (A, B, C, or D) and the number of elements in the union of S and T:

<answer>mode=A, count=5</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用智能交通路网诊断系统。为了排查城市路网状态，我们需要进行一次盲测推断。

系统接入了一个城市路网的全部监控节点全集 U，共包含 N 个节点（N 的值未知且大于等于 0）。在这些节点中，存在两个固定但未知的子集：
- 子集 S：当前发生严重拥堵的监控节点集合。
- 子集 T：当前发生交通事故的监控节点集合。

你可以通过集合表达式来向交通诊断系统构造查询，集合表达式的构造规则如下：
- 基本元素：空集 empty、全集 U、子集 S、子集 T
- 运算符：并集 union、交集 intersect、补集 complement
- 表达式示例：
  - (union S T) 表示 S 和 T 的并集（即拥堵或有事故的节点）
  - (intersect S T) 表示 S 和 T 的交集（既拥堵又有事故的节点）
  - (complement S) 表示 S 相对于 U 的补集（即未拥堵的节点）
  - (intersect (union S T) (complement S)) 表示复合运算

每轮你可以提交一对集合表达式 (X, Y)，系统会返回一个非负整数作为应答。

系统接口的应答模式在整个排查过程中保持不变，但具体是以下哪一种模式是未知的：
- 模式 A：返回 X 和 Y 的并集的节点个数
- 模式 B：返回 X 和 Y 的交集的节点个数
- 模式 C：返回 X 和 Y 的对称差的节点个数（即只属于其中一个集合的节点个数）
- 模式 D：返回 X 的节点个数加上 Y 的节点个数

你的目标是通过尽可能少的查询，同时推断出：
1. 系统的应答模式（A、B、C 或 D）
2. 发生严重拥堵或交通事故的节点总数（即 S 和 T 的并集的元素个数）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，排查失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询需要提供两个集合表达式 expr1 和 expr2。表达式使用前缀表示法，格式如下：

- 基本集合：empty、U、S、T
- 并集运算：(union E1 E2)
- 交集运算：(intersect E1 E2)
- 补集运算：(complement E)

查询格式：
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

提交最终答案时，需要说明应答模式（A、B、C 或 D）和 S 与 T 并集的元素个数，格式如下：

<answer>mode=A, count=5</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Network Diagnostic System. To troubleshoot the city's road network, we need to conduct a blind inference test.

The system is connected to a universal set U of all monitoring nodes in the city network, containing N nodes (N is unknown and greater than or equal to 0). Within this set, there exist two fixed but unknown subsets:
- Subset S: The set of nodes currently experiencing severe congestion.
- Subset T: The set of nodes currently reporting traffic accidents.

You can construct queries to the diagnostic system using set expressions. The construction rules for set expressions are:
- Basic elements: empty set (empty), universal set (U), subset S, subset T
- Operators: union, intersect, complement
- Expression examples:
  - (union S T) represents the union of S and T (nodes congested or with accidents)
  - (intersect S T) represents the intersection of S and T (nodes both congested and with accidents)
  - (complement S) represents the complement of S relative to U (uncongested nodes)
  - (intersect (union S T) (complement S)) represents composite operations

Each round you can submit a pair of set expressions (X, Y), and the system will return a non-negative integer as the response.

The system interface's response mode remains constant throughout the troubleshooting process, but which of the following modes it is remains unknown:
- Mode A: Returns the number of nodes in the union of X and Y
- Mode B: Returns the number of nodes in the intersection of X and Y
- Mode C: Returns the number of nodes in the symmetric difference of X and Y (nodes in exactly one of the sets)
- Mode D: Returns the number of nodes in X plus the number of nodes in Y

Your goal is to infer, through as few queries as possible:
1. The system's response mode (A, B, C, or D)
2. The total number of nodes experiencing either severe congestion or traffic accidents (i.e., the number of elements in the union of S and T)

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the troubleshooting fails.

## Query and Answer Format (must be strictly followed)

Each query requires two set expressions expr1 and expr2. Expressions use prefix notation with the following format:

- Basic sets: empty, U, S, T
- Union operation: (union E1 E2)
- Intersection operation: (intersect E1 E2)
- Complement operation: (complement E)

Query format:
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

When submitting the final answer, specify the response mode (A, B, C, or D) and the number of elements in the union of S and T:

<answer>mode=A, count=5</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用临床基因组学数据检索系统。为了分析罕见病的致病机理，我们需要在黑盒模式下进行数据探查。

系统建立了一个罕见病病例样本的有限全集 U，包含 N 个病例（N 的值未知且大于等于 0）。在这个样本库中，存在两个固定但未知的病例集合：
- 子集 S：携带特定基因突变 Alpha 的病例集合。
- 子集 T：携带特定基因突变 Beta 的病例集合。

你可以通过集合表达式来向数据库构造查询，集合表达式的构造规则如下：
- 基本元素：空集 empty、全集 U、子集 S、子集 T
- 运算符：并集 union、交集 intersect、补集 complement
- 表达式示例：
  - (union S T) 表示 S 和 T 的并集（携带 Alpha 或 Beta 突变的病例）
  - (intersect S T) 表示 S 和 T 的交集（同时携带 Alpha 和 Beta 突变的病例）
  - (complement S) 表示 S 相对于 U 的补集（不携带 Alpha 突变的病例）
  - (intersect (union S T) (complement S)) 表示复合运算

每轮你可以提交一对集合表达式 (X, Y)，系统会返回一个非负整数作为应答。

系统的数据脱敏应答模式在整个探查过程中保持不变，但具体是以下哪一种模式是未知的：
- 模式 A：返回 X 和 Y 的并集的病例个数
- 模式 B：返回 X 和 Y 的交集的病例个数
- 模式 C：返回 X 和 Y 的对称差的病例个数（即只属于其中一个集合的病例个数）
- 模式 D：返回 X 的病例个数加上 Y 的病例个数

你的目标是通过尽可能少的查询，同时推断出：
1. 系统的应答模式（A、B、C 或 D）
2. 携带至少一种特定基因突变（Alpha 或 Beta）的病例总数（即 S 和 T 的并集的元素个数）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，探查失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询需要提供两个集合表达式 expr1 和 expr2。表达式使用前缀表示法，格式如下：

- 基本集合：empty、U、S、T
- 并集运算：(union E1 E2)
- 交集运算：(intersect E1 E2)
- 补集运算：(complement E)

查询格式：
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

提交最终答案时，需要说明应答模式（A、B、C 或 D）和 S 与 T 并集的元素个数，格式如下：

<answer>mode=A, count=5</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Clinical Genomics Data Retrieval System. To analyze the pathogenic mechanisms of rare diseases, we need to conduct data probing in a black-box mode.

The system has established a finite universal set U of rare disease case samples, containing N cases (N is unknown and greater than or equal to 0). Within this repository, there exist two fixed but unknown case subsets:
- Subset S: The set of cases carrying the specific genetic mutation Alpha.
- Subset T: The set of cases carrying the specific genetic mutation Beta.

You can construct queries to the database using set expressions. The construction rules for set expressions are:
- Basic elements: empty set (empty), universal set (U), subset S, subset T
- Operators: union, intersect, complement
- Expression examples:
  - (union S T) represents the union of S and T (cases with Alpha or Beta mutation)
  - (intersect S T) represents the intersection of S and T (cases with both Alpha and Beta mutations)
  - (complement S) represents the complement of S relative to U (cases without Alpha mutation)
  - (intersect (union S T) (complement S)) represents composite operations

Each round you can submit a pair of set expressions (X, Y), and the system will return a non-negative integer as the response.

The system's data-desensitized response mode remains constant throughout the probing process, but which of the following modes it is remains unknown:
- Mode A: Returns the number of cases in the union of X and Y
- Mode B: Returns the number of cases in the intersection of X and Y
- Mode C: Returns the number of cases in the symmetric difference of X and Y (cases in exactly one of the sets)
- Mode D: Returns the number of cases in X plus the number of cases in Y

Your goal is to infer, through as few queries as possible:
1. The system's response mode (A, B, C, or D)
2. The total number of cases carrying at least one of the specific genetic mutations (Alpha or Beta) (i.e., the number of elements in the union of S and T)

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the probing fails.

## Query and Answer Format (must be strictly followed)

Each query requires two set expressions expr1 and expr2. Expressions use prefix notation with the following format:

- Basic sets: empty, U, S, T
- Union operation: (union E1 E2)
- Intersection operation: (intersect E1 E2)
- Complement operation: (complement E)

Query format:
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

When submitting the final answer, specify the response mode (A, B, C, or D) and the number of elements in the union of S and T:

<answer>mode=A, count=5</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用高校教务大数据分析平台。为了评估核心课程的选修情况，我们需要通过安全接口进行数据推断。

系统划定了一个参与在线学习平台的全体学生全集 U，包含 N 名学生（N 的值未知且大于等于 0）。在这个全集中，存在两个固定但未知的学生子集：
- 子集 S：选修了“高级人工智能”课程的学生集合。
- 子集 T：选修了“算法分析与设计”课程的学生集合。

你可以通过集合表达式来向教务接口构造查询，集合表达式的构造规则如下：
- 基本元素：空集 empty、全集 U、子集 S、子集 T
- 运算符：并集 union、交集 intersect、补集 complement
- 表达式示例：
  - (union S T) 表示 S 和 T 的并集
  - (intersect S T) 表示 S 和 T 的交集
  - (complement S) 表示 S 相对于 U 的补集
  - (intersect (union S T) (complement S)) 表示复合运算

每轮你可以提交一对集合表达式 (X, Y)，接口会返回一个非负整数作为应答。

安全接口的统计应答模式在整个分析过程中保持不变，但具体是以下哪一种模式是未知的：
- 模式 A：返回 X 和 Y 的并集的学生人数
- 模式 B：返回 X 和 Y 的交集的学生人数
- 模式 C：返回 X 和 Y 的对称差的学生人数（即只选修了其中一门课程的学生人数）
- 模式 D：返回 X 的学生人数加上 Y 的学生人数

你的目标是通过尽可能少的查询，同时推断出：
1. 接口的统计应答模式（A、B、C 或 D）
2. 选修了这两门核心课程中至少一门的学生总数（即 S 和 T 的并集的元素个数）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，分析失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询需要提供两个集合表达式 expr1 和 expr2。表达式使用前缀表示法，格式如下：

- 基本集合：empty、U、S、T
- 并集运算：(union E1 E2)
- 交集运算：(intersect E1 E2)
- 补集运算：(complement E)

查询格式：
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

提交最终答案时，需要说明应答模式（A、B、C 或 D）和 S 与 T 并集的元素个数，格式如下：

<answer>mode=A, count=5</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the University Academic Big Data Analysis Platform. To evaluate the enrollment in core courses, we need to conduct data inference through a secure interface.

The system defines a universal set U of all students participating in the online learning platform, containing N students (N is unknown and greater than or equal to 0). Within this universal set, there exist two fixed but unknown student subsets:
- Subset S: The set of students enrolled in "Advanced Artificial Intelligence".
- Subset T: The set of students enrolled in "Algorithm Analysis and Design".

You can construct queries to the academic interface using set expressions. The construction rules for set expressions are:
- Basic elements: empty set (empty), universal set (U), subset S, subset T
- Operators: union, intersect, complement
- Expression examples:
  - (union S T) represents the union of S and T
  - (intersect S T) represents the intersection of S and T
  - (complement S) represents the complement of S relative to U
  - (intersect (union S T) (complement S)) represents composite operations

Each round you can submit a pair of set expressions (X, Y), and the interface will return a non-negative integer as the response.

The secure interface's statistical response mode remains constant throughout the analysis process, but which of the following modes it is remains unknown:
- Mode A: Returns the number of students in the union of X and Y
- Mode B: Returns the number of students in the intersection of X and Y
- Mode C: Returns the number of students in the symmetric difference of X and Y (students enrolled in exactly one of the courses)
- Mode D: Returns the number of students in X plus the number of students in Y

Your goal is to infer, through as few queries as possible:
1. The interface's statistical response mode (A, B, C, or D)
2. The total number of students enrolled in at least one of these two core courses (i.e., the number of elements in the union of S and T)

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the analysis fails.

## Query and Answer Format (must be strictly followed)

Each query requires two set expressions expr1 and expr2. Expressions use prefix notation with the following format:

- Basic sets: empty, U, S, T
- Union operation: (union E1 E2)
- Intersection operation: (intersect E1 E2)
- Complement operation: (complement E)

Query format:
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

When submitting the final answer, specify the response mode (A, B, C, or D) and the number of elements in the union of S and T:

<answer>mode=A, count=5</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用智能制造流水线的质检黑盒探测仪。为了评估批次质量，我们需要对产线上的零部件进行无损检测推断。

探测仪扫描了当前批次的精密零部件全集 U，共包含 N 个零件（N 的值未知且大于等于 0）。在该批次中，存在两个固定但未知的缺陷集合：
- 子集 S：尺寸存在超差缺陷的零件集合。
- 子集 T：表面存在划痕缺陷的零件集合。

你可以通过集合表达式来向探测仪构造查询，集合表达式的构造规则如下：
- 基本元素：空集 empty、全集 U、子集 S、子集 T
- 运算符：并集 union、交集 intersect、补集 complement
- 表达式示例：
  - (union S T) 表示 S 和 T 的并集
  - (intersect S T) 表示 S 和 T 的交集
  - (complement S) 表示 S 相对于 U 的补集
  - (intersect (union S T) (complement S)) 表示复合运算

每轮你可以提交一对集合表达式 (X, Y)，探测仪会返回一个非负整数作为应答。

探测仪的传感器反馈模式在整个检测过程中保持不变，但具体是以下哪一种模式是未知的：
- 模式 A：返回 X 和 Y 的并集的零件个数
- 模式 B：返回 X 和 Y 的交集的零件个数
- 模式 C：返回 X 和 Y 的对称差的零件个数（即仅具有一种缺陷的零件个数）
- 模式 D：返回 X 的零件个数加上 Y 的零件个数

你的目标是通过尽可能少的查询，同时推断出：
1. 探测仪的传感器反馈模式（A、B、C 或 D）
2. 存在至少一种缺陷（尺寸超差或表面划痕）的不合格零件总数（即 S 和 T 的并集的元素个数）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，检测失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询需要提供两个集合表达式 expr1 和 expr2。表达式使用前缀表示法，格式如下：

- 基本集合：empty、U、S、T
- 并集运算：(union E1 E2)
- 交集运算：(intersect E1 E2)
- 补集运算：(complement E)

查询格式：
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

提交最终答案时，需要说明应答模式（A、B、C 或 D）和 S 与 T 并集的元素个数，格式如下：

<answer>mode=A, count=5</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the Quality Inspection Black Box Detector of the Smart Manufacturing Assembly Line. To assess batch quality, we need to perform non-destructive testing inference on the components on the production line.

The detector has scanned a universal set U of precision components from the current batch, containing N components (N is unknown and greater than or equal to 0). Within this batch, there exist two fixed but unknown defect subsets:
- Subset S: The set of components with out-of-tolerance dimensional defects.
- Subset T: The set of components with surface scratch defects.

You can construct queries to the detector using set expressions. The construction rules for set expressions are:
- Basic elements: empty set (empty), universal set (U), subset S, subset T
- Operators: union, intersect, complement
- Expression examples:
  - (union S T) represents the union of S and T
  - (intersect S T) represents the intersection of S and T
  - (complement S) represents the complement of S relative to U
  - (intersect (union S T) (complement S)) represents composite operations

Each round you can submit a pair of set expressions (X, Y), and the detector will return a non-negative integer as the response.

The detector's sensor feedback mode remains constant throughout the inspection process, but which of the following modes it is remains unknown:
- Mode A: Returns the number of components in the union of X and Y
- Mode B: Returns the number of components in the intersection of X and Y
- Mode C: Returns the number of components in the symmetric difference of X and Y (components with exactly one type of defect)
- Mode D: Returns the number of components in X plus the number of components in Y

Your goal is to infer, through as few queries as possible:
1. The detector's sensor feedback mode (A, B, C, or D)
2. The total number of non-compliant components with at least one type of defect (dimensional out-of-tolerance or surface scratch) (i.e., the number of elements in the union of S and T)

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the inspection fails.

## Query and Answer Format (must be strictly followed)

Each query requires two set expressions expr1 and expr2. Expressions use prefix notation with the following format:

- Basic sets: empty, U, S, T
- Union operation: (union E1 E2)
- Intersection operation: (intersect E1 E2)
- Complement operation: (complement E)

Query format:
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

When submitting the final answer, specify the response mode (A, B, C, or D) and the number of elements in the union of S and T:

<answer>mode=A, count=5</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用法律电子取证与案卷分析系统。为了理清一起复杂商业诉讼的证据链，我们需要在保密隔离区内进行案卷检索推断。

系统索引了本次诉讼相关的全部案卷材料全集 U，共包含 N 份案卷（N 的值未知且大于等于 0）。在这些案卷中，存在两个固定但未知的证据子集：
- 子集 S：包含“财务造假”直接证据的案卷集合。
- 子集 T：包含“违规披露”直接证据的案卷集合。

你可以通过集合表达式来向取证系统构造查询，集合表达式的构造规则如下：
- 基本元素：空集 empty、全集 U、子集 S、子集 T
- 运算符：并集 union、交集 intersect、补集 complement
- 表达式示例：
  - (union S T) 表示 S 和 T 的并集
  - (intersect S T) 表示 S 和 T 的交集
  - (complement S) 表示 S 相对于 U 的补集
  - (intersect (union S T) (complement S)) 表示复合运算

每轮你可以提交一对集合表达式 (X, Y)，取证系统会返回一个非负整数作为应答。

取证系统的保密检索应答模式在整个分析过程中保持不变，但具体是以下哪一种模式是未知的：
- 模式 A：返回 X 和 Y 的并集的案卷份数
- 模式 B：返回 X 和 Y 的交集的案卷份数
- 模式 C：返回 X 和 Y 的对称差的案卷份数（即仅包含一种违规证据的案卷份数）
- 模式 D：返回 X 的案卷份数加上 Y 的案卷份数

你的目标是通过尽可能少的查询，同时推断出：
1. 取证系统的检索应答模式（A、B、C 或 D）
2. 包含任意一种违规证据（财务造假或违规披露）的案卷总数（即 S 和 T 的并集的元素个数）

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，取证失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询需要提供两个集合表达式 expr1 和 expr2。表达式使用前缀表示法，格式如下：

- 基本集合：empty、U、S、T
- 并集运算：(union E1 E2)
- 交集运算：(intersect E1 E2)
- 补集运算：(complement E)

查询格式：
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

提交最终答案时，需要说明应答模式（A、B、C 或 D）和 S 与 T 并集的元素个数，格式如下：

<answer>mode=A, count=5</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Legal E-Discovery and Case File Analysis System. To clarify the chain of evidence in a complex commercial litigation, we need to conduct case file retrieval inference within a confidential quarantine area.

The system has indexed a universal set U of all case file materials related to this litigation, containing N files (N is unknown and greater than or equal to 0). Among these files, there exist two fixed but unknown evidentiary subsets:
- Subset S: The set of files containing direct evidence of "financial fraud".
- Subset T: The set of files containing direct evidence of "regulatory non-compliance in disclosure".

You can construct queries to the e-discovery system using set expressions. The construction rules for set expressions are:
- Basic elements: empty set (empty), universal set (U), subset S, subset T
- Operators: union, intersect, complement
- Expression examples:
  - (union S T) represents the union of S and T
  - (intersect S T) represents the intersection of S and T
  - (complement S) represents the complement of S relative to U
  - (intersect (union S T) (complement S)) represents composite operations

Each round you can submit a pair of set expressions (X, Y), and the e-discovery system will return a non-negative integer as the response.

The system's confidential retrieval response mode remains constant throughout the analysis process, but which of the following modes it is remains unknown:
- Mode A: Returns the number of files in the union of X and Y
- Mode B: Returns the number of files in the intersection of X and Y
- Mode C: Returns the number of files in the symmetric difference of X and Y (files containing exactly one type of non-compliant evidence)
- Mode D: Returns the number of files in X plus the number of files in Y

Your goal is to infer, through as few queries as possible:
1. The e-discovery system's retrieval response mode (A, B, C, or D)
2. The total number of files containing any type of non-compliant evidence (financial fraud or regulatory non-compliance in disclosure) (i.e., the number of elements in the union of S and T)

When you have gathered enough information, submit your final answer. If the answer is wrong or the format is invalid, the e-discovery fails.

## Query and Answer Format (must be strictly followed)

Each query requires two set expressions expr1 and expr2. Expressions use prefix notation with the following format:

- Basic sets: empty, U, S, T
- Union operation: (union E1 E2)
- Intersection operation: (intersect E1 E2)
- Complement operation: (complement E)

Query format:
<query>
expr1: (union S T)
expr2: (intersect S T)
</query>

When submitting the final answer, specify the response mode (A, B, C, or D) and the number of elements in the union of S and T:

<answer>mode=A, count=5</answer>
"""

    tags = ["answer", "query"]

    # 难度配置：
    # 1 (简单)      - N=10, 简单的S和T配置，模式A
    # 2 (中等偏下)  - N=15, 有重叠的S和T，模式B
    # 3 (中等偏上)  - N=20, 复杂重叠，模式C
    # 4 (较难)      - N=25, S和T关系复杂，模式D
    # 5 (难)        - N=30, 高度复杂的配置，模式C

    DIFFICULTY_CONFIG = {
        1: {
            "N": 10,
            "S": {1, 2, 3, 4},      # |S| = 4
            "T": {5, 6, 7},         # |T| = 3
            "mode": "A",            # |S ∪ T| = 7
        },
        2: {
            "N": 15,
            "S": {1, 2, 3, 4, 5, 6},    # |S| = 6
            "T": {4, 5, 6, 7, 8},       # |T| = 5
            "mode": "B",                # |S ∪ T| = 8, |S ∩ T| = 3
        },
        3: {
            "N": 20,
            "S": {1, 2, 3, 4, 5, 6, 7, 8},      # |S| = 8
            "T": {5, 6, 7, 8, 9, 10, 11, 12},   # |T| = 8
            "mode": "C",                        # |S ∪ T| = 12
        },
        4: {
            "N": 25,
            "S": {1, 3, 5, 7, 9, 11, 13, 15},   # |S| = 8
            "T": {2, 4, 6, 8, 10, 12, 14},      # |T| = 7
            "mode": "D",                        # |S ∪ T| = 15
        },
        5: {
            "N": 30,
            "S": {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12},       # |S| = 12
            "T": {6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16},      # |T| = 11
            "mode": "C",                                         # |S ∪ T| = 16
        },
    }

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[diff]
        self.N = cfg["N"]
        self.S = set(cfg["S"])  # 复制，避免修改类变量
        self.T = set(cfg["T"])
        self.mode = cfg["mode"]
        
        # 计算全集 U
        self.U = set(range(1, self.N + 1))
        
        # 计算正确答案：S ∪ T 的大小
        self.answer_count = len(self.S | self.T)
        
        # 用于规则模板的占位符（当前模板中未使用，但保留以备扩展）
        self._game_info = {}


    def _parse_set_expression(self, expr_str):
        """
        解析集合表达式，返回对应的集合
        表达式格式：前缀表示法
        - empty, U, S, T
        - (union E1 E2)
        - (intersect E1 E2)
        - (complement E)
        """
        expr_str = expr_str.strip()
        
        # 基本集合
        if expr_str == "empty":
            return set()
        elif expr_str == "U":
            return self.U.copy()
        elif expr_str == "S":
            return self.S.copy()
        elif expr_str == "T":
            return self.T.copy()
        
        # 复合表达式：必须以括号开始
        if not (expr_str.startswith("(") and expr_str.endswith(")")):
            raise ValueError(f"Invalid expression format: {expr_str}")
        
        # 去掉最外层括号
        inner = expr_str[1:-1].strip()
        
        # 解析运算符
        parts = self._split_expression(inner)
        
        if len(parts) == 0:
            raise ValueError(f"Empty expression: {expr_str}")
        
        op = parts[0]
        
        if op == "complement":
            if len(parts) != 2:
                raise ValueError(f"complement requires 1 argument: {expr_str}")
            arg = self._parse_set_expression(parts[1])
            return self.U - arg
        
        elif op == "union":
            if len(parts) != 3:
                raise ValueError(f"union requires 2 arguments: {expr_str}")
            arg1 = self._parse_set_expression(parts[1])
            arg2 = self._parse_set_expression(parts[2])
            return arg1 | arg2
        
        elif op == "intersect":
            if len(parts) != 3:
                raise ValueError(f"intersect requires 2 arguments: {expr_str}")
            arg1 = self._parse_set_expression(parts[1])
            arg2 = self._parse_set_expression(parts[2])
            return arg1 & arg2
        
        else:
            raise ValueError(f"Unknown operator: {op}")

    def _split_expression(self, expr):
        """
        将表达式按空格分割，但保持括号内的内容完整
        例如："union S (intersect T U)" -> ["union", "S", "(intersect T U)"]
        """
        parts = []
        current = ""
        depth = 0
        
        for char in expr:
            if char == "(":
                depth += 1
                current += char
            elif char == ")":
                depth -= 1
                current += char
            elif char == " " and depth == 0:
                if current:
                    parts.append(current)
                    current = ""
            else:
                current += char
        
        if current:
            parts.append(current)
        
        return parts

    def _compute_response(self, set_x, set_y):
        """
        根据当前模式计算对 (X, Y) 的响应
        """
        if self.mode == "A":
            # 返回 |X ∪ Y|
            return len(set_x | set_y)
        elif self.mode == "B":
            # 返回 |X ∩ Y|
            return len(set_x & set_y)
        elif self.mode == "C":
            # 返回 |X △ Y| (对称差)
            return len(set_x ^ set_y)
        elif self.mode == "D":
            # 返回 |X| + |Y|
            return len(set_x) + len(set_y)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def evaluate(self, parsed_info):
        """
        评估玩家提交的答案是否正确
        答案格式：mode=X, count=Y
        """
        raw_ans = parsed_info["answer"]
        
        # 解析答案
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip().lower()] = v.strip()
        
        if "mode" not in ans_dict or "count" not in ans_dict:
            return False
        
        # 检查模式（大小写不敏感）
        if ans_dict["mode"].upper() != self.mode:
            return False
        
        # 检查计数
        try:
            count = int(ans_dict["count"])
        except (ValueError, TypeError):
            return False
        
        return count == self.answer_count

    def _cf_core_produce(self, parsed_info):
        """
        原始的业务逻辑处理
        """
        if "query" not in parsed_info:
            raise ValueError("No query found in parsed info")
        
        query_content = parsed_info["query"]
        
        # 解析 expr1 和 expr2
        # 格式: expr1: ... \n expr2: ...
        lines = [line.strip() for line in query_content.strip().split("\n") if line.strip()]
        
        expr_dict = {}
        for line in lines:
            if ":" not in line:
                continue
            key, val = line.split(":", 1)
            expr_dict[key.strip()] = val.strip()
        
        if "expr1" not in expr_dict or "expr2" not in expr_dict:
            raise ValueError("Invalid query format. Both expr1 and expr2 are required.")
        
        # 解析两个表达式
        set_x = self._parse_set_expression(expr_dict["expr1"])
        set_y = self._parse_set_expression(expr_dict["expr2"])
        
        # 计算响应
        response_value = self._compute_response(set_x, set_y)
        
        return str(response_value)

    def _cf_make_wrong(self, correct: str) -> str:
        """
        根据正确答案生成一个明显不同的错误答案。
        在本游戏中，produce_response 返回的总是数字字符串或错误提示。
        """
        stripped = correct.strip()
        # 尝试解析为整数
        try:
            val = int(stripped)
            # 返回一个不同的非负整数
            if val == 0:
                return "1"
            else:
                return str(val + 1)
        except ValueError:
            pass
        
        # 对于非数字的响应（如错误消息），直接附加标记
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举具有区分度的集合表达式组合查询。
        """
        # 选取具有代表性且能提供不同信息的表达式对
        query_pairs = [
            ("S", "T"),
            ("S", "S"),
            ("T", "T"),
            ("empty", "empty"),
            ("S", "empty"),
            ("T", "empty"),
            ("U", "empty"),
            ("S", "U"),
            ("T", "U"),
            ("(union S T)", "empty"),
            ("(intersect S T)", "empty"),
            ("(complement S)", "T"),
            ("(complement T)", "S"),
            ("(union S T)", "(intersect S T)"),
            ("S", "(complement S)"),
            ("T", "(complement T)"),
        ]
        
        possible_queries = []
        
        for e1, e2 in query_pairs:
            query_content = f"expr1: {e1}\nexpr2: {e2}"
            
            try:
                set_x = self._parse_set_expression(e1)
                set_y = self._parse_set_expression(e2)
                ans_val = self._compute_response(set_x, set_y)
                answer_str = str(ans_val)
                
                possible_queries.append({
                    "query": f"<query>\n{query_content}\n</query>",
                    "answer": answer_str
                })
            except Exception:
                continue
                
        return possible_queries