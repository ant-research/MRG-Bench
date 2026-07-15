from .base import Game
import random

class HiddenTreeLayerGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"隐藏层映射"的推理游戏，规则如下：

游戏设定了一棵无向、连通、无环的树，节点编号为 1 到 {n}，根节点为 {root}。树的边集合为：{edges}。

定义树的高度 H 为从根节点出发的最大最短路径长度。定义第 k 层为距离根节点的最短路径长度为 k 的所有节点集合（k 从 0 到 H）。

**核心机制：隐藏排列**
存在一个固定但未知的排列规则，它将索引 0 到 H 进行了重新映射。当你使用索引 k 进行查询时，系统实际返回的是被重映射后的那一层的信息。

**交互阶段（排练）**
你可以反复进行以下查询来推断这个隐藏的映射关系：

1. 展示查询：询问索引 k 对应的层包含哪些节点。返回升序排列的节点编号列表。
2. 计数查询：询问索引 k 对应的层有多少个节点。返回一个非负整数。
3. 成员查询：询问节点 x 是否属于索引 k 对应的层。返回"是"或"否"。
4. 比较查询：比较索引 k1 和 k2 对应的层的节点数量大小。返回"大于"、"等于"或"小于"。
5. 读取树查询：获取树的基本信息（节点数、根节点、边集合）。
6. 高度查询：获取树的高度 H。

注意：如果输入的索引 k 不在有效范围内，或节点编号 x 无效，系统将返回"无效参数"。

**最终提交阶段**
当你完成至少两次有效查询后，系统会给出一个目标索引 K。此时你必须立即提交答案，不得再进行任何查询。你需要提交真实的第 K 层（未经映射）的所有节点编号，按升序排列。

**查询格式（使用 XML 标签）**

- 展示查询（例如查询索引 2）：
<query_show>2</query_show>

- 计数查询（例如查询索引 1）：
<query_count>1</query_count>

- 成员查询（例如查询节点 5 是否在索引 3 对应的层）：
<query_member>5,3</query_member>

- 比较查询（例如比较索引 0 和索引 2）：
<query_compare>0,2</query_compare>

- 读取树查询（无参数）：
<query_tree></query_tree>

- 高度查询（无参数）：
<query_height></query_height>

**提交答案格式**

当系统给出目标索引 K 后，你需要提交真实第 K 层的节点列表（升序，逗号分隔）：

<answer>1,3,5</answer>

**胜利条件**
提交的节点列表与真实第 K 层完全一致（集合内容和顺序都正确），且在最终阶段没有发起查询。

**失败条件**
答案错误、格式错误、在最终阶段发起查询、或排练阶段有效查询不足两次。
"""

    game_rule_en = """\
Let's play a "Hidden Layer Mapping" deduction game. Here are the rules:

The game features an undirected, connected, acyclic tree with nodes numbered 1 to {n}, and root node {root}. The edge set is: {edges}.

Define the tree height H as the maximum shortest path length from the root. Define layer k as the set of all nodes whose shortest path distance from the root is k (k ranges from 0 to H).

**Core Mechanism: Hidden Permutation**
There exists a fixed but unknown permutation that remaps indices 0 to H. When you query using index k, the system actually returns information about the remapped layer.

**Interaction Phase (Rehearsal)**
You can repeatedly make the following queries to infer the hidden mapping:

1. Show Query: Ask which nodes are in the layer corresponding to index k. Returns an ascending list of node IDs.
2. Count Query: Ask how many nodes are in the layer corresponding to index k. Returns a non-negative integer.
3. Member Query: Ask if node x belongs to the layer corresponding to index k. Returns "Yes" or "No".
4. Compare Query: Compare the sizes of layers corresponding to indices k1 and k2. Returns "Greater", "Equal", or "Less".
5. Tree Query: Get basic tree information (number of nodes, root, edge set).
6. Height Query: Get tree height H.

Note: Invalid index k or node ID x will return "Invalid parameter".

**Final Submission Phase**
After completing at least two valid queries, the system will provide a target index K. You must immediately submit your answer without making any more queries. You need to submit all node IDs in the true layer K (unmapped), in ascending order.

**Query Format (using XML tags)**

- Show Query (e.g., querying index 2):
<query_show>2</query_show>

- Count Query (e.g., querying index 1):
<query_count>1</query_count>

- Member Query (e.g., checking if node 5 is in layer corresponding to index 3):
<query_member>5,3</query_member>

- Compare Query (e.g., comparing indices 0 and 2):
<query_compare>0,2</query_compare>

- Tree Query (no parameters):
<query_tree></query_tree>

- Height Query (no parameters):
<query_height></query_height>

**Answer Submission Format**

When the system provides target index K, submit the true layer K node list (ascending, comma-separated):

<answer>1,3,5</answer>

**Victory Condition**
The submitted node list matches the true layer K exactly (both content and order), and no queries were made in the final phase.

**Failure Condition**
Wrong answer, invalid format, querying in final phase, or fewer than two valid queries in rehearsal phase.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项"隐藏路由映射"的交通网络分析任务，规则如下：

系统设定了一个无向、连通、无环的交通网络结构，站点编号为 1 到 {n}，核心枢纽站为 {root}。网络的直达路线集合为：{edges}。

定义网络的换乘深度 H 为从核心枢纽站出发的最大最少换乘次数。定义第 k 级换乘圈为距离核心枢纽站最少换乘次数为 k 的所有站点集合（k 从 0 到 H）。

**核心机制：加密别名映射**
网络系统中存在一个固定但未知的映射规则，它将真实换乘级数 0 到 H 的索引进行了重新分配。当你使用索引 k 进行查询时，系统实际返回的是被重映射后的那个换乘圈的信息。

**交互阶段（排练）**
你可以反复进行以下查询来推断这个隐藏的映射关系：

1. 展示查询：询问索引 k 对应的换乘圈包含哪些站点。返回升序排列的站点编号列表。
2. 计数查询：询问索引 k 对应的换乘圈有多少个站点。返回一个非负整数。
3. 成员查询：询问站点 x 是否属于索引 k 对应的换乘圈。返回"是"或"否"。
4. 比较查询：比较索引 k1 和 k2 对应的换乘圈的站点数量大小。返回"大于"、"等于"或"小于"。
5. 读取树查询：获取交通网络的基本信息（站点总数、核心枢纽站、路线集合）。
6. 高度查询：获取网络的换乘深度 H。

注意：如果输入的索引 k 不在有效范围内，或站点编号 x 无效，系统将返回"无效参数"。

**最终提交阶段**
当你完成至少两次有效查询后，系统会给出一个目标真实层级 K。此时你必须立即提交答案，不得再进行任何查询。你需要提交真实的第 K 级换乘圈（未经映射的）的所有站点编号，按升序排列。

**查询格式（使用 XML 标签）**

- 展示查询（例如查询索引 2）：
<query_show>2</query_show>

- 计数查询（例如查询索引 1）：
<query_count>1</query_count>

- 成员查询（例如查询站点 5 是否在索引 3 对应的换乘圈）：
<query_member>5,3</query_member>

- 比较查询（例如比较索引 0 和索引 2）：
<query_compare>0,2</query_compare>

- 读取树查询（无参数）：
<query_tree></query_tree>

- 高度查询（无参数）：
<query_height></query_height>

**提交答案格式**

当系统给出目标层级 K 后，你需要提交真实第 K 级的站点列表（升序，逗号分隔）：

<answer>1,3,5</answer>

**胜利条件**
提交的站点列表与真实第 K 级换乘圈完全一致（集合内容和顺序都正确），且在最终阶段没有发起查询。

**失败条件**
答案错误、格式错误、在最终阶段发起查询、或排练阶段有效查询不足两次。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's perform a "Hidden Route Mapping" transport network analysis task. Here are the rules:

The system defines an undirected, connected, acyclic transport network, with stations numbered 1 to {n}, and the central hub station being {root}. The set of direct routes is: {edges}.

Define the network transfer depth H as the maximum minimum number of transfers from the central hub. Define transfer tier k as the set of all stations whose minimum transfer distance from the central hub is k (k ranges from 0 to H).

**Core Mechanism: Encrypted Alias Mapping**
There exists a fixed but unknown permutation rule in the system that remaps the true transfer tier indices 0 to H. When you query using index k, the system actually returns information about the remapped transfer tier.

**Interaction Phase (Rehearsal)**
You can repeatedly make the following queries to infer the hidden mapping:

1. Show Query: Ask which stations are in the tier corresponding to index k. Returns an ascending list of station IDs.
2. Count Query: Ask how many stations are in the tier corresponding to index k. Returns a non-negative integer.
3. Member Query: Ask if station x belongs to the tier corresponding to index k. Returns "Yes" or "No".
4. Compare Query: Compare the sizes of tiers corresponding to indices k1 and k2. Returns "Greater", "Equal", or "Less".
5. Tree Query: Get basic network information (total stations, central hub, route set).
6. Height Query: Get the network transfer depth H.

Note: Invalid index k or station ID x will return "Invalid parameter".

**Final Submission Phase**
After completing at least two valid queries, the system will provide a target true tier K. You must immediately submit your answer without making any more queries. You need to submit all station IDs in the true transfer tier K (unmapped), in ascending order.

**Query Format (using XML tags)**

- Show Query (e.g., querying index 2):
<query_show>2</query_show>

- Count Query (e.g., querying index 1):
<query_count>1</query_count>

- Member Query (e.g., checking if station 5 is in tier corresponding to index 3):
<query_member>5,3</query_member>

- Compare Query (e.g., comparing indices 0 and 2):
<query_compare>0,2</query_compare>

- Tree Query (no parameters):
<query_tree></query_tree>

- Height Query (no parameters):
<query_height></query_height>

**Answer Submission Format**

When the system provides target tier K, submit the true tier K station list (ascending, comma-separated):

<answer>1,3,5</answer>

**Victory Condition**
The submitted station list matches the true tier K exactly (both content and order), and no queries were made in the final phase.

**Failure Condition**
Wrong answer, invalid format, querying in final phase, or fewer than two valid queries in rehearsal phase.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项"隐匿传播链映射"的流行病学流调任务，规则如下：

系统记录了一起无向、连通、无环的疾病传播网络，人员编号为 1 到 {n}，零号病人（初始感染源）为 {root}。已确认的密接传播路径集合为：{edges}。

定义传播网络的最大世代数 H 为从零号病人出发的最长传播路径长度。定义第 k 世代为距离零号病人传播路径长度为 k 的所有人员集合（k 从 0 到 H）。

**核心机制：隐私代号映射**
为了保护患者隐私，系统采用了一个固定但未知的映射规则，将真实的世代索引 0 到 H 重新分配了代号。当你使用索引 k 进行查询时，系统实际返回的是被重映射后的那个世代的信息。

**交互阶段（排练）**
你可以反复进行以下查询来推断这个隐藏的映射关系：

1. 展示查询：询问索引 k 对应的世代包含哪些人员。返回升序排列的人员编号列表。
2. 计数查询：询问索引 k 对应的世代有多少个人员。返回一个非负整数。
3. 成员查询：询问人员 x 是否属于索引 k 对应的世代。返回"是"或"否"。
4. 比较查询：比较索引 k1 和 k2 对应的世代的人员数量大小。返回"大于"、"等于"或"小于"。
5. 读取树查询：获取传播网络的基本信息（人员总数、零号病人、传播路径集合）。
6. 高度查询：获取最大传播世代数 H。

注意：如果输入的索引 k 不在有效范围内，或人员编号 x 无效，系统将返回"无效参数"。

**最终提交阶段**
当你完成至少两次有效查询后，系统会给出一个目标真实世代 K。此时你必须立即提交答案，不得再进行任何查询。你需要提交真实的第 K 世代（未经映射的）的所有人员编号，按升序排列。

**查询格式（使用 XML 标签）**

- 展示查询（例如查询索引 2）：
<query_show>2</query_show>

- 计数查询（例如查询索引 1）：
<query_count>1</query_count>

- 成员查询（例如查询人员 5 是否在索引 3 对应的世代）：
<query_member>5,3</query_member>

- 比较查询（例如比较索引 0 和索引 2）：
<query_compare>0,2</query_compare>

- 读取树查询（无参数）：
<query_tree></query_tree>

- 高度查询（无参数）：
<query_height></query_height>

**提交答案格式**

当系统给出目标世代 K 后，你需要提交真实第 K 世代的人员列表（升序，逗号分隔）：

<answer>1,3,5</answer>

**胜利条件**
提交的人员列表与真实第 K 世代完全一致（集合内容和顺序都正确），且在最终阶段没有发起查询。

**失败条件**
答案错误、格式错误、在最终阶段发起查询、或排练阶段有效查询不足两次。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's perform an epidemiological contact tracing task regarding a "Hidden Transmission Chain Mapping". Here are the rules:

The system records an undirected, connected, acyclic disease transmission network, with individuals numbered 1 to {n}, and Patient Zero (initial source) being {root}. The set of confirmed close contact transmission paths is: {edges}.

Define the maximum transmission generation H as the longest transmission path length from Patient Zero. Define generation k as the set of all individuals whose transmission path distance from Patient Zero is k (k ranges from 0 to H).

**Core Mechanism: Privacy Code Mapping**
To protect patient privacy, the system uses a fixed but unknown permutation rule that remaps the true generation indices 0 to H with privacy codes. When you query using index k, the system actually returns information about the remapped generation.

**Interaction Phase (Rehearsal)**
You can repeatedly make the following queries to infer the hidden mapping:

1. Show Query: Ask which individuals are in the generation corresponding to index k. Returns an ascending list of individual IDs.
2. Count Query: Ask how many individuals are in the generation corresponding to index k. Returns a non-negative integer.
3. Member Query: Ask if individual x belongs to the generation corresponding to index k. Returns "Yes" or "No".
4. Compare Query: Compare the sizes of generations corresponding to indices k1 and k2. Returns "Greater", "Equal", or "Less".
5. Tree Query: Get basic network information (total individuals, Patient Zero, transmission path set).
6. Height Query: Get the maximum transmission generation H.

Note: Invalid index k or individual ID x will return "Invalid parameter".

**Final Submission Phase**
After completing at least two valid queries, the system will provide a target true generation K. You must immediately submit your answer without making any more queries. You need to submit all individual IDs in the true generation K (unmapped), in ascending order.

**Query Format (using XML tags)**

- Show Query (e.g., querying index 2):
<query_show>2</query_show>

- Count Query (e.g., querying index 1):
<query_count>1</query_count>

- Member Query (e.g., checking if individual 5 is in generation corresponding to index 3):
<query_member>5,3</query_member>

- Compare Query (e.g., comparing indices 0 and 2):
<query_compare>0,2</query_compare>

- Tree Query (no parameters):
<query_tree></query_tree>

- Height Query (no parameters):
<query_height></query_height>

**Answer Submission Format**

When the system provides target generation K, submit the true generation K individual list (ascending, comma-separated):

<answer>1,3,5</answer>

**Victory Condition**
The submitted individual list matches the true generation K exactly (both content and order), and no queries were made in the final phase.

**Failure Condition**
Wrong answer, invalid format, querying in final phase, or fewer than two valid queries in rehearsal phase.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项"隐式先决条件映射"的知识图谱构建任务，规则如下：

系统包含一棵无向、连通、无环的知识模块依赖树，模块编号为 1 到 {n}，核心基础模块为 {root}。模块间的直接关联边集合为：{edges}。

定义知识体系的最大深度 H 为从核心基础模块出发的最长学习路径长度。定义第 k 学习阶段为距离核心基础模块路径长度为 k 的所有知识模块集合（k 从 0 到 H）。

**核心机制：乱序结构映射**
系统出于评测目的，采用了一个固定但未知的映射规则，将真实的学习阶段索引 0 到 H 进行了重新打乱。当你使用索引 k 进行查询时，系统实际返回的是被重映射后的那个学习阶段的信息。

**交互阶段（排练）**
你可以反复进行以下查询来推断这个隐藏的映射关系：

1. 展示查询：询问索引 k 对应的学习阶段包含哪些模块。返回升序排列的模块编号列表。
2. 计数查询：询问索引 k 对应的学习阶段有多少个模块。返回一个非负整数。
3. 成员查询：询问模块 x 是否属于索引 k 对应的学习阶段。返回"是"或"否"。
4. 比较查询：比较索引 k1 和 k2 对应的学习阶段的模块数量大小。返回"大于"、"等于"或"小于"。
5. 读取树查询：获取知识图谱的基本信息（模块总数、核心基础模块、关联边集合）。
6. 高度查询：获取最大学习深度 H。

注意：如果输入的索引 k 不在有效范围内，或模块编号 x 无效，系统将返回"无效参数"。

**最终提交阶段**
当你完成至少两次有效查询后，系统会给出一个目标真实阶段 K。此时你必须立即提交答案，不得再进行任何查询。你需要提交真实的第 K 学习阶段（未经映射的）的所有模块编号，按升序排列。

**查询格式（使用 XML 标签）**

- 展示查询（例如查询索引 2）：
<query_show>2</query_show>

- 计数查询（例如查询索引 1）：
<query_count>1</query_count>

- 成员查询（例如查询模块 5 是否在索引 3 对应的学习阶段）：
<query_member>5,3</query_member>

- 比较查询（例如比较索引 0 和索引 2）：
<query_compare>0,2</query_compare>

- 读取树查询（无参数）：
<query_tree></query_tree>

- 高度查询（无参数）：
<query_height></query_height>

**提交答案格式**

当系统给出目标阶段 K 后，你需要提交真实第 K 阶段的模块列表（升序，逗号分隔）：

<answer>1,3,5</answer>

**胜利条件**
提交的模块列表与真实第 K 学习阶段完全一致（集合内容和顺序都正确），且在最终阶段没有发起查询。

**失败条件**
答案错误、格式错误、在最终阶段发起查询、或排练阶段有效查询不足两次。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform a knowledge graph construction task regarding an "Implicit Prerequisite Mapping". Here are the rules:

The system contains an undirected, connected, acyclic knowledge module dependency tree, with modules numbered 1 to {n}, and the core fundamental module being {root}. The set of direct association edges between modules is: {edges}.

Define the maximum depth H of the knowledge system as the longest learning path length from the core fundamental module. Define learning stage k as the set of all knowledge modules whose path distance from the core fundamental module is k (k ranges from 0 to H).

**Core Mechanism: Shuffled Structure Mapping**
For assessment purposes, the system uses a fixed but unknown permutation rule that shuffles and remaps the true learning stage indices 0 to H. When you query using index k, the system actually returns information about the remapped learning stage.

**Interaction Phase (Rehearsal)**
You can repeatedly make the following queries to infer the hidden mapping:

1. Show Query: Ask which modules are in the learning stage corresponding to index k. Returns an ascending list of module IDs.
2. Count Query: Ask how many modules are in the learning stage corresponding to index k. Returns a non-negative integer.
3. Member Query: Ask if module x belongs to the learning stage corresponding to index k. Returns "Yes" or "No".
4. Compare Query: Compare the sizes of learning stages corresponding to indices k1 and k2. Returns "Greater", "Equal", or "Less".
5. Tree Query: Get basic knowledge graph information (total modules, core fundamental module, association edge set).
6. Height Query: Get the maximum learning depth H.

Note: Invalid index k or module ID x will return "Invalid parameter".

**Final Submission Phase**
After completing at least two valid queries, the system will provide a target true learning stage K. You must immediately submit your answer without making any more queries. You need to submit all module IDs in the true learning stage K (unmapped), in ascending order.

**Query Format (using XML tags)**

- Show Query (e.g., querying index 2):
<query_show>2</query_show>

- Count Query (e.g., querying index 1):
<query_count>1</query_count>

- Member Query (e.g., checking if module 5 is in stage corresponding to index 3):
<query_member>5,3</query_member>

- Compare Query (e.g., comparing indices 0 and 2):
<query_compare>0,2</query_compare>

- Tree Query (no parameters):
<query_tree></query_tree>

- Height Query (no parameters):
<query_height></query_height>

**Answer Submission Format**

When the system provides target stage K, submit the true stage K module list (ascending, comma-separated):

<answer>1,3,5</answer>

**Victory Condition**
The submitted module list matches the true stage K exactly (both content and order), and no queries were made in the final phase.

**Failure Condition**
Wrong answer, invalid format, querying in final phase, or fewer than two valid queries in rehearsal phase.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项"隐藏物料层级映射"的供应链结构解析任务，规则如下：

系统记录了一个无向、连通、无环的产品装配BOM（物料清单）树，零件编号为 1 到 {n}，最终成品为 {root}。装配依赖关系的边集合为：{edges}。

定义供应链最大纵深 H 为从最终成品出发的最长依赖路径长度。定义第 k 级物料层为距离最终成品依赖路径长度为 k 的所有零件集合（k 从 0 到 H）。

**核心机制：供应商代码映射**
为了保密供应链结构，系统采用了一个固定但未知的映射规则，将真实的物料层级索引 0 到 H 替换为匿名供应商代码。当你使用索引 k 进行查询时，系统实际返回的是被重映射后的那个物料层的信息。

**交互阶段（排练）**
你可以反复进行以下查询来推断这个隐藏的映射关系：

1. 展示查询：询问索引 k 对应的物料层包含哪些零件。返回升序排列的零件编号列表。
2. 计数查询：询问索引 k 对应的物料层有多少个零件。返回一个非负整数。
3. 成员查询：询问零件 x 是否属于索引 k 对应的物料层。返回"是"或"否"。
4. 比较查询：比较索引 k1 和 k2 对应的物料层的零件数量大小。返回"大于"、"等于"或"小于"。
5. 读取树查询：获取BOM树的基本信息（零件总数、最终成品、依赖关系边集合）。
6. 高度查询：获取供应链最大纵深 H。

注意：如果输入的索引 k 不在有效范围内，或零件编号 x 无效，系统将返回"无效参数"。

**最终提交阶段**
当你完成至少两次有效查询后，系统会给出一个目标真实物料层级 K。此时你必须立即提交答案，不得再进行任何查询。你需要提交真实的第 K 级物料层（未经映射的）的所有零件编号，按升序排列。

**查询格式（使用 XML 标签）**

- 展示查询（例如查询索引 2）：
<query_show>2</query_show>

- 计数查询（例如查询索引 1）：
<query_count>1</query_count>

- 成员查询（例如查询零件 5 是否在索引 3 对应的物料层）：
<query_member>5,3</query_member>

- 比较查询（例如比较索引 0 和索引 2）：
<query_compare>0,2</query_compare>

- 读取树查询（无参数）：
<query_tree></query_tree>

- 高度查询（无参数）：
<query_height></query_height>

**提交答案格式**

当系统给出目标层级 K 后，你需要提交真实第 K 级的零件列表（升序，逗号分隔）：

<answer>1,3,5</answer>

**胜利条件**
提交的零件列表与真实第 K 级物料层完全一致（集合内容和顺序都正确），且在最终阶段没有发起查询。

**失败条件**
答案错误、格式错误、在最终阶段发起查询、或排练阶段有效查询不足两次。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's perform a supply chain structure resolution task regarding a "Hidden BOM Tier Mapping". Here are the rules:

The system records an undirected, connected, acyclic product assembly BOM (Bill of Materials) tree, with parts numbered 1 to {n}, and the final product being {root}. The set of assembly dependency edges is: {edges}.

Define the maximum supply chain depth H as the longest dependency path length from the final product. Define BOM tier k as the set of all parts whose dependency path distance from the final product is k (k ranges from 0 to H).

**Core Mechanism: Supplier Code Mapping**
To keep the supply chain structure confidential, the system uses a fixed but unknown permutation rule that replaces the true BOM tier indices 0 to H with anonymous supplier codes. When you query using index k, the system actually returns information about the remapped BOM tier.

**Interaction Phase (Rehearsal)**
You can repeatedly make the following queries to infer the hidden mapping:

1. Show Query: Ask which parts are in the BOM tier corresponding to index k. Returns an ascending list of part IDs.
2. Count Query: Ask how many parts are in the BOM tier corresponding to index k. Returns a non-negative integer.
3. Member Query: Ask if part x belongs to the BOM tier corresponding to index k. Returns "Yes" or "No".
4. Compare Query: Compare the sizes of BOM tiers corresponding to indices k1 and k2. Returns "Greater", "Equal", or "Less".
5. Tree Query: Get basic BOM tree information (total parts, final product, dependency edge set).
6. Height Query: Get the maximum supply chain depth H.

Note: Invalid index k or part ID x will return "Invalid parameter".

**Final Submission Phase**
After completing at least two valid queries, the system will provide a target true BOM tier K. You must immediately submit your answer without making any more queries. You need to submit all part IDs in the true BOM tier K (unmapped), in ascending order.

**Query Format (using XML tags)**

- Show Query (e.g., querying index 2):
<query_show>2</query_show>

- Count Query (e.g., querying index 1):
<query_count>1</query_count>

- Member Query (e.g., checking if part 5 is in tier corresponding to index 3):
<query_member>5,3</query_member>

- Compare Query (e.g., comparing indices 0 and 2):
<query_compare>0,2</query_compare>

- Tree Query (no parameters):
<query_tree></query_tree>

- Height Query (no parameters):
<query_height></query_height>

**Answer Submission Format**

When the system provides target tier K, submit the true tier K part list (ascending, comma-separated):

<answer>1,3,5</answer>

**Victory Condition**
The submitted part list matches the true tier K exactly (both content and order), and no queries were made in the final phase.

**Failure Condition**
Wrong answer, invalid format, querying in final phase, or fewer than two valid queries in rehearsal phase.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项"隐蔽股权架构映射"的资本穿透调查任务，规则如下：

系统调取了一张无向、连通、无环的企业控制权网络，实体（公司/个人）编号为 1 到 {n}，实际控制人/最终母公司为 {root}。股权控制关系的边集合为：{edges}。

定义控制权网络的最大穿透层数 H 为从实际控制人出发的最长控制链长度。定义第 k 级投资主体层为距离实际控制人控制链长度为 k 的所有实体集合（k 从 0 到 H）。

**核心机制：空壳代持映射**
为了掩盖真实的资金流向，该网络采用了一个固定但未知的映射规则，将真实的投资层级索引 0 到 H 替换为了混淆的代持层级代码。当你使用索引 k 进行查询时，系统实际返回的是被重映射后的那个混淆主体层的信息。

**交互阶段（排练）**
你可以反复进行以下查询来推断这个隐藏的映射关系：

1. 展示查询：询问索引 k 对应的投资主体层包含哪些实体。返回升序排列的实体编号列表。
2. 计数查询：询问索引 k 对应的投资主体层有多少个实体。返回一个非负整数。
3. 成员查询：询问实体 x 是否属于索引 k 对应的投资主体层。返回"是"或"否"。
4. 比较查询：比较索引 k1 和 k2 对应的投资主体层的实体数量大小。返回"大于"、"等于"或"小于"。
5. 读取树查询：获取企业控制权网络的基本信息（实体总数、实际控制人、控制关系边集合）。
6. 高度查询：获取最大穿透层数 H。

注意：如果输入的索引 k 不在有效范围内，或实体编号 x 无效，系统将返回"无效参数"。

**最终提交阶段**
当你完成至少两次有效查询后，系统会给出一个目标真实的投资主体层 K。此时你必须立即提交答案，不得再进行任何查询。你需要提交真实的第 K 级投资主体层（未经映射的）的所有实体编号，按升序排列。

**查询格式（使用 XML 标签）**

- 展示查询（例如查询索引 2）：
<query_show>2</query_show>

- 计数查询（例如查询索引 1）：
<query_count>1</query_count>

- 成员查询（例如查询实体 5 是否在索引 3 对应的投资主体层）：
<query_member>5,3</query_member>

- 比较查询（例如比较索引 0 和索引 2）：
<query_compare>0,2</query_compare>

- 读取树查询（无参数）：
<query_tree></query_tree>

- 高度查询（无参数）：
<query_height></query_height>

**提交答案格式**

当系统给出目标投资主体层 K 后，你需要提交真实第 K 层的实体列表（升序，逗号分隔）：

<answer>1,3,5</answer>

**胜利条件**
提交的实体列表与真实第 K 级投资主体层完全一致（集合内容和顺序都正确），且在最终阶段没有发起查询。

**失败条件**
答案错误、格式错误、在最终阶段发起查询、或排练阶段有效查询不足两次。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's perform a capital penetration investigation task regarding a "Hidden Equity Structure Mapping". Here are the rules:

The system has retrieved an undirected, connected, acyclic corporate control network, with entities (companies/individuals) numbered 1 to {n}, and the ultimate controller/parent company being {root}. The set of equity control relationship edges is: {edges}.

Define the maximum penetration depth H of the control network as the longest control chain length from the ultimate controller. Define investment tier k as the set of all entities whose control chain length from the ultimate controller is k (k ranges from 0 to H).

**Core Mechanism: Shell Holding Mapping**
To conceal the true flow of capital, the network uses a fixed but unknown permutation rule that replaces the true investment tier indices 0 to H with obfuscated holding tier codes. When you query using index k, the system actually returns information about the remapped obfuscated entity tier.

**Interaction Phase (Rehearsal)**
You can repeatedly make the following queries to infer the hidden mapping:

1. Show Query: Ask which entities are in the investment tier corresponding to index k. Returns an ascending list of entity IDs.
2. Count Query: Ask how many entities are in the investment tier corresponding to index k. Returns a non-negative integer.
3. Member Query: Ask if entity x belongs to the investment tier corresponding to index k. Returns "Yes" or "No".
4. Compare Query: Compare the sizes of investment tiers corresponding to indices k1 and k2. Returns "Greater", "Equal", or "Less".
5. Tree Query: Get basic corporate control network information (total entities, ultimate controller, control relationship edge set).
6. Height Query: Get the maximum penetration depth H.

Note: Invalid index k or entity ID x will return "Invalid parameter".

**Final Submission Phase**
After completing at least two valid queries, the system will provide a target true investment tier K. You must immediately submit your answer without making any more queries. You need to submit all entity IDs in the true investment tier K (unmapped), in ascending order.

**Query Format (using XML tags)**

- Show Query (e.g., querying index 2):
<query_show>2</query_show>

- Count Query (e.g., querying index 1):
<query_count>1</query_count>

- Member Query (e.g., checking if entity 5 is in investment tier corresponding to index 3):
<query_member>5,3</query_member>

- Compare Query (e.g., comparing indices 0 and 2):
<query_compare>0,2</query_compare>

- Tree Query (no parameters):
<query_tree></query_tree>

- Height Query (no parameters):
<query_height></query_height>

**Answer Submission Format**

When the system provides target investment tier K, submit the true investment tier K entity list (ascending, comma-separated):

<answer>1,3,5</answer>

**Victory Condition**
The submitted entity list matches the true investment tier K exactly (both content and order), and no queries were made in the final phase.

**Failure Condition**
Wrong answer, invalid format, querying in final phase, or fewer than two valid queries in rehearsal phase.
"""

    tags = ["answer", "query_show", "query_count", "query_member", "query_compare", "query_tree", "query_height"]

    DIFFICULTY_CONFIG = {
        1: {
            "n": 7,
            "root": 1,
            "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            "permutation": [0, 2, 1],
        },
        2: {
            "n": 10,
            "root": 1,
            "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10)],
            "permutation": [3, 1, 2, 0],
        },
        3: {
            "n": 11,
            "root": 1,
            "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10), (6, 11)],
            "permutation": [2, 3, 0, 1],
        },
        4: {
            "n": 15,
            "root": 1,
            "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (8, 12), (9, 13), (10, 14), (11, 15)],
            "permutation": [4, 2, 0, 3, 1],
        },
        5: {
            "n": 16,
            "root": 1,
            "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (8, 12), (9, 13), (10, 14), (11, 15), (12, 16)],
            "permutation": [3, 4, 1, 0, 2],
        },
    }

    def __init__(self, config):
        self.query_count = 0
        self.final_phase = False
        self.target_index = None
        self._rng = random.Random(42)
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.n = cfg["n"]
        self.root = cfg["root"]
        self.edges = cfg["edges"]
        self.permutation = cfg["permutation"]

        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)

        self.distances = self._compute_distances()

        self.height = max(self.distances.values())

        self.layers = {k: [] for k in range(self.height + 1)}
        for node, dist in self.distances.items():
            self.layers[dist].append(node)
        
        for k in self.layers:
            self.layers[k].sort()

        edges_str = ", ".join([f"({u},{v})" for u, v in self.edges])
        
        self._game_info = {
            "n": self.n,
            "root": self.root,
            "edges": edges_str,
        }

    def _compute_distances(self):
        from collections import deque
        distances = {}
        queue = deque([self.root])
        distances[self.root] = 0
        
        while queue:
            node = queue.popleft()
            for neighbor in self.adj[node]:
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        
        return distances

    def _get_mapped_layer(self, index):
        if index < 0 or index > self.height:
            return None
        true_layer = self.permutation[index]
        return self.layers[true_layer]

    def evaluate(self, parsed_info):
        if not self.final_phase:
            return False
        
        raw_ans = parsed_info["answer"].strip()
        
        try:
            submitted_nodes = [int(x.strip()) for x in raw_ans.split(",") if x.strip()]
            submitted_nodes.sort()
            
            true_layer = sorted(self.layers[self.target_index])
            
            return submitted_nodes == true_layer
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.final_phase:
            raise ValueError("Queries are not allowed in the final phase.")

        yes_res = "是" if self.config.language == "zh" else "Yes"
        no_res = "否" if self.config.language == "zh" else "No"
        invalid_res = "无效参数" if self.config.language == "zh" else "Invalid parameter"
        greater_res = "大于" if self.config.language == "zh" else "Greater"
        equal_res = "等于" if self.config.language == "zh" else "Equal"
        less_res = "小于" if self.config.language == "zh" else "Less"

        if "query_show" in parsed_info:
            try:
                k = int(parsed_info["query_show"].strip())
                layer = self._get_mapped_layer(k)
                if layer is None:
                    return invalid_res
                self.query_count += 1
                return ",".join(map(str, layer))
            except:
                return invalid_res

        elif "query_count" in parsed_info:
            try:
                k = int(parsed_info["query_count"].strip())
                layer = self._get_mapped_layer(k)
                if layer is None:
                    return invalid_res
                self.query_count += 1
                return str(len(layer))
            except:
                return invalid_res

        elif "query_member" in parsed_info:
            try:
                parts = [x.strip() for x in parsed_info["query_member"].split(",")]
                x = int(parts[0])
                k = int(parts[1])
                
                if x < 1 or x > self.n:
                    return invalid_res
                
                layer = self._get_mapped_layer(k)
                if layer is None:
                    return invalid_res
                
                self.query_count += 1
                return yes_res if x in layer else no_res
            except:
                return invalid_res

        elif "query_compare" in parsed_info:
            try:
                parts = [x.strip() for x in parsed_info["query_compare"].split(",")]
                k1 = int(parts[0])
                k2 = int(parts[1])
                
                layer1 = self._get_mapped_layer(k1)
                layer2 = self._get_mapped_layer(k2)
                
                if layer1 is None or layer2 is None:
                    return invalid_res
                
                self.query_count += 1
                size1, size2 = len(layer1), len(layer2)
                
                if size1 > size2:
                    return greater_res
                elif size1 == size2:
                    return equal_res
                else:
                    return less_res
            except:
                return invalid_res

        elif "query_tree" in parsed_info:
            self.query_count += 1
            edges_str = "; ".join([f"({u},{v})" for u, v in self.edges])
            if self.config.language == "zh":
                return f"节点数: {self.n}, 根节点: {self.root}, 边集合: {edges_str}"
            else:
                return f"Nodes: {self.n}, Root: {self.root}, Edges: {edges_str}"

        elif "query_height" in parsed_info:
            self.query_count += 1
            return str(self.height)

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        if correct.lower() == "yes":
            return "No" if correct == "Yes" else "no"
        if correct.lower() == "no":
            return "Yes" if correct == "No" else "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        queries = []
        
        yes_res = "是" if self.config.language == "zh" else "Yes"
        no_res = "否" if self.config.language == "zh" else "No"
        greater_res = "大于" if self.config.language == "zh" else "Greater"
        equal_res = "等于" if self.config.language == "zh" else "Equal"
        less_res = "小于" if self.config.language == "zh" else "Less"

        for k in range(self.height + 1):
            layer = self._get_mapped_layer(k)
            if layer is not None:
                ans = ",".join(map(str, layer))
                queries.append({
                    "query": f"<query_show>{k}</query_show>",
                    "answer": ans
                })

        for k in range(self.height + 1):
            layer = self._get_mapped_layer(k)
            if layer is not None:
                ans = str(len(layer))
                queries.append({
                    "query": f"<query_count>{k}</query_count>",
                    "answer": ans
                })

        for x in range(1, self.n + 1):
            for k in range(self.height + 1):
                layer = self._get_mapped_layer(k)
                if layer is not None:
                    ans = yes_res if x in layer else no_res
                    queries.append({
                        "query": f"<query_member>{x},{k}</query_member>",
                        "answer": ans
                    })

        for k1 in range(self.height + 1):
            for k2 in range(self.height + 1):
                layer1 = self._get_mapped_layer(k1)
                layer2 = self._get_mapped_layer(k2)
                
                if layer1 is not None and layer2 is not None:
                    size1, size2 = len(layer1), len(layer2)
                    if size1 > size2:
                        ans = greater_res
                    elif size1 == size2:
                        ans = equal_res
                    else:
                        ans = less_res
                    
                    queries.append({
                        "query": f"<query_compare>{k1},{k2}</query_compare>",
                        "answer": ans
                    })

        edges_str = "; ".join([f"({u},{v})" for u, v in self.edges])
        if self.config.language == "zh":
            ans_tree = f"节点数: {self.n}, 根节点: {self.root}, 边集合: {edges_str}"
        else:
            ans_tree = f"Nodes: {self.n}, Root: {self.root}, Edges: {edges_str}"
        queries.append({
            "query": "<query_tree></query_tree>",
            "answer": ans_tree
        })

        queries.append({
            "query": "<query_height></query_height>",
            "answer": str(self.height)
        })

        return queries

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info:
                if self.query_count < 2:
                    if self.config.language == "zh":
                        res = "失败：排练阶段有效查询不足两次。"
                    else:
                        res = "Failed: Fewer than two valid queries in rehearsal phase."
                    self.state.set_state("failed", "insufficient queries")
                    self.state.add_message("user", res)
                    return self.state
                
                if not self.final_phase:
                    self.final_phase = True
                    self.target_index = self._rng.randint(0, self.height)
                    
                    if self.config.language == "zh":
                        prompt = f"排练阶段结束。现在请提交真实第 {self.target_index} 层的节点列表（升序，逗号分隔）："
                    else:
                        prompt = f"Rehearsal phase ended. Now submit the true layer {self.target_index} node list (ascending, comma-separated):"
                    
                    self.state.add_message("user", prompt)
                    return self.state
                
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确" if self.config.language == "zh" else "Correct answer."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            
            else:
                if self.final_phase:
                    if self.config.language == "zh":
                        res = "失败：最终阶段不允许进行查询。"
                    else:
                        res = "Failed: Queries are not allowed in the final phase."
                    self.state.set_state("failed", "query in final phase")
                    self.state.add_message("user", res)
                    return self.state
                
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state