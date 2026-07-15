from .base import Game
import random

class HiddenDistancePatternGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏距离模式"的推理游戏，规则如下：

游戏设定了一个固定的无向树 T，包含以下节点和边：
- 节点：A, B, C, D, E, F, G, H, I
- 边：A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

距离定义：对任意节点对 (X,Y)，d(X,Y) 为其在 T 上的最短路径长度（边数）。

系统内部已固定（但对你隐藏）以下两个要素：
1. 一个读数模式 f，从以下4种中选择其一：
   - 模式I：返回值 r 等于 d
   - 模式II：若 d 为奇数，r 等于 d 加 1；否则 r 等于 d
   - 模式III：若 d 为偶数，r 等于 d 加 1；否则 r 等于 d
   - 模式IV：r 等于 d 减 1 与 0 中的较大值

2. 一个隐藏目标对 Pk，从以下4对中选择其一：
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

你的任务是通过交互查询推断出：
1. 实际使用的读数模式（I/II/III/IV）
2. 隐藏目标对的编号（P1/P2/P3/P4）
3. 该目标对的真实距离值

你可以进行以下类型的查询：

1. 校准查询：提交任意节点对 (X,Y)，系统返回经过模式 f 处理后的读数 r。你需要至少完成2次校准查询。

2. 目标对读数请求：在完成至少2次校准查询后，可以请求获取隐藏目标对的读数 r_target。此类查询至多只能进行1次。

3. 最终提交：提交你推断的模式、目标对编号和真实距离。三项必须全部正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：

- 校准查询（例如查询节点 A 和 F 之间的距离）：
<query_calibrate>A,F</query_calibrate>

- 目标对读数请求（内容为空）：
<query_target></query_target>

- 最终提交（依次给出模式、目标对编号、真实距离）：
<answer>mode=I, pair=P1, distance=4</answer>

注意事项：
- 必须至少完成2次校准查询后才能请求目标对读数
- 目标对读数请求至多只能进行1次
- 节点名称必须从 A, B, C, D, E, F, G, H, I 中选择
- 违反规则或答案错误将导致游戏失败
"""

    game_rule_en = """\
Let's play a "Hidden Distance Pattern" deduction game. Here are the rules:

The game has a fixed undirected tree T with the following nodes and edges:
- Nodes: A, B, C, D, E, F, G, H, I
- Edges: A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

Distance definition: For any node pair (X,Y), d(X,Y) is the shortest path length (number of edges) in T.

The system has internally fixed (but hidden from you) two elements:
1. A reading pattern f, chosen from the following 4 types:
   - Mode I: return value r equals d
   - Mode II: if d is odd, r equals d plus 1; otherwise r equals d
   - Mode III: if d is even, r equals d plus 1; otherwise r equals d
   - Mode IV: r equals the maximum of d minus 1 and 0

2. A hidden target pair Pk, chosen from the following 4 pairs:
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

Your task is to infer through interactive queries:
1. The actual reading pattern (I/II/III/IV)
2. The hidden target pair number (P1/P2/P3/P4)
3. The true distance value of that target pair

You can perform the following types of queries:

1. Calibration Query: Submit any node pair (X,Y), the system returns a reading r processed by pattern f. You must complete at least 2 calibration queries.

2. Target Reading Request: After completing at least 2 calibration queries, you can request the reading r_target of the hidden target pair. This query can be performed at most once.

3. Final Submission: Submit your inferred pattern, target pair number, and true distance. All three must be correct to succeed.

Each query must contain only one tag, using the following XML format:

- Calibration Query (e.g., querying distance between nodes A and F):
<query_calibrate>A,F</query_calibrate>

- Target Reading Request (empty content):
<query_target></query_target>

- Final Submission (provide pattern, pair number, and true distance):
<answer>mode=I, pair=P1, distance=4</answer>

Notes:
- You must complete at least 2 calibration queries before requesting target reading
- Target reading request can be performed at most once
- Node names must be chosen from A, B, C, D, E, F, G, H, I
- Violating rules or incorrect answers will result in game failure
"""

    contextualized_rule_zh_1 = """\
欢迎使用“路网传感器标定系统”。
本系统管理的交通枢纽路网 T 包含以下枢纽节点和直达路段：
- 枢纽节点：A, B, C, D, E, F, G, H, I
- 直达路段：A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

站间距定义：任意枢纽对 (X,Y) 之间的 d(X,Y) 为两者在路网上的最短路段数。

系统内部已设定了两个隐藏参数，需要你通过探测来逆向推导：
1. 传感器计费模式 f，从以下4种中选择其一：
   - 模式I：计费读数 r 等于实际路段数 d
   - 模式II：若 d 为奇数，r 等于 d 加 1；否则 r 等于 d
   - 模式III：若 d 为偶数，r 等于 d 加 1；否则 r 等于 d
   - 模式IV：r 等于 d 减 1 与 0 中的较大值（即起步减免）

2. 一条隐藏的特殊物流线 Pk，从以下4组中选择其一：
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

你的任务是通过交互查询推断出：
1. 实际使用的计费模式（I/II/III/IV）
2. 特殊物流线的编号（P1/P2/P3/P4）
3. 该特殊物流线的真实路段数

你可以进行以下类型的查询：
1. 路线测试（校准查询）：提交任意枢纽对 (X,Y)，系统返回经过模式 f 处理后的计费读数 r。你需要至少完成2次路线测试。
2. 特殊线读数请求：在完成至少2次路线测试后，可以请求获取隐藏特殊物流线的计费读数 r_target。此类查询至多只能进行1次。
3. 最终提交：提交你推断的计费模式、物流线编号和真实路段数。三项必须全部正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：
- 路线测试（例如查询枢纽 A 和 F）：
<query_calibrate>A,F</query_calibrate>
- 特殊线读数请求（内容为空）：
<query_target></query_target>
- 最终提交（依次给出模式、物流线编号、真实路段数）：
<answer>mode=I, pair=P1, distance=4</answer>

注意事项：
- 必须至少完成2次路线测试后才能请求特殊线读数
- 特殊线读数请求至多只能进行1次
- 节点名称必须从 A, B, C, D, E, F, G, H, I 中选择
- 违反规则或答案错误将导致测试失败
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the "Road Network Sensor Calibration System".

The managed traffic hub network T contains the following hub nodes and direct routes:
- Hubs: A, B, C, D, E, F, G, H, I
- Direct routes: A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

Distance definition: For any hub pair (X,Y), d(X,Y) is the shortest number of route segments in T.

The system has internally fixed two hidden elements:
1. A billing pattern f, chosen from the following 4 types:
   - Mode I: reading r equals actual distance d
   - Mode II: if d is odd, r equals d plus 1; otherwise r equals d
   - Mode III: if d is even, r equals d plus 1; otherwise r equals d
   - Mode IV: r equals the maximum of d minus 1 and 0

2. A hidden special logistics line Pk, chosen from the following 4 pairs:
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

Your task is to infer through interactive queries:
1. The actual billing pattern (I/II/III/IV)
2. The special logistics line number (P1/P2/P3/P4)
3. The true route segment distance of that line

You can perform the following queries:
1. Route Test (Calibration Query): Submit any hub pair (X,Y), the system returns a reading r processed by pattern f. You must complete at least 2 route tests.
2. Special Line Reading Request: After completing at least 2 route tests, you can request the reading r_target of the hidden special line. This can be performed at most once.
3. Final Submission: Submit your inferred pattern, line number, and true distance. All three must be correct to succeed.

Each query must contain only one tag, using the following XML format:
- Route Test (e.g., test hubs A and F):
<query_calibrate>A,F</query_calibrate>
- Special Line Reading Request (empty content):
<query_target></query_target>
- Final Submission:
<answer>mode=I, pair=P1, distance=4</answer>

Notes:
- You must complete at least 2 route tests before requesting the special line reading.
- Special line reading request can be performed at most once.
- Hub names must be chosen from A, B, C, D, E, F, G, H, I.
- Violating rules or incorrect answers will result in failure.
"""

    contextualized_rule_zh_2 = """\
欢迎使用“神经传导通路分析系统”。
已知患者的局部神经传导网络 T 包含以下脑区节点和突触连接：
- 脑区节点：A, B, C, D, E, F, G, H, I
- 突触连接：A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

传导跳数定义：任意脑区对 (X,Y) 之间的 d(X,Y) 为其在网络中最短的突触连接数。

系统监测到存在未知的信号失真和潜在病灶，内部固化了以下要素：
1. 信号失真模式 f，从以下4种中选择其一：
   - 模式I：监测读数 r 等于真实跳数 d
   - 模式II：若 d 为奇数，r 等于 d 加 1；否则 r 等于 d
   - 模式III：若 d 为偶数，r 等于 d 加 1；否则 r 等于 d
   - 模式IV：r 等于 d 减 1 与 0 中的较大值（即存在阈值衰减）

2. 一对隐藏的关联病灶区 Pk，从以下4对中选择其一：
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

你的任务是通过交互刺激推断出：
1. 实际的信号失真模式（I/II/III/IV）
2. 关联病灶区的编号（P1/P2/P3/P4）
3. 该病灶区之间的真实传导跳数

你可以进行以下类型的查询：
1. 刺激传导测试（校准查询）：提交任意脑区对 (X,Y)，系统返回经过模式 f 处理后的监测读数 r。你需要至少完成2次传导测试。
2. 病灶读数请求：在完成至少2次传导测试后，可以获取隐藏病灶对的失真读数 r_target。此类查询至多只能进行1次。
3. 最终提交：提交你推断的失真模式、病灶编号和真实跳数。三项必须全部正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：
- 刺激传导测试（例如测试脑区 A 和 F）：
<query_calibrate>A,F</query_calibrate>
- 病灶读数请求（内容为空）：
<query_target></query_target>
- 最终提交（依次给出模式、病灶编号、真实跳数）：
<answer>mode=I, pair=P1, distance=4</answer>

注意事项：
- 必须至少完成2次传导测试后才能请求病灶读数
- 病灶读数请求至多只能进行1次
- 节点名称必须从 A, B, C, D, E, F, G, H, I 中选择
- 违反规则或答案错误将导致诊断失败
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the "Neural Conduction Pathway Analysis System".

The local neural network T contains the following brain region nodes and synaptic connections:
- Brain regions: A, B, C, D, E, F, G, H, I
- Synaptic connections: A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

Conduction hops definition: For any region pair (X,Y), d(X,Y) is the shortest number of synaptic connections in T.

The system has internally fixed two hidden elements:
1. A signal distortion pattern f, chosen from the following 4 types:
   - Mode I: monitored reading r equals actual hops d
   - Mode II: if d is odd, r equals d plus 1; otherwise r equals d
   - Mode III: if d is even, r equals d plus 1; otherwise r equals d
   - Mode IV: r equals the maximum of d minus 1 and 0

2. A hidden correlated lesion pair Pk, chosen from the following 4 pairs:
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

Your task is to infer through interactive stimulation:
1. The actual signal distortion pattern (I/II/III/IV)
2. The lesion pair number (P1/P2/P3/P4)
3. The true conduction hops of that lesion pair

You can perform the following queries:
1. Stimulation Test (Calibration Query): Submit any region pair (X,Y), the system returns a reading r processed by pattern f. You must complete at least 2 tests.
2. Lesion Reading Request: After completing at least 2 tests, you can request the reading r_target of the hidden lesion pair. This can be performed at most once.
3. Final Submission: Submit your inferred pattern, lesion number, and true hops. All three must be correct to succeed.

Each query must contain only one tag, using the following XML format:
- Stimulation Test (e.g., test regions A and F):
<query_calibrate>A,F</query_calibrate>
- Lesion Reading Request (empty content):
<query_target></query_target>
- Final Submission:
<answer>mode=I, pair=P1, distance=4</answer>

Notes:
- You must complete at least 2 tests before requesting the lesion reading.
- Lesion reading request can be performed at most once.
- Region names must be chosen from A, B, C, D, E, F, G, H, I.
- Violating rules or incorrect answers will result in failure.
"""

    contextualized_rule_zh_3 = """\
欢迎使用“知识图谱评估偏差分析系统”。
当前学科知识依赖树 T 包含以下知识模块和先修关系：
- 知识模块：A, B, C, D, E, F, G, H, I
- 先修关系：A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

学习跨度定义：任意知识模块对 (X,Y) 之间的 d(X,Y) 为其在图谱上的最短依赖路径长度。

测试系统存在固有的评估偏差，并设置了核心考查路径：
1. 计分评估模式 f，从以下4种中选择其一：
   - 模式I：评估层级 r 等于实际跨度 d
   - 模式II：若 d 为奇数，r 等于 d 加 1；否则 r 等于 d
   - 模式III：若 d 为偶数，r 等于 d 加 1；否则 r 等于 d
   - 模式IV：r 等于 d 减 1 与 0 中的较大值（即基础免测）

2. 一条隐藏的核心考查路径 Pk，从以下4对中选择其一：
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

你的任务是通过交互查询推断出：
1. 实际的计分评估模式（I/II/III/IV）
2. 核心考查路径的编号（P1/P2/P3/P4）
3. 该考查路径的真实学习跨度

你可以进行以下类型的查询：
1. 评估路径校准（校准查询）：提交任意模块对 (X,Y)，系统返回经过模式 f 处理后的评估层级 r。你需要至少完成2次校准。
2. 核心考查请求：在完成至少2次评估路径校准后，可以请求获取核心考查路径的评估读数 r_target。此类查询至多只能进行1次。
3. 最终提交：提交你推断的评估模式、考查路径编号和真实跨度。三项必须全部正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：
- 评估路径校准（例如查询模块 A 和 F）：
<query_calibrate>A,F</query_calibrate>
- 核心考查请求（内容为空）：
<query_target></query_target>
- 最终提交（依次给出模式、考查路径编号、真实跨度）：
<answer>mode=I, pair=P1, distance=4</answer>

注意事项：
- 必须至少完成2次评估路径校准后才能请求核心考查读数
- 核心考查请求至多只能进行1次
- 节点名称必须从 A, B, C, D, E, F, G, H, I 中选择
- 违反规则或答案错误将导致分析失败
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the "Knowledge Graph Assessment Bias Analysis System".

The subject dependency tree T contains the following knowledge modules and prerequisite links:
- Modules: A, B, C, D, E, F, G, H, I
- Prerequisite links: A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

Learning span definition: For any module pair (X,Y), d(X,Y) is the shortest dependency path length in T.

The system has internally fixed two hidden elements:
1. A scoring assessment pattern f, chosen from the following 4 types:
   - Mode I: assessment level r equals actual span d
   - Mode II: if d is odd, r equals d plus 1; otherwise r equals d
   - Mode III: if d is even, r equals d plus 1; otherwise r equals d
   - Mode IV: r equals the maximum of d minus 1 and 0

2. A hidden core examination path Pk, chosen from the following 4 pairs:
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

Your task is to infer through interactive queries:
1. The actual assessment pattern (I/II/III/IV)
2. The core examination path number (P1/P2/P3/P4)
3. The true learning span of that core path

You can perform the following queries:
1. Assessment Path Calibration (Calibration Query): Submit any module pair (X,Y), the system returns a reading r processed by pattern f. You must complete at least 2 calibrations.
2. Core Path Request: After completing at least 2 calibrations, you can request the reading r_target of the hidden core path. This can be performed at most once.
3. Final Submission: Submit your inferred pattern, core path number, and true span. All three must be correct to succeed.

Each query must contain only one tag, using the following XML format:
- Assessment Path Calibration (e.g., query modules A and F):
<query_calibrate>A,F</query_calibrate>
- Core Path Request (empty content):
<query_target></query_target>
- Final Submission:
<answer>mode=I, pair=P1, distance=4</answer>

Notes:
- You must complete at least 2 calibrations before requesting the core path reading.
- Core path request can be performed at most once.
- Module names must be chosen from A, B, C, D, E, F, G, H, I.
- Violating rules or incorrect answers will result in failure.
"""

    contextualized_rule_zh_4 = """\
欢迎进入“工业管网仪表校验与故障排查系统”。
厂区控制网 T 包含以下工作站节点和通信总线：
- 工作站节点：A, B, C, D, E, F, G, H, I
- 通信总线：A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

总线物理段数定义：任意工作站对 (X,Y) 之间的 d(X,Y) 为其在控制网上的最短总线段数。

系统中仪表的读数存在系统补偿偏差，并存在一对隐藏的故障隐患链路：
1. 仪表读数补偿模式 f，从以下4种中选择其一：
   - 模式I：显示读数 r 等于实际段数 d
   - 模式II：若 d 为奇数，r 等于 d 加 1；否则 r 等于 d
   - 模式III：若 d 为偶数，r 等于 d 加 1；否则 r 等于 d
   - 模式IV：r 等于 d 减 1 与 0 中的较大值（即消除串扰本底）

2. 一对隐藏的故障隐患链路 Pk，从以下4对中选择其一：
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

你的任务是通过诊断交互推断出：
1. 实际的仪表补偿模式（I/II/III/IV）
2. 故障隐患链路的编号（P1/P2/P3/P4）
3. 该隐患链路的真实物理段数

你可以进行以下类型的查询：
1. 仪表校准检测（校准查询）：提交任意工作站对 (X,Y)，系统返回经过模式 f 处理后的仪表显示读数 r。你需要至少完成2次检测。
2. 故障链路读数请求：在完成至少2次校准检测后，可以请求获取故障链路的仪表读数 r_target。此类查询至多只能进行1次。
3. 最终提交：提交你推断的补偿模式、隐患链路编号和真实段数。三项必须全部正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：
- 仪表校准检测（例如检测工作站 A 和 F）：
<query_calibrate>A,F</query_calibrate>
- 故障链路读数请求（内容为空）：
<query_target></query_target>
- 最终提交（依次给出模式、链路编号、真实段数）：
<answer>mode=I, pair=P1, distance=4</answer>

注意事项：
- 必须至少完成2次校准检测后才能请求故障链路读数
- 故障链路读数请求至多只能进行1次
- 节点名称必须从 A, B, C, D, E, F, G, H, I 中选择
- 违反规则或答案错误将导致排查失败
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the "Industrial Pipeline Instrument Calibration and Troubleshooting System".

The control network T contains the following workstations and communication buses:
- Workstations: A, B, C, D, E, F, G, H, I
- Communication buses: A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

Physical segments definition: For any workstation pair (X,Y), d(X,Y) is the shortest number of physical segments in T.

The system has internally fixed two hidden elements:
1. An instrument compensation pattern f, chosen from the following 4 types:
   - Mode I: display reading r equals actual segments d
   - Mode II: if d is odd, r equals d plus 1; otherwise r equals d
   - Mode III: if d is even, r equals d plus 1; otherwise r equals d
   - Mode IV: r equals the maximum of d minus 1 and 0

2. A hidden fault risk link Pk, chosen from the following 4 pairs:
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

Your task is to infer through diagnostic queries:
1. The actual compensation pattern (I/II/III/IV)
2. The fault link number (P1/P2/P3/P4)
3. The true physical segments of that fault link

You can perform the following queries:
1. Instrument Calibration Test (Calibration Query): Submit any workstation pair (X,Y), the system returns a reading r processed by pattern f. You must complete at least 2 tests.
2. Fault Link Reading Request: After completing at least 2 tests, you can request the reading r_target of the hidden fault link. This can be performed at most once.
3. Final Submission: Submit your inferred pattern, fault link number, and true segments. All three must be correct to succeed.

Each query must contain only one tag, using the following XML format:
- Instrument Calibration Test (e.g., test workstations A and F):
<query_calibrate>A,F</query_calibrate>
- Fault Link Reading Request (empty content):
<query_target></query_target>
- Final Submission:
<answer>mode=I, pair=P1, distance=4</answer>

Notes:
- You must complete at least 2 tests before requesting the fault link reading.
- Fault link reading request can be performed at most once.
- Workstation names must be chosen from A, B, C, D, E, F, G, H, I.
- Violating rules or incorrect answers will result in failure.
"""

    contextualized_rule_zh_5 = """\
欢迎启动“涉案资金网络穿透式审计系统”。
已查明的资金流转网络 T 包含以下涉案主体账户和流转关系：
- 主体账户：A, B, C, D, E, F, G, H, I
- 资金流转链：A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

流转层级定义：任意账户对 (X,Y) 之间的 d(X,Y) 为其在网络上的最短流转环节数。

犯罪集团设置了账目混淆策略，并掩盖了一条核心利益输送链：
1. 审计干扰模式 f，从以下4种中选择其一：
   - 模式I：账面层级 r 等于实际层级 d
   - 模式II：若 d 为奇数，r 等于 d 加 1；否则 r 等于 d（虚增偶数结构）
   - 模式III：若 d 为偶数，r 等于 d 加 1；否则 r 等于 d（虚增奇数结构）
   - 模式IV：r 等于 d 减 1 与 0 中的较大值（即掩盖直接流水）

2. 一条隐藏的核心输送链 Pk，从以下4对中选择其一：
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

你的任务是通过追踪查询推断出：
1. 实际的审计干扰模式（I/II/III/IV）
2. 核心输送链的编号（P1/P2/P3/P4）
3. 该输送链的真实流转层级数

你可以进行以下类型的操作：
1. 追踪审计查询（校准查询）：提交任意账户对 (X,Y)，系统返回经过模式 f 处理后的账面层级 r。你需要至少完成2次审计。
2. 核心输送链取证：在完成至少2次追踪审计后，可以请求获取核心输送链的账面层级 r_target。此类请求至多只能进行1次。
3. 最终提交：提交你推断的干扰模式、输送链编号和真实流转层级。三项必须全部正确才算成功。

每次查询只能包含一个标签，使用以下 XML 格式：
- 追踪审计查询（例如查询账户 A 和 F）：
<query_calibrate>A,F</query_calibrate>
- 核心输送链取证（内容为空）：
<query_target></query_target>
- 最终提交（依次给出模式、输送链编号、真实层级）：
<answer>mode=I, pair=P1, distance=4</answer>

注意事项：
- 必须至少完成2次追踪审计后才能进行核心链取证
- 核心链取证请求至多只能进行1次
- 节点名称必须从 A, B, C, D, E, F, G, H, I 中选择
- 违反规则或答案错误将导致取证失败
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the "Forensic Audit of Illicit Fund Networks System".

The fund transfer network T contains the following entities and transfer links:
- Entities: A, B, C, D, E, F, G, H, I
- Transfer links: A-B, B-C, B-D, D-E, E-F, C-G, G-H, H-I

Transfer steps definition: For any entity pair (X,Y), d(X,Y) is the shortest number of transfer steps in T.

The system has internally fixed two hidden elements:
1. An audit interference pattern f, chosen from the following 4 types:
   - Mode I: ledger steps r equals actual steps d
   - Mode II: if d is odd, r equals d plus 1; otherwise r equals d
   - Mode III: if d is even, r equals d plus 1; otherwise r equals d
   - Mode IV: r equals the maximum of d minus 1 and 0

2. A hidden core illicit transfer chain Pk, chosen from the following 4 pairs:
   - P1: (A, F)
   - P2: (C, H)
   - P3: (D, I)
   - P4: (E, G)

Your task is to infer through tracing queries:
1. The actual audit interference pattern (I/II/III/IV)
2. The core transfer chain number (P1/P2/P3/P4)
3. The true transfer steps of that core chain

You can perform the following queries:
1. Tracing Audit Query (Calibration Query): Submit any entity pair (X,Y), the system returns a reading r processed by pattern f. You must complete at least 2 audits.
2. Core Transfer Chain Evidence Request: After completing at least 2 audits, you can request the reading r_target of the hidden core chain. This can be performed at most once.
3. Final Submission: Submit your inferred pattern, chain number, and true steps. All three must be correct to succeed.

Each query must contain only one tag, using the following XML format:
- Tracing Audit Query (e.g., query entities A and F):
<query_calibrate>A,F</query_calibrate>
- Core Transfer Chain Evidence Request (empty content):
<query_target></query_target>
- Final Submission:
<answer>mode=I, pair=P1, distance=4</answer>

Notes:
- You must complete at least 2 audits before requesting the core chain evidence.
- Core chain evidence request can be performed at most once.
- Entity names must be chosen from A, B, C, D, E, F, G, H, I.
- Violating rules or incorrect answers will result in failure.
"""

    tags = ["answer", "query_calibrate", "query_target"]
    
    reasoning_type = "溯因推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        1: {
            "mode": "I",
            "target_pair": "P2",
        },
        2: {
            "mode": "II",
            "target_pair": "P1",
        },
        3: {
            "mode": "III",
            "target_pair": "P4",
        },
        4: {
            "mode": "IV",
            "target_pair": "P2",
        },
        5: {
            "mode": "IV",
            "target_pair": "P3",
        },
    }

    def __init__(self, config):
        self.tree_edges = [
            ("A", "B"), ("B", "C"), ("B", "D"), ("D", "E"), 
            ("E", "F"), ("C", "G"), ("G", "H"), ("H", "I")
        ]
        
        self.target_pairs_info = {
            "P1": (("A", "F"), 4),
            "P2": (("C", "H"), 2),
            "P3": (("D", "I"), 5),
            "P4": (("E", "G"), 4),
        }
        
        super().__init__(config)

    def _initialize_game(self):
        diff = self.config.difficulty
        
        if isinstance(diff, str):
            diff = int(diff)
        
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[diff]
        
        self.mode = cfg["mode"]
        self.target_pair_name = cfg["target_pair"]
        self.target_pair_nodes, self.target_true_distance = self.target_pairs_info[self.target_pair_name]
        
        self._build_graph()
        
        self.calibration_count = 0
        self.target_query_count = 0
        
        self._game_info = {}

    def _build_graph(self):
        from collections import defaultdict, deque
        
        self.graph = defaultdict(list)
        for u, v in self.tree_edges:
            self.graph[u].append(v)
            self.graph[v].append(u)
    
    def _compute_distance(self, node1, node2):
        from collections import deque
        
        if node1 == node2:
            return 0
        
        visited = {node1}
        queue = deque([(node1, 0)])
        
        while queue:
            current, dist = queue.popleft()
            for neighbor in self.graph[current]:
                if neighbor == node2:
                    return dist + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))
        
        return -1
    
    def _apply_mode(self, true_distance):
        d = true_distance
        
        if self.mode == "I":
            return d
        elif self.mode == "II":
            return d + 1 if d % 2 == 1 else d
        elif self.mode == "III":
            return d + 1 if d % 2 == 0 else d
        elif self.mode == "IV":
            return max(0, d - 1)
        else:
            raise ValueError(f"Unknown mode: {self.mode}")

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        kv_pairs = [x.strip() for x in raw_ans.split(",") if "=" in x]
        ans_dict = {}
        for kv in kv_pairs:
            k, v = kv.split("=", 1)
            ans_dict[k.strip()] = v.strip()
        
        if "mode" not in ans_dict or "pair" not in ans_dict or "distance" not in ans_dict:
            return False
        
        if ans_dict["mode"] != self.mode:
            return False
        
        if ans_dict["pair"] != self.target_pair_name:
            return False
        
        try:
            submitted_distance = int(ans_dict["distance"])
        except ValueError:
            return False
        
        return submitted_distance == self.target_true_distance

    def _cf_make_wrong(self, correct: str) -> str:
        try:
            correct_val = int(correct)
            wrong_val = correct_val + 1
            return str(wrong_val)
        except (ValueError, TypeError):
            return correct + " [WRONG]"

    def _cf_core_produce(self, parsed_info):
        if "query_calibrate" in parsed_info:
            raw = parsed_info["query_calibrate"].strip()
            parts = [x.strip() for x in raw.split(",")]
            
            if len(parts) != 2:
                raise ValueError(
                    "Calibration query must contain exactly two nodes separated by a comma."
                    if self.config.language == "en" else
                    "校准查询必须包含恰好两个节点，用逗号分隔。"
                )
            
            node1, node2 = parts
            
            valid_nodes = {"A", "B", "C", "D", "E", "F", "G", "H", "I"}
            if node1 not in valid_nodes or node2 not in valid_nodes:
                raise ValueError(
                    "Invalid node name. Must be chosen from A, B, C, D, E, F, G, H, I."
                    if self.config.language == "en" else
                    "节点名称无效。必须从 A, B, C, D, E, F, G, H, I 中选择。"
                )
            
            true_dist = self._compute_distance(node1, node2)
            
            reading = self._apply_mode(true_dist)
            
            self.calibration_count += 1
            
            return str(reading)
        
        elif "query_target" in parsed_info:
            if self.calibration_count < 2:
                raise ValueError(
                    f"You must complete at least 2 calibration queries before requesting target reading. Current count: {self.calibration_count}."
                    if self.config.language == "en" else
                    f"必须至少完成2次校准查询后才能请求目标对读数。当前已完成 {self.calibration_count} 次。"
                )
            
            if self.target_query_count >= 1:
                raise ValueError(
                    "Target reading request can be performed at most once."
                    if self.config.language == "en" else
                    "目标对读数请求至多只能进行1次。"
                )
            
            self.target_query_count += 1
            
            target_reading = self._apply_mode(self.target_true_distance)
            
            return str(target_reading)
        
        else:
            raise ValueError(
                "No valid query tag found."
                if self.config.language == "en" else
                "未找到有效的查询标签。"
            )

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        nodes = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        
        for i, n1 in enumerate(nodes):
            for n2 in nodes[i+1:]:
                true_dist = self._compute_distance(n1, n2)
                reading = self._apply_mode(true_dist)
                
                queries.append({
                    "query": f"<query_calibrate>{n1},{n2}</query_calibrate>",
                    "answer": str(reading)
                })
        
        target_reading = self._apply_mode(self.target_true_distance)
        queries.append({
            "query": "<query_target></query_target>",
            "answer": str(target_reading)
        })

        return queries