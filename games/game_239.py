from .base import Game
import random

class TreeModularPredicateGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树上模运算推理"游戏，规则如下：

游戏给定了一棵有根树，包含 {n} 个节点（编号从 1 到 {n}），根节点为编号 {root}。树的结构和每个节点的权值如下：

树的边（父节点 -> 子节点）：
{edges}

节点权值：
{weights}

我已经秘密选定了两个参数 M 和 R，其中 M 是一个 2 到 9 之间的整数，R 是一个 0 到 M-1 之间的整数。

对于树中的任意节点 u，定义"子树和" S(u) 为以 u 为根的子树中所有节点权值的总和（包括 u 自身）。

定义谓词 P(u)：当且仅当 S(u) 除以 M 的余数等于 R 时，P(u) 为真。

你的目标是通过有限次查询推断出参数 M 和 R，并给出所有满足 P(u) 为真的节点集合。

你可以向我查询任意节点 u，询问该节点是否满足 P(u) 为真（即 S(u) 除以 M 的余数是否等于 R）。我会如实回答"是"或"否"。

请尽可能用少的查询次数完成推理。当你确定答案后，请提交最终结果。

查询某个节点（例如查询节点 3）：
<query>{{node_id}}</query>

提交最终答案时，需要说明参数 M 和 R，以及所有满足条件的节点列表（用逗号隔开，顺序不限）：
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

例如：
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    game_rule_en = """\
Let's play a "Tree Modular Predicate Inference" game. Here are the rules:

You are given a rooted tree with {n} nodes (numbered from 1 to {n}), where the root is node {root}. The tree structure and node weights are as follows:

Tree edges (parent -> child):
{edges}

Node weights:
{weights}

I have secretly chosen two parameters M and R, where M is an integer between 2 and 9, and R is an integer between 0 and M-1.

For any node u in the tree, define the "subtree sum" S(u) as the sum of all node weights in the subtree rooted at u (including u itself).

Define predicate P(u): P(u) is true if and only if S(u) modulo M equals R.

Your goal is to infer the parameters M and R through a limited number of queries, and identify all nodes where P(u) is true.

You can query any node u to ask whether P(u) is true (i.e., whether S(u) modulo M equals R). I will answer truthfully with "Yes" or "No".

Please complete the inference with as few queries as possible. When you are confident, submit your final answer.

To query a node (e.g., query node 3):
<query>{{node_id}}</query>

When submitting the final answer, specify parameters M and R, and list all nodes satisfying the condition (comma-separated, order does not matter):
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

For example:
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市绿波交通网推断”系统。

系统中有一棵包含 {n} 个路口（节点编号从 1 到 {n}）的树状交通汇聚网络，根节点为总控制中心（编号 {root}）。网络拓扑和每个路口的独立车流量基数如下：

路网连接（上游路口 -> 下游路口）：
{edges}

各路口独立车流量基数：
{weights}

系统底层设定了两个信号灯协同周期的控制参数 M 和 R，其中 M 为周期模数（2到9之间的整数），R 为相位偏移量（0到M-1之间的整数）。

对于网络中的任意路口 u，我们定义“汇聚车流量” S(u) 为以 u 为根节点的汇聚子网中所有路口（包含 u 自身）的独立车流量基数之和。

定义特征判定 P(u)：当且仅当汇聚车流量 S(u) 除以 M 的余数等于 R 时，该路口 u 满足相位匹配，被系统自动标记为“绿波协调节点”。

你的目标是通过有限次查询，推断出控制参数 M 和 R，并找出所有被标记为“绿波协调节点”的路口。

你可以向我查询任意路口 u，询问其是否为“绿波协调节点”（即 S(u) 除以 M 的余数是否等于 R）。我会如实反馈“是”或“否”。

请以最少的查询次数完成推断。当你确定答案后，请提交最终结果。

查询某个路口（例如查询路口 3）：
<query>{{node_id}}</query>

提交最终答案时，需要说明参数 M 和 R，以及所有满足条件的路口列表（用逗号隔开，顺序不限）：
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

例如：
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Green Wave Traffic Inference" system.

The system manages a tree-structured traffic convergence network containing {n} intersections (numbered 1 to {n}), with the root node being the main control center (node {root}). The network topology and the independent base traffic volume for each intersection are as follows:

Network Connections (Upstream -> Downstream):
{edges}

Independent Base Traffic Volume:
{weights}

The system uses two hidden signal coordination parameters, M and R. M is the cycle modulus (an integer between 2 and 9), and R is the phase offset (an integer between 0 and M-1).

For any intersection u in the network, define the "convergent traffic volume" S(u) as the sum of the independent base traffic volumes of all intersections in the sub-network rooted at u (including u itself).

Define the characteristic condition P(u): P(u) is true if and only if the convergent traffic volume S(u) modulo M equals R. In this case, intersection u matches the phase and is marked as a "Green Wave Coordinated Node".

Your goal is to infer the parameters M and R through a limited number of queries, and identify all intersections marked as "Green Wave Coordinated Nodes".

You can query any intersection u to ask whether it is a "Green Wave Coordinated Node" (i.e., whether S(u) modulo M equals R). I will answer truthfully with "Yes" or "No".

Please complete the inference with as few queries as possible. Submit your final answer when you are confident.

To query an intersection (e.g., query intersection 3):
<query>{{node_id}}</query>

When submitting the final answer, specify parameters M and R, and list all nodes satisfying the condition (comma-separated, order does not matter):
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

For example:
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“传染病接触者追踪溯源”系统。

系统中有一棵包含 {n} 名受测人员（编号从 1 到 {n}）的树状传播网络，根节点为零号病人（编号 {root}）。传播路径和每个人的独立病毒载量指标如下：

传播路径（传染源 -> 被传染者）：
{edges}

各人员独立病毒载量：
{weights}

疾控中心正在研究该病毒亚型的两个基因特征参数 M 和 R，其中 M 为序列切分长度（2到9之间的整数），R 为特异性标记位（0到M-1之间的整数）。

对于网络中的任意人员 u，我们定义“累计变异载量” S(u) 为以 u 为传染源的下游分支中所有人员（包含 u 自身）的独立病毒载量之和。

定义特征判定 P(u)：当且仅当累计变异载量 S(u) 除以 M 的余数等于 R 时，该人员及其传播链触发特异性表达，被系统判定为“高风险变异聚集簇”。

你的目标是通过有限次查询，推断出特征参数 M 和 R，并找出所有被判定为“高风险变异聚集簇”的重点人员。

你可以向我查询任意人员 u，询问其是否属于“高风险变异聚集簇”（即 S(u) 除以 M 的余数是否等于 R）。我会如实反馈“是”或“否”。

请以最少的查询次数完成溯源推断。当你确定答案后，请提交最终结果。

查询某个人员（例如查询人员 3）：
<query>{{node_id}}</query>

提交最终答案时，需要说明参数 M 和 R，以及所有满足条件的人员列表（用逗号隔开，顺序不限）：
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

例如：
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Infectious Disease Contact Tracing and Sourcing" system.

The system tracks a tree-structured transmission network containing {n} tested individuals (numbered 1 to {n}), where the root node is patient zero (node {root}). The transmission pathways and the independent viral load for each individual are as follows:

Transmission Pathways (Infector -> Infectee):
{edges}

Independent Viral Load:
{weights}

The CDC is investigating two genetic characteristic parameters of this viral subtype, M and R. M is the sequence segmentation length (an integer between 2 and 9), and R is the specific marker locus (an integer between 0 and M-1).

For any individual u in the network, define the "cumulative mutational load" S(u) as the sum of the independent viral loads of all individuals in the transmission branch originating from u (including u itself).

Define the characteristic condition P(u): P(u) is true if and only if the cumulative mutational load S(u) modulo M equals R. When this occurs, the individual and their transmission chain trigger specific expression and are classified as a "High-Risk Mutation Cluster".

Your goal is to infer the characteristic parameters M and R through a limited number of queries, and identify all individuals classified as "High-Risk Mutation Clusters".

You can query any individual u to ask whether they belong to a "High-Risk Mutation Cluster" (i.e., whether S(u) modulo M equals R). I will answer truthfully with "Yes" or "No".

Please complete the inference with as few queries as possible. Submit your final answer when you are confident.

To query an individual (e.g., query person 3):
<query>{{node_id}}</query>

When submitting the final answer, specify parameters M and R, and list all nodes satisfying the condition (comma-separated, order does not matter):
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

For example:
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“在线课程学分转排与分析”系统。

系统中有一棵包含 {n} 个知识模块（编号从 1 到 {n}）的树状依赖结构，根节点为顶层综合项目（编号 {root}）。前置依赖关系和每个知识模块的独立学时如下：

依赖关系（高级模块 -> 基础模块）：
{edges}

各模块独立学时：
{weights}

教务系统在分配学分时隐藏了两个排课参数 M 和 R，其中 M 为每周课时上限模数（2到9之间的整数），R 为剩余自学课时要求（0到M-1之间的整数）。

对于结构中的任意知识模块 u，我们定义“总前置学时” S(u) 为以 u 为根节点的知识依赖树中所有前置模块（包含 u 自身）的独立学时之和。

定义特征判定 P(u)：当且仅当总前置学时 S(u) 除以 M 的余数等于 R 时，该模块触发排课阈值，被教务系统标记为“排课边缘模块”。

你的目标是通过有限次查询，推断出排课参数 M 和 R，并找出所有被标记为“排课边缘模块”的知识模块。

你可以向我查询任意知识模块 u，询问其是否为“排课边缘模块”（即 S(u) 除以 M 的余数是否等于 R）。我会如实反馈“是”或“否”。

请以最少的查询次数完成推断。当你确定答案后，请提交最终结果。

查询某个模块（例如查询模块 3）：
<query>{{node_id}}</query>

提交最终答案时，需要说明参数 M 和 R，以及所有满足条件的模块列表（用逗号隔开，顺序不限）：
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

例如：
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Online Course Credit Transfer and Scheduling Analysis" system.

The system manages a tree-structured dependency mapping containing {n} knowledge modules (numbered 1 to {n}), where the root node is the capstone project (node {root}). The prerequisite relationships and independent study hours for each module are as follows:

Dependency Relationships (Advanced Module -> Foundation Module):
{edges}

Independent Study Hours:
{weights}

The academic affairs system uses two hidden scheduling parameters for credit allocation, M and R. M is the weekly instruction limit modulus (an integer between 2 and 9), and R is the remaining self-study hours requirement (an integer between 0 and M-1).

For any knowledge module u in the structure, define the "total prerequisite hours" S(u) as the sum of the independent study hours of all prerequisite modules in the dependency tree rooted at u (including u itself).

Define the characteristic condition P(u): P(u) is true if and only if the total prerequisite hours S(u) modulo M equals R. In this case, the module hits the scheduling threshold and is marked by the system as a "Fringe Scheduling Module".

Your goal is to infer the scheduling parameters M and R through a limited number of queries, and identify all knowledge modules marked as "Fringe Scheduling Modules".

You can query any knowledge module u to ask whether it is a "Fringe Scheduling Module" (i.e., whether S(u) modulo M equals R). I will answer truthfully with "Yes" or "No".

Please complete the inference with as few queries as possible. Submit your final answer when you are confident.

To query a module (e.g., query module 3):
<query>{{node_id}}</query>

When submitting the final answer, specify parameters M and R, and list all nodes satisfying the condition (comma-separated, order does not matter):
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

For example:
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎进入“智能制造 BOM 质检分拣”系统。

系统中有一棵包含 {n} 个组件或零件（编号从 1 到 {n}）的树状装配结构（物料清单 BOM），根节点为最终成品（编号 {root}）。装配包含关系和每个零件的自身物理重量如下：

装配关系（父组件 -> 子组件/零件）：
{edges}

各零件自身重量：
{weights}

自动化质检传输带使用了两个承重分拣参数 M 和 R，其中 M 为传输带承重模数（2到9之间的整数），R 为特定轨道的配重余数要求（0到M-1之间的整数）。

对于装配树中的任意组件 u，我们定义“总成重量” S(u) 为装配组件 u 所需的所有下级子组件及零件（包含 u 的自身框架结构）的重量之和。

定义特征判定 P(u)：当且仅当总成重量 S(u) 除以 M 的余数等于 R 时，该组件符合特殊配重要求，将被自动化产线分配至“A号特种质检轨道”。

你的目标是通过有限次查询，推断出分拣参数 M 和 R，并找出所有被分配至“A号特种质检轨道”的组件。

你可以向我查询任意组件 u，询问其是否进入了“A号特种质检轨道”（即 S(u) 除以 M 的余数是否等于 R）。我会如实反馈“是”或“否”。

请以最少的查询次数完成产线参数推断。当你确定答案后，请提交最终结果。

查询某个组件（例如查询组件 3）：
<query>{{node_id}}</query>

提交最终答案时，需要说明参数 M 和 R，以及所有满足条件的组件列表（用逗号隔开，顺序不限）：
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

例如：
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Smart Manufacturing BOM Quality Inspection and Sorting" system.

The system tracks a tree-structured assembly structure (Bill of Materials, BOM) containing {n} components or parts (numbered 1 to {n}), where the root node is the final product (node {root}). The assembly containment relationships and the individual physical weight of each part are as follows:

Assembly Relationships (Parent Component -> Subcomponent/Part):
{edges}

Individual Part Weights:
{weights}

The automated inspection conveyor belt uses two weight sorting parameters, M and R. M is the conveyor load modulus (an integer between 2 and 9), and R is the residual counterweight requirement for a specific track (an integer between 0 and M-1).

For any component u in the assembly tree, define the "total assembly weight" S(u) as the sum of the weights of all required subcomponents and parts for component u (including the framework of u itself).

Define the characteristic condition P(u): P(u) is true if and only if the total assembly weight S(u) modulo M equals R. In this case, the component meets the special counterweight requirement and is routed by the automated line to the "Special Inspection Track A".

Your goal is to infer the sorting parameters M and R through a limited number of queries, and identify all components routed to "Special Inspection Track A".

You can query any component u to ask whether it has entered "Special Inspection Track A" (i.e., whether S(u) modulo M equals R). I will answer truthfully with "Yes" or "No".

Please complete the inference with as few queries as possible. Submit your final answer when you are confident.

To query a component (e.g., query component 3):
<query>{{node_id}}</query>

When submitting the final answer, specify parameters M and R, and list all nodes satisfying the condition (comma-separated, order does not matter):
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

For example:
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“企业资金往来与股权穿透审计”系统。

系统中有一棵包含 {n} 个涉案账户（编号从 1 到 {n}）的树状资金流向网络，根节点为核心控股账户（编号 {root}）。资金控制流向和每个账户的单笔隐匿资金额如下：

资金控制流向（上级账户 -> 下级账户）：
{edges}

各账户单笔隐匿资金额：
{weights}

反洗钱核查算法预设了两个特征参数 M 和 R，其中 M 为分片流转模数（2到9之间的整数），R 为洗钱沉淀特征值（0到M-1之间的整数）。

对于资金网中的任意账户 u，我们定义“穿透归集资金总额” S(u) 为以 u 为顶点的资金归集链路中所有关联下级账户（包含 u 自身）的隐匿资金额之和。

定义特征判定 P(u)：当且仅当穿透归集资金总额 S(u) 除以 M 的余数等于 R 时，该账户的资金沉淀行为触发算法阈值，被系统标记为“异常审计警报”。

你的目标是通过有限次查询，推断出核查参数 M 和 R，并找出所有触发了“异常审计警报”的重点账户。

你可以向我查询任意账户 u，询问其是否触发了“异常审计警报”（即 S(u) 除以 M 的余数是否等于 R）。我会如实反馈“是”或“否”。

请以最少的查询次数完成资金流推断。当你确定答案后，请提交最终结果。

查询某个账户（例如查询账户 3）：
<query>{{node_id}}</query>

提交最终答案时，需要说明参数 M 和 R，以及所有满足条件的账户列表（用逗号隔开，顺序不限）：
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

例如：
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Corporate Funds Flow and Equity Penetration Audit" system.

The system handles a tree-structured fund flow network containing {n} involved accounts (numbered 1 to {n}), where the root node is the core holding account (node {root}). The fund control flows and the individual concealed transaction amount for each account are as follows:

Fund Control Flows (Parent Account -> Subsidiary Account):
{edges}

Individual Concealed Transaction Amounts:
{weights}

The anti-money laundering verification algorithm is preset with two characteristic parameters, M and R. M is the fragmented transfer modulus (an integer between 2 and 9), and R is the laundering settlement characteristic value (an integer between 0 and M-1).

For any account u in the funds network, define the "penetrating consolidated fund total" S(u) as the sum of the concealed transaction amounts of all associated subsidiary accounts in the fund consolidation chain rooted at u (including account u itself).

Define the characteristic condition P(u): P(u) is true if and only if the penetrating consolidated fund total S(u) modulo M equals R. In this case, the account's fund settlement behavior hits the algorithm threshold and is flagged with an "Abnormal Audit Alert".

Your goal is to infer the verification parameters M and R through a limited number of queries, and identify all key accounts that triggered the "Abnormal Audit Alert".

You can query any account u to ask whether it triggered an "Abnormal Audit Alert" (i.e., whether S(u) modulo M equals R). I will answer truthfully with "Yes" or "No".

Please complete the inference with as few queries as possible. Submit your final answer when you are confident.

To query an account (e.g., query account 3):
<query>{{node_id}}</query>

When submitting the final answer, specify parameters M and R, and list all nodes satisfying the condition (comma-separated, order does not matter):
<answer>M={{M_value}}, R={{R_value}}, nodes={{node_list}}</answer>

For example:
<answer>M=3, R=1, nodes=2,5,7</answer>
"""

    tags = ["answer", "query"]
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "root": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5)],
                "weights": {1: 5, 2: 3, 3: 7, 4: 2, 5: 4},
                "M": 3,
                "R": 2,
            },
            2: {
                "n": 7,
                "root": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "weights": {1: 8, 2: 5, 3: 6, 4: 3, 5: 2, 6: 4, 7: 1},
                "M": 4,
                "R": 1,
            },
            3: {
                "n": 10,
                "root": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "weights": {1: 10, 2: 7, 3: 8, 4: 4, 5: 6, 6: 5, 7: 2, 8: 3, 9: 1, 10: 9},
                "M": 5,
                "R": 3,
            },
            4: {
                "n": 12,
                "root": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (7, 12)],
                "weights": {1: 12, 2: 8, 3: 9, 4: 5, 5: 7, 6: 6, 7: 4, 8: 3, 9: 2, 10: 8, 11: 1, 12: 6},
                "M": 6,
                "R": 4,
            },
            5: {
                "n": 15,
                "root": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10), (6, 11), (7, 12), (7, 13), (8, 14), (9, 15)],
                "weights": {1: 15, 2: 10, 3: 11, 4: 7, 5: 8, 6: 6, 7: 9, 8: 4, 9: 5, 10: 3, 11: 7, 12: 2, 13: 6, 14: 1, 15: 4},
                "M": 7,
                "R": 5,
            },
        },
        "en": {
            1: {
                "n": 5,
                "root": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5)],
                "weights": {1: 5, 2: 3, 3: 7, 4: 2, 5: 4},
                "M": 3,
                "R": 2,
            },
            2: {
                "n": 7,
                "root": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "weights": {1: 8, 2: 5, 3: 6, 4: 3, 5: 2, 6: 4, 7: 1},
                "M": 4,
                "R": 1,
            },
            3: {
                "n": 10,
                "root": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (4, 7), (4, 8), (5, 9), (6, 10)],
                "weights": {1: 10, 2: 7, 3: 8, 4: 4, 5: 6, 6: 5, 7: 2, 8: 3, 9: 1, 10: 9},
                "M": 5,
                "R": 3,
            },
            4: {
                "n": 12,
                "root": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10), (7, 11), (7, 12)],
                "weights": {1: 12, 2: 8, 3: 9, 4: 5, 5: 7, 6: 6, 7: 4, 8: 3, 9: 2, 10: 8, 11: 1, 12: 6},
                "M": 6,
                "R": 4,
            },
            5: {
                "n": 15,
                "root": 1,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10), (6, 11), (7, 12), (7, 13), (8, 14), (9, 15)],
                "weights": {1: 15, 2: 10, 3: 11, 4: 7, 5: 8, 6: 6, 7: 9, 8: 4, 9: 5, 10: 3, 11: 7, 12: 2, 13: 6, 14: 1, 15: 4},
                "M": 7,
                "R": 5,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self.n = cfg["n"]
        self.root = cfg["root"]
        self.edges = cfg["edges"]
        self.weights = cfg["weights"]
        self.M = cfg["M"]
        self.R = cfg["R"]
        
        self.children = {i: [] for i in range(1, self.n + 1)}
        for parent, child in self.edges:
            self.children[parent].append(child)
        
        self.subtree_sum = {}
        self._compute_subtree_sum(self.root)
        
        self.satisfying_nodes = set()
        for node in range(1, self.n + 1):
            if self.subtree_sum[node] % self.M == self.R:
                self.satisfying_nodes.add(node)
        
        edges_str = ", ".join([f"{p}->{c}" for p, c in self.edges])
        weights_str = ", ".join([f"节点{k}: {v}" if lang == "zh" else f"Node {k}: {v}" 
                                 for k, v in sorted(self.weights.items())])
        
        self._game_info["n"] = self.n
        self._game_info["root"] = self.root
        self._game_info["edges"] = edges_str
        self._game_info["weights"] = weights_str

    def _compute_subtree_sum(self, node):
        total = self.weights[node]
        for child in self.children[node]:
            total += self._compute_subtree_sum(child)
        self.subtree_sum[node] = total
        return total

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        i = 0
        while i < len(kv_pairs):
            pair = kv_pairs[i]
            if "=" in pair:
                k, v = pair.split("=", 1)
                k = k.strip()
                v = v.strip()
                
                if k == "nodes":
                    nodes_list = [v]
                    i += 1
                    while i < len(kv_pairs) and "=" not in kv_pairs[i]:
                        nodes_list.append(kv_pairs[i].strip())
                        i += 1
                    ans_dict[k] = ",".join(nodes_list)
                    continue
                else:
                    ans_dict[k] = v
            i += 1
        
        if "M" not in ans_dict or "R" not in ans_dict or "nodes" not in ans_dict:
            return False
        
        try:
            submitted_M = int(ans_dict["M"])
            submitted_R = int(ans_dict["R"])
        except ValueError:
            return False
        
        if submitted_M != self.M or submitted_R != self.R:
            return False
        
        try:
            submitted_nodes = set()
            node_str = ans_dict["nodes"].strip()
            if node_str:
                for n in node_str.split(","):
                    n = n.strip()
                    if n:
                        submitted_nodes.add(int(n))
        except ValueError:
            return False
        
        return submitted_nodes == self.satisfying_nodes

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效。"
            error_range = "错误：节点编号超出范围。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format."
            error_range = "Error: Node ID out of range."
        
        if "query" in parsed_info:
            try:
                node_id = int(parsed_info["query"].strip())
            except ValueError:
                return error_format
            
            if node_id < 1 or node_id > self.n:
                return error_range
            
            if self.subtree_sum[node_id] % self.M == self.R:
                return yes_res
            else:
                return no_res
        else:
            raise ValueError("No valid query tag found.")
            
    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        for node_id in range(1, self.n + 1):
            if self.subtree_sum[node_id] % self.M == self.R:
                ans = yes_res
            else:
                ans = no_res
            
            results.append({
                "query": f"<query>{node_id}</query>",
                "answer": ans
            })
            
        return results

    def _cf_make_wrong(self, correct: str) -> str:
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