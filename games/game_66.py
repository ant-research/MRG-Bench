from .base import Game
import random
import re

class CircularOrderRankingGame(Game):

    game_rule_zh = """\
我们来玩一个"循环顺序推理"游戏，规则如下：

游戏设定了一个正整数 N = {n}，以及一个目标元素 T = {target}。所有元素的取值范围均为 {{0, 1, ..., N-1}}。

在这 N 个元素上存在一个隐藏的全局线性顺序，该顺序由某个未知的偏移量决定。你的目标是推断出目标元素 T 在该全局顺序中的名次（名次从 1 到 N）。

你可以通过以下两种方式向我提问，我会根据隐藏的全局顺序如实回答：

1. **集合排序询问**：给出 2 到 6 个不同的元素，我会告诉你这些元素在全局顺序中的排列顺序。
   - 格式：<query_order>a1,a2,...,ak</query_order>
   - 约束：元素个数 k 在 2 到 6 之间；所有元素互不相同且在 [0, N-1] 范围内
   - 返回：这些元素按全局顺序排列的结果

2. **成对比较询问**：询问两个元素谁在全局顺序中更靠前。
   - 格式：<query_compare>a,b</query_compare>
   - 约束：a 和 b 不同，且均在 [0, N-1] 范围内
   - 返回：a-before-b 或 b-before-a

请尽可能少地提问。当你确定答案后，请提交目标元素的名次。

每次提问只能包含一个标签。

- 集合排序询问（例如询问元素 0, 3, 5 的顺序）：
<query_order>0,3,5</query_order>

- 成对比较询问（例如比较元素 1 和 4）：
<query_compare>1,4</query_compare>

提交最终答案时，必须说明目标元素 T 的名次（1 到 N 之间的整数），格式如下：
<answer>{target} is at position R</answer>

其中 R 是你推断的名次数字。
"""

    game_rule_en = """\
Let's play a "Circular Order Ranking" game. Here are the rules:

The game has a positive integer N = {n} and a target element T = {target}. All elements are in the range {{0, 1, ..., N-1}}.

There exists a hidden global linear order over these N elements, determined by an unknown offset. Your goal is to infer the rank of target element T in this global order (ranks range from 1 to N).

You can ask me questions in two ways, and I will answer truthfully based on the hidden global order:

1. **Set Ordering Query**: Provide 2 to 6 distinct elements, and I will tell you their ordering in the global sequence.
   - Format: <query_order>a1,a2,...,ak</query_order>
   - Constraints: k is between 2 and 6; all elements are distinct and in [0, N-1]
   - Returns: These elements arranged in the global order

2. **Pairwise Comparison Query**: Ask which of two elements comes first in the global order.
   - Format: <query_compare>a,b</query_compare>
   - Constraints: a and b are different and both in [0, N-1]
   - Returns: a-before-b or b-before-a

Please ask as few questions as possible. When you are confident, submit the rank of the target element.

Each query must contain only one tag.

- Set Ordering Query (e.g., asking about elements 0, 3, 5):
<query_order>0,3,5</query_order>

- Pairwise Comparison Query (e.g., comparing elements 1 and 4):
<query_compare>1,4</query_compare>

When submitting the final answer, specify the rank of target element T (an integer from 1 to N) in this format:
<answer>{target} is at position R</answer>

where R is the rank number you inferred.
"""

    contextualized_rule_zh_1 = """\
交通调度系统正在运行"环线班车推演"测试。

目前有一条由 N = {n} 个站点组成的环线公交，站点编号依次为 0 到 N-1。
受临时交通管制影响，该环线公交的首发站（即隐藏的偏移量）发生了改变，但车辆依然按站点编号的循环顺序行驶。
你的任务是推断出目标站点 T = {target} 在新的行驶周期中，是第几个到达的站点（名次从 1 到 N）。

你可以通过以下两种指令向调度中心查询，调度中心将根据实际的行驶顺序如实反馈：

1. **多站顺序查询**：输入 2 到 6 个不同的站点编号，调度中心会返回这些站点的实际到达先后顺序。
   - 格式：<query_order>a1,a2,...,ak</query_order>
   - 约束：站点数 k 在 2 到 6 之间；站点编号互不相同且在 [0, N-1] 范围内
   - 返回：这些站点按实际到达先后排序的结果

2. **双站对比查询**：询问两个站点哪一个先到达。
   - 格式：<query_compare>a,b</query_compare>
   - 约束：a 和 b 不同，且均在 [0, N-1] 范围内
   - 返回：a-before-b 或 b-before-a

请以最少的查询次数完成推演。确认答案后，请提交目标站点的到达顺位。

每次提问只能包含一个标签。

- 多站顺序查询（例如查询站点 0, 3, 5 的先后）：
<query_order>0,3,5</query_order>

- 双站对比查询（例如对比站点 1 和 4）：
<query_compare>1,4</query_compare>

提交最终答案时，必须说明目标站点 T 的顺位名次（1 到 N 之间的整数），格式如下：
<answer>{target} is at position R</answer>

其中 R 是你推演出的顺位数字。
"""

    contextualized_rule_en_1 = """\
[Traffic Scenario]
The traffic dispatch system is running a "Circular Shuttle Deduction" test.

There is currently a circular bus route consisting of N = {n} stations, numbered sequentially from 0 to N-1.
Due to temporary traffic control, the starting station (the hidden offset) for this circular route has been altered, but the bus still operates in the cyclic order of the station numbers. 
Your task is to deduce the rank of the target station T = {target} in the new driving cycle (ranks range from 1 to N).

You can query the dispatch center using the following two commands, and the center will provide truthful feedback based on the actual arrival sequence:

1. **Multi-Station Sequence Query**: Provide 2 to 6 distinct station numbers, and the dispatch center will return the actual chronological order of arrival for these stations.
   - Format: <query_order>a1,a2,...,ak</query_order>
   - Constraints: The number of stations k is between 2 and 6; station numbers are distinct and in [0, N-1]
   - Returns: These stations ordered by their actual arrival sequence

2. **Pairwise Station Comparison**: Ask which of two stations arrives first.
   - Format: <query_compare>a,b</query_compare>
   - Constraints: a and b are different and both in [0, N-1]
   - Returns: a-before-b or b-before-a

Please complete the deduction with as few queries as possible. Once you are confident, submit the arrival rank of the target station.

Each query must contain only one tag.

- Multi-Station Sequence Query (e.g., asking about stations 0, 3, 5):
<query_order>0,3,5</query_order>

- Pairwise Station Comparison (e.g., comparing stations 1 and 4):
<query_compare>1,4</query_compare>

When submitting the final answer, specify the arrival rank of target station T (an integer from 1 to N) in this format:
<answer>{target} is at position R</answer>

where R is the rank number you deduced.
"""

    contextualized_rule_zh_2 = """\
医疗排班系统正在运行"环形查房推演"。

医院有一个由 N = {n} 个病房组成的环形查房路线，病房编号依次为 0 到 N-1。
由于突发急诊，今日查房的起始病房（即隐藏的偏移量）发生了改变，但医生仍按病房编号的循环顺序进行查房。
你的任务是推断出目标病房 T = {target} 是今天第几个被查房的（名次从 1 到 N）。

你可以通过以下两种指令向排班系统查询，系统将根据实际的查房顺序如实反馈：

1. **多病房顺序查询**：输入 2 到 6 个不同的病房编号，系统会返回这些病房实际的查房先后顺序。
   - 格式：<query_order>a1,a2,...,ak</query_order>
   - 约束：病房数 k 在 2 到 6 之间；病房编号互不相同且在 [0, N-1] 范围内
   - 返回：这些病房按实际查房先后排序的结果

2. **双病房对比查询**：询问两个病房哪一个先被查房。
   - 格式：<query_compare>a,b</query_compare>
   - 约束：a 和 b 不同，且均在 [0, N-1] 范围内
   - 返回：a-before-b 或 b-before-a

请以最少的查询次数完成推演。确认答案后，请提交目标病房的查房顺位。

每次提问只能包含一个标签。

- 多病房顺序查询（例如查询病房 0, 3, 5 的先后）：
<query_order>0,3,5</query_order>

- 双病房对比查询（例如对比病房 1 和 4）：
<query_compare>1,4</query_compare>

提交最终答案时，必须说明目标病房 T 的顺位名次（1 到 N 之间的整数），格式如下：
<answer>{target} is at position R</answer>

其中 R 是你推演出的顺位数字。
"""

    contextualized_rule_en_2 = """\
[Medical Scenario]
The medical scheduling system is running a "Circular Ward Rounds" deduction scenario.

The hospital has a circular ward round route consisting of N = {n} wards, numbered sequentially from 0 to N-1.
Due to an emergency, the starting ward for today's rounds (the hidden offset) has shifted, but the doctors continue to conduct rounds following the cyclic order of the ward numbers.
Your task is to infer the rank of the target ward T = {target} in today's rounds (ranks range from 1 to N).

You can query the scheduling system using the following two commands, and the system will provide truthful feedback based on the actual rounds sequence:

1. **Multi-Ward Sequence Query**: Provide 2 to 6 distinct ward numbers, and the system will return the actual chronological order of rounds for these wards.
   - Format: <query_order>a1,a2,...,ak</query_order>
   - Constraints: The number of wards k is between 2 and 6; ward numbers are distinct and in [0, N-1]
   - Returns: These wards ordered by their actual round sequence

2. **Pairwise Ward Comparison**: Ask which of two wards is visited first.
   - Format: <query_compare>a,b</query_compare>
   - Constraints: a and b are different and both in [0, N-1]
   - Returns: a-before-b or b-before-a

Please complete the deduction with as few queries as possible. Once you are confident, submit the round rank of the target ward.

Each query must contain only one tag.

- Multi-Ward Sequence Query (e.g., asking about wards 0, 3, 5):
<query_order>0,3,5</query_order>

- Pairwise Ward Comparison (e.g., comparing wards 1 and 4):
<query_compare>1,4</query_compare>

When submitting the final answer, specify the visitation rank of target ward T (an integer from 1 to N) in this format:
<answer>{target} is at position R</answer>

where R is the rank number you deduced.
"""

    contextualized_rule_zh_3 = """\
班级管理系统正在进行"环形值日推演"。

班级有 N = {n} 名学生组成值日循环圈，学号依次从 0 到 N-1。
受节假日调休影响，本周期的起始值日生（即隐藏的偏移量）发生了变动，但依然严格按学号的循环顺序轮替。
你的任务是推断出目标学生 T = {target} 是本周期内第几个值日的（名次从 1 到 N）。

你可以通过以下两种指令向管理系统查询，系统将根据实际的值日轮替顺序如实反馈：

1. **多学生顺序查询**：输入 2 到 6 个不同的学生学号，系统会返回这些学生实际的值日先后顺序。
   - 格式：<query_order>a1,a2,...,ak</query_order>
   - 约束：学生数 k 在 2 到 6 之间；学号互不相同且在 [0, N-1] 范围内
   - 返回：这些学生按实际值日先后排序的结果

2. **双学生对比查询**：询问两名学生哪一个先值日。
   - 格式：<query_compare>a,b</query_compare>
   - 约束：a 和 b 不同，且均在 [0, N-1] 范围内
   - 返回：a-before-b 或 b-before-a

请以最少的查询次数完成推演。确认答案后，请提交目标学生的值日顺位。

每次提问只能包含一个标签。

- 多学生顺序查询（例如查询学号 0, 3, 5 的先后）：
<query_order>0,3,5</query_order>

- 双学生对比查询（例如对比学号 1 和 4）：
<query_compare>1,4</query_compare>

提交最终答案时，必须说明目标学生 T 的顺位名次（1 到 N 之间的整数），格式如下：
<answer>{target} is at position R</answer>

其中 R 是你推演出的顺位数字。
"""

    contextualized_rule_en_3 = """\
[Education Scenario]
The class management system is conducting a "Circular Duty Roster" deduction.

The class has a duty roster loop consisting of N = {n} students, with student IDs sequentially from 0 to N-1.
Due to holiday rescheduling, the starting student on duty for this cycle (the hidden offset) has changed, but the rotation still strictly follows the cyclic order of the student IDs.
Your task is to infer the rank of the target student T = {target} in this duty cycle (ranks range from 1 to N).

You can query the management system using the following two commands, and the system will provide truthful feedback based on the actual duty rotation sequence:

1. **Multi-Student Sequence Query**: Provide 2 to 6 distinct student IDs, and the system will return the actual chronological order of duty for these students.
   - Format: <query_order>a1,a2,...,ak</query_order>
   - Constraints: The number of students k is between 2 and 6; IDs are distinct and in [0, N-1]
   - Returns: These students ordered by their actual duty sequence

2. **Pairwise Student Comparison**: Ask which of two students is on duty first.
   - Format: <query_compare>a,b</query_compare>
   - Constraints: a and b are different and both in [0, N-1]
   - Returns: a-before-b or b-before-a

Please complete the deduction with as few queries as possible. Once you are confident, submit the duty rank of the target student.

Each query must contain only one tag.

- Multi-Student Sequence Query (e.g., asking about IDs 0, 3, 5):
<query_order>0,3,5</query_order>

- Pairwise Student Comparison (e.g., comparing IDs 1 and 4):
<query_compare>1,4</query_compare>

When submitting the final answer, specify the duty rank of target student T (an integer from 1 to N) in this format:
<answer>{target} is at position R</answer>

where R is the rank number you deduced.
"""

    contextualized_rule_zh_4 = """\
工业控制系统正在执行"环形流水线推演"。

一条自动化装配线上有 N = {n} 个环形排列的工位，编号依次为 0 到 N-1。
由于产线维护重启，首个被激活的工位（即隐藏的偏移量）发生了改变，但激活信号仍严格按工位编号的循环顺序传递。
你的任务是确定目标工位 T = {target} 是系统重启后第几个被激活的（名次从 1 到 N）。

你可以通过以下两种指令向控制系统查询，系统将根据实际的激活顺序如实反馈：

1. **多工位顺序查询**：输入 2 到 6 个不同的工位编号，系统会返回这些工位实际的激活先后顺序。
   - 格式：<query_order>a1,a2,...,ak</query_order>
   - 约束：工位数 k 在 2 到 6 之间；工位编号互不相同且在 [0, N-1] 范围内
   - 返回：这些工位按实际激活先后排序的结果

2. **双工位对比查询**：询问两个工位哪一个先被激活。
   - 格式：<query_compare>a,b</query_compare>
   - 约束：a 和 b 不同，且均在 [0, N-1] 范围内
   - 返回：a-before-b 或 b-before-a

请以最少的查询次数完成推演。确认答案后，请提交目标工位的激活顺位。

每次提问只能包含一个标签。

- 多工位顺序查询（例如查询工位 0, 3, 5 的先后）：
<query_order>0,3,5</query_order>

- 双工位对比查询（例如对比工位 1 和 4）：
<query_compare>1,4</query_compare>

提交最终答案时，必须说明目标工位 T 的顺位名次（1 到 N 之间的整数），格式如下：
<answer>{target} is at position R</answer>

其中 R 是你推演出的顺位数字。
"""

    contextualized_rule_en_4 = """\
[Manufacturing/Industrial Scenario]
The industrial control system is executing a "Circular Assembly Line" deduction scenario.

An automated assembly line consists of N = {n} cyclically arranged workstations, numbered sequentially from 0 to N-1.
Due to a production line restart after maintenance, the initially activated workstation (the hidden offset) has changed, but the activation signal still propagates strictly following the cyclic order of the workstation numbers.
Your task is to determine the rank of the target workstation T = {target} in this activation sequence following the restart (ranks range from 1 to N).

You can query the control system using the following two commands, and the system will provide truthful feedback based on the actual activation sequence:

1. **Multi-Workstation Sequence Query**: Provide 2 to 6 distinct workstation numbers, and the system will return the actual chronological order of activation for these workstations.
   - Format: <query_order>a1,a2,...,ak</query_order>
   - Constraints: The number of workstations k is between 2 and 6; workstation numbers are distinct and in [0, N-1]
   - Returns: These workstations ordered by their actual activation sequence

2. **Pairwise Workstation Comparison**: Ask which of two workstations is activated first.
   - Format: <query_compare>a,b</query_compare>
   - Constraints: a and b are different and both in [0, N-1]
   - Returns: a-before-b or b-before-a

Please complete the deduction with as few queries as possible. Once you are confident, submit the activation rank of the target workstation.

Each query must contain only one tag.

- Multi-Workstation Sequence Query (e.g., asking about workstations 0, 3, 5):
<query_order>0,3,5</query_order>

- Pairwise Workstation Comparison (e.g., comparing workstations 1 and 4):
<query_compare>1,4</query_compare>

When submitting the final answer, specify the activation rank of target workstation T (an integer from 1 to N) in this format:
<answer>{target} is at position R</answer>

where R is the rank number you deduced.
"""

    contextualized_rule_zh_5 = """\
法庭程序系统正在进行"圆桌听证推演"。

在一场圆桌听证会上，共有 N = {n} 位发言人参与，发言编号依次为 0 到 N-1。
按照特殊程序规则，全场首位发言人（即隐藏的偏移量）由抽签随机决定，随后严格按编号的循环顺序依次进行发言。
你的任务是推断出目标发言人 T = {target} 是全场第几个发言的（名次从 1 到 N）。

你可以通过以下两种指令向庭审系统查询，系统将根据实际的发言顺序如实反馈：

1. **多发言人顺序查询**：输入 2 到 6 个不同的发言人编号，系统会返回这些人员实际的发言先后顺序。
   - 格式：<query_order>a1,a2,...,ak</query_order>
   - 约束：人员数 k 在 2 到 6 之间；编号互不相同且在 [0, N-1] 范围内
   - 返回：这些发言人按实际发言先后排序的结果

2. **双发言人对比查询**：询问两位发言人哪一位先发言。
   - 格式：<query_compare>a,b</query_compare>
   - 约束：a 和 b 不同，且均在 [0, N-1] 范围内
   - 返回：a-before-b 或 b-before-a

请以最少的查询次数完成推演。确认答案后，请提交目标发言人的发言顺位。

每次提问只能包含一个标签。

- 多发言人顺序查询（例如查询发言人 0, 3, 5 的先后）：
<query_order>0,3,5</query_order>

- 双发言人对比查询（例如对比发言人 1 和 4）：
<query_compare>1,4</query_compare>

提交最终答案时，必须说明目标发言人 T 的顺位名次（1 到 N 之间的整数），格式如下：
<answer>{target} is at position R</answer>

其中 R 是你推演出的顺位数字。
"""

    contextualized_rule_en_5 = """\
[Legal Scenario]
The court procedural system is conducting a "Roundtable Hearing" deduction.

In a roundtable hearing, there are N = {n} speakers participating, with speaker IDs numbered sequentially from 0 to N-1.
According to special procedural rules, the very first speaker of the session (the hidden offset) is randomly determined by drawing lots, after which the floor strictly follows the cyclic order of the speaker IDs.
Your task is to infer the rank of the target speaker T = {target} in the overall speaking session (ranks range from 1 to N).

You can query the hearing system using the following two commands, and the system will provide truthful feedback based on the actual speaking sequence:

1. **Multi-Speaker Sequence Query**: Provide 2 to 6 distinct speaker IDs, and the system will return the actual chronological order of their speeches.
   - Format: <query_order>a1,a2,...,ak</query_order>
   - Constraints: The number of speakers k is between 2 and 6; IDs are distinct and in [0, N-1]
   - Returns: These speakers ordered by their actual speaking sequence

2. **Pairwise Speaker Comparison**: Ask which of two speakers takes the floor first.
   - Format: <query_compare>a,b</query_compare>
   - Constraints: a and b are different and both in [0, N-1]
   - Returns: a-before-b or b-before-a

Please complete the deduction with as few queries as possible. Once you are confident, submit the speaking rank of the target speaker.

Each query must contain only one tag.

- Multi-Speaker Sequence Query (e.g., asking about speakers 0, 3, 5):
<query_order>0,3,5</query_order>

- Pairwise Speaker Comparison (e.g., comparing speakers 1 and 4):
<query_compare>1,4</query_compare>

When submitting the final answer, specify the speaking rank of target speaker T (an integer from 1 to N) in this format:
<answer>{target} is at position R</answer>

where R is the rank number you deduced.
"""

    tags = ["answer", "query_order", "query_compare"]
    
    reasoning_type = "归纳推理"
    data_structure = "序列"

    
    DIFFICULTY_CONFIG = {
        "zh": {
            1: {"n": 5, "offset": 2, "target": 3},
            2: {"n": 8, "offset": 3, "target": 5},
            3: {"n": 12, "offset": 7, "target": 10},
            4: {"n": 16, "offset": 9, "target": 3},
            5: {"n": 20, "offset": 13, "target": 7},
        },
        "en": {
            1: {"n": 5, "offset": 2, "target": 3},
            2: {"n": 8, "offset": 3, "target": 5},
            3: {"n": 12, "offset": 7, "target": 10},
            4: {"n": 16, "offset": 9, "target": 3},
            5: {"n": 20, "offset": 13, "target": 7},
        },
    }

    def __init__(self, config):
        super().__init__(config)

    def _initialize_game(self):
        lang = self.config.language
        diff = self.config.difficulty
        
        if isinstance(diff, str):
            diff = int(diff)

        N_MAP = {1: 5, 2: 8, 3: 12, 4: 16, 5: 20}
        if diff not in N_MAP:
            raise KeyError(f"Unsupported difficulty: {diff}")

        self.n = N_MAP[diff]
        
        rng = random.Random(42 + diff * 1000)
        self.offset = rng.randint(0, self.n - 1)
        self.target = rng.randint(0, self.n - 1)
        
        self.global_order = [(i + self.offset) % self.n for i in range(self.n)]
        
        self.element_to_rank = {}
        for rank, element in enumerate(self.global_order, start=1):
            self.element_to_rank[element] = rank
        
        self.correct_rank = self.element_to_rank[self.target]
        
        self._game_info["n"] = self.n
        self._game_info["target"] = self.target
        
        self.query_count = 0
        self.max_queries = 10

    def _compare_elements(self, a, b):
        rank_a = self.element_to_rank[a]
        rank_b = self.element_to_rank[b]
        return "a-before-b" if rank_a < rank_b else "b-before-a"

    def _sort_elements(self, elements):
        return sorted(elements, key=lambda x: self.element_to_rank[x])

    def evaluate(self, parsed_info):
        raw_ans = parsed_info["answer"].strip()
        
        try:
            parts = raw_ans.split()
            if len(parts) < 5:
                return False
            
            if "position" not in raw_ans.lower():
                return False
            
            rank_str = parts[-1].strip()
            submitted_rank = int(rank_str)
            
            if submitted_rank < 1 or submitted_rank > self.n:
                return False
            
            return submitted_rank == self.correct_rank
            
        except (ValueError, IndexError):
            return False

    def _cf_core_produce(self, parsed_info):
        if self.config.language == "zh":
            error_invalid = "错误：无效的查询。"
            error_format = "错误：格式错误或元素超出范围。"
            error_constraint = "错误：集合排序询问需要 2 到 6 个不同的元素。"
            error_max_queries = f"错误：已达到最大查询次数 {self.max_queries}，请直接提交答案。"
        else:
            error_invalid = "Error: invalid query."
            error_format = "Error: invalid format or element out of range."
            error_constraint = "Error: set ordering query requires 2 to 6 distinct elements."
            error_max_queries = f"Error: maximum query limit ({self.max_queries}) reached. Please submit your answer."

        if self.query_count >= self.max_queries:
            return error_max_queries

        if "query_order" in parsed_info:
            self.query_count += 1
            try:
                raw = parsed_info["query_order"].strip()
                if not raw:
                    return error_format
                
                elements = [int(x.strip()) for x in raw.split(",")]
                
                if len(elements) < 2 or len(elements) > 6:
                    return error_constraint
                
                if len(elements) != len(set(elements)):
                    return error_format
                
                for elem in elements:
                    if elem < 0 or elem >= self.n:
                        return error_format
                
                sorted_elements = self._sort_elements(elements)
                result = ",".join(map(str, sorted_elements))
                
                if self.config.language == "zh":
                    return f"排序结果：[{result}]"
                else:
                    return f"Ordered: [{result}]"
                    
            except (ValueError, AttributeError):
                return error_format

        elif "query_compare" in parsed_info:
            self.query_count += 1
            try:
                raw = parsed_info["query_compare"].strip()
                parts = [x.strip() for x in raw.split(",")]
                
                if len(parts) != 2:
                    return error_format
                
                a, b = int(parts[0]), int(parts[1])
                
                if a == b:
                    return error_format
                
                if a < 0 or a >= self.n or b < 0 or b >= self.n:
                    return error_format
                
                return self._compare_elements(a, b)
                
            except (ValueError, IndexError):
                return error_format

        else:
            return error_invalid

    def _cf_make_wrong(self, correct: str) -> str:
        if "a-before-b" in correct:
            return correct.replace("a-before-b", "b-before-a")
        if "b-before-a" in correct:
            return correct.replace("b-before-a", "a-before-b")
        
        bracket_match = re.search(r'\[([^\]]+)\]', correct)
        if bracket_match:
            elements = bracket_match.group(1).split(",")
            reversed_elements = list(reversed(elements))
            wrong = correct.replace(bracket_match.group(1), ",".join(reversed_elements))
            if wrong != correct:
                return wrong
        
        if correct.strip().isdigit():
            return str(int(correct.strip()) + 1)
        
        return correct + "_WRONG"

    def get_all_possible_queries(self) -> list[dict]:
        queries = []
        
        
        for a in range(self.n):
            for b in range(self.n):
                if a == b:
                    continue
                
                query_content = f"{a},{b}"
                query_full = f"<query_compare>{query_content}</query_compare>"
                
                ans = self._compare_elements(a, b)
                
                queries.append({
                    "query": query_full,
                    "answer": ans
                })
        
        return queries