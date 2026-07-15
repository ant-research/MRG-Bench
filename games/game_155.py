from .base import Game
import re

class GraphReachabilityGame(Game):

    game_rule_zh = """\
我们现在来玩一个"标记有向图推理"的游戏，规则如下：

游戏设定了一个带标签的有向图，节点集合为 {{A, B, C, D, E}}，标签集合为 {{红, 蓝, 绿}}。每个节点对每个标签恰有一条确定的出边（可能为自环）。

实际的图结构从若干个候选方案之一产生（称为 W1、W2、W3、W4 等），且在整个交互过程中固定不变。候选方案如下：

{candidate_schemes}

你的任务是通过查询推断出真实的图方案。

你可以反复进行以下查询（每次仅限一个查询）：

**出边查询**：指定一个节点（A/B/C/D/E）和一个标签（红/蓝/绿），我会告诉你该节点经该标签的出边所指向的节点。

你的最终目标是：
1. 确定真实的图方案编号（W1、W2、W3 或 W4）
2. 判断节点 A 与节点 E 是否互相可达，即是否同时存在从 A 到 E 的有向路径与从 E 到 A 的有向路径

每次查询只能包含一个标签。请使用以下 XML 格式：

- 出边查询（例如查询节点 A 在标签红下的出边）：
<query_edge>A,红</query_edge>

提交最终答案时，必须说明方案编号和互相可达性，格式如下：

- 若判断互相可达：
<answer>方案=W1, 互相可达=是, A到E=红-蓝, E到A=绿-红-蓝</answer>

- 若判断不可达：
<answer>方案=W2, 互相可达=否</answer>

注意：
- 路径用标签序列表示，标签之间用短横线分隔
- 请尽可能少地进行查询
"""

    game_rule_en = """\
Let's play a "Labeled Directed Graph Deduction" game. Here are the rules:

The game features a labeled directed graph with node set {{A, B, C, D, E}} and label set {{Red, Blue, Green}}. Each node has exactly one outgoing edge for each label (possibly a self-loop).

The actual graph structure is generated from one of several candidate schemes (called W1, W2, W3, W4, etc.) and remains fixed throughout the interaction. The candidate schemes are as follows:

{candidate_schemes}

Your task is to infer the true graph scheme through queries.

You can repeatedly make the following query (one at a time):

**Edge Query**: Specify a node (A/B/C/D/E) and a label (Red/Blue/Green), and I will tell you which node this edge points to.

Your ultimate goals are:
1. Determine the true graph scheme number (W1, W2, W3, or W4)
2. Determine whether nodes A and E are mutually reachable, i.e., whether there exists both a directed path from A to E and a directed path from E to A

Each query must contain only one tag. Use the following XML format:

- Edge Query (e.g., querying node A with label Red):
<query_edge>A,Red</query_edge>

When submitting the final answer, specify the scheme number and mutual reachability using this format:

- If judged mutually reachable:
<answer>scheme=W1, mutually_reachable=yes, A_to_E=Red-Blue, E_to_A=Green-Red-Blue</answer>

- If judged not reachable:
<answer>scheme=W2, mutually_reachable=no</answer>

Notes:
- Paths are represented by label sequences, with labels separated by hyphens
- Try to minimize the number of queries
"""

    contextualized_rule_zh_1 = """\
欢迎使用“城市交通线网排查”系统。

本系统设定了一个包含5个核心交通枢纽的线网，枢纽集合为 {{A, B, C, D, E}}，运营线路标记为 {{红, 蓝, 绿}}。每个枢纽针对每种颜色的线路都有且仅有一个确定的下一站（可能原地环线）。

实际的线网结构由若干个候选方案之一产生（称为 W1、W2、W3、W4 等），且在整个排查过程中固定不变。候选方案如下：

{candidate_schemes}

你的任务是通过乘车查询推断出正在运行的真实线网方案。

你可以反复进行以下查询（每次仅限一个查询）：

**路线勘测**：指定一个枢纽（A/B/C/D/E）和一条线路（红/蓝/绿），我会告诉你乘坐该线路后抵达的下一个枢纽。

你的最终目标是：
1. 确定真实的线网方案编号（W1、W2、W3 或 W4）
2. 判断枢纽 A 与枢纽 E 是否互相可达，即是否同时存在从 A 到 E 的换乘路径与从 E 到 A 的换乘路径

每次查询只能包含一条线路。请使用以下 XML 格式：

- 路线勘测（例如查询在枢纽 A 乘坐红线抵达的枢纽）：
<query_edge>A,红</query_edge>

提交最终答案时，必须说明方案编号和互相可达性，格式如下：

- 若判断互相可达：
<answer>方案=W1, 互相可达=是, A到E=红-蓝, E到A=绿-红-蓝</answer>

- 若判断不可达：
<answer>方案=W2, 互相可达=否</answer>

注意：
- 路径用线路序列表示，线路之间用短横线分隔
- 请尽可能少地进行查询
"""

    contextualized_rule_en_1 = """\
[Urban Transit Network Inspection Scenario]
Welcome to the "Urban Transit Network Inspection" system.

The system features a network of 5 core transit hubs, with the hub set {{A, B, C, D, E}} and operating transit lines labeled {{Red, Blue, Green}}. Each hub has exactly one definitive next stop for each colored line (possibly a self-loop).

The actual network structure is generated from one of several candidate schemes (called W1, W2, W3, W4, etc.) and remains fixed throughout the inspection. The candidate schemes are as follows:

{candidate_schemes}

Your task is to infer the true operating network scheme through transit queries.

You can repeatedly make the following query (one at a time):

**Route Survey**: Specify a hub (A/B/C/D/E) and a line (Red/Blue/Green), and I will tell you the next hub you will arrive at by taking that line.

Your ultimate goals are:
1. Determine the true network scheme number (W1, W2, W3, or W4)
2. Determine whether hubs A and E are mutually reachable, i.e., whether there exists both a transit path from A to E and a transit path from E to A

Each query must contain only one line tag. Use the following XML format:

- Route Survey (e.g., querying the hub reached from hub A via the Red line):
<query_edge>A,Red</query_edge>

When submitting the final answer, specify the scheme number and mutual reachability using this format:

- If judged mutually reachable:
<answer>scheme=W1, mutually_reachable=yes, A_to_E=Red-Blue, E_to_A=Green-Red-Blue</answer>

- If judged not reachable:
<answer>scheme=W2, mutually_reachable=no</answer>

Notes:
- Paths are represented by line sequences, separated by hyphens
- Try to minimize the number of queries
"""

    contextualized_rule_zh_2 = """\
欢迎使用“疾病状态转移预测”系统。

本系统设定了一个特定病理模型的转归图，患者的生理状态集合为 {{A, B, C, D, E}}，可采用的医疗干预手段标记为 {{红, 蓝, 绿}}。每个状态在接受每种干预后恰有一条确定的转归路径（指向下一个状态，或维持原状）。

实际的转归图结构从若干个候选诊疗方案之一产生（称为 W1、W2、W3、W4 等），且在整个诊断交互过程中固定不变。候选方案如下：

{candidate_schemes}

你的任务是通过干预测试推断出真实的转归方案。

你可以反复进行以下查询（每次仅限一个查询）：

**干预测试**：指定一个状态（A/B/C/D/E）和一种干预手段（红/蓝/绿），我会告诉你实施该干预后患者转归到的生理状态。

你的最终目标是：
1. 确定真实的转归方案编号（W1、W2、W3 或 W4）
2. 判断状态 A 与状态 E 是否互相可达，即是否同时存在从 A 恶化/好转至 E 的治疗路径，以及从 E 恢复至 A 的治疗路径

每次查询只能包含一种干预手段。请使用以下 XML 格式：

- 干预测试（例如查询在状态 A 下施加红手段后的状态）：
<query_edge>A,红</query_edge>

提交最终答案时，必须说明方案编号和互相可达性，格式如下：

- 若判断互相可达：
<answer>方案=W1, 互相可达=是, A到E=红-蓝, E到A=绿-红-蓝</answer>

- 若判断不可达：
<answer>方案=W2, 互相可达=否</answer>

注意：
- 路径用干预手段序列表示，手段之间用短横线分隔
- 请尽可能少地进行查询
"""

    contextualized_rule_en_2 = """\
[Disease State Transition Prediction Scenario]
Welcome to the "Disease State Transition Prediction" system.

The system features a pathological model transition graph, with the patient's physiological state set {{A, B, C, D, E}} and medical interventions labeled {{Red, Blue, Green}}. Each state has exactly one definite transition path upon receiving each intervention (pointing to the next state, or maintaining the status quo).

The actual transition graph structure is generated from one of several candidate diagnostic schemes (called W1, W2, W3, W4, etc.) and remains fixed throughout the interaction. The candidate schemes are as follows:

{candidate_schemes}

Your task is to infer the true transition scheme through intervention tests.

You can repeatedly make the following query (one at a time):

**Intervention Test**: Specify a state (A/B/C/D/E) and an intervention (Red/Blue/Green), and I will tell you the physiological state the patient transitions to after this intervention.

Your ultimate goals are:
1. Determine the true transition scheme number (W1, W2, W3, or W4)
2. Determine whether states A and E are mutually reachable, i.e., whether there exists both a treatment path from A to E and a treatment path from E to A

Each query must contain only one intervention tag. Use the following XML format:

- Intervention Test (e.g., querying the state reached from state A via the Red intervention):
<query_edge>A,Red</query_edge>

When submitting the final answer, specify the scheme number and mutual reachability using this format:

- If judged mutually reachable:
<answer>scheme=W1, mutually_reachable=yes, A_to_E=Red-Blue, E_to_A=Green-Red-Blue</answer>

- If judged not reachable:
<answer>scheme=W2, mutually_reachable=no</answer>

Notes:
- Paths are represented by intervention sequences, separated by hyphens
- Try to minimize the number of queries
"""

    contextualized_rule_zh_3 = """\
欢迎使用“自适应学习路径评估”系统。

本系统设定了一个学习者能力跃迁图，认知阶段集合为 {{A, B, C, D, E}}，教学模块标记为 {{红, 蓝, 绿}}。每个认知阶段在完成每个教学模块后恰有一条确定的进阶路径（可能未获提升而保持原状）。

实际的能力跃迁图结构从若干个候选教研方案之一产生（称为 W1、W2、W3、W4 等），且在整个评估过程中固定不变。候选方案如下：

{candidate_schemes}

你的任务是通过教学反馈推断出真实的教研方案。

你可以反复进行以下查询（每次仅限一个查询）：

**教学反馈**：指定一个认知阶段（A/B/C/D/E）和一个教学模块（红/蓝/绿），我会告诉你完成该模块后学习者达到的新认知阶段。

你的最终目标是：
1. 确定真实的教研方案编号（W1、W2、W3 或 W4）
2. 判断阶段 A 与阶段 E 是否互相可达，即是否同时存在从 A 进阶到 E 的学习路径与从 E 回溯至 A 的学习路径

每次查询只能包含一个模块。请使用以下 XML 格式：

- 教学反馈（例如查询在阶段 A 完成红模块后的阶段）：
<query_edge>A,红</query_edge>

提交最终答案时，必须说明方案编号和互相可达性，格式如下：

- 若判断互相可达：
<answer>方案=W1, 互相可达=是, A到E=红-蓝, E到A=绿-红-蓝</answer>

- 若判断不可达：
<answer>方案=W2, 互相可达=否</answer>

注意：
- 路径用模块序列表示，模块之间用短横线分隔
- 请尽可能少地进行查询
"""

    contextualized_rule_en_3 = """\
[Adaptive Learning Path Assessment Scenario]
Welcome to the "Adaptive Learning Path Assessment" system.

The system features a learner capability transition graph, with the cognitive stage set {{A, B, C, D, E}} and teaching modules labeled {{Red, Blue, Green}}. Each stage has exactly one definite progression path after completing each module (possibly remaining unchanged).

The actual capability transition graph structure is generated from one of several candidate teaching schemes (called W1, W2, W3, W4, etc.) and remains fixed throughout the assessment. The candidate schemes are as follows:

{candidate_schemes}

Your task is to infer the true teaching scheme through pedagogical feedbacks.

You can repeatedly make the following query (one at a time):

**Pedagogical Feedback**: Specify a cognitive stage (A/B/C/D/E) and a module (Red/Blue/Green), and I will tell you the new cognitive stage the learner reaches after completing this module.

Your ultimate goals are:
1. Determine the true teaching scheme number (W1, W2, W3, or W4)
2. Determine whether stages A and E are mutually reachable, i.e., whether there exists both a learning path from A to E and a path from E to A

Each query must contain only one module tag. Use the following XML format:

- Pedagogical Feedback (e.g., querying the stage reached from stage A via the Red module):
<query_edge>A,Red</query_edge>

When submitting the final answer, specify the scheme number and mutual reachability using this format:

- If judged mutually reachable:
<answer>scheme=W1, mutually_reachable=yes, A_to_E=Red-Blue, E_to_A=Green-Red-Blue</answer>

- If judged not reachable:
<answer>scheme=W2, mutually_reachable=no</answer>

Notes:
- Paths are represented by module sequences, separated by hyphens
- Try to minimize the number of queries
"""

    contextualized_rule_zh_4 = """\
欢迎使用“工业控制逻辑调试”系统。

本系统设定了一个自动化设备的有限状态机，设备运行状态集合为 {{A, B, C, D, E}}，控制指令标记为 {{红, 蓝, 绿}}。每个状态在接收每种指令后恰有一条确定的状态跳转规则（可能无响应而维持原状）。

实际的控制逻辑从若干个候选配置方案之一产生（称为 W1、W2、W3、W4 等），且在整个调试交互过程中固定不变。候选方案如下：

{candidate_schemes}

你的任务是通过指令测试推断出设备的真实控制逻辑方案。

你可以反复进行以下查询（每次仅限一个查询）：

**指令测试**：指定一个状态（A/B/C/D/E）和一种指令（红/蓝/绿），我会告诉你设备接收该指令后跳转到的新状态。

你的最终目标是：
1. 确定真实的配置方案编号（W1、W2、W3 或 W4）
2. 判断状态 A 与状态 E 是否互相可达，即是否同时存在从 A 切换至 E 的指令序列与从 E 切换回 A 的指令序列

每次查询只能包含一种指令。请使用以下 XML 格式：

- 指令测试（例如查询在状态 A 接收红指令后的状态）：
<query_edge>A,红</query_edge>

提交最终答案时，必须说明方案编号和互相可达性，格式如下：

- 若判断互相可达：
<answer>方案=W1, 互相可达=是, A到E=红-蓝, E到A=绿-红-蓝</answer>

- 若判断不可达：
<answer>方案=W2, 互相可达=否</answer>

注意：
- 路径用指令序列表示，指令之间用短横线分隔
- 请尽可能少地进行查询
"""

    contextualized_rule_en_4 = """\
[Industrial Control Logic Debugging Scenario]
Welcome to the "Industrial Control Logic Debugging" system.

The system features a finite state machine for automated equipment, with the operating state set {{A, B, C, D, E}} and control commands labeled {{Red, Blue, Green}}. Each state has exactly one definite state transition rule upon receiving each command (possibly maintaining the status quo).

The actual control logic is generated from one of several candidate configuration schemes (called W1, W2, W3, W4, etc.) and remains fixed throughout the debugging. The candidate schemes are as follows:

{candidate_schemes}

Your task is to infer the true control logic scheme through command tests.

You can repeatedly make the following query (one at a time):

**Command Test**: Specify a state (A/B/C/D/E) and a command (Red/Blue/Green), and I will tell you the new state the equipment transitions to after receiving this command.

Your ultimate goals are:
1. Determine the true configuration scheme number (W1, W2, W3, or W4)
2. Determine whether states A and E are mutually reachable, i.e., whether there exists both a command sequence from A to E and a command sequence from E to A

Each query must contain only one command tag. Use the following XML format:

- Command Test (e.g., querying the state reached from state A via the Red command):
<query_edge>A,Red</query_edge>

When submitting the final answer, specify the scheme number and mutual reachability using this format:

- If judged mutually reachable:
<answer>scheme=W1, mutually_reachable=yes, A_to_E=Red-Blue, E_to_A=Green-Red-Blue</answer>

- If judged not reachable:
<answer>scheme=W2, mutually_reachable=no</answer>

Notes:
- Paths are represented by command sequences, separated by hyphens
- Try to minimize the number of queries
"""

    contextualized_rule_zh_5 = """\
欢迎使用“司法程序流转沙盘”系统。

本系统设定了一个案件审理流程图，案件所处的程序节点集合为 {{A, B, C, D, E}}，当事人可采取的法律行动标记为 {{红, 蓝, 绿}}。每个程序节点在介入每种法律行动后恰有一个确定的后续程序节点（可能维持原判或停留在原节点）。

实际的流转结构从若干个候选诉讼方案之一产生（称为 W1、W2、W3、W4 等），且在整个推演过程中固定不变。候选方案如下：

{candidate_schemes}

你的任务是通过推演查询推断出真实的司法程序流转方案。

你可以反复进行以下查询（每次仅限一个查询）：

**程序推演**：指定一个节点（A/B/C/D/E）和一种法律行动（红/蓝/绿），我会告诉你采取该行动后案件所进入的新节点。

你的最终目标是：
1. 确定真实的诉讼方案编号（W1、W2、W3 或 W4）
2. 判断节点 A 与节点 E 是否互相可达，即是否同时存在从 A 流转至 E 的行动路径与从 E 回到 A 的行动路径

每次查询只能包含一种行动。请使用以下 XML 格式：

- 程序推演（例如查询在节点 A 采取红行动后的节点）：
<query_edge>A,红</query_edge>

提交最终答案时，必须说明方案编号和互相可达性，格式如下：

- 若判断互相可达：
<answer>方案=W1, 互相可达=是, A到E=红-蓝, E到A=绿-红-蓝</answer>

- 若判断不可达：
<answer>方案=W2, 互相可达=否</answer>

注意：
- 路径用行动序列表示，行动之间用短横线分隔
- 请尽可能少地进行查询
"""

    contextualized_rule_en_5 = """\
[Judicial Procedure Flow Sandbox Scenario]
Welcome to the "Judicial Procedure Flow Sandbox" system.

The system features a case trial flow graph, with the procedural node set {{A, B, C, D, E}} and available legal actions labeled {{Red, Blue, Green}}. Each procedural node has exactly one definite subsequent node upon taking each legal action (possibly maintaining the current status).

The actual flow structure is generated from one of several candidate litigation schemes (called W1, W2, W3, W4, etc.) and remains fixed throughout the sandbox interaction. The candidate schemes are as follows:

{candidate_schemes}

Your task is to infer the true litigation scheme through deduction queries.

You can repeatedly make the following query (one at a time):

**Procedure Deduction**: Specify a node (A/B/C/D/E) and an action (Red/Blue/Green), and I will tell you the new node the case enters after taking this action.

Your ultimate goals are:
1. Determine the true litigation scheme number (W1, W2, W3, or W4)
2. Determine whether nodes A and E are mutually reachable, i.e., whether there exists both an action path from A to E and an action path from E to A

Each query must contain only one action tag. Use the following XML format:

- Procedure Deduction (e.g., querying the node reached from node A via the Red action):
<query_edge>A,Red</query_edge>

When submitting the final answer, specify the scheme number and mutual reachability using this format:

- If judged mutually reachable:
<answer>scheme=W1, mutually_reachable=yes, A_to_E=Red-Blue, E_to_A=Green-Red-Blue</answer>

- If judged not reachable:
<answer>scheme=W2, mutually_reachable=no</answer>

Notes:
- Paths are represented by action sequences, separated by hyphens
- Try to minimize the number of queries
"""

    tags = ["answer", "query_edge"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "scheme": "W1",
                "graph": {
                    "A": {"红": "B", "蓝": "C", "绿": "A"},
                    "B": {"红": "D", "蓝": "A", "绿": "B"},
                    "C": {"红": "B", "蓝": "E", "绿": "C"},
                    "D": {"红": "E", "蓝": "B", "绿": "D"},
                    "E": {"红": "D", "蓝": "C", "绿": "E"},
                },
                "mutually_reachable": True,
                "a_to_e": ["红", "红", "红"],
                "e_to_a": ["红", "蓝", "蓝"],
            },
            2: {
                "scheme": "W2",
                "graph": {
                    "A": {"红": "B", "蓝": "C", "绿": "A"},
                    "B": {"红": "D", "蓝": "A", "绿": "B"},
                    "C": {"红": "B", "蓝": "E", "绿": "C"},
                    "D": {"红": "E", "蓝": "E", "绿": "D"},
                    "E": {"红": "D", "蓝": "E", "绿": "E"},
                },
                "mutually_reachable": False,
                "a_to_e": ["红", "红", "红"],
                "e_to_a": None,
            },
            3: {
                "scheme": "W3",
                "graph": {
                    "A": {"红": "B", "蓝": "C", "绿": "A"},
                    "B": {"红": "D", "蓝": "A", "绿": "B"},
                    "C": {"红": "B", "蓝": "C", "绿": "C"},
                    "D": {"红": "E", "蓝": "B", "绿": "D"},
                    "E": {"红": "D", "蓝": "C", "绿": "E"},
                },
                "mutually_reachable": True,
                "a_to_e": ["红", "红", "红"],
                "e_to_a": ["蓝", "红", "蓝"],
            },
            4: {
                "scheme": "W4",
                "graph": {
                    "A": {"红": "B", "蓝": "C", "绿": "A"},
                    "B": {"红": "A", "蓝": "A", "绿": "B"},
                    "C": {"红": "B", "蓝": "C", "绿": "C"},
                    "D": {"红": "E", "蓝": "E", "绿": "D"},
                    "E": {"红": "D", "蓝": "E", "绿": "E"},
                },
                "mutually_reachable": False,
                "a_to_e": None,
                "e_to_a": None,
            },
            5: {
                "scheme": "W5",
                "graph": {
                    "A": {"红": "B", "蓝": "D", "绿": "A"},
                    "B": {"红": "C", "蓝": "E", "绿": "A"},
                    "C": {"红": "D", "蓝": "B", "绿": "C"},
                    "D": {"红": "E", "蓝": "C", "绿": "D"},
                    "E": {"红": "A", "蓝": "D", "绿": "E"},
                },
                "mutually_reachable": True,
                "a_to_e": ["红", "蓝"],
                "e_to_a": ["红"],
            },
        },
        "en": {
            1: {
                "scheme": "W1",
                "graph": {
                    "A": {"Red": "B", "Blue": "C", "Green": "A"},
                    "B": {"Red": "D", "Blue": "A", "Green": "B"},
                    "C": {"Red": "B", "Blue": "E", "Green": "C"},
                    "D": {"Red": "E", "Blue": "B", "Green": "D"},
                    "E": {"Red": "D", "Blue": "C", "Green": "E"},
                },
                "mutually_reachable": True,
                "a_to_e": ["Red", "Red", "Red"],
                "e_to_a": ["Red", "Blue", "Blue"],
            },
            2: {
                "scheme": "W2",
                "graph": {
                    "A": {"Red": "B", "Blue": "C", "Green": "A"},
                    "B": {"Red": "D", "Blue": "A", "Green": "B"},
                    "C": {"Red": "B", "Blue": "E", "Green": "C"},
                    "D": {"Red": "E", "Blue": "E", "Green": "D"},
                    "E": {"Red": "D", "Blue": "E", "Green": "E"},
                },
                "mutually_reachable": False,
                "a_to_e": ["Red", "Red", "Red"],
                "e_to_a": None,
            },
            3: {
                "scheme": "W3",
                "graph": {
                    "A": {"Red": "B", "Blue": "C", "Green": "A"},
                    "B": {"Red": "D", "Blue": "A", "Green": "B"},
                    "C": {"Red": "B", "Blue": "C", "Green": "C"},
                    "D": {"Red": "E", "Blue": "B", "Green": "D"},
                    "E": {"Red": "D", "Blue": "C", "Green": "E"},
                },
                "mutually_reachable": True,
                "a_to_e": ["Red", "Red", "Red"],
                "e_to_a": ["Blue", "Red", "Blue"],
            },
            4: {
                "scheme": "W4",
                "graph": {
                    "A": {"Red": "B", "Blue": "C", "Green": "A"},
                    "B": {"Red": "A", "Blue": "A", "Green": "B"},
                    "C": {"Red": "B", "Blue": "C", "Green": "C"},
                    "D": {"Red": "E", "Blue": "E", "Green": "D"},
                    "E": {"Red": "D", "Blue": "E", "Green": "E"},
                },
                "mutually_reachable": False,
                "a_to_e": None,
                "e_to_a": None,
            },
            5: {
                "scheme": "W5",
                "graph": {
                    "A": {"Red": "B", "Blue": "D", "Green": "A"},
                    "B": {"Red": "C", "Blue": "E", "Green": "A"},
                    "C": {"Red": "D", "Blue": "B", "Green": "C"},
                    "D": {"Red": "E", "Blue": "C", "Green": "D"},
                    "E": {"Red": "A", "Blue": "D", "Green": "E"},
                },
                "mutually_reachable": True,
                "a_to_e": ["Red", "Blue"],
                "e_to_a": ["Red"],
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
        
        self.scheme = cfg["scheme"]
        self.graph = cfg["graph"]
        self.mutually_reachable = cfg["mutually_reachable"]
        self.a_to_e_path = cfg.get("a_to_e")
        self.e_to_a_path = cfg.get("e_to_a")
        
        all_schemes = self.DIFFICULTY_CONFIG[lang]
        scheme_descriptions = []
        for d, s_cfg in sorted(all_schemes.items()):
            desc_lines = [f"{s_cfg['scheme']}:"]
            for node in ["A", "B", "C", "D", "E"]:
                edges = s_cfg["graph"][node]
                for label, target in edges.items():
                    desc_lines.append(f"  {node} --{label}--> {target}")
            scheme_descriptions.append("\n".join(desc_lines))
        
        self._game_info = {
            "candidate_schemes": "\n\n".join(scheme_descriptions)
        }

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        raw_ans = raw_ans.replace("，", ",")
        
        ans_dict = {}
        
        if self.config.language == "zh":
            parts = [x.strip() for x in raw_ans.split(",")]
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if ans_dict.get("方案") != self.scheme:
                return False
            
            reachable_answer = ans_dict.get("互相可达")
            if reachable_answer == "是":
                if not self.mutually_reachable:
                    return False
                a_to_e = ans_dict.get("A到E", "")
                e_to_a = ans_dict.get("E到A", "")
                if not a_to_e or not e_to_a:
                    return False
                a_to_e_labels = [x.strip() for x in a_to_e.split("-") if x.strip()]
                e_to_a_labels = [x.strip() for x in e_to_a.split("-") if x.strip()]
                return self._verify_path("A", "E", a_to_e_labels) and self._verify_path("E", "A", e_to_a_labels)
            elif reachable_answer == "否":
                return not self.mutually_reachable
            else:
                return False
        else:
            parts = [x.strip() for x in raw_ans.split(",")]
            for part in parts:
                if "=" in part:
                    k, v = part.split("=", 1)
                    ans_dict[k.strip()] = v.strip()
            
            if ans_dict.get("scheme") != self.scheme:
                return False
            
            reachable_answer = ans_dict.get("mutually_reachable")
            if reachable_answer == "yes":
                if not self.mutually_reachable:
                    return False
                a_to_e = ans_dict.get("A_to_E", "")
                e_to_a = ans_dict.get("E_to_A", "")
                if not a_to_e or not e_to_a:
                    return False
                a_to_e_labels = [x.strip() for x in a_to_e.split("-") if x.strip()]
                e_to_a_labels = [x.strip() for x in e_to_a.split("-") if x.strip()]
                return self._verify_path("A", "E", a_to_e_labels) and self._verify_path("E", "A", e_to_a_labels)
            elif reachable_answer == "no":
                return not self.mutually_reachable
            else:
                return False

    def _verify_path(self, start, end, labels):
        current = start
        for label in labels:
            if current not in self.graph or label not in self.graph[current]:
                return False
            current = self.graph[current][label]
        return current == end

    def _cf_core_produce(self, parsed_info):
        if "query_edge" in parsed_info:
            query = parsed_info["query_edge"].strip()
            try:
                parts = [x.strip() for x in query.split(",")]
                if len(parts) != 2:
                    raise ValueError
                
                node, label = parts[0], parts[1]
                
                if node not in self.graph:
                    if self.config.language == "zh":
                        return f"错误：节点 {node} 不在集合 {{A, B, C, D, E}} 中。"
                    else:
                        return f"Error: Node {node} is not in set {{A, B, C, D, E}}."
                
                if label not in self.graph[node]:
                    if self.config.language == "zh":
                        return f"错误：标签 {label} 不在集合 {{红, 蓝, 绿}} 中。"
                    else:
                        return f"Error: Label {label} is not in set {{Red, Blue, Green}}."
                
                target = self.graph[node][label]
                return target
                
            except:
                if self.config.language == "zh":
                    return "错误：查询格式无效。应为：节点,标签（例如：A,红）"
                else:
                    return "Error: Invalid query format. Should be: node,label (e.g., A,Red)"
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        nodes = ["A", "B", "C", "D", "E"]
        
        if correct in nodes:
            for n in nodes:
                if n != correct:
                    return n
        
        if isinstance(correct, str) and correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            if "否" in correct:
                return correct.replace("否", "是")
        else:
            lower_correct = correct.lower()
            if "yes" in lower_correct:
                return re.sub(r'(?i)yes', 'No', correct)
            if "no" in lower_correct:
                return re.sub(r'(?i)no', 'Yes', correct)
        
        return f"{correct}_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        nodes = ["A", "B", "C", "D", "E"]
        if self.config.language == "zh":
            labels = ["红", "蓝", "绿"]
        else:
            labels = ["Red", "Blue", "Green"]
            
        results = []
        for n in nodes:
            for l in labels:
                query_content = f"{n},{l}"
                if n in self.graph and l in self.graph[n]:
                    ans = self.graph[n][l]
                    results.append({
                        "query": f"<query_edge>{query_content}</query_edge>",
                        "answer": ans
                    })
        return results