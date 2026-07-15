import random
from .base import Game
import re

class AbstractReasoningGame(Game):

    game_rule_zh = """\
我们现在来玩一个"抽象推理"游戏，规则如下：

游戏设定了五种元素类型，记为 1, 2, 3, 4, 5，每种类型可以无限次添加。

系统状态是一个多重集合，由各类型的计数向量 x = (x1, x2, x3, x4, x5) 表示，其中每个 xi 是该类型元素的个数（非负整数）。初始状态下所有计数都为 0。

系统已秘密启用四种统计规则之一，该规则在整个游戏过程中固定不变。目标统计值 T = 3。

四种备选统计规则（具体启用哪一个是隐藏的）：
- 规则 A（不同类型计数）：统计值等于当前计数大于 0 的类型数量。
- 规则 B（成对计数）：统计值等于所有类型的"计数除以 2 向下取整"之和。
- 规则 C（奇数类型计数）：统计值等于当前计数为奇数的类型数量。
- 规则 D（最大计数）：统计值等于所有类型中计数的最大值（若所有为 0 则统计值为 0）。

你可以进行以下操作：

1. 添加操作（会改变状态，计入步数）：选择任一类型 i（1 到 5），添加一枚该类型的元素。系统会立即返回当前的统计值。

2. 查询操作（不改变状态，不计入步数）：
   - 查询当前统计值：询问当前统计值是多少，系统返回一个非负整数。
   - 查询统计值是否等于某值：询问当前统计值是否等于某个值 v，系统返回"是"或"否"。
   - 查询统计值变化：询问相较于上一次数值查询或添加操作后的读数，统计值变化了多少。系统返回一个整数；若无上次读数则返回提示信息。
   - 查询规则类型：询问当前启用的规则是否为某个特定规则（A、B、C 或 D），系统返回"是"或"否"。

3. 终局声明：当你认为已经推理出正确答案时，提交你的声明，包括：
   - 你认为的规则类型（A、B、C 或 D）
   - 你使用的添加操作次数
   系统会核验：规则是否正确，当前统计值是否等于 3，以及你使用的添加次数是否等于该规则下从空集达到统计值 3 的理论最少添加数。

你的目标是：
- 正确识别当前启用的规则
- 使当前统计值达到 3
- 使用尽可能少的添加次数

每次操作只能包含一个标签。请使用以下 XML 格式：

- 添加操作（例如添加类型 3）：
<add>3</add>

- 查询当前统计值：
<query_value></query_value>

- 查询统计值是否等于某值（例如查询是否等于 2）：
<query_equal>2</query_equal>

- 查询统计值变化：
<query_change></query_change>

- 查询规则类型（例如查询是否为规则 A）：
<query_rule>A</query_rule>

- 提交终局声明（例如声明规则为 A，使用了 3 次添加）：
<answer>rule=A, steps=3</answer>
"""

    game_rule_en = """\
Let's play an "Abstract Reasoning" game. Here are the rules:

The game has five element types, labeled 1, 2, 3, 4, 5. Each type can be added unlimited times.

The system state is a multiset represented by a count vector x = (x1, x2, x3, x4, x5), where each xi is the count of that type (non-negative integer). Initially, all counts are 0.

The system has secretly enabled one of four statistical rules, which remains fixed throughout the game. The target statistical value is T = 3.

Four candidate statistical rules (which one is enabled is hidden):
- Rule A (Distinct Type Count): The statistical value equals the number of types with count greater than 0.
- Rule B (Pair Count): The statistical value equals the sum of "count divided by 2 rounded down" for all types.
- Rule C (Odd Type Count): The statistical value equals the number of types with odd count.
- Rule D (Maximum Count): The statistical value equals the maximum count among all types (0 if all are 0).

You can perform the following operations:

1. Add operation (changes state, counts as a step): Choose any type i (1 to 5) and add one element of that type. The system immediately returns the current statistical value.

2. Query operation (does not change state, does not count as a step):
   - Query current value: Ask what the current statistical value is. System returns a non-negative integer.
   - Query equality: Ask whether the current statistical value equals some value v. System returns "Yes" or "No".
   - Query change: Ask how much the statistical value changed compared to the last numerical query or add operation. System returns an integer; if no previous reading exists, returns a notice.
   - Query rule type: Ask whether the currently enabled rule is a specific rule (A, B, C, or D). System returns "Yes" or "No".

3. Final declaration: When you believe you have deduced the correct answer, submit your declaration including:
   - The rule type you believe is active (A, B, C, or D)
   - The number of add operations you used
   The system will verify: whether the rule is correct, whether the current statistical value equals 3, and whether your add count equals the theoretical minimum number of adds needed to reach statistical value 3 from the empty set under that rule.

Your goal is to:
- Correctly identify the currently enabled rule
- Make the current statistical value reach 3
- Use as few add operations as possible

Each operation must contain only one tag. Use the following XML format:

- Add operation (e.g., add type 3):
<add>3</add>

- Query current statistical value:
<query_value></query_value>

- Query whether value equals something (e.g., query if equals 2):
<query_equal>2</query_equal>

- Query value change:
<query_change></query_change>

- Query rule type (e.g., query if rule is A):
<query_rule>A</query_rule>

- Submit final declaration (e.g., declare rule is A with 3 adds):
<answer>rule=A, steps=3</answer>
"""

    contextualized_rule_zh_1 = """\
我们现在来体验一个"智能交通调度"系统模拟。

系统设定了五种车辆类型，记为 1, 2, 3, 4, 5，每种类型可以无限次调度。

系统状态是一个多重集合，由各类型的调度计数向量 x = (x1, x2, x3, x4, x5) 表示，其中每个 xi 是该类型车辆的调度数量（非负整数）。初始状态下所有调度计数都为 0。

系统已秘密启用四种拥堵评估规则之一，该规则在整个调度过程中固定不变。目标拥堵指数 T = 3。

四种备选拥堵评估规则（具体启用哪一个是隐藏的）：
- 规则 A（车源丰富度）：拥堵指数等于当前调度数量大于 0 的车辆类型数量。
- 规则 B（车辆配对数）：拥堵指数等于所有类型的"调度数量除以 2 向下取整"之和（即成对出现的车辆对数）。
- 规则 C（零散调度数）：拥堵指数等于当前调度数量为奇数的车辆类型数量。
- 规则 D（单一极值）：拥堵指数等于所有车辆类型中调度数量的最大值（若所有为 0 则指数为 0）。

你可以进行以下操作：

1. 调度操作（会改变状态，计入步数）：选择任一车辆类型 i（1 到 5），向路网调度一辆该类型的车。系统会立即返回当前的拥堵指数。

2. 查询操作（不改变状态，不计入步数）：
   - 查询当前指数：询问当前的拥堵指数是多少，系统返回一个非负整数。
   - 查询指数是否达标：询问当前拥堵指数是否等于某个值 v，系统返回"是"或"否"。
   - 查询指数波动：询问相较于上一次数值查询或调度操作后的读数，拥堵指数变化了多少。系统返回一个整数；若无上次读数则返回提示信息。
   - 查询评估规则：询问当前启用的规则是否为某个特定规则（A、B、C 或 D），系统返回"是"或"否"。

3. 终局声明：当你认为已经推理出正确答案时，提交你的声明，包括：
   - 你认为的评估规则类型（A、B、C 或 D）
   - 你使用的调度操作次数
   系统会核验：规则是否正确，当前拥堵指数是否等于 3，以及你使用的调度次数是否等于该规则下从空集达到指数 3 的理论最少调度数。

你的目标是：
- 正确识别当前启用的评估规则
- 使当前拥堵指数达到 3
- 使用尽可能少的调度操作次数

每次操作只能包含一个标签。请使用以下 XML 格式：

- 调度操作（例如调度类型 3）：
<add>3</add>

- 查询当前拥堵指数：
<query_value></query_value>

- 查询指数是否等于某值（例如查询是否等于 2）：
<query_equal>2</query_equal>

- 查询指数波动：
<query_change></query_change>

- 查询评估规则（例如查询是否为规则 A）：
<query_rule>A</query_rule>

- 提交终局声明（例如声明规则为 A，使用了 3 次调度）：
<answer>rule=A, steps=3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's experience an "Intelligent Traffic Dispatch" system simulation.

The system features five vehicle types, labeled 1, 2, 3, 4, 5. Each type can be dispatched an unlimited number of times.

The system state is a multiset represented by a dispatch count vector x = (x1, x2, x3, x4, x5), where each xi is the dispatch count of that vehicle type (non-negative integer). Initially, all dispatch counts are 0.

The system has secretly enabled one of four congestion evaluation rules, which remains fixed throughout the dispatch process. The target congestion index is T = 3.

Four candidate congestion evaluation rules (which one is enabled is hidden):
- Rule A (Vehicle Diversity): The congestion index equals the number of vehicle types with a dispatch count greater than 0.
- Rule B (Vehicle Pairs): The congestion index equals the sum of "dispatch count divided by 2 rounded down" for all types.
- Rule C (Unpaired Dispatches): The congestion index equals the number of vehicle types with an odd dispatch count.
- Rule D (Single Extreme): The congestion index equals the maximum dispatch count among all vehicle types (0 if all are 0).

You can perform the following operations:

1. Dispatch operation (changes state, counts as a step): Choose any vehicle type i (1 to 5) and dispatch one vehicle of that type to the network. The system immediately returns the current congestion index.

2. Query operation (does not change state, does not count as a step):
   - Query current index: Ask what the current congestion index is. System returns a non-negative integer.
   - Query index target: Ask whether the current congestion index equals some value v. System returns "Yes" or "No".
   - Query index fluctuation: Ask how much the congestion index changed compared to the last numerical query or dispatch operation. System returns an integer; if no previous reading exists, returns a notice.
   - Query evaluation rule: Ask whether the currently enabled rule is a specific rule (A, B, C, or D). System returns "Yes" or "No".

3. Final declaration: When you believe you have deduced the correct answer, submit your declaration including:
   - The evaluation rule you believe is active (A, B, C, or D)
   - The number of dispatch operations you used
   The system will verify: whether the rule is correct, whether the current congestion index equals 3, and whether your dispatch count equals the theoretical minimum number of dispatches needed to reach congestion index 3 from an empty network under that rule.

Your goal is to:
- Correctly identify the currently enabled evaluation rule
- Make the current congestion index reach 3
- Use as few dispatch operations as possible

Each operation must contain only one tag. Use the following XML format:

- Dispatch operation (e.g., dispatch type 3):
<add>3</add>

- Query current congestion index:
<query_value></query_value>

- Query whether index equals something (e.g., query if equals 2):
<query_equal>2</query_equal>

- Query index fluctuation:
<query_change></query_change>

- Query evaluation rule (e.g., query if rule is A):
<query_rule>A</query_rule>

- Submit final declaration (e.g., declare rule is A with 3 dispatches):
<answer>rule=A, steps=3</answer>
"""

    contextualized_rule_zh_2 = """\
我们现在来体验一个"精准医疗用药"干预系统模拟。

系统设定了五种靶向药物类型，记为 1, 2, 3, 4, 5，每种类型可以无限次施加剂量。

系统状态是一个多重集合，由各药物类型的剂量向量 x = (x1, x2, x3, x4, x5) 表示，其中每个 xi 是该药物类型的施加剂量（非负整数）。初始状态下所有剂量都为 0。

系统已秘密启用四种疗效评估规则之一，该规则在整个干预过程中固定不变。目标综合疗效指数 T = 3。

四种备选疗效评估规则（具体启用哪一个是隐藏的）：
- 规则 A（用药广度）：疗效指数等于当前施加剂量大于 0 的药物种类数量。
- 规则 B（协同作用）：疗效指数等于所有药物类型的"剂量除以 2 向下取整"之和（即成对剂量产生的协同效应）。
- 规则 C（剂量失衡）：疗效指数等于当前施加剂量为奇数的药物种类数量。
- 规则 D（用药极值）：疗效指数等于所有药物类型中剂量的最大值（若所有为 0 则指数为 0）。

你可以进行以下操作：

1. 施药操作（会改变状态，计入步数）：选择任一药物类型 i（1 到 5），为患者施加一剂该类型的药物。系统会立即返回当前的疗效指数。

2. 查询操作（不改变状态，不计入步数）：
   - 查询当前指数：询问当前的疗效指数是多少，系统返回一个非负整数。
   - 查询指数是否达标：询问当前疗效指数是否等于某个值 v，系统返回"是"或"否"。
   - 查询指数波动：询问相较于上一次数值查询或施药操作后的读数，疗效指数变化了多少。系统返回一个整数；若无上次读数则返回提示信息。
   - 查询评估规则：询问当前启用的规则是否为某个特定规则（A、B、C 或 D），系统返回"是"或"否"。

3. 终局声明：当你认为已经推理出正确答案时，提交你的用药声明，包括：
   - 你认为的评估规则类型（A、B、C 或 D）
   - 你使用的施药操作次数
   系统会核验：规则是否正确，当前疗效指数是否等于 3，以及你使用的施药次数是否等于该规则下从零剂量达到指数 3 的理论最少施药数。

你的目标是：
- 正确识别当前启用的评估规则
- 使当前疗效指数达到 3
- 使用尽可能少的施药操作次数

每次操作只能包含一个标签。请使用以下 XML 格式：

- 施药操作（例如施加药物 3）：
<add>3</add>

- 查询当前疗效指数：
<query_value></query_value>

- 查询指数是否等于某值（例如查询是否等于 2）：
<query_equal>2</query_equal>

- 查询指数波动：
<query_change></query_change>

- 查询评估规则（例如查询是否为规则 A）：
<query_rule>A</query_rule>

- 提交终局声明（例如声明规则为 A，使用了 3 次施药）：
<answer>rule=A, steps=3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's experience a "Precision Medical Medication" intervention system simulation.

The system features five targeted drug types, labeled 1, 2, 3, 4, 5. Each type can be administered an unlimited number of times.

The system state is a multiset represented by a dosage vector x = (x1, x2, x3, x4, x5), where each xi is the administered dose of that drug type (non-negative integer). Initially, all doses are 0.

The system has secretly enabled one of four therapeutic evaluation rules, which remains fixed throughout the intervention. The target comprehensive therapeutic index is T = 3.

Four candidate therapeutic evaluation rules (which one is enabled is hidden):
- Rule A (Medication Breadth): The therapeutic index equals the number of drug types with a dose greater than 0.
- Rule B (Synergistic Effect): The therapeutic index equals the sum of "dose divided by 2 rounded down" for all types (representing synergy from paired doses).
- Rule C (Dose Imbalance): The therapeutic index equals the number of drug types with an odd dose.
- Rule D (Medication Extreme): The therapeutic index equals the maximum dose among all drug types (0 if all are 0).

You can perform the following operations:

1. Administer operation (changes state, counts as a step): Choose any drug type i (1 to 5) and administer one dose of that drug to the patient. The system immediately returns the current therapeutic index.

2. Query operation (does not change state, does not count as a step):
   - Query current index: Ask what the current therapeutic index is. System returns a non-negative integer.
   - Query index target: Ask whether the current therapeutic index equals some value v. System returns "Yes" or "No".
   - Query index fluctuation: Ask how much the therapeutic index changed compared to the last numerical query or administer operation. System returns an integer; if no previous reading exists, returns a notice.
   - Query evaluation rule: Ask whether the currently enabled rule is a specific rule (A, B, C, or D). System returns "Yes" or "No".

3. Final declaration: When you believe you have deduced the correct answer, submit your medication declaration including:
   - The evaluation rule you believe is active (A, B, C, or D)
   - The number of administer operations you used
   The system will verify: whether the rule is correct, whether the current therapeutic index equals 3, and whether your administer count equals the theoretical minimum number of doses needed to reach therapeutic index 3 from a zero-dose state under that rule.

Your goal is to:
- Correctly identify the currently enabled evaluation rule
- Make the current therapeutic index reach 3
- Use as few administer operations as possible

Each operation must contain only one tag. Use the following XML format:

- Administer operation (e.g., administer drug 3):
<add>3</add>

- Query current therapeutic index:
<query_value></query_value>

- Query whether index equals something (e.g., query if equals 2):
<query_equal>2</query_equal>

- Query index fluctuation:
<query_change></query_change>

- Query evaluation rule (e.g., query if rule is A):
<query_rule>A</query_rule>

- Submit final declaration (e.g., declare rule is A with 3 doses):
<answer>rule=A, steps=3</answer>
"""

    contextualized_rule_zh_3 = """\
我们现在来体验一个"个性化教学配置"模拟系统。

系统设定了五种学科模块，记为 1, 2, 3, 4, 5，每个模块可以无限次为学生配置任务。

系统状态是一个多重集合，由各模块的配置次数向量 x = (x1, x2, x3, x4, x5) 表示，其中每个 xi 是该模块被配置的次数（非负整数）。初始状态下所有配置次数都为 0。

系统已秘密启用四种素养评估规则之一，该规则在整个配置过程中固定不变。目标综合素养指数 T = 3。

四种备选素养评估规则（具体启用哪一个是隐藏的）：
- 规则 A（学科广度）：素养指数等于当前配置次数大于 0 的模块数量。
- 规则 B（深度搭配）：素养指数等于所有模块的"配置次数除以 2 向下取整"之和（即形成配对的深度学习任务）。
- 规则 C（偏科指标）：素养指数等于当前配置次数为奇数的模块数量。
- 规则 D（单科专精）：素养指数等于所有模块中配置次数的最大值（若所有为 0 则指数为 0）。

你可以进行以下操作：

1. 配置操作（会改变状态，计入步数）：选择任一模块 i（1 到 5），为学生增加一次该模块的任务。系统会立即返回当前的素养指数。

2. 查询操作（不改变状态，不计入步数）：
   - 查询当前指数：询问当前的素养指数是多少，系统返回一个非负整数。
   - 查询指数是否达标：询问当前素养指数是否等于某个值 v，系统返回"是"或"否"。
   - 查询指数波动：询问相较于上一次数值查询或配置操作后的读数，素养指数变化了多少。系统返回一个整数；若无上次读数则返回提示信息。
   - 查询评估规则：询问当前启用的规则是否为某个特定规则（A、B、C 或 D），系统返回"是"或"否"。

3. 终局声明：当你认为已经推理出正确答案时，提交你的配置方案声明，包括：
   - 你认为的评估规则类型（A、B、C 或 D）
   - 你使用的配置操作次数
   系统会核验：规则是否正确，当前素养指数是否等于 3，以及你使用的配置次数是否等于该规则下从零任务达到指数 3 的理论最少配置数。

你的目标是：
- 正确识别当前启用的评估规则
- 使当前素养指数达到 3
- 使用尽可能少的配置操作次数

每次操作只能包含一个标签。请使用以下 XML 格式：

- 配置操作（例如增加模块 3）：
<add>3</add>

- 查询当前素养指数：
<query_value></query_value>

- 查询指数是否等于某值（例如查询是否等于 2）：
<query_equal>2</query_equal>

- 查询指数波动：
<query_change></query_change>

- 查询评估规则（例如查询是否为规则 A）：
<query_rule>A</query_rule>

- 提交终局声明（例如声明规则为 A，使用了 3 次配置）：
<answer>rule=A, steps=3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's experience a "Personalized Teaching Configuration" simulation system.

The system features five subject modules, labeled 1, 2, 3, 4, 5. Each module can be assigned to students an unlimited number of times.

The system state is a multiset represented by an assignment count vector x = (x1, x2, x3, x4, x5), where each xi is the number of assignments for that module (non-negative integer). Initially, all assignment counts are 0.

The system has secretly enabled one of four literacy evaluation rules, which remains fixed throughout the configuration process. The target comprehensive literacy index is T = 3.

Four candidate literacy evaluation rules (which one is enabled is hidden):
- Rule A (Subject Breadth): The literacy index equals the number of modules with an assignment count greater than 0.
- Rule B (In-depth Pairing): The literacy index equals the sum of "assignment count divided by 2 rounded down" for all modules.
- Rule C (Imbalance Indicator): The literacy index equals the number of modules with an odd assignment count.
- Rule D (Single Subject Mastery): The literacy index equals the maximum assignment count among all modules (0 if all are 0).

You can perform the following operations:

1. Assign operation (changes state, counts as a step): Choose any module i (1 to 5) and assign one task of that module to the student. The system immediately returns the current literacy index.

2. Query operation (does not change state, does not count as a step):
   - Query current index: Ask what the current literacy index is. System returns a non-negative integer.
   - Query index target: Ask whether the current literacy index equals some value v. System returns "Yes" or "No".
   - Query index fluctuation: Ask how much the literacy index changed compared to the last numerical query or assign operation. System returns an integer; if no previous reading exists, returns a notice.
   - Query evaluation rule: Ask whether the currently enabled rule is a specific rule (A, B, C, or D). System returns "Yes" or "No".

3. Final declaration: When you believe you have deduced the correct answer, submit your configuration declaration including:
   - The evaluation rule you believe is active (A, B, C, or D)
   - The number of assign operations you used
   The system will verify: whether the rule is correct, whether the current literacy index equals 3, and whether your assign count equals the theoretical minimum number of assignments needed to reach literacy index 3 from zero tasks under that rule.

Your goal is to:
- Correctly identify the currently enabled evaluation rule
- Make the current literacy index reach 3
- Use as few assign operations as possible

Each operation must contain only one tag. Use the following XML format:

- Assign operation (e.g., assign module 3):
<add>3</add>

- Query current literacy index:
<query_value></query_value>

- Query whether index equals something (e.g., query if equals 2):
<query_equal>2</query_equal>

- Query index fluctuation:
<query_change></query_change>

- Query evaluation rule (e.g., query if rule is A):
<query_rule>A</query_rule>

- Submit final declaration (e.g., declare rule is A with 3 assignments):
<answer>rule=A, steps=3</answer>
"""

    contextualized_rule_zh_4 = """\
我们现在来体验一个"智能产线工序部署"模拟系统。

系统设定了五种加工工序类型，记为 1, 2, 3, 4, 5，每种工序可以在产线上无限次重复部署。

系统状态是一个多重集合，由各工序类型的部署计数向量 x = (x1, x2, x3, x4, x5) 表示，其中每个 xi 是该工序部署的次数（非负整数）。初始状态下所有工序部署都为 0。

系统已秘密启用四种能耗评估规则之一，该规则在整个部署过程中固定不变。目标综合负荷等级 T = 3。

四种备选能耗评估规则（具体启用哪一个是隐藏的）：
- 规则 A（工序多样性）：负荷等级等于当前部署次数大于 0 的工序种类数量。
- 规则 B（工序偶联数）：负荷等级等于所有工序类型的"部署次数除以 2 向下取整"之和（即成对部署带来的耦合损耗）。
- 规则 C（异步工序数）：负荷等级等于当前部署次数为奇数的工序种类数量。
- 规则 D（单一工序瓶颈）：负荷等级等于所有工序类型中部署次数的最大值（若所有为 0 则等级为 0）。

你可以进行以下操作：

1. 部署操作（会改变状态，计入步数）：选择任一工序类型 i（1 到 5），在产线上增加一道该工序。系统会立即返回当前的负荷等级。

2. 查询操作（不改变状态，不计入步数）：
   - 查询当前等级：询问当前的负荷等级是多少，系统返回一个非负整数。
   - 查询等级是否达标：询问当前负荷等级是否等于某个值 v，系统返回"是"或"否"。
   - 查询等级波动：询问相较于上一次数值查询或部署操作后的读数，负荷等级变化了多少。系统返回一个整数；若无上次读数则返回提示信息。
   - 查询评估规则：询问当前启用的规则是否为某个特定规则（A、B、C 或 D），系统返回"是"或"否"。

3. 终局声明：当你认为已经推理出正确答案时，提交你的部署方案声明，包括：
   - 你认为的评估规则类型（A、B、C 或 D）
   - 你使用的部署操作次数
   系统会核验：规则是否正确，当前负荷等级是否等于 3，以及你使用的部署次数是否等于该规则下从空产线达到等级 3 的理论最少部署数。

你的目标是：
- 正确识别当前启用的评估规则
- 使当前负荷等级达到 3
- 使用尽可能少的部署操作次数

每次操作只能包含一个标签。请使用以下 XML 格式：

- 部署操作（例如部署工序 3）：
<add>3</add>

- 查询当前负荷等级：
<query_value></query_value>

- 查询等级是否等于某值（例如查询是否等于 2）：
<query_equal>2</query_equal>

- 查询等级波动：
<query_change></query_change>

- 查询评估规则（例如查询是否为规则 A）：
<query_rule>A</query_rule>

- 提交终局声明（例如声明规则为 A，使用了 3 次部署）：
<answer>rule=A, steps=3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's experience an "Intelligent Production Line Process Deployment" simulation system.

The system features five machining process types, labeled 1, 2, 3, 4, 5. Each process can be deployed on the production line an unlimited number of times.

The system state is a multiset represented by a deployment count vector x = (x1, x2, x3, x4, x5), where each xi is the deployment count of that process type (non-negative integer). Initially, all deployment counts are 0.

The system has secretly enabled one of four energy consumption evaluation rules, which remains fixed throughout the deployment process. The target comprehensive load level is T = 3.

Four candidate energy consumption evaluation rules (which one is enabled is hidden):
- Rule A (Process Diversity): The load level equals the number of process types with a deployment count greater than 0.
- Rule B (Coupled Processes): The load level equals the sum of "deployment count divided by 2 rounded down" for all types (representing coupling loss from paired deployments).
- Rule C (Asynchronous Processes): The load level equals the number of process types with an odd deployment count.
- Rule D (Single Process Bottleneck): The load level equals the maximum deployment count among all process types (0 if all are 0).

You can perform the following operations:

1. Deploy operation (changes state, counts as a step): Choose any process type i (1 to 5) and add one instance of that process to the line. The system immediately returns the current load level.

2. Query operation (does not change state, does not count as a step):
   - Query current level: Ask what the current load level is. System returns a non-negative integer.
   - Query level target: Ask whether the current load level equals some value v. System returns "Yes" or "No".
   - Query level fluctuation: Ask how much the load level changed compared to the last numerical query or deploy operation. System returns an integer; if no previous reading exists, returns a notice.
   - Query evaluation rule: Ask whether the currently enabled rule is a specific rule (A, B, C, or D). System returns "Yes" or "No".

3. Final declaration: When you believe you have deduced the correct answer, submit your deployment declaration including:
   - The evaluation rule you believe is active (A, B, C, or D)
   - The number of deploy operations you used
   The system will verify: whether the rule is correct, whether the current load level equals 3, and whether your deploy count equals the theoretical minimum number of deployments needed to reach load level 3 from an empty line under that rule.

Your goal is to:
- Correctly identify the currently enabled evaluation rule
- Make the current load level reach 3
- Use as few deploy operations as possible

Each operation must contain only one tag. Use the following XML format:

- Deploy operation (e.g., deploy process 3):
<add>3</add>

- Query current load level:
<query_value></query_value>

- Query whether level equals something (e.g., query if equals 2):
<query_equal>2</query_equal>

- Query level fluctuation:
<query_change></query_change>

- Query evaluation rule (e.g., query if rule is A):
<query_rule>A</query_rule>

- Submit final declaration (e.g., declare rule is A with 3 deployments):
<answer>rule=A, steps=3</answer>
"""

    contextualized_rule_zh_5 = """\
我们现在来体验一个"法庭证据链推演"模拟系统。

系统设定了五种法定证据类型，记为 1, 2, 3, 4, 5，每种类型可以向法庭无限次提交。

系统状态是一个多重集合，由各类型证据的提交份数向量 x = (x1, x2, x3, x4, x5) 表示，其中每个 xi 是该证据类型的提交份数（非负整数）。初始状态下所有证据提交数都为 0。

系统已秘密启用四种证据采信评估规则之一，该规则在整个推演过程中固定不变。目标效力评级 T = 3。

四种备选证据采信评估规则（具体启用哪一个是隐藏的）：
- 规则 A（证据多样性）：效力评级等于当前提交份数大于 0 的证据种类数量。
- 规则 B（印证证据对）：效力评级等于所有证据类型的"提交份数除以 2 向下取整"之和（即互相印证的成对证据数量）。
- 规则 C（孤证疑点数）：效力评级等于当前提交份数为奇数的证据种类数量（即无法完全配对的孤立证据引发的疑点乘数）。
- 规则 D（主证堆叠度）：效力评级等于所有证据类型中提交份数的最大值（若所有为 0 则评级为 0）。

你可以进行以下操作：

1. 举证操作（会改变状态，计入步数）：选择任一证据类型 i（1 到 5），向法庭提交一份该类型的证据。系统会立即返回当前的效力评级。

2. 查询操作（不改变状态，不计入步数）：
   - 查询当前评级：询问当前的效力评级是多少，系统返回一个非负整数。
   - 查询评级是否达标：询问当前效力评级是否等于某个值 v，系统返回"是"或"否"。
   - 查询评级波动：询问相较于上一次数值查询或举证操作后的读数，效力评级变化了多少。系统返回一个整数；若无上次读数则返回提示信息。
   - 查询评估规则：询问当前启用的规则是否为某个特定规则（A、B、C 或 D），系统返回"是"或"否"。

3. 终局声明：当你认为已经推理出正确答案时，提交你的推演声明，包括：
   - 你认为的评估规则类型（A、B、C 或 D）
   - 你使用的举证操作次数
   系统会核验：规则是否正确，当前效力评级是否等于 3，以及你使用的举证次数是否等于该规则下从零证据达到评级 3 的理论最少举证数。

你的目标是：
- 正确识别当前启用的评估规则
- 使当前效力评级达到 3
- 使用尽可能少的举证操作次数

每次操作只能包含一个标签。请使用以下 XML 格式：

- 举证操作（例如提交证据类型 3）：
<add>3</add>

- 查询当前效力评级：
<query_value></query_value>

- 查询评级是否等于某值（例如查询是否等于 2）：
<query_equal>2</query_equal>

- 查询评级波动：
<query_change></query_change>

- 查询评估规则（例如查询是否为规则 A）：
<query_rule>A</query_rule>

- 提交终局声明（例如声明规则为 A，使用了 3 次举证）：
<answer>rule=A, steps=3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's experience a "Courtroom Evidence Chain Deduction" simulation system.

The system features five statutory evidence types, labeled 1, 2, 3, 4, 5. Each type can be submitted to the court an unlimited number of times.

The system state is a multiset represented by a submission count vector x = (x1, x2, x3, x4, x5), where each xi is the submission count of that evidence type (non-negative integer). Initially, all submission counts are 0.

The system has secretly enabled one of four evidence admissibility evaluation rules, which remains fixed throughout the deduction process. The target efficacy rating is T = 3.

Four candidate evidence admissibility evaluation rules (which one is enabled is hidden):
- Rule A (Evidence Diversity): The efficacy rating equals the number of evidence types with a submission count greater than 0.
- Rule B (Corroborating Pairs): The efficacy rating equals the sum of "submission count divided by 2 rounded down" for all types (representing pairs of mutually corroborating evidence).
- Rule C (Uncorroborated Doubts): The efficacy rating equals the number of evidence types with an odd submission count (representing doubt multipliers caused by isolated, unpaired evidence).
- Rule D (Primary Evidence Stacking): The efficacy rating equals the maximum submission count among all evidence types (0 if all are 0).

You can perform the following operations:

1. Submit operation (changes state, counts as a step): Choose any evidence type i (1 to 5) and submit one piece of that evidence to the court. The system immediately returns the current efficacy rating.

2. Query operation (does not change state, does not count as a step):
   - Query current rating: Ask what the current efficacy rating is. System returns a non-negative integer.
   - Query rating target: Ask whether the current efficacy rating equals some value v. System returns "Yes" or "No".
   - Query rating fluctuation: Ask how much the efficacy rating changed compared to the last numerical query or submit operation. System returns an integer; if no previous reading exists, returns a notice.
   - Query evaluation rule: Ask whether the currently enabled rule is a specific rule (A, B, C, or D). System returns "Yes" or "No".

3. Final declaration: When you believe you have deduced the correct answer, submit your deduction declaration including:
   - The evaluation rule you believe is active (A, B, C, or D)
   - The number of submit operations you used
   The system will verify: whether the rule is correct, whether the current efficacy rating equals 3, and whether your submission count equals the theoretical minimum number of submissions needed to reach efficacy rating 3 from zero evidence under that rule.

Your goal is to:
- Correctly identify the currently enabled evaluation rule
- Make the current efficacy rating reach 3
- Use as few submit operations as possible

Each operation must contain only one tag. Use the following XML format:

- Submit operation (e.g., submit evidence type 3):
<add>3</add>

- Query current efficacy rating:
<query_value></query_value>

- Query whether rating equals something (e.g., query if equals 2):
<query_equal>2</query_equal>

- Query rating fluctuation:
<query_change></query_change>

- Query evaluation rule (e.g., query if rule is A):
<query_rule>A</query_rule>

- Submit final declaration (e.g., declare rule is A with 3 submissions):
<answer>rule=A, steps=3</answer>
"""

    tags = ["answer", "add", "query_value", "query_equal", "query_change", "query_rule"]

    reasoning_type = "溯因推理"
    data_structure = "集合"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"rule": "D", "min_steps": 3},
            2: {"rule": "A", "min_steps": 3},
            3: {"rule": "C", "min_steps": 3},
            4: {"rule": "B", "min_steps": 6},
            5: {"rule": "B", "min_steps": 6},
        },
        "en": {
            1: {"rule": "D", "min_steps": 3},
            2: {"rule": "A", "min_steps": 3},
            3: {"rule": "C", "min_steps": 3},
            4: {"rule": "B", "min_steps": 6},
            5: {"rule": "B", "min_steps": 6},
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
        selected_rule = cfg["rule"]
        min_steps = cfg["min_steps"]

        self.rule_type = selected_rule
        self.min_steps = min_steps
        self.counts = [0, 0, 0, 0, 0]
        self.add_count = 0
        self.last_value = None
        
        self._game_info = {}

    def _compute_statistic(self):
        if self.rule_type == "A":
            return sum(1 for c in self.counts if c > 0)
        elif self.rule_type == "B":
            return sum(c // 2 for c in self.counts)
        elif self.rule_type == "C":
            return sum(1 for c in self.counts if c % 2 == 1)
        elif self.rule_type == "D":
            return max(self.counts) if any(c > 0 for c in self.counts) else 0
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",")]
        ans_dict = {}
        for kv in kv_pairs:
            if "=" in kv:
                k, v = kv.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "rule" not in ans_dict or "steps" not in ans_dict:
            return False
        
        claimed_rule = ans_dict["rule"].upper()
        if claimed_rule != self.rule_type:
            return False
        
        try:
            claimed_steps = int(ans_dict["steps"])
        except (ValueError, TypeError):
            return False
        
        if claimed_steps != self.min_steps:
            return False
        
        current_value = self._compute_statistic()
        if current_value != 3:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            no_prev_msg = "无上次读数"
            invalid_type_msg = "错误：无效的类型编号（必须是1到5）。"
            invalid_rule_msg = "错误：无效的规则标识（必须是A、B、C或D）。"
            invalid_format_msg = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            no_prev_msg = "No previous reading"
            invalid_type_msg = "Error: Invalid type number (must be 1 to 5)."
            invalid_rule_msg = "Error: Invalid rule identifier (must be A, B, C, or D)."
            invalid_format_msg = "Error: Invalid format."

        
        if "add" in parsed_info:
            try:
                type_id = int(parsed_info["add"].strip())
                if type_id < 1 or type_id > 5:
                    return invalid_type_msg
                
                self.counts[type_id - 1] += 1
                self.add_count += 1
                
                current_value = self._compute_statistic()
                self.last_value = current_value
                
                return str(current_value)
            except (ValueError, TypeError):
                return invalid_format_msg
        
        elif "query_value" in parsed_info:
            current_value = self._compute_statistic()
            self.last_value = current_value
            return str(current_value)
        
        elif "query_equal" in parsed_info:
            try:
                target = int(parsed_info["query_equal"].strip())
                current_value = self._compute_statistic()
                return yes_res if current_value == target else no_res
            except (ValueError, TypeError):
                return invalid_format_msg
        
        elif "query_change" in parsed_info:
            if self.last_value is None:
                return no_prev_msg
            
            current_value = self._compute_statistic()
            change = current_value - self.last_value
            return str(change)
        
        elif "query_rule" in parsed_info:
            try:
                queried_rule = parsed_info["query_rule"].strip().upper()
                if queried_rule not in ["A", "B", "C", "D"]:
                    return invalid_rule_msg
                
                return yes_res if queried_rule == self.rule_type else no_res
            except (ValueError, TypeError, AttributeError):
                return invalid_format_msg
        
        else:
            raise ValueError("No valid operation tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            no_prev_msg = "无上次读数"
        else:
            yes_res, no_res = "Yes", "No"
            no_prev_msg = "No previous reading"
            
        if self.rule_type == "A":
            add_seq = [1, 2, 3]
        elif self.rule_type == "B":
            add_seq = [1, 1, 2, 2, 3, 3]
        elif self.rule_type == "C":
            add_seq = [1, 2, 3]
        elif self.rule_type == "D":
            add_seq = [1, 1, 1]
        else:
            add_seq = [1, 2, 3]

        tmp_counts = [0, 0, 0, 0, 0]
        tmp_last_value = None

        def compute_stat(counts):
            if self.rule_type == "A":
                return sum(1 for c in counts if c > 0)
            elif self.rule_type == "B":
                return sum(c // 2 for c in counts)
            elif self.rule_type == "C":
                return sum(1 for c in counts if c % 2 == 1)
            elif self.rule_type == "D":
                return max(counts) if any(c > 0 for c in counts) else 0
            else:
                raise ValueError(f"Unknown rule type: {self.rule_type}")

        for type_id in add_seq:
            tmp_counts[type_id - 1] += 1
            current_value = compute_stat(tmp_counts)
            tmp_last_value = current_value
            results.append({
                "query": f"<add>{type_id}</add>",
                "answer": str(current_value)
            })

        current_value = compute_stat(tmp_counts)
        
        results.append({
            "query": "<query_value></query_value>",
            "answer": str(current_value)
        })
        
        for v in range(6):
            ans = yes_res if current_value == v else no_res
            results.append({
                "query": f"<query_equal>{v}</query_equal>",
                "answer": ans
            })
        
        if tmp_last_value is None:
            change_ans = no_prev_msg
        else:
            change_ans = str(current_value - tmp_last_value)
        
        results.append({
            "query": "<query_change></query_change>",
            "answer": change_ans
        })
        
        for r in ["A", "B", "C", "D"]:
            ans = yes_res if self.rule_type == r else no_res
            results.append({
                "query": f"<query_rule>{r}</query_rule>",
                "answer": ans
            })
            
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            val = int(correct)
            return str(val + 1) if val != 0 else "1"
        except ValueError:
            pass
        
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        
        lower_c = correct.lower()
        if lower_c == "yes":
            return "No" if correct[0].isupper() else "no"
        if lower_c == "no":
            return "Yes" if correct[0].isupper() else "yes"

        return correct + "_WRONG"