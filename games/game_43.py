# -*- coding: utf-8 -*-
# 自动生成 | 模型: api/gpt-5-2025-08-07
# 推理类型: 演绎推理（明确的规则系统）：从游戏既定规则和已知线索，推导出必定的事实。
# 数据结构: 序列：存在一个长度为N的有序序列。
# 知识点:   元素排名：某元素在排序后处于第几位
# ============================================================

from .base import Game
import random
import re
import itertools

class RankDeterminationGame(Game):

    game_rule_zh = """\
我们现在来玩一个"秩确定"的推理游戏，规则如下：

游戏设定了一个包含 {n} 个不同元素的集合 E，这些元素为 {elements}。在这个集合上存在一个隐藏但固定的严格全序关系（即任意两个不同元素都可以比较大小，没有并列，且关系具有传递性）。

我已经选定了一个目标元素 t = {target}。你的任务是确定这个目标元素在该全序关系中的秩 rank(t)。

秩的定义：对于元素 x，其秩 rank(x) 等于 1 加上小于 x 的元素个数。即最小的元素秩为 1，第二小的元素秩为 2，以此类推，最大的元素秩为 {n}。

你可以反复向我提出比较问题：询问集合中任意两个不同元素的相对顺序（即哪个元素在全序中更靠前）。我会根据隐藏的全序关系如实回答。

注意：
- 你不能直接询问目标元素的秩或等价问题（如"有多少元素小于目标元素"）
- 每次只能比较两个元素
- 请尽可能用最少的比较次数确定答案

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如询问元素 e1 和 e3 的相对顺序）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明目标元素的秩（一个 1 到 {n} 之间的整数），格式如下：

<answer>5</answer>

表示你认为目标元素 {target} 的秩为 5。
"""

    game_rule_en = """\
Let's play a "Rank Determination" reasoning game. Here are the rules:

The game defines a set E containing {n} distinct elements: {elements}. There exists a hidden but fixed strict total order on this set (meaning any two different elements can be compared, with no ties, and the relation is transitive).

I have selected a target element t = {target}. Your task is to determine the rank of this target element in the total order, denoted as rank(t).

Definition of rank: For an element x, its rank rank(x) equals 1 plus the number of elements smaller than x. That is, the smallest element has rank 1, the second smallest has rank 2, and so on, with the largest element having rank {n}.

You can repeatedly ask me comparison questions: inquire about the relative order of any two different elements in the set (i.e., which element comes first in the total order). I will answer truthfully based on the hidden total order.

Note:
- You cannot directly ask for the target element's rank or equivalent questions (such as "how many elements are smaller than the target")
- Each query can only compare two elements
- Try to determine the answer with as few comparisons as possible

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about the relative order of e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rank of the target element (an integer between 1 and {n}), using this format:

<answer>5</answer>

This means you believe the target element {target} has rank 5.
"""

    # 场景 1：交通
    contextualized_rule_zh_1 = """\
欢迎使用智能交通调度系统。在当前的调度批次中，包含 {n} 个待处理的通行任务（如车辆或信号），记为集合 E = {elements}。为了保障路网顺畅，系统内部已按照紧急程度和路线规划生成了一个严格的通行优先级序列（不存在并列，具有传递性）。

我已锁定了一个目标通行任务 t = {target}。你的任务是通过对比查询，确定该任务在总调度序列中的绝对通行位次 rank(t)。

位次的定义：通行优先级最高（最先通行）的任务位次为 1，其次为 2，以此类推，最后通行的任务位次为 {n}。这等同于 1 加上所有优先级高于该任务的数量。

你可以反复向我提出比对请求：每次指定两个不同的任务，系统将返回哪个任务应当优先通行（即在全序中更靠前）。

注意：
- 你不能直接查询目标任务的绝对位次或等价问题（如“有多少任务优先于目标任务”）
- 每次只能比对两个任务
- 请尽量用最少的比对次数确定目标任务的最终位次

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如询问任务 e1 和 e3 的优先顺序）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明目标任务的位次（一个 1 到 {n} 之间的整数），格式如下：

<answer>5</answer>

表示你认为目标任务 {target} 的绝对通行位次为 5。
"""

    contextualized_rule_en_1 = """\
[Transportation Scenario]
Welcome to the Intelligent Traffic Dispatch System. In the current dispatch batch, there are {n} pending traffic tasks (such as vehicles or signals), denoted as set E = {elements}. To ensure road network efficiency, the system has internally generated a strict traffic priority sequence based on urgency and route planning (with no ties, and the relation is transitive).

I have locked onto a target traffic task t = {target}. Your task is to determine the absolute dispatch rank of this task in the overall sequence, denoted as rank(t).

Definition of rank: The task with the highest priority (dispatched first) has rank 1, the second has rank 2, and so on, with the last task having rank {n}. This equals 1 plus the number of tasks with higher priority than the target.

You can repeatedly submit comparison requests: specify any two different tasks, and the system will return which task should be dispatched first (i.e., comes first in the total order).

Note:
- You cannot directly ask for the target task's rank or equivalent questions (such as "how many tasks have higher priority than the target")
- Each query can only compare two tasks
- Try to determine the answer with as few comparisons as possible

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about the priority order of task e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rank of the target task (an integer between 1 and {n}), using this format:

<answer>5</answer>

This means you believe the target task {target} has rank 5.
"""

    # 场景 2：医疗
    contextualized_rule_zh_2 = """\
欢迎进入急诊分诊排班系统。当前有 {n} 位待处理的急诊患者或医疗任务，集合为 E = {elements}。基于患者的生命体征和病情危重程度，医疗系统已生成了一个隐蔽但固定的严格优先就诊序列（绝无并列，严格遵守传递性）。

系统指派给你的重点关注对象是 t = {target}。你的任务是推断出该患者/任务在全院急诊序列中的确切就诊顺位 rank(t)。

顺位的定义：最先就诊的顺位为 1，第二名顺位为 2，以此类推，最后就诊的为 {n}。即 1 加上排在该对象之前的总人数。

你可以反复调用分诊比对接口：输入任意两个不同的对象，系统会根据医疗规范如实反馈哪一位优先级更高（更早排期）。

注意：
- 你不能直接查询目标对象的绝对顺位或等价问题（如“有多少患者排在目标之前”）
- 每次只能比对两个对象
- 请尽量用最少的比对次数确定目标对象的最终顺位

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如询问对象 e1 和 e3 的就诊先后）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明目标对象的顺位（一个 1 到 {n} 之间的整数），格式如下：

<answer>5</answer>

表示你认为目标对象 {target} 的确切就诊顺位为 5。
"""

    contextualized_rule_en_2 = """\
[Healthcare Scenario]
Welcome to the Emergency Triage and Scheduling System. There are currently {n} pending emergency patients or medical tasks, forming the set E = {elements}. Based on vital signs and critical condition severity, the system has generated a hidden but fixed strict priority treatment sequence (with no ties, strictly adhering to transitivity).

The system has assigned you a key target object t = {target}. Your task is to deduce the exact treatment rank of this patient/task in the overall hospital emergency sequence, denoted as rank(t).

Definition of rank: The object treated first has rank 1, the second has rank 2, and so on, with the last being {n}. This equals 1 plus the total number of individuals queued before the target object.

You can repeatedly invoke the triage comparison interface: input any two distinct objects, and the system will truthfully return which one has higher priority (scheduled earlier) according to medical protocols.

Note:
- You cannot directly ask for the target object's rank or equivalent questions (such as "how many patients are ahead of the target")
- Each query can only compare two objects
- Try to determine the answer with as few comparisons as possible

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about the treatment order of e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rank of the target object (an integer between 1 and {n}), using this format:

<answer>5</answer>

This means you believe the target object {target} has treatment rank 5.
"""

    # 场景 3：教育
    contextualized_rule_zh_3 = """\
欢迎使用综合学情评价与录取排位系统。本批次共有 {n} 名候选学生，名单集合 E = {elements}。系统根据多维度的综合考核成绩，已生成了一份严格的全序排名榜单（不存在同分并列情况，排名逻辑具有传递性）。

当前需要进行复核的目标学生是 t = {target}。你需要通过两两比对，准确确定该名学生在榜单上的最终名次 rank(t)。

名次的定义：排名最高（最优秀）的学生名次为 1，次之为 2，以此类推，最后的学生名次为 {n}。名次数值等于 1 加上成绩优于该名学生的总人数。

你可以反复向系统提出比较申请：询问任意两名不同学生的相对成绩高低（即谁的排名更靠前）。

注意：
- 你不能直接查询目标学生的绝对名次或等价问题（如“有多少学生名次高于目标学生”）
- 每次只能比对两名学生
- 请尽量用最少的比对次数确定目标学生的最终名次

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如询问学生 e1 和 e3 的成绩排名相对高低）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明目标学生的名次（一个 1 到 {n} 之间的整数），格式如下：

<answer>5</answer>

表示你认为目标学生 {target} 的最终名次为 5。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
Welcome to the Comprehensive Academic Evaluation and Admission Ranking System. There are {n} candidates in the current batch, forming the set E = {elements}. Based on multi-dimensional comprehensive assessments, the system has generated a strict total ranking list (with no ties or equal scores, and the ranking logic is transitive).

The target student currently under review is t = {target}. Your task is to accurately determine the final rank of this student on the list, denoted as rank(t), through pairwise comparisons.

Definition of rank: The highest-ranked (most excellent) student has rank 1, the second has rank 2, and so on, with the last student having rank {n}. The rank value equals 1 plus the total number of students with better performance than the target student.

You can repeatedly submit comparison requests to the system: inquire about the relative academic standing of any two different students (i.e., who ranks higher).

Note:
- You cannot directly ask for the target student's rank or equivalent questions (such as "how many students rank higher than the target")
- Each query can only compare two students
- Try to determine the answer with as few comparisons as possible

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about the relative ranking of students e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rank of the target student (an integer between 1 and {n}), using this format:

<answer>5</answer>

This means you believe the target student {target} has rank 5.
"""

    # 场景 4：制造业/工业
    contextualized_rule_zh_4 = """\
欢迎接入智能工厂生产流控系统。当前产线面临 {n} 个待排期的生产工单或设备维护任务，集合 E = {elements}。为最大化产能，排程引擎已计算出一条严格的流水线加工执行序列（无并发，严格按先后顺序执行，具有传递性）。

系统要求你定位关键工单 t = {target}。你的职责是查明该工单在全局执行序列中的确切流水号 rank(t)。

流水号的定义：第一个上机加工的工单流水号为 1，第二个为 2，以此类推，最后一个为 {n}。它等于 1 加上在该工单之前完成的工单总数。

你可以反复发起排程比对查询：输入两个不同工单，系统会读取引擎数据并返回哪个工单被安排在更前面加工。

注意：
- 你不能直接查询目标工单的绝对流水号或等价问题（如“有多少工单排在目标之前”）
- 每次只能比对两个工单
- 请尽量用最少的比对次数确定目标工单的最终流水号

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如询问工单 e1 和 e3 的加工先后顺序）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明目标工单的流水号（一个 1 到 {n} 之间的整数），格式如下：

<answer>5</answer>

表示你认为目标工单 {target} 的确切流水号为 5。
"""

    contextualized_rule_en_4 = """\
[Manufacturing Scenario]
Welcome to the Smart Factory Production Flow Control System. The production line currently faces {n} pending production orders or equipment maintenance tasks, forming the set E = {elements}. To maximize capacity, the scheduling engine has calculated a strict pipeline execution sequence (no concurrency, strictly sequential, and transitive).

The system requires you to locate a critical production order t = {target}. Your responsibility is to determine the exact execution rank of this order in the global sequence, denoted as rank(t).

Definition of rank: The first order to be processed on the machine has rank 1, the second has rank 2, and so on, with the last having rank {n}. It equals 1 plus the total number of orders completed before this target order.

You can repeatedly initiate scheduling comparison queries: input two distinct orders, and the system will read the engine data to return which order is scheduled to be processed first.

Note:
- You cannot directly ask for the target order's execution rank or equivalent questions (such as "how many orders are scheduled before the target")
- Each query can only compare two orders
- Try to determine the answer with as few comparisons as possible

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about the processing sequence of order e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the execution rank of the target order (an integer between 1 and {n}), using this format:

<answer>5</answer>

This means you believe the target order {target} has execution rank 5.
"""

    # 场景 5：法律
    contextualized_rule_zh_5 = """\
欢迎使用破产清算与债权优先级审查系统。本案共涉及 {n} 项独立债权或法律诉求，案卷集合 E = {elements}。根据相关法律法规的清偿顺序，法院已对这些诉求确立了一个严格的法定优先权序列（不存在同一顺位，具有法理上的传递性）。

目前法庭要求对特定债权 t = {target} 进行审查。你需要通过法律顺位比对，确定该债权在总体清偿序列中的绝对法定顺位 rank(t)。

顺位的定义：最先获得清偿的绝对顺位为 1，其次为 2，以此类推，最后清偿的顺位为 {n}。顺位值等于 1 加上优先于该债权受偿的诉求数量。

你可以向卷宗系统申请判例比对：提供任意两项不同的债权，系统将依据法定顺位反馈哪一项具有更高的清偿优先权（排在更前）。

注意：
- 你不能直接查询目标债权的绝对法定顺位或等价问题（如“有多少债权优先于该目标”）
- 每次只能比对两项债权
- 请尽量用最少的比对次数确定目标债权的最终顺位

## 询问与提交答案的格式（必须严格遵守）

每次询问只能包含一个标签。请使用以下 XML 格式：

- 比较查询（例如询问债权 e1 和 e3 的优先受偿顺序）：
<query_compare>e1,e3</query_compare>

提交最终答案时，必须说明目标债权的顺位（一个 1 到 {n} 之间的整数），格式如下：

<answer>5</answer>

表示你认为目标债权 {target} 的绝对法定顺位为 5。
"""

    contextualized_rule_en_5 = """\
[Law Scenario]
Welcome to the Bankruptcy Liquidation and Creditor Priority Review System. This case involves a total of {n} independent legal claims or creditor rights, denoted as case file set E = {elements}. In accordance with the settlement order prescribed by relevant laws and regulations, the court has established a strict statutory priority sequence for these claims (with no tied ranks, holding jurisprudential transitivity).

The court currently requires a review of a specific legal claim t = {target}. Your task is to determine the absolute legal precedence rank of this claim in the overall settlement sequence, denoted as rank(t), through priority comparisons.

Definition of rank: The absolute rank to receive settlement first is 1, the second is 2, and so on, with the final settlement rank being {n}. The rank value equals 1 plus the number of claims that have priority over the target claim.

You can apply for precedent comparison from the case file system: provide any two different claims, and the system will return which one has higher settlement priority (comes first) based on statutory ranking.

Note:
- You cannot directly ask for the target claim's absolute legal precedence rank or equivalent questions (such as "how many claims have priority over the target")
- Each query can only compare two claims
- Try to determine the answer with as few comparisons as possible

## Query and Answer Format (strictly required)

Each query must contain only one tag. Use the following XML format:

- Comparison Query (e.g., asking about the settlement priority order of claim e1 and e3):
<query_compare>e1,e3</query_compare>

When submitting the final answer, specify the rank of the target claim (an integer between 1 and {n}), using this format:

<answer>5</answer>

This means you believe the target claim {target} has a legal precedence rank of 5.
"""

    tags = ["answer", "query_compare"]
    
    # 新增类属性
    reasoning_type = "演绎推理"
    data_structure = "序列"

    # 难度配置：
    # 1 (简单)       - N=5, 目标在中间或边界
    # 2 (中等偏下)   - N=7, 目标稍偏中间
    # 3 (中等偏上)   - N=10, 目标需要更多推理
    # 4 (较难)       - N=15, 较大规模
    # 5 (难)         - N=20, 大规模需要优化策略

    DIFFICULTY_CONFIG = {
        "zh": {
            1: {
                "n": 5,
                "elements": ["e1", "e2", "e3", "e4", "e5"],
                "order": ["e2", "e4", "e1", "e5", "e3"],  # e2<e4<e1<e5<e3
                "target": "e1",  # rank=3
            },
            2: {
                "n": 7,
                "elements": ["e1", "e2", "e3", "e4", "e5", "e6", "e7"],
                "order": ["e3", "e1", "e5", "e7", "e2", "e4", "e6"],  # e3<e1<e5<e7<e2<e4<e6
                "target": "e7",  # rank=4
            },
            3: {
                "n": 10,
                "elements": ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10"],
                "order": ["e5", "e2", "e8", "e1", "e9", "e4", "e7", "e3", "e10", "e6"],
                "target": "e4",  # rank=6
            },
            4: {
                "n": 15,
                "elements": ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", "e11", "e12", "e13", "e14", "e15"],
                "order": ["e7", "e3", "e11", "e1", "e14", "e5", "e9", "e13", "e2", "e8", "e15", "e4", "e10", "e6", "e12"],
                "target": "e8",  # rank=10
            },
            5: {
                "n": 20,
                "elements": ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", 
                           "e11", "e12", "e13", "e14", "e15", "e16", "e17", "e18", "e19", "e20"],
                "order": ["e9", "e15", "e3", "e17", "e7", "e12", "e1", "e19", "e5", "e14", 
                         "e11", "e8", "e20", "e4", "e16", "e2", "e13", "e6", "e10", "e18"],
                "target": "e11",  # rank=11
            },
        },
        "en": {
            1: {
                "n": 5,
                "elements": ["e1", "e2", "e3", "e4", "e5"],
                "order": ["e2", "e4", "e1", "e5", "e3"],
                "target": "e1",  # rank=3
            },
            2: {
                "n": 7,
                "elements": ["e1", "e2", "e3", "e4", "e5", "e6", "e7"],
                "order": ["e3", "e1", "e5", "e7", "e2", "e4", "e6"],
                "target": "e7",  # rank=4
            },
            3: {
                "n": 10,
                "elements": ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10"],
                "order": ["e5", "e2", "e8", "e1", "e9", "e4", "e7", "e3", "e10", "e6"],
                "target": "e4",  # rank=6
            },
            4: {
                "n": 15,
                "elements": ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", "e11", "e12", "e13", "e14", "e15"],
                "order": ["e7", "e3", "e11", "e1", "e14", "e5", "e9", "e13", "e2", "e8", "e15", "e4", "e10", "e6", "e12"],
                "target": "e8",  # rank=10
            },
            5: {
                "n": 20,
                "elements": ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", 
                           "e11", "e12", "e13", "e14", "e15", "e16", "e17", "e18", "e19", "e20"],
                "order": ["e9", "e15", "e3", "e17", "e7", "e12", "e1", "e19", "e5", "e14", 
                         "e11", "e8", "e20", "e4", "e16", "e2", "e13", "e6", "e10", "e18"],
                "target": "e11",  # rank=11
            },
        },
    }

    def __init__(self, config):
        # 初始化比较计数器
        self.comparison_count = 0
        super().__init__(config)

    def _initialize_game(self):
        """初始化游戏：加载难度配置，构建全序关系"""
        lang = self.config.language
        diff = self.config.difficulty
        
        # 确保 difficulty 为整数类型
        if isinstance(diff, str):
            diff = int(diff)

        if lang not in self.DIFFICULTY_CONFIG:
            raise KeyError(f"Unsupported language: {lang}")
        if diff not in self.DIFFICULTY_CONFIG[lang]:
            raise KeyError(f"Unsupported difficulty: {diff}")

        cfg = self.DIFFICULTY_CONFIG[lang][diff]
        
        # 设置游戏信息（用于填充规则模板）
        self._game_info["n"] = cfg["n"]
        self._game_info["elements"] = ", ".join(cfg["elements"])
        self._game_info["target"] = cfg["target"]
        
        # 保存元素集合
        self.elements = set(cfg["elements"])
        
        # 保存目标元素
        self.target = cfg["target"]
        
        # 构建全序关系：建立元素到位置的映射
        self.order = cfg["order"]  # 从小到大的完整排序
        self.rank_map = {elem: idx + 1 for idx, elem in enumerate(self.order)}
        
        # 计算目标元素的真实秩
        self.true_rank = self.rank_map[self.target]

    def evaluate(self, parsed_info):
        """评估模型提交的答案是否正确"""

        # 解析答案
        try:
            answer = int(parsed_info["answer"].strip())
        except:
            return False
        
        # 检查答案是否在有效范围内
        if answer < 1 or answer > self._game_info["n"]:
            return False
        
        # 判断是否与真实秩相等
        return answer == self.true_rank

    def _cf_core_produce(self, parsed_info):
        """核心业务逻辑处理查询，返回比较结果"""
        if "query_compare" not in parsed_info:
            if self.config.language == "zh":
                raise ValueError("无效的查询标签。")
            else:
                raise ValueError("Invalid query tag.")
        
        # 解析比较查询
        try:
            raw = parsed_info["query_compare"]
            parts = [x.strip() for x in raw.split(",")]
            if len(parts) != 2:
                raise ValueError("Invalid format")
            elem1, elem2 = parts
            
            # 检查元素是否在集合中
            if elem1 not in self.elements or elem2 not in self.elements:
                if self.config.language == "zh":
                    return "错误：元素不在集合中。"
                else:
                    return "Error: Element not in set."
            
            # 检查是否是相同元素
            if elem1 == elem2:
                if self.config.language == "zh":
                    return "错误：不能比较相同的元素。"
                else:
                    return "Error: Cannot compare identical elements."
            
            # 增加比较计数
            self.comparison_count += 1
            
            # 根据全序关系返回比较结果
            rank1 = self.rank_map[elem1]
            rank2 = self.rank_map[elem2]
            
            if self.config.language == "zh":
                if rank1 < rank2:
                    return f"{elem1} 在全序中位于 {elem2} 之前。"
                else:
                    return f"{elem2} 在全序中位于 {elem1} 之前。"
            else:
                if rank1 < rank2:
                    return f"{elem1} comes before {elem2} in the total order."
                else:
                    return f"{elem2} comes before {elem1} in the total order."
                    
        except Exception as e:
            if self.config.language == "zh":
                return "错误：查询格式无效。请使用格式 <query_compare>e1,e2</query_compare>"
            else:
                return "Error: Invalid query format. Please use format <query_compare>e1,e2</query_compare>"

    def _cf_make_wrong(self, correct: str) -> str:
        """生成错误答案：反转比较结果中的顺序"""
        # 尝试匹配英文格式: "X comes before Y in the total order."
        en_match = re.match(r'^(\S+) comes before (\S+) in the total order\.$', correct)
        if en_match:
            e1, e2 = en_match.group(1), en_match.group(2)
            return f"{e2} comes before {e1} in the total order."
        
        # 尝试匹配中文格式: "X 在全序中位于 Y 之前。"
        zh_match = re.match(r'^(\S+) 在全序中位于 (\S+) 之前。$', correct)
        if zh_match:
            e1, e2 = zh_match.group(1), zh_match.group(2)
            return f"{e2} 在全序中位于 {e1} 之前。"
        
        # 兜底：如果是错误提示信息等，直接追加标记
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        """
        枚举所有合法查询并返回对应的正确答案。
        使用组合而非排列，避免冗余的互补查询。

        Returns:
            list of dict, 每项格式：
            {
                "query" : str,   # 合法的 XML 标签字符串
                "answer": str,   # 调用游戏逻辑后得到的正确答案字符串
            }
        """
        queries = []
        sorted_elements = sorted(list(self.elements))
        
        for e1, e2 in itertools.combinations(sorted_elements, 2):
            query_str = f"<query_compare>{e1},{e2}</query_compare>"
            
            rank1 = self.rank_map[e1]
            rank2 = self.rank_map[e2]
            
            answer = ""
            if self.config.language == "zh":
                if rank1 < rank2:
                    answer = f"{e1} 在全序中位于 {e2} 之前。"
                else:
                    answer = f"{e2} 在全序中位于 {e1} 之前。"
            else:
                if rank1 < rank2:
                    answer = f"{e1} comes before {e2} in the total order."
                else:
                    answer = f"{e2} comes before {e1} in the total order."
            
            queries.append({
                "query": query_str,
                "answer": answer
            })
            
        return queries