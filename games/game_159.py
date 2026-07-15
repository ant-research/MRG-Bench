from .base import Game
import re
import itertools
from typing import List, Dict

class BipartiteGraphMatchingGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"隐藏二分图推理"游戏，规则如下：

游戏设定了一个二分图，包含两个顶点集：U = {{A, B, C, D}} 和 V = {{1, 2, 3, 4}}。
我已秘密选择了一个隐藏图H，它是以下{num_candidates}个候选二分图之一：

{candidates_desc}

匹配是指边的集合，其中任意两条边都不共享端点；最大匹配规模记为ν。

你的目标是通过提问确定隐藏图H是哪一个候选图，并给出该图的最大匹配规模M。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 计数型探测（Probe）：
   - 选择一个边集P，需满足：对U中的每个顶点u，在P中以u为端点的边数为1或2条（可以连接到V中的不同顶点；U中的不同顶点可以连接到V中的同一顶点）。
   - 回答：返回一个整数K，表示H与P的交集的最大匹配规模，但不提供具体匹配的边。

2. 确认型提问（Identity check）：
   - 询问"H是否等于候选X？"（X可以是{candidate_names}中的任一个）
   - 回答："是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次提问只能包含一个标签。请使用以下XML格式：

- 计数型探测（例如探测边集 (A,1),(A,2),(B,2),(C,3),(D,3)）：
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- 确认型提问（例如询问是否为候选alpha）：
<identity>alpha</identity>

提交最终答案时，必须说明隐藏图是哪个候选图以及其最大匹配规模M，格式如下：
<answer>graph=alpha, M=3</answer>
"""

    game_rule_en = """\
Let's play a "Hidden Bipartite Graph Deduction" game. Here are the rules:

The game involves a bipartite graph with two vertex sets: U = {{A, B, C, D}} and V = {{1, 2, 3, 4}}.
I have secretly selected a hidden graph H, which is one of the following {num_candidates} candidate bipartite graphs:

{candidates_desc}

A matching is a set of edges where no two edges share an endpoint; the maximum matching size is denoted as ν.

Your goal is to determine which candidate graph H is and provide its maximum matching size M through queries.

You can repeatedly ask me the following two types of questions (one per turn), and I will answer truthfully:

1. Counting Probe:
   - Choose an edge set P that satisfies: for each vertex u in U, the number of edges in P incident to u is 1 or 2 (can connect to different vertices in V; different vertices in U can connect to the same vertex in V).
   - Answer: Returns an integer K representing the maximum matching size of the intersection of H and P, without providing the specific matching edges.

2. Identity Check:
   - Ask "Is H equal to candidate X?" (X can be any of {candidate_names})
   - Answer: "Yes" or "No".

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Counting Probe (e.g., probing edge set (A,1),(A,2),(B,2),(C,3),(D,3)):
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- Identity Check (e.g., asking if it is candidate alpha):
<identity>alpha</identity>

When submitting the final answer, specify which candidate graph and its maximum matching size M, using this format:
<answer>graph=alpha, M=3</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能物流网络拓扑推演”系统。

系统设定了一个双边调度网络，包含配送中心集合：U = {{A, B, C, D}} 和派送区域集合：V = {{1, 2, 3, 4}}。
由于气候影响，系统已秘密锁定了一个当前的“实际连通状态”H，它是以下{num_candidates}个候选拓扑之一：

{candidates_desc}

并发专线（匹配）是指路线的集合，其中任意两条专线都不共享配送中心或派送区域；系统最大并发专线数记为M。

你的目标是通过探测确定实际连通状态H是哪一个候选拓扑，并给出该网络的最大并发专线数M。

你可以反复向系统提交以下两类指令（每次仅限一个），系统将如实反馈：

1. 连通性测试（Probe）：
   - 选择一个测试连线集P，需满足：对U中的每个配送中心u，在P中以u为起点的连线数为1或2条（可以连接到不同的派送区域；不同的配送中心也可以连接到同一区域）。
   - 回答：返回一个整数K，表示实际状态H与测试方案P交集所能支持的最大并发专线数，但不提供具体的调度明细。

2. 拓扑确认（Identity check）：
   - 询问"H是否等于候选拓扑X？"（X可以是{candidate_names}中的任一个）
   - 回答："是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，推演失败。

每次交互只能包含一个标签。请使用以下XML格式：

- 连通性测试（例如探测连线 (A,1),(A,2),(B,2),(C,3),(D,3)）：
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- 拓扑确认（例如询问是否为候选alpha）：
<identity>alpha</identity>

提交最终答案时，必须说明实际拓扑是哪个候选以及其最大并发专线数M，格式如下：
<answer>graph=alpha, M=3</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the "Intelligent Logistics Network Topology Deduction" system.

The system features a bipartite dispatch network comprising Distribution Centers: U = {{A, B, C, D}} and Delivery Zones: V = {{1, 2, 3, 4}}.
Due to weather impacts, the system has secretly locked into a "Real Connectivity State" H, which is one of the following {num_candidates} candidate topologies:

{candidates_desc}

A concurrent dedicated route (matching) is a set of active routes where no two routes share the same distribution center or delivery zone. The maximum number of concurrent dedicated routes is denoted as M.

Your goal is to deduce the Real Connectivity State H through probing and determine its maximum concurrent dedicated route capacity M.

You can repeatedly submit the following two types of queries (one per turn), and the system will respond truthfully:

1. Connectivity Probe (Probe):
   - Submit a test routing set P, satisfying: for each center u in U, the number of routes originating from u in P must be 1 or 2 (can target different zones; different centers can target the same zone).
   - Answer: Returns an integer K representing the maximum number of concurrent dedicated routes supported by the intersection of H and P, without revealing the specific dispatch schedule.

2. Topology Check (Identity check):
   - Ask "Is H equal to candidate topology X?" (X can be any of {candidate_names})
   - Answer: "Yes" or "No".

When you have gathered enough information, submit your final answer. If the answer is incorrect or improperly formatted, the deduction fails.

Each query must contain only one tag. Use the following XML format:

- Connectivity Probe (e.g., probing routes (A,1),(A,2),(B,2),(C,3),(D,3)):
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- Topology Check (e.g., asking if it is candidate alpha):
<identity>alpha</identity>

When submitting the final answer, specify which candidate topology it is and its maximum concurrent dedicated route capacity M, using this format:
<answer>graph=alpha, M=3</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“智能医疗排班调度推演”系统。

本院当前可用资源包含专家医师集合：U = {{A, B, C, D}} 和特需手术室集合：V = {{1, 2, 3, 4}}。
由于设备资质审核变动，系统内隐藏了一份当前的“实际资质授权表”H，它是以下{num_candidates}种候选授权表之一：

{candidates_desc}

并发手术台数（匹配）是指排班的集合，要求任意两台手术不共享同一个医师或同一个手术室；最大并发手术台数记为M。

你的目标是通过探测推断出实际资质授权表H是哪一个，并评估全院当前的最大并发手术台数M。

你可以反复向系统提交以下两类排班指令（每次仅限一个），系统将如实反馈：

1. 排班试探方案（Probe）：
   - 提交一个意向集P，需满足：对U中的每位医师u，在P中u申请的手术室数量为1或2间（可申请不同手术室；不同医师也可申请同一手术室）。
   - 回答：返回一个整数K，表示在实际授权表H与试探方案P的交集中，能够成功运作的最大并发手术台数，但不提供具体的排班明细。

2. 授权表确认（Identity check）：
   - 询问"H是否等于候选授权表X？"（X可以是{candidate_names}中的任一个）
   - 回答："是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，排班推演失败。

每次交互只能包含一个标签。请使用以下XML格式：

- 排班试探（例如提交意向 (A,1),(A,2),(B,2),(C,3),(D,3)）：
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- 授权表确认（例如询问是否为候选alpha）：
<identity>alpha</identity>

提交最终答案时，必须说明实际授权表是哪个候选以及其最大并发手术台数M，格式如下：
<answer>graph=alpha, M=3</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the "Intelligent Medical Scheduling Deduction" system.

The hospital's current available resources include a set of Medical Experts: U = {{A, B, C, D}} and a set of Specialized Surgery Rooms: V = {{1, 2, 3, 4}}.
Due to changes in equipment qualification reviews, there is a hidden "Actual Qualification Roster" H, which is one of the following {num_candidates} candidate rosters:

{candidates_desc}

Concurrent surgeries (matching) refers to a schedule where no two surgeries share the same expert or the same surgery room; the maximum number of concurrent surgeries is denoted as M.

Your goal is to deduce the Actual Qualification Roster H through probing and evaluate the hospital's maximum concurrent surgeries capacity M.

You can repeatedly submit the following two types of scheduling queries (one per turn), and the system will respond truthfully:

1. Scheduling Probe (Probe):
   - Submit a proposal set P, satisfying: for each expert u in U, the number of surgery rooms requested by u in P must be 1 or 2 (can request different rooms; different experts can request the same room).
   - Answer: Returns an integer K representing the maximum number of concurrent surgeries successfully supported by the intersection of H and P, without revealing the specific scheduling details.

2. Roster Check (Identity check):
   - Ask "Is H equal to candidate roster X?" (X can be any of {candidate_names})
   - Answer: "Yes" or "No".

When you have gathered enough information, submit your final answer. If the answer is incorrect or improperly formatted, the scheduling deduction fails.

Each query must contain only one tag. Use the following XML format:

- Scheduling Probe (e.g., proposing pairings (A,1),(A,2),(B,2),(C,3),(D,3)):
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- Roster Check (e.g., asking if it is candidate alpha):
<identity>alpha</identity>

When submitting the final answer, specify which candidate roster it is and its maximum concurrent surgeries capacity M, using this format:
<answer>graph=alpha, M=3</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“科研导师双向选择推演”系统。

本期学术互选包含了高级导师集合：U = {{A, B, C, D}} 和科研课题集合：V = {{1, 2, 3, 4}}。
系统后台已生成了一份基于研究方向的“实际学术契合度矩阵”H，它是以下{num_candidates}个候选矩阵之一：

{candidates_desc}

独立指导配对（匹配）是指配对的集合，确保每位导师仅负责一个课题，且每个课题仅由一位导师指导；全院最大可行的独立指导配对数记为M。

你的目标是通过探测推断出实际学术契合度矩阵H，并给出当前的最大独立指导配对数M。

你可以反复向系统提交以下两类操作（每次仅限一个），系统将如实反馈：

1. 意向投递方案（Probe）：
   - 提交一个意向集P，需满足：对U中的每位导师u，在P中u选择的课题数为1或2个（可选择不同课题；不同导师也可选择同一课题）。
   - 回答：返回一个整数K，表示实际矩阵H与投递方案P交集下，能够达成的最大独立指导配对数，但不公开具体的录用名单。

2. 矩阵确认（Identity check）：
   - 询问"H是否等于候选矩阵X？"（X可以是{candidate_names}中的任一个）
   - 回答："是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，推演失败。

每次交互只能包含一个标签。请使用以下XML格式：

- 意向投递（例如提交选择 (A,1),(A,2),(B,2),(C,3),(D,3)）：
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- 矩阵确认（例如询问是否为候选alpha）：
<identity>alpha</identity>

提交最终答案时，必须说明实际矩阵是哪个候选以及其最大独立指导配对数M，格式如下：
<answer>graph=alpha, M=3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Academic Mentorship Bidirectional Selection Deduction" system.

This semester's matching includes a set of Senior Tutors: U = {{A, B, C, D}} and a set of Research Projects: V = {{1, 2, 3, 4}}.
The system background has generated an "Actual Academic Compatibility Matrix" H based on research directions, which is one of the following {num_candidates} candidate matrices:

{candidates_desc}

Exclusive mentorship pairings (matching) refer to a set of pairs ensuring each tutor is responsible for only one project, and each project is guided by only one tutor; the maximum feasible exclusive mentorship pairings for the institution is denoted as M.

Your goal is to deduce the Actual Academic Compatibility Matrix H through probing and provide the maximum exclusive mentorship capacity M.

You can repeatedly submit the following two types of queries (one per turn), and the system will respond truthfully:

1. Intent Submission Probe (Probe):
   - Submit an intent set P, satisfying: for each tutor u in U, the number of projects selected by u in P must be 1 or 2 (can select different projects; different tutors can select the same project).
   - Answer: Returns an integer K representing the maximum number of exclusive mentorship pairings successfully formed by the intersection of H and P, without revealing the specific admission list.

2. Matrix Check (Identity check):
   - Ask "Is H equal to candidate matrix X?" (X can be any of {candidate_names})
   - Answer: "Yes" or "No".

When you have gathered enough information, submit your final answer. If the answer is incorrect or improperly formatted, the deduction fails.

Each query must contain only one tag. Use the following XML format:

- Intent Submission (e.g., submitting choices (A,1),(A,2),(B,2),(C,3),(D,3)):
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- Matrix Check (e.g., asking if it is candidate alpha):
<identity>alpha</identity>

When submitting the final answer, specify which candidate matrix it is and its maximum exclusive mentorship pairings M, using this format:
<answer>graph=alpha, M=3</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“柔性制造连线规划推演”系统。

车间内包含自动化加工单元集合：U = {{A, B, C, D}} 和产品装配线集合：V = {{1, 2, 3, 4}}。
经过一轮固件升级，系统目前存在一个未知的“实际硬件兼容拓扑”H，它是以下{num_candidates}个候选拓扑之一：

{candidates_desc}

并行生产流水线（匹配）是指设备连线的集合，要求任意两套流水线不得复用同一个加工单元或装配线；车间最大并行生产流水线数量记为M。

你的目标是通过探测推断出实际硬件兼容拓扑H，并计算出当前的全局最大并行生产流水线数量M。

你可以反复向系统提交以下两类诊断指令（每次仅限一个），系统将如实反馈：

1. 工艺连线测试（Probe）：
   - 提交一个物理连线集P，需满足：对U中的每个加工单元u，在P中分配的装配线目标数为1或2条（可连接不同装配线；不同单元也可指向同一装配线）。
   - 回答：返回一个整数K，表示实际兼容拓扑H与连线测试P交集下，能够成功点亮的最大并行生产流水线数，但不输出具体的连线日志。

2. 拓扑确认（Identity check）：
   - 询问"H是否等于候选拓扑X？"（X可以是{candidate_names}中的任一个）
   - 回答："是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，规划推演失败。

每次交互只能包含一个标签。请使用以下XML格式：

- 工艺连线测试（例如测试连线 (A,1),(A,2),(B,2),(C,3),(D,3)）：
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- 拓扑确认（例如询问是否为候选alpha）：
<identity>alpha</identity>

提交最终答案时，必须说明实际拓扑是哪个候选以及其最大并行生产流水线数量M，格式如下：
<answer>graph=alpha, M=3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Flexible Manufacturing Linkage Deduction" system.

The workshop contains a set of Automated Processing Units: U = {{A, B, C, D}} and a set of Product Assembly Lines: V = {{1, 2, 3, 4}}.
Following a firmware upgrade, there is an unknown "Actual Hardware Compatibility Topology" H, which is one of the following {num_candidates} candidate topologies:

{candidates_desc}

Parallel production streams (matching) refer to a set of equipment linkages ensuring no two streams reuse the same processing unit or assembly line; the workshop's maximum number of parallel production streams is denoted as M.

Your goal is to deduce the Actual Hardware Compatibility Topology H through probing and calculate the global maximum parallel production streams M.

You can repeatedly submit the following two types of diagnostic queries (one per turn), and the system will respond truthfully:

1. Process Linkage Probe (Probe):
   - Submit a physical linkage set P, satisfying: for each processing unit u in U, the number of targeted assembly lines in P must be 1 or 2 (can link to different lines; different units can point to the same line).
   - Answer: Returns an integer K representing the maximum number of parallel production streams successfully activated by the intersection of H and P, without outputting the specific linkage logs.

2. Topology Check (Identity check):
   - Ask "Is H equal to candidate topology X?" (X can be any of {candidate_names})
   - Answer: "Yes" or "No".

When you have gathered enough information, submit your final answer. If the answer is incorrect or improperly formatted, the planning deduction fails.

Each query must contain only one tag. Use the following XML format:

- Process Linkage Probe (e.g., testing links (A,1),(A,2),(B,2),(C,3),(D,3)):
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- Topology Check (e.g., asking if it is candidate alpha):
<identity>alpha</identity>

When submitting the final answer, specify which candidate topology it is and its maximum parallel production streams M, using this format:
<answer>graph=alpha, M=3</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“律所案件代理冲突审查”系统。

本机构当前拥有高级诉讼律师集合：U = {{A, B, C, D}} 和复杂案件组集合：V = {{1, 2, 3, 4}}。
基于最新的客户利益冲突隔离墙机制，系统内维持着一份“无利益冲突授权表”H，它是以下{num_candidates}种候选授权表之一：

{candidates_desc}

并发独立代理（匹配）是指律师接案的集合，要求任意两起案件代理互不干扰，即每位律师至多处理一个案件组，且每个案件组仅由一位律师主导；全局最大并发独立代理数记为M。

你的目标是通过探测推断出实际的无利益冲突授权表H，并评估当前的最大并发独立代理数M。

你可以反复向系统提交以下两类审查指令（每次仅限一个），系统将如实反馈：

1. 利益冲突审查批次（Probe）：
   - 提交一个提名集P，需满足：对U中的每位律师u，在P中提名的案件组数量为1或2个（可提名不同案件组；不同律师也可提名同一案件组）。
   - 回答：返回一个整数K，表示在实际授权表H与提名集P的交集中，合规通过审查的最大并发独立代理数，但不输出具体的代理指派明细。

2. 授权表确认（Identity check）：
   - 询问"H是否等于候选授权表X？"（X可以是{candidate_names}中的任一个）
   - 回答："是"或"否"。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，审查系统将锁定失败。

每次交互只能包含一个标签。请使用以下XML格式：

- 冲突审查批次（例如提名 (A,1),(A,2),(B,2),(C,3),(D,3)）：
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- 授权表确认（例如询问是否为候选alpha）：
<identity>alpha</identity>

提交最终答案时，必须说明实际授权表是哪个候选以及其最大并发独立代理数M，格式如下：
<answer>graph=alpha, M=3</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the "Law Firm Case Representation Conflict Check" system.

Our institution currently has a set of Senior Litigators: U = {{A, B, C, D}} and a set of Complex Case Portfolios: V = {{1, 2, 3, 4}}.
Based on the latest client conflict-of-interest firewall mechanisms, the system maintains a "Conflict-Free Clearance Roster" H, which is one of the following {num_candidates} candidate rosters:

{candidates_desc}

Simultaneous independent representations (matching) refers to a set of case assignments ensuring no interference, meaning each lawyer handles at most one case portfolio, and each portfolio is led by only one lawyer; the global maximum simultaneous independent representations is denoted as M.

Your goal is to deduce the actual Conflict-Free Clearance Roster H through probing and evaluate the current maximum simultaneous independent representations M.

You can repeatedly submit the following two types of clearance queries (one per turn), and the system will respond truthfully:

1. Conflict Check Batch (Probe):
   - Submit a nomination set P, satisfying: for each lawyer u in U, the number of case portfolios nominated by u in P must be 1 or 2 (can nominate different portfolios; different lawyers can nominate the same portfolio).
   - Answer: Returns an integer K representing the maximum number of simultaneous independent representations successfully passing clearance within the intersection of H and P, without detailing the specific representative assignments.

2. Roster Check (Identity check):
   - Ask "Is H equal to candidate roster X?" (X can be any of {candidate_names})
   - Answer: "Yes" or "No".

When you have gathered enough information, submit your final answer. If the answer is incorrect or improperly formatted, the clearance system will lock out and fail.

Each query must contain only one tag. Use the following XML format:

- Conflict Check Batch (e.g., nominating (A,1),(A,2),(B,2),(C,3),(D,3)):
<probe>(A,1),(A,2),(B,2),(C,3),(D,3)</probe>

- Roster Check (e.g., asking if it is candidate alpha):
<identity>alpha</identity>

When submitting the final answer, specify which candidate roster it is and its maximum simultaneous independent representations M, using this format:
<answer>graph=alpha, M=3</answer>
"""

    tags = ["answer", "probe", "identity"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "candidates": {
                    "alpha": [("A", "1"), ("A", "2"), ("B", "2"), ("C", "2"), ("C", "3"), ("D", "3")],
                    "beta": [("A", "1"), ("B", "1"), ("B", "2"), ("C", "3"), ("D", "3"), ("D", "4")],
                    "gamma": [("A", "1"), ("A", "4"), ("B", "2"), ("C", "2"), ("C", "3"), ("D", "3")],
                    "delta": [("A", "1"), ("A", "2"), ("B", "2"), ("B", "3"), ("C", "3"), ("D", "4")],
                },
                "hidden": "alpha",
            },
            2: {
                "candidates": {
                    "alpha": [("A", "1"), ("B", "2"), ("C", "3"), ("D", "4")],
                    "beta": [("A", "1"), ("A", "2"), ("B", "3"), ("C", "4"), ("D", "2")],
                    "gamma": [("A", "2"), ("B", "1"), ("C", "3"), ("D", "4")],
                    "delta": [("A", "1"), ("B", "2"), ("C", "2"), ("C", "4"), ("D", "3")],
                },
                "hidden": "beta",
            },
            3: {
                "candidates": {
                    "alpha": [("A", "1"), ("A", "2"), ("B", "2"), ("C", "3"), ("D", "4")],
                    "beta": [("A", "1"), ("B", "2"), ("B", "3"), ("C", "3"), ("D", "4")],
                    "gamma": [("A", "1"), ("A", "2"), ("B", "3"), ("C", "2"), ("D", "4")],
                    "delta": [("A", "1"), ("B", "1"), ("B", "2"), ("C", "3"), ("D", "4")],
                    "epsilon": [("A", "2"), ("B", "2"), ("B", "3"), ("C", "1"), ("D", "4")],
                },
                "hidden": "gamma",
            },
            4: {
                "candidates": {
                    "alpha": [("A", "1"), ("A", "2"), ("B", "2"), ("B", "3"), ("C", "3"), ("D", "4")],
                    "beta": [("A", "1"), ("A", "2"), ("B", "2"), ("C", "3"), ("C", "4"), ("D", "4")],
                    "gamma": [("A", "1"), ("A", "2"), ("B", "3"), ("C", "2"), ("C", "3"), ("D", "4")],
                    "delta": [("A", "1"), ("B", "2"), ("B", "3"), ("C", "2"), ("C", "3"), ("D", "4")],
                    "epsilon": [("A", "1"), ("A", "2"), ("B", "2"), ("B", "4"), ("C", "3"), ("D", "3")],
                },
                "hidden": "delta",
            },
            5: {
                "candidates": {
                    "alpha": [("A", "1"), ("A", "2"), ("B", "2"), ("B", "3"), ("C", "3"), ("C", "4"), ("D", "4")],
                    "beta": [("A", "1"), ("A", "2"), ("B", "2"), ("B", "4"), ("C", "3"), ("C", "4"), ("D", "3")],
                    "gamma": [("A", "1"), ("A", "3"), ("B", "2"), ("B", "3"), ("C", "2"), ("C", "4"), ("D", "4")],
                    "delta": [("A", "1"), ("A", "2"), ("B", "3"), ("B", "4"), ("C", "2"), ("C", "3"), ("D", "4")],
                    "epsilon": [("A", "1"), ("A", "4"), ("B", "2"), ("B", "3"), ("C", "2"), ("C", "4"), ("D", "3")],
                    "zeta": [("A", "2"), ("A", "3"), ("B", "1"), ("B", "3"), ("C", "2"), ("C", "4"), ("D", "4")],
                },
                "hidden": "epsilon",
            },
        },
        "en": {
            1: {
                "candidates": {
                    "alpha": [("A", "1"), ("A", "2"), ("B", "2"), ("C", "2"), ("C", "3"), ("D", "3")],
                    "beta": [("A", "1"), ("B", "1"), ("B", "2"), ("C", "3"), ("D", "3"), ("D", "4")],
                    "gamma": [("A", "1"), ("A", "4"), ("B", "2"), ("C", "2"), ("C", "3"), ("D", "3")],
                    "delta": [("A", "1"), ("A", "2"), ("B", "2"), ("B", "3"), ("C", "3"), ("D", "4")],
                },
                "hidden": "alpha",
            },
            2: {
                "candidates": {
                    "alpha": [("A", "1"), ("B", "2"), ("C", "3"), ("D", "4")],
                    "beta": [("A", "1"), ("A", "2"), ("B", "3"), ("C", "4"), ("D", "2")],
                    "gamma": [("A", "2"), ("B", "1"), ("C", "3"), ("D", "4")],
                    "delta": [("A", "1"), ("B", "2"), ("C", "2"), ("C", "4"), ("D", "3")],
                },
                "hidden": "beta",
            },
            3: {
                "candidates": {
                    "alpha": [("A", "1"), ("A", "2"), ("B", "2"), ("C", "3"), ("D", "4")],
                    "beta": [("A", "1"), ("B", "2"), ("B", "3"), ("C", "3"), ("D", "4")],
                    "gamma": [("A", "1"), ("A", "2"), ("B", "3"), ("C", "2"), ("D", "4")],
                    "delta": [("A", "1"), ("B", "1"), ("B", "2"), ("C", "3"), ("D", "4")],
                    "epsilon": [("A", "2"), ("B", "2"), ("B", "3"), ("C", "1"), ("D", "4")],
                },
                "hidden": "gamma",
            },
            4: {
                "candidates": {
                    "alpha": [("A", "1"), ("A", "2"), ("B", "2"), ("B", "3"), ("C", "3"), ("D", "4")],
                    "beta": [("A", "1"), ("A", "2"), ("B", "2"), ("C", "3"), ("C", "4"), ("D", "4")],
                    "gamma": [("A", "1"), ("A", "2"), ("B", "3"), ("C", "2"), ("C", "3"), ("D", "4")],
                    "delta": [("A", "1"), ("B", "2"), ("B", "3"), ("C", "2"), ("C", "3"), ("D", "4")],
                    "epsilon": [("A", "1"), ("A", "2"), ("B", "2"), ("B", "4"), ("C", "3"), ("D", "3")],
                },
                "hidden": "delta",
            },
            5: {
                "candidates": {
                    "alpha": [("A", "1"), ("A", "2"), ("B", "2"), ("B", "3"), ("C", "3"), ("C", "4"), ("D", "4")],
                    "beta": [("A", "1"), ("A", "2"), ("B", "2"), ("B", "4"), ("C", "3"), ("C", "4"), ("D", "3")],
                    "gamma": [("A", "1"), ("A", "3"), ("B", "2"), ("B", "3"), ("C", "2"), ("C", "4"), ("D", "4")],
                    "delta": [("A", "1"), ("A", "2"), ("B", "3"), ("B", "4"), ("C", "2"), ("C", "3"), ("D", "4")],
                    "epsilon": [("A", "1"), ("A", "4"), ("B", "2"), ("B", "3"), ("C", "2"), ("C", "4"), ("D", "3")],
                    "zeta": [("A", "2"), ("A", "3"), ("B", "1"), ("B", "3"), ("C", "2"), ("C", "4"), ("D", "4")],
                },
                "hidden": "epsilon",
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
        
        self.candidates = cfg["candidates"]
        self.hidden_graph_name = cfg["hidden"]
        self.hidden_graph = set(cfg["candidates"][cfg["hidden"]])
        
        self.max_matching_size = self._compute_max_matching(self.hidden_graph)
        
        self.candidate_matching_sizes = {}
        for name, edges in self.candidates.items():
            self.candidate_matching_sizes[name] = self._compute_max_matching(set(edges))
        
        self._game_info["num_candidates"] = len(self.candidates)
        self._game_info["candidate_names"] = ", ".join(self.candidates.keys())
        
        candidates_desc_lines = []
        for name, edges in self.candidates.items():
            edges_str = ", ".join([f"({u},{v})" for u, v in edges])
            if lang == "zh":
                candidates_desc_lines.append(f"- 候选{name}：{{{edges_str}}}")
            else:
                candidates_desc_lines.append(f"- Candidate {name}: {{{edges_str}}}")
        self._game_info["candidates_desc"] = "\n".join(candidates_desc_lines)

    def _compute_max_matching(self, edges):
        edges_set = set(edges)
        u_match = {}
        v_match = {}
        
        def find_augmenting_path(u, visited):
            for edge in edges_set:
                if edge[0] != u:
                    continue
                v = edge[1]
                if v in visited:
                    continue
                visited.add(v)
                
                if v not in v_match or find_augmenting_path(v_match[v], visited):
                    u_match[u] = v
                    v_match[v] = u
                    return True
            return False
        
        u_vertices = set(edge[0] for edge in edges_set)
        for u in sorted(u_vertices):
            visited = set()
            find_augmenting_path(u, visited)
        
        return len(u_match)

    def _parse_edge_set(self, edge_str):
        edges = set()
        pattern = r'\(\s*([A-D])\s*,\s*([1-4])\s*\)'
        matches = re.findall(pattern, edge_str)
        for u, v in matches:
            edges.add((u, v))
        return edges

    def _validate_probe(self, edges):
        u_vertices = ["A", "B", "C", "D"]
        for u in u_vertices:
            count = sum(1 for edge in edges if edge[0] == u)
            if count < 1 or count > 2:
                return False
        return True

    def evaluate(self, parsed_info):
        raw_ans = parsed_info.get("answer", "")
        
        try:
            kv_pairs = raw_ans.split(",")
            ans_dict = {}
            for kv in kv_pairs:
                if "=" in kv:
                    k, v = kv.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if "graph" not in ans_dict or "M" not in ans_dict:
                return False
            
            if ans_dict["graph"] != self.hidden_graph_name:
                return False
            
            try:
                m_value = int(ans_dict["M"])
            except:
                return False
                
            return m_value == self.max_matching_size
            
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效。"
            error_constraint = "错误：边集不满足约束条件。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format."
            error_constraint = "Error: Edge set does not satisfy constraints."

        if "probe" in parsed_info:
            try:
                probe_str = parsed_info["probe"].strip()
                edges = self._parse_edge_set(probe_str)
                
                if not edges:
                    return error_format
                
                if not self._validate_probe(edges):
                    return error_constraint
                
                intersection = self.hidden_graph & edges
                matching_size = self._compute_max_matching(intersection)
                
                return str(matching_size)
                
            except:
                return error_format

        elif "identity" in parsed_info:
            try:
                candidate_name = parsed_info["identity"].strip()
                if candidate_name not in self.candidates:
                    return error_format
                
                return yes_res if candidate_name == self.hidden_graph_name else no_res
                
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            if correct == "否":
                return "是"
        else:
            if correct.lower() == "yes":
                return "No" if correct[0].isupper() else "no"
            if correct.lower() == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> List[Dict[str, str]]:
        results = []

        yes_res = "是" if self.config.language == "zh" else "Yes"
        no_res = "否" if self.config.language == "zh" else "No"

        for name in self.candidates:
            query_xml = f"<identity>{name}</identity>"
            ans = yes_res if name == self.hidden_graph_name else no_res
            results.append({
                "query": query_xml,
                "answer": ans
            })

        
        u_nodes = ["A", "B", "C", "D"]
        v_nodes = ["1", "2", "3", "4"]
        
        node_choices = []
        for u in u_nodes:
            choices = []
            for v in v_nodes:
                choices.append( [(u, v)] )
            node_choices.append(choices)
            
        for choice_tuple in itertools.product(*node_choices):
            all_edges = []
            for c in choice_tuple:
                all_edges.extend(c)
            
            edge_strs = [f"({u},{v})" for u, v in all_edges]
            probe_content = ",".join(edge_strs)
            query_xml = f"<probe>{probe_content}</probe>"
            
            probe_set = set(all_edges)
            intersection = self.hidden_graph & probe_set
            
            m_size = self._compute_max_matching(intersection)
            
            results.append({
                "query": query_xml,
                "answer": str(m_size)
            })
            
        return results