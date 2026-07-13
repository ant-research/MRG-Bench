# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 图：存在一个由节点和边构成的图。
# 知识点:   边存在性：两个给定节点之间是否存在直接相连的边
# ============================================================

from .base import Game
import re


class HiddenRelationGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "图"
    enable_counterfactual = False   # 设为 True 时开启反事实干预模式

    game_rule_zh = """\
我们来玩一个"隐藏关系推理"游戏，规则如下：

游戏设定了一个标号集合 V = {{0, 1, ..., {n_minus_1}}}，共 {n} 个元素。

在这个集合上，存在一个未知的二元关系 E。这个关系满足以下性质：
1. 对称性：如果元素对 {{u, v}} 满足关系 E，那么 {{v, u}} 也满足关系 E。
2. 无自环：任何元素不与自己构成关系，即 {{u, u}} 不存在。
3. 非平凡：既存在满足关系的元素对，也存在不满足关系的元素对。

这个关系由一个仅依赖于元素标号的确定性规则决定，但该规则对你是未知的。

## 禁问集合
有一组特定的元素对被设置为"禁问对" F，你不能直接查询这些对是否满足关系 E。禁问对集合为：
{forbidden_pairs_str}

## 查询配额
你有 {quota} 次查询机会。你需要通过查询非禁问对来推断出生成关系 E 的规则，并最终预测所有禁问对是否满足关系 E。

## 你可以进行的操作

1. **查询边存在性**：询问某个非禁问的元素对 {{u, v}} 是否满足关系 E。
   - 要求：u 不等于 v，{{u, v}} 不在禁问集合 F 中，且此前未查询过该对。
   - 我会回答"有"或"没有"。

2. **查询剩余配额**：询问还剩多少次查询机会。
   - 我会回答一个非负整数。

3. **最终提交**：当你认为已掌握规律时，对所有禁问对进行预测。
   - 你需要对每个禁问对给出"有"或"没有"的判断。

## 查询与提交格式（必须严格遵守）

每次操作只能包含一个标签，使用以下 XML格式：

- 查询边存在性（例如查询元素 2 和 5）：
<query_edge>2,5</query_edge>

- 查询剩余配额：
<query_budget></query_budget>

- 最终提交答案（对所有禁问对进行预测）：
<answer>{{0,3}}=有, {{1,4}}=没有, {{2,5}}=有</answer>

注意：
1. 答案中必须包含所有禁问对的预测，格式为"{{u,v}}=有"或"{{u,v}}=没有"，用逗号分隔。
2. 元素对顺序不限（{{2,5}} 和 {{5,2}} 等价）。
3. 不得查询禁问对或重复查询同一对。
4. 不得超出查询配额。
5. 请尽可能少地使用查询次数，通过归纳推理找出规则。

违反任何约束或预测错误将导致游戏失败。
"""

    game_rule_en = """\
Let's play a "Hidden Relation Inference" game. Here are the rules:

There is a labeled set V = {{0, 1, ..., {n_minus_1}}}, containing {n} elements in total.

On this set, there exists an unknown binary relation E. This relation satisfies the following properties:
1. Symmetry: If element pair {{u, v}} satisfies relation E, then {{v, u}} also satisfies relation E.
2. No self-loops: No element is related to itself, i.e., {{u, u}} does not exist.
3. Non-trivial: There exist both pairs that satisfy the relation and pairs that do not.

This relation is determined by a deterministic rule that depends only on element labels, but the rule is unknown to you.

## Forbidden Set
A specific set of element pairs is designated as "forbidden pairs" F. You cannot directly query whether these pairs satisfy relation E. The forbidden pair set is:
{forbidden_pairs_str}

## Query Quota
You have {quota} query opportunities. You need to infer the rule generating relation E by querying non-forbidden pairs, and ultimately predict whether all forbidden pairs satisfy relation E.

## Available Operations

1. **Query Edge Existence**: Ask whether a non-forbidden element pair {{u, v}} satisfies relation E.
   - Requirements: u is not equal to v, {{u, v}} is not in forbidden set F, and the pair has not been queried before.
   - I will answer "Yes" or "No".

2. **Query Remaining Quota**: Ask how many query opportunities remain.
   - I will answer with a non-negative integer.

3. **Final Submission**: When you believe you have grasped the pattern, predict all forbidden pairs.
   - You need to give a "Yes" or "No" judgment for each forbidden pair.

## Query and Submission Format (must strictly follow)

Each operation can only contain one tag, using the following XML format:

- Query edge existence (e.g., query elements 2 and 5):
<query_edge>2,5</query_edge>

- Query remaining quota:
<query_budget></query_budget>

- Final answer submission (predict all forbidden pairs):
<answer>{{0,3}}=Yes, {{1,4}}=No, {{2,5}}=Yes</answer>

Notes:
1. The answer must include predictions for all forbidden pairs, formatted as "{{u,v}}=Yes" or "{{u,v}}=No", separated by commas.
2. Element pair order does not matter ({{2,5}} and {{5,2}} are equivalent).
3. Do not query forbidden pairs or repeatedly query the same pair.
4. Do not exceed the query quota.
5. Use as few queries as possible and find the rule through inductive reasoning.

Violating any constraint or making incorrect predictions will result in game failure.
"""

    contextualized_rule_zh_1 = """\
作为城市交通规划师，你需要摸清一张未知交通网络的连通规则。

我们来玩一个"隐藏交通网络推理"游戏，规则如下：

系统设定了一个交通枢纽编号集合 V = {{0, 1, ..., {n_minus_1}}}，共 {n} 个枢纽。

在这个集合上，存在一个未知的直达连通关系 E。这个连通关系满足以下性质：
1. 对称性：如果枢纽对 {{u, v}} 存在双向直达连通 E，那么 {{v, u}} 也同样连通。
2. 无自环：任何枢纽不与自己构成连通关系，即 {{u, u}} 不存在。
3. 非平凡：既存在相互连通的枢纽对，也存在不连通的枢纽对。

这个连通关系由一个仅依赖于枢纽编号的确定性规则决定，但该规则对你是未知的。

## 禁问集合
有一组特定的枢纽对被设置为"禁查路线" F，你不能直接查询这些对是否连通。禁查路线集合为：
{forbidden_pairs_str}

## 查询配额
你有 {quota} 次查询机会。你需要通过查询非禁查路线来推断出生成连通关系 E 的规则，并最终预测所有禁查路线是否连通。

## 你可以进行的操作

1. **查询边存在性**：询问某个非禁查的枢纽对 {{u, v}} 是否存在直达连通 E。
   - 要求：u 不等于 v，{{u, v}} 不在禁查路线集合 F 中，且此前未查询过该路线。
   - 我会回答"有"或"没有"。

2. **查询剩余配额**：询问还剩多少次查询机会。
   - 我会回答一个非负整数。

3. **最终提交**：当你认为已掌握规律时，对所有禁查路线进行预测。
   - 你需要对每个禁查路线给出"有"或"没有"的判断。

## 查询与提交格式（必须严格遵守）

每次操作只能包含一个标签，使用以下 XML 格式：

- 查询边存在性（例如查询枢纽 2 和 5）：
<query_edge>2,5</query_edge>

- 查询剩余配额：
<query_budget></query_budget>

- 最终提交答案（对所有禁查路线进行预测）：
<answer>{{0,3}}=有, {{1,4}}=没有, {{2,5}}=有</answer>

注意：
1. 答案中必须包含所有禁查路线的预测，格式为"{{u,v}}=有"或"{{u,v}}=没有"，用逗号分隔。
2. 枢纽对顺序不限（{{2,5}} 和 {{5,2}} 等价）。
3. 不得查询禁查路线或重复查询同一路线。
4. 不得超出查询配额。
5. 请尽可能少地使用查询次数，通过归纳推理找出规则。

违反任何约束或预测错误将导致规划任务失败。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
As an urban traffic planner, you need to uncover the connectivity rules of an unknown transportation network.

Let's play a "Hidden Traffic Network Inference" game. Here are the rules:

There is a designated set of traffic hub labels V = {{0, 1, ..., {n_minus_1}}}, containing {n} hubs in total.

On this set, there exists an unknown direct connectivity relation E. This relation satisfies the following properties:
1. Symmetry: If hub pair {{u, v}} satisfies relation E, then {{v, u}} also satisfies relation E.
2. No self-loops: No hub is connected to itself, i.e., {{u, u}} does not exist.
3. Non-trivial: There exist both pairs that satisfy the relation and pairs that do not.

This relation is determined by a deterministic rule that depends only on hub labels, but the rule is unknown to you.

## Forbidden Set
A specific set of hub pairs is designated as "forbidden routes" F. You cannot directly query whether these routes satisfy relation E. The forbidden route set is:
{forbidden_pairs_str}

## Query Quota
You have {quota} query opportunities. You need to infer the rule generating relation E by querying non-forbidden routes, and ultimately predict whether all forbidden routes satisfy relation E.

## Available Operations

1. **Query Edge Existence**: Ask whether a non-forbidden hub pair {{u, v}} satisfies relation E.
   - Requirements: u is not equal to v, {{u, v}} is not in the forbidden set F, and the route has not been queried before.
   - I will answer "Yes" or "No".

2. **Query Remaining Quota**: Ask how many query opportunities remain.
   - I will answer with a non-negative integer.

3. **Final Submission**: When you believe you have grasped the pattern, predict all forbidden routes.
   - You need to give a "Yes" or "No" judgment for each forbidden route.

## Query and Submission Format (must strictly follow)

Each operation can only contain one tag, using the following XML format:

- Query edge existence (e.g., query hubs 2 and 5):
<query_edge>2,5</query_edge>

- Query remaining quota:
<query_budget></query_budget>

- Final answer submission (predict all forbidden routes):
<answer>{{0,3}}=Yes, {{1,4}}=No, {{2,5}}=Yes</answer>

Notes:
1. The answer must include predictions for all forbidden routes, formatted as "{{u,v}}=Yes" or "{{u,v}}=No", separated by commas.
2. Hub pair order does not matter ({{2,5}} and {{5,2}} are equivalent).
3. Do not query forbidden routes or repeatedly query the same route.
4. Do not exceed the query quota.
5. Use as few queries as possible and find the rule through inductive reasoning.

Violating any constraint or making incorrect predictions will result in planning failure.
"""

    contextualized_rule_zh_2 = """\
作为临床药学专家，你需要推断一种新型药物库中不同成分之间是否存在相互作用。

我们来玩一个"隐藏药物作用推理"游戏，规则如下：

系统设定了一个药物成分编号集合 V = {{0, 1, ..., {n_minus_1}}}，共 {n} 种成分。

在这个集合上，存在一个未知的相互作用关系 E。这个相互作用满足以下性质：
1. 对称性：如果成分对 {{u, v}} 存在相互作用 E，那么 {{v, u}} 也同样存在。
2. 无自环：任何成分不与自己构成相互作用测试，即 {{u, u}} 不存在。
3. 非平凡：既存在产生相互作用的成分对，也存在无相互作用的成分对。

这个相互作用由一个仅依赖于成分编号的确定性规则决定，但该规则对你是未知的。

## 禁问集合
有一组特定的成分对被设置为"临床禁忌测试对" F，你不能直接查询这些对是否存在相互作用。禁忌测试集合为：
{forbidden_pairs_str}

## 查询配额
你有 {quota} 次查询机会。你需要通过查询非禁忌对来推断出生成关系 E 的规则，并最终预测所有禁忌测试对是否存在相互作用 E。

## 你可以进行的操作

1. **查询边存在性**：询问某个非禁忌的成分对 {{u, v}} 是否存在相互作用 E。
   - 要求：u 不等于 v，{{u, v}} 不在禁忌测试集合 F 中，且此前未查询过该组合。
   - 我会回答"有"或"没有"。

2. **查询剩余配额**：询问还剩多少次查询机会。
   - 我会回答一个非负整数。

3. **最终提交**：当你认为已掌握规律时，对所有临床禁忌测试对进行预测。
   - 你需要对每个禁忌对给出"有"或"没有"的判断。

## 查询与提交格式（必须严格遵守）

每次操作只能包含一个标签，使用以下 XML 格式：

- 查询边存在性（例如查询成分 2 和 5）：
<query_edge>2,5</query_edge>

- 查询剩余配额：
<query_budget></query_budget>

- 最终提交答案（对所有禁忌对进行预测）：
<answer>{{0,3}}=有, {{1,4}}=没有, {{2,5}}=有</answer>

注意：
1. 答案中必须包含所有禁忌对的预测，格式为"{{u,v}}=有"或"{{u,v}}=没有"，用逗号分隔。
2. 成分对顺序不限（{{2,5}} 和 {{5,2}} 等价）。
3. 不得查询禁忌对或重复查询同一对。
4. 不得超出查询配额。
5. 请尽可能少地使用查询次数，通过归纳推理找出规则。

违反任何约束或预测错误将导致临床分析失败。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
As a clinical pharmacy expert, you need to infer whether there are drug-drug interactions between different compounds in a novel drug library.

Let's play a "Hidden Drug Interaction Inference" game. Here are the rules:

There is a set of designated drug compound labels V = {{0, 1, ..., {n_minus_1}}}, containing {n} compounds in total.

On this set, there exists an unknown interaction relation E. This interaction satisfies the following properties:
1. Symmetry: If compound pair {{u, v}} has interaction E, then {{v, u}} also has it.
2. No self-loops: No compound is tested for interaction with itself, i.e., {{u, u}} does not exist.
3. Non-trivial: There exist both pairs that interact and pairs that do not.

This interaction is determined by a deterministic rule that depends only on compound labels, but the rule is unknown to you.

## Forbidden Set
A specific set of compound pairs is designated as "clinical contraindication pairs" F. You cannot directly query whether these pairs have interactions. The forbidden pair set is:
{forbidden_pairs_str}

## Query Quota
You have {quota} query opportunities. You need to infer the rule generating relation E by querying non-forbidden pairs, and ultimately predict whether all contraindication pairs have interaction E.

## Available Operations

1. **Query Edge Existence**: Ask whether a non-forbidden compound pair {{u, v}} has interaction E.
   - Requirements: u is not equal to v, {{u, v}} is not in the forbidden set F, and the pair has not been queried before.
   - I will answer "Yes" or "No".

2. **Query Remaining Quota**: Ask how many query opportunities remain.
   - I will answer with a non-negative integer.

3. **Final Submission**: When you believe you have grasped the pattern, predict all clinical contraindication pairs.
   - You need to give a "Yes" or "No" judgment for each forbidden pair.

## Query and Submission Format (must strictly follow)

Each operation can only contain one tag, using the following XML format:

- Query edge existence (e.g., query compounds 2 and 5):
<query_edge>2,5</query_edge>

- Query remaining quota:
<query_budget></query_budget>

- Final answer submission (predict all contraindication pairs):
<answer>{{0,3}}=Yes, {{1,4}}=No, {{2,5}}=Yes</answer>

Notes:
1. The answer must include predictions for all contraindication pairs, formatted as "{{u,v}}=Yes" or "{{u,v}}=No", separated by commas.
2. Compound pair order does not matter ({{2,5}} and {{5,2}} are equivalent).
3. Do not query contraindication pairs or repeatedly query the same pair.
4. Do not exceed the query quota.
5. Use as few queries as possible and find the rule through inductive reasoning.

Violating any constraint or making incorrect predictions will result in clinical analysis failure.
"""

    contextualized_rule_zh_3 = """\
作为课程研发主管，你需要梳理一套全新教学大纲中知识点之间的交叉融合关联逻辑。

我们来玩一个"隐藏知识关联推理"游戏，规则如下：

大纲设定了一个核心知识点编号集合 V = {{0, 1, ..., {n_minus_1}}}，共 {n} 个知识点。

在这个集合上，存在一个未知的学科交叉关联 E。这个关联满足以下性质：
1. 对称性：如果知识点对 {{u, v}} 存在交叉关联 E，那么 {{v, u}} 也同样存在关联。
2. 无自环：任何知识点不与自己构成关联比较，即 {{u, u}} 不存在。
3. 非平凡：既存在有关联的知识点对，也存在无关联的知识点对。

这个关联关系由一个仅依赖于知识点编号的确定性规则决定，但该规则对你是未知的。

## 禁问集合
有一组特定的知识点对被设置为"盲盒评估对" F，你不能直接查询这些对是否存在关联。盲盒评估集合为：
{forbidden_pairs_str}

## 查询配额
你有 {quota} 次查询机会。你需要通过查询非盲盒对来推断出生成关联 E 的规则，并最终预测所有盲盒评估对是否存在交叉关联。

## 你可以进行的操作

1. **查询边存在性**：询问某个非盲盒的知识点对 {{u, v}} 是否存在交叉关联 E。
   - 要求：u 不等于 v，{{u, v}} 不在盲盒评估集合 F 中，且此前未查询过该对。
   - 我会回答"有"或"没有"。

2. **查询剩余配额**：询问还剩多少次查询机会。
   - 我会回答一个非负整数。

3. **最终提交**：当你认为已掌握规律时，对所有盲盒评估对进行预测。
   - 你需要对每个盲盒对给出"有"或"没有"的判断。

## 查询与提交格式（必须严格遵守）

每次操作只能包含一个标签，使用以下 XML 格式：

- 查询边存在性（例如查询知识点 2 和 5）：
<query_edge>2,5</query_edge>

- 查询剩余配额：
<query_budget></query_budget>

- 最终提交答案（对所有盲盒评估对进行预测）：
<answer>{{0,3}}=有, {{1,4}}=没有, {{2,5}}=有</answer>

注意：
1. 答案中必须包含所有盲盒评估对的预测，格式为"{{u,v}}=有"或"{{u,v}}=没有"，用逗号分隔。
2. 知识点对顺序不限（{{2,5}} 和 {{5,2}} 等价）。
3. 不得查询盲盒评估对或重复查询同一对。
4. 不得超出查询配额。
5. 请尽可能少地使用查询次数，通过归纳推理找出规则。

违反任何约束或预测错误将导致大纲梳理失败。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
As a curriculum development director, you need to map out the cross-disciplinary correlation logic between knowledge points in a brand-new syllabus.

Let's play a "Hidden Knowledge Correlation Inference" game. Here are the rules:

The syllabus defines a set of core knowledge point labels V = {{0, 1, ..., {n_minus_1}}}, containing {n} points in total.

On this set, there exists an unknown cross-disciplinary correlation E. This correlation satisfies the following properties:
1. Symmetry: If knowledge point pair {{u, v}} has correlation E, then {{v, u}} also has it.
2. No self-loops: No knowledge point is correlated with itself for this purpose, i.e., {{u, u}} does not exist.
3. Non-trivial: There exist both pairs that are correlated and pairs that are not.

This correlation is determined by a deterministic rule that depends only on the point labels, but the rule is unknown to you.

## Forbidden Set
A specific set of knowledge point pairs is designated as "blind-box evaluation pairs" F. You cannot directly query whether these pairs are correlated. The forbidden pair set is:
{forbidden_pairs_str}

## Query Quota
You have {quota} query opportunities. You need to infer the rule generating correlation E by querying non-forbidden pairs, and ultimately predict whether all blind-box evaluation pairs have correlation E.

## Available Operations

1. **Query Edge Existence**: Ask whether a non-forbidden knowledge point pair {{u, v}} has correlation E.
   - Requirements: u is not equal to v, {{u, v}} is not in the blind-box evaluation set F, and the pair has not been queried before.
   - I will answer "Yes" or "No".

2. **Query Remaining Quota**: Ask how many query opportunities remain.
   - I will answer with a non-negative integer.

3. **Final Submission**: When you believe you have grasped the pattern, predict all blind-box evaluation pairs.
   - You need to give a "Yes" or "No" judgment for each forbidden pair.

## Query and Submission Format (must strictly follow)

Each operation can only contain one tag, using the following XML format:

- Query edge existence (e.g., query knowledge points 2 and 5):
<query_edge>2,5</query_edge>

- Query remaining quota:
<query_budget></query_budget>

- Final answer submission (predict all blind-box pairs):
<answer>{{0,3}}=Yes, {{1,4}}=No, {{2,5}}=Yes</answer>

Notes:
1. The answer must include predictions for all blind-box pairs, formatted as "{{u,v}}=Yes" or "{{u,v}}=No", separated by commas.
2. Knowledge point pair order does not matter ({{2,5}} and {{5,2}} are equivalent).
3. Do not query blind-box pairs or repeatedly query the same pair.
4. Do not exceed the query quota.
5. Use as few queries as possible and find the rule through inductive reasoning.

Violating any constraint or making incorrect predictions will result in curriculum mapping failure.
"""

    contextualized_rule_zh_4 = """\
作为智能制造系统工程师，你需要测试新产线上各模块间的装配兼容互换性。

我们来玩一个"隐藏装配兼容推理"游戏，规则如下：

产线设定了一个加工模块编号集合 V = {{0, 1, ..., {n_minus_1}}}，共 {n} 个模块。

在这个集合上，存在一个未知的装配兼容关系 E。这个兼容关系满足以下性质：
1. 对称性：如果模块对 {{u, v}} 存在装配兼容 E，那么 {{v, u}} 也同样兼容。
2. 无自环：任何模块不与自己进行装配兼容测试，即 {{u, u}} 不存在。
3. 非平凡：既存在兼容的模块对，也存在不兼容的模块对。

这个兼容关系由一个仅依赖于模块编号的确定性工艺规则决定，但该规则对你是未知的。

## 禁问集合
有一组特定的模块对被设置为"限制测试对" F，你不能直接查询这些对是否兼容。限制测试集合为：
{forbidden_pairs_str}

## 查询配额
你有 {quota} 次查询机会。你需要通过查询非限制测试对来推断出生成兼容关系 E 的工艺规则，并最终预测所有限制测试对是否兼容。

## 你可以进行的操作

1. **查询边存在性**：询问某个非限制测试的模块对 {{u, v}} 是否存在装配兼容 E。
   - 要求：u 不等于 v，{{u, v}} 不在限制测试集合 F 中，且此前未测试过该组合。
   - 我会回答"有"或"没有"。

2. **查询剩余配额**：询问还剩多少次查询机会。
   - 我会回答一个非负整数。

3. **最终提交**：当你认为已掌握规律时，对所有限制测试对进行预测。
   - 你需要对每个限制测试对给出"有"或"没有"的判断。

## 查询与提交格式（必须严格遵守）

每次操作只能包含一个标签，使用以下 XML 格式：

- 查询边存在性（例如查询模块 2 和 5）：
<query_edge>2,5</query_edge>

- 查询剩余配额：
<query_budget></query_budget>

- 最终提交答案（对所有限制测试对进行预测）：
<answer>{{0,3}}=有, {{1,4}}=没有, {{2,5}}=有</answer>

注意：
1. 答案中必须包含所有限制测试对的预测，格式为"{{u,v}}=有"或"{{u,v}}=没有"，用逗号分隔。
2. 模块对顺序不限（{{2,5}} 和 {{5,2}} 等价）。
3. 不得查询限制测试对或重复测试同一对。
4. 不得超出查询配额。
5. 请尽可能少地使用查询次数，通过归纳推理找出规则。

违反任何约束或预测错误将导致系统调试失败。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
As a smart manufacturing systems engineer, you need to test the assembly compatibility and interchangeability among different modules on a new production line.

Let's play a "Hidden Assembly Compatibility Inference" game. Here are the rules:

The production line designates a set of processing module labels V = {{0, 1, ..., {n_minus_1}}}, containing {n} modules in total.

On this set, there exists an unknown assembly compatibility relation E. This compatibility relation satisfies the following properties:
1. Symmetry: If module pair {{u, v}} is compatible for assembly E, then {{v, u}} is also compatible.
2. No self-loops: No module is tested for compatibility with itself, i.e., {{u, u}} does not exist.
3. Non-trivial: There exist both compatible module pairs and incompatible pairs.

This compatibility is determined by a deterministic process rule that depends only on the module labels, but the rule is unknown to you.

## Forbidden Set
A specific set of module pairs is designated as "restricted test pairs" F. You cannot directly query whether these pairs are compatible. The restricted test set is:
{forbidden_pairs_str}

## Query Quota
You have {quota} query opportunities. You need to infer the process rule generating compatibility E by querying non-restricted pairs, and ultimately predict whether all restricted test pairs are compatible.

## Available Operations

1. **Query Edge Existence**: Ask whether a non-restricted module pair {{u, v}} is compatible E.
   - Requirements: u is not equal to v, {{u, v}} is not in the restricted test set F, and the pair has not been tested before.
   - I will answer "Yes" or "No".

2. **Query Remaining Quota**: Ask how many query opportunities remain.
   - I will answer with a non-negative integer.

3. **Final Submission**: When you believe you have grasped the pattern, predict all restricted test pairs.
   - You need to give a "Yes" or "No" judgment for each restricted pair.

## Query and Submission Format (must strictly follow)

Each operation can only contain one tag, using the following XML format:

- Query edge existence (e.g., query modules 2 and 5):
<query_edge>2,5</query_edge>

- Query remaining quota:
<query_budget></query_budget>

- Final answer submission (predict all restricted pairs):
<answer>{{0,3}}=Yes, {{1,4}}=No, {{2,5}}=Yes</answer>

Notes:
1. The answer must include predictions for all restricted test pairs, formatted as "{{u,v}}=Yes" or "{{u,v}}=No", separated by commas.
2. Module pair order does not matter ({{2,5}} and {{5,2}} are equivalent).
3. Do not query restricted test pairs or repeatedly query the same pair.
4. Do not exceed the query quota.
5. Use as few queries as possible and find the rule through inductive reasoning.

Violating any constraint or making incorrect predictions will result in system debugging failure.
"""

    contextualized_rule_zh_5 = """\
作为高级法务顾问，你需要分析一部新颁布法规中各条款之间潜在的竞合关系。

我们来玩一个"隐藏法律竞合推理"游戏，规则如下：

法典设定了一个法律条款编号集合 V = {{0, 1, ..., {n_minus_1}}}，共 {n} 项条款。

在这个集合上，存在一个未知的条款竞合关系 E。这个竞合关系满足以下性质：
1. 对称性：如果条款对 {{u, v}} 存在竞合关系 E，那么 {{v, u}} 也同样存在竞合。
2. 无自环：任何条款不与自己进行竞合判定，即 {{u, u}} 不存在。
3. 非平凡：既存在产生竞合的条款对，也存在不竞合的条款对。

这个竞合关系由一个仅依赖于条款编号的确定性法理规则决定，但该规则对你是未知的。

## 禁问集合
有一组特定的条款对被设置为"未公开裁决条款对" F，你不能直接查询这些对是否存在竞合。未公开裁决集合为：
{forbidden_pairs_str}

## 查询配额
你有 {quota} 次查询机会。你需要通过查询非未公开的裁决对来推断出生成竞合关系 E 的法理规则，并最终预测所有未公开裁决条款对是否存在竞合。

## 你可以进行的操作

1. **查询边存在性**：询问某个非未公开裁决的条款对 {{u, v}} 是否存在竞合关系 E。
   - 要求：u 不等于 v，{{u, v}} 不在未公开裁决集合 F 中，且此前未查询过该条款对。
   - 我会回答"有"或"没有"。

2. **查询剩余配额**：询问还剩多少次查询机会。
   - 我会回答一个非负整数。

3. **最终提交**：当你认为已掌握法理规律时，对所有未公开裁决条款对进行预测。
   - 你需要对每个未公开对给出"有"或"没有"的判断。

## 查询与提交格式（必须严格遵守）

每次操作只能包含一个标签，使用以下 XML 格式：

- 查询边存在性（例如查询条款 2 和 5）：
<query_edge>2,5</query_edge>

- 查询剩余配额：
<query_budget></query_budget>

- 最终提交答案（对所有未公开裁决条款对进行预测）：
<answer>{{0,3}}=有, {{1,4}}=没有, {{2,5}}=有</answer>

注意：
1. 答案中必须包含所有未公开裁决对的预测，格式为"{{u,v}}=有"或"{{u,v}}=没有"，用逗号分隔。
2. 条款对顺序不限（{{2,5}} 和 {{5,2}} 等价）。
3. 不得查询未公开裁决对或重复查询同一对。
4. 不得超出查询配额。
5. 请尽可能少地使用查询次数，通过归纳推理找出法理规则。

违反任何约束或预测错误将导致法理分析失败。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
As a senior legal counsel, you need to analyze the potential concurrence relationships between various articles in a newly enacted regulation.

Let's play a "Hidden Legal Concurrence Inference" game. Here are the rules:

The legal code defines a set of article labels V = {{0, 1, ..., {n_minus_1}}}, containing {n} articles in total.

On this set, there exists an unknown article concurrence relation E. This concurrence relation satisfies the following properties:
1. Symmetry: If article pair {{u, v}} has a concurrence relationship E, then {{v, u}} also has it.
2. No self-loops: No article is evaluated for concurrence with itself, i.e., {{u, u}} does not exist.
3. Non-trivial: There exist both article pairs that concur and pairs that do not.

This concurrence relation is determined by a deterministic jurisprudential rule that depends only on the article labels, but the rule is unknown to you.

## Forbidden Set
A specific set of article pairs is designated as "undisclosed ruling pairs" F. You cannot directly query whether these pairs have concurrence. The undisclosed ruling set is:
{forbidden_pairs_str}

## Query Quota
You have {quota} query opportunities. You need to infer the jurisprudential rule generating concurrence E by querying non-undisclosed pairs, and ultimately predict whether all undisclosed ruling article pairs have concurrence.

## Available Operations

1. **Query Edge Existence**: Ask whether a non-undisclosed article pair {{u, v}} has concurrence relationship E.
   - Requirements: u is not equal to v, {{u, v}} is not in the undisclosed ruling set F, and the pair has not been queried before.
   - I will answer "Yes" or "No".

2. **Query Remaining Quota**: Ask how many query opportunities remain.
   - I will answer with a non-negative integer.

3. **Final Submission**: When you believe you have grasped the jurisprudential pattern, predict all undisclosed ruling article pairs.
   - You need to give a "Yes" or "No" judgment for each undisclosed pair.

## Query and Submission Format (must strictly follow)

Each operation can only contain one tag, using the following XML format:

- Query edge existence (e.g., query articles 2 and 5):
<query_edge>2,5</query_edge>

- Query remaining quota:
<query_budget></query_budget>

- Final answer submission (predict all undisclosed pairs):
<answer>{{0,3}}=Yes, {{1,4}}=No, {{2,5}}=Yes</answer>

Notes:
1. The answer must include predictions for all undisclosed pairs, formatted as "{{u,v}}=Yes" or "{{u,v}}=No", separated by commas.
2. Article pair order does not matter ({{2,5}} and {{5,2}} are equivalent).
3. Do not query undisclosed ruling pairs or repeatedly query the same pair.
4. Do not exceed the query quota.
5. Use as few queries as possible and find the rule through inductive reasoning.

Violating any constraint or making incorrect predictions will result in legal analysis failure.
"""

    tags = ["answer", "query_edge", "query_budget"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "rule_func": lambda u, v: (u + v) % 2 == 0,
                "forbidden_pairs": [{0, 3}, {1, 4}, {2, 5}],
                "quota": 8,
            },
            2: {
                "n": 8,
                "rule_func": lambda u, v: (u % 2) == (v % 2),
                "forbidden_pairs": [{0, 4}, {1, 5}, {2, 6}, {3, 7}],
                "quota": 10,
            },
            3: {
                "n": 10,
                "rule_func": lambda u, v: abs(u - v) <= 2,
                "forbidden_pairs": [{0, 5}, {1, 6}, {2, 7}, {3, 8}, {4, 9}],
                "quota": 12,
            },
            4: {
                "n": 12,
                "rule_func": lambda u, v: (u * v) % 3 == 0,
                "forbidden_pairs": [{0, 7}, {1, 8}, {2, 9}, {3, 10}, {4, 11}, {5, 6}],
                "quota": 15,
            },
            5: {
                "n": 15,
                "rule_func": lambda u, v: (u + v) % 4 < 2,
                "forbidden_pairs": [{0, 8}, {1, 9}, {2, 10}, {3, 11}, {4, 12}, {5, 13}, {6, 14}, {7, 8}],
                "quota": 18,
            },
        },
        "en": {
            1: {
                "n": 6,
                "rule_func": lambda u, v: (u + v) % 2 == 0,
                "forbidden_pairs": [{0, 3}, {1, 4}, {2, 5}],
                "quota": 8,
            },
            2: {
                "n": 8,
                "rule_func": lambda u, v: (u % 2) == (v % 2),
                "forbidden_pairs": [{0, 4}, {1, 5}, {2, 6}, {3, 7}],
                "quota": 10,
            },
            3: {
                "n": 10,
                "rule_func": lambda u, v: abs(u - v) <= 2,
                "forbidden_pairs": [{0, 5}, {1, 6}, {2, 7}, {3, 8}, {4, 9}],
                "quota": 12,
            },
            4: {
                "n": 12,
                "rule_func": lambda u, v: (u * v) % 3 == 0,
                "forbidden_pairs": [{0, 7}, {1, 8}, {2, 9}, {3, 10}, {4, 11}, {5, 6}],
                "quota": 15,
            },
            5: {
                "n": 15,
                "rule_func": lambda u, v: (u + v) % 4 < 2,
                "forbidden_pairs": [{0, 8}, {1, 9}, {2, 10}, {3, 11}, {4, 12}, {5, 13}, {6, 14}, {7, 8}],
                "quota": 18,
            },
        },
    }

    def __init__(self, config):
        self.queried_pairs = set()  # 已查询过的元素对
        self.remaining_quota = 0    # 剩余查询配额
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏配置和规则"""
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 基本配置
        self._game_info["n"] = cfg["n"]
        self._game_info["n_minus_1"] = cfg["n"] - 1
        self._game_info["quota"] = cfg["quota"]
        
        # 规则函数和禁问对
        self.rule_func = cfg["rule_func"]
        self.forbidden_pairs = cfg["forbidden_pairs"]
        self.remaining_quota = cfg["quota"]
        
        # 格式化禁问对字符串用于显示
        forbidden_str = ", ".join(["{" + f"{min(p)},{max(p)}" + "}" for p in self.forbidden_pairs])
        self._game_info["forbidden_pairs_str"] = forbidden_str
        
        # 构建完整的关系 E（用于验证答案）
        self.relation_E = set()
        for u in range(cfg["n"]):
            for v in range(u + 1, cfg["n"]):
                if self.rule_func(u, v):
                    self.relation_E.add(frozenset({u, v}))

    def _normalize_pair(self, u, v):
        """将元素对标准化为 frozenset"""
        return frozenset({u, v})

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        raw_ans = parsed_info["answer"]
        
        # 根据语言确定关键字
        if self.config.language == "zh":
            yes_keyword = "有"
            no_keyword = "没有"
        else:
            yes_keyword = "Yes"
            no_keyword = "No"
        
        # 解析答案：格式如 {0,3}=有, {1,4}=没有
        # 使用正则提取所有的 {u,v}=答案 格式
        pattern = r'\{(\d+),(\d+)\}\s*=\s*(' + yes_keyword + '|' + no_keyword + ')'
        matches = re.findall(pattern, raw_ans, re.IGNORECASE)
        
        if not matches:
            return False
        
        # 构建模型的预测字典
        model_predictions = {}
        for match in matches:
            u, v = int(match[0]), int(match[1])
            prediction = match[2]
            pair = self._normalize_pair(u, v)
            # 使用大小写不敏感比较
            model_predictions[pair] = (prediction.lower() == yes_keyword.lower())
        
        # 检查是否覆盖了所有禁问对
        forbidden_pairs_set = {self._normalize_pair(*p) for p in self.forbidden_pairs}
        if set(model_predictions.keys()) != forbidden_pairs_set:
            return False
        
        # 检查每个禁问对的预测是否正确
        for pair in forbidden_pairs_set:
            predicted = model_predictions[pair]
            actual = pair in self.relation_E
            if predicted != actual:
                return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "有", "没有"
            error_out_of_range = "错误：元素标号超出范围。"
            error_self_loop = "错误：不能查询元素与自身的关系。"
            error_forbidden = "错误：该元素对在禁问集合中，不能查询。"
            error_repeated = "错误：该元素对已经查询过。"
            error_quota_exceeded = "错误：查询配额已用尽。"
            error_invalid_format = "错误：查询格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_out_of_range = "Error: Element ID out of range."
            error_self_loop = "Error: Cannot query relation between an element and itself."
            error_forbidden = "Error: This pair is in the forbidden set and cannot be queried."
            error_repeated = "Error: This pair has already been queried."
            error_quota_exceeded = "Error: Query quota exhausted."
            error_invalid_format = "Error: Invalid query format."

        # 优先处理查询配额
        if "query_budget" in parsed_info:
            return str(self.remaining_quota)

        # 处理边查询
        elif "query_edge" in parsed_info:
            try:
                raw = parsed_info["query_edge"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                u, v = int(parts[0]), int(parts[1])
                
                # 验证元素范围
                if u < 0 or u >= self._game_info["n"] or v < 0 or v >= self._game_info["n"]:
                    return error_out_of_range
                
                # 验证不是自环
                if u == v:
                    return error_self_loop
                
                pair = self._normalize_pair(u, v)
                
                # 验证不在禁问集合
                if pair in {self._normalize_pair(*p) for p in self.forbidden_pairs}:
                    return error_forbidden
                
                # 验证未重复查询
                if pair in self.queried_pairs:
                    return error_repeated
                
                # 验证配额
                if self.remaining_quota <= 0:
                    return error_quota_exceeded
                
                # 执行查询
                self.queried_pairs.add(pair)
                self.remaining_quota -= 1
                
                # 返回结果
                in_relation = pair in self.relation_E
                return yes_res if in_relation else no_res
                
            except (ValueError, IndexError):
                return error_invalid_format

        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 查询内容字符串，与游戏中 parsed_info["query"] 的值格式一致
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        possible_queries = []
        n = self._game_info["n"]
        
        # 预处理禁问对集合，方便快速查找
        forbidden_set = {self._normalize_pair(*p) for p in self.forbidden_pairs}
        
        # 根据语言确定回答文本
        if self.config.language == "zh":
            yes_res, no_res = "有", "没有"
        else:
            yes_res, no_res = "Yes", "No"
            
        # 遍历所有可能的无向边 (u, v) 其中 u < v
        # 这涵盖了所有合法的、非自环的边查询
        for u in range(n):
            for v in range(u + 1, n):
                pair = self._normalize_pair(u, v)
                
                # 如果是禁问对，则跳过（因为规则禁止直接查询禁问对）
                if pair in forbidden_set:
                    continue
                
                # 获取正确答案（利用初始化时构建的 relation_E）
                # 这里不使用 produce_response，避免消耗配额或改变游戏状态
                is_connected = pair in self.relation_E
                ans = yes_res if is_connected else no_res
                
                possible_queries.append({
                    "query": f"<query_edge>{u},{v}</query_edge>",
                    "answer": ans
                })
                
        return possible_queries

    def _cf_make_wrong(self, correct: str) -> str:
        """根据正确答案生成错误答案"""
        # 纯整数字符串
        if correct.isdigit():
            return str(int(correct) + 1)
        
        # 中文是非
        if correct == "有":
            return "没有"
        if correct == "没有":
            return "有"
        
        # 英文Yes/No (忽略大小写)
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"

        # 其他情况
        return correct + "_WRONG"