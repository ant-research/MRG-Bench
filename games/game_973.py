# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   遍历相对顺序：两个节点在某种遍历下谁先被访问
# ============================================================

from .base import Game


class BinaryTreeTraversalGame(Game):

    game_rule_zh = """\
我们现在来玩一个"二叉树遍历推理"游戏，规则如下：

游戏设定了一棵固定的有根二叉树，节点集合为 {{A, B, C, D, E, F, G, H, I}}，结构如下：
- 根节点：A
- A 的左子节点：B；右子节点：C
- B 的左子节点：D；右子节点：E
- C 的左子节点：F；右子节点：G
- E 的左子节点：H；右子节点：I
- 其他未列出的子节点为空

我已秘密选择了一种遍历规则（先序、中序、后序或层序遍历），并将这棵树按该规则遍历，得到一个节点的全排列序列。

你的目标是通过询问推断出：
1. 我选择的遍历规则是哪一种
2. 在该遍历序列中第 {k} 个位置的节点是什么

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 先后比较：询问在遍历序列中，节点 X 与节点 Y 谁更靠前。我会回答节点名称。
2. 相邻查询：询问在遍历序列中，节点 X 是否紧挨在节点 Y 之前（即 X 的位置恰好是 Y 的位置减 1）。我会回答"是"或"否"。

注意：
- 询问中的节点必须属于 {{A, B, C, D, E, F, G, H, I}} 且两个节点不能相同
- 你需要至少进行两次有效询问后才能提交最终答案
- 请用尽可能少的询问次数推断出答案

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 先后比较（例如询问节点 A 和节点 B 谁更靠前）：
<query_order>A,B</query_order>

- 相邻查询（例如询问节点 A 是否紧挨在节点 B 之前）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明遍历规则类型（Preorder、Inorder、Postorder 或 Level-order）并给出第 {k} 个位置的节点，格式如下：

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    game_rule_en = """\
Let's play a "Binary Tree Traversal Inference" game. Here are the rules:

The game uses a fixed rooted binary tree with node set {{A, B, C, D, E, F, G, H, I}}, structured as follows:
- Root: A
- A's left child: B; right child: C
- B's left child: D; right child: E
- C's left child: F; right child: G
- E's left child: H; right child: I
- Other unlisted children are null

I have secretly selected a traversal rule (Preorder, Inorder, Postorder, or Level-order) and traversed this tree according to that rule, obtaining a complete permutation sequence of the nodes.

Your goal is to infer through queries:
1. Which traversal rule I selected
2. What node is at position {k} in that traversal sequence

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Order Comparison: Ask which of nodes X and Y appears earlier in the traversal sequence. I will answer with a node name.
2. Adjacency Query: Ask whether node X immediately precedes node Y in the traversal sequence (i.e., X's position is exactly Y's position minus 1). I will answer "Yes" or "No".

Notes:
- Query nodes must belong to {{A, B, C, D, E, F, G, H, I}} and the two nodes must be different
- You must make at least two valid queries before submitting your final answer
- Please use as few queries as possible to infer the answer

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Order Comparison (e.g., asking which of nodes A and B comes first):
<query_order>A,B</query_order>

- Adjacency Query (e.g., asking if node A immediately precedes node B):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the traversal rule type (Preorder, Inorder, Postorder, or Level-order) and the node at position {k}, using this format:

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    contextualized_rule_zh_1 = """\
我们正在规划一个"交通枢纽巡检路径"推理系统，规则如下：

系统设定了一个固定的干线物流分发网络，枢纽站点集合为 {{A, B, C, D, E, F, G, H, I}}，网络呈二叉树层级结构：
- 总枢纽：A
- A 的左线枢纽：B；右线枢纽：C
- B 的左线枢纽：D；右线枢纽：E
- C 的左线枢纽：F；右线枢纽：G
- E 的左线枢纽：H；右线枢纽：I
- 其他未列出的分支为空

调度中心秘密采取了一种固定的巡检策略（先序 Preorder、中序 Inorder、后序 Postorder 或层序 Level-order），对所有枢纽进行了一次完整巡视，形成了一个站点全排列的巡检序列。

你的目标是通过询问推断出：
1. 调度中心选择的巡检策略是哪一种
2. 在该巡检序列中第 {k} 个位置的枢纽站点是什么

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 先后比较：询问在巡检序列中，站点 X 与站点 Y 哪个更早被巡视。我会回答站点名称。
2. 相邻查询：询问在巡检序列中，站点 X 是否紧挨在站点 Y 之前被巡视（即 X 的访问次序恰好是 Y 的次序减 1）。我会回答"是"或"否"。

注意：
- 询问中的站点必须属于 {{A, B, C, D, E, F, G, H, I}} 且两个站点不能相同
- 你需要至少进行两次有效询问后才能提交最终答案
- 请用尽可能少的询问次数推断出答案

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 先后比较（例如询问站点 A 和站点 B 谁更早）：
<query_order>A,B</query_order>

- 相邻查询（例如询问站点 A 是否紧挨在站点 B 之前）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明巡检策略类型（Preorder、Inorder、Postorder 或 Level-order）并给出第 {k} 个被巡视的站点，格式如下：

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic / Transportation Scenario]
We are planning a "Traffic Hub Inspection Path" inference system. Here are the rules:

The system operates on a fixed trunk logistics distribution network with a hub set {{A, B, C, D, E, F, G, H, I}}, structured as a hierarchical binary tree:
- Main hub: A
- A's left line hub: B; right line hub: C
- B's left line hub: D; right line hub: E
- C's left line hub: F; right line hub: G
- E's left line hub: H; right line hub: I
- Other unlisted branches are null

The dispatch center has secretly adopted a fixed inspection strategy (Preorder, Inorder, Postorder, or Level-order) to conduct a complete inspection of all hubs, resulting in a complete permutation sequence of the stations.

Your goal is to infer through queries:
1. Which inspection strategy the dispatch center selected
2. What hub is at position {k} in that inspection sequence

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Order Comparison: Ask which of hubs X and Y is inspected earlier in the sequence. I will answer with the hub name.
2. Adjacency Query: Ask whether hub X is inspected immediately before hub Y (i.e., X's turn is exactly Y's turn minus 1). I will answer "Yes" or "No".

Notes:
- Query hubs must belong to {{A, B, C, D, E, F, G, H, I}} and the two hubs must be different
- You must make at least two valid queries before submitting your final answer
- Please use as few queries as possible to infer the answer

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Order Comparison (e.g., asking which of hubs A and B is inspected first):
<query_order>A,B</query_order>

- Adjacency Query (e.g., asking if hub A is inspected immediately before hub B):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the inspection strategy type (Preorder, Inorder, Postorder, or Level-order) and the hub at position {k}, using this format:

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来执行"临床诊疗路径审查"推理程序，规则如下：

系统依托于一个固定的疾病诊断决策树，临床检查项目集合为 {{A, B, C, D, E, F, G, H, I}}，层级结构如下：
- 初诊评估：A
- A 的左分支检查：B；右分支检查：C
- B 的左分支检查：D；右分支检查：E
- C 的左分支检查：F；右分支检查：G
- E 的左分支检查：H；右分支检查：I
- 其他未列出的分支无需检查

医疗质控中心秘密选定了一种临床审查路径（先序 Preorder、中序 Inorder、后序 Postorder 或层序 Level-order），依据该标准对所有检查项目执行了审查，形成了一个完整的审查顺序序列。

你的目标是通过询问推断出：
1. 质控中心采用的临床审查路径类型是什么
2. 在该审查序列中，第 {k} 个被审查的检查项目是哪一项

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 先后比较：询问在审查序列中，项目 X 与项目 Y 哪个优先被审查。我会回答项目名称。
2. 相邻查询：询问在审查序列中，项目 X 是否紧接在项目 Y 之前被审查（即 X 的审查次序恰好是 Y 的次序减 1）。我会回答"是"或"否"。

注意：
- 询问中的项目必须属于 {{A, B, C, D, E, F, G, H, I}} 且两个项目不能相同
- 你需要至少进行两次有效询问后才能提交最终答案
- 请用尽可能少的询问次数推断出答案

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 先后比较（例如询问项目 A 和项目 B 谁优先审查）：
<query_order>A,B</query_order>

- 相邻查询（例如询问项目 A 是否紧接在项目 B 之前审查）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明临床审查路径类型（Preorder、Inorder、Postorder 或 Level-order）并给出第 {k} 个位置的检查项目，格式如下：

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    contextualized_rule_en_2 = """\
[Medical / Healthcare Scenario]
Let's execute the "Clinical Pathway Audit Inference" procedure. Here are the rules:

The system relies on a fixed disease diagnostic decision tree, with a clinical examination items set {{A, B, C, D, E, F, G, H, I}}, structured hierarchically as follows:
- Primary assessment: A
- A's left branch exam: B; right branch exam: C
- B's left branch exam: D; right branch exam: E
- C's left branch exam: F; right branch exam: G
- E's left branch exam: H; right branch exam: I
- Other unlisted branches require no examination

The medical quality control center has secretly selected a clinical audit pathway (Preorder, Inorder, Postorder, or Level-order) and audited all examination items according to that standard, obtaining a complete permutation sequence of the audit order.

Your goal is to infer through queries:
1. Which clinical audit pathway type the control center adopted
2. What examination item is at position {k} in that audit sequence

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Order Comparison: Ask which of items X and Y is audited earlier. I will answer with the item name.
2. Adjacency Query: Ask whether item X is audited immediately before item Y (i.e., X's turn is exactly Y's turn minus 1). I will answer "Yes" or "No".

Notes:
- Query items must belong to {{A, B, C, D, E, F, G, H, I}} and the two items must be different
- You must make at least two valid queries before submitting your final answer
- Please use as few queries as possible to infer the answer

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Order Comparison (e.g., asking which of items A and B is audited first):
<query_order>A,B</query_order>

- Adjacency Query (e.g., asking if item A is audited immediately before item B):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the clinical audit pathway type (Preorder, Inorder, Postorder, or Level-order) and the examination item at position {k}, using this format:

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来使用"课程知识图谱授课顺序"推理系统，规则如下：

系统内置了一门核心课程的前置依赖知识树，知识点集合为 {{A, B, C, D, E, F, G, H, I}}，依赖关系呈现严格的二叉树结构：
- 基础核心知识点：A
- A 的左分支进阶点：B；右分支进阶点：C
- B 的左分支进阶点：D；右分支进阶点：E
- C 的左分支进阶点：F；右分支进阶点：G
- E 的左分支进阶点：H；右分支进阶点：I
- 其他未列出的分支点为空

教务处秘密制定了一种教学大纲授课策略（先序 Preorder、中序 Inorder、后序 Postorder 或层序 Level-order），对所有知识点进行了一次系统性讲解，形成了一个知识点的全排列授课序列。

你的目标是通过询问推断出：
1. 教务处制定的授课策略是哪一种
2. 在该大纲授课序列中第 {k} 个被讲授的知识点是什么

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 先后比较：询问在授课序列中，知识点 X 与知识点 Y 哪个先被讲授。我会回答知识点名称。
2. 相邻查询：询问在授课序列中，知识点 X 是否紧连在知识点 Y 之前讲授（即 X 的课时进度恰好是 Y 的进度减 1）。我会回答"是"或"否"。

注意：
- 询问中的知识点必须属于 {{A, B, C, D, E, F, G, H, I}} 且两个知识点不能相同
- 你需要至少进行两次有效询问后才能提交最终答案
- 请用尽可能少的询问次数推断出答案

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 先后比较（例如询问知识点 A 和知识点 B 谁先讲授）：
<query_order>A,B</query_order>

- 相邻查询（例如询问知识点 A 是否紧连在知识点 B 之前讲授）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明授课策略类型（Preorder、Inorder、Postorder 或 Level-order）并给出第 {k} 个进度的知识点，格式如下：

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's use the "Course Knowledge Graph Teaching Order" inference system. Here are the rules:

The system integrates a prerequisite dependency tree for a core course. The knowledge point set is {{A, B, C, D, E, F, G, H, I}}, showing a strict binary tree structure:
- Fundamental core point: A
- A's left advanced point: B; right advanced point: C
- B's left advanced point: D; right advanced point: E
- C's left advanced point: F; right advanced point: G
- E's left advanced point: H; right advanced point: I
- Other unlisted branch points are null

The academic affairs office has secretly formulated a syllabus teaching strategy (Preorder, Inorder, Postorder, or Level-order) to systematically explain all knowledge points, forming a complete permutation sequence of teaching.

Your goal is to infer through queries:
1. Which teaching strategy the academic affairs office formulated
2. What knowledge point is taught at position {k} in that syllabus sequence

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Order Comparison: Ask which of knowledge points X and Y is taught earlier. I will answer with the knowledge point name.
2. Adjacency Query: Ask whether knowledge point X is taught immediately before point Y (i.e., X's schedule is exactly Y's schedule minus 1). I will answer "Yes" or "No".

Notes:
- Query knowledge points must belong to {{A, B, C, D, E, F, G, H, I}} and the two points must be different
- You must make at least two valid queries before submitting your final answer
- Please use as few queries as possible to infer the answer

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Order Comparison (e.g., asking which of points A and B is taught first):
<query_order>A,B</query_order>

- Adjacency Query (e.g., asking if point A is taught immediately before point B):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the teaching strategy type (Preorder, Inorder, Postorder, or Level-order) and the knowledge point at position {k}, using this format:

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来进行"产品装配工序 SOP 推理"验证，规则如下：

工艺文件设定了一个固定的产品装配 BOM 树，装配工序集合为 {{A, B, C, D, E, F, G, H, I}}，结构流向如下：
- 总成装配：A
- A 的左子系统装配：B；右子系统装配：C
- B 的左子系统装配：D；右子系统装配：E
- C 的左子系统装配：F；右子系统装配：G
- E 的左子系统装配：H；右子系统装配：I
- 其他未列出的子装配工序为空

工艺工程师秘密确定了一种流水线装配策略（先序 Preorder、中序 Inorder、后序 Postorder 或层序 Level-order），并按此策略完成了整个产品的流水线作业，得到一个工序的全排列执行序列。

你的目标是通过询问推断出：
1. 工程师选定的装配策略类型是什么
2. 在该作业 SOP 序列中第 {k} 步执行的装配工序是什么

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据生产记录如实回答：

1. 先后比较：询问在执行序列中，工序 X 与工序 Y 哪个先被执行。我会回答工序名称。
2. 相邻查询：询问在执行序列中，工序 X 是否无缝衔接在工序 Y 之前执行（即 X 的工位进度恰好是 Y 的进度减 1）。我会回答"是"或"否"。

注意：
- 询问中的工序必须属于 {{A, B, C, D, E, F, G, H, I}} 且两个工序不能相同
- 你需要至少进行两次有效询问后才能提交最终答案
- 请用尽可能少的询问次数推断出答案

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 先后比较（例如询问工序 A 和工序 B 谁先执行）：
<query_order>A,B</query_order>

- 相邻查询（例如询问工序 A 是否无缝衔接在工序 B 之前执行）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明装配策略类型（Preorder、Inorder、Postorder 或 Level-order）并给出第 {k} 个位置的装配工序，格式如下：

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing / Industry Scenario]
Let's conduct the "Product Assembly SOP Inference" verification. Here are the rules:

The technical document defines a fixed product assembly BOM tree, with an assembly process set {{A, B, C, D, E, F, G, H, I}}, structured as follows:
- Final assembly: A
- A's left subsystem assembly: B; right subsystem assembly: C
- B's left subsystem assembly: D; right subsystem assembly: E
- C's left subsystem assembly: F; right subsystem assembly: G
- E's left subsystem assembly: H; right subsystem assembly: I
- Other unlisted sub-assemblies are null

The process engineer has secretly determined an assembly line strategy (Preorder, Inorder, Postorder, or Level-order) and completed the entire product line operation according to this strategy, resulting in a complete permutation sequence of the processes.

Your goal is to infer through queries:
1. Which assembly strategy type the engineer selected
2. What assembly process is executed at step {k} in that SOP sequence

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully based on production records:

1. Order Comparison: Ask which of processes X and Y is executed earlier. I will answer with the process name.
2. Adjacency Query: Ask whether process X is executed seamlessly immediately before process Y (i.e., X's step is exactly Y's step minus 1). I will answer "Yes" or "No".

Notes:
- Query processes must belong to {{A, B, C, D, E, F, G, H, I}} and the two processes must be different
- You must make at least two valid queries before submitting your final answer
- Please use as few queries as possible to infer the answer

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Order Comparison (e.g., asking which of processes A and B is executed first):
<query_order>A,B</query_order>

- Adjacency Query (e.g., asking if process A is executed immediately before process B):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the assembly strategy type (Preorder, Inorder, Postorder, or Level-order) and the process at position {k}, using this format:

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来进行"庭审证据链审查逻辑推理"，规则如下：

案卷设定了一个固定的法庭辩论逻辑树，核心诉求与支撑证据集合为 {{A, B, C, D, E, F, G, H, I}}，证据链结构如下：
- 核心诉求点：A
- A 的左侧支撑证据：B；右侧支撑证据：C
- B 的左侧支撑证据：D；右侧支撑证据：E
- C 的左侧支撑证据：F；右侧支撑证据：G
- E 的左侧支撑证据：H；右侧支撑证据：I
- 其他未列出的延展证据为空

法官与审判长秘密采纳了一种庭审审查顺序逻辑（先序 Preorder、中序 Inorder、后序 Postorder 或层序 Level-order），对所有诉求与证据点进行了一轮完整的法庭质证，形成了一个完整的证据链审查序列。

你的目标是通过询问推断出：
1. 法庭采纳的审查顺序逻辑是哪一种
2. 在该庭审审查序列中第 {k} 顺位被审查的证据点是什么

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据庭审记录如实回答：

1. 先后比较：询问在审查序列中，证据 X 与证据 Y 哪个先被法庭质证。我会回答证据点名称。
2. 相邻查询：询问在审查序列中，证据 X 是否紧接在证据 Y 之前被质证（即 X 的出示次序恰好是 Y 的次序减 1）。我会回答"是"或"否"。

注意：
- 询问中的证据点必须属于 {{A, B, C, D, E, F, G, H, I}} 且两个证据点不能相同
- 你需要至少进行两次有效询问后才能提交最终答案
- 请用尽可能少的询问次数推断出答案

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 先后比较（例如询问证据 A 和证据 B 谁先被审查）：
<query_order>A,B</query_order>

- 相邻查询（例如询问证据 A 是否紧接在证据 B 之前审查）：
<query_adjacent>A,B</query_adjacent>

提交最终答案时，必须说明审查逻辑类型（Preorder、Inorder、Postorder 或 Level-order）并给出第 {k} 个位置的证据点，格式如下：

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct the "Court Trial Evidence Chain Review Logic Inference". Here are the rules:

The case file establishes a fixed court debate logic tree, with the core claim and supporting evidence set {{A, B, C, D, E, F, G, H, I}}, structured as follows:
- Core claim: A
- A's left supporting evidence: B; right supporting evidence: C
- B's left supporting evidence: D; right supporting evidence: E
- C's left supporting evidence: F; right supporting evidence: G
- E's left supporting evidence: H; right supporting evidence: I
- Other unlisted extended evidence are null

The presiding judge has secretly adopted a trial review sequence logic (Preorder, Inorder, Postorder, or Level-order) to conduct a complete round of cross-examination on all claims and evidence points, resulting in a complete permutation sequence of the evidence chain review.

Your goal is to infer through queries:
1. Which review sequence logic the court adopted
2. What evidence point is reviewed at rank {k} in that trial review sequence

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully based on trial records:

1. Order Comparison: Ask which of evidence points X and Y is cross-examined earlier. I will answer with the evidence point name.
2. Adjacency Query: Ask whether evidence point X is cross-examined immediately before evidence point Y (i.e., X's presentation turn is exactly Y's turn minus 1). I will answer "Yes" or "No".

Notes:
- Query evidence points must belong to {{A, B, C, D, E, F, G, H, I}} and the two evidence points must be different
- You must make at least two valid queries before submitting your final answer
- Please use as few queries as possible to infer the answer

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Order Comparison (e.g., asking which of evidence A and B is reviewed first):
<query_order>A,B</query_order>

- Adjacency Query (e.g., asking if evidence A is reviewed immediately before evidence B):
<query_adjacent>A,B</query_adjacent>

When submitting the final answer, specify the review logic type (Preorder, Inorder, Postorder, or Level-order) and the evidence point at position {k}, using this format:

<answer>traversal=Preorder, position_{k}=B</answer>
"""

    tags = ["answer", "query_order", "query_adjacent"]

    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"traversal": "Preorder", "k": 6},
            2: {"traversal": "Inorder", "k": 6},
            3: {"traversal": "Postorder", "k": 6},
            4: {"traversal": "Level-order", "k": 6},
            5: {"traversal": "Postorder", "k": 3},
        },
        "en": {
            1: {"traversal": "Preorder", "k": 6},
            2: {"traversal": "Inorder", "k": 6},
            3: {"traversal": "Postorder", "k": 6},
            4: {"traversal": "Level-order", "k": 6},
            5: {"traversal": "Postorder", "k": 3},
        },
    }

    def __init__(self, config):
        # 查询计数器
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：构建二叉树并生成所有遍历序列"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数类型

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.traversal_type = cfg["traversal"]
        self.target_k = cfg["k"]
        self._game_info["k"] = self.target_k

        # 构建二叉树结构（使用字典表示）
        # 格式：节点名 -> (左子节点, 右子节点)
        self.tree = {
            'A': ('B', 'C'),
            'B': ('D', 'E'),
            'C': ('F', 'G'),
            'D': (None, None),
            'E': ('H', 'I'),
            'F': (None, None),
            'G': (None, None),
            'H': (None, None),
            'I': (None, None),
        }

        # 生成所有可能的遍历序列
        self.traversals = {
            'Preorder': self._preorder('A'),
            'Inorder': self._inorder('A'),
            'Postorder': self._postorder('A'),
            'Level-order': self._levelorder(),
        }

        # 获取当前难度对应的遍历序列
        self.current_sequence = self.traversals[self.traversal_type]
        
        # 构建序列索引映射（用于快速查询）
        self.node_position = {node: idx for idx, node in enumerate(self.current_sequence)}


    def _preorder(self, node):
        """先序遍历：根 -> 左子树 -> 右子树"""
        if node is None:
            return []
        left, right = self.tree[node]
        return [node] + self._preorder(left) + self._preorder(right)

    def _inorder(self, node):
        """中序遍历：左子树 -> 根 -> 右子树"""
        if node is None:
            return []
        left, right = self.tree[node]
        return self._inorder(left) + [node] + self._inorder(right)

    def _postorder(self, node):
        """后序遍历：左子树 -> 右子树 -> 根"""
        if node is None:
            return []
        left, right = self.tree[node]
        return self._postorder(left) + self._postorder(right) + [node]

    def _levelorder(self):
        """层序遍历：按层自上而下，同层自左到右"""
        if not self.tree:
            return []
        result = []
        queue = ['A']  # 从根节点开始
        while queue:
            node = queue.pop(0)
            result.append(node)
            left, right = self.tree[node]
            if left:
                queue.append(left)
            if right:
                queue.append(right)
        return result

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        # 检查是否至少询问了两次
        if self.query_count < 2:
            return False

        raw_ans = parsed_info["answer"]
        # 解析答案: traversal=X, position_K=Y
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()

        # 检查必要字段
        position_key = f"position_{self.target_k}"
        if "traversal" not in ans_dict or position_key not in ans_dict:
            return False

        # 检查遍历类型
        if ans_dict["traversal"] != self.traversal_type:
            return False

        # 检查第 K 个位置的节点（注意：题目中位置从1开始）
        expected_node = self.current_sequence[self.target_k - 1]
        return ans_dict[position_key] == expected_node


    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        
        # 预先确定语言对应的回答文本
        if self.config.language == "zh":
            yes_str, no_str = "是", "否"
        else:
            yes_str, no_str = "Yes", "No"

        for n1 in nodes:
            for n2 in nodes:
                # 规则：两个节点不能相同
                if n1 == n2:
                    continue
                
                # 1. 先后比较 query_order
                # 构造符合 parse 解析的 XML 字符串
                q_order = f"<query_order>{n1},{n2}</query_order>"
                
                # 逻辑：比较索引位置，返回较小的那个（即更靠前的）
                idx1 = self.node_position[n1]
                idx2 = self.node_position[n2]
                ans_order = n1 if idx1 < idx2 else n2
                
                queries.append({"query": q_order, "answer": ans_order})

                # 2. 相邻查询 query_adjacent
                # 构造 XML 字符串
                q_adj = f"<query_adjacent>{n1},{n2}</query_adjacent>"
                
                # 逻辑：判断是否紧挨（n1 的位置恰好是 n2 的位置减 1）
                is_adj = (idx1 + 1 == idx2)
                ans_adj = yes_str if is_adj else no_str
                
                queries.append({"query": q_adj, "answer": ans_adj})
                
        return queries

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或节点名称错误。"
            error_same = "错误：两个节点不能相同。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or node name."
            error_same = "Error: The two nodes must be different."

        # 优先处理 query_order
        if "query_order" in parsed_info:
            try:
                raw = parsed_info["query_order"]
                node1, node2 = [x.strip() for x in raw.split(",")]
                
                # 验证节点有效性
                if node1 not in self.node_position or node2 not in self.node_position:
                    return error_format
                if node1 == node2:
                    return error_same

                # 比较位置，返回更靠前的节点
                pos1 = self.node_position[node1]
                pos2 = self.node_position[node2]
                self.query_count += 1
                return node1 if pos1 < pos2 else node2
            except Exception:
                return error_format

        # 处理 query_adjacent
        elif "query_adjacent" in parsed_info:
            try:
                raw = parsed_info["query_adjacent"]
                node1, node2 = [x.strip() for x in raw.split(",")]
                
                # 验证节点有效性
                if node1 not in self.node_position or node2 not in self.node_position:
                    return error_format
                if node1 == node2:
                    return error_same

                # 检查 node1 是否紧挨在 node2 之前
                pos1 = self.node_position[node1]
                pos2 = self.node_position[node2]
                is_adjacent = (pos1 + 1 == pos2)
                self.query_count += 1
                return yes_res if is_adjacent else no_res
            except Exception:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是": return "否"
        if correct == "否": return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            if correct.isupper(): return "NO"
            if correct.istitle(): return "No"
            return "no"
        if lower_correct == "no":
            if correct.isupper(): return "YES"
            if correct.istitle(): return "Yes"
            return "yes"
            
        nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
        if correct in nodes:
            for n in nodes:
                if n != correct:
                    return n
                    
        return correct + "_WRONG"