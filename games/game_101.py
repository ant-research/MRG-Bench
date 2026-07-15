from .base import Game
import re

class TriangleRuleInferenceGame(Game):

    game_rule_zh = """\
我们现在来玩一个"三角形规则推断"游戏，规则如下：

游戏设定了一个公开且固定的无向简单图 G，包含 8 个顶点：A, B, C, D, E, F, G, H。

边集如下：
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

三角形定义：三个顶点两两相连构成的闭环（例如 ABC 因为存在边 AB、AC、BC 而构成三角形）。

游戏中存在以下未知信息：
1. 一个隐藏顶点 K，它是 A 到 H 中的某一个顶点。
2. 一个固定的规则函数 f，它将每个顶点映射到一个非负整数。该规则仅由图中与三角形相关的结构决定，并且与隐藏顶点 K 有关联。

你的目标是通过有限次数的查询，推断出：
1. 规则 f 的精确定义（必须用自然语言清晰描述 f 如何由三角形结构导出）
2. 隐藏顶点 K 的身份

你可以进行以下操作：

1. 观测查询：查询某个顶点 X 的读数值。我会返回该顶点对应的数值。
2. 预测校验：提交你对某个顶点 X 的读数预测值 n。我会告诉你是否正确，如果错误会给出正确值。此操作不消耗观测次数。
3. 最终提交：当你确定规则和隐藏顶点时，提交最终答案。

重要说明：
- 规则函数 f 是确定的、不变的，对同一顶点的多次查询结果一致。
- 你需要在尽可能少的观测查询次数内完成推断。
- 最终提交时，规则描述必须精确表述 f 如何计算。

每次只能包含一个操作标签：

- 观测查询（例如查询顶点 A）：
<query_observe>A</query_observe>

- 预测校验（例如预测顶点 B 的值为 5）：
<query_verify>B,5</query_verify>

- 最终提交（需同时提供规则描述和隐藏顶点）：
<answer>rule=包含隐藏顶点的三角形数量, hidden=D</answer>

注意：
- 观测查询会消耗查询次数
- 预测校验不消耗查询次数，但只会告知对错和正确值，不提供其他信息
- 最终提交的规则描述必须准确描述计算方法
"""

    game_rule_en = """\
Let's play a "Triangle Rule Inference" game. Here are the rules:

The game features a public and fixed undirected simple graph G with 8 vertices: A, B, C, D, E, F, G, H.

Edge set:
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

Triangle definition: A closed loop of three vertices that are pairwise connected (e.g., ABC forms a triangle because edges AB, AC, BC exist).

The game has the following unknown information:
1. A hidden vertex K, which is one of the vertices from A to H.
2. A fixed rule function f that maps each vertex to a non-negative integer. This rule is determined solely by triangle-related structures in the graph and is associated with the hidden vertex K.

Your goal is to infer through a limited number of queries:
1. The exact definition of rule f (must clearly describe in natural language how f is derived from triangle structures)
2. The identity of the hidden vertex K

You can perform the following operations:

1. Observation Query: Query the reading value of a vertex X. I will return the corresponding value.
2. Verification Query: Submit your predicted value n for a vertex X. I will tell you if it's correct, and provide the correct value if wrong. This operation does not consume observation counts.
3. Final Submission: When you've determined the rule and hidden vertex, submit your final answer.

Important notes:
- The rule function f is deterministic and invariant; querying the same vertex multiple times yields consistent results.
- You need to complete the inference with as few observation queries as possible.
- In the final submission, the rule description must precisely state how f is calculated.

Each operation must contain only one tag:

- Observation Query (e.g., querying vertex A):
<query_observe>A</query_observe>

- Verification Query (e.g., predicting vertex B has value 5):
<query_verify>B,5</query_verify>

- Final Submission (must provide both rule description and hidden vertex):
<answer>rule=number of triangles containing the hidden vertex, hidden=D</answer>

Note:
- Observation queries consume query counts
- Verification queries do not consume query counts, but only indicate correctness and provide the correct value
- The rule description in final submission must accurately describe the calculation method
"""

    contextualized_rule_zh_1 = """\
【交通场景】
我们现在来进行一场“交通网络枢纽排查”任务，规则如下：

系统设定了一个公开且固定的区域交通物流网络，包含 8 个物流枢纽（即网络中的顶点）：A, B, C, D, E, F, G, H。

直达航线（即边集）如下：
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

三枢纽互通圈（即网络拓扑中的“三角形”）：三个枢纽两两互通构成的闭环（例如 ABC 因为存在航线 AB、AC、BC 而构成一个三角形）。

系统中存在以下未知情况：
1. 一个核心故障枢纽（即隐藏顶点 K），它是 A 到 H 中的某一个枢纽。
2. 一个固定的物流负荷计算模型（即规则函数 f），它将每个枢纽映射到一个非负整数。该模型的负荷指数仅由网络中与三角形相关的结构决定，并且与隐藏顶点 K 有关联。

你的目标是通过有限次数的系统查询，推断出：
1. 负荷计算模型 f 的精确定义（必须用自然语言清晰描述 f 如何由三角形结构导出）
2. 核心故障枢纽（即隐藏顶点 K）的身份

你可以进行以下操作：
1. 观测查询：查询某个枢纽 X 的负荷读数值。我会返回该枢纽对应的数值。
2. 预测校验：提交你对某个枢纽 X 的读数预测值 n。我会告诉你是否正确，如果错误会给出正确值。此操作不消耗观测次数。
3. 最终提交：当你确定规则和隐藏顶点时，提交最终答案。

重要说明：
- 负荷计算模型 f 是确定的、不变的，对同一枢纽的多次查询结果一致。
- 你需要在尽可能少的观测查询次数内完成推断。
- 最终提交时，规则描述必须精确表述 f 如何计算。为了保证系统正确识别判定，请在最终描述中继续使用“隐藏顶点”和“三角形”这两个标准术语。

每次只能包含一个操作标签：

- 观测查询（例如查询枢纽 A）：
<query_observe>A</query_observe>

- 预测校验（例如预测枢纽 B 的值为 5）：
<query_verify>B,5</query_verify>

- 最终提交（需同时提供规则描述和隐藏顶点）：
<answer>rule=包含隐藏顶点的三角形数量, hidden=D</answer>

注意：
- 观测查询会消耗查询次数
- 预测校验不消耗查询次数，但只会告知对错和正确值，不提供其他信息
- 最终提交的规则描述必须准确描述计算方法
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's conduct a "Transportation Network Hub Investigation" task. Here are the rules:

The system features a public and fixed regional transportation logistics network with 8 logistics hubs (vertices): A, B, C, D, E, F, G, H.

Direct routes (edge set):
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

Three-hub interconnected loop (i.e., Triangle definition in network topology): A closed loop of three hubs that are pairwise connected (e.g., ABC forms a triangle because routes AB, AC, BC exist).

The system has the following unknown information:
1. A core faulty hub (i.e., hidden vertex K), which is one of the hubs from A to H.
2. A fixed logistics load calculation model (rule function f) that maps each hub to a non-negative integer. This model is determined solely by triangle-related structures in the network and is associated with the hidden vertex K.

Your goal is to infer through a limited number of system queries:
1. The exact definition of the load calculation model f (must clearly describe in natural language how f is derived from triangle structures)
2. The identity of the core faulty hub (hidden vertex K)

You can perform the following operations:

1. Observation Query: Query the load reading value of a hub X. I will return the corresponding value.
2. Verification Query: Submit your predicted value n for a hub X. I will tell you if it's correct, and provide the correct value if wrong. This operation does not consume observation counts.
3. Final Submission: When you've determined the rule and hidden vertex, submit your final answer.

Important notes:
- The calculation model f is deterministic and invariant; querying the same hub multiple times yields consistent results.
- You need to complete the inference with as few observation queries as possible.
- In the final submission, the rule description must precisely state how f is calculated. To ensure correct system recognition, please continue to use the standard terms "hidden vertex" and "triangle" in your description.

Each operation must contain only one tag:

- Observation Query (e.g., querying hub A):
<query_observe>A</query_observe>

- Verification Query (e.g., predicting hub B has value 5):
<query_verify>B,5</query_verify>

- Final Submission (must provide both rule description and hidden vertex):
<answer>rule=number of triangles containing the hidden vertex, hidden=D</answer>

Note:
- Observation queries consume query counts
- Verification queries do not consume query counts, but only indicate correctness and provide the correct value
- The rule description in final submission must accurately describe the calculation method
"""

    contextualized_rule_zh_2 = """\
【医疗场景】
我们现在来进行一项“蛋白质相互作用网络分析”任务，规则如下：

系统设定了一个公开且固定的蛋白质协同作用图谱，包含 8 个关键蛋白质分子（即网络中的顶点）：A, B, C, D, E, F, G, H。

协同反应关系（即边集）如下：
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

三元协同作用簇（即网络拓扑中的“三角形”）：三个蛋白质分子两两互相作用构成的闭环复合体（例如 ABC 因为存在作用关系 AB、AC、BC 而构成一个三角形）。

图谱中存在以下未知情况：
1. 一个核心致病靶蛋白（即隐藏顶点 K），它是 A 到 H 中的某一个蛋白质。
2. 一套固定的生物活性指数评估机制（即规则函数 f），它将每个蛋白质映射到一个非负整数活性值。该活性值仅由网络中与三角形相关的复合体结构决定，并且与隐藏顶点 K 有关联。

你的目标是通过有限次数的生化检验，推断出：
1. 活性评估机制 f 的精确定义（必须用自然语言清晰描述 f 如何由三角形结构导出）
2. 核心致病靶蛋白（即隐藏顶点 K）的身份

你可以进行以下操作：
1. 观测查询：检验某个蛋白质 X 的活性读数值。我会返回对应的数值。
2. 预测校验：提交你对某个蛋白质 X 的活性预测值 n。我会告诉你是否正确，如果错误会给出正确值。此操作不消耗观测次数。
3. 最终提交：当你确定规则和隐藏顶点时，提交最终诊断答案。

重要说明：
- 评估机制 f 是确定的、不变的，对同一蛋白质的多次检验结果一致。
- 你需要在尽可能少的检验次数内完成推断。
- 最终提交时，规则描述必须精确表述 f 如何计算。为了保证系统正确识别判定，请在最终描述中继续使用“隐藏顶点”和“三角形”这两个标准术语。

每次只能包含一个操作标签：

- 观测查询（例如检验蛋白质 A）：
<query_observe>A</query_observe>

- 预测校验（例如预测蛋白质 B 的值为 5）：
<query_verify>B,5</query_verify>

- 最终提交（需同时提供规则描述和隐藏顶点）：
<answer>rule=包含隐藏顶点的三角形数量, hidden=D</answer>

注意：
- 观测查询会消耗查询次数
- 预测校验不消耗查询次数，但只会告知对错和正确值，不提供其他信息
- 最终提交的规则描述必须准确描述计算方法
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's conduct a "Protein Interaction Network Analysis" task. Here are the rules:

The system features a public and fixed protein synergistic interaction map with 8 key protein molecules (vertices): A, B, C, D, E, F, G, H.

Synergistic interactions (edge set):
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

Ternary synergistic cluster (i.e., Triangle definition in network topology): A closed-loop complex of three protein molecules that are pairwise interactive (e.g., ABC forms a triangle because interactions AB, AC, BC exist).

The map has the following unknown information:
1. A core pathogenic target protein (i.e., hidden vertex K), which is one of the proteins from A to H.
2. A fixed biological activity index mechanism (rule function f) that maps each protein to a non-negative integer activity value. This value is determined solely by triangle-related structures in the network and is associated with the hidden vertex K.

Your goal is to infer through a limited number of biochemical queries:
1. The exact definition of the activity mechanism f (must clearly describe in natural language how f is derived from triangle structures)
2. The identity of the pathogenic target protein (hidden vertex K)

You can perform the following operations:

1. Observation Query: Query the activity reading value of a protein X. I will return the corresponding value.
2. Verification Query: Submit your predicted value n for a protein X. I will tell you if it's correct, and provide the correct value if wrong. This operation does not consume observation counts.
3. Final Submission: When you've determined the rule and hidden vertex, submit your final diagnostic answer.

Important notes:
- The mechanism f is deterministic and invariant; querying the same protein multiple times yields consistent results.
- You need to complete the inference with as few queries as possible.
- In the final submission, the rule description must precisely state how f is calculated. To ensure correct system recognition, please continue to use the standard terms "hidden vertex" and "triangle" in your description.

Each operation must contain only one tag:

- Observation Query (e.g., querying protein A):
<query_observe>A</query_observe>

- Verification Query (e.g., predicting protein B has value 5):
<query_verify>B,5</query_verify>

- Final Submission (must provide both rule description and hidden vertex):
<answer>rule=number of triangles containing the hidden vertex, hidden=D</answer>

Note:
- Observation queries consume query counts
- Verification queries do not consume query counts, but only indicate correctness and provide the correct value
- The rule description in final submission must accurately describe the calculation method
"""

    contextualized_rule_zh_3 = """\
【教育场景】
我们现在来进行一项“课程体系知识图谱解析”任务，规则如下：

教务系统设定了一个公开且固定的学科知识图谱，包含 8 个核心知识模块（即图谱中的顶点）：A, B, C, D, E, F, G, H。

前置依赖关联（即边集）如下：
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

跨学科知识闭环（即图谱结构中的“三角形”）：三个知识模块两两相互依赖构成的知识闭环（例如 ABC 因为存在关联 AB、AC、BC 而构成一个三角形）。

系统中存在以下未知情况：
1. 一个核心考察基石模块（即隐藏考点 K），它是 A 到 H 中的某一个知识模块。
2. 一个固定的复习权重计算公式（即规则函数 f），它将每个模块映射到一个非负整数权重分。该分数仅由图谱中与三角形相关的结构决定，并且与隐藏考点 K 有关联。

你的目标是通过有限次数的教务系统查询，推断出：
1. 复习权重公式 f 的精确定义（必须用自然语言清晰描述 f 如何由三角形结构导出）
2. 核心考察基石模块（即隐藏顶点 K）的身份

你可以进行以下操作：
1. 观测查询：查询某个知识模块 X 的权重分数。我会返回该模块对应的数值。
2. 预测校验：提交你对某个模块 X 的分数预测值 n。我会告诉你是否正确，如果错误会给出正确值。此操作不消耗观测次数。
3. 最终提交：当你确定规则和隐藏考点时，提交最终的解析答案。

重要说明：
- 权重公式 f 是确定的、不变的，对同一模块的多次查询结果一致。
- 你需要在尽可能少的查询次数内完成推断。
- 最终提交时，规则描述必须精确表述 f 如何计算。为了保证教务系统正确识别，请在最终描述中继续使用“隐藏顶点”和“三角形”这两个标准术语。

每次只能包含一个操作标签：

- 观测查询（例如查询模块 A）：
<query_observe>A</query_observe>

- 预测校验（例如预测模块 B 的分数为 5）：
<query_verify>B,5</query_verify>

- 最终提交（需同时提供规则描述和隐藏顶点）：
<answer>rule=包含隐藏顶点的三角形数量, hidden=D</answer>

注意：
- 观测查询会消耗查询次数
- 预测校验不消耗查询次数，但只会告知对错和正确值，不提供其他信息
- 最终提交的规则描述必须准确描述计算方法
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Course Knowledge Graph Analysis" task. Here are the rules:

The academic system features a public and fixed knowledge graph with 8 core knowledge modules (vertices): A, B, C, D, E, F, G, H.

Prerequisite relationships (edge set):
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

Interdisciplinary knowledge loop (i.e., Triangle definition in graph structure): A closed loop of three knowledge modules that are pairwise related (e.g., ABC forms a triangle because relations AB, AC, BC exist).

The system has the following unknown information:
1. A core testing module (i.e., hidden vertex K), which is one of the modules from A to H.
2. A fixed review weight calculation formula (rule function f) that maps each module to a non-negative integer weight score. This score is determined solely by triangle-related structures in the graph and is associated with the hidden vertex K.

Your goal is to infer through a limited number of system queries:
1. The exact definition of the formula f (must clearly describe in natural language how f is derived from triangle structures)
2. The identity of the core testing module (hidden vertex K)

You can perform the following operations:

1. Observation Query: Query the weight score of a module X. I will return the corresponding value.
2. Verification Query: Submit your predicted score n for a module X. I will tell you if it's correct, and provide the correct value if wrong. This operation does not consume observation counts.
3. Final Submission: When you've determined the rule and hidden testing module, submit your final analysis.

Important notes:
- The formula f is deterministic and invariant; querying the same module multiple times yields consistent results.
- You need to complete the inference with as few queries as possible.
- In the final submission, the rule description must precisely state how f is calculated. To ensure correct system recognition, please continue to use the standard terms "hidden vertex" and "triangle" in your description.

Each operation must contain only one tag:

- Observation Query (e.g., querying module A):
<query_observe>A</query_observe>

- Verification Query (e.g., predicting module B has score 5):
<query_verify>B,5</query_verify>

- Final Submission (must provide both rule description and hidden vertex):
<answer>rule=number of triangles containing the hidden vertex, hidden=D</answer>

Note:
- Observation queries consume query counts
- Verification queries do not consume query counts, but only indicate correctness and provide the correct value
- The rule description in final submission must accurately describe the calculation method
"""

    contextualized_rule_zh_4 = """\
【工业制造场景】
我们现在来进行一项“供应链协同网络诊断”任务，规则如下：

排产系统设定了一个公开且固定的供应链协同网络，包含 8 个生产节点（即网络中的顶点）：A, B, C, D, E, F, G, H。

物料流转路径（即边集）如下：
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

闭环生产协同圈（即网络拓扑中的“三角形”）：三个生产节点两两流转互通构成的闭环（例如 ABC 因为存在流转路径 AB、AC、BC 而构成一个三角形）。

网络中存在以下未知情况：
1. 一个核心生产瓶颈（即隐藏顶点 K），它是 A 到 H 中的某一个生产节点。
2. 一个固定的产能负荷指数模型（即规则函数 f），它将每个生产节点映射到一个非负整数负荷值。该指数仅由网络中与三角形相关的协同结构决定，并且与核心瓶颈（隐藏顶点 K）有关联。

你的目标是通过有限次数的诊断查询，推断出：
1. 产能负荷模型 f 的精确定义（必须用自然语言清晰描述 f 如何由三角形结构导出）
2. 核心生产瓶颈（即隐藏顶点 K）的身份

你可以进行以下操作：
1. 观测查询：查询某个生产节点 X 的负荷指数值。我会返回对应的数值。
2. 预测校验：提交你对某个节点 X 的指数预测值 n。我会告诉你是否正确，如果错误会给出正确值。此操作不消耗观测次数。
3. 最终提交：当你确定规则和瓶颈节点时，提交最终的诊断结果。

重要说明：
- 负荷指数模型 f 是确定的、不变的，对同一节点的多次查询结果一致。
- 你需要在尽可能少的诊断查询次数内完成推断。
- 最终提交时，规则描述必须精确表述 f 如何计算。为了保证排产系统正确解析判定，请在最终描述中继续使用“隐藏顶点”和“三角形”这两个标准术语。

每次只能包含一个操作标签：

- 观测查询（例如查询生产节点 A）：
<query_observe>A</query_observe>

- 预测校验（例如预测生产节点 B 的值为 5）：
<query_verify>B,5</query_verify>

- 最终提交（需同时提供规则描述和隐藏顶点）：
<answer>rule=包含隐藏顶点的三角形数量, hidden=D</answer>

注意：
- 观测查询会消耗查询次数
- 预测校验不消耗查询次数，但只会告知对错和正确值，不提供其他信息
- 最终提交的规则描述必须准确描述计算方法
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct a "Supply Chain Coordination Network Diagnosis" task. Here are the rules:

The production scheduling system features a public and fixed supply chain network with 8 production nodes (vertices): A, B, C, D, E, F, G, H.

Material flows (edge set):
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

Closed-loop supply circle (i.e., Triangle definition in network topology): A closed loop of three production nodes that are pairwise interconnected (e.g., ABC forms a triangle because flows AB, AC, BC exist).

The network has the following unknown information:
1. A core bottleneck node (i.e., hidden vertex K), which is one of the nodes from A to H.
2. A fixed capacity load index model (rule function f) that maps each node to a non-negative integer load value. This index is determined solely by triangle-related collaborative structures in the network and is associated with the hidden bottleneck (hidden vertex K).

Your goal is to infer through a limited number of diagnostic queries:
1. The exact definition of the capacity load model f (must clearly describe in natural language how f is derived from triangle structures)
2. The identity of the core bottleneck node (hidden vertex K)

You can perform the following operations:

1. Observation Query: Query the load index value of a node X. I will return the corresponding value.
2. Verification Query: Submit your predicted index n for a node X. I will tell you if it's correct, and provide the correct value if wrong. This operation does not consume observation counts.
3. Final Submission: When you've determined the rule and hidden bottleneck, submit your final diagnostic result.

Important notes:
- The model f is deterministic and invariant; querying the same node multiple times yields consistent results.
- You need to complete the inference with as few diagnostic queries as possible.
- In the final submission, the rule description must precisely state how f is calculated. To ensure correct system parsing, please continue to use the standard terms "hidden vertex" and "triangle" in your description.

Each operation must contain only one tag:

- Observation Query (e.g., querying node A):
<query_observe>A</query_observe>

- Verification Query (e.g., predicting node B has index 5):
<query_verify>B,5</query_verify>

- Final Submission (must provide both rule description and hidden vertex):
<answer>rule=number of triangles containing the hidden vertex, hidden=D</answer>

Note:
- Observation queries consume query counts
- Verification queries do not consume query counts, but only indicate correctness and provide the correct value
- The rule description in final submission must accurately describe the calculation method
"""

    contextualized_rule_zh_5 = """\
【法律经侦场景】
我们现在来进行一项“经侦资金流转网络盘查”任务，规则如下：

经侦系统调取了一个公开且固定的涉案资金网络，包含 8 个涉案主体或空壳公司（即网络中的顶点）：A, B, C, D, E, F, G, H。

已被查实的资金往来（即边集）如下：
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

三角利益输送圈（即网络拓扑中的“三角形”）：三个涉案主体两两产生资金往来构成的闭环洗钱结构（例如 ABC 因为存在往来 AB、AC、BC 而构成一个三角形）。

网络中存在以下未知情况：
1. 一个幕后实控主体（即隐藏顶点 K），它是 A 到 H 中的某一个涉案主体。
2. 一套内部的洗钱风险评估指数公式（即规则函数 f），它将每个涉案主体映射到一个非负整数风险值。该指数仅由网络中与三角形相关的闭环结构决定，并且与幕后实控主体（隐藏顶点 K）有关联。

你的目标是通过有限次数的审查调证，推断出：
1. 风险指数公式 f 的精确定义（必须用自然语言清晰描述 f 如何由三角形结构导出）
2. 幕后实控主体（即隐藏顶点 K）的身份

你可以进行以下操作：
1. 观测查询：查询某个涉案主体 X 的风险读数值。我会返回对应的数值。
2. 预测校验：提交你对某个主体 X 的风险预测值 n。我会告诉你是否正确，如果错误会给出正确值。此操作不消耗观测次数。
3. 最终提交：当你确定规则和幕后实控主体时，提交最终的盘查结论。

重要说明：
- 风险公式 f 是确定的、不变的，对同一主体的多次查询结果一致。
- 你需要在尽可能少的审查调证次数内完成推断。
- 最终提交时，规则描述必须精确表述 f 如何计算。为了保证经侦判定系统顺利录入卷宗，请在最终描述中继续使用“隐藏顶点”和“三角形”这两个标准术语。

每次只能包含一个操作标签：

- 观测查询（例如查询涉案主体 A）：
<query_observe>A</query_observe>

- 预测校验（例如预测涉案主体 B 的值为 5）：
<query_verify>B,5</query_verify>

- 最终提交（需同时提供规则描述和隐藏顶点）：
<answer>rule=包含隐藏顶点的三角形数量, hidden=D</answer>

注意：
- 观测查询会消耗查询次数
- 预测校验不消耗查询次数，但只会告知对错和正确值，不提供其他信息
- 最终提交的规则描述必须准确描述计算方法
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct an "Economic Crime Funds Network Investigation" task. Here are the rules:

The system has retrieved a public and fixed suspect funds network with 8 involved entities (vertices): A, B, C, D, E, F, G, H.

Verified financial transactions (edge set):
- AB, AC, AD, BC, BD, CD
- BE, CE, DE
- CF, DF, EF
- DG, EG, FG
- EH, FH, GH

Triangle interest transfer circle (i.e., Triangle definition in network topology): A closed-loop money laundering structure of three entities that are pairwise transacting (e.g., ABC forms a triangle because transactions AB, AC, BC exist).

The network has the following unknown information:
1. A hidden mastermind entity (i.e., hidden vertex K), which is one of the entities from A to H.
2. An internal money laundering risk index formula (rule function f) that maps each entity to a non-negative integer risk value. This index is determined solely by triangle-related closed-loop structures in the network and is associated with the mastermind (hidden vertex K).

Your goal is to infer through a limited number of investigative queries:
1. The exact definition of the risk formula f (must clearly describe in natural language how f is derived from triangle structures)
2. The identity of the hidden mastermind entity (hidden vertex K)

You can perform the following operations:

1. Observation Query: Query the risk reading value of an entity X. I will return the corresponding value.
2. Verification Query: Submit your predicted risk value n for an entity X. I will tell you if it's correct, and provide the correct value if wrong. This operation does not consume observation counts.
3. Final Submission: When you've determined the rule and mastermind, submit your final investigative conclusion.

Important notes:
- The formula f is deterministic and invariant; querying the same entity multiple times yields consistent results.
- You need to complete the inference with as few investigative queries as possible.
- In the final submission, the rule description must precisely state how f is calculated. To ensure smooth entry into the legal case system, please continue to use the standard terms "hidden vertex" and "triangle" in your description.

Each operation must contain only one tag:

- Observation Query (e.g., querying entity A):
<query_observe>A</query_observe>

- Verification Query (e.g., predicting entity B has value 5):
<query_verify>B,5</query_verify>

- Final Submission (must provide both rule description and hidden vertex):
<answer>rule=number of triangles containing the hidden vertex, hidden=D</answer>

Note:
- Observation queries consume query counts
- Verification queries do not consume query counts, but only indicate correctness and provide the correct value
- The rule description in final submission must accurately describe the calculation method
"""

    tags = ["answer", "query_observe", "query_verify"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    GRAPH_EDGES = [
        ('A', 'B'), ('A', 'C'), ('A', 'D'),
        ('B', 'C'), ('B', 'D'), ('C', 'D'),
        ('B', 'E'), ('C', 'E'), ('D', 'E'),
        ('C', 'F'), ('D', 'F'), ('E', 'F'),
        ('D', 'G'), ('E', 'G'), ('F', 'G'),
        ('E', 'H'), ('F', 'H'), ('G', 'H')
    ]
    
    VERTICES = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "hidden_vertex": "D",
                "rule_type": "triangles_containing_vertex",
                "rule_desc": "包含该顶点的三角形数量"
            },
            2: {
                "hidden_vertex": "E",
                "rule_type": "vertices_sharing_triangle_with_hidden",
                "rule_desc": "与隐藏顶点共享至少一个三角形的顶点数量"
            },
            3: {
                "hidden_vertex": "C",
                "rule_type": "triangles_containing_vertex_not_hidden",
                "rule_desc": "包含该顶点但不包含隐藏顶点的三角形数量"
            },
            4: {
                "hidden_vertex": "F",
                "rule_type": "common_neighbors_with_hidden",
                "rule_desc": "该顶点与隐藏顶点的共同邻居数量"
            },
            5: {
                "hidden_vertex": "E",
                "rule_type": "triangles_containing_both",
                "rule_desc": "同时包含该顶点和隐藏顶点的三角形数量"
            }
        },
        "en": {
            1: {
                "hidden_vertex": "D",
                "rule_type": "triangles_containing_vertex",
                "rule_desc": "number of triangles containing this vertex"
            },
            2: {
                "hidden_vertex": "E",
                "rule_type": "vertices_sharing_triangle_with_hidden",
                "rule_desc": "number of vertices sharing at least one triangle with the hidden vertex"
            },
            3: {
                "hidden_vertex": "C",
                "rule_type": "triangles_containing_vertex_not_hidden",
                "rule_desc": "number of triangles containing this vertex but not the hidden vertex"
            },
            4: {
                "hidden_vertex": "F",
                "rule_type": "common_neighbors_with_hidden",
                "rule_desc": "number of common neighbors between this vertex and the hidden vertex"
            },
            5: {
                "hidden_vertex": "E",
                "rule_type": "triangles_containing_both",
                "rule_desc": "number of triangles containing both this vertex and the hidden vertex"
            }
        }
    }

    def __init__(self, config):
        self._build_graph()
        super().__init__(config)

    def _build_graph(self):
        self.adjacency = {v: set() for v in self.VERTICES}
        for u, v in self.GRAPH_EDGES:
            self.adjacency[u].add(v)
            self.adjacency[v].add(u)
        
        self.triangles = []
        vertices = self.VERTICES
        for i in range(len(vertices)):
            for j in range(i + 1, len(vertices)):
                for k in range(j + 1, len(vertices)):
                    v1, v2, v3 = vertices[i], vertices[j], vertices[k]
                    if (v2 in self.adjacency[v1] and 
                        v3 in self.adjacency[v1] and 
                        v3 in self.adjacency[v2]):
                        self.triangles.append((v1, v2, v3))
        
        self.vertex_triangles = {v: [] for v in self.VERTICES}
        for tri in self.triangles:
            for v in tri:
                self.vertex_triangles[v].append(tri)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.hidden_vertex = cfg["hidden_vertex"]
        self.rule_type = cfg["rule_type"]
        self.expected_rule_desc = cfg["rule_desc"]
        
        self._game_info = {}
        
        self.vertex_values = {}
        for v in self.VERTICES:
            self.vertex_values[v] = self._compute_value(v)
        
        self.query_count = 0

    def _compute_value(self, vertex):
        if self.rule_type == "triangles_containing_vertex":
            return len(self.vertex_triangles[vertex])
        
        elif self.rule_type == "vertices_sharing_triangle_with_hidden":
            if vertex == self.hidden_vertex:
                return len(self.vertex_triangles[vertex])
            count = 0
            for tri in self.vertex_triangles[vertex]:
                if self.hidden_vertex in tri:
                    count += 1
            return count
        
        elif self.rule_type == "triangles_containing_vertex_not_hidden":
            count = 0
            for tri in self.vertex_triangles[vertex]:
                if self.hidden_vertex not in tri:
                    count += 1
            return count
        
        elif self.rule_type == "common_neighbors_with_hidden":
            if vertex == self.hidden_vertex:
                return len(self.adjacency[vertex])
            neighbors_v = self.adjacency[vertex]
            neighbors_h = self.adjacency[self.hidden_vertex]
            return len(neighbors_v & neighbors_h)
        
        elif self.rule_type == "triangles_containing_both":
            if vertex == self.hidden_vertex:
                return len(self.vertex_triangles[vertex])
            count = 0
            for tri in self.vertex_triangles[vertex]:
                if self.hidden_vertex in tri:
                    count += 1
            return count
        
        return 0

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        try:
            hidden_match = re.search(r'hidden\s*=\s*([A-H])', raw_ans, re.IGNORECASE)
            if not hidden_match:
                return False
            
            hidden_vertex = hidden_match.group(1).strip().upper()
            
            rule_part = raw_ans[:hidden_match.start()]
            rule_match = re.search(r'rule\s*=\s*(.+)', rule_part, re.IGNORECASE | re.DOTALL)
            
            if not rule_match:
                return False
            
            rule_desc = rule_match.group(1).strip().rstrip(',').strip()
            
            if hidden_vertex != self.hidden_vertex:
                return False
            
            rule_desc_lower = rule_desc.lower()
            
            if self.config.language == "zh":
                keywords_map = {
                    "triangles_containing_vertex": ["三角形", "包含", "顶点", "数量"],
                    "vertices_sharing_triangle_with_hidden": ["隐藏", "共享", "三角形", "顶点", "数"],
                    "triangles_containing_vertex_not_hidden": ["包含", "不包含", "隐藏", "三角形"],
                    "common_neighbors_with_hidden": ["共同", "邻居", "数量"],
                    "triangles_containing_both": ["同时", "包含", "顶点", "隐藏", "三角形"]
                }
            else:
                keywords_map = {
                    "triangles_containing_vertex": ["triangle", "containing", "vertex"],
                    "vertices_sharing_triangle_with_hidden": ["vertices", "sharing", "triangle", "hidden"],
                    "triangles_containing_vertex_not_hidden": ["triangle", "containing", "not", "hidden"],
                    "common_neighbors_with_hidden": ["common", "neighbor"],
                    "triangles_containing_both": ["triangle", "containing", "both", "hidden"]
                }
            
            keywords = keywords_map.get(self.rule_type, [])
            matched_keywords = sum(1 for kw in keywords if kw in rule_desc_lower)
            
            return matched_keywords >= len(keywords) - 1
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "query_observe" in parsed_info:
            vertex = parsed_info["query_observe"].strip().upper()
            
            if vertex not in self.VERTICES:
                return "错误：无效的顶点。" if lang == "zh" else "Error: Invalid vertex."
            
            self.query_count += 1
            value = self.vertex_values[vertex]
            
            if lang == "zh":
                return f"顶点 {vertex} 的读数为：{value}"
            else:
                return f"Reading for vertex {vertex}: {value}"
        
        elif "query_verify" in parsed_info:
            try:
                raw = parsed_info["query_verify"].strip()
                parts = raw.split(",")
                if len(parts) != 2:
                    raise ValueError
                
                vertex = parts[0].strip().upper()
                predicted_value = int(parts[1].strip())
                
                if vertex not in self.VERTICES:
                    return "错误：无效的顶点。" if lang == "zh" else "Error: Invalid vertex."
                
                actual_value = self.vertex_values[vertex]
                
                if predicted_value == actual_value:
                    return f"检验 {vertex}: 正确" if lang == "zh" else f"Verification {vertex}: Correct"
                else:
                    if lang == "zh":
                        return f"检验 {vertex}: 错误，正确值为 {actual_value}"
                    else:
                        return f"Verification {vertex}: Incorrect, correct value is {actual_value}"
                        
            except Exception:
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
            
        import re
        if re.search(r'\d+', correct):
            return re.sub(r'\d+', lambda m: str(int(m.group(0)) + 1), correct)
        
        lang = self.config.language
        ret = correct
        
        if lang == "zh":
            if "正确" in ret:
                return ret.replace("正确", "错误")
            elif "错误" in ret:
                return ret.replace("错误", "正确")
            elif "是" in ret:
                return ret.replace("是", "否")
            elif "否" in ret:
                return ret.replace("否", "是")
        else:
            def replace_case_insensitive(text, old, new):
                pattern = re.compile(re.escape(old), re.IGNORECASE)
                return pattern.sub(lambda m: new.upper() if m.group(0).isupper() 
                                   else new.lower() if m.group(0).islower() 
                                   else new.capitalize() if m.group(0)[0].isupper() 
                                   else new, text)

            if re.search(r'\bcorrect\b', ret, re.IGNORECASE):
                return replace_case_insensitive(ret, "Correct", "Incorrect")
            elif re.search(r'\bincorrect\b', ret, re.IGNORECASE):
                return replace_case_insensitive(ret, "Incorrect", "Correct")
            elif re.search(r'\byes\b', ret, re.IGNORECASE):
                return replace_case_insensitive(ret, "Yes", "No")
            elif re.search(r'\bno\b', ret, re.IGNORECASE):
                return replace_case_insensitive(ret, "No", "Yes")

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        lang = self.config.language
        
        for vertex in self.VERTICES:
            query_xml = f"<query_observe>{vertex}</query_observe>"
            
            value = self.vertex_values[vertex]
            
            if lang == "zh":
                answer = f"顶点 {vertex} 的读数为：{value}"
            else:
                answer = f"Reading for vertex {vertex}: {value}"
            
            results.append({
                "query": query_xml,
                "answer": answer
            })
            
        return results