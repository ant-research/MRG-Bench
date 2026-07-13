from .base import Game
import re
import itertools

class GraphIndependenceGame(Game):
    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"图独立性推理"游戏，规则如下：

游戏设定了一个整数集合 [N] = {{1, 2, ..., {n}}}。存在一个未知的、固定的布尔关系 R，它定义了一个无向图 G：
- 图的顶点就是集合 [N] 中的所有数字
- 对于任意两个不同的数字 i 和 j（i < j），如果 R(i,j) = 1，则它们之间存在一条边
- 关系 R 是对称的且没有自环（即一个数字不会与自己连边）

你的目标是通过有限次数的查询，推断出这个未知关系 R 的规律，并最终正确判断 {k} 个测试集合是否为独立集。

**独立集定义**：一个子集 S 是独立集，当且仅当 S 内任意两个不同元素之间都不存在边。

## 可用的查询类型

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **子集独立性查询**：询问一个子集 S 是否为独立集
   - 如果 S 是独立集，回答"独立"
   - 如果 S 不是独立集，回答"非独立"，并给出 S 内字典序最小的相连边对 (x,y)，其中 x < y

2. **边存在性查询**：询问两个数字 i 和 j 之间是否存在边（要求 i < j）
   - 如果存在边，回答"存在边"
   - 如果不存在边，回答"无边"

3. **边计数查询**：询问一个子集 S 内部边的总数量
   - 回答 S 内边的数量（一个非负整数）

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 子集独立性查询（例如查询子集 {{1,3,5}}）：
<query_independence>1,3,5</query_independence>

- 边存在性查询（例如查询 2 和 5 之间）：
<query_edge>2,5</query_edge>

- 边计数查询（例如查询子集 {{1,2,3,4}}）：
<query_count>1,2,3,4</query_count>

当你完成所有查询后，需要提交最终答案，判断 {k} 个测试集合是否为独立集。格式如下：

<answer>1:yes,2:no,3:yes</answer>

其中数字表示测试集合的编号（从 1 开始），yes 表示独立集，no 表示非独立集。{k} 个判断用逗号分隔。

**注意**：
- 请尽可能少地使用查询次数来推断规律
- 以下是你需要判断的 {k} 个测试集合：
{test_sets_desc}
- 所有查询的回答保证一致性
- 答案格式必须严格按照要求，否则视为失败
"""

    game_rule_en = """\
Let's play a "Graph Independence Reasoning" game. Here are the rules:

The game defines an integer set [N] = {{1, 2, ..., {n}}}. There exists an unknown, fixed boolean relation R that defines an undirected graph G:
- The vertices of the graph are all numbers in set [N]
- For any two different numbers i and j (i < j), if R(i,j) = 1, there is an edge between them
- Relation R is symmetric and has no self-loops (a number cannot connect to itself)

Your goal is to infer the pattern of this unknown relation R through a limited number of queries, and finally correctly determine whether {k} test sets are independent sets.

**Independent Set Definition**: A subset S is an independent set if and only if there is no edge between any two different elements in S.

## Available Query Types

You can repeatedly make the following three types of queries (one query at a time):

1. **Subset Independence Query**: Ask whether a subset S is an independent set
   - If S is independent, answer "Independent"
   - If S is not independent, answer "Not Independent" and provide the lexicographically smallest connected pair (x,y) in S, where x < y

2. **Edge Existence Query**: Ask whether there is an edge between two numbers i and j (require i < j)
   - If an edge exists, answer "Edge exists"
   - If no edge exists, answer "No edge"

3. **Edge Count Query**: Ask for the total number of edges within a subset S
   - Answer the number of edges in S (a non-negative integer)

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset Independence Query (e.g., query subset {{1,3,5}}):
<query_independence>1,3,5</query_independence>

- Edge Existence Query (e.g., query between 2 and 5):
<query_edge>2,5</query_edge>

- Edge Count Query (e.g., query subset {{1,2,3,4}}):
<query_count>1,2,3,4</query_count>

After completing all queries, you need to submit the final answer to determine whether the {k} test sets are independent sets. Format as follows:

<answer>1:yes,2:no,3:yes</answer>

Where the number indicates the test set number (starting from 1), yes means independent set, no means not independent set. Separate the {k} judgments with commas.

**Note**:
- Use as few queries as possible to infer the pattern
- Here are the {k} test sets you need to judge:
{test_sets_desc}
- All query answers are guaranteed to be consistent
- Answer format must strictly follow the requirements, otherwise it is considered a failure
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市交通路口冲突分析系统”。

系统管控着辖区内 [N] = {{1, 2, ..., {n}}} 号交通路口。存在一个未知的、固定的交通流冲突关系 R，它定义了一个无向图 G：
- 图的顶点即为集合 [N] 中的所有路口编号
- 对于任意两个不同的路口 i 和 j（i < j），如果 R(i,j) = 1，表示这两个路口的车流存在严重冲突（即存在边）
- 冲突关系是对称的且没有自环（即单个路口自身不存在冲突）

你的目标是通过有限次数的查询，推断出该路网冲突关系 R 的规律，并最终正确判断 {k} 个路口测试子集是否为无冲突的“安全并行集”（即独立集）。

**独立集（安全并行集）定义**：一个子集 S 是独立集，当且仅当 S 内任意两个不同路口之间都不存在冲突（边）。

## 可用的查询类型

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **子集独立性查询**：询问一个路口子集 S 是否为独立集
   - 如果 S 是独立集，回答"独立"
   - 如果 S 不是独立集，回答"非独立"，并给出 S 内字典序最小的冲突相连边对 (x,y)，其中 x < y

2. **边存在性查询**：询问两个路口 i 和 j 之间是否存在冲突（即边）（要求 i < j）
   - 如果存在冲突（边），回答"存在边"
   - 如果不存在冲突，回答"无边"

3. **边计数查询**：询问一个路口子集 S 内部冲突（边）的总数量
   - 回答 S 内冲突的总数量（一个非负整数）

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 子集独立性查询（例如查询子集 {{1,3,5}}）：
<query_independence>1,3,5</query_independence>

- 边存在性查询（例如查询 2 和 5 之间）：
<query_edge>2,5</query_edge>

- 边计数查询（例如查询子集 {{1,2,3,4}}）：
<query_count>1,2,3,4</query_count>

当你完成所有查询后，需要提交最终答案，判断 {k} 个测试集合是否为独立集。格式如下：

<answer>1:yes,2:no,3:yes</answer>

其中数字表示测试集合的编号（从 1 开始），yes 表示独立集，no 表示非独立集。{k} 个判断用逗号分隔。

**注意**：
- 请尽可能少地使用查询次数来推断规律
- 以下是你需要判断的 {k} 个测试集合：
{test_sets_desc}
- 所有查询的回答保证一致性
- 答案格式必须严格按照要求，否则视为失败
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Intersection Conflict Analysis System".

The system manages traffic intersections numbered [N] = {{1, 2, ..., {n}}}. There exists an unknown, fixed traffic flow conflict relation R that defines an undirected graph G:
- The vertices of the graph are all intersection numbers in set [N]
- For any two different intersections i and j (i < j), if R(i,j) = 1, it means their traffic flows have a severe conflict (i.e., there is an edge between them)
- Relation R is symmetric and has no self-loops (an intersection cannot conflict with itself)

Your goal is to infer the pattern of this conflict relation R through a limited number of queries, and finally correctly determine whether {k} test sets are conflict-free "safe parallel sets" (i.e., independent sets).

**Independent Set (Safe Parallel Set) Definition**: A subset S is an independent set if and only if there is no conflict (edge) between any two different elements in S.

## Available Query Types

You can repeatedly make the following three types of queries (one query at a time):

1. **Subset Independence Query**: Ask whether a subset S is an independent set
   - If S is independent, answer "Independent"
   - If S is not independent, answer "Not Independent" and provide the lexicographically smallest connected conflict pair (x,y) in S, where x < y

2. **Edge Existence Query**: Ask whether there is a conflict (edge) between two intersections i and j (require i < j)
   - If a conflict exists, answer "Edge exists"
   - If no conflict exists, answer "No edge"

3. **Edge Count Query**: Ask for the total number of conflicts (edges) within a subset S
   - Answer the number of conflicts in S (a non-negative integer)

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset Independence Query (e.g., query subset {{1,3,5}}):
<query_independence>1,3,5</query_independence>

- Edge Existence Query (e.g., query between 2 and 5):
<query_edge>2,5</query_edge>

- Edge Count Query (e.g., query subset {{1,2,3,4}}):
<query_count>1,2,3,4</query_count>

After completing all queries, you need to submit the final answer to determine whether the {k} test sets are independent sets. Format as follows:

<answer>1:yes,2:no,3:yes</answer>

Where the number indicates the test set number (starting from 1), yes means independent set, no means not independent set. Separate the {k} judgments with commas.

**Note**:
- Use as few queries as possible to infer the pattern
- Here are the {k} test sets you need to judge:
{test_sets_desc}
- All query answers are guaranteed to be consistent
- Answer format must strictly follow the requirements, otherwise it is considered a failure
"""

    contextualized_rule_zh_2 = """\
欢迎使用“临床药物配伍禁忌分析系统”。

系统收录了 [N] = {{1, 2, ..., {n}}} 号候选药物。存在一个未知的、固定的不良相互作用关系 R，它定义了一个无向图 G：
- 图的顶点即为集合 [N] 中的所有药物编号
- 对于任意两种不同的药物 i 和 j（i < j），如果 R(i,j) = 1，表示这两种药物联用会产生不良反应（即存在边）
- 相互作用是对称的且没有自环（即单一药物不存在自我配伍禁忌）

你的目标是通过有限次数的查询，推断出这种药物相互作用 R 的规律，并最终正确判断 {k} 个处方测试集合是否为安全的“联合用药集”（即独立集）。

**独立集（联合用药集）定义**：一个子集 S 是独立集，当且仅当 S 内任意两种不同药物之间都不存在不良反应（边）。

## 可用的查询类型

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **子集独立性查询**：询问一个药物子集 S 是否为独立集
   - 如果 S 是独立集，回答"独立"
   - 如果 S 不是独立集，回答"非独立"，并给出 S 内字典序最小的不良反应边对 (x,y)，其中 x < y

2. **边存在性查询**：询问两种药物 i 和 j 之间是否存在相互作用（即边）（要求 i < j）
   - 如果存在作用（边），回答"存在边"
   - 如果不存在作用，回答"无边"

3. **边计数查询**：询问一个药物子集 S 内部不良反应（边）的总数量
   - 回答 S 内相互作用的总数量（一个非负整数）

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 子集独立性查询（例如查询子集 {{1,3,5}}）：
<query_independence>1,3,5</query_independence>

- 边存在性查询（例如查询 2 和 5 之间）：
<query_edge>2,5</query_edge>

- 边计数查询（例如查询子集 {{1,2,3,4}}）：
<query_count>1,2,3,4</query_count>

当你完成所有查询后，需要提交最终答案，判断 {k} 个测试集合是否为独立集。格式如下：

<answer>1:yes,2:no,3:yes</answer>

其中数字表示测试集合的编号（从 1 开始），yes 表示独立集，no 表示非独立集。{k} 个判断用逗号分隔。

**注意**：
- 请尽可能少地使用查询次数来推断规律
- 以下是你需要判断的 {k} 个测试集合：
{test_sets_desc}
- 所有查询的回答保证一致性
- 答案格式必须严格按照要求，否则视为失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Drug Interaction Analysis System".

The system includes candidate drugs numbered [N] = {{1, 2, ..., {n}}}. There exists an unknown, fixed adverse drug interaction relation R that defines an undirected graph G:
- The vertices of the graph are all drug numbers in set [N]
- For any two different drugs i and j (i < j), if R(i,j) = 1, it means co-administering them causes an adverse reaction (i.e., there is an edge between them)
- Relation R is symmetric and has no self-loops (a drug cannot interact with itself)

Your goal is to infer the pattern of this drug interaction relation R through a limited number of queries, and finally correctly determine whether {k} test sets are safe "joint medication sets" (i.e., independent sets).

**Independent Set (Joint Medication Set) Definition**: A subset S is an independent set if and only if there is no adverse interaction (edge) between any two different elements in S.

## Available Query Types

You can repeatedly make the following three types of queries (one query at a time):

1. **Subset Independence Query**: Ask whether a subset S is an independent set
   - If S is independent, answer "Independent"
   - If S is not independent, answer "Not Independent" and provide the lexicographically smallest interacting pair (x,y) in S, where x < y

2. **Edge Existence Query**: Ask whether there is an interaction (edge) between two drugs i and j (require i < j)
   - If an interaction exists, answer "Edge exists"
   - If no interaction exists, answer "No edge"

3. **Edge Count Query**: Ask for the total number of interactions (edges) within a subset S
   - Answer the number of interactions in S (a non-negative integer)

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset Independence Query (e.g., query subset {{1,3,5}}):
<query_independence>1,3,5</query_independence>

- Edge Existence Query (e.g., query between 2 and 5):
<query_edge>2,5</query_edge>

- Edge Count Query (e.g., query subset {{1,2,3,4}}):
<query_count>1,2,3,4</query_count>

After completing all queries, you need to submit the final answer to determine whether the {k} test sets are independent sets. Format as follows:

<answer>1:yes,2:no,3:yes</answer>

Where the number indicates the test set number (starting from 1), yes means independent set, no means not independent set. Separate the {k} judgments with commas.

**Note**:
- Use as few queries as possible to infer the pattern
- Here are the {k} test sets you need to judge:
{test_sets_desc}
- All query answers are guaranteed to be consistent
- Answer format must strictly follow the requirements, otherwise it is considered a failure
"""

    contextualized_rule_zh_3 = """\
欢迎使用“高校排课冲突智能检测系统”。

系统包含了 [N] = {{1, 2, ..., {n}}} 号核心课程。存在一个未知的、固定的排课时间冲突关系 R，它定义了一个无向图 G：
- 图的顶点即为集合 [N] 中的所有课程编号
- 对于任意两门不同的课程 i 和 j（i < j），如果 R(i,j) = 1，表示这两门课程上课时间冲突（即存在边）
- 冲突关系是对称的且没有自环（即单门课程不存在自我冲突）

你的目标是通过有限次数的查询，推断出这种课程冲突关系 R 的规律，并最终正确判断 {k} 个选课测试集合是否为无冲突的“可行选课集”（即独立集）。

**独立集（可行选课集）定义**：一个子集 S 是独立集，当且仅当 S 内任意两门不同课程之间都不存在时间冲突（边）。

## 可用的查询类型

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **子集独立性查询**：询问一个选课子集 S 是否为独立集
   - 如果 S 是独立集，回答"独立"
   - 如果 S 不是独立集，回答"非独立"，并给出 S 内字典序最小的冲突边对 (x,y)，其中 x < y

2. **边存在性查询**：询问两门课程 i 和 j 之间是否存在冲突（即边）（要求 i < j）
   - 如果存在冲突（边），回答"存在边"
   - 如果不存在冲突，回答"无边"

3. **边计数查询**：询问一个选课子集 S 内部时间冲突（边）的总数量
   - 回答 S 内冲突的总数量（一个非负整数）

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 子集独立性查询（例如查询子集 {{1,3,5}}）：
<query_independence>1,3,5</query_independence>

- 边存在性查询（例如查询 2 和 5 之间）：
<query_edge>2,5</query_edge>

- 边计数查询（例如查询子集 {{1,2,3,4}}）：
<query_count>1,2,3,4</query_count>

当你完成所有查询后，需要提交最终答案，判断 {k} 个测试集合是否为独立集。格式如下：

<answer>1:yes,2:no,3:yes</answer>

其中数字表示测试集合的编号（从 1 开始），yes 表示独立集，no 表示非独立集。{k} 个判断用逗号分隔。

**注意**：
- 请尽可能少地使用查询次数来推断规律
- 以下是你需要判断的 {k} 个测试集合：
{test_sets_desc}
- 所有查询的回答保证一致性
- 答案格式必须严格按照要求，否则视为失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "University Course Scheduling Conflict Detection System".

The system contains core courses numbered [N] = {{1, 2, ..., {n}}}. There exists an unknown, fixed scheduling conflict relation R that defines an undirected graph G:
- The vertices of the graph are all course numbers in set [N]
- For any two different courses i and j (i < j), if R(i,j) = 1, it means their class times conflict (i.e., there is an edge between them)
- Relation R is symmetric and has no self-loops (a course cannot conflict with itself)

Your goal is to infer the pattern of this scheduling conflict relation R through a limited number of queries, and finally correctly determine whether {k} test sets are conflict-free "feasible selection sets" (i.e., independent sets).

**Independent Set (Feasible Selection Set) Definition**: A subset S is an independent set if and only if there is no time conflict (edge) between any two different elements in S.

## Available Query Types

You can repeatedly make the following three types of queries (one query at a time):

1. **Subset Independence Query**: Ask whether a subset S is an independent set
   - If S is independent, answer "Independent"
   - If S is not independent, answer "Not Independent" and provide the lexicographically smallest conflicting pair (x,y) in S, where x < y

2. **Edge Existence Query**: Ask whether there is a conflict (edge) between two courses i and j (require i < j)
   - If a conflict exists, answer "Edge exists"
   - If no conflict exists, answer "No edge"

3. **Edge Count Query**: Ask for the total number of conflicts (edges) within a subset S
   - Answer the number of conflicts in S (a non-negative integer)

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset Independence Query (e.g., query subset {{1,3,5}}):
<query_independence>1,3,5</query_independence>

- Edge Existence Query (e.g., query between 2 and 5):
<query_edge>2,5</query_edge>

- Edge Count Query (e.g., query subset {{1,2,3,4}}):
<query_count>1,2,3,4</query_count>

After completing all queries, you need to submit the final answer to determine whether the {k} test sets are independent sets. Format as follows:

<answer>1:yes,2:no,3:yes</answer>

Where the number indicates the test set number (starting from 1), yes means independent set, no means not independent set. Separate the {k} judgments with commas.

**Note**:
- Use as few queries as possible to infer the pattern
- Here are the {k} test sets you need to judge:
{test_sets_desc}
- All query answers are guaranteed to be consistent
- Answer format must strictly follow the requirements, otherwise it is considered a failure
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业生产线工序干涉排查系统”。

系统中定义了 [N] = {{1, 2, ..., {n}}} 号生产工序。存在一个未知的、固定的工序资源干涉关系 R，它定义了一个无向图 G：
- 图的顶点即为集合 [N] 中的所有工序编号
- 对于任意两个不同的工序 i 和 j（i < j），如果 R(i,j) = 1，表示这两个工序同时进行会发生资源干涉（即存在边）
- 干涉关系是对称的且没有自环（即单个工序自身不会产生干涉）

你的目标是通过有限次数的查询，推断出这种工序干涉关系 R 的规律，并最终正确判断 {k} 个工序测试集合是否为可同时运行的“并行加工集”（即独立集）。

**独立集（并行加工集）定义**：一个子集 S 是独立集，当且仅当 S 内任意两个不同工序之间都不存在资源干涉（边）。

## 可用的查询类型

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **子集独立性查询**：询问一个工序子集 S 是否为独立集
   - 如果 S 是独立集，回答"独立"
   - 如果 S 不是独立集，回答"非独立"，并给出 S 内字典序最小的干涉边对 (x,y)，其中 x < y

2. **边存在性查询**：询问两个工序 i 和 j 之间是否存在干涉（即边）（要求 i < j）
   - 如果存在干涉（边），回答"存在边"
   - 如果不存在干涉，回答"无边"

3. **边计数查询**：询问一个工序子集 S 内部资源干涉（边）的总数量
   - 回答 S 内干涉的总数量（一个非负整数）

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 子集独立性查询（例如查询子集 {{1,3,5}}）：
<query_independence>1,3,5</query_independence>

- 边存在性查询（例如查询 2 和 5 之间）：
<query_edge>2,5</query_edge>

- 边计数查询（例如查询子集 {{1,2,3,4}}）：
<query_count>1,2,3,4</query_count>

当你完成所有查询后，需要提交最终答案，判断 {k} 个测试集合是否为独立集。格式如下：

<answer>1:yes,2:no,3:yes</answer>

其中数字表示测试集合的编号（从 1 开始），yes 表示独立集，no 表示非独立集。{k} 个判断用逗号分隔。

**注意**：
- 请尽可能少地使用查询次数来推断规律
- 以下是你需要判断的 {k} 个测试集合：
{test_sets_desc}
- 所有查询的回答保证一致性
- 答案格式必须严格按照要求，否则视为失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Production Line Process Interference Checking System".

The system defines production processes numbered [N] = {{1, 2, ..., {n}}}. There exists an unknown, fixed process resource interference relation R that defines an undirected graph G:
- The vertices of the graph are all process numbers in set [N]
- For any two different processes i and j (i < j), if R(i,j) = 1, it means running them simultaneously causes resource interference (i.e., there is an edge between them)
- Relation R is symmetric and has no self-loops (a process cannot interfere with itself)

Your goal is to infer the pattern of this interference relation R through a limited number of queries, and finally correctly determine whether {k} test sets are parallel processing sets (i.e., independent sets).

**Independent Set (Parallel Processing Set) Definition**: A subset S is an independent set if and only if there is no resource interference (edge) between any two different elements in S.

## Available Query Types

You can repeatedly make the following three types of queries (one query at a time):

1. **Subset Independence Query**: Ask whether a subset S is an independent set
   - If S is independent, answer "Independent"
   - If S is not independent, answer "Not Independent" and provide the lexicographically smallest interfering pair (x,y) in S, where x < y

2. **Edge Existence Query**: Ask whether there is an interference (edge) between two processes i and j (require i < j)
   - If an interference exists, answer "Edge exists"
   - If no interference exists, answer "No edge"

3. **Edge Count Query**: Ask for the total number of interferences (edges) within a subset S
   - Answer the number of interferences in S (a non-negative integer)

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset Independence Query (e.g., query subset {{1,3,5}}):
<query_independence>1,3,5</query_independence>

- Edge Existence Query (e.g., query between 2 and 5):
<query_edge>2,5</query_edge>

- Edge Count Query (e.g., query subset {{1,2,3,4}}):
<query_count>1,2,3,4</query_count>

After completing all queries, you need to submit the final answer to determine whether the {k} test sets are independent sets. Format as follows:

<answer>1:yes,2:no,3:yes</answer>

Where the number indicates the test set number (starting from 1), yes means independent set, no means not independent set. Separate the {k} judgments with commas.

**Note**:
- Use as few queries as possible to infer the pattern
- Here are the {k} test sets you need to judge:
{test_sets_desc}
- All query answers are guaranteed to be consistent
- Answer format must strictly follow the requirements, otherwise it is considered a failure
"""

    contextualized_rule_zh_5 = """\
欢迎使用“案件证据链逻辑排异系统”。

系统录入了 [N] = {{1, 2, ..., {n}}} 号关键证据。存在一个未知的、固定的证据矛盾关系 R，它定义了一个无向图 G：
- 图的顶点即为集合 [N] 中的所有证据编号
- 对于任意两份不同的证据 i 和 j（i < j），如果 R(i,j) = 1，表示这两份证据在逻辑上相互矛盾（即存在边）
- 矛盾关系是对称的且没有自环（即单份证据不存在自我矛盾）

你的目标是通过有限次数的查询，推断出这种证据矛盾关系 R 的规律，并最终正确判断 {k} 个证据测试集合是否为逻辑自洽的“有效证据链”（即独立集）。

**独立集（有效证据链）定义**：一个子集 S 是独立集，当且仅当 S 内任意两份不同证据之间都不存在逻辑矛盾（边）。

## 可用的查询类型

你可以反复提出以下三类查询（每次仅限一个查询）：

1. **子集独立性查询**：询问一个证据子集 S 是否为独立集
   - 如果 S 是独立集，回答"独立"
   - 如果 S 不是独立集，回答"非独立"，并给出 S 内字典序最小的逻辑矛盾边对 (x,y)，其中 x < y

2. **边存在性查询**：询问两份证据 i 和 j 之间是否存在矛盾（即边）（要求 i < j）
   - 如果存在矛盾（边），回答"存在边"
   - 如果不存在矛盾，回答"无边"

3. **边计数查询**：询问一个证据子集 S 内部逻辑矛盾（边）的总数量
   - 回答 S 内矛盾的总数量（一个非负整数）

## 查询与提交答案的格式（必须严格遵守）

每次只能包含一个查询标签。请使用以下 XML 格式：

- 子集独立性查询（例如查询子集 {{1,3,5}}）：
<query_independence>1,3,5</query_independence>

- 边存在性查询（例如查询 2 和 5 之间）：
<query_edge>2,5</query_edge>

- 边计数查询（例如查询子集 {{1,2,3,4}}）：
<query_count>1,2,3,4</query_count>

当你完成所有查询后，需要提交最终答案，判断 {k} 个测试集合是否为独立集。格式如下：

<answer>1:yes,2:no,3:yes</answer>

其中数字表示测试集合的编号（从 1 开始），yes 表示独立集，no 表示非独立集。{k} 个判断用逗号分隔。

**注意**：
- 请尽可能少地使用查询次数来推断规律
- 以下是你需要判断的 {k} 个测试集合：
{test_sets_desc}
- 所有查询的回答保证一致性
- 答案格式必须严格按照要求，否则视为失败
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Case Evidence Logic Contradiction Analysis System".

The system records key evidence items numbered [N] = {{1, 2, ..., {n}}}. There exists an unknown, fixed logical contradiction relation R that defines an undirected graph G:
- The vertices of the graph are all evidence numbers in set [N]
- For any two different evidence items i and j (i < j), if R(i,j) = 1, it means they are logically contradictory (i.e., there is an edge between them)
- Relation R is symmetric and has no self-loops (an evidence item cannot contradict itself)

Your goal is to infer the pattern of this contradiction relation R through a limited number of queries, and finally correctly determine whether {k} test sets are logically consistent "valid evidence chains" (i.e., independent sets).

**Independent Set (Valid Evidence Chain) Definition**: A subset S is an independent set if and only if there is no logical contradiction (edge) between any two different elements in S.

## Available Query Types

You can repeatedly make the following three types of queries (one query at a time):

1. **Subset Independence Query**: Ask whether a subset S is an independent set
   - If S is independent, answer "Independent"
   - If S is not independent, answer "Not Independent" and provide the lexicographically smallest contradictory pair (x,y) in S, where x < y

2. **Edge Existence Query**: Ask whether there is a contradiction (edge) between two evidence items i and j (require i < j)
   - If a contradiction exists, answer "Edge exists"
   - If no contradiction exists, answer "No edge"

3. **Edge Count Query**: Ask for the total number of contradictions (edges) within a subset S
   - Answer the number of contradictions in S (a non-negative integer)

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Subset Independence Query (e.g., query subset {{1,3,5}}):
<query_independence>1,3,5</query_independence>

- Edge Existence Query (e.g., query between 2 and 5):
<query_edge>2,5</query_edge>

- Edge Count Query (e.g., query subset {{1,2,3,4}}):
<query_count>1,2,3,4</query_count>

After completing all queries, you need to submit the final answer to determine whether the {k} test sets are independent sets. Format as follows:

<answer>1:yes,2:no,3:yes</answer>

Where the number indicates the test set number (starting from 1), yes means independent set, no means not independent set. Separate the {k} judgments with commas.

**Note**:
- Use as few queries as possible to infer the pattern
- Here are the {k} test sets you need to judge:
{test_sets_desc}
- All query answers are guaranteed to be consistent
- Answer format must strictly follow the requirements, otherwise it is considered a failure
"""

    tags = ["answer", "query_independence", "query_edge", "query_count"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "k": 2,
                "rule_type": "parity_sum",  # (i+j) % 2 == 1
                "test_sets": [
                    [1, 3, 5],      
                    [2, 3, 4],      
                ]
            },
            2: {
                "n": 8,
                "k": 3,
                "rule_type": "close_distance",  # |i-j| <= 2
                "test_sets": [
                    [1, 4, 7],      
                    [2, 3, 5],      
                    [1, 5, 8],      
                ]
            },
            3: {
                "n": 10,
                "k": 3,
                "rule_type": "gcd_greater_1",  # gcd(i,j) > 1
                "test_sets": [
                    [1, 3, 5, 7],   
                    [2, 4, 8],      
                    [1, 2, 5],      
                ]
            },
            4: {
                "n": 12,
                "k": 4,
                "rule_type": "mod3_product",  
                "test_sets": [
                    [1, 2, 4, 5],   
                    [3, 6, 9],      
                    [1, 4, 7, 10],  
                    [2, 5, 6],      
                ]
            },
            5: {
                "n": 15,
                "k": 5,
                "rule_type": "xor_odd_bits",  # popcount(i XOR j) % 2 == 1
                "test_sets": [
                    [1, 2, 4, 8],   
                    [3, 5, 6],      
                    [1, 3, 7],      
                    [2, 8, 10],     
                    [4, 5, 12, 13], 
                ]
            },
        },
        "en": {
            1: {
                "n": 6,
                "k": 2,
                "rule_type": "parity_sum",
                "test_sets": [
                    [1, 3, 5],
                    [2, 3, 4],
                ]
            },
            2: {
                "n": 8,
                "k": 3,
                "rule_type": "close_distance",
                "test_sets": [
                    [1, 4, 7],
                    [2, 3, 5],
                    [1, 5, 8],
                ]
            },
            3: {
                "n": 10,
                "k": 3,
                "rule_type": "gcd_greater_1",
                "test_sets": [
                    [1, 3, 5, 7],
                    [2, 4, 8],
                    [1, 2, 5],
                ]
            },
            4: {
                "n": 12,
                "k": 4,
                "rule_type": "mod3_product",
                "test_sets": [
                    [1, 2, 4, 5],
                    [3, 6, 9],
                    [1, 4, 7, 10],
                    [2, 5, 6],
                ]
            },
            5: {
                "n": 15,
                "k": 5,
                "rule_type": "xor_odd_bits",
                "test_sets": [
                    [1, 2, 4, 8],
                    [3, 5, 6],
                    [1, 3, 7],
                    [2, 8, 10],
                    [4, 5, 12, 13],
                ]
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 查询计数器
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置和规则"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]
        
        self.n = cfg["n"]
        self.k = cfg["k"]
        self.rule_type = cfg["rule_type"]
        self.test_sets = cfg["test_sets"]
        
        # 构建测试集描述，直接放入规则中
        test_sets_desc_lines = []
        for idx, ts in enumerate(self.test_sets, 1):
            if lang == "zh":
                test_sets_desc_lines.append(f"  测试集 {idx}: {{{','.join(map(str, ts))}}}")
            else:
                test_sets_desc_lines.append(f"  Test set {idx}: {{{','.join(map(str, ts))}}}")
        self._game_info["test_sets_desc"] = "\n".join(test_sets_desc_lines)
        
        # 预计算所有边的关系（Ground Truth）
        self.edges = set()
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                if self._has_edge(i, j):
                    self.edges.add((i, j))

    def _has_edge(self, i, j):
        """判断 i 和 j 之间是否有边（根据规则类型）"""
        if i > j:
            i, j = j, i
        
        if self.rule_type == "parity_sum":
            # (i+j) 是奇数时有边
            return (i + j) % 2 == 1
        
        elif self.rule_type == "close_distance":
            # |i-j| <= 2 时有边
            return abs(i - j) <= 2
        
        elif self.rule_type == "gcd_greater_1":
            # gcd(i,j) > 1 时有边
            from math import gcd
            return gcd(i, j) > 1
        
        elif self.rule_type == "mod3_product":
            # i 和 j 中至少有一个是3的倍数时有边
            return (i % 3 == 0) or (j % 3 == 0)
        
        elif self.rule_type == "xor_odd_bits":
            # (i XOR j) 的二进制中1的个数为奇数时有边
            xor_val = i ^ j
            bit_count = bin(xor_val).count('1')
            return bit_count % 2 == 1
        
        return False

    def _is_independent_set(self, subset):
        """判断子集是否为独立集"""
        subset_list = sorted(subset)
        for i in range(len(subset_list)):
            for j in range(i + 1, len(subset_list)):
                if (subset_list[i], subset_list[j]) in self.edges:
                    return False, (subset_list[i], subset_list[j])
        return True, None

    def _count_edges_in_subset(self, subset):
        """计算子集内边的数量"""
        count = 0
        subset_list = sorted(subset)
        for i in range(len(subset_list)):
            for j in range(i + 1, len(subset_list)):
                if (subset_list[i], subset_list[j]) in self.edges:
                    count += 1
        return count

    def evaluate(self, parsed_info):
        """评估最终答案"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析答案格式：1:yes,2:no,3:yes
        try:
            judgments = {}
            for item in raw_ans.split(","):
                item = item.strip()
                idx_str, result = item.split(":")
                idx = int(idx_str)
                result = result.strip().lower()
                if result not in ["yes", "no"]:
                    return False
                judgments[idx] = (result == "yes")
            
            # 检查是否有k个判断
            if len(judgments) != self.k:
                return False
            
            # 检查每个测试集的判断是否正确
            for idx in range(1, self.k + 1):
                if idx not in judgments:
                    return False
                
                test_set = self.test_sets[idx - 1]
                is_indep, _ = self._is_independent_set(test_set)
                
                if judgments[idx] != is_indep:
                    return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        self.query_count += 1
        
        if self.config.language == "zh":
            indep_yes = "独立"
            indep_no_prefix = "非独立，证人对："
            edge_yes = "存在边"
            edge_no = "无边"
            err_format = "错误：格式无效"
            err_range = "错误：数字超出范围"
        else:
            indep_yes = "Independent"
            indep_no_prefix = "Not Independent, witness pair: "
            edge_yes = "Edge exists"
            edge_no = "No edge"
            err_format = "Error: Invalid format"
            err_range = "Error: Number out of range"

        try:
            # 子集独立性查询
            if "query_independence" in parsed_info:
                raw = parsed_info["query_independence"].strip()
                if not raw:  # 空查询
                    return err_format
                
                nums = [int(x.strip()) for x in raw.split(",")]
                # 验证范围
                for num in nums:
                    if num < 1 or num > self.n:
                        return err_range
                
                # 去重并排序
                subset = sorted(set(nums))
                is_indep, witness = self._is_independent_set(subset)
                
                if is_indep:
                    return indep_yes
                else:
                    return f"{indep_no_prefix}({witness[0]},{witness[1]})"
            
            # 边存在性查询
            elif "query_edge" in parsed_info:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return err_format
                
                i, j = int(parts[0]), int(parts[1])
                if i < 1 or i > self.n or j < 1 or j > self.n:
                    return err_range
                if i >= j:
                    return err_format
                
                if (i, j) in self.edges:
                    return edge_yes
                else:
                    return edge_no
            
            # 边计数查询
            elif "query_count" in parsed_info:
                raw = parsed_info["query_count"].strip()
                if not raw:  # 空查询
                    return err_format
                
                nums = [int(x.strip()) for x in raw.split(",")]
                for num in nums:
                    if num < 1 or num > self.n:
                        return err_range
                
                subset = set(nums)
                count = self._count_edges_in_subset(subset)
                return str(count)
            
            else:
                return err_format
                
        except Exception as e:
            return err_format

    def _cf_make_wrong(self, correct):
        """生成一个与正确答案相反/不同的错误答案"""
        if correct.isdigit():
            val = int(correct)
            return str(val + 1)
        
        if self.config.language == "zh":
            if correct == "独立":
                return "非独立，证人对：(1,2)"
            if correct.startswith("非独立"):
                return "独立"
            if correct == "存在边":
                return "无边"
            if correct == "无边":
                return "存在边"
        else:
            if correct == "Independent":
                return "Not Independent, witness pair: (1,2)"
            if correct.startswith("Not Independent"):
                return "Independent"
            if correct == "Edge exists":
                return "No edge"
            if correct == "No edge":
                return "Edge exists"
        
        return correct + " [WRONG]"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        为避免指数爆炸和上下文溢出，限制总查询数。
        """
        queries = []
        
        if self.config.language == "zh":
            indep_yes = "独立"
            indep_no_prefix = "非独立，证人对："
            edge_yes = "存在边"
            edge_no = "无边"
        else:
            indep_yes = "Independent"
            indep_no_prefix = "Not Independent, witness pair: "
            edge_yes = "Edge exists"
            edge_no = "No edge"

        # 1. 边存在性查询
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                query_str = f"<query_edge>{i},{j}</query_edge>"
                if (i, j) in self.edges:
                    ans = edge_yes
                else:
                    ans = edge_no
                queries.append({"query": query_str, "answer": ans})

        # 2. 子集查询 — 限制子集大小以避免指数爆炸
        max_subset_size = min(self.n, 3)  # 从4降到3以减少查询量
        for r in range(2, max_subset_size + 1):
            for subset_tuple in itertools.combinations(range(1, self.n + 1), r):
                subset = sorted(subset_tuple)
                subset_str = ",".join(map(str, subset))
                
                # 子集独立性查询
                is_indep, witness = self._is_independent_set(subset)
                if is_indep:
                    indep_ans = indep_yes
                else:
                    indep_ans = f"{indep_no_prefix}({witness[0]},{witness[1]})"
                
                queries.append({
                    "query": f"<query_independence>{subset_str}</query_independence>",
                    "answer": indep_ans
                })
                
                # 边计数查询
                count = self._count_edges_in_subset(subset)
                queries.append({
                    "query": f"<query_count>{subset_str}</query_count>",
                    "answer": str(count)
                })

        return queries