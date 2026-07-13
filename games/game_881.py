# -*- coding: utf-8 -*-
from .base import Game
import re

class DirectedGraphCycleDetectionGame(Game):

    game_rule_zh = """\
我们现在来玩一个"有向图环检测"的推理游戏，规则如下：

游戏设定了一个固定的有向图 G=(V,E)，节点数为 N（未知但可查询），节点以 1 到 N 标号。每个节点 u 有若干出边，出度记为 deg(u)（可能为 0）。每条出边在该节点处有局部端口编号 1 到 deg(u)。从节点 u 通过端口 k 会到达某个节点 v（允许自环）。图在整个游戏过程中保持不变。

你的目标是判定该图是否存在有向环。你可以通过以下查询与系统交互（每次提交一个查询），我会根据真实设定如实回答：

1. 查询节点数：询问图中节点总数 N。
2. 查询出度：询问指定节点 i 的出度。若节点不存在则返回错误。
3. 单步遍历：从节点 i 通过端口 k 走一步，返回到达的节点 j。若节点或端口无效则返回错误。
4. 多步遍历：从指定起点出发，按给定的端口序列连续行走多步。系统会返回访问序列，并在检测到重复节点时立即停止并报告回路信息。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询节点数：
<query_n></query_n>

- 查询出度（例如查询节点 5 的出度）：
<query_degree>5</query_degree>

- 单步遍历（例如从节点 3 通过端口 2 走一步）：
<query_step>3,2</query_step>

- 多步遍历（例如从节点 1 出发，依次通过端口 1,2,1）：
<query_path>start=1,ports=[1,2,1]</query_path>

提交最终判定时，必须说明是否存在环。若判定存在环，可选择性附上一条回路作为证据（用逗号隔开的节点序列，首尾节点相同），格式如下：

- 判定不存在环：
<answer>no_cycle</answer>

- 判定存在环（不提供回路证据）：
<answer>has_cycle</answer>

- 判定存在环（提供回路证据，例如 1->2->3->1）：
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    game_rule_en = """\
Let's play a "Directed Graph Cycle Detection" reasoning game. Here are the rules:

The game features a fixed directed graph G=(V,E) with N nodes (unknown but queryable), labeled 1 to N. Each node u has some outgoing edges with out-degree deg(u) (possibly 0). Each outgoing edge at that node has a local port number 1 to deg(u). Following port k from node u leads to some node v (self-loops allowed). The graph remains constant throughout the game.

Your goal is to determine whether the graph contains a directed cycle. You can interact with the system through the following queries (submit one query at a time), and I will answer truthfully based on the actual setup:

1. Query node count: Ask for the total number of nodes N in the graph.
2. Query out-degree: Ask for the out-degree of a specified node i. Returns an error if the node does not exist.
3. Single-step traversal: Take one step from node i through port k, returning the destination node j. Returns an error if the node or port is invalid.
4. Multi-step traversal: Starting from a specified node, follow a given sequence of ports for multiple steps. The system returns the visit sequence and immediately stops upon detecting a repeated node, reporting cycle information.

When you have collected enough information, submit your final judgment. If the judgment is incorrect or the format is invalid, the game fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Query node count:
<query_n></query_n>

- Query out-degree (e.g., query out-degree of node 5):
<query_degree>5</query_degree>

- Single-step traversal (e.g., from node 3 through port 2):
<query_step>3,2</query_step>

- Multi-step traversal (e.g., start from node 1, follow ports 1,2,1):
<query_path>start=1,ports=[1,2,1]</query_path>

When submitting the final judgment, you must state whether a cycle exists. If judging that a cycle exists, you may optionally attach a cycle as evidence (comma-separated node sequence with the same first and last node), using this format:

- Judgment of no cycle:
<answer>no_cycle</answer>

- Judgment of cycle exists (without cycle evidence):
<answer>has_cycle</answer>

- Judgment of cycle exists (with cycle evidence, e.g., 1->2->3->1):
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来玩一个"城市路网死循环检测"的推理游戏，规则如下：

游戏设定了一个固定的城市单向路网图 G=(V,E)，交叉路口数为 N（未知但可查询），路口以 1 到 N 标号。每个路口 u 有若干驶出道路，驶出道路数记为 deg(u)（可能为 0）。每条驶出道路在该路口处有局部出口编号 1 到 deg(u)。从路口 u 通过出口 k 会行驶至某个路口 v（允许原地掉头）。路网在整个游戏过程中保持不变。

你的目标是判定该路网是否存在会导致车辆无限循环的闭环路线。你可以通过以下查询与系统交互（每次提交一个查询），我会根据真实设定如实回答：

1. 查询路口数：询问路网中交叉路口总数 N。
2. 查询驶出道路数：询问指定路口 i 的驶出道路数。若路口不存在则返回错误。
3. 单步行驶：从路口 i 通过出口 k 行驶一步，返回到达的路口 j。若路口或出口无效则返回错误。
4. 多步路线：从指定起点出发，按给定的出口序列连续行驶多步。系统会返回途经路口序列，并在检测到重复路口时立即停止并报告闭环信息。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询路口数：
<query_n></query_n>

- 查询驶出道路数（例如查询路口 5 的驶出道路数）：
<query_degree>5</query_degree>

- 单步行驶（例如从路口 3 通过出口 2 行驶一步）：
<query_step>3,2</query_step>

- 多步路线（例如从路口 1 出发，依次通过出口 1,2,1）：
<query_path>start=1,ports=[1,2,1]</query_path>

提交最终判定时，必须说明是否存在闭环。若判定存在闭环，可选择性附上一条闭环路线作为证据（用逗号隔开的路口序列，首尾路口相同），格式如下：

- 判定不存在闭环：
<answer>no_cycle</answer>

- 判定存在闭环（不提供路线证据）：
<answer>has_cycle</answer>

- 判定存在闭环（提供路线证据，例如 1->2->3->1）：
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's play a "City Road Network Deadlock Detection" reasoning game. Here are the rules:

The game features a fixed city one-way road network G=(V,E) with N intersections (unknown but queryable), labeled 1 to N. Each intersection u has some outgoing roads, with the number of outgoing roads denoted as deg(u) (possibly 0). Each outgoing road at that intersection has a local exit number from 1 to deg(u). Driving from intersection u through exit k leads to some intersection v (U-turns allowed). The road network remains constant throughout the game.

Your goal is to determine whether the network contains a closed route that would cause vehicles to circle infinitely. You can interact with the system through the following queries (submit one query at a time), and I will answer truthfully based on the actual setup:

1. Query intersection count: Ask for the total number of intersections N in the network.
2. Query outgoing road count: Ask for the number of outgoing roads for a specified intersection i. Returns an error if the intersection does not exist.
3. Single-step drive: Drive one step from intersection i through exit k, returning the destination intersection j. Returns an error if the intersection or exit is invalid.
4. Multi-step route: Starting from a specified intersection, follow a given sequence of exits for multiple steps. The system returns the passed intersection sequence and immediately stops upon detecting a repeated intersection, reporting the closed loop information.

When you have collected enough information, submit your final judgment. If the judgment is incorrect or the format is invalid, the game fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Query intersection count:
<query_n></query_n>

- Query outgoing road count (e.g., query outgoing road count of intersection 5):
<query_degree>5</query_degree>

- Single-step drive (e.g., from intersection 3 through exit 2):
<query_step>3,2</query_step>

- Multi-step route (e.g., start from intersection 1, follow exits 1,2,1):
<query_path>start=1,ports=[1,2,1]</query_path>

When submitting the final judgment, you must state whether a closed loop exists. If judging that a closed loop exists, you may optionally attach a closed route as evidence (comma-separated intersection sequence with the same first and last intersection), using this format:

- Judgment of no closed loop:
<answer>no_cycle</answer>

- Judgment of closed loop exists (without evidence):
<answer>has_cycle</answer>

- Judgment of closed loop exists (with evidence, e.g., 1->2->3->1):
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来玩一个"医疗转诊流程死循环检测"的推理游戏，规则如下：

游戏设定了一个固定的医疗转诊网络 G=(V,E)，诊疗科室数为 N（未知但可查询），科室以 1 到 N 标号。每个科室 u 有若干转出通道，转出通道数记为 deg(u)（可能为 0）。每条转出通道在该科室处有局部通道编号 1 到 deg(u)。从科室 u 通过通道 k 会转诊至某个科室 v（允许复诊本区）。转诊网络在整个游戏过程中保持不变。

你的目标是判定该转诊流程是否存在让患者无限打转的死循环。你可以通过以下查询与系统交互（每次提交一个查询），我会根据真实设定如实回答：

1. 查询科室数：询问网络中诊疗科室总数 N。
2. 查询转出通道数：询问指定科室 i 的转出通道数。若科室不存在则返回错误。
3. 单步转诊：从科室 i 通过通道 k 转诊一步，返回转诊至的科室 j。若科室或通道无效则返回错误。
4. 多步转诊：从指定起点出发，按给定的通道序列连续转诊多步。系统会返回就诊序列，并在检测到重复科室时立即停止并报告循环信息。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询科室数：
<query_n></query_n>

- 查询转出通道数（例如查询科室 5 的转出通道数）：
<query_degree>5</query_degree>

- 单步转诊（例如从科室 3 通过通道 2 转诊一步）：
<query_step>3,2</query_step>

- 多步转诊（例如从科室 1 出发，依次通过通道 1,2,1）：
<query_path>start=1,ports=[1,2,1]</query_path>

提交最终判定时，必须说明是否存在死循环。若判定存在死循环，可选择性附上一条循环流程作为证据（用逗号隔开的科室序列，首尾科室相同），格式如下：

- 判定不存在死循环：
<answer>no_cycle</answer>

- 判定存在死循环（不提供循环证据）：
<answer>has_cycle</answer>

- 判定存在死循环（提供循环证据，例如 1->2->3->1）：
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Medical Referral Deadlock Detection" reasoning game. Here are the rules:

The game features a fixed medical referral network G=(V,E) with N departments (unknown but queryable), labeled 1 to N. Each department u has some transfer channels, with the number of transfer channels denoted as deg(u) (possibly 0). Each transfer channel at that department has a local channel number from 1 to deg(u). Transferring from department u through channel k leads to some department v (re-visiting the same department allowed). The referral network remains constant throughout the game.

Your goal is to determine whether the referral process contains an infinite loop for patients. You can interact with the system through the following queries (submit one query at a time), and I will answer truthfully based on the actual setup:

1. Query department count: Ask for the total number of departments N in the network.
2. Query transfer channel count: Ask for the number of transfer channels for a specified department i. Returns an error if the department does not exist.
3. Single-step transfer: Transfer one step from department i through channel k, returning the destination department j. Returns an error if the department or channel is invalid.
4. Multi-step referral: Starting from a specified department, follow a given sequence of channels for multiple steps. The system returns the visit sequence and immediately stops upon detecting a repeated department, reporting the loop information.

When you have collected enough information, submit your final judgment. If the judgment is incorrect or the format is invalid, the game fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Query department count:
<query_n></query_n>

- Query transfer channel count (e.g., query channel count of department 5):
<query_degree>5</query_degree>

- Single-step transfer (e.g., from department 3 through channel 2):
<query_step>3,2</query_step>

- Multi-step referral (e.g., start from department 1, follow channels 1,2,1):
<query_path>start=1,ports=[1,2,1]</query_path>

When submitting the final judgment, you must state whether an infinite loop exists. If judging that an infinite loop exists, you may optionally attach a loop process as evidence (comma-separated department sequence with the same first and last department), using this format:

- Judgment of no infinite loop:
<answer>no_cycle</answer>

- Judgment of infinite loop exists (without evidence):
<answer>has_cycle</answer>

- Judgment of infinite loop exists (with evidence, e.g., 1->2->3->1):
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来玩一个"课程体系循环依赖检测"的推理游戏，规则如下：

游戏设定了一个固定的课程先修依赖图 G=(V,E)，知识模块数为 N（未知但可查询），模块以 1 到 N 标号。每个模块 u 有若干后续选项，后续选项数记为 deg(u)（可能为 0）。每个后续选项在该模块处有局部选项编号 1 到 deg(u)。从模块 u 通过选项 k 会导向某个模块 v（允许自我强化）。课程体系在整个游戏过程中保持不变。

你的目标是判定该课程体系是否存在导致无法毕业的循环依赖。你可以通过以下查询与系统交互（每次提交一个查询），我会根据真实设定如实回答：

1. 查询模块数：询问课程体系中知识模块总数 N。
2. 查询后续选项数：询问指定模块 i 的后续选项数。若模块不存在则返回错误。
3. 单步进阶：从模块 i 通过选项 k 学习一步，返回导向的模块 j。若模块或选项无效则返回错误。
4. 多步学习：从指定起点出发，按给定的选项序列连续学习多步。系统会返回学习序列，并在检测到重复模块时立即停止并报告循环信息。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML 格式：

- 查询模块数：
<query_n></query_n>

- 查询后续选项数（例如查询模块 5 的后续选项数）：
<query_degree>5</query_degree>

- 单步进阶（例如从模块 3 通过选项 2 学习一步）：
<query_step>3,2</query_step>

- 多步学习（例如从模块 1 出发，依次通过选项 1,2,1）：
<query_path>start=1,ports=[1,2,1]</query_path>

提交最终判定时，必须说明是否存在循环依赖。若判定存在循环依赖，可选择性附上一条循环路径作为证据（用逗号隔开的模块序列，首尾模块相同），格式如下：

- 判定不存在循环依赖：
<answer>no_cycle</answer>

- 判定存在循环依赖（不提供路径证据）：
<answer>has_cycle</answer>

- 判定存在循环依赖（提供路径证据，例如 1->2->3->1）：
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Curriculum Circular Dependency Detection" reasoning game. Here are the rules:

The game features a fixed curriculum prerequisite graph G=(V,E) with N knowledge modules (unknown but queryable), labeled 1 to N. Each module u has some subsequent options, with the number of options denoted as deg(u) (possibly 0). Each subsequent option at that module has a local option number from 1 to deg(u). Learning from module u through option k leads to some module v (self-reinforcement allowed). The curriculum structure remains constant throughout the game.

Your goal is to determine whether the curriculum contains a circular dependency that prevents graduation. You can interact with the system through the following queries (submit one query at a time), and I will answer truthfully based on the actual setup:

1. Query module count: Ask for the total number of modules N in the curriculum.
2. Query subsequent option count: Ask for the number of subsequent options for a specified module i. Returns an error if the module does not exist.
3. Single-step progression: Learn one step from module i through option k, returning the target module j. Returns an error if the module or option is invalid.
4. Multi-step learning: Starting from a specified module, follow a given sequence of options for multiple steps. The system returns the learning sequence and immediately stops upon detecting a repeated module, reporting the dependency loop information.

When you have collected enough information, submit your final judgment. If the judgment is incorrect or the format is invalid, the game fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Query module count:
<query_n></query_n>

- Query subsequent option count (e.g., query option count of module 5):
<query_degree>5</query_degree>

- Single-step progression (e.g., from module 3 through option 2):
<query_step>3,2</query_step>

- Multi-step learning (e.g., start from module 1, follow options 1,2,1):
<query_path>start=1,ports=[1,2,1]</query_path>

When submitting the final judgment, you must state whether a circular dependency exists. If judging that a circular dependency exists, you may optionally attach a loop path as evidence (comma-separated module sequence with the same first and last module), using this format:

- Judgment of no circular dependency:
<answer>no_cycle</answer>

- Judgment of circular dependency exists (without evidence):
<answer>has_cycle</answer>

- Judgment of circular dependency exists (with evidence, e.g., 1->2->3->1):
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来玩一个"工厂物料流转死循环检测"的推理游戏，规则如下：

游戏设定了一个固定的车间物料流转图 G=(V,E)，加工工序数为 N（未知但可查询），工序以 1 到 N 标号。每个工序 u 有若干传送带，传送带数记为 deg(u)（可能为 0）。每条传送带在该工序处有局部接口编号 1 到 deg(u)。从工序 u 通过接口 k 会将物料送至某个工序 v（允许返工原工序）。流转网络在整个游戏过程中保持不变。

你的目标是判定该物料流转网络是否存在导致物料永远无法产出的死循环。你可以通过以下查询与系统交互（每次提交一个查询），我会根据真实设定如实回答：

1. 查询工序数：询问流转图中的加工工序总数 N。
2. 查询传送带数：询问指定工序 i 的传送带数。若工序不存在则返回错误。
3. 单步流转：从工序 i 通过接口 k 流转一步，返回送至的工序 j。若工序或接口无效则返回错误。
4. 多步流转：从指定起点出发，按给定的接口序列连续流转多步。系统会返回流转序列，并在检测到重复工序时立即停止并报告死循环信息。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML format:

- 查询工序数：
<query_n></query_n>

- 查询传送带数（例如查询工序 5 的传送带数）：
<query_degree>5</query_degree>

- 单步流转（例如从工序 3 通过接口 2 流转一步）：
<query_step>3,2</query_step>

- 多步流转（例如从工序 1 出发，依次通过接口 1,2,1）：
<query_path>start=1,ports=[1,2,1]</query_path>

提交最终判定时，必须说明是否存在死循环。若判定存在死循环，可选择性附上一条死循环链路作为证据（用逗号隔开的工序序列，首尾工序相同），格式如下：

- 判定不存在死循环：
<answer>no_cycle</answer>

- 判定存在死循环（不提供链路证据）：
<answer>has_cycle</answer>

- 判定存在死循环（提供链路证据，例如 1->2->3->1）：
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's play a "Factory Material Flow Infinite Loop Detection" reasoning game. Here are the rules:

The game features a fixed workshop material flow graph G=(V,E) with N processing steps (unknown but queryable), labeled 1 to N. Each step u has some conveyor belts, with the number of belts denoted as deg(u) (possibly 0). Each conveyor belt at that step has a local interface number from 1 to deg(u). Routing materials from step u through interface k sends them to some step v (reworking at the same step allowed). The flow network remains constant throughout the game.

Your goal is to determine whether the material flow network contains an infinite loop preventing final production. You can interact with the system through the following queries (submit one query at a time), and I will answer truthfully based on the actual setup:

1. Query step count: Ask for the total number of processing steps N in the flow graph.
2. Query conveyor belt count: Ask for the number of conveyor belts for a specified step i. Returns an error if the step does not exist.
3. Single-step routing: Route materials one step from step i through interface k, returning the destination step j. Returns an error if the step or interface is invalid.
4. Multi-step flow: Starting from a specified step, follow a given sequence of interfaces for multiple steps. The system returns the flow sequence and immediately stops upon detecting a repeated step, reporting the infinite loop information.

When you have collected enough information, submit your final judgment. If the judgment is incorrect or the format is invalid, the game fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Query step count:
<query_n></query_n>

- Query conveyor belt count (e.g., query belt count of step 5):
<query_degree>5</query_degree>

- Single-step routing (e.g., from step 3 through interface 2):
<query_step>3,2</query_step>

- Multi-step flow (e.g., start from step 1, follow interfaces 1,2,1):
<query_path>start=1,ports=[1,2,1]</query_path>

When submitting the final judgment, you must state whether an infinite loop exists. If judging that an infinite loop exists, you may optionally attach a loop chain as evidence (comma-separated step sequence with the same first and last step), using this format:

- Judgment of no infinite loop:
<answer>no_cycle</answer>

- Judgment of infinite loop exists (without evidence):
<answer>has_cycle</answer>

- Judgment of infinite loop exists (with evidence, e.g., 1->2->3->1):
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来玩一个"司法审批程序死循环检测"的推理游戏，规则如下：

游戏设定了一个固定的司法案件移交网络 G=(V,E)，审批环节数为 N（未知但可查询），环节以 1 到 N 标号。每个环节 u 有若干案件移交选项，移交选项数记为 deg(u)（可能为 0）。每个移交选项在该环节处有局部选项编号 1 到 deg(u)。从环节 u 通过选项 k 会将案件移交至某个环节 v（允许退回本环节重审）。移交网络在整个游戏过程中保持不变。

你的目标是判定该审批网络是否存在会导致案件无限推诿的死循环。你可以通过以下查询与系统交互（每次提交一个查询），我会根据真实设定如实回答：

1. 查询环节数：询问网络中审批环节总数 N。
2. 查询移交选项数：询问指定环节 i 的案件移交选项数。若环节不存在则返回错误。
3. 单步移交：从环节 i 通过选项 k 移交一次，返回到达的环节 j。若环节或选项无效则返回错误。
4. 多步追踪：从指定起点出发，按给定的选项序列连续追踪多步。系统会返回移交序列，并在检测到重复环节时立即停止并报告循环推诿信息。

当你收集足够信息后，请提交最终判定。若判定错误或格式不符，游戏失败。

## 查询与提交答案的格式（必须严格遵守）

每次查询只能包含一个标签。请使用以下 XML format:

- 查询环节数：
<query_n></query_n>

- 查询移交选项数（例如查询环节 5 的案件移交选项数）：
<query_degree>5</query_degree>

- 单步移交（例如从环节 3 通过选项 2 移交一次）：
<query_step>3,2</query_step>

- 多步追踪（例如从环节 1 出发，依次通过选项 1,2,1）：
<query_path>start=1,ports=[1,2,1]</query_path>

提交最终判定时，必须说明是否存在死循环。若判定存在死循环，可选择性附上一条死循环链作为证据（用逗号隔开的环节序列，首尾环节相同），格式如下：

- 判定不存在死循环：
<answer>no_cycle</answer>

- 判定存在死循环（不提供证据）：
<answer>has_cycle</answer>

- 判定存在死循环（提供证据，例如 1->2->3->1）：
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Judicial Approval Deadlock Detection" reasoning game. Here are the rules:

The game features a fixed judicial case transfer network G=(V,E) with N approval stages (unknown but queryable), labeled 1 to N. Each stage u has some case transfer options, with the number of options denoted as deg(u) (possibly 0). Each transfer option at that stage has a local option number from 1 to deg(u). Transferring a case from stage u through option k sends it to some stage v (returning to the same stage for review allowed). The transfer network remains constant throughout the game.

Your goal is to determine whether the approval network contains a bureaucratic loop causing infinite delays. You can interact with the system through the following queries (submit one query at a time), and I will answer truthfully based on the actual setup:

1. Query stage count: Ask for the total number of approval stages N in the network.
2. Query transfer option count: Ask for the number of transfer options for a specified stage i. Returns an error if the stage does not exist.
3. Single-step transfer: Transfer a case one step from stage i through option k, returning the receiving stage j. Returns an error if the stage or option is invalid.
4. Multi-step tracking: Starting from a specified stage, follow a given sequence of options for multiple steps. The system returns the transfer sequence and immediately stops upon detecting a repeated stage, reporting the bureaucratic loop information.

When you have collected enough information, submit your final judgment. If the judgment is incorrect or the format is invalid, the game fails.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Query stage count:
<query_n></query_n>

- Query transfer option count (e.g., query option count of stage 5):
<query_degree>5</query_degree>

- Single-step transfer (e.g., from stage 3 through option 2):
<query_step>3,2</query_step>

- Multi-step tracking (e.g., start from stage 1, follow options 1,2,1):
<query_path>start=1,ports=[1,2,1]</query_path>

When submitting the final judgment, you must state whether a bureaucratic loop exists. If judging that a loop exists, you may optionally attach a closed chain as evidence (comma-separated stage sequence with the same first and last stage), using this format:

- Judgment of no bureaucratic loop:
<answer>no_cycle</answer>

- Judgment of bureaucratic loop exists (without evidence):
<answer>has_cycle</answer>

- Judgment of bureaucratic loop exists (with evidence, e.g., 1->2->3->1):
<answer>has_cycle,cycle=[1,2,3,1]</answer>
"""

    tags = ["answer", "query_n", "query_degree", "query_step", "query_path"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    # 难度配置说明：
    # 1 (简单)       - N=3, 明显自环
    # 2 (中等偏下)   - N=4, 简单环路
    # 3 (中等偏上)   - N=5, 环路较深
    # 4 (较难)       - N=6, 无环图（DAG）
    # 5 (难)         - N=7, 复杂结构含环

    DIFFICULTY_CONFIG = {
        1: {
            "n": 3,
            "edges": {
                # 节点1有自环
                1: [1],      # 端口1 -> 节点1
                2: [3],      # 端口1 -> 节点3
                3: [2],      # 端口1 -> 节点2
            },
            "has_cycle": True,
        },
        2: {
            "n": 4,
            "edges": {
                # 1->2->3->1 构成环
                1: [2],      # 端口1 -> 节点2
                2: [3],      # 端口1 -> 节点3
                3: [1],      # 端口1 -> 节点1
                4: [1],      # 端口1 -> 节点1（孤立节点指向1）
            },
            "has_cycle": True,
        },
        3: {
            "n": 5,
            "edges": {
                # 1->2->3->4->2 构成环
                1: [2],      # 端口1 -> 节点2
                2: [3, 5],   # 端口1 -> 节点3, 端口2 -> 节点5
                3: [4],      # 端口1 -> 节点4
                4: [2],      # 端口1 -> 节点2（回到2形成环）
                5: [1],      # 端口1 -> 节点1
            },
            "has_cycle": True,
        },
        4: {
            "n": 6,
            "edges": {
                # DAG: 1->2->4, 1->3->5, 2->5, 3->6, 5->6
                1: [2, 3],   # 端口1 -> 节点2, 端口2 -> 节点3
                2: [4, 5],   # 端口1 -> 节点4, 端口2 -> 节点5
                3: [5, 6],   # 端口1 -> 节点5, 端口2 -> 节点6
                4: [],       # 无出边
                5: [6],      # 端口1 -> 节点6
                6: [],       # 无出边
            },
            "has_cycle": False,
        },
        5: {
            "n": 7,
            "edges": {
                # 复杂结构：1->2->3->4->5->3（3-4-5-3环），1->6->7
                1: [2, 6],   # 端口1 -> 节点2, 端口2 -> 节点6
                2: [3],      # 端口1 -> 节点3
                3: [4],      # 端口1 -> 节点4
                4: [5, 7],   # 端口1 -> 节点5, 端口2 -> 节点7
                5: [3],      # 端口1 -> 节点3（回到3形成环）
                6: [7],      # 端口1 -> 节点7
                7: [],       # 无出边
            },
            "has_cycle": True,
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        if isinstance(diff, str):
            diff = int(diff)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self._game_info["n"] = cfg["n"]
        
        # 深拷贝图结构，避免修改类变量
        self.graph = {k: list(v) for k, v in cfg["edges"].items()}
        self.n = cfg["n"]
        self.has_cycle = cfg["has_cycle"]
        
        # 确保所有节点都存在于图中
        for i in range(1, self.n + 1):
            if i not in self.graph:
                self.graph[i] = []

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"].strip()
        
        # 解析答案
        if raw_ans == "no_cycle":
            model_judgment = False
            model_cycle = None
        elif raw_ans == "has_cycle":
            model_judgment = True
            model_cycle = None
        elif raw_ans.startswith("has_cycle,cycle="):
            model_judgment = True
            # 提取回路
            match = re.search(r'cycle=\[([^\]]+)\]', raw_ans)
            if match:
                try:
                    cycle_str = match.group(1)
                    model_cycle = [int(x.strip()) for x in cycle_str.split(",")]
                except:
                    return False
            else:
                return False
        else:
            return False
        
        # 1. 检查判定是否正确
        if model_judgment != self.has_cycle:
            return False
        
        # 2. 如果提供了回路证据，验证其有效性
        if model_cycle is not None:
            if not self._verify_cycle(model_cycle):
                return False
        
        return True

    def _verify_cycle(self, cycle):
        """验证给定的回路是否有效"""
        if len(cycle) < 2:
            return False
        
        # 首尾节点必须相同
        if cycle[0] != cycle[-1]:
            return False
        
        # 验证每条边是否存在
        for i in range(len(cycle) - 1):
            u, v = cycle[i], cycle[i + 1]
            if u < 1 or u > self.n:
                return False
            if v < 1 or v > self.n:
                return False
            if v not in self.graph[u]:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """根据查询类型产生响应"""
        if self.config.language == "zh":
            error_node = "错误：节点不存在。"
            error_port = "错误：端口无效。"
            error_format = "错误：格式无效。"
        else:
            error_node = "Error: Node does not exist."
            error_port = "Error: Invalid port."
            error_format = "Error: Invalid format."

        # 1. 查询节点数
        if "query_n" in parsed_info:
            return f"N={self.n}"

        # 2. 查询出度
        elif "query_degree" in parsed_info:
            try:
                node = int(parsed_info["query_degree"].strip())
                if node < 1 or node > self.n:
                    return error_node
                degree = len(self.graph[node])
                if self.config.language == "zh":
                    return f"节点 {node} 的出度为 {degree}"
                else:
                    return f"Node {node} has out-degree {degree}"
            except:
                return error_format

        # 3. 单步遍历
        elif "query_step" in parsed_info:
            try:
                raw = parsed_info["query_step"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                node = int(parts[0])
                port = int(parts[1])
                
                if node < 1 or node > self.n:
                    return error_node
                
                if port < 1 or port > len(self.graph[node]):
                    return error_port
                
                dest = self.graph[node][port - 1]  # 端口从1开始，列表从0开始
                if self.config.language == "zh":
                    return f"从节点 {node} 通过端口 {port} 到达节点 {dest}"
                else:
                    return f"From node {node} via port {port} reach node {dest}"
            except:
                return error_format

        # 4. 多步遍历
        elif "query_path" in parsed_info:
            try:
                raw = parsed_info["query_path"].strip()
                # 解析 start=X,ports=[p1,p2,...]
                start_match = re.search(r'start=(\d+)', raw)
                ports_match = re.search(r'ports=\[([^\]]*)\]', raw)
                
                if not start_match:
                    return error_format
                
                start_node = int(start_match.group(1))
                if start_node < 1 or start_node > self.n:
                    return error_node
                
                # 解析端口序列
                ports = []
                if ports_match:
                    ports_str = ports_match.group(1).strip()
                    if ports_str:
                        ports = [int(x.strip()) for x in ports_str.split(",")]
                
                # 执行多步遍历
                return self._execute_multi_step(start_node, ports)
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """产生一个错误的响应，用于反事实干预"""
        nums = list(re.finditer(r'\d+', correct))
        if nums:
            last_num = nums[-1]
            old_val = int(last_num.group())
            # 生成一个保证不同的数字
            new_val = old_val + 1
            if new_val == old_val:  # 理论上不会发生，但防御性编程
                new_val = old_val + 2
            return correct[:last_num.start()] + str(new_val) + correct[last_num.end():]
        
        # fallback
        return correct + "_WRONG"

    def _execute_multi_step(self, start, ports):
        """执行多步遍历，检测重复节点"""
        visited = [start]
        current = start
        
        if self.config.language == "zh":
            error_port_tpl = "错误：第 {} 步端口无效。已访问序列：{}。"
            no_repeat_tpl = "访问序列：{}，无重复节点。"
        else:
            error_port_tpl = "Error: Port invalid at step {}. Visit sequence so far: {}."
            no_repeat_tpl = "Visit sequence: {}, no repeated node."
        
        for step_idx, port in enumerate(ports, start=1):
            # 检查端口有效性
            if port < 1 or port > len(self.graph[current]):
                seq_str = "->".join(map(str, visited))
                return error_port_tpl.format(step_idx, seq_str)
            
            # 执行一步
            next_node = self.graph[current][port - 1]
            
            # 检查是否重复
            if next_node in visited:
                first_occurrence = visited.index(next_node)
                cycle_length = len(visited) - first_occurrence
                visited.append(next_node)
                seq_str = "->".join(map(str, visited))
                if self.config.language == "zh":
                    return (f"访问序列：{seq_str}，在第 {step_idx} 步检测到重复节点 {next_node}"
                            f"（首次出现在第 {first_occurrence} 步），回路长度为 {cycle_length}。")
                else:
                    return (f"Visit sequence: {seq_str}, repeated node {next_node} detected at step {step_idx}"
                            f" (first appeared at step {first_occurrence}), cycle length {cycle_length}.")
            
            visited.append(next_node)
            current = next_node
        
        # 完成所有步骤，无重复
        seq_str = "->".join(map(str, visited))
        return no_repeat_tpl.format(seq_str)

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        排除无限组合的 query_path，仅包含结构化查询（N, degree, step）。
        """
        queries = []
        
        # 1. 查询节点数 (Query Node Count)
        # 对应标签 <query_n>，内容为空
        queries.append({
            "query": "<query_n></query_n>",
            "answer": self._cf_core_produce({"query_n": ""})
        })
        
        # 2. 查询出度 (Query Degree)
        # 对应标签 <query_degree>，内容为节点编号 1..N
        for node in range(1, self.n + 1):
            q_val = str(node)
            ans = self._cf_core_produce({"query_degree": q_val})
            queries.append({
                "query": f"<query_degree>{q_val}</query_degree>",
                "answer": ans
            })
            
        # 3. 单步遍历 (Single Step)
        # 对应标签 <query_step>，内容为 "node,port"
        for node in range(1, self.n + 1):
            # 获取该节点的出度
            degree = len(self.graph[node])
            for port in range(1, degree + 1):
                q_val = f"{node},{port}"
                ans = self._cf_core_produce({"query_step": q_val})
                queries.append({
                    "query": f"<query_step>{q_val}</query_step>",
                    "answer": ans
                })
                
        return queries