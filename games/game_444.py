# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   条件边计数：权重满足某条件的边共有多少条
# ============================================================

from .base import Game
import random


class ConditionalEdgeCountingGame(Game):

    game_rule_zh = """\
我们来玩一个"图上条件边计数"的推理游戏，规则如下：

游戏设定了一个无向简单图 G，包含 {num_vertices} 个顶点和 {num_edges} 条边。每条边都被秘密地标注了一个 0 到 9 之间的整数（包括 0 和 9）。

现在定义一个"条件集合" S = {opening_braces}0, 2, 5, 7{closing_braces}。如果一条边的标注值属于集合 S，我们就称这条边为"条件边"。

你的目标是：推断出整个图中条件边的总数 T。

你可以反复向我提问（每次一个问题），询问某个顶点的"条件度数"，即：与该顶点相邻的边中，有多少条是条件边？我会如实回答一个整数。

当你认为已经收集到足够信息后，请提交你推断出的条件边总数。若答案正确则游戏成功，否则失败。

## 顶点列表

本局游戏的顶点为：{vertex_list}

## 提问与提交答案的格式

每次提问时，请使用以下 XML 格式询问某个顶点的条件度数（例如询问顶点 A）：

<query>A</query>

提交最终答案时，请使用以下格式（T 为你推断的条件边总数）：

<answer>T</answer>

请尽可能少地提问，并在确信答案正确时提交。
"""

    game_rule_en = """\
Let's play a "Conditional Edge Counting on Graph" deduction game. Here are the rules:

The game is set on an undirected simple graph G with {num_vertices} vertices and {num_edges} edges. Each edge has been secretly labeled with an integer between 0 and 9 (inclusive).

A "condition set" S = {opening_braces}0, 2, 5, 7{closing_braces} is defined. An edge is called a "conditional edge" if its label belongs to set S.

Your goal is to infer T, the total number of conditional edges in the entire graph.

You can repeatedly ask questions (one per turn) about the "conditional degree" of a vertex, which is: among all edges adjacent to that vertex, how many are conditional edges? I will answer truthfully with an integer.

When you believe you have gathered enough information, submit your inferred total count of conditional edges. If correct, you win; otherwise, you fail.

## Vertex List

The vertices in this game are: {vertex_list}

## Query and Answer Format

To query the conditional degree of a vertex (e.g., vertex A), use this XML format:

<query>A</query>

To submit your final answer, use this format (where T is your inferred total count of conditional edges):

<answer>T</answer>

Try to ask as few questions as possible and submit when you are confident in your answer.
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市交通路网分析系统。
本系统接入了全市的道路拓扑网络 G，包含 {num_vertices} 个关键路口（顶点）和 {num_edges} 条连接路段（边）。每条路段的传感器均实时测算出了一个 0 到 9 之间的拥堵风险指数（包括 0 和 9）。

根据交管局最新规定，风险指数属于集合 S = {opening_braces}0, 2, 5, 7{closing_braces} 的路段将被标记为“高危路段”。

你的目标是：排查并推断出整个交通网络中“高危路段”的总数 T。

你可以反复调用系统接口（每次查询一个），输入特定路口的编号，系统将反馈该路口相连的“高危路段”数量（即条件度数）。

当你确认已充分收集情报后，请提交你推断的高危路段总数。若上报数据完全准确则排查成功，否则将面临重大交通隐患。

## 路口列表

本区域的关键路口为：{vertex_list}

## 查询与提交格式

每次调用接口时，请使用以下 XML 格式查询某个路口的涉危路段数（例如查询路口 A）：

<query>A</query>

提交最终排查报告时，请使用以下格式（T 为你推断的高危路段总数）：

<answer>T</answer>

请尽可能减少系统调用次数，并在确信排查无误后提交。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Urban Traffic Network Analysis System.
This system monitors the city's road topology network G, which includes {num_vertices} key intersections (vertices) and {num_edges} connecting road segments (edges). The sensors on each road segment have calculated a real-time congestion risk index, which is an integer between 0 and 9 (inclusive).

According to the latest regulations from the Traffic Management Bureau, road segments with a risk index belonging to the set S = {opening_braces}0, 2, 5, 7{closing_braces} are flagged as "High-Risk Segments".

Your objective is to investigate and infer T, the total number of High-Risk Segments in the entire traffic network.

You can repeatedly call the system interface (one query per turn) by entering a specific intersection's ID. The system will return the number of High-Risk Segments connected to that intersection (its conditional degree).

When you are confident that you have gathered sufficient intelligence, submit your inferred total count of High-Risk Segments. If your reported data is completely accurate, the investigation succeeds; otherwise, a major traffic hazard will occur.

## Intersection List

The key intersections in this sector are: {vertex_list}

## Query and Answer Format

To query the number of High-Risk Segments connected to an intersection (e.g., intersection A), use this XML format:

<query>A</query>

To submit your final investigation report, use this format (where T is your inferred total count of High-Risk Segments):

<answer>T</answer>

Try to minimize the number of system calls and submit only when you are absolutely certain of your report.
"""

    contextualized_rule_zh_2 = """\
欢迎使用流行病学接触史追踪系统。
本系统记录了一个封闭社区的病例接触网络 G，包含 {num_vertices} 名被观察者（顶点）和 {num_edges} 条双向接触记录（边）。每次接触都被流行病学专家评估并赋予了一个 0 到 9 之间的暴露风险指数（包括 0 和 9）。

根据疾控中心的判定标准，暴露风险指数属于集合 S = {opening_braces}0, 2, 5, 7{closing_braces} 的接触记录将被定性为“高危传播链”。

你的目标是：推断出整个观察网络中“高危传播链”的总数 T。

你可以反复向系统提问（每次一个问题），询问某位被观察者的“高危暴露度”，即：与其直接接触的记录中，有多少条属于“高危传播链”？系统会如实返回具体数量。

当你认为已经收集到足够的数据后，请提交你推断出的高危传播链总数。若答案正确则追踪成功，否则防疫失败。

## 被观察者列表

本区域的被观察者编号为：{vertex_list}

## 提问与提交答案的格式

每次提问时，请使用以下 XML 格式询问某位被观察者的高危暴露度（例如查询被观察者 A）：

<query>A</query>

提交最终答案时，请使用以下格式（T 为你推断的高危传播链总数）：

<answer>T</answer>

请尽可能少地进行查询操作，并在确信答案正确时提交报告。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Epidemiological Contact Tracing System.
This system records the contact network G of a closed community, comprising {num_vertices} observed individuals (vertices) and {num_edges} two-way contact records (edges). Each contact has been evaluated by epidemiologists and assigned an exposure risk index between 0 and 9 (inclusive).

According to CDC criteria, contact records with a risk index belonging to the set S = {opening_braces}0, 2, 5, 7{closing_braces} are classified as "High-Risk Transmission Chains".

Your objective is to infer T, the total number of High-Risk Transmission Chains in the entire observation network.

You can repeatedly query the system (one question per turn) about a specific individual's "high-risk exposure degree," which means: among all direct contact records associated with that person, how many are High-Risk Transmission Chains? The system will answer truthfully with an exact count.

When you believe you have gathered enough data, submit your inferred total count of High-Risk Transmission Chains. If correct, the tracing succeeds; otherwise, epidemic prevention fails.

## Observed Individuals List

The observed individuals in this sector are: {vertex_list}

## Query and Answer Format

To query the high-risk exposure degree of an individual (e.g., individual A), use this XML format:

<query>A</query>

To submit your final answer, use this format (where T is your inferred total count of High-Risk Transmission Chains):

<answer>T</answer>

Try to perform as few queries as possible and submit your report when you are confident in its accuracy.
"""

    contextualized_rule_zh_3 = """\
欢迎进入学科知识图谱构建与分析工具。
当前分析的学科知识网络 G 包含 {num_vertices} 个核心知识点（顶点）以及 {num_edges} 条知识点间的关联边。每条关联边都经由教学研讨会评定了一个 0 到 9 之间的认知跨度评级（包括 0 和 9）。

为了优化教学大纲，我们将认知跨度评级属于集合 S = {opening_braces}0, 2, 5, 7{closing_braces} 的关联定义为“重难点关联”。

你的教学任务是：推断出整个知识网络中包含的“重难点关联”总数 T。

你可以反复调用分析工具（每次一项），查询某个知识点的“重难点度数”，即：与该知识点直接相连的关联中，有几条被定性为“重难点关联”？工具将反馈准确的整数。

当你确认已全面掌握知识架构后，请提交你推断出的重难点关联总数。若核对无误则教研任务达成，否则大纲将存在缺陷。

## 知识点列表

本模块的核心知识点代号为：{vertex_list}

## 查询与提交格式

每次调用分析工具时，请使用以下 XML 格式查询特定知识点的重难点度数（例如查询知识点 A）：

<query>A</query>

提交最终教学大纲评估时，请使用以下格式（T 为你推断的重难点关联总数）：

<answer>T</answer>

请尽可能高效地进行查询，并在确信结论正确时提交评估。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Subject Knowledge Graph Construction and Analysis Tool.
The current subject knowledge network G contains {num_vertices} core knowledge nodes (vertices) and {num_edges} associative links between them (edges). Each associative link has been assigned a cognitive span rating between 0 and 9 (inclusive) by the pedagogical committee.

To optimize the syllabus, we define associative links with a cognitive span rating belonging to the set S = {opening_braces}0, 2, 5, 7{closing_braces} as "Critical Difficulty Links".

Your teaching objective is to infer T, the total number of Critical Difficulty Links within the entire knowledge network.

You can repeatedly consult the analysis tool (one query per turn) regarding a specific knowledge node's "critical difficulty degree," which means: among all links directly connected to that node, how many are identified as Critical Difficulty Links? The tool will return an accurate integer.

When you confirm that you have fully grasped the knowledge architecture, submit your inferred total count of Critical Difficulty Links. If verified correctly, your pedagogical task is accomplished; otherwise, the syllabus will be flawed.

## Knowledge Nodes List

The core knowledge nodes in this module are: {vertex_list}

## Query and Answer Format

To consult the tool about the critical difficulty degree of a node (e.g., node A), use this XML format:

<query>A</query>

To submit your final syllabus evaluation, use this format (where T is your inferred total count of Critical Difficulty Links):

<answer>T</answer>

Try to query as efficiently as possible and submit your evaluation only when you are certain of the conclusion.
"""

    contextualized_rule_zh_4 = """\
欢迎使用智能工厂管线监控与排查系统。
系统正监控着工厂的流体输送网络 G，该网络由 {num_vertices} 个生产设备节点（顶点）和 {num_edges} 条物理管线（边）构成。每条管线均配备了传感器，实时测算出一个 0 到 9 之间的管壁老化指数（包括 0 和 9）。

基于安全生产红线，老化指数属于集合 S = {opening_braces}0, 2, 5, 7{closing_braces} 的管线已被系统标记为“急需检修管线”。

你的维护目标是：推断出整个厂区网络中“急需检修管线”的总数 T，以便调配检修资源。

你可以反复向控制台下达指令（每次排查一个设备），查询某个设备节点的“高危连接数”，即：与该设备直接相接的管线中，有多少条是“急需检修管线”？控制台会返回精确数值。

当你认为已收集完足够的数据，请提交你推断的检修管线总数。若资源调配数量完全吻合则排查成功，否则将面临停线风险。

## 设备节点列表

本产线的关键设备节点为：{vertex_list}

## 查询与提交答案格式

每次下达指令时，请使用以下 XML 格式查询特定设备节点的高危连接数（例如查询设备 A）：

<query>A</query>

提交最终检修计划时，请使用以下格式（T 为你推断的急需检修管线总数）：

<answer>T</answer>

请尽可能少地执行查询指令，并在确信检修数量无误时进行提交。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the Smart Factory Pipeline Monitoring and Inspection System.
The system is monitoring the factory's fluid transport network G, which consists of {num_vertices} production equipment nodes (vertices) and {num_edges} physical pipelines (edges). Each pipeline is equipped with sensors that calculate a real-time wall aging index between 0 and 9 (inclusive).

Based on safety protocols, pipelines with an aging index belonging to the set S = {opening_braces}0, 2, 5, 7{closing_braces} are flagged by the system as "Urgent Maintenance Pipelines".

Your maintenance objective is to infer T, the total number of Urgent Maintenance Pipelines in the entire factory network, in order to allocate maintenance resources.

You can repeatedly issue commands to the console (one inspection per turn) to query a specific equipment node's "high-risk connection count," which means: among all pipelines directly connected to that equipment, how many are Urgent Maintenance Pipelines? The console will return a precise number.

When you believe you have collected enough data, submit your inferred total count of pipelines requiring maintenance. If the resource allocation matches perfectly, the inspection is successful; otherwise, there will be a risk of production line shutdown.

## Equipment Nodes List

The key equipment nodes in this production line are: {vertex_list}

## Query and Answer Format

To query the high-risk connection count of an equipment node (e.g., equipment A), use this XML format:

<query>A</query>

To submit your final maintenance plan, use this format (where T is your inferred total count of Urgent Maintenance Pipelines):

<answer>T</answer>

Try to execute as few query commands as possible and submit only when you are certain the maintenance count is correct.
"""

    contextualized_rule_zh_5 = """\
欢迎进入经侦案件资金链路追踪系统。
本案侦查涉及的资金往来网络 G 包含了 {num_vertices} 个涉案账户（顶点）和 {num_edges} 条大额转账记录（边）。每条转账记录都已被反洗钱模型打上了一个 0 到 9 之间的洗钱嫌疑评级（包括 0 和 9）。

根据检察机关的定性标准，嫌疑评级属于集合 S = {opening_braces}0, 2, 5, 7{closing_braces} 的转账记录被认定为“核心洗钱链路”。

你的侦查目标是：推断出整个资金网络中“核心洗钱链路”的总数 T，以确定涉案总规模。

你可以反复向系统发起协查请求（每次查询一个账户），了解某个涉案账户的“涉案连接度”，即：与该账户直接相关的转账记录中，有几条属于“核心洗钱链路”？系统将反馈确切的整数。

当你认定已摸清资金网全貌后，请提交你推断的核心洗钱链路总数。若上报数据无误则结案成功，否则会导致案件关键线索遗漏。

## 涉案账户列表

本案重点关注的账户代号为：{vertex_list}

## 协查与提交格式

每次发起协查请求时，请使用以下 XML 格式查询特定账户的涉案连接度（例如查询账户 A）：

<query>A</query>

提交最终侦查结论时，请使用以下格式（T 为你推断的核心洗钱链路总数）：

<answer>T</answer>

请尽可能减少不必要的协查请求，并在确信侦查结论绝对准确时提交。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Economic Crime Financial Linkage Tracking System.
The financial transaction network G involved in this investigation comprises {num_vertices} implicated accounts (vertices) and {num_edges} large-scale transfer records (edges). Each transfer record has been tagged by the anti-money laundering model with an AML suspicion rating between 0 and 9 (inclusive).

According to the prosecutor's classification standards, transfer records with a suspicion rating belonging to the set S = {opening_braces}0, 2, 5, 7{closing_braces} are identified as "Core Money Laundering Links".

Your investigative objective is to infer T, the total number of Core Money Laundering Links in the entire financial network, in order to determine the overall scale of the case.

You can repeatedly submit inquiry requests to the system (one account per turn) to ascertain an implicated account's "illicit connectivity degree," which means: among all transfer records directly involving that account, how many are Core Money Laundering Links? The system will return an exact integer.

When you conclude that you have mapped the full scope of the financial network, submit your inferred total count of Core Money Laundering Links. If your reported data is flawless, the case is successfully closed; otherwise, critical leads will be missed.

## Implicated Accounts List

The key accounts in this case are: {vertex_list}

## Inquiry and Answer Format

To inquire about the illicit connectivity degree of an account (e.g., account A), use this XML format:

<query>A</query>

To submit your final investigative conclusion, use this format (where T is your inferred total count of Core Money Laundering Links):

<answer>T</answer>

Try to minimize unnecessary inquiry requests and submit only when you are absolutely certain of your investigative conclusion.
"""

    tags = ["answer", "query"]
    
    reasoning_type = "演绎推理"
    data_structure = "图"

    # 难度配置说明：
    # 1 (简单)         - 小图，较少边
    # 2 (中等偏下)     - 中等规模图
    # 3 (中等偏上)     - 原题规模图
    # 4 (较难)         - 稍大规模图
    # 5 (难)           - 更大规模图

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "vertices": ["A", "B", "C", "D"],
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"),
                    ("B", "C"), ("C", "D")
                ],
                # 预设边标注（用于确定性测试）
                "edge_labels": {
                    ("A", "B"): 0, ("A", "C"): 2, ("A", "D"): 5,
                    ("B", "C"): 7, ("C", "D"): 3
                }
            },
            2: {
                "vertices": ["A", "B", "C", "D", "E", "F"],
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"),
                    ("B", "C"), ("B", "E"), ("C", "D"),
                    ("C", "F"), ("D", "E"), ("E", "F")
                ],
                "edge_labels": {
                    ("A", "B"): 1, ("A", "C"): 0, ("A", "D"): 4,
                    ("B", "C"): 2, ("B", "E"): 7, ("C", "D"): 5,
                    ("C", "F"): 8, ("D", "E"): 0, ("E", "F"): 9
                }
            },
            3: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"),
                    ("B", "C"), ("B", "E"), ("C", "D"),
                    ("C", "F"), ("D", "E"), ("D", "F"),
                    ("D", "G"), ("E", "G"), ("E", "H"),
                    ("F", "G"), ("G", "H")
                ],
                "edge_labels": {
                    ("A", "B"): 0, ("A", "C"): 1, ("A", "D"): 2,
                    ("B", "C"): 3, ("B", "E"): 5, ("C", "D"): 7,
                    ("C", "F"): 4, ("D", "E"): 0, ("D", "F"): 6,
                    ("D", "G"): 2, ("E", "G"): 8, ("E", "H"): 5,
                    ("F", "G"): 7, ("G", "H"): 9
                }
            },
            4: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"),
                    ("B", "C"), ("B", "F"), ("C", "D"), ("C", "G"),
                    ("D", "E"), ("D", "H"), ("E", "F"), ("E", "I"),
                    ("F", "G"), ("G", "H"), ("H", "I"), ("F", "I")
                ],
                "edge_labels": {
                    ("A", "B"): 2, ("A", "C"): 5, ("A", "D"): 1, ("A", "E"): 7,
                    ("B", "C"): 0, ("B", "F"): 3, ("C", "D"): 4, ("C", "G"): 2,
                    ("D", "E"): 6, ("D", "H"): 0, ("E", "F"): 8, ("E", "I"): 5,
                    ("F", "G"): 7, ("G", "H"): 9, ("H", "I"): 2, ("F", "I"): 0
                }
            },
            5: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"),
                    ("B", "C"), ("B", "F"), ("B", "G"), ("C", "D"),
                    ("C", "H"), ("D", "E"), ("D", "I"), ("E", "F"),
                    ("E", "J"), ("F", "G"), ("F", "J"), ("G", "H"),
                    ("H", "I"), ("I", "J"), ("G", "J"), ("H", "J")
                ],
                "edge_labels": {
                    ("A", "B"): 0, ("A", "C"): 2, ("A", "D"): 5, ("A", "E"): 7,
                    ("B", "C"): 1, ("B", "F"): 0, ("B", "G"): 3, ("C", "D"): 2,
                    ("C", "H"): 6, ("D", "E"): 4, ("D", "I"): 5, ("E", "F"): 8,
                    ("E", "J"): 7, ("F", "G"): 9, ("F", "J"): 0, ("G", "H"): 2,
                    ("H", "I"): 5, ("I", "J"): 1, ("G", "J"): 7, ("H", "J"): 4
                }
            }
        },
        "en": {
            1: {
                "vertices": ["A", "B", "C", "D"],
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"),
                    ("B", "C"), ("C", "D")
                ],
                "edge_labels": {
                    ("A", "B"): 0, ("A", "C"): 2, ("A", "D"): 5,
                    ("B", "C"): 7, ("C", "D"): 3
                }
            },
            2: {
                "vertices": ["A", "B", "C", "D", "E", "F"],
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"),
                    ("B", "C"), ("B", "E"), ("C", "D"),
                    ("C", "F"), ("D", "E"), ("E", "F")
                ],
                "edge_labels": {
                    ("A", "B"): 1, ("A", "C"): 0, ("A", "D"): 4,
                    ("B", "C"): 2, ("B", "E"): 7, ("C", "D"): 5,
                    ("C", "F"): 8, ("D", "E"): 0, ("E", "F"): 9
                }
            },
            3: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"),
                    ("B", "C"), ("B", "E"), ("C", "D"),
                    ("C", "F"), ("D", "E"), ("D", "F"),
                    ("D", "G"), ("E", "G"), ("E", "H"),
                    ("F", "G"), ("G", "H")
                ],
                "edge_labels": {
                    ("A", "B"): 0, ("A", "C"): 1, ("A", "D"): 2,
                    ("B", "C"): 3, ("B", "E"): 5, ("C", "D"): 7,
                    ("C", "F"): 4, ("D", "E"): 0, ("D", "F"): 6,
                    ("D", "G"): 2, ("E", "G"): 8, ("E", "H"): 5,
                    ("F", "G"): 7, ("G", "H"): 9
                }
            },
            4: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I"],
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"),
                    ("B", "C"), ("B", "F"), ("C", "D"), ("C", "G"),
                    ("D", "E"), ("D", "H"), ("E", "F"), ("E", "I"),
                    ("F", "G"), ("G", "H"), ("H", "I"), ("F", "I")
                ],
                "edge_labels": {
                    ("A", "B"): 2, ("A", "C"): 5, ("A", "D"): 1, ("A", "E"): 7,
                    ("B", "C"): 0, ("B", "F"): 3, ("C", "D"): 4, ("C", "G"): 2,
                    ("D", "E"): 6, ("D", "H"): 0, ("E", "F"): 8, ("E", "I"): 5,
                    ("F", "G"): 7, ("G", "H"): 9, ("H", "I"): 2, ("F", "I"): 0
                }
            },
            5: {
                "vertices": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "edges": [
                    ("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"),
                    ("B", "C"), ("B", "F"), ("B", "G"), ("C", "D"),
                    ("C", "H"), ("D", "E"), ("D", "I"), ("E", "F"),
                    ("E", "J"), ("F", "G"), ("F", "J"), ("G", "H"),
                    ("H", "I"), ("I", "J"), ("G", "J"), ("H", "J")
                ],
                "edge_labels": {
                    ("A", "B"): 0, ("A", "C"): 2, ("A", "D"): 5, ("A", "E"): 7,
                    ("B", "C"): 1, ("B", "F"): 0, ("B", "G"): 3, ("C", "D"): 2,
                    ("C", "H"): 6, ("D", "E"): 4, ("D", "I"): 5, ("E", "F"): 8,
                    ("E", "J"): 7, ("F", "G"): 9, ("F", "J"): 0, ("G", "H"): 2,
                    ("H", "I"): 5, ("I", "J"): 1, ("G", "J"): 7, ("H", "J"): 4
                }
            }
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：加载图结构、边标注，并计算条件边集合"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 顶点和边列表
        self.vertices = cfg["vertices"]
        self.edges = cfg["edges"]
        
        # 标准化边（保证无序对的一致性）
        self.edge_labels = {}
        for edge, label in cfg["edge_labels"].items():
            normalized_edge = tuple(sorted(edge))
            self.edge_labels[normalized_edge] = label
        
        # 条件集合 S = {0, 2, 5, 7}
        self.condition_set = {0, 2, 5, 7}
        
        # 计算条件边集合（Ground Truth）
        self.conditional_edges = set()
        for edge, label in self.edge_labels.items():
            if label in self.condition_set:
                self.conditional_edges.add(edge)
        
        # 正确答案：条件边总数
        self.correct_answer = len(self.conditional_edges)
        
        # 构建邻接表，方便计算条件度数
        self.adjacency = {v: [] for v in self.vertices}
        for u, v in self.edges:
            self.adjacency[u].append(v)
            self.adjacency[v].append(u)
        
        # 填充游戏信息（用于格式化规则文本）
        self._game_info["num_vertices"] = len(self.vertices)
        self._game_info["num_edges"] = len(self.edges)
        self._game_info["vertex_list"] = ", ".join(self.vertices)
        self._game_info["opening_braces"] = "{"
        self._game_info["closing_braces"] = "}"

    def evaluate(self, parsed_info):
        """评估玩家提交的答案"""
        try:
            # 解析答案
            answer_str = parsed_info["answer"].strip()
            player_answer = int(answer_str)
            
            # 检查答案是否正确
            return player_answer == self.correct_answer
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."
        
        vertex = parsed_info["query"].strip()
        
        # 检查顶点是否有效
        if vertex not in self.vertices:
            if self.config.language == "zh":
                return f"错误：顶点 {vertex} 不在图中。有效顶点为：{', '.join(self.vertices)}"
            else:
                return f"Error: Vertex {vertex} is not in the graph. Valid vertices are: {', '.join(self.vertices)}"
        
        # 计算该顶点的条件度数
        conditional_degree = 0
        for neighbor in self.adjacency[vertex]:
            edge = tuple(sorted([vertex, neighbor]))
            if edge in self.conditional_edges:
                conditional_degree += 1
        
        return str(conditional_degree)

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        results = []
        for vertex in self.vertices:
            # 计算该顶点的条件度数
            conditional_degree = 0
            if vertex in self.adjacency:
                for neighbor in self.adjacency[vertex]:
                    edge = tuple(sorted([vertex, neighbor]))
                    if edge in self.conditional_edges:
                        conditional_degree += 1
            
            results.append({
                "query": f"<query>{vertex}</query>",
                "answer": str(conditional_degree)
            })
        return results

    def _cf_make_wrong(self, correct):
        try:
            val = int(correct)
            return str(val + 1)
        except ValueError:
            pass

        if self.config.language == "zh":
            if correct == "是": return "否"
            if correct == "否": return "是"
        else:
            if correct.lower() == "yes":
                return "No" if correct[0].isupper() else "no"
            if correct.lower() == "no":
                return "Yes" if correct[0].isupper() else "yes"

        return correct + "_WRONG"