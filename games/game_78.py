# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。例如扫雷，需要推断出哪些格子埋有地雷。
# 数据结构: 树：存在一个N节点的树。
# 知识点:   限距节点数：从某节点出发距离不超过k的节点共有多少个
# ============================================================

from .base import Game
import random
from collections import deque

class TreeSearchGame(Game):

    game_rule_zh = """\
我们现在来玩一个"树搜索"的推理游戏，规则如下：

游戏设定了一棵未知的有限无向树 T，节点数为 {n}。给定正整数 K = {k}。

定义距离 dist(u, v) 为树上 u 到 v 的最短路径边数。
定义函数 E(v) 为从节点 v 出发，距离小于等于 K 的节点总数（包括 v 自己）。

每个节点 v 的所有邻居在本地以端口 1 到 deg(v) 的整数编号标识，编号固定但对你未知；不同节点的端口编号彼此无关。

你从起始节点 S 开始。游戏保证：
- 存在唯一节点 H 使 E(H) 严格最大。
- 对任意节点 u 不等于 H，如果 w 是 u 到 H 的唯一路径上的相邻下一节点，则 E(w) 大于 E(u)（沿指向 H 的路径严格单调上升）。

你的目标是通过尽可能少的交互次数，找到并宣告这个唯一使 E(v) 最大的节点 H。

你可以反复向我提出以下五类操作（每次仅限一个操作），我会根据真实设定如实回答：

1. 询问度数：询问当前节点的度数（邻居数量）。回答一个非负整数。
2. 询问值：询问当前节点的 E 值。回答一个正整数。
3. 移动：沿当前节点的第 j 号端口移动到相邻节点。若端口存在则返回"已移动"，否则返回"无此端口"且位置不变。
4. 回退：返回到上一个节点。若可以回退则返回"已返回"，否则返回"无法返回"。
5. 宣告：宣告当前节点为目标节点 H。若正确则游戏成功，否则游戏失败。

## 询问与宣告的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 询问度数：
<query_degree></query_degree>

- 询问值：
<query_value></query_value>

- 移动到第 j 号端口（例如移动到端口 2）：
<move>2</move>

- 回退到上一个节点：
<back></back>

- 宣告当前节点为目标：
<answer></answer>
"""

    game_rule_en = """\
Let's play a "Tree Search" deduction game. Here are the rules:

There is an unknown finite undirected tree T with {n} nodes. Given a positive integer K = {k}.

Define dist(u, v) as the number of edges in the shortest path from u to v in the tree.
Define function E(v) as the count of nodes reachable from node v within distance K (including v itself).

Each node v has neighbors locally identified by port numbers 1 to deg(v), where deg(v) is the degree of v. The numbering is fixed but unknown to you; port numbering at different nodes are independent.

You start at a starting node S. The game guarantees:
- There exists a unique node H such that E(H) is strictly maximum.
- For any node u not equal to H, if w is the adjacent next node on the unique path from u to H, then E(w) is greater than E(u) (strictly monotonically increasing along the path toward H).

Your goal is to find and declare the unique node H that maximizes E(v) using as few interactions as possible.

You can repeatedly perform one of the following five operations (one per turn), and I will respond truthfully:

1. Query degree: Ask for the degree of the current node (number of neighbors). Answer is a non-negative integer.
2. Query value: Ask for the E value of the current node. Answer is a positive integer.
3. Move: Move along the j-th port of the current node to an adjacent node. Returns "Moved" if the port exists, otherwise "No such port" and position remains unchanged.
4. Back: Return to the previous node. Returns "Returned" if possible, otherwise "Cannot return".
5. Declare: Declare the current node as the target node H. Game succeeds if correct, otherwise fails.

## Query and Declaration Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query degree:
<query_degree></query_degree>

- Query value:
<query_value></query_value>

- Move to port j (e.g., move to port 2):
<move>2</move>

- Back to previous node:
<back></back>

- Declare current node as target:
<answer></answer>
"""

    # ==========================================
    # 场景 1：交通
    # ==========================================
    contextualized_rule_zh_1 = """\
欢迎进入“核心枢纽勘测”交通调度任务，规则如下：

我们的城市路网系统设计为一棵未知的有限无向树 T（无环路），枢纽节点数为 {n}。给定通勤范围限制 K = {k}。

定义距离 dist(u, v) 为路网上枢纽 u 到 v 的最少路段数。
定义指标 E(v) 为从枢纽 v 出发，在距离小于等于 K 的范围内能辐射到的枢纽总数（包括 v 自己）。

每个枢纽 v 的相连路段在本地以端口 1 到 deg(v) 的整数编号标识，编号固定但对你未知；不同枢纽的端口编号彼此无关。

你从起始枢纽 S 开始调度。系统保证：
- 存在唯一一个核心枢纽 H，使得 E(H) 严格最大。
- 对任意非 H 的枢纽 u，如果 w 是 u 到 H 的唯一路径上的相邻下一枢纽，则 E(w) 大于 E(u)（即沿着指向 H 的路径，辐射能力严格单调上升）。

你的目标是通过尽可能少的交互次数，找到并宣告这个唯一使 E(v) 最大的核心枢纽 H。

你可以反复向我提出以下五类操作（每次仅限一个操作），我会根据真实路网状态如实回答：

1. 询问直达路线：询问当前枢纽的度数（直接相连的枢纽数量）。回答一个非负整数。
2. 询问辐射力：询问当前枢纽的 E 值。回答一个正整数。
3. 移动：沿当前枢纽的第 j 号端口路段移动到相邻枢纽。若路线存在则返回"已移动"，否则返回"无此端口"且位置不变。
4. 回退：返回到上一个枢纽。若可以回退则返回"已返回"，否则返回"无法返回"。
5. 宣告：宣告当前枢纽为核心枢纽 H。若正确则任务成功，否则失败。

## 询问与宣告的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 询问直达路线（度数）：
<query_degree></query_degree>

- 询问辐射力（E值）：
<query_value></query_value>

- 移动到第 j 号端口路线（例如移动到端口 2）：
<move>2</move>

- 回退到上一个枢纽：
<back></back>

- 宣告当前枢纽为目标：
<answer></answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Core Hub Survey" transportation dispatch task. Here are the rules:

Our city road network is designed as an unknown finite undirected tree T (no cycles) with {n} hub nodes. Given a commute range limit K = {k}.

Define dist(u, v) as the minimum number of road segments from hub u to v.
Define function E(v) as the total number of hubs reachable from hub v within a distance of K (including v itself).

Each hub v has connected road segments locally identified by port numbers 1 to deg(v), where deg(v) is its degree. The numbering is fixed but unknown to you; port numbering at different hubs are independent.

You start at a starting hub S. The system guarantees:
- There exists a unique core hub H such that E(H) is strictly maximum.
- For any hub u not equal to H, if w is the adjacent next hub on the unique path from u to H, then E(w) is greater than E(u) (strictly monotonically increasing radiation capacity along the path toward H).

Your goal is to find and declare the unique core hub H that maximizes E(v) using as few interactions as possible.

You can repeatedly perform one of the following five operations (one per turn), and I will respond truthfully based on the actual network state:

1. Query degree: Ask for the degree of the current hub (number of directly connected hubs). Answer is a non-negative integer.
2. Query value: Ask for the E value (radiation capacity) of the current hub. Answer is a positive integer.
3. Move: Move along the j-th port road segment of the current hub to an adjacent hub. Returns "Moved" if the port exists, otherwise "No such port" and position remains unchanged.
4. Back: Return to the previous hub. Returns "Returned" if possible, otherwise "Cannot return".
5. Declare: Declare the current hub as the target core hub H. Task succeeds if correct, otherwise fails.

## Query and Declaration Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query degree (number of direct routes):
<query_degree></query_degree>

- Query value (radiation capacity):
<query_value></query_value>

- Move to port j route (e.g., move to port 2):
<move>2</move>

- Back to previous hub:
<back></back>

- Declare current hub as target:
<answer></answer>
"""

    # ==========================================
    # 场景 2：医疗
    # ==========================================
    contextualized_rule_zh_2 = """\
欢迎进入“区域医疗协同”转诊网络调度任务，规则如下：

我们的分级诊疗网络构成了一棵未知的有限无向树 T，医疗机构节点数为 {n}。给定紧急医疗响应距离限制 K = {k}。

定义距离 dist(u, v) 为网络中机构 u 到 v 的最少转诊通道数。
定义指标 E(v) 为从机构 v 出发，在距离小于等于 K 的范围内能直接调度的医疗机构总数（包括 v 自己）。

每个机构 v 的直接转诊通道在本地以端口 1 到 deg(v) 的整数编号标识，编号固定但对你未知；不同机构的端口编号彼此无关。

你从首诊机构 S 开始。系统保证：
- 存在唯一一个医疗调度中心 H，使得 E(H) 严格最大。
- 对任意非 H 的机构 u，如果 w 是 u 到 H 的唯一路径上的相邻下一机构，则 E(w) 大于 E(u)（即沿着指向 H 的路径，区域协同救治能力严格单调上升）。

你的目标是通过尽可能少的交互次数，找到并宣告这个唯一使 E(v) 最大的医疗调度中心 H。

你可以反复向我提出以下五类操作（每次仅限一个操作），我会根据真实医疗网络状态如实回答：

1. 询问转诊通道数：询问当前机构的度数（直接相连的机构数量）。回答一个非负整数。
2. 询问救治能力：询问当前机构的 E 值。回答一个正整数。
3. 移动：沿当前机构的第 j 号端口通道前往相邻机构。若通道存在则返回"已移动"，否则返回"无此端口"且位置不变。
4. 回退：返回到上一个就诊机构。若可以回退则返回"已返回"，否则返回"无法返回"。
5. 宣告：宣告当前机构为医疗调度中心 H。若正确则任务成功，否则失败。

## 询问与宣告的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 询问转诊通道数（度数）：
<query_degree></query_degree>

- 询问救治能力（E值）：
<query_value></query_value>

- 移动到第 j 号端口通道（例如移动到端口 2）：
<move>2</move>

- 回退到上一个就诊机构：
<back></back>

- 宣告当前机构为目标：
<answer></answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Regional Medical Synergy" referral network dispatch task. Here are the rules:

Our tiered diagnosis and treatment network is structured as an unknown finite undirected tree T with {n} medical institution nodes. Given an emergency medical response distance limit K = {k}.

Define dist(u, v) as the minimum number of referral channels from institution u to v.
Define function E(v) as the total number of institutions directly dispatchable from institution v within a distance of K (including v itself).

Each institution v has direct referral channels locally identified by port numbers 1 to deg(v), where deg(v) is its degree. The numbering is fixed but unknown to you; port numbering at different institutions are independent.

You start at the initial diagnostic institution S. The system guarantees:
- There exists a unique medical dispatch center H such that E(H) is strictly maximum.
- For any institution u not equal to H, if w is the adjacent next institution on the unique path from u to H, then E(w) is greater than E(u) (strictly monotonically increasing regional synergistic treatment capacity along the path toward H).

Your goal is to find and declare the unique medical dispatch center H that maximizes E(v) using as few interactions as possible.

You can repeatedly perform one of the following five operations (one per turn), and I will respond truthfully based on the actual medical network state:

1. Query degree: Ask for the degree of the current institution (number of directly connected institutions). Answer is a non-negative integer.
2. Query value: Ask for the E value (regional synergistic treatment capacity) of the current institution. Answer is a positive integer.
3. Move: Move along the j-th port channel of the current institution to an adjacent institution. Returns "Moved" if the port exists, otherwise "No such port" and position remains unchanged.
4. Back: Return to the previous institution. Returns "Returned" if possible, otherwise "Cannot return".
5. Declare: Declare the current institution as the target medical dispatch center H. Task succeeds if correct, otherwise fails.

## Query and Declaration Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query degree (number of referral channels):
<query_degree></query_degree>

- Query value (synergistic treatment capacity):
<query_value></query_value>

- Move to port j channel (e.g., move to port 2):
<move>2</move>

- Back to previous institution:
<back></back>

- Declare current institution as target:
<answer></answer>
"""

    # ==========================================
    # 场景 3：教育
    # ==========================================
    contextualized_rule_zh_3 = """\
欢迎进入“教育资源共享”网络优化任务，规则如下：

我们的区域教育网络构建为一棵未知的有限无向树 T，学校节点数为 {n}。给定资源调拨允许的最大传递层级 K = {k}。

定义距离 dist(u, v) 为网络中学校 u 到 v 的最少共享专线数。
定义指标 E(v) 为从学校 v 出发，在不超过 K 个层级内能共享到的学校总数（包括 v 自己）。

每个学校 v 的共享专线在本地以端口 1 到 deg(v) 的整数编号标识，编号固定但对你未知；不同学校的端口编号彼此无关。

你从起始学校 S 开始访问。系统保证：
- 存在唯一一个主教育资源汇聚中心 H，使得 E(H) 严格最大。
- 对任意非 H 的学校 u，如果 w 是 u 到 H 的唯一路径上的相邻下一学校，则 E(w) 大于 E(u)（即沿着指向 H 的路径，教育资源辐射力严格单调上升）。

你的目标是通过尽可能少的交互次数，找到并宣告这个唯一使 E(v) 最大的汇聚中心 H。

你可以反复向我提出以下五类操作（每次仅限一个操作），我会根据真实网络状态如实回答：

1. 询问共享专线数：询问当前学校的度数（直接合作的学校数量）。回答一个非负整数。
2. 询问辐射力：询问当前学校的 E 值。回答一个正整数。
3. 移动：通过当前学校的第 j 号端口专线访问相邻学校。若专线存在则返回"已移动"，否则返回"无此端口"且位置不变。
4. 回退：撤回到上一个访问的学校。若可以回退则返回"已返回"，否则返回"无法返回"。
5. 宣告：确立当前学校为主教育资源汇聚中心 H。若正确则任务成功，否则失败。

## 询问与宣告的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 询问共享专线数（度数）：
<query_degree></query_degree>

- 询问辐射力（E值）：
<query_value></query_value>

- 移动到第 j 号端口专线（例如移动到端口 2）：
<move>2</move>

- 回退到上一个访问的学校：
<back></back>

- 宣告当前学校为目标：
<answer></answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Educational Resource Sharing" network optimization task. Here are the rules:

Our regional education network is built as an unknown finite undirected tree T with {n} school nodes. Given a maximum transmission tier limit for resource allocation K = {k}.

Define dist(u, v) as the minimum number of sharing dedicated lines from school u to v.
Define function E(v) as the total number of schools that can be shared with from school v within K tiers (including v itself).

Each school v has sharing dedicated lines locally identified by port numbers 1 to deg(v), where deg(v) is its degree. The numbering is fixed but unknown to you; port numbering at different schools are independent.

You start at the initial school S. The system guarantees:
- There exists a unique main educational resource convergence center H such that E(H) is strictly maximum.
- For any school u not equal to H, if w is the adjacent next school on the unique path from u to H, then E(w) is greater than E(u) (strictly monotonically increasing resource radiation capability along the path toward H).

Your goal is to find and declare the unique convergence center H that maximizes E(v) using as few interactions as possible.

You can repeatedly perform one of the following five operations (one per turn), and I will respond truthfully based on the actual network state:

1. Query degree: Ask for the degree of the current school (number of directly cooperating schools). Answer is a non-negative integer.
2. Query value: Ask for the E value (resource radiation capability) of the current school. Answer is a positive integer.
3. Move: Visit an adjacent school through the j-th port dedicated line of the current school. Returns "Moved" if the line exists, otherwise "No such port" and position remains unchanged.
4. Back: Withdraw to the previously visited school. Returns "Returned" if possible, otherwise "Cannot return".
5. Declare: Establish the current school as the main educational resource convergence center H. Task succeeds if correct, otherwise fails.

## Query and Declaration Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query degree (number of sharing dedicated lines):
<query_degree></query_degree>

- Query value (resource radiation capability):
<query_value></query_value>

- Move to port j dedicated line (e.g., move to port 2):
<move>2</move>

- Back to previous school:
<back></back>

- Declare current school as target:
<answer></answer>
"""

    # ==========================================
    # 场景 4：制造业/工业
    # ==========================================
    contextualized_rule_zh_4 = """\
欢迎进入“工业供应链”物流拓扑分析任务，规则如下：

我们的工厂生产线物流拓扑构成了一棵未知的有限无向树 T，生产/仓储节点数为 {n}。给定物料配送的中转次数上限 K = {k}。

定义距离 dist(u, v) 为拓扑中节点 u 到 v 的最少运输线路数。
定义指标 E(v) 为从节点 v 出发，在不超过 K 次中转的范围内能送达的节点总数（包括 v 自己）。

每个节点 v 的运输线路在本地以端口 1 到 deg(v) 的整数编号标识，编号固定但对你未知；不同节点的端口编号彼此无关。

你从起始节点 S 开始排查。系统保证：
- 存在唯一一个主干仓储分发中心 H，使得 E(H) 严格最大。
- 对任意非 H 的节点 u，如果 w 是 u 到 H 的唯一路径上的相邻下一节点，则 E(w) 大于 E(u)（即沿着指向 H 的路径，物流覆盖度严格单调上升）。

你的目标是通过尽可能少的交互次数，找到并宣告这个唯一使 E(v) 最大的主干仓储分发中心 H。

你可以反复向我提出以下五类操作（每次仅限一个操作），我会根据真实物流拓扑如实回答：

1. 询问运输线数：询问当前节点的度数（直接相连的节点数量）。回答一个非负整数。
2. 询问物流覆盖度：询问当前节点的 E 值。回答一个正整数。
3. 移动：沿当前节点的第 j 号端口线路前往相邻节点。若线路存在则返回"已移动"，否则返回"无此端口"且位置不变。
4. 回退：退回上一个物流节点。若可以回退则返回"已返回"，否则返回"无法返回"。
5. 宣告：确认该节点为主干仓储分发中心 H。若正确则任务成功，否则失败。

## 询问与宣告的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 询问运输线数（度数）：
<query_degree></query_degree>

- 询问物流覆盖度（E值）：
<query_value></query_value>

- 移动到第 j 号端口线路（例如移动到端口 2）：
<move>2</move>

- 回退到上一个物流节点：
<back></back>

- 宣告当前节点为目标：
<answer></answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Industrial Supply Chain" logistics topology analysis task. Here are the rules:

Our factory production line logistics topology forms an unknown finite undirected tree T with {n} production/storage nodes. Given a maximum number of transits for material delivery K = {k}.

Define dist(u, v) as the minimum number of transport routes from node u to v.
Define function E(v) as the total number of nodes reachable from node v within K transits (including v itself).

Each node v has transport routes locally identified by port numbers 1 to deg(v), where deg(v) is its degree. The numbering is fixed but unknown to you; port numbering at different nodes are independent.

You start at the initial node S. The system guarantees:
- There exists a unique backbone storage distribution center H such that E(H) is strictly maximum.
- For any node u not equal to H, if w is the adjacent next node on the unique path from u to H, then E(w) is greater than E(u) (strictly monotonically increasing logistics coverage along the path toward H).

Your goal is to find and declare the unique backbone storage distribution center H that maximizes E(v) using as few interactions as possible.

You can repeatedly perform one of the following five operations (one per turn), and I will respond truthfully based on the actual logistics topology:

1. Query degree: Ask for the degree of the current node (number of directly connected nodes). Answer is a non-negative integer.
2. Query value: Ask for the E value (logistics coverage) of the current node. Answer is a positive integer.
3. Move: Proceed to an adjacent node along the j-th port route of the current node. Returns "Moved" if the route exists, otherwise "No such port" and position remains unchanged.
4. Back: Return to the previous logistics node. Returns "Returned" if possible, otherwise "Cannot return".
5. Declare: Confirm the current node as the backbone storage distribution center H. Task succeeds if correct, otherwise fails.

## Query and Declaration Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query degree (number of transport routes):
<query_degree></query_degree>

- Query value (logistics coverage):
<query_value></query_value>

- Move to port j route (e.g., move to port 2):
<move>2</move>

- Back to previous logistics node:
<back></back>

- Declare current node as target:
<answer></answer>
"""

    # ==========================================
    # 场景 5：法律
    # ==========================================
    contextualized_rule_zh_5 = """\
欢迎进入“司法协作网络”线索追踪任务，规则如下：

我们的司法管辖协作网络被映射为一棵未知的有限无向树 T，司法机关节点数为 {n}。给定协查权限允许的传递层级 K = {k}。

定义距离 dist(u, v) 为网络中机关 u 到 v 的最少协查通道数。
定义指标 E(v) 为从机关 v出发，在不超过 K 个层级内可发起协查请求的机关总数（包括 v 自己）。

每个机关 v 的直接协查通道在本地以端口 1 到 deg(v) 的整数编号标识，编号固定但对你未知；不同机关的端口编号彼此无关。

你从首个接入的机关 S 开始调查。系统保证：
- 存在唯一一个案件联合指挥中心 H，使得 E(H) 严格最大。
- 对任意非 H 的机关 u，如果 w 是 u 到 H 的唯一路径上的相邻下一机关，则 E(w) 大于 E(u)（即沿着指向 H 的路径，协查覆盖广度严格单调上升）。

你的目标是通过尽可能少的交互次数，找到并宣告这个唯一使 E(v) 最大的案件联合指挥中心 H。

你可以反复向我提出以下五类操作（每次仅限一个操作），我会根据真实司法网络状态如实回答：

1. 询问协查通道数：询问当前机关的度数（直接协作的机关数量）。回答一个非负整数。
2. 询问协查广度：询问当前机关的 E 值。回答一个正整数。
3. 移动：沿当前机关的第 j 号端口通道前往相邻司法机关。若通道存在则返回"已移动"，否则返回"无此端口"且位置不变。
4. 回退：撤回到上一个请求机关。若可以回退则返回"已返回"，否则返回"无法返回"。
5. 宣告：确定该机关为案件联合指挥中心 H。若正确则任务成功，否则失败。

## 询问与宣告的格式（必须严格遵守）

每次操作只能包含一个标签。请使用以下 XML 格式：

- 询问协查通道数（度数）：
<query_degree></query_degree>

- 询问协查广度（E值）：
<query_value></query_value>

- 移动到第 j 号端口通道（例如移动到端口 2）：
<move>2</move>

- 回退到上一个请求机关：
<back></back>

- 宣告当前机关为目标：
<answer></answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Judicial Collaboration Network" clue tracking task. Here are the rules:

Our judicial jurisdiction collaboration network is mapped as an unknown finite undirected tree T with {n} judicial authority nodes. Given a transmission tier limit permitted by investigation authority K = {k}.

Define dist(u, v) as the minimum number of investigation channels from authority u to v.
Define function E(v) as the total number of authorities that can be requested for joint investigation from authority v within K tiers (including v itself).

Each authority v has direct investigation channels locally identified by port numbers 1 to deg(v), where deg(v) is its degree. The numbering is fixed but unknown to you; port numbering at different authorities are independent.

You start at the initial accessed authority S. The system guarantees:
- There exists a unique joint case command center H such that E(H) is strictly maximum.
- For any authority u not equal to H, if w is the adjacent next authority on the unique path from u to H, then E(w) is greater than E(u) (strictly monotonically increasing investigation coverage breadth along the path toward H).

Your goal is to find and declare the unique joint case command center H that maximizes E(v) using as few interactions as possible.

You can repeatedly perform one of the following five operations (one per turn), and I will respond truthfully based on the actual judicial network state:

1. Query degree: Ask for the degree of the current authority (number of directly collaborating authorities). Answer is a non-negative integer.
2. Query value: Ask for the E value (investigation coverage breadth) of the current authority. Answer is a positive integer.
3. Move: Proceed to an adjacent judicial authority along the j-th port channel of the current authority. Returns "Moved" if the channel exists, otherwise "No such port" and position remains unchanged.
4. Back: Withdraw to the previously requesting authority. Returns "Returned" if possible, otherwise "Cannot return".
5. Declare: Determine the current authority as the joint case command center H. Task succeeds if correct, otherwise fails.

## Query and Declaration Format (strictly required)

Each operation must contain only one tag. Use the following XML format:

- Query degree (number of investigation channels):
<query_degree></query_degree>

- Query value (investigation coverage breadth):
<query_value></query_value>

- Move to port j channel (e.g., move to port 2):
<move>2</move>

- Back to previous requesting authority:
<back></back>

- Declare current authority as target:
<answer></answer>
"""

    tags = ["answer", "query_degree", "query_value", "move", "back"]
    reasoning_type = "演绎推理"
    data_structure = "树"
    enable_counterfactual = False   # 设为 True 时开启反事实干预模式

    # 难度配置：
    # 1 (简单)       - N=5,  K=1, 简单链状结构
    # 2 (中等偏下)   - N=7,  K=1, 简单树结构
    # 3 (中等偏上)   - N=10, K=2, 中等复杂度树
    # 4 (较难)       - N=12, K=2, 较复杂树结构
    # 5 (难)         - N=15, K=2, 复杂树结构

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "k": 1,
                # 简单链状：1-2-3-4-5，目标为中心节点3
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "start": 1,
                "target": 3,
            },
            2: {
                "n": 7,
                "k": 1,
                # 星形结构：4为中心，连接1,2,3,5,6,7
                "edges": [(4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7)],
                "start": 1,
                "target": 4,
            },
            3: {
                "n": 10,
                "k": 2,
                # 中等树：5为中心节点
                "edges": [(5, 3), (3, 1), (3, 2), (5, 7), (7, 6), (7, 8), (5, 9), (9, 4), (9, 10)],
                "start": 1,
                "target": 5,
            },
            4: {
                "n": 12,
                "k": 2,
                # 较复杂树：6为中心节点
                "edges": [(6, 3), (3, 1), (3, 2), (6, 8), (8, 7), (8, 9), (6, 11), (11, 10), (11, 12), (6, 4), (4, 5)],
                "start": 1,
                "target": 6,
            },
            5: {
                "n": 15,
                "k": 2,
                # 复杂树：8为中心节点
                "edges": [(8, 5), (5, 2), (2, 1), (5, 3), (3, 4), (8, 10), (10, 9), (10, 11), (11, 12), 
                         (8, 14), (14, 13), (14, 15), (8, 6), (6, 7)],
                "start": 1,
                "target": 8,
            },
        },
        "en": {
            1: {
                "n": 5,
                "k": 1,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "start": 1,
                "target": 3,
            },
            2: {
                "n": 7,
                "k": 1,
                "edges": [(4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7)],
                "start": 1,
                "target": 4,
            },
            3: {
                "n": 10,
                "k": 2,
                "edges": [(5, 3), (3, 1), (3, 2), (5, 7), (7, 6), (7, 8), (5, 9), (9, 4), (9, 10)],
                "start": 1,
                "target": 5,
            },
            4: {
                "n": 12,
                "k": 2,
                "edges": [(6, 3), (3, 1), (3, 2), (6, 8), (8, 7), (8, 9), (6, 11), (11, 10), (11, 12), (6, 4), (4, 5)],
                "start": 1,
                "target": 6,
            },
            5: {
                "n": 15,
                "k": 2,
                "edges": [(8, 5), (5, 2), (2, 1), (5, 3), (3, 4), (8, 10), (10, 9), (10, 11), (11, 12), 
                         (8, 14), (14, 13), (14, 15), (8, 6), (6, 7)],
                "start": 1,
                "target": 8,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：构建树结构、计算E值、设置起始位置"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["k"] = cfg["k"]
        
        n = cfg["n"]
        k = cfg["k"]
        edges = cfg["edges"]
        
        # 构建邻接表（节点从1到n）
        self.adj = {i: [] for i in range(1, n + 1)}
        for u, v in edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        # 为每个节点的邻居分配端口编号（使用固定种子以保证可复现性）
        self.ports = {}  # ports[node] = {port_num: neighbor_node}
        rng = random.Random(42)
        for node in range(1, n + 1):
            neighbors = sorted(self.adj[node])  # 先排序保证确定性输入
            rng.shuffle(neighbors)  # 使用固定种子的随机数生成器
            self.ports[node] = {i + 1: neighbors[i] for i in range(len(neighbors))}
        
        # 计算每个节点的E值（BFS计算K-邻域大小）
        self.e_values = {}
        for node in range(1, n + 1):
            self.e_values[node] = self._calculate_e_value(node, k)
        
        # 设置起始节点和目标节点
        self.start_node = cfg["start"]
        self.target_node = cfg["target"]
        self.current_node = self.start_node
        
        # 记录移动历史，用于回退
        self.move_history = []  # 栈，存储(from_node, to_node)

    def _calculate_e_value(self, start, k):
        """BFS计算从start节点出发，距离小于等于k的节点数量"""
        visited = {start: 0}
        queue = deque([start])
        count = 0
        
        while queue:
            node = queue.popleft()
            dist = visited[node]
            count += 1
            
            if dist < k:
                for neighbor in self.adj[node]:
                    if neighbor not in visited:
                        visited[neighbor] = dist + 1
                        queue.append(neighbor)
        
        return count

    def evaluate(self, parsed_info):
        """评估答案：检查当前节点是否为目标节点"""
        return self.current_node == self.target_node

    def _cf_core_produce(self, parsed_info):
        """原始的游戏响应逻辑"""
        if self.config.language == "zh":
            moved_msg = "已移动"
            no_port_msg = "无此端口"
            returned_msg = "已返回"
            cannot_return_msg = "无法返回"
        else:
            moved_msg = "Moved"
            no_port_msg = "No such port"
            returned_msg = "Returned"
            cannot_return_msg = "Cannot return"

        # 优先级：query_degree > query_value > move > back
        if "query_degree" in parsed_info:
            # 返回当前节点的度数
            degree = len(self.adj[self.current_node])
            return str(degree)
        
        elif "query_value" in parsed_info:
            # 返回当前节点的E值
            return str(self.e_values[self.current_node])
        
        elif "move" in parsed_info:
            # 尝试移动到指定端口
            try:
                port = int(parsed_info["move"].strip())
                if port in self.ports[self.current_node]:
                    next_node = self.ports[self.current_node][port]
                    self.move_history.append((self.current_node, next_node))
                    self.current_node = next_node
                    return moved_msg
                else:
                    return no_port_msg
            except (ValueError, KeyError):
                return no_port_msg

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        由于游戏状态依赖当前节点位置，这里枚举所有节点上的所有操作。
        """
        results = []
        n = self._game_info["n"]

        if self.config.language == "zh":
            moved_msg = "已移动"
            no_port_msg = "无此端口"
            returned_msg = "已返回"
            cannot_return_msg = "无法返回"
        else:
            moved_msg = "Moved"
            no_port_msg = "No such port"
            returned_msg = "Returned"
            cannot_return_msg = "Cannot return"

        for node in range(1, n + 1):
            # 1. query_degree：在节点 node 处询问度数
            results.append({
                "query": "<query_degree></query_degree>",
                "answer": str(len(self.adj[node])),
                "context": f"at_node={node}",
            })

            # 2. query_value：在节点 node 处询问E值
            results.append({
                "query": "<query_value></query_value>",
                "answer": str(self.e_values[node]),
                "context": f"at_node={node}",
            })

            # 3. move：枚举所有端口（有效端口 + 至少一个无效端口）
            max_port = len(self.ports[node])
            for port in range(1, max_port + 1):
                # 有效端口
                neighbor = self.ports[node][port]
                results.append({
                    "query": f"<move>{port}</move>",
                    "answer": moved_msg,
                    "context": f"at_node={node}",
                })
            # 一个必然无效的端口
            invalid_port = max_port + 1
            results.append({
                "query": f"<move>{invalid_port}</move>",
                "answer": no_port_msg,
                "context": f"at_node={node}",
            })

            # 4. back：在节点 node 处回退
            # 若 move_history 非空则可回退，否则不可
            # 这里枚举两种情况
            results.append({
                "query": "<back></back>",
                "answer": returned_msg,
                "context": f"at_node={node},has_history=True",
            })
            results.append({
                "query": "<back></back>",
                "answer": cannot_return_msg,
                "context": f"at_node={node},has_history=False",
            })

        return results

    def _cf_make_wrong(self, correct: str) -> str:
        """将正确的查询响应篡改为错误值，用于反事实干预"""
        if self.config.language == "zh":
            moved_msg = "已移动"
            no_port_msg = "无此端口"
            returned_msg = "已返回"
            cannot_return_msg = "无法返回"
        else:
            moved_msg = "Moved"
            no_port_msg = "No such port"
            returned_msg = "Returned"
            cannot_return_msg = "Cannot return"

        # 移动结果取反
        if correct == moved_msg:
            return no_port_msg
        if correct == no_port_msg:
            return moved_msg

        # 回退结果取反
        if correct == returned_msg:
            return cannot_return_msg
        if correct == cannot_return_msg:
            return returned_msg

        # 数字类响应（度数或E值）：加1篡改
        try:
            val = int(correct)
            wrong = val + 1
            # 避免与正确值相同（理论上不会，但保险起见）
            if wrong == val:
                wrong = val + 2
            return str(wrong)
        except ValueError:
            pass

        return correct + "_WRONG"