# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   删节点后连通性：删除某节点后，连通分量数量如何变化
# ============================================================

from .base import Game
import random


class GraphNodeRemovalGame(Game):

    game_rule_zh = """\
我们来玩一个"图节点删除推理"游戏，规则如下：

游戏设定了一张连通无向图 G，节点命名采用分层结构：
- 主干节点：S-1, S-2, ..., S-H（至少3个），主干节点之间依次相连
- 支节点：每个主干节点 S-j 可能挂接若干支节点，命名为 S-j-1, S-j-2, ...
- 叶节点：每个支节点 S-j-k 可能挂接若干叶节点，命名为 S-j-k-1, S-j-k-2, ...

你会得到以下信息：
1. 所有节点的名称列表（共 {total_nodes} 个节点）
2. 一个目标集合 T，包含 {target_size} 个节点：{target_nodes}
3. 查询预算 {query_budget} 次
4. 目标计数值 {target_count}

你的任务分为三个阶段：

**阶段一：试删查询（消耗预算）**
你可以选择任意不在目标集合 T 中的节点进行"试删查询"，询问：如果从原图中删除该节点及其关联的所有边，图会分裂成多少个连通分量？
每次查询会消耗1次预算，共有 {query_budget} 次查询机会。

**阶段二：预测目标集合（不消耗预算）**
基于你的查询结果，推断并预测目标集合 T 中每个节点的删除分量数（即删除该节点后图会分裂成多少个连通分量）。

**阶段三：最终选择（不消耗预算）**
从所有未被查询过的节点中，选择一个节点，使得删除该节点后的连通分量数恰好等于目标计数值 {target_count}。

## 交互格式（必须严格遵守）

每次只能包含一个操作标签：

- 试删查询（例如查询节点 S-2-1）：
<query_removal>S-2-1</query_removal>

- 提交目标集合预测（必须包含目标集合中所有节点的预测，格式为"节点名=分量数"，用逗号分隔）：
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- 最终选择（选择一个未查询过的节点）：
<answer>S-2-3</answer>

## 注意事项
- 试删查询不能查询目标集合 T 中的节点
- 预测阶段必须对目标集合 T 中的所有节点给出预测
- 最终选择的节点必须是未被查询过的节点
- 查询预算用完后不能再进行试删查询
- 请尽可能少地使用查询次数
"""

    game_rule_en = """\
Let's play a "Graph Node Removal Reasoning" game. Here are the rules:

The game features a connected undirected graph G with a hierarchical node naming structure:
- Backbone nodes: S-1, S-2, ..., S-H (at least 3), connected sequentially
- Branch nodes: Each backbone node S-j may have attached branch nodes named S-j-1, S-j-2, ...
- Leaf nodes: Each branch node S-j-k may have attached leaf nodes named S-j-k-1, S-j-k-2, ...

You will be given:
1. A list of all node names (total {total_nodes} nodes)
2. A target set T containing {target_size} nodes: {target_nodes}
3. A query budget of {query_budget} queries
4. A target count value of {target_count}

Your task has three phases:

**Phase 1: Removal Queries (consumes budget)**
You can select any node NOT in target set T for a "removal query", asking: if this node and all its edges are removed from the graph, how many connected components would result?
Each query consumes 1 budget unit, with a total of {query_budget} queries available.

**Phase 2: Predict Target Set (does not consume budget)**
Based on your query results, infer and predict the removal component count for each node in target set T (i.e., how many connected components would result from removing that node).

**Phase 3: Final Selection (does not consume budget)**
From all unqueried nodes, select one node such that removing it results in exactly {target_count} connected components.

## Interaction Format (must strictly follow)

Each interaction must contain only one operation tag:

- Removal Query (e.g., querying node S-2-1):
<query_removal>S-2-1</query_removal>

- Submit Target Set Prediction (must include predictions for all nodes in target set, format "node=count", comma-separated):
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- Final Selection (select one unqueried node):
<answer>S-2-3</answer>

## Important Notes
- Removal queries cannot query nodes in target set T
- Prediction phase must provide predictions for all nodes in target set T
- Final selection must be an unqueried node
- No more removal queries after budget is exhausted
- Try to use as few queries as possible
"""

    contextualized_rule_zh_1 = """\
欢迎接入"城市轨道交通应急演练系统"。

目前我们正在对本市的连通轨道交通网络 G 进行停运影响评估。站点命名采用分层结构：
- 主干枢纽站：S-1, S-2, ..., S-H（至少3个），主干枢纽之间依次相连构成本市交通动脉。
- 支线换乘站：每个主干枢纽 S-j 可能接驳若干支线换乘站，命名为 S-j-1, S-j-2, ...
- 末端站点：每个支线换乘站 S-j-k 可能延伸出若干末端站点，命名为 S-j-k-1, S-j-k-2, ...

你会得到以下系统信息：
1. 路网全量站点列表（共 {total_nodes} 个站点）
2. 重点监控集合 T，包含 {target_size} 个核心站点：{target_nodes}
3. 演练预算 {query_budget} 次
4. 目标切分区块数 {target_count}

你的任务分为三个阶段：

**阶段一：停运演练（消耗预算）**
你可以选择任意不在监控集合 T 中的站点进行"停运演练"，询问：如果关闭该站点及其所有进出线路，整个路网会分裂成多少个互相无法通达的独立区块（连通分量）？
每次演练消耗1次预算，共有 {query_budget} 次机会。

**阶段二：预测监控集合（不消耗预算）**
基于演练结果，推断并预测监控集合 T 中每个站点的停运影响（即关闭该站后路网会分裂成多少个独立区块）。

**阶段三：最终选择（不消耗预算）**
从所有未被演练过的站点中，选择一个站点，使得关闭该站后的独立区块数恰好等于目标切分区块数 {target_count}。

## 交互格式（必须严格遵守）

每次只能包含一个操作标签：

- 停运演练（例如演练站点 S-2-1）：
<query_removal>S-2-1</query_removal>

- 提交监控集合预测（必须包含集合中所有站点的预测，格式为"站点名=区块数"，用逗号分隔）：
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- 最终选择（选择一个未演练过的站点）：
<answer>S-2-3</answer>

## 注意事项
- 停运演练不能查询监控集合 T 中的站点
- 预测阶段必须对集合 T 中的所有站点给出预测
- 最终选择的站点必须是未被演练过的
- 演练预算用完后不能再进行停运演练
- 请尽可能少地消耗演练次数
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Urban Rail Transit Emergency Drill System".

We are currently evaluating the outage impact on the city's connected rail network G. Station naming follows a hierarchical structure:
- Backbone Hubs: S-1, S-2, ..., S-H (at least 3), connected sequentially forming the city's transit artery.
- Branch Transfer Stations: Each backbone hub S-j may connect to several branch stations named S-j-1, S-j-2, ...
- Terminal Stations: Each branch station S-j-k may extend to several terminal stations named S-j-k-1, S-j-k-2, ...

You will receive the following system information:
1. Complete list of all stations (total {total_nodes} stations)
2. A critical monitoring set T containing {target_size} core stations: {target_nodes}
3. A drill budget of {query_budget} queries
4. A target isolated block count of {target_count}

Your task has three phases:

**Phase 1: Outage Drills (consumes budget)**
You can select any station NOT in monitoring set T for an "outage drill", asking: if this station and all its connected tracks are closed, how many isolated transit blocks (connected components) would the network split into?
Each drill consumes 1 budget unit, with a total of {query_budget} drills available.

**Phase 2: Predict Monitoring Set (does not consume budget)**
Based on your drill results, infer and predict the outage impact for each station in monitoring set T (i.e., how many isolated blocks would result from closing that station).

**Phase 3: Final Selection (does not consume budget)**
From all undrilled stations, select one station such that closing it results in exactly {target_count} isolated blocks.

## Interaction Format (must strictly follow)

Each interaction must contain only one operation tag:

- Outage Drill (e.g., drilling station S-2-1):
<query_removal>S-2-1</query_removal>

- Submit Monitoring Set Prediction (must include predictions for all stations in the set, format "station=count", comma-separated):
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- Final Selection (select one undrilled station):
<answer>S-2-3</answer>

## Important Notes
- Outage drills cannot query stations in monitoring set T
- Prediction phase must provide predictions for all stations in set T
- Final selection must be an undrilled station
- No more outage drills after budget is exhausted
- Try to use as few drills as possible
"""

    contextualized_rule_zh_2 = """\
欢迎接入"区域医疗资源隔离调度系统"。

目前我们正在推演本区域连通医疗协同网络 G 的封控影响。医疗机构命名采用分层结构：
- 省级总院：S-1, S-2, ..., S-H（至少3个），省级总院之间依次相连构成核心调度主干。
- 市级分院：每个省级总院 S-j 可能下辖若干市级分院，命名为 S-j-1, S-j-2, ...
- 社区卫生站：每个市级分院 S-j-k 可能管辖若干社区卫生服务站，命名为 S-j-k-1, S-j-k-2, ...

你会得到以下系统信息：
1. 全网医疗机构列表（共 {total_nodes} 个节点）
2. 高危监控集合 T，包含 {target_size} 个重点机构：{target_nodes}
3. 模拟熔断预算 {query_budget} 次
4. 目标独立运作区域数 {target_count}

你的任务分为三个阶段：

**阶段一：熔断模拟（消耗预算）**
你可以选择任意不在高危集合 T 中的机构进行"熔断模拟"，询问：如果因感染封控该机构及其所有协同通道，整个医疗网络会分裂成多少个互相隔离的独立运作区域（连通分量）？
每次模拟消耗1次预算，共有 {query_budget} 次机会。

**阶段二：预测高危集合（不消耗预算）**
基于模拟结果，推断并预测高危集合 T 中每个机构的封控影响（即封控该机构后网络会分裂成多少个独立运作区域）。

**阶段三：最终选择（不消耗预算）**
从所有未被模拟过的机构中，选择一个机构，使得封控该机构后的独立区域数恰好等于目标独立运作区域数 {target_count}。

## 交互格式（必须严格遵守）

每次只能包含一个操作标签：

- 熔断模拟（例如模拟封控机构 S-2-1）：
<query_removal>S-2-1</query_removal>

- 提交高危集合预测（必须包含集合中所有机构的预测，格式为"机构名=区域数"，用逗号分隔）：
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- 最终选择（选择一个未模拟过的机构）：
<answer>S-2-3</answer>

## 注意事项
- 熔断模拟不能查询高危集合 T 中的机构
- 预测阶段必须对集合 T 中的所有机构给出预测
- 最终选择的机构必须是未被模拟过的
- 模拟预算用完后不能再进行熔断模拟
- 请尽可能少地消耗模拟次数
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Regional Medical Resource Isolation and Dispatch System".

We are deducing the lockdown impact on the region's connected medical synergy network G. The naming of medical institutions follows a hierarchical structure:
- Provincial General Hospitals: S-1, S-2, ..., S-H (at least 3), connected sequentially forming the core dispatch backbone.
- Municipal Branch Hospitals: Each provincial hospital S-j may govern several branch hospitals named S-j-1, S-j-2, ...
- Community Health Clinics: Each branch hospital S-j-k may oversee several community clinics named S-j-k-1, S-j-k-2, ...

You will receive the following system information:
1. Complete list of all institutions (total {total_nodes} nodes)
2. A high-risk monitoring set T containing {target_size} critical institutions: {target_nodes}
3. A simulation budget of {query_budget} queries
4. A target isolated operational region count of {target_count}

Your task has three phases:

**Phase 1: Lockdown Simulations (consumes budget)**
You can select any institution NOT in high-risk set T for a "lockdown simulation", asking: if this institution and all its synergy channels are locked down due to infection, how many isolated operational regions (connected components) would the network split into?
Each simulation consumes 1 budget unit, with a total of {query_budget} simulations available.

**Phase 2: Predict High-Risk Set (does not consume budget)**
Based on your simulation results, infer and predict the lockdown impact for each institution in high-risk set T (i.e., how many isolated operational regions would result from locking down that institution).

**Phase 3: Final Selection (does not consume budget)**
From all unsimulated institutions, select one institution such that locking it down results in exactly {target_count} isolated operational regions.

## Interaction Format (must strictly follow)

Each interaction must contain only one operation tag:

- Lockdown Simulation (e.g., simulating lockdown of institution S-2-1):
<query_removal>S-2-1</query_removal>

- Submit High-Risk Set Prediction (must include predictions for all institutions in the set, format "institution=count", comma-separated):
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- Final Selection (select one unsimulated institution):
<answer>S-2-3</answer>

## Important Notes
- Lockdown simulations cannot query institutions in high-risk set T
- Prediction phase must provide predictions for all institutions in set T
- Final selection must be an unsimulated institution
- No more lockdown simulations after budget is exhausted
- Try to use as few simulations as possible
"""

    contextualized_rule_zh_3 = """\
欢迎接入"分布式在线教育网络运维平台"。

目前我们正在评估连通教育资源分发网络 G 的设备下线维护影响。服务器节点命名采用分层结构：
- 大区数据中心：S-1, S-2, ..., S-H（至少3个），大区中心之间依次相连构成核心骨干网。
- 市级分发节点：每个大区中心 S-j 可能挂接若干市级教育节点，命名为 S-j-1, S-j-2, ...
- 校级终端服务器：每个市级节点 S-j-k 可能连接若干校级终端，命名为 S-j-k-1, S-j-k-2, ...

你会得到以下系统信息：
1. 全网服务器节点列表（共 {total_nodes} 个节点）
2. 核心观测集合 T，包含 {target_size} 个关键服务器：{target_nodes}
3. 维护演练预算 {query_budget} 次
4. 目标局域网孤岛数 {target_count}

你的任务分为三个阶段：

**阶段一：下线演练（消耗预算）**
你可以选择任意不在核心集合 T 中的服务器进行"下线演练"，询问：如果将该服务器关机断网并切断所有通信链路，整个教育网络会分裂成多少个互相断连的局域网孤岛（连通分量）？
每次演练消耗1次预算，共有 {query_budget} 次机会。

**阶段二：预测核心集合（不消耗预算）**
基于演练结果，推断并预测核心集合 T 中每个服务器的下线影响（即下线该服务器后网络会分裂成多少个局域网孤岛）。

**阶段三：最终选择（不消耗预算）**
从所有未被演练过的服务器中，选择一个服务器，使得下线该服务器后的局域网孤岛数恰好等于目标孤岛数 {target_count}。

## 交互格式（必须严格遵守）

每次只能包含一个操作标签：

- 下线演练（例如演练服务器 S-2-1）：
<query_removal>S-2-1</query_removal>

- 提交核心集合预测（必须包含集合中所有服务器的预测，格式为"服务器名=孤岛数"，用逗号分隔）：
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- 最终选择（选择一个未演练过的服务器）：
<answer>S-2-3</answer>

## 注意事项
- 下线演练不能查询核心集合 T 中的服务器
- 预测阶段必须对集合 T 中的所有服务器给出预测
- 最终选择的服务器必须是未被演练过的
- 演练预算用完后不能再进行下线演练
- 请尽可能少地消耗演练次数
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Distributed Online Education Network Maintenance Platform".

We are assessing the equipment offline maintenance impact on the connected education resource distribution network G. Server nodes follow a hierarchical naming structure:
- Regional Data Centers: S-1, S-2, ..., S-H (at least 3), connected sequentially forming the core backbone.
- Municipal Distribution Nodes: Each regional center S-j may connect to several municipal education nodes named S-j-1, S-j-2, ...
- School Terminal Servers: Each municipal node S-j-k may connect to several school terminals named S-j-k-1, S-j-k-2, ...

You will receive the following system information:
1. Complete list of all server nodes (total {total_nodes} nodes)
2. A core observation set T containing {target_size} critical servers: {target_nodes}
3. A maintenance drill budget of {query_budget} queries
4. A target isolated LAN island count of {target_count}

Your task has three phases:

**Phase 1: Offline Drills (consumes budget)**
You can select any server NOT in observation set T for an "offline drill", asking: if this server is powered off and all its communication links are severed, how many isolated LAN islands (connected components) would the education network split into?
Each drill consumes 1 budget unit, with a total of {query_budget} drills available.

**Phase 2: Predict Observation Set (does not consume budget)**
Based on your drill results, infer and predict the offline impact for each server in observation set T (i.e., how many isolated LAN islands would result from taking that server offline).

**Phase 3: Final Selection (does not consume budget)**
From all undrilled servers, select one server such that taking it offline results in exactly {target_count} isolated LAN islands.

## Interaction Format (must strictly follow)

Each interaction must contain only one operation tag:

- Offline Drill (e.g., drilling server S-2-1):
<query_removal>S-2-1</query_removal>

- Submit Observation Set Prediction (must include predictions for all servers in the set, format "server=count", comma-separated):
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- Final Selection (select one undrilled server):
<answer>S-2-3</answer>

## Important Notes
- Offline drills cannot query servers in observation set T
- Prediction phase must provide predictions for all servers in set T
- Final selection must be an undrilled server
- No more offline drills after budget is exhausted
- Try to use as few drills as possible
"""

    contextualized_rule_zh_4 = """\
欢迎接入"工业自动化生产线供电拓扑分析系统"。

目前我们正在对大型工厂的连通供电/通信拓扑 G 进行断电检修影响评估。设备节点命名采用分层结构：
- 主控配电柜：S-1, S-2, ..., S-H（至少3个），主控配电柜之间依次相连构成核心电力总线。
- 车间级配电箱：每个主控配电柜 S-j 可能挂接若干车间配电箱，命名为 S-j-1, S-j-2, ...
- 终端单体机床：每个车间配电箱 S-j-k 可能接入若干终端机床，命名为 S-j-k-1, S-j-k-2, ...

你会得到以下系统信息：
1. 全厂设备节点列表（共 {total_nodes} 个节点）
2. 关键设备评估清单 T，包含 {target_size} 个核心设备：{target_nodes}
3. 断电推演预算 {query_budget} 次
4. 目标独立生产单元数 {target_count}

你的任务分为三个阶段：

**阶段一：断电推演（消耗预算）**
你可以选择任意不在评估清单 T 中的设备进行"断电推演"，询问：如果对该设备拉闸断电并切断所有电气连接，整个厂区拓扑会分裂成多少个互相绝缘的独立运转生产单元（连通分量）？
每次推演消耗1次预算，共有 {query_budget} 次机会。

**阶段二：预测评估清单（不消耗预算）**
基于推演结果，推断并预测评估清单 T 中每个设备的停机影响（即断电该设备后拓扑会分裂成多少个独立生产单元）。

**阶段三：最终选择（不消耗预算）**
从所有未被推演过的设备中，选择一个设备，使得对其断电后的独立生产单元数恰好等于目标数量 {target_count}。

## 交互格式（必须严格遵守）

每次只能包含一个操作标签：

- 断电推演（例如推演设备 S-2-1）：
<query_removal>S-2-1</query_removal>

- 提交评估清单预测（必须包含清单中所有设备的预测，格式为"设备名=单元数"，用逗号分隔）：
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- 最终选择（选择一个未推演过的设备）：
<answer>S-2-3</answer>

## 注意事项
- 断电推演不能查询评估清单 T 中的设备
- 预测阶段必须对清单 T 中的所有设备给出预测
- 最终选择的设备必须是未被推演过的
- 推演预算用完后不能再进行断电推演
- 请尽可能少地消耗推演次数
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Industrial Automation Production Line Power Topology Analysis System".

We are currently evaluating the power outage and maintenance impact on the large factory's connected power/communication topology G. Equipment nodes follow a hierarchical naming structure:
- Main Control Distribution Cabinets: S-1, S-2, ..., S-H (at least 3), connected sequentially forming the core power bus.
- Workshop Distribution Boxes: Each main cabinet S-j may connect to several workshop boxes named S-j-1, S-j-2, ...
- Terminal Machine Tools: Each workshop box S-j-k may supply several terminal machines named S-j-k-1, S-j-k-2, ...

You will receive the following system information:
1. Complete list of all equipment nodes (total {total_nodes} nodes)
2. A critical equipment evaluation list T containing {target_size} core devices: {target_nodes}
3. A power outage simulation budget of {query_budget} queries
4. A target isolated production unit count of {target_count}

Your task has three phases:

**Phase 1: Outage Simulations (consumes budget)**
You can select any equipment NOT in evaluation list T for a "power outage simulation", asking: if this equipment is powered off and all its electrical connections are severed, how many mutually insulated, isolated production units (connected components) would the factory topology split into?
Each simulation consumes 1 budget unit, with a total of {query_budget} simulations available.

**Phase 2: Predict Evaluation List (does not consume budget)**
Based on your simulation results, infer and predict the shutdown impact for each device in evaluation list T (i.e., how many isolated production units would result from powering off that device).

**Phase 3: Final Selection (does not consume budget)**
From all unsimulated equipment, select one device such that powering it off results in exactly {target_count} isolated production units.

## Interaction Format (must strictly follow)

Each interaction must contain only one operation tag:

- Outage Simulation (e.g., simulating equipment S-2-1):
<query_removal>S-2-1</query_removal>

- Submit Evaluation List Prediction (must include predictions for all devices in the list, format "equipment=count", comma-separated):
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- Final Selection (select one unsimulated device):
<answer>S-2-3</answer>

## Important Notes
- Outage simulations cannot query equipment in evaluation list T
- Prediction phase must provide predictions for all devices in list T
- Final selection must be an unsimulated device
- No more outage simulations after budget is exhausted
- Try to use as few simulations as possible
"""

    contextualized_rule_zh_5 = """\
欢迎接入"跨国洗钱犯罪资金链溯源分析系统"。

目前我们正在对已截获的连通洗钱资金网络 G 开展查封影响推演。账户节点命名采用分层结构：
- 主干核心钱庄账户：S-1, S-2, ..., S-H（至少3个），核心账户之间依次转账构筑主干资金通道。
- 二级中转账户：每个核心账户 S-j 可能关联若干二级中转账户，命名为 S-j-1, S-j-2, ...
- 底层分散账户：每个中转账户 S-j-k 可能控制若干底层壳公司或个人账户，命名为 S-j-k-1, S-j-k-2, ...

你会得到以下系统信息：
1. 全网嫌疑账户列表（共 {total_nodes} 个账户）
2. 重点嫌疑集合 T，包含 {target_size} 个高优账户：{target_nodes}
3. 冻结模拟预算 {query_budget} 次
4. 目标孤立资金池数量 {target_count}

你的任务分为三个阶段：

**阶段一：查封模拟（消耗预算）**
你可以选择任意不在重点集合 T 中的账户进行"查封模拟"，询问：如果冻结该账户并切断其所有资金流水链路，整个资金网络会断裂成多少个无法互相流转的孤立资金池（连通分量）？
每次模拟消耗1次预算，共有 {query_budget} 次机会。

**阶段二：预测重点集合（不消耗预算）**
基于模拟结果，推断并预测重点集合 T 中每个账户的冻结影响（即查封该账户后资金网会断裂成多少个孤立资金池）。

**阶段三：最终选择（不消耗预算）**
从所有未被模拟过的账户中，选择一个账户实施精准打击，使得查封该账户后的孤立资金池数量恰好等于目标数量 {target_count}。

## 交互格式（必须严格遵守）

每次只能包含一个操作标签：

- 查封模拟（例如模拟冻结账户 S-2-1）：
<query_removal>S-2-1</query_removal>

- 提交重点集合预测（必须包含集合中所有账户的预测，格式为"账户名=资金池数"，用逗号分隔）：
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- 最终选择（选择一个未模拟过的账户）：
<answer>S-2-3</answer>

## 注意事项
- 查封模拟不能查询重点集合 T 中的账户
- 预测阶段必须对集合 T 中的所有账户给出预测
- 最终打击的账户必须是未被模拟过的
- 模拟预算用完后不能再进行查封模拟
- 请尽可能少地消耗推演次数
"""

    contextualized_rule_en_5 = """\
[Legal/Law Enforcement Scenario]
Welcome to the "Transnational Money Laundering Funds Trace Analysis System".

We are currently conducting seizure impact deductions on the intercepted connected money laundering network G. Account nodes follow a hierarchical naming structure:
- Core Backbone Underground Bank Accounts: S-1, S-2, ..., S-H (at least 3), transferring sequentially to build the main fund channel.
- Secondary Transfer Accounts: Each core account S-j may associate with several secondary accounts named S-j-1, S-j-2, ...
- Bottom Dispersed Accounts: Each secondary account S-j-k may control several bottom shell companies or personal accounts named S-j-k-1, S-j-k-2, ...

You will receive the following system information:
1. Complete list of all suspect accounts (total {total_nodes} accounts)
2. A priority suspect set T containing {target_size} high-priority accounts: {target_nodes}
3. A freeze simulation budget of {query_budget} queries
4. A target isolated fund pool count of {target_count}

Your task has three phases:

**Phase 1: Seizure Simulations (consumes budget)**
You can select any account NOT in priority set T for a "seizure simulation", asking: if this account is frozen and all its transaction links are severed, how many isolated fund pools (connected components) incapable of mutual transfer would the financial network break into?
Each simulation consumes 1 budget unit, with a total of {query_budget} simulations available.

**Phase 2: Predict Priority Set (does not consume budget)**
Based on your simulation results, infer and predict the freeze impact for each account in priority set T (i.e., how many isolated fund pools would result from seizing that account).

**Phase 3: Final Selection (does not consume budget)**
From all unsimulated accounts, select one account for a precision strike such that freezing it results in exactly {target_count} isolated fund pools.

## Interaction Format (must strictly follow)

Each interaction must contain only one operation tag:

- Seizure Simulation (e.g., simulating freeze on account S-2-1):
<query_removal>S-2-1</query_removal>

- Submit Priority Set Prediction (must include predictions for all accounts in the set, format "account=count", comma-separated):
<predict>S-1=3, S-2-1=2, S-3=4</predict>

- Final Selection (select one unsimulated account):
<answer>S-2-3</answer>

## Important Notes
- Seizure simulations cannot query accounts in priority set T
- Prediction phase must provide predictions for all accounts in set T
- The finally selected account must be an unsimulated one
- No more seizure simulations after budget is exhausted
- Try to use as few simulations as possible
"""

    tags = ["query_removal", "predict", "answer"]
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    # 难度配置说明：
    # 1 (简单)        - H=3, 较少支节点和叶节点，目标集合6个，预算5次
    # 2 (中等偏下)    - H=4, 中等支节点和叶节点，目标集合8个，预算6次
    # 3 (中等偏上)    - H=5, 较多支节点和叶节点，目标集合9个，预算7次
    # 4 (较难)        - H=6, 复杂支节点和叶节点，目标集合10个，预算8次
    # 5 (难)          - H=7, 非常复杂的结构，目标集合12个，预算9次

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "H": 3,  # 主干节点数
                "branches": {  # 每个主干节点的支节点数
                    1: 2,
                    2: 2,
                    3: 1,
                },
                "leaves": {  # 每个支节点的叶节点数 (主干索引, 支索引): 叶数
                    (1, 1): 1,
                    (1, 2): 2,
                    (2, 1): 1,
                    (2, 2): 1,
                    (3, 1): 2,
                },
                "target_nodes": ["S-1", "S-2", "S-1-1", "S-2-2", "S-1-1-1", "S-3-1-2"],
                "query_budget": 5,
                "target_count": 3,  # 选择S-1-2或S-3-1（支节点）: 1+2=3
            },
            2: {
                "H": 4,
                "branches": {
                    1: 2,
                    2: 3,
                    3: 2,
                    4: 1,
                },
                "leaves": {
                    (1, 1): 2,
                    (1, 2): 1,
                    (2, 1): 2,
                    (2, 2): 1,
                    (2, 3): 2,
                    (3, 1): 1,
                    (3, 2): 2,
                    (4, 1): 1,
                },
                "target_nodes": ["S-1", "S-3", "S-2-1", "S-3-2", "S-1-1-2", "S-2-2-1", "S-4-1", "S-3-1-1"],
                "query_budget": 6,
                "target_count": 5,  # 选择S-3（中间主干节点）: 2（支节点数）+ 2（分成两段）+ 1（自身）= 4，实际为2+2=4，目标设为5（S-2: 3+2=5）
            },
            3: {
                "H": 5,
                "branches": {
                    1: 3,
                    2: 2,
                    3: 3,
                    4: 2,
                    5: 2,
                },
                "leaves": {
                    (1, 1): 2,
                    (1, 2): 1,
                    (1, 3): 2,
                    (2, 1): 2,
                    (2, 2): 2,
                    (3, 1): 1,
                    (3, 2): 2,
                    (3, 3): 1,
                    (4, 1): 2,
                    (4, 2): 1,
                    (5, 1): 2,
                    (5, 2): 1,
                },
                "target_nodes": ["S-2", "S-4", "S-1-2", "S-3-1", "S-5-1", "S-2-1-1", "S-3-2-2", "S-4-2-1", "S-1-3-2"],
                "query_budget": 7,
                "target_count": 5,  # 选择S-3（中间主干节点）: 3（支节点数）+ 2（分成两段）= 5
            },
            4: {
                "H": 6,
                "branches": {
                    1: 3,
                    2: 3,
                    3: 2,
                    4: 3,
                    5: 2,
                    6: 2,
                },
                "leaves": {
                    (1, 1): 2,
                    (1, 2): 2,
                    (1, 3): 1,
                    (2, 1): 2,
                    (2, 2): 2,
                    (2, 3): 1,
                    (3, 1): 2,
                    (3, 2): 2,
                    (4, 1): 1,
                    (4, 2): 2,
                    (4, 3): 2,
                    (5, 1): 2,
                    (5, 2): 1,
                    (6, 1): 2,
                    (6, 2): 1,
                },
                "target_nodes": ["S-1", "S-3", "S-5", "S-2-1", "S-4-2", "S-1-1-2", "S-3-2-1", "S-5-1-2", "S-6-1", "S-2-3-1"],
                "query_budget": 8,
                "target_count": 5,  # 选择S-2或S-4（中间主干节点）: 3+2=5
            },
            5: {
                "H": 7,
                "branches": {
                    1: 3,
                    2: 3,
                    3: 4,
                    4: 3,
                    5: 3,
                    6: 2,
                    7: 2,
                },
                "leaves": {
                    (1, 1): 2,
                    (1, 2): 2,
                    (1, 3): 2,
                    (2, 1): 2,
                    (2, 2): 1,
                    (2, 3): 2,
                    (3, 1): 2,
                    (3, 2): 2,
                    (3, 3): 1,
                    (3, 4): 2,
                    (4, 1): 2,
                    (4, 2): 2,
                    (4, 3): 1,
                    (5, 1): 2,
                    (5, 2): 2,
                    (5, 3): 1,
                    (6, 1): 2,
                    (6, 2): 2,
                    (7, 1): 2,
                    (7, 2): 1,
                },
                "target_nodes": ["S-2", "S-4", "S-6", "S-1-2", "S-3-3", "S-5-1", "S-7-1", "S-2-1-2", "S-4-2-1", "S-3-4-2", "S-6-1-1", "S-5-3-1"],
                "query_budget": 9,
                "target_count": 6,  # 选择S-4（中间主干节点）: 3（支节点数）+ 2（分成两段）+ 1 = 5，实际为3+2=5，目标设为6（S-3: 4+2=6）
            },
        },
        "en": {
            1: {
                "H": 3,
                "branches": {
                    1: 2,
                    2: 2,
                    3: 1,
                },
                "leaves": {
                    (1, 1): 1,
                    (1, 2): 2,
                    (2, 1): 1,
                    (2, 2): 1,
                    (3, 1): 2,
                },
                "target_nodes": ["S-1", "S-2", "S-1-1", "S-2-2", "S-1-1-1", "S-3-1-2"],
                "query_budget": 5,
                "target_count": 3,
            },
            2: {
                "H": 4,
                "branches": {
                    1: 2,
                    2: 3,
                    3: 2,
                    4: 1,
                },
                "leaves": {
                    (1, 1): 2,
                    (1, 2): 1,
                    (2, 1): 2,
                    (2, 2): 1,
                    (2, 3): 2,
                    (3, 1): 1,
                    (3, 2): 2,
                    (4, 1): 1,
                },
                "target_nodes": ["S-1", "S-3", "S-2-1", "S-3-2", "S-1-1-2", "S-2-2-1", "S-4-1", "S-3-1-1"],
                "query_budget": 6,
                "target_count": 5,
            },
            3: {
                "H": 5,
                "branches": {
                    1: 3,
                    2: 2,
                    3: 3,
                    4: 2,
                    5: 2,
                },
                "leaves": {
                    (1, 1): 2,
                    (1, 2): 1,
                    (1, 3): 2,
                    (2, 1): 2,
                    (2, 2): 2,
                    (3, 1): 1,
                    (3, 2): 2,
                    (3, 3): 1,
                    (4, 1): 2,
                    (4, 2): 1,
                    (5, 1): 2,
                    (5, 2): 1,
                },
                "target_nodes": ["S-2", "S-4", "S-1-2", "S-3-1", "S-5-1", "S-2-1-1", "S-3-2-2", "S-4-2-1", "S-1-3-2"],
                "query_budget": 7,
                "target_count": 5,
            },
            4: {
                "H": 6,
                "branches": {
                    1: 3,
                    2: 3,
                    3: 2,
                    4: 3,
                    5: 2,
                    6: 2,
                },
                "leaves": {
                    (1, 1): 2,
                    (1, 2): 2,
                    (1, 3): 1,
                    (2, 1): 2,
                    (2, 2): 2,
                    (2, 3): 1,
                    (3, 1): 2,
                    (3, 2): 2,
                    (4, 1): 1,
                    (4, 2): 2,
                    (4, 3): 2,
                    (5, 1): 2,
                    (5, 2): 1,
                    (6, 1): 2,
                    (6, 2): 1,
                },
                "target_nodes": ["S-1", "S-3", "S-5", "S-2-1", "S-4-2", "S-1-1-2", "S-3-2-1", "S-5-1-2", "S-6-1", "S-2-3-1"],
                "query_budget": 8,
                "target_count": 5,
            },
            5: {
                "H": 7,
                "branches": {
                    1: 3,
                    2: 3,
                    3: 4,
                    4: 3,
                    5: 3,
                    6: 2,
                    7: 2,
                },
                "leaves": {
                    (1, 1): 2,
                    (1, 2): 2,
                    (1, 3): 2,
                    (2, 1): 2,
                    (2, 2): 1,
                    (2, 3): 2,
                    (3, 1): 2,
                    (3, 2): 2,
                    (3, 3): 1,
                    (3, 4): 2,
                    (4, 1): 2,
                    (4, 2): 2,
                    (4, 3): 1,
                    (5, 1): 2,
                    (5, 2): 2,
                    (5, 3): 1,
                    (6, 1): 2,
                    (6, 2): 2,
                    (7, 1): 2,
                    (7, 2): 1,
                },
                "target_nodes": ["S-2", "S-4", "S-6", "S-1-2", "S-3-3", "S-5-1", "S-7-1", "S-2-1-2", "S-4-2-1", "S-3-4-2", "S-6-1-1", "S-5-3-1"],
                "query_budget": 9,
                "target_count": 6,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 构建图结构
        self.H = cfg["H"]
        self.branches = cfg["branches"]  # {主干索引: 支节点数}
        self.leaves = cfg["leaves"]  # {(主干索引, 支索引): 叶节点数}
        
        # 生成所有节点名称
        self.all_nodes = set()
        
        # 主干节点
        for i in range(1, self.H + 1):
            self.all_nodes.add(f"S-{i}")
        
        # 支节点和叶节点
        for backbone_idx, num_branches in self.branches.items():
            for branch_idx in range(1, num_branches + 1):
                branch_name = f"S-{backbone_idx}-{branch_idx}"
                self.all_nodes.add(branch_name)
                
                # 叶节点
                key = (backbone_idx, branch_idx)
                if key in self.leaves:
                    num_leaves = self.leaves[key]
                    for leaf_idx in range(1, num_leaves + 1):
                        leaf_name = f"S-{backbone_idx}-{branch_idx}-{leaf_idx}"
                        self.all_nodes.add(leaf_name)
        
        # 目标集合
        self.target_set = set(cfg["target_nodes"])
        self.query_budget = cfg["query_budget"]
        self.target_count = cfg["target_count"]
        
        # 游戏状态
        self.queries_used = 0
        self.queried_nodes = set()
        self.prediction_submitted = False
        
        # 填充游戏信息用于规则模板
        self._game_info["total_nodes"] = len(self.all_nodes)
        self._game_info["target_size"] = len(self.target_set)
        self._game_info["target_nodes"] = ", ".join(sorted(self.target_set))
        self._game_info["query_budget"] = self.query_budget
        self._game_info["target_count"] = self.target_count

    def _calculate_components(self, node: str) -> int:
        """
        计算删除指定节点后的连通分量数
        
        规则：
        - 删除叶节点：R=1（图仍连通）
        - 删除支节点 S-j-k：R=1+M_{j,k}（该支下各叶各成一分量，主干及其余部分为一分量）
        - 删除主干节点 S-j：
          - 若 1<j<H（主干内点）：R=A_j+2（主干被切成两段，各一分量；挂在 S-j 的每个支节点各成一分量）
          - 若 j∈{1,H}（主干端点）：R=A_j+1（主干剩一段；挂在 S-j 的每个支节点各成一分量）
        """
        parts = node.split("-")
        
        # 叶节点：S-j-k-m
        if len(parts) == 4:
            return 1
        
        # 支节点：S-j-k
        elif len(parts) == 3:
            backbone_idx = int(parts[1])
            branch_idx = int(parts[2])
            key = (backbone_idx, branch_idx)
            num_leaves = self.leaves.get(key, 0)
            return 1 + num_leaves
        
        # 主干节点：S-j
        elif len(parts) == 2:
            backbone_idx = int(parts[1])
            num_branches = self.branches.get(backbone_idx, 0)
            
            # 判断是否为端点
            if backbone_idx == 1 or backbone_idx == self.H:
                return num_branches + 1
            else:
                return num_branches + 2
        
        else:
            raise ValueError(f"Invalid node format: {node}")

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        answer_node = parsed_info["answer"].strip()
        
        # 检查节点是否有效
        if answer_node not in self.all_nodes:
            return False
        
        # 检查节点是否被查询过
        if answer_node in self.queried_nodes:
            return False
        
        # 计算删除该节点后的连通分量数
        actual_count = self._calculate_components(answer_node)
        
        # 判断是否等于目标计数
        return actual_count == self.target_count

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        possible_queries = []
        
        for node in sorted(self.all_nodes):
            if node in self.target_set:
                continue
            
            result = self._calculate_components(node)
            
            possible_queries.append({
                "query": f"<query_removal>{node}</query_removal>",
                "answer": str(result)
            })
            
        return possible_queries

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_budget = "错误：查询预算已用完。"
            error_target = "错误：不能查询目标集合中的节点。"
            error_invalid = "错误：节点名称无效。"
            error_already_predicted = "错误：已提交过预测，无法再进行查询。"
            error_no_budget = "错误：尚未提交预测或查询预算未用完。"
            success_predict = "预测已提交。正确数量：{correct}/{total}。"
            error_predict_format = "错误：预测格式无效或未包含所有目标节点。"
        else:
            error_budget = "Error: Query budget exhausted."
            error_target = "Error: Cannot query nodes in target set."
            error_invalid = "Error: Invalid node name."
            error_already_predicted = "Error: Prediction already submitted, cannot query anymore."
            error_no_budget = "Error: Must submit prediction first or query budget not exhausted."
            success_predict = "Prediction submitted. Correct count: {correct}/{total}."
            error_predict_format = "Error: Invalid prediction format or missing target nodes."

        # 处理试删查询
        if "query_removal" in parsed_info:
            if self.prediction_submitted:
                raise ValueError(error_already_predicted)
            
            if self.queries_used >= self.query_budget:
                raise ValueError(error_budget)
            
            node = parsed_info["query_removal"].strip()
            
            if node in self.target_set:
                raise ValueError(error_target)
            
            if node not in self.all_nodes:
                raise ValueError(error_invalid)
            
            # 执行查询
            self.queries_used += 1
            self.queried_nodes.add(node)
            
            components = self._calculate_components(node)
            return str(components)
        
        # 处理预测提交
        elif "predict" in parsed_info:
            pred_str = parsed_info["predict"]
            predictions = {}
            
            # 解析预测：格式为 "S-1=3, S-2=4, ..."
            for item in pred_str.split(","):
                item = item.strip()
                if not item:
                    continue
                if "=" not in item:
                    raise ValueError(error_predict_format)
                parts = item.split("=", 1)
                node = parts[0].strip()
                try:
                    count = int(parts[1].strip())
                except ValueError:
                    raise ValueError(error_predict_format)
                predictions[node] = count
            
            # 检查是否包含所有目标节点
            if set(predictions.keys()) != self.target_set:
                raise ValueError(error_predict_format)
            
            # 计算正确数量
            correct = 0
            for node in self.target_set:
                actual = self._calculate_components(node)
                if predictions[node] == actual:
                    correct += 1
            
            self.prediction_submitted = True
            return success_predict.format(correct=correct, total=len(self.target_set))
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        # 若 correct 是纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 否则按规则替换关键词
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            # 忽略大小写，保持原始大小写风格
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                # 简单实现，替换常见形式
                return correct.replace("Yes", "No").replace("yes", "no").replace("YES", "NO")
            elif "no" in lower_correct:
                return correct.replace("No", "Yes").replace("no", "yes").replace("NO", "YES")
        
        # 若都不匹配
        return correct + "_WRONG"

    def step(self, response: str):
        """重写step方法以处理三阶段逻辑"""
        try:
            parsed_info = self.parse(response)
            
            # 最终答案提交
            if "answer" in parsed_info:
                # 必须先提交预测
                if not self.prediction_submitted:
                    if self.config.language == "zh":
                        raise ValueError("错误：必须先提交预测才能提交最终答案。")
                    else:
                        raise ValueError("Error: Must submit prediction before final answer.")
                
                is_success = self.evaluate(parsed_info)
                if is_success:
                    res = "答案正确" if self.config.language == "zh" else "Correct answer."
                    self.state.set_state("success", "success")
                    self.state.add_message("user", res)
                else:
                    res = "答案错误" if self.config.language == "zh" else "Incorrect answer."
                    self.state.set_state("failed", "incorrect answer")
                    self.state.add_message("user", res)
            
            # 查询或预测
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state