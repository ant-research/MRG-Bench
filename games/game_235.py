from .base import Game
import random

class TreeOrderRankGame(Game):

    game_rule_zh = """\
我们来玩一个"树序推理"游戏，规则如下：

游戏设定了一棵有根且子节点有固定左右次序的有序树。节点总数为 {n}，节点编号为 1 到 {n}。树已经给定了根节点以及每个节点的有序子节点列表。

我已经使用某个确定性规则对这棵树的所有节点生成了一个固定的全序排列 O（即对所有节点的一个排列顺序）。该排列在整个游戏过程中保持不变，没有任何随机性。但这个生成规则对你起初是不可见的。

你的目标是：在本轮中，系统会给定一个目标节点 T，你需要确定该节点 T 在隐藏全序 O 中的名次（即它是第几个节点，名次范围为 1 到 {n}）。

你可以使用以下查询来获取信息（每次只能进行一个查询）：

1. **比较查询**：询问节点 A 和节点 B 哪个在全序 O 中更早出现（A 和 B 必须不同）。我会回答"A earlier than B"或"B earlier than A"。

2. **名次验证查询**：询问节点 X 是否恰好是全序中的第 k 位。我会回答"Yes"或"No"。

当你准备好后，请提交目标节点的名次作为最终答案。注意：
- 你应当尽可能少地使用查询次数。
- 每轮只能提交一次答案。
- 如果答案错误或查询次数超出限制，游戏失败。

根节点：{root}

每个节点的子节点列表（按左到右顺序）：
{tree_structure}

目标节点：{target}

每次只能包含一个查询标签。请使用以下 XML 格式：

- 比较查询（例如比较节点 1 和节点 3）：
<query_compare>1,3</query_compare>

- 名次验证查询（例如验证节点 5 是否是第 2 位）：
<query_is_k>5,2</query_is_k>

提交最终答案时，给出目标节点的名次（一个整数），格式如下：

<answer>3</answer>
"""

    game_rule_en = """\
Let's play a "Tree Order Ranking" game. Here are the rules:

The game uses a rooted ordered tree where child nodes have a fixed left-to-right order. There are {n} nodes in total, numbered from 1 to {n}. The tree has a given root node and each node has an ordered list of child nodes.

I have generated a fixed total order O of all nodes in this tree using a deterministic rule. This order remains constant throughout the game with no randomness. However, the generation rule is initially hidden from you.

Your goal is: In this round, the system will specify a target node T, and you need to determine the rank of node T in the hidden total order O (i.e., its position in the order, ranging from 1 to {n}).

You can use the following queries to gather information (one query at a time):

1. **Compare Query**: Ask which of two different nodes A and B appears earlier in the total order O. I will answer "A earlier than B" or "B earlier than A".

2. **Rank Verification Query**: Ask whether node X is exactly at position k in the total order. I will answer "Yes" or "No".

When ready, submit the rank of the target node as your final answer. Note:
- You should use as few queries as possible.
- You can only submit one answer per round.
- If your answer is incorrect or you exceed the query limit, the game fails.

Root node: {root}

Child node lists for each node (in left-to-right order):
{tree_structure}

Target node: {target}

Each query must contain only one tag. Use the following XML format:

- Compare Query (e.g., comparing nodes 1 and 3):
<query_compare>1,3</query_compare>

- Rank Verification Query (e.g., verifying if node 5 is at position 2):
<query_is_k>5,2</query_is_k>

When submitting the final answer, provide the rank of the target node (an integer) in this format:

<answer>3</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通巡检系统正在对城市路网进行排查，规则如下：

系统管辖着一个呈有序树状拓扑结构的交通监控网络。站点总数为 {n}，编号为 1 到 {n}。树的根节点是主控中心，每个站点都有其固定的下级监控子站点列表（按从左到右的优先级排序）。

系统已根据某个内部确定性算法，生成了一条固定的无人机全局巡检路线，产生了一个全序排列 O（即对所有站点的巡检先后顺序）。该路线在整个排查期间保持不变，且无任何随机性。但这个调度算法起初对你是保密的。

你的任务是：本轮中，系统会给出一个目标站点 T，你需要推理出该站点 T 在全局巡检路线 O 中的确切顺位（即它是第几个被巡检的，顺位范围为 1 到 {n}）。

你可以使用以下查询指令来获取调度信息（每次只能执行一个查询）：

1. **路线比较查询**：询问站点 A 和站点 B 哪个在巡检路线 O 中更早被访问（A 和 B 必须不同）。系统会回答"A earlier than B"或"B earlier than A"。

2. **顺位验证查询**：询问站点 X 是否恰好是巡检路线中的第 k 站。系统会回答"Yes"或"No"。

当你推理出结果后，请提交目标站点的巡检顺位作为最终答案。注意：
- 你应当尽可能少地占用查询带宽。
- 每轮只能提交一次答案。
- 如果答案错误或查询次数超出系统配额，排查任务失败。

主控中心（根节点）：{root}

各站点的下级监控子站点列表（按优先级顺序）：
{tree_structure}

目标站点：{target}

每次只能包含一个查询标签。请使用以下 XML 格式：

- 路线比较查询（例如比较站点 1 和 3）：
<query_compare>1,3</query_compare>

- 顺位验证查询（例如验证站点 5 是否为第 2 站）：
<query_is_k>5,2</query_is_k>

提交最终答案时，给出目标站点的顺位（一个整数），格式如下：

<answer>3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
An intelligent traffic inspection system is investigating the city's road network under the following rules:

The system manages a traffic monitoring network configured as an ordered tree topology. There are {n} stations in total, numbered from 1 to {n}. The tree has a given root node (the main control center), and each station has an ordered list of subordinate monitoring stations (prioritized from left to right).

The system has generated a fixed global drone inspection route, resulting in a total order O of all stations, based on a deterministic internal algorithm. This route remains constant throughout the investigation with no randomness. However, the scheduling algorithm is initially hidden from you.

Your task is: In this round, the system will specify a target station T, and you must deduce the exact inspection rank of station T in the global route O (i.e., its position in the sequence, ranging from 1 to {n}).

You can use the following queries to gather scheduling information (one query at a time):

1. **Route Compare Query**: Ask which of two different stations A and B is visited earlier in the inspection route O. I will answer "A earlier than B" or "B earlier than A".

2. **Rank Verification Query**: Ask whether station X is exactly the k-th station in the route. I will answer "Yes" or "No".

When you have deduced the result, submit the inspection rank of the target station as your final answer. Note:
- You should use as few queries as possible to save bandwidth.
- You can only submit one answer per round.
- If your answer is incorrect or you exceed the query quota, the investigation fails.

Main Control Center (Root node): {root}

Subordinate monitoring station lists for each station (in priority order):
{tree_structure}

Target station: {target}

Each query must contain only one tag. Use the following XML format:

- Route Compare Query (e.g., comparing stations 1 and 3):
<query_compare>1,3</query_compare>

- Rank Verification Query (e.g., verifying if station 5 is the 2nd stop):
<query_is_k>5,2</query_is_k>

When submitting the final answer, provide the rank of the target station (an integer) in this format:

<answer>3</answer>
"""

    contextualized_rule_zh_2 = """\
医疗AI助手正在执行病区查房规划，规则如下：

系统管理着一个呈有序树状结构的病区科室分布图。科室总数为 {n}，编号为 1 到 {n}。树结构给定了一个主治病区作为根节点，并且每个科室都有其固定的下辖子科室列表（按从左到右的空间流线顺序排列）。

医疗系统已通过特定的临床确定性规则，为医疗机器人生成了一套固定的全局查房顺序 O（即对所有科室的访问全序排列）。该顺序在整个查房周期内保持不变，不含随机性。但生成规则对你起初是隐藏的。

你的目标是：在本轮中，系统会指定一个目标科室 T，你需要确定该科室 T 在全局查房顺序 O 中的具体名次（即它是第几个被查房的，范围为 1 到 {n}）。

你可以使用以下指令来查询查房记录（每次只能进行一个查询）：

1. **查房先后查询**：询问科室 A 和科室 B 哪个在查房顺序 O 中更早被访问（A 和 B 必须不同）。系统会回答"A earlier than B"或"B earlier than A"。

2. **查房轮次验证查询**：询问科室 X 是否恰好是全局查房的第 k 站。系统会回答"Yes"或"No"。

当你得出结论后，请提交目标科室的查房名次作为最终答案。注意：
- 你应当尽可能少地调用查询接口。
- 每轮只能提交一次答案。
- 如果答案错误或查询次数超限，查房规划验证失败。

主治病区（根节点）：{root}

每个科室的下辖子科室列表（按空间流线顺序）：
{tree_structure}

目标科室：{target}

每次只能包含一个查询标签。请使用以下 XML 格式：

- 查房先后查询（例如比较科室 1 和 3）：
<query_compare>1,3</query_compare>

- 查房轮次验证查询（例如验证科室 5 是否是第 2 站）：
<query_is_k>5,2</query_is_k>

提交最终答案时，给出目标科室的名次（一个整数），格式如下：

<answer>3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
A Medical AI Assistant is planning ward rounds under the following rules:

The system manages a ward and department layout configured as an ordered tree. There are {n} departments in total, numbered from 1 to {n}. The tree specifies a primary ward as the root node, and each department has an ordered list of subordinate sub-departments (arranged from left to right following spatial flow).

The medical system has generated a fixed global round order O (a total order of visits to all departments) for the medical robot using a deterministic clinical rule. This order remains constant throughout the round cycle with no randomness. However, the generation rule is initially hidden from you.

Your goal is: In this round, the system will specify a target department T, and you need to determine the exact rank of department T in the global round order O (i.e., its position in the sequence, ranging from 1 to {n}).

You can use the following queries to check the round logs (one query at a time):

1. **Round Compare Query**: Ask which of two different departments A and B is visited earlier in the round order O. I will answer "A earlier than B" or "B earlier than A".

2. **Round Rank Verification Query**: Ask whether department X is exactly the k-th stop in the global round. I will answer "Yes" or "No".

When you have deduced the result, submit the rank of the target department as your final answer. Note:
- You should use as few queries as possible.
- You can only submit one answer per round.
- If your answer is incorrect or you exceed the query limit, the round planning validation fails.

Primary Ward (Root node): {root}

Subordinate sub-department lists for each department (in spatial flow order):
{tree_structure}

Target department: {target}

Each query must contain only one tag. Use the following XML format:

- Round Compare Query (e.g., comparing departments 1 and 3):
<query_compare>1,3</query_compare>

- Round Rank Verification Query (e.g., verifying if department 5 is the 2nd stop):
<query_is_k>5,2</query_is_k>

When submitting the final answer, provide the rank of the target department (an integer) in this format:

<answer>3</answer>
"""

    contextualized_rule_zh_3 = """\
智能教学大纲排课系统正在规划课程讲授顺序，规则如下：

一门课程的知识点构成了一棵有序的先修关系树。知识点总数为 {n}，编号为 1 到 {n}。树中给定了基础核心知识点作为根节点，且每个知识点都有其固定的后续延伸知识点列表（按从左到右的教学逻辑排列）。

系统已经使用某种确定性的教育学法则，为所有知识点生成了一个固定的教学绝对顺序 O（即一个全序排列）。该讲授顺序在整个学期内保持不变，没有任何随机性。但这个排课法则起初对你是不公开的。

你的目标是：本轮中，系统会指定一个目标知识点 T，你需要推理出该知识点 T 在全局教学顺序 O 中的课时顺位（即它是第几个被讲授的，顺位范围为 1 到 {n}）。

你可以使用以下查询来获取排课信息（每次只能进行一个查询）：

1. **讲授先后查询**：询问知识点 A 和知识点 B 哪个在教学顺序 O 中更早讲授（A 和 B 必须不同）。系统会回答"A earlier than B"或"B earlier than A"。

2. **课时顺位验证查询**：询问知识点 X 是否恰好安排在第 k 个顺位讲授。系统会回答"Yes"或"No"。

准备就绪后，请提交目标知识点的课时顺位作为最终答案。注意：
- 你应当尽量减少对排课系统的查询次数。
- 每轮只能提交一次排课答案。
- 如果顺位错误或查询次数超限，大纲规划即告失败。

核心知识点（根节点）：{root}

每个知识点的后续延伸知识点列表（按教学逻辑顺序）：
{tree_structure}

目标知识点：{target}

每次只能包含一个查询标签。请使用以下 XML 格式：

- 讲授先后查询（例如比较知识点 1 和 3）：
<query_compare>1,3</query_compare>

- 课时顺位验证查询（例如验证知识点 5 是否为第 2 顺位）：
<query_is_k>5,2</query_is_k>

提交最终答案时，给出目标知识点的课时顺位（一个整数），格式如下：

<answer>3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
An intelligent syllabus scheduling system is planning the teaching sequence under the following rules:

The knowledge points of a course form an ordered prerequisite relationship tree. There are {n} knowledge points in total, numbered from 1 to {n}. The tree defines a core foundational point as the root node, and each knowledge point has an ordered list of subsequent extension points (arranged from left to right following pedagogical logic).

The system has generated a fixed absolute teaching sequence O (a total order) for all knowledge points using a deterministic educational algorithm. This teaching sequence remains constant throughout the semester with no randomness. However, the scheduling algorithm is initially unrevealed to you.

Your goal is: In this round, the system will specify a target knowledge point T, and you must deduce the exact lesson rank of point T in the global teaching sequence O (i.e., its position in the schedule, ranging from 1 to {n}).

You can use the following queries to gather scheduling information (one query at a time):

1. **Teaching Sequence Compare Query**: Ask which of two different knowledge points A and B is taught earlier in the sequence O. I will answer "A earlier than B" or "B earlier than A".

2. **Lesson Rank Verification Query**: Ask whether knowledge point X is scheduled exactly at the k-th position. I will answer "Yes" or "No".

When ready, submit the lesson rank of the target knowledge point as your final answer. Note:
- You should minimize your queries to the scheduling system.
- You can only submit one schedule answer per round.
- If your rank is incorrect or you exceed the query limit, the syllabus planning fails.

Core foundational point (Root node): {root}

Subsequent extension point lists for each knowledge point (in pedagogical logic order):
{tree_structure}

Target knowledge point: {target}

Each query must contain only one tag. Use the following XML format:

- Teaching Sequence Compare Query (e.g., comparing points 1 and 3):
<query_compare>1,3</query_compare>

- Lesson Rank Verification Query (e.g., verifying if point 5 is at position 2):
<query_is_k>5,2</query_is_k>

When submitting the final answer, provide the lesson rank of the target knowledge point (an integer) in this format:

<answer>3</answer>
"""

    contextualized_rule_zh_4 = """\
自动化产线的质检追溯系统正在校验装配流程，规则如下：

一条复杂产品的生产线被建模为一棵有序的装配依赖树。工位总数为 {n}，编号为 1 到 {n}。树结构中，总装工位是根节点，每个工位都有其依赖的前置子装配工位列表（按从左到右的工艺优先级排列）。

系统已内置了某种确定性的工艺审查规则，对所有工位生成了一个固定的全局质检序列 O（即一个全序排列）。该序列在整个批次生产过程中严格保持不变，杜绝任何随机干扰。但该审查规则的底层逻辑起初是未知的。

你的任务是：本轮中，系统会圈定一个目标工位 T，你需要推导出该工位 T 在全局质检序列 O 中的确切批次位次（即它是第几个被质检的，位次范围为 1 到 {n}）。

你可以利用以下指令来调取质检日志（每次只能下达一个指令）：

1. **质检时序比较**：询问工位 A 和工位 B 哪个在质检序列 O 中更早执行（A 和 B 必须不同）。系统会返回"A earlier than B"或"B earlier than A"。

2. **位次校验指令**：询问工位 X 是否恰好处于质检序列的第 k 位。系统会返回"Yes"或"No"。

分析完毕后，请提交目标工位的质检位次作为最终确认。注意：
- 你应尽力优化指令调用次数以降低系统开销。
- 每轮仅允许提交一次核对结果。
- 如果位次核对失败或调用次数溢出，流水线校验报错。

总装工位（根节点）：{root}

各工位的子装配工位列表（按工艺优先级顺序）：
{tree_structure}

目标工位：{target}

每次只能包含一个查询标签。请使用以下 XML 格式：

- 质检时序比较（例如比较工位 1 和 3）：
<query_compare>1,3</query_compare>

- 位次校验指令（例如验证工位 5 是否为第 2 位）：
<query_is_k>5,2</query_is_k>

提交最终答案时，给出目标工位的质检位次（一个整数），格式如下：

<answer>3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
An automated production line's quality inspection traceability system is verifying the assembly process under the following rules:

The production line of a complex product is modeled as an ordered assembly dependency tree. There are {n} stations in total, numbered from 1 to {n}. In the tree structure, the final assembly station is the root node, and each station has an ordered list of prerequisite sub-assembly stations (arranged from left to right by process priority).

The system has built in a deterministic process review rule, generating a fixed global inspection sequence O (a total order) for all stations. This sequence remains strictly constant throughout the batch production, preventing any random interference. However, the underlying logic of this review rule is initially unknown to you.

Your task is: In this round, the system will highlight a target station T, and you must deduce the exact batch rank of station T in the global inspection sequence O (i.e., its position in the sequence, ranging from 1 to {n}).

You can use the following commands to fetch inspection logs (one command at a time):

1. **Inspection Timing Compare**: Ask which of two different stations A and B is executed earlier in the inspection sequence O. I will return "A earlier than B" or "B earlier than A".

2. **Rank Validation Command**: Ask whether station X is exactly at the k-th position in the inspection sequence. I will return "Yes" or "No".

Upon completing the analysis, submit the inspection rank of the target station as your final confirmation. Note:
- You should optimize your command calls to reduce system overhead.
- Only one verification result can be submitted per round.
- If the rank verification fails or call limit is exceeded, the pipeline validation throws an error.

Final Assembly Station (Root node): {root}

Sub-assembly station lists for each station (in process priority order):
{tree_structure}

Target station: {target}

Each query must contain only one tag. Use the following XML format:

- Inspection Timing Compare (e.g., comparing stations 1 and 3):
<query_compare>1,3</query_compare>

- Rank Validation Command (e.g., verifying if station 5 is at position 2):
<query_is_k>5,2</query_is_k>

When submitting the final answer, provide the inspection rank of the target station (an integer) in this format:

<answer>3</answer>
"""

    contextualized_rule_zh_5 = """\
司法证据链审查系统正在进行案卷逻辑推演，规则如下：

案件的证据条目构成了一棵有序的法律逻辑推理树。证据条目总数为 {n}，编号为 1 到 {n}。树结构给定了一项核心指控作为根节点，每项证据都有其固定的支撑性附属证据列表（按从左到右的法理审查优先级排列）。

审查委员会已依据特定的确定性法定程序，为所有证据条目生成了一个固定的全局审查序列 O（即对所有证据的一个全序排列）。该审查序列在整个庭审推演中保持不变，不存在任何自由裁量引发的随机性。但该法定生成规则对你起初是保密的。

你的目标是：在本轮中，系统会提供一项目标证据 T，你需要确定该证据 T 在全局审查序列 O 中的准确位次（即它是第几个被审查的，位次范围为 1 到 {n}）。

你可以通过以下质询来获取审查进程信息（每次只能提出一个质询）：

1. **审查时序质询**：询问证据 A 和证据 B 哪个在审查序列 O 中更早进入审查环节（A 和 B 必须不同）。系统会回答"A earlier than B"或"B earlier than A"。

2. **环节位次验证**：询问证据 X 是否恰好是审查序列中的第 k 项。系统会回答"Yes"或"No"。

质证完毕后，请提交目标证据的审查位次作为最终结论。注意：
- 你应当尽量精简质询次数，提高诉讼效率。
- 每轮只能提交一次结论。
- 如果审查位次判定错误或质询次数超过法定限制，逻辑推演驳回。

核心指控（根节点）：{root}

每项证据的附属证据列表（按法理审查优先级）：
{tree_structure}

目标证据：{target}

每次只能包含一个查询标签。请使用以下 XML 格式：

- 审查时序质询（例如比较证据 1 和 3）：
<query_compare>1,3</query_compare>

- 环节位次验证（例如验证证据 5 是否为第 2 项）：
<query_is_k>5,2</query_is_k>

提交最终答案时，给出目标证据的审查位次（一个整数），格式如下：

<answer>3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The Judicial Evidence Chain Review System is conducting case logic deduction under the following rules:

The evidence items of a case form an ordered legal logic deduction tree. There are {n} evidence items in total, numbered from 1 to {n}. The tree establishes a core allegation as the root node, and each evidence item has a fixed list of supporting subsidiary evidence (arranged from left to right by jurisprudential review priority).

The review committee has generated a fixed global review sequence O (a total order for all evidence) based on a deterministic statutory procedure. This review sequence remains strictly constant throughout the trial deduction, with no randomness caused by discretionary powers. However, the statutory generation rule is initially confidential to you.

Your goal is: In this round, the system will provide a target evidence item T, and you need to determine the precise rank of evidence T in the global review sequence O (i.e., its position in the review process, ranging from 1 to {n}).

You can use the following inquiries to gather review process information (one inquiry at a time):

1. **Review Timing Inquiry**: Ask which of two different evidence items A and B enters the review phase earlier in sequence O. I will answer "A earlier than B" or "B earlier than A".

2. **Phase Rank Verification**: Ask whether evidence X is exactly the k-th item in the review sequence. I will answer "Yes" or "No".

Upon completing the cross-examination, submit the review rank of the target evidence as your final conclusion. Note:
- You should streamline your inquiries to improve litigation efficiency.
- You can only submit one conclusion per round.
- If the review rank judgment is incorrect or inquiries exceed the statutory limit, the logic deduction is dismissed.

Core Allegation (Root node): {root}

Subsidiary evidence lists for each item (in jurisprudential review priority):
{tree_structure}

Target evidence: {target}

Each query must contain only one tag. Use the following XML format:

- Review Timing Inquiry (e.g., comparing evidence 1 and 3):
<query_compare>1,3</query_compare>

- Phase Rank Verification (e.g., verifying if evidence 5 is the 2nd item):
<query_is_k>5,2</query_is_k>

When submitting the final answer, provide the review rank of the target evidence (an integer) in this format:

<answer>3</answer>
"""

    tags = ["answer", "query_compare", "query_is_k"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "root": 1,
                "children": {
                    1: [2, 3],
                    2: [4],
                    3: [5],
                    4: [],
                    5: []
                },
                "target": 1,
                "max_queries": 6
            },
            2: {
                "n": 7,
                "root": 1,
                "children": {
                    1: [2, 3],
                    2: [4, 5],
                    3: [6, 7],
                    4: [],
                    5: [],
                    6: [],
                    7: []
                },
                "target": 5,
                "max_queries": 7
            },
            3: {
                "n": 10,
                "root": 1,
                "children": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7],
                    4: [8, 9],
                    5: [],
                    6: [10],
                    7: [],
                    8: [],
                    9: [],
                    10: []
                },
                "target": 10,
                "max_queries": 8
            },
            4: {
                "n": 12,
                "root": 1,
                "children": {
                    1: [2, 3],
                    2: [4, 5, 6],
                    3: [7, 8],
                    4: [9],
                    5: [],
                    6: [10],
                    7: [11],
                    8: [12],
                    9: [],
                    10: [],
                    11: [],
                    12: []
                },
                "target": 11,
                "max_queries": 9
            },
            5: {
                "n": 15,
                "root": 1,
                "children": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7, 8, 9],
                    4: [10],
                    5: [11],
                    6: [12],
                    7: [],
                    8: [13, 14],
                    9: [],
                    10: [15],
                    11: [],
                    12: [],
                    13: [],
                    14: [],
                    15: []
                },
                "target": 13,
                "max_queries": 10
            }
        },
        "en": {
            1: {
                "n": 5,
                "root": 1,
                "children": {
                    1: [2, 3],
                    2: [4],
                    3: [5],
                    4: [],
                    5: []
                },
                "target": 1,
                "max_queries": 6
            },
            2: {
                "n": 7,
                "root": 1,
                "children": {
                    1: [2, 3],
                    2: [4, 5],
                    3: [6, 7],
                    4: [],
                    5: [],
                    6: [],
                    7: []
                },
                "target": 5,
                "max_queries": 7
            },
            3: {
                "n": 10,
                "root": 1,
                "children": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7],
                    4: [8, 9],
                    5: [],
                    6: [10],
                    7: [],
                    8: [],
                    9: [],
                    10: []
                },
                "target": 10,
                "max_queries": 8
            },
            4: {
                "n": 12,
                "root": 1,
                "children": {
                    1: [2, 3],
                    2: [4, 5, 6],
                    3: [7, 8],
                    4: [9],
                    5: [],
                    6: [10],
                    7: [11],
                    8: [12],
                    9: [],
                    10: [],
                    11: [],
                    12: []
                },
                "target": 11,
                "max_queries": 9
            },
            5: {
                "n": 15,
                "root": 1,
                "children": {
                    1: [2, 3, 4],
                    2: [5, 6],
                    3: [7, 8, 9],
                    4: [10],
                    5: [11],
                    6: [12],
                    7: [],
                    8: [13, 14],
                    9: [],
                    10: [15],
                    11: [],
                    12: [],
                    13: [],
                    14: [],
                    15: []
                },
                "target": 13,
                "max_queries": 10
            }
        }
    }

    def __init__(self, config):
        self.query_count = 0
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
        self._game_info["root"] = cfg["root"]
        self.children = cfg["children"]
        self.max_queries = cfg["max_queries"]
        
        self.target = cfg["target"]
        
        tree_lines = []
        for node in sorted(self.children.keys()):
            if self.children[node]:
                children_str = ", ".join(map(str, self.children[node]))
                tree_lines.append(f"Node {node}: [{children_str}]" if lang == "en" else f"节点 {node}：[{children_str}]")
            else:
                tree_lines.append(f"Node {node}: []" if lang == "en" else f"节点 {node}：[]")
        
        self._game_info["tree_structure"] = "\n".join(tree_lines)
        self._game_info["target"] = self.target
        
        self.preorder = []
        self._preorder_traverse(cfg["root"])
        self.node_to_rank = {node: idx + 1 for idx, node in enumerate(self.preorder)}

    def _preorder_traverse(self, node):
        self.preorder.append(node)
        for child in self.children[node]:
            self._preorder_traverse(child)

    def evaluate(self, parsed_info):
        try:
            submitted_rank = int(parsed_info["answer"].strip())
            correct_rank = self.node_to_rank[self.target]
            return submitted_rank == correct_rank
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "Yes", "No"
            earlier_template = "{} earlier than {}"
        else:
            yes_res, no_res = "Yes", "No"
            earlier_template = "{} earlier than {}"

        query_tags_present = [tag for tag in ["query_compare", "query_is_k"] if tag in parsed_info]
        if len(query_tags_present) > 1:
            return ("Error: Only one query per turn is allowed." 
                    if self.config.language == "en" 
                    else "错误：每次只能进行一个查询。")

        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Expected exactly 2 parts")
                node_a, node_b = int(parts[0]), int(parts[1])
                
                if node_a == node_b:
                    return "Error: Nodes must be different." if self.config.language == "en" else "错误：节点必须不同。"
                if node_a not in self.node_to_rank or node_b not in self.node_to_rank:
                    return "Error: Invalid node ID." if self.config.language == "en" else "错误：无效的节点编号。"
                
                if self.query_count + 1 > self.max_queries:
                    raise ValueError(
                        f"Query limit exceeded ({self.max_queries} queries allowed)." 
                        if self.config.language == "en" 
                        else f"查询次数超限（最多允许 {self.max_queries} 次查询）。"
                    )
                self.query_count += 1

                rank_a = self.node_to_rank[node_a]
                rank_b = self.node_to_rank[node_b]
                
                if rank_a < rank_b:
                    return earlier_template.format(node_a, node_b)
                else:
                    return earlier_template.format(node_b, node_a)
            except (ValueError, IndexError) as e:
                if "Query limit exceeded" in str(e) or "查询次数超限" in str(e):
                    raise e
                return "Error: Invalid compare query format." if self.config.language == "en" else "错误：比较查询格式无效。"

        elif "query_is_k" in parsed_info:
            try:
                raw = parsed_info["query_is_k"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError("Expected exactly 2 parts")
                node_x, k = int(parts[0]), int(parts[1])
                
                if node_x not in self.node_to_rank:
                    return "Error: Invalid node ID." if self.config.language == "en" else "错误：无效的节点编号。"
                if k < 1 or k > self._game_info["n"]:
                    return "Error: Rank out of range." if self.config.language == "en" else "错误：名次超出范围。"
                
                if self.query_count + 1 > self.max_queries:
                    raise ValueError(
                        f"Query limit exceeded ({self.max_queries} queries allowed)." 
                        if self.config.language == "en" 
                        else f"查询次数超限（最多允许 {self.max_queries} 次查询）。"
                    )
                self.query_count += 1

                actual_rank = self.node_to_rank[node_x]
                return yes_res if actual_rank == k else no_res
            except (ValueError, IndexError) as e:
                if "Query limit exceeded" in str(e) or "查询次数超限" in str(e):
                    raise e
                return "Error: Invalid rank verification query format." if self.config.language == "en" else "错误：名次验证查询格式无效。"

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        n = self._game_info["n"]
        node_to_rank = self.node_to_rank
        
        earlier_template = "{} earlier than {}"
        yes_res = "Yes"
        no_res = "No"

        for a in range(1, n + 1):
            for b in range(a + 1, n + 1):
                query_str = f"<query_compare>{a},{b}</query_compare>"
                
                rank_a = node_to_rank[a]
                rank_b = node_to_rank[b]
                
                if rank_a < rank_b:
                    ans = earlier_template.format(a, b)
                else:
                    ans = earlier_template.format(b, a)
                
                queries.append({
                    "query": query_str,
                    "answer": ans
                })

        for x in range(1, n + 1):
            for k in range(1, n + 1):
                query_str = f"<query_is_k>{x},{k}</query_is_k>"
                
                actual_rank = node_to_rank[x]
                ans = yes_res if actual_rank == k else no_res
                
                queries.append({
                    "query": query_str,
                    "answer": ans
                })

        return queries

    def _cf_make_wrong(self, correct):
        import re as _re
        
        m = _re.match(r'^(\S+)\s+earlier\s+than\s+(\S+)$', correct)
        if m:
            return f"{m.group(2)} earlier than {m.group(1)}"
        
        if correct.isdigit():
            return str(int(correct) + 1)
        
        low = correct.lower()
        if low == "yes":
            return "No"
        if low == "no":
            return "Yes"

        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")

        return correct + "_WRONG"

