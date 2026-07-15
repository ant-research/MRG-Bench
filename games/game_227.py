from .base import Game
import random

class HiddenRootGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏根推理"游戏，规则如下：

游戏设定了一棵无向树，包含 {n} 个节点（编号从 1 到 {n}）。树的结构如下：

{tree_structure}

我已秘密选择了其中一个节点作为"根"。当树以这个隐藏根为根时，会形成一棵有根树，从而在所有节点之间定义了祖先关系。

定义：对于两个不同的节点 x 和 y，如果 x 位于从根到 y 的唯一路径上（且 x 不等于 y），则称 x 是 y 的祖先。

你的目标是通过尽可能少的查询推断出隐藏的根节点，并能正确判断任意节点对的祖先关系。

1. **祖先判定查询**：询问节点 x 是否是节点 y 的祖先（x 和 y 必须不同）。我会回答"是"或"否"。

2. **根猜测**：当你认为已经找到答案时，提交你猜测的根节点编号。

3. **评测阶段**：一旦你的根猜测正确，系统会给出 {m} 个新的节点对，你需要依次判断每对中第一个节点是否是第二个节点的祖先。

每次只能提交一个操作。请使用以下 XML 格式：

- 祖先判定查询（例如询问节点 2 是否是节点 5 的祖先）：
<query_ancestor>2,5</query_ancestor>

- 根猜测（例如猜测节点 3 是根）：
<answer>3</answer>

- 评测阶段判定（例如判断节点 1 是节点 4 的祖先）：
<eval_answer>是</eval_answer>

或

<eval_answer>否</eval_answer>

注意：请尽可能减少查询次数，高效地推断出隐藏的根。
"""

    game_rule_en = """\
Let's play a "Hidden Root Deduction" game. Here are the rules:

The game is set on an undirected tree with {n} nodes (numbered from 1 to {n}). The tree structure is as follows:

{tree_structure}

I have secretly selected one node as the "root". When the tree is rooted at this hidden root, it becomes a rooted tree, defining ancestor relationships among all nodes.

Definition: For two distinct nodes x and y, x is an ancestor of y if and only if x lies on the unique path from the root to y (and x is not equal to y).

Your goal is to infer the hidden root node through as few queries as possible, and be able to correctly determine the ancestor relationship for any pair of nodes.

1. **Ancestor Query**: Ask whether node x is an ancestor of node y (x and y must be different). I will answer "Yes" or "No".

2. **Root Guess**: When you think you have found the answer, submit your guessed root node number.

3. **Evaluation Phase**: Once your root guess is correct, the system will provide {m} new node pairs, and you need to determine in sequence whether the first node is an ancestor of the second node in each pair.

Only one operation can be submitted at a time. Use the following XML format:

- Ancestor Query (e.g., asking if node 2 is an ancestor of node 5):
<query_ancestor>2,5</query_ancestor>

- Root Guess (e.g., guessing node 3 is the root):
<answer>3</answer>

- Evaluation Phase Answer (e.g., determining node 1 is an ancestor of node 4):
<eval_answer>Yes</eval_answer>

or

<eval_answer>No</eval_answer>

Note: Please minimize the number of queries and efficiently infer the hidden root.
"""

    contextualized_rule_zh_1 = """\
欢迎使用"物流溯源分析系统"，规则如下：

系统监测到一个包含 {n} 个物流枢纽（编号从 1 到 {n}）的无向连通运输网络。网络道路结构如下：

{tree_structure}

我们已知其中一个枢纽是隐藏的全国核心调度中心。当物资从该核心中心发往全国各地时，整个网络会形成一棵有向的流向树，并严格确立了各枢纽间的上下游关系。

定义：对于两个不同的枢纽 x 和 y，如果枢纽 x 位于从核心调度中心到枢纽 y 的唯一运输路线上（且 x 不等于 y），则称枢纽 x 是枢纽 y 的"上游枢纽"。

你的目标是通过尽可能少的查询，精确定位出隐藏的核心调度中心，并能正确梳理任意枢纽对的上下游关系。

1. **上游关系查询**：询问枢纽 x 是否是枢纽 y 的上游枢纽（x 和 y 必须不同）。我会回答"是"或"否"。

2. **核心猜测**：当你认为已经明确目标时，提交你推断的核心调度中心枢纽编号。

3. **评测阶段**：一旦你成功锁定核心枢纽，系统会给出 {m} 个新的枢纽对，你需要依次判断每对中第一个枢纽是否是第二个枢纽的上游枢纽。

每次只能提交一个操作。请使用以下 XML 格式：

- 上游关系查询（例如询问枢纽 2 是否是枢纽 5 的上游枢纽）：
<query_ancestor>2,5</query_ancestor>

- 核心猜测（例如猜测枢纽 3 是核心调度中心）：
<answer>3</answer>

- 评测阶段判定（例如判断枢纽 1 是枢纽 4 的上游枢纽）：
<eval_answer>是</eval_answer>

或

<eval_answer>否</eval_answer>

注意：请尽可能减少查询次数，高效地推断出隐藏的调度源头。
"""

    contextualized_rule_en_1 = """\
[Traffic/Transportation Scenario]
Welcome to the "Logistics Source Analysis System". Here are the rules:

The system monitors an undirected connected transportation network consisting of {n} logistics hubs (numbered from 1 to {n}). The road network structure is as follows:

{tree_structure}

We know that one of the hubs is secretly functioning as the national core dispatch center. When materials are dispatched from this core center to regions nationwide, the entire network forms a directed flow tree, strictly establishing upstream and downstream relationships among the hubs.

Definition: For two distinct hubs x and y, hub x is an "upstream hub" of hub y if and only if hub x lies on the unique transportation path from the core dispatch center to hub y (and x is not equal to y).

Your objective is to accurately pinpoint the hidden core dispatch center using as few queries as possible, and correctly determine the upstream-downstream relationship for any pair of hubs.

1. **Upstream Query**: Ask whether hub x is an upstream hub of hub y (x and y must be different). I will answer "Yes" or "No".

2. **Core Guess**: When you believe you have found the answer, submit the hub number of the guessed core dispatch center.

3. **Evaluation Phase**: Once you successfully lock onto the core hub, the system will provide {m} new hub pairs. You must sequentially determine whether the first hub is an upstream hub of the second in each pair.

Only one operation can be submitted at a time. Please use the following XML format:

- Upstream Query (e.g., asking if hub 2 is an upstream hub of hub 5):
<query_ancestor>2,5</query_ancestor>

- Core Guess (e.g., guessing hub 3 is the core dispatch center):
<answer>3</answer>

- Evaluation Phase Answer (e.g., determining hub 1 is an upstream hub of hub 4):
<eval_answer>Yes</eval_answer>

or

<eval_answer>No</eval_answer>

Note: Please minimize the number of queries and efficiently infer the hidden dispatch source.
"""

    contextualized_rule_zh_2 = """\
欢迎使用"流行病传染链溯源系统"，规则如下：

系统已建立了一个包含 {n} 个密切接触者（编号从 1 到 {n}）的传染连通网络。接触网络结构如下：

{tree_structure}

我们已知其中一个病例是隐藏的"零号病人"（首发病例）。当病毒从零号病人开始传播时，整个网络形成了一棵有向的传播树，从而在所有感染者之间确立了明确的传染源上下游关系。

定义：对于两个不同的病例 x 和 y，如果病例 x 位于从零号病人到病例 y 的唯一传播链条上（且 x 不等于 y），则称病例 x 是病例 y 的"上游传染源"。

你的目标是通过尽可能少的查询，排查出隐藏的零号病人，并能正确验证任意病例对的传染路径关系。

1. **传染源查询**：询问病例 x 是否是病例 y 的上游传染源（x 和 y 必须不同）。我会回答"是"或"否"。

2. **零号病人锁定**：当你认为已经追踪到源头时，提交你猜测的零号病人编号。

3. **评测阶段**：一旦你成功锁定零号病人，系统会给出 {m} 个新的病例对，你需要依次判断每对中第一个病例是否是第二个病例的上游传染源。

每次只能提交一个操作。请使用以下 XML 格式：

- 传染源查询（例如询问病例 2 是否是病例 5 的上游传染源）：
<query_ancestor>2,5</query_ancestor>

- 零号病人锁定（例如猜测病例 3 是零号病人）：
<answer>3</answer>

- 评测阶段判定（例如判断病例 1 是病例 4 的上游传染源）：
<eval_answer>是</eval_answer>

或

<eval_answer>否</eval_answer>

注意：请尽可能减少排查次数，高效地推断出隐藏的感染源头。
"""

    contextualized_rule_en_2 = """\
[Medical/Healthcare Scenario]
Welcome to the "Epidemiological Tracing System". Here are the rules:

The system has established an infectious contact network containing {n} close contacts (numbered from 1 to {n}). The contact network structure is as follows:

{tree_structure}

We know that one of these cases is the hidden "Patient Zero" (the index case). As the virus spreads from Patient Zero, the entire network forms a directed transmission tree, thereby establishing clear upstream and downstream transmission source relationships among all infected individuals.

Definition: For two distinct cases x and y, case x is an "upstream infectious source" of case y if and only if case x lies on the unique transmission chain from Patient Zero to case y (and x is not equal to y).

Your objective is to trace and locate the hidden Patient Zero through as few queries as possible, and correctly verify the transmission path relationship for any pair of cases.

1. **Source Query**: Ask whether case x is an upstream infectious source of case y (x and y must be different). I will answer "Yes" or "No".

2. **Patient Zero Lock**: When you believe you have tracked down the source, submit the case number of the suspected Patient Zero.

3. **Evaluation Phase**: Once you successfully lock onto Patient Zero, the system will provide {m} new case pairs. You must sequentially determine whether the first case is an upstream infectious source of the second in each pair.

Only one operation can be submitted at a time. Please use the following XML format:

- Source Query (e.g., asking if case 2 is an upstream infectious source of case 5):
<query_ancestor>2,5</query_ancestor>

- Patient Zero Lock (e.g., guessing case 3 is Patient Zero):
<answer>3</answer>

- Evaluation Phase Answer (e.g., determining case 1 is an upstream infectious source of case 4):
<eval_answer>Yes</eval_answer>

or

<eval_answer>No</eval_answer>

Note: Please minimize the number of queries and efficiently infer the hidden infection source.
"""

    contextualized_rule_zh_3 = """\
欢迎使用"知识图谱前置依赖分析系统"，规则如下：

系统分析得到了一个包含 {n} 个知识节点（编号从 1 到 {n}）的无向关联图谱。图谱的关联结构如下：

{tree_structure}

根据学科逻辑，其中存在一个隐藏的核心"元概念"（基础公理）。当基于这个元概念推演整个图谱时，所有的知识节点会延展成一棵有向的知识树，形成了严密的前置学习依赖关系。

定义：对于两个不同的知识节点 x 和 y，如果节点 x 位于从元概念到节点 y 的唯一认知推演路径上（且 x 不等于 y），则称节点 x 是节点 y 的"前置基础知识"。

你的目标是通过尽可能少的查询，分析出隐藏的核心元概念，并能正确判定任意知识节点之间的前置依赖关系。

1. **前置知识查询**：询问节点 x 是否是节点 y 的前置基础知识（x 和 y 必须不同）。我会回答"是"或"否"。

2. **元概念推断**：当你认为已经找到答案时，提交你推断的元概念节点编号。

3. **评测阶段**：一旦你成功推断出元概念，系统会给出 {m} 个新的知识节点对，你需要依次判断每对中第一个节点是否是第二个节点的前置基础知识。

每次只能提交一个操作。请使用以下 XML 格式：

- 前置知识查询（例如询问节点 2 是否是节点 5 的前置基础知识）：
<query_ancestor>2,5</query_ancestor>

- 元概念推断（例如推断节点 3 是元概念）：
<answer>3</answer>

- 评测阶段判定（例如判断节点 1 是节点 4 的前置基础知识）：
<eval_answer>是</eval_answer>

或

<eval_answer>否</eval_answer>

注意：请尽可能减少查询次数，高效地定位出学科的隐藏基础。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Prerequisite Analysis System". Here are the rules:

The system has mapped out an undirected relational graph containing {n} knowledge nodes (numbered from 1 to {n}). The structure of the relations is as follows:

{tree_structure}

Based on disciplinary logic, there exists a hidden core "meta-concept" (foundational axiom). When the entire graph is deduced from this meta-concept, all knowledge nodes expand into a directed knowledge tree, forming strict prerequisite learning dependencies.

Definition: For two distinct knowledge nodes x and y, node x is a "prerequisite knowledge" of node y if and only if node x lies on the unique cognitive deduction path from the meta-concept to node y (and x is not equal to y).

Your objective is to identify the hidden core meta-concept with as few queries as possible, and correctly determine the prerequisite dependency relationship for any pair of knowledge nodes.

1. **Prerequisite Query**: Ask whether node x is a prerequisite knowledge of node y (x and y must be different). I will answer "Yes" or "No".

2. **Meta-concept Deduction**: When you think you have found the answer, submit the node number of the deduced meta-concept.

3. **Evaluation Phase**: Once you successfully deduce the meta-concept, the system will provide {m} new node pairs. You must sequentially determine whether the first node is a prerequisite knowledge of the second in each pair.

Only one operation can be submitted at a time. Please use the following XML format:

- Prerequisite Query (e.g., asking if node 2 is a prerequisite of node 5):
<query_ancestor>2,5</query_ancestor>

- Meta-concept Deduction (e.g., guessing node 3 is the meta-concept):
<answer>3</answer>

- Evaluation Phase Answer (e.g., determining node 1 is a prerequisite of node 4):
<eval_answer>Yes</eval_answer>

or

<eval_answer>No</eval_answer>

Note: Please minimize the number of queries and efficiently locate the hidden foundation of the subject.
"""

    contextualized_rule_zh_4 = """\
欢迎使用"工业流水线追踪控制系统"，规则如下：

工厂车间包含了一个由 {n} 个加工工序（编号从 1 到 {n}）组成的连通生产装配网络。工序的物理连接结构如下：

{tree_structure}

在这些工序中，有一个是隐藏的源头"初加工台"。当原料从该初加工台进入生产线流转时，整个装配网络会形成一棵有向的流水线作业树，严格确立了工序间的先后流转关系。

定义：对于两个不同的加工工序 x 和 y，如果工序 x 位于从初加工台到工序 y 的唯一工艺流程线上（且 x 不等于 y），则称工序 x 是工序 y 的"上游前置工序"。

你的目标是通过尽可能少的探查，定位出隐藏的源头初加工台，并能正确理清任意加工工序间的上下游依赖关系。

1. **前置工序查询**：询问工序 x 是否是工序 y 的上游前置工序（x 和 y 必须不同）。我会回答"是"或"否"。

2. **源头定位**：当你认为已经追踪到起点时，提交你定位的初加工台编号。

3. **评测阶段**：一旦你锁定初加工台，系统会给出 {m} 个新的工序对，你需要依次判断每对中第一个工序是否是第二个工序的上游前置工序。

每次只能提交一个操作。请使用以下 XML 格式：

- 前置工序查询（例如询问工序 2 是否是工序 5 的上游前置工序）：
<query_ancestor>2,5</query_ancestor>

- 源头定位（例如确认工序 3 为初加工台）：
<answer>3</answer>

- 评测阶段判定（例如判断工序 1 是工序 4 的上游前置工序）：
<eval_answer>是</eval_answer>

或

<eval_answer>否</eval_answer>

注意：请尽可能减少探查指令，高效地找出工业生产的隐藏起点。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Industrial Assembly Line Tracking System". Here are the rules:

The factory floor contains a connected production assembly network composed of {n} processing operations (numbered from 1 to {n}). The physical connection structure of the operations is as follows:

{tree_structure}

Among these operations, one is the secretly designated "initial processing station" (the source). When raw materials enter the production line from this initial processing station, the entire assembly network forms a directed assembly line tree, strictly establishing the sequential flow relationships among the operations.

Definition: For two distinct processing operations x and y, operation x is an "upstream preceding process" of operation y if and only if operation x lies on the unique workflow line from the initial processing station to operation y (and x is not equal to y).

Your objective is to locate the hidden initial processing station through as few probes as possible, and correctly clarify the upstream and downstream dependency relationships for any pair of operations.

1. **Preceding Process Query**: Ask whether operation x is an upstream preceding process of operation y (x and y must be different). I will answer "Yes" or "No".

2. **Source Location**: When you believe you have tracked down the starting point, submit the operation number of the located initial processing station.

3. **Evaluation Phase**: Once you successfully locate the initial processing station, the system will provide {m} new operation pairs. You must sequentially determine whether the first operation is an upstream preceding process of the second in each pair.

Only one operation can be submitted at a time. Please use the following XML format:

- Preceding Process Query (e.g., asking if operation 2 is an upstream process of operation 5):
<query_ancestor>2,5</query_ancestor>

- Source Location (e.g., confirming operation 3 is the initial processing station):
<answer>3</answer>

- Evaluation Phase Answer (e.g., determining operation 1 is an upstream process of operation 4):
<eval_answer>Yes</eval_answer>

or

<eval_answer>No</eval_answer>

Note: Please minimize the number of probe commands and efficiently uncover the hidden starting point of the industrial production.
"""

    contextualized_rule_zh_5 = """\
欢迎使用"涉案资金洗钱流向侦查系统"，规则如下：

经融侦查部门截获了一个包含 {n} 个银行账户（编号从 1 到 {n}）的无向资金往来网络。网络的转账关系结构如下：

{tree_structure}

调查表明，其中一个账户是隐藏的核心"资金源头账户"。当非法资金从该源头账户开始分散洗白时，整个网络构成了一棵有向的资金流向树，清晰反映了各账户间的资金上下游清洗关系。

定义：对于两个不同的银行账户 x 和 y，如果账户 x 位于从资金源头账户流向账户 y 的唯一转账路径上（且 x 不等于 y），则称账户 x 是账户 y 的"上游转账账户"。

你的侦查目标是通过尽可能少的问询查询，揪出隐藏的资金源头账户，并能准确指认任意账户对之间的资金流向先后关系。

1. **上游流向查询**：询问账户 x 是否是账户 y 的上游转账账户（x 和 y 必须不同）。我会回答"是"或"否"。

2. **源头抓捕锁定**：当你确信已查明真相时，提交你锁定的资金源头账户编号。

3. **评测阶段**：一旦你锁定源头账户正确，系统会提供 {m} 个新的涉案账户对，你需要依次判断每对中第一个账户是否是第二个账户的上游转账账户。

每次只能提交一个操作。请使用以下 XML 格式：

- 上游流向查询（例如询问账户 2 是否是账户 5 的上游账户）：
<query_ancestor>2,5</query_ancestor>

- 源头抓捕锁定（例如锁定账户 3 为资金源头）：
<answer>3</answer>

- 评测阶段判定（例如判断账户 1 是账户 4 的上游账户）：
<eval_answer>是</eval_answer>

或

<eval_answer>否</eval_answer>

注意：请尽可能减少查询次数，高效地破获这起隐藏的洗钱源头网络。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Illicit Funds Flow Investigation System". Here are the rules:

The financial investigation department has intercepted an undirected fund transaction network comprising {n} bank accounts (numbered from 1 to {n}). The structure of the transfer relations is as follows:

{tree_structure}

Investigations indicate that one of the accounts is the hidden core "source fund account". As illicit funds begin to be dispersed and laundered from this source account, the entire network forms a directed fund flow tree, clearly reflecting the upstream and downstream laundering relationships among the accounts.

Definition: For two distinct bank accounts x and y, account x is an "upstream transfer account" of account y if and only if account x lies on the unique transfer path from the source fund account to account y (and x is not equal to y).

Your investigative objective is to root out the hidden source fund account with as few inquiries as possible, and accurately identify the chronological fund flow relationship for any pair of accounts.

1. **Upstream Flow Query**: Ask whether account x is an upstream transfer account of account y (x and y must be different). I will answer "Yes" or "No".

2. **Source Lock**: When you are confident you have uncovered the truth, submit the account number of the locked source fund account.

3. **Evaluation Phase**: Once you correctly lock the source account, the system will provide {m} new suspected account pairs. You must sequentially determine whether the first account is an upstream transfer account of the second in each pair.

Only one operation can be submitted at a time. Please use the following XML format:

- Upstream Flow Query (e.g., asking if account 2 is an upstream account of account 5):
<query_ancestor>2,5</query_ancestor>

- Source Lock (e.g., locking account 3 as the fund source):
<answer>3</answer>

- Evaluation Phase Answer (e.g., determining account 1 is an upstream account of account 4):
<eval_answer>Yes</eval_answer>

or

<eval_answer>No</eval_answer>

Note: Please minimize the number of queries and efficiently dismantle the hidden source of this money laundering network.
"""

    tags = ["answer", "query_ancestor", "eval_answer"]

    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "root": 3,
                "eval_pairs": [(2, 4), (4, 2), (1, 5)],
                "m": 3,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "root": 1,
                "eval_pairs": [(1, 4), (2, 3), (4, 5), (6, 7)],
                "m": 4,
            },
            3: {
                "n": 9,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9)],
                "root": 2,
                "eval_pairs": [(2, 7), (1, 8), (4, 5), (3, 9), (7, 8)],
                "m": 5,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (8, 12)],
                "root": 3,
                "eval_pairs": [(3, 8), (1, 10), (2, 6), (4, 9), (7, 12), (10, 11)],
                "m": 6,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (10, 15)],
                "root": 4,
                "eval_pairs": [(4, 13), (2, 11), (1, 15), (8, 9), (3, 10), (6, 12), (13, 14)],
                "m": 7,
            },
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "root": 3,
                "eval_pairs": [(2, 4), (4, 2), (1, 5)],
                "m": 3,
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "root": 1,
                "eval_pairs": [(1, 4), (2, 3), (4, 5), (6, 7)],
                "m": 4,
            },
            3: {
                "n": 9,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (5, 8), (6, 9)],
                "root": 2,
                "eval_pairs": [(2, 7), (1, 8), (4, 5), (3, 9), (7, 8)],
                "m": 5,
            },
            4: {
                "n": 12,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (8, 12)],
                "root": 3,
                "eval_pairs": [(3, 8), (1, 10), (2, 6), (4, 9), (7, 12), (10, 11)],
                "m": 6,
            },
            5: {
                "n": 15,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (10, 15)],
                "root": 4,
                "eval_pairs": [(4, 13), (2, 11), (1, 15), (8, 9), (3, 10), (6, 12), (13, 14)],
                "m": 7,
            },
        },
    }

    def __init__(self, config):
        self.in_eval_phase = False
        self.eval_index = 0
        self.eval_correct_count = 0
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
        self._game_info["m"] = cfg["m"]
        
        self.n = cfg["n"]
        self.edges = cfg["edges"]
        self.hidden_root = cfg["root"]
        self.eval_pairs = cfg["eval_pairs"]
        
        self.adj = [[] for _ in range(self.n + 1)]
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        edges_str = ", ".join([f"({u},{v})" for u, v in self.edges])
        if lang == "zh":
            self._game_info["tree_structure"] = f"边集合：{edges_str}"
        else:
            self._game_info["tree_structure"] = f"Edge set: {edges_str}"
        
        self._compute_ancestor_relations()

    def _compute_ancestor_relations(self):
        self.parent = {}
        self.depth = {}
        visited = set()
        queue = [self.hidden_root]
        visited.add(self.hidden_root)
        self.parent[self.hidden_root] = None
        self.depth[self.hidden_root] = 0
        
        while queue:
            u = queue.pop(0)
            for v in self.adj[u]:
                if v not in visited:
                    visited.add(v)
                    self.parent[v] = u
                    self.depth[v] = self.depth[u] + 1
                    queue.append(v)

    def _is_ancestor(self, x, y):
        if x == y:
            return False
        current = y
        while current is not None:
            if current == x:
                return True
            current = self.parent.get(current)
        return False

    def evaluate(self, parsed_info):
        try:
            guessed_root = int(parsed_info["answer"].strip())
            if guessed_root < 1 or guessed_root > self.n:
                return False
            return guessed_root == self.hidden_root
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            correct_res, incorrect_res = "对", "错"
            error_format = "错误：格式无效或节点编号错误。"
            error_same = "错误：两个节点必须不同。"
            error_eval_complete = "评测阶段已完成。"
        else:
            yes_res, no_res = "Yes", "No"
            correct_res, incorrect_res = "Correct", "Incorrect"
            error_format = "Error: Invalid format or node number."
            error_same = "Error: The two nodes must be different."
            error_eval_complete = "Evaluation phase completed."

        if "query_ancestor" in parsed_info:
            if self.in_eval_phase:
                return "Error: Cannot query during evaluation phase." if self.config.language == "en" else "错误：评测阶段不能进行查询。"
            
            try:
                raw = parsed_info["query_ancestor"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                x, y = int(parts[0]), int(parts[1])
                if x < 1 or x > self.n or y < 1 or y > self.n:
                    return error_format
                if x == y:
                    return error_same
                
                return yes_res if self._is_ancestor(x, y) else no_res
            except:
                return error_format

        elif "eval_answer" in parsed_info:
            if not self.in_eval_phase:
                return "Error: Not in evaluation phase." if self.config.language == "en" else "错误：尚未进入评测阶段。"
            
            if self.eval_index >= len(self.eval_pairs):
                return error_eval_complete
            
            user_answer = parsed_info["eval_answer"].strip()
            x, y = self.eval_pairs[self.eval_index]
            correct_answer = self._is_ancestor(x, y)
            
            if self.config.language == "zh":
                is_correct = (user_answer == "是" and correct_answer) or (user_answer == "否" and not correct_answer)
            else:
                is_correct = (user_answer == "Yes" and correct_answer) or (user_answer == "No" and not correct_answer)
            
            self.eval_index += 1
            
            if is_correct:
                self.eval_correct_count += 1
                if self.eval_index >= len(self.eval_pairs):
                    self.state.set_state("success", "all evaluations correct")
                    return correct_res
                else:
                    next_x, next_y = self.eval_pairs[self.eval_index]
                    if self.config.language == "zh":
                        return f"{correct_res}。请判断：节点 {next_x} 是否是节点 {next_y} 的祖先？"
                    else:
                        return f"{correct_res}. Please determine: Is node {next_x} an ancestor of node {next_y}?"
            else:
                self.state.set_state("failed", "incorrect evaluation")
                return incorrect_res
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是": return "否"
            if correct == "否": return "是"
        else:
            if correct.lower() == "yes":
                return "No" if correct[0].isupper() else "no"
            if correct.lower() == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for x in range(1, self.n + 1):
            for y in range(1, self.n + 1):
                if x == y:
                    continue
                
                query_content = f"{x},{y}"
                
                is_anc = self._is_ancestor(x, y)
                answer = yes_res if is_anc else no_res
                
                queries.append({
                    "query": query_content,
                    "answer": answer
                })
        
        return queries

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            
            if "answer" in parsed_info and not self.in_eval_phase:
                is_correct = self.evaluate(parsed_info)
                if is_correct:
                    self.in_eval_phase = True
                    self.eval_index = 0
                    self.eval_correct_count = 0
                    
                    x, y = self.eval_pairs[0]
                    if self.config.language == "zh":
                        res = f"根猜测正确！现在进入评测阶段。请判断：节点 {x} 是否是节点 {y} 的祖先？"
                    else:
                        res = f"Root guess correct! Now entering evaluation phase. Please determine: Is node {x} an ancestor of node {y}?"
                    self.state.add_message("user", res)
                else:
                    res = "根猜测错误。" if self.config.language == "zh" else "Root guess incorrect."
                    self.state.set_state("failed", "incorrect root guess")
                    self.state.add_message("user", res)
            
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state