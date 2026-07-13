from .base import Game
import re
import random
from collections import deque

class PeriodicTreeStructureGame(Game):

    game_rule_zh = """\
我们现在来玩一个"周期树结构推理"游戏，规则如下：

游戏设定了一棵未知的有根树，满足以下性质：
- 树的层高为 H（未知），根节点的深度为 0。
- 树的分叉规律遵循周期性：存在一个未知的周期 p（p 可能是 2、3 或 4），以及一个未知的数组 (c0, c1, ..., c{{p-1}})，其中每个 ci 是 1 到 4 之间的整数。
- 对于深度 d 小于 H 的每个节点，它有恰好 c{{d mod p}} 个子节点。
- 所有叶子节点恰好在深度 H。
- 树的总节点数为 N = {n}，所有节点被随机打乱编号为 1 到 {n}，你无法从编号直接获知任何结构信息。

你的目标是通过交互查询推断出树的结构参数（周期 p、分叉数组 c、最大深度 H）以及每个节点的深度，或者找到一个能够准确预测任意节点闭球大小的规则。

## 交互接口

你可以进行以下两种查询（总查询次数不超过 30 次）：

1. **单次计数查询**：询问节点 v 在半径 k 内的闭球大小（即距离小于等于 k 的节点总数）。
   格式：
   <query_count>v,k</query_count>
   
   例如：
   <query_count>5,2</query_count>

2. **批量计数查询**：对同一个节点 v 询问多个不同半径的闭球大小。
   格式：
   <query_multi>v,k1,k2,...,km</query_multi>
   
   例如：
   <query_multi>3,0,1,2,3</query_multi>

注意：
- 一次 query_multi 算作一次查询。
- 距离定义为最短路径的边数。
- 闭球大小 COUNT(v,k) 是指与节点 v 距离小于等于 k 的所有节点数量（包括 v 自身）。

## 提交答案

当你收集足够信息后，请提交最终答案。答案需要包含：
1. 周期 p
2. 分叉数组 c（用逗号分隔，长度为 p）
3. 最大深度 H
4. 每个节点的深度分配（格式：节点编号=深度，用逗号分隔）

答案格式如下：
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

注意：depths 必须包含所有 {n} 个节点的深度信息。

## 验证方式

提交答案后，系统会验证你提交的周期 p、分叉数组 c、最大深度 H 以及每个节点的深度是否与实际树结构完全一致。全部正确则通过，否则失败。
"""

    game_rule_en = """\
Let's play a "Periodic Tree Structure Inference" game. Here are the rules:

The game involves an unknown rooted tree with the following properties:
- The tree has a height H (unknown), with the root at depth 0.
- The branching follows a periodic pattern: there exists an unknown period p (p can be 2, 3, or 4) and an unknown array (c0, c1, ..., c{{p-1}}), where each ci is an integer between 1 and 4.
- For each node at depth d less than H, it has exactly c{{d mod p}} children.
- All leaf nodes are exactly at depth H.
- The tree has a total of N = {n} nodes, randomly shuffled and labeled from 1 to {n}, with no structural information revealed by the labels.

Your goal is to infer the tree's structural parameters (period p, branching array c, maximum depth H) and the depth of each node through interactive queries, or to find a rule that can accurately predict the closed ball size for any node.

## Interaction Interface

You can make the following two types of queries (total queries limited to 30):

1. **Single Count Query**: Ask for the closed ball size of node v within radius k (i.e., the total number of nodes at distance at most k).
   Format:
   <query_count>v,k</query_count>
   
   Example:
   <query_count>5,2</query_count>

2. **Multi Count Query**: Ask for multiple radii for the same node v.
   Format:
   <query_multi>v,k1,k2,...,km</query_multi>
   
   Example:
   <query_multi>3,0,1,2,3</query_multi>

Notes:
- One query_multi counts as one query.
- Distance is defined as the number of edges in the shortest path.
- Closed ball size COUNT(v,k) is the number of all nodes at distance at most k from node v (including v itself).

## Submit Answer

When you have gathered enough information, submit your final answer containing:
1. Period p
2. Branching array c (comma-separated, length p)
3. Maximum depth H
4. Depth assignment for each node (format: node_id=depth, comma-separated)

Answer format:
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

Note: depths must include depth information for all {n} nodes.

## Verification

After submission, the system will verify whether your submitted period p, branching array c, maximum depth H, and the depth of each node are completely consistent with the actual tree structure. All correct means success, otherwise failure.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市交通路网层级推演系统”。

系统正在分析一个未知的树状路网枢纽结构，满足以下性质：
- 路网最大层级为 H（未知），中央主枢纽深度为 0。
- 道路分流遵循周期性规律：存在一个未知的周期 p（p 可能是 2、3 或 4），以及一个未知的路口分流数组 (c0, c1, ..., c{{p-1}})，其中每个 ci 是 1 到 4 之间的整数。
- 对于深度 d 小于 H 的每个路口，它恰好连接 c{{d mod p}} 个下一级路口或站点。
- 所有末端站点恰好位于层级 H。
- 路网总节点数为 N = {n}，所有站点和路口被随机打乱编号为 1 到 {n}，你无法从编号直接获知任何拓扑结构信息。

你的目标是通过交互查询推断出路网的结构参数（周期 p、分流数组 c、最大层级 H）以及每个节点的层级深度，或者找到一个能够准确预测任意节点在特定通勤距离内可达节点总数的规则。

## 交互接口

你可以进行以下两种查询（总查询次数不超过 30 次）：

1. **单次范围查询**：询问节点 v 在通勤距离 k 内的可达节点总数（即经过的道路段数小于等于 k 的节点总数）。
   格式：
   <query_count>v,k</query_count>
   
   例如：
   <query_count>5,2</query_count>

2. **批量范围查询**：对同一个节点 v 询问多个不同通勤距离的可达节点总数。
   格式：
   <query_multi>v,k1,k2,...,km</query_multi>
   
   例如：
   <query_multi>3,0,1,2,3</query_multi>

注意：
- 一次 query_multi 算作一次查询。
- 通勤距离定义为最短路径的道路段数（边数）。
- 可达节点总数 COUNT(v,k) 是指与节点 v 距离小于等于 k 的所有节点数量（包括 v 自身）。

## 提交答案

当你收集足够信息后，请提交最终路网模型。答案需要包含：
1. 周期 p
2. 分流数组 c（用逗号分隔，长度为 p）
3. 最大层级 H
4. 每个节点的层级深度分配（格式：节点编号=深度，用逗号分隔）

答案格式如下：
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

注意：depths 必须包含所有 {n} 个节点的层级深度信息。

## 验证方式

提交答案后，系统会验证你提交的周期 p、分流数组 c、最大层级 H 以及每个节点的层级深度是否与实际路网结构完全一致。全部正确则通过，否则失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Network Hierarchy Inference System".

The system is analyzing an unknown tree-like traffic hub structure with the following properties:
- The network has a maximum level H (unknown), with the central main hub at depth 0.
- The road bifurcation follows a periodic pattern: there exists an unknown period p (p can be 2, 3, or 4) and an unknown bifurcation array (c0, c1, ..., c{{p-1}}), where each ci is an integer between 1 and 4.
- For each intersection at depth d less than H, it connects to exactly c{{d mod p}} next-level intersections or stations.
- All terminal stations are exactly at level H.
- The network has a total of N = {n} nodes, randomly shuffled and labeled from 1 to {n}, with no topological information revealed by the labels.

Your goal is to infer the network's structural parameters (period p, bifurcation array c, maximum level H) and the depth level of each node through interactive queries, or to find a rule that can accurately predict the total number of reachable nodes within a specific commuting distance for any node.

## Interaction Interface

You can make the following two types of queries (total queries limited to 30):

1. **Single Range Query**: Ask for the total number of reachable nodes from node v within commuting distance k (i.e., the total number of nodes at a road segment distance of at most k).
   Format:
   <query_count>v,k</query_count>
   
   Example:
   <query_count>5,2</query_count>

2. **Multi Range Query**: Ask for multiple commuting distances for the same node v.
   Format:
   <query_multi>v,k1,k2,...,km</query_multi>
   
   Example:
   <query_multi>3,0,1,2,3</query_multi>

Notes:
- One query_multi counts as one query.
- Commuting distance is defined as the number of road segments (edges) in the shortest path.
- The reachable node count COUNT(v,k) is the number of all nodes at distance at most k from node v (including v itself).

## Submit Answer

When you have gathered enough information, submit your final network model containing:
1. Period p
2. Bifurcation array c (comma-separated, length p)
3. Maximum level H
4. Depth level assignment for each node (format: node_id=depth, comma-separated)

Answer format:
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

Note: depths must include depth information for all {n} nodes.

## Verification

After submission, the system will verify whether your submitted period p, bifurcation array c, maximum level H, and the depth level of each node are completely consistent with the actual network structure. All correct means success, otherwise failure.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“分级诊疗网络拓扑推演系统”。

系统记录了一个未知的树状分级诊疗网络，满足以下性质：
- 诊疗网络的最大层级为 H（未知），国家级中心医院深度为 0。
- 医院的下属分支建立遵循周期性管理规律：存在一个未知的周期 p（p 可能是 2、3 或 4），以及一个未知的机构编制数组 (c0, c1, ..., c{{p-1}})，其中每个 ci 是 1 到 4 之间的整数。
- 对于深度 d 小于 H 的每个医疗机构，它恰好管辖 c{{d mod p}} 个下级医疗机构。
- 所有基层社区诊所恰好位于层级 H。
- 诊疗网络总机构数为 N = {n}，所有机构被随机打乱编号为 1 到 {n}，你无法从编号直接获知任何层级结构信息。

你的目标是通过交互查询推断出该医疗网络的结构参数（周期 p、机构编制数组 c、最大层级 H）以及每个机构的层级深度，或者找到一个能够准确预测任意机构在特定转诊步数内覆盖的机构总数的规则。

## 交互接口

你可以进行以下两种查询（总查询次数不超过 30 次）：

1. **单次辐射查询**：询问机构 v 在转诊步数 k 内的覆盖机构总数（即最短转诊路径小于等于 k 的机构总数）。
   格式：
   <query_count>v,k</query_count>
   
   例如：
   <query_count>5,2</query_count>

2. **批量辐射查询**：对同一个机构 v 询问多个不同转诊步数的覆盖机构总数。
   格式：
   <query_multi>v,k1,k2,...,km</query_multi>
   
   例如：
   <query_multi>3,0,1,2,3</query_multi>

注意：
- 一次 query_multi 算作一次查询。
- 转诊步数定义为机构间最短路径的边数。
- 覆盖机构总数 COUNT(v,k) 是指与机构 v 距离小于等于 k 的所有机构数量（包括 v 自身）。

## 提交答案

当你收集足够信息后，请提交最终网络模型。答案需要包含：
1. 周期 p
2. 机构编制数组 c（用逗号分隔，长度为 p）
3. 最大层级 H
4. 每个机构的层级深度分配（格式：机构编号=深度，用逗号分隔）

答案格式如下：
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

注意：depths 必须包含所有 {n} 个机构的层级深度信息。

## 验证方式

提交答案后，系统会验证你提交的周期 p、机构编制数组 c、最大层级 H 以及每个机构的层级深度是否与实际医疗网络完全一致。全部正确则通过，否则失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Hierarchical Medical Referral Network Topology Inference System".

The system has recorded an unknown tree-like hierarchical medical network with the following properties:
- The network has a maximum level H (unknown), with the national central hospital at depth 0.
- The establishment of subordinate branches follows a periodic management rule: there exists an unknown period p (p can be 2, 3, or 4) and an unknown institutional capacity array (c0, c1, ..., c{{p-1}}), where each ci is an integer between 1 and 4.
- For each medical facility at depth d less than H, it administers exactly c{{d mod p}} subordinate medical facilities.
- All primary community clinics are exactly at level H.
- The network has a total of N = {n} facilities, randomly shuffled and labeled from 1 to {n}, with no structural hierarchy information revealed by the labels.

Your goal is to infer the network's structural parameters (period p, capacity array c, maximum level H) and the depth level of each facility through interactive queries, or to find a rule that can accurately predict the total number of covered facilities within a specific number of referral steps for any facility.

## Interaction Interface

You can make the following two types of queries (total queries limited to 30):

1. **Single Coverage Query**: Ask for the total number of covered facilities from facility v within k referral steps (i.e., the total number of facilities with a shortest referral path of at most k).
   Format:
   <query_count>v,k</query_count>
   
   Example:
   <query_count>5,2</query_count>

2. **Multi Coverage Query**: Ask for multiple referral step radii for the same facility v.
   Format:
   <query_multi>v,k1,k2,...,km</query_multi>
   
   Example:
   <query_multi>3,0,1,2,3</query_multi>

Notes:
- One query_multi counts as one query.
- Referral steps are defined as the number of edges in the shortest path between facilities.
- The covered facility count COUNT(v,k) is the number of all facilities at distance at most k from facility v (including v itself).

## Submit Answer

When you have gathered enough information, submit your final network model containing:
1. Period p
2. Capacity array c (comma-separated, length p)
3. Maximum level H
4. Depth level assignment for each facility (format: facility_id=depth, comma-separated)

Answer format:
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

Note: depths must include depth information for all {n} facilities.

## Verification

After submission, the system will verify whether your submitted period p, capacity array c, maximum level H, and the depth level of each facility are completely consistent with the actual medical network. All correct means success, otherwise failure.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“教育行政管辖架构推演系统”。

系统内存在一个未知的树状教育管理架构，满足以下性质：
- 管理架构的最高层级为 H（未知），中央教育部深度为 0。
- 行政区划的下属单位划分遵循周期性规律：存在一个未知的周期 p（p 可能是 2、3 或 4），以及一个未知的管辖划分数组 (c0, c1, ..., c{{p-1}})，其中每个 ci 是 1 到 4 之间的整数。
- 对于深度 d 小于 H 的每个行政单位，它恰好直辖 c{{d mod p}} 个下级单位。
- 所有最基层的学校恰好位于层级 H。
- 架构总单位数为 N = {n}，所有单位被随机打乱编号为 1 到 {n}，你无法从编号直接获知任何职级结构信息。

你的目标是通过交互查询推断出架构的层级参数（周期 p、管辖划分数组 c、最大层级 H）以及每个单位的职级深度，或者找到一个能够准确预测任意单位在特定政令传达步数内能辐射到的单位总数的规则。

## 交互接口

你可以进行以下两种查询（总查询次数不超过 30 次）：

1. **单次辐射查询**：询问单位 v 在政令传达步数 k 内的辐射单位总数（即最短联络路径小于等于 k 的单位总数）。
   格式：
   <query_count>v,k</query_count>
   
   例如：
   <query_count>5,2</query_count>

2. **批量辐射查询**：对同一个单位 v 询问多个不同政令传达步数的辐射单位总数。
   格式：
   <query_multi>v,k1,k2,...,km</query_multi>
   
   例如：
   <query_multi>3,0,1,2,3</query_multi>

注意：
- 一次 query_multi 算作一次查询。
- 政令传达步数定义为上下级间最短联络路径的边数。
- 辐射单位总数 COUNT(v,k) 是指与单位 v 距离小于等于 k 的所有单位数量（包括 v 自身）。

## 提交答案

当你收集足够信息后，请提交最终架构模型。答案需要包含：
1. 周期 p
2. 管辖划分数组 c（用逗号分隔，长度为 p）
3. 最大层级 H
4. 每个单位的职级深度分配（格式：单位编号=深度，用逗号分隔）

答案格式如下：
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

注意：depths 必须包含所有 {n} 个单位的职级深度信息。

## 验证方式

提交答案后，系统会验证你提交的周期 p、管辖划分数组 c、最大层级 H 以及每个单位的职级深度是否与实际管理架构完全一致。全部正确则通过，否则失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Educational Administration Architecture Inference System".

The system contains an unknown tree-like educational management architecture with the following properties:
- The maximum level of the management architecture is H (unknown), with the Central Ministry of Education at depth 0.
- The division of subordinate units follows a periodic rule: there exists an unknown period p (p can be 2, 3, or 4) and an unknown jurisdiction division array (c0, c1, ..., c{{p-1}}), where each ci is an integer between 1 and 4.
- For each administrative unit at depth d less than H, it directly administers exactly c{{d mod p}} subordinate units.
- All grassroots schools are exactly at level H.
- The architecture has a total of N = {n} units, randomly shuffled and labeled from 1 to {n}, with no rank structure information revealed by the labels.

Your goal is to infer the architecture's hierarchical parameters (period p, division array c, maximum level H) and the rank depth of each unit through interactive queries, or to find a rule that can accurately predict the total number of units reached within a specific number of policy transmission steps for any unit.

## Interaction Interface

You can make the following two types of queries (total queries limited to 30):

1. **Single Reach Query**: Ask for the total number of reached units from unit v within policy transmission steps k (i.e., the total number of units with a shortest communication path of at most k).
   Format:
   <query_count>v,k</query_count>
   
   Example:
   <query_count>5,2</query_count>

2. **Multi Reach Query**: Ask for multiple policy transmission step radii for the same unit v.
   Format:
   <query_multi>v,k1,k2,...,km</query_multi>
   
   Example:
   <query_multi>3,0,1,2,3</query_multi>

Notes:
- One query_multi counts as one query.
- Policy transmission steps are defined as the number of edges in the shortest communication path between units.
- The reached unit count COUNT(v,k) is the number of all units at distance at most k from unit v (including v itself).

## Submit Answer

When you have gathered enough information, submit your final architecture model containing:
1. Period p
2. Division array c (comma-separated, length p)
3. Maximum level H
4. Rank depth assignment for each unit (format: unit_id=depth, comma-separated)

Answer format:
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

Note: depths must include depth information for all {n} units.

## Verification

After submission, the system will verify whether your submitted period p, division array c, maximum level H, and the rank depth of each unit are completely consistent with the actual management architecture. All correct means success, otherwise failure.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业产品装配BOM分析系统”。

系统正在解析一个未知的树状产品物料清单（BOM）结构，满足以下性质：
- 装配层级的最大深度为 H（未知），最终成品（顶层装配）的深度为 0。
- 组件的拆解规律遵循周期性：存在一个未知的周期 p（p 可能是 2、3 或 4），以及一个未知的子件需求数组 (c0, c1, ..., c{{p-1}})，其中每个 ci 是 1 到 4 之间的整数。
- 对于深度 d 小于 H 的每个组件，它恰好由 c{{d mod p}} 个直接子组件拼装而成。
- 所有最底层的不可拆解基础原材料恰好位于深度 H。
- BOM树的总组件数为 N = {n}，所有组件被随机打乱编号为 1 到 {n}，你无法从编号直接获知任何装配层级信息。

你的目标是通过交互查询推断出该BOM的结构参数（周期 p、需求数组 c、最大深度 H）以及每个组件的装配深度，或者找到一个能够准确预测任意组件在特定关联级数内涉及的组件总数的规则。

## 交互接口

你可以进行以下两种查询（总查询次数不超过 30 次）：

1. **单次关联查询**：询问组件 v 在关联级数 k 内的关联组件总数（即装配路径距离小于等于 k 的组件总数）。
   格式：
   <query_count>v,k</query_count>
   
   例如：
   <query_count>5,2</query_count>

2. **批量关联查询**：对同一个组件 v 询问多个不同关联级数的组件总数。
   格式：
   <query_multi>v,k1,k2,...,km</query_multi>
   
   例如：
   <query_multi>3,0,1,2,3</query_multi>

注意：
- 一次 query_multi 算作一次查询。
- 关联级数定义为BOM树结构中最短依赖路径的边数。
- 关联组件总数 COUNT(v,k) 是指与组件 v 距离小于等于 k 的所有组件数量（包括 v 自身）。

## 提交答案

当你收集足够信息后，请提交最终装配结构模型。答案需要包含：
1. 周期 p
2. 需求数组 c（用逗号分隔，长度为 p）
3. 最大深度 H
4. 每个组件的装配深度分配（格式：组件编号=深度，用逗号分隔）

答案格式如下：
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

注意：depths 必须包含所有 {n} 个组件的深度信息。

## 验证方式

提交答案后，系统会验证你提交的周期 p、需求数组 c、最大深度 H 以及每个组件的装配深度是否与实际装配结构完全一致。全部正确则通过，否则失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Product Assembly BOM Analysis System".

The system is parsing an unknown tree-like Bill of Materials (BOM) structure with the following properties:
- The maximum depth of the assembly levels is H (unknown), with the final product (top-level assembly) at depth 0.
- The breakdown of components follows a periodic pattern: there exists an unknown period p (p can be 2, 3, or 4) and an unknown subcomponent requirement array (c0, c1, ..., c{{p-1}}), where each ci is an integer between 1 and 4.
- For each component at depth d less than H, it is assembled from exactly c{{d mod p}} direct subcomponents.
- All bottom-level, indivisible raw materials are exactly at depth H.
- The BOM tree has a total of N = {n} components, randomly shuffled and labeled from 1 to {n}, with no assembly hierarchy information revealed by the labels.

Your goal is to infer the BOM's structural parameters (period p, requirement array c, maximum depth H) and the assembly depth of each component through interactive queries, or to find a rule that can accurately predict the total number of related components within a specific relation level for any component.

## Interaction Interface

You can make the following two types of queries (total queries limited to 30):

1. **Single Relation Query**: Ask for the total number of related components for component v within relation level k (i.e., the total number of components with an assembly path distance of at most k).
   Format:
   <query_count>v,k</query_count>
   
   Example:
   <query_count>5,2</query_count>

2. **Multi Relation Query**: Ask for multiple relation levels for the same component v.
   Format:
   <query_multi>v,k1,k2,...,km</query_multi>
   
   Example:
   <query_multi>3,0,1,2,3</query_multi>

Notes:
- One query_multi counts as one query.
- Relation level is defined as the number of edges in the shortest dependency path within the BOM tree structure.
- The related component count COUNT(v,k) is the number of all components at distance at most k from component v (including v itself).

## Submit Answer

When you have gathered enough information, submit your final assembly structure model containing:
1. Period p
2. Requirement array c (comma-separated, length p)
3. Maximum depth H
4. Assembly depth assignment for each component (format: component_id=depth, comma-separated)

Answer format:
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

Note: depths must include depth information for all {n} components.

## Verification

After submission, the system will verify whether your submitted period p, requirement array c, maximum depth H, and the assembly depth of each component are completely consistent with the actual assembly structure. All correct means success, otherwise failure.
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法管辖层级溯源系统”。

系统正在评估一个未知的树状法院管辖层级网络，满足以下性质：
- 司法体系的最大层级深度为 H（未知），最高法院的深度为 0。
- 下级法院的设立遵循法定的周期性编制规则：存在一个未知的周期 p（p 可能是 2、3 或 4），以及一个未知的辖区划分数组 (c0, c1, ..., c{{p-1}})，其中每个 ci 是 1 到 4 之间的整数。
- 对于深度 d 小于 H 的每个法院，它恰好管辖 c{{d mod p}} 个直接下级法院。
- 所有最基层的地方法庭恰好位于层级深度 H。
- 法院网络总节点数为 N = {n}，所有法院被随机打乱编号为 1 到 {n}，你无法从编号直接获知任何管辖权结构信息。

你的目标是通过交互查询推断出该司法网络的结构参数（周期 p、辖区划分数组 c、最大层级 H）以及每个法院的层级深度，或者找到一个能够准确预测任意法院在特定管辖跨度内关联法院总数的规则。

## 交互接口

你可以进行以下两种查询（总查询次数不超过 30 次）：

1. **单次关联查询**：询问法院 v 在管辖跨度 k 内的关联法院总数（即层级连带关系的最短距离小于等于 k 的法院总数）。
   格式：
   <query_count>v,k</query_count>
   
   例如：
   <query_count>5,2</query_count>

2. **批量关联查询**：对同一个法院 v 询问多个不同管辖跨度的关联法院总数。
   格式：
   <query_multi>v,k1,k2,...,km</query_multi>
   
   例如：
   <query_multi>3,0,1,2,3</query_multi>

注意：
- 一次 query_multi 算作一次查询。
- 管辖跨度定义为法院间上下级最短关系链的边数。
- 关联法院总数 COUNT(v,k) 是指与法院 v 距离小于等于 k 的所有法院数量（包括 v 自身）。

## 提交答案

当你收集足够信息后，请提交最终管辖层级模型。答案需要包含：
1. 周期 p
2. 辖区划分数组 c（用逗号分隔，长度为 p）
3. 最大层级 H
4. 每个法院的层级深度分配（格式：法院编号=深度，用逗号分隔）

答案格式如下：
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

注意：depths 必须包含所有 {n} 个法院的层级深度信息。

## 验证方式

提交答案后，系统会验证你提交的周期 p、辖区划分数组 c、最大层级 H 以及每个法院的层级深度是否与实际司法网络完全一致。全部正确则通过，否则失败。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Jurisdiction Hierarchy Tracing System".

The system is evaluating an unknown tree-like court jurisdiction hierarchy network with the following properties:
- The maximum level depth of the judicial system is H (unknown), with the Supreme Court at depth 0.
- The establishment of lower courts follows a statutory periodic organizational rule: there exists an unknown period p (p can be 2, 3, or 4) and an unknown jurisdiction division array (c0, c1, ..., c{{p-1}}), where each ci is an integer between 1 and 4.
- For each court at depth d less than H, it directly administers exactly c{{d mod p}} direct lower courts.
- All grassroots local tribunals are exactly at level depth H.
- The court network has a total of N = {n} nodes, randomly shuffled and labeled from 1 to {n}, with no jurisdiction structure information revealed by the labels.

Your goal is to infer the judicial network's structural parameters (period p, division array c, maximum level H) and the depth level of each court through interactive queries, or to find a rule that can accurately predict the total number of associated courts within a specific jurisdiction span for any court.

## Interaction Interface

You can make the following two types of queries (total queries limited to 30):

1. **Single Association Query**: Ask for the total number of associated courts for court v within jurisdiction span k (i.e., the total number of courts with a shortest hierarchical relationship distance of at most k).
   Format:
   <query_count>v,k</query_count>
   
   Example:
   <query_count>5,2</query_count>

2. **Multi Association Query**: Ask for multiple jurisdiction spans for the same court v.
   Format:
   <query_multi>v,k1,k2,...,km</query_multi>
   
   Example:
   <query_multi>3,0,1,2,3</query_multi>

Notes:
- One query_multi counts as one query.
- Jurisdiction span is defined as the number of edges in the shortest hierarchical relationship chain between courts.
- The associated court count COUNT(v,k) is the number of all courts at distance at most k from court v (including v itself).

## Submit Answer

When you have gathered enough information, submit your final jurisdiction hierarchy model containing:
1. Period p
2. Division array c (comma-separated, length p)
3. Maximum level H
4. Depth level assignment for each court (format: court_id=depth, comma-separated)

Answer format:
<answer>p=2, c=3,2, H=4, depths=1=0,2=1,3=1,4=1,5=2,6=2,7=2,8=2,9=2,10=2,...</answer>

Note: depths must include depth information for all {n} courts.

## Verification

After submission, the system will verify whether your submitted period p, division array c, maximum level H, and the depth level of each court are completely consistent with the actual judicial network. All correct means success, otherwise failure.
"""

    tags = ["answer", "query_count", "query_multi"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        1: {"p": 2, "c": [2, 1], "H": 4},
        2: {"p": 2, "c": [3, 2], "H": 3},
        3: {"p": 3, "c": [2, 2, 1], "H": 4},
        4: {"p": 3, "c": [2, 3, 2], "H": 3},
        5: {"p": 4, "c": [2, 2, 3, 1], "H": 3},
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.p = cfg["p"]
        self.c = cfg["c"]
        self.H = cfg["H"]
        
        self.nodes_per_depth = [0] * (self.H + 1)
        self.nodes_per_depth[0] = 1 
        for d in range(self.H):
            branching = self.c[d % self.p]
            self.nodes_per_depth[d + 1] = self.nodes_per_depth[d] * branching

        total = sum(self.nodes_per_depth)
        self.n = total
        self._game_info["n"] = self.n

        logical_adj = {i: [] for i in range(1, self.n + 1)}
        logical_depths = {1: 0}
        
        current_layer = [1]
        next_id = 2
        
        for d in range(self.H):
            branching = self.c[d % self.p]
            next_layer = []
            for parent in current_layer:
                for _ in range(branching):
                    child = next_id
                    next_id += 1
                    logical_adj[parent].append(child)
                    logical_adj[child].append(parent)
                    logical_depths[child] = d + 1
                    next_layer.append(child)
            current_layer = next_layer

        nodes = list(range(1, self.n + 1))
        rng = random.Random(self.config.difficulty * 42)
        rng.shuffle(nodes)
        
        self.logical_to_shuffled = {}
        original_ids = list(range(1, self.n + 1))
        for i, original_id in enumerate(original_ids):
            self.logical_to_shuffled[original_id] = nodes[i]
            
        self.node_depths = {}
        self.adj = {i: [] for i in range(1, self.n + 1)}
        
        for log_id in original_ids:
            shuff_id = self.logical_to_shuffled[log_id]
            self.node_depths[shuff_id] = logical_depths[log_id]
            for neighbor_log_id in logical_adj[log_id]:
                neighbor_shuff_id = self.logical_to_shuffled[neighbor_log_id]
                self.adj[shuff_id].append(neighbor_shuff_id)

        self.queried_pairs = set()

    def _compute_count(self, v, k):
        """计算节点 v 在半径 k 内的闭球大小"""
        if v < 1 or v > self.n or k < 0:
            return None
        
        if v not in self.adj:
            return None
            
        visited = {v}
        queue = deque([(v, 0)])
        count = 0
        
        while queue:
            curr, dist = queue.popleft()
            count += 1
            
            if dist < k:
                for neighbor in self.adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, dist + 1))
        
        return count

    def evaluate(self, parsed_info):
        """验证答案是否正确"""
        try:
            raw_ans = parsed_info["answer"].strip()
            
            # 用正则提取各字段
            p_match = re.search(r'p\s*=\s*(\d+)', raw_ans)
            h_match = re.search(r'H\s*=\s*(\d+)', raw_ans)
            c_match = re.search(r'c\s*=\s*([\d\s,]+?)(?:\s*,\s*H\s*=)', raw_ans)
            depths_match = re.search(r'depths\s*=\s*(.+)', raw_ans)
            
            if not all([p_match, h_match, c_match, depths_match]):
                return False
            
            p_ans = int(p_match.group(1))
            if p_ans != self.p:
                return False
            
            c_ans = [int(x.strip()) for x in c_match.group(1).strip().split(",")]
            if c_ans != self.c:
                return False
            
            H_ans = int(h_match.group(1))
            if H_ans != self.H:
                return False
            
            depths_str = depths_match.group(1).strip()
            depth_pairs = depths_str.split(",")
            depths_ans = {}
            for pair in depth_pairs:
                pair = pair.strip()
                if "=" in pair:
                    node_str, depth_str = pair.split("=", 1)
                    depths_ans[int(node_str.strip())] = int(depth_str.strip())
            
            if set(depths_ans.keys()) != set(range(1, self.n + 1)):
                return False
            
            for node in range(1, self.n + 1):
                if depths_ans[node] != self.node_depths[node]:
                    return False
            
            return True
            
        except Exception:
            return False

    def _compute_count_from_structure(self, v, k, depths_ans):
        """根据提交的结构计算闭球大小"""
        user_depth = depths_ans.get(v)
        if user_depth is None or user_depth < 0 or user_depth > self.H:
            return -1 
            
        proxy_node = None
        for node_id, depth in self.node_depths.items():
            if depth == user_depth:
                proxy_node = node_id
                break
        
        if proxy_node is None:
            return -1
            
        return self._compute_count(proxy_node, k)

    def _cf_core_produce(self, parsed_info):
        """原始业务逻辑，由基类 produce_response 调用"""
        if self.config.language == "zh":
            invalid_msg = "无效请求：格式错误或参数超出范围。"
        else:
            invalid_msg = "Invalid request: format error or parameters out of range."

        try:
            if "query_count" in parsed_info:
                raw = parsed_info["query_count"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return invalid_msg
                
                v = int(parts[0])
                k = int(parts[1])
                
                result = self._compute_count(v, k)
                if result is None:
                    return invalid_msg
                
                self.queried_pairs.add((v, k))
                return str(result)
            
            elif "query_multi" in parsed_info:
                raw = parsed_info["query_multi"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) < 2:
                    return invalid_msg
                
                v = int(parts[0])
                ks = [int(x) for x in parts[1:]]
                
                results = []
                for k in ks:
                    result = self._compute_count(v, k)
                    if result is None:
                        return invalid_msg
                    results.append(str(result))
                    self.queried_pairs.add((v, k))
                
                return ", ".join(results)
            
            else:
                return invalid_msg
                
        except Exception as e:
            return invalid_msg

    def _cf_make_wrong(self, correct):
        """生成一个错误的响应"""
        # 尝试处理逗号分隔的多个数字（query_multi 的结果）
        parts = [p.strip() for p in correct.split(",")]
        if all(p.isdigit() for p in parts) and len(parts) >= 1:
            # 修改第一个数字
            parts[0] = str(int(parts[0]) + 1)
            return ", ".join(parts)
        
        if "Yes" in correct:
            return correct.replace("Yes", "No")
        if "No" in correct:
            return correct.replace("No", "Yes")
        if "yes" in correct:
            return correct.replace("yes", "no")
        if "no" in correct:
            return correct.replace("no", "yes")
            
        if "是" in correct:
            return correct.replace("是", "否")
        if "否" in correct:
            return correct.replace("否", "是")
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        """
        possible_queries = []
        for v in range(1, self.n + 1):
            for k in range(0, self.H * 2 + 2):
                ans = self._compute_count(v, k)
                if ans is not None:
                    possible_queries.append({
                        "query": f"<query_count>{v},{k}</query_count>",
                        "answer": str(ans)
                    })
        return possible_queries