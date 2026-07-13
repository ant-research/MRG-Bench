# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   子树规模：以某节点为根的子树共有多少个节点
# ============================================================

from .base import Game
import re
import random


class TreeFunctionInferenceGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "树"

    game_rule_zh = """\
我们现在来玩一个"树结构函数推理"游戏，规则如下：

游戏设定了一棵有根树，包含 {n} 个节点（编号 1 到 {n}），节点 1 是根节点。树的完整结构如下：
{tree_structure}

对于任意节点 v，定义 size(v) 为以 v 为根的子树的节点总数（包含 v 自己）。

系统隐藏了一个确定的函数 f，对每个节点 v 会返回一个非负整数 S(v)。这个函数在整个游戏过程中保持不变，且仅依赖于与该节点相关的子树规模信息（例如该节点自己的子树规模、其父节点或子节点的子树规模、这些规模之间的比较、求和、求差、奇偶性等简单运算），不会使用节点编号、位置等其他信息。

你的目标是通过询问推断出函数 f 的规则，并对至少 {k} 个未直接询问过数值的节点给出正确的 S(v) 预测。

你可以进行以下类型的询问：

1. 数值询问：询问某个节点的响应值 S(v)
2. 比较询问：比较两个节点的响应值大小关系（返回格式为 "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)"）
3. 规模核对：询问某个节点的子树规模 size(v)（本局最多可使用 {r} 次）

当你收集足够信息后，请提交最终答案，包括：
- 函数 f 的明确规则描述
- 至少 {k} 个未进行过数值询问的节点及其 S(v) 预测值

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 数值询问（例如询问节点 3）：
<query_value>3</query_value>

- 比较询问（例如比较节点 2 和 5）：
<query_compare>2,5</query_compare>

- 规模核对（例如询问节点 4 的子树规模）：
<query_size>4</query_size>

提交最终答案时，必须包含函数规则描述和至少 {k} 个未采样节点的预测，格式如下：

<answer>
rule: [你推断的函数规则描述]
predictions: 2=3, 5=1, 7=0, ...
</answer>

注意：predictions 中的节点必须是你没有进行过数值询问的节点，且至少包含 {k} 个节点。
"""

    game_rule_en = """\
Let's play a "Tree Function Inference" game. Here are the rules:

The game involves a rooted tree with {n} nodes (numbered 1 to {n}), where node 1 is the root. The complete tree structure is as follows:
{tree_structure}

For any node v, define size(v) as the total number of nodes in the subtree rooted at v (including v itself).

The system has a hidden deterministic function f that returns a non-negative integer S(v) for each node v. This function remains constant throughout the game and depends only on subtree size information related to the node (such as its own subtree size, subtree sizes of its parent or children, comparisons between these sizes, sums, differences, parity, and other simple operations), without using node identifiers, positions, or other information.

Your goal is to infer the rule of function f through queries and provide correct S(v) predictions for at least {k} nodes that you have not directly queried for their values.

You can perform the following types of queries:

1. Value Query: Ask for the response value S(v) of a node
2. Comparison Query: Compare the response values of two nodes (returns "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)")
3. Size Check: Ask for the subtree size size(v) of a node (maximum {r} uses per game)

When you have collected enough information, submit your final answer including:
- A clear description of the rule for function f
- At least {k} nodes that you have not performed value queries on, along with their predicted S(v) values

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying node 3):
<query_value>3</query_value>

- Comparison Query (e.g., comparing nodes 2 and 5):
<query_compare>2,5</query_compare>

- Size Check (e.g., asking for subtree size of node 4):
<query_size>4</query_size>

When submitting the final answer, you must include the function rule description and predictions for at least {k} unsampled nodes in this format:

<answer>
rule: [your inferred function rule description]
predictions: 2=3, 5=1, 7=0, ...
</answer>

Note: The nodes in predictions must be nodes you have not performed value queries on, and there must be at least {k} nodes.
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎使用"交通路网层级调度分析"系统，规则如下：

系统导入了一个包含 {n} 个站点的树状层级交通网络（编号 1 到 {n}），其中站点 1 是总枢纽中心。完整路网结构如下：
{tree_structure}

对于任意站点 v，其"辖区规模" size(v) 定义为以 v 为层级根节点的子网中的站点总数（包含 v 自身）。

交通调度中心设定了一个隐藏的调度指数评级函数 f，每个站点 v 都会被赋予一个确定的非负整数评级 S(v)。该评估规则在全网范围内保持一致，且仅依赖于该站点相关的辖区规模信息（例如自身辖区规模、上下游节点辖区规模的大小比较、求和、差值、奇偶性等简单指标），不依赖站点编号或其他地理属性。

你的任务是通过系统指令推断出调度指数的评估规则 f，并为至少 {k} 个未直接查询的站点预测正确的 S(v) 值。

你可以发送以下类型的调度查询指令：

1. 数值询问：查询某站点的调度指数 S(v)
2. 比较询问：比对两个站点的调度指数大小关系（返回格式为 "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)"）
3. 规模核对：查询某站点的辖区规模 size(v)（本局限用 {r} 次）

当你收集到足够的情报后，请提交最终报告，包括：
- 调度指数评估规则 f 的明确描述
- 至少 {k} 个未进行数值询问的站点及其 S(v) 预测值

## 指令与提交报告的格式（必须严格遵守）

每次指令只能包含一个标签。请使用以下 XML 格式：

- 数值询问（例如查询站点 3）：
<query_value>3</query_value>

- 比较询问（例如比对站点 2 和 5）：
<query_compare>2,5</query_compare>

- 规模核对（例如查询站点 4 的辖区规模）：
<query_size>4</query_size>

提交最终报告时，必须包含规则描述和至少 {k} 个未采样站点的预测，格式如下：

<answer>
rule: [你推断的评估规则描述]
predictions: 2=3, 5=1, 7=0, ...
</answer>

注意：predictions 中的站点必须是你没有进行过数值询问的节点，且至少包含 {k} 个站点。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Traffic Network Hierarchical Dispatch Analysis" system. The operational rules are as follows:

The system has mapped a hierarchical traffic network comprising {n} stations (numbered 1 to {n}), where station 1 serves as the central hub. The complete network topology is:
{tree_structure}

For any station v, its "jurisdiction size" size(v) is defined as the total number of stations within the subnet rooted at v (including v itself).

The dispatch center utilizes a hidden deterministic dispatch index function f, assigning a non-negative integer rating S(v) to each station v. This evaluation mechanism remains constant across the network and relies solely on jurisdiction size metrics related to the station (e.g., its own jurisdiction size, jurisdiction sizes of upstream/downstream stations, comparisons, sums, parity, etc.), completely ignoring station IDs or geographical attributes.

Your objective is to deduce the dispatch index evaluation rule f through system queries and provide accurate S(v) predictions for at least {k} unqueried stations.

You may issue the following types of dispatch queries:

1. Value Query: Request the dispatch index S(v) of a specific station
2. Comparison Query: Compare the dispatch indices of two stations (returns "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)")
3. Size Check: Request the jurisdiction size size(v) of a station (maximum {r} uses per session)

Upon gathering sufficient intelligence, submit your final report including:
- A clear description of the dispatch index evaluation rule f
- Predicted S(v) values for at least {k} stations that have not been directly queried

## Query and Report Submission Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Value Query (e.g., querying station 3):
<query_value>3</query_value>

- Comparison Query (e.g., comparing stations 2 and 5):
<query_compare>2,5</query_compare>

- Size Check (e.g., requesting jurisdiction size of station 4):
<query_size>4</query_size>

When submitting the final report, you must include the rule description and predictions for at least {k} unsampled stations in this format:

<answer>
rule: [your deduced evaluation rule description]
predictions: 2=3, 5=1, 7=0, ...
</answer>

Note: The stations in predictions must be ones you have not performed value queries on, and there must be at least {k} stations.
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎使用"医疗分级诊疗网络分配"系统，规则如下：

系统接入了一个包含 {n} 个医疗机构节点的树状转诊网络（编号 1 到 {n}），其中节点 1 是区域总院。分级诊疗网络完整架构如下：
{tree_structure}

对于任意医疗机构 v，其"下属网络规模" size(v) 定义为以 v 为层级起点的分支诊疗网中的机构总数（包含 v 自身）。

卫健委设定了一个隐藏的资源调配优先级函数 f，每个机构 v 都会被赋予一个确定的非负整数优先级指数 S(v)。该调配规则在全系统保持不变，且仅依赖于该机构相关的下属网络规模信息（例如自身网络规模、上下级机构网络规模的差值、总和、奇偶性等常规考核指标），不参考机构的具体编号或行政区划。

你的任务是通过系统核查推断出资源优先级的分配规则 f，并为至少 {k} 个未直接查询的机构预测正确的 S(v) 指数。

你可以执行以下类型的系统核查：

1. 数值询问：查询某医疗机构的优先级指数 S(v)
2. 比较询问：比对两家医疗机构的优先级大小关系（返回格式为 "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)"）
3. 规模核对：查询某医疗机构的下属网络规模 size(v)（本局限用 {r} 次）

当你掌握分配逻辑后，请提交最终评估报告，包括：
- 优先级分配规则 f 的明确描述
- 至少 {k} 个未进行数值询问的机构及其 S(v) 预测值

## 核查与提交报告的格式（必须严格遵守）

每次核查只能包含一个标签。请使用以下 XML 格式：

- 数值询问（例如查询机构 3）：
<query_value>3</query_value>

- 比较询问（例如比对机构 2 和 5）：
<query_compare>2,5</query_compare>

- 规模核对（例如查询机构 4 的下属网络规模）：
<query_size>4</query_size>

提交最终报告时，必须包含规则描述和至少 {k} 个未采样机构的预测，格式如下：

<answer>
rule: [你推断的资源分配规则描述]
predictions: 2=3, 5=1, 7=0, ...
</answer>

注意：predictions 中的机构必须是你没有进行过数值询问的节点，且至少包含 {k} 个机构。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Hierarchical Medical Referral Network Allocation" system. The operational rules are as follows:

The system has integrated a hierarchical referral network containing {n} medical institution nodes (numbered 1 to {n}), where node 1 is the regional general hospital. The complete network architecture is as follows:
{tree_structure}

For any medical institution v, its "subordinate network size" size(v) is defined as the total number of institutions within the branch referral network originating from v (including v itself).

The health commission has configured a hidden deterministic resource allocation priority function f, where each institution v is assigned a non-negative integer priority index S(v). This allocation mechanism remains constant throughout the system and relies solely on subordinate network size metrics related to the institution (e.g., its own network size, differences/sums/parity of network sizes of superior or subordinate institutions, and other routine assessment indicators), without referencing specific institution IDs or administrative divisions.

Your task is to deduce the resource priority allocation rule f through system audits and provide accurate S(v) index predictions for at least {k} institutions that you have not directly queried.

You can execute the following types of system audits:

1. Value Query: Request the priority index S(v) of a specific medical institution
2. Comparison Query: Compare the priority indices of two medical institutions (returns "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)")
3. Size Check: Request the subordinate network size size(v) of an institution (maximum {r} uses per session)

When you have grasped the allocation logic, please submit your final evaluation report, including:
- A clear description of the priority allocation rule f
- Predicted S(v) values for at least {k} institutions that have not undergone a value query

## Audit and Report Submission Format (strictly required)

Each audit must contain only one tag. Please use the following XML format:

- Value Query (e.g., querying institution 3):
<query_value>3</query_value>

- Comparison Query (e.g., comparing institutions 2 and 5):
<query_compare>2,5</query_compare>

- Size Check (e.g., requesting the subordinate network size of institution 4):
<query_size>4</query_size>

When submitting the final report, you must include the rule description and predictions for at least {k} unsampled institutions, formatted as follows:

<answer>
rule: [your deduced resource allocation rule description]
predictions: 2=3, 5=1, 7=0, ...
</answer>

Note: The institutions in predictions must be nodes you have not performed value queries on, and there must be at least {k} institutions.
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎使用"教育资源定向倾斜分配"系统，规则如下：

系统导入了一个包含 {n} 个教学节点的树状教育管理体系（编号 1 到 {n}），其中节点 1 是市级教委。完整管理层级结构如下：
{tree_structure}

对于任意教学节点 v，其"管辖学区规模" size(v) 定义为以 v 为顶层节点的分支教育网中的节点总数（包含 v 自身）。

教育局设定了一个隐藏的确定性教育资源倾斜函数 f，每个教学节点 v 都会被赋予一个非负整数权重指数 S(v)。该评估规则在全辖区内保持不变，且仅依赖于该节点相关的学区规模信息（例如自身学区规模、上下级节点学区规模的比较、求和、差值、奇偶性等），不依赖节点编号或地理位置。

你的任务是通过系统调研推断出资源权重的评估规则 f，并为至少 {k} 个未直接查询的教学节点预测正确的 S(v) 值。

你可以发送以下类型的调研指令：

1. 数值询问：查询某教学节点的权重指数 S(v)
2. 比较询问：比对两个教学节点的权重指数大小关系（返回格式为 "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)"）
3. 规模核对：查询某教学节点的管辖学区规模 size(v)（本局限用 {r} 次）

当你收集到足够的信息后，请提交最终报告，包括：
- 资源权重评估规则 f 的明确描述
- 至少 {k} 个未进行数值询问的节点及其 S(v) 预测值

## 调研与提交报告的格式（必须严格遵守）

每次调研只能包含一个标签。请使用以下 XML 格式：

- 数值询问（例如查询节点 3）：
<query_value>3</query_value>

- 比较询问（例如比对节点 2 和 5）：
<query_compare>2,5</query_compare>

- 规模核对（例如查询节点 4 的管辖学区规模）：
<query_size>4</query_size>

提交最终报告时，必须包含规则描述和至少 {k} 个未采样节点的预测，格式如下：

<answer>
rule: [你推断的资源权重评估规则描述]
predictions: 2=3, 5=1, 7=0, ...
</answer>

注意：predictions 中的节点必须是你没有进行过数值询问的节点，且至少包含 {k} 个节点。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Targeted Educational Resource Allocation" system. The operational rules are as follows:

The system has imported a hierarchical educational management framework comprising {n} teaching nodes (numbered 1 to {n}), where node 1 is the municipal education commission. The complete management hierarchy is as follows:
{tree_structure}

For any teaching node v, its "jurisdictional district size" size(v) is defined as the total number of nodes within the branch educational network topped by v (including v itself).

The education bureau employs a hidden deterministic resource weighting function f, assigning a non-negative integer weight index S(v) to each teaching node v. This evaluation mechanism remains constant across the district and relies solely on district size metrics related to the node (e.g., its own district size, comparisons/sums/differences/parity of district sizes of superior/subordinate nodes), ignoring node IDs or geographical locations.

Your objective is to deduce the resource weighting evaluation rule f through system investigations and provide accurate S(v) predictions for at least {k} teaching nodes that you have not directly queried.

You can issue the following types of investigation commands:

1. Value Query: Request the weight index S(v) of a specific teaching node
2. Comparison Query: Compare the weight indices of two teaching nodes (returns "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)")
3. Size Check: Request the jurisdictional district size size(v) of a teaching node (maximum {r} uses per session)

Upon gathering sufficient information, please submit your final report, including:
- A clear description of the resource weighting evaluation rule f
- Predicted S(v) values for at least {k} teaching nodes that have not undergone a value query

## Investigation and Report Submission Format (strictly required)

Each investigation command must contain only one tag. Please use the following XML format:

- Value Query (e.g., querying node 3):
<query_value>3</query_value>

- Comparison Query (e.g., comparing nodes 2 and 5):
<query_compare>2,5</query_compare>

- Size Check (e.g., requesting the jurisdictional district size of node 4):
<query_size>4</query_size>

When submitting the final report, you must include the rule description and predictions for at least {k} unsampled nodes, formatted as follows:

<answer>
rule: [your deduced resource weighting evaluation rule description]
predictions: 2=3, 5=1, 7=0, ...
</answer>

Note: The nodes in predictions must be nodes you have not performed value queries on, and there must be at least {k} nodes.
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎使用"工业供应链产能评估"系统，规则如下：

系统构建了一个包含 {n} 个生产节点的树状供应链体系（编号 1 到 {n}），其中节点 1 是总装工厂。完整供应链结构如下：
{tree_structure}

对于任意生产节点 v，其"供应链分支规模" size(v) 定义为以 v 为链条起点的分支网络中的节点总数（包含 v 自身）。

生产指挥部设定了一个隐藏的产能保障定级函数 f，每个生产节点 v 都会被赋予一个确定的非负整数评级 S(v)。该定级规则在全供应链中保持不变，且仅依赖于该节点相关的分支规模信息（例如自身分支规模、上下游节点分支规模的大小比较、求和、差值、奇偶性等简单运算），不使用节点编号或其他工厂属性。

你的任务是通过系统检测推断出产能定级规则 f，并为至少 {k} 个未直接查询的生产节点预测正确的 S(v) 值。

你可以进行以下类型的检测指令：

1. 数值询问：查询某生产节点的产能评级 S(v)
2. 比较询问：比对两个生产节点的评级大小关系（返回格式为 "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)"）
3. 规模核对：查询某生产节点的供应链分支规模 size(v)（本局限用 {r} 次）

当你收集到足够数据后，请提交最终报告，包括：
- 产能保障定级规则 f 的明确描述
- 至少 {k} 个未进行数值询问的节点及其 S(v) 预测值

## 检测与提交报告的格式（必须严格遵守）

每次检测只能包含一个标签。请使用以下 XML 格式：

- 数值询问（例如查询生产节点 3）：
<query_value>3</query_value>

- 比较询问（例如比对生产节点 2 和 5）：
<query_compare>2,5</query_compare>

- 规模核对（例如查询生产节点 4 的供应链分支规模）：
<query_size>4</query_size>

提交最终报告时，必须包含规则描述和至少 {k} 个未采样节点的预测，格式如下：

<answer>
rule: [你推断的产能保障定级规则描述]
predictions: 2=3, 5=1, 7=0, ...
</answer>

注意：predictions 中的节点必须是你没有进行过数值询问的节点，且至少包含 {k} 个节点。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the "Industrial Supply Chain Capacity Assessment" system. The operational rules are as follows:

The system has mapped out a hierarchical supply chain framework comprising {n} production nodes (numbered 1 to {n}), where node 1 is the final assembly plant. The complete supply chain structure is as follows:
{tree_structure}

For any production node v, its "supply chain branch size" size(v) is defined as the total number of nodes within the branch network originating from v (including v itself).

The production command center utilizes a hidden deterministic capacity assurance rating function f, assigning a non-negative integer rating S(v) to each production node v. This rating mechanism remains constant across the entire supply chain and relies solely on branch size metrics related to the node (e.g., its own branch size, comparisons/sums/differences/parity of branch sizes of upstream/downstream nodes), completely ignoring node IDs or other factory attributes.

Your objective is to deduce the capacity rating rule f through system inspections and provide accurate S(v) predictions for at least {k} production nodes that you have not directly queried.

You can issue the following types of inspection commands:

1. Value Query: Request the capacity rating S(v) of a specific production node
2. Comparison Query: Compare the capacity ratings of two production nodes (returns "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)")
3. Size Check: Request the supply chain branch size size(v) of a production node (maximum {r} uses per session)

Upon gathering sufficient data, please submit your final report, including:
- A clear description of the capacity assurance rating rule f
- Predicted S(v) values for at least {k} production nodes that have not undergone a value query

## Inspection and Report Submission Format (strictly required)

Each inspection command must contain only one tag. Please use the following XML format:

- Value Query (e.g., querying production node 3):
<query_value>3</query_value>

- Comparison Query (e.g., comparing production nodes 2 and 5):
<query_compare>2,5</query_compare>

- Size Check (e.g., requesting the supply chain branch size of production node 4):
<query_size>4</query_size>

When submitting the final report, you must include the rule description and predictions for at least {k} unsampled nodes, formatted as follows:

<answer>
rule: [your deduced capacity assurance rating rule description]
predictions: 2=3, 5=1, 7=0, ...
</answer>

Note: The nodes in predictions must be nodes you have not performed value queries on, and there must be at least {k} nodes.
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎使用"司法判例溯源分析"系统，规则如下：

系统梳理了一个包含 {n} 个案件卷宗节点的树状判例引用网络（编号 1 到 {n}），其中节点 1 是核心指导案例。完整引用网络结构如下：
{tree_structure}

对于任意案件卷宗 v，其"衍生引用规模" size(v) 定义为以 v 为溯源起点的分支引用网中的卷宗总数（包含 v 自身）。

司法信息库设定了一个隐藏的判例效力评估函数 f，每个案件卷宗 v 都会被赋予一个确定的非负整数司法效力指数 S(v)。该评估规则在整个网络中保持不变，且仅依赖于该卷宗相关的引用规模信息（例如自身衍生规模、前后序卷宗引用规模的比较、求和、差值、奇偶性等逻辑特征），不采纳卷宗编号或具体案由。

你的任务是通过系统调阅推断出效力评估规则 f，并为至少 {k} 个未直接调阅数值的卷宗预测正确的 S(v) 值。

你可以发出以下类型的调阅指令：

1. 数值询问：查询某案件卷宗的司法效力指数 S(v)
2. 比较询问：比对两个案件卷宗的效力指数大小关系（返回格式为 "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)"）
3. 规模核对：查询某案件卷宗的衍生引用规模 size(v)（本局限用 {r} 次）

当你完成逻辑推演后，请提交最终结论，包括：
- 效力评估规则 f 的明确描述
- 至少 {k} 个未进行数值询问的卷宗及其 S(v) 预测值

## 调阅与提交结论的格式（必须严格遵守）

每次调阅只能包含一个标签。请使用以下 XML 格式：

- 数值询问（例如查询卷宗 3）：
<query_value>3</query_value>

- 比较询问（例如比对卷宗 2 和 5）：
<query_compare>2,5</query_compare>

- 规模核对（例如查询卷宗 4 的衍生引用规模）：
<query_size>4</query_size>

提交最终结论时，必须包含规则描述和至少 {k} 个未采样卷宗的预测，格式如下：

<answer>
rule: [你推断的效力评估规则描述]
predictions: 2=3, 5=1, 7=0, ...
</answer>

注意：predictions 中的卷宗必须是你没有进行过数值询问的节点，且至少包含 {k} 个卷宗。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Judicial Precedent Traceability Analysis" system. The operational rules are as follows:

The system has structured a hierarchical precedent citation network containing {n} case file nodes (numbered 1 to {n}), where node 1 is the core guiding case. The complete citation network structure is as follows:
{tree_structure}

For any case file v, its "derivative citation size" size(v) is defined as the total number of files within the branch citation network originating from v as the tracing point (including v itself).

The judicial database has established a hidden deterministic precedent validity evaluation function f, assigning a non-negative integer judicial validity index S(v) to each case file v. This evaluation mechanism remains constant across the entire network and relies solely on citation size metrics related to the case file (e.g., its own derivative size, comparisons/sums/differences/parity of citation sizes of preceding/subsequent case files, and other logical features), without adopting file IDs or specific causes of action.

Your objective is to deduce the validity evaluation rule f through system retrieval commands and provide accurate S(v) predictions for at least {k} case files that you have not directly retrieved values for.

You may issue the following types of retrieval commands:

1. Value Query: Request the judicial validity index S(v) of a specific case file
2. Comparison Query: Compare the validity indices of two case files (returns "S(a) > S(b)" / "S(a) < S(b)" / "S(a) = S(b)")
3. Size Check: Request the derivative citation size size(v) of a case file (maximum {r} uses per session)

Upon completing your logical deduction, please submit your final conclusion, including:
- A clear description of the validity evaluation rule f
- Predicted S(v) values for at least {k} case files that have not undergone a value query

## Retrieval and Conclusion Submission Format (strictly required)

Each retrieval command must contain only one tag. Please use the following XML format:

- Value Query (e.g., querying case file 3):
<query_value>3</query_value>

- Comparison Query (e.g., comparing case files 2 and 5):
<query_compare>2,5</query_compare>

- Size Check (e.g., requesting the derivative citation size of case file 4):
<query_size>4</query_size>

When submitting the final conclusion, you must include the rule description and predictions for at least {k} unsampled case files, formatted as follows:

<answer>
rule: [your deduced validity evaluation rule description]
predictions: 2=3, 5=1, 7=0, ...
</answer>

Note: The case files in predictions must be nodes you have not performed value queries on, and there must be at least {k} case files.
"""


    tags = ["answer", "query_value", "query_compare", "query_size"]

    # 难度配置：
    # 1 (简单) - 小树，函数规则为 f(v) = size(v)
    # 2 (中等偏下) - 中等树，函数规则为 f(v) = size(v) 的奇偶性（0或1）
    # 3 (中等偏上) - 中等树，函数规则为 f(v) = 子节点数量
    # 4 (较难) - 较大树，函数规则为 f(v) = size(v) % 3
    # 5 (难) - 大树，函数规则为 f(v) = max(子节点的size) 如果有子节点，否则为 0

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "tree_edges": "1-2,1-3,2-4,2-5,3-6,3-7",  # 父子关系
                "rule_type": "size",
                "rule_desc": "f(v) 等于 size(v)（节点 v 的子树规模）",
                "k": 3,  # 需要预测的未采样节点数
                "r": 2,  # 规模核对次数限制
            },
            2: {
                "n": 10,
                "tree_edges": "1-2,1-3,1-4,2-5,2-6,3-7,4-8,4-9,4-10",
                "rule_type": "size_parity",
                "rule_desc": "f(v) 等于 size(v) 的奇偶性（偶数为0，奇数为1）",
                "k": 4,
                "r": 2,
            },
            3: {
                "n": 12,
                "tree_edges": "1-2,1-3,2-4,2-5,2-6,3-7,3-8,4-9,5-10,6-11,6-12",
                "rule_type": "children_count",
                "rule_desc": "f(v) 等于节点 v 的直接子节点数量",
                "k": 5,
                "r": 1,
            },
            4: {
                "n": 15,
                "tree_edges": "1-2,1-3,2-4,2-5,2-6,3-7,3-8,4-9,4-10,5-11,6-12,7-13,8-14,8-15",
                "rule_type": "size_mod3",
                "rule_desc": "f(v) 等于 size(v) 对 3 取模的结果",
                "k": 6,
                "r": 1,
            },
            5: {
                "n": 20,
                "tree_edges": "1-2,1-3,1-4,2-5,2-6,3-7,3-8,3-9,4-10,5-11,5-12,6-13,7-14,8-15,8-16,9-17,10-18,10-19,10-20",
                "rule_type": "max_child_size",
                "rule_desc": "f(v) 等于节点 v 的所有直接子节点中最大的子树规模，如果没有子节点则为 0",
                "k": 7,
                "r": 0,
            },
        },
        "en": {
            1: {
                "n": 7,
                "tree_edges": "1-2,1-3,2-4,2-5,3-6,3-7",
                "rule_type": "size",
                "rule_desc": "f(v) equals size(v) (the subtree size of node v)",
                "k": 3,
                "r": 2,
            },
            2: {
                "n": 10,
                "tree_edges": "1-2,1-3,1-4,2-5,2-6,3-7,4-8,4-9,4-10",
                "rule_type": "size_parity",
                "rule_desc": "f(v) equals the parity of size(v) (0 for even, 1 for odd)",
                "k": 4,
                "r": 2,
            },
            3: {
                "n": 12,
                "tree_edges": "1-2,1-3,2-4,2-5,2-6,3-7,3-8,4-9,5-10,6-11,6-12",
                "rule_type": "children_count",
                "rule_desc": "f(v) equals the number of direct children of node v",
                "k": 5,
                "r": 1,
            },
            4: {
                "n": 15,
                "tree_edges": "1-2,1-3,2-4,2-5,2-6,3-7,3-8,4-9,4-10,5-11,6-12,7-13,8-14,8-15",
                "rule_type": "size_mod3",
                "rule_desc": "f(v) equals size(v) modulo 3",
                "k": 6,
                "r": 1,
            },
            5: {
                "n": 20,
                "tree_edges": "1-2,1-3,1-4,2-5,2-6,3-7,3-8,3-9,4-10,5-11,5-12,6-13,7-14,8-15,8-16,9-17,10-18,10-19,10-20",
                "rule_type": "max_child_size",
                "rule_desc": "f(v) equals the maximum subtree size among all direct children of node v, or 0 if v has no children",
                "k": 7,
                "r": 0,
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
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]
        self._game_info["r"] = cfg["r"]

        # 构建树结构
        self.n = cfg["n"]
        self.children = {i: [] for i in range(1, self.n + 1)}  # 每个节点的子节点列表
        self.parent = {i: None for i in range(1, self.n + 1)}  # 每个节点的父节点
        
        # 解析边
        edges = cfg["tree_edges"].split(",")
        for edge in edges:
            parent_node, child_node = map(int, edge.split("-"))
            self.children[parent_node].append(child_node)
            self.parent[child_node] = parent_node

        # 计算每个节点的子树规模
        self.subtree_size = {}
        self._compute_subtree_size(1)

        # 设置函数规则
        self.rule_type = cfg["rule_type"]
        self.ground_truth_rule = cfg["rule_desc"]
        
        # 计算每个节点的真实函数值
        self.function_values = {}
        for v in range(1, self.n + 1):
            self.function_values[v] = self._compute_function_value(v)

        # 构建树结构的可读描述
        tree_desc = self._build_tree_description()
        self._game_info["tree_structure"] = tree_desc

        # 跟踪查询状态
        self.queried_values = set()  # 已经进行过数值询问的节点
        self.size_check_count = 0  # 规模核对使用次数
        self.max_size_checks = cfg["r"]
        self.min_predictions = cfg["k"]

    def _compute_subtree_size(self, v):
        """递归计算子树规模"""
        if v in self.subtree_size:
            return self.subtree_size[v]
        
        size = 1  # 节点自己
        for child in self.children[v]:
            size += self._compute_subtree_size(child)
        
        self.subtree_size[v] = size
        return size

    def _compute_function_value(self, v):
        """根据规则类型计算节点 v 的函数值"""
        if self.rule_type == "size":
            return self.subtree_size[v]
        elif self.rule_type == "size_parity":
            return self.subtree_size[v] % 2
        elif self.rule_type == "children_count":
            return len(self.children[v])
        elif self.rule_type == "size_mod3":
            return self.subtree_size[v] % 3
        elif self.rule_type == "max_child_size":
            if not self.children[v]:
                return 0
            return max(self.subtree_size[child] for child in self.children[v])
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def _build_tree_description(self):
        """构建树结构的可读描述"""
        lines = []
        if self.config.language == "zh":
            lines.append("节点 -> 子节点列表")
        else:
            lines.append("Node -> Children List")
        
        for v in range(1, self.n + 1):
            if self.children[v]:
                children_str = ", ".join(map(str, self.children[v]))
                lines.append(f"{v} -> [{children_str}]")
            else:
                if self.config.language == "zh":
                    lines.append(f"{v} -> [叶节点]")
                else:
                    lines.append(f"{v} -> [leaf]")
        
        return "\n".join(lines)

    def evaluate(self, parsed_info):
        """评估最终答案"""
        raw_ans = parsed_info["answer"]
        
        # 解析规则和预测
        try:
            # 提取 rule 和 predictions
            rule_match = re.search(r'rule:\s*(.+?)(?=predictions:|$)', raw_ans, re.IGNORECASE | re.DOTALL)
            pred_match = re.search(r'predictions:\s*(.+)', raw_ans, re.IGNORECASE | re.DOTALL)
            
            if not rule_match or not pred_match:
                return False
            
            rule_desc = rule_match.group(1).strip()
            pred_str = pred_match.group(1).strip()
            
            # 解析预测：格式为 "node=value, node=value, ..."
            predictions = {}
            pred_pairs = pred_str.split(",")
            for pair in pred_pairs:
                pair = pair.strip()
                if "=" not in pair:
                    continue
                node_str, value_str = pair.split("=", 1)
                node = int(node_str.strip())
                value = int(value_str.strip())
                predictions[node] = value
            
            # 检查1：预测的节点数量是否足够
            if len(predictions) < self.min_predictions:
                return False
            
            # 检查2：预测的节点是否都是未采样的
            for node in predictions:
                if node in self.queried_values:
                    return False
                if node < 1 or node > self.n:
                    return False
            
            # 检查3：预测的值是否全部正确
            for node, predicted_value in predictions.items():
                if self.function_values[node] != predicted_value:
                    return False
            
            # 检查4：随机抽查一些其他未采样节点（可选，这里抽查最多3个）
            unsampled_nodes = [v for v in range(1, self.n + 1) 
                             if v not in self.queried_values and v not in predictions]
            import random
            random.seed(42)  # 固定随机种子以确保可重复性
            check_nodes = random.sample(unsampled_nodes, min(3, len(unsampled_nodes)))
            
            # 这里我们需要用规则来验证，但由于规则是自然语言描述，
            # 实际上无法自动验证规则的正确性
            # 所以我们只能通过预测值的正确性来判断
            # 如果要求更严格，可以要求规则描述与ground_truth_rule相似
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的业务逻辑，提取自原 produce_response"""
        if self.config.language == "zh":
            error_range = "错误：节点编号超出范围。"
            error_quota = "错误：规模核对次数已用完。"
            error_format = "错误：查询格式无效。"
        else:
            error_range = "Error: Node ID out of range."
            error_quota = "Error: Size check quota exhausted."
            error_format = "Error: Invalid query format."

        # 优先级：value > compare > size
        if "query_value" in parsed_info:
            node_str = parsed_info["query_value"].strip()
            try:
                node = int(node_str)
                if node < 1 or node > self.n:
                    return error_range
                # 记录已查询的节点
                self.queried_values.add(node)
                return str(self.function_values[node])
            except:
                return error_format

        elif "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                node1_str, node2_str = [x.strip() for x in raw.split(",")]
                node1, node2 = int(node1_str), int(node2_str)
                
                if node1 < 1 or node1 > self.n or node2 < 1 or node2 > self.n:
                    return error_range
                
                val1 = self.function_values[node1]
                val2 = self.function_values[node2]
                
                if val1 > val2:
                    return f"S({node1}) > S({node2})"
                elif val1 < val2:
                    return f"S({node1}) < S({node2})"
                else:
                    return f"S({node1}) = S({node2})"
            except:
                return error_format

        elif "query_size" in parsed_info:
            # 检查配额
            if self.size_check_count >= self.max_size_checks:
                return error_quota
            
            node_str = parsed_info["query_size"].strip()
            try:
                node = int(node_str)
                if node < 1 or node > self.n:
                    return error_range
                
                self.size_check_count += 1
                return str(self.subtree_size[node])
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成反事实错误答案"""
        # 若 correct 是纯整数字符串（如 "0", "1", "2"）：返回 str(int(correct) + 1)
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 否则按以下规则替换关键词（区分语言）
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:  # en
            # 忽略大小写匹配，但返回时尽量保持简单（题目示例直接给出了"Yes"和"No"）
            # 为了符合题目 "Yes" ↔ "No" 且保持原始风格，这里做简单替换
            if correct.lower() == "yes":
                return "No"
            elif correct.lower() == "no":
                return "Yes"
        
        # 若都不匹配：在字符串末尾追加 "_WRONG"
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,
                "answer": str,
            }
        """
        queries = []

        # 1. 数值询问 (query_value)
        # 遍历所有节点
        for v in range(1, self.n + 1):
            queries.append({
                "query": f"<query_value>{v}</query_value>",
                "answer": str(self.function_values[v])
            })

        # 2. 比较询问 (query_compare)
        # 遍历所有节点对 (v1, v2)
        # 虽然 N=20 时有 400 个组合，但对于自动求解器来说是可以接受的
        for v1 in range(1, self.n + 1):
            for v2 in range(1, self.n + 1):
                # 即使 v1 == v2 也是合法查询
                val1 = self.function_values[v1]
                val2 = self.function_values[v2]
                
                if val1 > val2:
                    ans = f"S({v1}) > S({v2})"
                elif val1 < val2:
                    ans = f"S({v1}) < S({v2})"
                else:
                    ans = f"S({v1}) = S({v2})"
                
                queries.append({
                    "query": f"<query_compare>{v1},{v2}</query_compare>",
                    "answer": ans
                })

        # 3. 规模核对 (query_size)
        # 遍历所有节点
        for v in range(1, self.n + 1):
            queries.append({
                "query": f"<query_size>{v}</query_size>",
                "answer": str(self.subtree_size[v])
            })
            
        return queries