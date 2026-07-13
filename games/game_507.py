from .base import Game
import math
from typing import List, Dict

class HiddenParentFunctionGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏父函数推理"游戏，规则如下：

游戏设定了一个节点集合 {{0, 1, 2, ..., {N}}}，其中存在一个隐藏的父函数 f，对于每个节点 i（i 大于等于 1），都有 f(i) 是一个小于 i 的非负整数，即 f(i) 属于 {{0, 1, ..., i-1}}。这样所有节点通过父函数形成了一棵以 0 为根的树结构。

父函数 f 遵循某个固定的数值规则（例如：某种数学公式），但具体规则对你是隐藏的。

你的目标是：推断出目标节点集合 T = {{{target_nodes}}} 中每个节点的父节点值，即对于每个 t 在 T 中，找出 f(t) 的值。

为了帮助你推理，你可以向我提出两类查询（查询次数有限）：

1. **值查询**：询问某个非目标节点 x 的父节点值 f(x)。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，且 x 不能是目标节点（即 x 不在 T 中）。
   - 回答：返回 f(x) 的具体数值。
   - 预算：你最多可以进行 {L} 次值查询。

2. **等式查询**：询问某个节点 x 的父节点是否等于 y。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，y 必须在 {{0, ..., x-1}} 范围内。
   - 回答：回答"是"或"否"。
   - 预算：你最多可以进行 {M} 次等式查询。

当你收集到足够信息后，请提交最终答案。答案需要包含目标集合 T 中所有节点的父节点值。

## 查询与提交答案的格式

每次只能提交一个查询或答案。请使用以下 XML 格式：

- 值查询（例如查询节点 5 的父节点）：
<query_value>5</query_value>

- 等式查询（例如询问节点 7 的父节点是否为 3）：
<query_equal>7,3</query_equal>

- 提交最终答案（格式为"节点=父节点"的列表，用分号分隔）：
<answer>8=4;12=6;15=7</answer>

注意：答案中必须包含目标集合 T 中的所有节点，且格式严格按照上述要求。
"""

    game_rule_en = """\
Let's play a "Hidden Parent Function Inference" game. Here are the rules:

The game defines a node set {{0, 1, 2, ..., {N}}}, where there exists a hidden parent function f. For each node i (i greater than or equal to 1), f(i) is a non-negative integer less than i, i.e., f(i) belongs to {{0, 1, ..., i-1}}. All nodes form a tree structure rooted at 0 through the parent function.

The parent function f follows a fixed numerical rule (e.g., some mathematical formula), but the specific rule is hidden from you.

Your goal is: Infer the parent node value for each node in the target node set T = {{{target_nodes}}}, i.e., for each t in T, find the value of f(t).

To help you reason, you can make two types of queries (with limited query budget):

1. **Value Query**: Ask for the parent node value f(x) of a non-target node x.
   - Constraint: x must be in the range {{1, ..., {N}}}, and x cannot be a target node (i.e., x not in T).
   - Answer: Returns the specific value of f(x).
   - Budget: You can make at most {L} value queries.

2. **Equality Query**: Ask whether the parent node of node x equals y.
   - Constraint: x must be in the range {{1, ..., {N}}}, y must be in the range {{0, ..., x-1}}.
   - Answer: Answers "Yes" or "No".
   - Budget: You can make at most {M} equality queries.

When you have collected enough information, submit your final answer. The answer must include the parent node values for all nodes in the target set T.

## Query and Answer Format

You can only submit one query or answer at a time. Use the following XML format:

- Value Query (e.g., query the parent of node 5):
<query_value>5</query_value>

- Equality Query (e.g., ask if the parent of node 7 is 3):
<query_equal>7,3</query_equal>

- Submit Final Answer (format as "node=parent" list, separated by semicolons):
<answer>8=4;12=6;15=7</answer>

Note: The answer must include all nodes in the target set T, with strict adherence to the format above.
"""

    contextualized_rule_zh_1 = """\
我们正在进行城市交通路网的层级调度链路梳理。

系统设定了一个交通节点集合 {{0, 1, 2, ..., {N}}}，其中存在一个隐藏的直接上级调度节点 f，对于每个交通节点 i（i 大于等于 1），都有 f(i) 是一个小于 i 的非负整数，即 f(i) 属于 {{0, 1, ..., i-1}}。这样所有交通节点通过调度关系形成了一棵以 0（总控制中心）为根的层级控制树。

直接上级调度节点 f 遵循某个固定的系统分配规则，但具体规则对你是隐藏的。

你的目标是：推断出需要紧急维护的目标集合 T = {{{target_nodes}}} 中每个交通节点的直接上级调度节点值，即对于每个 t 在 T 中，找出 f(t) 的值。

为了帮助你推理，你可以向我提出两类查询（查询次数有限）：

1. **值查询**（向上级调度追溯）：询问某个非目标交通节点 x 的直接上级调度节点值 f(x)。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，且 x 不能是目标交通节点（即 x 不在 T 中）。
   - 回答：返回 f(x) 的具体数值。
   - 预算：你最多可以进行 {L} 次值查询。

2. **等式查询**（校验调度关系）：询问某个交通节点 x 的直接上级调度节点是否等于 y。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，y 必须在 {{0, ..., x-1}} 范围内。
   - 回答：回答"是"或"否"。
   - 预算：你最多可以进行 {M} 次等式查询。

当你收集到足够信息后，请提交最终答案。答案需要包含目标集合 T 中所有交通节点的直接上级调度节点值。

## 查询与提交答案的格式

每次只能提交一个查询或答案。请使用以下 XML 格式：

- 值查询（例如查询交通节点 5 的直接上级调度节点）：
<query_value>5</query_value>

- 等式查询（例如询问交通节点 7 的直接上级调度节点是否为 3）：
<query_equal>7,3</query_equal>

- 提交最终答案（格式为"交通节点=直接上级调度节点"的列表，用分号分隔）：
<answer>8=4;12=6;15=7</answer>

注意：答案中必须包含目标集合 T 中的所有交通节点，且格式严格按照上述要求。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are sorting out the hierarchical dispatch links of the urban traffic network.

The system defines a traffic node set {{0, 1, 2, ..., {N}}}, where there exists a hidden direct superior dispatch node f. For each traffic node i (i greater than or equal to 1), f(i) is a non-negative integer less than i, i.e., f(i) belongs to {{0, 1, ..., i-1}}. All traffic nodes form a hierarchical control tree rooted at 0 (the main control center) through the dispatch relations.

The direct superior dispatch node f follows a fixed system allocation rule, but the specific rule is hidden from you.

Your goal is: Infer the direct superior dispatch node value for each traffic node in the target set T = {{{target_nodes}}} requiring emergency maintenance, i.e., for each t in T, find the value of f(t).

To help you reason, you can make two types of queries (with limited query budget):

1. **Value Query** (Trace Superior Dispatch): Ask for the direct superior dispatch node value f(x) of a non-target traffic node x.
   - Constraint: x must be in the range {{1, ..., {N}}}, and x cannot be a target traffic node (i.e., x not in T).
   - Answer: Returns the specific value of f(x).
   - Budget: You can make at most {L} value queries.

2. **Equality Query** (Verify Dispatch Relation): Ask whether the direct superior dispatch node of traffic node x equals y.
   - Constraint: x must be in the range {{1, ..., {N}}}, y must be in the range {{0, ..., x-1}}.
   - Answer: Answers "Yes" or "No".
   - Budget: You can make at most {M} equality queries.

When you have collected enough information, submit your final answer. The answer must include the direct superior dispatch node values for all traffic nodes in the target set T.

## Query and Answer Format

You can only submit one query or answer at a time. Use the following XML format:

- Value Query (e.g., query the direct superior dispatch node of traffic node 5):
<query_value>5</query_value>

- Equality Query (e.g., ask if the direct superior dispatch node of traffic node 7 is 3):
<query_equal>7,3</query_equal>

- Submit Final Answer (format as "traffic node=direct superior dispatch node" list, separated by semicolons):
<answer>8=4;12=6;15=7</answer>

Note: The answer must include all traffic nodes in the target set T, with strict adherence to the format above.
"""

    contextualized_rule_zh_2 = """\
我们正在执行一项传染病溯源的流行病学调查任务。

系统设定了一个感染病例集合 {{0, 1, 2, ..., {N}}}，其中存在一个隐藏的直接传染源 f，对于每个病例 i（i 大于等于 1），都有 f(i) 是一个小于 i 的非负整数，即 f(i) 属于 {{0, 1, ..., i-1}}。这样所有病例通过传播链形成了一棵以 0（零号病人）为根的感染树。

直接传染源 f 遵循某个固定的病毒传播机制，但具体机制对你是隐藏的。

你的目标是：推断出重点关注的目标集合 T = {{{target_nodes}}} 中每个病例的直接传染源编号，即对于每个 t 在 T 中，找出 f(t) 的值。

为了帮助你推理，你可以向我提出两类查询（查询次数有限）：

1. **值查询**（流行病学调查）：询问某个非目标病例 x 的直接传染源编号 f(x)。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，且 x 不能是目标病例（即 x 不在 T 中）。
   - 回答：返回 f(x) 的具体数值。
   - 预算：你最多可以进行 {L} 次值查询。

2. **等式查询**（接触史比对）：询问某个病例 x 的直接传染源是否等于病例 y。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，y 必须在 {{0, ..., x-1}} 范围内。
   - 回答：回答"是"或"否"。
   - 预算：你最多可以进行 {M} 次等式查询。

当你收集到足够信息后，请提交最终答案。答案需要包含目标集合 T 中所有病例的直接传染源编号。

## 查询与提交答案的格式

每次只能提交一个查询或答案。请使用以下 XML 格式：

- 值查询（例如查询病例 5 的直接传染源）：
<query_value>5</query_value>

- 等式查询（例如询问病例 7 的直接传染源是否为 3）：
<query_equal>7,3</query_equal>

- 提交最终答案（格式为"病例=直接传染源"的列表，用分号分隔）：
<answer>8=4;12=6;15=7</answer>

注意：答案中必须包含目标集合 T 中的所有病例，且格式严格按照上述要求。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
We are executing an epidemiological investigation task for tracing infectious diseases.

The system defines an infection case set {{0, 1, 2, ..., {N}}}, where there exists a hidden direct source of infection f. For each case i (i greater than or equal to 1), f(i) is a non-negative integer less than i, i.e., f(i) belongs to {{0, 1, ..., i-1}}. All cases form an infection tree rooted at 0 (patient zero) through the transmission chain.

The direct source of infection f follows a fixed virus transmission mechanism, but the specific mechanism is hidden from you.

Your goal is: Infer the direct source of infection ID for each case in the key monitoring target set T = {{{target_nodes}}}, i.e., for each t in T, find the value of f(t).

To help you reason, you can make two types of queries (with limited query budget):

1. **Value Query** (Epidemiological Investigation): Ask for the direct source of infection ID f(x) of a non-target case x.
   - Constraint: x must be in the range {{1, ..., {N}}}, and x cannot be a target case (i.e., x not in T).
   - Answer: Returns the specific value of f(x).
   - Budget: You can make at most {L} value queries.

2. **Equality Query** (Contact History Comparison): Ask whether the direct source of infection for case x equals y.
   - Constraint: x must be in the range {{1, ..., {N}}}, y must be in the range {{0, ..., x-1}}.
   - Answer: Answers "Yes" or "No".
   - Budget: You can make at most {M} equality queries.

When you have collected enough information, submit your final answer. The answer must include the direct source of infection IDs for all cases in the target set T.

## Query and Answer Format

You can only submit one query or answer at a time. Use the following XML format:

- Value Query (e.g., query the direct source of infection of case 5):
<query_value>5</query_value>

- Equality Query (e.g., ask if the direct source of infection of case 7 is 3):
<query_equal>7,3</query_equal>

- Submit Final Answer (format as "case=direct source of infection" list, separated by semicolons):
<answer>8=4;12=6;15=7</answer>

Note: The answer must include all cases in the target set T, with strict adherence to the format above.
"""

    contextualized_rule_zh_3 = """\
我们正在构建知识图谱的前置依赖系统大纲。

系统设定了一个知识点集合 {{0, 1, 2, ..., {N}}}，其中存在一个隐藏的核心前置知识点 f，对于每个知识点 i（i 大于等于 1），都有 f(i) 是一个小于 i 的非负整数，即 f(i) 属于 {{0, 1, ..., i-1}}。这样所有知识点通过先决条件关系形成了一棵以 0（基础启蒙知识）为根的学习路径树。

核心前置知识点 f 遵循某个固定的教学法规则，但具体规则对你是隐藏的。

你的目标是：推断出特定高阶课程的目标集合 T = {{{target_nodes}}} 中每个知识点的核心前置知识点值，即对于每个 t 在 T 中，找出 f(t) 的值。

为了帮助你推理，你可以向我提出两类查询（查询次数有限）：

1. **值查询**（教学大纲查询）：询问某个非目标知识点 x 的核心前置知识点 f(x)。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，且 x 不能是目标知识点（即 x 不在 T 中）。
   - 回答：返回 f(x) 的具体数值。
   - 预算：你最多可以进行 {L} 次值查询。

2. **等式查询**（先修条件测试）：询问某个知识点 x 的核心前置知识点是否等于 y。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，y 必须在 {{0, ..., x-1}} 范围内。
   - 回答：回答"是"或"否"。
   - 预算：你最多可以进行 {M} 次等式查询。

当你收集到足够信息后，请提交最终答案。答案需要包含目标集合 T 中所有知识点的核心前置知识点值。

## 查询与提交答案的格式

每次只能提交一个查询或答案。请使用以下 XML 格式：

- 值查询（例如查询知识点 5 的核心前置知识点）：
<query_value>5</query_value>

- 等式查询（例如询问知识点 7 的核心前置知识点是否为 3）：
<query_equal>7,3</query_equal>

- 提交最终答案（格式为"知识点=核心前置知识点"的列表，用分号分隔）：
<answer>8=4;12=6;15=7</answer>

注意：答案中必须包含目标集合 T 中的所有知识点，且格式严格按照上述要求。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are constructing the prerequisite dependency outline for a knowledge graph.

The system defines a knowledge point set {{0, 1, 2, ..., {N}}}, where there exists a hidden core prerequisite knowledge point f. For each knowledge point i (i greater than or equal to 1), f(i) is a non-negative integer less than i, i.e., f(i) belongs to {{0, 1, ..., i-1}}. All knowledge points form a learning path tree rooted at 0 (foundational introductory knowledge) through prerequisite relations.

The core prerequisite knowledge point f follows a fixed pedagogical rule, but the specific rule is hidden from you.

Your goal is: Infer the core prerequisite knowledge point value for each knowledge point in the target set T = {{{target_nodes}}} representing specific advanced courses, i.e., for each t in T, find the value of f(t).

To help you reason, you can make two types of queries (with limited query budget):

1. **Value Query** (Syllabus Query): Ask for the core prerequisite knowledge point f(x) of a non-target knowledge point x.
   - Constraint: x must be in the range {{1, ..., {N}}}, and x cannot be a target knowledge point (i.e., x not in T).
   - Answer: Returns the specific value of f(x).
   - Budget: You can make at most {L} value queries.

2. **Equality Query** (Prerequisite Condition Test): Ask whether the core prerequisite knowledge point of knowledge point x equals y.
   - Constraint: x must be in the range {{1, ..., {N}}}, y must be in the range {{0, ..., x-1}}.
   - Answer: Answers "Yes" or "No".
   - Budget: You can make at most {M} equality queries.

When you have collected enough information, submit your final answer. The answer must include the core prerequisite knowledge point values for all knowledge points in the target set T.

## Query and Answer Format

You can only submit one query or answer at a time. Use the following XML format:

- Value Query (e.g., query the core prerequisite knowledge point of knowledge point 5):
<query_value>5</query_value>

- Equality Query (e.g., ask if the core prerequisite knowledge point of knowledge point 7 is 3):
<query_equal>7,3</query_equal>

- Submit Final Answer (format as "knowledge point=core prerequisite knowledge point" list, separated by semicolons):
<answer>8=4;12=6;15=7</answer>

Note: The answer must include all knowledge points in the target set T, with strict adherence to the format above.
"""

    contextualized_rule_zh_4 = """\
我们正在进行供应链与生产工序的追溯审查。

系统设定了一个生产工序集合 {{0, 1, 2, ..., {N}}}，其中存在一个隐藏的直接上游工序 f，对于每个工序 i（i 大于等于 1），都有 f(i) 是一个小于 i 的非负整数，即 f(i) 属于 {{0, 1, ..., i-1}}。这样所有生产工序通过装配依赖关系形成了一棵以 0（原材料获取）为根的BOM（物料清单）树。

直接上游工序 f 遵循某个固定的工业设计规范，但具体规范对你是隐藏的。

你的目标是：推断出存在质量缺陷的目标集合 T = {{{target_nodes}}} 中每个生产工序的直接上游工序值，即对于每个 t 在 T 中，找出 f(t) 的值。

为了帮助你推理，你可以向我提出两类查询（查询次数有限）：

1. **值查询**（BOM单审查）：询问某个非目标工序 x 的直接上游工序 f(x)。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，且 x 不能是目标工序（即 x 不在 T 中）。
   - 回答：返回 f(x) 的具体数值。
   - 预算：你最多可以进行 {L} 次值查询。

2. **等式查询**（装配校验）：询问某个工序 x 的直接上游工序是否等于 y。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，y 必须在 {{0, ..., x-1}} 范围内。
   - 回答：回答"是"或"否"。
   - 预算：你最多可以进行 {M} 次等式查询。

当你收集到足够信息后，请提交最终答案。答案需要包含目标集合 T 中所有生产工序的直接上游工序值。

## 查询与提交答案的格式

每次只能提交一个查询或答案。请使用以下 XML 格式：

- 值查询（例如查询生产工序 5 的直接上游工序）：
<query_value>5</query_value>

- 等式查询（例如询问生产工序 7 的直接上游工序是否为 3）：
<query_equal>7,3</query_equal>

- 提交最终答案（格式为"生产工序=直接上游工序"的列表，用分号分隔）：
<answer>8=4;12=6;15=7</answer>

注意：答案中必须包含目标集合 T 中的所有生产工序，且格式严格按照上述要求。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
We are conducting a traceability review of the supply chain and production processes.

The system defines a production process set {{0, 1, 2, ..., {N}}}, where there exists a hidden direct upstream process f. For each process i (i greater than or equal to 1), f(i) is a non-negative integer less than i, i.e., f(i) belongs to {{0, 1, ..., i-1}}. All production processes form a BOM (Bill of Materials) tree rooted at 0 (raw material acquisition) through assembly dependencies.

The direct upstream process f follows a fixed industrial design specification, but the specific specification is hidden from you.

Your goal is: Infer the direct upstream process value for each production process in the target set T = {{{target_nodes}}} that exhibits quality defects, i.e., for each t in T, find the value of f(t).

To help you reason, you can make two types of queries (with limited query budget):

1. **Value Query** (BOM Review): Ask for the direct upstream process f(x) of a non-target process x.
   - Constraint: x must be in the range {{1, ..., {N}}}, and x cannot be a target process (i.e., x not in T).
   - Answer: Returns the specific value of f(x).
   - Budget: You can make at most {L} value queries.

2. **Equality Query** (Assembly Verification): Ask whether the direct upstream process of process x equals y.
   - Constraint: x must be in the range {{1, ..., {N}}}, y must be in the range {{0, ..., x-1}}.
   - Answer: Answers "Yes" or "No".
   - Budget: You can make at most {M} equality queries.

When you have collected enough information, submit your final answer. The answer must include the direct upstream process values for all production processes in the target set T.

## Query and Answer Format

You can only submit one query or answer at a time. Use the following XML format:

- Value Query (e.g., query the direct upstream process of production process 5):
<query_value>5</query_value>

- Equality Query (e.g., ask if the direct upstream process of production process 7 is 3):
<query_equal>7,3</query_equal>

- Submit Final Answer (format as "production process=direct upstream process" list, separated by semicolons):
<answer>8=4;12=6;15=7</answer>

Note: The answer must include all production processes in the target set T, with strict adherence to the format above.
"""

    contextualized_rule_zh_5 = """\
我们正在建立法律条款与司法判例的溯源网络。

系统设定了一个法律条款集合 {{0, 1, 2, ..., {N}}}，其中存在一个隐藏的直接上位法依据 f，对于每个条款 i（i 大于等于 1），都有 f(i) 是一个小于 i 的非负整数，即 f(i) 属于 {{0, 1, ..., i-1}}。这样所有法律条款通过法理渊源形成了一棵以 0（宪法基础）为根的法理树。

直接上位法依据 f 遵循某个固定的立法逻辑，但具体逻辑对你是隐藏的。

你的目标是：推断出核心争议条款目标集合 T = {{{target_nodes}}} 中每个条款的直接上位法依据值，即对于每个 t 在 T 中，找出 f(t) 的值。

为了帮助你推理，你可以向我提出两类查询（查询次数有限）：

1. **值查询**（法理渊源检索）：询问某个非目标条款 x 的直接上位法依据 f(x)。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，且 x 不能是目标条款（即 x 不在 T 中）。
   - 回答：返回 f(x) 的具体数值。
   - 预算：你最多可以进行 {L} 次值查询。

2. **等式查询**（法律适用核对）：询问某个条款 x 的直接上位法依据是否等于 y。
   - 约束：x 必须在 {{1, ..., {N}}} 范围内，y 必须在 {{0, ..., x-1}} 范围内。
   - 回答：回答"是"或"否"。
   - 预算：你最多可以进行 {M} 次等式查询。

当你收集到足够信息后，请提交最终答案。答案需要包含目标集合 T 中所有条款的直接上位法依据值。

## 查询与提交答案的格式

每次只能提交一个查询或答案。请使用以下 XML 格式：

- 值查询（例如查询法律条款 5 的直接上位法依据）：
<query_value>5</query_value>

- 等式查询（例如询问法律条款 7 的直接上位法依据是否为 3）：
<query_equal>7,3</query_equal>

- 提交最终答案（格式为"法律条款=直接上位法依据"的列表，用分号分隔）：
<answer>8=4;12=6;15=7</answer>

注意：答案中必须包含目标集合 T 中的所有法律条款，且格式严格按照上述要求。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are establishing a traceability network for legal provisions and judicial precedents.

The system defines a legal provision set {{0, 1, 2, ..., {N}}}, where there exists a hidden direct higher-level legal basis f. For each provision i (i greater than or equal to 1), f(i) is a non-negative integer less than i, i.e., f(i) belongs to {{0, 1, ..., i-1}}. All legal provisions form a jurisprudential tree rooted at 0 (constitutional basis) through jurisprudential origins.

The direct higher-level legal basis f follows a fixed legislative logic, but the specific logic is hidden from you.

Your goal is: Infer the direct higher-level legal basis value for each provision in the target set T = {{{target_nodes}}} of core disputed provisions, i.e., for each t in T, find the value of f(t).

To help you reason, you can make two types of queries (with limited query budget):

1. **Value Query** (Jurisprudential Origin Search): Ask for the direct higher-level legal basis f(x) of a non-target provision x.
   - Constraint: x must be in the range {{1, ..., {N}}}, and x cannot be a target provision (i.e., x not in T).
   - Answer: Returns the specific value of f(x).
   - Budget: You can make at most {L} value queries.

2. **Equality Query** (Legal Application Verification): Ask whether the direct higher-level legal basis of provision x equals y.
   - Constraint: x must be in the range {{1, ..., {N}}}, y must be in the range {{0, ..., x-1}}.
   - Answer: Answers "Yes" or "No".
   - Budget: You can make at most {M} equality queries.

When you have collected enough information, submit your final answer. The answer must include the direct higher-level legal basis values for all provisions in the target set T.

## Query and Answer Format

You can only submit one query or answer at a time. Use the following XML format:

- Value Query (e.g., query the direct higher-level legal basis of legal provision 5):
<query_value>5</query_value>

- Equality Query (e.g., ask if the direct higher-level legal basis of legal provision 7 is 3):
<query_equal>7,3</query_equal>

- Submit Final Answer (format as "legal provision=direct higher-level legal basis" list, separated by semicolons):
<answer>8=4;12=6;15=7</answer>

Note: The answer must include all legal provisions in the target set T, with strict adherence to the format above.
"""

    tags = ["answer", "query_value", "query_equal"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"N": 10, "rule": "div2", "target_nodes": [8], "L": 6, "M": 3},
            2: {"N": 15, "rule": "div2", "target_nodes": [12, 14], "L": 8, "M": 4},
            3: {"N": 20, "rule": "div3", "target_nodes": [15, 18], "L": 10, "M": 5},
            4: {"N": 30, "rule": "digit_sum", "target_nodes": [20, 25, 28], "L": 12, "M": 6},
            5: {"N": 50, "rule": "popcount", "target_nodes": [35, 42, 47], "L": 15, "M": 8},
        },
        "en": {
            1: {"N": 10, "rule": "div2", "target_nodes": [8], "L": 6, "M": 3},
            2: {"N": 15, "rule": "div2", "target_nodes": [12, 14], "L": 8, "M": 4},
            3: {"N": 20, "rule": "div3", "target_nodes": [15, 18], "L": 10, "M": 5},
            4: {"N": 30, "rule": "digit_sum", "target_nodes": [20, 25, 28], "L": 12, "M": 6},
            5: {"N": 50, "rule": "popcount", "target_nodes": [35, 42, 47], "L": 15, "M": 8},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：根据难度配置设定父函数规则、目标节点、查询预算等"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.N = cfg["N"]
        self.rule_type = cfg["rule"]
        self.target_nodes = set(cfg["target_nodes"])
        self.L = cfg["L"]  # 值查询预算
        self.M = cfg["M"]  # 等式查询预算

        # 初始化查询计数器
        self.value_query_count = 0
        self.equal_query_count = 0

        # 预计算父函数 f(i) for i in [1, N]
        self.parent_function = {}
        for i in range(1, self.N + 1):
            self.parent_function[i] = self._compute_parent(i)

        # 设置游戏信息用于格式化规则文本
        self._game_info["N"] = self.N
        self._game_info["target_nodes"] = ", ".join(map(str, sorted(self.target_nodes)))
        self._game_info["L"] = self.L
        self._game_info["M"] = self.M

    def _compute_parent(self, i):
        """根据规则类型计算节点 i 的父节点"""
        if self.rule_type == "div2":
            return i // 2
        elif self.rule_type == "div3":
            return i // 3
        elif self.rule_type == "digit_sum":
            # f(i) = i - 各位数字和
            digit_sum = sum(int(d) for d in str(i))
            result = i - digit_sum
            return max(0, result)  # 确保非负
        elif self.rule_type == "popcount":
            # f(i) = i - 二进制中1的个数
            popcount = bin(i).count('1')
            result = i - popcount
            return max(0, result)
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析答案格式：node1=parent1;node2=parent2;...
        try:
            pairs = [p.strip() for p in raw_ans.split(";") if p.strip()]
            answer_dict = {}
            for pair in pairs:
                if "=" not in pair:
                    return False
                node_str, parent_str = pair.split("=", 1)
                node = int(node_str.strip())
                parent = int(parent_str.strip())
                answer_dict[node] = parent
        except:
            return False

        # 检查是否包含所有目标节点
        if set(answer_dict.keys()) != self.target_nodes:
            return False

        # 检查每个目标节点的父节点是否正确
        for node in self.target_nodes:
            if answer_dict[node] != self.parent_function[node]:
                return False

        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效。"
            error_range = "错误：节点编号超出范围。"
            error_target = "错误：不能对目标节点进行值查询。"
            error_budget_value = "错误：值查询次数已用尽。"
            error_budget_equal = "错误：等式查询次数已用尽。"
            error_constraint = "错误：y 必须在 [0, x-1] 范围内。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format."
            error_range = "Error: Node ID out of range."
            error_target = "Error: Cannot perform value query on target nodes."
            error_budget_value = "Error: Value query budget exhausted."
            error_budget_equal = "Error: Equality query budget exhausted."
            error_constraint = "Error: y must be in range [0, x-1]."

        # 处理值查询
        if "query_value" in parsed_info:
            if self.value_query_count >= self.L:
                return error_budget_value
            
            try:
                x = int(parsed_info["query_value"].strip())
            except:
                return error_format

            if x < 1 or x > self.N:
                return error_range
            if x in self.target_nodes:
                return error_target

            self.value_query_count += 1
            return str(self.parent_function[x])

        # 处理等式查询
        elif "query_equal" in parsed_info:
            if self.equal_query_count >= self.M:
                return error_budget_equal

            try:
                raw = parsed_info["query_equal"].strip()
                x_str, y_str = raw.split(",")
                x = int(x_str.strip())
                y = int(y_str.strip())
            except:
                return error_format

            if x < 1 or x > self.N:
                return error_range
            if y < 0 or y >= x:
                return error_constraint

            self.equal_query_count += 1
            return yes_res if self.parent_function[x] == y else no_res

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """
        将正确的查询响应篡改为错误值，用于反事实干预模式。
        """
        if correct.startswith("Error:") or correct.startswith("错误："):
            return correct

        try:
            correct_val = int(correct)
            # 对数值型答案进行偏移
            if correct_val == 0:
                return str(correct_val + 1)
            else:
                return str(correct_val - 1)
        except ValueError:
            # 对 Yes/No 或 是/否 类型的答案取反
            if correct in ("Yes", "yes"):
                return "No"
            elif correct in ("No", "no"):
                return "Yes"
            elif correct == "是":
                return "否"
            elif correct == "否":
                return "是"
            else:
                return correct + " [WRONG]"

    def get_all_possible_queries(self) -> List[Dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        为避免查询数量爆炸，等式查询仅枚举目标节点相关的查询。
        """
        queries = []
        
        # 确定语言相关的回答
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        # 1. 枚举所有合法的值查询 (Value Query)
        # 约束：x 在 [1, N] 且 x 不在 target_nodes 中
        for x in range(1, self.N + 1):
            if x not in self.target_nodes:
                # 计算正确答案
                ans = str(self.parent_function[x])
                
                queries.append({
                    "query": f"<query_value>{x}</query_value>",
                    "answer": ans
                })

        # 2. 仅枚举目标节点的等式查询 (Equality Query)，避免 O(N^2) 爆炸
        for x in sorted(self.target_nodes):
            for y in range(0, x):
                # 计算正确答案
                is_correct = (self.parent_function[x] == y)
                ans = yes_res if is_correct else no_res
                
                queries.append({
                    "query": f"<query_equal>{x},{y}</query_equal>",
                    "answer": ans
                })

        return queries