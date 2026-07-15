from .base import Game
import random

class HiddenTreeFunctionGame(Game):

    game_rule_zh = """\
我们来玩一个"树结构函数推理"游戏，规则如下：

游戏设定了一个包含 {n} 个结点的有根树（连通、无环，每个结点最多一个父结点，根结点无父结点）。结点编号为：{node_list}。

我定义了一个隐藏函数 f，它为每个结点赋予一个非负整数值。你的目标是通过交互查询来推断这个函数的规律，并在测试阶段准确预测指定结点的函数值。

你可以使用以下查询来了解树结构和函数规律（每种查询有配额限制）：

1. **取值查询**（配额 {quota_val} 次）：查询结点 X 的函数值
2. **子结点查询**（配额 {quota_children} 次）：查询结点 X 的所有直接子结点
3. **祖先关系判断**（配额 {quota_ancestor} 次）：判断结点 X 是否为结点 Y 的严格祖先（X=Y 时返回"否"）
4. **父结点查询**（配额 {quota_parent} 次）：查询结点 X 的父结点

我会指定 {test_count} 个目标结点。在此阶段：
- **禁止**使用取值查询
- 允许继续使用结构查询（子结点、祖先关系、父结点查询），但总计不超过 {test_quota} 次
- 你需要一次性提交这些目标结点的函数值预测

每次只能提交一个查询。格式如下：

- 取值查询（例如查询结点 5）：
<query_val>5</query_val>

- 子结点查询（例如查询结点 3 的子结点）：
<query_children>3</query_children>

- 祖先关系判断（例如判断 2 是否为 7 的祖先）：
<query_ancestor>2,7</query_ancestor>

- 父结点查询（例如查询结点 4 的父结点）：
<query_parent>4</query_parent>

- 进入测试阶段（当你准备好进入测试阶段时）：
<enter_test></enter_test>

- 提交最终答案（测试阶段，格式为"结点=值"，用逗号分隔）：
<answer>1=5,3=8,7=2</answer>

- 探索阶段的查询配额用完后会自动进入测试阶段
- 测试阶段禁止取值查询，结构查询总数不能超过配额
- 答案必须包含所有测试目标结点，且值必须完全正确
"""

    game_rule_en = """\
Let's play a "Tree Structure Function Deduction" game. Here are the rules:

The game features a rooted tree with {n} nodes (connected, acyclic, each node has at most one parent, root has no parent). Node IDs are: {node_list}.

I have defined a hidden function f that assigns a non-negative integer value to each node. Your goal is to infer the pattern of this function through interactive queries and accurately predict the function values for specified nodes in the test phase.

You can use the following queries to learn about the tree structure and function pattern (each query type has a quota):

1. **Value Query** (quota: {quota_val} times): Query the function value of node X
2. **Children Query** (quota: {quota_children} times): Query all direct children of node X
3. **Ancestor Query** (quota: {quota_ancestor} times): Check if node X is a strict ancestor of node Y (returns "No" when X=Y)
4. **Parent Query** (quota: {quota_parent} times): Query the parent of node X

I will specify {test_count} target nodes. In this phase:
- Value queries are **forbidden**
- Structure queries (children, ancestor, parent) are allowed but total count cannot exceed {test_quota}
- You must submit predictions for all target nodes at once

Only one query per turn. Format:

- Value Query (e.g., query node 5):
<query_val>5</query_val>

- Children Query (e.g., query children of node 3):
<query_children>3</query_children>

- Ancestor Query (e.g., check if 2 is ancestor of 7):
<query_ancestor>2,7</query_ancestor>

- Parent Query (e.g., query parent of node 4):
<query_parent>4</query_parent>

- Enter Test Phase (when ready for test phase):
<enter_test></enter_test>

- Submit Final Answer (in test phase, format "node=value", comma-separated):
<answer>1=5,3=8,7=2</answer>

- Exploration phase ends automatically when quotas are exhausted
- Test phase forbids value queries; structure queries cannot exceed quota
- Answer must include all test target nodes with exact values
"""

    contextualized_rule_zh_1 = """\
欢迎使用“交通网络级联覆盖度”分析系统，工作规程如下：

系统映射了一个包含 {n} 个枢纽节点的层级分发路网（连通、无环，每个枢纽最多一个上游，总根节点无上游）。枢纽编号为：{node_list}。

路网中存在一个隐藏的级联流量函数 f，代表每个枢纽节点所能辐射的总节点数（即包含自身在内的所有下游及分支枢纽总数）。你的目标是通过交互查询推断流量分布模式，并在测试阶段准确预测指定枢纽的流量覆盖值。

你可以使用以下指令来摸排路网结构和流量规律（每种指令有配额限制）：

1. **流量查询**（配额 {quota_val} 次）：查询枢纽 X 的流量覆盖值
2. **下游查询**（配额 {quota_children} 次）：查询枢纽 X 的所有直接下游枢纽
3. **上游路径判断**（配额 {quota_ancestor} 次）：判断枢纽 X 是否为枢纽 Y 的严格上游（X=Y 时返回"否"）
4. **上游查询**（配额 {quota_parent} 次）：查询枢纽 X 的直接上游枢纽

系统会指定 {test_count} 个目标枢纽。在此阶段：
- **禁止**使用流量查询
- 允许继续使用结构查询（下游、路径判断、上游查询），但总计不超过 {test_quota} 次
- 你需要一次性提交这些目标枢纽的流量覆盖值预测

每次只能提交一个查询。格式如下：

- 流量查询（例如查询枢纽 5）：
<query_val>5</query_val>

- 下游查询（例如查询枢纽 3 的直接下游）：
<query_children>3</query_children>

- 上游路径判断（例如判断 2 是否为 7 的严格上游）：
<query_ancestor>2,7</query_ancestor>

- 上游查询（例如查询枢纽 4 的直接上游）：
<query_parent>4</query_parent>

- 进入测试阶段（当你准备好进入测试阶段时）：
<enter_test></enter_test>

- 提交最终预测（测试阶段，格式为"枢纽=值"，用逗号分隔）：
<answer>1=5,3=8,7=2</answer>

- 勘探阶段的指令配额用完后会自动进入测试阶段
- 测试阶段禁止流量查询，结构查询总数不能超过配额
- 预测结果必须包含所有测试目标枢纽，且数值必须完全正确
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Traffic Network Cascade Coverage" analysis system. The operational protocol is as follows:

The system has mapped a hierarchical distribution network with {n} hub nodes (connected, acyclic, each hub has at most one upstream, root has no upstream). Hub IDs are: {node_list}.

There is a hidden cascade traffic function f that represents the total number of nodes covered by each hub (including itself and all downstream branches). Your goal is to infer the traffic distribution pattern through interactive queries and accurately predict the coverage values for specified hubs in the test phase.

You can use the following queries to learn about the network structure and traffic pattern (each query type has a quota):

1. **Traffic Query** (quota: {quota_val} times): Query the coverage value of hub X
2. **Downstream Query** (quota: {quota_children} times): Query all direct downstream hubs of hub X
3. **Upstream Path Query** (quota: {quota_ancestor} times): Check if hub X is a strict upstream of hub Y (returns "No" when X=Y)
4. **Upstream Query** (quota: {quota_parent} times): Query the direct upstream of hub X

The system will specify {test_count} target hubs. In this phase:
- Traffic queries are **forbidden**
- Structure queries (downstream, path, upstream) are allowed but total count cannot exceed {test_quota}
- You must submit predictions for all target hubs at once

Only one query per turn. Format:

- Traffic Query (e.g., query hub 5):
<query_val>5</query_val>

- Downstream Query (e.g., query downstream of hub 3):
<query_children>3</query_children>

- Upstream Path Query (e.g., check if 2 is upstream of 7):
<query_ancestor>2,7</query_ancestor>

- Upstream Query (e.g., query upstream of hub 4):
<query_parent>4</query_parent>

- Enter Test Phase (when ready for test phase):
<enter_test></enter_test>

- Submit Final Answer (in test phase, format "hub=value", comma-separated):
<answer>1=5,3=8,7=2</answer>

- Exploration phase ends automatically when quotas are exhausted
- Test phase forbids traffic queries; structure queries cannot exceed quota
- Answer must include all test target hubs with exact values
"""

    contextualized_rule_zh_2 = """\
欢迎使用“传染病溯源与传播链”流行病学调查系统，工作规程如下：

系统记录了一个包含 {n} 个病例节点的病毒传播树（连通、无环，每个病例最多一个直接暴露源，零号病人无暴露源）。病例编号为：{node_list}。

系统内置了一个隐藏的聚集性感染函数 f，代表由病例 X 及其后续传播链引发的总感染人数（包含其自身）。你的目标是通过交互式流调查询来推断传播规律，并在测试阶段准确预测指定病例的聚集性感染规模。

你可以使用以下指令来摸排传播链和感染规模（每种指令有配额限制）：

1. **规模查询**（配额 {quota_val} 次）：查询病例 X 的聚集性感染规模
2. **继发查询**（配额 {quota_children} 次）：查询病例 X 的所有直接继发病例
3. **溯源路径判断**（配额 {quota_ancestor} 次）：判断病例 X 是否为病例 Y 的传播链严格上游源头（X=Y 时返回"否"）
4. **暴露源查询**（配额 {quota_parent} 次）：查询病例 X 的直接暴露源

系统会指定 {test_count} 个流调目标病例。在此阶段：
- **禁止**使用规模查询
- 允许继续使用结构查询（继发、溯源路径、暴露源查询），但总计不超过 {test_quota} 次
- 你需要一次性提交这些目标病例的聚集性感染规模预测

每次只能提交一个查询。格式如下：

- 规模查询（例如查询病例 5）：
<query_val>5</query_val>

- 继发查询（例如查询病例 3 的直接继发）：
<query_children>3</query_children>

- 溯源路径判断（例如判断 2 是否为 7 的源头）：
<query_ancestor>2,7</query_ancestor>

- 暴露源查询（例如查询病例 4 的直接暴露源）：
<query_parent>4</query_parent>

- 进入测试阶段（当你准备好进入测试阶段时）：
<enter_test></enter_test>

- 提交最终预测（测试阶段，格式为"病例=值"，用逗号分隔）：
<answer>1=5,3=8,7=2</answer>

- 勘探阶段的指令配额用完后会自动进入测试阶段
- 测试阶段禁止规模查询，结构查询总数不能超过配额
- 预测结果必须包含所有测试目标病例，且数值必须完全正确
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Infectious Disease Tracing and Transmission Chains" epidemiological investigation system. The protocol is as follows:

The system has logged a virus transmission tree with {n} case nodes (connected, acyclic, each case has at most one direct source of exposure, Patient Zero has no source). Case IDs are: {node_list}.

There is a hidden cluster infection function f representing the total number of infected individuals caused by Case X and its subsequent transmission chain (including itself). Your goal is to infer the transmission pattern through interactive epidemiological queries and accurately predict the cluster infection sizes for specified cases in the test phase.

You can use the following queries to trace transmission chains and cluster sizes (each query has a quota):

1. **Cluster Size Query** (quota: {quota_val} times): Query the total infection size of Case X
2. **Secondary Case Query** (quota: {quota_children} times): Query all direct secondary cases of Case X
3. **Tracing Path Query** (quota: {quota_ancestor} times): Check if Case X is a strict upstream transmission source of Case Y (returns "No" when X=Y)
4. **Exposure Source Query** (quota: {quota_parent} times): Query the direct exposure source of Case X

The system will specify {test_count} target cases. In this phase:
- Cluster size queries are **forbidden**
- Structure queries (secondary case, tracing path, exposure source) are allowed but total count cannot exceed {test_quota}
- You must submit predictions for all target cases at once

Only one query per turn. Format:

- Cluster Size Query (e.g., query case 5):
<query_val>5</query_val>

- Secondary Case Query (e.g., query secondary cases of case 3):
<query_children>3</query_children>

- Tracing Path Query (e.g., check if 2 is the source of 7):
<query_ancestor>2,7</query_ancestor>

- Exposure Source Query (e.g., query direct source of case 4):
<query_parent>4</query_parent>

- Enter Test Phase (when ready for test phase):
<enter_test></enter_test>

- Submit Final Answer (in test phase, format "case=value", comma-separated):
<answer>1=5,3=8,7=2</answer>

- Exploration phase ends automatically when quotas are exhausted
- Test phase forbids cluster size queries; structure queries cannot exceed quota
- Answer must include all test target cases with exact values
"""

    contextualized_rule_zh_3 = """\
欢迎使用“学科知识图谱依赖树”系统，工作规程如下：

系统构建了一个包含 {n} 个知识点的前置依赖图谱（树状结构，连通、无环，每个知识点最多受一个直接前置约束，根知识点无前置）。知识点编号为：{node_list}。

图谱中存在一个隐藏的衍生权重函数 f，代表以知识点 X 为前置条件的所有衍生知识点总数（包含自身）。你的目标是通过系统指令查询来推断知识体系架构，并在测试阶段准确预测指定知识点的衍生权重。

你可以使用以下指令来摸排图谱结构和权重规律（每种指令有配额限制）：

1. **权重查询**（配额 {quota_val} 次）：查询知识点 X 的衍生权重值
2. **衍生查询**（配额 {quota_children} 次）：查询以知识点 X 为直接前置的所有衍生知识点
3. **前置依赖判断**（配额 {quota_ancestor} 次）：判断知识点 X 是否为知识点 Y 的严格前置条件（X=Y 时返回"否"）
4. **直接前置查询**（配额 {quota_parent} 次）：查询知识点 X 的直接前置节点

系统会指定 {test_count} 个核心知识点。在此阶段：
- **禁止**使用权重查询
- 允许继续使用图谱结构查询（衍生、前置依赖、直接前置查询），但总计不超过 {test_quota} 次
- 你需要一次性提交这些核心知识点的衍生权重预测

每次只能提交一个查询。格式如下：

- 权重查询（例如查询知识点 5）：
<query_val>5</query_val>

- 衍生查询（例如查询知识点 3 的直接衍生）：
<query_children>3</query_children>

- 前置依赖判断（例如判断 2 是否为 7 的前置）：
<query_ancestor>2,7</query_ancestor>

- 直接前置查询（例如查询知识点 4 的前置）：
<query_parent>4</query_parent>

- 进入测试阶段（当你准备好进入测试阶段时）：
<enter_test></enter_test>

- 提交最终预测（测试阶段，格式为"知识点=值"，用逗号分隔）：
<answer>1=5,3=8,7=2</answer>

- 勘探阶段的指令配额用完后会自动进入测试阶段
- 测试阶段禁止权重查询，结构查询总数不能超过配额
- 预测结果必须包含所有测试知识点，且数值必须完全正确
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Subject Knowledge Graph Dependency Tree" system. The operational protocol is as follows:

The system has mapped a prerequisite dependency graph with {n} knowledge points (tree structure, connected, acyclic, each point has at most one direct prerequisite, the root has none). Knowledge point IDs are: {node_list}.

There is a hidden derived weight function f that indicates the total number of knowledge points derived from point X (including itself). Your goal is to infer the architecture of the knowledge system through interactive queries and accurately predict the derived weights for specified points in the test phase.

You can use the following queries to learn about the graph structure and weight patterns (each query type has a quota):

1. **Weight Query** (quota: {quota_val} times): Query the derived weight value of knowledge point X
2. **Derivative Query** (quota: {quota_children} times): Query all direct derived knowledge points of point X
3. **Prerequisite Dependency Query** (quota: {quota_ancestor} times): Check if point X is a strict prerequisite of point Y (returns "No" when X=Y)
4. **Direct Prerequisite Query** (quota: {quota_parent} times): Query the direct prerequisite of point X

The system will specify {test_count} core knowledge points. In this phase:
- Weight queries are **forbidden**
- Graph structure queries (derivative, prerequisite dependency, direct prerequisite) are allowed but total count cannot exceed {test_quota}
- You must submit predictions for all core knowledge points at once

Only one query per turn. Format:

- Weight Query (e.g., query point 5):
<query_val>5</query_val>

- Derivative Query (e.g., query derivatives of point 3):
<query_children>3</query_children>

- Prerequisite Dependency Query (e.g., check if 2 is a prerequisite of 7):
<query_ancestor>2,7</query_ancestor>

- Direct Prerequisite Query (e.g., query prerequisite of point 4):
<query_parent>4</query_parent>

- Enter Test Phase (when ready for test phase):
<enter_test></enter_test>

- Submit Final Answer (in test phase, format "point=value", comma-separated):
<answer>1=5,3=8,7=2</answer>

- Exploration phase ends automatically when quotas are exhausted
- Test phase forbids weight queries; structure queries cannot exceed quota
- Answer must include all test knowledge points with exact values
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业产品BOM（物料清单）”解析系统，工作规程如下：

系统导入了一个包含 {n} 个组件节点的BOM装配树（连通、无环，每个组件最多归属一个父装配体，顶层产品无父装配体）。组件编号为：{node_list}。

系统中存在一个隐藏的物料统计函数 f，表示装配组件 X 所需的底层及下属零部件总数（包含组件自身构件）。你的目标是通过工艺查询来推断BOM层级规律，并在测试阶段准确预测指定组件的零部件总数。

你可以使用以下指令来摸排装配结构和物料规模（每种指令有配额限制）：

1. **件数查询**（配额 {quota_val} 次）：查询组件 X 的零部件总数
2. **子件查询**（配额 {quota_children} 次）：查询组件 X 的所有直接下级子组件
3. **装配层级判断**（配额 {quota_ancestor} 次）：判断组件 X 是否为组件 Y 的严格上级装配体（X=Y 时返回"否"）
4. **父件查询**（配额 {quota_parent} 次）：查询组件 X 的直接父级装配体

系统会指定 {test_count} 个核心物料组件。在此阶段：
- **禁止**使用件数查询
- 允许继续使用结构查询（子件、装配层级、父件查询），但总计不超过 {test_quota} 次
- 你需要一次性提交这些核心组件的零部件总数预测

每次只能提交一个查询。格式如下：

- 件数查询（例如查询组件 5）：
<query_val>5</query_val>

- 子件查询（例如查询组件 3 的直接子件）：
<query_children>3</query_children>

- 装配层级判断（例如判断 2 是否为 7 的上级）：
<query_ancestor>2,7</query_ancestor>

- 父件查询（例如查询组件 4 的父级装配体）：
<query_parent>4</query_parent>

- 进入测试阶段（当你准备好进入测试阶段时）：
<enter_test></enter_test>

- 提交最终预测（测试阶段，格式为"组件=值"，用逗号分隔）：
<answer>1=5,3=8,7=2</answer>

- 勘探阶段的指令配额用完后会自动进入测试阶段
- 测试阶段禁止件数查询，结构查询总数不能超过配额
- 预测结果必须包含所有测试目标组件，且数值必须完全正确
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Product BOM (Bill of Materials)" parsing system. The operational protocol is as follows:

The system has loaded a BOM assembly tree with {n} component nodes (connected, acyclic, each component belongs to at most one parent assembly, the top-level product has no parent). Component IDs are: {node_list}.

There is a hidden material statistics function f that represents the total number of sub-parts and components required for assembly X (including the component itself). Your goal is to infer the BOM hierarchy pattern through process queries and accurately predict the total part counts for specified components in the test phase.

You can use the following queries to investigate the assembly structure and material scales (each query type has a quota):

1. **Part Count Query** (quota: {quota_val} times): Query the total part count of component X
2. **Sub-assembly Query** (quota: {quota_children} times): Query all direct sub-assemblies of component X
3. **Assembly Hierarchy Query** (quota: {quota_ancestor} times): Check if component X is a strict parent/ancestor assembly of component Y (returns "No" when X=Y)
4. **Parent Assembly Query** (quota: {quota_parent} times): Query the direct parent assembly of component X

The system will specify {test_count} core components. In this phase:
- Part count queries are **forbidden**
- Structure queries (sub-assembly, hierarchy, parent assembly) are allowed but total count cannot exceed {test_quota}
- You must submit predictions for all core components at once

Only one query per turn. Format:

- Part Count Query (e.g., query component 5):
<query_val>5</query_val>

- Sub-assembly Query (e.g., query sub-assemblies of component 3):
<query_children>3</query_children>

- Assembly Hierarchy Query (e.g., check if 2 is an ancestor assembly of 7):
<query_ancestor>2,7</query_ancestor>

- Parent Assembly Query (e.g., query parent assembly of component 4):
<query_parent>4</query_parent>

- Enter Test Phase (when ready for test phase):
<enter_test></enter_test>

- Submit Final Answer (in test phase, format "component=value", comma-separated):
<answer>1=5,3=8,7=2</answer>

- Exploration phase ends automatically when quotas are exhausted
- Test phase forbids part count queries; structure queries cannot exceed quota
- Answer must include all test target components with exact values
"""

    contextualized_rule_zh_5 = """\
欢迎使用“企业股权穿透与控制权”司法审计系统，工作规程如下：

系统抓取了一个包含 {n} 个企业法人的控制权网络树（连通、无环，每个法人最多受一个直接母公司控股，顶层实控企业无母公司）。法人编号为：{node_list}。

系统定义了一个隐藏的控制规模函数 f，反映了法人 X 直接或间接控制的企业实体总数（包含其自身）。你的目标是通过调证查询推断股权穿透规律，并在测试阶段准确预测指定法人的实际控制规模。

你可以使用以下指令来摸排股权架构和控制规模（每种指令有配额限制）：

1. **规模查询**（配额 {quota_val} 次）：查询法人 X 的控制规模数值
2. **子公司查询**（配额 {quota_children} 次）：查询法人 X 的直接控股子公司
3. **股权穿透判断**（配额 {quota_ancestor} 次）：判断法人 X 是否为法人 Y 的严格上层（间接或直接）控股母公司（X=Y 时返回"否"）
4. **母公司查询**（配额 {quota_parent} 次）：查询法人 X 的直接母公司

系统会指定 {test_count} 个审查目标法人。在此阶段：
- **禁止**使用规模查询
- 允许继续使用架构查询（子公司、股权穿透、母公司查询），但总计不超过 {test_quota} 次
- 你需要一次性提交这些审查目标法人的控制规模预测

每次只能提交一个查询。格式如下：

- 规模查询（例如查询法人 5）：
<query_val>5</query_val>

- 子公司查询（例如查询法人 3 的直接子公司）：
<query_children>3</query_children>

- 股权穿透判断（例如判断 2 是否为 7 的上层母公司）：
<query_ancestor>2,7</query_ancestor>

- 母公司查询（例如查询法人 4 的直接母公司）：
<query_parent>4</query_parent>

- 进入测试阶段（当你准备好进入测试阶段时）：
<enter_test></enter_test>

- 提交最终预测（测试阶段，格式为"法人=值"，用逗号分隔）：
<answer>1=5,3=8,7=2</answer>

- 勘探阶段的指令配额用完后会自动进入测试阶段
- 测试阶段禁止规模查询，架构查询总数不能超过配额
- 预测结果必须包含所有审查目标法人，且数值必须完全正确
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Corporate Equity Penetration and Control" judicial audit system. The operational protocol is as follows:

The system has scraped a control network tree comprising {n} corporate entities (connected, acyclic, each entity has at most one direct parent holding company, the ultimate holding company has none). Entity IDs are: {node_list}.

There is a hidden control scale function f that reflects the total number of corporate entities directly or indirectly controlled by Entity X (including itself). Your goal is to infer the equity penetration structure through evidentiary queries and accurately predict the actual control scale for specified entities in the test phase.

You can use the following queries to investigate the equity architecture and control scales (each query type has a quota):

1. **Scale Query** (quota: {quota_val} times): Query the control scale value of Entity X
2. **Subsidiary Query** (quota: {quota_children} times): Query all direct subsidiaries of Entity X
3. **Equity Penetration Query** (quota: {quota_ancestor} times): Check if Entity X is a strict upstream (direct or indirect) holding company of Entity Y (returns "No" when X=Y)
4. **Parent Company Query** (quota: {quota_parent} times): Query the direct parent company of Entity X

The system will specify {test_count} target entities for review. In this phase:
- Scale queries are **forbidden**
- Architecture queries (subsidiary, equity penetration, parent company) are allowed but total count cannot exceed {test_quota}
- You must submit predictions for all target entities at once

Only one query per turn. Format:

- Scale Query (e.g., query entity 5):
<query_val>5</query_val>

- Subsidiary Query (e.g., query subsidiaries of entity 3):
<query_children>3</query_children>

- Equity Penetration Query (e.g., check if 2 is a holding company of 7):
<query_ancestor>2,7</query_ancestor>

- Parent Company Query (e.g., query parent company of entity 4):
<query_parent>4</query_parent>

- Enter Test Phase (when ready for test phase):
<enter_test></enter_test>

- Submit Final Answer (in test phase, format "entity=value", comma-separated):
<answer>1=5,3=8,7=2</answer>

- Exploration phase ends automatically when quotas are exhausted
- Test phase forbids scale queries; architecture queries cannot exceed quota
- Answer must include all review target entities with exact values
"""

    tags = ["answer", "query_val", "query_children", "query_ancestor", "query_parent", "enter_test"]
    
    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "tree_edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (5, 9), (6, 10), (6, 11)],
                "quota_val": 6,
                "quota_children": 10,
                "quota_ancestor": 60,
                "quota_parent": 6,
                "test_count": 5,
                "test_quota": 20,
                "test_nodes": [3, 5, 2, 7, 11],
            },
            2: {
                "n": 15,
                "tree_edges": [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (8, 14)],
                "quota_val": 5,
                "quota_children": 9,
                "quota_ancestor": 50,
                "quota_parent": 5,
                "test_count": 5,
                "test_quota": 18,
                "test_nodes": [1, 6, 8, 10, 14],
            },
            3: {
                "n": 18,
                "tree_edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (5, 10), (5, 11), (6, 12), (7, 13), (8, 14), (9, 15), (11, 16), (12, 17)],
                "quota_val": 5,
                "quota_children": 8,
                "quota_ancestor": 45,
                "quota_parent": 5,
                "test_count": 5,
                "test_quota": 16,
                "test_nodes": [2, 7, 9, 12, 16],
            },
            4: {
                "n": 22,
                "tree_edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (6, 12), (6, 13), (7, 14), (8, 15), (9, 16), (10, 17), (11, 18), (13, 19), (14, 20), (15, 21)],
                "quota_val": 4,
                "quota_children": 7,
                "quota_ancestor": 40,
                "quota_parent": 4,
                "test_count": 5,
                "test_quota": 15,
                "test_nodes": [1, 5, 11, 14, 19],
            },
            5: {
                "n": 25,
                "tree_edges": [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (3, 8), (3, 9), (4, 10), (4, 11), (5, 12), (6, 13), (7, 14), (7, 15), (8, 16), (9, 17), (9, 18), (10, 19), (11, 20), (13, 21), (14, 22), (16, 23), (18, 24)],
                "quota_val": 4,
                "quota_children": 6,
                "quota_ancestor": 35,
                "quota_parent": 4,
                "test_count": 5,
                "test_quota": 12,
                "test_nodes": [3, 7, 10, 17, 21],
            },
        },
        "en": {
            1: {
                "n": 12,
                "tree_edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (4, 8), (5, 9), (6, 10), (6, 11)],
                "quota_val": 6,
                "quota_children": 10,
                "quota_ancestor": 60,
                "quota_parent": 6,
                "test_count": 5,
                "test_quota": 20,
                "test_nodes": [3, 5, 2, 7, 11],
            },
            2: {
                "n": 15,
                "tree_edges": [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (3, 8), (4, 9), (5, 10), (6, 11), (7, 12), (8, 13), (8, 14)],
                "quota_val": 5,
                "quota_children": 9,
                "quota_ancestor": 50,
                "quota_parent": 5,
                "test_count": 5,
                "test_quota": 18,
                "test_nodes": [1, 6, 8, 10, 14],
            },
            3: {
                "n": 18,
                "tree_edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (5, 10), (5, 11), (6, 12), (7, 13), (8, 14), (9, 15), (11, 16), (12, 17)],
                "quota_val": 5,
                "quota_children": 8,
                "quota_ancestor": 45,
                "quota_parent": 5,
                "test_count": 5,
                "test_quota": 16,
                "test_nodes": [2, 7, 9, 12, 16],
            },
            4: {
                "n": 22,
                "tree_edges": [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6), (3, 7), (3, 8), (4, 9), (4, 10), (5, 11), (6, 12), (6, 13), (7, 14), (8, 15), (9, 16), (10, 17), (11, 18), (13, 19), (14, 20), (15, 21)],
                "quota_val": 4,
                "quota_children": 7,
                "quota_ancestor": 40,
                "quota_parent": 4,
                "test_count": 5,
                "test_quota": 15,
                "test_nodes": [1, 5, 11, 14, 19],
            },
            5: {
                "n": 25,
                "tree_edges": [(0, 1), (0, 2), (0, 3), (1, 4), (1, 5), (2, 6), (2, 7), (3, 8), (3, 9), (4, 10), (4, 11), (5, 12), (6, 13), (7, 14), (7, 15), (8, 16), (9, 17), (9, 18), (10, 19), (11, 20), (13, 21), (14, 22), (16, 23), (18, 24)],
                "quota_val": 4,
                "quota_children": 6,
                "quota_ancestor": 35,
                "quota_parent": 4,
                "test_count": 5,
                "test_quota": 12,
                "test_nodes": [3, 7, 10, 17, 21],
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
        
        self.n = cfg["n"]
        self._game_info["n"] = self.n
        self._game_info["node_list"] = ", ".join(str(i) for i in range(self.n))
        self._game_info["quota_val"] = cfg["quota_val"]
        self._game_info["quota_children"] = cfg["quota_children"]
        self._game_info["quota_ancestor"] = cfg["quota_ancestor"]
        self._game_info["quota_parent"] = cfg["quota_parent"]
        self._game_info["test_count"] = cfg["test_count"]
        self._game_info["test_quota"] = cfg["test_quota"]
        
        self.tree_edges = cfg["tree_edges"]
        self.children = {i: [] for i in range(self.n)}
        self.parent = {i: None for i in range(self.n)}
        
        for p, c in self.tree_edges:
            self.children[p].append(c)
            self.parent[c] = p
        
        self.root = None
        for i in range(self.n):
            if self.parent[i] is None:
                self.root = i
                break
        
        self.function_values = self._compute_subtree_sizes()
        
        self.test_nodes = cfg["test_nodes"]
        self.test_mode = False
        
        self.query_counts = {
            "val": 0,
            "children": 0,
            "ancestor": 0,
            "parent": 0,
            "test_structure": 0,
        }
        
        self.queried_val_nodes = set()

    def _compute_subtree_sizes(self):
        sizes = {}
        
        def dfs(node):
            size = 1
            for child in self.children[node]:
                size += dfs(child)
            sizes[node] = size
            return size
        
        dfs(self.root)
        return sizes

    def _is_ancestor(self, ancestor, descendant):
        if ancestor == descendant:
            return False
        
        current = self.parent[descendant]
        while current is not None:
            if current == ancestor:
                return True
            current = self.parent[current]
        return False

    def _check_quotas(self):
        if self.test_mode:
            return
        
        if (self.query_counts["val"] >= self._game_info["quota_val"] and
            self.query_counts["children"] >= self._game_info["quota_children"] and
            self.query_counts["ancestor"] >= self._game_info["quota_ancestor"] and
            self.query_counts["parent"] >= self._game_info["quota_parent"]):
            self.test_mode = True
            if self.config.language == "zh":
                return "探索阶段配额已用完，自动进入测试阶段。"
            else:
                return "Exploration quotas exhausted, automatically entering test phase."
        return None

    def evaluate(self, parsed_info):
        if not self.test_mode:
            return False
        
        raw_ans = parsed_info["answer"]
        try:
            pairs = [x.strip() for x in raw_ans.split(",")]
            predictions = {}
            for pair in pairs:
                if "=" not in pair:
                    return False
                node_str, val_str = pair.split("=", 1)
                node = int(node_str.strip())
                value = int(val_str.strip())
                predictions[node] = value
        except:
            return False
        
        if set(predictions.keys()) != set(self.test_nodes):
            return False
        
        for node in self.test_nodes:
            if predictions[node] != self.function_values[node]:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        
        if "enter_test" in parsed_info:
            if self.test_mode:
                return "已经在测试阶段。" if lang == "zh" else "Already in test phase."
            self.test_mode = True
            test_nodes_str = ", ".join(str(n) for n in self.test_nodes)
            if lang == "zh":
                return f"进入测试阶段。测试目标结点：{test_nodes_str}。请使用结构查询（总计不超过 {self._game_info['test_quota']} 次）后提交答案。"
            else:
                return f"Entering test phase. Test target nodes: {test_nodes_str}. Use structure queries (max {self._game_info['test_quota']} total) then submit answer."
        
        if "query_val" in parsed_info:
            if self.test_mode:
                return "测试阶段禁止取值查询。" if lang == "zh" else "Value queries forbidden in test phase."
            
            if self.query_counts["val"] >= self._game_info["quota_val"]:
                msg = "取值查询配额已用完。" if lang == "zh" else "Value query quota exhausted."
                auto_enter = self._check_quotas()
                return msg if auto_enter is None else f"{msg}\n{auto_enter}"
            
            try:
                node = int(parsed_info["query_val"].strip())
                if node < 0 or node >= self.n:
                    return "结点编号超出范围。" if lang == "zh" else "Node ID out of range."
                
                self.query_counts["val"] += 1
                self.queried_val_nodes.add(node)
                result = str(self.function_values[node])
                
                auto_enter = self._check_quotas()
                return result if auto_enter is None else f"{result}\n{auto_enter}"
            except:
                return "查询格式错误。" if lang == "zh" else "Invalid query format."
        
        if "query_children" in parsed_info:
            quota_key = "test_structure" if self.test_mode else "children"
            max_quota = self._game_info["test_quota"] if self.test_mode else self._game_info["quota_children"]
            
            if self.query_counts[quota_key] >= max_quota:
                msg = "子结点查询配额已用完。" if lang == "zh" else "Children query quota exhausted."
                if not self.test_mode:
                    auto_enter = self._check_quotas()
                    return msg if auto_enter is None else f"{msg}\n{auto_enter}"
                return msg
            
            try:
                node = int(parsed_info["query_children"].strip())
                if node < 0 or node >= self.n:
                    return "结点编号超出范围。" if lang == "zh" else "Node ID out of range."
                
                self.query_counts[quota_key] += 1
                children_list = self.children[node]
                if not children_list:
                    result = "无" if lang == "zh" else "None"
                else:
                    result = ", ".join(str(c) for c in children_list)
                
                if not self.test_mode:
                    auto_enter = self._check_quotas()
                    return result if auto_enter is None else f"{result}\n{auto_enter}"
                return result
            except:
                return "查询格式错误。" if lang == "zh" else "Invalid query format."
        
        if "query_ancestor" in parsed_info:
            quota_key = "test_structure" if self.test_mode else "ancestor"
            max_quota = self._game_info["test_quota"] if self.test_mode else self._game_info["quota_ancestor"]
            
            if self.query_counts[quota_key] >= max_quota:
                msg = "祖先关系查询配额已用完。" if lang == "zh" else "Ancestor query quota exhausted."
                if not self.test_mode:
                    auto_enter = self._check_quotas()
                    return msg if auto_enter is None else f"{msg}\n{auto_enter}"
                return msg
            
            try:
                parts = [x.strip() for x in parsed_info["query_ancestor"].split(",")]
                if len(parts) != 2:
                    return "查询格式错误。" if lang == "zh" else "Invalid query format."
                
                ancestor = int(parts[0])
                descendant = int(parts[1])
                
                if ancestor < 0 or ancestor >= self.n or descendant < 0 or descendant >= self.n:
                    return "结点编号超出范围。" if lang == "zh" else "Node ID out of range."
                
                self.query_counts[quota_key] += 1
                is_anc = self._is_ancestor(ancestor, descendant)
                result = "是" if is_anc else "否" if lang == "zh" else "Yes" if is_anc else "No"
                
                if not self.test_mode:
                    auto_enter = self._check_quotas()
                    return result if auto_enter is None else f"{result}\n{auto_enter}"
                return result
            except:
                return "查询格式错误。" if lang == "zh" else "Invalid query format."
        
        if "query_parent" in parsed_info:
            quota_key = "test_structure" if self.test_mode else "parent"
            max_quota = self._game_info["test_quota"] if self.test_mode else self._game_info["quota_parent"]
            
            if self.query_counts[quota_key] >= max_quota:
                msg = "父结点查询配额已用完。" if lang == "zh" else "Parent query quota exhausted."
                if not self.test_mode:
                    auto_enter = self._check_quotas()
                    return msg if auto_enter is None else f"{msg}\n{auto_enter}"
                return msg
            
            try:
                node = int(parsed_info["query_parent"].strip())
                if node < 0 or node >= self.n:
                    return "结点编号超出范围。" if lang == "zh" else "Node ID out of range."
                
                self.query_counts[quota_key] += 1
                parent = self.parent[node]
                if parent is None:
                    result = "无" if lang == "zh" else "None"
                else:
                    result = str(parent)
                
                if not self.test_mode:
                    auto_enter = self._check_quotas()
                    return result if auto_enter is None else f"{result}\n{auto_enter}"
                return result
            except:
                return "查询格式错误。" if lang == "zh" else "Invalid query format."
        
        return "无效的查询类型。" if lang == "zh" else "Invalid query type."

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_correct == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        lang = self.config.language
        
        for node in range(self.n):
            queries.append({
                "query": f"<query_val>{node}</query_val>",
                "answer": str(self.function_values[node])
            })
        
        for node in range(self.n):
            children = self.children[node]
            if not children:
                ans = "无" if lang == "zh" else "None"
            else:
                ans = ", ".join(str(c) for c in children)
            queries.append({
                "query": f"<query_children>{node}</query_children>",
                "answer": ans
            })

        for node in range(self.n):
            p = self.parent[node]
            if p is None:
                ans = "无" if lang == "zh" else "None"
            else:
                ans = str(p)
            queries.append({
                "query": f"<query_parent>{node}</query_parent>",
                "answer": ans
            })
        
        for u in range(self.n):
            for v in range(self.n):
                is_anc = self._is_ancestor(u, v)
                if lang == "zh":
                    ans = "是" if is_anc else "否"
                else:
                    ans = "Yes" if is_anc else "No"
                queries.append({
                    "query": f"<query_ancestor>{u},{v}</query_ancestor>",
                    "answer": ans
                })
                
        return queries
