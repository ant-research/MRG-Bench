import re
from typing import Dict, Set, Tuple, List
from .base import Game

class GraphScenarioDeductionGame(Game):

    reasoning_type = "溯因推理"
    data_structure = "图"

    contextualized_rule_zh_1 = """\
我们来玩一个"城市交通网络诊断"游戏，规则如下：

游戏设定了一个交通网络图 G=(V,E)，其中枢纽节点集合 V = {{A, B, C, D, E, F}}。

基准路况的通行时间（小时）如下：
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

我已秘密选择了以下四种路况变体之一，并在整个游戏中保持不变：
- S1（基准）：通行时间如上所述。
- S2（A枢纽严重拥堵）：所有与 A 相邻的路段通行时间加 1 小时（A-B: 3, A-C: 4, A-F: 3），其余不变。
- S3（E枢纽周边施工）：所有与 E 相邻的路段通行时间加 1 小时（E-F: 2, D-E: 3, C-E: 4），其余不变。
- S4（C-E 直达快线）：仅将 C-E 的通行时间缩短为 1 小时，其余同基准。

你的目标是通过查询推断出隐藏的路况变体，并计算从枢纽 C 到其他所有枢纽的最短通行时间总和。

你可以进行最多 {max_queries} 次查询，每次查询两个枢纽之间的最短通行时间。查询格式和限制如下：

1. **时间查询**：询问枢纽 X 和 Y 之间的最短通行时间（X 和 Y 必须是 A、B、D、E、F 中的不同枢纽）。
2. **重要限制**：不允许查询任何涉及枢纽 C 的时间（例如 C-A、C-B 等，因 C 枢纽监控设备离线）。
3. **最少查询要求**：你必须至少完成 2 次合法查询后才能提交最终答案。

我会根据隐藏的路况变体如实回答每个合法查询的精确通行时间。

每次只能包含一个标签。请使用以下 XML 格式：

- 时间查询（例如询问 A 和 B 之间的通行时间）：
<query_distance>A,B</query_distance>

提交最终答案时，必须说明推断的路况变体（S1、S2、S3 或 S4）以及从枢纽 C 到所有其他枢纽的最短通行时间总和，格式如下：

<answer>scenario=S1, sum_from_c=10</answer>

其中 sum_from_c 是 d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F) 的总和。

请尽可能少地使用查询次数来完成推理。若答案错误或格式不符，游戏失败。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's play a "City Transit Network Diagnosis" game. Here are the rules:

The game involves a transit network graph G=(V,E), where the hub node set V = {{A, B, C, D, E, F}}.

The baseline travel times (in hours) are as follows:
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

I have secretly chosen one of the following four traffic variants, which remains fixed throughout the game:
- S1 (Baseline): Travel times as described above.
- S2 (Severe congestion at A): All routes adjacent to A have travel time increased by 1 hour (A-B: 3, A-C: 4, A-F: 3), others unchanged.
- S3 (Construction at E): All routes adjacent to E have travel time increased by 1 hour (E-F: 2, D-E: 3, C-E: 4), others unchanged.
- S4 (C-E express line): Only C-E travel time is reduced to 1 hour, others remain baseline.

Your goal is to infer the hidden traffic variant through queries and calculate the sum of shortest travel times from hub C to all other hubs.

You can make at most {max_queries} queries, each asking for the shortest travel time between two hubs. Query format and restrictions:

1. **Time Query**: Ask for the shortest travel time between hubs X and Y (X and Y must be different hubs from A, B, D, E, F).
2. **Important Restriction**: You are NOT allowed to query any travel time involving hub C (e.g., C-A, C-B, etc., due to camera offline).
3. **Minimum Query Requirement**: You must complete at least 2 valid queries before submitting your final answer.

I will truthfully answer each valid query with the exact travel time under the hidden variant.

Each query must contain only one tag. Use the following XML format:

- Time Query (e.g., asking for travel time between A and B):
<query_distance>A,B</query_distance>

When submitting the final answer, specify the inferred scenario (S1, S2, S3, or S4) and the sum of shortest travel times from hub C to all other hubs, using this format:

<answer>scenario=S1, sum_from_c=10</answer>

Where sum_from_c is the sum of d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F).

Try to use as few queries as possible to complete the diagnosis. If the answer is wrong or the format is invalid, the game is a failure.
"""

    contextualized_rule_zh_2 = """\
我们来玩一个"医院物资调配诊断"游戏，规则如下：

游戏设定了一个物资流转图 G=(V,E)，其中科室节点集合 V = {{A, B, C, D, E, F}}。

基准流转的传输时间（分钟）如下：
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

我已秘密选择了以下四种运行变体之一，并在整个游戏中保持不变：
- S1（基准）：传输时间如上所述。
- S2（A科室防疫隔离）：所有与 A 相邻的传输时间加 1 分钟（A-B: 3, A-C: 4, A-F: 3），其余不变。
- S3（E科室气动物流故障）：所有与 E 相邻的传输时间加 1 分钟（E-F: 2, D-E: 3, C-E: 4），其余不变。
- S4（C-E 紧急绿色通道）：仅将 C-E 的传输时间缩短为 1 分钟，其余同基准。

你的目标是通过查询推断出隐藏的运行变体，并计算从科室 C 到其他所有科室的最短急救传输时间总和。

你可以进行最多 {max_queries} 次查询，每次查询两个科室之间的最短传输时间。查询格式和限制如下：

1. **时间查询**：询问科室 X 和 Y 之间的最短传输时间（X 和 Y 必须是 A、B、D、E、F 中的不同科室）。
2. **重要限制**：不允许查询任何涉及科室 C 的时间（例如 C-A、C-B 等，因 C 科室处于严格隔离中）。
3. **最少查询要求**：你必须至少完成 2 次合法查询后才能提交最终答案。

我会根据隐藏的运行变体如实回答每个合法查询的精确传输时间。

每次只能包含一个标签。请使用以下 XML 格式：

- 时间查询（例如询问 A 和 B 之间的传输时间）：
<query_distance>A,B</query_distance>

提交最终答案时，必须说明推断的运行变体（S1、S2、S3 或 S4）以及从科室 C 到所有其他科室的最短传输时间总和，格式如下：

<answer>scenario=S1, sum_from_c=10</answer>

其中 sum_from_c 是 d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F) 的总和。

请尽可能少地使用查询次数来完成诊断。若答案错误或格式不符，游戏失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's play a "Hospital Resource Routing Diagnosis" game. Here are the rules:

The game involves a resource transfer graph G=(V,E), where the department node set V = {{A, B, C, D, E, F}}.

The baseline transfer times (in minutes) are as follows:
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

I have secretly chosen one of the following four operational variants, which remains fixed throughout the game:
- S1 (Baseline): Transfer times as described above.
- S2 (Quarantine at Dept A): All transfers adjacent to A have time increased by 1 minute (A-B: 3, A-C: 4, A-F: 3), others unchanged.
- S3 (Tube breakdown at Dept E): All transfers adjacent to E have time increased by 1 minute (E-F: 2, D-E: 3, C-E: 4), others unchanged.
- S4 (C-E priority green channel): Only C-E transfer time is reduced to 1 minute, others remain baseline.

Your goal is to infer the hidden operational variant through queries and calculate the sum of shortest emergency transfer times from Dept C to all other departments.

You can make at most {max_queries} queries, each asking for the shortest transfer time between two departments. Query format and restrictions:

1. **Time Query**: Ask for the shortest transfer time between departments X and Y (X and Y must be different departments from A, B, D, E, F).
2. **Important Restriction**: You are NOT allowed to query any transfer time involving Dept C (e.g., C-A, C-B, etc., due to strict isolation).
3. **Minimum Query Requirement**: You must complete at least 2 valid queries before submitting your final answer.

I will truthfully answer each valid query with the exact transfer time under the hidden variant.

Each query must contain only one tag. Use the following XML format:

- Time Query (e.g., asking for transfer time between A and B):
<query_distance>A,B</query_distance>

When submitting the final answer, specify the inferred scenario (S1, S2, S3, or S4) and the sum of shortest transfer times from Dept C to all other departments, using this format:

<answer>scenario=S1, sum_from_c=10</answer>

Where sum_from_c is the sum of d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F).

Try to use as few queries as possible to complete the diagnosis. If the answer is wrong or the format is invalid, the game is a failure.
"""

    contextualized_rule_zh_3 = """\
我们来玩一个"校园通行网络分析"游戏，规则如下：

游戏设定了一个校园地图 G=(V,E)，其中教学楼节点集合 V = {{A, B, C, D, E, F}}。

基准情况下的步行时间（分钟）如下：
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

我已秘密选择了以下四种通行变体之一，并在整个游戏中保持不变：
- S1（基准）：步行时间如上所述。
- S2（A楼大型活动拥挤）：所有与 A 相邻的路段步行时间加 1 分钟（A-B: 3, A-C: 4, A-F: 3），其余不变。
- S3（E楼周边路面维护）：所有与 E 相邻的路段步行时间加 1 分钟（E-F: 2, D-E: 3, C-E: 4），其余不变。
- S4（C-E 开放内部连廊）：仅将 C-E 的步行时间缩短为 1 分钟，其余同基准。

你的目标是通过查询推断出隐藏的通行变体，并计算从主楼 C 到其他所有教学楼的最短步行时间总和。

你可以进行最多 {max_queries} 次查询，每次查询两栋教学楼之间的最短步行时间。查询格式和限制如下：

1. **时间查询**：询问教学楼 X 和 Y 之间的最短步行时间（X 和 Y 必须是 A、B、D、E、F 中的不同教学楼）。
2. **重要限制**：不允许查询任何涉及主楼 C 的时间（例如 C-A、C-B 等，因 C 楼门禁系统升级无法访问数据）。
3. **最少查询要求**：你必须至少完成 2 次合法查询后才能提交最终答案。

我会根据隐藏的通行变体如实回答每个合法查询的精确步行时间。

每次只能包含一个标签。请使用以下 XML 格式：

- 时间查询（例如询问 A 和 B 之间的步行时间）：
<query_distance>A,B</query_distance>

提交最终答案时，必须说明推断的通行变体（S1、S2、S3 或 S4）以及从主楼 C 到所有其他教学楼的最短步行时间总和，格式如下：

<answer>scenario=S1, sum_from_c=10</answer>

其中 sum_from_c 是 d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F) 的总和。

请尽可能少地使用查询次数来完成分析。若答案错误或格式不符，游戏失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Campus Walking Path Analysis" game. Here are the rules:

The game involves a campus map graph G=(V,E), where the building node set V = {{A, B, C, D, E, F}}.

The baseline walking times (in minutes) are as follows:
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

I have secretly chosen one of the following four traffic variants, which remains fixed throughout the game:
- S1 (Baseline): Walking times as described above.
- S2 (Event crowd at Building A): All paths adjacent to A have walking time increased by 1 minute (A-B: 3, A-C: 4, A-F: 3), others unchanged.
- S3 (Path maintenance at Building E): All paths adjacent to E have walking time increased by 1 minute (E-F: 2, D-E: 3, C-E: 4), others unchanged.
- S4 (C-E shortcut opened): Only C-E walking time is reduced to 1 minute, others remain baseline.

Your goal is to infer the hidden traffic variant through queries and calculate the sum of shortest walking times from Main Building C to all other buildings.

You can make at most {max_queries} queries, each asking for the shortest walking time between two buildings. Query format and restrictions:

1. **Time Query**: Ask for the shortest walking time between buildings X and Y (X and Y must be different buildings from A, B, D, E, F).
2. **Important Restriction**: You are NOT allowed to query any walking time involving Building C (e.g., C-A, C-B, etc., due to access restrictions).
3. **Minimum Query Requirement**: You must complete at least 2 valid queries before submitting your final answer.

I will truthfully answer each valid query with the exact walking time under the hidden variant.

Each query must contain only one tag. Use the following XML format:

- Time Query (e.g., asking for walking time between A and B):
<query_distance>A,B</query_distance>

When submitting the final answer, specify the inferred scenario (S1, S2, S3, or S4) and the sum of shortest walking times from Building C to all other buildings, using this format:

<answer>scenario=S1, sum_from_c=10</answer>

Where sum_from_c is the sum of d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F).

Try to use as few queries as possible to complete the analysis. If the answer is wrong or the format is invalid, the game is a failure.
"""

    contextualized_rule_zh_4 = """\
我们来玩一个"工业流水线瓶颈排查"游戏，规则如下：

游戏设定了一个传送带网络 G=(V,E)，其中加工工站节点集合 V = {{A, B, C, D, E, F}}。

基准情况下的物料传送时间（秒）如下：
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

我已秘密选择了以下四种故障变体之一，并在整个排查过程中保持不变：
- S1（基准）：传送时间如上所述。
- S2（A工站电机老化）：所有与 A 相连的传送带耗时加 1 秒（A-B: 3, A-C: 4, A-F: 3），其余不变。
- S3（E工站传感器需校准）：所有与 E 相连的传送带耗时加 1 秒（E-F: 2, D-E: 3, C-E: 4），其余不变。
- S4（C-E 高速旁路）：仅将 C-E 的传送时间降至 1 秒，其余同基准。

你的目标是通过查询推断出流水线的实际故障情况，并计算从中控工站 C 到其他所有工站的最短传送时间总和。

你可以进行最多 {max_queries} 次查询，每次查询两个工站之间的最短传送时间。查询格式和限制如下：

1. **时间查询**：询问工站 X 和 Y 之间的最短传送时间（X 和 Y 必须是 A、B、D、E、F 中的不同工站）。
2. **重要限制**：不允许查询任何涉及工站 C 的时间（例如 C-A、C-B 等，因 C 工站的直接诊断接口损坏）。
3. **最少查询要求**：你必须至少完成 2 次合法查询后才能提交最终答案。

我会根据隐藏的故障变体如实回答每个合法查询的精确传送时间。

每次只能包含一个标签。请使用以下 XML 格式：

- 时间查询（例如询问 A 和 B 之间的传送时间）：
<query_distance>A,B</query_distance>

提交最终答案时，必须说明推断的变体（S1、S2、S3 或 S4）以及从工站 C 到所有其他工站的最短传送时间总和，格式如下：

<answer>scenario=S1, sum_from_c=10</answer>

其中 sum_from_c 是 d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F) 的总和。

请尽可能少地使用查询次数来完成排查。若答案错误或格式不符，排查失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Assembly Line Bottleneck Diagnosis" game. Here are the rules:

The game involves a conveyor network graph G=(V,E), where the workstation node set V = {{A, B, C, D, E, F}}.

The baseline transport times (in seconds) are as follows:
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

I have secretly chosen one of the following four fault variants, which remains fixed throughout the diagnosis:
- S1 (Baseline): Transport times as described above.
- S2 (Motor degradation at Station A): All belts adjacent to A have time increased by 1 second (A-B: 3, A-C: 4, A-F: 3), others unchanged.
- S3 (Sensor calibration issue at Station E): All belts adjacent to E have time increased by 1 second (E-F: 2, D-E: 3, C-E: 4), others unchanged.
- S4 (C-E high-speed bypass): Only C-E transport time is reduced to 1 second, others remain baseline.

Your goal is to infer the hidden fault variant through queries and calculate the sum of shortest transport times from Central Station C to all other stations.

You can make at most {max_queries} queries, each asking for the shortest transport time between two stations. Query format and restrictions:

1. **Time Query**: Ask for the shortest transport time between stations X and Y (X and Y must be different stations from A, B, D, E, F).
2. **Important Restriction**: You are NOT allowed to query any transport time involving Station C (e.g., C-A, C-B, etc., due to disabled local diagnostic ping).
3. **Minimum Query Requirement**: You must complete at least 2 valid queries before submitting your final answer.

I will truthfully answer each valid query with the exact transport time under the hidden variant.

Each query must contain only one tag. Use the following XML format:

- Time Query (e.g., asking for transport time between A and B):
<query_distance>A,B</query_distance>

When submitting the final answer, specify the inferred scenario (S1, S2, S3, or S4) and the sum of shortest transport times from Station C to all other stations, using this format:

<answer>scenario=S1, sum_from_c=10</answer>

Where sum_from_c is the sum of d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F).

Try to use as few queries as possible to complete the diagnosis. If the answer is wrong or the format is invalid, the diagnosis fails.
"""

    contextualized_rule_zh_5 = """\
我们来玩一个"司法审批流程审查"游戏，规则如下：

游戏设定了一个审批流转网络 G=(V,E)，其中处理部门节点集合 V = {{A, B, C, D, E, F}}。

基准情况下的材料流转周期（天）如下：
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

我已秘密选择了以下四种瓶颈变体之一，并在整个审查过程中保持不变：
- S1（基准）：流转周期如上所述。
- S2（A部门深度合规审计）：所有涉及 A 的流转周期加 1 天（A-B: 3, A-C: 4, A-F: 3），其余不变。
- S3（E部门人员短缺）：所有涉及 E 的流转周期加 1 天（E-F: 2, D-E: 3, C-E: 4），其余不变。
- S4（C-E 特批通道）：仅将 C-E 的流转周期缩短为 1 天，其余同基准。

你的目标是通过查询查明目前的审批瓶颈状态，并计算从 C 部门到其他所有部门的最短流转周期总和。

你可以进行最多 {max_queries} 次查询，每次查询两个部门之间的最短流转周期。查询格式和限制如下：

1. **周期查询**：询问部门 X 和 Y 之间的最短流转周期（X 和 Y 必须是 A、B、D、E、F 中的不同部门）。
2. **重要限制**：不允许查询任何涉及部门 C 的周期（例如 C-A、C-B 等，因 C 部门目前涉及机密审查，数据已脱敏）。
3. **最少查询要求**：你必须至少完成 2 次合法查询后才能提交最终审查结果。

我会根据隐藏的瓶颈变体如实回答每个合法查询的精确流转周期。

每次只能包含一个标签。请使用以下 XML 格式：

- 周期查询（例如询问 A 和 B 之间的流转周期）：
<query_distance>A,B</query_distance>

提交最终答案时，必须说明推断的瓶颈变体（S1、S2、S3 或 S4）以及从部门 C 到所有其他部门的最短流转周期总和，格式如下：

<answer>scenario=S1, sum_from_c=10</answer>

其中 sum_from_c 是 d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F) 的总和。

请尽可能少地使用查询次数来完成审查。若答案错误或格式不符，审查失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's play a "Judicial Workflow Review" game. Here are the rules:

The game involves a bureaucratic routing network graph G=(V,E), where the department node set V = {{A, B, C, D, E, F}}.

The baseline processing delays (in days) are as follows:
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

I have secretly chosen one of the following four bottleneck variants, which remains fixed throughout the review:
- S1 (Baseline): Processing delays as described above.
- S2 (Compliance audit at Dept A): All procedures adjacent to A have delay increased by 1 day (A-B: 3, A-C: 4, A-F: 3), others unchanged.
- S3 (Staff shortage at Dept E): All procedures adjacent to E have delay increased by 1 day (E-F: 2, D-E: 3, C-E: 4), others unchanged.
- S4 (C-E expedited channel): Only C-E processing delay is reduced to 1 day, others remain baseline.

Your goal is to infer the hidden bottleneck state through queries and calculate the sum of shortest processing delays from Dept C to all other departments.

You can make at most {max_queries} queries, each asking for the shortest processing delay between two departments. Query format and restrictions:

1. **Delay Query**: Ask for the shortest processing delay between departments X and Y (X and Y must be different departments from A, B, D, E, F).
2. **Important Restriction**: You are NOT allowed to query any processing delay involving Dept C (e.g., C-A, C-B, etc., due to confidential review redaction).
3. **Minimum Query Requirement**: You must complete at least 2 valid queries before submitting your final answer.

I will truthfully answer each valid query with the exact processing delay under the hidden variant.

Each query must contain only one tag. Use the following XML format:

- Delay Query (e.g., asking for processing delay between A and B):
<query_distance>A,B</query_distance>

When submitting the final answer, specify the inferred scenario (S1, S2, S3, or S4) and the sum of shortest processing delays from Dept C to all other departments, using this format:

<answer>scenario=S1, sum_from_c=10</answer>

Where sum_from_c is the sum of d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F).

Try to use as few queries as possible to complete the review. If the answer is wrong or the format is invalid, the review fails.
"""

    game_rule_zh = """\
我们来玩一个"图变体推理"游戏，规则如下：

游戏设定了一个无向加权图 G=(V,E)，其中节点集合 V = {{A, B, C, D, E, F}}。

基准图的边与权重如下：
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

我已秘密选择了以下四种加权变体之一，并在整个游戏中保持不变：
- S1（基准）：权重如上所述。
- S2（A-邻接增重）：所有与 A 相邻的边权重加 1（A-B: 3, A-C: 4, A-F: 3），其余不变。
- S3（E-邻接增重）：所有与 E 相邻的边权重加 1（E-F: 2, D-E: 3, C-E: 4），其余不变。
- S4（C-E 减重）：仅将 C-E 的权重调整为 1，其余同基准。

你的目标是通过查询推断出隐藏的变体，并计算从节点 C 到其他所有节点的最短距离总和。

你可以进行最多 {max_queries} 次查询，每次查询两个节点之间的最短路距离。查询格式和限制如下：

1. **距离查询**：询问节点 X 和 Y 之间的最短路距离（X 和 Y 必须是 A、B、D、E、F 中的不同节点）。
2. **重要限制**：不允许查询任何涉及节点 C 的距离（例如 C-A、C-B 等）。
3. **最少查询要求**：你必须至少完成 2 次合法查询后才能提交最终答案。

我会根据隐藏的变体如实回答每个合法查询的精确距离。

每次只能包含一个标签。请使用以下 XML 格式：

- 距离查询（例如询问 A 和 B 之间的距离）：
<query_distance>A,B</query_distance>

提交最终答案时，必须说明推断的变体（S1、S2、S3 或 S4）以及从节点 C 到所有其他节点的最短距离总和，格式如下：

<answer>scenario=S1, sum_from_c=10</answer>

其中 sum_from_c 是 d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F) 的总和。

请尽可能少地使用查询次数来完成推理。若答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Graph Scenario Deduction" game. Here are the rules:

The game involves an undirected weighted graph G=(V,E), where the node set V = {{A, B, C, D, E, F}}.

The baseline graph has the following edges and weights:
- A-B: 2, B-C: 1, C-D: 2, D-E: 2, E-F: 1, F-A: 2
- A-C: 3, B-D: 3, C-E: 3, D-F: 3

I have secretly chosen one of the following four weighted variants, which remains fixed throughout the game:
- S1 (Baseline): Weights as described above.
- S2 (A-adjacent increased): All edges adjacent to A have weight increased by 1 (A-B: 3, A-C: 4, A-F: 3), others unchanged.
- S3 (E-adjacent increased): All edges adjacent to E have weight increased by 1 (E-F: 2, D-E: 3, C-E: 4), others unchanged.
- S4 (C-E decreased): Only C-E is adjusted to 1, others remain baseline.

Your goal is to infer the hidden variant through queries and calculate the sum of shortest distances from node C to all other nodes.

You can make at most {max_queries} queries, each asking for the shortest path distance between two nodes. Query format and restrictions:

1. **Distance Query**: Ask for the shortest path distance between nodes X and Y (X and Y must be different nodes from A, B, D, E, F).
2. **Important Restriction**: You are NOT allowed to query any distance involving node C (e.g., C-A, C-B, etc.).
3. **Minimum Query Requirement**: You must complete at least 2 valid queries before submitting your final answer.

I will truthfully answer each valid query with the exact distance under the hidden variant.

Each query must contain only one tag. Use the following XML format:

- Distance Query (e.g., asking for distance between A and B):
<query_distance>A,B</query_distance>

When submitting the final answer, specify the inferred scenario (S1, S2, S3, or S4) and the sum of shortest distances from node C to all other nodes, using this format:

<answer>scenario=S1, sum_from_c=10</answer>

Where sum_from_c is the sum of d(C,A) + d(C,B) + d(C,D) + d(C,E) + d(C,F).

Try to use as few queries as possible to complete the deduction. If the answer is wrong or the format is invalid, the game is a failure.
"""

    tags = ["answer", "query_distance"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"max_queries": 5, "scenario": "S1"},
            2: {"max_queries": 4, "scenario": "S2"},
            3: {"max_queries": 3, "scenario": "S3"},
            4: {"max_queries": 3, "scenario": "S4"},
            5: {"max_queries": 3, "scenario": "S2"},
        },
        "en": {
            1: {"max_queries": 5, "scenario": "S1"},
            2: {"max_queries": 4, "scenario": "S2"},
            3: {"max_queries": 3, "scenario": "S3"},
            4: {"max_queries": 3, "scenario": "S4"},
            5: {"max_queries": 3, "scenario": "S2"},
        },
    }

    def __init__(self, config):
        self.query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        import random as _random
        
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.max_queries = cfg["max_queries"]
        
        all_scenarios = ["S1", "S2", "S3", "S4"]
        self.scenario = _random.choice(all_scenarios)
        
        self._game_info["max_queries"] = self.max_queries

        self._init_graph()
        
        self._apply_scenario()

    def _init_graph(self):
        self.graph: Dict[str, Dict[str, int]] = {
            'A': {'B': 2, 'C': 3, 'F': 2},
            'B': {'A': 2, 'C': 1, 'D': 3},
            'C': {'A': 3, 'B': 1, 'D': 2, 'E': 3},
            'D': {'B': 3, 'C': 2, 'E': 2, 'F': 3},
            'E': {'C': 3, 'D': 2, 'F': 1},
            'F': {'A': 2, 'D': 3, 'E': 1},
        }

    def _apply_scenario(self):
        if self.scenario == "S1":
            pass
        elif self.scenario == "S2":
            self.graph['A']['B'] = 3
            self.graph['B']['A'] = 3
            self.graph['A']['C'] = 4
            self.graph['C']['A'] = 4
            self.graph['A']['F'] = 3
            self.graph['F']['A'] = 3
        elif self.scenario == "S3":
            self.graph['E']['F'] = 2
            self.graph['F']['E'] = 2
            self.graph['D']['E'] = 3
            self.graph['E']['D'] = 3
            self.graph['C']['E'] = 4
            self.graph['E']['C'] = 4
        elif self.scenario == "S4":
            self.graph['C']['E'] = 1
            self.graph['E']['C'] = 1
        else:
            raise ValueError(f"Unknown scenario: {self.scenario}")

    def _dijkstra(self, start: str) -> Dict[str, int]:
        import heapq
        
        dist = {node: float('inf') for node in self.graph}
        dist[start] = 0
        pq = [(0, start)]
        visited = set()
        
        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            
            for v, weight in self.graph[u].items():
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    heapq.heappush(pq, (dist[v], v))
        
        return dist

    def _get_distance(self, node1: str, node2: str) -> int:
        dist = self._dijkstra(node1)
        return dist[node2]

    def _calculate_sum_from_c(self) -> int:
        dist = self._dijkstra('C')
        return sum(dist[node] for node in ['A', 'B', 'D', 'E', 'F'])

    def evaluate(self, parsed_info):
        
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        
        for kv in kv_pairs:
            if "=" not in kv:
                continue
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "scenario" not in ans_dict or "sum_from_c" not in ans_dict:
            return False
        
        if ans_dict["scenario"] != self.scenario:
            return False
        
        try:
            model_sum = int(ans_dict["sum_from_c"])
        except (ValueError, TypeError):
            return False
        
        true_sum = self._calculate_sum_from_c()
        return model_sum == true_sum

    def _cf_core_produce(self, parsed_info):
        if "query_distance" in parsed_info:
            if self.query_count >= self.max_queries:
                if self.config.language == "zh":
                    raise ValueError(f"已达到最大查询次数（{self.max_queries}次），请直接提交答案。")
                else:
                    raise ValueError(f"Maximum query limit ({self.max_queries}) reached. Please submit your answer.")
            
            raw = parsed_info["query_distance"]
            nodes = [x.strip().upper() for x in raw.split(",")]
            
            if len(nodes) != 2:
                raise ValueError("Must query exactly two nodes")
            
            node1, node2 = nodes
            
            valid_nodes = {'A', 'B', 'D', 'E', 'F'}
            if node1 not in valid_nodes or node2 not in valid_nodes:
                if self.config.language == "zh":
                    return "错误：查询必须使用节点 A、B、D、E、F，且不能涉及节点 C。"
                else:
                    return "Error: Query must use nodes A, B, D, E, F, and cannot involve node C."
            
            if node1 == node2:
                if self.config.language == "zh":
                    return "错误：必须查询两个不同的节点。"
                else:
                    return "Error: Must query two different nodes."
            
            distance = self._get_distance(node1, node2)
            self.query_count += 1
            
            return str(distance)
        
        else:
            raise ValueError("No valid query tag found.")
    
    def get_all_possible_queries(self) -> List[Dict]:
        possible_queries = []
        valid_nodes = ['A', 'B', 'D', 'E', 'F']
        
        for i in range(len(valid_nodes)):
            for j in range(i + 1, len(valid_nodes)):
                node1 = valid_nodes[i]
                node2 = valid_nodes[j]
                
                distance = self._get_distance(node1, node2)
                
                possible_queries.append({
                    "query": f"<query_distance>{node1},{node2}</query_distance>",
                    "answer": str(distance)
                })
        
        return possible_queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_correct = correct.lower()
        if lower_correct == "yes":
            return "No"
        if lower_correct == "no":
            return "Yes"
            
        return correct + "_WRONG"