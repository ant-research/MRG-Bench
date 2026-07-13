from .base import Game
import re
import itertools


class SetSymmetricDifferenceGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏集合推理"游戏，规则如下：

游戏设定了一个宇宙集合 U = {{A, B, C, D, E, F, G, H, I, J}}，包含 10 个元素。

我已经秘密选择了一个固定的子集 K（K 是 U 的子集，可能为空集）。在整个游戏过程中，K 保持不变。

同时，存在一个固定的映射函数 f，它接受你提交的任意非空子集 S 作为输入，返回另一个集合 f(S)。这个函数 f 的具体规则对你是未知的，但它在整个游戏中保持一致。

你的目标是：
1. 推断出函数 f 的运作机制（用自然语言描述）。
2. 准确识别出隐藏的子集 K 包含哪些元素。

## 交互方式

每一轮，你可以提交一个非空子集 S，并请求以下任一种反馈（每轮只能请求一种）：

1. **列表反馈**：我会返回集合 f(S) 的所有元素（无序）。
2. **计数反馈**：我会返回 f(S) 中元素的个数。
3. **单点判定**：你指定一个元素 x（x 必须在 U 中），我会告诉你 x 是否在 f(S) 中。

注意：
- 提交的集合 S 不能为空。
- 对于相同的 S，无论请求多少次，返回的结果都是一致的。
- 你需要至少完成 3 轮交互后才能提交最终答案。
- 请尽可能用更少的轮数完成推理。

## 询问与提交答案的格式（严格要求）

每次询问只能包含一个标签。请使用以下 XML 格式：

- **列表反馈**（例如查询集合 {{A, B, C}}）：
<query_list>A,B,C</query_list>

- **计数反馈**（例如查询集合 {{D, E}}）：
<query_count>D,E</query_count>

- **单点判定**（例如查询集合 {{A, B}} 并判断 C 是否在 f(S) 中）：
<query_member>A,B|C</query_member>

注意：单点判定格式为"集合元素|待判定元素"，用竖线分隔。

## 提交最终答案

当你完成至少 3 轮交互并收集足够信息后，请提交最终答案，格式如下：

<answer>mechanism=你对函数f的描述, K=集合K的元素（用逗号分隔，如果是空集则写empty）</answer>

例如：
<answer>mechanism=函数f返回输入集合与某个固定集合的对称差, K=A,C,E</answer>

或者（如果 K 是空集）：
<answer>mechanism=函数f返回输入集合本身, K=empty</answer>

如果答案错误或格式不符，游戏失败。
"""

    game_rule_en = """\
Let's play a "Hidden Set Deduction" game. Here are the rules:

The game defines a universe set U = {{A, B, C, D, E, F, G, H, I, J}}, containing 10 elements.

I have secretly selected a fixed subset K (K is a subset of U, possibly empty). Throughout the game, K remains constant.

There is also a fixed mapping function f that takes any non-empty subset S you submit as input and returns another set f(S). The specific rule of function f is unknown to you, but it remains consistent throughout the game.

Your goal is to:
1. Infer the operating mechanism of function f (described in natural language).
2. Accurately identify which elements are in the hidden subset K.

## Interaction Protocol

Each round, you can submit a non-empty subset S and request one of the following feedback types (only one per round):

1. **List Feedback**: I will return all elements of set f(S) (unordered).
2. **Count Feedback**: I will return the number of elements in f(S).
3. **Membership Test**: You specify an element x (x must be in U), and I will tell you whether x is in f(S).

Notes:
- The submitted set S cannot be empty.
- For the same S, no matter how many times you request, the returned result is consistent.
- You must complete at least 3 rounds of interaction before submitting your final answer.
- Try to complete the reasoning with as few rounds as possible.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- **List Feedback** (e.g., querying set {{A, B, C}}):
<query_list>A,B,C</query_list>

- **Count Feedback** (e.g., querying set {{D, E}}):
<query_count>D,E</query_count>

- **Membership Test** (e.g., querying set {{A, B}} and testing if C is in f(S)):
<query_member>A,B|C</query_member>

Note: The membership test format is "set elements|element to test", separated by a vertical bar.

## Submit Final Answer

After completing at least 3 rounds of interaction and gathering enough information, submit your final answer in the following format:

<answer>mechanism=your description of function f, K=elements of set K (comma-separated, write empty if K is empty set)</answer>

For example:
<answer>mechanism=function f returns the symmetric difference between the input set and a fixed set, K=A,C,E</answer>

Or (if K is empty set):
<answer>mechanism=function f returns the input set itself, K=empty</answer>

If the answer is incorrect or the format is invalid, the game fails.
"""

    contextualized_rule_zh_1 = """\
智慧交通指挥中心正在进行道路状态推演测试。
我们来玩一个"隐藏交通状态推理"游戏，规则如下：

游戏设定了一个交通枢纽集合 U = {{A, B, C, D, E, F, G, H, I, J}}，包含 10 个枢纽节点。

系统已经秘密选择了一个固定的拥堵/施工枢纽子集 K（K 是 U 的子集，可能为空集）。在整个推演过程中，K 保持不变。

同时，存在一个固定的状态推演函数 f，它接受你提交的任意非空重点监测枢纽子集 S 作为输入，返回另一个表现出异常交通流的枢纽集合 f(S)。这个函数 f 的具体推演规则对你是未知的，但它在整个推演中保持一致。

你的目标是：
1. 推断出状态推演函数 f 的运作机制（用自然语言描述）。
2. 准确识别出隐藏的拥堵/施工枢纽子集 K 包含哪些节点。

## 交互方式

每一轮推演，你可以提交一个非空枢纽子集 S，并请求以下任一种反馈（每轮只能请求一种）：

1. **列表反馈**：系统会返回集合 f(S) 的所有枢纽（无序）。
2. **计数反馈**：系统会返回 f(S) 中枢纽的个数。
3. **单点判定**：你指定一个枢纽 x（x 必须在 U 中），系统会告诉你 x 是否在 f(S) 中。

注意：
- 提交的监测集合 S 不能为空。
- 对于相同的 S，无论请求多少次，返回的推演结果都是一致的。
- 你需要至少完成 3 轮推演交互后才能提交最终答案。
- 请尽可能用更少的轮数完成推理。

## 询问与提交答案的格式（严格要求）

每次推演询问只能包含一个标签。请使用以下 XML 格式：

- **列表反馈**（例如查询枢纽集合 {{A, B, C}}）：
<query_list>A,B,C</query_list>

- **计数反馈**（例如查询枢纽集合 {{D, E}}）：
<query_count>D,E</query_count>

- **单点判定**（例如查询枢纽集合 {{A, B}} 并判断 C 是否在 f(S) 中）：
<query_member>A,B|C</query_member>

注意：单点判定格式为"集合元素|待判定元素"，用竖线分隔。

## 提交最终答案

当你完成至少 3 轮交互并收集足够信息后，请提交最终排查答案，格式如下：

<answer>mechanism=你对推演函数f的描述, K=集合K的枢纽节点（用逗号分隔，如果是空集则写empty）</answer>

例如：
<answer>mechanism=函数f返回输入监测集合与某个固定异常集合的对称差, K=A,C,E</answer>

或者（如果 K 是空集）：
<answer>mechanism=函数f返回输入监测集合本身, K=empty</answer>

如果排查答案错误或格式不符，推演失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Smart Traffic Command Center is conducting a road status simulation test.
Let's play a "Hidden Traffic Status Deduction" game. Here are the rules:

The game defines a traffic hub universe set U = {{A, B, C, D, E, F, G, H, I, J}}, containing 10 hub nodes.

The system has secretly selected a fixed subset of congested/under-construction hubs K (K is a subset of U, possibly empty). Throughout the simulation, K remains constant.

There is also a fixed status simulation function f that takes any non-empty monitored hub subset S you submit as input and returns another set of hubs showing abnormal traffic flow f(S). The specific rule of function f is unknown to you, but it remains consistent throughout the simulation.

Your goal is to:
1. Infer the operating mechanism of the simulation function f (described in natural language).
2. Accurately identify which nodes are in the hidden subset K.

## Interaction Protocol

Each simulation round, you can submit a non-empty hub subset S and request one of the following feedback types (only one per round):

1. **List Feedback**: The system will return all hubs in set f(S) (unordered).
2. **Count Feedback**: The system will return the number of hubs in f(S).
3. **Membership Test**: You specify a hub x (x must be in U), and the system will tell you whether x is in f(S).

Notes:
- The submitted monitoring set S cannot be empty.
- For the same S, no matter how many times you request, the returned simulation result is consistent.
- You must complete at least 3 rounds of interaction before submitting your final answer.
- Try to complete the reasoning with as few rounds as possible.

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- **List Feedback** (e.g., querying hub set {{A, B, C}}):
<query_list>A,B,C</query_list>

- **Count Feedback** (e.g., querying hub set {{D, E}}):
<query_count>D,E</query_count>

- **Membership Test** (e.g., querying hub set {{A, B}} and testing if C is in f(S)):
<query_member>A,B|C</query_member>

Note: The membership test format is "set elements|element to test", separated by a vertical bar.

## Submit Final Answer

After completing at least 3 rounds of interaction and gathering enough information, submit your final diagnostic answer in the following format:

<answer>mechanism=your description of function f, K=elements of set K (comma-separated, write empty if K is empty set)</answer>

For example:
<answer>mechanism=function f returns the symmetric difference between the monitored set and a fixed abnormal set, K=A,C,E</answer>

Or (if K is empty set):
<answer>mechanism=function f returns the monitored set itself, K=empty</answer>

If the diagnostic answer is incorrect or the format is invalid, the simulation fails.
"""

    contextualized_rule_zh_2 = """\
精准医疗实验室正在进行靶点药物反应机制的研究。
我们来玩一个"隐藏基因突变推理"游戏，规则如下：

游戏设定了一个靶点基因集合 U = {{A, B, C, D, E, F, G, H, I, J}}，包含 10 个候选靶点。

患者体内存在一个被秘密确定的基因突变子集 K（K 是 U 的子集，可能为空集）。在整个诊疗推理过程中，K 保持不变。

同时，存在一个固定的药物反应函数 f，它接受你提交的任意非空干预靶点子集 S 作为输入，返回最终表现出异常表达的靶点集合 f(S)。这个函数 f 的具体药理规则对你是未知的，但它在整个过程中保持一致。

你的目标是：
1. 推断出药物反应函数 f 的运作机制（用自然语言描述）。
2. 准确识别出隐藏的基因突变子集 K 包含哪些靶点。

## 交互方式

每一轮诊疗，你可以提交一个非空靶点子集 S，并请求以下任一种反馈（每轮只能请求一种）：

1. **列表反馈**：系统会返回集合 f(S) 的所有靶点（无序）。
2. **计数反馈**：系统会返回 f(S) 中靶点的个数。
3. **单点判定**：你指定一个靶点 x（x 必须在 U 中），系统会告诉你 x 是否在 f(S) 中。

注意：
- 提交的干预集合 S 不能为空。
- 对于相同的 S，无论请求多少次，返回的检测结果都是一致的。
- 你需要至少完成 3 轮诊疗交互后才能提交最终答案。
- 请尽可能用更少的轮数完成推理。

## 询问与提交答案的格式（严格要求）

每次检测询问只能包含一个标签。请使用以下 XML 格式：

- **列表反馈**（例如查询靶点集合 {{A, B, C}}）：
<query_list>A,B,C</query_list>

- **计数反馈**（例如查询靶点集合 {{D, E}}）：
<query_count>D,E</query_count>

- **单点判定**（例如查询靶点集合 {{A, B}} 并判断 C 是否在 f(S) 中）：
<query_member>A,B|C</query_member>

注意：单点判定格式为"集合元素|待判定元素"，用竖线分隔。

## 提交最终答案

当你完成至少 3 轮交互并收集足够信息后，请提交最终诊断答案，格式如下：

<answer>mechanism=你对反应函数f的描述, K=集合K的靶点（用逗号分隔，如果是空集则写empty）</answer>

例如：
<answer>mechanism=函数f返回输入干预集合与某个固定突变集合的对称差, K=A,C,E</answer>

或者（如果 K 是空集）：
<answer>mechanism=函数f返回输入干预集合本身, K=empty</answer>

如果诊断答案错误或格式不符，推理失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The Precision Medicine Laboratory is researching target drug response mechanisms.
Let's play a "Hidden Gene Mutation Deduction" game. Here are the rules:

The game defines a target gene universe set U = {{A, B, C, D, E, F, G, H, I, J}}, containing 10 candidate targets.

A secretly determined gene mutation subset K exists within the patient (K is a subset of U, possibly empty). Throughout the diagnostic reasoning process, K remains constant.

There is also a fixed drug response function f that takes any non-empty intervened target subset S you submit as input and returns another set of targets showing abnormal expression f(S). The specific pharmacological rule of function f is unknown to you, but it remains consistent throughout the process.

Your goal is to:
1. Infer the operating mechanism of the drug response function f (described in natural language).
2. Accurately identify which targets are in the hidden mutation subset K.

## Interaction Protocol

Each diagnostic round, you can submit a non-empty target subset S and request one of the following feedback types (only one per round):

1. **List Feedback**: The system will return all targets in set f(S) (unordered).
2. **Count Feedback**: The system will return the number of targets in f(S).
3. **Membership Test**: You specify a target x (x must be in U), and the system will tell you whether x is in f(S).

Notes:
- The submitted intervention set S cannot be empty.
- For the same S, no matter how many times you request, the returned test result is consistent.
- You must complete at least 3 rounds of interaction before submitting your final answer.
- Try to complete the reasoning with as few rounds as possible.

## Query and Answer Format (strictly required)

Each testing query must contain only one tag. Use the following XML format:

- **List Feedback** (e.g., querying target set {{A, B, C}}):
<query_list>A,B,C</query_list>

- **Count Feedback** (e.g., querying target set {{D, E}}):
<query_count>D,E</query_count>

- **Membership Test** (e.g., querying target set {{A, B}} and testing if C is in f(S)):
<query_member>A,B|C</query_member>

Note: The membership test format is "set elements|element to test", separated by a vertical bar.

## Submit Final Answer

After completing at least 3 rounds of interaction and gathering enough information, submit your final diagnostic answer in the following format:

<answer>mechanism=your description of function f, K=elements of set K (comma-separated, write empty if K is empty set)</answer>

For example:
<answer>mechanism=function f returns the symmetric difference between the intervention set and a fixed mutation set, K=A,C,E</answer>

Or (if K is empty set):
<answer>mechanism=function f returns the intervention set itself, K=empty</answer>

If the diagnostic answer is incorrect or the format is invalid, the deduction fails.
"""

    contextualized_rule_zh_3 = """\
智能教育平台正在评估学生的知识点掌握情况。
我们来玩一个"隐藏知识盲区推理"游戏，规则如下：

游戏设定了一个核心知识模块集合 U = {{A, B, C, D, E, F, G, H, I, J}}，包含 10 个模块。

系统已经秘密锁定了该学生的一个固定知识盲区子集 K（K 是 U 的子集，可能为空集）。在整个评估过程中，K 保持不变。

同时，存在一个固定的辅导效果评估函数 f，它接受你提交的任意非空考核模块子集 S 作为输入，返回最终被判定为需要重点复习的模块集合 f(S)。这个函数 f 的具体评估规则对你是未知的，但它在整个过程中保持一致。

你的目标是：
1. 推断出评估函数 f 的运作机制（用自然语言描述）。
2. 准确识别出隐藏的知识盲区子集 K 包含哪些模块。

## 交互方式

每一轮评估，你可以提交一个非空模块子集 S，并请求以下任一种反馈（每轮只能请求一种）：

1. **列表反馈**：系统会返回集合 f(S) 的所有模块（无序）。
2. **计数反馈**：系统会返回 f(S) 中模块的个数。
3. **单点判定**：你指定一个模块 x（x 必须在 U 中），系统会告诉你 x 是否在 f(S) 中。

注意：
- 提交的考核集合 S 不能为空。
- 对于相同的 S，无论请求多少次，返回的评估结果都是一致的。
- 你需要至少完成 3 轮评估交互后才能提交最终答案。
- 请尽可能用更少的轮数完成推理。

## 询问与提交答案的格式（严格要求）

每次评估询问只能包含一个标签。请使用以下 XML 格式：

- **列表反馈**（例如查询模块集合 {{A, B, C}}）：
<query_list>A,B,C</query_list>

- **计数反馈**（例如查询模块集合 {{D, E}}）：
<query_count>D,E</query_count>

- **单点判定**（例如查询模块集合 {{A, B}} 并判断 C 是否在 f(S) 中）：
<query_member>A,B|C</query_member>

注意：单点判定格式为"集合元素|待判定元素"，用竖线分隔。

## 提交最终答案

当你完成至少 3 轮交互并收集足够信息后，请提交最终分析答案，格式如下：

<answer>mechanism=你对评估函数f的描述, K=集合K的模块（用逗号分隔，如果是空集则写empty）</answer>

例如：
<answer>mechanism=函数f返回输入考核集合与某个固定盲区集合的对称差, K=A,C,E</answer>

或者（如果 K 是空集）：
<answer>mechanism=函数f返回输入考核集合本身, K=empty</answer>

如果分析答案错误或格式不符，评估失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The intelligent education platform is evaluating a student's mastery of knowledge points.
Let's play a "Hidden Knowledge Blind Spot Deduction" game. Here are the rules:

The game defines a core knowledge module universe set U = {{A, B, C, D, E, F, G, H, I, J}}, containing 10 modules.

The system has secretly locked onto a fixed knowledge blind spot subset K for the student (K is a subset of U, possibly empty). Throughout the evaluation process, K remains constant.

There is also a fixed tutoring effect evaluation function f that takes any non-empty tested module subset S you submit as input and returns another set of modules judged as needing intensive review f(S). The specific evaluation rule of function f is unknown to you, but it remains consistent throughout the process.

Your goal is to:
1. Infer the operating mechanism of the evaluation function f (described in natural language).
2. Accurately identify which modules are in the hidden blind spot subset K.

## Interaction Protocol

Each evaluation round, you can submit a non-empty module subset S and request one of the following feedback types (only one per round):

1. **List Feedback**: The system will return all modules in set f(S) (unordered).
2. **Count Feedback**: The system will return the number of modules in f(S).
3. **Membership Test**: You specify a module x (x must be in U), and the system will tell you whether x is in f(S).

Notes:
- The submitted testing set S cannot be empty.
- For the same S, no matter how many times you request, the returned evaluation result is consistent.
- You must complete at least 3 rounds of interaction before submitting your final answer.
- Try to complete the reasoning with as few rounds as possible.

## Query and Answer Format (strictly required)

Each evaluation query must contain only one tag. Use the following XML format:

- **List Feedback** (e.g., querying module set {{A, B, C}}):
<query_list>A,B,C</query_list>

- **Count Feedback** (e.g., querying module set {{D, E}}):
<query_count>D,E</query_count>

- **Membership Test** (e.g., querying module set {{A, B}} and testing if C is in f(S)):
<query_member>A,B|C</query_member>

Note: The membership test format is "set elements|element to test", separated by a vertical bar.

## Submit Final Answer

After completing at least 3 rounds of interaction and gathering enough information, submit your final analytical answer in the following format:

<answer>mechanism=your description of function f, K=elements of set K (comma-separated, write empty if K is empty set)</answer>

For example:
<answer>mechanism=function f returns the symmetric difference between the tested set and a fixed blind spot set, K=A,C,E</answer>

Or (if K is empty set):
<answer>mechanism=function f returns the tested set itself, K=empty</answer>

If the analytical answer is incorrect or the format is invalid, the evaluation fails.
"""

    contextualized_rule_zh_4 = """\
工业自动化流水线正在进行异常诊断测试。
我们来玩一个"隐藏系统性缺陷推理"游戏，规则如下：

游戏设定了一个质检节点集合 U = {{A, B, C, D, E, F, G, H, I, J}}，包含 10 个关键节点。

产线上存在一个秘密产生的固定异常节点子集 K（K 是 U 的子集，可能为空集）。在整个排查过程中，K 保持不变。

同时，存在一个固定的故障诊断函数 f，它接受你提交的任意非空抽样监测子集 S 作为输入，返回最终触发警报的节点集合 f(S)。这个函数 f 的具体诊断规则对你是未知的，但它在整个排查中保持一致。

你的目标是：
1. 推断出故障诊断函数 f 的运作机制（用自然语言描述）。
2. 准确识别出隐藏的异常节点子集 K 包含哪些节点。

## 交互方式

每一轮排查，你可以提交一个非空节点子集 S，并请求以下任一种反馈（每轮只能请求一种）：

1. **列表反馈**：系统会返回集合 f(S) 的所有节点（无序）。
2. **计数反馈**：系统会返回 f(S) 中节点的个数。
3. **单点判定**：你指定一个节点 x（x 必须在 U 中），系统会告诉你 x 是否在 f(S) 中。

注意：
- 提交的抽样监测集合 S 不能为空。
- 对于相同的 S，无论请求多少次，返回的诊断结果都是一致的。
- 你需要至少完成 3 轮排查交互后才能提交最终答案。
- 请尽可能用更少的轮数完成推理。

## 询问与提交答案的格式（严格要求）

每次诊断询问只能包含一个标签。请使用以下 XML 格式：

- **列表反馈**（例如查询节点集合 {{A, B, C}}）：
<query_list>A,B,C</query_list>

- **计数反馈**（例如查询节点集合 {{D, E}}）：
<query_count>D,E</query_count>

- **单点判定**（例如查询节点集合 {{A, B}} 并判断 C 是否在 f(S) 中）：
<query_member>A,B|C</query_member>

注意：单点判定格式为"集合元素|待判定元素"，用竖线分隔。

## 提交最终答案

当你完成至少 3 轮交互并收集足够信息后，请提交最终排查答案，格式如下：

<answer>mechanism=你对诊断函数f的描述, K=集合K的节点（用逗号分隔，如果是空集则写empty）</answer>

例如：
<answer>mechanism=函数f返回输入抽样集合与某个固定异常集合的对称差, K=A,C,E</answer>

或者（如果 K 是空集）：
<answer>mechanism=函数f返回输入抽样集合本身, K=empty</answer>

如果排查答案错误或格式不符，测试失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
The industrial automated assembly line is undergoing anomaly diagnostic testing.
Let's play a "Hidden Systemic Defect Deduction" game. Here are the rules:

The game defines a quality inspection node universe set U = {{A, B, C, D, E, F, G, H, I, J}}, containing 10 key nodes.

A secretly generated fixed subset of abnormal nodes K exists on the production line (K is a subset of U, possibly empty). Throughout the troubleshooting process, K remains constant.

There is also a fixed fault diagnostic function f that takes any non-empty sampled monitoring subset S you submit as input and returns another set of nodes triggering alarms f(S). The specific diagnostic rule of function f is unknown to you, but it remains consistent throughout the process.

Your goal is to:
1. Infer the operating mechanism of the diagnostic function f (described in natural language).
2. Accurately identify which nodes are in the hidden abnormal subset K.

## Interaction Protocol

Each troubleshooting round, you can submit a non-empty node subset S and request one of the following feedback types (only one per round):

1. **List Feedback**: The system will return all nodes in set f(S) (unordered).
2. **Count Feedback**: The system will return the number of nodes in f(S).
3. **Membership Test**: You specify a node x (x must be in U), and the system will tell you whether x is in f(S).

Notes:
- The submitted sampling set S cannot be empty.
- For the same S, no matter how many times you request, the returned diagnostic result is consistent.
- You must complete at least 3 rounds of interaction before submitting your final answer.
- Try to complete the reasoning with as few rounds as possible.

## Query and Answer Format (strictly required)

Each diagnostic query must contain only one tag. Use the following XML format:

- **List Feedback** (e.g., querying node set {{A, B, C}}):
<query_list>A,B,C</query_list>

- **Count Feedback** (e.g., querying node set {{D, E}}):
<query_count>D,E</query_count>

- **Membership Test** (e.g., querying node set {{A, B}} and testing if C is in f(S)):
<query_member>A,B|C</query_member>

Note: The membership test format is "set elements|element to test", separated by a vertical bar.

## Submit Final Answer

After completing at least 3 rounds of interaction and gathering enough information, submit your final troubleshooting answer in the following format:

<answer>mechanism=your description of function f, K=elements of set K (comma-separated, write empty if K is empty set)</answer>

For example:
<answer>mechanism=function f returns the symmetric difference between the sampled set and a fixed abnormal set, K=A,C,E</answer>

Or (if K is empty set):
<answer>mechanism=function f returns the sampled set itself, K=empty</answer>

If the troubleshooting answer is incorrect or the format is invalid, the test fails.
"""

    contextualized_rule_zh_5 = """\
司法推演系统正在对一宗复杂商业纠纷进行逻辑梳理。
我们来玩一个"隐藏核心证据推理"游戏，规则如下：

案件设定了一个关键证据链集合 U = {{A, B, C, D, E, F, G, H, I, J}}，包含 10 项法条或证据。

案卷中隐藏了一个被秘密篡改或隐瞒的核心违规证据子集 K（K 是 U 的子集，可能为空集）。在整个推演过程中，K 保持不变。

同时，存在一个固定的法庭质证判定函数 f，它接受你提交的任意非空主张证据子集 S 作为输入，返回最终在法庭上产生争议或被驳回的证据集合 f(S)。这个函数 f 的具体判定规则对你是未知的，但它在整个推演中保持一致。

你的目标是：
1. 推断出质证判定函数 f 的运作机制（用自然语言描述）。
2. 准确识别出隐藏的核心违规证据子集 K 包含哪些证据。

## 交互方式

每一轮推演，你可以提交一个非空证据子集 S，并请求以下任一种反馈（每轮只能请求一种）：

1. **列表反馈**：系统会返回集合 f(S) 的所有证据（无序）。
2. **计数反馈**：系统会返回 f(S) 中证据的个数。
3. **单点判定**：你指定一个证据 x（x 必须在 U 中），系统会告诉你 x 是否在 f(S) 中。

注意：
- 提交的主张证据集合 S 不能为空。
- 对于相同的 S，无论请求多少次，返回的质证结果都是一致的。
- 你需要至少完成 3 轮推演交互后才能提交最终答案。
- 请尽可能用更少的轮数完成推理。

## 询问与提交答案的格式（严格要求）

每次推演询问只能包含一个标签。请使用以下 XML格式：

- **列表反馈**（例如查询证据集合 {{A, B, C}}）：
<query_list>A,B,C</query_list>

- **计数反馈**（例如查询证据集合 {{D, E}}）：
<query_count>D,E</query_count>

- **单点判定**（例如查询证据集合 {{A, B}} 并判断 C 是否在 f(S) 中）：
<query_member>A,B|C</query_member>

注意：单点判定格式为"集合元素|待判定元素"，用竖线分隔。

## 提交最终答案

当你完成至少 3 轮交互并收集足够信息后，请提交最终判决建议，格式如下：

<answer>mechanism=你对判定函数f的描述, K=集合K的证据（用逗号分隔，如果是空集则写empty）</answer>

例如：
<answer>mechanism=函数f返回输入主张集合与某个固定违规集合的对称差, K=A,C,E</answer>

或者（如果 K 是空集）：
<answer>mechanism=函数f返回输入主张集合本身, K=empty</answer>

如果判决建议错误或格式不符，推演失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The judicial simulation system is logically sorting out a complex commercial dispute.
Let's play a "Hidden Core Evidence Deduction" game. Here are the rules:

The case defines a key evidence chain universe set U = {{A, B, C, D, E, F, G, H, I, J}}, containing 10 articles of law or evidence items.

A secretly tampered or concealed core violation evidence subset K is hidden in the case file (K is a subset of U, possibly empty). Throughout the simulation process, K remains constant.

There is also a fixed court cross-examination ruling function f that takes any non-empty claimed evidence subset S you submit as input and returns another set of evidence that ultimately causes controversy or gets rejected in court f(S). The specific ruling rule of function f is unknown to you, but it remains consistent throughout the simulation.

Your goal is to:
1. Infer the operating mechanism of the ruling function f (described in natural language).
2. Accurately identify which evidence items are in the hidden core violation subset K.

## Interaction Protocol

Each simulation round, you can submit a non-empty evidence subset S and request one of the following feedback types (only one per round):

1. **List Feedback**: The system will return all evidence items in set f(S) (unordered).
2. **Count Feedback**: The system will return the number of evidence items in f(S).
3. **Membership Test**: You specify an evidence item x (x must be in U), and the system will tell you whether x is in f(S).

Notes:
- The submitted claimed evidence set S cannot be empty.
- For the same S, no matter how many times you request, the returned cross-examination result is consistent.
- You must complete at least 3 rounds of interaction before submitting your final answer.
- Try to complete the reasoning with as few rounds as possible.

## Query and Answer Format (strictly required)

Each simulation query must contain only one tag. Use the following XML format:

- **List Feedback** (e.g., querying evidence set {{A, B, C}}):
<query_list>A,B,C</query_list>

- **Count Feedback** (e.g., querying evidence set {{D, E}}):
<query_count>D,E</query_count>

- **Membership Test** (e.g., querying evidence set {{A, B}} and testing if C is in f(S)):
<query_member>A,B|C</query_member>

Note: The membership test format is "set elements|element to test", separated by a vertical bar.

## Submit Final Answer

After completing at least 3 rounds of interaction and gathering enough information, submit your final judgment proposal in the following format:

<answer>mechanism=your description of function f, K=elements of set K (comma-separated, write empty if K is empty set)</answer>

For example:
<answer>mechanism=function f returns the symmetric difference between the claimed set and a fixed violation set, K=A,C,E</answer>

Or (if K is empty set):
<answer>mechanism=function f returns the claimed set itself, K=empty</answer>

If the judgment proposal is incorrect or the format is invalid, the simulation fails.
"""

    tags = ["answer", "query_list", "query_count", "query_member"]
    
    reasoning_type = "归纳推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "K": set(),
                "description": "函数f返回输入集合本身"
            },
            2: {
                "K": {"A"},
                "description": "函数f返回输入集合与固定集合{A}的对称差"
            },
            3: {
                "K": {"B", "D", "F"},
                "description": "函数f返回输入集合与固定集合{B,D,F}的对称差"
            },
            4: {
                "K": {"A", "C", "E", "G", "I"},
                "description": "函数f返回输入集合与固定集合{A,C,E,G,I}的对称差"
            },
            5: {
                "K": {"A", "B", "C", "D", "E"},
                "description": "函数f返回输入集合与固定集合{A,B,C,D,E}的对称差"
            },
        },
        "en": {
            1: {
                "K": set(),
                "description": "function f returns the input set itself"
            },
            2: {
                "K": {"A"},
                "description": "function f returns the symmetric difference between the input set and a fixed set {A}"
            },
            3: {
                "K": {"B", "D", "F"},
                "description": "function f returns the symmetric difference between the input set and a fixed set {B,D,F}"
            },
            4: {
                "K": {"A", "C", "E", "G", "I"},
                "description": "function f returns the symmetric difference between the input set and a fixed set {A,C,E,G,I}"
            },
            5: {
                "K": {"A", "B", "C", "D", "E"},
                "description": "function f returns the symmetric difference between the input set and a fixed set {A,B,C,D,E}"
            },
        },
    }

    def __init__(self, config):
        self.round_count = 0 
        self.query_history = []
        self.universe = {"A", "B", "C", "D", "E", "F", "G", "H", "I", "J"}
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保 difficulty 是整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self.K = cfg["K"]
        self.expected_mechanism_desc = cfg["description"]
        self._game_info["n"] = 10

    def _apply_function(self, S: set) -> set:
        return S.symmetric_difference(self.K)

    def parse(self, response: str):
        response = response.strip()
        parsed_info = {}

        for tag in self.tags:
            pattern = rf'<{tag}>\s*(.*?)\s*</{tag}>'
            match = re.search(pattern, response, re.IGNORECASE | re.DOTALL)
            if match:
                parsed_info[tag] = match.group(1).strip()
        
        contain_answer = "answer" in parsed_info
        contain_query = any(
            tag in parsed_info
            for tag in self.tags
            if tag != "answer"
        )

        if contain_answer and self.round_count < 3:
            parsed_info.pop("answer")
            parsed_info["early_answer_error"] = True
            contain_answer = False

        if contain_answer or contain_query or "early_answer_error" in parsed_info:
            return parsed_info
        else:
            raise ValueError(
                f"Invalid LLM response. Parsed tags: {list(parsed_info.keys())}; "
                f"expected tags: {list(self.tags)}, and require either 'answer' "
                f"or at least one query tag to be present."
            )

    def evaluate(self, parsed_info):
        if self.round_count < 3:
            return False

        raw_ans = parsed_info["answer"]
        
        try:
            # 使用正则表达式提取 mechanism 和 K 部分
            # K= 可能出现在 mechanism 描述中，所以我们找最后一个 ", K=" 作为分隔
            k_pattern = re.search(r',\s*K\s*=\s*(.+)$', raw_ans, re.IGNORECASE)
            m_pattern = re.search(r'^mechanism\s*=\s*(.+?)(?:,\s*K\s*=)', raw_ans, re.IGNORECASE | re.DOTALL)
            
            if k_pattern is None or m_pattern is None:
                return False
            
            mechanism_part = m_pattern.group(1).strip()
            k_part = k_pattern.group(1).strip()
            
            if k_part.lower() == "empty":
                submitted_K = set()
            else:
                submitted_K = set(x.strip().upper() for x in k_part.split(",") if x.strip())
            
            # 验证提交的 K 与所有历史查询的一致性
            for S, feedback_type, feedback_value in self.query_history:
                computed_fS = S.symmetric_difference(submitted_K)
                
                if feedback_type == "list":
                    if computed_fS != feedback_value:
                        return False
                elif feedback_type == "count":
                    if len(computed_fS) != feedback_value:
                        return False
                elif feedback_type == "member":
                    element, is_member = feedback_value
                    if (element in computed_fS) != is_member:
                        return False
            
            mechanism_lower = mechanism_part.lower()
            keywords_zh = ["对称差", "异或"]
            keywords_en = ["symmetric difference", "xor"]
            
            if self.config.language == "zh":
                has_keyword = any(kw in mechanism_lower for kw in keywords_zh)
            else:
                has_keyword = any(kw in mechanism_lower for kw in keywords_en)
            
            if submitted_K == set():
                return_itself_zh = ["返回输入集合本身", "返回本身", "不变"]
                return_itself_en = ["returns the input set itself", "returns itself", "unchanged"]
                if self.config.language == "zh":
                    has_keyword = has_keyword or any(kw in mechanism_lower for kw in return_itself_zh)
                else:
                    has_keyword = has_keyword or any(kw in mechanism_lower for kw in return_itself_en)
            
            return has_keyword and submitted_K == self.K
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            err_empty = "错误：提交的集合不能为空。"
            err_invalid = "错误：集合元素必须在宇宙集合 U 中。"
            err_format = "错误：格式无效。"
            err_early = "错误：你需要至少完成 3 轮交互后才能提交最终答案。"
        else:
            yes_res, no_res = "Yes", "No"
            err_empty = "Error: The submitted set cannot be empty."
            err_invalid = "Error: Set elements must be in universe U."
            err_format = "Error: Invalid format."
            err_early = "Error: You must complete at least 3 rounds of interaction before submitting your answer."

        try:
            if "early_answer_error" in parsed_info:
                return err_early
                
            elif "query_list" in parsed_info:
                raw = parsed_info["query_list"].strip()
                if not raw:
                    return err_empty
                
                S = set(x.strip().upper() for x in raw.split(",") if x.strip())
                if not S:
                    return err_empty
                if not S.issubset(self.universe):
                    return err_invalid
                
                fS = self._apply_function(S)
                self.round_count += 1
                self.query_history.append((S, "list", fS))
                
                if fS:
                    result = ",".join(sorted(fS))
                else:
                    result = "empty" if self.config.language == "en" else "空集"
                return result

            elif "query_count" in parsed_info:
                raw = parsed_info["query_count"].strip()
                if not raw:
                    return err_empty
                
                S = set(x.strip().upper() for x in raw.split(",") if x.strip())
                if not S:
                    return err_empty
                if not S.issubset(self.universe):
                    return err_invalid
                
                fS = self._apply_function(S)
                count = len(fS)
                self.round_count += 1
                self.query_history.append((S, "count", count))
                
                return str(count)

            elif "query_member" in parsed_info:
                raw = parsed_info["query_member"].strip()
                if "|" not in raw:
                    return err_format
                
                parts = raw.split("|")
                if len(parts) != 2:
                    return err_format
                
                set_part, elem_part = parts[0].strip(), parts[1].strip().upper()
                
                if not set_part:
                    return err_empty
                
                S = set(x.strip().upper() for x in set_part.split(",") if x.strip())
                if not S:
                    return err_empty
                if not S.issubset(self.universe):
                    return err_invalid
                if elem_part not in self.universe:
                    return err_invalid
                
                fS = self._apply_function(S)
                is_member = elem_part in fS
                self.round_count += 1
                self.query_history.append((S, "member", (elem_part, is_member)))
                
                return yes_res if is_member else no_res

            else:
                raise ValueError("No valid query tag found.")
                
        except Exception as e:
            raise ValueError(f"{err_format} Details: {str(e)}")

    def _cf_make_wrong(self, correct: str) -> str:
        correct = correct.strip()
        
        # 处理数字（count反馈）
        if correct.isdigit():
            val = int(correct)
            return str(val + 1) if val < 10 else str(val - 1)
        
        # 处理是/否（member反馈）
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
        
        # 处理空集
        if correct.lower() == "empty" or correct == "空集":
            return "A"
        
        # 处理列表反馈（如 "A,C,E"）
        elements = set(x.strip().upper() for x in correct.split(",") if x.strip())
        universe_list = sorted(self.universe)
        
        # 找一个不在结果中的元素添加进去，或者移除一个元素
        not_in_result = [x for x in universe_list if x not in elements]
        if not_in_result:
            elements.add(not_in_result[0])
        elif elements:
            elements.pop()
        
        if not elements:
            return "empty" if self.config.language == "en" else "空集"
        return ",".join(sorted(elements))

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        universe_list = sorted(list(self.universe))
        
        if self.config.language == "zh":
            ans_yes, ans_no = "是", "否"
            ans_empty = "空集"
        else:
            ans_yes, ans_no = "Yes", "No"
            ans_empty = "empty"

        # 只生成单元素和双元素子集的查询，以及全集查询，避免组合爆炸
        subsets_to_query = []
        
        # 单元素子集
        for elem in universe_list:
            subsets_to_query.append({elem})
        
        # 几个代表性的双元素子集
        for i in range(0, len(universe_list) - 1, 2):
            subsets_to_query.append({universe_list[i], universe_list[i+1]})
        
        # 全集
        subsets_to_query.append(set(universe_list))
        
        for S in subsets_to_query:
            s_list_sorted = sorted(list(S))
            s_str = ",".join(s_list_sorted)
            
            fS = S.symmetric_difference(self.K)
            fS_sorted = sorted(list(fS))
            
            if not fS:
                ans_list = ans_empty
            else:
                ans_list = ",".join(fS_sorted)
            
            # 只生成 list 反馈查询
            queries.append({
                "query": f"<query_list>{s_str}</query_list>",
                "answer": ans_list
            })
                
        return queries