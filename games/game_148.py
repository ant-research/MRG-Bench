from .base import Game
import re

class TreePathReasoningGame(Game):

    game_rule_zh = """\
我们来玩一个"树路径推理"游戏，规则如下：

游戏设定了一棵有根树，每个节点有一个基础数值 v（整数）和一个二值标签 t（L1 或 L0）。树的结构、节点属性已完全确定，你可以随时查询。

树中有若干条从根到叶的路径。我已秘密选择了一个评分函数（共有四种可能），该函数会对任意一条路径计算出一个整数得分。你的目标是：
1. 推断出我使用的是哪个评分函数
2. 找出在该评分函数下得分最高的路径
3. 给出该路径的总得分

每次只能执行一个操作，使用以下 XML 格式：

1. 探测路径得分（例如探测路径 1）：
<probe>1</probe>

我会返回该路径在隐藏评分函数下的得分，格式为：YIELD x（x 为整数）。同时会告知你已使用的探测次数。

2. 列出所有路径：
<list_paths></list_paths>

我会列出所有可选路径及其节点序列。

3. 列出所有节点信息：
<list_nodes></list_nodes>

我会列出所有节点的标识、基础数值 v 和标签 t。

- 你必须至少进行 2 次探测才能提交最终答案
- 最多只能进行 5 次探测
- 请在有限的探测次数内，通过分析结果推断评分函数

当你准备好提交答案时，使用以下格式：

<answer>
FILTER=函数编号
PATH=路径编号
TOTAL=总得分
REASONING=你的推理过程，必须引用至少两次探测结果说明如何排除其他函数并确定当前函数
</answer>

注意：
- FILTER 应为 F1、F2、F3 或 F4 之一
- PATH 应为有效的路径编号
- TOTAL 应为该路径在该函数下的得分（整数）
- REASONING 必须引用至少两次 PROBE 结果进行论证

- 探测次数少于 2 次就提交答案
- 探测次数超过 5 次
- 判定的评分函数错误
- 选择的最优路径错误
- 报告的总得分不匹配
- 推理论证中未引用至少两次探测结果
"""

    game_rule_en = """\
Let's play a "Tree Path Reasoning" game with the following rules:

The game features a rooted tree where each node has a base value v (integer) and a binary label t (L1 or L0). The tree structure and node properties are fully determined and can be queried at any time.

The tree contains several root-to-leaf paths. I have secretly selected one scoring function (out of four possibilities) that computes an integer score for any given path. Your goals are:
1. Deduce which scoring function I am using
2. Find the path with the highest score under that function
3. Provide the total score of that path

You can perform one operation at a time using the following XML format:

1. Probe a path score (e.g., probe path 1):
<probe>1</probe>

I will return the score of that path under the hidden scoring function as: YIELD x (x is an integer). I will also inform you of the number of probes used.

2. List all paths:
<list_paths></list_paths>

I will list all available paths and their node sequences.

3. List all node information:
<list_nodes></list_nodes>

I will list all nodes with their identifiers, base values v, and labels t.

- You must perform at least 2 probes before submitting your final answer
- You can perform at most 5 probes
- Use the limited probes wisely to deduce the scoring function through analysis

When ready to submit your answer, use the following format:

<answer>
FILTER=function_id
PATH=path_number
TOTAL=total_score
REASONING=Your reasoning process, must reference at least two probe results to explain how you eliminated other functions and determined the current one
</answer>

Note:
- FILTER should be one of F1, F2, F3, or F4
- PATH should be a valid path number
- TOTAL should be the score of that path under that function (integer)
- REASONING must reference at least two PROBE results for justification

- Submitting answer with fewer than 2 probes
- Exceeding 5 probes
- Incorrect scoring function identification
- Incorrect optimal path selection
- Mismatched total score
- Reasoning does not reference at least two probe results
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市智能路网调度系统”。我们来进行路网路径规划的推理测试，规则如下：

系统设定了一个呈树状结构的城市路网，每个路口（节点）具有一个基础通行时间 v（整数）和一个道路类型标签 t（L1 表示高频拥堵的主干道，L0 表示普通支路）。路网的拓扑结构和路口属性已完全确定，你可以随时查询。

路网中有若干条从起点到终点的通行路线（路径）。我已秘密采用了一种路况评估模型（共有四种可能的函数），该模型会对任意一条路线计算出一个总拥堵指数（整数得分）。你的目标是：
1. 推断出我使用的是哪个路况评估模型（函数）
2. 找出在该评估模型下拥堵指数（得分）最高的路线
3. 给出该路线的总拥堵指数（总得分）

每次只能执行一个操作，使用以下 XML 格式：

1. 探测路线拥堵指数（例如探测路线 1）：
<probe>1</probe>

我会返回该路线在隐藏评估模型下的指数，格式为：YIELD x（x 为整数）。同时会告知你已使用的探测次数。

2. 列出所有通行路线：
<list_paths></list_paths>

我会列出所有可选路线及其途经的路口序列。

3. 列出所有路口（节点）信息：
<list_nodes></list_nodes>

我会列出所有路口的标识、基础通行时间 v 和道路类型标签 t。

- 你必须至少进行 2 次实地探测（probe）才能提交最终评估报告
- 最多只能进行 5 次探测
- 请在有限的测试次数内，通过分析路况指数推断出评估模型

当你准备好提交分析报告时，使用以下格式：

<answer>
FILTER=模型编号
PATH=路线编号
TOTAL=总拥堵指数
REASONING=你的推理过程，必须引用至少两次实地探测结果说明如何排除其他模型并确定当前模型
</answer>

注意：
- FILTER 应为 F1、F2、F3 或 F4 之一
- PATH 应为有效的路线编号
- TOTAL 应为该路线在该模型下的拥堵指数（整数）
- REASONING 必须引用至少两次 PROBE 结果进行论证

- 探测次数少于 2 次就提交报告
- 探测次数超过 5 次
- 判定的评估模型错误
- 选择的最高指数路线错误
- 报告的总拥堵指数不匹配
- 推理论证中未引用至少两次探测结果
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Intelligent Traffic Routing System". Let's play a route planning reasoning test with the following rules:

The system features a tree-structured urban road network where each intersection (node) has a base transit time v (integer) and a road type label t (L1 for high-traffic arterial road, or L0 for standard branch road). The network structure and intersection properties are fully determined and can be queried at any time.

The network contains several root-to-destination routes (paths). I have secretly selected one traffic evaluation model (out of four possibilities) that computes a total congestion index (integer score) for any given route. Your goals are:
1. Deduce which evaluation model I am using
2. Find the route with the highest congestion index under that model
3. Provide the total congestion index of that route

You can perform one operation at a time using the following XML format:

1. Probe a route's congestion index (e.g., probe route 1):
<probe>1</probe>

I will return the index of that route under the hidden evaluation model as: YIELD x (x is an integer). I will also inform you of the number of probes used.

2. List all available routes:
<list_paths></list_paths>

I will list all available routes and their intersection sequences.

3. List all intersection (node) information:
<list_nodes></list_nodes>

I will list all intersections with their identifiers, base transit times v, and road type labels t.

- You must perform at least 2 field probes before submitting your final report
- You can perform at most 5 probes
- Use the limited test probes wisely to deduce the evaluation model through analysis

When ready to submit your analysis report, use the following format:

<answer>
FILTER=model_id
PATH=route_number
TOTAL=total_congestion_index
REASONING=Your reasoning process, must reference at least two probe results to explain how you eliminated other models and determined the current one
</answer>

Note:
- FILTER should be one of F1, F2, F3, or F4
- PATH should be a valid route number
- TOTAL should be the congestion index of that route under that model (integer)
- REASONING must reference at least two PROBE results for justification

- Submitting report with fewer than 2 probes
- Exceeding 5 probes
- Incorrect evaluation model identification
- Incorrect optimal route selection
- Mismatched total congestion index
- Reasoning does not reference at least two probe results
"""

    contextualized_rule_zh_2 = """\
欢迎使用“临床诊疗决策分析系统”。我们来进行诊疗路径推理测试，规则如下：

系统具有一棵诊疗步骤树，每个干预步骤（节点）有一个基础风险值 v（整数）和一个指征标签 t（L1 代表侵入性操作，L0 代表非侵入性操作）。树的结构、节点属性已完全确定，你可以随时查询。

树中有若干条从初诊到终末干预的诊疗方案（路径）。我已秘密选择了一个并发症风险预测模型（共有四种可能），该模型会对任意一条诊疗方案计算出一个综合风险指数（整数得分）。你的目标是：
1. 推断出我使用的是哪个预测模型（函数）
2. 找出在该预测模型下风险指数最高（得分最高）的诊疗路径
3. 给出该路径的总风险指数（总得分）

每次只能执行一个操作，使用以下 XML 格式：

1. 探测诊疗路径风险指数（例如探测路径 1）：
<probe>1</probe>

我会返回该路径在隐藏预测模型下的风险指数，格式为：YIELD x（x 为整数）。同时会告知你已使用的探测次数。

2. 列出所有诊疗路径：
<list_paths></list_paths>

我会列出所有可选路径及其干预步骤序列。

3. 列出所有干预步骤（节点）信息：
<list_nodes></list_nodes>

我会列出所有干预步骤的标识、基础风险值 v 和指征标签 t。

- 你必须至少进行 2 次临床模拟探测才能提交最终诊断分析
- 最多只能进行 5 次探测
- 请在有限的探测次数内，通过分析风险指数推断预测模型

当你准备好提交诊断分析时，使用以下格式：

<answer>
FILTER=模型编号
PATH=路径编号
TOTAL=总风险指数
REASONING=你的推理过程，必须引用至少两次模拟探测结果说明如何排除其他模型并确定当前模型
</answer>

注意：
- FILTER 应为 F1、F2、F3 或 F4 之一
- PATH 应为有效的路径编号
- TOTAL 应为该路径在该模型下的风险指数（整数）
- REASONING 必须引用至少两次 PROBE 结果进行论证

- 探测次数少于 2 次就提交答案
- 探测次数超过 5 次
- 判定的预测模型错误
- 选择的最高风险路径错误
- 报告的总风险指数不匹配
- 推理论证中未引用至少两次探测结果
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Diagnostic Decision Analysis System". Let's play a diagnostic pathway reasoning test with the following rules:

The system features a clinical decision tree where each intervention step (node) has a base risk index v (integer) and an intervention type label t (L1 for invasive procedures, or L0 for non-invasive procedures). The tree structure and step properties are fully determined and can be queried at any time.

The tree contains several root-to-terminal diagnostic pathways (paths). I have secretly selected one complication risk prediction model (out of four possibilities) that computes a comprehensive risk score (integer score) for any given pathway. Your goals are:
1. Deduce which prediction model I am using
2. Find the pathway with the highest risk score under that model
3. Provide the total risk score of that pathway

You can perform one operation at a time using the following XML format:

1. Probe a pathway's risk score (e.g., probe pathway 1):
<probe>1</probe>

I will return the score of that pathway under the hidden prediction model as: YIELD x (x is an integer). I will also inform you of the number of probes used.

2. List all available pathways:
<list_paths></list_paths>

I will list all available pathways and their intervention sequences.

3. List all intervention step (node) information:
<list_nodes></list_nodes>

I will list all steps with their identifiers, base risk indices v, and intervention labels t.

- You must perform at least 2 clinical simulations (probes) before submitting your final analysis
- You can perform at most 5 probes
- Use the limited test probes wisely to deduce the prediction model through analysis

When ready to submit your diagnostic analysis, use the following format:

<answer>
FILTER=model_id
PATH=pathway_number
TOTAL=total_risk_score
REASONING=Your reasoning process, must reference at least two probe results to explain how you eliminated other models and determined the current one
</answer>

Note:
- FILTER should be one of F1, F2, F3, or F4
- PATH should be a valid pathway number
- TOTAL should be the risk score of that pathway under that model (integer)
- REASONING must reference at least two PROBE results for justification

- Submitting analysis with fewer than 2 probes
- Exceeding 5 probes
- Incorrect prediction model identification
- Incorrect optimal pathway selection
- Mismatched total risk score
- Reasoning does not reference at least two probe results
"""

    contextualized_rule_zh_3 = """\
欢迎使用“个性化学习路径评估系统”。我们来进行学习路线推理测试，规则如下：

系统构建了一棵知识点前置依赖树，每个学习模块（节点）有一个基础课时 v（整数）和一个考核类型标签 t（L1 代表核心必修，L0 代表拓展选修）。图谱结构和模块属性已完全确定，你可以随时查询。

树中有若干条从基础到高阶的学习路线（路径）。我已秘密选择了一个教学负荷评估模型（共有四种可能），该模型会对任意一条学习路线计算出一个总学分负荷（整数得分）。你的目标是：
1. 推断出我使用的是哪个评估模型（函数）
2. 找出在该评估模型下总学分负荷（得分）最高的学习路线
3. 给出该路线的总学分负荷（总得分）

每次只能执行一个操作，使用以下 XML 格式：

1. 探测学习路线学分负荷（例如探测路线 1）：
<probe>1</probe>

我会返回该路线在隐藏评估模型下的负荷，格式为：YIELD x（x 为整数）。同时会告知你已使用的探测次数。

2. 列出所有学习路线：
<list_paths></list_paths>

我会列出所有可选路线及其学习模块序列。

3. 列出所有学习模块（节点）信息：
<list_nodes></list_nodes>

我会列出所有模块的标识、基础课时 v 和考核类型标签 t。

- 你必须至少进行 2 次负荷测算探测才能提交最终评估方案
- 最多只能进行 5 次探测
- 请在有限的测试次数内，通过分析负荷数据推断评估模型

当你准备好提交评估方案时，使用以下格式：

<answer>
FILTER=模型编号
PATH=路线编号
TOTAL=总学分负荷
REASONING=你的推理过程，必须引用至少两次测算结果说明如何排除其他模型并确定当前模型
</answer>

注意：
- FILTER 应为 F1、F2、F3 或 F4 之一
- PATH 应为有效的路线编号
- TOTAL 应为该路线在该模型下的学分负荷（整数）
- REASONING 必须引用至少两次 PROBE 结果进行论证

- 探测次数少于 2 次就提交方案
- 探测次数超过 5 次
- 判定的评估模型错误
- 选择的最高负荷路线错误
- 报告的总学分负荷不匹配
- 推理论证中未引用至少两次探测结果
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Personalized Learning Path Evaluation System". Let's play a learning route reasoning test with the following rules:

The system features a prerequisite knowledge tree where each learning module (node) has base study hours v (integer) and a module type label t (L1 for core compulsory, or L0 for elective extension). The tree structure and module properties are fully determined and can be queried at any time.

The tree contains several root-to-advanced learning routes (paths). I have secretly selected one academic load evaluation model (out of four possibilities) that computes a total study load (integer score) for any given route. Your goals are:
1. Deduce which evaluation model I am using
2. Find the route with the highest study load under that model
3. Provide the total study load of that route

You can perform one operation at a time using the following XML format:

1. Probe a route's study load (e.g., probe route 1):
<probe>1</probe>

I will return the load of that route under the hidden evaluation model as: YIELD x (x is an integer). I will also inform you of the number of probes used.

2. List all learning routes:
<list_paths></list_paths>

I will list all available routes and their module sequences.

3. List all learning module (node) information:
<list_nodes></list_nodes>

I will list all modules with their identifiers, base study hours v, and module type labels t.

- You must perform at least 2 load measurement probes before submitting your final evaluation
- You can perform at most 5 probes
- Use the limited test probes wisely to deduce the evaluation model through analysis

When ready to submit your evaluation plan, use the following format:

<answer>
FILTER=model_id
PATH=route_number
TOTAL=total_study_load
REASONING=Your reasoning process, must reference at least two probe results to explain how you eliminated other models and determined the current one
</answer

Note:
- FILTER should be one of F1, F2, F3, or F4
- PATH should be a valid route number
- TOTAL should be the study load of that route under that model (integer)
- REASONING must reference at least two PROBE results for justification

- Submitting evaluation with fewer than 2 probes
- Exceeding 5 probes
- Incorrect evaluation model identification
- Incorrect optimal route selection
- Mismatched total study load
- Reasoning does not reference at least two probe results
"""

    contextualized_rule_zh_4 = """\
欢迎进入“数字孪生工业产线能效评估平台”。我们来进行工艺流程推理测试，规则如下：

系统的工艺流程呈现一棵树状拓扑，每个加工工序（节点）有一个基础能耗 v（整数）和一个工艺类型标签 t（L1 代表精密加工，L0 代表标准加工）。拓扑结构和工序属性已完全确定，你可以随时查询。

树中有若干条从原料到成品的工艺路线（路径）。我已秘密选择了一个数字孪生能效算法（共有四种可能），该算法会对任意一条工艺路线计算出一个总能耗数值（整数得分）。你的目标是：
1. 推断出我使用的是哪个能效算法（函数）
2. 找出在该能效算法下总能耗（得分）最高的工艺路线
3. 给出该路线的总能耗数值（总得分）

每次只能执行一个操作，使用以下 XML 格式：

1. 探测工艺路线能耗（例如探测路线 1）：
<probe>1</probe>

我会返回该路线在隐藏算法下的能耗数值，格式为：YIELD x（x 为整数）。同时会告知你已使用的探测次数。

2. 列出所有工艺路线：
<list_paths></list_paths>

我会列出所有可选路线及其加工工序序列。

3. 列出所有工序（节点）信息：
<list_nodes></list_nodes>

我会列出所有工序的标识、基础能耗 v 和工艺类型标签 t。

- 你必须至少进行 2 次仿真测算（probe）才能提交最终能效分析
- 最多只能进行 5 次探测
- 请在有限的仿真次数内，通过分析能耗数据推断算法

当你准备好提交分析报告时，使用以下格式：

<answer>
FILTER=算法编号
PATH=路线编号
TOTAL=总能耗数值
REASONING=你的推理过程，必须引用至少两次测算结果说明如何排除其他算法并确定当前算法
</answer>

注意：
- FILTER 应为 F1、F2、F3 或 F4 之一
- PATH 应为有效的路线编号
- TOTAL 应为该路线在该算法下的能耗数值（整数）
- REASONING 必须引用至少两次 PROBE 结果进行论证

- 探测次数少于 2 次就提交报告
- 探测次数超过 5 次
- 判定的能效算法错误
- 选择的最高能耗路线错误
- 报告的总能耗数值不匹配
- 推理论证中未引用至少两次探测结果
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Digital Twin Industrial Energy Efficiency Platform". Let's play a manufacturing process reasoning test with the following rules:

The manufacturing process forms a tree-structured topology where each processing stage (node) has a base energy consumption v (integer) and a process type label t (L1 for precision processing, or L0 for standard processing). The topology structure and stage properties are fully determined and can be queried at any time.

The tree contains several raw-to-finished process routes (paths). I have secretly selected one digital twin energy efficiency algorithm (out of four possibilities) that computes a total energy score (integer score) for any given route. Your goals are:
1. Deduce which efficiency algorithm I am using
2. Find the process route with the highest energy score under that algorithm
3. Provide the total energy score of that route

You can perform one operation at a time using the following XML format:

1. Probe a route's energy score (e.g., probe route 1):
<probe>1</probe>

I will return the energy score of that route under the hidden algorithm as: YIELD x (x is an integer). I will also inform you of the number of probes used.

2. List all process routes:
<list_paths></list_paths>

I will list all available routes and their processing sequences.

3. List all processing stage (node) information:
<list_nodes></list_nodes>

I will list all stages with their identifiers, base energy consumption v, and process type labels t.

- You must perform at least 2 simulation probes before submitting your final analysis
- You can perform at most 5 probes
- Use the limited test probes wisely to deduce the efficiency algorithm through analysis

When ready to submit your efficiency analysis, use the following format:

<answer>
FILTER=algorithm_id
PATH=route_number
TOTAL=total_energy_score
REASONING=Your reasoning process, must reference at least two probe results to explain how you eliminated other algorithms and determined the current one
</answer>

Note:
- FILTER should be one of F1, F2, F3, or F4
- PATH should be a valid route number
- TOTAL should be the energy score of that route under that algorithm (integer)
- REASONING must reference at least two PROBE results for justification

- Submitting analysis with fewer than 2 probes
- Exceeding 5 probes
- Incorrect efficiency algorithm identification
- Incorrect optimal route selection
- Mismatched total energy score
- Reasoning does not reference at least two probe results
"""

    contextualized_rule_zh_5 = """\
欢迎使用“AI诉讼策略推演专家系统”。我们来进行诉讼路径推理测试，规则如下：

案件的程序推进构成了一棵决策树，每个争议焦点或程序（节点）有一个基础耗时 v（整数）和一个判例支持度标签 t（L1 代表有明确先例，L0 代表无先例）。决策树结构和程序属性已完全确定，你可以随时查询。

树中有若干条从立案到判决的诉讼策略（路径）。我已秘密选择了一个案件推演评估模型（共有四种可能），该模型会对任意一条策略路径计算出一个综合诉讼阻力指数（整数得分）。你的目标是：
1. 推断出我使用的是哪个推演评估模型（函数）
2. 找出在该评估模型下诉讼阻力（得分）最高的策略路径
3. 给出该路径的总诉讼阻力指数（总得分）

每次只能执行一个操作，使用以下 XML 格式：

1. 探测策略阻力指数（例如探测路径 1）：
<probe>1</probe>

我会返回该策略在隐藏评估模型下的阻力指数，格式为：YIELD x（x 为整数）。同时会告知你已使用的探测次数。

2. 列出所有策略路径：
<list_paths></list_paths>

我会列出所有可选路径及其推进程序序列。

3. 列出所有程序（节点）信息：
<list_nodes></list_nodes>

我会列出所有节点的标识、基础耗时 v 和判例支持度标签 t。

- 你必须至少进行 2 次 AI 推演探测才能提交最终策略审查
- 最多只能进行 5 次探测
- 请在有限的推演次数内，通过分析阻力数据推断出评估模型

当你准备好提交策略审查时，使用以下格式：

<answer>
FILTER=模型编号
PATH=路径编号
TOTAL=总阻力指数
REASONING=你的推理过程，必须引用至少两次推演结果说明如何排除其他模型并确定当前模型
</answer>

注意：
- FILTER 应为 F1、F2、F3 或 F4 之一
- PATH 应为有效的路径编号
- TOTAL 应为该路径在该模型下的阻力指数（整数）
- REASONING 必须引用至少两次 PROBE 结果进行论证

- 探测次数少于 2 次就提交审查
- 探测次数超过 5 次
- 判定的评估模型错误
- 选择的最高阻力路径错误
- 报告的总阻力指数不匹配
- 推理论证中未引用至少两次探测结果
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "AI Litigation Strategy Simulation Expert System". Let's play a litigation pathway reasoning test with the following rules:

The case progression forms a decision tree where each legal issue or procedural step (node) has a base time cost v (integer) and a precedent support label t (L1 for precedent-supported, or L0 for novel/no precedent). The tree structure and step properties are fully determined and can be queried at any time.

The tree contains several filing-to-judgment litigation strategies (paths). I have secretly selected one case simulation evaluation model (out of four possibilities) that computes a comprehensive litigation resistance index (integer score) for any given strategy path. Your goals are:
1. Deduce which evaluation model I am using
2. Find the strategy path with the highest resistance index under that model
3. Provide the total resistance index of that path

You can perform one operation at a time using the following XML format:

1. Probe a strategy's resistance index (e.g., probe path 1):
<probe>1</probe>

I will return the resistance index of that path under the hidden evaluation model as: YIELD x (x is an integer). I will also inform you of the number of probes used.

2. List all strategy paths:
<list_paths></list_paths>

I will list all available strategy paths and their procedural sequences.

3. List all procedural step (node) information:
<list_nodes></list_nodes>

I will list all steps with their identifiers, base time costs v, and precedent support labels t.

- You must perform at least 2 AI simulation probes before submitting your final strategy review
- You can perform at most 5 probes
- Use the limited test probes wisely to deduce the evaluation model through analysis

When ready to submit your strategy review, use the following format:

<answer>
FILTER=model_id
PATH=path_number
TOTAL=total_resistance_index
REASONING=Your reasoning process, must reference at least two probe results to explain how you eliminated other models and determined the current one
</answer>

Note:
- FILTER should be one of F1, F2, F3, or F4
- PATH should be a valid path number
- TOTAL should be the resistance index of that path under that model (integer)
- REASONING must reference at least two PROBE results for justification

- Submitting review with fewer than 2 probes
- Exceeding 5 probes
- Incorrect evaluation model identification
- Incorrect optimal path selection
- Mismatched total resistance index
- Reasoning does not reference at least two probe results
"""

    tags = ["answer", "probe", "list_paths", "list_nodes"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        1: {
            "tree": {
                "R": {"v": 5, "t": "L1", "children": ["A", "B"]},
                "A": {"v": 2, "t": "L0", "children": []},
                "B": {"v": 3, "t": "L1", "children": ["C", "D"]},
                "C": {"v": 4, "t": "L0", "children": []},
                "D": {"v": 1, "t": "L1", "children": []},
            },
            "paths": [
                ["R", "A"],
                ["R", "B", "C"],
                ["R", "B", "D"],
            ],
            "filter": "F1",
            "best_path": 2,
        },
        2: {
            "tree": {
                "R": {"v": 3, "t": "L0", "children": ["A", "B"]},
                "A": {"v": 4, "t": "L1", "children": ["C", "D"]},
                "C": {"v": 2, "t": "L0", "children": []},
                "D": {"v": 5, "t": "L1", "children": []},
                "B": {"v": 6, "t": "L0", "children": ["E", "F"]},
                "E": {"v": 3, "t": "L1", "children": []},
                "F": {"v": 7, "t": "L0", "children": []},
            },
            "paths": [
                ["R", "A", "C"],
                ["R", "A", "D"],
                ["R", "B", "E"],
                ["R", "B", "F"],
            ],
            "filter": "F4",
            "best_path": 4,
        },
        3: {
            "tree": {
                "R": {"v": 4, "t": "L1", "children": ["A", "B", "C"]},
                "A": {"v": 3, "t": "L1", "children": ["D", "E"]},
                "D": {"v": 6, "t": "L0", "children": []},
                "E": {"v": 1, "t": "L1", "children": []},
                "B": {"v": 5, "t": "L0", "children": ["F", "G"]},
                "F": {"v": 4, "t": "L1", "children": []},
                "G": {"v": 7, "t": "L0", "children": []},
                "C": {"v": 2, "t": "L0", "children": ["H"]},
                "H": {"v": 8, "t": "L1", "children": []},
            },
            "paths": [
                ["R", "A", "D"],
                ["R", "A", "E"],
                ["R", "B", "F"],
                ["R", "B", "G"],
                ["R", "C", "H"],
            ],
            "filter": "F2",
            "best_path": 1,
        },
        4: {
            "tree": {
                "R": {"v": 2, "t": "L0", "children": ["A", "B", "C"]},
                "A": {"v": 5, "t": "L1", "children": ["D", "E"]},
                "D": {"v": 3, "t": "L0", "children": []},
                "E": {"v": 6, "t": "L1", "children": []},
                "B": {"v": 4, "t": "L0", "children": ["F", "G"]},
                "F": {"v": 7, "t": "L1", "children": []},
                "G": {"v": 2, "t": "L0", "children": []},
                "C": {"v": 8, "t": "L1", "children": ["H", "I"]},
                "H": {"v": 5, "t": "L0", "children": []},
                "I": {"v": 9, "t": "L1", "children": []},
            },
            "paths": [
                ["R", "A", "D"],
                ["R", "A", "E"],
                ["R", "B", "F"],
                ["R", "B", "G"],
                ["R", "C", "H"],
                ["R", "C", "I"],
            ],
            "filter": "F3",
            "best_path": 6,
        },
        5: {
            "tree": {
                "R": {"v": 6, "t": "L1", "children": ["A", "B", "C"]},
                "A": {"v": 7, "t": "L0", "children": ["D", "E"]},
                "D": {"v": 4, "t": "L1", "children": []},
                "E": {"v": 9, "t": "L0", "children": []},
                "B": {"v": 3, "t": "L1", "children": ["F", "G", "H"]},
                "F": {"v": 8, "t": "L0", "children": []},
                "G": {"v": 5, "t": "L1", "children": []},
                "H": {"v": 11, "t": "L0", "children": []},
                "C": {"v": 2, "t": "L0", "children": ["I", "J"]},
                "I": {"v": 10, "t": "L1", "children": []},
                "J": {"v": 6, "t": "L0", "children": []},
            },
            "paths": [
                ["R", "A", "D"],
                ["R", "A", "E"],
                ["R", "B", "F"],
                ["R", "B", "G"],
                ["R", "B", "H"],
                ["R", "C", "I"],
                ["R", "C", "J"],
            ],
            "filter": "F1",
            "best_path": 2,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        
        self.tree = cfg["tree"]
        self.paths = cfg["paths"]
        self.filter_type = cfg["filter"]
        self.best_path_idx = cfg["best_path"]
        
        self.probe_count = 0
        self.max_probes = 5
        self.min_probes = 2
        
        self._game_info = {}
        
        self._precompute_scores()

    def _precompute_scores(self):
        self.all_scores = {}
        for i, path in enumerate(self.paths, 1):
            self.all_scores[i] = {
                "F1": self._score_f1(path),
                "F2": self._score_f2(path),
                "F3": self._score_f3(path),
                "F4": self._score_f4(path),
            }

    def _score_f1(self, path):
        return sum(self.tree[node]["v"] for node in path)

    def _score_f2(self, path):
        score = self.tree[path[0]]["v"]
        for i in range(len(path) - 1):
            parent = path[i]
            child = path[i + 1]
            parent_tag = self.tree[parent]["t"]
            alpha = 2 if parent_tag == "L1" else 1
            score += self.tree[child]["v"] * alpha
        return score

    def _score_f3(self, path):
        score = self.tree[path[0]]["v"]
        for i in range(1, len(path)):
            child = path[i]
            child_tag = self.tree[child]["t"]
            beta = 2 if child_tag == "L1" else 1
            score += self.tree[child]["v"] * beta
        return score

    def _score_f4(self, path):
        base = sum(self.tree[node]["v"] for node in path)
        leaf = path[-1]
        return base + 2 * self.tree[leaf]["v"]

    def _format_paths_info(self):
        if self.config.language == "zh":
            result = "可选路径列表：\n"
            for i, path in enumerate(self.paths, 1):
                result += f"路径{i}: {' -> '.join(path)}\n"
        else:
            result = "Available paths:\n"
            for i, path in enumerate(self.paths, 1):
                result += f"Path {i}: {' -> '.join(path)}\n"
        return result.strip()

    def _format_nodes_info(self):
        if self.config.language == "zh":
            result = "所有节点信息：\n"
            for node_id, info in self.tree.items():
                children = info.get("children", [])
                is_leaf = "（叶节点）" if not children else ""
                result += f"节点{node_id}: v={info['v']}, t={info['t']}{is_leaf}\n"
        else:
            result = "All node information:\n"
            for node_id, info in self.tree.items():
                children = info.get("children", [])
                is_leaf = " (leaf)" if not children else ""
                result += f"Node {node_id}: v={info['v']}, t={info['t']}{is_leaf}\n"
        return result.strip()

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        ans_dict = {}
        lines = raw_ans.strip().split("\n")
        current_key = None
        current_value_lines = []
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                if current_key:
                    current_value_lines.append("")
                continue
            
            if "=" in line_stripped:
                k, v = line_stripped.split("=", 1)
                k_upper = k.strip().upper()
                if k_upper in ("FILTER", "PATH", "TOTAL", "REASONING"):
                    if current_key is not None:
                        ans_dict[current_key] = "\n".join(current_value_lines).strip()
                    current_key = k_upper
                    current_value_lines = [v.strip()]
                    continue
            
            if current_key is not None:
                current_value_lines.append(line_stripped)
        
        if current_key is not None:
            ans_dict[current_key] = "\n".join(current_value_lines).strip()
        
        required_fields = ["FILTER", "PATH", "TOTAL", "REASONING"]
        for f in required_fields:
            if f not in ans_dict:
                return False
        
        if self.probe_count < self.min_probes:
            return False
        
        if ans_dict["FILTER"] != self.filter_type:
            return False
        
        try:
            path_idx = int(ans_dict["PATH"])
            if path_idx != self.best_path_idx:
                return False
        except:
            return False
        
        try:
            total = int(ans_dict["TOTAL"])
            expected_total = self.all_scores[self.best_path_idx][self.filter_type]
            if total != expected_total:
                return False
        except:
            return False
        
        reasoning = ans_dict.get("REASONING", "")
        reasoning_upper = reasoning.upper()
        probe_refs = re.findall(
            r'PROBE\s*\d|探测\s*(?:路径\s*)?\d|PROBING\s+PATH\s*\d|PROBED\s+PATH\s*\d',
            reasoning_upper
        )
        if len(probe_refs) < 2:
            mention_count = reasoning_upper.count("PROBE") + reasoning.count("探测")
            if mention_count < 2:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_max = f"错误：已达到最大探测次数（{self.max_probes}次）。"
            error_invalid = "错误：无效的路径编号。"
        else:
            error_max = f"Error: Maximum probe limit ({self.max_probes}) reached."
            error_invalid = "Error: Invalid path number."
        
        if "probe" in parsed_info:
            if self.probe_count >= self.max_probes:
                raise ValueError("Exceeded maximum probe limit")
            
            try:
                path_idx = int(parsed_info["probe"].strip())
                if path_idx < 1 or path_idx > len(self.paths):
                    return error_invalid
                
                score = self.all_scores[path_idx][self.filter_type]
                self.probe_count += 1
                
                if self.config.language == "zh":
                    return f"YIELD {score}\n（已使用探测次数：{self.probe_count}/{self.max_probes}）"
                else:
                    return f"YIELD {score}\n(Probes used: {self.probe_count}/{self.max_probes})"
                    
            except ValueError:
                return error_invalid
        
        elif "list_paths" in parsed_info:
            return self._format_paths_info()
        
        elif "list_nodes" in parsed_info:
            return self._format_nodes_info()
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        m = re.search(r'YIELD\s+(-?\d+)', str(correct))
        if m:
            original_val = int(m.group(1))
            wrong_val = original_val + 3
            return correct.replace(f"YIELD {original_val}", f"YIELD {wrong_val}")
        
        if str(correct).strip().lstrip('-').isdigit():
            return str(int(correct) + 1)
        
        if "是" in str(correct):
            return str(correct).replace("是", "否")
        if "否" in str(correct):
            return str(correct).replace("否", "是")
            
        lower_correct = str(correct).lower()
        if "yes" in lower_correct:
            if "Yes" in correct: return correct.replace("Yes", "No")
            if "YES" in correct: return correct.replace("YES", "NO")
            return correct.replace("yes", "no")
        if "no" in lower_correct:
            if "No" in correct: return correct.replace("No", "Yes")
            if "NO" in correct: return correct.replace("NO", "YES")
            return correct.replace("no", "yes")

        return str(correct) + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []

        queries.append({
            "query": "<list_paths></list_paths>",
            "answer": self._format_paths_info()
        })

        queries.append({
            "query": "<list_nodes></list_nodes>",
            "answer": self._format_nodes_info()
        })

        probe_counter = 0
        for i in range(1, len(self.paths) + 1):
            if probe_counter >= self.max_probes:
                break
            score = self.all_scores[i][self.filter_type]
            probe_counter += 1

            if self.config.language == "zh":
                ans = f"YIELD {score}\n（已使用探测次数：{probe_counter}/{self.max_probes}）"
            else:
                ans = f"YIELD {score}\n(Probes used: {probe_counter}/{self.max_probes})"

            queries.append({
                "query": f"<probe>{i}</probe>",
                "answer": ans
            })
            
        return queries