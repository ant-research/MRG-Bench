from .base import Game
import itertools

class GraphNeighborDeductionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"图邻居推断"游戏，规则如下：

游戏设定了16个节点，标签为四位二进制后缀的标识：S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111。这些节点构成一个无向、无权图。

你的目标是推断出目标节点 {target_node} 的全部邻居节点。注意：你不能对目标节点 {target_node} 本身进行任何查询，否则将被判定为非法操作。

你可以通过以下三类查询获取信息（每次仅限一个查询）：

1. 邻居列表查询（类型A，最多 {quota_a} 次）：询问某个节点的全部邻居列表。我会返回该节点的所有邻居，按字典序升序排列。
2. 是否相邻查询（类型B，最多 {quota_b} 次）：询问两个节点是否相邻。我会回答"是"或"否"。
3. 度数查询（类型C，最多 {quota_c} 次）：询问某个节点的度数（即邻居数量）。我会回答一个非负整数。

请注意：
- 所有查询的节点必须是上述16个节点之一，且不能是目标节点 {target_node}。
- 每类查询都有次数限制，超过限制将导致游戏失败。
- 如果你对目标节点 {target_node} 发起查询累计达到3次，游戏将直接失败。

当你收集足够信息后，请提交最终答案。若答案不正确或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 邻居列表查询（例如查询 S0001 的邻居）：
<query_neighbors>S0001</query_neighbors>

- 是否相邻查询（例如查询 S0001 和 S0010 是否相邻）：
<query_adjacent>S0001,S0010</query_adjacent>

- 度数查询（例如查询 S0001 的度数）：
<query_degree>S0001</query_degree>

提交最终答案时，请列出目标节点 {target_node} 的所有邻居（顺序不限），格式如下：

<answer>S0000,S1000,S1011,S1110</answer>
"""

    game_rule_en = """\
Let's play a "Graph Neighbor Deduction" game. Here are the rules:

There are 16 nodes with labels based on four-bit binary suffixes: S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111. These nodes form an undirected, unweighted graph.

Your goal is to infer all neighbors of the target node {target_node}. Note: You cannot query the target node {target_node} itself, or it will be considered an illegal operation.

You can gather information through three types of queries (one query per turn):

1. Neighbor List Query (Type A, at most {quota_a} times): Ask for the complete neighbor list of a node. I will return all neighbors of that node in lexicographically ascending order.
2. Adjacency Query (Type B, at most {quota_b} times): Ask if two nodes are adjacent. I will answer "Yes" or "No".
3. Degree Query (Type C, at most {quota_c} times): Ask for the degree (number of neighbors) of a node. I will answer with a non-negative integer.

Please note:
- All queried nodes must be one of the 16 nodes listed above, and cannot be the target node {target_node}.
- Each query type has a usage limit; exceeding the limit will cause the game to fail.
- If you query the target node {target_node} 3 times in total, the game will fail immediately.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Neighbor List Query (e.g., querying neighbors of S0001):
<query_neighbors>S0001</query_neighbors>

- Adjacency Query (e.g., querying if S0001 and S0010 are adjacent):
<query_adjacent>S0001,S0010</query_adjacent>

- Degree Query (e.g., querying the degree of S0001):
<query_degree>S0001</query_degree>

When submitting the final answer, list all neighbors of the target node {target_node} (order does not matter), using this format:

<answer>S0000,S1000,S1011,S1110</answer>
"""

    contextualized_rule_zh_1 = """\
【交通场景】我们现在来进行一项城市交通网络规划。
游戏设定了16个交通枢纽，标识为：S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111。它们构成了一个无向的交通网络。

你的目标是推断出目标交通枢纽 {target_node} 的全部直连枢纽。注意：你不能对目标交通枢纽 {target_node} 本身进行任何查询，否则将被判定为非法操作。

你可以通过以下三类查询获取信息（每次仅限一个查询）：

1. 直连枢纽列表查询（类型A，最多 {quota_a} 次）：询问某个交通枢纽的全部直连枢纽列表。我会返回该枢纽的所有直连枢纽，按字典序升序排列。
2. 是否直连查询（类型B，最多 {quota_b} 次）：询问两个交通枢纽是否直连。我会回答"是"或"否"。
3. 直连枢纽数量查询（类型C，最多 {quota_c} 次）：询问某个交通枢纽的直连枢纽数量。我会回答一个非负整数。

请注意：
- 所有查询的交通枢纽必须是上述16个之一，且不能是目标交通枢纽 {target_node}。
- 每类查询都有次数限制，超过限制将导致游戏失败。
- 如果你对目标交通枢纽 {target_node} 发起查询累计达到3次，游戏将直接失败。

当你收集足够信息后，请提交最终答案。若答案不正确或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 直连枢纽列表查询（例如查询 S0001 的直连枢纽）：
<query_neighbors>S0001</query_neighbors>

- 是否直连查询（例如查询 S0001 和 S0010 是否直连）：
<query_adjacent>S0001,S0010</query_adjacent>

- 直连枢纽数量查询（例如查询 S0001 的直连枢纽数量）：
<query_degree>S0001</query_degree>

提交最终答案时，请列出目标交通枢纽 {target_node} 的所有直连枢纽（顺序不限），格式如下：

<answer>S0000,S1000,S1011,S1110</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario] Let's plan an urban traffic network.
There are 16 traffic hubs labeled: S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111. They form an undirected traffic network.

Your goal is to infer all directly connected hubs of the target traffic hub {target_node}. Note: You cannot query the target traffic hub {target_node} itself, or it will be considered an illegal operation.

You can gather information through three types of queries (one query per turn):

1. Connected Hubs List Query (Type A, at most {quota_a} times): Ask for the complete list of directly connected hubs of a traffic hub. I will return all connected hubs in lexicographically ascending order.
2. Direct Connection Query (Type B, at most {quota_b} times): Ask if two traffic hubs are directly connected. I will answer "Yes" or "No".
3. Connection Count Query (Type C, at most {quota_c} times): Ask for the number of directly connected hubs of a traffic hub. I will answer with a non-negative integer.

Please note:
- All queried traffic hubs must be one of the 16 listed above, and cannot be the target traffic hub {target_node}.
- Each query type has a usage limit; exceeding the limit will cause the game to fail.
- If you query the target traffic hub {target_node} 3 times in total, the game will fail immediately.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Connected Hubs List Query (e.g., querying directly connected hubs of S0001):
<query_neighbors>S0001</query_neighbors>

- Direct Connection Query (e.g., querying if S0001 and S0010 are directly connected):
<query_adjacent>S0001,S0010</query_adjacent>

- Connection Count Query (e.g., querying the number of connected hubs of S0001):
<query_degree>S0001</query_degree>

When submitting the final answer, list all directly connected hubs of the target traffic hub {target_node} (order does not matter), using this format:

<answer>S0000,S1000,S1011,S1110</answer>
"""

    contextualized_rule_zh_2 = """\
【医疗场景】我们现在来进行一项传染病接触追踪。
游戏设定了16个监测对象，标识为：S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111。他们构成了一个接触传播网络。

你的目标是推断出目标监测对象 {target_node} 的全部密接对象。注意：你不能对目标监测对象 {target_node} 本身进行任何查询，否则将被判定为非法操作。

你可以通过以下三类查询获取信息（每次仅限一个查询）：

1. 密接列表查询（类型A，最多 {quota_a} 次）：询问某个监测对象的全部密接对象列表。我会返回其所有的密接对象，按字典序升序排列。
2. 是否接触查询（类型B，最多 {quota_b} 次）：询问两个监测对象是否有过直接接触。我会回答"是"或"否"。
3. 密接数量查询（类型C，最多 {quota_c} 次）：询问某个监测对象的密接对象数量。我会回答一个非负整数。

请注意：
- 所有查询的监测对象必须是上述16个之一，且不能是目标监测对象 {target_node}。
- 每类查询都有次数限制，超过限制将导致游戏失败。
- 如果你对目标监测对象 {target_node} 发起查询累计达到3次，游戏将直接失败。

当你收集足够信息后，请提交最终答案。若答案不正确或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 密接列表查询（例如查询 S0001 的密接对象）：
<query_neighbors>S0001</query_neighbors>

- 是否接触查询（例如查询 S0001 和 S0010 是否接触）：
<query_adjacent>S0001,S0010</query_adjacent>

- 密接数量查询（例如查询 S0001 的密接数量）：
<query_degree>S0001</query_degree>

提交最终答案时，请列出目标监测对象 {target_node} 的所有密接对象（顺序不限），格式如下：

<answer>S0000,S1000,S1011,S1110</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario] Let's conduct infectious disease contact tracing.
There are 16 monitored subjects labeled: S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111. They form a contact spread network.

Your goal is to infer all close contacts of the target monitored subject {target_node}. Note: You cannot query the target monitored subject {target_node} itself, or it will be considered an illegal operation.

You can gather information through three types of queries (one query per turn):

1. Close Contacts List Query (Type A, at most {quota_a} times): Ask for the complete list of close contacts of a subject. I will return all their close contacts in lexicographically ascending order.
2. Direct Contact Query (Type B, at most {quota_b} times): Ask if two monitored subjects had direct contact. I will answer "Yes" or "No".
3. Contacts Count Query (Type C, at most {quota_c} times): Ask for the number of close contacts of a subject. I will answer with a non-negative integer.

Please note:
- All queried monitored subjects must be one of the 16 listed above, and cannot be the target monitored subject {target_node}.
- Each query type has a usage limit; exceeding the limit will cause the game to fail.
- If you query the target monitored subject {target_node} 3 times in total, the game will fail immediately.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Close Contacts List Query (e.g., querying close contacts of S0001):
<query_neighbors>S0001</query_neighbors>

- Direct Contact Query (e.g., querying if S0001 and S0010 had direct contact):
<query_adjacent>S0001,S0010</query_adjacent>

- Contacts Count Query (e.g., querying the number of close contacts of S0001):
<query_degree>S0001</query_degree>

When submitting the final answer, list all close contacts of the target monitored subject {target_node} (order does not matter), using this format:

<answer>S0000,S1000,S1011,S1110</answer>
"""

    contextualized_rule_zh_3 = """\
【教育场景】我们现在来进行一项学术合作网络分析。
游戏设定了16位学者，标识为：S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111。他们构成了一个学术合作网络。

你的目标是推断出目标学者 {target_node} 的全部合作学者。注意：你不能对目标学者 {target_node} 本身进行任何查询，否则将被判定为非法操作。

你可以通过以下三类查询获取信息（每次仅限一个查询）：

1. 合作学者列表查询（类型A，最多 {quota_a} 次）：询问某位学者的全部合作学者列表。我会返回其所有的合作学者，按字典序升序排列。
2. 是否合作查询（类型B，最多 {quota_b} 次）：询问两位学者是否曾直接合作过。我会回答"是"或"否"。
3. 合作者数量查询（类型C，最多 {quota_c} 次）：询问某位学者的合作学者总数。我会回答一个非负整数。

请注意：
- 所有查询的学者必须是上述16位之一，且不能是目标学者 {target_node}。
- 每类查询都有次数限制，超过限制将导致游戏失败。
- 如果你对目标学者 {target_node} 发起查询累计达到3次，游戏将直接失败。

当你收集足够信息后，请提交最终答案。若答案不正确或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 合作学者列表查询（例如查询 S0001 的合作学者）：
<query_neighbors>S0001</query_neighbors>

- 是否合作查询（例如查询 S0001 和 S0010 是否曾合作）：
<query_adjacent>S0001,S0010</query_adjacent>

- 合作者数量查询（例如查询 S0001 的合作学者数量）：
<query_degree>S0001</query_degree>

提交最终答案时，请列出目标学者 {target_node} 的所有合作学者（顺序不限），格式如下：

<answer>S0000,S1000,S1011,S1110</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario] Let's analyze an academic collaboration network.
There are 16 scholars labeled: S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111. They form an academic collaboration network.

Your goal is to infer all collaborators of the target scholar {target_node}. Note: You cannot query the target scholar {target_node} itself, or it will be considered an illegal operation.

You can gather information through three types of queries (one query per turn):

1. Collaborators List Query (Type A, at most {quota_a} times): Ask for the complete list of collaborators of a scholar. I will return all their collaborators in lexicographically ascending order.
2. Collaboration Query (Type B, at most {quota_b} times): Ask if two scholars have collaborated directly. I will answer "Yes" or "No".
3. Collaborator Count Query (Type C, at most {quota_c} times): Ask for the total number of collaborators of a scholar. I will answer with a non-negative integer.

Please note:
- All queried scholars must be one of the 16 listed above, and cannot be the target scholar {target_node}.
- Each query type has a usage limit; exceeding the limit will cause the game to fail.
- If you query the target scholar {target_node} 3 times in total, the game will fail immediately.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Collaborators List Query (e.g., querying collaborators of S0001):
<query_neighbors>S0001</query_neighbors>

- Collaboration Query (e.g., querying if S0001 and S0010 have collaborated):
<query_adjacent>S0001,S0010</query_adjacent>

- Collaborator Count Query (e.g., querying the number of collaborators of S0001):
<query_degree>S0001</query_degree>

When submitting the final answer, list all collaborators of the target scholar {target_node} (order does not matter), using this format:

<answer>S0000,S1000,S1011,S1110</answer>
"""

    contextualized_rule_zh_4 = """\
【制造业/工业场景】我们现在来进行一项供应链依赖网络分析。
游戏设定了16个生产单元，标识为：S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111。它们构成了一个物料流转网络。

你的目标是推断出目标生产单元 {target_node} 的全部直接关联单元。注意：你不能对目标生产单元 {target_node} 本身进行任何查询，否则将被判定为非法操作。

你可以通过以下三类查询获取信息（每次仅限一个查询）：

1. 关联单元列表查询（类型A，最多 {quota_a} 次）：询问某个生产单元的全部直接关联单元列表。我会返回其所有的关联单元，按字典序升序排列。
2. 是否流转查询（类型B，最多 {quota_b} 次）：询问两个生产单元之间是否存在直接物料流转。我会回答"是"或"否"。
3. 关联数量查询（类型C，最多 {quota_c} 次）：询问某个生产单元的直接关联单元总数。我会回答一个非负整数。

请注意：
- 所有查询的生产单元必须是上述16个之一，且不能是目标生产单元 {target_node}。
- 每类查询都有次数限制，超过限制将导致游戏失败。
- 如果你对目标生产单元 {target_node} 发起查询累计达到3次，游戏将直接失败。

当你收集足够信息后，请提交最终答案。若答案不正确或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 关联单元列表查询（例如查询 S0001 的直接关联单元）：
<query_neighbors>S0001</query_neighbors>

- 是否流转查询（例如查询 S0001 和 S0010 是否有直接流转）：
<query_adjacent>S0001,S0010</query_adjacent>

- 关联数量查询（例如查询 S0001 的关联单元总数）：
<query_degree>S0001</query_degree>

提交最终答案时，请列出目标生产单元 {target_node} 的所有直接关联单元（顺序不限），格式如下：

<answer>S0000,S1000,S1011,S1110</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario] Let's analyze a supply chain dependency network.
There are 16 production units labeled: S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111. They form a material flow network.

Your goal is to infer all connected units of the target production unit {target_node}. Note: You cannot query the target production unit {target_node} itself, or it will be considered an illegal operation.

You can gather information through three types of queries (one query per turn):

1. Connected Units List Query (Type A, at most {quota_a} times): Ask for the complete list of directly connected units of a production unit. I will return all connected units in lexicographically ascending order.
2. Direct Flow Query (Type B, at most {quota_b} times): Ask if there is a direct material flow between two production units. I will answer "Yes" or "No".
3. Connections Count Query (Type C, at most {quota_c} times): Ask for the total number of connected units for a production unit. I will answer with a non-negative integer.

Please note:
- All queried production units must be one of the 16 listed above, and cannot be the target production unit {target_node}.
- Each query type has a usage limit; exceeding the limit will cause the game to fail.
- If you query the target production unit {target_node} 3 times in total, the game will fail immediately.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Connected Units List Query (e.g., querying connected units of S0001):
<query_neighbors>S0001</query_neighbors>

- Direct Flow Query (e.g., querying if S0001 and S0010 have direct flow):
<query_adjacent>S0001,S0010</query_adjacent>

- Connections Count Query (e.g., querying the number of connected units of S0001):
<query_degree>S0001</query_degree>

When submitting the final answer, list all directly connected units of the target production unit {target_node} (order does not matter), using this format:

<answer>S0000,S1000,S1011,S1110</answer>
"""

    contextualized_rule_zh_5 = """\
【法律场景】我们现在来进行一项企业反洗钱的资金往来网络分析。
游戏设定了16个实体账户，标识为：S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111。它们构成了一个资金交易网络。

你的目标是推断出目标实体账户 {target_node} 的全部直接交易账户。注意：你不能对目标实体账户 {target_node} 本身进行任何查询，否则将被判定为非法操作。

你可以通过以下三类查询获取信息（每次仅限一个查询）：

1. 交易账户列表查询（类型A，最多 {quota_a} 次）：询问某个实体账户的全部直接交易账户列表。我会返回其所有的交易账户，按字典序升序排列。
2. 是否交易查询（类型B，最多 {quota_b} 次）：询问两个实体账户之间是否有过直接资金往来。我会回答"是"或"否"。
3. 交易账户数量查询（类型C，最多 {quota_c} 次）：询问某个实体账户的直接交易账户总数。我会回答一个非负整数。

请注意：
- 所有查询的实体账户必须是上述16个之一，且不能是目标实体账户 {target_node}。
- 每类查询都有次数限制，超过限制将导致游戏失败。
- 如果你对目标实体账户 {target_node} 发起查询累计达到3次，游戏将直接失败。

当你收集足够信息后，请提交最终答案。若答案不正确或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 交易账户列表查询（例如查询 S0001 的直接交易账户）：
<query_neighbors>S0001</query_neighbors>

- 是否交易查询（例如查询 S0001 和 S0010 是否有直接往来）：
<query_adjacent>S0001,S0010</query_adjacent>

- 交易账户数量查询（例如查询 S0001 的交易账户总数）：
<query_degree>S0001</query_degree>

提交最终答案时，请列出目标实体账户 {target_node} 的所有直接交易账户（顺序不限），格式如下：

<answer>S0000,S1000,S1011,S1110</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario] Let's conduct an anti-money laundering financial transaction network analysis.
There are 16 entity accounts labeled: S0000, S0001, S0010, S0011, S0100, S0101, S0110, S0111, S1000, S1001, S1010, S1011, S1100, S1101, S1110, S1111. They form a financial transaction network.

Your goal is to infer all directly trading accounts of the target entity account {target_node}. Note: You cannot query the target entity account {target_node} itself, or it will be considered an illegal operation.

You can gather information through three types of queries (one query per turn):

1. Trading Accounts List Query (Type A, at most {quota_a} times): Ask for the complete list of directly trading accounts of an entity account. I will return all its trading accounts in lexicographically ascending order.
2. Direct Transaction Query (Type B, at most {quota_b} times): Ask if two entity accounts have had direct financial transactions. I will answer "Yes" or "No".
3. Trading Accounts Count Query (Type C, at most {quota_c} times): Ask for the total number of directly trading accounts for an entity account. I will answer with a non-negative integer.

Please note:
- All queried entity accounts must be one of the 16 listed above, and cannot be the target entity account {target_node}.
- Each query type has a usage limit; exceeding the limit will cause the game to fail.
- If you query the target entity account {target_node} 3 times in total, the game will fail immediately.

When you have gathered enough information, submit your final answer. If the answer is incorrect or the format is invalid, the game fails.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Trading Accounts List Query (e.g., querying directly trading accounts of S0001):
<query_neighbors>S0001</query_neighbors>

- Direct Transaction Query (e.g., querying if S0001 and S0010 have direct transactions):
<query_adjacent>S0001,S0010</query_adjacent>

- Trading Accounts Count Query (e.g., querying the number of trading accounts of S0001):
<query_degree>S0001</query_degree>

When submitting the final answer, list all directly trading accounts of the target entity account {target_node} (order does not matter), using this format:

<answer>S0000,S1000,S1011,S1110</answer>
"""

    tags = ["answer", "query_neighbors", "query_adjacent", "query_degree"]
    
    enable_counterfactual = False   # 设为 True 时开启反事实干预模式
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "target_node": "S0000",
                "quota_a": 8,
                "quota_b": 12,
                "quota_c": 15,
            },
            2: {
                "target_node": "S0101",
                "quota_a": 6,
                "quota_b": 10,
                "quota_c": 12,
            },
            3: {
                "target_node": "S1010",
                "quota_a": 6,
                "quota_b": 8,
                "quota_c": 10,
            },
            4: {
                "target_node": "S0111",
                "quota_a": 4,
                "quota_b": 6,
                "quota_c": 8,
            },
            5: {
                "target_node": "S1111",
                "quota_a": 3,
                "quota_b": 5,
                "quota_c": 6,
            },
        },
        "en": {
            1: {
                "target_node": "S0000",
                "quota_a": 8,
                "quota_b": 12,
                "quota_c": 15,
            },
            2: {
                "target_node": "S0101",
                "quota_a": 6,
                "quota_b": 10,
                "quota_c": 12,
            },
            3: {
                "target_node": "S1010",
                "quota_a": 6,
                "quota_b": 8,
                "quota_c": 10,
            },
            4: {
                "target_node": "S0111",
                "quota_a": 4,
                "quota_b": 6,
                "quota_c": 8,
            },
            5: {
                "target_node": "S1111",
                "quota_a": 3,
                "quota_b": 5,
                "quota_c": 6,
            },
        },
    }

    def __init__(self, config):
        # 初始化节点集合
        self.all_nodes = [
            "S0000", "S0001", "S0010", "S0011",
            "S0100", "S0101", "S0110", "S0111",
            "S1000", "S1001", "S1010", "S1011",
            "S1100", "S1101", "S1110", "S1111"
        ]
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是 int 类型

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.target_node = cfg["target_node"]
        self.quota_a = cfg["quota_a"]
        self.quota_b = cfg["quota_b"]
        self.quota_c = cfg["quota_c"]

        # 记录已使用的查询次数
        self.used_a = 0
        self.used_b = 0
        self.used_c = 0
        self.target_violations = 0  # 记录对目标节点的非法查询次数

        # 填充游戏信息
        self._game_info["target_node"] = self.target_node
        self._game_info["quota_a"] = self.quota_a
        self._game_info["quota_b"] = self.quota_b
        self._game_info["quota_c"] = self.quota_c

        # 构建图（基于汉明距离为1）
        self._build_graph()

    def _build_graph(self):
        """构建图的邻接关系：两节点相邻当且仅当其四位二进制后缀的汉明距离为1"""
        self.graph = {node: [] for node in self.all_nodes}
        
        for node1, node2 in itertools.combinations(self.all_nodes, 2):
            # 提取四位二进制后缀
            bits1 = node1[1:]  # 去掉'S'
            bits2 = node2[1:]
            
            # 计算汉明距离
            hamming_dist = sum(b1 != b2 for b1, b2 in zip(bits1, bits2))
            
            if hamming_dist == 1:
                self.graph[node1].append(node2)
                self.graph[node2].append(node1)
        
        # 排序邻居列表（字典序）
        for node in self.graph:
            self.graph[node].sort()

    def _check_node_valid(self, node):
        """检查节点是否有效且不是目标节点"""
        if node not in self.all_nodes:
            return False, "invalid_node"
        if node == self.target_node:
            self.target_violations += 1
            return False, "target_violation"
        return True, None

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        try:
            raw_ans = parsed_info["answer"].strip()
            # 解析答案中的节点列表
            if not raw_ans:
                return False
            
            model_neighbors = set(n.strip() for n in raw_ans.split(",") if n.strip())
            true_neighbors = set(self.graph[self.target_node])
            
            return model_neighbors == true_neighbors
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            illegal_res = "非法"
            quota_exceeded = "查询次数超限"
        else:
            yes_res, no_res = "Yes", "No"
            illegal_res = "Illegal"
            quota_exceeded = "Query quota exceeded"

        # 检查目标节点违规次数
        if self.target_violations >= 3:
            self.state.set_state("failed", "target_violation_limit")
            return illegal_res

        # 处理邻居列表查询
        if "query_neighbors" in parsed_info:
            if self.used_a >= self.quota_a:
                self.state.set_state("failed", "quota_a_exceeded")
                return quota_exceeded
            
            node = parsed_info["query_neighbors"].strip()
            valid, error_type = self._check_node_valid(node)
            
            if not valid:
                if error_type == "target_violation" and self.target_violations >= 3:
                    self.state.set_state("failed", "target_violation_limit")
                return illegal_res
            
            self.used_a += 1
            neighbors = self.graph[node]
            if not neighbors:
                return "[]"
            return "[" + ", ".join(neighbors) + "]"

        # 处理是否相邻查询
        elif "query_adjacent" in parsed_info:
            if self.used_b >= self.quota_b:
                self.state.set_state("failed", "quota_b_exceeded")
                return quota_exceeded
            
            try:
                raw = parsed_info["query_adjacent"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return illegal_res
                
                node1, node2 = parts
                
                # 先检查是否有目标节点，但只计一次违规
                has_target = (node1 == self.target_node or node2 == self.target_node)
                has_invalid = (node1 not in self.all_nodes or node2 not in self.all_nodes)
                
                if has_invalid:
                    return illegal_res
                
                if has_target:
                    self.target_violations += 1
                    if self.target_violations >= 3:
                        self.state.set_state("failed", "target_violation_limit")
                    return illegal_res
                
                self.used_b += 1
                is_adjacent = node2 in self.graph[node1]
                return yes_res if is_adjacent else no_res
            except:
                return illegal_res

        # 处理度数查询
        elif "query_degree" in parsed_info:
            if self.used_c >= self.quota_c:
                self.state.set_state("failed", "quota_c_exceeded")
                return quota_exceeded
            
            node = parsed_info["query_degree"].strip()
            valid, error_type = self._check_node_valid(node)
            
            if not valid:
                if error_type == "target_violation" and self.target_violations >= 3:
                    self.state.set_state("failed", "target_violation_limit")
                return illegal_res
            
            self.used_c += 1
            degree = len(self.graph[node])
            return str(degree)

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        
        # 预定义回答文本
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 遍历所有节点生成单节点查询（类型A和C）
        for node in self.all_nodes:
            # 跳过目标节点
            if node == self.target_node:
                continue
            
            # --- 类型A：邻居列表查询 ---
            neighbors = self.graph[node]
            # 格式化邻居列表
            if not neighbors:
                ans_neighbors = "[]"
            else:
                ans_neighbors = "[" + ", ".join(neighbors) + "]"
            
            queries.append({
                "query": f"<query_neighbors>{node}</query_neighbors>",
                "answer": ans_neighbors
            })

            # --- 类型C：度数查询 ---
            degree = len(neighbors)
            queries.append({
                "query": f"<query_degree>{node}</query_degree>",
                "answer": str(degree)
            })

        # 遍历节点对生成是否相邻查询（类型B）
        # 使用 combinations 避免重复 (A,B) 和 (B,A)，且不包含 (A,A)
        for node1, node2 in itertools.combinations(self.all_nodes, 2):
            # 只要有一个是目标节点，就跳过
            if node1 == self.target_node or node2 == self.target_node:
                continue
            
            # --- 类型B：是否相邻查询 ---
            # 检查相邻关系（无向图，查一边即可）
            is_adjacent = node2 in self.graph[node1]
            ans_adjacent = yes_res if is_adjacent else no_res
            
            queries.append({
                "query": f"<query_adjacent>{node1},{node2}</query_adjacent>",
                "answer": ans_adjacent
            })

        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文替换
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 英文替换（忽略大小写但保持格式，这里直接匹配常见的输出）
        correct_lower = correct.lower()
        if correct_lower == "yes":
            return "No"
        if correct_lower == "no":
            return "Yes"
        
        # 空列表
        if correct == "[]":
            # 返回一个假邻居
            fake_node = [n for n in self.all_nodes if n != self.target_node][0]
            return f"[{fake_node}]"
        
        # 邻居列表格式：[S0001, S0010, ...]
        if correct.startswith("[") and correct.endswith("]"):
            inner = correct[1:-1]
            neighbors = [n.strip() for n in inner.split(",") if n.strip()]
            if neighbors:
                # 移除最后一个邻居，或添加一个不存在的邻居来制造错误
                if len(neighbors) > 1:
                    # 移除一个邻居
                    wrong_neighbors = neighbors[:-1]
                else:
                    # 只有一个邻居时，替换为另一个节点
                    other = [n for n in self.all_nodes 
                             if n != self.target_node and n not in neighbors]
                    wrong_neighbors = [other[0]] if other else neighbors
                return "[" + ", ".join(wrong_neighbors) + "]"
        
        # 其他情况
        return correct + "_WRONG"