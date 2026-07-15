from .base import Game
import random
import hashlib

class GAME176(Game):

    game_rule_zh = """\
我们来玩一个"黑箱探测"的推理游戏，规则如下：

游戏设定了一个未知的正整数 H（H 在 1 到 {max_h} 之间）。系统提供一个确定性"黑箱"函数，你可以向它查询：给定一个正整数 k，黑箱会返回一个文本串 S(k)。

黑箱函数的特性：
1. 结构性质：S(k) = g(min(k, H))，其中 g 是一个未知但固定的编码函数
2. 单射性质：g 在集合 {{1, 2, ..., H}} 上是单射的，即对于所有 1 小于等于 i 小于 j 小于等于 H，都有 g(i) 不等于 g(j)
3. 确定性：对同一个 k 重复查询，返回值完全一致
4. 可观测性：你只能通过比较不同 k 的返回值是否完全相等来获取信息

由上述性质可以推导出：
- 当 k 小于 H 时，S(k) 不等于 S(k+1)
- 当 k 大于等于 H 时，S(k) 等于 S(k+1)（之后对更大的 k 也保持相同）

你的目标是：通过尽可能少的查询次数，确定未知参数 H 的值。

你可以进行以下操作：

1. 试探查询：提交一个正整数 k（1 到 {max_query} 之间），系统返回文本串 S(k)
2. 复查查询：请求重复上一轮的返回值，用于一致性验证（可选）
3. 提交答案：当你收集足够信息后，提交一个正整数作为对 H 的猜测

注意：返回的文本串是不透明的（不可直接映射为数值），唯一可用的信息是判断不同返回值之间是否相等。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 试探查询（例如查询 k=5）：
<query_probe>5</query_probe>

- 复查查询（重复上一次返回）：
<query_repeat></query_repeat>

- 提交最终答案（例如猜测 H=7）：
<answer>7</answer>
"""

    game_rule_en = """\
Let's play a "Black Box Probing" deduction game. Here are the rules:

The game has set an unknown positive integer H (H is between 1 and {max_h}). The system provides a deterministic "black box" function that you can query: given a positive integer k, the black box returns a text string S(k).

Properties of the black box function:
1. Structural property: S(k) = g(min(k, H)), where g is an unknown but fixed encoding function
2. Injectivity property: g is injective on the set {{1, 2, ..., H}}, meaning for all 1 less than or equal to i less than j less than or equal to H, g(i) is not equal to g(j)
3. Determinism: Repeated queries with the same k return exactly the same value
4. Observability: You can only obtain information by comparing whether return values for different k are completely equal

From the above properties, we can deduce:
- When k is less than H, S(k) is not equal to S(k+1)
- When k is greater than or equal to H, S(k) equals S(k+1) (and remains the same for larger k)

Your goal is: determine the value of the unknown parameter H with as few queries as possible.

You can perform the following operations:

1. Probe query: Submit a positive integer k (between 1 and {max_query}), the system returns text string S(k)
2. Repeat query: Request the return value from the last round for consistency verification (optional)
3. Submit answer: When you have gathered enough information, submit a positive integer as your guess for H

Note: The returned text strings are opaque (cannot be directly mapped to numerical values); the only usable information is determining whether different return values are equal.

Each operation must contain only one tag. Use the following XML format:

- Probe query (e.g., query k=5):
<query_probe>5</query_probe>

- Repeat query (repeat last return):
<query_repeat></query_repeat>

- Submit final answer (e.g., guess H=7):
<answer>7</answer>
"""

    contextualized_rule_zh_1 = """\
【交通场景】智能路网拥堵阈值探测
我们来进行一项城市路网承载力测试，规则如下：

系统设定了一个未知的道路饱和阈值 H（H 在 1 到 {max_h} 之间，单位：百辆/小时）。你拥有一个智能交通流量监测黑箱，你可以输入指定的测试车流量 k，监测器会返回该路段状态的加密特征签名 S(k)。

交通监测黑箱的特性：
1. 结构性质：S(k) = g(min(k, H))，其中 g 是未知的固定特征编码算法。
2. 单射性质：在未达到饱和前（即流量在 {{1, 2, ..., H}} 范围内），每个不同的流量都会产生唯一的交通状态签名。
3. 确定性：对相同的车流量 k 重复测试，返回的特征签名完全一致。
4. 可观测性：签名是经过加密的，你只能通过比对不同 k 值的签名是否完全一致来获取路网状态信息。

由此可以推导出交通流特性：
- 当车流量 k 小于饱和阈值 H 时，路况仍在动态变化，S(k) 不等于 S(k+1)。
- 当车流量 k 大于等于阈值 H 时，道路进入全面拥堵饱和状态，特征签名不再改变，即 S(k) 等于 S(k+1)。

你的目标是：通过尽可能少的测试次数，探测出该路网的精准饱和阈值 H。

你可以进行以下操作：
1. 试探查询：提交一个测试车流量 k（1 到 {max_query} 之间的正整数），获取特征签名 S(k)。
2. 复查查询：请求重复上一轮的签名数据，用于系统一致性校验（可选）。
3. 提交答案：当你确认了道路的饱和阈值后，提交该正整数作为对 H 的最终判定。

注意：返回的签名是不透明的字符串，唯一可用的信息是判断不同车流量下的签名是否相同。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 试探查询（例如输入车流量 k=5）：
<query_probe>5</query_probe>

- 复查查询（重复上一次返回）：
<query_repeat></query_repeat>

- 提交最终答案（例如判定阈值 H=7）：
<answer>7</answer>
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario] Smart Road Network Congestion Threshold Detection
Let's conduct an urban road network capacity test. The rules are as follows:

The system has an unknown road saturation threshold H (H is between 1 and {max_h}, unit: hundreds of vehicles/hour). You have access to a smart traffic flow monitoring black box. You can input a test traffic volume k, and the monitor will return an encrypted status signature S(k).

Properties of the traffic monitor:
1. Structural property: S(k) = g(min(k, H)), where g is an unknown but fixed signature encoding algorithm.
2. Injectivity: Before reaching saturation (i.e., on the set {{1, 2, ..., H}}), each different traffic volume produces a unique traffic state signature.
3. Determinism: Repeated tests with the same volume k will return exactly the same signature.
4. Observability: The signatures are encrypted. You can only deduce the network state by comparing whether signatures from different k values are identical.

From the above, we can deduce the traffic flow characteristics:
- When traffic volume k is less than the saturation threshold H, the road condition is still dynamic, so S(k) is not equal to S(k+1).
- When traffic volume k is greater than or equal to H, the road enters a fully congested, saturated state, and the signature stops changing, meaning S(k) equals S(k+1).

Your goal is: detect the precise saturation threshold H of the road network with as few tests as possible.

You can perform the following operations:
1. Probe query: Submit a test traffic volume k (a positive integer between 1 and {max_query}) to get the signature S(k).
2. Repeat query: Request the signature data from the last round for consistency verification (optional).
3. Submit answer: When you have confirmed the saturation threshold, submit a positive integer as your final determination for H.

Note: The returned signatures are opaque strings. The only usable information is determining whether signatures under different traffic volumes are equal.

Each operation must contain only one tag. Use the following XML format:

- Probe query (e.g., test volume k=5):
<query_probe>5</query_probe>

- Repeat query (repeat last return):
<query_repeat></query_repeat>

- Submit final answer (e.g., determine threshold H=7):
<answer>7</answer>
"""

    contextualized_rule_zh_2 = """\
【医疗场景】靶向药物受体饱和剂量测定
我们来进行一项临床药物剂量反应测试，规则如下：

人体对某款靶向药物存在一个未知的受体饱和剂量 H（H 在 1 到 {max_h} 之间，单位：毫克）。你拥有一个精密的生物标志物分析仪，你可以输入给药剂量 k，仪器会返回患者体内标志物图谱的哈希值 S(k)。

分析仪的特性：
1. 结构性质：S(k) = g(min(k, H))，其中 g 是未知的固定代谢映射函数。
2. 单射性质：在受体饱和前（即剂量在 {{1, 2, ..., H}} 范围内），不同的给药剂量会引发唯一的标志物图谱响应。
3. 确定性：对相同的剂量 k 重复给药分析，返回的图谱哈希值完全一致。
4. 可观测性：为了保护患者隐私，图谱被加密为哈希串，你只能通过比对不同 k 值的哈希是否完全一致来评估药效。

由此可以推导出药代动力学特性：
- 当给药剂量 k 小于饱和剂量 H 时，药物反应仍在递增，S(k) 不等于 S(k+1)。
- 当给药剂量 k 大于等于 H 时，受体达到完全饱和，增加剂量不再改变生物标志物图谱，即 S(k) 等于 S(k+1)。

你的目标是：通过尽可能少的测试次数，测定出该药物的确切饱和剂量 H。

你可以进行以下操作：
1. 试探查询：提交一个给药剂量 k（1 到 {max_query} 之间的正整数），获取图谱哈希 S(k)。
2. 复查查询：请求重复上一轮的哈希数据，用于仪器校准验证（可选）。
3. 提交答案：当你确认了受体饱和剂量后，提交该正整数作为对 H 的最终测定结果。

注意：返回的哈希串是不透明的，唯一可用的信息是判断不同给药剂量下的哈希值是否相同。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 试探查询（例如输入剂量 k=5）：
<query_probe>5</query_probe>

- 复查查询（重复上一次返回）：
<query_repeat></query_repeat>

- 提交最终答案（例如测定剂量 H=7）：
<answer>7</answer>
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario] Targeted Drug Receptor Saturation Dose Determination
Let's conduct a clinical drug dose-response test. The rules are as follows:

The human body has an unknown receptor saturation dose H for a targeted drug (H is between 1 and {max_h}, unit: mg). You operate a precise biomarker analyzer. You can input an administered dose k, and the instrument will return a hash string S(k) representing the patient's biomarker profile.

Properties of the analyzer:
1. Structural property: S(k) = g(min(k, H)), where g is an unknown but fixed metabolic mapping function.
2. Injectivity: Before receptors are saturated (i.e., on the set {{1, 2, ..., H}}), each different dose triggers a unique biomarker profile response.
3. Determinism: Repeated analysis with the same dose k will return exactly the same profile hash.
4. Observability: To protect patient privacy, profiles are encrypted into hashes. You can only evaluate efficacy by comparing whether hashes from different k values are identical.

From the above, we can deduce the pharmacokinetic characteristics:
- When dose k is less than the saturation dose H, the drug response is still increasing, so S(k) is not equal to S(k+1).
- When dose k is greater than or equal to H, receptors reach full saturation, and increasing the dose no longer changes the biomarker profile, meaning S(k) equals S(k+1).

Your goal is: determine the exact saturation dose H with as few tests as possible.

You can perform the following operations:
1. Probe query: Submit an administered dose k (a positive integer between 1 and {max_query}) to get the profile hash S(k).
2. Repeat query: Request the hash data from the last round for instrument calibration verification (optional).
3. Submit answer: When you have confirmed the receptor saturation dose, submit a positive integer as your final determination for H.

Note: The returned hashes are opaque strings. The only usable information is determining whether hashes under different doses are equal.

Each operation must contain only one tag. Use the following XML format:

- Probe query (e.g., input dose k=5):
<query_probe>5</query_probe>

- Repeat query (repeat last return):
<query_repeat></query_repeat>

- Submit final answer (e.g., determine dose H=7):
<answer>7</answer>
"""

    contextualized_rule_zh_3 = """\
【教育场景】学习者认知负荷极点评估
我们来进行一项智能教学系统的认知能力评估，规则如下：

系统正在为学生建立档案，该学生在当前模块存在一个未知的认知负荷极限 H（H 在 1 到 {max_h} 之间，单位：知识点数量）。你拥有一个自适应教学干预黑箱，你可以输入单次教授的知识点数量 k，系统会返回该学生认知状态的潜变量编码 S(k)。

教学评估黑箱的特性：
1. 结构性质：S(k) = g(min(k, H))，其中 g 是未知的学习状态映射模型。
2. 单射性质：在达到认知负荷极限前（即教授数量在 {{1, 2, ..., H}} 范围内），每个不同的知识点输入量都会反映为不同的认知吸收状态。
3. 确定性：对相同的知识点数量 k 重复测试，返回的认知状态编码完全一致。
4. 可观测性：潜变量编码是不透明的脱敏数据，你只能通过比对不同 k 值的状态编码是否完全一致来判断学生的学习状态。

由此可以推导出学习者的认知特性：
- 当教授数量 k 小于认知极限 H 时，学生仍在有效吸收新知识，认知状态不断变化，S(k) 不等于 S(k+1)。
- 当教授数量 k 大于等于极限 H 时，学生出现认知超载，无法再处理额外的信息，认知状态停止更新，即 S(k) 等于 S(k+1)。

你的目标是：通过尽可能少的教学测试，评估出该学生的精准认知负荷极限 H。

你可以进行以下操作：
1. 试探查询：提交教授的知识点数量 k（1 到 {max_query} 之间的正整数），获取认知状态编码 S(k)。
2. 复查查询：请求重复上一轮的编码数据，用于系统状态确认（可选）。
3. 提交答案：当你确认了学生的认知负荷极限后，提交该正整数作为对 H 的最终评估。

注意：返回的状态编码是脱敏字符串，唯一可用的信息是判断不同教授数量下的状态是否相同。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 试探查询（例如教授知识点 k=5）：
<query_probe>5</query_probe>

- 复查查询（重复上一次返回）：
<query_repeat></query_repeat>

- 提交最终答案（例如评估极限 H=7）：
<answer>7</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario] Learner Cognitive Load Limit Assessment
Let's conduct a cognitive ability assessment using an intelligent tutoring system. The rules are as follows:

The system is profiling a student who has an unknown cognitive load limit H for the current module (H is between 1 and {max_h}, unit: number of knowledge concepts). You operate an adaptive teaching intervention black box. You can input the number of concepts taught k, and the system will return a latent variable encoding S(k) representing the student's cognitive state.

Properties of the teaching assessment black box:
1. Structural property: S(k) = g(min(k, H)), where g is an unknown learning state mapping model.
2. Injectivity: Before reaching the cognitive load limit (i.e., on the set {{1, 2, ..., H}}), each different amount of input concepts reflects a distinct state of cognitive absorption.
3. Determinism: Repeated tests with the same number of concepts k will return exactly the same cognitive state encoding.
4. Observability: The latent variable encodings are opaque desensitized data. You can only judge the learning state by comparing whether encodings from different k values are identical.

From the above, we can deduce the learner's cognitive characteristics:
- When the number of taught concepts k is less than the cognitive limit H, the student is still effectively absorbing new knowledge, so the cognitive state keeps changing, meaning S(k) is not equal to S(k+1).
- When the number of concepts k is greater than or equal to H, the student experiences cognitive overload and cannot process extra information. The cognitive state stops updating, meaning S(k) equals S(k+1).

Your goal is: assess the precise cognitive load limit H of the student with as few teaching tests as possible.

You can perform the following operations:
1. Probe query: Submit the number of concepts taught k (a positive integer between 1 and {max_query}) to get the cognitive state encoding S(k).
2. Repeat query: Request the encoding data from the last round for system state confirmation (optional).
3. Submit answer: When you have confirmed the cognitive load limit, submit a positive integer as your final assessment for H.

Note: The returned state encodings are desensitized strings. The only usable information is determining whether states under different teaching amounts are equal.

Each operation must contain only one tag. Use the following XML format:

- Probe query (e.g., teach concepts k=5):
<query_probe>5</query_probe>

- Repeat query (repeat last return):
<query_repeat></query_repeat>

- Submit final answer (e.g., assess limit H=7):
<answer>7</answer>
"""

    contextualized_rule_zh_4 = """\
【工业制造场景】新型材料屈服强度无损检测
我们来进行一项针对新型合金材料的无损应力测试，规则如下：

该批次材料存在一个未知的屈服强度临界值 H（H 在 1 到 {max_h} 之间，单位：兆帕）。你操作一台搭载声发射传感器的伺服压力机，你可以施加指定的测试应力 k，传感器会返回材料内部结构的声发射特征码 S(k)。

材料检测系统的特性：
1. 结构性质：S(k) = g(min(k, H))，其中 g 是固定的声学特征转换算法。
2. 单射性质：在弹性形变阶段（即应力在 {{1, 2, ..., H}} 范围内），材料内部晶格随应力变化，每个应力水平都会发出独一无二的声发射特征。
3. 确定性：对相同的应力 k 重复施压，返回的声学特征码完全一致。
4. 可观测性：特征码是高度复杂的原始信号哈希，你只能通过比对不同 k 值的特征码是否完全一致来推断材料状态。

由此可以推导出材料的力学特性：
- 当施加的应力 k 小于屈服强度 H 时，材料处于弹性形变期，结构响应随应力改变，S(k) 不等于 S(k+1)。
- 当施加的应力 k 大于等于 H 时，材料进入塑性屈服阶段，声发射特征达到饱和极限不再改变，即 S(k) 等于 S(k+1)。

你的目标是：通过尽可能少的施压测试，精准定位该材料的屈服强度临界值 H。

你可以进行以下操作：
1. 试探查询：施加测试应力 k（1 到 {max_query} 之间的正整数），获取声发射特征码 S(k)。
2. 复查查询：请求重复上一轮的特征信号，用于消除传感器抖动（可选）。
3. 提交答案：当你确认了材料的屈服强度后，提交该正整数作为对 H 的最终测定。

注意：返回的特征码是不透明的，唯一可用的信息是判断不同应力下的特征是否相同。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 试探查询（例如施加应力 k=5）：
<query_probe>5</query_probe>

- 复查查询（重复上一次返回）：
<query_repeat></query_repeat>

- 提交最终答案（例如测定屈服强度 H=7）：
<answer>7</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario] Nondestructive Testing of Yield Strength for New Materials
Let's conduct a nondestructive stress test on a new batch of alloy materials. The rules are as follows:

The material batch has an unknown yield strength critical value H (H is between 1 and {max_h}, unit: MPa). You operate a servo press equipped with an acoustic emission sensor. You can apply a specified test stress k, and the sensor will return an acoustic emission feature code S(k) of the material's internal structure.

Properties of the material testing system:
1. Structural property: S(k) = g(min(k, H)), where g is a fixed acoustic feature conversion algorithm.
2. Injectivity: During the elastic deformation phase (i.e., stress on the set {{1, 2, ..., H}}), the internal lattice changes with stress, producing a unique acoustic emission feature for each stress level.
3. Determinism: Repeated pressing with the same stress k will return exactly the same acoustic feature code.
4. Observability: The feature codes are hashes of highly complex raw signals. You can only deduce the material state by comparing whether feature codes from different k values are identical.

From the above, we can deduce the material's mechanical properties:
- When applied stress k is less than the yield strength H, the material is in the elastic deformation phase, its structural response changes with stress, so S(k) is not equal to S(k+1).
- When applied stress k is greater than or equal to H, the material enters the plastic yield phase, and the acoustic emission feature reaches its saturation limit and stops changing, meaning S(k) equals S(k+1).

Your goal is: accurately pinpoint the material's yield strength critical value H with as few press tests as possible.

You can perform the following operations:
1. Probe query: Apply a test stress k (a positive integer between 1 and {max_query}) to get the acoustic emission feature code S(k).
2. Repeat query: Request the feature signal from the last round to eliminate sensor jitter (optional).
3. Submit answer: When you have confirmed the material's yield strength, submit a positive integer as your final determination for H.

Note: The returned feature codes are opaque. The only usable information is determining whether features under different stresses are equal.

Each operation must contain only one tag. Use the following XML format:

- Probe query (e.g., apply stress k=5):
<query_probe>5</query_probe>

- Repeat query (repeat last return):
<query_repeat></query_repeat>

- Submit final answer (e.g., determine yield strength H=7):
<answer>7</answer>
"""

    contextualized_rule_zh_5 = """\
【法律场景】合规监管处罚封顶阈值探明
我们来进行一项针对自动化合规裁决系统的黑盒审计，规则如下：

某项企业违规行为在现行法规中存在一个未知的法定最高处罚封顶阈值 H（H 在 1 到 {max_h} 之间，单位：严重性指数）。你拥有审计自动化裁决系统的权限，你可以输入违规严重性指数 k，系统会返回该案件的量刑分类脱敏哈希 S(k)。

裁决审计系统的特性：
1. 结构性质：S(k) = g(min(k, H))，其中 g 是未知的量刑分类映射算法。
2. 单射性质：在未触及处罚封顶线之前（即指数在 {{1, 2, ..., H}} 范围内），不同的严重性指数会导致完全不同的量刑分类。
3. 确定性：对相同的严重性指数 k 重复提交审计，系统返回的分类哈希完全一致。
4. 可观测性：由于案件保密要求，量刑分类被脱敏为哈希串，你只能通过比对不同 k 值的哈希是否完全一致来推断系统的量刑逻辑。

由此可以推导出合规裁决特性：
- 当违规指数 k 小于处罚封顶阈值 H 时，量刑标准仍在随严重性递增，S(k) 不等于 S(k+1)。
- 当违规指数 k 大于等于阈值 H 时，触发法定最高处罚上限（顶格处罚），即使指数继续增加，量刑分类也不再改变，即 S(k) 等于 S(k+1)。

你的目标是：通过尽可能少的审计查询，探明该法规中隐蔽的法定最高处罚封顶阈值 H。

你可以进行以下操作：
1. 试探查询：提交违规严重性指数 k（1 到 {max_query} 之间的正整数），获取量刑分类脱敏哈希 S(k)。
2. 复查查询：请求重复上一轮的哈希结果，用于审计日志核对（可选）。
3. 提交答案：当你确认了法定处罚封顶阈值后，提交该正整数作为对 H 的最终取证。

注意：返回的分类哈希是不透明的，唯一可用的信息是判断不同严重性指数下的哈希是否相同。

每次操作只能包含一个标签。请使用以下 XML 格式：

- 试探查询（例如提交严重性指数 k=5）：
<query_probe>5</query_probe>

- 复查查询（重复上一次返回）：
<query_repeat></query_repeat>

- 提交最终答案（例如查明封顶阈值 H=7）：
<answer>7</answer>
"""

    contextualized_rule_en_5 = """\
[Law Scenario] Compliance Regulation Penalty Cap Threshold Discovery
Let's conduct a black-box audit on an automated compliance adjudication system. The rules are as follows:

A certain corporate violation has an unknown statutory maximum penalty cap threshold H in the current regulation (H is between 1 and {max_h}, unit: severity index). You have access to audit the automated adjudication system. You can input a violation severity index k, and the system will return a desensitized hash S(k) representing the sentencing categorization of the case.

Properties of the adjudication audit system:
1. Structural property: S(k) = g(min(k, H)), where g is an unknown sentencing categorization mapping algorithm.
2. Injectivity: Before hitting the penalty cap (i.e., index on the set {{1, 2, ..., H}}), different severity indices lead to completely different sentencing categorizations.
3. Determinism: Repeated audit submissions with the same severity index k will return exactly the same categorization hash.
4. Observability: Due to case confidentiality, sentencing categories are desensitized into hashes. You can only deduce the sentencing logic by comparing whether hashes from different k values are identical.

From the above, we can deduce the compliance adjudication characteristics:
- When the violation index k is less than the penalty cap threshold H, the sentencing standard still increases with severity, so S(k) is not equal to S(k+1).
- When the violation index k is greater than or equal to H, it triggers the statutory maximum penalty limit (maximum penalty). Even if the index increases further, the sentencing categorization stops changing, meaning S(k) equals S(k+1).

Your goal is: discover the hidden statutory maximum penalty cap threshold H in the regulation with as few audit queries as possible.

You can perform the following operations:
1. Probe query: Submit a violation severity index k (a positive integer between 1 and {max_query}) to get the sentencing categorization hash S(k).
2. Repeat query: Request the hash result from the last round for audit log verification (optional).
3. Submit answer: When you have confirmed the statutory penalty cap threshold, submit a positive integer as your final evidentiary finding for H.

Note: The returned categorization hashes are opaque. The only usable information is determining whether hashes under different severity indices are equal.

Each operation must contain only one tag. Use the following XML format:

- Probe query (e.g., submit severity index k=5):
<query_probe>5</query_probe>

- Repeat query (repeat last return):
<query_repeat></query_repeat>

- Submit final answer (e.g., discover cap threshold H=7):
<answer>7</answer>
"""

    tags = ["answer", "query_probe", "query_repeat"]

    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "H": 5,
                "max_h": 20,
                "max_query": 20,
            },
            2: {
                "H": 15,
                "max_h": 50,
                "max_query": 50,
            },
            3: {
                "H": 30,
                "max_h": 100,
                "max_query": 100,
            },
            4: {
                "H": 50,
                "max_h": 150,
                "max_query": 150,
            },
            5: {
                "H": 100,
                "max_h": 300,
                "max_query": 300,
            },
        },
        "en": {
            1: {
                "H": 5,
                "max_h": 20,
                "max_query": 20,
            },
            2: {
                "H": 15,
                "max_h": 50,
                "max_query": 50,
            },
            3: {
                "H": 30,
                "max_h": 100,
                "max_query": 100,
            },
            4: {
                "H": 50,
                "max_h": 150,
                "max_query": 150,
            },
            5: {
                "H": 100,
                "max_h": 300,
                "max_query": 300,
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
        self.H = cfg["H"]
        self.max_query = cfg["max_query"]
        self.max_h = cfg["max_h"]
        
        self._game_info["max_h"] = self.max_h
        self._game_info["max_query"] = self.max_query
        
        self._salt = random.randint(0, 2**63)

        self.encoding_map = {}
        used_codes = set()
        for i in range(1, self.H + 1):
            code = self._generate_unique_code(i, used_codes)
            self.encoding_map[i] = code
            used_codes.add(code)
        
        self.encoding_map_for_large_k = self.encoding_map[self.H]
        
        self.last_response = None

    def _generate_unique_code(self, i, used_codes):
        base_str = f"code_{self._salt}_{self.H}_{i}"
        code = hashlib.sha256(base_str.encode()).hexdigest()[:16]
        
        counter = 0
        while code in used_codes:
            counter += 1
            base_str = f"code_{self._salt}_{self.H}_{i}_{counter}"
            code = hashlib.sha256(base_str.encode()).hexdigest()[:16]
        
        return code

    def _black_box_function(self, k):
        effective_value = min(k, self.H)
        return self.encoding_map[effective_value]

    def evaluate(self, parsed_info):
        try:
            answer = int(parsed_info["answer"].strip())
            return answer == self.H
        except (ValueError, KeyError):
            return False

    def _cf_core_produce(self, parsed_info):
        if "query_probe" in parsed_info:
            try:
                k = int(parsed_info["query_probe"].strip())
                
                if k < 1 or k > self.max_query:
                    if self.config.language == "zh":
                        return f"错误：k 必须在 1 到 {self.max_query} 之间。"
                    else:
                        return f"Error: k must be between 1 and {self.max_query}."
                
                response = self._black_box_function(k)
                self.last_response = response
                return response
                
            except ValueError:
                if self.config.language == "zh":
                    return "错误：无效的查询格式，k 必须是正整数。"
                else:
                    return "Error: Invalid query format, k must be a positive integer."
        
        elif "query_repeat" in parsed_info:
            if self.last_response is None:
                if self.config.language == "zh":
                    return "错误：没有可重复的查询记录。"
                else:
                    return "Error: No previous query to repeat."
            return self.last_response
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if all(c in '0123456789abcdef' for c in correct.lower()) and len(correct) >= 8:
            wrong_hash = hashlib.sha256(f"wrong_{correct}".encode()).hexdigest()[:len(correct)]
            if wrong_hash == correct:
                wrong_hash = hashlib.sha256(f"wrong2_{correct}".encode()).hexdigest()[:len(correct)]
            return wrong_hash

        if correct.lstrip('-').isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        elif self.config.language == "en":
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                pattern = "Yes" if "Yes" in correct else "yes"
                target = "No" if pattern == "Yes" else "no"
                return correct.replace(pattern, target)
            elif "no" in lower_correct:
                pattern = "No" if "No" in correct else "no"
                target = "Yes" if pattern == "No" else "yes"
                return correct.replace(pattern, target)

        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        results = []
        upper = min(2 * self.H, self.max_query)
        for k in range(1, upper + 1):
            response = self._black_box_function(k)
            results.append({
                "query": f"<query_probe>{k}</query_probe>",
                "answer": response
            })
        return results