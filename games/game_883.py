from .base import Game
import re
from typing import Set, Dict, List, Tuple

class GraphCutVertexInferenceGame(Game):
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"图割点推断"游戏，规则如下：

游戏设定了一个固定但不可见的无向图 G，顶点集合为 1 到 {n}，边的连接关系对你隐藏。同时，存在一个固定但未知的整数函数 F，它将图的连通分量数映射为一个整数反馈值。F 的具体形式对你隐藏，但它在整个游戏过程中保持不变、确定且一致。

你的目标是：
1. 通过有限次查询，归纳出一个通用的判定规则 R，能够根据反馈值判定删除某个顶点是否会使图的连通分量数增加（即判定该顶点是否为割点）。
2. 根据你的规则，列出图中所有割点的完整清单。

你可以进行以下两种类型的查询：

1. 单点删除查询：指定一个顶点 v（1 到 {n} 之间的整数），系统会返回从图中删除该顶点后的反馈值。对同一顶点的重复查询会返回相同结果。

2. 基线查询（最多使用一次）：不删除任何顶点，系统返回原图的反馈值。这可以帮助你建立参考基准。

注意：
- 你最多可以进行 {max_queries} 次查询（基线查询也计入次数）。
- 在提交最终答案前，你必须至少完成 3 次有效查询。
- 不得直接询问边的存在性、可达性或要求解释 F 的形式。
- 图 G 和函数 F 在整个游戏过程中不会改变，所有返回值都是确定的。

## 查询与提交答案的格式

每次只能包含一个查询或答案标签。

- 单点删除查询（例如查询删除顶点 5 后的反馈值）：
<query_remove>5</query_remove>

- 基线查询（查询原图的反馈值，内容为空）：
<query_baseline></query_baseline>

提交最终答案时，需要包含两部分：
1. rule: 你归纳出的判定规则（用自然语言描述如何根据反馈值判定割点）
2. cut_vertices: 所有割点的编号列表（用逗号隔开，若无割点则填写"无"或"none"）

格式如下：
<answer>rule=若删除顶点后的反馈值大于基线值则为割点, cut_vertices=1,3,5</answer>

或者当没有割点时：
<answer>rule=若删除顶点后的反馈值大于基线值则为割点, cut_vertices=无</answer>
"""

    game_rule_en = """\
Let's play a "Graph Cut Vertex Inference" game. Here are the rules:

The game has set up a fixed but invisible undirected graph G with vertices numbered from 1 to {n}. The edge connections are hidden from you. Additionally, there exists a fixed but unknown integer function F that maps the number of connected components in a graph to an integer feedback value. The specific form of F is hidden from you, but it remains constant, deterministic, and consistent throughout the game.

Your goals are:
1. Through a limited number of queries, deduce a general decision rule R that can determine whether removing a vertex increases the number of connected components (i.e., whether the vertex is a cut vertex) based on feedback values.
2. Based on your rule, list the complete set of all cut vertices in the graph.

You can perform the following two types of queries:

1. Single-point removal query: Specify a vertex v (an integer between 1 and {n}), and the system will return the feedback value after removing that vertex from the graph. Repeated queries for the same vertex will return the same result.

2. Baseline query (can be used at most once): Without removing any vertex, the system returns the feedback value of the original graph. This can help you establish a reference baseline.

Notes:
- You can perform at most {max_queries} queries (baseline query also counts).
- Before submitting your final answer, you must complete at least 3 valid queries.
- You cannot directly ask about edge existence, reachability, or request an explanation of F's form.
- Graph G and function F will not change throughout the game, and all return values are deterministic.

## Query and Answer Format

Each turn can contain only one query or answer tag.

- Single-point removal query (e.g., query feedback after removing vertex 5):
<query_remove>5</query_remove>

- Baseline query (query original graph feedback, empty content):
<query_baseline></query_baseline>

When submitting the final answer, include two parts:
1. rule: Your deduced decision rule (describe in natural language how to determine cut vertices based on feedback values)
2. cut_vertices: List of all cut vertex IDs (comma-separated; use "none" if there are no cut vertices)

Format:
<answer>rule=A vertex is a cut vertex if its removal feedback is greater than baseline, cut_vertices=1,3,5</answer>

Or when there are no cut vertices:
<answer>rule=A vertex is a cut vertex if its removal feedback is greater than baseline, cut_vertices=none</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用城市交通路网连通性评估系统。我们的目标是排查出所有的关键交通枢纽。

系统设定了一个固定但不可见的城市路网 G，包含编号从 1 到 {n} 的交通枢纽，枢纽间的道路连接对你隐藏。同时，存在一个固定但未知的诊断函数 F，它将当前路网中相互隔离的片区数量映射为一个整数型的系统诊断指数。F 的具体计算公式对你隐藏，但它在整个排查过程中保持不变、确定且一致。

你的目标是：
1. 通过有限次模拟封闭测试，归纳出一个通用的判定规则 R，能够根据诊断指数判定封闭某个枢纽是否会导致城市路网分裂成更多的隔离片区（即判定该枢纽是否为关键枢纽）。
2. 根据你的规则，列出路网中所有关键枢纽的完整编号清单。

你可以进行以下两种类型的测试：

1. 单点封闭测试：指定一个交通枢纽 v（1 到 {n} 之间的整数），系统会返回封闭该枢纽后的诊断指数。对同一枢纽的重复测试会返回相同结果。

2. 基线测试（最多使用一次）：不封闭任何枢纽，系统返回原路网的诊断指数。这可以帮助你建立参考基准。

注意：
- 你最多可以进行 {max_queries} 次测试（基线测试也计入次数）。
- 在提交最终报告前，你必须至少完成 3 次有效测试。
- 不得直接询问道路的存在性、可达性或要求解释 F 的公式。
- 路网 G 和函数 F 在整个排查过程中不会改变，所有返回值都是确定的。

## 测试与提交报告的格式

每次只能包含一个测试或报告标签。

- 单点封闭测试（例如测试封闭枢纽 5 后的诊断指数）：
<query_remove>5</query_remove>

- 基线测试（测试原路网的诊断指数，内容为空）：
<query_baseline></query_baseline>

提交最终报告时，需要包含两部分：
1. rule: 你归纳出的判定规则（用自然语言描述如何根据诊断指数判定关键枢纽）
2. cut_vertices: 所有关键枢纽的编号列表（用逗号隔开，若无关键枢纽则填写"无"或"none"）

格式如下：
<answer>rule=若封闭枢纽后的诊断指数大于基线值则为关键枢纽, cut_vertices=1,3,5</answer>

或者当没有关键枢纽时：
<answer>rule=若封闭枢纽后的诊断指数大于基线值则为关键枢纽, cut_vertices=无</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Urban Traffic Network Connectivity Assessment System. Our goal is to identify all critical transport hubs.

The system features a fixed but invisible urban road network G, with transport hubs numbered from 1 to {n}. The road connections are hidden from you. Additionally, there exists a fixed but unknown diagnostic function F that maps the number of isolated traffic zones in the network to an integer system diagnostic index. The specific formula of F is hidden from you, but it remains constant, deterministic, and consistent throughout the assessment.

Your goals are:
1. Through a limited number of simulated closure tests, deduce a general decision rule R that can determine whether closing a hub fragments the network into more isolated zones (i.e., whether the hub is a critical hub) based on the diagnostic index.
2. Based on your rule, list the complete set of all critical hub IDs in the network.

You can perform the following two types of tests:

1. Single-point closure test: Specify a transport hub v (an integer between 1 and {n}), and the system will return the diagnostic index after closing that hub. Repeated tests for the same hub will return the same result.

2. Baseline test (can be used at most once): Without closing any hub, the system returns the diagnostic index of the original network. This can help you establish a reference baseline.

Notes:
- You can perform at most {max_queries} tests (baseline test also counts).
- Before submitting your final report, you must complete at least 3 valid tests.
- You cannot directly ask about road existence, reachability, or request an explanation of F's formula.
- Network G and function F will not change throughout the assessment, and all return values are deterministic.

## Test and Report Format

Each turn can contain only one test or report tag.

- Single-point closure test (e.g., test index after closing hub 5):
<query_remove>5</query_remove>

- Baseline test (test original network index, empty content):
<query_baseline></query_baseline>

When submitting the final report, include two parts:
1. rule: Your deduced decision rule (describe in natural language how to determine critical hubs based on the diagnostic index)
2. cut_vertices: List of all critical hub IDs (comma-separated; use "none" if there are no critical hubs)

Format:
<answer>rule=A hub is critical if its closure index is greater than baseline, cut_vertices=1,3,5</answer>

Or when there are no critical hubs:
<answer>rule=A hub is critical if its closure index is greater than baseline, cut_vertices=none</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用神经网络病理节段分析系统。我们需要找出所有维持神经网络协同运作的核心神经元。

系统设定了一个固定但不可见的神经网络 G，包含编号从 1 到 {n} 的神经元节点，节点间的突触连接对你隐藏。同时，存在一个固定但未知的生物标志物函数 F，它将当前神经网络中彼此孤立的功能簇数量映射为一个整数型的神经活跃度指标。F 的具体代谢机制对你隐藏，但它在整个分析过程中保持不变、确定且一致。

你的目标是：
1. 通过有限次靶向抑制干预，归纳出一个通用的判定规则 R，能够根据神经活跃度指标判定抑制某个神经元是否会导致神经网络分裂成更多的孤立功能簇（即判定该神经元是否为核心神经元）。
2. 根据你的规则，列出网络中所有核心神经元的完整编号清单。

你可以进行以下两种类型的干预：

1. 单点靶向抑制：指定一个神经元节点 v（1 到 {n} 之间的整数），系统会返回抑制该节点后的神经活跃度指标。对同一节点的重复抑制会返回相同结果。

2. 基线检测（最多使用一次）：不抑制任何节点，系统返回原神经网络的神经活跃度指标。这可以帮助你建立参考基准。

注意：
- 你最多可以进行 {max_queries} 次干预（基线检测也计入次数）。
- 在提交最终诊断前，你必须至少完成 3 次有效干预。
- 不得直接询问突触连接的存在性、信号可达性或要求解释 F 的机制。
- 神经网络 G 和函数 F 在整个分析过程中不会改变，所有返回值都是确定的。

## 干预与提交诊断的格式

每次只能包含一个干预或诊断标签。

- 单点靶向抑制（例如检测抑制节点 5 后的指标）：
<query_remove>5</query_remove>

- 基线检测（检测原神经网络的指标，内容为空）：
<query_baseline></query_baseline>

提交最终诊断时，需要包含两部分：
1. rule: 你归纳出的判定规则（用自然语言描述如何根据活跃度指标判定核心神经元）
2. cut_vertices: 所有核心神经元的编号列表（用逗号隔开，若无核心神经元则填写"无"或"none"）

格式如下：
<answer>rule=若抑制节点后的指标大于基线值则为核心神经元, cut_vertices=1,3,5</answer>

或者当没有核心神经元时：
<answer>rule=若抑制节点后的指标大于基线值则为核心神经元, cut_vertices=无</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Neural Network Pathological Segment Analysis System. We need to identify all core neurons maintaining coordinated neural operations.

The system features a fixed but invisible neural network G, with neuron nodes numbered from 1 to {n}. The synaptic connections are hidden from you. Additionally, there exists a fixed but unknown biomarker function F that maps the number of isolated functional clusters in the network to an integer neural activation index. The specific metabolic mechanism of F is hidden from you, but it remains constant, deterministic, and consistent throughout the analysis.

Your goals are:
1. Through a limited number of targeted inhibition interventions, deduce a general decision rule R that can determine whether inhibiting a neuron fragments the network into more isolated clusters (i.e., whether the neuron is a core neuron) based on the neural activation index.
2. Based on your rule, list the complete set of all core neuron IDs in the network.

You can perform the following two types of interventions:

1. Single-point targeted inhibition: Specify a neuron node v (an integer between 1 and {n}), and the system will return the neural activation index after inhibiting that node. Repeated inhibitions for the same node will return the same result.

2. Baseline detection (can be used at most once): Without inhibiting any node, the system returns the neural activation index of the original neural network. This can help you establish a reference baseline.

Notes:
- You can perform at most {max_queries} interventions (baseline detection also counts).
- Before submitting your final diagnosis, you must complete at least 3 valid interventions.
- You cannot directly ask about synaptic existence, signal reachability, or request an explanation of F's mechanism.
- Neural network G and function F will not change throughout the analysis, and all return values are deterministic.

## Intervention and Diagnosis Format

Each turn can contain only one intervention or diagnosis tag.

- Single-point targeted inhibition (e.g., detect index after inhibiting node 5):
<query_remove>5</query_remove>

- Baseline detection (detect original neural network index, empty content):
<query_baseline></query_baseline>

When submitting the final diagnosis, include two parts:
1. rule: Your deduced decision rule (describe in natural language how to determine core neurons based on the activation index)
2. cut_vertices: List of all core neuron IDs (comma-separated; use "none" if there are no core neurons)

Format:
<answer>rule=A neuron is a core neuron if its inhibition index is greater than baseline, cut_vertices=1,3,5</answer>

Or when there are no core neurons:
<answer>rule=A neuron is a core neuron if its inhibition index is greater than baseline, cut_vertices=none</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用学科知识图谱解构系统。我们要寻找出知识体系中的基石概念。

系统设定了一个固定但不可见的知识图谱 G，包含编号从 1 到 {n} 的知识概念，概念间的关联逻辑对你隐藏。同时，存在一个固定但未知的认知评估函数 F，它将当前知识体系中缺乏关联的独立知识模块数量映射为一个整数型的认知负荷指数。F 的具体评价标准对你隐藏，但它在整个解构过程中保持不变、确定且一致。

你的目标是：
1. 通过有限次概念剥离测试，归纳出一个通用的判定规则 R，能够根据认知负荷指数判定剥离某个概念是否会导致知识体系碎裂成更多的独立模块（即判定该概念是否为基石概念）。
2. 根据你的规则，列出图谱中所有基石概念的完整编号清单。

你可以进行以下两种类型的测试：

1. 单点概念剥离：指定一个知识概念 v（1 到 {n} 之间的整数），系统会返回从图谱中剥离该概念后的认知负荷指数。对同一概念的重复剥离会返回相同结果。

2. 基线测试（最多使用一次）：不剥离任何概念，系统返回原知识图谱的认知负荷指数。这可以帮助你建立参考基准。

注意：
- 你最多可以进行 {max_queries} 次测试（基线测试也计入次数）。
- 在提交最终解析前，你必须至少完成 3 次有效测试。
- 不得直接询问概念间的关联存在性、推导可达性或要求解释 F 的评价标准。
- 知识图谱 G 和函数 F 在整个解构过程中不会改变，所有返回值都是确定的。

## 测试与提交解析的格式

每次只能包含一个测试或解析标签。

- 单点概念剥离（例如测试剥离概念 5 后的负荷指数）：
<query_remove>5</query_remove>

- 基线测试（测试原知识图谱的负荷指数，内容为空）：
<query_baseline></query_baseline>

提交最终解析时，需要包含两部分：
1. rule: 你归纳出的判定规则（用自然语言描述如何根据认知负荷指数判定基石概念）
2. cut_vertices: 所有基石概念的编号列表（用逗号隔开，若无基石概念则填写"无"或"none"）

格式如下：
<answer>rule=若剥离概念后的负荷指数大于基线值则为基石概念, cut_vertices=1,3,5</answer>

或者当没有基石概念时：
<answer>rule=若剥离概念后的负荷指数大于基线值则为基石概念, cut_vertices=无</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Subject Knowledge Graph Deconstruction System. We aim to identify the cornerstone concepts within the knowledge architecture.

The system features a fixed but invisible knowledge graph G, with knowledge concepts numbered from 1 to {n}. The logical associations between concepts are hidden from you. Additionally, there exists a fixed but unknown cognitive evaluation function F that maps the number of unassociated, independent knowledge modules to an integer cognitive load index. The specific evaluation criteria of F are hidden from you, but they remain constant, deterministic, and consistent throughout the deconstruction process.

Your goals are:
1. Through a limited number of concept ablation tests, deduce a general decision rule R that can determine whether ablating a concept fragments the knowledge architecture into more independent modules (i.e., whether it is a cornerstone concept) based on the cognitive load index.
2. Based on your rule, list the complete set of all cornerstone concept IDs in the graph.

You can perform the following two types of tests:

1. Single-point concept ablation: Specify a knowledge concept v (an integer between 1 and {n}), and the system will return the cognitive load index after ablating that concept. Repeated ablations for the same concept will return the same result.

2. Baseline test (can be used at most once): Without ablating any concept, the system returns the cognitive load index of the original knowledge graph. This can help you establish a reference baseline.

Notes:
- You can perform at most {max_queries} tests (baseline test also counts).
- Before submitting your final analysis, you must complete at least 3 valid tests.
- You cannot directly ask about the existence of associations, derivational reachability, or request an explanation of F's criteria.
- Knowledge graph G and function F will not change throughout the deconstruction process, and all return values are deterministic.

## Test and Analysis Format

Each turn can contain only one test or analysis tag.

- Single-point concept ablation (e.g., test load index after ablating concept 5):
<query_remove>5</query_remove>

- Baseline test (test original graph's load index, empty content):
<query_baseline></query_baseline>

When submitting the final analysis, include two parts:
1. rule: Your deduced decision rule (describe in natural language how to determine cornerstone concepts based on the cognitive load index)
2. cut_vertices: List of all cornerstone concept IDs (comma-separated; use "none" if there are no cornerstone concepts)

Format:
<answer>rule=A concept is a cornerstone concept if its ablation index is greater than baseline, cut_vertices=1,3,5</answer>

Or when there are no cornerstone concepts:
<answer>rule=A concept is a cornerstone concept if its ablation index is greater than baseline, cut_vertices=none</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用智能电网拓扑脆弱性排查系统。你的任务是找出所有会导致电网解列的关键变电站。

系统设定了一个固定但不可见的输电拓扑网 G，包含编号从 1 到 {n} 的变电站节点，线路连接情况对你隐藏。同时，存在一个固定但未知的电网监测函数 F，它将当前处于物理隔离状态的独立供电孤岛数量映射为一个整数型的系统稳定性读数。F 的内部测算算法对你隐藏，但它在整个排查过程中保持不变、确定且一致。

你的目标是：
1. 通过有限次断电隔离演练，归纳出一个通用的判定规则 R，能够根据系统稳定性读数判定隔离某个变电站是否会导致整个输电网解列成更多的供电孤岛（即判定该变电站是否为关键变电站）。
2. 根据你的规则，列出拓扑网中所有关键变电站的完整编号清单。

你可以进行以下两种类型的演练：

1. 单点隔离演练：指定一个变电站 v（1 到 {n} 之间的整数），系统会返回将该变电站断电隔离后的系统稳定性读数。对同一变电站的重复隔离会返回相同结果。

2. 基线读取（最多使用一次）：不隔离任何变电站，系统返回原电网的系统稳定性读数。这可以帮助你建立参考基准。

注意：
- 你最多可以进行 {max_queries} 次演练（基线读取也计入次数）。
- 在提交最终排查报告前，你必须至少完成 3 次有效演练。
- 不得直接询问线路的存在性、电力可达性或要求解释 F 的测算算法。
- 拓扑网 G 和函数 F 在整个排查过程中不会改变，所有返回值都是确定的。

## 演练与提交报告的格式

每次只能包含一个演练或报告标签。

- 单点隔离演练（例如读取隔离变电站 5 后的稳定性读数）：
<query_remove>5</query_remove>

- 基线读取（读取原电网的稳定性读数，内容为空）：
<query_baseline></query_baseline>

提交最终报告时，需要包含两部分：
1. rule: 你归纳出的判定规则（用自然语言描述如何根据稳定性读数判定关键变电站）
2. cut_vertices: 所有关键变电站的编号列表（用逗号隔开，若无关键变电站则填写"无"或"none"）

格式如下：
<answer>rule=若隔离变电站后的稳定性读数大于基线值则为关键变电站, cut_vertices=1,3,5</answer>

或者当没有关键变电站时：
<answer>rule=若隔离变电站后的稳定性读数大于基线值则为关键变电站, cut_vertices=无</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the Smart Grid Topological Vulnerability Inspection System. Your task is to identify all critical substations that could cause grid islanding.

The system features a fixed but invisible transmission topology network G, with substation nodes numbered from 1 to {n}. The line connections are hidden from you. Additionally, there exists a fixed but unknown grid monitoring function F that maps the number of physically isolated power islands to an integer system stability reading. The internal calculation algorithm of F is hidden from you, but it remains constant, deterministic, and consistent throughout the inspection.

Your goals are:
1. Through a limited number of blackout isolation drills, deduce a general decision rule R that can determine whether isolating a substation fragments the entire transmission grid into more power islands (i.e., whether the substation is a critical substation) based on the system stability reading.
2. Based on your rule, list the complete set of all critical substation IDs in the network.

You can perform the following two types of drills:

1. Single-point isolation drill: Specify a substation v (an integer between 1 and {n}), and the system will return the system stability reading after powering down and isolating that substation. Repeated isolations for the same substation will return the same result.

2. Baseline reading (can be used at most once): Without isolating any substation, the system returns the system stability reading of the original grid. This can help you establish a reference baseline.

Notes:
- You can perform at most {max_queries} drills (baseline reading also counts).
- Before submitting your final inspection report, you must complete at least 3 valid drills.
- You cannot directly ask about line existence, power reachability, or request an explanation of F's calculation algorithm.
- Topology network G and function F will not change throughout the inspection, and all return values are deterministic.

## Drill and Report Format

Each turn can contain only one drill or report tag.

- Single-point isolation drill (e.g., read stability after isolating substation 5):
<query_remove>5</query_remove>

- Baseline reading (read original grid stability, empty content):
<query_baseline></query_baseline>

When submitting the final report, include two parts:
1. rule: Your deduced decision rule (describe in natural language how to determine critical substations based on the stability reading)
2. cut_vertices: List of all critical substation IDs (comma-separated; use "none" if there are no critical substations)

Format:
<answer>rule=A substation is critical if its isolation stability reading is greater than baseline, cut_vertices=1,3,5</answer>

Or when there are no critical substations:
<answer>rule=A substation is critical if its isolation stability reading is greater than baseline, cut_vertices=none</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎进入法理逻辑审查与溯源系统。我们需要甄别出法典中维系法律体系不被割裂的核心条款。

系统设定了一个固定但不可见的法理依赖网络 G，包含编号从 1 到 {n} 的法律条款，条款间的引用和逻辑支撑关系对你隐藏。同时，存在一个固定但未知的法理评估函数 F，它将当前法律体系中缺乏逻辑联系的独立法理派系数量映射为一个整数型的体系一致性指数。F 的法理测算逻辑对你隐藏，但它在整个审查过程中保持不变、确定且一致。

你的目标是：
1. 通过有限次条款废止模拟，归纳出一个通用的判定规则 R，能够根据体系一致性指数判定废止某个条款是否会导致法律体系断裂成更多的独立法理派系（即判定该条款是否为核心条款）。
2. 根据你的规则，列出依赖网络中所有核心条款的完整编号清单。

你可以进行以下两种类型的模拟：

1. 单点条款废止：指定一个法律条款 v（1 到 {n} 之间的整数），系统会返回在虚拟法典中废止该条款后的体系一致性指数。对同一条款的重复废止会返回相同结果。

2. 基线审查（最多使用一次）：不废止任何条款，系统返回原法律体系的一致性指数。这可以帮助你建立参考基准。

注意：
- 你最多可以进行 {max_queries} 次模拟（基线审查也计入次数）。
- 在提交最终判决书前，你必须至少完成 3 次有效模拟。
- 不得直接询问引用关系的存在性、逻辑推演的可达性或要求解释 F 的法理测算逻辑。
- 法理依赖网络 G 和函数 F 在整个审查过程中不会改变，所有返回值都是确定的。

## 模拟与提交判决书的格式

每次只能包含一个模拟或判决标签。

- 单点条款废止（例如审查废止条款 5 后的一致性指数）：
<query_remove>5</query_remove>

- 基线审查（审查原法律体系的一致性指数，内容为空）：
<query_baseline></query_baseline>

提交最终判决书时，需要包含两部分：
1. rule: 你归纳出的判定规则（用自然语言描述如何根据一致性指数判定核心条款）
2. cut_vertices: 所有核心条款的编号列表（用逗号隔开，若无核心条款则填写"无"或"none"）

格式如下：
<answer>rule=若废止条款后的一致性指数大于基线值则为核心条款, cut_vertices=1,3,5</answer>

或者当没有核心条款时：
<answer>rule=若废止条款后的一致性指数大于基线值则为核心条款, cut_vertices=无</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Jurisprudential Logic Review and Traceability System. We need to identify the core clauses in the legal code that prevent the legal system from being fragmented.

The system features a fixed but invisible jurisprudential dependency network G, with legal clauses numbered from 1 to {n}. The citations and logical support relationships between clauses are hidden from you. Additionally, there exists a fixed but unknown jurisprudential evaluation function F that maps the number of logically disconnected, independent jurisprudential factions to an integer systemic consistency index. The specific logic of F is hidden from you, but it remains constant, deterministic, and consistent throughout the review.

Your goals are:
1. Through a limited number of clause abrogation simulations, deduce a general decision rule R that can determine whether abrogating a clause fractures the legal system into more independent factions (i.e., whether the clause is a core clause) based on the systemic consistency index.
2. Based on your rule, list the complete set of all core clause IDs in the dependency network.

You can perform the following two types of simulations:

1. Single-point clause abrogation: Specify a legal clause v (an integer between 1 and {n}), and the system will return the systemic consistency index after abrogating that clause in the virtual code. Repeated abrogations for the same clause will return the same result.

2. Baseline review (can be used at most once): Without abrogating any clause, the system returns the systemic consistency index of the original legal system. This can help you establish a reference baseline.

Notes:
- You can perform at most {max_queries} simulations (baseline review also counts).
- Before submitting your final ruling, you must complete at least 3 valid simulations.
- You cannot directly ask about the existence of citations, logical reachability, or request an explanation of F's calculation logic.
- Jurisprudential dependency network G and function F will not change throughout the review, and all return values are deterministic.

## Simulation and Ruling Format

Each turn can contain only one simulation or ruling tag.

- Single-point clause abrogation (e.g., review index after abrogating clause 5):
<query_remove>5</query_remove>

- Baseline review (review original legal system index, empty content):
<query_baseline></query_baseline>

When submitting the final ruling, include two parts:
1. rule: Your deduced decision rule (describe in natural language how to determine core clauses based on the consistency index)
2. cut_vertices: List of all core clause IDs (comma-separated; use "none" if there are no core clauses)

Format:
<answer>rule=A clause is a core clause if its abrogation index is greater than baseline, cut_vertices=1,3,5</answer>

Or when there are no core clauses:
<answer>rule=A clause is a core clause if its abrogation index is greater than baseline, cut_vertices=none</answer>
"""

    tags = ["answer", "query_remove", "query_baseline"]

    # 难度配置说明：
    # 1 (简单)      - N=6, 简单链状图，F(x)=x，明显割点
    # 2 (中等偏下)  - N=7, 星形图，F(x)=2*x，中心为唯一割点
    # 3 (中等偏上)  - N=8, 双环连接，F(x)=x+5，桥接点为割点
    # 4 (较难)      - N=10, 复杂连通图，F(x)=3*x-2，多个割点
    # 5 (难)        - N=12, 高度连通图，F(x)=x*x，少量关键割点

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,6)],  # 链状图: 1-2-3-4-5-6
                "f_type": "linear",
                "f_params": {"a": 1, "b": 0},  # F(x) = x
                "max_queries": 9,
            },
            2: {
                "n": 7,
                "edges": [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7)],  # 星形图，1为中心
                "f_type": "linear",
                "f_params": {"a": 2, "b": 0},  # F(x) = 2*x
                "max_queries": 10,
            },
            3: {
                "n": 8,
                "edges": [(1,2), (2,3), (3,1), (3,4), (4,5), (5,6), (6,7), (7,8), (8,5)],
                "f_type": "linear",
                "f_params": {"a": 1, "b": 5},  # F(x) = x + 5
                "max_queries": 11,
            },
            4: {
                "n": 10,
                "edges": [(1,2), (2,3), (3,4), (4,5), (1,6), (6,7), (7,8), (8,9), (9,10), (5,10), (2,6)],
                "f_type": "linear",
                "f_params": {"a": 3, "b": -2},  # F(x) = 3*x - 2
                "max_queries": 13,
            },
            5: {
                "n": 12,
                "edges": [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4), (4,5), (5,6), (5,7), 
                          (6,7), (7,8), (8,9), (8,10), (9,10), (10,11), (10,12), (11,12)],
                "f_type": "quadratic",
                "f_params": {"a": 1, "b": 0, "c": 0},  # F(x) = x*x
                "max_queries": 15,
            },
        },
        "en": {
            1: {
                "n": 6,
                "edges": [(1,2), (2,3), (3,4), (4,5), (5,6)],
                "f_type": "linear",
                "f_params": {"a": 1, "b": 0},
                "max_queries": 9,
            },
            2: {
                "n": 7,
                "edges": [(1,2), (1,3), (1,4), (1,5), (1,6), (1,7)],
                "f_type": "linear",
                "f_params": {"a": 2, "b": 0},
                "max_queries": 10,
            },
            3: {
                "n": 8,
                "edges": [(1,2), (2,3), (3,1), (3,4), (4,5), (5,6), (6,7), (7,8), (8,5)],
                "f_type": "linear",
                "f_params": {"a": 1, "b": 5},
                "max_queries": 11,
            },
            4: {
                "n": 10,
                "edges": [(1,2), (2,3), (3,4), (4,5), (1,6), (6,7), (7,8), (8,9), (9,10), (5,10), (2,6)],
                "f_type": "linear",
                "f_params": {"a": 3, "b": -2},
                "max_queries": 13,
            },
            5: {
                "n": 12,
                "edges": [(1,2), (1,3), (1,4), (2,3), (2,4), (3,4), (4,5), (5,6), (5,7), 
                          (6,7), (7,8), (8,9), (8,10), (9,10), (10,11), (10,12), (11,12)],
                "f_type": "quadratic",
                "f_params": {"a": 1, "b": 0, "c": 0},
                "max_queries": 15,
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
        self._game_info["n"] = cfg["n"]
        self._game_info["max_queries"] = cfg["max_queries"]
        
        # 构建图的邻接表
        self.n = cfg["n"]
        self.max_queries = cfg["max_queries"]
        self.edges = cfg["edges"]
        self.adj = {i: set() for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].add(v)
            self.adj[v].add(u)
        
        # 设置函数 F
        self.f_type = cfg["f_type"]
        self.f_params = cfg["f_params"]
        
        # 计算真实割点集合
        self.true_cut_vertices = self._find_cut_vertices()
        
        # 计算原图的连通分量数
        self.original_cc = self._count_components(set())
        
        # 查询计数
        self.query_count = 0
        self.baseline_queried = False
        self.queries_made = []

    def _apply_function(self, cc_count: int) -> int:
        """应用函数 F 到连通分量数"""
        if self.f_type == "linear":
            a = self.f_params["a"]
            b = self.f_params["b"]
            return a * cc_count + b
        elif self.f_type == "quadratic":
            a = self.f_params["a"]
            b = self.f_params.get("b", 0)
            c = self.f_params.get("c", 0)
            return a * cc_count * cc_count + b * cc_count + c
        else:
            raise ValueError(f"Unknown function type: {self.f_type}")

    def _count_components(self, removed_vertices: Set[int]) -> int:
        """计算删除指定顶点后的连通分量数"""
        visited = set()
        active_vertices = set(range(1, self.n + 1)) - removed_vertices
        component_count = 0
        
        for start in active_vertices:
            if start in visited:
                continue
            # BFS
            component_count += 1
            queue = [start]
            visited.add(start)
            while queue:
                u = queue.pop(0)
                for v in self.adj[u]:
                    if v not in removed_vertices and v not in visited:
                        visited.add(v)
                        queue.append(v)
        
        return component_count

    def _find_cut_vertices(self) -> Set[int]:
        """使用 Tarjan 算法找出所有割点"""
        cut_vertices = set()
        visited = set()
        disc = {}
        low = {}
        parent = {}
        time_counter = [0]
        
        def dfs(u):
            children = 0
            visited.add(u)
            disc[u] = low[u] = time_counter[0]
            time_counter[0] += 1
            
            for v in self.adj[u]:
                if v not in visited:
                    children += 1
                    parent[v] = u
                    dfs(v)
                    low[u] = min(low[u], low[v])
                    
                    # u 是割点的条件
                    if parent.get(u) is None and children > 1:
                        cut_vertices.add(u)
                    if parent.get(u) is not None and low[v] >= disc[u]:
                        cut_vertices.add(u)
                elif v != parent.get(u):
                    low[u] = min(low[u], disc[v])
        
        for vertex in range(1, self.n + 1):
            if vertex not in visited:
                parent[vertex] = None
                dfs(vertex)
        
        return cut_vertices

    def evaluate(self, parsed_info):
        """评估最终答案"""
        if self.query_count < 3:
            return False
        
        raw_ans = parsed_info["answer"]
        
        try:
            # 使用最后出现的 cut_vertices= 来分割
            # 先找 cut_vertices 的位置
            vertices_match = re.search(r'cut_vertices\s*=\s*(.+?)(?:\s*$)', raw_ans, re.IGNORECASE | re.DOTALL)
            rule_match = re.search(r'rule\s*=\s*(.+?)(?:,\s*cut_vertices\s*=)', raw_ans, re.IGNORECASE | re.DOTALL)
            
            if not vertices_match:
                return False
            
            # rule 不参与评判，只要求 cut_vertices 正确
            vertices_str = vertices_match.group(1).strip().rstrip('.,;!。，；')
            
            # 解析割点列表
            if vertices_str.lower() in ["无", "none", "null", ""]:
                model_cut_vertices = set()
            else:
                model_cut_vertices = set()
                for v in vertices_str.split(","):
                    v = v.strip().rstrip('.,;!。，；')
                    if v and v.isdigit():
                        model_cut_vertices.add(int(v))
            
            # 检查割点集合是否完全一致
            return model_cut_vertices == self.true_cut_vertices
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        """根据查询生成响应"""
        # 检查查询次数限制
        if self.query_count >= self.max_queries:
            if self.config.language == "zh":
                return f"已达到最大查询次数限制 {self.max_queries}，请直接提交你的最终答案。"
            else:
                return f"Maximum query limit of {self.max_queries} reached. Please submit your final answer now."
        
        # 处理基线查询
        if "query_baseline" in parsed_info:
            if self.baseline_queried:
                if self.config.language == "zh":
                    return "错误：基线查询只能使用一次。"
                else:
                    return "Error: Baseline query can only be used once."
            
            self.baseline_queried = True
            self.query_count += 1
            self.queries_made.append(("baseline", None))
            feedback = self._apply_function(self.original_cc)
            return str(feedback)
        
        # 处理单点删除查询
        elif "query_remove" in parsed_info:
            try:
                vertex_str = parsed_info["query_remove"].strip()
                vertex = int(vertex_str)
                
                if vertex < 1 or vertex > self.n:
                    if self.config.language == "zh":
                        return f"错误：顶点编号必须在 1 到 {self.n} 之间。"
                    else:
                        return f"Error: Vertex ID must be between 1 and {self.n}."
                
                self.query_count += 1
                self.queries_made.append(("remove", vertex))
                
                # 计算删除该顶点后的连通分量数
                cc_after_removal = self._count_components({vertex})
                feedback = self._apply_function(cc_after_removal)
                return str(feedback)
                
            except ValueError:
                if self.config.language == "zh":
                    return "错误：顶点编号必须是整数。"
                else:
                    return "Error: Vertex ID must be an integer."
        
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        possible_queries = []
        
        # 1. 基线查询
        baseline_feedback = self._apply_function(self.original_cc)
        possible_queries.append({
            "query": "<query_baseline></query_baseline>",
            "answer": str(baseline_feedback)
        })
        
        # 2. 单点删除查询 (枚举所有顶点)
        for v in range(1, self.n + 1):
            # 复用内部逻辑计算，避免副作用
            cc_after_removal = self._count_components({v})
            feedback = self._apply_function(cc_after_removal)
            
            possible_queries.append({
                "query": f"<query_remove>{v}</query_remove>",
                "answer": str(feedback)
            })
            
        return possible_queries

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        # 检查是否为纯整数（支持负数）
        if correct.isdigit() or (correct.startswith('-') and correct[1:].isdigit()):
            return str(int(correct) + 1)
        
        # 关键词替换
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                # 简单的大小写保持替换
                return re.sub(r'yes', 'no', correct, flags=re.IGNORECASE)
            elif "no" in lower_correct:
                return re.sub(r'no', 'yes', correct, flags=re.IGNORECASE)
        
        # 默认追加 _WRONG
        return correct + "_WRONG"