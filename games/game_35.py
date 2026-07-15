from .base import Game
import re

class GraphReachabilityGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "图"

    contextualized_rule_zh_1 = """\
欢迎使用“物流运输可达性分析”系统。

系统内记录了一个单向物流运输网络，物流站点集合为 {vertices}，具体的直达运输路线未知。网络中可能存在循环路线，但不包含自我发货。
我已经为你指定了初始发货站点 {start}，你的目标是推理出从该站点出发，货物最终能够送达的所有站点集合。

初始状态下，你已经确认发货站点 {start} 是可达的。

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的运输网络结构如实回答：

1. 邻接枚举查询：询问某个已确认可达站点的所有直接下游站点。
   - 限制：只能查询已确认可达的站点。
   - 回答：列出该站点的所有直接下游站点。

2. 边存在性查询：询问从某个已确认可达站点到另一站点是否存在直达路线。
   - 限制：起点必须是已确认可达的站点。
   - 回答："是"或"否"。

3. 路径验证查询：询问给定的站点序列是否构成从发货站点出发的实际运输路径。
   - 限制：序列必须以发货站点 {start} 开头，长度至少为 2，站点可以重复。
   - 回答："是"；或"否，在第 i 段失败"（i 为最小失败段的下标）。

4. 可达集合报告查询：询问当前已确认可达的站点集合。
   - 回答：列出当前所有已确认可达的站点。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，排查任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接枚举查询（例如查询站点 A）：
<query_neighbors>A</query_neighbors>

- 边存在性查询（例如查询从 A 到 B 是否有直达路线）：
<query_edge>A,B</query_edge>

- 路径验证查询（例如验证路线 A->B->C）：
<query_path>A,B,C</query_path>

- 可达集合报告查询：
<query_reachable></query_reachable>

提交最终答案时，请列出所有可达站点（用逗号隔开，顺序不限），格式如下：

<answer>A,B,C</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Logistics Network Reachability" system.

The system records a one-way logistics transport network with the station set {vertices}. The exact direct transport routes are unknown. The network may contain circular routes but no self-shipping.
I have designated an initial dispatch station {start} for you. Your goal is to infer the set of all stations reachable from this starting station.

Initially, you have confirmed that the starting station {start} is reachable.

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the actual transport network:

1. Neighbor Enumeration Query: Ask for all direct downstream stations of a confirmed reachable station.
   - Restriction: Can only query stations that are confirmed reachable.
   - Answer: List all direct downstream stations.

2. Edge Existence Query: Ask whether there is a direct route from a confirmed reachable station to another.
   - Restriction: The source station must be confirmed reachable.
   - Answer: "Yes" or "No".

3. Path Verification Query: Ask whether a given station sequence forms a valid transport route from the dispatch station.
   - Restriction: The sequence must start with {start}, have length at least 2, and stations can repeat.
   - Answer: "Yes"; or "No, failed at segment i" (i is the index of the first failing segment).

4. Reachable Set Report Query: Ask for the currently confirmed reachable station set.
   - Answer: List all currently confirmed reachable stations.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following XML format:

- Neighbor Enumeration Query (e.g., querying station A):
<query_neighbors>A</query_neighbors>

- Edge Existence Query (e.g., checking if there is a direct route from A to B):
<query_edge>A,B</query_edge>

- Path Verification Query (e.g., verifying route A->B->C):
<query_path>A,B,C</query_path>

- Reachable Set Report Query:
<query_reachable></query_reachable>

When submitting the final answer, list all reachable stations (comma-separated, order does not matter), using this format:

<answer>A,B,C</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“传染病接触溯源”系统。

系统追踪了一个局部的传染接触网络，涉及人员集合为 {vertices}，具体的直接接触史未知。网络中可能存在交叉接触，但不包含自我传染。
我已经为你指定了确认感染的零号病人 {start}，你的目标是推理出从该病人出发，可能被直接或间接传染的所有人员集合。

初始状态下，你已经确认零号病人 {start} 在感染名单中。

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的流行病学调查数据如实回答：

1. 邻接枚举查询：询问某个已确认感染人员的所有直接接触者。
   - 限制：只能查询已确认在感染名单中的人员。
   - 回答：列出该人员的所有直接接触者。

2. 边存在性查询：询问从某个已确认感染人员到另一人员是否存在直接接触史。
   - 限制：起点必须是已确认在感染名单中的人员。
   - 回答："是"或"否"。

3. 路径验证查询：询问给定的人员序列是否构成从零号病人出发的有效传播链。
   - 限制：序列必须以零号病人 {start} 开头，长度至少为 2，人员可以重复（如重复暴露）。
   - 回答："是"；或"否，在第 i 段失败"（i 为最小失败段的下标）。

4. 可达集合报告查询：询问当前已确认在感染名单中的人员集合。
   - 回答：列出当前所有已确认感染的人员。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，溯源任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接枚举查询（例如查询人员 A）：
<query_neighbors>A</query_neighbors>

- 边存在性查询（例如查询 A 是否直接接触了 B）：
<query_edge>A,B</query_edge>

- 路径验证查询（例如验证传播链 A->B->C）：
<query_path>A,B,C</query_path>

- 可达集合报告查询：
<query_reachable></query_reachable>

提交最终答案时，请列出所有可能被传染的人员（用逗号隔开，顺序不限），格式如下：

<answer>A,B,C</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Infectious Disease Contact Tracing" system.

The system tracks a localized transmission network involving the person set {vertices}. The exact direct contact history is unknown. Cross-contacts may exist, but self-infection is not included.
I have designated the confirmed Patient Zero {start} for you. Your goal is to infer the set of all persons who might have been directly or indirectly infected originating from this patient.

Initially, you have confirmed that Patient Zero {start} is in the infected list.

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on actual epidemiological investigation data:

1. Neighbor Enumeration Query: Ask for all direct contacts of a confirmed infected person.
   - Restriction: Can only query persons confirmed to be in the infected list.
   - Answer: List all direct contacts.

2. Edge Existence Query: Ask whether there is a direct contact history from a confirmed infected person to another.
   - Restriction: The source person must be confirmed infected.
   - Answer: "Yes" or "No".

3. Path Verification Query: Ask whether a given person sequence forms a valid transmission chain from Patient Zero.
   - Restriction: The sequence must start with {start}, have length at least 2, and persons can repeat (e.g., repeated exposure).
   - Answer: "Yes"; or "No, failed at segment i" (i is the index of the first failing segment).

4. Reachable Set Report Query: Ask for the currently confirmed infected person set.
   - Answer: List all currently confirmed infected persons.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the tracing task fails.

Each query must contain only one tag. Use the following XML format:

- Neighbor Enumeration Query (e.g., querying person A):
<query_neighbors>A</query_neighbors>

- Edge Existence Query (e.g., checking direct contact from A to B):
<query_edge>A,B</query_edge>

- Path Verification Query (e.g., verifying chain A->B->C):
<query_path>A,B,C</query_path>

- Reachable Set Report Query:
<query_reachable></query_reachable>

When submitting the final answer, list all potentially infected persons (comma-separated, order does not matter), using this format:

<answer>A,B,C</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“课程先修图谱解锁”系统。

系统设定了一个完整的学科知识图谱，课程模块集合为 {vertices}，具体的先修依赖关系未知。模块间可能存在循环依赖（如进阶互修），但不存在自我依赖。
我已经为你分配了初始必修课 {start}，你的目标是推理出只要完成该必修课，后续能够直接或间接解锁的所有课程模块集合。

初始状态下，你已经确认必修课 {start} 是已解锁的。

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的教学大纲依赖结构如实回答：

1. 邻接枚举查询：询问某个已解锁课程的所有直接后续课程（即以此为唯一先决条件的课程）。
   - 限制：只能查询已确认解锁的课程。
   - 回答：列出该课程的所有直接后续课程。

2. 边存在性查询：询问从某个已解锁课程到另一课程是否存在直接先修依赖。
   - 限制：起点必须是已确认解锁的课程。
   - 回答："是"或"否"。

3. 路径验证查询：询问给定的课程序列是否构成从初始必修课出发的有效学习进阶路线。
   - 限制：序列必须以初始必修课 {start} 开头，长度至少为 2，课程可以重复（如复习重修）。
   - 回答："是"；或"否，在第 i 段失败"（i 为最小进阶失败段的下标）。

4. 可达集合报告查询：询问当前已确认解锁的课程模块集合。
   - 回答：列出当前所有已确认解锁的课程。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，规划任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接枚举查询（例如查询课程 A）：
<query_neighbors>A</query_neighbors>

- 边存在性查询（例如查询 A 是否是 B 的直接先修课）：
<query_edge>A,B</query_edge>

- 路径验证查询（例如验证路线 A->B->C）：
<query_path>A,B,C</query_path>

- 可达集合报告查询：
<query_reachable></query_reachable>

提交最终答案时，请列出所有可解锁的课程模块（用逗号隔开，顺序不限），格式如下：

<answer>A,B,C</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Course Prerequisite Graph" system.

The system features a complete academic knowledge graph with the course module set {vertices}. The exact prerequisite dependencies are unknown. Circular dependencies may exist (e.g., advanced co-requisites), but self-dependencies do not.
I have assigned an initial required course {start} for you. Your goal is to infer the set of all course modules that can be directly or indirectly unlocked after completing this initial course.

Initially, you have confirmed that the required course {start} is unlocked.

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the actual syllabus dependency structure:

1. Neighbor Enumeration Query: Ask for all direct subsequent courses of a confirmed unlocked course (i.e., courses that have it as their sole prerequisite).
   - Restriction: Can only query courses that are confirmed unlocked.
   - Answer: List all direct subsequent courses.

2. Edge Existence Query: Ask whether there is a direct prerequisite dependency from a confirmed unlocked course to another.
   - Restriction: The source course must be confirmed unlocked.
   - Answer: "Yes" or "No".

3. Path Verification Query: Ask whether a given course sequence forms a valid learning progression route from the initial required course.
   - Restriction: The sequence must start with {start}, have length at least 2, and courses can repeat (e.g., retaking for review).
   - Answer: "Yes"; or "No, failed at segment i" (i is the index of the first failing progression segment).

4. Reachable Set Report Query: Ask for the currently confirmed unlocked course set.
   - Answer: List all currently confirmed unlocked courses.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the planning task fails.

Each query must contain only one tag. Use the following XML format:

- Neighbor Enumeration Query (e.g., querying course A):
<query_neighbors>A</query_neighbors>

- Edge Existence Query (e.g., checking if A is a direct prerequisite for B):
<query_edge>A,B</query_edge>

- Path Verification Query (e.g., verifying route A->B->C):
<query_path>A,B,C</query_path>

- Reachable Set Report Query:
<query_reachable></query_reachable>

When submitting the final answer, list all unlockable course modules (comma-separated, order does not matter), using this format:

<answer>A,B,C</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业流水线物料追踪”系统。

系统映射了一个复杂的工厂物料流转网络，加工单元集合为 {vertices}，具体的传送带连接状况未知。流转网络中可能存在物料回流，但不包含原地静止加工。
我已经为你指定了物料的初始投料口 {start}，你的目标是推理出从该投料口投入物料后，能够流经的所有加工单元集合。

初始状态下，你已经确认初始投料口 {start} 接收了物料。

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的厂区管网结构如实回答：

1. 邻接枚举查询：询问某个已确认接收物料单元的所有直接下游单元。
   - 限制：只能查询已确认接收物料的单元。
   - 回答：列出该单元的所有直接下游加工单元。

2. 边存在性查询：询问从某个已确认接收物料的单元到另一单元是否存在直接流转链路。
   - 限制：起点必须是已确认接收物料的单元。
   - 回答："是"或"否"。

3. 路径验证查询：询问给定的加工单元序列是否构成从投料口出发的实际物料流转路径。
   - 限制：序列必须以投料口 {start} 开头，长度至少为 2，单元可以重复（如回炉重造）。
   - 回答："是"；或"否，在第 i 段失败"（i 为最小流转中断段的下标）。

4. 可达集合报告查询：询问当前已确认接收到物料的加工单元集合。
   - 回答：列出当前所有已确认接收物料的单元。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，追踪任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接枚举查询（例如查询加工单元 A）：
<query_neighbors>A</query_neighbors>

- 边存在性查询（例如查询从单元 A 到 B 是否有传送带直接连接）：
<query_edge>A,B</query_edge>

- 路径验证查询（例如验证流转路径 A->B->C）：
<query_path>A,B,C</query_path>

- 可达集合报告查询：
<query_reachable></query_reachable>

提交最终答案时，请列出所有物料可达的加工单元（用逗号隔开，顺序不限），格式如下：

<answer>A,B,C</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Assembly Line Tracking" system.

The system maps a complex factory material flow network with the processing unit set {vertices}. The exact conveyor belt connections are unknown. Material backflow may exist in the network, but strictly stationary processing is not included.
I have designated the initial feed port {start} for you. Your goal is to infer the set of all processing units that the material can flow through starting from this feed port.

Initially, you have confirmed that the feed port {start} has received material.

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the actual plant piping and routing structure:

1. Neighbor Enumeration Query: Ask for all direct downstream units of a confirmed material-receiving unit.
   - Restriction: Can only query units that are confirmed to have received material.
   - Answer: List all direct downstream processing units.

2. Edge Existence Query: Ask whether there is a direct transfer link from a confirmed material-receiving unit to another.
   - Restriction: The source unit must be confirmed to have received material.
   - Answer: "Yes" or "No".

3. Path Verification Query: Ask whether a given sequence of processing units forms a valid material flow path from the feed port.
   - Restriction: The sequence must start with {start}, have length at least 2, and units can repeat (e.g., sent back for reprocessing).
   - Answer: "Yes"; or "No, failed at segment i" (i is the index of the first failing transfer segment).

4. Reachable Set Report Query: Ask for the currently confirmed material-receiving processing unit set.
   - Answer: List all units currently confirmed to have received material.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the tracking task fails.

Each query must contain only one tag. Use the following XML format:

- Neighbor Enumeration Query (e.g., querying processing unit A):
<query_neighbors>A</query_neighbors>

- Edge Existence Query (e.g., checking for a direct conveyor link from A to B):
<query_edge>A,B</query_edge>

- Path Verification Query (e.g., verifying flow path A->B->C):
<query_path>A,B,C</query_path>

- Reachable Set Report Query:
<query_reachable></query_reachable>

When submitting the final answer, list all reachable processing units (comma-separated, order does not matter), using this format:

<answer>A,B,C</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“涉案资金流向追踪”系统。

系统锁定了一个地下洗钱资金网络，涉案账户集合为 {vertices}，具体的转账流水明细未知。资金流转可能存在闭环洗钱特征，但不包含账户内自我转账。
我已经为你标记了资金源头的核心嫌疑账户 {start}，你的目标是推理出从该核心账户流出的资金，最终能够流入的所有涉案账户集合。

初始状态下，你已经确认核心嫌疑账户 {start} 持有涉案资金。

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的银行侦查流水数据如实回答：

1. 邻接枚举查询：询问某个已确认持有涉案资金账户的所有直接收款账户。
   - 限制：只能查询已确认持有涉案资金的账户。
   - 回答：列出该账户的所有直接收款账户。

2. 边存在性查询：询问从某个已确认持有涉案资金的账户到另一账户是否存在直接转账记录。
   - 限制：起点必须是已确认持有涉案资金的账户。
   - 回答："是"或"否"。

3. 路径验证查询：询问给定的账户序列是否构成从核心账户出发的真实资金链路。
   - 限制：序列必须以核心账户 {start} 开头，长度至少为 2，账户可以重复（如多次过账循环）。
   - 回答："是"；或"否，在第 i 段失败"（i 为最小链路中断段的下标）。

4. 可达集合报告查询：询问当前已确认持有涉案资金的账户集合。
   - 回答：列出当前所有已确认持有涉案资金的账户。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，追踪任务失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接枚举查询（例如查询涉案账户 A）：
<query_neighbors>A</query_neighbors>

- 边存在性查询（例如查询账户 A 是否直接转账给账户 B）：
<query_edge>A,B</query_edge>

- 路径验证查询（例如验证资金链路 A->B->C）：
<query_path>A,B,C</query_path>

- 可达集合报告查询：
<query_reachable></query_reachable>

提交最终答案时，请列出所有涉案资金流经的账户（用逗号隔开，顺序不限），格式如下：

<answer>A,B,C</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Illicit Fund Flow Tracking" system.

The system has locked onto an underground money laundering network with the suspect account set {vertices}. The exact transaction records are unknown. The fund flow may exhibit closed-loop laundering characteristics, but self-transfers within an account are not included.
I have flagged the core suspect account (fund source) {start} for you. Your goal is to infer the set of all suspect accounts that eventually received funds flowing from this core account.

Initially, you have confirmed that the core suspect account {start} holds the illicit funds.

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on actual bank reconnaissance transaction data:

1. Neighbor Enumeration Query: Ask for all direct payee accounts of an account confirmed to hold illicit funds.
   - Restriction: Can only query accounts confirmed to hold illicit funds.
   - Answer: List all direct payee accounts.

2. Edge Existence Query: Ask whether there is a direct transfer record from an account confirmed to hold illicit funds to another.
   - Restriction: The source account must be confirmed to hold illicit funds.
   - Answer: "Yes" or "No".

3. Path Verification Query: Ask whether a given account sequence forms an actual fund trail starting from the core account.
   - Restriction: The sequence must start with {start}, have length at least 2, and accounts can repeat (e.g., multiple transfer loops).
   - Answer: "Yes"; or "No, failed at segment i" (i is the index of the first broken link segment).

4. Reachable Set Report Query: Ask for the currently confirmed account set holding illicit funds.
   - Answer: List all accounts currently confirmed to hold illicit funds.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the tracking task fails.

Each query must contain only one tag. Use the following XML format:

- Neighbor Enumeration Query (e.g., querying suspect account A):
<query_neighbors>A</query_neighbors>

- Edge Existence Query (e.g., checking if account A directly transferred funds to account B):
<query_edge>A,B</query_edge>

- Path Verification Query (e.g., verifying fund trail A->B->C):
<query_path>A,B,C</query_path>

- Reachable Set Report Query:
<query_reachable></query_reachable>

When submitting the final answer, list all accounts that the illicit funds flowed through (comma-separated, order does not matter), using this format:

<answer>A,B,C</answer>
"""

    game_rule_zh = """\
我们现在来玩一个"图可达性推理"游戏，规则如下：

游戏设定了一个有限有向图，图的顶点集合为 {vertices}，边集合未知。图中可能存在回路，但不包含自环。
我已经为你指定了一个起点 {start}，你的目标是推理出从该起点出发能够到达的所有顶点集合。

初始状态下，你已经确认起点 {start} 是可达的。

你可以反复向我提出以下四类查询（每次仅限一个查询），我会根据真实的图结构如实回答：

1. 邻接枚举查询：询问某个已确认可达顶点的所有直接后继。
   - 限制：只能查询已确认可达的顶点。
   - 回答：列出该顶点的所有直接后继顶点。

2. 边存在性查询：询问从某个已确认可达顶点到另一个顶点是否存在直接边。
   - 限制：起点必须是已确认可达的顶点。
   - 回答："是"或"否"。

3. 路径验证查询：询问给定的顶点序列是否构成从起点出发的可行路径。
   - 限制：序列必须以起点 {start} 开头，长度至少为 2，顶点可以重复。
   - 回答："是"；或"否，在第 i 段失败"（i 为最小失败段的下标）。

4. 可达集合报告查询：询问当前已确认可达的顶点集合。
   - 回答：列出当前所有已确认可达的顶点。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 邻接枚举查询（例如查询顶点 A）：
<query_neighbors>A</query_neighbors>

- 边存在性查询（例如查询从 A 到 B 是否有边）：
<query_edge>A,B</query_edge>

- 路径验证查询（例如验证路径 A->B->C）：
<query_path>A,B,C</query_path>

- 可达集合报告查询：
<query_reachable></query_reachable>

提交最终答案时，请列出所有可达顶点（用逗号隔开，顺序不限），格式如下：

<answer>A,B,C</answer>
"""

    game_rule_en = """\
Let's play a "Graph Reachability Inference" game. Here are the rules:

The game has a finite directed graph with vertex set {vertices}. The edge set is unknown. The graph may contain cycles but no self-loops.
I have designated a starting vertex {start} for you. Your goal is to infer the set of all vertices reachable from this starting vertex.

Initially, you have confirmed that the starting vertex {start} is reachable.

You can repeatedly ask me four types of queries (one per turn), and I will answer truthfully based on the real graph structure:

1. Neighbor Enumeration Query: Ask for all direct successors of a confirmed reachable vertex.
   - Restriction: Can only query vertices that are confirmed reachable.
   - Answer: List all direct successor vertices.

2. Edge Existence Query: Ask whether there is a direct edge from a confirmed reachable vertex to another vertex.
   - Restriction: The source vertex must be confirmed reachable.
   - Answer: "Yes" or "No".

3. Path Verification Query: Ask whether a given vertex sequence forms a valid path from the starting vertex.
   - Restriction: The sequence must start with {start}, have length at least 2, and vertices can repeat.
   - Answer: "Yes"; or "No, failed at segment i" (i is the index of the first failing segment).

4. Reachable Set Report Query: Ask for the currently confirmed reachable vertex set.
   - Answer: List all currently confirmed reachable vertices.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Neighbor Enumeration Query (e.g., querying vertex A):
<query_neighbors>A</query_neighbors>

- Edge Existence Query (e.g., checking if there is an edge from A to B):
<query_edge>A,B</query_edge>

- Path Verification Query (e.g., verifying path A->B->C):
<query_path>A,B,C</query_path>

- Reachable Set Report Query:
<query_reachable></query_reachable>

When submitting the final answer, list all reachable vertices (comma-separated, order does not matter), using this format:

<answer>A,B,C</answer>
"""

    tags = ["answer", "query_neighbors", "query_edge", "query_path", "query_reachable"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "vertices": "A,B,C",
                "start": "A",
                "edges": "A->B,B->C",
            },
            2: {
                "vertices": "A,B,C,D,E",
                "start": "A",
                "edges": "A->B,A->C,B->D,C->D",
            },
            3: {
                "vertices": "A,B,C,D,E,F",
                "start": "A",
                "edges": "A->B,A->C,B->D,C->D,D->E",
            },
            4: {
                "vertices": "A,B,C,D,E,F,G",
                "start": "A",
                "edges": "A->B,B->C,C->B,B->D,D->E,A->F",
            },
            5: {
                "vertices": "A,B,C,D,E,F,G,H",
                "start": "A",
                "edges": "A->B,B->C,C->D,D->B,B->E,E->F,F->E,A->G",
            },
        },
        "en": {
            1: {
                "vertices": "A,B,C",
                "start": "A",
                "edges": "A->B,B->C",
            },
            2: {
                "vertices": "A,B,C,D,E",
                "start": "A",
                "edges": "A->B,A->C,B->D,C->D",
            },
            3: {
                "vertices": "A,B,C,D,E,F",
                "start": "A",
                "edges": "A->B,A->C,B->D,C->D,D->E",
            },
            4: {
                "vertices": "A,B,C,D,E,F,G",
                "start": "A",
                "edges": "A->B,B->C,C->B,B->D,D->E,A->F",
            },
            5: {
                "vertices": "A,B,C,D,E,F,G,H",
                "start": "A",
                "edges": "A->B,B->C,C->D,D->B,B->E,E->F,F->E,A->G",
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
        
        self.vertices = set(v.strip() for v in cfg["vertices"].split(","))
        self._game_info["vertices"] = cfg["vertices"]
        
        self.start = cfg["start"].strip()
        self._game_info["start"] = self.start
        
        self.adjacency = {v: [] for v in self.vertices}
        for edge in cfg["edges"].split(","):
            if "->" in edge:
                src, dst = edge.split("->")
                src, dst = src.strip(), dst.strip()
                if src in self.vertices and dst in self.vertices:
                    self.adjacency[src].append(dst)
        
        self.true_reachable = self._compute_reachable()
        
        self.confirmed_reachable = {self.start}

    def _compute_reachable(self):
        reachable = set()
        queue = [self.start]
        visited = {self.start}
        
        while queue:
            current = queue.pop(0)
            reachable.add(current)
            for neighbor in self.adjacency[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return reachable

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        saved_confirmed = self.confirmed_reachable.copy()
        
        self.confirmed_reachable = self.true_reachable.copy()
        
        try:
            tag = "query_reachable"
            parsed = {tag: ""}
            ans = self._cf_core_produce(parsed)
            queries.append({
                "query": f"<{tag}></{tag}>",
                "answer": ans
            })
            
            sorted_reachable = sorted(list(self.true_reachable))
            sorted_all_vertices = sorted(list(self.vertices))
            
            for v in sorted_reachable:
                tag = "query_neighbors"
                parsed = {tag: v}
                ans = self._cf_core_produce(parsed)
                queries.append({
                    "query": f"<{tag}>{v}</{tag}>",
                    "answer": ans
                })

            for src in sorted_reachable:
                for dst in sorted_all_vertices:
                    if src == dst:
                        continue
                    tag = "query_edge"
                    val = f"{src},{dst}"
                    parsed = {tag: val}
                    ans = self._cf_core_produce(parsed)
                    queries.append({
                        "query": f"<{tag}>{val}</{tag}>",
                        "answer": ans
                    })

        finally:
            self.confirmed_reachable = saved_confirmed
            
        return queries

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        try:
            submitted = set(v.strip() for v in raw_ans.split(",") if v.strip())
            return submitted == self.true_reachable
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_not_reachable = "错误：该顶点尚未确认可达，无法查询。"
            error_invalid_vertex = "错误：顶点不存在。"
            error_invalid_format = "错误：格式无效。"
            error_path_start = "错误：路径必须以起点开头。"
            error_path_length = "错误：路径长度必须至少为2。"
        else:
            yes_res, no_res = "Yes", "No"
            error_not_reachable = "Error: Vertex not confirmed reachable, cannot query."
            error_invalid_vertex = "Error: Vertex does not exist."
            error_invalid_format = "Error: Invalid format."
            error_path_start = "Error: Path must start with the starting vertex."
            error_path_length = "Error: Path length must be at least 2."

        if "query_neighbors" in parsed_info:
            vertex = parsed_info["query_neighbors"].strip()
            
            if vertex not in self.vertices:
                return error_invalid_vertex
            
            if vertex not in self.confirmed_reachable:
                return error_not_reachable
            
            neighbors = self.adjacency[vertex]
            self.confirmed_reachable.update(neighbors)
            
            if not neighbors:
                return "[]" if self.config.language == "en" else "[]"
            return "[" + ",".join(neighbors) + "]"

        elif "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                src, dst = [v.strip() for v in raw.split(",")]
                
                if src not in self.vertices or dst not in self.vertices:
                    return error_invalid_vertex
                
                if src not in self.confirmed_reachable:
                    return error_not_reachable
                
                edge_exists = dst in self.adjacency[src]
                
                if edge_exists:
                    self.confirmed_reachable.add(dst)
                    return yes_res
                else:
                    return no_res
            except:
                return error_invalid_format

        elif "query_path" in parsed_info:
            try:
                raw = parsed_info["query_path"].strip()
                path = [v.strip() for v in raw.split(",")]
                
                if len(path) < 2:
                    return error_path_length
                
                if path[0] != self.start:
                    return error_path_start
                
                for v in path:
                    if v not in self.vertices:
                        return error_invalid_vertex
                
                for i in range(len(path) - 1):
                    src, dst = path[i], path[i + 1]
                    if dst not in self.adjacency[src]:
                        if self.config.language == "zh":
                            return f"否，在第 {i} 段失败"
                        else:
                            return f"No, failed at segment {i}"
                
                self.confirmed_reachable.update(path)
                return yes_res
            except:
                return error_invalid_format

        elif "query_reachable" in parsed_info:
            reachable_list = sorted(list(self.confirmed_reachable))
            return "[" + ",".join(reachable_list) + "]"

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
            
        correct_lower = correct.lower()
        if correct_lower == "yes":
            if correct.istitle(): return "No"
            if correct.isupper(): return "NO"
            return "no"
        if correct_lower == "no":
            if correct.istitle(): return "Yes"
            if correct.isupper(): return "YES"
            return "yes"
        
        if correct.startswith("[") and correct.endswith("]"):
            inner = correct[1:-1].strip()
            if not inner:
                return "[X_FAKE]"
            items = [x.strip() for x in inner.split(",")]
            if len(items) > 1:
                return "[" + ",".join(items[1:]) + "]"
            else:
                return "[" + items[0] + ",X_FAKE]"
        
        import re
        seg_match = re.search(r'(\d+)', correct)
        if seg_match:
            old_num = int(seg_match.group(1))
            new_num = old_num + 1
            return correct.replace(str(old_num), str(new_num), 1)
        
        return f"{correct}_WRONG"