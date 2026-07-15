from .base import Game
import random
import re

class TreeDeleteRuleGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树删除规律推理"游戏，规则如下：

游戏设定了一棵包含 {n} 个结点的无向树，结点编号为 1 到 {n}。我已为这棵树秘密指定了一个根结点（固定但不公开），树的边结构也不公开。

给定了一组**受限结点**集合 S = {{{restricted_nodes}}}，这些结点**不可进行删除观测**。其余结点为**普通结点**，可以进行删除观测。

注意：每次删除观测后，树会**立即复原**，所有操作都在完整的树上进行。

你的目标是通过查询推断出一个**通用规律**：从结点的结构信息（如子结点数、是否为根）映射到"删除该结点后图的连通分量数"。最终，你需要对所有受限结点正确预测删除后的连通分量数。

1. **删除观测**（仅限普通结点 i 不在 S 中）：
   查询删除结点 i 后，图会分成多少个连通分量。

2. **子结点数查询**（任意结点 i）：
   查询以当前固定根为方向时，结点 i 的直接子结点个数。

3. **根判定查询**（任意结点 i）：
   查询结点 i 是否为根结点。

4. **规律声明**：
   当你认为已经找到通用规律时，可以声明你的规律公式。

5. **规律自测**（仅限普通结点 j 不在 S 中）：
   在声明规律后，可以先预测某个普通结点的删除结果，系统会告诉你预测是否正确。

6. **目标预测**（仅限受限结点 i 在 S 中）：
   对受限结点预测删除后的连通分量数。

- 在首次规律声明前，必须至少完成 **3 个不同结点**的完整样本采集（每个结点需要同时获得删除结果、子结点数和是否为根的信息）。
- 在规律声明后，需要在至少 **2 个此前未做过删除观测的普通结点**上执行自测（先预测，再验证）。
- 查询总数（删除观测 + 结构查询）不得超过 **{max_queries}** 次。

每次只能包含一个操作标签。使用以下 XML 格式：

- 删除观测（例如删除结点 5）：
<query_delete>5</query_delete>

- 子结点数查询（例如查询结点 3）：
<query_children>3</query_children>

- 根判定查询（例如查询结点 2）：
<query_isroot>2</query_isroot>

- 规律声明（用自然语言描述你的规律）：
<declare_rule>你的规律描述</declare_rule>

- 规律自测（例如预测结点 4 删除后有 3 个连通分量）：
<test>node=4, predicted=3</test>

- 目标预测（例如预测受限结点 7 删除后有 2 个连通分量）：
<predict>node=7, predicted=2</predict>

- 最终答案提交（对所有受限结点的预测）：
<answer>节点号:连通分量数, 节点号:连通分量数</answer>

- **成功**：在至少声明一次规律后，对 S 中所有结点的预测均正确。
- **失败**：
  - 对 S 中的结点预测累计出错 2 次；
  - 或查询总数超过 {max_queries} 次。
"""

    game_rule_en = """\
Let's play a "Tree Deletion Rule Inference" game. Here are the rules:

The game involves a fixed undirected tree with {n} nodes numbered from 1 to {n}. I have secretly designated a root node (fixed but not disclosed), and the edge structure is also hidden.

A set of **restricted nodes** S = {{{restricted_nodes}}} is given. These nodes **cannot be deleted for observation**. The remaining nodes are **normal nodes** that can be deleted for observation.

Note: After each deletion observation, the tree is **immediately restored**. All operations are performed on the complete tree.

Your goal is to infer a **universal rule** through queries: mapping from a node's structural information (such as number of children, whether it is the root) to "the number of connected components after deleting that node". Finally, you need to correctly predict the number of connected components after deletion for all restricted nodes.

1. **Delete Observation** (only for normal nodes i not in S):
   Query how many connected components the graph splits into after deleting node i.

2. **Children Count Query** (any node i):
   Query the number of direct children of node i when oriented from the current fixed root.

3. **Root Check Query** (any node i):
   Query whether node i is the root node.

4. **Rule Declaration**:
   When you think you have found the universal rule, you can declare your rule formula.

5. **Rule Self-Test** (only for normal nodes j not in S):
   After declaring a rule, you can first predict the deletion result of a normal node, and the system will tell you if the prediction is correct.

6. **Target Prediction** (only for restricted nodes i in S):
   Predict the number of connected components after deletion for restricted nodes.

- Before the first rule declaration, you must complete sample collection for at least **3 different nodes** (each node needs deletion result, children count, and root status).
- After rule declaration, you must perform self-tests on at least **2 normal nodes that have not been deletion-observed before** (predict first, then verify).
- Total number of queries (deletion observations + structural queries) must not exceed **{max_queries}**.

Each query must contain only one operation tag. Use the following XML format:

- Delete Observation (e.g., delete node 5):
<query_delete>5</query_delete>

- Children Count Query (e.g., query node 3):
<query_children>3</query_children>

- Root Check Query (e.g., query node 2):
<query_isroot>2</query_isroot>

- Rule Declaration (describe your rule in natural language):
<declare_rule>Your rule description</declare_rule>

- Rule Self-Test (e.g., predict node 4 has 3 components after deletion):
<test>node=4, predicted=3</test>

- Target Prediction (e.g., predict restricted node 7 has 2 components after deletion):
<predict>node=7, predicted=2</predict>

- Final Answer Submission (predictions for all restricted nodes):
<answer>node:components, node:components</answer>

- **Success**: After at least one rule declaration, all predictions for nodes in S are correct.
- **Failure**:
  - Cumulative 2 incorrect predictions for nodes in S;
  - Or total number of queries exceeds {max_queries}.
"""

    contextualized_rule_zh_1 = """\
欢迎来到交通规划调度中心。我们现在来进行一次"路网封锁规律推演"，规则如下：

系统设定了一个包含 {n} 个交通枢纽（结点编号为 1 到 {n}）的树状交通网。我们已为该路网秘密指定了一个总指挥中心（即固定的根结点），且道路的边结构不对外公开。

给定了一组**重点保护枢纽**集合 S = {{{restricted_nodes}}}，这些枢纽**不可进行封锁观测**（即删除观测）。其余枢纽为**普通枢纽**，可以进行封锁观测。

注意：每次封锁观测后，路网会**立即复原**，所有操作都在完整的交通网上进行。

你的目标是通过查询推断出一个**通用规律**：从枢纽的结构信息（如下级枢纽数、是否为总指挥中心）映射到"封锁该枢纽后，路网分裂成的独立交通子网（连通分量）数"。最终，你需要对所有重点保护枢纽正确预测封锁后的独立交通子网数。

1. **封锁观测**（即删除观测，仅限普通枢纽 i 不在 S 中）：
   查询封锁（删除）枢纽 i 后，交通网会分成多少个独立交通子网。

2. **下级枢纽数查询**（即子结点查询，任意枢纽 i）：
   查询以总指挥中心为方向时，枢纽 i 的直接下级枢纽个数。

3. **总指挥中心判定**（即根判定，任意枢纽 i）：
   查询枢纽 i 是否为总指挥中心（根结点）。

4. **规律声明**：
   当你认为已经找到通用规律时，可以声明你的规律公式。

5. **规律自测**（仅限普通枢纽 j 不在 S 中）：
   在声明规律后，可以先预测某个普通枢纽封锁后的结果，系统会告诉你预测是否正确。

6. **目标预测**（仅限重点保护枢纽 i 在 S 中）：
   对重点保护枢纽预测封锁后的独立交通子网数。

- 在首次规律声明前，必须至少完成 **3 个不同枢纽**的完整样本采集（每个枢纽需要同时获得封锁结果、下级枢纽数和是否为总指挥中心的信息）。
- 在规律声明后，需要在至少 **2 个此前未做过封锁观测的普通枢纽**上执行自测（先预测，再验证）。
- 查询总数（封锁观测 + 结构查询）不得超过 **{max_queries}** 次。

每次只能包含一个操作标签。使用以下 XML 格式：

- 封锁观测（例如封锁枢纽 5）：
<query_delete>5</query_delete>

- 下级枢纽数查询（例如查询枢纽 3）：
<query_children>3</query_children>

- 总指挥中心判定（例如查询枢纽 2）：
<query_isroot>2</query_isroot>

- 规律声明（用自然语言描述你的规律）：
<declare_rule>你的规律描述</declare_rule>

- 规律自测（例如预测枢纽 4 封锁后有 3 个交通子网）：
<test>node=4, predicted=3</test>

- 目标预测（例如预测重点保护枢纽 7 封锁后有 2 个交通子网）：
<predict>node=7, predicted=2</predict>

- 最终答案提交（对所有受限结点的预测）：
<answer>节点号:连通分量数, 节点号:连通分量数</answer>

- **成功**：在至少声明一次规律后，对 S 中所有枢纽的预测均正确。
- **失败**：
  - 对 S 中的枢纽预测累计出错 2 次；
  - 或查询总数超过 {max_queries} 次。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Traffic Network Planning Center. Let's perform a "Traffic Hub Blockade Rule Inference". Here are the rules:

The system models a tree-shaped traffic network containing {n} traffic hubs (nodes numbered from 1 to {n}). I have secretly designated a general command center (a fixed root node) for this network, and the edge structure of the roads is not disclosed.

A set of **highly protected hubs** S = {{{restricted_nodes}}} is given. These hubs **cannot be subjected to blockade observation** (i.e., deletion observation). The remaining hubs are **normal hubs** that can be blockaded for observation.

Note: After each blockade observation, the traffic network is **immediately restored**. All operations are performed on the complete network.

Your goal is to infer a **universal rule** through queries: mapping from a hub's structural information (such as the number of subordinate hubs, whether it is the command center) to "the number of independent traffic subnets (connected components) the network splits into after blockading that hub". Finally, you need to correctly predict the number of independent traffic subnets after blockading for all highly protected hubs.

1. **Blockade Observation** (Deletion Observation, only for normal hubs i not in S):
   Query how many independent traffic subnets the network splits into after blockading (deleting) hub i.

2. **Subordinate Hubs Count Query** (Children Count Query, any hub i):
   Query the number of direct subordinate hubs of hub i when oriented from the general command center.

3. **Command Center Check** (Root Check Query, any hub i):
   Query whether hub i is the general command center (root node).

4. **Rule Declaration**:
   When you think you have found the universal rule, you can declare your rule formula.

5. **Rule Self-Test** (only for normal hubs j not in S):
   After declaring a rule, you can first predict the blockade result of a normal hub, and the system will tell you if the prediction is correct.

6. **Target Prediction** (only for highly protected hubs i in S):
   Predict the number of independent traffic subnets after blockading highly protected hubs.

- Before the first rule declaration, you must complete sample collection for at least **3 different hubs** (each hub needs blockade result, subordinate hubs count, and command center status).
- After rule declaration, you must perform self-tests on at least **2 normal hubs that have not been blockade-observed before** (predict first, then verify).
- Total number of queries (blockade observations + structural queries) must not exceed **{max_queries}**.

Each query must contain only one operation tag. Use the following XML format:

- Blockade Observation (e.g., blockade hub 5):
<query_delete>5</query_delete>

- Subordinate Hubs Count Query (e.g., query hub 3):
<query_children>3</query_children>

- Command Center Check (e.g., query hub 2):
<query_isroot>2</query_isroot>

- Rule Declaration (describe your rule in natural language):
<declare_rule>Your rule description</declare_rule>

- Rule Self-Test (e.g., predict hub 4 yields 3 subnets after blockade):
<test>node=4, predicted=3</test>

- Target Prediction (e.g., predict protected hub 7 yields 2 subnets after blockade):
<predict>node=7, predicted=2</predict>

- Final Answer Submission (predictions for all restricted nodes):
<answer>node:components, node:components</answer>

- **Success**: After at least one rule declaration, all predictions for hubs in S are correct.
- **Failure**:
  - Cumulative 2 incorrect predictions for hubs in S;
  - Or total number of queries exceeds {max_queries}.
"""

    contextualized_rule_zh_2 = """\
欢迎来到疾病控制中心。我们现在来进行一次"传染病隔离干预规律推演"，规则如下：

系统记录了一条包含 {n} 个感染者（结点编号为 1 到 {n}）的树状接触追踪链。我们已秘密确认了零号病人（即固定的根结点），且接触传播的边结构不对外公开。

给定了一组**脆弱群体感染者**集合 S = {{{restricted_nodes}}}，这些感染者**不可进行隔离干预观测**（即删除观测）。其余为**普通感染者**，可以进行隔离干预观测。

注意：每次隔离干预观测后，传播链会**立即复原**（推演模拟），所有操作都在完整的传播网上进行。

你的目标是通过查询推断出一个**通用规律**：从感染者的结构信息（如直接传染的下线人数、是否为零号病人）映射到"隔离该感染者后，传播链断裂成的独立感染集群（连通分量）数"。最终，你需要对所有脆弱群体感染者正确预测隔离干预后的独立感染集群数。

1. **隔离观测**（即删除观测，仅限普通感染者 i 不在 S 中）：
   查询隔离（删除）感染者 i 后，传播链会分成多少个独立的感染集群。

2. **下线感染数查询**（即子结点查询，任意感染者 i）：
   查询以零号病人为溯源起点时，感染者 i 直接传染的下线人数。

3. **零号病人判定**（即根判定，任意感染者 i）：
   查询感染者 i 是否为零号病人（根结点）。

4. **规律声明**：
   当你认为已经找到通用规律时，可以声明你的规律公式。

5. **规律自测**（仅限普通感染者 j 不在 S 中）：
   在声明规律后，可以先预测某个普通感染者隔离后的结果，系统会告诉你预测是否正确。

6. **目标预测**（仅限脆弱群体感染者 i 在 S 中）：
   对脆弱群体感染者预测隔离后的独立感染集群数。

- 在首次规律声明前，必须至少完成 **3 个不同感染者**的完整样本采集（每个感染者需要同时获得隔离结果、下线人数和是否为零号病人的信息）。
- 在规律声明后，需要在至少 **2 个此前未做过隔离观测的普通感染者**上执行自测（先预测，再验证）。
- 查询总数（隔离观测 + 结构查询）不得超过 **{max_queries}** 次。

每次只能包含一个操作标签。使用以下 XML 格式：

- 隔离观测（例如隔离感染者 5）：
<query_delete>5</query_delete>

- 下线感染数查询（例如查询感染者 3）：
<query_children>3</query_children>

- 零号病人判定（例如查询感染者 2）：
<query_isroot>2</query_isroot>

- 规律声明（用自然语言描述你的规律）：
<declare_rule>你的规律描述</declare_rule>

- 规律自测（例如预测感染者 4 隔离后有 3 个感染集群）：
<test>node=4, predicted=3</test>

- 目标预测（例如预测脆弱群体感染者 7 隔离后有 2 个感染集群）：
<predict>node=7, predicted=2</predict>

- 最终答案提交（对所有受限结点的预测）：
<answer>节点号:连通分量数, 节点号:连通分量数</answer>

- **成功**：在至少声明一次规律后，对 S 中所有感染者的预测均正确。
- **失败**：
  - 对 S 中的感染者预测累计出错 2 次；
  - 或查询总数超过 {max_queries} 次。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Disease Control Center. Let's perform an "Infection Isolation Intervention Rule Inference". Here are the rules:

The system records a tree-shaped contact tracing chain containing {n} infected individuals (nodes numbered from 1 to {n}). We have secretly confirmed Patient Zero (the fixed root node), and the edge structure of transmission is not disclosed.

A set of **vulnerable group infected** S = {{{restricted_nodes}}} is given. These individuals **cannot be subjected to isolation intervention observation** (i.e., deletion observation). The remaining are **normal infected**, which can be subjected to isolation intervention observation.

Note: After each isolation intervention observation, the transmission chain is **immediately restored** (as this is a simulation). All operations are performed on the complete transmission network.

Your goal is to infer a **universal rule** through queries: mapping from an infected individual's structural information (such as the number of directly infected subordinates, whether they are Patient Zero) to "the number of independent infection clusters (connected components) the transmission chain breaks into after isolating that individual". Finally, you need to correctly predict the number of independent infection clusters after isolation for all vulnerable group infected.

1. **Isolation Observation** (Deletion Observation, only for normal infected i not in S):
   Query how many independent infection clusters the network splits into after isolating (deleting) infected i.

2. **Subordinate Infected Count Query** (Children Count Query, any infected i):
   Query the number of direct subordinate infected of individual i when oriented from Patient Zero.

3. **Patient Zero Check** (Root Check Query, any infected i):
   Query whether infected i is Patient Zero (root node).

4. **Rule Declaration**:
   When you think you have found the universal rule, you can declare your rule formula.

5. **Rule Self-Test** (only for normal infected j not in S):
   After declaring a rule, you can first predict the isolation result of a normal infected, and the system will tell you if the prediction is correct.

6. **Target Prediction** (only for vulnerable group infected i in S):
   Predict the number of independent infection clusters after isolation for vulnerable group infected.

- Before the first rule declaration, you must complete sample collection for at least **3 different infected individuals** (each needs isolation result, subordinate infected count, and Patient Zero status).
- After rule declaration, you must perform self-tests on at least **2 normal infected that have not been isolation-observed before** (predict first, then verify).
- Total number of queries (isolation observations + structural queries) must not exceed **{max_queries}**.

Each query must contain only one operation tag. Use the following XML format:

- Isolation Observation (e.g., isolate infected 5):
<query_delete>5</query_delete>

- Subordinate Infected Count Query (e.g., query infected 3):
<query_children>3</query_children>

- Patient Zero Check (e.g., query infected 2):
<query_isroot>2</query_isroot>

- Rule Declaration (describe your rule in natural language):
<declare_rule>Your rule description</declare_rule>

- Rule Self-Test (e.g., predict infected 4 yields 3 clusters after isolation):
<test>node=4, predicted=3</test>

- Target Prediction (e.g., predict vulnerable infected 7 yields 2 clusters after isolation):
<predict>node=7, predicted=2</predict>

- Final Answer Submission (predictions for all restricted nodes):
<answer>node:components, node:components</answer>

- **Success**: After at least one rule declaration, all predictions for infected in S are correct.
- **Failure**:
  - Cumulative 2 incorrect predictions for infected in S;
  - Or total number of queries exceeds {max_queries}.
"""

    contextualized_rule_zh_3 = """\
欢迎来到知识图谱学习系统。我们现在来进行一次"知识体系移除规律推演"，规则如下：

系统设定了一个包含 {n} 个知识点（结点编号为 1 到 {n}）的树状知识依赖网。我们已为该体系秘密指定了一个核心基础知识点（即固定的根结点），且依赖关系边结构不对外公开。

给定了一组**必修核心考点**集合 S = {{{restricted_nodes}}}，这些考点**不可进行移除观测**（即删除观测）。其余知识点为**普通知识点**，可以进行移除观测。

注意：每次移除观测后，知识网会**立即复原**，所有操作都在完整的知识体系上进行。

你的目标是通过查询推断出一个**通用规律**：从知识点的结构信息（如直接后置知识点数、是否为核心基础）映射到"移除该知识点后，体系分裂成的独立知识孤岛（连通分量）数"。最终，你需要对所有必修核心考点正确预测移除后的独立知识孤岛数。

1. **移除观测**（即删除观测，仅限普通知识点 i 不在 S 中）：
   查询移除（删除）知识点 i 后，知识体系会分成多少个独立的知识孤岛。

2. **后置知识点数查询**（即子结点查询，任意知识点 i）：
   查询以核心基础知识点为起点方向时，知识点 i 的直接后置知识点个数。

3. **核心基础判定**（即根判定，任意知识点 i）：
   查询知识点 i 是否为核心基础知识点（根结点）。

4. **规律声明**：
   当你认为已经找到通用规律时，可以声明你的规律公式。

5. **规律自测**（仅限普通知识点 j 不在 S 中）：
   在声明规律后，可以先预测某个普通知识点移除后的结果，系统会告诉你预测是否正确。

6. **目标预测**（仅限必修核心考点 i 在 S 中）：
   对必修核心考点预测移除后的独立知识孤岛数。

- 在首次规律声明前，必须至少完成 **3 个不同知识点**的完整样本采集（每个知识点需要同时获得移除结果、后置知识点数和是否为核心基础的信息）。
- 在规律声明后，需要在至少 **2 个此前未做过移除观测的普通知识点**上执行自测（先预测，再验证）。
- 查询总数（移除观测 + 结构查询）不得超过 **{max_queries}** 次。

每次只能包含一个操作标签。使用以下 XML 格式：

- 移除观测（例如移除知识点 5）：
<query_delete>5</query_delete>

- 后置知识点数查询（例如查询知识点 3）：
<query_children>3</query_children>

- 核心基础判定（例如查询知识点 2）：
<query_isroot>2</query_isroot>

- 规律声明（用自然语言描述你的规律）：
<declare_rule>你的规律描述</declare_rule>

- 规律自测（例如预测知识点 4 移除后有 3 个知识孤岛）：
<test>node=4, predicted=3</test>

- 目标预测（例如预测核心考点 7 移除后有 2 个知识孤岛）：
<predict>node=7, predicted=2</predict>

- 最终答案提交（对所有受限结点的预测）：
<answer>节点号:连通分量数, 节点号:连通分量数</answer>

- **成功**：在至少声明一次规律后，对 S 中所有知识点的预测均正确。
- **失败**：
  - 对 S 中的知识点预测累计出错 2 次；
  - 或查询总数超过 {max_queries} 次。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Knowledge Graph Learning System. Let's perform a "Knowledge Dependency Removal Rule Inference". Here are the rules:

The system contains a tree-shaped knowledge dependency network with {n} knowledge points (nodes numbered from 1 to {n}). We have secretly designated a core foundational point (the fixed root node), and the dependency edge structure is not disclosed.

A set of **mandatory core exam points** S = {{{restricted_nodes}}} is given. These points **cannot be subjected to removal observation** (i.e., deletion observation). The remaining are **normal knowledge points**, which can be subjected to removal observation.

Note: After each removal observation, the knowledge network is **immediately restored**. All operations are performed on the complete network.

Your goal is to infer a **universal rule** through queries: mapping from a knowledge point's structural information (such as the number of direct subsequent points, whether it is the core foundational point) to "the number of independent knowledge islands (connected components) the network splits into after removing that point". Finally, you need to correctly predict the number of independent knowledge islands after removal for all mandatory core exam points.

1. **Removal Observation** (Deletion Observation, only for normal points i not in S):
   Query how many independent knowledge islands the network splits into after removing (deleting) point i.

2. **Subsequent Points Count Query** (Children Count Query, any point i):
   Query the number of direct subsequent knowledge points of point i when oriented from the core foundational point.

3. **Core Foundational Check** (Root Check Query, any point i):
   Query whether point i is the core foundational point (root node).

4. **Rule Declaration**:
   When you think you have found the universal rule, you can declare your rule formula.

5. **Rule Self-Test** (only for normal points j not in S):
   After declaring a rule, you can first predict the removal result of a normal point, and the system will tell you if the prediction is correct.

6. **Target Prediction** (only for mandatory core exam points i in S):
   Predict the number of independent knowledge islands after removal for mandatory core exam points.

- Before the first rule declaration, you must complete sample collection for at least **3 different points** (each needs removal result, subsequent points count, and core foundational status).
- After rule declaration, you must perform self-tests on at least **2 normal points that have not been removal-observed before** (predict first, then verify).
- Total number of queries (removal observations + structural queries) must not exceed **{max_queries}**.

Each query must contain only one operation tag. Use the following XML format:

- Removal Observation (e.g., remove knowledge point 5):
<query_delete>5</query_delete>

- Subsequent Points Count Query (e.g., query point 3):
<query_children>3</query_children>

- Core Foundational Check (e.g., query point 2):
<query_isroot>2</query_isroot>

- Rule Declaration (describe your rule in natural language):
<declare_rule>Your rule description</declare_rule>

- Rule Self-Test (e.g., predict point 4 yields 3 islands after removal):
<test>node=4, predicted=3</test>

- Target Prediction (e.g., predict core exam point 7 yields 2 islands after removal):
<predict>node=7, predicted=2</predict>

- Final Answer Submission (predictions for all restricted nodes):
<answer>node:components, node:components</answer>

- **Success**: After at least one rule declaration, all predictions for points in S are correct.
- **Failure**:
  - Cumulative 2 incorrect predictions for points in S;
  - Or total number of queries exceeds {max_queries}.
"""

    contextualized_rule_zh_4 = """\
欢迎来到工业供应链规划部。我们现在来进行一次"供应链装配停机规律推演"，规则如下：

系统设定了一个包含 {n} 个生产工序节点（结点编号为 1 到 {n}）的树状供应链装配网。我们已秘密指定了一个最终总装节点（即固定的根结点），且装配依赖的边结构不对外公开。

给定了一组**核心瓶颈工序**集合 S = {{{restricted_nodes}}}，这些工序**不可进行停机阻断观测**（即删除观测）。其余为**普通工序**，可以进行停机阻断观测。

注意：每次停机阻断观测后，供应链网络会**立即复原**，所有操作都在完整的生产装配网上进行。

你的目标是通过查询推断出一个**通用规律**：从工序的结构信息（如直接下游工序数、是否为最终总装节点）映射到"停机阻断该工序后，供应链断裂成的独立生产子网（连通分量）数"。最终，你需要对所有核心瓶颈工序正确预测停机阻断后的独立生产子网数。

1. **停机阻断观测**（即删除观测，仅限普通工序 i 不在 S 中）：
   查询停机阻断（删除）工序 i 后，供应链会分成多少个独立的生产子网。

2. **下游工序数查询**（即子结点查询，任意工序 i）：
   查询以最终总装节点为汇聚方向时，工序 i 的直接下游工序个数。

3. **最终总装判定**（即根判定，任意工序 i）：
   查询工序 i 是否为最终总装节点（根结点）。

4. **规律声明**：
   当你认为已经找到通用规律时，可以声明你的规律公式。

5. **规律自测**（仅限普通工序 j 不在 S 中）：
   在声明规律后，可以先预测某个普通工序停机后的结果，系统会告诉你预测是否正确。

6. **目标预测**（仅限核心瓶颈工序 i 在 S 中）：
   对核心瓶颈工序预测停机阻断后的独立生产子网数。

- 在首次规律声明前，必须至少完成 **3 个不同工序**的完整样本采集（每个工序需要同时获得停机结果、下游工序数和是否为最终总装的信息）。
- 在规律声明后，需要在至少 **2 个此前未做过停机阻断观测的普通工序**上执行自测（先预测，再验证）。
- 查询总数（停机阻断观测 + 结构查询）不得超过 **{max_queries}** 次。

每次只能包含一个操作标签。使用以下 XML 格式：

- 停机阻断观测（例如停机工序 5）：
<query_delete>5</query_delete>

- 下游工序数查询（例如查询工序 3）：
<query_children>3</query_children>

- 最终总装判定（例如查询工序 2）：
<query_isroot>2</query_isroot>

- 规律声明（用自然语言描述你的规律）：
<declare_rule>你的规律描述</declare_rule>

- 规律自测（例如预测工序 4 停机后有 3 个生产子网）：
<test>node=4, predicted=3</test>

- 目标预测（例如预测核心瓶颈工序 7 停机后有 2 个生产子网）：
<predict>node=7, predicted=2</predict>

- 最终答案提交（对所有受限结点的预测）：
<answer>节点号:连通分量数, 节点号:连通分量数</answer>

- **成功**：在至少声明一次规律后，对 S 中所有工序的预测均正确。
- **失败**：
  - 对 S 中的工序预测累计出错 2 次；
  - 或查询总数超过 {max_queries} 次。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Industrial Supply Chain Planning Department. Let's perform a "Supply Chain Assembly Downtime Rule Inference". Here are the rules:

The system models a tree-shaped supply chain assembly network containing {n} production process nodes (nodes numbered from 1 to {n}). We have secretly designated a final assembly node (the fixed root node), and the assembly dependency edge structure is not disclosed.

A set of **core bottleneck processes** S = {{{restricted_nodes}}} is given. These processes **cannot be subjected to downtime blockade observation** (i.e., deletion observation). The remaining are **normal processes**, which can be subjected to downtime blockade observation.

Note: After each downtime blockade observation, the supply chain network is **immediately restored**. All operations are performed on the complete network.

Your goal is to infer a **universal rule** through queries: mapping from a process's structural information (such as the number of direct downstream processes, whether it is the final assembly node) to "the number of independent production subnets (connected components) the supply chain breaks into after halting that process". Finally, you need to correctly predict the number of independent production subnets after downtime for all core bottleneck processes.

1. **Downtime Blockade Observation** (Deletion Observation, only for normal processes i not in S):
   Query how many independent production subnets the network splits into after halting (deleting) process i.

2. **Downstream Processes Count Query** (Children Count Query, any process i):
   Query the number of direct downstream processes of process i when oriented towards the final assembly node.

3. **Final Assembly Check** (Root Check Query, any process i):
   Query whether process i is the final assembly node (root node).

4. **Rule Declaration**:
   When you think you have found the universal rule, you can declare your rule formula.

5. **Rule Self-Test** (only for normal processes j not in S):
   After declaring a rule, you can first predict the downtime result of a normal process, and the system will tell you if the prediction is correct.

6. **Target Prediction** (only for core bottleneck processes i in S):
   Predict the number of independent production subnets after downtime for core bottleneck processes.

- Before the first rule declaration, you must complete sample collection for at least **3 different processes** (each needs downtime result, downstream processes count, and final assembly status).
- After rule declaration, you must perform self-tests on at least **2 normal processes that have not been downtime-observed before** (predict first, then verify).
- Total number of queries (downtime observations + structural queries) must not exceed **{max_queries}**.

Each query must contain only one operation tag. Use the following XML format:

- Downtime Blockade Observation (e.g., stop process 5):
<query_delete>5</query_delete>

- Downstream Processes Count Query (e.g., query process 3):
<query_children>3</query_children>

- Final Assembly Check (e.g., query process 2):
<query_isroot>2</query_isroot>

- Rule Declaration (describe your rule in natural language):
<declare_rule>Your rule description</declare_rule>

- Rule Self-Test (e.g., predict process 4 yields 3 subnets after downtime):
<test>node=4, predicted=3</test>

- Target Prediction (e.g., predict core bottleneck process 7 yields 2 subnets after downtime):
<predict>node=7, predicted=2</predict>

- Final Answer Submission (predictions for all restricted nodes):
<answer>node:components, node:components</answer>

- **Success**: After at least one rule declaration, all predictions for processes in S are correct.
- **Failure**:
  - Cumulative 2 incorrect predictions for processes in S;
  - Or total number of queries exceeds {max_queries}.
"""

    contextualized_rule_zh_5 = """\
欢迎来到案件卷宗分析系统。我们现在来进行一次"证据链排除规律推演"，规则如下：

系统设定了一个包含 {n} 个证据节点（结点编号为 1 到 {n}）的树状证据依赖网。我们已为该证据链秘密指定了一个核心主证（即固定的根结点），且证据依赖的边结构不对外公开。

给定了一组**关键不可推翻物证**集合 S = {{{restricted_nodes}}}，这些证据**不可进行证据排除观测**（即删除观测）。其余为**普通证据**，可以进行证据排除观测。

注意：每次证据排除观测后，证据网络会**立即复原**（由于是逻辑推演），所有操作都在完整的证据网上进行。

你的目标是通过查询推断出一个**通用规律**：从证据节点的结构信息（如直接衍生的证据数、是否为核心主证）映射到"排除该证据后，整个证据链断裂成的独立证据闭环（连通分量）数"。最终，你需要对所有关键不可推翻物证正确预测排除后的独立证据闭环数。

1. **证据排除观测**（即删除观测，仅限普通证据 i 不在 S 中）：
   查询排除（删除）证据 i 后，证据网会分成多少个独立的证据闭环。

2. **衍生证据数查询**（即子结点查询，任意证据 i）：
   查询以核心主证为根基方向时，证据 i 的直接衍生证据个数。

3. **核心主证判定**（即根判定，任意证据 i）：
   查询证据 i 是否为核心主证（根结点）。

4. **规律声明**：
   当你认为已经找到通用规律时，可以声明你的规律公式。

5. **规律自测**（仅限普通证据 j 不在 S 中）：
   在声明规律后，可以先预测某个普通证据排除后的结果，系统会告诉你预测是否正确。

6. **目标预测**（仅限关键不可推翻物证 i 在 S 中）：
   对关键物证预测排除后的独立证据闭环数。

- 在首次规律声明前，必须至少完成 **3 个不同证据**的完整样本采集（每个证据需要同时获得排除结果、衍生证据数和是否为核心主证的信息）。
- 在规律声明后，需要在至少 **2 个此前未做过排除观测的普通证据**上执行自测（先预测，再验证）。
- 查询总数（排除观测 + 结构查询）不得超过 **{max_queries}** 次。

每次只能包含一个操作标签。使用以下 XML 格式：

- 证据排除观测（例如排除证据 5）：
<query_delete>5</query_delete>

- 衍生证据数查询（例如查询证据 3）：
<query_children>3</query_children>

- 核心主证判定（例如查询证据 2）：
<query_isroot>2</query_isroot>

- 规律声明（用自然语言描述你的规律）：
<declare_rule>你的规律描述</declare_rule>

- 规律自测（例如预测证据 4 排除后有 3 个证据闭环）：
<test>node=4, predicted=3</test>

- 目标预测（例如预测关键物证 7 排除后有 2 个证据闭环）：
<predict>node=7, predicted=2</predict>

- 最终答案提交（对所有受限结点的预测）：
<answer>节点号:连通分量数, 节点号:连通分量数</answer>

- **成功**：在至少声明一次规律后，对 S 中所有证据的预测均正确。
- **失败**：
  - 对 S 中的证据预测累计出错 2 次；
  - 或查询总数超过 {max_queries} 次。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Case File Analysis System. Let's perform an "Evidence Chain Exclusion Rule Inference". Here are the rules:

The system features a tree-shaped evidence dependency network containing {n} evidence nodes (nodes numbered from 1 to {n}). We have secretly designated a core primary evidence (the fixed root node), and the dependency edge structure of the evidence is not disclosed.

A set of **key irrefutable evidence** S = {{{restricted_nodes}}} is given. These evidence nodes **cannot be subjected to exclusion observation** (i.e., deletion observation). The remaining are **normal evidence**, which can be subjected to exclusion observation.

Note: After each exclusion observation, the evidence chain is **immediately restored**. All operations are performed on the complete network.

Your goal is to infer a **universal rule** through queries: mapping from an evidence's structural information (such as the number of direct derivative evidence, whether it is the core primary evidence) to "the number of independent evidence loops (connected components) the chain breaks into after excluding that evidence". Finally, you need to correctly predict the number of independent evidence loops after exclusion for all key irrefutable evidence.

1. **Exclusion Observation** (Deletion Observation, only for normal evidence i not in S):
   Query how many independent evidence loops the network splits into after excluding (deleting) evidence i.

2. **Derivative Evidence Count Query** (Children Count Query, any evidence i):
   Query the number of direct derivative evidence of evidence i when oriented from the core primary evidence.

3. **Core Primary Check** (Root Check Query, any evidence i):
   Query whether evidence i is the core primary evidence (root node).

4. **Rule Declaration**:
   When you think you have found the universal rule, you can declare your rule formula.

5. **Rule Self-Test** (only for normal evidence j not in S):
   After declaring a rule, you can first predict the exclusion result of normal evidence, and the system will tell you if the prediction is correct.

6. **Target Prediction** (only for key irrefutable evidence i in S):
   Predict the number of independent evidence loops after exclusion for key irrefutable evidence.

- Before the first rule declaration, you must complete sample collection for at least **3 different evidence nodes** (each needs exclusion result, derivative evidence count, and core primary status).
- After rule declaration, you must perform self-tests on at least **2 normal evidence nodes that have not been exclusion-observed before** (predict first, then verify).
- Total number of queries (exclusion observations + structural queries) must not exceed **{max_queries}**.

Each query must contain only one operation tag. Use the following XML format:

- Exclusion Observation (e.g., exclude evidence 5):
<query_delete>5</query_delete>

- Derivative Evidence Count Query (e.g., query evidence 3):
<query_children>3</query_children>

- Core Primary Check (e.g., query evidence 2):
<query_isroot>2</query_isroot>

- Rule Declaration (describe your rule in natural language):
<declare_rule>Your rule description</declare_rule>

- Rule Self-Test (e.g., predict evidence 4 yields 3 evidence loops after exclusion):
<test>node=4, predicted=3</test>

- Target Prediction (e.g., predict key evidence 7 yields 2 evidence loops after exclusion):
<predict>node=7, predicted=2</predict>

- Final Answer Submission (predictions for all restricted nodes):
<answer>node:components, node:components</answer>

- **Success**: After at least one rule declaration, all predictions for evidence in S are correct.
- **Failure**:
  - Cumulative 2 incorrect predictions for evidence in S;
  - Or total number of queries exceeds {max_queries}.
"""

    tags = ["query_delete", "query_children", "query_isroot", "declare_rule", "test", "predict", "answer"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "root": 3,
                "restricted": [1, 5],
                "max_queries": 15,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (5, 6), (5, 7)],
                "root": 1,
                "restricted": [6, 7],
                "max_queries": 21,
            },
            3: {
                "n": 9,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8), (7, 9)],
                "root": 1,
                "restricted": [4, 8, 9],
                "max_queries": 27,
            },
            4: {
                "n": 10,
                "edges": [(5, 1), (5, 2), (2, 3), (2, 4), (5, 6), (6, 7), (6, 8), (8, 9), (8, 10)],
                "root": 5,
                "restricted": [1, 3, 9, 10],
                "max_queries": 30,
            },
            5: {
                "n": 12,
                "edges": [(6, 1), (6, 2), (6, 3), (2, 4), (2, 5), (3, 7), (3, 8), (8, 9), (8, 10), (10, 11), (10, 12)],
                "root": 6,
                "restricted": [1, 4, 5, 9, 11, 12],
                "max_queries": 36,
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "root": 3,
                "restricted": [1, 5],
                "max_queries": 15,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (1, 4), (1, 5), (5, 6), (5, 7)],
                "root": 1,
                "restricted": [6, 7],
                "max_queries": 21,
            },
            3: {
                "n": 9,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8), (7, 9)],
                "root": 1,
                "restricted": [4, 8, 9],
                "max_queries": 27,
            },
            4: {
                "n": 10,
                "edges": [(5, 1), (5, 2), (2, 3), (2, 4), (5, 6), (6, 7), (6, 8), (8, 9), (8, 10)],
                "root": 5,
                "restricted": [1, 3, 9, 10],
                "max_queries": 30,
            },
            5: {
                "n": 12,
                "edges": [(6, 1), (6, 2), (6, 3), (2, 4), (2, 5), (3, 7), (3, 8), (8, 9), (8, 10), (10, 11), (10, 12)],
                "root": 6,
                "restricted": [1, 4, 5, 9, 11, 12],
                "max_queries": 36,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.n = cfg["n"]
        self.edges = cfg["edges"]
        self.root = cfg["root"]
        self.restricted = set(cfg["restricted"])
        self.max_queries = cfg["max_queries"]
        
        self._game_info["n"] = self.n
        self._game_info["restricted_nodes"] = ",".join(map(str, sorted(self.restricted)))
        self._game_info["max_queries"] = self.max_queries
        
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self._compute_tree_structure()
        
        self._compute_delete_results()
        
        self.query_count = 0
        self.sampled_nodes = set()
        self.deleted_nodes = set()
        self.rule_declared = False
        self.tested_nodes = set()
        self.predict_errors = 0
        self.predicted_restricted = {}
        self.children_queried = set()
        self.isroot_queried = set()

    def _compute_tree_structure(self):
        self.children_count = {i: 0 for i in range(1, self.n + 1)}
        self.parent = {i: None for i in range(1, self.n + 1)}
        
        visited = set()
        queue = [self.root]
        visited.add(self.root)
        
        while queue:
            u = queue.pop(0)
            for v in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    self.parent[v] = u
                    self.children_count[u] += 1
                    queue.append(v)

    def _compute_delete_results(self):
        self.delete_result = {}
        for node in range(1, self.n + 1):
            self.delete_result[node] = len(self.adj[node])

    def evaluate(self, parsed_info):
        if "answer" in parsed_info:
            try:
                raw = parsed_info["answer"]
                pairs = [x.strip() for x in raw.split(",")]
                for pair in pairs:
                    if ":" in pair:
                        node_str, val_str = pair.split(":")
                        node = int(node_str.strip())
                        predicted = int(val_str.strip())
                        self.predicted_restricted[node] = predicted
            except Exception:
                return False

        if len(self.predicted_restricted) < len(self.restricted):
            return False
        
        for node in self.restricted:
            if node not in self.predicted_restricted:
                return False
            if self.predicted_restricted[node] != self.delete_result[node]:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        yes_str = "是" if self.config.language == "zh" else "Yes"
        no_str = "否" if self.config.language == "zh" else "No"
        error_prefix = "错误：" if self.config.language == "zh" else "Error: "
        
        is_counting_query = any(tag in parsed_info for tag in ["query_delete", "query_children", "query_isroot"])
        
        if is_counting_query and self.query_count >= self.max_queries:
            self.state.set_state("failed", "exceeded max queries")
            return error_prefix + ("查询次数超限。" if self.config.language == "zh" else "Query limit exceeded.")
        
        if "query_delete" in parsed_info:
            try:
                node = int(parsed_info["query_delete"].strip())
                if node < 1 or node > self.n:
                    return error_prefix + ("结点编号超出范围。" if self.config.language == "zh" else "Node ID out of range.")
                if node in self.restricted:
                    return error_prefix + ("该结点为受限结点，不可进行删除观测。" if self.config.language == "zh" else "This is a restricted node, cannot be deleted.")
                
                self.query_count += 1
                self.deleted_nodes.add(node)
                result = self.delete_result[node]
                
                if self.config.language == "zh":
                    return f"删除结点 {node} 后，图分成 {result} 个连通分量。树已复原。"
                else:
                    return f"After deleting node {node}, the graph splits into {result} connected components. Tree restored."
            except ValueError:
                return error_prefix + ("无效的结点编号。" if self.config.language == "zh" else "Invalid node ID.")
        
        elif "query_children" in parsed_info:
            try:
                node = int(parsed_info["query_children"].strip())
                if node < 1 or node > self.n:
                    return error_prefix + ("结点编号超出范围。" if self.config.language == "zh" else "Node ID out of range.")
                
                self.query_count += 1
                self.children_queried.add(node)
                count = self.children_count[node]
                
                if self.config.language == "zh":
                    return f"结点 {node} 有 {count} 个子结点。"
                else:
                    return f"Node {node} has {count} children."
            except ValueError:
                return error_prefix + ("无效的结点编号。" if self.config.language == "zh" else "Invalid node ID.")
        
        elif "query_isroot" in parsed_info:
            try:
                node = int(parsed_info["query_isroot"].strip())
                if node < 1 or node > self.n:
                    return error_prefix + ("结点编号超出范围。" if self.config.language == "zh" else "Node ID out of range.")
                
                self.query_count += 1
                self.isroot_queried.add(node)
                is_root = (node == self.root)
                
                return yes_str if is_root else no_str
            except ValueError:
                return error_prefix + ("无效的结点编号。" if self.config.language == "zh" else "Invalid node ID.")
        
        elif "declare_rule" in parsed_info:
            complete_nodes = self.deleted_nodes & self.children_queried & self.isroot_queried
            
            if len(complete_nodes) < 3:
                return error_prefix + ("规律声明前需要至少完成 3 个不同结点的完整样本采集（每个结点需要删除观测、子结点数查询和根判定查询）。" 
                                       if self.config.language == "zh" 
                                       else "Need at least 3 complete samples (deletion, children count, and root check for each) before declaring a rule.")
            
            self.rule_declared = True
            if self.config.language == "zh":
                return "规律已记录。现在你需要在至少 2 个未做过删除观测的普通结点上进行自测。"
            else:
                return "Rule recorded. Now you need to perform self-tests on at least 2 normal nodes that have not been deletion-observed."
        
        elif "test" in parsed_info:
            if not self.rule_declared:
                return error_prefix + ("请先声明规律。" if self.config.language == "zh" else "Please declare a rule first.")
            
            try:
                raw = parsed_info["test"]
                parts = [x.strip() for x in raw.split(",")]
                test_dict = {}
                for part in parts:
                    if "=" in part:
                        k, v = part.split("=", 1)
                        test_dict[k.strip()] = v.strip()
                
                if "node" not in test_dict or "predicted" not in test_dict:
                    raise ValueError
                
                node = int(test_dict["node"])
                predicted = int(test_dict["predicted"])
                
                if node < 1 or node > self.n:
                    return error_prefix + ("结点编号超出范围。" if self.config.language == "zh" else "Node ID out of range.")
                if node in self.restricted:
                    return error_prefix + ("该结点为受限结点，请使用 predict 标签。" if self.config.language == "zh" 
                                           else "This is a restricted node, use predict tag.")
                if node in self.deleted_nodes:
                    return error_prefix + ("该结点已进行过删除观测，请选择其他结点。" if self.config.language == "zh" 
                                           else "This node has been deletion-observed, choose another.")
                
                self.tested_nodes.add(node)
                self.deleted_nodes.add(node)
                actual = self.delete_result[node]
                
                if predicted == actual:
                    if self.config.language == "zh":
                        return f"自测正确！结点 {node} 删除后确实有 {actual} 个连通分量。"
                    else:
                        return f"Test correct! Node {node} indeed has {actual} components after deletion."
                else:
                    if self.config.language == "zh":
                        return f"自测错误。结点 {node} 删除后实际有 {actual} 个连通分量，你预测的是 {predicted}。"
                    else:
                        return f"Test incorrect. Node {node} actually has {actual} components after deletion, you predicted {predicted}."
            except (ValueError, KeyError):
                return error_prefix + ("自测格式错误。" if self.config.language == "zh" else "Invalid test format.")
        
        elif "predict" in parsed_info:
            if not self.rule_declared:
                return error_prefix + ("请先声明规律。" if self.config.language == "zh" else "Please declare a rule first.")
            
            tested_normal_count = len(self.tested_nodes)
            if tested_normal_count < 2:
                return error_prefix + ("规律声明后需要先在至少 2 个未观测的普通结点上进行自测。" if self.config.language == "zh"
                                       else "Need to perform self-tests on at least 2 unobserved normal nodes after rule declaration.")
            
            try:
                raw = parsed_info["predict"]
                parts = [x.strip() for x in raw.split(",")]
                pred_dict = {}
                for part in parts:
                    if "=" in part:
                        k, v = part.split("=", 1)
                        pred_dict[k.strip()] = v.strip()
                
                if "node" not in pred_dict or "predicted" not in pred_dict:
                    raise ValueError
                
                node = int(pred_dict["node"])
                predicted = int(pred_dict["predicted"])
                
                if node < 1 or node > self.n:
                    return error_prefix + ("结点编号超出范围。" if self.config.language == "zh" else "Node ID out of range.")
                if node not in self.restricted:
                    return error_prefix + ("该结点不是受限结点。" if self.config.language == "zh" 
                                           else "This is not a restricted node.")
                
                actual = self.delete_result[node]
                self.predicted_restricted[node] = predicted
                
                if predicted == actual:
                    if self.config.language == "zh":
                        response = f"预测正确！结点 {node} 删除后有 {actual} 个连通分量。"
                    else:
                        response = f"Prediction correct! Node {node} has {actual} components after deletion."
                    
                    if len(self.predicted_restricted) == len(self.restricted):
                        all_correct = all(
                            self.predicted_restricted[n] == self.delete_result[n]
                            for n in self.restricted
                        )
                        if all_correct:
                            self.state.set_state("success", "all predictions correct")
                    
                    return response
                else:
                    self.predict_errors += 1
                    if self.predict_errors >= 2:
                        self.state.set_state("failed", "too many prediction errors")
                        if self.config.language == "zh":
                            return f"预测错误。结点 {node} 删除后实际有 {actual} 个连通分量。预测错误次数已达上限，游戏失败。"
                        else:
                            return f"Prediction incorrect. Node {node} actually has {actual} components. Error limit reached, game failed."
                    else:
                        if self.config.language == "zh":
                            return f"预测错误。结点 {node} 删除后实际有 {actual} 个连通分量，你预测的是 {predicted}。还有 1 次预测错误的机会。"
                        else:
                            return f"Prediction incorrect. Node {node} actually has {actual} components, you predicted {predicted}. 1 error chance remaining."
            except (ValueError, KeyError):
                return error_prefix + ("预测格式错误。" if self.config.language == "zh" else "Invalid prediction format.")
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        lang = self.config.language
        
        yes_str = "是" if lang == "zh" else "Yes"
        no_str = "否" if lang == "zh" else "No"
        
        for node in range(1, self.n + 1):
            if node not in self.restricted:
                q_xml = f"<query_delete>{node}</query_delete>"
                res = self.delete_result[node]
                if lang == "zh":
                    ans = f"删除结点 {node} 后，图分成 {res} 个连通分量。树已复原。"
                else:
                    ans = f"After deleting node {node}, the graph splits into {res} connected components. Tree restored."
                queries.append({"query": q_xml, "answer": ans})

            q_xml = f"<query_children>{node}</query_children>"
            count = self.children_count[node]
            if lang == "zh":
                ans = f"结点 {node} 有 {count} 个子结点。"
            else:
                ans = f"Node {node} has {count} children."
            queries.append({"query": q_xml, "answer": ans})

            q_xml = f"<query_isroot>{node}</query_isroot>"
            is_root = (node == self.root)
            ans = yes_str if is_root else no_str
            queries.append({"query": q_xml, "answer": ans})
            
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)
        
        lang = self.config.language
        
        if lang == "zh":
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
        else:
            if correct == "Yes":
                return "No"
            if correct == "No":
                return "Yes"
        
        numbers = list(re.finditer(r'\d+', correct))
        if numbers:
            last = numbers[-1]
            val = int(last.group())
            new_val = val + 1 if val > 0 else 2
            tweaked = correct[:last.start()] + str(new_val) + correct[last.end():]
            if tweaked != correct:
                return tweaked
                
        return correct + "_WRONG"