# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子树属性聚合：某子树内所有节点的属性之和/最大值是多少
# ============================================================

from .base import Game
import re


class MaxSubtreeSumGame(Game):

    game_rule_zh = """\
我们现在来玩一个"最大子树和推理"的游戏，规则如下：

游戏设定了一棵有根树，节点编号为 1 到 {n}，根节点为 {root}。每个节点都有一个整数权值（可能为负数）。对于任意节点 u，定义其子树和为：该节点的权值加上其所有直接子节点的子树和之和。

树的结构如下：
{tree_structure}

根节点的子树和为：{root_sum}

题目保证：在所有节点中，存在且仅存在一个节点的子树和严格大于其他所有节点（即唯一最大）。

你的目标是找到这个子树和最大的节点及其子树和的值。你可以使用以下两种查询方式，但查询次数有限：

1. 分支和查询：查询某个节点的子树和
2. 单点值查询：查询某个节点自身的权值

你有 {budget_b} 次分支和查询机会和 {budget_m} 次单点值查询机会。

重要约束：
- 根节点可以直接查询
- 对于非根节点 u，只有当其父节点已经被执行过分支和查询后，才能对 u 进行任何查询
- 重复查询同一项仍会消耗相应预算
- 你需要尽可能少地使用查询次数

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 分支和查询（例如查询节点 3 的子树和）：
<query_sum>3</query_sum>

- 单点值查询（例如查询节点 5 的权值）：
<query_val>5</query_val>

- 提交最终答案（例如断言节点 7 的子树和为 42）：
<answer>node=7, sum=42</answer>

- 主动放弃：
<give_up></give_up>

注意：提交答案时必须同时指定节点编号和该节点的子树和值。
"""

    game_rule_en = """\
Let's play a "Maximum Subtree Sum Inference" game. Here are the rules:

The game involves a rooted tree with nodes numbered from 1 to {n}, with root node {root}. Each node has an integer weight (which may be negative). For any node u, its subtree sum is defined as: the node's own weight plus the sum of all its direct children's subtree sums.

The tree structure is:
{tree_structure}

The root's subtree sum is: {root_sum}

It is guaranteed that there exists exactly one node whose subtree sum is strictly greater than all other nodes (i.e., uniquely maximum).

Your goal is to find this node with the maximum subtree sum and determine its subtree sum value. You can use two types of queries, but the number of queries is limited:

1. Branch sum query: Query a node's subtree sum
2. Single value query: Query a node's own weight

You have {budget_b} branch sum queries and {budget_m} single value queries available.

Important constraints:
- The root node can be queried directly
- For any non-root node u, it can only be queried after its parent has been queried with a branch sum query
- Repeated queries to the same item still consume the corresponding budget
- You should try to minimize the number of queries used

## Query and Answer Format (strictly required)

Each turn allows only one operation. Use the following XML format:

- Branch sum query (e.g., query subtree sum of node 3):
<query_sum>3</query_sum>

- Single value query (e.g., query weight of node 5):
<query_val>5</query_val>

- Submit final answer (e.g., assert node 7 has subtree sum 42):
<answer>node=7, sum=42</answer>

- Give up voluntarily:
<give_up></give_up>

Note: When submitting an answer, you must specify both the node number and its subtree sum value.
"""

    contextualized_rule_zh_1 = """\
【交通网络枢纽负荷排查系统】

调度员，您好。我们正在分析一个呈树状分布的区域交通网络，节点编号为 1 到 {n}，总枢纽为 {root}。
每个节点枢纽都有一个本地车流净增量（可能为负数，表示车流疏散）。对于任意节点 u，定义其“区域总负荷”为：该节点的本地车流净增量加上其所有直接下级分支节点的“区域总负荷”之和。

当前路网结构如下：
{tree_structure}

总枢纽的区域总负荷为：{root_sum}

系统警报：在所有节点中，存在且仅存在一个节点的区域总负荷严格大于其他所有节点，它是引发全网拥堵的核心源头。

你的目标是找到这个最大负荷枢纽及其区域总负荷值。你可以使用以下两种查询指令，但系统算力有限：

1. 分支负荷查询：查询某个节点及其下级的区域总负荷
2. 单点增量查询：查询某个节点自身的本地车流净增量

你拥有 {budget_b} 次分支负荷查询权限和 {budget_m} 次单点增量查询权限。

重要约束：
- 总枢纽节点可以直接查询
- 对于非总枢纽节点 u，只有当其上级节点已经被执行过“分支负荷查询”后，才能对 u 进行任何查询
- 重复查询同一项仍会消耗相应权限
- 你需要尽可能少地消耗查询次数

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 分支负荷查询（例如查询节点 3 的区域总负荷）：
<query_sum>3</query_sum>

- 单点增量查询（例如查询节点 5 的自身净增量）：
<query_val>5</query_val>

- 提交最终答案（例如断言节点 7 的区域总负荷为 42）：
<answer>node=7, sum=42</answer>

- 主动放弃：
<give_up></give_up>

注意：提交答案时必须同时指定节点编号和该节点的区域总负荷值。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario] Traffic Network Throughput Analysis

Hello, Dispatcher. We are analyzing a regional traffic network distributed in a tree structure. The nodes are numbered from 1 to {n}, with the main hub at {root}.
Each hub node has a local net traffic increment (which may be negative, indicating traffic dispersion). For any node u, its "regional total load" (subtree sum) is defined as: the node's local net traffic increment plus the sum of the regional total loads of all its direct downstream branches.

The current network topology is:
{tree_structure}

The regional total load of the main hub is: {root_sum}

System Alert: It is guaranteed that exactly one node has a regional total load strictly greater than all other nodes. This node is the core bottleneck causing network congestion.

Your goal is to pinpoint this maximum load hub and its regional total load value. You can use two types of query commands, but system processing power is limited:

1. Branch load query: Query the regional total load of a node and its downstream branches.
2. Single increment query: Query a node's own local net traffic increment.

You are granted {budget_b} branch load queries and {budget_m} single increment queries.

Important constraints:
- The main hub can be queried directly.
- For any non-main hub node u, it can only be queried after its parent hub has been subjected to a "branch load query".
- Repeated queries to the same node still consume the respective budget.
- You must minimize the number of queries used.

## Query and Answer Format (strictly required)

Each turn allows only one operation. Use the following XML format:

- Branch load query (e.g., query regional total load of node 3):
<query_sum>3</query_sum>

- Single increment query (e.g., query local net traffic increment of node 5):
<query_val>5</query_val>

- Submit final answer (e.g., assert node 7 has a regional total load of 42):
<answer>node=7, sum=42</answer>

- Give up voluntarily:
<give_up></give_up>

Note: When submitting an answer, you must specify both the node number and its regional total load value.
"""

    contextualized_rule_zh_2 = """\
【医疗病患接触史排查系统】

流行病学专家，您好。我们正在分析一场突发传染病的区域传播网络。防控站点呈树状结构分布，编号为 1 到 {n}，总疾控中心为 {root}。
每个站点都有一个本地新增病患指标（可能为负数，表示治愈溢出）。对于任意站点 u，定义其“区域累计感染总数”为：该站点的本地新增指标加上其所有直接下级站点的“区域累计感染总数”之和。

当前防控网络拓扑如下：
{tree_structure}

总疾控中心的区域累计感染总数为：{root_sum}

疫情警报：在所有站点中，存在且仅存在一个站点的区域累计感染总数严格大于其他所有站点，该区域是本次疫情的超级传播源。

你的目标是找到这个最大感染总数的站点及其具体数值。你可以使用以下两种检测手段，但检测试剂有限：

1. 区域流行病学筛查（分支和查询）：查询某个站点及其下辖区域的累计感染总数
2. 本地临床抽检（单点值查询）：查询某个站点自身的本地新增病患指标

你拥有 {budget_b} 次区域流行病学筛查权限和 {budget_m} 次本地临床抽检权限。

重要排查约束：
- 总疾控中心可以直接查询
- 对于非总中心站点 u，只有当其上级站点已经被执行过“区域流行病学筛查”后，才能对 u 进行任何查询
- 重复查询同一项仍会消耗相应试剂
- 你需要尽可能少地消耗检测次数

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 区域流行病学筛查（例如查询站点 3 的区域累计感染总数）：
<query_sum>3</query_sum>

- 本地临床抽检（例如查询站点 5 的本地新增指标）：
<query_val>5</query_val>

- 提交最终排查结果（例如断言站点 7 的区域累计感染总数为 42）：
<answer>node=7, sum=42</answer>

- 主动放弃：
<give_up></give_up>

注意：提交答案时必须同时指定站点编号和该站点的区域累计感染总数值。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario] Epidemic Control Network Analysis

Hello, Epidemiologist. We are analyzing the regional transmission network of a sudden infectious disease. The control stations form a tree structure, numbered from 1 to {n}, with the central CDC at {root}.
Each station has a local new patient index (which may be negative, indicating a surplus of recoveries). For any station u, its "regional cumulative infection count" (subtree sum) is defined as: the station's local new patient index plus the sum of the regional cumulative infection counts of all its direct subordinate stations.

The current control network topology is:
{tree_structure}

The regional cumulative infection count of the central CDC is: {root_sum}

Epidemic Alert: It is guaranteed that exactly one station has a regional cumulative infection count strictly greater than all other stations. This area is the super-spreader source of the current outbreak.

Your goal is to pinpoint this maximum infection station and its exact count. You can use two types of testing methods, but test kits are limited:

1. Regional epidemiological screening (Branch sum query): Query the cumulative infection count of a station and its jurisdiction.
2. Local clinical sampling (Single value query): Query a station's own local new patient index.

You have {budget_b} regional epidemiological screenings and {budget_m} local clinical samplings available.

Important constraints:
- The central CDC can be queried directly.
- For any non-central station u, it can only be queried after its parent station has been subjected to a "regional epidemiological screening".
- Repeated queries to the same station still consume the respective test kits.
- You must minimize the number of test kits used.

## Query and Answer Format (strictly required)

Each turn allows only one operation. Use the following XML format:

- Regional epidemiological screening (e.g., query cumulative infection count of station 3):
<query_sum>3</query_sum>

- Local clinical sampling (e.g., query local new patient index of station 5):
<query_val>5</query_val>

- Submit final result (e.g., assert station 7 has a cumulative infection count of 42):
<answer>node=7, sum=42</answer>

- Give up voluntarily:
<give_up></give_up>

Note: When submitting an answer, you must specify both the station number and its regional cumulative infection count.
"""

    contextualized_rule_zh_3 = """\
【教育质量评估追踪系统】

督导员，您好。我们正在对一套呈树状层级分布的教育行政体系进行质量评估。机构节点编号为 1 到 {n}，最高教育局为 {root}。
每个机构都有一个独立的基准测评得分（可能为负数，表示不达标扣分）。对于任意机构 u，定义其“分支综合教育指数”为：该机构自身的测评得分加上其所有直接下属机构的“分支综合教育指数”之和。

当前教育体系组织架构如下：
{tree_structure}

最高教育局的分支综合教育指数为：{root_sum}

评估目标：在所有机构中，存在且仅存在一个机构的分支综合教育指数严格大于其他所有机构，该节点是本年度的模范教育分支。

你的任务是找出这个综合指数最大的机构及其具体得分。你可以使用以下两种调研手段，但调研经费有限：

1. 综合分管调研（分支和查询）：查询某个机构及其所有下属机构的分支综合教育指数
2. 独立建制调研（单点值查询）：查询某个机构自身的基准测评得分

你拥有 {budget_b} 次综合分管调研经费和 {budget_m} 次独立建制调研经费。

重要评估约束：
- 最高教育局可以直接被调研
- 对于非最高机构 u，只有当其直属上级机构已经被执行过“综合分管调研”后，才能对 u 进行任何下沉调研
- 重复调研同一机构仍会消耗相应经费
- 你需要尽可能少地消耗调研次数

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 综合分管调研（例如查询机构 3 的分支综合教育指数）：
<query_sum>3</query_sum>

- 独立建制调研（例如查询机构 5 的基准测评得分）：
<query_val>5</query_val>

- 提交最终评估结果（例如断言机构 7 的分支综合教育指数为 42）：
<answer>node=7, sum=42</answer>

- 主动放弃：
<give_up></give_up>

注意：提交答案时必须同时指定机构编号和该机构的分支综合教育指数。
"""

    contextualized_rule_en_3 = """\
[Education Scenario] Education Quality Assessment Tracking System

Hello, Inspector. We are conducting a quality assessment on a hierarchically distributed educational administrative system. The institutional nodes are numbered from 1 to {n}, with the Supreme Education Bureau at {root}.
Each institution has an independent baseline evaluation score (which may be negative, indicating a penalty for underperformance). For any institution u, its "branch comprehensive education index" (subtree sum) is defined as: the institution's own evaluation score plus the sum of the branch comprehensive education indices of all its direct subordinate institutions.

The current organizational structure is:
{tree_structure}

The branch comprehensive education index of the Supreme Education Bureau is: {root_sum}

Assessment Objective: It is guaranteed that exactly one institution has a branch comprehensive education index strictly greater than all other institutions. This node represents the model educational branch of the year.

Your task is to identify this institution with the maximum comprehensive index and its exact score. You can use two types of investigative methods, but funding is limited:

1. Comprehensive branch investigation (Branch sum query): Query the comprehensive education index of an institution and all its subordinates.
2. Independent unit investigation (Single value query): Query an institution's own baseline evaluation score.

You have {budget_b} comprehensive branch investigations and {budget_m} independent unit investigations available.

Important constraints:
- The Supreme Education Bureau can be investigated directly.
- For any non-supreme institution u, it can only be subjected to downward investigation after its direct superior institution has undergone a "comprehensive branch investigation".
- Repeated investigations of the same institution still consume the respective funding.
- You must minimize the number of investigation queries used.

## Query and Answer Format (strictly required)

Each turn allows only one operation. Use the following XML format:

- Comprehensive branch investigation (e.g., query comprehensive index of institution 3):
<query_sum>3</query_sum>

- Independent unit investigation (e.g., query evaluation score of institution 5):
<query_val>5</query_val>

- Submit final assessment result (e.g., assert institution 7 has a comprehensive index of 42):
<answer>node=7, sum=42</answer>

- Give up voluntarily:
<give_up></give_up>

Note: When submitting an answer, you must specify both the institution number and its branch comprehensive education index.
"""

    contextualized_rule_zh_4 = """\
【工业组件供应链利润分析系统】

分析师，您好。我们正在审计一个复杂工业产品的装配供应链（呈树状依赖结构）。组件编号为 1 到 {n}，最终成品节点为 {root}。
每个生产组件都有一个直接利润贡献值（可能为负数，表示加工成本高于附加值）。对于任意组件 u，定义其“累计装配净利润”为：该组件自身的直接利润贡献加上其所有直接下级依赖组件的“累计装配净利润”之和。

当前供应链的BOM（物料清单）结构如下：
{tree_structure}

最终成品的累计装配净利润为：{root_sum}

审计目标：在所有节点中，存在且仅存在一个组件及其依赖链条的累计装配净利润严格大于其他所有节点，这是全供应链中最核心的利润增长极。

你的任务是找出这个最大净利润的组件总成及其利润值。你可以使用以下两种审计指令，但系统调用配额有限：

1. 总成累计利润审计（分支和查询）：查询某个组件及其所有底层依赖件的累计装配净利润
2. 零件直接利润审计（单点值查询）：查询某个组件自身的直接利润贡献值

你拥有 {budget_b} 次总成累计利润审计配额和 {budget_m} 次零件直接利润审计配额。

重要审计约束：
- 最终成品节点可以直接查询
- 对于非最终组件 u，只有当其父级装配节点已经被执行过“总成累计利润审计”后，才能对 u 进行任何查询
- 重复查询同一项仍会消耗相应配额
- 你需要尽可能少地消耗调用次数

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 总成累计利润审计（例如查询组件 3 的累计装配净利润）：
<query_sum>3</query_sum>

- 零件直接利润审计（例如查询组件 5 的直接利润贡献）：
<query_val>5</query_val>

- 提交最终审计报告（例如断言组件 7 的累计装配净利润为 42）：
<answer>node=7, sum=42</answer>

- 主动放弃：
<give_up></give_up>

注意：提交答案时必须同时指定组件编号和该组件的累计装配净利润值。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario] Industrial Component Supply Chain Profit Analysis

Hello, Analyst. We are auditing the assembly supply chain of a complex industrial product, structured as a dependency tree. The components are numbered from 1 to {n}, with the final product node at {root}.
Each component has a direct profit contribution value (which may be negative, indicating processing costs exceed value-added). For any component u, its "cumulative assembly net profit" (subtree sum) is defined as: the component's own direct profit contribution plus the sum of the cumulative assembly net profits of all its direct downstream dependencies.

The current BOM (Bill of Materials) structure is:
{tree_structure}

The cumulative assembly net profit of the final product is: {root_sum}

Audit Objective: It is guaranteed that exactly one component and its dependency chain have a cumulative assembly net profit strictly greater than all other nodes. This is the core profit growth pole of the entire supply chain.

Your task is to identify this maximum net profit assembly and its exact profit value. You can use two types of audit commands, but system quotas are limited:

1. Assembly cumulative profit audit (Branch sum query): Query the cumulative assembly net profit of a component and all its dependencies.
2. Component direct profit audit (Single value query): Query a component's own direct profit contribution.

You are allocated {budget_b} assembly cumulative profit audits and {budget_m} component direct profit audits.

Important constraints:
- The final product node can be queried directly.
- For any non-final component u, it can only be queried after its parent assembly node has undergone an "assembly cumulative profit audit".
- Repeated queries to the same component still consume the respective quota.
- You must minimize the number of command quotas used.

## Query and Answer Format (strictly required)

Each turn allows only one operation. Use the following XML format:

- Assembly cumulative profit audit (e.g., query cumulative net profit of component 3):
<query_sum>3</query_sum>

- Component direct profit audit (e.g., query direct profit contribution of component 5):
<query_val>5</query_val>

- Submit final audit report (e.g., assert component 7 has a cumulative net profit of 42):
<answer>node=7, sum=42</answer>

- Give up voluntarily:
<give_up></give_up>

Note: When submitting an answer, you must specify both the component number and its cumulative assembly net profit value.
"""

    contextualized_rule_zh_5 = """\
【商业犯罪涉案资金追踪系统】

调查员，您好。我们正在侦办一起跨国洗钱案，涉案的空壳企业网络呈树状控股结构。企业节点编号为 1 到 {n}，最终控股集团为 {root}。
每个企业账户都有一个直接截留的非法资金额（可能为负数，表示资金亏空或转移流失）。对于任意企业 u，定义其“涉案总资金池”为：该企业自身的直接截留金额加上其所有直接控股子公司的“涉案总资金池”之和。

当前查明的企业股权控制结构如下：
{tree_structure}

最终控股集团的涉案总资金池为：{root_sum}

侦查目标：在所有关联企业中，存在且仅存在一个控股分支的涉案总资金池严格大于其他所有分支，该节点是整个洗钱网络的核心蓄水池。

你的任务是揪出这个最大资金池的企业及其具体涉案金额。你可以使用以下两种搜查令，但司法审批额度有限：

1. 连带资产清查（分支和查询）：查询某个企业及其所有子公司的涉案总资金池
2. 独立账户穿透（单点值查询）：查询某个企业账户的直接截留金额

你拥有 {budget_b} 次连带资产清查审批额度和 {budget_m} 次独立账户穿透审批额度。

重要侦查约束：
- 最终控股集团可以直接被清查
- 对于非顶层企业 u，只有当其直接母公司已经被执行过“连带资产清查”后，才能对 u 申请任何搜查令
- 重复清查同一企业仍会消耗相应审批额度
- 你需要尽可能少地消耗审批次数

## 查询与提交答案的格式（必须严格遵守）

每次只能进行一个操作。请使用以下 XML 格式：

- 连带资产清查（例如查询企业 3 的涉案总资金池）：
<query_sum>3</query_sum>

- 独立账户穿透（例如查询企业 5 的直接截留金额）：
<query_val>5</query_val>

- 提交最终结案报告（例如断言企业 7 的涉案总资金池为 42）：
<answer>node=7, sum=42</answer>

- 主动放弃调查：
<give_up></give_up>

注意：提交答案时必须同时指定企业编号和该企业的涉案总资金池金额。
"""

    contextualized_rule_en_5 = """\
[Law Scenario] Commercial Crime Illicit Fund Tracing System

Hello, Investigator. We are investigating a transnational money laundering case involving a network of shell companies structured as a holding tree. The enterprise nodes are numbered from 1 to {n}, with the Ultimate Holding Group at {root}.
Each enterprise account has directly retained illicit funds (which may be negative, indicating fund deficits or outbound transfers). For any enterprise u, its "total illicit fund pool" (subtree sum) is defined as: the enterprise's directly retained funds plus the sum of the total illicit fund pools of all its direct subsidiaries.

The current corporate ownership structure is:
{tree_structure}

The total illicit fund pool of the Ultimate Holding Group is: {root_sum}

Investigation Objective: It is guaranteed that exactly one holding branch has a total illicit fund pool strictly greater than all other branches. This node serves as the core reservoir of the entire money laundering network.

Your task is to identify this maximum fund pool enterprise and its exact involved amount. You can use two types of search warrants, but judicial approval quotas are limited:

1. Comprehensive asset clearance (Branch sum query): Query the total illicit fund pool of an enterprise and all its subsidiaries.
2. Independent account penetration (Single value query): Query an enterprise account's directly retained illicit funds.

You are granted {budget_b} comprehensive asset clearance approvals and {budget_m} independent account penetration approvals.

Important investigation constraints:
- The Ultimate Holding Group can be cleared directly.
- For any non-top-level enterprise u, a warrant can only be requested for u after its direct parent company has been subjected to a "comprehensive asset clearance".
- Repeated clearances of the same enterprise still consume the respective approval quota.
- You must minimize the number of warrant approvals used.

## Query and Answer Format (strictly required)

Each turn allows only one operation. Use the following XML format:

- Comprehensive asset clearance (e.g., query total illicit fund pool of enterprise 3):
<query_sum>3</query_sum>

- Independent account penetration (e.g., query directly retained funds of enterprise 5):
<query_val>5</query_val>

- Submit final case report (e.g., assert enterprise 7 has a total illicit fund pool of 42):
<answer>node=7, sum=42</answer>

- Give up voluntarily:
<give_up></give_up>

Note: When submitting an answer, you must specify both the enterprise number and its total illicit fund pool amount.
"""

    tags = ["answer", "query_sum", "query_val", "give_up"]
    
    # 类属性：推理类型和数据结构
    reasoning_type = "演绎推理"
    data_structure = "树"
    
    # 难度配置：
    # 1 (简单)       - 小树，3节点，结构简单
    # 2 (中等偏下)   - 5节点，单分支
    # 3 (中等偏上)   - 7节点，二叉结构
    # 4 (较难)       - 10节点，多分支
    # 5 (难)         - 12节点，复杂结构

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 3,
                "root": 1,
                # 树结构: 1 -> [2, 3]
                # 权值: w[1]=-5, w[2]=10, w[3]=-2
                # 子树和: S[2]=10, S[3]=-2, S[1]=-5+10-2=3
                # 最大: S[2]=10
                "tree": {1: [2, 3], 2: [], 3: []},
                "weights": {1: -5, 2: 10, 3: -2},
                "budget_b": 3,
                "budget_m": 2,
                "max_node": 2,
            },
            2: {
                "n": 5,
                "root": 1,
                # 树结构: 1 -> [2], 2 -> [3, 4], 3 -> [5]
                # 权值: w[1]=-10, w[2]=5, w[3]=8, w[4]=-3, w[5]=12
                # 子树和: S[5]=12, S[3]=8+12=20, S[4]=-3, S[2]=5+20-3=22, S[1]=-10+22=12
                # 最大: S[2]=22
                "tree": {1: [2], 2: [3, 4], 3: [5], 4: [], 5: []},
                "weights": {1: -10, 2: 5, 3: 8, 4: -3, 5: 12},
                "budget_b": 6,
                "budget_m": 3,
                "max_node": 2,
            },
            3: {
                "n": 7,
                "root": 1,
                # 树结构: 1 -> [2, 3], 2 -> [4, 5], 3 -> [6, 7]
                # 权值: w[1]=-10, w[2]=10, w[3]=-5, w[4]=15, w[5]=8, w[6]=3, w[7]=2
                # 子树和: S[4]=15, S[5]=8, S[2]=10+15+8=33, S[6]=3, S[7]=2, S[3]=-5+3+2=0, S[1]=-10+33+0=23
                # 最大: S[2]=33
                "tree": {1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [], 5: [], 6: [], 7: []},
                "weights": {1: -10, 2: 10, 3: -5, 4: 15, 5: 8, 6: 3, 7: 2},
                "budget_b": 8,
                "budget_m": 4,
                "max_node": 2,
            },
            4: {
                "n": 10,
                "root": 1,
                # 树结构: 1 -> [2, 3, 4], 2 -> [5, 6], 3 -> [7], 4 -> [8, 9, 10]
                # 权值: w[1]=-50, w[2]=20, w[3]=10, w[4]=-8, w[5]=25, w[6]=-10, w[7]=18, w[8]=5, w[9]=3, w[10]=4
                # 子树和: S[5]=25, S[6]=-10, S[2]=20+25-10=35, S[7]=18, S[3]=10+18=28, 
                #        S[8]=5, S[9]=3, S[10]=4, S[4]=-8+5+3+4=4, S[1]=-50+35+28+4=17
                # 最大: S[2]=35
                "tree": {1: [2, 3, 4], 2: [5, 6], 3: [7], 4: [8, 9, 10], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []},
                "weights": {1: -50, 2: 20, 3: 10, 4: -8, 5: 25, 6: -10, 7: 18, 8: 5, 9: 3, 10: 4},
                "budget_b": 12,
                "budget_m": 6,
                "max_node": 2,
            },
            5: {
                "n": 12,
                "root": 1,
                # 树结构: 1 -> [2, 3], 2 -> [4, 5, 6], 3 -> [7, 8], 5 -> [9, 10], 7 -> [11, 12]
                # 权值: w[1]=-20, w[2]=-15, w[3]=8, w[4]=30, w[5]=40, w[6]=-20, w[7]=25, w[8]=-5, 
                #       w[9]=-8, w[10]=-12, w[11]=15, w[12]=10
                # 子树和: S[4]=30, S[9]=-8, S[10]=-12, S[5]=40-8-12=20, S[6]=-20, S[2]=-15+30+20-20=15
                #        S[11]=15, S[12]=10, S[7]=25+15+10=50, S[8]=-5, S[3]=8+50-5=53, S[1]=-20+15+53=48
                # 最大: S[3]=53
                "tree": {1: [2, 3], 2: [4, 5, 6], 3: [7, 8], 4: [], 5: [9, 10], 6: [], 7: [11, 12], 8: [], 9: [], 10: [], 11: [], 12: []},
                "weights": {1: -20, 2: -15, 3: 8, 4: 30, 5: 40, 6: -20, 7: 25, 8: -5, 9: -8, 10: -12, 11: 15, 12: 10},
                "budget_b": 15,
                "budget_m": 8,
                "max_node": 3,
            },
        },
        "en": {
            1: {
                "n": 3,
                "root": 1,
                "tree": {1: [2, 3], 2: [], 3: []},
                "weights": {1: -5, 2: 10, 3: -2},
                "budget_b": 3,
                "budget_m": 2,
                "max_node": 2,
            },
            2: {
                "n": 5,
                "root": 1,
                "tree": {1: [2], 2: [3, 4], 3: [5], 4: [], 5: []},
                "weights": {1: -10, 2: 5, 3: 8, 4: -3, 5: 12},
                "budget_b": 6,
                "budget_m": 3,
                "max_node": 2,
            },
            3: {
                "n": 7,
                "root": 1,
                "tree": {1: [2, 3], 2: [4, 5], 3: [6, 7], 4: [], 5: [], 6: [], 7: []},
                "weights": {1: -10, 2: 10, 3: -5, 4: 15, 5: 8, 6: 3, 7: 2},
                "budget_b": 8,
                "budget_m": 4,
                "max_node": 2,
            },
            4: {
                "n": 10,
                "root": 1,
                "tree": {1: [2, 3, 4], 2: [5, 6], 3: [7], 4: [8, 9, 10], 5: [], 6: [], 7: [], 8: [], 9: [], 10: []},
                "weights": {1: -50, 2: 20, 3: 10, 4: -8, 5: 25, 6: -10, 7: 18, 8: 5, 9: 3, 10: 4},
                "budget_b": 12,
                "budget_m": 6,
                "max_node": 2,
            },
            5: {
                "n": 12,
                "root": 1,
                "tree": {1: [2, 3], 2: [4, 5, 6], 3: [7, 8], 4: [], 5: [9, 10], 6: [], 7: [11, 12], 8: [], 9: [], 10: [], 11: [], 12: []},
                "weights": {1: -20, 2: -15, 3: 8, 4: 30, 5: 40, 6: -20, 7: 25, 8: -5, 9: -8, 10: -12, 11: 15, 12: 10},
                "budget_b": 15,
                "budget_m": 8,
                "max_node": 3,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏，加载配置并计算真实的子树和"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 基本信息
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self._game_info["budget_b"] = cfg["budget_b"]
        self._game_info["budget_m"] = cfg["budget_m"]
        
        # 树结构和权值
        self.tree = cfg["tree"]
        self.weights = cfg["weights"]
        self.root = cfg["root"]
        
        # 剩余预算
        self.budget_b_remaining = cfg["budget_b"]
        self.budget_m_remaining = cfg["budget_m"]
        
        # 已查询过分支和的节点（用于判断可见性）
        self.unlocked_nodes = set()
        
        # 构建父节点映射
        self.parent = {}
        for node, children in self.tree.items():
            for child in children:
                self.parent[child] = node
        
        # 计算所有节点的真实子树和
        self.subtree_sums = {}
        self._compute_subtree_sum(self.root)
        
        # 记录答案
        self.max_node = cfg["max_node"]
        self.max_sum = self.subtree_sums[self.max_node]
        
        # 格式化树结构用于显示
        tree_str = self._format_tree_structure()
        self._game_info["tree_structure"] = tree_str
        self._game_info["root_sum"] = self.subtree_sums[self.root]

    def _compute_subtree_sum(self, node):
        """递归计算节点的子树和"""
        if node in self.subtree_sums:
            return self.subtree_sums[node]
        
        children = self.tree.get(node, [])
        children_sum = sum(self._compute_subtree_sum(child) for child in children)
        self.subtree_sums[node] = self.weights[node] + children_sum
        return self.subtree_sums[node]

    def _format_tree_structure(self):
        """格式化树结构为可读字符串"""
        lines = []
        for node in sorted(self.tree.keys()):
            children = self.tree[node]
            if children:
                children_str = ", ".join(map(str, children))
                lines.append(f"节点 {node} 的子节点: [{children_str}]" if self.config.language == "zh" 
                           else f"Node {node}'s children: [{children_str}]")
            else:
                lines.append(f"节点 {node} 是叶节点" if self.config.language == "zh" 
                           else f"Node {node} is a leaf")
        return "\n".join(lines)

    def _is_unlocked(self, node):
        """检查节点是否可以被查询（根节点或其父节点已被查询分支和）"""
        if node == self.root:
            return True
        parent_node = self.parent.get(node)
        return parent_node in self.unlocked_nodes

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 解析答案格式: node=X, sum=Y
        try:
            kv_pairs = [x.strip() for x in raw_ans.split(",")]
            ans_dict = {}
            for kv in kv_pairs:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
            
            if "node" not in ans_dict or "sum" not in ans_dict:
                return False
            
            # 检查节点和子树和
            node = int(ans_dict["node"])
            claimed_sum = int(ans_dict["sum"])
            
            # 必须是最大子树和的节点，且数值正确
            return node == self.max_node and claimed_sum == self.max_sum
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑：根据查询类型生成响应"""
        lang = self.config.language
        
        # 处理放弃
        if "give_up" in parsed_info:
            msg = "游戏结束，你选择了放弃。" if lang == "zh" else "Game over, you chose to give up."
            self.state.set_state("failed", "give up")
            return msg
        
        # 处理分支和查询
        if "query_sum" in parsed_info:
            try:
                node = int(parsed_info["query_sum"].strip())
                
                # 检查节点是否存在
                if node not in self.tree:
                    return "错误：节点不存在。" if lang == "zh" else "Error: Node does not exist."
                
                # 检查预算
                if self.budget_b_remaining <= 0:
                    return "错误：分支和查询预算已用尽。" if lang == "zh" else "Error: No remaining branch sum query budget."
                
                # 检查可见性
                if not self._is_unlocked(node):
                    return "错误：该节点的父节点尚未解锁（父节点需先执行分支和查询）。" if lang == "zh" \
                        else "Error: Parent node not unlocked (parent must be queried with branch sum first)."
                
                # 执行查询
                self.budget_b_remaining -= 1
                self.unlocked_nodes.add(node)
                result = self.subtree_sums[node]
                
                if lang == "zh":
                    return f"节点 {node} 的子树和为 {result}。剩余分支和查询次数：{self.budget_b_remaining}，剩余单点值查询次数：{self.budget_m_remaining}。"
                else:
                    return f"Subtree sum of node {node} is {result}. Remaining branch queries: {self.budget_b_remaining}, remaining value queries: {self.budget_m_remaining}."
                    
            except ValueError:
                return "错误：无效的节点编号。" if lang == "zh" else "Error: Invalid node number."
        
        # 处理单点值查询
        if "query_val" in parsed_info:
            try:
                node = int(parsed_info["query_val"].strip())
                
                # 检查节点是否存在
                if node not in self.tree:
                    return "错误：节点不存在。" if lang == "zh" else "Error: Node does not exist."
                
                # 检查预算
                if self.budget_m_remaining <= 0:
                    return "错误：单点值查询预算已用尽。" if lang == "zh" else "Error: No remaining single value query budget."
                
                # 检查可见性
                if not self._is_unlocked(node):
                    return "错误：该节点的父节点尚未解锁（父节点需先执行分支和查询）。" if lang == "zh" \
                        else "Error: Parent node not unlocked (parent must be queried with branch sum first)."
                
                # 执行查询
                self.budget_m_remaining -= 1
                result = self.weights[node]
                
                if lang == "zh":
                    return f"节点 {node} 的权值为 {result}。剩余分支和查询次数：{self.budget_b_remaining}，剩余单点值查询次数：{self.budget_m_remaining}。"
                else:
                    return f"Weight of node {node} is {result}. Remaining branch queries: {self.budget_b_remaining}, remaining value queries: {self.budget_m_remaining}."
                    
            except ValueError:
                return "错误：无效的节点编号。" if lang == "zh" else "Error: Invalid node number."
        
        # 未识别的查询
        return "错误：无效的查询格式。" if lang == "zh" else "Error: Invalid query format."

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成一个明显不同的错误答案。
        
        由于 _cf_core_produce 返回的是包含数值的自然语言字符串，
        我们尝试找到其中的关键数值并进行篡改。
        """
        import re as _re
        
        # 尝试找到响应中的关键数值（子树和或权值）
        # 英文格式: "Subtree sum of node X is Y." 或 "Weight of node X is Y."
        # 中文格式: "节点 X 的子树和为 Y。" 或 "节点 X 的权值为 Y。"
        
        # 匹配 "is <number>" 或 "为 <number>"
        pattern = _re.compile(r'(?:is|为)\s*(-?\d+)')
        match = pattern.search(correct)
        if match:
            original_val = int(match.group(1))
            # 生成一个不同的值
            wrong_val = original_val + 7 if original_val >= 0 else original_val - 7
            return correct[:match.start(1)] + str(wrong_val) + correct[match.end(1):]
        
        # 如果响应是纯数字
        stripped = correct.strip()
        if stripped.lstrip('-').isdigit():
            return str(int(stripped) + 1)
        
        # 兜底：追加标记
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        为避免状态污染和预算数字不一致的问题，直接根据已知数据生成响应，
        而不调用 _cf_core_produce。
        """
        queries = []
        lang = self.config.language
        all_nodes = sorted(self.tree.keys())
        
        for node in all_nodes:
            # 1. 分支和查询 (query_sum)
            result_sum = self.subtree_sums[node]
            if lang == "zh":
                resp_sum = f"节点 {node} 的子树和为 {result_sum}。"
            else:
                resp_sum = f"Subtree sum of node {node} is {result_sum}."
            
            queries.append({
                "query": f"<query_sum>{node}</query_sum>",
                "answer": resp_sum
            })
            
            # 2. 单点值查询 (query_val)
            result_val = self.weights[node]
            if lang == "zh":
                resp_val = f"节点 {node} 的权值为 {result_val}。"
            else:
                resp_val = f"Weight of node {node} is {result_val}."
            
            queries.append({
                "query": f"<query_val>{node}</query_val>",
                "answer": resp_val
            })
        
        return queries