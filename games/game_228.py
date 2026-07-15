import random
from .base import Game

class HiddenMappingTreeSearchGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏映射树搜索"的推理游戏，规则如下：

游戏设定了一棵树结构，包含 {n} 个节点（编号从 1 到 {n}），根节点为 {root}。树的结构已公开：{tree_structure}

我已秘密选择了一个目标节点 T。同时，我为每个节点分配了一种颜色（共有 {num_colors} 种颜色）。

此外，我设定了一个隐藏的反馈映射规则：当你探测某个节点时，我会根据你与目标节点的"接近程度变化"给出三种符号之一：{symbol1}、{symbol2}、{symbol3}。这三个符号分别对应"更远"、"持平"和"更近"三种情况，但具体对应关系是隐藏的，需要你自行推断。

你的目标是通过提问找到目标节点 T，或给出从根节点到 T 的完整路径。

每次只能提出一个问题，使用以下格式：

1. 探测查询：探测某个节点（例如探测节点 5）
<probe>5</probe>

探测后，你的当前位置会更新为该节点，我会返回一个符号（{symbol1}、{symbol2} 或 {symbol3}），表示你与目标的接近程度变化。

2. 目标查询：询问某个节点是否为目标（例如询问节点 3）
<is_target>3</is_target>

返回"是"或"否"，不改变当前位置。

3. 路径验证：提交一条从根到某节点的完整路径（例如路径 1,2,5）
<check_path>1,2,5</check_path>

返回"是"或"否"，表示该路径是否恰好为从根到目标节点 T 的完整路径。

当你确定目标节点后，提交答案：
<answer>节点编号</answer>

例如：
<answer>7</answer>

或者提交完整路径：
<answer>1,3,7</answer>

答案正确即获胜，错误则失败。请尽可能少地使用提问次数。
"""

    game_rule_en = """\
Let's play a "Hidden Mapping Tree Search" deduction game. Here are the rules:

The game involves a tree structure with {n} nodes (numbered 1 to {n}), with root node {root}. The tree structure is public: {tree_structure}

I have secretly chosen a target node T. Additionally, I have assigned a color to each node (there are {num_colors} distinct colors).

Furthermore, I have set up a hidden feedback mapping: when you probe a node, I will respond with one of three symbols: {symbol1}, {symbol2}, {symbol3}. These three symbols correspond to "farther away", "no change", and "closer" respectively, but the exact mapping is hidden and you must infer it yourself.

Your goal is to find the target node T through queries, or provide the complete path from the root to T.

You may ask one question at a time using the following formats:

1. Probe Query: Probe a specific node (e.g., probe node 5)
<probe>5</probe>

After probing, your current position updates to that node, and I will return a symbol ({symbol1}, {symbol2}, or {symbol3}) indicating how your proximity to the target has changed.

2. Target Query: Ask if a specific node is the target (e.g., ask about node 3)
<is_target>3</is_target>

Returns "Yes" or "No", current position unchanged.

3. Path Verification: Submit a complete path from root to a node (e.g., path 1,2,5)
<check_path>1,2,5</check_path>

Returns "Yes" or "No", indicating whether this path is exactly the complete path from root to target node T.

When you have determined the target node, submit your answer:
<answer>node_id</answer>

For example:
<answer>7</answer>

Or submit the complete path:
<answer>1,3,7</answer>

Correct answer wins, incorrect fails. Try to minimize the number of queries.
"""

    contextualized_rule_zh_1 = """\
我们来执行一次"城市路网隐蔽事故点排查"任务，规则如下：

城市交通监控系统映射出了一棵树状的道路网络拓扑，包含 {n} 个路口节点（编号从 1 到 {n}），调度中心（根节点）为 {root}。路网的公开拓扑结构如下：{tree_structure}

系统侦测到一个隐藏的交通事故拥堵点 T。同时，我为每个路口分配了其所属的片区属性（共有 {num_colors} 种片区标识）。

此外，由于现场信号干扰，探查只能返回一种相对反馈规则：当你派遣无人机探测某个节点时，系统会根据该节点与实际事故点 T 的"拓扑距离变化"给出三种特征信号之一：{symbol1}、{symbol2}、{symbol3}。这三个信号分别对应"偏离目标"（更远）、"距离持平"和"逼近目标"（更近）三种情况，但具体的对应关系因信号加密是隐藏的，需要你自行推断。

你的目标是通过调度指令找到事故拥堵点 T，或给出从调度中心到 T 的完整救援路线。

每次只能下达一个指令，使用以下格式：

1. 探测指令：派遣无人机探测某个路口（例如探测节点 5）
<probe>5</probe>

探测后，你的当前监测重心会更新为该节点，系统会返回一个特征信号（{symbol1}、{symbol2} 或 {symbol3}），表示你与事故点的拓扑距离变化。

2. 定点核实：要求交警直接核实某节点是否为事故点（例如核实节点 3）
<is_target>3</is_target>

返回"是"或"否"，不改变当前监测重心。

3. 路线验证：提交一条从调度中心到某节点的完整救援路线（例如路径 1,2,5）
<check_path>1,2,5</check_path>

返回"是"或"否"，表示该路线是否恰好为从调度中心直达事故点 T 的完整路线。

当你确定事故拥堵点后，提交结论：
<answer>节点编号</answer>

例如：
<answer>7</answer>

或者提交完整救援路线：
<answer>1,3,7</answer>

定位正确即成功完成调度，错误则贻误战机导致失败。请尽可能少地使用指令次数以节约救援时间。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Let's conduct a "Hidden Traffic Incident Detection" operation in an urban road network. Here are the rules:

The urban traffic monitoring system has mapped out a tree-like road network topology with {n} intersection nodes (numbered 1 to {n}), with the dispatch center (root node) at {root}. The public network topology is: {tree_structure}

The system has detected a hidden traffic incident/congestion point T. Additionally, each intersection is assigned to a specific district zone (there are {num_colors} distinct zone categories).

Furthermore, due to field signal interference, reconnaissance only returns a relative feedback rule: when you dispatch a drone to probe a node, the system will respond with one of three characteristic signals based on how your "topological distance" to the incident point T changes: {symbol1}, {symbol2}, {symbol3}. These three signals correspond to "diverging" (farther away), "maintaining distance" (no change), and "approaching" (closer), but the exact mapping is encrypted and you must infer it yourself.

Your goal is to locate the incident point T through dispatch commands, or provide the complete rescue route from the dispatch center to T.

You may issue one command at a time using the following formats:

1. Probe Command: Dispatch a drone to probe a specific intersection (e.g., probe node 5)
<probe>5</probe>

After probing, your current monitoring focus updates to that node, and the system will return a characteristic signal ({symbol1}, {symbol2}, or {symbol3}) indicating how your proximity to the incident has changed.

2. Target Verification: Request traffic police to verify if a node is the incident point (e.g., verify node 3)
<is_target>3</is_target>

Returns "Yes" or "No", current monitoring focus unchanged.

3. Route Validation: Submit a complete rescue route from the dispatch center to a node (e.g., route 1,2,5)
<check_path>1,2,5</check_path>

Returns "Yes" or "No", indicating whether this route is exactly the complete path from the dispatch center to the incident point T.

When you have determined the incident point, submit your conclusion:
<answer>node_id</answer>

For example:
<answer>7</answer>

Or submit the complete rescue route:
<answer>1,3,7</answer>

Correct localization means a successful dispatch; failure leads to delayed rescue operations. Try to minimize the number of commands to save critical rescue time.
"""

    contextualized_rule_zh_2 = """\
我们来执行一次"隐蔽病灶靶向定位"医疗诊断任务，规则如下：

医学影像系统重建了一棵神经/血管拓扑树，包含 {n} 个组织节点（编号从 1 到 {n}），主干入口（根节点）为 {root}。拓扑结构已公开：{tree_structure}

系统提示存在一个隐藏的微小病灶节点 T。同时，我为每个节点标记了其组织液的生化显色属性（共有 {num_colors} 种显色类型）。

此外，探查设备受限于组织渗透率，采用了一种隐藏的反馈映射规则：当你通过导管向某个节点注射示踪剂探测时，监测仪会根据你与病灶节点的"生理距离变化"给出三种波形符号之一：{symbol1}、{symbol2}、{symbol3}。这三种波形分别对应"偏离病灶"（更远）、"距离持平"和"逼近病灶"（更近）三种情况，但具体对应关系需要你根据临床反馈自行推断。

你的目标是通过探测指令找到病灶节点 T，或规划出从主干入口到 T 的完整微创穿刺路径。

每次只能执行一项操作，使用以下格式：

1. 示踪探测：在特定节点注射示踪剂探测（例如探测节点 5）
<probe>5</probe>

探测后，导管的前端位置会更新为该节点，监测仪会返回一个波形符号（{symbol1}、{symbol2} 或 {symbol3}），表示你与病灶的生理距离变化。

2. 靶向活检：对某个节点进行活检确认是否为病灶（例如活检节点 3）
<is_target>3</is_target>

返回"是"或"否"，不改变当前导管前端位置。

3. 路径验证：模拟一条从主干到某节点的完整穿刺路径（例如路径 1,2,5）
<check_path>1,2,5</check_path>

返回"是"或"否"，表示该路径是否恰好为从主干入口到病灶节点 T 的完美穿刺路径。

当你确定病灶节点后，提交诊断：
<answer>节点编号</answer>

例如：
<answer>7</answer>

或者提交完整穿刺路径：
<answer>1,3,7</answer>

定位准确即可成功实施手术，错误将导致手术失败。请尽可能减少探测次数以降低患者创伤风险。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Let's conduct a "Hidden Lesion Targeted Localization" diagnostic task. Here are the rules:

The medical imaging system has reconstructed a neural/vascular topology tree containing {n} tissue nodes (numbered 1 to {n}), with the main trunk entry (root node) at {root}. The topological structure is public: {tree_structure}

The system indicates the presence of a hidden micro-lesion node T. Additionally, each node is categorized by its tissue fluid's biochemical staining property (there are {num_colors} distinct staining types).

Furthermore, due to tissue permeability limits, the probing equipment uses a hidden feedback mapping: when you inject a tracer via a catheter to probe a node, the monitor will display one of three waveform symbols based on how your "physiological distance" to the lesion node changes: {symbol1}, {symbol2}, {symbol3}. These three waveforms correspond to "deviating from the lesion" (farther away), "maintaining distance" (no change), and "approaching the lesion" (closer), but the exact clinical mapping is hidden and you must infer it yourself.

Your goal is to locate the lesion node T through probing commands, or map out the complete minimally invasive puncture path from the main trunk entry to T.

You may perform one operation at a time using the following formats:

1. Tracer Probe: Inject a tracer at a specific node (e.g., probe node 5)
<probe>5</probe>

After probing, the catheter tip position updates to that node, and the monitor returns a waveform symbol ({symbol1}, {symbol2}, or {symbol3}) indicating how your physiological distance to the lesion has changed.

2. Targeted Biopsy: Perform a biopsy on a node to verify if it is the lesion (e.g., biopsy node 3)
<is_target>3</is_target>

Returns "Yes" or "No", current catheter position unchanged.

3. Path Validation: Simulate a complete puncture path from the main trunk to a node (e.g., path 1,2,5)
<check_path>1,2,5</check_path>

Returns "Yes" or "No", indicating whether this path is exactly the perfect puncture route from the root entry to the lesion node T.

When you have determined the lesion node, submit your diagnosis:
<answer>node_id</answer>

For example:
<answer>7</answer>

Or submit the complete puncture path:
<answer>1,3,7</answer>

Accurate localization leads to a successful surgery; an incorrect diagnosis results in failure. Please minimize probing to reduce trauma risk to the patient.
"""

    contextualized_rule_zh_3 = """\
我们来进行一次"核心认知盲区追溯"的教学评估任务，规则如下：

教育大模型构建了一棵学科知识点先决条件树，包含 {n} 个知识节点（编号从 1 到 {n}），基础概念（根节点）为 {root}。知识图谱结构已公开：{tree_structure}

系统评估出学生存在一个隐藏的根本认知盲区节点 T。同时，我为每个知识点标注了其认知难度等级的颜色标识（共有 {num_colors} 种颜色）。

此外，测评系统设定了一种隐性反馈映射机制：当你对学生进行某知识点的专项测试时，系统会根据该测试点与真实盲区的"认知关联度变化"给出三种评估评级之一：{symbol1}、{symbol2}、{symbol3}。这三个评级分别对应"偏离盲区"（更远）、"关联度持平"和"逼近盲区"（更近）三种情况，但具体的评级映射关系是隐藏的，需要你作为教师自行推断。

你的目标是通过测试指令精准定位到该根本认知盲区 T，或给出从基础概念到 T 的完整认知推演路径。

每次只能下达一个指令，使用以下格式：

1. 专项测试：对某个知识点进行测验（例如测试节点 5）
<probe>5</probe>

测试后，你的当前诊断重心会更新为该节点，系统会返回一个评估评级（{symbol1}、{symbol2} 或 {symbol3}），表示你与认知盲区的关联度变化。

2. 盲区确认：直接询问诊断系统某节点是否即为最终盲区（例如确认节点 3）
<is_target>3</is_target>

返回"是"或"否"，不改变当前诊断重心。

3. 推演验证：提交一条从基础概念到某节点的完整认知推演路径（例如路径 1,2,5）
<check_path>1,2,5</check_path>

返回"是"或"否"，表示该路径是否恰好为从基础概念到盲区 T 的完整学习障碍链条。

当你确定认知盲区后，提交诊断结果：
<answer>节点编号</answer>

例如：
<answer>7</answer>

或者提交完整认知推演路径：
<answer>1,3,7</answer>

定位正确即可对症下药提升成绩，错误则辅导失败。请尽可能减少测试次数以免增加学生的考试负担。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's conduct a "Core Cognitive Blind Spot Tracing" pedagogical assessment task. Here are the rules:

The educational AI has constructed a subject prerequisite knowledge tree containing {n} knowledge nodes (numbered 1 to {n}), with the foundational concept (root node) at {root}. The knowledge graph structure is public: {tree_structure}

The system has evaluated that the student has a hidden fundamental cognitive blind spot node T. Additionally, each knowledge point is tagged with a color representing its cognitive difficulty level (there are {num_colors} distinct colors).

Furthermore, the assessment system features an implicit feedback mapping mechanism: when you administer a targeted test on a specific knowledge node, the system returns one of three evaluation ratings based on how the "cognitive relevance" to the true blind spot changes: {symbol1}, {symbol2}, {symbol3}. These three ratings correspond to "diverging from the blind spot" (farther away), "maintaining relevance" (no change), and "approaching the blind spot" (closer). The exact mapping is hidden, and you, as the educator, must deduce it.

Your goal is to pinpoint the fundamental cognitive blind spot T through assessment commands, or provide the complete cognitive deduction path from the foundational concept to T.

You may issue one command at a time using the following formats:

1. Targeted Test: Test a specific knowledge node (e.g., test node 5)
<probe>5</probe>

After testing, your current diagnostic focus updates to that node, and the system returns an evaluation rating ({symbol1}, {symbol2}, or {symbol3}) indicating the change in relevance to the blind spot.

2. Blind Spot Confirmation: Directly ask the diagnostic system if a node is the final blind spot (e.g., confirm node 3)
<is_target>3</is_target>

Returns "Yes" or "No", current diagnostic focus unchanged.

3. Deduction Validation: Submit a complete cognitive deduction path from the foundational concept to a node (e.g., path 1,2,5)
<check_path>1,2,5</check_path>

Returns "Yes" or "No", indicating whether this path perfectly matches the learning obstacle chain from the foundational concept to blind spot T.

When you have determined the cognitive blind spot, submit your diagnosis:
<answer>node_id</answer>

For example:
<answer>7</answer>

Or submit the complete cognitive deduction path:
<answer>1,3,7</answer>

An accurate diagnosis enables targeted tutoring; a wrong one leads to an ineffective study plan. Please minimize the number of tests to avoid overburdening the student.
"""

    contextualized_rule_zh_4 = """\
我们来执行一次"工业管网隐蔽故障排查"任务，规则如下：

工厂的SCADA系统映射出了一棵流体管网系统树，包含 {n} 个阀门节点（编号从 1 到 {n}），总阀门（根节点）为 {root}。管线的公开拓扑结构如下：{tree_structure}

传感器阵列侦测到管网深处存在一个隐藏的泄漏故障点 T。同时，我为每个节点标记了其管线材质的色标（共有 {num_colors} 种色标分类）。

此外，探伤仪采用了一种基于声学衰减的隐藏反馈映射规则：当你使用传感仪探测某个节点时，仪器会根据该节点与实际故障点 T 的"管线距离变化"给出三种特征代码之一：{symbol1}、{symbol2}、{symbol3}。这三个代码分别对应"偏离故障源"（更远）、"距离持平"和"逼近故障源"（更近）三种物理情况，但具体代码的对应关系未在手册中注明，需要你自行推断。

你的目标是通过探测指令找到泄漏故障点 T，或给出从总阀门到 T 的完整管线排查链路。

每次只能下达一项检修指令，使用以下格式：

1. 传感探测：在特定阀门节点使用探伤仪探测（例如探测节点 5）
<probe>5</probe>

探测后，检修队伍的当前位置会更新为该节点，仪器会返回一个特征代码（{symbol1}、{symbol2} 或 {symbol3}），表示队伍与故障源的距离变化。

2. 拆卸核查：要求工人直接拆卸核查某节点是否为泄漏点（例如核查节点 3）
<is_target>3</is_target>

返回"是"或"否"，不改变检修队伍的当前位置。

3. 链路验证：提交一条从总阀门到某节点的完整排查链路（例如链路 1,2,5）
<check_path>1,2,5</check_path>

返回"是"或"否"，表示该链路是否恰好为从总阀门到故障点 T 的正确追溯路线。

当你确定故障节点后，提交报告：
<answer>节点编号</answer>

例如：
<answer>7</answer>

或者提交完整管线排查链路：
<answer>1,3,7</answer>

排查正确即可迅速修复管网，错误则导致停工损失加剧。请尽可能减少探测步骤以降低排查成本。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industry Scenario]
Let's conduct a "Hidden Industrial Pipeline Fault Troubleshooting" task. Here are the rules:

The factory's SCADA system has mapped out a fluid pipeline network tree containing {n} valve nodes (numbered 1 to {n}), with the main valve (root node) at {root}. The public topology of the pipeline is: {tree_structure}

The sensor array has detected a hidden leakage fault point T deep within the network. Additionally, each node is tagged with a color code representing its pipeline material (there are {num_colors} distinct color codes).

Furthermore, the flaw detector utilizes a hidden feedback mapping based on acoustic attenuation: when you probe a node using the sensor, the instrument displays one of three characteristic codes based on how the "pipeline distance" to the actual fault point T changes: {symbol1}, {symbol2}, {symbol3}. These three codes correspond to "deviating from the fault source" (farther away), "maintaining distance" (no change), and "approaching the fault source" (closer). However, the specific code mapping is not in the manual, and you must deduce it yourself.

Your goal is to pinpoint the leakage fault point T through probe commands, or provide the complete inspection path from the main valve to T.

You may issue one command at a time using the following formats:

1. Sensor Probe: Use the flaw detector at a specific valve node (e.g., probe node 5)
<probe>5</probe>

After probing, the maintenance team's current position updates to that node, and the instrument returns a characteristic code ({symbol1}, {symbol2}, or {symbol3}) indicating the change in distance to the fault source.

2. Dismantle Verification: Request workers to dismantle and verify if a node is the leak point (e.g., verify node 3)
<is_target>3</is_target>

Returns "Yes" or "No", maintenance team's current position unchanged.

3. Path Validation: Submit a complete inspection path from the main valve to a node (e.g., path 1,2,5)
<check_path>1,2,5</check_path>

Returns "Yes" or "No", indicating whether this path perfectly traces the route from the main valve to the fault point T.

When you have determined the fault node, submit your report:
<answer>node_id</answer>

For example:
<answer>7</answer>

Or submit the complete inspection path:
<answer>1,3,7</answer>

Accurate troubleshooting enables rapid network repair; errors aggravate downtime losses. Try to minimize probe steps to reduce inspection costs.
"""

    contextualized_rule_zh_5 = """\
我们来执行一次"洗钱网络隐蔽实控人追踪"的司法调查任务，规则如下：

金融情报中心勾勒出了一棵复杂的资金流向与股权代持结构树，包含 {n} 个账户/实体节点（编号从 1 到 {n}），源头公司（根节点）为 {root}。公开的资金流转拓扑如下：{tree_structure}

调查显示存在一个隐藏的最终资金沉淀账户（实控人） T。同时，我为每个节点标记了其注册所在的司法辖区颜色代码（共有 {num_colors} 种辖区分类）。

此外，跨国取证遭遇壁垒，只能获取一种模糊的风险反馈机制：当你对特定账户发起调查取证时，监控网络会根据该账户与真实目标 T 的"关系链距离变化"给出三种风险变动标记之一：{symbol1}、{symbol2}、{symbol3}。这三个标记分别对应"线索偏离目标"（更远）、"关系层级持平"和"逼近真实目标"（更近）三种情况，但具体的标记暗号需要你作为调查员自行破解。

你的目标是通过取证指令锁定最终实控人账户 T，或给出从源头公司到 T 的完整资金流转证据链。

每次只能下达一项指令，使用以下格式：

1. 调查取证：对某个账户/实体进行穿透式查证（例如查证节点 5）
<probe>5</probe>

查证后，你的调查准星会更新为该节点，系统会返回一个风险变动标记（{symbol1}、{symbol2} 或 {symbol3}），表示你与最终实控人的关系链距离变化。

2. 冻结传唤：直接向某节点发出传唤并核实其是否为最终实控人（例如核实节点 3）
<is_target>3</is_target>

返回"是"或"否"，不改变当前调查准星。

3. 证据链审查：提交一条从源头公司到某账户的完整资金流转证据链（例如证据链 1,2,5）
<check_path>1,2,5</check_path>

返回"是"或"否"，表示该证据链是否恰好完整还原了从源头直达实控人 T 的洗钱链路。

当你锁定实控人账户后，提交卷宗：
<answer>节点编号</answer>

例如：
<answer>7</answer>

或者提交完整资金流转证据链：
<answer>1,3,7</answer>

指控准确即可成功收网，打草惊蛇则导致线索中断。请在有限的取证次数内破案以防止资金外逃。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Let's conduct a "Hidden Ultimate Beneficial Owner Tracking" judicial investigation task. Here are the rules:

The Financial Intelligence Unit has mapped out a complex money flow and proxy equity structure tree containing {n} account/entity nodes (numbered 1 to {n}), with the source company (root node) at {root}. The public topology of fund transfers is: {tree_structure}

Investigations reveal a hidden ultimate fund sink account (the Ultimate Beneficial Owner, UBO) T. Additionally, each node is tagged with a color code representing its registered legal jurisdiction (there are {num_colors} distinct jurisdiction categories).

Furthermore, due to cross-border evidence collection barriers, we can only rely on an obscure risk feedback mechanism: when you initiate an evidentiary probe on a specific account, the monitoring network returns one of three risk shift markers based on the change in "chain-of-relationship distance" to the true target T: {symbol1}, {symbol2}, {symbol3}. These three markers correspond to "clues diverging from the target" (farther away), "relationship tier unchanged" (no change), and "approaching the true target" (closer). However, the specific cipher of these markers is hidden, and you, as the investigator, must crack it.

Your goal is to lock onto the ultimate UBO account T through probe commands, or provide the complete chain of evidence of fund transfers from the source company to T.

You may issue one command at a time using the following formats:

1. Evidentiary Probe: Conduct a look-through probe on an account/entity (e.g., probe node 5)
<probe>5</probe>

After probing, your investigative crosshairs update to that node, and the system returns a risk shift marker ({symbol1}, {symbol2}, or {symbol3}) indicating how your relationship chain distance to the UBO has changed.

2. Subpoena & Freeze: Directly subpoena a node to verify if it is the ultimate UBO (e.g., verify node 3)
<is_target>3</is_target>

Returns "Yes" or "No", current investigative crosshairs unchanged.

3. Evidence Chain Audit: Submit a complete chain of fund transfer evidence from the source company to an account (e.g., chain 1,2,5)
<check_path>1,2,5</check_path>

Returns "Yes" or "No", indicating whether this evidence chain perfectly reconstructs the money laundering route from the source directly to UBO T.

When you have locked onto the UBO account, submit your case file:
<answer>node_id</answer>

For example:
<answer>7</answer>

Or submit the complete chain of fund transfer evidence:
<answer>1,3,7</answer>

An accurate indictment leads to a successful bust; alerting the suspects prematurely causes the trail to go cold. Please solve the case with minimal probes to prevent capital flight.
"""

    tags = ["answer", "probe", "is_target", "check_path"]

    reasoning_type = "归纳推理"
    data_structure = "树"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 6,
                "root": 1,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6)],
                "colors": {1:"红", 2:"红", 3:"蓝", 4:"绿", 5:"绿", 6:"蓝"},
                "target": 5,
                "symbols": ["△", "○", "◇"],
                "mapping": {-1: "△", 0: "○", 1: "◇"},
            },
            2: {
                "n": 10,
                "root": 1,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (6,10)],
                "colors": {1:"红", 2:"红", 3:"蓝", 4:"红", 5:"绿", 6:"蓝", 7:"绿", 8:"黄", 9:"黄", 10:"绿"},
                "target": 9,
                "symbols": ["α", "β", "γ"],
                "mapping": {-1: "β", 0: "γ", 1: "α"},
            },
            3: {
                "n": 15,
                "root": 1,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (4,9), (5,10), (6,11), (6,12), (7,13), (7,14), (8,15)],
                "colors": {1:"红", 2:"蓝", 3:"绿", 4:"红", 5:"黄", 6:"蓝", 7:"紫", 8:"红", 9:"黄", 10:"绿", 11:"紫", 12:"蓝", 13:"红", 14:"黄", 15:"绿"},
                "target": 12,
                "symbols": ["★", "■", "●"],
                "mapping": {-1: "■", 0: "●", 1: "★"},
            },
            4: {
                "n": 20,
                "root": 1,
                "edges": [(1,2), (1,3), (1,4), (2,5), (2,6), (3,7), (3,8), (4,9), (4,10), (5,11), (5,12), (6,13), (7,14), (7,15), (8,16), (9,17), (10,18), (10,19), (11,20)],
                "colors": {1:"红", 2:"蓝", 3:"绿", 4:"黄", 5:"紫", 6:"橙", 7:"红", 8:"蓝", 9:"绿", 10:"黄", 11:"紫", 12:"橙", 13:"红", 14:"蓝", 15:"绿", 16:"黄", 17:"紫", 18:"橙", 19:"红", 20:"蓝"},
                "target": 18,
                "symbols": ["A", "B", "C"],
                "mapping": {-1: "B", 0: "C", 1: "A"},
            },
            5: {
                "n": 31,
                "root": 1,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (4,9), (5,10), (5,11), (6,12), (6,13), (7,14), (7,15), (8,16), (8,17), (9,18), (9,19), (10,20), (10,21), (11,22), (12,23), (12,24), (13,25), (14,26), (14,27), (15,28), (16,29), (17,30), (18,31)],
                "colors": {i: ["红","蓝","绿","黄","紫","橙"][i % 6] for i in range(1, 32)},
                "target": 25,
                "symbols": ["◆", "▲", "◎"],
                "mapping": {-1: "▲", 0: "◎", 1: "◆"},
            },
        },
        "en": {
            1: {
                "n": 6,
                "root": 1,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6)],
                "colors": {1:"Red", 2:"Red", 3:"Blue", 4:"Green", 5:"Green", 6:"Blue"},
                "target": 5,
                "symbols": ["△", "○", "◇"],
                "mapping": {-1: "△", 0: "○", 1: "◇"},
            },
            2: {
                "n": 10,
                "root": 1,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (5,9), (6,10)],
                "colors": {1:"Red", 2:"Red", 3:"Blue", 4:"Red", 5:"Green", 6:"Blue", 7:"Green", 8:"Yellow", 9:"Yellow", 10:"Green"},
                "target": 9,
                "symbols": ["α", "β", "γ"],
                "mapping": {-1: "β", 0: "γ", 1: "α"},
            },
            3: {
                "n": 15,
                "root": 1,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (4,9), (5,10), (6,11), (6,12), (7,13), (7,14), (8,15)],
                "colors": {1:"Red", 2:"Blue", 3:"Green", 4:"Red", 5:"Yellow", 6:"Blue", 7:"Purple", 8:"Red", 9:"Yellow", 10:"Green", 11:"Purple", 12:"Blue", 13:"Red", 14:"Yellow", 15:"Green"},
                "target": 12,
                "symbols": ["★", "■", "●"],
                "mapping": {-1: "■", 0: "●", 1: "★"},
            },
            4: {
                "n": 20,
                "root": 1,
                "edges": [(1,2), (1,3), (1,4), (2,5), (2,6), (3,7), (3,8), (4,9), (4,10), (5,11), (5,12), (6,13), (7,14), (7,15), (8,16), (9,17), (10,18), (10,19), (11,20)],
                "colors": {1:"Red", 2:"Blue", 3:"Green", 4:"Yellow", 5:"Purple", 6:"Orange", 7:"Red", 8:"Blue", 9:"Green", 10:"Yellow", 11:"Purple", 12:"Orange", 13:"Red", 14:"Blue", 15:"Green", 16:"Yellow", 17:"Purple", 18:"Orange", 19:"Red", 20:"Blue"},
                "target": 18,
                "symbols": ["A", "B", "C"],
                "mapping": {-1: "B", 0: "C", 1: "A"},
            },
            5: {
                "n": 31,
                "root": 1,
                "edges": [(1,2), (1,3), (2,4), (2,5), (3,6), (3,7), (4,8), (4,9), (5,10), (5,11), (6,12), (6,13), (7,14), (7,15), (8,16), (8,17), (9,18), (9,19), (10,20), (10,21), (11,22), (12,23), (12,24), (13,25), (14,26), (14,27), (15,28), (16,29), (17,30), (18,31)],
                "colors": {i: ["Red","Blue","Green","Yellow","Purple","Orange"][i % 6] for i in range(1, 32)},
                "target": 25,
                "symbols": ["◆", "▲", "◎"],
                "mapping": {-1: "▲", 0: "◎", 1: "◆"},
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
        
        self._game_info["n"] = cfg["n"]
        self._game_info["root"] = cfg["root"]
        self.root = cfg["root"]
        self.target = cfg["target"]
        self.colors = cfg["colors"]
        self.mapping = cfg["mapping"]
        
        self.edges = cfg["edges"]
        self.children = {i: [] for i in range(1, cfg["n"] + 1)}
        self.parent = {i: None for i in range(1, cfg["n"] + 1)}
        
        for p, c in self.edges:
            self.children[p].append(c)
            self.parent[c] = p
        
        edge_str = ", ".join([f"({p},{c})" for p, c in self.edges])
        self._game_info["tree_structure"] = edge_str
        
        self._game_info["num_colors"] = len(set(self.colors.values()))
        self._game_info["symbol1"] = cfg["symbols"][0]
        self._game_info["symbol2"] = cfg["symbols"][1]
        self._game_info["symbol3"] = cfg["symbols"][2]
        
        self.current_position = self.root
        
        self.target_path = self._get_path_from_root(self.target)

    def _get_path_from_root(self, node):
        path = []
        curr = node
        while curr is not None:
            path.append(curr)
            curr = self.parent[curr]
            if curr is None: break
        path.reverse()
        return path

    def _compute_lcp_length(self, node1, node2):
        path1 = self._get_path_from_root(node1)
        path2 = self._get_path_from_root(node2)
        
        lcp = 0
        for i in range(min(len(path1), len(path2))):
            if path1[i] == path2[i]:
                lcp = i
            else:
                break
        return lcp

    def _is_valid_node(self, node_id):
        try:
            node = int(node_id)
            return 1 <= node <= self._game_info["n"]
        except:
            return False

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            node = int(raw_ans)
            return node == self.target
        except:
            pass
        
        try:
            path_nodes = [int(x.strip()) for x in raw_ans.split(",")]
            return path_nodes == self.target_path
        except:
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_invalid = "错误：节点编号无效。"
            error_format = "错误：格式无效。"
        else:
            yes_res, no_res = "Yes", "No"
            error_invalid = "Error: Invalid node ID."
            error_format = "Error: Invalid format."

        if "probe" in parsed_info:
            node_str = parsed_info["probe"].strip()
            if not self._is_valid_node(node_str):
                return error_invalid
            
            node = int(node_str)
            
            lcp_before = self._compute_lcp_length(self.current_position, self.target)
            lcp_after = self._compute_lcp_length(node, self.target)
            delta = lcp_after - lcp_before
            
            self.current_position = node
            
            delta_sign = 1 if delta > 0 else (-1 if delta < 0 else 0)
            return self.mapping[delta_sign]

        elif "is_target" in parsed_info:
            node_str = parsed_info["is_target"].strip()
            if not self._is_valid_node(node_str):
                return error_invalid
            
            node = int(node_str)
            
            if node == self.target:
                return yes_res
            else:
                return no_res

        elif "check_path" in parsed_info:
            try:
                path_str = parsed_info["check_path"].strip()
                path_nodes = [int(x.strip()) for x in path_str.split(",")]
                
                if not all(1 <= n <= self._game_info["n"] for n in path_nodes):
                    return error_invalid
                
                if path_nodes == self.target_path:
                    return yes_res
                else:
                    return no_res
            except:
                return error_format

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        if correct == "是":
            return "否"
        if correct == "否":
            return "是"
        if correct.lower() == "yes":
            return "No" if correct[0].isupper() else "no"
        if correct.lower() == "no":
            return "Yes" if correct[0].isupper() else "yes"
        
        all_symbols = list(self.mapping.values())
        if correct in all_symbols:
            other_symbols = [s for s in all_symbols if s != correct]
            if other_symbols:
                return other_symbols[0]
        
        if correct.lstrip('-').isdigit():
            return str(int(correct) + 1)
        
        return correct

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        is_zh = self.config.language == "zh"
        yes_str = "是" if is_zh else "Yes"
        no_str = "否" if is_zh else "No"
        n_nodes = self._game_info["n"]

        lcp_before = self._compute_lcp_length(self.current_position, self.target)
        
        for node in range(1, n_nodes + 1):
            lcp_after = self._compute_lcp_length(node, self.target)
            delta = lcp_after - lcp_before
            delta_sign = 1 if delta > 0 else (-1 if delta < 0 else 0)
            symbol = self.mapping[delta_sign]
            
            queries.append({
                "query": f"<probe>{node}</probe>",
                "answer": symbol
            })

        for node in range(1, n_nodes + 1):
            ans = yes_str if node == self.target else no_str
            queries.append({
                "query": f"<is_target>{node}</is_target>",
                "answer": ans
            })

        for node in range(1, n_nodes + 1):
            path = self._get_path_from_root(node)
            path_str = ",".join(str(x) for x in path)
            ans = yes_str if path == self.target_path else no_str
            queries.append({
                "query": f"<check_path>{path_str}</check_path>",
                "answer": ans
            })

        return queries