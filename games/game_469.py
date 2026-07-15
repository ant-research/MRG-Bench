from .base import Game
import random
from typing import List, Dict

class TransportationGraphConfigurationGame(Game):

    contextualized_rule_zh_1 = """\
【交通网络优化推理】
我们来玩一个"交通图配置推理"游戏，规则如下：

游戏设定了一个带权无向的区域交通网，包含五个核心城市节点 G、M、K、H、L。真实路网的边集为一条高速公路干线 G–M–K–H–L（不存在其他路线），但各路段的通行时间（小时）来自以下三种候选配置之一：
- 配置 A：G–M=2，M–K=3，K–H=2，H–L=2
- 配置 B：G–M=3，M–K=2，K–H=2，H–L=2
- 配置 C：G–M=2，M–K=2，K–H=3，H–L=2

已知：在三种配置中，未开启任何临时路线时，从 G 市到 L 市的最短通行时间均为 9 小时。

你的目标是识别当前路网真实采用的通行时间配置（A、B 或 C）。

你可以进行以下两类临时路线的测试查询（每次测试后路网会恢复为原始状态）：
1. 临时开通 M 市到 H 市的直达货运专线，通行时间为 4 小时，询问"此操作是否使 G 到 L 的最短通行时间严格变小？"
2. 临时开通 G 市到 K 市的直达货运专线，通行时间为 4 小时，询问"此操作是否使 G 到 L 的最短通行时间严格变小？"

反馈形式：
- "是"表示加边后新的 G 到 L 最短通行时间小于 9 小时
- "否"表示加边后新的 G 到 L 最短通行时间大于等于 9 小时

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 试验查询 M–H（内容为空）：
<query_mh></query_mh>

- 试验查询 G–K（内容为空）：
<query_gk></query_gk>

提交最终答案时，必须说明配置类型（A、B 或 C），格式如下：

<answer>配置</answer>

其中"配置"应为 A、B 或 C 中的一个字母。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Let's play a "Traffic Graph Configuration Deduction" game. Here are the rules:

The game involves a weighted undirected regional traffic network with five core city nodes: G, M, K, H, L. The true network's edge set is a highway chain G–M–K–H–L (no other routes exist), but the travel times (in hours) of each segment come from one of the following three candidate configurations:
- Configuration A: G–M=2, M–K=3, K–H=2, H–L=2
- Configuration B: G–M=3, M–K=2, K–H=2, H–L=2
- Configuration C: G–M=2, M–K=2, K–H=3, H–L=2

Known: In all three configurations, without any temporary routes, the shortest travel time from city G to L is 9 hours.

Your goal is to identify the true travel time configuration (A, B, or C).

You can perform the following two types of temporary route test queries (the network resets to its original state after each test):
1. Temporarily open a direct freight line between M and H taking 4 hours, and ask "Does this operation strictly decrease the shortest travel time from G to L?"
2. Temporarily open a direct freight line between G and K taking 4 hours, and ask "Does this operation strictly decrease the shortest travel time from G to L?"

Feedback format:
- "Yes" means the new shortest travel time from G to L after adding the route is less than 9 hours.
- "No" means the new shortest travel time from G to L after adding the route is greater than or equal to 9 hours.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Experimental query M–H (empty content):
<query_mh></query_mh>

- Experimental query G–K (empty content):
<query_gk></query_gk>

When submitting the final answer, specify the configuration type (A, B, or C), using this format:

<answer>Configuration</answer>

where "Configuration" should be one letter from A, B, or C.
"""

    contextualized_rule_zh_2 = """\
【医疗康复路径推理】
我们来玩一个"医疗干预配置推理"游戏，规则如下：

游戏设定了一个带权的康复路径图，包含五个关键生理恢复阶段 G、M、K、H、L。真实的康复路径为严格的顺序链条 G–M–K–H–L（不存在其他自然转化路径），但各阶段间所需的恢复时间（天数）来自以下三种候选配置之一：
- 配置 A：G–M=2，M–K=3，K–H=2，H–L=2
- 配置 B：G–M=3，M–K=2，K–H=2，H–L=2
- 配置 C：G–M=2，M–K=2，K–H=3，H–L=2

已知：在三种配置中，未施加任何靶向药物时，从阶段 G 到 L 的最短总恢复时间均为 9 天。

你的目标是识别患者真实对应的体质配置（A、B 或 C）。

你可以进行以下两类药物干预的临床试验查询（每次试验后患者状态会独立评估并恢复基线）：
1. 施加临时靶向药，打通 M 到 H 的代谢捷径，耗时 4 天，询问"此操作是否使 G 到 L 的最短总恢复时间严格变小？"
2. 施加临时靶向药，打通 G 到 K 的代谢捷径，耗时 4 天，询问"此操作是否使 G 到 L 的最短总恢复时间严格变小？"

反馈形式：
- "是"表示加药后新的 G 到 L 最短总恢复时间小于 9 天
- "否"表示加药后新的 G 到 L 最短总恢复时间大于等于 9 天

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 试验查询 M–H（内容为空）：
<query_mh></query_mh>

- 试验查询 G–K（内容为空）：
<query_gk></query_gk>

提交最终答案时，必须说明配置类型（A、B 或 C），格式如下：

<answer>配置</answer>

其中"配置"应为 A、B 或 C 中的一个字母。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Let's play a "Medical Pathway Configuration Deduction" game. Here are the rules:

The game involves a weighted undirected recovery pathway graph with five critical physiological stages: G, M, K, H, L. The true recovery path is a strict sequential chain G–M–K–H–L (no other natural paths exist), but the recovery times (in days) between stages come from one of the following three candidate configurations:
- Configuration A: G–M=2, M–K=3, K–H=2, H–L=2
- Configuration B: G–M=3, M–K=2, K–H=2, H–L=2
- Configuration C: G–M=2, M–K=2, K–H=3, H–L=2

Known: In all three configurations, without applying any targeted drugs, the shortest total recovery time from stage G to L is 9 days.

Your goal is to identify the true physiological configuration of the patient (A, B, or C).

You can perform the following two types of clinical trial queries (the patient state resets to baseline after each trial):
1. Apply a temporary targeted drug creating a metabolic shortcut from M to H taking 4 days, and ask "Does this operation strictly decrease the shortest total recovery time from G to L?"
2. Apply a temporary targeted drug creating a metabolic shortcut from G to K taking 4 days, and ask "Does this operation strictly decrease the shortest total recovery time from G to L?"

Feedback format:
- "Yes" means the new shortest recovery time from G to L after applying the drug is less than 9 days.
- "No" means the new shortest recovery time from G to L after applying the drug is greater than or equal to 9 days.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Experimental query M–H (empty content):
<query_mh></query_mh>

- Experimental query G–K (empty content):
<query_gk></query_gk>

When submitting the final answer, specify the configuration type (A, B, or C), using this format:

<answer>Configuration</answer>

where "Configuration" should be one letter from A, B, or C.
"""

    contextualized_rule_zh_3 = """\
【教育学习路径推理】
我们来玩一个"学习模块配置推理"游戏，规则如下：

游戏设定了一个带权无向的学习模块依赖图，包含五个进阶模块 G、M、K、H、L。真实的学习路径为基础链条 G–M–K–H–L（不存在其他前置条件），但掌握各相邻模块所需的学习周数来自以下三种候选配置之一：
- 配置 A：G–M=2，M–K=3，K–H=2，H–L=2
- 配置 B：G–M=3，M–K=2，K–H=2，H–L=2
- 配置 C：G–M=2，M–K=2，K–H=3，H–L=2

已知：在三种配置中，未引入任何强化课程时，从模块 G 掌握到 L 的最短总学习时间均为 9 周。

你的目标是识别学生群体真实适用的认知难度配置（A、B 或 C）。

你可以进行以下两类强化课程的教学试验查询（每次试验后教学计划会恢复为原始大纲）：
1. 临时引入一个从 M 直接跃升至 H 的集训营，耗时 4 周，询问"此操作是否使 G 到 L 的最短总学习时间严格变小？"
2. 临时引入一个从 G 直接跃升至 K 的集训营，耗时 4 周，询问"此操作是否使 G 到 L 的最短总学习时间严格变小？"

反馈形式：
- "是"表示加入集训营后新的 G 到 L 最短学习时间小于 9 周
- "否"表示加入集训营后新的 G 到 L 最短学习时间大于等于 9 周

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 试验查询 M–H（内容为空）：
<query_mh></query_mh>

- 试验查询 G–K（内容为空）：
<query_gk></query_gk>

提交最终答案时，必须说明配置类型（A、B 或 C），格式如下：

<answer>配置</answer>

其中"配置"应为 A、B 或 C 中的一个字母。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Let's play a "Learning Module Configuration Deduction" game. Here are the rules:

The game involves a weighted undirected learning dependency graph with five progressive modules: G, M, K, H, L. The true learning path is a basic chain G–M–K–H–L (no other prerequisites exist), but the required study times (in weeks) between modules come from one of the following three candidate configurations:
- Configuration A: G–M=2, M–K=3, K–H=2, H–L=2
- Configuration B: G–M=3, M–K=2, K–H=2, H–L=2
- Configuration C: G–M=2, M–K=2, K–H=3, H–L=2

Known: In all three configurations, without any intensive courses, the shortest total study time from module G to L is 9 weeks.

Your goal is to identify the true cognitive profile configuration of the students (A, B, or C).

You can perform the following two types of educational test queries (the curriculum resets to its original syllabus after each test):
1. Temporarily introduce an intensive bootcamp leaping from M to H taking 4 weeks, and ask "Does this operation strictly decrease the shortest total study time from G to L?"
2. Temporarily introduce an intensive bootcamp leaping from G to K taking 4 weeks, and ask "Does this operation strictly decrease the shortest total study time from G to L?"

Feedback format:
- "Yes" means the new shortest study time from G to L after introducing the bootcamp is less than 9 weeks.
- "No" means the new shortest study time from G to L after introducing the bootcamp is greater than or equal to 9 weeks.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Experimental query M–H (empty content):
<query_mh></query_mh>

- Experimental query G–K (empty content):
<query_gk></query_gk>

When submitting the final answer, specify the configuration type (A, B, or C), using this format:

<answer>Configuration</answer>

where "Configuration" should be one letter from A, B, or C.
"""

    contextualized_rule_zh_4 = """\
【工业生产线优化推理】
我们来玩一个"生产线配置推理"游戏，规则如下：

游戏设定了一个带权无向的流水线工序图，包含五个加工节点 G、M、K、H、L。真实的生产流程为一条主流水线 G–M–K–H–L（不存在其他传送带），但各相邻工序间的处理时间（小时）来自以下三种候选配置之一：
- 配置 A：G–M=2，M–K=3，K–H=2，H–L=2
- 配置 B：G–M=3，M–K=2，K–H=2，H–L=2
- 配置 C：G–M=2，M–K=2，K–H=3，H–L=2

已知：在三种配置中，未启用任何备用传送带时，从原料 G 到成品 L 的最短生产时间均为 9 小时。

你的目标是识别当前车间真实采用的设备工时配置（A、B 或 C）。

你可以进行以下两类设备调度的测试查询（每次测试后生产线会恢复为原始架构）：
1. 临时启用 M 到 H 的自动化直达传送带，处理时间为 4 小时，询问"此操作是否使 G 到 L 的最短生产时间严格变小？"
2. 临时启用 G 到 K 的自动化直达传送带，处理时间为 4 小时，询问"此操作是否使 G 到 L 的最短生产时间严格变小？"

反馈形式：
- "是"表示启用传送带后新的 G 到 L 最短生产时间小于 9 小时
- "否"表示启用传送带后新的 G 到 L 最短生产时间大于等于 9 小时

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 试验查询 M–H（内容为空）：
<query_mh></query_mh>

- 试验查询 G–K（内容为空）：
<query_gk></query_gk>

提交最终答案时，必须说明配置类型（A、B 或 C），格式如下：

<answer>配置</answer>

其中"配置"应为 A、B 或 C 中的一个字母。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Let's play an "Assembly Line Configuration Deduction" game. Here are the rules:

The game involves a weighted undirected workflow graph with five processing stations: G, M, K, H, L. The true production flow is a main assembly line chain G–M–K–H–L (no other conveyors exist), but the processing times (in hours) between adjacent stations come from one of the following three candidate configurations:
- Configuration A: G–M=2, M–K=3, K–H=2, H–L=2
- Configuration B: G–M=3, M–K=2, K–H=2, H–L=2
- Configuration C: G–M=2, M–K=2, K–H=3, H–L=2

Known: In all three configurations, without enabling any backup conveyors, the shortest production time from raw material G to finished product L is 9 hours.

Your goal is to identify the true equipment timing configuration of the workshop (A, B, or C).

You can perform the following two types of equipment scheduling test queries (the assembly line resets to its original architecture after each test):
1. Temporarily enable an automated direct conveyor from M to H taking 4 hours, and ask "Does this operation strictly decrease the shortest production time from G to L?"
2. Temporarily enable an automated direct conveyor from G to K taking 4 hours, and ask "Does this operation strictly decrease the shortest production time from G to L?"

Feedback format:
- "Yes" means the new shortest production time from G to L after enabling the conveyor is less than 9 hours.
- "No" means the new shortest production time from G to L after enabling the conveyor is greater than or equal to 9 hours.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Experimental query M–H (empty content):
<query_mh></query_mh>

- Experimental query G–K (empty content):
<query_gk></query_gk>

When submitting the final answer, specify the configuration type (A, B, or C), using this format:

<answer>Configuration</answer>

where "Configuration" should be one letter from A, B, or C.
"""

    contextualized_rule_zh_5 = """\
【法律诉讼程序推理】
我们来玩一个"诉讼程序配置推理"游戏，规则如下：

游戏设定了一个带权无向的司法流转图，包含五个必经程序节点 G、M、K、H、L。真实的诉讼路径为标准链条 G–M–K–H–L（不存在其他并行程序），但各程序间的审理周期（个月）来自以下三种候选配置之一：
- 配置 A：G–M=2，M–K=3，K–H=2，H–L=2
- 配置 B：G–M=3，M–K=2，K–H=2，H–L=2
- 配置 C：G–M=2，M–K=2，K–H=3，H–L=2

已知：在三种配置中，未动用任何特殊通道时，从立案 G 到终审 L 的最短总周期均为 9 个月。

你的目标是识别当前案件真实适用的司法管辖区周期配置（A、B 或 C）。

你可以进行以下两类特别程序的推演查询（每次推演后程序假定会恢复为常规流程）：
1. 临时申请 M 到 H 的专属仲裁通道，耗时 4 个月，询问"此操作是否使 G 到 L 的最短总周期严格变小？"
2. 临时申请 G 到 K 的快速禁令通道，耗时 4 个月，询问"此操作是否使 G 到 L 的最短总周期严格变小？"

反馈形式：
- "是"表示申请通道后新的 G 到 L 最短总周期小于 9 个月
- "否"表示申请通道后新的 G 到 L 最短总周期大于等于 9 个月

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 试验查询 M–H（内容为空）：
<query_mh></query_mh>

- 试验查询 G–K（内容为空）：
<query_gk></query_gk>

提交最终答案时，必须说明配置类型（A、B 或 C），格式如下：

<answer>配置</answer>

其中"配置"应为 A、B 或 C 中的一个字母。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Let's play a "Legal Procedure Configuration Deduction" game. Here are the rules:

The game involves a weighted undirected judicial workflow graph with five mandatory procedure nodes: G, M, K, H, L. The true litigation path is a standard chain G–M–K–H–L (no other parallel procedures exist), but the trial durations (in months) between procedures come from one of the following three candidate configurations:
- Configuration A: G–M=2, M–K=3, K–H=2, H–L=2
- Configuration B: G–M=3, M–K=2, K–H=2, H–L=2
- Configuration C: G–M=2, M–K=2, K–H=3, H–L=2

Known: In all three configurations, without using any special channels, the shortest total duration from filing G to final verdict L is 9 months.

Your goal is to identify the true jurisdiction duration configuration for the current case (A, B, or C).

You can perform the following two types of special procedure deduction queries (the procedural flow hypothetically resets to the conventional process after each query):
1. Temporarily apply for an exclusive arbitration channel from M to H taking 4 months, and ask "Does this operation strictly decrease the shortest total duration from G to L?"
2. Temporarily apply for a fast-track injunction from G to K taking 4 months, and ask "Does this operation strictly decrease the shortest total duration from G to L?"

Feedback format:
- "Yes" means the new shortest duration from G to L after applying the channel is less than 9 months.
- "No" means the new shortest duration from G to L after applying the channel is greater than or equal to 9 months.

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Experimental query M–H (empty content):
<query_mh></query_mh>

- Experimental query G–K (empty content):
<query_gk></query_gk>

When submitting the final answer, specify the configuration type (A, B, or C), using this format:

<answer>Configuration</answer>

where "Configuration" should be one letter from A, B, or C.
"""

    game_rule_zh = """\
我们来玩一个"图配置推理"游戏，规则如下：

游戏设定了一个带权无向图，包含五个节点 G、M、K、H、L。真实图的边集为一条链 G–M–K–H–L（不存在其他边），但边权来自以下三种候选配置之一：
- 配置 A：G–M=2，M–K=3，K–H=2，H–L=2
- 配置 B：G–M=3，M–K=2，K–H=2，H–L=2
- 配置 C：G–M=2，M–K=2，K–H=3，H–L=2

已知：在三种配置中，未加任何额外边时，G 到 L 的最短路距离均为 9。

你的目标是识别真实采用的边权配置（A、B 或 C）。

你可以进行以下两类试验查询（每次试验后图会恢复为原始状态）：
1. 向图中临时加入边 M–H，权重为 4，询问"此操作是否使 G 到 L 的最短路距离严格变小？"
2. 向图中临时加入边 G–K，权重为 4，询问"此操作是否使 G 到 L 的最短路距离严格变小？"

反馈形式：
- "是"表示加边后新的 G 到 L 最短路距离小于 9
- "否"表示加边后新的 G 到 L 最短路距离大于等于 9

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 试验查询 M–H（内容为空）：
<query_mh></query_mh>

- 试验查询 G–K（内容为空）：
<query_gk></query_gk>

提交最终答案时，必须说明配置类型（A、B 或 C），格式如下：

<answer>配置</answer>

其中"配置"应为 A、B 或 C 中的一个字母。
"""

    game_rule_en = """\
Let's play a "Graph Configuration Deduction" game. Here are the rules:

The game involves a weighted undirected graph with five nodes: G, M, K, H, L. The true graph's edge set is a chain G–M–K–H–L (no other edges exist), but the edge weights come from one of the following three candidate configurations:
- Configuration A: G–M=2, M–K=3, K–H=2, H–L=2
- Configuration B: G–M=3, M–K=2, K–H=2, H–L=2
- Configuration C: G–M=2, M–K=2, K–H=3, H–L=2

Known: In all three configurations, without any additional edges, the shortest path distance from G to L is 9.

Your goal is to identify the true edge weight configuration (A, B, or C).

You can perform the following two types of experimental queries (the graph resets to its original state after each experiment):
1. Temporarily add edge M–H with weight 4, and ask "Does this operation strictly decrease the shortest path distance from G to L?"
2. Temporarily add edge G–K with weight 4, and ask "Does this operation strictly decrease the shortest path distance from G to L?"

Feedback format:
- "Yes" means the new shortest path distance from G to L after adding the edge is less than 9
- "No" means the new shortest path distance from G to L after adding the edge is greater than or equal to 9

When you have collected enough information, submit your final answer. If the answer is wrong or the format is invalid, the game is a failure.

Each query must contain only one tag. Use the following XML format:

- Experimental query M–H (empty content):
<query_mh></query_mh>

- Experimental query G–K (empty content):
<query_gk></query_gk>

When submitting the final answer, specify the configuration type (A, B, or C), using this format:

<answer>Configuration</answer>

where "Configuration" should be one letter from A, B, or C.
"""

    tags = ["answer", "query_mh", "query_gk"]
    
    reasoning_type = "溯因推理"
    data_structure = "图"

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"config": "A"},
            2: {"config": "B"},
            3: {"config": "C"},
            4: {"config": "random_AB"},
            5: {"config": "random_ABC"},
        },
        "en": {
            1: {"config": "A"},
            2: {"config": "B"},
            3: {"config": "C"},
            4: {"config": "random_AB"},
            5: {"config": "random_ABC"},
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
        config_choice = cfg["config"]

        if config_choice == "random_AB":
            self.true_config = random.Random(42).choice(["A", "B"])
        elif config_choice == "random_ABC":
            self.true_config = random.Random(42).choice(["A", "B", "C"])
        else:
            self.true_config = config_choice

        self._game_info["n"] = 5

        self.configs = {
            "A": {"G-M": 2, "M-K": 3, "K-H": 2, "H-L": 2},
            "B": {"G-M": 3, "M-K": 2, "K-H": 2, "H-L": 2},
            "C": {"G-M": 2, "M-K": 2, "K-H": 3, "H-L": 2},
        }

        self.query_responses = {
            "A": {"query_mh": True, "query_gk": True},
            "B": {"query_mh": False, "query_gk": True},
            "C": {"query_mh": True, "query_gk": False},
        }

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip().upper()
        
        config_letter = None
        for char in raw_ans:
            if char in ["A", "B", "C"]:
                config_letter = char
                break
        
        if config_letter is None:
            return False
        
        return config_letter == self.true_config

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
            error_msg = "错误：无效的查询格式。"
        else:
            yes_res, no_res = "Yes", "No"
            error_msg = "Error: Invalid query format."

        if "query_mh" in parsed_info:
            result = self.query_responses[self.true_config]["query_mh"]
            return yes_res if result else no_res

        elif "query_gk" in parsed_info:
            result = self.query_responses[self.true_config]["query_gk"]
            return yes_res if result else no_res

        else:
            return error_msg

    def get_all_possible_queries(self) -> List[Dict]:
        if self.config.language == "zh":
            yes_res, no_res = "是", "否"
        else:
            yes_res, no_res = "Yes", "No"
        
        possible_queries = []
        query_tags = ["query_mh", "query_gk"]

        for tag in query_tags:
            result_bool = self.query_responses[self.true_config][tag]
            ans = yes_res if result_bool else no_res
            
            possible_queries.append({
                "query": f"<{tag}></{tag}>",
                "answer": ans
            })
            
        return possible_queries

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if correct == "是":
                return "否"
            elif correct == "否":
                return "是"
        else:
            lowered = correct.lower()
            if lowered == "yes":
                return "No" if correct[0].isupper() else "no"
            elif lowered == "no":
                return "Yes" if correct[0].isupper() else "yes"
        
        return correct + "_WRONG"