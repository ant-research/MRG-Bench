from .base import Game
import re
from itertools import product
from math import gcd


class BooleanConceptIdentificationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"布尔概念识别"的推理游戏，规则如下：

游戏设定了三个二值特征 x1, x2, x3，每个特征的取值为 0 或 1。因此共有 8 种可能的赋值组合：
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

我已秘密选择了一个目标子集 G，它是这 8 种赋值的某个子集。你的目标是通过提问来确定这个隐藏的目标子集 G。

## 查询方式

你可以向我提交布尔公式进行查询。布尔公式只能使用以下元素：
- 变量：x1, x2, x3
- 逻辑运算符：AND（与）、OR（或）、NOT（非）
- 常量：TRUE、FALSE
- 括号用于控制优先级

公式示例：
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## 反馈规则

当你提交一个布尔公式 φ 时：
1. 我会计算出满足该公式的赋值数量 K（即使公式为真的赋值个数）
2. 如果 K = 0（公式恒假，没有赋值满足），我会提示"查询为空集，请重新提问"，该次查询不计入次数
3. 如果 K 大于 0，我会计算满足公式且属于目标集合 G 的赋值数量 H，然后返回比例 H/K

例如：
- 如果你查询 "x1"，有 4 个赋值满足（K=4），其中 3 个属于 G（H=3），则返回 "3/4"
- 如果返回 "1/1"，说明所有满足你查询公式的赋值都在 G 中

## 目标

你需要尽可能少的查询次数来达成以下任一目标：

1. **精确识别**：明确给出 8 个赋值中哪些属于 G（可以用真值表形式）
2. **等价公式**：给出一个布尔公式，它在所有 8 个赋值上的真值与 G 的特征函数完全相同
3. **确定性子集**：找到一个查询公式，使得反馈必然为 1/1，并基于之前的反馈说明理由

## 查询与提交答案的格式（必须严格遵守）

查询布尔公式时，使用以下格式：
<query>x1 AND x2</query>

提交最终答案时，使用以下格式之一：

方式1 - 真值表（按字典序列出8个赋值的标签，1表示属于G，0表示不属于G）：
<answer>00010111</answer>

方式2 - 等价布尔公式：
<answer>x1 OR (x2 AND NOT x3)</answer>

注意：
- 每次只能提交一个标签
- 查询的公式必须是合法的布尔表达式
- 最终答案要么是8位二进制串（真值表），要么是布尔公式
"""

    game_rule_en = """\
Let's play a "Boolean Concept Identification" deduction game. Here are the rules:

The game involves three binary features x1, x2, x3, each taking value 0 or 1. There are 8 possible assignment combinations:
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

I have secretly selected a target subset G, which is a subset of these 8 assignments. Your goal is to identify this hidden target subset G through queries.

## Query Method

You can submit Boolean formulas as queries. Boolean formulas can only use:
- Variables: x1, x2, x3
- Logical operators: AND, OR, NOT
- Constants: TRUE, FALSE
- Parentheses for precedence

Formula examples:
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## Feedback Rules

When you submit a Boolean formula φ:
1. I calculate the number K of assignments satisfying the formula (assignments making it true)
2. If K = 0 (formula always false, no assignments satisfy it), I respond "Query is empty set, please re-query", and this query does not count
3. If K > 0, I calculate H, the number of assignments satisfying the formula AND belonging to target set G, then return ratio H/K

Examples:
- If you query "x1", 4 assignments satisfy it (K=4), 3 of them belong to G (H=3), return "3/4"
- If return is "1/1", all assignments satisfying your query are in G

## Objective

Use as few queries as possible to achieve any one of:

1. **Precise Identification**: Explicitly state which of the 8 assignments belong to G (truth table form)
2. **Equivalent Formula**: Provide a Boolean formula whose truth values on all 8 assignments exactly match G's characteristic function
3. **Deterministic Subset**: Find a query formula that necessarily returns 1/1, with justification based on previous feedback

## Query and Answer Format (strictly required)

To query a Boolean formula, use:
<query>x1 AND x2</query>

To submit final answer, use one of:

Method 1 - Truth table (list labels for 8 assignments in lexicographic order, 1 means belongs to G, 0 means not):
<answer>00010111</answer>

Method 2 - Equivalent Boolean formula:
<answer>x1 OR (x2 AND NOT x3)</answer>

Note:
- Only one tag per submission
- Query formulas must be valid Boolean expressions
- Final answer must be either an 8-bit binary string (truth table) or a Boolean formula
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
我们现在来进行一项"城市交通拥堵归因分析"的推理排查，规则如下：

交通管理系统监测了三个关键的二值特征 x1, x2, x3（例如：是否高峰期、是否主干道、是否恶劣天气），每个特征的取值为 0 或 1。因此共有 8 种可能的交通状况组合：
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

系统已秘密记录了一个必然导致严重拥堵的目标子集 G，它是这 8 种组合的某个子集。你的目标是通过系统查询来确定这个隐藏的拥堵条件子集 G。

## 查询方式

你可以向我提交布尔公式进行数据查询。布尔公式只能使用以下元素：
- 变量：x1, x2, x3
- 逻辑运算符：AND（与）、OR（或）、NOT（非）
- 常量：TRUE、FALSE
- 括号用于控制优先级

公式示例：
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## 反馈规则

当你提交一个布尔公式 φ 时：
1. 我会计算出满足该公式的交通状况组合数量 K（即符合查询条件的组合个数）
2. 如果 K = 0（公式恒假，没有组合满足），我会提示"查询为空集，请重新提问"，该次查询不计入次数
3. 如果 K 大于 0，我会计算满足公式且属于严重拥堵集合 G 的组合数量 H，然后返回比例 H/K

例如：
- 如果你查询 "x1"，有 4 个组合满足（K=4），其中 3 个属于 G（H=3），则返回 "3/4"
- 如果返回 "1/1"，说明所有满足你查询条件的组合都在 G 中

## 目标

你需要尽可能少的查询次数来达成以下任一目标：

1. **精确识别**：明确给出 8 个交通状况组合中哪些属于 G（可以用真值表形式）
2. **等价公式**：给出一个布尔公式，它在所有 8 个组合上的真值与 G 的特征函数完全相同
3. **确定性子集**：找到一个查询公式，使得反馈必然为 1/1，并基于之前的反馈说明理由

## 查询与提交答案的格式（必须严格遵守）

查询布尔公式时，使用以下格式：
<query>x1 AND x2</query>

提交最终答案时，使用以下格式之一：

方式1 - 真值表（按字典序列出8个组合的标签，1表示属于严重拥堵集合G，0表示不属于）：
<answer>00010111</answer>

方式2 - 等价布尔公式：
<answer>x1 OR (x2 AND NOT x3)</answer>

注意：
- 每次只能提交一个标签
- 查询的公式必须是合法的布尔表达式
- 最终答案要么是8位二进制串（真值表），要么是布尔公式
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a deduction investigation for "Urban Traffic Congestion Attribution Analysis". Here are the rules:

The traffic management system monitors three key binary features x1, x2, x3 (e.g., peak hours, main roads, severe weather), each taking value 0 or 1. There are 8 possible traffic condition combinations:
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

The system has secretly recorded a target subset G that inevitably leads to severe congestion, which is a subset of these 8 combinations. Your goal is to identify this hidden congestion condition subset G through system queries.

## Query Method

You can submit Boolean formulas as data queries. Boolean formulas can only use:
- Variables: x1, x2, x3
- Logical operators: AND, OR, NOT
- Constants: TRUE, FALSE
- Parentheses for precedence

Formula examples:
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## Feedback Rules

When you submit a Boolean formula φ:
1. I calculate the number K of traffic condition combinations satisfying the formula
2. If K = 0 (formula always false, no combinations satisfy it), I respond "Query is empty set, please re-query", and this query does not count
3. If K > 0, I calculate H, the number of combinations satisfying the formula AND belonging to the severe congestion set G, then return ratio H/K

Examples:
- If you query "x1", 4 combinations satisfy it (K=4), 3 of them belong to G (H=3), return "3/4"
- If return is "1/1", all combinations satisfying your query are in G

## Objective

Use as few queries as possible to achieve any one of:

1. **Precise Identification**: Explicitly state which of the 8 traffic condition combinations belong to G (truth table form)
2. **Equivalent Formula**: Provide a Boolean formula whose truth values on all 8 combinations exactly match G's characteristic function
3. **Deterministic Subset**: Find a query formula that necessarily returns 1/1, with justification based on previous feedback

## Query and Answer Format (strictly required)

To query a Boolean formula, use:
<query>x1 AND x2</query>

To submit final answer, use one of:

Method 1 - Truth table (list labels for 8 combinations in lexicographic order, 1 means belongs to G, 0 means not):
<answer>00010111</answer>

Method 2 - Equivalent Boolean formula:
<answer>x1 OR (x2 AND NOT x3)</answer>

Note:
- Only one tag per submission
- Query formulas must be valid Boolean expressions
- Final answer must be either an 8-bit binary string (truth table) or a Boolean formula
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
我们现在来进行一项"罕见病易感人群排查"的推理分析，规则如下：

医疗数据库记录了三个关键的二值特征 x1, x2, x3（例如：特定基因突变、基础病史、不良生活习惯），每个特征的取值为 0 或 1。因此共有 8 种可能的患者亚群组合：
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

研究团队已秘密锁定了一个极易感染该疾病的目标亚群集合 G，它是这 8 种组合的某个子集。你的目标是通过数据库查询来确定这个隐藏的易感人群子集 G。

## 查询方式

你可以向我提交布尔公式进行数据查询。布尔公式只能使用以下元素：
- 变量：x1, x2, x3
- 逻辑运算符：AND（与）、OR（或）、NOT（非）
- 常量：TRUE、FALSE
- 括号用于控制优先级

公式示例：
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## 反馈规则

当你提交一个布尔公式 φ 时：
1. 我会计算出满足该公式的患者亚群组合数量 K（即符合查询条件的组合个数）
2. 如果 K = 0（公式恒假，没有组合满足），我会提示"查询为空集，请重新提问"，该次查询不计入次数
3. 如果 K 大于 0，我会计算满足公式且属于易感人群集合 G 的组合数量 H，然后返回比例 H/K

例如：
- 如果你查询 "x1"，有 4 个组合满足（K=4），其中 3 个属于 G（H=3），则返回 "3/4"
- 如果返回 "1/1"，说明所有满足你查询条件的组合都在 G 中

## 目标

你需要尽可能少的查询次数来达成以下任一目标：

1. **精确识别**：明确给出 8 个患者亚群组合中哪些属于 G（可以用真值表形式）
2. **等价公式**：给出一个布尔公式，它在所有 8 个组合上的真值与 G 的特征函数完全相同
3. **确定性子集**：找到一个查询公式，使得反馈必然为 1/1，并基于之前的反馈说明理由

## 查询与提交答案的格式（必须严格遵守）

查询布尔公式时，使用以下格式：
<query>x1 AND x2</query>

提交最终答案时，使用以下格式之一：

方式1 - 真值表（按字典序列出8个组合的标签，1表示属于易感人群集合G，0表示不属于）：
<answer>00010111</answer>

方式2 - 等价布尔公式：
<answer>x1 OR (x2 AND NOT x3)</answer>

注意：
- 每次只能提交一个标签
- 查询的公式必须是合法的布尔表达式
- 最终答案要么是8位二进制串（真值表），要么是布尔公式
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a deduction analysis for "Rare Disease Susceptibility Screening". Here are the rules:

The medical database records three key binary features x1, x2, x3 (e.g., specific gene mutations, underlying medical history, poor lifestyle habits), each taking value 0 or 1. There are 8 possible patient subpopulation combinations:
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

The research team has secretly locked onto a target subset G that is highly susceptible to this disease, which is a subset of these 8 combinations. Your goal is to identify this hidden susceptible subpopulation subset G through database queries.

## Query Method

You can submit Boolean formulas as data queries. Boolean formulas can only use:
- Variables: x1, x2, x3
- Logical operators: AND, OR, NOT
- Constants: TRUE, FALSE
- Parentheses for precedence

Formula examples:
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## Feedback Rules

When you submit a Boolean formula φ:
1. I calculate the number K of patient subpopulation combinations satisfying the formula
2. If K = 0 (formula always false, no combinations satisfy it), I respond "Query is empty set, please re-query", and this query does not count
3. If K > 0, I calculate H, the number of combinations satisfying the formula AND belonging to the susceptible set G, then return ratio H/K

Examples:
- If you query "x1", 4 combinations satisfy it (K=4), 3 of them belong to G (H=3), return "3/4"
- If return is "1/1", all combinations satisfying your query are in G

## Objective

Use as few queries as possible to achieve any one of:

1. **Precise Identification**: Explicitly state which of the 8 patient subpopulation combinations belong to G (truth table form)
2. **Equivalent Formula**: Provide a Boolean formula whose truth values on all 8 combinations exactly match G's characteristic function
3. **Deterministic Subset**: Find a query formula that necessarily returns 1/1, with justification based on previous feedback

## Query and Answer Format (strictly required)

To query a Boolean formula, use:
<query>x1 AND x2</query>

To submit final answer, use one of:

Method 1 - Truth table (list labels for 8 combinations in lexicographic order, 1 means belongs to G, 0 means not):
<answer>00010111</answer>

Method 2 - Equivalent Boolean formula:
<answer>x1 OR (x2 AND NOT x3)</answer>

Note:
- Only one tag per submission
- Query formulas must be valid Boolean expressions
- Final answer must be either an 8-bit binary string (truth table) or a Boolean formula
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
我们现在来进行一项"优等生奖学金资格分析"的推理游戏，规则如下：

教务系统记录了三个关键的二值特征 x1, x2, x3（例如：参与课外辅导、作业完成率高、家长陪伴时间长），每个特征的取值为 0 或 1。因此共有 8 种可能的学生画像组合：
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

评审委员会已秘密确定了一个符合奖学金发放资格的目标子集 G，它是这 8 种组合的某个子集。你的目标是通过系统查询来确定这个隐藏的奖学金资格子集 G。

## 查询方式

你可以向我提交布尔公式进行数据查询。布尔公式只能使用以下元素：
- 变量：x1, x2, x3
- 逻辑运算符：AND（与）、OR（或）、NOT（非）
- 常量：TRUE、FALSE
- 括号用于控制优先级

公式示例：
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## 反路线反馈规则

当你提交一个布尔公式 φ 时：
1. 我会计算出满足该公式的学生画像组合数量 K（即符合查询条件的组合个数）
2. 如果 K = 0（公式恒假，没有组合满足），我会提示"查询为空集，请重新提问"，该次查询不计入次数
3. 如果 K 大于 0，我会计算满足公式且属于奖学金资格集合 G 的组合数量 H，然后返回比例 H/K

例如：
- 如果你查询 "x1"，有 4 个组合满足（K=4），其中 3 个属于 G（H=3），则返回 "3/4"
- 如果返回 "1/1"，说明所有满足你查询条件的组合都在 G 中

## 目标

你需要尽可能少的查询次数来达成以下任一目标：

1. **精确识别**：明确给出 8 个学生画像组合中哪些属于 G（可以用真值表形式）
2. **等价公式**：给出一个布尔公式，它在所有 8 个组合上的真值与 G 的特征函数完全相同
3. **确定性子集**：找到一个查询公式，使得反馈必然为 1/1，并基于之前的反馈说明理由

## 查询与提交答案的格式（必须严格遵守）

查询布尔公式时，使用以下格式：
<query>x1 AND x2</query>

提交最终答案时，使用以下格式之一：

方式1 - 真值表（按字典序列出8个组合的标签，1表示属于奖学金资格集合G，0表示不属于）：
<answer>00010111</answer>

方式2 - 等价布尔公式：
<answer>x1 OR (x2 AND NOT x3)</answer>

注意：
- 每次只能提交一个标签
- 查询的公式必须是合法的布尔表达式
- 最终答案要么是8位二进制串（真值表），要么是布尔公式
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a deduction game for "Top Student Scholarship Eligibility Analysis". Here are the rules:

The educational administration system records three key binary features x1, x2, x3 (e.g., active participation in extracurriculars, high attendance rate, excellent competition results), each taking value 0 or 1. There are 8 possible student profile combinations:
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

The review committee has secretly determined a target subset G eligible for the scholarship, which is a subset of these 8 combinations. Your goal is to identify this hidden eligibility subset G through system queries.

## Query Method

You can submit Boolean formulas as data queries. Boolean formulas can only use:
- Variables: x1, x2, x3
- Logical operators: AND, OR, NOT
- Constants: TRUE, FALSE
- Parentheses for precedence

Formula examples:
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## Feedback Rules

When you submit a Boolean formula φ:
1. I calculate the number K of student profile combinations satisfying the formula
2. If K = 0 (formula always false, no combinations satisfy it), I respond "Query is empty set, please re-query", and this query does not count
3. If K > 0, I calculate H, the number of combinations satisfying the formula AND belonging to the scholarship eligibility set G, then return ratio H/K

Examples:
- If you query "x1", 4 combinations satisfy it (K=4), 3 of them belong to G (H=3), return "3/4"
- If return is "1/1", all combinations satisfying your query are in G

## Objective

Use as few queries as possible to achieve any one of:

1. **Precise Identification**: Explicitly state which of the 8 student profile combinations belong to G (truth table form)
2. **Equivalent Formula**: Provide a Boolean formula whose truth values on all 8 combinations exactly match G's characteristic function
3. **Deterministic Subset**: Find a query formula that necessarily returns 1/1, with justification based on previous feedback

## Query and Answer Format (strictly required)

To query a Boolean formula, use:
<query>x1 AND x2</query>

To submit final answer, use one of:

Method 1 - Truth table (list labels for 8 combinations in lexicographic order, 1 means belongs to G, 0 means not):
<answer>00010111</answer>

Method 2 - Equivalent Boolean formula:
<answer>x1 OR (x2 AND NOT x3)</answer>

Note:
- Only one tag per submission
- Query formulas must be valid Boolean expressions
- Final answer must be either an 8-bit binary string (truth table) or a Boolean formula
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
我们现在来进行一项"生产线缺陷归因分析"的推理排查，规则如下：

工业物联网监测了三个关键的二值特征 x1, x2, x3（例如：高温环境、高转速、使用新材料），每个特征的取值为 0 或 1。因此共有 8 种可能的生产参数组合：
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

质检系统已秘密记录了一个必然导致零件报废（缺陷）的目标子集 G，它是这 8 种组合的某个子集。你的目标是通过系统查询来确定这个隐藏的缺陷参数子集 G。

## 查询方式

你可以向我提交布尔公式进行数据查询。布尔公式只能使用以下元素：
- 变量：x1, x2, x3
- 逻辑运算符：AND（与）、OR（或）、NOT（非）
- 常量：TRUE、FALSE
- 括号用于控制优先级

公式示例：
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## 反馈规则

当你提交一个布尔公式 φ 时：
1. 我会计算出满足该公式的生产参数组合数量 K（即符合查询条件的组合个数）
2. 如果 K = 0（公式恒假，没有组合满足），我会提示"查询为空集，请重新提问"，该次查询不计入次数
3. 如果 K 大于 0，我会计算满足公式且属于零件报废集合 G 的组合数量 H，然后返回比例 H/K

例如：
- 如果你查询 "x1"，有 4 个组合满足（K=4），其中 3 个属于 G（H=3），则返回 "3/4"
- 如果返回 "1/1"，说明所有满足你查询条件的组合都在 G 中

## 目标

你需要尽可能少的查询次数来达成以下任一目标：

1. **精确识别**：明确给出 8 个生产参数组合中哪些属于 G（可以用真值表形式）
2. **等价公式**：给出一个布尔公式，它在所有 8 个组合上的真值与 G 的特征函数完全相同
3. **确定性子集**：找到一个查询公式，使得反馈必然为 1/1，并基于之前的反馈说明理由

## 查询与提交答案的格式（必须严格遵守）

查询布尔公式时，使用以下格式：
<query>x1 AND x2</query>

提交最终答案时，使用以下格式之一：

方式1 - 真值表（按字典序列出8个组合的标签，1表示属于零件报废集合G，0表示不属于）：
<answer>00010111</answer>

方式2 - 等价布尔公式：
<answer>x1 OR (x2 AND NOT x3)</answer>

注意：
- 每次只能提交一个标签
- 查询的公式必须是合法的布尔表达式
- 最终答案要么是8位二进制串（真值表），要么是布尔公式
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Let's conduct a deduction investigation for "Production Line Defect Attribution Analysis". Here are the rules:

The Industrial IoT monitors three key binary features x1, x2, x3 (e.g., high-temperature environment, high rotation speed, specific batch materials), each taking value 0 or 1. There are 8 possible production parameter combinations:
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

The quality inspection system has secretly recorded a target subset G that inevitably leads to part scrappage (defects), which is a subset of these 8 combinations. Your goal is to identify this hidden defect parameter subset G through system queries.

## Query Method

You can submit Boolean formulas as data queries. Boolean formulas can only use:
- Variables: x1, x2, x3
- Logical operators: AND, OR, NOT
- Constants: TRUE, FALSE
- Parentheses for precedence

Formula examples:
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## Feedback Rules

When you submit a Boolean formula φ:
1. I calculate the number K of production parameter combinations satisfying the formula
2. If K = 0 (formula always false, no combinations satisfy it), I respond "Query is empty set, please re-query", and this query does not count
3. If K > 0, I calculate H, the number of combinations satisfying the formula AND belonging to the part scrappage set G, then return ratio H/K

Examples:
- If you query "x1", 4 combinations satisfy it (K=4), 3 of them belong to G (H=3), return "3/4"
- If return is "1/1", all combinations satisfying your query are in G

## Objective

Use as few queries as possible to achieve any one of:

1. **Precise Identification**: Explicitly state which of the 8 production parameter combinations belong to G (truth table form)
2. **Equivalent Formula**: Provide a Boolean formula whose truth values on all 8 combinations exactly match G's characteristic function
3. **Deterministic Subset**: Find a query formula that necessarily returns 1/1, with justification based on previous feedback

## Query and Answer Format (strictly required)

To query a Boolean formula, use:
<query>x1 AND x2</query>

To submit final answer, use one of:

Method 1 - Truth table (list labels for 8 combinations in lexicographic order, 1 means belongs to G, 0 means not):
<answer>00010111</answer>

Method 2 - Equivalent Boolean formula:
<answer>x1 OR (x2 AND NOT x3)</answer>

Note:
- Only one tag per submission
- Query formulas must be valid Boolean expressions
- Final answer must be either an 8-bit binary string (truth table) or a Boolean formula
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
我们现在来进行一项"刑罚加重条件判定"的推理排查，规则如下：

司法案卷记录了三个关键的二值特征 x1, x2, x3（例如：存在故意、造成重大损失、有自首情节），每个特征的取值为 0 或 1。因此共有 8 种可能的案件特征组合：
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

裁判标准中已秘密规定了一个符合特定刑罚加重条件的目标子集 G，它是这 8 种组合的某个子集。你的目标是通过法理查询来确定这个隐藏的加重条件子集 G。

## 查询方式

你可以向我提交布尔公式进行数据查询。布尔公式只能使用以下元素：
- 变量：x1, x2, x3
- 逻辑运算符：AND（与）、OR（或）、NOT（非）
- 常量：TRUE、FALSE
- 括号用于控制优先级

公式示例：
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## 反馈规则

当你提交一个布尔公式 φ 时：
1. 我会计算出满足该公式的案件特征组合数量 K（即符合查询条件的组合个数）
2. 如果 K = 0（公式恒假，没有组合满足），我会提示"查询为空集，请重新提问"，该次查询不计入次数
3. 如果 K 大于 0，我会计算满足公式且属于加重条件集合 G 的组合数量 H，然后返回比例 H/K

例如：
- 如果你查询 "x1"，有 4 个组合满足（K=4），其中 3 个属于 G（H=3），则返回 "3/4"
- 如果返回 "1/1"，说明所有满足你查询条件的组合都在 G 中

## 目标

你需要尽可能少的查询次数来达成以下任一目标：

1. **精确识别**：明确给出 8 个案件特征组合中哪些属于 G（可以用真值表形式）
2. **等价公式**：给出一个布尔公式，它在所有 8 个组合上的真值与 G 的特征函数完全相同
3. **确定性子集**：找到一个查询公式，使得反馈必然为 1/1，并基于之前的反馈说明理由

## 查询与提交答案的格式（必须严格遵守）

查询布尔公式时，使用以下格式：
<query>x1 AND x2</query>

提交最终答案时，使用以下格式之一：

方式1 - 真值表（按字典序列出8个组合的标签，1表示属于加重条件集合G，0表示不属于）：
<answer>00010111</answer>

方式2 - 等价布尔公式：
<answer>x1 OR (x2 AND NOT x3)</answer>

注意：
- 每次只能提交一个标签
- 查询的公式必须是合法的布尔表达式
- 最终答案要么是8位二进制串（真值表），要么是布尔公式
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a deduction investigation for "Penalty Aggravation Condition Determination". Here are the rules:

The judicial records contain three key binary features x1, x2, x3 (e.g., subjective intent, severe damages caused, absence of voluntary surrender), each taking value 0 or 1. There are 8 possible case feature combinations:
(0,0,0), (0,0,1), (0,1,0), (0,1,1), (1,0,0), (1,0,1), (1,1,0), (1,1,1)

The adjudication standards have secretly stipulated a target subset G that meets specific penalty aggravation conditions, which is a subset of these 8 combinations. Your goal is to identify this hidden aggravation condition subset G through jurisprudential queries.

## Query Method

You can submit Boolean formulas as data queries. Boolean formulas can only use:
- Variables: x1, x2, x3
- Logical operators: AND, OR, NOT
- Constants: TRUE, FALSE
- Parentheses for precedence

Formula examples:
- x1 AND x2
- (x1 OR x2) AND NOT x3
- x1
- NOT x1 OR (x2 AND x3)

## Feedback Rules

When you submit a Boolean formula φ:
1. I calculate the number K of case feature combinations satisfying the formula
2. If K = 0 (formula always false, no combinations satisfy it), I respond "Query is empty set, please re-query", and this query does not count
3. If K > 0, I calculate H, the number of combinations satisfying the formula AND belonging to the aggravation condition set G, then return ratio H/K

Examples:
- If you query "x1", 4 combinations satisfy it (K=4), 3 of them belong to G (H=3), return "3/4"
- If return is "1/1", all combinations satisfying your query are in G

## Objective

Use as few queries as possible to achieve any one of:

1. **Precise Identification**: Explicitly state which of the 8 case feature combinations belong to G (truth table form)
2. **Equivalent Formula**: Provide a Boolean formula whose truth values on all 8 combinations exactly match G's characteristic function
3. **Deterministic Subset**: Find a query formula that necessarily returns 1/1, with justification based on previous feedback

## Query and Answer Format (strictly required)

To query a Boolean formula, use:
<query>x1 AND x2</query>

To submit final answer, use one of:

Method 1 - Truth table (list labels for 8 combinations in lexicographic order, 1 means belongs to G, 0 means not):
<answer>00010111</answer>

Method 2 - Equivalent Boolean formula:
<answer>x1 OR (x2 AND NOT x3)</answer>

Note:
- Only one tag per submission
- Query formulas must be valid Boolean expressions
- Final answer must be either an 8-bit binary string (truth table) or a Boolean formula
"""

    tags = ["answer", "query"]
    
    reasoning_type = "归纳推理"
    data_structure = "集合"

    # 五种难度配置
    # 难度1（简单）：目标是单个变量 x1
    # 难度2（中等偏下）：目标是简单合取 x1 AND x2
    # 难度3（中等偏上）：目标是简单析取 x1 OR x3
    # 难度4（较难）：目标是带否定的合取 x1 AND NOT x2
    # 难度5（难）：目标是复杂表达式 (x1 AND x2) OR (NOT x1 AND x3)

    DIFFICULTY_CONFIG = {
        1: {
            "target_formula": "x1",
            "target_set": {"100", "101", "110", "111"},  # x1=1的所有情况
        },
        2: {
            "target_formula": "x1 AND x2",
            "target_set": {"110", "111"},  # x1=1 且 x2=1
        },
        3: {
            "target_formula": "x1 OR x3",
            "target_set": {"001", "011", "100", "101", "110", "111"},  # x1=1 或 x3=1
        },
        4: {
            "target_formula": "x1 AND NOT x2",
            "target_set": {"100", "101"},  # x1=1 且 x2=0
        },
        5: {
            "target_formula": "(x1 AND x2) OR (NOT x1 AND x3)",
            "target_set": {"001", "011", "110", "111"},  # (x1=1且x2=1) 或 (x1=0且x3=1)
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)

        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[diff]
        self.target_formula = cfg["target_formula"]
        # target_set 中每个字符串表示 x1x2x3 的取值
        self.target_set = cfg["target_set"].copy()
        
        # 为规则描述准备信息（这里不需要插入参数）
        self._game_info = {}

    def _parse_formula(self, formula_str):
        """
        解析布尔公式并评估在所有8个赋值上的真值
        返回满足公式的赋值集合（用字符串表示，如"101"表示x1=1,x2=0,x3=1）
        """
        formula_str = formula_str.strip()
        
        # 标准化：将常见写法统一
        formula_str = re.sub(r'\bAND\b', '&', formula_str, flags=re.IGNORECASE)
        formula_str = re.sub(r'\bOR\b', '|', formula_str, flags=re.IGNORECASE)
        formula_str = re.sub(r'\bNOT\b', '~', formula_str, flags=re.IGNORECASE)
        formula_str = re.sub(r'\bTRUE\b', 'True', formula_str, flags=re.IGNORECASE)
        formula_str = re.sub(r'\bFALSE\b', 'False', formula_str, flags=re.IGNORECASE)
        
        # 替换变量名为可求值的形式
        # 使用临时变量映射
        formula_str = re.sub(r'\bx1\b', '_x1', formula_str)
        formula_str = re.sub(r'\bx2\b', '_x2', formula_str)
        formula_str = re.sub(r'\bx3\b', '_x3', formula_str)
        
        # 替换逻辑运算符为Python运算符
        formula_str = formula_str.replace('&', ' and ')
        formula_str = formula_str.replace('|', ' or ')
        formula_str = formula_str.replace('~', ' not ')
        
        satisfying_set = set()
        
        # 遍历所有8个赋值
        for x1_val, x2_val, x3_val in product([0, 1], repeat=3):
            _x1, _x2, _x3 = x1_val, x2_val, x3_val
            try:
                # 安全地求值布尔表达式
                result = eval(formula_str, {"__builtins__": {}}, 
                            {"_x1": _x1, "_x2": _x2, "_x3": _x3, "True": True, "False": False})
                if result:
                    assignment = f"{x1_val}{x2_val}{x3_val}"
                    satisfying_set.add(assignment)
            except Exception as e:
                raise ValueError(f"Invalid formula syntax: {str(e)}")
        
        return satisfying_set

    def _normalize_formula_answer(self, formula_str):
        """
        将答案中的布尔公式转换为对应的真值表（8位二进制串）
        """
        try:
            satisfying_set = self._parse_formula(formula_str)
            # 生成8位真值表
            truth_table = ""
            for x1_val, x2_val, x3_val in product([0, 1], repeat=3):
                assignment = f"{x1_val}{x2_val}{x3_val}"
                truth_table += "1" if assignment in satisfying_set else "0"
            return truth_table
        except:
            return None

    def evaluate(self, parsed_info):
        """
        评估最终答案是否正确
        答案可以是：
        1. 8位二进制串（真值表）
        2. 等价的布尔公式
        """
        answer_str = parsed_info["answer"].strip()
        
        # 生成目标的真值表
        target_truth_table = ""
        for x1_val, x2_val, x3_val in product([0, 1], repeat=3):
            assignment = f"{x1_val}{x2_val}{x3_val}"
            target_truth_table += "1" if assignment in self.target_set else "0"
        
        # 情况1：答案是8位二进制串
        if re.match(r'^[01]{8}$', answer_str):
            return answer_str == target_truth_table
        
        # 情况2：答案是布尔公式
        else:
            normalized = self._normalize_formula_answer(answer_str)
            if normalized is None:
                return False
            return normalized == target_truth_table

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No query tag found.")
        
        query_formula = parsed_info["query"].strip()
        
        if not query_formula:
            if self.config.language == "zh":
                return "查询为空，请提供有效的布尔公式。"
            else:
                return "Query is empty, please provide a valid Boolean formula."
        
        # 解析查询公式，获取满足公式的赋值集合
        satisfying_set = self._parse_formula(query_formula)
        
        K = len(satisfying_set)
        
        # 如果查询为空集
        if K == 0:
            if self.config.language == "zh":
                return "查询为空集，请重新提问。（此次查询不计入次数）"
            else:
                return "Query is empty set, please re-query. (This query does not count)"
        
        # 计算交集
        H = len(satisfying_set & self.target_set)
        
        # 返回比例
        # 简化分数
        g = gcd(H, K)
        H_simplified = H // g
        K_simplified = K // g
        
        return f"{H_simplified}/{K_simplified}"

    def _cf_make_wrong(self, correct: str) -> str:
        """生成一个与正确答案不同的错误答案"""
        # 尝试匹配分数格式 H/K
        frac_match = re.match(r'^(\d+)/(\d+)$', correct.strip())
        if frac_match:
            H = int(frac_match.group(1))
            K = int(frac_match.group(2))
            # 生成一个不同的分子
            if H < K:
                wrong_H = H + 1
            else:
                wrong_H = H - 1 if H > 0 else 1
            g = gcd(wrong_H, K)
            return f"{wrong_H // g}/{K // g}"
        
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        
        lower_correct = correct.lower()
        if "yes" in lower_correct:
            return re.sub(r'(?i)yes', 'No', correct)
        if "no" in lower_correct:
            return re.sub(r'(?i)no', 'Yes', correct)
            
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        返回信息论上有意义的基础查询集合：
        - 8个单项minterms（单个赋值点）
        共 8 个查询足以完全确定目标集合。
        """
        assignments = ["".join(map(str, p)) for p in product([0, 1], repeat=3)]
        
        results = []
        
        # 枚举每个单独赋值的查询（minterm），这8个查询足以完全确定G
        for val in assignments:
            parts = []
            parts.append("x1" if val[0] == '1' else "NOT x1")
            parts.append("x2" if val[1] == '1' else "NOT x2")
            parts.append("x3" if val[2] == '1' else "NOT x3")
            query_content = f"({' AND '.join(parts)})"
            
            K = 1
            H = 1 if val in self.target_set else 0
            
            if H == 0:
                answer = "0/1"
            else:
                answer = "1/1"
            
            results.append({
                "query": f"<query>{query_content}</query>",
                "answer": answer
            })
        
        return results