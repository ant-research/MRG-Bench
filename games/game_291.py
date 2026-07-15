from .base import Game
import random

class SequenceIndexTransformGame(Game):

    game_rule_zh = """\
我们现在来玩一个"序列索引变换"的推理游戏，规则如下：

游戏设定了一个长度为 {n} 的有序序列 S[1..{n}]，其元素来自一个已公开的标签集合 L = {{{labels}}}。序列 S 是标签集合 L 的某个未知排列。

同时，游戏设定了一个固定但未知的索引变换规则 f，该规则将查询位置映射到实际返回位置。变换规则 f 从以下四种候选中选择其一（整局游戏中保持不变）：

A. 恒等变换：f(m) = m（直接返回第 m 个位置的元素）
B. 反转变换：f(m) = {n_plus_1} - m（返回对称位置的元素）
C. 近端吸附变换：计算 m 到左端的距离 dL = m - 1，到右端的距离 dR = {n} - m。若 dL 小于等于 dR，则 f(m) = 1；否则 f(m) = {n}
D. 远端吸附变换：计算 m 到左端的距离 dL = m - 1，到右端的距离 dR = {n} - m。若 dL 大于等于 dR，则 f(m) = 1；否则 f(m) = {n}

你的目标是通过尽可能少的查询次数，推断出序列的首位置元素 S[1] 是什么标签。

你可以反复提出查询：
- 位置查询：询问位置 m（1 到 {n} 之间的整数）。我会返回经过变换后的位置所对应的标签，即 S[f(m)]。

当你收集足够信息后，请提交最终答案，说明 S[1] 的标签是什么。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 位置查询（例如查询位置 3）：
<query_position>3</query_position>

提交最终答案时，必须说明 S[1] 的标签（你也可以选择性地说明推断出的变换规则类型 A、B、C 或 D，但这不影响判定），格式如下：

<answer>S[1]=标签X</answer>

或者：

<answer>S[1]=标签X, transform=A</answer>
"""

    game_rule_en = """\
Let's play a "Sequence Index Transform" deduction game. Here are the rules:

The game has set up an ordered sequence S[1..{n}] of length {n}, whose elements come from a publicly known label set L = {{{labels}}}. Sequence S is an unknown permutation of label set L.

Additionally, the game has set up a fixed but unknown index transformation rule f, which maps the queried position to the actual returned position. The transformation rule f is selected from one of the following four candidates (remains constant throughout the game):

A. Identity Transform: f(m) = m (directly returns the element at position m)
B. Reversal Transform: f(m) = {n_plus_1} - m (returns the element at the symmetric position)
C. Near-End Attraction Transform: Calculate distance to left end dL = m - 1, distance to right end dR = {n} - m. If dL is less than or equal to dR, then f(m) = 1; otherwise f(m) = {n}
D. Far-End Attraction Transform: Calculate distance to left end dL = m - 1, distance to right end dR = {n} - m. If dL is greater than or equal to dR, then f(m) = 1; otherwise f(m) = {n}

Your goal is to infer what label S[1] (the first position element) is through as few queries as possible.

You can repeatedly make queries:
- Position Query: Ask about position m (an integer between 1 and {n}). I will return the label at the transformed position, i.e., S[f(m)].

When you have collected enough information, submit your final answer stating what label S[1] is. If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Position Query (e.g., querying position 3):
<query_position>3</query_position>

When submitting the final answer, you must state the label of S[1] (you may optionally state the inferred transformation rule type A, B, C, or D, but this does not affect the judgment), using this format:

<answer>S[1]=LabelX</answer>

Or:

<answer>S[1]=LabelX, transform=A</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通调度中心正在运行一项"序列盲调"协议。

系统设定了一个长度为 {n} 的车队发车序列 S[1..{n}]，其车辆类型来自已公开的集合 L = {{{labels}}}。序列 S 是该集合的某个未知排列。

由于网络存在一个固定但未知的路由变换规则 f，该规则将你查询的调度槽位映射到实际发车的槽位。变换规则 f 从以下四种候选中选择其一（整局调度中保持不变）：

A. 恒等路由：f(m) = m（直接返回第 m 个槽位的车辆）
B. 镜像路由：f(m) = {n_plus_1} - m（返回对称槽位的车辆）
C. 近端枢纽吸附：计算 m 到首端的距离 dL = m - 1，到尾端的距离 dR = {n} - m。若 dL 小于等于 dR，则 f(m) = 1；否则 f(m) = {n}
D. 远端枢纽吸附：计算 m 到首端的距离 dL = m - 1，到尾端的距离 dR = {n} - m。若 dL 大于等于 dR，则 f(m) = 1；否则 f(m) = {n}

你的目标是通过尽可能少的查询次数，推断出领航车辆（即首发位置 S[1]）是什么类型。

你可以反复提出查询：
- 槽位查询：询问槽位 m（1 到 {n} 之间的整数）。调度系统会返回经过路由变换后对应槽位的车辆类型，即 S[f(m)]。

当你收集足够信息后，请提交最终答案，说明 S[1] 的车辆类型。若答案错误或格式不符，调度评估失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 槽位查询（例如查询槽位 3）：
<query_position>3</query_position>

提交最终答案时，必须说明 S[1] 的车辆类型（你也可以选择性地说明推断出的变换规则类型 A、B、C 或 D，但这不影响判定），格式如下：

<answer>S[1]=车辆X</answer>

或者：

<answer>S[1]=车辆X, transform=A</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
The Intelligent Traffic Dispatch Center is running a "Blind Sequence Dispatch" protocol.

The system has set up a dispatch sequence S[1..{n}] of length {n} for a fleet, whose vehicle types come from a publicly known set L = {{{labels}}}. Sequence S is an unknown permutation of set L.

Due to a fixed but unknown routing transformation rule f in the network, the queried dispatch slot is mapped to the actual dispatched slot. The transformation rule f is selected from one of the following four candidates (remains constant throughout the dispatch process):

A. Identity Routing: f(m) = m (directly returns the vehicle at slot m)
B. Mirror Routing: f(m) = {n_plus_1} - m (returns the vehicle at the symmetric slot)
C. Proximal Hub Attraction: Calculate distance to start dL = m - 1, distance to end dR = {n} - m. If dL is less than or equal to dR, then f(m) = 1; otherwise f(m) = {n}
D. Distal Hub Attraction: Calculate distance to start dL = m - 1, distance to end dR = {n} - m. If dL is greater than or equal to dR, then f(m) = 1; otherwise f(m) = {n}

Your goal is to infer what vehicle type the lead vehicle (first position S[1]) is through as few queries as possible.

You can repeatedly make queries:
- Slot Query: Ask about slot m (an integer between 1 and {n}). The dispatch system will return the vehicle type at the transformed slot, i.e., S[f(m)].

When you have collected enough information, submit your final answer stating what vehicle type S[1] is. If the answer is wrong or the format is invalid, the dispatch evaluation fails.

Each query must contain only one tag. Use the following XML format:

- Slot Query (e.g., querying slot 3):
<query_position>3</query_position>

When submitting the final answer, you must state the vehicle type of S[1] (you may optionally state the inferred routing rule type A, B, C, or D, but this does not affect the judgment), using this format:

<answer>S[1]=VehicleX</answer>

Or:

<answer>S[1]=VehicleX, transform=A</answer>
"""

    contextualized_rule_zh_2 = """\
医疗信息系统正在执行一项"盲态临床试验"的数据流转。

系统设定了一个长度为 {n} 的治疗阶段序列 S[1..{n}]，其干预药物来自已公开的集合 L = {{{labels}}}。序列 S 是该集合的某个未知排列。

同时，系统底层存在一个固定但未知的脱敏重定向规则 f，该规则将你查询的阶段映射到实际调用的阶段。重定向规则 f 从以下四种候选中选择其一（整局试验中保持不变）：

A. 恒等映射：f(m) = m（直接返回第 m 个阶段的药物）
B. 逆向映射：f(m) = {n_plus_1} - m（返回对称阶段的药物）
C. 近端基线吸附：计算 m 到初始阶段的距离 dL = m - 1，到终末阶段的距离 dR = {n} - m。若 dL 小于等于 dR，则 f(m) = 1；否则 f(m) = {n}
D. 远端基线吸附：计算 m 到初始阶段的距离 dL = m - 1，到终末阶段的距离 dR = {n} - m。若 dL 大于等于 dR，则 f(m) = 1；否则 f(m) = {n}

你的目标是通过尽可能少的查询次数，推断出首诊阶段（即 S[1]）使用的是什么干预药物。

你可以反复提出查询：
- 阶段查询：询问阶段 m（1 到 {n} 之间的整数）。系统会返回经过重定向后对应阶段的药物，即 S[f(m)]。

当你收集足够信息后，请提交最终答案，说明 S[1] 的药物。若答案错误或格式不符，试验评估失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 阶段查询（例如查询阶段 3）：
<query_position>3</query_position>

提交最终答案时，必须说明 S[1] 的药物（你也可以选择性地说明推断出的重定向规则类型 A、B、C 或 D，但这不影响判定），格式如下：

<answer>S[1]=药物X</answer>

或者：

<answer>S[1]=药物X, transform=A</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The Hospital Information System is executing a data workflow for a "Blinded Clinical Trial."

The system has configured a treatment phase sequence S[1..{n}] of length {n}, whose intervention drugs come from a publicly known set L = {{{labels}}}. Sequence S is an unknown permutation of set L.

Meanwhile, a fixed but unknown desensitization redirection rule f exists in the backend, mapping the queried phase to the actually retrieved phase. The redirection rule f is selected from one of the following four candidates (remains constant throughout the trial):

A. Identity Mapping: f(m) = m (directly returns the drug at phase m)
B. Reverse Mapping: f(m) = {n_plus_1} - m (returns the drug at the symmetric phase)
C. Proximal Baseline Attraction: Calculate distance to initial phase dL = m - 1, distance to terminal phase dR = {n} - m. If dL is less than or equal to dR, then f(m) = 1; otherwise f(m) = {n}
D. Distal Baseline Attraction: Calculate distance to initial phase dL = m - 1, distance to terminal phase dR = {n} - m. If dL is greater than or equal to dR, then f(m) = 1; otherwise f(m) = {n}

Your goal is to infer what drug is used in the first diagnostic phase (i.e., S[1]) through as few queries as possible.

You can repeatedly make queries:
- Phase Query: Ask about phase m (an integer between 1 and {n}). The system will return the drug at the redirected phase, i.e., S[f(m)].

When you have collected enough information, submit your final answer stating what drug S[1] is. If the answer is wrong or the format is invalid, the trial evaluation fails.

Each query must contain only one tag. Use the following XML format:

- Phase Query (e.g., querying phase 3):
<query_position>3</query_position>

When submitting the final answer, you must state the drug of S[1] (you may optionally state the inferred redirection rule type A, B, C, or D, but this does not affect the judgment), using this format:

<answer>S[1]=DrugX</answer>

Or:

<answer>S[1]=DrugX, transform=A</answer>
"""

    contextualized_rule_zh_3 = """\
自适应学习系统正在测试一项"认知序列重定向"算法。

系统设定了一个长度为 {n} 的学习模块序列 S[1..{n}]，其知识点主题来自已公开的集合 L = {{{labels}}}。序列 S 是该集合的某个未知排列。

同时，系统内置了一个固定但未知的学习路径重定向规则 f，该规则将你请求的模块索引映射到实际分发的模块。规则 f 从以下四种候选中选择其一（整局测试中保持不变）：

A. 线性路径：f(m) = m（直接返回第 m 个模块的主题）
B. 回溯路径：f(m) = {n_plus_1} - m（返回对称模块的主题）
C. 基础补救偏好：计算 m 到起点的距离 dL = m - 1，到终点的距离 dR = {n} - m。若 dL 小于等于 dR，则 f(m) = 1；否则 f(m) = {n}
D. 进阶挑战偏好：计算 m 到起点的距离 dL = m - 1，到终点的距离 dR = {n} - m。若 dL 大于等于 dR，则 f(m) = 1；否则 f(m) = {n}

你的目标是通过尽可能少的查询次数，推断出先导模块（即首位元素 S[1]）的主题是什么。

你可以反复提出查询：
- 模块查询：询问模块索引 m（1 到 {n} 之间的整数）。系统会返回经过重定向后对应模块的知识点主题，即 S[f(m)]。

当你收集足够信息后，请提交最终答案，说明 S[1] 的主题。若答案错误或格式不符，测试失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 模块查询（例如查询模块 3）：
<query_position>3</query_position>

提交最终答案时，必须说明 S[1] 的主题（你也可以选择性地说明推断出的重定向规则类型 A、B、C 或 D，但这不影响判定），格式如下：

<answer>S[1]=主题X</answer>

或者：

<answer>S[1]=主题X, transform=A</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The Adaptive Learning System is testing a "Cognitive Sequence Redirection" algorithm.

The system has established a learning module sequence S[1..{n}] of length {n}, whose knowledge topics come from a publicly known set L = {{{labels}}}. Sequence S is an unknown permutation of set L.

Concurrently, a fixed but unknown learning path redirection rule f is built into the system, mapping your requested module index to the actually distributed module. The rule f is selected from one of the following four candidates (remains constant throughout the test):

A. Linear Path: f(m) = m (directly returns the topic at module m)
B. Retrograde Path: f(m) = {n_plus_1} - m (returns the topic at the symmetric module)
C. Foundational Remedial Bias: Calculate distance to start dL = m - 1, distance to end dR = {n} - m. If dL is less than or equal to dR, then f(m) = 1; otherwise f(m) = {n}
D. Advanced Challenge Bias: Calculate distance to start dL = m - 1, distance to end dR = {n} - m. If dL is greater than or equal to dR, then f(m) = 1; otherwise f(m) = {n}

Your goal is to infer what the topic of the prerequisite module (first element S[1]) is through as few queries as possible.

You can repeatedly make queries:
- Module Query: Ask about module index m (an integer between 1 and {n}). The system will return the knowledge topic at the redirected module, i.e., S[f(m)].

When you have collected enough information, submit your final answer stating what topic S[1] is. If the answer is wrong or the format is invalid, the test fails.

Each query must contain only one tag. Use the following XML format:

- Module Query (e.g., querying module 3):
<query_position>3</query_position>

When submitting the final answer, you must state the topic of S[1] (you may optionally state the inferred redirection rule type A, B, C, or D, but this does not affect the judgment), using this format:

<answer>S[1]=TopicX</answer>

Or:

<answer>S[1]=TopicX, transform=A</answer>
"""

    contextualized_rule_zh_4 = """\
自动化无人工厂正在调试"柔性产线"的工位调度程序。

流水线设定了一个长度为 {n} 的加工工序序列 S[1..{n}]，其作业组件来自已公开的集合 L = {{{labels}}}。序列 S 是该集合的某个未知排列。

由于传送带系统存在一个固定但未知的物理偏转规则 f，该规则将你检测的工位映射到实际抓取的工位。偏转规则 f 从以下四种候选中选择其一（整局调试中保持不变）：

A. 准确定位：f(m) = m（直接抓取第 m 个工位的组件）
B. 镜像翻转：f(m) = {n_plus_1} - m（抓取对称工位的组件）
C. 近端缓存吸附：计算 m 到进料口的距离 dL = m - 1，到出料口的距离 dR = {n} - m。若 dL 小于等于 dR，则 f(m) = 1；否则 f(m) = {n}
D. 远端缓存吸附：计算 m 到进料口的距离 dL = m - 1，到出料口的距离 dR = {n} - m。若 dL 大于等于 dR，则 f(m) = 1；否则 f(m) = {n}

你的目标是通过尽可能少的查询次数，推断出基础组件（即首个工位 S[1]）是什么。

你可以反复提出查询：
- 工位查询：询问工位 m（1 到 {n} 之间的整数）。系统会返回经过偏转后对应工位的组件，即 S[f(m)]。

当你收集足够信息后，请提交最终答案，说明 S[1] 的组件。若答案错误或格式不符，调试失败。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 工位查询（例如查询工位 3）：
<query_position>3</query_position>

提交最终答案时，必须说明 S[1] 的组件（你也可以选择性地说明推断出的偏转规则类型 A、B、C 或 D，但这不影响判定），格式如下：

<answer>S[1]=组件X</answer>

或者：

<answer>S[1]=组件X, transform=A</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
The automated dark factory is debugging a workstation scheduler for its "Flexible Assembly Line."

The conveyor has set up a processing sequence S[1..{n}] of length {n}, whose operational components come from a publicly known set L = {{{labels}}}. Sequence S is an unknown permutation of set L.

Due to a fixed but unknown physical deflection rule f in the conveyor belt system, your inspected workstation is mapped to the actually fetched workstation. The deflection rule f is selected from one of the following four candidates (remains constant throughout the debugging):

A. Accurate Positioning: f(m) = m (directly fetches the component at workstation m)
B. Mirror Flip: f(m) = {n_plus_1} - m (fetches the component at the symmetric workstation)
C. Proximal Buffer Attraction: Calculate distance to intake dL = m - 1, distance to outtake dR = {n} - m. If dL is less than or equal to dR, then f(m) = 1; otherwise f(m) = {n}
D. Distal Buffer Attraction: Calculate distance to intake dL = m - 1, distance to outtake dR = {n} - m. If dL is greater than or equal to dR, then f(m) = 1; otherwise f(m) = {n}

Your goal is to infer what the base component (the first workstation S[1]) is through as few queries as possible.

You can repeatedly make queries:
- Workstation Query: Ask about workstation m (an integer between 1 and {n}). The system will return the component at the deflected workstation, i.e., S[f(m)].

When you have collected enough information, submit your final answer stating what component S[1] is. If the answer is wrong or the format is invalid, the debugging fails.

Each query must contain only one tag. Use the following XML format:

- Workstation Query (e.g., querying workstation 3):
<query_position>3</query_position>

When submitting the final answer, you must state the component of S[1] (you may optionally state the inferred deflection rule type A, B, C, or D, but this does not affect the judgment), using this format:

<answer>S[1]=ComponentX</answer>

Or:

<answer>S[1]=ComponentX, transform=A</answer>
"""

    contextualized_rule_zh_5 = """\
电子物证数字档案室正在启动"案卷盲态审查"程序。

档案库设定了一个长度为 {n} 的证据调用序列 S[1..{n}]，其物证类别来自已公开的集合 L = {{{labels}}}。序列 S 是该集合的某个未知排列。

审查系统底层存在一个固定但未知的权限校验规则 f，该规则将你请求的卷宗编号映射到实际提取的卷宗。校验规则 f 从以下四种候选中选择其一（整局审查中保持不变）：

A. 顺序归档：f(m) = m（直接提取第 m 号卷宗的物证）
B. 倒序归档：f(m) = {n_plus_1} - m（提取对称卷宗的物证）
C. 预审期吸附：计算 m 到首卷的距离 dL = m - 1，到末卷的距离 dR = {n} - m。若 dL 小于等于 dR，则 f(m) = 1；否则 f(m) = {n}
D. 终审期吸附：计算 m 到首卷的距离 dL = m - 1，到末卷的距离 dR = {n} - m。若 dL 大于等于 dR，则 f(m) = 1；否则 f(m) = {n}

你的目标是通过尽可能少的查询次数，推断出核心首证（即 S[1]）是什么物证类别。

你可以反复提出查询：
- 卷宗查询：询问卷宗编号 m（1 到 {n} 之间的整数）。档案室会返回经过校验后对应卷宗的物证类别，即 S[f(m)]。

当你收集足够信息后，请提交最终答案，说明 S[1] 的物证类别。若答案错误或格式不符，审查程序中止。

每次查询只能包含一个标签。请使用以下 XML 格式：

- 卷宗查询（例如查询卷宗 3）：
<query_position>3</query_position>

提交最终答案时，必须说明 S[1] 的物证类别（你也可以选择性地说明推断出的校验规则类型 A、B、C 或 D，但这不影响判定），格式如下：

<answer>S[1]=物证X</answer>

或者：

<answer>S[1]=物证X, transform=A</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
The Digital Evidence Archive is initiating a "Blind Case Review" procedure.

The archive has established an evidence retrieval sequence S[1..{n}] of length {n}, whose exhibit categories come from a publicly known set L = {{{labels}}}. Sequence S is an unknown permutation of set L.

A fixed but unknown permission validation rule f operates in the review system backend, mapping your requested file number to the actually extracted file. The validation rule f is selected from one of the following four candidates (remains constant throughout the review):

A. Chronological Filing: f(m) = m (directly extracts the exhibit of file m)
B. Reverse Filing: f(m) = {n_plus_1} - m (extracts the exhibit of the symmetric file)
C. Preliminary Phase Attraction: Calculate distance to first file dL = m - 1, distance to last file dR = {n} - m. If dL is less than or equal to dR, then f(m) = 1; otherwise f(m) = {n}
D. Final Phase Attraction: Calculate distance to first file dL = m - 1, distance to last file dR = {n} - m. If dL is greater than or equal to dR, then f(m) = 1; otherwise f(m) = {n}

Your goal is to infer what exhibit category the primary core evidence (i.e., S[1]) is through as few queries as possible.

You can repeatedly make queries:
- File Query: Ask about file number m (an integer between 1 and {n}). The archive will return the exhibit category of the validated file, i.e., S[f(m)].

When you have collected enough information, submit your final answer stating what exhibit category S[1] is. If the answer is wrong or the format is invalid, the review procedure halts.

Each query must contain only one tag. Use the following XML format:

- File Query (e.g., querying file 3):
<query_position>3</query_position>

When submitting the final answer, you must state the exhibit category of S[1] (you may optionally state the inferred validation rule type A, B, C, or D, but this does not affect the judgment), using this format:

<answer>S[1]=ExhibitX</answer>

Or:

<answer>S[1]=ExhibitX, transform=A</answer>
"""

    tags = ["answer", "query_position"]
    
    reasoning_type = "溯因推理"
    data_structure = "序列"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 3,
                "labels": ["甲", "乙", "丙"],
                "sequence": ["乙", "丙", "甲"],
                "transform": "A",
            },
            2: {
                "n": 4,
                "labels": ["红", "蓝", "绿", "黄"],
                "sequence": ["绿", "黄", "蓝", "红"],
                "transform": "B",
            },
            3: {
                "n": 5,
                "labels": ["α", "β", "γ", "δ", "ε"],
                "sequence": ["γ", "α", "δ", "β", "ε"],
                "transform": "C",
            },
            4: {
                "n": 6,
                "labels": ["木", "火", "土", "金", "水", "风"],
                "sequence": ["火", "金", "木", "水", "土", "风"],
                "transform": "D",
            },
            5: {
                "n": 7,
                "labels": ["日", "月", "星", "云", "雨", "雪", "雷"],
                "sequence": ["月", "星", "雨", "云", "日", "雷", "雪"],
                "transform": "B",
            },
        },
        "en": {
            1: {
                "n": 3,
                "labels": ["A", "B", "C"],
                "sequence": ["B", "C", "A"],
                "transform": "A",
            },
            2: {
                "n": 4,
                "labels": ["Red", "Blue", "Green", "Yellow"],
                "sequence": ["Green", "Yellow", "Blue", "Red"],
                "transform": "B",
            },
            3: {
                "n": 5,
                "labels": ["Alpha", "Beta", "Gamma", "Delta", "Epsilon"],
                "sequence": ["Gamma", "Alpha", "Delta", "Beta", "Epsilon"],
                "transform": "C",
            },
            4: {
                "n": 6,
                "labels": ["Wood", "Fire", "Earth", "Metal", "Water", "Wind"],
                "sequence": ["Fire", "Metal", "Wood", "Water", "Earth", "Wind"],
                "transform": "D",
            },
            5: {
                "n": 7,
                "labels": ["Sun", "Moon", "Star", "Cloud", "Rain", "Snow", "Thunder"],
                "sequence": ["Moon", "Star", "Rain", "Cloud", "Sun", "Thunder", "Snow"],
                "transform": "B",
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
        
        self.n = cfg["n"]
        self.labels = cfg["labels"]
        self.sequence = cfg["sequence"]
        self.transform_type = cfg["transform"]
        
        self._game_info["n"] = self.n
        self._game_info["n_plus_1"] = self.n + 1
        self._game_info["labels"] = ", ".join(self.labels)

    def _apply_transform(self, m):
        if self.transform_type == "A":
            return m
        elif self.transform_type == "B":
            return self.n + 1 - m
        elif self.transform_type == "C":
            dL = m - 1
            dR = self.n - m
            return 1 if dL <= dR else self.n
        elif self.transform_type == "D":
            dL = m - 1
            dR = self.n - m
            return 1 if dL >= dR else self.n
        else:
            raise ValueError(f"Unknown transform type: {self.transform_type}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        correct_answer = self.sequence[0]
        
        parts = [x.strip() for x in raw_ans.replace("，", ",").split(",")]
        ans_dict = {}
        
        for part in parts:
            if "=" in part:
                k, v = part.split("=", 1)
                ans_dict[k.strip()] = v.strip()
        
        if "S[1]" in ans_dict:
            return ans_dict["S[1]"].lower() == correct_answer.lower()
            
        if raw_ans.lower() == correct_answer.lower():
            return True
            
        return False

    def _cf_core_produce(self, parsed_info):
        if "query_position" in parsed_info:
            try:
                m = int(parsed_info["query_position"].strip())
                
                if m < 1 or m > self.n:
                    if self.config.language == "zh":
                        return f"错误：位置必须在 1 到 {self.n} 之间。"
                    else:
                        return f"Error: Position must be between 1 and {self.n}."
                
                transformed_pos = self._apply_transform(m)
                
                label = self.sequence[transformed_pos - 1]
                
                return label
                
            except ValueError:
                if self.config.language == "zh":
                    return "错误：查询位置必须是整数。"
                else:
                    return "Error: Query position must be an integer."
        else:
            raise ValueError("No valid query tag found.")

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        for m in range(1, self.n + 1):
            transformed_pos = self._apply_transform(m)
            
            label = self.sequence[transformed_pos - 1]
            
            results.append({
                "query": f"<query_position>{m}</query_position>",
                "answer": label
            })
            
        return results

    def _cf_make_wrong(self, correct: str) -> str:
        alternatives = [label for label in self.labels if label != correct]
        if alternatives:
            return alternatives[0]
        
        return f"{correct}_WRONG"