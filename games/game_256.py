from .base import Game
import re
import itertools

class GraphRuleInferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"图规则推理"游戏，规则如下：

游戏设定了一个包含 12 个节点的集合 V，每个节点用一对公开属性 (A,B) 标识，其中 A 属于 {{1,2,3}}，B 属于 {{1,2,3,4}}。所有 12 种 (A,B) 组合各出现一次。

存在一个固定但未知的无向简单图 G=(V,E)。边集 E 由一个隐藏的判定规则 R 决定，该规则对任意两个不同节点判断它们之间是否存在边。

我已经指定了起点 s={start} 和终点 t={end}，保证存在至少一条从 s 到 t 的合法路径。

你的目标是：通过查询推断出规则 R，并在未被直接试探过的节点对上进行正确预测，同时给出一条新的从 s 到 t 的合法路径。

你可以进行"路径合法性查询"：提交一个长度 k（k 大于等于 2）的节点序列。

- 查询格式：节点用 (A,B) 表示，多个节点用分号分隔
- 反馈：
  - 若序列中所有相邻节点对都存在边，回答"是"
  - 否则回答"否"，并给出首个不合法相邻对的位置索引（从 1 开始）

注意：在提交最终答案前，你需要完成至少 8 次不同的查询，其中至少 5 次为长度 2 的查询，至少 3 次为长度大于等于 3 的查询。

路径合法性查询：
<query_path>(1,2);(1,3);(2,4)</query_path>

当你收集足够信息后，需要一次性提交：

1. 规则描述：用自然语言描述你推断的边判定规则
2. 从 s 到 t 的路径：所有相邻节点对必须是之前查询中未出现过的
3. 额外预测：提交 4 个未在之前查询中出现过的节点对，其中 2 个标注为"连边"，2 个标注为"非连边"

提交格式：
<answer>
rule: [你推断的规则描述]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>

例如：
<answer>
rule: 当且仅当两个节点的 A 属性相同时存在边
path: (1,1);(1,2);(1,3)
predictions: (1,1)-(1,4):connected, (2,1)-(2,3):connected, (1,2)-(2,1):not_connected, (1,3)-(3,2):not_connected
</answer>
"""

    game_rule_en = """\
Let's play a "Graph Rule Inference" game. Here are the rules:

The game defines a set V of 12 nodes. Each node is identified by a pair of public attributes (A,B), where A is in {{1,2,3}} and B is in {{1,2,3,4}}. All 12 (A,B) combinations appear exactly once.

There exists a fixed but unknown undirected simple graph G=(V,E). The edge set E is determined by a hidden decision rule R, which judges whether an edge exists between any two distinct nodes.

I have specified a start node s={start} and an end node t={end}, and guarantee that at least one valid path exists from s to t.

Your goal is: infer rule R through queries, make correct predictions on untested node pairs, and provide a new valid path from s to t.

You can make "path validity queries": submit a node sequence of length k (k is greater than or equal to 2).

- Query format: nodes are represented as (A,B), multiple nodes separated by semicolons
- Feedback:
  - If all adjacent node pairs in the sequence have edges, answer "Yes"
  - Otherwise answer "No" and provide the position index of the first invalid adjacent pair (starting from 1)

Note: Before submitting the final answer, you need to complete at least 8 different queries, with at least 5 queries of length 2 and at least 3 queries of length greater than or equal to 3.

Path validity query:
<query_path>(1,2);(1,3);(2,4)</query_path>

When you have collected enough information, submit all at once:

1. Rule description: describe your inferred edge decision rule in natural language
2. Path from s to t: all adjacent node pairs must not have appeared in previous queries
3. Additional predictions: submit 4 node pairs not appearing in previous queries, with 2 labeled as "connected" and 2 as "not_connected"

Submission format:
<answer>
rule: [your inferred rule description]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>

Example:
<answer>
rule: An edge exists if and only if two nodes have the same A attribute
path: (1,1);(1,2);(1,3)
predictions: (1,1)-(1,4):connected, (2,1)-(2,3):connected, (1,2)-(2,1):not_connected, (1,3)-(3,2):not_connected
</answer>
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通路网规划系统”。你需要推断出隐藏的航线开通规则。

系统设定了一个包含 12 个交通枢纽的集合 V，每个枢纽用一对公开属性 (A,B) 标识，其中 A 代表枢纽所在区域（属于 {{1,2,3}}），B 代表枢纽的吞吐量等级（属于 {{1,2,3,4}}）。所有 12 种 (A,B) 组合各出现一次。

存在一个固定但未知的路网无向图 G=(V,E)。边集 E 由一个隐藏的判定规则 R 决定，该规则判断任意两个不同枢纽之间是否允许开通直达路线（即是否存在连边）。

我已经指定了起点枢纽 s={start} 和终点枢纽 t={end}，保证存在至少一条从 s 到 t 的合法路线。

你的目标是：通过查询推断出规则 R，并在未被直接试探过的枢纽对上进行正确预测，同时给出一条新的从 s 到 t 的合法路线。

你可以进行"路线合法性查询"：提交一个长度 k（k 大于等于 2）的枢纽序列。

- 查询格式：枢纽用 (A,B) 表示，多个枢纽用分号分隔
- 反馈：
  - 若序列中所有相邻枢纽对都允许开通直达路线，回答"是"
  - 否则回答"否"，并给出首个不合法相邻对的位置索引（从 1 开始）

注意：在提交最终答案前，你需要完成至少 8 次不同的查询，其中至少 5 次为长度 2 的查询，至少 3 次为长度大于等于 3 的查询。

路线合法性查询：
<query_path>(1,2);(1,3);(2,4)</query_path>

当你收集足够信息后，需要一次性提交：

1. 规则描述：用自然语言描述你推断的直达路线判定规则（请在描述中包含 A 属性和 B 属性等关键词）
2. 从 s 到 t 的路线：所有相邻枢纽对必须是之前查询中未出现过的
3. 额外预测：提交 4 个未在之前查询中出现过的枢纽对，其中 2 个标注为"connected"（可连通），2 个标注为"not_connected"（不可连通）

提交格式：
<answer>
rule: [你推断的规则描述]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>

例如：
<answer>
rule: 当且仅当两个枢纽的区域 A 属性相同时允许开通路线
path: (1,1);(1,2);(1,3)
predictions: (1,1)-(1,4):connected, (2,1)-(2,3):connected, (1,2)-(2,1):not_connected, (1,3)-(3,2):not_connected
</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Network Planning System". You need to infer the hidden route opening rules.

The system defines a set V of 12 traffic hubs. Each hub is identified by a pair of public attributes (A,B), where A represents the zone (in {{1,2,3}}) and B represents the throughput level (in {{1,2,3,4}}). All 12 (A,B) combinations appear exactly once.

There exists a fixed but unknown undirected network graph G=(V,E). The edge set E is determined by a hidden decision rule R, which judges whether a direct route is allowed between any two distinct hubs (i.e., whether an edge exists).

I have specified a start hub s={start} and an end hub t={end}, and guarantee that at least one valid transport route exists from s to t.

Your goal is: infer rule R through queries, make correct predictions on untested hub pairs, and provide a new valid route from s to t.

You can make "route validity queries": submit a hub sequence of length k (k is greater than or equal to 2).

- Query format: hubs are represented as (A,B), multiple hubs separated by semicolons
- Feedback:
  - If all adjacent hub pairs in the sequence allow direct routes, answer "Yes"
  - Otherwise answer "No" and provide the position index of the first invalid adjacent pair (starting from 1)

Note: Before submitting the final answer, you need to complete at least 8 different queries, with at least 5 queries of length 2 and at least 3 queries of length greater than or equal to 3.

Route validity query:
<query_path>(1,2);(1,3);(2,4)</query_path>

When you have collected enough information, submit all at once:

1. Rule description: describe your inferred direct route decision rule in natural language (please include keywords like A and B attributes)
2. Route from s to t: all adjacent hub pairs must not have appeared in previous queries
3. Additional predictions: submit 4 hub pairs not appearing in previous queries, with 2 labeled as "connected" and 2 as "not_connected"

Submission format:
<answer>
rule: [your inferred rule description]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>

Example:
<answer>
rule: A direct route is allowed if and only if two hubs have the same A attribute
path: (1,1);(1,2);(1,3)
predictions: (1,1)-(1,4):connected, (2,1)-(2,3):connected, (1,2)-(2,1):not_connected, (1,3)-(3,2):not_connected
</answer>
"""

    contextualized_rule_zh_2 = """\
欢迎使用“医疗会诊协作系统”。你需要推断出隐藏的跨科室协作规则。

系统设定了一个包含 12 位医疗专家的集合 V，每位专家用一对公开属性 (A,B) 标识，其中 A 代表专业大类（属于 {{1,2,3}}），B 代表专家职级（属于 {{1,2,3,4}}）。所有 12 种 (A,B) 组合各出现一次。

存在一个固定但未知的协作网络无向图 G=(V,E)。边集 E 由一个隐藏的判定规则 R 决定，该规则判断任意两位不同专家之间是否允许发起联合会诊（即是否存在连边）。

我已经指定了起始专家 s={start} 和终点专家 t={end}，保证存在至少一条从 s 到 t 的合法联合会诊路径。

你的目标是：通过查询推断出规则 R，并在未被直接试探过的专家对上进行正确预测，同时给出一条新的从 s 到 t 的合法会诊流转路径。

你可以进行"会诊路径合法性查询"：提交一个长度 k（k 大于等于 2）的专家序列。

- 查询格式：专家用 (A,B) 表示，多个专家用分号分隔
- 反馈：
  - 若序列中所有相邻专家对都允许联合会诊，回答"是"
  - 否则回答"否"，并给出首个不合法相邻对的位置索引（从 1 开始）

注意：在提交最终答案前，你需要完成至少 8 次不同的查询，其中至少 5 次为长度 2 的查询，至少 3 次为长度大于等于 3 的查询。

会诊路径合法性查询：
<query_path>(1,2);(1,3);(2,4)</query_path>

当你收集足够信息后，需要一次性提交：

1. 规则描述：用自然语言描述你推断的联合会诊判定规则（请在描述中包含 A 属性和 B 属性等关键词）
2. 从 s 到 t 的路径：所有相邻专家对必须是之前查询中未出现过的
3. 额外预测：提交 4 个未在之前查询中出现过的专家对，其中 2 个标注为"connected"（允许会诊），2 个标注为"not_connected"（不允许会诊）

提交格式：
<answer>
rule: [你推断的规则描述]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Medical Consultation Collaboration System". You need to infer the hidden cross-departmental collaboration rules.

The system defines a set V of 12 medical experts. Each expert is identified by a pair of public attributes (A,B), where A represents the specialty category (in {{1,2,3}}) and B represents the rank (in {{1,2,3,4}}). All 12 (A,B) combinations appear exactly once.

There exists a fixed but unknown undirected collaboration network graph G=(V,E). The edge set E is determined by a hidden decision rule R, which judges whether any two distinct experts are allowed to initiate a joint consultation (i.e., whether an edge exists).

I have specified a start expert s={start} and an end expert t={end}, and guarantee that at least one valid consultation path exists from s to t.

Your goal is: infer rule R through queries, make correct predictions on untested expert pairs, and provide a new valid path from s to t.

You can make "consultation path validity queries": submit an expert sequence of length k (k is greater than or equal to 2).

- Query format: experts are represented as (A,B), multiple experts separated by semicolons
- Feedback:
  - If all adjacent expert pairs in the sequence allow joint consultations, answer "Yes"
  - Otherwise answer "No" and provide the position index of the first invalid adjacent pair (starting from 1)

Note: Before submitting the final answer, you need to complete at least 8 different queries, with at least 5 queries of length 2 and at least 3 queries of length greater than or equal to 3.

Consultation path validity query:
<query_path>(1,2);(1,3);(2,4)</query_path>

When you have collected enough information, submit all at once:

1. Rule description: describe your inferred consultation decision rule in natural language (please include keywords like A and B attributes)
2. Path from s to t: all adjacent expert pairs must not have appeared in previous queries
3. Additional predictions: submit 4 expert pairs not appearing in previous queries, with 2 labeled as "connected" and 2 as "not_connected"

Submission format:
<answer>
rule: [your inferred rule description]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>
"""

    contextualized_rule_zh_3 = """\
欢迎使用“智能教育课程编排系统”。你需要推断出隐藏的课程关联规则。

系统设定了一个包含 12 门课程的集合 V，每门课程用一对公开属性 (A,B) 标识，其中 A 代表学科领域（属于 {{1,2,3}}），B 代表课程难度阶段（属于 {{1,2,3,4}}）。所有 12 种 (A,B) 组合各出现一次。

存在一个固定但未知的课程关联无向图 G=(V,E)。边集 E 由一个隐藏的判定规则 R 决定，该规则判断任意两门不同课程之间是否可以建立关联学习路径（即是否存在连边）。

我已经指定了起点课程 s={start} 和终点课程 t={end}，保证存在至少一条从 s 到 t 的合法连贯学习路径。

你的目标是：通过查询推断出规则 R，并在未被直接试探过的课程对上进行正确预测，同时给出一条新的从 s 到 t 的合法学习路径。

你可以进行"学习路径合法性查询"：提交一个长度 k（k 大于等于 2）的课程序列。

- 查询格式：课程用 (A,B) 表示，多门课程用分号分隔
- 反馈：
  - 若序列中所有相邻课程对都允许建立关联学习路径，回答"是"
  - 否则回答"否"，并给出首个不合法相邻对的位置索引（从 1 开始）

注意：在提交最终答案前，你需要完成至少 8 次不同的查询，其中至少 5 次为长度 2 的查询，至少 3 次为长度大于等于 3 的查询。

学习路径合法性查询：
<query_path>(1,2);(1,3);(2,4)</query_path>

当你收集足够信息后，需要一次性提交：

1. 规则描述：用自然语言描述你推断的课程关联判定规则（请在描述中包含 A 属性和 B 属性等关键词）
2. 从 s 到 t 的路径：所有相邻课程对必须是之前查询中未出现过的
3. 额外预测：提交 4 个未在之前查询中出现过的课程对，其中 2 个标注为"connected"（可关联），2 个标注为"not_connected"（不可关联）

提交格式：
<answer>
rule: [你推断的规则描述]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Intelligent Education Course Scheduling System". You need to infer the hidden course association rules.

The system defines a set V of 12 courses. Each course is identified by a pair of public attributes (A,B), where A represents the subject area (in {{1,2,3}}) and B represents the difficulty phase (in {{1,2,3,4}}). All 12 (A,B) combinations appear exactly once.

There exists a fixed but unknown undirected course association graph G=(V,E). The edge set E is determined by a hidden decision rule R, which judges whether an associated learning path can be established between any two distinct courses (i.e., whether an edge exists).

I have specified a start course s={start} and an end course t={end}, and guarantee that at least one valid learning path exists from s to t.

Your goal is: infer rule R through queries, make correct predictions on untested course pairs, and provide a new valid path from s to t.

You can make "learning path validity queries": submit a course sequence of length k (k is greater than or equal to 2).

- Query format: courses are represented as (A,B), multiple courses separated by semicolons
- Feedback:
  - If all adjacent course pairs in the sequence allow associated learning paths, answer "Yes"
  - Otherwise answer "No" and provide the position index of the first invalid adjacent pair (starting from 1)

Note: Before submitting the final answer, you need to complete at least 8 different queries, with at least 5 queries of length 2 and at least 3 queries of length greater than or equal to 3.

Learning path validity query:
<query_path>(1,2);(1,3);(2,4)</query_path>

When you have collected enough information, submit all at once:

1. Rule description: describe your inferred course association decision rule in natural language (please include keywords like A and B attributes)
2. Path from s to t: all adjacent course pairs must not have appeared in previous queries
3. Additional predictions: submit 4 course pairs not appearing in previous queries, with 2 labeled as "connected" and 2 as "not_connected"

Submission format:
<answer>
rule: [your inferred rule description]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业柔性制造调度系统”。你需要推断出隐藏的工序流转规则。

系统设定了一个包含 12 个加工工序的集合 V，每个工序用一对公开属性 (A,B) 标识，其中 A 代表工艺类型（属于 {{1,2,3}}），B 代表洁净等级（属于 {{1,2,3,4}}）。所有 12 种 (A,B) 组合各出现一次。

存在一个固定但未知的物料流转无向图 G=(V,E)。边集 E 由一个隐藏的判定规则 R 决定，该规则判断任意两个不同工序之间是否允许直接流转物料（即是否存在连边）。

我已经指定了起点工序 s={start} 和终点工序 t={end}，保证存在至少一条从 s 到 t 的合法流转路径。

你的目标是：通过查询推断出规则 R，并在未被直接试探过的工序对上进行正确预测，同时给出一条新的从 s 到 t 的合法多道工序流转路径。

你可以进行"工序流转路径合法性查询"：提交一个长度 k（k 大于等于 2）的工序序列。

- 查询格式：工序用 (A,B) 表示，多个工序用分号分隔
- 反馈：
  - 若序列中所有相邻工序对都允许物料直接流转，回答"是"
  - 否则回答"否"，并给出首个不合法流转相邻对的位置索引（从 1 开始）

注意：在提交最终答案前，你需要完成至少 8 次不同的查询，其中至少 5 次为长度 2 的查询，至少 3 次为长度大于等于 3 的查询。

流转路径合法性查询：
<query_path>(1,2);(1,3);(2,4)</query_path>

当你收集足够信息后，需要一次性提交：

1. 规则描述：用自然语言描述你推断的物料流转判定规则（请在描述中包含 A 属性和 B 属性等关键词）
2. 从 s 到 t 的流转路径：所有相邻工序对必须是之前查询中未出现过的
3. 额外预测：提交 4 个未在之前查询中出现过的工序对，其中 2 个标注为"connected"（允许流转），2 个标注为"not_connected"（不允许流转）

提交格式：
<answer>
rule: [你推断的规则描述]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Flexible Manufacturing Scheduling System". You need to infer the hidden process routing rules.

The system defines a set V of 12 manufacturing processes. Each process is identified by a pair of public attributes (A,B), where A represents the process type (in {{1,2,3}}) and B represents the cleanliness grade (in {{1,2,3,4}}). All 12 (A,B) combinations appear exactly once.

There exists a fixed but unknown undirected material flow graph G=(V,E). The edge set E is determined by a hidden decision rule R, which judges whether direct material flow is allowed between any two distinct processes (i.e., whether an edge exists).

I have specified a start process s={start} and an end process t={end}, and guarantee that at least one valid routing path exists from s to t.

Your goal is: infer rule R through queries, make correct predictions on untested process pairs, and provide a new valid routing path from s to t.

You can make "process routing path validity queries": submit a process sequence of length k (k is greater than or equal to 2).

- Query format: processes are represented as (A,B), multiple processes separated by semicolons
- Feedback:
  - If all adjacent process pairs in the sequence allow direct material flow, answer "Yes"
  - Otherwise answer "No" and provide the position index of the first invalid adjacent pair (starting from 1)

Note: Before submitting the final answer, you need to complete at least 8 different queries, with at least 5 queries of length 2 and at least 3 queries of length greater than or equal to 3.

Routing path validity query:
<query_path>(1,2);(1,3);(2,4)</query_path>

When you have collected enough information, submit all at once:

1. Rule description: describe your inferred material flow decision rule in natural language (please include keywords like A and B attributes)
2. Routing path from s to t: all adjacent process pairs must not have appeared in previous queries
3. Additional predictions: submit 4 process pairs not appearing in previous queries, with 2 labeled as "connected" and 2 as "not_connected"

Submission format:
<answer>
rule: [your inferred rule description]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>
"""

    contextualized_rule_zh_5 = """\
欢迎使用“法律合规审查推演系统”。你需要推断出隐藏的审批流转规则。

系统设定了一个包含 12 个审批节点的集合 V，每个节点用一对公开属性 (A,B) 标识，其中 A 代表法域（属于 {{1,2,3}}），B 代表效力层级（属于 {{1,2,3,4}}）。所有 12 种 (A,B) 组合各出现一次。

存在一个固定但未知的合规审查无向图 G=(V,E)。边集 E 由一个隐藏的判定规则 R 决定，该规则判断任意两个不同节点之间是否可以形成合规审查流转许可（即是否存在连边）。

我已经指定了首位审批节点 s={start} 和末位审批节点 t={end}，保证存在至少一条从 s 到 t 的合法连贯审查链。

你的目标是：通过查询推断出规则 R，并在未被直接试探过的节点对上进行正确预测，同时给出一条新的从 s 到 t 的合法合规审批链条。

你可以进行"合规审批链合法性查询"：提交一个长度 k（k 大于等于 2）的审批节点序列。

- 查询格式：节点用 (A,B) 表示，多个节点用分号分隔
- 反馈：
  - 若序列中所有相邻节点对都允许合规流转许可，回答"是"
  - 否则回答"否"，并给出首个不合法流转相邻对的位置索引（从 1 开始）

注意：在提交最终答案前，你需要完成至少 8 次不同的查询，其中至少 5 次为长度 2 的查询，至少 3 次为长度大于等于 3 的查询。

审批链合法性查询：
<query_path>(1,2);(1,3);(2,4)</query_path>

当你收集足够信息后，需要一次性提交：

1. 规则描述：用自然语言描述你推断的审查流转判定规则（请在描述中包含 A 属性和 B 属性等关键词）
2. 从 s 到 t 的审查链：所有相邻节点对必须是之前查询中未出现过的
3. 额外预测：提交 4 个未在之前查询中出现过的节点对，其中 2 个标注为"connected"（允许流转），2 个标注为"not_connected"（不允许流转）

提交格式：
<answer>
rule: [你推断的规则描述]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Legal Compliance Review System". You need to infer the hidden approval routing rules.

The system defines a set V of 12 approval nodes. Each node is identified by a pair of public attributes (A,B), where A represents the legal domain (in {{1,2,3}}) and B represents the effectiveness level (in {{1,2,3,4}}). All 12 (A,B) combinations appear exactly once.

There exists a fixed but unknown undirected compliance review graph G=(V,E). The edge set E is determined by a hidden decision rule R, which judges whether a compliance review chain can be formed between any two distinct nodes (i.e., whether an edge exists).

I have specified an initial approval node s={start} and a final approval node t={end}, and guarantee that at least one valid compliance review chain exists from s to t.

Your goal is: infer rule R through queries, make correct predictions on untested node pairs, and provide a new valid compliance review chain from s to t.

You can make "compliance review chain validity queries": submit a node sequence of length k (k is greater than or equal to 2).

- Query format: nodes are represented as (A,B), multiple nodes separated by semicolons
- Feedback:
  - If all adjacent node pairs in the sequence allow compliance routing, answer "Yes"
  - Otherwise answer "No" and provide the position index of the first invalid adjacent pair (starting from 1)

Note: Before submitting the final answer, you need to complete at least 8 different queries, with at least 5 queries of length 2 and at least 3 queries of length greater than or equal to 3.

Approval chain validity query:
<query_path>(1,2);(1,3);(2,4)</query_path>

When you have collected enough information, submit all at once:

1. Rule description: describe your inferred approval routing decision rule in natural language (please include keywords like A and B attributes)
2. Review chain from s to t: all adjacent node pairs must not have appeared in previous queries
3. Additional predictions: submit 4 node pairs not appearing in previous queries, with 2 labeled as "connected" and 2 as "not_connected"

Submission format:
<answer>
rule: [your inferred rule description]
path: (A1,B1);(A2,B2);...;(An,Bn)
predictions: (A1,B1)-(A2,B2):connected, (A3,B3)-(A4,B4):connected, (A5,B5)-(A6,B6):not_connected, (A7,B7)-(A8,B8):not_connected
</answer>
"""

    tags = ["answer", "query_path"]
    reasoning_type = "归纳推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "start": "(1,1)",
                "end": "(1,4)",
                "rule_type": "same_A",
                "rule_desc": "当且仅当两个节点的 A 属性相同时存在边"
            },
            2: {
                "start": "(2,1)",
                "end": "(2,4)",
                "rule_type": "B_diff_le_1",
                "rule_desc": "当且仅当两个节点的 B 属性相差小于等于 1 时存在边"
            },
            3: {
                "start": "(1,1)",
                "end": "(3,4)",
                "rule_type": "same_A_or_B",
                "rule_desc": "当且仅当两个节点的 A 属性相同或 B 属性相同时存在边"
            },
            4: {
                "start": "(1,1)",
                "end": "(3,4)",
                "rule_type": "sum_even",
                "rule_desc": "当且仅当两个节点的 A+B 之和均为偶数或均为奇数时存在边"
            },
            5: {
                "start": "(1,1)",
                "end": "(3,4)",
                "rule_type": "adjacent_grid",
                "rule_desc": "当且仅当两个节点满足以下条件之一时存在边：(1) A 相同且 B 相差小于等于 1；(2) B 相同且 A 相差小于等于 1"
            }
        },
        "en": {
            1: {
                "start": "(1,1)",
                "end": "(1,4)",
                "rule_type": "same_A",
                "rule_desc": "An edge exists if and only if two nodes have the same A attribute"
            },
            2: {
                "start": "(2,1)",
                "end": "(2,4)",
                "rule_type": "B_diff_le_1",
                "rule_desc": "An edge exists if and only if the difference of B attributes is at most 1"
            },
            3: {
                "start": "(1,1)",
                "end": "(3,4)",
                "rule_type": "same_A_or_B",
                "rule_desc": "An edge exists if and only if two nodes have the same A attribute or the same B attribute"
            },
            4: {
                "start": "(1,1)",
                "end": "(3,4)",
                "rule_type": "sum_even",
                "rule_desc": "An edge exists if and only if both nodes have A+B sums of the same parity"
            },
            5: {
                "start": "(1,1)",
                "end": "(3,4)",
                "rule_type": "adjacent_grid",
                "rule_desc": "An edge exists if and only if: (1) nodes have the same A and B differs by at most 1, or (2) nodes have the same B and A differs by at most 1"
            }
        }
    }

    def __init__(self, config):
        self.queried_pairs = set()
        self.query_count = 0
        self.short_query_count = 0
        self.long_query_count = 0
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["start"] = cfg["start"]
        self._game_info["end"] = cfg["end"]
        
        self.start_node = self._parse_node(cfg["start"])
        self.end_node = self._parse_node(cfg["end"])
        self.rule_type = cfg["rule_type"]
        self.rule_desc = cfg["rule_desc"]

    def _parse_node(self, node_str):
        match = re.match(r'\((\d+),(\d+)\)', node_str.strip())
        if not match:
            return None
        return (int(match.group(1)), int(match.group(2)))

    def _node_to_str(self, node):
        return f"({node[0]},{node[1]})"

    def _has_edge(self, node1, node2):
        if node1 == node2:
            return False
        
        a1, b1 = node1
        a2, b2 = node2

        if self.rule_type == "same_A":
            return a1 == a2
        elif self.rule_type == "B_diff_le_1":
            return abs(b1 - b2) <= 1
        elif self.rule_type == "same_A_or_B":
            return a1 == a2 or b1 == b2
        elif self.rule_type == "sum_even":
            return (a1 + b1) % 2 == (a2 + b2) % 2
        elif self.rule_type == "adjacent_grid":
            return (a1 == a2 and abs(b1 - b2) <= 1) or (b1 == b2 and abs(a1 - a2) <= 1)
        else:
            return False

    def _normalize_pair(self, node1, node2):
        return tuple(sorted([node1, node2]))

    def _check_rule_equivalence(self, described_rule):
        described_rule_lower = described_rule.lower()
        
        if self.rule_type == "same_A":
            if self.config.language == "zh":
                keywords = ["a 属性相同", "a属性相同", "a 相同", "a相同"]
            else:
                keywords = ["same a", "a attribute", "same a attribute"]
            return any(kw in described_rule_lower for kw in keywords)
        
        elif self.rule_type == "B_diff_le_1":
            if self.config.language == "zh":
                keywords = ["b 属性", "b属性", "b 相差", "b相差"]
                keywords2 = ["1", "小于等于"]
            else:
                keywords = ["b attribute", "b differ", "b diff", "difference of b"]
                keywords2 = ["1", "at most"]
            return any(kw in described_rule_lower for kw in keywords) and any(kw in described_rule_lower for kw in keywords2)
        
        elif self.rule_type == "same_A_or_B":
            if self.config.language == "zh":
                has_a = any(kw in described_rule_lower for kw in ["a 属性", "a属性"])
                has_b = any(kw in described_rule_lower for kw in ["b 属性", "b属性"])
                has_or = any(kw in described_rule_lower for kw in ["或", "任一"])
            else:
                has_a = any(kw in described_rule_lower for kw in ["same a", "a attribute"])
                has_b = any(kw in described_rule_lower for kw in ["same b", "b attribute"])
                has_or = "or" in described_rule_lower
            return has_a and has_b and has_or
        
        elif self.rule_type == "sum_even":
            if self.config.language == "zh":
                keywords = ["和", "奇偶", "偶数", "奇数"]
            else:
                keywords = ["sum", "parity", "even", "odd"]
            return sum(1 for kw in keywords if kw in described_rule_lower) >= 2
        
        elif self.rule_type == "adjacent_grid":
            if self.config.language == "zh":
                keywords = ["a 相同", "a相同", "b 相差", "b相差", "b 相同", "b相同", "a 相差", "a相差"]
            else:
                keywords = ["same a", "same b", "a differs", "b differs", "at most 1", "adjacent"]
            return sum(1 for kw in keywords if kw in described_rule_lower) >= 2
        
        return False

    def evaluate(self, parsed_info):
        try:
            answer_text = parsed_info["answer"].strip()
            
            rule_match = re.search(r'rule:\s*(.+?)(?=path:|$)', answer_text, re.IGNORECASE | re.DOTALL)
            path_match = re.search(r'path:\s*(.+?)(?=predictions:|$)', answer_text, re.IGNORECASE | re.DOTALL)
            pred_match = re.search(r'predictions:\s*(.+?)$', answer_text, re.IGNORECASE | re.DOTALL)
            
            if not (rule_match and path_match and pred_match):
                return False
            
            rule_text = rule_match.group(1).strip()
            path_text = path_match.group(1).strip()
            pred_text = pred_match.group(1).strip()
            
            if not self._check_rule_equivalence(rule_text):
                return False
            
            path_nodes = []
            for node_str in path_text.split(';'):
                node = self._parse_node(node_str.strip())
                if node is None:
                    return False
                path_nodes.append(node)
            
            if len(path_nodes) < 2:
                return False
            
            if path_nodes[0] != self.start_node or path_nodes[-1] != self.end_node:
                return False
            
            for i in range(len(path_nodes) - 1):
                pair = self._normalize_pair(path_nodes[i], path_nodes[i+1])
                if pair in self.queried_pairs:
                    return False
                if not self._has_edge(path_nodes[i], path_nodes[i+1]):
                    return False
            
            predictions = []
            for pred in pred_text.split(','):
                pred = pred.strip()
                match = re.match(r'\((\d+),(\d+)\)-\((\d+),(\d+)\):(connected|not_connected)', pred)
                if not match:
                    return False
                
                node1 = (int(match.group(1)), int(match.group(2)))
                node2 = (int(match.group(3)), int(match.group(4)))
                label = match.group(5)
                
                pair = self._normalize_pair(node1, node2)
                if pair in self.queried_pairs:
                    return False
                
                predictions.append((node1, node2, label))
            
            if len(predictions) != 4:
                return False
            
            connected_count = sum(1 for _, _, label in predictions if label == "connected")
            if connected_count != 2:
                return False
            
            for node1, node2, label in predictions:
                actual_connected = self._has_edge(node1, node2)
                predicted_connected = (label == "connected")
                if actual_connected != predicted_connected:
                    return False
            
            return True
            
        except Exception as e:
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_path" not in parsed_info:
            if self.config.language == "zh":
                return "错误：未找到有效的查询标签。"
            else:
                return "Error: No valid query tag found."
        
        path_text = parsed_info["query_path"].strip()
        
        nodes = []
        for node_str in path_text.split(';'):
            node = self._parse_node(node_str.strip())
            if node is None:
                if self.config.language == "zh":
                    return f"错误：无效的节点格式 '{node_str.strip()}'。"
                else:
                    return f"Error: Invalid node format '{node_str.strip()}'."
            
            a, b = node
            if a not in [1, 2, 3] or b not in [1, 2, 3, 4]:
                if self.config.language == "zh":
                    return f"错误：节点 {self._node_to_str(node)} 超出范围。"
                else:
                    return f"Error: Node {self._node_to_str(node)} out of range."
            
            nodes.append(node)
        
        if len(nodes) < 2:
            if self.config.language == "zh":
                return "错误：路径长度必须大于等于 2。"
            else:
                return "Error: Path length must be at least 2."
        
        self.query_count += 1
        if len(nodes) == 2:
            self.short_query_count += 1
        else:
            self.long_query_count += 1
        
        for i in range(len(nodes) - 1):
            pair = self._normalize_pair(nodes[i], nodes[i+1])
            self.queried_pairs.add(pair)
        
        for i in range(len(nodes) - 1):
            if not self._has_edge(nodes[i], nodes[i+1]):
                if self.config.language == "zh":
                    return f"否，断点位置：{i+1}"
                else:
                    return f"No, break at position: {i+1}"
        
        if self.config.language == "zh":
            return "是"
        else:
            return "Yes"

    def _cf_make_wrong(self, correct: str) -> str:
        if self.config.language == "zh":
            if correct == "是":
                return "否，断点位置：1"
            if correct.startswith("否"):
                return "是"
        elif self.config.language == "en":
            if correct == "Yes":
                return "No, break at position: 1"
            if correct.startswith("No"):
                return "Yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        nodes = []
        for a in range(1, 4):
            for b in range(1, 5):
                nodes.append((a, b))
        
        for u, v in itertools.combinations(nodes, 2):
            u_str = self._node_to_str(u)
            v_str = self._node_to_str(v)
            query_content = f"{u_str};{v_str}"
            
            has_edge = self._has_edge(u, v)
            
            if self.config.language == "zh":
                answer = "是" if has_edge else "否，断点位置：1"
            else:
                answer = "Yes" if has_edge else "No, break at position: 1"
            
            queries.append({
                "query": f"<query_path>{query_content}</query_path>",
                "answer": answer
            })
            
        return queries

    def step(self, response: str):
        try:
            parsed_info = self.parse(response)
            if "answer" in parsed_info:
                if self.query_count < 8 or self.short_query_count < 5 or self.long_query_count < 3:
                    if self.config.language == "zh":
                        res = f"错误：查询次数不足。需要至少 8 次查询（当前 {self.query_count} 次），其中至少 5 次长度为 2 的查询（当前 {self.short_query_count} 次），至少 3 次长度大于等于 3 的查询（当前 {self.long_query_count} 次）。"
                    else:
                        res = f"Error: Insufficient queries. Need at least 8 queries (current {self.query_count}), with at least 5 queries of length 2 (current {self.short_query_count}) and at least 3 queries of length >= 3 (current {self.long_query_count})."
                    self.state.set_state("failed", "insufficient queries")
                    self.state.add_message("user", res)
                else:
                    is_success = self.evaluate(parsed_info)
                    if is_success:
                        res = "答案完全正确！" if self.config.language == "zh" else "Answer is completely correct!"
                        self.state.set_state("success", "success")
                        self.state.add_message("user", res)
                    else:
                        res = "答案错误。" if self.config.language == "zh" else "Incorrect answer."
                        self.state.set_state("failed", "incorrect answer")
                        self.state.add_message("user", res)
            else:
                game_response = self.produce_response(parsed_info)
                self.state.add_message("user", game_response)
                
        except Exception as e:
            self.state.set_state("failed", str(e))
        
        return self.state