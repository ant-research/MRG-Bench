from .base import Game
import re

class TreeRootDiscoveryGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "树"

    game_rule_zh = """\
我们来玩一个"树根推理"游戏，规则如下：

游戏设定了一个包含 11 个节点的连通无向树，节点编号为 1 到 11，边的连接关系如下：
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

我已秘密选择了一个根节点 r，该根节点在候选集合 {root_candidates} 中，且在整个游戏过程中保持不变。

定义：第 k 层是指所有与根节点 r 的图距离为 k-1 的节点集合（k 为正整数，k 大于等于 1）。例如，第 1 层就是根节点本身（距离为 0），第 2 层是与根节点距离为 1 的所有节点。

你的目标是：
1. 推断出隐藏的根节点 r 是哪一个
2. 找出第 4 层（即与根节点距离为 3 的所有节点）包含哪些节点，并按升序排列

你可以向我提出两类查询问题，我会根据真实设定如实回答：

1. 数量查询：询问"第 k 层有多少个节点？"（其中 k 为 1 到 11 之间的整数）。我会回答一个整数（若该层不存在节点则回答 0）。
2. 成员查询：询问"节点 x 是否在第 k 层？"（其中 x 为 1 到 11 之间的节点编号，k 为 1 到 11 之间的整数）。我会回答"是"或"否"。

注意：
- 请尽可能少地使用查询次数
- 不支持一次性列出某层全部节点的查询
- 不支持复合或模糊条件的查询
- 所有反馈严格基于同一个隐藏根节点的层结构

每次查询只能包含一个标签。请使用以下 XML 格式：

- 数量查询（例如询问第 3 层的节点数量）：
<query_count>3</query_count>

- 成员查询（例如询问节点 5 是否在第 2 层）：
<query_member>5,2</query_member>

提交最终答案时，必须说明根节点编号和第 4 层的所有节点编号（用逗号隔开，按升序排列），格式如下：

<answer>root=2, layer4=7,8,9</answer>
"""

    game_rule_en = """\
Let's play a "Tree Root Discovery" game. Here are the rules:

The game involves a connected undirected tree with 11 nodes, numbered from 1 to 11. The edges are:
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

I have secretly chosen a root node r from the candidate set {root_candidates}, which remains fixed throughout the game.

Definition: Layer k consists of all nodes whose graph distance from root r is k-1 (where k is a positive integer greater than or equal to 1). For example, layer 1 is the root node itself (distance 0), and layer 2 contains all nodes at distance 1 from the root.

Your goals are:
1. Infer which node is the hidden root r
2. Identify all nodes in layer 4 (i.e., all nodes at distance 3 from the root) and list them in ascending order

You can ask me two types of queries, and I will answer truthfully based on the true configuration:

1. Count Query: Ask "How many nodes are in layer k?" (where k is an integer from 1 to 11). I will answer with an integer (0 if no nodes exist in that layer).
2. Membership Query: Ask "Is node x in layer k?" (where x is a node number from 1 to 11, and k is an integer from 1 to 11). I will answer "Yes" or "No".

Notes:
- Please use as few queries as possible
- Queries to list all nodes in a layer at once are not supported
- Compound or fuzzy conditional queries are not supported
- All feedback is strictly based on the same hidden root's layer structure

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about the number of nodes in layer 3):
<query_count>3</query_count>

- Membership Query (e.g., asking if node 5 is in layer 2):
<query_member>5,2</query_member>

When submitting the final answer, specify the root node number and all node numbers in layer 4 (comma-separated, in ascending order), using this format:

<answer>root=2, layer4=7,8,9</answer>
"""

    contextualized_rule_zh_1 = """\
我们来模拟一个"交通枢纽追溯"任务，规则如下：

我们的城市交通网包含 11 个核心交汇点（编号 1-11），它们之间的连通道路情况如下：
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

由于突发状况，控制中心秘密指定了其中一个交汇点作为临时指挥枢纽 r。该枢纽在候选集合 {root_candidates} 中，并在整个任务期间保持不变。

定义：第 k 圈层是指所有与指挥枢纽 r 的图距离为 k-1 的交汇点集合（k 为正整数，大于等于 1）。例如，第 1 圈层是指挥枢纽本身（距离为 0），第 2 圈层是与其相邻的所有直接连接点。

你的目标是：
1. 推断出隐藏的指挥枢纽 r 的编号
2. 找出第 4 圈层（即与指挥枢纽距离为 3 的所有交汇点）包含哪些交汇点，并按升序排列

你可以向我提出两类查询问题，我会根据真实路网状态如实回答：

1. 数量查询：询问"第 k 圈层有多少个交汇点？"（其中 k 为 1 到 11 之间的整数）。我会回答一个整数（若该圈层不存在交汇点则回答 0）。
2. 成员查询：询问"交汇点 x 是否在第 k 圈层？"（其中 x 为 1 到 11 之间的编号，k 为 1 到 11 之间的整数）。我会回答"是"或"否"。

注意：
- 请尽可能少地使用查询次数
- 不支持一次性列出某圈层全部交汇点的查询
- 不支持复合或模糊条件的查询
- 所有反馈严格基于同一个隐藏指挥枢纽的圈层结构

每次查询只能包含一个标签。请使用以下 XML 格式：

- 数量查询（例如询问第 3 圈层的交汇点数量）：
<query_count>3</query_count>

- 成员查询（例如询问交汇点 5 是否在第 2 圈层）：
<query_member>5,2</query_member>

提交最终答案时，必须说明指挥枢纽编号和第 4 圈层的所有交汇点编号（用逗号隔开，按升序排列），格式如下：

<answer>root=2, layer4=7,8,9</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's simulate a "Traffic Hub Tracing" task. Here are the rules:

Our city's traffic network consists of 11 core intersections (numbered 1 to 11) with the following road connections:
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

Due to an unexpected event, the control center has secretly designated one of the intersections as the temporary command hub r. This hub is chosen from the candidate set {root_candidates} and remains fixed throughout the task.

Definition: Layer k consists of all intersections whose graph distance from the command hub r is k-1 (where k is a positive integer greater than or equal to 1). For example, layer 1 is the command hub itself (distance 0), and layer 2 contains all intersections directly connected to the hub.

Your goals are:
1. Infer which intersection is the hidden command hub r
2. Identify all intersections in layer 4 (i.e., all intersections at distance 3 from the hub) and list them in ascending order

You can ask me two types of queries, and I will answer truthfully based on the actual network status:

1. Count Query: Ask "How many intersections are in layer k?" (where k is an integer from 1 to 11). I will answer with an integer (0 if no intersections exist in that layer).
2. Membership Query: Ask "Is intersection x in layer k?" (where x is a number from 1 to 11, and k is an integer from 1 to 11). I will answer "Yes" or "No".

Notes:
- Please use as few queries as possible
- Queries to list all intersections in a layer at once are not supported
- Compound or fuzzy conditional queries are not supported
- All feedback is strictly based on the same hidden command hub's layer structure

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about the number of intersections in layer 3):
<query_count>3</query_count>

- Membership Query (e.g., asking if intersection 5 is in layer 2):
<query_member>5,2</query_member>

When submitting the final answer, specify the command hub number and all intersection numbers in layer 4 (comma-separated, in ascending order), using this format:

<answer>root=2, layer4=7,8,9</answer>
"""

    contextualized_rule_zh_2 = """\
我们来执行一项"流行病源头追踪"任务，规则如下：

疾控中心监测到一个包含 11 名感染者的传播链网络（感染者编号为 1 到 11），已知的密切接触轨迹连边如下：
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

我已秘密锁定了一名"零号病人" r，该感染源在候选集合 {root_candidates} 中，且在整个追踪过程中保持不变。

定义：第 k 感染层是指所有与"零号病人" r 传播图距离为 k-1 的感染者集合（k 为正整数，大于等于 1）。例如，第 1 层就是零号病人本人（距离为 0），第 2 层是被其直接感染的一代病例。

你的目标是：
1. 推断出隐藏的"零号病人" r 是哪一位
2. 找出第 4 感染层（即与零号病人传播距离为 3 的所有病例）包含哪些感染者，并按升序排列

你可以向我提出两类查询问题，我会根据真实的流调数据如实回答：

1. 数量查询：询问"第 k 层有多少名感染者？"（其中 k 为 1 到 11 之间的整数）。我会回答一个整数（若该层不存在感染者则回答 0）。
2. 成员查询：询问"感染者 x 是否在第 k 层？"（其中 x 为 1 到 11 之间的编号，k 为 1 到 11 之间的整数）。我会回答"是"或"否"。

注意：
- 请尽可能少地使用查询次数
- 不支持一次性列出某层全部感染者的查询
- 不支持复合或模糊条件的查询
- 所有反馈严格基于同一个隐藏零号病人的传播结构

每次查询只能包含一个标签。请使用以下 XML 格式：

- 数量查询（例如询问第 3 层的感染者数量）：
<query_count>3</query_count>

- 成员查询（例如询问感染者 5 是否在第 2 层）：
<query_member>5,2</query_member>

提交最终答案时，必须说明零号病人编号和第 4 层的所有感染者编号（用逗号隔开，按升序排列），格式如下：

<answer>root=2, layer4=7,8,9</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's conduct an "Epidemic Source Tracing" task. Here are the rules:

The CDC has monitored a transmission network involving 11 infected individuals (numbered 1 to 11). The known close contact tracing edges are:
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

I have secretly locked onto a "Patient Zero" r, who is in the candidate set {root_candidates} and remains fixed throughout the tracing process.

Definition: Infection layer k consists of all individuals whose transmission graph distance from Patient Zero r is k-1 (where k is a positive integer greater than or equal to 1). For example, layer 1 is Patient Zero themselves (distance 0), and layer 2 contains all first-generation cases directly infected by them.

Your goals are:
1. Infer which individual is the hidden Patient Zero r
2. Identify all cases in infection layer 4 (i.e., all individuals at a transmission distance of 3 from Patient Zero) and list them in ascending order

You can ask me two types of queries, and I will answer truthfully based on the actual epidemiological data:

1. Count Query: Ask "How many infected individuals are in layer k?" (where k is an integer from 1 to 11). I will answer with an integer (0 if no individuals exist in that layer).
2. Membership Query: Ask "Is individual x in layer k?" (where x is a number from 1 to 11, and k is an integer from 1 to 11). I will answer "Yes" or "No".

Notes:
- Please use as few queries as possible
- Queries to list all individuals in a layer at once are not supported
- Compound or fuzzy conditional queries are not supported
- All feedback is strictly based on the same hidden Patient Zero's transmission structure

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about the number of cases in layer 3):
<query_count>3</query_count>

- Membership Query (e.g., asking if individual 5 is in layer 2):
<query_member>5,2</query_member>

When submitting the final answer, specify Patient Zero's number and all individual numbers in layer 4 (comma-separated, in ascending order), using this format:

<answer>root=2, layer4=7,8,9</answer>
"""

    contextualized_rule_zh_3 = """\
我们来模拟一次"校园应急通知溯源"演练，规则如下：

教育局设定了一个包含 11 个教职员工的紧急联络树（员工编号为 1 到 11），已知的联络汇报线路如下：
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

演练中，我已秘密指定了一名员工 r 作为通知的发起人（信源），该发起人在候选集合 {root_candidates} 中，且在整个演练期间保持不变。

定义：第 k 触达层是指所有与通知发起人 r 的信息传递距离为 k-1 的教职员工集合（k 为正整数，大于等于 1）。例如，第 1 层就是发起人自身（距离为 0），第 2 层是直接接到发起人电话的员工。

你的目标是：
1. 推断出隐藏的通知发起人 r 是哪一位
2. 找出第 4 触达层（即与发起人传递距离为 3 的所有员工）包含哪些人员，并按升序排列

你可以向我提出两类查询问题，我会根据真实的联络记录如实回答：

1. 数量查询：询问"第 k 层有多少名员工？"（其中 k 为 1 到 11 之间的整数）。我会回答一个整数（若该层不存在员工则回答 0）。
2. 成员查询：询问"员工 x 是否在第 k 层？"（其中 x 为 1 到 11 之间的编号，k 为 1 到 11 之间的整数）。我会回答"是"或"否"。

注意：
- 请尽可能少地使用查询次数
- 不支持一次性列出某层全部员工的查询
- 不支持复合或模糊条件的查询
- 所有反馈严格基于同一个隐藏发起人的联络树结构

每次查询只能包含一个标签。请使用以下 XML 格式：

- 数量查询（例如询问第 3 层的员工数量）：
<query_count>3</query_count>

- 成员查询（例如询问员工 5 是否在第 2 层）：
<query_member>5,2</query_member>

提交最终答案时，必须说明通知发起人的编号和第 4 层的所有员工编号（用逗号隔开，按升序排列），格式如下：

<answer>root=2, layer4=7,8,9</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's simulate a "Campus Emergency Notification Tracing" drill. Here are the rules:

The education board has set up an emergency contact tree consisting of 11 faculty members (numbered 1 to 11). The known reporting lines are:
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

For the drill, I have secretly designated one member r as the notification initiator (information source). This initiator is in the candidate set {root_candidates} and remains fixed throughout the drill.

Definition: Reach layer k consists of all faculty members whose information transfer distance from the initiator r is k-1 (where k is a positive integer greater than or equal to 1). For example, layer 1 is the initiator themselves (distance 0), and layer 2 contains members who directly received a call from the initiator.

Your goals are:
1. Infer which member is the hidden notification initiator r
2. Identify all members in reach layer 4 (i.e., all members at a transfer distance of 3 from the initiator) and list them in ascending order

You can ask me two types of queries, and I will answer truthfully based on the actual contact records:

1. Count Query: Ask "How many members are in layer k?" (where k is an integer from 1 to 11). I will answer with an integer (0 if no members exist in that layer).
2. Membership Query: Ask "Is member x in layer k?" (where x is a number from 1 to 11, and k is an integer from 1 to 11). I will answer "Yes" or "No".

Notes:
- Please use as few queries as possible
- Queries to list all members in a layer at once are not supported
- Compound or fuzzy conditional queries are not supported
- All feedback is strictly based on the same hidden initiator's contact tree structure

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about the number of members in layer 3):
<query_count>3</query_count>

- Membership Query (e.g., asking if member 5 is in layer 2):
<query_member>5,2</query_member>

When submitting the final answer, specify the initiator's number and all member numbers in layer 4 (comma-separated, in ascending order), using this format:

<answer>root=2, layer4=7,8,9</answer>
"""

    contextualized_rule_zh_4 = """\
我们来开展一项"供应链核心溯源"业务，规则如下：

我们的工业制造网络包含 11 个生产工厂（编号 1 到 11），它们之间的上下游供应链关联如下：
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

系统已秘密配置了其中一个工厂作为核心原料供应商 r。该核心供应商在候选集合 {root_candidates} 中，并在整个排查期间保持不变。

定义：第 k 供应层级是指所有与核心供应商 r 的供应链图距离为 k-1 的工厂集合（k 为正整数，大于等于 1）。例如，第 1 层级就是核心供应商本身（距离为 0），第 2 层级是直接接收其原料的一级加工厂。

你的目标是：
1. 推断出隐藏的核心供应商 r 是哪一个工厂
2. 找出第 4 供应层级（即与核心供应商距离为 3 的所有工厂）包含哪些工厂，并按升序排列

你可以向我提出两类查询问题，我会根据真实的供应链数据如实回答：

1. 数量查询：询问"第 k 层级有多少个工厂？"（其中 k 为 1 到 11 之间的整数）。我会回答一个整数（若该层级不存在工厂则回答 0）。
2. 成员查询：询问"工厂 x 是否在第 k 层级？"（其中 x 为 1 到 11 之间的编号，k 为 1 到 11 之间的整数）。我会回答"是"或"否"。

注意：
- 请尽可能少地使用查询次数
- 不支持一次性列出某层级全部工厂的查询
- 不支持复合或模糊条件的查询
- 所有反馈严格基于同一个隐藏核心供应商的供应链结构

每次查询只能包含一个标签。请使用以下 XML 格式：

- 数量查询（例如询问第 3 层级的工厂数量）：
<query_count>3</query_count>

- 成员查询（例如询问工厂 5 是否在第 2 层级）：
<query_member>5,2</query_member>

提交最终答案时，必须说明核心供应商编号和第 4 层级的所有工厂编号（用逗号隔开，按升序排列），格式如下：

<answer>root=2, layer4=7,8,9</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's conduct a "Supply Chain Core Tracing" operation. Here are the rules:

Our industrial manufacturing network consists of 11 production facilities (numbered 1 to 11) with the following upstream and downstream connections:
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

The system has secretly configured one of the facilities as the core raw material supplier r. This core supplier is in the candidate set {root_candidates} and remains fixed throughout the tracing period.

Definition: Supply tier k consists of all facilities whose supply chain graph distance from the core supplier r is k-1 (where k is a positive integer greater than or equal to 1). For example, tier 1 is the core supplier itself (distance 0), and tier 2 contains the primary processing facilities that directly receive its materials.

Your goals are:
1. Infer which facility is the hidden core supplier r
2. Identify all facilities in supply tier 4 (i.e., all facilities at a distance of 3 from the core supplier) and list them in ascending order

You can ask me two types of queries, and I will answer truthfully based on the actual supply chain data:

1. Count Query: Ask "How many facilities are in tier k?" (where k is an integer from 1 to 11). I will answer with an integer (0 if no facilities exist in that tier).
2. Membership Query: Ask "Is facility x in tier k?" (where x is a number from 1 to 11, and k is an integer from 1 to 11). I will answer "Yes" or "No".

Notes:
- Please use as few queries as possible
- Queries to list all facilities in a tier at once are not supported
- Compound or fuzzy conditional queries are not supported
- All feedback is strictly based on the same hidden core supplier's tier structure

Each query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about the number of facilities in tier 3):
<query_count>3</query_count>

- Membership Query (e.g., asking if facility 5 is in tier 2):
<query_member>5,2</query_member>

When submitting the final answer, specify the core supplier's number and all facility numbers in tier 4 (comma-separated, in ascending order), using this format:

<answer>root=2, layer4=7,8,9</answer>
"""

    contextualized_rule_zh_5 = """\
我们来执行一项"洗钱资金追踪"反欺诈调查，规则如下：

经侦部门冻结了一个包含 11 个涉案银行账户的资金流转网络（账户编号为 1 到 11），已查明的资金转账链路如下：
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

专案组已秘密锁定了其中一个账户作为洗钱的源头主犯账户 r。该源头账户在候选集合 {root_candidates} 中，并在整个侦查过程中保持不变。

定义：第 k 洗钱层级是指所有与源头主犯账户 r 资金流转图距离为 k-1 的账户集合（k 为正整数，大于等于 1）。例如，第 1 层级就是源头账户自身（距离为 0），第 2 层级是直接接收其赃款的过桥账户。

你的目标是：
1. 推断出隐藏的源头主犯账户 r 是哪一个
2. 找出第 4 洗钱层级（即与源头账户流转距离为 3 的所有账户）包含哪些账户，并按升序排列

你可以向我提出两类调查查询，我会根据真实的资金流水数据如实回答：

1. 数量查询：询问"第 k 层级有多少个账户？"（其中 k 为 1 到 11 之间的整数）。我会回答一个整数（若该层级不存在账户则回答 0）。
2. 成员查询：询问"账户 x 是否在第 k 层级？"（其中 x 为 1 到 11 之间的编号，k 为 1 到 11 之间的整数）。我会回答"是"或"否"。

注意：
- 请尽可能少地申请查询权限
- 不支持一次性调取某层级全部账户的查询
- 不支持复合或模糊条件的查询
- 所有反馈严格基于同一个隐藏源头账户的流转结构

每次调查查询只能包含一个标签。请使用以下 XML 格式：

- 数量查询（例如询问第 3 层级的账户数量）：
<query_count>3</query_count>

- 成员查询（例如询问账户 5 是否在第 2 层级）：
<query_member>5,2</query_member>

提交最终调查报告时，必须说明源头主犯账户编号和第 4 层级的所有账户编号（用逗号隔开，按升序排列），格式如下：

<answer>root=2, layer4=7,8,9</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's execute an "Illicit Fund Tracking" anti-fraud investigation. Here are the rules:

The economic crime department has frozen a fund transfer network involving 11 implicated bank accounts (numbered 1 to 11). The identified transfer links are:
- 1-2, 1-3, 2-4, 2-5, 3-6, 6-7, 6-8, 4-9, 5-10, 5-11

The task force has secretly locked onto one of the accounts as the mastermind's source account r for money laundering. This source account is in the candidate set {root_candidates} and remains fixed throughout the investigation.

Definition: Money laundering tier k consists of all accounts whose fund transfer graph distance from the mastermind's source account r is k-1 (where k is a positive integer greater than or equal to 1). For example, tier 1 is the source account itself (distance 0), and tier 2 contains the bridge accounts directly receiving the illicit funds.

Your goals are:
1. Infer which account is the hidden mastermind's source account r
2. Identify all accounts in laundering tier 4 (i.e., all accounts at a transfer distance of 3 from the source account) and list them in ascending order

You can ask me two types of investigative queries, and I will answer truthfully based on the actual financial ledger data:

1. Count Query: Ask "How many accounts are in tier k?" (where k is an integer from 1 to 11). I will answer with an integer (0 if no accounts exist in that tier).
2. Membership Query: Ask "Is account x in tier k?" (where x is a number from 1 to 11, and k is an integer from 1 to 11). I will answer "Yes" or "No".

Notes:
- Please use query permissions as sparingly as possible
- Queries to list all accounts in a tier at once are not supported
- Compound or fuzzy conditional queries are not supported
- All feedback is strictly based on the same hidden source account's transfer structure

Each investigative query must contain only one tag. Use the following XML format:

- Count Query (e.g., asking about the number of accounts in tier 3):
<query_count>3</query_count>

- Membership Query (e.g., asking if account 5 is in tier 2):
<query_member>5,2</query_member>

When submitting the final investigation report, specify the mastermind's source account number and all account numbers in tier 4 (comma-separated, in ascending order), using this format:

<answer>root=2, layer4=7,8,9</answer>
"""

    tags = ["answer", "query_count", "query_member"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "root": 1,
                "root_candidates": "1,2,3,4",
            },
            2: {
                "root": 2,
                "root_candidates": "1,2,5,6",
            },
            3: {
                "root": 5,
                "root_candidates": "1,2,5,6",
            },
            4: {
                "root": 6,
                "root_candidates": "1,2,5,6",
            },
            5: {
                "root": 6,
                "root_candidates": "2,3,5,6",
            },
        },
        "en": {
            1: {
                "root": 1,
                "root_candidates": "1,2,3,4",
            },
            2: {
                "root": 2,
                "root_candidates": "1,2,5,6",
            },
            3: {
                "root": 5,
                "root_candidates": "1,2,5,6",
            },
            4: {
                "root": 6,
                "root_candidates": "1,2,5,6",
            },
            5: {
                "root": 6,
                "root_candidates": "2,3,5,6",
            },
        },
    }

    def __init__(self, config):
        self.edges = [
            (1, 2), (1, 3), (2, 4), (2, 5), (3, 6),
            (6, 7), (6, 8), (4, 9), (5, 10), (5, 11)
        ]
        self.adj = {i: [] for i in range(1, 12)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.root = cfg["root"]
        self._game_info["root_candidates"] = cfg["root_candidates"]
        
        self.distances = self._bfs_distances(self.root)
        
        self.layers = {}
        for node, dist in self.distances.items():
            layer = dist + 1
            if layer not in self.layers:
                self.layers[layer] = []
            self.layers[layer].append(node)
        
        for layer in self.layers:
            self.layers[layer].sort()
        
        self.layer4_nodes = sorted(self.layers.get(4, []))

    def _bfs_distances(self, root):
        from collections import deque
        
        distances = {root: 0}
        queue = deque([root])
        
        while queue:
            node = queue.popleft()
            for neighbor in self.adj[node]:
                if neighbor not in distances:
                    distances[neighbor] = distances[node] + 1
                    queue.append(neighbor)
        
        return distances

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        i = 0
        while i < len(kv_pairs):
            pair = kv_pairs[i]
            if "=" in pair:
                k, v = pair.split("=", 1)
                key = k.strip()
                if key == "layer4":
                    values = [v.strip()]
                    i += 1
                    while i < len(kv_pairs) and "=" not in kv_pairs[i]:
                        values.append(kv_pairs[i].strip())
                        i += 1
                    ans_dict[key] = ",".join(values)
                else:
                    ans_dict[key] = v.strip()
                    i += 1
            else:
                i += 1
        
        if "root" not in ans_dict or "layer4" not in ans_dict:
            return False
        
        try:
            predicted_root = int(ans_dict["root"])
        except:
            return False
        
        if predicted_root != self.root:
            return False
        
        try:
            predicted_layer4 = sorted([int(x.strip()) for x in ans_dict["layer4"].split(",") if x.strip()])
        except:
            return False
        
        return predicted_layer4 == self.layer4_nodes

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效。"
            error_range = "错误：参数超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format."
            error_range = "Error: Parameter out of range."

        if "query_count" in parsed_info:
            try:
                k = int(parsed_info["query_count"].strip())
                if k < 1 or k > 11:
                    return error_range
                count = len(self.layers.get(k, []))
                return str(count)
            except:
                return error_format

        elif "query_member" in parsed_info:
            try:
                raw = parsed_info["query_member"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                x = int(parts[0])
                k = int(parts[1])
                
                if x < 1 or x > 11 or k < 1 or k > 11:
                    return error_range
                
                is_in_layer = x in self.layers.get(k, [])
                return yes_res if is_in_layer else no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for k in range(1, 12):
            count = len(self.layers.get(k, []))
            queries.append({
                "query": f"<query_count>{k}</query_count>",
                "answer": str(count)
            })

        for x in range(1, 12):
            for k in range(1, 12):
                is_in_layer = x in self.layers.get(k, [])
                ans = yes_res if is_in_layer else no_res
                queries.append({
                    "query": f"<query_member>{x},{k}</query_member>",
                    "answer": ans
                })

        return queries

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        if correct.lower() == "yes":
            return "No"
        if correct.lower() == "no":
            return "Yes"
        
        return correct + "_WRONG"