# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gemini-3-pro-preview
# 推理类型: 溯因推理（明确有若干种可能性，模型需要判断那种是正确的）：面对当前的状态（反馈），推测原因。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   元素排名：某元素在排序后处于第几位
# ============================================================

import re
from .base import Game


class AbstractReasoningGame(Game):

    game_rule_zh = """\
我们来玩一个"抽象推理"游戏，规则如下：

游戏设定了 6 个带标签的元素：e1, e2, e3, e4, e5, e6。每个元素有 4 个整数属性：(A, B, C, D)。

属性取值如下：
{element_attrs}

全局存在且固定的一条比较规则 R，且 R 只可能是以下四种之一（均为字典序比较）：
- R_A: 按 A 升序；若相同，则按 B 降序；若仍相同，则按 C 升序；若仍相同，则按 D 升序。
- R_B: 按 C 降序；若相同，则按 A 升序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。
- R_C: 按 B 升序；若相同，则按 C 升序；若仍相同，则按 D 升序。
- R_D: 按 A 升序；若相同，则按 C 降序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。

根据规则 R，6 个元素会形成一个确定的全序（从第 1 名到第 6 名）。

你的任务是通过尽可能少的成对比较查询，同时完成：
1) 判定真实采用的规则 R 属于哪一种（R_A、R_B、R_C 或 R_D）；
2) 给出目标元素 {target_element} 在最终全序中的名次 k（1 为最前，6 为最后）。

你可以发起成对比较查询。每次查询的形式为：比较(x, y)，其中 x 不等于 y 且 x, y 属于集合 {{e1, e2, e3, e4, e5, e6}}。
我会根据真实规则 R 对 x 与 y 在最终全序中的先后给出回答，回答仅为："x在前"或"y在前"。

注意：不允许直接询问 R 的身份（如"是否为 R_A?"）、任何元素的绝对名次、或要求返回完整排序。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如比较 e1 和 e3）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明规则类型（R_A、R_B、R_C 或 R_D）并给出目标元素 {target_element} 的名次（1 到 6 的整数），格式如下：

<answer>rule=R_A, rank=3</answer>
"""

    game_rule_en = """\
Let's play an "Abstract Reasoning" game. Here are the rules:

There are 6 labeled elements: e1, e2, e3, e4, e5, e6. Each element has 4 integer attributes: (A, B, C, D).

Attribute values are as follows:
{element_attrs}

There exists a globally fixed comparison rule R, which must be one of the following four types (all using lexicographic ordering):
- R_A: Sort by A ascending; if equal, by B descending; if still equal, by C ascending; if still equal, by D ascending.
- R_B: Sort by C descending; if equal, by A ascending; if still equal, by B ascending; if still equal, by D ascending.
- R_C: Sort by B ascending; if equal, by C ascending; if still equal, by D ascending.
- R_D: Sort by A ascending; if equal, by C descending; if still equal, by B ascending; if still equal, by D ascending.

According to rule R, the 6 elements form a definite total order (from rank 1 to rank 6).

Your task is to use as few pairwise comparison queries as possible to simultaneously determine:
1) Which rule R is actually being used (R_A, R_B, R_C, or R_D);
2) The rank k of the target element {target_element} in the final total order (1 is first, 6 is last).

You can make pairwise comparison queries. Each query takes the form: compare(x, y), where x is not equal to y and x, y belong to the set {{e1, e2, e3, e4, e5, e6}}.
I will respond based on the true rule R regarding which of x or y comes first in the final total order. The answer will be either: "x comes first" or "y comes first".

Note: You may not directly ask for R's identity (e.g., "Is it R_A?"), the absolute rank of any element, or request the complete ordering.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rule type (R_A, R_B, R_C, or R_D) and the rank of target element {target_element} (an integer from 1 to 6), using this format:

<answer>rule=R_A, rank=3</answer>
"""

    # ================= 场景 1：交通 =================
    contextualized_rule_zh_1 = """\
欢迎使用“智能交通调度系统”。系统当前有 6 条备选路线，标签为：e1, e2, e3, e4, e5, e6。
每条路线具有 4 个核心整数指标属性：(A: 拥堵指数, B: 平均车速, C: 信号灯数, D: 绕路里程)。

属性取值如下：
{element_attrs}

系统内置了一条全局固定且保密的路径调度规则 R，且 R 只可能是以下四种之一（均为字典序比较）：
- R_A: 按 A 升序；若相同，则按 B 降序；若仍相同，则按 C 升序；若仍相同，则按 D 升序。
- R_B: 按 C 降序；若相同，则按 A 升序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。
- R_C: 按 B 升序；若相同，则按 C 升序；若仍相同，则按 D 升序。
- R_D: 按 A 升序；若相同，则按 C 降序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。

根据规则 R，6 条路线会形成一个确定的推荐全序（从第 1 名到第 6 名）。

你的任务是通过尽可能少的成对比较查询，同时完成：
1) 判定真实采用的调度规则 R 属于哪一种（R_A、R_B、R_C 或 R_D）；
2) 给出目标路线 {target_element} 在最终推荐全序中的名次 k（1 为最优先，6 为最后）。

你可以发起成对比较查询。每次查询的形式为：比较(x, y)，其中 x 不等于 y 且 x, y 属于集合 {{e1, e2, e3, e4, e5, e6}}。
我会根据真实规则 R 对 x 与 y 在最终调度全序中的先后给出回答，回答仅为："x在前"或"y在前"。

注意：不允许直接询问 R 的身份（如"是否为 R_A?"）、任何路线的绝对名次、或要求返回完整排序。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如比较 e1 和 e3）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明规则类型（R_A、R_B、R_C 或 R_D）并给出目标路线 {target_element} 的名次（1 到 6 的整数），格式如下：

<answer>rule=R_A, rank=3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Dispatch System". The system currently has 6 alternative routes, labeled: e1, e2, e3, e4, e5, e6.
Each route has 4 core integer metrics: (A: Congestion Index, B: Average Speed, C: Traffic Lights, D: Detour Mileage).

Attribute values are as follows:
{element_attrs}

There exists a globally fixed and confidential dispatch rule R, which must be one of the following four types (all using lexicographic ordering):
- R_A: Sort by A ascending; if equal, by B descending; if still equal, by C ascending; if still equal, by D ascending.
- R_B: Sort by C descending; if equal, by A ascending; if still equal, by B ascending; if still equal, by D ascending.
- R_C: Sort by B ascending; if equal, by C ascending; if still equal, by D ascending.
- R_D: Sort by A ascending; if equal, by C descending; if still equal, by B ascending; if still equal, by D ascending.

According to rule R, the 6 routes form a definite recommended total order (from rank 1 to rank 6).

Your task is to use as few pairwise comparison queries as possible to simultaneously determine:
1) Which dispatch rule R is actually being used (R_A, R_B, R_C, or R_D);
2) The rank k of the target route {target_element} in the final recommended total order (1 is first, 6 is last).

You can make pairwise comparison queries. Each query takes the form: compare(x, y), where x is not equal to y and x, y belong to the set {{e1, e2, e3, e4, e5, e6}}.
I will respond based on the true rule R regarding which of x or y comes first in the dispatch total order. The answer will be either: "x comes first" or "y comes first".

Note: You may not directly ask for R's identity (e.g., "Is it R_A?"), the absolute rank of any route, or request the complete ordering.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rule type (R_A, R_B, R_C, or R_D) and the rank of target route {target_element} (an integer from 1 to 6), using this format:

<answer>rule=R_A, rank=3</answer>
"""

    # ================= 场景 2：医疗 =================
    contextualized_rule_zh_2 = """\
欢迎使用“临床诊疗方案评估系统”。系统设定了 6 个备选靶向治疗方案，标签为：e1, e2, e3, e4, e5, e6。
每个方案具有 4 个核心整数评估属性：(A: 副作用指数, B: 免疫激活度, C: 疗程天数, D: 复发风险值)。

属性取值如下：
{element_attrs}

系统内置了一条全局固定且保密的临床评估规则 R，且 R 只可能是以下四种之一（均为字典序比较）：
- R_A: 按 A 升序；若相同，则按 B 降序；若仍相同，则按 C 升序；若仍相同，则按 D 升序。
- R_B: 按 C 降序；若相同，则按 A 升序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。
- R_C: 按 B 升序；若相同，则按 C 升序；若仍相同，则按 D 升序。
- R_D: 按 A 升序；若相同，则按 C 降序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。

根据规则 R，6 个方案会形成一个确定的优选全序（从第 1 名到第 6 名）。

你的任务是通过尽可能少的成对比较查询，同时完成：
1) 判定真实采用的评估规则 R 属于哪一种（R_A、R_B、R_C 或 R_D）；
2) 给出目标方案 {target_element} 在最终优选全序中的名次 k（1 为最优先，6 为最后）。

你可以发起成对比较查询。每次查询的形式为：比较(x, y)，其中 x 不等于 y 且 x, y 属于集合 {{e1, e2, e3, e4, e5, e6}}。
我会根据真实规则 R 对 x 与 y 在最终临床优选全序中的先后给出回答，回答仅为："x在前"或"y在前"。

注意：不允许直接询问 R 的身份（如"是否为 R_A?"）、任何方案的绝对名次、或要求返回完整排序。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如比较 e1 和 e3）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明规则类型（R_A、R_B、R_C 或 R_D）并给出目标方案 {target_element} 的名次（1 到 6 的整数），格式如下：

<answer>rule=R_A, rank=3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Clinical Treatment Plan Evaluation System". The system has 6 alternative targeted treatment plans, labeled: e1, e2, e3, e4, e5, e6.
Each plan has 4 core integer evaluation attributes: (A: Side Effect Index, B: Immune Activation Level, C: Treatment Days, D: Relapse Risk Value).

Attribute values are as follows:
{element_attrs}

There exists a globally fixed and confidential evaluation rule R, which must be one of the following four types (all using lexicographic ordering):
- R_A: Sort by A ascending; if equal, by B descending; if still equal, by C ascending; if still equal, by D ascending.
- R_B: Sort by C descending; if equal, by A ascending; if still equal, by B ascending; if still equal, by D ascending.
- R_C: Sort by B ascending; if equal, by C ascending; if still equal, by D ascending.
- R_D: Sort by A ascending; if equal, by C descending; if still equal, by B ascending; if still equal, by D ascending.

According to rule R, the 6 plans form a definite total order for clinical preference (from rank 1 to rank 6).

Your task is to use as few pairwise comparison queries as possible to simultaneously determine:
1) Which evaluation rule R is actually being used (R_A, R_B, R_C, or R_D);
2) The rank k of the target plan {target_element} in the final preference total order (1 is first, 6 is last).

You can make pairwise comparison queries. Each query takes the form: compare(x, y), where x is not equal to y and x, y belong to the set {{e1, e2, e3, e4, e5, e6}}.
I will respond based on the true rule R regarding which of x or y comes first in the clinical preference total order. The answer will be either: "x comes first" or "y comes first".

Note: You may not directly ask for R's identity (e.g., "Is it R_A?"), the absolute rank of any plan, or request the complete ordering.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rule type (R_A, R_B, R_C, or R_D) and the rank of target plan {target_element} (an integer from 1 to 6), using this format:

<answer>rule=R_A, rank=3</answer>
"""

    # ================= 场景 3：教育 =================
    contextualized_rule_zh_3 = """\
欢迎来到“自适应学习路径规划系统”。当前设定了 6 个核心教学模块，标签为：e1, e2, e3, e4, e5, e6。
每个模块包含 4 个核心整数属性：(A: 难度系数, B: 互动活跃度, C: 前置知识点数, D: 预计课时)。

属性取值如下：
{element_attrs}

系统内置了一条全局固定且保密的课程编排规则 R，且 R 只可能是以下四种之一（均为字典序比较）：
- R_A: 按 A 升序；若相同，则按 B 降序；若仍相同，则按 C 升序；若仍相同，则按 D 升序。
- R_B: 按 C 降序；若相同，则按 A 升序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。
- R_C: 按 B 升序；若相同，则按 C 升序；若仍相同，则按 D 升序。
- R_D: 按 A 升序；若相同，则按 C 降序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。

根据规则 R，6 个教学模块会形成一个确定的学习顺序全序（从第 1 名到第 6 名）。

你的任务是通过尽可能少的成对比较查询，同时完成：
1) 判定真实采用的编排规则 R 属于哪一种（R_A、R_B、R_C 或 R_D）；
2) 给出目标模块 {target_element} 在最终学习顺序中的名次 k（1 为最先学习，6 为最后）。

你可以发起成对比较查询。每次查询的形式为：比较(x, y)，其中 x 不等于 y 且 x, y 属于集合 {{e1, e2, e3, e4, e5, e6}}。
我会根据真实规则 R 对 x 与 y 在最终学习全序中的先后给出回答，回答仅为："x在前"或"y在前"。

注意：不允许直接询问 R 的身份（如"是否为 R_A?"）、任何模块的绝对名次、或要求返回完整排序。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如比较 e1 和 e3）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明规则类型（R_A、R_B、R_C 或 R_D）并给出目标模块 {target_element} 的名次（1 到 6 的整数），格式如下：

<answer>rule=R_A, rank=3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Adaptive Learning Path Planning System". The system currently has 6 core teaching modules, labeled: e1, e2, e3, e4, e5, e6.
Each module has 4 core integer attributes: (A: Difficulty Level, B: Interactive Activity, C: Prerequisite Knowledge Count, D: Estimated Hours).

Attribute values are as follows:
{element_attrs}

There exists a globally fixed and confidential scheduling rule R, which must be one of the following four types (all using lexicographic ordering):
- R_A: Sort by A ascending; if equal, by B descending; if still equal, by C ascending; if still equal, by D ascending.
- R_B: Sort by C descending; if equal, by A ascending; if still equal, by B ascending; if still equal, by D ascending.
- R_C: Sort by B ascending; if equal, by C ascending; if still equal, by D ascending.
- R_D: Sort by A ascending; if equal, by C descending; if still equal, by B ascending; if still equal, by D ascending.

According to rule R, the 6 modules form a definite scheduling total order (from rank 1 to rank 6).

Your task is to use as few pairwise comparison queries as possible to simultaneously determine:
1) Which scheduling rule R is actually being used (R_A, R_B, R_C, or R_D);
2) The rank k of the target module {target_element} in the final scheduling total order (1 is first, 6 is last).

You can make pairwise comparison queries. Each query takes the form: compare(x, y), where x is not equal to y and x, y belong to the set {{e1, e2, e3, e4, e5, e6}}.
I will respond based on the true rule R regarding which of x or y comes first in the learning total order. The answer will be either: "x comes first" or "y comes first".

Note: You may not directly ask for R's identity (e.g., "Is it R_A?"), the absolute rank of any module, or request the complete ordering.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rule type (R_A, R_B, R_C, or R_D) and the rank of target module {target_element} (an integer from 1 to 6), using this format:

<answer>rule=R_A, rank=3</answer>
"""

    # ================= 场景 4：制造业/工业 =================
    contextualized_rule_zh_4 = """\
欢迎访问“工业柔性生产排程系统”。当前排队等待处理的有 6 个生产批次，标签为：e1, e2, e3, e4, e5, e6。
每个批次包含 4 个核心整数监测属性：(A: 缺陷率, B: 产能利用率, C: 能耗指标, D: 设备磨损度)。

属性取值如下：
{element_attrs}

系统内置了一条全局固定且保密的排产规则 R，且 R 只可能是以下四种之一（均为字典序比较）：
- R_A: 按 A 升序；若相同，则按 B 降序；若仍相同，则按 C 升序；若仍相同，则按 D 升序。
- R_B: 按 C 降序；若相同，则按 A 升序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。
- R_C: 按 B 升序；若相同，则按 C 升序；若仍相同，则按 D 升序。
- R_D: 按 A 升序；若相同，则按 C 降序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。

根据规则 R，6 个生产批次会形成一个确定的加工全序（从第 1 名到第 6 名）。

你的任务是通过尽可能少的成对比较查询，同时完成：
1) 判定真实采用的排产规则 R 属于哪一种（R_A、R_B、R_C 或 R_D）；
2) 给出目标批次 {target_element} 在最终加工全序中的名次 k（1 为最优先处理，6 为最后）。

你可以发起成对比较查询。每次查询的形式为：比较(x, y)，其中 x 不等于 y 且 x, y 属于集合 {{e1, e2, e3, e4, e5, e6}}。
我会根据真实规则 R 对 x 与 y 在最终排产全序中的先后给出回答，回答仅为："x在前"或"y在前"。

注意：不允许直接询问 R 的身份（如"是否为 R_A?"）、任何批次的绝对名次、或要求返回完整排序。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如比较 e1 和 e3）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明规则类型（R_A、R_B、R_C 或 R_D）并给出目标批次 {target_element} 的名次（1 到 6 的整数），格式如下：

<answer>rule=R_A, rank=3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Flexible Production Scheduling System". There are 6 production batches waiting in queue, labeled: e1, e2, e3, e4, e5, e6.
Each batch has 4 core integer monitoring attributes: (A: Defect Rate, B: Capacity Utilization, C: Energy Consumption Index, D: Equipment Wear Degree).

Attribute values are as follows:
{element_attrs}

There exists a globally fixed and confidential scheduling rule R, which must be one of the following four types (all using lexicographic ordering):
- R_A: Sort by A ascending; if equal, by B descending; if still equal, by C ascending; if still equal, by D ascending.
- R_B: Sort by C descending; if equal, by A ascending; if still equal, by B ascending; if still equal, by D ascending.
- R_C: Sort by B ascending; if equal, by C ascending; if still equal, by D ascending.
- R_D: Sort by A ascending; if equal, by C descending; if still equal, by B ascending; if still equal, by D ascending.

According to rule R, the 6 batches form a definite processing total order (from rank 1 to rank 6).

Your task is to use as few pairwise comparison queries as possible to simultaneously determine:
1) Which scheduling rule R is actually being used (R_A, R_B, R_C, or R_D);
2) The rank k of the target batch {target_element} in the final processing total order (1 is first, 6 is last).

You can make pairwise comparison queries. Each query takes the form: compare(x, y), where x is not equal to y and x, y belong to the set {{e1, e2, e3, e4, e5, e6}}.
I will respond based on the true rule R regarding which of x or y comes first in the processing total order. The answer will be either: "x comes first" or "y comes first".

Note: You may not directly ask for R's identity (e.g., "Is it R_A?"), the absolute rank of any batch, or request the complete ordering.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rule type (R_A, R_B, R_C, or R_D) and the rank of target batch {target_element} (an integer from 1 to 6), using this format:

<answer>rule=R_A, rank=3</answer>
"""

    # ================= 场景 5：法律 =================
    contextualized_rule_zh_5 = """\
欢迎使用“智能司法案宗审查系统”。当前系统池中提取了 6 个待审诉讼案宗，标签为：e1, e2, e3, e4, e5, e6。
每个案宗具有 4 个核心整数特征属性：(A: 争议金额等级, B: 证据完整度, C: 预期审理周期, D: 诉讼时效紧迫度)。

属性取值如下：
{element_attrs}

系统内置了一条全局固定且保密的审查优先级规则 R，且 R 只可能是以下四种之一（均为字典序比较）：
- R_A: 按 A 升序；若相同，则按 B 降序；若仍相同，则按 C 升序；若仍相同，则按 D 升序。
- R_B: 按 C 降序；若相同，则按 A 升序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。
- R_C: 按 B 升序；若相同，则按 C 升序；若仍相同，则按 D 升序。
- R_D: 按 A 升序；若相同，则按 C 降序；若仍相同，则按 B 升序；若仍相同，则按 D 升序。

根据规则 R，6 个案宗会形成一个确定的审理全序（从第 1 名到第 6 名）。

你的任务是通过尽可能少的成对比较查询，同时完成：
1) 判定真实采用的审查规则 R 属于哪一种（R_A、R_B、R_C 或 R_D）；
2) 给出目标案宗 {target_element} 在最终审理全序中的名次 k（1 为最优先，6 为最后）。

你可以发起成对比较查询。每次查询的形式为：比较(x, y)，其中 x 不等于 y 且 x, y 属于集合 {{e1, e2, e3, e4, e5, e6}}。
我会根据真实规则 R 对 x 与 y 在最终案宗审查全序中的先后给出回答，回答仅为："x在前"或"y在前"。

注意：不允许直接询问 R 的身份（如"是否为 R_A?"）、任何案宗的绝对名次、或要求返回完整排序。

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如比较 e1 和 e3）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明规则类型（R_A、R_B、R_C 或 R_D）并给出目标案宗 {target_element} 的名次（1 到 6 的整数），格式如下：

<answer>rule=R_A, rank=3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Intelligent Judicial Case File Review System". There are 6 pending litigation case files, labeled: e1, e2, e3, e4, e5, e6.
Each case file has 4 core integer feature attributes: (A: Dispute Amount Level, B: Evidence Completeness, C: Expected Trial Period, D: Statute of Limitations Urgency).

Attribute values are as follows:
{element_attrs}

There exists a globally fixed and confidential review priority rule R, which must be one of the following four types (all using lexicographic ordering):
- R_A: Sort by A ascending; if equal, by B descending; if still equal, by C ascending; if still equal, by D ascending.
- R_B: Sort by C descending; if equal, by A ascending; if still equal, by B ascending; if still equal, by D ascending.
- R_C: Sort by B ascending; if equal, by C ascending; if still equal, by D ascending.
- R_D: Sort by A ascending; if equal, by C descending; if still equal, by B ascending; if still equal, by D ascending.

According to rule R, the 6 case files form a definite review total order (from rank 1 to rank 6).

Your task is to use as few pairwise comparison queries as possible to simultaneously determine:
1) Which review rule R is actually being used (R_A, R_B, R_C, or R_D);
2) The rank k of the target case file {target_element} in the final review total order (1 is first, 6 is last).

You can make pairwise comparison queries. Each query takes the form: compare(x, y), where x is not equal to y and x, y belong to the set {{e1, e2, e3, e4, e5, e6}}.
I will respond based on the true rule R regarding which of x or y comes first in the review total order. The answer will be either: "x comes first" or "y comes first".

Note: You may not directly ask for R's identity (e.g., "Is it R_A?"), the absolute rank of any case file, or request the complete ordering.

## Query and Answer Format (must strictly follow)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., comparing e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rule type (R_A, R_B, R_C, or R_D) and the rank of target case file {target_element} (an integer from 1 to 6), using this format:

<answer>rule=R_A, rank=3</answer>
"""

    tags = ["answer", "query_compare"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    # 难度配置
    # 每个难度包含：元素属性、目标元素、真实规则
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {  # 简单：属性差异明显，规则 R_A
                "elements": {
                    "e1": {"A": 1, "B": 5, "C": 3, "D": 10},
                    "e2": {"A": 3, "B": 8, "C": 2, "D": 15},
                    "e3": {"A": 2, "B": 6, "C": 4, "D": 12},
                    "e4": {"A": 5, "B": 4, "C": 1, "D": 18},
                    "e5": {"A": 4, "B": 7, "C": 5, "D": 20},
                    "e6": {"A": 6, "B": 3, "C": 6, "D": 25},
                },
                "target": "e2",
                "rule": "R_A",
            },
            2: {  # 中等偏下：规则 R_C
                "elements": {
                    "e1": {"A": 5, "B": 7, "C": 4, "D": 11},
                    "e2": {"A": 6, "B": 9, "C": 3, "D": 14},
                    "e3": {"A": 5, "B": 6, "C": 5, "D": 9},
                    "e4": {"A": 7, "B": 8, "C": 2, "D": 16},
                    "e5": {"A": 4, "B": 10, "C": 6, "D": 21},
                    "e6": {"A": 6, "B": 5, "C": 4, "D": 13},
                },
                "target": "e2",
                "rule": "R_C",
            },
            3: {  # 中等偏上：规则 R_B，需要多级比较
                "elements": {
                    "e1": {"A": 7, "B": 9, "C": 5, "D": 11},
                    "e2": {"A": 5, "B": 12, "C": 4, "D": 23},
                    "e3": {"A": 7, "B": 8, "C": 6, "D": 7},
                    "e4": {"A": 6, "B": 10, "C": 3, "D": 15},
                    "e5": {"A": 5, "B": 7, "C": 7, "D": 31},
                    "e6": {"A": 8, "B": 9, "C": 2, "D": 19},
                },
                "target": "e2",
                "rule": "R_B",
            },
            4: {  # 较难：规则 R_D，属性相近
                "elements": {
                    "e1": {"A": 5, "B": 8, "C": 6, "D": 12},
                    "e2": {"A": 5, "B": 9, "C": 5, "D": 18},
                    "e3": {"A": 6, "B": 7, "C": 4, "D": 10},
                    "e4": {"A": 5, "B": 10, "C": 6, "D": 22},
                    "e5": {"A": 7, "B": 6, "C": 3, "D": 15},
                    "e6": {"A": 5, "B": 11, "C": 5, "D": 25},
                },
                "target": "e2",
                "rule": "R_D",
            },
            5: {  # 难：规则 R_A，多个属性相同需要深层比较
                "elements": {
                    "e1": {"A": 5, "B": 10, "C": 4, "D": 20},
                    "e2": {"A": 5, "B": 10, "C": 3, "D": 18},
                    "e3": {"A": 5, "B": 9, "C": 4, "D": 22},
                    "e4": {"A": 6, "B": 8, "C": 5, "D": 16},
                    "e5": {"A": 5, "B": 10, "C": 4, "D": 15},
                    "e6": {"A": 4, "B": 11, "C": 6, "D": 25},
                },
                "target": "e2",
                "rule": "R_A",
            },
        },
        "en": {
            1: {
                "elements": {
                    "e1": {"A": 1, "B": 5, "C": 3, "D": 10},
                    "e2": {"A": 3, "B": 8, "C": 2, "D": 15},
                    "e3": {"A": 2, "B": 6, "C": 4, "D": 12},
                    "e4": {"A": 5, "B": 4, "C": 1, "D": 18},
                    "e5": {"A": 4, "B": 7, "C": 5, "D": 20},
                    "e6": {"A": 6, "B": 3, "C": 6, "D": 25},
                },
                "target": "e2",
                "rule": "R_A",
            },
            2: {
                "elements": {
                    "e1": {"A": 5, "B": 7, "C": 4, "D": 11},
                    "e2": {"A": 6, "B": 9, "C": 3, "D": 14},
                    "e3": {"A": 5, "B": 6, "C": 5, "D": 9},
                    "e4": {"A": 7, "B": 8, "C": 2, "D": 16},
                    "e5": {"A": 4, "B": 10, "C": 6, "D": 21},
                    "e6": {"A": 6, "B": 5, "C": 4, "D": 13},
                },
                "target": "e2",
                "rule": "R_C",
            },
            3: {
                "elements": {
                    "e1": {"A": 7, "B": 9, "C": 5, "D": 11},
                    "e2": {"A": 5, "B": 12, "C": 4, "D": 23},
                    "e3": {"A": 7, "B": 8, "C": 6, "D": 7},
                    "e4": {"A": 6, "B": 10, "C": 3, "D": 15},
                    "e5": {"A": 5, "B": 7, "C": 7, "D": 31},
                    "e6": {"A": 8, "B": 9, "C": 2, "D": 19},
                },
                "target": "e2",
                "rule": "R_B",
            },
            4: {
                "elements": {
                    "e1": {"A": 5, "B": 8, "C": 6, "D": 12},
                    "e2": {"A": 5, "B": 9, "C": 5, "D": 18},
                    "e3": {"A": 6, "B": 7, "C": 4, "D": 10},
                    "e4": {"A": 5, "B": 10, "C": 6, "D": 22},
                    "e5": {"A": 7, "B": 6, "C": 3, "D": 15},
                    "e6": {"A": 5, "B": 11, "C": 5, "D": 25},
                },
                "target": "e2",
                "rule": "R_D",
            },
            5: {
                "elements": {
                    "e1": {"A": 5, "B": 10, "C": 4, "D": 20},
                    "e2": {"A": 5, "B": 10, "C": 3, "D": 18},
                    "e3": {"A": 5, "B": 9, "C": 4, "D": 22},
                    "e4": {"A": 6, "B": 8, "C": 5, "D": 16},
                    "e5": {"A": 5, "B": 10, "C": 4, "D": 15},
                    "e6": {"A": 4, "B": 11, "C": 6, "D": 25},
                },
                "target": "e2",
                "rule": "R_A",
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：加载难度配置，计算全序排名"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 保存元素属性
        self.elements = cfg["elements"]
        self.target_element = cfg["target"]
        self.true_rule = cfg["rule"]
        
        # 格式化元素属性用于游戏规则显示
        element_lines = []
        for eid in sorted(self.elements.keys()):
            attrs = self.elements[eid]
            element_lines.append(
                f"- {eid}: (A={attrs['A']}, B={attrs['B']}, C={attrs['C']}, D={attrs['D']})"
            )
        self._game_info["element_attrs"] = "\n".join(element_lines)
        self._game_info["target_element"] = self.target_element
        
        # 根据真实规则计算全序排名
        self._compute_ranking()

    def _compute_ranking(self):
        """根据真实规则计算所有元素的全序排名"""
        element_list = list(self.elements.keys())
        
        # 根据规则定义排序键
        def get_sort_key(eid):
            attrs = self.elements[eid]
            if self.true_rule == "R_A":
                # A升序, B降序, C升序, D升序
                return (attrs["A"], -attrs["B"], attrs["C"], attrs["D"])
            elif self.true_rule == "R_B":
                # C降序, A升序, B升序, D升序
                return (-attrs["C"], attrs["A"], attrs["B"], attrs["D"])
            elif self.true_rule == "R_C":
                # B升序, C升序, D升序
                return (attrs["B"], attrs["C"], attrs["D"])
            elif self.true_rule == "R_D":
                # A升序, C降序, B升序, D升序
                return (attrs["A"], -attrs["C"], attrs["B"], attrs["D"])
            else:
                raise ValueError(f"Unknown rule: {self.true_rule}")
        
        # 排序得到全序
        sorted_elements = sorted(element_list, key=get_sort_key)
        
        # 验证全序性：确保没有两个元素的排序键完全相同
        keys = [get_sort_key(eid) for eid in sorted_elements]
        for i in range(len(keys) - 1):
            if keys[i] == keys[i + 1]:
                raise ValueError(
                    f"Elements {sorted_elements[i]} and {sorted_elements[i+1]} "
                    f"have identical sort keys under rule {self.true_rule}. "
                    f"Total order is not guaranteed."
                )
        
        # 保存排名映射（元素 -> 名次，1-based）
        self.ranking = {eid: rank + 1 for rank, eid in enumerate(sorted_elements)}
        
        # 保存目标元素的正确名次
        self.target_rank = self.ranking[self.target_element]

    def _compare_elements(self, e1, e2):
        """根据真实规则比较两个元素的先后顺序，返回在前的元素"""
        # 根据排名判断谁在前
        if self.ranking[e1] < self.ranking[e2]:
            return e1
        else:
            return e2

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info.get("answer", "")
        
        # 解析答案: rule=R_X, rank=k
        rule_match = re.search(r"rule=(R_[A-D])", raw_ans)
        rank_match = re.search(r"rank=(\d+)", raw_ans)
        
        if not rule_match or not rank_match:
            return False
            
        pred_rule = rule_match.group(1)
        pred_rank = int(rank_match.group(1))
        
        return pred_rule == self.true_rule and pred_rank == self.target_rank

    def _cf_core_produce(self, parsed_info):
        """处理查询并返回判定结果"""
        if "query_compare" in parsed_info:
            query = parsed_info["query_compare"]
            parts = [p.strip() for p in query.split(",")]
            if len(parts) == 2:
                e1, e2 = parts
                if e1 in self.elements and e2 in self.elements and e1 != e2:
                    first = self._compare_elements(e1, e2)
                    # 暂存本次查询的两个元素，供 _cf_make_wrong 使用
                    self._last_compare_pair = (e1, e2)
                    if self.config.language == "zh":
                        return f"{first}在前"
                    else:
                        return f"{first} comes first"
        
        self._last_compare_pair = None
        if self.config.language == "zh":
            return "无效的查询。请确保元素存在且格式正确。"
        else:
            return "Invalid query. Please ensure elements exist and format is correct."

    def get_all_possible_queries(self):
        """获取所有可能的查询组合"""
        queries = []
        elements = sorted(self.elements.keys())
        for i in range(len(elements)):
            for j in range(i + 1, len(elements)):
                e1, e2 = elements[i], elements[j]
                query_str = f"<query_compare>{e1},{e2}</query_compare>"
                first = self._compare_elements(e1, e2)
                if self.config.language == "zh":
                    answer_str = f"{first}在前"
                else:
                    answer_str = f"{first} comes first"
                queries.append({
                    "query": query_str,
                    "answer": answer_str,
                })
        return queries

    def _cf_make_wrong(self, correct):
        """生成反事实错误答案：将比较结果反转为另一个元素在前"""
        pair = getattr(self, '_last_compare_pair', None)
        if pair is not None:
            e1, e2 = pair
            # 找出正确答案中在前的元素，然后换成另一个
            if self.config.language == "zh":
                for e in (e1, e2):
                    if e in correct:
                        other = e2 if e == e1 else e1
                        return f"{other}在前"
            else:
                for e in (e1, e2):
                    if e in correct:
                        other = e2 if e == e1 else e1
                        return f"{other} comes first"
        # fallback
        if correct.endswith("[WRONG]"):
            return correct
        return correct + " [WRONG]"

