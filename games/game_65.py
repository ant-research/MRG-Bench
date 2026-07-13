import re
from typing import List, Dict
from .base import Game


class HiddenTreeStructureGame(Game):
    # 严格保留底层逻辑及原类属性
    reasoning_type = "演绎推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"隐藏树结构"的推理游戏，规则如下：

游戏设定了一棵包含 {n} 个节点的有根树。根节点为 {root}，所有节点的标识为 {nodes}。树的边关系是固定的但对你隐藏。

术语说明：
- 对于任意节点 v，其"子树规模"定义为以 v 为根的子树中的节点总数（包括 v 自身）。
- 祖先关系是自反的，即任意节点 v 都是它自己的祖先。
- 叶节点指没有子节点的节点，其子树规模为 1。

你的目标是确定目标节点集合 {targets} 中每个节点的子树规模。

你可以通过以下三种方式向我提问（每次仅限一个问题）：

1. 祖先判定：询问节点 A 是否为节点 B 的祖先。我会回答"是"或"否"。注意：任意节点都是自己的祖先。
2. 叶子判定：询问节点 X 是否为叶节点。我会回答"是"或"否"。若为叶节点，则其子树规模为 1。
3. 双节点测量：同时测量两个节点 U 和 V 的子树规模之和。注意：U 和 V 必须互不为祖先或后代关系，否则测量无效。若有效，我会返回子树规模之和（整数）；若无效，我会返回"无效"并说明原因。

重要限制：
- 双节点测量必须确保两个节点互不为祖先或后代关系。
- 累计发生 3 次无效的双节点测量请求将导致游戏失败。
- 提交的最终答案若有任何错误将导致游戏失败。

当你收集到足够信息后，请提交最终答案。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 祖先判定（例如问节点 1 是否为节点 3 的祖先）：
<query_ancestor>1,3</query_ancestor>

- 叶子判定（例如问节点 5 是否为叶节点）：
<query_leaf>5</query_leaf>

- 双节点测量（例如测量节点 2 和节点 4 的子树规模之和）：
<query_pair>2,4</query_pair>

提交最终答案时，列出每个目标节点及其子树规模，格式如下（用分号分隔多个节点）：

<answer>node=1,size=5;node=3,size=2</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Tree Structure" deduction game. Here are the rules:

The game features a rooted tree with {n} nodes. The root node is {root}, and all node identifiers are {nodes}. The tree's edge relationships are fixed but hidden from you.

Terminology:
- For any node v, its "subtree size" is defined as the total number of nodes in the subtree rooted at v (including v itself).
- The ancestor relationship is reflexive, meaning any node v is an ancestor of itself.
- A leaf node is a node with no children, and its subtree size is 1.

Your goal is to determine the subtree size of each node in the target node set {targets}.

You can ask me questions in three ways (one question per turn):

1. Ancestor Query: Ask whether node A is an ancestor of node B. I will answer "Yes" or "No". Note: Any node is an ancestor of itself.
2. Leaf Query: Ask whether node X is a leaf node. I will answer "Yes" or "No". If it is a leaf, its subtree size is 1.
3. Pair Measurement: Simultaneously measure the sum of subtree sizes of two nodes U and V. Note: U and V must not be in an ancestor-descendant relationship, otherwise the measurement is invalid. If valid, I will return the sum (an integer); if invalid, I will return "Invalid" with a reason.

Important Constraints:
- Pair measurements must ensure the two nodes are not in an ancestor-descendant relationship.
- Accumulating 3 invalid pair measurement requests will result in game failure.
- Submitting a final answer with any errors will result in game failure.

When you have collected enough information, submit your final answer.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Ancestor Query (e.g., asking if node 1 is an ancestor of node 3):
<query_ancestor>1,3</query_ancestor>

- Leaf Query (e.g., asking if node 5 is a leaf):
<query_leaf>5</query_leaf>

- Pair Measurement (e.g., measuring the sum of subtree sizes of nodes 2 and 4):
<query_pair>2,4</query_pair>

When submitting the final answer, list each target node and its subtree size in the following format (separate multiple nodes with semicolons):

<answer>node=1,size=5;node=3,size=2</answer>
"""


    contextualized_rule_zh_1 = """\
我们现在来执行一项“隐藏路网拓扑分析”任务，规则如下：

任务设定了一个包含 {n} 个路口节点的交通路网树状结构。总枢纽节点为 {root}，所有节点的标识为 {nodes}。路网的单向道路连接关系是固定的但对你隐藏。

术语说明：
- 对于任意节点 v，其“下游路网覆盖规模”定义为以 v 为起点的下游分支中的节点总数（包括 v 自身）。
- 上游关系是自反的，即任意节点 v 都是它自己的上游。
- 终端节点指没有更下游节点的死胡同路口，其路网覆盖规模为 1。

你的目标是确定目标节点集合 {targets} 中每个节点的下游路网覆盖规模。

你可以通过以下三种方式向我发起查询（每次仅限一个查询）：

1. 上下游判定：询问节点 A 是否为节点 B 的上游。我会回答“是”或“否”。注意：任意节点都是自己的上游。
2. 终端判定：询问节点 X 是否为终端节点。我会回答“是”或“否”。若为终端节点，则其路网覆盖规模为 1。
3. 双节点联合测算：同时测算两个节点 U 和 V 的下游路网覆盖规模之和。注意：U 和 V 必须互不为上下游关系，否则测算无效。若有效，我会返回规模之和（整数）；若无效，我会返回“无效”并说明原因。

重要限制：
- 双节点联合测算必须确保两个节点互不为上下游关系。
- 累计发生 3 次无效的双节点测算请求将导致任务失败。
- 提交的最终答案若有任何错误将导致任务失败。

当你收集到足够信息后，请提交最终答案。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 上下游判定（对应祖先判定，例如问节点 1 是否为节点 3 的上游）：
<query_ancestor>1,3</query_ancestor>

- 终端判定（对应叶子判定，例如问节点 5 是否为终端节点）：
<query_leaf>5</query_leaf>

- 双节点联合测算（例如测算节点 2 和节点 4 的路网覆盖规模之和）：
<query_pair>2,4</query_pair>

提交最终答案时，列出每个目标节点及其下游路网覆盖规模，格式如下（用分号分隔多个节点）：

<answer>node=1,size=5;node=3,size=2</answer>
"""

    contextualized_rule_en_1 = """\
[Transport Scenario]
Let's execute a "Hidden Road Network Topology Analysis" task. Here are the rules:

The task features a traffic network tree structure with {n} intersection nodes. The main hub node is {root}, and all node identifiers are {nodes}. The network's one-way road connections are fixed but hidden from you.

Terminology:
- For any node v, its "downstream coverage size" is defined as the total number of nodes in the downstream branches starting from v (including v itself).
- The upstream relationship is reflexive, meaning any node v is an upstream node of itself.
- A terminal node is a dead-end with no downstream nodes, and its coverage size is 1.

Your goal is to determine the downstream coverage size of each node in the target node set {targets}.

You can ask me questions in three ways (one query per turn):

1. Upstream Query: Ask whether node A is upstream of node B. I will answer "Yes" or "No". Note: Any node is upstream of itself.
2. Terminal Query: Ask whether node X is a terminal node. I will answer "Yes" or "No". If it is a terminal node, its coverage size is 1.
3. Pair Measurement: Simultaneously measure the sum of downstream coverage sizes of two nodes U and V. Note: U and V must not be in an upstream-downstream relationship, otherwise the measurement is invalid. If valid, I will return the sum (an integer); if invalid, I will return "Invalid" with a reason.

Important Constraints:
- Pair measurements must ensure the two nodes are not in an upstream-downstream relationship.
- Accumulating 3 invalid pair measurement requests will result in task failure.
- Submitting a final answer with any errors will result in task failure.

When you have collected enough information, submit your final answer.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Upstream Query (corresponds to ancestor query, e.g., asking if node 1 is upstream of node 3):
<query_ancestor>1,3</query_ancestor>

- Terminal Query (corresponds to leaf query, e.g., asking if node 5 is a terminal node):
<query_leaf>5</query_leaf>

- Pair Measurement (e.g., measuring the sum of downstream coverage sizes of nodes 2 and 4):
<query_pair>2,4</query_pair>

When submitting the final answer, list each target node and its downstream coverage size in the following format (separate multiple nodes with semicolons):

<answer>node=1,size=5;node=3,size=2</answer>
"""


    contextualized_rule_zh_2 = """\
我们现在来执行一项“隐性病毒传播链追踪”任务，规则如下：

系统记录了一条包含 {n} 个感染者节点的树状传播链。零号病人节点为 {root}，所有感染者的标识为 {nodes}。具体的传染路径是固定的但目前对你隐藏。

术语说明：
- 对于任意感染者 v，其“感染分支规模”定义为由 v 直接及间接引发感染的总人数（包括 v 自身）。
- 传播源关系是自反的，即任意感染者 v 都是自己的传播源。
- 传播终点指没有再传染给其他人的感染者，其感染分支规模为 1。

你的目标是确定目标感染者集合 {targets} 中每个感染者的感染分支规模。

你可以通过以下三种方式向我发起排查（每次仅限一个排查）：

1. 传播源判定：询问感染者 A 是否为感染者 B 的传播源。我会回答“是”或“否”。注意：任意感染者都是自己的传播源。
2. 终点判定：询问感染者 X 是否为传播终点。我会回答“是”或“否”。若为传播终点，则其感染分支规模为 1。
3. 双节点联合排查：同时测算两个感染者 U 和 V 的感染分支规模之和。注意：U 和 V 必须互不为传播源及后续感染者关系，否则排查无效。若有效，我会返回规模之和（整数）；若无效，我会返回“无效”并说明原因。

重要限制：
- 双节点联合排查必须确保两人不在同一条纵向传播路径上。
- 累计发生 3 次无效的双节点排查请求将导致任务失败。
- 提交的最终答案若有任何错误将导致任务失败。

当你收集到足够信息后，请提交最终答案。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 传播源判定（对应祖先判定，例如问节点 1 是否为节点 3 的传播源）：
<query_ancestor>1,3</query_ancestor>

- 终点判定（对应叶子判定，例如问节点 5 是否为传播终点）：
<query_leaf>5</query_leaf>

- 双节点联合排查（例如测算节点 2 和节点 4 的感染分支规模之和）：
<query_pair>2,4</query_pair>

提交最终答案时，列出每个目标节点及其感染分支规模，格式如下（用分号分隔多个节点）：

<answer>node=1,size=5;node=3,size=2</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's execute a "Hidden Virus Transmission Chain Tracking" task. Here are the rules:

The system has recorded a virus transmission tree structure with {n} patient nodes. The patient zero node is {root}, and all patient identifiers are {nodes}. The specific infection paths are fixed but currently hidden from you.

Terminology:
- For any patient v, their "infection branch size" is defined as the total number of people directly and indirectly infected by v (including v themselves).
- The transmission source relationship is reflexive, meaning any patient v is their own transmission source.
- A transmission endpoint is a patient who did not infect anyone else, and their infection branch size is 1.

Your goal is to determine the infection branch size of each patient in the target set {targets}.

You can initiate screenings with me in three ways (one screening per turn):

1. Source Query: Ask whether patient A is the transmission source of patient B. I will answer "Yes" or "No". Note: Any patient is their own transmission source.
2. Endpoint Query: Ask whether patient X is a transmission endpoint. I will answer "Yes" or "No". If it is an endpoint, its infection branch size is 1.
3. Pair Screening: Simultaneously measure the sum of infection branch sizes of two patients U and V. Note: U and V must not be in a transmission source-successor relationship, otherwise the screening is invalid. If valid, I will return the sum (an integer); if invalid, I will return "Invalid" with a reason.

Important Constraints:
- Pair screenings must ensure the two patients are not on the same vertical transmission path.
- Accumulating 3 invalid pair screening requests will result in task failure.
- Submitting a final answer with any errors will result in task failure.

When you have collected enough information, submit your final answer.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Source Query (corresponds to ancestor query, e.g., asking if node 1 is the transmission source of node 3):
<query_ancestor>1,3</query_ancestor>

- Endpoint Query (corresponds to leaf query, e.g., asking if node 5 is a transmission endpoint):
<query_leaf>5</query_leaf>

- Pair Screening (e.g., measuring the sum of infection branch sizes of nodes 2 and 4):
<query_pair>2,4</query_pair>

When submitting the final answer, list each target node and its infection branch size in the following format (separate multiple nodes with semicolons):

<answer>node=1,size=5;node=3,size=2</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项“隐藏知识依赖树构建”任务，规则如下：

系统包含一棵有 {n} 个节点的知识点依赖树结构。基础核心知识点为 {root}，所有节点的标识为 {nodes}。知识点之间的先修学习关系是固定的但对你隐藏。

术语说明：
- 对于任意知识点 v，其“衍生知识点规模”定义为掌握 v 后可直接及间接解锁的所有衍生知识点总数（包括 v 自身）。
- 前置依赖关系是自反的，即任意知识点 v 都是它自己的前置依赖。
- 终极应用知识点指没有基于它的更高阶知识节点，其衍生知识点规模为 1。

你的目标是确定目标节点集合 {targets} 中每个节点的衍生知识点规模。

你可以通过以下三种方式向我发起核查（每次仅限一个核查）：

1. 前置判定：询问知识点 A 是否为知识点 B 的前置依赖。我会回答“是”或“否”。注意：任意知识点都是自己的前置依赖。
2. 终极判定：询问知识点 X 是否为终极应用知识点。我会回答“是”或“否”。若为终极应用，则其衍生知识点规模为 1。
3. 双节点联合评估：同时测算两个知识点 U 和 V 的衍生知识点规模之和。注意：U 和 V 必须互不为前置或后续关系，否则评估无效。若有效，我会返回规模之和（整数）；若无效，我会返回“无效”并说明原因。

重要限制：
- 双节点联合评估必须确保两个知识点互不为前置依赖关系。
- 累计发生 3 次无效的双节点评估请求将导致任务失败。
- 提交的最终答案若有任何错误将导致任务失败。

当你收集到足够信息后，请提交最终答案。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 前置判定（对应祖先判定，例如问节点 1 是否为节点 3 的前置依赖）：
<query_ancestor>1,3</query_ancestor>

- 终极判定（对应叶子判定，例如问节点 5 是否为终极应用知识点）：
<query_leaf>5</query_leaf>

- 双节点联合评估（例如测算节点 2 和节点 4 的衍生知识点规模之和）：
<query_pair>2,4</query_pair>

提交最终答案时，列出每个目标节点及其衍生知识点规模，格式如下（用分号分隔多个节点）：

<answer>node=1,size=5;node=3,size=2</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Hidden Knowledge Dependency Tree Building" task. Here are the rules:

The system contains a knowledge dependency tree structure with {n} concept nodes. The foundational core concept is {root}, and all node identifiers are {nodes}. The prerequisite learning relationships between concepts are fixed but hidden from you.

Terminology:
- For any concept v, its "derived knowledge size" is defined as the total number of derived concepts that can be unlocked directly and indirectly after mastering v (including v itself).
- The prerequisite dependency relationship is reflexive, meaning any concept v is a prerequisite of itself.
- An ultimate application concept refers to a node with no higher-order concepts based on it, and its derived knowledge size is 1.

Your goal is to determine the derived knowledge size of each concept in the target node set {targets}.

You can initiate verifications with me in three ways (one verification per turn):

1. Prerequisite Query: Ask whether concept A is a prerequisite dependency of concept B. I will answer "Yes" or "No". Note: Any concept is a prerequisite of itself.
2. Ultimate Query: Ask whether concept X is an ultimate application concept. I will answer "Yes" or "No". If it is an ultimate application, its derived knowledge size is 1.
3. Pair Measurement: Simultaneously evaluate the sum of derived knowledge sizes of two concepts U and V. Note: U and V must not be in a prerequisite-successor relationship, otherwise the evaluation is invalid. If valid, I will return the sum (an integer); if invalid, I will return "Invalid" with a reason.

Important Constraints:
- Pair measurements must ensure the two concepts are not prerequisite dependencies of each other.
- Accumulating 3 invalid pair measurement requests will result in task failure.
- Submitting a final answer with any errors will result in task failure.

When you have collected enough information, submit your final answer.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Prerequisite Query (corresponds to ancestor query, e.g., asking if node 1 is a prerequisite of node 3):
<query_ancestor>1,3</query_ancestor>

- Ultimate Query (corresponds to leaf query, e.g., asking if node 5 is an ultimate application concept):
<query_leaf>5</query_leaf>

- Pair Measurement (e.g., evaluating the sum of derived knowledge sizes of nodes 2 and 4):
<query_pair>2,4</query_pair>

When submitting the final answer, list each target node and its derived knowledge size in the following format (separate multiple nodes with semicolons):

<answer>node=1,size=5;node=3,size=2</answer>
"""


    contextualized_rule_zh_4 = """\
我们现在来执行一项“隐藏物料清单(BOM)层级分析”任务，规则如下：

系统记录了一套包含 {n} 个部件节点的BOM展开树结构。顶级装配体节点为 {root}，所有部件的标识为 {nodes}。装配间的包含层级关系是固定的但对你隐藏。

术语说明：
- 对于任意部件 v，其“包含零部件总规模”定义为以 v 为根的子装配体中包含的所有零部件层级总数（包括 v 自身）。
- 祖先装配体关系是自反的，即任意部件 v 都是它自己的祖先装配体。
- 基础原材料指不可再往下拆分的底层零件，其包含零部件总规模为 1。

你的目标是确定目标部件集合 {targets} 中每个部件的包含零部件总规模。

你可以通过以下三种方式向我发起核查（每次仅限一个核查）：

1. 层级判定：询问部件 A 是否为部件 B 的祖先装配体。我会回答“是”或“否”。注意：任意部件都是自己的祖先装配体。
2. 原材料判定：询问部件 X 是否为基础原材料。我会回答“是”或“否”。若为基础原材料，则其包含零部件总规模为 1。
3. 双节点联合核算：同时核算两个部件 U 和 V 的包含零部件总规模之和。注意：U 和 V 必须互不为包含与被包含的垂直关系，否则核算无效。若有效，我会返回规模之和（整数）；若无效，我会返回“无效”并说明原因。

重要限制：
- 双节点联合核算必须确保两个部件不存在上下级装配关系。
- 累计发生 3 次无效的双节点核算请求将导致任务失败。
- 提交的最终答案若有任何错误将导致任务失败。

当你收集到足够信息后，请提交最终答案。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 层级判定（对应祖先判定，例如问节点 1 是否为节点 3 的祖先装配体）：
<query_ancestor>1,3</query_ancestor>

- 原材料判定（对应叶子判定，例如问节点 5 是否为基础原材料）：
<query_leaf>5</query_leaf>

- 双节点联合核算（例如核算节点 2 和节点 4 的包含零部件总规模之和）：
<query_pair>2,4</query_pair>

提交最终答案时，列出每个目标节点及其包含零部件总规模，格式如下（用分号分隔多个节点）：

<answer>node=1,size=5;node=3,size=2</answer>
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Let's execute a "Hidden Bill of Materials (BOM) Hierarchy Analysis" task. Here are the rules:

The system records a BOM expansion tree structure with {n} component nodes. The top-level assembly node is {root}, and all component identifiers are {nodes}. The inclusion hierarchical relationships between assemblies are fixed but hidden from you.

Terminology:
- For any component v, its "contained components size" is defined as the total number of sub-components in the assembly hierarchy rooted at v (including v itself).
- The ancestor assembly relationship is reflexive, meaning any component v is an ancestor assembly of itself.
- A basic raw material refers to an indivisible bottom-level part, and its contained components size is 1.

Your goal is to determine the contained components size of each component in the target node set {targets}.

You can initiate verifications with me in three ways (one verification per turn):

1. Hierarchy Query: Ask whether component A is an ancestor assembly of component B. I will answer "Yes" or "No". Note: Any component is an ancestor assembly of itself.
2. Raw Material Query: Ask whether component X is a basic raw material. I will answer "Yes" or "No". If it is a basic raw material, its contained components size is 1.
3. Pair Accounting: Simultaneously account for the sum of contained components sizes of two components U and V. Note: U and V must not be in a vertical inclusion relationship, otherwise the accounting is invalid. If valid, I will return the sum (an integer); if invalid, I will return "Invalid" with a reason.

Important Constraints:
- Pair accounting must ensure the two components do not have an upstream-downstream assembly relationship.
- Accumulating 3 invalid pair accounting requests will result in task failure.
- Submitting a final answer with any errors will result in task failure.

When you have collected enough information, submit your final answer.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Hierarchy Query (corresponds to ancestor query, e.g., asking if node 1 is an ancestor assembly of node 3):
<query_ancestor>1,3</query_ancestor>

- Raw Material Query (corresponds to leaf query, e.g., asking if node 5 is a basic raw material):
<query_leaf>5</query_leaf>

- Pair Accounting (e.g., accounting for the sum of contained components sizes of nodes 2 and 4):
<query_pair>2,4</query_pair>

When submitting the final answer, list each target node and its contained components size in the following format (separate multiple nodes with semicolons):

<answer>node=1,size=5;node=3,size=2</answer>
"""


    contextualized_rule_zh_5 = """\
我们现在来执行一项“隐蔽股权控制架构核查”任务，规则如下：

案件涉及一个包含 {n} 个公司实体的股权控制树状结构。最终控股母公司节点为 {root}，所有公司的标识为 {nodes}。公司间的控股层级关系是固定的但目前对你隐藏。

术语说明：
- 对于任意公司 v，其“下辖企业总规模”定义为由 v 直接及间接控股的所有企业总数（包括 v 自身）。
- 控股母公司关系是自反的，即任意公司 v 都是它自己的控股母公司。
- 底层业务公司指没有再进一步控股其他实体的末端企业，其下辖企业总规模为 1。

你的目标是确定目标公司集合 {targets} 中每个公司的下辖企业总规模。

你可以通过以下三种方式向我发起审计查询（每次仅限一个查询）：

1. 控股判定：询问公司 A 是否为公司 B 的控股母公司。我会回答“是”或“否”。注意：任意公司都是自己的控股母公司。
2. 底层判定：询问公司 X 是否为底层业务公司。我会回答“是”或“否”。若为底层业务公司，则其下辖企业总规模为 1。
3. 双节点联合审计：同时审计两家公司 U 和 V 的下辖企业总规模之和。注意：U 和 V 必须互不为垂直控股关系，否则审计无效。若有效，我会返回规模之和（整数）；若无效，我会返回“无效”并说明原因。

重要限制：
- 双节点联合审计必须确保两家实体不存在上下级的控股关联。
- 累计发生 3 次无效的双节点审计请求将导致任务失败。
- 提交的最终答案若有任何错误将导致任务失败。

当你收集到足够信息后，请提交最终答案。

## 询问与提交答案的格式

每次询问只能包含一个标签。请使用以下 XML 格式：

- 控股判定（对应祖先判定，例如问节点 1 是否为节点 3 的控股母公司）：
<query_ancestor>1,3</query_ancestor>

- 底层判定（对应叶子判定，例如问节点 5 是否为底层业务公司）：
<query_leaf>5</query_leaf>

- 双节点联合审计（例如审计节点 2 和节点 4 的下辖企业总规模之和）：
<query_pair>2,4</query_pair>

提交最终答案时，列出每个目标节点及其下辖企业总规模，格式如下（用分号分隔多个节点）：

<answer>node=1,size=5;node=3,size=2</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's execute a "Hidden Equity Control Structure Verification" task. Here are the rules:

The case involves an equity control tree structure with {n} company entities. The ultimate controlling parent company node is {root}, and all company identifiers are {nodes}. The controlling hierarchical relationships between companies are fixed but currently hidden from you.

Terminology:
- For any company v, its "subsidiary enterprise size" is defined as the total number of enterprises directly and indirectly controlled by v (including v itself).
- The controlling parent company relationship is reflexive, meaning any company v is a controlling parent of itself.
- A bottom-level operating company refers to a terminal enterprise that does not control any other entities, and its subsidiary enterprise size is 1.

Your goal is to determine the subsidiary enterprise size of each company in the target set {targets}.

You can initiate audit queries with me in three ways (one query per turn):

1. Control Query: Ask whether company A is a controlling parent company of company B. I will answer "Yes" or "No". Note: Any company is a controlling parent of itself.
2. Bottom-level Query: Ask whether company X is a bottom-level operating company. I will answer "Yes" or "No". If it is a bottom-level operating company, its subsidiary enterprise size is 1.
3. Pair Audit: Simultaneously audit the sum of subsidiary enterprise sizes of two companies U and V. Note: U and V must not be in a vertical control relationship, otherwise the audit is invalid. If valid, I will return the sum (an integer); if invalid, I will return "Invalid" with a reason.

Important Constraints:
- Pair audits must ensure the two entities do not have an upstream-downstream control association.
- Accumulating 3 invalid pair audit requests will result in task failure.
- Submitting a final answer with any errors will result in task failure.

When you have collected enough information, submit your final answer.

## Query and Answer Format

Each query must contain only one tag. Use the following XML format:

- Control Query (corresponds to ancestor query, e.g., asking if node 1 is a controlling parent company of node 3):
<query_ancestor>1,3</query_ancestor>

- Bottom-level Query (corresponds to leaf query, e.g., asking if node 5 is a bottom-level operating company):
<query_leaf>5</query_leaf>

- Pair Audit (e.g., auditing the sum of subsidiary enterprise sizes of nodes 2 and 4):
<query_pair>2,4</query_pair>

When submitting the final answer, list each target node and its subsidiary enterprise size in the following format (separate multiple nodes with semicolons):

<answer>node=1,size=5;node=3,size=2</answer>
"""

    tags = ["answer", "query_ancestor", "query_leaf", "query_pair"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5, "root": "1", "nodes": "1,2,3,4,5", "targets": "2",
                "parent": {"2": "1", "3": "1", "4": "1", "5": "1"},
                "answer": {"2": 1},
            },
            2: {
                "n": 7, "root": "1", "nodes": "1,2,3,4,5,6,7", "targets": "2,3",
                "parent": {"2": "1", "3": "1", "4": "2", "5": "2", "6": "3", "7": "3"},
                "answer": {"2": 3, "3": 3},
            },
            3: {
                "n": 10, "root": "1", "nodes": "1,2,3,4,5,6,7,8,9,10", "targets": "2,4,5",
                "parent": {"2": "1", "3": "1", "4": "2", "5": "2", "6": "2", "7": "3", "8": "3", "9": "5", "10": "5"},
                "answer": {"2": 6, "4": 1, "5": 3},
            },
            4: {
                "n": 12, "root": "1", "nodes": "1,2,3,4,5,6,7,8,9,10,11,12", "targets": "2,3,6,8",
                "parent": {"2": "1", "3": "1", "4": "2", "5": "2", "6": "2", "7": "3", "8": "3", "9": "6", "10": "6", "11": "8", "12": "8"},
                "answer": {"2": 7, "3": 5, "6": 3, "8": 3},
            },
            5: {
                "n": 15, "root": "1", "nodes": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15", "targets": "2,3,5,7,10",
                "parent": {"2": "1", "3": "1", "4": "2", "5": "2", "6": "3", "7": "3", "8": "5", "9": "5", "10": "5", "11": "7", "12": "7", "13": "10", "14": "10", "15": "10"},
                "answer": {"2": 9, "3": 5, "5": 7, "7": 3, "10": 4},
            },
        },
        "en": {
            1: {
                "n": 5, "root": "1", "nodes": "1,2,3,4,5", "targets": "2",
                "parent": {"2": "1", "3": "1", "4": "1", "5": "1"},
                "answer": {"2": 1},
            },
            2: {
                "n": 7, "root": "1", "nodes": "1,2,3,4,5,6,7", "targets": "2,3",
                "parent": {"2": "1", "3": "1", "4": "2", "5": "2", "6": "3", "7": "3"},
                "answer": {"2": 3, "3": 3},
            },
            3: {
                "n": 10, "root": "1", "nodes": "1,2,3,4,5,6,7,8,9,10", "targets": "2,4,5",
                "parent": {"2": "1", "3": "1", "4": "2", "5": "2", "6": "2", "7": "3", "8": "3", "9": "5", "10": "5"},
                "answer": {"2": 6, "4": 1, "5": 3},
            },
            4: {
                "n": 12, "root": "1", "nodes": "1,2,3,4,5,6,7,8,9,10,11,12", "targets": "2,3,6,8",
                "parent": {"2": "1", "3": "1", "4": "2", "5": "2", "6": "2", "7": "3", "8": "3", "9": "6", "10": "6", "11": "8", "12": "8"},
                "answer": {"2": 7, "3": 5, "6": 3, "8": 3},
            },
            5: {
                "n": 15, "root": "1", "nodes": "1,2,3,4,5,6,7,8,9,10,11,12,13,14,15", "targets": "2,3,5,7,10",
                "parent": {"2": "1", "3": "1", "4": "2", "5": "2", "6": "3", "7": "3", "8": "5", "9": "5", "10": "5", "11": "7", "12": "7", "13": "10", "14": "10", "15": "10"},
                "answer": {"2": 9, "3": 5, "5": 7, "7": 3, "10": 4},
            },
        },
    }

    def __init__(self, config):
        self.invalid_query_count = 0  # 记录无效查询次数
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self._game_info["nodes"] = cfg["nodes"]
        self._game_info["targets"] = cfg["targets"]
        
        # 解析父节点映射
        self.parent_map = cfg["parent"]
        
        # 正确答案
        self.correct_answer = cfg["answer"]
        
        # 构建祖先关系缓存（用于快速判断）
        self.nodes_set = set(cfg["nodes"].split(","))
        self._build_tree_structure()

        # 提示词指明删除冗余的反事实干预控制变量

    def _build_tree_structure(self):
        """构建树结构，计算子树规模和祖先关系"""
        # 构建子节点映射
        self.children_map = {}
        for node in self.nodes_set:
            self.children_map[node] = []
        
        for child, parent in self.parent_map.items():
            if parent not in self.children_map:
                self.children_map[parent] = []
            self.children_map[parent].append(child)
        
        # 计算子树规模（使用DFS）
        self.subtree_size = {}
        
        def compute_size(node):
            if node in self.subtree_size:
                return self.subtree_size[node]
            size = 1
            for child in self.children_map.get(node, []):
                size += compute_size(child)
            self.subtree_size[node] = size
            return size
        
        root = self._game_info["root"]
        compute_size(root)
        
        # 构建祖先集合（用于快速判断祖先关系）
        self.ancestors = {}
        for node in self.nodes_set:
            self.ancestors[node] = set([node])  # 自反性
            current = node
            while current in self.parent_map:
                current = self.parent_map[current]
                self.ancestors[node].add(current)

    def _is_ancestor(self, a, b):
        """判断节点a是否为节点b的祖先（自反）"""
        return a in self.ancestors.get(b, set())

    def _is_leaf(self, node):
        """判断节点是否为叶节点"""
        return len(self.children_map.get(node, [])) == 0

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案格式: node=X,size=Y;node=X2,size=Y2
        try:
            pairs = [x.strip() for x in raw_ans.split(";") if x.strip()]
            submitted_answer = {}
            
            for pair in pairs:
                kv_dict = {}
                for kv in pair.split(","):
                    k, v = kv.split("=")
                    kv_dict[k.strip()] = v.strip()
                
                if "node" not in kv_dict or "size" not in kv_dict:
                    return False
                
                node = kv_dict["node"]
                size = int(kv_dict["size"])
                submitted_answer[node] = size
            
            # 检查答案是否完全匹配
            if set(submitted_answer.keys()) != set(self.correct_answer.keys()):
                return False
            
            for node, size in submitted_answer.items():
                if self.correct_answer[node] != size:
                    return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            invalid_msg = "无效（原因：两节点存在祖先-后代关系）"
            error_msg = "错误：节点不存在或格式错误。"
            limit_msg = "无效查询次数已达到3次，游戏失败。"
        else:
            yes_res, no_res = "Yes", "No"
            invalid_msg = "Invalid (reason: ancestor-descendant relationship exists)"
            error_msg = "Error: Node does not exist or format error."
            limit_msg = "Invalid query count reached 3, game failed."

        # 优先级：ancestor > leaf > pair
        if "query_ancestor" in parsed_info:
            try:
                raw = parsed_info["query_ancestor"]
                a, b = [x.strip() for x in raw.split(",")]
                if a not in self.nodes_set or b not in self.nodes_set:
                    return error_msg
                return yes_res if self._is_ancestor(a, b) else no_res
            except:
                return error_msg

        elif "query_leaf" in parsed_info:
            try:
                node = parsed_info["query_leaf"].strip()
                if node not in self.nodes_set:
                    return error_msg
                return yes_res if self._is_leaf(node) else no_res
            except:
                return error_msg

        elif "query_pair" in parsed_info:
            try:
                raw = parsed_info["query_pair"]
                u, v = [x.strip() for x in raw.split(",")]
                if u not in self.nodes_set or v not in self.nodes_set:
                    return error_msg
                
                # 检查是否互不为祖先或后代
                if self._is_ancestor(u, v) or self._is_ancestor(v, u):
                    self.invalid_query_count += 1
                    if self.invalid_query_count >= 3:
                        self.state.set_state("failed", "too many invalid queries")
                        return limit_msg
                    return invalid_msg
                
                # 返回子树规模之和
                return str(self.subtree_size[u] + self.subtree_size[v])
            except:
                return error_msg

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """
        生成一个错误的响应，用于反事实干预模式。
        对于数值型答案，修改数值；对于是/否型答案，取反。
        """
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 如果是 Yes/No 类型的回答，取反
        if correct == yes_res:
            return no_res
        if correct == no_res:
            return yes_res

        # 如果是数值型（双节点测量结果），修改数值
        try:
            val = int(correct)
            # 返回一个不同的值
            return str(val + 1)
        except ValueError:
            pass

        # 对于无效提示或错误消息，返回一个虚构的数值
        return "999"

    def get_all_possible_queries(self) -> List[Dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        每项包含 "query"（XML 标签字符串）和 "answer"（str）。
        """
        queries = []
        # 按数字顺序排序节点，保证确定性
        nodes = sorted(list(self.nodes_set), key=lambda x: int(x) if x.isdigit() else x)
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 1. 枚举所有叶子判定查询
        for node in nodes:
            ans = yes_res if self._is_leaf(node) else no_res
            queries.append({
                "query": f"<query_leaf>{node}</query_leaf>",
                "answer": ans
            })

        # 2. 枚举所有祖先判定查询 (u, v)
        for u in nodes:
            for v in nodes:
                ans = yes_res if self._is_ancestor(u, v) else no_res
                queries.append({
                    "query": f"<query_ancestor>{u},{v}</query_ancestor>",
                    "answer": ans
                })

        # 3. 枚举所有双节点测量查询 (u, v)，仅生成有序对避免重复
        for i, u in enumerate(nodes):
            for v in nodes[i+1:]:
                # 如果存在祖先-后代关系，则为无效查询，按规则应排除
                if self._is_ancestor(u, v) or self._is_ancestor(v, u):
                    continue
                
                # 计算有效查询的答案
                size_sum = self.subtree_size[u] + self.subtree_size[v]
                queries.append({
                    "query": f"<query_pair>{u},{v}</query_pair>",
                    "answer": str(size_sum)
                })

        return queries