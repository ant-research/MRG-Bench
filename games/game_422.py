from .base import Game
import random

class OrderInferenceGame(Game):
    reasoning_type = "溯因推理"
    data_structure = "序列"

    game_rule_zh = """\
我们现在来玩一个"序列推理"游戏，规则如下：

游戏设定了一个长度为 8 的全序序列，元素集合为 S = {{F, L, A, B, C, D, E, G}}。
每个元素都有一个唯一的位置编号（1到8），其中已知：
- F 的位置是 1（最前）
- L 的位置是 8（最后）
- 其余六个元素（A, B, C, D, E, G）的相对位置未知

我已经秘密选定了一个"响应规则"（从三种可能的规则中选择），并且指定了一对目标元素：{target_u} 和 {target_v}。

这三种可能的响应规则是：
- 规则 A（诚实）：总是如实回答查询的问题。
- 规则 B（完全反转）：总是给出与事实相反的回答。如果真实情况是"是"，会回答"否"；如果是"否"，会回答"是"。
- 规则 C（奇距反转）：如果查询的双方之间的真实位置绝对距离 |pos(X) - pos(Y)| 为偶数，会给出相反的回答；如果距离为奇数，会如实回答。

你的任务是：
1. 通过提问推断出我使用的是哪种响应规则
2. 判断目标对中 {target_u} 和 {target_v} 的真实前后关系

你可以反复向我提出二元比较查询，询问"元素 X 是否在元素 Y 之前？"
我会回答"是"或"否"，但我的回答会根据我选定的响应规则进行转换。

注意：你需要进行足够的有效比较（不同的元素对组合）才能推断出规则和答案。

使用以下 XML 格式提出比较查询（例如询问 A 是否在 B 之前）：

<query>A,B</query>

当你准备好给出最终答案时，必须同时说明：
1. 你推断的响应规则类型（rule）：使用 A、B 或 C
2. 目标对的真实前后关系（order）：使用 before 或 after

格式如下（假设推断规则为 A，且第一个元素在第二个元素之前）：

<answer>rule=A, order=before</answer>

其中 order=before 表示 {target_u} 在 {target_v} 之前，order=after 表示 {target_u} 在 {target_v} 之后。
"""

    game_rule_en = """\
Let's play an "Order Inference" game. Here are the rules:

The game has a totally ordered sequence of length 8, with element set S = {{F, L, A, B, C, D, E, G}}.
Each element has a unique position number (1 to 8), and it is known that:
- F is at position 1 (first)
- L is at position 8 (last)
- The relative positions of the other six elements (A, B, C, D, E, G) are unknown

I have secretly selected a "response rule" (from three possible rules) and designated a target pair of elements: {target_u} and {target_v}.

The three possible response rules are:
- Rule A (Honest): Always truthfully answers the query.
- Rule B (Full Inversion): Always gives the opposite of the truth. If the truth is "Yes", it says "No"; if the truth is "No", it says "Yes".
- Rule C (Even-Distance Inversion): If the absolute true distance |pos(X) - pos(Y)| between the two queried items is even, it inverts the truth; if the distance is odd, it answers truthfully.

Your task is to:
1. Infer which response rule I am using through queries
2. Determine the true order relationship between {target_u} and {target_v}

You can repeatedly ask me binary comparison queries: "Is element X before element Y?"
I will answer "Yes" or "No", but my answers will be transformed according to the response rule I selected.

Note: You need to make enough effective comparisons (different element pair combinations) to infer the rule and answer.

Use the following XML format for comparison queries (e.g., asking if A is before B):

<query>A,B</query>

When you are ready to give your final answer, you must specify both:
1. Your inferred response rule type (rule): use A, B, or C
2. The true order of the target pair (order): use before or after

Format as follows (assuming inferred rule is A and the first element is before the second):

<answer>rule=A, order=before</answer>

Where order=before means {target_u} is before {target_v}, and order=after means {target_u} is after {target_v}.
"""

    contextualized_rule_zh_1 = """\
我们现在来进行一项"轨道交通站点排查"任务，规则如下：

一条单向地铁线路上共有 8 个站点，站点代号集合为 S = {{F, L, A, B, C, D, E, G}}。
每个站点都有一个唯一的顺序编号（1到8），其中已知：
- 站点 F 是始发站，位置是 1（最前）
- 站点 L 是终点站，位置是 8（最后）
- 其余六个站点（A, B, C, D, E, G）的沿途相对先后顺序未知

系统的"信号响应规则"出现了异常（在三种可能的规则中固定了一种），并且调度中心指定了一对目标站点：{target_u} 和 {target_v} 需要你查明顺序。

这三种可能的响应规则是：
- 规则 A（诚实）：总是如实回答查询的问题。
- 规则 B（完全反转）：总是给出与事实相反的回答。如果真实情况是"是"，会回答"否"；如果是"否"，会回答"是"。
- 规则 C（奇距反转）：如果查询的双方之间的真实位置绝对距离 |pos(X) - pos(Y)| 为偶数，会给出相反的回答；如果距离为奇数，会如实回答。

你的任务是：
1. 通过提问推断出系统当前使用的是哪种信号响应规则
2. 判断目标站点对中 {target_u} 和 {target_v} 的真实先后到达关系

你可以反复向我提出二元比较查询，询问"列车是否先到达站点 X 再到达站点 Y？"
我会回答"是"或"否"，但我的回答会根据当前的信号响应规则进行转换反馈。

注意：你需要进行足够的有效比较（不同的站点对组合）才能推断出故障规则和真实顺序。

使用以下 XML 格式提出比较查询（例如询问是否先到 A 再到 B）：

<query>A,B</query>

当你准备好给出最终排查结果时，必须同时说明：
1. 你推断的响应规则类型（rule）：使用 A、B 或 C
2. 目标站点的真实先后关系（order）：使用 before 或 after

格式如下（假设推断规则为 A，且列车先到达第一个站点）：

<answer>rule=A, order=before</answer>

其中 order=before 表示先到达 {target_u} 再到达 {target_v}，order=after 表示先到达 {target_v} 再到达 {target_u}。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's conduct an "Urban Transit Station Sequence" diagnostic task. Here are the operational rules:

A unidirectional subway line has exactly 8 stations, with the station code set S = {{F, L, A, B, C, D, E, G}}.
Each station has a unique sequence number (1 to 8), and it is known that:
- Station F is the origin, at position 1 (first)
- Station L is the terminus, at position 8 (last)
- The relative sequence of the other six stations (A, B, C, D, E, G) is unknown

The system has locked into a secret "signal response rule" (one of three possible rules), and the dispatch center has designated a target pair of stations: {target_u} and {target_v}.

The three possible response rules are:
- Rule A (Honest): Always truthfully answers the query.
- Rule B (Full Inversion): Always gives the opposite of the truth. If the truth is "Yes", it says "No"; if the truth is "No", it says "Yes".
- Rule C (Even-Distance Inversion): If the absolute true distance |pos(X) - pos(Y)| between the two queried items is even, it inverts the truth; if the distance is odd, it answers truthfully.

Your task is to:
1. Infer which signal response rule the system is currently using through queries
2. Determine the true arrival order between station {target_u} and station {target_v}

You can repeatedly ask me binary comparison queries: "Does the train arrive at station X before station Y?"
I will answer "Yes" or "No", but my answers will be transformed according to the selected signal response rule.

Note: You need to make enough effective comparisons (different station pair combinations) to infer the rule and the correct sequence.

Use the following XML format for comparison queries (e.g., asking if station A is before B):

<query>A,B</query>

When you are ready to submit your final diagnostic report, you must specify both:
1. Your inferred response rule type (rule): use A, B, or C
2. The true arrival order of the target pair (order): use before or after

Format as follows (assuming inferred rule is A and the first station is visited before the second):

<answer>rule=A, order=before</answer>

Where order=before means the train arrives at {target_u} before {target_v}, and order=after means it arrives at {target_u} after {target_v}.
"""

    contextualized_rule_zh_2 = """\
我们现在来进行一项"疾病病理阶段回溯"分析，规则如下：

某未知疾病的完整发展周期包含 8 个病理阶段，阶段代号集合为 S = {{F, L, A, B, C, D, E, G}}。
每个阶段都有一个唯一的时间序编号（1到8），其中已知：
- 阶段 F 是初始感染期，位置是 1（最前）
- 阶段 L 是最终转归期，位置是 8（最后）
- 其余六个并发阶段（A, B, C, D, E, G）的相对发生顺序未知

监控仪器的"数据响应规则"被设定成了某种特定模式（从三种可能的规则中选择了一种），并且我们需要确认一对核心病理阶段：{target_u} 和 {target_v} 的先后关系。

这三种可能的响应规则是：
- 规则 A（诚实）：总是如实回答查询的问题。
- 规则 B（完全反转）：总是给出与事实相反的回答。如果真实情况是"是"，会回答"否"；如果是"否"，会回答"是"。
- 规则 C（奇距反转）：如果查询的双方之间的真实位置绝对距离 |pos(X) - pos(Y)| 为偶数，会给出相反的回答；如果距离为奇数，会如实回答。

你的任务是：
1. 通过提问推断出监控仪器使用的是哪种数据响应规则
2. 判断目标对中阶段 {target_u} 和阶段 {target_v} 的真实发生先后关系

你可以反复向我提出二元比较查询，询问"病理阶段 X 是否在阶段 Y 之前发生？"
我会回答"是"或"否"，但我的回答会根据设定的数据响应规则进行转换。

注意：你需要进行足够的有效比较（不同的阶段对组合）才能推断出规则和答案。

使用以下 XML 格式提出比较查询（例如询问阶段 A 是否在 B 之前发生）：

<query>A,B</query>

当你准备好给出最终分析结论时，必须同时说明：
1. 你推断的响应规则类型（rule）：使用 A、B 或 C
2. 目标病理阶段的真实先后关系（order）：使用 before 或 after

格式如下（假设推断规则为 A，且第一个阶段在第二个阶段之前发生）：

<answer>rule=A, order=before</answer>

其中 order=before 表示 {target_u} 在 {target_v} 之前发生，order=after 表示 {target_u} 在 {target_v} 之后发生。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Pathological Stage Retrospective" analysis. Here are the clinical rules:

The complete progression cycle of an unknown disease consists of 8 pathological stages, with the stage code set S = {{F, L, A, B, C, D, E, G}}.
Each stage has a unique chronological sequence number (1 to 8), and it is known that:
- Stage F is the initial infection phase, at position 1 (first)
- Stage L is the final clinical outcome, at position 8 (last)
- The relative occurrence order of the other six stages (A, B, C, D, E, G) is unknown

The monitoring instrument's "data response rule" is locked into a specific mode (one of three possible rules), and we need to verify the temporal relationship of a target pair of core stages: {target_u} and {target_v}.

The three possible response rules are:
- Rule A (Honest): Always truthfully answers the query.
- Rule B (Full Inversion): Always gives the opposite of the truth. If the truth is "Yes", it says "No"; if the truth is "No", it says "Yes".
- Rule C (Even-Distance Inversion): If the absolute true distance |pos(X) - pos(Y)| between the two queried items is even, it inverts the truth; if the distance is odd, it answers truthfully.

Your task is to:
1. Infer which data response rule the instrument is using through queries
2. Determine the true chronological order between stage {target_u} and stage {target_v}

You can repeatedly ask me binary comparison queries: "Did pathological stage X occur before stage Y?"
I will answer "Yes" or "No", but my answers will be transformed according to the active data response rule.

Note: You need to make enough effective clinical comparisons (different stage pair combinations) to infer the rule and the correct sequence.

Use the following XML format for comparison queries (e.g., asking if stage A occurred before B):

<query>A,B</query>

When you are ready to submit your final diagnostic conclusion, you must specify both:
1. Your inferred response rule type (rule): use A, B, or C
2. The true chronological order of the target pair (order): use before or after

Format as follows (assuming inferred rule is A and the first stage occurred before the second):

<answer>rule=A, order=before</answer>

Where order=before means {target_u} occurred before {target_v}, and order=after means {target_u} occurred after {target_v}.
"""

    contextualized_rule_zh_3 = """\
我们现在来进行一项"课程先修关系梳理"任务，规则如下：

某专业的培养方案包含 8 个核心模块，模块代码集合为 S = {{F, L, A, B, C, D, E, G}}。
每个模块都有一个唯一的授课顺位（1到8），其中已知：
- 模块 F 是新生导论，位置是 1（最前）
- 模块 L 是毕业设计，位置是 8（最后）
- 其余六个模块（A, B, C, D, E, G）的相对授课顺序未知

教务系统的"依赖查询响应规则"目前处于盲测状态（从三种可能的规则中选择了一种），并且系统要求我们验证一对目标模块：{target_u} 和 {target_v} 的先修关系。

这三种可能的响应规则是：
- 规则 A（诚实）：总是如实回答查询的问题。
- 规则 B（完全反转）：总是给出与事实相反的回答。如果真实情况是"是"，会回答"否"；如果是"否"，会回答"是"。
- 规则 C（奇距反转）：如果查询的双方之间的真实位置绝对距离 |pos(X) - pos(Y)| 为偶数，会给出相反的回答；如果距离为奇数，会如实回答。

你的任务是：
1. 通过提问推断出教务系统使用的是哪种响应规则
2. 判断目标对中模块 {target_u} 和模块 {target_v} 的真实授课先后关系

你可以反复向我提出二元比较查询，询问"模块 X 是否在模块 Y 之前授课？"
我会回答"是"或"否"，但我的回答会根据教务系统的查询响应规则进行转换。

注意：你需要进行足够的有效比较（不同的模块对组合）才能推断出规则和正确的授课大纲。

使用以下 XML 格式提出比较查询（例如询问 A 是否在 B 之前授课）：

<query>A,B</query>

当你准备好提交最终大纲审核时，必须同时说明：
1. 你推断的响应规则类型（rule）：使用 A、B 或 C
2. 目标模块对的真实先后关系（order）：使用 before 或 after

格式如下（假设推断规则为 A，且第一个模块在第二个模块之前授课）：

<answer>rule=A, order=before</answer>

其中 order=before 表示 {target_u} 先于 {target_v} 授课，order=after 表示 {target_u} 晚于 {target_v} 授课。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Curriculum Prerequisite Mapping" task. Here are the academic rules:

A degree program's curriculum contains 8 core modules, with the module code set S = {{F, L, A, B, C, D, E, G}}.
Each module has a unique teaching sequence number (1 to 8), and it is known that:
- Module F is the freshman introductory course, at position 1 (first)
- Module L is the capstone project, at position 8 (last)
- The relative teaching sequence of the other six modules (A, B, C, D, E, G) is unknown

The academic system's "dependency query response rule" is currently in a blind-test mode (one of three possible rules), and we must verify the prerequisite relationship of a target pair of modules: {target_u} and {target_v}.

The three possible response rules are:
- Rule A (Honest): Always truthfully answers the query.
- Rule B (Full Inversion): Always gives the opposite of the truth. If the truth is "Yes", it says "No"; if the truth is "No", it says "Yes".
- Rule C (Even-Distance Inversion): If the absolute true distance |pos(X) - pos(Y)| between the two queried items is even, it inverts the truth; if the distance is odd, it answers truthfully.

Your task is to:
1. Infer which response rule the academic system is using through queries
2. Determine the true teaching order between module {target_u} and module {target_v}

You can repeatedly ask me binary comparison queries: "Is module X taught before module Y?"
I will answer "Yes" or "No", but my answers will be transformed according to the system's response rule.

Note: You need to make enough effective academic comparisons (different module pair combinations) to infer the rule and the correct syllabus.

Use the following XML format for comparison queries (e.g., asking if module A is taught before B):

<query>A,B</query>

When you are ready to submit your final curriculum review, you must specify both:
1. Your inferred response rule type (rule): use A, B, or C
2. The true teaching order of the target pair (order): use before or after

Format as follows (assuming inferred rule is A and the first module is taught before the second):

<answer>rule=A, order=before</answer>

Where order=before means {target_u} is taught before {target_v}, and order=after means {target_u} is taught after {target_v}.
"""

    contextualized_rule_zh_4 = """\
我们现在来进行一项"流水线工序校验"任务，规则如下：

一条自动化装配线共有 8 道核心工序，工序代码集合为 S = {{F, L, A, B, C, D, E, G}}。
每道工序都有一个唯一的执行顺序（1到8），其中已知：
- 工序 F 是原料投料，位置是 1（最前）
- 工序 L 是成品包装，位置是 8（最后）
- 其余六道工序（A, B, C, D, E, G）的相对执行顺序未知

工控系统的"传感器反馈规则"目前处于校准模式（从三种可能的规则中固定了一种），并且总工要求我们排查一对目标工序：{target_u} 和 {target_v} 的先后执行关系。

这三种可能的响应规则是：
- 规则 A（诚实）：总是如实回答查询的问题。
- 规则 B（完全反转）：总是给出与事实相反的回答。如果真实情况是"是"，会回答"否"；如果是"否"，会回答"是"。
- 规则 C（奇距反转）：如果查询的双方之间的真实位置绝对距离 |pos(X) - pos(Y)| 为偶数，会给出相反的回答；如果距离为奇数，会如实回答。

你的任务是：
1. 通过提问推断出工控系统使用的是哪种传感器反馈规则
2. 判断目标对中工序 {target_u} 和工序 {target_v} 的真实执行先后关系

你可以反复向我提出二元比较查询，询问"工序 X 是否在工序 Y 之前执行？"
我会回答"是"或"否"，但我的回答会根据当前的传感器反馈规则进行转换输出。

注意：你需要进行足够的有效比较（不同的工序对组合）才能推断出规则和正确的工艺流程。

使用以下 XML 格式提出比较查询（例如询问工序 A 是否在 B 之前执行）：

<query>A,B</query>

当你准备好输出最终校准报告时，必须同时说明：
1. 你推断的传感器反馈规则类型（rule）：使用 A、B 或 C
2. 目标工序对的真实先后关系（order）：使用 before 或 after

格式如下（假设推断规则为 A，且第一道工序在第二道工序之前执行）：

<answer>rule=A, order=before</answer>

其中 order=before 表示 {target_u} 在 {target_v} 之前执行，order=after 表示 {target_u} 在 {target_v} 之后执行。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct an "Assembly Line Process Verification" task. Here are the operational rules:

An automated assembly line consists of 8 core processes, with the process code set S = {{F, L, A, B, C, D, E, G}}.
Each process has a unique execution sequence (1 to 8), and it is known that:
- Process F is raw material intake, at position 1 (first)
- Process L is final packaging, at position 8 (last)
- The relative execution sequence of the other six processes (A, B, C, D, E, G) is unknown

The industrial control system's "sensor feedback rule" is currently in a calibration mode (locked to one of three possible rules), and the chief engineer requires us to verify the execution order of a target pair of processes: {target_u} and {target_v}.

The three possible response rules are:
- Rule A (Honest): Always truthfully answers the query.
- Rule B (Full Inversion): Always gives the opposite of the truth. If the truth is "Yes", it says "No"; if the truth is "No", it says "Yes".
- Rule C (Even-Distance Inversion): If the absolute true distance |pos(X) - pos(Y)| between the two queried items is even, it inverts the truth; if the distance is odd, it answers truthfully.

Your task is to:
1. Infer which sensor feedback rule the control system is using through queries
2. Determine the true execution order between process {target_u} and process {target_v}

You can repeatedly ask me binary comparison queries: "Is process X executed before process Y?"
I will answer "Yes" or "No", but my answers will be transformed according to the active sensor feedback rule.

Note: You need to make enough effective process comparisons (different process pair combinations) to infer the rule and the correct manufacturing workflow.

Use the following XML format for comparison queries (e.g., asking if process A is executed before B):

<query>A,B</query>

When you are ready to output your final calibration report, you must specify both:
1. Your inferred sensor feedback rule type (rule): use A, B, or C
2. The true execution order of the target pair (order): use before or after

Format as follows (assuming inferred rule is A and the first process is executed before the second):

<answer>rule=A, order=before</answer>

Where order=before means {target_u} is executed before {target_v}, and order=after means {target_u} is executed after {target_v}.
"""

    contextualized_rule_zh_5 = """\
我们现在来进行一项"诉讼程序时间线重构"任务，规则如下：

一宗复杂的商业诉讼案件包含了 8 个关键的法定程序，程序代号集合为 S = {{F, L, A, B, C, D, E, G}}。
每个程序都有一个唯一的发生顺位（1到8），其中已知：
- 程序 F 是提交诉状，位置是 1（最前）
- 程序 L 是宣读判决，位置是 8（最后）
- 其余六个程序（A, B, C, D, E, G）的相对发生顺序未知

由于案宗档案受损，目前的"质证响应规则"是由当事人提供的（从三种可能的陈述规则中固定了一种），并且法庭要求查清一对核心程序：{target_u} 和 {target_v} 的先后关系。

这三种可能的响应规则是：
-规则 A（诚实）：总是如实回答查询的问题。
- 规则 B（完全反转）：总是给出与事实相反的回答。如果真实情况是"是"，会回答"否"；如果是"否"，会回答"是"。
- 规则 C（奇距反转）：如果查询的双方之间的真实位置绝对距离 |pos(X) - pos(Y)| 为偶数，会给出相反的回答；如果距离为奇数，会如实回答。

你的任务是：
1. 通过提问推断出当事人目前使用的是哪种质证响应规则
2. 判断目标对中程序 {target_u} 和程序 {target_v} 的真实发生先后关系

你可以反复向我提出二元比较查询，询问"程序 X 是否在程序 Y 之前发生？"
我会回答"是"或"否"，但我的回答会根据当事人所设定的质证响应规则进行转换。

注意：你需要进行足够的有效比较（不同的程序对组合）才能推断出陈述规则和真实的案情时间线。

使用以下 XML 格式提出比较查询（例如询问程序 A 是否在 B 之前发生）：

<query>A,B</query>

当你准备好提交最终法庭调查报告时，必须同时说明：
1. 你推断的响应规则类型（rule）：使用 A、B 或 C
2. 目标程序对的真实先后关系（order）：使用 before 或 after

格式如下（假设推断规则为 A，且第一个程序在第二个程序之前发生）：

<answer>rule=A, order=before</answer>

其中 order=before 表示 {target_u} 在 {target_v} 之前发生，order=after 表示 {target_u} 在 {target_v} 之后发生。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Litigation Timeline Reconstruction" task. Here are the procedural rules:

A complex commercial litigation case involves 8 key statutory procedures, with the procedure code set S = {{F, L, A, B, C, D, E, G}}.
Each procedure has a unique chronological sequence (1 to 8), and it is known that:
- Procedure F is filing the complaint, at position 1 (first)
- Procedure L is the final verdict delivery, at position 8 (last)
- The relative sequence of the other six procedures (A, B, C, D, E, G) is unknown

Due to damaged case files, the current "cross-examination response rule" is provided by a witness (locked to one of three possible narrative rules), and the court demands verification of the chronological order of a target pair of core procedures: {target_u} and {target_v}.

The three possible response rules are:
- Rule A (Honest): Always truthfully answers the query.
- Rule B (Full Inversion): Always gives the opposite of the truth. If the truth is "Yes", it says "No"; if the truth is "No", it says "Yes".
- Rule C (Even-Distance Inversion): If the absolute true distance |pos(X) - pos(Y)| between the two queried items is even, it inverts the truth; if the distance is odd, it answers truthfully.

Your task is to:
1. Infer which response rule the witness is using through queries
2. Determine the true chronological order between procedure {target_u} and procedure {target_v}

You can repeatedly ask me binary comparison queries: "Did procedure X legally precede procedure Y?"
I will answer "Yes" or "No", but my answers will be transformed according to the witness's established response rule.

Note: You need to make enough effective legal comparisons (different procedure pair combinations) to infer the rule and reconstruct the true factual timeline.

Use the following XML format for comparison queries (e.g., asking if procedure A preceded B):

<query>A,B</query>

When you are ready to submit your final court investigation report, you must specify both:
1. Your inferred response rule type (rule): use A, B, or C
2. The true chronological order of the target pair (order): use before or after

Format as follows (assuming inferred rule is A and the first procedure preceded the second):

<answer>rule=A, order=before</answer>

Where order=before means {target_u} occurred before {target_v}, and order=after means {target_u} occurred after {target_v}.
"""

    tags = ["answer", "query"]

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "sequence": ["F", "A", "B", "C", "D", "E", "G", "L"],
                "rule_type": "A",
                "target_pair": ("A", "G"),
            },
            2: {
                "sequence": ["F", "B", "D", "A", "E", "C", "G", "L"],
                "rule_type": "B",
                "target_pair": ("D", "C"),
            },
            3: {
                "sequence": ["F", "C", "A", "E", "B", "G", "D", "L"],
                "rule_type": "C",
                "target_pair": ("A", "G"),
            },
            4: {
                "sequence": ["F", "D", "B", "G", "A", "E", "C", "L"],
                "rule_type": "C",
                "target_pair": ("G", "A"),
            },
            5: {
                "sequence": ["F", "E", "G", "D", "C", "A", "B", "L"],
                "rule_type": "C",
                "target_pair": ("G", "D"),
            },
        },
        "en": {
            1: {
                "sequence": ["F", "A", "B", "C", "D", "E", "G", "L"],
                "rule_type": "A",
                "target_pair": ("A", "G"),
            },
            2: {
                "sequence": ["F", "B", "D", "A", "E", "C", "G", "L"],
                "rule_type": "B",
                "target_pair": ("D", "C"),
            },
            3: {
                "sequence": ["F", "C", "A", "E", "B", "G", "D", "L"],
                "rule_type": "C",
                "target_pair": ("A", "G"),
            },
            4: {
                "sequence": ["F", "D", "B", "G", "A", "E", "C", "L"],
                "rule_type": "C",
                "target_pair": ("G", "A"),
            },
            5: {
                "sequence": ["F", "E", "G", "D", "C", "A", "B", "L"],
                "rule_type": "C",
                "target_pair": ("G", "D"),
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
        
        self.sequence = cfg["sequence"]
        self.pos_map = {elem: idx + 1 for idx, elem in enumerate(self.sequence)}
        
        self.rule_type = cfg["rule_type"]
        
        self.target_pair = cfg["target_pair"]
        
        self.query_history = set()
        
        self._game_info = {
            "target_u": self.target_pair[0],
            "target_v": self.target_pair[1]
        }

    def _apply_rule(self, x, y):
        pos_x = self.pos_map[x]
        pos_y = self.pos_map[y]
        true_result = pos_x < pos_y
        
        if self.rule_type == "A":
            return true_result
        elif self.rule_type == "B":
            return not true_result
        elif self.rule_type == "C":
            distance = abs(pos_x - pos_y)
            if distance % 2 == 0:
                return not true_result
            else:
                return true_result
        else:
            raise ValueError(f"Unknown rule type: {self.rule_type}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "rule" not in ans_dict or "order" not in ans_dict:
            return False
        
        if ans_dict["rule"] != self.rule_type:
            return False
        
        u, v = self.target_pair
        true_order = "before" if self.pos_map[u] < self.pos_map[v] else "after"
        
        return ans_dict["order"] == true_order

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：查询格式无效，请使用 <query>X,Y</query> 格式。"
            error_element = "错误：元素不在集合中，请使用 F, L, A, B, C, D, E, G 中的元素。"
            error_same = "错误：不能查询相同的元素。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid query format. Please use <query>X,Y</query> format."
            error_element = "Error: Element not in set. Please use elements from F, L, A, B, C, D, E, G."
            error_same = "Error: Cannot query the same element."

        if "query" not in parsed_info:
            raise ValueError("No valid query tag found.")
        
        try:
            raw = parsed_info["query"]
            parts = [x.strip() for x in raw.split(",")]
            
            if len(parts) != 2:
                return error_format
            
            x, y = parts
            
            valid_elements = {"F", "L", "A", "B", "C", "D", "E", "G"}
            if x not in valid_elements or y not in valid_elements:
                return error_element
            
            if x == y:
                return error_same
            
            query_key = tuple(sorted([x, y]))
            self.query_history.add(query_key)
            
            result = self._apply_rule(x, y)
            return yes_res if result else no_res
            
        except Exception as e:
            return error_format

    def _cf_make_wrong(self, correct):
        try:
            int_val = int(correct)
            return str(int_val + 1)
        except ValueError:
            pass
        
        if correct == "是": return "否"
        if correct == "否": return "是"
        if correct == "Yes": return "No"
        if correct == "No": return "Yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self):
        valid_elements = ["F", "L", "A", "B", "C", "D", "E", "G"]
        
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        queries = []
        
        for x in valid_elements:
            for y in valid_elements:
                if x == y:
                    continue
                
                result = self._apply_rule(x, y)
                ans_str = yes_res if result else no_res
                
                queries.append({
                    "query": f"<query>{x},{y}</query>",
                    "answer": ans_str
                })
                
        return queries