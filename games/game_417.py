import re
from .base import Game

class SubsetCoveringGameTraffic(Game):

    reasoning_type = "溯因推理"
    data_structure = "集合"

    game_rule_zh = """\
我们来玩一个"子集覆盖推理"游戏，规则如下：

游戏设定了一个基本集合 U = {{1,2,3,4,5,6}}，以及 5 个子集索引 S1, S2, S3, S4, S5。

我已秘密选择了一个子集族（记为 A、B、C 或 D），该子集族将每个索引 Si 映射为 U 的一个固定子集。你需要通过询问来推断出真实的子集族，并在该子集族下求解最小覆盖问题。

你可以反复向我提出以下两类问题（每次仅限一个问题），我会根据真实设定如实回答：

1. 单子集基数查询：询问某个子集 Si 的元素个数。回答一个整数。
2. 双子集合并基数查询：询问两个不同子集 Si 和 Sj 合并后的元素总数（即它们并集的大小）。回答一个整数。

你的目标是：
1. 确定真实的子集族标签（A、B、C 或 D）。
2. 求出在该子集族下，覆盖全集 U 所需的最少子集数量 k。
3. 给出一组达到该最小覆盖数的索引集合。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，游戏失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单子集基数查询（例如询问 S3 的大小）：
<query_size>3</query_size>

- 双子集合并基数查询（例如询问 S1 和 S4 合并后的大小）：
<query_union>1,4</query_union>

提交最终答案时，必须说明子集族标签（A、B、C 或 D）、最小覆盖数量 k，以及一组索引集合（用逗号隔开，顺序不限），格式如下：

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    game_rule_en = """\
Let's play a "Subset Covering Inference" game. Here are the rules:

The game has a base set U = {{1,2,3,4,5,6}} and 5 subset indices S1, S2, S3, S4, S5.

I have secretly chosen a subset family (labeled A, B, C, or D), which maps each index Si to a fixed subset of U. Your task is to infer the true subset family through queries, and then solve the minimum covering problem under that family.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully:

1. Single Subset Size Query: Ask for the number of elements in subset Si. Answer is an integer.
2. Pairwise Union Size Query: Ask for the total number of elements in the union of two different subsets Si and Sj. Answer is an integer.

Your goals are:
1. Determine the true subset family label (A, B, C, or D).
2. Find the minimum number k of subsets needed to cover the entire set U under that family.
3. Provide one index set that achieves this minimum coverage.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the game fails.

Each query must contain only one tag. Use the following XML format:

- Single Subset Size Query (e.g., asking for size of S3):
<query_size>3</query_size>

- Pairwise Union Size Query (e.g., asking for union size of S1 and S4):
<query_union>1,4</query_union>

When submitting the final answer, specify the family label (A, B, C, or D), minimum cover number k, and an index set (comma-separated, order does not matter), using this format:

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    contextualized_rule_zh_1 = """\
智能交通管理系统正在运行。城市交通网络中被标记了 6 个核心拥堵路口，记为集合 U = {1,2,3,4,5,6}。
交管局规划了 5 条常态化巡逻路线，索引为 S1, S2, S3, S4, S5。

系统后台秘密部署了四套巡逻方案（记为 A、B、C 或 D），该方案将每条巡逻路线 Si 固定映射为 U 中特定的一些路口。你需要通过查询来推断出当前启用的真实巡逻方案，并在该方案下求解出最小覆盖问题。

你可以反复向我提出以下两类查询（每次仅限一个问题），我会根据真实设定如实回答：

1. 单一巡逻路线路口数查询：询问某条路线 Si 覆盖的路口数量。回答一个整数。
2. 路线组合路口总数查询：询问两条不同路线 Si 和 Sj 联合覆盖的去重路口总数。回答一个整数。

你的目标是：
1. 确定真实的巡逻方案标签（A、B、C 或 D）。
2. 求出在该方案下，覆盖全部 6 个拥堵路口所需的最少巡逻路线数量 k。
3. 给出一组达到该最少路线数量的路线索引集合。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，排班将失败。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单一巡逻路线路口数查询（例如询问 S3 的覆盖数）：
<query_size>3</query_size>

- 路线组合路口总数查询（例如询问 S1 和 S4 联合覆盖的路口总数）：
<query_union>1,4</query_union>

提交最终答案时，必须说明巡逻方案标签（A、B、C 或 D）、最小覆盖数量 k，以及一组路线索引集合（用逗号隔开，顺序不限），格式如下：

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The Intelligent Traffic Management System is running. There are 6 core congested intersections in the city's traffic network, denoted as the set U = {1,2,3,4,5,6}.
The Traffic Management Bureau has planned 5 routine patrol routes, indexed as S1, S2, S3, S4, S5.

The system has secretly deployed one of four patrol schemes (labeled A, B, C, or D), which maps each patrol route Si to a fixed subset of intersections in U. Your task is to infer the currently active patrol scheme through queries, and then solve the minimum covering problem under that scheme.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully based on the actual setting:

1. Single Route Coverage Query: Ask for the number of intersections covered by a specific route Si. Answer is an integer.
2. Combined Route Coverage Query: Ask for the total number of unique intersections covered by the union of two different routes Si and Sj. Answer is an integer.

Your goals are:
1. Determine the true patrol scheme label (A, B, C, or D).
2. Find the minimum number k of patrol routes needed to cover all 6 congested intersections under that scheme.
3. Provide one set of route indices that achieves this minimum coverage.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the scheduling fails.

Each query must contain only one tag. Use the following XML format:

- Single Route Coverage Query (e.g., asking for the coverage size of S3):
<query_size>3</query_size>

- Combined Route Coverage Query (e.g., asking for the combined coverage size of S1 and S4):
<query_union>1,4</query_union>

When submitting the final answer, specify the patrol scheme label (A, B, C, or D), minimum cover number k, and a set of route indices (comma-separated, order does not matter), using this format:

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    contextualized_rule_zh_2 = """\
临床决策支持系统已启动。面对一种复杂综合征，医学界确认了 6 种核心并发症，记为靶点集合 U = {1,2,3,4,5,6}。
药房储备了 5 种靶向药物，索引为 S1, S2, S3, S4, S5。

目前有四套已知的药物作用图谱（记为 A、B、C 或 D），该图谱将每种药物 Si 固定映射为 U 中其能有效控制的特定并发症子集。系统已秘密选定了符合当前病原体变异的真实作用图谱。你需要通过查询来推断出该图谱，并在该图谱下求解出最小药物覆盖问题。

你可以反复向我提出以下两类查询（每次仅限一个问题），我会根据真实设定如实回答：

1. 单药靶向数查询：询问某药物 Si 能控制的并发症数量。回答一个整数。
2. 双药联合靶向数查询：询问两种不同药物 Si 和 Sj 联合使用能控制的去重并发症总数。回答一个整数。

你的目标是：
1. 确定真实的药物作用图谱标签（A、B、C 或 D）。
2. 求出在该图谱下，控制所有 6 种并发症所需的最少药物数量 k。
3. 给出一组达到该最少药物数量的药物索引集合。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，处方将被驳回。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单药靶向数查询（例如询问 S3 的控制数量）：
<query_size>3</query_size>

- 双药联合靶向数查询（例如询问 S1 和 S4 联合控制的并发症总数）：
<query_union>1,4</query_union>

提交最终答案时，必须说明作用图谱标签（A、B、C 或 D）、最少药物数量 k，以及一组药物索引集合（用逗号隔开，顺序不限），格式如下：

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The Clinical Decision Support System is activated. Facing a complex syndrome, the medical community has identified 6 core complications, denoted as the target set U = {1,2,3,4,5,6}.
The pharmacy stocks 5 targeted drugs, indexed as S1, S2, S3, S4, S5.

There are four known drug efficacy profiles (labeled A, B, C, or D), which map each drug Si to a fixed subset of complications in U that it can effectively control. The system has secretly selected the true profile corresponding to the current pathogen mutation. Your task is to infer this profile through queries, and then solve the minimum drug coverage problem under that profile.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully based on the actual setting:

1. Single Drug Target Query: Ask for the number of complications a specific drug Si can control. Answer is an integer.
2. Drug Combination Target Query: Ask for the total number of unique complications controlled by the combination of two different drugs Si and Sj. Answer is an integer.

Your goals are:
1. Determine the true efficacy profile label (A, B, C, or D).
2. Find the minimum number k of drugs needed to control all 6 complications under that profile.
3. Provide one set of drug indices that achieves this minimum coverage.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the prescription will be rejected.

Each query must contain only one tag. Use the following XML format:

- Single Drug Target Query (e.g., asking for the control size of S3):
<query_size>3</query_size>

- Drug Combination Target Query (e.g., asking for the combined control size of S1 and S4):
<query_union>1,4</query_union>

When submitting the final answer, specify the efficacy profile label (A, B, C, or D), minimum cover number k, and a set of drug indices (comma-separated, order does not matter), using this format:

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    contextualized_rule_zh_3 = """\
学生综合素质评价系统已开启。教育局明确了 6 项学生必须具备的核心素养指标，记为集合 U = {1,2,3,4,5,6}。
学校教务处设计了 5 个综合实践活动，索引为 S1, S2, S3, S4, S5。

目前的教学大纲存在四套备选方案（记为 A、B、C 或 D），该方案将每个实践活动 Si 固定映射为 U 中其能有效培养的核心素养子集。系统已秘密选定了一套真实的教学大纲方案。你需要通过查询推断出当前方案，并在该方案下求解最少活动覆盖问题。

你可以反复向我提出以下两类查询（每次仅限一个问题），我会根据真实设定如实回答：

1. 单一活动素养数查询：询问某活动 Si 能培养的核心素养数量。回答一个整数。
2. 活动组合素养总数查询：询问两个不同活动 Si 和 Sj 组合后能培养的去重核心素养总数。回答一个整数。

你的目标是：
1. 确定真实的教学大纲方案标签（A、B、C 或 D）。
2. 求出在该方案下，全面覆盖所有 6 项核心素养所需的最少实践活动数量 k。
3. 给出一组达到该最少活动数量的活动索引集合。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，课程安排将无法通过审批。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单一活动素养数查询（例如询问 S3 培养的素养数）：
<query_size>3</query_size>

- 活动组合素养总数查询（例如询问 S1 和 S4 组合的素养总数）：
<query_union>1,4</query_union>

提交最终答案时，必须说明教学大纲方案标签（A、B、C 或 D）、最小覆盖数量 k，以及一组活动索引集合（用逗号隔开，顺序不限），格式如下：

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The Student Comprehensive Quality Assessment System is online. The Education Bureau has specified 6 core competency indicators that students must acquire, denoted as the set U = {1,2,3,4,5,6}.
The school's academic affairs office has designed 5 comprehensive practical activities, indexed as S1, S2, S3, S4, S5.

There are four alternative syllabus schemes (labeled A, B, C, or D) for the current curriculum, which map each activity Si to a fixed subset of core competencies in U that it can effectively cultivate. The system has secretly selected the true syllabus scheme. Your task is to infer the current scheme through queries, and then solve the minimum activity coverage problem under that scheme.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully based on the actual setting:

1. Single Activity Competency Query: Ask for the number of core competencies cultivated by a specific activity Si. Answer is an integer.
2. Combined Activity Competency Query: Ask for the total number of unique core competencies cultivated by the combination of two different activities Si and Sj. Answer is an integer.

Your goals are:
1. Determine the true syllabus scheme label (A, B, C, or D).
2. Find the minimum number k of practical activities needed to comprehensively cover all 6 core competencies under that scheme.
3. Provide one set of activity indices that achieves this minimum coverage.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the course scheduling will not be approved.

Each query must contain only one tag. Use the following XML format:

- Single Activity Competency Query (e.g., asking for the competency size of S3):
<query_size>3</query_size>

- Combined Activity Competency Query (e.g., asking for the combined competency size of S1 and S4):
<query_union>1,4</query_union>

When submitting the final answer, specify the syllabus scheme label (A, B, C, or D), minimum cover number k, and a set of activity indices (comma-separated, order does not matter), using this format:

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    contextualized_rule_zh_4 = """\
智能工厂质检规划系统已上线。在流水线生产中，定义了 6 个关键的质量检测环节，记为集合 U = {1,2,3,4,5,6}。
车间配置了 5 台多功能自动化检测设备，索引为 S1, S2, S3, S4, S5。

供应商提供了四套设备能力清单（记为 A、B、C 或 D），该清单将每台设备 Si 固定映射为 U 中其能独立覆盖的质检环节子集。系统已秘密加载了与当前产线匹配的真实设备清单。你需要通过查询推断出当前的清单标签，并在该清单下求解最少设备覆盖问题。

你可以反复向我提出以下两类查询（每次仅限一个问题），我会根据真实设定如实回答：

1. 单设备覆盖环节数查询：询问某台设备 Si 能完成的质检环节数量。回答一个整数。
2. 双设备联合覆盖环节数查询：询问两台不同设备 Si 和 Sj 联合后能完成的去重质检环节总数。回答一个整数。

你的目标是：
1. 确定真实的设备能力清单标签（A、B、C 或 D）。
2. 求出在该清单下，完整覆盖所有 6 个质检环节所需的最少设备数量 k。
3. 给出一组达到该最少设备数量的设备索引集合。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，产线配置将判定为不合格。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单设备覆盖环节数查询（例如询问 S3 的覆盖数）：
<query_size>3</query_size>

- 双设备联合覆盖环节数查询（例如询问 S1 和 S4 联合覆盖的总数）：
<query_union>1,4</query_union>

提交最终答案时，必须说明设备清单标签（A、B、C 或 D）、最少设备数量 k，以及一组设备索引集合（用逗号隔开，顺序不限），格式如下：

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
The Smart Factory Quality Inspection Planning System is online. In assembly line production, 6 critical quality inspection stages have been defined, denoted as the set U = {1,2,3,4,5,6}.
The workshop is equipped with 5 multi-functional automated inspection devices, indexed as S1, S2, S3, S4, S5.

Suppliers have provided four sets of device capability inventories (labeled A, B, C, or D), which map each device Si to a fixed subset of inspection stages in U that it can independently cover. The system has secretly loaded the true device inventory matching the current production line. Your task is to infer the current inventory label through queries, and then solve the minimum device coverage problem under that inventory.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully based on the actual setting:

1. Single Device Coverage Query: Ask for the number of inspection stages a specific device Si can complete. Answer is an integer.
2. Dual Device Combined Coverage Query: Ask for the total number of unique inspection stages completed by the combination of two different devices Si and Sj. Answer is an integer.

Your goals are:
1. Determine the true device capability inventory label (A, B, C, or D).
2. Find the minimum number k of devices needed to fully cover all 6 inspection stages under that inventory.
3. Provide one set of device indices that achieves this minimum coverage.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the production line configuration will be deemed unqualified.

Each query must contain only one tag. Use the following XML format:

- Single Device Coverage Query (e.g., asking for the coverage size of S3):
<query_size>3</query_size>

- Dual Device Combined Coverage Query (e.g., asking for the combined coverage size of S1 and S4):
<query_union>1,4</query_union>

When submitting the final answer, specify the device inventory label (A, B, C, or D), minimum cover number k, and a set of device indices (comma-separated, order does not matter), using this format:

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    contextualized_rule_zh_5 = """\
智能庭审辅助系统已启动。在一起复杂的商业诉讼中，法院归纳了 6 个关键的争议焦点，记为集合 U = {1,2,3,4,5,6}。
律师团队精心准备了 5 组核心证据链，索引为 S1, S2, S3, S4, S5。

根据不同的案情推演，存在四种可能的庭审策略（记为 A、B、C 或 D），该策略将每组证据链 Si 固定映射为 U 中其能形成有效证明的争议焦点子集。系统已秘密锁定了对方律师实际采用的真实策略。你需要通过查询来推断出该庭审策略，并在该策略下求解最少证据链覆盖问题。

你可以反复向我提出以下两类查询（每次仅限一个问题），我会根据真实设定如实回答：

1. 单证据链证明数查询：询问某组证据链 Si 能覆盖的争议焦点数量。回答一个整数。
2. 联合证据链证明总数查询：询问两组不同证据链 Si 和 Sj 联合后能覆盖的去重争议焦点总数。回答一个整数。

你的目标是：
1. 确定真实的庭审策略标签（A、B、C 或 D）。
2. 求出在该策略下，完成全案 6 个争议焦点举证所需的最少证据链数量 k。
3. 给出一组达到该最少证据链数量的证据链索引集合。

当你收集足够信息后，请提交最终答案。若答案错误或格式不符，法庭将驳回你的诉讼请求。

每次询问只能包含一个标签。请使用以下 XML 格式：

- 单证据链证明数查询（例如询问 S3 覆盖的焦点数）：
<query_size>3</query_size>

- 联合证据链证明总数查询（例如询问 S1 和 S4 联合覆盖的焦点总数）：
<query_union>1,4</query_union>

提交最终答案时，必须说明庭审策略标签（A、B、C 或 D）、最小覆盖数量 k，以及一组证据链索引集合（用逗号隔开，顺序不限），格式如下：

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The Intelligent Trial Assistance System is activated. In a complex commercial lawsuit, the court has summarized 6 key focal points of dispute, denoted as the set U = {1,2,3,4,5,6}.
The legal team has carefully prepared 5 core chains of evidence, indexed as S1, S2, S3, S4, S5.

Based on different case deductions, there are four possible trial strategies (labeled A, B, C, or D), which map each evidence chain Si to a fixed subset of focal points in U that it can effectively prove. The system has secretly locked onto the true strategy actually adopted by the opposing counsel. Your task is to infer this trial strategy through queries, and then solve the minimum evidence chain coverage problem under that strategy.

You can repeatedly ask me two types of questions (one per turn), and I will answer truthfully based on the actual setting:

1. Single Evidence Chain Proof Query: Ask for the number of focal points covered by a specific evidence chain Si. Answer is an integer.
2. Combined Evidence Chain Proof Query: Ask for the total number of unique focal points covered by the union of two different evidence chains Si and Sj. Answer is an integer.

Your goals are:
1. Determine the true trial strategy label (A, B, C, or D).
2. Find the minimum number k of evidence chains needed to complete the burden of proof for all 6 focal points under that strategy.
3. Provide one set of evidence chain indices that achieves this minimum coverage.

When you have enough information, submit your final answer. If the answer is wrong or the format is invalid, the court will dismiss your litigation claims.

Each query must contain only one tag. Use the following XML format:

- Single Evidence Chain Proof Query (e.g., asking for the coverage size of S3):
<query_size>3</query_size>

- Combined Evidence Chain Proof Query (e.g., asking for the combined coverage size of S1 and S4):
<query_union>1,4</query_union>

When submitting the final answer, specify the trial strategy label (A, B, C, or D), minimum cover number k, and a set of evidence chain indices (comma-separated, order does not matter), using this format:

<answer>family=A, min_cover=3, indices=1,3,4</answer>
"""

    tags = ["answer", "query_size", "query_union"]

    FAMILIES = {
        "A": {
            "S1": {1, 2, 3},
            "S2": {3, 4},
            "S3": {1, 4, 5},
            "S4": {2, 5, 6},
            "S5": {6},
        },
        "B": {
            "S1": {1, 2, 6},
            "S2": {3, 4},
            "S3": {1, 3, 5},
            "S4": {2, 5},
            "S5": {6},
        },
        "C": {
            "S1": {1, 2, 6},
            "S2": {3, 4, 5},
            "S3": {1, 3},
            "S4": {2, 5},
            "S5": {6},
        },
        "D": {
            "S1": {1, 2, 3},
            "S2": {1, 4, 5},
            "S3": {4, 6},
            "S4": {2, 5, 6},
            "S5": {3},
        },
    }

    DIFFICULTY_CONFIG = {
        1: {"family": "A", "min_cover": 3, "valid_covers": [{1, 2, 4}, {1, 3, 4}]},
        2: {"family": "B", "min_cover": 3, "valid_covers": [{1, 2, 4}, {1, 2, 3}]},
        3: {"family": "C", "min_cover": 3, "valid_covers": [{1, 2, 3}, {1, 2, 4}]},
        4: {"family": "D", "min_cover": 3, "valid_covers": [{1, 2, 3}, {1, 3, 4}, {1, 2, 4}]},
        5: {"family": "A", "min_cover": 3, "valid_covers": [{1, 2, 4}, {1, 3, 4}, {2, 3, 4}]},
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        diff = int(self.config.difficulty)
        if diff not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported difficulty: {diff}")
        
        cfg = self.DIFFICULTY_CONFIG[diff]
        self.true_family_label = cfg["family"]
        self.min_cover_count = cfg["min_cover"]
        self.valid_cover_sets = cfg["valid_covers"]
        
        self.true_family = self.FAMILIES[self.true_family_label]
        self.universe = {1, 2, 3, 4, 5, 6}
        self._game_info = {}

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"]
        
        family_match = re.search(r'family\s*=\s*([A-D])', raw_ans)
        min_cover_match = re.search(r'min_cover\s*=\s*(\d+)', raw_ans)
        indices_match = re.search(r'indices\s*=\s*([\d,\s]+)', raw_ans)
        
        if not family_match or not min_cover_match or not indices_match:
            return False
        
        if family_match.group(1) != self.true_family_label:
            return False
        
        try:
            submitted_k = int(min_cover_match.group(1))
        except:
            return False
        
        if submitted_k != self.min_cover_count:
            return False
        
        try:
            indices_str = indices_match.group(1).strip()
            if not indices_str:
                return False
            submitted_indices = set(int(x.strip()) for x in indices_str.split(",") if x.strip())
        except:
            return False
        
        if len(submitted_indices) != submitted_k:
            return False
        
        if not all(1 <= i <= 5 for i in submitted_indices):
            return False
        
        union = set()
        for i in submitted_indices:
            subset_key = f"S{i}"
            union = union.union(self.true_family[subset_key])
        
        if union != self.universe:
            return False
        
        return True

    def _cf_core_produce(self, parsed_info):
        if "query_size" in parsed_info:
            try:
                idx = int(parsed_info["query_size"].strip())
                if not (1 <= idx <= 5):
                    if self.config.language == "zh":
                        return "错误：索引必须在 1 到 5 之间。"
                    else:
                        return "Error: Index must be between 1 and 5."
                
                subset_key = f"S{idx}"
                size = len(self.true_family[subset_key])
                return str(size)
            except:
                if self.config.language == "zh":
                    return "错误：无效的查询格式。"
                else:
                    return "Error: Invalid query format."
        
        elif "query_union" in parsed_info:
            try:
                raw = parsed_info["query_union"].strip()
                parts = [x.strip() for x in raw.split(",")]
                if len(parts) != 2:
                    raise ValueError
                
                i, j = int(parts[0]), int(parts[1])
                
                if not (1 <= i <= 5 and 1 <= j <= 5):
                    raise ValueError
                
                if i == j:
                    if self.config.language == "zh":
                        return "错误：两个索引必须不同。"
                    else:
                        return "Error: The two indices must be different."
                
                subset_i = self.true_family[f"S{i}"]
                subset_j = self.true_family[f"S{j}"]
                union_size = len(subset_i.union(subset_j))
                return str(union_size)
            except:
                if self.config.language == "zh":
                    return "错误：无效的查询格式或索引超出范围。"
                else:
                    return "Error: Invalid query format or index out of range."
        
        else:
            raise ValueError("No valid query tag found.")

    def _cf_make_wrong(self, correct: str) -> str:
        if correct.isdigit():
            return str(int(correct) + 1)
        
        if self.config.language == "zh":
            if "是" in correct:
                return correct.replace("是", "否")
            elif "否" in correct:
                return correct.replace("否", "是")
        else:
            if "Yes" in correct:
                return correct.replace("Yes", "No")
            elif "No" in correct:
                return correct.replace("No", "Yes")
            elif "yes" in correct:
                return correct.replace("yes", "no")
            elif "no" in correct:
                return correct.replace("no", "yes")
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        for i in range(1, 6):
            subset_key = f"S{i}"
            size = len(self.true_family[subset_key])
            queries.append({
                "query": f"<query_size>{i}</query_size>",
                "answer": str(size)
            })

        for i in range(1, 6):
            for j in range(i + 1, 6):
                subset_i = self.true_family[f"S{i}"]
                subset_j = self.true_family[f"S{j}"]
                union_size = len(subset_i.union(subset_j))
                queries.append({
                    "query": f"<query_union>{i},{j}</query_union>",
                    "answer": str(union_size)
                })
                
        return queries