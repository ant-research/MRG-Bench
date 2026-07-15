from .base import Game
import re

class HiddenGraphPathGame(Game):
    
    reasoning_type = "归纳推理"
    data_structure = "图"

    game_rule_zh = """\
我们现在来玩一个"隐藏图路径"推理游戏，规则如下：

游戏设定了一个有序节点集合 1 到 {n}，其中起点为 {s}，终点为 {t}。我已秘密选定了一个差值集合 R，R 是 1 到 {n_minus_1} 之间某些整数的集合。对于任意两个节点 i 和 j（其中 i 小于 j），当且仅当它们的差值（j 减 i）属于 R 时，存在一条从 i 到 j 的有向边；否则不存在该边。保证从起点到终点至少存在一条路径。

你的目标是：
1. 推断出差值集合 R（集合中的所有元素）
2. 枚举出从起点 {s} 到终点 {t} 的所有简单路径

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 边查询：询问节点 a 到节点 b 是否存在有向边（要求 a 小于 b）。回答"是"或"否"。
2. 路径验证查询：提交一个严格递增的节点序列，我会验证该序列是否构成有效路径。
   - 如果序列不是严格递增的，返回"非法"
   - 如果序列是有效路径，返回"成功"
   - 如果序列中存在无效边，返回"失败"以及第一个无效边的位置

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏继续。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 边查询（例如询问节点 2 到节点 5 是否有边）：
<query_edge>2,5</query_edge>

- 路径验证查询（例如验证路径 1->3->5->7）：
<query_path>1,3,5,7</query_path>

提交最终答案时，必须包含差值集合 R 和所有路径。格式如下：

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

答案格式说明：
- 第一行：R= 后跟差值集合的所有元素（升序排列，逗号分隔）
- 第二行：paths= 后跟路径总数
- 后续每行：一条从起点到终点的完整路径（节点用逗号分隔）
- 路径建议按长度从短到长排列，相同长度的按字典序排列

请尽可能少地使用查询次数来完成任务。
"""

    game_rule_en = """\
Let's play a "Hidden Graph Path" deduction game. Here are the rules:

The game has an ordered set of nodes from 1 to {n}, with start node {s} and end node {t}. I have secretly selected a difference set R, which is a subset of integers from 1 to {n_minus_1}. For any two nodes i and j (where i is less than j), there exists a directed edge from i to j if and only if their difference (j minus i) belongs to R; otherwise, no such edge exists. It is guaranteed that at least one path exists from the start to the end node.

Your goal is to:
1. Infer the difference set R (all elements in the set)
2. Enumerate all simple paths from start node {s} to end node {t}

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully:

1. Edge Query: Ask if there is a directed edge from node a to node b (where a is less than b). Answer "Yes" or "No".
2. Path Verification Query: Submit a strictly increasing sequence of nodes, and I will verify if it forms a valid path.
   - If the sequence is not strictly increasing, return "Invalid"
   - If the sequence forms a valid path, return "Success"
   - If there is an invalid edge in the sequence, return "Failed" along with the position of the first invalid edge

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game continues.

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., asking if there is an edge from node 2 to node 5):
<query_edge>2,5</query_edge>

- Path Verification Query (e.g., verifying path 1->3->5->7):
<query_path>1,3,5,7</query_path>

When submitting the final answer, you must include the difference set R and all paths. Format:

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

Answer format explanation:
- First line: R= followed by all elements in the difference set (in ascending order, comma-separated)
- Second line: paths= followed by the total number of paths
- Subsequent lines: Each line contains one complete path from start to end (nodes comma-separated)
- Paths should be sorted by length (shorter first), and within the same length, by lexicographic order

Please use as few queries as possible to complete the task.
"""

    contextualized_rule_zh_1 = """\
我们现在进入"高速路网规划"管理系统，规则如下：

系统设定了一系列按线路顺序排列的高速收费站节点 1 到 {n}，其中起点站为 {s}，终点站为 {t}。交通局秘密设定了一个合规的站间跨距集合 R，R 是 1 到 {n_minus_1} 之间某些整数的集合。对于任意两个收费站 i 和 j（其中 i 小于 j），当且仅当它们的编号差值（j 减 i）属于 R 时，才允许修建一条从 i 到 j 的单向直达快速通道；否则不允许修建。保证从起点站到终点站至少存在一条完整路线。

你的目标是：
1. 推断出合规的跨距集合 R（集合中的所有元素）
2. 枚举出从起点站 {s} 到终点站 {t} 的所有直达行驶路线

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 通道查询：询问收费站 a 到收费站 b 是否修建了直达通道（要求 a 小于 b）。回答"是"或"否"。
2. 路线验证查询：提交一个严格递增的收费站序列，我会验证该序列是否构成合法路线。
   - 如果序列不是严格递增的，返回"非法"
   - 如果序列是合法路线，返回"成功"
   - 如果序列中存在未连接的通道，返回"失败"以及第一个无效通道的位置

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，系统将驳回并继续。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 通道查询（例如询问收费站 2 到收费站 5 是否有直达通道）：
<query_edge>2,5</query_edge>

- 路线验证查询（例如验证路线 1->3->5->7）：
<query_path>1,3,5,7</query_path>

提交最终答案时，必须包含跨距集合 R 和所有路线。格式如下：

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

答案格式说明：
- 第一行：R= 后跟集合的所有元素（升序排列，逗号分隔）
- 第二行：paths= 后跟路线总数
- 后续每行：一条从起点站到终点站的完整路线（节点用逗号分隔）
- 路线建议按长度从短到长排列，相同长度的按字典序排列

请尽可能少地使用查询次数来完成规划任务。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's access the "Highway Network Planning" deduction system. The rules are as follows:

The system sets an ordered series of toll station nodes from 1 to {n}, with the starting station {s} and the terminal station {t}. The traffic bureau has secretly established a compliant inter-station distance set R, which is a subset of integers from 1 to {n_minus_1}. For any two toll stations i and j (where i is less than j), a one-way direct express channel exists from i to j if and only if their index difference (j minus i) belongs to R; otherwise, it is prohibited. It is guaranteed that at least one complete route exists from the starting station to the terminal.

Your goal is to:
1. Infer the compliant distance set R (all elements in the set)
2. Enumerate all direct express driving routes from start station {s} to terminal station {t}

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully:

1. Channel Query: Ask if a direct channel is built from station a to station b (where a is less than b). Answer "Yes" or "No".
2. Route Verification Query: Submit a strictly increasing sequence of toll stations, and I will verify if it forms a valid route.
   - If the sequence is not strictly increasing, return "Invalid"
   - If the sequence forms a valid route, return "Success"
   - If there is an unconnected channel in the sequence, return "Failed" along with the position of the first invalid channel

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the system continues.

Each query must contain only one tag. Use the following XML format:

- Channel Query (e.g., asking if there is a channel from station 2 to station 5):
<query_edge>2,5</query_edge>

- Route Verification Query (e.g., verifying route 1->3->5->7):
<query_path>1,3,5,7</query_path>

When submitting the final answer, you must include the distance set R and all routes. Format:

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

Answer format explanation:
- First line: R= followed by all elements in the set (in ascending order, comma-separated)
- Second line: paths= followed by the total number of routes
- Subsequent lines: Each line contains one complete route from start to terminal (nodes comma-separated)
- Routes should be sorted by length (shorter first), and within the same length, by lexicographic order

Please use as few queries as possible to complete the planning task.
"""

    contextualized_rule_zh_2 = """\
我们现在进入"康复治疗方案"规划系统，规则如下：

系统设定了从初级到完全康复的有序评估阶段 1 到 {n}，其中初始阶段为 {s}，最终康复阶段为 {t}。医疗指南秘密规定了一个合法的跨越治疗周期集合 R，R 是 1 到 {n_minus_1} 之间某些整数的集合。对于任意两个评估阶段 i 和 j（其中 i 小于 j），当且仅当它们的阶段差值（j 减 i）属于 R 时，临床允许患者从阶段 i 直接跃升进行阶段 j 的治疗；否则不允许。保证从初始阶段到最终康复至少存在一条合规的康复路径。

你的目标是：
1. 推断出合法的治疗跨度集合 R（集合中的所有元素）
2. 枚举出从初始阶段 {s} 到最终康复阶段 {t} 的所有合规康复路径

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 跃升查询：询问是否允许从阶段 a 直接跃升治疗阶段 b（要求 a 小于 b）。回答"是"或"否"。
2. 治疗方案验证查询：提交一个严格递增的治疗阶段序列，我会验证该序列是否构成合规方案。
   - 如果序列不是严格递增的，返回"非法"
   - 如果序列是合规方案，返回"成功"
   - 如果序列中存在违规的阶段跨越，返回"失败"以及第一个无效跨越的位置

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，评估将继续。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 跃升查询（例如询问能否从阶段 2 直接跃升至阶段 5）：
<query_edge>2,5</query_edge>

- 治疗方案验证查询（例如验证治疗方案 1->3->5->7）：
<query_path>1,3,5,7</query_path>

提交最终答案时，必须包含跨度集合 R 和所有康复路径。格式如下：

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

答案格式说明：
- 第一行：R= 后跟跨度集合的所有元素（升序排列，逗号分隔）
- 第二行：paths= 后跟路径总数
- 后续每行：一条从初始阶段到最终阶段的完整治疗路径（节点用逗号分隔）
- 路径建议按疗程长度从短到长排列，相同长度的按字典序排列

请尽可能少地使用查询次数来完成规划任务。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's access the "Rehabilitation Protocol" planning system. The rules are as follows:

The system sets an ordered series of evaluation stages from 1 to {n}, with the initial stage being {s} and the full recovery stage being {t}. The clinical guidelines have secretly established a compliant clinical jump span set R, which is a subset of integers from 1 to {n_minus_1}. For any two evaluation stages i and j (where i is less than j), the clinical guidelines permit a direct jump from stage i to stage j for treatment if and only if their stage difference (j minus i) belongs to R; otherwise, it is prohibited. It is guaranteed that at least one compliant rehabilitation protocol exists from the initial stage to full recovery.

Your goal is to:
1. Infer the compliant jump span set R (all elements in the set)
2. Enumerate all direct jump treatment protocols from initial stage {s} to full recovery stage {t}

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully:

1. Jump Query: Ask if it is permitted to directly jump from stage a to stage b (where a is less than b). Answer "Yes" or "No".
2. Protocol Verification Query: Submit a strictly increasing sequence of stages, and I will verify if it forms a compliant protocol.
   - If the sequence is not strictly increasing, return "Invalid"
   - If the sequence forms a compliant protocol, return "Success"
   - If there is an unpermitted jump in the sequence, return "Failed" along with the position of the first invalid jump

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the assessment continues.

Each query must contain only one tag. Use the following XML format:

- Jump Query (e.g., asking if a jump from stage 2 to stage 5 is allowed):
<query_edge>2,5</query_edge>

- Protocol Verification Query (e.g., verifying protocol 1->3->5->7):
<query_path>1,3,5,7</query_path>

When submitting the final answer, you must include the jump span set R and all protocols. Format:

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

Answer format explanation:
- First line: R= followed by all elements in the span set (in ascending order, comma-separated)
- Second line: paths= followed by the total number of protocols
- Subsequent lines: Each line contains one complete protocol from initial to full recovery (stages comma-separated)
- Protocols should be sorted by length (shorter first), and within the same length, by lexicographic order

Please use as few queries as possible to complete the planning task.
"""

    contextualized_rule_zh_3 = """\
我们现在进入"个性化选课"推荐系统，规则如下：

系统设定了具有严格进阶顺序的课程模块 1 到 {n}，其中基础模块为 {s}，结业模块为 {t}。学术委员会秘密设定了一个允许的跳级跨度集合 R，R 是 1 到 {n_minus_1} 之间某些整数的集合。对于任意两个课程模块 i 和 j（其中 i 小于 j），当且仅当它们的层级差值（j 减 i）属于 R 时，系统允许学生修完模块 i 后直接解锁模块 j；否则不允许跨级。保证从基础模块到结业模块至少存在一条完整的修读路径。

你的目标是：
1. 推断出学术委员会批准的跳级跨度集合 R（集合中的所有元素）
2. 枚举出从基础模块 {s} 到结业模块 {t} 的所有有效选课路线

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 解锁查询：询问修完模块 a 后能否直接解锁选修模块 b（要求 a 小于 b）。回答"是"或"否"。
2. 选课路线验证查询：提交一个严格递增的模块序列，我会验证该序列是否构成有效选课路线。
   - 如果序列不是严格递增的，返回"非法"
   - 如果序列是有效选课路线，返回"成功"
   - 如果序列中存在无法直接解锁的模块跨越，返回"失败"以及第一个无效跨越的位置

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，选课指导继续。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 解锁查询（例如询问修完模块 2 后能否直接解锁模块 5）：
<query_edge>2,5</query_edge>

- 选课路线验证查询（例如验证选课路线 1->3->5->7）：
<query_path>1,3,5,7</query_path>

提交最终答案时，必须包含跳级跨度集合 R 和所有选课路线。格式如下：

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

答案格式说明：
- 第一行：R= 后跟跨度集合的所有元素（升序排列，逗号分隔）
- 第二行：paths= 后跟选课路线总数
- 后续每行：一条从基础到结业的完整选课路线（模块编号用逗号分隔）
- 路线建议按模块数量从少到多排列，相同数量的按字典序排列

请尽可能少地使用查询次数来完成推荐任务。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's access the "Personalized Course Selection" recommendation system. The rules are as follows:

The system sets an ordered series of course modules from 1 to {n}, with the foundation module {s} and graduation module {t}. The academic committee has secretly set an allowed skip span set R, which is a subset of integers from 1 to {n_minus_1}. For any two course modules i and j (where i is less than j), the system allows a student to unlock module j directly after finishing module i if and only if their tier difference (j minus i) belongs to R; otherwise, skipping is not allowed. It is guaranteed that at least one complete study route exists from the foundation to graduation.

Your goal is to:
1. Infer the allowed skip span set R (all elements in the set)
2. Enumerate all valid study routes from foundation module {s} to graduation module {t}

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully:

1. Unlock Query: Ask if module b can be directly unlocked after finishing module a (where a is less than b). Answer "Yes" or "No".
2. Route Verification Query: Submit a strictly increasing sequence of modules, and I will verify if it forms a valid study route.
   - If the sequence is not strictly increasing, return "Invalid"
   - If the sequence forms a valid route, return "Success"
   - If there is an invalid module skip in the sequence, return "Failed" along with the position of the first invalid skip

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the advising continues.

Each query must contain only one tag. Use the following XML format:

- Unlock Query (e.g., asking if module 5 can be unlocked after module 2):
<query_edge>2,5</query_edge>

- Route Verification Query (e.g., verifying route 1->3->5->7):
<query_path>1,3,5,7</query_path>

When submitting the final answer, you must include the skip span set R and all valid routes. Format:

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

Answer format explanation:
- First line: R= followed by all elements in the span set (in ascending order, comma-separated)
- Second line: paths= followed by the total number of routes
- Subsequent lines: Each line contains one complete study route from foundation to graduation (modules comma-separated)
- Routes should be sorted by length (shorter first), and within the same length, by lexicographic order

Please use as few queries as possible to complete the recommendation task.
"""

    contextualized_rule_zh_4 = """\
我们现在进入"自动化流水线工艺"优化系统，规则如下：

系统设定了顺序排布的标准加工工位 1 到 {n}，其中原料投入工位为 {s}，成品产出工位为 {t}。控制系统秘密配置了一个支持的工序流转步长集合 R，R 是 1 到 {n_minus_1} 之间某些整数的集合。对于任意两个工位 i 和 j（其中 i 小于 j），当且仅当它们的序号差（j 减 i）属于 R 时，传送带机制才支持将物料从工位 i 直接传输至工位 j；否则无法直接传输。保证从原料投入到成品产出至少存在一条有效加工工艺路径。

你的目标是：
1. 推断出系统支持的流转步长集合 R（集合中的所有元素）
2. 枚举出从投入工位 {s} 到产出工位 {t} 的所有合规工艺流程路径

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 传输查询：询问工位 a 是否能将物料直接传输到工位 b（要求 a 小于 b）。回答"是"或"否"。
2. 工艺流程验证查询：提交一个严格递增的流转工位序列，我会验证该序列是否构成合规工艺流程。
   - 如果序列不是严格递增的，返回"非法"
   - 如果序列是合规流程，返回"成功"
   - 如果序列中存在不支持的传输步骤，返回"失败"以及第一个无效传输的位置

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，优化流程继续。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 传输查询（例如询问工位 2 能否直接传输到工位 5）：
<query_edge>2,5</query_edge>

- 工艺流程验证查询（例如验证工艺流程 1->3->5->7）：
<query_path>1,3,5,7</query_path>

提交最终答案时，必须包含步长集合 R 和所有工艺路径。格式如下：

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

答案格式说明：
- 第一行：R= 后跟步长集合的所有元素（升序排列，逗号分隔）
- 第二行：paths= 后跟路径总数
- 后续每行：一条从投入到产出的完整工艺路径（工位编号用逗号分隔）
- 路径建议按工序步骤从少到多排列，相同步骤数的按字典序排列

请尽可能少地使用查询次数来完成工艺优化。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's access the "Automated Assembly Line" optimization system. The rules are as follows:

The system sets an ordered series of processing stations from 1 to {n}, with the raw material input station {s} and the finished product output station {t}. The control system secretly configured a supported workflow stride length set R, which is a subset of integers from 1 to {n_minus_1}. For any two stations i and j (where i is less than j), the conveyor mechanism supports direct transfer of materials from station i to station j if and only if their index difference (j minus i) belongs to R; otherwise, direct transfer is unsupported. It is guaranteed that at least one valid processing workflow exists from input to output.

Your goal is to:
1. Infer the supported stride length set R (all elements in the set)
2. Enumerate all compliant assembly paths from input station {s} to output station {t}

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully:

1. Transfer Query: Ask if materials can be directly transferred from station a to station b (where a is less than b). Answer "Yes" or "No".
2. Workflow Verification Query: Submit a strictly increasing sequence of processing stations, and I will verify if it forms a compliant workflow.
   - If the sequence is not strictly increasing, return "Invalid"
   - If the sequence forms a compliant workflow, return "Success"
   - If there is an unsupported transfer step in the sequence, return "Failed" along with the position of the first invalid transfer

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the optimization continues.

Each query must contain only one tag. Use the following XML format:

- Transfer Query (e.g., asking if station 2 can transfer to station 5 directly):
<query_edge>2,5</query_edge>

- Workflow Verification Query (e.g., verifying workflow 1->3->5->7):
<query_path>1,3,5,7</query_path>

When submitting the final answer, you must include the stride length set R and all paths. Format:

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

Answer format explanation:
- First line: R= followed by all elements in the stride set (in ascending order, comma-separated)
- Second line: paths= followed by the total number of paths
- Subsequent lines: Each line contains one complete assembly path from input to output (stations comma-separated)
- Paths should be sorted by length (shorter first), and within the same length, by lexicographic order

Please use as few queries as possible to complete the optimization task.
"""

    contextualized_rule_zh_5 = """\
我们现在进入"司法诉讼程序"流转系统，规则如下：

系统设定了逐级递增的审理审批环节 1 到 {n}，其中立案环节为 {s}，判决生效环节为 {t}。诉讼法秘密规定了一个允许的程序越级层级集合 R，R 是 1 到 {n_minus_1} 之间某些整数的集合。对于任意两个环节 i 和 j（其中 i 小于 j），当且仅当它们的层级差值（j 减 i）属于 R 时，法律允许案件从环节 i 直接移交或上诉至环节 j；否则程序不合法。保证从立案到判决生效至少存在一条合法流转路径。

你的目标是：
1. 推断出合法的程序流转层级集合 R（集合中的所有元素）
2. 穷举出从立案环节 {s} 到判决生效环节 {t} 的所有合规司法流转路线

你可以反复向我提出以下两类查询（每次仅限一个查询），我会根据真实设定如实回答：

1. 移交查询：询问案件能否从环节 a 直接移交至环节 b（要求 a 小于 b）。回答"是"或"否"。
2. 诉讼程序验证查询：提交一个严格递增的审理环节序列，我会验证该上诉流程是否合法。
   - 如果序列不是严格递增的，返回"非法"
   - 如果序列是合法流程，返回"成功"
   - 如果序列中存在违规的程序跳跃，返回"失败"以及第一个无效移交的位置

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，案件审理退回补充侦查。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 移交查询（例如询问案件能否从环节 2 直接移交至环节 5）：
<query_edge>2,5</query_edge>

- 诉讼程序验证查询（例如验证审理流程 1->3->5->7）：
<query_path>1,3,5,7</query_path>

提交最终答案时，必须包含流转层级集合 R 和所有流转路线。格式如下：

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

答案格式说明：
- 第一行：R= 后跟层级集合的所有元素（升序排列，逗号分隔）
- 第二行：paths= 后跟路线总数
- 后续每行：一条从立案到结案的完整流转路线（环节编号用逗号分隔）
- 路线建议按环节数从少到多排列，相同环节数的按字典序排列

请尽可能少地使用查询次数来完成程序审查任务。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's access the "Judicial Litigation Process" routing system. The rules are as follows:

The system sets an ordered series of review phases from 1 to {n}, with the case filing phase {s} and the final judgment phase {t}. The procedural law secretly regulates a permitted procedural jump tier set R, which is a subset of integers from 1 to {n_minus_1}. For any two phases i and j (where i is less than j), the law allows direct transfer or appeal of a case from phase i to phase j if and only if their tier difference (j minus i) belongs to R; otherwise, the procedure is invalid. It is guaranteed that at least one compliant litigation route exists from case filing to final judgment.

Your goal is to:
1. Infer the permitted procedural jump tier set R (all elements in the set)
2. Enumerate all compliant judicial litigation routes from case filing phase {s} to final judgment phase {t}

You can repeatedly ask me two types of queries (one per turn), and I will answer truthfully:

1. Transfer Query: Ask if a case can be directly transferred from phase a to phase b (where a is less than b). Answer "Yes" or "No".
2. Litigation Route Verification Query: Submit a strictly increasing sequence of review phases, and I will verify if it forms a compliant litigation route.
   - If the sequence is not strictly increasing, return "Invalid"
   - If the sequence forms a compliant route, return "Success"
   - If there is an invalid procedural jump in the sequence, return "Failed" along with the position of the first invalid transfer

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the review continues.

Each query must contain only one tag. Use the following XML format:

- Transfer Query (e.g., asking if a case can transfer from phase 2 to phase 5 directly):
<query_edge>2,5</query_edge>

- Litigation Route Verification Query (e.g., verifying route 1->3->5->7):
<query_path>1,3,5,7</query_path>

When submitting the final answer, you must include the jump tier set R and all routes. Format:

<answer>
R=1,2,3
paths=5
{s},2,3,{t}
{s},2,4,{t}
{s},3,4,{t}
{s},2,3,5,{t}
{s},3,5,{t}
</answer>

Answer format explanation:
- First line: R= followed by all elements in the tier set (in ascending order, comma-separated)
- Second line: paths= followed by the total number of routes
- Subsequent lines: Each line contains one complete litigation route from filing to final judgment (phases comma-separated)
- Routes should be sorted by length (shorter first), and within the same length, by lexicographic order

Please use as few queries as possible to complete the procedural review task.
"""

    tags = ["answer", "query_edge", "query_path"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "s": 1,
                "t": 5,
                "R": [1, 2],
            },
            2: {
                "n": 7,
                "s": 1,
                "t": 7,
                "R": [1, 3],
            },
            3: {
                "n": 7,
                "s": 1,
                "t": 7,
                "R": [2, 3],
            },
            4: {
                "n": 8,
                "s": 1,
                "t": 8,
                "R": [1, 2, 4],
            },
            5: {
                "n": 10,
                "s": 1,
                "t": 10,
                "R": [2, 3, 5],
            },
        },
        "en": {
            1: {
                "n": 5,
                "s": 1,
                "t": 5,
                "R": [1, 2],
            },
            2: {
                "n": 7,
                "s": 1,
                "t": 7,
                "R": [1, 3],
            },
            3: {
                "n": 7,
                "s": 1,
                "t": 7,
                "R": [2, 3],
            },
            4: {
                "n": 8,
                "s": 1,
                "t": 8,
                "R": [1, 2, 4],
            },
            5: {
                "n": 10,
                "s": 1,
                "t": 10,
                "R": [2, 3, 5],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.n = cfg["n"]
        self.s = cfg["s"]
        self.t = cfg["t"]
        self.R = set(cfg["R"])
        
        self._game_info["n"] = self.n
        self._game_info["s"] = self.s
        self._game_info["t"] = self.t
        self._game_info["n_minus_1"] = self.n - 1
        
        self.ground_truth_paths = self._find_all_paths()

    def _find_all_paths(self):
        all_paths = []
        
        def dfs(current, target, path):
            if current == target:
                all_paths.append(path[:])
                return
            for diff in self.R:
                next_node = current + diff
                if next_node <= self.n:
                    path.append(next_node)
                    dfs(next_node, target, path)
                    path.pop()
        
        dfs(self.s, self.t, [self.s])
        
        all_paths.sort(key=lambda p: (len(p), p))
        return all_paths

    def _has_edge(self, a, b):
        return (b - a) in self.R

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        lines = [line.strip() for line in raw_ans.split('\n') if line.strip()]
        
        if len(lines) < 2:
            return False
        
        r_line = lines[0]
        if not r_line.startswith("R="):
            return False
        try:
            r_str = r_line[2:].strip()
            submitted_R = set(int(x.strip()) for x in r_str.split(',') if x.strip())
        except:
            return False
        
        if submitted_R != self.R:
            return False
        
        paths_line = lines[1]
        if not paths_line.startswith("paths="):
            return False
        try:
            expected_count = int(paths_line[6:].strip())
        except:
            return False
        
        submitted_paths = []
        for i in range(2, len(lines)):
            try:
                path = [int(x.strip()) for x in lines[i].split(',') if x.strip()]
                submitted_paths.append(path)
            except:
                return False
        
        if len(submitted_paths) != expected_count:
            return False
        
        if len(submitted_paths) != len(self.ground_truth_paths):
            return False
        
        submitted_paths.sort(key=lambda p: (len(p), p))
        
        return submitted_paths == self.ground_truth_paths

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            success_msg = "成功"
        else:
            yes_res, no_res = "Yes", "No"
            success_msg = "Success"
        
        stripped = correct.strip()
        if stripped == yes_res:
            return no_res
        if stripped == no_res:
            return yes_res
        
        if stripped == success_msg:
            if self.config.language == "zh":
                return "失败：第 1 条边不存在。"
            else:
                return "Failed: Edge 1 does not exist."
        
        return success_msg

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            invalid_msg = "非法"
            success_msg = "成功"
            failed_msg = "失败"
        else:
            yes_res, no_res = "Yes", "No"
            invalid_msg = "Invalid"
            success_msg = "Success"
            failed_msg = "Failed"

        if "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                a, b = int(parts[0]), int(parts[1])
                
                if a >= b or a < 1 or b > self.n:
                    if self.config.language == "zh":
                        return "错误：节点编号不合法或顺序错误。"
                    else:
                        return "Error: Invalid node numbers or order."
                
                return yes_res if self._has_edge(a, b) else no_res
            except:
                if self.config.language == "zh":
                    return "错误：查询格式错误。"
                else:
                    return "Error: Invalid query format."

        elif "query_path" in parsed_info:
            try:
                raw = parsed_info["query_path"].strip()
                path = [int(x.strip()) for x in raw.split(",") if x.strip()]
                
                for i in range(len(path) - 1):
                    if path[i] >= path[i + 1]:
                        return invalid_msg
                
                for i in range(len(path) - 1):
                    if not self._has_edge(path[i], path[i + 1]):
                        if self.config.language == "zh":
                            return f"{failed_msg}：第 {i+1} 条边（{path[i]} 到 {path[i+1]}）不存在。"
                        else:
                            return f"{failed_msg}: Edge {i+1} (from {path[i]} to {path[i+1]}) does not exist."
                
                return success_msg
            except:
                if self.config.language == "zh":
                    return "错误：路径格式错误。"
                else:
                    return "Error: Invalid path format."

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                query_content = f"{i},{j}"
                query_xml = f"<query_edge>{query_content}</query_edge>"
                
                is_connected = self._has_edge(i, j)
                answer = yes_res if is_connected else no_res
                
                queries.append({
                    "query": query_xml,
                    "answer": answer
                })
        
        return queries