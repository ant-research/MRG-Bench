# -*- coding: utf-8 -*-

from .base import Game
import re

class TransitiveOrderGame(Game):

    game_rule_zh = """\
我们来玩一个"传递序推理"游戏，规则如下：

游戏设定了一个包含 {n} 个元素的集合，每个元素用编号 1 到 {n} 标识。这些元素之间存在一个隐藏的严格线性顺序关系（不存在并列、不存在循环）。对于任意两个不同的元素 X 和 Y，要么 X 在 Y 之前，要么 Y 在 X 之前，并且这种顺序关系满足传递性。

我已经指定了两个目标元素：**元素 {target_P}** 和 **元素 {target_Q}**。

你的任务是：在不直接询问这两个目标元素的先后关系的前提下，通过询问其他元素对的先后关系，利用传递性推导出目标元素 {target_P} 和 {target_Q} 的先后顺序，并提供一条完整的证据链证明你的结论。

## 允许的操作

每轮你可以进行以下操作之一：

1. **比较查询**：询问"元素 X 是否在元素 Y 之前？"
   - 约束：X 和 Y 必须是 1 到 {n} 之间的不同编号
   - **禁止直接询问目标元素对**（不能问 {target_P} 和 {target_Q} 的关系）
   - 我会回答"是"或"否"

2. **历史回顾**：请求查看所有已回答过的比较查询及其结果
   - 这不会提供新信息，仅用于回顾

## 提交答案

当你准备好提交答案时，需要提供：
1. **结论**：说明 {target_P} 在 {target_Q} 之前，还是 {target_Q} 在 {target_P} 之前
2. **证据链**：给出一条基于已回答查询的推导链，证明你的结论
   - 证据链必须包含至少 3 条直接比较
   - 每条比较必须来自历史查询的回答
   - 通过传递性逐步连接，形成从一个目标元素到另一个的完整路径

## 格式要求

**比较查询**（询问元素 3 是否在元素 7 之前）：
<query_compare>3,7</query_compare>

**历史回顾**：
<query_history></query_history>

**提交最终答案**（假设结论是 {target_P} 在 {target_Q} 之前，证据链为 {target_P}→5→8→{target_Q}）：
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

注意：
- 结论格式为"A<B"表示 A 在 B 之前
- 证据链用逗号分隔多条比较关系，每条比较用"X<Y"表示 X 在 Y 之前
- 证据链必须形成连续的传递路径
"""

    game_rule_en = """\
Let's play a "Transitive Order Deduction" game. Here are the rules:

The game involves a set of {n} elements, each identified by a number from 1 to {n}. There exists a hidden strict linear order among these elements (no ties, no cycles). For any two different elements X and Y, either X comes before Y or Y comes before X, and this ordering satisfies transitivity.

I have designated two target elements: **Element {target_P}** and **Element {target_Q}**.

Your task is: without directly asking about the relationship between these two target elements, deduce the order of {target_P} and {target_Q} by querying relationships between other element pairs, using transitivity, and provide a complete evidence chain to prove your conclusion.

## Allowed Operations

Each turn you may perform one of the following:

1. **Comparison Query**: Ask "Does element X come before element Y?"
   - Constraint: X and Y must be different numbers between 1 and {n}
   - **Direct comparison of target elements is forbidden** (cannot ask about {target_P} and {target_Q})
   - I will answer "Yes" or "No"

2. **History Review**: Request to see all answered comparison queries and their results
   - This provides no new information, only for review

## Submitting Your Answer

When ready to submit, you must provide:
1. **Conclusion**: State whether {target_P} comes before {target_Q}, or vice versa
2. **Evidence Chain**: Provide a deduction chain based on answered queries to prove your conclusion
   - The chain must contain at least 3 direct comparisons
   - Each comparison must come from historical query answers
   - Must form a complete path from one target element to the other through transitivity

## Format Requirements

**Comparison Query** (asking if element 3 comes before element 7):
<query_compare>3,7</query_compare>

**History Review**:
<query_history></query_history>

**Submit Final Answer** (assuming conclusion is {target_P} before {target_Q}, with chain {target_P}→5→8→{target_Q}):
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

Note:
- Conclusion format "A<B" means A comes before B
- Evidence chain uses comma to separate multiple comparisons, each as "X<Y" meaning X before Y
- The chain must form a continuous transitive path
"""

    contextualized_rule_zh_1 = """\
【交通系统：航班调度】

智能调度系统设定了一个包含 {n} 个关键航班的起降队列，每个航班用编号 1 到 {n} 标识。这些航班之间存在一个隐藏的严格起降顺序（不存在同时起降、不存在循环调度）。对于任意两个不同的航班 X 和 Y，要么 X 在 Y 之前起降，要么 Y 在 X 之前起降，并且这种调度顺序满足传递性。

调度中心已经指定了两个关键航班：**航班 {target_P}** 和 **航班 {target_Q}**。

你的任务是：在不直接向系统询问这两个关键航班先后关系的前提下，通过询问其他航班对的调度先后关系，利用传递性推导出航班 {target_P} 和 {target_Q} 的起降顺序，并提供一条完整的证据链证明你的结论。

## 允许的操作

每轮你可以进行以下操作之一：

1. **比较查询**：询问"航班 X 是否在航班 Y 之前起降？"
   - 约束：X 和 Y 必须是 1 到 {n} 之间的不同编号
   - **禁止直接询问关键航班对**（不能问 {target_P} 和 {target_Q} 的关系）
   - 系统会回答"是"或"否"

2. **历史回顾**：请求查看所有已回答过的调度查询及其结果
   - 这不会提供新信息，仅用于回顾

## 提交答案

当你准备好提交答案时，需要提供：
1. **结论**：说明 {target_P} 在 {target_Q} 之前起降，还是 {target_Q} 在 {target_P} 之前起降
2. **证据链**：给出一条基于已回答查询的推导链，证明你的调度结论
   - 证据链必须包含至少 3 条直接比较
   - 每条比较必须来自历史查询的回答
   - 通过传递性逐步连接，形成从一个关键航班到另一个的完整路径

## 格式要求

**比较查询**（询问航班 3 是否在航班 7 之前起降）：
<query_compare>3,7</query_compare>

**历史回顾**：
<query_history></query_history>

**提交最终答案**（假设结论是 {target_P} 在 {target_Q} 之前起降，证据链为 {target_P}→5→8→{target_Q}）：
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

注意：
- 结论格式为"A<B"表示 航班 A 在 航班 B 之前起降
- 证据链用逗号分隔多条比较关系，每条比较用"X<Y"表示 航班 X 在 航班 Y 之前起降
- 证据链必须形成连续的传递路径
"""

    contextualized_rule_en_1 = """\
[Traffic System: Flight Scheduling]

The intelligent scheduling system has set a takeoff and landing queue containing {n} key flights, each identified by a number from 1 to {n}. There exists a hidden strict scheduling order among these flights (no simultaneous takeoffs/landings, no cycles). For any two different flights X and Y, either X takes off before Y or Y takes off before X, and this scheduling order satisfies transitivity.

The control center has designated two key flights: **Flight {target_P}** and **Flight {target_Q}**.

Your task is: without directly asking the system about the relationship between these two key flights, deduce the order of Flight {target_P} and Flight {target_Q} by querying relationships between other flight pairs, using transitivity, and provide a complete evidence chain to prove your conclusion.

## Allowed Operations

Each turn you may perform one of the following:

1. **Comparison Query**: Ask "Does flight X take off before flight Y?"
   - Constraint: X and Y must be different numbers between 1 and {n}
   - **Direct comparison of key flights is forbidden** (cannot ask about {target_P} and {target_Q})
   - The system will answer "Yes" or "No"

2. **History Review**: Request to see all answered scheduling queries and their results
   - This provides no new information, only for review

## Submitting Your Answer

When ready to submit, you must provide:
1. **Conclusion**: State whether Flight {target_P} takes off before Flight {target_Q}, or vice versa
2. **Evidence Chain**: Provide a deduction chain based on answered queries to prove your conclusion
   - The chain must contain at least 3 direct comparisons
   - Each comparison must come from historical query answers
   - Must form a complete path from one key flight to the other through transitivity

## Format Requirements

**Comparison Query** (asking if flight 3 takes off before flight 7):
<query_compare>3,7</query_compare>

**History Review**:
<query_history></query_history>

**Submit Final Answer** (assuming conclusion is {target_P} before {target_Q}, with chain {target_P}→5→8→{target_Q}):
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

Note:
- Conclusion format "A<B" means Flight A takes off before Flight B
- Evidence chain uses comma to separate multiple comparisons, each as "X<Y" meaning Flight X before Flight Y
- The chain must form a continuous transitive path
"""

    contextualized_rule_zh_2 = """\
【医疗系统：患者治疗优先级队列】

医院急诊分诊系统设定了一个包含 {n} 名患者的等待队列，每位患者用编号 1 到 {n} 标识。这些患者之间存在一个隐藏的严格治疗优先级顺序（不存在同等优先级、不存在循环依赖）。对于任意两名不同的患者 X 和 Y，要么 X 的优先级高于 Y，要么 Y 的优先级高于 X，并且这种优先级排序满足传递性。

主治医师已经指定了两名需要特别关注的患者：**患者 {target_P}** 和 **患者 {target_Q}**。

你的任务是：在不直接向系统询问这两名患者优先级关系的前提下，通过询问其他患者对的优先级关系，利用传递性推导出患者 {target_P} 和 {target_Q} 的真实治疗优先级顺序，并提供一条完整的证据链证明你的诊断结论。

## 允许的操作

每轮你可以进行以下操作之一：

1. **比较查询**：询问"患者 X 的优先级是否高于患者 Y？"
   - 约束：X 和 Y 必须是 1 到 {n} 之间的不同编号
   - **禁止直接询问关键患者对**（不能问 {target_P} 和 {target_Q} 的关系）
   - 分诊系统会回答"是"或"否"

2. **历史回顾**：请求查看所有已回答过的优先级查询及其结果
   - 这不会提供新信息，仅用于回顾

## 提交答案

当你准备好提交答案时，需要提供：
1. **结论**：说明 患者 {target_P} 优先级是否高于 患者 {target_Q}，反之亦然
2. **证据链**：给出一条基于已回答查询的推导链，证明你的排程结论
   - 证据链必须包含至少 3 条直接比较
   - 每条比较必须来自历史查询的回答
   - 通过传递性逐步连接，形成从一名关键患者到另一名的完整路径

## 格式要求

**比较查询**（询问患者 3 优先级是否高于患者 7）：
<query_compare>3,7</query_compare>

**历史回顾**：
<query_history></query_history>

**提交最终答案**（假设结论是 {target_P} 优先级高于 {target_Q}，证据链为 {target_P}→5→8→{target_Q}）：
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

注意：
- 结论格式为"A<B"表示 患者 A 的优先级高于 患者 B
- 证据链用逗号分隔多条比较关系，每条比较用"X<Y"表示 患者 X 的优先级高于 患者 Y
- 证据链必须形成连续的传递路径
"""

    contextualized_rule_en_2 = """\
[Medical System: Patient Priority Queue]

The hospital's emergency triage system has set a waiting queue containing {n} patients, each identified by a number from 1 to {n}. There exists a hidden strict treatment priority order among these patients (no equal priorities, no cycles). For any two different patients X and Y, either X has a higher priority than Y, or Y has a higher priority than X, and this priority ordering satisfies transitivity.

The attending physician has designated two patients requiring special attention: **Patient {target_P}** and **Patient {target_Q}**.

Your task is: without directly asking the system about the relationship between these two critical patients, deduce the priority order of Patient {target_P} and Patient {target_Q} by querying relationships between other patient pairs, using transitivity, and provide a complete evidence chain to prove your triage conclusion.

## Allowed Operations

Each turn you may perform one of the following:

1. **Comparison Query**: Ask "Does patient X have a higher priority than patient Y?"
   - Constraint: X and Y must be different numbers between 1 and {n}
   - **Direct comparison of critical patients is forbidden** (cannot ask about {target_P} and {target_Q})
   - The triage system will answer "Yes" or "No"

2. **History Review**: Request to see all answered priority queries and their results
   - This provides no new information, only for review

## Submitting Your Answer

When ready to submit, you must provide:
1. **Conclusion**: State whether Patient {target_P} has a higher priority than Patient {target_Q}, or vice versa
2. **Evidence Chain**: Provide a deduction chain based on answered queries to prove your conclusion
   - The chain must contain at least 3 direct comparisons
   - Each comparison must come from historical query answers
   - Must form a complete path from one critical patient to the other through transitivity

## Format Requirements

**Comparison Query** (asking if patient 3 has a higher priority than patient 7):
<query_compare>3,7</query_compare>

**History Review**:
<query_history></query_history>

**Submit Final Answer** (assuming conclusion is {target_P} higher than {target_Q}, with chain {target_P}→5→8→{target_Q}):
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

Note:
- Conclusion format "A<B" means Patient A has a higher priority than Patient B
- Evidence chain uses comma to separate multiple comparisons, each as "X<Y" meaning Patient X has higher priority than Patient Y
- The chain must form a continuous transitive path
"""

    contextualized_rule_zh_3 = """\
【教育系统：知识图谱先修路径】

课程教务系统配置了一个包含 {n} 个核心知识模块的学习路径图，每个模块用编号 1 到 {n} 标识。这些知识模块之间存在一个隐藏的严格先修顺序（不存在平行教学、不存在循环依赖）。对于任意两个不同的模块 X 和 Y，要么 X 必须在 Y 之前教授，要么 Y 必须在 X 之前教授，并且这种教学先后关系满足传递性。

教研组已经指定了两个关键知识模块：**模块 {target_P}** 和 **模块 {target_Q}**。

你的任务是：在不直接向系统询问这两个关键模块先后关系的前提下，通过询问其他知识模块对的教学先后关系，利用传递性推导出模块 {target_P} 和 {target_Q} 的正确教学顺序，并提供一条完整的证据链证明你的课程编排结论。

## 允许的操作

每轮你可以进行以下操作之一：

1. **比较查询**：询问"模块 X 是否在模块 Y 之前教授？"
   - 约束：X 和 Y 必须是 1 到 {n} 之间的不同编号
   - **禁止直接询问关键模块对**（不能问 {target_P} 和 {target_Q} 的关系）
   - 系统会回答"是"或"否"

2. **历史回顾**：请求查看所有已回答过的先修查询及其结果
   - 这不会提供新信息，仅用于回顾

## 提交答案

当你准备好提交答案时，需要提供：
1. **结论**：说明 模块 {target_P} 是否在 模块 {target_Q} 之前教授，反之亦然
2. **证据链**：给出一条基于已回答查询的推导链，证明你的教研结论
   - 证据链必须包含至少 3 条直接比较
   - 每条比较必须来自历史查询的回答
   - 通过传递性逐步连接，形成从一个关键模块到另一个的完整教学路径

## 格式要求

**比较查询**（询问模块 3 是否在模块 7 之前教授）：
<query_compare>3,7</query_compare>

**历史回顾**：
<query_history></query_history>

**提交最终答案**（假设结论是 {target_P} 在 {target_Q} 之前教授，证据链为 {target_P}→5→8→{target_Q}）：
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

注意：
- 结论格式为"A<B"表示 模块 A 必须在 模块 B 之前教授
- 证据链用逗号分隔多条比较关系，每条比较用"X<Y"表示 模块 X 在 模块 Y 之前教授
- 证据链必须形成连续的传递路径
"""

    contextualized_rule_en_3 = """\
[Education System: Prerequisite Knowledge Path]

The academic administration system has configured a learning path graph containing {n} core knowledge modules, each identified by a number from 1 to {n}. There exists a hidden strict prerequisite order among these modules (no parallel teaching, no cyclical dependencies). For any two different modules X and Y, either X must be taught before Y, or Y must be taught before X, and this teaching order satisfies transitivity.

The teaching research group has designated two critical modules: **Module {target_P}** and **Module {target_Q}**.

Your task is: without directly asking the system about the relationship between these two critical modules, deduce the correct teaching order of Module {target_P} and Module {target_Q} by querying relationships between other module pairs, using transitivity, and provide a complete evidence chain to prove your curriculum conclusion.

## Allowed Operations

Each turn you may perform one of the following:

1. **Comparison Query**: Ask "Is module X taught before module Y?"
   - Constraint: X and Y must be different numbers between 1 and {n}
   - **Direct comparison of critical modules is forbidden** (cannot ask about {target_P} and {target_Q})
   - The system will answer "Yes" or "No"

2. **History Review**: Request to see all answered prerequisite queries and their results
   - This provides no new information, only for review

## Submitting Your Answer

When ready to submit, you must provide:
1. **Conclusion**: State whether Module {target_P} is taught before Module {target_Q}, or vice versa
2. **Evidence Chain**: Provide a deduction chain based on answered queries to prove your conclusion
   - The chain must contain at least 3 direct comparisons
   - Each comparison must come from historical query answers
   - Must form a complete path from one critical module to the other through transitivity

## Format Requirements

**Comparison Query** (asking if module 3 is taught before module 7):
<query_compare>3,7</query_compare>

**History Review**:
<query_history></query_history>

**Submit Final Answer** (assuming conclusion is {target_P} before {target_Q}, with chain {target_P}→5→8→{target_Q}):
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

Note:
- Conclusion format "A<B" means Module A must be taught before Module B
- Evidence chain uses comma to separate multiple comparisons, each as "X<Y" meaning Module X is taught before Module Y
- The chain must form a continuous transitive path
"""

    contextualized_rule_zh_4 = """\
【工业制造：流水线工序排程】

智能制造系统设定了一个包含 {n} 个标准加工工序的装配流水线，每个工序用编号 1 到 {n} 标识。这些工序之间存在一个隐藏的严格执行先后顺序（不存在并行工序、不存在循环依赖）。对于任意两个不同的工序 X 和 Y，要么 X 在 Y 之前执行，要么 Y 在 X 之前执行，并且这种工艺排序满足传递性。

生产主管已经指定了两个关键节点工序：**工序 {target_P}** 和 **工序 {target_Q}**。

你的任务是：在不直接向系统询问这两个关键工序先后关系的前提下，通过询问其他工序对的执行先后关系，利用传递性推导出工序 {target_P} 和 {target_Q} 的正确排程顺序，并提供一条完整的证据链证明你的排产结论。

## 允许的操作

每轮你可以进行以下操作之一：

1. **比较查询**：询问"工序 X 是否在工序 Y 之前执行？"
   - 约束：X 和 Y 必须是 1 到 {n} 之间的不同编号
   - **禁止直接询问关键工序对**（不能问 {target_P} 和 {target_Q} 的关系）
   - 控制系统会回答"是"或"否"

2. **历史回顾**：请求查看所有已回答过的排程查询及其结果
   - 这不会提供新信息，仅用于回顾

## 提交答案

当你准备好提交答案时，需要提供：
1. **结论**：说明 工序 {target_P} 是否在 工序 {target_Q} 之前执行，反之亦然
2. **证据链**：给出一条基于已回答查询的推导链，证明你的排程结论
   - 证据链必须包含至少 3 条直接比较
   - 每条比较必须来自历史查询的回答
   - 通过传递性逐步连接，形成从一个关键工序到另一个的完整加工路径

## 格式要求

**比较查询**（询问工序 3 是否在工序 7 之前执行）：
<query_compare>3,7</query_compare>

**历史回顾**：
<query_history></query_history>

**提交最终答案**（假设结论是 {target_P} 在 {target_Q} 之前执行，证据链为 {target_P}→5→8→{target_Q}）：
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

注意：
- 结论格式为"A<B"表示 工序 A 在 工序 B 之前执行
- 证据链用逗号分隔多条比较关系，每条比较用"X<Y"表示 工序 X 在 工序 Y 之前执行
- 证据链必须形成连续的传递路径
"""

    contextualized_rule_en_4 = """\
[Manufacturing: Assembly Line Process Scheduling]

The intelligent manufacturing system has set an assembly line containing {n} standard processing steps, each identified by a number from 1 to {n}. There exists a hidden strict execution order among these steps (no parallel processing, no cyclical dependencies). For any two different steps X and Y, either X is executed before Y, or Y is executed before X, and this process sequencing satisfies transitivity.

The production supervisor has designated two critical node steps: **Step {target_P}** and **Step {target_Q}**.

Your task is: without directly asking the system about the relationship between these two critical steps, deduce the correct scheduling order of Step {target_P} and Step {target_Q} by querying relationships between other step pairs, using transitivity, and provide a complete evidence chain to prove your production scheduling conclusion.

## Allowed Operations

Each turn you may perform one of the following:

1. **Comparison Query**: Ask "Is step X executed before step Y?"
   - Constraint: X and Y must be different numbers between 1 and {n}
   - **Direct comparison of critical steps is forbidden** (cannot ask about {target_P} and {target_Q})
   - The control system will answer "Yes" or "No"

2. **History Review**: Request to see all answered scheduling queries and their results
   - This provides no new information, only for review

## Submitting Your Answer

When ready to submit, you must provide:
1. **Conclusion**: State whether Step {target_P} is executed before Step {target_Q}, or vice versa
2. **Evidence Chain**: Provide a deduction chain based on answered queries to prove your conclusion
   - The chain must contain at least 3 direct comparisons
   - Each comparison must come from historical query answers
   - Must form a complete path from one critical step to the other through transitivity

## Format Requirements

**Comparison Query** (asking if step 3 is executed before step 7):
<query_compare>3,7</query_compare>

**History Review**:
<query_history></query_history>

**Submit Final Answer** (assuming conclusion is {target_P} before {target_Q}, with chain {target_P}→5→8→{target_Q}):
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

Note:
- Conclusion format "A<B" means Step A is executed before Step B
- Evidence chain uses comma to separate multiple comparisons, each as "X<Y" meaning Step X is executed before Step Y
- The chain must form a continuous transitive path
"""

    contextualized_rule_zh_5 = """\
【司法系统：案件事实时间线重构】

案件取证系统记录了包含 {n} 个关键事件的证据链条，每个案件事件用编号 1 到 {n} 标识。这些事件之间存在一个隐藏的严格发生时间顺序（不存在同时发生、不存在时间逻辑闭环）。对于任意两个不同的事件 X 和 Y，要么 X 发生在 Y 之前，要么 Y 发生在 X 之前，并且这种时间线顺序满足传递性。

法官已经指定了两个决定定罪的关键事件：**事件 {target_P}** 和 **事件 {target_Q}**。

你的任务是：在不直接向系统询问这两个关键事件先后关系的前提下，通过询问其他案件事件对的时间先后关系，利用传递性推导出事件 {target_P} 和 {target_Q} 的客观发生顺序，并提供一条完整的证据链证明你的司法时间线结论。

## 允许的操作

每轮你可以进行以下操作之一：

1. **比较查询**：询问"事件 X 是否发生在事件 Y 之前？"
   - 约束：X 和 Y 必须是 1 到 {n} 之间的不同编号
   - **禁止直接询问关键事件对**（不能问 {target_P} 和 {target_Q} 的关系）
   - 证物系统会回答"是"或"否"

2. **历史回顾**：请求查看所有已回答过的时间线查询及其结果
   - 这不会提供新信息，仅用于回顾

## 提交答案

当你准备好提交答案时，需要提供：
1. **结论**：说明 事件 {target_P} 是否发生在 事件 {target_Q} 之前，反之亦然
2. **证据链**：给出一条基于已回答查询的推导链，证明你的时间线重构结论
   - 证据链必须包含至少 3 条直接比较
   - 每条比较必须来自历史查询的回答
   - 通过传递性逐步连接，形成从一个关键事件到另一个的完整发生路径

## 格式要求

**比较查询**（询问事件 3 是否发生在事件 7 之前）：
<query_compare>3,7</query_compare>

**历史回顾**：
<query_history></query_history>

**提交最终答案**（假设结论是 {target_P} 发生在 {target_Q} 之前，证据链为 {target_P}→5→8→{target_Q}）：
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

注意：
- 结论格式为"A<B"表示 事件 A 发生在 事件 B 之前
- 证据链用逗号分隔多条比较关系，每条比较用"X<Y"表示 事件 X 发生在 事件 Y 之前
- 证据链必须形成连续的传递路径
"""

    contextualized_rule_en_5 = """\
[Judicial System: Case Timeline Reconstruction]

The forensic evidence system has recorded an evidence chain containing {n} key case events, each identified by a number from 1 to {n}. There exists a hidden strict chronological order among these events (no simultaneous occurrences, no temporal paradoxes). For any two different events X and Y, either X occurred before Y, or Y occurred before X, and this timeline ordering satisfies transitivity.

The judge has designated two critical events decisive for the verdict: **Event {target_P}** and **Event {target_Q}**.

Your task is: without directly asking the system about the relationship between these two critical events, deduce the objective chronological order of Event {target_P} and Event {target_Q} by querying relationships between other event pairs, using transitivity, and provide a complete evidence chain to prove your judicial timeline conclusion.

## Allowed Operations

Each turn you may perform one of the following:

1. **Comparison Query**: Ask "Did event X occur before event Y?"
   - Constraint: X and Y must be different numbers between 1 and {n}
   - **Direct comparison of critical events is forbidden** (cannot ask about {target_P} and {target_Q})
   - The forensics system will answer "Yes" or "No"

2. **History Review**: Request to see all answered timeline queries and their results
   - This provides no new information, only for review

## Submitting Your Answer

When ready to submit, you must provide:
1. **Conclusion**: State whether Event {target_P} occurred before Event {target_Q}, or vice versa
2. **Evidence Chain**: Provide a deduction chain based on answered queries to prove your conclusion
   - The chain must contain at least 3 direct comparisons
   - Each comparison must come from historical query answers
   - Must form a complete path from one critical event to the other through transitivity

## Format Requirements

**Comparison Query** (asking if event 3 occurred before event 7):
<query_compare>3,7</query_compare>

**History Review**:
<query_history></query_history>

**Submit Final Answer** (assuming conclusion is {target_P} before {target_Q}, with chain {target_P}→5→8→{target_Q}):
<answer>conclusion={target_P}<{target_Q}, chain={target_P}<5,5<8,8<{target_Q}</answer>

Note:
- Conclusion format "A<B" means Event A occurred before Event B
- Evidence chain uses comma to separate multiple comparisons, each as "X<Y" meaning Event X occurred before Event Y
- The chain must form a continuous transitive path
"""

    tags = ["answer", "query_compare", "query_history"]
    
    reasoning_type = "演绎推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 7,
                "order": "1,3,5,2,7,4,6",  # 隐藏的全序
                "target_P": "1",
                "target_Q": "7",
                # 最短路径示例: 1<3, 3<5, 5<7 (3步)
            },
            2: {
                "n": 8,
                "order": "2,5,1,7,3,8,4,6",
                "target_P": "2",
                "target_Q": "8",
                # 最短路径示例: 2<5, 5<1, 1<8 (3步)
            },
            3: {
                "n": 9,
                "order": "3,1,6,4,8,2,9,5,7",
                "target_P": "3",
                "target_Q": "9",
                # 最短路径示例: 3<1, 1<6, 6<4, 4<9 (4步)
            },
            4: {
                "n": 10,
                "order": "5,2,8,1,9,3,7,10,4,6",
                "target_P": "5",
                "target_Q": "10",
                # 最短路径示例: 5<2, 2<8, 8<1, 1<10 (4步)
            },
            5: {
                "n": 10,
                "order": "4,7,1,9,5,2,10,8,3,6",
                "target_P": "4",
                "target_Q": "6",
                # 最短路径示例: 4<7, 7<1, 1<9, 9<5, 5<6 (5步)
            },
        },
        "en": {
            1: {
                "n": 7,
                "order": "1,3,5,2,7,4,6",
                "target_P": "1",
                "target_Q": "7",
            },
            2: {
                "n": 8,
                "order": "2,5,1,7,3,8,4,6",
                "target_P": "2",
                "target_Q": "8",
            },
            3: {
                "n": 9,
                "order": "3,1,6,4,8,2,9,5,7",
                "target_P": "3",
                "target_Q": "9",
            },
            4: {
                "n": 10,
                "order": "5,2,8,1,9,3,7,10,4,6",
                "target_P": "5",
                "target_Q": "10",
            },
            5: {
                "n": 10,
                "order": "4,7,1,9,5,2,10,8,3,6",
                "target_P": "4",
                "target_Q": "6",
            },
        },
    }

    def __init__(self, config):
        # 先初始化查询历史，再调用父类初始化
        self.query_history = []
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：设置隐藏顺序、目标元素"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 强制转为整数，防止类型不一致

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        self._game_info["target_P"] = cfg["target_P"]
        self._game_info["target_Q"] = cfg["target_Q"]
        
        # 解析隐藏的线性顺序
        order_list = [x.strip() for x in cfg["order"].split(",")]
        self.order_map = {}  # element -> position
        for pos, elem in enumerate(order_list):
            self.order_map[elem] = pos
        
        self.target_P = cfg["target_P"]
        self.target_Q = cfg["target_Q"]
        self.query_history = []  # 记录所有查询历史

    def _is_before(self, x, y):
        """判断元素 x 是否在元素 y 之前"""
        return self.order_map[x] < self.order_map[y]

    def _is_valid_element(self, elem):
        """检查元素是否有效"""
        return elem in self.order_map

    def evaluate(self, parsed_info):
        """评估最终答案的正确性"""
        raw_ans = parsed_info["answer"]
        
        try:
            # 解析答案格式: conclusion=A<B, chain=X<Y,Y<Z,...
            # 先找 conclusion= 和 chain= 的位置
            conclusion_match = re.search(r'conclusion\s*=\s*(\S+)', raw_ans)
            chain_match = re.search(r'chain\s*=\s*(.+)', raw_ans)
            
            if not conclusion_match or not chain_match:
                return False
            
            conclusion = conclusion_match.group(1).strip().rstrip(',')
            chain_str = chain_match.group(1).strip()
            
            # 检查结论格式: A<B
            if "<" not in conclusion:
                return False
            first, second = [x.strip() for x in conclusion.split("<", 1)]
            
            # 验证结论涉及的是目标元素
            if not ({first, second} == {self.target_P, self.target_Q}):
                return False
            
            # 检查结论是否正确
            conclusion_correct = False
            if first == self.target_P and second == self.target_Q:
                conclusion_correct = self._is_before(self.target_P, self.target_Q)
            elif first == self.target_Q and second == self.target_P:
                conclusion_correct = self._is_before(self.target_Q, self.target_P)
            else:
                return False
            
            if not conclusion_correct:
                return False
            
            # 解析证据链: X<Y,Y<Z,Z<W
            chain_parts = [x.strip() for x in chain_str.split(",")]
            if len(chain_parts) < 3:  # 至少需要3条比较
                return False
            
            # 验证证据链的每一步——直接用 order_map 验证而非依赖 query_history
            chain_elements = []
            for comparison in chain_parts:
                if "<" not in comparison:
                    return False
                a, b = [x.strip() for x in comparison.split("<", 1)]
                
                # 检查元素是否有效
                if not self._is_valid_element(a) or not self._is_valid_element(b):
                    return False
                
                # 检查比较关系是否正确（根据真实顺序）
                if not self._is_before(a, b):
                    return False
                
                chain_elements.append((a, b))
            
            # 验证证据链的连续性（传递性）
            for i in range(len(chain_elements) - 1):
                if chain_elements[i][1] != chain_elements[i + 1][0]:
                    return False
            
            # 验证证据链的起点和终点与结论一致
            if chain_elements[0][0] != first or chain_elements[-1][1] != second:
                return False
            
            return True
            
        except Exception:
            return False

    def _cf_core_produce(self, parsed_info):
        """原始的响应生成逻辑"""
        lang = self.config.language
        yes_res = "是" if lang == "zh" else "Yes"
        no_res = "否" if lang == "zh" else "No"
        error_invalid = "无效问题：" if lang == "zh" else "Invalid query: "
        error_forbidden = "禁止直接比较目标元素。" if lang == "zh" else "Direct comparison of target elements is forbidden."
        error_format = "格式错误或元素不存在。" if lang == "zh" else "Format error or element does not exist."
        
        # 处理历史回顾请求
        if "query_history" in parsed_info:
            if not self.query_history:
                return "暂无查询历史。" if lang == "zh" else "No query history yet."
            
            history_lines = []
            for idx, ((x, y), result) in enumerate(self.query_history, 1):
                res_text = yes_res if result else no_res
                if lang == "zh":
                    history_lines.append(f"{idx}. 元素 {x} 是否在元素 {y} 之前？ 答：{res_text}")
                else:
                    history_lines.append(f"{idx}. Does element {x} come before element {y}? Answer: {res_text}")
            
            return "\n".join(history_lines)
        
        # 处理比较查询
        if "query_compare" in parsed_info:
            try:
                raw = parsed_info["query_compare"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_invalid + error_format
                
                x, y = parts[0], parts[1]
                
                # 检查元素是否有效
                if not self._is_valid_element(x) or not self._is_valid_element(y):
                    return error_invalid + error_format
                
                # 检查是否相同
                if x == y:
                    return error_invalid + ("元素不能相同。" if lang == "zh" else "Elements must be different.")
                
                # 检查是否直接比较目标元素
                if {x, y} == {self.target_P, self.target_Q}:
                    return error_invalid + error_forbidden
                
                # 执行比较
                result = self._is_before(x, y)
                self.query_history.append(((x, y), result))
                
                return yes_res if result else no_res
                
            except Exception as e:
                return error_invalid + error_format
        
        raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list:
        queries = []
        n        = self._game_info["n"]
        target_P = str(self._game_info["target_P"])
        target_Q = str(self._game_info["target_Q"])
        lang     = self.config.language
        yes_res  = "是" if lang == "zh" else "Yes"
        no_res   = "否" if lang == "zh" else "No"

        elements = [str(i) for i in range(1, n + 1)]

        for x in elements:
            for y in elements:
                if x == y:
                    continue
                # 禁止直接比较目标元素对
                if {x, y} == {target_P, target_Q}:
                    continue
                ans = yes_res if self._is_before(x, y) else no_res
                queries.append({
                    "query":  f"<query_compare>{x},{y}</query_compare>",
                    "answer": ans,
                })

        return queries

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:  # en
            # 忽略大小写，保持原始大小写风格
            if correct.lower() == "yes":
                return "No" if correct[0].isupper() else "no"
            elif correct.lower() == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        return correct + "_WRONG"