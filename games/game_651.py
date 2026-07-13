from .base import Game
import re
from collections import deque


class GraphPathIdentificationGame(Game):

    game_rule_zh = """\
我们来玩一个"图路径识别"游戏，规则如下：

游戏设定了一个由 6 个节点（A、B、C、D、E、F）组成的无向等权图，所有边的权重均为 1。图中包含以下边：
A-B、A-C、B-C、B-D、C-D、C-E、D-E、D-F、E-F

在这个图中，某些边可能因故障而不可用。存在四种可能的配置之一正在生效（你不知道是哪一种）：
{config_details}

你的目标是：
1. 通过查询边的状态来推断出当前生效的是哪个配置
2. 基于推断出的配置，找出从起点 A 到终点 F 的最短路径

你可以查询以下边的状态：{queryable_edges}

每次查询会告诉你该边在当前配置下是"可用"还是"不可用"。

约束条件：
- 你必须至少进行 {min_queries} 次查询后才能提交答案
- 你最多可以进行 {max_queries} 次查询
- 请尽可能用较少的查询次数完成任务

## 查询与提交答案的格式

查询边的状态（例如查询 A-B）：
<query_edge>A-B</query_edge>

提交最终答案时，需要指定配置编号（I、II、III 或 IV）和从 A 到 F 的最短路径节点序列，格式如下：
<answer>config=I, path=A,B,D,F</answer>

注意：路径节点之间用逗号分隔，不含空格。
"""

    game_rule_en = """\
Let's play a "Graph Path Identification" game. Here are the rules:

The game features an undirected equal-weight graph with 6 nodes (A, B, C, D, E, F), where all edges have weight 1. The graph contains the following edges:
A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

In this graph, certain edges may be unavailable due to failures. One of four possible configurations is in effect (you don't know which one):
{config_details}

Your objectives are:
1. Infer which configuration is currently in effect by querying edge states
2. Based on the inferred configuration, find the shortest path from start node A to end node F

You can query the status of the following edges: {queryable_edges}

Each query will tell you whether the edge is "available" or "unavailable" in the current configuration.

Constraints:
- You must make at least {min_queries} queries before submitting your answer
- You can make at most {max_queries} queries
- Try to complete the task with as few queries as possible

## Query and Answer Format

To query an edge status (e.g., querying A-B):
<query_edge>A-B</query_edge>

When submitting your final answer, specify the configuration number (I, II, III, or IV) and the shortest path node sequence from A to F, in this format:
<answer>config=I, path=A,B,D,F</answer>

Note: Path nodes are separated by commas without spaces.
"""

    contextualized_rule_zh_1 = """\
我们来进行一次"应急交通路网调度"任务，具体情况如下：

当前区域交通网络由 6 个核心枢纽节点（A、B、C、D、E、F）组成。枢纽之间由双向等距的高速公路连接，包含以下路段：
A-B、A-C、B-C、B-D、C-D、C-E、D-E、D-F、E-F

由于突发地质灾害，部分路段可能受损而无法通行。目前有四种潜在的灾害影响预案配置（你未知当前是哪种配置生效）：
{config_details}

你的核心任务是：
1. 通过查询路段的通行状态，推断出当前生效的是哪一种灾害预案配置
2. 根据确认的预案配置，规划出从枢纽 A 到枢纽 F 的最短畅通路段序列

你可以调取监控查询以下路段的状态：{queryable_edges}

每次查询会反馈该路段在当前灾害影响下是"可用"（畅通）还是"不可用"（阻断）。

约束条件：
- 你必须至少进行 {min_queries} 次路段状态查询后才能提交最终调度方案
- 你最多可以进行 {max_queries} 次查询
- 请尽可能以最少的查询次数完成路网排查

## 查询与提交答案的格式

查询路段状态（例如查询 A-B 路段）：
<query_edge>A-B</query_edge>

提交最终调度方案时，需要指定预案配置编号（I、II、III 或 IV）以及从 A 到 F 的最短通行路径节点序列，格式如下：
<answer>config=I, path=A,B,D,F</answer>

注意：路径节点之间用逗号分隔，不含空格。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's conduct an "Emergency Traffic Network Dispatch" task. Here are the operational details:

The regional traffic network consists of 6 core hub nodes (A, B, C, D, E, F). The hubs are connected by two-way, equal-distance highways, including the following segments:
A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

Due to a sudden geological disaster, certain segments may be damaged and impassable. There are four potential disaster impact plan configurations currently possible (you do not know which one is in effect):
{config_details}

Your core objectives are:
1. Infer which disaster plan configuration is currently in effect by querying the passage status of the segments.
2. Based on the confirmed configuration, route the shortest passable path from hub A to hub F.

You can retrieve surveillance data for the following segments: {queryable_edges}

Each query will indicate whether the segment is "available" (clear) or "unavailable" (blocked) under the current disaster condition.

Constraints:
- You must make at least {min_queries} segment status queries before submitting your final dispatch plan.
- You can make at most {max_queries} queries.
- Please aim to complete the network assessment with as few queries as possible.

## Query and Answer Format

To query a segment status (e.g., querying segment A-B):
<query_edge>A-B</query_edge>

When submitting your final dispatch plan, specify the configuration number (I, II, III, or IV) and the shortest path node sequence from A to F, in this format:
<answer>config=I, path=A,B,D,F</answer>

Note: Path nodes are separated by commas without spaces.
"""

    contextualized_rule_zh_2 = """\
我们来进行一次"神经传导通路诊断"任务，具体情况如下：

患者的局部神经系统可抽象为由 6 个神经节点（A、B、C、D、E、F）组成的传导网络。相邻节点间的传导通路为双向等效阻抗，包含以下通路：
A-B、A-C、B-C、B-D、C-D、C-E、D-E、D-F、E-F

由于病理学病变，部分神经通路可能发生阻断而无法传导电信号。临床上存在四种可能的病理综合征配置之一正在生效（你需要进行确诊）：
{config_details}

你的核心任务是：
1. 通过肌电图测试查询通路的传导状态，确诊当前患者属于哪一种病理综合征配置
2. 基于确诊的综合征配置，找出从刺激点 A 到反应点 F 的最短有效传导通路

你可以测试以下通路的传导状态：{queryable_edges}

每次测试会反馈该通路在当前病理状态下是"可用"（传导正常）还是"不可用"（传导阻断）。

约束条件：
- 你必须至少进行 {min_queries} 次通路测试后才能出具诊断报告
- 你最多可以进行 {max_queries} 次测试
- 请尽可能用较少的测试次数完成确诊，以减轻患者负担

## 测试与提交诊断的格式

测试通路的传导状态（例如测试 A-B 通路）：
<query_edge>A-B</query_edge>

提交最终诊断报告时，需要指定综合征配置编号（I、II、III 或 IV）和从 A 到 F 的最短有效传导节点序列，格式如下：
<answer>config=I, path=A,B,D,F</answer>

注意：路径节点之间用逗号分隔，不含空格。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's conduct a "Neural Conduction Pathway Diagnosis" task. Here are the clinical details:

The patient's localized nervous system can be abstracted as a conduction network consisting of 6 neural nodes (A, B, C, D, E, F). The conduction pathways between adjacent nodes have bidirectional equal impedance, including the following pathways:
A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

Due to pathological lesions, certain neural pathways may be blocked and unable to conduct electrical signals. Clinically, one of four possible pathological syndrome configurations is in effect (you need to diagnose which one):
{config_details}

Your core objectives are:
1. Diagnose which pathological syndrome configuration is currently in effect by electromyography testing of the pathways' conduction status.
2. Based on the diagnosed syndrome configuration, identify the shortest effective conduction pathway from stimulus point A to response point F.

You can test the conduction status of the following pathways: {queryable_edges}

Each test will report whether the pathway is "available" (normal conduction) or "unavailable" (conduction blocked) under the current pathological condition.

Constraints:
- You must make at least {min_queries} pathway tests before issuing your diagnosis report.
- You can make at most {max_queries} tests.
- Please aim to complete the diagnosis with as few tests as possible to minimize patient burden.

## Test and Diagnosis Submission Format

To test a pathway's conduction status (e.g., testing pathway A-B):
<query_edge>A-B</query_edge>

When submitting your final diagnosis report, specify the syndrome configuration number (I, II, III, or IV) and the shortest effective conduction node sequence from A to F, in this format:
<answer>config=I, path=A,B,D,F</answer>

Note: Path nodes are separated by commas without spaces.
"""

    contextualized_rule_zh_3 = """\
我们来进行一次"认知结构图谱测定"任务，具体情况如下：

某个学科的知识网络由 6 个核心知识模块（A、B、C、D、E、F）组成。模块之间存在无向的同等学习转化依赖关系，包含以下认知关联：
A-B、A-C、B-C、B-D、C-D、C-E、D-E、D-F、E-F

由于学生的个体差异或学习困难，部分认知关联可能未建立或存在认知障碍。根据教学经验，该学生目前属于四种常见的认知误区配置之一（你未知具体是哪一种）：
{config_details}

你的核心任务是：
1. 通过测验特定知识关联的掌握状态，诊断出该学生当前的认知误区配置
2. 基于诊断出的误区配置，规划出从基础概念 A 到高级应用 F 的最短顺畅学习路径

你可以测验以下认知关联的掌握状态：{queryable_edges}

每次测验会反馈该关联对该学生而言是"可用"（认知顺畅）还是"不可用"（存在障碍）。

约束条件：
- 你必须至少进行 {min_queries} 次测验后才能提交个性化学习方案
- 你最多可以进行 {max_queries} 次测验
- 请尽可能用较少的测验次数完成诊断，以免增加学生的焦虑感

## 测验与提交方案的格式

测验认知关联状态（例如测验 A-B 关联）：
<query_edge>A-B</query_edge>

提交最终学习方案时，需要指定认知误区配置编号（I、II、III 或 IV）和从 A 到 F 的最短顺畅学习路径节点序列，格式如下：
<answer>config=I, path=A,B,D,F</answer>

注意：路径节点之间用逗号分隔，不含空格。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Cognitive Structure Mapping" task. Here are the pedagogical details:

A subject's knowledge network is composed of 6 core knowledge modules (A, B, C, D, E, F). There are undirected, equally weighted learning transfer dependencies between these modules, including the following cognitive links:
A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

Due to individual differences or learning difficulties, certain cognitive links may be unestablished or obstructed by cognitive barriers. Based on teaching experience, the student currently falls into one of four common cognitive misconception configurations (you do not know which one):
{config_details}

Your core objectives are:
1. Diagnose the student's current cognitive misconception configuration by testing their mastery status of specific knowledge links.
2. Based on the diagnosed misconception configuration, map out the shortest fluid learning path from foundational concept A to advanced application F.

You can test the mastery status of the following cognitive links: {queryable_edges}

Each test will provide feedback on whether the link is "available" (fluently understood) or "unavailable" (obstructed by a barrier) for the student.

Constraints:
- You must administer at least {min_queries} tests before submitting the personalized learning plan.
- You can administer at most {max_queries} tests.
- Please aim to complete the diagnosis with as few tests as possible to avoid increasing the student's anxiety.

## Test and Plan Submission Format

To test a cognitive link's status (e.g., testing link A-B):
<query_edge>A-B</query_edge>

When submitting your final learning plan, specify the misconception configuration number (I, II, III, or IV) and the shortest fluid learning path node sequence from A to F, in this format:
<answer>config=I, path=A,B,D,F</answer>

Note: Path nodes are separated by commas without spaces.
"""

    contextualized_rule_zh_4 = """\
我们来进行一次"工业产线故障排查与物流重构"任务，具体情况如下：

智能制造工厂的物流系统由 6 个加工车间（A、B、C、D、E、F）组成。车间之间通过双向等速的自动传送带连接，包含以下传送路线：
A-B、A-C、B-C、B-D、C-D、C-E、D-E、D-F、E-F

由于设备老化或电网波动，部分传送带可能发生故障而停机。主控系统提示，当前工厂网络处于四种已知的故障模式配置之一（你未知当前是哪种模式）：
{config_details}

你的核心任务是：
1. 通过检测传送带的运行状态，排查出当前工厂处于哪一种故障模式配置
2. 基于排查出的故障模式，重新规划从原料库 A 到成品库 F 的最短可用物流输送路径

你可以向传感器网络发送指令检测以下传送带的状态：{queryable_edges}

每次检测会反馈该传送带在当前模式下是"可用"（正常运转）还是"不可用"（故障停机）。

约束条件：
- 你必须至少进行 {min_queries} 次检测后才能提交最终物流重构方案
- 你最多可以进行 {max_queries} 次检测
- 请尽可能用较少的检测次数完成排查，以降低系统通信负荷

## 检测与提交方案的格式

检测传送带状态（例如检测 A-B 路线）：
<query_edge>A-B</query_edge>

提交最终物流重构方案时，需要指定故障模式配置编号（I、II、III 或 IV）和从 A 到 F 的最短可用物流路径节点序列，格式如下：
<answer>config=I, path=A,B,D,F</answer>

注意：路径节点之间用逗号分隔，不含空格。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct an "Industrial Production Line Troubleshooting and Logistics Reconfiguration" task. Here are the operational details:

The logistics system of a smart manufacturing plant consists of 6 processing workshops (A, B, C, D, E, F). The workshops are connected by bidirectional, equal-speed automated conveyor belts, including the following conveyor routes:
A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

Due to equipment aging or power grid fluctuations, certain conveyor belts may experience faults and shut down. The main control system indicates that the plant network is currently in one of four known fault mode configurations (you do not know which mode is active):
{config_details}

Your core objectives are:
1. Troubleshoot which fault mode configuration is currently active by inspecting the operational status of the conveyor belts.
2. Based on the identified fault mode, reconfigure the shortest available logistics transport path from the raw material warehouse A to the finished goods warehouse F.

You can send commands to the sensor network to inspect the status of the following conveyor belts: {queryable_edges}

Each inspection will return whether the conveyor belt is "available" (operating normally) or "unavailable" (faulty and shut down) under the current mode.

Constraints:
- You must make at least {min_queries} inspections before submitting your final logistics reconfiguration plan.
- You can make at most {max_queries} inspections.
- Please aim to complete the troubleshooting with as few inspections as possible to reduce system communication load.

## Inspection and Plan Submission Format

To inspect a conveyor belt's status (e.g., inspecting route A-B):
<query_edge>A-B</query_edge>

When submitting your final logistics reconfiguration plan, specify the fault mode configuration number (I, II, III, or IV) and the shortest available logistics path node sequence from A to F, in this format:
<answer>config=I, path=A,B,D,F</answer>

Note: Path nodes are separated by commas without spaces.
"""

    contextualized_rule_zh_5 = """\
我们来进行一次"非法资金流转网络追踪"任务，具体情况如下：

某涉案集团的资金洗白网络由 6 个实体账户（A、B、C、D、E、F）组成。账户之间存在双向同等级别的资金流转通道，包含以下通道：
A-B、A-C、B-C、B-D、C-D、C-E、D-E、D-F、E-F

由于执法部门的介入，部分通道已被依法冻结而无法流转资金。根据情报分析，该集团目前的资金隐匿网络处于四种可能的洗钱特征配置之一（你未知具体是哪一种）：
{config_details}

你的核心任务是：
1. 通过向有关部门查询资金通道的法律状态，推断出该集团当前采用的是哪一种洗钱特征配置
2. 基于推断出的特征配置，追踪出从初始黑钱账户 A 到最终洗白账户 F 的最短有效资金转移路径，以便实施精准打击

你可以依法调证查询以下通道的状态：{queryable_edges}

每次查询会反馈该通道在当前网络特征下是"可用"（合法存续可流转）还是"不可用"（已被冻结或无效）。

约束条件：
- 你必须至少进行 {min_queries} 次调证查询后才能提交案件分析报告
- 你最多可以进行 {max_queries} 次查询
- 请尽可能用较少的查询次数完成排查，以免惊动犯罪分子

## 查询与提交报告的格式

查询资金通道状态（例如查询 A-B 通道）：
<query_edge>A-B</query_edge>

提交最终案件分析报告时，需要指定特征配置编号（I、II、III 或 IV）和从 A 到 F 的最短有效资金转移节点序列，格式如下：
<answer>config=I, path=A,B,D,F</answer>

注意：路径节点之间用逗号分隔，不含空格。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's conduct an "Illicit Fund Transfer Network Tracking" task. Here are the case details:

A suspect syndicate's money laundering network consists of 6 entity accounts (A, B, C, D, E, F). There are bidirectional, equal-tier fund transfer channels between these accounts, including the following channels:
A-B, A-C, B-C, B-D, C-D, C-E, D-E, D-F, E-F

Due to law enforcement intervention, certain channels have been legally frozen and cannot transfer funds. According to intelligence analysis, the syndicate's fund concealment network currently operates under one of four possible money laundering topological configurations (you do not know which one):
{config_details}

Your core objectives are:
1. Deduce which money laundering topological configuration the syndicate is currently using by querying the legal status of the fund channels with relevant authorities.
2. Based on the deduced configuration, trace the shortest active fund transfer path from the initial illicit account A to the final laundered account F to execute a precision strike.

You can legally subpoena and query the status of the following channels: {queryable_edges}

Each query will indicate whether the channel is "available" (legally active and transferable) or "unavailable" (frozen or invalid) under the current network topology.

Constraints:
- You must make at least {min_queries} subpoena queries before submitting your case analysis report.
- You can make at most {max_queries} queries.
- Please aim to complete the tracking with as few queries as possible to avoid alerting the criminals.

## Query and Report Submission Format

To query a fund channel's status (e.g., querying channel A-B):
<query_edge>A-B</query_edge>

When submitting your final case analysis report, specify the topological configuration number (I, II, III, or IV) and the shortest active fund transfer node sequence from A to F, in this format:
<answer>config=I, path=A,B,D,F</answer>

Note: Path nodes are separated by commas without spaces.
"""

    tags = ["answer", "query_edge"]
    reasoning_type = "溯因推理"
    data_structure = "图"

    # 难度配置：
    # 1 (简单) - 最多3次查询，最少2次，配置差异明显
    # 2 (中等偏下) - 最多3次查询，最少2次，需要更仔细推断
    # 3 (中等偏上) - 最多3次查询，最少2次，配置更复杂
    # 4 (较难) - 最多3次查询，最少2次，需要综合判断
    # 5 (难) - 最多3次查询，最少2次，最具挑战性

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "queryable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "min_queries": 2,
                "max_queries": 3,
                "config_id": "I",
                "unavailable_edges": ["A-C", "C-D"],
                "shortest_path": ["A", "B", "D", "F"],
                "responses": {
                    "available": "可用",
                    "unavailable": "不可用"
                }
            },
            2: {
                "queryable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "min_queries": 2,
                "max_queries": 3,
                "config_id": "II",
                "unavailable_edges": ["A-B", "D-F"],
                "shortest_path": ["A", "C", "E", "F"],
                "responses": {
                    "available": "可用",
                    "unavailable": "不可用"
                }
            },
            3: {
                "queryable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "min_queries": 2,
                "max_queries": 3,
                "config_id": "III",
                "unavailable_edges": ["B-D", "C-E"],
                "shortest_path": ["A", "B", "C", "D", "F"],
                "responses": {
                    "available": "可用",
                    "unavailable": "不可用"
                }
            },
            4: {
                "queryable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "min_queries": 2,
                "max_queries": 3,
                "config_id": "IV",
                "unavailable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "shortest_path": ["A", "C", "D", "E", "F"],
                "responses": {
                    "available": "可用",
                    "unavailable": "不可用"
                }
            },
            5: {
                "queryable_edges": ["A-C", "B-C", "C-E", "D-F"],
                "min_queries": 2,
                "max_queries": 3,
                "config_id": "IV",
                "unavailable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "shortest_path": ["A", "C", "D", "E", "F"],
                "responses": {
                    "available": "可用",
                    "unavailable": "不可用"
                }
            },
        },
        "en": {
            1: {
                "queryable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "min_queries": 2,
                "max_queries": 3,
                "config_id": "I",
                "unavailable_edges": ["A-C", "C-D"],
                "shortest_path": ["A", "B", "D", "F"],
                "responses": {
                    "available": "available",
                    "unavailable": "unavailable"
                }
            },
            2: {
                "queryable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "min_queries": 2,
                "max_queries": 3,
                "config_id": "II",
                "unavailable_edges": ["A-B", "D-F"],
                "shortest_path": ["A", "C", "E", "F"],
                "responses": {
                    "available": "available",
                    "unavailable": "unavailable"
                }
            },
            3: {
                "queryable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "min_queries": 2,
                "max_queries": 3,
                "config_id": "III",
                "unavailable_edges": ["B-D", "C-E"],
                "shortest_path": ["A", "B", "C", "D", "F"],
                "responses": {
                    "available": "available",
                    "unavailable": "unavailable"
                }
            },
            4: {
                "queryable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "min_queries": 2,
                "max_queries": 3,
                "config_id": "IV",
                "unavailable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "shortest_path": ["A", "C", "D", "E", "F"],
                "responses": {
                    "available": "available",
                    "unavailable": "unavailable"
                }
            },
            5: {
                "queryable_edges": ["A-C", "B-C", "C-E", "D-F"],
                "min_queries": 2,
                "max_queries": 3,
                "config_id": "IV",
                "unavailable_edges": ["A-B", "B-D", "C-E", "D-F"],
                "shortest_path": ["A", "C", "D", "E", "F"],
                "responses": {
                    "available": "available",
                    "unavailable": "unavailable"
                }
            },
        },
    }

    def __init__(self, config):
        self.query_count = 0  # 查询计数器
        super().__init__(config)

    def _build_config_details(self, lang):
        """构建四种配置的详细说明"""
        # 定义四种配置（固定，与难度无关）
        configs = {
            "I": ["A-C", "C-D"],
            "II": ["A-B", "D-F"],
            "III": ["B-D", "C-E"],
            "IV": ["A-B", "B-D", "C-E", "D-F"],
        }
        if lang == "zh":
            lines = []
            for cid, edges in configs.items():
                lines.append(f"- 配置 {cid}：不可用的边为 {'、'.join(edges)}")
            return "\n".join(lines)
        else:
            lines = []
            for cid, edges in configs.items():
                lines.append(f"- Configuration {cid}: Unavailable edges are {', '.join(edges)}")
            return "\n".join(lines)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置游戏参数
        self.queryable_edges = cfg["queryable_edges"]
        self.min_queries = cfg["min_queries"]
        self.max_queries = cfg["max_queries"]
        self.config_id = cfg["config_id"]
        self.unavailable_edges = cfg["unavailable_edges"]
        self.shortest_path = cfg["shortest_path"]
        self.responses = cfg["responses"]
        
        # 用于格式化游戏规则
        self._game_info["queryable_edges"] = "、".join(self.queryable_edges) if lang == "zh" else ", ".join(self.queryable_edges)
        self._game_info["min_queries"] = self.min_queries
        self._game_info["max_queries"] = self.max_queries
        
        # 添加四种配置的详细描述，让玩家可以进行推理区分
        self._game_info["config_details"] = self._build_config_details(lang)
        
        # 完整图的边集（用于验证路径）
        self.all_edges = [
            "A-B", "A-C", "B-C", "B-D", "C-D", 
            "C-E", "D-E", "D-F", "E-F"
        ]

    def _normalize_edge(self, edge_str):
        """标准化边的表示（例如 B-A 转为 A-B）"""
        parts = edge_str.strip().split("-")
        if len(parts) != 2:
            return None
        a, b = parts[0].strip(), parts[1].strip()
        return f"{min(a, b)}-{max(a, b)}"

    def _is_edge_available(self, edge):
        """判断边是否可用"""
        normalized = self._normalize_edge(edge)
        return normalized not in self.unavailable_edges

    def _find_shortest_path_length(self):
        """BFS 计算从 A 到 F 的最短路径长度（节点数）"""
        # 构建可用边的邻接表
        adj = {}
        for node in "ABCDEF":
            adj[node] = []
        for edge in self.all_edges:
            if self._is_edge_available(edge):
                a, b = edge.split("-")
                adj[a].append(b)
                adj[b].append(a)
        
        # BFS
        queue = deque([("A", ["A"])])
        visited = {"A"}
        while queue:
            node, path = queue.popleft()
            if node == "F":
                return len(path)
            for neighbor in adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return float('inf')  # 不可达

    def _validate_path(self, path_nodes):
        """验证路径是否有效且为最短路径"""
        # 检查起点和终点
        if len(path_nodes) < 2:
            return False, "path_too_short"
        if path_nodes[0] != "A" or path_nodes[-1] != "F":
            return False, "wrong_endpoints"
        
        # 检查路径中的每条边是否存在且可用
        for i in range(len(path_nodes) - 1):
            edge = f"{path_nodes[i]}-{path_nodes[i+1]}"
            normalized = self._normalize_edge(edge)
            
            # 检查边是否在图中存在
            if normalized not in self.all_edges:
                return False, "edge_not_exist"
            
            # 检查边是否可用
            if not self._is_edge_available(normalized):
                return False, "edge_unavailable"
        
        # 检查是否为最短路径（通过 BFS 验证长度）
        shortest_len = self._find_shortest_path_length()
        if len(path_nodes) > shortest_len:
            return False, "not_shortest"
        
        return True, "valid"

    def evaluate(self, parsed_info):
        # 检查是否满足最少查询次数要求
        if self.query_count < self.min_queries:
            return False
            
        # 解析答案: config=I, path=A,B,D,F
        raw_ans = parsed_info["answer"]
        
        # 提取 config 和 path
        config_match = re.search(r'config\s*=\s*(IV|III|II|I)\b', raw_ans, re.IGNORECASE)
        path_match = re.search(r'path\s*=\s*([A-Z,]+)', raw_ans, re.IGNORECASE)
        
        if not config_match or not path_match:
            return False
        
        model_config = config_match.group(1).upper()
        model_path_str = path_match.group(1)
        
        # 检查配置是否正确
        if model_config != self.config_id:
            return False
        
        # 解析路径
        try:
            path_nodes = [node.strip() for node in model_path_str.split(",")]
        except:
            return False
        
        # 验证路径
        is_valid, _ = self._validate_path(path_nodes)
        return is_valid

    def _cf_core_produce(self, parsed_info):
        if "query_edge" in parsed_info:
            # 检查是否超过最大查询次数
            if self.query_count >= self.max_queries:
                if self.config.language == "zh":
                    return f"错误：已达到最大查询次数（{self.max_queries}次）。请直接提交你的最终答案。"
                else:
                    return f"Error: Maximum query limit ({self.max_queries}) reached. Please submit your final answer now."
            
            edge_query = parsed_info["query_edge"].strip()
            normalized = self._normalize_edge(edge_query)
            
            if normalized is None:
                if self.config.language == "zh":
                    return f"错误：无法解析边 {edge_query}。"
                else:
                    return f"Error: Cannot parse edge {edge_query}."
            
            # 对 queryable_edges 也标准化后比较
            normalized_queryable = [self._normalize_edge(e) for e in self.queryable_edges]
            if normalized not in normalized_queryable:
                if self.config.language == "zh":
                    return f"错误：边 {edge_query} 不在可查询列表中。"
                else:
                    return f"Error: Edge {edge_query} is not in the queryable list."
            
            # 增加查询计数
            self.query_count += 1
            
            # 返回边的状态
            is_available = self._is_edge_available(normalized)
            status = self.responses["available"] if is_available else self.responses["unavailable"]
            
            return f"{normalized}: {status}"
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        queries = []
        for edge in self.queryable_edges:
            normalized = self._normalize_edge(edge)
            
            # 不增加查询计数，直接计算结果
            is_available = self._is_edge_available(normalized)
            status = self.responses["available"] if is_available else self.responses["unavailable"]
            answer = f"{normalized}: {status}"
            
            queries.append({
                "query": f"<query_edge>{edge}</query_edge>",
                "answer": answer
            })
        return queries

    def _cf_make_wrong(self, correct: str) -> str:
        # 针对实际响应格式进行翻转
        if self.config.language == "zh":
            if "不可用" in correct:
                return correct.replace("不可用", "可用")
            if "可用" in correct:
                return correct.replace("可用", "不可用")
        else:  # en
            if "unavailable" in correct:
                return correct.replace("unavailable", "available")
            if "available" in correct:
                return correct.replace("available", "unavailable")
        
        # fallback
        return correct + "_WRONG"