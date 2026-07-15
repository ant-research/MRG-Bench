from .base import Game
import re

class ElementMappingGame(Game):

    game_rule_zh = """\
我们来玩一个"元素映射推理"游戏，规则如下：

游戏设定了一个元素集合 U = {R1, R2, R3, B1, B2, B3, G1, G2}。
这个集合被划分为三个分组：
- R 组：R1, R2, R3（组内顺序：R1 < R2 < R3）
- B 组：B1, B2, B3（组内顺序：B1 < B2 < B3）
- G 组：G1, G2（组内顺序：G1 < G2）

在同一组内，按照上述顺序，每个元素与其前后相邻的元素为"相邻元素"。例如 R2 的相邻元素是 R1 和 R3。

我已经秘密选择了一种**映射规则**，该规则定义了一个函数 f，对于任意元素 x，会返回一个元素集合 f(x)。有四种可能的映射规则（A、B、C、D）：

- 规则 A：f(x) = x 所在组的所有其他元素（不包括 x 自己）
- 规则 B：f(x) = x 所在组的所有元素（包括 x 自己）
- 规则 C：f(x) = x 在其组内的所有相邻元素（不包括 x 自己）
- 规则 D：f(x) = x 所在组中，除了 x 自己和 x 的相邻元素之外的所有元素

整个游戏中，我使用的映射规则是固定的，对所有查询保持一致。

你的目标是：
1. 识别出我使用的是哪一种映射规则（A、B、C 或 D）
2. 在标准规则 A 的定义下，计算出 B2 的映射结果（即 B 组中除 B2 外的所有元素），并按组内顺序从小到大输出
3. 提供至少两条查询证据，证明你的推理过程

你可以反复向我提出以下三类问题（每次仅限一个问题）：

1. **名单查询**：询问 f(X) 包含哪些元素。我会返回一个元素列表（列表顺序随机，不传递额外信息）。
2. **成员判定**：询问某元素 Y 是否属于 f(X)。我会回答"是"或"否"。
3. **数量查询**：询问 f(X) 中有多少个元素。我会回答一个整数。

**重要约束**：
- 在提交最终答案前，你必须对至少两个不同的元素 X 进行过查询（查询类型可以相同或不同）
- 每次只能提出一个问题

每次询问必须使用以下 XML 格式（只能包含一个标签）：

- 名单查询（例如查询 R2 的映射结果）：
<query_list>R2</query_list>

- 成员判定（例如询问 B1 是否在 R2 的映射结果中）：
<query_member>R2,B1</query_member>

- 数量查询（例如查询 G1 的映射结果包含多少元素）：
<query_count>G1</query_count>

提交最终答案时，必须包含以下三部分信息：
1. 识别出的映射规则（A、B、C 或 D）
2. 在规则 A 下 B2 的映射结果，按组内顺序输出（用逗号分隔）
3. 至少两条查询证据（格式：元素=结果）

答案格式如下：
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

若答案错误、格式不符或证据不足，游戏失败。
"""

    game_rule_en = """\
Let's play an "Element Mapping Inference" game. Here are the rules:

The game defines an element set U = {R1, R2, R3, B1, B2, B3, G1, G2}.
This set is divided into three groups:
- Group R: R1, R2, R3 (order within group: R1 < R2 < R3)
- Group B: B1, B2, B3 (order within group: B1 < B2 < B3)
- Group G: G1, G2 (order within group: G1 < G2)

Within the same group, according to the above order, each element's adjacent elements are those directly before or after it. For example, R2's adjacent elements are R1 and R3.

I have secretly chosen a **mapping rule** that defines a function f. For any element x, it returns an element set f(x). There are four possible mapping rules (A, B, C, D):

- Rule A: f(x) = all other elements in x's group (excluding x itself)
- Rule B: f(x) = all elements in x's group (including x itself)
- Rule C: f(x) = all adjacent elements of x within its group (excluding x itself)
- Rule D: f(x) = all elements in x's group, excluding x itself and x's adjacent elements

Throughout the game, the mapping rule I use is fixed and consistent for all queries.

Your goals are:
1. Identify which mapping rule I am using (A, B, C, or D)
2. Under the standard Rule A definition, calculate the mapping result for B2 (i.e., all elements in group B except B2), and output them in ascending order within the group
3. Provide at least two query evidences to prove your reasoning

You can repeatedly ask me the following three types of questions (one per turn):

1. **List Query**: Ask which elements are included in f(X). I will return a list of elements (list order is random and carries no additional information).
2. **Membership Query**: Ask whether element Y belongs to f(X). I will answer "Yes" or "No".
3. **Count Query**: Ask how many elements are in f(X). I will answer with an integer.

**Important Constraints**:
- Before submitting your final answer, you must have queried at least two different elements X (query types can be same or different)
- Each turn you can only ask one question

Each query must use the following XML format (only one tag allowed):

- List Query (e.g., query the mapping result of R2):
<query_list>R2</query_list>

- Membership Query (e.g., ask if B1 is in the mapping result of R2):
<query_member>R2,B1</query_member>

- Count Query (e.g., query how many elements are in the mapping result of G1):
<query_count>G1</query_count>

When submitting the final answer, you must include the following three parts:
1. The identified mapping rule (A, B, C, or D)
2. The mapping result of B2 under Rule A, output in group order (comma-separated)
3. At least two query evidences (format: element=result)

Answer format:
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

If the answer is wrong, format is invalid, or evidence is insufficient, the game fails.
"""

    contextualized_rule_zh_1 = """\
欢迎使用"城市交通网络应急联动调度系统"。我们来进行一次"联动站点映射推理"测试，规则如下：

系统设定了一个交通枢纽集合 U = {R1, R2, R3, B1, B2, B3, G1, G2}。
这个集合被划分为三条线路：
- R 组：红线地铁站 R1, R2, R3（沿线顺序：R1 < R2 < R3）
- B 组：蓝线地铁站 B1, B2, B3（沿线顺序：B1 < B2 < B3）
- G 组：绿线地铁站 G1, G2（沿线顺序：G1 < G2）

在同一线路内，按照上述顺序，每个站点与其前后相邻的站点为"相邻站点"。例如 R2 的相邻站点是 R1 和 R3。

系统已秘密配置了一种**应急调度规则**，该规则定义了一个函数 f，对于任意站点 x，会返回一个受波及的站点集合 f(x)。有四种可能的规则（A、B、C、D）：

- 规则 A：f(x) = x 所在线路的所有其他站点（不包括 x 自身）
- 规则 B：f(x) = x 所在线路的所有站点（包括 x 自身）
- 规则 C：f(x) = x 在其线路内的所有相邻站点（不包括 x 自身）
- 规则 D：f(x) = x 所在线路中，除了 x 自身和相邻站点之外的所有站点

整个测试中，系统使用的调度规则是固定的，对所有查询保持一致。

你的目标是：
1. 识别出当前系统使用的是哪一种调度规则（A、B、C 或 D）
2. 在标准规则 A 的定义下，计算出 B2 的调度结果（即蓝线中除 B2 外的所有站点），并按沿线顺序从小到大输出
3. 提供至少两条查询证据，证明你的推理过程

你可以反复向我提出以下三类查询（每次仅限一个查询）：

1. **名单查询**：询问 f(X) 包含哪些站点。我会返回一个站点列表（列表顺序随机，不传递额外信息）。
2. **成员判定**：询问某站点 Y 是否属于 f(X)。我会回答"是"或"否"。
3. **数量查询**：询问 f(X) 中有多少个站点。我会回答一个整数。

**重要约束**：
- 在提交最终答案前，你必须对至少两个不同的站点 X 进行过查询（查询类型可以相同或不同）
- 每次只能提出一个问题

每次询问必须使用以下 XML 格式（只能包含一个标签）：

- 名单查询（例如查询 R2 的调度结果）：
<query_list>R2</query_list>

- 成员判定（例如询问 B1 是否在 R2 的调度结果中）：
<query_member>R2,B1</query_member>

- 数量查询（例如查询 G1 的调度结果包含多少站点）：
<query_count>G1</query_count>

提交最终答案时，必须包含以下三部分信息：
1. 识别出的调度规则（A、B、C 或 D）
2. 在规则 A 下 B2 的调度结果，按沿线顺序输出（用逗号分隔）
3. 至少两条查询证据（格式：站点=结果）

答案格式如下：
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

若答案错误、格式不符或证据不足，测试失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Urban Traffic Network Emergency Linkage Dispatch System". Let's conduct a "Linked Station Mapping Inference" test. Here are the rules:

The system defines a transportation hub set U = {R1, R2, R3, B1, B2, B3, G1, G2}.
This set is divided into three transit lines:
- Group R: Red Line stations R1, R2, R3 (route order: R1 < R2 < R3)
- Group B: Blue Line stations B1, B2, B3 (route order: B1 < B2 < B3)
- Group G: Green Line stations G1, G2 (route order: G1 < G2)

Within the same transit line, according to the above order, each station's adjacent stations are those directly before or after it. For example, R2's adjacent stations are R1 and R3.

The system has secretly configured an **emergency dispatch rule** that defines a function f. For any station x, it returns an affected station set f(x). There are four possible rules (A, B, C, D):

- Rule A: f(x) = all other stations on x's transit line (excluding x itself)
- Rule B: f(x) = all stations on x's transit line (including x itself)
- Rule C: f(x) = all adjacent stations of x within its transit line (excluding x itself)
- Rule D: f(x) = all stations on x's transit line, excluding x itself and x's adjacent stations

Throughout the test, the dispatch rule used by the system is fixed and consistent for all queries.

Your goals are:
1. Identify which dispatch rule the system is using (A, B, C, or D)
2. Under the standard Rule A definition, calculate the dispatch result for B2 (i.e., all stations on the Blue Line except B2), and output them in ascending route order
3. Provide at least two query evidences to prove your reasoning

You can repeatedly ask me the following three types of queries (one per turn):

1. **List Query**: Ask which stations are included in f(X). I will return a list of stations (list order is random and carries no additional information).
2. **Membership Query**: Ask whether station Y belongs to f(X). I will answer "Yes" or "No".
3. **Count Query**: Ask how many stations are in f(X). I will answer with an integer.

**Important Constraints**:
- Before submitting your final answer, you must have queried at least two different stations X (query types can be same or different)
- Each turn you can only ask one question

Each query must use the following XML format (only one tag allowed):

- List Query (e.g., query the dispatch result of R2):
<query_list>R2</query_list>

- Membership Query (e.g., ask if B1 is in the dispatch result of R2):
<query_member>R2,B1</query_member>

- Count Query (e.g., query how many stations are in the dispatch result of G1):
<query_count>G1</query_count>

When submitting the final answer, you must include the following three parts:
1. The identified dispatch rule (A, B, C, or D)
2. The dispatch result of B2 under Rule A, output in route order (comma-separated)
3. At least two query evidences (format: station=result)

Answer format:
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

If the answer is wrong, format is invalid, or evidence is insufficient, the test fails.
"""

    contextualized_rule_zh_2 = """\
欢迎进入"医院传染病房接触追踪与隔离系统"。我们来进行一次"隔离范围推演"演练，规则如下：

系统监控的重点病房集合为 U = {R1, R2, R3, B1, B2, B3, G1, G2}。
这个集合被划分为三个重点科室：
- R 组：呼吸科病房 R1, R2, R3（走廊顺序：R1 < R2 < R3）
- B 组：血液科病房 B1, B2, B3（走廊顺序：B1 < B2 < B3）
- G 组：胃肠科病房 G1, G2（走廊顺序：G1 < G2）

在同一科室走廊内，按照上述顺序，每个病房与其前后相邻的病房为"相邻病房"。例如 R2 的相邻病房是 R1 和 R3。

系统已秘密配置了一种**感染追踪规则**，该规则定义了一个函数 f，对于任意出现确诊病例的病房 x，会返回一个需紧急隔离的病房集合 f(x)。有四种可能的规则（A、B、C、D）：

- 规则 A：f(x) = x 所在科室的所有其他病房（不包括 x 自身）
- 规则 B：f(x) = x 所在科室的所有病房（包括 x 自身）
- 规则 C：f(x) = x 在其科室内的所有相邻病房（不包括 x 自身）
- 规则 D：f(x) = x 所在科室中，除了 x 自身和相邻病房之外的所有病房

整个演练中，系统使用的追踪规则是固定的，对所有查询保持一致。

你的目标是：
1. 识别出当前系统使用的是哪一种追踪规则（A、B、C 或 D）
2. 在标准规则 A 的定义下，计算出 B2 的隔离结果（即血液科中除 B2 外的所有病房），并按走廊顺序从小到大输出
3. 提供至少两条查询证据，证明你的推理过程

你可以反复向我提出以下三类查询（每次仅限一个查询）：

1. **名单查询**：询问 f(X) 包含哪些病房。我会返回一个病房列表（列表顺序随机，不传递额外信息）。
2. **成员判定**：询问某病房 Y 是否属于 f(X)。我会回答"是"或"否"。
3. **数量查询**：询问 f(X) 中有多少个病房。我会回答一个整数。

**重要约束**：
- 在提交最终答案前，你必须对至少两个不同的病房 X 进行过查询（查询类型可以相同或不同）
- 每次只能提出一个问题

每次询问必须使用以下 XML 格式（只能包含一个标签）：

- 名单查询（例如查询 R2 的隔离结果）：
<query_list>R2</query_list>

- Membership Query（例如询问 B1 是否在 R2 的隔离结果中）：
<query_member>R2,B1</query_member>

- 数量查询（例如查询 G1 的隔离结果包含多少病房）：
<query_count>G1</query_count>

提交最终答案时，必须包含以下三部分信息：
1. 识别出的追踪规则（A、B、C 或 D）
2. 在规则 A 下 B2 的隔离结果，按走廊顺序输出（用逗号分隔）
3. 至少两条查询证据（格式：病房=结果）

答案格式如下：
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

若答案错误、格式不符或证据不足，演练失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Hospital Infectious Ward Contact Tracing and Isolation System". Let's conduct an "Isolation Scope Inference" drill. Here are the rules:

The system monitors a high-risk ward set U = {R1, R2, R3, B1, B2, B3, G1, G2}.
This set is divided into three key departments:
- Group R: Respiratory wards R1, R2, R3 (corridor order: R1 < R2 < R3)
- Group B: Hematology wards B1, B2, B3 (corridor order: B1 < B2 < B3)
- Group G: Gastroenterology wards G1, G2 (corridor order: G1 < G2)

Within the same department corridor, according to the above order, each ward's adjacent wards are those directly before or after it. For example, R2's adjacent wards are R1 and R3.

The system has secretly configured an **infection tracing rule** that defines a function f. For any ward x with a confirmed case, it returns an urgent isolation ward set f(x). There are four possible rules (A, B, C, D):

- Rule A: f(x) = all other wards in x's department (excluding x itself)
- Rule B: f(x) = all wards in x's department (including x itself)
- Rule C: f(x) = all adjacent wards of x within its department (excluding x itself)
- Rule D: f(x) = all wards in x's department, excluding x itself and x's adjacent wards

Throughout the drill, the tracing rule used by the system is fixed and consistent for all queries.

Your goals are:
1. Identify which tracing rule the system is using (A, B, C, or D)
2. Under the standard Rule A definition, calculate the isolation result for B2 (i.e., all wards in the Hematology department except B2), and output them in ascending corridor order
3. Provide at least two query evidences to prove your reasoning

You can repeatedly ask me the following three types of queries (one per turn):

1. **List Query**: Ask which wards are included in f(X). I will return a list of wards (list order is random and carries no additional information).
2. **Membership Query**: Ask whether ward Y belongs to f(X). I will answer "Yes" or "No".
3. **Count Query**: Ask how many wards are in f(X). I will answer with an integer.

**Important Constraints**:
- Before submitting your final answer, you must have queried at least two different wards X (query types can be same or different)
- Each turn you can only ask one question

Each query must use the following XML format (only one tag allowed):

- List Query (e.g., query the isolation result of R2):
<query_list>R2</query_list>

- Membership Query (e.g., ask if B1 is in the isolation result of R2):
<query_member>R2,B1</query_member>

- Count Query (e.g., query how many wards are in the isolation result of G1):
<query_count>G1</query_count>

When submitting the final answer, you must include the following three parts:
1. The identified tracing rule (A, B, C, or D)
2. The isolation result of B2 under Rule A, output in corridor order (comma-separated)
3. At least two query evidences (format: ward=result)

Answer format:
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

If the answer is wrong, format is invalid, or evidence is insufficient, the drill fails.
"""

    contextualized_rule_zh_3 = """\
欢迎使用"学校教研督导与互评分配系统"。我们来进行一次"互相听课分配机制"推演，规则如下：

系统录入了参与本轮教学互评的教师集合 U = {R1, R2, R3, B1, B2, B3, G1, G2}。
该集合被划分为三个核心教研组：
- R 组：文科教研组教师 R1, R2, R3（工位顺序：R1 < R2 < R3）
- B 组：理科教研组教师 B1, B2, B3（工位顺序：B1 < B2 < B3）
- G 组：艺术教研组教师 G1, G2（工位顺序：G1 < G2）

在同一教研组内，按照上述工位排列顺序，每位教师与在其旁边的教师为"相邻工位教师"。例如 R2 的相邻工位教师是 R1 和 R3。

系统已秘密生成了一种**听课督导规则**，该规则定义了一个函数 f，对于任意教师 x，会返回该教师需前往听课评审的教师集合 f(x)。有四种可能的规则（A、B、C、D）：

- 规则 A：f(x) = x 所在教研组的所有其他教师（不包括 x 自身）
- 规则 B：f(x) = x 所在教研组的所有教师（包括 x 自身的反思自评）
- 规则 C：f(x) = x 在其教研组内的所有相邻工位教师（不包括 x 自身）
- 规则 D：f(x) = x 所在教研组中，除了 x 自身和相邻工位教师之外的所有教师

整个推演中，系统使用的听课分配规则是固定的，对所有查询保持一致。

你的目标是：
1. 识别出当前系统使用的是哪一种听课分配规则（A、B、C 或 D）
2. 在标准规则 A 的定义下，计算出 B2 的分配结果（即理科组中除 B2 外的所有教师），并按工位顺序从小到大输出
3. 提供至少两条查询证据，证明你的推理过程

你可以反复向我提出以下三类查询（每次仅限一个查询）：

1. **名单查询**：询问 f(X) 包含哪些教师。我会返回一个教师列表（列表顺序随机，不传递额外信息）。
2. **成员判定**：询问某教师 Y 是否属于 f(X)。我会回答"是"或"否"。
3. **数量查询**：询问 f(X) 中有多少名教师。我会回答一个整数。

**重要约束**：
- 在提交最终答案前，你必须对至少两个不同的教师 X 进行过查询（查询类型可以相同或不同）
- 每次只能提出一个问题

每次询问必须使用以下 XML 格式（只能包含一个标签）：

- 名单查询（例如查询 R2 需要听评的教师结果）：
<query_list>R2</query_list>

- 成员判定（例如询问 B1 是否在 R2 的分配结果中）：
<query_member>R2,B1</query_member>

- 数量查询（例如查询 G1 需要听评多少名教师）：
<query_count>G1</query_count>

提交最终答案时，必须包含以下三部分信息：
1. 识别出的分配规则（A、B、C 或 D）
2. 在规则 A 下 B2 的分配结果，按工位顺序输出（用逗号分隔）
3. 至少两条查询证据（格式：教师=结果）

答案格式如下：
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

若答案错误、格式不符或证据不足，推演失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "School Teaching Research Supervision and Peer Review Allocation System". Let's conduct a "Peer Review Mechanism Inference", rules are as follows:

The system has registered a participating teacher set U = {R1, R2, R3, B1, B2, B3, G1, G2}.
This set is divided into three core teaching groups:
- Group R: Liberal Arts group teachers R1, R2, R3 (desk order: R1 < R2 < R3)
- Group B: Science group teachers B1, B2, B3 (desk order: B1 < B2 < B3)
- Group G: Arts group teachers G1, G2 (desk order: G1 < G2)

Within the same teaching group, according to the desk order, each teacher's adjacent teachers are those seated directly next to them. For example, R2's adjacent teachers are R1 and R3.

The system has secretly generated a **peer review allocation rule** that defines a function f. For any teacher x, it returns a set of teachers f(x) that x must evaluate. There are four possible rules (A, B, C, D):

- Rule A: f(x) = all other teachers in x's teaching group (excluding x itself)
- Rule B: f(x) = all teachers in x's teaching group (including self-evaluation for x)
- Rule C: f(x) = all adjacent desk teachers of x within its group (excluding x itself)
- Rule D: f(x) = all teachers in x's teaching group, excluding x itself and adjacent desk teachers

Throughout the inference, the allocation rule used by the system is fixed and consistent for all queries.

Your goals are:
1. Identify which allocation rule the system is using (A, B, C, or D)
2. Under the standard Rule A definition, calculate the allocation result for B2 (i.e., all teachers in the Science group except B2), and output them in ascending desk order
3. Provide at least two query evidences to prove your reasoning

You can repeatedly ask me the following three types of queries (one per turn):

1. **List Query**: Ask which teachers are included in f(X). I will return a list of teachers (list order is random and carries no additional information).
2. **Membership Query**: Ask whether teacher Y belongs to f(X). I will answer "Yes" or "No".
3. **Count Query**: Ask how many teachers are in f(X). I will answer with an integer.

**Important Constraints**:
- Before submitting your final answer, you must have queried at least two different teachers X (query types can be same or different)
- Each turn you can only ask one question

Each query must use the following XML format (only one tag allowed):

- List Query (e.g., query the allocation result of R2):
<query_list>R2</query_list>

- Membership Query (e.g., ask if B1 is in the allocation result of R2):
<query_member>R2,B1</query_member>

- Count Query (e.g., query how many teachers are in the allocation result of G1):
<query_count>G1</query_count>

When submitting the final answer, you must include the following three parts:
1. The identified allocation rule (A, B, C, or D)
2. The allocation result of B2 under Rule A, output in desk order (comma-separated)
3. At least two query evidences (format: teacher=result)

Answer format:
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

If the answer is wrong, format is invalid, or evidence is insufficient, the inference fails.
"""

    contextualized_rule_zh_4 = """\
欢迎操作"工厂流水线设备异常关联预警系统"。我们来进行一次"故障波及范围排查"模拟，规则如下：

系统监控的流水线设备集合为 U = {R1, R2, R3, B1, B2, B3, G1, G2}。
该集合被划分为三个主要生产车间：
- R 组：粗加工车间机床 R1, R2, R3（流水线顺序：R1 < R2 < R3）
- B 组：精加工车间机床 B1, B2, B3（流水线顺序：B1 < B2 < B3）
- G 组：质检车间设备 G1, G2（流水线顺序：G1 < G2）

在同一车间内，按照上述流水线加工顺序，每个设备与其前后紧邻的设备为"相邻设备"。例如 R2 的相邻设备是 R1 和 R3。

系统已秘密载入了一种**停机检修规则**，该规则定义了一个函数 f，对于任意发生异常的设备 x，会返回一组必须同步停机排查的关联设备集合 f(x)。有四种可能的规则（A、B、C、D）：

- 规则 A：f(x) = x 所在车间的所有其他设备（不包括 x 自身）
- 规则 B：f(x) = x 所在车间的所有设备（包括 x 自身）
- 规则 C：f(x) = x 在其车间内的所有相邻设备（不包括 x 自身）
- 规则 D：f(x) = x 所在车间中，除了 x 自身和相邻设备之外的所有设备

整个模拟中，系统使用的关联规则是固定的，对所有查询保持一致。

你的目标是：
1. 识别出当前系统使用的是哪一种关联规则（A、B、C 或 D）
2. 在标准规则 A 的定义下，计算出 B2 的波及结果（即精加工车间中除 B2 外的所有设备），并按流水线顺序从小到大输出
3. 提供至少两条查询证据，证明你的推理过程

你可以反复向我提出以下三类查询（每次仅限一个查询）：

1. **名单查询**：询问 f(X) 包含哪些设备。我会返回一个设备列表（列表顺序随机，不传递额外信息）。
2. **成员判定**：询问某设备 Y 是否属于 f(X)。我会回答"是"或"否"。
3. **数量查询**：询问 f(X) 中有多少台设备。我会回答一个整数。

**重要约束**：
- 在提交最终答案前，你必须对至少两台不同的设备 X 进行过查询（查询类型可以相同或不同）
- 每次只能提出一个问题

每次询问必须使用以下 XML 格式（只能包含一个标签）：

- 名单查询（例如查询 R2 的同步停机结果）：
<query_list>R2</query_list>

- 成员判定（例如询问 B1 是否在 R2 的停机结果中）：
<query_member>R2,B1</query_member>

- 数量查询（例如查询 G1 的停机波及包含多少台设备）：
<query_count>G1</query_count>

提交最终答案时，必须包含以下三部分信息：
1. 识别出的关联规则（A、B、C 或 D）
2. 在规则 A 下 B2 的波及结果，按流水线顺序输出（用逗号分隔）
3. 至少两条查询证据（格式：设备=结果）

答案格式如下：
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

若答案错误、格式不符或证据不足，模拟排查失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Welcome to the "Factory Assembly Line Equipment Anomaly Associated Warning System". Let's conduct a "Failure Cascade Scope Troubleshooting" simulation. Here are the rules:

The system monitors an assembly line equipment set U = {R1, R2, R3, B1, B2, B3, G1, G2}.
This set is divided into three primary production workshops:
- Group R: Rough machining workshop machines R1, R2, R3 (assembly line order: R1 < R2 < R3)
- Group B: Precision machining workshop machines B1, B2, B3 (assembly line order: B1 < B2 < B3)
- Group G: Quality inspection workshop equipment G1, G2 (assembly line order: G1 < G2)

Within the same workshop, according to the assembly line processing order, each equipment's adjacent equipment are those directly before or after it. For example, R2's adjacent equipment are R1 and R3.

The system has secretly loaded a **downtime maintenance rule** that defines a function f. For any equipment x reporting an anomaly, it returns an associated equipment set f(x) that must be simultaneously shut down for inspection. There are four possible rules (A, B, C, D):

- Rule A: f(x) = all other equipment in x's workshop (excluding x itself)
- Rule B: f(x) = all equipment in x's workshop (including x itself)
- Rule C: f(x) = all adjacent equipment of x within its workshop (excluding x itself)
- Rule D: f(x) = all equipment in x's workshop, excluding x itself and x's adjacent equipment

Throughout the simulation, the associated rule used by the system is fixed and consistent for all queries.

Your goals are:
1. Identify which associated rule the system is using (A, B, C, or D)
2. Under the standard Rule A definition, calculate the cascade result for B2 (i.e., all equipment in the Precision machining workshop except B2), and output them in ascending assembly line order
3. Provide at least two query evidences to prove your reasoning

You can repeatedly ask me the following three types of queries (one per turn):

1. **List Query**: Ask which equipment are included in f(X). I will return a list of equipment (list order is random and carries no additional information).
2. **Membership Query**: Ask whether equipment Y belongs to f(X). I will answer "Yes" or "No".
3. **Count Query**: Ask how many equipment are in f(X). I will answer with an integer.

**Important Constraints**:
- Before submitting your final answer, you must have queried at least two different equipment X (query types can be same or different)
- Each turn you can only ask one question

Each query must use the following XML format (only one tag allowed):

- List Query (e.g., query the synchronous downtime result of R2):
<query_list>R2</query_list>

- Membership Query (e.g., ask if B1 is in the downtime result of R2):
<query_member>R2,B1</query_member>

- Count Query (e.g., query how many equipment are affected by the downtime of G1):
<query_count>G1</query_count>

When submitting the final answer, you must include the following three parts:
1. The identified associated rule (A, B, C, or D)
2. The cascade result of B2 under Rule A, output in assembly line order (comma-separated)
3. At least two query evidences (format: equipment=result)

Answer format:
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

If the answer is wrong, format is invalid, or evidence is insufficient, the simulation fails.
"""

    contextualized_rule_zh_5 = """\
欢迎使用"律师事务所利益冲突审查与案件回避系统"。我们来进行一次"合规防火墙映射"审核测试，规则如下：

系统记录了需要受控的本所律师集合 U = {R1, R2, R3, B1, B2, B3, G1, G2}。
该集合被划分为三个核心业务团队：
- R 组：刑事诉讼团队律师 R1, R2, R3（资历顺序：R1 < R2 < R3）
- B 组：商业并购团队律师 B1, B2, B3（资历顺序：B1 < B2 < B3）
- G 组：知识产权团队律师 G1, G2（资历顺序：G1 < G2）

在同一团队内，按照上述资历深浅顺序，每位律师与其紧邻资历的律师为"相邻资历律师"。例如 R2 的相邻资历律师是 R1 和 R3。

系统已秘密执行了一种**案件回避规则**，该规则定义了一个函数 f，对于任意接手敏感案件的律师 x，会返回该团队必须设立信息防火墙以进行强制回避的律师集合 f(x)。有四种可能的规则（A、B、C、D）：

- 规则 A：f(x) = x 所在团队的所有其他律师（不包括 x 自身）
- 规则 B：f(x) = x 所在团队的所有律师（包括 x 自身的业务静默）
- 规则 C：f(x) = x 在其团队内的所有相邻资历律师（不包括 x 自身）
- 规则 D：f(x) = x 所在团队中，除了 x 自身和相邻资历律师之外的所有律师

整个测试中，系统使用的回避规则是固定的，对所有查询保持一致。

你的目标是：
1. 识别出当前系统使用的是哪一种回避规则（A、B、C 或 D）
2. 在标准规则 A 的定义下，计算出 B2 的回避结果（即商业并购团队中除 B2 外的所有律师），并按资历顺序从小到大输出
3. 提供至少两条查询证据，证明你的推理过程

你可以反复向我提出以下三类查询（每次仅限一个查询）：

1. **名单查询**：询问 f(X) 包含哪些律师。我会返回一个律师列表（列表顺序随机，不传递额外信息）。
2. **成员判定**：询问某律师 Y 是否属于 f(X)。我会回答"是"或"否"。
3. **数量查询**：询问 f(X) 中有多少名律师。我会回答一个整数。

**重要约束**：
- 在提交最终答案前，你必须对至少两名不同的律师 X 进行过查询（查询类型可以相同或不同）
- 每次只能提出一个问题

每次询问必须使用以下 XML 格式（只能包含一个标签）：

- 名单查询（例如查询接手案件后针对 R2 的回避结果）：
<query_list>R2</query_list>

- 成员判定（例如询问 B1 是否在 R2 的回避名单中）：
<query_member>R2,B1</query_member>

- 数量查询（例如查询针对 G1 的回避包含多少名律师）：
<query_count>G1</query_count>

提交最终答案时，必须包含以下三部分信息：
1. 识别出的回避规则（A、B、C 或 D）
2. 在规则 A 下 B2 的回避结果，按资历顺序输出（用逗号分隔）
3. 至少两条查询证据（格式：律师=结果）

答案格式如下：
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

若答案错误、格式不符或证据不足，合规审核测试失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Law Firm Conflict of Interest Review and Recusal System". Let's conduct a "Compliance Firewall Mapping" audit test. Here are the rules:

The system records a controlled set of firm lawyers U = {R1, R2, R3, B1, B2, B3, G1, G2}.
This set is divided into three core practice teams:
- Group R: Criminal Litigation team lawyers R1, R2, R3 (seniority order: R1 < R2 < R3)
- Group B: M&A team lawyers B1, B2, B3 (seniority order: B1 < B2 < B3)
- Group G: Intellectual Property team lawyers G1, G2 (seniority order: G1 < G2)

Within the same team, according to the seniority order above, each lawyer's adjacent lawyers are those directly preceding or succeeding them in seniority. For example, R2's adjacent seniority lawyers are R1 and R3.

The system has secretly enforced a **recusal rule** that defines a function f. For any lawyer x taking on a sensitive case, it returns a set of lawyers f(x) that must establish an information firewall and undergo mandatory recusal. There are four possible rules (A, B, C, D):

- Rule A: f(x) = all other lawyers in x's team (excluding x itself)
- Rule B: f(x) = all lawyers in x's team (including a business silence for x itself)
- Rule C: f(x) = all adjacent seniority lawyers of x within its team (excluding x itself)
- Rule D: f(x) = all lawyers in x's team, excluding x itself and adjacent seniority lawyers

Throughout the test, the recusal rule used by the system is fixed and consistent for all queries.

Your goals are:
1. Identify which recusal rule the system is using (A, B, C, or D)
2. Under the standard Rule A definition, calculate the recusal result for B2 (i.e., all lawyers in the M&A team except B2), and output them in ascending seniority order
3. Provide at least two query evidences to prove your reasoning

You can repeatedly ask me the following three types of queries (one per turn):

1. **List Query**: Ask which lawyers are included in f(X). I will return a list of lawyers (list order is random and carries no additional information).
2. **Membership Query**: Ask whether lawyer Y belongs to f(X). I will answer "Yes" or "No".
3. **Count Query**: Ask how many lawyers are in f(X). I will answer with an integer.

**Important Constraints**:
- Before submitting your final answer, you must have queried at least two different lawyers X (query types can be same or different)
- Each turn you can only ask one question

Each query must use the following XML format (only one tag allowed):

- List Query (e.g., query the recusal result for R2):
<query_list>R2</query_list>

- Membership Query (e.g., ask if B1 is in the recusal list for R2):
<query_member>R2,B1</query_member>

- Count Query (e.g., query how many lawyers are affected by the recusal of G1):
<query_count>G1</query_count>

When submitting the final answer, you must include the following three parts:
1. The identified recusal rule (A, B, C, or D)
2. The recusal result of B2 under Rule A, output in seniority order (comma-separated)
3. At least two query evidences (format: lawyer=result)

Answer format:
<answer>rule=A, target=B1,B3, evidence=R1=[R2,R3];G1=[G2]</answer>

If the answer is wrong, format is invalid, or evidence is insufficient, the compliance audit test fails.
"""

    tags = ["answer", "query_list", "query_member", "query_count"]
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"rule": "A"},
            2: {"rule": "B"},
            3: {"rule": "C"},
            4: {"rule": "D"},
            5: {"rule": "D"},
        },
        "en": {
            1: {"rule": "A"},
            2: {"rule": "B"},
            3: {"rule": "C"},
            4: {"rule": "D"},
            5: {"rule": "D"},
        },
    }

    def __init__(self, config):
        self.groups = {
            "R": ["R1", "R2", "R3"],
            "B": ["B1", "B2", "B3"],
            "G": ["G1", "G2"],
        }
        
        self.element_to_group = {}
        for group_name, elements in self.groups.items():
            for elem in elements:
                self.element_to_group[elem] = group_name
        
        self.queried_elements = set()
        self._standard_mode = True
        
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.mapping_rule = cfg["rule"]
        self._game_info["rule"] = self.mapping_rule

    def _get_adjacent_elements(self, elem):
        group_name = self.element_to_group.get(elem)
        if not group_name:
            return []
        
        group = self.groups[group_name]
        idx = group.index(elem)
        adjacent = []
        
        if idx > 0:
            adjacent.append(group[idx - 1])
        if idx < len(group) - 1:
            adjacent.append(group[idx + 1])
        
        return adjacent

    def _apply_mapping(self, elem):
        group_name = self.element_to_group.get(elem)
        if not group_name:
            return []
        
        group = self.groups[group_name]
        
        if self.mapping_rule == "A":
            return [e for e in group if e != elem]
        
        elif self.mapping_rule == "B":
            return group[:]
        
        elif self.mapping_rule == "C":
            return self._get_adjacent_elements(elem)
        
        elif self.mapping_rule == "D":
            adjacent = self._get_adjacent_elements(elem)
            return [e for e in group if e != elem and e not in adjacent]
        
        return []

    def evaluate(self, parsed_info):
        
        raw_ans = parsed_info["answer"]
        
        try:
            rule_match = re.search(r'rule\s*=\s*([A-D])', raw_ans, re.IGNORECASE)
            target_match = re.search(r'target\s*=\s*([\w,]+)', raw_ans, re.IGNORECASE)
            evidence_match = re.search(r'evidence\s*=\s*(.+)', raw_ans, re.IGNORECASE)
            
            if not (rule_match and target_match and evidence_match):
                return False
            
            identified_rule = rule_match.group(1).upper()
            if identified_rule != self.mapping_rule:
                return False
            
            target_str = target_match.group(1).strip()
            target_elements = [e.strip() for e in target_str.split(",") if e.strip()]
            
            correct_target = ["B1", "B3"]
            if target_elements != correct_target:
                return False
            
            evidence_str = evidence_match.group(1).strip()
            evidence_parts = [e.strip() for e in evidence_str.split(";") if e.strip()]
            
            if len(evidence_parts) < 2:
                return False
            
            for evidence in evidence_parts:
                if "=" not in evidence:
                    return False
                
                elem_part, result_part = evidence.split("=", 1)
                elem = elem_part.strip()
                
                if elem not in self.element_to_group:
                    return False
                
                if self._standard_mode and elem not in self.queried_elements:
                    return False
                
                result_match_re = re.search(r'\[(.*?)\]', result_part)
                if not result_match_re:
                    return False
                
                result_content = result_match_re.group(1).strip()
                if result_content:
                    result_elements = set(e.strip() for e in result_content.split(",") if e.strip())
                else:
                    result_elements = set()
                
                actual_result = set(self._apply_mapping(elem))
                if result_elements != actual_result:
                    return False
            
            if self._standard_mode and len(self.queried_elements) < 2:
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_invalid = "错误：元素不存在或格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_invalid = "Error: Element does not exist or format is invalid."

        if "query_list" in parsed_info:
            elem = parsed_info["query_list"].strip()
            
            if elem not in self.element_to_group:
                return error_invalid
            
            self.queried_elements.add(elem)
            
            result = self._apply_mapping(elem)
            
            sorted_result = sorted(result)
            
            return "[" + ", ".join(sorted_result) + "]"

        elif "query_member" in parsed_info:
            try:
                raw = parsed_info["query_member"]
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 2:
                    return error_invalid
                
                elem, target = parts
                
                if elem not in self.element_to_group or target not in self.element_to_group:
                    return error_invalid
                
                self.queried_elements.add(elem)
                
                result = self._apply_mapping(elem)
                return yes_res if target in result else no_res
                
            except Exception:
                return error_invalid

        elif "query_count" in parsed_info:
            elem = parsed_info["query_count"].strip()
            
            if elem not in self.element_to_group:
                return error_invalid
            
            self.queried_elements.add(elem)
            
            result = self._apply_mapping(elem)
            return str(len(result))

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lowered = correct.lower()
        if lowered == "yes":
            return "No" if correct[0].isupper() else "no"
        if lowered == "no":
            return "Yes" if correct[0].isupper() else "yes"
        
        list_match = re.match(r'\[(.*)\]', correct)
        if list_match:
            content = list_match.group(1).strip()
            if content:
                elements = [e.strip() for e in content.split(",") if e.strip()]
            else:
                elements = []
            
            all_elements = []
            for group in self.groups.values():
                all_elements.extend(group)
            
            elements_set = set(elements)
            not_in_result = [e for e in all_elements if e not in elements_set]
            
            if not_in_result:
                wrong_elements = elements + [not_in_result[0]]
                wrong_elements.sort()
            elif elements:
                wrong_elements = elements[1:]
            else:
                wrong_elements = [all_elements[0]]
            
            return "[" + ", ".join(wrong_elements) + "]"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        possible_queries = []
        
        all_elements = []
        for group in self.groups.values():
            all_elements.extend(group)
        all_elements.sort()
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"

        for elem in all_elements:
            result_list = self._apply_mapping(elem)
            sorted_result = sorted(result_list)
            list_answer = "[" + ", ".join(sorted_result) + "]"
            
            possible_queries.append({
                "query": f"<query_list>{elem}</query_list>",
                "answer": list_answer
            })
            
            count_answer = str(len(result_list))
            possible_queries.append({
                "query": f"<query_count>{elem}</query_count>",
                "answer": count_answer
            })
            
            group_name = self.element_to_group[elem]
            group_elements = self.groups[group_name]
            result_set = set(result_list)
            for target in group_elements:
                is_member = target in result_set
                member_answer = yes_res if is_member else no_res
                
                possible_queries.append({
                    "query": f"<query_member>{elem},{target}</query_member>",
                    "answer": member_answer
                })

        return possible_queries