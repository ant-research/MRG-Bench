from .base import Game
import re
import itertools

class ParityRuleGame(Game):

    reasoning_type = "归纳推理"
    data_structure = "集合"

    game_rule_zh = """\
我们现在来玩一个"奇偶规则推理"游戏，规则如下：

有一个包含16个对象的集合，每个对象由4个二元特征 A1, A2, A3, A4 描述，每个特征的取值为0或1。集合中恰好包含所有可能的特征组合（从 0000 到 1111）各一个。

我已秘密设定了一个"标记规则"，该规则由以下两部分组成：
1. **关键特征集合 H**：从4个特征中选择若干个（可能为空集、单个特征、多个特征或全部特征）
2. **目标奇偶性 p**：为"奇"或"偶"

标记规则的工作方式：对于集合中的任意一个对象，如果该对象在关键特征集合 H 中的特征取值为1的个数的奇偶性等于目标奇偶性 p，则该对象被标记为1；否则标记为0。

例如：若 H = {{A1, A3}}，p = "奇"，则对象 (1,0,1,0) 在 H 中有2个特征为1（偶数），不满足奇数要求，标记为0；而对象 (1,0,0,0) 在 H 中有1个特征为1（奇数），满足要求，标记为1。

通过尽可能少的查询次数，推断出关键特征集合 H 和目标奇偶性 p。

你可以进行"条件计数查询"。每次查询时，你需要对4个特征给出部分约束条件，每个特征可以指定为：
- **0**：该特征必须为0
- **1**：该特征必须为1  
- **?**：该特征可以为0或1（不限制）

**重要限制**：每次查询必须至少有一个特征为 ?（即不允许将所有特征都固定）。

我会返回两个数字：
- **k**：在你的约束条件下，被标记为1的对象数量
- **m**：在你的约束条件下，符合约束的对象总数

每次查询使用以下 XML 格式（四个特征的取值用逗号分隔，顺序为 A1, A2, A3, A4）：

查询示例（查询 A1=1, A2=?, A3=0, A4=? 的情况）：
<query>1,?,0,?</query>

提交最终答案时，需要明确说明关键特征集合 H 和目标奇偶性 p。格式如下：

- H 为特征名称列表，用逗号分隔（若为空集则写 empty）
- p 为"奇"或"偶"

答案示例1（H = {{A1, A3}}，p = 奇）：
<answer>H=A1,A3, p=奇</answer>

答案示例2（H 为空集，p = 偶）：
<answer>H=empty, p=偶</answer>

答案示例3（H = {{A1, A2, A3, A4}}，p = 偶）：
<answer>H=A1,A2,A3,A4, p=偶</answer>
"""

    game_rule_en = """\
Let's play a "Parity Rule Deduction" game. Here are the rules:

There is a set of 16 objects, each described by 4 binary features A1, A2, A3, A4, where each feature takes value 0 or 1. The set contains exactly one object for each possible feature combination (from 0000 to 1111).

I have secretly set up a "marking rule" consisting of two components:
1. **Key Feature Set H**: A subset of the 4 features (may be empty, single feature, multiple features, or all features)
2. **Target Parity p**: Either "odd" or "even"

How the marking rule works: For any object in the set, if the count of features in the key feature set H that have value 1 matches the target parity p, then the object is marked as 1; otherwise marked as 0.

For example: If H = {{A1, A3}}, p = "odd", then object (1,0,1,0) has 2 features in H with value 1 (even count), doesn't satisfy odd requirement, marked as 0; while object (1,0,0,0) has 1 feature in H with value 1 (odd count), satisfies requirement, marked as 1.

Through as few queries as possible, deduce the key feature set H and target parity p.

You can perform "conditional count queries". For each query, you specify partial constraints on the 4 features, where each feature can be:
- **0**: The feature must be 0
- **1**: The feature must be 1
- **?**: The feature can be 0 or 1 (unrestricted)

**Important Restriction**: Each query must have at least one feature as ? (i.e., you cannot fix all features).

I will return two numbers:
- **k**: The count of objects marked as 1 under your constraints
- **m**: The total count of objects satisfying your constraints

Each query uses the following XML format (four feature values separated by commas, in order A1, A2, A3, A4):

Query example (querying A1=1, A2=?, A3=0, A4=?):
<query>1,?,0,?</query>

When submitting final answer, specify the key feature set H and target parity p. Format:

- H is a list of feature names, comma-separated (if empty set, write empty)
- p is "odd" or "even"

Answer example 1 (H = {{A1, A3}}, p = odd):
<answer>H=A1,A3, p=odd</answer>

Answer example 2 (H is empty set, p = even):
<answer>H=empty, p=even</answer>

Answer example 3 (H = {{A1, A2, A3, A4}}, p = even):
<answer>H=A1,A2,A3,A4, p=even</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通系统正在进行“事故风险归纳”风控测试。

在交通流量分析数据库中，包含16种典型的“路口状态画像”，每种画像由4个二元特征 A1, A2, A3, A4 描述（例如：A1代表是否为主干道，A2代表是否为早晚高峰等），每个特征取值为0或1。数据库中恰好涵盖了所有可能的特征组合（从 0000 到 1111）各一个。

交通指挥中心秘密设定了一项“风险标记规则”，该规则由以下两部分组成：
1. **关键特征集合 H**：从4个特征中选择若干个（可能为空集、单个特征、多个特征或全部特征）
2. **目标奇偶性 p**：为"奇"或"偶"

风控判定方式：对于任意一个路口状态，如果该状态在关键特征集合 H 中取值为1的特征个数的奇偶性等于目标奇偶性 p，则该状态被标记为高风险（记为1）；否则标记为正常（记为0）。

例如：若 H = {{A1, A3}}，p = "奇"，则状态 (1,0,1,0) 在 H 中有2个特征为1（偶数），不满足奇数要求，标记为0；而状态 (1,0,0,0) 在 H 中有1个特征为1（奇数），满足要求，标记为1。

通过尽可能少的数据查询次数，推断出控制中心的“关键特征集合 H”和“目标奇偶性 p”。

你可以进行“条件计数查询”。每次查询时，你需要对4个特征给出部分检索条件，每个特征可以指定为：
- **0**：该特征必须为0
- **1**：该特征必须为1  
- **?**：该特征可以为0或1（不限制）

**重要限制**：每次查询必须至少包含一个 ?（即不允许将所有特征都固定检索）。

系统会返回两个统计数字：
- **k**：在你的检索条件下，被标记为高风险(1)的状态数量
- **m**：在你的检索条件下，符合检索条件的状态总数

每次查询使用以下 XML 格式（四个特征的取值用逗号分隔，顺序为 A1, A2, A3, A4）：

查询示例（检索 A1=1, A2=?, A3=0, A4=? 的情况）：
<query>1,?,0,?</query>

提交最终推断时，需要明确说明关键特征集合 H 和目标奇偶性 p。格式如下：

- H 为特征名称列表，用逗号分隔（若为空集则写 empty）
- p 为"奇"或"偶"

答案示例1（H = {{A1, A3}}，p = 奇）：
<answer>H=A1,A3, p=奇</answer>

答案示例2（H 为空集，p = 偶）：
<answer>H=empty, p=偶</answer>

答案示例3（H = {{A1, A2, A3, A4}}，p = 偶）：
<answer>H=A1,A2,A3,A4, p=偶</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
The Intelligent Traffic System is running an "Accident Risk Deduction" risk control test.

The traffic flow database contains 16 typical "intersection state profiles". Each profile is described by 4 binary features A1, A2, A3, A4 (e.g., A1 for main road, A2 for rush hour, etc.), taking values 0 or 1. The database exactly contains all possible feature combinations (from 0000 to 1111) once.

The traffic control center has secretly established a "Risk Marking Rule" consisting of two components:
1. **Key Feature Set H**: A subset of the 4 features (may be empty, single, multiple, or all features)
2. **Target Parity p**: Either "odd" or "even"

Risk assessment logic: For any intersection state, if the count of features in the key feature set H that have value 1 matches the target parity p, the state is flagged as high-risk (marked 1); otherwise normal (marked 0).

For example: If H = {{A1, A3}}, p = "odd", then profile (1,0,1,0) has 2 features in H with value 1 (even count), doesn't satisfy the odd requirement, and is marked 0. Profile (1,0,0,0) has 1 feature in H with value 1 (odd count), satisfies the requirement, and is marked 1.

Through as few data queries as possible, deduce the "Key Feature Set H" and "Target Parity p".

You can perform "conditional count queries". For each query, specify partial search constraints on the 4 features, where each feature can be:
- **0**: The feature must be 0
- **1**: The feature must be 1
- **?**: The feature can be 0 or 1 (unrestricted)

**Important Restriction**: Each query must have at least one feature as ? (cannot fix all features).

The system will return two metrics:
- **k**: The count of high-risk (1) profiles under your constraints
- **m**: The total count of matching profiles satisfying your constraints

Each query uses the following XML format (four feature values separated by commas, in order A1, A2, A3, A4):

Query example (querying A1=1, A2=?, A3=0, A4=?):
<query>1,?,0,?</query>

When submitting your final deduction, specify the key feature set H and target parity p. Format:

- H is a list of feature names, comma-separated (if empty set, write empty)
- p is "odd" or "even"

Answer example 1 (H = {{A1, A3}}, p = odd):
<answer>H=A1,A3, p=odd</answer>

Answer example 2 (H is empty set, p = even):
<answer>H=empty, p=even</answer>

Answer example 3 (H = {{A1, A2, A3, A4}}, p = even):
<answer>H=A1,A2,A3,A4, p=even</answer>
"""

    contextualized_rule_zh_2 = """\
临床医学研究中心正在进行“生物标记物反应归纳”测试。

在患者临床实验数据库中，包含16种典型的“患者症状画像”，每种画像由4个二元临床特征 A1, A2, A3, A4 描述（例如：A1代表是否发热，A2代表是否有基础病等），每个特征取值为0或1。数据库中恰好涵盖了所有可能的特征组合（从 0000 到 1111）各一个。

医学系统秘密设定了一项基于复杂生物学通路的“阳性反应标记规则”，该规则由以下两部分组成：
1. **关键特征集合 H**：从4个特征中选择若干个核心表征（可能为空集、单个特征、多个特征或全部特征）
2. **目标奇偶性 p**：为"奇"或"偶"

临床判定方式：对于任意一个患者画像，如果该画像在关键特征集合 H 中取值为1的特征个数的奇偶性等于目标奇偶性 p，则认为该患者对新药呈阳性反应（记为1）；否则为阴性反应（记为0）。

例如：若 H = {{A1, A3}}，p = "奇"，则画像 (1,0,1,0) 在 H 中有2个特征为1（偶数），不满足奇数要求，标记为0；而画像 (1,0,0,0) 在 H 中有1个特征为1（奇数），满足要求，标记为1。

通过尽可能少的数据查询次数，推断出核心的“关键特征集合 H”和“目标奇偶性 p”。

你可以进行“条件计数查询”。每次查询时，你需要对4个特征给出部分检索条件，每个特征可以指定为：
- **0**：该特征必须为0
- **1**：该特征必须为1  
- **?**：该特征可以为0或1（不限制）

**重要限制**：每次查询必须至少包含一个 ?（即不允许将所有特征都固定检索）。

系统会返回两个统计数字：
- **k**：在你的检索条件下，呈阳性反应(1)的画像数量
- **m**：在你的检索条件下，符合检索条件的画像总数

每次查询使用以下 XML 格式（四个特征的取值用逗号分隔，顺序为 A1, A2, A3, A4）：

查询示例（检索 A1=1, A2=?, A3=0, A4=? 的情况）：
<query>1,?,0,?</query>

提交最终推断时，需要明确说明关键特征集合 H 和目标奇偶性 p。格式如下：

- H 为特征名称列表，用逗号分隔（若为空集则写 empty）
- p 为"奇"或"偶"

答案示例1（H = {{A1, A3}}，p = 奇）：
<answer>H=A1,A3, p=奇</answer>

答案示例2（H 为空集，p = 偶）：
<answer>H=empty, p=偶</answer>

答案示例3（H = {{A1, A2, A3, A4}}，p = 偶）：
<answer>H=A1,A2,A3,A4, p=偶</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
The clinical medical research center is running a "Biomarker Reaction Deduction" test.

The clinical trial database contains 16 typical "patient symptom profiles". Each profile is described by 4 binary clinical features A1, A2, A3, A4 (e.g., A1 for fever, A2 for underlying disease, etc.), taking values 0 or 1. The database exactly contains all possible feature combinations (from 0000 to 1111) once.

The medical system has secretly established a "Positive Reaction Marking Rule" based on a complex biological pathway, consisting of two components:
1. **Key Feature Set H**: A subset of the 4 core clinical features (may be empty, single, multiple, or all features)
2. **Target Parity p**: Either "odd" or "even"

Clinical assessment logic: For any patient profile, if the count of features in the key feature set H that have value 1 matches the target parity p, the patient is considered to have a positive reaction to the new drug (marked 1); otherwise a negative reaction (marked 0).

For example: If H = {{A1, A3}}, p = "odd", then profile (1,0,1,0) has 2 features in H with value 1 (even count), doesn't satisfy the odd requirement, and is marked 0. Profile (1,0,0,0) has 1 feature in H with value 1 (odd count), satisfies the requirement, and is marked 1.

Through as few data queries as possible, deduce the core "Key Feature Set H" and "Target Parity p".

You can perform "conditional count queries". For each query, specify partial search constraints on the 4 features, where each feature can be:
- **0**: The feature must be 0
- **1**: The feature must be 1
- **?**: The feature can be 0 or 1 (unrestricted)

**Important Restriction**: Each query must have at least one feature as ? (cannot fix all features).

The system will return two metrics:
- **k**: The count of positive reaction (1) profiles under your constraints
- **m**: The total count of matching profiles satisfying your constraints

Each query uses the following XML format (four feature values separated by commas, in order A1, A2, A3, A4):

Query example (querying A1=1, A2=?, A3=0, A4=?):
<query>1,?,0,?</query>

When submitting your final deduction, specify the key feature set H and target parity p. Format:

- H is a list of feature names, comma-separated (if empty set, write empty)
- p is "odd" or "even"

Answer example 1 (H = {{A1, A3}}, p = odd):
<answer>H=A1,A3, p=odd</answer>

Answer example 2 (H is empty set, p = even):
<answer>H=empty, p=even</answer>

Answer example 3 (H = {{A1, A2, A3, A4}}, p = even):
<answer>H=A1,A2,A3,A4, p=even</answer>
"""

    contextualized_rule_zh_3 = """\
智能教育平台正在进行“学习轨迹归纳”分析。

在学生行为跟踪数据库中，包含16种典型的“学习行为画像”，每种画像由4个二元行为特征 A1, A2, A3, A4 描述（例如：A1代表是否完成预习，A2代表是否参与讨论等），每个特征取值为0或1。数据库中恰好涵盖了所有可能的特征组合（从 0000 到 1111）各一个。

教学跟踪系统秘密设定了一项“高潜力推荐规则”，该规则由以下两部分组成：
1. **关键特征集合 H**：从4个行为特征中选择若干个（可能为空集、单个特征、多个特征或全部特征）
2. **目标奇偶性 p**：为"奇"或"偶"

推荐判定方式：对于任意一个学习行为画像，如果该画像在关键特征集合 H 中取值为1的特征个数的奇偶性等于目标奇偶性 p，则该画像被标记为推荐进入培优库（记为1）；否则标记为普通（记为0）。

例如：若 H = {{A1, A3}}，p = "奇"，则画像 (1,0,1,0) 在 H 中有2个特征为1（偶数），不满足奇数要求，标记为0；而画像 (1,0,0,0) 在 H 中有1个特征为1（奇数），满足要求，标记为1。

通过尽可能少的数据查询次数，推断出系统的“关键特征集合 H”和“目标奇偶性 p”。

你可以进行“条件计数查询”。每次查询时，你需要对4个特征给出部分检索条件，每个特征可以指定为：
- **0**：该特征必须为0
- **1**：该特征必须为1  
- **?**：该特征可以为0或1（不限制）

**重要限制**：每次查询必须至少包含一个 ?（即不允许将所有特征都固定检索）。

系统会返回两个统计数字：
- **k**：在你的检索条件下，被标记为推荐(1)的画像数量
- **m**：在你的检索条件下，符合检索条件的画像总数

每次查询使用以下 XML 格式（四个特征的取值用逗号分隔，顺序为 A1, A2, A3, A4）：

查询示例（检索 A1=1, A2=?, A3=0, A4=? 的情况）：
<query>1,?,0,?</query>

提交最终推断时，需要明确说明关键特征集合 H 和目标奇偶性 p。格式如下：

- H 为特征名称列表，用逗号分隔（若为空集则写 empty）
- p 为"奇"或"偶"

答案示例1（H = {{A1, A3}}，p = 奇）：
<answer>H=A1,A3, p=奇</answer>

答案示例2（H 为空集，p = 偶）：
<answer>H=empty, p=偶</answer>

答案示例3（H = {{A1, A2, A3, A4}}，p = 偶）：
<answer>H=A1,A2,A3,A4, p=偶</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The intelligent education platform is running a "Learning Trajectory Deduction" analysis.

The student behavior tracking database contains 16 typical "learning behavior profiles". Each profile is described by 4 binary behavioral features A1, A2, A3, A4 (e.g., A1 for pre-class study, A2 for discussion participation, etc.), taking values 0 or 1. The database exactly contains all possible feature combinations (from 0000 to 1111) once.

The tracking system has secretly established a "High-Potential Recommendation Rule" consisting of two components:
1. **Key Feature Set H**: A subset of the 4 behavioral features (may be empty, single, multiple, or all features)
2. **Target Parity p**: Either "odd" or "even"

Recommendation logic: For any learning behavior profile, if the count of features in the key feature set H that have value 1 matches the target parity p, the profile is flagged for recommendation to the advanced track (marked 1); otherwise standard (marked 0).

For example: If H = {{A1, A3}}, p = "odd", then profile (1,0,1,0) has 2 features in H with value 1 (even count), doesn't satisfy the odd requirement, and is marked 0. Profile (1,0,0,0) has 1 feature in H with value 1 (odd count), satisfies the requirement, and is marked 1.

Through as few data queries as possible, deduce the system's "Key Feature Set H" and "Target Parity p".

You can perform "conditional count queries". For each query, specify partial search constraints on the 4 features, where each feature can be:
- **0**: The feature must be 0
- **1**: The feature must be 1
- **?**: The feature can be 0 or 1 (unrestricted)

**Important Restriction**: Each query must have at least one feature as ? (cannot fix all features).

The system will return two metrics:
- **k**: The count of recommended (1) profiles under your constraints
- **m**: The total count of matching profiles satisfying your constraints

Each query uses the following XML format (four feature values separated by commas, in order A1, A2, A3, A4):

Query example (querying A1=1, A2=?, A3=0, A4=?):
<query>1,?,0,?</query>

When submitting your final deduction, specify the key feature set H and target parity p. Format:

- H is a list of feature names, comma-separated (if empty set, write empty)
- p is "odd" or "even"

Answer example 1 (H = {{A1, A3}}, p = odd):
<answer>H=A1,A3, p=odd</answer>

Answer example 2 (H is empty set, p = even):
<answer>H=empty, p=even</answer>

Answer example 3 (H = {{A1, A2, A3, A4}}, p = even):
<answer>H=A1,A2,A3,A4, p=even</answer>
"""

    contextualized_rule_zh_4 = """\
自动化质检系统正在执行“缺陷复检逻辑推导”任务。

在生产工艺数据库中，包含16批典型的“工艺组合批次”，每个批次由4个二元工艺特征 A1, A2, A3, A4 描述（例如：A1代表是否经过高温处理，A2代表是否有化学涂层等），每个特征取值为0或1。数据库中恰好涵盖了所有可能的特征组合（从 0000 到 1111）各一个。

质量保证(QA)模块秘密设定了一项“异常拦截规则”，该规则由以下两部分组成：
1. **关键特征集合 H**：从4个工艺特征中选择若干个重点工艺（可能为空集、单个特征、多个特征或全部特征）
2. **目标奇偶性 p**：为"奇"或"偶"

拦截判定方式：对于任意一个生产批次，如果该批次在关键特征集合 H 中取值为1的特征个数的奇偶性等于目标奇偶性 p，则触发质检警报，该批次被标记为需复检（记为1）；否则标记为直接放行（记为0）。

例如：若 H = {{A1, A3}}，p = "奇"，则批次 (1,0,1,0) 在 H 中有2个特征为1（偶数），不满足奇数要求，标记为0；而批次 (1,0,0,0) 在 H 中有1个特征为1（奇数），满足要求，标记为1。

通过尽可能少的数据查询次数，推断出QA模块内部的“关键特征集合 H”和“目标奇偶性 p”。

你可以进行“条件计数查询”。每次查询时，你需要对4个特征给出部分检索条件，每个特征可以指定为：
- **0**：该特征必须为0
- **1**：该特征必须为1  
- **?**：该特征可以为0或1（不限制）

**重要限制**：每次查询必须至少包含一个 ?（即不允许将所有特征都固定检索）。

系统会返回两个统计数字：
- **k**：在你的检索条件下，被标记为需复检(1)的批次数量
- **m**：在你的检索条件下，符合检索条件的批次总数

每次查询使用以下 XML 格式（四个特征的取值用逗号分隔，顺序为 A1, A2, A3, A4）：

查询示例（检索 A1=1, A2=?, A3=0, A4=? 的情况）：
<query>1,?,0,?</query>

提交最终推断时，需要明确说明关键特征集合 H 和目标奇偶性 p。格式如下：

- H 为特征名称列表，用逗号分隔（若为空集则写 empty）
- p 为"奇"或"偶"

答案示例1（H = {{A1, A3}}，p = 奇）：
<answer>H=A1,A3, p=奇</answer>

答案示例2（H 为空集，p = 偶）：
<answer>H=empty, p=偶</answer>

答案示例3（H = {{A1, A2, A3, A4}}，p = 偶）：
<answer>H=A1,A2,A3,A4, p=偶</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
The automated quality inspection system is performing a "Defect Re-inspection Logic Deduction" task.

The production process database contains 16 typical "process combination batches". Each batch is described by 4 binary process features A1, A2, A3, A4 (e.g., A1 for high-temp treatment, A2 for chemical coating, etc.), taking values 0 or 1. The database exactly contains all possible feature combinations (from 0000 to 1111) once.

The Quality Assurance (QA) module has secretly established an "Anomaly Interception Rule" consisting of two components:
1. **Key Feature Set H**: A subset of the 4 core process features (may be empty, single, multiple, or all features)
2. **Target Parity p**: Either "odd" or "even"

Interception logic: For any production batch, if the count of features in the key feature set H that have value 1 matches the target parity p, it triggers a quality alert, and the batch is flagged for re-inspection (marked 1); otherwise it passes directly (marked 0).

For example: If H = {{A1, A3}}, p = "odd", then batch (1,0,1,0) has 2 features in H with value 1 (even count), doesn't satisfy the odd requirement, and is marked 0. Batch (1,0,0,0) has 1 feature in H with value 1 (odd count), satisfies the requirement, and is marked 1.

Through as few data queries as possible, deduce the QA module's internal "Key Feature Set H" and "Target Parity p".

You can perform "conditional count queries". For each query, specify partial search constraints on the 4 features, where each feature can be:
- **0**: The feature must be 0
- **1**: The feature must be 1
- **?**: The feature can be 0 or 1 (unrestricted)

**Important Restriction**: Each query must have at least one feature as ? (cannot fix all features).

The system will return two metrics:
- **k**: The count of batches flagged for re-inspection (1) under your constraints
- **m**: The total count of matching batches satisfying your constraints

Each query uses the following XML format (four feature values separated by commas, in order A1, A2, A3, A4):

Query example (querying A1=1, A2=?, A3=0, A4=?):
<query>1,?,0,?</query>

When submitting your final deduction, specify the key feature set H and target parity p. Format:

- H is a list of feature names, comma-separated (if empty set, write empty)
- p is "odd" or "even"

Answer example 1 (H = {{A1, A3}}, p = odd):
<answer>H=A1,A3, p=odd</answer>

Answer example 2 (H is empty set, p = even):
<answer>H=empty, p=even</answer>

Answer example 3 (H = {{A1, A2, A3, A4}}, p = even):
<answer>H=A1,A2,A3,A4, p=even</answer>
"""

    contextualized_rule_zh_5 = """\
合规审查系统正在进行“反垄断审查触发机制”推演。

在企业尽职调查数据库中，包含16宗典型的“企业并购案画像”，每宗画像由4个二元法律特征 A1, A2, A3, A4 描述（例如：A1代表是否含外资背景，A2代表是否涉及数据出境等），每个特征取值为0或1。数据库中恰好涵盖了所有可能的特征组合（从 0000 到 1111）各一个。

监管框架内秘密设定了一项“重点审查触发规则”，该规则由以下两部分组成：
1. **关键特征集合 H**：从4个法律特征中选择若干个（可能为空集、单个特征、多个特征或全部特征）
2. **目标奇偶性 p**：为"奇"或"偶"

触发判定方式：对于任意一宗并购案，如果该案件在关键特征集合 H 中取值为1的特征个数的奇偶性等于目标奇偶性 p，则触发红线，案件被标记为需审查（记为1）；否则标记为合规（记为0）。

例如：若 H = {{A1, A3}}，p = "奇"，则案件 (1,0,1,0) 在 H 中有2个特征为1（偶数），不满足奇数要求，标记为0；而案件 (1,0,0,0) 在 H 中有1个特征为1（奇数），满足要求，标记为1。

通过尽可能少的数据查询次数，推断出监管框架设定的“关键特征集合 H”和“目标奇偶性 p”。

你可以进行“条件计数查询”。每次查询时，你需要对4个特征给出部分检索条件，每个特征可以指定为：
- **0**：该特征必须为0
- **1**：该特征必须为1  
- **?**：该特征可以为0或1（不限制）

**重要限制**：每次查询必须至少包含一个 ?（即不允许将所有特征都固定检索）。

系统会返回两个统计数字：
- **k**：在你的检索条件下，被标记为需审查(1)的案件数量
- **m**：在你的检索条件下，符合检索条件的案件总数

每次查询使用以下 XML 格式（四个特征的取值用逗号分隔，顺序为 A1, A2, A3, A4）：

查询示例（检索 A1=1, A2=?, A3=0, A4=? 的情况）：
<query>1,?,0,?</query>

提交最终推断时，需要明确说明关键特征集合 H 和目标奇偶性 p。格式如下：

- H 为特征名称列表，用逗号分隔（若为空集则写 empty）
- p 为"奇"或"偶"

答案示例1（H = {{A1, A3}}，p = 奇）：
<answer>H=A1,A3, p=奇</answer>

答案示例2（H 为空集，p = 偶）：
<answer>H=empty, p=偶</answer>

答案示例3（H = {{A1, A2, A3, A4}}，p = 偶）：
<answer>H=A1,A2,A3,A4, p=偶</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
The compliance review system is running an "Antitrust Review Trigger Deduction" exercise.

The corporate due diligence database contains 16 typical "corporate M&A case profiles". Each profile is described by 4 binary legal features A1, A2, A3, A4 (e.g., A1 for foreign capital involvement, A2 for cross-border data transfer, etc.), taking values 0 or 1. The database exactly contains all possible feature combinations (from 0000 to 1111) once.

The regulatory framework has secretly established a "Priority Review Trigger Rule" consisting of two components:
1. **Key Feature Set H**: A subset of the 4 legal features (may be empty, single, multiple, or all features)
2. **Target Parity p**: Either "odd" or "even"

Trigger logic: For any M&A case, if the count of features in the key feature set H that have value 1 matches the target parity p, the red line is triggered and the case is flagged for review (marked 1); otherwise compliant (marked 0).

For example: If H = {{A1, A3}}, p = "odd", then case (1,0,1,0) has 2 features in H with value 1 (even count), doesn't satisfy the odd requirement, and is marked 0. Case (1,0,0,0) has 1 feature in H with value 1 (odd count), satisfies the requirement, and is marked 1.

Through as few data queries as possible, deduce the regulatory framework's "Key Feature Set H" and "Target Parity p".

You can perform "conditional count queries". For each query, specify partial search constraints on the 4 features, where each feature can be:
- **0**: The feature must be 0
- **1**: The feature must be 1
- **?**: The feature can be 0 or 1 (unrestricted)

**Important Restriction**: Each query must have at least one feature as ? (cannot fix all features).

The system will return two metrics:
- **k**: The count of cases flagged for review (1) under your constraints
- **m**: The total count of matching cases satisfying your constraints

Each query uses the following XML format (four feature values separated by commas, in order A1, A2, A3, A4):

Query example (querying A1=1, A2=?, A3=0, A4=?):
<query>1,?,0,?</query>

When submitting your final deduction, specify the key feature set H and target parity p. Format:

- H is a list of feature names, comma-separated (if empty set, write empty)
- p is "odd" or "even"

Answer example 1 (H = {{A1, A3}}, p = odd):
<answer>H=A1,A3, p=odd</answer>

Answer example 2 (H is empty set, p = even):
<answer>H=empty, p=even</answer>

Answer example 3 (H = {{A1, A2, A3, A4}}, p = even):
<answer>H=A1,A2,A3,A4, p=even</answer>
"""

    tags = ["answer", "query"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "H": ["A1"],
                "p": "偶",
            },
            2: {
                "H": [],
                "p": "偶",
            },
            3: {
                "H": ["A1", "A3"],
                "p": "奇",
            },
            4: {
                "H": ["A2", "A3", "A4"],
                "p": "偶",
            },
            5: {
                "H": ["A1", "A2", "A3", "A4"],
                "p": "奇",
            },
        },
        "en": {
            1: {
                "H": ["A1"],
                "p": "even",
            },
            2: {
                "H": [],
                "p": "even",
            },
            3: {
                "H": ["A1", "A3"],
                "p": "odd",
            },
            4: {
                "H": ["A2", "A3", "A4"],
                "p": "even",
            },
            5: {
                "H": ["A1", "A2", "A3", "A4"],
                "p": "odd",
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
        
        self.H = set(cfg["H"])
        self.p = cfg["p"]
        
        self.objects = []
        self.markings = []
        
        for i in range(16):
            obj = [
                (i >> 3) & 1,
                (i >> 2) & 1,
                (i >> 1) & 1,
                i & 1
            ]
            self.objects.append(obj)
            
            count_in_H = sum(
                obj[j] for j, feature in enumerate(["A1", "A2", "A3", "A4"])
                if feature in self.H
            )
            
            if lang == "zh":
                target_is_odd = (self.p == "奇")
            else:
                target_is_odd = (self.p == "odd")
            
            actual_is_odd = (count_in_H % 2 == 1)
            
            marking = 1 if (actual_is_odd == target_is_odd) else 0
            self.markings.append(marking)
        
        self._game_info = {}

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            h_match = re.search(r'H\s*=\s*(.*?)\s*,\s*p\s*=', raw_ans, re.IGNORECASE)
            p_match = re.search(r'p\s*=\s*(\S+)', raw_ans, re.IGNORECASE)
            
            if not h_match or not p_match:
                return False
            
            h_str = h_match.group(1).strip()
            model_p = p_match.group(1).strip().rstrip('.,;:!?。，；：！？')
            
            if h_str.lower() == "empty":
                model_H = set()
            else:
                model_H = set(x.strip().upper() for x in h_str.split(",") if x.strip())
            
            expected_H = set(x.upper() for x in self.H)
            
            if model_H != expected_H:
                return False
            
            if model_p.lower() != self.p.lower():
                return False
            
            return True
            
        except Exception:
            return False

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        options = ["0", "1", "?"]
        
        for p in itertools.product(options, repeat=4):
            if "?" not in p:
                continue
            
            query_str = ",".join(p)
            
            answer = self._cf_core_produce({"query": query_str})
            
            results.append({
                "query": f"<query>{query_str}</query>",
                "answer": answer
            })
            
        return results

    def _cf_core_produce(self, parsed_info):
        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        query_str = parsed_info["query"].strip()
        
        try:
            constraints = [x.strip() for x in query_str.split(",")]
            
            if len(constraints) != 4:
                if self.config.language == "zh":
                    return "错误：查询必须包含4个特征的约束（用逗号分隔）。"
                else:
                    return "Error: Query must contain constraints for 4 features (comma-separated)."
            
            if "?" not in constraints:
                if self.config.language == "zh":
                    return "错误：查询必须至少有一个特征为 ?（不能将所有特征都固定）。"
                else:
                    return "Error: Query must have at least one feature as ? (cannot fix all features)."
            
            for c in constraints:
                if c not in ["0", "1", "?"]:
                    if self.config.language == "zh":
                        return "错误：每个特征的约束必须是 0、1 或 ?。"
                    else:
                        return "Error: Each feature constraint must be 0, 1, or ?."
            
            k = 0
            m = 0
            
            for obj, marking in zip(self.objects, self.markings):
                satisfies = True
                for i, constraint in enumerate(constraints):
                    if constraint != "?":
                        if obj[i] != int(constraint):
                            satisfies = False
                            break
                
                if satisfies:
                    m += 1
                    if marking == 1:
                        k += 1
            
            if self.config.language == "zh":
                return f"满足条件且被标记为1的对象数量 k = {k}，符合条件的对象总数 m = {m}。"
            else:
                return f"Count of marked objects k = {k}, total count of matching objects m = {m}."
            
        except Exception as e:
            if self.config.language == "zh":
                return f"错误：查询格式无效。{str(e)}"
            else:
                return f"Error: Invalid query format. {str(e)}"

    def _cf_make_wrong(self, correct: str) -> str:
        import re as _re
        
        def _modify_k(match):
            k_val = int(match.group(1))
            m_match = _re.search(r'm\s*=\s*(\d+)', correct)
            m_val = int(m_match.group(1)) if m_match else 16
            wrong_k = k_val + 1 if k_val < m_val else k_val - 1
            return match.group(0).replace(match.group(1), str(wrong_k))
        
        modified = _re.sub(r'k\s*=\s*(\d+)', _modify_k, correct, count=1)
        
        if modified != correct:
            return modified
        
        return correct + "_WRONG"