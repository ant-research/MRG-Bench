from .base import Game
import re
import itertools

class HiddenOrderGame(Game):

    reasoning_type = "演绎推理"
    data_structure = "序列"

    game_rule_zh = """\
我们来玩一个"隐藏次序推理"游戏，规则如下：

游戏设定了一个包含 {n} 个不同元素的集合 S = {{{elements}}}。这些元素按照某种严格的线性次序排列（即存在一个隐藏的排列顺序），任意两个不同的元素之间都有确定的先后关系。

你的目标是推断出以下 {num_targets} 组目标对中每一对元素的相对顺序：
{target_pairs}

你可以通过提问来收集信息，但请注意：

1. **前后比较查询**：询问两个非目标对元素 x 和 y 的相对顺序。
   - 注意：不能查询目标对中的元素组合，否则该查询无效且不会得到答案。
   - 回答形式："x 在 y 之前" 或 "y 在 x 之前"。

2. **相邻检验查询**：询问两个元素 x 和 y 是否在隐藏次序中紧邻（中间没有其他元素）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你谁在前谁在后。

3. **介于检验查询**：询问元素 r 是否严格位于元素 x 和 y 之间（无论 x、y 谁前谁后）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你 x、y 或 r 的具体顺序。

每轮只能提出一个查询。请尽可能少地使用查询次数，收集足够信息后提交最终答案。

每次查询必须使用以下 XML 格式之一：

- 前后比较查询（例如询问元素 A 和 B）：
<query_compare>A,B</query_compare>

- 相邻检验查询（例如询问元素 C 和 D 是否相邻）：
<query_adjacent>C,D</query_adjacent>

- 介于检验查询（例如询问元素 E 是否在 F 和 G 之间）：
<query_between>E,F,G</query_between>

提交最终答案时，必须对每个目标对明确说明顺序关系，格式如下：

<answer>A before B; C before D</answer>

注意：
- 每对元素用"before"连接（表示前者在后者之前）
- 多个目标对之间用分号和空格分隔
- 必须覆盖所有 {num_targets} 个目标对
"""

    game_rule_en = """\
Let's play a "Hidden Order Deduction" game. Here are the rules:

The game has a set S of {n} distinct elements: {{{elements}}}. These elements are arranged in a strict linear order (i.e., a hidden permutation), where any two different elements have a definite ordering relationship.

Your goal is to determine the relative order of each pair in the following {num_targets} target pairs:
{target_pairs}

You can gather information through queries, but please note:

1. **Compare Query**: Ask about the relative order of two elements x and y that do NOT form a target pair.
   - Warning: You cannot query target pair combinations; such queries are invalid and will not be answered.
   - Response format: "x before y" or "y before x".

2. **Adjacent Query**: Ask whether two elements x and y are adjacent in the hidden order (no elements between them).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you who comes first.

3. **Between Query**: Ask whether element r is strictly between elements x and y (regardless of which of x or y comes first).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you the specific order of x, y, or r.

You can only ask one query per turn. Use as few queries as possible, and submit your final answer when you have enough information.

Each query must use one of the following XML formats:

- Compare Query (e.g., asking about elements A and B):
<query_compare>A,B</query_compare>

- Adjacent Query (e.g., asking if elements C and D are adjacent):
<query_adjacent>C,D</query_adjacent>

- Between Query (e.g., asking if element E is between F and G):
<query_between>E,F,G</query_between>

When submitting the final answer, you must specify the order for each target pair in this format:

<answer>A before B; C before D</answer>

Note:
- Use "before" to connect each pair (indicating the first comes before the second)
- Separate multiple target pairs with semicolons and spaces
- Must cover all {num_targets} target pairs
"""

    contextualized_rule_zh_1 = """\
【交通场景：列车调度系统】
我们来玩一个"隐藏次序推理"演练，规则如下：

演练设定了一个包含 {n} 个不同列车班次的集合 S = {{{elements}}}。这些班次按照某种严格的发车次序排列（即存在一个隐藏的排列顺序），任意两个不同的班次之间都有确定的先后发车关系。

你的目标是推断出以下 {num_targets} 组目标班次对中每一对的相对发车顺序：
{target_pairs}

你可以通过提问调度系统来收集信息，但请注意：

1. **前后比较查询**：询问两个非目标对班次 x 和 y 的发车先后顺序。
   - 注意：不能查询目标对中的班次组合，否则该查询无效且不会得到答案。
   - 回答形式："x 在 y 之前" 或 "y 在 x 之前"。

2. **相邻检验查询**：询问两个班次 x 和 y 是否在发车次序中紧邻（中间没有安排其他班次发车）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你哪个班次先发车。

3. **介于检验查询**：询问班次 r 是否严格位于班次 x 和 y 的发车时间之间（无论 x、y 谁先发车）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你 x、y 或 r 的具体发车顺序。

每轮只能提出一个查询。请尽可能少地使用查询次数，收集足够信息后提交最终的调度序列答案。

每次查询必须使用以下 XML 格式之一：

- 前后比较查询（例如询问班次 A 和 B）：
<query_compare>A,B</query_compare>

- 相邻检验查询（例如询问班次 C 和 D 是否紧邻）：
<query_adjacent>C,D</query_adjacent>

- 介于检验查询（例如询问班次 E 是否在 F 和 G 之间）：
<query_between>E,F,G</query_between>

提交最终答案时，必须对每个目标对明确说明顺序关系，格式如下：

<answer>A before B; C before D</answer>

注意：
- 每对元素用"before"连接（表示前者在后者之前）
- 多个目标对之间用分号和空格分隔
- 必须覆盖所有 {num_targets} 个目标对
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario: Train Dispatch System]
Let's play a "Hidden Order Deduction" exercise. Here are the rules:

The system has a set S of {n} distinct train services: {{{elements}}}. These services are arranged in a strict linear departure order (i.e., a hidden permutation), where any two different services have a definite ordering relationship regarding their departure times.

Your goal is to determine the relative departure order of each pair in the following {num_targets} target service pairs:
{target_pairs}

You can gather information through queries to the dispatch system, but please note:

1. **Compare Query**: Ask about the relative departure order of two services x and y that do NOT form a target pair.
   - Warning: You cannot query target pair combinations; such queries are invalid and will not be answered.
   - Response format: "x before y" or "y before x".

2. **Adjacent Query**: Ask whether two services x and y are strictly consecutive in the departure schedule (no other services depart between them).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you which service departs first.

3. **Between Query**: Ask whether service r departs strictly between services x and y (regardless of which of x or y departs first).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you the specific order of x, y, or r.

You can only ask one query per turn. Use as few queries as possible, and submit your final dispatch schedule answer when you have enough information.

Each query must use one of the following XML formats:

- Compare Query (e.g., asking about services A and B):
<query_compare>A,B</query_compare>

- Adjacent Query (e.g., asking if services C and D are consecutive):
<query_adjacent>C,D</query_adjacent>

- Between Query (e.g., asking if service E is between F and G):
<query_between>E,F,G</query_between>

When submitting the final answer, you must specify the order for each target pair in this format:

<answer>A before B; C before D</answer>

Note:
- Use "before" to connect each pair (indicating the first comes before the second)
- Separate multiple target pairs with semicolons and spaces
- Must cover all {num_targets} target pairs
"""

    contextualized_rule_zh_2 = """\
【医疗场景：手术排台顺序】
我们来进行"手术排台次序推理"演练，规则如下：

排台系统设定了一个包含 {n} 名待手术患者的集合 S = {{{elements}}}。这些患者按照某种严格的手术先后次序排列（即存在一个隐藏的排台顺序），任意两名不同患者的手术都有确定的先后关系。

你的目标是推断出以下 {num_targets} 组目标患者对中每一对的手术先后顺序：
{target_pairs}

你可以通过查询排台系统来收集信息，但请注意：

1. **前后比较查询**：询问两名非目标对患者 x 和 y 的手术先后顺序。
   - 注意：不能查询目标对中的患者组合，否则该查询无效且不会得到答案。
   - 回答形式："x 在 y 之前" 或 "y 在 x 之前"。

2. **相邻检验查询**：询问两名患者 x 和 y 是否在排台次序中紧邻（中间没有安排其他患者手术）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你哪名患者先进行手术。

3. **介于检验查询**：询问患者 r 是否严格位于患者 x 和 y 的手术安排之间（无论 x、y 谁先手术）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你 x、y 或 r 的具体手术顺序。

每轮只能提出一个查询。请尽可能少地使用查询次数，收集足够信息后提交最终排期确认答案。

每次查询必须使用以下 XML 格式之一：

- 前后比较查询（例如询问患者 A 和 B）：
<query_compare>A,B</query_compare>

- 相邻检验查询（例如询问患者 C 和 D 是否紧邻）：
<query_adjacent>C,D</query_adjacent>

- 介于检验查询（例如询问患者 E 是否在 F 和 G 之间）：
<query_between>E,F,G</query_between>

提交最终答案时，必须对每个目标对明确说明顺序关系，格式如下：

<answer>A before B; C before D</answer>

注意：
- 每对元素用"before"连接（表示前者在后者之前）
- 多个目标对之间用分号和空格分隔
- 必须覆盖所有 {num_targets} 个目标对
"""

    contextualized_rule_en_2 = """\
[Medical Scenario: Surgical Scheduling]
Let's conduct a "Surgical Schedule Deduction" exercise. Here are the rules:

The scheduling system has a set S of {n} distinct patients pending surgery: {{{elements}}}. These patients are arranged in a strict linear surgical order (i.e., a hidden schedule), where any two different patients have a definite chronological relationship.

Your goal is to determine the relative surgical order of each pair in the following {num_targets} target patient pairs:
{target_pairs}

You can gather information through queries to the scheduling system, but please note:

1. **Compare Query**: Ask about the relative surgical order of two patients x and y that do NOT form a target pair.
   - Warning: You cannot query target pair combinations; such queries are invalid and will not be answered.
   - Response format: "x before y" or "y before x".

2. **Adjacent Query**: Ask whether two patients x and y are scheduled consecutively (no other operations scheduled between them).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you who undergoes surgery first.

3. **Between Query**: Ask whether patient r is scheduled strictly between patients x and y (regardless of which of x or y is first).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you the specific order of x, y, or r.

You can only ask one query per turn. Use as few queries as possible, and submit your final schedule confirmation when you have enough information.

Each query must use one of the following XML formats:

- Compare Query (e.g., asking about patients A and B):
<query_compare>A,B</query_compare>

- Adjacent Query (e.g., asking if patients C and D are scheduled consecutively):
<query_adjacent>C,D</query_adjacent>

- Between Query (e.g., asking if patient E is between F and G):
<query_between>E,F,G</query_between>

When submitting the final answer, you must specify the order for each target pair in this format:

<answer>A before B; C before D</answer>

Note:
- Use "before" to connect each pair (indicating the first comes before the second)
- Separate multiple target pairs with semicolons and spaces
- Must cover all {num_targets} target pairs
"""

    contextualized_rule_zh_3 = """\
【教育场景：教学大纲编排】
我们来进行"教学大纲知识点次序推理"任务，规则如下：

大纲设定了一个包含 {n} 个核心知识点的集合 S = {{{elements}}}。这些知识点按照某种严格的授课次序排列（即存在一个隐藏的教学逻辑顺序），任意两个不同知识点都有确定的先后授课关系。

你的目标是推断出以下 {num_targets} 组目标知识点对中每一对的先后授课顺序：
{target_pairs}

你可以通过提问教务系统来收集信息，但请注意：

1. **前后比较查询**：询问两个非目标对知识点 x 和 y 的授课先后顺序。
   - 注意：不能查询目标对中的知识点组合，否则该查询无效且不会得到答案。
   - 回答形式："x 在 y 之前" 或 "y 在 x 之前"。

2. **相邻检验查询**：询问两个知识点 x 和 y 是否在授课次序中紧邻（中间没有插入其他知识点教学）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你哪个知识点先讲授。

3. **介于检验查询**：询问知识点 r 是否严格安排在知识点 x 和 y 的授课阶段之间（无论 x、y 谁先讲）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你 x、y 或 r 的具体授课顺序。

每轮只能提出一个查询。请尽可能少地使用查询次数，收集足够信息后提交最终编排确认答案。

每次查询必须使用以下 XML 格式之一：

- 前后比较查询（例如询问知识点 A 和 B）：
<query_compare>A,B</query_compare>

- 相邻检验查询（例如询问知识点 C 和 D 是否紧邻授课）：
<query_adjacent>C,D</query_adjacent>

- 介于检验查询（例如询问知识点 E 是否在 F 和 G 之间）：
<query_between>E,F,G</query_between>

提交最终答案时，必须对每个目标对明确说明顺序关系，格式如下：

<answer>A before B; C before D</answer>

注意：
- 每对元素用"before"连接（表示前者在后者之前）
- 多个目标对之间用分号和空格分隔
- 必须覆盖所有 {num_targets} 个目标对
"""

    contextualized_rule_en_3 = """\
[Education Scenario: Syllabus Sequencing]
Let's perform a "Syllabus Topic Sequence Deduction" task. Here are the rules:

The syllabus defines a set S of {n} core learning topics: {{{elements}}}. These topics are arranged in a strict linear instructional order (i.e., a hidden pedagogical sequence), where any two different topics have a definite preceding/succeeding relationship.

Your goal is to determine the relative instructional order of each pair in the following {num_targets} target topic pairs:
{target_pairs}

You can gather information through queries to the curriculum system, but please note:

1. **Compare Query**: Ask about the relative teaching order of two topics x and y that do NOT form a target pair.
   - Warning: You cannot query target pair combinations; such queries are invalid and will not be answered.
   - Response format: "x before y" or "y before x".

2. **Adjacent Query**: Ask whether two topics x and y are taught consecutively (no other topics are taught between them).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you which topic is taught first.

3. **Between Query**: Ask whether topic r is taught strictly between topics x and y (regardless of which of x or y is taught first).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you the specific teaching order of x, y, or r.

You can only ask one query per turn. Use as few queries as possible, and submit your final syllabus sequence confirmation when you have enough information.

Each query must use one of the following XML formats:

- Compare Query (e.g., asking about topics A and B):
<query_compare>A,B</query_compare>

- Adjacent Query (e.g., asking if topics C and D are taught consecutively):
<query_adjacent>C,D</query_adjacent>

- Between Query (e.g., asking if topic E is between F and G):
<query_between>E,F,G</query_between>

When submitting the final answer, you must specify the order for each target pair in this format:

<answer>A before B; C before D</answer>

Note:
- Use "before" to connect each pair (indicating the first comes before the second)
- Separate multiple target pairs with semicolons and spaces
- Must cover all {num_targets} target pairs
"""

    contextualized_rule_zh_4 = """\
【制造业场景：装配流水线工序】
我们来进行"装配流水线工序次序推理"测试，规则如下：

产线设定了一个包含 {n} 道不同加工工序的集合 S = {{{elements}}}。这些工序按照某种严格的流水线执行次序排列（即存在一个隐藏的工艺路线），任意两道不同工序之间都有确定的先后执行关系。

你的目标是推断出以下 {num_targets} 组目标工序对中每一对的相对执行顺序：
{target_pairs}

你可以通过查询制造执行系统（MES）来收集信息，但请注意：

1. **前后比较查询**：询问两道非目标对工序 x 和 y 的执行先后顺序。
   - 注意：不能查询目标对中的工序组合，否则该查询无效且系统拒绝回答。
   - 回答形式："x 在 y 之前" 或 "y 在 x 之前"。

2. **相邻检验查询**：询问两道工序 x 和 y 是否在流水线上紧邻执行（中间无其他工序）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你哪道工序先执行。

3. **介于检验查询**：询问工序 r 是否严格位于工序 x 和 y 的工艺环节之间（无论 x、y 谁先执行）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你 x、y 或 r 的具体流转顺序。

每轮只能提出一个查询。请尽可能少地使用查询次数，收集足够信息后提交最终的工艺确认答案。

每次查询必须使用以下 XML 格式之一：

- 前后比较查询（例如询问工序 A 和 B）：
<query_compare>A,B</query_compare>

- 相邻检验查询（例如询问工序 C 和 D 是否紧邻）：
<query_adjacent>C,D</query_adjacent>

- 介于检验查询（例如询问工序 E 是否在 F 和 G 之间）：
<query_between>E,F,G</query_between>

提交最终答案时，必须对每个目标对明确说明顺序关系，格式如下：

<answer>A before B; C before D</answer>

注意：
- 每对元素用"before"连接（表示前者在后者之前）
- 多个目标对之间用分号和空格分隔
- 必须覆盖所有 {num_targets} 个目标对
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario: Assembly Line Procedures]
Let's conduct an "Assembly Line Procedure Deduction" test. Here are the rules:

The production line involves a set S of {n} distinct processing steps: {{{elements}}}. These steps are arranged in a strict linear execution order (i.e., a hidden routing sequence), where any two different steps have a definite temporal execution relationship.

Your goal is to determine the relative execution order of each pair in the following {num_targets} target step pairs:
{target_pairs}

You can gather information through queries to the Manufacturing Execution System (MES), but please note:

1. **Compare Query**: Ask about the relative execution order of two steps x and y that do NOT form a target pair.
   - Warning: You cannot query target pair combinations; such queries are invalid and will be rejected.
   - Response format: "x before y" or "y before x".

2. **Adjacent Query**: Ask whether two steps x and y are strictly consecutive on the assembly line (no intermediate steps).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you which step is executed first.

3. **Between Query**: Ask whether step r is strictly located between steps x and y in the routing sequence (regardless of which of x or y comes first).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you the specific routing order of x, y, or r.

You can only ask one query per turn. Use as few queries as possible, and submit your final routing confirmation when you have enough information.

Each query must use one of the following XML formats:

- Compare Query (e.g., asking about steps A and B):
<query_compare>A,B</query_compare>

- Adjacent Query (e.g., asking if steps C and D are consecutive):
<query_adjacent>C,D</query_adjacent>

- Between Query (e.g., asking if step E is between F and G):
<query_between>E,F,G</query_between>

When submitting the final answer, you must specify the order for each target pair in this format:

<answer>A before B; C before D</answer>

Note:
- Use "before" to connect each pair (indicating the first comes before the second)
- Separate multiple target pairs with semicolons and spaces
- Must cover all {num_targets} target pairs
"""

    contextualized_rule_zh_5 = """\
【法律场景：庭审证据出示】
我们来进行"庭审证据出示次序推理"审查，规则如下：

法庭审查设定了一个包含 {n} 份不同关键证据的集合 S = {{{elements}}}。这些证据在庭审中按照某种严格的呈现次序排列（即存在一个隐藏的举证顺位），任意两份不同证据之间都有确定的先后出示关系。

你的目标是推断出以下 {num_targets} 组目标证据对中每一对的先后出示顺序：
{target_pairs}

你可以向书记员系统提出查询来收集信息，但请注意：

1. **前后比较查询**：询问两份非目标对证据 x 和 y 的出示先后顺序。
   - 注意：不能查询目标对中的证据组合，否则该查询无效且不会得到回答。
   - 回答形式："x 在 y 之前" 或 "y 在 x 之前"。

2. **相邻检验查询**：询问两份证据 x 和 y 是否在举证环节中紧邻出示（中间没有穿插其他证据）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你哪份证据先出示。

3. **介于检验查询**：询问证据 r 是否严格安排在证据 x 和 y 的出示环节之间（无论 x、y 谁先出示）。
   - 回答形式："是" 或 "否"。
   - 注意：此查询不会告诉你 x、y 或 r 的具体举证顺序。

每轮只能提出一个查询。请尽可能少地使用查询次数，收集足够信息后提交最终的证据链顺位答案。

每次查询必须使用以下 XML 格式之一：

- 前后比较查询（例如询问证据 A 和 B）：
<query_compare>A,B</query_compare>

- 相邻检验查询（例如询问证据 C 和 D 是否紧邻出示）：
<query_adjacent>C,D</query_adjacent>

- 介于检验查询（例如询问证据 E 是否在 F 和 G 之间）：
<query_between>E,F,G</query_between>

提交最终答案时，必须对每个目标对明确说明顺序关系，格式如下：

<answer>A before B; C before D</answer>

注意：
- 每对元素用"before"连接（表示前者在后者之前）
- 多个目标对之间用分号和空格分隔
- 必须覆盖所有 {num_targets} 个目标对
"""

    contextualized_rule_en_5 = """\
[Legal Scenario: Trial Evidence Presentation]
Let's conduct a "Trial Evidence Sequence Deduction" review. Here are the rules:

The court review defines a set S of {n} distinct key pieces of evidence: {{{elements}}}. This evidence is presented during the trial in a strict linear order (i.e., a hidden presentation sequence), where any two different pieces of evidence have a definite sequential relationship.

Your goal is to determine the relative presentation order of each pair in the following {num_targets} target evidence pairs:
{target_pairs}

You can gather information through queries to the clerk system, but please note:

1. **Compare Query**: Ask about the relative presentation order of two pieces of evidence x and y that do NOT form a target pair.
   - Warning: You cannot query target pair combinations; such queries are invalid and will not be answered.
   - Response format: "x before y" or "y before x".

2. **Adjacent Query**: Ask whether two pieces of evidence x and y are presented consecutively (no other evidence is introduced between them).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you which evidence is presented first.

3. **Between Query**: Ask whether evidence r is introduced strictly between evidence x and y (regardless of which of x or y is presented first).
   - Response format: "Yes" or "No".
   - Note: This query does not tell you the specific sequential order of x, y, or r.

You can only ask one query per turn. Use as few queries as possible, and submit your final evidence sequence answer when you have enough information.

Each query must use one of the following XML formats:

- Compare Query (e.g., asking about evidence A and B):
<query_compare>A,B</query_compare>

- Adjacent Query (e.g., asking if evidence C and D are presented consecutively):
<query_adjacent>C,D</query_adjacent>

- Between Query (e.g., asking if evidence E is between F and G):
<query_between>E,F,G</query_between>

When submitting the final answer, you must specify the order for each target pair in this format:

<answer>A before B; C before D</answer>

Note:
- Use "before" to connect each pair (indicating the first comes before the second)
- Separate multiple target pairs with semicolons and spaces
- Must cover all {num_targets} target pairs
"""

    tags = ["answer", "query_compare", "query_adjacent", "query_between"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "elements": ["A", "B", "C", "D", "E"],
                "order": ["A", "C", "E", "B", "D"],
                "targets": [("A", "D"), ("C", "B")],
            },
            2: {
                "elements": ["A", "B", "C", "D", "E", "F"],
                "order": ["B", "D", "A", "F", "C", "E"],
                "targets": [("A", "B"), ("C", "D"), ("E", "F")],
            },
            3: {
                "elements": ["A", "B", "C", "D", "E", "F", "G"],
                "order": ["C", "A", "E", "G", "B", "D", "F"],
                "targets": [("A", "B"), ("C", "D"), ("E", "F"), ("G", "D")],
            },
            4: {
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "order": ["D", "F", "A", "H", "C", "E", "B", "G"],
                "targets": [("A", "B"), ("C", "D"), ("E", "F"), ("G", "H"), ("A", "E")],
            },
            5: {
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "order": ["E", "B", "H", "D", "A", "I", "F", "C", "J", "G"],
                "targets": [("A", "B"), ("C", "D"), ("E", "F"), ("G", "H"), ("I", "J"), ("A", "C")],
            },
        },
        "en": {
            1: {
                "elements": ["A", "B", "C", "D", "E"],
                "order": ["A", "C", "E", "B", "D"],
                "targets": [("A", "D"), ("C", "B")],
            },
            2: {
                "elements": ["A", "B", "C", "D", "E", "F"],
                "order": ["B", "D", "A", "F", "C", "E"],
                "targets": [("A", "B"), ("C", "D"), ("E", "F")],
            },
            3: {
                "elements": ["A", "B", "C", "D", "E", "F", "G"],
                "order": ["C", "A", "E", "G", "B", "D", "F"],
                "targets": [("A", "B"), ("C", "D"), ("E", "F"), ("G", "D")],
            },
            4: {
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H"],
                "order": ["D", "F", "A", "H", "C", "E", "B", "G"],
                "targets": [("A", "B"), ("C", "D"), ("E", "F"), ("G", "H"), ("A", "E")],
            },
            5: {
                "elements": ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                "order": ["E", "B", "H", "D", "A", "I", "F", "C", "J", "G"],
                "targets": [("A", "B"), ("C", "D"), ("E", "F"), ("G", "H"), ("I", "J"), ("A", "C")],
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
        
        self.elements = cfg["elements"]
        self.hidden_order = cfg["order"]
        self.targets = cfg["targets"]
        
        self.pos_map = {elem: idx for idx, elem in enumerate(self.hidden_order)}
        
        self.target_set = {frozenset([x, y]) for x, y in self.targets}
        
        self.query_count = 0
        
        self._game_info = {
            "n": len(self.elements),
            "elements": ", ".join(self.elements),
            "num_targets": len(self.targets),
            "target_pairs": self._format_target_pairs(),
        }

    def _format_target_pairs(self):
        if self.config.language == "zh":
            return "\n".join([f"  - ({x}, {y})" for x, y in self.targets])
        else:
            return "\n".join([f"  - ({x}, {y})" for x, y in self.targets])

    def _is_target_pair(self, x, y):
        return frozenset([x, y]) in self.target_set

    def _compare(self, x, y):
        if x not in self.pos_map or y not in self.pos_map:
            return None
        pos_x = self.pos_map[x]
        pos_y = self.pos_map[y]
        if pos_x < pos_y:
            return (x, y)
        else:
            return (y, x)

    def _is_adjacent(self, x, y):
        if x not in self.pos_map or y not in self.pos_map:
            return None
        pos_x = self.pos_map[x]
        pos_y = self.pos_map[y]
        return abs(pos_x - pos_y) == 1

    def _is_between(self, r, x, y):
        if r not in self.pos_map or x not in self.pos_map or y not in self.pos_map:
            return None
        pos_r = self.pos_map[r]
        pos_x = self.pos_map[x]
        pos_y = self.pos_map[y]
        min_pos = min(pos_x, pos_y)
        max_pos = max(pos_x, pos_y)
        return min_pos < pos_r < max_pos

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"
        
        for x, y in itertools.combinations(self.elements, 2):
            if self._is_target_pair(x, y):
                continue
            
            first, second = self._compare(x, y)
            if lang == "zh":
                ans = f"{first} 在 {second} 之前"
            else:
                ans = f"{first} before {second}"
            
            queries.append({
                "query": f"<query_compare>{x},{y}</query_compare>",
                "answer": ans
            })
            
        for x, y in itertools.combinations(self.elements, 2):
            is_adj = self._is_adjacent(x, y)
            ans = yes_res if is_adj else no_res
            
            queries.append({
                "query": f"<query_adjacent>{x},{y}</query_adjacent>",
                "answer": ans
            })
            
        for r in self.elements:
            other_elements = [e for e in self.elements if e != r]
            for x, y in itertools.combinations(other_elements, 2):
                is_btwn = self._is_between(r, x, y)
                ans = yes_res if is_btwn else no_res
                
                queries.append({
                    "query": f"<query_between>{r},{x},{y}</query_between>",
                    "answer": ans
                })
                
        return queries

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        pairs_str = [s.strip() for s in raw_ans.split(";")]
        
        if len(pairs_str) != len(self.targets):
            return False
            
        covered_targets = set()
        
        for pair_str in pairs_str:
            parts = re.split(r'\s+before\s+', pair_str, flags=re.IGNORECASE)
            if len(parts) != 2:
                return False
            
            x, y = parts[0].strip(), parts[1].strip()
            
            pair_key = frozenset([x, y])
            if pair_key not in self.target_set:
                return False
                
            if pair_key in covered_targets:
                return False
            covered_targets.add(pair_key)
            
            first, second = self._compare(x, y)
            if first != x or second != y:
                return False
        
        return covered_targets == self.target_set

    def _cf_core_produce(self, parsed_info):
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"
        
        if "query_compare" in parsed_info:
            raw = parsed_info["query_compare"].strip()
            parts = [p.strip() for p in raw.split(",")]
            if len(parts) != 2:
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
            
            x, y = parts[0], parts[1]
            
            if x not in self.pos_map or y not in self.pos_map:
                return "错误：元素不在集合中。" if lang == "zh" else "Error: Element not in set."
            
            if x == y:
                return "错误：不能比较相同的元素。" if lang == "zh" else "Error: Cannot compare an element with itself."
            
            if self._is_target_pair(x, y):
                return "错误：不能查询目标对。" if lang == "zh" else "Error: Cannot query target pairs."
            
            self.query_count += 1
            
            first, second = self._compare(x, y)
            if lang == "zh":
                return f"{first} 在 {second} 之前"
            else:
                return f"{first} before {second}"
        
        elif "query_adjacent" in parsed_info:
            raw = parsed_info["query_adjacent"].strip()
            parts = [p.strip() for p in raw.split(",")]
            if len(parts) != 2:
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
            
            x, y = parts[0], parts[1]
            
            if x not in self.pos_map or y not in self.pos_map:
                return "错误：元素不在集合中。" if lang == "zh" else "Error: Element not in set."
            
            if x == y:
                return "错误：不能查询相同的元素。" if lang == "zh" else "Error: Cannot query an element with itself."
            
            self.query_count += 1
            
            return yes_res if self._is_adjacent(x, y) else no_res
        
        elif "query_between" in parsed_info:
            raw = parsed_info["query_between"].strip()
            parts = [p.strip() for p in raw.split(",")]
            if len(parts) != 3:
                return "错误：格式无效。" if lang == "zh" else "Error: Invalid format."
            
            r, x, y = parts[0], parts[1], parts[2]
            
            if r not in self.pos_map or x not in self.pos_map or y not in self.pos_map:
                return "错误：元素不在集合中。" if lang == "zh" else "Error: Element not in set."
            
            if len({r, x, y}) < 3:
                return "错误：三个元素必须互不相同。" if lang == "zh" else "Error: All three elements must be distinct."
            
            self.query_count += 1
            
            return yes_res if self._is_between(r, x, y) else no_res
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if correct == "是": return "否"
        if correct == "否": return "是"
        
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
            
        zh_match = re.match(r'^(\S+)\s+在\s+(\S+)\s+之前$', correct)
        if zh_match:
            return f"{zh_match.group(2)} 在 {zh_match.group(1)} 之前"
        
        en_match = re.match(r'^(\S+)\s+before\s+(\S+)$', correct, re.IGNORECASE)
        if en_match:
            return f"{en_match.group(2)} before {en_match.group(1)}"
            
        return correct + "_WRONG"

