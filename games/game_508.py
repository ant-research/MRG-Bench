# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子节点列表：某给定节点的所有直接子节点有哪些
# ============================================================

from .base import Game
import re


class PrefixTreeRuleGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"前缀树规则推理"游戏，规则如下：

## 游戏设定

存在一棵有根前缀树，具有以下性质：
- 字母表为 {1, 2, 3, 4}
- 根节点标签为空串
- 其余节点标签为该字母表上的字符串，最大长度为 3
- 任一长度为 3 的标签为叶子节点，无子节点
- 总节点数固定为 {total_nodes} 个
- 树结构在交互过程中不改变

存在一条对所有节点一致、固定且未公开的确定性规则 R。对任一节点 x（长度小于 3），R(x) 返回一个非空子集 S(x)，该子集是 {1, 2, 3, 4} 的子集，该节点的直接子节点集合为 {x 拼接 d : d 属于 S(x)}。规则 R 不随交互变化。

## 你可以发起的查询

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. **计数查询**：询问节点 X 有多少个直接子节点。X 为空串（用"root"表示）或长度不超过 3 的数字串。回答为非负整数。

2. **成员查询**：询问标签 Y 是否是节点 X 的直接子节点。仅当 Y = X 拼接 d（d 属于 {1, 2, 3, 4}），且 X 长度小于 3 时为有效查询；否则答复"无效"。有效时答复"是"或"否"。

3. **叶子查询**：询问节点 X 是否为叶子。答复"是"或"否"（等价于计数是否为 0；当 X 长度为 3 时必为"是"）。

注意：总查询次数有限制，请尽可能高效地推理。

## 你的任务

在查询后，你需要推断并提交：
1. 规则 R 的确定性、可检验描述（能据此对任一长度小于 3 的标签计算其允许的下一位数字集合）
2. 节点 A="{target_a}" 的全部直接子节点标签，按数值升序列出
3. 节点 B="{target_b}" 的全部直接子节点标签，按数值升序列出

若规则描述与实际树不一致，或 A/B 的子节点列表有误，则判定失败。

## 查询与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 计数查询（例如询问节点"12"）：
<query_count>12</query_count>

- 计数查询（询问根节点）：
<query_count>root</query_count>

- 成员查询（例如询问"123"是否是"12"的子节点）：
<query_member>12,123</query_member>

- 叶子查询（例如询问"12"是否为叶子）：
<query_leaf>12</query_leaf>

提交最终答案时，必须包含规则描述、节点 A 的子节点列表、节点 B 的子节点列表，格式如下：

<answer>
rule=规则的自然语言描述
node_a={target_a},children=子节点1,子节点2,...
node_b={target_b},children=子节点1,子节点2,...
</answer>

例如：
<answer>
rule=每个节点的子节点集合为所有大于该节点最后一位数字的数字
node_a=13,children=134
node_b=24,children=
</answer>

注意：如果某节点无子节点（是叶子），children= 后面留空即可。
"""

    game_rule_en = """\
Let's play a "Prefix Tree Rule Inference" game. Here are the rules:

## Game Setting

There exists a rooted prefix tree with the following properties:
- Alphabet is {1, 2, 3, 4}
- Root node label is empty string
- Other node labels are strings over this alphabet, with maximum length 3
- Any label of length 3 is a leaf node with no children
- Total number of nodes is fixed at {total_nodes}
- Tree structure does not change during interaction

There exists a deterministic rule R that is consistent across all nodes, fixed, and undisclosed. For any node x (length less than 3), R(x) returns a non-empty subset S(x) which is a subset of {1, 2, 3, 4}, and the set of direct children of that node is {x concatenated with d : d in S(x)}. Rule R does not change during interaction.

## Available Queries

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

1. **Count Query**: Ask how many direct children node X has. X is either empty string (represented as "root") or a digit string of length at most 3. Answer is a non-negative integer.

2. **Member Query**: Ask if label Y is a direct child of node X. Only valid when Y = X concatenated with d (d in {1, 2, 3, 4}) and X has length less than 3; otherwise answer "invalid". When valid, answer "Yes" or "No".

3. **Leaf Query**: Ask if node X is a leaf. Answer "Yes" or "No" (equivalent to whether count is 0; when X has length 3, must be "Yes").

Note: Total number of queries is limited, please reason as efficiently as possible.

## Your Task

After querying, you need to infer and submit:
1. A deterministic, verifiable description of rule R (from which one can compute the allowed next digit set for any label of length less than 3)
2. All direct children labels of node A="{target_a}", listed in numerical ascending order
3. All direct children labels of node B="{target_b}", listed in numerical ascending order

If the rule description is inconsistent with the actual tree, or the child lists of A/B are incorrect, it is judged as failure.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about node "12"):
<query_count>12</query_count>

- Count Query (asking about root):
<query_count>root</query_count>

- Member Query (e.g., asking if "123" is a child of "12"):
<query_member>12,123</query_member>

- Leaf Query (e.g., asking if "12" is a leaf):
<query_leaf>12</query_leaf>

When submitting the final answer, must include rule description, child list of node A, and child list of node B, in the format:

<answer>
rule=natural language description of the rule
node_a={target_a},children=child1,child2,...
node_b={target_b},children=child1,child2,...
</answer>

For example:
<answer>
rule=Each node's children set consists of all digits greater than the last digit of that node
node_a=13,children=134
node_b=24,children=
</answer>

Note: If a node has no children (is a leaf), leave children= empty.
"""

    contextualized_rule_zh_1 = """\
[交通场景]
我们现在来体验一套"交通网络规划与连通性推理"系统，规则如下：

## 系统设定

存在一个核心枢纽路网结构（可视为有根前缀树），具有以下特征：
- 枢纽节点的可选分支干道代码为 {1, 2, 3, 4}
- 起点总指挥中心标记为空串（代表初始位置）
- 其余站点的路径编码为干道代码拼接的字符串，最大路径深度为 3
- 任一深度为 3 的路径为交通终端站，无下一站分支
- 系统内总合法站点节点数固定为 {total_nodes} 个
- 交通网络拓扑结构在查询期间保持不变

存在一条对所有节点一致、固定且未公开的连通分配规则 R。对于任一非终端节点 x（长度小于 3），规则 R(x) 返回一个非空分支子集 S(x)（包含于 {1, 2, 3, 4}），该节点的直接可达下一站集合为 {x 拼接 d : d 属于 S(x)}。规则 R 始终保持稳定。

## 你可以发起的查询

你可以反复向系统发起以下三类查询（每次仅限一个），系统将如实反馈：

1. **计数查询**：询问节点 X 有多少个直接可达的下一站。X 为空串（用"root"表示起点）或长度不超过 3 的路径数字串。回答为非负整数。
2. **成员查询**：询问站点 Y 是否是节点 X 的直接可达下一站。仅当 Y = X 拼接 d（d 属于 {1, 2, 3, 4}），且 X 长度小于 3 时为有效查询；否则答复"无效"。有效时答复"是"或"否"。
3. **叶子查询**：询问节点 X 是否为终端站（无下一站）。答复"是"或"否"（等价于下一站计数是否为 0；当 X 长度为 3 时必为"是"）。

注意：系统查询配额有限，请高效规划你的验证策略。

## 你的任务

完成查询后，你需要推断并提交：
1. 连通规则 R 的确定性、可检验描述（能据此对任一非终端节点计算其允许的下一站分支干道集合）
2. 节点 A="{target_a}" 的全部直接可达下一站路径代码，按数值升序列出
3. 节点 B="{target_b}" 的全部直接可达下一站路径代码，按数值升序列出

若规则描述与实际路网拓扑不一致，或 A/B 的直接下一站列表错误，则判定为推理失败。

## 查询与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 计数查询（例如询问节点"12"）：
<query_count>12</query_count>

- 计数查询（询问起点根节点）：
<query_count>root</query_count>

- 成员查询（例如询问"123"是否是"12"的下一站）：
<query_member>12,123</query_member>

- 叶子查询（例如询问"12"是否为终端站）：
<query_leaf>12</query_leaf>

提交最终答案时，必须包含规则描述、节点 A 的下一站列表、节点 B 的下一站列表，格式如下：

<answer>
rule=规则的自然语言描述
node_a={target_a},children=子节点1,子节点2,...
node_b={target_b},children=子节点1,子节点2,...
</answer>

例如：
<answer>
rule=每个节点的下一站集合为所有大于该节点最后一位数字的干道代码
node_a=13,children=134
node_b=24,children=
</answer>

注意：如果某节点无下一站（是终端站），children= 后面留空即可。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's experience a "Traffic Network Connectivity Inference" system. Here are the rules:

## System Setting

There exists a core hub network structure (modeled as a rooted prefix tree) with the following properties:
- The available branch route codes for hub nodes are {1, 2, 3, 4}
- The starting command center is marked with an empty string
- Other station route codes are strings of these route codes, with a maximum depth of 3
- Any route code of length 3 is a terminal station with no further branches
- Total number of valid station nodes is fixed at {total_nodes}
- The network topology does not change during interaction

There exists a deterministic connectivity allocation rule R that is consistent across all nodes, fixed, and undisclosed. For any non-terminal node x (length less than 3), R(x) returns a non-empty subset S(x) within {1, 2, 3, 4}, and the set of directly reachable next-station nodes is {x concatenated with d : d in S(x)}. Rule R remains stable.

## Available Queries

You can repeatedly ask three types of questions (one per turn), and the system will answer truthfully:

1. **Count Query**: Ask how many direct next stations node X has. X is either the empty string (represented as "root") or a route code string of length at most 3. Answer is a non-negative integer.
2. **Member Query**: Ask if station Y is a directly reachable next station of node X. Only valid when Y = X concatenated with d (d in {1, 2, 3, 4}) and X has length less than 3; otherwise answer "invalid". When valid, answer "Yes" or "No".
3. **Leaf Query**: Ask if node X is a terminal station. Answer "Yes" or "No" (equivalent to whether the next station count is 0; when X has length 3, must be "Yes").

Note: Query quota is limited, please plan your validation strategy efficiently.

## Your Task

After querying, you need to infer and submit:
1. A deterministic, verifiable description of connectivity rule R (from which one can compute the allowed next route code set for any non-terminal node)
2. All direct next station codes of node A="{target_a}", listed in numerical ascending order
3. All direct next station codes of node B="{target_b}", listed in numerical ascending order

If the rule description is inconsistent with the actual network, or the next station lists of A/B are incorrect, it is judged as a failure.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about node "12"):
<query_count>12</query_count>

- Count Query (asking about root):
<query_count>root</query_count>

- Member Query (e.g., asking if "123" is a next station of "12"):
<query_member>12,123</query_member>

- Leaf Query (e.g., asking if "12" is a terminal station):
<query_leaf>12</query_leaf>

When submitting the final answer, must include rule description, next station list of node A, and next station list of node B, in the format:

<answer>
rule=natural language description of the rule
node_a={target_a},children=child1,child2,...
node_b={target_b},children=child1,child2,...
</answer>

For example:
<answer>
rule=Each node's next station set consists of all route codes greater than the last digit of that node
node_a=13,children=134
node_b=24,children=
</answer>

Note: If a node has no next stations (is a terminal), leave children= empty.
"""

    contextualized_rule_zh_2 = """\
[医疗场景]
我们现在来体验一套"疾病演化路径推理"系统，规则如下：

## 系统设定

存在一个核心病程演化网络，具有以下特征：
- 基础病理指征或治疗代码为 {1, 2, 3, 4}
- 初始健康状态或初诊标记为空串（代表起点）
- 其余病程状态编码为指征代码拼接的字符串，最大病程演化深度为 3
- 任一深度为 3 的病程状态为终末转归状态，不再产生新指征
- 系统内总合法状态节点数固定为 {total_nodes} 个
- 病程演化拓扑在查询期间保持不变

存在一条对所有状态一致、固定且未公开的演化规律 R。对于任一非终末状态 x（长度小于 3），规律 R(x) 返回一个非空后续指征子集 S(x)（包含于 {1, 2, 3, 4}），该状态的直接后续病程状态集合为 {x 拼接 d : d 属于 S(x)}。规律 R 始终保持稳定。

## 你可以发起的查询

你可以反复向系统发起以下三类查询（每次仅限一个），系统将如实反馈：

1. **计数查询**：询问病程状态 X 有多少个直接后续状态。X 为空串（用"root"表示初诊）或长度不超过 3 的状态代码。回答为非负整数。
2. **成员查询**：询问状态 Y 是否是状态 X 的直接后续状态。仅当 Y = X 拼接 d（d 属于 {1, 2, 3, 4}），且 X 长度小于 3 时为有效查询；否则答复"无效"。有效时答复"是"或"否"。
3. **叶子查询**：询问状态 X 是否为终末转归状态（无后续）。答复"是"或"否"（等价于后续状态计数是否为 0；当 X 长度为 3 时必为"是"）。

注意：系统查询配额有限，请高效规划你的验证策略。

## 你的任务

完成查询后，你需要推断并提交：
1. 演化规律 R 的确定性、可检验描述（能据此对任一非终末状态计算其允许的下一阶段指征代码集合）
2. 状态 A="{target_a}" 的全部直接后续状态代码，按数值升序列出
3. 状态 B="{target_b}" 的全部直接后续状态代码，按数值升序列出

若规律描述与实际演化网络不一致，或 A/B 的直接后续状态列表错误，则判定为失败。

## 查询与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 计数查询（例如询问状态"12"）：
<query_count>12</query_count>

- 计数查询（询问初诊根节点）：
<query_count>root</query_count>

- 成员查询（例如询问"123"是否是"12"的后续状态）：
<query_member>12,123</query_member>

- 叶子查询（例如询问"12"是否为终末转归状态）：
<query_leaf>12</query_leaf>

提交最终答案时，必须包含规律描述、状态 A 的后续列表、状态 B 的后续列表，格式如下：

<answer>
rule=规律的自然语言描述
node_a={target_a},children=子状态1,子状态2,...
node_b={target_b},children=子状态1,子状态2,...
</answer>

例如：
<answer>
rule=每个状态的后续指征集合为所有大于该状态最后一位代码的指征代码
node_a=13,children=134
node_b=24,children=
</answer>

注意：如果某状态无后续状态（是终末转归），children= 后面留空即可。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's use a "Disease Evolution Path Inference" system. Here are the rules:

## System Setting

There exists a core disease evolution network with the following properties:
- The basic pathological indicator or treatment codes are {1, 2, 3, 4}
- The initial health state or initial diagnosis mark is represented by an empty string
- Other disease stage codes are strings of these indicator codes, with a maximum evolution depth of 3
- Any stage code of length 3 is a terminal outcome state with no new indicators
- Total number of valid state nodes is fixed at {total_nodes}
- The evolution topology does not change during interaction

There exists a deterministic evolution rule R that is consistent across all states, fixed, and undisclosed. For any non-terminal state x (length less than 3), R(x) returns a non-empty subset S(x) within {1, 2, 3, 4}, and the set of direct subsequent states is {x concatenated with d : d in S(x)}. Rule R remains stable.

## Available Queries

You can repeatedly ask three types of questions (one per turn), and the system will answer truthfully:

1. **Count Query**: Ask how many direct subsequent states state X has. X is either the empty string (represented as "root") or a stage code string of length at most 3. Answer is a non-negative integer.
2. **Member Query**: Ask if state Y is a direct subsequent state of state X. Only valid when Y = X concatenated with d (d in {1, 2, 3, 4}) and X has length less than 3; otherwise answer "invalid". When valid, answer "Yes" or "No".
3. **Leaf Query**: Ask if state X is a terminal outcome state. Answer "Yes" or "No" (equivalent to whether the subsequent state count is 0; when X has length 3, must be "Yes").

Note: Query quota is limited, please plan your validation strategy efficiently.

## Your Task

After querying, you need to infer and submit:
1. A deterministic, verifiable description of evolution rule R (from which one can compute the allowed next indicator code set for any non-terminal state)
2. All direct subsequent state codes of state A="{target_a}", listed in numerical ascending order
3. All direct subsequent state codes of state B="{target_b}", listed in numerical ascending order

If the rule description is inconsistent with the actual evolution network, or the subsequent state lists of A/B are incorrect, it is judged as a failure.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about state "12"):
<query_count>12</query_count>

- Count Query (asking about root):
<query_count>root</query_count>

- Member Query (e.g., asking if "123" is a subsequent state of "12"):
<query_member>12,123</query_member>

- Leaf Query (e.g., asking if "12" is a terminal outcome state):
<query_leaf>12</query_leaf>

When submitting the final answer, must include rule description, subsequent list of state A, and subsequent list of state B, in the format:

<answer>
rule=natural language description of the rule
node_a={target_a},children=child1,child2,...
node_b={target_b},children=child1,child2,...
</answer>

For example:
<answer>
rule=Each state's subsequent indicator set consists of all codes greater than the last digit of that state
node_a=13,children=134
node_b=24,children=
</answer>

Note: If a state has no subsequent states (is a terminal outcome), leave children= empty.
"""

    contextualized_rule_zh_3 = """\
[教育场景]
我们现在来体验一套"学习路径与课程解锁推理"系统，规则如下：

## 系统设定

存在一个核心课程进阶网络，具有以下特征：
- 基础进阶模块代码为 {1, 2, 3, 4}
- 初始学习起点（零基础）标记为空串
- 其余学习路径编码为模块代码拼接的字符串，最大进阶深度为 3
- 任一深度为 3 的学习阶段为学业终点，无后续可修模块
- 系统内总合法学习节点数固定为 {total_nodes} 个
- 课程解锁拓扑结构在查询期间保持不变

存在一条对所有阶段一致、固定且未公开的课程解锁机制 R。对于任一非终点阶段 x（长度小于 3），机制 R(x) 返回一个非空后续模块子集 S(x)（包含于 {1, 2, 3, 4}），该阶段直接解锁的后续课程组合为 {x 拼接 d : d 属于 S(x)}。机制 R 始终保持稳定。

## 你可以发起的查询

你可以反复向系统发起以下三类查询（每次仅限一个），系统将如实反馈：

1. **计数查询**：询问学习阶段 X 之后直接解锁了几门后续课程。X 为空串（用"root"表示）或长度不超过 3 的路径代码。回答为非负整数。
2. **成员查询**：询问学习路径 Y 是否是阶段 X 的直接后续解锁路径。仅当 Y = X 拼接 d（d 属于 {1, 2, 3, 4}），且 X 长度小于 3 时为有效查询；否则答复"无效"。有效时答复"是"或"否"。
3. **叶子查询**：询问阶段 X 是否为学业终点。答复"是"或"否"（等价于解锁计数是否为 0；当 X 长度为 3 时必为"是"）。

注意：系统查询配额有限，请高效规划你的验证策略。

## 你的任务

完成查询后，你需要推断并提交：
1. 课程解锁机制 R 的确定性、可检验描述（能据此对任一非终点阶段计算其允许的直接选修模块集合）
2. 阶段 A="{target_a}" 的全部直接解锁课程路径，按数值升序列出
3. 阶段 B="{target_b}" 的全部直接解锁课程路径，按数值升序列出

若机制描述与实际课程网络不一致，或 A/B 的直接解锁列表错误，则判定为失败。

## 查询与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 计数查询（例如询问阶段"12"）：
<query_count>12</query_count>

- 计数查询（询问初始起点）：
<query_count>root</query_count>

- 成员查询（例如询问"123"是否是"12"的后续路径）：
<query_member>12,123</query_member>

- 叶子查询（例如询问"12"是否为学业终点）：
<query_leaf>12</query_leaf>

提交最终答案时，必须包含机制描述、阶段 A 的解锁列表、阶段 B 的解锁列表，格式如下：

<answer>
rule=机制的自然语言描述
node_a={target_a},children=子路径1,子路径2,...
node_b={target_b},children=子路径1,子路径2,...
</answer>

例如：
<answer>
rule=每个阶段的直接解锁集合为所有大于该阶段最后一位代码的模块代码
node_a=13,children=134
node_b=24,children=
</answer>

注意：如果某阶段无解锁课程（是学业终点），children= 后面留空即可。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's experience a "Learning Path and Course Unlock Inference" system. Here are the rules:

## System Setting

There exists a core course progression network with the following properties:
- The basic advanced module codes are {1, 2, 3, 4}
- The initial learning starting point (zero basis) is marked with an empty string
- Other learning path codes are strings of these module codes, with a maximum progression depth of 3
- Any learning stage of length 3 is an academic terminal point, with no further modules available
- Total number of valid learning nodes is fixed at {total_nodes}
- The course unlock topology does not change during interaction

There exists a deterministic course unlock mechanism R that is consistent across all stages, fixed, and undisclosed. For any non-terminal stage x (length less than 3), mechanism R(x) returns a non-empty subsequent module subset S(x) within {1, 2, 3, 4}, and the set of directly unlocked subsequent courses is {x concatenated with d : d in S(x)}. Mechanism R remains stable.

## Available Queries

You can repeatedly ask three types of questions (one per turn), and the system will answer truthfully:

1. **Count Query**: Ask how many subsequent courses are directly unlocked after stage X. X is either the empty string (represented as "root") or a path code string of length at most 3. Answer is a non-negative integer.
2. **Member Query**: Ask if learning path Y is a directly unlocked subsequent path of stage X. Only valid when Y = X concatenated with d (d in {1, 2, 3, 4}) and X has length less than 3; otherwise answer "invalid". When valid, answer "Yes" or "No".
3. **Leaf Query**: Ask if stage X is an academic terminal point. Answer "Yes" or "No" (equivalent to whether the unlock count is 0; when X has length 3, must be "Yes").

Note: Query quota is limited, please plan your validation strategy efficiently.

## Your Task

After querying, you need to infer and submit:
1. A deterministic, verifiable description of unlock mechanism R (from which one can compute the allowed direct module set for any non-terminal stage)
2. All directly unlocked course paths of stage A="{target_a}", listed in numerical ascending order
3. All directly unlocked course paths of stage B="{target_b}", listed in numerical ascending order

If the mechanism description is inconsistent with the actual course network, or the unlock lists of A/B are incorrect, it is judged as a failure.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about stage "12"):
<query_count>12</query_count>

- Count Query (asking about starting point):
<query_count>root</query_count>

- Member Query (e.g., asking if "123" is a subsequent path of "12"):
<query_member>12,123</query_member>

- Leaf Query (e.g., asking if "12" is an academic terminal point):
<query_leaf>12</query_leaf>

When submitting the final answer, must include mechanism description, unlock list of stage A, and unlock list of stage B, in the format:

<answer>
rule=natural language description of the mechanism
node_a={target_a},children=child1,child2,...
node_b={target_b},children=child1,child2,...
</answer>

For example:
<answer>
rule=Each stage's direct unlock set consists of all module codes greater than the last digit of that stage
node_a=13,children=134
node_b=24,children=
</answer>

Note: If a stage has no unlocked courses (is an academic terminal point), leave children= empty.
"""

    contextualized_rule_zh_4 = """\
[工业制造场景]
我们现在来体验一套"工艺流转与加工控制推理"系统，规则如下：

## 系统设定

存在一个核心生产线调度网络，具有以下特征：
- 加工车间或工序代码为 {1, 2, 3, 4}
- 初始毛坯部件标记为空串（代表起点）
- 其余加工流转码为工序代码拼接的字符串，最大加工深度为 3
- 任一深度为 3 的流转码对应成品状态，无后续工序
- 系统内总合法流转节点数固定为 {total_nodes} 个
- 工艺流转拓扑结构在查询期间保持不变

存在一条对所有状态一致、固定且未公开的工艺流转控制规则 R。对于任一非成品状态 x（长度小于 3），规则 R(x) 返回一个非空后续工序子集 S(x)（包含于 {1, 2, 3, 4}），该状态直接合法的后续加工状态集合为 {x 拼接 d : d 属于 S(x)}。规则 R 始终保持稳定。

## 你可以发起的查询

你可以反复向系统发起以下三类查询（每次仅限一个），系统将如实反馈：

1. **计数查询**：询问工序状态 X 有多少个合法的直接后续工序。X 为空串（用"root"表示）或长度不超过 3 的流转码。回答为非负整数。
2. **成员查询**：询问加工流转码 Y 是否是状态 X 的合法的直接后续状态。仅当 Y = X 拼接 d（d 属于 {1, 2, 3, 4}），且 X 长度小于 3 时为有效查询；否则答复"无效"。有效时答复"是"或"否"。
3. **叶子查询**：询问状态 X 是否为成品状态。答复"是"或"否"（等价于后续工序计数是否为 0；当 X 长度为 3 时必为"是"）。

注意：系统查询配额有限，请高效规划你的验证策略。

## 你的任务

完成查询后，你需要推断并提交：
1. 流转控制规则 R 的确定性、可检验描述（能据此对任一非成品状态计算其允许的直接后续车间集合）
2. 状态 A="{target_a}" 的全部直接后续加工流转码，按数值升序列出
3. 状态 B="{target_b}" 的全部直接后续加工流转码，按数值升序列出

若规则描述与实际生产调度网络不一致，或 A/B 的直接后续列表错误，则判定为失败。

## 查询与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 计数查询（例如询问状态"12"）：
<query_count>12</query_count>

- 计数查询（询问毛坯起点）：
<query_count>root</query_count>

- 成员查询（例如询问"123"是否是"12"的后续状态）：
<query_member>12,123</query_member>

- 叶子查询（例如询问"12"是否为成品状态）：
<query_leaf>12</query_leaf>

提交最终答案时，必须包含规则描述、状态 A 的后续列表、状态 B 的后续列表，格式如下：

<answer>
rule=规则的自然语言描述
node_a={target_a},children=子状态1,子状态2,...
node_b={target_b},children=子状态1,子状态2,...
</answer>

例如：
<answer>
rule=每个状态的直接后续工序集合为所有大于该状态最后一位代码的车间代码
node_a=13,children=134
node_b=24,children=
</answer>

注意：如果某状态无后续工序（是成品状态），children= 后面留空即可。
"""

    contextualized_rule_en_4 = """\
[Industry Scenario]
Let's use a "Process Routing and Manufacturing Control Inference" system. Here are the rules:

## System Setting

There exists a core production line scheduling network with the following properties:
- The processing workshop or step codes are {1, 2, 3, 4}
- The initial roughcast component is marked with an empty string
- Other processing routing codes are strings of these step codes, with a maximum processing depth of 3
- Any routing code of length 3 is a finished product state, with no subsequent steps
- Total number of valid routing nodes is fixed at {total_nodes}
- The process routing topology does not change during interaction

There exists a deterministic process routing control rule R that is consistent across all states, fixed, and undisclosed. For any non-finished state x (length less than 3), rule R(x) returns a non-empty subsequent step subset S(x) within {1, 2, 3, 4}, and the set of valid direct subsequent processing states is {x concatenated with d : d in S(x)}. Rule R remains stable.

## Available Queries

You can repeatedly ask three types of questions (one per turn), and the system will answer truthfully:

1. **Count Query**: Ask how many valid direct subsequent steps state X has. X is either the empty string (represented as "root") or a routing code string of length at most 3. Answer is a non-negative integer.
2. **Member Query**: Ask if processing routing code Y is a valid direct subsequent state of state X. Only valid when Y = X concatenated with d (d in {1, 2, 3, 4}) and X has length less than 3; otherwise answer "invalid". When valid, answer "Yes" or "No".
3. **Leaf Query**: Ask if state X is a finished product state. Answer "Yes" or "No" (equivalent to whether the subsequent step count is 0; when X has length 3, must be "Yes").

Note: Query quota is limited, please plan your validation strategy efficiently.

## Your Task

After querying, you need to infer and submit:
1. A deterministic, verifiable description of routing control rule R (from which one can compute the allowed direct workshop set for any non-finished state)
2. All direct subsequent routing codes of state A="{target_a}", listed in numerical ascending order
3. All direct subsequent routing codes of state B="{target_b}", listed in numerical ascending order

If the rule description is inconsistent with the actual scheduling network, or the subsequent lists of A/B are incorrect, it is judged as a failure.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about state "12"):
<query_count>12</query_count>

- Count Query (asking about roughcast starting point):
<query_count>root</query_count>

- Member Query (e.g., asking if "123" is a subsequent state of "12"):
<query_member>12,123</query_member>

- Leaf Query (e.g., asking if "12" is a finished product state):
<query_leaf>12</query_leaf>

When submitting the final answer, must include rule description, subsequent list of state A, and subsequent list of state B, in the format:

<answer>
rule=natural language description of the rule
node_a={target_a},children=child1,child2,...
node_b={target_b},children=child1,child2,...
</answer>

For example:
<answer>
rule=Each state's direct subsequent step set consists of all workshop codes greater than the last digit of that state
node_a=13,children=134
node_b=24,children=
</answer>

Note: If a state has no subsequent steps (is a finished product), leave children= empty.
"""

    contextualized_rule_zh_5 = """\
[法律场景]
我们现在来体验一套"法定程序流转推理"系统，规则如下：

## 系统设定

存在一个核心案件审理推演网络，具有以下特征：
- 法律程序分支代码为 {1, 2, 3, 4}
- 初始立案案卷标记为空串（代表起点）
- 其余案件阶段编码为程序代码拼接的字符串，最大审理深度为 3
- 任一深度为 3 的案件阶段代表结案终审状态，无后续法律程序
- 系统内总合法案卷节点数固定为 {total_nodes} 个
- 法定程序网络拓扑在查询期间保持不变

存在一条对所有阶段一致、固定且未公开的法定程序流转规则 R。对于任一非结案阶段 x（长度小于 3），规则 R(x) 返回一个非空后续程序子集 S(x)（包含于 {1, 2, 3, 4}），该阶段允许的直接后续案件阶段集合为 {x 拼接 d : d 属于 S(x)}。规则 R 始终保持稳定。

## 你可以发起的查询

你可以反复向系统发起以下三类查询（每次仅限一个），系统将如实反馈：

1. **计数查询**：询问案卷状态 X 能衍生出几个合法的直接后续程序。X 为空串（用"root"表示）或长度不超过 3 的阶段代码。回答为非负整数。
2. **成员查询**：询问案件阶段 Y 是否是状态 X 的合法的直接后续阶段。仅当 Y = X 拼接 d（d 属于 {1, 2, 3, 4}），且 X 长度小于 3 时为有效查询；否则答复"无效"。有效时答复"是"或"否"。
3. **叶子查询**：询问状态 X 是否为结案终审状态。答复"是"或"否"（等价于后续程序计数是否为 0；当 X 长度为 3 时必为"是"）。

注意：系统查询配额有限，请高效规划你的验证策略。

## 你的任务

完成查询后，你需要推断并提交：
1. 程序流转规则 R 的确定性、可检验描述（能据此对任一非结案阶段计算其允许的直接后续程序代码集合）
2. 状态 A="{target_a}" 的全部直接后续阶段代码，按数值升序列出
3. 状态 B="{target_b}" 的全部直接后续阶段代码，按数值升序列出

若规则描述与实际推演网络不一致，或 A/B 的直接后续列表错误，则判定为失败。

## 查询与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 计数查询（例如询问状态"12"）：
<query_count>12</query_count>

- 计数查询（询问初始立案）：
<query_count>root</query_count>

- 成员查询（例如询问"123"是否是"12"的后续阶段）：
<query_member>12,123</query_member>

- 叶子查询（例如询问"12"是否为结案终审状态）：
<query_leaf>12</query_leaf>

提交最终答案时，必须包含规则描述、状态 A 的后续列表、状态 B 的后续列表，格式如下：

<answer>
rule=规则的自然语言描述
node_a={target_a},children=子阶段1,子阶段2,...
node_b={target_b},children=子阶段1,子阶段2,...
</answer>

例如：
<answer>
rule=每个阶段的直接后续程序集合为所有大于该阶段最后一位代码的分支代码
node_a=13,children=134
node_b=24,children=
</answer>

注意：如果某状态无后续程序（是结案终审状态），children= 后面留空即可。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's use a "Statutory Procedure Routing Inference" system. Here are the rules:

## System Setting

There exists a core case trial deduction network with the following properties:
- The legal procedure branch codes are {1, 2, 3, 4}
- The initial case filing is marked with an empty string
- Other case stage codes are strings of these procedure codes, with a maximum trial depth of 3
- Any case stage of length 3 represents a final closed case state, with no subsequent legal procedures
- Total number of valid case file nodes is fixed at {total_nodes}
- The statutory procedure topology does not change during interaction

There exists a deterministic statutory procedure routing rule R that is consistent across all stages, fixed, and undisclosed. For any non-closed stage x (length less than 3), rule R(x) returns a non-empty subsequent procedure subset S(x) within {1, 2, 3, 4}, and the set of allowed direct subsequent case stages is {x concatenated with d : d in S(x)}. Rule R remains stable.

## Available Queries

You can repeatedly ask three types of questions (one per turn), and the system will answer truthfully:

1. **Count Query**: Ask how many valid direct subsequent procedures case state X can derive. X is either the empty string (represented as "root") or a stage code string of length at most 3. Answer is a non-negative integer.
2. **Member Query**: Ask if case stage Y is a valid direct subsequent stage of state X. Only valid when Y = X concatenated with d (d in {1, 2, 3, 4}) and X has length less than 3; otherwise answer "invalid". When valid, answer "Yes" or "No".
3. **Leaf Query**: Ask if state X is a final closed case state. Answer "Yes" or "No" (equivalent to whether the subsequent procedure count is 0; when X has length 3, must be "Yes").

Note: Query quota is limited, please plan your validation strategy efficiently.

## Your Task

After querying, you need to infer and submit:
1. A deterministic, verifiable description of routing rule R (from which one can compute the allowed direct procedure code set for any non-closed stage)
2. All direct subsequent stage codes of state A="{target_a}", listed in numerical ascending order
3. All direct subsequent stage codes of state B="{target_b}", listed in numerical ascending order

If the rule description is inconsistent with the actual deduction network, or the subsequent lists of A/B are incorrect, it is judged as a failure.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about state "12"):
<query_count>12</query_count>

- Count Query (asking about initial case filing):
<query_count>root</query_count>

- Member Query (e.g., asking if "123" is a subsequent stage of "12"):
<query_member>12,123</query_member>

- Leaf Query (e.g., asking if "12" is a final closed case state):
<query_leaf>12</query_leaf>

When submitting the final answer, must include rule description, subsequent list of state A, and subsequent list of state B, in the format:

<answer>
rule=natural language description of the rule
node_a={target_a},children=child1,child2,...
node_b={target_b},children=child1,child2,...
</answer>

For example:
<answer>
rule=Each stage's direct subsequent procedure set consists of all branch codes greater than the last digit of that stage
node_a=13,children=134
node_b=24,children=
</answer>

Note: If a state has no subsequent procedures (is a closed state), leave children= empty.
"""

    tags = ["answer", "query_count", "query_member", "query_leaf"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "total_nodes": 15,
                "rule_type": "last_gte_2",  # 最后一位 >= 2
                "target_a": "13",
                "target_b": "24",
            },
            2: {
                "total_nodes": 15,
                "rule_type": "last_odd",  # 最后一位为奇数
                "target_a": "13",
                "target_b": "24",
            },
            3: {
                "total_nodes": 15,
                "rule_type": "last_lt_3",  # 最后一位 < 3
                "target_a": "12",
                "target_b": "23",
            },
            4: {
                "total_nodes": 15,
                "rule_type": "digit_sum_even",  # 数字和为偶数
                "target_a": "13",
                "target_b": "22",
            },
            5: {
                "total_nodes": 15,
                "rule_type": "last_neq_prev",  # 最后一位不等于倒数第二位
                "target_a": "11",
                "target_b": "22",
            },
        },
        "en": {
            1: {
                "total_nodes": 15,
                "rule_type": "last_gte_2",
                "target_a": "13",
                "target_b": "24",
            },
            2: {
                "total_nodes": 15,
                "rule_type": "last_odd",
                "target_a": "13",
                "target_b": "24",
            },
            3: {
                "total_nodes": 15,
                "rule_type": "last_lt_3",
                "target_a": "12",
                "target_b": "23",
            },
            4: {
                "total_nodes": 15,
                "rule_type": "digit_sum_even",
                "target_a": "13",
                "target_b": "22",
            },
            5: {
                "total_nodes": 15,
                "rule_type": "last_neq_prev",
                "target_a": "11",
                "target_b": "22",
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 查询计数器
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，构建前缀树"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["total_nodes"] = cfg["total_nodes"]
        self._game_info["target_a"] = cfg["target_a"]
        self._game_info["target_b"] = cfg["target_b"]
        
        self.rule_type = cfg["rule_type"]
        self.target_a = cfg["target_a"]
        self.target_b = cfg["target_b"]
        
        # 构建前缀树
        self._build_tree()

    def _build_tree(self):
        """根据规则类型构建前缀树"""
        self.tree = {}  # 存储每个节点的子节点列表
        
        # 定义规则函数
        def get_children_by_rule(node: str) -> list:
            """根据规则返回节点的子节点集合"""
            if len(node) >= 3:
                return []
            
            candidates = ['1', '2', '3', '4']
            children = []
            
            if self.rule_type == "last_gte_2":
                # 最后一位 >= 2，即添加的数字 >= 2
                children = [node + d for d in candidates if int(d) >= 2]
                
            elif self.rule_type == "last_odd":
                # 最后一位为奇数
                children = [node + d for d in candidates if int(d) % 2 == 1]
                
            elif self.rule_type == "last_lt_3":
                # 最后一位 < 3
                children = [node + d for d in candidates if int(d) < 3]
                
            elif self.rule_type == "digit_sum_even":
                # 新节点的数字和为偶数
                for d in candidates:
                    new_node = node + d
                    digit_sum = sum(int(c) for c in new_node)
                    if digit_sum % 2 == 0:
                        children.append(new_node)
                        
            elif self.rule_type == "last_neq_prev":
                # 最后一位不等于倒数第二位
                if len(node) == 0:
                    # 根节点：所有数字都可以
                    children = [d for d in candidates]
                else:
                    last_digit = node[-1]
                    children = [node + d for d in candidates if d != last_digit]
            
            return children
        
        # BFS构建树
        queue = [""]  # 从空串（根节点）开始
        visited = set([""])
        
        while queue:
            node = queue.pop(0)
            children = get_children_by_rule(node)
            self.tree[node] = children
            
            for child in children:
                if child not in visited:
                    visited.add(child)
                    queue.append(child)

    def evaluate(self, parsed_info):
        """评估答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案
        lines = [line.strip() for line in raw_ans.strip().split('\n') if line.strip()]
        
        ans_dict = {}
        for line in lines:
            if '=' in line:
                key, value = line.split('=', 1)
                ans_dict[key.strip()] = value.strip()
        
        # 检查必需字段
        if "rule" not in ans_dict:
            return False
        
        # 提取节点A和B的子节点列表
        node_a_children = None
        node_b_children = None
        
        for key, value in ans_dict.items():
            if key.startswith("node_a"):
                # 格式：node_a=13,children=134,135
                parts = value.split(',children=')
                if len(parts) == 2:
                    children_str = parts[1].strip()
                    node_a_children = set(children_str.split(',')) if children_str else set()
            elif key.startswith("node_b"):
                parts = value.split(',children=')
                if len(parts) == 2:
                    children_str = parts[1].strip()
                    node_b_children = set(children_str.split(',')) if children_str else set()
        
        if node_a_children is None or node_b_children is None:
            return False
        
        # 获取正确答案
        correct_a = set(self.tree.get(self.target_a, []))
        correct_b = set(self.tree.get(self.target_b, []))
        
        # 验证
        return node_a_children == correct_a and node_b_children == correct_b

    def _cf_core_produce(self, parsed_info):
        """生成对查询的响应（原始逻辑）"""
        self.query_count += 1
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            invalid_res = "无效"
        else:
            yes_res, no_res = "Yes", "No"
            invalid_res = "Invalid"
        
        # 处理计数查询
        if "query_count" in parsed_info:
            node = parsed_info["query_count"].strip()
            if node.lower() == "root":
                node = ""
            
            if len(node) > 3:
                return invalid_res
            
            if node in self.tree:
                return str(len(self.tree[node]))
            else:
                return "0"
        
        # 处理成员查询
        elif "query_member" in parsed_info:
            try:
                raw = parsed_info["query_member"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_res
                
                parent, child = parts[0], parts[1]
                
                # 验证查询有效性
                if len(parent) >= 3:
                    return invalid_res
                if len(child) != len(parent) + 1:
                    return invalid_res
                if not child.startswith(parent):
                    return invalid_res
                if child[-1] not in ['1', '2', '3', '4']:
                    return invalid_res
                
                # 检查是否为子节点
                if parent in self.tree:
                    return yes_res if child in self.tree[parent] else no_res
                else:
                    return no_res
                    
            except:
                return invalid_res
        
        # 处理叶子查询
        elif "query_leaf" in parsed_info:
            node = parsed_info["query_leaf"].strip()
            
            if len(node) > 3:
                return invalid_res
            
            # 长度为3的节点必为叶子
            if len(node) == 3:
                return yes_res
            
            # 检查是否有子节点
            if node in self.tree:
                return no_res if len(self.tree[node]) > 0 else yes_res
            else:
                return yes_res
        
        else:
            raise ValueError("No valid query tag found.")

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
        original_count = self.query_count
        
        # 生成所有可能的节点标签
        nodes = [""]
        current_level = [""]
        # 生成直到长度为3的所有节点
        for _ in range(3):
            next_level = []
            for node in current_level:
                for d in ['1', '2', '3', '4']:
                    child = node + d
                    next_level.append(child)
            nodes.extend(next_level)
            current_level = next_level
            
        for node in nodes:
            # 1. 计数查询
            # 根节点用 "root" 表示
            q_node = "root" if node == "" else node
            query_str = f"<query_count>{q_node}</query_count>"
            
            # 模拟解析后的 info
            parsed = {"query_count": q_node}
            
            # 调用核心逻辑获取答案（需暂存计数器）
            ans = self._cf_core_produce(parsed)
            # 恢复计数器
            self.query_count = original_count
            
            queries.append({
                "query": query_str,
                "answer": ans
            })
            
            # 2. 叶子查询
            query_str = f"<query_leaf>{q_node}</query_leaf>"
            parsed = {"query_leaf": q_node}
            ans = self._cf_core_produce(parsed)
            self.query_count = original_count
            
            queries.append({
                "query": query_str,
                "answer": ans
            })
            
            # 3. 成员查询
            # 仅当节点长度 < 3 时有效
            if len(node) < 3:
                for d in ['1', '2', '3', '4']:
                    child = node + d
                    # 成员查询中，根节点一般通过空串拼接，如 ",1"
                    # 这里直接使用 node (如果是空串则为空)
                    member_val = f"{node},{child}"
                    query_str = f"<query_member>{member_val}</query_member>"
                    parsed = {"query_member": member_val}
                    
                    ans = self._cf_core_produce(parsed)
                    self.query_count = original_count
                    
                    queries.append({
                        "query": query_str,
                        "answer": ans
                    })
                    
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        """将正确的查询响应篡改为错误值，用于反事实干预"""
        is_zh = self.config.language == "zh"

        # 处理是/否响应（成员查询、叶子查询）
        if is_zh:
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
        else:
            if correct == "Yes":
                return "No"
            if correct == "No":
                return "Yes"

        # 处理无效响应（不应被反事实干预，但作为保底）
        if correct in ("无效", "Invalid"):
            return correct

        # 处理计数查询响应（非负整数字符串）
        try:
            val = int(correct)
            # 将计数加1作为错误值（确保不为负数）
            return str(val + 1)
        except ValueError:
            pass

        return correct + "_WRONG"