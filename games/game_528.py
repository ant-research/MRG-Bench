from .base import Game
import random
from collections import defaultdict, deque


class HiddenTreeRuleGame(Game):

    game_rule_zh = """\
我们来玩一个"隐藏树规则推断"游戏。规则如下：

游戏设定：
- 存在一个节点集合 V = {{1, 2, ..., {n}}}。
- 有一棵固定但对你不可见的隐藏树 T，它连接了所有这些节点。
- 存在一个固定但未知的确定性规则 F，它会在特定情况下选择树边的某个子集。
- 你维护一个可见状态图 H，初始时 H 没有任何边。H 的边由两部分组成：
  * B：你主动成功添加的边（非树边）
  * W：根据规则 F 被动加入的树边
  
规则 F 的工作方式：
当你成功在 H 中添加一条边 (u,v) 时（且不产生环），规则 F 会查看隐藏树 T 中 u 到 v 的唯一路径，并从该路径的边中选择一个确定的子集加入到 W 中（仅加入之前未在 W 中的边）。F 的选择规则在整个游戏中保持不变。

你可以进行的操作：

1. 预判操作：询问"如果现在在 H 中添加边 (u,v) 是否会产生环？"
   格式：<query_predict>u,v</query_predict>
   返回：是 或 否

2. 连接操作：尝试在 H 中实际添加边 (u,v)
   格式：<query_connect>u,v</query_connect>
   返回：
   - 若产生环：返回"成环"
   - 若不成环：返回"不成环；本次新增 k 段"（k 表示从树中新加入 W 的边数）

3. 统计操作：查询当前 H 的连通块数量
   格式：<query_count></query_count>
   返回：一个整数（连通块数量）

操作限制：
- 连接操作最多 {max_connect} 次
- 预判操作最多 {max_predict} 次
- 统计操作次数不限

你的目标：
在探索阶段收集信息后，需要对以下 {challenge_count} 个节点对进行预测，判断"如果此刻添加该边是否会产生环"：
{challenge_pairs}

提交最终答案时，按顺序给出每个节点对的预测结果（是/否），用逗号分隔：

<answer>是,否,是</answer>

注意：
- 判断是否成环仅依赖当前 H 的连通性：如果 u 和 v 在 H 中已连通则会成环，否则不会
- 成功的连接操作会将 (u,v) 加入 B，同时根据规则 F 将树路径上的若干边加入 W
- 你需要通过有限的操作次数推断出当前 H 的连通结构
- 你必须答对所有 {challenge_count} 个预测才能获胜
"""

    game_rule_en = """\
Let's play a "Hidden Tree Rule Inference" game. Here are the rules:

Game Setup:
- There is a node set V = {{1, 2, ..., {n}}}.
- There exists a fixed but invisible hidden tree T connecting all these nodes.
- There exists a fixed but unknown deterministic rule F that selects a subset of tree edges under specific conditions.
- You maintain a visible state graph H, initially with no edges. H's edges consist of two parts:
  * B: edges you actively added successfully (non-tree edges)
  * W: tree edges passively added according to rule F
  
How rule F works:
When you successfully add an edge (u,v) to H (without creating a cycle), rule F examines the unique path from u to v in the hidden tree T, and selects a deterministic subset of edges from that path to add to W (only edges not previously in W are added). F's selection rule remains constant throughout the game.

Available operations:

1. Predict operation: Ask "Will adding edge (u,v) to H create a cycle?"
   Format: <query_predict>u,v</query_predict>
   Returns: Yes or No

2. Connect operation: Actually attempt to add edge (u,v) to H
   Format: <query_connect>u,v</query_connect>
   Returns:
   - If creates cycle: "Cycle created"
   - If no cycle: "No cycle; k new segments added" (k indicates number of tree edges newly added to W)

3. Count operation: Query the current number of connected components in H
   Format: <query_count></query_count>
   Returns: An integer (number of connected components)

Operation limits:
- Connect operations: at most {max_connect} times
- Predict operations: at most {max_predict} times
- Count operations: unlimited

Your goal:
After the exploration phase, you need to predict for the following {challenge_count} node pairs whether "adding this edge now would create a cycle":
{challenge_pairs}

When submitting your final answer, provide predictions for each pair in order (Yes/No), separated by commas:

<answer>Yes,No,Yes</answer>

Notes:
- Cycle detection depends only on current connectivity in H: if u and v are already connected in H, adding the edge creates a cycle; otherwise it doesn't
- Successful connect operations add (u,v) to B and, according to rule F, add some edges from the tree path to W
- You need to infer the connectivity structure of H through limited operations
- You must answer all {challenge_count} predictions correctly to win
"""

    # --- 场景 1：交通 ---
    contextualized_rule_zh_1 = """\
欢迎进入智能交通路网规划系统。你将作为城市交通总工程师，在未知地下管网的情况下，排查并构建城市交通联络线。
规则如下：

游戏设定：
- 存在一个关键交通枢纽集合 V = {{1, 2, ..., {n}}}。
- 有一棵固定但对你不可见的地下轨道管网树 T，它连接了所有这些枢纽。
- 存在一个固定但未知的系统审批规则 F，它会在特定情况下自动验收并启用地下路段的某个子集。
- 你维护一个当前的地上/地下交通状态图 H，初始时 H 没有任何线路。H 的线路由于两部分组成：
  * B：你主动成功修建的地面快速公交线路
  * W：根据审批规则 F 自动启用的地下管网路段
  
规则 F 的工作方式：
当你成功在 H 中修建一条线路 (u,v) 时（且不产生环线），审批规则 F 会查看地下管网树 T 中 u 到 v 的唯一路径，并从该路径的路段中选择一个确定的子集加入到 W 中（仅加入之前未在 W 中的路段）。F 的验收规则在整个工程中保持不变。

你可以进行的操作：

1. 预判操作：询问"如果现在在 H 中修建线路 (u,v) 是否会产生环线冗余？"
   格式：<query_predict>u,v</query_predict>
   返回：是 或 否

2. 连接操作：尝试在 H 中实际修建线路 (u,v)
   格式：<query_connect>u,v</query_connect>
   返回：
   - 若产生环线：返回"成环"
   - 若不产生环线：返回"不成环；本次新增 k 段"（k 表示从地下管网新加入 W 的路段数）

3. 统计操作：查询当前 H 的独立交通网络（连通块）数量
   格式：<query_count></query_count>
   返回：一个整数（连通块数量）

操作限制：
- 连接操作最多 {max_connect} 次
- 预判操作最多 {max_predict} 次
- 统计操作次数不限

你的目标：
在勘测阶段收集信息后，需要对以下 {challenge_count} 个枢纽对进行预测，判断"如果此刻修建该线路是否会产生环线冗余"：
{challenge_pairs}

提交最终答案时，按顺序给出每个枢纽对的预测结果（是/否），用逗号分隔：

<answer>是,否,是</answer>

注意：
- 判断是否成环仅依赖当前 H 的交通连通性：如果 u 和 v 在 H 中已连通则会成环，否则不会
- 成功的连接操作会将 (u,v) 加入 B，同时根据审批规则 F 将地下管网路径上的若干路段加入 W
- 你需要通过有限的操作次数推断出当前 H 的连通结构
- 你必须答对所有 {challenge_count} 个预测才能通过考核
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
Welcome to the Intelligent Traffic Network Planning System. As the Chief Traffic Engineer, you will route and construct city transit lines while dealing with an unknown underground pipe network. 
Here are the rules:

Game Setup:
- There is a set of key transit hubs V = {{1, 2, ..., {n}}}.
- There exists a fixed but invisible hidden underground pipeline tree T connecting all these hubs.
- There exists a fixed but unknown system approval rule F that automatically inspects and activates a subset of underground segments under specific conditions.
- You maintain a visible traffic state graph H, initially with no lines. H's lines consist of two parts:
  * B: Surface bus rapid transit lines you actively built successfully
  * W: Underground pipeline segments passively activated according to approval rule F
  
How rule F works:
When you successfully build a line (u,v) in H (without creating a transit loop), rule F examines the unique path from u to v in the underground tree T, and selects a deterministic subset of segments from that path to add to W (only segments not previously in W are added). F's approval rule remains constant throughout the project.

Available operations:

1. Predict operation: Ask "Will building line (u,v) in H create a transit loop?"
   Format: <query_predict>u,v</query_predict>
   Returns: Yes or No

2. Connect operation: Actually attempt to build line (u,v) in H
   Format: <query_connect>u,v</query_connect>
   Returns:
   - If creates loop: "Cycle created"
   - If no loop: "No cycle; k new segments added" (k indicates number of underground segments newly added to W)

3. Count operation: Query the current number of independent transit networks (connected components) in H
   Format: <query_count></query_count>
   Returns: An integer (number of connected components)

Operation limits:
- Connect operations: at most {max_connect} times
- Predict operations: at most {max_predict} times
- Count operations: unlimited

Your goal:
After the exploration phase, you need to predict for the following {challenge_count} hub pairs whether "building this line now would create a transit loop":
{challenge_pairs}

When submitting your final answer, provide predictions for each pair in order (Yes/No), separated by commas:

<answer>Yes,No,Yes</answer>

Notes:
- Cycle detection depends only on current transit connectivity in H: if u and v are already connected in H, building the line creates a cycle; otherwise it doesn't
- Successful connect operations add (u,v) to B and, according to rule F, add some segments from the underground path to W
- You need to infer the connectivity structure of H through limited operations
- You must answer all {challenge_count} predictions correctly to pass the assessment
"""

    # --- 场景 2：医疗 ---
    contextualized_rule_zh_2 = """\
欢迎进入靶向医疗手术推演系统。你将作为主治医师，在人体未知隐藏神经传导路径的情况下，规划并建立血管支架通道。
规则如下：

游戏设定：
- 存在一个关键器官/神经中枢集合 V = {{1, 2, ..., {n}}}。
- 有一棵固定但对你不可见的潜在生理依赖树 T，它连接了所有这些器官。
- 存在一个固定但未知的药物代谢激活规则 F，它会在特定情况下自动触发潜在生理路径的某个子集。
- 你维护一个当前的药物传导通道状态图 H，初始时 H 没有任何通道。H 的通道由两部分组成：
  * B：你主动成功通过靶向手术建立的人工通道
  * W：根据代谢激活规则 F 发生连锁药理反应而被动激活的隐性传导路径
  
规则 F 的工作方式：
当你成功在 H 中建立一条通道 (u,v) 时（且不产生药效闭环），激活规则 F 会查看生理依赖树 T 中 u 到 v 的唯一路径，并从该路径的依赖段中选择一个确定的子集加入到 W 中（仅加入之前未在 W 中的传导路径）。F 的代谢激活规则在整个治疗中保持不变。

你可以进行的操作：

1. 预判操作：询问"如果现在在 H 中建立通道 (u,v) 是否会产生药效闭环风险？"
   格式：<query_predict>u,v</query_predict>
   返回：是 或 否

2. 连接操作：尝试在 H 中实际进行手术建立通道 (u,v)
   格式：<query_connect>u,v</query_connect>
   返回：
   - 若产生闭环：返回"成环"
   - 若不产生闭环：返回"不成环；本次新增 k 段"（k 表示从生理网络中新加入 W 的隐性路径数）

3. 统计操作：查询当前 H 的独立生理系统（连通块）数量
   格式：<query_count></query_count>
   返回：一个整数（连通块数量）

操作限制：
- 连接操作最多 {max_connect} 次
- 预判操作最多 {max_predict} 次
- 统计操作次数不限

你的目标：
在探查阶段收集信息后，需要对以下 {challenge_count} 个器官对进行预测，判断"如果此刻建立该通道是否会产生药效闭环"：
{challenge_pairs}

提交最终答案时，按顺序给出每个器官对的预测结果（是/否），用逗号分隔：

<answer>是,否,是</answer>

注意：
- 判断是否成环仅依赖当前 H 的药效连通性：如果 u 和 v 在 H 中已连通则会产生闭环，否则不会
- 成功的连接操作会将 (u,v) 加入 B，同时根据代谢激活规则 F 将生理路径上的若干段加入 W
- 你需要通过有限的操作次数推断出当前 H 的连通结构
- 你必须答对所有 {challenge_count} 个预测才能制定出安全的手术方案
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
Welcome to the Targeted Medical Surgery Simulation System. As the attending physician, you will plan and establish vascular stent channels without full knowledge of the human body's hidden neural conduction pathways.
Here are the rules:

Game Setup:
- There is a set of key organs/neural centers V = {{1, 2, ..., {n}}}.
- There exists a fixed but invisible hidden physiological dependency tree T connecting all these organs.
- There exists a fixed but unknown drug metabolism activation rule F that automatically triggers a subset of potential physiological pathways under specific conditions.
- You maintain a visible drug conduction state graph H, initially with no channels. H's channels consist of two parts:
  * B: Artificial channels you actively and successfully established via targeted surgery
  * W: Hidden conduction pathways passively activated due to chain pharmacological reactions according to rule F
  
How rule F works:
When you successfully establish a channel (u,v) in H (without creating a pharmacological loop), activation rule F examines the unique path from u to v in the physiological tree T, and selects a deterministic subset of segments from that path to add to W (only pathways not previously in W are added). F's metabolic activation rule remains constant throughout the treatment.

Available operations:

1. Predict operation: Ask "Will establishing channel (u,v) in H create a pharmacological loop risk?"
   Format: <query_predict>u,v</query_predict>
   Returns: Yes or No

2. Connect operation: Actually attempt to establish channel (u,v) in H via surgery
   Format: <query_connect>u,v</query_connect>
   Returns:
   - If creates loop: "Cycle created"
   - If no loop: "No cycle; k new segments added" (k indicates the number of hidden pathways newly added to W)

3. Count operation: Query the current number of independent physiological systems (connected components) in H
   Format: <query_count></query_count>
   Returns: An integer (number of connected components)

Operation limits:
- Connect operations: at most {max_connect} times
- Predict operations: at most {max_predict} times
- Count operations: unlimited

Your goal:
After the exploration phase, you need to predict for the following {challenge_count} organ pairs whether "establishing this channel now would create a pharmacological loop":
{challenge_pairs}

When submitting your final answer, provide predictions for each pair in order (Yes/No), separated by commas:

<answer>Yes,No,Yes</answer>

Notes:
- Cycle detection depends only on current pharmacological connectivity in H: if u and v are already connected in H, establishing the channel creates a loop; otherwise it doesn't
- Successful connect operations add (u,v) to B and, according to metabolic rule F, add some segments from the physiological path to W
- You need to infer the connectivity structure of H through limited operations
- You must answer all {challenge_count} predictions correctly to formulate a safe surgical plan
"""

    # --- 场景 3：教育 ---
    contextualized_rule_zh_3 = """\
欢迎使用自适应教育认知图谱系统。你将作为高级导师，在未知学生底层认知依赖的情况下，通过启发式教学建立知识点间的关联。
规则如下：

游戏设定：
- 存在一个核心知识点集合 V = {{1, 2, ..., {n}}}。
- 有一棵固定但对你不可见的底层认知依赖树 T，它连接了所有这些知识点。
- 存在一个固定但未知的学生顿悟泛化规则 F，它会在特定教学启发下自动打通认知依赖链路的某个子集。
- 你维护一个可见的学生当前知识关联状态图 H，初始时 H 没有任何关联。H 的关联由两部分组成：
  * B：你主动成功通过跨章节教学建立的知识联结
  * W：根据顿悟规则 F，学生被动触发并自动领悟的底层认知链路
  
规则 F 的工作方式：
当你成功在 H 中建立知识联结 (u,v) 时（且不产生认知循环论证），顿悟规则 F 会查看认知依赖树 T 中 u 到 v 的唯一路径，并从该路径的链路中选择一个确定的子集加入到 W 中（仅加入之前未在 W 中的链路）。F 的领悟泛化规则在整个教学周期中保持不变。

你可以进行的操作：

1. 预判操作：询问"如果现在在 H 中建立联结 (u,v) 是否会产生逻辑闭环（循环论证）？"
   格式：<query_predict>u,v</query_predict>
   返回：是 或 否

2. 连接操作：尝试在 H 中实际启发教学以建立联结 (u,v)
   格式：<query_connect>u,v</query_connect>
   返回：
   - 若产生闭环：返回"成环"
   - 若不产生闭环：返回"不成环；本次新增 k 段"（k 表示学生顿悟新加入 W 的认知链路数）

3. 统计操作：查询当前 H 的独立知识体系（连通块）数量
   格式：<query_count></query_count>
   返回：一个整数（连通块数量）

操作限制：
- 连接操作最多 {max_connect} 次
- 预判操作最多 {max_predict} 次
- 统计操作次数不限

你的目标：
在教学摸底阶段收集信息后，需要对以下 {challenge_count} 个知识点对进行预测，判断"如果此刻启发该联结是否会导致认知闭环"：
{challenge_pairs}

提交最终答案时，按顺序给出每个知识点对的预测结果（是/否），用逗号分隔：

<answer>是,否,是</answer>

注意：
- 判断是否成环仅依赖当前 H 的知识连通性：如果 u 和 v 在 H 中已建立关联则会产生闭环，否则不会
- 成功的连接操作会将 (u,v) 加入 B，同时根据顿悟规则 F 将认知路径上的若干链路加入 W
- 你需要通过有限的操作次数推断出当前学生的认知连通结构
- 你必须答对所有 {challenge_count} 个预测才能完成教学大纲的制定
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Adaptive Educational Cognitive Graph System. As a senior tutor, you will establish connections between knowledge points through heuristic teaching, dealing with the student's unknown underlying cognitive dependencies.
Here are the rules:

Game Setup:
- There is a set of core knowledge points V = {{1, 2, ..., {n}}}.
- There exists a fixed but invisible hidden cognitive dependency tree T connecting all these points.
- There exists a fixed but unknown student insight generalization rule F that automatically bridges a subset of cognitive dependency links under specific teaching heuristics.
- You maintain a visible student knowledge association state graph H, initially with no connections. H's connections consist of two parts:
  * B: Knowledge links you actively and successfully established via cross-chapter teaching
  * W: Underlying cognitive links passively triggered and automatically comprehended by the student according to insight rule F
  
How rule F works:
When you successfully establish a knowledge link (u,v) in H (without creating a circular reasoning loop), insight rule F examines the unique path from u to v in the cognitive dependency tree T, and selects a deterministic subset of links from that path to add to W (only links not previously in W are added). F's comprehension generalization rule remains constant throughout the teaching cycle.

Available operations:

1. Predict operation: Ask "Will establishing link (u,v) in H create a logical loop (circular reasoning)?"
   Format: <query_predict>u,v</query_predict>
   Returns: Yes or No

2. Connect operation: Actually attempt heuristic teaching to establish link (u,v) in H
   Format: <query_connect>u,v</query_connect>
   Returns:
   - If creates loop: "Cycle created"
   - If no loop: "No cycle; k new segments added" (k indicates the number of cognitive links newly added to W via student insight)

3. Count operation: Query the current number of independent knowledge systems (connected components) in H
   Format: <query_count></query_count>
   Returns: An integer (number of connected components)

Operation limits:
- Connect operations: at most {max_connect} times
- Predict operations: at most {max_predict} times
- Count operations: unlimited

Your goal:
After the preliminary teaching phase, you need to predict for the following {challenge_count} knowledge point pairs whether "inspiring this link now would cause a cognitive loop":
{challenge_pairs}

When submitting your final answer, provide predictions for each pair in order (Yes/No), separated by commas:

<answer>Yes,No,Yes</answer>

Notes:
- Cycle detection depends only on current knowledge connectivity in H: if u and v are already associated in H, establishing the link creates a loop; otherwise it doesn't
- Successful connect operations add (u,v) to B and, according to insight rule F, add some links from the cognitive path to W
- You need to infer the connectivity structure of H through limited operations
- You must answer all {challenge_count} predictions correctly to finalize the curriculum syllabus
"""

    # --- 场景 4：制造业/工业 ---
    contextualized_rule_zh_4 = """\
欢迎使用智能车间柔性生产调度系统。你将作为自动化工程师，在未知厂房底层暗线网络的情况下，配置并桥接生产工位间的物料传输链路。
规则如下：

游戏设定：
- 存在一个核心生产工位集合 V = {{1, 2, ..., {n}}}。
- 有一棵固定但对你不可见的底层预埋暗线网络树 T，它连接了所有这些工位。
- 存在一个固定但未知的工业控制自动负载均衡规则 F，它会在特定负荷变化下被动激活暗线网络的某个子集。
- 你维护一个当前的车间生产协同状态图 H，初始时 H 没有任何传输链路。H 的链路由于两部分组成：
  * B：你主动成功架设的柔性生产临时桥接带
  * W：根据负载均衡规则 F 被动激活的暗线传输段
  
规则 F 的工作方式：
当你成功在 H 中架设一条临时桥接带 (u,v) 时（且不产生死锁循环），负载均衡规则 F 会查看暗线树 T 中 u 到 v 的唯一路径，并从该路径的传输段中选择一个确定的子集加入到 W 中（仅加入之前未在 W 中的传输段）。F 的负载均衡策略在整个生产班次中保持不变。

你可以进行的操作：

1. 预判操作：询问"如果现在在 H 中架设桥接带 (u,v) 是否会导致物料死锁循环？"
   格式：<query_predict>u,v</query_predict>
   返回：是 或 否

2. 连接操作：尝试在 H 中实际架设临时桥接带 (u,v)
   格式：<query_connect>u,v</query_connect>
   返回：
   - 若产生死锁：返回"成环"
   - 若不死锁：返回"不成环；本次新增 k 段"（k 表示从暗线网络中新加入 W 的传输段数）

3. 统计操作：查询当前 H 的独立运转生产集群（连通块）数量
   格式：<query_count></query_count>
   返回：一个整数（连通块数量）

操作限制：
- 连接操作最多 {max_connect} 次
- 预判操作最多 {max_predict} 次
- 统计操作次数不限

你的目标：
在设备调试阶段收集信息后，需要对以下 {challenge_count} 个工位对进行预测，判断"如果此刻架设该桥接带是否会引发死锁循环"：
{challenge_pairs}

提交最终答案时，按顺序给出每个工位对的预测结果（是/否），用逗号分隔：

<answer>是,否,是</answer>

注意：
- 判断是否成环仅依赖当前 H 的链路连通性：如果 u 和 v 在 H 中已连通则会引发死锁，否则不会
- 成功的连接操作会将 (u,v) 加入 B，同时根据负载均衡规则 F 将暗线路径上的若干段加入 W
- 你需要通过有限的操作次数推断出当前 H 的连通结构
- 你必须答对所有 {challenge_count} 个预测才能批准产线的正式投产
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
Welcome to the Smart Workshop Flexible Production Scheduling System. As an automation engineer, you will configure and bridge material transfer links between production stations while dealing with an unknown underlying embedded wiring network.
Here are the rules:

Game Setup:
- There is a set of core production stations V = {{1, 2, ..., {n}}}.
- There exists a fixed but invisible hidden embedded wiring network tree T connecting all these stations.
- There exists a fixed but unknown industrial control load-balancing rule F that passively activates a subset of the wiring network under specific load changes.
- You maintain a visible workshop production synergy state graph H, initially with no transfer links. H's links consist of two parts:
  * B: Flexible production temporary bridges you actively built successfully
  * W: Embedded transfer segments passively activated according to load-balancing rule F
  
How rule F works:
When you successfully build a temporary bridge (u,v) in H (without creating a deadlock loop), load-balancing rule F examines the unique path from u to v in the embedded tree T, and selects a deterministic subset of transfer segments from that path to add to W (only segments not previously in W are added). F's load-balancing strategy remains constant throughout the production shift.

Available operations:

1. Predict operation: Ask "Will building bridge (u,v) in H cause a material deadlock loop?"
   Format: <query_predict>u,v</query_predict>
   Returns: Yes or No

2. Connect operation: Actually attempt to build temporary bridge (u,v) in H
   Format: <query_connect>u,v</query_connect>
   Returns:
   - If creates deadlock: "Cycle created"
   - If no deadlock: "No cycle; k new segments added" (k indicates the number of embedded segments newly added to W)

3. Count operation: Query the current number of independently operating production clusters (connected components) in H
   Format: <query_count></query_count>
   Returns: An integer (number of connected components)

Operation limits:
- Connect operations: at most {max_connect} times
- Predict operations: at most {max_predict} times
- Count operations: unlimited

Your goal:
After the equipment debugging phase, you need to predict for the following {challenge_count} station pairs whether "building this bridge now would trigger a deadlock loop":
{challenge_pairs}

When submitting your final answer, provide predictions for each pair in order (Yes/No), separated by commas:

<answer>Yes,No,Yes</answer>

Notes:
- Cycle detection depends only on current link connectivity in H: if u and v are already connected in H, building the bridge creates a deadlock; otherwise it doesn't
- Successful connect operations add (u,v) to B and, according to load-balancing rule F, add some segments from the embedded path to W
- You need to infer the connectivity structure of H through limited operations
- You must answer all {challenge_count} predictions correctly to approve the official launch of the production line
"""

    # --- 场景 5：法律 ---
    contextualized_rule_zh_5 = """\
欢迎使用经济犯罪证据链推演系统。你将作为主诉检察官，在案件背后资金暗网未明的情况下，通过庭审质证逐步构建案件的证据逻辑图。
规则如下：

游戏设定：
- 存在一个关键诉讼主体/证据集合 V = {{1, 2, ..., {n}}}。
- 有一棵固定但对你不可见的利益输送暗网树 T，它连接了所有这些主体/证据。
- 存在一个固定但未知的嫌疑人心理防线崩溃法则 F，它会在特定质证压力下迫使嫌疑人交代出暗网的某个子集。
- 你维护一个检方当前已掌握的证据链逻辑图 H，初始时 H 没有任何关联。H 的关联由两部分组成：
  * B：你主动成功通过庭审质证建立的直接证据关联
  * W：根据崩溃法则 F，嫌疑人迫于压力交代出的暗网关联线索
  
规则 F 的工作方式：
当你成功在 H 中抛出质证建立关联 (u,v) 时（且未形成逻辑闭环），心理防线崩溃法则 F 会查看利益暗网树 T 中 u 到 v 的唯一路径，并从该路径的线索中选择一个确定的子集加入到 W 中（仅加入之前未在 W 中的线索）。F 的心理博弈法则在整个庭审中保持不变。

你可以进行的操作：

1. 预判操作：询问"如果现在在 H 中抛出证据关联 (u,v) 是否足以形成逻辑闭环？"
   格式：<query_predict>u,v</query_predict>
   返回：是 或 否

2. 连接操作：尝试在庭审中实际抛出质证关联 (u,v)
   格式：<query_connect>u,v</query_connect>
   返回：
   - 若形成闭环：返回"成环"
   - 若未形成闭环：返回"不成环；本次新增 k 段"（k 表示嫌疑人新交代并加入 W 的暗网线索数）

3. 统计操作：查询当前 H 的孤立证据链条（连通块）数量
   格式：<query_count></query_count>
   返回：一个整数（连通块数量）

操作限制：
- 连接操作最多 {max_connect} 次
- 预判操作最多 {max_predict} 次
- 统计操作次数不限

你的目标：
在法庭调查阶段收集信息后，需要对以下 {challenge_count} 个诉讼主体/证据对进行预测，判断"如果此刻抛出该关联是否会直接构成证据闭环"：
{challenge_pairs}

提交最终答案时，按顺序给出每个证据对的预测结果（是/否），用逗号分隔：

<answer>是,否,是</answer>

注意：
- 判断是否成环仅依赖当前 H 的逻辑连通性：如果 u 和 v 在 H 中已连通，则建立该关联即宣告闭环形成，否则不会
- 成功的连接操作会将 (u,v) 加入 B，同时根据心理法则 F 将暗网路径上的若干线索加入 W
- 你需要通过有限的操作次数推断出当前 H 的连通结构
- 你必须答对所有 {challenge_count} 个预测才能确保最终的定罪量刑
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
Welcome to the Economic Crime Evidence Chain Simulation System. As the lead prosecutor, you will progressively build the logical graph of evidence through cross-examination, facing an unknown dark web of financial transfers behind the case.
Here are the rules:

Game Setup:
- There is a set of key litigation subjects/evidence V = {{1, 2, ..., {n}}}.
- There exists a fixed but invisible hidden dark web of interests tree T connecting all these subjects/evidence.
- There exists a fixed but unknown suspect psychological defense collapse rule F that forces the suspect to confess a subset of the dark web under specific cross-examination pressure.
- You maintain a visible prosecution evidence logic graph H, initially with no associations. H's associations consist of two parts:
  * B: Direct evidence associations you actively established successfully through cross-examination
  * W: Dark web clues confessed by the suspect under pressure according to collapse rule F
  
How rule F works:
When you successfully establish an association (u,v) in H (without forming a logical loop), psychological collapse rule F examines the unique path from u to v in the dark web tree T, and selects a deterministic subset of clues from that path to add to W (only clues not previously in W are added). F's psychological game rule remains constant throughout the trial.

Available operations:

1. Predict operation: Ask "Will presenting evidence association (u,v) in H sufficiently form a logical loop?"
   Format: <query_predict>u,v</query_predict>
   Returns: Yes or No

2. Connect operation: Actually attempt to present cross-examination association (u,v) in court
   Format: <query_connect>u,v</query_connect>
   Returns:
   - If forms loop: "Cycle created"
   - If no loop: "No cycle; k new segments added" (k indicates the number of dark web clues newly confessed and added to W)

3. Count operation: Query the current number of isolated evidence chains (connected components) in H
   Format: <query_count></query_count>
   Returns: An integer (number of connected components)

Operation limits:
- Connect operations: at most {max_connect} times
- Predict operations: at most {max_predict} times
- Count operations: unlimited

Your goal:
After the court investigation phase, you need to predict for the following {challenge_count} subject/evidence pairs whether "presenting this association now would directly form an evidence loop":
{challenge_pairs}

When submitting your final answer, provide predictions for each pair in order (Yes/No), separated by commas:

<answer>Yes,No,Yes</answer>

Notes:
- Cycle detection depends only on current logical connectivity in H: if u and v are already connected in H, establishing the association completes the loop; otherwise it doesn't
- Successful connect operations add (u,v) to B and, according to psychological rule F, add some clues from the dark web path to W
- You need to infer the connectivity structure of H through limited operations
- You must answer all {challenge_count} predictions correctly to secure the final conviction and sentencing
"""

    tags = ["answer", "query_predict", "query_connect", "query_count"]
    
    # 类属性：推理类型和数据结构
    reasoning_type = "归纳推理"
    data_structure = "树"

    # 难度配置：
    # 1 (简单)       - N=5, 规则F选择路径的前1/3边, 最多5次连接, 3次预判, 2个挑战
    # 2 (中等偏下)   - N=6, 规则F选择路径的前1/2边, 最多4次连接, 3次预判, 3个挑战
    # 3 (中等偏上)   - N=7, 规则F选择路径的所有边, 最多4次连接, 2次预判, 3个挑战
    # 4 (较难)       - N=8, 规则F选择路径中索引为偶数的边, 最多3次连接, 2次预判, 4个挑战
    # 5 (难)         - N=9, 规则F选择路径的后1/2边, 最多3次连接, 1次预判, 5个挑战

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "tree_edges": [(1,2), (2,3), (3,4), (4,5)],  # 线性树
                "rule_type": "first_third",  # 选择路径前1/3的边
                "max_connect": 5,
                "max_predict": 3,
                "challenge_pairs": [(1,5), (2,4)],
            },
            2: {
                "n": 6,
                "tree_edges": [(1,2), (1,3), (2,4), (2,5), (3,6)],  # 星形树变体
                "rule_type": "first_half",  # 选择路径前1/2的边
                "max_connect": 4,
                "max_predict": 3,
                "challenge_pairs": [(4,5), (4,6), (5,6)],
            },
            3: {
                "n": 7,
                "tree_edges": [(1,2), (2,3), (3,4), (2,5), (5,6), (5,7)],  # 复杂树
                "rule_type": "all",  # 选择路径所有边
                "max_connect": 4,
                "max_predict": 2,
                "challenge_pairs": [(1,4), (6,7), (4,6)],
            },
            4: {
                "n": 8,
                "tree_edges": [(1,2), (2,3), (3,4), (4,5), (3,6), (6,7), (7,8)],  # 链式分支树
                "rule_type": "even_index",  # 选择路径中索引为偶数的边(0-indexed)
                "max_connect": 3,
                "max_predict": 2,
                "challenge_pairs": [(1,5), (1,8), (5,8), (6,4)],
            },
            5: {
                "n": 9,
                "tree_edges": [(1,2), (2,3), (3,4), (4,5), (2,6), (6,7), (7,8), (8,9)],  # 深度树
                "rule_type": "last_half",  # 选择路径后1/2的边
                "max_connect": 3,
                "max_predict": 1,
                "challenge_pairs": [(1,5), (1,9), (5,9), (3,7), (4,8)],
            },
        },
        "en": {
            1: {
                "n": 5,
                "tree_edges": [(1,2), (2,3), (3,4), (4,5)],
                "rule_type": "first_third",
                "max_connect": 5,
                "max_predict": 3,
                "challenge_pairs": [(1,5), (2,4)],
            },
            2: {
                "n": 6,
                "tree_edges": [(1,2), (1,3), (2,4), (2,5), (3,6)],
                "rule_type": "first_half",
                "max_connect": 4,
                "max_predict": 3,
                "challenge_pairs": [(4,5), (4,6), (5,6)],
            },
            3: {
                "n": 7,
                "tree_edges": [(1,2), (2,3), (3,4), (2,5), (5,6), (5,7)],
                "rule_type": "all",
                "max_connect": 4,
                "max_predict": 2,
                "challenge_pairs": [(1,4), (6,7), (4,6)],
            },
            4: {
                "n": 8,
                "tree_edges": [(1,2), (2,3), (3,4), (4,5), (3,6), (6,7), (7,8)],
                "rule_type": "even_index",
                "max_connect": 3,
                "max_predict": 2,
                "challenge_pairs": [(1,5), (1,8), (5,8), (6,4)],
            },
            5: {
                "n": 9,
                "tree_edges": [(1,2), (2,3), (3,4), (4,5), (2,6), (6,7), (7,8), (8,9)],
                "rule_type": "last_half",
                "max_connect": 3,
                "max_predict": 1,
                "challenge_pairs": [(1,5), (1,9), (5,9), (3,7), (4,8)],
            },
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏状态"""
        lang = self.config.language
        diff = int(self.config.difficulty)  # 确保是整数

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        self._game_info["n"] = cfg["n"]
        self._game_info["max_connect"] = cfg["max_connect"]
        self._game_info["max_predict"] = cfg["max_predict"]
        self._game_info["challenge_count"] = len(cfg["challenge_pairs"])
        
        # 格式化挑战对
        if lang == "zh":
            pairs_str = ", ".join([f"({u},{v})" for u, v in cfg["challenge_pairs"]])
        else:
            pairs_str = ", ".join([f"({u},{v})" for u, v in cfg["challenge_pairs"]])
        self._game_info["challenge_pairs"] = pairs_str
        
        # 隐藏树的边集（裁判知道，模型不知道）
        self.tree_edges = set()
        for u, v in cfg["tree_edges"]:
            self.tree_edges.add((min(u,v), max(u,v)))
        
        # 规则类型
        self.rule_type = cfg["rule_type"]
        
        # 挑战节点对
        self.challenge_pairs = cfg["challenge_pairs"]
        
        # 构建树的邻接表（用于路径查找）
        self.tree_adj = defaultdict(list)
        for u, v in self.tree_edges:
            self.tree_adj[u].append(v)
            self.tree_adj[v].append(u)
        
        # 状态图 H 的边集
        self.B = set()  # 模型主动添加的边
        self.W = set()  # 根据规则F被动加入的树边
        
        # 操作计数
        self.connect_count = 0
        self.predict_count = 0

    def _find_tree_path(self, u, v):
        """在隐藏树中找到u到v的唯一路径（BFS）"""
        if u == v:
            return []
        
        queue = deque([(u, [u])])
        visited = {u}
        
        while queue:
            node, path = queue.popleft()
            for neighbor in self.tree_adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    if neighbor == v:
                        # 将路径转换为边的列表
                        edges = []
                        for i in range(len(new_path) - 1):
                            a, b = new_path[i], new_path[i+1]
                            edges.append((min(a,b), max(a,b)))
                        return edges
                    queue.append((neighbor, new_path))
        
        return []  # 不应该发生（树是连通的）

    def _apply_rule_F(self, path_edges):
        """根据规则F从路径边中选择子集"""
        if not path_edges:
            return []
        
        if self.rule_type == "first_third":
            k = max(1, len(path_edges) // 3)
            return path_edges[:k]
        elif self.rule_type == "first_half":
            k = max(1, len(path_edges) // 2)
            return path_edges[:k]
        elif self.rule_type == "all":
            return path_edges
        elif self.rule_type == "even_index":
            return [path_edges[i] for i in range(0, len(path_edges), 2)]
        elif self.rule_type == "last_half":
            k = max(1, len(path_edges) // 2)
            return path_edges[-k:]
        else:
            return []

    def _is_connected_in_H(self, u, v):
        """检查u和v在当前状态图H中是否连通"""
        # H的边集 = B ∪ W
        H_edges = self.B | self.W
        
        # 构建H的邻接表
        H_adj = defaultdict(list)
        for a, b in H_edges:
            H_adj[a].append(b)
            H_adj[b].append(a)
        
        # BFS检查连通性
        if u == v:
            return True
        
        queue = deque([u])
        visited = {u}
        
        while queue:
            node = queue.popleft()
            if node == v:
                return True
            for neighbor in H_adj[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False

    def _count_components(self):
        """计算当前状态图H的连通块数量"""
        H_edges = self.B | self.W
        H_adj = defaultdict(list)
        for a, b in H_edges:
            H_adj[a].append(b)
            H_adj[b].append(a)
        
        visited = set()
        components = 0
        
        for node in range(1, self._game_info["n"] + 1):
            if node not in visited:
                components += 1
                # BFS遍历该连通块
                queue = deque([node])
                visited.add(node)
                while queue:
                    curr = queue.popleft()
                    for neighbor in H_adj[curr]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
        
        return components

    def evaluate(self, parsed_info):
        """评估最终答案是否正确"""
        if "answer" not in parsed_info:
            return False
            
        raw_ans = parsed_info["answer"].strip()
        
        # 解析答案
        predictions = [x.strip() for x in raw_ans.split(",")]
        
        if len(predictions) != len(self.challenge_pairs):
            return False
        
        # 标准化答案
        if self.config.language == "zh":
            yes_vals = ["是"]
            no_vals = ["否"]
        else:
            yes_vals = ["Yes", "yes", "YES"]
            no_vals = ["No", "no", "NO"]
        
        # 检查每个预测
        for i, (u, v) in enumerate(self.challenge_pairs):
            pred = predictions[i].strip(" \t\n\r.。!！")
            # 计算真实答案：如果u和v在H中已连通则会成环
            actual = self._is_connected_in_H(u, v)
            
            if actual:  # 会成环
                if pred not in yes_vals:
                    return False
            else:  # 不会成环
                if pred not in no_vals:
                    return False
        
        return True

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        由于 connect 操作有副作用（会改变游戏状态），这里仅返回无状态查询。
        """
        results = []
        n = self._game_info["n"]
        
        # 准备本地化字符串
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
            
        # 1. 统计操作
        results.append({
            "query": "<query_count></query_count>",
            "answer": str(self._count_components())
        })
        
        # 2. 预判操作 (遍历所有无向边 u < v)
        for u in range(1, n + 1):
            for v in range(u + 1, n + 1):
                is_connected = self._is_connected_in_H(u, v)
                ans_predict = yes_res if is_connected else no_res
                results.append({
                    "query": f"<query_predict>{u},{v}</query_predict>",
                    "answer": ans_predict
                })
                
        return results

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑"""
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            cycle_res = "成环"
            no_cycle_res = "不成环；本次新增 {} 段"
            error_format = "错误：格式无效"
            error_range = "错误：节点超出范围"
            error_limit_connect = "错误：连接操作次数已达上限"
            error_limit_predict = "错误：预判操作次数已达上限"
        else:
            yes_res, no_res = "Yes", "No"
            cycle_res = "Cycle created"
            no_cycle_res = "No cycle; {} new segments added"
            error_format = "Error: Invalid format"
            error_range = "Error: Node out of range"
            error_limit_connect = "Error: Connect operation limit reached"
            error_limit_predict = "Error: Predict operation limit reached"

        # 优先级：connect > predict > count
        if "query_connect" in parsed_info:
            if self.connect_count >= self._game_info["max_connect"]:
                return error_limit_connect
            
            try:
                raw = parsed_info["query_connect"]
                u, v = [int(x.strip()) for x in raw.split(",")]
                
                if u < 1 or u > self._game_info["n"] or v < 1 or v > self._game_info["n"]:
                    return error_range
                
                if u == v:
                    if self.config.language == "zh":
                        return "错误：不允许自环操作"
                    else:
                        return "Error: Self-loop not allowed"
                
                self.connect_count += 1
                
                # 检查是否会成环
                if self._is_connected_in_H(u, v):
                    return cycle_res
                else:
                    # 不成环，执行连接操作
                    # 1. 将(u,v)加入B
                    self.B.add((min(u,v), max(u,v)))
                    
                    # 2. 找到树中u到v的路径
                    path_edges = self._find_tree_path(u, v)
                    
                    # 3. 应用规则F
                    selected_edges = self._apply_rule_F(path_edges)
                    
                    # 4. 将选中的边加入W（仅加入之前不在W中的）
                    new_edges = [e for e in selected_edges if e not in self.W]
                    k = len(new_edges)
                    self.W.update(new_edges)
                    
                    return no_cycle_res.format(k)
                    
            except:
                return error_format

        elif "query_predict" in parsed_info:
            if self.predict_count >= self._game_info["max_predict"]:
                return error_limit_predict
            
            try:
                raw = parsed_info["query_predict"]
                u, v = [int(x.strip()) for x in raw.split(",")]
                
                if u < 1 or u > self._game_info["n"] or v < 1 or v > self._game_info["n"]:
                    return error_range
                
                if u == v:
                    if self.config.language == "zh":
                        return "错误：不允许自环操作"
                    else:
                        return "Error: Self-loop not allowed"
                
                self.predict_count += 1
                
                # 检查是否会成环（不改变状态）
                if self._is_connected_in_H(u, v):
                    return yes_res
                else:
                    return no_res
                    
            except:
                return error_format

        elif "query_count" in parsed_info:
            return str(self._count_components())

        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct):
        """生成错误答案"""
        # 纯整数情况（连通块数量查询）
        if correct.isdigit():
            val = int(correct)
            return str(val + 1) if val > 0 else "2"
        
        # 关键词替换（预判操作的 是/否）
        map_bool = {
            "是": "否", "否": "是",
            "Yes": "No", "No": "Yes",
            "yes": "no", "no": "yes",
            "YES": "NO", "NO": "YES"
        }
        
        if correct in map_bool:
            return map_bool[correct]
        
        # 连接操作的成环响应
        if self.config.language == "zh":
            if correct == "成环":
                return "不成环；本次新增 0 段"
            if correct.startswith("不成环"):
                return "成环"
        else:
            if correct == "Cycle created":
                return "No cycle; 0 new segments added"
            if correct.startswith("No cycle"):
                return "Cycle created"
            
        # 默认追加 _WRONG
        return correct + "_WRONG"