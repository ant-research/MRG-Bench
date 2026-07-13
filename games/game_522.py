# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子树属性聚合：某子树内所有节点的属性之和/最大值是多少
# ============================================================

import random
from .base import Game


class HiddenTreeRuleGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏树规则推断"游戏。规则如下：

## 游戏设定

给定一棵有根树，包含 {n} 个节点，根节点编号为 {root}。每个节点 v 有一个非负整数属性 val[v]。
树的结构（所有边的父子关系）和每个节点的属性值如下：

{tree_structure}

对于任意节点 u，你可以自行计算以下两个值：
- SUM(u)：节点 u 的整棵子树（包括 u 本身）所有节点属性值之和
- MAX(u)：节点 u 的整棵子树（包括 u 本身）所有节点属性值的最大值

## 隐藏规则

系统内部对每个节点 u 设定了一个隐藏的确定性规则 g(u)，该规则只能是 SUM 或 MAX 之一。
规则 g 仅依赖于节点的可见特征（如深度、子树大小等），在整个游戏过程中保持不变。

当你查询节点 u 时，系统会返回 H(u) = g(u)(u)，即：
- 如果 g(u) = SUM，则返回 SUM(u)
- 如果 g(u) = MAX，则返回 MAX(u)

## 游戏目标

你最多可以进行 {max_probes} 次查询来推断隐藏规则。在查询阶段结束后，系统会给你一组目标节点，你需要正确预测这些节点的 H 值。

## 交互格式（必须严格遵守）

### 查询节点
使用以下格式查询节点 u 的 H 值（u 必须是有效节点编号）：
<query_probe>u</query_probe>

### 进入最终测验
当你准备好进入最终测验阶段时，使用：
<query_final></query_final>

系统会返回需要你预测的目标节点列表。

### 提交最终答案
对目标节点列表中的所有节点提交预测值，格式如下：
<answer>u1:x1, u2:x2, u3:x3</answer>

其中 u1, u2, u3 等是目标节点编号，x1, x2, x3 等是你预测的对应 H 值。
节点顺序不限，但必须包含所有目标节点且每个节点恰好出现一次。

## 注意事项
- 查询次数有限，请合理规划
- 建议选择 SUM 值和 MAX 值不相等的节点进行查询，以获得更多信息
- 隐藏规则是确定性的，不依赖于查询历史
"""

    game_rule_en = """\
Let's play a "Hidden Tree Rule Inference" game. Here are the rules:

## Game Setup

Given a rooted tree with {n} nodes, the root node is numbered {root}. Each node v has a non-negative integer attribute val[v].
The tree structure (all parent-child relationships) and each node's attribute value are as follows:

{tree_structure}

For any node u, you can independently calculate the following two values:
- SUM(u): The sum of all node attribute values in the entire subtree of node u (including u itself)
- MAX(u): The maximum of all node attribute values in the entire subtree of node u (including u itself)

## Hidden Rule

The system has internally set a hidden deterministic rule g(u) for each node u, which can only be either SUM or MAX.
The rule g only depends on visible features of the node (such as depth, subtree size, etc.) and remains constant throughout the game.

When you query node u, the system will return H(u) = g(u)(u), that is:
- If g(u) = SUM, it returns SUM(u)
- If g(u) = MAX, it returns MAX(u)

## Game Objective

You can perform at most {max_probes} queries to infer the hidden rule. After the query phase ends, the system will give you a set of target nodes, and you need to correctly predict the H values of these nodes.

## Interaction Format (must strictly follow)

### Query a node
Use the following format to query the H value of node u (u must be a valid node number):
<query_probe>u</query_probe>

### Enter final test
When you are ready to enter the final test phase, use:
<query_final></query_final>

The system will return the list of target nodes you need to predict.

### Submit final answer
Submit predicted values for all nodes in the target node list in the following format:
<answer>u1:x1, u2:x2, u3:x3</answer>

Where u1, u2, u3, etc. are target node numbers, and x1, x2, x3, etc. are your predicted corresponding H values.
The order of nodes does not matter, but must include all target nodes and each node must appear exactly once.

## Notes
- The number of queries is limited, please plan wisely
- It is recommended to select nodes where SUM value and MAX value are not equal for queries to obtain more information
- The hidden rule is deterministic and does not depend on query history
"""

    # -------------------------------------------------------------
    # 场景 1：交通
    # -------------------------------------------------------------
    contextualized_rule_zh_1 = """\
欢迎使用“城市智能交通监控分析系统”。我们将进行一项辖区交通枢纽评估策略推断任务。

## 监控网设定

本市的道路监控网络由 {n} 个节点组成的树状结构构成，总控中心节点编号为 {root}。每个节点 v（代表路口或区域）记录了当前的实时基础车流量 val[v]。
监控网的层级关系（上级管辖区域 -> 下级路段）及各节点基础车流量如下：

{tree_structure}

对于任意监控节点 u，系统会统计该节点及其下属所有区域的两种交通负荷指标：
- SUM(u)：节点 u 管辖的所有区域（含自身）的总车流量汇聚值。
- MAX(u)：节点 u 管辖的所有区域（含自身）中，车流量最大的单一节点值（即拥堵极值）。

## 隐藏评估策略

系统对每个监控节点 u 配置了固定的交通评估策略 g(u)，它只可能是 SUM 或 MAX 之一。
规则 g 仅依赖于节点的固有拓扑特征（如层级深度、管辖的子节点数等），在整个调配过程中保持不变。

当你查询节点 u 的负荷时，系统会返回评估结果 H(u) = g(u)(u)，即：
- 若评估策略 g(u) 为 SUM，则返回区域总车流量 SUM(u)
- 若评估策略 g(u) 为 MAX，则返回拥堵极值 MAX(u)

## 任务目标

你最多可以进行 {max_probes} 次查询来摸清系统背后的评估策略。查询阶段结束后，系统会下发一组需要重点监控的目标节点，你需要正确预测这些节点的评估值 H。

## 交互格式（必须严格遵守）

### 查询节点
使用以下格式查询节点 u 的评估值（u 必须是有效节点编号）：
<query_probe>u</query_probe>

### 进入最终测验
当你准备好进入最终预测阶段时，使用：
<query_final></query_final>
系统会返回需要你预测的目标监控节点列表。

### 提交最终答案
对目标节点列表中的所有节点提交预测值，格式如下：
<answer>u1:x1, u2:x2, u3:x3</answer>

其中 u1, u2, u3 等是目标节点编号，x1, x2, x3 等是你预测的对应评估值。
节点顺序不限，但必须包含所有目标节点且每个节点恰好出现一次。

## 注意事项
- 查询次数有限，请合理规划
- 建议选择 SUM 值和 MAX 值存在差异的节点进行查询，以辨别其使用的策略
- 评估策略是确定性的，不会因你的查询顺序而改变
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Intelligent Traffic Monitoring and Analysis System". We will conduct an inference task on the evaluation strategy of regional traffic hubs.

## Monitoring Network Setup

The city's road monitoring network consists of a tree structure with {n} nodes, where the main control center node is numbered {root}. Each node v (representing an intersection or area) records the current real-time basic traffic volume val[v].
The hierarchical relationships (upper management area -> lower road segment) and the basic traffic volume of each node are as follows:

{tree_structure}

For any monitoring node u, the system calculates two traffic load metrics for this node and all its subordinate areas:
- SUM(u): The total aggregated traffic volume of all areas under node u (including u itself).
- MAX(u): The maximum basic traffic volume among all single areas under node u (including u itself), representing the congestion peak.

## Hidden Evaluation Strategy

The system has configured a fixed traffic evaluation strategy g(u) for each monitoring node u, which can only be either SUM or MAX.
The rule g depends only on the inherent topological features of the node (such as hierarchical depth, number of subordinate nodes, etc.) and remains unchanged throughout the process.

When you query the load of node u, the system will return the evaluation result H(u) = g(u)(u), that is:
- If g(u) is SUM, it returns the total area traffic volume SUM(u)
- If g(u) is MAX, it returns the congestion peak MAX(u)

## Task Objective

You can perform at most {max_probes} queries to figure out the underlying evaluation strategy. After the query phase, the system will assign a set of target nodes that need key monitoring, and you must correctly predict their evaluation values H.

## Interaction Format (must strictly follow)

### Query a node
Use the following format to query the evaluation value of node u (u must be a valid node number):
<query_probe>u</query_probe>

### Enter final test
When you are ready to enter the final prediction phase, use:
<query_final></query_final>
The system will return the list of target monitoring nodes you need to predict.

### Submit final answer
Submit predicted values for all nodes in the target list in the following format:
<answer>u1:x1, u2:x2, u3:x3</answer>

Where u1, u2, u3, etc. are target node numbers, and x1, x2, x3, etc. are your predicted evaluation values.
The node order does not matter, but all target nodes must be included exactly once.

## Notes
- Query attempts are limited; plan wisely.
- It is recommended to query nodes where SUM and MAX values differ to distinguish the strategy used.
- The evaluation strategy is deterministic and does not change based on your query history.
"""

    # -------------------------------------------------------------
    # 场景 2：医疗
    # -------------------------------------------------------------
    contextualized_rule_zh_2 = """\
欢迎进入“医疗疾控网络监测预警系统”。你需要推断疾控中心对各级监测单位的风险评估模型。

## 监测网设定

区域传染病监测网络由 {n} 个机构节点构成有向层级树，总疾控中心节点为 {root}。每个节点 v 记录了当下的单日新增病例数 val[v]。
医疗机构的上下级隶属关系（上级 -> 下级）及各节点的单日病例数据如下：

{tree_structure}

对于任意监测机构 u，系统会测算该节点及其下辖分支机构的两个关键风险指标：
- SUM(u)：节点 u 管辖范围内的总累计病例数。
- MAX(u)：节点 u 管辖范围内的聚集性感染极值（即单一下属机构报告的最高病例数）。

## 隐藏评估策略

系统对每个机构节点 u 配置了固定的风险评估策略 g(u)，要么采用 SUM 评估总量，要么采用 MAX 评估极值。
该策略仅依据节点的固有特征（如行政层级深度、管辖分支规模等）自动判定，且在监测周期内不变。

当你查询节点 u 的预警读数时，系统会返回 H(u) = g(u)(u)，即：
- 若 g(u) 为 SUM，则返回总累计病例数 SUM(u)
- 若 g(u) 为 MAX，则返回聚集性感染极值 MAX(u)

## 任务目标

你最多可以发送 {max_probes} 次查询请求来逆向推演该评估策略。查询结束后，系统会指定一组高风险目标机构，你需要正确测算它们的预警读数 H。

## 交互格式（必须严格遵守）

### 查询节点
使用以下格式查询节点 u 的预警读数（u 必须是有效节点编号）：
<query_probe>u</query_probe>

### 进入最终测验
当你准备好提交最终报告时，使用：
<query_final></query_final>
系统会返回需要你预测的目标机构列表。

### 提交最终答案
对目标节点列表中的所有节点提交预测值，格式如下：
<answer>u1:x1, u2:x2, u3:x3</answer>

其中 u1, u2, u3 等是目标机构编号，x1, x2, x3 等是你预测的预警读数。
节点顺序不限，但必须包含所有目标节点且每个节点恰好出现一次。

## 注意事项
- 查询次数有严格限制，请精确制导
- 建议挑选 SUM 与 MAX 不相等的机构节点进行查询，以提升信息获取效率
- 评估策略是确定且静态的
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Medical Disease Control Network Monitoring and Warning System". Your task is to infer the risk assessment model applied to monitoring units at all levels.

## Monitoring Network Setup

The regional infectious disease monitoring network consists of a directed hierarchical tree with {n} institutional nodes, with the main CDC node being {root}. Each node v records the current daily new cases val[v].
The hierarchical relationships (superior -> subordinate) and daily case data for each node are as follows:

{tree_structure}

For any monitoring institution u, the system calculates two key risk metrics for it and its subordinate branches:
- SUM(u): The total cumulative number of cases within node u's jurisdiction.
- MAX(u): The cluster infection peak within node u's jurisdiction (i.e., the highest case count reported by a single subordinate institution).

## Hidden Evaluation Strategy

The system configures a fixed risk assessment strategy g(u) for each institution u, which either uses SUM for total volume or MAX for peak severity.
This strategy is automatically determined based solely on inherent features (like administrative depth or branch scale) and remains constant during the monitoring cycle.

When you query the warning reading for node u, the system returns H(u) = g(u)(u), meaning:
- If g(u) is SUM, it returns the total cumulative cases SUM(u)
- If g(u) is MAX, it returns the cluster infection peak MAX(u)

## Task Objective

You can send at most {max_probes} query requests to reverse-engineer this assessment strategy. After the queries, the system will specify a set of high-risk target institutions, and you must correctly calculate their warning readings H.

## Interaction Format (must strictly follow)

### Query a node
Use the following format to query the warning reading of node u (u must be a valid node number):
<query_probe>u</query_probe>

### Enter final test
When you are ready to submit the final report, use:
<query_final></query_final>
The system will return the list of target institutions you need to predict.

### Submit final answer
Submit predicted values for all nodes in the target list in the following format:
<answer>u1:x1, u2:x2, u3:x3</answer>

Where u1, u2, u3, etc. are target institution numbers, and x1, x2, x3, etc. are your predicted warning readings.
The node order does not matter, but all target nodes must be included exactly once.

## Notes
- Query attempts are strictly limited; aim precisely.
- It is recommended to select institutions where SUM and MAX differ to maximize information gain.
- The evaluation strategy is deterministic and static.
"""

    # -------------------------------------------------------------
    # 场景 3：教育
    # -------------------------------------------------------------
    contextualized_rule_zh_3 = """\
欢迎访问“学区教育资源智能调配系统”。你需要摸清教育局对各级教学单位的资源评估测算规则。

## 调配网设定

学区资源网络是一棵包含 {n} 个节点的层级树（涵盖学区、学校、年级、班级等），顶层统筹节点为 {root}。每个节点 v 登记了当前的特需生基础人数 val[v]。
教学单位的隶属结构（上级 -> 下级）及各单位基础特需人数如下：

{tree_structure}

针对任意教育节点 u，系统会测算其管辖范围（含自身及所有下级单位）的两个需求指标：
- SUM(u)：节点 u 管辖范围内的总体特需生人数。
- MAX(u)：节点 u 管辖范围内的单点最大特需生人数（代表局部资源瓶颈）。

## 隐藏测算规则

教育局对每个节点 u 配置了一套固定的资源拨付测算规则 g(u)，必须是 SUM 或 MAX 二者选其一。
测算规则完全取决于节点的结构属性（比如在学区树中的深度或覆盖规模），在当前学期内固定不变。

当你查询节点 u 的测算值时，系统会返回 H(u) = g(u)(u)，即：
- 若 g(u) 为 SUM，则返回总体需求量 SUM(u)
- 若 g(u) 为 MAX，则返回局部瓶颈需求 MAX(u)

## 任务目标

你拥有的系统查询权限上限为 {max_probes} 次。利用这些次数推演隐藏的测算规则。查询阶段结束后，你需要为系统抽取的一批目标教学单位精准预测测算值 H。

## 交互格式（必须严格遵守）

### 查询节点
使用以下格式查询节点 u 的测算值（u 必须是有效节点编号）：
<query_probe>u</query_probe>

### 进入最终测验
当你准备好进行最终预测时，使用：
<query_final></query_final>
系统会返回目标教学单位列表。

### 提交最终答案
对目标节点列表中的所有节点提交预测值，格式如下：
<answer>u1:x1, u2:x2, u3:x3</answer>

其中 u1, u2, u3 等是单位编号，x1, x2, x3 等是你预测的资源测算值。
节点顺序不限，但必须包含所有目标节点且每个节点恰好出现一次。

## 注意事项
- 查询额度有限，请合理使用
- 建议针对 SUM 和 MAX 指标有差异的教学单位进行探查，方便比对
- 测算规则由内部算法决定，独立于你的查询记录
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "School District Educational Resource Intelligent Allocation System". You need to figure out the resource evaluation rules applied by the education bureau to various teaching units.

## Allocation Network Setup

The district resource network is a hierarchical tree containing {n} nodes (covering districts, schools, grades, classes, etc.), with the top-level coordinating node being {root}. Each node v records the current base number of special-needs students val[v].
The affiliation structure of teaching units (superior -> subordinate) and the base number for each unit are as follows:

{tree_structure}

For any educational node u, the system calculates two demand metrics for its jurisdiction (including itself and all subordinate units):
- SUM(u): The overall number of special-needs students within node u's jurisdiction.
- MAX(u): The single-point maximum number of special-needs students within node u's jurisdiction (representing a local resource bottleneck).

## Hidden Calculation Rule

The education bureau configures a fixed resource allocation rule g(u) for each node u, which must be either SUM or MAX.
The calculation rule completely depends on the node's structural properties (like depth in the district tree or coverage scale) and remains fixed for the current semester.

When you query the calculation value for node u, the system returns H(u) = g(u)(u), meaning:
- If g(u) is SUM, it returns the overall demand SUM(u)
- If g(u) is MAX, it returns the local bottleneck demand MAX(u)

## Task Objective

Your system query authorization is capped at {max_probes} attempts. Use them to deduce the hidden calculation rule. Once the query phase ends, you must accurately predict the calculation values H for a batch of target teaching units drawn by the system.

## Interaction Format (must strictly follow)

### Query a node
Use the following format to query the calculation value of node u (u must be a valid node number):
<query_probe>u</query_probe>

### Enter final test
When you are ready for the final prediction, use:
<query_final></query_final>
The system will return the list of target teaching units.

### Submit final answer
Submit predicted values for all nodes in the target list in the following format:
<answer>u1:x1, u2:x2, u3:x3</answer>

Where u1, u2, u3, etc. are unit numbers, and x1, x2, x3, etc. are your predicted resource calculation values.
The node order does not matter, but all target nodes must be included exactly once.

## Notes
- Query quota is limited; use it reasonably.
- It is advisable to probe teaching units where the SUM and MAX metrics differ for easier comparison.
- The calculation rule is determined by an internal algorithm and is independent of your query history.
"""

    # -------------------------------------------------------------
    # 场景 4：制造业/工业
    # -------------------------------------------------------------
    contextualized_rule_zh_4 = """\
欢迎使用“智能工厂产能监控与排程系统”。你需要破解各级生产单元的绩效考核评估策略。

## 生产排程网设定

工厂的生产调度网络由 {n} 个层级节点构成，总控中心为 {root}。每个节点 v（代表车间、产线或单一设备）具备基础的日均产出件数 val[v]。
生产单元的归属关系（上游 -> 下游设备/工位）及基础产量数据如下：

{tree_structure}

针对任意生产节点 u，控制台会聚合其下辖生产树（含自身）的两个产能指标：
- SUM(u)：节点 u 整个下辖体系的总产出汇总。
- MAX(u)：节点 u 整个下辖体系中，产出最高的单点单元峰值产量。

## 隐藏评估策略

系统内核为每个节点 u 绑定了既定的产能审核标准 g(u)，要么审核总量(SUM)，要么审核峰值(MAX)。
考核标准仅与生产节点在网络中的层级、负荷范围等可见架构属性相关，且在整个班次内不可篡改。

当你调用节点 u 的考核值时，系统会返回 H(u) = g(u)(u)，即：
- 若标准 g(u) 为 SUM，则返回总产出 SUM(u)
- 若标准 g(u) 为 MAX，则返回单点峰值 MAX(u)

## 任务目标

你被授权最多 {max_probes} 次查询指令来推演该评估标准。当诊断阶段完成，你需要对系统随机抽检的一组目标生产节点给出精准的考核值 H 预测。

## 交互格式（必须严格遵守）

### 查询节点
使用以下格式查询节点 u 的考核值（u 必须是有效节点编号）：
<query_probe>u</query_probe>

### 进入最终测验
当你准备好执行最终系统抽检时，使用：
<query_final></query_final>
系统会返回抽检目标节点列表。

### 提交最终答案
对目标节点列表中的所有节点提交预测值，格式如下：
<answer>u1:x1, u2:x2, u3:x3</answer>

其中 u1, u2, u3 等是目标节点编号，x1, x2, x3 等是你预测的对应考核值。
节点顺序不限，但必须包含所有目标节点且每个节点恰好出现一次。

## 注意事项
- 查询指令次数受限，请谨慎规划探测点
- 建议锁定那些总产出与单点峰值不同的节点进行查询，以获取更多有效信息
- 评估策略是绝对确定的物理规则，不随查询动态变化
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Smart Factory Capacity Monitoring and Scheduling System". Your task is to decode the performance evaluation strategies of various production units.

## Production Scheduling Network Setup

The factory's production scheduling network consists of {n} hierarchical nodes, with the main control center being {root}. Each node v (representing a workshop, production line, or single machine) has a basic daily output count val[v].
The affiliation relationships of production units (upstream -> downstream equipment/stations) and basic output data are as follows:

{tree_structure}

For any production node u, the console aggregates two capacity metrics for its subordinate production tree (including itself):
- SUM(u): The total aggregated output of node u's entire subordinate system.
- MAX(u): The peak output of the single highest-producing unit within node u's subordinate system.

## Hidden Evaluation Strategy

The system kernel binds a set capacity audit standard g(u) to each node u, checking either the total volume (SUM) or the peak (MAX).
The standard is only related to visible architectural properties like the node's level in the network and load scope, and cannot be tampered with throughout the shift.

When you call the audit value of node u, the system returns H(u) = g(u)(u), meaning:
- If the standard g(u) is SUM, it returns the total output SUM(u)
- If the standard g(u) is MAX, it returns the single-point peak MAX(u)

## Task Objective

You are authorized for at most {max_probes} query commands to deduce this evaluation standard. Once the diagnostic phase is complete, you must provide precise predictions of the audit values H for a group of target production nodes randomly selected by the system for inspection.

## Interaction Format (must strictly follow)

### Query a node
Use the following format to query the audit value of node u (u must be a valid node number):
<query_probe>u</query_probe>

### Enter final test
When you are ready to execute the final system inspection, use:
<query_final></query_final>
The system will return the list of inspected target nodes.

### Submit final answer
Submit predicted values for all nodes in the target list in the following format:
<answer>u1:x1, u2:x2, u3:x3</answer>

Where u1, u2, u3, etc. are target node numbers, and x1, x2, x3, etc. are your predicted audit values.
The node order does not matter, but all target nodes must be included exactly once.

## Notes
- Query commands are limited; plan your probe points carefully.
- It is recommended to target nodes where total output and single-point peak differ to gather more effective information.
- The evaluation strategy is an absolutely deterministic physical rule, unchanging regardless of your queries.
"""

    # -------------------------------------------------------------
    # 场景 5：法律
    # -------------------------------------------------------------
    contextualized_rule_zh_5 = """\
欢迎登录“司法辖区案件积压督办系统”。你的目标是解构上级法院对不同层级司法机构的督办核查规则。

## 司法网络设定

本辖区的司法层级体系可视为包含 {n} 个机构节点的树状结构，最高法院节点为 {root}。每个节点 v 记录着该独立机构当前的未结积压案件数 val[v]。
法院间的层级管辖关系（上级法院 -> 下级法院/法庭）及各机构未结案件数据如下：

{tree_structure}

针对辖区内任意司法机构 u，系统会统计该节点及其下级所有机构的案件积压状况：
- SUM(u)：节点 u 管辖范围（含本机构）的总体积压案件总量。
- MAX(u)：节点 u 管辖范围（含本机构）内，单家法院/法庭面对的最高积压案件数（代表最重负荷点）。

## 隐藏核查规则

系统为每个司法机构 u 制定了固定的案件督办核查规则 g(u)，该规则要么评估总量(SUM)，要么评估极值(MAX)。
核查规则完全由机构的结构定位（如管辖深度、下属单位数量等）决定，并在本轮督办周期内保持恒定。

当你调阅机构 u 的督办核查值时，系统会返回 H(u) = g(u)(u)，即：
- 若 g(u) 为 SUM，则返回总体积压量 SUM(u)
- 若 g(u) 为 MAX，则返回最高单点积压量 MAX(u)

## 任务目标

你最多拥有 {max_probes} 次查询权限来破解这套督办核查规则。查询结束时，系统将派发一批重点督办的目标法院名单，你需要准确预测它们的督办核查值 H。

## 交互格式（必须严格遵守）

### 查询节点
使用以下格式调阅机构 u 的核查值（u 必须是有效节点编号）：
<query_probe>u</query_probe>

### 进入最终测验
当你准备好应对最终督办考核时，使用：
<query_final></query_final>
系统会返回需要你预测的目标司法机构列表。

### 提交最终答案
对目标节点列表中的所有节点提交预测值，格式如下：
<answer>u1:x1, u2:x2, u3:x3</answer>

其中 u1, u2, u3 等是机构编号，x1, x2, x3 等是你推算的督办核查值。
节点顺序不限，但必须包含所有目标节点且每个节点恰好出现一次。

## 注意事项
- 查询权限次数有限，请讲究策略
- 建议查询辖区总量与单点极值不一致的机构节点，以判别其评估基准
- 核查规则是确定的内部机制，不会受查询动作干扰
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial District Case Backlog Supervision System". Your objective is to deconstruct the supervisory verification rules applied by higher courts to different tiers of judicial institutions.

## Judicial Network Setup

The judicial hierarchy of this district is structured as a tree containing {n} institutional nodes, with the highest court being node {root}. Each node v records the current number of unsettled backlog cases val[v] for that independent institution.
The hierarchical jurisdictional relationships between courts (superior court -> lower court/tribunal) and the unsettled case data of each institution are as follows:

{tree_structure}

For any judicial institution u in the district, the system tallies the case backlog conditions for it and all its subordinate institutions:
- SUM(u): The overall total volume of backlog cases within node u's jurisdiction (including itself).
- MAX(u): The highest number of backlog cases faced by a single court/tribunal within node u's jurisdiction (including itself), representing the point of heaviest load.

## Hidden Verification Rule

The system has established a fixed case supervision verification rule g(u) for each institution u, evaluating either the total volume (SUM) or the extreme value (MAX).
The verification rule is determined entirely by the institution's structural positioning (e.g., jurisdictional depth, number of subordinate units) and remains constant throughout the current supervision cycle.

When you access the supervisory verification value for institution u, the system returns H(u) = g(u)(u), meaning:
- If g(u) is SUM, it returns the overall backlog volume SUM(u)
- If g(u) is MAX, it returns the highest single-point backlog MAX(u)

## Task Objective

You have a maximum of {max_probes} query permissions to crack this supervisory verification rule. At the end of the queries, the system will dispatch a list of key target courts for supervision, and you must accurately predict their verification values H.

## Interaction Format (must strictly follow)

### Query a node
Use the following format to access the verification value of institution u (u must be a valid node number):
<query_probe>u</query_probe>

### Enter final test
When you are ready to face the final supervisory assessment, use:
<query_final></query_final>
The system will return the list of target judicial institutions you need to predict.

### Submit final answer
Submit predicted values for all nodes in the target list in the following format:
<answer>u1:x1, u2:x2, u3:x3</answer>

Where u1, u2, u3, etc. are institution numbers, and x1, x2, x3, etc. are your calculated verification values.
The node order does not matter, but all target nodes must be included exactly once.

## Notes
- Query permissions are limited; be strategic.
- It is advisable to query institutional nodes where total volume and single-point extremes differ, to distinguish the evaluation baseline.
- The verification rule is a deterministic internal mechanism unaffected by query actions.
"""

    tags = ["answer", "query_probe", "query_final"]
    
    # 类属性：推理类型、数据结构
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置：
    # 1 (简单)      - 小树，规则：深度奇偶
    # 2 (中等偏下)  - 中等树，规则：子树大小奇偶
    # 3 (中等偏上)  - 中等树，规则：是否为叶子节点
    # 4 (较难)      - 较大树，规则：子树大小模3
    # 5 (难)        - 大树，规则：深度模3与子树大小奇偶的组合

    DIFFICULTY_CONFIG = {
        1: {
            "n": 7,
            "root": 1,
            "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
            "values": {1: 5, 2: 3, 3: 8, 4: 2, 5: 1, 6: 4, 7: 6},
            "rule_type": "depth_parity",  # 深度为奇数用SUM，偶数用MAX
            "max_probes": 4,
            "target_count": 2,
        },
        2: {
            "n": 10,
            "root": 1,
            "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (5, 9), (6, 10)],
            "values": {1: 10, 2: 5, 3: 7, 4: 3, 5: 2, 6: 4, 7: 6, 8: 1, 9: 8, 10: 9},
            "rule_type": "subtree_size_parity",  # 子树大小为奇数用MAX，偶数用SUM
            "max_probes": 5,
            "target_count": 3,
        },
        3: {
            "n": 12,
            "root": 1,
            "edges": [(1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (4, 9), (5, 10), (7, 11), (8, 12)],
            "values": {1: 15, 2: 8, 3: 12, 4: 6, 5: 4, 6: 3, 7: 9, 8: 2, 9: 5, 10: 7, 11: 10, 12: 1},
            "rule_type": "is_leaf",  # 叶子节点用SUM，非叶子用MAX
            "max_probes": 6,
            "target_count": 3,
        },
        4: {
            "n": 15,
            "root": 1,
            "edges": [
                (1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (3, 8),
                (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (9, 14), (10, 15)
            ],
            "values": {1: 20, 2: 10, 3: 15, 4: 5, 5: 8, 6: 12, 7: 6, 8: 9, 9: 3, 10: 4, 11: 7, 12: 11, 13: 2, 14: 1, 15: 13},
            "rule_type": "subtree_size_mod3",  # 子树大小模3: 0→SUM, 1→MAX, 2→SUM
            "max_probes": 7,
            "target_count": 4,
        },
        5: {
            "n": 20,
            "root": 1,
            "edges": [
                (1, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (4, 10),
                (5, 11), (6, 12), (7, 13), (8, 14), (9, 15), (10, 16), (11, 17), (12, 18),
                (13, 19), (14, 20)
            ],
            "values": {
                1: 25, 2: 18, 3: 22, 4: 14, 5: 9, 6: 11, 7: 16, 8: 13, 9: 7, 10: 8,
                11: 4, 12: 5, 13: 12, 14: 6, 15: 3, 16: 10, 17: 2, 18: 15, 19: 1, 20: 19
            },
            "rule_type": "depth_mod3_and_size_parity",  # (深度模3==1 且 子树大小为偶)→MAX，否则→SUM
            "max_probes": 8,
            "target_count": 5,
        },
    }

    def __init__(self, config):
        # 先初始化游戏数据，再调用父类初始化
        self._pre_initialize_game(config)
        super().__init__(config)

    def _pre_initialize_game(self, config):
        """在父类初始化前准备游戏数据"""
        diff = config.difficulty
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.n = cfg["n"]
        self.root = cfg["root"]
        self.edges = cfg["edges"]
        self.values = cfg["values"]
        self.rule_type = cfg["rule_type"]
        self.max_probes = cfg["max_probes"]
        self.target_count = cfg["target_count"]

        # 构建树结构
        self.children = {i: [] for i in range(1, self.n + 1)}
        for parent, child in self.edges:
            self.children[parent].append(child)

        # 计算每个节点的深度、子树大小、SUM和MAX
        self._compute_tree_properties()

        # 根据规则类型计算每个节点的g函数（SUM或MAX）
        self._compute_hidden_rule()

        # 游戏状态
        self.probe_count = 0
        self.in_final_phase = False
        self.target_nodes = []

    def _initialize_game(self):
        """初始化游戏信息用于规则模板"""
        # 构建树结构描述
        if self.config.language == "zh":
            structure_lines = ["节点属性值："]
            for i in range(1, self.n + 1):
                structure_lines.append(f"  节点 {i}: val = {self.values[i]}")
            structure_lines.append("\n父子关系（父 -> 子）：")
            for parent, child in self.edges:
                structure_lines.append(f"  {parent} -> {child}")
        else:
            structure_lines = ["Node attribute values:"]
            for i in range(1, self.n + 1):
                structure_lines.append(f"  Node {i}: val = {self.values[i]}")
            structure_lines.append("\nParent-child relationships (parent -> child):")
            for parent, child in self.edges:
                structure_lines.append(f"  {parent} -> {child}")

        self._game_info["n"] = self.n
        self._game_info["root"] = self.root
        self._game_info["tree_structure"] = "\n".join(structure_lines)
        self._game_info["max_probes"] = self.max_probes

    def _compute_tree_properties(self):
        """计算每个节点的深度、子树大小、SUM和MAX"""
        self.depth = {}
        self.subtree_size = {}
        self.subtree_sum = {}
        self.subtree_max = {}

        def dfs(node, d):
            self.depth[node] = d
            self.subtree_sum[node] = self.values[node]
            self.subtree_max[node] = self.values[node]
            self.subtree_size[node] = 1

            for child in self.children[node]:
                dfs(child, d + 1)
                self.subtree_sum[node] += self.subtree_sum[child]
                self.subtree_max[node] = max(self.subtree_max[node], self.subtree_max[child])
                self.subtree_size[node] += self.subtree_size[child]

        dfs(self.root, 0)

    def _compute_hidden_rule(self):
        """根据规则类型计算每个节点应返回SUM还是MAX"""
        self.node_rule = {}  # 存储每个节点应该用SUM还是MAX

        for node in range(1, self.n + 1):
            if self.rule_type == "depth_parity":
                # 深度为奇数用SUM，偶数用MAX
                self.node_rule[node] = "SUM" if self.depth[node] % 2 == 1 else "MAX"

            elif self.rule_type == "subtree_size_parity":
                # 子树大小为奇数用MAX，偶数用SUM
                self.node_rule[node] = "MAX" if self.subtree_size[node] % 2 == 1 else "SUM"

            elif self.rule_type == "is_leaf":
                # 非叶子节点用MAX，叶子用SUM（叶子SUM==MAX，所以关键区分在非叶子）
                is_leaf = len(self.children[node]) == 0
                self.node_rule[node] = "SUM" if is_leaf else "MAX"

            elif self.rule_type == "subtree_size_mod3":
                # 子树大小模3: 0→SUM, 1→MAX, 2→SUM
                mod_val = self.subtree_size[node] % 3
                self.node_rule[node] = "MAX" if mod_val == 1 else "SUM"

            elif self.rule_type == "depth_mod3_and_size_parity":
                # (深度模3==1 且 子树大小为偶)→MAX，否则→SUM
                depth_mod = self.depth[node] % 3
                size_even = self.subtree_size[node] % 2 == 0
                self.node_rule[node] = "MAX" if (depth_mod == 1 and size_even) else "SUM"

            else:
                raise ValueError(f"Unknown rule type: {self.rule_type}")

    def _get_h_value(self, node):
        """获取节点的H值"""
        if self.node_rule[node] == "SUM":
            return self.subtree_sum[node]
        else:
            return self.subtree_max[node]

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        # 如果 target_nodes 为空，尝试按照规则生成它们（兼容冗余性评测场景）
        if not self.target_nodes:
            rng = random.Random(self.config.difficulty * 100)
            candidates = [node for node in range(1, self.n + 1)
                          if self.subtree_sum[node] != self.subtree_max[node]]
            if len(candidates) < self.target_count:
                candidates = list(range(1, self.n + 1))
            self.target_nodes = sorted(rng.sample(candidates, min(self.target_count, len(candidates))))
            self.in_final_phase = True

        if not self.in_final_phase or not self.target_nodes:
            return False

        raw_ans = parsed_info.get("answer", "").strip()
        
        # 解析答案格式：u1:x1, u2:x2, ...
        try:
            pairs = [p.strip() for p in raw_ans.split(",")]
            ans_dict = {}
            for pair in pairs:
                if ":" not in pair:
                    return False
                node_str, value_str = pair.split(":", 1)
                node = int(node_str.strip())
                value = int(value_str.strip())
                ans_dict[node] = value
        except:
            return False

        # 检查是否包含所有目标节点且无多余节点
        if set(ans_dict.keys()) != set(self.target_nodes):
            return False

        # 检查每个节点的H值是否正确
        for node in self.target_nodes:
            if ans_dict[node] != self._get_h_value(node):
                return False

        return True

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑，处理查询并产生响应"""
        lang = self.config.language

        # 处理探测查询
        if "query_probe" in parsed_info:
            if self.in_final_phase:
                return "错误：已进入最终测验阶段，无法继续查询。" if lang == "zh" else "Error: Already in final test phase, cannot continue querying."

            if self.probe_count >= self.max_probes:
                return f"错误：已达到最大查询次数 {self.max_probes}。" if lang == "zh" else f"Error: Maximum query limit {self.max_probes} reached."

            try:
                node = int(parsed_info["query_probe"].strip())
                if node < 1 or node > self.n:
                    return "错误：节点编号超出范围。" if lang == "zh" else "Error: Node number out of range."

                self.probe_count += 1
                h_value = self._get_h_value(node)
                remain = self.max_probes - self.probe_count

                if lang == "zh":
                    return f"H({node}) = {h_value}\n剩余查询次数: {remain}"
                else:
                    return f"H({node}) = {h_value}\nRemaining queries: {remain}"

            except ValueError:
                return "错误：无效的节点编号格式。" if lang == "zh" else "Error: Invalid node number format."

        # 处理进入最终阶段
        elif "query_final" in parsed_info:
            if self.in_final_phase:
                return "错误：已经在最终测验阶段。" if lang == "zh" else "Error: Already in final test phase."

            self.in_final_phase = True
            
            # 随机选择目标节点（确保它们的SUM和MAX不同，以便测试有意义）
            candidates = [node for node in range(1, self.n + 1) 
                         if self.subtree_sum[node] != self.subtree_max[node]]
            
            if len(candidates) < self.target_count:
                # 如果候选不足，从所有节点中选择
                candidates = list(range(1, self.n + 1))
            
            # 使用固定种子确保难度一致性
            rng = random.Random(self.config.difficulty * 100)
            self.target_nodes = sorted(rng.sample(candidates, min(self.target_count, len(candidates))))

            if lang == "zh":
                nodes_str = ", ".join(map(str, self.target_nodes))
                return f"最终测验阶段开始。\n目标节点列表: {nodes_str}\n请对这些节点提交预测的 H 值。"
            else:
                nodes_str = ", ".join(map(str, self.target_nodes))
                return f"Final test phase begins.\nTarget node list: {nodes_str}\nPlease submit predicted H values for these nodes."

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案：修改响应中的 H 值"""
        import re as _re
        # 尝试匹配 H(x) = y 格式并修改数值
        match = _re.search(r'(H\(\d+\)\s*=\s*)(\d+)', correct)
        if match:
            original_val = int(match.group(2))
            wrong_val = original_val + random.choice([1, 2, 3, -1, -2])
            if wrong_val < 0:
                wrong_val = original_val + 3
            if wrong_val == original_val:
                wrong_val = original_val + 1
            return correct[:match.start(2)] + str(wrong_val) + correct[match.end(2):]

        # fallback
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            # 简单的英文 Yes/No 替换
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            elif "No" in correct:
                return correct.replace("No", "Yes")
            elif "yes" in correct:
                return correct.replace("yes", "no")
            elif "no" in correct:
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        包含所有节点的 probe 查询和一个 final 查询（触发最终阶段）。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,
                "answer": str,
            }
        """
        possible_queries = []
        lang = self.config.language

        for node in range(1, self.n + 1):
            h_value = self._get_h_value(node)

            if lang == "zh":
                ans = f"H({node}) = {h_value}"
            else:
                ans = f"H({node}) = {h_value}"

            possible_queries.append({
                "query": f"<query_probe>{node}</query_probe>",
                "answer": ans
            })

        # 添加 query_final 以触发最终阶段并展示目标节点
        # 先模拟触发最终阶段来获取目标节点列表
        rng = random.Random(self.config.difficulty * 100)
        candidates = [node for node in range(1, self.n + 1)
                      if self.subtree_sum[node] != self.subtree_max[node]]
        if len(candidates) < self.target_count:
            candidates = list(range(1, self.n + 1))
        target_nodes = sorted(rng.sample(candidates, min(self.target_count, len(candidates))))
        nodes_str = ", ".join(map(str, target_nodes))

        if lang == "zh":
            final_ans = f"最终测验阶段开始。\n目标节点列表: {nodes_str}\n请对这些节点提交预测的 H 值。"
        else:
            final_ans = f"Final test phase begins.\nTarget node list: {nodes_str}\nPlease submit predicted H values for these nodes."

        possible_queries.append({
            "query": "<query_final></query_final>",
            "answer": final_ans
        })

        return possible_queries