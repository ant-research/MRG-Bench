from .base import Game
import re


class DirectedGraphNeighborCountGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们来玩一个"有向图邻接计数推理"游戏，规则如下：

游戏设定了一个固定的有向图，节点集合为 V = {{A, B, C, D, E, F}}。
有向边集合为：{edges}。

我已秘密选择了一个邻接计数函数 f，该函数属于以下四种候选定义之一：
1. f1(v) = 出度（从节点 v 出发的边数；自环计为1条出边）
2. f2(v) = 入度（指向节点 v 的边数；自环计为1条入边）
3. f3(v) = 入度 + 出度（自环同时贡献入度和出度，因此贡献2）
4. f4(v) = 忽略方向的相邻不同节点数量（自环不计入）

你的目标是：
1. 推断出真实的邻接计数函数编号 j（1, 2, 3 或 4）
2. 在该函数下找出邻接计数最大的节点 Z；若有多个节点并列最大，选择字母序最小者

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 定量查询：询问某个节点 X 的邻接计数是多少。回答一个整数。
2. 等值查询：询问某个节点 X 的邻接计数是否等于 k。回答"是"或"否"。
3. 比较查询：询问节点 X 与节点 Y 的邻接计数大小关系。回答"X大"、"Y大"或"相等"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 定量查询（例如询问节点 A）：
<query_value>A</query_value>

- 等值查询（例如询问节点 B 的计数是否等于 3）：
<query_equal>B,3</query_equal>

- 比较查询（例如比较节点 C 和节点 D）：
<query_compare>C,D</query_compare>

提交最终答案时，必须说明函数编号（1, 2, 3 或 4）和目标节点（A, B, C, D, E 或 F），格式如下：

<answer>function=2, node=C</answer>
"""

    game_rule_en = """\
Let's play a "Directed Graph Neighbor Count Inference" game. Here are the rules:

The game is based on a fixed directed graph with node set V = {{A, B, C, D, E, F}}.
The directed edge set is: {edges}.

I have secretly selected a neighbor count function f, which is one of the following four candidate definitions:
1. f1(v) = out-degree (number of edges leaving node v; self-loop counts as 1 outgoing edge)
2. f2(v) = in-degree (number of edges pointing to node v; self-loop counts as 1 incoming edge)
3. f3(v) = in-degree + out-degree (self-loop contributes to both in-degree and out-degree, thus contributes 2)
4. f4(v) = number of distinct adjacent nodes ignoring direction (self-loop does not count)

Your goal is to:
1. Infer the true neighbor count function number j (1, 2, 3, or 4)
2. Find the node Z with the maximum count under that function; if multiple nodes tie, choose the one with smallest lexicographic order

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

1. Value Query: Ask for the neighbor count of a node X. Answer an integer.
2. Equality Query: Ask if the neighbor count of node X equals k. Answer "Yes" or "No".
3. Comparison Query: Ask about the relationship between neighbor counts of nodes X and Y. Answer "X larger", "Y larger", or "Equal".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about node A):
<query_value>A</query_value>

- Equality Query (e.g., asking if node B's count equals 3):
<query_equal>B,3</query_equal>

- Comparison Query (e.g., comparing nodes C and D):
<query_compare>C,D</query_compare>

When submitting the final answer, specify the function number (1, 2, 3, or 4) and the target node (A, B, C, D, E, or F), using this format:

<answer>function=2, node=C</answer>
"""

    contextualized_rule_zh_1 = """\
【交通场景：城市交通路网流量评估】
我们来执行一次"城市路网枢纽流量评估"任务，规则如下：

系统设定了一个固定的交通路网，关键枢纽节点集合为 V = {{A, B, C, D, E, F}}。
单向车道集合为：{edges}。
（注意：(D,D) 这类自环表示枢纽内部的循环高架或掉头车道）。

我已秘密选择了一个流量评估模型 f，该模型属于以下四种候选定义之一：
1. f1(v) = 辐射车流量评估（从枢纽 v 驶出的车道数；内部循环计为1条驶出车道）
2. f2(v) = 汇集车流量评估（驶入枢纽 v 的车道数；内部循环计为1条驶入车道）
3. f3(v) = 综合吞吐量评估（驶入 + 驶出车道数，内部循环同时贡献驶入和驶出，因此贡献2）
4. f4(v) = 连通区域广度评估（忽略车道方向的相邻不同枢纽数量，内部循环不计入）

你的目标是：
1. 推断出真实的流量评估模型编号 j（1, 2, 3 或 4）
2. 在该模型下找出评估值最大的枢纽 Z；若有多个枢纽并列最大，选择字母序最小者

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 定量查询：询问某个枢纽 X 的评估值是多少。回答一个整数。
2. 等值查询：询问某个枢纽 X 的评估值是否等于 k。回答"是"或"否"。
3. 比较查询：询问枢纽 X 与枢纽 Y 的评估值大小关系。回答"X大"、"Y大"或"相等"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 定量查询（例如询问枢纽 A）：
<query_value>A</query_value>

- 等值查询（例如询问枢纽 B 的评估值是否等于 3）：
<query_equal>B,3</query_equal>

- 比较查询（例如比较枢纽 C 和枢纽 D）：
<query_compare>C,D</query_compare>

提交最终答案时，必须说明模型编号（1, 2, 3 或 4）和目标枢纽（A, B, C, D, E 或 F），格式如下：

<answer>function=2, node=C</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's perform an "Urban Traffic Hub Flow Evaluation" task. Here are the rules:

The system is based on a fixed traffic network, with the key hub node set V = {{A, B, C, D, E, F}}.
The one-way traffic lane set is: {edges}.
(Note: self-loops like (D,D) represent internal circular overpasses or U-turn lanes within a hub).

I have secretly selected a flow evaluation model f, which is one of the following four candidate definitions:
1. f1(v) = Outbound Traffic Volume (number of lanes leaving hub v; internal loop counts as 1 outbound lane)
2. f2(v) = Inbound Traffic Volume (number of lanes entering hub v; internal loop counts as 1 inbound lane)
3. f3(v) = Overall Throughput (inbound + outbound lanes; internal loop contributes 2)
4. f4(v) = Connected Area Breadth (number of distinct adjacent hubs ignoring direction; internal loop does not count)

Your goal is to:
1. Infer the true evaluation model number j (1, 2, 3, or 4)
2. Find the hub Z with the maximum evaluation value under that model; if multiple hubs tie, choose the one with the smallest lexicographic order

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

1. Value Query: Ask for the evaluation value of a hub X. Answer an integer.
2. Equality Query: Ask if the evaluation value of hub X equals k. Answer "Yes" or "No".
3. Comparison Query: Ask about the relationship between evaluation values of hubs X and Y. Answer "X larger", "Y larger", or "Equal".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about hub A):
<query_value>A</query_value>

- Equality Query (e.g., asking if hub B's value equals 3):
<query_equal>B,3</query_equal>

- Comparison Query (e.g., comparing hubs C and D):
<query_compare>C,D</query_compare>

When submitting the final answer, specify the model number (1, 2, 3, or 4) and the target hub (A, B, C, D, E, or F), using this format:

<answer>function=2, node=C</answer>
"""

    contextualized_rule_zh_2 = """\
【医疗场景：传染病传播溯源与接触者网络分析】
我们来执行一次"传染病接触网络分析"任务，规则如下：

系统设定了一个固定的接触者网络，确诊患者节点集合为 V = {{A, B, C, D, E, F}}。
单向传播路径集合为：{edges}。
（注意：(D,D) 这类自环表示患者自身的不同部位/阶段的二次自我暴露，或环境留存导致的反复感染）。

我已秘密选择了一个风险评估模型 f，该模型属于以下四种候选定义之一：
1. f1(v) = 传染源释放指数（向外传播的次数；二次暴露计为1次向外传播）
2. f2(v) = 易感暴露指数（被感染或接触的次数；二次暴露计为1次被接触）
3. f3(v) = 总体接触频次（入度和出度总和，二次暴露同时贡献入度和出度，因此贡献2）
4. f4(v) = 独立接触人员数量（忽略传播方向的相邻不同患者人数，自我二次暴露不计入）

你的目标是：
1. 推断出真实的风险评估模型编号 j（1, 2, 3 或 4）
2. 在该模型下找出风险指数最大的患者 Z；若有多个患者并列最大，选择字母序最小者

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 定量查询：询问某个患者 X 的风险指数是多少。回答一个整数。
2. 等值查询：询问某个患者 X 的风险指数是否等于 k。回答"是"或"否"。
3. 比较查询：询问患者 X 与患者 Y 的风险指数大小关系。回答"X大"、"Y大"或"相等"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 定量查询（例如询问患者 A）：
<query_value>A</query_value>

- 等值查询（例如询问患者 B 的指数是否等于 3）：
<query_equal>B,3</query_equal>

- 比较查询（例如比较患者 C 和患者 D）：
<query_compare>C,D</query_compare>

提交最终答案时，必须说明模型编号（1, 2, 3 或 4）和目标患者（A, B, C, D, E 或 F），格式如下：

<answer>function=2, node=C</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's perform an "Infectious Disease Contact Network Analysis" task. Here are the rules:

The system is based on a fixed contact network, with the confirmed patient node set V = {{A, B, C, D, E, F}}.
The one-way transmission path set is: {edges}.
(Note: self-loops like (D,D) represent secondary self-exposure or repeated infection from environmental retention).

I have secretly selected a risk assessment model f, which is one of the following four candidate definitions:
1. f1(v) = Infection Source Release Index (number of outward transmission contacts; self-exposure counts as 1 outward transmission)
2. f2(v) = Susceptibility Exposure Index (number of incoming infection sources or contacts; self-exposure counts as 1 incoming contact)
3. f3(v) = Total Contact Frequency (sum of incoming and outward contacts; self-exposure contributes 2)
4. f4(v) = Distinct Contact Individuals (number of distinct adjacent patients ignoring direction; self-exposure does not count)

Your goal is to:
1. Infer the true risk assessment model number j (1, 2, 3, or 4)
2. Find the patient Z with the maximum risk index under that model; if multiple patients tie, choose the one with the smallest lexicographic order

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

1. Value Query: Ask for the risk index of patient X. Answer an integer.
2. Equality Query: Ask if the risk index of patient X equals k. Answer "Yes" or "No".
3. Comparison Query: Ask about the relationship between risk indices of patients X and Y. Answer "X larger", "Y larger", or "Equal".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about patient A):
<query_value>A</query_value>

- Equality Query (e.g., asking if patient B's index equals 3):
<query_equal>B,3</query_equal>

- Comparison Query (e.g., comparing patients C and D):
<query_compare>C,D</query_compare>

When submitting the final answer, specify the model number (1, 2, 3, or 4) and the target patient (A, B, C, D, E, or F), using this format:

<answer>function=2, node=C</answer>
"""

    contextualized_rule_zh_3 = """\
【教育场景：学生知识点掌握情况的前置依赖分析】
我们来执行一次"知识模块依赖度分析"任务，规则如下：

系统设定了一个固定的知识大纲网络，核心知识模块节点集合为 V = {{A, B, C, D, E, F}}。
单向先修依赖关系集合为（(u,v)表示学完u才能学v）：{edges}。
（注意：(D,D) 这类自环表示该模块需要内部的多阶段复习循环）。

我已秘密选择了一个关联度评估标准 f，该标准属于以下四种候选定义之一：
1. f1(v) = 知识点基础辐射度（作为前置条件的路径数；内部复习计为1个前置辐射）
2. f2(v) = 知识点学习门槛（需要掌握的前置条件路径数；内部复习计为1个学习门槛）
3. f3(v) = 综合学习关联度（前置与后置路径数总和，内部复习同时贡献前置和后置，因此贡献2）
4. f4(v) = 跨模块知识面覆盖（相邻的不同知识模块数量，内部复习不计入）

你的目标是：
1. 推断出教学大纲真实采用的评估标准编号 j（1, 2, 3 或 4）
2. 在该标准下找出关联度最大的知识模块 Z；若有多个模块并列最大，选择字母序最小者

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 定量查询：询问某个模块 X 的关联度是多少。回答一个整数。
2. 等值查询：询问某个模块 X 的关联度是否等于 k。回答"是"或"否"。
3. 比较查询：询问模块 X 与模块 Y 的关联度大小关系。回答"X大"、"Y大"或"相等"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 定量查询（例如询问模块 A）：
<query_value>A</query_value>

- 等值查询（例如询问模块 B 的关联度是否等于 3）：
<query_equal>B,3</query_equal>

- 比较查询（例如比较模块 C 和模块 D）：
<query_compare>C,D</query_compare>

提交最终答案时，必须说明标准编号（1, 2, 3 或 4）和目标模块（A, B, C, D, E 或 F），格式如下：

<answer>function=2, node=C</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's perform a "Knowledge Module Dependency Analysis" task. Here are the rules:

The system is based on a fixed curriculum network, with the core knowledge module node set V = {{A, B, C, D, E, F}}.
The one-way prerequisite dependency set (where (u,v) means u must be learned before v) is: {edges}.
(Note: self-loops like (D,D) represent multi-stage review cycles within a module).

I have secretly selected an association evaluation standard f, which is one of the following four candidate definitions:
1. f1(v) = Foundational Radiance (number of outgoing prerequisite paths; internal review counts as 1 outgoing path)
2. f2(v) = Learning Threshold (number of incoming prerequisite paths; internal review counts as 1 learning threshold)
3. f3(v) = Comprehensive Learning Association (sum of incoming and outgoing paths; internal review contributes 2)
4. f4(v) = Cross-Module Knowledge Coverage (number of distinct adjacent modules ignoring direction; internal review does not count)

Your goal is to:
1. Infer the true evaluation standard number j (1, 2, 3, or 4)
2. Find the module Z with the maximum association value under that standard; if multiple modules tie, choose the one with the smallest lexicographic order

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

1. Value Query: Ask for the association value of module X. Answer an integer.
2. Equality Query: Ask if the association value of module X equals k. Answer "Yes" or "No".
3. Comparison Query: Ask about the relationship between association values of modules X and Y. Answer "X larger", "Y larger", or "Equal".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about module A):
<query_value>A</query_value>

- Equality Query (e.g., asking if module B's value equals 3):
<query_equal>B,3</query_equal>

- Comparison Query (e.g., comparing modules C and D):
<query_compare>C,D</query_compare>

When submitting the final answer, specify the standard number (1, 2, 3, or 4) and the target module (A, B, C, D, E, or F), using this format:

<answer>function=2, node=C</answer>
"""

    contextualized_rule_zh_4 = """\
【制造业/工业场景：工厂流水线物料流转网络优化】
我们来执行一次"车间物料流转产能评估"任务，规则如下：

系统设定了一个固定的车间物流网络，生产车间节点集合为 V = {{A, B, C, D, E, F}}。
单向物料输送带集合为：{edges}。
（注意：(D,D) 这类自环表示车间内部的返工或循环工序）。

我已秘密选择了一个产能评估指标 f，该指标属于以下四种候选定义之一：
1. f1(v) = 物料产出负荷（向外输送的工序流向数；内部循环计为1个流向）
2. f2(v) = 物料接收压力（接收物料的工序来源数；内部循环计为1个来源）
3. f3(v) = 车间综合运转吞吐（接收和输出的工序流向总和，内部循环同时贡献接收和输出，因此贡献2）
4. f4(v) = 协作车间数量（与之有物流往来的不同车间总数，内部循环不计入）

你的目标是：
1. 推断出系统真实采用的产能评估指标编号 j（1, 2, 3 或 4）
2. 在该指标下找出评估值最大的车间 Z；若有多个车间并列最大，选择字母序最小者

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 定量查询：询问某个车间 X 的评估值是多少。回答一个整数。
2. 等值查询：询问某个车间 X 的评估值是否等于 k。回答"是"或"否"。
3. 比较查询：询问车间 X 与车间 Y 的评估值大小关系。回答"X大"、"Y大"或"相等"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 定量查询（例如询问车间 A）：
<query_value>A</query_value>

- 等值查询（例如询问车间 B 的评估值是否等于 3）：
<query_equal>B,3</query_equal>

- 比较查询（例如比较车间 C 和车间 D）：
<query_compare>C,D</query_compare>

提交最终答案时，必须说明指标编号（1, 2, 3 或 4）和目标车间（A, B, C, D, E 或 F），格式如下：

<answer>function=2, node=C</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's perform a "Workshop Material Flow Capacity Evaluation" task. Here are the rules:

The system is based on a fixed logistics network, with the production workshop node set V = {{A, B, C, D, E, F}}.
The one-way material conveyor belt set is: {edges}.
(Note: self-loops like (D,D) represent internal rework or cyclic processes within a workshop).

I have secretly selected a capacity assessment metric f, which is one of the following four candidate definitions:
1. f1(v) = Material Output Load (number of outward conveying flows; internal cycle counts as 1 outward flow)
2. f2(v) = Material Receiving Pressure (number of incoming conveying sources; internal cycle counts as 1 incoming source)
3. f3(v) = Overall Workshop Throughput (sum of incoming and outward flows; internal cycle contributes 2)
4. f4(v) = Collaborative Workshop Count (number of distinct collaborative workshops ignoring direction; internal cycle does not count)

Your goal is to:
1. Infer the true assessment metric number j (1, 2, 3, or 4)
2. Find the workshop Z with the maximum assessment value under that metric; if multiple workshops tie, choose the one with the smallest lexicographic order

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

1. Value Query: Ask for the assessment value of workshop X. Answer an integer.
2. Equality Query: Ask if the assessment value of workshop X equals k. Answer "Yes" or "No".
3. Comparison Query: Ask about the relationship between assessment values of workshops X and Y. Answer "X larger", "Y larger", or "Equal".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about workshop A):
<query_value>A</query_value>

- Equality Query (e.g., asking if workshop B's value equals 3):
<query_equal>B,3</query_equal>

- Comparison Query (e.g., comparing workshops C and D):
<query_compare>C,D</query_compare>

When submitting the final answer, specify the metric number (1, 2, 3, or 4) and the target workshop (A, B, C, D, E, or F), using this format:

<answer>function=2, node=C</answer>
"""

    contextualized_rule_zh_5 = """\
【法律场景：复杂商业纠纷中的资金转移及证据链追踪】
我们来执行一次"资金转移网络审计"任务，规则如下：

系统设定了一个固定的资金转账网络，涉案主体节点集合为 V = {{A, B, C, D, E, F}}。
单向资金汇款记录集合为：{edges}。
（注意：(D,D) 这类自环表示主体内部不同账户间的转移/洗钱操作）。

我已秘密选择了一个洗钱嫌疑评估算法 f，该算法属于以下四种候选定义之一：
1. f1(v) = 资金流出活跃度（汇出资金的笔数；内部转移计为1笔汇出）
2. f2(v) = 资金汇入归集度（收到汇款的笔数；内部转移计为1笔汇入）
3. f3(v) = 账户整体交易频率（汇入和汇出的总笔数，内部转移同时贡献汇入和汇出，因此贡献2）
4. f4(v) = 实际交易对手方数量（有资金往来的不同涉案主体数，自身转账不计入）

你的目标是：
1. 推断出审计部门真实采用的评估算法编号 j（1, 2, 3 或 4）
2. 在该算法下找出嫌疑评估值最大的涉案主体 Z；若有多个主体并列最大，选择字母序最小者

你可以反复向我提出以下三类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 定量查询：询问某个主体 X 的评估值是多少。回答一个整数。
2. 等值查询：询问某个主体 X 的评估值是否等于 k。回答"是"或"否"。
3. 比较查询：询问主体 X 与主体 Y 的评估值大小关系。回答"X大"、"Y大"或"相等"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 定量查询（例如询问主体 A）：
<query_value>A</query_value>

- 等值查询（例如询问主体 B 的评估值是否等于 3）：
<query_equal>B,3</query_equal>

- 比较查询（例如比较主体 C 和主体 D）：
<query_compare>C,D</query_compare>

提交最终答案时，必须说明算法编号（1, 2, 3 或 4）和目标涉案主体（A, B, C, D, E 或 F），格式如下：

<answer>function=2, node=C</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's perform a "Fund Transfer Network Audit" task. Here are the rules:

The system is based on a fixed fund transfer network, with the involved subject node set V = {{A, B, C, D, E, F}}.
The one-way fund remittance record set is: {edges}.
(Note: self-loops like (D,D) represent internal transfers or money laundering between accounts of the same subject).

I have secretly selected a money laundering assessment algorithm f, which is one of the following four candidate definitions:
1. f1(v) = Fund Outflow Activity (number of outward remittances; internal transfer counts as 1 outward remittance)
2. f2(v) = Fund Inflow Concentration (number of received remittances; internal transfer counts as 1 incoming remittance)
3. f3(v) = Overall Account Transaction Frequency (sum of inbound and outbound remittances; internal transfer contributes 2)
4. f4(v) = Distinct Counterparty Count (number of distinct entities involved in transactions ignoring direction; internal transfer does not count)

Your goal is to:
1. Infer the true assessment algorithm number j (1, 2, 3, or 4)
2. Find the subject Z with the maximum assessment value under that algorithm; if multiple subjects tie, choose the one with the smallest lexicographic order

You can repeatedly ask me three types of questions (one per turn), and I will answer truthfully:

1. Value Query: Ask for the assessment value of subject X. Answer an integer.
2. Equality Query: Ask if the assessment value of subject X equals k. Answer "Yes" or "No".
3. Comparison Query: Ask about the relationship between assessment values of subjects X and Y. Answer "X larger", "Y larger", or "Equal".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the task is a failure.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., asking about subject A):
<query_value>A</query_value>

- Equality Query (e.g., asking if subject B's value equals 3):
<query_equal>B,3</query_equal>

- Comparison Query (e.g., comparing subjects C and D):
<query_compare>C,D</query_compare>

When submitting the final answer, specify the algorithm number (1, 2, 3, or 4) and the target subject (A, B, C, D, E, or F), using this format:

<answer>function=2, node=C</answer>
"""

    tags = ["answer", "query_value", "query_equal", "query_compare"]

    # 难度配置：通过限制可见的边集合来调整难度
    # 难度越高，图的结构越复杂，推理难度越大
    DIFFICULTY_CONFIG = {
        1: {  # 简单：较小的图，明显的差异
            "edges": [
                ("A", "B"), ("A", "C"),
                ("B", "C"),
                ("C", "A")
            ],
            "description": "小规模图，4条边，容易区分不同函数"
        },
        2: {  # 中等偏下：增加一些边和自环
            "edges": [
                ("A", "B"), ("A", "C"),
                ("B", "C"), ("B", "A"),
                ("C", "A"), ("C", "D"),
                ("D", "D")
            ],
            "description": "包含自环，7条边"
        },
        3: {  # 中等偏上：更多的边
            "edges": [
                ("A", "B"), ("A", "C"),
                ("B", "C"), ("B", "E"), ("B", "A"),
                ("C", "A"), ("C", "D"),
                ("D", "B"), ("D", "D"),
                ("E", "D")
            ],
            "description": "10条边，有自环和多个高度节点"
        },
        4: {  # 较难：接近完整图
            "edges": [
                ("A", "B"), ("A", "C"),
                ("B", "C"), ("B", "E"), ("B", "A"),
                ("C", "A"), ("C", "D"), ("C", "E"),
                ("D", "B"), ("D", "D"),
                ("E", "D"), ("E", "F"),
                ("F", "C")
            ],
            "description": "13条边，结构较复杂"
        },
        5: {  # 难：完整图（题目中的完整边集）
            "edges": [
                ("A", "B"), ("A", "C"),
                ("B", "C"), ("B", "E"), ("B", "A"),
                ("C", "A"), ("C", "D"), ("C", "E"),
                ("D", "B"), ("D", "D"),
                ("E", "D"), ("E", "F"),
                ("F", "C"), ("F", "A")
            ],
            "description": "完整的14条边，最复杂"
        }
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化图结构和计数函数"""
        import hashlib
        diff = int(self.config.difficulty)
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        # 获取当前难度的边集
        self.edges = self.DIFFICULTY_CONFIG[diff]["edges"]
        self.nodes = ["A", "B", "C", "D", "E", "F"]
        
        # 使用基于边集的确定性哈希来选择函数，确保可重现且覆盖多种函数
        edge_hash = int(hashlib.md5(str(self.edges).encode()).hexdigest(), 16)
        self.true_function = (edge_hash % 4) + 1  # 1, 2, 3, or 4
        
        # 计算所有节点在所有函数下的值
        self._compute_all_counts()
        
        # 确定正确答案
        max_count = max(self.counts[self.true_function].values())
        max_nodes = [node for node in self.nodes if self.counts[self.true_function][node] == max_count]
        self.correct_node = min(max_nodes)
        
        self._game_info["n"] = len(self.nodes)
        
        edge_str = ", ".join(f"({u},{v})" for u, v in self.edges)
        self._game_info["edges"] = edge_str
        self._game_info["edge_count"] = len(self.edges)

    def _compute_all_counts(self):
        """计算所有节点在四种函数下的邻接计数"""
        self.counts = {1: {}, 2: {}, 3: {}, 4: {}}
        
        for node in self.nodes:
            # f1: 出度
            out_degree = sum(1 for u, v in self.edges if u == node)
            self.counts[1][node] = out_degree
            
            # f2: 入度
            in_degree = sum(1 for u, v in self.edges if v == node)
            self.counts[2][node] = in_degree
            
            # f3: 入度 + 出度
            self.counts[3][node] = in_degree + out_degree
            
            # f4: 忽略方向的相邻不同节点数量（自环不计入）
            neighbors = set()
            for u, v in self.edges:
                if u == node and v != node:
                    neighbors.add(v)
                elif v == node and u != node:
                    neighbors.add(u)
            self.counts[4][node] = len(neighbors)

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案: function=X, node=Y
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "function" not in ans_dict or "node" not in ans_dict:
                return False
            
            # 检查函数编号
            try:
                func_num = int(ans_dict["function"])
            except:
                return False
            
            if func_num != self.true_function:
                return False
            
            # 检查节点
            node = ans_dict["node"].upper()
            if node != self.correct_node:
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑：根据查询类型生成响应"""
        lang = self.config.language
        
        # 定量查询
        if "query_value" in parsed_info:
            node = parsed_info["query_value"].strip().upper()
            if node not in self.nodes:
                return "错误：节点不存在。" if lang == "zh" else "Error: Node does not exist."
            return str(self.counts[self.true_function][node])
        
        # 等值查询
        elif "query_equal" in parsed_info:
            try:
                parts = parsed_info["query_equal"].split(",")
                if len(parts) != 2:
                    raise ValueError
                node = parts[0].strip().upper()
                k = int(parts[1].strip())
                
                if node not in self.nodes:
                    return "错误：节点不存在。" if lang == "zh" else "Error: Node does not exist."
                
                result = self.counts[self.true_function][node] == k
                if lang == "zh":
                    return "是" if result else "否"
                else:
                    return "Yes" if result else "No"
            except (ValueError, IndexError):
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
        
        # 比较查询
        elif "query_compare" in parsed_info:
            try:
                parts = parsed_info["query_compare"].split(",")
                if len(parts) != 2:
                    raise ValueError
                node_x = parts[0].strip().upper()
                node_y = parts[1].strip().upper()
                
                if node_x not in self.nodes or node_y not in self.nodes:
                    return "错误：节点不存在。" if lang == "zh" else "Error: Node does not exist."
                
                count_x = self.counts[self.true_function][node_x]
                count_y = self.counts[self.true_function][node_y]
                
                if count_x > count_y:
                    return "X大" if lang == "zh" else "X larger"
                elif count_x < count_y:
                    return "Y大" if lang == "zh" else "Y larger"
                else:
                    return "相等" if lang == "zh" else "Equal"
            except (ValueError, IndexError):
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """根据正确答案生成一个明显不同的错误答案"""
        # 若 correct 是纯整数字符串
        if correct.lstrip('-').isdigit():
            return str(int(correct) + 1)
        
        # 中文是非替换
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        # 中文比较查询替换
        if correct == "X大":
            return "Y大"
        if correct == "Y大":
            return "X大"
        if correct == "相等":
            return "X大"
        
        # 英文 Yes/No 替换（忽略大小写，保持原始大小写风格）
        correct_lower = correct.lower()
        if correct_lower == "yes":
            if correct.isupper(): return "NO"
            if correct.istitle(): return "No"
            return "no"
        if correct_lower == "no":
            if correct.isupper(): return "YES"
            if correct.istitle(): return "Yes"
            return "yes"
            
        # 英文比较查询替换
        if correct == "X larger":
            return "Y larger"
        if correct == "Y larger":
            return "X larger"
        if correct == "Equal":
            return "X larger"
            
        # 若都不匹配
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        
        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 完整的 XML 查询字符串
                "answer": str,   # 对应的正确答案
            }
        """
        queries = []
        lang = self.config.language
        current_counts = self.counts[self.true_function]
        
        # 1. 定量查询 (Value Query)
        # 格式: <query_value>A</query_value>
        for node in self.nodes:
            query_content = f"<query_value>{node}</query_value>"
            ans = str(current_counts[node])
            queries.append({"query": query_content, "answer": ans})

        # 2. 等值查询 (Equality Query)
        # 格式: <query_equal>B,3</query_equal>
        # 只枚举实际出现的值及其附近值，避免数量爆炸
        actual_values = set(current_counts.values())
        test_values = set()
        for v in actual_values:
            test_values.update([max(0, v - 1), v, v + 1])
        
        for node in self.nodes:
            for k in sorted(test_values):
                query_content = f"<query_equal>{node},{k}</query_equal>"
                is_equal = (current_counts[node] == k)
                
                if lang == "zh":
                    ans = "是" if is_equal else "否"
                else:
                    ans = "Yes" if is_equal else "No"
                
                queries.append({"query": query_content, "answer": ans})

        # 3. 比较查询 (Comparison Query)
        # 格式: <query_compare>C,D</query_compare>
        for n1 in self.nodes:
            for n2 in self.nodes:
                if n1 == n2:
                    continue
                query_content = f"<query_compare>{n1},{n2}</query_compare>"
                val1 = current_counts[n1]
                val2 = current_counts[n2]
                
                if val1 > val2:
                    ans = "X大" if lang == "zh" else "X larger"
                elif val1 < val2:
                    ans = "Y大" if lang == "zh" else "Y larger"
                else:
                    ans = "相等" if lang == "zh" else "Equal"
                
                queries.append({"query": query_content, "answer": ans})
                
        return queries