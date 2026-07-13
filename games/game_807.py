# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/claude-sonnet-4-5-20250929
# 推理类型: 归纳推理（完全自主总结规律）：从多次反馈的样本中，总结出背后隐藏的规律/模式。例如猜拳游戏，模型需要总结对手出拳的模式。
# 数据结构: 集合：存在一个由N个物体组成的集合，注意他们不存在位置、前后和大小关系。
# 知识点:   替换影响：将某元素替换为另一元素后，满足条件的元素数量如何变化
# ============================================================

from .base import Game
import re


class MultisetActivationRuleGame(Game):

    game_rule_zh = """\
我们现在来玩一个"多重集合激活规则"的推理游戏，规则如下：

游戏设定了一个由 {n} 个元素组成的多重集合，每个元素属于一个且仅一个类型标签（A、B、C）。初始的类型计数向量已被秘密设定，且三者和为 {n}。

存在一个固定但未知的"激活判定规则"：该规则的输出是当前被判定为"激活"的元素总数；该规则仅依赖当前各类型的计数，不依赖元素位置、顺序或个体差异。

你的目标是通过交互推测出这个激活判定规则，并在给定目标值后，通过类型替换操作达到目标激活数。

## 可用的交互操作

你可以反复进行以下操作（每次仅限一个操作）：

1. 查询当前激活数：
<query_activation></query_activation>

2. 查询是否存在某类型可用元素（例如查询类型A）：
<query_exists>A</query_exists>

3. 执行一次类型替换（例如将一枚A替换为B）：
<operation_replace>A,B</operation_replace>
注意：若源类型当前计数为0，则该操作失败，不改变状态。

4. 撤销上一步替换：
<operation_undo></operation_undo>
注意：仅能撤销最近的一步替换；可连续撤销。

5. 宣布你归纳出的规则（用于判定）：
<declare_rule>你的规律假说</declare_rule>
注意：必须是一般性陈述，不依赖当前具体计数。

6. 请求目标激活数（在完成规律归纳后）：
<request_target></request_target>

## 目标与判定

胜利条件（需同时满足）：
1. 规律判定正确：你宣布的规律与隐藏规则一致。
2. 目标达成：在给出的两个目标值下，分别通过尽可能少的替换次数，使当前激活数精确等于目标值。

失败条件：
- 任一目标在替换次数超过限制后仍未达成。
- 累计三次规律宣告被判定为错误。

## 操作格式要求

每次只能包含一个操作标签，严格使用上述XML格式。
"""

    game_rule_en = """\
Let's play a "Multiset Activation Rule" deduction game. Here are the rules:

The game has a multiset of {n} elements, where each element belongs to exactly one type label (A, B, C). The initial type count vector has been secretly set, and the three counts sum to {n}.

There exists a fixed but unknown "activation determination rule": this rule outputs the total number of elements currently determined as "activated"; the rule depends only on the current type counts, not on element positions, order, or individual differences.

Your goal is to infer this activation determination rule through interaction, and after being given target values, achieve the target activation counts through type replacement operations.

## Available Interactive Operations

You can repeatedly perform the following operations (one operation per turn):

1. Query current activation count:
<query_activation></query_activation>

2. Query if at least one element of a type exists (e.g., query type A):
<query_exists>A</query_exists>

3. Execute one type replacement (e.g., replace one A with B):
<operation_replace>A,B</operation_replace>
Note: If the source type's current count is 0, the operation fails and does not change the state.

4. Undo the last replacement:
<operation_undo></operation_undo>
Note: Can only undo the most recent replacement; can undo consecutively.

5. Declare your inferred rule (for judgment):
<declare_rule>Your rule hypothesis</declare_rule>
Note: Must be a general statement, not dependent on current specific counts.

6. Request target activation counts (after completing rule inference):
<request_target></request_target>

## Goals and Judgment

Victory conditions (must satisfy both):
1. Rule judgment correct: Your declared rule matches the hidden rule.
2. Target achievement: For both given target values, achieve the exact target activation count through as few replacements as possible.

Failure conditions:
- Any target is not achieved after exceeding the replacement limit.
- Three rule declarations are judged as incorrect.

## Operation Format Requirements

Only one operation tag per turn, strictly using the above XML format.
"""

    contextualized_rule_zh_1 = """\
欢迎使用“智能交通流管控规则”模拟系统。本系统用于推演不同车型组合下触发道路限流的隐藏规律。

系统设定了一个由 {n} 辆车组成的车队多重集合，每辆车属于一个且仅一个车型标签（A：小型汽车，B：公交车，C：货车）。初始的车型计数向量已被秘密设定，且三者和为 {n}。

存在一个固定但未知的“管控触发判定规则”：该规则的输出是当前被判定为“激活（触发管控）”的车辆总数；该规则仅依赖当前各车型的计数，不依赖车辆位置、顺序或个体差异。

你的目标是通过交互推测出这个管控触发判定规则，并在给定目标激活值后，通过车型替换操作达到目标激活数。

## 可用的交互操作

你可以反复进行以下操作（每次仅限一个操作）：

1. 查询当前激活数：
<query_activation></query_activation>

2. 查询是否存在某车型可用车辆（例如查询车型A）：
<query_exists>A</query_exists>

3. 执行一次车型替换（例如将一辆A替换为B）：
<operation_replace>A,B</operation_replace>
注意：若源车型当前计数为0，则该操作失败，不改变状态。

4. 撤销上一步替换：
<operation_undo></operation_undo>
注意：仅能撤销最近的一步替换；可连续撤销。

5. 宣布你归纳出的规则（用于判定）：
<declare_rule>你的规律假说</declare_rule>
注意：必须是一般性陈述，不依赖当前具体计数。

6. 请求目标激活数（在完成规律归纳后）：
<request_target></request_target>

## 目标与判定

胜利条件（需同时满足）：
1. 规律判定正确：你宣布的规律与隐藏规则一致。
2. 目标达成：在给出的两个目标值下，分别通过尽可能少的替换次数，使当前激活数精确等于目标值。

失败条件：
- 任一目标在替换次数超过限制后仍未达成。
- 累计三次规律宣告被判定为错误。

## 操作格式要求

每次只能包含一个操作标签，严格使用上述XML格式。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Intelligent Traffic Flow Control Rule" simulation system. This system is used to deduce the hidden rules triggering road restrictions under different vehicle type combinations.

The system features a fleet multiset composed of {n} vehicles, where each vehicle belongs to exactly one vehicle type label (A: Car, B: Bus, C: Truck). The initial vehicle type count vector has been secretly set, and the three counts sum to {n}.

There exists a fixed but unknown "control trigger determination rule": this rule outputs the total number of vehicles currently determined as "activated" (triggering traffic control); the rule depends only on the current vehicle type counts, not on vehicle positions, order, or individual differences.

Your goal is to infer this control trigger determination rule through interaction, and after being given target activation values, achieve the exact target activation counts through vehicle type replacement operations.

## Available Interactive Operations

You can repeatedly perform the following operations (one operation per turn):

1. Query current activation count:
<query_activation></query_activation>

2. Query if at least one vehicle of a vehicle type exists (e.g., query vehicle type A):
<query_exists>A</query_exists>

3. Execute one vehicle type replacement (e.g., replace one A with B):
<operation_replace>A,B</operation_replace>
Note: If the source vehicle type's current count is 0, the operation fails and does not change the state.

4. Undo the last replacement:
<operation_undo></operation_undo>
Note: Can only undo the most recent replacement; can undo consecutively.

5. Declare your inferred rule (for judgment):
<declare_rule>Your rule hypothesis</declare_rule>
Note: Must be a general statement, not dependent on current specific counts.

6. Request target activation counts (after completing rule inference):
<request_target></request_target>

## Goals and Judgment

Victory conditions (must satisfy both):
1. Rule judgment correct: Your declared rule matches the hidden rule.
2. Target achievement: For both given target values, achieve the exact target activation count through as few replacements as possible.

Failure conditions:
- Any target is not achieved after exceeding the replacement limit.
- Three rule declarations are judged as incorrect.

## Operation Format Requirements

Only one operation tag per turn, strictly using the above XML format.
"""

    contextualized_rule_zh_2 = """\
欢迎进入“病区医疗资源调度”推演系统。本系统旨在推导不同病情患者组合下，触发重点看护资源的隐藏分配规律。

系统设定了一个由 {n} 名患者组成的病区多重集合，每名患者属于一个且仅一个病情标签（A：轻症，B：重症，C：危重症）。初始的病情计数向量已被秘密设定，且三者和为 {n}。

存在一个固定但未知的“重点看护判定规则”：该规则的输出是当前被判定为“激活（需重点看护）”的患者总数；该规则仅依赖当前各病情的计数，不依赖患者位置、顺序或个体差异。

你的目标是通过交互推测出这个重点看护判定规则，并在给定目标激活值后，通过病情替换（例如转诊）操作达到目标激活数。

## 可用的交互操作

你可以反复进行以下操作（每次仅限一个操作）：

1. 查询当前激活数：
<query_activation></query_activation>

2. 查询是否存在某病情可用患者（例如查询病情A）：
<query_exists>A</query_exists>

3. 执行一次病情替换（例如将一名A替换为B）：
<operation_replace>A,B</operation_replace>
注意：若源病情当前计数为0，则该操作失败，不改变状态。

4. 撤销上一步替换：
<operation_undo></operation_undo>
注意：仅能撤销最近的一步替换；可连续撤销。

5. 宣布你归纳出的规则（用于判定）：
<declare_rule>你的规律假说</declare_rule>
注意：必须是一般性陈述，不依赖当前具体计数。

6. 请求目标激活数（在完成规律归纳后）：
<request_target></request_target>

## 目标与判定

胜利条件（需同时满足）：
1. 规律判定正确：你宣布的规律与隐藏规则一致。
2. 目标达成：在给出的两个目标值下，分别通过尽可能少的替换次数，使当前激活数精确等于目标值。

失败条件：
- 任一目标在替换次数超过限制后仍未达成。
- 累计三次规律宣告被判定为错误。

## 操作格式要求

每次只能包含一个操作标签，严格使用上述XML格式。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Ward Medical Resource Dispatch" simulation system. This system aims to deduce the hidden allocation rules for intensive care resources under different patient acuity combinations.

The system features a ward multiset composed of {n} patients, where each patient belongs to exactly one acuity label (A: Mild, B: Severe, C: Critical). The initial acuity count vector has been secretly set, and the three counts sum to {n}.

There exists a fixed but unknown "intensive care determination rule": this rule outputs the total number of patients currently determined as "activated" (requiring intensive care); the rule depends only on the current acuity counts, not on patient positions, order, or individual differences.

Your goal is to infer this intensive care determination rule through interaction, and after being given target activation values, achieve the exact target activation counts through acuity replacement operations.

## Available Interactive Operations

You can repeatedly perform the following operations (one operation per turn):

1. Query current activation count:
<query_activation></query_activation>

2. Query if at least one patient of an acuity exists (e.g., query acuity A):
<query_exists>A</query_exists>

3. Execute one acuity replacement (e.g., replace one A with B):
<operation_replace>A,B</operation_replace>
Note: If the source acuity's current count is 0, the operation fails and does not change the state.

4. Undo the last replacement:
<operation_undo></operation_undo>
Note: Can only undo the most recent replacement; can undo consecutively.

5. Declare your inferred rule (for judgment):
<declare_rule>Your rule hypothesis</declare_rule>
Note: Must be a general statement, not dependent on current specific counts.

6. Request target activation counts (after completing rule inference):
<request_target></request_target>

## Goals and Judgment

Victory conditions (must satisfy both):
1. Rule judgment correct: Your declared rule matches the hidden rule.
2. Target achievement: For both given target values, achieve the exact target activation count through as few replacements as possible.

Failure conditions:
- Any target is not achieved after exceeding the replacement limit.
- Three rule declarations are judged as incorrect.

## Operation Format Requirements

Only one operation tag per turn, strictly using the above XML format.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“排课与教学资源分配”推演系统。本系统用于探索不同课程类型组合下的资源配额占用规律。

系统设定了一个由 {n} 门课程组成的课表多重集合，每门课程属于一个且仅一个课程标签（A：理科，B：文科，C：体艺）。初始的课程计数向量已被秘密设定，且三者和为 {n}。

存在一个固定但未知的“资源配额判定规则”：该规则的输出是当前被判定为“激活（占用配额）”的课程总数；该规则仅依赖当前各课程类型的计数，不依赖课程位置、顺序或个体差异。

你的目标是通过交互推测出这个资源配额判定规则，并在给定目标激活值后，通过课程类型替换操作达到目标激活数。

## 可用的交互操作

你可以反复进行以下操作（每次仅限一个操作）：

1. 查询当前激活数：
<query_activation></query_activation>

2. 查询是否存在某课程类型可用课程（例如查询课程类型A）：
<query_exists>A</query_exists>

3. 执行一次课程类型替换（例如将一门A替换为B）：
<operation_replace>A,B</operation_replace>
注意：若源课程类型当前计数为0，则该操作失败，不改变状态。

4. 撤销上一步替换：
<operation_undo></operation_undo>
注意：仅能撤销最近的一步替换；可连续撤销。

5. 宣布你归纳出的规则（用于判定）：
<declare_rule>你的规律假说</declare_rule>
注意：必须是一般性陈述，不依赖当前具体计数。

6. 请求目标激活数（在完成规律归纳后）：
<request_target></request_target>

## 目标与判定

胜利条件（需同时满足）：
1. 规律判定正确：你宣布的规律与隐藏规则一致。
2. 目标达成：在给出的两个目标值下，分别通过尽可能少的替换次数，使当前激活数精确等于目标值。

失败条件：
- 任一目标在替换次数超过限制后仍未达成。
- 累计三次规律宣告被判定为错误。

## 操作格式要求

每次只能包含一个操作标签，严格使用上述XML格式。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Course Scheduling and Resource Allocation" simulation system. This system is used to explore the resource quota occupation rules under different course type combinations.

The system features a curriculum multiset composed of {n} courses, where each course belongs to exactly one course type label (A: Science, B: Arts, C: Arts/Sports). The initial course type count vector has been secretly set, and the three counts sum to {n}.

There exists a fixed but unknown "resource quota determination rule": this rule outputs the total number of courses currently determined as "activated" (occupying a resource quota); the rule depends only on the current course type counts, not on course positions, order, or individual differences.

Your goal is to infer this resource quota determination rule through interaction, and after being given target activation values, achieve the exact target activation counts through course type replacement operations.

## Available Interactive Operations

You can repeatedly perform the following operations (one operation per turn):

1. Query current activation count:
<query_activation></query_activation>

2. Query if at least one course of a course type exists (e.g., query course type A):
<query_exists>A</query_exists>

3. Execute one course type replacement (e.g., replace one A with B):
<operation_replace>A,B</operation_replace>
Note: If the source course type's current count is 0, the operation fails and does not change the state.

4. Undo the last replacement:
<operation_undo></operation_undo>
Note: Can only undo the most recent replacement; can undo consecutively.

5. Declare your inferred rule (for judgment):
<declare_rule>Your rule hypothesis</declare_rule>
Note: Must be a general statement, not dependent on current specific counts.

6. Request target activation counts (after completing rule inference):
<request_target></request_target>

## Goals and Judgment

Victory conditions (must satisfy both):
1. Rule judgment correct: Your declared rule matches the hidden rule.
2. Target achievement: For both given target values, achieve the exact target activation count through as few replacements as possible.

Failure conditions:
- Any target is not achieved after exceeding the replacement limit.
- Three rule declarations are judged as incorrect.

## Operation Format Requirements

Only one operation tag per turn, strictly using the above XML format.
"""

    contextualized_rule_zh_4 = """\
欢迎使用“生产批次质检抽样”模拟系统。本系统用于测算不同零件组合下触发动态质检的隐藏规律。

系统设定了一个由 {n} 个零件组成的批次多重集合，每个零件属于一个且仅一个零件标签（A：标准件，B：精密件，C：定制件）。初始的零件计数向量已被秘密设定，且三者和为 {n}。

存在一个固定但未知的“质检激活判定规则”：该规则的输出是当前被判定为“激活（触发质检）”的零件总数；该规则仅依赖当前各零件类型的计数，不依赖零件位置、顺序或个体差异。

你的目标是通过交互推测出这个质检激活判定规则，并在给定目标激活值后，通过零件类型替换操作达到目标激活数。

## 可用的交互操作

你可以反复进行以下操作（每次仅限一个操作）：

1. 查询当前激活数：
<query_activation></query_activation>

2. 查询是否存在某零件类型可用零件（例如查询零件类型A）：
<query_exists>A</query_exists>

3. 执行一次零件类型替换（例如将一个A替换为B）：
<operation_replace>A,B</operation_replace>
注意：若源零件类型当前计数为0，则该操作失败，不改变状态。

4. 撤销上一步替换：
<operation_undo></operation_undo>
注意：仅能撤销最近的一步替换；可连续撤销。

5. 宣布你归纳出的规则（用于判定）：
<declare_rule>你的规律假说</declare_rule>
注意：必须是一般性陈述，不依赖当前具体计数。

6. 请求目标激活数（在完成规律归纳后）：
<request_target></request_target>

## 目标与判定

胜利条件（需同时满足）：
1. 规律判定正确：你宣布的规律与隐藏规则一致。
2. 目标达成：在给出的两个目标值下，分别通过尽可能少的替换次数，使当前激活数精确等于目标值。

失败条件：
- 任一目标在替换次数超过限制后仍未达成。
- 累计三次规律宣告被判定为错误。

## 操作格式要求

每次只能包含一个操作标签，严格使用上述XML格式。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Production Batch Quality Inspection Sampling" simulation system. This system is used to calculate the hidden rules triggering dynamic quality inspection under different part combinations.

The system features a batch multiset composed of {n} parts, where each part belongs to exactly one part type label (A: Standard, B: Precision, C: Custom). The initial part type count vector has been secretly set, and the three counts sum to {n}.

There exists a fixed but unknown "quality inspection activation determination rule": this rule outputs the total number of parts currently determined as "activated" (triggering quality inspection); the rule depends only on the current part type counts, not on part positions, order, or individual differences.

Your goal is to infer this quality inspection activation determination rule through interaction, and after being given target activation values, achieve the exact target activation counts through part type replacement operations.

## Available Interactive Operations

You can repeatedly perform the following operations (one operation per turn):

1. Query current activation count:
<query_activation></query_activation>

2. Query if at least one part of a part type exists (e.g., query part type A):
<query_exists>A</query_exists>

3. Execute one part type replacement (e.g., replace one A with B):
<operation_replace>A,B</operation_replace>
Note: If the source part type's current count is 0, the operation fails and does not change the state.

4. Undo the last replacement:
<operation_undo></operation_undo>
Note: Can only undo the most recent replacement; can undo consecutively.

5. Declare your inferred rule (for judgment):
<declare_rule>Your rule hypothesis</declare_rule>
Note: Must be a general statement, not dependent on current specific counts.

6. Request target activation counts (after completing rule inference):
<request_target></request_target>

## Goals and Judgment

Victory conditions (must satisfy both):
1. Rule judgment correct: Your declared rule matches the hidden rule.
2. Target achievement: For both given target values, achieve the exact target activation count through as few replacements as possible.

Failure conditions:
- Any target is not achieved after exceeding the replacement limit.
- Three rule declarations are judged as incorrect.

## Operation Format Requirements

Only one operation tag per turn, strictly using the above XML format.
"""

    contextualized_rule_zh_5 = """\
欢迎进入“证据链效力评估”推演系统。本系统用于分析不同证据类型组合下，法庭采信效力的隐藏评估规律。

系统设定了一个由 {n} 份证据组成的案卷多重集合，每份证据属于一个且仅一个证据标签（A：书证，B：证人证言，C：物证）。初始的证据计数向量已被秘密设定，且三者和为 {n}。

存在一个固定但未知的“采信效力判定规则”：该规则的输出是当前被判定为“激活（有效采信）”的证据总数；该规则仅依赖当前各证据类型的计数，不依赖证据位置、顺序或个体差异。

你的目标是通过交互推测出这个采信效力判定规则，并在给定目标激活值后，通过证据类型替换操作达到目标激活数。

## 可用的交互操作

你可以反复进行以下操作（每次仅限一个操作）：

1. 查询当前激活数：
<query_activation></query_activation>

2. 查询是否存在某证据类型可用证据（例如查询证据类型A）：
<query_exists>A</query_exists>

3. 执行一次证据类型替换（例如将一份A替换为B）：
<operation_replace>A,B</operation_replace>
注意：若源证据类型当前计数为0，则该操作失败，不改变状态。

4. 撤销上一步替换：
<operation_undo></operation_undo>
注意：仅能撤销最近的一步替换；可连续撤销。

5. 宣布你归纳出的规则（用于判定）：
<declare_rule>你的规律假说</declare_rule>
注意：必须是一般性陈述，不依赖当前具体计数。

6. 请求目标激活数（在完成规律归纳后）：
<request_target></request_target>

## 目标与判定

胜利条件（需同时满足）：
1. 规律判定正确：你宣布的规律与隐藏规则一致。
2. 目标达成：在给出的两个目标值下，分别通过尽可能少的替换次数，使当前激活数精确等于目标值。

失败条件：
- 任一目标在替换次数超过限制后仍未达成。
- 累计三次规律宣告被判定为错误。

## 操作格式要求

每次只能包含一个操作标签，严格使用上述XML格式。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Evidence Chain Validity Assessment" simulation system. This system is used to analyze the hidden assessment rules for court admissibility validity under different evidence type combinations.

The system features a case file multiset composed of {n} evidence items, where each evidence item belongs to exactly one evidence type label (A: Documentary, B: Testimonial, C: Physical). The initial evidence type count vector has been secretly set, and the three counts sum to {n}.

There exists a fixed but unknown "admissibility validity determination rule": this rule outputs the total number of evidence items currently determined as "activated" (validly admitted as evidence); the rule depends only on the current evidence type counts, not on evidence positions, order, or individual differences.

Your goal is to infer this admissibility validity determination rule through interaction, and after being given target activation values, achieve the exact target activation counts through evidence type replacement operations.

## Available Interactive Operations

You can repeatedly perform the following operations (one operation per turn):

1. Query current activation count:
<query_activation></query_activation>

2. Query if at least one evidence item of an evidence type exists (e.g., query evidence type A):
<query_exists>A</query_exists>

3. Execute one evidence type replacement (e.g., replace one A with B):
<operation_replace>A,B</operation_replace>
Note: If the source evidence type's current count is 0, the operation fails and does not change the state.

4. Undo the last replacement:
<operation_undo></operation_undo>
Note: Can only undo the most recent replacement; can undo consecutively.

5. Declare your inferred rule (for judgment):
<declare_rule>Your rule hypothesis</declare_rule>
Note: Must be a general statement, not dependent on current specific counts.

6. Request target activation counts (after completing rule inference):
<request_target></request_target>

## Goals and Judgment

Victory conditions (must satisfy both):
1. Rule judgment correct: Your declared rule matches the hidden rule.
2. Target achievement: For both given target values, achieve the exact target activation count through as few replacements as possible.

Failure conditions:
- Any target is not achieved after exceeding the replacement limit.
- Three rule declarations are judged as incorrect.

## Operation Format Requirements

Only one operation tag per turn, strictly using the above XML format.
"""

    user_prompt_zh = "你可以开始第一次操作了。"
    user_prompt_en = "You can start your first operation now."

    tags = ["query_activation", "query_exists", "operation_replace", "operation_undo", 
            "declare_rule", "request_target", "answer"]

    reasoning_type = "归纳推理"
    data_structure = "集合"

    # 难度配置说明：
    # 1 (简单)     - N=12, 规则: 激活数 = A的数量
    # 2 (中等偏下) - N=12, 规则: 激活数 = B的数量
    # 3 (中等偏上) - N=12, 规则: 激活数 = A + B
    # 4 (较难)     - N=12, 规则: 激活数 = max(A, B)
    # 5 (难)       - N=12, 规则: 激活数 = min(A + B, C * 2)

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 12,
                "initial_counts": {"A": 4, "B": 3, "C": 5},
                "rule_type": "count_A",
                "rule_desc": "激活数等于A类型的元素数量",
                "targets": [6, 2],
                "max_steps": 8,
            },
            2: {
                "n": 12,
                "initial_counts": {"A": 5, "B": 4, "C": 3},
                "rule_type": "count_B",
                "rule_desc": "激活数等于B类型的元素数量",
                "targets": [7, 1],
                "max_steps": 8,
            },
            3: {
                "n": 12,
                "initial_counts": {"A": 3, "B": 4, "C": 5},
                "rule_type": "sum_AB",
                "rule_desc": "激活数等于A类型和B类型的元素数量之和",
                "targets": [10, 4],
                "max_steps": 8,
            },
            4: {
                "n": 12,
                "initial_counts": {"A": 5, "B": 3, "C": 4},
                "rule_type": "max_AB",
                "rule_desc": "激活数等于A类型和B类型的元素数量中的较大值",
                "targets": [6, 4],
                "max_steps": 8,
            },
            5: {
                "n": 12,
                "initial_counts": {"A": 3, "B": 3, "C": 6},
                "rule_type": "min_sum_AB_double_C",
                "rule_desc": "激活数等于A加B的和与C的两倍中的较小值",
                "targets": [8, 10],
                "max_steps": 8,
            },
        },
        "en": {
            1: {
                "n": 12,
                "initial_counts": {"A": 4, "B": 3, "C": 5},
                "rule_type": "count_A",
                "rule_desc": "activation count equals the number of type A elements",
                "targets": [6, 2],
                "max_steps": 8,
            },
            2: {
                "n": 12,
                "initial_counts": {"A": 5, "B": 4, "C": 3},
                "rule_type": "count_B",
                "rule_desc": "activation count equals the number of type B elements",
                "targets": [7, 1],
                "max_steps": 8,
            },
            3: {
                "n": 12,
                "initial_counts": {"A": 3, "B": 4, "C": 5},
                "rule_type": "sum_AB",
                "rule_desc": "activation count equals the sum of type A and type B elements",
                "targets": [10, 4],
                "max_steps": 8,
            },
            4: {
                "n": 12,
                "initial_counts": {"A": 5, "B": 3, "C": 4},
                "rule_type": "max_AB",
                "rule_desc": "activation count equals the maximum of type A and type B element counts",
                "targets": [6, 4],
                "max_steps": 8,
            },
            5: {
                "n": 12,
                "initial_counts": {"A": 3, "B": 3, "C": 6},
                "rule_type": "min_sum_AB_double_C",
                "rule_desc": "activation count equals the minimum of the sum of A and B and twice C",
                "targets": [8, 10],
                "max_steps": 8,
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态"""
        lang = self.config.language
        diff = self.config.difficulty

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        # 初始化计数向量
        self.counts = cfg["initial_counts"].copy()
        self.rule_type = cfg["rule_type"]
        self.rule_desc = cfg["rule_desc"]
        self.targets = cfg["targets"]
        self.max_steps = cfg["max_steps"]
        
        # 操作历史（用于撤销）
        self.history = []
        
        # 规则判定相关
        self.rule_declared = False
        self.rule_correct = False
        self.declare_attempts = 0
        self.max_declare_attempts = 3
        
        # 目标达成相关
        self.targets_requested = False
        self.current_target_index = 0
        self.target_steps = 0

    def _calculate_activation(self):
        """根据规则类型计算当前激活数"""
        if self.rule_type == "count_A":
            return self.counts["A"]
        elif self.rule_type == "count_B":
            return self.counts["B"]
        elif self.rule_type == "sum_AB":
            return self.counts["A"] + self.counts["B"]
        elif self.rule_type == "max_AB":
            return max(self.counts["A"], self.counts["B"])
        elif self.rule_type == "min_sum_AB_double_C":
            return min(self.counts["A"] + self.counts["B"], self.counts["C"] * 2)
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def evaluate(self, parsed_info):
        """评估最终答案。
        本游戏的主要胜利路径在 produce_response 中，但为兼容基类 step() 
        和 Inferencer 的冗余性评测，若所有目标已达成且规则正确则返回 True。
        """
        if self.state.state == "success":
            return True
        # 如果规则已正确判定且所有目标已完成
        if self.rule_correct and self.targets_requested and self.current_target_index >= len(self.targets):
            return True
        return False

    def _check_rule_match(self, declared_rule):
        """检查声明的规则是否与隐藏规则匹配 - 使用数值验证方式"""
        # 策略：尝试从声明中提取一个公式化的描述，然后用多组测试值验证
        # 由于纯文本匹配容易误判，改为关键词匹配 + 辅助数值测试
        declared_lower = declared_rule.lower().strip()
        
        # 定义每种规则的核心关键词模式（更严格）
        if self.rule_type == "count_A":
            # 必须明确只提到 A 类型的数量
            patterns_pos = [
                r'(?:activation|激活)\s*(?:count|数)\s*(?:=|equals|等于|is)\s*(?:the\s+)?(?:number|count|数量)\s*(?:of\s+)?(?:type\s*)?a\b',
                r'(?:只|仅|only)\s*(?:计算|count|统计)\s*(?:type\s*)?a',
                r'(?:activation|激活)\s*=\s*(?:count_?)?a\b',
                r'(?:type\s*)?a\s*(?:的数量|的计数|element)',
            ]
            patterns_neg = [r'\btype\s*b\b', r'\btype\s*c\b', r'b类', r'c类', r'\+', r'sum', r'max', r'min']
            
            has_pos = any(re.search(p, declared_lower) for p in patterns_pos)
            has_neg = any(re.search(p, declared_lower) for p in patterns_neg)
            return has_pos and not has_neg
        
        elif self.rule_type == "count_B":
            patterns_pos = [
                r'(?:activation|激活)\s*(?:count|数)\s*(?:=|equals|等于|is)\s*(?:the\s+)?(?:number|count|数量)\s*(?:of\s+)?(?:type\s*)?b\b',
                r'(?:只|仅|only)\s*(?:计算|count|统计)\s*(?:type\s*)?b',
                r'(?:activation|激活)\s*=\s*(?:count_?)?b\b',
                r'(?:type\s*)?b\s*(?:的数量|的计数|element)',
            ]
            patterns_neg = [r'\btype\s*a\b', r'\btype\s*c\b', r'a类', r'c类', r'\+', r'sum', r'max', r'min']
            
            has_pos = any(re.search(p, declared_lower) for p in patterns_pos)
            has_neg = any(re.search(p, declared_lower) for p in patterns_neg)
            return has_pos and not has_neg
        
        elif self.rule_type == "sum_AB":
            patterns_pos = [
                r'(?:type\s*)?a\s*(?:\+|plus|加|和)\s*(?:type\s*)?b',
                r'(?:type\s*)?b\s*(?:\+|plus|加|和)\s*(?:type\s*)?a',
                r'sum\s*(?:of\s*)?(?:type\s*)?a\s*(?:and|与)\s*(?:type\s*)?b',
                r'a\s*(?:类|类型)?\s*(?:和|与|加)\s*b\s*(?:类|类型)?\s*(?:的)?\s*(?:数量|计数|之和|和)',
            ]
            has_pos = any(re.search(p, declared_lower) for p in patterns_pos)
            return has_pos
        
        elif self.rule_type == "max_AB":
            patterns_pos = [
                r'max\s*\(\s*(?:type\s*)?a\s*,\s*(?:type\s*)?b\s*\)',
                r'(?:maximum|较大值|最大值|larger|greater)\s*(?:of|的)\s*(?:type\s*)?a\s*(?:and|与|和)\s*(?:type\s*)?b',
                r'(?:type\s*)?a\s*(?:和|与|and)\s*(?:type\s*)?b\s*(?:中|的)\s*(?:较大|最大|larger|greater|maximum)',
            ]
            has_pos = any(re.search(p, declared_lower) for p in patterns_pos)
            return has_pos
        
        elif self.rule_type == "min_sum_AB_double_C":
            has_min = re.search(r'min|较小|最小|minimum', declared_lower) is not None
            has_ab_sum = re.search(r'(?:type\s*)?a\s*(?:\+|plus|加|和)\s*(?:type\s*)?b|(?:type\s*)?b\s*(?:\+|plus|加|和)\s*(?:type\s*)?a', declared_lower) is not None
            has_c_double = re.search(r'(?:2\s*\*?\s*(?:type\s*)?c|(?:type\s*)?c\s*\*?\s*2|twice\s*(?:type\s*)?c|(?:type\s*)?c\s*(?:的)?\s*(?:两倍|二倍)|double\s*(?:type\s*)?c)', declared_lower) is not None
            return has_min and has_ab_sum and has_c_double
        
        return False

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        query 字段必须是合法的 XML 标签字符串。
        """
        results = []
        lang = self.config.language

        # 1. query_activation
        activation = self._calculate_activation()
        if lang == "zh":
            ans_act = f"当前激活数={activation}。"
        else:
            ans_act = f"Current activation count={activation}."
        
        results.append({
            "query": "<query_activation></query_activation>", 
            "answer": ans_act
        })

        # 2. query_exists for each type
        for t in ["A", "B", "C"]:
            exists = self.counts[t] > 0
            if lang == "zh":
                ans_exists = "是。" if exists else "否。"
            else:
                ans_exists = "Yes." if exists else "No."
            
            results.append({
                "query": f"<query_exists>{t}</query_exists>",
                "answer": ans_exists
            })

        return results

    def _cf_core_produce(self, parsed_info):
        """根据玩家操作生成响应（原始逻辑）"""
        lang = self.config.language
        
        # 1. 查询当前激活数
        if "query_activation" in parsed_info:
            activation = self._calculate_activation()
            if lang == "zh":
                return f"当前激活数={activation}。"
            else:
                return f"Current activation count={activation}."
        
        # 2. 查询是否存在某类型
        elif "query_exists" in parsed_info:
            type_query = parsed_info["query_exists"].strip().upper()
            if type_query not in ["A", "B", "C"]:
                if lang == "zh":
                    return "错误：类型必须是A、B或C。"
                else:
                    return "Error: Type must be A, B, or C."
            
            exists = self.counts[type_query] > 0
            if lang == "zh":
                return "是。" if exists else "否。"
            else:
                return "Yes." if exists else "No."
        
        # 3. 执行类型替换
        elif "operation_replace" in parsed_info:
            try:
                raw = parsed_info["operation_replace"]
                parts = [x.strip().upper() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                source, target = parts
                
                if source not in ["A", "B", "C"] or target not in ["A", "B", "C"]:
                    raise ValueError
                
                # 检查源类型是否有可用元素
                if self.counts[source] <= 0:
                    activation = self._calculate_activation()
                    if lang == "zh":
                        return f"失败：不存在可替换的{source}。当前激活数={activation}。"
                    else:
                        return f"Failure: No available {source} to replace. Current activation count={activation}."
                
                # 保存历史状态（用于撤销）
                self.history.append(self.counts.copy())
                
                # 执行替换
                self.counts[source] -= 1
                self.counts[target] += 1
                
                # 如果在目标达成阶段，增加步数计数
                if self.targets_requested:
                    self.target_steps += 1
                
                activation = self._calculate_activation()
                
                # 检查是否达到目标
                if self.targets_requested:
                    current_target = self.targets[self.current_target_index]
                    if activation == current_target:
                        # 目标达成
                        if self.current_target_index == len(self.targets) - 1:
                            # 所有目标达成，游戏成功
                            self.state.set_state("success", "all targets achieved")
                            if lang == "zh":
                                return f"成功！所有目标已达成。当前激活数={activation}。"
                            else:
                                return f"Success! All targets achieved. Current activation count={activation}."
                        else:
                            # 进入下一个目标
                            self.current_target_index += 1
                            self.target_steps = 0
                            next_target = self.targets[self.current_target_index]
                            if lang == "zh":
                                return f"成功达到目标{self.current_target_index}！当前激活数={activation}。请继续达到目标{self.current_target_index + 1}={next_target}。"
                            else:
                                return f"Target {self.current_target_index} achieved! Current activation count={activation}. Please achieve target {self.current_target_index + 1}={next_target}."
                    
                    # 检查是否超过步数限制
                    if self.target_steps > self.max_steps:
                        self.state.set_state("failed", "exceeded max steps")
                        if lang == "zh":
                            return f"失败：替换次数超过限制。当前激活数={activation}。"
                        else:
                            return f"Failure: Exceeded replacement limit. Current activation count={activation}."
                
                if lang == "zh":
                    return f"成功。当前激活数={activation}。"
                else:
                    return f"Success. Current activation count={activation}."
                
            except:
                if lang == "zh":
                    return "错误：格式无效。替换操作格式应为 <operation_replace>X,Y</operation_replace>，其中X和Y为A、B或C。"
                else:
                    return "Error: Invalid format. Replacement format should be <operation_replace>X,Y</operation_replace>, where X and Y are A, B, or C."
        
        # 4. 撤销操作
        elif "operation_undo" in parsed_info:
            if not self.history:
                activation = self._calculate_activation()
                if lang == "zh":
                    return f"无法撤销。当前激活数={activation}。"
                else:
                    return f"Cannot undo. Current activation count={activation}."
            
            # 恢复上一个状态
            self.counts = self.history.pop()
            
            # 如果在目标达成阶段，回退步数计数
            if self.targets_requested and getattr(self, "target_steps", 0) > 0:
                self.target_steps -= 1
            
            activation = self._calculate_activation()
            if lang == "zh":
                return f"已撤销。当前激活数={activation}。"
            else:
                return f"Undone. Current activation count={activation}."
        
        # 5. 宣布规则
        elif "declare_rule" in parsed_info:
            if self.rule_correct:
                if lang == "zh":
                    return "规律已经判定正确，无需重复宣布。"
                else:
                    return "Rule already judged correct, no need to declare again."
            
            self.declare_attempts += 1
            declared_rule = parsed_info["declare_rule"]
            
            if self._check_rule_match(declared_rule):
                self.rule_declared = True
                self.rule_correct = True
                if lang == "zh":
                    return "规律判定：正确。"
                else:
                    return "Rule judgment: Correct."
            else:
                if self.declare_attempts >= self.max_declare_attempts:
                    self.state.set_state("failed", "exceeded max declare attempts")
                    if lang == "zh":
                        return "规律判定：错误。已达到最大尝试次数，游戏失败。"
                    else:
                        return "Rule judgment: Incorrect. Maximum attempts reached, game failed."
                
                if lang == "zh":
                    return f"规律判定：错误。剩余尝试次数：{self.max_declare_attempts - self.declare_attempts}。"
                else:
                    return f"Rule judgment: Incorrect. Remaining attempts: {self.max_declare_attempts - self.declare_attempts}."
        
        # 6. 请求目标值
        elif "request_target" in parsed_info:
            if not self.rule_correct:
                if lang == "zh":
                    return "错误：必须先正确归纳出规律，才能请求目标值。"
                else:
                    return "Error: Must correctly infer the rule before requesting target values."
            
            if self.targets_requested:
                if lang == "zh":
                    return "目标值已经给出。"
                else:
                    return "Target values already provided."
            
            self.targets_requested = True
            self.current_target_index = 0
            self.target_steps = 0
            
            if lang == "zh":
                return f"两目标：T1={self.targets[0]}，T2={self.targets[1]}。请先达到T1。"
            else:
                return f"Two targets: T1={self.targets[0]}, T2={self.targets[1]}. Please achieve T1 first."
        
        else:
            raise ValueError("No valid operation tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案"""
        # 1. 尝试替换响应中的数字（如激活数）
        numbers = list(re.finditer(r'(?<==)\s*(\d+)', correct))
        if numbers:
            # 找到 "=数字" 模式，修改最后一个匹配的数字
            match = numbers[-1]
            orig_num = int(match.group(1))
            wrong_num = orig_num + 1
            return correct[:match.start(1)] + str(wrong_num) + correct[match.end(1):]
        
        # 2. 中文："是" ↔ "否"
        if "是。" in correct and "否。" not in correct:
            return correct.replace("是。", "否。")
        if "否。" in correct and "是。" not in correct:
            return correct.replace("否。", "是。")
        
        # 3. 英文："Yes" ↔ "No"
        if re.search(r'\bYes\b', correct):
            return re.sub(r'\bYes\b', 'No', correct)
        if re.search(r'\bNo\b', correct):
            return re.sub(r'\bNo\b', 'Yes', correct)
        if re.search(r'\byes\b', correct):
            return re.sub(r'\byes\b', 'no', correct)
        if re.search(r'\bno\b', correct):
            return re.sub(r'\bno\b', 'yes', correct)

        # 4. 若都不匹配：在字符串末尾追加 "_WRONG"
        return correct + "_WRONG"