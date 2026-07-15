from .base import Game
import random

class TreeRitualGame(Game):

    game_rule_zh = """\
我们来玩一个"树上仪式探测"的推理游戏。规则如下：

游戏设定了一个未知的树形结构 T，包含 {n} 个节点，编号为 1 到 {n}。树中存在一个未知的特殊节点 H（目标节点）。同时，存在一个未知但固定的反馈规则 R，可能是以下三种之一：

1. 规则 A（距离规则）：返回节点到目标节点 H 的距离
2. 规则 B（反转规则）：返回某个固定值 F 减去节点到 H 的距离（F 为 H 的离心率，即 H 到所有节点的最大距离）
3. 规则 C（奇偶规则）：返回节点到 H 的距离的奇偶性（0 或 1）

你的目标是通过查询推断出：反馈规则类型 R（A、B 或 C）以及目标节点 H 的编号。

你可以进行以下类型的查询（可多次，尽可能少地使用）：

1. Echo 查询：询问节点 i 的反馈值。根据实际规则 R，返回对应的非负整数。
2. Dist 查询：询问节点 i 和节点 j 之间的树上距离。返回一个非负整数。
3. Verify 查询（至多使用一次，可选）：验证节点 i 是否为目标节点 H。
   - 若正确：返回"是"，游戏继续，但你仍需识别规则 R 才算完成
   - 若错误：返回"否"，游戏立即失败

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次查询只能包含一个标签。请使用以下格式：

- Echo 查询（例如查询节点 5）：
<query_echo>5</query_echo>

- Dist 查询（例如查询节点 1 和节点 3 之间的距离）：
<query_dist>1,3</query_dist>

- Verify 查询（例如验证节点 2 是否为目标）：
<query_verify>2</query_verify>

提交最终答案时，必须说明规则类型（A、B 或 C）和目标节点编号，格式如下：
<answer>ritual=A, root=3</answer>
"""

    game_rule_en = """\
Let's play a "Tree Ritual Detection" deduction game. Here are the rules:

The game has set up an unknown tree structure T with {n} nodes, numbered from 1 to {n}. There exists an unknown special node H (target node) in the tree. Additionally, there is an unknown but fixed feedback rule R, which could be one of the following three:

1. Rule A (Distance Rule): Returns the distance from a node to the target node H
2. Rule B (Inverted Rule): Returns a fixed value F minus the distance from a node to H (F is the eccentricity of H, i.e., the maximum distance from H to all nodes)
3. Rule C (Parity Rule): Returns the parity of the distance from a node to H (0 or 1)

Your goal is to infer through queries: the feedback rule type R (A, B, or C) and the target node H's number.

You can perform the following types of queries (multiple times, use as few as possible):

1. Echo Query: Ask for the feedback value of node i. Based on the actual rule R, returns a corresponding non-negative integer.
2. Dist Query: Ask for the tree distance between node i and node j. Returns a non-negative integer.
3. Verify Query (at most once, optional): Verify whether node i is the target node H.
   - If correct: Returns "Yes", game continues, but you still need to identify rule R to complete
   - If incorrect: Returns "No", game fails immediately

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following format:

- Echo Query (e.g., querying node 5):
<query_echo>5</query_echo>

- Dist Query (e.g., querying distance between node 1 and node 3):
<query_dist>1,3</query_dist>

- Verify Query (e.g., verifying if node 2 is the target):
<query_verify>2</query_verify>

When submitting the final answer, specify the rule type (A, B, or C) and the target node number, using this format:
<answer>ritual=A, root=3</answer>
"""

    contextualized_rule_zh_1 = """\
我们正在进行一项"城市交通核心检测"任务。本市的交通路网呈现为包含 {n} 个路口（节点编号 1 到 {n}）的树状拓扑结构。网络中隐藏着一个“隐秘交通控制中心”（目标节点 H）。路网的传感器网络使用了一种未知的反馈协议 R，可能为以下三种之一：

1. 协议 A（延迟衰减）：返回该路口到控制中心 H 的网络跳数距离
2. 协议 B（信号强度）：返回网络最大覆盖半径 F 减去该路口到 H 的距离（F 为中心 H 到最边缘路口的跳数）
3. 协议 C（相位同步）：返回该路口到 H 距离的奇偶校验位（0 或 1）

你的目标是通过探测推断出：反馈协议类型 R（A、B 或 C）以及控制中心 H 的编号。

你可以进行以下类型的查询（可多次，尽可能少地使用）：

1. Echo 查询：读取路口 i 的传感器反馈值。根据实际协议 R，返回对应的非负整数。
2. Dist 查询：查询路口 i 和路口 j 之间的拓扑跳数距离。返回一个非负整数。
3. Verify 查询（至多使用一次，可选）：派遣实地稽查队验证路口 i 是否为控制中心 H。
   - 若正确：返回"是"，任务继续，但你仍需识别协议 R 才算完成
   - 若错误：返回"否"，打草惊蛇，任务立即失败

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

每次查询只能包含一个标签。请使用以下格式：

- Echo 查询（例如查询路口 5）：
<query_echo>5</query_echo>

- Dist 查询（例如查询路口 1 和路口 3 之间的距离）：
<query_dist>1,3</query_dist>

- Verify 查询（例如验证路口 2 是否为中心）：
<query_verify>2</query_verify>

提交最终答案时，必须说明协议类型（A、B 或 C）和控制中心编号，格式如下：
<answer>ritual=A, root=3</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
We are conducting an "Urban Traffic Core Detection" task. The city's road network forms a tree topology with {n} intersections (nodes numbered 1 to {n}). Hidden within is a "Secret Traffic Control Center" (target node H). The sensor network uses an unknown feedback protocol R, which could be one of the following three:

1. Protocol A (Delay Attenuation): Returns the network hop distance from the intersection to control center H
2. Protocol B (Signal Strength): Returns the maximum coverage radius F minus the distance to H (F is the max hops from H to any intersection)
3. Protocol C (Phase Synchronization): Returns the parity bit (0 or 1) of the distance to H

Your goal is to deduce through probing: the feedback protocol type R (A, B, or C) and the control center H's number.

You can perform the following types of queries (multiple times, use as few as possible):

1. Echo Query: Read the sensor feedback value for intersection i. Based on the actual protocol R, returns a corresponding non-negative integer.
2. Dist Query: Ask for the topological hop distance between intersection i and j. Returns a non-negative integer.
3. Verify Query (at most once, optional): Dispatch an inspection team to verify if intersection i is the control center H.
   - If correct: Returns "Yes", task continues, but you still need to identify protocol R to complete
   - If incorrect: Returns "No", alerting the target, task fails immediately

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following format:

- Echo Query (e.g., querying intersection 5):
<query_echo>5</query_echo>

- Dist Query (e.g., querying distance between intersection 1 and 3):
<query_dist>1,3</query_dist>

- Verify Query (e.g., verifying if intersection 2 is the center):
<query_verify>2</query_verify>

When submitting the final answer, specify the protocol type (A, B, or C) and the control center number, using this format:
<answer>ritual=A, root=3</answer>
"""

    contextualized_rule_zh_2 = """\
我们正在进行一项"传染病零号病人追踪"任务。流行病学调查显示，传播链形成了一个包含 {n} 名感染者（节点编号 1 到 {n}）的树状网络。其中存在一位未知的“零号病人”（目标节点 H）。同时，该病原体的标志物表达符合某种未知的变异规律 R，可能为以下三种之一：

1. 规律 A（代际法则）：返回该患者距离零号病人 H 的传播代数
2. 规律 B（抗体衰减）：返回最大传播深度 F 减去该患者到 H 的代数距离（F 为 H 到最末端感染者的代数）
3. 规律 C（表位交替）：返回该患者到 H 距离的奇偶性（0 或 1）

你的目标是通过检测推断出：变异规律 R（A、B 或 C）以及零号病人 H 的编号。

你可以进行以下类型的查询（可多次，尽可能少地使用）：

1. Echo 查询：检测患者 i 的标志物读数。根据实际规律 R，返回对应的非负整数。
2. Dist 查询：查询患者 i 和患者 j 之间的传播链代数距离。返回一个非负整数。
3. Verify 查询（至多使用一次，可选）：对患者 i 进行全基因组序列比对以验证其是否为零号病人。
   - 若正确：返回"是"，追踪继续，但你仍需识别规律 R 才算完成
   - 若错误：返回"否"，造成医疗资源浪费，任务立即失败

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

每次查询只能包含一个标签。请使用以下格式：

- Echo 查询（例如检测患者 5）：
<query_echo>5</query_echo>

- Dist 查询（例如查询患者 1 和患者 3 之间的距离）：
<query_dist>1,3</query_dist>

- Verify 查询（例如验证患者 2 是否为零号病人）：
<query_verify>2</query_verify>

提交最终答案时，必须说明变异规律（A、B 或 C）和零号病人编号，格式如下：
<answer>ritual=A, root=3</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
We are conducting a "Patient Zero Tracking" task. Epidemiological investigation shows a transmission chain forming a tree network of {n} infected individuals (nodes numbered 1 to {n}). There exists an unknown "Patient Zero" (target node H). The pathogen's marker expression follows an unknown mutation pattern R, which could be one of the following three:

1. Pattern A (Generational Law): Returns the transmission generations from the patient to Patient Zero H
2. Pattern B (Antibody Attenuation): Returns the maximum transmission depth F minus the distance to H (F is the max generations from H to any patient)
3. Pattern C (Epitope Alternation): Returns the parity (0 or 1) of the distance to H

Your goal is to deduce through testing: the mutation pattern R (A, B, or C) and Patient Zero H's number.

You can perform the following types of queries (multiple times, use as few as possible):

1. Echo Query: Test the marker reading for patient i. Based on the actual pattern R, returns a corresponding non-negative integer.
2. Dist Query: Ask for the transmission chain distance between patient i and j. Returns a non-negative integer.
3. Verify Query (at most once, optional): Perform whole-genome sequencing to verify if patient i is Patient Zero.
   - If correct: Returns "Yes", tracking continues, but you still need to identify pattern R to complete
   - If incorrect: Returns "No", wasting medical resources, task fails immediately

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following format:

- Echo Query (e.g., testing patient 5):
<query_echo>5</query_echo>

- Dist Query (e.g., querying distance between patient 1 and 3):
<query_dist>1,3</query_dist>

- Verify Query (e.g., verifying if patient 2 is Patient Zero):
<query_verify>2</query_verify>

When submitting the final answer, specify the mutation pattern (A, B, or C) and Patient Zero's number, using this format:
<answer>ritual=A, root=3</answer>
"""

    contextualized_rule_zh_3 = """\
我们正在进行一项"知识图谱溯源"任务。该学科包含 {n} 个知识模块（节点编号 1 到 {n}），构成了一个树状的前置依赖网络。其中存在一个未知的“核心元概念”（目标节点 H）。系统的认知负荷评估标准 R 也是未知的，可能为以下三种之一：

1. 标准 A（深度评估）：返回该模块到核心概念 H 的衍生步数
2. 标准 B（留存指数）：返回最大认知深度 F 减去该模块到 H 的衍生步数（F 为 H 到最末端模块的步数）
3. 标准 C（分类标签）：返回该模块到 H 步数的奇偶性（0 或 1）

你的目标是通过评估推断出：评估标准 R（A、B 或 C）以及核心概念 H 的编号。

你可以进行以下类型的查询（可多次，尽可能少地使用）：

1. Echo 查询：提取模块 i 的认知负荷读数。根据实际标准 R，返回对应的非负整数。
2. Dist 查询：查询模块 i 和模块 j 之间的依赖链路距离。返回一个非负整数。
3. Verify 查询（至多使用一次，可选）：开展深度教研以验证模块 i 是否为核心概念。
   - 若正确：返回"是"，溯源继续，但你仍需识别标准 R 才算完成
   - 若错误：返回"否"，教研方向偏离，任务立即失败

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

每次查询只能包含一个标签。请使用以下格式：

- Echo 查询（例如提取模块 5）：
<query_echo>5</query_echo>

- Dist 查询（例如查询模块 1 和模块 3 之间的距离）：
<query_dist>1,3</query_dist>

- Verify 查询（例如验证模块 2 是否为核心概念）：
<query_verify>2</query_verify>

提交最终答案时，必须说明评估标准（A、B 或 C）和核心概念编号，格式如下：
<answer>ritual=A, root=3</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
We are conducting a "Knowledge Graph Tracing" task. The subject contains {n} learning modules (nodes numbered 1 to {n}), forming a tree-structured prerequisite network. There exists an unknown "Core Meta-Concept" (target node H). The cognitive load evaluation standard R is also unknown, which could be one of the following three:

1. Standard A (Depth Evaluation): Returns the derivation steps from the module to the core concept H
2. Standard B (Retention Index): Returns the maximum cognitive depth F minus the steps to H (F is the max steps from H to any leaf module)
3. Standard C (Category Tag): Returns the parity (0 or 1) of the steps to H

Your goal is to deduce through assessment: the evaluation standard R (A, B, or C) and the core concept H's number.

You can perform the following types of queries (multiple times, use as few as possible):

1. Echo Query: Extract the cognitive load reading for module i. Based on the actual standard R, returns a corresponding non-negative integer.
2. Dist Query: Ask for the prerequisite link distance between module i and j. Returns a non-negative integer.
3. Verify Query (at most once, optional): Conduct in-depth research to verify if module i is the core concept.
   - If correct: Returns "Yes", tracing continues, but you still need to identify standard R to complete
   - If incorrect: Returns "No", research direction skewed, task fails immediately

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following format:

- Echo Query (e.g., assessing module 5):
<query_echo>5</query_echo>

- Dist Query (e.g., querying distance between module 1 and 3):
<query_dist>1,3</query_dist>

- Verify Query (e.g., verifying if module 2 is the core concept):
<query_verify>2</query_verify>

When submitting the final answer, specify the evaluation standard (A, B, or C) and the core concept number, using this format:
<answer>ritual=A, root=3</answer>
"""

    contextualized_rule_zh_4 = """\
我们正在进行一项"工业管网故障排查"任务。厂区的流体输送管网是一个包含 {n} 个节点（节点编号 1 到 {n}）的树状结构。管网中有一个未知的“主控泵站”（目标节点 H）。管网传感器的校准规则 R 是未知的，可能为以下三种之一：

1. 规则 A（压降检测）：返回该节点到主控泵站 H 的管道段数
2. 规则 B（静压读数）：返回系统最大扬程 F 减去该节点到 H 的管道段数（F 为 H 到最边缘节点的段数）
3. 规则 C（阀门相位）：返回该节点到 H 距离的奇偶状态（0 或 1）

你的目标是通过排查推断出：传感器校准规则 R（A、B 或 C）以及主控泵站 H 的编号。

你可以进行以下类型的查询（可多次，尽可能少地使用）：

1. Echo 查询：读取节点 i 的传感器数值。根据实际规则 R，返回对应的非负整数。
2. Dist 查询：查询节点 i 和节点 j 之间的管道段数。返回一个非负整数。
3. Verify 查询（至多使用一次，可选）：强制系统停机以验证节点 i 是否为主控泵站。
   - 若正确：返回"是"，排查继续，但你仍需识别规则 R 才算完成
   - 若错误：返回"否"，引发严重生产事故，任务立即失败

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

每次查询只能包含一个标签。请使用以下格式：

- Echo 查询（例如读取节点 5）：
<query_echo>5</query_echo>

- Dist 查询（例如查询节点 1 和节点 3 之间的管道距离）：
<query_dist>1,3</query_dist>

- Verify 查询（例如验证节点 2 是否为主控泵站）：
<query_verify>2</query_verify>

提交最终答案时，必须说明校准规则（A、B 或 C）和主控泵站编号，格式如下：
<answer>ritual=A, root=3</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
We are conducting an "Industrial Pipeline Troubleshooting" task. The plant's fluid distribution network forms a tree structure with {n} nodes (numbered 1 to {n}). There exists an unknown "Main Control Pump" (target node H). The sensor calibration rule R is unknown, which could be one of the following three:

1. Rule A (Pressure Drop): Returns the number of pipe segments from the node to control pump H
2. Rule B (Static Pressure): Returns the system's maximum head F minus the pipe segments to H (F is the max segments from H to any edge node)
3. Rule C (Valve Phase): Returns the parity state (0 or 1) of the distance to H

Your goal is to deduce through troubleshooting: the calibration rule R (A, B, or C) and the control pump H's number.

You can perform the following types of queries (multiple times, use as few as possible):

1. Echo Query: Read the sensor numerical value for node i. Based on the actual rule R, returns a corresponding non-negative integer.
2. Dist Query: Ask for the pipe segment distance between node i and j. Returns a non-negative integer.
3. Verify Query (at most once, optional): Force a system shutdown to verify if node i is the main control pump.
   - If correct: Returns "Yes", troubleshooting continues, but you still need to identify rule R to complete
   - If incorrect: Returns "No", causing a severe production accident, task fails immediately

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following format:

- Echo Query (e.g., reading node 5):
<query_echo>5</query_echo>

- Dist Query (e.g., querying distance between node 1 and 3):
<query_dist>1,3</query_dist>

- Verify Query (e.g., verifying if node 2 is the main pump):
<query_verify>2</query_verify>

When submitting the final answer, specify the calibration rule (A, B, or C) and the main pump's number, using this format:
<answer>ritual=A, root=3</answer>
"""

    contextualized_rule_zh_5 = """\
我们正在进行一项"金融洗钱网络审查"任务。资金追踪显示，涉案的 {n} 个洗钱壳公司（节点编号 1 到 {n}）构成了一个树状的股权代持网络。网络中隐藏着一名未知的“实际控制人”（目标节点 H）。账目的混淆算法 R 是未知的，可能为以下三种之一：

1. 算法 A（层级穿透）：返回该公司距离实际控制人 H 的代持层级数
2. 算法 B（资金留存）：返回网络最大深度 F 减去该公司到 H 的层级数（F 为 H 到最外围壳公司的层级数）
3. 算法 C（审计辖区）：返回该公司到 H 距离的奇偶性（0 或 1，代表境内/境外管辖）

你的目标是通过审查推断出：混淆算法 R（A、B 或 C）以及实际控制人 H 的节点编号。

你可以进行以下类型的查询（可多次，尽可能少地使用）：

1. Echo 查询：调取公司 i 的账目混淆特征值。根据实际算法 R，返回对应的非负整数。
2. Dist 查询：查询公司 i 和公司 j 之间的股权层级跨度。返回一个非负整数。
3. Verify 查询（至多使用一次，可选）：申请搜查令以确认公司 i 是否为实际控制人。
   - 若正确：返回"是"，审查继续，但你仍需识别算法 R 才算完成
   - 若错误：返回"否"，打草惊蛇导致证据销毁，任务立即失败

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，任务失败。

每次查询只能包含一个标签。请使用以下格式：

- Echo 查询（例如调取公司 5）：
<query_echo>5</query_echo>

- Dist 查询（例如查询公司 1 和公司 3 之间的层级跨度）：
<query_dist>1,3</query_dist>

- Verify 查询（例如验证公司 2 是否为实际控制人）：
<query_verify>2</query_verify>

提交最终答案时，必须说明混淆算法（A、B 或 C）和实际控制人编号，格式如下：
<answer>ritual=A, root=3</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
We are conducting a "Financial Money Laundering Network Audit". Funds tracing shows {n} shell companies (nodes numbered 1 to {n}) forming a tree-structured equity proxy network. Hidden within is an unknown "Ultimate Beneficial Owner" (UBO, target node H). The ledger obfuscation algorithm R is unknown, which could be one of the following three:

1. Algorithm A (Tier Penetration): Returns the number of proxy tiers from the company to UBO H
2. Algorithm B (Fund Retention): Returns the maximum network depth F minus the tiers to H (F is the max tiers from H to any outer shell company)
3. Algorithm C (Audit Jurisdiction): Returns the parity (0 or 1, domestic/offshore) of the distance to H

Your goal is to uncover through auditing: the obfuscation algorithm R (A, B, or C) and the UBO H's number.

You can perform the following types of queries (multiple times, use as few as possible):

1. Echo Query: Subpoena the obfuscation feature value for company i. Based on the actual algorithm R, returns a corresponding non-negative integer.
2. Dist Query: Ask for the equity tier span between company i and j. Returns a non-negative integer.
3. Verify Query (at most once, optional): Execute a search warrant to confirm if company i is the UBO.
   - If correct: Returns "Yes", audit continues, but you still need to identify algorithm R to complete
   - If incorrect: Returns "No", alerting suspects and causing evidence destruction, task fails immediately

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the task fails.

Each query must contain only one tag. Use the following format:

- Echo Query (e.g., subpoenaing company 5):
<query_echo>5</query_echo>

- Dist Query (e.g., querying tier span between company 1 and 3):
<query_dist>1,3</query_dist>

- Verify Query (e.g., verifying if company 2 is the UBO):
<query_verify>2</query_verify>

When submitting the final answer, specify the obfuscation algorithm (A, B, or C) and the UBO's number, using this format:
<answer>ritual=A, root=3</answer>
"""

    tags = ["answer", "query_echo", "query_dist", "query_verify"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "target": 3,
                "rule": "A"
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "target": 1,
                "rule": "C"
            },
            3: {
                "n": 8,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8)],
                "target": 2,
                "rule": "A"
            },
            4: {
                "n": 9,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7), (6, 8), (8, 9)],
                "target": 6,
                "rule": "B"
            },
            5: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (1, 8), (8, 9), (9, 10)],
                "target": 3,
                "rule": "B"
            }
        },
        "en": {
            1: {
                "n": 5,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5)],
                "target": 3,
                "rule": "A"
            },
            2: {
                "n": 7,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7)],
                "target": 1,
                "rule": "C"
            },
            3: {
                "n": 8,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (7, 8)],
                "target": 2,
                "rule": "A"
            },
            4: {
                "n": 9,
                "edges": [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (6, 7), (6, 8), (8, 9)],
                "target": 6,
                "rule": "B"
            },
            5: {
                "n": 10,
                "edges": [(1, 2), (2, 3), (3, 4), (4, 5), (3, 6), (6, 7), (1, 8), (8, 9), (9, 10)],
                "target": 3,
                "rule": "B"
            }
        }
    }

    def __init__(self, config):
        self.verify_used = False
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = int(self.config.difficulty)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        self._game_info["n"] = cfg["n"]
        
        self.n = cfg["n"]
        self.edges = cfg["edges"]
        self.target = cfg["target"]
        self.rule = cfg["rule"]
        
        self.adj = {i: [] for i in range(1, self.n + 1)}
        for u, v in self.edges:
            self.adj[u].append(v)
            self.adj[v].append(u)
        
        self.dist_matrix = {}
        for start in range(1, self.n + 1):
            self.dist_matrix[start] = self._bfs_distances(start)
        
        self.F = max(self.dist_matrix[self.target].values())

    def _bfs_distances(self, start):
        from collections import deque
        dist = {start: 0}
        queue = deque([start])
        
        while queue:
            u = queue.popleft()
            for v in self.adj[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        
        return dist

    def _get_echo_value(self, node):
        d = self.dist_matrix[self.target][node]
        
        if self.rule == "A":
            return d
        elif self.rule == "B":
            return self.F - d
        elif self.rule == "C":
            return d % 2
        else:
            raise ValueError(f"Unknown rule: {self.rule}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            parts = kv.split("=", 1)
            if len(parts) == 2:
                ans_dict[parts[0].strip()] = parts[1].strip()
        
        if "ritual" not in ans_dict or "root" not in ans_dict:
            return False
        
        if ans_dict["ritual"].upper() != self.rule:
            return False
        
        try:
            guessed_root = int(ans_dict["root"])
            return guessed_root == self.target
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_format = "错误：格式无效或节点编号错误。"
            error_range = "错误：节点编号超出范围。"
            error_verify = "错误：Verify 查询只能使用一次。"
        else:
            yes_res, no_res = "Yes", "No"
            error_format = "Error: Invalid format or node number."
            error_range = "Error: Node number out of range."
            error_verify = "Error: Verify query can only be used once."

        if "query_echo" in parsed_info:
            try:
                node = int(parsed_info["query_echo"].strip())
                if node < 1 or node > self.n:
                    return error_range
                return str(self._get_echo_value(node))
            except:
                return error_format

        elif "query_dist" in parsed_info:
            try:
                raw = parsed_info["query_dist"]
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    return error_format
                node1, node2 = int(parts[0]), int(parts[1])
                if node1 < 1 or node1 > self.n or node2 < 1 or node2 > self.n:
                    return error_range
                return str(self.dist_matrix[node1][node2])
            except:
                return error_format

        elif "query_verify" in parsed_info:
            if self.verify_used:
                return error_verify
            self.verify_used = True
            
            try:
                node = int(parsed_info["query_verify"].strip())
                if node < 1 or node > self.n:
                    return error_range
                
                if node == self.target:
                    return yes_res
                else:
                    if not getattr(self, "enable_counterfactual", False):
                        self.state.set_state("failed", "verify failed")
                    return no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        mapping = {
            "是": "否",
            "否": "是",
            "Yes": "No",
            "No": "Yes"
        }
        
        if correct in mapping:
            return mapping[correct]
        
        correct_lower = correct.lower()
        if correct_lower == "yes": return "No"
        if correct_lower == "no": return "Yes"
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        if self.config.language == "zh":
            yes_res = "是"
        else:
            yes_res = "Yes"

        for i in range(1, self.n + 1):
            query_str = f"<query_echo>{i}</query_echo>"
            answer = str(self._get_echo_value(i))
            queries.append({"query": query_str, "answer": answer})

        for i in range(1, self.n + 1):
            for j in range(i + 1, self.n + 1):
                query_str = f"<query_dist>{i},{j}</query_dist>"
                answer = str(self.dist_matrix[i][j])
                queries.append({"query": query_str, "answer": answer})

        query_str = f"<query_verify>{self.target}</query_verify>"
        queries.append({"query": query_str, "answer": yes_res})

        return queries